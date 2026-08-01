"""Get a set of packages with package compatibility."""

from __future__ import annotations

from fnmatch import fnmatch

from loguru import logger
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.utils import canonicalize_name

from licensecheck import license_matrix
from licensecheck.models.constants import JOINS
from licensecheck.models.license import License
from licensecheck.models.packageinfo import PackageInfo
from licensecheck.packageinforesolver import PackageInfoManager


def _package_matches(package: PackageInfo, patterns: set[str]) -> bool:
	package_names = {package.name.upper()}
	if package.version:
		package_names.add(f"{package.name}=={package.version}".upper())
	return any(
		fnmatch(package_name, pattern.upper())
		for package_name in package_names
		for pattern in patterns
	)


def _matches_allowed_license_reference(
	allowed_license_references: set[str], dependency_license: str
) -> bool:
	dependency_license = dependency_license.strip().casefold()
	return dependency_license.startswith("licenseref-") and dependency_license in {
		license_ref.strip().casefold() for license_ref in allowed_license_references
	}


def _parse_license_overrides(
	license_overrides: dict[str, str],
) -> list[tuple[str, SpecifierSet, str]]:
	"""Parse the configured overrides once, rather than once per package."""
	parsed: list[tuple[str, SpecifierSet, str]] = []
	for package_requirement, license_value in license_overrides.items():
		requirement = Requirement(package_requirement)
		if not requirement.specifier:
			# An unversioned override would silently apply to every version of the package.
			logger.warning(
				f"Ignoring license override '{package_requirement}': "
				f"an exact name==version is required"
			)
			continue
		parsed.append(
			(canonicalize_name(requirement.name), requirement.specifier, license_value.strip())
		)
	return parsed


def _license_override(
	package: PackageInfo, license_overrides: list[tuple[str, SpecifierSet, str]]
) -> str | None:
	if package.version is None:
		return None
	package_name = canonicalize_name(package.name)
	for name, specifier, license_value in license_overrides:
		if name == package_name and specifier.contains(package.version, prereleases=True):
			return license_value
	return None


def check(
	requirements_paths: set[str],
	groups: set[str],
	extras: set[str],
	this_license: License,
	package_info_manager: PackageInfoManager,
	*,
	this_license_text: str | None = None,
	ignore_packages: set[str] | None = None,
	license_overrides: dict[str, str] | None = None,
	fail_packages: set[str] | None = None,
	ignore_licenses: set[str] | None = None,
	allowed_license_references: set[str] | None = None,
	fail_licenses: set[str] | None = None,
	only_licenses: set[str] | None = None,
	skip_dependencies: set[str] | None = None,
) -> tuple[bool, set[PackageInfo]]:
	# Def values
	ignore_packages = ignore_packages or set()
	parsed_license_overrides = _parse_license_overrides(license_overrides or {})
	fail_packages = fail_packages or set()
	ignore_licenses = ignore_licenses or set()
	# The project's own license reference is always an accepted reference
	allowed_license_references = (allowed_license_references or set()) | (
		{this_license_text} if this_license_text else set()
	)
	fail_licenses = fail_licenses or set()
	only_licenses = only_licenses or set()
	skip_dependencies = skip_dependencies or set()

	package_info_manager.resolve_requirements(
		requirements_paths=requirements_paths,
		groups=groups,
		extras=extras,
		skip_dependencies=skip_dependencies,
	)

	ignoreLicensesType = license_matrix.licenseType(
		str(JOINS.join(ignore_licenses)), ignore_licenses
	)
	failLicensesType = license_matrix.licenseType(str(JOINS.join(fail_licenses)), ignore_licenses)
	onlyLicensesType = license_matrix.licenseType(str(JOINS.join(only_licenses)), ignore_licenses)
	# licenseType will always return NO_LICENSE when onlyLicenses is empty
	if License.NO_LICENSE in onlyLicensesType:
		onlyLicensesType.remove(License.NO_LICENSE)

	# Check it is compatible with packages and add a note
	packages = package_info_manager.getPackages()
	for package in packages:
		if override := _license_override(package, parsed_license_overrides):
			package.license = override
			package.licenseSource = "configured override"
		# Deal with --ignore-packages and --fail-packages
		package.licenseCompat = False
		if _package_matches(package, ignore_packages):
			package.licenseCompat = True
		elif _package_matches(package, fail_packages):
			pass  # package.licenseCompat = False
		elif license_matrix.licenseType(str(package.license), ignore_licenses) & failLicensesType:
			pass
		elif _matches_allowed_license_reference(allowed_license_references, str(package.license)):
			package.licenseCompat = True
		# Else get compat with myLice
		else:
			package.licenseCompat = license_matrix.depCompatWMyLice(
				this_license,
				license_matrix.licenseType(str(package.license), ignore_licenses),
				ignoreLicensesType,
				failLicensesType,
				onlyLicensesType,
			)

	# Are any licenses incompatible?
	incompatible = any(not package.licenseCompat for package in packages)

	return incompatible, packages
