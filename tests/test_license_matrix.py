import logging
import sys
from io import StringIO
from pathlib import Path

from licensecheck import license_matrix, types

THISDIR = str(Path(__file__).resolve().parent)


def test_licenseLookup():
	licenses = []
	for rawLicense in Path(f"{THISDIR}/data/rawLicenses.txt").read_text("utf-8").splitlines():
		licenseName = license_matrix.licenseLookup(types.ucstr(rawLicense))._name_
		licenses.append(licenseName)

	for x in types.License._member_names_:
		if x not in licenses:
			logging.error(f"{x} not in licenses")
			assert False

	# Path(f"{THISDIR}/data/licenseCheckLicenses.txt").write_text("\n".join(licenses), "utf-8")
	assert "\n".join(licenses) == Path(f"{THISDIR}/data/licenseCheckLicenses.txt").read_text(
		"utf-8"
	)


def test_licenseType():
	licenses = Path(f"{THISDIR}/data/rawLicenses.txt").read_text("utf-8").replace("\n", types.JOINS)
	licenseNames = [x._name_ for x in license_matrix.licenseType(licenses)]
	assert (
		licenseNames
		== Path(f"{THISDIR}/data/licenseCheckLicenses.txt").read_text("utf-8").splitlines()
	)


def test_licenseType_empty():
	no_licenses = [
		all(x == types.L.NO_LICENSE for x in license_matrix.licenseType(y))
		for y in ["", None, "this_license_does_not_exist"]
	]
	assert all(no_licenses)


def test_apacheCompatWithLGPL3():
	assert license_matrix.depCompatWMyLice(types.L.LGPL_3, [types.L.APACHE])


def test_dualLicenseCompat():
	assert license_matrix.depCompatWMyLice(types.L.MIT, [types.L.GPL_2, types.L.MIT])


def test_warningsForIgnoredLicense():
	_stdout = sys.stdout
	sys.stdout = StringIO()
	zope = types.ucstr("ZOPE PUBLIC LICENSE")
	license_matrix.licenseLookup(zope, [])
	assert (
		sys.stdout.getvalue()
		== "WARN: 'ZOPE PUBLIC LICENSE' License not identified so falling back to NO_LICENSE\n"
	)


def test_warningsForIgnoredLicenseIgnored():
	_stdout = sys.stdout
	sys.stdout = StringIO()
	zope = types.ucstr("ZOPE PUBLIC LICENSE")
	license_matrix.licenseLookup(zope, [zope])
	assert sys.stdout.getvalue() == ""
