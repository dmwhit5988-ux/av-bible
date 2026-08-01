"""Render Genesis 4 (Cain's line) as per-verse vector SVGs.

One family tree, replayed for all 26 verses. The chapter is two things at once:
the story of the first murder (verses 1-16) and the first genealogy — Cain's
line down seven generations to Lamech and his three sons, the fathers of
herding, music, and metalwork (17-24) — closing with Seth and Enosh in Adam's
other line (25-26). So the tree is on screen throughout, and the story plays
across it: the two offerings, the strike that kills Abel, the curse and the
sign on Cain, then the descent lighting name by name.

Newly named people arrive with their connector drawing itself once and then
holding, matching the other genealogy graphics. Verse 15's "vengeance
sevenfold" is drawn as a chip that Lamech's "seventy-seven times" answers in
verse 24 — the chapter's own escalation, made visible.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_genesis4_svg.py
"""

import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, TEXT,
                                 TEXT_DIM, GOLD, HL, out_path)

RED = (170, 70, 60)            # the blood, and the strike
BLOOD = (150, 62, 54)


def g(alpha):
    return HL + (int(255 * alpha),)


def dim(color, a):
    """`color` with an 0-255 alpha, in the (r, g, b, a) form SvgCanvas takes
    (it turns the fourth element into a fill-/stroke-opacity)."""
    return color + (int(a),)


# ---------------------------------------------------------------------------
# Nodes:  key -> (label, sub, x, y, w, h, intro verse)
# `sub` renders inside the box under the name; None leaves the box name-only.
# ---------------------------------------------------------------------------

NODES = {
    "ADAM":   ("Adam  ·  Eve", None, 405, 108, 200, 30, 1),
    "ABEL":   ("Abel", "keeper of sheep", 150, 176, 150, 44, 2),
    "CAIN":   ("Cain", "tiller of the ground", 330, 176, 150, 44, 1),
    "SETH":   ("Seth", "instead of Abel", 660, 176, 150, 44, 25),
    "ENOSH":  ("Enosh", None, 660, 248, 150, 44, 26),
    "ENOCH":  ("Enoch", None, 330, 226, 150, 28, 17),
    "IRAD":   ("Irad", None, 330, 272, 150, 28, 18),
    "MEHUJAEL": ("Mehujael", None, 330, 318, 150, 28, 18),
    "METHUSHAEL": ("Methushael", None, 330, 364, 150, 28, 18),
    "LAMECH": ("Lamech", None, 330, 406, 150, 28, 18),
    "ADAH":   ("Adah", None, 215, 452, 100, 26, 19),
    "ZILLAH": ("Zillah", None, 445, 452, 100, 26, 19),
}

# Lamech's four children carry their trade on two lines inside a taller box.
CHILDREN = [
    ("JABAL", "Jabal", ["tents & livestock"], 106, 20),
    ("JUBAL", "Jubal", ["harp & pipe"], 248, 21),
    ("TUBAL", "Tubal Cain", ["brass & iron"], 400, 22),
    ("NAAMAH", "Naamah", [], 542, 22),
]
CHILD_Y, CHILD_W, CHILD_H = 508, 134, 54

# Parent -> child edges of the trunk (drawn as elbow connectors).
EDGES = [
    ("ADAM", "ABEL"), ("ADAM", "CAIN"), ("ADAM", "SETH"),
    ("CAIN", "ENOCH"), ("ENOCH", "IRAD"), ("IRAD", "MEHUJAEL"),
    ("MEHUJAEL", "METHUSHAEL"), ("METHUSHAEL", "LAMECH"),
    ("LAMECH", "ADAH"), ("LAMECH", "ZILLAH"), ("SETH", "ENOSH"),
]
CHILD_EDGES = [("ADAH", "JABAL"), ("ADAH", "JUBAL"),
               ("ZILLAH", "TUBAL"), ("ZILLAH", "NAAMAH")]

# ---------------------------------------------------------------------------
# The annotations on Cain — the curse, the sign, and the land he goes to.
# (verse it lights, y, line 1, line 2)
# ---------------------------------------------------------------------------

CHIP_X, CHIP_W, CHIP_H = 412, 158, 46
CHIPS = [
    (11, 218, "cursed", ""),
    (12, 272, "a fugitive", ""),
    (15, 326, "the sign · sevenfold", ""),
    (16, 380, "Nod, east of Eden", ""),
]
BOAST = (604, 380, 140, 54)     # Lamech's answer to verse 15

# ---------------------------------------------------------------------------
# Which nodes the current verse lights
# ---------------------------------------------------------------------------

LIT = {
    1: ["CAIN"], 2: ["ABEL"], 3: ["CAIN"], 4: ["ABEL"], 5: ["CAIN"],
    6: ["CAIN"], 7: ["CAIN"], 8: ["CAIN", "ABEL"], 9: ["ABEL"],
    10: ["ABEL"], 11: ["CAIN"], 12: ["CAIN"], 13: ["CAIN"], 14: ["CAIN"],
    15: ["CAIN"], 16: ["CAIN"], 17: ["ENOCH"],
    18: ["IRAD", "MEHUJAEL", "METHUSHAEL", "LAMECH"],
    19: ["ADAH", "ZILLAH"], 20: ["JABAL"], 21: ["JUBAL"],
    22: ["TUBAL", "NAAMAH"], 23: ["LAMECH"], 24: ["LAMECH"],
    25: ["SETH"], 26: ["ENOSH"],
}

# ---------------------------------------------------------------------------
# The chapter's beats (side panel)
# ---------------------------------------------------------------------------

BEATS = [
    (1, 2, "Two sons born", "Cain the tiller, Abel the shepherd"),
    (3, 5, "Two offerings", "Abel’s respected, Cain’s not"),
    (6, 7, "The warning", "sin crouches at the door"),
    (8, 8, "The murder", "Cain rose up against his brother"),
    (9, 12, "The curse", "the blood cries out from the ground"),
    (13, 15, "The sign", "vengeance sevenfold on whoever slays him"),
    (16, 16, "East of Eden", "Cain lived in the land of Nod"),
    (17, 18, "Cain’s line", "Enoch to Methushael — five generations"),
    (19, 19, "Two wives", "Adah and Zillah"),
    (20, 22, "Three trades", "tents, harp and pipe, brass and iron"),
    (23, 24, "Lamech’s boast", "seventy-seven times"),
    (25, 26, "Seth instead", "and Enosh — men call on Yahweh’s name"),
]


def beat_index(v):
    for i, (lo, hi, _t, _n) in enumerate(BEATS):
        if lo <= v <= hi:
            return i
    return 0


# ---------------------------------------------------------------------------
# Node geometry helpers
# ---------------------------------------------------------------------------

def box(key):
    """(x0, y0, x1, y1) of a node's box."""
    for ck, label, lines, cx, intro in CHILDREN:
        if ck == key:
            return (cx - CHILD_W / 2, CHILD_Y - CHILD_H / 2,
                    cx + CHILD_W / 2, CHILD_Y + CHILD_H / 2)
    _l, _s, x, y, w, h, _i = NODES[key]
    return x - w / 2, y - h / 2, x + w / 2, y + h / 2


def intro_of(key):
    for ck, _l, _lines, _cx, intro in CHILDREN:
        if ck == key:
            return intro
    return NODES[key][6]


def draw_node_box(c, x0, y0, x1, y1, live, lit, first=True):
    c.rect(x0, y0, x1 - x0, y1 - y0,
           fill=PANEL if live else BG,
           stroke=None if lit else (SAND if live else SAND_DIM),
           width=1.5, rx=4)
    if lit:
        # a brighten on the verse the name is spoken, not a redraw on every
        # verse it stays lit
        c.pulse_rect(x0, y0, x1 - x0, y1 - y0, g(0.95), width=2.5,
                     first=first, rx=4)


def draw_nodes(c, v):
    lit_keys = set(LIT.get(v, ()))
    was_lit = set(LIT.get(v - 1, ()))
    for key, (label, sub, x, y, w, h, intro) in NODES.items():
        live = v >= intro
        lit = key in lit_keys
        x0, y0, x1, y1 = box(key)
        struck = (key == "ABEL" and v >= 8)
        draw_node_box(c, x0, y0, x1, y1, live, lit, first=key not in was_lit)
        name_col = HL if lit else (TEXT if live else TEXT_DIM)
        if struck and not lit:
            name_col = dim(TEXT_DIM, 200)
        ny = y - 9 if sub else y
        c.text((x, ny), label, 16 if sub else 15, name_col, "mm", bold=live)
        if sub:
            c.text((x, y + 11), sub, 11,
                   GOLD if lit else (TEXT_DIM if live else dim(TEXT_DIM, 150)),
                   "mm", italic=True)
        if struck:
            c.line((x0 + 8, y), (x1 - 8, y), RED, 2)

    for key, label, lines, cx, intro in CHILDREN:
        live = v >= intro
        lit = key in lit_keys
        x0, y0, x1, y1 = box(key)
        draw_node_box(c, x0, y0, x1, y1, live, lit, first=key not in was_lit)
        c.text((cx, CHILD_Y - 16), label, 15,
               HL if lit else (TEXT if live else TEXT_DIM), "mm", bold=live)
        for i, line in enumerate(lines):
            c.text((cx, CHILD_Y + 2 + i * 13), line, 10,
                   GOLD if lit else (TEXT_DIM if live else dim(TEXT_DIM, 150)),
                   "mm", italic=True)


def draw_edges(c, v):
    """Elbow connectors. A child's edge draws itself in on the verse that
    names the child, and is a static line afterwards."""
    for parent, child in EDGES + CHILD_EDGES:
        ci = intro_of(child)
        if v < ci:
            continue
        px0, py0, px1, py1 = box(parent)
        cx0, cy0, cx1, cy1 = box(child)
        pxc, cxc = (px0 + px1) / 2, (cx0 + cx1) / 2
        mid = (py1 + cy0) / 2
        pts = ([(pxc, py1), (pxc, mid), (cxc, mid), (cxc, cy0)]
               if abs(pxc - cxc) > 1 else [(pxc, py1), (cxc, cy0)])
        if v == ci:
            c.traced(pts, stroke=GOLD, width=2.5, dur="1.8s")
        else:
            c.polyline(pts, stroke=SAND_DIM + (255,), width=2)


def draw_offerings(c, v):
    """The two offerings (verses 3-5), under Abel's side of the tree."""
    if v < 3:
        return
    for who, x, label, sub, verse in (
            ("ABEL", 88, "Abel’s", None, 4),
            ("CAIN", 238, "Cain’s", None, 3)):
        lit = (v == verse) or (who == "CAIN" and v == 5)
        accepted = (who == "ABEL")
        y = 250
        col = HL if lit else (TEXT if v >= verse else TEXT_DIM)
        # a small altar mound
        c.polygon([(x - 18, y + 10), (x + 18, y + 10), (x + 12, y - 2),
                   (x - 12, y - 2)],
                  fill=dim(SAND_DIM, 200), stroke=col, width=1.5)
        if accepted:
            flame = [(x, y - 26), (x + 7, y - 12), (x - 7, y - 12)]
            c.polygon(flame, fill=GOLD if v >= 4 else None,
                      stroke=GOLD if v >= 4 else SAND_DIM, width=1.5)
        else:
            c.polyline([(x - 6, y - 6), (x + 5, y - 14), (x - 4, y - 22)],
                       stroke=SAND_DIM + (255,), width=1.5, dash="3,4")
            if v >= 5:
                c.line((x - 12, y - 24), (x + 12, y - 4), RED, 2.5)
                c.line((x + 12, y - 24), (x - 12, y - 4), RED, 2.5)
        c.text((x, y + 24), label, 13, col, "mm", bold=lit)


def draw_murder(c, v):
    """Verse 8 onward: the strike from Cain to Abel, and the blood."""
    if v < 8:
        return
    ax0, ay0, ax1, ay1 = box("ABEL")
    cx0, cy0, cx1, cy1 = box("CAIN")
    pts = [(cx0 - 2, 176), (ax1 + 2, 176)]
    if v == 8:
        c.traced(pts, stroke=RED, width=3.5, dur="1.4s")
    else:
        c.polyline(pts, stroke=dim(RED, 190), width=2)
    c.polygon([(ax1 + 2, 176), (ax1 + 14, 171), (ax1 + 14, 181)],
              fill=RED if v == 8 else dim(RED, 190))
    if 10 <= v <= 12:
        # below the two offerings, so it never lands on the altars
        bx = (ax0 + ax1) / 2
        c.polyline([(bx, 348), (bx - 8, 330), (bx + 7, 312)],
                   stroke=BLOOD, width=2.5, dash="3,4")


def draw_chips(c, v):
    """Cain's sentence, chip by chip, and Lamech's answer to the sevenfold."""
    for verse, y, l1, l2 in CHIPS:
        if v < verse:
            continue
        lit = (v == verse) or (verse == 12 and v in (13, 14))
        c.rect(CHIP_X, y, CHIP_W, CHIP_H, fill=PANEL,
               stroke=None if lit else SAND, width=1.5, rx=4)
        if lit:
            c.pulse_rect(CHIP_X, y, CHIP_W, CHIP_H, g(0.9), width=2.5,
                         first=(v == verse), rx=4)
        c.text((CHIP_X + 12, y + CHIP_H / 2), l1, 12, HL if lit else TEXT,
               "lm", bold=lit)

    if v >= 11:  # the connector from Cain into his sentence
        c.polyline([(405, 176), (CHIP_X - 6, 176), (CHIP_X - 6, 241),
                    (CHIP_X, 241)], stroke=SAND_DIM + (255,), width=1.5,
                   dash="4,5")

    if v >= 23:
        bx, by, bw, bh = BOAST
        lit = (v == 24)
        c.rect(bx, by, bw, bh, fill=PANEL, stroke=None if lit else SAND,
               width=1.5, rx=4)
        if lit:
            c.pulse_rect(bx, by, bw, bh, g(0.9), width=2.5, first=True, rx=4)
        c.text((bx + bw / 2, by + bh / 2), "seventy-seven", 12,
               HL if lit else TEXT, "mm", bold=lit)
        # the escalation: Cain's sevenfold chip answered here
        c.polyline([(CHIP_X + CHIP_W, 349), (bx - 10, 349), (bx - 10, by + 20),
                    (bx, by + 20)], stroke=GOLD if lit else SAND_DIM,
                   width=1.5, dash="3,4")


# ---------------------------------------------------------------------------
# Side panel
# ---------------------------------------------------------------------------

PANEL_X = 764
ROW0, ROWH = 122, 34


def draw_panel(c, v):
    cur = beat_index(v)
    c.text((PANEL_X, 90), "THE FIRST FAMILY", 18, TEXT, "la", bold=True)
    dot_x, name_x = PANEL_X + 8, PANEL_X + 24
    c.line((dot_x, ROW0), (dot_x, ROW0 + (len(BEATS) - 1) * ROWH), SAND_DIM, 2)
    for i, (lo, hi, title, note) in enumerate(BEATS):
        y = ROW0 + i * ROWH
        live = (i == cur)
        if live:
            c.circle(dot_x, y, 6, fill=HL, stroke=BG, width=1)
        else:
            c.circle(dot_x, y, 4, fill=SAND if i < cur else BG,
                     stroke=SAND_DIM, width=1.5)
        c.text((name_x, y), title, 14,
               HL if live else (TEXT if i < cur else TEXT_DIM), "lm",
               bold=live)
        rng = f"{lo}" if lo == hi else f"{lo}–{hi}"
        c.text((W - 16, y), rng, 10, TEXT_DIM, "rm", italic=True)


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

def render(v):
    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 24), "Genesis 4 · Cain’s Line", 22, TEXT, "la", bold=True)

    draw_edges(c, v)
    draw_offerings(c, v)
    draw_murder(c, v)
    draw_chips(c, v)
    draw_nodes(c, v)
    draw_panel(c, v)
    return c


def main():
    total = count = 0
    for v in range(1, 27):
        c = render(v)
        out = out_path("Genesis", 4, f"Genesis_4_{v}.svg")
        c.save(out)
        total += os.path.getsize(out)
        count += 1
    print(f"Genesis 4: {count} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
