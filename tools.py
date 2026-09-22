import sqlite3

DATABASE = "database/expenses.db"


def search_expenses(category=None):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if category:

        cursor.execute("""
            SELECT date, category, amount, description
            FROM expenses
            WHERE LOWER(category) = LOWER(?)
            ORDER BY date
        """, (category,))

    else:

        cursor.execute("""
            SELECT date, category, amount, description
            FROM expenses
            ORDER BY date
        """)

    results = cursor.fetchall()

    connection.close()

    return results


def calculate_total(category=None):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if category:

        cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE LOWER(category) = LOWER(?)
        """, (category,))

    else:

        cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
        """)

    result = cursor.fetchone()[0]

    connection.close()

    return result or 0


def highest_expense():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT date, category, amount, description
        FROM expenses
        ORDER BY amount DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    connection.close()

    return result