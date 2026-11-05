"""Plan a coherent, teacher-reviewable mission around approved questions.

Purpose: Generate a goal and ordered milestones without modifying academic questions.
Directed by: Edenna Chen
AI-assisted implementation: ChatGPT (OpenAI), GPT-6, 2026-11-05
Human review required: mission steps, accessibility settings, and academic alignment.
External sources: None.
"""

import json
from pathlib import Path
from backend import llm_query

PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "lesson_mission_planner.md"


# ------------------------------------------------------------
# AI-ASSISTED ADDITION: normalize_presentation()
# Purpose: Keep academic difficulty separate from presentation needs.
# Directed by: Edenna Chen | ChatGPT GPT-6 | 2026-11-05
# ------------------------------------------------------------
def normalize_presentation(settings=None):
    settings = settings or {}
    defaults = {
        "story_complexity": "simple",
        "instruction_chunking": "one_step",
        "predictability": "explicit",
        "visual_density": "low",
        "motion": "reduced",
        "help_mode": "optional",
    }
    choices = {
        "story_complexity": {"simple", "moderate", "rich"},
        "instruction_chunking": {"one_step", "grouped"},
        "predictability": {"explicit", "exploratory"},
        "visual_density": {"low", "medium", "rich"},
        "motion": {"reduced", "gentle"},
        "help_mode": {"optional", "prominent"},
    }
    for key, value in settings.items():
        if key in choices:
            if value not in choices[key]:
                raise ValueError(f"Invalid {key}: {value!r}")
            defaults[key] = value
    return defaults


# ------------------------------------------------------------
# AI-ASSISTED ADDITION: validate_mission()
# Purpose: Require exactly one milestone per approved question, in order.
# Directed by: Edenna Chen | ChatGPT GPT-6 | 2026-11-05
# ------------------------------------------------------------
def validate_mission(result, question_ids):
    if not isinstance(result, dict):
        raise RuntimeError("Mission planner did not return a JSON object.")
    mission = result.get("mission")
    if not isinstance(mission, dict):
        raise RuntimeError("Mission must be an object.")
    for key in ("title", "goal", "starting_state", "final_state", "roadmap_visual_prompt"):
        if not isinstance(mission.get(key), str) or not mission[key].strip():
            raise RuntimeError(f"Mission missing nonempty {key}.")
    milestones = result.get("milestones")
    if not isinstance(milestones, list) or len(milestones) != len(question_ids):
        raise RuntimeError("Mission must have one milestone per approved question.")
    if [item.get("question_id") if isinstance(item, dict) else None for item in milestones] != question_ids:
        raise RuntimeError("Mission milestones must match approved question IDs in order.")
    for index, item in enumerate(milestones):
        for key in ("id", "title", "purpose", "unlocks", "before_visual_prompt", "after_visual_prompt"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise RuntimeError(f"Milestone {index + 1} missing {key}.")
    return result


# ------------------------------------------------------------
# AI-ASSISTED ADDITION: generate_mission_plan()
# Purpose: Produce a reusable roadmap before narrative generation.
# Directed by: Edenna Chen | ChatGPT GPT-6 | 2026-11-05
# ------------------------------------------------------------
def generate_mission_plan(objective, story_concept, questions, presentation=None):
    approved = [q for q in questions if q.get("status") != "rejected"]
    if not approved:
        raise ValueError("At least one approved question is required.")
    if not isinstance(story_concept, dict) or not story_concept.get("title"):
        raise ValueError("A selected story concept is required.")
    question_ids = [str(q["id"]) for q in approved]
    if len(set(question_ids)) != len(question_ids):
        raise ValueError("Approved question IDs must be unique.")
    settings = normalize_presentation(presentation)
    payload = {
        "learning_objective": objective,
        "story_concept": story_concept,
        "presentation": settings,
        "approved_questions": [
            {"id": str(q["id"]), "competency": q.get("competency"),
             "text": q.get("text") or q.get("original")}
            for q in approved
        ],
    }
    # A deterministic offline preview; it does NOT establish academic alignment.
    mock_reply = {
        "mission": {
            "title": story_concept["title"],
            "goal": story_concept.get("story_goal") or "Complete the mission",
            "starting_state": "The mission has not begun.",
            "final_state": "All mission tasks are complete.",
            "roadmap_visual_prompt": "Simple, uncluttered pixel-art roadmap with numbered empty milestones; no text.",
        },
        "milestones": [
            {
                "id": f"task_{i + 1}", "question_id": qid,
                "title": f"Mission task {i + 1}",
                "purpose": "MOCK: Teacher must specify how this task advances the goal.",
                "unlocks": f"Next task {i + 2}" if i + 1 < len(question_ids) else "Mission finale",
                "before_visual_prompt": "Unfinished mission scene, simple pixel art, no text.",
                "after_visual_prompt": "Same scene with one visible task completed, simple pixel art, no text.",
            }
            for i, qid in enumerate(question_ids)
        ],
        "alignment_warning": "MOCK MODE: Mission coherence and academic alignment have not been checked.",
    }
    if not PROMPT_PATH.is_file():
        raise FileNotFoundError(f"Mission prompt missing: {PROMPT_PATH}")
    result = llm_query.chat_json(
        [
            {"role": "system", "content": PROMPT_PATH.read_text(encoding="utf-8")},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        mock_reply=mock_reply,
        prompt_id="lesson_mission_planner",
    )
    result = validate_mission(result, question_ids)
    result["presentation"] = settings
    result["llm_mode"] = llm_query.mode()
    return result
