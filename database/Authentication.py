import sqlite3
import hashlib


class UserAuthentication:
    def __init__(self, database_path='database/User_info.db'):
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()

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

    def close_db(self):
        self.conn.close()

    @staticmethod
    def _hash_input(password):
        h = hashlib.sha256()
        h.update(password.encode())
        return h.hexdigest()
