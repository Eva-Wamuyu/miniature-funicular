import sqlite3


def create_tables():
    conn = sqlite3.connect('restful.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
    name TEXT NOT NULL,
    email TEXT NOT NULL 
)
''')

    cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    account_number TEXT NOT NULL,
    balance REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
)
''')

    cursor.execute('''
CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    card_number TEXT NOT NULL,
    card_type TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts (id)
)
''')

    conn.commit()


