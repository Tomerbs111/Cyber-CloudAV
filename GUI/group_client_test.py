import threading
import time
from tkinter import filedialog as fd
from datetime import date
import customtkinter
import ttkbootstrap as ttk
from customtkinter import *
from PIL import Image, ImageTk

from GUI.GroupsPage import GroupsPage

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

from tkvideo import tkvideo


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
                self.after(1000, lambda: self.switch_callback("HomePage", self.client_communicator))

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
            self.server_ans = "n"

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
                self.after(1000, lambda: self.switch_callback("HomePage", self.client_communicator))


class FileFrame(ttk.Frame):
    def __init__(self, master, fname, fsize, fdate, favorite_callback=None):
        super().__init__(master)
        self.fname = fname
        self.fsize = fsize
        self.fdate = fdate

        self.check_var = StringVar(value="off")
        self.mark_for_action = ttk.Checkbutton(self, text="",
                                               variable=self.check_var, onvalue="on", offvalue="off")
        self.mark_for_action.pack(side='left', padx=5)

        # Set the default icon path
        icon_path = "GUI/file_icons/other_file_icon.png"

        # Check file type and set icon accordingly
        if self.is_image(fname):
            icon_path = "GUI/file_icons/image_file_icon.png"
        elif self.is_document(fname):
            icon_path = "GUI/file_icons/word_file_icon.png"
        elif self.is_pdf(fname):
            icon_path = "GUI/file_icons/pdf_file_icon.png"
        elif self.is_powerpoint(fname):
            icon_path = "GUI/file_icons/powerpoint_file_icon.png"
        elif self.is_text(fname):
            icon_path = "GUI/file_icons/text_file_icon.png"
        elif self.is_zip(fname):
            icon_path = "GUI/file_icons/zip_file_icon.png"
        elif self.is_excel(fname):
            icon_path = "GUI/file_icons/excel_file_icon.png"
        elif self.is_video(fname):
            icon_path = "GUI/file_icons/video_file_icon.png"
        elif self.is_code(fname):
            icon_path = "GUI/file_icons/code_file_icon.png"

        # Load the icon image
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize((25, 25))

        tk_icon_image = ImageTk.PhotoImage(icon_image)

        # Create a label to display the icon
        icon_label = ttk.Label(master=self, image=tk_icon_image)
        icon_label.image = tk_icon_image
        icon_label.pack(side='left', padx=(0, 5), pady=5)

        text_size = 12

        self.check_favorite = StringVar(value="off")
        self.favorite_callback = favorite_callback

        self.favorite_button = CTkButton(
            master=self,
            image=CTkImage(Image.open("GUI/file_icons/star_icon.png"), size=(20, 20)),
            compound='left',
            text="",
            width=30,
            fg_color='transparent',
            command=self.toggle_favorite  # Assign the command to the function
        )

        self.favorite_button.pack(side='right', padx=5, anchor='e')

        # Create labels with larger text
        self.lu_filename = ttk.Label(
            master=self,
            text=self.fname,
            font=("Arial", text_size)
        )
        self.lu_filename.pack(side='left', padx=(0, 5), pady=5, anchor='w')

        # Pack the size label with proper alignment
        self.lu_size = ttk.Label(
            master=self,
            text=self.fsize,
            font=("Arial", text_size)
        )
        self.lu_size.pack(side='right', padx=(0, 27), pady=5, anchor='e')  # Adjust padx as needed

        # Pack the date label with proper alignment
        self.lu_date_mod = ttk.Label(
            master=self,
            text=self.fdate,
            font=("Arial", text_size)
        )
        self.lu_date_mod.pack(side='right', padx=(0, 65), pady=5, anchor='e')

    def toggle_favorite(self):
        current_value = self.check_favorite.get()
        new_value = "on" if current_value == "off" else "off"
        self.check_favorite.set(new_value)

        # Change the button icon based on the new value
        new_icon_path = "GUI/file_icons/star_icon_light.png" if new_value == "on" else "GUI/file_icons/star_icon.png"
        new_icon = CTkImage(Image.open(new_icon_path), size=(20, 20))
        self.favorite_button.configure(image=new_icon)

        # Notify the HomePage when the favorite button is pressed
        if self.favorite_callback:
            self.favorite_callback(self, new_value)

    def get_checkvar(self) -> bool:
        return self.check_var.get() == "on"

    def get_filename(self):
        return self.fname

    def set_filename(self, fname):
        self.fname = fname
        self.lu_filename.configure(text=fname)

    def uncheck(self):
        self.check_var.set("off")

    def kill_frame(self):
        self.destroy()

    def is_image(self, fname):
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        return any(fname.lower().endswith(ext) for ext in image_extensions)

    def is_document(self, fname):
        document_extensions = ['.doc', '.docx']
        return any(fname.lower().endswith(ext) for ext in document_extensions)

    def is_pdf(self, fname):
        pdf_extensions = ['.pdf']
        return any(fname.lower().endswith(ext) for ext in pdf_extensions)

    def is_powerpoint(self, fname):
        powerpoint_extensions = ['.ppt', '.pptx', '.pps', '.pot', '.potx', '.ppsx']
        return any(fname.lower().endswith(ext) for ext in powerpoint_extensions)

    def is_text(self, fname):
        text_extensions = ['.txt']
        return any(fname.lower().endswith(ext) for ext in text_extensions)

    def is_zip(self, fname):
        zip_extensions = ['.zip', '.rar', '.7z', '.tar', '.gz']
        return any(fname.lower().endswith(ext) for ext in zip_extensions)

    def is_excel(self, fname):
        excel_extensions = ['.xlsx', '.dbf', '.csv', '.xls', '.xlsm']
        return any(fname.lower().endswith(ext) for ext in excel_extensions)

    def is_video(self, fname):
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.mp3', '.asd']
        return any(fname.lower().endswith(ext) for ext in video_extensions)

    def is_code(self, fname):
        code_extensions = ['.py', '.c', '.cpp', '.java', '.js', '.php', '.css', '.cs']
        return any(fname.lower().endswith(ext) for ext in code_extensions)


class Page(ttk.Frame):
    def __init__(self, master, switch_frame, client_communicator):
        super().__init__(master)
        self.current_frame = None
        self.master = master
        self.switch_frame = switch_frame
        self.client_communicator = client_communicator

        self.f_data_center = None
        self.f_current_page = None

        self.setup_searchbar_frame()
        self.setup_option_frame()
        self.setup_data_center_frame()
        self.setup_current_page_frame()

    def setup_searchbar_frame(self):
        # Code for setting up the Searchbar frame
        f_searchbar = ttk.Frame(master=self, style="dark")
        f_searchbar.pack(side="top", fill="x")

        cloudav_image = CTkImage(
            light_image=Image.open(r"../GUI/file_icons/only_logo.png"),
            dark_image=Image.open(r"../GUI/file_icons/only_logo.png"),
            size=(75, 75))
        cav_image_lbl = CTkLabel(master=f_searchbar, image=cloudav_image, text="")
        cav_image_lbl.pack(side="left", padx=10)

        search_frame = ttk.Frame(master=f_searchbar, style="dark")
        search_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.3, relheight=0.5)

        search_button = ttk.Button(search_frame, text="Search")
        search_button.pack(side="left", expand=True, fill="x")

        search_entry = ttk.Entry(search_frame, width=70)
        search_entry.pack(side="left", expand=True, fill="x")

        # Profile Photo Placeholder on the Right
        profile_photo_placeholder = ttk.Label(f_searchbar, text="👤", font=("Arial", 30))
        profile_photo_placeholder.pack(side="right", padx=10)

        # Settings Button on the Right
        settings_button = ttk.Button(f_searchbar, text="Settings")
        settings_button.pack(side="right", padx=10)

    def setup_data_center_frame(self):
        # Code for setting up the Data center frame
        self.f_data_center = ttk.Frame(master=self, style="default")
        self.f_data_center.place(rely=0.1, relx=0, relheight=0.9, relwidth=1)

    def setup_option_frame(self):
        # Code for setting up the Option frame
        f_options = ttk.Frame(master=self.f_data_center, style="dark")
        f_options.place(relx=0, rely=0.1, relwidth=0.2, relheight=1)

        CTkButton(
            f_options,
            text="Add",
            image=CTkImage(Image.open("../GUI/file_icons/add_file_plus_icon.png"), size=(30, 30)),
            compound='left'
        ).pack(side='top', pady=20, anchor='w', padx=10)

        ttk.Separator(f_options, orient="horizontal").pack(side='top', fill='x', pady=5, padx=10)

        CTkButton(
            f_options,
            text="Home",
            image=CTkImage(Image.open("../GUI/file_icons/home_icon.png"), size=(20, 20)),
            compound='left',
            command=self.switch_to_home
        ).pack(side='top', pady=5, anchor='w', fill='x', padx=10)

        CTkButton(
            f_options,
            text="Shared",
            image=CTkImage(Image.open("../GUI/file_icons/shared_icon.png"), size=(20, 20)),
            compound='left'
        ).pack(side='top', pady=5, anchor='w', fill='x', padx=10)

        CTkButton(
            f_options,
            text="Favorites",
            image=CTkImage(Image.open("../GUI/file_icons/star_icon.png"), size=(20, 20)),
            compound='left',
        ).pack(side='top', pady=5, anchor='w', fill='x', padx=10)

        CTkButton(
            f_options,
            text="Groups",
            image=CTkImage(Image.open("../GUI/file_icons/group_icon.png"), size=(20, 20)),
            compound='left',
            command=self.switch_to_groups
        ).pack(side='top', pady=5, anchor='w', fill='x', padx=10)

        CTkButton(
            f_options,
            text="Recycle bin",
            image=CTkImage(Image.open("../GUI/file_icons/trash_icon.png"), size=(20, 20)),
            compound='left'
        ).pack(side='top', pady=5, anchor='w', fill='x', padx=10)

        CTkButton(
            f_options,
            text="Log out",
            image=CTkImage(Image.open("../GUI/file_icons/log_out_icon.png"), size=(20, 20)),
            compound='left'
        ).pack(side='top', pady=5, anchor='w', fill='x', padx=10)

        ttk.Label(f_options, text="Storage:").pack(side='top', pady=10, anchor='w', fill='x', padx=10)

    def setup_current_page_frame(self):
        self.f_current_page = ttk.Frame(master=self.f_data_center, style="info")
        self.f_current_page.place(relx=0.21, rely=0.02, relwidth=0.78, relheight=0.96)

    def switch_to_groups(self):
        print("Switching to groups page")
        self.switch_frame("GroupsPage", self.client_communicator)

    def switch_to_home(self):
        print("Switching to home page")
        self.switch_frame("HomePage", self.client_communicator)


class HomePage(ttk.Frame):
    def __init__(self, parent, switch_frame, client_communicator):
        super().__init__(parent)
        self.parent_app = parent
        self.switch_frame = switch_frame
        self.client_communicator = client_communicator

        self.f_file_list = None
        self.file_frames = []
        self.file_frame_counter = 0
        self.save_path = None
        self.rename_button = None

        self.setup_file_actions_frame()

    def setup_file_actions_frame(self):
        f_action = ttk.Frame(master=self)
        f_action.place(relx=0, rely=0, relwidth=1, relheight=0.05)

        delete_button = CTkButton(
            master=f_action,
            image=CTkImage(Image.open("../GUI/file_icons/trash_icon.png"), size=(20, 20)),
            compound='left',
            text="Delete",
            width=30,
            command=self.delete_checked_file,
            fg_color='transparent'
        )
        delete_button.pack(side='left', padx=5)

        download_button = CTkButton(
            master=f_action,
            command=self.receive_checked_files,
            image=CTkImage(Image.open("../GUI/file_icons/download_icon.png"), size=(20, 20)),
            compound='left',
            text="Download",
            width=30,
            fg_color='transparent'
        )
        download_button.pack(side='left', padx=5)

        self.rename_button = CTkButton(
            master=f_action,
            image=CTkImage(Image.open("../GUI/file_icons/rename_icon.png"), size=(20, 20)),
            compound='left',
            text="Rename",
            width=30,
            command=self.rename_checked_file,
            fg_color='transparent'
        )
        self.rename_button.pack(side='left', padx=5)

        shared_button = CTkButton(
            master=f_action,
            image=CTkImage(Image.open("../GUI/file_icons/shared_icon.png"), size=(20, 20)),
            compound='left',
            text="Share",
            width=30,
            fg_color='transparent'
        )
        shared_button.pack(side='left', padx=5)

        copy_button = CTkButton(
            master=f_action,
            image=CTkImage(Image.open("../GUI/file_icons/copy_icon.png"), size=(20, 20)),
            compound='left',
            text="Copy",
            width=30,
            fg_color='transparent'
        )
        copy_button.pack(side='left', padx=5)

        combined_frame = CTkFrame(master=self)
        combined_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)

        f_file_properties = CTkFrame(master=combined_frame, fg_color='transparent')
        f_file_properties.place(relx=0, rely=0, relwidth=1, relheight=0.08)

        CTkButton(master=f_file_properties, text="Name").pack(side='left', padx=5)
        CTkButton(master=f_file_properties, text="Size").pack(side='right', padx=10)
        CTkButton(master=f_file_properties, text="Upload date").pack(side='right', padx=10)

        ttk.Separator(combined_frame, orient="horizontal").place(relx=0, rely=0.08, relwidth=1)

        self.f_file_list = CTkScrollableFrame(master=combined_frame, fg_color='transparent')
        self.f_file_list.place(relx=0, rely=0.09, relwidth=1, relheight=0.91)

    def add_file(self):
        try:
            filetypes = (
                ('All files', '*.*'),
                ('text files', '*.txt'),
                ('All files', '*.*')
            )

            file_name = fd.askopenfilename(
                title='Select a file',
                initialdir='/',
                filetypes=filetypes)

            file_bytes = os.path.getsize(file_name)
            file_date = date.today()

            short_filename, formatted_file_size, short_file_date = \
                self.prepare_for_display(file_name, file_bytes, file_date)

            send_file_thread = threading.Thread(
                target=self.client_communicator.send_file(file_name, short_filename,
                                                          short_file_date, file_bytes))
            send_file_thread.start()

            favorite = 0

            self.add_file_frame(short_filename, formatted_file_size, short_file_date, favorite)

        except FileNotFoundError:
            return

    def add_file_frame(self, file_name, file_size, file_date, favorite):
        file_frame = FileFrame(self.f_file_list, file_name, file_size, file_date,
                               favorite_callback=self.favorite_file_pressed)

        file_frame.pack(expand=True, fill='x', side='top')
        self.file_frames.append(file_frame)
        self.file_frame_counter += 1

        if favorite == 1:
            file_frame.favorite_button.configure(
                image=CTkImage(Image.open("../GUI/file_icons/star_icon_light.png"), size=(20, 20)))
            file_frame.check_favorite.set("on")

    def favorite_file_pressed(self, file_frame, new_value):
        file_name = file_frame.get_filename()
        if new_value == "on":
            favorite_thread = threading.Thread(
                target=self.client_communicator.favorite_file,
                args=(file_name, new_value))
            favorite_thread.start()
        else:
            unfavorite_thread = threading.Thread(
                target=self.client_communicator.favorite_file,
                args=(file_name, new_value))
            unfavorite_thread.start()

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

    def prepare_for_display(self, file_name, file_bytes, file_uploadate: date):
        short_filename = os.path.basename(file_name)
        formatted_file_size = self.format_file_size(file_bytes)

        short_file_date = file_uploadate.strftime('%B %d, %Y')

        return short_filename, formatted_file_size, short_file_date

    def checked_file_frames(self):
        checked_file_frames_list = []
        for file_frame in self.file_frames:
            if file_frame.get_checkvar():
                checked_file_frames_list.append(file_frame)
                file_frame.uncheck()

        return checked_file_frames_list

    def delete_checked_file(self):
        frames_to_delete = self.checked_file_frames()
        names_to_delete_lst = [file_frame.get_filename() for file_frame in frames_to_delete]
        print(names_to_delete_lst)

        self.client_communicator.delete_checked_files(names_to_delete_lst)
        for file_frame in frames_to_delete:
            file_frame.kill_frame()

        self.file_frame_counter = len(self.file_frames)

    def receive_checked_files(self):
        if self.save_path is None:
            self.get_save_path_dialog()
        else:
            select_file_frames = self.checked_file_frames()
            select_file_names_lst = [file_frame.get_filename() for file_frame in select_file_frames]

            receive_thread = threading.Thread(
                target=self.client_communicator.receive_checked_files,
                args=(select_file_names_lst, self.save_path))
            receive_thread.start()

    def rename_checked_file(self):
        try:
            file_frame = self.checked_file_frames()[0]
            old_name = file_frame.get_filename()

            file_format = os.path.splitext(old_name)[1]

            new_name_dialog = CTkInputDialog(text=f"Replace {old_name} with:",
                                             title="Rename file")
            new_name = new_name_dialog.get_input()

            if new_name:
                new_name_with_format = f"{new_name}{file_format}"

                rename_thread = threading.Thread(
                    target=self.client_communicator.rename_files,
                    args=((old_name, new_name_with_format),))
                rename_thread.start()

                file_frame.set_filename(new_name_with_format)
                file_frame.update_idletasks()
        except IndexError:
            pass

    def get_save_path_dialog(self):
        dialog = CTkInputDialog(text="Write the path you want to save your files on:",
                                title="Get save path")
        input_path = dialog.get_input()

        if input_path:
            self.save_path = os.path.normpath(input_path)
        else:
            self.save_path = os.path.join(os.path.expanduser("~"), "Downloads")



class MyApp(ttk.Window):
    def __init__(self, client_communicator):
        super().__init__(themename="darkly")
        self.geometry("1150x710")
        self.title("Cloud-AV")

        self.current_frame = None
        self.client_communicator = client_communicator
        self.page = Page(self, self.switch_frame, self.client_communicator)

        self.switch_frame("RegistrationApp", self.client_communicator)

    def switch_frame(self, frame_class, *args):
        if frame_class == "RegistrationApp":
            new_frame = RegistrationApp(self, self.switch_frame, *args)

            if self.current_frame:
                self.current_frame.pack_forget()

            new_frame.pack(fill="both", expand=True)
            self.current_frame = new_frame

        else:
            new_frame = globals()[frame_class](self.page.f_current_page, self.switch_frame, *args)

            if self.current_frame:
                self.current_frame.pack_forget()

            self.page.pack(fill="both", expand=True)
            new_frame.pack(fill="both", expand=True)


            self.current_frame = new_frame


if __name__ == "__main__":
    app = MyApp(None)
    app.mainloop()
