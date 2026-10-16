# File for SQLite Functions
import sqlite3
import pandas as pd
file_name = "crawldata.db"

def open_database(filename):
    try:
        connection_obj = sqlite3.connect(filename)
        cursor = connection_obj.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crawldata (
                url TEXT PRIMARY KEY,
                title TEXT,
                date_retrieved INTEGER,
                text TEXT NOT NULL
            )
        ''')
        return connection_obj
    except Exception as e:
        print("Database Error:",e)

        return None

def insert_crawldata(cursor,url,title,date_retrieved,text):
    cursor.execute('''
    INSERT INTO crawldata (url,title,date_retrieved,text) VALUES (?,?,?,?,?)
        ''', (url,title,date_retrieved,text))

def insert_many_crawldata(cursor,data):
    cursor.executemany(''' 
    INSERT INTO crawldata (url,title,dateretrieved,text) VALUES (?,?,?,?)''', data)

def fetch_all_data(cursor):
    cursor.execute('''SELECT * FROM crawldata ''')
    rows = cursor.fetchall()
    all_urls = []
    all_titles = []
    all_text = []
    for row in rows:
        all_urls.append(row[0])
        all_titles.append(row[1])
        all_text.append(row[3])

    return all_urls,all_titles,all_text

def all_data_to_csv():
    with sqlite3.connect("crawldata.db") as conn:
        # Read the entire table directly into a Pandas DataFrame
        df = pd.read_sql_query("SELECT * FROM crawldata", conn)
        df.to_csv("crawl_exports.csv", index=False)

def read_csv():
    df = pd.read_csv("crawl_exports.csv",usecols=[0,1,3])
    return df

def remove_line_breaks():
    with sqlite3.connect("crawldata.db") as conn:
        # Read the entire table directly into a Pandas DataFrame
        df = pd.read_sql_query("SELECT * FROM crawldata", conn)
        df['text'] = df['text'].str.replace("\n", " ")
        df.to_csv("crawl_exports.csv", index=False)


def close_database(connection_obj):
    connection_obj.close()

