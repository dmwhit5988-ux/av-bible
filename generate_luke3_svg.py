"""Render Luke 3:23-38 as per-verse vector SVGs — the vector twin of the
backward-genealogy WebP animations (generate_luke3.py).

Luke's motion is a tracking camera dollying along one long road from Jesus
back toward Adam. That camera slide lives in the coordinate mapping, not in a
separate overlay, so (unlike the other genealogy SVGs) it is re-expressed here
rather than reusing draw_frame: the whole road — its line, every milestone dot
and name — is drawn once in road space inside a <g>, and that group's
translate animates from the verse's starting camera to its resting camera and
freezes, reproducing the dolly. The centered traveler ring, the bright "just
travelled" sweep behind it, and the minimap progress/marker animate as screen-
fixed overlays on top. Names/geometry, fonts and colours are the WebP's own.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_luke3_svg.py
"""

import os
import time

from svg_surface import SvgCanvas, SvgLayer, _rgb, _fmt
from generate_tabernacle import (W, H, BG, SAND, SAND_DIM, TEXT, TEXT_DIM, HL,
                                 out_path)
from generate_luke3 import (
    extract_line, build_grid, era_of, ROAD_Y, SPACING,
    MINI_X0, MINI_X1, MINI_Y, F_ROAD, F_ROAD_B, F_ERA,
)
from passages import PassageError, TRANSLATIONS

DUR = "2.6s"
EASE = "0.42 0 0.58 1"


def _op(color):
    return color[3] / 255.0 if len(color) > 3 else 1.0


def _anim(attr, v0, v1):
    return (f'<animate attributeName="{attr}" values="{_fmt(v0)};{_fmt(v1)}" '
            f'dur="{DUR}" begin="0s" fill="freeze" calcMode="spline" '
            f'keyTimes="0;1" keySplines="{EASE}"/>')


def _stroke_attrs(color, width, linecap="round"):
    a = (f'stroke="{_rgb(color)}" stroke-width="{_fmt(width)}" '
         f'stroke-linecap="{linecap}"')
    op = _op(color)
    if op < 1:
        a += f' stroke-opacity="{op:.3f}"'
    return a


def caption_for(verse, slots, ranges):
    start, end = ranges[verse]
    batch = [slots[i][0] for i in range(start, end) if slots[i][0] != "Jesus"]
    if verse == 23:
        return "the son (as was supposed) of " + ", of ".join(batch)
    if verse == 38:
        return ("… of " + ", of ".join(batch[:-1]) +
                f", the son of {batch[-1]}")
    return "the son of " + ", of ".join(batch)


def render_verse_svg(verse, slots, ranges):
    n = len(slots)
    span = (n - 1) * SPACING
    start, end = ranges[verse]
    prev = max(start - 1, 0)
    tip0 = prev * SPACING              # camera at the verse's first frame
    tip1 = (end - 1) * SPACING         # camera at rest (held final)
    dx = tip1 - tip0                   # how far the road slides left

    def sx(s):                         # road position -> screen x, at rest
        return W // 2 + s - tip1

    c = SvgCanvas(W, H, bg=BG)
    caption = caption_for(verse, slots, ranges)
    c.text((28, 20), "From Jesus back to Adam — Luke 3", 24, TEXT, "la",
           bold=True)
    c.text((28, 52), f"verse {verse} — {caption[:92]}", 18, HL, "la",
           italic=True)

    # ---- the road group: everything road-fixed, drawn once, then dollied ----
    road = SvgLayer()
    road.line([(sx(0), ROAD_Y), (sx(span), ROAD_Y)], fill=SAND_DIM, width=3)
    road.line([(sx(0), ROAD_Y), (sx(prev * SPACING), ROAD_Y)], fill=SAND,
              width=3)
    for i, (name, _v) in enumerate(slots):
        x = sx(i * SPACING)
        era = era_of(name, i)
        cur = start <= i < end
        read = i < start
        r = 7 if era else 5
        road.ellipse([x - r, ROAD_Y - r, x + r, ROAD_Y + r],
                     outline=SAND if (read or cur) else SAND_DIM, width=2)
        fill = HL if cur else TEXT if read else TEXT_DIM
        above = (i % 2 == 0)
        ny = ROAD_Y - 46 if above else ROAD_Y + 46
        ey = ROAD_Y - 24 if above else ROAD_Y + 24
        road.text((x, ny), name, font=F_ROAD_B if era else F_ROAD, fill=fill,
                  anchor="mm")
        if era:
            road.text((x, ey), era, font=F_ERA, fill=TEXT_DIM, anchor="mm")
    grp = (f'<g><animateTransform attributeName="transform" '
           f'attributeType="XML" type="translate" '
           f'values="{_fmt(dx)} 0;0 0" dur="{DUR}" begin="0s" fill="freeze" '
           f'calcMode="spline" keyTimes="0;1" keySplines="{EASE}"/>'
           + "".join(road.elements()) + "</g>")
    c.raw([grp])

    # ---- screen-fixed overlays on top ----
    # the bright "just travelled" sweep: right end pinned at the centre, left
    # end slides out from the centre to the previous resting point.
    cx = W // 2
    x1 = sx(prev * SPACING)
    c.raw([f'<line x1="{_fmt(cx)}" y1="{ROAD_Y}" x2="{_fmt(cx)}" y2="{ROAD_Y}" '
           f'{_stroke_attrs(HL + (242,), 5)}>{_anim("x1", cx, x1)}</line>'])
    # the traveler: a steady ring at the centre of the view
    c.circle(cx, ROAD_Y, 10, stroke=HL + (255,), width=3)

    # ---- minimap: the whole road at a glance ----
    def mx(s):
        return MINI_X0 + (MINI_X1 - MINI_X0) * s / span

    c.line((MINI_X0, MINI_Y), (MINI_X1, MINI_Y), SAND_DIM, 2)
    c.raw([f'<line x1="{_fmt(MINI_X0)}" y1="{MINI_Y}" x2="{_fmt(mx(tip0))}" '
           f'y2="{MINI_Y}" {_stroke_attrs(SAND, 2, "butt")}>'
           f'{_anim("x2", mx(tip0), mx(tip1))}</line>'])
    for i, (name, _v) in enumerate(slots):
        if not era_of(name, i):
            continue
        x = mx(i * SPACING)
        c.line((x, MINI_Y - 4), (x, MINI_Y + 4), SAND, 2)
        ly = MINI_Y - 14 if name == "Adam" else MINI_Y + 14
        c.text((x, ly), name, 13, TEXT_DIM, "mm", italic=True)
    c.raw([f'<circle cx="{_fmt(mx(tip0))}" cy="{MINI_Y}" r="4" '
           f'fill="{_rgb(HL)}">{_anim("cx", mx(tip0), mx(tip1))}</circle>'])

    if end >= n:
        counter = f"all {n - 1} generations — back to the beginning"
    else:
        counter = f"generation {end - 1} of {n - 1}"
    c.text((W - 28, H - 26), counter, 14, TEXT, "ra", italic=True)
    c.text((28, H - 26),
           "Luke traces the line backward — from Jesus to Adam, "
           "“the son of God”", 14, TEXT_DIM, "la", italic=True)
    return c


def render_chapter(line, suffix):
    slots, ranges = build_grid(line)
    total = 0
    for verse in sorted(ranges):
        c = render_verse_svg(verse, slots, ranges)
        out = out_path("Luke", 3, f"Luke_3_{verse}{suffix}.svg")
        c.save(out)
        total += os.path.getsize(out)
    return len(ranges), total


def main():
    codes = [code for code, *_ in TRANSLATIONS]
    resolved = {}
    for code in codes:
        try:
            resolved[code] = extract_line(code)
        except (ValueError, PassageError) as e:
            print(f"{code}: extraction failed ({e}) — will use generic")
            resolved[code] = None
        time.sleep(0.2)

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
    print(f"TOTAL: {grand_files} SVG files, {grand_bytes/1e3:.0f} KB")


if __name__ == "__main__":
    main()
