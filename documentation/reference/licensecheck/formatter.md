# Formatter

[Licensecheck Index](../README.md#licensecheck-index) / [Licensecheck](./index.md#licensecheck) / Formatter

> Auto-generated documentation for [licensecheck.formatter](../../../licensecheck/formatter.py) module.

- [Formatter](#formatter)
  - [_printLicense](#_printlicense)
  - [ansi](#ansi)
  - [html](#html)
  - [markdown](#markdown)
  - [plainText](#plaintext)
  - [raw](#raw)
  - [rawCsv](#rawcsv)
  - [stripAnsi](#stripansi)

## _printLicense

[Show source in formatter.py:51](../../../licensecheck/formatter.py#L51)

Output a license as plain text.

#### Arguments

- `licenseEnum` *License* - License

#### Returns

Type: *str*
license of plain text

#### Signature

```python
def _printLicense(licenseEnum: License) -> str: ...
```

#### See also

- [License](./types.md#license)



## ansi

[Show source in formatter.py:108](../../../licensecheck/formatter.py#L108)

Format to ansi.

#### Arguments

----
 - `myLice` *License* - project license
 - `packages` *list[PackageInfo]* - list of PackageCompats to format.
 - `hide_parameters` *list[str]* - list of parameters to ignore in the output.

#### Returns

-------
 - `str` - string to send to specified output in ansi format

#### Signature

```python
def ansi(
    myLice: License,
    packages: list[PackageInfo],
    hide_parameters: list[ucstr] | None = None,
) -> str: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)



## html

[Show source in formatter.py:253](../../../licensecheck/formatter.py#L253)

Format to html.

#### Arguments

----
 - `myLice` *License* - project license
 - `packages` *list[PackageInfo]* - list of PackageCompats to format.
 - `hide_parameters` *list[str]* - list of parameters to ignore in the output.

#### Returns

-------
 - `str` - string to send to specified output in html format

#### Signature

```python
def html(
    myLice: License,
    packages: list[PackageInfo],
    hide_parameters: list[ucstr] | None = None,
) -> str: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)



## markdown

[Show source in formatter.py:198](../../../licensecheck/formatter.py#L198)

Format to markdown.

#### Arguments

----
 - `myLice` *License* - project license
 - `packages` *list[PackageInfo]* - list of PackageCompats to format.
 - `hide_parameters` *list[str]* - list of parameters to ignore in the output.

#### Returns

-------
 - `str` - string to send to specified output in markdown format

#### Signature

```python
def markdown(
    myLice: License,
    packages: list[PackageInfo],
    hide_parameters: list[ucstr] | None = None,
) -> str: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)



## plainText

[Show source in formatter.py:175](../../../licensecheck/formatter.py#L175)

Format to ansi.

#### Arguments

----
 - `myLice` *License* - project license
 - `packages` *list[PackageInfo]* - list of PackageCompats to format.
 - `hide_parameters` *list[str]* - list of parameters to ignore in the output.

#### Returns

-------
 - `str` - string to send to specified output in plain text format

#### Signature

```python
def plainText(
    myLice: License,
    packages: list[PackageInfo],
    hide_parameters: list[ucstr] | None = None,
) -> str: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)



## raw

[Show source in formatter.py:278](../../../licensecheck/formatter.py#L278)

Format to json.

#### Arguments

----
 - `myLice` *License* - project license
 - `packages` *list[PackageInfo]* - list of PackageCompats to format.
 - `hide_parameters` *list[str]* - list of parameters to ignore in the output.

#### Returns

-------
 - `str` - string to send to specified output in raw json format

#### Signature

```python
def raw(
    myLice: License,
    packages: list[PackageInfo],
    hide_parameters: list[ucstr] | None = None,
) -> str: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)



## rawCsv

[Show source in formatter.py:308](../../../licensecheck/formatter.py#L308)

Format to csv.

#### Arguments

----
 - `myLice` *License* - project license
 - `packages` *list[PackageInfo]* - list of PackageCompats to format.
 - `hide_parameters` *list[str]* - list of parameters to ignore in the output.

#### Returns

-------
 - `str` - string to send to specified output in raw csv format

#### Signature

```python
def rawCsv(
    myLice: License,
    packages: list[PackageInfo],
    hide_parameters: list[ucstr] | None = None,
) -> str: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)



## stripAnsi

[Show source in formatter.py:93](../../../licensecheck/formatter.py#L93)

Strip ansi codes from a given string.

#### Arguments

----
 - `string` *str* - string to strip codes from

#### Returns

-------
 - `str` - plaintext, utf-8 string (safe for writing to files)

#### Signature

```python
def stripAnsi(string: str) -> str: ...
```