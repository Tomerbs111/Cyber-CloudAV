import pickle

from customtkinter import *
import packaging
import re


class RegistrationApp(CTk):
    def __init__(self, client_socket):
        super().__init__()
        self.geometry("700x500")
        self.title("Test App")

        self.login_frame = CTkFrame(master=self)
        self.login_frame.pack(side="top", fill="both", expand=True)

        self.register_frame = CTkFrame(master=self)

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
        self.register_frame = CTkFrame(master=self)
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
        self.login_frame = CTkFrame(master=self)
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
        welcome = CTkLabel(
            master=master,
            text=welcome_msg,
            font=("Calibri bold", 35)
        )
        welcome.place(relx=0.02, rely=0.05)

    def setup_email(self, master):
        l_email = CTkLabel(
            master=master,
            text="Email",
            font=("Calibri", 15)
        )
        l_email.place(relx=0.02, rely=0.15)
        self.email_entry = CTkEntry(
            master=master,
            placeholder_text="example@example.com",
            width=300,
        )
        self.email_entry.place(relx=0.02, rely=0.2)
        self.ans_email = CTkLabel(
            master=master,
            text=""
        )
        self.ans_email.place(relx=0.02, rely=0.255)

    def setup_username(self, master):
        l_username = CTkLabel(
            master=master,
            text="Username",
            font=("Calibri", 15)
        )
        l_username.place(relx=0.02, rely=0.3)
        self.username_entry = CTkEntry(
            master=master,
            placeholder_text="Min. 6 characters",
            width=300
        )
        self.username_entry.place(relx=0.02, rely=0.35)
        self.ans_username = CTkLabel(
            master=master,
            text=""
        )
        self.ans_username.place(relx=0.02, rely=0.405)

    def setup_password(self, master, posx, posy):
        l_password = CTkLabel(
            master=master,
            text="Password",
            font=("Calibri", 15)
        )
        l_password.place(relx=posx, rely=posy)
        self.password_entry = CTkEntry(
            master=master,
            placeholder_text="Min. 8 characters",
            width=300
        )
        self.password_entry.place(relx=0.02, rely=posy + 0.05)
        self.ans_password = CTkLabel(
            master=master,
            text=""
        )
        self.ans_password.place(relx=0.02, rely=posy + 0.107)

    def setup_confirmation_label(self, master, posy):
        self.l_confirm = CTkLabel(
            master=master,
            text="",
            font=("Calibri bold", 20),
            text_color="#009900"
        )
        self.l_confirm.place(relx=0.02, rely=posy)

    def setup_submit_button(self, master, submit_title, posx, posy, submit_command):
        self.submit_btn = CTkButton(
            master=master,
            text=submit_title,
            command=submit_command
        )
        self.submit_btn.place(relx=posx, rely=posy)

    def setup_switch_button(self, master, switch_msg, posx, posy, switch_command):
        self.switch_btn = CTkButton(
            master=master,
            text=switch_msg,
            command=switch_command
        )
        self.switch_btn.place(relx=posx, rely=posy)

    def r_when_submit(self):
        checksum = 0

        u_email = self.email_entry.get()
        if len(u_email) > 0 and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', u_email):
            self.ans_email.configure(text="Email is valid.", text_color="#009900")
            checksum += 1
        else:
            self.ans_email.configure(text="Invalid email. Please enter a valid email.", text_color="#FF0000")
            checksum -= 1 if checksum != 0 else 0

        u_username = self.username_entry.get()
        if len(u_username) >= 6:
            self.ans_username.configure(text="Username is valid", text_color="#009900")
            checksum += 1
        else:
            self.ans_username.configure(text="Invalid username. must be 6 characters or longer.",
                                        text_color="#FF0000")
            checksum -= 1 if checksum != 0 else 0

        u_password = self.password_entry.get()
        if len(u_password) > 0 and len(u_password) >= 8:
            self.ans_password.configure(text="Password is valid", text_color="#009900")
            checksum += 1
        else:
            self.ans_password.configure(text="Invalid password. must be 8 characters or longer.", text_color="#FF0000")
            checksum -= 1 if checksum != 0 else 0

        if checksum == 3:
            self.client_socket.send(self.attempt_type.encode())
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

                self.client_socket.send(pickle.dumps(field_dict))


                self.server_reg_ans = self.client_socket.recv(1024).decode()
                print(f"answer: {self.server_reg_ans}")

                if self.server_reg_ans == "<EXISTS>":
                    self.ans_email.configure(text="Registration failed. Email is already in use.", text_color="#FF0000")
                    self.ans_username.configure(text="Registration failed.", text_color="#FF0000")
                    self.ans_password.configure(text="Registration failed.", text_color="#FF0000")
                elif self.server_reg_ans == "<SUCCESS>":
                    self.l_confirm.configure(text="User Registered successfully")
                    self.auth_completed = True

    def l_when_submit(self):
        checksum = 0

        u_email = self.email_entry.get()
        if len(u_email) > 0 and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', u_email):
            self.ans_email.configure(text="Email is valid.", text_color="#009900")
            checksum += 1
        else:
            self.ans_email.configure(text="Invalid email. Please enter a valid email.", text_color="#FF0000")
            checksum -= 1 if checksum != 0 else 0

        u_password = self.password_entry.get()
        if len(u_password) >= 8:
            self.ans_password.configure(text="Password is valid", text_color="#009900")
            checksum += 1
        else:
            self.ans_password.configure(text="Invalid password. must be 8 characters or longer.", text_color="#FF0000")
            checksum -= 1 if checksum != 0 else 0

        if checksum == 2:
            self.client_socket.send(self.attempt_type.encode())

            if self.attempt_type == "<LOGIN>":
                print("User info -----------------------")
                print(f"Email: {u_email}")
                print(f"Password: {u_password}")
                print("---------------------------------")

                field_dict = {
                    'email': u_email,
                    'password': u_password
                }

                self.client_socket.send(pickle.dumps(field_dict))

                self.server_login_ans = self.client_socket.recv(1024).decode()
                print(f"answer: {self.server_login_ans}")

                if self.server_login_ans == "<NO_EMAIL_EXISTS>":
                    self.ans_email.configure(text="Login failed. No accounts under the provided email.",
                                             text_color="#FF0000")
                    self.ans_password.configure(text="Login failed. Password doesn't match the provided email.",
                                                text_color="#FF0000")
                elif self.server_login_ans == "<WRONG_PASSWORD>":
                    self.ans_password.configure(text="Login failed. Password doesn't match the provided email.",
                                                text_color="#FF0000")
                else:
                    self.l_confirm.configure(text=f"Welcome back {self.server_login_ans}")
                    self.auth_completed = True
