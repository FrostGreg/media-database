import tkinter as tk
from tkinter import ttk
from .style import Style


class EditRecord:
    def __init__(self, file):
        self.file = file
        self.data = self.file.store()
        self.width = 500
        self.height = 400
        self.top = tk.Toplevel()
        self.top.title("Media Library - Edit Record")
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
        self.submit_lbl.configure(text="Record has been Edited\nPlease close this window")  # feedback for user
        self.edit_record()  # updates the record with edited information

    def load_record(self):
        rec_id = self.check_ID.get()  # finds the correct file
        auto_num = self.file.genAutonum()  # gens a new index number to should the last possible record id
        if int(rec_id) >= auto_num:  # stops users from trying to find record that isnt there
            self.submit_lbl.configure(text="The record could not be found")  # feedback for user
        else:  # if record was found
            index = int(self.file.findRecord(rec_id))  # gets index number
            media_type = self.file.getType(index, "update")
            media_type = self.file.typeConvert(media_type, "charToNum")
            int(media_type)
            self.invalid.set(media_type)
            media = self.file.getName(index, "update")
            author = self.file.getAuthor(index, "update")
            date = self.file.getDate(index, "update")  # gets record information

            self.media_name.delete(0, tk.END)  # clears the entry box
            self.media_name.insert(0, media)  # inputs the record information into entry box

            self.author.delete(0, tk.END)
            self.author.insert(0, author)

            self.date.delete(0, tk.END)
            self.date.insert(0, date)

    def edit_record(self):
        rec_id = self.check_ID.get()
        name = self.media_name.get()
        author = self.author.get()
        date = self.date.get()
        media_type = self.invalid.get()
        media_type = self.file.typeConvert(media_type, "numToChar")  # gets the record info
        record = [rec_id, name, author, date, media_type]  # creates a record

        i = 0  # initialises the start of loop
        self.file.overwrite()
        for line in self.data:
            if line == "#START#\n":  # ignores non record lines
                i += 1
                continue
            elif line == "\n":
                i += 1
                continue
            else:  # if line is record
                index = self.file.getIndex(i, self.data)
                if index == rec_id:  # if its the selected record
                    with open("assets/database.txt", "a") as file:
                        file.write("\n" + str(record) + "\n")  # replace old record with new one
                    i += 1
                else:
                    with open("assets/database.txt", "a") as file:
                        file.write("\n" + line)  # rewrite the line
                    i += 1
