import socket
import os
import threading

# Server configuration
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
BASE_DIR = "shared_files"

# Initialize the server
def initialize_server():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    
    server_socket = socket.socket()
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
    
    while True:
        client_socket, address = server_socket.accept()
        print(f"[+] {address} is connected.")
        
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

# Handle client connections
def handle_client(client_socket):
    try:
        # Receive file info
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        
        filepath = os.path.join(BASE_DIR, filename)
        
        # Receive file data
        with open(filepath, "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
        
        print(f"File {filename} received successfully.")
        
        # Send the download link to the client
        link = f"http://{SERVER_HOST}:{SERVER_PORT}/download/{filename}"
        client_socket.send(f"File received. Download link: {link}".encode())
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    initialize_server()
