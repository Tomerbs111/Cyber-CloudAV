import pickle
import socket
import os
import re
from GUI.Registration_GUI import RegistrationApp

HOST = '127.0.0.1'
PORT = 40303

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

try:
    win = RegistrationApp(client_socket)
    win.mainloop()

    if win.auth_completed:
        while True:
            action = input("Do you want to send a file (S) or receive a file (R) or Sign out (SIGN OUT)? ")

            if action.upper() == "SIGN OUT":
                client_socket.send("SIGN OUT".encode())
                client_socket.close()
                break

            if action.upper() == "S":
                client_socket.send(action.encode())
                file_path = input("Enter the path of the file to send (type RETURN to return to options): ")

                if file_path.upper() == 'RETURN':
                    continue

                if not os.path.exists(file_path):
                    print("File not found. Please enter a valid file path.")
                    continue

                # sending the file name
                file_name = os.path.basename(file_path)
                client_socket.send(file_name.encode())

                # sending the file size
                file_size = os.path.getsize(file_path)
                client_socket.send(str(file_size).encode())

                with open(file_path, 'rb') as file:
                    while True:
                        data = file.read()
                        if not data:
                            break
                        client_socket.send(data)

                    # Signal the end of data
                    client_socket.send(b"<END_OF_DATA>")

                print(f"File '{file_name}' sent successfully")

            if action.upper() == "R":
                client_socket.send(action.encode())
                file_name = input("Enter the name of the file to receive: ")
                save_path = input("Enter the path of the save folder: ")

                # sending the requested file name to the server
                client_socket.send(file_name.encode())

                done_sending = False
                with open(save_path + '/' + file_name, 'wb') as file:
                    while not done_sending:
                        recived_file_data = client_socket.recv(1024)
                        if not recived_file_data:
                            done_sending = True
                        else:
                            file.write(recived_file_data)


except (socket.error, IOError) as e:
    print(f"Error: {e}")
finally:
    client_socket.close()
