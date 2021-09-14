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
        author_filter = self.filter_entry.get()  # gets the user filter request
        data = self.file.load()  # gets the data from file
        self.main_screen.table.delete(*self.main_screen.table.get_children())  # clears the table
        for record in data:
            author = self.file.get_author(record)  # gets the author of the line
            if any(variant in author for variant in
                   [author_filter.title(), author_filter.upper(), author_filter.lower()]):
                self.show_record(record)  # if user request is in name of author then show the record
