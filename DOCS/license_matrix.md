Module licensecheck.license_matrix
==================================
Define a foss compatability license_matrix

Standard disclaimer:: I am not a lawyer and there is no guarentee that the
information provided here is complete or correct. Do not take this as legal
advice on foss license compatability

https://en.wikipedia.org/wiki/IANAL

Types of license/ compatability

Public Domain
- Unlicense

Permissive Compatible
Permissive license compatible with gpl
- Mit
- Boost
- Bsd
- Isc
- Ncsa

Permissive Not Compatible
Permissive license NOT compatible with gpl
- Apache
- Eclipse
- Acedemic Free

Copyleft
permissive -> lgpl 2.1 -> gpl 2
permissive -> lgpl 3 -> gpl 3 -> agpl
permissive -> mpl -> gpl -> agpl (3 only)

permissive (any) -> EU
EU -> gpl -> agpl (3 only)

Functions
---------

    
`depCompatibleLice(myLicense: License, depLice: list[License]) ‑> bool`
:   Identify if the end user license is compatible with the dependency
    license(s)
    
    Args:
            myLicense (License): end user license to check
            depLice (list[License]): dependency license
    
    Returns:
            bool: True if compatible, otherwise False

    
`licenseType(lice: str) ‑> list`
:   Return a list of license types from a license string
    
    Args:
            lice (str): license name
    
    Returns:
            list[License]: the license

Classes
-------

`License(value, names=None, *, module=None, qualname=None, type=None, start=1)`
:   License Enum to hold a set of potential licenses

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `ACEDEMIC_FREE`
    :

    `AGPL_3_PLUS`
    :

    `APACHE`
    :

    `BOOST`
    :

    `BSD`
    :

    `ECLIPSE`
    :

    `EU`
    :

    `GPL_2`
    :

    `GPL_2_PLUS`
    :

    `GPL_3`
    :

    `GPL_3_PLUS`
    :

    `GPL_X`
    :

    `ISC`
    :

    `LGPL_2`
    :

    `LGPL_2_PLUS`
    :

    `LGPL_3`
    :

    `LGPL_3_PLUS`
    :

    `LGPL_X`
    :

    `MIT`
    :

    `MPL`
    :

    `NCSA`
    :

    `NO_LICENSE`
    :

    `PUBLIC`
    :

    `UNLICENSE`
    :