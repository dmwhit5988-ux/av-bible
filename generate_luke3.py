"""Generate per-verse animations for the genealogy of Jesus, Luke 3:23-38.

Luke runs the line BACKWARD — from Jesus through David and Abraham all the
way to Adam, "the son of God." The visual is a slow tracking camera: the
whole line is one long road, and the camera dollies along it as the chapter
is read — a bright marker stays centered while the road and the names slide
past, each generation's name written large beside its milestone. Era
landmarks (Jesus, David, Abraham, Noah, Adam, God) get bold names and an
era word. A minimap along the bottom shows the whole road, the landmarks,
and how far back the line has traveled, with a "generation N of M" counter.

Because each verse's animation ends with the camera resting on that verse's
last name, and the next verse begins there, the chapter plays as one
continuous journey.

(The previous "whole serpentine path at once" design is preserved in
backups/luke3_journey/ — copy it back to revert.)

Names are extracted directly from each translation's own verse text —
"the son of X" / "of X" phrasing where present (WEB, KJV, ...), with a
comma-list fallback for translations that print the names bare (OEB).
Translation-suffixed files are emitted only where the extracted names
differ from the generic (WEB) set. Animations play once, slowly, then
hold (loop=1) — no flashing.

Run inside the project venv:  .venv\\Scripts\\python.exe generate_luke3.py
"""

import os
import re
import time

from PIL import Image, ImageDraw

from generate_tabernacle import (W, H, BG, SAND, SAND_DIM, TEXT, TEXT_DIM,
                                 HL, F_SMALL, F_VERSE, F_TITLE, font, ease,
                                 g, out_path)
from generate_genealogy import G_FRAMES, G_FRAME_MS
from passages import fetch_passage, PassageError, TRANSLATIONS

F_ROAD = font(18)                  # names along the road
F_ROAD_B = font(18, bold=True)     # era landmarks
F_ERA = font(13, italic=True)

SON_OF = re.compile(r"of\s+([A-Z][A-Za-z]+)")
NAME_TOKEN = re.compile(r"^[A-Z][a-z]+$")
NOT_NAMES = {"He", "When", "The", "And", "His", "Now", "This"}

# era landmarks along the road, with spellings seen across translations;
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
# Layout: an unrolled road under a tracking camera
# ---------------------------------------------------------------------------

ROAD_Y = 320
SPACING = 92                        # px between generations at road zoom
MINI_X0, MINI_X1, MINI_Y = 64, 960, 508


def draw_frame(verse, slots, ranges, t):
    grow = ease(min(1.0, t / 0.92))
    n = len(slots)
    start, end = ranges[verse]
    batch_names = [slots[i][0] for i in range(start, end)
                   if slots[i][0] != "Jesus"]
    if verse == 23:
        caption = "the son (as was supposed) of " + ", of ".join(batch_names)
    elif verse == 38:
        caption = "… of " + ", of ".join(batch_names[:-1]) + \
                  f", the son of {batch_names[-1]}"
    else:
        caption = "the son of " + ", of ".join(batch_names)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    d.text((28, 20), "From Jesus back to Adam — Luke 3", font=F_TITLE,
           fill=TEXT)
    d.text((28, 52), f"verse {verse} — {caption[:92]}", font=F_VERSE,
           fill=HL)

    # the camera rides the sweep tip: the marker stays centered while the
    # road slides past, from the previous verse's resting point to this
    # verse's last name — so the chapter plays as one continuous journey
    prev = max(start - 1, 0)
    tip_s = (prev + (end - 1 - prev) * grow) * SPACING

    def sx(s):
        return W // 2 + s - tip_s

    def clamp(x):
        return max(-60, min(W + 60, x))

    # road: dim ahead, plain behind, bright sweep for this verse
    d.line([(clamp(sx(0)), ROAD_Y), (clamp(sx((n - 1) * SPACING)), ROAD_Y)],
           fill=SAND_DIM, width=3)
    if sx(prev * SPACING) > -60:
        d.line([(clamp(sx(0)), ROAD_Y), (clamp(sx(prev * SPACING)), ROAD_Y)],
               fill=SAND, width=3)
    od.line([(clamp(sx(prev * SPACING)), ROAD_Y), (W // 2, ROAD_Y)],
            fill=g(0.95), width=5)

    for i, (name, _v) in enumerate(slots):
        x = sx(i * SPACING)
        if x < -140 or x > W + 140:
            continue
        era = era_of(name, i)
        passed = i * SPACING <= tip_s + 1
        cur = start <= i < end
        read = i < start
        r = 7 if era else 5
        d.ellipse([x - r, ROAD_Y - r, x + r, ROAD_Y + r],
                  outline=SAND if (read or (cur and passed)) else SAND_DIM,
                  width=2)
        if cur and passed:
            fill = HL
        elif read:
            fill = TEXT
        else:
            fill = TEXT_DIM
        above = (i % 2 == 0)
        ny = ROAD_Y - 46 if above else ROAD_Y + 46
        ey = ROAD_Y - 24 if above else ROAD_Y + 24
        d.text((x, ny), name, font=F_ROAD_B if era else F_ROAD,
               fill=fill, anchor="mm")
        if era:
            d.text((x, ey), era, font=F_ERA, fill=TEXT_DIM, anchor="mm")

    # the traveler: a steady ring at the center of the view
    od.ellipse([W // 2 - 10, ROAD_Y - 10, W // 2 + 10, ROAD_Y + 10],
               outline=g(1.0), width=3)

    # ---- minimap: the whole road at a glance ----
    span = (n - 1) * SPACING

    def mx(s):
        return MINI_X0 + (MINI_X1 - MINI_X0) * s / span

    d.line([(MINI_X0, MINI_Y), (MINI_X1, MINI_Y)], fill=SAND_DIM, width=2)
    d.line([(MINI_X0, MINI_Y), (mx(tip_s), MINI_Y)], fill=SAND, width=2)
    for i, (name, _v) in enumerate(slots):
        era = era_of(name, i)
        if not era:
            continue
        x = mx(i * SPACING)
        d.line([(x, MINI_Y - 4), (x, MINI_Y + 4)], fill=SAND, width=2)
        ly = MINI_Y - 14 if name == "Adam" else MINI_Y + 14
        d.text((x, ly), name, font=F_ERA, fill=TEXT_DIM, anchor="mm")
    od.ellipse([mx(tip_s) - 4, MINI_Y - 4, mx(tip_s) + 4, MINI_Y + 4],
               fill=g(1.0))

    if end >= n:
        counter = f"all {n - 1} generations — back to the beginning"
    else:
        counter = f"generation {end - 1} of {n - 1}"
    d.text((W - 28, H - 26), counter, font=F_SMALL, fill=TEXT, anchor="ra")

    d.text((28, H - 26),
           "Luke traces the line backward — from Jesus to Adam, "
           "“the son of God”", font=F_SMALL, fill=TEXT_DIM)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def render_chapter(line, suffix):
    slots, ranges = build_grid(line)
    total_bytes = 0
    for verse in sorted(ranges):
        frames = [draw_frame(verse, slots, ranges, i / (G_FRAMES - 1))
                  for i in range(G_FRAMES)]
        out = out_path("Luke", 3, f"Luke_3_{verse}{suffix}.webp")
        frames[0].save(out, save_all=True, append_images=frames[1:],
                       duration=G_FRAME_MS, loop=1, quality=82, method=4)
        total_bytes += os.path.getsize(out)
    return len(ranges), total_bytes


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
