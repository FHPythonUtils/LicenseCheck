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

[Show source in packageinfo.py:161](../../../licensecheck/packageinfo.py#L161)

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

[Show source in packageinfo.py:144](../../../licensecheck/packageinfo.py#L144)

Get the package license from "setup.cfg", "pyproject.toml" or user input

#### Returns

- `str` - license name

#### Signature

```python
def getMyPackageLicense() -> str:
    ...
```



## getMyPackageMetadata

[Show source in packageinfo.py:120](../../../licensecheck/packageinfo.py#L120)

Get the package classifiers and license from "setup.cfg", "pyproject.toml"

#### Returns

- `dict[str,` *Any]* - {"classifiers": list[str], "license": str}

#### Signature

```python
def getMyPackageMetadata() -> dict[str, Any]:
    ...
```



## getPackageInfoLocal

[Show source in packageinfo.py:16](../../../licensecheck/packageinfo.py#L16)

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

[Show source in packageinfo.py:53](../../../licensecheck/packageinfo.py#L53)

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

[Show source in packageinfo.py:98](../../../licensecheck/packageinfo.py#L98)

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

[Show source in packageinfo.py:78](../../../licensecheck/packageinfo.py#L78)

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


