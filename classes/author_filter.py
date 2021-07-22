from .filter import Filter


class AuthorFilter(Filter):
    def __init__(self, file, main_screen):
        self.main_screen = main_screen
        self.file = file
        super().__init__(file, main_screen)  # gets parnet variables and methods
        self.top.title("Media Database - Author Filter")
        self.title.configure(text="Author Filter")  # changes some of the variables
        self.filter_btn.configure(command=self.filter)

    def filter(self):
        filter = self.filter_entry.get()  # gets the user filter request
        data = self.file.store()  # gets the data from file
        self.main_screen.table.delete(*self.main_screen.table.get_children())  # clears the table
        i = 0
        for _ in data:
            author = self.file.get_author(i, data)  # gets the author of the line
            if filter.title() in author or filter.upper() in author or filter.lower() in author:
                self.show_record(i)  # if user request is in name of author then show the record
                i += 1
            else:
                i += 1