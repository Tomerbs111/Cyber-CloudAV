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

        lu_filename = ttk.Label(
            master=self,
            text=self.fname
        )
        lu_filename.pack(side='left', padx=30)

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

        self.check_var = customtkinter.StringVar(value="off")
        self.mark_for_action = ttk.Checkbutton(self, text="",
                                               variable=self.check_var, onvalue="on", offvalue="off")
        self.mark_for_action.pack(side='left')

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
        self.f_file_tags = None
        self.f_file_list = None
        self.file_frames = []  # List to store FileFrame instances
        self.file_frame_counter = 0
        self.save_path = None

        # Call the setup functions
        self.setup_action_frame()
        self.setup_data_center_frame()
        self.setup_option_frame()
        self.setup_file_tags_frame()
        self.setup_file_list_frame()

        narf_thread = threading.Thread(target=self.notify_and_receive_files)
        narf_thread.start()

    def notify_and_receive_files(self):
        for individual_file in self.client_communicator.notify_and_receive_files():
            file_name, file_bytes, file_date = individual_file

            short_filename, formatted_file_size, short_file_date = \
                self.prepare_for_display(file_name, file_bytes, file_date)  # a func from Gui_CAV.py

            self.add_file_frame(short_filename, formatted_file_size, short_file_date)  # a func from Gui_CAV.py



    def setup_action_frame(self):
        # Code for setting up the Action frame
        f_actions = ttk.Frame(master=self)
        f_actions.place(x=0, y=0, relheight=0.1, relwidth=1)
        ttk.Button(self, text="Logout").pack(expand=True, fill='both')

    def setup_data_center_frame(self):
        # Code for setting up the Data center frame
        self.f_data_center = ttk.Frame(master=self)
        self.f_data_center.place(rely=0.1, x=0, relheight=0.9, relwidth=1)

    def setup_option_frame(self):
        # Code for setting up the Option frame
        f_options = ttk.Frame(master=self.f_data_center)
        f_options.place(x=0, y=0, relwidth=0.2, relheight=1)
        ttk.Label(master=f_options, text="f_options").pack(expand=True, fill='both')

    def setup_file_tags_frame(self):
        # Code for setting up the File tags frame
        self.f_file_tags = ttk.Frame(master=self.f_data_center)
        self.f_file_tags.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.13)

        add_file_btn = (ttk.Button(master=self.f_file_tags, text="add file", command=self.add_file)
                        .pack(fill='x'))

        process_checked_file_frames = (ttk.Button(master=self.f_file_tags, text="get results",
                                                  command=self.receive_checked_files).pack(fill='x'))

    def setup_file_list_frame(self):
        # Code for setting up the File list frame
        self.f_file_list = ScrolledFrame(master=self.f_data_center, autohide=True, bootstyle='solar')
        self.f_file_list.place(relx=0.2, rely=0.13, relwidth=0.8, relheight=0.87)

        ttk.Label(master=self.f_file_tags, text="Name").pack(side='left', padx=30)
        ttk.Label(master=self.f_file_tags, text="Size").pack(side='right', padx=50)
        ttk.Label(master=self.f_file_tags, text="Upload date").pack(side='right', padx=25)

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
                target=self.client_communicator.send_file(file_name, short_filename, formatted_file_size,
                                                          short_file_date,
                                                          file_bytes))
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
        dialog = customtkinter.CTkInputDialog(text="Write the path you want to save your files on:",
                                              title="Get save path")
        input_path = dialog.get_input()

        if input_path:
            # Normalize the path to handle potential issues with backslashes
            self.save_path = os.path.normpath(input_path)
        else:
            # Use the default Downloads folder
            self.save_path = os.path.join(os.path.expanduser("~"), "Downloads")