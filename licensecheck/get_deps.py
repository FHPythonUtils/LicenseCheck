"""Get a list of packages with package compatibility.
"""
from __future__ import annotations

import subprocess
import warnings

import requirements

from licensecheck import license_matrix, packageinfo
from licensecheck.types import PackageCompat

usings = ["requirements", "poetry"]


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


def getDepsWLicenses(using: str) -> list[PackageCompat]:
	"""Get a list of packages with package compatibility.

	Returns:
		list[PackageCompat]: list of packages (python dicts)
	"""
	if using not in usings:
		using = "poetry"
	reqs = []

	# Is poetry installed?
	if using == "poetry" and _doSysExec("poetry -h")[0] != 0:
		using = "requirements"  # Poetry not installed - fall back to requirements
		warnings.warn(RuntimeWarning("poetry is not on the system path"))

	# Poetry
	if using == "poetry":  # Use poetry show to get dependents of dependencies
		lines = _doSysExec("poetry show")[1].splitlines(False)
		for line in lines:
			try:
				parts = line.split()
				reqs.append(parts[0])
			except IndexError:
				print(
					"An error occurred with poetry, try running 'poetry show' to "
					"see what went wrong! - (fall back to requirements)"
				)
				using = "requirements"  # Poetry died - fall back to requirements
				break

	# Requirements
	if using == "requirements":
		with open("requirements.txt", "r") as requirementsTxt:
			for req in requirements.parse(requirementsTxt):
				reqs.append(req.name)

	# Get my license
	myLiceTxt = packageinfo.getMyPackageLicense()
	myLice = license_matrix.licenseType(myLiceTxt)[0]

	# Check it is compatible with packages and add a note
	dependenciesWLicenses = []
	for package in packageinfo.getPackages(reqs):
		depLice = license_matrix.licenseType(package["license"])
		dependenciesWLicenses.append(
			PackageCompat(
				**package, license_compat=license_matrix.depCompatWMyLice(myLice, depLice)
			)
		)
	return dependenciesWLicenses
