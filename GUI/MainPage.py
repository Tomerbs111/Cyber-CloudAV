import threading
from tkinter import filedialog as fd
from datetime import datetime
import customtkinter
from ttkbootstrap.scrolled import ScrolledFrame
import re
import ttkbootstrap as ttk
from customtkinter import *
from PIL import Image, ImageTk


class FileFrame(ttk.Frame):
    def __init__(self, master, fname, fsize, fdate):
        super().__init__(master)
        self.fname = fname
        self.fsize = fsize
        self.fdate = fdate

        self.check_var = StringVar(value="off")
        self.mark_for_action = ttk.Checkbutton(self, text="",
                                               variable=self.check_var, onvalue="on", offvalue="off")
        self.mark_for_action.pack(side='left', padx=5)

        lu_filename = ttk.Label(
            master=self,
            text=self.fname
        )
        lu_filename.pack(side='left', padx=5)

        lu_size = ttk.Label(
            master=self,
            text=self.fsize
        )
        lu_size.pack(side='right', padx=27)

        lu_date_mod = ttk.Label(
            master=self,
            text=self.fdate
        )
        lu_date_mod.pack(side='right', padx=43)

    def get_checkvar(self) -> bool:
        return self.check_var.get() == "on"

    def get_filename(self):
        return self.fname

    def uncheck(self):
        self.check_var.set("off")


class MainPage(ttk.Frame):
    def __init__(self, parent, switch_callback, client_communicator):
        super().__init__(parent)
        self.parent_app = parent
        self.switch_callback = switch_callback
        self.client_communicator = client_communicator

        # Initialize instance variables
        self.f_data_center = None
        self.f_action = None
        self.f_file_list = None
        self.file_frames = []  # List to store FileFrame instances
        self.file_frame_counter = 0
        self.save_path = None

        # Call the setup functions
        self.setup_searchbar_frame()
        self.setup_data_center_frame()
        self.setup_option_frame()
        self.setup_action_frame()
        self.setup_file_management_frame()

        narf_thread = threading.Thread(target=self.notify_and_receive_files)
        narf_thread.start()

    def notify_and_receive_files(self):
        for individual_file in self.client_communicator.notify_and_receive_files():
            file_name, file_bytes, file_date = individual_file

            short_filename, formatted_file_size, short_file_date = \
                self.prepare_for_display(file_name, file_bytes, file_date)  # a func from Gui_CAV.py

            self.add_file_frame(short_filename, formatted_file_size, short_file_date)  # a func from Gui_CAV.py

    def setup_searchbar_frame(self):
        # Code for setting up the Searchbar frame
        f_searchbar = ttk.Frame(master=self, style="dark")
        f_searchbar.place(relx=0, rely=0, relheight=0.1, relwidth=1)

        # Logo Placeholder on the Left
        cloudav_image = CTkImage(
            light_image=Image.open(
                r"../GUI/file_icons/only_logo.png"),
            dark_image=Image.open(
                r"../GUI/file_icons/only_logo.png"),
            size=(75, 75))
        cav_image_lbl = CTkLabel(master=f_searchbar, image=cloudav_image, text="").pack(side="left", padx=10)

        # Search Entry in the Center
        search_entry = ttk.Entry(f_searchbar, width=60)  # Adjust the width as needed
        search_entry.pack(side="left", fill="both", expand=True, padx=(0, 5))  # Reduced padx

        # Search Button in the Center
        search_button = ttk.Button(f_searchbar, text="Search")
        search_button.pack(side="left", padx=5)  # Reduced padx

        # Profile Photo Placeholder on the Right
        profile_photo_placeholder = ttk.Label(f_searchbar, text="👤", font=("Arial", 14))
        profile_photo_placeholder.pack(side="right", padx=10)

        # Settings Button on the Right
        settings_button = ttk.Button(f_searchbar, text="Settings")
        settings_button.pack(side="right", padx=10)

        # Center the entry widget vertically
        f_searchbar.grid_propagate(False)
        f_searchbar.update_idletasks()
        search_entry.place(in_=f_searchbar, anchor="center", relx=0.5, rely=0.5)

    def setup_data_center_frame(self):
        # Code for setting up the Data center frame
        self.f_data_center = ttk.Frame(master=self, style="dark")
        self.f_data_center.place(rely=0.1, x=0, relheight=0.9, relwidth=1)

    # ... (Previous code)

    def setup_option_frame(self):
        # Code for setting up the Option frame
        f_options = ttk.Frame(master=self, style="dark")
        f_options.place(relx=0, rely=0.1, relwidth=0.2, relheight=1)

        CTkButton(
            f_options,
            text="Add",
            command=self.add_file,
            image=CTkImage(Image.open("../GUI/file_icons/add_file_plus_icon.png"), size=(30, 30)),
            compound='left'
        ).pack(side='top', pady=20, anchor='w', padx=10)

        ttk.Separator(f_options, orient="horizontal").pack(side='top', fill='x', pady=5, padx=10)

        CTkButton(
            f_options,
            text="Home",
            image=CTkImage(Image.open("../GUI/file_icons/home_icon.png"), size=(20, 20)),
            compound='left'
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
            compound='left'
        ).pack(side='top', pady=5, anchor='w', fill='x', padx=10)

        CTkButton(
            f_options,
            text="Groups",
            image=CTkImage(Image.open("../GUI/file_icons/group_icon.png"), size=(20, 20)),
            compound='left'
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

    def setup_action_frame(self):
        # Code for setting up the File tags frame
        self.f_action = ttk.Frame(master=self.f_data_center)
        self.f_action.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.05)

        # Delete Button
        delete_button = CTkButton(
            master=self.f_action,
            image=CTkImage(Image.open("../GUI/file_icons/trash_icon.png"), size=(20, 20)),
            compound='left',
            text="Delete",
            width=30,
            fg_color='transparent'
        )
        delete_button.pack(side='left', padx=5)

        # Download Button
        download_button = CTkButton(
            master=self.f_action,
            command=self.receive_checked_files,
            image=CTkImage(Image.open("../GUI/file_icons/download_icon.png"), size=(20, 20)),
            compound='left',
            text="Download",
            width=30,
            fg_color='transparent'
        )
        download_button.pack(side='left', padx=5)

        # Rename Button
        rename_button = CTkButton(
            master=self.f_action,
            image=CTkImage(Image.open("../GUI/file_icons/rename_icon.png"), size=(20, 20)),
            compound='left',
            text="Rename",
            width=30,
            fg_color='transparent'
        )
        rename_button.pack(side='left', padx=5)

        # Shared Button
        shared_button = CTkButton(
            master=self.f_action,
            image=CTkImage(Image.open("../GUI/file_icons/shared_icon.png"), size=(20, 20)),
            compound='left',
            text="Share",
            width=30,
            fg_color='transparent'
        )
        shared_button.pack(side='left', padx=5)

        # Copy Button
        copy_button = CTkButton(
            master=self.f_action,
            image=CTkImage(Image.open("../GUI/file_icons/copy_icon.png"), size=(20, 20)),
            compound='left',
            text="Copy",
            width=30,
            fg_color='transparent'
        )
        copy_button.pack(side='left', padx=5)

        # Favorite Button
        favorite_button = CTkButton(
            master=self.f_action,
            image=CTkImage(Image.open("../GUI/file_icons/star_icon.png"), size=(20, 20)),
            compound='left',
            text="Favorite",
            width=30,
            fg_color='transparent'
        )
        favorite_button.pack(side='left', padx=5)

    # ...

    def setup_file_management_frame(self):
        f_file_management = ttk.Frame(master=self.f_data_center)
        f_file_management.place(relx=0.2, rely=0.05, relwidth=0.8, relheight=0.95)

        f_file_properties = ttk.Frame(master=f_file_management)
        f_file_properties.place(relx=0, rely=0, relwidth=1, relheight=0.05)

        CTkButton(master=f_file_properties, text="Name").pack(side='left', padx=5)
        CTkButton(master=f_file_properties, text="Size").pack(side='right', padx=27)
        CTkButton(master=f_file_properties, text="Upload date").pack(side='right', padx=47)

        self.f_file_list = ScrolledFrame(master=f_file_management, autohide=False)
        self.f_file_list.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)

    def setup_file_properties_frame(self):
        f_file_properties = CTkFrame(master=self.f_data_center, corner_radius=10)
        f_file_properties.place(relx=0.2, rely=0.05, relwidth=0.79, relheight=0.05)

        self.f_file_list = CTkScrollableFrame(master=self.f_data_center, corner_radius=10)
        self.f_file_list.place(relx=0.2, rely=0.1, relwidth=0.79, relheight=0.88)

    # client communication parts in GUI
    def add_file(self):
        try:
            filetypes = (
                ('text files', '*.txt'),
                ('All files', '*.*')
            )

            file_name = fd.askopenfilename(
                title='Select a file',
                initialdir='/',
                filetypes=filetypes)

            # getting all the file properties needed for the server to handle
            file_bytes = os.path.getsize(file_name)
            file_date = datetime.now()

            # formatting all the properties
            short_filename, formatted_file_size, short_file_date = \
                self.prepare_for_display(file_name, file_bytes, file_date)

            send_file_thread = threading.Thread(
                target=self.client_communicator.send_file(file_name, short_filename,
                                                          short_file_date, formatted_file_size,file_bytes))
            send_file_thread.start()

            self.add_file_frame(short_filename, formatted_file_size, short_file_date)

        except FileNotFoundError:  # in cases of an error
            return

    def receive_checked_files(self):
        if self.save_path is None:
            self.get_save_path_dialog()
        else:
            select_file_names_lst = self.checked_file_frames()
            self.client_communicator.receive_checked_files(select_file_names_lst, self.save_path)

    def add_file_frame(self, file_name, file_size, file_date):
        file_frame = FileFrame(self.f_file_list, file_name, file_size, file_date)

        # Check if the file is an image (you can customize the list of image extensions)
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        is_image = any(file_name.lower().endswith(ext) for ext in image_extensions)

        # Check if the file is a document type (you can customize the list of document extensions)
        document_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx']
        is_document = any(file_name.lower().endswith(ext) for ext in document_extensions)

        # Check if the file is a video type (you can customize the list of video extensions)
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov']
        is_video = any(file_name.lower().endswith(ext) for ext in video_extensions)

        if is_image:
            # Path to the image icon for images (replace with your path)
            icon_path = "../GUI/file_icons/image_icon.png"
        elif is_document:
            # Path to the icon for document types (replace with your path)
            icon_path = "../GUI/file_icons/documents_icon.png"
        elif is_video:
            # Path to the icon for video types (replace with your path)
            icon_path = "../GUI/file_icons/video_icon.png"
        else:
            icon_path = None

        if icon_path:
            # Load the icon image
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((20, 20))  # Adjust the size as needed

            # Convert the image to a format compatible with tkinter
            tk_icon_image = ImageTk.PhotoImage(icon_image)

            # Create a label to display the icon
            icon_label = ttk.Label(master=file_frame, image=tk_icon_image)
            icon_label.image = tk_icon_image
            icon_label.pack(side='left', padx=10)  # Adjust the padding as needed

        file_frame.pack(expand=True, fill='x', side='top')
        self.file_frames.append(file_frame)  # Add FileFrame instance to the list
        self.file_frame_counter += 1

    @staticmethod
    def format_file_size(file_size_bytes):
        if file_size_bytes < 1024:
            return f"{file_size_bytes} bytes"
        elif file_size_bytes < 1024 ** 2:
            return f"{file_size_bytes / 1024:.2f} KB"
        elif file_size_bytes < 1024 ** 3:
            return f"{file_size_bytes / (1024 ** 2):.2f} MB"
        else:
            return f"{file_size_bytes / (1024 ** 3):.2f} GB"

    def prepare_for_display(self, file_name, file_bytes, file_uploadate):
        short_filename = os.path.basename(file_name)
        formatted_file_size = self.format_file_size(file_bytes)

        if isinstance(file_uploadate, datetime):
            short_file_date = datetime.strftime(file_uploadate, "%y/%m/%d")

        elif isinstance(file_uploadate, str):
            original_date = datetime.strptime(file_uploadate, "%Y-%m-%d %H:%M:%S.%f")
            short_file_date = original_date.strftime("%y/%m/%d")

        return short_filename, formatted_file_size, short_file_date

    def checked_file_frames(self):
        """
        :return: Returns a list of filenames for the checked file frames.
        """
        checked_file_frames_list = []
        for file_frame in self.file_frames:
            if file_frame.get_checkvar():
                checked_file_frames_list.append(file_frame.get_filename())
                file_frame.uncheck()  # Uncheck the checkbox

        return checked_file_frames_list

    def get_save_path_dialog(self):
        dialog = CTkInputDialog(text="Write the path you want to save your files on:",
                                title="Get save path")
        input_path = dialog.get_input()

        if input_path:
            # Normalize the path to handle potential issues with backslashes
            self.save_path = os.path.normpath(input_path)
        else:
            # Use the default Downloads folder
            self.save_path = os.path.join(os.path.expanduser("~"), "Downloads")


class MyApp(ttk.Window):
    def __init__(self, client_communicator):
        super().__init__(themename="darkly")
        self.geometry("1150x710")
        self.title("Cloud-AV")

        self.client_communicator = client_communicator
        self.current_frame = None
        self.switch_frame(MainPage, self.client_communicator)

    def switch_frame(self, frame_class, *args):
        new_frame = frame_class(self, self.switch_frame, *args)

        if self.current_frame:
            self.current_frame.pack_forget()

        new_frame.pack(fill="both", expand=True)
        self.current_frame = new_frame


if __name__ == "__main__":
    my_app = MyApp("1")
    my_app.mainloop()
