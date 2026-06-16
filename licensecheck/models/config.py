from __future__ import annotations

from dataclasses import field

from licensecheck.models.defaultonnone import DefaultOnNoneModel
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
	fail_packages: set[str] = field(default_factory=set)
	ignore_licenses: set[str] = field(default_factory=set)
	fail_licenses: set[str] = field(default_factory=set)
	only_licenses: set[str] = field(default_factory=set)
	skip_dependencies: set[str] = field(default_factory=set)
	hide_output_parameters: set[str] = field(default_factory=set)
