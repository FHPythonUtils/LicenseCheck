import appdirs
import requests_cache

session = requests_cache.CachedSession(appdirs.user_cache_dir("licensecheck", "fredhappyface"))
