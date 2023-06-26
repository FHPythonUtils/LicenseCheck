from pathlib import Path

from licensecheck import formatter, types

THISDIR = str(Path(__file__).resolve().parent)


simplePackages = [types.PackageInfo(name="example")]
complexPackages = [
	types.PackageInfo(
		name="example0",
		version="1.0.0",
		size=10,
		homePage="https://example.com",
		author="example_author",
		license="mit",
		licenseCompat=True,
		errorCode=0,
	),
	types.PackageInfo(
		name="example1",
		size=10,
		homePage="https://example.com",
		author="example_author",
		license="gpl3",
		licenseCompat=False,
		errorCode=1,
	),
]
myLice = types.License.MIT


def test_simpleMarkdown():
	fmt = formatter.markdown(myLice, simplePackages)
	# Path(f"{THISDIR}/data/simple.md").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.md").read_text("utf-8")


def test_advancedMarkdown():
	fmt = formatter.markdown(myLice, complexPackages)
	# Path(f"{THISDIR}/data/advanced.md").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.md").read_text("utf-8")


def test_simpleRaw():
	fmt = formatter.raw(myLice, simplePackages)
	# Path(f"{THISDIR}/data/simple.json").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.json").read_text("utf-8")


def test_advancedRaw():
	fmt = formatter.raw(myLice, complexPackages)
	# Path(f"{THISDIR}/data/advanced.json").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.json").read_text("utf-8")


def test_simpleRawCsv():
	fmt = formatter.rawCsv(myLice, simplePackages)
	# Path(f"{THISDIR}/data/simple.csv").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.csv").read_text("utf-8")


def test_advancedRawCsv():
	fmt = formatter.rawCsv(myLice, complexPackages)
	# Path(f"{THISDIR}/data/advanced.csv").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.csv").read_text("utf-8")


def test_simpleAnsi():
	fmt = formatter.ansi(myLice, simplePackages)
	# Path(f"{THISDIR}/data/simple.ansi").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.ansi").read_text("utf-8")


def test_advancedAnsi():
	fmt = formatter.ansi(myLice, complexPackages)
	# Path(f"{THISDIR}/data/advanced.ansi").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.ansi").read_text("utf-8")


def test_simplePlainText():
	fmt = formatter.plainText(myLice, simplePackages)
	# Path(f"{THISDIR}/data/simple.txt").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.txt").read_text("utf-8")


def test_advancedPlainText():
	fmt = formatter.plainText(myLice, complexPackages)
	# Path(f"{THISDIR}/data/advanced.txt").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.txt").read_text("utf-8")
