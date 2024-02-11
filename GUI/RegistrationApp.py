import threading
from tkinter import filedialog as fd
from datetime import datetime
import customtkinter
from ttkbootstrap.scrolled import ScrolledFrame
import re
import ttkbootstrap as ttk
from customtkinter import *
from PIL import Image, ImageTk
import tkinter as tk

from GUI.HomePage import HomePage
from tkvideo import tkvideo


class RegistrationApp(ttk.Frame):
    def __init__(self, parent, switch_frame, client_communicator):
        super().__init__(parent)
        self.parent_app = parent
        self.switch_frame = switch_frame
        self.client_communicator = client_communicator

        self.register_frame = ttk.Frame(master=self)

        # Frame for fields (left side)
        self.login_frame = ttk.Frame(master=self)
        self.login_frame.place(x=0, y=0, relwidth=0.45, relheight=1)

        # Frame for animation (right side)
        self.animation_frame = CTkFrame(master=self, )
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

        self.setup_email(self.login_frame, posx=0.04, posy=0.2)
        self.setup_password(self.login_frame, posx=0.04, posy=0.35)
        self.setup_submit_button(self.login_frame, "Sign in", posx=0.04, posy=0.55,
                                 submit_command=self.l_when_submit)
        self.setup_confirmation_label(self.login_frame, posy=0.8)

        cav_image_lbl = tk.Label(master=self.animation_frame)
        cav_image_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)
        video_path = r'..\GUI\file_icons\video_reglog2.mp4'  # Replace with your actual video file path

        # Create an instance of tkvideo
        video_player = tkvideo(video_path, cav_image_lbl, loop=1, size=(900, 900))

        # Set the video file path
        video_player.play()

    def switch_to_registration(self):
        self.register_frame = ttk.Frame(master=self)
        self.setup_logo(self.register_frame, posx=0.01, posy=0.04)
        self.setup_welcome(self.register_frame, "Register", posx=0.15, posy=0.05)
        self.setup_switch_button(self.register_frame, "sign in", posx=0.02, posy=0.15,
                                 switch_command=self.switch_to_login,
                                 text_before_btn_text="Already have an account? Click here to ")

        self.setup_email(self.register_frame, posx=0.04, posy=0.2)
        self.setup_username(self.register_frame, posx=0.04, posy=0.35)
        self.setup_password(self.register_frame, posx=0.04, posy=0.50)
        self.setup_submit_button(self.register_frame, "Sign up", posx=0.04, posy=0.70,
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

        self.setup_email(self.login_frame, posx=0.04, posy=0.2)
        self.setup_password(self.login_frame, posx=0.04, posy=0.35)
        self.setup_submit_button(self.login_frame, "Sign in", posx=0.04, posy=0.55,
                                 submit_command=self.l_when_submit)
        self.setup_confirmation_label(self.login_frame, posy=0.8)

        self.register_frame.destroy()
        self.login_frame.place(x=0, y=0, relwidth=0.45, relheight=1)
        self.attempt_type = "<LOGIN>"

    @staticmethod
    def setup_logo(master, posx, posy):
        cloudav_image = CTkImage(
            light_image=Image.open(
                r"../GUI/file_icons/only_logo.png"),
            dark_image=Image.open(
                r"../GUI/file_icons/only_logo.png"),
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
            style="info"

        )
        l_email.place(relx=posx, rely=posy, relwidth=label_width, relheight=label_height)

        self.email_entry = ttk.Entry(
            master=master,
            width=60,  # Set the width based on the desired entry width
            style="primary",

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
            style="info"
        )
        l_username.place(relx=posx, rely=posy, relwidth=label_width, relheight=label_height)

        self.username_entry = ttk.Entry(
            master=master,
            width=60,  # Set the width based on the desired entry width
            style="primary"
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
            style="info"

        )
        l_password.place(relx=posx, rely=posy, relwidth=label_width, relheight=label_height)

        self.password_entry = ttk.Entry(
            master=master,
            width=60,  # Set the width based on the desired entry width
            style="primary"

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
            style="info"
        )
        self.submit_btn.place(relx=posx, rely=posy, relwidth=button_width, relheight=button_height)

    # Modify the switch button setup method in your RegLog class

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
            self.server_ans = self.client_communicator.r_when_submit(self.attempt_type, u_email, u_username, u_password)

            if self.server_ans == "<EXISTS>":
                self.ans_email.configure(text="Registration failed. Email is already in use.", bootstyle="danger")
                self.ans_username.configure(text="Registration failed.", bootstyle="danger")
                self.ans_password.configure(text="Registration failed.", bootstyle="danger")
            elif self.server_ans == "<SUCCESS>":
                self.l_confirm.configure(text="User Registered successfully", bootstyle="success")
                self.after(1000, lambda: self.switch_frame("HomePage", self.client_communicator))

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
                self.after(1000, lambda: self.switch_frame("HomePage", self.client_communicator))
