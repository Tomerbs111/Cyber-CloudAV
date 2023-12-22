from GUI.Registration_GUI import *
from database.Authentication import *

auth = UserAuthentication()


def handle_registration(email, username, password, attempt_type, app_ans):
    print("User info:\n---------------------------------")
    print(f"Email: {email}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print("---------------------------------")
    print(f"\nType: {attempt_type}")

    if attempt_type == "<REGISTER>":
        auth_answer = auth.register(email, username, password)
        print(auth_answer)

        if auth_answer == "<EXISTS>":
            app_ans.ans_email.configure(text="Registration failed. Email is already in use.", text_color="#FF0000")
            app_ans.ans_username.configure(text="Registration failed.", text_color="#FF0000")
            app_ans.ans_password.configure(text="Registration failed.", text_color="#FF0000")
        if auth_answer == "<SUCCESS>":
            app_ans.l_confirm.configure(text="User Registered successfully")

    if attempt_type == "<LOGIN>":
        auth_answer = auth.login(email, password)
        print(f"\n{auth_answer}")

        if auth_answer == "<NO_EMAIL_EXISTS>":
            app_ans.ans_email.configure(text="Login failed. No accounts under the provided email.",
                                        text_color="#FF0000")
            app_ans.ans_password.configure(text="Login failed. Password doesn't match to the provided email.",
                                           text_color="#FF0000")

        elif auth_answer == "<WRONG_PASSWORD>":
            app_ans.ans_password.configure(text="Login failed. Password doesn't match to the provided email.",
                                           text_color="#FF0000")

        else:
            app_ans.l_confirm.configure(text=f"Welcome back {auth_answer}")


if __name__ == "__main__":
    win = RegistrationApp(handle_registration)
    win.mainloop()


