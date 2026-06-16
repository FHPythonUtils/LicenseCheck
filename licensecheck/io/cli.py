"""Output the licenses used by dependencies and check if these are compatible with the project license."""

from __future__ import annotations

import argparse
from dataclasses import fields
from pathlib import Path
from sys import exit as sysexit
from sys import stdin, stdout

from configurator import Config
from configurator.node import ConfigNode

from licensecheck import checker, license_matrix
from licensecheck.io import fmt
from licensecheck.models.config import LC_Config
from licensecheck.models.packageinfo import PackageInfo
from licensecheck.packageinforesolver import PackageInfoManager, ProjectMetadata

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
		help=f"Output format. one of: {', '.join(x.value for x in fmt.FMT)}. default=simple",
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
		help="set of packages/dependencies to ignore (compat=True), globs are supported",
		nargs="+",
	)
	parser.add_argument(
		"--fail-packages",
		help="set of packages/dependencies to fail (compat=False), globs are supported",
		nargs="+",
	)
	parser.add_argument(
		"--ignore-licenses",
		help="set of licenses to ignore (skipped, compat may still be False)",
		nargs="+",
	)
	parser.add_argument(
		"--fail-licenses",
		help="set of licenses to fail (compat=False)",
		nargs="+",
	)
	parser.add_argument(
		"--only-licenses",
		help="set of allowed licenses (packages/dependencies with any other license will fail)",
		nargs="+",
	)
	parser.add_argument(
		"--skip-dependencies",
		help="set of packages/dependencies to skip (this sets the 'compatibility' to True)",
		nargs="+",
	)
	parser.add_argument(
		"--hide-output-parameters",
		help="set of parameters to hide from the produced output",
		nargs="+",
	)
	parser.add_argument(
		"--show-only-failing",
		help="Only output a set of incompatible/ failing packages from this lib",
		action="store_true",
	)
	parser.add_argument(
		"--pypi-api",
		help="Specify a custom pypi api endpoint, for example if using a custom pypi server",
	)
	parser.add_argument(
		"--zero",
		"-0",
		help="Return non zero exit code if an incompatible license is found, ideal for CI/CD",
		action="store_true",
	)
	args = vars(parser.parse_args())

	if args.get("format", "simple") not in fmt.FMT:
		args["format"] = "simple"

	stdin_path = Path("__stdin__")
	if not args.get("requirements_paths"):
		if stdin.isatty():
			args["requirements_paths"] = ["pyproject.toml"]
		else:
			stdin_path.write_text("\n".join(stdin.readlines()), encoding="utf-8")

	config: ConfigNode = Config()

	# (Parses in the following order:
	config_files = [
		"~/licensecheck.json",
		"~/licensecheck.toml",
		"licensecheck.json",
		"licensecheck.toml",
		"pyproject.toml",
	]

	for file in config_files:
		config += Config.from_path(file, optional=True)

	scopedData: ConfigNode = config.get("tool", {}).get("licensecheck", ConfigNode())
	licensecheckConf: LC_Config = LC_Config.model_validate({**scopedData.data, **args})

	ec = main(licensecheckConf)
	stdin_path.unlink(missing_ok=True)

	sysexit(ec)


def main(licensecheckConf: LC_Config) -> int:
	"""Test entry point."""
	exitCode = 0

	# File
	requirements_paths = licensecheckConf.requirements_paths or {"__stdin__"}
	output_file = (
		stdout
		if licensecheckConf.file == ""
		else Path(licensecheckConf.file or "").open("w", encoding="utf-8")
	)

	# Get my license
	this_license_text = licensecheckConf.license or ProjectMetadata.get_license()
	this_license = license_matrix.licenseType(this_license_text).pop()

	package_info_manager = PackageInfoManager(licensecheckConf.pypi_api or "https://pypi.org")

	incompatible, depsWithLicenses = checker.check(
		requirements_paths=set(requirements_paths),
		groups=licensecheckConf.groups,
		extras=licensecheckConf.extras,
		this_license=this_license,
		package_info_manager=package_info_manager,
		ignore_packages=licensecheckConf.ignore_packages,
		fail_packages=licensecheckConf.fail_packages,
		ignore_licenses=licensecheckConf.ignore_licenses,
		fail_licenses=licensecheckConf.fail_licenses,
		only_licenses=licensecheckConf.only_licenses,
		skip_dependencies=licensecheckConf.skip_dependencies,
	)

	# Format the results
	hide_output_parameters = licensecheckConf.hide_output_parameters

	available_params = [param.name.upper() for param in fields(PackageInfo)]
	if not all(hop in available_params for hop in hide_output_parameters):
		msg = (
			f"Invalid parameter(s) in `hide_output_parameters`. "
			f"Valid parameters are: {', '.join(available_params)}"
		)
		raise ValueError(msg)

	if licensecheckConf.format in fmt.FMT:
		print(
			fmt.fmt(
				licensecheckConf.format,
				this_license,
				sorted(depsWithLicenses),
				hide_output_parameters,
				show_only_failing=licensecheckConf.show_only_failing,
			),
			file=output_file,
		)
	else:
		exitCode = 2

	# Exit code of 1 if args.zero
	if licensecheckConf.zero and incompatible:
		exitCode = 1

	# Cleanup + exit
	if licensecheckConf.file != "":
		output_file.close()
	return exitCode
