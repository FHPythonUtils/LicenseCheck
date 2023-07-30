from pathlib import Path

import tomli

from licensecheck import  get_deps

THISDIR = Path(__file__).resolve().parent

def test_doGetReqs():

	using = "PEP631"
	extras = "socks"
	pyproject = tomli.loads((THISDIR/"data/pep631_socks.toml").read_text(encoding="utf-8"))
	requirementsPaths = []

	assert get_deps._doGetReqs(using, extras, pyproject, requirementsPaths) == {
		'ATTRS',
		'BACKPORTS.SHUTIL-GET-TERMINAL-SIZE',
		'BACKPORTS.SSL-MATCH-HOSTNAME',
		'CACHED-PROPERTY',
		'CERTIFI',
		'CHARDET',
		'CHARSET-NORMALIZER',
		'CLICK',
		'COLORAMA',
		'DISTRO',
		'DOCKER',
		'DOCKERPTY',
		'DOCOPT',
		'ENUM34',
		'FQDN',
		'IDNA',
		'IMPORTLIB-RESOURCES',
		'IPADDRESS',
		'ISODURATION',
		'JSONPOINTER',
		'JSONSCHEMA',
		'JSONSCHEMA-SPECIFICATIONS',
		'PACKAGING',
		'PARAMIKO',
		'PKGUTIL-RESOLVE-NAME',
		'PYSOCKS',
		'PYTHON-DOTENV',
		'PYTHON-SOCKS',
		'PYWIN32',
		'PYYAML',
		'REFERENCING',
		'REQUESTS',
		'RFC3339-VALIDATOR',
		'RFC3986-VALIDATOR',
		'RFC3987',
		'RPDS-PY',
		'SPHINX',
		'SPHINX-RTD-THEME',
		'SUBPROCESS32',
		'TEXTTABLE',
		'URI-TEMPLATE',
		'URLLIB3',
		'WEBCOLORS',
		'WEBSOCKET-CLIENT',
		'WEBSOCKETS',
		'WSACCEL',
	}
