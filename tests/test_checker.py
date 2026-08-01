from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from licensecheck.checker import check
from licensecheck.models.license import License
from licensecheck.models.packageinfo import PackageInfo
from licensecheck.packageinforesolver import PackageInfoManager


@pytest.fixture
def mock_package_info_manager() -> PackageInfoManager:
	"""Fixture to provide a mocked PackageInfoManager."""
	return MagicMock(spec=PackageInfoManager)


@pytest.mark.parametrize(
	("ignore_packages", "fail_packages", "fail_licenses", "expected_incompatible"),
	[
		(None, None, None, False),  # No fail conditions, should pass
		({"PACKAGE_B"}, None, None, False),  # Ignored package should not cause failure
		({"PACKAGE*"}, None, None, False),  # Globs are supported in ignore_packages
		(None, {"PACKAGE_A"}, None, True),  # PACKAGE_A in fail_packages should fail
		(None, {"PACKAGE*"}, None, True),  # Globs are supported in fail_packages
		(None, None, {"GPL-3.0"}, True),  # GPL-3.0 should be marked as incompatible
		(None, None, {"GPL*"}, False),  # Globs are not supported on licenses!
		({"package_b"}, None, None, False),  # Ignored package should not cause failure
		({"package*"}, None, None, False),  # Globs are supported in ignore_packages
		(None, {"package_a"}, None, True),  # PACKAGE_A in fail_packages should fail
		(None, {"package*"}, None, True),  # Globs are supported in fail_packages
		(None, None, {"gpl-3.0"}, True),  # GPL-3.0 should be marked as incompatible
		(None, None, {"gpl*"}, False),  # Globs are not supported on licenses!
	],
)
def test_check(
	mock_package_info_manager: PackageInfoManager,
	ignore_packages: set[str] | None,
	fail_packages: set[str] | None,
	fail_licenses: set[str] | None,
	*,
	expected_incompatible: bool,
) -> None:
	"""Parametrized test for different license check scenarios."""
	mock_packages = {
		PackageInfo(name="PACKAGE_A", license="MIT", licenseCompat=True),
		PackageInfo(name="PACKAGE_B", license="GPL-3.0", licenseCompat=False),
	}
	mock_package_info_manager.getPackages.return_value = mock_packages
	mock_package_info_manager.base_pypi_url = "https://pypi.org"

	incompatible, packages = check(
		requirements_paths={"requirements.txt"},
		groups=set(),
		extras=set(),
		this_license=License.GPL_3_PLUS,
		package_info_manager=mock_package_info_manager,
		ignore_packages=ignore_packages,
		fail_packages=fail_packages,
		fail_licenses=fail_licenses,
	)

	assert incompatible == expected_incompatible, packages


@pytest.mark.parametrize(
	("ignore_packages", "expected_incompatible"),
	[
		({"private-package==1.2.3"}, False),
		({"private-package==1.2.4"}, True),
		({"private-package==1.*"}, False),
	],
)
def test_ignore_packages_can_match_versions(
	mock_package_info_manager: PackageInfoManager,
	ignore_packages: set[str],
	*,
	expected_incompatible: bool,
) -> None:
	mock_package_info_manager.getPackages.return_value = {
		PackageInfo(
			name="private-package",
			version="1.2.3",
			license="PROPRIETARY",
		)
	}

	incompatible, packages = check(
		requirements_paths={"requirements.txt"},
		groups=set(),
		extras=set(),
		this_license=License.MIT,
		package_info_manager=mock_package_info_manager,
		ignore_packages=ignore_packages,
	)

	assert incompatible == expected_incompatible, packages


@pytest.mark.parametrize(
	("dependency_license", "expected_incompatible"),
	[
		("LicenseRef-CVector-Proprietary", False),
		("licenseref-cvector-proprietary", False),
		("LicenseRef-Other-Proprietary", True),
		("PROPRIETARY", True),
	],
)
def test_matching_custom_license_reference_is_compatible(
	mock_package_info_manager: PackageInfoManager,
	dependency_license: str,
	*,
	expected_incompatible: bool,
) -> None:
	mock_package_info_manager.getPackages.return_value = {
		PackageInfo(name="private-package", version="1.2.3", license=dependency_license)
	}

	incompatible, packages = check(
		requirements_paths={"requirements.txt"},
		groups=set(),
		extras=set(),
		this_license=License.PROPRIETARY,
		this_license_text="LicenseRef-CVector-Proprietary",
		package_info_manager=mock_package_info_manager,
	)

	assert incompatible == expected_incompatible, packages


@pytest.mark.parametrize(
	(
		"dependency_license",
		"allowed_license_references",
		"fail_licenses",
		"expected_incompatible",
	),
	[
		(
			"LicenseRef-NVIDIA-Proprietary",
			{"LicenseRef-NVIDIA-Proprietary"},
			None,
			False,
		),
		(
			"licenseref-nvidia-proprietary",
			{"LicenseRef-NVIDIA-Proprietary"},
			None,
			False,
		),
		(
			"LicenseRef-Other-Proprietary",
			{"LicenseRef-NVIDIA-Proprietary"},
			None,
			True,
		),
		("PROPRIETARY", {"PROPRIETARY"}, None, True),
		(
			"LicenseRef-NVIDIA-Proprietary",
			{"LicenseRef-NVIDIA-Proprietary"},
			{"PROPRIETARY"},
			True,
		),
	],
)
def test_allowed_license_references_match_exact_raw_references(
	mock_package_info_manager: PackageInfoManager,
	dependency_license: str,
	allowed_license_references: set[str],
	fail_licenses: set[str] | None,
	*,
	expected_incompatible: bool,
) -> None:
	mock_package_info_manager.getPackages.return_value = {
		PackageInfo(name="private-package", version="1.2.3", license=dependency_license)
	}

	incompatible, packages = check(
		requirements_paths={"requirements.txt"},
		groups=set(),
		extras=set(),
		this_license=License.PROPRIETARY,
		package_info_manager=mock_package_info_manager,
		allowed_license_references=allowed_license_references,
		fail_licenses=fail_licenses,
	)

	assert incompatible == expected_incompatible, packages


@pytest.mark.parametrize(
	("override_package", "expected_incompatible", "expected_license_source"),
	[
		("private-package==1.2.3", False, "configured override"),
		("PRIVATE_package==1.2.3", False, "configured override"),
		("private-package==1.2.4", True, None),
	],
)
def test_license_overrides_apply_only_to_exact_versions(
	mock_package_info_manager: PackageInfoManager,
	override_package: str,
	*,
	expected_incompatible: bool,
	expected_license_source: str | None,
) -> None:
	mock_package_info_manager.getPackages.return_value = {
		PackageInfo(
			name="private-package",
			version="1.2.3",
			license="Other/Proprietary License",
		)
	}

	incompatible, packages = check(
		requirements_paths={"requirements.txt"},
		groups=set(),
		extras=set(),
		this_license=License.MIT,
		package_info_manager=mock_package_info_manager,
		license_overrides={override_package: "BSD-3-Clause"},
	)
	package = packages.pop()

	assert incompatible == expected_incompatible
	assert package.license == (
		"BSD-3-Clause" if expected_license_source else "Other/Proprietary License"
	)
	assert package.licenseSource == expected_license_source


def test_license_overrides_still_obey_license_deny_rules(
	mock_package_info_manager: PackageInfoManager,
) -> None:
	mock_package_info_manager.getPackages.return_value = {
		PackageInfo(name="private-package", version="1.2.3", license="MIT")
	}

	incompatible, packages = check(
		requirements_paths={"requirements.txt"},
		groups=set(),
		extras=set(),
		this_license=License.MIT,
		package_info_manager=mock_package_info_manager,
		license_overrides={"private-package==1.2.3": "GPL-3.0"},
		fail_licenses={"GPL-3.0"},
	)

	assert incompatible, packages
