# Packageinfo

[Licensecheck Index](../README.md#licensecheck-index) / [Licensecheck](./index.md#licensecheck) / Packageinfo

> Auto-generated documentation for [licensecheck.packageinfo](../../../licensecheck/packageinfo.py) module.

- [Packageinfo](#packageinfo)
  - [LocalPackageInfo](#localpackageinfo)
    - [LocalPackageInfo.get_info](#localpackageinfoget_info)
    - [LocalPackageInfo.get_size](#localpackageinfoget_size)
  - [PackageInfoManager](#packageinfomanager)
    - [PackageInfoManager().getPackages](#packageinfomanager()getpackages)
    - [PackageInfoManager().get_package_info](#packageinfomanager()get_package_info)
  - [ProjectMetadata](#projectmetadata)
    - [ProjectMetadata.get_license](#projectmetadataget_license)
    - [ProjectMetadata.get_metadata](#projectmetadataget_metadata)
  - [RemotePackageInfo](#remotepackageinfo)
    - [RemotePackageInfo.get_info](#remotepackageinfoget_info)
    - [RemotePackageInfo.get_size](#remotepackageinfoget_size)
  - [from_classifiers](#from_classifiers)
  - [meta_get](#meta_get)

## LocalPackageInfo

[Show source in packageinfo.py:80](../../../licensecheck/packageinfo.py#L80)

Handles retrieval of package info from local installation.

#### Signature

```python
class LocalPackageInfo: ...
```

### LocalPackageInfo.get_info

[Show source in packageinfo.py:83](../../../licensecheck/packageinfo.py#L83)

Retrieve package metadata from local installation.

#### Arguments

- `package` *ucstr* - Package name.

#### Raises

- `ModuleNotFoundError` - If the package is not found locally.

#### Returns

- `PackageInfo` - Local package information.

#### Signature

```python
@staticmethod
def get_info(package: ucstr) -> PackageInfo: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)

### LocalPackageInfo.get_size

[Show source in packageinfo.py:116](../../../licensecheck/packageinfo.py#L116)

Retrieve installed package size.

#### Arguments

- `package` *ucstr* - Package name.

#### Returns

- `int` - Size in bytes.

#### Signature

```python
@staticmethod
def get_size(package: ucstr) -> int: ...
```

#### See also

- [ucstr](./types.md#ucstr)



## PackageInfoManager

[Show source in packageinfo.py:23](../../../licensecheck/packageinfo.py#L23)

Manages retrieval of local and remote package information.

#### Signature

```python
class PackageInfoManager:
    def __init__(self, pypi_api: str = "https://pypi.org/pypi/") -> None: ...
```

### PackageInfoManager().getPackages

[Show source in packageinfo.py:29](../../../licensecheck/packageinfo.py#L29)

Retrieve package information from local installation or PyPI.

#### Arguments

- `reqs` *set[ucstr]* - Set of dependency names to retrieve information for.

#### Returns

- `set[PackageInfo]` - A set of package information objects.

#### Signature

```python
def getPackages(self, reqs: set[ucstr]) -> set[PackageInfo]: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)

### PackageInfoManager().get_package_info

[Show source in packageinfo.py:47](../../../licensecheck/packageinfo.py#L47)

Retrieve package information, preferring local data.

#### Arguments

- `package` *ucstr* - Package name.

#### Returns

- `PackageInfo` - Information about the package.

#### Signature

```python
def get_package_info(self, package: ucstr) -> PackageInfo: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)



## ProjectMetadata

[Show source in packageinfo.py:222](../../../licensecheck/packageinfo.py#L222)

Handles extraction of project metadata from configuration files.

#### Signature

```python
class ProjectMetadata: ...
```

### ProjectMetadata.get_license

[Show source in packageinfo.py:250](../../../licensecheck/packageinfo.py#L250)

Extract license from project metadata.

#### Returns

- `ucstr` - License string.

#### Signature

```python
@staticmethod
def get_license() -> ucstr: ...
```

#### See also

- [ucstr](./types.md#ucstr)

### ProjectMetadata.get_metadata

[Show source in packageinfo.py:225](../../../licensecheck/packageinfo.py#L225)

Extract project metadata from setup.cfg or pyproject.toml.

#### Returns

Type: *dict[str, Any]*
Extracted metadata.

#### Signature

```python
@staticmethod
def get_metadata() -> dict[str, Any]: ...
```



## RemotePackageInfo

[Show source in packageinfo.py:131](../../../licensecheck/packageinfo.py#L131)

Handles retrieval of package info from PyPI.

#### Signature

```python
class RemotePackageInfo: ...
```

### RemotePackageInfo.get_info

[Show source in packageinfo.py:134](../../../licensecheck/packageinfo.py#L134)

Retrieve package metadata from PyPI.

#### Arguments

- `package` *ucstr* - Package name.
- `pypi_api` *str* - PyPI API base URL.

#### Raises

- `ModuleNotFoundError` - If package is not found.

#### Returns

- `PackageInfo` - Remote package information.

#### Signature

```python
@staticmethod
def get_info(package: ucstr, pypi_api: str) -> PackageInfo: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)

### RemotePackageInfo.get_size

[Show source in packageinfo.py:171](../../../licensecheck/packageinfo.py#L171)

Retrieve package size from PyPI metadata.

#### Arguments

data (dict[str, Any]): PyPI response JSON.

#### Returns

- `int` - Package size in bytes.

#### Signature

```python
@staticmethod
def get_size(data: dict[str, Any]) -> int: ...
```



## from_classifiers

[Show source in packageinfo.py:203](../../../licensecheck/packageinfo.py#L203)

Extract license from classifiers.

:param list[str] | None classifiers: list of classifiers

#### Returns

Type: *ucstr*
licenses as a ucstr

#### Signature

```python
def from_classifiers(classifiers: list[str] | None) -> ucstr: ...
```

#### See also

- [ucstr](./types.md#ucstr)



## meta_get

[Show source in packageinfo.py:186](../../../licensecheck/packageinfo.py#L186)

Retrieve metadata value safely.

#### Arguments

metadata_obj (metadata.PackageMetadata | dict[str, Any]): Metadata source.
- `key` *str* - Metadata key.

#### Returns

- `str` - Retrieved metadata value.

#### Signature

```python
def meta_get(
    metadata_obj: metadata.PackageMetadata | dict[str, Any], key: str
) -> str: ...
```