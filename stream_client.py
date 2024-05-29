import socket
import cv2
import pickle
import struct

# Client configuration
host = '192.168.21.174'  # Server IP address
port = 9999

# Create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame from webcam
    ret, frame = cap.read()

    # Serialize frame data
    data = pickle.dumps(frame)
    msg_size = struct.pack("Q", len(data))

    # Send frame data to server
    client_socket.sendall(msg_size + data)

# Close connections
cap.release()
client_socket.close()
