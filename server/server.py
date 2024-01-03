import pickle
import socket
import os
import threading
from database.Authentication import UserAuthentication
from database.UserFiles import UserFiles
from datetime import datetime

HOST = '127.0.0.1'
PORT = 40303


def handle_register_info(client_socket, u_email, u_username, u_password):
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


def handle_login_info(client_socket, u_email, u_password):
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


def handle_requests(client_socket, identifier):
    try:
        while True:
            user_files_manager = UserFiles(identifier)
            action = client_socket.recv(1024).decode()

            if action == "SIGN OUT":
                print(f"{auth.get_username(identifier)} has signed out.")
                break

            if action == "S":
                file_name = client_socket.recv(1024).decode()
                file_date = datetime.now()
                file_size = client_socket.recv(1024).decode()

                done_sending = False
                all_data = b""
                while not done_sending:
                    data = client_socket.recv(2048)
                    if data[-len(b"<END_OF_DATA>"):] == b"<END_OF_DATA>":
                        done_sending = True
                        all_data += data[:-len(b"<END_OF_DATA>")]
                        serialized_data = pickle.dumps(all_data)
                    else:
                        all_data += data

                user_files_manager.InsertFile(file_name, file_size, file_date, serialized_data)
                print(f"File '{file_name}' received and saved in the database")

            if action == "R":
                try:
                    file_name = client_socket.recv(1024).decode()
                    file_data = user_files_manager.get_file_data(file_name)[0]
                    file_size = user_files_manager.get_file_size(file_name)[0]

                    client_socket.send(file_size).encode()

                    client_socket.send(str(file_size).encode())
                    with open(file_data, 'rb') as file:
                        while True:
                            data = file.read(1024)
                            if not data:
                                break
                            client_socket.send(data)
                        client_socket.send(b"<END_OF_DATA>")

                    print(f"File '{file_name}' sent successfully")

                except FileNotFoundError:
                    print(f"File '{file_name}' not found.")
                    # Optionally, you can notify the client about the file not found.
                    client_socket.send("FILE_NOT_FOUND".encode())

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
            if u_status == "<REGISTER>":
                u_email = client_socket.recv(1024).decode()
                u_username = client_socket.recv(1024).decode()
                u_password = client_socket.recv(1024).decode()

                identifier = handle_register_info(client_socket, u_email, u_username, u_password)

            elif u_status == "<LOGIN>":
                u_email = client_socket.recv(100).decode()
                u_password = client_socket.recv(100).decode()

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
