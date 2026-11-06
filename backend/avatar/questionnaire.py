"""Onboarding questionnaire definition: six short questions about the student's preferences.

A question has a type:
  "text"   - a short typed answer (only the nickname)
  "choice" - the student taps one or more options

Each option has an id (what the screen remembers), a label (what the student sees) and
a value (what gets saved in Preferences). On the help question, "Not sure" saves the
gentle default; on the goal question it saves nothing. On the multi-choice questions the student can skip, which also means "not sure".

Not asked here, on purpose:
  - Break length: the teacher sets it (2 or 5 minutes).
  - Session length: the school sets it.
  - Sounds and animations: calm by default, with one on/off switch in settings.
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
        "title": "What kind of projects do you enjoy?",
        "options": _opts(
            ("hands_on", "🛠️ Building"), ("design", "✏️ Drawing or designing"),
            ("computer", "💻 Using the computer"), ("writing", "📝 Writing"),
        ),
    },
    {
        "id": "read_aloud", "field": "read_aloud", "type": "choice", "multi": False,
        "title": "Do you want your steps read out loud?",
        "options": _opts(("yes", "🔊 Yes", True), ("no", "No", False)),
    },
    {
        "id": "help_mode", "field": "help_mode", "type": "choice", "multi": False,
        "title": "When you get stuck, what do you want?",
        "options": _opts(
            ("ask", "✋ I'll ask"), ("check_in", "👋 Check on me if I'm stuck"),
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
