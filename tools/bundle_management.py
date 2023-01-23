from tools.ios_app import APPLICATION_BUNDLES
from tools.utils import read_file
from tools.ios_app import AppInfo
from re import findall, sub
from pathlib import Path

# Utilities for processing applications info


def prepare_paths(applications_ids: str) -> list:
    bundle_ids = applications_ids.split("\n")
    if not bundle_ids:
        return []

    plists = list()
    for bundle_id in bundle_ids:
        if not bundle_id:
            continue

        plist_path = f"{APPLICATION_BUNDLES}/{bundle_id}/"
        plists.append(AppInfo(bundle_id, plist_path))

    return plists


def find_app_internal_name(listed_files: str) -> str:
    coincidences = findall(r".+[.]app", listed_files)
    if coincidences:
        return coincidences[0].strip()


def find_properties(file_path: Path) -> dict:
    data = read_file(file_path)
    if not data:
        return dict()

    properties = dict()
    properties_host_keys = ["CFBundleName", "CFBundleIdentifier", "CFBundleShortVersionString"]
    properties_local_keys = ["app_name", "app_bundle", "app_version"]

    for host_key, local_key in zip(properties_host_keys, properties_local_keys):
        coincidences = findall(f"<key>{host_key}" + r"</key>\W+<string>.*</string>", data)
        if coincidences:
            property_value = sub(f"<key>{host_key}" + r"</key>\W+<string>", "", coincidences[0])
            property_value = sub(r"</string>", "", property_value).strip()
            properties[local_key] = property_value

    return properties
