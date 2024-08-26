# Get Deps

[Licensecheck Index](../README.md#licensecheck-index) / [Licensecheck](./index.md#licensecheck) / Get Deps

> Auto-generated documentation for [licensecheck.get_deps](../../../licensecheck/get_deps.py) module.

- [Get Deps](#get-deps)
  - [getDepsWithLicenses](#getdepswithlicenses)
  - [getReqs](#getreqs)

## getDepsWithLicenses

[Show source in get_deps.py:75](../../../licensecheck/get_deps.py#L75)

Get a set of dependencies with licenses and determine license compatibility.

#### Arguments

----
 - `using` *str* - use requirements or poetry
 - `myLice` *License* - user license
 - `ignorePackages` *list[ucstr]* - a list of packages to ignore (compat=True)
 - `failPackages` *list[ucstr]* - a list of packages to fail (compat=False)
 - `ignoreLicenses` *list[ucstr]* - a list of licenses to ignore (skipped, compat may still be
 False)
 - `failLicenses` *list[ucstr]* - a list of licenses to fail (compat=False)
 - `onlyLicenses` *list[ucstr]* - a list of allowed licenses (any other license will fail)
 - `skipDependencies` *list[ucstr]* - a list of dependencies to skip (compat=False)

#### Returns

-------
 - `tuple[License,` *set[PackageInfo]]* - tuple of
  my package license
  set of updated dependencies with licenseCompat set

#### Signature

```python
def getDepsWithLicenses(
    using: str,
    myLice: License,
    ignorePackages: list[ucstr],
    failPackages: list[ucstr],
    ignoreLicenses: list[ucstr],
    failLicenses: list[ucstr],
    onlyLicenses: list[ucstr],
    skipDependencies: list[ucstr],
) -> set[PackageInfo]: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)



## getReqs

[Show source in get_deps.py:17](../../../licensecheck/get_deps.py#L17)

Get requirements for the end user project/ lib.

```python
>>> getReqs("poetry")
>>> getReqs("poetry:dev")
>>> getReqs("requirements")
>>> getReqs("requirements:requirements.txt;requirements-dev.txt")
>>> getReqs("PEP631")
>>> getReqs("PEP631:tests")
```

#### Arguments

----
 - `using` *str* - use requirements, poetry or PEP631.
 - `skipDependencies` *list[str]* - list of dependencies to skip.

#### Returns

-------
 - `set[str]` - set of requirement packages

#### Signature

```python
def getReqs(using: str, skipDependencies: list[ucstr]) -> set[ucstr]: ...
```

#### See also

- [ucstr](./types.md#ucstr)