"""Output the licenses used by dependencies and check if these are compatible with the project
license.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from sys import exit as sysexit
from sys import stdout

from fhconfparser import FHConfParser, SimpleConf

from licensecheck import formatter, get_deps

stdout.reconfigure(encoding="utf-8")


def cli() -> None:
	"""Cli entry point."""
	exitCode = 0
	parser = argparse.ArgumentParser(description=__doc__, argument_default=argparse.SUPPRESS)
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
		"--zero",
		"-0",
		help="Return non zero exit code if an incompatible license is found",
		action="store_true",
	)
	args = vars(parser.parse_args())

	# ConfigParser (Parses in the following order: `pyproject.toml`,
	# `setup.cfg`, `licensecheck.toml`, `licensecheck.json`,
	# `licensecheck.ini`, `~/licensecheck.toml`, `~/licensecheck.json`, `~/licensecheck.ini`)
	configparser = FHConfParser()
	configparser.parseConfigList(
		[("pyproject.toml", "toml"), ("setup.cfg", "ini")]
		+ [
			(f"{directory}/licensecheck.{ext}", ext)
			for ext in ("toml", "json", "ini")
			for directory in [".", str(Path.home())]
		],
		["tool"],
		["tool"],
	)
	simpleConf = SimpleConf(configparser, "licensecheck", args)

	# File
	filename = (
		stdout
		if simpleConf.get("file") is None
		else open(simpleConf.get("file"), "w", encoding="utf-8")
	)

	# Get list of licenses
	myLice, depsWithLicenses = get_deps.getDepsWithLicenses(
		simpleConf.get("using", "poetry"),
		simpleConf.get("ignore_packages", []),
		simpleConf.get("fail_packages", []),
		simpleConf.get("ignore_licenses", []),
		simpleConf.get("fail_licenses", []),
	)

	# Are any licenses incompatible?
	incompatible = any(not lice.licenseCompat for lice in depsWithLicenses)

	# Format the results
	if simpleConf.get("format", "simple") in formatter.formatMap:
		print(
			formatter.formatMap[simpleConf.get("format", "simple")](myLice, sorted(depsWithLicenses)),
			file=filename,
		)
	else:
		exitCode = 2

	# Exit code of 1 if args.zero
	if simpleConf.get("zero", False) and incompatible:
		exitCode = 1

	# Cleanup + exit
	filename.close()
	sysexit(exitCode)
