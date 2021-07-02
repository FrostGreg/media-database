def createFile():
    file = open("Test.txt", "a")
    file.close()


def displayFile():
    with open("Test.txt", "r") as file:
        print(file.read())


def addRecord():
    with open("Test.txt", "a") as file:
        autonum = genAutonum()
        line = [str(autonum)]
        info = ["name", "author", "date"]
        for att in info:
            att = input("Please enter " + att + "?: ")
            line.append(att)
        line = str(line)
        file.write("\n" + line)


def findRecord():
    req_index = input("Enter the record ID of the record you want: ")
    found = False
    i = 0
    while not found:
        index = getIndex(i)
        if index != req_index:
                i += 1
        else:
            found = True
    return i, index

def deleteRecord():
    del_req = input("Enter the record ID of the record you want to delete: ")
    data = store()
    overwrite()
    for line in data:
        index = line[2:3]
        if line == "#START#\n":
            continue
        elif line == "\n":
            continue
        else:
            if index == del_req:
                continue
            else:
                with open("Test.txt", "a") as file:
                    file.write("\n" + line)

def getSeperators(i):
    with open("Test.txt", "r") as file:
        lines = file.readlines()
        line = lines[i]
        start = 0
        seperators = list()
        for i in range (8):
            seperators_locations = line.find("\'", start)
            seperators.append(seperators_locations)
            start = seperators_locations + 1
        #print(seperators)
    return line, seperators


def getIndex(i):
    line, seperators = getSeperators(i)
    index = line[seperators[0] + 1 : seperators[1]]
    return index


def getName(i):
    line, seperators = getSeperators(i)
    name = line[seperators[2] + 1 : seperators[3]]
    return name


def getAuthor(i):
    line, seperators = getSeperators(i)
    author = line[seperators[4] + 1: seperators[5]]
    return author


def getDate(i):
    line, seperators = getSeperators(i)
    date = line[seperators[6] + 1: seperators[7]]
    return date


def displayRecord():
    i, index = findRecord()
    name = getName(i)
    author = getAuthor(i)
    date = getDate(i)
    print("The record index is: "+index+
          "\nThe Name of the media is: "+name+
          "\nThe author of the media is: "+author+
          "\nThe release date of the media is: "+date)

def genAutonum():
    count = 0
    with open("Test.txt", "r") as file:
        for line in file:
            count += 1
        finished = False
        lines = store()
        lineno = count - 1
        while not finished:
            if lines[lineno] == "\n":
                lineno -= 1
            else:
                finished = True
        index = getIndex(lineno)
    autonum = int(index) + 1
    return autonum

def overwrite():
    with open("Test.txt", "w") as file:
        file.write("#START#")

def store():
    with open("Test.txt", "r") as file:
        data = file.readlines()
    return data

createFile()
closed = False
mode_input = None
while not closed:
    while 1:
        try:
            mode_input = int(input("\n1. Display File "
                                   "\n2. Add Record "
                                   "\n3. Display Record "
                                   "\n4. Delete Record "
                                   "\n10. Close Program "
                                   "\nWhat mode would you like?: "))
            break
        except ValueError:
            print("################\nError: Invalid Input   Please try a valid number\n################")
            continue

    if mode_input == 1:
        displayFile()

    elif mode_input == 2:
        addRecord()

    elif mode_input == 3:
        displayRecord()

    elif mode_input == 4:
        deleteRecord()

    elif mode_input == 5:
        print(genAutonum())


    elif mode_input == 10:
        closed = True
        quit()