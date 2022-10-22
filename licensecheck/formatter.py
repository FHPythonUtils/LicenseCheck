"""Output

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

To one of the following formats:

- ansi
- plain
- markdown
- json
- csv
"""

import csv
import json
import re
from io import StringIO

from rich.console import Console
from rich.table import Table

from licensecheck.types import PackageCompat

INFO = {"program": "licensecheck", "version": "2022.2.0"}


def stripAnsi(string: str) -> str:
	"""Strip ansi codes from a given string

	Args:
		string (str): string to strip codes from

	Returns:
		str: plaintext, utf-8 string (safe for writing to files)
	"""
	return re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])").sub("", string)


def ansi(packages: list[PackageCompat]) -> str:
	"""Format to ansi

	Args:
		packages (list[PackageCompat]): list of PackageCompats to format.

	Returns:
		str: string to send to specified output in ansi format
	"""
	if len(packages) == 0:
		return "No packages"

	string = StringIO()

	console = Console(file=string, color_system="truecolor")

	table = Table(title="\nlist of packages")
	table.add_column("Compatible", style="cyan")
	table.add_column("Package", style="magenta")
	table.add_column("License(s)", style="magenta")
	licenseCompat = (
		"[red]✖[/]",
		"[green]✔[/]",
	)
	_ = [table.add_row(licenseCompat[x["license_compat"]], x["name"], x["license"]) for x in packages]
	console.print(table)
	return string.getvalue()


def plainText(packages: list[PackageCompat]) -> str:
	"""Format to plain text

	Args:
		packages (list[PackageCompat]): list of PackageCompats to format.

	Returns:
		str: string to send to specified output in plain text format
	"""
	return stripAnsi(ansi(packages))


def markdown(packages: list[PackageCompat]) -> str:
	"""Format to markdown

	Args:
		packages (list[PackageCompat]): list of PackageCompats to format.

	Returns:
		str: string to send to specified output in markdown format
	"""
	if len(packages) == 0:
		return "No packages"

	strBuf = ["\n# Packages\nFind a list of packages below\n"]
	packages = sorted(packages, key=lambda i: i["name"])

	# Summary Table
	strBuf.append("|Compatible|Package|\n|:--|:--|")
	for pkg in packages:
		strBuf.append(f"|{pkg['license_compat']}|{pkg['name']}|")

	# Details
	for pkg in packages:
		strBuf.extend(
			[
				f"\n## {pkg['namever']}",
				f"\n- HomePage: {pkg['home_page']}",
				f"- Author: {pkg['author']}",
				f"- License: {pkg['license']}",
				f"- Compatible: {pkg['license_compat']}",
				f"- Size: {pkg['size']}",
			]
		)
	return "\n".join(strBuf) + "\n"



def raw(packages: list[PackageCompat]) -> str:
	"""Format to raw json

	Args:
		packages (list[PackageCompat]): list of PackageCompats to format.

	Returns:
		str: string to send to specified output in raw json format
	"""
	return json.dumps({"info": INFO, "packages": packages}, indent="\t")


def rawCsv(packages: list[PackageCompat]) -> str:
	"""Format to raw csv

	Args:
		packages (list[PackageCompat]): list of PackageCompats to format.

	Returns:
		str: string to send to specified output in raw csv format
	"""
	string = StringIO()
	writer = csv.DictWriter(string, fieldnames=list(packages[0]), lineterminator="\n")
	writer.writeheader()
	writer.writerows(packages)
	return string.getvalue()


formatMap = {
	"json": raw,
	"markdown": markdown,
	"csv": rawCsv,
	"ansi": ansi,
	"simple": plainText,
}
