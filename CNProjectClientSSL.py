import socket
import ssl
import matplotlib.pyplot as plt
import time

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) #Transport Layer Security
    context.check_hostname = False #not checking as hostname is statically assigned
    context.verify_mode = ssl.CERT_NONE #NONE due to self signed certificate
    
    ssl_client_socket = context.wrap_socket(client_socket, server_hostname='192.168.157.15')
    ssl_client_socket.connect(('192.168.157.15', 8888))
    print("Connected to server.")

   
    

    plt.ion() #start interactive mode
    fig, ax = plt.subplots() #figure and subplots
    ax.set_xlabel("Timestamp")
    ax.set_ylabel('Distance')
    ax.set_title('DistVsTime')
    line,=ax.plot([],[],'b-',lw=2)
    distances = []
    timestamps = []
    try:
        while True:
            dist = ssl_client_socket.recv(1024)
            dist = dist.decode()
            dist = int(dist)
            if dist < 500: #more than 500cm was giving erroneous results
                distances.append(dist)
                timestamp = time.time()
                timestamp = int(timestamp)
                timestamps.append(timestamp)
            print(dist,timestamp)
            line.set_xdata(timestamps)
            line.set_ydata(distances)
            ax.set_xlim(max(timestamps)-100,max(timestamps))
            ax.set_ylim(min(distances)-10,max(distances)+10)

            fig.canvas.draw() 
            fig.canvas.flush_events() #threading GUI events
    except KeyboardInterrupt:
        plt.ioff()

if __name__ == "__main__":
    main()
    