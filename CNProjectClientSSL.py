import socket
import ssl
import matplotlib.pyplot as plt
import time
import json

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    ssl_client_socket = context.wrap_socket(client_socket, server_hostname='192.168.164.15')
    ssl_client_socket.connect(('192.168.164.15', 8888))
    print("Connected to server.")

    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlabel("Timestamp")
    ax.set_ylabel('Values')
    ax.set_title('Data Vs Time')
    lines = ['b-', 'g-', 'r-']  # Different colors for each variable
    labels = ['Humidity', 'Temperature', 'Distance']  # Capitalized labels
    plots = [ax.plot([], [], line, label=label)[0] for line, label in zip(lines, labels)]
    ax.legend(loc='upper right')
    
    data = {'humidity': [], 'temperature': [], 'distance': []}
    timestamps = []

    try:
        while True:
            data_recv = ssl_client_socket.recv(1024)
            data_recv = data_recv.decode()
            print(data_recv)
            try:
                json_data = json.loads(data_recv)
                for key, value in json_data.items():
                    if key in data:
                        data[key].append(float(value) if value is not None else 0.0)
            except json.JSONDecodeError:
                print("Error decoding JSON data")
                continue
                
            timestamp = time.time()
            timestamps.append(timestamp)
            
            for i, plot in enumerate(plots):
                if timestamps and data[labels[i].lower()] and (labels[i] != 'Distance' or data['distance'][-1] < 200):  # Check if arrays are not empty and plot distance only if less than 200 cm
                    plot.set_xdata(timestamps)
                    plot.set_ydata(data[labels[i].lower()])
                
            # Update plot limits only if there is data
            if timestamps and any(data.values()):
                ax.set_xlim(max(timestamps)-100,max(timestamps))
                ax.set_ylim(-10,210)
                
            fig.canvas.draw()
            fig.canvas.flush_events()
            
    except KeyboardInterrupt:
        plt.ioff()
        ssl_client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
