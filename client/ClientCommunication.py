import os
import pickle
import socket


class ClientCommunication:

    def __init__(self, client_socket: socket):
        self.client_socket = client_socket


    def r_when_submit(self, attempt_type, u_email, u_username, u_password):
        self.client_socket.sendall(attempt_type.encode())
        print("status sent")

        if attempt_type == "<REGISTER>":
            print("User info -----------------------")
            print(f"Email: {u_email}")
            print(f"Username: {u_username}")
            print(f"Password: {u_password}")
            print("---------------------------------")

            field_dict = {
                'email': u_email,
                'username': u_username,
                'password': u_password,
            }

            self.client_socket.sendall(pickle.dumps(field_dict))

            server_ans = self.client_socket.recv(1024).decode()
            return server_ans


    def l_when_submit(self, attempt_type, u_email, u_password):
        self.client_socket.sendall(attempt_type.encode())

        if attempt_type == "<LOGIN>":
            print("User info -----------------------")
            print(f"Email: {u_email}")
            print(f"Password: {u_password}")
            print("---------------------------------")

            field_dict = {
                'email': u_email,
                'password': u_password
            }

            self.client_socket.sendall(pickle.dumps(field_dict))

            server_ans = self.client_socket.recv(1024).decode()
            print(f"answer: {server_ans}")
            return server_ans


    def send_file(self, file_name, short_filename, formatted_file_size, short_file_date, file_bytes):
        """
        Sends a file to the client.

        Args:
        file_name (str): The full name of the file.
        short_filename (str): The short name of the file.
        formatted_file_size (str): The formatted size of the file.
        short_file_date (str): The short date of the file.
        file_bytes (bytes): The content of the file in bytes.
        """
        # Send the "S" flag to indicate file transmission
        self.client_socket.send("S".encode())
        # Send the file metadata and content
        self.client_socket.send(pickle.dumps([short_filename, file_bytes, short_file_date]))

        # Receive acknowledgment from the client
        serv_ans = self.client_socket.recv(72).decode()

        # Check if the client is ready to receive the file
        if serv_ans == "<GOT_PROP>":
            with open(file_name, 'rb') as file:
                while True:
                    # Read and send the file in chunks
                    data = file.read(1024)
                    if not data:
                        break
                    self.client_socket.send(data)

                # Signal the end of data transmission
                self.client_socket.send(b"<END_OF_DATA>")
                print(f"File '{file_name}' sent successfully")

    def receive_checked_files(self, select_file_names_lst, save_path):
        self.client_socket.send(b'<R>')

        # Convert the list to a pickled string
        pickled_data = pickle.dumps(select_file_names_lst)

        # Send the length of the pickled data
        data_len = str(len(pickled_data))
        self.client_socket.send(data_len.encode())

        # Send the pickled data
        self.client_socket.send(pickled_data)

        # Now the client receives the dictionary from the server
        data_len = int(self.client_socket.recv(1024).decode())
        pickled_fdn_dict = self.client_socket.recv(data_len)

        # Load the dictionary
        file_data_name_dict = pickle.loads(pickled_fdn_dict)

        for indiv_filename, indiv_filebytes in file_data_name_dict.items():
            file_path = os.path.join(save_path, indiv_filename)
            with open(file_path, "wb") as file:
                file.write(indiv_filebytes)
                print(f"File '{indiv_filename}' received successfully.")

    def notify_and_receive_files(self):
        self.client_socket.send(b'<NARF>')

        # Receive the length of the pickled data
        data_len = int(self.client_socket.recv(1024).decode())

        # Receive the pickled data
        pickled_data = self.client_socket.recv(data_len)

        # Load the pickled data
        saved_file_prop_lst = pickle.loads(pickled_data)
        return saved_file_prop_lst
