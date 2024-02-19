import threading
import ttkbootstrap as ttk
from customtkinter import *
from PIL import Image, ImageTk

from GUI.RegistrationApp import RegistrationApp
from GUI.GroupsPage import GroupsPage
from GUI.HomePage import HomePage


class Page(ttk.Frame):
    def __init__(self, master, switch_frame, communicator, current_frame):
        super().__init__(master)
        self.current_frame = None
        self.master = master
        self.switch_frame = switch_frame
        self.communicator = communicator
        self.current_frame = current_frame

        self.f_data_center = None
        self.f_current_page = None

        self.setup_searchbar_frame()
        self.setup_option_frame()
        self.setup_data_center_frame()
        self.setup_current_page_frame()

    def setup_searchbar_frame(self):
        # Code for setting up the Searchbar frame
        f_searchbar = ttk.Frame(master=self, style="dark")
        f_searchbar.pack(side="top", fill="x")

        cloudav_image = CTkImage(
            light_image=Image.open(r"../GUI/file_icons/only_logo.png"),
            dark_image=Image.open(r"../GUI/file_icons/only_logo.png"),
            size=(75, 75))
        cav_image_lbl = CTkLabel(master=f_searchbar, image=cloudav_image, text="")
        cav_image_lbl.pack(side="left", padx=10)

        search_frame = ttk.Frame(master=f_searchbar, style="dark")
        search_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.3, relheight=0.5)

        search_button = ttk.Button(search_frame, text="Search")
        search_button.pack(side="left", expand=True, fill="x")

        search_entry = ttk.Entry(search_frame, width=70)
        search_entry.pack(side="left", expand=True, fill="x")

        # Profile Photo Placeholder on the Right
        profile_photo_placeholder = ttk.Label(f_searchbar, text="👤", font=("Arial", 30))
        profile_photo_placeholder.pack(side="right", padx=10)

        # Settings Button on the Right
        settings_button = ttk.Button(f_searchbar, text="Settings")
        settings_button.pack(side="right", padx=10)

    def setup_data_center_frame(self):
        # Code for setting up the Data center frame
        self.f_data_center = ttk.Frame(master=self, style="default")
        self.f_data_center.place(rely=0.1, relx=0, relheight=0.9, relwidth=1)

    def setup_option_frame(self):
        # Code for setting up the Option frame
        f_options = ttk.Frame(master=self.f_data_center, style="dark")
        f_options.place(relx=0, rely=0.1, relwidth=0.2, relheight=1)

        CTkButton(
            f_options,
            text="Add",
            image=CTkImage(Image.open("../GUI/file_icons/add_file_plus_icon.png"), size=(30, 30)),
            compound='left',
            command=self.handle_add_file
        ).pack(side='top', pady=20, anchor='w', padx=10)

        ttk.Separator(f_options, orient="horizontal").pack(side='top', fill='x', pady=5, padx=10)

        CTkButton(
            f_options,
            text="Home",
            image=CTkImage(Image.open("../GUI/file_icons/home_icon.png"), size=(20, 20)),
            compound='left',
            command=self.switch_to_home
        ).pack(side='top', pady=5, anchor='w', fill='x', padx=10)

        CTkButton(
            f_options,
            text="Shared",
            image=CTkImage(Image.open("../GUI/file_icons/shared_icon.png"), size=(20, 20)),
            compound='left'
        ).pack(side='top', pady=5, anchor='w', fill='x', padx=10)

        CTkButton(
            f_options,
            text="Favorites",
            image=CTkImage(Image.open("../GUI/file_icons/star_icon.png"), size=(20, 20)),
            compound='left',
        ).pack(side='top', pady=5, anchor='w', fill='x', padx=10)

        CTkButton(
            f_options,
            text="Groups",
            image=CTkImage(Image.open("../GUI/file_icons/group_icon.png"), size=(20, 20)),
            compound='left',
            command=self.switch_to_groups
        ).pack(side='top', pady=5, anchor='w', fill='x', padx=10)

        CTkButton(
            f_options,
            text="Recycle bin",
            image=CTkImage(Image.open("../GUI/file_icons/trash_icon.png"), size=(20, 20)),
            compound='left'
        ).pack(side='top', pady=5, anchor='w', fill='x', padx=10)

        CTkButton(
            f_options,
            text="Log out",
            image=CTkImage(Image.open("../GUI/file_icons/log_out_icon.png"), size=(20, 20)),
            compound='left'
        ).pack(side='top', pady=5, anchor='w', fill='x', padx=10)

        ttk.Label(f_options, text="Storage:").pack(side='top', pady=10, anchor='w', fill='x', padx=10)

    def setup_current_page_frame(self):
        self.f_current_page = ttk.Frame(master=self.f_data_center, style="info")
        self.f_current_page.place(relx=0.21, rely=0.02, relwidth=0.78, relheight=0.96)

    def switch_to_groups(self):
        if self.current_frame.__class__.__name__ != "GroupsPage":
            print("Switching to groups page")
            self.switch_frame("GroupsPage", self.communicator)
        threading.Thread(target=self.current_frame.group_communicator.join_group).start()

    def switch_to_home(self):
        threading.Thread(target=self.current_frame.group_communicator.leave_group).start()
        if self.current_frame.__class__.__name__ != "HomePage":
            print("Switching to home page")
            self.switch_frame("HomePage", self.communicator)

    def handle_add_file(self):
        threading.Thread(target=self.current_frame.handle_add_file).start()


class MyApp(ttk.Window):
    def __init__(self, client_communicator, group_communicator):
        super().__init__(themename="darkly")
        self.geometry("1150x710")
        self.title("Cloud-AV")

        self.current_frame = None
        self.client_communicator = client_communicator
        self.group_communicator = group_communicator
        self.page = Page(self, self.switch_frame, self.client_communicator, self.current_frame)

        self.switch_frame("RegistrationApp", self.client_communicator)

    def switch_frame(self, frame_class, *args):
        if frame_class == "RegistrationApp":
            new_frame = RegistrationApp(self, self.switch_frame, self.client_communicator)

            if self.current_frame:
                self.current_frame.pack_forget()

            new_frame.pack(fill="both", expand=True)
            self.current_frame = new_frame

        elif frame_class == "GroupsPage":
            new_frame = GroupsPage(self.page.f_current_page, self.switch_frame, self.group_communicator)

            if self.current_frame:
                self.current_frame.pack_forget()

            self.page.pack(fill="both", expand=True)
            new_frame.pack(fill="both", expand=True)

            self.page.current_frame = new_frame
            self.current_frame = new_frame

            new_frame.set_on_broadcast_callback(self.group_communicator.on_broadcast_callback)


        elif frame_class == "HomePage":
            new_frame = HomePage(self.page.f_current_page, self.switch_frame, self.client_communicator)

            if self.current_frame:
                self.current_frame.pack_forget()

            self.page.pack(fill="both", expand=True)
            new_frame.pack(fill="both", expand=True)

            self.page.current_frame = new_frame
            self.current_frame = new_frame
