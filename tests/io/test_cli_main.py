from pathlib import Path
from typing import Any, Literal

import pytest

from licensecheck.io.cli import ExitCode, main
from licensecheck.models.config import LC_Config


@pytest.fixture
def config() -> LC_Config:
	return LC_Config(
		requirements_paths={"requirements.txt"},
		file=None,
		license="MIT",
		pypi_api=None,
		groups=set(),
		extras=set(),
		ignore_packages=set(),
		fail_packages=set(),
		ignore_licenses=set(),
		fail_licenses=set(),
		only_licenses=set(),
		skip_dependencies=set(),
		hide_output_parameters=set(),
		format="simple",
		show_only_failing=False,
		zero=False,
	)


@pytest.fixture
def config_invalid_fmt() -> LC_Config:
	return LC_Config(
		requirements_paths={"requirements.txt"},
		file=None,
		license="MIT",
		pypi_api=None,
		groups=set(),
		extras=set(),
		ignore_packages=set(),
		fail_packages=set(),
		ignore_licenses=set(),
		fail_licenses=set(),
		only_licenses=set(),
		skip_dependencies=set(),
		hide_output_parameters=set(),
		format="invalid_format",
		show_only_failing=False,
		zero=False,
	)


def test_main_success(
	config: LC_Config,
	monkeypatch,
) -> None:
	monkeypatch.setattr(
		"licensecheck.io.cli.checker.check",
		lambda **_: (False, []),
	)

	monkeypatch.setattr(
		"licensecheck.io.cli.fmt.formatMap",
		{"simple": object()},
	)

	monkeypatch.setattr(
		"licensecheck.io.cli.fmt.fmt",
		lambda *_args, **_kwargs: "output",
	)

	assert main(config) == ExitCode.SUCCESS


def test_main_invalid_format(
	config_invalid_fmt: LC_Config,
	monkeypatch,
) -> None:

	monkeypatch.setattr(
		"licensecheck.io.cli.checker.check",
		lambda **_: (False, []),
	)

	monkeypatch.setattr(
		"licensecheck.io.cli.fmt.formatMap",
		{},
	)

	assert main(config_invalid_fmt) == ExitCode.SUCCESS


@pytest.mark.parametrize(
	("zero", "incompatible", "expected"),
	[
		(False, False, ExitCode.SUCCESS),
		(False, True, ExitCode.SUCCESS),
		(True, False, ExitCode.NO_PACKAGES),
		(True, True, ExitCode.INCOMPATIBLE_LICENSE),
	],
)
def test_main_exit_code_zero_mode(
	config: LC_Config,
	monkeypatch,
	*,
	zero: bool,
	incompatible: bool,
	expected: int,
) -> None:
	config.zero = zero

	monkeypatch.setattr(
		"licensecheck.io.cli.checker.check",
		lambda **_: (incompatible, []),
	)

	monkeypatch.setattr(
		"licensecheck.io.cli.fmt.formatMap",
		{"simple": object()},
	)

	monkeypatch.setattr(
		"licensecheck.io.cli.fmt.fmt",
		lambda *_args, **_kwargs: "",
	)

	assert main(config) == expected


def test_main_invalid_hidden_parameter(
	config: LC_Config,
	monkeypatch,
) -> None:
	config.hide_output_parameters = {"NOT_A_FIELD"}

	monkeypatch.setattr(
		"licensecheck.io.cli.checker.check",
		lambda **_: (False, []),
	)

	with pytest.raises(
		ValueError,
		match="Invalid parameter",
	):
		main(config)


@pytest.mark.parametrize(
	"hidden",
	[
		[],
		["LICENSE"],
		["LICENSE", "NAME"],
	],
)
def test_main_valid_hidden_parameters(
	config: LC_Config,
	monkeypatch,
	hidden: list[str],
) -> None:
	config.hide_output_parameters = hidden

	monkeypatch.setattr(
		"licensecheck.io.cli.checker.check",
		lambda **_: (False, []),
	)

	monkeypatch.setattr(
		"licensecheck.io.cli.fmt.formatMap",
		{"simple": object()},
	)

	monkeypatch.setattr(
		"licensecheck.io.cli.fmt.fmt",
		lambda *_args, **_kwargs: "",
	)

	assert main(config) == ExitCode.SUCCESS


def test_main_passes_args_to_checker(
	config: LC_Config,
	monkeypatch,
) -> None:
	called = {}

	def fake_check(**kwargs: dict[str, Any]) -> tuple[Literal[False], list[Any]]:
		called.update(kwargs)
		return False, []

	monkeypatch.setattr(
		"licensecheck.io.cli.checker.check",
		fake_check,
	)

	monkeypatch.setattr(
		"licensecheck.io.cli.fmt.formatMap",
		{"simple": object()},
	)

	monkeypatch.setattr(
		"licensecheck.io.cli.fmt.fmt",
		lambda *_args, **_kwargs: "",
	)

	main(config)

	assert called["groups"] == config.groups
	assert called["extras"] == config.extras
	assert called["skip_dependencies"] == config.skip_dependencies


def test_main_closes_output_file(
	config: LC_Config,
	monkeypatch,
	tmp_path: Path,
) -> None:
	output = tmp_path / "out.txt"

	config.file = str(output)

	monkeypatch.setattr(
		"licensecheck.io.cli.checker.check",
		lambda **_: (False, []),
	)

	monkeypatch.setattr(
		"licensecheck.io.cli.fmt.formatMap",
		{"simple": object()},
	)

	monkeypatch.setattr(
		"licensecheck.io.cli.fmt.fmt",
		lambda *_args, **_kwargs: "hello",
	)

	assert main(config) == ExitCode.SUCCESS
	assert output.read_text() == "hello\n"
