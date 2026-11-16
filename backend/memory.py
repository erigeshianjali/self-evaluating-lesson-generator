import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "lesson_memory.db"

def connect_database():
    return sqlite3.connect(DB_PATH)

def create_table():
    with connect_database() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                attempt INTEGER NOT NULL,
                failed_criteria TEXT,
                feedback TEXT,
                final_status TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_evaluation(topic, attempt, failed_criteria, feedback, final_status):
    create_table()
    with connect_database() as connection:
        connection.execute("""
            INSERT INTO evaluations
            (topic, attempt, failed_criteria, feedback, final_status)
            VALUES (?, ?, ?, ?, ?)
        """, (topic, attempt, failed_criteria, feedback, final_status))

def get_evaluations(limit=100):
    create_table()
    with connect_database() as connection:
        rows = connection.execute("""
            SELECT id, topic, attempt, failed_criteria, feedback, final_status, created_at
            FROM evaluations ORDER BY id DESC LIMIT ?
        """, (limit,)).fetchall()
    return rows
