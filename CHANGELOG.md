# Changelog
All major and minor version changes will be documented in this file. Details of
patch-level version changes can be found in [commit messages](../../commits/master).

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
