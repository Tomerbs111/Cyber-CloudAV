from datetime import datetime
import sqlite3


class UserFiles:
    CREATE_TABLE_QUERY_FILES = '''
        CREATE TABLE IF NOT EXISTS Files (
            id INTEGER PRIMARY KEY,
            Owner TEXT NOT NULL,
            Name TEXT NOT NULL,
            Size INTEGER NOT NULL,
            Date TEXT NOT NULL,
            Favorite INTEGER DEFAULT 0,
            FileBytes BLOB
        );
    '''

    INSERT_FILE_QUERY = '''
        INSERT INTO Files (Owner, Name, Size, Date, FileBytes)
        VALUES (?, ?, ?, ?, ?);
    '''

    REMOVE_FILE_QUERY = '''
        DELETE FROM Files WHERE Owner = ? AND Name = ?;
    '''

    GET_FILE_DATA_QUERY = '''
        SELECT FileBytes FROM Files WHERE Owner = ? AND Name = ?;
    '''

    GET_FILE_SIZE_QUERY = '''
        SELECT Size FROM Files WHERE Owner = ? AND Name = ?;
    '''

    GET_ALL_DATA_QUERY = '''
        SELECT Name, Size, Date, Favorite FROM Files WHERE Owner = ?;
    '''

    RENAME_FILE_QUERY = '''
        UPDATE Files SET Name = ? WHERE Owner = ? AND Name = ?;
    '''

    GET_FAVORITE_STATUS_QUERY = '''
        SELECT Favorite FROM Files WHERE Owner = ? AND Name = ?;
    '''

    SET_FAVORITE_STATUS_QUERY = '''
        UPDATE Files SET Favorite = ? WHERE Owner = ? AND Name = ?;
    '''

    def __init__(self, userid: str, database_path='../database/User_info.db'):
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()
        self.userid_db = userid
        self.cur.execute(self.CREATE_TABLE_QUERY_FILES)
        self.conn.commit()

    def _execute_query(self, query, params=None):
        if params:
            return self.cur.execute(query, params).fetchall()
        else:
            return self.cur.execute(query).fetchall()

    def insert_file(self, name: str, size: int, date: datetime, filebytes: bytes):
        self._execute_query(self.INSERT_FILE_QUERY, (self.userid_db, name, size, date, filebytes))
        self.conn.commit()

    def delete_file(self, name: str):
        self._execute_query(self.REMOVE_FILE_QUERY, (self.userid_db, name))
        self.conn.commit()

    def rename_file(self, old_name: str, new_name: str):
        self._execute_query(self.RENAME_FILE_QUERY, (new_name, self.userid_db, old_name))
        self.conn.commit()

    def get_file_data(self, file_name: str) -> bytes:
        data = self._execute_query(self.GET_FILE_DATA_QUERY, (self.userid_db, file_name))
        return data[0] if data else None

    def get_file_size(self, file_name: str) -> int:
        size = self._execute_query(self.GET_FILE_SIZE_QUERY, (self.userid_db, file_name))
        return size[0] if size else None

    def get_all_data(self):
        all_details = self._execute_query(self.GET_ALL_DATA_QUERY, (self.userid_db,))
        return all_details if all_details is not None else "<NO_DATA>"

    def get_favorite_status(self, file_name: str) -> int:
        status = self._execute_query(self.GET_FAVORITE_STATUS_QUERY, (self.userid_db, file_name))
        return status[0] if status else None

    def set_favorite_status(self, file_name: str, favorite: int):
        self._execute_query(self.SET_FAVORITE_STATUS_QUERY, (favorite, self.userid_db, file_name))
        self.conn.commit()

    def set_unfavorite_status(self, file_name: str):
        self.set_favorite_status(file_name, 0)

    def close_connection(self):
        self.conn.close()
