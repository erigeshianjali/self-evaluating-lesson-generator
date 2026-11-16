# Self-Evaluating Lesson Generator

A Python-based lesson generation and self-evaluation workflow that creates beginner-friendly lessons, evaluates them against six teaching criteria, improves them when necessary, and stores evaluation history using SQLite.

## Project Overview

The Self-Evaluating Lesson Generator is designed to produce clear and structured educational content for a given topic.

The workflow:
1. Takes a lesson topic as input.
2. Generates beginner-friendly lesson content.
3. Evaluates the lesson using six criteria.
4. Identifies failed criteria and attempts to improve the lesson.
5. Re-evaluates the improved lesson.
6. Stores evaluation history and recurring failure information in an SQLite database.

The workflow allows a maximum of three attempts: one initial attempt and up to two improvement attempts.

## Evaluation Criteria

Each lesson is evaluated using these six criteria:

1. **Accuracy and Grounding** – Checks whether the lesson has appropriate supporting evidence. Accuracy remains pending when it has not been independently verified.
2. **Beginner-Friendly Language** – Checks whether the content is easy for beginners to understand.
3. **Teaching by Example** – Checks whether the lesson includes examples.
4. **No Unexplained Jargon** – Checks whether technical terms are explained.
5. **Topic Coverage** – Checks for definition, importance, working process, advantages, and limitations.
6. **Coherent Teaching Flow** – Checks whether the lesson follows a logical structure.

A lesson is approved only when all six criteria pass.

## Technologies Used

- Python
- FastAPI
- SQLite
- HTML
- Uvicorn

## Project Structure

```text
self-evaluating-lesson-generator/
│
├── backend/
│   ├── accuracy_checker.py
│   ├── agent.py
│   ├── evaluator.py
│   ├── evidence_checker.py
│   ├── improver.py
│   ├── learning.py
│   ├── lesson_generator.py
│   ├── main.py
│   ├── memory.py
│   ├── source_reader.py
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
│
└── README.md
```

## Setup and Installation

### Prerequisites

- Python 3.10 or later
- Visual Studio Code or another code editor
- A web browser

### Step 1: Clone the repository

```bash
git clone https://github.com/erigeshianjali/self-evaluating-lesson-generator.git
```

This downloads the project from GitHub to your computer.

### Step 2: Open the project folder

```bash
cd self-evaluating-lesson-generator/backend
```

This moves the terminal into the backend folder.

### Step 3: Create a virtual environment

```bash
py -m venv venv
```

This creates an isolated Python environment for the project dependencies.

### Step 4: Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

This installs the Python packages required by the project.

## Running the Application

From the backend folder, run:

```bash
python -m uvicorn main:app --reload
```

This starts the FastAPI application with automatic reloading when code changes.

Open the browser at:

```text
http://127.0.0.1:8000
```

## Database and Memory

The project uses SQLite to store lesson evaluation history and recurring failure information.

The database is created locally when the application runs. It does not need to be uploaded to GitHub.

## Important Notes and Limitations

- The current demo uses rule-based lesson generation and evaluation logic.
- The evidence checker identifies potential textual support but does not guarantee factual correctness.
- Accuracy must be independently reviewed; pending accuracy should not be treated as verified.
- No paid API key is required to run the current rule-based demo.

## Conclusion

The Self-Evaluating Lesson Generator demonstrates a structured lesson generation and evaluation workflow with automatic improvement attempts and persistent evaluation history. It aims to make educational content clearer, more organized, and beginner-friendly.
