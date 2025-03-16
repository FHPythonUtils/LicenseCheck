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

[Show source in packageinfo.py:77](../../../licensecheck/packageinfo.py#L77)

Handles retrieval of package info from local installation.

#### Signature

```python
class LocalPackageInfo: ...
```

### LocalPackageInfo.get_info

[Show source in packageinfo.py:80](../../../licensecheck/packageinfo.py#L80)

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

[Show source in packageinfo.py:106](../../../licensecheck/packageinfo.py#L106)

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
    def __init__(self, base_pypi_url: str = "https://pypi.org") -> None: ...
```

### PackageInfoManager().getPackages

[Show source in packageinfo.py:36](../../../licensecheck/packageinfo.py#L36)

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

[Show source in packageinfo.py:50](../../../licensecheck/packageinfo.py#L50)

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

[Show source in packageinfo.py:194](../../../licensecheck/packageinfo.py#L194)

Handles extraction of project metadata from configuration files.

#### Signature

```python
class ProjectMetadata: ...
```

### ProjectMetadata.get_license

[Show source in packageinfo.py:222](../../../licensecheck/packageinfo.py#L222)

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

[Show source in packageinfo.py:197](../../../licensecheck/packageinfo.py#L197)

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

[Show source in packageinfo.py:117](../../../licensecheck/packageinfo.py#L117)

Handles retrieval of package info from PyPI.

#### Signature

```python
class RemotePackageInfo: ...
```

### RemotePackageInfo.get_info

[Show source in packageinfo.py:120](../../../licensecheck/packageinfo.py#L120)

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

[Show source in packageinfo.py:150](../../../licensecheck/packageinfo.py#L150)

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

[Show source in packageinfo.py:175](../../../licensecheck/packageinfo.py#L175)

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

[Show source in packageinfo.py:162](../../../licensecheck/packageinfo.py#L162)

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