from datetime import datetime
from typing import Any

import sqlite3


class UserFiles:
    def __init__(self, userid: str, database_path='../database/User_info.db'):
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()
        self.userid_db = userid
        create_table_query_files = f'''
            CREATE TABLE IF NOT EXISTS {self.userid_db} (
                id INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Size INTEGER NOT NULL,
                Date TEXT NOT NULL,
                FileBytes BLOB  
            );
            '''
        self.cur.execute(create_table_query_files)
        self.conn.commit()

    def InsertFile(self, name: str, size: int, date: datetime, filebytes: bytes):
        insert_file = f'''
        INSERT INTO {self.userid_db} (Name, Size, Date, FileBytes)
        VALUES (?, ?, ?, ?);
        '''
        self.cur.execute(insert_file, (name, size, date, filebytes))
        self.conn.commit()  # Don't forget to commit the changes

    def RemoveFile(self, name: str):
        remove_file = f'''
        DELETE FROM {self.userid_db} WHERE Name = ?;
        '''
        self.cur.execute(remove_file, (name,))
        self.conn.commit()  # Don't forget to commit the changes

    # You might want to add a method to close the connection when you're done

    def get_file_data(self, file_name: str) -> bytes:
        get_data_query = f'''SELECT FileBytes FROM {self.userid_db} WHERE Name = ?;'''
        data = self.cur.execute(get_data_query, (file_name,)).fetchone()

        return data[0] if data else None

    def get_file_size(self, file_name: str) -> int:
        get_size_query = f'''SELECT Size FROM {self.userid_db} WHERE Name = ?;'''
        size = self.cur.execute(get_size_query, (file_name,)).fetchone()

        return size[0] if size else None

    def get_all_data(self, given_id: int):
        get_size_query = f'''SELECT Name, Size, Date FROM {self.userid_db} WHERE id = ?;'''
        all_details = self.cur.execute(get_size_query, (given_id,)).fetchone()

        if all_details is not None:
            file_name = all_details[0]
            file_size = all_details[1]
            file_date = all_details[2]
            return {"file_name": file_name, "file_size": file_size, "file_date": file_date}
        else:
            return "<DONE>"

    def close_connection(self):
        self.conn.close()
