import tkinter as tk
from tkinter import ttk
from .style import Style


class EditRecord:
    def __init__(self, file, menu):
        self.file = file
        self.menu = menu
        self.data = self.file.load()
        self.width = 500
        self.height = 400
        self.top = tk.Toplevel()
        self.top.title("Media Database - Edit Record")
        self.top.geometry("%dx%d" % (self.width, self.height))
        self.top.configure(bg=Style.bg)
        # creates the form
        self.title = tk.Label(self.top,
                              text="Edit record",
                              bg=Style.table_top,
                              fg="white",
                              font=("Courier", Style.font_size),
                              borderwidth=2,
                              relief="ridge")
        self.title.grid(row=1, column=2, pady=20)

        self.record_lbl = tk.Label(self.top, text="Enter the record ID you want to edit", bg=Style.bg, font=("calibri"))
        self.check_ID = tk.Entry(self.top)
        self.load_ID = ttk.Button(self.top, text="Load", command=self.load_record)
        self.record_lbl.grid(row=2, column=2)
        self.check_ID.grid(row=3, column=2)
        self.load_ID.grid(row=3, column=3)

        self.invalid = tk.IntVar()
        self.invalid.set(4)  # deselects the radio buttons
        media_types = [("DVD", "1"),
                       ("CD", "2"),
                       ("GAME", "3")]  # defines the buttons name and value
        i = 5  # sets minimum height for button height
        for val, types in enumerate(media_types):  # for every media type loop
            tk.Radiobutton(self.top,
                           text=types,
                           padx=10,
                           variable=self.invalid,
                           bg=Style.bg,
                           value=val).grid(row=i, column=2)  # creates the button and places it at i height
            i += 1  # increases the height of i

        self.type_lbl = tk.Label(self.top, text="Media Type: ", bg=Style.bg, font=("calibri"))
        self.type_lbl.grid(row=4, column=2)

        self.name_lbl = tk.Label(self.top, text="Name of media: ", bg=Style.bg, font=("calibri"))
        self.media_name = tk.Entry(self.top)
        self.name_lbl.grid(row=8, column=1)
        self.media_name.grid(row=9, column=1, padx=5)

        self.author_lbl = tk.Label(self.top, text="Author: ", bg=Style.bg, font=("calibri"))
        self.author = tk.Entry(self.top)
        self.author_lbl.grid(row=8, column=2)
        self.author.grid(row=9, column=2)

        self.date_lbl = tk.Label(self.top, text="Date Published: ", bg=Style.bg, font=("calibri"))
        self.date = tk.Entry(self.top)
        self.date_lbl.grid(row=8, column=3)
        self.date.grid(row=9, column=3)

        self.submit = ttk.Button(self.top, text="Submit", command=self.submit_btn, style="C.TButton")
        self.submit.grid(row=10, column=3, pady=75)

        self.submit_lbl = tk.Label(self.top, text="", bg=Style.bg, font=("calibri"))
        self.submit_lbl.grid(row=10, column=2)

    def submit_btn(self):
        if self.edit_record():  # updates the record with edited information
            self.submit_lbl.configure(text="Record has been Edited\nPlease close this window")  # feedback for user
            self.menu.refresh_btn()
            self.top.destroy()

    def validate_record(self):
        rec_id = self.check_ID.get()
        valid = False
        if len(rec_id) == 0:
            self.submit_lbl.configure(text="Please enter a record")
        else:
            self.submit_lbl.configure(text="")
            try:
                rec_id = int(rec_id)
                if not self.file.cursor.execute("SELECT * FROM records WHERE id = ?;", (rec_id,)):
                    self.submit_lbl.configure(text="Record does not exist")
                else:
                    valid = True
            except ValueError:
                valid = False

        return valid

    def load_record(self):
        rec_id = self.check_ID.get()  # finds the correct file
        if not self.validate_record():  # stops users from trying to find record that isn't there
            self.submit_lbl.configure(text="The record could not be found")  # feedback for user
        else:  # if record was found
            record = self.file.find_record(rec_id).fetchone()  # gets index number
            media_type = self.file.type_convert(self.file.get_type(record), "charToNum")
            self.invalid.set(media_type)
            media = self.file.get_name(record)
            author = self.file.get_author(record)
            date = self.file.get_date(record)  # gets record information

            self.media_name.delete(0, tk.END)  # clears the entry box
            self.media_name.insert(0, media)  # inputs the record information into entry box

            self.author.delete(0, tk.END)
            self.author.insert(0, author)

            self.date.delete(0, tk.END)
            self.date.insert(0, date)

            self.submit_lbl.configure(text="")

    def get_values(self):
        # gets the current value of each input
        rec_id = self.check_ID.get()
        media_type = self.file.type_convert(self.invalid.get(), "numToChar")  # gets the record info
        name = self.media_name.get()
        author = self.author.get()
        date = self.date.get()
        return rec_id, media_type, name, author, date

    def validate_input(self):
        rec_id, media_type, name, author, date = self.get_values()
        valid = False
        for x in [media_type, name, author]:
            if len(x) == 0:  # if nothing in entry box
                self.submit_lbl.configure(
                    text="*Please make sure all\nentry boxes are filled")  # say nothing in entry box
                break
        else:
            valid = True

        # checks rec_id and date are real numbers
        try:
            int(date)
            int(rec_id)
            if self.validate_record():
                valid = True
        except ValueError:
            self.submit_lbl.configure(text="Invalid Integers")
            valid = False

        return valid

    def edit_record(self):
        if self.validate_input():
            rec_id, media_type, name, author, date = self.get_values()
            self.file.cursor.execute("UPDATE records SET name = ?, author = ?, year = ?, type = ? WHERE id = ?;",
                                     (name, author, date, media_type, rec_id))
            self.file.db.commit()

            return True
