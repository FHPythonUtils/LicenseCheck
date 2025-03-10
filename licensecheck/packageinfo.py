"""Get information for installed and online packages."""

from __future__ import annotations

import configparser
import contextlib
from collections.abc import Iterable
from importlib import metadata
from pathlib import Path
from typing import Any

import tomli

from licensecheck.session import session
from licensecheck.types import JOINS, UNKNOWN, PackageInfo, ucstr


class PackageInfoManager:
	def __init__(self, pypi_api: str) -> None:
		self.pypi_api = pypi_api

	def getPackages(self, reqs: set[ucstr]) -> set[PackageInfo]:
		"""Get dependency info.

		Args:
		----
			reqs (set[ucstr]): set of dependency names to gather info on

		Returns:
		-------
			set[PackageInfo]: set of dependencies

		"""
		packageinfo = set()
		for requirement in reqs:
			try:
				packageinfo.add(self.getPackageInfoLocal(requirement))
			except ModuleNotFoundError:
				try:
					packageinfo.add(self.getPackageInfoPypi(requirement))
				except ModuleNotFoundError:
					packageinfo.add(PackageInfo(name=requirement, errorCode=1))

		return packageinfo

	def getPackageInfoLocal(self, requirement: ucstr) -> PackageInfo:
		"""Get package info from local files including version, author
		and	the license.

		:param str requirement: name of the package
		:raises ModuleNotFoundError: if the package does not exist
		:return PackageInfo: package information
		"""
		try:
			# Get pkg metadata,, license, homepage, and author
			pkgMetadata = metadata.metadata(requirement)
			lice = licenseFromClassifierlist(pkgMetadata.get_all("Classifier"))
			if lice == UNKNOWN:
				lice = _pkgMetadataGet(pkgMetadata, "License")
			homePage = _pkgMetadataGet(pkgMetadata, "Home-page")
			author = _pkgMetadataGet(pkgMetadata, "Author")
			name = _pkgMetadataGet(pkgMetadata, "Name")
			version = _pkgMetadataGet(pkgMetadata, "Version")
			size = 0
			packagePaths = metadata.Distribution.from_name(requirement).files
			if packagePaths is not None:
				size = sum(pp.size for pp in packagePaths if pp.size is not None)

			# append to pkgInfo
			return PackageInfo(
				name=name,
				version=version,
				homePage=homePage,
				author=author,
				size=size,
				license=ucstr(lice),
			)

		except metadata.PackageNotFoundError as error:
			raise ModuleNotFoundError from error

	def getPackageInfoPypi(self, requirement: ucstr) -> PackageInfo:
		"""Get package info from local files including version, author
		and	the license.

		:param str requirement: name of the package
		:raises ModuleNotFoundError: if the package does not exist
		:return PackageInfo: package information
		"""
		request = session.get(f"{self.pypi_api}{requirement}/json", timeout=60)
		response = request.json()
		try:
			info = response.get("info", {})
			licenseClassifier = licenseFromClassifierlist(info["classifiers"])

			size = -1
			urls = response.get("urls", [])
			if urls:
				size = int(urls[-1]["size"])

			return PackageInfo(
				name=_pkgMetadataGet(info, "name"),
				version=_pkgMetadataGet(info, "version"),
				homePage=_pkgMetadataGet(info, "home_page"),
				author=_pkgMetadataGet(info, "author"),
				size=size,
				license=ucstr(
					licenseClassifier
					if licenseClassifier != UNKNOWN
					else info.get("license", UNKNOWN) or UNKNOWN
				),
			)
		except KeyError as error:
			raise ModuleNotFoundError from error


def _pkgMetadataGet(pkgMetadata: metadata.PackageMetadata | dict[str, Any], key: str) -> str:
	"""Get a string from a key from pkgMetadata."""
	value = pkgMetadata.get(key, UNKNOWN)
	if not isinstance(value, str) and isinstance(value, Iterable):
		value = JOINS.join(str(x) for x in value)
	return str(value) or UNKNOWN


def licenseFromClassifierlist(classifiers: list[str] | None | list[Any]) -> ucstr:
	"""Get license string from a list of project classifiers.

	Args:
	----
		classifiers (list[str]): list of classifiers

	Returns:
	-------
		str: the license name

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
	return ucstr(JOINS.join(licenses) if len(licenses) > 0 else UNKNOWN)


def getMyPackageMetadata() -> dict[str, Any]:
	"""Get the package classifiers and license from "setup.cfg", "pyproject.toml".

	Returns
	-------
		dict[str, Any]: {"classifiers": list[str], "license": ucstr}

	"""
	if Path("setup.cfg").exists():
		config = configparser.ConfigParser()
		config.read("setup.cfg")
		if "metadata" in config.sections() and "license" in config["metadata"]:
			if "classifier" in config["metadata"]:
				classifiers = config.get("metadata", "classifier").strip().splitlines()
			else:
				classifiers = config.get("metadata", "classifiers").strip().splitlines()
			licenseStr = ucstr(config.get("metadata", "license"))
			return {"classifiers": classifiers, "license": licenseStr}

	if Path("pyproject.toml").exists():
		pyproject = tomli.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
		tool = pyproject.get("tool", {})
		if "poetry" in tool:
			return tool["poetry"]
		if "flit" in tool:
			return tool["flit"]["metadata"]
		if pyproject.get("project") is not None:
			return pyproject["project"]

	return {"classifiers": [], "license": ucstr("")}


def getMyPackageLicense() -> ucstr:
	"""Get the package license from "setup.cfg", "pyproject.toml" or user input.

	Returns
	-------
		str: license name

	"""
	metaData = getMyPackageMetadata()
	licenseClassifier = licenseFromClassifierlist(metaData.get("classifiers", []))
	if licenseClassifier != UNKNOWN:
		return licenseClassifier
	if "license" in metaData:
		if isinstance(metaData["license"], dict) and metaData["license"].get("text") is not None:
			return ucstr(metaData["license"].get("text", UNKNOWN))
		return ucstr(f"{metaData['license']}")
	return ucstr(input("Enter the project license\n>"))


def getModuleSize(path: Path, name: ucstr) -> int:
	"""Get the size of a given module as an int.

	Args:
	----
		path (Path): path to package
		name (str): name of package

	Returns:
	-------
		int: size in bytes

	"""
	HTTP_OK = 200
	size = 0
	with contextlib.suppress(AttributeError):
		size = sum(
			f.stat().st_size
			for f in path.glob("**/*")
			if f.is_file() and "__pycache__" not in str(f)
		)
	if size > 0:
		return size
	request = session.get(f"https://pypi.org/pypi/{name}/json", timeout=60)
	if request.status_code != HTTP_OK:
		return 0
	response = request.json()
	return int(response["urls"][-1]["size"])
