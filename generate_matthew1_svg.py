"""Render Matthew 1:1-17 as per-verse vector SVGs — the vector twin of the
Matthew genealogy WebP animations (generate_matthew1.py).

Reuses that generator's exact drawing (draw_frame_on) and name-resolution, so
the same three-column layout and the same set of translation-suffixed files
(Matthew_1_2.KJV.svg ...) come out. The static columns/dots/names go on a
plain SvgLayer; the growing per-verse connector goes on an SvgAnimLayer, so it
draws itself in once and then holds — the WebP's "play once, no flashing"
motion.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_matthew1_svg.py
"""

import os
import time

from svg_surface import SvgCanvas, SvgLayer, SvgAnimLayer
from generate_tabernacle import W, H, BG, out_path
from generate_matthew1 import (
    build_specs, first_read_map, draw_frame_on, MT_KEYS, MT_VARIANTS,
)
from generate_genealogy import resolve_names
from passages import PassageError, TRANSLATIONS

DUR = "2.6s"


def render_verse_svg(verse, spec, specs, names, first_read):
    base, over = SvgLayer(), SvgAnimLayer(dur=DUR)
    draw_frame_on(base, over, verse, spec, specs, names, first_read, t=1.0)
    c = SvgCanvas(W, H, bg=BG)
    c.raw(base.elements())
    c.raw(over.elements())
    return c


def render_chapter(names, suffix):
    specs = build_specs(names)
    first_read = first_read_map(specs)
    total = 0
    for verse, spec in sorted(specs.items()):
        c = render_verse_svg(verse, spec, specs, names, first_read)
        out = out_path("Matthew", 1, f"Matthew_1_{verse}{suffix}.svg")
        c.save(out)
        total += os.path.getsize(out)
    return len(specs), total


def main():
    codes = [code for code, *_ in TRANSLATIONS]
    resolved = {}
    for code in codes:
        try:
            resolved[code] = resolve_names(code, 1, MT_KEYS, book="Matthew",
                                           variants=MT_VARIANTS)
        except PassageError as e:
            print(f"{code}: chapter unavailable ({e}) — skipped")
            continue
        time.sleep(0.2)

    generic = resolved["WEB"]
    grand_files, grand_bytes = render_chapter(generic, "")
    print(f"Matthew 1 generic: {grand_files} files")
    for code in codes:
        if code == "WEB" or code not in resolved:
            continue
        if resolved[code] == generic:
            print(f"  {code}: matches generic spellings — skipped")
            continue
        n_files, n_bytes = render_chapter(resolved[code], f".{code}")
        grand_files += n_files
        grand_bytes += n_bytes
        print(f"  {code}: {n_files} translation-specific files")
    print(f"TOTAL: {grand_files} SVG files, {grand_bytes/1e3:.0f} KB")


if __name__ == "__main__":
    main()
