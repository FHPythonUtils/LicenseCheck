# Changelog

All major and minor version changes will be documented in this file. Details of
patch-level version changes can be found in [commit messages](../../commits/master).

## 2022.0.1 - 2022/02/01

- Hopefully fix https://github.com/FHPythonUtils/LicenseCheck/issues/14 for real this time
- Update deps
- Remove `pip`
- Replace `tomlkit` with `tomli`

## 2022 - 2022/01/14

- Fix https://github.com/FHPythonUtils/LicenseCheck/issues/18

## 2021.5.2 - 2021/10/18

- Compatible with pip 21.3
- Code quality improvements

## 2021.5 - 2021/09/14

- Add `-u poetry:dev` to command-line to include dev packages (excluded by default) per https://github.com/FHPythonUtils/LicenseCheck/issues/16
- Add support for proprietary license per https://github.com/FHPythonUtils/LicenseCheck/issues/15
- Raise RuntimeError if missing license and classifier https://github.com/FHPythonUtils/LicenseCheck/issues/14
- Quality improvements to license_matrix.py
- Add additional examples to readme
- Support pre-commit-hooks https://github.com/FHPythonUtils/LicenseCheck/issues/8

## 2021.4.1 - 2021/09/07

- Command-line options take precedent over config options as expected

## 2021.4 - 2021/09/07

- Add config file functionality per https://github.com/FHPythonUtils/LicenseCheck/issues/11
	- Parsed in the following order: `pyproject.toml`, `setup.cfg`, `licensecheck.toml`, `licensecheck.json`, `licensecheck.ini`, `~/licensecheck.toml`, `~/licensecheck.json`, `~/licensecheck.ini`
	- Note that the config takes precedent over command-line options
- Add optional path to requirements.txt as outlined in https://github.com/FHPythonUtils/LicenseCheck/issues/9#issuecomment-898878228
	- Eg. `licensecheck --using requirements:c:/path/to/reqs.txt;path/to/other/reqs.txt`

## 2021.3 - 2021/08/13

- Add `--ignore-packages`, `--fail-packages`,`--ignore-licenses`, `--fail-licenses`, per https://github.com/FHPythonUtils/LicenseCheck/issues/7
- Fix spelling
- Added a couple examples to the readme
- Added pylintrc to pyproject.toml

## 2021.2 - 2021/08/13

- Added ability to use requirements.txt per https://github.com/FHPythonUtils/LicenseCheck/issues/6
- Code clean-up + refactoring
- Fix spelling
- packagecompat.py → types.py as this module holds types + typing info

## 2021.1.2 - 2021/06/07

- reformat
- improve docstrings

## 2021.1.1 - 2021/03/01

- Add PSFL to matrix.

## 2021.1 - 2021/03/01

- Tidied up
- Added `--zero/-0` flag to return non-zero exit code when an incompatible
	license is found

## 2021 - 2021/01/24

- Updated requirements
- Fallback to requirements.txt when poetry throws an error and direct the user
	to troubleshoot

## 2020.0.4 - 2020/10/14

- Improved support for GPL fans out there by detecting variants in a more
	granular manner. Fewer false -ves for said GPL variants. E.g. a dependency with
	GPL2 only will be flagged for a project using GPL3

## 2020.0.3 - 2020/10/12

- set stdout to utf-8

## 2020.0.2 - 2020/10/12

- fancy tables in simple and ansi formats

## 2020.0.1 - 2020/10/11

- dependencies bugfix

## 2020 - 2020/10/09

- First release
