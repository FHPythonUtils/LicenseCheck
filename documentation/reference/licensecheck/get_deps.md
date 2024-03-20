# Get Deps

[Licensecheck Index](../README.md#licensecheck-index) / [Licensecheck](./index.md#licensecheck) / Get Deps

> Auto-generated documentation for [licensecheck.get_deps](../../../licensecheck/get_deps.py) module.

- [Get Deps](#get-deps)
  - [do_get_reqs](#do_get_reqs)
  - [getDepsWithLicenses](#getdepswithlicenses)
  - [getReqs](#getreqs)

## do_get_reqs

[Show source in get_deps.py:65](../../../licensecheck/get_deps.py#L65)

Underlying machineary to get requirements.

#### Arguments

----
 - `using` *str* - use requirements, poetry or PEP631.
 - `skipDependencies` *list[str]* - list of dependencies to skip.
 extras (str | None): to-do
 pyproject (dict[str, Any]): to-do
 - `requirementsPaths` *list[Path]* - to-do

#### Returns

-------
 - `set[str]` - set of requirement packages

#### Signature

```python
def do_get_reqs(
    using: str,
    skipDependencies: list[ucstr],
    extras: list[str],
    pyproject: dict[str, Any],
    requirementsPaths: list[Path],
) -> set[ucstr]: ...
```

#### See also

- [ucstr](./types.md#ucstr)



## getDepsWithLicenses

[Show source in get_deps.py:188](../../../licensecheck/get_deps.py#L188)

Get a set of dependencies with licenses and determine license compatibility.

#### Arguments

----
 - `using` *str* - use requirements or poetry
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
    ignorePackages: list[ucstr],
    failPackages: list[ucstr],
    ignoreLicenses: list[ucstr],
    failLicenses: list[ucstr],
    onlyLicenses: list[ucstr],
    skipDependencies: list[ucstr],
) -> tuple[License, set[PackageInfo]]: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)
- [ucstr](./types.md#ucstr)



## getReqs

[Show source in get_deps.py:22](../../../licensecheck/get_deps.py#L22)

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