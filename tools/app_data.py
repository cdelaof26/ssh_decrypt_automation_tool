import tools.utils as utils
from pathlib import Path
from enum import Enum
import shutil


class DumpUtility(Enum):
    CLUTCH = 0
    BFDECRYPT = 1
    CLUTCH_BFDECRYPT = 2
    BFDECRYPT_CLUTCH = 3


CWD_PATH = Path().cwd()

CONFIG_DIR = CWD_PATH.joinpath("config")


# If this file exist, this program will try to authenticate as soon as it starts
AUTHENTICATE_ON_STARTUP = CONFIG_DIR.joinpath("auth")

# This directory contains logs for failed dumps
FAILED_LOGS = CWD_PATH.joinpath("error_logs")


# This file just holds the last IP entered,
# If file is found, contents are read to skip having to
# enter the IP again
IP_FILE = CONFIG_DIR.joinpath("ip.txt")

# This file holds username and password if user decides to save them as plain text
# (not recommend)
UP_FILE = CONFIG_DIR.joinpath("up.txt")

DECRYPT_METHOD_CONFIG = CONFIG_DIR.joinpath("d_method")
decrypt_method = ""

CLUTCH_EXECUTABLE = CWD_PATH.joinpath("Clutch_troll")
BFDECRYPT_DEB = CWD_PATH.joinpath("bfdecrypt.deb")
DOWNLOADED_APPS = CWD_PATH.joinpath("IPAs")


def read_ip_file() -> str:
    global IP_FILE
    if not IP_FILE.exists():
        return ""

    return utils.read_file(IP_FILE)


def save_ip_file(ip: str):
    global IP_FILE
    utils.write_file(IP_FILE, ip)


def read_up_file() -> list:
    global UP_FILE
    if not UP_FILE.exists():
        return []

    return utils.read_file(UP_FILE).split("\n")


def save_up_file(usr: str, pwd: str):
    global UP_FILE
    utils.write_file(UP_FILE, usr + "\n" + pwd)


def does_clutch_exist() -> bool:
    global CLUTCH_EXECUTABLE, DECRYPT_METHOD_CONFIG
    if not CLUTCH_EXECUTABLE.exists():
        print(f"\"{CLUTCH_EXECUTABLE.resolve()}\" doesn't exist")
        return False

    if not DECRYPT_METHOD_CONFIG.exists():
        select_decrypt_utility("1")

    return True


def does_bfdecrypt_exist() -> bool:
    global BFDECRYPT_DEB
    if not BFDECRYPT_DEB.exists():
        print(f"\"{BFDECRYPT_DEB.resolve()}\" doesn't exist")
        return False

    return True


def get_file_copy(copy_as_clutch: bool):
    global CLUTCH_EXECUTABLE, BFDECRYPT_DEB

    utils.clear_terminal()
    print("Drag and drop the file")

    if not utils.IS_SYSTEM_NT:
        file = Path(input("> ").replace("\\", "").strip())
    else:
        file = Path(input("> ").strip())

    if file.is_dir():
        return False

    if file.exists():
        if copy_as_clutch:
            shutil.copy(str(file), str(CLUTCH_EXECUTABLE))
        else:
            shutil.copy(str(file), str(BFDECRYPT_DEB))

    if copy_as_clutch:
        return CLUTCH_EXECUTABLE.exists()
    return BFDECRYPT_DEB.exists()


def write_log(log: str):
    global FAILED_LOGS
    if not FAILED_LOGS.exists():
        FAILED_LOGS.mkdir()

    log_file = FAILED_LOGS.joinpath("dump_log.txt")
    i = 0
    while log_file.exists():
        log_file = FAILED_LOGS.joinpath(f"dump_log ({i}).txt")
        i += 1

    utils.write_file(log_file, log)


def read_decrypt_method_config():
    global DECRYPT_METHOD_CONFIG, decrypt_method
    if DECRYPT_METHOD_CONFIG.exists():
        decrypt_method = utils.read_file(DECRYPT_METHOD_CONFIG)
        try:
            DumpUtility[decrypt_method]
        except KeyError:
            print(f"  Invalid decrypt mode! ({decrypt_method})")
            print("Please, reconfigure decrypt method in settings")
            DECRYPT_METHOD_CONFIG.unlink()


def select_decrypt_utility(option=None):
    global DECRYPT_METHOD_CONFIG, decrypt_method

    utils.clear_terminal()

    if option is None:
        print("  Select the utility to use")
        print("1. Clutch")
        print("2. bfdecrypt")
        print("3. Clutch -> bfdecrypt as fallback")
        print("4. bfdecrypt -> Clutch as fallback")
        print("5. Cancel")
        print("Select an option")
        option = utils.choose(["1", "2", "3", "4", "5"])

    if option == "5":
        return

    if option == "1":
        decrypt_method = DumpUtility.CLUTCH.name
    elif option == "2":
        decrypt_method = DumpUtility.BFDECRYPT.name
    elif option == "3":
        decrypt_method = DumpUtility.CLUTCH_BFDECRYPT.name
    else:
        decrypt_method = DumpUtility.BFDECRYPT_CLUTCH.name

    utils.write_file(DECRYPT_METHOD_CONFIG, decrypt_method)


def show_settings_menu(usr: str, pwd: str, ip: str):
    global CONFIG_DIR, AUTHENTICATE_ON_STARTUP, IP_FILE, UP_FILE, decrypt_method
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir()

    while True:
        utils.clear_terminal()
        print("  Settings")
        if not IP_FILE.exists():
            print("1. Save IP for future uses")
        else:
            print("1. Delete saved IP")

        if not UP_FILE.exists():
            print("2. Save user and password for future uses")
        else:
            print("2. Delete saved user and password")

        if not AUTHENTICATE_ON_STARTUP.exists():
            print("3. Enable auto authentication when app starts")
        else:
            print("3. Disable auto authentication when app starts")

        if decrypt_method:
            print(f"4. Select decrypt utility [Selected: {decrypt_method}]")
        else:
            print(f"4. Select decrypt utility")

        print("E. Go back")
        print("Select an option")
        option = utils.choose(["1", "2", "3", "4", "E"])

        if option == "1":
            if not IP_FILE.exists():
                save_ip_file(ip)
            else:
                IP_FILE.unlink()
        elif option == "2":
            if not UP_FILE.exists():
                save_up_file(usr, pwd)
            else:
                UP_FILE.unlink()
        elif option == "3":
            if not AUTHENTICATE_ON_STARTUP.exists():
                utils.write_file(AUTHENTICATE_ON_STARTUP, "")
            else:
                AUTHENTICATE_ON_STARTUP.unlink()
        elif option == "4":
            select_decrypt_utility()
        else:
            break
