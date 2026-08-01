"""Get information for installed and online packages."""

from __future__ import annotations

import configparser
import contextlib
import functools
import os
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
from email.message import Message
from importlib import metadata
from importlib.metadata._meta import PackageMetadata
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import url2pathname

import license_expression
import requests
import requirements
import tomli
from boolean.boolean import Expression
from depgather.models.pypijson import ProjectResponse
from depgather.parse import gather
from license_expression import Licensing
from loguru import logger
from packaging.requirements import InvalidRequirement, Requirement
from packaging.utils import canonicalize_name
from packaging.version import InvalidVersion, Version

from licensecheck.models.constants import JOINS, UNKNOWN
from licensecheck.models.packageinfo import PackageInfo
from licensecheck.session import session

RAW_JOINS = " AND "
HTTP_OK = 200

EXPLICIT_LICENSE_ALIASES = {
	"Apache 2.0": "Apache-2.0",
}

# uv can block indefinitely (for example prompting for index credentials), so cap each call
UV_RESOLVE_TIMEOUT_SECONDS = 900
UV_ARTIFACT_TIMEOUT_SECONDS = 600


class UvUnavailableError(RuntimeError):
	"""Raised when the optional uv executable is unavailable."""


@dataclass(frozen=True)
class _UvIndex:
	name: str | None
	url: str
	format: str | None = None


@dataclass(frozen=True)
class _UvResolutionContext:
	directory: Path
	base_index_url: str
	source_url: str | None = None
	index_args: tuple[str, ...] = ()
	index_environment: tuple[tuple[str, str], ...] = ()
	prefer_artifact: bool = False
	remote_matches_source: bool = False


def _has_usable_license(license_value: str | None) -> bool:
	return bool(
		license_value
		and license_value.strip()
		and license_value.strip().upper() not in {UNKNOWN, "NONE"}
	)


@functools.lru_cache(maxsize=1)
def _spdx_licensing() -> Licensing:
	"""
	Build the SPDX licensing index once.

	``license_expression.get_spdx_licensing`` re-reads and re-parses a large vendored JSON
	index on every call, so it must not be called per package.
	"""
	return license_expression.get_spdx_licensing()


def _recognizable_explicit_license(license_value: str | None) -> str | None:
	if not _has_usable_license(license_value):
		return None

	value = str(license_value).strip()
	if re.fullmatch(r"LicenseRef-[A-Za-z0-9.-]+", value, flags=re.IGNORECASE):
		return value
	if value in EXPLICIT_LICENSE_ALIASES:
		return EXPLICIT_LICENSE_ALIASES[value]

	with contextlib.suppress(license_expression.ExpressionError):
		_spdx_licensing().parse(value, validate=True)
		return value
	return None


def _license_from_metadata(
	license_expression_value: str | None,
	classifiers: list[str] | None,
	legacy_license: str | None,
) -> str | None:
	return (
		license_expression_value
		or _recognizable_explicit_license(legacy_license)
		or from_classifiers(classifiers)
		or legacy_license
	)


def _versions_match(expected: str | None, actual: str | None) -> bool:
	if expected is None:
		return True
	if actual is None:
		return False

	try:
		return Version(expected) == Version(actual)
	except InvalidVersion:
		return expected == actual


def _exact_requirement_version(requirement: Requirement | PackageInfo) -> str | None:
	if not isinstance(requirement, Requirement):
		return requirement.version
	versions = {
		item.version
		for item in requirement.specifier
		if item.operator in {"==", "==="} and "*" not in item.version
	}
	return next(iter(versions)) if len(versions) == 1 else None


def _requirement_key(
	requirement: Requirement | PackageInfo,
) -> tuple[str, str | None, str | None]:
	return (
		canonicalize_name(requirement.name),
		_exact_requirement_version(requirement),
		getattr(requirement, "url", None),
	)


@functools.cache
def _normalized_index_url(url: str) -> str:
	parsed = urlparse(url)
	if not parsed.scheme and Path(url).is_absolute():
		return Path(url).resolve().as_uri().rstrip("/")
	if parsed.scheme == "file":
		return Path(url2pathname(parsed.path)).resolve().as_uri().rstrip("/")
	normalized = url.rstrip("/").removesuffix("/simple")
	parsed = urlparse(normalized)
	if parsed.hostname:
		host = parsed.hostname.lower()
		if parsed.port:
			host = f"{host}:{parsed.port}"
		normalized = parsed._replace(netloc=host, query="", fragment="").geturl()
	return normalized


def _is_public_pypi(url: str) -> bool:
	parsed = urlparse(_normalized_index_url(url))
	return parsed.hostname in {"pypi.org", "www.pypi.org"} and parsed.path in {"", "/"}


def _same_index(left: str, right: str) -> bool:
	return _normalized_index_url(left) == _normalized_index_url(right)


def _read_uv_configuration(directory: Path) -> tuple[dict[str, Any], Path]:
	for candidate_directory in (directory, *directory.parents):
		uv_toml = candidate_directory / "uv.toml"
		if uv_toml.is_file():
			return tomli.loads(uv_toml.read_text(encoding="utf-8")), candidate_directory

		pyproject_path = candidate_directory / "pyproject.toml"
		if pyproject_path.is_file():
			pyproject = tomli.loads(pyproject_path.read_text(encoding="utf-8"))
			uv_config = pyproject.get("tool", {}).get("uv")
			if isinstance(uv_config, dict):
				return uv_config, candidate_directory

	return {}, directory


def _resolved_uv_index_url(raw_url: object, config_directory: Path) -> str:
	url = str(raw_url)
	if Path(url).is_absolute() or not urlparse(url).scheme:
		return (config_directory / url).resolve().as_uri()
	return url


def _legacy_uv_indexes(
	config: dict[str, Any],
	config_directory: Path,
) -> list[_UvIndex]:
	indexes: list[_UvIndex] = []
	default_index = config.get("index-url")
	if default_index:
		indexes.append(
			_UvIndex(
				name=None,
				url=_resolved_uv_index_url(default_index, config_directory),
			)
		)
	extra_indexes = config.get("extra-index-url", [])
	if isinstance(extra_indexes, str):
		extra_indexes = [extra_indexes]
	indexes.extend(
		_UvIndex(name=None, url=_resolved_uv_index_url(url, config_directory))
		for url in extra_indexes
	)
	find_links = config.get("find-links", [])
	if isinstance(find_links, str):
		find_links = [find_links]
	indexes.extend(
		_UvIndex(
			name=None,
			url=_resolved_uv_index_url(url, config_directory),
			format="flat",
		)
		for url in find_links
	)
	return indexes


def _configured_uv_indexes(
	uv_config: dict[str, Any],
	config_directory: Path,
) -> list[_UvIndex]:
	raw_indexes = uv_config.get("index", [])
	if isinstance(raw_indexes, dict):
		raw_indexes = [raw_indexes]

	indexes: list[_UvIndex] = []
	for index in raw_indexes:
		if not isinstance(index, dict) or not index.get("url"):
			continue
		indexes.append(
			_UvIndex(
				name=index.get("name"),
				url=_resolved_uv_index_url(index["url"], config_directory),
				format=index.get("format"),
			)
		)

	indexes.extend(_legacy_uv_indexes(uv_config, config_directory))
	pip_config = uv_config.get("pip", {})
	if isinstance(pip_config, dict):
		indexes.extend(_legacy_uv_indexes(pip_config, config_directory))

	return indexes


def _environment_uv_indexes() -> list[_UvIndex]:
	indexes: list[_UvIndex] = []
	for variable in ("UV_INDEX", "UV_EXTRA_INDEX_URL"):
		for value in os.environ.get(variable, "").split():
			if urlparse(value).scheme:
				indexes.append(_UvIndex(name=None, url=value))
				continue
			name, separator, url = value.partition("=")
			indexes.append(_UvIndex(name=name if separator else None, url=url or name))
	indexes.extend(
		_UvIndex(name=None, url=value)
		for variable in ("UV_DEFAULT_INDEX", "UV_INDEX_URL")
		if (value := os.environ.get(variable))
	)
	indexes.extend(
		_UvIndex(name=None, url=value, format="flat")
		for value in os.environ.get("UV_FIND_LINKS", "").split()
	)
	return indexes


def _index_invocation_for_source(
	source_url: str,
	indexes: list[_UvIndex],
) -> tuple[tuple[str, ...], tuple[tuple[str, str], ...]]:
	matching_index = next(
		(index for index in indexes if _same_index(index.url, source_url)),
		None,
	)
	if matching_index is not None and matching_index.format == "flat":
		parsed_index = urlparse(matching_index.url)
		if parsed_index.username or parsed_index.password or parsed_index.query:
			return ("--no-index",), (("UV_FIND_LINKS", matching_index.url),)
		return ("--no-index", "--find-links", matching_index.url), ()

	if matching_index is not None and matching_index.name:
		parsed_index = urlparse(matching_index.url)
		if parsed_index.username or parsed_index.password or parsed_index.query:
			index_value = f"{matching_index.name}={matching_index.url}"
			return (), (("UV_INDEX", index_value),)
		return (
			("--index", f"{matching_index.name}={source_url}"),
			(),
		)

	if matching_index is not None and (
		urlparse(matching_index.url).username
		or urlparse(matching_index.url).password
		or urlparse(matching_index.url).query
	):
		return (), (("UV_INDEX", matching_index.url),)
	if urlparse(source_url).username or urlparse(source_url).password or urlparse(source_url).query:
		return (), (("UV_INDEX", source_url),)

	return ("--index", source_url), ()


def _annotated_requirement_sources(
	raw_requirements: str,
) -> dict[tuple[str, str | None, str | None], str]:
	sources: dict[tuple[str, str | None, str | None], str] = {}
	current_requirement: Requirement | None = None
	for raw_line in raw_requirements.splitlines():
		line = raw_line.strip()
		if line.startswith("# from ") and current_requirement is not None:
			sources[_requirement_key(current_requirement)] = line.removeprefix("# from ").strip()
			continue
		if not line or line.startswith("#"):
			continue
		if line.startswith(("-e ", "--editable ", "--")):
			current_requirement = None
			continue
		try:
			current_requirement = Requirement(line)
		except InvalidRequirement:
			current_requirement = None
	return sources


def _locked_requirement_sources(
	lock_path: Path,
) -> dict[tuple[str, str | None, str | None], str]:
	if not lock_path.is_file():
		return {}

	lock = tomli.loads(lock_path.read_text(encoding="utf-8"))
	sources: dict[tuple[str, str | None, str | None], str] = {}
	for package in lock.get("package", []):
		if not isinstance(package, dict):
			continue
		name = package.get("name")
		version = package.get("version")
		source = package.get("source", {})
		registry = source.get("registry") if isinstance(source, dict) else None
		if name and registry:
			sources[(canonicalize_name(name), version, None)] = str(registry)
	return sources


def _editable_project_path(line: str, base_path: Path) -> Path | None:
	stripped_line = line.strip()
	for prefix in ("-e ", "--editable "):
		if stripped_line.startswith(prefix):
			target = stripped_line.removeprefix(prefix).strip()
			break
	else:
		return None

	parsed_url = urlparse(target)
	if parsed_url.scheme and parsed_url.scheme != "file":
		return None

	if parsed_url.scheme == "file":
		path = Path(url2pathname(parsed_url.path))
	else:
		# A bare path is not a URL; only strip a trailing "#egg=" style fragment.
		path = Path(target.split("#", 1)[0])
	if not path.is_absolute():
		path = base_path / path
	return path.resolve()


def _requirement_project_path(requirement: Requirement, base_path: Path) -> Path | None:
	if not requirement.url:
		return None
	parsed_url = urlparse(requirement.url)
	if parsed_url.scheme != "file":
		return None

	path = Path(url2pathname(parsed_url.path))
	if not path.is_absolute():
		path = base_path / path
	return path.resolve()


def _parse_uv_requirements(
	raw_requirements: str,
	skip_dependencies: set[str],
	base_path: Path,
) -> tuple[
	set[Requirement],
	set[Path],
	dict[tuple[str, str | None, str | None], str],
]:
	skip_names = {canonicalize_name(name) for name in skip_dependencies}
	parsed_requirements: set[Requirement] = set()
	editable_paths: set[Path] = set()

	for parsed in requirements.parse(raw_requirements):
		if parsed.editable:
			if editable_path := _editable_project_path(parsed.line, base_path):
				editable_paths.add(editable_path)
			continue
		if not parsed.name or canonicalize_name(parsed.name) in skip_names:
			continue

		requirement = Requirement(parsed.line)
		requirement.name = canonicalize_name(requirement.name)
		parsed_requirements.add(requirement)

	return parsed_requirements, editable_paths, _annotated_requirement_sources(raw_requirements)


def _uv_requirement_command(
	requirements_path: Path,
	*,
	use_lock: bool,
	base_index_url: str,
) -> list[str]:
	if use_lock:
		return [
			"uv",
			"export",
			"--project",
			requirements_path.parent.as_posix(),
			"--format",
			"requirements.txt",
			"--locked",
			"--no-hashes",
			"--no-header",
			"--no-default-groups",
			"--no-emit-project",
			"--color",
			"never",
		]

	command = [
		"uv",
		"pip",
		"compile",
		"--color",
		"never",
		"--emit-index-annotation",
	]
	if not _is_public_pypi(base_index_url):
		command.extend(["--default-index", base_index_url])
	command.append(requirements_path.as_posix())
	return command


def _gather_uv_requirements(
	requirements_path: Path,
	groups: set[str],
	extras: set[str],
	skip_dependencies: set[str],
	base_index_url: str,
) -> tuple[
	set[Requirement],
	set[Path],
	dict[tuple[str, str | None, str | None], str],
]:
	requirements_path = requirements_path.resolve()
	lock_path = requirements_path.with_name("uv.lock")
	use_lock = requirements_path.name == "pyproject.toml" and lock_path.is_file()
	command = _uv_requirement_command(
		requirements_path,
		use_lock=use_lock,
		base_index_url=base_index_url,
	)
	for group in groups:
		command.extend(["--group", group])
	for extra in extras:
		command.extend(["--extra", extra])

	if not use_lock and requirements_path.name == "pyproject.toml":
		pyproject = tomli.loads(requirements_path.read_text(encoding="utf-8"))
		prerelease = pyproject.get("tool", {}).get("uv", {}).get("prerelease")
		if prerelease:
			command.extend(["--prerelease", prerelease])

	try:
		result = subprocess.run(  # noqa: S603
			command,
			capture_output=True,
			text=True,
			check=False,
			cwd=requirements_path.parent,
			stdin=subprocess.DEVNULL,
			timeout=UV_RESOLVE_TIMEOUT_SECONDS,
		)
	except FileNotFoundError as error:
		raise UvUnavailableError from error
	except subprocess.TimeoutExpired as error:
		message = f"Timed out after {UV_RESOLVE_TIMEOUT_SECONDS}s running: {' '.join(command)}"
		raise RuntimeError(message) from error
	except OSError as error:
		raise RuntimeError from error

	if result.returncode != 0:
		message = f"Non-zero returncode: {result.stderr}, {result.stdout}"
		raise RuntimeError(message)

	parsed_requirements, editable_paths, sources = _parse_uv_requirements(
		result.stdout,
		skip_dependencies,
		requirements_path.parent.resolve(),
	)
	if use_lock:
		sources.update(_locked_requirement_sources(lock_path))
	return parsed_requirements, editable_paths, sources


def _project_indexes(directory: Path) -> list[_UvIndex]:
	"""
	Collect the uv indexes that apply to ``directory``.

	This reads configuration files and the environment, so it is resolved once per
	requirements file rather than once per requirement.
	"""
	uv_config, config_directory = _read_uv_configuration(directory)
	return [
		*_configured_uv_indexes(uv_config, config_directory),
		*_environment_uv_indexes(),
	]


def _resolution_context(
	directory: Path,
	indexes: list[_UvIndex],
	requirement: Requirement,
	source_url: str | None,
	base_index_url: str,
) -> _UvResolutionContext:
	index_args, index_environment = (
		_index_invocation_for_source(source_url, indexes) if source_url else ((), ())
	)
	has_custom_index = any(not _is_public_pypi(index.url) for index in indexes)
	prefer_artifact = bool(
		requirement.url
		or (source_url and not _is_public_pypi(source_url))
		or (source_url is None and has_custom_index)
		or not _is_public_pypi(base_index_url)
	)
	remote_matches_source = bool(
		(source_url and _same_index(source_url, base_index_url))
		or (source_url is None and not requirement.url and not _is_public_pypi(base_index_url))
	)
	return _UvResolutionContext(
		directory=directory,
		base_index_url=base_index_url,
		source_url=source_url,
		index_args=index_args,
		index_environment=index_environment,
		prefer_artifact=prefer_artifact,
		remote_matches_source=remote_matches_source,
	)


class PackageInfoManager:
	"""Manages retrieval of local and remote package information."""

	def __init__(self, base_pypi_url: str = "https://pypi.org") -> None:
		"""
		Manage retrieval of local and remote package information.

		:param str pypi_api: url of pypi server. Typically the public instance, defaults
		to "https://pypi.org"
		"""
		self.base_pypi_url = base_pypi_url
		self.reqs: set[Requirement] = set()
		self.local_projects: dict[str, PackageInfo] = {}
		self.resolution_contexts: dict[
			tuple[str, str | None, str | None], _UvResolutionContext
		] = {}

	def resolve_requirements(
		self,
		requirements_paths: set[str],
		groups: set[str],
		extras: set[str],
		skip_dependencies: set[str],
	) -> None:
		for requirements_path in requirements_paths:
			requirements_path_obj = Path(requirements_path).resolve()
			try:
				resolved_requirements, editable_paths, source_urls = _gather_uv_requirements(
					requirements_path=requirements_path_obj,
					groups=groups,
					extras=extras,
					skip_dependencies=skip_dependencies,
					base_index_url=self.base_pypi_url,
				)
			except RuntimeError as error:
				# UvUnavailableError is a RuntimeError; only a genuine resolution failure
				# for a pyproject.toml is fatal.
				if not isinstance(error, UvUnavailableError) and (
					requirements_path_obj.name == "pyproject.toml"
				):
					raise
				logger.warning(
					f"Falling back to the legacy resolver for {requirements_path_obj}: {error}"
				)
				resolved_requirements = gather(
					skipDependencies=skip_dependencies,
					groups=groups,
					extras=extras,
					requirementsPath=requirements_path_obj,
					base_index_url=self.base_pypi_url,
				)
				editable_paths = set()
				source_urls = {}

			self._register_editable_projects(
				resolved_requirements,
				editable_paths,
				skip_dependencies,
			)
			self._register_direct_local_projects(
				resolved_requirements,
				requirements_path_obj.parent,
			)
			directory = requirements_path_obj.parent.resolve()
			indexes = _project_indexes(directory)
			for requirement in resolved_requirements:
				key = _requirement_key(requirement)
				self.resolution_contexts[key] = _resolution_context(
					directory,
					indexes,
					requirement,
					source_urls.get(key),
					self.base_pypi_url,
				)
			self.reqs.update(resolved_requirements)

	def _register_editable_projects(
		self,
		resolved_requirements: set[Requirement],
		editable_paths: set[Path],
		skip_dependencies: set[str],
	) -> None:
		skip_names = {canonicalize_name(name) for name in skip_dependencies}
		for editable_path in editable_paths:
			pyproject_path = (
				editable_path
				if editable_path.name == "pyproject.toml"
				else editable_path / "pyproject.toml"
			)
			package = self._read_project_package(pyproject_path)
			if package is None:
				continue

			self.local_projects[package.name] = package
			if package.name in skip_names:
				continue

			requirement = package.name
			if package.version:
				requirement = f"{requirement}=={package.version}"
			resolved_requirements.add(Requirement(requirement))

	def _register_direct_local_projects(
		self,
		resolved_requirements: set[Requirement],
		base_path: Path,
	) -> None:
		for requirement in resolved_requirements:
			project_path = _requirement_project_path(requirement, base_path)
			if project_path is None:
				continue
			pyproject_path = (
				project_path
				if project_path.name == "pyproject.toml"
				else project_path / "pyproject.toml"
			)
			package = self._read_project_package(pyproject_path)
			if package is not None and package.name == canonicalize_name(requirement.name):
				self.local_projects[package.name] = package

	@staticmethod
	def _read_project_package(pyproject_path: Path) -> PackageInfo | None:
		if not pyproject_path.is_file():
			return None

		pyproject = tomli.loads(pyproject_path.read_text(encoding="utf-8"))
		tool = pyproject.get("tool", {})
		project = (
			pyproject.get("project")
			or tool.get("poetry")
			or tool.get("flit", {}).get("metadata", {})
		)
		if not isinstance(project, dict):
			return None

		name = project.get("name") or project.get("dist-name") or project.get("module")
		if not name:
			return None

		license_value = project.get("license", UNKNOWN)
		if isinstance(license_value, dict):
			license_value = license_value.get("text", UNKNOWN)
		if not _has_usable_license(str(license_value)):
			license_value = from_classifiers(project.get("classifiers")) or UNKNOWN
		license_value = normalize_license(str(license_value))

		authors = project.get("authors", project.get("author", []))
		if isinstance(authors, str):
			authors = [authors]
		author_names = [
			author.get("name", "") if isinstance(author, dict) else str(author)
			for author in authors
		]
		project_urls = project.get("urls", {})
		if not isinstance(project_urls, dict):
			project_urls = {}

		return PackageInfo(
			name=canonicalize_name(name),
			version=project.get("version"),
			homePage=(
				project_urls.get("Homepage")
				or project_urls.get("homepage")
				or project.get("homepage")
				or project.get("home-page")
			),
			author=", ".join(filter(None, author_names)),
			license=license_value,
			errorCode=0,
		)

	def getPackages(self) -> set[PackageInfo]:
		"""
		Retrieve package information from local installation or PyPI.

		:param set[str] reqs: Set of dependency names to retrieve information for.
		:return set[PackageInfo]: A set of package information objects.
		"""
		with ThreadPoolExecutor() as executor:
			return set(executor.map(self._get_package_info, self.reqs))

	def _get_package_info(self, package: Requirement) -> PackageInfo:
		"""
		Retrieve package information, preferring local info.

		:param Requirement package: package info to unpack
		:return PackageInfo: Information about the package.
		"""
		context = self.resolution_contexts.get(_requirement_key(package))
		package.name = canonicalize_name(package.name)

		if local_project := self.local_projects.get(package.name):
			local_package = replace(local_project)
			if local_package.license:
				local_package.license = normalize_license(local_package.license)
			return local_package

		base_pkg_info: PackageInfo = PackageInfo(
			name=package.name,
			version=_exact_requirement_version(package),
			errorCode=1,
		)

		lpi = LocalPackageInfo(package=base_pkg_info)
		resolved_source = context is not None and (
			context.source_url is not None or context.prefer_artifact
		)
		local_matches = not resolved_source and _versions_match(
			base_pkg_info.version,
			lpi.get_version(),
		)
		local_name = lpi.get_name() if local_matches else None
		local_license = lpi.get_license() if local_matches else None

		preferred_index: IndexPackageInfo | None = None
		if context is not None and context.prefer_artifact:
			preferred_index = IndexPackageInfo(
				package=base_pkg_info,
				requirement=package,
				context=context,
			)
			if preferred_index.get_name():
				pkg_info = PackageInfo(
					name=package.name,
					version=base_pkg_info.version or preferred_index.get_version(),
					homePage=preferred_index.get_homePage(),
					author=preferred_index.get_author(),
					license=preferred_index.get_license(),
					errorCode=0,
				)
				if pkg_info.license:
					pkg_info.license = normalize_license(pkg_info.license)
				return pkg_info
			if not context.remote_matches_source:
				return PackageInfo(
					name=package.name,
					version=base_pkg_info.version,
					errorCode=1,
				)

		rpi = RemotePackageInfo(pypi_api=self.base_pypi_url, package=base_pkg_info)
		rpi.lazy_fetch()
		remote_license = rpi.get_license()

		needs_index = (not local_name and rpi.http_code != HTTP_OK) or not any(
			_has_usable_license(value) for value in (local_license, remote_license)
		)
		# Reuse the artifact fetch already attempted above rather than re-running `uv pip install`
		ipi = preferred_index
		if ipi is None and needs_index:
			ipi = IndexPackageInfo(
				package=base_pkg_info,
				requirement=package,
				context=context,
			)
		index_name = ipi.get_name() if ipi is not None else None
		index_license = ipi.get_license() if ipi is not None else None
		license_candidates = (local_license, index_license, remote_license)
		license_value = next(
			(value for value in license_candidates if _has_usable_license(value)),
			next((value for value in license_candidates if value), None),
		)

		pkg_info = PackageInfo(
			name=package.name,
			version=base_pkg_info.version
			or (lpi.get_version() if local_matches else None)
			or (ipi.get_version() if ipi is not None else None)
			or rpi.get_version(),
			size=(lpi.get_size() if local_matches else None)
			or (ipi.get_size() if ipi is not None else None)
			or rpi.get_size(),
			homePage=(lpi.get_homePage() if local_matches else None)
			or (ipi.get_homePage() if ipi is not None else None)
			or rpi.get_homePage(),
			author=(lpi.get_author() if local_matches else None)
			or (ipi.get_author() if ipi is not None else None)
			or rpi.get_author(),
			license=license_value,
			errorCode=(
				0 if rpi.http_code == HTTP_OK or local_name or index_name else rpi.http_code
			),
		)

		# normailzing the license
		if pkg_info.license:
			pkg_info.license = normalize_license(pkg_info.license)

		return pkg_info


def normalize_license(lice: str) -> str:
	licensing = Licensing()
	parsed = None
	with contextlib.suppress(license_expression.ExpressionParseError):
		parsed = licensing.parse(re.sub(r"[^a-zA-Z0-9_.:\- ]", "_", lice.splitlines()[0]))
	if parsed is None:
		return lice

	tokens: list[Expression] = sorted(parsed.literals)
	return str(JOINS.join(getattr(x, "key", str(x)) for x in tokens))


class LocalPackageInfo:
	"""Handles retrieval of package info from local installation."""

	def __init__(self, package: PackageInfo) -> None:
		self.package: PackageInfo = package
		# email message appears to mostly conform to the protocol
		# https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata
		self.meta: Message[str, str] | PackageMetadata = Message()
		with contextlib.suppress(metadata.PackageNotFoundError):
			self.meta = metadata.metadata(package.name)

	def get_license(self) -> str | None:
		return _license_from_metadata(
			self.meta.get("License-Expression"),
			self.meta.get_all("Classifier"),
			self.meta.get("License"),
		)

	def get_name(self) -> str | None:
		return self.meta.get("Name")

	def get_version(self) -> str | None:
		return self.meta.get("Version")

	def get_homePage(self) -> str | None:
		return self.meta.get("Home-page")

	def get_author(self) -> str | None:
		return self.meta.get("Author")

	def get_size(self) -> int | None:
		"""
		Retrieve installed package size.

		:param str package: Package name.
		:return int: Size in bytes.
		"""
		try:
			package_files = metadata.Distribution.from_name(self.package.name).files
			return sum(f.size for f in package_files if f.size) if package_files else 0
		except metadata.PackageNotFoundError:
			return None  # Package not found


class IndexPackageInfo:
	"""Handles package metadata from indexes configured for uv."""

	def __init__(
		self,
		package: PackageInfo,
		requirement: Requirement | PackageInfo | None = None,
		context: _UvResolutionContext | None = None,
	) -> None:
		self.package = package
		self.requirement = requirement
		self.context = context
		self.meta: Message[str, str] | PackageMetadata = Message()
		self.fetched = False

	def lazy_fetch(self) -> None:
		if self.fetched:
			return
		self.fetched = True

		requirement_url = getattr(self.requirement, "url", None)
		requirement = str(self.requirement) if requirement_url else self.package.name
		if self.package.version and not requirement_url:
			requirement = f"{requirement}=={self.package.version}"

		with tempfile.TemporaryDirectory(prefix="licensecheck-") as target:
			command = [
				"uv",
				"pip",
				"install",
				"--color",
				"never",
				"--no-progress",
				"--no-deps",
				"--only-binary",
				":all:",
				"--target",
				target,
			]
			if self.context is not None:
				if not _is_public_pypi(self.context.base_index_url):
					command.extend(["--default-index", self.context.base_index_url])
				command.extend(self.context.index_args)
			command.append(requirement)
			run_environment = None
			if self.context is not None and self.context.index_environment:
				run_environment = os.environ.copy()
				run_environment.update(dict(self.context.index_environment))
			try:
				result = subprocess.run(  # noqa: S603
					command,
					capture_output=True,
					text=True,
					check=False,
					cwd=self.context.directory if self.context is not None else None,
					env=run_environment,
					stdin=subprocess.DEVNULL,
					timeout=UV_ARTIFACT_TIMEOUT_SECONDS,
				)
			except (OSError, subprocess.TimeoutExpired) as error:
				logger.warning(f"Could not fetch the artifact for {self.package.name}: {error}")
				return

			if result.returncode != 0:
				logger.warning(
					f"Could not fetch the artifact for {self.package.name}: {result.stderr}"
				)
				return

			for distribution in metadata.distributions(path=[target]):
				name = distribution.metadata.get("Name")
				if name and canonicalize_name(name) == self.package.name:
					self.meta = distribution.metadata
					return

	def get_license(self) -> str | None:
		self.lazy_fetch()
		return _license_from_metadata(
			self.meta.get("License-Expression"),
			self.meta.get_all("Classifier"),
			self.meta.get("License"),
		)

	def get_name(self) -> str | None:
		self.lazy_fetch()
		return self.meta.get("Name")

	def get_version(self) -> str | None:
		self.lazy_fetch()
		return self.meta.get("Version")

	def get_homePage(self) -> str | None:
		self.lazy_fetch()
		return self.meta.get("Home-page")

	def get_author(self) -> str | None:
		self.lazy_fetch()
		return self.meta.get("Author")

	def get_size(self) -> None:
		return None


class RemotePackageInfo:
	"""Handles retrieval of package info from PyPI."""

	def __init__(self, pypi_api: str, package: PackageInfo) -> None:
		self.pypi_api_pypi = pypi_api + "/pypi"
		self.pypi_api_integrity = pypi_api + "/integrity"
		self.package = package
		self.http_code: int = 0
		self.resp: ProjectResponse | None = None

	def lazy_fetch(self) -> None:
		if self.resp is None:
			if self.package.version:
				rc, raw_resp = self.make_req(
					url=f"{self.pypi_api_pypi}/{self.package.name}/{self.package.version}/json"
				)
			else:
				rc, raw_resp = self.make_req(url=f"{self.pypi_api_pypi}/{self.package.name}/json")

			self.http_code = rc
			self.resp = ProjectResponse.model_validate(raw_resp)

	def _response(self) -> ProjectResponse:
		self.lazy_fetch()
		if self.resp is None:
			message = "Package metadata response was not initialized"
			raise RuntimeError(message)
		return self.resp

	def make_req(
		self, url: str, headers: dict[str, str] | None = None
	) -> tuple[int, dict[str, Any]]:
		headers = headers or {}
		try:
			r = session.get(url, headers=headers, timeout=60)

			return r.status_code, r.json()
		except requests.exceptions.JSONDecodeError:
			return -1, {}
		except requests.exceptions.RequestException:
			return -2, {}

	def get_name(self) -> str:
		return self._response().info.name

	def get_version(self) -> str:
		return self._response().info.version

	def get_homePage(self) -> str:
		return self._response().info.home_page

	def get_author(self) -> str:
		response = self._response()
		author_email = response.info.author_email or ""
		return response.info.author or author_email.split("<")[0].strip()

	def get_license(self) -> str:
		response = self._response()
		return _license_from_metadata(
			response.info.license_expression,
			response.info.classifiers,
			response.info.license,
		)

	def get_size(self) -> int | None:
		urls = self._response().urls
		return urls[-1].size if len(urls) > 0 else None


def from_classifiers(classifiers: list[str] | None) -> str | None:
	"""
	Extract license from classifiers.

	:param list[str] | None classifiers: list of classifiers
	:return str: licenses as a str
	"""
	if not classifiers:
		return None

	licenses: list[str] = []
	for _val in classifiers:
		val = str(_val)
		if val.startswith("License"):
			lice = val.rsplit(" :: ", maxsplit=1)[-1]
			if lice != "OSI Approved":
				licenses.append(lice)
	return RAW_JOINS.join(licenses) if len(licenses) > 0 else None


class ProjectMetadata:
	"""Handles extraction of project metadata from configuration files."""

	@staticmethod
	def get_metadata() -> dict[str, Any]:
		"""
		Extract project metadata from setup.cfg or pyproject.toml.

		:return dict[str, Any]: Extracted metadata.
		"""
		if Path("setup.cfg").exists():
			config = configparser.ConfigParser()
			config.read("setup.cfg")
			if "metadata" in config:
				classifiers = config.get("metadata", "classifier", fallback="").strip().splitlines()
				license_str = str(config.get("metadata", "license", fallback=""))
				return {"classifiers": classifiers, "license": license_str}

		if Path("pyproject.toml").exists():
			pyproject = tomli.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
			tool = pyproject.get("tool", {})
			return (
				pyproject.get("project", {})
				or tool.get("poetry")
				or tool.get("flit", {}).get("metadata", {})
			)

		return {"classifiers": [], "license": UNKNOWN}

	@staticmethod
	def get_license() -> str:
		"""
		Extract license from project metadata.

		:return str: License string.
		"""
		metadata = ProjectMetadata.get_metadata()
		license_str = from_classifiers(metadata.get("classifiers", []))

		if license_str is not None:
			return str(license_str)

		if isinstance(metadata.get("license"), dict):
			return str(metadata["license"].get("text", UNKNOWN))

		return str(metadata.get("license", UNKNOWN))
