
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.database.connection import get_connection
from backend.database.students import (
    create_student,
    get_student,
    update_preferences,
)
from backend.database.profiles import (
    get_profile,
    add_teacher_note,
    update_ai_summary,
)
from backend.homeroom.service import get_student_projects

router = APIRouter(prefix="/api", tags=["database"])


class StudentCreate(BaseModel):
    name: str = Field(min_length=1)
    email: str | None = None
    grade_level: int | None = None


class PreferencesUpdate(BaseModel):
    interests: list[str] | None = None
    interests_text: str | None = None
    learning_preferences_text: str | None = None
    content_format: str | None = None
    sensory_sensitive: bool | None = None
    help_mode: str | None = None
    break_minutes: int | None = None


class TeacherNoteCreate(BaseModel):
    section: str
    note_text: str


@router.get("/students")
def list_students():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, email, grade_level FROM students ORDER BY name"
        ).fetchall()
        return [dict(row) for row in rows]


@router.post("/students")
def add_student(data: StudentCreate):
    return create_student(
        name=data.name,
        email=data.email,
        grade_level=data.grade_level,
    )


@router.get("/students/{student_id}")
def student_detail(student_id: str):
    student = get_student(student_id)
    if student is None:
        raise HTTPException(404, "Student not found")
    return student


@router.patch("/students/{student_id}/preferences")
def save_preferences(student_id: str, data: PreferencesUpdate):
    if get_student(student_id) is None:
        raise HTTPException(404, "Student not found")

    changes = data.model_dump(exclude_unset=True)
    changes = {k: v for k, v in changes.items() if v is not None}

    return update_preferences(student_id, **changes)


@router.get("/students/{student_id}/profile")
def student_profile(student_id: str):
    profile = get_profile(student_id)
    if profile is None:
        raise HTTPException(404, "Student not found")
    return profile


@router.post("/students/{student_id}/notes")
def save_teacher_note(student_id: str, data: TeacherNoteCreate):
    if get_student(student_id) is None:
        raise HTTPException(404, "Student not found")

    try:
        note_id = add_teacher_note(
            student_id, data.section, data.note_text
        )
    except ValueError as error:
        raise HTTPException(400, str(error))

    return {"id": note_id}


@router.get("/students/{student_id}/projects")
def student_projects(student_id: str):
    if get_student(student_id) is None:
        raise HTTPException(404, "Student not found")
    return get_student_projects(student_id)
