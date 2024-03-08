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

    def r_when_submit(self, attempt_type, u_email, u_username, u_password):
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

    def l_when_submit(self, attempt_type, u_email, u_password):
        field_dict = {
            'email': u_email,
            'password': u_password
        }

        data_dict = {"FLAG": attempt_type, "DATA": field_dict}
        self.send_data(self.client_socket, pickle.dumps(data_dict))

        server_answer = pickle.loads(self.recv_data(self.client_socket))
        answer_flag = server_answer.get("FLAG")
        return answer_flag





    def send_file(self, file_name, short_filename, short_file_date, file_size):
        file_content = b''
        with open(file_name, 'rb') as file:
            while True:
                # Read and send the file in chunks
                data = file.read(1024)
                if not data:
                    break
                file_content += data

        all_file_content = [short_filename, file_size, short_file_date, file_content]
        data_dict = {"FLAG": '<SEND>', "DATA": all_file_content}
        self.send_data(self.client_socket, pickle.dumps(data_dict))
        print(f"File '{file_name}' sent successfully")

    def receive_checked_files(self, select_file_names_lst, save_path):
        try:
            operation_dict = {"FLAG": '<ACTION>', "OPERATION": "<RECV>"}
            self.send_data(self.client_socket, pickle.dumps(operation_dict))

            # Convert the list to a pickled string
            pickled_data = pickle.dumps(select_file_names_lst)

            # Send the length of the pickled data as a fixed-size binary value
            data_len = struct.pack("!I", len(pickled_data))
            self.client_socket.send(data_len)

            # Send the pickled data
            self.client_socket.sendall(pickled_data)

            # Receive the length of the pickled dictionary data
            data_len = struct.unpack("!I", self.client_socket.recv(4))[0]

            # Receive the pickled dictionary data
            pickled_fdn_dict = self.client_socket.recv(data_len)

            # Load the dictionary
            file_data_name_dict = pickle.loads(pickled_fdn_dict)

            for indiv_filename, indiv_filebytes in file_data_name_dict.items():
                file_path = os.path.join(save_path, indiv_filename)
                with open(file_path, "wb") as file:
                    file.write(indiv_filebytes)
                    print(f"File '{indiv_filename}' received successfully.")

        except Exception as e:
            print(f"Error in receive_checked_files: {e}")

    def notify_and_receive_files(self):
        try:
            operation_dict = {"FLAG": '<ACTION>', "OPERATION": "<NARF>"}
            self.send_data(self.client_socket, pickle.dumps(operation_dict))

            received_data = pickle.loads(self.recv_data(self.client_socket))
            saved_file_prop_lst = received_data.get("DATA")

            return saved_file_prop_lst

        except Exception as e:
            print(f"Error in receive_checked_files: {e}")

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

    def rename_files(self, rename_data):
        """
        Receives a list of checked files, a list of tuples containing old names and new names, and renames the files.
        """
        self.client_socket.send(b'<RENAME>')

        # Convert the list of tuples to a pickled string
        pickled_data = pickle.dumps(rename_data)
        self.client_socket.send(len(pickled_data).to_bytes(4, byteorder='big'))
        self.client_socket.send(pickled_data)

        print("Files renamed successfully.")

    def favorite_file(self, file_name, switch_value):
        if switch_value == "on":
            self.client_socket.send(b'<FAVORITE>')

            self.client_socket.send(file_name.encode('utf-8'))
            print(f"File '{file_name}' favorited.")

        else:
            self.client_socket.send(b'<UNFAVORITE>')

            self.client_socket.send(file_name.encode('utf-8'))
            print(f"File '{file_name}' unfavorited.")

    def get_all_users(self):
        self.client_socket.send(b'<GET_USERS>')
        pickled_all_users = self.client_socket.recv(1024)
        all_users = pickle.loads(pickled_all_users)
        return all_users

    def create_group(self, group_name, group_participants, permissions):
        print(f"nigga {group_name}")
        print(f"nigga2 {group_participants}")
        self.client_socket.send(b'<CREATE_GROUP>')

        self.client_socket.send(pickle.dumps([group_name, group_participants, permissions]))

    def get_all_groups(self):
        self.client_socket.send(b'<GET_ROOMS>')
        pickled_all_rooms = self.client_socket.recv(1024)
        all_rooms = pickle.loads(pickled_all_rooms)
        return all_rooms


class GroupCommunication:
    def __init__(self, client_socket, on_broadcast_callback):
        self.client_socket = client_socket
        self.on_broadcast_callback = on_broadcast_callback  # Define the callback function

        self.receive_thread = None  # Thread for receiving broadcasted files
        self.running = False  # Flag to control the thread

    def get_all_users(self):
        self.client_socket.send(b'<GET_USERS>')
        pickled_all_users = self.client_socket.recv(1024)
        all_users = pickle.loads(pickled_all_users)
        return all_users

    def create_group(self, group_name, group_participants):
        print(f"nigga {group_name}")
        print(f"nigga2 {group_participants}")
        self.client_socket.send(b'<CREATE_GROUP>')

        self.client_socket.send(pickle.dumps([group_name, group_participants]))

    def join_group(self, group_name):
        self.client_socket.send(b'<JOIN_GROUP>')
        self.client_socket.send(group_name.encode('utf-8'))
        ans = self.client_socket.recv(64)
        if ans == b'<JOINED>':
            print("joined")
            saved_file_prop_lst = self.notify_and_receive_files()
            self.on_broadcast_callback(pickle.dumps([saved_file_prop_lst, "<NARF>"]))
            # Create a new thread to receive broadcasted files
            # Start the thread when the client joins the group
            self.running = True
            self.receive_thread = threading.Thread(target=self.receive_broadcasted_files,
                                                   args=(self.on_broadcast_callback,))
            self.receive_thread.start()

    def leave_group(self):
        self.client_socket.send(b'<LEAVE_GROUP>')
        self.running = False
        if self.receive_thread:
            self.receive_thread.join()

    def receive_broadcasted_files(self, on_broadcast_callback):
        while self.running:
            data = self.client_socket.recv(1024)

            if data == b'<LEFT>':
                self.running = False
                break
            # Call the callback function in GroupsPage
            self.on_broadcast_callback(data)

    def send_file(self, file_name, short_filename, short_file_date, file_bytes):
        self.client_socket.send(b'<SEND>')

        self.client_socket.send(pickle.dumps([short_filename, file_bytes, short_file_date]))

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

    def delete_checked_files(self, select_file_names_lst):
        self.client_socket.send(b'<DELETE>')

        # Convert the list to a pickled string
        pickled_data = pickle.dumps(select_file_names_lst)

        # Send the length of the pickled data
        self.client_socket.send(pickled_data)

    def notify_and_receive_files(self):
        """
        Sends a '<NARF>' message through the client socket, receives the length of the pickled data,
        receives the pickled data, loads the pickled data, and returns the saved file properties list.
        """
        self.client_socket.send(b'<NARF>')

        # Receive the packed length (assuming it's a 4-byte integer)
        len_data = self.client_socket.recv(4)

        # Unpack the length using struct
        data_len = int.from_bytes(len_data, byteorder='big')

        # Receive the pickled data
        pickled_data = self.client_socket.recv(data_len)

        # Load the pickled data
        saved_file_prop_lst = pickle.loads(pickled_data)

        return saved_file_prop_lst

    def rename_files(self, rename_data):
        """
        Receives a list of checked files, a list of tuples containing old names and new names, and renames the files.
        """
        self.client_socket.send(b'<RENAME>')
        print("sent")
        # Convert the list of tuples to a pickled string
        pickled_data = pickle.dumps(rename_data)
        self.client_socket.send(len(pickled_data).to_bytes(4, byteorder='big'))
        self.client_socket.send(pickled_data)

        print("Files renamed successfully.")

    def receive_checked_files(self, select_file_names_lst, save_path):
        try:
            self.client_socket.send(b'<RECV>')

            # Convert the list to a pickled string
            pickled_data = pickle.dumps(select_file_names_lst)

            # Send the length of the pickled data as a fixed-size binary value
            data_len = struct.pack("!I", len(pickled_data))
            self.client_socket.send(data_len)

            # Send the pickled data
            self.client_socket.sendall(pickled_data)

            # Receive the length of the pickled dictionary data
            data_len = struct.unpack("!I", self.client_socket.recv(4))[0]

            # Receive the pickled dictionary data
            pickled_fdn_dict = self.client_socket.recv(data_len)

            # Load the dictionary
            file_data_name_dict = pickle.loads(pickled_fdn_dict)

            for indiv_filename, indiv_filebytes in file_data_name_dict.items():
                file_path = os.path.join(save_path, indiv_filename)
                with open(file_path, "wb") as file:
                    file.write(indiv_filebytes)
                    print(f"File '{indiv_filename}' received successfully.")


        except Exception as e:
            print(f"Error in receive_checked_files: {e}")


# ------------Client setup------------
HOST = '127.0.0.1'
PORT = 40300


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
