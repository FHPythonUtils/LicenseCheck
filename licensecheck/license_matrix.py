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

from licensecheck.types import License as L


def licenseLookup(licenseStr: str) -> L:
	"""Identify a license from an uppercase string representation of a license.

	Args:
		licenseStr (str): uppercase string representation of a license

	Returns:
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
		"GPL-2.0-OR-LATER": L.GPL_2_PLUS,
		"GPLV2+": L.GPL_2_PLUS,
		"GPL-3.0-OR-LATER": L.GPL_3_PLUS,
		"GPLV3+": L.GPL_3_PLUS,
		"GPLV2": L.GPL_2,
		"GPL-2.0": L.GPL_2,
		"GPLV3": L.GPL_3,
		"GPL-3.0": L.GPL_3,
		"MPL": L.MPL,
		"EUPL": L.EU,
		"PROPRIETARY": L.PROPRIETARY,
	}
	for liceStr, lice in termToLicense.items():
		if liceStr in licenseStr:
			return lice

	print(f"WARN: '{licenseStr}' License not identified so falling back to NO_LICENSE")
	return L.NO_LICENSE


def licenseType(lice: str) -> list[L]:
	"""Return a list of license types from a license string.

	Args:
		lice (str): license name

	Returns:
		list[L]: the license
	"""
	if len(lice) < 1:
		return []
	return [licenseLookup(x) for x in lice.upper().split(", ")]


# Permissive licenses compatible with GPL
PERMISSIVE = [
	L.MIT,
	L.BOOST,
	L.BSD,
	L.ISC,
	L.NCSA,
	L.PSFL,
]
# Permissive licenses NOT compatible with GPL
PERMISSIVE_OTHER = [
	L.APACHE,
	L.ECLIPSE,
	L.ACADEMIC_FREE,
]
# LGPL licenses
LGPL = [
	L.LGPL_2,
	L.LGPL_3,
	L.LGPL_2_PLUS,
	L.LGPL_3_PLUS,
	L.LGPL_X,
]
# GPL licenses (including AGPL)
GPL = [
	L.GPL_2,
	L.GPL_3,
	L.GPL_2_PLUS,
	L.GPL_3_PLUS,
	L.GPL_X,
	L.AGPL_3_PLUS,
]
# Other Copyleft licenses
OTHER_COPYLEFT = [
	L.MPL,
	L.EU,
]

# Basic compat matrix
UNLICENSE_INCOMPATIBLE = (
	PERMISSIVE + PERMISSIVE_OTHER + GPL + LGPL + OTHER_COPYLEFT + [L.NO_LICENSE, L.PROPRIETARY]
)
PERMISSIVE_INCOMPATIBLE = GPL + [L.EU, L.NO_LICENSE, L.PROPRIETARY]
LGPL_INCOMPATIBLE = GPL + OTHER_COPYLEFT + PERMISSIVE_OTHER + [L.NO_LICENSE, L.PROPRIETARY]
GPL_INCOMPATIBLE = PERMISSIVE_OTHER + [L.AGPL_3_PLUS, L.NO_LICENSE, L.PROPRIETARY]
PERMISSIVE_GPL_INCOMPATIBLE = PERMISSIVE_OTHER + [L.NO_LICENSE, L.PROPRIETARY]

# GPL compat matrix
# https://www.gnu.org/licenses/gpl-faq.html#AllCompatibility
GPL_2_INCOMPATIBLE = [L.GPL_3, L.GPL_3_PLUS, L.LGPL_3, L.LGPL_3_PLUS]
L_GPL_3_INCOMPATIBLE = [L.GPL_2]


def depCompatWMyLice(
	myLicense: L,
	depLice: list[L],
	ignoreLicenses: list[L] | None = None,
	failLicenses: list[L] | None = None,
) -> bool:
	"""Identify if the end user license is compatible with the dependency license(s).

	Args:
		myLicense (L): end user license to check
		depLice (list[L]): dependency license
		ignoreLicenses (list[L], optional): list of licenses to ignore. Defaults to None.
		failLicenses (list[L], optional): list of licenses to fail on. Defaults to None.

	Returns:
		bool: True if compatible, otherwise False
	"""
	blacklist = {
		L.UNLICENSE: UNLICENSE_INCOMPATIBLE,
		L.PUBLIC: UNLICENSE_INCOMPATIBLE,
		L.MIT: PERMISSIVE_INCOMPATIBLE,
		L.BOOST: PERMISSIVE_INCOMPATIBLE,
		L.BSD: PERMISSIVE_INCOMPATIBLE,
		L.ISC: PERMISSIVE_INCOMPATIBLE,
		L.NCSA: PERMISSIVE_INCOMPATIBLE,
		L.PSFL: PERMISSIVE_INCOMPATIBLE,
		L.APACHE: PERMISSIVE_INCOMPATIBLE,
		L.ECLIPSE: PERMISSIVE_INCOMPATIBLE,
		L.ACADEMIC_FREE: PERMISSIVE_INCOMPATIBLE,
		L.LGPL_X: LGPL_INCOMPATIBLE,
		L.LGPL_2: LGPL_INCOMPATIBLE,
		L.LGPL_3: LGPL_INCOMPATIBLE + L_GPL_3_INCOMPATIBLE,
		L.LGPL_2_PLUS: LGPL_INCOMPATIBLE,
		L.LGPL_3_PLUS: LGPL_INCOMPATIBLE + L_GPL_3_INCOMPATIBLE,
		L.GPL_X: GPL_INCOMPATIBLE,
		L.GPL_2: GPL_INCOMPATIBLE + GPL_2_INCOMPATIBLE,
		L.GPL_3: GPL_INCOMPATIBLE + L_GPL_3_INCOMPATIBLE,
		L.GPL_2_PLUS: GPL_INCOMPATIBLE,
		L.GPL_3_PLUS: GPL_INCOMPATIBLE + L_GPL_3_INCOMPATIBLE,
		L.AGPL_3_PLUS: PERMISSIVE_GPL_INCOMPATIBLE,
		L.MPL: LGPL + GPL + [L.EU],
		L.EU: PERMISSIVE_GPL_INCOMPATIBLE + LGPL + GPL + [L.MPL],
		L.PROPRIETARY: PERMISSIVE_INCOMPATIBLE,
	}
	# Protect against None
	failLicenses = failLicenses or []
	ignoreLicenses = ignoreLicenses or []
	blacklistResolved = blacklist[myLicense]
	for lice in depLice:
		if lice in failLicenses or (lice not in ignoreLicenses and lice in blacklistResolved):
			return False
	return True
