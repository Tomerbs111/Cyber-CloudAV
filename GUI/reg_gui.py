from customtkinter import *
import re


class RegistrationApp(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x500")
        self.title("Registration App")

        # ----------------welcome----------------
        set_appearance_mode("system")
        welcome = CTkLabel(
            master=self,
            text="Welcome to CloudAV",
            font=("Calibri bold", 35)
        )
        welcome.place(relx=0.02, rely=0.05)

        # ----------------email----------------
        l_email = CTkLabel(
            master=self,
            text="Email",
            font=("Calibri", 15)
        )
        l_email.place(relx=0.02, rely=0.15)
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
        l_username = CTkLabel(
            master=self,
            text="Username",
            font=("Calibri", 15)
        )
        l_username.place(relx=0.02, rely=0.3)
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
        l_password = CTkLabel(
            master=self,
            text="Password",
            font=("Calibri", 15)
        )
        l_password.place(relx=0.02, rely=0.45)
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
        register_btn = CTkButton(
            master=self,
            text="Register",
            command=self.when_submit
        )
        register_btn.place(relx=0.02, rely=0.65)
        self.l_confirm = CTkLabel(
            master=self,
            text="",
            font=("Calibri bold", 20),
            text_color="#00ff00"
        )
        self.l_confirm.place(relx=0.02, rely=0.75)
        self.login_btn = CTkButton(
            master=self,
            text="Wanna log in?",
        )
        self.login_btn.place(relx=0.25, rely=0.65)

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
        if len(u_username) >= 6:
            self.ans_username.configure(text="Username is valid", text_color="#00ff00")
            checksum += 1
        else:
            self.ans_username.configure(text="Invalid username. must 6 characters or longer.", text_color="#FF0000")
            checksum -= 1 if checksum != 0 else 0

        u_password = self.password_entry.get()
        if len(u_password) > 0 and len(u_password) >= 8:
            self.ans_password.configure(text="Password is valid", text_color="#00ff00")
            checksum += 1
        else:
            self.ans_password.configure(text="Invalid password. must be 8 characters or longer.", text_color="#FF0000")
            checksum -= 1 if checksum != 0 else 0

        if checksum == 3:
            self.l_confirm.configure(text="User Registered successfully")


class LoginApp(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x500")
        self.title("Login App")

        # ----------------welcome----------------
        set_appearance_mode("system")
        welcome = CTkLabel(
            master=self,
            text="Welcome back!",
            font=("Calibri bold", 35)
        )
        welcome.place(relx=0.02, rely=0.05)

        # ----------------email----------------
        l_email = CTkLabel(
            master=self,
            text="Email",
            font=("Calibri", 15)
        )
        l_email.place(relx=0.02, rely=0.15)
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
        l_password = CTkLabel(
            master=self,
            text="Password",
            font=("Calibri", 15)
        )
        l_password.place(relx=0.02, rely=0.3)
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

        # ----------------login----------------
        login_btn = CTkButton(
            master=self,
            text="Login",
            command=self.when_login
        )
        login_btn.place(relx=0.02, rely=0.5)
        self.l_confirm = CTkLabel(
            master=self,
            text="",
            font=("Calibri bold", 20),
            text_color="#00ff00"
        )
        self.l_confirm.place(relx=0.02, rely=0.65)

    def when_login(self):
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
