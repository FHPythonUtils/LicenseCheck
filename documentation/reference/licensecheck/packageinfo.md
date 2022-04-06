# Packageinfo

> Auto-generated documentation for [licensecheck.packageinfo](../../../licensecheck/packageinfo.py) module.

Get information for installed and online packages.

- [Licensecheck](../README.md#licensecheck-index) / [Modules](../MODULES.md#licensecheck-modules) / [Licensecheck](index.md#licensecheck) / Packageinfo
    - [getModuleSize](#getmodulesize)
    - [getMyPackageLicense](#getmypackagelicense)
    - [getPackages](#getpackages)
    - [getPackagesFromLocal](#getpackagesfromlocal)
    - [licenseFromClassifierlist](#licensefromclassifierlist)
    - [packageInfoFromPypi](#packageinfofrompypi)

## getModuleSize

[[find in source code]](../../../licensecheck/packageinfo.py#L159)

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

[[find in source code]](../../../licensecheck/packageinfo.py#L128)

```python
def getMyPackageLicense() -> str:
```

Get the pyproject data.

#### Returns

- `str` - license name

#### Raises

- `RuntimeError` - Must specify a license using license spdx or classifier (tool.poetry or tool.flit)

## getPackages

[[find in source code]](../../../licensecheck/packageinfo.py#L112)

```python
def getPackages(reqs: list[str]) -> list[PackageInfo]:
```

Get dependency info.

#### Arguments

- `reqs` *list[str]* - list of dependency names to gather info on

#### Returns

- `list[PackageInfo]` - list of dependencies

#### See also

- [PackageInfo](types.md#packageinfo)

## getPackagesFromLocal

[[find in source code]](../../../licensecheck/packageinfo.py#L17)

```python
def getPackagesFromLocal(requirements: list[str]) -> list[PackageInfo]:
```

Get a list of package info from local files including version, author
and	the license.

#### Arguments

- `requirements` *list[str]* - [description]

#### Returns

- `list[PackageInfo]` - [description]

#### See also

- [PackageInfo](types.md#packageinfo)

## licenseFromClassifierlist

[[find in source code]](../../../licensecheck/packageinfo.py#L94)

```python
def licenseFromClassifierlist(classifiers: list[str]) -> str:
```

Get license string from a list of project classifiers.

#### Arguments

- `classifiers` *list[str]* - list of classifiers

#### Returns

- `str` - the license name

## packageInfoFromPypi

[[find in source code]](../../../licensecheck/packageinfo.py#L64)

```python
def packageInfoFromPypi(requirements: list[str]) -> list[PackageInfo]:
```

Get a list of package info from pypi.org including version, author
and	the license.

#### Arguments

- `requirements` *list[str]* - [description]

#### Returns

- `list[PackageInfo]` - [description]

#### See also

- [PackageInfo](types.md#packageinfo)
