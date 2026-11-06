"""FastAPI router for the avatar module (prefix /avatar)."""
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, Response

from backend.avatar import catalog, growth, renderer, storage
from backend.avatar.models import Avatar, Event, Pet, SaveRequest, Student
from backend.avatar.questionnaire import QUESTIONS

router = APIRouter(prefix="/avatar", tags=["avatar"])


def _check_choices(a: Avatar) -> None:
    """Only choices listed in the catalog are allowed (closed choices, never free text)."""
    found = catalog.problems(a.base, a.options)
    if found:
        raise HTTPException(status_code=422, detail=found)


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
def get_catalog() -> dict:
    return catalog.public_catalog()


@router.get("/questionnaire")
def questionnaire_questions() -> list:
    return QUESTIONS


@router.get("/preview.svg")
def preview_svg(request: Request, base: str) -> Response:
    """Draws unsaved choices, so the onboarding screens can show a live preview.

    The choices come as extra query parameters named after the option, e.g. ?base=human&hair=short01&skin=ffdbac
    """
    picked = {k: v for k, v in request.query_params.items() if k != "base"}
    avatar = Avatar(base=base, options=picked)
    _check_choices(avatar)
    return Response(renderer.render(avatar), media_type="image/svg+xml")


@router.get("/{student_id}")
def get_student(student_id: UUID) -> Student:
    return _get_or_404(student_id)


@router.put("/{student_id}")
def save_student(student_id: UUID, body: SaveRequest) -> Student:
    _check_choices(body.avatar)
    student = storage.load(student_id)
    if student is None:
        student = Student(student_id=student_id, avatar=body.avatar, pet=Pet(type=body.pet_type), preferences=body.preferences)
    else:  # editing later: keep the pet's growth and the support history
        student.avatar = body.avatar
        student.preferences = body.preferences
    storage.save(student)
    return student


@router.get("/{student_id}/render.svg")
def render_svg(student_id: UUID) -> Response:
    student = _get_or_404(student_id)
    return Response(renderer.render(student.avatar), media_type="image/svg+xml")


@router.post("/{student_id}/events")
def post_event(student_id: UUID, event: Event) -> dict:
    student = _get_or_404(student_id)
    result = growth.apply_event(student, event)
    storage.save(student)  # shortcut: read-then-write, fine for one user; use a transaction with the shared DB
    return result
