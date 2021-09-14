"""PackageCompat type.
"""
import typing
from enum import Enum


class PackageInfo(typing.TypedDict):
	"""PackageInfo type."""

	name: str
	version: str
	namever: str
	size: int
	home_page: str
	author: str
	license: str


class PackageCompat(PackageInfo):
	"""PackageCompat type."""

	license_compat: bool


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
