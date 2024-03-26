import pickle
import threading
from tkinter import filedialog as fd
import ttkbootstrap as ttk
from customtkinter import *
from PIL import Image, ImageTk
import datetime


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
        self.lu_filename = ttk.Label(
            master=self,
            text=self._file_name,
            font=("Arial", text_size)
        )
        self.lu_filename.pack(side='left', padx=(0, 5), pady=5, anchor='w')

        self.lu_size = ttk.Label(
            master=self,
            text=self.file_size,
            font=("Arial", 12)
        )
        self.lu_size.pack(side='right', padx=(0, 27), pady=5, anchor='e')

        self.lu_date_mod = ttk.Label(
            master=self,
            text=self.file_date,
            font=("Arial", 12)
        )
        self.lu_date_mod.pack(side='right', padx=(0, 65), pady=5, anchor='e')

        self.lu_owner = ttk.Label(
            master=self,
            text=self.file_owner,
            font=("Arial", 12)
        )
        self.lu_owner.pack(side='right', padx=(0, 65), pady=5, anchor='e')

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

    def get_filename(self):
        return self._file_name

    def create_label(self, text):
        return ttk.Label(master=self, text=text, font=("Arial", 12))

    def get_checkvar(self) -> bool:
        return self.check_var.get() == "on"

    def set_filename(self, value):
        self._file_name = value
        self.lu_filename.configure(text=self._file_name)

    def uncheck(self):
        self.check_var.set("off")

    def kill_frame(self):
        self.destroy()


class GroupsPage(ttk.Frame):
    def __init__(self, parent, switch_frame, group_communicator, group_name, permissions):
        super().__init__(parent)
        self.parent_app = parent
        self.switch_frame = switch_frame
        self.group_name = group_name
        self.group_communicator = group_communicator
        self.permissions = permissions

        # setting up variables
        self.rename_button = None
        self.f_file_list = None
        self.group_file_frames = []
        self.file_frame_counter = 0
        self.save_path = os.path.join(os.path.expanduser("~"), "Downloads")

        # setting up the frame
        self.setup_group_file_actions_frame()

    def setup_group_file_actions_frame(self):
        name_frame = ttk.Frame(master=self)
        name_frame.place(relx=0, rely=0, relwidth=1, relheight=0.05)

        CTkLabel(name_frame, text=self.group_name, font=('Arial Bold', 20)).pack(side='top',expand=True, anchor='w', padx=5)

        f_action = ttk.Frame(master=self)
        f_action.place(relx=0, rely=0.05, relwidth=1, relheight=0.05)

        delete_button = CTkButton(
            master=f_action,
            image=CTkImage(Image.open("../GUI/file_icons/trash_icon.png"), size=(20, 20)),
            compound='left',
            text="Delete",
            width=30,
            command=self.handle_delete_request_group,
            fg_color='transparent'
        )
        delete_button.pack(side='left', padx=5)

        download_button = CTkButton(
            master=f_action,
            command=self.handle_download_request_group,
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
            command=self.handle_rename_request_group,
            fg_color='transparent'
        )
        self.rename_button.pack(side='left', padx=5)

        combined_frame = CTkFrame(master=self)
        combined_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.95)

        f_file_properties = CTkFrame(master=combined_frame, fg_color='transparent')
        f_file_properties.place(relx=0, rely=0, relwidth=1, relheight=0.08)

        CTkButton(master=f_file_properties, text="Name").pack(side='left', padx=5)
        CTkButton(master=f_file_properties, text="Size").pack(side='right', padx=10)
        CTkButton(master=f_file_properties, text="Upload date").pack(side='right', padx=10)

        ttk.Separator(combined_frame, orient="horizontal").place(relx=0, rely=0.08, relwidth=1)

        self.f_file_list = CTkScrollableFrame(master=combined_frame, fg_color='transparent')
        self.f_file_list.place(relx=0, rely=0.09, relwidth=1, relheight=0.91)

    def set_size_format(self, file_size_bytes):
        if file_size_bytes < 1024:
            return f"{file_size_bytes} bytes"
        elif file_size_bytes < 1024 ** 2:
            return f"{file_size_bytes / 1024:.2f} KB"
        elif file_size_bytes < 1024 ** 3:
            return f"{file_size_bytes / (1024 ** 2):.2f} MB"
        else:
            return f"{file_size_bytes / (1024 ** 3):.2f} GB"

    def set_date_format(self, file_uploadate: datetime):
        time_difference = datetime.datetime.now() - file_uploadate

        # Calculate the time difference in minutes
        minutes_difference = int(time_difference.total_seconds() / 60)

        # Format the short date string based on the time difference
        if minutes_difference < 60:
            short_file_date = f"{minutes_difference} minute ago"
        elif minutes_difference < 24 * 60:
            short_file_date = f"{minutes_difference // 60} hours ago"
        elif minutes_difference < 24 * 60 * 7:
            short_file_date = f"{minutes_difference // (24 * 60)}d"
        else:
            short_file_date = file_uploadate.strftime('%B %d, %Y')

        return short_file_date

    def set_frame_properties_for_display(self, file_name, file_bytes, file_uploadate: datetime):
        short_filename = os.path.basename(file_name)

        formatted_file_size = self.set_size_format(file_bytes)
        short_file_date = self.set_date_format(file_uploadate)

        return short_filename, formatted_file_size, short_file_date

    def get_checked_file_frames(self):
        checked_file_frames_list = []
        for file_frame in self.group_file_frames:
            if file_frame.get_checkvar():
                checked_file_frames_list.append(file_frame)
                file_frame.uncheck()

        return checked_file_frames_list

    def get_and_destroy_checked_file_names(self, names_to_delete_lst):
        for file_frame in self.group_file_frames:
            filename = file_frame.get_filename()
            if filename in names_to_delete_lst:
                file_frame.kill_frame()

        self.file_frame_counter = len(self.group_file_frames)

    def add_file_frame(self, group_file_name, group_file_size, group_file_date, group_file_owner):
        file_frame = GroupFileFrame(self.f_file_list, group_file_name, group_file_size, group_file_date,
                                    group_file_owner)

        file_frame.pack(expand=True, fill='x', side='top')
        self.group_file_frames.append(file_frame)
        self.file_frame_counter += 1

    def get_file_name_to_rename(self, received_data):
        old_name, new_name = received_data
        for file_frame in self.group_file_frames:
            filename = file_frame.get_filename()
            if filename == old_name:
                file_frame.set_filename(new_name)
                file_frame.update_idletasks()

    def handle_presenting_presaved_files(self, received_data):
        for individual_file in received_data:
            owner, name, size, date, group_name = individual_file

            formatted_file_size = self.set_size_format(size)
            formatted_file_date = self.set_date_format(date)
            self.add_file_frame(name, formatted_file_size, formatted_file_date, owner)  # a func from Gui_CAV.py

    def handle_send_file_request(self):
        filetypes = (
            ('All files', '*.*'),
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        file_name = fd.askopenfilename(
            title='Select a file',
            initialdir='/',
            filetypes=filetypes)

        file_bytes = os.path.getsize(file_name)
        file_date = datetime.datetime.now()

        short_filename, formatted_file_size, short_file_date = \
            self.set_frame_properties_for_display(file_name, file_bytes, file_date)

        send_file_thread = threading.Thread(
            target=self.group_communicator.handle_send_file_request,
            args=(file_name, short_filename, file_date, file_bytes)
        )
        send_file_thread.start()

        self.add_file_frame(short_filename, formatted_file_size, short_file_date, group_file_owner="self")

    def handle_download_request_group(self):
        select_file_frames = self.get_checked_file_frames()
        select_file_names_lst = [file_frame.get_filename() for file_frame in select_file_frames]

        receive_thread = threading.Thread(
            target=self.group_communicator.handle_download_request_group,
            args=(select_file_names_lst,))
        receive_thread.start()

    def handle_saving_broadcasted_files(self, file_data_name_dict, save_path):
        for indiv_filename, indiv_filebytes in file_data_name_dict.items():
            file_path = os.path.join(save_path, indiv_filename)
            with open(file_path, "wb") as file:
                file.write(indiv_filebytes)
                print(f"File '{indiv_filename}' received successfully.")

    def handle_delete_request_group(self):
        frames_to_delete = self.get_checked_file_frames()
        names_to_delete_lst = [file_frame.get_filename() for file_frame in frames_to_delete]

        self.delete_thread = threading.Thread(
            target=self.group_communicator.handle_delete_request_group,
            args=(names_to_delete_lst,)
        ).start()
        for file_frame in frames_to_delete:
            file_frame.kill_frame()

        self.file_frame_counter = len(self.group_file_frames)

    def handle_rename_request_group(self):
        try:
            file_frame = self.get_checked_file_frames()[0]
            old_name = file_frame.get_filename()

            file_format = os.path.splitext(old_name)[1]

            new_name_dialog = CTkInputDialog(text=f"Replace {old_name} with:",
                                             title="Rename file")
            new_name = new_name_dialog.get_input()

            if new_name:
                new_name_with_format = f"{new_name}{file_format}"

                rename_thread = threading.Thread(
                    target=self.group_communicator.handle_rename_request_group,
                    args=((old_name, new_name_with_format),))
                rename_thread.start()

                file_frame.set_filename(new_name_with_format)
                file_frame.update_idletasks()
        except IndexError:
            pass

    def set_handle_broadcast_requests_function(self):
        self.group_communicator.handle_broadcast_requests = self.handle_broadcast_requests

    def handle_broadcast_requests(self, pickled_data):
        try:
            try:
                data = pickle.loads(pickled_data)
            except TypeError:
                data = pickled_data

            protocol_flag = data.get("FLAG")
            received_data = data.get("DATA")

            if protocol_flag == "<SEND>":
                for item in received_data:
                    owner, name, size, date, group_name = item
                    self.add_file_frame(name, self.set_size_format(size), date, owner)

            elif protocol_flag == "<NARF>":
                self.handle_presenting_presaved_files(received_data)

            elif protocol_flag == "<DELETE>":
                self.get_and_destroy_checked_file_names(received_data)

            elif protocol_flag == "<RECV>":
                self.handle_saving_broadcasted_files(received_data, self.save_path)

            elif protocol_flag == "<RENAME>":
                self.get_file_name_to_rename(received_data)

        except pickle.UnpicklingError:
            return
