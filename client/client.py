import socket
import os
from GUI.Registration_GUI import RegistrationApp
from GUI.Mainpage_GUI import MainPage

HOST = '10.10.11.135'
PORT = 40303

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

try:
    win = RegistrationApp(client_socket)
    win.mainloop()

    if win.auth_completed:
        while True:
            main_app = MainPage(client_socket)
            main_app.mainloop()
            client_socket.send("X".encode())
            client_socket.close()
            break
except (socket.error, IOError) as e:
    print(f"Error: {e}")
finally:
    client_socket.close()

