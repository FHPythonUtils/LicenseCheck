"""Output the licenses used by dependencies and check if these are compatible with the project license.
"""
from __future__ import annotations

import argparse
from functools import partial
from pathlib import Path
from sys import exit as sysexit, stdout

from fhconfparser import FHConfParser

from licensecheck import formatter, get_deps

stdout.reconfigure(encoding="utf-8")


def cli() -> None:
	"""Cli entry point."""
	exitCode = 0
	parser = argparse.ArgumentParser(description=__doc__)
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
		default=[],
	)
	parser.add_argument(
		"--fail-packages", help="a list of packages to fail (compat=False)", nargs="+", default=[]
	)
	parser.add_argument(
		"--ignore-licenses",
		help="a list of licenses to ignore (skipped, compat may still be False)",
		nargs="+",
		default=[],
	)
	parser.add_argument(
		"--fail-licenses", help="a list of licenses to fail (compat=False)", nargs="+", default=[]
	)
	parser.add_argument(
		"--zero",
		"-0",
		help="Return non zero exit code if an incompatible license is found",
		action="store_true",
	)
	# yapf: enable
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

	# Function to read the config and fall back the the command-line
	conf = lambda option: configparser.get("licensecheck", option) or args[option]

	# File
	filename = stdout if conf("file") is None else open(conf("file"), "w")

	# Get list of licenses
	dependenciesWLicenses = get_deps.getDepsWLicenses(
		conf("using"),
		conf("ignore_packages"),
		conf("fail_packages"),
		conf("ignore_licenses"),
		conf("fail_licenses"),
	)

	# Are any licenses incompatible?
	incompatible = any(not lice["license_compat"] for lice in dependenciesWLicenses)

	# Format the results
	if conf("format") is None:
		print(formatter.simple(dependenciesWLicenses), file=filename)
	elif conf("format") in formatter.formatMap:
		print(formatter.formatMap[conf("format")](dependenciesWLicenses), file=filename)
	else:
		exitCode = 2

	# Exit code of 1 if args.zero
	if conf("zero") and incompatible:
		exitCode = 1

	# Cleanup + exit
	filename.close()
	sysexit(exitCode)
