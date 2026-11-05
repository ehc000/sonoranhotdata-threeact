"""Checks that every catalog option has a valid SVG file and that every combination renders.
Run from the project root: python -m tests.check_assets"""
import xml.etree.ElementTree as ET
from itertools import product

from backend.avatar.models import Avatar, Pet
from backend.avatar.renderer import ASSETS, render
from backend.avatar.router import CATALOG

heads = [(base, head) for base, options in CATALOG["heads"].items() for head in options]
expected = (
    [f"heads/{head}.svg" for _, head in heads]
    + [f"eyes/{eyes}.svg" for eyes in CATALOG["eyes"]]
    + [f"pets/{pet}_{stage}.svg" for pet in CATALOG["pets"] for stage in range(1, CATALOG["pet_stages"] + 1)]
)
for rel in expected:
    assert (ASSETS / rel).is_file(), f"missing asset: {rel}"
    ET.parse(ASSETS / rel)  # raises if the SVG is not valid XML
assert len(list(ASSETS.rglob("*.svg"))) == len(expected), "asset files not listed in the catalog"

assert len(CATALOG["color_names"]) == len(CATALOG["colors"]), "every color needs a name"

count = 0
for (base, head), eyes, color, pet, stage in product(heads, CATALOG["eyes"], CATALOG["colors"][:2], CATALOG["pets"], range(1, 6)):
    avatar = Avatar(base=base, primary_color=color, head=head, eyes=eyes)
    out = render(avatar, Pet(type=pet, stage=stage))
    ET.fromstring(out)
    assert f'color="{color}"' in out
    count += 1

print(f"asset checks OK ({len(expected)} files, {count} renders)")
