from pathlib import Path

import tomli

from licensecheck import get_deps

THISDIR = Path(__file__).resolve().parent


def test_doGetReqs_PEP631():
	using = "PEP631"
	extras = "socks"
	pyproject = tomli.loads((THISDIR / "data/pep631_socks.toml").read_text(encoding="utf-8"))
	requirementsPaths = []
	skipDependencies = ["TOSKIP"]

	assert get_deps._doGetReqs(using, skipDependencies, extras, pyproject, requirementsPaths) == {
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
		"CHARDET",
		"PYTHON-DOTENV",
	}


def test_doGetReqs_requirements():
	using = "requirements"
	extras = f"{THISDIR}/data/test_requirements.txt"
	pyproject = {}
	requirementsPaths = [Path(f"{THISDIR}/data/test_requirements.txt")]
	skipDependencies = ["TOSKIP"]

	deps = get_deps._doGetReqs(using, skipDependencies, extras, pyproject, requirementsPaths)
	assert deps == {
		"NUMPY",
		"ODFPY",
		"OPENPYXL",
		"PANDAS",
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
	)  # xarray is an optional dependecy of pandas associated with 'computation' key that is not tracked in test_requirements.txt
