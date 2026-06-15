from __future__ import annotations

from dataclasses import dataclass, field

from licensecheck.models.constants import UNKNOWN


@dataclass(unsafe_hash=True, order=True)
class PackageInfo:
	"""PackageInfo type."""

	name: str
	version: str | None = None
	namever: str = field(init=False)
	size: int | None = None
	homePage: str | None = None
	author: str | None = None
	license: str | None = None
	licenseCompat: bool = False
	errorCode: int = 0

	def __post_init__(self) -> None:
		"""Set the namever once the object is initialised."""
		self.namever = f"{self.name}-{self.version or UNKNOWN}"

	def get_filtered_dict(self, hide_output_parameters: set[str]) -> dict:
		"""
		Return a filtered dictionary of the object.

		:param set[str] hide_output_parameters: set of parameters to ignore
		:return dict: filtered dictionary
		"""
		hide_output_parameters_upper = {x.upper() for x in hide_output_parameters}
		return {
			k: (v if v is not None else UNKNOWN)
			for k, v in self.__dict__.items()
			if k.upper() not in hide_output_parameters_upper
		}
