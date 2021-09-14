from .filter import Filter


class MediaFilter(Filter):
    def __init__(self, file, main_screen):
        self.main_screen = main_screen
        self.file = file
        super().__init__(file, main_screen)  # gets the variables and methods from parent
        self.top.title("Media Database - Media Filter")  # changes some of the variables
        self.title.configure(text="Media Filter")
        self.filter_btn.configure(command=self.filter)

    def filter(self):
        media_filter = self.filter_entry.get().upper()  # gets the users requested filter and stores it in upper class
        data = self.file.load()
        self.main_screen.table.delete(*self.main_screen.table.get_children())  # clears the table
        for record in data:
            media_type = self.file.get_type(record)  # gets the media type
            if media_type == media_filter:  # if type equals what the user wants then display record
                self.show_record(record)
