import tkinter as tk # imports the required modules
from tkinter import ttk

# region "Variables"
bg = "#D7CEC7"
button_colour = "#565C5E"
button_colour_active = "#3e4243"
but_del = "#994848"
but_del_active = "#763838"
but_submit = "#1f8844"
but_submit_active = "#165e2f"
table_top = "#76323F"
table_top_active = "#52232C" # defines the hex code for the colours used
title_font = 20 # the font size of all the titles

# endregion

# Opens the database file and stores the content in the data variable
def store():
    with open("Database.txt", "r") as file:
        data = file.readlines()
    return data

# works through each record until the requested one is found
def findRecord(reqID):
    found = False
    i = 0
    while not found:
        index = getIndex(i, "update")
        if index != reqID:
            i += 1
        else:
            found = True
    return i

# gets the positions of the seperators for each record
def getSeperators(i, data):
    if data == "update":
        data = store()
    line = data[i]
    start = 0
    seperators = list()
    for i in range(10):
        seperators_locations = line.find("\'", start)
        seperators.append(seperators_locations)
        start = seperators_locations + 1
    return line, seperators

# uses the seperators to find the correct information and returns it
def getIndex(i, data):
    line, seperators = getSeperators(i, data)
    index = line[seperators[0] + 1: seperators[1]]
    return index


def getName(i, data):
    line, seperators = getSeperators(i, data)
    name = line[seperators[2] + 1: seperators[3]]
    return name


def getAuthor(i, data):
    line, seperators = getSeperators(i, data)
    author = line[seperators[4] + 1: seperators[5]]
    return author


def getDate(i, data):
    line, seperators = getSeperators(i, data)
    date = line[seperators[6] + 1: seperators[7]]
    return date


def getType(i, data):
    line, seperators = getSeperators(i, data)
    type = line[seperators[8] + 1: seperators[9]]
    return type

# converts media type so it can taken from and put into radio buttons
def typeConvert(type, method):
    if method == "numToChar":
        if type == 0:
            type = "DVD"
        elif type == 1:
            type = "CD"
        elif type == 2:
            type = "GAME"

    elif method == "charToNum":
        if type == "DVD":
            type = 0
        elif type == "CD":
            type = 1
        elif type == "GAME":
            type = 2
    return type

# creates the index for the next record
def genAutonum():
    count = 0
    data = store()
    for line in data:
        count += 1
    finished = False
    lines = store()
    lineno = count - 1
    while not finished:
        if lines[lineno] == "\n":
            lineno -= 1
        else:
            finished = True
    index = getIndex(lineno, "update")
    autonum = int(index) + 1
    return autonum

#clears the file ready for file to be rewritten
def overwrite():
    with open("Database.txt", "w") as file:
        file.write("#START#")


class MainMenu:
    def __init__(self, window):
        #creates the menu bar at the top
        menu_bar = tk.Menu(window)
        filemenu = tk.Menu(menu_bar, tearoff=0)
        filemenu.add_command(label="Help Page", command=Help)
        filemenu.add_command(label="Exit Program", command=window.quit)
        menu_bar.add_cascade(label="File", menu=filemenu)

        sortmenu = tk.Menu(menu_bar, tearoff=0)
        sortmenu.add_command(label="Alphabetical(Author)", command=lambda: self.recordSort("author"))
        sortmenu.add_command(label="Alphabetical(Name)", command=lambda: self.recordSort("name"))
        sortmenu.add_command(label="Release Date", command=lambda: self.recordSort("date"))
        sortmenu.add_command(label="Media Type", command=lambda: self.recordSort("type"))
        menu_bar.add_cascade(label="Sort", menu=sortmenu)

        filtermenu = tk.Menu(menu_bar, tearoff=0)
        filtermenu.add_command(label="Media Type", command=MediaFilter) # command calls the class
        filtermenu.add_command(label="Author", command=AuthorFilter)
        menu_bar.add_cascade(label="Filter", menu=filtermenu)

        window.config(menu=menu_bar)

        title = tk.Label(window,
                         text="Your Library",
                         bg=table_top,
                         fg="white",
                         font=("Courier", title_font),
                         borderwidth=2,
                         relief="ridge")
        title.grid(column=2, row=1, pady=10, padx=80)

        style = ttk.Style(window)
        style.theme_use("clam")
        # region "Style"
        # adds style to the widgets
        style.configure("Treeview", font=("Helvetica", 10))

        style.configure("Treeview.Heading", background=table_top, foreground="white", font=("Calibri", 12, "italic"))
        style.map("Treeview.Heading", background=[('active', table_top_active)])

        style.configure('TButton',
                        font=('calibri', 10),
                        borderwidth='4',
                        background=button_colour,
                        foreground="white")

        style.map('TButton',
                  foreground=[('active', 'white')],
                  background=[('active', button_colour_active)])

        style.configure("W.TButton",
                        font=('calibri', 10),
                        borderwidth='4',
                        background=but_del,
                        foreground="white")

        style.map("W.TButton",
                  foreground=[("active", "white")],
                  background=[("active", but_del_active)])

        style.configure("C.TButton",
                        font=("calibri, 10"),
                        borderwidth="4",
                        background=but_submit,
                        foreground="white")

        style.map("C.TButton",
                        foreground=[("active", "white")],
                        background=[("active", but_submit_active)])

        # endregion
        self.table = ttk.Treeview(window)
        self.table["columns"]=("one", "two", "three", "four")
        self.table.column("#0", width=70)
        self.table.column("one", width=170)
        self.table.column("two", width=170)
        self.table.column("three", width=120)
        self.table.column("four", width=100)

        self.table.heading("#0", text="Index No.", command=self.filltable)
        self.table.heading("one", text="Media Name", command=lambda: self.recordSort("name"))
        self.table.heading("two", text="Author Name", command=lambda: self.recordSort("author"))
        self.table.heading("three", text="Date", command=lambda: self.recordSort("date"))
        self.table.heading("four", text="Media Type", command=lambda: self.recordSort("type"))
        #lamda used so that function can be called with arguments without it running directly

        self.filltable()
        self.table.grid(column=2, row=2, rowspan=3)

        self.refreshlbl = tk.Label(window, text="", bg=bg, font=("calibri", 10))
        self.refreshlbl.grid(column=2, row=6,pady=10)

        self.photo = tk.PhotoImage(file="unnamed.png")
        self.photoimage = self.photo.subsample(15, 15)
        refresh = ttk.Button(window, command=self.refreshButton, image=self.photoimage)

        refresh.grid(column=2, row=5, pady=5)

        self.but_add = ttk.Button(window, text="Add record", command=AddRecord) # command calls the class
        self.but_edit = ttk.Button(window, text="Edit Record", command=EditRecord)
        self.but_del = ttk.Button(window, text="Delete Record", command=DeleteRecord, style="W.TButton")
        # adds the unique style of the delete button

        self.but_add.grid(column=1, row=2, padx=25)
        self.but_edit.grid(column=1, row=3, padx=25)
        self.but_del.grid(column=1, row=4, padx=25)

        self.TMlbl = tk.Label(window,
                              text="Property of and\nDeveloped by Gregory Frost",
                              font=("calibri", 6),
                              bg=bg,
                              fg="white")
        self.TMlbl.grid(column=1, row=6)

    def refreshButton(self):
        self.refreshlbl.configure(text="Table Refreshed")
        self.filltable() # refills the table with new information

    def recordSort(self, method):
        self.table.delete(*self.table.get_children()) # clears the table
        data = store() # gets the database file
        i = 0
        dateindex = list()
        for line in data:
            #ignores non record lines
            if line == "#START#\n":
                i += 1
            elif line == "\n":
                i += 1
            else:
                #adds sorting information into list
                if method == "date":
                    date = getDate(i, "update")
                    item = [date, i]

                elif method == "author":
                    author = getAuthor(i, "update")
                    item = [author, i]

                elif method == "name":
                    name = getName(i, "update")
                    item = [name, i]

                elif method == "type":
                    type = getType(i, "update")
                    item = [type, i]

                dateindex.append(item)
                i += 1

        final = sorted(dateindex, key=lambda x: x[0]) # sorts the records
        ind = 0
        for record in final:
            #puts the sorted record into the table
            index = final[ind][1]
            name = getName(index, "update")
            author = getAuthor(index, "update")
            date = getDate(index, "update")
            type = getType(index, "update")
            index = int(getIndex(index, "update"))
            self.table.insert("", tk.END, text=index, values=(name, author, date, type))
            ind += 1

    def filltable(self):
        self.table.delete(*self.table.get_children())
        data = store()
        i = 0
        for lines in data:
            if lines == "#START#\n":
                i += 1
            elif lines == "\n":
                i += 1
            else:
                index = getIndex(i, "update")
                name = getName(i, "update")
                author = getAuthor(i, "update")
                author = author.title()
                date = getDate(i, "update")
                type = getType(i, "update")
                self.table.insert("", i, text=index, values=(name, author, date, type))
                i += 1


class Help:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.top = tk.Toplevel() # creates new form on top of main screen
        self.top.geometry("%dx%d" % (self.width, self.height)) # creates the form
        self.top.title("Media Library - Help Page")
        self.top.configure(bg=bg)
        self.i = 0

        self.title = tk.Label(self.top,
                              bg=table_top,
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
                                   font=("courier", (title_font-7)),
                                   borderwidth=2,
                                   relief="ridge")
        self.subheading.grid(column=2, row=2)

        #defines the image paths
        self.homeimage = tk.PhotoImage(file="HomeScreenHelp.png")
        self.addimage = tk.PhotoImage(file="AddScreenHelp.png")
        self.editimage = tk.PhotoImage(file="EditScreenHelp.png")
        self.delimage = tk.PhotoImage(file="DeleteScreenHelp.png")
        self.sortimage = tk.PhotoImage(file="SortScreenHelp.png")
        self.filterimage = tk.PhotoImage(file="FilterScreenHelp.png")

        self.top.homeimage = self.homeimage
        self.content = tk.Canvas(self.top, height=420, width=750, bg=bg,highlightthickness=1, highlightbackground=bg)
        self.content.grid(column=1, row=3, columnspan=3, padx=25, pady=10)
        self.contentimage = self.content.create_image(370, 200, image=self.homeimage)

        self.btnnext = ttk.Button(self.top, text=">", command=self.nextpage)
        self.btnprev = ttk.Button(self.top, text="<", command=self.prevpage)
        self.pagenum = tk.Label(self.top, bg=bg, text="Page 1/6", font=("courier"))
        self.btnnext.grid(column=3, row=4, padx=50)
        self.btnprev.grid(column=1, row=4, padx=50)
        self.pagenum.grid(column=2, row=4)

    def nextpage(self):
        if self.i < 5:
            self.i += 1 # increments page number and loops around to the start
        else:
            self.i = 0
        self.updatetext()

    def prevpage(self):
        if self.i > 0:
            self.i -= 1 # deincrements the page number loops to the end
        else:
            self.i = 5
        self.updatetext()

    def showimage(self, newimage):
        self.content.itemconfig(self.contentimage, image=newimage) # changes the image shown

    def updatetext(self):
        #updates the text and image based on what page number the help screen is on
        if self.i == 0:
            self.subheading.configure(text="Home Screen")
            self.showimage(self.homeimage)
            self.pagenum.configure(text="Page 1/6")
        elif self.i == 1:
            self.subheading.configure(text="Add Record")
            self.showimage(self.addimage)
            self.pagenum.configure(text="Page 2/6")
        elif self.i == 2:
            self.subheading.configure(text="Edit Record")
            self.showimage(self.editimage)
            self.pagenum.configure(text="Page 3/6")
        elif self.i == 3:
            self.subheading.configure(text="Delete Record")
            self.showimage(self.delimage)
            self.pagenum.configure(text="Page 4/6")
        elif self.i == 4:
            self.subheading.configure(text="Sorting")
            self.showimage(self.sortimage)
            self.pagenum.configure(text="Page 5/6")
        elif self.i == 5:
            self.subheading.configure(text="Filter Table")
            self.showimage(self.filterimage)
            self.pagenum.configure(text="Page 6/6")


class Filter:
    def __init__(self):
        self.width = 500
        self.height = 250
        self.top = tk.Toplevel()
        self.top.geometry("%dx%d" % (self.width, self.height))
        self.top.configure(bg=bg)
        #creates the new form

        self.title = tk.Label(self.top,
                              text="",
                              bg=table_top,
                              fg="white",
                              font=("Courier", title_font),
                              borderwidth=2,
                              relief="ridge")
        self.title.grid(column=2, row=1, padx=150, pady=20)
        self.filterlbl = tk.Label(self.top, text="Enter the filter requirements: ", bg=bg, font=("calibri"))
        self.filterlbl.grid(column=2, row=2)
        self.filterEntry = tk.Entry(self.top)
        self.filterEntry.grid(column=2, row=3, pady=15)
        self.filterbut = ttk.Button(self.top, text="Filter")
        self.filterbut.grid(column=2, row=4, pady=20)

    def showRecord(self, i):
        passed = False # resets the loop
        index = getIndex(i, "update") # reopens the file and gathers information
        name = getName(i, "update")
        author = getAuthor(i, "update")
        date = getDate(i, "update")
        type = getType(i, "update")
        items = [index, name, author, date, type] # compiles the info into one record
        for component in items:
            if component == "#START#":
                #ignores the start line of the database file
                passed = False
            else:
                passed = True
        if passed:
            MainScreen.table.insert("", i, text=index, values=(name, author, date, type))
            #if not the first line then add it to the table


class MediaFilter(Filter):
    def __init__(self):
        super().__init__() # gets the variables and methods from parent
        self.top.title("Media Library - Media Filter") # changes some of the variables
        self.title.configure(text="Media Filter")
        self.filterbut.configure(command=self.filter)

    def filter(self):
        self.filter = self.filterEntry.get().upper() # gets the users requested filter and stores it in upper class
        data = store()
        MainScreen.table.delete(*MainScreen.table.get_children()) # clears the table
        i = 0
        for lines in data:
            type = getType(i, data) # gets the media type
            if type == self.filter: # if type equals what the user wants then display record
                self.showRecord(i)
                i += 1
            else:
                i += 1


class AuthorFilter(Filter):
    def __init__(self):
        super().__init__() # gets parnet variables and methods
        self.top.title("Media Library - Author Filter")
        self.title.configure(text="Author Filter") # changes some of the variables
        self.filterbut.configure(command=self.filter)

    def filter(self):
        self.filter = self.filterEntry.get() # gets the user filter request
        data = store() # gets the data from file
        MainScreen.table.delete(*MainScreen.table.get_children()) # clears the table
        i = 0
        for lines in data:
            author = getAuthor(i, data) # gets the author of the line
            if self.filter.title() in author or self.filter.upper() in author or self.filter.lower() in author:
                self.showRecord(i) # if user request is in name of author then show the record
                i += 1
            else:
                i += 1


class AddRecord:
    def __init__(self):
        self.width = 500
        self.height = 400
        self.top = tk.Toplevel()
        self.top.title("Media Library - Add Record")
        self.top.geometry("%dx%d" % (self.width, self.height))
        self.top.configure(bg=bg)
        #creates the form
        self.title = tk.Label(self.top,
                              text="Add New Record",
                              bg=table_top,
                              fg="white",
                              font=("Courier", title_font),
                              borderwidth=2,
                              relief="ridge")
        self.title.grid(row=1, column=1, pady=20, columnspan=2)

        self.typeLabel = tk.Label(self.top, text="Type of Media:", bg=bg, font=("calibri"))
        self.typeLabel.grid(column=1, row=2)

        self.v = tk.IntVar()
        self.v.set(3)       # deselects any radio button
        mediaTypes = [("DVD", "1"),
                      ("CD", "2"),
                      ("GAME", "3")]    #shows the name of radio button and the value of each
        i = 3 # sets the minimum row height of the radio button
        for val, types in enumerate(mediaTypes): # for every media type loop
            tk.Radiobutton(self.top,
                           text=types,
                           padx=20,
                           variable=self.v,
                           bg=bg,
                           value=val).grid(row=i, column=1) # creates a radio button placed at i value
            i += 1 # increments i so next radio button is placed below it

        self.authorLabel = tk.Label(self.top, text="Name of Author: ", bg=bg, font=("calibri"))
        self.MediaLabel = tk.Label(self.top, text="Name of Media: ", bg=bg, font=("calibri"))
        self.DateLabel = tk.Label(self.top, text="Release Date: ", bg=bg, font=("calibri"))

        self.authorT = tk.Entry(self.top)
        self.MediaT = tk.Entry(self.top)
        self.dateT = tk.Entry(self.top) # creates entry boxes

        self.authorLabel.grid(row=6, column=1, pady=20)
        self.authorT.grid(row=7, column=1, padx=40)

        self.MediaLabel.grid(row=2, column=2)
        self.MediaT.grid(row=4, column=2)

        self.DateLabel.grid(row=6, column=2)
        self.dateT.grid(row=7,column=2, padx=90)

        self.Submit = ttk.Button(self.top, text="Submit", command=self.submitRecord, style="C.TButton")
        self.Submit.grid(row=8, column=2, pady=40)

        self.Submitlbl = tk.Label(self.top, text=" ", bg=bg, font=("calibri"))
        self.Submitlbl.grid(column=1, row=8)

    def submitRecord(self):
        self.Submitlbl.configure(text="Record Submitted \nPlease close the window") # feedback for user
        self.create_record() #creates the record in the database

    def getValues(self):
        #gets the current value of each input
        mediaType = self.v.get()
        mediaType = typeConvert(mediaType, "numToChar")
        name = self.MediaT.get()
        author = self.authorT.get()
        date = self.dateT.get()
        return mediaType, name, author, date

    def create_record(self):
        type, name, author, date = self.getValues()
        attributes = [type, name, author, date]
        valid = False # resets the validity check
        check = 0
        for x in attributes:
            if len(x) == 0: # if nothing in entry box
                self.Submitlbl.configure(text="*Please make sure all\nentry boxes are filled") # say nothing in entry box
            else:
                check += 1 # entry box is filled
        if check == 4: # if all entry boxes are filled
            valid = True # record becomes valid
        if valid:
            autonum = genAutonum() # creates an id number for the record
            record = [str(autonum), name, author, date, type] # creates the record
            with open("Database.txt", "a") as file:
                file.write("\n" + str(record)) # writes the record into file


class EditRecord:
    def __init__(self):
        self.data = store()
        self.width = 500
        self.height = 400
        self.top = tk.Toplevel()
        self.top.title("Media Library - Edit Record")
        self.top.geometry("%dx%d" % (self.width, self.height))
        self.top.configure(bg=bg)
        #creates the form
        self.title = tk.Label(self.top,
                              text="Edit record",
                              bg=table_top,
                              fg="white",
                              font=("Courier", title_font),
                              borderwidth=2,
                              relief="ridge")
        self.title.grid(row=1, column=2, pady=20)
        
        self.lbl1 = tk.Label(self.top, text="Enter the record ID you want to edit", bg=bg, font=("calibri"))
        self.IDcheck = tk.Entry(self.top)
        self.loadID = ttk.Button(self.top, text="Load", command=self.loadRecord)
        self.lbl1.grid(row=2, column=2)
        self.IDcheck.grid(row=3, column=2)
        self.loadID.grid(row=3, column=3)

        self.v = tk.IntVar()
        self.v.set(4) #deselects the radio buttons
        mediaTypes = [("DVD", "1"),
                      ("CD", "2"),
                      ("GAME", "3")] # defines the buttons name and value
        i = 5 # sets minimum height for button height
        for val, types in enumerate(mediaTypes): # for every media type loop
            tk.Radiobutton(self.top,
                           text=types,
                           padx=10,
                           variable=self.v,
                           bg=bg,
                           value=val).grid(row=i, column=2) # creates the button and places it at i height
            i += 1 # increases the height of i

        self.lbl2 = tk.Label(self.top, text="Media Type: ", bg=bg, font=("calibri"))
        self.lbl2.grid(row=4,column=2)

        self.lbl3 = tk.Label(self.top, text="Name of media: ", bg=bg, font=("calibri"))
        self.medianame = tk.Entry(self.top)
        self.lbl3.grid(row=8,column=1)
        self.medianame.grid(row=9,column=1, padx=5)

        self.lbl4 = tk.Label(self.top, text="Author: ", bg=bg, font=("calibri"))
        self.author = tk.Entry(self.top)
        self.lbl4.grid(row=8,column=2)
        self.author.grid(row=9,column=2)

        self.lbl5 = tk.Label(self.top, text="Date Published: ", bg=bg, font=("calibri"))
        self.date = tk.Entry(self.top)
        self.lbl5.grid(row=8,column=3)
        self.date.grid(row=9,column=3)

        self.submit = ttk.Button(self.top, text="Submit", command=self.submitBut, style="C.TButton")
        self.submit.grid(row=10,column=3, pady=75)

        self.submitlbl = tk.Label(self.top, text="", bg=bg, font=("calibri"))
        self.submitlbl.grid(row=10, column=2)

    def submitBut(self):
        self.submitlbl.configure(text="Record has been Edited\nPlease close this window") # feedback for user
        self.editRecord() # updates the record with edited information

    def loadRecord(self):
        recID = self.IDcheck.get() # finds the correct file
        autonum = genAutonum() # gens a new index number to should the last possible record id
        if int(recID) >= autonum: # stops users from trying to find record that isnt there
            self.submitlbl.configure(text="The record could not be found") # feedback for user
        else: # if record was found
            index = int(findRecord(recID)) # gets index number
            type = getType(index, "update")
            type = typeConvert(type, "charToNum")
            int(type)
            self.v.set(type)
            media = getName(index, "update")
            author = getAuthor(index, "update")
            date = getDate(index, "update") # gets record information

            self.medianame.delete(0, tk.END) #clears the entry box
            self.medianame.insert(0, media) # inputs the record information into entry box

            self.author.delete(0, tk.END)
            self.author.insert(0, author)

            self.date.delete(0, tk.END)
            self.date.insert(0, date)

    def editRecord(self):
        recID = self.IDcheck.get()
        name = self.medianame.get()
        author = self.author.get()
        date = self.date.get()
        type = self.v.get()
        type = typeConvert(type, "numToChar") # gets the record info
        record = [recID, name, author, date, type] # creates a record

        i = 0 # initialises the start of loop
        overwrite()
        for line in self.data:
            if line == "#START#\n": # ignores non record lines
                i += 1
                continue
            elif line == "\n":
                i += 1
                continue
            else: # if line is record
                index = getIndex(i, self.data)
                if index == recID: # if its the selected record
                    with open("Database.txt", "a") as file:
                        file.write("\n" + str(record) + "\n") # replace old record with new one
                    i += 1
                else:
                    with open("Database.txt", "a") as file:
                        file.write("\n" + line) # rewrite the line
                    i += 1


class DeleteRecord:
    def __init__(self):
        self.width = 500
        self.height = 400
        self.top = tk.Toplevel()
        self.top.title("Media Library - Delete Record")
        self.top.geometry("%dx%d" % (self.width, self.height))
        self.top.configure(bg=bg)
        #creates the form
        self.title = tk.Label(self.top,
                              text="Delete a record",
                              bg=table_top,
                              fg="white",
                              font=("Courier", title_font),
                              borderwidth=2,
                              relief="ridge")
        self.title.grid(row=1, column=2, padx=110, pady=20)

        self.lbl1 = tk.Label(self.top, text="Please enter the record ID that you want to be deleted: ", bg=bg)
        self.lbl1.grid(row=2, column=2, pady=50)

        self.selectrecord = tk.Entry(self.top)
        self.selectrecord.grid(row=3, column=2)

        self.but_del = ttk.Button(self.top, text="Delete Record", command=self.deleteButton, style="W.TButton")
        self.but_del.grid(row=4, column=2, pady=20)

        self.deletelbl = tk.Label(self.top, text=" ", bg=bg, font=("calibri"))
        self.deletelbl.grid(row=5, column=2)

    def deleteButton(self):
        self.deletelbl.configure(text="Record has been deleted \nPlease close this window")#feedback for user
        self.deleteRecord()#deletes the record

    def deleteRecord(self):
        del_req = self.selectrecord.get() # gets the user input for what record
        autonum = genAutonum()
        if int(del_req) >= autonum: # makes sure the record exists
            self.deletelbl.configure(text="Record could not be found")
        else: # if record exists
            data = store() # store the current file data
            overwrite() #clear the file data
            i = 0
            for line in data:
                index = getIndex(i, data) # gets index of each line
                if line == "#START#\n": # ignores the non record lines
                    i += 1
                    continue
                elif line == "\n":
                    i += 1
                    continue
                else:
                    if index == del_req: # if record id == the requested id
                        i += 1 # skip that line
                        continue
                    else: # if record id doesnt == the requested id
                        with open("Database.txt", "a") as file:
                            file.write("\n" + line) # skip that line
                        i += 1


# region "SplashScreen"
splashScreen = tk.Tk() # creates a window
width = 800
height = 600
splashScreen.title("Media Library")
splashScreen.call('wm', 'iconphoto', splashScreen._w, tk.PhotoImage(file='MLIcon.png'))
splashScreen.configure(bg=bg)
#defines attributes of window
image1 = tk.PhotoImage(file="splashscreen1.png") # loads image for splashscreen

canvas = tk.Canvas(splashScreen, height=height*0.8, width=width*0.8, bg=bg) # creates canvas for image
canvas.pack()
splashscreenimage = canvas.create_image(width * 0.8 / 2, height * 0.8 / 2, image=image1) # displays image on canvas
canvas.pack()


def close(event): # closes the splash screen
    splashScreen.destroy()


splashScreen.bind("<Button-1>", close) # if LMB is clicked then close the window

splashScreen.mainloop()

# endregion

window = tk.Tk() # creates window
window.title("Media Library")
window.configure(bg=bg)
window.geometry("800x400")
window.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='MLIcon.png'))  # adds favicon to window
MainScreen = MainMenu(window)  # creates object for the main menu

window.mainloop()
