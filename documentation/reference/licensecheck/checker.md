# Checker

[Licensecheck Index](../README.md#licensecheck-index) / [Licensecheck](./index.md#licensecheck) / Checker

> Auto-generated documentation for [licensecheck.checker](../../../licensecheck/checker.py) module.

- [Checker](#checker)
  - [check](#check)

## check

[Show source in checker.py:12](../../../licensecheck/checker.py#L12)

#### Signature

```python
def check(
    requirements_paths: list[str],
    groups: list[str],
    extras: list[str],
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