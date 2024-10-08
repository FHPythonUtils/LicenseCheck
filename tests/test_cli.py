from pathlib import Path

import pytest

from licensecheck import formatter, main

THISDIR = str(Path(__file__).resolve().parent)


formatter.INFO = {"program": "licensecheck", "version": "dev", "license": "MIT LICENSE"}


def aux_get_text(file: str) -> str:
	return Path(file).read_text("utf-8").replace("\r\n", "\n")


def aux_file(file: str) -> str:
	return f"{THISDIR}/data/{file}"


test_data = [
	({"license": "MIT", "file": aux_file("test_main_tc1.txt"), "requirements_paths": ["pyproject.toml"]}, 0),
	(
		{
			"license": "BSD",
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
			"file": aux_file("test_main_tc4.json"),
			"requirements_paths": ["pyproject.toml"],
			"format": "json",
			"hide_output_parameters": ["size", "version", "namever"],
		},
		0,
	),
]


@pytest.mark.parametrize(("args", "expected_exit_code"), test_data)
def test_main(args, expected_exit_code) -> None:
	exit_code = main(args)
	assert exit_code == expected_exit_code
	assert aux_get_text(args["file"]).replace(
		"typing_extensions",
		"typing-extensions",  # for python 3.8
	) == aux_get_text(args["file"].replace(".", "_expected."))
