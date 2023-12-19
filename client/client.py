import socket
import os
import re
from GUI.Registration_GUI import RegistrationApp

HOST = '127.0.0.1'
PORT = 40303

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def when_try_register():
    app = RegistrationApp()
    app.mainloop()
    u_email, u_username, u_password = app.get_user_values()
    print("All fields are good, waiting for server response...")
    client_socket.send(u_email.encode())
    client_socket.send(u_username.encode())
    client_socket.send(u_password.encode())
    print("Send")


try:
    when_try_register()
    reg_ans = client_socket.recv(1024).decode()
    if reg_ans == "<EXISTS>":
        print("Registration failed: Email already exists")
        when_try_register()
    elif reg_ans == "<SUCCESS>":
        print("Registration successful")
    else:
        print(f"Unexpected response from registration")

    while True:
        action = input("Do you want to send a file (S) or receive a file (R) or end (END)? ")

        if action.upper() == "END":
            client_socket.send("END".encode())
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
                    data = file.read(1024)
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

            # receiving the file size from the server
            file_size = int(client_socket.recv(1024).decode())

            if file_size == 0:
                print(f"File '{file_name}' not found on the server.")
            else:
                received_data = b""
                while len(received_data) < file_size:
                    chunk = client_socket.recv(1024)
                    received_data += chunk

                with open(os.path.join(save_path, file_name), 'wb') as file:
                    file.write(received_data)

                print(f"File '{file_name}' received successfully.")

except (socket.error, IOError) as e:
    print(f"Error: {e}")
finally:
    client_socket.close()
