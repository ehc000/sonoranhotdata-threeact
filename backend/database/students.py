
import json
import uuid

from backend.database.connection import get_connection


def create_student(name, email=None, grade_level=None):
    """Create a student and their default preferences."""
    student_id = str(uuid.uuid4())

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO students (id, name, email, grade_level)
            VALUES (?, ?, ?, ?)
            """,
            (student_id, name, email, grade_level),
        )

        conn.execute(
            """
            INSERT INTO student_preferences (student_id)
            VALUES (?)
            """,
            (student_id,),
        )

    return get_student(student_id)


def get_student(student_id):
    """Return a student and their preferences."""
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT
                s.id,
                s.name,
                s.email,
                s.grade_level,
                p.interests,
                p.interests_text,
                p.learning_preferences_text,
                p.content_format,
                p.sensory_sensitive,
                p.help_mode,
                p.break_minutes
            FROM students s
            LEFT JOIN student_preferences p
                ON s.id = p.student_id
            WHERE s.id = ?
            """,
            (student_id,),
        ).fetchone()

    if row is None:
        return None

    student = dict(row)
    student["interests"] = json.loads(
        student["interests"] or "[]"
    )
    student["sensory_sensitive"] = bool(
        student["sensory_sensitive"]
    )

    return student


ALLOWED_PREFERENCES = {
    "interests",
    "interests_text",
    "learning_preferences_text",
    "content_format",
    "sensory_sensitive",
    "help_mode",
    "break_minutes",
}


def update_preferences(student_id, **changes):
    """Update only the preference fields provided."""
    if not changes:
        return get_student(student_id)

    invalid = set(changes) - ALLOWED_PREFERENCES
    if invalid:
        raise ValueError(f"Unknown preference fields: {invalid}")

    if "interests" in changes:
        changes["interests"] = json.dumps(changes["interests"])

    if "sensory_sensitive" in changes:
        changes["sensory_sensitive"] = int(
            changes["sensory_sensitive"]
        )

    columns = ", ".join(f"{key} = ?" for key in changes)
    values = list(changes.values())

    with get_connection() as conn:
        cursor = conn.execute(
            f"""
            UPDATE student_preferences
            SET {columns}
            WHERE student_id = ?
            """,
            values + [student_id],
        )

        if cursor.rowcount == 0:
            raise ValueError("Student preferences not found")

    return get_student(student_id)
