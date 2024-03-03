import tkinter as tk
import ttkbootstrap as ttk
from customtkinter import CTkToplevel, CTkFrame, CTkEntry, CTkLabel, CTkButton, CTkScrollableFrame


class CreateGroupWin(CTkToplevel):
    def __init__(self, master, participant_names):

        super().__init__(master)
        self.geometry("500x500")
        self.title("Create New Group")

        self.group_name = tk.StringVar(value="")

        self.selected_participants = {}
        self.participant_names = participant_names
        self.selected_name = None
        self.group_name_error_label = None
        self.participants_error_label = None

        ttk.Label(self, text="Create your shared file group", font=("Calibri bold", 22)
                  ).pack(anchor='w', padx=5, pady=15, fill='x')

        self.setup_group_name_entry()
        self.setup_participants_list()
        self.setup_buttons()

    def setup_group_name_entry(self):
        container = CTkFrame(self)
        container.pack(fill="both", expand=True, padx=5, pady=5)
        CTkLabel(container, text="Group Name:").pack(anchor='w', padx=10, pady=5)
        self.group_name_entry = CTkEntry(container, textvariable=self.group_name, width=200)
        self.group_name_entry.pack(anchor='w', padx=10)

        # Error label for Group Name entry
        self.group_name_error_label = CTkLabel(container, text="", text_color="red")
        self.group_name_error_label.pack(anchor='w', padx=10)

    def setup_participants_list(self):
        participants_list = CTkScrollableFrame(self, label_anchor="w", label_text="Participants:",
                                               label_fg_color='transparent')
        participants_list.pack(fill="both", expand=True, padx=5)

        for name in self.participant_names:
            participant_var = ttk.StringVar(value="off")
            self.selected_participants[name] = participant_var

            participants_container = CTkFrame(participants_list)
            participants_container.pack(fill='x', expand=True)

            checkbox = ttk.Checkbutton(participants_container, text="", variable=participant_var,
                                       onvalue="on", offvalue="off")
            checkbox.pack(side='left', padx=5, pady=5)
            participant_label = ttk.Label(participants_container, text=name)
            participant_label.pack(anchor='w', fill='x', expand=True, pady=5)

        # Error label for Participants list
        self.participants_error_label = CTkLabel(participants_list, text="", text_color="red")
        self.participants_error_label.pack(anchor='w', padx=5, pady=5)

    def setup_buttons(self):
        container = CTkFrame(self, bg_color='transparent')
        container.pack(fill="x", expand=True, padx=5, pady=5, side="bottom")

        submit_button = CTkButton(container, text="Submit", width=20, command=self.on_submit)
        submit_button.pack(side="left", padx=5)

        cancel_button = CTkButton(container, text="Cancel", width=20)
        cancel_button.pack(side="left", padx=5)

    def on_submit(self):
        # Clear previous error messages
        self.group_name_error_label.configure(text="")
        self.participants_error_label.configure(text="")

        # Validate Group Name
        group_name = self.group_name.get()
        if not group_name:
            self.group_name_error_label.configure(text="Please enter a group name.")
            return

        self.selected_name = group_name
        # Validate at least one participant is selected
        selected_participants = [name for name, var in self.selected_participants.items() if var.get() == "on"]
        if not selected_participants:
            self.participants_error_label.configure(text="Please select at least one participant.")
            return

        print(f"Group Name: {self.selected_name}")
        print(f"Selected Participants: {selected_participants}")
        self.destroy()

    def on_cancel(self):
        self.destroy()


def main():
    root = tk.Tk()
    app = CreateGroupWin(root, ["Alice", "Bob", "Charlie"])
    app.mainloop()


if __name__ == "__main__":
    main()
