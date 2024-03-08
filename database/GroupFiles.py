from datetime import datetime
import sqlite3


class GroupFiles:
    CREATE_TABLE_QUERY_FILES = '''
        CREATE TABLE IF NOT EXISTS GroupsFiles (
            id INTEGER PRIMARY KEY,
            Owner TEXT NOT NULL,
            Name TEXT NOT NULL,
            Size INTEGER NOT NULL,
            Date TEXT NOT NULL,
            GroupName TEXT NOT NULL,
            FileBytes BLOB NOT NULL
        );
    '''

    INSERT_FILE_QUERY = '''
        INSERT INTO GroupsFiles (Owner, Name, Size, Date, GroupName, FileBytes)
        VALUES (?, ?, ?, ?, ?, ?);
    '''

    REMOVE_FILE_QUERY = '''
        DELETE FROM GroupsFiles WHERE GroupName = ? AND Owner = ? AND Name = ?;
    '''

    GET_FILE_DATA_QUERY = '''
        SELECT FileBytes FROM GroupsFiles WHERE GroupName = ? AND Owner = ? AND Name = ?;
    '''

    GET_FILE_INFO_QUERY = '''
        SELECT Owner, Name, Size, Date, GroupName FROM GroupsFiles WHERE GroupName = ? AND Owner = ? AND Name = ?;
    '''

    DELETE_FILE_QUERY = '''
        DELETE FROM GroupsFiles WHERE GroupName = ? AND Owner = ? AND Name = ?;
    '''

    RENAME_FILE_QUERY = '''
        UPDATE GroupsFiles SET Name = ? WHERE GroupName = ? AND Owner = ? AND Name = ?;
    '''

    GET_ALL_FILES_FROM_GROUP_QUERY = '''
        SELECT Owner, Name, Size, Date, GroupName FROM GroupsFiles WHERE GroupName = ?;
    '''

    def __init__(self, userid: str, database_path='../database/User_info.db'):
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()
        self.owner_id = userid
        self.cur.execute(self.CREATE_TABLE_QUERY_FILES)
        self.conn.commit()

    def _execute_query(self, query, params=None):
        if params:
            return self.cur.execute(query, params).fetchall()
        else:
            return self.cur.execute(query).fetchall()

    def insert_file(self, name: str, size: int, date: datetime, group_name: str, filebytes: bytes):
        self._execute_query(self.INSERT_FILE_QUERY, (self.owner_id, name, size, date, group_name, filebytes))
        self.conn.commit()

    def delete_file(self, group_name: str, name: str):
        self._execute_query(self.REMOVE_FILE_QUERY, (group_name, self.owner_id, name))
        self.conn.commit()

    def rename_file(self, group_name: str, old_name: str, new_name: str):
        self._execute_query(self.RENAME_FILE_QUERY, (new_name, group_name, self.owner_id, old_name))
        self.conn.commit()

    def get_file_info(self, group_name: str, name: str):
        return self._execute_query(self.GET_FILE_INFO_QUERY, (group_name, self.owner_id, name))

    def get_file_data(self, group_name: str, name: str):
        result = self._execute_query(self.GET_FILE_DATA_QUERY, (group_name, self.owner_id, name))
        if result:
            # Assuming that result is a list containing a single tuple
            return result[0]
        else:
            # Handle the case where no matching records are found
            return None  # or raise an exception or return a default value

    def get_all_files_from_group(self, group_name: str):
        return self._execute_query(self.GET_ALL_FILES_FROM_GROUP_QUERY, (group_name,))
