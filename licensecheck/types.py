"""PackageCompat type."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


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

	def get_filtered_dict(self, hide_output_parameters: list[ucstr]) -> dict:
		"""Return a filtered dictionary of the object.

		:param list[ucstr] hide_output_parameters: list of parameters to ignore
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
