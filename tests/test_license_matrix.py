import sys
from pathlib import Path

from _pytest.logging import LogCaptureFixture  # pyright: ignore {reportMissingImports}
from loguru import logger

from licensecheck import license_matrix
from licensecheck.models.constants import JOINS
from licensecheck.models.license import L, License

THISDIR = str(Path(__file__).resolve().parent)

logger.remove()
logger.add(sys.stderr, colorize=False)


import logging

import pytest

from licensecheck.license_matrix import licenseType


@pytest.mark.parametrize("license_string", ["GNU LIBRARY", "UPL-1.0"])
def test_gnu_library_and_upl_1_is_recognized_without_warnings(
	caplog: pytest.LogCaptureFixture, license_string: str
) -> None:
	with caplog.at_level(logging.WARNING):
		# Correct license where found.
		license_type = licenseType(license_string)
		assert len(license_type) == 1
		assert isinstance(license_type.pop(), L)
		assert L.UNKNOWN not in license_type
		# No warnings were emitted.
		if len(caplog.records):
			assert license_string not in caplog.text


def test_licenseLookup() -> None:
	"""Check that all of the License Enums are present in the processed dataset, we add "NO_LICENSE"
	as all test data contains some license.

	"""
	licenses = []
	for rawLicense in Path(f"{THISDIR}/data/rawLicenses.txt").read_text("utf-8").splitlines():
		licenseName = license_matrix._licenseLookup(rawLicense)._name_
		licenses.append(licenseName)

	licenses.append("NO_LICENSE")
	msgs = []
	for x in License._member_names_:
		if x not in licenses:
			msgs.append(f"{x} not in licenses")

	if msgs:
		logger.error(msgs)
		raise AssertionError(msgs)

	cmp_file = Path(f"{THISDIR}/data/licenseCheckLicenses.txt")

	# cmp_file.write_text("\n".join(licenses), "utf-8")
	assert "\n".join(licenses) == cmp_file.read_text("utf-8")


def test_licenseType() -> None:
	licenses = Path(f"{THISDIR}/data/rawLicenses.txt").read_text("utf-8").replace("\n", JOINS)
	licenseNames = [x._name_ for x in license_matrix._lst_licenseType(licenses)]
	cmp_file = Path(f"{THISDIR}/data/licenseCheckLicenses.txt")

	# cmp_file.write_text("\n".join(licenses), "utf-8")
	assert licenseNames == cmp_file.read_text("utf-8").splitlines()


def test_licenseType_unknown() -> None:
	assert all(x == L.UNKNOWN for x in license_matrix.licenseType("this_license_does_not_exist"))


def test_licenseType_empty() -> None:
	no_licenses = {
		all(x == L.NO_LICENSE for x in license_matrix.licenseType(y)) for y in ("", None)
	}
	assert all(no_licenses)


def test_apacheCompatWithLGPL3() -> None:
	assert license_matrix.depCompatWMyLice(L.LGPL_3, {L.APACHE})


def test_dualLicenseCompat() -> None:
	assert license_matrix.depCompatWMyLice(L.MIT, {L.GPL_2, L.MIT})


def test_whitelistedLicenseCompat() -> None:
	assert license_matrix.depCompatWMyLice(L.MIT, {L.MIT}, onlyLicenses={L.MIT})
	assert license_matrix.depCompatWMyLice(L.MPL, {L.MIT}, onlyLicenses={L.MIT})
	assert not license_matrix.depCompatWMyLice(L.MIT, {L.MIT}, onlyLicenses={L.MPL})
	assert not license_matrix.depCompatWMyLice(L.MPL, {L.MIT}, onlyLicenses={L.MPL})


def test_warningsForIgnoredLicense(caplog: LogCaptureFixture) -> None:
	zope = "ZOPE PUBLIC LICENSE"
	license_matrix._licenseLookup(zope, set())
	assert any(
		record.levelname == "WARNING"
		and f"'{zope}' License not identified so falling back to UNKNOWN" in record.message
		for record in caplog.records
	)


def test_warningsForIgnoredLicenseIgnored(caplog: LogCaptureFixture) -> None:
	zope = "ZOPE PUBLIC LICENSE"
	license_matrix._licenseLookup(zope, {zope})
	assert caplog.text == ""


def test_warningsForIgnoredLicenseIgnored_lc(caplog: LogCaptureFixture) -> None:
	zope = "ZOPE PUBLIC LICENSE"
	license_matrix._licenseLookup(zope, {zope.lower()})
	assert caplog.text == ""
