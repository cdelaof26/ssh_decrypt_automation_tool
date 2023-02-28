from tools.ios_app import APPLICATION_BUNDLES, APPLICATION_DOCUMENTS, AppInfo

# Utilities for processing applications info


def find_plists(applications_ids: str, find_in_documents: bool) -> list:
    bundle_ids = applications_ids.split("\n")
    if not bundle_ids:
        return []

    plists = list()
    for bundle_id in bundle_ids:
        if not bundle_id:
            continue

        if find_in_documents:
            plist_path = f"{APPLICATION_DOCUMENTS + bundle_id}/.com.apple.mobile_container_manager.metadata.plist"
            plists.append(plist_path)
        else:
            plist_path = f"{APPLICATION_BUNDLES + bundle_id}/iTunesMetadata.plist"
            plists.append(AppInfo(bundle_id, plist_path))

    # find_in_documents if true:
    # will return a list of strings, if false
    # it'll return a list of AppInfo objects

    return plists
