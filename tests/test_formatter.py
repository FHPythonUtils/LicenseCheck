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


def test_simpleMarkdown():
    # Path(f"{THISDIR}/data/simple.md").write_text(formatter.markdown(simplePackages), "utf-8")
    assert formatter.markdown(simplePackages) == Path(f"{THISDIR}/data/simple.md").read_text(
        "utf-8"
    )


def test_advancedMarkdown():
    # Path(f"{THISDIR}/data/advanced.md").write_text(formatter.markdown(complexPackages), "utf-8")
    assert formatter.markdown(complexPackages) == Path(f"{THISDIR}/data/advanced.md").read_text(
        "utf-8"
    )


def test_simpleRaw():
    # Path(f"{THISDIR}/data/simple.json").write_text(formatter.raw(simplePackages), "utf-8")
    assert formatter.raw(simplePackages) == Path(f"{THISDIR}/data/simple.json").read_text("utf-8")


def test_advancedRaw():
    # Path(f"{THISDIR}/data/advanced.json").write_text(formatter.raw(complexPackages), "utf-8")
    assert formatter.raw(complexPackages) == Path(f"{THISDIR}/data/advanced.json").read_text(
        "utf-8"
    )


def test_simpleRawCsv():
    # Path(f"{THISDIR}/data/simple.csv").write_text(formatter.rawCsv(simplePackages), "utf-8")
    assert formatter.rawCsv(simplePackages) == Path(f"{THISDIR}/data/simple.csv").read_text("utf-8")


def test_advancedRawCsv():
    # Path(f"{THISDIR}/data/advanced.csv").write_text(formatter.rawCsv(complexPackages), "utf-8")
    assert formatter.rawCsv(complexPackages) == Path(f"{THISDIR}/data/advanced.csv").read_text(
        "utf-8"
    )


def test_simpleAnsi():
    # Path(f"{THISDIR}/data/simple.ansi").write_text(formatter.ansi(simplePackages), "utf-8")
    assert formatter.ansi(simplePackages) == Path(f"{THISDIR}/data/simple.ansi").read_text("utf-8")


def test_advancedAnsi():
    # Path(f"{THISDIR}/data/advanced.ansi").write_text(formatter.ansi(complexPackages), "utf-8")
    assert formatter.ansi(complexPackages) == Path(f"{THISDIR}/data/advanced.ansi").read_text(
        "utf-8"
    )


def test_simplePlainText():
    # Path(f"{THISDIR}/data/simple.txt").write_text(formatter.plainText(simplePackages), "utf-8")
    assert formatter.plainText(simplePackages) == Path(f"{THISDIR}/data/simple.txt").read_text(
        "utf-8"
    )


def test_advancedPlainText():
    # Path(f"{THISDIR}/data/advanced.txt").write_text(formatter.plainText(complexPackages), "utf-8")
    assert formatter.plainText(complexPackages) == Path(f"{THISDIR}/data/advanced.txt").read_text(
        "utf-8"
    )
