import socket
import os
from ClientCommunication import ClientCommunication
from GUI.MyApp import MyApp

HOST = '127.0.0.1'
PORT = 40301

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

client_communicator = ClientCommunication(client_socket)

try:
    while True:
        app = MyApp(client_communicator)
        app.mainloop()
        client_socket.sendall("X".encode())
        client_socket.close()
        break
except (socket.error, IOError) as e:
    print(f"Error: {e}")
finally:
    client_socket.close()

