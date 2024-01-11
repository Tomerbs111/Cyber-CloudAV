import tkinter as tk
from customtkinter import *
from tkinter import filedialog as fd
import os
from datetime import datetime


# create the root window
root = CTk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')


def format_file_size(file_size_bytes):
    if file_size_bytes < 1024:
        return f"{file_size_bytes} bytes"
    elif file_size_bytes < 1024 ** 2:
        return f"{file_size_bytes / 1024:.2f} KB"
    elif file_size_bytes < 1024 ** 3:
        return f"{file_size_bytes / (1024 ** 2):.2f} MB"
    else:
        return f"{file_size_bytes / (1024 ** 3):.2f} GB"


def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Select a file',
        initialdir='/',
        filetypes=filetypes)

    file_size = format_file_size(os.path.getsize(filename))
    file_date = datetime.now().strftime("%m/%d/%Y")


btn_fd = CTkButton(
    master=root,
    text="select a file",
    command=select_file
)
ans = CTkLabel(
    master=root,
    text=""
)

btn_fd.pack()
ans.pack()

# run the application
root.mainloop()
