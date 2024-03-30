# Packageinfo

[Licensecheck Index](../README.md#licensecheck-index) / [Licensecheck](./index.md#licensecheck) / Packageinfo

> Auto-generated documentation for [licensecheck.packageinfo](../../../licensecheck/packageinfo.py) module.

- [Packageinfo](#packageinfo)
  - [_pkgMetadataGet](#_pkgmetadataget)
  - [getModuleSize](#getmodulesize)
  - [getMyPackageLicense](#getmypackagelicense)
  - [getMyPackageMetadata](#getmypackagemetadata)
  - [getPackageInfoLocal](#getpackageinfolocal)
  - [getPackageInfoPypi](#getpackageinfopypi)
  - [getPackages](#getpackages)
  - [licenseFromClassifierlist](#licensefromclassifierlist)

## _pkgMetadataGet

[Show source in packageinfo.py:17](../../../licensecheck/packageinfo.py#L17)

Get a string from a key from pkgMetadata.

#### Signature

```python
def _pkgMetadataGet(
    pkgMetadata: metadata.PackageMetadata | dict[str, Any], key: str
) -> str: ...
```



## getModuleSize

[Show source in packageinfo.py:192](../../../licensecheck/packageinfo.py#L192)

Get the size of a given module as an int.

#### Arguments

----
 - `path` *Path* - path to package
 - `name` *str* - name of package

#### Returns

-------
 - `int` - size in bytes

#### Signature

```python
def getModuleSize(path: Path, name: ucstr) -> int: ...
```

#### See also

- [ucstr](./types.md#ucstr)



## getMyPackageLicense

[Show source in packageinfo.py:173](../../../licensecheck/packageinfo.py#L173)

Get the package license from "setup.cfg", "pyproject.toml" or user input.

Returns
-------
 str: license name

#### Signature

```python
def getMyPackageLicense() -> ucstr: ...
```

#### See also

- [ucstr](./types.md#ucstr)



## getMyPackageMetadata

[Show source in packageinfo.py:144](../../../licensecheck/packageinfo.py#L144)

Get the package classifiers and license from "setup.cfg", "pyproject.toml".

Returns
-------
 dict[str, Any]: {"classifiers": list[str], "license": ucstr}

#### Signature

```python
def getMyPackageMetadata() -> dict[str, Any]: ...
```



## getPackageInfoLocal

[Show source in packageinfo.py:25](../../../licensecheck/packageinfo.py#L25)

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
def getPackageInfoLocal(requirement: ucstr) -> PackageInfo: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)



## getPackageInfoPypi

[Show source in packageinfo.py:62](../../../licensecheck/packageinfo.py#L62)

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
def getPackageInfoPypi(requirement: ucstr) -> PackageInfo: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)



## getPackages

[Show source in packageinfo.py:119](../../../licensecheck/packageinfo.py#L119)

Get dependency info.

#### Arguments

----
 - `reqs` *set[ucstr]* - set of dependency names to gather info on

#### Returns

-------
 - `set[PackageInfo]` - set of dependencies

#### Signature

```python
def getPackages(reqs: set[ucstr]) -> set[PackageInfo]: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)



## licenseFromClassifierlist

[Show source in packageinfo.py:95](../../../licensecheck/packageinfo.py#L95)

Get license string from a list of project classifiers.

#### Arguments

----
 - `classifiers` *list[str]* - list of classifiers

#### Returns

-------
 - `str` - the license name

#### Signature

```python
def licenseFromClassifierlist(classifiers: list[str] | None | list[Any]) -> ucstr: ...
```

#### See also

- [ucstr](./types.md#ucstr)