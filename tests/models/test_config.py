import pytest
import tomli

from licensecheck.io.fmt import FMT
from licensecheck.models.config import LC_Config


def test_no_config() -> None:
	LC_Config.model_validate({})


def test_basic_config() -> None:
	raw_conf = tomli.loads("""

[tool.licensecheck]
license = "mit"               # Specify the project license explicitly
format = "simple"             # Output format (e.g., "json", "csv", etc.)
requirements_paths = []       # List of filenames to read from
groups = []                   # List of selected groups
extras = []                   # List of selected extras
file = ""                     # Output file (leave empty for stdout)
ignore_packages = []          # Packages/dependencies to ignore
license_overrides = { "sample==1.2.3" = "MIT" } # Reviewed exact-version licenses
fail_packages = []            # Packages/dependencies that cause failure
ignore_licenses = []          # Licenses to ignore
allowed_license_references = [] # Exact LicenseRef identifiers to accept
fail_licenses = []            # Licenses that cause failure
only_licenses = []            # Allowed licenses (all others will fail)
skip_dependencies = []        # Dependencies to skip (compatibility = True)
hide_output_parameters = []   # Parameters to hide from output
show_only_failing = false     # Show only incompatible/failing packages
pypi_api = "https://pypi.org" # Custom PyPI API endpoint
zero = false                  # Return non-zero exit code for incompatible licenses (for CI/CD)

""")

	conf = LC_Config.model_validate(raw_conf["tool"]["licensecheck"])
	assert conf.format == FMT.simple
	assert conf.pypi_api == "https://pypi.org"
	assert conf.license_overrides == {"sample==1.2.3": "MIT"}


def test_basic_config2() -> None:
	raw_conf = tomli.loads("""

[tool.licensecheck]
license = "mit"               # Specify the project license explicitly
ignore_packages = []          # Packages/dependencies to ignore
fail_packages = []            # Packages/dependencies that cause failure
ignore_licenses = []          # Licenses to ignore
allowed_license_references = [] # Exact LicenseRef identifiers to accept
fail_licenses = []            # Licenses that cause failure
only_licenses = []            # Allowed licenses (all others will fail)
skip_dependencies = []        # Dependencies to skip (compatibility = True)
hide_output_parameters = []   # Parameters to hide from output
show_only_failing = false     # Show only incompatible/failing packages
zero = false                  # Return non-zero exit code for incompatible licenses (for CI/CD)

""")

	conf = LC_Config.model_validate(raw_conf["tool"]["licensecheck"])
	assert conf.format == FMT.simple
	assert conf.pypi_api == ""


@pytest.mark.parametrize(
	"package",
	[
		"sample",
		"sample>=1.2.3",
		"sample==1.*",
		"sample==1.2.3; python_version > '3.11'",
	],
)
def test_license_overrides_require_exact_versions(package: str) -> None:
	with pytest.raises(ValueError, match="exact name==version"):
		LC_Config.model_validate({"license_overrides": {package: "MIT"}})


def test_license_overrides_require_nonempty_licenses() -> None:
	with pytest.raises(ValueError, match="must not be empty"):
		LC_Config.model_validate({"license_overrides": {"sample==1.2.3": " "}})
