# Types

[Licensecheck Index](../README.md#licensecheck-index) /
[Licensecheck](./index.md#licensecheck) /
Types

> Auto-generated documentation for [licensecheck.types](../../../licensecheck/types.py) module.

- [Types](#types)
  - [License](#license)
  - [PackageCompat](#packagecompat)
  - [PackageInfo](#packageinfo)

## License

[Show source in types.py:27](../../../licensecheck/types.py#L27)

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


License Enum to hold a set of potential licenses.

#### Signature

```python
class License(Enum):
    ...
```



## PackageCompat

[Show source in types.py:21](../../../licensecheck/types.py#L21)

PackageCompat type.

#### Signature

```python
class PackageCompat(PackageInfo):
    ...
```

#### See also

- [PackageInfo](#packageinfo)



## PackageInfo

[Show source in types.py:9](../../../licensecheck/types.py#L9)

PackageInfo type.

#### Signature

```python
class PackageInfo(typing.TypedDict):
    ...
```


