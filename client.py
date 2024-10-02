import socket
import subprocess
import os


def main():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")

    host = '192.168.0.133'
    port = 6666

    # Connect to the server on the local machine
    try:
        s.connect((host, port))  # You can replace this with ('127.0.0.1', port) for localhost
        print(f"Connected to {socket.gethostname()} on port {port}")
    except socket.error as e:
        print(f"Connection error: {e}")
        return

    while True:
        data = s.recv(1024).decode()

        # If the server sends 'exit', break the loop and close the connection
        if data == 'exit':
            s.send("exit".encode())
            print("Exiting...")
            break

        # Command to shutdown the machine
        if data == 'shutdown':
            print("Shutting down the machine...")
            s.send("Shutting down...".encode())
            subprocess.Popen(['shutdown', '/s', '/t', '0'])

        # Command to restart the machine
        elif data == 'restart':
            print("Restarting the machine...")
            s.send("Restarting...".encode())
            subprocess.Popen(['shutdown', '/r', '/t', '0'])

        # Command to open the file explorer
        elif data == 'explorer':
            print("Opening file explorer...")
            s.send("Opening file explorer...".encode())
            subprocess.Popen('explorer')

        # Command to open Notepad
        elif data == 'notepad':
            print("Opening Notepad...")
            s.send("Opening Notepad...".encode())
            subprocess.Popen('notepad')

        # Command to open Chrome
        elif data == 'chrome':
            print("Opening Chrome...")
            s.send("Opening Chrome...".encode())
            subprocess.run(os.path.join(os.environ['PROGRAMFILES'], 'Google/Chrome/Application/chrome.exe'))
            s.send("Chrome opened".encode())

        # Print the data received from the server
        print(f"Server says: {data}")

    # Close the connection
    s.close()


if __name__ == '__main__':
    main()
