"""Get a list of packages with package compatibility.
"""
from __future__ import annotations

import subprocess
import warnings
from pathlib import Path

import requirements
import tomli
from requirements.requirement import Requirement

from licensecheck import license_matrix, packageinfo
from licensecheck.types import JOINS, License, PackageInfo

USINGS = ["requirements", "poetry", "PEP631"]


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


def getReqs(using: str) -> set[str]:
	"""Get requirements for the end user project/ lib.

	>>> getReqs("poetry")
	>>> getReqs("poetry:dev")
	>>> getReqs("requirements")
	>>> getReqs("requirements:requirements.txt;requirements-dev.txt")
	>>> getReqs("PEP631")
	>>> getReqs("PEP631:tests")

	Args:
		using (str): use requirements, poetry or PEP631.

	Returns:
		set[str]: set of requirement packages
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
		lines = _doSysExec("poetry show " + ("" if extras else "--only main"))[1].splitlines(False)
		for line in lines:
			try:
				parts = line.split()
				reqs.add(parts[0].lower())
			except IndexError:
				print(
					"An error occurred with poetry, try running 'poetry show' to "
					"see what went wrong! - (fall back to requirements)"
				)
				using = "requirements"  # Poetry died - fall back to requirements
				break

	# PEP631 (hatch)
	if using == "PEP631":
		project = tomli.loads(Path("pyproject.toml").read_text(encoding="utf-8"))["project"]
		reqLists = [project["dependencies"]]
		if extras:
			reqLists.extend(project["optional-dependencies"][x] for x in extras.split(";"))
		for reqList in reqLists:
			for req in reqList:
				reqs.add(str(Requirement.parse(req).name).lower())

	# Requirements
	if using == "requirements":
		for reqTxt in (extras or "requirements.txt").split(";"):
			with open(reqTxt, encoding="utf-8") as requirementsTxt:
				for req in requirements.parse(requirementsTxt):
					reqs.add(str(req.name).lower())
	return reqs


def getDepsWithLicenses(
	using: str,
	ignorePackages: list[str],
	failPackages: list[str],
	ignoreLicenses: list[str],
	failLicenses: list[str],
) -> tuple[License, set[PackageInfo]]:
	"""Get a set of dependencies with licenses and determine license compatibility.

	Args:
		using (str): use requirements or poetry
		ignorePackages (list[str]): a list of packages to ignore (compat=True)
		failPackages (list[str]): a list of packages to fail (compat=False)
		ignoreLicenses (list[str]): a list of licenses to ignore (skipped, compat may still be False)
		failLicenses (list[str]): a list of licenses to fail (compat=False)

	Returns:
		tuple[License, set[PackageInfo]]: tuple of
			my package license
			set of updated dependencies with licenseCompat set
	"""
	reqs = getReqs(using)

	# Get my license
	myLiceTxt = packageinfo.getMyPackageLicense()
	myLice = license_matrix.licenseType(myLiceTxt)[0]

	# Check it is compatible with packages and add a note
	packages = packageinfo.getPackages(reqs)
	for package in packages:
		# Deal with --ignore-packages and --fail-packages
		package.licenseCompat = False
		if package.name.lower() in [x.lower() for x in ignorePackages]:
			package.licenseCompat = True
		elif package.name.lower() in [x.lower() for x in failPackages]:
			pass  # package.licenseCompat = False
		# Old behaviour
		else:
			package.licenseCompat = license_matrix.depCompatWMyLice(  # type: ignore
				myLice,
				license_matrix.licenseType(package.license),
				license_matrix.licenseType(JOINS.join(ignoreLicenses)),
				license_matrix.licenseType(JOINS.join(failLicenses)),
			)
	return myLice, packages
