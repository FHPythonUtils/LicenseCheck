"""Get a set of packages with package compatibility."""

from __future__ import annotations

from fnmatch import fnmatch

from licensecheck import license_matrix
from licensecheck.models.constants import JOINS
from licensecheck.models.license import License
from licensecheck.models.packageinfo import PackageInfo
from licensecheck.packageinfo import PackageInfoManager


def check(
	requirements_paths: set[str],
	groups: set[str],
	extras: set[str],
	this_license: License,
	package_info_manager: PackageInfoManager,
	ignore_packages: set[str] | None = None,
	fail_packages: set[str] | None = None,
	ignore_licenses: set[str] | None = None,
	fail_licenses: set[str] | None = None,
	only_licenses: set[str] | None = None,
	skip_dependencies: set[str] | None = None,
) -> tuple[bool, set[PackageInfo]]:
	# Def values
	ignore_packages = ignore_packages or set()
	fail_packages = fail_packages or set()
	ignore_licenses = ignore_licenses or set()
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
		# Deal with --ignore-packages and --fail-packages
		package.licenseCompat = False
		packageName = package.name.upper()
		if any(fnmatch(packageName, pattern.upper()) for pattern in ignore_packages):
			package.licenseCompat = True
		elif any(fnmatch(packageName, pattern.upper()) for pattern in fail_packages):
			pass  # package.licenseCompat = False
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
