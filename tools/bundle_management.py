from tools.ios_app import APPLICATION_BUNDLES, AppInfo

# Utilities for processing applications info


def find_metadata_plist(applications_ids: str) -> list:
    bundle_ids = applications_ids.split("\n")
    if not bundle_ids:
        return []

    plists = list()
    for bundle_id in bundle_ids:
        if not bundle_id:
            continue

        plist_path = f"{APPLICATION_BUNDLES}/{bundle_id}/iTunesMetadata.plist"
        plists.append(AppInfo(bundle_id, plist_path))

    return plists

