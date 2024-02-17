import socket
import threading


class GroupUser:
    def __init__(self, user_socket: socket, user_email: str, group_name: str):
        """
        Initialize the GroupUser object.
        every group user has its own socket, user unique email, and if the user created the group he will be the admin

        :param user_socket: the socket of the user. allows communication with the server.
        :param user_email: the user unique email.
        # :param user_role: the role of the user. can be an admin with special permissions or just a normal user.
        :param group_name: the name of the group.
        """
        self.user_socket = user_socket
        self.user_email = user_email
        self.group_name = group_name
