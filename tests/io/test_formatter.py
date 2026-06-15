from __future__ import annotations

from pathlib import Path

import pytest

from licensecheck.io import fmt
from licensecheck.models.license import License
from licensecheck.models.packageinfo import PackageInfo

fmt.INFO = {"program": "licensecheck", "version": "dev", "license": "MIT LICENSE"}

THISDIR = str(Path(__file__).resolve().parent)


simplePackages = [PackageInfo(name="example")]
complexPackages = [
	PackageInfo(
		name="example0",
		version="1.0.0",
		size=10,
		homePage="https://example.com",
		author="example_author",
		license="mit",
		licenseCompat=True,
		errorCode=0,
	),
	PackageInfo(
		name="example1",
		size=10,
		homePage="https://example.com",
		author="example_author",
		license="gpl3",
		licenseCompat=False,
		errorCode=1,
	),
]
myLice = License.MIT


@pytest.mark.parametrize(
	("_fmt", "packages", "expected_output_file", "hide_params"),
	[
		("markdown", simplePackages, "simple.md", None),
		("markdown", complexPackages, "advanced.md", None),
		("markdown", complexPackages, "advanced_ignore_params.md", []),
		("json", simplePackages, "simple.json", None),
		("json", complexPackages, "advanced.json", None),
		(
			"json",
			complexPackages,
			"advanced_ignore_params.json",
			["HOMEPAGE", "AUTHOR"],
		),
		(
			"json",
			complexPackages,
			"advanced_ignore_params2.json",
			["homepage", "author"],
		),
		("csv", simplePackages, "simple.csv", None),
		("csv", complexPackages, "advanced.csv", None),
		("ansi", simplePackages, "simple.ansi", None),
		("ansi", complexPackages, "advanced.ansi", None),
		("ansi", complexPackages, "advanced.ansi", []),
		("simple", simplePackages, "simple.txt", None),
		("simple", complexPackages, "advanced.txt", None),
		("simple", complexPackages, "advanced.txt", ["WRONG_PARAMETER"]),
	],
)
def test_output__fmt(
	_fmt: str,
	packages: list[PackageInfo],
	expected_output_file: str,
	hide_params: list[str] | None,
) -> None:
	actual_output = fmt.fmt(_fmt, myLice, packages, hide_parameters=hide_params)
	expected_output = Path(f"{THISDIR}/data/fmt/{expected_output_file}")
	# expected_output.write_text(actual_output, "utf-8")
	assert assert_eq(actual_output, expected_output.read_text("utf-8"))


def assert_eq(actual_input: str, expected_output: str) -> bool:
	actual = actual_input.strip().splitlines()
	expected = expected_output.strip().splitlines()

	if len(expected) != len(actual):
		return False

	return [x.strip() for x in actual] == [x.strip() for x in expected]
