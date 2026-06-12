# License Matrix

[Licensecheck Index](../../README.md#licensecheck-index) / [Licensecheck](../index.md#licensecheck) / License Matrix

> Auto-generated documentation for [licensecheck.license_matrix](../../../../licensecheck/license_matrix/__init__.py) module.

- [License Matrix](#license-matrix)
  - [depCompatWMyLice](#depcompatwmylice)
  - [liceCompat](#licecompat)
  - [licenseLookup](#licenselookup)
  - [licenseType](#licensetype)

## depCompatWMyLice

[Show source in __init__.py:137](../../../../licensecheck/license_matrix/__init__.py#L137)

Identify if the end user license is compatible with the dependency license(s).

#### Arguments

----
 - `myLicense` *L* - end user license to check
 - `depLice` *list[L]* - dependency license
 - `ignoreLicenses` *list[L], optional* - list of licenses to ignore. Defaults to None.
 - `failLicenses` *list[L], optional* - list of licenses to fail on. Defaults to None.
 - `onlyLicenses` *list[L], optional* - list of allowed licenses. Defaults to None.

#### Returns

-------
 - `bool` - True if compatible, otherwise False

#### Signature

```python
def depCompatWMyLice(
    myLicense: L,
    depLice: list[L],
    ignoreLicenses: list[L] | None = None,
    failLicenses: list[L] | None = None,
    onlyLicenses: list[L] | None = None,
) -> bool: ...
```

#### See also

- [License](../types.md#license)



## liceCompat

[Show source in __init__.py:177](../../../../licensecheck/license_matrix/__init__.py#L177)

Identify if the end user license is compatible with the dependency license.

#### Arguments

- `myLicense` *L* - end user license
- `lice` *L* - dependency license
:param list[L] ignoreLicenses: list of licenses to ignore. Defaults to None.
:param list[L] failLicenses: list of licenses to fail on. Defaults to None.
:param list[L] onlyLicenses: list of allowed licenses. Defaults to None.

#### Returns

Type: *bool*
True if compatible, otherwise False

#### Signature

```python
def liceCompat(
    myLicense: L,
    lice: L,
    ignoreLicenses: list[L],
    failLicenses: list[L],
    onlyLicenses: list[L],
) -> bool: ...
```

#### See also

- [License](../types.md#license)



## licenseLookup

[Show source in __init__.py:99](../../../../licensecheck/license_matrix/__init__.py#L99)

Identify a license from an uppercase string representation of a license.

#### Arguments

- `licenseStr` *ucstr* - uppercase string representation of a license
:param list[ucstr] | None ignoreLicenses: licenses to ignore, defaults to None

#### Returns

Type: *L*
License represented by licenseStr

#### Signature

```python
def licenseLookup(licenseStr: ucstr, ignoreLicenses: list[ucstr] | None = None) -> L: ...
```

#### See also

- [License](../types.md#license)
- [ucstr](../types.md#ucstr)



## licenseType

[Show source in __init__.py:118](../../../../licensecheck/license_matrix/__init__.py#L118)

Return a list of license types from a license string.

#### Arguments

----
 - `lice` *ucstr* - license name
 - `ignoreLicenses` *list[ucstr]* - a list of licenses to ignore (skipped, compat may still be
 False)

#### Returns

-------
 - `list[L]` - the license

#### Signature

```python
def licenseType(lice: ucstr, ignoreLicenses: list[ucstr] | None = None) -> list[L]: ...
```

#### See also

- [License](../types.md#license)
- [ucstr](../types.md#ucstr)