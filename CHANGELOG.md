# Changelog

All major and minor version changes will be documented in this file. Details of
patch-level version changes can be found in [commit messages](../../commits/master).

## 2024.3 - 2024/08/26

- Use uv to parse dependencies before falling back to the native resolver
- deprecate the native resolver as many 3rd party libs (uv/pip/poetry) have done better

## 2024.2 - 2024/04/04

- Add html output using `markdown` lib https://github.com/FHPythonUtils/LicenseCheck/issues/77

## 2024.1.5 - 2024/04/04

- fix critical TypeError: can only join an iterable

## 2024.1.4 - 2024/03/30

- fix critical https://github.com/FHPythonUtils/LicenseCheck/issues/75 where importlib.metadata.PackageMetadata.json does not exist in Python < 3.10

  ```txt
  py311: OK (7.55=setup[5.89]+cmd[1.66] seconds)
  py310: SKIP (0.02 seconds)
  py39: SKIP (0.02 seconds)
  py38: OK (6.23=setup[4.30]+cmd[1.94] seconds)
  congratulations :) (13.95 seconds)
  ```

## 2024.1.3 - 2024/03/20

- fix https://github.com/FHPythonUtils/LicenseCheck/issues/74
- update tests (as env has changed, ideally we'd mock more than we do atm)
- linting fixes

## 2024.1.2 - 2024/03/20

- fix: use `appdirs` for storing the db for `requests_cache`

## 2024.1.1 - 2024/03/17

- Update Matrix for AGPL_3_PLUS

## 2024.1 - 2024/03/16

- code improvements
- fix issue where onlyLicenses logic caused licensecompat to be `false` when unspecified from the command line
- move `cli()` to `cli.py`
- add tests for the main entry point
- update deps

## 2024 - 2024/01/27

- code improvements
- users can now specify a license from the command line with `--license` https://github.com/FHPythonUtils/LicenseCheck/issues/69

## 2024 - 2024/01/07

- update dependencies

## 2023.5.2 - 2023/12/01

- fix: crash when a namespace doesn't exist https://github.com/FHPythonUtils/LicenseCheck/issues/65
- fix: add support for double quotes in extras https://github.com/FHPythonUtils/LicenseCheck/pull/64,
  thanks https://github.com/arunkumarpandian

## 2023.5.1 - 2023/09/21

- Fix optional extras from dependencies being included by default. Thank you https://github.com/arunkumarpandian!
- Dynamically get version from package metadata. Thank you https://github.com/emesar
- Bump version of rich

## 2023.4.3 - 2023/08/30

- Add a new flag `--skip-dependencies` which will exclude from the processing a list of the current project dependencies. Suitable for private dependencies which are only available on a private registry and not on PyPi. Thank you https://github.com/Azraeht :)

## 2023.4.2 - 2023/08/25

- Fixed Bug: handle missing urls for a pypi package https://github.com/FHPythonUtils/LicenseCheck/issues/57. Thank you https://github.com/Azraeht!

## 2023.4.1 - 2023/08/20

- Fixed Bug: https://github.com/FHPythonUtils/LicenseCheck/issues/55

## 2023.4 - 2023/08/20

- Refactor and code enhancements
- Fixed Bug: fix behaviour of dependency discovery for 'extras', thank you https://github.com/TuriJ95!
- Fixed Bug: ignore-package not working, thank you https://github.com/mathiasbockwoldt !

## 2023.3 - 2023/07/29

- Fixed Bug: requirements:requirements.txt reading mode, thank you https://github.com/NicolaDonelli
- Fixed Bug: Permissive libraries are not compatible with closed licenses. Closes #49
- Fixed Bug: Unexpected warnings for ignored license. Closes #48
- New Feature: Support option ignore-licenses in pyproject.toml. Closes #46
- Performance enhancements
- Extended test suite

## 2023.2 - 2023/07/28

- New Feature: Improve error messages (#44)
- New Feature: Support Transitive Dependencies 1 layer deep (#42)
- Fixed Bug: Unexpected warnings for ignored license (#48)
- Fixed Bug: A compatible dual licensed library is shown as incompatible (#47)
- Fixed Bug: licensecheck gives IndexError: list index out of range (#41)
- Fixed Bug: Apache2 is shown as incompatible with LGPL3 (#40)

## 2023.1.4 - 2023/06/26

- Update format to output info and detected package license
- Bump dep versions

## 2023.1.2 - 2023/06/24

- Merge PR https://github.com/FHPythonUtils/LicenseCheck/pull/39 (Fixes #38)

## 2023.1.1 - 2023/03/07

- Merge PR https://github.com/FHPythonUtils/LicenseCheck/pull/33
  (implements feature: Support for PEP631: Declaring dependencies in pyproject.toml enhancement)
- Fix crash if setup.cfg exists with no metadata section
  (https://github.com/FHPythonUtils/LicenseCheck/issues/34)

## 2023

- Fix: https://github.com/FHPythonUtils/LicenseCheck/issues/26
- Fix python 3.8 compatibility, thanks https://github.com/NicolaDonelli !

## 2022.3.2 - 2022/12/30

- Fix: use constant `JOINS` (";; ") in place of hardcoded ", " string to avoid splitting single license with commas
- Fix: Add `GPL_X` for GPL without a defined version
- Minor refactoring eg renaming functions
- Make namever consistent
- Add regression tests

## 2022.3.0 - 2022/12/30

- Combined `PackageCompat` and `PackageInfo` to a `@dataclass` of `PackageInfo`
- `get_deps.py` and `packageinfo.py` use sets in-place of lists. NOTE: `list(depsWithLicenses)` is passed to `formatter.py` (which expects lists of `PackageInfo`)

## 2022.2.0 - 2022/10/22

- Add support for `setup.cfg` https://github.com/FHPythonUtils/LicenseCheck/issues/21
  (thank you https://github.com/NicolaDonelli for the code :))
- Use rich for table rendering https://github.com/FHPythonUtils/LicenseCheck/issues/20

## 2022.1.1 - 2022/04/09

- More detailed warnings per https://github.com/FHPythonUtils/LicenseCheck/issues/19
- Add check using spdx identifiers

## 2022.1 - 2022/04/06

- Remove metprint
- Move docs
- Update precommit

## 2022.0.2 - 2022/03/10

- Fix crash when calculating module size
- Fix crash when module name was in different case to the requirement

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
