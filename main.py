import tools.ssh_connection as ssh_connection
import tools.app_data as settings
import tools.utils as utils

if not settings.does_clutch_exist():
    print("    Please provide a copy of Clutch_troll!")
    print("        If you need assistance, please check README.md")
    exit(1)


client, username, password, ip = None, None, None, None
listed_applications = None


def connect(setup_new_device):
    global client, username, password, ip, listed_applications
    client, username, password, ip = ssh_connection.setup_connection(setup_new_device)
    if client is not None:
        if ssh_connection.put_clutch_troll(client):
            listed_applications = ssh_connection.list_apps(client)
        else:
            client, username, password, ip = None, None, None, None


if settings.AUTHENTICATE_ON_STARTUP.exists():
    connect(False)
    utils.clear_terminal()

interrupted = False

while True:
    try:
        print("    Welcome to ssh decrypt automation tool")
        print("        By WholesomeThoughts26\n")
        print("  Main menu")
        if client is None:
            print("1. Connect to iOS device")
        else:
            print(f"1. Disconnect from '{ip}'")
            if listed_applications is None:
                print("2. List apps")
            else:
                print("2. Re-list apps")
            print("3. Dump app")
            print("4. Dump multiple apps")
            print("S. Settings")

        print("E. Exit")
        print("Select an option")

        if client is None:
            option = utils.choose(["1", "E"])
        else:
            option = utils.choose(["1", "2", "3", "4", "S", "E"])

        if option == "1":
            if client is None:
                connect(True)
            else:
                ssh_connection.disconnect(client)
                client, username, password, ip = None, None, None, None

        if option == "2":
            utils.clear_terminal()
            listed_applications = ssh_connection.list_apps(client)

        if option == "3":
            app = utils.select_apps(listed_applications, False)
            if app is not None:
                ssh_connection.dump_app(client, app)

        if option == "4":
            ssh_connection.dump_multiple_apps(client, utils.select_apps(listed_applications, True))

        if option == "S":
            settings.show_settings_menu(username, password, ip)

        if option == "E":
            break

        input("\nPress enter to continue... ")
        utils.clear_terminal()
    except KeyboardInterrupt:
        interrupted = client is not None
        break

if client is not None:
    if interrupted:
        print("  Please don't interrupt disconnection process!")
    ssh_connection.disconnect(client)
