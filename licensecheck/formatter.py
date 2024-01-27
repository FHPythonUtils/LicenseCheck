"""Output.

```json
{
	name: str
	version: str
	namever: str
	size: int
	homePage: str
	author: str
	license: ucstr
	licenseCompat: bool
}
```

To one of the following formats:

- ansi
- plain
- markdown
- json
- csv
"""
from __future__ import annotations

import csv
import json
import re
from importlib.metadata import PackageNotFoundError, version
from io import StringIO

from rich.console import Console
from rich.table import Table

from licensecheck.types import License, PackageInfo, printLicense

try:
	VERSION = version("licensecheck")
except PackageNotFoundError:
	VERSION = "dev"
INFO = {"program": "licensecheck", "version": VERSION, "license": "MIT LICENSE"}


def stripAnsi(string: str) -> str:
	"""Strip ansi codes from a given string.

	Args:
	----
		string (str): string to strip codes from

	Returns:
	-------
		str: plaintext, utf-8 string (safe for writing to files)
	"""
	return re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])").sub("", string)


def ansi(myLice: License, packages: list[PackageInfo]) -> str:
	"""Format to ansi.

	Args:
	----
		myLice (License): project license
		packages (list[PackageInfo]): list of PackageCompats to format.

	Returns:
	-------
		str: string to send to specified output in ansi format
	"""
	string = StringIO()

	console = Console(file=string, color_system="truecolor")

	table = Table(title="\nInfo")
	table.add_column("Item", style="cyan")
	table.add_column("Value", style="magenta")
	_ = [table.add_row(k, v) for k, v in INFO.items()]
	table.add_row("project_license", printLicense(myLice))

	console.print(table)

	if len(packages) == 0:
		return f"{string.getvalue()}\nNo packages"

	errors = [x for x in packages if x.errorCode > 0]
	if len(errors) > 0:
		table = Table(title="\nList Of Errors")
		table.add_column("Package", style="magenta")
		_ = [table.add_row(x.name) for x in errors]
		console.print(table)

	table = Table(title="\nList Of Packages")
	table.add_column("Compatible", style="cyan")
	table.add_column("Package", style="magenta")
	table.add_column("License(s)", style="magenta")
	licenseCompat = (
		"[red]✖[/]",
		"[green]✔[/]",
	)
	_ = [table.add_row(licenseCompat[x.licenseCompat], x.name, x.license) for x in packages]
	console.print(table)
	return string.getvalue()


def plainText(myLice: License, packages: list[PackageInfo]) -> str:
	"""Format to ansi.

	Args:
	----
		myLice (License): project license
		packages (list[PackageInfo]): list of PackageCompats to format.

	Returns:
	-------
		str: string to send to specified output in plain text format
	"""
	return stripAnsi(ansi(myLice, packages))


def markdown(myLice: License, packages: list[PackageInfo]) -> str:
	"""Format to markdown.

	Args:
	----
		myLice (License): project license
		packages (list[PackageInfo]): list of PackageCompats to format.

	Returns:
	-------
		str: string to send to specified output in markdown format
	"""
	info = "\n".join(f"- **{k}**: {v}" for k, v in INFO.items())
	strBuf = [f"## Info\n\n{info}\n\n## Project License\n\n{printLicense(myLice)}\n"]

	if len(packages) == 0:
		return f"{strBuf[0]}\nNo packages"

	strBuf.append("## Packages\n\nFind a list of packages below\n")
	packages = sorted(packages, key=lambda i: i.name)

	# Summary Table
	strBuf.append("|Compatible|Package|\n|:--|:--|")
	for pkg in packages:
		strBuf.append(f"|{'✔' if pkg.licenseCompat else '✖'}|{pkg.name}|")

	# Details
	for pkg in packages:
		strBuf.extend(
			[
				f"\n### {pkg.namever}",
				f"\n- HomePage: {pkg.homePage}",
				f"- Author: {pkg.author}",
				f"- License: {pkg.license}",
				f"- Compatible: {pkg.licenseCompat}",
				f"- Size: {pkg.size}",
			]
		)
	return "\n".join(strBuf) + "\n"


def raw(myLice: License, packages: list[PackageInfo]) -> str:
	"""Format to json.

	Args:
	----
		myLice (License): project license
		packages (list[PackageInfo]): list of PackageCompats to format.

	Returns:
	-------
		str: string to send to specified output in raw json format
	"""
	return json.dumps(
		{
			"info": INFO,
			"project_license": printLicense(myLice),
			"packages": [x.__dict__ for x in packages],
		},
		indent="\t",
	)


def rawCsv(myLice: License, packages: list[PackageInfo]) -> str:
	"""Format to csv.

	Args:
	----
		myLice (License): project license
		packages (list[PackageInfo]): list of PackageCompats to format.

	Returns:
	-------
		str: string to send to specified output in raw csv format
	"""
	_ = myLice
	string = StringIO()
	writer = csv.DictWriter(string, fieldnames=list(packages[0].__dict__), lineterminator="\n")
	writer.writeheader()
	writer.writerows([x.__dict__ for x in packages])
	return string.getvalue()


formatMap = {
	"json": raw,
	"markdown": markdown,
	"csv": rawCsv,
	"ansi": ansi,
	"simple": plainText,
}
