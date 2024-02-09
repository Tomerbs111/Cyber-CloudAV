import threading
from tkinter import filedialog as fd
from datetime import date
import customtkinter
import ttkbootstrap as ttk
from customtkinter import *
from PIL import Image, ImageTk

from GUI.GroupsPage import GroupsPage


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
    """
    Initialize the class with the parent, switch_callback, and client_communicator parameters.
    Initialize instance variables for data center, action, file list, file frames, file frame counter, and save path.
    Call setup functions for searchbar frame, data center frame, option frame, action frame, and file management frame.
    Start a new thread to notify and receive files.
    """

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
        self.rename_button = None

        # Call the setup functions
        self.setup_searchbar_frame()
        self.setup_data_center_frame()
        self.setup_option_frame()
        self.setup_action_frame()
        self.setup_file_management_frame()

        narf_thread = threading.Thread(target=self.notify_and_receive_files)
        narf_thread.start()

    def notify_and_receive_files(self):
        narf_answer = self.client_communicator.notify_and_receive_files()
        if narf_answer == "<NO_DATA>":
            return

        else:
            for individual_file in self.client_communicator.notify_and_receive_files():
                (file_name, file_bytes, file_date, favorite) = individual_file

                formatted_file_size = self.format_file_size(file_bytes)  # a func from Gui_CAV.py
                self.add_file_frame(file_name, formatted_file_size, file_date, favorite)  # a func from Gui_CAV.py

    def setup_searchbar_frame(self):
        # Code for setting up the Searchbar frame
        f_searchbar = ttk.Frame(master=self, style="dark")
        f_searchbar.place(relx=0, rely=0, relheight=0.1, relwidth=1)

        # Logo Placeholder on the Left
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
            command=self.delete_checked_file,
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
        self.rename_button = CTkButton(
            master=self.f_action,
            image=CTkImage(Image.open("../GUI/file_icons/rename_icon.png"), size=(20, 20)),
            compound='left',
            text="Rename",
            width=30,
            command=self.rename_checked_file,
            fg_color='transparent'
        )
        self.rename_button.pack(side='left', padx=5)

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

    def setup_file_management_frame(self):
        customtkinter.set_appearance_mode("dark")

        f_file_management = ttk.Frame(master=self.f_data_center)
        f_file_management.place(relx=0.2, rely=0.05, relwidth=0.8, relheight=0.95)

        # Combined frame for file properties and file list
        combined_frame = CTkFrame(master=f_file_management)
        combined_frame.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.92)

        # Buttons for file properties
        f_file_properties = CTkFrame(master=combined_frame, fg_color='transparent')
        f_file_properties.place(relx=0, rely=0, relwidth=1, relheight=0.08)

        CTkButton(master=f_file_properties, text="Name").pack(side='left', padx=5)
        CTkButton(master=f_file_properties, text="Size").pack(side='right', padx=10)
        CTkButton(master=f_file_properties, text="Upload date").pack(side='right', padx=10)

        # Separator
        ttk.Separator(combined_frame, orient="horizontal").place(relx=0.01, rely=0.08, relwidth=0.98)

        # Scrollable frame for file list
        self.f_file_list = CTkScrollableFrame(master=combined_frame, fg_color='transparent')
        self.f_file_list.place(relx=0, rely=0.09, relwidth=1, relheight=0.91)

    # client communication parts in GUI
    def add_file(self):
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

            # getting all the file properties needed for the server to handle
            file_bytes = os.path.getsize(file_name)
            file_date = date.today()

            # formatting all the properties
            short_filename, formatted_file_size, short_file_date = \
                self.prepare_for_display(file_name, file_bytes, file_date)

            send_file_thread = threading.Thread(
                target=self.client_communicator.send_file(file_name, short_filename,
                                                          short_file_date, file_bytes))
            send_file_thread.start()

            favorite = 0

            self.add_file_frame(short_filename, formatted_file_size, short_file_date, favorite)

        except FileNotFoundError:  # in cases of an error
            return

    def add_file_frame(self, file_name, file_size, file_date, favorite):
        file_frame = FileFrame(self.f_file_list, file_name, file_size, file_date,
                               favorite_callback=self.favorite_file_pressed)

        file_frame.pack(expand=True, fill='x', side='top')
        self.file_frames.append(file_frame)  # Add FileFrame instance to the list
        self.file_frame_counter += 1

        if favorite == 1:
            file_frame.favorite_button.configure(
                image=CTkImage(Image.open("../GUI/file_icons/star_icon_light.png"), size=(20, 20)))
            file_frame.check_favorite.set("on")

    def favorite_file_pressed(self, file_frame, new_value):
        file_name = file_frame.get_filename()
        if new_value == "on":
            favorite_thread = threading.Thread(
                target=self.client_communicator.favorite_file,
                args=(file_name, new_value))
            favorite_thread.start()
        else:
            unfavorite_thread = threading.Thread(
                target=self.client_communicator.favorite_file,
                args=(file_name, new_value))
            unfavorite_thread.start()

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

    def prepare_for_display(self, file_name, file_bytes, file_uploadate: date):
        short_filename = os.path.basename(file_name)
        formatted_file_size = self.format_file_size(file_bytes)

        short_file_date = file_uploadate.strftime('%B %d, %Y')

        return short_filename, formatted_file_size, short_file_date

    # Inside the HomePage class

    def checked_file_frames(self):
        """
        :return: Returns a list of checked FileFrame objects.
        """
        checked_file_frames_list = []
        for file_frame in self.file_frames:
            if file_frame.get_checkvar():
                checked_file_frames_list.append(file_frame)
                file_frame.uncheck()

        return checked_file_frames_list

    # Modify the delete_checked_file method accordingly

    def delete_checked_file(self):
        frames_to_delete = self.checked_file_frames()
        names_to_delete_lst = [file_frame.get_filename() for file_frame in frames_to_delete]
        print(names_to_delete_lst)

        self.client_communicator.delete_checked_files(names_to_delete_lst)
        for file_frame in frames_to_delete:
            file_frame.kill_frame()

        # Optional: Update the file frame counter if needed
        self.file_frame_counter = len(self.file_frames)

    # Modify the receive_checked_files method accordingly

    def receive_checked_files(self):
        if self.save_path is None:
            self.get_save_path_dialog()
        else:
            select_file_frames = self.checked_file_frames()
            select_file_names_lst = [file_frame.get_filename() for file_frame in select_file_frames]

            receive_thread = threading.Thread(
                target=self.client_communicator.receive_checked_files,
                args=(select_file_names_lst, self.save_path))
            receive_thread.start()

    def rename_checked_file(self):
        try:
            file_frame = self.checked_file_frames()[0]
            old_name = file_frame.get_filename()

            # Extract the file format from the old name
            file_format = os.path.splitext(old_name)[1]

            new_name_dialog = CTkInputDialog(text=f"Replace {old_name} with:",
                                             title="Rename file")
            new_name = new_name_dialog.get_input()

            if new_name:
                # Append the file format to the new name
                new_name_with_format = f"{new_name}{file_format}"

                # Modify the rename_files call to pass a list of tuples
                rename_thread = threading.Thread(
                    target=self.client_communicator.rename_files,
                    args=((old_name, new_name_with_format),))
                rename_thread.start()

                # Update the file frame label with the new name
                file_frame.set_filename(new_name_with_format)
                file_frame.update_idletasks()  # Ensure the label is updated immediately
        except IndexError:
            pass

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

    def switch_to_groups(self):
        print("Switching to groups page")
        self.switch_callback(GroupsPage, self.client_communicator)
