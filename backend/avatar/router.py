"""FastAPI router for the avatar module (prefix /avatar)."""
import json
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Response

from backend.avatar import growth, renderer, storage
from backend.avatar.models import Avatar, Event, Pet, SaveRequest, Student
from backend.avatar.questionnaire import QUESTIONS

router = APIRouter(prefix="/avatar", tags=["avatar"])

CATALOG = json.loads((Path(__file__).parent / "catalog.json").read_text(encoding="utf-8"))


def _check_choices(a: Avatar, pet_type: str) -> None:
    """Only options listed in the catalog are allowed (closed choices, never free text)."""
    problems = []
    if a.base not in CATALOG["bases"]:
        problems.append(f"unknown base: {a.base}")
    elif a.head not in CATALOG["heads"][a.base]:
        problems.append(f"head {a.head} does not belong to base {a.base}")
    if a.primary_color.upper() not in CATALOG["colors"]:
        problems.append(f"unknown color: {a.primary_color}")
    if a.eyes not in CATALOG["eyes"]:
        problems.append(f"unknown eyes: {a.eyes}")
    if pet_type not in CATALOG["pets"]:
        problems.append(f"unknown pet: {pet_type}")
    if problems:
        raise HTTPException(status_code=422, detail=problems)


def _get_or_404(student_id: UUID) -> Student:
    student = storage.load(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


# These fixed paths come before /{student_id} so "catalog" is not read as a student id.
@router.get("/catalog")
def catalog() -> dict:
    return CATALOG


@router.get("/questionnaire")
def questionnaire_questions() -> list:
    return QUESTIONS


@router.get("/preview.svg")
def preview_svg(base: str, primary_color: str, head: str, eyes: str, pet_type: str, stage: int = Query(1, ge=1, le=5)) -> Response:
    """Draws unsaved choices, so the onboarding screens can show a live preview."""
    try:
        avatar = Avatar(base=base, primary_color=primary_color, head=head, eyes=eyes)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    _check_choices(avatar, pet_type)
    return Response(renderer.render(avatar, Pet(type=pet_type, stage=stage)), media_type="image/svg+xml")


@router.get("/{student_id}")
def get_student(student_id: UUID) -> Student:
    return _get_or_404(student_id)


@router.put("/{student_id}")
def save_student(student_id: UUID, body: SaveRequest) -> Student:
    _check_choices(body.avatar, body.pet_type)
    student = storage.load(student_id)
    if student is None:
        student = Student(student_id=student_id, avatar=body.avatar, pet=Pet(type=body.pet_type), preferences=body.preferences)
    else:  # editing later: keep the pet's growth and the support history
        student.avatar = body.avatar
        student.pet.type = body.pet_type
        student.preferences = body.preferences
    storage.save(student)
    return student


@router.get("/{student_id}/render.svg")
def render_svg(student_id: UUID) -> Response:
    student = _get_or_404(student_id)
    return Response(renderer.render(student.avatar, student.pet), media_type="image/svg+xml")


@router.post("/{student_id}/events")
def post_event(student_id: UUID, event: Event) -> dict:
    student = _get_or_404(student_id)
    result = growth.apply_event(student, event)
    storage.save(student)  # shortcut: read-then-write, fine for one user; use a transaction with the shared DB
    return result
