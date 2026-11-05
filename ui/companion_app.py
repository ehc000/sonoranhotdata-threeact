"""Streamlit prototype: onboarding screens and the "My companion" screen.

Streamlit re-runs this whole file every time the student clicks something, so everything
that must be remembered (current step, choices) lives in st.session_state.
This file only talks to the API over HTTP; it never touches the database.
"""
import base64
import html
import os
from datetime import datetime, timezone
from uuid import uuid4

import requests
import streamlit as st

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")
API = f"{API_BASE_URL}/avatar"
AVATAR_STEPS = ["base", "color", "head", "eyes", "pet", "name"]
# Demo only: in the real app the teacher enters these when creating the student profile.
TEACHER_INTERESTS = ["cars", "space"]

st.set_page_config(page_title="My companion", layout="centered")
ss = st.session_state

# Calm look: bigger text and tap targets, no animations, no toolbar or spinner to distract.
# Cards get a key starting with "card-" (or "sel-" when chosen) so the CSS can outline the chosen one.
st.markdown("""
<style>
html { font-size: 18px; }
[data-testid="stToolbar"], [data-testid="stStatusWidget"], footer { display: none; }
* { transition: none !important; animation: none !important; }
.stButton { width: 100%; }
.stButton > button { min-height: 3rem; border-radius: 14px; width: 100%; }
.stButton > button[kind="secondary"] { border: 2px solid #6F8396; }
[data-testid="stCaptionContainer"] { color: #4A5866; }
img { margin-bottom: 0.75rem; }
[class*="st-key-card-"], [class*="st-key-sel-"] { border-radius: 18px; }
[class*="st-key-sel-"] { background: #E3ECF3; border: 3px solid #3F6A8C !important; }
[class*="st-key-card-"] .stButton, [class*="st-key-sel-"] .stButton { display: flex; justify-content: center; }
</style>
""", unsafe_allow_html=True)


# ---------- talking to the API ----------

def problem(detail: str) -> None:
    """Kind message for the student, technical detail in small print for the adults; then stop."""
    st.error("Something went wrong and your companion can't load right now. Please ask your teacher for help.")
    st.caption(detail)
    st.stop()


def call(method: str, path: str, **kwargs) -> requests.Response:
    try:
        return requests.request(method, f"{API}{path}", timeout=10, **kwargs)
    except requests.RequestException as exc:
        problem(f"Cannot reach the API at {API_BASE_URL}. Is it running? ({exc})")


@st.cache_data(show_spinner=False)
def catalog() -> dict:
    return call("GET", "/catalog").json()


@st.cache_data(show_spinner=False)
def questions() -> list:
    return call("GET", "/questionnaire").json()


@st.cache_data(show_spinner=False)
def preview(base: str, color: str, head: str, eyes: str, pet: str, stage: int = 1) -> str:
    params = {"base": base, "primary_color": color, "head": head, "eyes": eyes, "pet_type": pet, "stage": stage}
    return call("GET", "/preview.svg", params=params).text


AVATAR_ONLY, PET_ONLY = "0 0 100 100", "100 0 100 100"  # the picture is 200 wide: avatar on the left, pet on the right


def show_svg(svg: str, width: str = "100%", view: str | None = None, alt: str = "") -> None:
    """Show an SVG string; `view` crops it to one half (avatar or pet)."""
    if view:
        svg = svg.replace('viewBox="0 0 200 100"', f'viewBox="{view}"', 1)
    data = base64.b64encode(svg.encode()).decode()
    st.markdown(f'<img src="data:image/svg+xml;base64,{data}" style="width:{width}" alt="{html.escape(alt)}">', unsafe_allow_html=True)


def pretty(option_id: str) -> str:
    return option_id.replace("_", " ").title()


# ---------- which student is this ----------

if "student" not in st.query_params:  # keeps the same fictional student when the page reloads
    st.query_params["student"] = str(uuid4())
student_id = st.query_params["student"]


def go_onboarding(mode: str) -> None:
    """mode 'new' = all steps; 'edit' = avatar steps only, keeping saved answers."""
    cat = catalog()
    if mode == "edit":
        saved = call("GET", f"/{student_id}").json()
        a = saved["avatar"]
        ss.draft = {"base": a["base"], "color": a["primary_color"], "head": a["head"], "eyes": a["eyes"],
                    "pet": saved["pet"]["type"], "name": a["display_name"]}
    else:
        ss.draft = {"base": cat["bases"][0], "color": cat["colors"][0], "head": cat["heads"][cat["bases"][0]][0],
                    "eyes": cat["eyes"][0], "pet": cat["pets"][0], "name": ""}
    ss.answers = {"interests": list(TEACHER_INTERESTS)}
    ss.mode, ss.step, ss.screen = mode, 1 if mode == "edit" else 0, "onboarding"


def save(skip: bool = False) -> None:
    """Send the choices to the API; skipping saves the default companion."""
    d, saved = ss.draft, None
    if ss.mode == "edit":
        saved = call("GET", f"/{student_id}").json()
        prefs, static = saved["preferences"], saved["avatar"]["static_mode"]
    else:
        prefs, static = {}, False  # calm by default: no sounds or animations unless a settings switch turns them on
        for q in questions():
            chosen = ss.answers.get(q["id"])
            if q["type"] == "text":
                prefs[q["field"]] = (chosen or "").strip()
            elif q["multi"]:
                prefs[q["field"]] = chosen or []
            elif chosen and not skip:
                prefs[q["field"]] = next(o["value"] for o in q["options"] if o["id"] == chosen)
    body = {"avatar": {"base": d["base"], "primary_color": d["color"], "head": d["head"], "eyes": d["eyes"],
                       "display_name": d["name"], "static_mode": static},
            "pet_type": d["pet"], "preferences": prefs}
    r = call("PUT", f"/{student_id}", json=body)
    if r.status_code != 200:
        problem(f"Could not save (HTTP {r.status_code}): {r.text}")
    ss.screen = "companion"
    st.rerun()


if "screen" not in ss:
    if call("GET", f"/{student_id}").status_code == 404:
        go_onboarding("new")
    else:
        ss.screen = "companion"


# ---------- onboarding ----------

def choice_buttons(options: list, selected: list, multi: bool, key: str, per_row: int = 4, max_choices: int | None = None):
    """Big buttons; returns the new selection when one was clicked, else None."""
    for start in range(0, len(options), per_row):
        cols = st.columns(per_row)
        for col, o in zip(cols, options[start:start + per_row]):
            on = o["id"] in selected
            # The check mark means "chosen" even without seeing the color.
            if col.button(("✓ " if on else "") + o["label"], key=f"{key}-{o['id']}", type="primary" if on else "secondary"):
                if not multi:
                    return [o["id"]]
                if on:
                    return [i for i in selected if i != o["id"]]
                if max_choices and len(selected) >= max_choices:
                    return None  # already at the limit: tap one to remove it first
                return selected + [o["id"]]
    return None


def option_cards(options: list, current: str, key: str, image) -> str | None:
    """A picture card per option (image(option) returns the picture); returns the clicked option."""
    cols = st.columns(len(options))
    for col, opt in zip(cols, options):
        on = opt == current
        with col, st.container(key=f"{'sel' if on else 'card'}-{key}-{opt}", border=True):
            image(opt)
            if st.button(("✓ " if on else "") + pretty(opt.split("_", 1)[-1] if key == "head" else opt),
                         key=f"{key}-{opt}", type="primary" if on else "secondary"):
                return opt
    return None


def onboarding() -> None:
    cat, d, qs = catalog(), ss.draft, questions()
    steps = ["welcome"] + AVATAR_STEPS + ([q["id"] for q in qs] if ss.mode == "new" else [])
    step = steps[ss.step]
    last = ss.step == len(steps) - 1

    # The page title is the question for this step, so each screen says what to do in one line.
    titles = {"welcome": "Let's create your companion", "base": "Pick a type", "color": "Pick a color", "head": "Pick a head",
              "eyes": "Pick the eyes", "pet": "Pick a pet", "name": "Give it a name (optional)", **{q["id"]: q["title"] for q in qs}}
    st.title(titles[step])
    if step != "welcome":
        n_avatar = len(AVATAR_STEPS)
        st.caption(f"Step {ss.step} of {n_avatar}" if ss.step <= n_avatar else f"Question {ss.step - n_avatar} of {len(qs)}")
        st.progress(ss.step / (len(steps) - 1))

    # Back / Next always sit in the same place, right under the title.
    back_col, next_col, _ = st.columns([1, 1, 2])
    if step != "welcome" and back_col.button("← Back"):
        if ss.step == 1 and ss.mode == "edit":  # editing skips the welcome screen
            ss.screen = "companion"
        else:
            ss.step -= 1
        st.rerun()
    # Avatar steps always have a default; a single-choice question needs an answer first.
    # The nickname and the multi-choice questions can be skipped.
    answered = step == "welcome" or step in d or step in ss.answers or any(q["type"] == "text" or q["multi"] for q in qs if q["id"] == step)
    if step == "welcome":
        if next_col.button("Start", type="primary"):
            ss.step = 1
            st.rerun()
    elif next_col.button("Done ✓" if last else "Next →", type="primary", disabled=not answered):
        if last:
            save()
        else:
            ss.step += 1
            st.rerun()
    st.divider()

    def pick(key: str, value) -> None:
        d[key] = value
        if key == "base":  # a head from another base would not fit, so start with the first one
            d["head"] = cat["heads"][value][0]
        st.rerun()

    def draw(**over) -> str:
        v = {"base": d["base"], "color": d["color"], "head": d["head"], "eyes": d["eyes"], "pet": d["pet"], **over}
        return preview(v["base"], v["color"], v["head"], v["eyes"], v["pet"], v.get("stage", 1))

    if step == "welcome":
        _, middle, _ = st.columns([1, 2, 1])
        with middle:
            show_svg(draw(), alt="A preview of a companion")
        st.write(f"We will make your companion in {len(AVATAR_STEPS)} steps, then ask {len(qs)} quick questions. You can change it later.")
        if st.button("Skip for now"):
            save(skip=True)
    elif step == "base":
        c =option_cards(cat["bases"], d["base"], "base", lambda o: show_svg(draw(base=o, head=cat["heads"][o][0]), view=AVATAR_ONLY))
        if c:
            pick("base", c)
    elif step == "color":
        cols = st.columns(len(cat["colors"]))
        for col, color, color_name in zip(cols, cat["colors"], cat["color_names"]):
            with col:
                st.markdown(f'<div style="height:48px;border-radius:12px;background:{color};border:2px solid #5F7080" role="img" aria-label="{color_name}"></div>', unsafe_allow_html=True)
                on = color == d["color"]
                if st.button(("✓ " if on else "") + color_name, key=f"color-{color}", type="primary" if on else "secondary"):
                    pick("color", color)
        show_svg(draw(), "50%")
    elif step == "head":
        c =option_cards(cat["heads"][d["base"]], d["head"], "head", lambda o: show_svg(draw(head=o), view=AVATAR_ONLY))
        if c:
            pick("head", c)
    elif step == "eyes":
        c =option_cards(cat["eyes"], d["eyes"], "eyes", lambda o: show_svg(draw(eyes=o), view=AVATAR_ONLY))
        if c:
            pick("eyes", c)
    elif step == "pet":
        c =option_cards(cat["pets"], d["pet"], "pet", lambda o: show_svg(draw(pet=o, stage=3), view=PET_ONLY))  # stage 3 so the pets are easy to tell apart
        if c:
            pick("pet", c)
    elif step == "name":
        d["name"] = st.text_input("Your companion's name", value=d["name"], max_chars=20)
        show_svg(draw(), "60%")
    else:  # a questionnaire question
        q = next(q for q in qs if q["id"] == step)
        if q["type"] == "text":  # the nickname: a short typed answer, never the full name
            st.caption(q["hint"])
            ss.answers[step] = st.text_input("Nickname", value=ss.answers.get(step, ""), max_chars=q["max_length"])
            return
        if step == "interests":
            st.caption("Your teacher added some of these. Tap to add or remove.")
        now = ss.answers.get(step, [] if q["multi"] else None)
        new = choice_buttons(q["options"], now if q["multi"] else [now], q["multi"], step, 3, q.get("max_choices"))
        if new is not None:
            ss.answers[step] = new if q["multi"] else new[0]
            st.rerun()


# ---------- My companion ----------

def companion() -> None:
    saved = call("GET", f"/{student_id}").json()
    name = saved["avatar"]["display_name"]
    st.title(name or "My companion")
    _, middle, _ = st.columns([1, 4, 1])  # centered, always in the same place
    with middle:
        show_svg(call("GET", f"/{student_id}/render.svg").text, alt=f"{name or 'Your'} companion and pet")
    if st.button("Change my companion"):
        go_onboarding("edit")
        st.rerun()

    # The student's screen stays calm; the demo tools live in a closed panel until they are needed.
    if "lesson_id" not in ss:
        ss.lesson_id = str(uuid4())
    st.divider()
    with st.expander("Demo controls (not part of the student view)", expanded="result" in ss):
        st.caption("These stand in for the other modules, which send these events.")
        hints = st.number_input("Hints used in this lesson", min_value=0, max_value=5, value=0)
        events = [("Card done", "card_completed"), ("Lesson done", "lesson_completed"), ("Check-in done", "checkin_done"),
                  ("Took a break", "break_taken"), ("I need help", "help_requested")]
        for i, (label, event) in enumerate(events):
            if i % 3 == 0:  # three buttons per row so the labels fit
                cols = st.columns(3)
            if cols[i % 3].button(label, key=event):
                body = {"event": event, "lesson_id": ss.lesson_id, "hints": hints, "at": datetime.now(timezone.utc).isoformat()}
                ss.result = call("POST", f"/{student_id}/events", json=body).json()
                if event == "lesson_completed":
                    ss.lesson_id = str(uuid4())  # the next lesson is a new one
                st.rerun()
        if "result" in ss:
            r = ss.result
            with st.container(border=True):
                st.markdown("**Teacher view**")
                st.write(f"Pet stage: {r['stage']} of 5")
                st.write(f"Reward suggestion: {r['reward_suggestion'] or 'none for this event'}")
                st.write(f"Support trend: {r['fading_trend'].replace('_', ' ')}")
        if st.button("Start over with a new demo student"):
            for key in list(ss.keys()):
                del ss[key]
            st.query_params["student"] = str(uuid4())
            st.rerun()


if ss.screen == "onboarding":
    onboarding()
else:
    companion()
