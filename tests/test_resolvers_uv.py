import contextlib
from pathlib import Path

from licensecheck import types
from licensecheck.resolvers import uv as req_uv

THISDIR = Path(__file__).resolve().parent


def test_PEP631() -> None:
	extras = ["socks"]
	requirementsPaths = [f"{THISDIR}/data/pep631_socks.toml"]
	skipDependencies = [types.ucstr("TOSKIP")]

	deps = req_uv.get_reqs(
		skipDependencies=skipDependencies,
		extras=extras,
		groups=[],
		requirementsPaths=requirementsPaths,
	)
	reqs = {d.name.upper() for d in deps}

	assert reqs == {
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
	requirementsPaths = [f"{THISDIR}/data/test_requirements.txt"]
	skipDependencies = [types.ucstr("TOSKIP")]

	deps = req_uv.get_reqs(
		skipDependencies, extras=[], groups=[], requirementsPaths=requirementsPaths
	)
	reqs = {d.name.upper() for d in deps}

	assert reqs == {
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
	assert "OPENPYXL" in reqs
	assert (
		"XARRAY" not in reqs
	)  # xarray is an optional dependency of pandas associated with 'computation' key that is not
	# tracked in test_requirements.txt


def test_requirements_with_hashes() -> None:
	requirementsPaths = [f"{THISDIR}/data/test_requirements_hash.txt"]
	skipDependencies = [types.ucstr("TOSKIP")]

	deps = req_uv.get_reqs(
		skipDependencies, extras=[], groups=[], requirementsPaths=requirementsPaths
	)
	reqs = {d.name.upper() for d in deps}
	assert reqs == {"PACKAGING"}
	assert "TOSKIP" not in reqs


def test_issue_62() -> None:
	requirementsPaths = [f"{THISDIR}/data/issue_62.toml"]

	deps = req_uv.get_reqs(
		skipDependencies=[], extras=[], groups=[], requirementsPaths=requirementsPaths
	)
	reqs = {d.name.upper() for d in deps}
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
	requirementsPaths = [f"{THISDIR}/data/issue_81.txt"]
	with contextlib.suppress(Exception):
		_deps = req_uv.get_reqs(
			skipDependencies=[], extras=[], groups=[], requirementsPaths=requirementsPaths
		)

	#     RuntimeError:    No solution found when resolving dependencies:
	#        Because nvidia-cudnn-cu12==8.9.2.26 has no wheels with a matching
	#           platform tag and you require nvidia-cudnn-cu12==8.9.2.26, we can
	#           conclude that your requirements are unsatisfiable.


def test_issue_84() -> None:
	requirementsPaths = [f"{THISDIR}/data/issue_84.txt"]

	deps = req_uv.get_reqs(
		skipDependencies=[], extras=[], groups=[], requirementsPaths=requirementsPaths
	)
	assert {d.name.upper() for d in deps} == {
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
		"TZDATA",
		"VINE",
		"WCWIDTH",
	}
