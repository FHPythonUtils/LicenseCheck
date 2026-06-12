# Types

[Licensecheck Index](../README.md#licensecheck-index) / [Licensecheck](./index.md#licensecheck) / Types

> Auto-generated documentation for [licensecheck.types](../../../licensecheck/types.py) module.

- [Types](#types)
  - [License](#license)
  - [PackageInfo](#packageinfo)
    - [PackageInfo().__post_init__](#packageinfo()__post_init__)
    - [PackageInfo().get_filtered_dict](#packageinfo()get_filtered_dict)
  - [ucstr](#ucstr)
    - [ucstr().__new__](#ucstr()__new__)

## License

[Show source in types.py:60](../../../licensecheck/types.py#L60)

#### Attributes

- `PUBLIC` - Public domain: 0

- `MIT` - Permissive GPL compatible: 10

- `APACHE` - Other permissive: 20

- `LGPL_X` - LGPL: 30

- `GPL_X` - GPL: 40

- `AGPL_3_PLUS` - AGPL: 50

- `MPL` - Other copyleft: 60

- `PROPRIETARY` - PROPRIETARY: 190

- `NO_LICENSE` - No License: 200


License Enum to hold a set of potential licenses.

#### Signature

```python
class License(Enum): ...
```



## PackageInfo

[Show source in types.py:30](../../../licensecheck/types.py#L30)

PackageInfo type.

#### Signature

```python
class PackageInfo: ...
```

### PackageInfo().__post_init__

[Show source in types.py:43](../../../licensecheck/types.py#L43)

Set the namever once the object is initialised.

#### Signature

```python
def __post_init__(self) -> None: ...
```

### PackageInfo().get_filtered_dict

[Show source in types.py:47](../../../licensecheck/types.py#L47)

Return a filtered dictionary of the object.

:param list[ucstr] hide_output_parameters: list of parameters to ignore

#### Returns

Type: *dict*
filtered dictionary

#### Signature

```python
def get_filtered_dict(self, hide_output_parameters: list[ucstr]) -> dict: ...
```

#### See also

- [ucstr](#ucstr)



## ucstr

[Show source in types.py:9](../../../licensecheck/types.py#L9)

Uppercase string.

#### Signature

```python
class ucstr(str): ...
```

### ucstr().__new__

[Show source in types.py:14](../../../licensecheck/types.py#L14)

Create a new ucstr from a str.

#### Arguments

- `v` *str* - string to cast

#### Returns

Type: *ucstr*
uppercase string.

#### Signature

```python
def __new__(cls, v: str | None): ...
```