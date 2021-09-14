import tkinter as tk
from tkinter import ttk
from .style import Style


class DeleteRecord:
    def __init__(self, file):
        self.file = file
        self.width = 500
        self.height = 400
        self.top = tk.Toplevel()
        self.top.title("Media Database - Delete Record")
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
        if self.delete_record():  # deletes the record
            self.delete_lbl.configure(text="Record has been deleted \nPlease close this window")  # feedback for user

    def validate_input(self):
        user_in = self.select_record.get()
        valid = False
        if len(user_in) == 0:
            self.delete_lbl.configure(text="Enter A Record ID")
        else:
            try:
                user_in = int(user_in)
                if not self.file.cursor.execute("SELECT * FROM records WHERE id = ?;", (user_in,)):
                    self.delete_lbl.configure(text="Record does not exist")
                else:
                    valid = True
            except ValueError:
                self.delete_lbl.configure(text="Invalid Record ID")

        return valid

    def delete_record(self):
        if self.validate_input():
            del_rec = self.select_record.get()  # gets the user input for what record
            self.file.cursor.execute("DELETE FROM records WHERE id = ?", (del_rec,))
            self.file.db.commit()
            return True

