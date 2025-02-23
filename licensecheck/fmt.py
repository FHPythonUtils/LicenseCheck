"""The formatter is reponsible for outputting the list of PackageInfo[s].

Note the PackageInfo has the following attributes, that we can use to build each output format:
- name: str
- version: str
- namever: str
- size: int = -1
- homePage: str
- author: str
- license: ucstr
- licenseCompat: bool
- errorCode: int = 0


The available output formats are defined as follows


- ansi: Plain text output with ANSI color codes for terminal display.
	used for simple, color-coded output on the command line.
- plain: A basic, no-frills plain text format, used when a clean and simple
	textual representation is needed without any additional markup or styling.
- markdown: A lightweight markup language with plain-text formatting syntax. Ideal
	for creating formatted documents that can be easily converted into HTML for web display.
- html: A format suitable for rendering in web browsers. (can be styled with CSS
	for more complex presentation.)
- json: A structured data format. This format representing the list of PackageInfo[s]
	as a JSON object
- csv: A simple, comma-separated values format. widely used in spreadsheets and
	databases for easy import/export of data.

Note that these support the get_filtered_dict method, which allows users
to hide some of the output via the `--hide-output-parameters` cli flag. In addition
these support the show_only_failing method, which allows users
to show only packages that are not compatible with out license via the
`--show-only-failing` cli flag

"""

from __future__ import annotations

import csv
import json
import re
from collections import OrderedDict
from importlib.metadata import PackageNotFoundError, version
from io import StringIO
from pathlib import Path
from typing import Any

import markdown as markdownlib
from rich.console import Console
from rich.table import Table

from licensecheck.types import License, PackageInfo, ucstr

THISDIR = Path(__file__).resolve().parent

try:
	VERSION = version("licensecheck")
except PackageNotFoundError:
	VERSION = "dev"
INFO = {"program": "licensecheck", "version": VERSION, "license": "MIT LICENSE"}


def _printLicense(licenseEnum: License) -> str:
	"""Output a license as plain text.

	:param License licenseEnum: License
	:return str: license of plain text
	"""

	licenseMap = {
		License.PUBLIC: "PUBLIC DOMAIN/ CC-PDDC/ CC0-1.0",
		License.UNLICENSE: "UNLICENSE/ WTFPL",
		License.BOOST: "BOOST/ BSL-1.0",
		License.MIT: "MIT",
		License.BSD: "BSD",
		License.ISC: "ISC",
		License.NCSA: "NCSA",
		License.PSFL: "PYTHON/ PSF-2.0",
		License.APACHE: "APACHE",
		License.ECLIPSE: "ECLIPSE",
		License.ACADEMIC_FREE: "AFL",
		License.LGPL_2_PLUS: "LGPLV2+/ LGPL-2.0-OR-LATER",
		License.LGPL_3_PLUS: "LGPLV3+/ LGPL-3.0-OR-LATER",
		License.LGPL_2: "LGPL-2.0-ONLY/ LGPLV2",
		License.LGPL_3: "LGPL-3.0-ONLY/ LGPLV3",
		License.LGPL_X: "LGPL",
		License.AGPL_3_PLUS: "AGPL",
		License.GPL_2_PLUS: "GPL-2.0-OR-LATER/ GPLV2+",
		License.GPL_3_PLUS: "GPL-3.0-OR-LATER/ GPLV3+",
		License.GPL_2: "GPLV2/ GPL-2.0",
		License.GPL_3: "GPLV3/ GPL-3.0",
		License.GPL_X: "GPL",
		License.MPL: "MPL",
		License.EU: "EUPL",
		License.PROPRIETARY: "PROPRIETARY",
		License.NO_LICENSE: "NO LICENSE/ UNKNOWN",
	}

	if licenseEnum not in licenseMap:
		return "NO LICENSE/ UNKNOWN LICENSE"

	return f"{licenseMap[licenseEnum]} LICENSE"


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


def ansi(
	myLice: License,
	packages: list[dict[str, Any]],
) -> str:
	"""Format to ansi.

	:param License myLice: project license
	:param list[dict[str, Any]] packages: list of PackageCompats to format.
	:return str: string to send to specified output in ansi format
	"""

	string = StringIO()

	console = Console(file=string, color_system="truecolor", safe_box=False)

	table = Table(title="\nInfo")
	table.add_column("Item", style="cyan")
	table.add_column("Value", style="magenta")
	_ = [table.add_row(k, v) for k, v in INFO.items()]
	table.add_row("project_license", _printLicense(myLice))

	console.print(table)

	if len(packages) == 0:
		return f"{string.getvalue()}\nNo packages"

	errors = [x for x in packages if x.get("errorCode", 0) > 0]
	if len(errors) > 0:
		table = Table(title="\nList Of Errors")
		table.add_column("Package", style="magenta")
		_ = [table.add_row(x.get("name", "?")) for x in errors]
		console.print(table)

	table = Table(title="\nList Of Packages")
	if licensecompat_bool := "licenseCompat" in packages[0]:
		table.add_column("Compatible", style="cyan")
	if name_bool := "name" in packages[0]:
		table.add_column("Package", style="magenta")
	if license_bool := "license" in packages[0]:
		table.add_column("License(s)", style="magenta")
	licenseCompat = (
		"[red]✖[/]",
		"[green]✔[/]",
	)
	_ = [
		table.add_row(
			*(
				([licenseCompat[x.get("licenseCompat", 0)]] if licensecompat_bool else [])
				+ ([x.get("name")] if name_bool else [])
				+ ([x.get("license")] if license_bool else [])
			)
		)
		for x in packages
	]
	console.print(table)
	return string.getvalue()


def plainText(
	myLice: License,
	packages: list[dict[str, Any]],
) -> str:
	"""Format to plain text.

	:param License myLice: project license
	:param list[dict[str, Any]] packages: list of PackageCompats to format.
	:return str: string to send to specified output in plain text format

	"""
	return stripAnsi(ansi(myLice, packages))


def markdown(
	myLice: License,
	packages: list[dict[str, Any]],
) -> str:
	"""Format to markdown.

	:param License myLice: project license
	:param list[dict[str, Any]] packages: list of PackageCompats to format.
	:return str: string to send to specified output in markdown format
	"""

	info = "\n".join(f"- {k}: {v}" for k, v in INFO.items())
	strBuf = [f"## Info\n\n{info}\n\n## Project License\n\n{_printLicense(myLice)}\n"]

	if len(packages) == 0:
		return f"{strBuf[0]}\nNo packages"

	strBuf.append("## Packages\n\nFind a list of packages below\n")
	packages = sorted(packages, key=lambda i: i.get("name", "?"))

	# Summary Table
	strBuf.append("|Compatible|Package|\n|:--|:--|")
	strBuf.extend(
		[f"|{'✔' if pkg.get('licenseCompat') else '✖'}|{pkg.get('name')}|" for pkg in packages]
	)

	# Details
	params_use_in_markdown = {
		"homePage": "HomePage",
		"author": "Author",
		"license": "License",
		"licenseCompat": "Compatible",
		"size": "Size",
	}
	for pkg in packages:
		pkg_ordered_dict = OrderedDict(
			(param, pkg[param]) for param in params_use_in_markdown if param in pkg
		)
		strBuf.extend(
			[
				f"\n### {pkg.get('namever')}\n",
				*(f"- {params_use_in_markdown[k]}: {v}" for k, v in pkg_ordered_dict.items()),
			]
		)
	return "\n".join(strBuf) + "\n"


def html(
	myLice: License,
	packages: list[dict[str, Any]],
) -> str:
	"""Format to html.

	:param License myLice: project license
	:param list[dict[str, Any]] packages: list of PackageCompats to format.
	:return str: string to send to specified output in html format
	"""
	html = markdownlib.markdown(
		markdown(myLice=myLice, packages=packages),
		extensions=["tables"],
	)
	return (THISDIR / "html.template").read_text("utf-8").replace("{html}", html)


def raw(myLice: License, packages: list[dict[str, Any]]) -> str:
	"""Format to json.

	:param License myLice: project license
	:param list[dict[str, Any]] packages: list of PackageCompats to format.
	:return str: string to send to specified output in json format
	"""

	return json.dumps(
		{
			"info": INFO,
			"project_license": _printLicense(myLice),
			"packages": packages,
		},
		indent="\t",
	)


def rawCsv(
	myLice: License,
	packages: list[dict[str, Any]],
) -> str:
	"""Format to csv.

	:param License myLice: project license
	:param list[dict[str, Any]] packages: list of PackageCompats to format.
	:return str: string to send to specified output in csv format
	"""

	_ = myLice
	string = StringIO()
	writer = csv.DictWriter(string, fieldnames=list(packages[0]), lineterminator="\n")
	writer.writeheader()
	writer.writerows(packages)
	return string.getvalue()


def fmt(
	format_: str,
	myLice: License,
	packages: list[PackageInfo],
	hide_parameters: list[ucstr] | None = None,
	*,
	show_only_failing: bool = False,
) -> str:
	"""Format to a given format by `format_`.

	:param License myLice: project license
	:param list[PackageInfo] packages: list of PackageCompats to format.
	:param list[ucstr] hide_parameters: list of parameters to ignore in the output.
	:param bool show_only_failing: output only failing packages, defaults to False.
	:return str: string to send to specified output in ansi format
	"""
	hide_parameters = hide_parameters or []
	if show_only_failing:
		packages = [x for x in packages if not x.licenseCompat]

	pkgs: list[dict[str, Any]] = [x.get_filtered_dict(hide_parameters) for x in packages]

	return formatMap.get(format_, plainText)(myLice, pkgs)


formatMap = {
	"json": raw,
	"markdown": markdown,
	"html": html,
	"csv": rawCsv,
	"ansi": ansi,
	"simple": plainText,
}
