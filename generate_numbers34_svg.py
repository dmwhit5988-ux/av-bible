"""Render Numbers 34 as per-verse vector SVGs (the held final frame of the
existing animated WebP maps).

Reuses the hand-tuned geometry, border segments, tribal territories, captions
and side-panel copy from generate_tribal_maps.py — only the drawing backend
changes, from PIL raster frames to a single static SvgCanvas per verse. The
result is a crisp, hand-editable vector that scales to any screen (see the
web app's new .svg support) and is far smaller than the 24-frame WebP.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_numbers34_svg.py
"""

import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, SAND, SAND_DIM, TEXT, TEXT_DIM, HL,
                                 out_path)
from generate_tribal_maps import (
    MapFrame, ANCHORS, PANEL_X, FOOTER,
    LAND_POLY, COAST, LAKES, JORDAN_UP, JORDAN_LOW, ARNON, JABBOK, YARMOUK,
    BORDER_SEGS, CANAAN_POLY, LANDMARKS34,
    TRIBES, WEST_TRIBES, EAST_TRIBES, TRIBE_COL, PRINCES,
    CAPTIONS_34A, CAPTIONS_34B, PANEL_34A,
    SEA, LAND, RIVER, WATER_TXT,
)

DASH = "6,5"          # dashed border underlay (future segments)


def g(alpha):
    return HL + (int(255 * alpha),)


# ---------------------------------------------------------------------------
# Shared drawing helpers (SVG re-implementations of the raster ones)
# ---------------------------------------------------------------------------

def draw_base(c, fr):
    """Sea already fills the map window; add land, coast, lakes, rivers."""
    c.polygon(fr.pts(LAND_POLY), fill=LAND)
    c.polyline(fr.pts(COAST), stroke=SAND_DIM, width=2)
    for lake in LAKES:
        c.polygon(fr.pts(lake), fill=SEA, stroke=SAND_DIM)
    for rv in (JORDAN_UP, JORDAN_LOW, ARNON, JABBOK, YARMOUK):
        c.polyline(fr.pts(rv), stroke=RIVER, width=2)


def redraw_lakes(c, fr):
    for lake in LAKES:
        c.polygon(fr.pts(lake), fill=SEA + (255,), stroke=SAND_DIM + (255,))


def label_dot(c, xy, name, place, fill, size, dot, bold=False, italic=False,
              unc=False, leader=False, r=3):
    x, y = xy
    if dot:
        c.circle(x, y, r, stroke=dot, width=2)
    dx, dy, anch = ANCHORS[place] if isinstance(place, str) else place
    if leader:
        lx, ly = x + dx * 0.75, y + dy * 0.75
        c.line((x + (2 if dx >= 0 else -2), y - 3), (lx, ly),
               stroke=SAND_DIM, width=1)
    txt = name + " ?" if unc else name
    c.text((x + dx, y + dy), txt, size, fill, anch, bold=bold, italic=italic)


def compass_scale(c, fr):
    x, y = fr.mw - 24, fr.mh - 62
    c.line((x, y + 22), (x, y), TEXT_DIM, 2)
    c.line((x - 5, y + 8), (x, y), TEXT_DIM, 2)
    c.line((x + 5, y + 8), (x, y), TEXT_DIM, 2)
    c.text((x - 10, y + 2), "N", 14, TEXT_DIM, "rm")
    bar = 50 * fr.s / 111.0
    bx, by = fr.mw - 16 - bar, fr.mh - 16
    c.line((bx, by), (bx + bar, by), TEXT_DIM, 2)
    c.line((bx, by - 3), (bx, by + 3), TEXT_DIM, 2)
    c.line((bx + bar, by - 3), (bx + bar, by + 3), TEXT_DIM, 2)
    c.text((bx + bar / 2, by - 6), "50 km", 14, TEXT_DIM, "mb", italic=True)


def map_border(c, fr):
    c.rect(fr.px - 1, fr.py - 1, fr.mw + 1, fr.mh + 1, stroke=SAND_DIM,
           width=1)


def panel_lines(c, x, y, lines, gap=22):
    for ln in lines:
        dimmed = ln.startswith(" ")
        c.text((x, y), ln.strip(), 14 if dimmed else 15,
               TEXT_DIM if dimmed else TEXT, "la", italic=dimmed)
        y += gap
    return y


def canvas(title, verse, caption):
    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 18), title, 24, TEXT, "la", bold=True)
    c.text((28, 52), f"verse {verse} — {caption}", 18, HL, "la", italic=True)
    c.text((PANEL_X, H - 40), FOOTER, 14, TEXT_DIM, "la", italic=True)
    return c


# ---------------------------------------------------------------------------
# vv1-15 — tracing the border of Greater Canaan
# ---------------------------------------------------------------------------

def draw_wide(c, verse):
    fr = MapFrame(29.7, 35.0, 33.3, 37.9, (36, 86, 410, 556))
    with c.group(fr.px, fr.py, clip=(fr.mw, fr.mh)):
        c.rect(0, 0, fr.mw, fr.mh, fill=SEA)
        draw_base(c, fr)

        if verse >= 2:
            c.polygon(fr.pts(CANAAN_POLY), fill=HL + (16,))
        if verse in (14, 15):
            for key in EAST_TRIBES:
                c.polygon(fr.pts(TRIBES[key][1]), fill=TRIBE_COL[key] + (80,))
        redraw_lakes(c, fr)

        for v, seg in BORDER_SEGS:
            pts = fr.pts(seg)
            if verse > v or verse >= 13:
                c.polyline(pts, stroke=SAND + (255,), width=3)
            elif verse == v:
                # the border of this verse traces itself over a dashed underlay
                c.polyline(pts, stroke=SAND_DIM + (255,), width=1, dash=DASH)
                c.traced(pts, stroke=g(0.95), width=4, dur="2.6s")
            else:
                c.polyline(pts, stroke=SAND_DIM + (255,), width=1, dash=DASH)

        # text pass
        c.text(fr.pt(32.90, 34.15), "The Great Sea", 14, WATER_TXT, "mm",
               italic=True)
        c.text(fr.pt(31.22, 35.66), "Salt Sea", 14, WATER_TXT, "lm",
               italic=True)
        c.text(fr.pt(32.82, 35.72), "Chinnereth", 14, WATER_TXT, "lm",
               italic=True)
        c.text(fr.pt(30.50, 35.80), "EDOM", 14, TEXT_DIM, "mm")
        c.text(fr.pt(30.05, 34.60), "wilderness of Zin", 14, TEXT_DIM, "mm",
               italic=True)
        label_dot(c, fr.pt(33.51, 36.29), "Damascus", "r", TEXT_DIM, 14,
                  SAND_DIM, italic=True)
        label_dot(c, fr.pt(31.78, 35.23), "Jerusalem", "l", TEXT_DIM, 14,
                  SAND_DIM, italic=True)
        if verse >= 5:
            c.text(fr.pt(30.55, 33.42), "Brook of Egypt", 14,
                   TEXT if verse == 5 else TEXT_DIM, "lm", italic=True)

        for name, la, lo, v0, place, leader, unc in LANDMARKS34:
            if verse < v0:
                continue
            cur = (verse == v0)
            label_dot(c, fr.pt(la, lo), name, place,
                      HL if cur else TEXT, 14, HL if cur else SAND,
                      bold=cur, unc=unc, leader=leader)

        compass_scale(c, fr)
    map_border(c, fr)


# ---------------------------------------------------------------------------
# vv16-29 — the allotment, tribe by tribe
# ---------------------------------------------------------------------------

def draw_zoom(c, verse):
    fr = MapFrame(30.5, 33.5, 34.2, 36.7, (36, 86, 410, 556))
    focus = PRINCES.get(verse)
    focus_key = focus[0] if focus else None
    labels, dim_lines, outlines = [], [], []

    with c.group(fr.px, fr.py, clip=(fr.mw, fr.mh)):
        c.rect(0, 0, fr.mw, fr.mh, fill=SEA)
        draw_base(c, fr)

        for key in WEST_TRIBES + EAST_TRIBES:
            label, poly, lab = TRIBES[key]
            east = key in EAST_TRIBES
            cur = (key == focus_key or (verse == 23 and key == "MANASSEH_E"))
            done = verse == 29 and not east
            ring = fr.pts(poly + poly[:1])
            if cur:
                # the focus tribe's territory grows in, its border traces round
                c.grown(fr.pts(poly), TRIBE_COL[key], 60 / 255, 150 / 255,
                        dur="2.6s")
                outlines.append(ring)
                labels.append((fr.pt(*lab), label, True, HL))
            else:
                c.polygon(fr.pts(poly),
                          fill=TRIBE_COL[key] + (26 if east else 42,))
                dim_lines.append((ring, (SAND if done else SAND_DIM) + (255,)))
                fill = TEXT if done else (TEXT_DIM if east else TEXT)
                labels.append((fr.pt(*lab), label, done, fill))

        redraw_lakes(c, fr)
        for pts, col in dim_lines:
            c.polyline(pts, stroke=col, width=1)
        for pts in outlines:
            c.traced(pts, stroke=g(0.95), width=3, dur="2.6s")

        # text pass
        for xy, label, bold, fill in labels:
            c.text(xy, label, 14, fill, "mm", bold=bold)
        c.text(fr.pt(32.08, 34.60), "The Great Sea", 14, WATER_TXT, "mm",
               italic=True)
        c.text(fr.pt(30.95, 35.62), "Salt Sea", 14, WATER_TXT, "lm",
               italic=True)
        compass_scale(c, fr)
    map_border(c, fr)


# ---------------------------------------------------------------------------
# Verse assembly
# ---------------------------------------------------------------------------

def render_34(verse):
    if verse <= 15:
        c = canvas("The Borders of the Land — Numbers 34", verse,
                   CAPTIONS_34A[verse])
        draw_wide(c, verse)
        lines = PANEL_34A.get(verse)
        if lines:
            c.text((PANEL_X, 120), "the ancient landmarks", 14, TEXT_DIM,
                   "la", bold=True)
            panel_lines(c, PANEL_X, 150, lines)
        return c

    focus = PRINCES.get(verse)
    if focus:
        caption = f"for the tribe of {TRIBES[focus[0]][0]}: {focus[1]}"
    else:
        caption = CAPTIONS_34B[verse]
    c = canvas("Dividing the Inheritance — Numbers 34", verse, caption)
    draw_zoom(c, verse)
    if focus:
        c.text((PANEL_X, 130), TRIBES[focus[0]][0], 30, HL, "la", bold=True)
        c.text((PANEL_X, 176), f"prince: {focus[1]}", 15, TEXT, "la")
        panel_lines(c, PANEL_X, 212, focus[2])
        c.text((PANEL_X, 330), "territory as described in Joshua 13-19", 14,
               TEXT_DIM, "la", italic=True)
        c.text((PANEL_X, 352), "Reuben, Gad, half-Manasseh: already", 14,
               TEXT_DIM, "la", italic=True)
        c.text((PANEL_X, 372), "settled east of the Jordan (Num 32)", 14,
               TEXT_DIM, "la", italic=True)
    elif verse == 17:
        panel_lines(c, PANEL_X, 130,
                    ["Eleazar casts the lots;", "Joshua leads the conquest",
                     "", " the division itself is told", " in Joshua 13-19"])
    elif verse == 18:
        panel_lines(c, PANEL_X, 130,
                    ["ten princes for ten tribes —", "Levi receives cities,",
                     "not territory (Num 35)"])
    return c


def main():
    total = 0
    for verse in range(1, 30):
        c = render_34(verse)
        out = out_path("Numbers", 34, f"Numbers_34_{verse}.svg")
        c.save(out)
        total += os.path.getsize(out)
    print(f"Numbers 34: 29 SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
