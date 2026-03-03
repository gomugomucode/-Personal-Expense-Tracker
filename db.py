
import sqlite3
from datetime import datetime 

def init_db():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute(''' 
CREATE TABLE IF NOT EXITS categories(
    id INTEGER PRIMARY KEY,
    name REAL UNIQUE,

);''')

    cursor.execute(''' CREATE TABLE IF NOT EXITS expenses(
        id INTEGER PRIMARY KEY,
        amount REAL,
        description TEXT, 
        date TEXT, 
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories(id),
    );
    ''')

 # Add some default categories
    default_cats = [('Food',), ('Transport',), ('Entertainment',), ('Rent',) ,('Electronics',), ('Books',), ('Clothing',),]
    cursor.executemany("INSERT OR IGNORE INTO categories (name) VALUES (?)", default_cats)

    conn.commit()
    return conn