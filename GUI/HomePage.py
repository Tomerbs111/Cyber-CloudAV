import threading
from tkinter import filedialog as fd
import customtkinter
import ttkbootstrap as ttk
from customtkinter import *
from PIL import Image, ImageTk

from GUI.GroupsPage import GroupsPage
import datetime



class FileFrame(ttk.Frame):
    def __init__(self, master, fname, fsize, fdate, favorite_callback=None):
        super().__init__(master)
        self.fname = fname
        self.fsize = fsize
        self.fdate = fdate

        self.check_var = StringVar(value="off")
        self.mark_for_action = ttk.Checkbutton(self, text="",
                                               variable=self.check_var, onvalue="on", offvalue="off")
        self.mark_for_action.pack(side='left', padx=5)

        # Set the default icon path
        icon_path = "../GUI/file_icons/other_file_icon.png"

        # Check file type and set icon accordingly
        if self.is_image(fname):
            icon_path = "../GUI/file_icons/image_file_icon.png"
        elif self.is_document(fname):
            icon_path = "../GUI/file_icons/word_file_icon.png"
        elif self.is_pdf(fname):
            icon_path = "../GUI/file_icons/pdf_file_icon.png"
        elif self.is_powerpoint(fname):
            icon_path = "../GUI/file_icons/powerpoint_file_icon.png"
        elif self.is_text(fname):
            icon_path = "../GUI/file_icons/text_file_icon.png"
        elif self.is_zip(fname):
            icon_path = "../GUI/file_icons/zip_file_icon.png"
        elif self.is_excel(fname):
            icon_path = "../GUI/file_icons/excel_file_icon.png"
        elif self.is_video(fname):
            icon_path = "../GUI/file_icons/video_file_icon.png"
        elif self.is_code(fname):
            icon_path = "../GUI/file_icons/code_file_icon.png"

        # Load the icon image
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize((25, 25))

        tk_icon_image = ImageTk.PhotoImage(icon_image)

        # Create a label to display the icon
        icon_label = ttk.Label(master=self, image=tk_icon_image)
        icon_label.image = tk_icon_image
        icon_label.pack(side='left', padx=(0, 5), pady=5)

        text_size = 12

        self.check_favorite = StringVar(value="off")
        self.favorite_callback = favorite_callback

        self.favorite_button = CTkButton(
            master=self,
            image=CTkImage(Image.open("../GUI/file_icons/star_icon.png"), size=(20, 20)),
            compound='left',
            text="",
            width=30,
            fg_color='transparent',
            command=self.toggle_favorite  # Assign the command to the function
        )

        self.favorite_button.pack(side='right', padx=5, anchor='e')

        # Create labels with larger text
        self.lu_filename = ttk.Label(
            master=self,
            text=self.fname,
            font=("Arial", text_size)
        )
        self.lu_filename.pack(side='left', padx=(0, 5), pady=5, anchor='w')

        # Pack the size label with proper alignment
        self.lu_size = ttk.Label(
            master=self,
            text=self.fsize,
            font=("Arial", text_size)
        )
        self.lu_size.pack(side='right', padx=(0, 27), pady=5, anchor='e')  # Adjust padx as needed

        # Pack the date label with proper alignment
        self.lu_date_mod = ttk.Label(
            master=self,
            text=self.fdate,
            font=("Arial", text_size)
        )
        self.lu_date_mod.pack(side='right', padx=(0, 65), pady=5, anchor='e')

    def toggle_favorite(self):
        current_value = self.check_favorite.get()
        new_value = "on" if current_value == "off" else "off"
        self.check_favorite.set(new_value)

        # Change the button icon based on the new value
        new_icon_path = "../GUI/file_icons/star_icon_light.png" if new_value == "on" else "../GUI/file_icons/star_icon.png"
        new_icon = CTkImage(Image.open(new_icon_path), size=(20, 20))
        self.favorite_button.configure(image=new_icon)

        # Notify the HomePage when the favorite button is pressed
        if self.favorite_callback:
            self.favorite_callback(self, new_value)

    def get_checkvar(self) -> bool:
        return self.check_var.get() == "on"

    def get_filename(self):
        return self.fname

    def set_filename(self, fname):
        self.fname = fname
        self.lu_filename.configure(text=fname)

    def uncheck(self):
        self.check_var.set("off")

    def kill_frame(self):
        self.destroy()

    def is_image(self, fname):
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        return any(fname.lower().endswith(ext) for ext in image_extensions)

    def is_document(self, fname):
        document_extensions = ['.doc', '.docx']
        return any(fname.lower().endswith(ext) for ext in document_extensions)

    def is_pdf(self, fname):
        pdf_extensions = ['.pdf']
        return any(fname.lower().endswith(ext) for ext in pdf_extensions)

    def is_powerpoint(self, fname):
        powerpoint_extensions = ['.ppt', '.pptx', '.pps', '.pot', '.potx', '.ppsx']
        return any(fname.lower().endswith(ext) for ext in powerpoint_extensions)

    def is_text(self, fname):
        text_extensions = ['.txt']
        return any(fname.lower().endswith(ext) for ext in text_extensions)

    def is_zip(self, fname):
        zip_extensions = ['.zip', '.rar', '.7z', '.tar', '.gz']
        return any(fname.lower().endswith(ext) for ext in zip_extensions)

    def is_excel(self, fname):
        excel_extensions = ['.xlsx', '.dbf', '.csv', '.xls', '.xlsm']
        return any(fname.lower().endswith(ext) for ext in excel_extensions)

    def is_video(self, fname):
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.mp3', '.asd']
        return any(fname.lower().endswith(ext) for ext in video_extensions)

    def is_code(self, fname):
        code_extensions = ['.py', '.c', '.cpp', '.java', '.js', '.php', '.css', '.cs']
        return any(fname.lower().endswith(ext) for ext in code_extensions)


class HomePage(ttk.Frame):
    customtkinter.set_appearance_mode("dark")
    def __init__(self, parent, switch_frame, client_communicator):
        super().__init__(parent)
        self.parent_app = parent
        self.switch_frame = switch_frame
        self.client_communicator = client_communicator

        self.f_file_list = None
        self.file_frames = []
        self.file_frame_counter = 0
        self.save_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.rename_button = None
        self.delete_button = None

        self.name_sort_order = 'ascending'  # Keep track of the current sorting order

        self.setup_file_actions_frame()

        narf_thread = threading.Thread(target=self.handle_presenting_presaved_files)
        narf_thread.start()
    def setup_file_actions_frame(self):
        name_frame = ttk.Frame(master=self)
        name_frame.place(relx=0, rely=0, relwidth=1, relheight=0.05)

        CTkLabel(name_frame, text="Home", font=('Arial Bold', 20)).pack(side='top',expand=True, anchor='w', padx=5)

        f_action = ttk.Frame(master=self)
        f_action.place(relx=0, rely=0.05, relwidth=1, relheight=0.05)

        delete_button = CTkButton(
            master=f_action,
            image=CTkImage(Image.open("../GUI/file_icons/trash_icon.png"), size=(20, 20)),
            compound='left',
            text="Delete",
            width=30,
            command=self.handle_delete_request_client,
            fg_color='transparent'
        )
        delete_button.pack(side='left', padx=5)

        download_button = CTkButton(
            master=f_action,
            command=self.handle_download_request_client,
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
            command=self.handle_rename_request_client,
            fg_color='transparent'
        )
        self.rename_button.pack(side='left', padx=5)

        shared_button = CTkButton(
            master=f_action,
            image=CTkImage(Image.open("../GUI/file_icons/shared_icon.png"), size=(20, 20)),
            compound='left',
            text="Share",
            width=30,
            fg_color='transparent'
        )
        shared_button.pack(side='left', padx=5)

        copy_button = CTkButton(
            master=f_action,
            image=CTkImage(Image.open("../GUI/file_icons/copy_icon.png"), size=(20, 20)),
            compound='left',
            text="Copy",
            width=30,
            fg_color='transparent'
        )
        copy_button.pack(side='left', padx=5)

        combined_frame = CTkFrame(master=self)
        combined_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.95)

        f_file_properties = CTkFrame(master=combined_frame, fg_color='transparent')
        f_file_properties.place(relx=0, rely=0, relwidth=1, relheight=0.08)

        CTkButton(master=f_file_properties, text="Name", command=self.sort_by_name).pack(side='left', padx=5)
        CTkButton(master=f_file_properties, text="Size").pack(side='right', padx=10)
        CTkButton(master=f_file_properties, text="Upload date").pack(side='right', padx=10)

        ttk.Separator(combined_frame, orient="horizontal").place(relx=0, rely=0.08, relwidth=1)

        self.f_file_list = CTkScrollableFrame(master=combined_frame, fg_color='transparent')
        self.f_file_list.place(relx=0, rely=0.09, relwidth=1, relheight=0.91)

    def sort_by_name(self):
        # Toggle the sorting order
        if self.name_sort_order == 'ascending':
            self.file_frames.sort(key=lambda x: x.get_filename().lower())
            self.name_sort_order = 'descending'
        else:
            self.file_frames.sort(key=lambda x: x.get_filename().lower(), reverse=True)
            self.name_sort_order = 'ascending'

        # Re-pack the file frames in the scrollable frame
        for file_frame in self.file_frames:
            file_frame.pack_forget()
            file_frame.pack(expand=True, fill='x', side='top')
    @staticmethod
    def set_size_format(file_size_bytes):
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
        for file_frame in self.file_frames:
            if file_frame.get_checkvar():
                checked_file_frames_list.append(file_frame)
                file_frame.uncheck()

        return checked_file_frames_list
    def add_file_frame(self, file_name, file_size, file_date, favorite):
        file_frame = FileFrame(self.f_file_list, file_name, file_size, file_date,
                               favorite_callback=self.handle_favorite_toggle)

        file_frame.pack(expand=True, fill='x', side='top')
        self.file_frames.append(file_frame)
        self.file_frame_counter += 1

        if favorite == 1:
            file_frame.favorite_button.configure(
                image=CTkImage(Image.open("../GUI/file_icons/star_icon_light.png"), size=(20, 20)))
            file_frame.check_favorite.set("on")
    def handle_presenting_presaved_files(self):
        narf_answer = self.client_communicator.handle_presaved_files_client()

        for individual_file in narf_answer:
            (file_name, file_bytes, file_date, favorite) = individual_file

            formatted_file_date = self.set_date_format(file_date)
            formatted_file_size = self.set_size_format(file_bytes)
            self.add_file_frame(file_name, formatted_file_size, formatted_file_date, favorite)

    def handle_send_file_request(self):
        try:
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
                target=self.client_communicator.handle_send_file_request(file_name, short_filename, file_date,
                                                                         file_bytes))
            send_file_thread.start()

            favorite = 0

            self.add_file_frame(short_filename, formatted_file_size, short_file_date, favorite)

        except FileNotFoundError:
            return
    def handle_download_request_client(self):
        select_file_frames = self.get_checked_file_frames()
        select_file_names_lst = [file_frame.get_filename() for file_frame in select_file_frames]

        receive_thread = threading.Thread(
            target=self.client_communicator.handle_download_request_client,
            args=(select_file_names_lst, self.save_path))
        receive_thread.start()
    def handle_favorite_toggle(self, file_frame, new_value):
        file_name = file_frame.get_filename()
        if new_value == "on":
            favorite_thread = threading.Thread(
                target=self.client_communicator.handle_set_favorite_request_client,
                args=(file_name, new_value))
            favorite_thread.start()
        else:
            unfavorite_thread = threading.Thread(
                target=self.client_communicator.handle_set_favorite_request_client,
                args=(file_name, new_value))
            unfavorite_thread.start()
    def handle_rename_request_client(self):
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
                    target=self.client_communicator.handle_rename_request_client,
                    args=((old_name, new_name_with_format),))
                rename_thread.start()

                file_frame.set_filename(new_name_with_format)
                file_frame.update_idletasks()
        except IndexError:
            pass
    def handle_delete_request_client(self):
        frames_to_delete = self.get_checked_file_frames()
        names_to_delete_lst = [file_frame.get_filename() for file_frame in frames_to_delete]

        self.client_communicator.handle_delete_request_client(names_to_delete_lst)
        for file_frame in frames_to_delete:
            file_frame.kill_frame()

        self.file_frame_counter = len(self.file_frames)








