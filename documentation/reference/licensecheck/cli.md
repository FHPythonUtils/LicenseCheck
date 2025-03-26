# Cli

[Licensecheck Index](../README.md#licensecheck-index) / [Licensecheck](./index.md#licensecheck) / Cli

> Auto-generated documentation for [licensecheck.cli](../../../licensecheck/cli.py) module.

- [Cli](#cli)
  - [cli](#cli)
  - [main](#main)

## cli

[Show source in cli.py:21](../../../licensecheck/cli.py#L21)

Cli entry point.

#### Signature

```python
def cli() -> None: ...
```



## main

[Show source in cli.py:124](../../../licensecheck/cli.py#L124)

Test entry point.

Note: FHConfParser (Parses in the following order: `pyproject.toml`,
`setup.cfg`, `licensecheck.toml`, `licensecheck.json`,
`licensecheck.ini`, `~/licensecheck.toml`, `~/licensecheck.json`, `~/licensecheck.ini`)

#### Signature

```python
def main(args: dict) -> int: ...
```