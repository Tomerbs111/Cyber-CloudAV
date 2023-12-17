from GUI.reg_gui import *

if __name__ == "__main__":
    reg = RegistrationApp()
    reg.mainloop()
    u_email, u_username, u_password = reg.get_user_values()
    if u_email is not None and u_username is not None and u_password is not None:
        print("Email:", u_email)
        print("Username: ", u_username)
        print("Password:", u_password)



