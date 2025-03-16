from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from licensecheck import fmt, main

THISDIR = str(Path(__file__).resolve().parent)


fmt.INFO = {"program": "licensecheck", "version": "dev", "license": "MIT LICENSE"}


def aux_get_text(file: str) -> str:
	return Path(file).read_text("utf-8").replace("\r\n", "\n")


def aux_file(file: str) -> str:
	return f"{THISDIR}/data/{file}"


test_data = [
	(
		{
			"license": "MIT",
			"pypi_api": "https://pypi.org/pypi/",
			"file": aux_file("test_main_tc1.txt"),
			"requirements_paths": ["pyproject.toml"],
		},
		0,
	),
	(
		{
			"license": "BSD",
			"pypi_api": "https://pypi.org/pypi/",
			"file": aux_file("test_main_tc3.txt"),
			"requirements_paths": ["pyproject.toml"],
			"ignore_packages": ["requests"],
			"ignore_licenses": ["GPL"],
		},
		0,
	),
	(
		{
			"license": "GPL",
			"pypi_api": "https://pypi.org/pypi/",
			"file": aux_file("test_main_tc4.json"),
			"requirements_paths": ["pyproject.toml"],
			"format": "json",
			"hide_output_parameters": ["size", "version", "namever"],
		},
		0,
	),
]


@pytest.mark.parametrize(("args", "expected_exit_code"), test_data)
def test_main(args: dict[str, Any], expected_exit_code: int) -> None:
	exit_code = main(args)
	assert exit_code == expected_exit_code
	# Path(args["file"].replace(".", "_expected.")).write_text(aux_get_text(args["file"]), encoding="utf-8")
	assert aux_get_text(args["file"]) == aux_get_text(args["file"].replace(".", "_expected."))
