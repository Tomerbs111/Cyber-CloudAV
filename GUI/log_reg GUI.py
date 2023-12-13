from customtkinter import *
import re

app = CTk()
app.geometry("700x500")


def when_submit():
    checksum = 0
    u_email = email_entry.get()
    if len(u_email) > 0 and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', u_email):
        ans_email.configure(text="Email is valid.", text_color="#00ff00")
        checksum += 1
    else:
        ans_email.configure(text="Invalid email. Please enter a valid email.", text_color="#FF0000")
        checksum -= 1 if checksum != 0 else 0

    u_username = username_entry.get()
    if len(u_username) >= 6:
        ans_username.configure(text="Username is valid", text_color="#00ff00")
        checksum += 1

    else:
        ans_username.configure(text="Invalid username. must 6 characters or longer.", text_color="#FF0000")
        checksum -= 1 if checksum != 0 else 0

    u_password = password_entry.get()
    if len(u_password) > 0 and len(u_password) >= 8:
        ans_password.configure(text="Password is valid", text_color="#00ff00")
        checksum += 1
    else:
        ans_password.configure(text="Invalid password. must be 8 characters or longer.", text_color="#FF0000")
        checksum -= 1 if checksum != 0 else 0

    if checksum == 3:
        l_confirm.configure(text="User Registered successfully")


# ----------------welcome----------------
set_appearance_mode("system")
welcome = CTkLabel(
    master=app,
    text="Welcome to CloudAV",
    font=("Calibri bold", 35)
)
welcome.place(relx=0.02, rely=0.05)

# ----------------email----------------
l_email = CTkLabel(
    master=app,
    text="Email",
    font=("Calibri", 15)
)
l_email.place(relx=0.02, rely=0.15)
email_entry = CTkEntry(
    master=app,
    placeholder_text="example@example.com",
    width=300,
)
email_entry.place(relx=0.02, rely=0.2)
ans_email = CTkLabel(
    master=app,
    text=""
)
ans_email.place(relx=0.02, rely=0.255)

# ----------------username----------------
l_username = CTkLabel(
    master=app,
    text="Username",
    font=("Calibri", 15)
)
l_username.place(relx=0.02, rely=0.3)
username_entry = CTkEntry(
    master=app,
    placeholder_text="Min. 6 characters",
    width=300
)
username_entry.place(relx=0.02, rely=0.35)
ans_username = CTkLabel(
    master=app,
    text=""
)
ans_username.place(relx=0.02, rely=0.405)

# ----------------password----------------
l_password = CTkLabel(
    master=app,
    text="Password",
    font=("Calibri", 15)
)
l_password.place(relx=0.02, rely=0.45)
password_entry = CTkEntry(
    master=app,
    placeholder_text="Min. 8 characters",
    width=300,
    show="●"
)
password_entry.place(relx=0.02, rely=0.5)
ans_password = CTkLabel(
    master=app,
    text=""
)
ans_password.place(relx=0.02, rely=0.555)

# ----------------register----------------
register_btn = CTkButton(
    master=app,
    text="Register",
    command=when_submit
)
register_btn.place(relx=0.02, rely=0.65)
l_confirm = CTkLabel(
    master=app,
    text="",
    font=("Calibri bold", 20),
    text_color="#00ff00"

)
l_confirm.place(relx=0.02, rely=0.75)
app.mainloop()
