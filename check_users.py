import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

print("Email entered:", form.email.data)
cursor.execute("SELECT id, full_name, email FROM users")

users = cursor.fetchall()

print(users)

connection.close()