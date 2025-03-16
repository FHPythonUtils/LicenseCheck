[![GitHub top language](https://img.shields.io/github/languages/top/FHPythonUtils/LicenseCheck.svg?style=for-the-badge&cacheSeconds=28800)](../../)
[![Issues](https://img.shields.io/github/issues/FHPythonUtils/LicenseCheck.svg?style=for-the-badge&cacheSeconds=28800)](../../issues)
[![License](https://img.shields.io/github/license/FHPythonUtils/LicenseCheck.svg?style=for-the-badge&cacheSeconds=28800)](/LICENSE.md)
[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/LicenseCheck.svg?style=for-the-badge&cacheSeconds=28800)](../../commits/master)
[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/LicenseCheck.svg?style=for-the-badge&cacheSeconds=28800)](../../commits/master)
[![PyPI Downloads](https://img.shields.io/pypi/dm/licensecheck.svg?style=for-the-badge&cacheSeconds=28800)](https://pypistats.org/packages/licensecheck)
[![PyPI Total Downloads](https://img.shields.io/badge/dynamic/json?style=for-the-badge&label=total%20downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi%2Epepy%2Etech%2Fapi%2Fv2%2Fprojects%2Flicensecheck)](https://pepy.tech/project/licensecheck)
[![PyPI Version](https://img.shields.io/pypi/v/licensecheck.svg?style=for-the-badge&cacheSeconds=28800)](https://pypi.org/project/licensecheck)

<!-- omit in toc -->
# LicenseCheck

<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">

NOTICE: I am not a lawyer (IANAL)

**Any output provided by this software is for general informational purposes only and
should not be construed as legal advice. I am not a lawyer and there is no guarantee that the
information provided here is complete or correct. Any reliance on the information provided by this
software is at your own risk.**

See also: https://en.wikipedia.org/wiki/IANAL, [project license (MIT)](/LICENSE.md)

Output the licences used by dependencies and check if these are compatible with
the project license

<!-- omit in toc -->
## Table of Contents

- [Examples from the command-line](#examples-from-the-command-line)
	- [Pipe a requirements.txt file as input](#pipe-a-requirementstxt-file-as-input)
	- [Using pyproject.toml (default if not piping input)](#using-pyprojecttoml-default-if-not-piping-input)
	- [Failing on packages under MIT license](#failing-on-packages-under-mit-license)
	- [Only allow a predefined set of licenses](#only-allow-a-predefined-set-of-licenses)
	- [Show only failing](#show-only-failing)
	- [Use csv format](#use-csv-format)
- [Help](#help)
- [Configuration Example](#configuration-example)
	- [Example 1: pyproject.toml](#example-1-pyprojecttoml)
	- [Example 2: licensecheck.json](#example-2-licensecheckjson)
	- [Example 3: licensecheck.ini](#example-3-licensecheckini)
- [Documentation](#documentation)
- [Install With PIP](#install-with-pip)
- [Language information](#language-information)
	- [Built for](#built-for)
- [Install Python on Windows](#install-python-on-windows)
	- [Chocolatey](#chocolatey)
	- [Windows - Python.org](#windows---pythonorg)
- [Install Python on Linux](#install-python-on-linux)
	- [Apt](#apt)
	- [Dnf](#dnf)
- [Install Python on MacOS](#install-python-on-macos)
	- [Homebrew](#homebrew)
	- [MacOS - Python.org](#macos---pythonorg)
- [How to run](#how-to-run)
	- [Windows](#windows)
	- [Linux/ MacOS](#linux-macos)
- [Building](#building)
- [Testing](#testing)
- [Download Project](#download-project)
	- [Clone](#clone)
		- [Using The Command Line](#using-the-command-line)
		- [Using GitHub Desktop](#using-github-desktop)
	- [Download Zip File](#download-zip-file)
- [Community Files](#community-files)
	- [Licence](#licence)
	- [Changelog](#changelog)
	- [Code of Conduct](#code-of-conduct)
	- [Contributing](#contributing)
	- [Security](#security)
	- [Support](#support)
	- [Rationale](#rationale)

## Examples from the command-line

See below for the output if you run `licensecheck` in this directory

### Pipe a requirements.txt file as input

```txt
>> cat ./requirements.txt | licensecheck

               Info
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Item            ┃ Value        ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ program         │ licensecheck │
│ version         │ 2025         │
│ license         │ MIT LICENSE  │
│ project_license │ MIT LICENSE  │
└─────────────────┴──────────────┘

                              List Of Packages
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Compatible ┃ Package             ┃ License(s)                            ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ✔          │ Markdown            │ BSD LICENSE                           │
│ ✔          │ Pygments            │ BSD LICENSE                           │
│ ✔          │ appdirs             │ MIT LICENSE                           │
│ ✔          │ attrs               │ MIT LICENSE                           │
│ ✔          │ boolean.py          │ BSD-2-CLAUSE                          │
│ ✔          │ cattrs              │ MIT LICENSE                           │
│ ✔          │ certifi             │ MOZILLA PUBLIC LICENSE 2.0 _MPL 2.0_  │
│ ✔          │ charset-normalizer  │ MIT LICENSE                           │
│ ✔          │ colorama            │ BSD LICENSE                           │
│ ✔          │ fhconfparser        │ MIT LICENSE                           │
│ ✔          │ idna                │ BSD LICENSE                           │
│ ✔          │ license-expression  │ APACHE-2.0                            │
│ ✔          │ loguru              │ MIT LICENSE                           │
│ ✔          │ markdown-it-py      │ MIT LICENSE                           │
│ ✔          │ mdurl               │ MIT LICENSE                           │
│ ✔          │ packaging           │ APACHE SOFTWARE LICENSE;; BSD LICENSE │
│ ✔          │ platformdirs        │ MIT LICENSE                           │
│ ✔          │ requests            │ APACHE SOFTWARE LICENSE               │
│ ✔          │ requests-cache      │ BSD LICENSE                           │
│ ✔          │ requirements-parser │ APACHE SOFTWARE LICENSE               │
│ ✔          │ rich                │ MIT LICENSE                           │
│ ✔          │ setuptools          │ MIT LICENSE                           │
│ ✔          │ six                 │ MIT LICENSE                           │
│ ✔          │ tomli               │ MIT LICENSE                           │
│ ✔          │ types-setuptools    │ APACHE SOFTWARE LICENSE               │
│ ✔          │ url-normalize       │ MIT LICENSE                           │
│ ✔          │ urllib3             │ MIT LICENSE                           │
│ ✔          │ uv                  │ APACHE SOFTWARE LICENSE;; MIT LICENSE │
│ ✔          │ win32_setctime      │ MIT LICENSE                           │
└────────────┴─────────────────────┴───────────────────────────────────────┘

└────────────┴─────────────────────┴──────────────────────────────────────┘
```

### Using pyproject.toml (default if not piping input)

```txt
>> licensecheck  --fail-licenses mit
...
```

### Failing on packages under MIT license

```txt
>> licensecheck  --fail-licenses mit

               Info
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Item            ┃ Value        ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ program         │ licensecheck │
│ version         │ 2025.0.1     │
│ license         │ MIT LICENSE  │
│ project_license │ MIT LICENSE  │
└─────────────────┴──────────────┘

                              List Of Packages
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Compatible ┃ Package             ┃ License(s)                            ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ✔          │ Markdown            │ BSD LICENSE                           │
│ ✔          │ Pygments            │ BSD LICENSE                           │
│ ✖          │ appdirs             │ MIT LICENSE                           │
│ ✖          │ attrs               │ MIT LICENSE                           │
│ ✔          │ boolean.py          │ BSD-2-CLAUSE                          │
│ ✖          │ cattrs              │ MIT LICENSE                           │
│ ✔          │ certifi             │ MOZILLA PUBLIC LICENSE 2.0 _MPL 2.0_  │
│ ✖          │ charset-normalizer  │ MIT LICENSE                           │
│ ✔          │ colorama            │ BSD LICENSE                           │
│ ✖          │ fhconfparser        │ MIT LICENSE                           │
│ ✔          │ idna                │ BSD LICENSE                           │
│ ✔          │ license-expression  │ APACHE-2.0                            │
│ ✖          │ loguru              │ MIT LICENSE                           │
│ ✖          │ markdown-it-py      │ MIT LICENSE                           │
│ ✖          │ mdurl               │ MIT LICENSE                           │
│ ✔          │ packaging           │ APACHE SOFTWARE LICENSE;; BSD LICENSE │
│ ✖          │ platformdirs        │ MIT LICENSE                           │
│ ✔          │ requests            │ APACHE SOFTWARE LICENSE               │
│ ✔          │ requests-cache      │ BSD LICENSE                           │
│ ✔          │ requirements-parser │ APACHE SOFTWARE LICENSE               │
│ ✖          │ rich                │ MIT LICENSE                           │
│ ✖          │ setuptools          │ MIT LICENSE                           │
│ ✖          │ six                 │ MIT LICENSE                           │
│ ✖          │ tomli               │ MIT LICENSE                           │
│ ✔          │ types-setuptools    │ APACHE SOFTWARE LICENSE               │
│ ✖          │ url-normalize       │ MIT LICENSE                           │
│ ✖          │ urllib3             │ MIT LICENSE                           │
│ ✔          │ uv                  │ APACHE SOFTWARE LICENSE;; MIT LICENSE │
│ ✖          │ win32_setctime      │ MIT LICENSE                           │
└────────────┴─────────────────────┴───────────────────────────────────────┘


```

### Only allow a predefined set of licenses

```txt

>> licensecheck --only-licenses mit apache
...
                             List Of Packages
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Compatible ┃ Package             ┃ License(s)                            ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ✖          │ Markdown            │ BSD LICENSE                           │
│ ✖          │ Pygments            │ BSD LICENSE                           │
│ ✔          │ appdirs             │ MIT LICENSE                           │
│ ✔          │ attrs               │ MIT LICENSE                           │
│ ✖          │ boolean.py          │ BSD-2-CLAUSE                          │
│ ✔          │ cattrs              │ MIT LICENSE                           │
│ ✖          │ certifi             │ MOZILLA PUBLIC LICENSE 2.0 _MPL 2.0_  │
...

```



### Show only failing

```txt
>>> licensecheck  --only-licenses mit apache --show-only-failing

               Info
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Item            ┃ Value        ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ program         │ licensecheck │
│ version         │ 2025.0.1     │
│ license         │ MIT LICENSE  │
│ project_license │ MIT LICENSE  │
└─────────────────┴──────────────┘

                           List Of Packages
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Compatible ┃ Package        ┃ License(s)                           ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ✖          │ Markdown       │ BSD LICENSE                          │
│ ✖          │ Pygments       │ BSD LICENSE                          │
│ ✖          │ boolean.py     │ BSD-2-CLAUSE                         │
│ ✖          │ certifi        │ MOZILLA PUBLIC LICENSE 2.0 _MPL 2.0_ │
│ ✖          │ colorama       │ BSD LICENSE                          │
│ ✖          │ idna           │ BSD LICENSE                          │
│ ✖          │ requests-cache │ BSD LICENSE                          │
└────────────┴────────────────┴──────────────────────────────────────┘
```

### Use csv format

```csv
>>> licensecheck  --only-licenses mit apache --show-only-failing -f csv
name,version,size,homePage,author,license,licenseCompat,errorCode,namever
Markdown,3.7,361400,UNKNOWN,"Manfred Stienstra, Yuri Takhteyev",BSD LICENSE,False,0,Markdown-3.7
Pygments,2.19.1,4508396,UNKNOWN,UNKNOWN,BSD LICENSE,False,0,Pygments-2.19.1
boolean.py,4.0,109354,https://github.com/bastikr/boolean.py,Sebastian Kraemer,BSD-2-CLAUSE,False,0,boolean.py-4.0
certifi,2025.1.31,305559,https://github.com/certifi/python-certifi,Kenneth Reitz,MOZILLA PUBLIC LICENSE 2.0 _MPL 2.0_,False,0,certifi-2025.1.31
colorama,0.4.6,76299,UNKNOWN,UNKNOWN,BSD LICENSE,False,0,colorama-0.4.6
idna,3.10,349141,UNKNOWN,UNKNOWN,BSD LICENSE,False,0,idna-3.10
requests-cache,1.2.1,174099,https://github.com/requests-cache/requests-cache,Roman Haritonov,BSD LICENSE,False,0,requests-cache-1.2.1
```

## Help

```txt
usage: licensecheck [-h] [--license LICENSE] [--format FORMAT] [--requirements-paths REQUIREMENTS_PATHS [REQUIREMENTS_PATHS ...]]
                    [--groups GROUPS [GROUPS ...]] [--file FILE] [--ignore-packages IGNORE_PACKAGES [IGNORE_PACKAGES ...]]
                    [--fail-packages FAIL_PACKAGES [FAIL_PACKAGES ...]] [--ignore-licenses IGNORE_LICENSES [IGNORE_LICENSES ...]]
                    [--fail-licenses FAIL_LICENSES [FAIL_LICENSES ...]] [--only-licenses ONLY_LICENSES [ONLY_LICENSES ...]]
                    [--skip-dependencies SKIP_DEPENDENCIES [SKIP_DEPENDENCIES ...]]
                    [--hide-output-parameters HIDE_OUTPUT_PARAMETERS [HIDE_OUTPUT_PARAMETERS ...]] [--show-only-failing]
                    [--pypi-api PYPI_API] [--zero]

Output the licenses used by dependencies and check if these are compatible with the project license.

options:
  -h, --help            show this help message and exit
  --license LICENSE, -l LICENSE
                        Specify the project license explicitly, rather than rely on licensecheck interpreting this from pyproject.toml
  --format FORMAT, -f FORMAT
                        Output format. one of: json, markdown, html, csv, ansi, simple. default=simple
  --requirements-paths REQUIREMENTS_PATHS [REQUIREMENTS_PATHS ...], -r REQUIREMENTS_PATHS [REQUIREMENTS_PATHS ...]
                        Filenames to read from (omit for stdin if piping, else pyproject.toml)
  --groups GROUPS [GROUPS ...], -g GROUPS [GROUPS ...]
                        Select groups/extras from supported files
  --file FILE, -o FILE  Filename to write output to (omit this for stdout)
  --ignore-packages IGNORE_PACKAGES [IGNORE_PACKAGES ...]
                        List of packages/dependencies to ignore (compat=True), globs are supported
  --fail-packages FAIL_PACKAGES [FAIL_PACKAGES ...]
                        List of packages/dependencies to fail (compat=False), globs are supported
  --ignore-licenses IGNORE_LICENSES [IGNORE_LICENSES ...]
                        List of licenses to ignore (skipped, compat may still be False)
  --fail-licenses FAIL_LICENSES [FAIL_LICENSES ...]
                        List of licenses to fail (compat=False)
  --only-licenses ONLY_LICENSES [ONLY_LICENSES ...]
                        List of allowed licenses (packages/dependencies with any other license will fail)
  --skip-dependencies SKIP_DEPENDENCIES [SKIP_DEPENDENCIES ...]
                        List of packages/dependencies to skip (this sets the 'compatability' to True)
  --hide-output-parameters HIDE_OUTPUT_PARAMETERS [HIDE_OUTPUT_PARAMETERS ...]
                        List of parameters to hide from the produced output
  --show-only-failing   Only output a list of incompatible/ failing packages from this lib
  --pypi-api PYPI_API   Specify a custom pypi api endpoint, for example if using a custom pypi server
  --zero, -0            Return non zero exit code if an incompatible license is found, ideal for CI/CD
```

You can also import this into your own project and use any of the functions
in the DOCS

## Configuration Example

Configuration files are parsed in the following order: `pyproject.toml`,
`setup.cfg`, `licensecheck.toml`, `licensecheck.json`, `licensecheck.ini`,
`~/licensecheck.toml`, `~/licensecheck.json`, `~/licensecheck.ini`

- ⚠ All config files are parsed, however configuration defined in previous files takes precedent

Add optional path to requirements.txt as outlined in
https://github.com/FHPythonUtils/LicenseCheck/issues/9#issuecomment-898878228
for example: `licensecheck --using requirements:c:/path/to/reqs.txt;path/to/other/reqs.txt`

### Example 1: pyproject.toml

The following config is equivalent to `licensecheck -u 'requirements:requirements.txt;requirements_optional.txt' -f json`

```toml
[tool.licensecheck]
using = "requirements:requirements.txt;requirements_optional.txt"
format = "json"
```

### Example 2: licensecheck.json

The following config is equivalent to `licensecheck -u 'requirements:requirements.txt;requirements_optional.txt' -f json`

```json
{
	"tool": {
		"licensecheck": {
			"using": "requirements:requirements.txt;requirements_optional.txt",
			"format": "json"
		}
	}
}
```

### Example 3: licensecheck.ini

The following config is equivalent to `licensecheck -u 'requirements:requirements.txt;requirements_optional.txt' -f json`

```ini
[licensecheck]
using = "requirements:requirements.txt;requirements_optional.txt"
format = "json"
```

## Documentation

A high-level overview of how the documentation is organized organized will help you know
where to look for certain things:

<!--
- [Tutorials](/documentation/tutorials) take you by the hand through a series of steps to get
  started using the software. Start here if you’re new.
-->
- The [Technical Reference](/documentation/reference) documents APIs and other aspects of the
  machinery. This documentation describes how to use the classes and functions at a lower level
  and assume that you have a good high-level understanding of the software.
<!--
- The [Help](/documentation/help) guide provides a starting point and outlines common issues that you
  may have.
-->

## Install With PIP

```python
pip install licensecheck
```

Head to https://pypi.org/project/licensecheck/ for more info

## Language information

### Built for

This program has been written for Python versions 3.8 - 3.11 and has been tested with both 3.8 and
3.11

## Install Python on Windows

### Chocolatey

```powershell
choco install python
```

### Windows - Python.org

To install Python, go to https://www.python.org/downloads/windows/ and download the latest
version.

## Install Python on Linux

### Apt

```bash
sudo apt install python3.x
```

### Dnf

```bash
sudo dnf install python3.x
```

## Install Python on MacOS

### Homebrew

```bash
brew install python@3.x
```

### MacOS - Python.org

To install Python, go to https://www.python.org/downloads/macos/ and download the latest
version.

## How to run

### Windows

- Module
	`py -3.x -m [module]` or `[module]` (if module installs a script)

- File
	`py -3.x [file]` or `./[file]`

### Linux/ MacOS

- Module
	`python3.x -m [module]` or `[module]` (if module installs a script)

- File
	`python3.x [file]` or `./[file]`

## Building

This project uses https://github.com/FHPythonUtils/FHMake to automate most of the building. This
command generates the documentation, updates the requirements.txt and builds the library artefacts

Note the functionality provided by fhmake can be approximated by the following

```sh
handsdown  --cleanup -o documentation/reference
poetry export -f requirements.txt --output requirements.txt
poetry export -f requirements.txt --with dev --output requirements_optional.txt
poetry build
```

`fhmake audit` can be run to perform additional checks

## Testing

For testing with the version of python used by poetry use

```sh
poetry run pytest
```

Alternatively use `tox` to run tests over python 3.8 - 3.11

```sh
tox
```

## Download Project

### Clone

#### Using The Command Line

1. Press the Clone or download button in the top right
2. Copy the URL (link)
3. Open the command line and change directory to where you wish to
clone to
4. Type 'git clone' followed by URL in step 2
	```bash
	git clone https://github.com/FHPythonUtils/LicenseCheck
	```

More information can be found at
https://help.github.com/en/articles/cloning-a-repository

#### Using GitHub Desktop

1. Press the Clone or download button in the top right
2. Click open in desktop
3. Choose the path for where you want and click Clone

More information can be found at
https://help.github.com/en/desktop/contributing-to-projects/cloning-a-repository-from-github-to-github-desktop

### Download Zip File

1. Download this GitHub repository
2. Extract the zip archive
3. Copy/ move to the desired location

## Community Files

### Licence

MIT License
Copyright (c) FredHappyface
(See the [LICENSE](/LICENSE.md) for more information.)

### Changelog

See the [Changelog](/CHANGELOG.md) for more information.

### Code of Conduct

Online communities include people from many backgrounds. The *Project*
contributors are committed to providing a friendly, safe and welcoming
environment for all. Please see the
[Code of Conduct](https://github.com/FHPythonUtils/.github/blob/master/CODE_OF_CONDUCT.md)
 for more information.

### Contributing

Contributions are welcome, please see the
[Contributing Guidelines](https://github.com/FHPythonUtils/.github/blob/master/CONTRIBUTING.md)
for more information.

### Security

Thank you for improving the security of the project, please see the
[Security Policy](https://github.com/FHPythonUtils/.github/blob/master/SECURITY.md)
for more information.

### Support

Thank you for using this project, I hope it is of use to you. Please be aware that
those involved with the project often do so for fun along with other commitments
(such as work, family, etc). Please see the
[Support Policy](https://github.com/FHPythonUtils/.github/blob/master/SUPPORT.md)
for more information.

### Rationale

The rationale acts as a guide to various processes regarding projects such as
the versioning scheme and the programming styles used. Please see the
[Rationale](https://github.com/FHPythonUtils/.github/blob/master/RATIONALE.md)
for more information.
