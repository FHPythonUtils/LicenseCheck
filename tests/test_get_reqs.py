import contextlib
from pathlib import Path

from licensecheck import types
from licensecheck.get_deps import resolve_requirements

THISDIR = Path(__file__).resolve().parent


def test_pep631_socks() -> None:
	using = "PEP631:socks"
	skipDependencies = [types.ucstr("TOSKIP")]

	assert resolve_requirements(using, skipDependencies) == {
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


def test_requirements() -> None:
	using = "requirements"
	extras = []
	requirementsPaths = [f"{THISDIR}/data/test_requirements.txt"]
	skipDependencies = [types.ucstr("TOSKIP")]

	deps = resolve_requirements(using, skipDependencies, extras, requirementsPaths)
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


def test_requirements_with_hashes() -> None:
	using = "requirements"
	extras = []
	requirementsPaths = [f"{THISDIR}/data/test_requirements_hash.txt"]
	skipDependencies = [types.ucstr("TOSKIP")]

	deps = resolve_requirements(using, skipDependencies, extras, requirementsPaths)
	assert deps == {"PACKAGING"}
	assert "TOSKIP" not in deps


def test_issue_62() -> None:
	using = "PEP631"
	extras = []
	requirementsPaths = [f"{THISDIR}/data/issue_62.toml"]
	skipDependencies = []

	reqs = resolve_requirements(using, skipDependencies, extras, requirementsPaths)
	assert "PYQT5" not in reqs

	assert reqs == {
		"CACHETOOLS",
		"CERTIFI",
		"CHARSET-NORMALIZER",
		"DEPRECATED",
		"EARTHENGINE-API",
		"GOOGLE-API-CORE",
		"GOOGLE-API-PYTHON-CLIENT",
		"GOOGLE-AUTH",
		"GOOGLE-AUTH-HTTPLIB2",
		"GOOGLE-CLOUD-CORE",
		"GOOGLE-CLOUD-STORAGE",
		"GOOGLE-CRC32C",
		"GOOGLE-RESUMABLE-MEDIA",
		"GOOGLEAPIS-COMMON-PROTOS",
		"HTTPLIB2",
		"IDNA",
		"NUMPY",
		"PANDAS",
		"PROTO-PLUS",
		"PROTOBUF",
		"PYARROW",
		"PYASN1",
		"PYASN1-MODULES",
		"PYPARSING",
		"PYTHON-DATEUTIL",
		"PYTZ",
		"REQUESTS",
		"RSA",
		"SIX",
		"URITEMPLATE",
		"URLLIB3",
		"WRAPT",
	}


def test_issue_81() -> None:
	using = "requirements"
	extras = []
	requirementsPaths = [f"{THISDIR}/data/issue_81.txt"]
	skipDependencies = []
	with contextlib.suppress(Exception):
		deps = resolve_requirements(using, skipDependencies, extras, requirementsPaths)
	#     RuntimeError:   Ã— No solution found when resolving dependencies:
	#       â•°â”€â–¶ Because nvidia-cudnn-cu12==8.9.2.26 has no wheels with a matching
	#           platform tag and you require nvidia-cudnn-cu12==8.9.2.26, we can
	#           conclude that your requirements are unsatisfiable.


def test_issue_84() -> None:
	using = "requirements"
	extras = []
	requirementsPaths = [f"{THISDIR}/data/issue_84.txt"]
	skipDependencies = []

	deps = resolve_requirements(using, skipDependencies, extras, requirementsPaths)
	assert deps == {
		"AMQP",
		"BILLIARD",
		"CELERY",
		"CLICK",
		"CLICK-DIDYOUMEAN",
		"CLICK-PLUGINS",
		"CLICK-REPL",
		"COLORAMA",
		"KOMBU",
		"PROMPT-TOOLKIT",
		"PYTZ",
		"VINE",
		"WCWIDTH",
	}
