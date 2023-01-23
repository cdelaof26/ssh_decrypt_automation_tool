from tools.utils import choose, clear_terminal, read_file, write_file
from pathlib import Path


CONFIG_DIR = Path.cwd().joinpath("config")


# If this file exist, this program will try to authenticate as soon as it starts
AUTHENTICATE_ON_STARTUP = CONFIG_DIR.joinpath("auth")

# This directory contains logs for failed dumps
FAILED_LOGS = Path.cwd().joinpath("error_logs")


# This file just holds the last IP entered,
# If file is found, contents are readed to skip having to
# enter the IP again
IP_FILE = CONFIG_DIR.joinpath("ip.txt")

# This file holds username and password if user decides to save them as plain text
# (thing which I don't recommend)
UP_FILE = CONFIG_DIR.joinpath("up.txt")


CLUTCH_EXECUTABLE = Path().cwd().joinpath("Clutch_troll")
DOWNLOADED_APPS = Path.cwd().joinpath("IPAs")


def read_ip_file() -> str:
    global IP_FILE
    if not IP_FILE.exists():
        return ""

    return read_file(IP_FILE)


def save_ip_file(ip: str):
    global IP_FILE
    write_file(IP_FILE, ip)


def read_up_file() -> list:
    global UP_FILE
    if not UP_FILE.exists():
        return []

    return read_file(UP_FILE).split("\n")


def save_up_file(usr: str, pwd: str):
    global UP_FILE
    write_file(UP_FILE, usr + "\n" + pwd)


def does_clutch_exist() -> bool:
    global CLUTCH_EXECUTABLE
    if not CLUTCH_EXECUTABLE.exists():
        print(f"\"{CLUTCH_EXECUTABLE.resolve()}\" doesn't exist")
        return False

    return True


def write_log(log: str):
    global FAILED_LOGS
    if not FAILED_LOGS.exists():
        FAILED_LOGS.mkdir()

    log_file = FAILED_LOGS.joinpath("dump_log.txt")
    i = 0
    while log_file.exists():
        log_file = FAILED_LOGS.joinpath(f"dump_log ({i}).txt")
        i += 1

    write_file(log_file, log)


def show_settings_menu(usr: str, pwd: str, ip: str):
    global CONFIG_DIR, AUTHENTICATE_ON_STARTUP, IP_FILE, UP_FILE
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir()

    while True:
        clear_terminal()
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

        print("E. Go back")
        print("Select an option")
        option = choose(["1", "2", "3", "E"])

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
                write_file(AUTHENTICATE_ON_STARTUP, "")
            else:
                AUTHENTICATE_ON_STARTUP.unlink()
        else:
            break
