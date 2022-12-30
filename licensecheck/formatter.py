"""Output

```json
{
	name: str
	version: str
	namever: str
	size: int
	homePage: str
	author: str
	license: str
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
from io import StringIO

from rich.console import Console
from rich.table import Table

from licensecheck.types import PackageInfo

INFO = {"program": "licensecheck", "version": "2022.2.0"}


def stripAnsi(string: str) -> str:
	"""Strip ansi codes from a given string

	Args:
		string (str): string to strip codes from

	Returns:
		str: plaintext, utf-8 string (safe for writing to files)
	"""
	return re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])").sub("", string)


def ansi(packages: list[PackageInfo]) -> str:
	"""Format to ansi

	Args:
		packages (list[PackageInfo]): list of PackageCompats to format.

	Returns:
		str: string to send to specified output in ansi format
	"""
	if len(packages) == 0:
		return "No packages"

	string = StringIO()

	console = Console(file=string, color_system="truecolor")

	errors = [x for x in packages if x.errorCode > 0]
	if len(errors) > 0:
		table = Table(title="\nlist of errors")
		table.add_column("Package", style="magenta")
		_ = [table.add_row(x.name) for x in errors]
		console.print(table)

	table = Table(title="\nlist of packages")
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


def plainText(packages: list[PackageInfo]) -> str:
	"""Format to plain text

	Args:
		packages (list[PackageInfo]): list of PackageCompats to format.

	Returns:
		str: string to send to specified output in plain text format
	"""
	return stripAnsi(ansi(packages))


def markdown(packages: list[PackageInfo]) -> str:
	"""Format to markdown

	Args:
		packages (list[PackageInfo]): list of PackageCompats to format.

	Returns:
		str: string to send to specified output in markdown format
	"""
	if len(packages) == 0:
		return "No packages"

	strBuf = ["\n# Packages\nFind a list of packages below\n"]
	packages = sorted(packages, key=lambda i: i.name)

	# Summary Table
	strBuf.append("|Compatible|Package|\n|:--|:--|")
	for pkg in packages:
		strBuf.append(f"|{pkg.licenseCompat}|{pkg.name}|")

	# Details
	for pkg in packages:
		strBuf.extend(
			[
				f"\n## {pkg.namever}",
				f"\n- HomePage: {pkg.homePage}",
				f"- Author: {pkg.author}",
				f"- License: {pkg.license}",
				f"- Compatible: {pkg.licenseCompat}",
				f"- Size: {pkg.size}",
			]
		)
	return "\n".join(strBuf) + "\n"


def raw(packages: list[PackageInfo]) -> str:
	"""Format to raw json

	Args:
		packages (list[PackageInfo]): list of PackageCompats to format.

	Returns:
		str: string to send to specified output in raw json format
	"""
	return json.dumps({"info": INFO, "packages": [x.__dict__ for x in packages]}, indent="\t")


def rawCsv(packages: list[PackageInfo]) -> str:
	"""Format to raw csv

	Args:
		packages (list[PackageInfo]): list of PackageCompats to format.

	Returns:
		str: string to send to specified output in raw csv format
	"""
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
