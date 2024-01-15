import pickle
import socket
import os
import threading
from typing import Any

from database.Authentication import UserAuthentication
from database.UserFiles import UserFiles
from datetime import datetime

HOST = '0.0.0.0'
PORT = 40303


def handle_register_info(client_socket: socket, u_email: str, u_username: str, u_password: str) -> int | str:
    try:
        ans = auth.register(u_email, u_username, u_password)
        client_socket.send(ans.encode())
        if ans == "<EXISTS>":
            print("Registration failed: Email already exists")
            return "<EXISTS>"

        elif ans == "<SUCCESS>":
            print("Registration successful")
            userid = auth.get_userid(u_email)
            return userid[0]
        else:
            print(f"Unexpected response from registration: {ans}")

    except Exception as e:
        print(f"Unexpected error during registration: {e}")
        client_socket.send("Unexpected error during registration".encode())


def handle_login_info(client_socket: socket, u_email: str, u_password: str) -> str | None:
    auth = UserAuthentication()
    try:
        auth_ans = auth.login(u_email, u_password)
        client_socket.send(auth_ans.encode())
        if auth_ans == "<NO_EMAIL_EXISTS>":
            print("Login failed. No accounts under the provided email.")
            return
        elif auth_ans == "<WRONG_PASSWORD>":
            print("Login failed. Password doesn't match to the provided email.")
            return
        else:
            print("User logged in Successfully")
            userid = auth.get_userid(u_email)
            return userid[0]

    except Exception as e:
        print(f"Unexpected error during login: {e}")
        client_socket.send("Unexpected error during Login".encode())
        return "<FAILED>"


def handle_requests(client_socket: socket, identifier: int) -> None:
    try:
        while True:
            user_files_manager = UserFiles(f'u_{identifier}')
            action = client_socket.recv(8).decode()

            if action == "X":
                print(f"User {identifier} has signed out.")
                break

            if action == "S":
                # server is getting the file properties to write in db
                file_prop_lst = pickle.loads(client_socket.recv(1024))

                file_name = file_prop_lst[0]
                file_size = file_prop_lst[1]
                file_date = file_prop_lst[2]
                client_socket.send(b"<GOT_PROP>")

                # server god all the properties
                done_sending = False
                all_data = b""
                while not done_sending:
                    data = client_socket.recv(1024)
                    if data[-len(b"<END_OF_DATA>"):] == b"<END_OF_DATA>":
                        done_sending = True
                        all_data += data[:-len(b"<END_OF_DATA>")]
                    else:
                        all_data += data

                user_files_manager.InsertFile(file_name, file_size, file_date, all_data)
                print(f"File '{file_name}' received and saved in the database")

            if action == "R":
                try:
                    file_name = client_socket.recv(1024).decode()
                    file_data = user_files_manager.get_file_data(file_name)

                    if file_data is None:
                        raise FileNotFoundError(f"File '{file_name}' not found or empty")

                    current_place = 0
                    while current_place < len(file_data):
                        data = file_data[current_place:current_place + 1024]
                        client_socket.send(data)
                        current_place += 1024

                    # Ensure that the string "<END_OF_DATA>" is sent as bytes
                    client_socket.send(b"<END_OF_DATA>")
                    print(f"File '{file_name}' sent successfully")

                except FileNotFoundError:
                    print(f"File '{file_name}' not found.")
                    client_socket.send("FILE_NOT_FOUND".encode())

                except Exception as e:
                    print(f"Error while sending file '{file_name}': {e}")
                    client_socket.send("ERROR_SENDING_FILE".encode())

    except (socket.error, IOError) as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

auth = UserAuthentication()

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        identifier = None  # Initialize identifier outside the loop

        while True:
            u_status = client_socket.recv(1024).decode()
            client_socket.send(b'<ACK>')
            if u_status == "<REGISTER>":
                field_dict = pickle.loads(client_socket.recv(1024))
                u_email = field_dict['email']
                u_username = field_dict['username']
                u_password = field_dict['password']

                identifier = handle_register_info(client_socket, u_email, u_username, u_password)

            elif u_status == "<LOGIN>":
                field_dict = pickle.loads(client_socket.recv(1024))
                u_email = field_dict['email']
                u_password = field_dict['password']

                identifier = handle_login_info(client_socket, u_email, u_password)

            if identifier and identifier != "<EXISTS>":
                # Start a new thread to handle the client
                client_handler = threading.Thread(target=handle_requests, args=(client_socket, identifier))
                client_handler.start()
                break  # Break out of the inner loop if registration is successful

except KeyboardInterrupt:
    print("Server terminated by user.")
finally:
    server_socket.close()
