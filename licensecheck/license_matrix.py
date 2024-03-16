"""Define a foss compatability license_matrix.

Standard disclaimer:: I am not a lawyer and there is no guarantee that the
information provided here is complete or correct. Do not take this as legal
advice on foss license compatability

https://en.wikipedia.org/wiki/IANAL


Types of license/ compatability

Public Domain
- Unlicense

Permissive Compatible
Permissive license compatible with gpl
- Mit
- Boost
- Bsd
- Isc
- Ncsa

Permissive Not Compatible
Permissive license NOT compatible with gpl
- Apache
- Eclipse
- Academic Free


Copyleft
permissive -> lgpl 2.1 -> gpl 2
permissive -> lgpl 3 -> gpl 3 -> agpl
permissive -> mpl -> gpl -> agpl (3 only)

permissive (any) -> EU
EU -> gpl -> agpl (3 only)
"""

from __future__ import annotations

import csv
from pathlib import Path

from loguru import logger

from licensecheck.types import JOINS, ucstr
from licensecheck.types import License as L

THISDIR = Path(__file__).resolve().parent

with Path(THISDIR / "matrix.csv").open(mode="r", newline="", encoding="utf-8") as csv_file:
	LICENSE_MATRIX = list(csv.reader(csv_file))


def licenseLookup(licenseStr: ucstr, ignoreLicenses: list[ucstr] | None = None) -> L:
	"""Identify a license from an uppercase string representation of a license.

	Args:
	----
		licenseStr (ucstr): uppercase string representation of a license
		ignoreLicenses (list[ucstr] | None) licenses to ignore. Default=None

	Returns:
	-------
		L: License represented by licenseStr

	"""
	termToLicense = {
		"PUBLIC DOMAIN": L.PUBLIC,
		"CC-PDDC": L.PUBLIC,
		"CC0-1.0": L.PUBLIC,
		"UNLICENSE": L.UNLICENSE,
		"WTFPL": L.UNLICENSE,
		"BOOST": L.BOOST,
		"BSL-1.0": L.BOOST,
		"MIT": L.MIT,
		"BSD": L.BSD,
		"ISC": L.ISC,
		"NCSA": L.NCSA,
		"PYTHON": L.PSFL,
		"PSF-2.0": L.PSFL,
		"APACHE": L.APACHE,
		"ECLIPSE": L.ECLIPSE,
		"AFL": L.ACADEMIC_FREE,
		"LGPLV2+": L.LGPL_2_PLUS,
		"LGPL-2.0-OR-LATER": L.LGPL_2_PLUS,
		"LGPLV3+": L.LGPL_3_PLUS,
		"LGPL-3.0-OR-LATER": L.LGPL_3_PLUS,
		"LGPL-2.0-ONLY": L.LGPL_2,
		"LGPLV2": L.LGPL_2,
		"LGPL-3.0-ONLY": L.LGPL_3,
		"LGPLV3": L.LGPL_3,
		"LGPL": L.LGPL_X,
		"AGPL": L.AGPL_3_PLUS,
		"GNU AFFERO GENERAL PUBLIC LICENSE V3": L.AGPL_3_PLUS,
		"GPL-2.0-OR-LATER": L.GPL_2_PLUS,
		"GPLV2+": L.GPL_2_PLUS,
		"GPL-3.0-OR-LATER": L.GPL_3_PLUS,
		"GPLV3+": L.GPL_3_PLUS,
		"GPLV2": L.GPL_2,
		"GPL-2.0": L.GPL_2,
		"GPLV3": L.GPL_3,
		"GPL-3.0": L.GPL_3,
		"GPL": L.GPL_X,
		"MPL": L.MPL,
		"EUPL": L.EU,
		"PROPRIETARY": L.PROPRIETARY,
	}
	for liceStr, lice in termToLicense.items():
		if liceStr in licenseStr:
			return lice
	if licenseStr not in (ignoreLicenses or ""):
		logger.warning(f"'{licenseStr}' License not identified so falling back to NO_LICENSE")
	return L.NO_LICENSE


def licenseType(lice: ucstr, ignoreLicenses: list[ucstr] | None = None) -> list[L]:
	"""Return a list of license types from a license string.

	Args:
	----
		lice (ucstr): license name
		ignoreLicenses (list[ucstr]): a list of licenses to ignore (skipped, compat may still be
		False)

	Returns:
	-------
		list[L]: the license

	"""
	if len(lice or "") < 1:
		return [L.NO_LICENSE]
	return [licenseLookup(ucstr(x), ignoreLicenses) for x in lice.split(JOINS)]


def depCompatWMyLice(
	myLicense: L,
	depLice: list[L],
	ignoreLicenses: list[L] | None = None,
	failLicenses: list[L] | None = None,
	onlyLicenses: list[L] | None = None,
) -> bool:
	"""Identify if the end user license is compatible with the dependency license(s).

	Args:
	----
		myLicense (L): end user license to check
		depLice (list[L]): dependency license
		ignoreLicenses (list[L], optional): list of licenses to ignore. Defaults to None.
		failLicenses (list[L], optional): list of licenses to fail on. Defaults to None.
		onlyLicenses (list[L], optional): list of allowed licenses. Defaults to None.

	Returns:
	-------
		bool: True if compatible, otherwise False

	"""

	# Protect against None
	failLicenses = failLicenses or []
	ignoreLicenses = ignoreLicenses or []
	onlyLicenses = onlyLicenses or []

	return any(
		liceCompat(
			myLicense,
			lice,
			ignoreLicenses,
			failLicenses,
			onlyLicenses,
		)
		for lice in depLice
	)


def liceCompat(
	myLicense: L,
	lice: L,
	ignoreLicenses: list[L],
	failLicenses: list[L],
	onlyLicenses: list[L],
) -> bool:
	"""Identify if the end user license is compatible with the dependency license.

	:param L myLicense: end user license
	:param L lice: dependency license
	:param list[L] ignoreLicenses: list of licenses to ignore. Defaults to None.
	:param list[L] failLicenses: list of licenses to fail on. Defaults to None.
	:param list[L] onlyLicenses: list of allowed licenses. Defaults to None.
	:return bool: True if compatible, otherwise False
	"""
	if lice in failLicenses:
		return False
	if lice in ignoreLicenses:
		return True
	if len(onlyLicenses) > 0 and (lice not in onlyLicenses):
		return False
	licenses = list(L)
	row, col = licenses.index(myLicense) + 1, licenses.index(lice) + 1

	if LICENSE_MATRIX[row][col] == "1":
		return True
	return False
