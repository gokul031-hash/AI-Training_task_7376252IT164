import sqlite3
import os

DATABASE = os.path.join("database", "expenses.db")

os.makedirs("database", exist_ok=True)

connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")

expenses = [
    ("2026-09-01", "Food", 120, "Lunch"),
    ("2026-09-02", "Travel", 80, "Bus"),
    ("2026-09-03", "Food", 150, "Dinner"),
    ("2026-09-04", "Books", 500, "Python book"),
    ("2026-09-05", "Travel", 100, "College bus"),
    ("2026-09-06", "Food", 200, "Restaurant"),
    ("2026-09-07", "Education", 300, "Course"),
    ("2026-09-08", "Travel", 60, "Auto"),
    ("2026-09-09", "Food", 100, "Breakfast"),
    ("2026-09-10", "Books", 250, "DSA book")
]

cursor.executemany("""
INSERT INTO expenses
(date, category, amount, description)
VALUES (?, ?, ?, ?)
""", expenses)

connection.commit()
connection.close()

print("Database created successfully.")