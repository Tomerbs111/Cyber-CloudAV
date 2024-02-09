import socket
import threading


class GroupUser:
    """
    Represents a user in a group with information about their socket and user ID.

    Attributes:
        _guser_socket_id (str): The socket ID of the user.
        _guser_id (int): The user ID in the database.
    """

    def __init__(self, guser_socket_id, guser_id):
        """
        Class constructor that initializes two instance variables: _guser_socket_id and _guser_id.

        :param guser_socket_id: The socket ID of the user.
        :param guser_id: The user ID in the database.
        """
        self._guser_socket_id = guser_socket_id
        self._guser_id = guser_id

    @property
    def g_user_socket_id(self):
        """Getter for g_user_socket_id."""
        return self._guser_socket_id

    @g_user_socket_id.setter
    def g_user_socket_id(self, value):
        """Setter for g_user_socket_id."""
        self._guser_socket_id = value

    @g_user_socket_id.deleter
    def g_user_socket_id(self):
        """Deleter for g_user_socket_id."""
        del self._guser_socket_id

    @property
    def user_id(self):
        """Getter for user_id."""
        return self._guser_id
