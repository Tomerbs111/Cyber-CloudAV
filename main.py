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