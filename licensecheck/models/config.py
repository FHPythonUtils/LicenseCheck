from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(unsafe_hash=True, order=True)
class LC_Config:
	"""LC_Config type."""

	file: str | None
	license: str | None
	format: str | None
	pypi_api: str | None
	show_only_failing: bool
	zero: bool

	requirements_paths: set[str] = field(default_factory=set)
	groups: set[str] = field(default_factory=set)
	extras: set[str] = field(default_factory=set)
	ignore_packages: set[str] = field(default_factory=set)
	fail_packages: set[str] = field(default_factory=set)
	ignore_licenses: set[str] = field(default_factory=set)
	fail_licenses: set[str] = field(default_factory=set)
	only_licenses: set[str] = field(default_factory=set)
	skip_dependencies: set[str] = field(default_factory=set)
	hide_output_parameters: set[str] = field(default_factory=set)

	@staticmethod
	def from_mapping(**kwargs: dict[str, Any]) -> LC_Config:
		for key in (
			"requirements_paths",
			"groups",
			"extras",
			"ignore_packages",
			"fail_packages",
			"fail_licenses",
			"only_licenses",
			"skip_dependencies",
			"hide_output_parameters",
		):
			kwargs[key] = set(kwargs.get(key) or ())
		return LC_Config(**kwargs)
