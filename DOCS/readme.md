Module licensecheck
===================
Output the licenses used by dependencies and check if these are compatible
with the project license

Sub-modules
-----------
* licensecheck.formatter
* licensecheck.license_matrix
* licensecheck.packagecompat
* licensecheck.packageinfo

Functions
---------

    
`cli() ‑> NoneType`
:   cli entry point

    
`getdepsLicenses() ‑> list`
:   Get a list of packages with package compatibility
    
    Returns:
            list[PackageCompat]: list of packages (python dicts)