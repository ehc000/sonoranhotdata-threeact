"""Smoke test against a running API (start it with run_demo_api.ps1 first).
Run from the project root: python -m tests.smoke_api  (uses a fictional student id)"""
import os
from uuid import uuid4

import requests

BASE = os.environ.get("API_BASE_URL", "http://localhost:8000") + "/avatar"
sid, lesson = uuid4(), uuid4()
at = "2026-11-02T16:00:00Z"
body = {
    "avatar": {"base": "robot", "options": {"eyes": "happy", "glow": "5eead4"}, "display_name": "Bip"},
    "preferences": {"nickname": "Sam", "interests": ["cars", "space"], "read_aloud": True, "break_minutes": 2},
}

# the catalog lists the four bases and hides the drawing params
catalog = requests.get(f"{BASE}/catalog").json()
assert [b["id"] for b in catalog["bases"]] == ["human", "animal", "robot", "creature"]
assert "params" not in str(catalog)

assert requests.get(f"{BASE}/{sid}").status_code == 404
assert requests.post(f"{BASE}/{sid}/events", json={"event": "card_completed", "at": at}).status_code == 404

# only listed choices are accepted
for wrong in ({"base": "dragon", "options": {}}, {"base": "robot", "options": {"hair": "long05"}},
              {"base": "human", "options": {"hair": "not_a_hair"}}):
    assert requests.put(f"{BASE}/{sid}", json={**body, "avatar": wrong}).status_code == 422, wrong

saved = requests.put(f"{BASE}/{sid}", json=body)
# pets are on hold, but the pet data is still created so growth can come back later
assert saved.status_code == 200 and saved.json()["pet"] == {"type": "plant", "stage": 1, "growth": 0}
assert saved.json()["avatar"]["options"] == {"eyes": "happy", "glow": "5eead4"}

r = requests.post(f"{BASE}/{sid}/events", json={"event": "lesson_completed", "lesson_id": str(lesson), "hints": 1, "at": at})
assert r.json()["reward_suggestion"].startswith("Finished a full lesson with one hint"), r.text
assert requests.post(f"{BASE}/{sid}/events", json={"event": "lesson_completed", "at": at}).status_code == 422

# switching to another base keeps the growth and the support history
body["avatar"] = {"base": "animal", "options": {"body": "rabbit", "color": "8a5a3a"}, "display_name": "Bun"}
again = requests.put(f"{BASE}/{sid}", json=body).json()
assert again["avatar"]["base"] == "animal" and again["pet"]["growth"] == 20 and again["support_history"][0]["hints"] == 1
assert requests.get(f"{BASE}/{sid}").json() == again

svg = requests.get(f"{BASE}/{sid}/render.svg")
assert svg.headers["content-type"] == "image/svg+xml" and svg.text.startswith("<svg") and 'viewBox="0 0 16 16"' in svg.text
assert requests.get(f"{BASE}/{uuid4()}/render.svg").status_code == 404

assert len(requests.get(f"{BASE}/questionnaire").json()) == 6

# the live preview draws unsaved choices; the choices are plain query parameters
preview = requests.get(f"{BASE}/preview.svg", params={"base": "human", "hair": "long05", "skin": "8d5524"})
assert preview.status_code == 200 and preview.text.startswith("<svg")
other = requests.get(f"{BASE}/preview.svg", params={"base": "human", "hair": "short01", "skin": "ffdbac"})
assert other.text != preview.text
assert requests.get(f"{BASE}/preview.svg", params={"base": "human", "hair": "not_a_hair"}).status_code == 422
assert requests.get(f"{BASE}/preview.svg", params={"base": "dragon"}).status_code == 422

print("API smoke test OK")
