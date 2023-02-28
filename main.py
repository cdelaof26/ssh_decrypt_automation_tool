import tools.ssh_connection as ssh_connection
import tools.app_data as settings
import tools.utils as utils


client, username, password, ip = None, None, None, None
listed_applications = None


def connect(setup_new_device):
    global client, username, password, ip, listed_applications
    client, username, password, ip = ssh_connection.setup_connection(setup_new_device)
    if client is not None:
        listed_applications = ssh_connection.list_apps(client)


if settings.AUTHENTICATE_ON_STARTUP.exists():
    connect(False)
    utils.clear_terminal()

interrupted = False

settings.read_decrypt_method_config()

while True:
    try:
        print("    Welcome to ssh decrypt automation tool")
        print("        By WholesomeThoughts26\n")
        print("  Main menu")
        options = ["1", "E"]

        try:
            # Check if client is alive
            if client is not None:
                client.exec_command("ls")
        except AttributeError:
            client, username, password, ip = None, None, None, None
            listed_applications = None

        if client is None:
            print("1. Connect to iOS device")
        else:
            options.append("2")
            options.append("3")

            print(f"1. Disconnect from '{ip}'")
            if listed_applications is None:
                print("2. List apps")
            else:
                print("2. Re-list apps")

            if not settings.decrypt_method:
                print("3. Select decrypt utility (needed to decrypt apps)")
            else:
                print("3. Dump app")
                print("4. Dump multiple apps")
                options.append("4")

            print("S. Settings")
            options.append("S")

        print("E. Exit")
        print("Select an option")

        option = utils.choose(options)

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
            if not settings.decrypt_method:
                settings.select_decrypt_utility()
            elif ssh_connection.is_idevice_ready(client):
                app = utils.select_apps(listed_applications, False)
                if app is not None:
                    ssh_connection.dump_app(client, app, False)

        if option == "4":
            if ssh_connection.is_idevice_ready(client):
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
