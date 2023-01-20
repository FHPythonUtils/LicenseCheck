"""Get information for installed and online packages.
"""
from __future__ import annotations

import configparser
import sys
from importlib import metadata

if sys.version_info < (3, 9, 0):
	import importlib_resources as ilr
else:
	import importlib.resources as ilr
from pathlib import Path
from typing import Any, cast

import requests
import tomli

from licensecheck.types import JOINS, UNKNOWN, PackageInfo


def getPackageInfoLocal(requirement: str) -> PackageInfo:
	"""Get package info from local files including version, author
	and	the license.

	:param str requirement: name of the package
	:raises ModuleNotFoundError: if the package does not exist
	:return PackageInfo: package information
	"""
	try:
		# Get pkg metadata: license, homepage + author
		pkgMetadata = metadata.metadata(requirement)
		lice = licenseFromClassifierlist(pkgMetadata.get_all("Classifier"))
		if lice == UNKNOWN:
			lice = pkgMetadata.get("License", UNKNOWN)
		homePage = pkgMetadata.get("Home-page", UNKNOWN)
		author = pkgMetadata.get("Author", UNKNOWN)
		name = pkgMetadata.get("Name", UNKNOWN)
		version = pkgMetadata.get("Version", UNKNOWN)
		size = 0
		try:
			packagePath = ilr.files(requirement)
			size = getModuleSize(cast(Path, packagePath), name)
		except TypeError:
			pass
		# append to pkgInfo
		return PackageInfo(
			name=name,
			version=version,
			homePage=homePage,
			author=author,
			size=size,
			license=lice,
		)

	except (metadata.PackageNotFoundError, ModuleNotFoundError) as error:
		raise ModuleNotFoundError from error


def getPackageInfoPypi(requirement: str) -> PackageInfo:
	"""Get package info from local files including version, author
	and	the license.

	:param str requirement: name of the package
	:raises ModuleNotFoundError: if the package does not exist
	:return PackageInfo: package information
	"""
	request = requests.get(f"https://pypi.org/pypi/{requirement}/json", timeout=60)
	response = request.json()
	try:
		info = response["info"]
		licenseClassifier = licenseFromClassifierlist(info["classifiers"])
		return PackageInfo(
			name=requirement,
			version=info["version"],
			homePage=info["home_page"],
			author=info["author"],
			size=int(response["urls"][-1]["size"]),
			license=licenseClassifier if licenseClassifier != UNKNOWN else info["license"],
		)
	except KeyError as error:
		raise ModuleNotFoundError from error


def licenseFromClassifierlist(classifiers: list[str]) -> str:
	"""Get license string from a list of project classifiers.

	Args:
		classifiers (list[str]): list of classifiers

	Returns:
		str: the license name
	"""
	if not classifiers:
		return UNKNOWN
	licenses = []
	for val in classifiers:
		if val.startswith("License"):
			lice = val.split(" :: ")[-1]
			if lice != "OSI Approved":
				licenses.append(lice)
	return JOINS.join(licenses) if len(licenses) > 0 else UNKNOWN


def getPackages(reqs: set[str]) -> set[PackageInfo]:
	"""Get dependency info.

	Args:
		reqs (set[str]): set of dependency names to gather info on

	Returns:
		set[PackageInfo]: set of dependencies
	"""
	packageinfo = set()
	for requirement in reqs:
		try:
			packageinfo.add(getPackageInfoLocal(requirement))
		except ModuleNotFoundError:
			try:
				packageinfo.add(getPackageInfoPypi(requirement))
			except ModuleNotFoundError:
				packageinfo.add(PackageInfo(name=requirement, errorCode=1))

	return packageinfo


def getMyPackageMetadata() -> dict[str, Any]:
	"""Get the package classifiers and license from "setup.cfg", "pyproject.toml"

	Returns:
		dict[str, Any]: {"classifiers": list[str], "license": str}
	"""
	if Path("setup.cfg").exists():
		config = configparser.ConfigParser()
		config.read("setup.cfg")
		if "license" in config["metadata"]:
			return config["metadata"].__dict__
	if Path("pyproject.toml").exists():
		pyproject = tomli.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
		tool = pyproject["tool"]
		if "poetry" in tool:
			return tool["poetry"]
		if "flit" in tool:
			return tool["flit"]["metadata"]
		if pyproject.get("project") is not None:
			return pyproject["project"]

	return {"classifiers": [], "license": ""}


def getMyPackageLicense() -> str:
	"""Get the package license from "setup.cfg", "pyproject.toml" or user input

	Returns:
		str: license name
	"""
	metaData = getMyPackageMetadata()
	licenseClassifier = licenseFromClassifierlist(metaData.get("classifiers", []))
	if licenseClassifier != UNKNOWN:
		return licenseClassifier
	if "license" in metaData:
		if isinstance(metaData["license"], dict) and metaData["license"].get("text") is not None:
			return str(metaData["license"].get("text"))
		return str(metaData["license"])
	return input("Enter the project license\n>")


def getModuleSize(path: Path, name: str) -> int:
	"""Get the size of a given module as an int.

	Args:
		path (Path): path to package
		name (str): name of package

	Returns:
		int: size in bytes
	"""
	size = 0
	try:
		size = sum(
			f.stat().st_size
			for f in path.glob("**/*")
			if f.is_file() and "__pycache__" not in str(f)
		)
	except AttributeError:
		pass
	if size > 0:
		return size
	request = requests.get(f"https://pypi.org/pypi/{name}/json", timeout=60)
	response = request.json()
	return int(response["urls"][-1]["size"])
