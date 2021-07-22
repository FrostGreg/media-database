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

    def show_record(self, i):
        passed = False  # resets the loop
        index = self.file.get_index(i, "update")  # reopens the file and gathers information
        name = self.file.get_name(i, "update")
        author = self.file.get_author(i, "update")
        date = self.file.get_date(i, "update")
        media_type = self.file.get_type(i, "update")
        items = [index, name, author, date, media_type]  # compiles the info into one record
        for component in items:
            if component == "#START#":
                # ignores the start line of the database file
                passed = False
            else:
                passed = True
        if passed:
            self.main_screen.table.insert("", i, text=index, values=(name, author, date, media_type))
            # if not the first line then add it to the table
