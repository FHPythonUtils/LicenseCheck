[![GitHub top language](https://img.shields.io/github/languages/top/FHPythonUtils/LicenseCheck.svg?style=for-the-badge)](../../)
[![Repository size](https://img.shields.io/github/repo-size/FHPythonUtils/LicenseCheck.svg?style=for-the-badge)](../../)
[![Issues](https://img.shields.io/github/issues/FHPythonUtils/LicenseCheck.svg?style=for-the-badge)](../../issues)
[![License](https://img.shields.io/github/license/FHPythonUtils/LicenseCheck.svg?style=for-the-badge)](/LICENSE.md)
[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/LicenseCheck.svg?style=for-the-badge)](../../commits/master)
[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/LicenseCheck.svg?style=for-the-badge)](../../commits/master)
[![PyPI Downloads](https://img.shields.io/pypi/dm/licensecheck.svg?style=for-the-badge)](https://pypistats.org/packages/licensecheck)
[![PyPI Total Downloads](https://img.shields.io/badge/dynamic/json?style=for-the-badge&label=total%20downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Flicensecheck)](https://pepy.tech/project/licensecheck)
[![PyPI Version](https://img.shields.io/pypi/v/licensecheck.svg?style=for-the-badge)](https://pypi.org/project/licensecheck)

<!-- omit in toc -->
# LicenseCheck

<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">

Output the licences used by dependencies and check if these are compatible with
the project license


<!-- omit in toc -->
## Table of Contents
- [Example Use](#example-use)
	- [Help](#help)
	- [Configuration](#configuration)
		- [Example 1: pyproject.toml](#example-1-pyprojecttoml)
		- [Example 2: licensecheck.json](#example-2-licensecheckjson)
		- [Example 3: licensecheck.ini](#example-3-licensecheckini)
- [Documentation](#documentation)
- [Install With PIP](#install-with-pip)
- [Language information](#language-information)
	- [Built for](#built-for)
- [Install Python on Windows](#install-python-on-windows)
	- [Chocolatey](#chocolatey)
	- [Download](#download)
- [Install Python on Linux](#install-python-on-linux)
	- [Apt](#apt)
- [How to run](#how-to-run)
	- [With VSCode](#with-vscode)
	- [From the Terminal](#from-the-terminal)
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



## Example Use

See below for the output if you run `licensecheck` in this directory

```txt
>> licensecheck
    | Package | License             |
    | ------- | ------------------- |
    | [+]     | certifi             | Mozilla Public License 2.0 (MP |
    | [+]     | chardet             | GNU Library or Lesser General  |
    | [+]     | idna                | BSD License                    |
    | [+]     | metprint            | MIT License                    |
    | [+]     | requests            | Apache Software License        |
    | [+]     | requirements-parser | BSD License                    |
    | [+]     | urllib3             | MIT License                    |
```


If `metprint` is installed the tables look slightly different (note that the
leftmost symbols are coloured in the terminal)

```txt
>> licensecheck -u requirements
    ┌────────────────────┬──────────────────────────────┐
    │Package             │License                       │
    ├────────────────────┼──────────────────────────────┤
[+] │pip                 │MIT License                   │
[+] │requests            │Apache Software License       │
[+] │requirements-parser │BSD License                   │
[+] │tomlkit             │MIT License                   │
    └────────────────────┴──────────────────────────────┘
```


```txt
>> licensecheck --fail-licenses mit
    ┌────────────────────┬──────────────────────────────┐
    │Package             │License                       │
    ├────────────────────┼──────────────────────────────┤
[+] │certifi             │Mozilla Public License 2.0 (MP│
[-] │charset-normalizer  │MIT License                   │
[+] │idna                │BSD License                   │
[-] │metprint            │MIT License                   │
[+] │requests            │Apache Software License       │
[+] │requirements-parser │BSD License                   │
[-] │tomlkit             │MIT License                   │
[-] │urllib3             │MIT License                   │
    └────────────────────┴──────────────────────────────┘
```

### Help

```txt
usage: __main__.py [-h] [--format FORMAT] [--file FILE] [--using USING]
                   [--ignore-packages IGNORE_PACKAGES [IGNORE_PACKAGES ...]]
                   [--fail-packages FAIL_PACKAGES [FAIL_PACKAGES ...]]
                   [--ignore-licenses IGNORE_LICENSES [IGNORE_LICENSES ...]]
                   [--fail-licenses FAIL_LICENSES [FAIL_LICENSES ...]] [--zero]

Output the licenses used by dependencies and check if these are compatible with the project license.

optional arguments:
  -h, --help            show this help message and exit
  --format FORMAT, -f FORMAT
                        Output format. one of: json, markdown, csv, ansi, simple. default=simple
  --file FILE, -o FILE  Filename to write to (omit for stdout)
  --using USING, -u USING
                        Environment to use e.g. requirements.txt. one of: requirements, poetry. default=poetry
  --ignore-packages IGNORE_PACKAGES [IGNORE_PACKAGES ...]
                        a list of packages to ignore (compat=True)
  --fail-packages FAIL_PACKAGES [FAIL_PACKAGES ...]
                        a list of packages to fail (compat=False)
  --ignore-licenses IGNORE_LICENSES [IGNORE_LICENSES ...]
                        a list of licenses to ignore (skipped, compat may still be False)
  --fail-licenses FAIL_LICENSES [FAIL_LICENSES ...]
                        a list of licenses to fail (compat=False)
  --zero, -0            Return non zero exit code if an incompatible license is found
```

You can also import this into your own project and use any of the functions
in the DOCS


### Configuration

Configuration files are parsed in the following order: `pyproject.toml`,
`setup.cfg`, `licensecheck.toml`, `licensecheck.json`, `licensecheck.ini`,
`~/licensecheck.toml`, `~/licensecheck.json`, `~/licensecheck.ini`

- ⚠ All config files are parsed, however configuration defined in previous files takes precedent

Add optional path to requirements.txt as outlined in
https://github.com/FHPythonUtils/LicenseCheck/issues/9#issuecomment-898878228
for example: `licensecheck --using requirements:c:/path/to/reqs.txt;path/to/other/reqs.txt`


#### Example 1: pyproject.toml

The following config is equivalent to `licensecheck -u 'requirements:requirements.txt;requirements_optional.txt' -f json`

```toml
[tool.licensecheck]
using = "requirements:requirements.txt;requirements_optional.txt"
format = "json"

```


#### Example 2: licensecheck.json

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


#### Example 3: licensecheck.ini

The following config is equivalent to `licensecheck -u 'requirements:requirements.txt;requirements_optional.txt' -f json`

```ini
[licensecheck]
using = "requirements:requirements.txt;requirements_optional.txt"
format = "json"

```

## Documentation
See the [Docs](/DOCS/) for more information.

## Install With PIP
```python
pip install licensecheck
```

Head to https://pypi.org/project/licensecheck/ for more info

## Language information
### Built for
This program has been written for Python 3 and has been tested with
Python version 3.9.0 <https://www.python.org/downloads/release/python-380/>.

## Install Python on Windows
### Chocolatey
```powershell
choco install python
```
### Download
To install Python, go to <https://www.python.org/> and download the latest
version.

## Install Python on Linux
### Apt
```bash
sudo apt install python3.9
```

## How to run
### With VSCode
1. Open the .py file in vscode
2. Ensure a python 3.9 interpreter is selected (Ctrl+Shift+P > Python:Select
Interpreter > Python 3.9)
3. Run by pressing Ctrl+F5 (if you are prompted to install any modules, accept)
### From the Terminal
```bash
./[file].py
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
$ git clone https://github.com/FHPythonUtils/LicenseCheck
```

More information can be found at
<https://help.github.com/en/articles/cloning-a-repository>

#### Using GitHub Desktop
1. Press the Clone or download button in the top right
2. Click open in desktop
3. Choose the path for where you want and click Clone

More information can be found at
<https://help.github.com/en/desktop/contributing-to-projects/cloning-a-repository-from-github-to-github-desktop>

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
