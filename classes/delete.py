import tkinter as tk
from tkinter import ttk
from .style import Style


class DeleteRecord:
    def __init__(self, file):
        self.file = file
        self.width = 500
        self.height = 400
        self.top = tk.Toplevel()
        self.top.title("Media Library - Delete Record")
        self.top.geometry("%dx%d" % (self.width, self.height))
        self.top.configure(bg=Style.bg)
        # creates the form
        self.title = tk.Label(self.top,
                              text="Delete a record",
                              bg=Style.table_top,
                              fg="white",
                              font=("Courier", Style.font_size),
                              borderwidth=2,
                              relief="ridge")
        self.title.grid(row=1, column=2, padx=110, pady=20)

        self.record_lbl = tk.Label(self.top, text="Please enter the record ID that you want to be deleted: ", bg=Style.bg)
        self.record_lbl.grid(row=2, column=2, pady=50)

        self.select_record = tk.Entry(self.top)
        self.select_record.grid(row=3, column=2)

        self.btn_del = ttk.Button(self.top, text="Delete Record", command=self.delete_btn, style="W.TButton")
        self.btn_del.grid(row=4, column=2, pady=20)

        self.delete_lbl = tk.Label(self.top, text=" ", bg=Style.bg, font=("calibri"))
        self.delete_lbl.grid(row=5, column=2)

    def delete_btn(self):
        self.delete_lbl.configure(text="Record has been deleted \nPlease close this window")  # feedback for user
        self.delete_record()  # deletes the record

    def delete_record(self):
        del_req = self.select_record.get()  # gets the user input for what record
        auto_num = self.file.genAutonum()
        if int(del_req) >= auto_num:  # makes sure the record exists
            self.delete_lbl.configure(text="Record could not be found")
        else:  # if record exists
            data = self.file.store()  # store the current file data
            self.file.overwrite()  # clear the file data
            i = 0
            for line in data:
                index = self.file.getIndex(i, data)  # gets index of each line
                if line == "#START#\n":  # ignores the non record lines
                    i += 1
                    continue
                elif line == "\n":
                    i += 1
                    continue
                else:
                    if index == del_req:  # if record id == the requested id
                        i += 1  # skip that line
                        continue
                    else:  # if record id doesnt == the requested id
                        with open("assets/database.txt", "a") as file:
                            file.write("\n" + line)  # skip that line
                        i += 1
