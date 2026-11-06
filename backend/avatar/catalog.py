"""The closed list of avatar choices: four bases, each with its own options.

A student never types anything to build an avatar; every option is picked from the lists below.
- human is drawn by DiceBear (its "pixel-art" style, CC0).
- animal, creature and robot are drawn by our own sprites (see sprites.py), because DiceBear has no pixel art
  animals or creatures, and its robot is only a glowing face (no head, antenna or body).

Each choice has an id (what gets saved), a label (what the student reads) and params (what the drawing code needs).
Only the ids and labels leave the server; the params stay inside (see public_catalog).
"""


def _choice(cid: str, label: str, params: dict, swatch: str | None = None) -> dict:
    choice = {"id": cid, "label": label, "params": params}
    if swatch:
        choice["swatch"] = swatch  # a color the screen can show as a small square
    return choice


def _option(oid: str, label: str, choices: list[dict]) -> dict:
    return {"id": oid, "label": label, "default": choices[0]["id"], "choices": choices}


def _colors(oid: str, label: str, key: str, hexes: list[str], wrap: bool = False) -> dict:
    """A color option. `wrap` is True for DiceBear, which wants colors as a list without the #."""
    choices = [
        _choice(h, f"Color {i}", {key: [h.lstrip("#")] if wrap else "#" + h.lstrip("#")}, "#" + h.lstrip("#"))
        for i, h in enumerate(hexes, 1)
    ]
    return _option(oid, label, choices)


def _variants(oid: str, label: str, key: str, names: list[str], words: str, probability: str | None = None,
              none: bool = False) -> dict:
    """A list of drawings. `probability` is the DiceBear option that switches the part on (0 = never, 100 = always)."""
    choices = []
    if none:
        choices.append(_choice("none", "None", {probability: 0}))
    for i, name in enumerate(names, 1):
        params = {key: [name]}
        if probability:
            params[probability] = 100
        choices.append(_choice(name, f"{words} {i}", params))
    return _option(oid, label, choices)


def _sprite(oid: str, label: str, key: str, names: list[str]) -> dict:
    return _option(oid, label, [_choice(n, n.capitalize(), {key: n}) for n in names])


SKIN = ["ffdbac", "f5cfa0", "eac393", "e0b687", "cb9e6e", "b68655", "a26d3d", "8d5524"]
HAIR_COLOR = ["cab188", "a78961", "83623b", "603a14", "611c17", "28150a", "bd1700", "009bbd", "91cb15"]
HAIR = ["short01", "short02", "short05", "short06", "short09", "short11", "short14", "short17", "short20",
        "long01", "long02", "long05", "long08", "long12", "long15", "long19"]
CLOTHING = ["428bca", "5bc0de", "03396c", "88d8b0", "44c585", "ff6f69", "d11141", "ffd969"]
ACCESSORY_COLOR = ["ffd969", "ff6f69", "5bc0de", "88d8b0", "c4b5fd", "ffffff"]
FUR = ["e9c79b", "c48b5a", "8a5a3a", "5b4636", "9aa3ae", "e8e4da", "e39b4f", "2f3340"]
CREATURE_COLOR = ["7bc6a4", "8fb8f0", "c9a7f0", "f09ba8", "f0d56b", "9bd66e", "f0a872", "6fd0d6"]
METAL = ["b8c2d0", "e8ecf1", "8e9aab", "6b7a90", "e3c36b", "d4915f", "8fd3c1", "e08a8a"]
GLOW = ["7dd3fc", "5eead4", "86efac", "bef264", "fde68a", "fdba74", "f9a8d4", "c4b5fd", "ffffff"]
SCREEN = ["0f172a", "172554", "1e1b4b", "2e1065", "500724", "022c22"]


def _sprite_base(base_id: str, label: str, group: str, body_key: str, body_label: str, bodies: list[str],
                 colors: list[str], eyes: list[str], mouths: list[str]) -> dict:
    return {
        "id": base_id, "label": label, "engine": "sprite", "group": group, "fixed": {},
        "options": [
            _sprite("body", body_label, "body", bodies),
            _colors("color", "Color", "fur", colors),
            _sprite("eyes", "Eyes", "eyes", eyes),
            _sprite("mouth", "Mouth", "mouth", mouths),
            _sprite("accessory", "Extra", "accessory", ["none", "glasses", "sunglasses", "headband"]),
            _colors("accessory_color", "Extra color", "accessory_color", ACCESSORY_COLOR),
            _sprite("clothes", "Clothes", "clothes", ["tee", "collar", "stripes"]),
            _colors("clothing_color", "Clothes color", "clothing", CLOTHING),
        ],
    }


BASES = [
    {
        "id": "human", "label": "Human", "engine": "dicebear", "style": "pixel-art",
        # Everything not chosen by the student is switched off, so the same choices always give the same picture.
        "fixed": {"seed": "avatar", "beardProbability": 0, "accessoriesProbability": 0, "mouthColor": ["c98276"],
                  "glassesColor": ["4b4b4b"], "eyesColor": ["647b90"]},
        "options": [
            _colors("skin", "Skin", "skinColor", SKIN, wrap=True),
            _variants("hair", "Hair", "hairVariant", HAIR, "Hair", "hairProbability"),
            _colors("hair_color", "Hair color", "hairColor", HAIR_COLOR, wrap=True),
            _variants("eyes", "Eyes", "eyesVariant", ["variant01", "variant02", "variant03", "variant05", "variant08", "variant11"],
                      "Eyes", "eyesProbability"),
            _variants("mouth", "Mouth", "mouthVariant", ["happy01", "happy02", "happy04", "happy07"], "Smile", "mouthProbability"),
            _variants("glasses", "Glasses", "glassesVariant", ["dark01", "dark03", "dark05", "light02"], "Glasses",
                      "glassesProbability", none=True),
            _variants("hat", "Hat", "hatVariant", ["variant01", "variant03", "variant06", "variant08"], "Hat",
                      "hatProbability", none=True),
            _colors("hat_color", "Hat color", "hatColor", ["2663a3", "3d8a6b", "cc6192", "614f8a", "a62116", "2e1e05"], wrap=True),
            _variants("clothes", "Clothes", "clothesVariant",
                      ["variant01", "variant02", "variant03", "variant05", "variant07", "variant13", "variant16", "variant19"],
                      "Clothes", "clothesProbability"),
            _colors("clothing_color", "Clothes color", "clothingColor", CLOTHING, wrap=True),
        ],
    },
    _sprite_base("animal", "Animal", "animal", "body", "Animal", ["cat", "dog", "rabbit", "bear"], FUR,
                 ["dots", "tall", "big", "happy", "sleepy"], ["smile", "open", "flat", "nose"]),
    {
        # A robot with a head, an antenna and a body, drawn by our sprites (the screen and the lights are customizable).
        "id": "robot", "label": "Robot", "engine": "sprite", "group": "robot", "fixed": {},
        "options": [
            _sprite("head", "Head", "head", ["dome", "oval", "round", "square"]),
            _colors("color", "Metal color", "fur", METAL),
            _sprite("antenna", "Antenna", "antenna", ["ball", "double", "stick", "none"]),
            _sprite("eyes", "Eyes", "eyes", ["round", "happy", "blocks", "soft", "tall", "slim", "wide"]),
            _sprite("mouth", "Mouth", "mouth", ["smile", "big", "flat", "tiny", "open"]),
            _colors("glow", "Light color", "glow", GLOW),
            _colors("screen", "Screen color", "screen", SCREEN),
            _sprite("torso", "Body", "torso", ["plain", "panel", "stripe", "lights"]),
            _colors("clothing_color", "Body color", "clothing", CLOTHING),
        ],
    },
    _sprite_base("creature", "Creature", "creature", "body", "Shape", ["blob", "alien", "dragon", "monster"],
                 CREATURE_COLOR, ["dots", "big", "cyclops", "three", "sleepy"], ["smile", "open", "fangs", "flat"]),
]

BY_ID = {b["id"]: b for b in BASES}


def public_catalog() -> dict:
    """What the API sends to the screens: ids, labels and swatches, never the drawing params."""
    return {
        "bases": [
            {
                "id": b["id"], "label": b["label"],
                "options": [
                    {"id": o["id"], "label": o["label"], "default": o["default"],
                     "choices": [{k: v for k, v in c.items() if k != "params"} for c in o["choices"]]}
                    for o in b["options"]
                ],
            }
            for b in BASES
        ]
    }


def defaults(base_id: str) -> dict:
    return {o["id"]: o["default"] for o in BY_ID[base_id]["options"]}


def problems(base_id: str, picked: dict) -> list[str]:
    """Return what is wrong with a set of choices (empty list = fine). Only listed choices are allowed."""
    base = BY_ID.get(base_id)
    if base is None:
        return [f"unknown base: {base_id}"]
    found = []
    options = {o["id"]: {c["id"] for c in o["choices"]} for o in base["options"]}
    for oid, cid in picked.items():
        if oid not in options:
            found.append(f"{base_id} has no option called {oid}")
        elif cid not in options[oid]:
            found.append(f"{cid} is not a choice for {oid}")
    return found


def resolve(base_id: str, picked: dict) -> dict:
    """Join the fixed params of the base with the params of every chosen (or default) choice."""
    base = BY_ID[base_id]
    params = dict(base["fixed"])
    for option in base["options"]:
        wanted = picked.get(option["id"], option["default"])
        choice = next(c for c in option["choices"] if c["id"] == wanted)
        params.update(choice["params"])
    return params
