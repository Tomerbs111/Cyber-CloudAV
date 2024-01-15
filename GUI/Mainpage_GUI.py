import pickle
import random
from typing import Any
from tkinter import filedialog as fd
from datetime import datetime
import os
import socket

import customtkinter
from customtkinter import *


class FileFrame(CTkFrame):
    def __init__(self, fname, fsize, fdate, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        self.id_of_frame = random.randint(1, 100)
        self.fname = fname
        self.fsize = fsize
        self.fdate = fdate

        lu_filename = CTkLabel(
            master=self,
            text=self.fname
        )
        lu_filename.pack(side='left', padx=30)

        lu_size = CTkLabel(
            master=self,
            text=self.fsize
        )
        lu_size.pack(side='right', padx=27)

        lu_date_mod = CTkLabel(
            master=self,
            text=self.fdate
        )
        lu_date_mod.pack(side='right', padx=43)

        self.check_var = customtkinter.StringVar(value="off")
        self.mark_for_action = customtkinter.CTkCheckBox(self, text="",
                                                         variable=self.check_var, onvalue="on", offvalue="off")
        self.mark_for_action.pack(side='left')

    def get_checkvar(self) -> bool:
        return self.check_var.get() == "on"

    def get_filename(self):
        return self.fname

    def uncheck(self):
        self.check_var.set("off")


class MainPage(CTk):
    def __init__(self, client_socket: socket):
        super().__init__()
        self.geometry("800x600")
        self.client_socket = client_socket

        # Initialize instance variables
        self.f_data_center = None
        self.f_file_tags = None
        self.f_file_list = None
        self.file_frames = []  # List to store FileFrame instances
        self.file_frame_counter = 0
        self.save_path = None

        # Call the setup functions
        self.setup_action_frame()
        self.setup_data_center_frame()
        self.setup_option_frame()
        self.setup_file_tags_frame()
        self.setup_file_list_frame()

    def setup_action_frame(self):
        # Code for setting up the Action frame
        f_actions = CTkFrame(master=self)
        f_actions.place(x=0, y=0, relheight=0.1, relwidth=1)
        l1 = CTkLabel(master=f_actions, bg_color='red', text="f_actions").pack(expand=True, fill='both')

    def setup_data_center_frame(self):
        # Code for setting up the Data center frame
        self.f_data_center = CTkFrame(master=self)
        self.f_data_center.place(rely=0.1, x=0, relheight=0.9, relwidth=1)

    def setup_option_frame(self):
        # Code for setting up the Option frame
        f_options = CTkFrame(master=self.f_data_center, fg_color="transparent")
        f_options.place(x=0, y=0, relwidth=0.2, relheight=1)
        l2 = CTkLabel(master=f_options, bg_color='blue', text="f_options").pack(expand=True, fill='both')

    def setup_file_tags_frame(self):
        # Code for setting up the File tags frame
        self.f_file_tags = CTkFrame(master=self.f_data_center)
        self.f_file_tags.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.06)

    def setup_file_list_frame(self):
        # Code for setting up the File list frame
        self.f_file_list = CTkScrollableFrame(master=self.f_data_center, orientation="vertical")
        self.f_file_list.place(relx=0.2, rely=0.05, relwidth=0.8, relheight=0.95)
        l_name = CTkLabel(master=self.f_file_tags, text="Name").pack(side='left', padx=30)
        l_size = CTkLabel(master=self.f_file_tags, text="Size").pack(side='right', padx=50)
        l_modate = CTkLabel(master=self.f_file_tags, text="Upload date").pack(side='right', padx=25)

        add_file_btn = (CTkButton(master=self.f_file_list, text="add file", command=self.add_file)
                        .pack(expand=True, fill='x'))

        process_checked_file_frames = (CTkButton(master=self.f_file_list, text="get results",
                                                 command=self.get_save_path_dialog).pack(expand=True, fill='x'))

    @staticmethod
    def format_file_size(file_size_bytes):
        if file_size_bytes < 1024:
            return f"{file_size_bytes} bytes"
        elif file_size_bytes < 1024 ** 2:
            return f"{file_size_bytes / 1024:.2f} KB"
        elif file_size_bytes < 1024 ** 3:
            return f"{file_size_bytes / (1024 ** 2):.2f} MB"
        else:
            return f"{file_size_bytes / (1024 ** 3):.2f} GB"

    def add_file(self):
        if self.save_path is None:
            self.get_save_path_dialog()
        else:
            self.client_socket.send("S".encode())
            try:
                filetypes = (
                    ('text files', '*.txt'),
                    ('All files', '*.*')
                )

                file_name = fd.askopenfilename(
                    title='Select a file',
                    initialdir='/',
                    filetypes=filetypes)

                # getting all the file properties needed for the server to handle
                file_bytes = os.path.getsize(file_name)
                short_filename = os.path.basename(file_name)
                file_date = datetime.now()

                file_size = self.format_file_size(file_bytes)
                short_file_date = file_date.strftime("%m/%d/%Y")
                self.client_socket.send(pickle.dumps([short_filename, file_bytes, file_date]))
                serv_ans = self.client_socket.recv(72).decode()

                # the file will start to send after the OK flag has been raised
                if serv_ans == "<GOT_PROP>":
                    with open(file_name, 'rb') as file:
                        while True:
                            data = file.read()
                            if not data:
                                break
                            self.client_socket.send(data)

                        # Signal the end of data
                        self.client_socket.send(b"<END_OF_DATA>")
                        print(f"File '{file_name}' sent successfully")

                    # adding the file to the gui
                    self.add_file_frame(short_filename, file_size, short_file_date)

            except FileNotFoundError:  # in cases of an error
                return

    def add_file_frame(self, file_name="hello.exe", file_size="100GB", file_date="10/1/12"):
        file_frame = FileFrame(file_name, file_size, file_date, master=self.f_file_list)
        file_frame.pack(expand=True, fill='x', side='top')
        self.file_frames.append(file_frame)  # Add FileFrame instance to the list
        self.file_frame_counter += 1

    def checked_file_frames(self):
        checked_file_frames_list = []
        for file_frame in self.file_frames:
            if file_frame.get_checkvar():
                checked_file_frames_list.append(file_frame.get_filename())
                file_frame.uncheck()  # Uncheck the checkbox

        return checked_file_frames_list

    def receive_checked_files(self):
        if self.save_path is None:
            self.get_save_path_dialog()
        else:
            lst_of_fnames = self.checked_file_frames()
            for file_name in lst_of_fnames:
                self.client_socket.send("R".encode())
                file_name = lst_of_fnames[file_name]

                # sending the requested file name to the server
                self.client_socket.send(file_name.encode())

                with open(os.path.join(self.save_path, file_name), 'wb') as file:
                    done_sending = False
                    received_data = b""
                    while not done_sending:
                        data = self.client_socket.recv(1024)
                        if data[-len(b"<END_OF_DATA>"):] == b"<END_OF_DATA>":
                            done_sending = True
                            file.write(data[:-len(b"<END_OF_DATA>")])
                        else:
                            file.write(data)

                print(f"File '{file_name}' received successfully.")

    def get_save_path_dialog(self):
        dialog = customtkinter.CTkInputDialog(text="Write the path you want to save your files on:", title="Get save "
                                                                                                           "path")
        self.save_path = dialog.get_input()


if __name__ == "__main__":
    app = MainPage("1")
    app.mainloop()
