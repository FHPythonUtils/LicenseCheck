# Types

[Licensecheck Index](../README.md#licensecheck-index) /
[Licensecheck](./index.md#licensecheck) /
Types

> Auto-generated documentation for [licensecheck.types](../../../licensecheck/types.py) module.

- [Types](#types)
  - [License](#license)
  - [PackageInfo](#packageinfo)

## License

[Show source in types.py:30](../../../licensecheck/types.py#L30)

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



## PackageInfo

[Show source in types.py:13](../../../licensecheck/types.py#L13)

PackageInfo type.

#### Signature

```python
class PackageInfo:
    ...
```


