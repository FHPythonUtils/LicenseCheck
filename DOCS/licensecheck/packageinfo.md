# packageinfo

> Auto-generated documentation for [licensecheck.packageinfo](../../licensecheck/packageinfo.py) module.

Get information for installed and online packages.

- [Licensecheck](../README.md#licensecheck-index) / [Modules](../README.md#licensecheck-modules) / [licensecheck](index.md#licensecheck) / packageinfo
    - [PackageInfo](#packageinfo)
    - [calcContainer](#calccontainer)
    - [getModuleSize](#getmodulesize)
    - [getMyPackageLicense](#getmypackagelicense)
    - [getPackages](#getpackages)
    - [getPackagesFromLocal](#getpackagesfromlocal)
    - [getPackagesFromOnline](#getpackagesfromonline)
    - [licenseFromClassifierMessage](#licensefromclassifiermessage)
    - [licenseFromClassifierlist](#licensefromclassifierlist)

## PackageInfo

[[find in source code]](../../licensecheck/packageinfo.py#L22)

```python
class PackageInfo(typing.TypedDict):
```

PackageInfo type.

## calcContainer

[[find in source code]](../../licensecheck/packageinfo.py#L201)

```python
def calcContainer(path: str) -> int:
```

Get size of installed module from path.

#### Arguments

- `path` *str* - path to the module

#### Returns

- `int` - size in bytes

## getModuleSize

[[find in source code]](../../licensecheck/packageinfo.py#L218)

```python
def getModuleSize(pkg: Distribution) -> int:
```

Get the size of a given module as an int.

#### Arguments

- `pkg` *Distribution* - package to get the size of

#### Returns

- `int` - size in bytes

## getMyPackageLicense

[[find in source code]](../../licensecheck/packageinfo.py#L174)

```python
def getMyPackageLicense() -> str:
```

Get the pyproject data.

#### Returns

- `str` - license name

## getPackages

[[find in source code]](../../licensecheck/packageinfo.py#L158)

```python
def getPackages(reqs: list[str]) -> list[PackageInfo]:
```

Get dependency info.

#### Arguments

- `reqs` *list[str]* - list of dependency names to gather info on

#### Returns

- `list[PackageInfo]` - list of dependencies

## getPackagesFromLocal

[[find in source code]](../../licensecheck/packageinfo.py#L34)

```python
def getPackagesFromLocal(requirements: list[str]) -> list[PackageInfo]:
```

Get a list of package info from local files including version, author...

and	the license.

#### Arguments

- `requirements` *list[str]* - [description]

#### Returns

- `list[PackageInfo]` - [description]

## getPackagesFromOnline

[[find in source code]](../../licensecheck/packageinfo.py#L105)

```python
def getPackagesFromOnline(requirements: list[str]) -> list[PackageInfo]:
```

Get a list of package info from pypi.org including version, author...

and	the license.

#### Arguments

- `requirements` *list[str]* - [description]

#### Returns

- `list[PackageInfo]` - [description]

## licenseFromClassifierMessage

[[find in source code]](../../licensecheck/packageinfo.py#L83)

```python
def licenseFromClassifierMessage(message: Message) -> str:
```

Get license string from a Message of project classifiers.

#### Arguments

- `classifiers` *Message* - Message of classifiers

#### Returns

- `str` - the license name

## licenseFromClassifierlist

[[find in source code]](../../licensecheck/packageinfo.py#L136)

```python
def licenseFromClassifierlist(classifiers: list[str]) -> str:
```

Get license string from a list of project classifiers.

#### Arguments

- `classifiers` *list[str]* - list of classifiers

#### Returns

- `str` - the license name
