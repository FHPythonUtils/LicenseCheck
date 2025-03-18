from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from licensecheck.checker import check
from licensecheck.packageinfo import PackageInfoManager
from licensecheck.types import License, PackageInfo, ucstr


@pytest.fixture
def mock_package_info_manager() -> PackageInfoManager:
	"""Fixture to provide a mocked PackageInfoManager."""
	return MagicMock(spec=PackageInfoManager)


@pytest.mark.parametrize(
	("ignore_packages", "fail_packages", "fail_licenses", "expected_incompatible"),
	[
		(None, None, None, False),  # No fail conditions, should pass
		(["PACKAGE_B"], None, None, False),  # Ignored package should not cause failure
		(["PACKAGE*"], None, None, False),  # Globs are supported in ignore_packages
		(None, ["PACKAGE_A"], None, True),  # PACKAGE_A in fail_packages should fail
		(None, ["PACKAGE*"], None, True),  # Globs are supported in fail_packages
		(None, None, ["GPL-3.0"], True),  # GPL-3.0 should be marked as incompatible
		(None, None, ["GPL*"], False),  # Globs are not supported on licenses!
	],
)
def test_check(
	mock_package_info_manager: PackageInfoManager,
	ignore_packages: list | None,
	fail_packages: list | None,
	fail_licenses: list | None,
	expected_incompatible: bool,
) -> None:
	"""Parametrized test for different license check scenarios."""
	mock_packages = {
		PackageInfo(name="PACKAGE_A", license=ucstr("MIT"), licenseCompat=True),
		PackageInfo(name="PACKAGE_B", license=ucstr("GPL-3.0"), licenseCompat=False),
	}
	mock_package_info_manager.getPackages.return_value = mock_packages
	mock_package_info_manager.pypi_search = "https://pypi.org/simple"

	incompatible, packages = check(
		requirements_paths=["requirements.txt"],
		groups=[],
		extras=[],
		this_license=License.GPL_3_PLUS,
		package_info_manager=mock_package_info_manager,
		ignore_packages=ignore_packages,
		fail_packages=fail_packages,
		fail_licenses=fail_licenses,
	)

	assert incompatible == expected_incompatible, packages
