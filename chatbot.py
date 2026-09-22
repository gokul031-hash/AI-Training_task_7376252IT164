import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

print("Plain Chatbot")
print("Type 'exit' to stop.")

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
                You are a simple chatbot.
                You do not have access to the user's private
                expense database.
                Explain that you cannot access private records
                when the user asks about personal expenses.
                """
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    print("\nChatbot:")
    print(response.choices[0].message.content)