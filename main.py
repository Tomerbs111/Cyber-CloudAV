import pickle
import socket
import os
import threading
from typing import Any

from database.Authentication import UserAuthentication
from database.UserFiles import UserFiles
from datetime import datetime


def send_saved_files_details(identifier: str):
    user_files_manager = UserFiles(f'u_{identifier}')
    file_details_dict = {}
    file_counter = 1

    try:
        while True:
            f_details = user_files_manager.get_all_data(file_counter)
            if f_details == "<DONE>":
                break
            else:
                file_name = f_details["file_name"]
                file_size = f_details["file_size"]
                file_date = f_details["file_date"]

                file_details_dict[file_name] = [file_size, file_date]
                file_counter += 1

        # Sending the file details over the socket
        return file_details_dict
    except Exception as e:
        print(f"Error in send_saved_files_details: {e}")

# ...

if __name__ == "__main__":
    print(send_saved_files_details("1"))


def recive_saved_file_details(serv_ans):
    ans_dict = serv_ans
    for key in ans_dict:
        add_file_frame(key,format_file_size(ans_dict[0]), ans_dict[1])