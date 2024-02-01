import threading
from tkinter import filedialog as fd
from datetime import datetime
import customtkinter
from ttkbootstrap.scrolled import ScrolledFrame
import re
import ttkbootstrap as ttk
from customtkinter import *
from PIL import Image, ImageTk

from GUI.RegistrationApp import RegistrationApp


class MyApp(ttk.Window):
    def __init__(self, client_communicator):
        super().__init__(themename="darkly")
        self.geometry("1150x710")
        self.title("Cloud-AV")

        self.client_communicator = client_communicator
        self.current_frame = None
        self.switch_frame(RegistrationApp, self.client_communicator)

    def switch_frame(self, frame_class, *args):
        new_frame = frame_class(self, self.switch_frame, *args)

        if self.current_frame:
            self.current_frame.pack_forget()

        new_frame.pack(fill="both", expand=True)
        self.current_frame = new_frame
