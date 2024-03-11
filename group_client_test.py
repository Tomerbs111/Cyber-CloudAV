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

from GUI.HomePage import HomePage
from tkvideo import tkvideo


class TwoFactorAuthentication(CTkToplevel):
    def __init__(self, master, email, username, password):
        super().__init__(master)
        self.master = master
        self.email = email
        self.username = username
        self.password = password
        self.email = email

        self.setup_information()
        self.setup_code_area()
        self.setup_submit_button()
        self.setup_video_frame()

    def setup_video_frame(self):
        container = ttk.Frame(master=self)
        container.pack(side="top", fill="both", padx=20, pady=20)

        video_label = ttk.Label(container)
        video_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        script_directory = os.path.dirname(os.path.realpath(__file__))
        video_path = r"C:\Users\shoon\OneDrive - פורטל החינוך פתח תקווה\שולחן העבודה\Cyber-CloudAV\GUI\file_icons\video_2fa.mp4"

        # Create an instance of tkvideo
        video_player = tkvideo(video_path, video_label, loop=1, size=(900, 900))

        # Set the video file path
        video_player.play()

    def setup_information(self):
        container = ttk.Frame(master=self)
        container.pack(side="top", fill="both", padx=20, pady=20)
        ttk.Label(container, text="Two-Factor Authentication").pack(side="top", anchor="center", pady=30)
        ttk.Label(container, text="Enter the six-digit code we have sent to your email").pack(side="top",
                                                                                              anchor="center", pady=10)

    def setup_code_area(self):
        code_frame = ttk.Frame(self)
        code_frame.pack(side="top", fill="both", padx=20, pady=20)

        self.code_entries = []
        for i in range(6):
            entry = ttk.Entry(code_frame, width=3, font=("Helvetica", 20), justify="center")
            entry.grid(row=0, column=i, padx=(5, 5))

            # Bind the <Key> event to move the focus to the next entry widget
            entry.bind('<Key>', lambda event, entry=entry, index=i: self.on_key(event, entry, index))

            self.code_entries.append(entry)

    def on_key(self, event, entry, index):
        if event.char.isdigit() and index < 5:
            self.code_entries[index + 1].focus_set()

    def setup_submit_button(self):
        container_frame = ttk.Frame(self)
        container_frame.pack(side="bottom", fill="both", padx=20, pady=20)
        submit_button = ttk.Button(container_frame, text="Submit", command=self.on_submit)
        submit_button.pack(side="top", pady=10)

        self.answer_label = CTkLabel(container_frame, text="Checking", text_color="red")
        self.answer_label.pack(side="bottom", pady=10)

    def on_submit(self):
        pass


def run_test():
    root = tk.Tk()
    email = "test@example.com"
    username = "test_user"
    password = "test_password"

    # Create an instance of TwoFactorAuthentication
    two_factor_auth = TwoFactorAuthentication(root, email, username, password)

    # Run the Tkinter main loop
    root.mainloop()


# Run the test
if __name__ == "__main__":
    run_test()
