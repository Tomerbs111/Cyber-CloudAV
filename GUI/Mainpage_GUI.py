from customtkinter import *
import os
from tkinter import filedialog as fd
from datetime import datetime


class MainPage(CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("800x600")

        # ----------------Action frame----------------
        self.f_actions = CTkFrame(master=self.master)
        self.f_actions.place(x=0, y=0, relheight=0.1, relwidth=1)
        self.l1 = CTkLabel(master=self.f_actions, bg_color='red', text="f_actions").pack(expand=True, fill='both')

        # ----------------Data center frame----------------
        self.f_data_center = CTkFrame(master=self.master)
        self.f_data_center.place(rely=0.1, x=0, relheight=0.9, relwidth=1)

        # ----------------Option frame----------------
        self.f_options = CTkFrame(master=self.f_data_center, fg_color="transparent")
        self.f_options.place(x=0, y=0, relwidth=0.2, relheight=1)
        self.l2 = CTkLabel(master=self.f_options, bg_color='blue', text="f_options").pack(expand=True, fill='both')

        # ----------------File tags frame----------------
        self.f_file_tags = CTkFrame(master=self.f_data_center)
        self.f_file_tags.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.06)

        # ----------------File list frame----------------
        self.f_file_list = CTkScrollableFrame(master=self.f_data_center, orientation="vertical")
        self.f_file_list.place(relx=0.2, rely=0.05, relwidth=0.8, relheight=0.95)
        self.l_name = CTkLabel(master=self.f_file_tags, text="Name").pack(side='left', padx=30)
        self.l_size = CTkLabel(master=self.f_file_tags, text="Size").pack(side='right', padx=50)
        self.l_modate = CTkLabel(master=self.f_file_tags, text="Upload date").pack(side='right', padx=25)

        self.add_file_btn = (CTkButton(master=self.f_file_list, text="add file", command=self.select_file)
                             .pack(expand=True, fill='x'))

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

    def select_file(self):
        try:
            filetypes = (
                ('text files', '*.txt'),
                ('All files', '*.*')
            )

            file_name = fd.askopenfilename(
                title='Select a file',
                initialdir='/',
                filetypes=filetypes)

            short_fname = os.path.basename(file_name)
            file_size = self.format_file_size(os.path.getsize(file_name))
            file_date = datetime.now().strftime("%m/%d/%Y")

            self.add_file(short_fname, file_size, file_date)

        except FileNotFoundError:
            return

    def add_file(self, file_name, file_size, file_date):
        file_frame = CTkFrame(master=self.f_file_list)

        lu_filename = CTkLabel(
            master=file_frame,
            text=file_name
        ).pack(side='left', padx=20)

        lu_size = CTkLabel(
            master=file_frame,
            text=file_size
        ).pack(side='right', padx=27)

        lu_date_mod = CTkLabel(
            master=file_frame,
            text=file_date
        ).pack(side='right', padx=43)

        # Pack the file_frame into f_file_list
        file_frame.pack(side='top', fill='x')


if __name__ == "__main__":
    app = MainPage()
    app.mainloop()
