# formatter

> Auto-generated documentation for [licensecheck.formatter](../../licensecheck/formatter.py) module.

Take our package compat dictionary and give things a pretty format.

- [Licensecheck](../README.md#licensecheck-index) / [Modules](../README.md#licensecheck-modules) / [licensecheck](index.md#licensecheck) / formatter
    - [ansi](#ansi)
    - [csv](#csv)
    - [json](#json)
    - [markdown](#markdown)
    - [simple](#simple)

```json
{
 name: str
 version: str
 namever: str
 size: int
 home_page: str
 author: str
 license: str
 license_compat: bool
}
```

Formats

- markdown
- json
- csv
- ansi

## ansi

[[find in source code]](../../licensecheck/formatter.py#L142)

```python
def ansi(
    packages: list[PackageCompat],
    heading: typing.Optional[str] = None,
) -> str:
```

Format to ansi.

#### Arguments

- `packages` *list[PackageCompat]* - PackageCompats to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.

#### Returns

- `str` - String to write to a file of stdout

## csv

[[find in source code]](../../licensecheck/formatter.py#L100)

```python
def csv(
    packages: list[PackageCompat],
    heading: typing.Optional[str] = None,
) -> str:
```

Format to CSV.

#### Arguments

- `packages` *list[PackageCompat]* - PackageCompats to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.

#### Returns

- `str` - String to write to a file of stdout

## json

[[find in source code]](../../licensecheck/formatter.py#L80)

```python
def json(
    packages: list[PackageCompat],
    heading: typing.Optional[str] = None,
) -> str:
```

Format to Json.

#### Arguments

- `packages` *list[PackageCompat]* - PackageCompats to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.

#### Returns

- `str` - String to write to a file of stdout

## markdown

[[find in source code]](../../licensecheck/formatter.py#L41)

```python
def markdown(
    packages: list[PackageCompat],
    heading: typing.Optional[str] = None,
) -> str:
```

Format to Markdown.

#### Arguments

- `packages` *list[PackageCompat]* - PackageCompats to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.

#### Returns

- `str` - String to write to a file of stdout

## simple

[[find in source code]](../../licensecheck/formatter.py#L195)

```python
def simple(packages: list[PackageCompat]) -> str:
```

Format to plain text.

#### Arguments

- `packages` *list[PackageCompat]* - PackageCompats to format

#### Returns

- `str` - String to write to a file of stdout
