"""Onboarding questionnaire definition: eight short questions about the student's preferences.

A question has a type:
  "text"   - a short typed answer (only the nickname)
  "choice" - the student taps one or more options

Each option has an id (what the screen remembers), a label (what the student sees) and
a value (what gets saved in Preferences). "Not sure" is always allowed: on single-choice
questions it saves the gentle default, on multi-choice questions the student just skips.

Break length is not asked: the teacher sets it (2 or 5 minutes).
Session length is not asked either: the school sets it.
"""


def _opts(*items: tuple) -> list[dict]:
    """Build options from (id, label) or (id, label, value) tuples; value defaults to the id."""
    return [{"id": i[0], "label": i[1], "value": i[2] if len(i) > 2 else i[0]} for i in items]


QUESTIONS = [
    {
        "id": "nickname", "field": "nickname", "type": "text", "max_length": 20,
        "title": "What should your buddy call you?",
        "hint": "A nickname is fine. Please do not use your full name.",
    },
    {
        "id": "interests", "field": "interests", "type": "choice", "multi": True, "max_choices": 3,
        "title": "What do you love? Pick up to 3.",
        "options": _opts(
            ("cars", "🚗 Cars"), ("space", "🚀 Space"), ("animals", "🐶 Animals"), ("music", "🎵 Music"),
            ("drawing", "🎨 Drawing"), ("games", "🎮 Video games"), ("sports", "⚽ Sports"), ("cooking", "🍳 Cooking"),
            ("nature", "🌳 Nature"), ("building", "🧱 Building"), ("robots", "🤖 Robots"), ("reading", "📚 Reading"),
            ("other", "✨ Something else"),
        ),
    },
    {
        "id": "work_style", "field": "work_style", "type": "choice", "multi": True,
        "title": "How do you like to work?",
        "options": _opts(
            ("hands_on", "🛠️ Building with my hands"), ("design", "✏️ Drawing or designing"),
            ("computer", "💻 Using the computer"), ("writing", "📝 Writing"),
        ),
    },
    {
        "id": "content_format", "field": "content_format", "type": "choice", "multi": False,
        "title": "How do you like your steps?",
        "options": _opts(
            ("images", "🖼️ Show me pictures"), ("audio", "🔊 Read them to me"),
            ("text", "📄 Let me read them"), ("mixed", "🔀 A mix"),
        ),
    },
    {
        "id": "sounds_bother", "field": "sounds_bother", "type": "choice", "multi": False,
        "title": "Do sounds bother you?",
        "options": _opts(("yes", "Yes"), ("no", "No"), ("sometimes", "Sometimes"), ("not_sure", "Not sure", "sometimes")),
    },
    {
        "id": "motion_bother", "field": "motion_bother", "type": "choice", "multi": False,
        "title": "Do moving pictures bother you?",
        "options": _opts(("yes", "Yes"), ("no", "No"), ("sometimes", "Sometimes"), ("not_sure", "Not sure", "sometimes")),
    },
    {
        "id": "help_mode", "field": "help_mode", "type": "choice", "multi": False,
        "title": "When you get stuck, what do you want?",
        "options": _opts(
            ("ask", "✋ I'll ask when I need help"), ("check_in", "👋 Check on me if I'm stuck"),
            ("not_sure", "Not sure", "check_in"),
        ),
    },
    {
        "id": "goal", "field": "goal", "type": "choice", "multi": False,
        "title": "One thing I want to get better at",
        "options": _opts(
            ("finishing_projects", "🏁 Finishing projects"), ("asking_for_help", "🙋 Asking for help"),
            ("staying_organized", "🗂️ Staying organized"), ("working_alone", "🧍 Working on my own"),
            ("not_sure", "Not sure", None),
        ),
    },
]
