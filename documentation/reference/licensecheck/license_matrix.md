# License Matrix

[Licensecheck Index](../README.md#licensecheck-index) /
[Licensecheck](./index.md#licensecheck) /
License Matrix

> Auto-generated documentation for [licensecheck.license_matrix](../../../licensecheck/license_matrix.py) module.

#### Attributes

- `PERMISSIVE` - Permissive licenses compatible with GPL: `[L.MIT, L.BOOST, L.BSD, L.ISC, L.NCSA, L.PSFL]`

- `PERMISSIVE_OTHER` - Permissive licenses NOT compatible with GPL: `[L.APACHE, L.ECLIPSE, L.ACADEMIC_FREE]`

- `LGPL` - LGPL licenses: `[L.LGPL_2, L.LGPL_3, L.LGPL_2_PLUS, L.LGPL_3_PLUS, L.LGPL_X]`

- `GPL` - GPL licenses (including AGPL): `[L.GPL_2, L.GPL_3, L.GPL_2_PLUS, L.GPL_3_PLUS, L.GPL_X, L.AGPL_3_PLUS]`

- `OTHER_COPYLEFT` - Other Copyleft licenses: `[L.MPL, L.EU]`

- `UNLICENSE_INCOMPATIBLE` - Basic compat matrix: `PERMISSIVE + PERMISSIVE_OTHER + GPL + LGPL + OTHER_COPYLEFT + [L.NO_LICENSE, L.PROPRIETARY]`

- `GPL_2_INCOMPATIBLE` - GPL compat matrix
  https://www.gnu.org/licenses/gpl-faq.html#AllCompatibility: `[L.GPL_3, L.GPL_3_PLUS, L.LGPL_3, L.LGPL_3_PLUS]`


- [License Matrix](#license-matrix)
  - [depCompatWMyLice](#depcompatwmylice)
  - [licenseLookup](#licenselookup)
  - [licenseType](#licensetype)

## depCompatWMyLice

[Show source in license_matrix.py:168](../../../licensecheck/license_matrix.py#L168)

Identify if the end user license is compatible with the dependency license(s).

#### Arguments

- `myLicense` *L* - end user license to check
- `depLice` *list[L]* - dependency license
- `ignoreLicenses` *list[L], optional* - list of licenses to ignore. Defaults to None.
- `failLicenses` *list[L], optional* - list of licenses to fail on. Defaults to None.

#### Returns

- `bool` - True if compatible, otherwise False

#### Signature

```python
def depCompatWMyLice(
    myLicense: L,
    depLice: list[L],
    ignoreLicenses: list[L] | None = None,
    failLicenses: list[L] | None = None,
) -> bool:
    ...
```

#### See also

- [License](./types.md#license)



## licenseLookup

[Show source in license_matrix.py:44](../../../licensecheck/license_matrix.py#L44)

Identify a license from an uppercase string representation of a license.

#### Arguments

- `licenseStr` *str* - uppercase string representation of a license

#### Returns

- `L` - License represented by licenseStr

#### Signature

```python
def licenseLookup(licenseStr: str) -> L:
    ...
```

#### See also

- [License](./types.md#license)



## licenseType

[Show source in license_matrix.py:101](../../../licensecheck/license_matrix.py#L101)

Return a list of license types from a license string.

#### Arguments

- `lice` *str* - license name

#### Returns

- `list[L]` - the license

#### Signature

```python
def licenseType(lice: str) -> list[L]:
    ...
```

#### See also

- [License](./types.md#license)
