import pickle
import socket
import threading

from database.Authentication import UserAuthentication
from database.UserFiles import UserFiles
from datetime import datetime

HOST = '0.0.0.0'
PORT = 40301


def handle_register_info(client_socket: socket, u_email: str, u_username: str, u_password: str) -> int | str:
    """
    Handles the registration information for a new user.

    Args:
        client_socket (socket): The client socket for communication.
        u_email (str): The email of the user for registration.
        u_username (str): The username of the user for registration.
        u_password (str): The password of the user for registration.

    Returns:
        int | str: The user ID if registration is successful, or a string indicating failure.
    """
    auth = UserAuthentication()
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
    """
    Handle login information and authenticate the user.

    Args:
        client_socket (socket): The client socket for communication.
        u_email (str): The user's email for login.
        u_password (str): The user's password for login.

    Returns:
        str | None: The user ID if login is successful, otherwise None.
    """
    auth = UserAuthentication()
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


def handle_narf_action(client_socket, user_files_manager):
    """
    Handle the "<NARF>" action.
    """
    saved_file_prop_lst = user_files_manager.get_all_data()

    # Convert the list to a pickled string
    pickled_data = pickle.dumps(saved_file_prop_lst)

    # Send the length of the pickled data
    data_len = str(len(pickled_data))
    client_socket.send(data_len.encode())

    # Send the pickled data
    client_socket.send(pickled_data)


def handle_sign_out_action(identifier):
    """
    Handle the "X" action.
    """
    print(f"User {identifier} has signed out.")


def handle_save_file_action(client_socket, user_files_manager):
    """
    Handle the "S" action.
    """
    # server is getting the file properties to write in db
    file_prop_lst = pickle.loads(client_socket.recv(1024))

    file_name = file_prop_lst[0]
    file_size = file_prop_lst[1]
    file_date = file_prop_lst[2]
    client_socket.send(b"<GOT_PROP>")

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

    user_files_manager.insert_file(file_name, file_size, file_date, all_data)
    print(f"File '{file_name}' received and saved in the database")


def handle_read_files_action(client_socket, user_files_manager):
    """
    Handle the "<R>" action.
    """
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


def handle_delete_action(client_socket, user_files_manager):
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


def handle_requests(client_socket: socket, identifier: int):
    """
    A function to handle requests from a client socket.
    """
    try:
        user_files_manager = UserFiles(identifier)
        while True:
            action = client_socket.recv(1024).decode()

            if action == "<NARF>":
                handle_narf_action(client_socket, user_files_manager)

            elif action == "X":
                handle_sign_out_action(identifier)
                break

            elif action == "<SEND>":
                handle_save_file_action(client_socket, user_files_manager)

            elif action == "<RECV>":
                handle_read_files_action(client_socket, user_files_manager)

            elif action == "<DELETE>":
                handle_delete_action(client_socket, user_files_manager)

    except (socket.error, IOError) as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()


def send_presaved_files_to_client(client_socket, identifier):
    """
    Send presaved files to the client using the provided client socket and identifier.
    """
    try:
        user_files_manager = UserFiles(f'u_{identifier}')
        presaved_files_dict = user_files_manager.get_all_data(identifier)

        # Send the presaved files dictionary to the client
        client_socket.sendall(pickle.dumps(presaved_files_dict))
    except Exception as e:
        print(f"Error sending presaved files data to client: {e}")


def handle_register_login(client_socket: socket, identifier):
    """
    Handle the registration or login of a client.

    Parameters:
        client_socket (socket): The socket connected to the client.
        identifier: The identifier of the client.

    Returns:
        None
    """
    try:
        while True:
            u_status = client_socket.recv(1024).decode()
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
                break  # Break out of the inner loop if registration or login is successful

    except (socket.error, IOError) as e:
        print(f"Error: {e}")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        identifier = None

        client_register_login_handler = threading.Thread(target=handle_register_login,
                                                         args=(client_socket, identifier))
        client_register_login_handler.start()

except KeyboardInterrupt:
    print("Server terminated by user.")
finally:
    server_socket.close()
