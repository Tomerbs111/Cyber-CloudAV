import socket
import os
import pickle
import struct
import threading

from GUI.MyApp import MyApp


class ClientCommunication:
    def __init__(self, client_socket: socket):
        self.client_socket = client_socket

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

    def handle_client_register(self, attempt_type, u_email, u_username, u_password):
        field_dict = {
            'email': u_email,
            'username': u_username,
            'password': u_password,
        }

        data_dict = {"FLAG": attempt_type, "DATA": field_dict}
        self.send_data(self.client_socket, pickle.dumps(data_dict))

        server_answer = pickle.loads(self.recv_data(self.client_socket))
        answer_flag = server_answer.get("FLAG")
        return answer_flag

    def handle_client_login(self, attempt_type, u_email, u_password):
        field_dict = {
            'email': u_email,
            'password': u_password
        }

        data_dict = {"FLAG": attempt_type, "DATA": field_dict}
        self.send_data(self.client_socket, pickle.dumps(data_dict))

        server_answer = pickle.loads(self.recv_data(self.client_socket))
        print(server_answer)
        answer_flag = server_answer.get("FLAG")
        if answer_flag == "<SUCCESS>":
            username = server_answer.get("DATA")
            return username
        else:
            return answer_flag

    def handle_send_file_request(self, file_name, short_filename, short_file_date, file_size):
        file_content = b''
        with open(file_name, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                file_content += data

        all_file_content = [short_filename, file_size, short_file_date, file_content]
        data_dict = {"FLAG": '<SEND>', "DATA": all_file_content}
        self.send_data(self.client_socket, pickle.dumps(data_dict))

        print(f"File '{file_name}' sent successfully")

    def handle_download_request_client(self, select_file_names_lst, save_path):
        try:
            data_dict = {"FLAG": '<RECV>', "DATA": select_file_names_lst}
            self.send_data(self.client_socket, pickle.dumps(data_dict))

            received_data = pickle.loads(self.recv_data(self.client_socket))
            file_data_name_dict = received_data.get("DATA")

            for indiv_filename, indiv_filebytes in file_data_name_dict.items():
                file_path = os.path.join(save_path, indiv_filename)
                with open(file_path, "wb") as file:
                    file.write(indiv_filebytes)
                    print(f"File '{indiv_filename}' received successfully.")

        except Exception as e:
            print(f"Error in receive_checked_files: {e}")

    def handle_presaved_files_client(self):
        try:
            operation_dict = {"FLAG": "<NARF>"}
            self.send_data(self.client_socket, pickle.dumps(operation_dict))

            received_data = pickle.loads(self.recv_data(self.client_socket))
            saved_file_prop_lst = received_data.get("DATA")
            print(saved_file_prop_lst)

            return saved_file_prop_lst

        except Exception as e:
            print(f"Error in handle_presaved_files_client: {e}")

    def handle_delete_request_client(self, select_file_names_lst):
        data_dict = {"FLAG": '<DELETE>', "DATA": select_file_names_lst}
        self.send_data(self.client_socket, pickle.dumps(data_dict))
        print("Files deleted successfully.")

    def handle_rename_request_client(self, rename_data):
        data_dict = {"FLAG": '<RENAME>', "DATA": rename_data}
        self.send_data(self.client_socket, pickle.dumps(data_dict))
        print("Files renamed successfully.")

    def handle_set_favorite_request_client(self, file_name, switch_value):
        if switch_value == "on":
            data_dict_on = {"FLAG": '<FAVORITE>', "DATA": file_name}
            self.send_data(self.client_socket, pickle.dumps(data_dict_on))

            print(f"File '{file_name}' favorited.")

        elif switch_value == "off":
            data_dict_off = {"FLAG": '<UNFAVORITE>', "DATA": file_name}
            self.send_data(self.client_socket, pickle.dumps(data_dict_off))

            print(f"File '{file_name}' unfavorited.")

    def get_all_registered_users(self):
        data_dict = {"FLAG": '<GET_USERS>'}
        self.send_data(self.client_socket, pickle.dumps(data_dict))

        received_data = pickle.loads(self.recv_data(self.client_socket))
        all_users = received_data.get("DATA")
        return all_users

    def handle_create_group_request(self, group_name, group_participants, permissions):
        group_properties = [group_name, group_participants, permissions]
        data_dict = {"FLAG": '<CREATE_GROUP>', "DATA": group_properties}
        self.send_data(self.client_socket, pickle.dumps(data_dict))

    def get_all_groups(self):
        operation_dict = {"FLAG": "<GET_ROOMS>"}
        self.send_data(self.client_socket, pickle.dumps(operation_dict))

        received_data = pickle.loads(self.recv_data(self.client_socket))
        all_rooms = received_data.get("DATA")
        return all_rooms


class GroupCommunication:
    def __init__(self, client_socket, handle_broadcast_requests):
        self.client_socket = client_socket
        self.handle_broadcast_requests = handle_broadcast_requests  # Define the callback function

        self.receive_thread = None  # Thread for receiving broadcasted files
        self.running = False  # Flag to control the thread

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

    def get_all_registered_users(self):
        data_dict = {"FLAG": '<GET_USERS>'}
        self.send_data(self.client_socket, pickle.dumps(data_dict))

        received_data = pickle.loads(self.recv_data(self.client_socket))
        all_users = received_data.get("DATA")
        return all_users

    def handle_create_group_request(self, group_name, group_participants):
        data_dict = {"FLAG": '<CREATE_GROUP>', "DATA": [group_name, group_participants]}
        self.send_data(self.client_socket, pickle.dumps(data_dict))

    def handle_join_group_request(self, group_name):
        data_dict = {"FLAG": '<JOIN_GROUP>', "DATA": group_name}
        self.send_data(self.client_socket, pickle.dumps(data_dict))

        received_data = pickle.loads(self.recv_data(self.client_socket))
        print(received_data)
        if received_data.get("FLAG") == '<JOINED>':
            print("joined")
            saved_file_prop_lst = self.handle_presaved_files_group()
            print("i like man")
            # Check if the callback is set before calling it
            if self.handle_broadcast_requests:
                self.handle_broadcast_requests(pickle.dumps({"FLAG": "<NARF>", "DATA": saved_file_prop_lst}))

            self.running = True
            self.receive_thread = threading.Thread(target=self.handle_broadcasted_group_data,
                                                   args=(self.handle_broadcast_requests,))
            self.receive_thread.start()

    def handle_leave_group_request(self):
        self.send_data(self.client_socket, pickle.dumps({"FLAG": '<LEAVE_GROUP>'}))
        self.running = False
        if self.receive_thread:
            self.receive_thread.join()

    def handle_broadcasted_group_data(self, on_broadcast_callback):
        while self.running:
            received_data = pickle.loads(self.recv_data(self.client_socket))
            print(f"Received data from broadcast in client: {received_data}")
            flag = received_data.get("FLAG")

            if flag == "<LEFT>":
                print("left")
                self.running = False
                break

            # Check if the callback is set before calling it
            if on_broadcast_callback:
                on_broadcast_callback(received_data)

    def handle_send_file_request(self, file_name, short_filename, short_file_date, file_size):
        file_content = b''
        with open(file_name, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                file_content += data

        all_file_content = [short_filename, file_size, short_file_date, file_content]
        data_dict = {"FLAG": '<SEND>', "DATA": all_file_content}

        self.send_data(self.client_socket, pickle.dumps(data_dict))
        print(f"File '{file_name}' sent successfully")

    def handle_download_request_group(self, select_file_names_lst):
        try:
            print("Receiving files...")
            data_dict = {"FLAG": '<RECV>', "DATA": select_file_names_lst}
            self.send_data(self.client_socket, pickle.dumps(data_dict))

        except Exception as e:
            print(f"Error in receive_checked_files: {e}")

    def handle_presaved_files_group(self):
        try:
            operation_dict = {"FLAG": "<NARF>"}
            self.send_data(self.client_socket, pickle.dumps(operation_dict))

            received_data = pickle.loads(self.recv_data(self.client_socket))
            saved_file_prop_lst = received_data.get("DATA")

            return saved_file_prop_lst

        except Exception as e:
            print(f"Error in handle_presaved_files_client: {e}")

    def handle_delete_request_group(self, select_file_names_lst):
        data_dict = {"FLAG": '<DELETE>', "DATA": select_file_names_lst}
        self.send_data(self.client_socket, pickle.dumps(data_dict))
        print("Files deleted successfully.")

    def handle_rename_request_group(self, rename_data):
        data_dict = {"FLAG": '<RENAME>', "DATA": rename_data}
        self.send_data(self.client_socket, pickle.dumps(data_dict))
        print("Files renamed successfully.")


# ------------Client setup------------
HOST = '127.0.0.1'  # '192.168.1.152'
PORT = 40301


class MainClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))
        self.client_communicator = ClientCommunication(self.client_socket)
        self.group_communicator = GroupCommunication(self.client_socket, None)

    def run(self):
        try:
            while True:
                app = MyApp(self.client_communicator, self.group_communicator)
                app.mainloop()
                self.client_socket.sendall("X".encode())
                self.client_socket.close()
                break
        except (socket.error, IOError) as e:
            print(f"Error: {e}")
        finally:
            self.client_socket.close()


if __name__ == "__main__":
    main_client = MainClient()
    main_client.run()
