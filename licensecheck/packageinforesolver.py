"""Get information for installed and online packages."""

from __future__ import annotations

import configparser
import contextlib
import re
from concurrent.futures import ThreadPoolExecutor
from email.message import Message
from importlib import metadata
from importlib.metadata._meta import PackageMetadata
from pathlib import Path
from typing import Any

import license_expression
import requests
import tomli
from boolean.boolean import Expression
from depgather.models.pypijson import ProjectResponse
from depgather.parse import gather
from license_expression import Licensing
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from licensecheck.models.constants import JOINS, UNKNOWN
from licensecheck.models.packageinfo import PackageInfo
from licensecheck.session import session

RAW_JOINS = " AND "
HTTP_OK = 200


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

	def resolve_requirements(
		self,
		requirements_paths: set[str],
		groups: set[str],
		extras: set[str],
		skip_dependencies: set[str],
	) -> None:
		for requirements_path in requirements_paths:
			self.reqs.update(
				gather(
					skipDependencies=skip_dependencies,
					groups=groups,
					extras=extras,
					requirementsPath=Path(requirements_path),
					base_index_url=self.base_pypi_url,
				)
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
		versions: set[str | None] = {None}
		package.name = canonicalize_name(package.name)

		specifier = getattr(package, "specifier", None)
		if specifier is not None:
			parsed_versions = {item.version for item in specifier}
			if parsed_versions:
				versions = parsed_versions

		package.name = canonicalize_name(package.name)

		base_pkg_info: PackageInfo = PackageInfo(
			name=package.name, version=versions.pop(), errorCode=1
		)

		lpi = LocalPackageInfo(package=base_pkg_info)
		rpi = RemotePackageInfo(pypi_api=self.base_pypi_url, package=base_pkg_info)

		pkg_info = PackageInfo(
			name=package.name,
			version=lpi.get_version() or rpi.get_version(),
			size=lpi.get_size() or rpi.get_size(),
			homePage=lpi.get_homePage() or rpi.get_homePage(),
			author=lpi.get_author() or rpi.get_author(),
			license=str(lpi.get_license() or rpi.get_license()),
			errorCode=rpi.http_code if rpi.http_code != HTTP_OK else 0,
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
		self.meta: PackageMetadata = Message()
		with contextlib.suppress(metadata.PackageNotFoundError):
			self.meta = metadata.metadata(package.name)

	def get_license(self) -> str | None:
		return (
			self.meta.get("License-Expression")
			or from_classifiers(self.meta.get_all("Classifier"))
			or self.meta.get("License")
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


class RemotePackageInfo:
	"""Handles retrieval of package info from PyPI."""

	def __init__(self, pypi_api: str, package: PackageInfo) -> None:
		self.pypi_api_pypi = pypi_api + "/pypi"
		self.pypi_api_integrity = pypi_api + "/integrity"
		self.package = package
		self.http_code: int = 0
		self.resp: ProjectResponse = None

	def lazy_fetch(self) -> None:
		if self.resp is None:
			# Attempt to get versioned info first
			rc, raw_resp = self.make_req(
				url=f"{self.pypi_api_pypi}{self.package.name}/{self.package.version}/json"
			)
			# Otherwise just get the latest
			if rc != HTTP_OK:
				rc, raw_resp = self.make_req(url=f"{self.pypi_api_pypi}/{self.package.name}/json")

			self.http_code = rc
			self.resp = ProjectResponse.model_validate(raw_resp)

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
		self.lazy_fetch()
		return self.resp.info.name

	def get_version(self) -> str:
		self.lazy_fetch()
		return self.resp.info.version

	def get_homePage(self) -> str:
		self.lazy_fetch()
		return self.resp.info.home_page

	def get_author(self) -> str:
		self.lazy_fetch()
		author_email = self.resp.info.author_email or ""
		return self.resp.info.author or author_email.split("<")[0].strip()

	def get_license(self) -> str:
		self.lazy_fetch()
		return (
			self.resp.info.license_expression
			or from_classifiers(self.resp.info.classifiers)
			or self.resp.info.license
		)

	def get_size(self) -> int | None:
		self.lazy_fetch()
		urls = self.resp.urls
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
