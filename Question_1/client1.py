import socket
# Define connect_to_server() function :  responsible for establishing a connection to the server.
def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # If the client socket doesn't receive any data within 10 seconds, raise a socket timeout exception:
    #client_socket.settimeout(20)
    try:
        client_socket.connect(('127.0.0.1', 1234))
        welcome_message = client_socket.recv(1024)
        print(welcome_message.decode("utf-8"))

        # Authentication process:
        # Enter account number and password
        account_username = input(client_socket.recv(1024).decode("utf-8"))
        client_socket.send(account_username.encode("utf-8"))
        password = input(client_socket.recv(1024).decode("utf-8"))
        client_socket.send(password.encode("utf-8"))
        auth_response = client_socket.recv(1024).decode("utf-8")
        print(auth_response)
        if "Authentication successful" in auth_response:
            while True:
                options = client_socket.recv(1024).decode("utf-8")
                operation = input(f"{options}: ")
                client_socket.send(operation.encode("utf-8"))
                if operation == '1':
                    response = client_socket.recv(1024).decode("utf-8")
                    print(f"{response}\n")
                elif operation == '2':
                    amount = input(client_socket.recv(1024).decode("utf-8"))
                    client_socket.send(amount.encode("utf-8"))
                    response = client_socket.recv(1024).decode("utf-8")
                    print(f"{response}\n")
                elif operation == '3':
                    amount = input(client_socket.recv(1024).decode("utf-8"))
                    client_socket.send(amount.encode("utf-8") )
                    response = client_socket.recv(1024).decode("utf-8")
                    print(f"{response}\n")
                elif operation == '4':
                    response = client_socket.recv(1024).decode("utf-8")
                    print(response)
                    client_socket.close()
                    break
                else:
                    response = client_socket.recv(1024).decode("utf-8")
                    print(response)   
    # Handling Connection Errors: 
    except socket.error as err:
        print('exp', err)
    #Ensures that the client socket is always closed
    finally:
        client_socket.close()


if __name__ == "__main__":
    connect_to_server()