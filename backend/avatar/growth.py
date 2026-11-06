"""Pet growth: apply_event, stage thresholds, reward suggestion, fading trend.

Growth only ever goes up. Nothing here takes anything away from the student.
"""
from backend.avatar.models import Event, Student, SupportEntry

# How much each event adds. These numbers are internal; the student only sees the pet change.
GROWTH_PER_EVENT = {
    "card_completed": 5,
    "lesson_completed": 20,
    "checkin_done": 5,
    "break_taken": 5,  # taking a break is positive
    "help_requested": 0,  # never negative; only logged
}
NO_HINT_BONUS = 10  # extra growth for a lesson finished with no hints
STAGE_STARTS = [0, 50, 120, 220, 350]  # growth needed to reach stage 1..5


def stage_for(growth: int) -> int:
    return sum(growth >= start for start in STAGE_STARTS)


def reward_suggestion(hints: int) -> str:
    """One line the educator dashboard can show; the teacher decides what to do."""
    used = "no hints" if hints == 0 else "one hint" if hints == 1 else f"{hints} hints"
    return f"Finished a full lesson with {used} — consider a classroom reward."


def fading_trend(history: list[SupportEntry]) -> str:
    """Compare the support used in the older half of the lessons with the newer half."""
    if len(history) < 4:
        return "not_enough_data"
    ordered = sorted(history, key=lambda e: e.at)
    half = len(ordered) // 2
    older = ordered[:half]
    newer = ordered[-half:]  # same size as older, skips the middle lesson when the count is odd

    def average(entries: list[SupportEntry]) -> float:
        return sum(e.hints + e.help_requested for e in entries) / len(entries)

    if average(newer) < average(older):
        return "falling"  # needs less support
    if average(newer) > average(older):
        return "rising"
    return "steady"


def apply_event(student: Student, event: Event) -> dict:
    """Update the student's pet and support history in place; return what the API sends back."""
    points = GROWTH_PER_EVENT[event.event]
    if event.event == "lesson_completed" and event.hints == 0:
        points += NO_HINT_BONUS
    student.pet.growth += points
    student.pet.stage = stage_for(student.pet.growth)

    if event.event in ("lesson_completed", "help_requested"):
        entry = next((e for e in student.support_history if e.lesson_id == event.lesson_id), None)
        if entry is None:
            entry = SupportEntry(lesson_id=event.lesson_id, at=event.at)
            student.support_history.append(entry)
        if event.event == "help_requested":
            entry.help_requested += 1
        else:
            entry.hints = event.hints
            entry.at = event.at

    return {
        "stage": student.pet.stage,
        "reward_suggestion": reward_suggestion(event.hints) if event.event == "lesson_completed" else None,
        "fading_trend": fading_trend(student.support_history),
    }
