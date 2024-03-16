"""PackageCompat type."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import requests_cache

THISDIR = Path(__file__).resolve().parent


session = requests_cache.CachedSession(f"{THISDIR}/licensecheck")


class ucstr(str):
	"""Uppercase string."""

	__slots__ = ()

	def __new__(cls, v: str) -> ucstr:
		"""Create a new ucstr from a str.

		:param str v: string to cast
		:return ucstr: uppercase string.
		"""
		return super().__new__(cls, v.upper())


UNKNOWN = ucstr("UNKNOWN")
JOINS = ucstr(";; ")


@dataclass(unsafe_hash=True, order=True)
class PackageInfo:
	"""PackageInfo type."""

	name: str
	version: str = UNKNOWN
	namever: str = field(init=False)
	size: int = -1
	homePage: str = UNKNOWN
	author: str = UNKNOWN
	license: ucstr = UNKNOWN
	licenseCompat: bool = False
	errorCode: int = 0

	def __post_init__(self) -> None:
		"""Set the namever once the object is initialised."""
		self.namever = f"{self.name}-{self.version}"

	def get_filtered_dict(self, hide_output_parameters: list[str]) -> dict:
		"""Return a filtered dictionary of the object.

		:param list[str] hide_output_parameters: list of parameters to ignore
		:return dict: filtered dictionary
		"""
		return {k: v for k, v in self.__dict__.items() if k.upper() not in hide_output_parameters}


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
	"""Output a license as plain text.

	:param L licenseEnum: License
	:return str: license of plain text
	"""

	licenseMap = {
		L.PUBLIC: "PUBLIC DOMAIN/ CC-PDDC/ CC0-1.0",
		L.UNLICENSE: "UNLICENSE/ WTFPL",
		L.BOOST: "BOOST/ BSL-1.0",
		L.MIT: "MIT",
		L.BSD: "BSD",
		L.ISC: "ISC",
		L.NCSA: "NCSA",
		L.PSFL: "PYTHON/ PSF-2.0",
		L.APACHE: "APACHE",
		L.ECLIPSE: "ECLIPSE",
		L.ACADEMIC_FREE: "AFL",
		L.LGPL_2_PLUS: "LGPLV2+/ LGPL-2.0-OR-LATER",
		L.LGPL_3_PLUS: "LGPLV3+/ LGPL-3.0-OR-LATER",
		L.LGPL_2: "LGPL-2.0-ONLY/ LGPLV2",
		L.LGPL_3: "LGPL-3.0-ONLY/ LGPLV3",
		L.LGPL_X: "LGPL",
		L.AGPL_3_PLUS: "AGPL",
		L.GPL_2_PLUS: "GPL-2.0-OR-LATER/ GPLV2+",
		L.GPL_3_PLUS: "GPL-3.0-OR-LATER/ GPLV3+",
		L.GPL_2: "GPLV2/ GPL-2.0",
		L.GPL_3: "GPLV3/ GPL-3.0",
		L.GPL_X: "GPL",
		L.MPL: "MPL",
		L.EU: "EUPL",
		L.PROPRIETARY: "PROPRIETARY",
		L.NO_LICENSE: "NO LICENSE/ UNKNOWN",
	}

	if licenseEnum not in licenseMap:
		return "NO LICENSE/ UNKNOWN LICENSE"

	return f"{licenseMap[licenseEnum]} LICENSE"
