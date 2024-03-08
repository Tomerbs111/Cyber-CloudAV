import pickle
import socket
import struct
import threading
from database.AuthManager import AuthManager
from database.GroupFiles import GroupFiles
from database.UserFiles import UserFiles
from database.RoomManager import RoomManager

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

    def send_data(self, client_socket: socket, data: str | bytes):
        if isinstance(data, str):
            data = pickle.dumps(data)

        data_len = len(data).to_bytes(4, byteorder='big')
        client_socket.send(data_len + data)

    def recv_data(self, client_socket: socket):
        data_len = client_socket.recv(4)

        while len(data_len) < 4:
            data_len += client_socket.recv(4 - len(data_len))
        len_to_int = int.from_bytes(data_len, byteorder='big')
        data = client_socket.recv(len_to_int)

        while len(data) < len_to_int:
            data += client_socket.recv(len_to_int - len(data))

        return data

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
        except Exception as e:
            print(f"Unexpected error in server start: {e}")
        finally:
            self.server_socket.close()

    def handle_register_login(self, client_socket, identifier):
        try:
            while True:
                received_data = pickle.loads(self.recv_data(client_socket))
                authentication_flag = received_data.get("FLAG")
                field_dict = received_data.get("DATA")
                db_authentication = AuthManager()

                if authentication_flag == "<REGISTER>":
                    u_email = field_dict['email']
                    u_username = field_dict['username']
                    u_password = field_dict['password']

                    answer_to_send = self.handle_register_info(u_email, u_username, u_password, db_authentication)

                elif authentication_flag == "<LOGIN>":
                    u_email = field_dict['email']
                    u_password = field_dict['password']

                    answer_to_send = self.handle_login_info(u_email, u_password, db_authentication)

                self.send_data(client_socket, pickle.dumps(answer_to_send))
                if answer_to_send.get("FLAG") == "<SUCCESS>":
                    identifier = answer_to_send.get("DATA")

                if identifier:
                    # Start a new thread to handle the client
                    client_handler = threading.Thread(
                        target=self.handle_requests,
                        args=(client_socket, identifier)
                    )

                    client_handler.start()
                    break  # Break out of the inner loop if registration or login is successful

        except (socket.error, IOError) as e:
            print(f"Error in handle_register_login: {e}")
            client_socket.close()

    def broadcast_files(self):
        try:
            while True:
                # Get a message from the queue
                queued_data = self.file_queue.get()

                # Unpack the message to get the client socket and the file data
                sender_socket, file_data = queued_data

                # Broadcast the message to all connected clients except the sender
                for g_users in self.clients_list:
                    try:
                        if g_users.user_socket != sender_socket:
                            self.send_data(g_users.user_socket, pickle.dumps(file_data))
                    except Exception as e:
                        print(f"Error in broadcast_files: {e}")

        except Exception as e:
            print(f"Error in broadcast_files thread: {e}")

    def handle_register_info(self, u_email, u_username, u_password, auth):
        try:
            db_answer = auth.register(u_email, u_username, u_password)

            # Create a dictionary with "FLAG" and "DATA" keys
            answer_to_send = {"FLAG": db_answer, "DATA": None}

            if db_answer == "<EXISTS>":
                answer_to_send["DATA"] = "Email already exists"
            elif db_answer == "<SUCCESS>":
                userid = auth.get_userid(u_email)
                answer_to_send["DATA"] = userid[0]

            return answer_to_send

        except Exception as e:
            answer_to_send["FLAG"] = "<FAILED>"
            answer_to_send["DATA"] = f"Unexpected error during registration: {e}"
            return answer_to_send

    def handle_login_info(self, u_email, u_password, auth):
        try:
            db_answer = auth.login(u_email, u_password)

            # Create a dictionary with "FLAG" and "DATA" keys
            answer_to_send = {"FLAG": None, "DATA": None}

            if db_answer == "<NO_EMAIL_EXISTS>":

                answer_to_send["FLAG"] = "<NO_EMAIL_EXISTS>"
                answer_to_send["DATA"] = "Email doesn't exist"

            elif db_answer == "<WRONG_PASSWORD>":
                answer_to_send["FLAG"] = "<WRONG_PASSWORD>"
                answer_to_send["DATA"] = "Wrong password"

            else:
                userid = auth.get_userid(u_email)
                answer_to_send["FLAG"] = "<SUCCESS>"
                answer_to_send["DATA"] = userid[0]

            return answer_to_send

        except Exception as e:
            answer_to_send["FLAG"] = "<FAILED>"
            answer_to_send["DATA"] = f"Unexpected error during login: {e}"
            return answer_to_send

    def handle_requests(self, client_socket, identifier):
        try:
            user_files_manager = UserFiles(identifier)

            while True:
                action = None
                received_data = pickle.loads(self.recv_data(client_socket))
                if received_data.get("FLAG") == "<ACTION>":
                    action = received_data.get("OPERATION")

                if received_data.get("FLAG") == "<NARF>":
                    self.handle_narf_action(client_socket, user_files_manager)

                elif action == "X":
                    self.handle_sign_out_action(identifier)
                    break

                elif received_data.get("FLAG") == "<SEND>":
                    send_data = received_data.get("DATA")
                    self.handle_save_file_action(client_socket, user_files_manager, send_data)

                elif received_data.get("FLAG") == "<RECV>":
                    recv_data = received_data.get("DATA")
                    self.handle_read_files_action(client_socket, user_files_manager, recv_data)

                elif received_data.get("FLAG") == "<DELETE>":
                    delete_data = received_data.get("DATA")
                    self.handle_delete_action(client_socket, user_files_manager, delete_data)

                elif received_data.get("FLAG") == "<RENAME>":
                    rename_data = received_data.get("DATA")
                    self.handle_rename_action(client_socket, user_files_manager, rename_data)

                elif received_data.get("FLAG") == "<FAVORITE>":
                    favorite_data = received_data.get("DATA")
                    self.handle_favorite_action(client_socket, user_files_manager, favorite_data)

                elif received_data.get("FLAG") == "<UNFAVORITE>":
                    unfavorite_data = received_data.get("DATA")
                    self.handle_unfavorite_action(client_socket, user_files_manager, unfavorite_data)

                elif received_data.get("FLAG") == "<GET_USERS>":
                    self.handle_get_users_action(client_socket, identifier)

                elif received_data.get("FLAG") == "<CREATE_GROUP>":
                    create_group_data = received_data.get("DATA")
                    self.handle_create_group_action(client_socket, identifier, create_group_data)

                elif received_data.get("FLAG") == "<GET_ROOMS>":
                    self.handle_get_rooms_action(client_socket, identifier)

                elif received_data.get("FLAG") == "<JOIN_GROUP>":
                    join_group_data = received_data.get("DATA")
                    self.handle_join_group_action(client_socket, identifier, join_group_data)
                    break

        except (socket.error, IOError) as e:
            print(f"Error in handle_requests: {e}")
            client_socket.close()

    def handle_group_requests(self, client_socket: socket, identifier):
        try:
            group_manager = GroupFiles(AuthManager().get_email(identifier))

            while True:
                action = None
                received_data = pickle.loads(self.recv_data(client_socket))
                if received_data.get("FLAG") == "<ACTION>":
                    action = received_data.get("OPERATION")

                if received_data.get("FLAG") == "<NARF>":
                    self.handle_narf_action(client_socket, group_manager)

                elif received_data.get("FLAG") == "<RECV>":
                    recv_data = received_data.get("DATA")
                    self.handle_read_files_action(client_socket, group_manager, recv_data)

                elif received_data.get("FLAG") == "<SEND>":
                    send_data = received_data.get("DATA")
                    self.handle_save_file_action(client_socket, group_manager, send_data)

                elif received_data.get("FLAG") == "<DELETE>":
                    delete_data = received_data.get("DATA")
                    self.handle_delete_action(client_socket, group_manager, delete_data)

                elif received_data.get("FLAG") == "<RENAME>":
                    rename_data = received_data.get("DATA")
                    self.handle_rename_action(client_socket, group_manager, rename_data)

                elif received_data.get("FLAG") == "<CREATE_GROUP>":
                    create_group_data = received_data.get("DATA")
                    self.handle_create_group_action(client_socket, identifier, create_group_data)

                elif received_data.get("FLAG") == "<LEAVE_GROUP>":
                    self.handle_leave_group_action(client_socket, identifier)
                    break

        except (socket.error, IOError) as e:
            print(f"Error in handle_group_requests: {e}")
            client_socket.close()

    def handle_narf_action(self, client_socket, db_manager):
        try:
            saved_file_prop_lst = None
            if isinstance(db_manager, GroupFiles):
                group_name = self.get_group_name(client_socket)
                saved_file_prop_lst = db_manager.get_all_files_from_group(group_name)

            elif isinstance(db_manager, UserFiles):
                saved_file_prop_lst = db_manager.get_all_data()

            data_to_send = {"FLAG": "<NARF>", "DATA": saved_file_prop_lst}

            self.send_data(client_socket, pickle.dumps(data_to_send))

        except Exception as e:
            print(f"Error in handle_narf_action: {e}")
            client_socket.close()

    def handle_sign_out_action(self, identifier):
        print(f"User {identifier} has signed out.")

    def handle_save_file_action(self, client_socket, db_manager, all_file_content):
        try:
            file_name = all_file_content[0]
            file_size = all_file_content[1]
            file_date = all_file_content[2]
            file_bytes = all_file_content[3]

            if isinstance(db_manager, GroupFiles):
                group_name = self.get_group_name(client_socket)
                db_manager.insert_file(file_name, file_size, file_date, group_name, file_bytes)

                file_info = self.get_file_info(db_manager, group_name, file_name)
                queued_info = {"FLAG": "<SEND>", "DATA": file_info}

                self.file_queue.put((client_socket, queued_info))

            elif isinstance(db_manager, UserFiles):
                db_manager.insert_file(file_name, file_size, file_date, file_bytes)

            print(f"File '{file_name}' received and saved in the database")

        except Exception as e:
            print(f"Error in handle_save_file_action: {e}")
            client_socket.close()

    def handle_read_files_action(self, client_socket, db_manager, select_file_names_lst):
        try:
            file_data_name_dict = {}
            if isinstance(db_manager, GroupFiles):
                for individual_file in select_file_names_lst:
                    file_data = db_manager.get_file_data(self.get_group_name(client_socket), individual_file)[0]
                    file_data_name_dict[individual_file] = file_data

            elif isinstance(db_manager, UserFiles):
                for individual_file in select_file_names_lst:
                    file_data = db_manager.get_file_data(individual_file)[0]
                    file_data_name_dict[individual_file] = file_data

            data_dict = {"FLAG": '<RECV>', "DATA": file_data_name_dict}
            self.send_data(client_socket, pickle.dumps(data_dict))

            print("Files sent successfully.")

        except Exception as e:
            print(f"Error in handle_read_files_action: {e}")

    def handle_delete_action(self, client_socket, db_manager, select_file_names_lst):
        try:
            if isinstance(db_manager, GroupFiles):
                for individual_file in select_file_names_lst:
                    db_manager.delete_file(self.get_group_name(client_socket), individual_file)
                    queued_info = {"FLAG": "<DELETE>", "DATA": individual_file}

                    self.file_queue.put((client_socket, queued_info))

            elif isinstance(db_manager, UserFiles):
                for individual_file in select_file_names_lst:
                    db_manager.delete_file(individual_file)
            print("Files deleted successfully.")

        except Exception as e:
            print(f"Error in handle_delete_action: {e}")
            client_socket.close()

    def handle_rename_action(self, client_socket, db_manager, rename_data):
        try:
            old_name, new_name = rename_data

            if isinstance(db_manager, GroupFiles):
                group_name = self.get_group_name(client_socket)
                db_manager.rename_file(group_name, old_name, new_name)
                queued_info = {"FLAG": "<RENAME>", "DATA": rename_data}

                self.file_queue.put((client_socket, queued_info))

            elif isinstance(db_manager, UserFiles):
                db_manager.rename_file(old_name, new_name)

            print("File renamed successfully.")

        except Exception as e:
            print(f"Error in handle_rename_action: {e}")
            client_socket.close()

    def handle_favorite_action(self, client_socket, user_files_manager, favorite_file_name):
        try:
            user_files_manager.set_favorite_status(favorite_file_name, 1)
            print("File favorited successfully.")
        except Exception as e:
            print(f"Error in handle_favorite_action: {e}")
            client_socket.close()

    def handle_unfavorite_action(self, client_socket, user_files_manager, unfavorite_file_name):
        try:
            user_files_manager.set_favorite_status(unfavorite_file_name, 0)
            print("File unfavorited successfully.")
        except Exception as e:
            print(f"Error in handle_unfavorite_action: {e}")
            client_socket.close()

    def handle_get_users_action(self, client_socket, identifier):
        all_users = AuthManager().get_all_users(identifier)
        data_to_send = {"FLAG": "<GET_USERS>", "DATA": all_users}
        self.send_data(client_socket, pickle.dumps(data_to_send))

    def handle_create_group_action(self, client_socket, identifier, group_data):
        user_email = AuthManager().get_email(identifier)

        group_name = group_data[0]
        group_participants = group_data[1]
        group_participants.append(user_email)
        group_permissions = group_data[2]
        permission_values = []

        for permission in group_permissions:
            permission_values.append(str(group_permissions[permission]))

        print(permission_values)

        # Create a room in the database using RoomManager
        room_manager = RoomManager()
        room_manager.insert_room(group_name, ",".join(group_participants), user_email, permission_values)
        print(f"Group created successfully.")

    def handle_get_rooms_action(self, client_socket, identifier):
        try:
            user_email = AuthManager().get_email(identifier)
            room_manager = RoomManager()

            rooms_containing_user = room_manager.get_rooms_by_participant(user_email)

            # Create a dictionary with room names as keys and permissions as values
            rooms_dict = {}
            for room in rooms_containing_user:
                room_permissions = room_manager.get_room_permissions(room)
                rooms_dict[room] = room_permissions

            # Pickle and send the dictionary over the socket
            data_to_send = {"FLAG": "<GET_ROOMS>", "DATA": rooms_dict}
            self.send_data(client_socket, pickle.dumps(data_to_send))

            print(f"Sent rooms containing {user_email} to the client.")

        except Exception as e:
            print(f"Error in fetch_rooms_for_user: {e}")
            client_socket.close()

    def is_user_admin(self, username, group_name):
        try:
            room_manager = RoomManager()
            admin_email = room_manager.get_room_admin(group_name)

            if admin_email == AuthManager().get_email(username):
                return True
            else:
                return False

        except Exception as e:
            print(f"Error in is_user_admin: {e}")
            return False

    def handle_join_group_action(self, client_socket, identifier, group_name):
        try:
            user_email = AuthManager().get_email(identifier)

            # Check if the user is already in the clients_list with a different group name
            user_found = False
            for group_user in self.clients_list:
                if group_user.user_socket == client_socket:
                    if group_user.group_name != group_name:
                        group_user.group_name = group_name  # Change the group_name to the new one
                    user_found = True
                    break

            if not user_found:
                # If the user is not in the list, append with the received group name
                self.clients_list.append(GroupUser(client_socket, user_email, group_name))

            self.send_data(client_socket, pickle.dumps({"FLAG": "<JOINED>"}))
            print(f"User {user_email} joined the group '{group_name}'.")

            group_handler = threading.Thread(
                target=self.handle_group_requests,
                args=(client_socket, identifier)
            )
            group_handler.start()

        except Exception as e:
            print(f"Error in handle_join_group_action: {e}")
            client_socket.close()

    def handle_leave_group_action(self, client_socket, identifier):
        try:
            for group_user in self.clients_list:
                if group_user.user_socket == client_socket:
                    self.clients_list.remove(group_user)
                    break
            self.send_data(client_socket, pickle.dumps({"FLAG": "<LEFT>"}))
            client_handler = threading.Thread(
                target=self.handle_requests,
                args=(client_socket, identifier)
            )
            client_handler.start()

        except Exception as e:
            print(f"Error in handle_leave_group_action: {e}")
            client_socket.close()

    def get_file_info(self, group_manager, group_name, filename):
        return group_manager.get_file_info(group_name, filename)

    def get_group_name(self, client_socket):
        for index, group_user in enumerate(self.clients_list):
            if group_user.user_socket == client_socket:
                return group_user.group_name
if __name__ == "__main__":
    server = Server()
    server.start()
