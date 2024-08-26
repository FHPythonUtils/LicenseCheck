"""Get a list of packages with package compatibility."""

from __future__ import annotations

from pathlib import Path

import tomli

from licensecheck import license_matrix, packageinfo
from licensecheck.resolvers import native as res_native
from licensecheck.resolvers import uv as res_uv
from licensecheck.types import JOINS, License, PackageInfo, ucstr

USINGS = ["requirements", "poetry", "PEP631"]


def getReqs(using: str, skipDependencies: list[ucstr]) -> set[ucstr]:
	"""Get requirements for the end user project/ lib.

	>>> getReqs("poetry")
	>>> getReqs("poetry:dev")
	>>> getReqs("requirements")
	>>> getReqs("requirements:requirements.txt;requirements-dev.txt")
	>>> getReqs("PEP631")
	>>> getReqs("PEP631:tests")

	Args:
	----
		using (str): use requirements, poetry or PEP631.
		skipDependencies (list[str]): list of dependencies to skip.

	Returns:
	-------
		set[str]: set of requirement packages

	"""

	_ = using.split(":", 1)
	using = _[0]
	extras = _[1].split(";") if len(_) > 1 else []
	if using not in USINGS:
		using = "poetry"

	# if using poetry or pep621
	requirementsPaths = ["pyproject.toml"]

	# Requirements
	if using == "requirements":
		requirementsPaths = ["requirements.txt"] if len(extras) > 0 else extras
		extras = []

	try:
		return res_uv.get_reqs(
			using=using,
			skipDependencies=skipDependencies,
			extras=extras,
			requirementsPaths=requirementsPaths,
		)

	except RuntimeError:
		pyproject = {}
		if "pyproject.toml" in requirementsPaths:
			pyproject = tomli.loads(Path("pyproject.toml").read_text("utf-8"))

		# Fallback to the old resolver (hopefully we can deprecate this asap!)
		return res_native.get_reqs(
			using=using,
			skipDependencies=skipDependencies,
			extras=extras,
			pyproject=pyproject,
			requirementsPaths=[Path(x) for x in requirementsPaths],
		)


def getDepsWithLicenses(
	using: str,
	myLice: License,
	ignorePackages: list[ucstr],
	failPackages: list[ucstr],
	ignoreLicenses: list[ucstr],
	failLicenses: list[ucstr],
	onlyLicenses: list[ucstr],
	skipDependencies: list[ucstr],
) -> set[PackageInfo]:
	"""Get a set of dependencies with licenses and determine license compatibility.

	Args:
	----
		using (str): use requirements or poetry
		myLice (License): user license
		ignorePackages (list[ucstr]): a list of packages to ignore (compat=True)
		failPackages (list[ucstr]): a list of packages to fail (compat=False)
		ignoreLicenses (list[ucstr]): a list of licenses to ignore (skipped, compat may still be
		False)
		failLicenses (list[ucstr]): a list of licenses to fail (compat=False)
		onlyLicenses (list[ucstr]): a list of allowed licenses (any other license will fail)
		skipDependencies (list[ucstr]): a list of dependencies to skip (compat=False)

	Returns:
	-------
		tuple[License, set[PackageInfo]]: tuple of
			my package license
			set of updated dependencies with licenseCompat set

	"""
	reqs = getReqs(using, skipDependencies)

	ignoreLicensesType = license_matrix.licenseType(
		ucstr(JOINS.join(ignoreLicenses)), ignoreLicenses
	)
	failLicensesType = license_matrix.licenseType(ucstr(JOINS.join(failLicenses)), ignoreLicenses)
	onlyLicensesType = license_matrix.licenseType(ucstr(JOINS.join(onlyLicenses)), ignoreLicenses)
	# licenseType will always return NO_LICENSE when onlyLicenses is empty          # noqa: ERA001
	if License.NO_LICENSE in onlyLicensesType:
		onlyLicensesType.remove(License.NO_LICENSE)

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
		# Else get compat with myLice
		else:
			package.licenseCompat = license_matrix.depCompatWMyLice(
				myLice,
				license_matrix.licenseType(package.license, ignoreLicenses),
				ignoreLicensesType,
				failLicensesType,
				onlyLicensesType,
			)
	return packages
