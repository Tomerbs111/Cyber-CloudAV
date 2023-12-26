from customtkinter import *

app = CTk()

f_file_list = CTkScrollableFrame(master=app, orientation="vertical")

f_file = CTkFrame(master=f_file_list).pack(expand=True, side='top', fill='x')
lu_filename = CTkLabel(
    master=f_file_list,
    text="my_file.txt"
).pack(side='left', padx=20)

lu_size = CTkLabel(
    master=f_file_list,
    text="100MB"
).pack(side='right', padx=20)

lu_date_mod = CTkLabel(
    master=f_file_list,
    text="1/10/2023"
).pack(side='right', padx=30)

lu_owner = CTkLabel(
    master=f_file_list,
    text="tomer"
).pack(side='right', padx=30)

app.mainloop()