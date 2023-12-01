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

        if len(u_email) > 0 and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', u_email):
            # client_socket.send(u_email.encode())
            if client_socket.recv(1024).decode() == "<INVALID>":
                print("email is already registered")
                continue
            print("email Sent")

        else:
            print("Invalid email format. Please enter a valid email.")
            attempts += 1
            continue

        if len(u_username) > 0:
            # client_socket.send(u_username.encode())
            print("username Sent")

        else:
            print("You must provide a username.")
            attempts += 1
            continue

        if len(u_password) > 0 and len(u_password) >= 8:
            # client_socket.send(u_username.encode())
            print("password Sent")

        else:
            print("Invalid password. Password must be 8 characters or longer.")
            attempts += 1
            continue

        print("All data is correct. Registration successful!")
        break

    if attempts == max_attempts:
        print("Maximum number of attempts reached. Registration failed.")


def server_when_register():
    u_email = client_socket.recv(1024).decode()

    if not auth.email_exists(u_email):
        client_socket.send(b'<INVALID>')
    else:
        u_username = client_socket.recv(1024).decode()
        u_password = client_socket.recv(1024).decode()
        auth.register(u_email, u_username, u_password)

    return u_username


if __name__ == "__main__":

