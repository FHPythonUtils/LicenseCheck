# licensecheck

> Auto-generated documentation for [licensecheck](../../licensecheck/__init__.py) module.

Output the licenses used by dependencies and check if these are compatible...

- [Licensecheck](../README.md#licensecheck-index) / [Modules](../README.md#licensecheck-modules) / licensecheck
    - [cli](#cli)
    - [getDepsLicenses](#getdepslicenses)
    - Modules
        - [\_\_main\_\_](module.md#__main__)
        - [formatter](formatter.md#formatter)
        - [license_matrix](license_matrix.md#license_matrix)
        - [packagecompat](packagecompat.md#packagecompat)
        - [packageinfo](packageinfo.md#packageinfo)

with the project license

## cli

[[find in source code]](../../licensecheck/__init__.py#L80)

```python
def cli() -> None:
```

Cli entry point.

## getDepsLicenses

[[find in source code]](../../licensecheck/__init__.py#L36)

```python
def getDepsLicenses() -> list[PackageCompat]:
```

Get a list of packages with package compatibility.

#### Returns

- `list[PackageCompat]` - list of packages (python dicts)
