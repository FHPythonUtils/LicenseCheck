# Packageinfo

[Licensecheck Index](../README.md#licensecheck-index) /
[Licensecheck](./index.md#licensecheck) /
Packageinfo

> Auto-generated documentation for [licensecheck.packageinfo](../../../licensecheck/packageinfo.py) module.

- [Packageinfo](#packageinfo)
  - [getModuleSize](#getmodulesize)
  - [getMyPackageLicense](#getmypackagelicense)
  - [getMyPackageMetadata](#getmypackagemetadata)
  - [getPackageInfoLocal](#getpackageinfolocal)
  - [getPackageInfoPypi](#getpackageinfopypi)
  - [getPackages](#getpackages)
  - [licenseFromClassifierlist](#licensefromclassifierlist)

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

[Show source in packageinfo.py:149](../../../licensecheck/packageinfo.py#L149)

Get the package license from "setup.cfg", "pyproject.toml" or user input

#### Returns

- `str` - license name

#### Signature

```python
def getMyPackageLicense() -> str:
    ...
```



## getMyPackageMetadata

[Show source in packageinfo.py:125](../../../licensecheck/packageinfo.py#L125)

Get the package classifiers and license from "setup.cfg", "pyproject.toml"

#### Returns

- `dict[str,` *Any]* - {"classifiers": list[str], "license": str}

#### Signature

```python
def getMyPackageMetadata() -> dict[str, Any]:
    ...
```



## getPackageInfoLocal

[Show source in packageinfo.py:22](../../../licensecheck/packageinfo.py#L22)

Get package info from local files including version, author
and	the license.

#### Arguments

- `requirement` *str* - name of the package

#### Raises

- `ModuleNotFoundError` -  if the package does not exist

#### Returns

Type: *PackageInfo*
package information

#### Signature

```python
def getPackageInfoLocal(requirement: str) -> PackageInfo:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)



## getPackageInfoPypi

[Show source in packageinfo.py:60](../../../licensecheck/packageinfo.py#L60)

Get package info from local files including version, author
and	the license.

#### Arguments

- `requirement` *str* - name of the package

#### Raises

- `ModuleNotFoundError` -  if the package does not exist

#### Returns

Type: *PackageInfo*
package information

#### Signature

```python
def getPackageInfoPypi(requirement: str) -> PackageInfo:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)



## getPackages

[Show source in packageinfo.py:103](../../../licensecheck/packageinfo.py#L103)

Get dependency info.

#### Arguments

- `reqs` *set[str]* - set of dependency names to gather info on

#### Returns

- `set[PackageInfo]` - set of dependencies

#### Signature

```python
def getPackages(reqs: set[str]) -> set[PackageInfo]:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)



## licenseFromClassifierlist

[Show source in packageinfo.py:85](../../../licensecheck/packageinfo.py#L85)

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


