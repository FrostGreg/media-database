import sqlite3
from dotenv import load_dotenv
import os


class File:
    def __init__(self):
        self.db = sqlite3.connect('media.db')
        self.cursor = self.db.cursor()

        # create table in database if not already there
        if not self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='records';"):
            self.cursor.execute(
                "CREATE TABLE records(id int PRIMARY KEY, name VARCHAR(255),"
                + " author VARCHAR(255), year int, type VARCHAR(255));")
            self.db.commit()

    def close(self):
        return self.db.close()

    # Opens the database file and stores the content in the data variable
    def load(self):
        return self.cursor.execute("SELECT * FROM records;")

    # works through each record until the requested one is found
    def find_record(self, rec_id):
        return self.cursor.execute("SELECT * FROM records WHERE id = ?", (rec_id,))

    def get_index(self, record):
        return record[0]

    def get_name(self, record):
        return record[1]

    def get_author(self, record):
        return record[2]

    def get_date(self, record):
        return record[3]

    def get_type(self, record):
        return record[4]

    # converts media type so it can taken from and put into radio buttons
    def type_convert(self, media_type, method):
        if method == "numToChar":
            converter = {0: "DVD", 1: "CD", 2: "GAME"}
        else:
            converter = {"DVD": 0, "CD": 1, "GAME": 2}

        return converter[media_type]
