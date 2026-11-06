"""Draws the pet SVG files in backend/avatar/assets/pets/ in one soft, rounded style.

Pets are on hold, and the avatars no longer use these files (they are drawn by DiceBear and sprites.py).

Run from the project root:  python tools/make_assets.py
Re-running rewrites all 20 files, so change a drawing here, not in the SVG files.

How the look is built (so every part matches):
- Same soft outline on everything (a darker, half-transparent line).
- Every filled shape gets a gentle top-to-bottom shine drawn over it (the "sh" gradient).
"""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "backend" / "avatar" / "assets"
DARK = "#3B4752"
LINE = 'stroke="#3E5062" stroke-opacity=".5" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"'
# The shine gradient is identical in every file, so it is safe when several parts share one page.
DEFS = ('<defs><linearGradient id="sh" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#FFFFFF" stop-opacity=".4"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#000000" stop-opacity=".12"/></linearGradient></defs>')


def svg(inner: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n{DEFS}\n{inner}\n</svg>\n'


def write(rel: str, inner: str) -> None:
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg(inner), encoding="utf-8")


def B(tag: str, attrs: str) -> str:
    """Body part: primary color with outline and shine."""
    return f'<{tag} {attrs} fill="currentColor" {LINE}/><{tag} {attrs} fill="url(#sh)"/>'


def D(tag: str, attrs: str, opacity: float = 0.4) -> str:
    """Darker tone of the primary color (hair, ears, horns)."""
    return f'<{tag} {attrs} fill="currentColor" {LINE}/><{tag} {attrs} fill="#1F2D3A" fill-opacity="{opacity}"/><{tag} {attrs} fill="url(#sh)"/>'


def W(tag: str, attrs: str, opacity: float = 0.45) -> str:
    """Light patch over a body part (muzzle, inner ear, belly)."""
    return f'<{tag} {attrs} fill="#FFFFFF" fill-opacity="{opacity}"/>'


def P(tag: str, attrs: str, fill: str) -> str:
    """Fixed-color part (pets) with the same outline and shine."""
    return f'<{tag} {attrs} fill="{fill}" {LINE}/><{tag} {attrs} fill="url(#sh)"/>'


SHADOW = '<ellipse cx="50" cy="92" rx="28" ry="4" fill="#1F2D3A" fill-opacity=".1"/>'
PINK, GREEN, SAND, LILAC, STEEL, GOLD, POT = "#EFB3C4", "#A7D8AA", "#F4D9BC", "#CDBBE6", "#CBD9E4", "#F4DC93", "#E8B596"
PET_CHEEKS = lambda y, dx=8: f'<circle cx="{50 - dx - 5}" cy="{y}" r="3.2" fill="#F29CB0" fill-opacity=".4"/><circle cx="{50 + dx + 5}" cy="{y}" r="3.2" fill="#F29CB0" fill-opacity=".4"/>'
PET_EYES = lambda y, dx=6, r=2.2: "".join(f'<circle cx="{50 + s * dx}" cy="{y}" r="{r}" fill="{DARK}"/><circle cx="{50 + s * dx + 0.8}" cy="{y - 0.8}" r="0.8" fill="#FFFFFF"/>' for s in (-1, 1))
SMILE = lambda y: f'<path d="M46 {y} Q50 {y + 3} 54 {y}" fill="none" stroke="{DARK}" stroke-width="1.5" stroke-linecap="round"/>'


def leaf(x: float, y: float, side: int) -> str:
    """A pointed leaf growing to the left (side -1) or right (side 1) of the stem."""
    return (P("path", f'd="M{x} {y} Q{x + side * 9} {y - 9} {x + side * 16} {y - 3} Q{x + side * 9} {y + 5} {x} {y}Z"', GREEN)
            + f'<path d="M{x} {y} L{x + side * 12} {y - 3}" stroke="#6FA377" stroke-width="1" stroke-linecap="round"/>')


def plant(st: int) -> str:
    h = 8 + 6 * st
    top = 70 - h
    leaves = "".join(leaf(50, 70 - h * (k + 0.7) / (st + 1), 1 if k % 2 else -1) for k in range(st + 1))
    flower = ""
    if st == 4:
        flower = P("circle", f'cx="50" cy="{top - 3}" r="5"', PINK)
    if st == 5:
        petals = "".join(P("circle", f'cx="{50 + 8 * math.cos(a * math.pi / 3):.1f}" cy="{top - 4 + 8 * math.sin(a * math.pi / 3):.1f}" r="5.2"', PINK) for a in range(6))
        flower = petals + P("circle", f'cx="50" cy="{top - 4}" r="4.6"', GOLD)
    ribbon = P("rect", 'x="32" y="67" width="36" height="7" rx="3"', "#E3A7BC") if st >= 3 else P("rect", 'x="32" y="67" width="36" height="7" rx="3"', "#DDA386")
    return (f'{SHADOW}<line x1="50" y1="70" x2="50" y2="{top}" stroke="#6FA377" stroke-width="3.2" stroke-linecap="round"/>{leaves}{flower}'
            + P("path", 'd="M34 92 Q33 80 37 73 L63 73 Q67 80 66 92Z"', POT) + ribbon + PET_EYES(82, 5.5, 1.9) + SMILE(86) + PET_CHEEKS(85, 7))


def small_animal(st: int) -> str:
    tail = P("circle", 'cx="75" cy="76" r="9"', SAND) + W("circle", 'cx="77" cy="77" r="4"', 0.6) if st >= 4 else ""
    scarf = P("rect", 'x="34" y="62" width="32" height="8" rx="4"', "#E3A7BC") + '<path d="M58 69 L58 78 L63 78 L63 69Z" fill="#E3A7BC" stroke="#3E5062" stroke-opacity=".5" stroke-width="1.2"/>' if st >= 3 else ""
    flower = P("circle", 'cx="38" cy="39" r="3.8"', PINK) + '<circle cx="38" cy="39" r="1.4" fill="#F4DC93"/>' if st >= 5 else ""
    return (f'{SHADOW}{tail}' + P("ellipse", 'cx="50" cy="77" rx="22" ry="15"', SAND)
            + P("ellipse", 'cx="37" cy="36" rx="5.5" ry="11"', SAND) + P("ellipse", 'cx="63" cy="36" rx="5.5" ry="11"', SAND)
            + W("ellipse", 'cx="37" cy="37" rx="2.5" ry="6.5"', 0.7).replace("#FFFFFF", "#F2A6B8") + W("ellipse", 'cx="63" cy="37" rx="2.5" ry="6.5"', 0.7).replace("#FFFFFF", "#F2A6B8")
            + P("circle", 'cx="50" cy="54" r="17"', SAND) + PET_EYES(52, 6.5, 2.3) + '<ellipse cx="50" cy="58" rx="2.6" ry="1.9" fill="#C97C8C"/>'
            + PET_CHEEKS(58, 9) + scarf + flower)


def robot_buddy(st: int) -> str:
    antenna = (f'<line x1="50" y1="52" x2="50" y2="42" {LINE}/>' + P("circle", f'cx="50" cy="40" r="{5 if st >= 5 else 3.6}"', GOLD if st >= 5 else STEEL)) if st >= 2 else ""
    arms = P("rect", 'x="21" y="62" width="9" height="19" rx="4.5"', STEEL) + P("rect", 'x="70" y="62" width="9" height="19" rx="4.5"', STEEL) if st >= 4 else ""
    badge = P("circle", 'cx="50" cy="79" r="4.2"', GOLD) if st >= 3 else ""
    return (f'{SHADOW}{antenna}{arms}' + P("rect", 'x="31" y="52" width="38" height="35" rx="10"', STEEL)
            + '<rect x="36" y="57" width="28" height="16" rx="6" fill="#3B4752"/>'
            + '<circle cx="44" cy="65" r="2.6" fill="#FFFFFF"/><circle cx="56" cy="65" r="2.6" fill="#FFFFFF"/>'
            + f'{badge}' + P("circle", 'cx="40" cy="89" r="4.2"', "#6B7C8B") + P("circle", 'cx="60" cy="89" r="4.2"', "#6B7C8B"))


def creature(st: int) -> str:
    wings = P("ellipse", 'cx="23" cy="66" rx="9" ry="14"', "#E6DCF3") + P("ellipse", 'cx="77" cy="66" rx="9" ry="14"', "#E6DCF3") if st >= 5 else ""
    horns = P("path", 'd="M36 52 L31 37 L45 48Z"', GOLD) + P("path", 'd="M64 52 L69 37 L55 48Z"', GOLD) if st >= 3 else ""
    belly = W("ellipse", 'cx="50" cy="77" rx="12" ry="9"', 0.55) if st >= 2 else ""
    dots = '<circle cx="35" cy="73" r="2.6" fill="#B6A0D2"/><circle cx="67" cy="69" r="2.6" fill="#B6A0D2"/>' if st >= 4 else ""
    return (f'{SHADOW}{wings}' + P("path", 'd="M25 80 C21 55 38 45 52 47 C73 49 79 66 75 82 C71 93 29 93 25 80Z"', LILAC)
            + f'{horns}{belly}{dots}' + PET_EYES(62, 8.5, 2.5) + PET_CHEEKS(68, 12) + SMILE(68))


PETS = {"plant": plant, "small_animal": small_animal, "robot_buddy": robot_buddy, "creature": creature}
for name, draw in PETS.items():
    for stage in range(1, 6):
        scale = 0.5 + 0.1 * stage  # the pet is drawn bigger at each stage
        body = f'<g transform="translate(50 92) scale({scale:.1f}) translate(-50 -92)">{draw(stage)}</g>'
        cloud = '<ellipse cx="20" cy="16" rx="12" ry="5" fill="#E8EEF3"/><ellipse cx="28" cy="13" rx="8" ry="5" fill="#E8EEF3"/>' if stage >= 4 else ""
        spark = f'<path d="M82 10 L84 16 L90 18 L84 20 L82 26 L80 20 L74 18 L80 16Z" fill="{GOLD}"/>' if stage >= 5 else ""
        write(f"pets/{name}_{stage}.svg", cloud + spark + body)

print("done:", len(list(OUT.rglob("*.svg"))), "files")
