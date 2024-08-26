# Native

[Licensecheck Index](../../README.md#licensecheck-index) / [Licensecheck](../index.md#licensecheck) / [Resolvers](./index.md#resolvers) / Native

> Auto-generated documentation for [licensecheck.resolvers.native](../../../../licensecheck/resolvers/native.py) module.

- [Native](#native)
  - [get_reqs](#get_reqs)

## get_reqs

[Show source in native.py:16](../../../../licensecheck/resolvers/native.py#L16)

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
def get_reqs(
    using: str,
    skipDependencies: list[ucstr],
    extras: list[str],
    pyproject: dict[str, Any],
    requirementsPaths: list[Path],
) -> set[ucstr]: ...
```

#### See also

- [ucstr](../types.md#ucstr)