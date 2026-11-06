"""Draws an avatar as one SVG string (16 x 16 pixels, scales to any size).

The avatar has no mood and no animation, so static_mode needs no extra work here.
- human: DiceBear draws it, from the style files shipped in the dicebear-styles package.
- animal, creature and robot: sprites.py draws them.
"""
import json
from functools import lru_cache
from importlib.resources import files

from dicebear import Avatar as DiceBearAvatar, Style

from backend.avatar import catalog, sprites
from backend.avatar.models import Avatar


@lru_cache(maxsize=None)
def _style(name: str) -> Style:
    """Load a DiceBear style once; reading the JSON file again for every picture would be slow."""
    return Style(json.loads(files("dicebear_styles").joinpath(f"{name}.json").read_text("utf-8")))


def render(a: Avatar) -> str:
    """Names were checked against the catalog when saved; resolve() fails loudly if they were not."""
    params = catalog.resolve(a.base, a.options)
    base = catalog.BY_ID[a.base]
    if base["engine"] == "dicebear":
        return DiceBearAvatar(_style(base["style"]), params).to_string()
    return sprites.render(base["group"], params)
