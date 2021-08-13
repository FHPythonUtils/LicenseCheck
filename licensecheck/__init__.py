"""Output the licenses used by dependencies and check if these are compatible with the project license.
"""
from __future__ import annotations

import argparse
from sys import exit as sysexit, stdout

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
		"--zero",
		"-0",
		help="Return non zero exit code if an incompatible license is found",
		action="store_true",
	)
	# yapf: enable
	args = parser.parse_args()
	# File
	filename = stdout if args.file is None else open(args.file, "w")

	# Get list of licenses
	dependenciesWLicenses = get_deps.getDepsWLicenses(args.using)

	# Are any licenses incompatible?
	incompatible = any(not lice["license_compat"] for lice in dependenciesWLicenses)

	# Format the results
	if args.format is None:
		print(formatter.simple(dependenciesWLicenses), file=filename)
	elif args.format in formatter.formatMap:
		print(formatter.formatMap[args.format](dependenciesWLicenses), file=filename)
	else:
		exitCode = 2

	# Exit code of 1 if args.zero
	if args.zero and incompatible:
		exitCode = 1

	# Cleanup + exit
	filename.close()
	sysexit(exitCode)
