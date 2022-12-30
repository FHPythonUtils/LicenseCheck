# Get Deps

[Licensecheck Index](../README.md#licensecheck-index) /
[Licensecheck](./index.md#licensecheck) /
Get Deps

> Auto-generated documentation for [licensecheck.get_deps](../../../licensecheck/get_deps.py) module.

- [Get Deps](#get-deps)
  - [getDepsWithLicenses](#getdepswithlicenses)
  - [getReqs](#getreqs)

## getDepsWithLicenses

[Show source in get_deps.py:90](../../../licensecheck/get_deps.py#L90)

Get a set of dependencies with licenses and determine license compatibility.

#### Arguments

- `using` *str* - use requirements or poetry
- `ignorePackages` *list[str]* - a list of packages to ignore (compat=True)
- `failPackages` *list[str]* - a list of packages to fail (compat=False)
- `ignoreLicenses` *list[str]* - a list of licenses to ignore (skipped, compat may still be False)
- `failLicenses` *list[str]* - a list of licenses to fail (compat=False)

#### Returns

- `set[PackageInfo]` - set of updated dependencies with licenseCompat set

#### Signature

```python
def getDepsWithLicenses(
    using: str,
    ignorePackages: list[str],
    failPackages: list[str],
    ignoreLicenses: list[str],
    failLicenses: list[str],
) -> set[PackageInfo]:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)



## getReqs

[Show source in get_deps.py:41](../../../licensecheck/get_deps.py#L41)

Get requirements for the end user project/ lib.

```python
>>> getReqs("poetry")
>>> getReqs("poetry:dev")
>>> getReqs("requirements")
>>> getReqs("requirements:requirements.txt;requirements-dev.txt")
```

#### Arguments

- `using` *str* - use requirements or poetry.

#### Returns

- `set[str]` - set of requirement packages

#### Signature

```python
def getReqs(using: str) -> set[str]:
    ...
```


