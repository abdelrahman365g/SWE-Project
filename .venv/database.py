import sqlite3

db = sqlite3.connect('database.db')
cur = db.cursor()

cur.execute("""
    CREATE TABLE User(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE Account(
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bank_name TEXT NOT NULL,
        account_number INTEGER NOT NULL,
        expiry_date TEXT NOT NULL,
        cvv INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
""")

cur.execute("""
    CREATE TABLE Transaction(
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        transaction_date TEXT NOT NULL,
        transaction_time TEXT NOT NULL,
        account_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        FOREIGN KEY (account_id) REFERENCES Account(account_id),
        FOREIGN KEY (category_id) REFERENCES Category(category_id)
    )
""")

cur.execute("""
    CREATE TABLE Category(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL,
        budget REAL NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE Report(
        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        format TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
""")

db.commit()
db.close()
