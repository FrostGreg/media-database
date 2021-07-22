import tkinter as tk
from tkinter import ttk
from .style import Style


class Help:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.top = tk.Toplevel()  # creates new form on top of main screen
        self.top.geometry("%dx%d" % (self.width, self.height))  # creates the form
        self.top.title("Media Database - Help Page")
        self.top.configure(bg=Style.bg)
        self.page_num = 0

        self.title = tk.Label(self.top,
                              bg=Style.table_top,
                              text="Help",
                              fg="white",
                              font=("Courier", 30),
                              borderwidth=2,
                              relief="ridge")
        self.title.grid(column=2, row=1, padx=150, pady=20)
        self.subheading = tk.Label(self.top,
                                   text="Home Screen",
                                   bg="black",
                                   fg="white",
                                   font=("courier", (Style.font_size - 7)),
                                   borderwidth=2,
                                   relief="ridge")
        self.subheading.grid(column=2, row=2)

        # defines the image paths
        self.home_img = tk.PhotoImage(file="assets/home-screen-help.png")
        self.add_img = tk.PhotoImage(file="assets/add-screen-help.png")
        self.edit_img = tk.PhotoImage(file="assets/edit-screen-help.png")
        self.del_img = tk.PhotoImage(file="assets/delete-screen-help.png")
        self.sort_img = tk.PhotoImage(file="assets/sort-screen-help.png")
        self.filter_img = tk.PhotoImage(file="assets/filter-screen-help.png")

        self.top.home_img = self.home_img
        self.content = tk.Canvas(self.top, height=420, width=750, bg=Style.bg, highlightthickness=1,
                                 highlightbackground=Style.bg)
        self.content.grid(column=1, row=3, columnspan=3, padx=25, pady=10)
        self.content_img = self.content.create_image(370, 200, image=self.home_img)

        self.btn_next = ttk.Button(self.top, text=">", command=self.next_page)
        self.btn_prev = ttk.Button(self.top, text="<", command=self.prev_page)
        self.page_num_lbl = tk.Label(self.top, bg=Style.bg, text="Page 1/6", font=("courier"))
        self.btn_next.grid(column=3, row=4, padx=50)
        self.btn_prev.grid(column=1, row=4, padx=50)
        self.page_num_lbl.grid(column=2, row=4)

    def next_page(self):
        if self.page_num < 5:
            self.page_num += 1  # increments page number and loops around to the start
        else:
            self.page_num = 0
        self.update_text()

    def prev_page(self):
        if self.page_num > 0:
            self.page_num -= 1  # deincrements the page number loops to the end
        else:
            self.page_num = 5
        self.update_text()

    def show_img(self, new_img):
        self.content.itemconfig(self.content_img, image=new_img)  # changes the image shown

    def update_text(self):
        # updates the text and image based on what page number the help screen is on
        if self.page_num == 0:
            self.subheading.configure(text="Home Screen")
            self.show_img(self.home_img)
            self.page_num_lbl.configure(text="Page 1/6")
        elif self.page_num == 1:
            self.subheading.configure(text="Add Record")
            self.show_img(self.add_img)
            self.page_num_lbl.configure(text="Page 2/6")
        elif self.page_num == 2:
            self.subheading.configure(text="Edit Record")
            self.show_img(self.edit_img)
            self.page_num_lbl.configure(text="Page 3/6")
        elif self.page_num == 3:
            self.subheading.configure(text="Delete Record")
            self.show_img(self.del_img)
            self.page_num_lbl.configure(text="Page 4/6")
        elif self.page_num == 4:
            self.subheading.configure(text="Sorting")
            self.show_img(self.sort_img)
            self.page_num_lbl.configure(text="Page 5/6")
        elif self.page_num == 5:
            self.subheading.configure(text="Filter Table")
            self.show_img(self.filter_img)
            self.page_num_lbl.configure(text="Page 6/6")
