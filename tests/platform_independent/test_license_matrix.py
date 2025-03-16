import sys
from pathlib import Path

from _pytest.logging import LogCaptureFixture  # pyright: ignore [reportMissingImports]
from loguru import logger

from licensecheck import license_matrix, types

THISDIR = str(Path(__file__).resolve().parent)

logger.remove()
logger.add(sys.stderr, colorize=False)


def test_licenseLookup() -> None:
	"""Check that all of the License Enums are present in the processed dataset, we add "NO_LICENSE"
	as all test data contains some license.

	"""
	licenses = []
	for rawLicense in Path(f"{THISDIR}/data/rawLicenses.txt").read_text("utf-8").splitlines():
		licenseName = license_matrix.licenseLookup(types.ucstr(rawLicense))._name_
		licenses.append(licenseName)

	licenses.append("NO_LICENSE")
	for x in types.License._member_names_:
		if x not in licenses:
			msg = f"{x} not in licenses"
			logger.error(msg)
			raise AssertionError(msg)

	cmp_file = Path(f"{THISDIR}/data/licenseCheckLicenses.txt")

	# cmp_file.write_text("\n".join(licenses), "utf-8")
	assert "\n".join(licenses) == cmp_file.read_text("utf-8")


def test_licenseType() -> None:
	licenses = Path(f"{THISDIR}/data/rawLicenses.txt").read_text("utf-8").replace("\n", types.JOINS)
	licenseNames = [x._name_ for x in license_matrix.licenseType(types.ucstr(licenses))]
	cmp_file = Path(f"{THISDIR}/data/licenseCheckLicenses.txt")

	# cmp_file.write_text("\n".join(licenses), "utf-8")
	assert licenseNames == cmp_file.read_text("utf-8").splitlines()


def test_licenseType_unknown() -> None:
	assert all(
		x == types.L.UNKNOWN for x in license_matrix.licenseType("this_license_does_not_exist")
	)


def test_licenseType_empty() -> None:
	no_licenses = [
		all(x == types.L.NO_LICENSE for x in license_matrix.licenseType(y)) for y in ["", None]
	]
	assert all(no_licenses)


def test_apacheCompatWithLGPL3() -> None:
	assert license_matrix.depCompatWMyLice(types.L.LGPL_3, [types.L.APACHE])


def test_dualLicenseCompat() -> None:
	assert license_matrix.depCompatWMyLice(types.L.MIT, [types.L.GPL_2, types.L.MIT])


def test_whitelistedLicenseCompat() -> None:
	assert license_matrix.depCompatWMyLice(types.L.MIT, [types.L.MIT], onlyLicenses=[types.L.MIT])
	assert license_matrix.depCompatWMyLice(types.L.MPL, [types.L.MIT], onlyLicenses=[types.L.MIT])
	assert not license_matrix.depCompatWMyLice(
		types.L.MIT, [types.L.MIT], onlyLicenses=[types.L.MPL]
	)
	assert not license_matrix.depCompatWMyLice(
		types.L.MPL, [types.L.MIT], onlyLicenses=[types.L.MPL]
	)


def test_warningsForIgnoredLicense(caplog: LogCaptureFixture) -> None:
	zope = types.ucstr("ZOPE PUBLIC LICENSE")
	license_matrix.licenseLookup(zope, [])
	assert any(
		record.levelname == "WARNING"
		and f"'{zope}' License not identified so falling back to UNKNOWN" in record.message
		for record in caplog.records
	)


def test_warningsForIgnoredLicenseIgnored(caplog: LogCaptureFixture) -> None:
	zope = types.ucstr("ZOPE PUBLIC LICENSE")
	license_matrix.licenseLookup(zope, [zope])
	assert caplog.text == ""
