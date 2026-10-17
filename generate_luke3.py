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

Names are extracted directly from WEB's verse text (WEB is the only text,
passages.TRANSLATION) — its "the son of X, of Y" phrasing. Animations play
once, slowly, then hold (loop=1) — no flashing.

This module holds the extraction, the grid and the root geometry;
generate_luke3_svg.py renders the files:
    .venv\\Scripts\\python.exe generate_luke3_svg.py
"""

import math
import os
import re


from generate_tabernacle import (W, H, BG, TEXT, TEXT_DIM,
                                 F_SMALL, F_TITLE, font, ease, g,
                                 out_path)
from generate_genealogy import G_FRAMES, G_FRAME_MS
from passages import load_chapter

F_ROOT = font(18)                  # names along the root
F_ROOT_B = font(18, bold=True)     # era landmarks
F_ERA = font(13, italic=True)

SON_OF = re.compile(r"of\s+([A-Z][A-Za-z]+)")

# era landmarks along the root; "Jesus" anchors only at the head of the line
ERA_WORDS = [
    ("Jesus", "the Christ"),
    ("David", "the king"),
    ("Abraham", "the patriarchs"),
    ("Noah", "the flood"),
    ("Adam", "the first man"),
    ("God", "in the beginning"),
]


def era_of(name, idx):
    for word, era in ERA_WORDS:
        if name == word and (name != "Jesus" or idx == 0):
            return era
    return None


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def _parse(verses):
    out = {}
    for v in range(23, 39):
        names = SON_OF.findall(verses.get(v, ""))
        if v == 23:
            # exclude the subject ("Jesus himself...") — build_grid puts him
            # at the head of the line
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


def extract_line():
    """{verse: [names...]} for Luke 3:23-38, from WEB's text."""
    return _parse(dict(load_chapter("Luke", 3).verses))


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
