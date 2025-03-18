"""Get information for installed and online packages."""

from __future__ import annotations

import configparser
import contextlib
import re
from collections.abc import Iterable
from email.message import Message
from importlib import metadata
from pathlib import Path
from typing import Any

import license_expression
import requests
import tomli
from license_expression import Licensing
from loguru import logger

from licensecheck.resolvers import native as res_native
from licensecheck.resolvers import uv as res_uv
from licensecheck.session import session
from licensecheck.types import JOINS, UNKNOWN, PackageInfo, ucstr

RAW_JOINS = " AND "


class PackageInfoManager:
	"""Manages retrieval of local and remote package information."""

	def __init__(self, base_pypi_url: str = "https://pypi.org") -> None:
		"""Manage retrieval of local and remote package information.

		:param str pypi_api: url of pypi server. Typically the public instance, defaults
		to "https://pypi.org"
		"""
		self.base_pypi_url = base_pypi_url
		self.pypi_api = base_pypi_url + "/pypi/"
		self.pypi_search = base_pypi_url + "/simple/"

	def resolve_requirements(
		self,
		requirements_paths: list[str],
		groups: list[str],
		extras: list[str],
		skip_dependencies: list[ucstr],
	) -> None:
		try:
			self.reqs = res_uv.get_reqs(
				skipDependencies=skip_dependencies,
				groups=groups,
				extras=extras,
				requirementsPaths=requirements_paths,
				index_url=self.pypi_search,
			)
			return

		except RuntimeError as e:
			logger.warning(e)
			pyproject = {}
			if "pyproject.toml" in requirements_paths:
				pyproject = tomli.loads(Path("pyproject.toml").read_text("utf-8"))

			# Fallback to the old resolver (hopefully we can deprecate this asap!)
			self.reqs = res_native.get_reqs(
				skipDependencies=skip_dependencies,
				extras=groups,
				pyproject=pyproject,
				requirementsPaths=[Path(x) for x in requirements_paths],
			)
			return

	def getPackages(self) -> set[PackageInfo]:
		"""Retrieve package information from local installation or PyPI.

		:param set[ucstr] reqs: Set of dependency names to retrieve information for.
		:return set[PackageInfo]: A set of package information objects.
		"""
		package_info_set = set()

		for package in self.reqs:
			package_info = self.get_package_info(package)
			package_info_set.add(package_info)

		return package_info_set

	def get_package_info(self, package: PackageInfo) -> PackageInfo:
		"""Retrieve package information, preferring local data.

		:param ucstr pacage: Package name.
		:return PackageInfo: Information about the package.
		"""
		pkg_info = PackageInfo(name=package.name, version=package.version, errorCode=1)

		lpi = LocalPackageInfo(package=package)
		rpi = RemotePackageInfo(pypi_api=self.pypi_api, package=package)

		pkg_info = PackageInfo(
			name=package.name,
			version=lpi.get_version() or rpi.get_version(),
			size=lpi.get_size() or rpi.get_size(),
			homePage=lpi.get_homePage() or rpi.get_homePage(),
			author=lpi.get_author() or rpi.get_author(),
			license=ucstr(lpi.get_license() or rpi.get_license()),
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
			pkg_info.license = ucstr(JOINS.join(x.key for x in tokens))

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

	def get_size(self) -> int:
		"""Retrieve installed package size.

		:param ucstr package: Package name.
		:return int: Size in bytes.
		"""
		try:
			package_files = metadata.Distribution.from_name(self.package.name).files
			return sum(f.size for f in package_files if f.size) if package_files else 0
		except metadata.PackageNotFoundError:
			return 0  # Package not found


class RemotePackageInfo:
	"""Handles retrieval of package info from PyPI."""

	def __init__(self, pypi_api: str, package: PackageInfo) -> None:
		self.pypi_api = pypi_api
		self.package = package
		self.raw_data: dict = None  # type: ignore # Becuase we lateinit this
		self.error_state = None

	def poke_pypi(self) -> None:
		if self.raw_data is None:
			# Attempt to get versioned data first
			data = (
				self.make_req(url=f"{self.pypi_api}{self.package.name}/{self.package.version}/json")
				if self.package.version
				else None
			)
			# Otherwise just get the latest
			if not data:
				data = self.make_req(url=f"{self.pypi_api}{self.package.name}/json")
			self.raw_data = data

	def make_req(self, url: str) -> dict:
		try:
			response = session.get(url, timeout=60)

			if response.status_code != 200:
				self.error_state = f"Non-200 when contacting {url}"
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
		return meta_get(self.raw_data, "author")

	def get_size(self) -> int:
		"""Retrieve package size from PyPI metadata.

		:param dict[str, Any] data: PyPI response JSON.

		:return int: Package size in bytes.
		"""
		self.poke_pypi()
		if self.raw_data is None:
			return -1
		urls = self.raw_data.get("urls", [])
		return int(urls[-1]["size"]) if len(urls) > 0 else -1


def meta_get(meta: Message | dict[str, Any], key: str) -> str | None:
	"""Retrieve metadata value safely.

	:param Message | dict[str, Any] self.meta: Metadata source.
	:param str key: Metadata key.
	:return str: Retrieved metadata value.
	"""
	value = meta.get(key)
	if isinstance(value, Iterable) and not isinstance(value, str):
		return RAW_JOINS.join(str(x) for x in value)
	return str(value) if value else None


def from_classifiers(classifiers: list[str] | None) -> str | None:
	"""Extract license from classifiers.

	:param list[str] | None classifiers: list of classifiers
	:return ucstr: licenses as a ucstr
	"""
	if not classifiers:
		return None

	licenses: list[str] = []
	for _val in classifiers:
		val = str(_val)
		if val.startswith("License"):
			lice = val.split(" :: ")[-1]
			if lice != "OSI Approved":
				licenses.append(lice)
	return RAW_JOINS.join(licenses) if len(licenses) > 0 else None


class ProjectMetadata:
	"""Handles extraction of project metadata from configuration files."""

	@staticmethod
	def get_metadata() -> dict[str, Any]:
		"""Extract project metadata from setup.cfg or pyproject.toml.

		:return dict[str, Any]: Extracted metadata.
		"""
		if Path("setup.cfg").exists():
			config = configparser.ConfigParser()
			config.read("setup.cfg")
			if "metadata" in config:
				classifiers = config.get("metadata", "classifier", fallback="").strip().splitlines()
				license_str = ucstr(config.get("metadata", "license", fallback=""))
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
	def get_license() -> ucstr:
		"""Extract license from project metadata.

		:return ucstr: License string.
		"""
		metadata = ProjectMetadata.get_metadata()
		license_str = from_classifiers(metadata.get("classifiers", []))

		if license_str is not None:
			return ucstr(license_str)

		if isinstance(metadata.get("license"), dict):
			return ucstr(metadata["license"].get("text", UNKNOWN))

		return ucstr(metadata.get("license", UNKNOWN))
