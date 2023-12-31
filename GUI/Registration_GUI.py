from customtkinter import *
import packaging
import re


class RegistrationApp(CTk):
    def __init__(self, client_socket):
        super().__init__()
        self.geometry("700x500")
        self.title("Registration App")

        self.auth_completed = False
        self.server_reglog_ans = None
        self.client_socket = client_socket
        self.attempt_type = "<REGISTER>"

        # ----------------welcome----------------
        set_appearance_mode("system")
        self.welcome = CTkLabel(
            master=self,
            text="Welcome to CloudAV",
            font=("Calibri bold", 35)
        )
        self.welcome.place(relx=0.02, rely=0.05)

        # ----------------email----------------
        self.l_email = CTkLabel(
            master=self,
            text="Email",
            font=("Calibri", 15)
        )
        self.l_email.place(relx=0.02, rely=0.15)
        self.email_entry = CTkEntry(
            master=self,
            placeholder_text="example@example.com",
            width=300,
        )
        self.email_entry.place(relx=0.02, rely=0.2)
        self.ans_email = CTkLabel(
            master=self,
            text=""
        )
        self.ans_email.place(relx=0.02, rely=0.255)

        # ----------------username----------------
        self.l_username = CTkLabel(
            master=self,
            text="Username",
            font=("Calibri", 15)
        )
        self.l_username.place(relx=0.02, rely=0.3)
        self.username_entry = CTkEntry(
            master=self,
            placeholder_text="Min. 6 characters",
            width=300
        )
        self.username_entry.place(relx=0.02, rely=0.35)
        self.ans_username = CTkLabel(
            master=self,
            text=""
        )
        self.ans_username.place(relx=0.02, rely=0.405)

        # ----------------password----------------
        self.l_password = CTkLabel(
            master=self,
            text="Password",
            font=("Calibri", 15)
        )
        self.l_password.place(relx=0.02, rely=0.45)
        self.password_entry = CTkEntry(
            master=self,
            placeholder_text="Min. 8 characters",
            width=300,

        )
        self.password_entry.place(relx=0.02, rely=0.5)
        self.ans_password = CTkLabel(
            master=self,
            text=""
        )
        self.ans_password.place(relx=0.02, rely=0.555)

        # ----------------register----------------
        self.submit_btn = CTkButton(
            master=self,
            text="Sign up",
            command=self.r_when_submit
        )
        self.submit_btn.place(relx=0.02, rely=0.65)
        self.l_confirm = CTkLabel(
            master=self,
            text="",
            font=("Calibri bold", 20),
            text_color="#009900"
        )
        self.switch_btn = CTkButton(
            master=self,
            text="Sign in instead?",
            command=self.go_to_login
        )
        self.switch_btn.place(relx=0.25, rely=0.65)
        self.l_confirm.place(relx=0.02, rely=0.75)

    # ----------------checks fields with username----------------
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

                self.client_socket.send(u_email.encode())
                self.client_socket.send(u_username.encode())
                self.client_socket.send(u_password.encode())

                self.server_reglog_ans = self.client_socket.recv(1024).decode()
                print(f"answer: {self.server_reglog_ans}")

                if self.server_reglog_ans == "<EXISTS>":
                    self.ans_email.configure(text="Registration failed. Email is already in use.", text_color="#FF0000")
                    self.ans_username.configure(text="Registration failed.", text_color="#FF0000")
                    self.ans_password.configure(text="Registration failed.", text_color="#FF0000")
                if self.server_reglog_ans == "<SUCCESS>":
                    self.l_confirm.configure(text="User Registered successfully")
                    self.auth_completed = True

    # ----------------checks fields without username----------------
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
        if len(u_password) > 0 and len(u_password) >= 8:
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
                self.client_socket.send(u_email.encode())
                self.client_socket.send(u_password.encode())

                self.server_reglog_ans = self.client_socket.recv(1024).decode()
                print(f"answer: {self.server_reglog_ans}")

                if self.server_reglog_ans == "<NO_EMAIL_EXISTS>":
                    self.ans_email.configure(text="Login failed. No accounts under the provided email.",
                                             text_color="#FF0000")
                    self.ans_password.configure(text="Login failed. Password doesn't match to the provided email.",
                                                text_color="#FF0000")
                elif self.server_reglog_ans == "<WRONG_PASSWORD>":
                    self.ans_password.configure(text="Login failed. Password doesn't match to the provided email.",
                                                text_color="#FF0000")
                else:
                    self.l_confirm.configure(text=f"Welcome back {self.server_reglog_ans}")
                    self.auth_completed = True

    def go_to_login(self):
        self.welcome.configure(text="Sign in to CloudAV")
        self.submit_btn.configure(text="Sign in", command=self.l_when_submit)
        self.switch_btn.configure(text="Sign up instead?")

        self.l_username.destroy()
        self.username_entry.destroy()
        self.ans_username.destroy()

        # Shift the password-related widgets up
        self.l_password.place(rely=0.3)
        self.password_entry.place(rely=0.35)
        self.ans_password.place(rely=0.405)

        # Adjust the position of other widgets
        self.switch_btn.place(rely=0.5)
        self.submit_btn.place(rely=0.5)
        self.l_confirm.place(rely=0.6)

        # Notify the client when switching to login page
        self.attempt_type = "<LOGIN>"
