import pickle
import socket
import os
import threading
import tqdm
from database.Authentication import UserAuthentication
from database.UserFiles import UserFiles
from datetime import datetime
import sqlite3

database_path = 'database/User_info.db'
conn = sqlite3.connect(database_path)
cur = conn.cursor()

# Assuming the 'FileBytes' column in 'UserFiles' table contains pickled data
command = '''
    SELECT FileBytes FROM UserFiles WHERE UserID = 1 AND Name = 'chord.docx';
'''

result = cur.execute(command).fetchone()

if result:
    print(result)
    # Assuming 'a[0]' contains the pickled data
    pickled_data = result[0]

    with open('chord.docx', 'wb') as file:
        file.write(pickle.loads(pickled_data))

# Commit and close the connection
conn.commit()
conn.close()
