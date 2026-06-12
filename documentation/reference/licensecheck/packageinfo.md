# Packageinfo

[Licensecheck Index](../README.md#licensecheck-index) / [Licensecheck](./index.md#licensecheck) / Packageinfo

> Auto-generated documentation for [licensecheck.packageinfo](../../../licensecheck/packageinfo.py) module.

- [Packageinfo](#packageinfo)
  - [LocalPackageInfo](#localpackageinfo)
    - [LocalPackageInfo().get_author](#localpackageinfo()get_author)
    - [LocalPackageInfo().get_homePage](#localpackageinfo()get_homepage)
    - [LocalPackageInfo().get_license](#localpackageinfo()get_license)
    - [LocalPackageInfo().get_name](#localpackageinfo()get_name)
    - [LocalPackageInfo().get_size](#localpackageinfo()get_size)
    - [LocalPackageInfo().get_version](#localpackageinfo()get_version)
  - [PackageInfoManager](#packageinfomanager)
    - [PackageInfoManager().getPackages](#packageinfomanager()getpackages)
    - [PackageInfoManager().get_package_info](#packageinfomanager()get_package_info)
    - [PackageInfoManager().resolve_requirements](#packageinfomanager()resolve_requirements)
  - [ProjectMetadata](#projectmetadata)
    - [ProjectMetadata.get_license](#projectmetadataget_license)
    - [ProjectMetadata.get_metadata](#projectmetadataget_metadata)
  - [RemotePackageInfo](#remotepackageinfo)
    - [RemotePackageInfo().get_author](#remotepackageinfo()get_author)
    - [RemotePackageInfo().get_homePage](#remotepackageinfo()get_homepage)
    - [RemotePackageInfo().get_license](#remotepackageinfo()get_license)
    - [RemotePackageInfo().get_name](#remotepackageinfo()get_name)
    - [RemotePackageInfo().get_size](#remotepackageinfo()get_size)
    - [RemotePackageInfo().get_version](#remotepackageinfo()get_version)
    - [RemotePackageInfo().make_req](#remotepackageinfo()make_req)
    - [RemotePackageInfo().poke_pypi](#remotepackageinfo()poke_pypi)
  - [from_classifiers](#from_classifiers)
  - [meta_get](#meta_get)

## LocalPackageInfo

[Show source in packageinfo.py:126](../../../licensecheck/packageinfo.py#L126)

Handles retrieval of package info from local installation.

#### Signature

```python
class LocalPackageInfo:
    def __init__(self, package: PackageInfo) -> None: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)

### LocalPackageInfo().get_author

[Show source in packageinfo.py:153](../../../licensecheck/packageinfo.py#L153)

#### Signature

```python
def get_author(self) -> str | None: ...
```

### LocalPackageInfo().get_homePage

[Show source in packageinfo.py:150](../../../licensecheck/packageinfo.py#L150)

#### Signature

```python
def get_homePage(self) -> str | None: ...
```

### LocalPackageInfo().get_license

[Show source in packageinfo.py:137](../../../licensecheck/packageinfo.py#L137)

#### Signature

```python
def get_license(self) -> str | None: ...
```

### LocalPackageInfo().get_name

[Show source in packageinfo.py:144](../../../licensecheck/packageinfo.py#L144)

#### Signature

```python
def get_name(self) -> str | None: ...
```

### LocalPackageInfo().get_size

[Show source in packageinfo.py:156](../../../licensecheck/packageinfo.py#L156)

Retrieve installed package size.

#### Arguments

- `package` *ucstr* - Package name.

#### Returns

Type: *int*
Size in bytes.

#### Signature

```python
def get_size(self) -> int: ...
```

### LocalPackageInfo().get_version

[Show source in packageinfo.py:147](../../../licensecheck/packageinfo.py#L147)

#### Signature

```python
def get_version(self) -> str | None: ...
```



## PackageInfoManager

[Show source in packageinfo.py:28](../../../licensecheck/packageinfo.py#L28)

Manages retrieval of local and remote package information.

#### Signature

```python
class PackageInfoManager:
    def __init__(self, base_pypi_url: str = "https://pypi.org") -> None: ...
```

### PackageInfoManager().getPackages

[Show source in packageinfo.py:73](../../../licensecheck/packageinfo.py#L73)

Retrieve package information from local installation or PyPI.

:param set[ucstr] reqs: Set of dependency names to retrieve information for.

#### Returns

Type: *set[PackageInfo]*
A set of package information objects.

#### Signature

```python
def getPackages(self) -> set[PackageInfo]: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)

### PackageInfoManager().get_package_info

[Show source in packageinfo.py:87](../../../licensecheck/packageinfo.py#L87)

Retrieve package information, preferring local data.

#### Arguments

- `pacage` *ucstr* - Package name.

#### Returns

Type: *PackageInfo*
Information about the package.

#### Signature

```python
def get_package_info(self, package: PackageInfo) -> PackageInfo: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)

### PackageInfoManager().resolve_requirements

[Show source in packageinfo.py:41](../../../licensecheck/packageinfo.py#L41)

#### Signature

```python
def resolve_requirements(
    self,
    requirements_paths: list[str],
    groups: list[str],
    extras: list[str],
    skip_dependencies: list[ucstr],
) -> None: ...
```

#### See also

- [ucstr](./types.md#ucstr)



## ProjectMetadata

[Show source in packageinfo.py:277](../../../licensecheck/packageinfo.py#L277)

Handles extraction of project metadata from configuration files.

#### Signature

```python
class ProjectMetadata: ...
```

### ProjectMetadata.get_license

[Show source in packageinfo.py:305](../../../licensecheck/packageinfo.py#L305)

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

[Show source in packageinfo.py:280](../../../licensecheck/packageinfo.py#L280)

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

[Show source in packageinfo.py:169](../../../licensecheck/packageinfo.py#L169)

Handles retrieval of package info from PyPI.

#### Signature

```python
class RemotePackageInfo:
    def __init__(self, pypi_api: str, package: PackageInfo) -> None: ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)

### RemotePackageInfo().get_author

[Show source in packageinfo.py:227](../../../licensecheck/packageinfo.py#L227)

#### Signature

```python
def get_author(self) -> str | None: ...
```

### RemotePackageInfo().get_homePage

[Show source in packageinfo.py:223](../../../licensecheck/packageinfo.py#L223)

#### Signature

```python
def get_homePage(self) -> str | None: ...
```

### RemotePackageInfo().get_license

[Show source in packageinfo.py:207](../../../licensecheck/packageinfo.py#L207)

#### Signature

```python
def get_license(self) -> str | None: ...
```

### RemotePackageInfo().get_name

[Show source in packageinfo.py:215](../../../licensecheck/packageinfo.py#L215)

#### Signature

```python
def get_name(self) -> str | None: ...
```

### RemotePackageInfo().get_size

[Show source in packageinfo.py:231](../../../licensecheck/packageinfo.py#L231)

Retrieve package size from PyPI metadata.

:param dict[str, Any] data: PyPI response JSON.

#### Returns

Type: *int*
Package size in bytes.

#### Signature

```python
def get_size(self) -> int: ...
```

### RemotePackageInfo().get_version

[Show source in packageinfo.py:219](../../../licensecheck/packageinfo.py#L219)

#### Signature

```python
def get_version(self) -> str | None: ...
```

### RemotePackageInfo().make_req

[Show source in packageinfo.py:191](../../../licensecheck/packageinfo.py#L191)

#### Signature

```python
def make_req(self, url: str) -> dict: ...
```

### RemotePackageInfo().poke_pypi

[Show source in packageinfo.py:178](../../../licensecheck/packageinfo.py#L178)

#### Signature

```python
def poke_pypi(self) -> None: ...
```



## from_classifiers

[Show source in packageinfo.py:258](../../../licensecheck/packageinfo.py#L258)

Extract license from classifiers.

:param list[str] | None classifiers: list of classifiers

#### Returns

Type: *ucstr*
licenses as a ucstr

#### Signature

```python
def from_classifiers(classifiers: list[str] | None) -> str | None: ...
```



## meta_get

[Show source in packageinfo.py:245](../../../licensecheck/packageinfo.py#L245)

Retrieve metadata value safely.

:param Message | dict[str, Any] self.meta: Metadata source.

#### Arguments

- `key` *str* - Metadata key.

#### Returns

Type: *str*
Retrieved metadata value.

#### Signature

```python
def meta_get(meta: Message | dict[str, Any], key: str) -> str | None: ...
```