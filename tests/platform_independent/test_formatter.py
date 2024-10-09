from pathlib import Path

from licensecheck import formatter
from licensecheck.types import License, PackageInfo, ucstr

formatter.INFO = {"program": "licensecheck", "version": "dev", "license": "MIT LICENSE"}

THISDIR = str(Path(__file__).resolve().parent)

# ruff: noqa: ERA001

simplePackages = [PackageInfo(name="example")]
complexPackages = [
	PackageInfo(
		name="example0",
		version="1.0.0",
		size=10,
		homePage="https://example.com",
		author="example_author",
		license=ucstr("mit"),
		licenseCompat=True,
		errorCode=0,
	),
	PackageInfo(
		name="example1",
		size=10,
		homePage="https://example.com",
		author="example_author",
		license=ucstr("gpl3"),
		licenseCompat=False,
		errorCode=1,
	),
]
myLice = License.MIT


def test_simpleMarkdown() -> None:
	fmt = formatter.markdown(myLice, simplePackages)
	# Path(f"{THISDIR}/data/simple.md").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.md").read_text("utf-8")


def test_advancedMarkdown() -> None:
	fmt = formatter.markdown(myLice, complexPackages)
	# Path(f"{THISDIR}/data/advanced.md").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.md").read_text("utf-8")


def test_advancedMarkdownIgnoreParams() -> None:
	fmt = formatter.markdown(myLice, complexPackages)
	# Path(f"{THISDIR}/data/advanced_ignore_params.md").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced_ignore_params.md").read_text("utf-8")


def test_simpleRaw() -> None:
	fmt = formatter.raw(myLice, simplePackages)
	# Path(f"{THISDIR}/data/simple.json").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.json").read_text("utf-8")


def test_advancedRaw() -> None:
	fmt = formatter.raw(myLice, complexPackages)
	# Path(f"{THISDIR}/data/advanced.json").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.json").read_text("utf-8")


def test_advancedRawIgnoreParams() -> None:
	fmt = formatter.raw(
		myLice, complexPackages, hide_parameters=[ucstr("HOMEPAGE"), ucstr("AUTHOR")]
	)
	# Path(f"{THISDIR}/data/advanced_ignore_params.json").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced_ignore_params.json").read_text("utf-8")


def test_simpleRawCsv() -> None:
	fmt = formatter.rawCsv(myLice, simplePackages)
	# Path(f"{THISDIR}/data/simple.csv").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.csv").read_text("utf-8")


def test_advancedRawCsv() -> None:
	fmt = formatter.rawCsv(myLice, complexPackages)
	# Path(f"{THISDIR}/data/advanced.csv").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.csv").read_text("utf-8")


def test_simpleAnsi() -> None:
	fmt = formatter.ansi(myLice, simplePackages)
	# Path(f"{THISDIR}/data/simple.ansi").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.ansi").read_text("utf-8")


def test_advancedAnsi() -> None:
	fmt = formatter.ansi(myLice, complexPackages)
	# Path(f"{THISDIR}/data/advanced.ansi").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.ansi").read_text("utf-8")


def test_advancedAnsiIgnoreParams() -> None:
	fmt = formatter.ansi(myLice, complexPackages, hide_parameters=[])
	assert fmt == Path(f"{THISDIR}/data/advanced.ansi").read_text("utf-8")


def test_simplePlainText() -> None:
	fmt = formatter.plainText(myLice, simplePackages)
	# Path(f"{THISDIR}/data/simple.txt").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.txt").read_text("utf-8")


def test_advancedPlainText() -> None:
	fmt = formatter.plainText(myLice, complexPackages)
	# Path(f"{THISDIR}/data/advanced.txt").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.txt").read_text("utf-8")


def test_advancedPlainTextIgnoreParams() -> None:
	fmt = formatter.plainText(myLice, complexPackages, hide_parameters=[ucstr("WRONG_PARAMETER")])
	assert fmt == Path(f"{THISDIR}/data/advanced.txt").read_text("utf-8")
