import pickle
import socket
import threading
from database.AuthManager import AuthManager
from database.GroupFiles import GroupFiles
from database.UserFiles import UserFiles
from GroupUser import GroupUser
from queue import Queue

HOST = '0.0.0.0'
PORT = 40301


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(5)
        print(f"Server listening on {HOST}:{PORT}")

        # Initialize clients list
        self.clients_list = []

        # Message queue for broadcasting
        self.file_queue = Queue()

        # Create a thread for broadcasting messages
        self.broadcast_thread = threading.Thread(target=self.broadcast_files)
        self.broadcast_thread.start()

    def start(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from {client_address}")

                identifier = None

                client_register_login_handler = threading.Thread(
                    target=self.handle_register_login,
                    args=(client_socket, identifier)
                )
                client_register_login_handler.start()

        except KeyboardInterrupt:
            print("Server terminated by user.")
        finally:
            self.server_socket.close()

    def handle_register_login(self, client_socket, identifier):
        try:
            while True:
                u_status = client_socket.recv(1024).decode()
                if u_status == "<REGISTER>":
                    field_dict = pickle.loads(client_socket.recv(1024))
                    u_email = field_dict['email']
                    u_username = field_dict['username']
                    u_password = field_dict['password']

                    identifier = self.handle_register_info(client_socket, u_email, u_username, u_password)

                elif u_status == "<LOGIN>":
                    field_dict = pickle.loads(client_socket.recv(1024))
                    u_email = field_dict['email']
                    u_password = field_dict['password']

                    identifier = self.handle_login_info(client_socket, u_email, u_password)

                if identifier and identifier != "<EXISTS>":
                    # Start a new thread to handle the client
                    client_handler = threading.Thread(
                        target=self.handle_requests,
                        args=(client_socket, identifier)
                    )

                    client_handler.start()
                    break  # Break out of the inner loop if registration or login is successful

        except (socket.error, IOError) as e:
            print(f"Error: {e}")

    def broadcast_files(self):
        while True:
            print("Broadcasting files...")
            # Get a message from the queue
            pickled_file = self.file_queue.get()

            # Unpack the message to get the client socket and the file data
            sender_socket, file_data = pickled_file

            # Broadcast the message to all connected clients except the sender
            for g_users in self.clients_list:
                if g_users.user_socket != sender_socket:
                    g_users.user_socket.send(b'<BROADCAST>' + file_data)

    def handle_register_info(self, client_socket, u_email, u_username, u_password):
        auth = AuthManager()
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

    def handle_login_info(self, client_socket, u_email, u_password):
        auth = AuthManager()
        try:
            auth_ans = auth.login(u_email, u_password)
            client_socket.send(auth_ans.encode())
            if auth_ans == "<NO_EMAIL_EXISTS>":
                print("Login failed. No accounts under the provided email.")
                return
            elif auth_ans == "<WRONG_PASSWORD>":
                print("Login failed. Password doesn't match the provided email.")
                return
            else:
                print("User logged in Successfully")
                userid = auth.get_userid(u_email)
                return userid[0]

        except Exception as e:
            print(f"Unexpected error during login: {e}")
            client_socket.send("Unexpected error during Login".encode())
            return "<FAILED>"

    def handle_requests(self, client_socket, identifier):
        try:
            user_files_manager = UserFiles(identifier)

            while True:
                action = client_socket.recv(1024).decode()

                if action == "<NARF>":
                    self.handle_narf_action(client_socket, user_files_manager)

                elif action == "X":
                    self.handle_sign_out_action(identifier)
                    break

                elif action == "<SEND>":
                    print("hello")
                    self.handle_save_file_action(client_socket, user_files_manager)

                elif action == "<RECV>":
                    self.handle_read_files_action(client_socket, user_files_manager)

                elif action == "<DELETE>":
                    self.handle_delete_action(client_socket, user_files_manager)

                elif action == "<RENAME>":
                    self.handle_rename_action(client_socket, user_files_manager)

                elif action == "<FAVORITE>":
                    self.handle_favorite_action(client_socket, user_files_manager)

                elif action == "<UNFAVORITE>":
                    self.handle_unfavorite_action(client_socket, user_files_manager)

                elif action == "<JOIN_GROUP>":
                    self.handle_join_group_action(client_socket, identifier)
                    break


        except (socket.error, IOError) as e:
            print(f"Error: {e}")

    def handle_group_requests(self, client_socket: socket, identifier):
        group_manager = GroupFiles(identifier)
        group_name = self.get_group_name(client_socket)

        while True:
            action = client_socket.recv(1024).decode()

            if action == "<SEND>":
                filename = self.handle_save_file_action(client_socket, group_manager)
                print("got filename")
                file_info = self.get_file_info(group_manager, group_name, filename)
                print(f"file info: {file_info}")
                # Enqueue the file info for broadcasting
                self.file_queue.put((client_socket, pickle.dumps(file_info)))

            elif action == "<LEAVE_GROUP>":
                self.handle_leave_group_action(client_socket, identifier)
                break

    def get_file_info(self, group_manager, group_name, filename):
        return group_manager.get_file_info(group_name, filename)

    def get_group_name(self, client_socket):
        for index, group_user in enumerate(self.clients_list):
            if group_user.user_socket == client_socket:
                return group_user.group_name

        return "group1"  # return a default group name

    def handle_narf_action(self, client_socket, user_files_manager):
        saved_file_prop_lst = user_files_manager.get_all_data()
        pickled_data = pickle.dumps(saved_file_prop_lst)

        data_len = str(len(pickled_data))
        client_socket.send(data_len.encode())

        client_socket.send(pickled_data)

    def handle_sign_out_action(self, identifier):
        print(f"User {identifier} has signed out.")

    def handle_save_file_action(self, client_socket, db_manager):
        file_prop_lst = pickle.loads(client_socket.recv(1024))

        file_name = file_prop_lst[0]
        file_size = file_prop_lst[1]
        file_date = file_prop_lst[2]
        # server got all the properties
        done_sending = False
        all_data = b""
        while not done_sending:
            data = client_socket.recv(1024)
            if data[-len(b"<END_OF_DATA>"):] == b"<END_OF_DATA>":
                done_sending = True
                all_data += data[:-len(b"<END_OF_DATA>")]
            else:
                all_data += data

        if isinstance(db_manager, GroupFiles):
            # If db_manager is a GroupFiles object, get the group name from the GroupUser
            group_name = self.get_group_name(client_socket)

            db_manager.insert_file(file_name, file_size, file_date, group_name, all_data)
            return file_name

        elif isinstance(db_manager, UserFiles):
            db_manager.insert_file(file_name, file_size, file_date, all_data)

        print(f"File '{file_name}' received and saved in the database")

    def handle_read_files_action(self, client_socket, user_files_manager):
        data_len = int(client_socket.recv(1024).decode())

        pickled_data = client_socket.recv(data_len)
        select_file_names_lst = pickle.loads(pickled_data)

        file_data_name_dict = {}
        for individual_file in select_file_names_lst:
            file_data = user_files_manager.get_file_data(individual_file)[0]
            file_data_name_dict[individual_file] = file_data

        # Convert the dictionary to a pickled string
        pickled_fdn_dict = pickle.dumps(file_data_name_dict)

        # Send the length of the pickled data
        data_len = str(len(pickled_fdn_dict))
        client_socket.send(data_len.encode())

        # Send the pickled dictionary
        client_socket.send(pickled_fdn_dict)

        print("Files sent successfully.")

    def handle_delete_action(self, client_socket, user_files_manager):
        """
            Handle the delete action by receiving data from the client socket and
            deleting the specified files using the user files manager.

            :param client_socket: The socket for communication with the client
            :param user_files_manager: The manager for the user's files
            """
        pickled_data = client_socket.recv(1024)
        select_file_names_lst = pickle.loads(pickled_data)

        for individual_file in select_file_names_lst:
            user_files_manager.delete_file(individual_file)
        print("Files deleted successfully.")

    def handle_rename_action(self, client_socket, user_files_manager):
        # Receive the pickled data containing a single tuple (old_name, new_name)
        pickled_data_length = client_socket.recv(4)
        data_length = int.from_bytes(pickled_data_length, byteorder='big')
        pickled_data = client_socket.recv(data_length)

        rename_data = pickle.loads(pickled_data)

        # Unpickle the data to get the tuple (old_name, new_name)
        old_name, new_name = rename_data

        # Perform renaming for a single file
        user_files_manager.rename_file(old_name, new_name)

        print("File renamed successfully.")

    def handle_favorite_action(self, client_socket, user_files_manager):
        favorite_file_name = client_socket.recv(1024).decode('utf-8')
        user_files_manager.set_favorite_status(favorite_file_name, 1)

        print("File favorited successfully.")

    def handle_unfavorite_action(self, client_socket, user_files_manager):
        unfavorite_file_name = client_socket.recv(1024).decode('utf-8')
        user_files_manager.set_unfavorite_status(unfavorite_file_name)
        print("File unfavorited successfully.")

    def handle_join_group_action(self, client_socket, identifier):
        user_email = AuthManager().get_email(identifier)
        self.clients_list.append(GroupUser(client_socket, user_email, "group1"))

        client_socket.send(b'<JOINED>')
        print("joined group")


        group_handler = threading.Thread(
            target=self.handle_group_requests,
            args=(client_socket, identifier)

        )
        group_handler.start()

    def handle_leave_group_action(self, client_socket, identifier):
        client_socket.send(b'<LEFT>')
        for group_user in self.clients_list:
            if group_user.user_socket == client_socket:
                self.clients_list.remove(group_user)
                break
        client_handler = threading.Thread(
            target=self.handle_requests,
            args=(client_socket, identifier)
        )

        client_handler.start()


if __name__ == "__main__":
    server = Server()
    server.start()
