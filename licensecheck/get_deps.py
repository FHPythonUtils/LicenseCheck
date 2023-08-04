"""Get a list of packages with package compatibility.
"""
from __future__ import annotations

import re
from importlib import metadata
from pathlib import Path
from typing import Any

import pkg_resources
import requirements
import tomli

from licensecheck import license_matrix, packageinfo
from licensecheck.types import JOINS, License, PackageInfo, session, ucstr

USINGS = ["requirements", "poetry", "PEP631"]


def getReqs(using: str) -> set[ucstr]:
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

	pyproject = {}
	requirementsPaths = []

	pyprojectPath = Path("pyproject.toml")
	if pyprojectPath.exists():
		pyproject = tomli.loads(pyprojectPath.read_text(encoding="utf-8"))

	# Requirements
	if using == "requirements":
		requirementsPaths = [Path(x) for x in (extras or "requirements.txt").split(";")]

	return _doGetReqs(using, extras, pyproject, requirementsPaths)


def _doGetReqs(
	using: str, extras: str | None, pyproject: dict[str, Any], requirementsPaths: list[Path]
) -> set[ucstr]:
	resolveReq = lambda req: ucstr(pkg_resources.Requirement.parse(req).project_name)
	resolveExtraReq = lambda extra_req: re.sub("extra == ", "", re.findall(r"extra == '.*?'",extra_req)[0].replace("'", "")) if len(re.findall(r"extra == '.*?'",extra_req)) > 0 else None

	reqs = set()
	extras_reqs = dict()

	if using == "poetry":
		try:
			project = pyproject["tool"]["poetry"]
			reqLists = [project["dependencies"]]
		except KeyError as error:
			raise RuntimeError(
				"Could not find specification of requirements (pyproject.toml)."
			) from error
		if extras is not None:
			reqLists.extend(
				project.get("group", {x: {"dependencies": {}}})[x]["dependencies"]
				for x in extras.split(";")
			)
			reqLists.append(project.get("dev-dependencies", {}))
		for reqList in reqLists:
			for req in reqList:
				try:
					extra = re.search(r'(?<=\[)(.*?)(?=\])',req).group(0)
					extras_reqs[resolveReq(req)] = extra
					reqs.add(f"{resolveReq(req)}[{extra}]")
				except (KeyError, AttributeError):
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
				try:
					extra = re.search(r'(?<=\[)(.*?)(?=\])',req).group(0)
					extras_reqs[resolveReq(req)] = extra
					reqs.add(f"{resolveReq(req)}[{extra}]")
				except (KeyError, AttributeError):
					reqs.add(resolveReq(req))

	# Requirements
	if using == "requirements":
		for reqPath in requirementsPaths:
			if not reqPath.exists():
				raise RuntimeError(f"Could not find specification of requirements ({reqPath}).")

			with open(reqPath, encoding="utf-8") as requirementsTxt:
				for req in requirements.parse(requirementsTxt):
					if len(req.extras)>0:
						extras_reqs[resolveReq(req.name)] = req.extras
						for extra in req.extras:
							reqs.add(f"{resolveReq(req.name)}[{extra}]")
					else:
						reqs.add(resolveReq(req.name))

	try:
		reqs.remove("PYTHON")
	except KeyError:
		pass

	# Get Dependencies (1 deep)
	requirementsWithDeps = reqs.copy()
	for requirement in reqs:
		try:
			pkgMetadata = metadata.metadata(requirement)
			for req in [resolveReq(req) for req in pkgMetadata.get_all("Requires-Dist") or []]:
				requirementsWithDeps.add(req)
		except metadata.PackageNotFoundError:
			request = session.get(f"https://pypi.org/pypi/{requirement.split('[')[0]}/json", timeout=60)
			response = request.json()
			try:
				for dependency in response["info"]["requires_dist"]:
					if resolveExtraReq(dependency) is not None:
						if (resolveReq(requirement) in extras_reqs.keys()) and (resolveExtraReq(dependency) in extras_reqs[resolveReq(requirement)]):
							requirementsWithDeps.add(resolveReq(dependency))
					else:
						requirementsWithDeps.add(resolveReq(dependency))
			except (KeyError, TypeError):
				pass

	return {r.split('[')[0] for r in requirementsWithDeps}

def getDepsWithLicenses(
	using: str,
	ignorePackages: list[ucstr],
	failPackages: list[ucstr],
	ignoreLicenses: list[ucstr],
	failLicenses: list[ucstr],
) -> tuple[License, set[PackageInfo]]:
	"""Get a set of dependencies with licenses and determine license compatibility.

	Args:
		using (str): use requirements or poetry
		ignorePackages (list[ucstr]): a list of packages to ignore (compat=True)
		failPackages (list[ucstr]): a list of packages to fail (compat=False)
		ignoreLicenses (list[ucstr]): a list of licenses to ignore (skipped, compat may still be False)
		failLicenses (list[ucstr]): a list of licenses to fail (compat=False)

	Returns:
		tuple[License, set[PackageInfo]]: tuple of
			my package license
			set of updated dependencies with licenseCompat set
	"""
	reqs = getReqs(using)

	# Get my license
	myLiceTxt = packageinfo.getMyPackageLicense()
	myLice = license_matrix.licenseType(myLiceTxt)[0]
	ignoreLicensesType = license_matrix.licenseType(
		ucstr(JOINS.join(ignoreLicenses)), ignoreLicenses
	)
	failLicensesType = license_matrix.licenseType(ucstr(JOINS.join(failLicenses)), ignoreLicenses)

	# Check it is compatible with packages and add a note
	packages = packageinfo.getPackages(reqs)
	for package in packages:
		# Deal with --ignore-packages and --fail-packages
		package.licenseCompat = False
		packageName = package.name
		if packageName in ignorePackages:
			package.licenseCompat = True
		elif packageName in failPackages:
			pass  # package.licenseCompat = False
		# Old behaviour
		else:
			package.licenseCompat = license_matrix.depCompatWMyLice(  # type: ignore
				myLice,
				license_matrix.licenseType(package.license, ignoreLicenses),
				ignoreLicensesType,
				failLicensesType,
			)
	return myLice, packages
