Module licensecheck.formatter
=============================
Take our package compat dictionary and give things a pretty format

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

Functions
---------

    
`ansi(packages: list[PackageCompat], heading: typing.Optional[str] = None) ‑> str`
:   Format to ansi
    
    Args:
            packages (list[PackageCompat]): PackageCompats to format
            heading (str, optional): Optional heading to include. Defaults to None.
    
    Returns:
            str: String to write to a file of stdout

    
`csv(packages: list[PackageCompat], heading: typing.Optional[str] = None) ‑> str`
:   Format to CSV
    
    Args:
            packages (list[PackageCompat]): PackageCompats to format
            heading (str, optional): Optional heading to include. Defaults to None.
    
    Returns:
            str: String to write to a file of stdout

    
`json(packages: list[PackageCompat], heading: typing.Optional[str] = None) ‑> str`
:   Format to Json
    
    Args:
            packages (list[PackageCompat]): PackageCompats to format
            heading (str, optional): Optional heading to include. Defaults to None.
    
    Returns:
            str: String to write to a file of stdout

    
`markdown(packages: list[PackageCompat], heading: typing.Optional[str] = None) ‑> str`
:   Format to Markdown
    
    Args:
            packages (list[PackageCompat]): PackageCompats to format
            heading (str, optional): Optional heading to include. Defaults to None.
    
    Returns:
            str: String to write to a file of stdout

    
`simple(packages: list[PackageCompat]) ‑> str`
:   Format to ansi
    
    Args:
            packages (list[PackageCompat]): PackageCompats to format
    
    Returns:
            str: String to write to a file of stdout