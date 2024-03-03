from datetime import datetime
import sqlite3


class RoomManager:
    CREATE_TABLE_QUERY_ROOMS = '''
    CREATE TABLE IF NOT EXISTS Rooms (
        id INTEGER PRIMARY KEY,
        Admin TEXT NOT NULL,
        Name TEXT NOT NULL,
        Participants TEXT NOT NULL
    )'''

    INSERT_ROOM_QUERY = '''
        INSERT INTO Rooms (Admin, Name, Participants)
        VALUES (?, ?, ?);
    '''

    REMOVE_ROOM_QUERY = '''
        DELETE FROM Rooms WHERE Name = ?;
    '''

    GET_ROOM_PARTICIPANTS_QUERY = '''
        SELECT Participants FROM Rooms WHERE Name = ?;
    '''

    SET_ROOM_PARTICIPANTS_QUERY = '''
        UPDATE Rooms SET Participants = ? WHERE Name = ?;
    '''

    GET_ROOMS_BY_PARTICIPANT_QUERY = '''
            SELECT Name FROM Rooms WHERE Participants LIKE ?;
        '''

    def __init__(self, database_path='../database/User_info.db'):
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()
        self.cur.execute(self.CREATE_TABLE_QUERY_ROOMS)
        self.conn.commit()

    def _execute_query(self, query, params=None):
        if params:
            return self.cur.execute(query, params).fetchall()
        else:
            return self.cur.execute(query).fetchall()

    def insert_room(self, name: str, participants: str, admin: str):
        self._execute_query(self.INSERT_ROOM_QUERY, (admin, name, participants))
        self.conn.commit()

    def remove_room(self, name: str):
        self._execute_query(self.REMOVE_ROOM_QUERY, (name,))
        self.conn.commit()

    def get_room_participants(self, name: str):
        return self._execute_query(self.GET_ROOM_PARTICIPANTS_QUERY, (name,))

    def set_room_participants(self, room_name, new_participant):
        try:
            # Fetch the current list of participants
            current_participants = self.get_room_participants(room_name)

            # Append the new participant to the list
            updated_participants = current_participants + [new_participant]

            # Update the participants list in the database
            self._execute_query(self.SET_ROOM_PARTICIPANTS_QUERY, (",".join(updated_participants), room_name))
            self.conn.commit()

            print(f"Participants list updated for room '{room_name}'.")

        except Exception as e:
            print(f"Error in set_room_participants: {e}")

    def get_rooms_by_participant(self, user_email):
        query_param = f'%{user_email}%'
        result = self._execute_query(self.GET_ROOMS_BY_PARTICIPANT_QUERY, (query_param,))
        return [row[0] for row in result]
