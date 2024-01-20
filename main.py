import tkinter as tk
from tkinter import messagebox
import sqlite3


class LoginPage(tk.Frame):
    def __init__(self, parent, switch_callback):
        super().__init__(parent)
        self.parent = parent
        self.switch_callback = switch_callback

        # Add your login page widgets here
        self.label = tk.Label(self, text="Login Page")
        self.label.pack(pady=10)

        self.login_button = tk.Button(self, text="Login", command=self.on_login)
        self.login_button.pack(pady=10)

    def on_login(self):
        # Check login credentials here
        if self.is_valid_login():
            messagebox.showinfo("Login Successful", "Welcome!")
            self.switch_callback(MainPage)

    def is_valid_login(self):
        # Implement your login validation logic here
        # Return True if login is successful, else False
        return True


class MainPage(tk.Frame):
    def __init__(self, parent, switch_callback):
        super().__init__(parent)
        self.parent = parent
        self.switch_callback = switch_callback

        # Add your main page widgets here
        self.label = tk.Label(self, text="Main Page")
        self.label.pack(pady=10)

        self.logout_button = tk.Button(self, text="Logout", command=self.on_logout)
        self.logout_button.pack(pady=10)

    def on_logout(self):
        print(self.parent)
        self.switch_callback(LoginPage)

    def print_test(self):
        print("Test")


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("Login App")

        self.current_frame = None
        self.switch_frame(LoginPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self, self.switch_frame)

        if self.current_frame:
            self.current_frame.pack_forget()

        new_frame.pack(fill="both", expand=True)
        self.current_frame = new_frame

        # Check if the switched frame is MainPage and call the print_test function
        if frame_class == MainPage:
            new_frame.print_test()


import tkinter as tk
from tkinter import ttk
from time import sleep

teams = range(100)


def button_command():
    # start progress bar
    popup = tk.Toplevel()
    tk.Label(popup, text="Files being downloaded").grid(row=0, column=0)

    progress = 0
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
    progress_bar.grid(row=1, column=0)  # .pack(fill=tk.X, expand=1, side=tk.BOTTOM)
    popup.pack_slaves()

    progress_step = float(100.0 / len(teams))
    for team in teams:
        popup.update()
        sleep(0.1)  # lauch task
        progress += progress_step
        progress_var.set(progress)

    return 0


root = tk.Tk()

tk.Button(root, text="Launch", command=button_command).pack()

root.mainloop()
