import sqlite3


class UserFiles:
    def __init__(self, userid, database_path='../database/User_info.db'):
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()
        self.userid = userid

    def InsertFile(self, name, size, date, filebytes):
        insert_file = '''
        INSERT INTO UserFiles (UserID, Name, Size, Date, FileBytes)
        VALUES (?, ?, ?, ?, ?);
        '''
        self.cur.execute(insert_file, (self.userid, name, size, date, filebytes))
        self.conn.commit()  # Don't forget to commit the changes

    def RemoveFile(self, name):
        remove_file = '''
        DELETE FROM UserFiles WHERE UserID = ? AND Name = ?;
        '''
        self.cur.execute(remove_file, (self.userid, name,))
        self.conn.commit()  # Don't forget to commit the changes

    # You might want to add a method to close the connection when you're done

    def get_file_data(self, file_name):
        get_data = self.cur.execute('''SELECT FileBytes FROM UserFiles WHERE UserID = ? AND Name = ?; ''',
                                    [self.userid, file_name]).fetchone()
        return get_data

    def get_file_size(self, file_name):
        get_size = self.cur.execute('''SELECT Size FROM UserFiles WHERE UserID = ? AND Name = ?; ''',
                                    [self.userid, file_name]).fetchone()
        return get_size

    def close_connection(self):
        self.conn.close()
