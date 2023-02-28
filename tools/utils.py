import plistlib
from pathlib import Path
from subprocess import call

# General utilities

CLEAR_CMD = "cls"
IS_SYSTEM_NT = True

try:
    from os import uname
    CLEAR_CMD = "clear"
    IS_SYSTEM_NT = False
except ImportError:  # uname doesn't exist in Windows
    pass


def clear_terminal():
    global CLEAR_CMD
    call(CLEAR_CMD, shell=True)


# "options" and "options_values" must have the same size
def choose(options: list, options_values=None):
    selection = ""

    while not selection:
        selection = input("> ").upper()
        if selection not in options:
            print("    Option not found!")
            print("  Please select an option in list")
            selection = ""

    if options_values is not None:
        return options_values[options.index(selection)]

    return selection


def write_file(file_path: Path, data: str) -> bool:
    try:
        with open(file_path, "w") as file:
            file.write(data)
            return True
    except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
        return False


def write_binary_file(file_path: Path, data: bytes) -> bool:
    try:
        with open(file_path, "wb") as file:
            file.write(data)
            return True
    except IsADirectoryError:
        return False


def read_file(file_path: Path) -> str:
    try:
        with open(file_path, "r") as file:
            return file.read()
    except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
        # print("    Cannot read file ", file_path)
        return ""


def read_plist_file(file_path: Path) -> dict:
    try:
        with open(file_path, "rb") as file:
            return plistlib.load(file)
    except (FileNotFoundError, IsADirectoryError):
        return dict()


def enumerate_app_list(apps: list) -> list:
    enumerated_apps = ""
    enumerated_apps_as_options = list()
    apps_copy = apps.copy()

    i = 0
    while i < len(apps_copy):
        if apps_copy[i].app_name:
            enumerated_apps += f"{i + 1}.\t" \
                               f"{apps_copy[i].app_name}\n"
            enumerated_apps_as_options.append(f"{i + 1}")
            i += 1
        else:
            apps_copy.pop(i)

    return [enumerated_apps[:-1], enumerated_apps_as_options, apps_copy]


def select_apps(listed_applications: list, select_multiple_apps):
    clear_terminal()
    input("Make sure your device is unlocked, press enter to proceed")

    selected_apps = list()
    valid_bundles = listed_applications.copy()
    while True:
        listed_apps, options, valid_bundles = enumerate_app_list(valid_bundles)
        if select_multiple_apps:
            listed_apps += "\nA. Select all"
            options += ["A"]
            valid_bundles += "A"

        listed_apps += "\nE. End"
        options += ["E"]
        valid_bundles += "E"

        print(listed_apps)
        print("Select an app")
        app = choose(options, valid_bundles)

        if select_multiple_apps:
            valid_bundles = valid_bundles[:-2]
        else:
            valid_bundles = valid_bundles[:-1]

        if isinstance(app, str):
            if app == "E":
                break

            print("\nThis might take a while!")
            selected_apps = valid_bundles
            break

        selected_apps.append(app)
        valid_bundles.remove(app)

        clear_terminal()
        if not select_multiple_apps:
            break

    if selected_apps and not select_multiple_apps:
        return selected_apps[0]
    elif not select_multiple_apps:
        return None

    return selected_apps
