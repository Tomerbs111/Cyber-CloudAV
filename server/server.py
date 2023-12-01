import socket
import os
import threading
import tqdm
from database.Authentication import UserAuthentication

HOST = '127.0.0.1'
PORT = 40302


def handle_requests(client_socket, identifier):
    sub_folder_path = os.path.join('Received_files', identifier)
    os.makedirs(sub_folder_path, exist_ok=True)

    try:
        while True:
            action = client_socket.recv(1024).decode()

            if action == "END":
                print(f"The session with has ended.")
                break

            progress_bar = None  # Initialize progress_bar outside the block

            if action == "S":
                file_name = client_socket.recv(1024).decode()
                file_path = os.path.join(sub_folder_path, file_name)
                file_size = client_socket.recv(1024).decode()

                with open(file_path, "wb") as file:
                    done_sending = False
                    progress_bar = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(file_size))

                    while not done_sending:
                        data = client_socket.recv(1024)
                        if data[-len(b"<END_OF_DATA>"):] == b"<END_OF_DATA>":
                            done_sending = True
                            file.write(data[:-len(b"<END_OF_DATA>")])
                        else:
                            file.write(data)
                        progress_bar.update(len(data))

                    progress_bar.close()
                    print(f"File '{file_name}' received and saved in '{sub_folder_path}'")

            if action == "R":
                file_name = client_socket.recv(1024).decode()
                file_path = os.path.join(sub_folder_path, file_name)

                try:
                    with open(file_path, 'rb') as file:
                        file_data = file.read()
                        file_size = str(len(file_data))
                        client_socket.send(file_size.encode())

                        # Sending the file in chunks using send()
                        chunk_size = 1024
                        for i in range(0, len(file_data), chunk_size):
                            client_socket.send(file_data[i:i + chunk_size])
                            # Update progress bar for each chunk
                            if progress_bar:
                                progress_bar.update(chunk_size)

                        # Signal the end of data
                        client_socket.send(b"<END_OF_DATA>")
                        print(f"File '{file_name}' sent successfully")

                except FileNotFoundError:
                    print(f"File '{file_name}' not found.")
                    # Optionally, you can notify the client about the file not found.
                    client_socket.send("FILE_NOT_FOUND".encode())

    except (socket.error, IOError) as e:
        print(f"Error: {e}")

    finally:
        if progress_bar:
            progress_bar.close()
        client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        identifier = client_socket.recv(1024).decode()

        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_requests, args=(client_socket, identifier))
        client_handler.start()

except KeyboardInterrupt:
    print("Server terminated by user.")
finally:
    server_socket.close()
