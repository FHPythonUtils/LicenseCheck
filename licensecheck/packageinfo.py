"""Get information for installed and online packages."""

from __future__ import annotations

import configparser
import contextlib
import re
from collections.abc import Iterable
from importlib import metadata
from pathlib import Path
from typing import Any

import license_expression
import tomli
from license_expression import Licensing

from licensecheck.session import session
from licensecheck.types import JOINS, UNKNOWN, PackageInfo, ucstr

RAW_JOINS = " AND "


class PackageInfoManager:
	"""Manages retrieval of local and remote package information."""

	def __init__(self, pypi_api: str = "https://pypi.org/pypi/") -> None:
		"""Manage retrieval of local and remote package information.

		:param str pypi_api: url of pypi server. Typically the public instance, defaults
		to "https://pypi.org/pypi/"
		"""
		self.pypi_api = pypi_api

	def getPackages(self, reqs: set[ucstr]) -> set[PackageInfo]:
		"""Retrieve package information from local installation or PyPI.

		:param set[ucstr] reqs: Set of dependency names to retrieve information for.
		:return set[PackageInfo]: A set of package information objects.
		"""
		package_info_set = set()

		for package in reqs:
			package_info = self.get_package_info(package)
			package_info_set.add(package_info)

		return package_info_set

	def get_package_info(self, package: ucstr) -> PackageInfo:
		"""Retrieve package information, preferring local data.

		:param ucstr pacage: Package name.
		:return PackageInfo: Information about the package.
		"""
		pkg_info = PackageInfo(name=package, errorCode=1)
		try:
			pkg_info = LocalPackageInfo.get_info(package)
		except ModuleNotFoundError:
			with contextlib.suppress(ModuleNotFoundError):
				pkg_info = RemotePackageInfo.get_info(package, self.pypi_api)

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

	@staticmethod
	def get_info(package: ucstr) -> PackageInfo:
		"""Retrieve package metadata from local installation.

		:param ucstr package: Package name.
		:return PackageInfo: Local package information.
		"""
		try:
			metadata_obj = metadata.metadata(package)
			license_str = meta_get(metadata_obj, "License_Expression")
			if license_str == UNKNOWN:
				license_str = from_classifiers(metadata_obj.get_all("Classifier"))
			if license_str == UNKNOWN:
				license_str = meta_get(metadata_obj, "License")

			return PackageInfo(
				name=meta_get(metadata_obj, "Name"),
				version=meta_get(metadata_obj, "Version"),
				homePage=meta_get(metadata_obj, "Home-page"),
				author=meta_get(metadata_obj, "Author"),
				size=LocalPackageInfo.get_size(package),
				license=ucstr(license_str),
			)
		except metadata.PackageNotFoundError as error:
			raise ModuleNotFoundError from error

	@staticmethod
	def get_size(package: ucstr) -> int:
		"""Retrieve installed package size.

		:param ucstr package: Package name.
		:return int: Size in bytes.
		"""
		package_files = metadata.Distribution.from_name(package).files
		return sum(f.size for f in package_files if f.size is not None) if package_files else 0


class RemotePackageInfo:
	"""Handles retrieval of package info from PyPI."""

	@staticmethod
	def get_info(package: ucstr, pypi_api: str) -> PackageInfo:
		"""Retrieve package metadata from PyPI.

		:param ucstr package: Package name.
		:param str pypi_api: PyPI API base URL.
		:return PackageInfo: Remote package information.
		"""
		response = session.get(f"{pypi_api}{package}/json", timeout=60)

		if response.status_code != 200:
			raise ModuleNotFoundError

		data = response.json().get("info", {})

		license_str = meta_get(data, "license_expression")
		if license_str == UNKNOWN:
			license_str = from_classifiers(data.get("classifiers", []))
		if license_str == UNKNOWN:
			license_str = meta_get(data, "license")

		return PackageInfo(
			name=meta_get(data, "name"),
			version=meta_get(data, "version"),
			homePage=meta_get(data, "home_page"),
			author=meta_get(data, "author"),
			size=RemotePackageInfo.get_size(data),
			license=ucstr(license_str),
		)

	@staticmethod
	def get_size(data: dict[str, Any]) -> int:
		"""Retrieve package size from PyPI metadata.

		:param dict[str, Any] data: PyPI response JSON.

		:return int: Package size in bytes.
		"""
		urls = data.get("urls", [])
		return int(urls[-1]["size"]) if urls else -1


def meta_get(metadata_obj: metadata.PackageMetadata | dict[str, Any], key: str) -> str:
	"""Retrieve metadata value safely.

	:param metadata.PackageMetadata | dict[str, Any] metadata_obj: Metadata source.
	:param str key: Metadata key.
	:return str: Retrieved metadata value.
	"""
	value = metadata_obj.get(key, UNKNOWN)
	if isinstance(value, Iterable) and not isinstance(value, str):
		return RAW_JOINS.join(str(x) for x in value)
	return str(value) if value else UNKNOWN


def from_classifiers(classifiers: list[str] | None) -> ucstr:
	"""Extract license from classifiers.

	:param list[str] | None classifiers: list of classifiers
	:return ucstr: licenses as a ucstr
	"""
	if not classifiers:
		return UNKNOWN

	licenses: list[str] = []
	for _val in classifiers:
		val = str(_val)
		if val.startswith("License"):
			lice = val.split(" :: ")[-1]
			if lice != "OSI Approved":
				licenses.append(lice)
	return ucstr(RAW_JOINS.join(licenses) if len(licenses) > 0 else UNKNOWN)


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

		if license_str != UNKNOWN:
			return license_str

		if isinstance(metadata.get("license"), dict):
			return ucstr(metadata["license"].get("text", UNKNOWN))

		return ucstr(metadata.get("license", UNKNOWN))
