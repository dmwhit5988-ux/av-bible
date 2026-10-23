"""Render Numbers 32 as per-verse vector SVGs: the Transjordan map.

Each verse has a stage in generate_tribal_maps.SPECS_32 (survey, rebuke,
pledge, grant, build, machir, jair, nobah ...) that picks what the map
highlights. Regions and kingdoms trace their borders with SvgCanvas.traced
(draw once, then hold), and the city-building verses list each city with its
modern identification in the side panel.

The geometry, city coordinates and spec table come from
generate_tribal_maps.py, which Numbers 34 draws from too.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_numbers32_svg.py
"""

import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, SAND_DIM, TEXT, TEXT_DIM, HL,
                                 out_path)
from generate_tribal_maps import (
    MapFrame, ANCHORS, PANEL_X, RIVER, RIVER_DIM, SEA, LAND, WATER_TXT,
    LAND_POLY, COAST, LAKES, JORDAN_UP, JORDAN_LOW, ARNON, JABBOK, YARMOUK,
    JAZER_GILEAD, SIHON_POLY, OG_POLY, N_GILEAD, HAVVOTH_JAIR,
    TRIBES, TRIBE_COL, CITIES32, V3_CITIES, BUILD_VERSES, SPECS_32,
)
from passages import verse_numbers

DUR = "2.6s"


def g(alpha):
    return HL + (int(255 * alpha),)


# ---------------------------------------------------------------------------
# Map helpers
# ---------------------------------------------------------------------------

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


def canvas(title, verse, caption):
    # (no caption line or footer: the verse is narrated aloud — the map and
    # its place names carry the graphic; SPECS_32 still holds `caption` data)
    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 18), title, 24, TEXT, "la", bold=True)
    return c


def draw_base(c, fr, dim=False):
    """Sea already fills the window; add land, coast, lakes, rivers.
    `dim` mutes the rivers for the rebuke verses (Canaan still waits)."""
    c.polygon(fr.pts(LAND_POLY), fill=LAND)
    c.polyline(fr.pts(COAST), stroke=SAND_DIM, width=2)
    for lake in LAKES:
        c.polygon(fr.pts(lake), fill=SEA, stroke=SAND_DIM)
    river = RIVER_DIM if dim else RIVER
    for rv in (JORDAN_UP, JORDAN_LOW, ARNON, JABBOK, YARMOUK):
        c.polyline(fr.pts(rv), stroke=river, width=2)


def draw_32(c, verse):
    fr = MapFrame(31.0, 33.4, 35.0, 36.9, (36, 86, 410, 556))
    stage, caption, notes = SPECS_32[verse]

    with c.group(fr.px, fr.py, clip=(fr.mw, fr.mh)):
        c.rect(0, 0, fr.mw, fr.mh, fill=SEA)
        draw_base(c, fr, dim=(stage == "rebuke"))

        # ---- overlay pass: fills, water repaint, self-tracing highlights ----
        if stage in ("survey", "cities3"):
            c.polygon(fr.pts(JAZER_GILEAD), fill=HL + (40,))
            redraw_lakes(c, fr)
            c.traced(fr.pts(JAZER_GILEAD), stroke=g(0.9), width=3, dur=DUR,
                     closed=True)

        elif stage == "rebuke":
            west = [(32.4, 35.0), (32.4, 35.55), (31.9, 35.5), (31.77, 35.5),
                    (31.6, 35.4), (31.1, 35.4), (31.1, 35.0)]
            c.polygon(fr.pts(west), fill=TRIBE_COL["EPHRAIM"] + (26,))
            redraw_lakes(c, fr)
            if verse == 8:                       # arrow back to Kadesh-barnea
                x, y = fr.pt(31.06, 35.06)
                for hx, hy in ((46, -14), (10, -2), (4, -12)):
                    c.line((x + hx, y + hy), (x, y), g(0.85), 2)

        elif stage == "pledge":
            c.polygon(fr.pts(JAZER_GILEAD), fill=HL + (28,))
            redraw_lakes(c, fr)
            a0, a1 = fr.pt(31.98, 35.72), fr.pt(31.95, 35.32)   # crossing arrow
            c.traced([a0, a1], stroke=g(0.9), width=3, dur=DUR)
            x, y = a1
            c.line((x + 10, y - 7), (x, y), g(0.9), 3)
            c.line((x + 11, y + 5), (x, y), g(0.9), 3)

        elif stage == "grant":
            for poly in (SIHON_POLY, OG_POLY):
                c.polygon(fr.pts(poly), fill=HL + (34,))
            redraw_lakes(c, fr)
            for poly in (SIHON_POLY, OG_POLY):
                c.traced(fr.pts(poly), stroke=g(0.95), width=3, dur=DUR,
                         closed=True)

        elif stage == "build":
            tribe, _cities = BUILD_VERSES[verse]
            c.polygon(fr.pts(TRIBES[tribe][1]), fill=TRIBE_COL[tribe] + (60,))
            redraw_lakes(c, fr)

        elif stage in ("machir", "jair"):
            c.polygon(fr.pts(N_GILEAD), fill=TRIBE_COL["MANASSEH_E"] + (70,))
            redraw_lakes(c, fr)
            c.traced(fr.pts(N_GILEAD), stroke=g(0.9), width=3, dur=DUR,
                     closed=True)
            if stage == "jair":
                for la, lo in HAVVOTH_JAIR:
                    x, y = fr.pt(la, lo)
                    c.circle(x, y, 3, stroke=g(0.95), width=2)

        elif stage == "nobah":
            c.polygon(fr.pts(OG_POLY), fill=TRIBE_COL["MANASSEH_E"] + (40,))
            redraw_lakes(c, fr)
            x, y = fr.pt(*CITIES32["Kenath"][1:3])
            c.circle(x, y, 3, stroke=g(0.95), width=2)

        # ---- text pass (always on top, so nothing paints over a word) ----
        c.text(fr.pt(31.15, 35.60), "Salt Sea", 14, WATER_TXT, "lm",
               italic=True)
        c.text(fr.pt(32.82, 35.68), "Chinnereth", 14, WATER_TXT, "lm",
               italic=True)
        c.text(fr.pt(32.30, 35.48), "Jordan", 14, WATER_TXT, "rm",
               italic=True)
        c.text(fr.pt(31.36, 36.20), "Arnon", 14, WATER_TXT, "lm",
               italic=True)
        c.text(fr.pt(32.06, 35.94), "Jabbok", 14, WATER_TXT, "lt",
               italic=True)
        if stage != "grant":       # region words yield to the kingdom names
            c.text(fr.pt(31.20, 36.20), "MOAB", 14, TEXT_DIM, "mm")
            c.text(fr.pt(31.85, 36.45), "AMMON", 14, TEXT_DIM, "mm")
            c.text(fr.pt(32.95, 36.25), "BASHAN", 14, TEXT_DIM, "mm")
            c.text(fr.pt(32.25, 35.72), "GILEAD", 14, TEXT_DIM, "lm")
        c.text(fr.pt(31.70, 35.20), "CANAAN", 14, TEXT_DIM, "mm")
        label_dot(c, fr.pt(31.87, 35.44), "Jericho", (-8, 10, "rm"),
                  TEXT_DIM, 14, SAND_DIM, italic=True)

        if stage == "survey":
            c.text(fr.pt(31.98, 35.66), "Jazer", 14, TEXT, "rm")
        elif stage == "cities3":
            for key in V3_CITIES:
                disp, la, lo, place, _ = CITIES32[key]
                label_dot(c, fr.pt(la, lo), disp, place, HL, 14, HL, r=2)
        elif stage == "rebuke" and verse == 8:
            x, y = fr.pt(31.06, 35.06)
            c.text((x + 50, y - 16), "to Kadesh-barnea", 14, TEXT, "lm",
                   italic=True)
        elif stage == "pledge":
            c.text(fr.pt(32.08, 35.52), "armed, ahead of Israel", 14, TEXT,
                   "mb", italic=True)
        elif stage == "grant":
            c.text(fr.pt(31.62, 35.82), "kingdom of SIHON", 14, HL, "mm",
                   bold=True)
            c.text(fr.pt(32.93, 36.10), "kingdom of OG", 14, HL, "mm",
                   bold=True)
            c.text(fr.pt(31.35, 35.85), "Reuben", 14, TEXT, "mm", bold=True)
            c.text(fr.pt(32.13, 35.82), "Gad", 14, TEXT, "mm", bold=True)
            c.text(fr.pt(33.05, 35.85), "half-Manasseh", 14, TEXT, "mm",
                   bold=True)
        elif stage == "build":
            tribe, cities = BUILD_VERSES[verse]
            c.text(fr.pt(*TRIBES[tribe][2]), TRIBES[tribe][0], 14, TEXT, "mm",
                   bold=True)
            for v in range(34, verse):      # earlier cities of same tribe stay
                if v in BUILD_VERSES and BUILD_VERSES[v][0] == tribe:
                    for key in BUILD_VERSES[v][1]:
                        _, la, lo, place, _ = CITIES32[key]
                        label_dot(c, fr.pt(la, lo), key, place, TEXT, 14,
                                  SAND_DIM, r=2, italic=True)
            for key in cities:
                _, la, lo, place, _ = CITIES32[key]
                label_dot(c, fr.pt(la, lo), key, place, HL, 14, HL, r=3,
                          bold=True)
        elif stage in ("machir", "jair"):
            c.text(fr.pt(32.62, 36.00), "Machir (Manasseh)", 14, HL, "mm",
                   bold=True)
            if stage == "jair":
                c.text(fr.pt(32.22, 36.04), "Havvoth-jair", 14, HL, "lt",
                       bold=True)
        elif stage == "nobah":
            x, y = fr.pt(*CITIES32["Kenath"][1:3])
            c.text((x, y + 7), "Kenath", 14, HL, "mt", bold=True)
            c.text((x, y + 23), "(Nobah)", 14, HL, "mt")

        compass_scale(c, fr)
    map_border(c, fr)


def render_32(verse):
    stage, caption, notes = SPECS_32[verse]
    c = canvas("East of the Jordan — Numbers 32", verse, caption)
    draw_32(c, verse)

    y = 120
    if verse in BUILD_VERSES:
        c.text((PANEL_X, y), "modern identifications", 14, TEXT_DIM, "la",
               bold=True)
        y += 28
        for key in BUILD_VERSES[verse][1]:
            modern = CITIES32[key][4]
            line = f"{key} — {modern}" if modern else f"{key} — site unknown"
            c.text((PANEL_X, y), line, 14, TEXT, "la", italic=True)
            y += 22
    if verse == 3:
        c.text((PANEL_X, y), "identified sites include", 14, TEXT_DIM, "la",
               bold=True)
        y += 28
        for key in ("Dibon", "Heshbon", "Nebo", "Baal-meon"):
            c.text((PANEL_X, y), f"{CITIES32[key][0]} — {CITIES32[key][4]}",
                   14, TEXT, "la", italic=True)
            y += 22
    return c


def main():
    total = 0
    verses = verse_numbers("Numbers", 32)
    for verse in verses:
        c = render_32(verse)
        out = out_path("Numbers", 32, f"Numbers_32_{verse}.svg")
        c.save(out)
        total += os.path.getsize(out)
    print(f"Numbers 32: {len(verses)} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
