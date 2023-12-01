from database.Authentication import UserAuthentication
import socket
import re

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
auth = UserAuthentication()


def when_try_register():
    max_attempts = 10
    attempts = 0

    while attempts < max_attempts:
        u_email = input("Enter email: ")
        u_username = input("Enter username: ")
        u_password = input("Enter password: ")

        # Checking email
        if len(u_email) > 0 and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', u_email):
            print("---Email is valid---")
            client_socket.send(u_email.encode())
        else:
            print("Invalid email format. Please enter a valid email.")
            attempts += 1
            continue

        # Checking username
        if len(u_username) > 0:
            print("---Username is valid---")
            client_socket.send(u_username.encode())
        else:
            print("You must provide a username.")
            attempts += 1
            continue

        # Checking password
        if len(u_password) > 0 and len(u_password) >= 8:
            print("---Password is valid---")
            client_socket.send(u_password.encode())
        else:
            print("Invalid password. Password must be 8 characters or longer.")
            attempts += 1
            continue

        print("All fields are good, waiting for server response...")
        break  # Break out of the loop as all fields are valid

    if attempts == max_attempts:
        print("Maximum number of attempts reached. Registration failed.")


def server_when_register():
    u_email = client_socket.recv(1024).decode()
    u_username = client_socket.recv(1024).decode()
    u_password = client_socket.recv(1024).decode()
    handle_register_info(u_email, u_username, u_password)


def handle_register_info(u_email, u_username, u_password):
    try:
        ans = auth.register(u_email, u_username, u_password)
        client_socket.send(ans.encode())
        if ans == "<EXISTS>":
            print("Registration failed: Email already exists")

        elif ans == "<SUCCESS>":
            print("Registration successful")
            # will set the identifier folder's name to the username
            return u_username
        else:
            print(f"Unexpected response from registration: {ans}")

    except Exception as e:
        print(f"Unexpected error during registration: {e}")
        client_socket.send("Unexpected error during registration".encode())


if __name__ == "__main__":
    when_try_register()
    reg_ans = client_socket.recv(1024).decode()
    if reg_ans == "<EXISTS>":
        print("Registration failed: Email already exists")
        when_try_register()
    elif reg_ans == "<SUCCESS>":
        print("Registration successful")
    else:
        print(f"Unexpected response from registration")
