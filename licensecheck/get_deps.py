"""Get a list of packages with package compatibility.
"""
from __future__ import annotations

import subprocess
import warnings

import requirements

from licensecheck import license_matrix, packageinfo
from licensecheck.types import PackageCompat

USINGS = ["requirements", "poetry"]


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


def getReqs(using: str) -> list[str]:
	"""Get requirements for the end user project/ lib.

	Args:
		using (str): use requirements or poetry

	Returns:
		list[str]: list of requirement packages
	"""
	_ = using.split(":", 1)
	using, extras = _[0], _[1] if len(_) > 1 else None
	if using not in USINGS:
		using = "poetry"
	reqs = set()

	# Is poetry installed?
	if using == "poetry" and _doSysExec("poetry -h")[0] != 0:
		using = "requirements"  # Poetry not installed - fall back to requirements
		warnings.warn(RuntimeWarning("poetry is not on the system path"))

	# Poetry
	if using == "poetry":  # Use poetry show to get dependents of dependencies
		lines = _doSysExec("poetry show " + ("" if extras else "--no-dev"))[1].splitlines(False)
		for line in lines:
			try:
				parts = line.split()
				reqs.add(parts[0])
			except IndexError:
				print(
					"An error occurred with poetry, try running 'poetry show' to "
					"see what went wrong! - (fall back to requirements)"
				)
				using = "requirements"  # Poetry died - fall back to requirements
				break

	# Requirements
	if using == "requirements":
		for reqTxt in (extras or "requirements.txt").split(";"):
			with open(reqTxt, "r", encoding="utf-8") as requirementsTxt:
				for req in requirements.parse(requirementsTxt):
					reqs.add(req.name)
	return list(reqs)


def getDepsWLicenses(
	using: str,
	ignorePackages: list[str],
	failPackages: list[str],
	ignoreLicenses: list[str],
	failLicenses: list[str],
) -> list[PackageCompat]:
	"""Get a list of dependencies with licenses and determin license compatibility.

	Args:
		using (str): use requirements or poetry
		ignorePackages (list[str]): a list of packages to ignore (compat=True)
		failPackages (list[str]): a list of packages to fail (compat=False)
		ignoreLicenses (list[str]): a list of licenses to ignore (skipped, compat may still be False)
		failLicenses (list[str]): a list of licenses to fail (compat=False)

	Returns:
		list[PackageCompat]: list of packagecompat types: dependency info + licence compat
	"""
	reqs = getReqs(using)

	# Get my license
	myLiceTxt = packageinfo.getMyPackageLicense()
	myLice = license_matrix.licenseType(myLiceTxt)[0]

	# Check it is compatible with packages and add a note
	dependenciesWLicenses = []
	for package in packageinfo.getPackages(reqs):
		# Deal with --ignore-packages and --fail-packages
		licenseCompat = False
		if package["name"].lower() in [x.lower() for x in ignorePackages]:
			licenseCompat = True
		elif package["name"].lower() in [x.lower() for x in failPackages]:
			pass  # licenseCompat=False
		# Old behaviour
		else:
			licenseCompat = license_matrix.depCompatWMyLice(
				myLice,
				license_matrix.licenseType(package["license"]),
				license_matrix.licenseType(", ".join(ignoreLicenses)),
				license_matrix.licenseType(", ".join(failLicenses)),
			)
		# Add to list of dependenciesWLicenses
		dependenciesWLicenses.append(PackageCompat(**package, license_compat=licenseCompat))
	return dependenciesWLicenses
