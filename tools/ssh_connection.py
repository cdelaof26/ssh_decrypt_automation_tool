import tools.bundle_management as bm
import tools.app_data as app_data
import tools.ios_app as ios_apps
import paramiko
import socket
from tools.utils import choose, clear_terminal, write_binary_file, read_plist_file
from paramiko.channel import ChannelFile
from socket import gaierror
from time import sleep
from re import findall


# Utilities for connection


def connect(ip: str, username: str, password: str) -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(ip, username=username, password=password, timeout=30)

    return client


def disconnect(client: paramiko.SSHClient):
    print("Closing connection... ", end="", flush=True)
    if client:
        sleep(5)
        client.close()
        print("Done")
    else:
        print("No connection was opened")


def is_client_darwin(client: paramiko.SSHClient) -> bool:
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command("uname")
    return findall("Darwin", read_output(ssh_stdout)) != []


def disconnect_sftp(sftp_client: paramiko.SFTPClient):
    if sftp_client:
        sleep(5)
        sftp_client.close()


def setup_connection(ask_to_setup_new_idevice=True) -> list:
    clear_terminal()
    print("    Connection setup")
    tmp_ip = app_data.read_ip_file()
    if not tmp_ip:
        ip = None
    else:
        ip = tmp_ip

    tmp_up = app_data.read_up_file()
    if not tmp_up or len(tmp_up) != 2:
        username = None
        password = None
    else:
        username = tmp_up[0]
        password = tmp_up[1]

    client = None

    if tmp_ip and tmp_up and ask_to_setup_new_idevice:
        print("\nDo you want to setup a new device?")
        print("1. Yes")
        print(f"2. No, connect to {ip}")
        if choose(["1", "2"], [True, False]):
            ip, username, password = None, None, None
            ios_apps.clear_cache()

    attempts = 0

    while client is None and attempts < 3:
        if ip is None:
            print("\nEnter the iOS device IP:")
            ip = input("> ")

        if username is None or password is None:
            print("\nEnter your credentials")
            print("    Do you want to login with root/alpine?")
            print("1. Yes")
            print("2. No, let me enter my username and password")

            if choose(["1", "2"], [True, False]):
                username, password = "root", "alpine"
            else:
                print("\nEnter your username")
                username = input("> ")
                print("\nEnter your password")
                password = input("> ")

        try:
            print("\nTrying connection... ", end="", flush=True)
            client = connect(ip, username, password)
        except socket.timeout:
            print("Time out!")
            client = None
            attempts += 1
            continue
        except (paramiko.ssh_exception.NoValidConnectionsError, gaierror):
            print(f"Failed to find host '{ip}'")
            client = None
            ip = None
            attempts += 1
            continue
        except paramiko.ssh_exception.AuthenticationException:
            print("Failed to authenticate!")
            client = None
            username = None
            password = None
            attempts += 1
            continue

    if not client:
        print("\n    Please check your internet connection, username and password")
        print("    If you need more assistance, check README.md file\n")
        raise InterruptedError("Too many attempts")

    print("Connection success!")

    if password == "alpine":
        print("\n    Please, consider changing ssh default password!")

    if not is_client_darwin(client):
        print("\n    Looks like you're not connected to an iOS device...")
        disconnect(client)
        return [None, None, None, None]

    return [client, username, password, ip]


def read_output(ssh_stdout: ChannelFile) -> str:
    data = ssh_stdout.read()
    if data:
        return data.decode("utf-8")

    return ""


def put_clutch_troll(client: paramiko.SSHClient) -> bool:
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(f"cd {ios_apps.MOBILE_DOCUMENTS}; ls")
    output = read_output(ssh_stdout)
    if not findall("Clutch_troll", output):
        try:
            sftp_client = client.open_sftp()
            sftp_client.put(app_data.CLUTCH_EXECUTABLE, ios_apps.MOBILE_DOCUMENTS + "/Clutch_troll")
            disconnect_sftp(sftp_client)
            client.exec_command(f"cd {ios_apps.MOBILE_DOCUMENTS}; chmod +x Clutch_troll")
            return True
        except FileNotFoundError:
            print("It's not possible copy Clutch_troll!")
            disconnect(client)
            return False

    client.exec_command(f"cd {ios_apps.MOBILE_DOCUMENTS}; chmod +x Clutch_troll")

    return True


def list_bundle_ids(client: paramiko.SSHClient) -> list:
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(f"cd {ios_apps.APPLICATION_BUNDLES}; ls")

    output = read_output(ssh_stdout)

    return bm.find_metadata_plist(output)


def retrieve_apps_plists(client: paramiko.SSHClient, listed_applications: list):
    if not ios_apps.LOCAL_CACHE_DIR.exists():
        ios_apps.LOCAL_CACHE_DIR.mkdir()

    sftp_client = client.open_sftp()

    for app in listed_applications:
        app.local_plist_path = ios_apps.LOCAL_CACHE_DIR.joinpath(app.bundle_id + ".plist")
        if app.local_plist_path.exists():
            continue

        try:
            remote_file = sftp_client.open(app.host_plist_path, "rb")
            write_binary_file(app.local_plist_path, remote_file.read())
        except FileNotFoundError:
            pass

    disconnect_sftp(sftp_client)


def retrieve_apps_names(client: paramiko.SSHClient, listed_applications: list):
    files_in_cache = ios_apps.is_there_any_cache()
    download_plist = files_in_cache == 0 or files_in_cache != len(listed_applications)

    if download_plist:
        retrieve_apps_plists(client, listed_applications)
    else:
        for app in listed_applications:
            app.local_plist_path = ios_apps.LOCAL_CACHE_DIR.joinpath(app.bundle_id + ".plist")

    for app in listed_applications:
        plist_data = read_plist_file(app.local_plist_path)
        if not plist_data:
            continue

        try:
            app.app_name = plist_data["itemName"]
            app.app_bundle = plist_data["softwareVersionBundleId"]
            app.app_version = plist_data["bundleShortVersionString"]
        except KeyError:
            continue


def list_apps(client: paramiko.SSHClient) -> list:
    print("\nListing apps... ", end="", flush=True)
    listed_applications = list_bundle_ids(client)
    retrieve_apps_names(client, listed_applications)
    print("Done")

    return listed_applications


def decrypt_app(client: paramiko.SSHClient, app: ios_apps.AppInfo) -> str:
    cmd = f"cd {ios_apps.MOBILE_DOCUMENTS} && ./Clutch_troll -d {app.app_bundle}"
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(cmd)

    output = read_output(ssh_stdout) + "\n" + read_output(ssh_stderr)  # Somehow output is getting into stderr

    if not findall("FAILED", output):  # FAILED was not found, meaning that app was decrypted
        decrypted = findall(f"DONE: /private/var/mobile/Documents/Dumped/{app.app_bundle}.*", output)
        if decrypted:
            return str(decrypted[0]).replace("DONE: ", "")

    output = f"Command:    {cmd}\n" \
             f"App:        {app.app_name}\n" \
             f"AppVersion: {app.app_version}\n" \
             f"AppBundle:  {app.app_bundle}\n" \
             f"AppPath:    {app.bundle_id}\n" \
             f"Clutch output:\n" + output
    app_data.write_log(output)
    return ""


def download_app(client: paramiko.SSHClient, app: ios_apps.AppInfo, ipa_path: str) -> str:
    if not app_data.DOWNLOADED_APPS.exists():
        app_data.DOWNLOADED_APPS.mkdir()

    local_file_name = app_data.DOWNLOADED_APPS.joinpath(app.app_name.replace(" ", "_") + "_" + app.app_version + ".ipa")

    sftp_client = client.open_sftp()
    try:
        sftp_client.get(ipa_path, local_file_name)
        client.exec_command(f"rm \"{ipa_path}\"")

        return local_file_name.name
    except FileNotFoundError:
        return ""
    finally:
        disconnect_sftp(sftp_client)


def dump_app(client: paramiko.SSHClient, app: ios_apps.AppInfo):
    print(f"Dumping {app.app_bundle}... ", end="", flush=True)
    ipa_path = decrypt_app(client, app)
    if ipa_path:
        print("Success")
        print("Downloading... ", end="", flush=True)
        downloaded = download_app(client, app, ipa_path)
        if downloaded:
            print("File saved as", downloaded)
        else:
            print("Failed to download ipa!")
    else:
        print("Error while decrypting ipa!")


def dump_multiple_apps(client: paramiko.SSHClient, apps: list):
    for app in apps:
        dump_app(client, app)
