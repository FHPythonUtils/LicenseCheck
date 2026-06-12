# Fmt

[Licensecheck Index](../README.md#licensecheck-index) / [Licensecheck](./index.md#licensecheck) / Fmt

> Auto-generated documentation for [licensecheck.fmt](../../../licensecheck/fmt.py) module.

- [Fmt](#fmt)
  - [_printLicense](#_printlicense)
  - [ansi](#ansi)
  - [fmt](#fmt)
  - [html](#html)
  - [markdown](#markdown)
  - [plainText](#plaintext)
  - [raw](#raw)
  - [rawCsv](#rawcsv)
  - [stripAnsi](#stripansi)

## _printLicense

[Show source in fmt.py:65](../../../licensecheck/fmt.py#L65)

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

[Show source in fmt.py:122](../../../licensecheck/fmt.py#L122)

Format to ansi.

#### Arguments

- `myLice` *License* - project license
:param list[dict[str, Any]] packages: list of PackageCompats to format.

#### Returns

Type: *str*
string to send to specified output in ansi format

#### Signature

```python
def ansi(myLice: License, packages: list[dict[str, Any]]) -> str: ...
```

#### See also

- [License](./types.md#license)



## fmt

[Show source in fmt.py:295](../../../licensecheck/fmt.py#L295)

Format to a given format by `format_`.

#### Arguments

- `myLice` *License* - project license
:param list[PackageInfo] packages: list of PackageCompats to format.
:param list[ucstr] hide_parameters: list of parameters to ignore in the output.
- `show_only_failing` *bool* - output only failing packages, defaults to False.

#### Returns

Type: *str*
string to send to specified output in ansi format

#### Signature

```python
def fmt(
    format_: str,
    myLice: License,
    packages: list[PackageInfo],
    hide_parameters: list[ucstr] | None = None,
    show_only_failing: bool = False,
) -> str: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)



## html

[Show source in fmt.py:241](../../../licensecheck/fmt.py#L241)

Format to html.

#### Arguments

- `myLice` *License* - project license
:param list[dict[str, Any]] packages: list of PackageCompats to format.

#### Returns

Type: *str*
string to send to specified output in html format

#### Signature

```python
def html(myLice: License, packages: list[dict[str, Any]]) -> str: ...
```

#### See also

- [License](./types.md#license)



## markdown

[Show source in fmt.py:194](../../../licensecheck/fmt.py#L194)

Format to markdown.

#### Arguments

- `myLice` *License* - project license
:param list[dict[str, Any]] packages: list of PackageCompats to format.

#### Returns

Type: *str*
string to send to specified output in markdown format

#### Signature

```python
def markdown(myLice: License, packages: list[dict[str, Any]]) -> str: ...
```

#### See also

- [License](./types.md#license)



## plainText

[Show source in fmt.py:180](../../../licensecheck/fmt.py#L180)

Format to plain text.

#### Arguments

- `myLice` *License* - project license
:param list[dict[str, Any]] packages: list of PackageCompats to format.

#### Returns

Type: *str*
string to send to specified output in plain text format

#### Signature

```python
def plainText(myLice: License, packages: list[dict[str, Any]]) -> str: ...
```

#### See also

- [License](./types.md#license)



## raw

[Show source in fmt.py:258](../../../licensecheck/fmt.py#L258)

Format to json.

#### Arguments

- `myLice` *License* - project license
:param list[dict[str, Any]] packages: list of PackageCompats to format.

#### Returns

Type: *str*
string to send to specified output in json format

#### Signature

```python
def raw(myLice: License, packages: list[dict[str, Any]]) -> str: ...
```

#### See also

- [License](./types.md#license)



## rawCsv

[Show source in fmt.py:276](../../../licensecheck/fmt.py#L276)

Format to csv.

#### Arguments

- `myLice` *License* - project license
:param list[dict[str, Any]] packages: list of PackageCompats to format.

#### Returns

Type: *str*
string to send to specified output in csv format

#### Signature

```python
def rawCsv(myLice: License, packages: list[dict[str, Any]]) -> str: ...
```

#### See also

- [License](./types.md#license)



## stripAnsi

[Show source in fmt.py:107](../../../licensecheck/fmt.py#L107)

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