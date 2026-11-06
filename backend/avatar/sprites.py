"""Our own pixel sprites for the animal, creature and robot avatars (16 x 16 pixels, flat colors, no outline).

DiceBear has no pixel art animals or creatures, and its robot is only a glowing face, so these are drawn here
in the same size and look as its "pixel-art" human, and they can be customized the same way.

How a sprite is stored:
- A layer is 16 rows of 8 characters. Only the LEFT half is written; the right half is the mirror image.
- Every character is one pixel and means a color role:
    .  nothing            f  main color (fur or skin)   g  shade of the main color   h  light version of the main color
    p  pink (inner ear)   k  dark (eyes, nose, mouth)   w  white                     x  horn / antenna color
    c  clothing color     d  shade of the clothing      a  accessory color
    s  robot screen color l  robot light color (eyes, mouth, antenna tip)
- A picture is made by stacking layers. Animal and creature: body, clothes, mouth, eyes, accessory.
  Robot: antenna, head, torso, mouth, eyes.
"""

SIZE = 16


def _rows(rows: dict) -> list[str]:
    """Build a layer from only the rows that have pixels: {row number: 8 characters}."""
    return [rows.get(y, "........") for y in range(SIZE)]


# ---------- layers (left half only) ----------

BODIES = {
    "animal": {
        "cat": [
            "........", "..f.....", "..ffg...", "..fpff..", "..ffffff", "..ffffff", "..gfffff", "..gfffff",
            "..gfffhh", "..gffhhh", "...ffhhh", "....ffff", "......gf", "......gf", "........", "........"],
        "dog": [
            "........", "........", "...fffff", ".ggfffff", ".ggfffff", ".ggfffff", ".ggfffff", ".ggfffff",
            ".ggfffhh", "..gffhhh", "...ffhhh", "....ffff", "......gf", "......gf", "........", "........"],
        "rabbit": [
            "...ff...", "..fpf...", "..fpf...", "..fpf...", "...fffff", "..ffffff", "..gfffff", "..gfffff",
            "..gfffhh", "..gffhhh", "...ffhhh", "....ffff", "......gf", "......gf", "........", "........"],
        "bear": [
            "........", "........", "..fff...", "..fpf...", "..ffffff", "..ffffff", "..gfffff", "..gfffff",
            "..gfffhh", "..gffhhh", "...ffhhh", "....ffff", "......gf", "......gf", "........", "........"],
    },
    "creature": {
        "blob": [
            "........", "........", "....ffff", "..ffffff", ".fffffff", ".fffffff", ".gffffff", ".gffffff",
            ".gffffff", ".gffffff", "..gfffff", "...fffff", "......gf", "......gf", "........", "........"],
        "alien": [
            "...xx...", "....g...", "...fffff", "..ffffff", "..ffffff", "..ffffff", "..gfffff", "..gfffff",
            "..gfffff", "...fffff", "....ffff", ".....fff", "......gf", "......gf", "........", "........"],
        "dragon": [
            "..x.....", "..xx....", "..ffffff", "..ffffff", "..ffffff", "..ffffff", "..gfffff", "..gfffff",
            "..gfhhhh", "..gfhhhh", "...fhhhh", "....ffff", "......gf", "......gf", "........", "........"],
        "monster": [
            "........", "........", "..f.f.f.", ".fffffff", ".fffffff", "gfffffff", ".fffffff", "gfffffff",
            ".fffffff", "gfffffff", "..ffffff", "...fffff", "......gf", "......gf", "........", "........"],
    },
}

EYES = {
    "animal": {
        "dots": ["........"] * 6 + ["....k...", "........"] + ["........"] * 8,
        "tall": ["........"] * 6 + ["....k...", "....k..."] + ["........"] * 8,
        "big": ["........"] * 6 + ["....wk..", "....kk.."] + ["........"] * 8,
        "happy": ["........"] * 6 + ["....kk..", "...k..k."] + ["........"] * 8,
        "sleepy": ["........"] * 7 + ["....kk.."] + ["........"] * 8,
    },
    "creature": {
        "dots": ["........"] * 6 + ["....k...", "........"] + ["........"] * 8,
        "big": ["........"] * 6 + ["....wk..", "....kk.."] + ["........"] * 8,
        "cyclops": ["........"] * 5 + ["......ww", "......wk", "......ww"] + ["........"] * 8,
        "three": ["........"] * 5 + [".......k", "...k...k"] + ["........"] * 9,
        "sleepy": ["........"] * 7 + ["....kk.."] + ["........"] * 8,
    },
}

MOUTHS = {
    "animal": {
        "smile": ["........"] * 8 + ["......kk", "......k.", ".......k"] + ["........"] * 5,
        "open": ["........"] * 8 + ["......kk", "......kk", "......pp"] + ["........"] * 5,
        "flat": ["........"] * 8 + ["......kk", "......kk"] + ["........"] * 6,
        "nose": ["........"] * 8 + ["......kk"] + ["........"] * 7,
    },
    "creature": {
        "smile": ["........"] * 9 + ["....k...", ".....kkk"] + ["........"] * 5,
        "open": ["........"] * 9 + ["....kkkk", ".....kkk"] + ["........"] * 5,
        "fangs": ["........"] * 9 + ["....kkkk", "....w..."] + ["........"] * 5,
        "flat": ["........"] * 9 + ["....kkkk"] + ["........"] * 6,
    },
}

ACCESSORIES = {
    "none": ["........"] * 16,
    "glasses": ["........"] * 5 + ["..kkkk..", "..k..kkk", "..k..k..", "..kkkk.."] + ["........"] * 7,
    "sunglasses": ["........"] * 6 + ["..kkkkkk", "..kkkk.."] + ["........"] * 8,
    "headband": ["........"] * 4 + ["..aaaaaa"] + ["........"] * 11,
}

CLOTHES = {
    "tee": ["........"] * 13 + ["..cccc..", ".cccccdd", "cccccccc"],
    "collar": ["........"] * 13 + ["..cccc..", ".ccccwww", "cccccccc"],
    "stripes": ["........"] * 13 + ["..cccc..", ".dddddd.", "cccccccc"],
}

# ---------- robot layers (left half only) ----------
# Heads run from row 2 or 3 to row 11. The dark "s" area is the screen where the eyes and mouth light up.

_SCREEN_ROWS = {6: "ggfsssss", 7: "ggfsssss", 8: "ggfsssss"}  # the side bolts are the "g" pixels

ROBOT_HEADS = {
    "dome": _rows({2: "....hhhh", 3: "..hhhhhh", 4: "..ffffff", 5: "..fsssss", **_SCREEN_ROWS,
                   9: "..fsssss", 10: "..ffffff", 11: "..gggggg"}),
    "oval": _rows({3: "...hhhhh", 4: "..ffffff", 5: "..fsssss", **_SCREEN_ROWS,
                   9: "..fsssss", 10: "...fffff", 11: "....gggg"}),
    "round": _rows({3: "...hhhhh", 4: "..hfffff", 5: ".hfsssss", **_SCREEN_ROWS,
                    9: ".gfsssss", 10: "..gfffff", 11: "...ggggg"}),
    "square": _rows({3: "..hhhhhh", 4: "..ffffff", 5: "..fsssss", **_SCREEN_ROWS,
                     9: "..fsssss", 10: "..ffffff", 11: "..gggggg"}),
}

ROBOT_ANTENNAS = {
    "ball": _rows({0: "......ll", 1: "......ll", 2: ".......g"}),
    "double": _rows({0: "...l....", 1: "...g....", 2: "...g...."}),
    "stick": _rows({0: ".......l", 1: ".......g", 2: ".......g"}),
    "none": _rows({}),
}

# The torso starts with a short neck (row 12) and ends at the bottom of the picture.
ROBOT_TORSOS = {
    "plain": _rows({12: "......gg", 13: "..ffffff", 14: ".fffffff", 15: ".fffffff"}),
    "panel": _rows({12: "......gg", 13: "..ffffff", 14: ".ffffccc", 15: ".ffffccc"}),
    "stripe": _rows({12: "......gg", 13: "..ffffff", 14: ".ccccccc", 15: ".fffffff"}),
    "lights": _rows({12: "......gg", 13: "..ffffff", 14: ".fffffll", 15: ".fffffff"}),
}

ROBOT_EYES = {
    "round": _rows({6: "....ll..", 7: "....ll.."}),
    "happy": _rows({6: "....ll..", 7: "...l..l."}),
    "blocks": _rows({6: "...lll..", 7: "...lll.."}),
    "soft": _rows({7: "....ll.."}),
    "tall": _rows({5: "....l...", 6: "....l...", 7: "....l..."}),
    "slim": _rows({6: "...lll.."}),
    "wide": _rows({6: "...llll.", 7: "...llll."}),
}

ROBOT_MOUTHS = {
    "smile": _rows({8: "...l....", 9: "....llll"}),
    "big": _rows({8: "...lllll", 9: "....llll"}),
    "flat": _rows({9: "....llll"}),
    "tiny": _rows({9: "......ll"}),
    "open": _rows({8: "......ll", 9: "......ll"}),
}


# ---------- drawing ----------

def _mix(hex_color: str, other: str, amount: float) -> str:
    """Blend a color toward another one (amount 0 = unchanged, 1 = the other color)."""
    a = [int(hex_color[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(other[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * amount):02x}" for x, y in zip(a, b))


def _palette(choices: dict) -> dict:
    fur, clothing = choices["fur"], choices["clothing"]
    return {
        "f": fur, "g": _mix(fur, "#000000", 0.2), "h": _mix(fur, "#ffffff", 0.45), "p": "#e9a3ad",
        "k": "#2b2d3a", "w": "#ffffff", "x": "#f3e8c6",
        "c": clothing, "d": _mix(clothing, "#000000", 0.2), "a": choices.get("accessory_color", "#ffffff"),
        "s": choices.get("screen", "#0f172a"), "l": choices.get("glow", "#7dd3fc"),
    }


def _layers(group: str, choices: dict) -> list[list[str]]:
    """The layers of one avatar, from back to front."""
    if group == "robot":
        return [ROBOT_ANTENNAS[choices["antenna"]], ROBOT_HEADS[choices["head"]], ROBOT_TORSOS[choices["torso"]],
                ROBOT_MOUTHS[choices["mouth"]], ROBOT_EYES[choices["eyes"]]]
    return [BODIES[group][choices["body"]], CLOTHES[choices["clothes"]], MOUTHS[group][choices["mouth"]],
            EYES[group][choices["eyes"]], ACCESSORIES[choices["accessory"]]]


def _mirror(half: list[str]) -> list[str]:
    return [row + row[::-1] for row in half]


def render(group: str, choices: dict) -> str:
    """Draw one sprite avatar as an SVG string. `group` is "animal", "creature" or "robot"."""
    colors = _palette(choices)
    pixels = {}
    for layer in _layers(group, choices):  # later layers are drawn over earlier ones
        for y, row in enumerate(_mirror(layer)):
            for x, ch in enumerate(row):
                if ch != ".":
                    pixels[(x, y)] = colors[ch]
    rects = []
    for y in range(SIZE):  # join neighbouring pixels of one color into a single rectangle per row
        x = 0
        while x < SIZE:
            color = pixels.get((x, y))
            if color is None:
                x += 1
                continue
            end = x
            while pixels.get((end + 1, y)) == color:
                end += 1
            rects.append(f'<rect x="{x}" y="{y}" width="{end - x + 1}" height="1" fill="{color}"/>')
            x = end + 1
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" shape-rendering="crispEdges" '
            f'aria-hidden="true">{"".join(rects)}</svg>')
