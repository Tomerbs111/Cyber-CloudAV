import os
import pickle
import socket


class ClientCommunication:

    def __init__(self, client_socket: socket):
        self.client_socket = client_socket

    def r_when_submit(self, attempt_type, u_email, u_username, u_password):
        """
        Send attempt_type to server, then send user info if attempt_type is <REGISTER>, and return server_ans.

        :param attempt_type: str, the type of attempt being made
        :param u_email: str, the user's email
        :param u_username: str, the user's username
        :param u_password: str, the user's password
        :return: str, the server's answer
        """
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
            print(f"answer: {server_ans}")
            return server_ans

    def l_when_submit(self, attempt_type, u_email, u_password):
        """
        Sends the attempt type, user email, and user password to the server, and receives
        and returns the server's response.

        Parameters:
            attempt_type (str): The type of login attempt ("<LOGIN>" in this case).
            u_email (str): The user's email.
            u_password (str): The user's password.

        Returns:
            str: The server's response to the login attempt.
        """
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

    def send_file(self, file_name, short_filename, short_file_date, file_bytes):
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
        self.client_socket.send(b'<SEND>')
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
        """
        Receives a list of checked files, a list of selected file names, and a save path.
        It sends the files to the client socket, receives a dictionary from the server,
        and saves the files to the specified save path.
        """
        self.client_socket.send(b'<RECV>')

        # Convert the list to a pickled string
        pickled_data = pickle.dumps(select_file_names_lst)

        # Send the length of the pickled data
        data_len = len(pickled_data)
        print(data_len)
        self.client_socket.send(str(data_len).encode())

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
        """
        Sends a '<NARF>' message through the client socket, receives the length of the pickled data,
        receives the pickled data, loads the pickled data, and returns the saved file properties list.
        """
        self.client_socket.send(b'<NARF>')

        # Receive the length of the pickled data
        data_len = int(self.client_socket.recv(1024).decode())

        # Receive the pickled data
        pickled_data = self.client_socket.recv(data_len)

        # Load the pickled data
        saved_file_prop_lst = pickle.loads(pickled_data)


        return saved_file_prop_lst

    def delete_checked_files(self, select_file_names_lst):
        """
        Receives a list of checked files, a list of selected file names, and deletes the files.
        """
        self.client_socket.send(b'<DELETE>')

        # Convert the list to a pickled string
        pickled_data = pickle.dumps(select_file_names_lst)

        # Send the length of the pickled data
        self.client_socket.send(pickled_data)

        print("Files deleted successfully.")


    def rename_files(self, select_file_name, new_name):
        """
        Receives a list of checked files, a list of selected file names, and renames the files.
        """
        self.client_socket.send(b'<RENAME>')

        # Convert the list to a pickled string
        pickled_data = pickle.dumps(select_file_name)

        # Send the length of the pickled data
        self.client_socket.send(pickled_data)

        # Send the new name
        self.client_socket.send(new_name.encode())

        print("Files renamed successfully.")

