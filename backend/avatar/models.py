"""Pydantic models: Avatar, Pet, Preferences, SupportEntry (plus the request bodies).

A "model" is a description of what a piece of data must look like.
Pydantic checks incoming data against it and rejects anything that does not fit.
"""
from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class Avatar(BaseModel):
    base: str  # human / animal / robot / creature
    options: dict[str, str] = {}  # option id -> choice id, e.g. {"hair": "short01"}; anything missing uses the default
    display_name: str = Field(default="", max_length=20)  # the avatar's name, not the student's
    static_mode: bool = False  # True turns off all motion


class Pet(BaseModel):
    type: str
    stage: int = 1  # 1 to 5, never goes down
    growth: int = 0  # internal number, never shown to the student


class Preferences(BaseModel):
    nickname: str = Field(default="", max_length=20)  # what the buddy calls the student, never the full name
    interests: list[Annotated[str, Field(max_length=40)]] = Field(default=[], max_length=30)
    work_style: list[Literal["hands_on", "design", "computer", "writing"]] = []
    read_aloud: bool = False  # access need: True reads every step out loud. Steps always show pictures and text
    help_mode: Literal["ask", "check_in"] = "check_in"  # check_in = the app checks on the student if they seem stuck
    goal: Literal["finishing_projects", "asking_for_help", "staying_organized", "working_alone"] | None = None  # one thing to get better at
    sounds_and_animations: bool = False  # calm by default; a settings switch, not a question
    break_minutes: Literal[2, 5] = 2  # set by the teacher, not asked to the student


class SupportEntry(BaseModel):
    """Hints and help presses for one lesson. Only stored; never used against the student."""
    lesson_id: UUID
    hints: int = 0
    help_requested: int = 0
    at: datetime


class Student(BaseModel):
    """The one JSON document kept per student."""
    student_id: UUID
    avatar: Avatar
    pet: Pet
    preferences: Preferences
    support_history: list[SupportEntry] = []


class SaveRequest(BaseModel):
    """Body of PUT /avatar/{student_id}."""
    avatar: Avatar
    pet_type: str = "plant"  # pets are on hold: nothing shows or asks for them for now
    preferences: Preferences


class Event(BaseModel):
    """Body of POST /avatar/{student_id}/events."""
    event: Literal["card_completed", "lesson_completed", "checkin_done", "break_taken", "help_requested"]
    lesson_id: UUID | None = None
    hints: int = Field(default=0, ge=0)
    at: datetime

    @model_validator(mode="after")
    def lesson_id_needed(self):
        if self.event in ("lesson_completed", "help_requested") and self.lesson_id is None:
            raise ValueError(f"lesson_id is required for {self.event}")
        return self
