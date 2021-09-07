# get_deps

> Auto-generated documentation for [licensecheck.get_deps](../../licensecheck/get_deps.py) module.

Get a list of packages with package compatibility.

- [Licensecheck](../README.md#licensecheck-index) / [Modules](../README.md#licensecheck-modules) / [licensecheck](index.md#licensecheck) / get_deps
    - [getDepsWLicenses](#getdepswlicenses)
    - [getReqs](#getreqs)

## getDepsWLicenses

[[find in source code]](../../licensecheck/get_deps.py#L85)

```python
def getDepsWLicenses(
    using: str,
    ignorePackages: list[str],
    failPackages: list[str],
    ignoreLicenses: list[str],
    failLicenses: list[str],
) -> list[PackageCompat]:
```

Get a list of dependencies with licenses and determin license compatibility.

#### Arguments

- `using` *str* - use requirements or poetry
- `ignorePackages` *list[str]* - a list of packages to ignore (compat=True)
- `failPackages` *list[str]* - a list of packages to fail (compat=False)
- `ignoreLicenses` *list[str]* - a list of licenses to ignore (skipped, compat may still be False)
- `failLicenses` *list[str]* - a list of licenses to fail (compat=False)

#### Returns

- `list[PackageCompat]` - list of packagecompat types: dependency info + licence compat

## getReqs

[[find in source code]](../../licensecheck/get_deps.py#L41)

```python
def getReqs(using: str) -> list[str]:
```

Get requirements for the end user project/ lib.

#### Arguments

- `using` *str* - use requirements or poetry

#### Returns

- `list[str]` - list of requirement packages
