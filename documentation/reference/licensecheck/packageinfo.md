# Packageinfo

[Licensecheck Index](../README.md#licensecheck-index) /
[Licensecheck](./index.md#licensecheck) /
Packageinfo

> Auto-generated documentation for [licensecheck.packageinfo](../../../licensecheck/packageinfo.py) module.

- [Packageinfo](#packageinfo)
  - [getClassifiersLicense](#getclassifierslicense)
  - [getModuleSize](#getmodulesize)
  - [getMyPackageLicense](#getmypackagelicense)
  - [getPackageInfoLocal](#getpackageinfolocal)
  - [getPackageInfoPypi](#getpackageinfopypi)
  - [getPackages](#getpackages)
  - [licenseFromClassifierlist](#licensefromclassifierlist)

## getClassifiersLicense

[Show source in packageinfo.py:121](../../../licensecheck/packageinfo.py#L121)

Get the package classifiers and license from "setup.cfg", "pyproject.toml" or user input

#### Returns

- `dict[str,` *Any]* - {"classifiers": set[str], "license": str}

#### Signature

```python
def getClassifiersLicense() -> dict[str, Any]:
    ...
```



## getModuleSize

[Show source in packageinfo.py:163](../../../licensecheck/packageinfo.py#L163)

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

[Show source in packageinfo.py:145](../../../licensecheck/packageinfo.py#L145)

Get the package license from "setup.cfg", "pyproject.toml" or user input

#### Returns

- `str` - license name

#### Signature

```python
def getMyPackageLicense() -> str:
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

[Show source in packageinfo.py:55](../../../licensecheck/packageinfo.py#L55)

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

[Show source in packageinfo.py:99](../../../licensecheck/packageinfo.py#L99)

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

[Show source in packageinfo.py:81](../../../licensecheck/packageinfo.py#L81)

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


