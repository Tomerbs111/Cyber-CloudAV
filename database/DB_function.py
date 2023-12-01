import sqlite3

conn = sqlite3.connect('User_info.db')

cursor = conn.cursor()

# query for user login
create_table_query_1 = '''
CREATE TABLE IF NOT EXISTS Authenticated (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
'''

cursor.execute(create_table_query_1)
conn.commit()
conn.close()
