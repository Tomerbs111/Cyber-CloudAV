import threading
from tkinter import filedialog as fd
from datetime import datetime
import customtkinter
from ttkbootstrap.scrolled import ScrolledFrame
import re
import ttkbootstrap as ttk
from customtkinter import *
from PIL import Image, ImageTk
from datetime import date


class GroupFileFrame(ttk.Frame):
    ICON_PATHS = {
        'image': "../GUI/file_icons/image_file_icon.png",
        'document': "../GUI/file_icons/word_file_icon.png",
        'pdf': "../GUI/file_icons/pdf_file_icon.png",
        'powerpoint': "../GUI/file_icons/powerpoint_file_icon.png",
        'text': "../GUI/file_icons/text_file_icon.png",
        'zip': "../GUI/file_icons/zip_file_icon.png",
        'excel': "../GUI/file_icons/excel_file_icon.png",
        'video': "../GUI/file_icons/video_file_icon.png",
        'code': "../GUI/file_icons/code_file_icon.png",
        'default': "../GUI/file_icons/other_file_icon.png",
    }

    FILE_TYPE_EXTENSIONS = {
        'image': ['.png', '.jpg', '.jpeg', '.gif', '.bmp'],
        'document': ['.doc', '.docx'],
        'pdf': ['.pdf'],
        'powerpoint': ['.ppt', '.pptx', '.pps', '.pot', '.potx', '.ppsx'],
        'text': ['.txt'],
        'zip': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'excel': ['.xlsx', '.dbf', '.csv', '.xls', '.xlsm'],
        'video': ['.mp4', '.avi', '.mkv', '.mov', '.mp3', '.asd'],
        'code': ['.py', '.c', '.cpp', '.java', '.js', '.php', '.css', '.cs'],
    }

    def __init__(self, master, file_name, file_size, file_date, file_owner):
        super().__init__(master)
        self._file_name = file_name
        self.file_size = file_size
        self.file_date = file_date
        self.file_owner = file_owner

        self.check_var = StringVar(value="off")
        self.mark_for_action = ttk.Checkbutton(self, text="", variable=self.check_var, onvalue="on", offvalue="off")
        self.mark_for_action.pack(side='left', padx=5)

        icon_path = self.get_icon_path(file_name)
        tk_icon_image = self.load_icon(icon_path)
        icon_label = ttk.Label(master=self, image=tk_icon_image)
        icon_label.image = tk_icon_image
        icon_label.pack(side='left', padx=(0, 5), pady=5)

        text_size = 12
        self.lu_filename = self.create_label(self._file_name).pack(side='left', padx=(0, 5), pady=5, anchor='w')
        self.lu_size = self.create_label(self.file_size).pack(side='right', padx=(0, 27), pady=5, anchor='e')
        self.lu_date_mod = self.create_label(self.file_date).pack(side='right', padx=(0, 65), pady=5, anchor='e')
        self.lu_owner = self.create_label(self.file_owner).pack(side='right', padx=(0, 65), pady=5, anchor='e')

    @property
    def filename(self):
        return self._file_name

    @filename.setter
    def filename(self, value):
        self._file_name = value
        self.lu_filename.configure(text=value)

    def get_icon_path(self, file_name):
        for file_type, extensions in self.FILE_TYPE_EXTENSIONS.items():
            if any(file_name.lower().endswith(ext) for ext in extensions):
                return self.ICON_PATHS[file_type]
        return self.ICON_PATHS['default']

    def load_icon(self, icon_path):
        icon_image = Image.open(icon_path).resize((25, 25))
        tk_icon_image = ImageTk.PhotoImage(icon_image)
        return tk_icon_image

    def create_label(self, text):
        return ttk.Label(master=self, text=text, font=("Arial", 12))

    def get_checkvar(self) -> bool:
        return self.check_var.get() == "on"

    def set_filename(self, fname):
        self._file_name = fname
        self.lu_filename.configure(text=fname)

    def uncheck(self):
        self.check_var.set("off")

    def kill_frame(self):
        self.destroy()


class GroupsPage(ttk.Frame):
    def __init__(self, parent, switch_frame, client_communicator):
        super().__init__(parent)
        self.parent_app = parent
        self.switch_frame = switch_frame
        self.client_communicator = client_communicator

        self.rename_button = None
        self.f_file_list = None
        self.file_frames = []
        self.file_frame_counter = 0
        self.save_path = os.path.join(os.path.expanduser("~"), "Downloads")

        self.setup_file_actions_frame()

        self.add_file_frame("test", "test", "test", "test")

    def setup_file_actions_frame(self):
        f_action = ttk.Frame(master=self)
        f_action.place(relx=0, rely=0, relwidth=1, relheight=0.05)

        delete_button = CTkButton(
            master=f_action,
            image=CTkImage(Image.open("../GUI/file_icons/trash_icon.png"), size=(20, 20)),
            compound='left',
            text="Delete",
            width=30,
            command=self.handle_delete_file_group,
            fg_color='transparent'
        )
        delete_button.pack(side='left', padx=5)

        download_button = CTkButton(
            master=f_action,
            command=self.handle_download_file_group,
            image=CTkImage(Image.open("../GUI/file_icons/download_icon.png"), size=(20, 20)),
            compound='left',
            text="Download",
            width=30,
            fg_color='transparent'
        )
        download_button.pack(side='left', padx=5)

        self.rename_button = CTkButton(
            master=f_action,
            image=CTkImage(Image.open("../GUI/file_icons/rename_icon.png"), size=(20, 20)),
            compound='left',
            text="Rename",
            width=30,
            command=self.handle_rename_file_group,
            fg_color='transparent'
        )
        self.rename_button.pack(side='left', padx=5)

        combined_frame = CTkFrame(master=self)
        combined_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)

        f_file_properties = CTkFrame(master=combined_frame, fg_color='transparent')
        f_file_properties.place(relx=0, rely=0, relwidth=1, relheight=0.08)

        CTkButton(master=f_file_properties, text="Name").pack(side='left', padx=5)
        CTkButton(master=f_file_properties, text="Size").pack(side='right', padx=10)
        CTkButton(master=f_file_properties, text="Upload date").pack(side='right', padx=10)

        ttk.Separator(combined_frame, orient="horizontal").place(relx=0, rely=0.08, relwidth=1)

        self.f_file_list = CTkScrollableFrame(master=combined_frame, fg_color='transparent')
        self.f_file_list.place(relx=0, rely=0.09, relwidth=1, relheight=0.91)

    def add_file_frame(self, group_file_name, group_file_size, group_file_date, group_file_owner):
        file_frame = GroupFileFrame(self.f_file_list, group_file_name, group_file_size, group_file_date,
                                    group_file_owner)

        file_frame.pack(expand=True, fill='x', side='top')
        self.file_frames.append(file_frame)
        self.file_frame_counter += 1

    def handle_receive_presaved_files(self):
        pass

    def handle_send_file_group(self):
        pass

    def handle_download_file_group(self):
        pass

    def handle_delete_file_group(self):
        pass

    def handle_rename_file_group(self):
        pass

    def handle_group_leave(self):
        pass

    def handle_group_join(self):
        pass
