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

[Show source in formatter.py:51](../../../licensecheck/formatter.py#L51)

Format to ansi

#### Arguments

- `packages` *list[PackageInfo]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in ansi format

#### Signature

```python
def ansi(packages: list[PackageInfo]) -> str:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)



## markdown

[Show source in formatter.py:99](../../../licensecheck/formatter.py#L99)

Format to markdown

#### Arguments

- `packages` *list[PackageInfo]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in markdown format

#### Signature

```python
def markdown(packages: list[PackageInfo]) -> str:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)



## plainText

[Show source in formatter.py:87](../../../licensecheck/formatter.py#L87)

Format to plain text

#### Arguments

- `packages` *list[PackageInfo]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in plain text format

#### Signature

```python
def plainText(packages: list[PackageInfo]) -> str:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)



## raw

[Show source in formatter.py:134](../../../licensecheck/formatter.py#L134)

Format to raw json

#### Arguments

- `packages` *list[PackageInfo]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in raw json format

#### Signature

```python
def raw(packages: list[PackageInfo]) -> str:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)



## rawCsv

[Show source in formatter.py:146](../../../licensecheck/formatter.py#L146)

Format to raw csv

#### Arguments

- `packages` *list[PackageInfo]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in raw csv format

#### Signature

```python
def rawCsv(packages: list[PackageInfo]) -> str:
    ...
```

#### See also

- [PackageInfo](./types.md#packageinfo)



## stripAnsi

[Show source in formatter.py:39](../../../licensecheck/formatter.py#L39)

Strip ansi codes from a given string

#### Arguments

- `string` *str* - string to strip codes from

#### Returns

- `str` - plaintext, utf-8 string (safe for writing to files)

#### Signature

```python
def stripAnsi(string: str) -> str:
    ...
```


