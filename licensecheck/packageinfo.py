"""Get information for installed and online packages.
"""
from __future__ import annotations

from importlib import metadata, resources
from pathlib import Path
from typing import cast

import requests
import tomli

from licensecheck.types import PackageInfo

UNKNOWN = "UNKNOWN"


def getPackagesFromLocal(requirements: list[str]) -> list[PackageInfo]:
	"""Get a list of package info from local files including version, author
	and	the license.

	Args:
		requirements (list[str]): [description]

	Returns:
		list[PackageInfo]: [description]
	"""
	pkgInfo = []
	for requirement in requirements:
		try:
			# Get pkg metadata: license, homepage + author
			pkgMetadata = metadata.metadata(requirement)
			lice = licenseFromClassifierlist(
				[val for key, val in pkgMetadata.items() if key == "Classifier"]
			)
			if lice == UNKNOWN:
				lice = pkgMetadata.get("License", UNKNOWN)
			homePage = pkgMetadata.get("Home-page", UNKNOWN)
			author = pkgMetadata.get("Author", UNKNOWN)
			name = pkgMetadata.get("Name", UNKNOWN)
			version = pkgMetadata.get("Version", UNKNOWN)
			size = 0
			try:
				packagePath = resources.files(requirement)
				size = getModuleSize(cast(Path, packagePath), name)
			except TypeError:
				pass
			# append to pkgInfo
			pkgInfo.append(
				{
					"name": name,
					"version": version,
					"namever": f"{name}-{version}",
					"home_page": homePage,
					"author": author,
					"size": size,
					"license": lice,
				}
			)
		except (metadata.PackageNotFoundError, ModuleNotFoundError):
			pass
	return pkgInfo


def packageInfoFromPypi(requirements: list[str]) -> list[PackageInfo]:
	"""Get a list of package info from pypi.org including version, author
	and	the license.

	Args:
		requirements (list[str]): [description]

	Returns:
		list[PackageInfo]: [description]
	"""
	pkgInfo = []
	for pkg in requirements:
		request = requests.get(f"https://pypi.org/pypi/{pkg}/json")
		response = request.json()
		info = response["info"]
		licenseClassifier = licenseFromClassifierlist(info["classifiers"])
		pkgInfo.append(
			{
				"name": pkg,
				"version": info["version"],
				"namever": f"{pkg} {info['version']}",
				"home_page": info["home_page"],
				"author": info["author"],
				"size": int(response["urls"][-1]["size"]),
				"license": licenseClassifier if licenseClassifier != UNKNOWN else info["license"],
			}
		)
	return pkgInfo


def licenseFromClassifierlist(classifiers: list[str]) -> str:
	"""Get license string from a list of project classifiers.

	Args:
		classifiers (list[str]): list of classifiers

	Returns:
		str: the license name
	"""
	licenses = []
	for val in classifiers:
		if val.startswith("License"):
			lice = val.split(" :: ")[-1]
			if lice != "OSI Approved":
				licenses.append(lice)
	return ", ".join(licenses) if len(licenses) > 0 else UNKNOWN


def getPackages(reqs: list[str]) -> list[PackageInfo]:
	"""Get dependency info.

	Args:
		reqs (list[str]): list of dependency names to gather info on

	Returns:
		list[PackageInfo]: list of dependencies
	"""
	localReqs = getPackagesFromLocal(reqs)
	for localReq in localReqs:
		reqs.remove(localReq["name"].lower())
	onlineReqs = packageInfoFromPypi(reqs)
	return localReqs + onlineReqs


def getMyPackageLicense() -> str:
	"""Get the pyproject data.

	Returns:
		str: license name

	Raises:
		RuntimeError: Must specify a license using license spdx or classifier (tool.poetry or tool.flit)
	"""
	try:
		pyproject = tomli.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
	except FileNotFoundError:
		return input("Enter the project license")
	tool = pyproject["tool"]
	metaData = {"classifiers": [], "license": ""}
	if "poetry" in tool:
		metaData = tool["poetry"]
	elif "flit" in tool:
		metaData = tool["flit"]["metadata"]
	else:
		return input("Enter the project license")
	licenseClassifier = licenseFromClassifierlist(metaData.get("classifiers", []))
	if licenseClassifier != UNKNOWN:
		return licenseClassifier
	if "license" in metaData:
		return str(metaData["license"])
	raise RuntimeError(
		"Must specify a license using license spdx or classifier (tool.poetry or tool.flit)"
	)


def getModuleSize(path: Path, name: str) -> int:
	"""Get the size of a given module as an int.

	Args:
		path (Path): path to package
		name (str): name of package

	Returns:
		int: size in bytes
	"""
	size = sum(
		f.stat().st_size for f in path.glob("**/*") if f.is_file() and "__pycache__" not in str(f)
	)
	if size > 0:
		return size
	request = requests.get(f"https://pypi.org/pypi/{name}/json")
	response = request.json()
	return int(response["urls"][-1]["size"])
