import sqlite3
from pathlib import Path
from memory import get_evaluations, DB_PATH

HINTS = {
    "accuracy_and_grounding": "Verify factual claims against trusted sources before approval.",
    "beginner_friendly": "Use short sentences and explain difficult words.",
    "teaches_by_example": "Include at least one practical, topic-related example.",
    "no_unexplained_jargon": "Define technical terms in simple language when first introduced.",
    "covers_key_points": "Include definition, importance, how it works, advantages, and limitations.",
    "coherent_flow": "Use an introduction, logically ordered sections, and a conclusion.",
}

def update_learning_hints():
    counts = {}
    for record in get_evaluations(limit=1000):
        failed = record[3] or ""
        for criterion in failed.split(","):
            criterion = criterion.strip()
            if criterion:
                counts[criterion] = counts.get(criterion, 0) + 1

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS learning_hints (
                criterion TEXT PRIMARY KEY,
                failure_count INTEGER NOT NULL,
                hint TEXT NOT NULL
            )
        """)
        for criterion, count in counts.items():
            if count >= 2 and criterion in HINTS:
                connection.execute("""
                    INSERT INTO learning_hints (criterion, failure_count, hint)
                    VALUES (?, ?, ?)
                    ON CONFLICT(criterion) DO UPDATE SET
                        failure_count=excluded.failure_count,
                        hint=excluded.hint
                """, (criterion, count, HINTS[criterion]))

def get_learning_hints():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS learning_hints (
                criterion TEXT PRIMARY KEY,
                failure_count INTEGER NOT NULL,
                hint TEXT NOT NULL
            )
        """)
        return connection.execute(
            "SELECT criterion, failure_count, hint FROM learning_hints ORDER BY criterion"
        ).fetchall()
