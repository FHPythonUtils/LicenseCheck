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

[Show source in packageinfo.py:162](../../../licensecheck/packageinfo.py#L162)

Get the size of a given module as an int.

#### Arguments

- `path` *Path* - path to package
- `name` *str* - name of package

#### Returns

- `int` - size in bytes

#### Signature

```python
def getModuleSize(path: Path, name: ucstr) -> int:
    ...
```

#### See also

- [ucstr](./types.md#ucstr)



## getMyPackageLicense

[Show source in packageinfo.py:145](../../../licensecheck/packageinfo.py#L145)

Get the package license from "setup.cfg", "pyproject.toml" or user input

#### Returns

- `str` - license name

#### Signature

```python
def getMyPackageLicense() -> ucstr:
    ...
```

#### See also

- [ucstr](./types.md#ucstr)



## getMyPackageMetadata

[Show source in packageinfo.py:121](../../../licensecheck/packageinfo.py#L121)

Get the package classifiers and license from "setup.cfg", "pyproject.toml"

#### Returns

- `dict[str,` *Any]* - {"classifiers": list[str], "license": ucstr}

#### Signature

```python
def getMyPackageMetadata() -> dict[str, Any]:
    ...
```



## getPackageInfoLocal

[Show source in packageinfo.py:15](../../../licensecheck/packageinfo.py#L15)

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
def getPackageInfoLocal(requirement: ucstr) -> PackageInfo:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)



## getPackageInfoPypi

[Show source in packageinfo.py:52](../../../licensecheck/packageinfo.py#L52)

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
def getPackageInfoPypi(requirement: ucstr) -> PackageInfo:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)



## getPackages

[Show source in packageinfo.py:99](../../../licensecheck/packageinfo.py#L99)

Get dependency info.

#### Arguments

- `reqs` *set[ucstr]* - set of dependency names to gather info on

#### Returns

- `set[PackageInfo]` - set of dependencies

#### Signature

```python
def getPackages(reqs: set[ucstr]) -> set[PackageInfo]:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)



## licenseFromClassifierlist

[Show source in packageinfo.py:79](../../../licensecheck/packageinfo.py#L79)

Get license string from a list of project classifiers.

#### Arguments

- `classifiers` *list[str]* - list of classifiers

#### Returns

- `str` - the license name

#### Signature

```python
def licenseFromClassifierlist(classifiers: list[str]) -> ucstr:
    ...
```

#### See also

- [ucstr](./types.md#ucstr)