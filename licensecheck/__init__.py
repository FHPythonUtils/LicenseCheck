"""Output the licenses used by dependencies and check if these are compatible with the project license.
"""
from __future__ import annotations

import argparse
from functools import partial
from pathlib import Path
from sys import exit as sysexit, stdout

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
		help=f"Environment to use e.g. requirements.txt. one of: {', '.join(get_deps.usings)}. default=poetry",
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
	sc = SimpleConf(configparser, "licensecheck", args)

	# File
	filename = stdout if sc.get("file") is None else open(sc.get("file"), "w")

	# Get list of licenses
	dependenciesWLicenses = get_deps.getDepsWLicenses(
		sc.get("using", "poetry"),
		sc.get("ignore_packages", []),
		sc.get("fail_packages", []),
		sc.get("ignore_licenses", []),
		sc.get("fail_licenses", []),
	)

	# Are any licenses incompatible?
	incompatible = any(not lice["license_compat"] for lice in dependenciesWLicenses)

	# Format the results
	if sc.get("format", "simple") in formatter.formatMap:
		print(formatter.formatMap[sc.get("format", "simple")](dependenciesWLicenses), file=filename)
	else:
		exitCode = 2

	# Exit code of 1 if args.zero
	if sc.get("zero", False) and incompatible:
		exitCode = 1

	# Cleanup + exit
	filename.close()
	sysexit(exitCode)
