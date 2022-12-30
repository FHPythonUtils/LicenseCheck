from pathlib import Path

from licensecheck import packageinfo

THISDIR = str(Path(__file__).resolve().parent)


def test_getPackageInfoPypi():
	package = packageinfo.getPackageInfoPypi("requests")

	assert (
		package.name == "requests"
		and package.homePage == "https://requests.readthedocs.io"
		and package.author == "Kenneth Reitz"
		and package.license == "Apache Software License"
	)


def test_licenseFromClassifierlist():
	licenses = []
	for rawLicense in Path(f"{THISDIR}/data/pypiClassifiers.txt").read_text("utf-8").splitlines():
		licenses.append(packageinfo.licenseFromClassifierlist([rawLicense]))
	# Path(f"{THISDIR}/data/licenses.txt").write_text("\n".join(licenses), "utf-8")
	assert "\n".join(licenses) == Path(f"{THISDIR}/data/licenses.txt").read_text("utf-8")
