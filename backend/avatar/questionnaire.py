"""Onboarding questionnaire definition: five multiple-choice questions with icons.

Each option has an id (what the screen remembers), a label (what the student sees) and
a value (what gets saved in Preferences). Session length is not asked: the school sets it.
"""


def _opts(*items: tuple) -> list[dict]:
    """Build options from (id, label) or (id, label, value) tuples; value defaults to the id."""
    return [{"id": i[0], "label": i[1], "value": i[2] if len(i) > 2 else i[0]} for i in items]


QUESTIONS = [
    {
        "id": "interests", "field": "interests", "multi": True,
        "title": "What do you like?",
        "options": _opts(
            ("cars", "🚗 Cars"), ("space", "🚀 Space"), ("animals", "🐶 Animals"), ("music", "🎵 Music"),
            ("drawing", "🎨 Drawing"), ("games", "🎮 Video games"), ("sports", "⚽ Sports"), ("cooking", "🍳 Cooking"),
            ("nature", "🌳 Nature"), ("building", "🧱 Building"), ("robots", "🤖 Robots"), ("reading", "📚 Reading"),
        ),
    },
    {
        "id": "content_format", "field": "content_format", "multi": False,
        "title": "How do you like to see things?",
        "options": _opts(("text", "📝 Short text"), ("images", "🖼️ Images"), ("audio", "🔊 Audio"), ("mixed", "🔀 A mix")),
    },
    {
        "id": "sensory", "field": "sensory_sensitive", "multi": False,
        "title": "Do sounds or animations bother you?",
        "options": _opts(("yes", "Yes", True), ("sometimes", "Sometimes", True), ("no", "No", False)),
    },
    {
        "id": "help_mode", "field": "help_mode", "multi": False,
        "title": "When you get stuck, what do you want?",
        "options": _opts(("offer", "🙋 Offer me help"), ("ask", "✋ I will ask")),
    },
    {
        "id": "break_minutes", "field": "break_minutes", "multi": False,
        "title": "How long should a break be?",
        "options": _opts(("2", "⏱️ 2 minutes", 2), ("5", "⏱️ 5 minutes", 5)),
    },
]
