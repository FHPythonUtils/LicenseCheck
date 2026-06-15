import pytest

from licensecheck.io.cli import main
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
		lambda *args, **kwargs: "output",
	)

	assert main(config) == 0


def test_main_invalid_format(
	config: LC_Config,
	monkeypatch,
) -> None:
	config.format = "does-not-exist"

	monkeypatch.setattr(
		"licensecheck.io.cli.checker.check",
		lambda **_: (False, []),
	)

	monkeypatch.setattr(
		"licensecheck.io.cli.fmt.formatMap",
		{},
	)

	assert main(config) == 2


@pytest.mark.parametrize(
	("zero", "incompatible", "expected"),
	[
		(False, False, 0),
		(False, True, 0),
		(True, False, 0),
		(True, True, 1),
	],
)
def test_main_exit_code_zero_mode(
	config: LC_Config,
	monkeypatch,
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
		lambda *args, **kwargs: "",
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
		lambda *args, **kwargs: "",
	)

	assert main(config) == 0


def test_main_passes_args_to_checker(
	config: LC_Config,
	monkeypatch,
) -> None:
	called = {}

	def fake_check(**kwargs):
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
		lambda *args, **kwargs: "",
	)

	main(config)

	assert called["groups"] == config.groups
	assert called["extras"] == config.extras
	assert called["skip_dependencies"] == config.skip_dependencies


def test_main_closes_output_file(
	config: LC_Config,
	monkeypatch,
	tmp_path,
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
		lambda *args, **kwargs: "hello",
	)

	assert main(config) == 0
	assert output.read_text() == "hello\n"
