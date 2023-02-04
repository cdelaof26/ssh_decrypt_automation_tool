from pathlib import Path

# Utilities for apps management

LOCAL_CACHE_DIR = Path().cwd().joinpath("cache")
APPLICATION_BUNDLES = "/var/containers/Bundle/Application"
MOBILE_DOCUMENTS = "/var/mobile/Documents"
DUMPED_APPS = MOBILE_DOCUMENTS + "/Dumped"


def is_there_any_cache() -> int:
    global LOCAL_CACHE_DIR
    if LOCAL_CACHE_DIR.exists():
        return len(list(LOCAL_CACHE_DIR.iterdir()))

    return 0


def clear_cache():
    global LOCAL_CACHE_DIR
    if not LOCAL_CACHE_DIR.exists():
        return

    for cache in LOCAL_CACHE_DIR.iterdir():
        cache.unlink()


# This class holds various information about
# installed apps

class AppInfo:
    def __init__(self, bundle_id: str, host_plist_path: str):
        self.bundle_id: str = bundle_id
        self.bundle_path: str = host_plist_path

        self.host_plist_path: str = host_plist_path
        self.local_plist_path: Path
        self.app_name: str = ""
        self.app_bundle: str = ""
        self.app_version: str = ""
