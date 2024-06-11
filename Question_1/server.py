import socket
import threading

# Pre-defined accounts (we use account username as key and a dict with balance and password as value)
accounts = {
    'client1': {'balance': 1000, 'password': 'password1'},
    'client2': {'balance': 2000, 'password': 'password2'},
    'client3': {'balance': 1500, 'password': 'password3'},
}

def check_balance(accounts, account_username):
    balance = accounts[account_username]['balance']
    return balance

def deposit(accounts,account_username, amount):
    balance = accounts[account_username]['balance']
    balance += amount
    return balance

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"Connection from {client_address} has been established!")
    client_socket.send(f" Welcome to the bank ATM!".encode("utf-8"))

    # Authentication process
    client_socket.send("Enter your account username: ".encode("utf-8"))
    account_username = client_socket.recv(1024).decode("utf-8")
    
    client_socket.send("Enter your password: ".encode("utf-8"))
    password = client_socket.recv(1024).decode("utf-8")
    
    # Check if account exists and password matches
    if account_username.strip().lower() in accounts and accounts[account_username]['password'] == password:
        client_socket.send("Authentication successful!".encode("utf-8"))
        authenticated = True
    else:
        client_socket.send("Authentication failed! Closing connection....".encode("utf-8"))
        client_socket.close()
        return # the function should terminate immediately without executing any further code
    
    while authenticated:
        client_socket.send("Choose operation: \n1. Check Balance \n2. Deposit \n3. Withdraw \n4. Exit".encode("utf-8"))
        operation = client_socket.recv(1024).decode("utf-8")
        
        # Check balance:
        if operation == '1':
            balance = check_balance(accounts, account_username)
            client_socket.send(f"Your balance is: ${balance}".encode("utf-8"))
        # Deposit:
        elif operation == '2':
            client_socket.send("Enter amount to deposit: ".encode("utf-8"))
            amount = float(client_socket.recv(1024).decode("utf-8"))
            balance = deposit(accounts,account_username, amount)
            accounts[account_username]['balance'] = balance
            client_socket.send(f"${amount} deposited. New balance is: ${balance}".encode( "utf-8"))
        # Withdraw:
        elif operation == '3':
            client_socket.send("Enter amount to withdraw: ".encode("utf-8"))
            amount = float(client_socket.recv(1024).decode("utf-8"))
            balance = accounts[account_username]['balance']
            if amount <= accounts[account_username]['balance']:
                accounts[account_username]['balance'] -= amount
                client_socket.send(bytes(f"${amount} withdrawn. New balance is: ${accounts[account_username]['balance']}", "utf-8"))
            else:
                client_socket.send(bytes("Insufficient funds!", "utf-8"))
        elif operation == '4':
            client_socket.send(f"Final balance: ${accounts[account_username]['balance']}. Goodbye!".encode("utf-8"))
            client_socket.close()
            break
        else:
            client_socket.send("Invalid operation. Please try again.".encode("utf-8"))
#Define start_server() function :responsible for setting up and running the TCP server.
def start_server():
    # Create a TCP socket object:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allows the socket address to be reused immediately after the socket is closed:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    # bind the server socket to a specific address and port.
    server_socket.bind(('0.0.0.0', 1234)) #(0.0.0.0 means  all available network interfaces 
    # Start listening for incoming connections:
    server_socket.listen() 
    print("Server is listening on port 1234...")
    connected = True

    # Accepting Client Connections
    while connected:
        client_socket, client_address = server_socket.accept()
        # Create a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    start_server()