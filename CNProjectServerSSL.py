import socket
import ssl
import threading
import serial
import time

ser = serial.Serial('COM6', 9600, timeout=1)
dist = 0
d = 0

def handle_client(client_socket):
    try:
        while True:
            # Send the value of dist to the client
            global dist
            client_socket.send(str(dist).encode())
            time.sleep(0.5)
    finally:
        client_socket.close()

def serial_reader():
    global dist
    while True:
        ser.write(b'r')
        response = ser.readline().decode().strip()
        if response:
            print(response)
            dist = int(response)
        time.sleep(1)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8888))
    server_socket.listen(5)
    print("Server listening on port 8888...")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    # Start a thread to read data from the serial port
    serial_thread = threading.Thread(target=serial_reader)
    serial_thread.daemon = True  # Daemonize the thread so it exits when the main program ends
    serial_thread.start()

    while True:
        client_socket, addr = server_socket.accept()
        print("Connected to", addr)
        ssl_client_socket = context.wrap_socket(client_socket, server_side=True)
        # Start a new thread for each client
        threading.Thread(target=handle_client, args=(ssl_client_socket,)).start()

if __name__ == "__main__":
    main()

