# gui.py
import os
import pickle
import random
import re
import threading
import time
from typing import Any
from tkinter import filedialog as fd
from datetime import datetime

from customtkinter import *
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from customtkinter import CTkInputDialog

import re

import ttkbootstrap as ttk
from customtkinter import *
from PIL import Image


class FileFrame(ttk.Frame):
    def __init__(self, master, fname, fsize, fdate):
        super().__init__(master)
        self.fname = fname
        self.fsize = fsize
        self.fdate = fdate

        self.check_var = StringVar(value="off")
        self.mark_for_action = ttk.Checkbutton(self, text="",
                                               variable=self.check_var, onvalue="on", offvalue="off")
        self.mark_for_action.pack(side='left', padx=5)

        lu_filename = ttk.Label(
            master=self,
            text=self.fname
        )
        lu_filename.pack(side='left', padx=5)

        lu_size = ttk.Label(
            master=self,
            text=self.fsize
        )
        lu_size.pack(side='right', padx=27)

        lu_date_mod = ttk.Label(
            master=self,
            text=self.fdate
        )
        lu_date_mod.pack(side='right', padx=43)

    def get_checkvar(self) -> bool:
        return self.check_var.get() == "on"

    def get_filename(self):
        return self.fname

    def uncheck(self):
        self.check_var.set("off")


class MainPage(ttk.Frame):
    def __init__(self, parent, switch_callback, client_communicator):
        super().__init__(parent)
        self.parent_app = parent
        self.switch_callback = switch_callback
        self.client_communicator = client_communicator

        # Initialize instance variables
        self.f_data_center = None
        self.f_action = None
        self.f_file_list = None
        self.file_frames = []  # List to store FileFrame instances
        self.file_frame_counter = 0
        self.save_path = None

        # Call the setup functions
        self.setup_searchbar_frame()
        self.setup_data_center_frame()
        self.setup_option_frame()
        self.setup_action_frame()
        self.setup_file_management_frame()

        narf_thread = threading.Thread(target=self.notify_and_receive_files)
        narf_thread.start()

    def notify_and_receive_files(self):
        for individual_file in self.client_communicator.notify_and_receive_files():
            file_name, file_bytes, file_date = individual_file

            short_filename, formatted_file_size, short_file_date = \
                self.prepare_for_display(file_name, file_bytes, file_date)  # a func from Gui_CAV.py

            self.add_file_frame(short_filename, formatted_file_size, short_file_date)  # a func from Gui_CAV.py

    def setup_searchbar_frame(self):
        # Code for setting up the Action frame
        f_searchbar = ttk.Frame(master=self)
        f_searchbar.place(x=0, y=0, relheight=0.1, relwidth=1)
        ttk.Label(f_searchbar, text="Searchbar Placeholder").pack(fill="both", expand=True)

    def setup_data_center_frame(self):
        # Code for setting up the Data center frame
        self.f_data_center = ttk.Frame(master=self, bootstyle="dark")
        self.f_data_center.place(rely=0.1, x=0, relheight=0.9, relwidth=1)

    def setup_option_frame(self):
        # Code for setting up the Option frame
        f_options = ttk.Frame(master=self)
        f_options.place(relx=0, rely=0.1, relwidth=0.2, relheight=1)
        ttk.Label(f_options, text="Option Placeholder", bootstyle="inverse-dark").pack(fill="both", expand=True)

    def setup_action_frame(self):
        # Code for setting up the File tags frame
        self.f_action = ttk.Frame(master=self.f_data_center)
        self.f_action.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.05)

        ttk.Button(master=self.f_action, text="add file", command=self.add_file).pack(fill='x')

    # ...

    def setup_file_management_frame(self):
        f_file_management = ttk.Frame(master=self.f_data_center)
        f_file_management.place(relx=0.2, rely=0.05, relwidth=0.8, relheight=0.95)

        f_file_properties = ttk.Frame(master=f_file_management)
        f_file_properties.place(relx=0, rely=0, relwidth=1, relheight=0.05)

        CTkButton(master=f_file_properties, text="Name").pack(side='left', padx=5)  # Adjusted padding
        CTkButton(master=f_file_properties, text="Size").pack(side='right', padx=27)  # Adjusted padding
        CTkButton(master=f_file_properties, text="Upload date").pack(side='right', padx=47)  # Adjusted padding

        self.f_file_list = ScrolledFrame(master=f_file_management, autohide=False)
        self.f_file_list.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)

    def setup_file_properties_frame(self):
        f_file_properties = CTkFrame(master=self.f_data_center, corner_radius=10)
        f_file_properties.place(relx=0.2, rely=0.05, relwidth=0.79, relheight=0.05)

        self.f_file_list = CTkScrollableFrame(master=self.f_data_center, corner_radius=10)
        self.f_file_list.place(relx=0.2, rely=0.1, relwidth=0.79, relheight=0.88)

    # client communication parts in GUI
    def add_file(self):
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
            file_date = datetime.now()

            # formatting all the properties
            short_filename, formatted_file_size, short_file_date = \
                self.prepare_for_display(file_name, file_bytes, file_date)

            send_file_thread = threading.Thread(
                target=self.client_communicator.send_file(file_name, short_filename, formatted_file_size,
                                                          short_file_date,file_bytes))
            send_file_thread.start()

            self.add_file_frame(short_filename, formatted_file_size, short_file_date)

        except FileNotFoundError:  # in cases of an error
            return

    def receive_checked_files(self):
        if self.save_path is None:
            self.get_save_path_dialog()
        else:
            select_file_names_lst = self.checked_file_frames()
            self.client_communicator.receive_checked_files(select_file_names_lst, self.save_path)

    def add_file_frame(self, file_name, file_size, file_date):
        file_frame = FileFrame(self.f_file_list, file_name, file_size, file_date)
        file_frame.pack(expand=True, fill='x', side='top')
        self.file_frames.append(file_frame)  # Add FileFrame instance to the list
        self.file_frame_counter += 1

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

    def prepare_for_display(self, file_name, file_bytes, file_uploadate):
        short_filename = os.path.basename(file_name)
        formatted_file_size = self.format_file_size(file_bytes)

        if isinstance(file_uploadate, datetime):
            short_file_date = datetime.strftime(file_uploadate, "%y/%m/%d")

        elif isinstance(file_uploadate, str):
            original_date = datetime.strptime(file_uploadate, "%Y-%m-%d %H:%M:%S.%f")
            short_file_date = original_date.strftime("%y/%m/%d")

        return short_filename, formatted_file_size, short_file_date

    def checked_file_frames(self):
        """
        :return: Returns a list of filenames for the checked file frames.
        """
        checked_file_frames_list = []
        for file_frame in self.file_frames:
            if file_frame.get_checkvar():
                checked_file_frames_list.append(file_frame.get_filename())
                file_frame.uncheck()  # Uncheck the checkbox

        return checked_file_frames_list

    def get_save_path_dialog(self):
        dialog = CTkInputDialog(text="Write the path you want to save your files on:",
                                title="Get save path")
        input_path = dialog.get_input()

        if input_path:
            # Normalize the path to handle potential issues with backslashes
            self.save_path = os.path.normpath(input_path)
        else:
            # Use the default Downloads folder
            self.save_path = os.path.join(os.path.expanduser("~"), "Downloads")


class MyApp(ttk.Window):
    def __init__(self, client_communicator):
        super().__init__(themename="darkly")
        self.geometry("1150x710")
        self.title("Cloud-AV")

        self.client_communicator = client_communicator
        self.current_frame = None
        self.switch_frame(MainPage, self.client_communicator)

    def switch_frame(self, frame_class, *args):
        new_frame = frame_class(self, self.switch_frame, *args)

        if self.current_frame:
            self.current_frame.pack_forget()

        new_frame.pack(fill="both", expand=True)
        self.current_frame = new_frame


if __name__ == "__main__":
    my_app = MyApp("1")
    my_app.mainloop()
