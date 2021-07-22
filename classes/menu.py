import tkinter as tk
from tkinter import ttk
from .style import Style
from .file import File
from .help import Help
from .media_filter import MediaFilter
from .author_filter import AuthorFilter
from .add import AddRecord
from .edit import EditRecord
from .delete import DeleteRecord


class MainMenu:
    def __init__(self, window):
        # creates the menu bar at the top
        self.file = File()
        menu_bar = tk.Menu(window)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Help Page", command=Help)
        file_menu.add_command(label="Exit Program", command=window.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        sort_menu = tk.Menu(menu_bar, tearoff=0)
        sort_menu.add_command(label="Alphabetical(Author)", command=lambda: self.sort_record("author"))
        sort_menu.add_command(label="Alphabetical(Name)", command=lambda: self.sort_record("name"))
        sort_menu.add_command(label="Release Date", command=lambda: self.sort_record("date"))
        sort_menu.add_command(label="Media Type", command=lambda: self.sort_record("type"))
        menu_bar.add_cascade(label="Sort", menu=sort_menu)

        filter_menu = tk.Menu(menu_bar, tearoff=0)
        filter_menu.add_command(label="Media Type",
                                command=lambda: MediaFilter(self.file, self))  # command calls the class
        filter_menu.add_command(label="Author", command=lambda: AuthorFilter(self.file, self))
        menu_bar.add_cascade(label="Filter", menu=filter_menu)

        window.config(menu=menu_bar)

        title = tk.Label(window,
                         text="Your Library",
                         bg=Style.table_top,
                         fg="white",
                         font=("Courier", Style.font_size),
                         borderwidth=2,
                         relief="ridge")
        title.grid(column=2, row=1, pady=10, padx=80)

        style = ttk.Style(window)
        style.theme_use("clam")
        # region "Style"
        # adds style to the widgets
        style.configure("Treeview", font=("Helvetica", 10))

        style.configure("Treeview.Heading", background=Style.table_top, foreground="white",
                        font=("Calibri", 12, "italic"))
        style.map("Treeview.Heading", background=[('active', Style.table_top_act)])

        style.configure('TButton',
                        font=('calibri', 10),
                        borderwidth='4',
                        background=Style.btn_clr,
                        foreground="white")

        style.map('TButton',
                  foreground=[('active', 'white')],
                  background=[('active', Style.btn_clr_act)])

        style.configure("W.TButton",
                        font=('calibri', 10),
                        borderwidth='4',
                        background=Style.btn_del,
                        foreground="white")

        style.map("W.TButton",
                  foreground=[("active", "white")],
                  background=[("active", Style.btn_del_act)])

        style.configure("C.TButton",
                        font=("calibri, 10"),
                        borderwidth="4",
                        background=Style.btn_submit,
                        foreground="white")

        style.map("C.TButton",
                  foreground=[("active", "white")],
                  background=[("active", Style.btn_submit_act)])

        # endregion
        self.table = ttk.Treeview(window)
        self.table["columns"] = ("one", "two", "three", "four")
        self.table.column("#0", width=70)
        self.table.column("one", width=170)
        self.table.column("two", width=170)
        self.table.column("three", width=120)
        self.table.column("four", width=100)

        self.table.heading("#0", text="Index No.", command=self.fill_table)
        self.table.heading("one", text="Media Name", command=lambda: self.sort_record("name"))
        self.table.heading("two", text="Author Name", command=lambda: self.sort_record("author"))
        self.table.heading("three", text="Date", command=lambda: self.sort_record("date"))
        self.table.heading("four", text="Media Type", command=lambda: self.sort_record("type"))
        # lamda used so that function can be called with arguments without it running directly

        self.fill_table()
        self.table.grid(column=2, row=2, rowspan=3)

        self.refresh_lbl = tk.Label(window, text="", bg=Style.bg, font=("calibri", 10))
        self.refresh_lbl.grid(column=2, row=6, pady=10)

        self.photo = tk.PhotoImage(file="assets/refresh.png")
        self.photo_img = self.photo.subsample(15, 15)
        refresh = ttk.Button(window, command=self.refresh_btn, image=self.photo_img)

        refresh.grid(column=2, row=5, pady=5)

        self.but_add = ttk.Button(window, text="Add record",
                                  command=lambda: AddRecord(self.file))  # command calls the class
        self.but_edit = ttk.Button(window, text="Edit Record", command=lambda: EditRecord(self.file))
        self.but_del = ttk.Button(window, text="Delete Record", command=lambda: DeleteRecord(self.file),
                                  style="W.TButton")
        # adds the unique style of the delete button

        self.but_add.grid(column=1, row=2, padx=25)
        self.but_edit.grid(column=1, row=3, padx=25)
        self.but_del.grid(column=1, row=4, padx=25)

        self.owner_lbl = tk.Label(window,
                                  text="Property of and\nDeveloped by Gregory Frost",
                                  font=("calibri", 6),
                                  bg=Style.bg,
                                  fg="white")
        self.owner_lbl.grid(column=1, row=6)

    def refresh_btn(self):
        self.refresh_lbl.configure(text="Table Refreshed")
        self.fill_table()  # refills the table with new information

    def sort_record(self, method):
        self.table.delete(*self.table.get_children())  # clears the table
        data = self.file.store()  # gets the database file
        i = 0
        item = ["", i]
        date_index = list()
        for line in data:
            # ignores non record lines
            if line == "#START#\n":
                i += 1
            elif line == "\n":
                i += 1
            else:
                # adds sorting information into list
                if method == "date":
                    date = self.file.get_date(i, "update")
                    item = [date, i]

                elif method == "author":
                    author = self.file.get_author(i, "update")
                    item = [author, i]

                elif method == "name":
                    name = self.file.get_name(i, "update")
                    item = [name, i]

                elif method == "type":
                    media_type = self.file.get_type(i, "update")
                    item = [media_type, i]

                date_index.append(item)
                i += 1

        final = sorted(date_index, key=lambda x: x[0])  # sorts the records
        ind = 0
        for _ in final:
            # puts the sorted record into the table
            index = final[ind][1]
            name = self.file.get_name(index, "update")
            author = self.file.get_author(index, "update")
            date = self.file.get_date(index, "update")
            media_type = self.file.get_type(index, "update")
            index = int(self.file.get_index(index, "update"))
            self.table.insert("", tk.END, text=index, values=(name, author, date, media_type))
            ind += 1

    def fill_table(self):
        self.table.delete(*self.table.get_children())
        data = self.file.store()
        i = 0
        for lines in data:
            if lines == "#START#\n":
                i += 1
            elif lines == "\n":
                i += 1
            else:
                index = self.file.get_index(i, "update")
                name = self.file.get_name(i, "update")
                author = self.file.get_author(i, "update")
                author = author.title()
                date = self.file.get_date(i, "update")
                media_type = self.file.get_type(i, "update")
                self.table.insert("", i, text=index, values=(name, author, date, media_type))
                i += 1
