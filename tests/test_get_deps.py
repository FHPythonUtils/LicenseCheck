from pathlib import Path

import tomli

from licensecheck import get_deps, types

THISDIR = Path(__file__).resolve().parent


def test_doGetReqs_PEP631() -> None:
	using = "PEP631"
	extras = ["socks"]
	pyproject = tomli.loads((THISDIR / "data/pep631_socks.toml").read_text(encoding="utf-8"))
	requirementsPaths = []
	skipDependencies = [types.ucstr("TOSKIP")]

	assert get_deps.do_get_reqs(using, skipDependencies, extras, pyproject, requirementsPaths) == {
		"DOCKERPTY",
		"PACKAGING",
		"ATTRS",
		"JSONSCHEMA",
		"PYYAML",
		"PYSOCKS",
		"CERTIFI",
		"ENUM34",
		"DOCKER",
		"TEXTTABLE",
		"PYWIN32",
		"JSONSCHEMA-SPECIFICATIONS",
		"IPADDRESS",
		"PKGUTIL-RESOLVE-NAME",
		"DOCOPT",
		"BACKPORTS-SSL-MATCH-HOSTNAME",
		"PARAMIKO",
		"IDNA",
		"COLORAMA",
		"IMPORTLIB-RESOURCES",
		"CACHED-PROPERTY",
		"DISTRO",
		"BACKPORTS-SHUTIL-GET-TERMINAL-SIZE",
		"CHARSET-NORMALIZER",
		"URLLIB3",
		"WEBSOCKET-CLIENT",
		"RPDS-PY",
		"SUBPROCESS32",
		"REQUESTS",
		"REFERENCING",
		"PYTHON-DOTENV",
	}


def test_doGetReqs_requirements() -> None:
	using = "requirements"
	extras = [f"{THISDIR}/data/test_requirements.txt"]
	pyproject = {}
	requirementsPaths = [Path(f"{THISDIR}/data/test_requirements.txt")]
	skipDependencies = [types.ucstr("TOSKIP")]

	deps = get_deps.do_get_reqs(using, skipDependencies, extras, pyproject, requirementsPaths)
	assert deps == {
		"NUMPY",
		"ODFPY",
		"OPENPYXL",
		"PANDAS",
		"PYTHON-CALAMINE",
		"PYTHON-DATEUTIL",
		"PYTZ",
		"PYXLSB",
		"TZDATA",
		"XLRD",
		"XLSXWRITER",
	}
	assert "OPENPYXL" in deps
	assert (
		"XARRAY" not in deps
	)  # xarray is an optional dependency of pandas associated with 'computation' key that is not
	# tracked in test_requirements.txt

def test_doGetReqs_requirements_with_hashes() -> None:
	using = "requirements"
	extras = []
	pyproject = {}
	requirementsPaths = [Path(f"{THISDIR}/data/test_requirements_hash.txt")]
	skipDependencies = [types.ucstr("TOSKIP")]

	deps = get_deps.do_get_reqs(using, skipDependencies, extras, pyproject, requirementsPaths)
	assert deps == {
		"PACKAGING"
	}
	assert (
		"TOSKIP" not in deps
	)
