"""Smoke test against a running API (start it with run_api.ps1 first).
Run from the project root: python -m tests.smoke_api  (uses a fictional student id)"""
import os
from uuid import uuid4

import requests

BASE = os.environ.get("API_BASE_URL", "http://localhost:8000") + "/avatar"
sid, lesson = uuid4(), uuid4()
at = "2026-11-02T16:00:00Z"
body = {
    "avatar": {"base": "robot", "primary_color": "#A8C5DA", "head": "robot_round", "eyes": "dots", "display_name": "Bip"},
    "pet_type": "plant",
    "preferences": {"nickname": "Sam", "interests": ["cars", "space"], "read_aloud": True, "break_minutes": 2},
}

assert requests.get(f"{BASE}/catalog").json()["pet_stages"] == 5
assert requests.get(f"{BASE}/{sid}").status_code == 404
assert requests.post(f"{BASE}/{sid}/events", json={"event": "card_completed", "at": at}).status_code == 404

bad = {**body, "avatar": {**body["avatar"], "head": "human_round"}}
assert requests.put(f"{BASE}/{sid}", json=bad).status_code == 422  # head does not match the base

saved = requests.put(f"{BASE}/{sid}", json=body)
assert saved.status_code == 200 and saved.json()["pet"] == {"type": "plant", "stage": 1, "growth": 0}

r = requests.post(f"{BASE}/{sid}/events", json={"event": "lesson_completed", "lesson_id": str(lesson), "hints": 1, "at": at})
assert r.json()["reward_suggestion"].startswith("Finished a full lesson with one hint"), r.text
assert requests.post(f"{BASE}/{sid}/events", json={"event": "lesson_completed", "at": at}).status_code == 422

# editing the avatar keeps the pet's growth
body["avatar"]["eyes"] = "round"
again = requests.put(f"{BASE}/{sid}", json=body).json()
assert again["pet"]["growth"] == 20 and again["support_history"][0]["hints"] == 1
assert requests.get(f"{BASE}/{sid}").json() == again

svg = requests.get(f"{BASE}/{sid}/render.svg")
assert svg.headers["content-type"] == "image/svg+xml" and svg.text.startswith("<svg") and 'color="#A8C5DA"' in svg.text
assert requests.get(f"{BASE}/{uuid4()}/render.svg").status_code == 404

assert len(requests.get(f"{BASE}/questionnaire").json()) == 6
choices = {"base": "robot", "primary_color": "#A8C5DA", "head": "robot_round", "eyes": "dots", "pet_type": "plant", "stage": 3}
preview = requests.get(f"{BASE}/preview.svg", params=choices)
assert preview.status_code == 200 and preview.text.startswith("<svg")
assert requests.get(f"{BASE}/preview.svg", params={**choices, "head": "human_round"}).status_code == 422
assert requests.get(f"{BASE}/preview.svg", params={**choices, "stage": 9}).status_code == 422

print("API smoke test OK")
