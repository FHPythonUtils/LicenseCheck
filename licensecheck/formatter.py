"""Take our package compat dictionary and give things a pretty format.

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
"""
from __future__ import annotations

from csv import writer
from io import StringIO
from json import dumps

from licensecheck.types import PackageCompat

logger = None
try:
	from metprint import Logger, LogType

	logger = Logger()
except ModuleNotFoundError:
	pass


def markdown(packages: list[PackageCompat], heading: str | None = None) -> str:
	"""Format to Markdown.

	Args:
		packages (list[PackageCompat]): PackageCompats to format
		heading (str, optional): Optional heading to include. Defaults to None.

	Returns:
		str: String to write to a file of stdout
	"""
	if len(packages) == 0:
		return "No packages"

	heading = heading if heading is not None else "# Packages\nFind a list of packages below"
	strBuf = [heading]
	packages = sorted(packages, key=lambda i: i["name"])

	# Summary Table
	strBuf.append("")
	strBuf.append("|Compatible|Package|\n|:--|:--|")
	for pkg in packages:
		strBuf.append(f"|{pkg['license_compat']}|{pkg['name']}|")
	strBuf.append("")

	# Details
	for pkg in packages:
		strBuf.extend(
			[
				f"## {pkg['namever']}",
				f"\n\n- HomePage: {pkg['home_page']}",
				f"\n- Author: {pkg['author']}",
				f"\n- License: {pkg['license']}",
				f"\n- Compatible: {pkg['license_compat']}",
				f"\n- Size: {pkg['size']}",
			]
		)
	return "\n".join(strBuf) + "\n"


def json(packages: list[PackageCompat], heading: str | None = None) -> str:
	"""Format to Json.

	Args:
		packages (list[PackageCompat]): PackageCompats to format
		heading (str, optional): Optional heading to include. Defaults to None.

	Returns:
		str: String to write to a file of stdout
	"""
	packages = sorted(packages, key=lambda i: i["name"])
	out = {
		"heading": (
			heading if heading is not None else "# Packages - Find a list of packages below"
		),
		"packages": packages,
	}
	return dumps(out, indent="\t")


def csv(packages: list[PackageCompat], heading: str | None = None) -> str:
	"""Format to CSV.

	Args:
		packages (list[PackageCompat]): PackageCompats to format
		heading (str, optional): Optional heading to include. Defaults to None.

	Returns:
		str: String to write to a file of stdout
	"""
	packages = sorted(packages, key=lambda i: i["name"])
	output = StringIO()
	csvString = writer(output)
	csvString.writerow(
		[
			(
				heading
				if heading is not None
				else "# Packages - Find a list of packages below "
				"(you may want to delete this line)"
			)
		]
	)
	csvString.writerow(
		["name", "version", "namever", "home_page", "author", "size", "license", "license_compat"]
	)
	for pkg in packages:
		csvString.writerow(
			[
				pkg["name"],
				pkg["version"],
				pkg["namever"],
				pkg["home_page"],
				pkg["author"],
				pkg["size"],
				pkg["license"],
				pkg["license_compat"],
			]
		)
	return output.getvalue()


def ansi(packages: list[PackageCompat], heading: str | None = None) -> str:
	"""Format to ansi.

	Args:
		packages (list[PackageCompat]): PackageCompats to format
		heading (str, optional): Optional heading to include. Defaults to None.

	Returns:
		str: String to write to a file of stdout
	"""
	# pylint: disable=invalid-name
	BLD = "\033[01m"
	CLS = "\033[00m"
	UL = "\033[04m"
	CB = "\033[36m"
	CG = "\033[32m"

	if len(packages) == 0:
		return f"{BLD}{UL}{CB}No packages{CLS}"

	# pylint: enable=invalid-name
	heading = (
		heading
		if heading is not None
		else f"{BLD}{UL}{CB}PackageCompats{CLS}\n\nFind a list of packages below\n"
	)
	strBuf = [heading]
	packages = sorted(packages, key=lambda i: i["name"])

	# Summary Table
	strBuf.append(f"┌{'─'*10}┬{'─'*30}┐")
	strBuf.append("│Compatible│Package                       │")
	strBuf.append(f"├{'─'*10}┼{'─'*30}┤")
	for pkg in packages:
		strBuf.append(f"│{str(pkg['license_compat']): <10}│{pkg['name'][:30]: <30}│")
	strBuf.append(f"└{'─'*10}┴{'─'*30}┘")
	strBuf.append("")

	# Details
	for pkg in packages:
		strBuf.extend(
			[
				f"{BLD}{UL}{CG}{pkg['namever']}{CLS}",
				f"HomePage: {pkg['home_page']}",
				f"Author: {pkg['author']}",
				f"License: {pkg['license']}",
				f"Compatible: {pkg['license_compat']}",
				f"Size: {pkg['size']}\n",
			]
		)
	return "\n".join(strBuf)


def simple(packages: list[PackageCompat]) -> str:
	"""Format to plain text.

	Args:
		packages (list[PackageCompat]): PackageCompats to format

	Returns:
		str: String to write to a file of stdout
	"""
	packages = sorted(packages, key=lambda i: i["name"])

	# Summary Table
	if logger is None:
		strBuf = [f"┌{'─'*10}┬{'─'*20}┬{'─'*20}┐"]
		strBuf.append("│Compatible│Package             │License             │")
		strBuf.append(f"├{'─'*10}┼{'─'*20}┼{'─'*20}┤")
		for pkg in packages:
			strBuf.append(
				f"│{str(pkg['license_compat']): <10}│{pkg['name'][:20]: <20}│{pkg['license'][:20]: <20}│"
			)
		strBuf.append(f"└{'─'*10}┴{'─'*20}┴{'─'*20}┘")
	else:
		strBuf = [logger.logString(f"┌{'─'*20}┬{'─'*30}┐", LogType.NONE, True)]
		strBuf.append(
			logger.logString(
				"│Package             │License                       │", LogType.NONE, True
			)
		)
		strBuf.append(logger.logString(f"├{'─'*20}┼{'─'*30}┤", LogType.NONE, True))
		for pkg in packages:
			strBuf.append(
				logger.logString(
					f"│{pkg['name'][:20]: <20}│{pkg['license'][:30]: <30}│",
					LogType.SUCCESS if pkg["license_compat"] else LogType.ERROR,
				)
			)
		strBuf.append(logger.logString(f"└{'─'*20}┴{'─'*30}┘", LogType.NONE, True))
	return "\n".join(strBuf)


formatMap = {
	"json": json,
	"markdown": markdown,
	"csv": csv,
	"ansi": ansi,
	"simple": simple,
}
