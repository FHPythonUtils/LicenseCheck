from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import pytest

from licensecheck import packageinfo, types
from licensecheck.packageinfo import PackageInfoManager

THISDIR = str(Path(__file__).resolve().parent)


package_info_manager = PackageInfoManager("https://pypi.org/pypi/")


def test_getPackageInfoLocal() -> None:
	try:
		package = packageinfo.LocalPackageInfo.get_info(types.ucstr("requests"))
		assert package.name == "requests"
	except ModuleNotFoundError:
		assert True


def test_getPackageInfoPypi() -> None:
	package = packageinfo.RemotePackageInfo.get_info(
		types.ucstr("requests"), "https://pypi.org/pypi/"
	)

	assert package.name == "requests"
	assert package.homePage == "https://requests.readthedocs.io"
	assert package.author == "Kenneth Reitz"
	assert package.license == "APACHE SOFTWARE LICENSE"


def test_getPackageInfoLocalNotFound() -> None:
	try:
		packageinfo.LocalPackageInfo.get_info(types.ucstr("this_package_does_not_exist"))
		raise AssertionError
	except ModuleNotFoundError:
		assert True


def test_getPackagePypiLocalNotFound() -> None:
	try:
		packageinfo.RemotePackageInfo.get_info(
			types.ucstr("this_package_does_not_exist"), "https://pypi.org/pypi/"
		)
		raise AssertionError
	except ModuleNotFoundError:
		assert True


def test_getPackages() -> None:
	packages = package_info_manager.getPackages({types.ucstr("requests")})
	assert all(
		(
			package.name == "requests"
			and package.homePage == "https://requests.readthedocs.io"
			and package.author == "Kenneth Reitz"
			and package.license == "APACHE SOFTWARE LICENSE"
		)
		for package in packages
	)


def test_getPackagesNotFound() -> None:
	packages = package_info_manager.getPackages({types.ucstr("this_package_does_not_exist")})

	assert all(
		(package.name == "THIS_PACKAGE_DOES_NOT_EXIST" and package.errorCode == 1)
		for package in packages
	)


def test_from_classifiers() -> None:
	licenses = []
	for rawLicense in Path(f"{THISDIR}/data/pypiClassifiers.txt").read_text("utf-8").splitlines():
		licenses.append(packageinfo.from_classifiers([rawLicense]))
	# Path(f"{THISDIR}/data/licenses.txt").write_text("\n".join(licenses), "utf-8")
	assert "\n".join(licenses) == Path(f"{THISDIR}/data/licenses.txt").read_text("utf-8")


def test_licenseFromEmptyClassifierlist() -> None:
	licenses = []
	licenses.append(packageinfo.from_classifiers([]))
	assert licenses == [types.UNKNOWN]


def test_getModuleSize() -> None:
	with pytest.raises(importlib.metadata.PackageNotFoundError):
		packageinfo.LocalPackageInfo.get_size(types.ucstr("this_package_does_not_exist"))


# Define test cases
@pytest.mark.parametrize(
	("pkg_metadata", "key", "expected"),
	[
		({"name": "Package Name", "version": "1.0"}, "name", "Package Name"),
		({"name": ["Package Name"], "version": "1.0"}, "name", "Package Name"),
		({"name": [1], "version": "1.0"}, "name", "1"),
		({"name": 1, "version": "1.0"}, "name", "1"),
		({"name": None, "version": "1.0"}, "name", types.UNKNOWN),
		({"name": ["Package", "Name"], "version": "1.0"}, "name", "Package AND Name"),
		({}, "name", types.UNKNOWN),
		({"name": "Package Name", "version": "1.0"}, "description", types.UNKNOWN),
	],
)
def test_get_metadata(pkg_metadata: dict[str, Any], key: str, expected: str) -> None:
	assert packageinfo.meta_get(pkg_metadata, key) == expected
