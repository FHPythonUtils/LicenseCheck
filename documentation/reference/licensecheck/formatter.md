# Formatter

[Licensecheck Index](../README.md#licensecheck-index) /
[Licensecheck](./index.md#licensecheck) /
Formatter

> Auto-generated documentation for [licensecheck.formatter](../../../licensecheck/formatter.py) module.

- [Formatter](#formatter)
  - [ansi](#ansi)
  - [markdown](#markdown)
  - [plainText](#plaintext)
  - [raw](#raw)
  - [rawCsv](#rawcsv)
  - [stripAnsi](#stripansi)

## ansi

[Show source in formatter.py:56](../../../licensecheck/formatter.py#L56)

Format to ansi

#### Arguments

- `myLice` *License* - project license
- `packages` *list[PackageInfo]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in ansi format

#### Signature

```python
def ansi(myLice: License, packages: list[PackageInfo]) -> str: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)



## markdown

[Show source in formatter.py:114](../../../licensecheck/formatter.py#L114)

Format to markdown

#### Arguments

- `myLice` *License* - project license
- `packages` *list[PackageInfo]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in markdown format

#### Signature

```python
def markdown(myLice: License, packages: list[PackageInfo]) -> str: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)



## plainText

[Show source in formatter.py:101](../../../licensecheck/formatter.py#L101)

Format to ansi

#### Arguments

- `myLice` *License* - project license
- `packages` *list[PackageInfo]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in plain text format

#### Signature

```python
def plainText(myLice: License, packages: list[PackageInfo]) -> str: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)



## raw

[Show source in formatter.py:153](../../../licensecheck/formatter.py#L153)

Format to json

#### Arguments

- `myLice` *License* - project license
- `packages` *list[PackageInfo]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in raw json format

#### Signature

```python
def raw(myLice: License, packages: list[PackageInfo]) -> str: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)



## rawCsv

[Show source in formatter.py:173](../../../licensecheck/formatter.py#L173)

Format to csv

#### Arguments

- `myLice` *License* - project license
- `packages` *list[PackageInfo]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in raw csv format

#### Signature

```python
def rawCsv(myLice: License, packages: list[PackageInfo]) -> str: ...
```

#### See also

- [License](./types.md#license)
- [PackageInfo](./types.md#packageinfo)



## stripAnsi

[Show source in formatter.py:44](../../../licensecheck/formatter.py#L44)

Strip ansi codes from a given string

#### Arguments

- `string` *str* - string to strip codes from

#### Returns

- `str` - plaintext, utf-8 string (safe for writing to files)

#### Signature

```python
def stripAnsi(string: str) -> str: ...
```