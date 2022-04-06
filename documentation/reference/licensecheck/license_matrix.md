# License Matrix

> Auto-generated documentation for [licensecheck.license_matrix](../../../licensecheck/license_matrix.py) module.

Define a foss compatability license_matrix.

- [Licensecheck](../README.md#licensecheck-index) / [Modules](../MODULES.md#licensecheck-modules) / [Licensecheck](index.md#licensecheck) / License Matrix
    - [depCompatWMyLice](#depcompatwmylice)
    - [licenseLookup](#licenselookup)
    - [licenseType](#licensetype)

Standard disclaimer:: I am not a lawyer and there is no guarantee that the
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
- Academic Free

Copyleft
permissive -> lgpl 2.1 -> gpl 2
permissive -> lgpl 3 -> gpl 3 -> agpl
permissive -> mpl -> gpl -> agpl (3 only)

permissive (any) -> EU
EU -> gpl -> agpl (3 only)

#### Attributes

- `PERMISSIVE` - Permissive licenses compatible with GPL: `[L.MIT, L.BOOST, L.BSD, L.ISC, L.NCSA, L.PSFL]`
- `PERMISSIVE_OTHER` - Permissive licenses NOT compatible with GPL: `[L.APACHE, L.ECLIPSE, L.ACADEMIC_FREE]`
- `LGPL` - LGPL licenses: `[L.LGPL_2, L.LGPL_3, L.LGPL_2_PLUS, L.LGPL_3_PLUS, L.LGPL_X]`
- `GPL` - GPL licenses (including AGPL): `[L.GPL_2, L.GPL_3, L.GPL_2_PLUS, L.GPL_3_PLUS, L.GPL_X, L.AGPL_3_PLUS]`
- `OTHER_COPYLEFT` - Other Copyleft licenses: `[L.MPL, L.EU]`
- `UNLICENSE_INCOMPATIBLE` - Basic compat matrix: `PERMISSIVE + PERMISSIVE_OTHER + GPL + LGPL + OT...`
- `GPL_2_INCOMPATIBLE` - GPL compat matrix
  https://www.gnu.org/licenses/gpl-faq.html#AllCompatibility: `[L.GPL_3, L.GPL_3_PLUS, L.LGPL_3, L.LGPL_3_PLUS]`

## depCompatWMyLice

[[find in source code]](../../../licensecheck/license_matrix.py#L153)

```python
def depCompatWMyLice(
    myLicense: L,
    depLice: list[L],
    ignoreLicenses: list[L] = None,
    failLicenses: list[L] = None,
) -> bool:
```

Identify if the end user license is compatible with the dependency license(s).

#### Arguments

- `myLicense` *L* - end user license to check
- `depLice` *list[L]* - dependency license
- `ignoreLicenses` *list[L], optional* - list of licenses to ignore. Defaults to None.
- `failLicenses` *list[L], optional* - list of licenses to fail on. Defaults to None.

#### Returns

- `bool` - True if compatible, otherwise False

#### See also

- [License](types.md#license)

## licenseLookup

[[find in source code]](../../../licensecheck/license_matrix.py#L43)

```python
def licenseLookup(licenseStr: str) -> L:
```

Identify a license from an uppercase string representation of a license.

#### Arguments

- `licenseStr` *str* - uppercase string representation of a license

#### Returns

- `L` - License represented by licenseStr

#### See also

- [License](types.md#license)

## licenseType

[[find in source code]](../../../licensecheck/license_matrix.py#L86)

```python
def licenseType(lice: str) -> list[L]:
```

Return a list of license types from a license string.

#### Arguments

- `lice` *str* - license name

#### Returns

- `list[L]` - the license

#### See also

- [License](types.md#license)
