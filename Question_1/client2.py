import socket
# Define connect_to_server() function :  responsible for establishing a connection to the server.
def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # If the client socket doesn't receive any data within 10 seconds, raise a socket timeout exception:
    client_socket.settimeout(10)
    msg_from_client = input("Enter a name to send to the server: ")
    try:
        client_socket.connect(('127.0.0.1', 1234))
        client_socket.send(msg_from_client.encode("utf-8"))
        msg_from_server = client_socket.recv(1024) # receive data from the server
        print(msg_from_server.decode("utf-8"))
    # Handling Connection Errors: 
    except socket.error as err:
        print('exp', err)
    #Ensures that the client socket is always closed
    finally:
        client_socket.close()


if __name__ == "__main__":
    connect_to_server()