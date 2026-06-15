from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from licensecheck.models.constants import UNKNOWN
from licensecheck.models.packageinfo import PackageInfo
from licensecheck.packageinfo import (
	LocalPackageInfo,
	PackageInfoManager,
	RemotePackageInfo,
	from_classifiers,
	meta_get,
)

THISDIR = str(Path(__file__).resolve().parent)


@pytest.fixture
def package_info_manager() -> PackageInfoManager:
	"""Fixture to provide a PackageInfoManager instance."""
	return PackageInfoManager("https://pypi.org/")


@pytest.fixture
def local_package_info() -> LocalPackageInfo:
	return LocalPackageInfo(requests_package)


@pytest.fixture
def remote_package_info() -> RemotePackageInfo:
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
	assert pkg.get_author() == "Kenneth Reitz"
	assert pkg.get_license() == "Apache Software License"


def test_getPackageInfoLocalNotFound() -> None:
	pkg = LocalPackageInfo(aux_packageinfo("this_package_does_not_exist"))
	assert pkg.get_size() is None


def test_getPackagePypiLocalNotFound() -> None:
	pkg = RemotePackageInfo("https://pypi.org/", aux_packageinfo("this_package_does_not_exist"))
	assert pkg.get_size() is None


def test_getPackages(package_info_manager: PackageInfoManager) -> None:
	package_info_manager.reqs = {aux_packageinfo("requests")}
	packages = package_info_manager.getPackages()
	package = packages.pop()
	assert package.name == "requests"
	assert package.author == "Kenneth Reitz"
	assert package.license == "Apache Software License"


def test_getPackagesNotFound(package_info_manager: PackageInfoManager) -> None:
	package_info_manager.reqs = {aux_packageinfo("this_package_does_not_exist")}

	packages = package_info_manager.getPackages()
	package = packages.pop()

	assert package.name == "this-package-does-not-exist"
	assert package.errorCode == 1


def test_from_classifiers() -> None:
	lines = Path(f"{THISDIR}/data/pypiClassifiers.txt").read_text("utf-8").splitlines()
	licenses = [from_classifiers([rawLicense]) or UNKNOWN for rawLicense in lines]
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
