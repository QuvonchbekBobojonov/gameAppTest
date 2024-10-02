import socket
import subprocess
import os
import glob


def get_start_menu_links():
    """Fetches all Start Menu shortcut (.lnk) files from both user and system Start Menu directories."""
    user_start_menu = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs')
    system_start_menu = os.path.expandvars(r'%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs')

    # Recursively search for all .lnk files in the Start Menu directories
    user_links = glob.glob(os.path.join(user_start_menu, '**', '*.lnk'), recursive=True)
    system_links = glob.glob(os.path.join(system_start_menu, '**', '*.lnk'), recursive=True)

    return user_links + system_links


def handle_client_commands(s, apps):
    """Handles client commands received from the server and processes them."""
    while True:
        try:
            # Receive data from the server
            data = s.recv(1024).decode()
            if not data:
                break  # If no data is received, exit the loop

            if data == 'exit':
                s.send("Exiting...".encode())
                print("Exiting...")
                break

            elif data == 'apps':
                # Send the list of available apps (start menu shortcuts)
                for i, app in enumerate(apps):
                    s.send(f"{i}: {app}\n".encode())

            elif data.startswith('open:'):
                try:
                    index = int(data.split(':')[1])
                    if 0 <= index < len(apps):
                        # Open the application at the specified index
                        subprocess.run(['explorer', apps[index]], shell=True)
                        s.send(f"Opened {apps[index]}\n".encode())
                    else:
                        s.send(f"Invalid app index: {index}\n".encode())
                except (ValueError, IndexError):
                    s.send("Invalid command format or index.\n".encode())
            elif data.startswith('close:'):
                try:
                    index = int(data.split(':')[1])
                    if 0 <= index < len(apps):
                        # Close the application at the specified index
                        subprocess.run(['taskkill', '/f', '/im', apps[index]], shell=True)
                        s.send(f"Closed {apps[index]}\n".encode())
                    else:
                        s.send(f"Invalid app index: {index}\n".encode())
                except (ValueError, IndexError):
                    s.send("Invalid command format or index.\n".encode())

            elif data == 'shutdown':
                s.send("Shutting down the machine...\n".encode())
                subprocess.run('shutdown /s /t 0', shell=True)

            elif data == 'restart':
                s.send("Restarting the machine...\n".encode())
                subprocess.run('shutdown /r /t 0', shell=True)

            else:
                s.send(f"Unknown command: {data}\n".encode())

        except Exception as e:
            print(f"Error handling client command: {e}")
            break


def main():
    """Main function to establish a connection to the server and handle client commands."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")

    host = '192.168.0.133'
    port = 6666

    # Get the list of Start Menu apps
    apps = get_start_menu_links()

    try:
        # Connect to the server
        s.connect((host, port))
        print(f"Connected to server {host} on port {port}")
    except socket.error as e:
        print(f"Connection error: {e}")
        return

    # Handle client commands
    handle_client_commands(s, apps)

    # Close the connection
    s.close()


if __name__ == '__main__':
    main()
