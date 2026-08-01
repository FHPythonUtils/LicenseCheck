from __future__ import annotations

from dataclasses import field
from typing import Any, Literal

from depgather.models.defaultonnone import DefaultOnNoneModel
from packaging.requirements import InvalidRequirement, Requirement
from pydantic import field_validator

from licensecheck.io.fmt import FMT


class LC_Config(DefaultOnNoneModel):
	"""LC_Config type."""

	file: str = ""
	license: str = ""
	format: FMT = FMT.simple
	pypi_api: str = ""
	show_only_failing: bool = False
	zero: bool = False

	requirements_paths: set[str] = field(default_factory=set)
	groups: set[str] = field(default_factory=set)
	extras: set[str] = field(default_factory=set)
	ignore_packages: set[str] = field(default_factory=set)
	license_overrides: dict[str, str] = field(default_factory=dict)
	fail_packages: set[str] = field(default_factory=set)
	ignore_licenses: set[str] = field(default_factory=set)
	allowed_license_references: set[str] = field(default_factory=set)
	fail_licenses: set[str] = field(default_factory=set)
	only_licenses: set[str] = field(default_factory=set)
	skip_dependencies: set[str] = field(default_factory=set)
	hide_output_parameters: set[str] = field(default_factory=set)

	@field_validator("format", mode="before")
	@classmethod
	def normalize_format(cls, value: Any) -> Any | Literal[FMT.simple]:
		if value not in FMT:
			return FMT.simple
		return value

	@field_validator("license_overrides")
	@classmethod
	def validate_license_overrides(cls, value: dict[str, str]) -> dict[str, str]:
		for package, license_value in value.items():
			try:
				requirement = Requirement(package)
			except InvalidRequirement as exc:
				message = f"Invalid license override package: {package}"
				raise ValueError(message) from exc

			specifiers = list(requirement.specifier)
			if (
				requirement.url
				or requirement.extras
				or requirement.marker
				or len(specifiers) != 1
				or specifiers[0].operator != "=="
				or specifiers[0].version.endswith(".*")
			):
				message = f"License override packages must use an exact name==version: {package}"
				raise ValueError(message)
			if not license_value.strip():
				message = f"License override must not be empty: {package}"
				raise ValueError(message)
		return value
