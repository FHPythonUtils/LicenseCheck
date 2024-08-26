"""Output the licenses used by dependencies and check if these are compatible with the project
license.
"""

from __future__ import annotations

import argparse
from dataclasses import fields
from pathlib import Path
from sys import exit as sysexit
from sys import stdout

from fhconfparser import FHConfParser, SimpleConf

from licensecheck import formatter, get_deps, license_matrix, packageinfo, types

stdout.reconfigure(encoding="utf-8")  # type: ignore[general-type-issues]


def cli() -> None:  # pragma: no cover
	"""Cli entry point."""
	parser = argparse.ArgumentParser(description=__doc__, argument_default=argparse.SUPPRESS)
	parser.add_argument(
		"--license",
		"-l",
		help="",
	)
	parser.add_argument(
		"--format",
		"-f",
		help=f"Output format. one of: {', '.join(list(formatter.formatMap))}. default=simple",
	)
	parser.add_argument(
		"--file",
		"-o",
		help="Filename to write to (omit for stdout)",
	)
	parser.add_argument(
		"--using",
		"-u",
		help="Environment to use e.g. requirements.txt. one of: "
		f"{', '.join(get_deps.USINGS)}. default=poetry",
	)
	parser.add_argument(
		"--ignore-packages",
		help="a list of packages to ignore (compat=True)",
		nargs="+",
	)
	parser.add_argument(
		"--fail-packages",
		help="a list of packages to fail (compat=False)",
		nargs="+",
	)
	parser.add_argument(
		"--ignore-licenses",
		help="a list of licenses to ignore (skipped, compat may still be False)",
		nargs="+",
	)
	parser.add_argument(
		"--fail-licenses",
		help="a list of licenses to fail (compat=False)",
		nargs="+",
	)
	parser.add_argument(
		"--only-licenses",
		help="a list of allowed licenses (any other license will fail)",
		nargs="+",
	)
	parser.add_argument(
		"--skip-dependencies",
		help="a list of packages to skip (compat=True)",
		nargs="+",
	)
	parser.add_argument(
		"--hide-output-parameters",
		help="a list of parameters to hide from the produced output",
		nargs="+",
	)
	parser.add_argument(
		"--zero",
		"-0",
		help="Return non zero exit code if an incompatible license is found",
		action="store_true",
	)
	args = vars(parser.parse_args())
	sysexit(main(args))


def main(args: dict) -> int:
	"""Test entry point.

	Note: FHConfParser (Parses in the following order: `pyproject.toml`,
	`setup.cfg`, `licensecheck.toml`, `licensecheck.json`,
	`licensecheck.ini`, `~/licensecheck.toml`, `~/licensecheck.json`, `~/licensecheck.ini`)
	"""
	exitCode = 0

	configparser = FHConfParser()
	namespace = ["tool"]
	configparser.parseConfigList(
		[("pyproject.toml", "toml"), ("setup.cfg", "ini")]
		+ [
			(f"{directory}/licensecheck.{ext}", ext)
			for ext in ("toml", "json", "ini")
			for directory in [".", str(Path.home())]
		],
		namespace,
		namespace,
	)
	simpleConf = SimpleConf(configparser, "licensecheck", args)

	# File
	textIO = (
		stdout
		if simpleConf.get("file") is None
		else Path(simpleConf.get("file")).open("w", encoding="utf-8")
	)

	# Get my license
	myLiceTxt = args["license"] if args.get("license") else packageinfo.getMyPackageLicense()
	myLice = license_matrix.licenseType(myLiceTxt)[0]

	# Get list of licenses
	depsWithLicenses = get_deps.getDepsWithLicenses(
		simpleConf.get("using", "poetry"),
		myLice,
		list(map(types.ucstr, simpleConf.get("ignore_packages", []))),
		list(map(types.ucstr, simpleConf.get("fail_packages", []))),
		list(map(types.ucstr, simpleConf.get("ignore_licenses", []))),
		list(map(types.ucstr, simpleConf.get("fail_licenses", []))),
		list(map(types.ucstr, simpleConf.get("only_licenses", []))),
		list(map(types.ucstr, simpleConf.get("skip_dependencies", []))),
	)

	# Are any licenses incompatible?
	incompatible = any(not lice.licenseCompat for lice in depsWithLicenses)

	# Format the results
	hide_output_parameters = [types.ucstr(x) for x in simpleConf.get("hide_output_parameters", [])]
	available_params = [param.name.upper() for param in fields(types.PackageInfo)]
	if not all(hop in available_params for hop in hide_output_parameters):
		msg = (
			f"Invalid parameter(s) in `hide_output_parameters`. "
			f"Valid parameters are: {', '.join(available_params)}"
		)
		raise ValueError(msg)
	if simpleConf.get("format", "simple") in formatter.formatMap:
		print(
			formatter.formatMap[simpleConf.get("format", "simple")](
				myLice,
				sorted(depsWithLicenses),
				hide_output_parameters,
			),
			file=textIO,
		)
	else:
		exitCode = 2

	# Exit code of 1 if args.zero
	if simpleConf.get("zero", False) and incompatible:
		exitCode = 1

	# Cleanup + exit
	if simpleConf.get("file") is not None:
		textIO.close()
	return exitCode
