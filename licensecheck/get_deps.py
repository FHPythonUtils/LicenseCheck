"""Get a list of packages with package compatibility.
"""
from __future__ import annotations

from importlib import metadata
from pathlib import Path

import requirements
import pkg_resources
import requests
import tomli

from licensecheck import license_matrix, packageinfo
from licensecheck.types import JOINS, License, PackageInfo

USINGS = ["requirements", "poetry", "PEP631"]


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

	resolveReq = lambda req: pkg_resources.Requirement.parse(req).project_name.lower()

	_ = using.split(":", 1)
	using, extras = _[0], _[1] if len(_) > 1 else None
	if using not in USINGS:
		using = "poetry"
	reqs = set()

	pyprojectPath = Path("pyproject.toml")
	pyproject = {}
	if pyprojectPath.exists():
		pyproject = tomli.loads(pyprojectPath.read_text(encoding="utf-8"))

	if using == "poetry":
		try:
			project = pyproject["tool"]["poetry"]
			reqLists = [project["dependencies"]]
		except KeyError as error:
			raise RuntimeError(
				"Could not find specification of requirements (pyproject.toml)."
			) from error
		if extras:
			reqLists.extend(
				project.get("group", {x: {"dependencies": {}}})[x]["dependencies"]
				for x in extras.split(";")
			)
			reqLists.append(project.get("dev-dependencies", {}))
		for reqList in reqLists:
			for req in reqList:
				reqs.add(resolveReq(req))

	# PEP631 (hatch)
	if using == "PEP631":
		try:
			project = pyproject["project"]
			reqLists = [project["dependencies"]]
		except KeyError as error:
			raise RuntimeError(
				"Could not find specification of requirements (pyproject.toml)."
			) from error
		if extras:
			reqLists.extend(project["optional-dependencies"][x] for x in extras.split(";"))
		for reqList in reqLists:
			for req in reqList:
				reqs.add(resolveReq(req))

	# Requirements
	if using == "requirements":
		for reqTxt in (extras or "requirements.txt").split(";"):

			reqPath = Path(reqTxt)
			if not reqPath.exists():
				raise RuntimeError(f"Could not find specification of requirements ({reqPath}).")

			with open(reqPath, encoding="utf-8") as requirementsTxt:
				for req in requirements.parse(requirementsTxt):
					reqs.add(str(req.name).lower())

	try:
		reqs.remove("python")
	except KeyError:
		pass

	# Get Dependencies (1 deep)
	requirementsWithDeps = reqs.copy()
	for requirement in reqs:
		try:
			pkgMetadata = metadata.metadata(resolveReq(requirement))
			for req in [resolveReq(req) for req in pkgMetadata.get_all("Requires-Dist") or []]:
				requirementsWithDeps.add(req)
		except metadata.PackageNotFoundError:
			request = requests.get(f"https://pypi.org/pypi/{requirement}/json", timeout=60)
			response = request.json()
			try:
				for req in [resolveReq(req) for req in response["info"]["requires_dist"]]:
					requirementsWithDeps.add(req)
			except KeyError:
				pass

	return requirementsWithDeps


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
