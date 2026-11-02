"""Local SQLite storage for student documents (to be replaced by the shared database).

One table, one row per student: the id and the whole JSON document.
The router only calls load() and save(), so swapping in the shared database later
means rewriting this file only.
"""
import os
import sqlite3
from contextlib import closing
from pathlib import Path
from uuid import UUID

from backend.avatar.models import Student

# The database file lives in the project root unless AVATAR_DB_PATH says otherwise.
DB_PATH = Path(os.environ.get("AVATAR_DB_PATH", Path(__file__).resolve().parents[2] / "avatar.db"))


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS students (student_id TEXT PRIMARY KEY, doc TEXT NOT NULL)")
    return conn


def load(student_id: UUID) -> Student | None:
    with closing(_connect()) as conn:
        row = conn.execute("SELECT doc FROM students WHERE student_id = ?", (str(student_id),)).fetchone()
    return Student.model_validate_json(row[0]) if row else None


def save(student: Student) -> None:
    with closing(_connect()) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO students (student_id, doc) VALUES (?, ?)",
            (str(student.student_id), student.model_dump_json()),
        )
        conn.commit()
