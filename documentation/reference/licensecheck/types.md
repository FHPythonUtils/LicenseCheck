# Types

[Licensecheck Index](../README.md#licensecheck-index) /
[Licensecheck](./index.md#licensecheck) /
Types

> Auto-generated documentation for [licensecheck.types](../../../licensecheck/types.py) module.

- [Types](#types)
  - [License](#license)
  - [PackageInfo](#packageinfo)
  - [ucstr](#ucstr)
  - [printLicense](#printlicense)

## License

[Show source in types.py:45](../../../licensecheck/types.py#L45)

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

[Show source in types.py:28](../../../licensecheck/types.py#L28)

PackageInfo type.

#### Signature

```python
class PackageInfo:
    ...
```



## ucstr

[Show source in types.py:16](../../../licensecheck/types.py#L16)

Uppercase string

#### Signature

```python
class ucstr(str):
    ...
```



## printLicense

[Show source in types.py:88](../../../licensecheck/types.py#L88)

Output a license as plain text

#### Arguments

- `licenseEnum` *L* - License

#### Returns

Type: *str*
license of plain text

#### Signature

```python
def printLicense(licenseEnum: L) -> str:
    ...
```

#### See also

- [L](#l)


