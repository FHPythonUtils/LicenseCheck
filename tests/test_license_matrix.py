import logging
from pathlib import Path

from licensecheck import license_matrix, types

THISDIR = str(Path(__file__).resolve().parent)


def test_licenseLookup():
	licenses = []
	for rawLicense in Path(f"{THISDIR}/data/rawLicenses.txt").read_text("utf-8").splitlines():
		licenseName = license_matrix.licenseLookup(rawLicense.upper())._name_
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
