import socket


def send_command_to_client(client_socket):
    while True:
        # Get the command from user to send to the client
        command = input("Enter a command to send to the client (shutdown/restart/exit): ").strip()

        # Validate command
        if command not in ['shutdown', 'restart', 'exit']:
            print("Invalid command. Please enter 'shutdown', 'restart', or 'exit'.")
            continue

        # Send the command to the client
        client_socket.send(command.encode())

        # Exit the loop if the command is 'exit'
        if command == 'exit':
            print("Exiting...")
            break

    client_socket.close()
    print("Client socket closed.")


def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")

    host = socket.gethostname()  # Get the local machine name
    port = 6666

    # Bind the socket to the address and port
    server_socket.bind((host, port))
    print(f"Socket bound to {host}:{port}")

    # Put the socket into listening mode
    server_socket.listen(5)
    print("Server is listening for connections...")

    try:
        while True:
            # Accept a connection from a client
            client_socket, addr = server_socket.accept()
            print(f"Got connection from {addr}")
            send_command_to_client(client_socket)
            print("Waiting for the next connection...")

    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server_socket.close()
        print("Socket closed.")


if __name__ == '__main__':
    main()
