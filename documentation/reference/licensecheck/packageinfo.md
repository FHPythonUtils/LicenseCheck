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

[Show source in packageinfo.py:75](../../../licensecheck/packageinfo.py#L75)

Handles retrieval of package info from local installation.

#### Signature

```python
class LocalPackageInfo: ...
```

### LocalPackageInfo.get_info

[Show source in packageinfo.py:78](../../../licensecheck/packageinfo.py#L78)

Retrieve package metadata from local installation.

#### Arguments

- `package` *ucstr* - Package name.

#### Returns

Type: *PackageInfo*
Local package information.

#### Signature

```python
@staticmethod
def get_info(package: ucstr) -> PackageInfo: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)

### LocalPackageInfo.get_size

[Show source in packageinfo.py:104](../../../licensecheck/packageinfo.py#L104)

Retrieve installed package size.

#### Arguments

- `package` *ucstr* - Package name.

#### Returns

Type: *int*
Size in bytes.

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

[Show source in packageinfo.py:34](../../../licensecheck/packageinfo.py#L34)

Retrieve package information from local installation or PyPI.

:param set[ucstr] reqs: Set of dependency names to retrieve information for.

#### Returns

Type: *set[PackageInfo]*
A set of package information objects.

#### Signature

```python
def getPackages(self, reqs: set[ucstr]) -> set[PackageInfo]: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)

### PackageInfoManager().get_package_info

[Show source in packageinfo.py:48](../../../licensecheck/packageinfo.py#L48)

Retrieve package information, preferring local data.

#### Arguments

- `pacage` *ucstr* - Package name.

#### Returns

Type: *PackageInfo*
Information about the package.

#### Signature

```python
def get_package_info(self, package: ucstr) -> PackageInfo: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)



## ProjectMetadata

[Show source in packageinfo.py:192](../../../licensecheck/packageinfo.py#L192)

Handles extraction of project metadata from configuration files.

#### Signature

```python
class ProjectMetadata: ...
```

### ProjectMetadata.get_license

[Show source in packageinfo.py:220](../../../licensecheck/packageinfo.py#L220)

Extract license from project metadata.

#### Returns

Type: *ucstr*
License string.

#### Signature

```python
@staticmethod
def get_license() -> ucstr: ...
```

#### See also

- [ucstr](./types.md#ucstr)

### ProjectMetadata.get_metadata

[Show source in packageinfo.py:195](../../../licensecheck/packageinfo.py#L195)

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

[Show source in packageinfo.py:115](../../../licensecheck/packageinfo.py#L115)

Handles retrieval of package info from PyPI.

#### Signature

```python
class RemotePackageInfo: ...
```

### RemotePackageInfo.get_info

[Show source in packageinfo.py:118](../../../licensecheck/packageinfo.py#L118)

Retrieve package metadata from PyPI.

#### Arguments

- `package` *ucstr* - Package name.
- `pypi_api` *str* - PyPI API base URL.

#### Returns

Type: *PackageInfo*
Remote package information.

#### Signature

```python
@staticmethod
def get_info(package: ucstr, pypi_api: str) -> PackageInfo: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)

### RemotePackageInfo.get_size

[Show source in packageinfo.py:148](../../../licensecheck/packageinfo.py#L148)

Retrieve package size from PyPI metadata.

:param dict[str, Any] data: PyPI response JSON.

#### Returns

Type: *int*
Package size in bytes.

#### Signature

```python
@staticmethod
def get_size(data: dict[str, Any]) -> int: ...
```



## from_classifiers

[Show source in packageinfo.py:173](../../../licensecheck/packageinfo.py#L173)

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

[Show source in packageinfo.py:160](../../../licensecheck/packageinfo.py#L160)

Retrieve metadata value safely.

:param metadata.PackageMetadata | dict[str, Any] metadata_obj: Metadata source.

#### Arguments

- `key` *str* - Metadata key.

#### Returns

Type: *str*
Retrieved metadata value.

#### Signature

```python
def meta_get(
    metadata_obj: metadata.PackageMetadata | dict[str, Any], key: str
) -> str: ...
```