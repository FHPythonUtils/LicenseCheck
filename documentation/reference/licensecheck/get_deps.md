# Get Deps

[Licensecheck Index](../README.md#licensecheck-index) / [Licensecheck](./index.md#licensecheck) / Get Deps

> Auto-generated documentation for [licensecheck.get_deps](../../../licensecheck/get_deps.py) module.

- [Get Deps](#get-deps)
  - [check](#check)
  - [resolve_requirements](#resolve_requirements)

## check

[Show source in get_deps.py:42](../../../licensecheck/get_deps.py#L42)

#### Signature

```python
def check(
    requirements_paths: list[str],
    groups: list[str],
    this_license: License,
    package_info_manager: PackageInfoManager,
    ignore_packages: list[ucstr] | None = None,
    fail_packages: list[ucstr] | None = None,
    ignore_licenses: list[ucstr] | None = None,
    fail_licenses: list[ucstr] | None = None,
    only_licenses: list[ucstr] | None = None,
    skip_dependencies: list[ucstr] | None = None,
) -> tuple[bool, set[PackageInfo]]: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfoManager](./packageinfo.md#packageinfomanager)
- [PackageInfo](./types.md#packageinfo)



## resolve_requirements

[Show source in get_deps.py:16](../../../licensecheck/get_deps.py#L16)

#### Signature

```python
def resolve_requirements(
    requirements_paths: list[str], groups: list[str], skip_dependencies: list[ucstr]
) -> set[ucstr]: ...
```

#### See also

- [ucstr](./types.md#ucstr)