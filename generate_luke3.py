"""Generate per-verse animations for the genealogy of Jesus, Luke 3:23-38.

Luke runs the line BACKWARD — from Jesus through David and Abraham all the
way to Adam, "the son of God." The visual is a taproot: the whole line is
one root running straight down from a tree at the surface (Jesus), and the
camera descends it as the chapter is read — a bright marker rides the root
tip while the soil and the names slide past. Each era is its own stratum of
earth (the kings, the patriarchs, the pre-flood fathers, bedrock at Adam),
so the ground itself says how deep in time the line has gone; at the very
bottom the soil gives way to light around "of God." Era landmarks (Jesus,
David, Abraham, Noah, Adam, God) get bold names and an era word, and a slim
depth gauge on the right shows the whole root with a "generation N of M"
counter. John's own image — the axe laid at the root of the trees (v9) —
is what verse 23 descends into.

Because each verse's animation ends with the camera resting on that verse's
last name, and the next verse begins there, the chapter plays as one
continuous descent.

(The previous designs are preserved: the straight-road tracking camera in
backups/luke3_road/, the "whole serpentine path at once" original in
backups/luke3_journey/ — copy one back to revert. Concept mocks for the
designs that were considered are in mockups/luke3/ + LUKE3_IDEAS.md.)

Names are extracted directly from each translation's own verse text —
"the son of X" / "of X" phrasing where present (WEB, KJV, ...), with a
comma-list fallback for translations that print the names bare (OEB).
Translation-suffixed files are emitted only where the extracted names
differ from the generic (WEB) set. Animations play once, slowly, then
hold (loop=1) — no flashing.

Run inside the project venv:  .venv\\Scripts\\python.exe generate_luke3.py
"""

import math
import os
import re
import time


from generate_tabernacle import (W, H, BG, SAND, SAND_DIM, TEXT, TEXT_DIM,
                                 HL, F_SMALL, F_TITLE, font, ease, g,
                                 out_path)
from generate_genealogy import G_FRAMES, G_FRAME_MS
from passages import fetch_passage, PassageError, TRANSLATIONS

F_ROOT = font(18)                  # names along the root
F_ROOT_B = font(18, bold=True)     # era landmarks
F_ERA = font(13, italic=True)

SON_OF = re.compile(r"of\s+([A-Z][A-Za-z]+)")
NAME_TOKEN = re.compile(r"^[A-Z][a-z]+$")
NOT_NAMES = {"He", "When", "The", "And", "His", "Now", "This"}

# era landmarks along the root, with spellings seen across translations;
# "Jesus" anchors only at the head of the line — ASV/DRA name an ancestor
# Jesus in v29 who is no landmark.
ERA_WORDS = [
    ({"Jesus"}, "the Christ"),
    ({"David"}, "the king"),
    ({"Abraham"}, "the patriarchs"),
    ({"Noah", "Noe"}, "the flood"),
    ({"Adam"}, "the first man"),
    ({"God"}, "in the beginning"),
]


def era_of(name, idx):
    for variants, era in ERA_WORDS:
        if name in variants and (name != "Jesus" or idx == 0):
            return era
    return None


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def _names_son_of(text):
    return SON_OF.findall(text)


def _names_from_list(text):
    """Names printed as a bare comma list (OEB): 'Mattith, Levi, Melchiah,'"""
    text = text.replace(" the son of ", ", ")
    text = re.sub(r"\band\b", ",", text)
    out = []
    for part in re.split(r"[,—;]", text):
        w = part.strip(" .:'\"”“’")
        if NAME_TOKEN.match(w) and w not in NOT_NAMES:
            out.append(w)
    return out


def _parse(verses, parser):
    out = {}
    for v in range(23, 39):
        names = parser(verses.get(v, ""))
        if v == 23:
            # exclude the subject ("Jesus himself...") — but ONLY here:
            # some translations (ASV, DRA) name an ancestor "Jesus" in v29.
            names = [n for n in names if n != "Jesus"]
        if not (1 <= len(names) <= 8):
            raise ValueError(f"Luke 3:{v}: extracted {names}")
        out[v] = names
    total = sum(len(n) for n in out.values())
    if not 70 <= total <= 85:
        raise ValueError(f"{total} names extracted — unexpected")
    for must in ("David", "Abraham", "Adam", "God"):
        if not any(must in batch for batch in out.values()):
            raise ValueError(f"{must} missing from extraction")
    return out


def extract_line(code):
    """{verse: [names...]} for Luke 3:23-38, from the translation's text."""
    for attempt in range(2):
        try:
            p = fetch_passage("", "Luke", 3, code)
            break
        except PassageError as e:
            if attempt == 0 and "rate limit" in str(e).lower():
                time.sleep(32)
            else:
                raise
    verses = dict(p.verses)
    errors = []
    for parser in (_names_son_of, _names_from_list):
        try:
            return _parse(verses, parser)
        except ValueError as e:
            errors.append(str(e))
    raise ValueError(f"{code}: no parser matched ({errors[0]})")


def build_grid(line):
    """-> (slots [(name, verse)], per-verse (start,end) slot ranges)"""
    slots = [("Jesus", 23)]
    ranges = {}
    for v in range(23, 39):
        start = len(slots) if v != 23 else 0
        for name in line[v]:
            slots.append((name, v))
        ranges[v] = (start, len(slots))
    return slots, ranges


# ---------------------------------------------------------------------------
# Layout: a taproot under a descending camera
# ---------------------------------------------------------------------------

CY = 300                            # camera: the root tip rests here
SPACING = 64                        # px between generations at root zoom
ROOT_AMP, ROOT_FREQ = 60, 0.7       # the root's side-to-side wander
SURFACE = -0.7 * SPACING            # root-space y of ground level
TOP_STRIP, BOT_STRIP = 64, 538      # screen bands kept clear for title/footer
GA_X, GA_Y0, GA_Y1 = 966, 96, 512   # the depth gauge at the right edge
V23_LIFT = 2.8 * SPACING            # v23 starts up in the tree, then plunges

# soil tones, one per era band (Jesus->David, ->Abraham, ->Noah, ->Adam,
# then bedrock below Adam) — each deeper stratum a little darker
STRATA = [(33, 29, 24), (40, 32, 23), (31, 28, 33), (27, 26, 20),
          (24, 23, 27)]
STRATA_LINE = (66, 56, 42)


def root_x(s):
    """Root-space x of the taproot at generation s (float)."""
    return W // 2 + ROOT_AMP * math.sin(s * ROOT_FREQ)


# the tree at the surface: a small self-similar fractal — every branch forks
# into two shorter ones, slightly asymmetric so it reads as grown, not drawn
TREE_DEPTH = 7
TREE_RATIO = 0.72
TREE_SPLIT_L, TREE_SPLIT_R = 0.63, 0.55      # radians off the parent
TREE_W = [14, 9, 6, 4, 2.6, 1.8, 1.2]        # stroke width per depth


def tree_segments():
    """[(x0, y0, x1, y1, depth)] relative to the trunk base at the surface,
    y negative = up. Deterministic, shared by the raster and SVG surfaces."""
    segs = []

    def grow(x, y, ang, length, depth):
        nx = x + length * math.sin(ang)
        ny = y - length * math.cos(ang)
        segs.append((x, y, nx, ny, depth))
        if depth + 1 < TREE_DEPTH:
            grow(nx, ny, ang - TREE_SPLIT_L, length * TREE_RATIO, depth + 1)
            grow(nx, ny, ang + TREE_SPLIT_R, length * TREE_RATIO, depth + 1)

    grow(0.0, 0.0, 0.0, 115, 0)
    return segs


def strata_bands(slots):
    """[(top_px, bottom_px, tone)] in root space; bottom None = bedrock."""
    n = len(slots)
    marks = [i for i in range(n) if era_of(slots[i][0], i)]
    # a boundary sits just below each landmark: David closes the first age...
    cuts = [(m + 0.5) * SPACING for m in marks[1:-1]]   # David..Adam
    bands, top = [], SURFACE
    for k, cut in enumerate(cuts):
        bands.append((top, cut, STRATA[k]))
        top = cut
    bands.append((top, None, STRATA[len(cuts)]))
    return bands


def root_points(s0, s1, ys, step=0.25):
    """Screen polyline tracing the root from generation s0 to s1."""
    pts, s = [], s0
    while s < s1:
        pts.append((root_x(s), ys(s * SPACING)))
        s += step
    pts.append((root_x(s1), ys(s1 * SPACING)))
    return pts


def draw_tree(d, ys):
    """Ground level and the tree whose root this is (verse 23's opening)."""
    gy = ys(SURFACE)
    if gy < -40:
        return
    xt = root_x(SURFACE / SPACING)      # trunk grows where the root emerges
    d.line([(0, gy), (W, gy)], fill=SAND, width=3)
    for tx in range(60, W, 90):                     # sparse grass ticks
        if abs(tx - xt) > 60:
            d.line([(tx, gy - 5), (tx + 6, gy - 12)], fill=SAND_DIM, width=2)
    for x0, y0, x1, y1, depth in tree_segments():
        d.line([(xt + x0, gy + y0), (xt + x1, gy + y1)], fill=SAND,
               width=max(1, round(TREE_W[depth])))


def draw_glow(od, cx, cy):
    """The soil gives way to light around 'of God' at the root's end."""
    for r, a in ((130, 16), (104, 26), (80, 38), (58, 54), (40, 74),
                 (26, 96)):
        od.ellipse([cx - r, cy - r, cx + r, cy + r], fill=HL + (a,))


# The WebP rendering that used to live here has been removed: the app reads
# the SVGs natively, so the raster path was building animated images nobody
# ever fetched. What remains is what this file is actually for — Luke 3's
# name extraction, its grid, and the root/strata geometry that
# generate_luke3_svg.py imports and draws.

if __name__ == "__main__":
    codes = [code for code, *_ in TRANSLATIONS]
    resolved = {}
    for code in codes:
        try:
            resolved[code] = extract_line(code)
            total = sum(len(v) for v in resolved[code].values()) + 1
            print(f"{code}: {total} names · v24 = "
                  + ", ".join(resolved[code][24]))
        except (ValueError, PassageError) as e:
            print(f"{code}: extraction failed ({e}) — will use generic")
            resolved[code] = None
        time.sleep(2.5)

    generic = resolved["WEB"]
    if generic is None:
        raise SystemExit("WEB extraction failed; cannot build generic set")
    grand_files, grand_bytes = render_chapter(generic, "")
    print(f"Luke 3 generic: {grand_files} files")
    for code in codes:
        if code == "WEB" or resolved[code] is None:
            continue
        if resolved[code] == generic:
            print(f"  {code}: matches generic — skipped")
            continue
        n_files, n_bytes = render_chapter(resolved[code], f".{code}")
        grand_files += n_files
        grand_bytes += n_bytes
        print(f"  {code}: {n_files} translation-specific files")
    print(f"TOTAL: {grand_files} files, {grand_bytes/1e6:.1f} MB")
