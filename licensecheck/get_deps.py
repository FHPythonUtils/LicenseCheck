"""Get a list of packages with package compatibility.
"""
from __future__ import annotations

import re
from importlib import metadata
from pathlib import Path
from typing import Any

import tomli
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from licensecheck import license_matrix, packageinfo
from licensecheck.types import JOINS, License, PackageInfo, session, ucstr

USINGS = ["requirements", "poetry", "PEP631"]


def getReqs(using: str, skipDependencies: list(ucstr)) -> set[ucstr]:
	"""Get requirements for the end user project/ lib.

	>>> getReqs("poetry")
	>>> getReqs("poetry:dev")
	>>> getReqs("requirements")
	>>> getReqs("requirements:requirements.txt;requirements-dev.txt")
	>>> getReqs("PEP631")
	>>> getReqs("PEP631:tests")

	Args:
		using (str): use requirements, poetry or PEP631.
		skipDependencies (list[str]): list of dependencies to skip.

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

	return _doGetReqs(using, skipDependencies, extras, pyproject, requirementsPaths)


def _doGetReqs(
	using: str,
	skipDependencies: list(ucstr),
	extras: str | None,
	pyproject: dict[str, Any],
	requirementsPaths: list[Path],
) -> set[ucstr]:
	reqs = set()
	extrasReqs = {}

	def resolveReq(req: str, extra: bool = True) -> ucstr:
		requirement = Requirement(req)
		extras = {ucstr(extra) for extra in requirement.extras}
		name = ucstr(canonicalize_name(requirement.name))
		canonicalName = name
		if len(extras) > 0:
			canonicalName = ucstr(f"{name}[{list(extras)[0]}]")
			# To avoid overwriting the initial mapping in extrasReqs
			# only overwrite when extra = True
			if extra:
				extrasReqs[name] = extras
		return canonicalName if extra else name

	def resolveExtraReq(extraReq: str) -> ucstr | None:
		match = re.search(r"extra\s*==\s*'(.*?)'", extraReq)
		if match is None:
			return None
		return ucstr(match.group(1))

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
		for reqPath in requirementsPaths:
			if not reqPath.exists():
				raise RuntimeError(f"Could not find specification of requirements ({reqPath}).")

			for line in reqPath.read_text(encoding="utf-8").splitlines():
				line = line.strip()
				if not line or line[0] in {"#", "-"}:
					continue
				reqs.add(resolveReq(line))

	# Remove PYTHON if define as requirement
	try:
		reqs.remove("PYTHON")
	except KeyError:
		pass
	# Remove skip dependencies
	for skipDependency in skipDependencies:
		try:
			reqs.remove(skipDependency)
		except KeyError:
			pass

	# Get Dependencies (1 deep)
	requirementsWithDeps = reqs.copy()

	def update_dependencies(dependency: str) -> None:
		dep = resolveReq(dependency, False)
		req = resolveReq(requirement, False)
		extra = resolveExtraReq(dependency)
		if extra is not None:
			if req in extrasReqs and extra in extrasReqs.get(req, []):
				requirementsWithDeps.add(dep)
		else:
			requirementsWithDeps.add(dep)

	for requirement in reqs:
		try:
			pkgMetadata = metadata.metadata(requirement)
			for dependency in pkgMetadata.get_all("Require-Dist") or []:
				update_dependencies(dependency)
		except metadata.PackageNotFoundError:
			request = session.get(
				f"https://pypi.org/pypi/{requirement.split('[')[0]}/json", timeout=60
			)
			response = request.json()
			try:
				for dependency in response["info"]["requires_dist"] or []:
					update_dependencies(dependency)
			except (KeyError, TypeError):
				pass

	return {r.split("[")[0] for r in requirementsWithDeps}


def getDepsWithLicenses(
	using: str,
	ignorePackages: list[ucstr],
	failPackages: list[ucstr],
	ignoreLicenses: list[ucstr],
	failLicenses: list[ucstr],
	skipDependencies: list[ucstr],
) -> tuple[License, set[PackageInfo]]:
	"""Get a set of dependencies with licenses and determine license compatibility.

	Args:
		using (str): use requirements or poetry
		ignorePackages (list[ucstr]): a list of packages to ignore (compat=True)
		failPackages (list[ucstr]): a list of packages to fail (compat=False)
		ignoreLicenses (list[ucstr]): a list of licenses to ignore (skipped, compat may still be False)
		failLicenses (list[ucstr]): a list of licenses to fail (compat=False)
		skipDependencies (list[ucstr]): a list of dependencies to skip (compat=False)

	Returns:
		tuple[License, set[PackageInfo]]: tuple of
			my package license
			set of updated dependencies with licenseCompat set
	"""
	reqs = getReqs(using, skipDependencies)

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
		packageName = package.name.upper()
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
