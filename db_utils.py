# File for SQLite Functions
import sqlite3

file_name = "crawldata.db"

def open_database(filename):
    connection_obj = sqlite3.connect(filename)
    cursor_obj = connection_obj.cursor()



open_database(file_name)