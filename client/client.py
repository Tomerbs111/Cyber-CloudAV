import socket
import os
from GUI.CloudGUI import *

HOST = '127.0.0.1'
PORT = 40303

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

try:
    while True:
        app = MyApp(client_socket)
        app.mainloop()
        client_socket.sendall("X".encode())
        client_socket.close()
        break
except (socket.error, IOError) as e:
    print(f"Error: {e}")
finally:
    client_socket.close()

