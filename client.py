import socket
import os
import qrcode

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# Upload file to the server
def upload_file(filepath):
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    
    s = socket.socket()
    print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")
    s.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connected.")
    
    # Send file info
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    
    # Send file data
    with open(filepath, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
    
    # Receive download link
    response = s.recv(BUFFER_SIZE).decode()
    print(response)
    
    # Generate QR code for the download link
    if "Download link" in response:
        link = response.split(": ")[1]
        generate_qr_code(link)
    
    s.close()

# Generate QR code for the download link
def generate_qr_code(link):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.show()
    img.save(f"qrcode_{os.path.basename(link)}.png")

if __name__ == "__main__":
    filepath = input("Enter the file path to upload: ")
    upload_file(filepath)
