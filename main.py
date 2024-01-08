import pickle
import socket
import os
import threading
from database.Authentication import UserAuthentication
from database.UserFiles import UserFiles
from datetime import datetime
import sqlite3

database_path = 'User_info.db'
conn = sqlite3.connect(database_path)
cur = conn.cursor()

# Assuming the 'FileBytes' column in 'UserFiles' table contains pickled data
get_size = cur.execute('''SELECT FileBytes FROM UserFiles WHERE UserID = ? AND Name = ?; ''',
                       [1, "test.txt"]).fetchone()

print(type(get_size[0]))

# Commit and close the connection
conn.commit()
conn.close()
