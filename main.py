import pickle
import socket
import os
import threading
from database.Authentication import UserAuthentication
from database.UserFiles import UserFiles
from datetime import datetime
import sqlite3

test = UserFiles(f'u_{1}')

print(test.get_file_data("m ali 2.jpg"))
