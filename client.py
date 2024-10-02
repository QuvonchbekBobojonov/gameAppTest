import socket
import subprocess
from windows_tools.installed_software import get_installed_software

# Constants for commands
COMMAND_EXIT = 'exit'
COMMAND_APPS = 'apps'
COMMAND_OPEN = 'open:'
COMMAND_CLOSE = 'close:'
COMMAND_SHUTDOWN = 'shutdown'
COMMAND_RESTART = 'restart'


def get_installed_apps():
    apps = get_installed_software()
    for app in apps:
        print(app)
    return [app['DisplayName'] for app in apps]


def handle_client_commands(s, apps):
    while True:
        try:
            data = s.recv(1024).decode()
            if not data:
                break

            if data == COMMAND_EXIT:
                s.send("Exiting...".encode())
                print("Exiting...")
                break

            elif data == COMMAND_APPS:
                apps_list = '\n'.join(f"{i}: {app}" for i, app in enumerate(apps))
                s.send(apps_list.encode())

            elif data.startswith(COMMAND_OPEN):
                handle_application(s, data, apps, 'open')

            elif data.startswith(COMMAND_CLOSE):
                handle_application(s, data, apps, 'close')

            elif data == COMMAND_SHUTDOWN:
                s.send("Shutting down the machine...\n".encode())
                subprocess.run('shutdown /s /t 0', shell=True)

            elif data == COMMAND_RESTART:
                s.send("Restarting the machine...\n".encode())
                subprocess.run('shutdown /r /t 0', shell=True)

            else:
                s.send(f"Unknown command: {data}\n".encode())

        except Exception as e:
            print(f"Error handling client command: {e}")
            break


def handle_application(s, data, apps, action):
    try:
        index = int(data.split(':')[1])
        if 0 <= index < len(apps):
            app_name = apps[index]
            if action == 'open':
                subprocess.run(['explorer', app_name], shell=True)
                s.send(f"Opened {app_name}\n".encode())
            elif action == 'close':
                subprocess.run(['taskkill', '/f', '/im', f"{app_name}.exe"], shell=True)
                s.send(f"Closed {app_name}\n".encode())
        else:
            s.send(f"Invalid app index: {index}\n".encode())
    except (ValueError, IndexError):
        s.send("Invalid command format or index.\n".encode())


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")

    host = '192.168.0.133'
    port = 6666

    apps = get_installed_apps()

    try:
        s.connect((host, port))
        print(f"Connected to server {host} on port {port}")
    except socket.error as e:
        print(f"Connection error: {e}")
        return

    handle_client_commands(s, apps)

    s.close()


if __name__ == '__main__':
    main()
