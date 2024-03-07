import socket
import ssl
import threading
import serial
import time
import json

ser = serial.Serial('COM6', 9600, timeout=1)
received_json = ""  # Variable to store received JSON

def handle_client(client_socket):
    try:
        while True:
            global received_json
            if received_json:  # Check if JSON data is available
                client_socket.send(received_json.encode())  # Send JSON data to client
                received_json = ""  # Clear the variable after sending
    except KeyboardInterrupt:
        client_socket.close()
        print("Closing Client connection")
    finally:
        client_socket.close()

def serial_reader():
    global received_json
    try:
        while True:
            ser.write(b'r')
            response = ser.readline().decode('utf-8').strip()

            if response:
                received_json = response  # Store received JSON
            time.sleep(0.1)
    except KeyboardInterrupt:
        exit(0)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('172.20.10.11', 8888))
    server_socket.listen(5)
    print("Server listening on port 8888...")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    serial_thread = threading.Thread(target=serial_reader)
    serial_thread.daemon = True
    serial_thread.start()

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print("Connected to", addr)
            ssl_client_socket = context.wrap_socket(client_socket, server_side=True)
            threading.Thread(target=handle_client, args=(ssl_client_socket,)).start()
    except KeyboardInterrupt:
        exit(0)

if __name__ == "__main__":
    main()
