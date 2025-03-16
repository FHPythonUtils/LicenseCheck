

## Basic Example Use




## Supported tools/ standards

Licensecheck supports a broad range of different tools and workflows. Though please note that
for some of these tools, behaviour may differ from what is expected

| Name of tool | Supported | Notes |
| ------------ | --------- | ----- |
| Poetry 2.x   | ✔         | ???   |


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
