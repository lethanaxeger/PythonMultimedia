import socket
import cv2
import pickle
import struct
import time

# Server configuration
host = '0.0.0.0'  # Listen on all network interfaces
port = 9999

# Create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

print("Server listening on port", port)

try:
    # Accept a client connection
    client_socket, addr = server_socket.accept()
    print('Connected to:', addr)

    # Start receiving and displaying video stream
    data = b""
    payload_size = struct.calcsize("Q")
    frame_count = 0
    start_time = time.time()

    while True:
        # Retrieve message size
        while len(data) < payload_size:
            data += client_socket.recv(4096)

        # Extract message size and data
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        # Retrieve frame data
        while len(data) < msg_size:
            data += client_socket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Deserialize frame data
        frame = pickle.loads(frame_data)

        # Check if frame is valid
        if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
            # Increment frame count
            frame_count += 1

            # Display frame
            cv2.putText(frame, f"FPS: {frame_count / (time.time() - start_time):.2f}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Stream', frame)
            cv2.waitKey(1)
        else:
            print("Invalid frame received")

finally:
    # Close connections
    client_socket.close()
    server_socket.close()
