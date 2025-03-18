

## Examples from the command-line

See below for the output if you run `licensecheck` in this directory

### Pipe a requirements.txt file as input

```txt
>> cat ./requirements.txt | licensecheck

               Info
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Item            ┃ Value        ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ program         │ licensecheck │
│ version         │ 2025         │
│ license         │ MIT LICENSE  │
│ project_license │ MIT LICENSE  │
└─────────────────┴──────────────┘

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

### Using pyproject.toml (default if not piping input)

```txt
>> licensecheck
...
```

### Failing on packages under MIT license

```txt
>> licensecheck  --fail-licenses mit

               Info
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Item            ┃ Value        ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ program         │ licensecheck │
│ version         │ 2025.0.1     │
│ license         │ MIT LICENSE  │
│ project_license │ MIT LICENSE  │
└─────────────────┴──────────────┘

                              List Of Packages
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Compatible ┃ Package             ┃ License(s)                            ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ✖          │ appdirs             │ MIT LICENSE                           │
│ ✖          │ attrs               │ MIT LICENSE                           │
│ ✔          │ boolean-py          │ BSD-2-CLAUSE                          │
│ ✖          │ cattrs              │ MIT LICENSE                           │
│ ✔          │ certifi             │ MOZILLA PUBLIC LICENSE 2.0 _MPL 2.0_  │
│ ✖          │ charset-normalizer  │ MIT LICENSE                           │
│ ✔          │ colorama            │ BSD LICENSE                           │
│ ✖          │ fhconfparser        │ MIT LICENSE                           │
│ ✔          │ idna                │ BSD LICENSE                           │
│ ✔          │ license-expression  │ APACHE-2.0                            │
│ ✖          │ loguru              │ MIT LICENSE                           │
│ ✔          │ markdown            │ BSD LICENSE                           │
│ ✖          │ markdown-it-py      │ MIT LICENSE                           │
│ ✖          │ mdurl               │ MIT LICENSE                           │
│ ✔          │ packaging           │ APACHE SOFTWARE LICENSE;; BSD LICENSE │
│ ✖          │ platformdirs        │ MIT LICENSE                           │
│ ✔          │ pygments            │ BSD LICENSE                           │
│ ✔          │ requests            │ APACHE SOFTWARE LICENSE               │
│ ✔          │ requests-cache      │ BSD LICENSE                           │
│ ✔          │ requirements-parser │ APACHE SOFTWARE LICENSE               │
│ ✖          │ rich                │ MIT LICENSE                           │
│ ✖          │ setuptools          │ MIT LICENSE                           │
│ ✖          │ six                 │ MIT LICENSE                           │
│ ✖          │ tomli               │ MIT LICENSE                           │
│ ✔          │ types-setuptools    │ APACHE SOFTWARE LICENSE               │
│ ✖          │ url-normalize       │ MIT LICENSE                           │
│ ✖          │ urllib3             │ MIT LICENSE                           │
│ ✔          │ uv                  │ APACHE SOFTWARE LICENSE;; MIT LICENSE │
│ ✖          │ win32-setctime      │ MIT LICENSE                           │
└────────────┴─────────────────────┴───────────────────────────────────────┘


```

### Only allow a predefined set of licenses

```txt

>> licensecheck --only-licenses mit apache
...
                             List Of Packages
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Compatible ┃ Package             ┃ License(s)                            ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ✔          │ appdirs             │ MIT LICENSE                           │
│ ✔          │ attrs               │ MIT LICENSE                           │
│ ✖          │ boolean-py          │ BSD-2-CLAUSE                          │
│ ✔          │ cattrs              │ MIT LICENSE                           │
│ ✖          │ certifi             │ MOZILLA PUBLIC LICENSE 2.0 _MPL 2.0_  │
│ ✔          │ charset-normalizer  │ MIT LICENSE                           │
...

```



### Show only failing

```txt
>>> licensecheck  --only-licenses mit apache --show-only-failing

               Info
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Item            ┃ Value        ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ program         │ licensecheck │
│ version         │ 2025.0.1     │
│ license         │ MIT LICENSE  │
│ project_license │ MIT LICENSE  │
└─────────────────┴──────────────┘

                           List Of Packages
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Compatible ┃ Package        ┃ License(s)                           ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ✖          │ boolean-py     │ BSD-2-CLAUSE                         │
│ ✖          │ certifi        │ MOZILLA PUBLIC LICENSE 2.0 _MPL 2.0_ │
│ ✖          │ colorama       │ BSD LICENSE                          │
│ ✖          │ idna           │ BSD LICENSE                          │
│ ✖          │ markdown       │ BSD LICENSE                          │
│ ✖          │ pygments       │ BSD LICENSE                          │
│ ✖          │ requests-cache │ BSD LICENSE                          │
└────────────┴────────────────┴──────────────────────────────────────┘
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

               Info
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Item            ┃ Value        ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ program         │ licensecheck │
│ version         │ 2025.0.1     │
│ license         │ MIT LICENSE  │
│ project_license │ MIT LICENSE  │
└─────────────────┴──────────────┘

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
│ ✖          │ markdown          │ BSD LICENSE                          │
│ ✖          │ markupsafe        │ BSD LICENSE                          │
│ ✖          │ nodeenv           │ BSD LICENSE                          │
│ ✖          │ pathspec          │ MOZILLA PUBLIC LICENSE 2.0 _MPL 2.0_ │
│ ✖          │ psutil            │ BSD LICENSE                          │
│ ✖          │ pycparser         │ BSD LICENSE                          │
│ ✖          │ pygments          │ BSD LICENSE                          │
│ ✖          │ requests-cache    │ BSD LICENSE                          │
│ ✖          │ shellingham       │ ISC LICENSE _ISCL_                   │
│ ✖          │ typing-extensions │ PYTHON SOFTWARE FOUNDATION LICENSE   │
└────────────┴───────────────────┴──────────────────────────────────────┘

```
