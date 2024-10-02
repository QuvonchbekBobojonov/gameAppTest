import socket


def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")

    host = socket.gethostname()  # Get the local machine name
    port = 6666

    # Bind the socket to the address and port
    server_socket.bind((host, port))
    print(f"Socket binded to {host}:{port}")

    # Put the socket into listening mode
    server_socket.listen(5)
    print("Server is listening for connections...")

    # Accept a connection from a client
    client_socket, addr = server_socket.accept()
    print(f"Got connection from {addr}")

    while True:
        # Get the command from user to send to the client
        command = input("Enter a command to send to the client (shutdown/restart/exit): ").strip()

        # Send the command to the client
        client_socket.send(command.encode())

        # Exit the loop if the command is 'exit'
        if command == 'exit':
            print("Exiting...")
            break

    # Close the client connection
    client_socket.close()

    # Close the server socket
    server_socket.close()


if __name__ == '__main__':
    main()
