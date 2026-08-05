"""Render the whole letter to the Romans (16 chapters, 433 verses) as
per-verse vector SVGs from one spec.

The infographic catalog listed three separate Romans candidates — the
argument arc of the whole letter, the Adam/Christ parallel of chapter 5, and
the olive tree of 9-11. They are one object at three zoom levels: the two
set-pieces are stops on the arc. So this generator draws one frame that never
changes shape:

    rail (left)                 stage (right)
    the seven stops of the      the current stop's set-piece, drawn large
    argument, each an emblem    and reacting to the beat of the passage
    of its own set-piece;
    the current one lit

Every rail emblem is a miniature of the stage drawing it opens, so the rail
reads as a row of thumbnails of the same seven pictures rather than a table
of contents.

Text budget (INFOGRAPHIC "less is more" rule — the verse is being read
aloud, so the canvas must not restate it):

* No captions, no prose, no footnotes anywhere.
* Along the bottom runs a bead track, one bead per verse of the chapter.
  Only the *current* bead is labelled, with a single word. Every other verse
  of the chapter is an unlabelled dot. That is where the per-verse motion
  lives, which frees the set-piece above to move only at the beats.
* The set-pieces carry names, numbers and labelled parts — never sentences.
  Where a passage is a list (the gifts, the golden chain, the saints greeted
  in chapter 16), the drawing lights a part and lets the bead say the word.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_romans_svg.py
"""

import math
import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, TEXT,
                                 TEXT_DIM, HL, GOLD, RED, BROWN, GRAY,
                                 out_path)

BOOK = "Romans"

# Two colours this book needs that the tabernacle palette has no name for.
OLIVE = (122, 146, 92)          # the good olive tree
WILD = (150, 168, 104)          # the wild branches grafted in


def dim(col, a):
    """The palette colour at `a` opacity."""
    return (col[0], col[1], col[2], int(255 * a))


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

RAIL_X = 24                      # rail column
RAIL_W = 214
GLYPH_X = 54                     # emblem centre in the rail
ROW0, ROWH = 106, 60

SX0, SX1 = 266, 996              # stage window
SY0, SY1 = 92, 486

CX = (SX0 + SX1) / 2             # 631
CY = (SY0 + SY1) / 2             # 289

TRACK_Y = 526                    # the per-verse bead track
TRACK_X0, TRACK_X1 = 286, 976
WORD_Y = 494                     # the one word belonging to this verse

CH_LEN = {1: 32, 2: 29, 3: 31, 4: 25, 5: 21, 6: 23, 7: 25, 8: 39,
          9: 33, 10: 21, 11: 36, 12: 21, 13: 14, 14: 23, 15: 33, 16: 27}

_OFFSET = {}
_run = 0
for _ch in range(1, 17):
    _OFFSET[_ch] = _run
    _run += CH_LEN[_ch]


def P(ch, v):
    """Reading position: one number across the whole letter, so 'has this
    been reached yet' is a single comparison."""
    return _OFFSET[ch] + v


def since(pos, ch, v):
    """(shown, first) for an element that appears at ch:v — `first` marks the
    one verse it animates on, per the house 'draw once, then hold' rule."""
    p = P(ch, v)
    return pos >= p, pos == p


# ---------------------------------------------------------------------------
# The seven stops of the argument. Each is (key, label, range, emblem).
# The label is the rail's whole text budget: two words, never a sentence.
# ---------------------------------------------------------------------------

STOPS = [
    ("ARC",    "The gospel",    "1:1–17"),
    ("DOCK",   "All guilty",    "1:18–3:20"),
    ("SCALE",  "Justified",     "3:21–4:25"),
    ("TWO",    "Adam · Christ", "5"),
    ("ASCENT", "Alive",         "6–8"),
    ("TREE",   "Israel",        "9–11"),
    ("BODY",   "One body",      "12–16"),
]
STOP_ROW = {key: i for i, (key, _, _) in enumerate(STOPS)}

# ---------------------------------------------------------------------------
# Beats:  chapter -> [(from_verse, stage, focus), ...]
# The stage changes rarely; the focus is what the set-piece reacts to.
# ---------------------------------------------------------------------------

BEATS = {
    1:  [(1, "ARC", "letter"), (8, "ARC", "road"), (16, "ARC", "arc"),
         (18, "DOCK", "gentile")],
    2:  [(1, "DOCK", "moralist"), (17, "DOCK", "jew")],
    3:  [(1, "DOCK", "jew"), (9, "DOCK", "all"), (21, "SCALE", "weight"),
         (24, "SCALE", "grace"), (27, "SCALE", "boast")],
    4:  [(1, "SCALE", "abraham"), (6, "SCALE", "david"), (9, "SCALE", "seal"),
         (13, "SCALE", "promise"), (23, "SCALE", "us")],
    5:  [(1, "TWO", "ladder"), (12, "TWO", "adam"), (15, "TWO", "both"),
         (20, "TWO", "abound")],
    6:  [(1, "ASCENT", "grave"), (8, "ASCENT", "risen"), (12, "ASCENT", "yield"),
         (20, "ASCENT", "wages")],
    7:  [(1, "ASCENT", "bond"), (7, "ASCENT", "divided")],
    8:  [(1, "ASCENT", "spirit"), (12, "ASCENT", "sons"), (18, "ASCENT", "groan"),
         (28, "ASCENT", "chain"), (31, "ASCENT", "hold")],
    9:  [(1, "TREE", "sorrow"), (6, "TREE", "election"), (14, "TREE", "mercy"),
         (25, "TREE", "remnant"), (30, "TREE", "stumble")],
    10: [(1, "TREE", "call"), (14, "TREE", "sent")],
    11: [(1, "TREE", "remnant"), (11, "TREE", "root"), (17, "TREE", "graft"),
         (25, "TREE", "restore"), (33, "TREE", "depth")],
    12: [(1, "BODY", "members")],
    13: [(1, "BODY", "powers"), (8, "BODY", "armour")],
    14: [(1, "BODY", "weak")],
    15: [(1, "BODY", "weak"), (14, "BODY", "journey")],
    16: [(1, "BODY", "names")],
}


def beat(ch, v):
    """(stage, focus, first) — `first` is True on the verse the beat starts,
    which is what the set-piece animates on."""
    cur = BEATS[ch][0]
    for entry in BEATS[ch]:
        if v >= entry[0]:
            cur = entry
    return cur[1], cur[2], v == cur[0]


# ---------------------------------------------------------------------------
# The bead track: one word per verse. This is the whole per-verse text budget
# of the graphic — a single word, and only for the verse being read.
# ---------------------------------------------------------------------------

TRACK = {
    1: ["Servant", "Promised", "David", "Resurrection", "Nations", "Called",
        "Rome", "Faith", "Prayers", "Journey", "Gift", "Comfort", "Fruit",
        "Debtor", "Ready", "Power", "Righteousness", "Wrath", "Manifest",
        "Creation", "Darkened", "Fools", "Images", "Uncleanness", "The lie",
        "Vile", "Error", "Reprobate", "Filled", "Haters", "Unforgiving",
        "Pleasure"],
    2: ["Inexcusable", "Truth", "Escape", "Goodness", "Hardness", "Deeds",
        "Glory", "Wrath", "Anguish", "Peace", "No respect", "Perish", "Doers",
        "By nature", "Conscience", "Secrets", "Boast", "Instructed", "Guide",
        "Teacher", "Steal", "Rob temples", "Dishonor", "Blasphemed",
        "Circumcision", "Counted", "Judge", "Outward", "Inward"],
    3: ["Advantage", "Revelations", "Unbelief", "True", "Vengeance", "Judge",
        "Lie", "Slander", "Under sin", "No one righteous", "No one seeks",
        "Unprofitable", "An open tomb", "Cursing", "Swift", "Destruction",
        "No peace", "No fear", "Stopped", "Not by works", "But now",
        "No difference", "All", "Freely", "Atoning sacrifice", "Justifier",
        "Excluded", "By faith", "Gentiles", "One God", "Established"],
    4: ["Abraham", "Works", "Counted", "Debt", "Ungodly", "David", "Forgiven",
        "Blessed", "Reckoned", "Uncircumcised", "Seal", "Father", "Promise",
        "Void", "Wrath", "Grace", "Nations", "Hope", "A hundred years",
        "Strong", "Persuaded", "Imputed", "For us", "Raised", "Justification"],
    5: ["Peace", "Access", "Patience", "Hope", "Love", "In due time",
        "Scarcely", "Sinners", "Saved", "Reconciled", "Atonement", "One man",
        "No law", "Adam", "Free gift", "Condemnation", "Reign", "All men",
        "Obedience", "Abounded", "Grace"],
    6: ["Continue?", "Dead", "Baptized", "Buried", "Planted", "Old man",
        "Freed", "Live", "No more", "Once", "Reckon", "Body", "Instruments",
        "Grace", "May it never be", "Servants", "Obeyed", "Free", "Holiness",
        "Once free", "Ashamed", "Fruit", "Wages"],
    7: ["Dominion", "Bound", "Loosed", "Married", "Sinful passions", "Delivered",
        "Covet", "Occasion", "I died", "Death", "Killed me", "Holy", "Exceeding",
        "Fleshly", "Hate", "Consent", "Dwells in me", "No good", "Evil", "In me",
        "A law", "Delight", "Warring", "Wretched", "Thanks"],
    8: ["No condemnation", "Free", "Sending", "Fulfilled", "Mind", "Peace",
        "Enmity", "Cannot", "Dwell", "Life", "Give life", "Debtors", "Put to death",
        "Led", "Abba", "Witness", "Heirs", "Sufferings", "Waits", "Vanity",
        "Liberty", "Groans", "Firstfruits", "Hope", "Patience",
        "Intercession", "Searches", "All things", "Foreknew", "Glorified",
        "For us", "Freely", "Elect", "Risen", "Separate", "Sheep",
        "Conquerors", "Powers", "Height"],
    9: ["Truth", "Sorrow", "Accursed", "Israelites", "The fathers", "Not all",
        "Isaac", "Promise", "Sarah", "Rebecca", "Election", "The elder",
        "Jacob", "Unrighteous?", "Moses", "Mercy", "Pharaoh", "Hardens",
        "Resisted", "O man", "The potter", "Vessels", "Riches", "Called",
        "My people", "Children", "A remnant", "Short work", "A seed",
        "Attained", "Israel", "Stumbled", "Sion"],
    10: ["Prayer", "Zeal", "Their own", "The end", "Moses", "Ascend",
         "Descend", "Nigh", "Confess", "Heart", "Ashamed", "No difference",
         "Whosoever", "Hear", "Sent", "Report", "Hearing", "Sound",
         "Jealousy", "Found", "Stretched"],
    11: ["Benjamin", "Elias", "Alone", "Seven thousand", "Remnant", "Grace",
         "Blinded", "Slumber", "A snare", "Darkened", "Jealousy", "Fulness",
         "Gentiles", "To jealousy", "Life", "Root", "Graffed", "Boast not",
         "Broken", "Unbelief", "Take heed", "Severity", "Again", "Contrary",
         "Mystery", "All Israel", "Covenant", "Beloved", "Gifts", "Mercy",
         "Through you", "Concluded", "The depth", "Counsellor", "Given",
         "Glory"],
    12: ["Sacrifice", "Transformed", "Soberly", "Members", "One body",
         "Prophecy", "Ministry", "Mercy", "Love", "Honor", "Fervent",
         "Prayer", "Hospitality", "Bless", "Weep", "Lowly", "Honest",
         "Peaceably", "Vengeance", "Coals", "Overcome"],
    13: ["Powers", "Ordinance", "Rulers", "The sword", "Conscience", "Tribute",
         "Dues", "Owe", "Neighbor", "Fulfilling", "Awake", "Armor",
         "Honestly", "Put on"],
    14: ["Receive", "Herbs", "Despise", "Stands", "Persuaded", "Thanks",
         "To himself", "The Lord's", "Lord", "The seat", "Every knee",
         "Account", "Stumblingblock", "Unclean", "Charitably", "Spoken",
         "Kingdom", "Approved", "Edify", "Pure", "Wine", "Happy", "Doubts"],
    15: ["The strong", "Edification", "Reproaches", "Learning", "Likeminded",
         "One mouth", "Receive", "Confirm", "Sing", "Rejoice", "Praise",
         "Jesse", "Joy", "Goodness", "Boldly", "Offering", "Glory",
         "Obedient", "Illyricum", "Foundation", "Understand", "Hindered",
         "Desire", "Spain", "Jerusalem", "Contribution", "Debtors", "Sealed",
         "Fulness", "Strive", "Delivered", "Refreshed", "Peace"],
    16: ["Phebe", "Succourer", "Priscilla", "Necks", "Epaenetus", "Mary",
         "Andronicus", "Amplias", "Urbane", "Apelles", "Herodion", "Tryphena",
         "Rufus", "Asyncritus", "Philologus", "Holy kiss", "Divisions",
         "Deceive", "Obedience", "Satan", "Timotheus", "Tertius", "Gaius",
         "Grace", "Mystery", "Manifest", "Glory"],
}

for _ch, _words in TRACK.items():
    assert len(_words) == CH_LEN[_ch], f"Romans {_ch}: {len(_words)} words"


def draw_track(c, ch, v):
    words = TRACK[ch]
    n = len(words)
    step = (TRACK_X1 - TRACK_X0) / max(1, n - 1)
    c.line((TRACK_X0, TRACK_Y), (TRACK_X1, TRACK_Y), dim(SAND_DIM, 0.75), 1)
    for i in range(n):
        x = TRACK_X0 + i * step
        if i + 1 < v:
            c.circle(x, TRACK_Y, 3, fill=dim(SAND, 0.6))
        elif i + 1 > v:
            c.circle(x, TRACK_Y, 2.6, stroke=dim(SAND_DIM, 0.95), width=1)
    x = TRACK_X0 + (v - 1) * step
    c.circle(x, TRACK_Y, 5.5, fill=HL)
    c.pulse_ellipse(x, TRACK_Y, 11, 11, dim(HL, 0.85), width=1.6, first=True)
    c.text((x, TRACK_Y + 18), str(v), 11, TEXT_DIM, "mm")
    lx = min(max(x, TRACK_X0 + 120), TRACK_X1 - 120)
    c.text((lx, WORD_Y), words[v - 1], 23, HL, "mm", bold=True)


# ---------------------------------------------------------------------------
# Emblems — one per stop, drawn small in the rail and large on the arc.
# Each fits a box of side `s` centred on (cx, cy).
# ---------------------------------------------------------------------------

def _lw(s):
    return max(1.3, s * 0.05)


def gl_letter(c, cx, cy, s, col):
    w, h, lw = s * 0.84, s * 0.60, _lw(s)
    c.rect(cx - w / 2, cy - h / 2, w, h, stroke=col, width=lw, rx=s * 0.05)
    c.polyline([(cx - w / 2, cy - h / 2), (cx, cy + h * 0.14),
                (cx + w / 2, cy - h / 2)], col, lw)


def gl_dock(c, cx, cy, s, col):
    lw = _lw(s)
    for dx in (-0.28, 0.0, 0.28):
        x = cx + dx * s
        c.circle(x, cy - s * 0.22, s * 0.085, stroke=col, width=lw)
        c.line((x, cy - s * 0.11), (x, cy + s * 0.22), col, lw)
    c.line((cx - s * 0.44, cy + s * 0.04), (cx + s * 0.44, cy + s * 0.04),
           col, lw * 1.25)


def gl_scale(c, cx, cy, s, col):
    lw = _lw(s)
    c.line((cx, cy - s * 0.28), (cx, cy + s * 0.30), col, lw)
    c.line((cx - s * 0.16, cy + s * 0.30), (cx + s * 0.16, cy + s * 0.30),
           col, lw)
    c.line((cx - s * 0.40, cy - s * 0.22), (cx + s * 0.40, cy - s * 0.22),
           col, lw)
    for dx in (-0.40, 0.40):
        x = cx + dx * s
        c.line((x, cy - s * 0.22), (x, cy - s * 0.06), col, lw * 0.8)
        c.polyline([(x - s * 0.15, cy - s * 0.06), (x + s * 0.15, cy - s * 0.06),
                    (x + s * 0.09, cy + s * 0.05), (x - s * 0.09, cy + s * 0.05)],
                   col, lw, closed=True)


def gl_two(c, cx, cy, s, col):
    lw = _lw(s)
    for dx in (-0.22, 0.22):
        x = cx + dx * s
        c.circle(x, cy - s * 0.26, s * 0.085, stroke=col, width=lw)
        c.line((x, cy - s * 0.15), (x, cy + s * 0.18), col, lw)
        c.line((x - s * 0.14, cy + s * 0.26), (x + s * 0.14, cy + s * 0.26),
               col, lw)


def gl_ascent(c, cx, cy, s, col):
    lw = _lw(s)
    c.polyline([(cx - s * 0.42, cy + s * 0.30), (cx - s * 0.13, cy + s * 0.30),
                (cx - s * 0.13, cy + s * 0.06), (cx + s * 0.15, cy + s * 0.06),
                (cx + s * 0.15, cy - s * 0.18), (cx + s * 0.42, cy - s * 0.18)],
               col, lw)
    c.circle(cx + s * 0.42, cy - s * 0.32, s * 0.075, fill=col)


def gl_tree(c, cx, cy, s, col):
    lw = _lw(s)
    c.line((cx, cy + s * 0.32), (cx, cy - s * 0.04), col, lw * 1.4)
    c.line((cx - s * 0.34, cy + s * 0.32), (cx + s * 0.34, cy + s * 0.32),
           col, lw)
    for dx, dy in ((-0.26, -0.28), (0.0, -0.36), (0.26, -0.28)):
        c.line((cx, cy - s * 0.04), (cx + dx * s, cy + dy * s), col, lw)
    # the one branch broken off
    c.line((cx, cy - s * 0.04), (cx - s * 0.30, cy - s * 0.02), col, lw)
    c.line((cx - s * 0.30, cy + s * 0.06), (cx - s * 0.42, cy + s * 0.18),
           dim(col, 0.5), lw)


def gl_body(c, cx, cy, s, col):
    lw = _lw(s)
    c.circle(cx, cy - s * 0.26, s * 0.105, stroke=col, width=lw)
    c.line((cx, cy - s * 0.14), (cx, cy + s * 0.12), col, lw)
    c.line((cx - s * 0.24, cy - s * 0.02), (cx + s * 0.24, cy - s * 0.02),
           col, lw)
    c.line((cx, cy + s * 0.12), (cx - s * 0.16, cy + s * 0.34), col, lw)
    c.line((cx, cy + s * 0.12), (cx + s * 0.16, cy + s * 0.34), col, lw)


EMBLEM = {"ARC": gl_letter, "DOCK": gl_dock, "SCALE": gl_scale,
          "TWO": gl_two, "ASCENT": gl_ascent, "TREE": gl_tree,
          "BODY": gl_body}


# ---------------------------------------------------------------------------
# The rail — the whole argument, always on screen, current stop lit
# ---------------------------------------------------------------------------

def draw_rail(c, stage, first):
    row = STOP_ROW[stage]
    top = ROW0
    bot = ROW0 + (len(STOPS) - 1) * ROWH
    c.line((GLYPH_X, top), (GLYPH_X, bot), dim(SAND_DIM, 0.9), 2)

    for i, (key, label, span) in enumerate(STOPS):
        y = ROW0 + i * ROWH
        cur = (i == row)
        done = i < row
        col = HL if cur else (dim(SAND, 0.85) if done else dim(SAND_DIM, 0.95))
        c.circle(GLYPH_X, y, 21, fill=BG)
        EMBLEM[key](c, GLYPH_X, y, 34, col)
        if cur:
            c.pulse_ellipse(GLYPH_X, y, 23, 23, dim(HL, 0.8), width=1.8,
                            first=first)
        c.text((84, y - 7), label, 16 if cur else 15,
               HL if cur else (TEXT if done else TEXT_DIM), "lm", bold=cur)
        c.text((84, y + 12), span, 11.5,
               TEXT_DIM if cur else dim(TEXT_DIM, 0.7), "lm", italic=True)

    c.line((246, SY0 - 8), (246, 548), dim(SAND_DIM, 0.8), 1)


# ---------------------------------------------------------------------------
# Stage 1 — the arc (1:1-17): the letter's road to Rome runs through the
# seven emblems, so the opening frame *is* the whole argument.
# ---------------------------------------------------------------------------

ARC_PTS = [(330 + 100 * i, 420 - 38 * i + 4 * (i - 3) ** 2) for i in range(7)]


def draw_arc(c, ch, v, focus, first, pos):
    road_on, road_first = since(pos, 1, 8)
    lit_all = focus == "arc"

    if road_on:
        pts = [(300, 462)] + ARC_PTS + [(956, 196)]
        if road_first:
            c.traced(pts, dim(GOLD, 0.55), 2.4, dur="2.6s")
        else:
            c.polyline(pts, dim(GOLD, 0.55), 2.4, dash="6,7")

    for i, (key, label, _span) in enumerate(STOPS):
        x, y = ARC_PTS[i]
        col = HL if lit_all else (
            GOLD if (key == "ARC" and focus == "letter") else dim(SAND_DIM, 1.0))
        EMBLEM[key](c, x, y, 62, col)
        if lit_all:
            c.text((x, y + 46), label, 13, dim(TEXT, 0.9), "mm")

    c.circle(300, 462, 5, fill=GOLD if focus == "letter" else dim(SAND, 0.8))
    c.text((300, 486), "PAUL", 16, HL if focus == "letter" else TEXT_DIM, "mm",
           bold=focus == "letter")
    if road_on:
        c.circle(956, 196, 5, fill=GOLD if focus != "letter" else dim(SAND, 0.6))
        c.text((956, 170), "ROME", 16, HL if focus == "road" else TEXT, "mm",
               bold=focus == "road")


# ---------------------------------------------------------------------------
# Stage 2 — the dock (1:18-3:20): three defendants, each convicted in turn
# ---------------------------------------------------------------------------

DOCKS = [
    ("GENTILE", 300, (1, 18), (1, 32)),      # x, opens at, stamped at
    ("MORALIST", 536, (2, 1), (2, 16)),
    ("JEW", 772, (2, 17), (3, 8)),
]
DOCK_W, DOCK_TOP, DOCK_H = 190, 168, 212


def draw_dock(c, ch, v, focus, first, pos):
    wrath_on, wrath_first = since(pos, 1, 18)
    if wrath_on:
        for i in range(15):
            x = 300 + i * 47
            c.line((x, 104), (x, 104 + (18 if i % 2 else 26)),
                   dim(RED, 0.75), 2, linecap="round")
        c.text((SX1 - 4, 112), "WRATH", 15, dim(RED, 0.95), "rm", bold=True)

    all_guilty = focus == "all"
    for i, (name, x, opens, stamped) in enumerate(DOCKS):
        open_on, _ = since(pos, *opens)
        if not open_on:
            continue
        cur = (focus == name.lower()) or all_guilty
        c.rect(x, DOCK_TOP, DOCK_W, DOCK_H, fill=PANEL,
               stroke=dim(SAND_DIM, 1.0), width=1.5, rx=10)

        hx = x + DOCK_W / 2
        fig = dim(SAND, 0.95) if cur else dim(SAND_DIM, 1.0)
        c.circle(hx, DOCK_TOP + 70, 17, stroke=fig, width=2)
        c.polyline([(hx - 26, DOCK_TOP + 176), (hx - 18, DOCK_TOP + 100),
                    (hx + 18, DOCK_TOP + 100), (hx + 26, DOCK_TOP + 176)],
                   fig, 2)

        c.text((hx, DOCK_TOP + DOCK_H + 26), name, 17,
               HL if cur else TEXT_DIM, "mm", bold=cur)

        stamp_on, stamp_first = since(pos, *stamped)
        if stamp_on:
            sw, sh = 148, 36
            sx, sy = hx - sw / 2, DOCK_TOP + 118
            c.rect(sx, sy, sw, sh, fill=dim(RED, 0.22), stroke=dim(RED, 0.9),
                   width=2, rx=4)
            c.text((hx, sy + sh / 2), "GUILTY", 21, dim(RED, 1.0), "mm",
                   bold=True)
            if stamp_first:
                c.pulse_rect(sx, sy, sw, sh, dim(HL, 0.9), width=2.5,
                             first=True, rx=4)

        if cur and not all_guilty:
            c.pulse_rect(x - 5, DOCK_TOP - 5, DOCK_W + 10, DOCK_H + 10,
                         dim(HL, 0.85), width=2.5, first=first, rx=12)

    verdict_on, verdict_first = since(pos, 3, 10)
    if verdict_on:
        c.line((300, 438), (962, 438), dim(HL, 0.5), 1.5)
        c.text((CX, 462), "NONE RIGHTEOUS", 24, HL, "mm", bold=True)
        if verdict_first:
            c.pulse_rect(CX - 150, 444, 300, 34, dim(HL, 0.8), width=2,
                         first=True, rx=6)


# ---------------------------------------------------------------------------
# Stage 3 — the balance (3:21-4:25): the weight moves, the beam levels
# ---------------------------------------------------------------------------

PIVOT = (CX, 196)
ARM = 232
WEIGHTS = [(3, 21), (3, 22), (3, 23)]        # a block per verse: all sinned
LEDGER = [("ABRAHAM", 430, (4, 1)), ("DAVID", 631, (4, 6)),
          ("US", 832, (4, 23))]


def _pan(c, x, y, col, label, lit):
    c.line((x, PIVOT[1]), (x, y), col, 1.6)
    c.polyline([(x - 68, y), (x + 68, y), (x + 52, y + 16), (x - 52, y + 16)],
               col, 2, closed=True)
    c.text((x, y + 40), label, 16, HL if lit else TEXT_DIM, "mm", bold=lit)


def draw_scale(c, ch, v, focus, first, pos):
    level, level_first = since(pos, 3, 24)
    ang = math.radians(0 if level else 13)
    lx, ly = PIVOT[0] - ARM * math.cos(ang), PIVOT[1] + ARM * math.sin(ang)
    rx, ry = PIVOT[0] + ARM * math.cos(ang), PIVOT[1] - ARM * math.sin(ang)

    c.line((PIVOT[0], PIVOT[1]), (PIVOT[0], 424), dim(SAND, 0.9), 3)
    c.polyline([(PIVOT[0] - 46, 424), (PIVOT[0] + 46, 424),
                (PIVOT[0] + 34, 408), (PIVOT[0] - 34, 408)],
               dim(SAND, 0.9), 2, closed=True)
    c.line((lx, ly), (rx, ry), dim(SAND, 1.0), 3.5)
    c.circle(PIVOT[0], PIVOT[1], 7, fill=dim(SAND, 1.0))

    _pan(c, lx, ly + 96, dim(SAND, 0.9), "LAW", focus == "weight")
    _pan(c, rx, ry + 96, dim(GOLD, 0.95) if level else dim(SAND_DIM, 1.0),
         "FAITH", level)

    # the debt: a block per "all have sinned" verse, stacked on the law pan
    for i, at in enumerate(WEIGHTS):
        on, block_first = since(pos, *at)
        if not on:
            continue
        by = ly + 96 - 24 - i * 26
        c.rect(lx - 44, by, 88, 24, fill=dim(GRAY, 0.5), stroke=dim(SAND, 0.9),
               width=1.5, rx=3)
        if block_first:
            c.pulse_rect(lx - 44, by, 88, 24, dim(HL, 0.9), width=2,
                         first=True, rx=3)

    if level:
        gy = ry + 96 - 30
        c.rect(rx - 56, gy, 112, 30, fill=dim(GOLD, 0.32), stroke=GOLD,
               width=2, rx=4)
        c.text((rx, gy + 15), "GRACE", 18, HL, "mm", bold=True)
        if level_first:
            c.pulse_rect(rx - 56, gy, 112, 30, dim(HL, 0.9), width=2.5,
                         first=True, rx=4)

    boast_on, boast_first = since(pos, 3, 27)
    if boast_on:
        bx, by = lx - 52, ly + 20
        c.rect(bx, by, 104, 28, stroke=dim(SAND_DIM, 1.0), width=1.5, rx=3)
        c.text((bx + 52, by + 14), "BOASTING", 14, dim(TEXT_DIM, 0.95), "mm")
        c.line((bx, by + 28), (bx + 104, by), dim(RED, 0.85), 2)
        if boast_first:
            c.pulse_rect(bx, by, 104, 28, dim(RED, 0.85), width=2, first=True,
                         rx=3)

    # chapter 4: the account is credited to named men
    if pos >= P(4, 1):
        c.line((394, 462), (868, 462), dim(SAND_DIM, 0.9), 1.5)
        for name, x, at in LEDGER:
            on, name_first = since(pos, *at)
            if not on:
                continue
            lit = focus == name.lower() or (focus in ("seal", "promise")
                                            and name == "ABRAHAM")
            c.circle(x, 462, 6 if lit else 4,
                     fill=HL if lit else dim(SAND, 0.8))
            c.text((x, 440), name, 17 if lit else 15,
                   HL if lit else TEXT_DIM, "mm", bold=lit)
            if name_first:
                c.pulse_ellipse(x, 462, 15, 15, dim(HL, 0.85), width=2,
                                first=True)


# ---------------------------------------------------------------------------
# Stage 4 — the two men (chapter 5)
# ---------------------------------------------------------------------------

COL_X = {"adam": 452, "christ": 806}
CHIPS = [("PEACE", (5, 1)), ("ACCESS", (5, 2)), ("HOPE", (5, 4)),
         ("LOVE", (5, 5))]


def _column(c, x, name, col, base_n, lit, first):
    c.text((x, 138), name, 22, HL if lit else TEXT_DIM, "mm", bold=lit)
    c.circle(x, 186, 23, stroke=col, width=2.5)
    c.line((x, 209), (x, 344), col, 6)
    c.polyline([(x - 9, 332), (x, 346), (x + 9, 332)], col, 3)
    span = 22 * (base_n - 1)
    for i in range(base_n):
        fx = x - span / 2 + i * 22
        c.circle(fx, 380, 7, fill=col if lit else dim(col, 0.5))
    if lit and first:
        c.pulse_ellipse(x, 186, 32, 32, dim(HL, 0.85), width=2, first=True)


def draw_two(c, ch, v, focus, first, pos):
    ladder = focus == "ladder"
    adam_lit = focus in ("adam", "both", "abound")
    christ_lit = focus in ("both", "abound")

    base_n = 9
    if pos >= P(5, 17):
        base_n = 11
    if pos >= P(5, 20):
        base_n = 13

    _column(c, COL_X["adam"], "ADAM",
            dim(RED, 0.9) if adam_lit else dim(SAND_DIM, 1.0), 9,
            adam_lit, first and focus == "adam")
    c.text((COL_X["adam"], 412), "DEATH", 16,
           dim(RED, 0.95) if adam_lit else TEXT_DIM, "mm", bold=adam_lit)

    _column(c, COL_X["christ"], "CHRIST",
            GOLD if christ_lit else dim(SAND_DIM, 1.0),
            base_n if christ_lit else 9, christ_lit,
            first and focus == "both")
    c.text((COL_X["christ"], 412), "LIFE", 16,
           HL if christ_lit else TEXT_DIM, "mm", bold=christ_lit)

    # the ladder of 5:1-11, standing between the two men
    for i, (word, at) in enumerate(CHIPS):
        on, chip_first = since(pos, *at)
        if not on:
            continue
        y = 372 - i * 52
        col = HL if ladder else dim(SAND_DIM, 1.0)
        c.rect(CX - 66, y - 17, 132, 34,
               fill=dim(GOLD, 0.20) if ladder else None,
               stroke=col, width=1.8, rx=17)
        c.text((CX, y), word, 16, HL if ladder else TEXT_DIM, "mm",
               bold=ladder)
        if i:
            c.line((CX, y + 17), (CX, y + 35), col, 1.5)
        if chip_first:
            c.pulse_rect(CX - 66, y - 17, 132, 34, dim(HL, 0.9), width=2.2,
                         first=True, rx=17)


# ---------------------------------------------------------------------------
# Stage 5 — the ascent (6-8): out of the grave, through the divided man,
# up to the chain that cannot be broken
# ---------------------------------------------------------------------------

GROUND_Y = 412

# (x, y, first verse of the station)
ASCENT = [
    (306, 452, (6, 1)), (366, 436, (6, 4)), (420, 398, (6, 8)),
    (474, 374, (6, 12)), (528, 356, (6, 20)), (578, 342, (7, 1)),
    (612, 322, (7, 7)), (648, 350, (7, 14)), (676, 312, (7, 18)),
    (706, 344, (7, 21)), (734, 306, (7, 25)),
    (768, 278, (8, 1)), (806, 254, (8, 12)), (842, 232, (8, 18)),
]
CHAIN = [(872, 208, (8, 28)), (896, 192, (8, 29)), (920, 176, (8, 29)),
         (944, 160, (8, 30)), (966, 144, (8, 30))]


def draw_ascent(c, ch, v, focus, first, pos):
    c.line((290, GROUND_Y), (980, GROUND_Y), dim(SAND_DIM, 0.9), 1.5,
           dash="7,7")
    c.text((296, GROUND_Y + 30), "SIN", 15,
           dim(RED, 0.9) if focus == "grave" else TEXT_DIM, "lm",
           bold=focus == "grave")

    shown = [(x, y) for x, y, at in ASCENT if pos >= P(*at)]
    live = [(x, y, at) for x, y, at in ASCENT if pos >= P(*at)]
    if len(shown) > 1:
        newest = live[-1][2]
        if pos == P(*newest) and len(shown) > 1:
            c.polyline(shown[:-1], dim(GOLD, 0.75), 3)
            c.traced(shown[-2:], GOLD, 3, dur="1.4s")
        else:
            c.polyline(shown, dim(GOLD, 0.75), 3)

    for i, (x, y, at) in enumerate(ASCENT):
        if pos < P(*at):
            continue
        cur = live[-1][:2] == (x, y)
        c.circle(x, y, 5 if cur else 3.5,
                 fill=HL if cur else dim(GOLD, 0.8))
        if cur:
            c.pulse_ellipse(x, y, 12, 12, dim(HL, 0.85), width=1.8,
                            first=first)

    # chapter 7: the war in the members, drawn where the path frays
    if ch == 7 and focus == "divided":
        c.polyline([(660, 258), (660, 292)], dim(SAND, 0.9), 2)
        c.polyline([(654, 268), (660, 256), (666, 268)], dim(SAND, 0.9), 2)
        c.text((660, 240), "MIND", 14, dim(TEXT, 0.95), "mm")
        c.polyline([(700, 386), (700, 420)], dim(RED, 0.85), 2)
        c.polyline([(694, 410), (700, 422), (706, 410)], dim(RED, 0.85), 2)
        c.text((700, 442), "FLESH", 14, dim(RED, 0.95), "mm")

    if pos >= P(8, 1):
        c.text((762, 306), "SPIRIT", 16,
               HL if focus == "spirit" else dim(TEXT_DIM, 0.95), "mm",
               bold=focus == "spirit")

    # 8:29-30 — the five links
    links = [(x, y) for x, y, at in CHAIN if pos >= P(*at)]
    for i, (x, y) in enumerate(links):
        newest = i == len(links) - 1 and pos == P(*CHAIN[i][2])
        c.circle(x, y, 13, stroke=GOLD if not newest else HL, width=3)
        if newest:
            c.pulse_ellipse(x, y, 18, 18, dim(HL, 0.9), width=2, first=True)
    if links:
        c.text((966, 112), "GLORY", 16,
               HL if focus in ("chain", "hold") else TEXT_DIM, "mm",
               bold=focus in ("chain", "hold"))

    # 8:31-39 — what strikes the chain and does not break it
    if focus == "hold":
        for i, (ax, ay) in enumerate([(840, 300), (880, 320), (920, 300),
                                      (952, 270)]):
            tx, ty = ax + 14, ay - 46
            c.line((ax, ay), (tx, ty), dim(RED, 0.55), 2)
            c.circle(tx, ty, 3, fill=dim(RED, 0.55))


# ---------------------------------------------------------------------------
# Stage 6 — the olive tree (9-11)
# ---------------------------------------------------------------------------

# The tree sits high in the stage: everything below y=474 belongs to the bead
# track's word, which slides horizontally and would collide with any label
# parked down there.
TRUNK_X, ROOT_Y, FORK_Y = 700, 414, 278

# natural branches: (tip x, tip y, broken?, verse it breaks)
NATURAL = [
    (520, 214, True), (566, 168, False), (628, 140, True),
    (700, 128, False), (770, 146, True), (820, 190, False),
]
WILD_TIPS = [(884, 226), (916, 268), (930, 318)]
FATHERS = [("ABRAHAM", 596, (9, 6)), ("ISAAC", 700, (9, 7)),
           ("JACOB", 804, (9, 10))]
CALL_STEPS = [(858, 350), (886, 366), (912, 380), (936, 392), (958, 402)]


def _leaves(c, x, y, col, r=9):
    for dx, dy in ((-10, 2), (0, -8), (10, 2)):
        c.ellipse(x + dx, y + dy, r, r * 0.55, fill=col)


def draw_tree(c, ch, v, focus, first, pos):
    graft_on = pos >= P(11, 17)          # branches broken off, wild ones in
    restored = pos >= P(11, 26)          # "and so all Israel shall be saved"

    c.ellipse(TRUNK_X, ROOT_Y, 136, 20, fill=dim(BROWN, 0.45),
              stroke=dim(BROWN, 0.9), width=2)
    c.text((TRUNK_X, ROOT_Y + 30), "ROOT", 16,
           HL if focus == "root" else TEXT_DIM, "mm", bold=focus == "root")
    c.polyline([(TRUNK_X - 11, ROOT_Y), (TRUNK_X - 8, FORK_Y),
                (TRUNK_X + 8, FORK_Y), (TRUNK_X + 11, ROOT_Y)],
               dim(BROWN, 0.9), 2, closed=True, fill=dim(BROWN, 0.55))

    for tx, ty, breaks in NATURAL:
        mx, my = (TRUNK_X + tx) / 2, (FORK_Y + ty) / 2 - 18
        gone = breaks and graft_on and not restored
        if gone:
            # a stub left on the trunk, the branch itself fallen away below
            c.polyline([(TRUNK_X, FORK_Y), ((TRUNK_X + mx) / 2,
                                            (FORK_Y + my) / 2)],
                       dim(OLIVE, 0.45), 4)
            c.polyline([(mx, my + 60), (tx - 12, ty + 96)],
                       dim(OLIVE, 0.35), 3)
        else:
            grafted_back = breaks and restored
            c.polyline([(TRUNK_X, FORK_Y), (mx, my), (tx, ty)], OLIVE, 4)
            _leaves(c, tx, ty, dim(OLIVE, 0.62 if grafted_back else 0.9))
    c.text((470, 130), "ISRAEL", 17,
           HL if focus in ("stumble", "remnant", "restore") else TEXT_DIM,
           "mm", bold=focus in ("stumble", "remnant", "restore"))

    if graft_on:
        for i, (tx, ty) in enumerate(WILD_TIPS):
            on, wild_first = since(pos, 11, 17 + i)
            if not on:
                continue
            pts = [(TRUNK_X, FORK_Y + 18 + i * 12), ((TRUNK_X + tx) / 2 + 20,
                                                     (FORK_Y + ty) / 2 + 10),
                   (tx, ty)]
            if wild_first:
                c.traced(pts, WILD, 4, dur="1.6s")
            else:
                c.polyline(pts, WILD, 4)
            _leaves(c, tx, ty, dim(WILD, 0.9))
            c.rect(TRUNK_X - 14, FORK_Y + 12 + i * 12, 28, 8,
                   fill=dim(GOLD, 0.55), rx=3)
        c.text((944, 156), "GENTILES", 17,
               HL if focus == "graft" else TEXT_DIM, "mm",
               bold=focus == "graft")

    # chapter 9: the promise runs through named sons
    if ch == 9 and pos >= P(9, 6):
        for name, x, at in FATHERS:
            on, name_first = since(pos, *at)
            if not on:
                continue
            c.circle(x, ROOT_Y, 6, fill=HL if focus == "election" else
                     dim(SAND, 0.85))
            c.text((x, ROOT_Y - 22), name, 14,
                   HL if focus == "election" else TEXT_DIM, "mm")
            if name_first:
                c.pulse_ellipse(x, ROOT_Y, 15, 15, dim(HL, 0.85), width=2,
                                first=True)
        for label, x, at in (("ISHMAEL", 560, (9, 8)), ("ESAU", 856, (9, 13))):
            if pos >= P(*at):
                c.line((x, ROOT_Y + 8), (x - 16, ROOT_Y + 28),
                       dim(SAND_DIM, 1.0), 2)
                c.text((x - 20, ROOT_Y + 42), label, 12, dim(TEXT_DIM, 0.9),
                       "mm")

    # 11:4 — the reserved remnant, a number, on Israel's side of the tree
    if pos >= P(11, 4):
        c.rect(454, 430, 132, 32, stroke=dim(GOLD, 0.85), width=1.8,
               rx=16, fill=dim(GOLD, 0.18))
        c.text((520, 446), "7000", 19,
               HL if focus == "remnant" else TEXT, "mm", bold=True)

    # chapter 10: the word sent out to the nations
    if ch == 10:
        c.polyline([(TRUNK_X + 60, 284), (800, 320), (846, 344)],
                   dim(GOLD, 0.7), 2.5, dash="6,6")
        steps = CALL_STEPS if focus == "sent" else []
        for i, (x, y) in enumerate(steps):
            at = (10, 14 + i)
            if pos < P(*at):
                c.circle(x, y, 3.5, stroke=dim(SAND_DIM, 1.0), width=1.5)
                continue
            cur = pos == P(*at)
            c.circle(x, y, 5.5 if cur else 4, fill=HL if cur else
                     dim(GOLD, 0.85))

    if focus == "stumble" and pos >= P(9, 32):
        c.polygon([(500, 444), (534, 428), (560, 448), (524, 462)],
                  fill=dim(GRAY, 0.55), stroke=dim(SAND, 0.9), width=2)


# ---------------------------------------------------------------------------
# Stage 7 — one body (12-16)
# ---------------------------------------------------------------------------

BODY_HEAD = (CX, 178)
BODY_OUTLINE = [
    (CX - 26, 224), (CX - 52, 232), (CX - 112, 316), (CX - 126, 330),
    (CX - 108, 342), (CX - 44, 268), (CX - 40, 356), (CX - 52, 452),
    (CX - 30, 458), (CX - 8, 372), (CX + 8, 372), (CX + 30, 458),
    (CX + 52, 452), (CX + 40, 356), (CX + 44, 268), (CX + 108, 342),
    (CX + 126, 330), (CX + 112, 316), (CX + 52, 232), (CX + 26, 224),
]
# the seven gifts of 12:6-8, as places on the body
GIFTS = [(CX, 178, (12, 6)), (CX - 52, 250, (12, 7)), (CX + 52, 250, (12, 7)),
         (CX, 286, (12, 8)), (CX - 118, 324, (12, 8)),
         (CX + 118, 324, (12, 8)), (CX, 350, (12, 8))]
# chapter 16: how many are greeted by name in each verse
NAMES_AT = {1: 1, 3: 2, 5: 1, 6: 1, 7: 2, 8: 1, 9: 2, 10: 2, 11: 2, 12: 3,
            13: 2, 14: 5, 15: 5, 21: 4, 22: 1, 23: 3}
NAME_TOTAL = sum(NAMES_AT.values())
JOURNEY = [("JERUSALEM", 400, (15, 19)), ("ROME", 640, (15, 23)),
           ("SPAIN", 900, (15, 24))]


def _sample(pts, n):
    """n points spread evenly round the closed outline — the body drawn as
    the people who make it up (chapter 16)."""
    ring = pts + pts[:1]
    segs = [(a, b, math.dist(a, b)) for a, b in zip(ring, ring[1:])]
    total = sum(s[2] for s in segs)
    out, target, walked, i = [], 0.0, 0.0, 0
    for k in range(n):
        target = total * k / n
        while i < len(segs) - 1 and walked + segs[i][2] < target:
            walked += segs[i][2]
            i += 1
        (ax, ay), (bx, by), ln = segs[i]
        t = 0 if ln == 0 else (target - walked) / ln
        out.append((ax + (bx - ax) * t, ay + (by - ay) * t))
    return out


_NAME_DOTS = None


def name_dots():
    global _NAME_DOTS
    if _NAME_DOTS is None:
        _NAME_DOTS = _sample(BODY_OUTLINE, NAME_TOTAL)
    return _NAME_DOTS


def draw_body(c, ch, v, focus, first, pos):
    names = focus == "names"
    body_col = dim(SAND, 0.85) if not names else dim(SAND_DIM, 1.0)

    c.circle(*BODY_HEAD, 34, stroke=body_col, width=2.5)
    c.polyline(BODY_OUTLINE, body_col, 2.5, closed=True)

    if ch == 12:
        for i, (x, y, at) in enumerate(GIFTS):
            on, gift_first = since(pos, *at)
            if not on:
                continue
            c.circle(x, y, 7, fill=dim(GOLD, 0.9))
            if gift_first:
                c.pulse_ellipse(x, y, 16, 16, dim(HL, 0.85), width=2,
                                first=True)

    if ch == 13:
        if focus == "powers":
            c.polyline([(CX - 92, 128), (CX - 92, 104), (CX - 46, 104),
                        (CX - 46, 118), (CX + 46, 118), (CX + 46, 104),
                        (CX + 92, 104), (CX + 92, 128)], GOLD, 3)
            c.text((CX, 88), "POWERS", 17, HL, "mm", bold=True)
            c.line((CX + 168, 214), (CX + 168, 300), dim(SAND, 0.95), 4)
            c.line((CX + 152, 232), (CX + 184, 232), dim(SAND, 0.95), 3)
        elif pos >= P(13, 12):
            c.polyline([(CX - 56, 250), (CX + 56, 250), (CX + 56, 330),
                        (CX, 372), (CX - 56, 330)], GOLD, 3)
            c.text((CX, 300), "ARMOUR", 16, HL, "mm", bold=True)

    if focus == "weak":
        for label, x, lit in (("WEAK", 380, ch == 14), ("STRONG", 882, ch == 15)):
            col = HL if lit else dim(SAND_DIM, 1.0)
            c.circle(x, 262, 16, stroke=col, width=2.5)
            c.polyline([(x - 22, 356), (x - 15, 288), (x + 15, 288),
                        (x + 22, 356)], col, 2.5)
            c.text((x, 388), label, 16, HL if lit else TEXT_DIM, "mm",
                   bold=lit)
        c.line((408, 300), (CX - 128, 300), dim(GOLD, 0.6), 2, dash="6,6")
        c.line((CX + 128, 300), (854, 300), dim(GOLD, 0.6), 2, dash="6,6")

    if focus == "journey":
        c.line((JOURNEY[0][1], 128), (JOURNEY[-1][1], 128),
               dim(SAND_DIM, 1.0), 2, dash="6,6")
        for label, x, at in JOURNEY:
            on, j_first = since(pos, *at)
            c.circle(x, 128, 6 if on else 4,
                     fill=HL if on else None,
                     stroke=None if on else dim(SAND_DIM, 1.0), width=1.5)
            c.text((x, 104), label, 15, HL if on else TEXT_DIM, "mm", bold=on)
            if j_first:
                c.pulse_ellipse(x, 128, 15, 15, dim(HL, 0.85), width=2,
                                first=True)

    if names:
        dots = name_dots()
        lit = sum(n for verse, n in NAMES_AT.items() if verse <= v)
        for i, (x, y) in enumerate(dots):
            if i < lit:
                c.circle(x, y, 6, fill=dim(GOLD, 0.95))
            else:
                c.circle(x, y, 4, stroke=dim(SAND_DIM, 1.0), width=1.4)
        fresh = NAMES_AT.get(v, 0)
        for i in range(lit - fresh, lit):
            x, y = dots[i]
            c.pulse_ellipse(x, y, 14, 14, dim(HL, 0.9), width=2, first=True)


STAGES = {"ARC": draw_arc, "DOCK": draw_dock, "SCALE": draw_scale,
          "TWO": draw_two, "ASCENT": draw_ascent, "TREE": draw_tree,
          "BODY": draw_body}


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

def render(ch, v):
    stage, focus, first = beat(ch, v)
    pos = P(ch, v)

    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 24), f"Romans {ch}", 23, TEXT, "la", bold=True)
    draw_rail(c, stage, first)
    STAGES[stage](c, ch, v, focus, first, pos)
    draw_track(c, ch, v)
    return c


def main():
    total = count = 0
    for ch in range(1, 17):
        for v in range(1, CH_LEN[ch] + 1):
            out = out_path(BOOK, ch, f"{BOOK}_{ch}_{v}.svg")
            render(ch, v).save(out)
            total += os.path.getsize(out)
            count += 1
    print(f"Romans: {count} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
