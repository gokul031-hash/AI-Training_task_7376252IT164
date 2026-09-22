# Student Expense Assistant — Chatbot vs Rule-Based Workflow vs AI Agent

## Agentic AI: Foundations and Open-Source Practice — Day 1 Task

This project demonstrates the difference between a **Plain Chatbot**, a **Rule-Based Workflow**, and an **AI Agent** using the same private-data scenario.

The selected scenario is a **Student Expense Assistant**, where personal expense information is stored in a local SQLite database.

The project demonstrates the core Agentic AI concept:

**AI Agent = LLM + Tools + Loop**

---

## Project Scenario

A student has private expense records containing information such as:

- Date
- Category
- Amount
- Description

Example questions include:

- How much did I spend on food?
- How much did I spend on travel?
- What is my total expense?
- What was my highest expense?
- Analyze my expenses.

The same problem is implemented using three different approaches.

---

## 1. Plain Chatbot

The Plain Chatbot uses an LLM through the **Groq API**.

It uses the OpenAI Python client:

```python
from openai import OpenAI
```

The Groq API is accessed using its OpenAI-compatible endpoint.

The chatbot does **not** have access to the private SQLite expense database.

### Flow

```text
User
  ↓
Groq LLM
  ↓
Response
```

### Limitation

If the user asks:

```text
How much did I spend on food?
```

the chatbot cannot determine the actual amount because it cannot access the user's private expense records.

---

## 2. Rule-Based Workflow

The Rule-Based Workflow does **not use an LLM**.

Instead, it uses predefined Python conditions and directly accesses the SQLite database.

Example:

```python
if "food" in question:
    # Calculate food expenses

elif "travel" in question:
    # Calculate travel expenses

elif "total" in question:
    # Calculate total expenses
```

### Flow

```text
User
  ↓
Predefined Rules
  ↓
SQLite Database
  ↓
Result
```

### Limitation

The system only understands requests that have already been anticipated and programmed.

Different or unexpected questions may not be handled correctly.

---

## 3. AI Agent

The AI Agent combines:

```text
LLM + Tools + Loop
```

The LLM is accessed through the **Groq API**, while Python functions act as tools for accessing the private SQLite database.

Available tools can perform operations such as:

- Search expense records
- Calculate total expenses
- Calculate category expenses
- Find the highest expense

### Flow

```text
User Request
     ↓
Groq LLM
     ↓
Understand Request
     ↓
Select Tool
     ↓
SQLite Database
     ↓
Observe Result
     ↓
Groq LLM
     ↓
Final Response
```

Unlike the plain chatbot, the AI Agent can use tools to obtain information from private data before producing its final response.

---

## Technologies Used

- Python
- Groq API
- OpenAI Python SDK
- SQLite
- python-dotenv
- Git
- GitHub

---

## Project Structure

```text
day1-agentic-ai/
│
├── chatbot/
│   └── chatbot.py
│
├── rule_based/
│   └── rule_based.py
│
├── agent/
│   ├── agent.py
│   └── tools.py
│
├── database/
│   └── expenses.db
│
├── Output/
│   ├── chatbot.png
│   ├── rule_based.png
│   └── agent.png
│
├── setup_database.py
├── requirements.txt
├── analysis.md
├── README.md
├── .env
└── .gitignore
```

---

# Installation and Setup

## Step 1 — Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd day1-agentic-ai
```

---

## Step 2 — Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
openai
python-dotenv
```

SQLite support is included with Python.

---

## Step 4 — Configure Groq API Key

Create a `.env` file in the root directory:

```text
GROQ_API_KEY=your_groq_api_key
```

The Groq client is configured using the OpenAI Python package:

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
```

> **Important:** Never upload your `.env` file or API key to GitHub.

The `.gitignore` file should contain:

```text
.env
venv/
__pycache__/
*.pyc
```

---

# Database Setup

The private expense information is stored in:

```text
database/expenses.db
```

To create and populate the database, run:

```bash
python setup_database.py
```

Expected output:

```text
Database created successfully.
```

---

# Running the Project

## 1. Run the Plain Chatbot

From the project root:

```bash
python chatbot/chatbot.py
```

Example:

```text
Plain Chatbot

You: How much did I spend on food?

Chatbot:
I cannot access your private expense records.
```

---

## 2. Run the Rule-Based Workflow

```bash
python rule_based/rule_based.py
```

Example:

```text
Rule-Based Expense System

You: How much did I spend on food?

System:
You spent ₹570.00 on food.
```

---

## 3. Run the AI Agent

Run the AI Agent using:

```bash
python agent/agent.py
```

Example:

```text
AI Expense Agent

You: Analyze my food expenses.

Agent:
You spent ₹570 on food based on your private expense records.
```

The AI Agent uses the LLM together with tools that access the SQLite database.

---

# Comparison

| Feature | Plain Chatbot | Rule-Based Workflow | AI Agent |
|---|---|---|---|
| LLM | Yes | No | Yes |
| Predefined Rules | No | Yes | Some control logic |
| Tool Usage | No | Fixed database operations | Tool-based |
| Private Data Access | No | Yes | Yes through tools |
| Decision Making | LLM response generation | Fixed conditions | LLM-based tool selection |
| Flexibility | Limited for private data | Limited to programmed cases | Handles more varied requests |
| Multi-Step Tasks | Limited | Predefined | Can use multiple steps |
| Automation | Limited | Fixed | Dynamic |

---

# Output Screenshots

The `Output` directory contains screenshots showing the execution of all three approaches.

```text
Output/
├── chatbot.png
├── rule_based.png
└── agent.png
```

These screenshots demonstrate how each system responds to the private-data expense scenario.

---

# Key Concept

The main purpose of this project is to understand the difference between the three approaches.

### Plain Chatbot

```text
LLM → Response
```

Useful for general conversation but cannot access the private expense database in this implementation.

### Rule-Based Workflow

```text
Rules → Database → Result
```

Reliable for predefined operations but limited to conditions written by the programmer.

### AI Agent

```text
LLM → Select Tool → Execute Tool → Observe Result → Respond
```

The AI Agent combines reasoning through an LLM with external tools and private data.

Therefore:

```text
AI Agent = LLM + Tools + Loop
```

---

# Security

The Groq API key is stored in the `.env` file.

The `.env` file is excluded from Git using `.gitignore`.

Never commit API keys or other secrets to a public GitHub repository.

---

# Analysis

A detailed comparison of the three approaches is available in:

```text
analysis.md
```

It contains:

- Explanation of each approach
- Comparison table
- Suitability analysis
- Conclusion

---

# Conclusion

This project demonstrates how the same Student Expense Assistant problem can be implemented using three different approaches.

A **Plain Chatbot** uses an LLM to generate conversational responses but has no access to private expense records in this project.

A **Rule-Based Workflow** uses predefined conditions and directly queries the private SQLite database without using an LLM.

An **AI Agent** combines an LLM with tools and an execution loop. It can understand a request, select an appropriate tool, access private data, observe the result, and use that information to produce a final response.

This demonstrates the fundamental Agentic AI architecture:

**LLM + Tools + Loop = AI Agent**