from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from licensecheck.packageinfo import (
	LocalPackageInfo,
	PackageInfoManager,
	RemotePackageInfo,
	from_classifiers,
	meta_get,
)
from licensecheck.types import UNKNOWN, PackageInfo

THISDIR = str(Path(__file__).resolve().parent)


@pytest.fixture
def package_info_manager():
	"""Fixture to provide a PackageInfoManager instance."""
	return PackageInfoManager("https://pypi.org/pypi/")


@pytest.fixture
def local_package_info():
	return LocalPackageInfo(requests_package)


@pytest.fixture
def remote_package_info():
	return RemotePackageInfo("https://pypi.org/pypi/", requests_package)


def aux_packageinfo(package_name: str) -> PackageInfo:
	return PackageInfo(name=package_name)


requests_package = aux_packageinfo("requests")


def test_getPackageInfoLocal(local_package_info: LocalPackageInfo) -> None:
	try:
		name = local_package_info.get_name()
		assert name == "requests"
	except ModuleNotFoundError:
		assert True


def test_getPackageInfoPypi(remote_package_info: RemotePackageInfo) -> None:
	pkg = remote_package_info

	assert pkg.get_name() == "requests"
	assert pkg.get_homePage() == "https://requests.readthedocs.io"
	assert pkg.get_author() == "Kenneth Reitz"
	assert pkg.get_license() == "Apache Software License"


def test_getPackageInfoLocalNotFound() -> None:
	pkg = LocalPackageInfo(aux_packageinfo("this_package_does_not_exist"))
	assert pkg.get_size() == 0


def test_getPackagePypiLocalNotFound() -> None:
	pkg = RemotePackageInfo(
		"https://pypi.org/pypi/", aux_packageinfo("this_package_does_not_exist")
	)
	assert pkg.get_size() == -1


def test_getPackages(package_info_manager: PackageInfoManager) -> None:
	package_info_manager.reqs = {aux_packageinfo("requests")}
	packages = package_info_manager.getPackages()
	assert all(
		(
			package.name == "requests"
			and package.homePage == "https://requests.readthedocs.io"
			and package.author == "Kenneth Reitz"
			and package.license == "APACHE SOFTWARE LICENSE"
		)
		for package in packages
	)


def test_getPackagesNotFound(package_info_manager: PackageInfoManager) -> None:
	package_info_manager.reqs = {aux_packageinfo("this_package_does_not_exist")}

	packages = package_info_manager.getPackages()

	assert all(
		(package.name.upper() == "THIS_PACKAGE_DOES_NOT_EXIST" and package.errorCode == 1)
		for package in packages
	)


def test_from_classifiers() -> None:
	licenses = []
	for rawLicense in Path(f"{THISDIR}/data/pypiClassifiers.txt").read_text("utf-8").splitlines():
		licenses.append(from_classifiers([rawLicense]) or UNKNOWN)
	# Path(f"{THISDIR}/data/licenses.txt").write_text("\n".join(licenses), "utf-8")
	assert "\n".join(licenses) == Path(f"{THISDIR}/data/licenses.txt").read_text("utf-8")


def test_licenseFromEmptyClassifierlist() -> None:
	licenses = []
	licenses.append(from_classifiers([]))
	assert licenses == [None]


def test_getModuleSize() -> None:
	local_package_info = LocalPackageInfo(aux_packageinfo("this_package_does_not_exist"))
	local_package_info.get_size()


# Define test cases
@pytest.mark.parametrize(
	("pkg_metadata", "key", "expected"),
	[
		({"name": "Package Name", "version": "1.0"}, "name", "Package Name"),
		({"name": ["Package Name"], "version": "1.0"}, "name", "Package Name"),
		({"name": [1], "version": "1.0"}, "name", "1"),
		({"name": 1, "version": "1.0"}, "name", "1"),
		({"name": None, "version": "1.0"}, "name", None),
		({"name": ["Package", "Name"], "version": "1.0"}, "name", "Package AND Name"),
		({}, "name", None),
		({"name": "Package Name", "version": "1.0"}, "description", None),
	],
)
def test_get_metadata(pkg_metadata: dict[str, Any], key: str, expected: str) -> None:
	assert meta_get(pkg_metadata, key) == expected
