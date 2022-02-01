# packageinfo

> Auto-generated documentation for [licensecheck.packageinfo](../../licensecheck/packageinfo.py) module.

Get information for installed and online packages.

- [Licensecheck](../README.md#licensecheck-index) / [Modules](../README.md#licensecheck-modules) / [licensecheck](index.md#licensecheck) / packageinfo
    - [getModuleSize](#getmodulesize)
    - [getMyPackageLicense](#getmypackagelicense)
    - [getPackages](#getpackages)
    - [getPackagesFromLocal](#getpackagesfromlocal)
    - [licenseFromClassifierlist](#licensefromclassifierlist)
    - [packageInfoFromPypi](#packageinfofrompypi)

## getModuleSize

[[find in source code]](../../licensecheck/packageinfo.py#L153)

```python
def getModuleSize(path: Path, name: str) -> int:
```

Get the size of a given module as an int.

#### Arguments

- `path` *Path* - path to package
- `name` *str* - name of package

#### Returns

- `int` - size in bytes

## getMyPackageLicense

[[find in source code]](../../licensecheck/packageinfo.py#L122)

```python
def getMyPackageLicense() -> str:
```

Get the pyproject data.

#### Returns

- `str` - license name

#### Raises

- `RuntimeError` - Must specify a license using license spdx or classifier (tool.poetry or tool.flit)

## getPackages

[[find in source code]](../../licensecheck/packageinfo.py#L106)

```python
def getPackages(reqs: list[str]) -> list[PackageInfo]:
```

Get dependency info.

#### Arguments

- `reqs` *list[str]* - list of dependency names to gather info on

#### Returns

- `list[PackageInfo]` - list of dependencies

## getPackagesFromLocal

[[find in source code]](../../licensecheck/packageinfo.py#L17)

```python
def getPackagesFromLocal(requirements: list[str]) -> list[PackageInfo]:
```

Get a list of package info from local files including version, author
and	the license.

#### Arguments

- `requirements` *list[str]* - [description]

#### Returns

- `list[PackageInfo]` - [description]

## licenseFromClassifierlist

[[find in source code]](../../licensecheck/packageinfo.py#L88)

```python
def licenseFromClassifierlist(classifiers: list[str]) -> str:
```

Get license string from a list of project classifiers.

#### Arguments

- `classifiers` *list[str]* - list of classifiers

#### Returns

- `str` - the license name

## packageInfoFromPypi

[[find in source code]](../../licensecheck/packageinfo.py#L58)

```python
def packageInfoFromPypi(requirements: list[str]) -> list[PackageInfo]:
```

Get a list of package info from pypi.org including version, author
and	the license.

#### Arguments

- `requirements` *list[str]* - [description]

#### Returns

- `list[PackageInfo]` - [description]
