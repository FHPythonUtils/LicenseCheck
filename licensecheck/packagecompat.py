import typing


class PackageCompat(typing.TypedDict):
	"""PackageCompat type
	"""
	name: str
	version: str
	namever: str
	size: int
	home_page: str
	author: str
	license: str
	license_compat: bool
