"""PackageCompat type.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

UNKNOWN = "UNKNOWN"
JOINS = ";; "


@dataclass(unsafe_hash=True, order=True)
class PackageInfo:
	"""PackageInfo type."""

	name: str
	version: str = UNKNOWN
	namever: str = field(init=False)
	size: int = -1
	homePage: str = UNKNOWN
	author: str = UNKNOWN
	license: str = UNKNOWN
	licenseCompat: bool = False
	errorCode: int = 0

	def __post_init__(self):
		self.namever = f"{self.name}-{self.version}"


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
	ACADEMIC_FREE = 22
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
	# PROPRIETARY
	PROPRIETARY = 190
	# No License
	NO_LICENSE = 200


L = License


def printLicense(licenseEnum: L) -> str:
	"""Output a license as plain text

	:param L licenseEnum: License
	:return str: license of plain text
	"""

	licenseMap = {
		L.PUBLIC: "public domain/ cc-pddc/ cc0-1.0",
		L.UNLICENSE: "unlicense/ wtfpl",
		L.BOOST: "boost/ bsl-1.0",
		L.MIT: "mit",
		L.BSD: "bsd",
		L.ISC: "isc",
		L.NCSA: "ncsa",
		L.PSFL: "python/ psf-2.0",
		L.APACHE: "apache",
		L.ECLIPSE: "eclipse",
		L.ACADEMIC_FREE: "afl",
		L.LGPL_2_PLUS: "lgplv2+/ lgpl-2.0-or-later",
		L.LGPL_3_PLUS: "lgplv3+/ lgpl-3.0-or-later",
		L.LGPL_2: "lgpl-2.0-only/ lgplv2",
		L.LGPL_3: "lgpl-3.0-only/ lgplv3",
		L.LGPL_X: "lgpl",
		L.AGPL_3_PLUS: "agpl",
		L.GPL_2_PLUS: "gpl-2.0-or-later/ gplv2+",
		L.GPL_3_PLUS: "gpl-3.0-or-later/ gplv3+",
		L.GPL_2: "gplv2/ gpl-2.0",
		L.GPL_3: "gplv3/ gpl-3.0",
		L.GPL_X: "gpl",
		L.MPL: "mpl",
		L.EU: "eupl",
		L.PROPRIETARY: "proprietary",
		L.NO_LICENSE: "no license/ unknown",
	}

	if licenseEnum not in licenseMap:
		return "no license/ unknown"

	return licenseMap[licenseEnum]
