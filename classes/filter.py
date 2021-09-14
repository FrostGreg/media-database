import tkinter as tk
from tkinter import ttk
from .style import Style


class Filter:
    def __init__(self, file, main_screen):
        self.main_screen = main_screen
        self.file = file
        self.width = 500
        self.height = 250
        self.top = tk.Toplevel()
        self.top.geometry("%dx%d" % (self.width, self.height))
        self.top.configure(bg=Style.bg)
        # creates the new form

        self.title = tk.Label(self.top,
                              text="",
                              bg=Style.table_top,
                              fg="white",
                              font=("Courier", Style.font_size),
                              borderwidth=2,
                              relief="ridge")
        self.title.grid(column=2, row=1, padx=150, pady=20)
        self.filter_lbl = tk.Label(self.top, text="Enter the filter requirements: ", bg=Style.bg, font=("calibri"))
        self.filter_lbl.grid(column=2, row=2)
        self.filter_entry = tk.Entry(self.top)
        self.filter_entry.grid(column=2, row=3, pady=15)
        self.filter_btn = ttk.Button(self.top, text="Filter")
        self.filter_btn.grid(column=2, row=4, pady=20)

    def show_record(self, record):
        index = self.file.get_index(record)  # reopens the file and gathers information
        name = self.file.get_name(record)
        author = self.file.get_author(record)
        date = self.file.get_date(record)
        media_type = self.file.get_type(record)
        self.main_screen.table.insert("", index, text=index, values=(name, author, date, media_type))
        # if not the first line then add it to the table
