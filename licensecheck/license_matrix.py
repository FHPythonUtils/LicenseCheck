"""Define a foss compatability license_matrix

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
	"""[License Enum to hold a set of potential licenses
	"""
	# Public domain
	PUBLIC = 0
	UNLICENSE = 1
	# Permissive GPL compatible
	MIT = 10
	BOOST = 11
	BSD = 12
	ISC = 13
	NCSA = 14
	# Other permissive
	APACHE = 20
	ECLIPSE = 21
	ACEDEMIC_FREE = 22
	# LGPL
	LGPL_X = 30
	LGPL_2 = 31
	LGPL_3 = 32
	# GPL
	GPL_X = 40
	GPL_2 = 41
	GPL_3 = 42
	# AGPL
	AGPL_3 = 50
	# Other copyleft
	MPL = 60
	EU = 61

	# Unknown
	UNKNOWN = 200

def licenseType(lice: str) -> list[License]:
	"""Return a list of license types from a license string

	Args:
		lice (str): license name

	Returns:
		list[License]: the license
	"""
	licenses = []
	liceL = lice.split(", ") # Deal with multilicense
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

		elif "APACHE" in lice:
			licenses.append(License.APACHE)
		elif "ECLIPSE" in lice:
			licenses.append(License.ECLIPSE)
		elif "AFL" in lice:
			licenses.append(License.ACEDEMIC_FREE)

		elif "LGPL" in lice:
			if "LGPLV2" in lice:
				licenses.append(License.LGPL_2)
			elif "LGPLV3" in lice:
				licenses.append(License.LGPL_3)
			else:
				licenses.append(License.LGPL_X)
		elif "AGPL" in lice:
			licenses.append(License.AGPL_3)
		elif "GPL" in lice:
			if "GPLV2" in lice:
				licenses.append(License.GPL_2)
			elif "GPLV3" in lice:
				licenses.append(License.GPL_3)
			else:
				licenses.append(License.GPL_X)

		elif "MPL" in lice:
			licenses.append(License.MPL)
		elif "EUPL" in lice:
			licenses.append(License.EU)
		else:
			licenses.append(License.UNKNOWN)
	return licenses

PERMISSIVE = [License.MIT, License.BOOST, License.BSD, License.ISC, License.NCSA]
PERMISSIVE_GPL_INCOMPATIBLE = [License.APACHE, License.ECLIPSE, License.ACEDEMIC_FREE]
LGPL = [License.LGPL_2, License.LGPL_3, License.LGPL_X]
GPL = [License.GPL_2, License.GPL_3, License.GPL_X, License.AGPL_3]
OTHER_COPYLEFT = [License.MPL, License.EU]

UNLICENSEE_INCOMPATIBLE = PERMISSIVE + PERMISSIVE_GPL_INCOMPATIBLE + GPL + LGPL + OTHER_COPYLEFT
PERMISSIVE_INCOMPATIBLE = GPL + [License.EU]
LGPL_INCOMPATIBLE = GPL + OTHER_COPYLEFT + PERMISSIVE_GPL_INCOMPATIBLE
GPL_INCOMPATIBLE = PERMISSIVE_GPL_INCOMPATIBLE + [License.AGPL_3]

def depCompatibleLice(myLicense: License, depLice: list[License]) -> bool:
	"""Identify if the end user license is compatible with the dependency
	license(s)

	Args:
		myLicense (License): end user license to check
		depLice (list[License]): dependency license

	Returns:
		bool: True if compatible, otherwise False
	"""
	blacklist = {License.UNLICENSE: UNLICENSEE_INCOMPATIBLE,
	License.PUBLIC: UNLICENSEE_INCOMPATIBLE,

	License.MIT: PERMISSIVE_INCOMPATIBLE,
	License.BOOST: PERMISSIVE_INCOMPATIBLE,
	License.BSD: PERMISSIVE_INCOMPATIBLE,
	License.ISC: PERMISSIVE_INCOMPATIBLE,
	License.NCSA: PERMISSIVE_INCOMPATIBLE,
	License.APACHE: PERMISSIVE_INCOMPATIBLE,
	License.ECLIPSE: PERMISSIVE_INCOMPATIBLE,
	License.ACEDEMIC_FREE: PERMISSIVE_INCOMPATIBLE,

	License.LGPL_X: LGPL_INCOMPATIBLE,
	License.LGPL_2: LGPL_INCOMPATIBLE,
	License.LGPL_3: LGPL_INCOMPATIBLE,
	License.GPL_X: GPL_INCOMPATIBLE,
	License.GPL_2: GPL_INCOMPATIBLE,
	License.GPL_3: GPL_INCOMPATIBLE,
	License.AGPL_3: PERMISSIVE_GPL_INCOMPATIBLE,

	License.MPL: LGPL + GPL + [License.EU],
	License.EU: PERMISSIVE_GPL_INCOMPATIBLE + LGPL + GPL + [License.MPL],
	}

	blacklistResolved = blacklist[myLicense]
	for lice in depLice:
		if lice in blacklistResolved:
			return False
	return True
