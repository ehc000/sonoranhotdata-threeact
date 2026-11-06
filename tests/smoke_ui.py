"""Walks through the Streamlit screens like a student would (API must be running).
Run from the project root: python -m tests.smoke_ui"""
import os
from pathlib import Path
from uuid import uuid4

import requests
from streamlit.testing.v1 import AppTest

API = os.environ.get("API_BASE_URL", "http://localhost:8000") + "/avatar"
sid = str(uuid4())  # fictional student

APP = Path(__file__).resolve().parent.parent / "ui" / "companion_app.py"
at = AppTest.from_file(str(APP), default_timeout=60)
at.query_params["student"] = sid
at.run()
assert not at.exception, at.exception


def press(key: str = None, label: str = None) -> None:
    button = at.button(key=key) if key else next(b for b in at.button if b.label == label)
    button.click().run()
    assert not at.exception, at.exception


assert at.title[0].value == "Let's create your companion"
press(label="Start")
assert at.title[0].value == "Pick a type"
press("base-robot")
press(label="Next →")
assert at.title[0].value == "Make it yours"
press("eyes-wide")
press("glow-5eead4")
press(label="Next →")
at.text_input[0].set_value("Bip").run()  # the companion's name
press(label="Next →")
assert at.caption[0].value == "Question 1 of 6"
at.text_input[0].set_value("Sam").run()  # nickname
press(label="Next →")
press(label="Next →")  # interests keep the teacher's pre-filled choices
press(label="Next →")  # project types can be skipped
for pick in ("read_aloud-yes", "help_mode-ask", "goal-working_alone"):
    press(pick)
    if pick != "goal-working_alone":
        press(label="Next →")
press(label="Done ✓")

saved = requests.get(f"{API}/{sid}").json()
assert saved["avatar"] == {"base": "robot", "options": {"eyes": "wide", "glow": "5eead4"}, "display_name": "Bip", "static_mode": False}
assert saved["preferences"] == {"nickname": "Sam", "interests": ["cars", "space"], "work_style": [], "read_aloud": True,
                                "help_mode": "ask", "goal": "working_alone", "sounds_and_animations": False, "break_minutes": 2}
assert at.title[0].value == "Bip"

press("lesson_completed")
assert any("Reward suggestion" in m.value for m in at.markdown) or any("Reward suggestion" in t.value for t in at.text), "teacher view missing"

press(label="Change my companion")  # editing keeps the saved answers, starts at the type step
assert at.title[0].value == "Pick a type"
press("base-human")  # another base starts again from its own defaults
press(label="Next →")
press("hair-long05")
press("skin-8d5524")
press(label="Next →")
press(label="Done ✓")
again = requests.get(f"{API}/{sid}").json()
assert again["avatar"]["base"] == "human" and again["avatar"]["options"] == {"hair": "long05", "skin": "8d5524"}
assert again["preferences"] == saved["preferences"] and again["pet"]["growth"] > 0

print("UI smoke test OK")
