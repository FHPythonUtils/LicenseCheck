# Uv

[Licensecheck Index](../../README.md#licensecheck-index) / [Licensecheck](../index.md#licensecheck) / [Resolvers](./index.md#resolvers) / Uv

> Auto-generated documentation for [licensecheck.resolvers.uv](../../../../licensecheck/resolvers/uv.py) module.

- [Uv](#uv)
  - [get_reqs](#get_reqs)

## get_reqs

[Show source in uv.py:15](../../../../licensecheck/resolvers/uv.py#L15)

#### Signature

```python
def get_reqs(
    skipDependencies: list[ucstr],
    groups: list[str],
    extras: list[str],
    requirementsPaths: list[str],
    index_url: str = "https://pypi.org/simple",
) -> set[PackageInfo]: ...
```

#### See also

- [PackageInfo](../types.md#packageinfo)
- [ucstr](../types.md#ucstr)