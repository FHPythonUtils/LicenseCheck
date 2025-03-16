# Cli

[Licensecheck Index](../README.md#licensecheck-index) / [Licensecheck](./index.md#licensecheck) / Cli

> Auto-generated documentation for [licensecheck.cli](../../../licensecheck/cli.py) module.

- [Cli](#cli)
  - [cli](#cli)
  - [main](#main)

## cli

[Show source in cli.py:20](../../../licensecheck/cli.py#L20)

Cli entry point.

#### Signature

```python
def cli() -> None: ...
```



## main

[Show source in cli.py:112](../../../licensecheck/cli.py#L112)

Test entry point.

Note: FHConfParser (Parses in the following order: `pyproject.toml`,
`setup.cfg`, `licensecheck.toml`, `licensecheck.json`,
`licensecheck.ini`, `~/licensecheck.toml`, `~/licensecheck.json`, `~/licensecheck.ini`)

#### Signature

```python
def main(args: dict | argparse.Namespace) -> int: ...
```