import tkinter as tk
from tkinter import ttk
from time import sleep

# region "Variables"
bg = "#D7CEC7"
button_colour = "#565C5E"
but_del = "#994848"
but_submit = "#1f8844"
table_top = "#76323F"

# endregion


def findRecord(reqID):
    found = False
    i = 0
    while not found:
        index = getIndex(i)
        if index != reqID:
            i += 1
        else:
            found = True
    return i


def getSeperators(i):
    with open("Database.txt", "r") as file:
        lines = file.readlines()
        line = lines[i]
        start = 0
        seperators = list()
        for i in range(10):
            seperators_locations = line.find("\'", start)
            seperators.append(seperators_locations)
            start = seperators_locations + 1
    return line, seperators


def getIndex(i):
    line, seperators = getSeperators(i)
    index = line[seperators[0] + 1: seperators[1]]
    return index


def getName( i):
    line, seperators = getSeperators(i)
    name = line[seperators[2] + 1: seperators[3]]
    return name


def getAuthor( i):
    line, seperators = getSeperators(i)
    author = line[seperators[4] + 1: seperators[5]]
    return author


def getDate( i):
    line, seperators = getSeperators(i)
    date = line[seperators[6] + 1: seperators[7]]
    return date


def getType( i):
    line, seperators = getSeperators(i)
    type = line[seperators[8] + 1: seperators[9]]
    return type

def overwrite():
    with open("Database.txt", "w") as file:
        file.write("#START#")

class MainMenu:
    def __init__(self, window):
        menu_bar = tk.Menu(window)
        filemenu = tk.Menu(menu_bar, tearoff=0)
        filemenu.add_command(label="Exit Program", command=window.quit)
        menu_bar.add_cascade(label="File", menu=filemenu)

        sortmenu = tk.Menu(menu_bar, tearoff=0)
        sortmenu.add_command(label="Alphabetical(Author)", command=self.test)
        sortmenu.add_command(label="Alphabetical(Name)", command=self.test)
        sortmenu.add_command(label="Release Date", command=self.test)
        sortmenu.add_command(label="Media Type", command=self.test)
        menu_bar.add_cascade(label="Sort", menu=sortmenu)

        filtermenu = tk.Menu(menu_bar, tearoff=0)
        filtermenu.add_command(label="Media Type", command=self.test)
        filtermenu.add_command(label="Author", command=self.test)
        menu_bar.add_cascade(label="Filter", menu=filtermenu)

        window.config(menu=menu_bar)

        title = tk.Label(window, text="Your Library", bg=bg)
        title.grid(column=2, row=1)

        self.but_add = tk.Button(window, text="Add Record", command=AddRecord, bg=button_colour, fg="white")
        self.but_edit = tk.Button(window, text="Edit Record", command=EditRecord, bg=button_colour, fg="white")
        self.but_del = tk.Button(window, text="Delete Record", command=DeleteRecord, bg=but_del, fg="white")

        self.but_add.grid(column=1, row=2, padx=40, pady=25)
        self.but_edit.grid(column=1, row=3, padx=40, pady=25)
        self.but_del.grid(column=1, row=4, padx=40, pady=25)

        self.table = ttk.Treeview(window)
        self.table["columns"]=("one", "two", "three", "four")
        self.table.column("#0", width=60)
        self.table.column("one", width=170)
        self.table.column("two", width=170)
        self.table.column("three", width=120)
        self.table.column("four", width=100)

        self.table.heading("#0", text="Index No.")
        self.table.heading("one", text="Media Name")
        self.table.heading("two", text="Author Name")
        self.table.heading("three", text="Date")
        self.table.heading("four", text="Media Type")

        self.filltable()
        self.table.grid(column=2, row=2, rowspan=3, pady=100)

        refresh = tk.Button(window, text="Refresh Table", command=self.refreshButton, bg=button_colour, fg="white")
        refresh.grid(column=2, row=5)

        self.refreshlbl = tk.Label(window, text="", bg=bg)
        self.refreshlbl.grid(column=2, row=4)

    def refreshButton(self):
        self.refreshlbl.configure(text="Table Refreshed")
        self.filltable()

    def test(self):
        x = 0



    def filltable(self):
        self.table.delete(*self.table.get_children())
        with open("Database.txt", "r") as file:
            i = 0
            for lines in file:
                if lines == "#START#\n":
                    i += 1
                    continue
                elif lines == "\n":
                    i += 1
                    continue
                else:
                    index = getIndex(i)
                    name = getName(i)
                    author = getAuthor(i)
                    date = getDate(i)
                    type = getType(i)
                    self.table.insert("", i, "", text=index, values=(name, author, date, type))
                    i += 1



class AddRecord:
    def __init__(self):
        self.width = 500
        self.height = 400
        self.top = tk.Toplevel()
        self.top.title("Add Record")
        self.top.geometry("%dx%d" % (self.width, self.height))
        self.top.configure(bg=bg)

        self.title = tk.Label(self.top, text="Add New Record", bg=bg)
        self.title.grid(row=1, column=2, padx=50, pady=20)

        self.v = tk.IntVar()
        self.v.set(1)
        mediaTypes = [("DVD", "1"),
                      ("CD" , "2"),
                      ("Game", "3")]
        i = 3
        for val, types in enumerate(mediaTypes):
            tk.Radiobutton(self.top,
                           text=types,
                           padx=20,
                           variable=self.v,
                           bg=bg,
                           command=self.ShowChoice,
                           value=val).grid(row=i, column=1)
            i += 1

        self.authorLabel = tk.Label(self.top, text="Name of Author: ", bg=bg)
        self.MediaLabel = tk.Label(self.top, text="Name of Media: ", bg=bg)
        self.DateLabel = tk.Label(self.top, text="Release Date: ", bg=bg)

        self.authorT = tk.Entry(self.top)
        self.MediaT = tk.Entry(self.top)
        self.dateT = tk.Entry(self.top)

        self.authorLabel.grid(row=6, column=1)
        self.authorT.grid(row=7, column=1)

        self.MediaLabel.grid(row=2, column=3)
        self.MediaT.grid(row=4, column=3)

        self.DateLabel.grid(row=6, column=3)
        self.dateT.grid(row=7,column=3)

        self.Submit = tk.Button(self.top, text="Submit", command=self.submitRecord, bg=but_submit, fg="white")
        self.Submit.grid(row=8, column=3)

        self.Submitlbl = tk.Label(self.top, text=" ", bg=bg)
        self.Submitlbl.grid(column=3, row=9)

    def submitRecord(self):
        self.Submitlbl.configure(text="Record Submitted \nPlease close the window")
        self.create_record()
        
    def ShowChoice(self):
        print("The Choice made is: ", self.v.get())

    def getValues(self):
        mediaType = self.v.get()
        if mediaType == 0:
            mediaType = "DVD"
        elif mediaType == 1:
            mediaType = "CD"
        elif mediaType == 2:
            mediaType = "Game"

        name = self.MediaT.get()
        author = self.authorT.get()
        date = self.dateT.get()
        return mediaType, name, author, date

    def store(self):
        with open("Database.txt", "r") as file:
            data = file.readlines()
        return data

    def genAutonum(self):
        count = 0
        with open("Database.txt", "r") as file:
            for line in file:
                count += 1
            finished = False
            lines = self.store()
            lineno = count - 1
            while not finished:
                if lines[lineno] == "\n":
                    lineno -= 1
                else:
                    finished = True
            index = getIndex(lineno)
        autonum = int(index) + 1
        return autonum

    def create_record(self):
        type, name, author, date = self.getValues()
        autonum = self.genAutonum()
        record = [str(autonum), name, author, date, type]
        with open("Database.txt", "a") as file:
            file.write("\n" + str(record))

class EditRecord:
    def __init__(self):
        with open("Database.txt", "r") as file:
            self.data = file.readlines()
        self.width = 500
        self.height = 400
        self.top = tk.Toplevel()
        self.top.title("Edit Record")
        self.top.geometry("%dx%d" % (self.width, self.height))
        self.top.configure(bg=bg)

        self.title = tk.Label(self.top, text="Edit record", bg=bg)
        self.title.grid(row=1, column=2)
        
        self.lbl1 = tk.Label(self.top, text="Enter the record ID you want to edit", bg=bg)
        self.IDcheck = tk.Entry(self.top)
        self.loadID = tk.Button(self.top, text="Load", command=self.loadRecord, bg=button_colour, fg="white")
        self.lbl1.grid(row=2, column=2)
        self.IDcheck.grid(row=3, column=2)
        self.loadID.grid(row=3, column=3)

        self.v = tk.IntVar()
        self.v.set(1)
        mediaTypes = [("DVD", "1"),
                      ("CD", "2"),
                      ("Game", "3")]
        i = 5
        for val, types in enumerate(mediaTypes):
            tk.Radiobutton(self.top,
                           text=types,
                           padx=20,
                           variable=self.v,
                           bg=bg,
                           command=self.ShowChoice(),
                           value=val).grid(row=i, column=2)
            i += 1

        self.lbl2 = tk.Label(self.top, text="Media Type: ", bg=bg)
        self.lbl2.grid(row=4,column=2)

        self.lbl3 = tk.Label(self.top, text="Name of media: ", bg=bg)
        self.medianame = tk.Entry(self.top)
        self.lbl3.grid(row=8,column=1)
        self.medianame.grid(row=9,column=1)

        self.lbl4 = tk.Label(self.top, text="Author: ", bg=bg)
        self.author = tk.Entry(self.top)
        self.lbl4.grid(row=8,column=2)
        self.author.grid(row=9,column=2)

        self.lbl5 = tk.Label(self.top, text="Date Published: ",bg=bg)
        self.date = tk.Entry(self.top)
        self.lbl5.grid(row=8,column=3)
        self.date.grid(row=9,column=3)

        self.submit = tk.Button(self.top, text="Submit", command=self.submitBut, bg=but_submit, fg="white")
        self.submit.grid(row=10,column=4)

        self.submitlbl = tk.Label(self.top, text="", bg=bg)
        self.submitlbl.grid(row=11, column=4)

    def ShowChoice(self):
        print(self.v.get())

    def submitBut(self):
        self.submitlbl.configure(text="Record has been Edited\nPlease close this window")
        self.editRecord()

    def getSeperators(self, i):
        line = self.data[i]
        start = 0
        seperators = list()
        for i in range(10):
            seperators_locations = line.find("\'", start)
            seperators.append(seperators_locations)
            start = seperators_locations + 1
        return line, seperators

    def getIndex(self, i):
        line, seperators = self.getSeperators(i)
        index = line[seperators[0] + 1: seperators[1]]
        return index

    def loadRecord(self):
        recID = self.IDcheck.get()
        index = int(findRecord(recID))
        type = getType(index)
        if type == "DVD":
            type = 1
        elif type == "CD":
            type = 2
        elif type == "Game":
            type = 3

        media = getName(index)
        author = getAuthor(index)
        date = getDate(index)

        self.medianame.delete(0, tk.END)
        self.medianame.insert(0, media)

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
        if type == 0:
            type = "DVD"
        elif type == 1:
            type = "CD"
        elif type == 2:
            type = "Game"

        record = [recID, name, author, date, type]

        i = 0
        overwrite()
        for line in self.data:
            if line == "#START#\n":
                i += 1
                continue
            elif line == "\n":
                i += 1
                continue
            else:
                index = self.getIndex(i)
                if index == recID:
                    with open("Database.txt", "a") as file:
                        file.write("\n" + str(record) + "\n")
                    i += 1
                else:
                    with open("Database.txt", "a") as file:
                        file.write("\n" + line)
                    i += 1







class DeleteRecord:
    def __init__(self):
        self.width = 500
        self.height = 400
        self.top = tk.Toplevel()
        self.top.title("Delete Record")
        self.top.geometry("%dx%d" % (self.width, self.height))
        self.top.configure(bg=bg)

        self.title = tk.Label(self.top, text="Delete a record", bg=bg)
        self.title.grid(row=1, column=2, padx=160, pady=35)

        self.lbl1 = tk.Label(self.top, text="Please enter the record ID that you want to be deleted: ", bg=bg)
        self.lbl1.grid(row=2, column=2, pady=50)

        self.selectrecord = tk.Entry(self.top)
        self.selectrecord.grid(row=3, column=2)

        self.but_del = tk.Button(self.top, text="Delete Record", command=self.deleteButton, bg=but_del, fg="white")
        self.but_del.grid(row=4, column=3, pady=120)

        self.deletelbl = tk.Label(self.top, text=" ", bg=bg)
        self.deletelbl.grid(column=2, row=4)

    def deleteButton(self):
        self.deletelbl.configure(text="Record has been deleted \nPlease close this window")
        self.deleteRecord()

    def store(self):
        with open("Database.txt", "r") as file:
            data = file.readlines()
        return data



    def getSeperators(self, i, data):
        line = data[i]
        start = 0
        seperators = list()
        for i in range(10):
            seperators_locations = line.find("\'", start)
            seperators.append(seperators_locations)
            start = seperators_locations + 1
        return line, seperators

    def getIndex(self, i, data):
        line, seperators = self.getSeperators(i, data)
        index = line[seperators[0] + 1: seperators[1]]
        return index

    def deleteRecord(self):
        del_req = self.selectrecord.get()
        data = self.store()
        overwrite()
        i = 0
        for line in data:
            index = self.getIndex(i, data)
            if line == "#START#\n":
                i += 1
                continue
            elif line == "\n":
                i += 1
                continue
            else:
                if index == del_req:
                    i += 1
                    continue
                else:
                    with open("Database.txt", "a") as file:
                        file.write("\n" + line)
                    i += 1

# region "SplashScreen"
splashScreen = tk.Tk()
width = splashScreen.winfo_screenwidth()
height = splashScreen.winfo_screenheight()
splashScreen.title("Media Library")
splashScreen.call('wm', 'iconphoto', splashScreen._w, tk.PhotoImage(file='MLIcon.png'))
splashScreen.configure(bg=bg)


image1 = tk.PhotoImage(file="splashscreen1.png")


canvas = tk.Canvas(splashScreen, height=height*0.8, width=width*0.8, bg=bg)
canvas.pack()
splashscreenimage = canvas.create_image(width * 0.8 / 2, height * 0.8 / 2, image=image1)
canvas.pack()

def close(event):
    splashScreen.destroy()

splashScreen.bind("<Button-1>", close)

splashScreen.mainloop()

# endregion

window = tk.Tk()
window.title("Media Library")
window.configure(bg=bg)
window.geometry("800x600")
window.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='MLIcon.png'))
MainScreen = MainMenu(window)

window.mainloop()
