"""Quick self-check for avatar/growth.py. Run from the project root: python -m tests.check_growth"""
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from backend.avatar.growth import apply_event, fading_trend, stage_for
from backend.avatar.models import Avatar, Event, Pet, Preferences, Student, SupportEntry

NOW = datetime(2026, 11, 2, tzinfo=timezone.utc)


def new_student() -> Student:
    avatar = Avatar(base="robot")
    return Student(student_id=uuid4(), avatar=avatar, pet=Pet(type="plant"), preferences=Preferences())


def entry(day: int, hints: int) -> SupportEntry:
    return SupportEntry(lesson_id=uuid4(), hints=hints, at=NOW + timedelta(days=day))


# stages
assert [stage_for(g) for g in (0, 49, 50, 119, 120, 219, 220, 349, 350, 9999)] == [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]

# events add growth, help_requested adds none and is logged
s = new_student()
lesson = uuid4()
apply_event(s, Event(event="card_completed", at=NOW))
assert s.pet.growth == 5
apply_event(s, Event(event="help_requested", lesson_id=lesson, at=NOW))
assert s.pet.growth == 5 and s.support_history[0].help_requested == 1

# no-hint bonus and the reward suggestion
result = apply_event(s, Event(event="lesson_completed", lesson_id=lesson, hints=0, at=NOW))
assert s.pet.growth == 35 and "no hints" in result["reward_suggestion"]
assert len(s.support_history) == 1  # same lesson, same entry
result = apply_event(s, Event(event="lesson_completed", lesson_id=uuid4(), hints=1, at=NOW))
assert s.pet.growth == 55 and s.pet.stage == 2 and "one hint" in result["reward_suggestion"]

# a lesson event without lesson_id is rejected
try:
    Event(event="lesson_completed", at=NOW)
    raise AssertionError("expected a validation error")
except ValueError:
    pass

# fading trend
assert fading_trend([entry(0, 3)]) == "not_enough_data"
assert fading_trend([entry(0, 4), entry(1, 3), entry(2, 1), entry(3, 0)]) == "falling"
assert fading_trend([entry(0, 0), entry(1, 1), entry(2, 3), entry(3, 4)]) == "rising"
assert fading_trend([entry(i, 2) for i in range(4)]) == "steady"

print("growth checks OK")
