import threading

from server.GroupUser import GroupUser


class GroupRoom:

    def __init__(self, room_name: str, room_id: int, user_list: dict, room_admin: GroupUser, users_permissions: dict):
        """
        GroupRoom class constructor.
        GroupRoom handles all the actions of the group users in the room.

        :param room_name (str): The name of the room.
        :param room_id (int): The ID of the room.
        :param user_list (dict): A dictionary containing the users in the room, key is the user's username,
                                                            value is the current active socket of the user.
        :param room_admin (GroupUser): The creator of the room, has special abilities.
        :param users_permissions (dict): a dictionary containing the permissions of each user set by the admin.
        """

        self._room_name = room_name
        self.room_id = room_id
        self.user_list = user_list
        self.room_admin = room_admin
        self.users_permissions = users_permissions

    @property
    def room_name(self):
        return self._room_name

    @room_name.setter
    def room_name(self, value):
        self._room_name = value

    @property
    def room_admin(self):
        return self._room_admin

    @room_admin.setter
    def room_admin(self, value):
        self._room_admin = value
