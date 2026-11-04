
import uuid

from backend.database.connection import get_connection


PROFILE_SECTIONS = {
    "current_project",
    "interests",
    "strengths",
    "struggles",
    "supports",
    "notes",
}


def validate_section(section):
    if section not in PROFILE_SECTIONS:
        raise ValueError(f"Invalid profile section: {section}")


def get_profile(student_id):
    """Load AI summaries and teacher notes for a student."""

    with get_connection() as conn:
        student = conn.execute(
            "SELECT id FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        if student is None:
            return None

        summaries = conn.execute(
            """
            SELECT section, ai_summary, updated_at
            FROM profile_sections
            WHERE student_id = ?
            """,
            (student_id,),
        ).fetchall()

        notes = conn.execute(
            """
            SELECT id, section, educator_id, note_text,
                   created_at, updated_at
            FROM teacher_notes
            WHERE student_id = ?
            ORDER BY created_at, id
            """,
            (student_id,),
        ).fetchall()

    profile = {
        section: {
            "ai_summary": "",
            "teacher_notes": [],
        }
        for section in PROFILE_SECTIONS
    }

    for row in summaries:
        if row["section"] in profile:
            profile[row["section"]]["ai_summary"] = row["ai_summary"]

    for row in notes:
        if row["section"] in profile:
            profile[row["section"]]["teacher_notes"].append(dict(row))

    return profile


def update_ai_summary(student_id, section, summary):
    """Update an AI summary without modifying teacher notes."""

    validate_section(section)

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO profile_sections
                (student_id, section, ai_summary)
            VALUES (?, ?, ?)
            ON CONFLICT(student_id, section)
            DO UPDATE SET
                ai_summary = excluded.ai_summary,
                updated_at = CURRENT_TIMESTAMP
            """,
            (student_id, section, summary),
        )

    return get_profile(student_id)


def add_teacher_note(student_id, section, note_text, educator_id=None):
    """Add a permanent teacher note to a profile section."""

    validate_section(section)

    if not note_text or not note_text.strip():
        raise ValueError("Teacher note cannot be empty")

    note_id = str(uuid.uuid4())

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO teacher_notes
                (id, student_id, section, educator_id, note_text)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                note_id,
                student_id,
                section,
                educator_id,
                note_text.strip(),
            ),
        )

    return note_id


def update_teacher_note(note_id, note_text):
    """Edit a teacher note explicitly, without touching AI summaries."""

    if not note_text or not note_text.strip():
        raise ValueError("Teacher note cannot be empty")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE teacher_notes
            SET note_text = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (note_text.strip(), note_id),
        )

        if cursor.rowcount == 0:
            raise ValueError("Teacher note not found")


def delete_teacher_note(note_id):
    """Delete a note only through an explicit operation."""

    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM teacher_notes WHERE id = ?",
            (note_id,),
        )

        if cursor.rowcount == 0:
            raise ValueError("Teacher note not found")
