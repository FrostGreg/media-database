import tkinter as tk
from tkinter import ttk
from .style import Style


class AddRecord:
    def __init__(self, file, menu):
        self.file = file
        self.menu = menu
        self.width = 500
        self.height = 400
        self.top = tk.Toplevel()
        self.top.title("Media Database - Add Record")
        self.top.geometry("%dx%d" % (self.width, self.height))
        self.top.configure(bg=Style.bg)
        # creates the form
        self.title = tk.Label(self.top,
                              text="Add New Record",
                              bg=Style.table_top,
                              fg="white",
                              font=("Courier", Style.font_size),
                              borderwidth=2,
                              relief="ridge")
        self.title.grid(row=1, column=1, pady=20, columnspan=2)

        self.type_lbl = tk.Label(self.top, text="Type of Media:", bg=Style.bg, font=("calibri"))
        self.type_lbl.grid(column=1, row=2)

        self.invalid = tk.IntVar()
        self.invalid.set(3)  # deselects any radio button
        media_types = [("DVD", "1"),
                       ("CD", "2"),
                       ("GAME", "3")]  # shows the name of radio button and the value of each
        i = 3  # sets the minimum row height of the radio button
        for val, types in enumerate(media_types):  # for every media type loop
            tk.Radiobutton(self.top,
                           text=types,
                           padx=20,
                           variable=self.invalid,
                           bg=Style.bg,
                           value=val).grid(row=i, column=1)  # creates a radio button placed at i value
            i += 1  # increments i so next radio button is placed below it

        self.author_lbl = tk.Label(self.top, text="Name of Author: ", bg=Style.bg, font=("calibri"))
        self.media_lbl = tk.Label(self.top, text="Name of Media: ", bg=Style.bg, font=("calibri"))
        self.date_lbl = tk.Label(self.top, text="Release Date: ", bg=Style.bg, font=("calibri"))

        self.author_entry = tk.Entry(self.top)
        self.media_entry = tk.Entry(self.top)
        self.date_entry = tk.Entry(self.top)  # creates entry boxes

        self.author_lbl.grid(row=6, column=1, pady=20)
        self.author_entry.grid(row=7, column=1, padx=40)

        self.media_lbl.grid(row=2, column=2)
        self.media_entry.grid(row=4, column=2)

        self.date_lbl.grid(row=6, column=2)
        self.date_entry.grid(row=7, column=2, padx=90)

        self.submit = ttk.Button(self.top, text="Submit", command=self.submit_record, style="C.TButton")
        self.submit.grid(row=8, column=2, pady=40)

        self.submit_lbl = tk.Label(self.top, text=" ", bg=Style.bg, font=("calibri"))
        self.submit_lbl.grid(column=1, row=8)

    def submit_record(self):
        if self.create_record():  # creates the record in the database
            self.submit_lbl.configure(text="Record Submitted \nPlease close the window")  # feedback for user
            self.menu.refresh_btn()
            self.top.destroy()

    def get_values(self):
        # gets the current value of each input
        media_type = self.invalid.get()
        media_type = self.file.type_convert(media_type, "numToChar")
        name = self.media_entry.get()
        author = self.author_entry.get()
        date = self.date_entry.get()
        return media_type, name, author, date

    def validate_input(self):
        valid = False  # resets the validity check
        attributes = self.get_values()
        for x in attributes[:3]:
            if len(x) == 0:  # if nothing in entry box
                self.submit_lbl.configure(
                    text="*Please make sure all\nentry boxes are filled")  # say nothing in entry box
                break
        else:
            valid = True

        # Checks if date is a valid integer
        try:
            int(attributes[3])
        except ValueError:
            self.submit_lbl.configure(text="Invalid Date")
            valid = False

        return valid

    def create_record(self):
        if self.validate_input():
            media_type, name, author, date = self.get_values()
            self.file.cursor.execute("INSERT INTO records (name, author, year, type) VALUES (?, ?, ?, ?)",
                                     (name, author, date, media_type))
            self.file.db.commit()
            return True
