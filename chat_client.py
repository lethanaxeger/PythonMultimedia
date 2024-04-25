import socket
import threading

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            # If an error occurs, close the client socket
            print("Error receiving message.")
            client_socket.close()
            break

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
#client_socket.connect(('127.0.0.1', 5555)) //Public IP & Port
client_socket.connect(('192.168.1.7', 5555))

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Send messages to the server
while True:
    message = input()
    client_socket.send(message.encode())
