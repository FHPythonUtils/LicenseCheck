"""Get a list of packages with package compatibility."""

from __future__ import annotations

from fnmatch import fnmatch

from licensecheck import license_matrix
from licensecheck.packageinfo import PackageInfoManager
from licensecheck.types import JOINS, License, PackageInfo, ucstr


def check(
	requirements_paths: list[str],
	groups: list[str],
	extras: list[str],
	this_license: License,
	package_info_manager: PackageInfoManager,
	ignore_packages: list[ucstr] | None = None,
	fail_packages: list[ucstr] | None = None,
	ignore_licenses: list[ucstr] | None = None,
	fail_licenses: list[ucstr] | None = None,
	only_licenses: list[ucstr] | None = None,
	skip_dependencies: list[ucstr] | None = None,
) -> tuple[bool, set[PackageInfo]]:
	# Def values
	ignore_packages = ignore_packages or []
	fail_packages = fail_packages or []
	ignore_licenses = ignore_licenses or []
	fail_licenses = fail_licenses or []
	only_licenses = only_licenses or []
	skip_dependencies = skip_dependencies or []

	package_info_manager.resolve_requirements(
		requirements_paths=requirements_paths,
		groups=groups,
		extras=extras,
		skip_dependencies=skip_dependencies,
	)

	ignoreLicensesType = license_matrix.licenseType(
		ucstr(JOINS.join(ignore_licenses)), ignore_licenses
	)
	failLicensesType = license_matrix.licenseType(ucstr(JOINS.join(fail_licenses)), ignore_licenses)
	onlyLicensesType = license_matrix.licenseType(ucstr(JOINS.join(only_licenses)), ignore_licenses)
	# licenseType will always return NO_LICENSE when onlyLicenses is empty          # noqa: ERA001
	if License.NO_LICENSE in onlyLicensesType:
		onlyLicensesType.remove(License.NO_LICENSE)

	# Check it is compatible with packages and add a note
	packages = package_info_manager.getPackages()
	for package in packages:
		# Deal with --ignore-packages and --fail-packages
		package.licenseCompat = False
		packageName = package.name.upper()
		if any(fnmatch(packageName, pattern) for pattern in ignore_packages):
			package.licenseCompat = True
		elif any(fnmatch(packageName, pattern) for pattern in fail_packages):
			pass  # package.licenseCompat = False
		# Else get compat with myLice
		else:
			package.licenseCompat = license_matrix.depCompatWMyLice(
				this_license,
				license_matrix.licenseType(ucstr(package.license), ignore_licenses),
				ignoreLicensesType,
				failLicensesType,
				onlyLicensesType,
			)

	# Are any licenses incompatible?
	incompatible = any(not package.licenseCompat for package in packages)

	return incompatible, packages
