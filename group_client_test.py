import secrets
import smtplib
import string
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
    def __init__(self, master, email):
        super().__init__(master)
        self.master = master
        self.email = email
        self.email = email

        self.verification_pass = self.send_email(self.email)
        self.setup_image()
        self.setup_information()
        self.setup_verification_code_frame()
        self.setup_submit_button()

    def setup_image(self):
        container = tk.Frame(master=self)
        container.pack(side="top", padx=20)
        two_fa_image = CTkImage(
            light_image=Image.open(r"GUI\file_icons\2fa_image.jpg"),
            dark_image=Image.open(r"GUI\file_icons\2fa_image.jpg"),
            size=(251, 173)
        )
        image_label = CTkLabel(container, image=two_fa_image, text="", bg_color='transparent')
        image_label.pack(side="top", fill="both", expand=True)

    def setup_information(self):
        container = CTkFrame(master=self)
        container.pack(side="top", fill="both", padx=20)
        CTkLabel(container, text="Two-Factor\nAuthentication", font=("Arial Bold", 30), bg_color='transparent').pack(
            side="top", anchor="center", pady=30)
        CTkLabel(container, text="Enter the six-digit code we have sent to your email", font=("Helvetica", 12),
                 bg_color='transparent').pack(side="top",
                                              anchor="center", pady=10)

    def setup_verification_code_frame(self):
        code_frame = CTkFrame(self)
        code_frame.pack(side="top", fill="both", padx=20, pady=20, expand=True)

        self.code_entries = []
        for i in range(6):
            digit_entry = CTkEntry(code_frame, width=50, height=50, font=("Helvetica", 20), justify="center")
            digit_entry.pack(side="left", padx=15, expand=True)

            # Bind the <Key> event to move the focus to the next digit_entry widget
            digit_entry.bind('<Key>', lambda event, entry=digit_entry, index=i: self.on_key(event, entry, index))

            self.code_entries.append(digit_entry)

    def on_key(self, event, entry, index):
        if event.char.isdigit() and index < 5:
            self.code_entries[index + 1].focus_set()

    def setup_submit_button(self):
        container_frame = CTkFrame(self)
        container_frame.pack(side="bottom", fill="both", padx=20, pady=20)
        submit_button = CTkButton(container_frame, text="Verify", command=self.on_submit, font=("Helvetica", 20))
        submit_button.pack(side="top", pady=10, anchor="center", fill='x', padx=10)

        self.answer_label = CTkLabel(container_frame, text="", text_color="red")

    def on_submit(self):
        if self.code_entries == self.verification_pass:
            print("gay")

    def send_email(self, u_email):
        characters = string.digits

        # Generate a random password of the specified length
        password = ''.join(secrets.choice(characters) for i in range(6))
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login('cloudav03@gmail.com', 'CloudAV1234')
            message = f'Subject: makore msg\n\nyour password is {password}'
            server.sendmail('makore616@gmail.com', u_email, message)
            # server.quit()
            print("Email sent successfully!")

            return password
        except Exception as e:
            print(e)
            print("Email failed to send.")


def run_test():
    root = tk.Tk()
    email = "chairgood1@gmail.com"

    # Create an instance of TwoFactorAuthentication
    two_factor_auth = TwoFactorAuthentication(root, email)

    # Run the Tkinter main loop
    root.mainloop()


# Run the test
if __name__ == "__main__":
    run_test()
