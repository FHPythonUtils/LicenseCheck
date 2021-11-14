# types

> Auto-generated documentation for [licensecheck.types](../../licensecheck/types.py) module.

PackageCompat type.

- [Licensecheck](../README.md#licensecheck-index) / [Modules](../README.md#licensecheck-modules) / [licensecheck](index.md#licensecheck) / types
    - [License](#license)
    - [PackageCompat](#packagecompat)
    - [PackageInfo](#packageinfo)

## License

[[find in source code]](../../licensecheck/types.py#L27)

```python
class License(Enum):
```

License Enum to hold a set of potential licenses.

#### Attributes

- `PUBLIC` - Public domain: `0`
- `MIT` - Permissive GPL compatible: `10`
- `APACHE` - Other permissive: `20`
- `LGPL_X` - LGPL: `30`
- `GPL_X` - GPL: `40`
- `AGPL_3_PLUS` - AGPL: `50`
- `MPL` - Other copyleft: `60`
- `PROPRIETARY` - PROPRIETARY: `190`
- `NO_LICENSE` - No License: `200`

## PackageCompat

[[find in source code]](../../licensecheck/types.py#L21)

```python
class PackageCompat(PackageInfo):
```

PackageCompat type.

#### See also

- [PackageInfo](#packageinfo)

## PackageInfo

[[find in source code]](../../licensecheck/types.py#L9)

```python
class PackageInfo(typing.TypedDict):
```

PackageInfo type.
