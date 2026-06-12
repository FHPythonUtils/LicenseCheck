# Native

[Licensecheck Index](../../README.md#licensecheck-index) / [Licensecheck](../index.md#licensecheck) / [Resolvers](./index.md#resolvers) / Native

> Auto-generated documentation for [licensecheck.resolvers.native](../../../../licensecheck/resolvers/native.py) module.

- [Native](#native)
  - [do_get_reqs](#do_get_reqs)
  - [get_reqs](#get_reqs)

## do_get_reqs

[Show source in native.py:46](../../../../licensecheck/resolvers/native.py#L46)

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
) -> set[PackageInfo]: ...
```

#### See also

- [PackageInfo](../types.md#packageinfo)
- [ucstr](../types.md#ucstr)



## get_reqs

[Show source in native.py:17](../../../../licensecheck/resolvers/native.py#L17)

#### Signature

```python
def get_reqs(
    skipDependencies: list[ucstr],
    extras: list[str],
    requirementsPaths: list[Path],
    pyproject: dict[str, Any],
) -> set[PackageInfo]: ...
```

#### See also

- [PackageInfo](../types.md#packageinfo)
- [ucstr](../types.md#ucstr)