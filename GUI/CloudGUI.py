import os
import pickle
import random
import re
import time
from typing import Any
from tkinter import filedialog as fd
from datetime import datetime
import socket
import customtkinter
from customtkinter import *
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame


class RegistrationApp(ttk.Frame):
    def __init__(self, parent, client_socket: socket, switch_callback):
        super().__init__(parent)
        self.parent_app = parent
        self.switch_callback = switch_callback

        self.login_frame = ttk.Frame(master=self)
        self.login_frame.pack(side="top", fill="both", expand=True)

        self.register_frame = ttk.Frame(master=self)

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
        self.server_login_ans = None
        self.server_reg_ans = None
        self.client_socket = client_socket
        self.attempt_type = "<LOGIN>"

        # Initialize UI components
        self.setup_welcome(self.login_frame, "Welcome back to CloudAV")
        self.setup_email(self.login_frame)
        self.setup_password(self.login_frame, 0.02, 0.3)
        self.setup_submit_button(self.login_frame, "Sign in", 0.02, 0.5, self.l_when_submit)
        self.setup_confirmation_label(self.login_frame, 0.6)
        self.setup_switch_button(self.login_frame, "want to register?", 0.25, 0.5, self.switch_to_registration)

    def switch_to_registration(self):
        self.register_frame = ttk.Frame(master=self)
        self.setup_welcome(self.register_frame, "Welcome to CloudAV")
        self.setup_email(self.register_frame)
        self.setup_username(self.register_frame)
        self.setup_password(self.register_frame, 0.02, 0.45)
        self.setup_submit_button(self.register_frame, "Sign up", 0.02, 0.65, self.r_when_submit)
        self.setup_confirmation_label(self.register_frame, 0.75)
        self.setup_switch_button(self.register_frame, "want to login?", 0.25, 0.65, self.switch_to_login)

        self.login_frame.destroy()
        self.register_frame.pack(side="top", fill="both", expand=True)
        self.attempt_type = "<REGISTER>"

    def switch_to_login(self):
        self.login_frame = ttk.Frame(master=self)
        self.setup_welcome(self.login_frame, "Welcome back to CloudAV")
        self.setup_email(self.login_frame)
        self.setup_password(self.login_frame, 0.02, 0.3)
        self.setup_submit_button(self.login_frame, "Sign in", 0.02, 0.5, self.l_when_submit)
        self.setup_confirmation_label(self.login_frame, 0.6)
        self.setup_switch_button(self.login_frame, "want to register?", 0.25, 0.5, self.switch_to_registration)

        self.register_frame.destroy()
        self.login_frame.pack(side="top", fill="both", expand=True)
        self.attempt_type = "<LOGIN>"

    @staticmethod
    def setup_welcome(master, welcome_msg):
        set_appearance_mode("system")
        welcome = ttk.Label(
            master=master,
            text=welcome_msg,
            font=("Calibri bold", 35)
        )
        welcome.place(relx=0.02, rely=0.05)

    def setup_email(self, master):
        l_email = ttk.Label(
            master=master,
            text="Email",
            font=("Calibri", 15)
        )
        l_email.place(relx=0.02, rely=0.15)
        self.email_entry = ttk.Entry(
            master=master,
            width=60,
        )
        self.email_entry.place(relx=0.02, rely=0.2)
        self.email_entry.insert(0, "tomerbs1810@gmail.com")
        self.ans_email = ttk.Label(
            master=master,
            text=""
        )
        self.ans_email.place(relx=0.02, rely=0.255)

    def setup_username(self, master):
        l_username = ttk.Label(
            master=master,
            text="Username",
            font=("Calibri", 15)
        )
        l_username.place(relx=0.02, rely=0.3)
        self.username_entry = ttk.Entry(
            master=master,
            width=60
        )
        self.username_entry.place(relx=0.02, rely=0.35)
        self.ans_username = ttk.Label(
            master=master,
            text=""
        )
        self.ans_username.place(relx=0.02, rely=0.405)

    def setup_password(self, master, posx, posy):
        l_password = ttk.Label(
            master=master,
            text="Password",
            font=("Calibri", 15)
        )
        l_password.place(relx=posx, rely=posy)
        self.password_entry = ttk.Entry(
            master=master,
            width=60
        )
        self.password_entry.place(relx=0.02, rely=posy + 0.05)
        self.password_entry.insert(0, "01102006t")
        self.ans_password = ttk.Label(
            master=master,
            text=""
        )
        self.ans_password.place(relx=0.02, rely=posy + 0.107)

    def setup_confirmation_label(self, master, posy):
        self.l_confirm = ttk.Label(
            master=master,
            text="",
            font=("Calibri bold", 20),
        )
        self.l_confirm.place(relx=0.02, rely=posy)

    def setup_submit_button(self, master, submit_title, posx, posy, submit_command):
        self.submit_btn = ttk.Button(
            master=master,
            text=submit_title,
            command=submit_command
        )
        self.submit_btn.place(relx=posx, rely=posy)

    def setup_switch_button(self, master, switch_msg, posx, posy, switch_command):
        self.switch_btn = ttk.Button(
            master=master,
            text=switch_msg,
            command=switch_command
        )
        self.switch_btn.place(relx=posx, rely=posy)

    def r_when_submit(self):
        checksum = 0

        u_email = self.email_entry.get()
        if len(u_email) > 0 and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', u_email):
            self.ans_email.configure(text="Email is valid.", foreground="green")
            checksum += 1
        else:
            self.ans_email.configure(text="Invalid email. Please enter a valid email.", foreground="red")
            checksum -= 1 if checksum != 0 else 0

        u_username = self.username_entry.get()
        if len(u_username) >= 6:
            self.ans_username.configure(text="Username is valid", foreground="green")
            checksum += 1
        else:
            self.ans_username.configure(text="Invalid username. must be 6 characters or longer.", foreground="red",
                                        )
            checksum -= 1 if checksum != 0 else 0

        u_password = self.password_entry.get()
        if len(u_password) > 0 and len(u_password) >= 8:
            self.ans_password.configure(text="Password is valid", foreground="green")
            checksum += 1
        else:
            self.ans_password.configure(text="Invalid password. must be 8 characters or longer.", foreground="red")
            checksum -= 1 if checksum != 0 else 0

        if checksum == 3:
            self.client_socket.sendall(self.attempt_type.encode())
            print("status sent")

            if self.attempt_type == "<REGISTER>":
                print("User info -----------------------")
                print(f"Email: {u_email}")
                print(f"Username: {u_username}")
                print(f"Password: {u_password}")
                print("---------------------------------")

                field_dict = {
                    'email': u_email,
                    'username': u_username,
                    'password': u_password,
                }

                self.client_socket.sendall(pickle.dumps(field_dict))

                self.server_reg_ans = self.client_socket.recv(1024).decode()
                print(f"answer: {self.server_reg_ans}")

                if self.server_reg_ans == "<EXISTS>":
                    self.ans_email.configure(text="Registration failed. Email is already in use.", foreground="red")
                    self.ans_username.configure(text="Registration failed.", foreground="red")
                    self.ans_password.configure(text="Registration failed.", foreground="red")
                elif self.server_reg_ans == "<SUCCESS>":
                    self.l_confirm.configure(text="User Registered successfully", foreground="green")
                    self.switch_callback(MainPage)

    def l_when_submit(self):
        checksum = 0

        u_email = self.email_entry.get()
        if len(u_email) > 0 and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', u_email):
            self.ans_email.configure(text="Email is valid.", foreground="green")
            checksum += 1
        else:
            self.ans_email.configure(text="Invalid email. Please enter a valid email.", foreground="red")
            checksum -= 1 if checksum != 0 else 0

        u_password = self.password_entry.get()
        if len(u_password) >= 8:
            self.ans_password.configure(text="Password is valid", foreground="green")
            checksum += 1
        else:
            self.ans_password.configure(text="Invalid password. must be 8 characters or longer.", foreground="red")
            checksum -= 1 if checksum != 0 else 0

        if checksum == 2:
            self.client_socket.sendall(self.attempt_type.encode())

            if self.attempt_type == "<LOGIN>":
                print("User info -----------------------")
                print(f"Email: {u_email}")
                print(f"Password: {u_password}")
                print("---------------------------------")

                field_dict = {
                    'email': u_email,
                    'password': u_password
                }

                self.client_socket.sendall(pickle.dumps(field_dict))

                self.server_login_ans = self.client_socket.recv(1024).decode()
                print(f"answer: {self.server_login_ans}")

                if self.server_login_ans == "<NO_EMAIL_EXISTS>":
                    self.ans_email.configure(text="Login failed. No accounts under the provided email."
                                             , foreground="red")
                    self.ans_password.configure(text="Login failed. Password doesn't match the provided email."
                                                , foreground="red")
                elif self.server_login_ans == "<WRONG_PASSWORD>":
                    self.ans_password.configure(text="Login failed. Password doesn't match the provided email."
                                                , foreground="red")
                else:
                    self.l_confirm.configure(text=f"Welcome back {self.server_login_ans}", foreground="green")
                    self.switch_callback(MainPage)


class FileFrame(ttk.Frame):
    def __init__(self, fname, fsize, fdate, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        self.id_of_frame = random.randint(1, 100)
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
    def __init__(self, parent, client_socket: socket, switch_callback):
        super().__init__(parent)
        self.parent_app = parent
        self.client_socket = client_socket
        self.switch_callback = switch_callback

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

        # Activate the function after MainPage has finished loading
        time.sleep(3)
        self.notify_and_receive_files()

    def notify_and_receive_files(self):
        self.client_socket.send(b'<NARF>')

        # Receive the length of the pickled data
        data_len = int(self.client_socket.recv(1024).decode())

        # Receive the pickled data
        pickled_data = self.client_socket.recv(data_len)

        # Load the pickled data
        saved_file_prop_lst = pickle.loads(pickled_data)

        for individual_file in saved_file_prop_lst:
            file_name, file_bytes, file_date = individual_file

            short_filename, formatted_file_size, short_file_date = \
                self.prepare_for_display(file_name, file_bytes, file_date)

            self.add_file_frame(short_filename, formatted_file_size, short_file_date)

        print("All files received")

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

        original_date = datetime.strptime(file_uploadate, "%Y-%m-%d %H:%M:%S.%f")
        short_file_date = original_date.strftime("%y/%m/%d")

        return short_filename, formatted_file_size, short_file_date

    def add_file(self):
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
            file_date = datetime.now()

            # formatting all the properties
            short_filename, formatted_file_size, short_file_date = \
                self.prepare_for_display(file_name, file_bytes, file_date)

            self.client_socket.send(pickle.dumps([short_filename, file_bytes, short_file_date]))
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
                self.add_file_frame(short_filename, formatted_file_size, short_file_date)

        except FileNotFoundError:  # in cases of an error
            return

    def add_file_frame(self, file_name, file_size, file_date):
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
            self.client_socket.send(b'<R>')
            select_file_names_lst = self.checked_file_frames()

            # Convert the list to a pickled string
            pickled_data = pickle.dumps(select_file_names_lst)

            # Send the length of the pickled data
            data_len = str(len(pickled_data))
            self.client_socket.send(data_len.encode())

            # Send the pickled data
            self.client_socket.send(pickled_data)

            # Now the client receives the dictionary from the server
            data_len = int(self.client_socket.recv(1024).decode())
            pickled_fdn_dict = self.client_socket.recv(data_len)

            # Load the dictionary
            file_data_name_dict = pickle.loads(pickled_fdn_dict)

            for indiv_filename, indiv_filebytes in file_data_name_dict.items():
                file_path = os.path.join(self.save_path, indiv_filename)
                with open(file_path, "wb") as file:
                    file.write(indiv_filebytes)
                    print(f"File '{indiv_filename}' received successfully.")

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
    def __init__(self, client_socket):
        super().__init__()
        self.geometry("1150x810")
        self.title("Cloud-AV")
        self.client_socket = client_socket
        self.current_frame = None
        self.switch_frame(RegistrationApp)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self, self.client_socket, self.switch_frame)

        if self.current_frame:
            self.current_frame.pack_forget()

        new_frame.pack(fill="both", expand=True)
        self.current_frame = new_frame


if __name__ == "__main__":
    my_app = MyApp(client_socket=None)
    my_app.mainloop()
