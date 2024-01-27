from pathlib import Path

from licensecheck import packageinfo, types

THISDIR = str(Path(__file__).resolve().parent)


def test_getPackageInfoLocal() -> None:
	try:
		package = packageinfo.getPackageInfoLocal(types.ucstr("requests"))
		assert package.name == "requests"
	except ModuleNotFoundError:
		assert True


def test_getPackageInfoPypi() -> None:
	package = packageinfo.getPackageInfoPypi(types.ucstr("requests"))

	assert package.name == "requests"
	assert package.homePage == "https://requests.readthedocs.io"
	assert package.author == "Kenneth Reitz"
	assert package.license == "APACHE SOFTWARE LICENSE"


def test_getPackageInfoLocalNotFound() -> None:
	try:
		packageinfo.getPackageInfoLocal(types.ucstr("this_package_does_not_exist"))
		raise AssertionError
	except ModuleNotFoundError:
		assert True


def test_getPackagePypiLocalNotFound() -> None:
	try:
		packageinfo.getPackageInfoPypi(types.ucstr("this_package_does_not_exist"))
		raise AssertionError
	except ModuleNotFoundError:
		assert True


def test_getPackages() -> None:
	packages = packageinfo.getPackages({types.ucstr("requests")})

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
	packages = packageinfo.getPackages({types.ucstr("this_package_does_not_exist")})

	assert all(
		(package.name == "THIS_PACKAGE_DOES_NOT_EXIST" and package.errorCode == 1)
		for package in packages
	)


def test_licenseFromClassifierlist() -> None:
	licenses = []
	for rawLicense in Path(f"{THISDIR}/data/pypiClassifiers.txt").read_text("utf-8").splitlines():
		licenses.append(packageinfo.licenseFromClassifierlist([rawLicense]))
	# Path(f"{THISDIR}/data/licenses.txt").write_text("\n".join(licenses), "utf-8")
	assert "\n".join(licenses) == Path(f"{THISDIR}/data/licenses.txt").read_text("utf-8")


def test_licenseFromEmptyClassifierlist() -> None:
	licenses = []
	licenses.append(packageinfo.licenseFromClassifierlist([]))
	assert licenses == [types.UNKNOWN]


def test_getModuleSize() -> None:
	size = packageinfo.getModuleSize(
		Path("this_package_does_not_exist"), types.ucstr("this_package_does_not_exist")
	)
	assert size == 0
