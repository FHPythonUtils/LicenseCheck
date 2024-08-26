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

[Show source in packageinfo.py:18](../../../licensecheck/packageinfo.py#L18)

Get a string from a key from pkgMetadata.

#### Signature

```python
def _pkgMetadataGet(
    pkgMetadata: metadata.PackageMetadata | dict[str, Any], key: str
) -> str: ...
```



## getModuleSize

[Show source in packageinfo.py:195](../../../licensecheck/packageinfo.py#L195)

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

[Show source in packageinfo.py:176](../../../licensecheck/packageinfo.py#L176)

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

[Show source in packageinfo.py:147](../../../licensecheck/packageinfo.py#L147)

Get the package classifiers and license from "setup.cfg", "pyproject.toml".

Returns
-------
 dict[str, Any]: {"classifiers": list[str], "license": ucstr}

#### Signature

```python
def getMyPackageMetadata() -> dict[str, Any]: ...
```



## getPackageInfoLocal

[Show source in packageinfo.py:26](../../../licensecheck/packageinfo.py#L26)

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

[Show source in packageinfo.py:63](../../../licensecheck/packageinfo.py#L63)

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

[Show source in packageinfo.py:122](../../../licensecheck/packageinfo.py#L122)

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

[Show source in packageinfo.py:98](../../../licensecheck/packageinfo.py#L98)

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