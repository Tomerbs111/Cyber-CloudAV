from customtkinter import *
import re


class RegistrationApp(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x500")
        self.title("Registration App")

        self.registered_email = None
        self.registered_username = None
        self.registered_password = None
        self.toplevel_window = None

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
            show="●"
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
            text="Register",
            command=self.when_submit
        )
        self.submit_btn.place(relx=0.02, rely=0.65)
        self.l_confirm = CTkLabel(
            master=self,
            text="",
            font=("Calibri bold", 20),
            text_color="#00ff00"
        )
        self.login_btn = CTkButton(
            master=self,
            text="Wanna log in?",
            command=self.go_to_login
        )
        self.login_btn.place(relx=0.25, rely=0.65)
        self.l_confirm.place(relx=0.02, rely=0.75)

    def when_submit(self):
        checksum = 0

        u_email = self.email_entry.get()
        if len(u_email) > 0 and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', u_email):
            self.ans_email.configure(text="Email is valid.", text_color="#00ff00")
            checksum += 1
        else:
            self.ans_email.configure(text="Invalid email. Please enter a valid email.", text_color="#FF0000")
            checksum -= 1 if checksum != 0 else 0

        u_username = self.username_entry.get()
        if  self.username_entry:
            if len(u_username) >= 6:
                self.ans_username.configure(text="Username is valid", text_color="#00ff00")
                checksum += 1
            else:
                self.ans_username.configure(text="Invalid username. must be 6 characters or longer.",
                                            text_color="#FF0000")
                checksum -= 1 if checksum != 0 else 0
        else:
            checksum += 1
            pass
            # in the login page

        u_password = self.password_entry.get()
        if len(u_password) > 0 and len(u_password) >= 8:
            self.ans_password.configure(text="Password is valid", text_color="#00ff00")
            checksum += 1
        else:
            self.ans_password.configure(text="Invalid password. must be 8 characters or longer.", text_color="#FF0000")
            checksum -= 1 if checksum != 0 else 0

        if checksum == 3:
            self.l_confirm.configure(text="User Registered successfully")
            self.registered_email = u_email
            self.registered_username = u_username
            self.registered_password = u_password

    def go_to_login(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = LoginApp()
        else:
            self.toplevel_window.focus()

    def get_user_values(self):
        return self.registered_email, self.registered_username, self.registered_password


class LoginApp(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("700x500")
        self.title("Login App")

        self.registered_email = None
        self.registered_username = None
        self.registered_password = None

        # ----------------welcome----------------
        set_appearance_mode("system")
        self.welcome = CTkLabel(
            master=self,
            text="Log into CloudAV",
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

        # ----------------password----------------
        self.l_password = CTkLabel(
            master=self,
            text="Password",
            font=("Calibri", 15)
        )
        self.l_password.place(relx=0.02, rely=0.3)
        self.password_entry = CTkEntry(
            master=self,
            placeholder_text="Min. 8 characters",
            width=300,
            show="●"
        )
        self.password_entry.place(relx=0.02, rely=0.35)
        self.ans_password = CTkLabel(
            master=self,
            text=""
        )
        self.ans_password.place(relx=0.02, rely=0.405)

        # ----------------register----------------
        self.submit_btn = CTkButton(
            master=self,
            text="Log in",
            command=self.when_submit
        )
        self.submit_btn.place(relx=0.02, rely=0.5)
        self.l_confirm = CTkLabel(
            master=self,
            text="",
            font=("Calibri bold", 20),
            text_color="#00ff00"
        )
        self.login_btn = CTkButton(
            master=self,
            text="Wanna log in?",
        )
        self.login_btn.place(relx=0.25, rely=0.5)
        self.l_confirm.place(relx=0.02, rely=0.6)

    def when_submit(self):
        checksum = 0

        u_email = self.email_entry.get()
        if len(u_email) > 0 and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', u_email):
            self.ans_email.configure(text="Email is valid.", text_color="#00ff00")
            checksum += 1
        else:
            self.ans_email.configure(text="Invalid email. Please enter a valid email.", text_color="#FF0000")
            checksum -= 1 if checksum != 0 else 0

        u_password = self.password_entry.get()
        if len(u_password) > 0 and len(u_password) >= 8:
            self.ans_password.configure(text="Password is valid", text_color="#00ff00")
            checksum += 1
        else:
            self.ans_password.configure(text="Invalid password. must be 8 characters or longer.", text_color="#FF0000")
            checksum -= 1 if checksum != 0 else 0

        if checksum == 2:
            self.l_confirm.configure(text="User Registered successfully")
            self.registered_email = u_email
            self.registered_password = u_password