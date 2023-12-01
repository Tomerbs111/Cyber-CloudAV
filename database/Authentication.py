import sqlite3
import hashlib


class UserAuthentication:
    def __init__(self, database_path='database/User_info.db'):
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()

    def _hash_input(self, input):
        h = hashlib.sha256()
        h.update(input.encode())
        return h.hexdigest()

    def _email_exists(self, email):
        query = "SELECT * FROM Authenticated WHERE LOWER(email)=?"
        result = self.cur.execute(query, [email.lower()]).fetchone()
        return result is not None

    def login(self, email, password):
        get_from_query = self.cur.execute("SELECT * FROM Authenticated WHERE LOWER(email)=?", [email.lower()]).fetchone()
        ans = ""
        if get_from_query is not None:
            hashed_password = self._hash_input(password)
            if hashed_password == get_from_query[3]:
                print("Login succeed")
                return get_from_query[2]  # returns username
            else:
                return "<WRONG_PASSWORD>"
        else:
            return "<WRONG_EMAIL>"

    def register(self, email, username, password):
        email = email.lower()  # Convert email to lowercase
        if self._email_exists(email):
            print("Email already exists in the database.")
            return "<EXISTS>"

        hashed_password = self._hash_input(password)
        insert_query = '''
        INSERT INTO Authenticated (email, username, password)
        VALUES (?, ?, ?);
        '''

        self.cur.execute(insert_query, (email, username, hashed_password))
        self.conn.commit()

        print("Login information inserted into the database.")
        return "<SUCCESS>"

    def close_db(self):
        self.conn.close()

# Example usage:
# auth = UserAuthentication()
# print(auth.email_exists("test@example.com"))
# auth.close_db()
