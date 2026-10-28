"""The Kings and prophets reference page: Judah and Israel as two lanes of
reigns from Saul to the exile, on Ussher's years with Thiele's beside them,
the prophets beside the kings the text names with them, the foreign kings
at the regnal years the text dates them by, and the judges before.

Writes web/visuals/reference/Kings_and_prophets.svg, its sidecar
Kings_and_prophets.json and the viewer page Kings_and_prophets.html
(reference_viewer.page). The web app's Reference list opens it
(web/js/app.js REFERENCES). The data is kings.py and prophets.py.

The sheet, time running down:

- **The year line** is Ussher's, the house count, and it stretches where
  reigns are short so every reign's bar can carry its name: Zimri's seven
  days get as much room as a year. The rail on the left gives the year.
- **The reigns.** The united kingdom across the middle, then Judah on the
  left and Israel on the right. A bar is coloured by the text's verdict on
  the king (right, right but, evil, none), and carries his Ussher years and
  Thiele's. A reign that overlaps another (Jehoram beside Jehoshaphat,
  Tibni against Omri) stands in the half of its column; Ussher's interregna
  in Israel are hatched.
- **The prophets** beside their kingdom: a writing prophet from the first
  to the last king his book's opening verse names, a narrative prophet
  over the reigns of the kings the histories set him beside. The undated
  books are listed at the foot.
- **The nations** between the two kingdoms: each foreign king at the
  regnal year the text dates him by (a filled mark), or in the middle of
  the reign when the text gives no year (a hollow one).
- **The judges** in a strip above, in order, with the years the text gives
  each. Not on the year line: their sum exceeds 1 Kings 6:1's 480 years.

A card gives a king's years in both counts, the text's length, accession,
father and mother, verdict, end and burial, each with its verse; his
passages in Kings and Chronicles; the prophets and events beside him; and
a link to his box on the OT family tree.

    .venv\\Scripts\\python.exe generate_kings_reference.py
"""

import json
import math
import os
import re

import kings as K
import prophets as PR
import reference_viewer
import verse_refs
from books import BOOK_NAMES, chapters_in
from config import VISUALS_DIR
from generate_tabernacle import BG, GOLD, SAND, SAND_DIM, TEXT, TEXT_DIM
from svg_map_camera import ink
from svg_surface import SvgCanvas, _fmt, _rgb

OUT_DIR = os.path.join(VISUALS_DIR, "reference")
STEM = "Kings_and_prophets"
TITLE = "Kings and prophets"

# -- the year line -----------------------------------------------------------
TOP_BC, BOTTOM_BC = 1100, 495            # to Haggai and Zechariah, 520
PPY = 9                      # px a year where nothing is crowded
MINBAR = 48                  # the least a reign's bar is drawn, to carry its name

# -- the columns (x) -----------------------------------------------------------
RAIL = (40, 190)
JP = (210, 600)              # Judah's prophets
JK = (620, 930)              # Judah's kings
NA = (950, 1590)             # the nations: Judah's dealings left, Israel's right
IK = (1610, 1920)            # Israel's kings
IP = (1940, 2330)            # Israel's prophets
W = 2370
PLANE = 30                   # a prophet's lane

VERDICT_FILL = {"right": (96, 80, 36), "right, but": (72, 64, 42),
                "evil": (66, 34, 42), "none stated": (46, 46, 56)}
REALM_LINE = {"judah": (196, 160, 82), "israel": (104, 138, 182), "united": (150, 122, 176)}
THIELE_COL = (128, 170, 196)
EVENT_COL = (200, 150, 110)
HATCH = (90, 90, 104)


def P(*a):
    return a


# ---------------------------------------------------------------------------
# Years
# ---------------------------------------------------------------------------

def short_years(length):
    """How long a reign was in years, from the text's words (for the bar's
    least height only)."""
    t = (length or "").lower()
    if "day" in t:
        return 7 / 365
    if "month" in t:
        m = re.search(r"(\w+) months?", t)
        n = {"a": 1, "one": 1, "three": 3, "six": 6}.get(m.group(1), 3) if m else 3
        return n / 12
    return 1.0


def spans():
    """{key: (top_bc, bottom_bc)} for each reign, in fractional Ussher years:
    a reign that begins and ends in one year runs for its stated months or
    days, and the next reign of its realm begins where it ends."""
    out = {}
    for realm in ("united", "judah", "israel"):
        rs = sorted([(k, r) for k, r in K.REIGNS.items() if r.realm == realm],
                    key=lambda x: x[1].order)
        prev_end = None
        for k, r in rs:
            a, e = r.ussher
            if prev_end is not None and a == math.ceil(prev_end) and prev_end < a:
                a = prev_end                 # Tibni and Omri, after Zimri's seven days
            if e >= a:
                e = a - short_years(r.length)
            out[k] = (a, e)
            if k not in ("tibni", "ishbosheth"):
                prev_end = e
    return out


SPANS = spans()


def axis():
    """A monotone map BC year -> y: PPY px a year, stretched so each reign's
    bar is at least MINBAR tall."""
    pts = {TOP_BC, BOTTOM_BC}
    for a, e in SPANS.values():
        pts |= {a, e}
    for _r, a, e, _w in K.INTERREGNA:
        pts |= {a, e}
    pts = sorted(pts, reverse=True)
    ys, y = {pts[0]: 0.0}, 0.0
    bars = set(SPANS.values())
    for p0, p1 in zip(pts, pts[1:]):
        gap = (p0 - p1) * PPY
        if (p0, p1) in bars:
            gap = max(gap, MINBAR)
        y += gap
        ys[p1] = y
    return pts, ys


PTS, YS = axis()
Y0 = 560                     # the year line's top on the sheet, below the judges


def Y(bc):
    """The y of a BC year (between two known points, linearly)."""
    if bc in YS:
        return Y0 + YS[bc]
    for p0, p1 in zip(PTS, PTS[1:]):
        if p0 >= bc >= p1:
            f = (p0 - bc) / (p0 - p1)
            return Y0 + YS[p0] + f * (YS[p1] - YS[p0])
    return Y0 + (YS[PTS[-1]] if bc < PTS[-1] else 0)


H = round(Y(BOTTOM_BC) + 200)


def regnal(key, year, chron="ussher"):
    """The BC year of a king's nth regnal year in a count."""
    r = K.REIGNS[key]
    a = (r.ussher if chron == "ussher" else r.thiele)[0]
    return a - (year - 1)


# ---------------------------------------------------------------------------
# Matching names to reigns
# ---------------------------------------------------------------------------

REALM_WORD = {"judah": "judah", "israel": "israel", "united israel": "united"}


def find_king(text):
    """'Uzziah (Judah)', 'Jeroboam son of Joash (Israel)' -> the reign's key,
    or None for a foreign king."""
    m = re.match(r"\s*(.+?)\s*\((.+)\)\s*$", text or "")
    if not m:
        return None
    who, realm = m.group(1), m.group(2).strip().lower()
    realms = {"judah": ("judah",), "israel": ("israel", "united"),
              "united israel": ("united",)}.get(realm)
    if not realms:
        return None
    name, father = (who.split(" son of ") + [""])[:2]
    name = name.strip()
    # a king's own name first: Ahaziah of Judah is also called Jehoahaz
    hits = [k for k, r in K.REIGNS.items() if r.realm in realms and r.name == name] or \
        [k for k, r in K.REIGNS.items() if r.realm in realms and name in r.aka]
    if len(hits) > 1 and father:
        hits = [k for k in hits if father.strip() in K.REIGNS[k].father]
    if len(hits) > 1:
        # the namesakes of one realm (Jeroboam): the first, unless the father says
        hits = sorted(hits, key=lambda k: K.REIGNS[k].order)
    return hits[0] if hits else None


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def text(c, xy, s, size, fill, anchor="lm", bold=False, italic=False, spacing=0,
         opacity=1.0):
    ta = {"l": "start", "m": "middle", "r": "end"}[anchor[0]]
    db = {"a": "text-before-edge", "m": "central", "d": "text-after-edge",
          "s": "alphabetic"}[anchor[1]]
    a = [f'x="{_fmt(xy[0])}"', f'y="{_fmt(xy[1])}"', f'font-size="{_fmt(size)}"',
         f'text-anchor="{ta}"', f'dominant-baseline="{db}"', f'fill="{_rgb(fill)}"']
    if bold:
        a.append('font-weight="bold"')
    if italic:
        a.append('font-style="italic"')
    if spacing:
        a.append(f'letter-spacing="{_fmt(spacing)}"')
    if opacity < 1:
        a.append(f'fill-opacity="{opacity:.2f}"')
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    c._emit(f"<text {' '.join(a)}>{s}</text>")


def width(s, size, bold=False, italic=False):
    x0, _y0, x1, _y1 = ink(s, size, bold, italic, "lm")
    return x1 - x0


def fit(s, size, room, bold=False, italic=False):
    """The text, shortened with an ellipsis if it is wider than room."""
    if width(s, size, bold, italic) <= room:
        return s
    while s and width(s + "…", size, bold, italic) > room:
        s = s[:-1]
    return s.rstrip() + "…"


def yrs(a, b):
    a, b = round(a), round(b)
    return f"{a}" if a == b else f"{a}–{b}"


# ---------------------------------------------------------------------------
# The sheet
# ---------------------------------------------------------------------------

def column(realm):
    return {"judah": JK, "israel": IK, "united": (JK[0], IK[1])}[realm]


def overlaps():
    """Reigns that overlap another of their realm in Ussher's count, drawn in
    the right half of the column."""
    # the rival claimants stand beside the king, whatever their dates
    half = {"tibni", "ishbosheth"}
    for realm in ("judah", "israel"):
        rs = sorted([(k, SPANS[k]) for k, r in K.REIGNS.items()
                     if r.realm == realm and k not in half],
                    key=lambda x: (-x[1][0], K.REIGNS[x[0]].order))
        for i, (k, (a, e)) in enumerate(rs):
            for k2, (a2, e2) in rs[:i]:
                if k2 not in half and a < a2 and e2 < a - 0.01:
                    half.add(k)
                    break
    return half


HALF = overlaps()


def bar_box(key):
    r = K.REIGNS[key]
    x0, x1 = column(r.realm)
    if r.realm == "united":
        x0, x1 = (JK[0], IK[1]) if key != "ishbosheth" else (IK[0], IK[1])
    elif key in HALF:
        x0 = (x0 + x1) / 2
    a, e = SPANS[key]
    return (x0, Y(a), x1, Y(e))


def draw_rail(c):
    x0, x1 = RAIL
    for y in range(TOP_BC, BOTTOM_BC - 1, -10):
        yy = Y(y)
        big = y % 50 == 0
        c.line((x1 - (22 if big else 10), yy), (x1, yy), SAND if big else SAND_DIM, 2 if big else 1)
        if big:
            text(c, (x1 - 30, yy), f"{y} BC", 22, TEXT_DIM, "rm")
            c.line((x1 + 10, yy), (IP[1], yy), (40, 40, 52), 1)
    c.line((x1, Y(TOP_BC)), (x1, Y(BOTTOM_BC)), SAND, 2)
    text(c, ((x0 + x1) / 2, Y0 - 40), "Ussher", 22, TEXT_DIM, "mm", italic=True)


LANDMARKS = [(975, "THE KINGDOM DIVIDED"), (721, "SAMARIA FALLS"),
             (588, "JERUSALEM FALLS"), (536, "THE RETURN UNDER CYRUS")]


def draw_landmarks(c, words):
    """The rules, under the bars, or their words, over everything at the
    right-hand end, clear of the nations' names."""
    for bc, label in LANDMARKS:
        y = Y(bc)
        if words:
            text(c, (IP[1] - 10, y - 8), label, 22, GOLD, "rd", bold=True, spacing=3)
        else:
            c.line((RAIL[1], y), (IP[1], y), (150, 120, 70), 3, dash="10 8")


def draw_heads(c):
    y = Y0 - 40
    for (x0, x1), name, col in ((JP, "PROPHETS TO JUDAH", REALM_LINE["judah"]),
                                (JK, "JUDAH", REALM_LINE["judah"]),
                                (NA, "THE NATIONS", EVENT_COL),
                                (IK, "ISRAEL", REALM_LINE["israel"]),
                                (IP, "PROPHETS TO ISRAEL", REALM_LINE["israel"])):
        big = name in ("JUDAH", "ISRAEL")
        text(c, ((x0 + x1) / 2, y), name, 40 if big else 24, col, "mm", bold=True,
             spacing=6 if big else 3)
    text(c, ((JK[0] + IK[1]) / 2, Y(1095) - 24), "THE UNITED KINGDOM", 30,
         REALM_LINE["united"], "md", bold=True, spacing=5)


def draw_interregna(c):
    for realm, a, e, _why in K.INTERREGNA:
        x0, x1 = column(realm)
        y0, y1 = Y(a), Y(e)
        c.rect(x0, y0, x1 - x0, y1 - y0, fill=(28, 28, 36), stroke=HATCH, width=1.5)
        for i in range(int((x1 - x0 + y1 - y0) / 18) + 1):
            d = i * 18
            p0 = (x0 + max(0, d - (y1 - y0)), y0 + min(d, y1 - y0))
            p1 = (x0 + min(d, x1 - x0), y0 + max(0, d - (x1 - x0)))
            c.line(p0, p1, HATCH, 1.5)
        text(c, ((x0 + x1) / 2, (y0 + y1) / 2), "no king (Ussher)", 18, TEXT_DIM, "mm",
             italic=True)


def draw_reigns(c):
    boxes = {}
    order = sorted(K.REIGNS, key=lambda k: (k in HALF, K.REIGNS[k].order))
    for key in order:
        r = K.REIGNS[key]
        x0, y0, x1, y1 = bar_box(key)
        fill = VERDICT_FILL.get(r.verdict, VERDICT_FILL["none stated"])
        c.rect(x0 + 2, y0 + 1, x1 - x0 - 4, y1 - y0 - 2, fill=fill,
               stroke=REALM_LINE[r.realm], width=2.5 if key not in HALF else 3, rx=6)
        h = y1 - y0
        room = x1 - x0 - 24
        name = fit(r.name, 24, room, bold=True)
        us = f"{yrs(*r.ussher)} BC" if r.ussher else ""
        th = f"Thiele {yrs(*r.thiele)}" if r.thiele else ""
        if h >= 74:
            text(c, (x0 + 14, y0 + 22), name, 24, (246, 236, 206), "lm", bold=True)
            text(c, (x0 + 14, y0 + 46), us, 17, TEXT, "lm")
            if th:
                text(c, (x0 + 14, y0 + 66), th, 15, THIELE_COL, "lm")
        else:
            text(c, (x0 + 14, y0 + 18), name, 22, (246, 236, 206), "lm", bold=True)
            text(c, (x0 + 14, y0 + 38), fit(us, 14, room), 14, TEXT, "lm")
            # Thiele's years in his own colour, where they fit after Ussher's
            tx0 = x0 + 14 + width(us, 14) + 14
            if th and tx0 + width(th, 14) <= x1 - 10:
                text(c, (tx0, y0 + 38), th, 14, THIELE_COL, "lm")
        boxes[key] = (x0, y0, x1, y1)
    return boxes


def pack(items):
    """Greedy lanes for (key, top, bottom): the first lane each fits in."""
    lanes, out = [], {}
    for key, a, b in sorted(items, key=lambda x: x[1]):
        for i, end in enumerate(lanes):
            if a > end + 50:
                lanes[i] = b
                out[key] = i
                break
        else:
            lanes.append(b)
            out[key] = len(lanes) - 1
    return out


# the exile and the return, which no reign spans: Ussher's years from the
# verses that date them (chronology.BIND places Daniel 606, Ezekiel 593 and
# Zechariah 520)
FIXED = {"daniel": (606, 534, "Dan 1:1; 10:1"),
         # the 5th and 25th years of Jehoiachin's captivity, counted from 599
         "ezekiel": (595, 575, "Ezek 1:2; 40:1"),
         "haggai": (520, 520, "Hag 1:1"), "zechariah": (520, 518, "Zech 1:1; 7:1"),
         # where the kings a prophet is set beside overstate his span: Samuel
         # died before David reigned (1 Sam 25:1; Ussher 1060); Jeremiah began
         # in Josiah's 13th year (chronology.BIND's 627); Amos's Uzziah and
         # Jeroboam reigned together 810-784; Hosea's Jeroboam is alive at the
         # start, his Hezekiah at the end
         "samuel": (1100, 1060, "1 Sam 10:1; 25:1"),
         "jeremiah": (627, 588, "Jer 1:2-3"),
         "amos": (810, 784, "Amos 1:1"), "hosea": (810, 698, "Hos 1:1")}


def prophet_span(key, p):
    if key in FIXED:
        return FIXED[key][:2]
    ks = [find_king(t) for t in p.kings]
    ks = [k for k in ks if k]
    if not ks:
        return None
    if p.kind == "narrative":
        own = [k for k in ks if K.REIGNS[k].realm == p.realm]
        ks = own or ks
    return (max(SPANS[k][0] for k in ks), min(SPANS[k][1] for k in ks))


# shorter names for the narrow bars, where the full name won't fit
PROPHET_SHORT = {"jehu_son_of_hanani": "Jehu son of Hanani", "man_of_god_from_judah": "the man of God",
                 "uriah_son_of_shemaiah": "Uriah", "azariah_son_of_oded": "Azariah son of Oded",
                 "zechariah_son_of_jehoiada": "Zechariah son of Jehoiada",
                 "eliezer_son_of_dodavahu": "Eliezer"}


def prophet_side(p):
    return IP if p.realm == "israel" else JP


def draw_prophets(c):
    boxes, sides = {}, {"JP": [], "IP": []}
    for key, p in PR.PROPHETS.items():
        sp = prophet_span(key, p)
        if not sp:
            continue
        side = "IP" if prophet_side(p) is IP else "JP"
        sides[side].append((key, Y(sp[0]), max(Y(sp[1]), Y(sp[0]) + 130)))
    for side, items in sides.items():
        x0, x1 = JP if side == "JP" else IP
        lanes = pack(items)
        n = max(lanes.values()) + 1
        lw = min(150, (x1 - x0) / n)
        for key, y0, y1 in items:
            i = lanes[key]
            # the prophets to Judah fill from the kings' side out
            lx = x1 - (i + 1) * lw if side == "JP" else x0 + i * lw
            p = PR.PROPHETS[key]
            col = (150, 130, 190) if p.kind == "writing" else (120, 110, 140)
            c.rect(lx + 4, y0, lw - 8, y1 - y0, fill=(36, 32, 48), stroke=col,
                   width=2.5 if p.kind == "writing" else 1.5, rx=10)
            # the full name if it fits, else a shorter one, else smaller
            room = y1 - y0 - 24
            label, fs = p.name, 19
            if width(label, fs) > room:
                label = PROPHET_SHORT.get(key, label)
            while width(label, fs) > room and fs > 14:
                fs -= 1
            c._emit(f'<text x="{_fmt(lx + lw / 2)}" y="{_fmt(y0 + 12)}" font-size="{fs}" '
                    f'fill="{_rgb((222, 210, 240))}" font-weight="{"bold" if p.kind == "writing" else "normal"}" '
                    f'writing-mode="tb" text-anchor="start">{_esc(fit(label, fs, room))}</text>')
            boxes[key] = (lx + 4, y0, lx + lw - 4, y1)
    return boxes


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


UNDATED = [k for k, p in PR.PROPHETS.items() if p.kind == "writing" and not prophet_span(k, p)]


def draw_undated(c, below):
    boxes = {}
    y = max(Y(BOTTOM_BC), below) + 50
    x0 = JP[0]
    text(c, (x0, y), "Undated in their own words:", 22, TEXT_DIM, "lm", italic=True)
    x = x0 + width("Undated in their own words:", 22, italic=True) + 24
    for key in UNDATED:
        p = PR.PROPHETS[key]
        w = width(p.name, 22, bold=True) + 30
        c.rect(x, y - 22, w, 44, fill=(36, 32, 48), stroke=(150, 130, 190), width=2, rx=10)
        text(c, (x + w / 2, y), p.name, 22, (222, 210, 240), "mm", bold=True)
        boxes[key] = (x, y - 22, x + w, y + 22)
        x += w + 16
    return boxes


def event_year(e, chron="ussher", key_=None):
    """(bc, exact) for an event, in a count: its anchor king's regnal year,
    accession or death, or the middle of his reign when the text gives none;
    in Ussher's count, his own year where kings.EVENT_USSHER gives it."""
    if chron == "ussher" and key_ in K.EVENT_USSHER:
        exact = bool(re.match(r"\d", e.anchor_year)) or e.anchor_year in ("accession", "death")
        return (K.EVENT_USSHER[key_], exact)
    key = find_king(e.anchor_king)
    if not key:
        # Cyrus's first year, dated by his own reign: Ussher's 536, and 538
        # in the modern count Thiele's dates belong to
        if "Cyrus" in e.foreign_king:
            return (536 if chron == "ussher" else 538, True)
        return (None, False)
    r = K.REIGNS[key]
    yrs_ = r.ussher if chron == "ussher" else r.thiele
    if not yrs_:
        return (None, False)
    a, b = yrs_
    t = e.anchor_year.lower()
    m = re.match(r"(\d+)", t)
    if m:
        return (a - (int(m.group(1)) - 1), True)
    if "accession" in t:
        return (a, True)
    if "death" in t:
        return (b, True)
    return ((a + b) / 2, False)


def event_name(e):
    """The foreign king as the sheet names him: 'Shishak, Egypt'; the nation
    alone where the text names no king ('the king of Assyria')."""
    nation = re.sub(r"\s*\([^)]*\)", "", e.nation).split("/")[0].strip()
    if e.foreign_king.lower().startswith("the king of"):
        return nation
    return f"{e.foreign_king}, {nation}"


def event_when(e, exact):
    anchor = find_king(e.anchor_king)
    whose = K.REIGNS[anchor].name if anchor else e.foreign_king
    if re.match(r"\d", e.anchor_year):
        return f"{whose}'s {ordinal(e.anchor_year)}"
    if "death" in e.anchor_year and anchor:
        return f"at {whose}'s death"
    if "accession" in e.anchor_year and anchor:
        return f"as {whose} came to the throne"
    return f"in {whose}'s reign" if anchor else ""


def spread(ys, gap):
    """Positions for labels wanted at ys (sorted), at least gap apart, each
    crowded run centred on the years it stands for, so a stack spreads up
    and down from its reign rather than only down."""
    groups = [[y] for y in ys]
    pos = list(ys)
    while True:
        out, start, moved = [], [], False
        for g in groups:
            if out:
                n_prev = len(out[-1])
                top_prev = start[-1]
                if top_prev + n_prev * gap > sum(g) / len(g) - (len(g) - 1) * gap / 2:
                    out[-1] = out[-1] + g
                    moved = True
                    m = sum(out[-1]) / len(out[-1])
                    start[-1] = m - (len(out[-1]) - 1) * gap / 2
                    continue
            out.append(g)
            start.append(sum(g) / len(g) - (len(g) - 1) * gap / 2)
        groups = out
        if not moved:
            break
    pos = []
    for g, s in zip(groups, start):
        pos += [s + i * gap for i in range(len(g))]
    return pos


def draw_events(c):
    """Each side's events in their own stack: Judah's labels to the left of
    the column, Israel's to the right, so the leaders never cross it."""
    boxes = {}
    side = {"judah": [], "israel": []}
    for key, e in K.EVENTS.items():
        bc, exact = event_year(e, key_=key)
        if bc is None:
            continue
        anchor = find_king(e.anchor_king)
        realm = "israel" if anchor and K.REIGNS[anchor].realm == "israel" else "judah"
        order = K.REIGNS[anchor].order if anchor else 99
        side[realm].append((Y(bc), order, key, e, exact))
    mid = (NA[0] + NA[1]) / 2
    for realm, items in side.items():
        items.sort(key=lambda x: (x[0], x[1]))
        lys = spread([y for y, *_ in items], 46)
        for (y, _o, key, e, exact), ly in zip(items, lys):
            if realm == "israel":
                c.line((NA[1] - 40, y), (IK[0], y), EVENT_COL, 2)
                mx, lx, anchor_ = NA[1] - 40, NA[1] - 64, "r"
            else:
                c.line((JK[1], y), (NA[0] + 40, y), EVENT_COL, 2)
                mx, lx, anchor_ = NA[0] + 40, NA[0] + 64, "l"
            if exact:
                c.circle(mx, y, 7, fill=EVENT_COL)
            else:
                c.circle(mx, y, 6, fill=BG, stroke=EVENT_COL, width=2.5)
            if abs(ly - y) > 1:
                c.line((mx, y), (lx + (6 if anchor_ == "r" else -6), ly), EVENT_COL, 1)
            room = mid - NA[0] - 74
            name = fit(event_name(e), 19, room, bold=True)
            gist = K.EVENT_GIST.get(key, "")
            sub = fit(" · ".join(x for x in (gist, event_when(e, exact)) if x), 15, room,
                      italic=True)
            text(c, (lx, ly - 2), name, 19, (236, 214, 190), anchor_ + "s", bold=True)
            if sub:
                text(c, (lx, ly + 16), sub, 15, TEXT_DIM, anchor_ + "m", italic=True)
            w = max(width(name, 19, True), width(sub, 15, italic=True) if sub else 0)
            x0, x1 = (lx, lx + w) if anchor_ == "l" else (lx - w, lx)
            boxes[key] = (min(x0, mx) - 10, ly - 24, max(x1, mx) + 10, ly + 26)
    return boxes


def ordinal(n):
    m = re.match(r"(\d+)", n)
    if not m:
        return n
    i = int(m.group(1))
    suf = "th" if 10 <= i % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(i % 10, "th")
    tail = " year" + (" of his captivity" if "captivity" in n else "")
    return f"{i}{suf}{tail}"


JW, JH, JGAP = 126, 110, 8


NUMBER = {"three": 3, "six": 6, "seven": 7, "eight": 8, "ten": 10, "twenty": 20,
          "twenty-two": 22, "twenty-three": 23, "forty": 40, "eighty": 80}
# the enemy, short, where the text's phrase is long
JUDGE_FOE = {"jephthah": "Ammon, Philistines"}


def judge_years(j):
    """The years the text gives, as a figure: 'forty years' -> '40 years'."""
    m = re.search(r"(\w+(?:-\w+)?) years", j.years)
    if not m:
        return ""
    n = NUMBER.get(m.group(1).lower())
    return f"{n} years" if n else f"{m.group(1)} years"


def draw_judges(c):
    boxes = {}
    js = sorted(K.JUDGES.items(), key=lambda x: x[1].order)
    total = len(js) * (JW + JGAP) - JGAP
    x = (W - total) / 2
    y = 300
    text(c, (W / 2, y - 30), "THE JUDGES, IN ORDER — the years the text gives each; not to scale",
         22, TEXT_DIM, "mm", spacing=2)
    for key, j in js:
        c.rect(x, y, JW, JH, fill=(40, 38, 34), stroke=SAND_DIM, width=2, rx=8)
        fs = 21
        while width(j.name, fs, bold=True) > JW - 12 and fs > 15:
            fs -= 1
        text(c, (x + JW / 2, y + 26), fit(j.name, fs, JW - 12, bold=True), fs,
             (240, 226, 190), "mm", bold=True)
        yy = judge_years(j)
        if yy:
            text(c, (x + JW / 2, y + 54), yy, 18, TEXT, "mm")
        if j.oppressor:
            foe = JUDGE_FOE.get(key) or short_oppressor(j.oppressor)
            text(c, (x + JW / 2, y + 82), fit(foe, 14, JW - 10), 14, TEXT_DIM, "mm",
                 italic=True)
        boxes[key] = (x, y, x + JW, y + JH)
        x += JW + JGAP
    return boxes


def short_oppressor(s):
    return re.split(r",| \(| who | the king", s)[0].strip()


def draw_masthead(c):
    text(c, (60, 90), TITLE, 64, TEXT, "lm", bold=True)
    text(c, (62, 150), "Israel and Judah from Saul to the exile, on Ussher's years, "
         "with Thiele's beside them", 26, TEXT_DIM, "lm", italic=True)


def draw_legend(c):
    x, y = 1350, 70
    for v, word in (("right", "did right"), ("right, but", "right, but…"),
                    ("evil", "did evil"), ("none stated", "no verdict")):
        c.rect(x, y - 14, 40, 28, fill=VERDICT_FILL[v], stroke=SAND_DIM, width=1.5, rx=5)
        text(c, (x + 52, y), word, 20, TEXT, "lm")
        x += 70 + width(word, 20)
    x, y = 1350, 120
    c.circle(x + 10, y, 7, fill=EVENT_COL)
    text(c, (x + 26, y), "dated by a king's year", 18, TEXT, "lm")
    x += 250
    c.circle(x + 10, y, 6, fill=BG, stroke=EVENT_COL, width=2.5)
    text(c, (x + 26, y), "in his reign, year not given", 18, TEXT, "lm")
    y = 160
    text(c, (1350, y), "Thiele 931–913", 18, THIELE_COL, "lm")
    text(c, (1520, y), "the modern synchronised count", 18, TEXT_DIM, "lm", italic=True)


def build_svg():
    c = SvgCanvas(W, H, bg=BG)
    draw_masthead(c)
    draw_legend(c)
    jb = draw_judges(c)
    draw_rail(c)
    draw_heads(c)
    # the landmark rules under the bars, so they don't strike through a
    # king's years
    draw_landmarks(c, words=False)
    draw_interregna(c)
    rb = draw_reigns(c)
    pb = draw_prophets(c)
    ub = draw_undated(c, max(b[3] for b in pb.values()))
    eb = draw_events(c)
    draw_landmarks(c, words=True)
    return c.tostring().replace(
        "<svg ", f'<svg data-kind="timeline" data-title="{TITLE}" ', 1), rb, pb, ub, eb, jb


# ---------------------------------------------------------------------------
# The sidecar
# ---------------------------------------------------------------------------

def rows(ref):
    """A ref string as rows [book index, c1, v1, c2, v2] (0 = none)."""
    if not ref:
        return []
    return [[BOOK_NAMES.index(r.book), r.c1, r.v1 or 0, r.c2 or 0, r.v2 or 0]
            for r in verse_refs.parse(ref, "Genesis")]


# the father the tree hangs a king under, where the text names him otherwise
TREE_FATHER = {"ahaziah_judah": "Joram",     # Jehoram, as the tree spells him
               "athaliah": "Ahab"}           # "the daughter of Omri": his granddaughter


def tree_ids():
    """Each reign's box on the OT family tree, by name and father."""
    path = os.path.join(OUT_DIR, "Old_Testament_family_tree.json")
    items = json.load(open(path, encoding="utf-8"))["items"]
    out = {}
    for key, r in K.REIGNS.items():
        names = {r.name, *r.aka}
        hits = [i for i, it in enumerate(items) if it.get("x") is None and
                names & {p.strip() for p in it["n"].split("·")}]
        if len(hits) > 1 and (r.father or key in TREE_FATHER):
            f = TREE_FATHER.get(key) or r.father.split()[0]
            hits = [i for i in hits if items[i].get("p") is not None and
                    f in items[items[i]["p"]]["n"]] or hits
        if len(hits) > 1:
            kings = [i for i in hits if items[i].get("k") == "king"]
            hits = kings if len(kings) == 1 else hits
        if len(hits) == 1:
            out[key] = items[hits[0]]["id"]
    return out


REALM_TITLE = {"judah": "king of Judah", "israel": "king of Israel", "united": "king of all Israel"}


def nth(i):
    suf = "th" if 10 <= i % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(i % 10, "th")
    return f"{i}{suf}"


# the rivals and the usurper reigned, but outside the line of kings each
# realm counts, so they take no number
UNCOUNTED = {"ishbosheth", "athaliah", "tibni"}


def counted(key):
    """A king's place in his realm's line: Saul 1st, David 2nd, Solomon 3rd."""
    r = K.REIGNS[key]
    return 1 + sum(1 for k, o in K.REIGNS.items() if o.realm == r.realm and
                   o.order < r.order and k not in UNCOUNTED)


def king_card(key, b, tree):
    r = K.REIGNS[key]
    title = f"{REALM_TITLE[r.realm]}, the {nth(counted(key))}"
    if key == "athaliah":
        title = "queen over Judah, the usurper"
    if key == "tibni":
        title = "rival of Omri for Israel"
    if key == "ishbosheth":
        title = "king over Israel, not Judah, rival of David"
    dims = []
    if r.ussher:
        dims.append(["Ussher", f"{yrs(*r.ussher)} BC", "", []])
    if r.thiele:
        dims.append(["Thiele", f"{yrs(*r.thiele)} BC" +
                     (f", with a coregency from {r.coregent}" if r.coregent else ""), "", []])
    for label, value, ref in (("Reigned", r.length + (f", from age {r.age}" if r.age else ""), r.length_ref),
                              ("Came to the throne", r.synchronism, r.synchronism_ref),
                              ("Father", r.father, r.father_ref),
                              ("Mother", r.mother, r.mother_ref)):
        if value:
            dims.append([label, value, "", rows(ref)])
    if r.verdict_text:
        flag = {"right": "right", "evil": "evil", "right, but": "right, but"}.get(r.verdict, "")
        dims.append(["The verdict", r.verdict_text, flag, rows(r.verdict_ref)])
    for label, value, ref in (("The end", r.end, r.end_ref), ("Buried", r.buried, r.buried_ref)):
        if value:
            dims.append([label, value, "", rows(ref)])
    tx = []
    if r.aka:
        tx.append(["Also called", ", ".join(r.aka)])
    if r.length_alt:
        tx.append(["The texts differ", r.length_alt])
    if r.ussher_note:
        tx.append(["Ussher's years", r.ussher_note])
    item = {"id": key.replace("_", "-"), "n": r.name, "s": title,
            "a": list(r.aka), "dims": dims, "tx": tx,
            "b": [round(b[0], 1), round(b[1], 1), round(b[2] - b[0], 1), round(b[3] - b[1], 1)]}
    if r.note:
        item["note"] = r.note
    rg = []
    if r.kings_refs:
        rg.append(["In " + ("Samuel and Kings" if "Sam" in r.kings_refs and "Kgs" in r.kings_refs
                            else "Samuel" if "Sam" in r.kings_refs else "Kings"), rows(r.kings_refs)])
    if r.chronicles_refs:
        rg.append(["In Chronicles", rows(r.chronicles_refs)])
    item["rg"] = rg
    singles = [x for ref in (r.synchronism_ref, r.length_ref, r.verdict_ref, r.mother_ref,
                             r.end_ref, r.buried_ref) for x in rows(ref)]
    item["r"] = singles + rows(r.kings_refs) + rows(r.chronicles_refs)
    if key in tree:
        item["ln"] = [["On the family tree",
                       f"/visuals/reference/Old_Testament_family_tree.html#id={tree[key]}"]]
    return item


BOOK_OF = {"isaiah": "Isaiah", "jeremiah": "Jeremiah", "ezekiel": "Ezekiel", "daniel": "Daniel",
           "hosea": "Hosea", "joel": "Joel", "amos": "Amos", "obadiah": "Obadiah",
           "jonah": "Jonah", "micah": "Micah", "nahum": "Nahum", "habakkuk": "Habakkuk",
           "zephaniah": "Zephaniah", "haggai": "Haggai", "zechariah": "Zechariah",
           "malachi": "Malachi"}
REALM_TO = {"judah": "to Judah", "israel": "to Israel", "united": "to all Israel",
            "exile": "in the exile", "return": "after the return"}


def prophet_card(key, b):
    p = PR.PROPHETS[key]
    item = {"id": "prophet-" + key.replace("_", "-"), "n": p.name,
            "s": ("writing prophet " if p.kind == "writing" else "prophet ") + REALM_TO[p.realm],
            "a": list(p.aka),
            "b": [round(b[0], 1), round(b[1], 1), round(b[2] - b[0], 1), round(b[3] - b[1], 1)]}
    dims = []
    if p.dated_by:
        dims.append(["Dated by", p.dated_text or "", "", rows(p.dated_by)])
    if key in FIXED:
        a, e, ref = FIXED[key]
        dims.append(["Ussher", f"{yrs(a, e)} BC, from the years these verses give", "", rows(ref)])
    item["dims"] = dims
    tx = []
    if p.kings:
        tx.append(["Kings named", ", ".join(p.kings)])
    item["tx"] = tx
    if p.note:
        item["note"] = p.note
    rg = [["Named in", rows(p.refs)]]
    book = BOOK_OF.get(key) if p.kind == "writing" else None
    if book:
        rg.append(["The book", [[BOOK_NAMES.index(book), 1, 0, chapters_in(book), 0]]])
    item["rg"] = rg
    item["r"] = rows(p.dated_by) + rows(p.refs) + (rg[1][1] if book else [])
    item["kings"] = [k for k in (find_king(t) for t in p.kings) if k]
    return item


def event_card(key, b):
    e = K.EVENTS[key]
    u, ue = event_year(e, key_=key)
    anchor = find_king(e.anchor_king)
    dims = [["Dated", e.ref_text or e.anchor_year, "", rows(e.ref)]]
    if u is not None:
        dims.append(["Ussher", (f"{round(u)} BC" if ue else f"about {round(u)} BC, in the reign"), "", []])
    # the modern date, with its source, stands for Thiele's count: his
    # synchronisms don't all follow from a king's whole-year reign
    if e.modern:
        dims.append(["Modern", e.modern, "", []])
    # titled by the foreign king, as the sheet names him; what happened is
    # the note
    when = (f"{K.REIGNS[anchor].name}'s {ordinal(e.anchor_year)}" if anchor and re.match(r"\d", e.anchor_year)
            else f"at {K.REIGNS[anchor].name}'s death" if anchor and "death" in e.anchor_year
            else f"as {K.REIGNS[anchor].name} came to the throne" if anchor and "accession" in e.anchor_year
            else f"in {K.REIGNS[anchor].name}'s reign" if anchor else "")
    item = {"id": "event-" + key.replace("_", "-"), "n": e.foreign_king,
            "s": ", ".join(x for x in (e.nation, when) if x), "a": [e.nation], "dims": dims,
            "note": e.label + ".",
            "b": [round(b[0], 1), round(b[1], 1), round(b[2] - b[0], 1), round(b[3] - b[1], 1)],
            "rg": [], "r": rows(e.ref), "anchor": anchor}
    return item


def judge_card(key, b):
    j = K.JUDGES[key]
    dims = []
    if j.years:
        dims.append(["Years", j.years, "", rows(j.years_ref)])
    if j.oppressor:
        dims.append(["Before", j.oppressor + (f", {j.oppression_years}" if j.oppression_years else ""),
                     "", rows(j.oppression_ref)])
    if j.tribe:
        dims.append(["Tribe", j.tribe, "", rows(j.tribe_ref)])
    item = {"id": "judge-" + key.replace("_", "-"), "n": j.name,
            "s": "judge, " + nth(j.order) + " in the book's order" if key not in ("eli", "samuel")
            else "judged Israel (1 Samuel)", "a": [], "dims": dims,
            "b": [round(b[0], 1), round(b[1], 1), round(b[2] - b[0], 1), round(b[3] - b[1], 1)],
            "rg": [["The story", rows(j.refs)]], "r": rows(j.years_ref) + rows(j.refs)}
    if j.note:
        item["note"] = j.note
    return item


def sidecar(rb, pb, ub, eb, jb):
    tree = tree_ids()
    items, index = [], {}
    for key in sorted(K.REIGNS, key=lambda k: ({"united": 0, "judah": 1, "israel": 2}[K.REIGNS[k].realm],
                                               K.REIGNS[k].order)):
        index[("k", key)] = len(items)
        items.append(king_card(key, rb[key], tree))
    for key in PR.PROPHETS:
        b = pb.get(key) or ub.get(key)
        if not b:
            continue
        index[("p", key)] = len(items)
        items.append(prophet_card(key, b))
    for key in K.EVENTS:
        if key in eb:
            index[("e", key)] = len(items)
            items.append(event_card(key, eb[key]))
    for key in K.JUDGES:
        index[("j", key)] = len(items)
        items.append(judge_card(key, jb[key]))
    # the links between them: a king's prophets and events, a prophet's and
    # an event's king
    for it in items:
        ks = it.pop("kings", None)
        if ks is not None:
            it["see"] = [index[("k", k)] for k in ks if ("k", k) in index]
        a = it.pop("anchor", None) if "anchor" in it else None
        if a:
            it["see"] = [index[("k", a)]]
    for key in K.REIGNS:
        i = index[("k", key)]
        see = [j for j, it in enumerate(items) if i in it.get("see", []) and j != i]
        if see:
            items[i]["see"] = see
    used = sorted({r[0] for it in items for r in it.get("r", [])} |
                  {r[0] for it in items for _g, rs in it.get("rg", []) for r in rs} |
                  {r[0] for it in items for d in it.get("dims", []) for r in d[3]})
    remap = {b: i for i, b in enumerate(used)}
    done = set()
    for it in items:
        lists = [it.get("r", [])] + [rs for _g, rs in it.get("rg", [])] + [d[3] for d in it.get("dims", [])]
        for r in (r for rs in lists for r in rs):
            if id(r) not in done:
                done.add(id(r))
                r[0] = remap[r[0]]
    ids = [it["id"] for it in items]
    assert len(set(ids)) == len(ids), "ids collide"
    return {"version": 1, "card": "parts", "noun": ["king or prophet", "kings and prophets"],
            "books": [BOOK_NAMES[b] for b in used], "items": items}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    svg, rb, pb, ub, eb, jb = build_svg()
    path = os.path.join(OUT_DIR, STEM + ".svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    data = sidecar(rb, pb, ub, eb, jb)
    dp = os.path.join(OUT_DIR, STEM + ".json")
    with open(dp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    vp = os.path.join(OUT_DIR, STEM + ".html")
    with open(vp, "w", encoding="utf-8") as f:
        f.write(reference_viewer.page(
            STEM, _fmt(W), _fmt(H), TITLE, data=True,
            placeholder="find a king or prophet — Jehu, Elijah…"))
    print(path)
    print(f"  {W} x {H} px · {os.path.getsize(path) / 1024:.0f} KB")
    print(dp)
    print(f"  {len(data['items'])} cards · {os.path.getsize(dp) / 1024:.0f} KB")
    print(vp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
