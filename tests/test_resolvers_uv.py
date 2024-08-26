from pathlib import Path

from licensecheck import types
from licensecheck.resolvers import uv as req_uv

THISDIR = Path(__file__).resolve().parent


def test_doGetReqs_PEP631() -> None:
	using = "PEP631"
	extras = ["socks"]
	requirementsPaths = [f"{THISDIR}/data/pep631_socks.toml"]
	skipDependencies = [types.ucstr("TOSKIP")]

	assert req_uv.get_reqs(using, skipDependencies, extras, requirementsPaths) == {
		"DOCKERPTY",
		"ATTRS",
		"JSONSCHEMA",
		"PYYAML",
		"PYSOCKS",
		"CERTIFI",
		"DOCKER",
		"TEXTTABLE",
		"PYWIN32",
		"DOCOPT",
		"PARAMIKO",
		"IDNA",
		"COLORAMA",
		"CACHED-PROPERTY",
		"DISTRO",
		"CHARSET-NORMALIZER",
		"URLLIB3",
		"WEBSOCKET-CLIENT",
		"REQUESTS",
		"PYTHON-DOTENV",
		"CFFI",
		"PYNACL",
		"BCRYPT",
		"SIX",
		"PYCPARSER",
		"CRYPTOGRAPHY",
		"PYRSISTENT",
		"PYPIWIN32",
		"SETUPTOOLS",
	}


def test_doGetReqs_requirements() -> None:
	using = "requirements"
	extras = []
	requirementsPaths = [f"{THISDIR}/data/test_requirements.txt"]
	skipDependencies = [types.ucstr("TOSKIP")]

	deps = req_uv.get_reqs(using, skipDependencies, extras, requirementsPaths)
	assert deps == {
		"NUMPY",
		"ODFPY",
		"OPENPYXL",
		"PANDAS",
		"SIX",
		"DEFUSEDXML",
		"ET-XMLFILE",
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
	requirementsPaths = [f"{THISDIR}/data/test_requirements_hash.txt"]
	skipDependencies = [types.ucstr("TOSKIP")]

	deps = req_uv.get_reqs(using, skipDependencies, extras, requirementsPaths)
	assert deps == {"PACKAGING"}
	assert "TOSKIP" not in deps
