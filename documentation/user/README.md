

## Basic Example Use

Per the main README... More examples are available [here](examples.md)

### Using pyproject.toml (default if not piping input)

```txt
>> licensecheck

...
							  List Of Packages
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Compatible ┃ Package             ┃ License(s)                            ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ✔          │ appdirs             │ MIT LICENSE                           │
│ ✔          │ attrs               │ MIT LICENSE                           │
│ ✔          │ boolean-py          │ BSD-2-CLAUSE                          │
│ ✔          │ cattrs              │ MIT LICENSE                           │
│ ✔          │ certifi             │ MOZILLA PUBLIC LICENSE 2.0 _MPL 2.0_  │
│ ✔          │ charset-normalizer  │ MIT LICENSE                           │
│ ✔          │ colorama            │ BSD LICENSE                           │
│ ✔          │ fhconfparser        │ MIT LICENSE                           │
│ ✔          │ idna                │ BSD LICENSE                           │
│ ✔          │ license-expression  │ APACHE-2.0                            │
│ ✔          │ loguru              │ MIT LICENSE                           │
│ ✔          │ markdown            │ BSD LICENSE                           │
│ ✔          │ markdown-it-py      │ MIT LICENSE                           │
│ ✔          │ mdurl               │ MIT LICENSE                           │
│ ✔          │ packaging           │ APACHE SOFTWARE LICENSE;; BSD LICENSE │
│ ✔          │ platformdirs        │ MIT LICENSE                           │
│ ✔          │ pygments            │ BSD LICENSE                           │
│ ✔          │ requests            │ APACHE SOFTWARE LICENSE               │
│ ✔          │ requests-cache      │ BSD LICENSE                           │
│ ✔          │ requirements-parser │ APACHE SOFTWARE LICENSE               │
│ ✔          │ rich                │ MIT LICENSE                           │
│ ✔          │ setuptools          │ MIT LICENSE                           │
│ ✔          │ six                 │ MIT LICENSE                           │
│ ✔          │ tomli               │ MIT LICENSE                           │
│ ✔          │ types-setuptools    │ APACHE SOFTWARE LICENSE               │
│ ✔          │ url-normalize       │ MIT LICENSE                           │
│ ✔          │ urllib3             │ MIT LICENSE                           │
│ ✔          │ uv                  │ APACHE SOFTWARE LICENSE;; MIT LICENSE │
│ ✔          │ win32-setctime      │ MIT LICENSE                           │
└────────────┴─────────────────────┴───────────────────────────────────────┘

```



### Use csv format

```csv
>>> licensecheck  --only-licenses mit apache --show-only-failing -f csv
name,version,size,homePage,author,license,licenseCompat,errorCode,namever
Markdown,3.7,361400,UNKNOWN,"Manfred Stienstra, Yuri Takhteyev",BSD LICENSE,False,0,Markdown-3.7
Pygments,2.19.1,4508396,UNKNOWN,UNKNOWN,BSD LICENSE,False,0,Pygments-2.19.1
boolean.py,4.0,109354,https://github.com/bastikr/boolean.py,Sebastian Kraemer,BSD-2-CLAUSE,False,0,boolean.py-4.0
certifi,2025.1.31,305559,https://github.com/certifi/python-certifi,Kenneth Reitz,MOZILLA PUBLIC LICENSE 2.0 _MPL 2.0_,False,0,certifi-2025.1.31
colorama,0.4.6,76299,UNKNOWN,UNKNOWN,BSD LICENSE,False,0,colorama-0.4.6
idna,3.10,349141,UNKNOWN,UNKNOWN,BSD LICENSE,False,0,idna-3.10
requests-cache,1.2.1,174099,https://github.com/requests-cache/requests-cache,Roman Haritonov,BSD LICENSE,False,0,requests-cache-1.2.1
```


### Groups

```txt
uv run licensecheck  --only-licenses mit apache --show-only-failing -g dev

...

							List Of Packages
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Compatible ┃ Package           ┃ License(s)                           ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ✖          │ authlib           │ BSD LICENSE                          │
│ ✖          │ boolean-py        │ BSD-2-CLAUSE                         │
│ ✖          │ certifi           │ MOZILLA PUBLIC LICENSE 2.0 _MPL 2.0_ │
│ ✖          │ click             │ BSD LICENSE                          │
│ ✖          │ colorama          │ BSD LICENSE                          │
│ ✖          │ filelock          │ THE UNLICENSE _UNLICENSE_            │
│ ✖          │ idna              │ BSD LICENSE                          │
│ ✖          │ jinja2            │ BSD LICENSE                          │
│ ✖          │ joblib            │ BSD LICENSE                          │
...
```


## Supported tools/ standards

Licensecheck supports a broad range of different tools and workflows. Though please note that
for some of these tools, behaviour may differ from what is expected. We use `uv` for the dependency
resolution due to the good performance across projects, with a fallback to a native parser in case of
an error, which will be logged

Note that `uv` supports requirements.in files. If a pyproject.toml, setup.py, or setup.cfg file is
provided, `uv` will extract the requirements for the relevant project. In testing this seems to have
broad support for various workflows

In addition to this, `licensecheck` will attempt to determine your project license from a `pyproject.toml` or
a `setup.cfg`

| Name of tool | Supported | Notes |
| ------------ | --------- | ----- |
| Poetry 2.x   | ✔         |    |
| Poetry 1.x   | ✔         |    |
| uv   | ✔         |    |
| flit   | ✔         |    |


### 'legacy' setup.cfg example

```ini
[metadata]
classifiers =
    License :: OSI Approved :: MIT License
    Programming Language :: Python :: 3.8
license = MIT

```

### Poetry example

```toml
[tool.poetry]
name = "mypackage"
version = "0.1.0"
description = "A simple Python package"
license = "MIT"
authors = ["Author <author@example.com>"]
classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.8"
]

[tool.poetry.dependencies]
python = "^3.8"

```

### Flit example

```toml
[tool.flit.metadata]
module = "mypackage"
description = "A simple Python package"
license = "MIT"
classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.8"
]
```

## Resolve all deps

Previous versions of the licensecheck tool implemented a custom resolver to discover packages.
Current versions look to move away from this for a number of reasons, such as correctness and
reducing the maintenance burden. Over time many contributors helped out with the custom
resolver which is very much appreciated. Now, we use `uv` to attempt to resolve deps before
falling back to the legacy approach, which is needed in certain cases where uv fails

Q: Why doesn't this use packages from my lockfile?
A: The answer to this somewhat depends on what resolver licensecheck ends up using to
find all of the packages in use by your project. Ideally, `uv` is used which has pretty
good support for pyproject.toml and some other standard requirements formats and will discover
packages. The legacy resolver is deprecated and may result in funky output in some cases

Q: The license for my dep has changed in v >1.0, so I'm using v < 1.0, why doesn't licensecheck report the correct license version?
A: In some cases it will, for example if licensecheck can find the dep metadata via importlib. Otherwise we reach out to pypi.org for this metadata. There are no plans at present to resolve this

[note to me: I 'might' look at this as we should have a copy of the package version ]

## License lookup format


At present the licenses are not looked up via the SPDX format, which would be preffred going forwards, but via a custom mapping that corresponds to a substring of the python license classifiers. The table below shows the current lookup

Some means of normalizing this, perhaps with the aid of a 3rd party lib is planned


| License Name Containing              | License Type    |
| ------------------------------------ | --------------- |
| PUBLIC DOMAIN                        | L.PUBLIC        |
| CC-PDDC                              | L.PUBLIC        |
| CC0-1.0                              | L.PUBLIC        |
| UNLICENSE                            | L.UNLICENSE     |
| WTFPL                                | L.UNLICENSE     |
| BOOST                                | L.BOOST         |
| BSL-1.0                              | L.BOOST         |
| MIT                                  | L.MIT           |
| BSD                                  | L.BSD           |
| ISC                                  | L.ISC           |
| NCSA                                 | L.NCSA          |
| PYTHON                               | L.PSFL          |
| PSF-2.0                              | L.PSFL          |
| APACHE                               | L.APACHE        |
| ECLIPSE                              | L.ECLIPSE       |
| AFL                                  | L.ACADEMIC_FREE |
| LGPLV2+                              | L.LGPL_2_PLUS   |
| LGPL-2.0-OR-LATER                    | L.LGPL_2_PLUS   |
| LGPLV3+                              | L.LGPL_3_PLUS   |
| LGPL-3.0-OR-LATER                    | L.LGPL_3_PLUS   |
| LGPL-2.0-ONLY                        | L.LGPL_2        |
| LGPLV2                               | L.LGPL_2        |
| LGPL-3.0-ONLY                        | L.LGPL_3        |
| LGPLV3                               | L.LGPL_3        |
| LGPL                                 | L.LGPL_X        |
| AGPL                                 | L.AGPL_3_PLUS   |
| GNU AFFERO GENERAL PUBLIC LICENSE V3 | L.AGPL_3_PLUS   |
| GPL-2.0-OR-LATER                     | L.GPL_2_PLUS    |
| GPLV2+                               | L.GPL_2_PLUS    |
| GPL-3.0-OR-LATER                     | L.GPL_3_PLUS    |
| GPLV3+                               | L.GPL_3_PLUS    |
| GPLV2                                | L.GPL_2         |
| GPL-2.0                              | L.GPL_2         |
| GPLV3                                | L.GPL_3         |
| GPL-3.0                              | L.GPL_3         |
| GPL                                  | L.GPL_X         |
| MPL                                  | L.MPL           |
| EUPL                                 | L.EU            |
| PROPRIETARY                          | L.PROPRIETARY   |





## Output formats

The formatter is reponsible for outputting the list of PackageInfo[s].

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


## Using in CI/CD
