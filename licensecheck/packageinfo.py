"""Get information for installed and online packages.
"""

from __future__ import annotations

import os
import os.path
import typing
from email import message_from_string
from email.message import Message
from email.parser import FeedParser

import requests
import tomlkit
from pip._internal.utils.misc import get_installed_distributions
from pip._vendor.pkg_resources import Distribution
from tomlkit import items

LICENSE_UNKNOWN = 'UNKNOWN'


class PackageInfo(typing.TypedDict):
	"""PackageInfo type.
	"""
	name: str
	version: str
	namever: str
	size: int
	home_page: str
	author: str
	license: str


def getPackagesFromLocal(requirements: list[str]) -> list[PackageInfo]:
	"""Get a list of package info from local files including version, author...

	and	the license.

	Args:
		requirements (list[str]): [description]

	Returns:
		list[PackageInfo]: [description]
	"""
	# Filter our packages
	pkgsToKeep = []
	pkgs = get_installed_distributions()
	for pkg in pkgs:
		if pkg.project_name in requirements:
			pkgsToKeep.append(pkg)

	pkgInfo = []
	for pkg in pkgsToKeep:
		licenseClassifier = homePage = author = lice = LICENSE_UNKNOWN
		# Try and get metadata
		metadata = None
		if pkg.has_metadata('METADATA'):
			metadata = pkg.get_metadata('METADATA')
		if pkg.has_metadata('PKG-INFO') and metadata is None:
			metadata = pkg.get_metadata('PKG-INFO')
		if metadata is not None:
			message = message_from_string(metadata)
			licenseClassifier = licenseFromClassifierMessage(message)
			feedParser = FeedParser()
			feedParser.feed(metadata)
			parsedMetadata = feedParser.close()
			homePage = parsedMetadata.get("home-page", LICENSE_UNKNOWN)
			author = parsedMetadata.get("author", LICENSE_UNKNOWN)
			lice = parsedMetadata.get("license", LICENSE_UNKNOWN)

		pkgLicense = licenseClassifier if licenseClassifier != LICENSE_UNKNOWN else lice
		pkgInfo.append({
		"name": pkg.project_name,
		"version": pkg.version,
		"namever": str(pkg),
		"home_page": homePage,
		"author": author,
		"size": getModuleSize(pkg),
		"license": pkgLicense}) # yapf: disable
	return pkgInfo


def licenseFromClassifierMessage(message: Message) -> str:
	"""Get license string from a Message of project classifiers.

	Args:
		classifiers (Message): Message of classifiers

	Returns:
		str: the license name
	"""
	fromClassifier = LICENSE_UNKNOWN
	licenses = []
	for key, val in message.items():
		if key == 'Classifier' and val.startswith('License'):
			lice = val.split(' :: ')[-1]
			# Through the declaration of 'Classifier: License :: OSI Approved'
			if lice != 'OSI Approved':
				licenses.append(lice)
	if len(licenses) > 0:
		fromClassifier = ', '.join(licenses)
	return fromClassifier


def getPackagesFromOnline(requirements: list[str]) -> list[PackageInfo]:
	"""Get a list of package info from pypi.org including version, author...

	and	the license.

	Args:
		requirements (list[str]): [description]

	Returns:
		list[PackageInfo]: [description]
	"""
	pkgInfo = []
	for pkg in requirements:
		url = "https://pypi.org/pypi/" + pkg + "/json"
		request = requests.get(url) # type: ignore
		response = request.json() # type: ignore
		info = response["info"]
		licenseClassifier = licenseFromClassifierlist(response["info"]
		["classifiers"])
		pkgLicense = licenseClassifier if licenseClassifier != LICENSE_UNKNOWN else info[
		"license"]
		pkgInfo.append({"name": pkg,
		"version": info["version"],
		"namever": f"{pkg} {info['version']}",
		"home_page": info["home_page"],
		"author": info["author"],
		"size": int(response["urls"][-1]["size"]),
		"license": pkgLicense}) # yapf: disable
	return pkgInfo


def licenseFromClassifierlist(classifiers: list[str]) -> str:
	"""Get license string from a list of project classifiers.

	Args:
		classifiers (list[str]): list of classifiers

	Returns:
		str: the license name
	"""
	fromClassifier = LICENSE_UNKNOWN
	licenses = []
	for val in classifiers:
		if val.startswith('License'):
			lice = val.split(' :: ')[-1]
			# Through the declaration of 'Classifier: License :: OSI Approved'
			if lice != 'OSI Approved':
				licenses.append(lice)
	if len(licenses) > 0:
		fromClassifier = ', '.join(licenses)
	return fromClassifier


def getPackages(reqs: list[str]) -> list[PackageInfo]:
	"""Get dependency info.

	Args:
		reqs (list[str]): list of dependency names to gather info on

	Returns:
		list[PackageInfo]: list of dependencies
	"""
	localReqs = getPackagesFromLocal(reqs)
	for localReq in localReqs:
		reqs.remove(localReq["name"])
	onlineReqs = getPackagesFromOnline(reqs)
	return localReqs + onlineReqs


def getMyPackageLicense() -> str:
	"""Get the pyproject data.

	Returns:
		str: license name
	"""
	pyproject = None
	try:
		with open("pyproject.toml") as pyproject:
			pyproject = tomlkit.parse(pyproject.read())
	except FileNotFoundError:
		return input("Enter the project license")
	tool = typing.cast(items.Table, pyproject["tool"])
	metaData = {"classifiers": [], "license": ""}
	if "poetry" in tool:
		metaData = typing.cast(items.Table, tool["poetry"])
	elif "flit" in tool:
		metaData = typing.cast(items.Table,
		typing.cast(items.Table, tool["flit"])["metadata"])
	else:
		return input("Enter the project license")
	licenseClassifier = licenseFromClassifierlist(metaData["classifiers"]) # type: ignore yapf: disable
	if licenseClassifier != LICENSE_UNKNOWN:
		return licenseClassifier
	return str(metaData["license"])


def calcContainer(path: str) -> int:
	"""Get size of installed module from path.

	Args:
		path (str): path to the module

	Returns:
		int: size in bytes
	"""
	totalSize = 0
	for dirpath, _dirnames, filenames in os.walk(path, followlinks=True):
		for file in filenames:
			filePointer = os.path.join(dirpath, file)
			totalSize += os.path.getsize(filePointer)
	return totalSize


def getModuleSize(pkg: Distribution) -> int:
	"""Get the size of a given module as an int.

	Args:
		pkg (Distribution): package to get the size of

	Returns:
		int: size in bytes
	"""
	pkgDirname = "{}-{}.dist-info".format(pkg.project_name.replace("-", "_"),
	pkg.version)
	path = os.path.join(pkg.location, pkgDirname) # type: ignore
	size = calcContainer(path)
	if size > 0:
		return size
	url = "https://pypi.org/pypi/" + pkg.project_name + "/json"
	request = requests.get(url) # type: ignore
	response = request.json() # type: ignore
	return int(response["urls"][-1]["size"])
