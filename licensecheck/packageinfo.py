"""Get information for installed and online packages."""

from __future__ import annotations

import configparser
import contextlib
import re
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from email.message import Message
from importlib import metadata
from pathlib import Path
from typing import Any

import license_expression
import requests
import tomli
from depgather.parse import gather
from license_expression import Licensing
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from licensecheck.models.constants import JOINS, UNKNOWN
from licensecheck.models.packageinfo import PackageInfo
from licensecheck.session import session

RAW_JOINS = " AND "


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
		Retrieve package information, preferring local data.

		:param Requirement package: package info to unpack
		:return PackageInfo: Information about the package.
		"""
		versions = {None}
		try:
			requirement_specs = package.specifier._specs
			versions = {x._spec[1] for x in requirement_specs}
		except AttributeError:
			pass

		# current version of depgather does not c14n names on its output
		package.name = canonicalize_name(package.name)
		base_pkg_info: PackageInfo = PackageInfo(
			name=package.name, version=versions.pop(), errorCode=1
		)

		lpi = LocalPackageInfo(package=base_pkg_info)
		rpi = RemotePackageInfo(pypi_api=self.base_pypi_url + "/pypi", package=base_pkg_info)

		pkg_info = PackageInfo(
			name=package.name,
			version=lpi.get_version() or rpi.get_version(),
			size=lpi.get_size() or rpi.get_size(),
			homePage=lpi.get_homePage() or rpi.get_homePage(),
			author=lpi.get_author() or rpi.get_author(),
			license=str(lpi.get_license() or rpi.get_license()),
		)

		if rpi.error_state:
			pkg_info.errorCode = 1

		if pkg_info.license:
			licensing = Licensing()
			parsed = None
			with contextlib.suppress(license_expression.ExpressionParseError):
				parsed = licensing.parse(
					re.sub(r"[^a-zA-Z0-9_.:\- ]", "_", pkg_info.license.splitlines()[0])
				)
			if parsed is None:
				return pkg_info

			tokens = sorted(parsed.literals)
			pkg_info.license = str(JOINS.join(x.key for x in tokens))

		return pkg_info


class LocalPackageInfo:
	"""Handles retrieval of package info from local installation."""

	def __init__(self, package: PackageInfo) -> None:
		self.package = package
		try:
			self.meta = metadata.metadata(package.name)
		except metadata.PackageNotFoundError:
			# In the event of an error create an empty dict like object
			self.meta = Message()

	def get_license(self) -> str | None:
		return (
			meta_get(self.meta, "License_Expression")
			or from_classifiers(self.meta.get_all("Classifier"))
			or meta_get(self.meta, "License")
		)

	def get_name(self) -> str | None:
		return meta_get(self.meta, "Name")

	def get_version(self) -> str | None:
		return meta_get(self.meta, "Version")

	def get_homePage(self) -> str | None:
		return meta_get(self.meta, "Home-page")

	def get_author(self) -> str | None:
		return meta_get(self.meta, "Author")

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
		self.pypi_api = pypi_api
		self.package = package
		self.raw_data: dict[str, Any] = None  # type: ignore # Becuase we lateinit this
		self.error_state = None

	def poke_pypi(self) -> None:
		if self.raw_data is None:
			# Attempt to get versioned data first
			data = (
				self.make_req(
					url=f"{self.pypi_api}/{self.package.name}/{self.package.version}/json"
				)
				if self.package.version
				else None
			)
			# Otherwise just get the latest
			if not data:
				data = self.make_req(url=f"{self.pypi_api}/{self.package.name}/json")
			self.raw_data = data

	def make_req(self, url: str) -> dict[str, Any]:
		try:
			response = session.get(url, timeout=60)

			if response.status_code != 200:
				self.error_state = f"{response.status_code} when contacting {url}"
				return {}

			return response.json().get("info", {})
		except requests.exceptions.JSONDecodeError:
			self.error_state = f"Unable to decode package info from {url}"
			return {}
		except requests.exceptions.RequestException:
			self.error_state = f"Some exception when contacting {url}"
			return {}

	def get_license(self) -> str | None:
		self.poke_pypi()
		return (
			meta_get(self.raw_data, "license_expression")
			or from_classifiers(self.raw_data.get("classifiers", []))
			or meta_get(self.raw_data, "license")
		)

	def get_name(self) -> str | None:
		self.poke_pypi()
		return meta_get(self.raw_data, "name")

	def get_version(self) -> str | None:
		self.poke_pypi()
		return meta_get(self.raw_data, "version")

	def get_homePage(self) -> str | None:
		self.poke_pypi()
		return meta_get(self.raw_data, "home_page")

	def get_author(self) -> str | None:
		self.poke_pypi()
		author = meta_get(self.raw_data, "author")
		author_email = meta_get(self.raw_data, "author_email") or ""

		return author or author_email.split("<")[0].strip()

	def get_size(self) -> int | None:
		"""
		Retrieve package size from PyPI metadata.

		:param dict[str, Any] data: PyPI response JSON.

		:return int: Package size in bytes.
		"""
		self.poke_pypi()
		if self.raw_data is None:
			return None
		urls = self.raw_data.get("urls", [])
		return int(urls[-1]["size"]) if len(urls) > 0 else None


def meta_get(meta: Message | dict[str, Any], key: str) -> str | None:
	"""
	Retrieve metadata value safely.

	:param Message | dict[str, Any] self.meta: Metadata source.
	:param str key: Metadata key.
	:return str: Retrieved metadata value.
	"""
	value = meta.get(key)
	if isinstance(value, Iterable) and not isinstance(value, str):
		return RAW_JOINS.join(str(x) for x in value)
	return str(value) if value else None


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
