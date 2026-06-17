import requests_cache
from platformdirs import PlatformDirs

dirs = PlatformDirs("licensecheck", "fredhappyface")


session = requests_cache.CachedSession(dirs.user_cache_dir)
