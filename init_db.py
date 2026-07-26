import sqlite3

connection = sqlite3.connect("database.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT NOT NULL,

    email TEXT NOT NULL UNIQUE,

    password TEXT NOT NULL

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    amount REAL NOT NULL,

    category TEXT NOT NULL,

    description TEXT,

    date TEXT NOT NULL,

    FOREIGN KEY(user_id) REFERENCES users(id)

)
""")

connection.commit()
connection.close()

print("Database created successfully!")