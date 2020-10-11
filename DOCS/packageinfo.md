Module licensecheck.packageinfo
===============================
Get information for installed and online packages

Functions
---------

    
`calcContainer(path: str) ‑> int`
:   Get size of installed module from path
    
    Args:
            path (str): path to the module
    
    Returns:
            int: size in bytes

    
`getModuleSize(pkg: Distribution) ‑> int`
:   Get the size of a given module as an int
    
    Args:
            pkg (Distribution): package to get the size of
    
    Returns:
            int: size in bytes

    
`getMyPackageLicense() ‑> str`
:   get the pyproject data
    
    Returns:
            str: license name

    
`getPackages(reqs: list[str]) ‑> list`
:   Get dependency info
    
    Args:
            reqs (list[str]): list of dependency names to gather info on
    
    Returns:
            list[PackageInfo]: list of dependencies

    
`getPackagesFromLocal(requirements: list[str]) ‑> list`
:   Get a list of package info from local files including version, author, and
    the license
    
    Args:
            requirements (list[str]): [description]
    
    Returns:
            list[PackageInfo]: [description]

    
`getPackagesFromOnline(requirements: list[str]) ‑> list`
:   Get a list of package info from pypi.org including version, author, and
    the license
    
    Args:
            requirements (list[str]): [description]
    
    Returns:
            list[PackageInfo]: [description]

    
`licenseFromClassifierMessage(message: Message) ‑> str`
:   Get license string from a Message of project classifiers
    
    Args:
            classifiers (Message): Message of classifiers
    
    Returns:
            str: the license name

    
`licenseFromClassifierlist(classifiers: list[str]) ‑> str`
:   Get license string from a list of project classifiers
    
    Args:
            classifiers (list[str]): list of classifiers
    
    Returns:
            str: the license name

Classes
-------

`PackageInfo(*args, **kwargs)`
:   PackageInfo type

    ### Ancestors (in MRO)

    * builtins.dict

    ### Class variables

    `author: str`
    :

    `home_page: str`
    :

    `license: str`
    :

    `name: str`
    :

    `namever: str`
    :

    `size: int`
    :

    `version: str`
    :