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

[Show source in formatter.py:50](../../../licensecheck/formatter.py#L50)

Format to ansi

#### Arguments

- `packages` *list[PackageCompat]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in ansi format

#### Signature

```python
def ansi(packages: list[PackageCompat]) -> str:
    ...
```

#### See also

- [PackageCompat](./types.md#packagecompat)



## markdown

[Show source in formatter.py:91](../../../licensecheck/formatter.py#L91)

Format to markdown

#### Arguments

- `packages` *list[PackageCompat]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in markdown format

#### Signature

```python
def markdown(packages: list[PackageCompat]) -> str:
    ...
```

#### See also

- [PackageCompat](./types.md#packagecompat)



## plainText

[Show source in formatter.py:79](../../../licensecheck/formatter.py#L79)

Format to plain text

#### Arguments

- `packages` *list[PackageCompat]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in plain text format

#### Signature

```python
def plainText(packages: list[PackageCompat]) -> str:
    ...
```

#### See also

- [PackageCompat](./types.md#packagecompat)



## raw

[Show source in formatter.py:127](../../../licensecheck/formatter.py#L127)

Format to raw json

#### Arguments

- `packages` *list[PackageCompat]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in raw json format

#### Signature

```python
def raw(packages: list[PackageCompat]) -> str:
    ...
```

#### See also

- [PackageCompat](./types.md#packagecompat)



## rawCsv

[Show source in formatter.py:139](../../../licensecheck/formatter.py#L139)

Format to raw csv

#### Arguments

- `packages` *list[PackageCompat]* - list of PackageCompats to format.

#### Returns

- `str` - string to send to specified output in raw csv format

#### Signature

```python
def rawCsv(packages: list[PackageCompat]) -> str:
    ...
```

#### See also

- [PackageCompat](./types.md#packagecompat)



## stripAnsi

[Show source in formatter.py:38](../../../licensecheck/formatter.py#L38)

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


