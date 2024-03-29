import sqlite3
import hashlib


class AuthManager:
    def __init__(self, database_path='../database/User_info.db'):
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()
        create_table_query_users = '''
        CREATE TABLE IF NOT EXISTS Authenticated (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
        '''
        self.cur.execute(create_table_query_users)
        self.conn.commit()

    def _email_exists(self, email):
        query = "SELECT * FROM Authenticated WHERE LOWER(email)=?"
        result = self.cur.execute(query, [email]).fetchone()
        return result is not None

    def login(self, email, password):
        get_from_query = self.cur.execute("SELECT * FROM Authenticated WHERE LOWER(email)=?",
                                          [email]).fetchone()
        ans = ""
        if get_from_query is not None:
            hashed_password = self._hash_input(password)
            if hashed_password == get_from_query[3]:
                # Login succeed
                return get_from_query[2]  # returns username
            else:
                return "<WRONG_PASSWORD>"
        else:
            return "<NO_EMAIL_EXISTS>"

    def register(self, email, username, password):
        email = email.lower()  # Convert email to lowercase
        if self._email_exists(email):
            # Email already exists in the database.
            return "<EXISTS>"

        hashed_password = self._hash_input(password)
        insert_query = '''
        INSERT INTO Authenticated (email, username, password)
        VALUES (?, ?, ?);
        '''

        self.cur.execute(insert_query, (email, username, hashed_password))
        self.conn.commit()

        return "<SUCCESS>"

    def get_userid(self, email):
        get_from_query = self.cur.execute("SELECT id FROM Authenticated WHERE LOWER(email)=?",
                                          [email]).fetchone()
        return get_from_query

    def get_username(self, user_id):
        get_from_query = self.cur.execute("SELECT username FROM Authenticated WHERE id = ?",
                                          [user_id]).fetchone()
        return get_from_query[0]

    def get_email(self, user_id):
        get_from_query = self.cur.execute("SELECT email FROM Authenticated WHERE id = ?",
                                          [user_id]).fetchone()
        return get_from_query[0]

    def get_all_users(self, user_id):
        get_from_query = self.cur.execute("SELECT email FROM Authenticated WHERE id != ?", [user_id]).fetchall()
        user_emails = [result[0] for result in get_from_query]  # Assuming each result is a tuple with one element
        return user_emails

    def close_db(self):
        self.conn.close()

    @staticmethod
    def _hash_input(password):
        h = hashlib.sha256()
        h.update(password.encode())
        return h.hexdigest()


if __name__ == '__main__':
    auth = AuthManager()
    print(auth.get_all_users(1))
