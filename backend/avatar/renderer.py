"""Renders the avatar and pet as one SVG string.

Each part is a small SVG file in avatar/assets/ (heads/, eyes/, pets/). The renderer
reads the parts the student chose and stacks them: head, then eyes, then the pet beside them.
The avatar has no mood and no animation, so static_mode needs no extra work here.
"""
import re
from pathlib import Path

from backend.avatar.models import Avatar, Pet

ASSETS = Path(__file__).parent / "assets"


def _inner(relative_path: str) -> str:
    """Return what is inside the <svg> tag of one asset file."""
    text = (ASSETS / relative_path).read_text(encoding="utf-8")
    return re.search(r"<svg[^>]*>(.*)</svg>", text, re.DOTALL).group(1)


def render(a: Avatar, pet: Pet) -> str:
    # Names were checked against the catalog when saved; this keeps the file lookup safe anyway.
    for name in (a.head, a.eyes, pet.type):
        if not re.fullmatch(r"[a-z_]+", name):
            raise ValueError(f"invalid asset name: {name}")
    # The head uses currentColor, so setting `color` on the group paints it with the primary color.
    avatar = f'<g color="{a.primary_color}">{_inner(f"heads/{a.head}.svg")}{_inner(f"eyes/{a.eyes}.svg")}</g>'
    pet_svg = f'<g transform="translate(100 0)">{_inner(f"pets/{pet.type}_{pet.stage}.svg")}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" role="img" '
            f'aria-label="Avatar and pet">{avatar}{pet_svg}</svg>')
