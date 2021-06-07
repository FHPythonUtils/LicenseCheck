"""Output the licenses used by dependencies and check if these are compatible...

with the project license
"""
from __future__ import annotations

import argparse
import subprocess
import warnings
from sys import exit as sysexit, stdout

import requirements

from licensecheck import formatter, license_matrix, packageinfo
from licensecheck.packagecompat import PackageCompat

stdout.reconfigure(encoding="utf-8")


def _doSysExec(command: str) -> tuple[int, str]:
	"""Execute a command and check for errors.

	Args:
		command (str): commands as a string

	Raises:
		RuntimeWarning: throw a warning should there be a non exit code

	Returns:
		tuple[int, str]: exit code and message
	"""
	with subprocess.Popen(
		command,
		shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,
		encoding="utf-8",
		errors="ignore",
	) as process:
		out = process.communicate()[0]
		exitCode = process.returncode
	return exitCode, out


def getDepsLicenses() -> list[PackageCompat]:
	"""Get a list of packages with package compatibility.

	Returns:
		list[PackageCompat]: list of packages (python dicts)
	"""
	# Is poetry installed?
	poetryInstalled = True
	if _doSysExec("poetry -h")[0] != 0:
		poetryInstalled = False
		warnings.warn(RuntimeWarning("poetry is not on the system path"))
	# Get list of requirements
	reqs = []
	if poetryInstalled:
		# Use poetry show to get dependents of dependencies
		lines = _doSysExec("poetry show")[1].splitlines(False)
		for line in lines:
			try:
				parts = line.split()
				reqs.append(parts[0])
			except IndexError:
				print(
					"An error occurred with poetry try running "
					"'poetry show' to see what went wrong!"
				)
				poetryInstalled = False  # Some error occurred so fallback to requirements.txt
				break
	if not poetryInstalled:
		with open("requirements.txt", "r") as requirementsTxt:
			for req in requirements.parse(requirementsTxt):  # type: ignore
				reqs.append(req.name)  # type: ignore
	# Get my license
	myLiceTxt = packageinfo.getMyPackageLicense()
	myLice = license_matrix.licenseType(myLiceTxt)[0]
	# Check it is compatible with packages and add a note
	depsLicenses = []
	for package in packageinfo.getPackages(reqs):
		depLice = license_matrix.licenseType(package["license"])
		depsLicenses.append(
			PackageCompat(
				**package, license_compat=license_matrix.depCompatibleLice(myLice, depLice)
			)
		)
	return depsLicenses


FORMAT_HELP = "Output format. One of simple, ansi, json, markdown, csv. default=simple"


def cli() -> None:
	"""Cli entry point."""

	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--format", "-f", help=FORMAT_HELP)
	parser.add_argument("--file", "-o", help="Filename to write to (omit for stdout)")
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
	# Format
	formatMap = {
		"json": formatter.json,
		"markdown": formatter.markdown,
		"csv": formatter.csv,
		"ansi": formatter.ansi,
		"simple": formatter.simple,
	}
	if args.format is not None and args.format not in formatMap:
		print(FORMAT_HELP)
		sysexit(2)
	licenses = getDepsLicenses()
	incompatible = any(not lice["license_compat"] for lice in licenses)
	if args.format is None:
		print(formatter.simple(licenses), file=filename)
	elif args.format in formatMap:
		print(formatMap[args.format](licenses), file=filename)
	if incompatible and args.zero:
		sysexit(1)
	sysexit(0)
