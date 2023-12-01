from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/GUI/Reg_window/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("800x650")
window.configure(bg="#EBEBEB")

canvas = Canvas(
    window,
    bg="#EBEBEB",
    height=650,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    607.0,
    325.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    216.0,
    325.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    216.0,
    98.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    432.0,
    103.0,
    image=image_image_4
)

canvas.create_text(
    42.0,
    36.0,
    anchor="nw",
    text="Join CloudAV\ntoday!",
    fill="#FFFFFF",
    font=("Inter Black", 48 * -1)
)

canvas.create_text(
    60.0,
    427.0,
    anchor="nw",
    text="Password:\n",
    fill="#221B1B",
    font=("Inconsolata Bold", 20 * -1)
)

canvas.create_text(
    60.0,
    236.0,
    anchor="nw",
    text="Email:\n",
    fill="#221A1A",
    font=("Inconsolata Bold", 20 * -1)
)

canvas.create_text(
    60.0,
    327.0,
    anchor="nw",
    text="User name: ",
    fill="#221B1B",
    font=("Inconsolata Bold", 20 * -1)
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    215.0,
    471.0,
    image=image_image_5
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("To_Login.png"))
entry_bg_1 = canvas.create_image(
    215.0,
    469.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#EBEBEB",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=72.0,
    y=454.0,
    width=286.0,
    height=33.0
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    215.0,
    372.0,
    image=image_image_6
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    215.0,
    370.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#EBEBEB",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=72.0,
    y=355.0,
    width=286.0,
    height=33.0
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    215.0,
    281.0,
    image=image_image_7
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    215.0,
    279.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#EBEBEB",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=72.0,
    y=264.0,
    width=286.0,
    height=33.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("Register.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=147.0,
    y=539.0,
    width=135.0,
    height=41.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=92.0,
    y=608.0,
    width=246.0,
    height=42.0
)
window.resizable(False, False)
window.mainloop()
