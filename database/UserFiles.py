from datetime import datetime
from typing import Any

import sqlite3

class UserFiles:
    CREATE_TABLE_QUERY_FILES = '''
        CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Size INTEGER NOT NULL,
            Date TEXT NOT NULL,
            FileBytes BLOB  
        );
    '''

    INSERT_FILE_QUERY = '''
        INSERT INTO {} (Name, Size, Date, FileBytes)
        VALUES (?, ?, ?, ?);
    '''

    REMOVE_FILE_QUERY = '''
        DELETE FROM {} WHERE Name = ?;
    '''

    GET_FILE_DATA_QUERY = '''
        SELECT FileBytes FROM {} WHERE Name = ?;
    '''

    GET_FILE_SIZE_QUERY = '''
        SELECT Size FROM {} WHERE Name = ?;
    '''

    GET_ALL_DATA_QUERY = '''
        SELECT Name, Size, Date FROM {};
    '''

    def __init__(self, userid: str, database_path='../database/User_info.db'):
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()
        self.userid_db = userid
        self.cur.execute(self.CREATE_TABLE_QUERY_FILES.format(self.userid_db))
        self.conn.commit()

    def _execute_query(self, query, params=None):
        if params:
            return self.cur.execute(query.format(self.userid_db), params).fetchone()
        else:
            return self.cur.execute(query.format(self.userid_db)).fetchall()

    def insert_file(self, name: str, size: int, date: datetime, filebytes: bytes):
        self._execute_query(self.INSERT_FILE_QUERY, (name, size, date, filebytes))
        self.conn.commit()

    def remove_file(self, name: str):
        self._execute_query(self.REMOVE_FILE_QUERY, (name,))
        self.conn.commit()

    def get_file_data(self, file_name: str) -> bytes:
        data = self._execute_query(self.GET_FILE_DATA_QUERY, (file_name,))
        return data[0] if data else None

    def get_file_size(self, file_name: str) -> int:
        size = self._execute_query(self.GET_FILE_SIZE_QUERY, (file_name,))
        return size[0] if size else None

    def get_all_data(self):
        all_details = self._execute_query(self.GET_ALL_DATA_QUERY)
        return all_details if all_details is not None else "<DONE>"

    def close_connection(self):
        self.conn.close()
