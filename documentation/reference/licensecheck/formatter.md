# Formatter

[Licensecheck Index](../README.md#licensecheck-index) / [Licensecheck](./index.md#licensecheck) / Formatter

> Auto-generated documentation for [licensecheck.formatter](../../../licensecheck/formatter.py) module.

- [Formatter](#formatter)
  - [ansi](#ansi)
  - [markdown](#markdown)
  - [plainText](#plaintext)
  - [raw](#raw)
  - [rawCsv](#rawcsv)
  - [stripAnsi](#stripansi)

## ansi

[Show source in formatter.py:61](../../../licensecheck/formatter.py#L61)

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



## markdown

[Show source in formatter.py:151](../../../licensecheck/formatter.py#L151)

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

[Show source in formatter.py:128](../../../licensecheck/formatter.py#L128)

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

[Show source in formatter.py:206](../../../licensecheck/formatter.py#L206)

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

[Show source in formatter.py:236](../../../licensecheck/formatter.py#L236)

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

[Show source in formatter.py:46](../../../licensecheck/formatter.py#L46)

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