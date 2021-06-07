"""Define a foss compatability license_matrix.

Standard disclaimer:: I am not a lawyer and there is no guarentee that the
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
- Acedemic Free


Copyleft
permissive -> lgpl 2.1 -> gpl 2
permissive -> lgpl 3 -> gpl 3 -> agpl
permissive -> mpl -> gpl -> agpl (3 only)

permissive (any) -> EU
EU -> gpl -> agpl (3 only)
"""
from __future__ import annotations

from enum import Enum


class License(Enum):
	"""License Enum to hold a set of potential licenses."""

	# Public domain
	PUBLIC = 0
	UNLICENSE = 1
	# Permissive GPL compatible
	MIT = 10
	BOOST = 11
	BSD = 12
	ISC = 13
	NCSA = 14
	PSFL = 15
	# Other permissive
	APACHE = 20
	ECLIPSE = 21
	ACEDEMIC_FREE = 22
	# LGPL
	LGPL_X = 30
	LGPL_2 = 31
	LGPL_3 = 32
	LGPL_2_PLUS = 33
	LGPL_3_PLUS = 34
	# GPL
	GPL_X = 40
	GPL_2 = 41
	GPL_3 = 42
	GPL_2_PLUS = 43
	GPL_3_PLUS = 44
	# AGPL
	AGPL_3_PLUS = 50
	# Other copyleft
	MPL = 60
	EU = 61

	# No License
	NO_LICENSE = 200


def licenseType(lice: str) -> list[License]:
	"""Return a list of license types from a license string.

	Args:
		lice (str): license name

	Returns:
		list[License]: the license
	"""
	licenses = []
	liceL = lice.split(", ")  # Deal with multilicense
	for liceS in liceL:
		lice = liceS.upper()
		if "PUBLIC DOMAIN" in lice:
			licenses.append(License.PUBLIC)
		elif "UNLICENSE" in lice:
			licenses.append(License.UNLICENSE)

		elif "MIT" in lice:
			licenses.append(License.MIT)
		elif "BOOST" in lice:
			licenses.append(License.BOOST)
		elif "BSD" in lice:
			licenses.append(License.BSD)
		elif "ISC" in lice:
			licenses.append(License.ISC)
		elif "NCSA" in lice:
			licenses.append(License.NCSA)
		elif "PYTHON" in lice:
			licenses.append(License.PSFL)

		elif "APACHE" in lice:
			licenses.append(License.APACHE)
		elif "ECLIPSE" in lice:
			licenses.append(License.ECLIPSE)
		elif "AFL" in lice:
			licenses.append(License.ACEDEMIC_FREE)

		elif "LGPL" in lice:
			if "LGPLV2+" in lice:
				licenses.append(License.LGPL_2_PLUS)
			elif "LGPLV3+" in lice:
				licenses.append(License.LGPL_3_PLUS)
			elif "LGPLV2+" in lice:
				licenses.append(License.LGPL_2_PLUS)
			elif "LGPLV3+" in lice:
				licenses.append(License.LGPL_3_PLUS)
			else:
				licenses.append(License.LGPL_X)
		elif "AGPL" in lice:
			licenses.append(License.AGPL_3_PLUS)
		elif "GPL" in lice:
			if "GPLV2+" in lice:
				licenses.append(License.GPL_2_PLUS)
			elif "GPLV3+" in lice:
				licenses.append(License.GPL_3_PLUS)
			elif "GPLV2+" in lice:
				licenses.append(License.GPL_2_PLUS)
			elif "GPLV3+" in lice:
				licenses.append(License.GPL_3_PLUS)
			else:
				licenses.append(License.GPL_X)

		elif "MPL" in lice:
			licenses.append(License.MPL)
		elif "EUPL" in lice:
			licenses.append(License.EU)
		else:
			licenses.append(License.NO_LICENSE)
	return licenses


# Permissive licenses compatible with GPL
PERMISSIVE = [License.MIT, License.BOOST, License.BSD, License.ISC, License.NCSA, License.PSFL]
# Permissive licenses NOT compatible with GPL
PERMISSIVE_OTHER = [License.APACHE, License.ECLIPSE, License.ACEDEMIC_FREE]
# LGPL licenses
LGPL = [License.LGPL_2, License.LGPL_3, License.LGPL_2_PLUS, License.LGPL_3_PLUS, License.LGPL_X]
# GPL licenses (including AGPL)
GPL = [
	License.GPL_2,
	License.GPL_3,
	License.GPL_2_PLUS,
	License.GPL_3_PLUS,
	License.GPL_X,
	License.AGPL_3_PLUS,
]
# Other Copyleft licenses
OTHER_COPYLEFT = [License.MPL, License.EU]

# Basic compat matrix
UNLICENSEE_INCOMPATIBLE = (
	PERMISSIVE + PERMISSIVE_OTHER + GPL + LGPL + OTHER_COPYLEFT + [License.NO_LICENSE]
)
PERMISSIVE_INCOMPATIBLE = GPL + [License.EU, License.NO_LICENSE]
LGPL_INCOMPATIBLE = GPL + OTHER_COPYLEFT + PERMISSIVE_OTHER + [License.NO_LICENSE]
GPL_INCOMPATIBLE = PERMISSIVE_OTHER + [License.AGPL_3_PLUS, License.NO_LICENSE]
PERMISSIVE_GPL_INCOMPATIBLE = PERMISSIVE_OTHER + [License.NO_LICENSE]

# GPL compat matrix
# https://www.gnu.org/licenses/gpl-faq.html#AllCompatibility
GPL_2_INCOMPATIBLE = [License.GPL_3, License.GPL_3_PLUS, License.LGPL_3, License.LGPL_3_PLUS]
L_GPL_3_INCOMPATIBLE = [License.GPL_2]


def depCompatibleLice(myLicense: License, depLice: list[License]) -> bool:
	"""Identify if the end user license is compatible with the dependency license(s).

	Args:
		myLicense (License): end user license to check
		depLice (list[License]): dependency license

	Returns:
		bool: True if compatible, otherwise False
	"""
	blacklist = {
		License.UNLICENSE: UNLICENSEE_INCOMPATIBLE,
		License.PUBLIC: UNLICENSEE_INCOMPATIBLE,
		License.MIT: PERMISSIVE_INCOMPATIBLE,
		License.BOOST: PERMISSIVE_INCOMPATIBLE,
		License.BSD: PERMISSIVE_INCOMPATIBLE,
		License.ISC: PERMISSIVE_INCOMPATIBLE,
		License.NCSA: PERMISSIVE_INCOMPATIBLE,
		License.PSFL: PERMISSIVE_INCOMPATIBLE,
		License.APACHE: PERMISSIVE_INCOMPATIBLE,
		License.ECLIPSE: PERMISSIVE_INCOMPATIBLE,
		License.ACEDEMIC_FREE: PERMISSIVE_INCOMPATIBLE,
		License.LGPL_X: LGPL_INCOMPATIBLE,
		License.LGPL_2: LGPL_INCOMPATIBLE,
		License.LGPL_3: LGPL_INCOMPATIBLE + L_GPL_3_INCOMPATIBLE,
		License.LGPL_2_PLUS: LGPL_INCOMPATIBLE,
		License.LGPL_3_PLUS: LGPL_INCOMPATIBLE + L_GPL_3_INCOMPATIBLE,
		License.GPL_X: GPL_INCOMPATIBLE,
		License.GPL_2: GPL_INCOMPATIBLE + GPL_2_INCOMPATIBLE,
		License.GPL_3: GPL_INCOMPATIBLE + L_GPL_3_INCOMPATIBLE,
		License.GPL_2_PLUS: GPL_INCOMPATIBLE,
		License.GPL_3_PLUS: GPL_INCOMPATIBLE + L_GPL_3_INCOMPATIBLE,
		License.AGPL_3_PLUS: PERMISSIVE_GPL_INCOMPATIBLE,
		License.MPL: LGPL + GPL + [License.EU],
		License.EU: PERMISSIVE_GPL_INCOMPATIBLE + LGPL + GPL + [License.MPL],
	}

	blacklistResolved = blacklist[myLicense]
	for lice in depLice:
		if lice in blacklistResolved:
			return False
	return True
