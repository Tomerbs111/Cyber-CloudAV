import tkinter as tk
from tkinter import font

root = tk.Tk()
root.title("Custom Fonts in Tkinter")

# Define the file paths for your TTF font files
semi_bold_font_path = "GUI/fonts/Urbanist-SemiBold.ttf"
regular_font_path = "GUI/fonts/Urbanist-Regular.ttf"

# Define font families
semi_bold_font_family = "Urbanist-SemiBold"
regular_font_family = "Urbanist-Regular"

# Load the fonts
try:
    semi_bold_font = font.Font(family=semi_bold_font_family, name=semi_bold_font_family, exists=True, file=semi_bold_font_path)
except tk.TclError:
    print(f"Error loading {semi_bold_font_family} font. Make sure the font file is available.")

try:
    regular_font = font.Font(family=regular_font_family, name=regular_font_family, exists=True, file=regular_font_path)
except tk.TclError:
    print(f"Error loading {regular_font_family} font. Make sure the font file is available.")

# Create a label using the custom fonts
label1 = tk.Label(root, text="Urbanist SemiBold Font", font=semi_bold_font_path, pady=10)
label1.pack()

label2 = tk.Label(root, text="Urbanist Regular Font", font=semi_bold_font_path, pady=10)
label2.pack()

root.mainloop()
