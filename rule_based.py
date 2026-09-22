import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(
    BASE_DIR,
    "database",
    "expenses.db"
)
import sqlite3

DATABASE = "database/expenses.db"


def get_category_total(category):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE LOWER(category) = LOWER(?)
    """, (category,))

    result = cursor.fetchone()[0]

    connection.close()

    return result or 0


def get_total():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result or 0


def get_highest_expense():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, amount, description
        FROM expenses
        ORDER BY amount DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    connection.close()

    return result


def process_question(question):

    question = question.lower()

    if "food" in question:

        total = get_category_total("Food")

        return f"You spent ₹{total:.2f} on food."

    elif "travel" in question:

        total = get_category_total("Travel")

        return f"You spent ₹{total:.2f} on travel."

    elif "books" in question:

        total = get_category_total("Books")

        return f"You spent ₹{total:.2f} on books."

    elif "total" in question:

        total = get_total()

        return f"Your total expense is ₹{total:.2f}."

    elif "highest" in question or "maximum" in question:

        category, amount, description = get_highest_expense()

        return (
            f"Your highest expense was ₹{amount:.2f} "
            f"for {description} under {category}."
        )

    else:

        return "Sorry, I only understand predefined expense questions."


print("Rule-Based Expense System")
print("Type 'exit' to stop.")

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    answer = process_question(question)

    print("\nSystem:")
    print(answer)