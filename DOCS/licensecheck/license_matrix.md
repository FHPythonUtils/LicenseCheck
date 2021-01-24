# license_matrix

> Auto-generated documentation for [licensecheck.license_matrix](../../licensecheck/license_matrix.py) module.

Define a foss compatability license_matrix

- [Licensecheck](../README.md#licensecheck-index) / [Modules](../README.md#licensecheck-modules) / [licensecheck](index.md#licensecheck) / license_matrix
    - [License](#license)
    - [depCompatibleLice](#depcompatiblelice)
    - [licenseType](#licensetype)

Standard disclaimer:: I am not a lawyer and there is no guarentee that the
information provided here is complete or correct. Do not take this as legal
advice on foss license compatability

https://en.wikipedia.org/wiki/IANAL

Types of license/ compatability

Public Domain
- Unlicense

Permissive Compatible
Permissive license compatible with gpl
- Mit
- Boost
- Bsd
- Isc
- Ncsa

Permissive Not Compatible
Permissive license NOT compatible with gpl
- Apache
- Eclipse
- Acedemic Free

Copyleft
permissive -> lgpl 2.1 -> gpl 2
permissive -> lgpl 3 -> gpl 3 -> agpl
permissive -> mpl -> gpl -> agpl (3 only)

permissive (any) -> EU
EU -> gpl -> agpl (3 only)

#### Attributes

- `PERMISSIVE` - Permissive licenses compatible with GPL: `[License.MIT, License.BOOST, License.BSD, License.ISC, License.NCSA]`
- `PERMISSIVE_OTHER` - Permissive licenses NOT compatible with GPL: `[License.APACHE, License.ECLIPSE, License.ACEDEMIC_FREE]`
- `LGPL` - LGPL licenses: `[License.LGPL_2, License.LGPL_3, License.LGPL_2...`
- `GPL` - GPL licenses (including AGPL): `[License.GPL_2, License.GPL_3, License.GPL_2_PL...`
- `OTHER_COPYLEFT` - Other Copyleft licenses: `[License.MPL, License.EU]`
- `UNLICENSEE_INCOMPATIBLE` - Basic compat matrix: `PERMISSIVE + PERMISSIVE_OTHER + GPL + LGPL + OT...`
- `GPL_2_INCOMPATIBLE` - GPL compat matrix
  https://www.gnu.org/licenses/gpl-faq.html#AllCompatibility: `[License.GPL_3, License.GPL_3_PLUS, License.LGPL_3, License.LGPL_3_PLUS]`

## License

[[find in source code]](../../licensecheck/license_matrix.py#L43)

```python
class License(Enum):
```

License Enum to hold a set of potential licenses

#### Attributes

- `PUBLIC` - Public domain: `0`
- `MIT` - Permissive GPL compatible: `10`
- `APACHE` - Other permissive: `20`
- `LGPL_X` - LGPL: `30`
- `GPL_X` - GPL: `40`
- `AGPL_3_PLUS` - AGPL: `50`
- `MPL` - Other copyleft: `60`
- `NO_LICENSE` - No License: `200`

## depCompatibleLice

[[find in source code]](../../licensecheck/license_matrix.py#L174)

```python
def depCompatibleLice(myLicense: License, depLice: list[License]) -> bool:
```

Identify if the end user license is compatible with the dependency
license(s)

#### Arguments

- `myLicense` *License* - end user license to check
- `depLice` *list[License]* - dependency license

#### Returns

- `bool` - True if compatible, otherwise False

#### See also

- [License](#license)

## licenseType

[[find in source code]](../../licensecheck/license_matrix.py#L80)

```python
def licenseType(lice: str) -> list[License]:
```

Return a list of license types from a license string

#### Arguments

- `lice` *str* - license name

#### Returns

- `list[License]` - the license
