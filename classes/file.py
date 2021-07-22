class File:
    # Opens the database file and stores the content in the data variable
    def store(self):
        with open("assets/database.txt", "r") as file:
            data = file.readlines()
        return data

    # works through each record until the requested one is found
    def find_record(self, req_id):
        found = False
        i = 0
        while not found:
            index = self.get_index(i, "update")
            if index != req_id:
                i += 1
            else:
                found = True
        return i

    # gets the positions of the separators for each record
    def get_separators(self, i, data):
        if data == "update":
            data = self.store()
        line = data[i]
        start = 0
        separators = list()
        for i in range(10):
            separators_locations = line.find("\'", start)
            separators.append(separators_locations)
            start = separators_locations + 1
        return line, separators

    # uses the separators to find the correct information and returns it
    def get_index(self, i, data):
        line, separators = self.get_separators(i, data)
        index = line[separators[0] + 1: separators[1]]
        return index

    def get_name(self, i, data):
        line, separators = self.get_separators(i, data)
        name = line[separators[2] + 1: separators[3]]
        return name

    def get_author(self, i, data):
        line, separators = self.get_separators(i, data)
        author = line[separators[4] + 1: separators[5]]
        return author

    def get_date(self, i, data):
        line, separators = self.get_separators(i, data)
        date = line[separators[6] + 1: separators[7]]
        return date

    def get_type(self, i, data):
        line, separators = self.get_separators(i, data)
        media_type = line[separators[8] + 1: separators[9]]
        return media_type

    # converts media type so it can taken from and put into radio buttons
    def type_convert(self, media_type, method):
        if method == "numToChar":
            if media_type == 0:
                media_type = "DVD"
            elif media_type == 1:
                media_type = "CD"
            elif media_type == 2:
                media_type = "GAME"

        elif method == "charToNum":
            if media_type == "DVD":
                media_type = 0
            elif media_type == "CD":
                media_type = 1
            elif media_type == "GAME":
                media_type = 2
        return media_type

    # creates the index for the next record
    def gen_auto_num(self):
        count = 0
        data = self.store()
        for _ in data:
            count += 1
        finished = False
        lines = self.store()
        line_no = count - 1
        while not finished:
            if lines[line_no] == "\n":
                line_no -= 1
            else:
                finished = True
        index = self.get_index(line_no, "update")
        auto_num = int(index) + 1
        return auto_num

    # clears the file ready for file to be rewritten
    def overwrite(self):
        with open("assets/database.txt", "w") as file:
            file.write("#START#")
