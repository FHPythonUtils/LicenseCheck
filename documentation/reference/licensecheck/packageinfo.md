# Packageinfo

[Licensecheck Index](../README.md#licensecheck-index) /
[Licensecheck](./index.md#licensecheck) /
Packageinfo

> Auto-generated documentation for [licensecheck.packageinfo](../../../licensecheck/packageinfo.py) module.

- [Packageinfo](#packageinfo)
  - [getClassifiersLicense](#getclassifierslicense)
  - [getModuleSize](#getmodulesize)
  - [getMyPackageLicense](#getmypackagelicense)
  - [getPackages](#getpackages)
  - [getPackagesFromLocal](#getpackagesfromlocal)
  - [licenseFromClassifierlist](#licensefromclassifierlist)
  - [packageInfoFromPypi](#packageinfofrompypi)

## getClassifiersLicense

[Show source in packageinfo.py:128](../../../licensecheck/packageinfo.py#L128)

Get the package classifiers and license from "setup.cfg", "pyproject.toml" or user input

#### Returns

- `dict[str,` *Any]* - {"classifiers": list[str], "license": str}

#### Signature

```python
def getClassifiersLicense() -> dict[str, Any]:
    ...
```



## getModuleSize

[Show source in packageinfo.py:166](../../../licensecheck/packageinfo.py#L166)

Get the size of a given module as an int.

#### Arguments

- `path` *Path* - path to package
- `name` *str* - name of package

#### Returns

- `int` - size in bytes

#### Signature

```python
def getModuleSize(path: Path, name: str) -> int:
    ...
```



## getMyPackageLicense

[Show source in packageinfo.py:150](../../../licensecheck/packageinfo.py#L150)

Get the package license from "setup.cfg", "pyproject.toml" or user input

#### Returns

- `str` - license name

#### Signature

```python
def getMyPackageLicense() -> str:
    ...
```



## getPackages

[Show source in packageinfo.py:113](../../../licensecheck/packageinfo.py#L113)

Get dependency info.

#### Arguments

- `reqs` *list[str]* - list of dependency names to gather info on

#### Returns

- `list[PackageInfo]` - list of dependencies

#### Signature

```python
def getPackages(reqs: list[str]) -> list[PackageInfo]:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)



## getPackagesFromLocal

[Show source in packageinfo.py:18](../../../licensecheck/packageinfo.py#L18)

Get a list of package info from local files including version, author
and	the license.

#### Arguments

- `requirements` *list[str]* - [description]

#### Returns

- `list[PackageInfo]` - [description]

#### Signature

```python
def getPackagesFromLocal(requirements: list[str]) -> list[PackageInfo]:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)



## licenseFromClassifierlist

[Show source in packageinfo.py:95](../../../licensecheck/packageinfo.py#L95)

Get license string from a list of project classifiers.

#### Arguments

- `classifiers` *list[str]* - list of classifiers

#### Returns

- `str` - the license name

#### Signature

```python
def licenseFromClassifierlist(classifiers: list[str]) -> str:
    ...
```



## packageInfoFromPypi

[Show source in packageinfo.py:65](../../../licensecheck/packageinfo.py#L65)

Get a list of package info from pypi.org including version, author
and	the license.

#### Arguments

- `requirements` *list[str]* - [description]

#### Returns

- `list[PackageInfo]` - [description]

#### Signature

```python
def packageInfoFromPypi(requirements: list[str]) -> list[PackageInfo]:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)


