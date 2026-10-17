"""Generate per-verse genealogy animations for Genesis 5 and Genesis 11:10-32.

Layout: the family chain on the left (Adam -> Noah, or Shem -> Abram) and
an overlapping-lifespans TIMELINE filling the right
side — one horizontal bar per patriarch, positioned by birth year, so the
listener watches lives overlap down the family line (Adam's life reaches
Lamech's; Methuselah's ends in the flood year; in Genesis 11 the lifespans
visibly collapse after the flood).

Nothing textual flashes: all text is drawn at full opacity. The only pulsing
element is the small ring marking the current person; all other animation is
bars/edges extending once per loop.

Because the visuals contain names, and translations spell them differently
(KJV "Enos/Cainan", WEB "Enosh/Kenan", Douay-Rheims "Henoch/Mathusala"),
this script fetches each translation's actual chapter text, detects which
spelling it uses, and writes translation-suffixed files (Genesis_5_3.KJV.webp)
only for translations that differ from the generic (WEB-spelling) set.

Run inside the project venv:  .venv\\Scripts\\python.exe generate_genealogy.py
"""

import os
import re
import time


import svg_figures as F

from generate_tabernacle import (W, H, BG, PANEL, SAND,
                                 SAND_DIM, TEXT, TEXT_DIM, HL,
                                 F_LABEL, F_SMALL, F_DIM, F_VERSE, F_TITLE,
                                 font, ease, g, dashed_line, out_path)
from passages import fetch_passage, PassageError, TRANSLATIONS

F_CHAIN = font(17)                  # chain names
F_CHAIN_CUR = font(17, bold=True)   # current person pops from the chain
F_NUM = font(14)                    # year labels/ticks — upright; small
                                    # italic digits blur at fullscreen

# Genealogy animations play ONCE, slowly, then hold (loop=1 in the saved
# file; the app honors it). Nothing pulses — per user feedback, no flashing.
G_FRAMES = 24
G_FRAME_MS = 120

# ---------------------------------------------------------------------------
# Name spellings, verified against each translation's own text
# ---------------------------------------------------------------------------

NAME_VARIANTS = {
    "Adam": ["Adam"], "Seth": ["Seth"],
    "Enosh": ["Enosh", "Enos"],
    "Kenan": ["Kenan", "Cainan"],
    "Mahalalel": ["Mahalalel", "Mahalaleel", "Malaleel"],
    "Jared": ["Jared", "Jered"],
    "Enoch": ["Enoch", "Henoch"],
    "Methuselah": ["Methuselah", "Methushelah", "Mathusala"],
    "Lamech": ["Lamech", "Lemech"],
    "Noah": ["Noah", "Noe"],
    "Shem": ["Shem", "Sem"],
    "Ham": ["Ham", "Cham"],
    "Japheth": ["Japheth", "Japhet"],
    "Arpachshad": ["Arpachshad", "Arphaxad"],
    "Shelah": ["Shelah", "Salah", "Sale"],
    "Eber": ["Eber", "Heber"],
    "Peleg": ["Peleg", "Phaleg"],
    "Reu": ["Reu", "Ragau"],
    "Serug": ["Serug", "Sarug"],
    "Nahor": ["Nahor", "Nachor"],
    "Terah": ["Terah", "Thare"],
    "Abram": ["Abram"],
    "Haran": ["Haran", "Aran"],
    "Sarai": ["Sarai"],
    "Lot": ["Lot"],
}

G5_KEYS = ["Adam", "Seth", "Enosh", "Kenan", "Mahalalel", "Jared", "Enoch",
           "Methuselah", "Lamech", "Noah", "Shem", "Ham", "Japheth"]
G11_KEYS = ["Shem", "Arpachshad", "Shelah", "Eber", "Peleg", "Reu", "Serug",
            "Nahor", "Terah", "Abram", "Haran", "Sarai", "Lot"]


def resolve_names(code, chapter, keys, book="Genesis", variants=None):
    variants = variants or NAME_VARIANTS
    for attempt in range(2):
        try:
            # fetch_passage prefers local bundles (bibles/<CODE>/), which is
            # the only path for BSB/YLT/OEB; API translations fall through
            # to bible-api.com (usually already disk-cached).
            p = fetch_passage("", book, chapter, code)
            break
        except PassageError as e:
            if attempt == 0 and "rate limit" in str(e).lower():
                time.sleep(32)
            else:
                raise
    text = " ".join(t for _, t in p.verses)
    out = {}
    for key in keys:
        for variant in variants[key]:
            if re.search(rf"\b{variant}\b", text):
                out[key] = variant
                break
        else:
            out[key] = variants[key][0]
            print(f"  !! {code} {book} {chapter}: no variant of {key} "
                  f"found; using {out[key]}")
    return out


# ---------------------------------------------------------------------------
# Chapter data
# ---------------------------------------------------------------------------

# (key, age at son's birth, years after, total years, verse of "fathered")
G5_LINE = [
    ("Adam", 130, 800, 930, 3), ("Seth", 105, 807, 912, 6),
    ("Enosh", 90, 815, 905, 9), ("Kenan", 70, 840, 910, 12),
    ("Mahalalel", 65, 830, 895, 15), ("Jared", 162, 800, 962, 18),
    ("Enoch", 65, 300, 365, 21), ("Methuselah", 187, 782, 969, 25),
    ("Lamech", 182, 595, 777, 28), ("Noah", 500, None, None, 32),
]

# (key, age at son's birth, years after, verse of "fathered")
G11_LINE = [
    ("Shem", 100, 500, 10), ("Arpachshad", 35, 403, 12),
    ("Shelah", 30, 403, 14), ("Eber", 34, 430, 16),
    ("Peleg", 30, 209, 18), ("Reu", 32, 207, 20),
    ("Serug", 30, 200, 22), ("Nahor", 29, 119, 24),
    ("Terah", 70, None, 26), ("Abram", None, None, None),
]


class ChapterData:
    """Timeline numbers derived from the chapter's own figures."""

    def __init__(self, chapter):
        self.chapter = chapter
        if chapter == 5:
            self.keys = [k for k, *_ in G5_LINE]
            self.ages = [a for _, a, *_ in G5_LINE]
            self.fathered_verses = [v for *_, v in G5_LINE]
            self.done_verses = [5, 8, 11, 14, 17, 20, 23, 27, 31, None]
            births = [0]
            for age in self.ages[:-1]:
                births.append(births[-1] + age)
            self.births = births
            self.deaths = [b + t if t else None
                           for b, (_, _, _, t, _) in zip(births, G5_LINE)]
            self.taken_index = 6           # Enoch
            self.range = (0, 1750)
            self.ticks = (0, 500, 1000, 1500)
            self.axis_label = "years after the creation of Adam"
            self.flood_x = 1656            # Methuselah's death year
            self.title = "The Generations of Adam — Genesis 5"
        else:
            self.keys = [k for k, *_ in G11_LINE]
            self.ages = [a for _, a, *_ in G11_LINE]
            self.fathered_verses = [v for *_, v in G11_LINE]
            self.done_verses = [11, 13, 15, 17, 19, 21, 23, 25, 32, None]
            births = [-98]                 # Shem was 100 two years after
            for age in self.ages[:-1]:     # the flood (Gen 11:10)
                births.append(births[-1] + age)
            self.births = births
            deaths = []
            for b, (key, age, after, _) in zip(births, G11_LINE):
                if key == "Terah":
                    deaths.append(b + 205)  # stated in v32
                elif age is not None and after is not None:
                    deaths.append(b + age + after)
                else:
                    deaths.append(None)
            self.deaths = deaths
            self.taken_index = None
            self.range = (-120, 570)
            self.ticks = (0, 200, 400)
            self.axis_label = "years after the flood"
            self.flood_x = 0
            self.title = "From Shem to Abram — Genesis 11"

    def birth_verse(self, i):
        return 1 if i == 0 else self.fathered_verses[i - 1]


# ---------------------------------------------------------------------------
# Verse specs.  stage: intro | fathered | after | named | total | taken |
#                      trio | narr
# ---------------------------------------------------------------------------

def build_g5_specs(n):
    line = G5_LINE
    specs = {
        1: dict(caption="the book of the generations of Adam", focus=0,
                stage="intro",
                card=(n["Adam"], ["made in the likeness of God"])),
        2: dict(caption="male and female he created them", focus=0,
                stage="intro",
                card=(n["Adam"], ["created male and female,",
                                  "blessed, and named Mankind"])),
    }
    for i, (key, age, after, total, v) in enumerate(line[:-1]):
        child = line[i + 1][0]
        specs[v] = dict(
            caption=f"{n[key]} fathered {n[child]}", focus=i, stage="fathered",
            card=(n[key], [f"fathered {n[child]} at {age}"]))
        if key == "Enoch":
            specs[v + 1] = dict(
                caption="Enoch walked with God 300 years", focus=i,
                stage="after",
                card=(n[key], ["walked with God 300 years",
                               f"after {n[child]} was born"]))
            specs[v + 2] = dict(
                caption="all the days of Enoch: 365 years", focus=i,
                stage="total",
                card=(n[key], ["all his days: 365 years"]))
            specs[v + 3] = dict(
                caption="he was not, for God took him", focus=i,
                stage="taken",
                card=(n[key], ["walked with God, and he was not,",
                               "for God took him"]))
        elif key == "Lamech":
            specs[v + 1] = dict(
                caption=f"he named him {n['Noah']} — “this one will comfort us”",
                focus=i, stage="named",
                card=(n[key], [f"named his son {n['Noah']} —",
                               "“this one shall comfort us in our work”"]))
            specs[v + 2] = dict(
                caption=f"{n[key]} lived {after} years after", focus=i,
                stage="after",
                card=(n[key], [f"lived {after} years after {n['Noah']},",
                               "and had other sons and daughters"]))
            specs[v + 3] = dict(
                caption=f"all the days of {n[key]}: {total} years", focus=i,
                stage="total",
                card=(n[key], [f"all his days: {total} years — he died"]))
        else:
            specs[v + 1] = dict(
                caption=f"{n[key]} lived {after} years after", focus=i,
                stage="after",
                card=(n[key], [f"lived {after} years after {n[child]},",
                               "and had other sons and daughters"]))
            lines = [f"all his days: {total} years — he died"]
            total_caption = f"all the days of {n[key]}: {total} years"
            if key == "Methuselah":
                lines.append("the longest recorded life")
                total_caption += " — the longest recorded life"
            specs[v + 2] = dict(
                caption=total_caption, focus=i,
                stage="total", card=(n[key], lines))
    specs[32] = dict(
        caption=f"{n['Noah']} fathered {n['Shem']}, {n['Ham']}, and "
                f"{n['Japheth']}",
        focus=9, stage="trio",
        card=(n["Noah"], ["after 500 years, fathered",
                          f"{n['Shem']}, {n['Ham']}, and {n['Japheth']}"]))
    return specs


def build_g11_specs(n):
    line = G11_LINE
    specs = {}
    for i, (key, age, after, v) in enumerate(line[:-1]):
        if v is None:
            continue
        child = line[i + 1][0]
        extra = " — two years after the flood" if key == "Shem" else ""
        if key == "Terah":
            specs[26] = dict(
                caption=f"{n['Terah']} fathered {n['Abram']}, {n['Nahor']}, "
                        f"and {n['Haran']}",
                focus=i, stage="fathered",
                card=(n[key], [f"at 70, fathered {n['Abram']},",
                               f"{n['Nahor']}, and {n['Haran']}"]))
            continue
        specs[v] = dict(
            caption=f"{n[key]} fathered {n[child]}{extra}", focus=i,
            stage="fathered",
            card=(n[key], [f"fathered {n[child]} at {age}{extra}"]))
        specs[v + 1] = dict(
            caption=f"{n[key]} lived {after} years after", focus=i,
            stage="after",
            card=(n[key], [f"lived {after} years after {n[child]},",
                           "and had other sons and daughters"]))
    specs[27] = dict(
        caption=f"the generations of {n['Terah']}", focus=8, stage="narr",
        card=(n["Terah"], [f"{n['Abram']}, {n['Nahor']}, {n['Haran']} —",
                           f"and {n['Haran']} fathered {n['Lot']}"]))
    specs[28] = dict(
        caption=f"{n['Haran']} died before his father, in Ur", focus=8,
        stage="narr",
        card=(n["Haran"], ["died before his father Terah,",
                           "in Ur of the Chaldeans"]))
    specs[29] = dict(
        caption=f"{n['Abram']} took {n['Sarai']} as his wife", focus=9,
        stage="narr",
        card=(n["Abram"], [f"took {n['Sarai']} as his wife;",
                           "Nahor married Milcah"]))
    specs[30] = dict(
        caption=f"{n['Sarai']} was barren; she had no child", focus=9,
        stage="narr",
        card=(n["Sarai"], ["was barren —", "she had no child"]))
    specs[31] = dict(
        caption="from Ur toward Canaan; they settled in Haran", focus=8,
        stage="narr",
        card=(n["Terah"], [f"took {n['Abram']}, {n['Lot']}, and {n['Sarai']}",
                           "from Ur toward Canaan, as far as Haran"]))
    specs[32] = dict(
        caption=f"the days of {n['Terah']} were 205 years", focus=8,
        stage="total",
        card=(n["Terah"], ["lived 205 years,", "and died in Haran"]))
    return specs


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

CHAIN_X = 92
CHAIN_TOP, CHAIN_STEP = 112, 42
TL_X0, TL_X1 = 430, 985
BAR_H = 4              # half-height of a timeline bar (kept slim so the
                       # year labels above never touch the bar outline)


def node_y(i):
    return CHAIN_TOP + i * CHAIN_STEP


# ---------------------------------------------------------------------------
# Genesis 5's gutter
# ---------------------------------------------------------------------------
#
# Between the name chain and the timeline there is a column of empty page.
# Chapter 5 has one thing to say that the numbers cannot: eight men are
# reported dead in the same eight words, and one is not. So a tomb lands in
# the gutter on each "and he died" and stays; Enoch's row never gets one and
# empties upward instead; and while Adam is still alive the pair created male
# and female stand on his row, giving way to his tomb at 5:5.
#
# Genesis 11 shares this drawing and gets none of it — no refrain, no Enoch —
# so everything here is gated on the chapter.
#
# Noah's row is deliberately left bare: 5:32 already branches Shem, Ham and
# Japheth across this very gutter as named nodes.

GUT_X = 296                       # clear of the longest name, left of TL_X0
G5_DIED = {5: 0, 8: 1, 11: 2, 14: 3, 17: 4, 20: 5, 27: 7, 31: 8}


def blit(layer, parts, x, gy, s, ink, flip=1):
    """Draw svg_figures parts onto a PIL-shaped surface.

    The vocabulary emits (kind, data, material) for an SvgCanvas; this maps
    those onto the ellipse/polygon/line the genealogy's two backends both
    already speak, so one call works for the raster loop and the vector build
    alike.
    """
    sheet = F.palette(tuple(ink[:3]), BG)
    for kind, data, mat in parts:
        fill, stroke, wd = sheet.get(mat, sheet["rule"])
        w = max(1, int(round(wd)))
        if kind == "dot":
            (cx, cy), = F.place([(data[0], data[1])], x, gy, s, flip)
            r = data[2] * s
            layer.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
                          outline=stroke, width=w)
        elif kind == "fill":
            layer.polygon(F.place(data, x, gy, s, flip), fill=fill,
                          outline=stroke, width=w)
        else:
            layer.line(F.place(data, x, gy, s, flip), fill=stroke, width=w)


def _fit_h(parts, h):
    y0, y1 = F.bbox((parts, 0))[2:]
    return h / (y1 - y0)


def draw_g5_gutter(d, verse):
    """The chapter's own shape, drawn beside the names. Chapter 5 only."""
    if 2 <= verse < 5:                    # male and female he created them
        col = HL if verse == 2 else SAND + (190,)
        for make, dx, h in ((F.man, -15, 36), (F.woman, 15, 34)):
            parts = make()
            blit(d, parts, GUT_X + dx, node_y(0) + 15, _fit_h(parts, h), col)

    tomb = F.tomb()
    for at, row in G5_DIED.items():
        if verse >= at:
            col = HL if verse == at else SAND_DIM + (140,)
            blit(d, tomb, GUT_X, node_y(row) + 12, _fit_h(tomb, 26), col)

    if verse >= 24:                       # and he was not, for God took him
        col = HL if verse == 24 else SAND + (140,)
        man = F.man(arms="up")
        blit(d, man, GUT_X, node_y(6) + 13, _fit_h(man, 30), col)
        for k in range(3):
            yy = node_y(6) - 9 - k * 7
            d.line([(GUT_X - 8 + k * 2, yy), (GUT_X + 8 - k * 2, yy)],
                   fill=col, width=2)


# Genesis 11 has a refrain of its own and it is NOT Genesis 5's. There is no
# "and he died" here at all: eight times over the formula ends "and he became
# the father of sons and daughters", and then stops saying it. So this gutter
# fills with children on exactly the verses that say so — while the bars
# beside them collapse from six hundred years to a hundred and forty-eight.
# Then Terah's grave, the one death the chapter records, and then Abram and
# Sarai with nothing between them. The line multiplies for eight generations
# and runs out at the ninth, which is the whole reason the chapter exists.

G11_SONS = {11: 0, 13: 1, 15: 2, 17: 3, 19: 4, 21: 5, 23: 6, 25: 7}
G11_BROOD = (3, 2, 3, 3, 2, 3, 2, 3)   # fixed, so no row reshuffles per build
G11_TERAH, G11_ABRAM = 8, 9


def draw_g11_gutter(d, verse):
    """Chapter 11 only. See G5's gutter above for the shared reasoning."""
    child = F.child()
    for at, row in G11_SONS.items():
        if verse < at:
            continue
        col = HL if verse == at else SAND_DIM + (150,)
        n = G11_BROOD[row]
        for k in range(n):
            dx = (k - (n - 1) / 2) * 19
            blit(d, child, GUT_X + dx, node_y(row) + 11,
                 _fit_h(child, 21 if k % 2 else 23), col)

    if verse >= 30:                       # Sarai was barren; she had no child
        col = HL if verse == 30 else SAND + (150,)
        for make, dx, h in ((F.man, -22, 34), (F.woman, 22, 32)):
            p = make()
            blit(d, p, GUT_X + dx, node_y(G11_ABRAM) + 14, _fit_h(p, h), col)
        r, cy = 7, node_y(G11_ABRAM) + 2   # the place a child would be, empty
        d.ellipse([GUT_X - r, cy - r, GUT_X + r, cy + r],
                  outline=SAND_DIM + (150,), width=1)

    if verse >= 32:                       # Terah died in Haran
        col = HL if verse == 32 else SAND_DIM + (150,)
        tomb = F.tomb()
        blit(d, tomb, GUT_X, node_y(G11_TERAH) + 12, _fit_h(tomb, 26), col)


def focus_bar(od, xb, y, x_start, x_final, grow, fill, outline):
    """The current person's lifespan bar, drawn onto overlay `od`.

    The bar always spans xb..x_final; `x_start` is where this verse's growth
    begins (xb for a bar built from birth, the son's x for an 'after' verse
    that continues from the son, x_final for a completed-life verse). On the
    vector overlay the xb..x_start part is held and only x_start..x_final wipes
    in, so an 'after' verse never backtracks to birth; on raster the bar is
    drawn at the current grow (x_start..x_final interpolate, as before).
    """
    if hasattr(od, "grow_rect"):
        od.grow_rect([xb, y - BAR_H, x_final, y + BAR_H], x_start,
                     fill=fill, outline=outline, width=2)
    else:
        x_end = x_start + (x_final - x_start) * grow
        od.rectangle([xb, y - BAR_H, x_end, y + BAR_H],
                     fill=fill, outline=outline, width=2)


# The WebP rendering that used to live here has been removed: the app reads
# the SVGs natively, so the raster frames were built for nobody. draw_frame_on
# below is kept and is the real drawing — generate_genealogy_svg.py calls it
# with SVG layers instead of PIL surfaces.

def draw_frame_on(d, od, cd, verse, spec, names, t):
    """Draw one genealogy frame onto base `d` and overlay `od` at phase `t`.

    Surface-agnostic so the same hand-tuned drawing serves both backends: PIL
    ImageDraw for the raster loop, and SvgLayer + SvgAnimLayer for the vector
    build (generate_genealogy_svg.py), where the overlay's growing bars and
    edges self-animate once and hold.
    """
    ring_alpha = 1.0                       # static — nothing flashes
    grow = ease(min(1.0, t / 0.92))

    d.text((28, 20), cd.title, font=F_TITLE, fill=TEXT)
    # (no caption line: the verse is narrated aloud, so the graphic carries
    # only names, years and the chain — specs still hold `caption` data)

    if cd.chapter == 5:
        draw_g5_gutter(d, verse)
    else:
        draw_g11_gutter(d, verse)

    focus = spec["focus"]
    stage = spec["stage"]
    keys = cd.keys

    x0, x1 = cd.range
    scale = (TL_X1 - TL_X0) / (x1 - x0)

    def tx(year):
        return TL_X0 + (year - x0) * scale

    # ---- chain (left) ----
    for i in range(len(keys) - 1):
        y0, y1 = node_y(i) + 7, node_y(i + 1) - 7
        fv = cd.fathered_verses[i]
        established = fv is not None and verse > fv
        if stage == "fathered" and focus == i:
            gy = y0 + (y1 - y0) * grow
            od.line([(CHAIN_X, y0), (CHAIN_X, gy)], fill=g(0.95), width=4)
        d.line([(CHAIN_X, y0), (CHAIN_X, y1)],
               fill=SAND if established else SAND_DIM, width=2)
    for i, key in enumerate(keys):
        y = node_y(i)
        seen = verse >= cd.birth_verse(i)
        d.ellipse([CHAIN_X - 6, y - 6, CHAIN_X + 6, y + 6],
                  outline=SAND if (seen or i <= focus) else SAND_DIM, width=2)
        if i == focus:
            name_font, name_fill = F_CHAIN_CUR, HL
        elif seen or i <= focus:
            name_font, name_fill = F_CHAIN, TEXT
        else:
            name_font, name_fill = F_CHAIN, TEXT_DIM
        d.text((CHAIN_X + 22, y), names[key], font=name_font,
               fill=name_fill, anchor="lm")
        if i == focus:
            od.ellipse([CHAIN_X - 11, y - 11, CHAIN_X + 11, y + 11],
                       outline=g(ring_alpha), width=3)

    if stage == "trio":
        y = node_y(len(keys) - 1)
        trio = [names["Shem"], names["Ham"], names["Japheth"]]
        # start the connector after the father's name, not through it
        # (nx0, not x0 — x0 is the timeline origin captured by tx())
        nx0 = (CHAIN_X + 22 +
               d.textlength(names[keys[-1]], font=F_CHAIN_CUR) + 10)
        for j, nm in enumerate(trio):
            x = 240 + j * 84
            gl = min(1.0, grow * 1.3)
            od.line([(nx0, y), (nx0 + (x - 8 - nx0) * gl, y)],
                    fill=g(0.9), width=2)
            d.ellipse([x - 5, y - 5, x + 5, y + 5], outline=SAND, width=2)
            d.text((x, y - 17), nm, font=F_LABEL, fill=TEXT, anchor="mm")

    # (the top-right fact card was removed at user request — the narration
    # carries the verse content, and the card crowded the year labels
    # of the top timeline bars; specs still carry `card` data if a future
    # design wants it back)

    # ---- timeline ----
    axis_y = node_y(len(keys) - 1) + 30
    d.line([(TL_X0 - 6, axis_y), (TL_X1 + 6, axis_y)], fill=SAND_DIM,
           width=2)
    for tick in cd.ticks:
        x = tx(tick)
        d.line([(x, axis_y - 3), (x, axis_y + 3)], fill=SAND_DIM, width=2)
        d.text((x, axis_y + 11), str(tick), font=F_NUM, fill=TEXT_DIM,
               anchor="mm")
    d.text((TL_X1, axis_y + 26), cd.axis_label, font=F_SMALL, fill=TEXT_DIM,
           anchor="rm")
    if cd.flood_x is not None:
        fx = tx(cd.flood_x)
        dashed_line(d, (fx, CHAIN_TOP - 10), (fx, axis_y), SAND_DIM, 1)
        d.text((fx - 6, axis_y - 12), "the Flood", font=F_SMALL,
               fill=TEXT, anchor="rm")

    def bar_label(i, x_end, bright, beside=False):
        # beside=True sets the label right of the bar end, clear of the
        # "taken" chevrons that otherwise print on top of it (Enoch).
        span = cd.deaths[i] - cd.births[i]
        xy = (x_end + 12, node_y(i) - 15) if beside \
            else (x_end, node_y(i) - 15)
        d.text(xy, str(span), font=F_NUM,
               fill=HL if bright else TEXT, anchor="lm" if beside else "mm")

    def death_cap(i, x, col):
        y = node_y(i)
        d.line([(x, y - BAR_H - 2), (x, y + BAR_H + 2)], fill=col, width=2)

    def taken_mark(i, x):
        y = node_y(i)
        for k in range(3):
            yy = y - 10 - k * 7
            d.line([(x - 5, yy + 4), (x, yy - 2), (x + 5, yy + 4)],
                   fill=HL, width=2)

    for i, key in enumerate(keys):
        y = node_y(i)
        b = cd.births[i]
        dth = cd.deaths[i]
        born = verse >= cd.birth_verse(i)
        done = cd.done_verses[i] is not None and verse > cd.done_verses[i]
        current = (i == focus)

        if current and stage != "intro":
            xb = tx(b)
            if stage == "fathered":
                # build from birth up to the son
                focus_bar(od, xb, y, xb, tx(b + cd.ages[i]), grow,
                          HL + (110,), g(0.95))
                if grow > 0.92 and i + 1 < len(keys):
                    cy = node_y(i + 1)
                    d.ellipse([tx(b + cd.ages[i]) - 3, cy - 3,
                               tx(b + cd.ages[i]) + 3, cy + 3],
                              outline=HL, width=2)
            elif stage == "named" or (stage == "narr" and dth is None
                                      and cd.ages[i]):
                # birth-to-son bar, shown complete (no growth)
                xson = tx(b + cd.ages[i])
                focus_bar(od, xb, y, xson, xson, grow, HL + (110,), g(0.95))
            elif stage == "narr" and cd.ages[i] is None:
                od.ellipse([xb - 4, y - 4, xb + 4, y + 4],
                           outline=g(0.95), width=2)
            elif stage == "narr" and done:
                focus_bar(od, xb, y, tx(dth), tx(dth), grow,
                          HL + (90,), g(0.9))
                bar_label(i, tx(dth), True)
            elif stage == "narr":
                xson = tx(b + (cd.ages[i] or 0))
                focus_bar(od, xb, y, xson, xson, grow, HL + (110,), g(0.95))
            elif stage == "after":
                # continue from the son onward — do NOT restart at birth
                mid = b + cd.ages[i]
                end = dth if dth is not None else mid
                focus_bar(od, xb, y, tx(mid), tx(end), grow,
                          HL + (110,), g(0.95))
                bar_label(i, tx(end), True)
            elif stage in ("total", "taken"):
                # the completed life, shown whole (no growth)
                focus_bar(od, xb, y, tx(dth), tx(dth), grow,
                          HL + (110,), g(0.95))
                bar_label(i, tx(dth), True, beside=(stage == "taken"))
                if stage == "taken":
                    taken_mark(i, tx(dth))
                else:
                    death_cap(i, tx(dth), HL)
            elif stage == "trio":
                # build from birth up to the son (Noah's line branches on)
                focus_bar(od, xb, y, xb, tx(b + cd.ages[i]), grow,
                          HL + (110,), g(0.95))
                dashed_line(d, (tx(b + cd.ages[i]) + 4, y),
                            (TL_X1, y), SAND_DIM, 1)
            continue

        if done and dth is not None:
            d.rectangle([tx(b), y - BAR_H, tx(dth), y + BAR_H],
                        outline=SAND, width=2)
            bar_label(i, tx(dth), False, beside=(i == cd.taken_index))
            if i == cd.taken_index:
                taken_mark(i, tx(dth))
            else:
                death_cap(i, tx(dth), SAND)
        elif (born and cd.ages[i] is not None
              and cd.fathered_verses[i] is not None
              and verse >= cd.fathered_verses[i]):
            # What has already been drawn stays drawn. Terah is named at
            # 11:26 and not buried until 11:32, and in between the focus
            # moves to Abram — so his bar used to appear, vanish for 11:29
            # and 11:30, then come back, which reads as a glitch rather than
            # as a life. Everyone else goes straight from focus to done, so
            # this branch changes nothing for them.
            d.rectangle([tx(b), y - BAR_H, tx(b + cd.ages[i]), y + BAR_H],
                        outline=SAND_DIM, width=2)
        elif born:
            xb = tx(b)
            d.ellipse([xb - 3, y - 3, xb + 3, y + 3], outline=SAND_DIM,
                      width=2)

    d.text((28, H - 26), "years as given in the text", font=F_SMALL,
           fill=TEXT_DIM)


if __name__ == "__main__":
    codes = [code for code, *_ in TRANSLATIONS]
    resolved = {}
    for code in codes:
        try:
            g5 = resolve_names(code, 5, G5_KEYS)
            time.sleep(2.5)
            g11 = resolve_names(code, 11, G11_KEYS)
            time.sleep(2.5)
        except PassageError as e:
            # e.g. OEB has no Old Testament — that translation simply
            # falls back to the generic files at runtime.
            print(f"{code}: chapters unavailable ({e}) — skipped")
            continue
        resolved[code] = {5: g5, 11: g11}
        print(f"{code}: Gen5 {g5['Enosh']}/{g5['Kenan']}/{g5['Methuselah']}"
              f" · Gen11 {g11['Arpachshad']}/{g11['Shelah']}/{g11['Terah']}")

    generic = resolved["WEB"]
    grand_files = grand_bytes = 0
    for chapter in (5, 11):
        n_files, n_bytes = render_chapter(chapter, generic[chapter], "")
        grand_files += n_files
        grand_bytes += n_bytes
        print(f"Genesis {chapter} generic: {n_files} files")
        for code in codes:
            if code == "WEB" or code not in resolved:
                continue
            if resolved[code][chapter] == generic[chapter]:
                print(f"  {code}: matches generic spellings — skipped")
                continue
            n_files, n_bytes = render_chapter(chapter,
                                              resolved[code][chapter],
                                              f".{code}")
            grand_files += n_files
            grand_bytes += n_bytes
            print(f"  {code}: {n_files} translation-specific files")
    print(f"TOTAL: {grand_files} files, {grand_bytes/1e6:.1f} MB")
