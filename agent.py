import os
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI

# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv()

# ==========================================
# DATABASE PATH
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(
    BASE_DIR,
    "database",
    "expenses.db"
)

# ==========================================
# GROQ + OPENAI CLIENT
# ==========================================

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# ==========================================
# TOOL 1 - FOOD EXPENSE
# ==========================================

def get_food_expense():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE LOWER(category) = 'food'
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result or 0


# ==========================================
# TOOL 2 - TRAVEL EXPENSE
# ==========================================

def get_travel_expense():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE LOWER(category) = 'travel'
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result or 0


# ==========================================
# TOOL 3 - BOOK EXPENSE
# ==========================================

def get_books_expense():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE LOWER(category) = 'books'
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result or 0


# ==========================================
# TOOL 4 - EDUCATION EXPENSE
# ==========================================

def get_education_expense():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE LOWER(category) = 'education'
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result or 0


# ==========================================
# TOOL 5 - TOTAL EXPENSE
# ==========================================

def get_total_expense():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result or 0


# ==========================================
# TOOL 6 - HIGHEST EXPENSE
# ==========================================

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

    if result:
        category, amount, description = result

        return (
            f"Highest expense: ₹{amount:.2f}, "
            f"Category: {category}, "
            f"Description: {description}"
        )

    return "No expenses found."


# ==========================================
# TOOL DEFINITIONS
# ==========================================

tools = [

    {
        "type": "function",
        "function": {
            "name": "get_food_expense",
            "description": "Get the total amount spent on food from the private expense database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_travel_expense",
            "description": "Get the total amount spent on travel from the private expense database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_books_expense",
            "description": "Get the total amount spent on books from the private expense database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_education_expense",
            "description": "Get the total amount spent on education from the private expense database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_total_expense",
            "description": "Get the total amount of all expenses from the private expense database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_highest_expense",
            "description": "Find the highest expense from the private expense database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


# ==========================================
# TOOL FUNCTION MAP
# ==========================================

available_functions = {

    "get_food_expense": get_food_expense,

    "get_travel_expense": get_travel_expense,

    "get_books_expense": get_books_expense,

    "get_education_expense": get_education_expense,

    "get_total_expense": get_total_expense,

    "get_highest_expense": get_highest_expense
}


# ==========================================
# AI AGENT
# ==========================================

def agent(question):

    messages = [

        {
            "role": "system",
            "content": """
You are a Student Expense AI Agent.

You have access to private expense data through tools.

When the user asks about expenses, select the
appropriate tool.

Do not invent private expense information.

Use the available tools whenever the question
requires private expense data.

After receiving the tool result, provide a
simple final answer to the user.
"""
        },

        {
            "role": "user",
            "content": question
        }
    ]


    # ======================================
    # AGENT LOOP
    # ======================================

    for step in range(5):

        print("\nThinking...")

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=messages,

            tools=tools,

            tool_choice="auto",

            parallel_tool_calls=False
        )

        message = response.choices[0].message


        # ==================================
        # NO TOOL NEEDED
        # ==================================

        if not message.tool_calls:

            return message.content


        # ==================================
        # ADD ASSISTANT MESSAGE
        # ==================================

        messages.append(message)


        # ==================================
        # EXECUTE TOOL
        # ==================================

        for tool_call in message.tool_calls:

            function_name = tool_call.function.name

            print("\nTool selected:")
            print(function_name)


            if function_name in available_functions:

                function = available_functions[function_name]

                result = function()

            else:

                result = "Unknown tool."


            print("Tool result:")
            print(result)


            # ==================================
            # SEND TOOL RESULT BACK TO MODEL
            # ==================================

            messages.append({

                "role": "tool",

                "tool_call_id": tool_call.id,

                "content": str(result)
            })


    return "The agent could not complete the request."


# ==========================================
# MAIN PROGRAM
# ==========================================

print("=" * 60)
print("                 AI EXPENSE AGENT")
print("=" * 60)

print("Private data source: SQLite database")

print("Tools available:")
print("1. Food expense")
print("2. Travel expense")
print("3. Books expense")
print("4. Education expense")
print("5. Total expense")
print("6. Highest expense")

print("\nType 'exit' to stop.")


while True:

    question = input("\nYou: ")

    if question.lower() == "exit":

        print("\nAgent stopped.")

        break


    answer = agent(question)


    print("\nAgent:")
    print(answer)