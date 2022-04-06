# Formatter

> Auto-generated documentation for [licensecheck.formatter](../../../licensecheck/formatter.py) module.

Take our package compat dictionary and give things a pretty format.

- [Licensecheck](../README.md#licensecheck-index) / [Modules](../MODULES.md#licensecheck-modules) / [Licensecheck](index.md#licensecheck) / Formatter
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

[[find in source code]](../../../licensecheck/formatter.py#L133)

```python
def ansi(packages: list[PackageCompat], heading: str | None = None) -> str:
```

Format to ansi.

#### Arguments

- `packages` *list[PackageCompat]* - PackageCompats to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.

#### Returns

- `str` - String to write to a file of stdout

#### See also

- [PackageCompat](types.md#packagecompat)

## csv

[[find in source code]](../../../licensecheck/formatter.py#L91)

```python
def csv(packages: list[PackageCompat], heading: str | None = None) -> str:
```

Format to CSV.

#### Arguments

- `packages` *list[PackageCompat]* - PackageCompats to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.

#### Returns

- `str` - String to write to a file of stdout

#### See also

- [PackageCompat](types.md#packagecompat)

## json

[[find in source code]](../../../licensecheck/formatter.py#L71)

```python
def json(packages: list[PackageCompat], heading: str | None = None) -> str:
```

Format to Json.

#### Arguments

- `packages` *list[PackageCompat]* - PackageCompats to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.

#### Returns

- `str` - String to write to a file of stdout

#### See also

- [PackageCompat](types.md#packagecompat)

## markdown

[[find in source code]](../../../licensecheck/formatter.py#L32)

```python
def markdown(
    packages: list[PackageCompat],
    heading: str | None = None,
) -> str:
```

Format to Markdown.

#### Arguments

- `packages` *list[PackageCompat]* - PackageCompats to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.

#### Returns

- `str` - String to write to a file of stdout

#### See also

- [PackageCompat](types.md#packagecompat)

## simple

[[find in source code]](../../../licensecheck/formatter.py#L186)

```python
def simple(packages: list[PackageCompat]) -> str:
```

Format to plain text.

#### Arguments

- `packages` *list[PackageCompat]* - PackageCompats to format

#### Returns

- `str` - String to write to a file of stdout

#### See also

- [PackageCompat](types.md#packagecompat)
