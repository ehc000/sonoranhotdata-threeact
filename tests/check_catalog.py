"""Checks the avatar catalog and drawing code. Run from the project root: python -m tests.check_catalog

Draws every single choice of every base, then checks that bad choices are refused,
that drawings are deterministic, and that nothing moves (no animation in any picture).
"""
import xml.etree.ElementTree as ET
from itertools import product

from backend.avatar import catalog, renderer
from backend.avatar.models import Avatar

assert [b["id"] for b in catalog.BASES] == ["human", "animal", "robot", "creature"]

drawn = 0
for base in catalog.BASES:
    assert base["options"], f"{base['id']} has no options"
    default = renderer.render(Avatar(base=base["id"]))
    ET.fromstring(default)  # raises if the SVG is not valid XML
    for option in base["options"]:
        ids = [c["id"] for c in option["choices"]]
        assert len(ids) == len(set(ids)), f"{base['id']}.{option['id']} has repeated choice ids"
        assert option["default"] in ids, f"{base['id']}.{option['id']} default is not a choice"
        for choice in option["choices"]:
            svg = renderer.render(Avatar(base=base["id"], options={option["id"]: choice["id"]}))
            ET.fromstring(svg)
            assert "<animate" not in svg and "<set" not in svg, f"{base['id']}.{option['id']}.{choice['id']} moves"
            drawn += 1

# The same choices always give the same picture.
picked = {"hair": "long05", "skin": "8d5524", "glasses": "dark03"}
assert renderer.render(Avatar(base="human", options=picked)) == renderer.render(Avatar(base="human", options=picked))

# Different choices give different pictures (spot check on every base).
for base in catalog.BASES:
    first, second = base["options"][0], base["options"][1]
    a = renderer.render(Avatar(base=base["id"], options={first["id"]: first["choices"][0]["id"], second["id"]: second["choices"][0]["id"]}))
    b = renderer.render(Avatar(base=base["id"], options={first["id"]: first["choices"][-1]["id"], second["id"]: second["choices"][-1]["id"]}))
    assert a != b, f"{base['id']}: choices do not change the picture"

# Only listed choices are accepted.
assert catalog.problems("human", {"hair": "long05"}) == []
assert catalog.problems("dragon", {})
assert catalog.problems("human", {"hair": "not_a_hair"})
assert catalog.problems("human", {"wings": "big"})
assert catalog.problems("robot", {"hair": "long05"}), "a robot has no hair"

# The public catalog never leaks the drawing params.
public = catalog.public_catalog()
assert all("params" not in c for b in public["bases"] for o in b["options"] for c in o["choices"])

# Every combination of two options on the animal and creature sprites draws (catches a missing layer name).
for base_id in ("animal", "creature"):
    base = catalog.BY_ID[base_id]
    body, eyes, mouth = base["options"][0], base["options"][2], base["options"][3]
    for b, e, m in product(body["choices"], eyes["choices"], mouth["choices"]):
        renderer.render(Avatar(base=base_id, options={body["id"]: b["id"], eyes["id"]: e["id"], mouth["id"]: m["id"]}))

# Every head with every antenna, body and mouth on the robot draws too.
robot = {o["id"]: o for o in catalog.BY_ID["robot"]["options"]}
for h, a, t, m in product(*(robot[k]["choices"] for k in ("head", "antenna", "torso", "mouth"))):
    renderer.render(Avatar(base="robot", options={"head": h["id"], "antenna": a["id"], "torso": t["id"], "mouth": m["id"]}))

print(f"catalog checks OK ({drawn} choices drawn)")
