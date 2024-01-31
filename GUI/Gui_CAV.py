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

import customtkinter
from customtkinter import *
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from customtkinter import CTkInputDialog

import re

import ttkbootstrap as ttk
from customtkinter import *
from PIL import Image, ImageTk


class RegistrationApp(ttk.Frame):
    def __init__(self, parent, switch_callback, client_communicator):
        super().__init__(parent)
        self.parent_app = parent
        self.switch_callback = switch_callback
        self.client_communicator = client_communicator

        self.register_frame = ttk.Frame(master=self)

        # Frame for fields (left side)
        self.login_frame = ttk.Frame(master=self)
        self.login_frame.place(x=0, y=0, relwidth=0.45, relheight=1)

        # Frame for animation (right side)
        self.animation_frame = ttk.Frame(master=self)
        self.animation_frame.place(relx=0.45, y=0, relwidth=0.55, relheight=1)

        # Instance variables for all answers
        self.ans_password = None
        self.ans_email = None
        self.ans_username = None
        self.l_confirm = None

        # Instance variables for user input
        self.email_entry = None
        self.username_entry = None
        self.password_entry = None
        self.switch_btn = None
        self.submit_btn = None

        # Instance variables for socket communication
        self.auth_completed = False
        self.server_ans = None
        self.attempt_type = "<LOGIN>"

        # Initialize UI components
        self.setup_logo(self.login_frame, posx=0.01, posy=0.04)
        self.setup_welcome(self.login_frame, "Login", posx=0.15, posy=0.05)
        self.setup_switch_button(self.login_frame, "sign up", posx=0.02, posy=0.15,
                                 switch_command=self.switch_to_registration,
                                 text_before_btn_text="Doesn't have an account? Click here to ")

        self.setup_email(self.login_frame, posx=0.02, posy=0.2)
        self.setup_password(self.login_frame, posx=0.02, posy=0.35)
        self.setup_submit_button(self.login_frame, "Sign in", posx=0.02, posy=0.55,
                                 submit_command=self.l_when_submit)
        self.setup_confirmation_label(self.login_frame, posy=0.8)

        # Placeholder for animation (you can replace this with your animation logic)
        ttk.Label(self.animation_frame, text="Animation Placeholder", background="red").pack(fill="both", expand=True)

    def switch_to_registration(self):
        self.register_frame = ttk.Frame(master=self)
        self.setup_logo(self.register_frame, posx=0.01, posy=0.04)
        self.setup_welcome(self.register_frame, "Register", posx=0.15, posy=0.05)
        self.setup_switch_button(self.register_frame, "sign in", posx=0.02, posy=0.15,
                                 switch_command=self.switch_to_login,
                                 text_before_btn_text="Already have an account? Click here to ")

        self.setup_email(self.register_frame, posx=0.02, posy=0.2)
        self.setup_username(self.register_frame, posx=0.02, posy=0.35)
        self.setup_password(self.register_frame, posx=0.02, posy=0.50)
        self.setup_submit_button(self.register_frame, "Sign up", posx=0.02, posy=0.70,
                                 submit_command=self.r_when_submit)
        self.setup_confirmation_label(self.register_frame, posy=0.8)

        self.login_frame.destroy()
        self.register_frame.place(x=0, y=0, relwidth=0.45, relheight=1)
        self.attempt_type = "<REGISTER>"

    def switch_to_login(self):
        self.login_frame = ttk.Frame(master=self)
        self.setup_logo(self.login_frame, posx=0.01, posy=0.04)
        self.setup_welcome(self.login_frame, "Login", posx=0.15, posy=0.05)
        self.setup_switch_button(self.login_frame, "sign up", posx=0.02, posy=0.15,
                                 switch_command=self.switch_to_registration,
                                 text_before_btn_text="Doesn't have an account? Click here to ")

        self.setup_email(self.login_frame, posx=0.02, posy=0.2)
        self.setup_password(self.login_frame, posx=0.02, posy=0.35)
        self.setup_submit_button(self.login_frame, "Sign in", posx=0.02, posy=0.55,
                                 submit_command=self.l_when_submit)
        self.setup_confirmation_label(self.login_frame, posy=0.8)

        self.register_frame.destroy()
        self.login_frame.place(x=0, y=0, relwidth=0.45, relheight=1)
        self.attempt_type = "<LOGIN>"

    @staticmethod
    def setup_logo(master, posx, posy):
        cloudav_image = CTkImage(
            light_image=Image.open(
                r"../GUI/only_logo.png"),
            dark_image=Image.open(
                r"../GUI/only_logo.png"),
            size=(75, 75))

        cav_image_lbl = CTkLabel(master=master, image=cloudav_image, text="")
        cav_image_lbl.place(relx=posx, rely=posy)

    @staticmethod
    def setup_welcome(master, welcome_msg, posx, posy):
        welcome = ttk.Label(
            master=master,
            text=welcome_msg,
            font=("Calibri bold", 35)
        )
        welcome.place(relx=posx, rely=posy)

    def setup_email(self, master, posx, posy):
        label_height = 0.05
        entry_height = 0.05
        label_width = entry_width = 0.85  # Adjust as needed

        l_email = ttk.Label(
            master=master,
            text="Email",
            font=("Calibri", 15),
            bootstyle="info"

        )
        l_email.place(relx=posx, rely=posy, relwidth=label_width, relheight=label_height)

        self.email_entry = ttk.Entry(
            master=master,
            width=60,  # Set the width based on the desired entry width
            bootstyle="info"

        )
        self.email_entry.place(relx=posx, rely=posy + label_height, relwidth=entry_width, relheight=entry_height)
        self.email_entry.insert(0, "tomerbs1810@gmail.com")
        self.ans_email = ttk.Label(
            master=master,
            text=""
        )
        self.ans_email.place(relx=posx, rely=posy + 0.01 + label_height + entry_height)

    # Similar adjustments for setup_username and setup_password methods

    def setup_username(self, master, posx, posy):
        label_height = 0.05
        entry_height = 0.05
        label_width = entry_width = 0.85  # Adjust as needed

        l_username = ttk.Label(
            master=master,
            text="Username",
            font=("Calibri", 15),
            bootstyle="info"
        )
        l_username.place(relx=posx, rely=posy, relwidth=label_width, relheight=label_height)

        self.username_entry = ttk.Entry(
            master=master,
            width=60,  # Set the width based on the desired entry width
            bootstyle="info"
        )
        self.username_entry.place(relx=posx, rely=posy + label_height, relwidth=entry_width, relheight=entry_height)
        self.ans_username = ttk.Label(
            master=master,
            text=""
        )
        self.ans_username.place(relx=posx, rely=posy + 0.01 + label_height + entry_height)

    def setup_password(self, master, posx, posy):
        label_height = 0.05
        entry_height = 0.05
        label_width = entry_width = 0.85  # Adjust as needed

        l_password = ttk.Label(
            master=master,
            text="Password",
            font=("Calibri", 15),
            bootstyle="info"

        )
        l_password.place(relx=posx, rely=posy, relwidth=label_width, relheight=label_height)

        self.password_entry = ttk.Entry(
            master=master,
            width=60,  # Set the width based on the desired entry width
            bootstyle="info"

        )
        self.password_entry.place(relx=posx, rely=posy + label_height, relwidth=entry_width, relheight=entry_height)
        self.password_entry.insert(0, "01102006t")
        self.ans_password = ttk.Label(
            master=master,
            text="",
        )
        self.ans_password.place(relx=posx, rely=posy + 0.01 + label_height + entry_height)

    def setup_confirmation_label(self, master, posy):
        self.l_confirm = ttk.Label(
            master=master,
            text="",
            font=("Calibri bold", 20),
        )
        self.l_confirm.place(relx=0.02, rely=posy)

    def setup_submit_button(self, master, submit_title, posx, posy, submit_command):
        button_height = 0.05
        button_width = 0.85  # Adjust as needed

        self.submit_btn = ttk.Button(
            master=master,
            text=submit_title,
            command=submit_command,
            bootstyle="info"
        )
        self.submit_btn.place(relx=posx, rely=posy, relwidth=button_width, relheight=button_height)

    # Modify the switch button setup method in your RegistrationApp class

    def setup_switch_button(self, master, switch_msg, posx, posy, switch_command, text_before_btn_text):
        text_before_btn = ttk.Label(
            master=master,
            text=text_before_btn_text,
            font=("Calibri bold", 12),
        )
        text_before_btn.place(relx=posx, rely=posy)

        self.switch_btn = ttk.Label(
            master=master,
            text=switch_msg,
            cursor="hand2",
            style="info",
            font=("Calibri bold", 12)
        )
        self.switch_btn.place(relx=posx + 0.52, rely=posy)
        self.switch_btn.bind("<Button-1>", lambda event: switch_command())

    def r_when_submit(self):
        checksum = 0

        u_email = self.email_entry.get()
        if len(u_email) > 0 and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', u_email):
            self.ans_email.configure(text="Email is valid.", bootstyle="success")
            checksum += 1
        else:
            self.ans_email.configure(text="Invalid email. Please enter a valid email.", bootstyle="danger")
            checksum -= 1 if checksum != 0 else 0

        u_username = self.username_entry.get()
        if len(u_username) >= 6:
            self.ans_username.configure(text="Username is valid", bootstyle="success")
            checksum += 1
        else:
            self.ans_username.configure(text="Invalid username. must be 6 characters or longer.",
                                        bootstyle="danger")
            checksum -= 1 if checksum != 0 else 0

        u_password = self.password_entry.get()
        if len(u_password) > 0 and len(u_password) >= 8:
            self.ans_password.configure(text="Password is valid", bootstyle="success")
            checksum += 1
        else:
            self.ans_password.configure(text="Invalid password. must be 8 characters or longer.",
                                        bootstyle="danger")
            checksum -= 1 if checksum != 0 else 0

        if checksum == 3:
            self.client_communicator.r_when_submit(self.attempt_type, u_email, u_username, u_password)

            if self.server_ans == "<EXISTS>":
                self.ans_email.configure(text="Registration failed. Email is already in use.", bootstyle="danger")
                self.ans_username.configure(text="Registration failed.", bootstyle="danger")
                self.ans_password.configure(text="Registration failed.", bootstyle="danger")
            elif self.server_ans == "<SUCCESS>":
                self.l_confirm.configure(text="User Registered successfully", bootstyle="success")
                self.after(1000, lambda: self.switch_callback(MainPage, self.client_communicator))

    def l_when_submit(self):
        checksum = 0

        u_email = self.email_entry.get()
        if len(u_email) > 0 and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', u_email):
            self.ans_email.configure(text="Email is valid.", bootstyle="success")
            checksum += 1
        else:
            self.ans_email.configure(text="Invalid email. Please enter a valid email.", bootstyle="danger")
            checksum -= 1 if checksum != 0 else 0

        u_password = self.password_entry.get()
        if len(u_password) >= 8:
            self.ans_password.configure(text="Password is valid", bootstyle="success")
            checksum += 1
        else:
            self.ans_password.configure(text="Invalid password. must be 8 characters or longer.",
                                        bootstyle="danger")
            checksum -= 1 if checksum != 0 else 0

        if checksum == 2:
            self.server_ans = self.client_communicator.l_when_submit(self.attempt_type, u_email, u_password)

            if self.server_ans == "<NO_EMAIL_EXISTS>":
                self.ans_email.configure(text="Login failed. No accounts under the provided email.",
                                         bootstyle="danger")
                self.ans_password.configure(text="Login failed. Password doesn't match the provided email.",
                                            bootstyle="danger")
            elif self.server_ans == "<WRONG_PASSWORD>":
                self.ans_password.configure(text="Login failed. Password doesn't match the provided email.",
                                            bootstyle="danger")
            else:
                self.l_confirm.configure(text=f"Welcome back {self.server_ans}", bootstyle="success")
                self.after(1000, lambda: self.switch_callback(MainPage, self.client_communicator))


class FileFrame(ttk.Frame):
    def __init__(self, master, fname, fsize, fdate):
        super().__init__(master)
        self.fname = fname
        self.fsize = fsize
        self.fdate = fdate

        lu_filename = ttk.Label(
            master=self,
            text=self.fname
        )
        lu_filename.pack(side='left', padx=30)

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

        self.check_var = customtkinter.StringVar(value="off")
        self.mark_for_action = ttk.Checkbutton(self, text="",
                                               variable=self.check_var, onvalue="on", offvalue="off")
        self.mark_for_action.pack(side='left')

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

        narf_thread = threading.Thread(target=self.notify_and_receive_files)
        narf_thread.start()

    def notify_and_receive_files(self):
        for individual_file in self.client_communicator.notify_and_receive_files():
            file_name, file_bytes, file_date = individual_file

            short_filename, formatted_file_size, short_file_date = \
                self.prepare_for_display(file_name, file_bytes, file_date)  # a func from Gui_CAV.py

            self.add_file_frame(short_filename, formatted_file_size, short_file_date)  # a func from Gui_CAV.py

    def on_logout(self):
        self.switch_callback(RegistrationApp)

    def setup_action_frame(self):
        # Code for setting up the Action frame
        f_actions = ttk.Frame(master=self)
        f_actions.place(x=0, y=0, relheight=0.1, relwidth=1)
        ttk.Button(self, text="Logout", command=self.on_logout).pack(expand=True, fill='both')

    def setup_data_center_frame(self):
        # Code for setting up the Data center frame
        self.f_data_center = ttk.Frame(master=self)
        self.f_data_center.place(rely=0.1, x=0, relheight=0.9, relwidth=1)

    def setup_option_frame(self):
        # Code for setting up the Option frame
        f_options = ttk.Frame(master=self.f_data_center)
        f_options.place(x=0, y=0, relwidth=0.2, relheight=1)
        ttk.Label(master=f_options, text="f_options").pack(expand=True, fill='both')

    def setup_file_tags_frame(self):
        # Code for setting up the File tags frame
        self.f_file_tags = ttk.Frame(master=self.f_data_center)
        self.f_file_tags.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.13)

        add_file_btn = (ttk.Button(master=self.f_file_tags, text="add file", command=self.add_file)
                        .pack(fill='x'))

        process_checked_file_frames = (ttk.Button(master=self.f_file_tags, text="get results",
                                                  command=self.receive_checked_files).pack(fill='x'))

    def setup_file_list_frame(self):
        # Code for setting up the File list frame
        self.f_file_list = ScrolledFrame(master=self.f_data_center, autohide=True, bootstyle='solar')
        self.f_file_list.place(relx=0.2, rely=0.13, relwidth=0.8, relheight=0.87)

        ttk.Label(master=self.f_file_tags, text="Name").pack(side='left', padx=30)
        ttk.Label(master=self.f_file_tags, text="Size").pack(side='right', padx=50)
        ttk.Label(master=self.f_file_tags, text="Upload date").pack(side='right', padx=25)

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
                                                          short_file_date,
                                                          file_bytes))
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

        # Check if the file is an image (you can customize the list of image extensions)
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        is_image = any(file_name.lower().endswith(ext) for ext in image_extensions)

        # Check if the file is a document type (you can customize the list of document extensions)
        document_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx']
        is_document = any(file_name.lower().endswith(ext) for ext in document_extensions)

        # Check if the file is a video type (you can customize the list of video extensions)
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov']
        is_video = any(file_name.lower().endswith(ext) for ext in video_extensions)

        if is_image:
            # Path to the image icon for images (replace with your path)
            icon_path = "../GUI/file_icons/image_icon.png"
        elif is_document:
            # Path to the icon for document types (replace with your path)
            icon_path = "../GUI/file_icons/documents_icon.png"
        elif is_video:
            # Path to the icon for video types (replace with your path)
            icon_path = "../GUI/file_icons/video_icon.png"
        else:
            icon_path = None

        if icon_path:
            # Load the icon image
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((20, 20))  # Adjust the size as needed

            # Convert the image to a format compatible with tkinter
            tk_icon_image = ImageTk.PhotoImage(icon_image)

            # Create a label to display the icon
            icon_label = ttk.Label(master=file_frame, image=tk_icon_image)
            icon_label.image = tk_icon_image
            icon_label.pack(side='left', padx=10)  # Adjust the padding as needed

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
        dialog = customtkinter.CTkInputDialog(text="Write the path you want to save your files on:",
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
        self.switch_frame(RegistrationApp, self.client_communicator)

    def switch_frame(self, frame_class, *args):
        new_frame = frame_class(self, self.switch_frame, *args)

        if self.current_frame:
            self.current_frame.pack_forget()

        new_frame.pack(fill="both", expand=True)
        self.current_frame = new_frame


if __name__ == "__main__":
    my_app = MyApp()
    my_app.mainloop()
