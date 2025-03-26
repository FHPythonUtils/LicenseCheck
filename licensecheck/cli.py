"""Output the licenses used by dependencies and check if these are compatible with the project
license.
"""

from __future__ import annotations

import argparse
from dataclasses import fields
from pathlib import Path
from sys import exit as sysexit
from sys import stdin, stdout
from configurator import Config
from configurator.node import ConfigNode
from pathlib import Path

from licensecheck import checker, fmt, license_matrix, packageinfo, types

stdout.reconfigure(encoding="utf-8")  # type: ignore[general-type-issues]


def cli() -> None:  # pragma: no cover
	"""Cli entry point."""
	parser = argparse.ArgumentParser(description=__doc__, argument_default=argparse.SUPPRESS)
	parser.add_argument(
		"--license",
		"-l",
		help="Specify the project license explicitly, rather than rely on "
		"licensecheck interpreting this from pyproject.toml",
	)
	parser.add_argument(
		"--format",
		"-f",
		help=f"Output format. one of: {', '.join(list(fmt.formatMap))}. default=simple",
	)
	parser.add_argument(
		"--requirements-paths",
		"-r",
		help="Filenames to read from (omit for stdin if piping, else pyproject.toml)",
		nargs="+",
	)
	parser.add_argument(
		"--groups",
		"-g",
		help="Select groups from supported files",
		nargs="+",
	)
	parser.add_argument(
		"--extras",
		"-e",
		help="Select extras from supported files",
		nargs="+",
	)
	parser.add_argument(
		"--file",
		"-o",
		help="Filename to write output to (omit this for stdout)",
	)
	parser.add_argument(
		"--ignore-packages",
		help="List of packages/dependencies to ignore (compat=True), globs are supported",
		nargs="+",
	)
	parser.add_argument(
		"--fail-packages",
		help="List of packages/dependencies to fail (compat=False), globs are supported",
		nargs="+",
	)
	parser.add_argument(
		"--ignore-licenses",
		help="List of licenses to ignore (skipped, compat may still be False)",
		nargs="+",
	)
	parser.add_argument(
		"--fail-licenses",
		help="List of licenses to fail (compat=False)",
		nargs="+",
	)
	parser.add_argument(
		"--only-licenses",
		help="List of allowed licenses (packages/dependencies with any other license will fail)",
		nargs="+",
	)
	parser.add_argument(
		"--skip-dependencies",
		help="List of packages/dependencies to skip (this sets the 'compatability' to True)",
		nargs="+",
	)
	parser.add_argument(
		"--hide-output-parameters",
		help="List of parameters to hide from the produced output",
		nargs="+",
	)
	parser.add_argument(
		"--show-only-failing",
		help="Only output a list of incompatible/ failing packages from this lib",
		action="store_true",
	)
	parser.add_argument(
		"--pypi-api",
		help="Specify a custom pypi api endpoint, for example if using a custom pypi server",
		default="https://pypi.org",
	)
	parser.add_argument(
		"--zero",
		"-0",
		help="Return non zero exit code if an incompatible license is found, ideal for CI/CD",
		action="store_true",
	)
	args = vars(parser.parse_args())

	stdin_path = Path("__stdin__")
	if not args.get("requirements_paths"):
		if stdin.isatty():
			args["requirements_paths"] = ["pyproject.toml"]
		else:
			stdin_path.write_text("\n".join(stdin.readlines()), encoding="utf-8")

	ec = main(args)
	stdin_path.unlink(missing_ok=True)

	sysexit(ec)


def main(args: dict) -> int:
	"""Test entry point.

	Note: FHConfParser (Parses in the following order: `pyproject.toml`,
	`setup.cfg`, `licensecheck.toml`, `licensecheck.json`,
	`licensecheck.ini`, `~/licensecheck.toml`, `~/licensecheck.json`, `~/licensecheck.ini`)
	"""
	exitCode = 0

	config: ConfigNode = Config()

	config_files = [
		"~/licensecheck.json",
		"~/licensecheck.toml",
		"licensecheck.json",
		"licensecheck.toml",
		"setup.cfg",
		"pyproject.toml",
	]

	for file in config_files:
		config += Config.from_path(file, optional=True)

	scopedData: ConfigNode = config.get("tool", default={}).get("licensecheck", default=ConfigNode())
	scopedConfig = {**scopedData.data, **args}

	# File
	requirements_paths = scopedConfig.get("requirements_paths") or ["__stdin__"]
	output_file = (
		stdout
		if scopedConfig.get("file") in [None, ""]
		else Path(scopedConfig.get("file")).open("w", encoding="utf-8")
	)

	# Get my license
	this_license_text = (
		args["license"] if args.get("license") else packageinfo.ProjectMetadata.get_license()
	)
	this_license = license_matrix.licenseType(this_license_text)[0]

	def getFromConfig(key: str) -> list[types.ucstr]:
		return list(map(types.ucstr, scopedConfig.get(key, [])))

	package_info_manager = packageinfo.PackageInfoManager(scopedConfig.get("pypi_api"))

	incompatible, depsWithLicenses = checker.check(
		requirements_paths=requirements_paths,
		groups=scopedConfig.get("groups", []),
		extras=scopedConfig.get("extras", []),
		this_license=this_license,
		package_info_manager=package_info_manager,
		ignore_packages=getFromConfig("ignore_packages"),
		fail_packages=getFromConfig("fail_packages"),
		ignore_licenses=getFromConfig("ignore_licenses"),
		fail_licenses=getFromConfig("fail_licenses"),
		only_licenses=getFromConfig("only_licenses"),
		skip_dependencies=getFromConfig("skip_dependencies"),
	)

	# Format the results
	hide_output_parameters = [
		types.ucstr(x) for x in scopedConfig.get("hide_output_parameters", [])
	]
	available_params = [param.name.upper() for param in fields(types.PackageInfo)]
	if not all(hop in available_params for hop in hide_output_parameters):
		msg = (
			f"Invalid parameter(s) in `hide_output_parameters`. "
			f"Valid parameters are: {', '.join(available_params)}"
		)
		raise ValueError(msg)
	if scopedConfig.get("format", "simple") in fmt.formatMap:
		print(
			fmt.fmt(
				scopedConfig.get("format", "simple"),
				this_license,
				sorted(depsWithLicenses),
				hide_output_parameters,
				show_only_failing=args.get("show_only_failing", False),
			),
			file=output_file,
		)
	else:
		exitCode = 2

	# Exit code of 1 if args.zero
	if scopedConfig.get("zero", False) and incompatible:
		exitCode = 1

	# Cleanup + exit
	if scopedConfig.get("file") not in [None, ""]:
		output_file.close()
	return exitCode
