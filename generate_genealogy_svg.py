"""Render Genesis 5 and 11:10-32 as per-verse vector SVGs — the vector twins
of the genealogy WebP animations (generate_genealogy.py).

Reuses that generator's exact drawing (draw_frame_on) and its translation
name-resolution, so the same hand-tuned layout and the same set of
translation-suffixed files (Genesis_5_3.KJV.svg ...) come out — only the
backend changes. The static chain, timeline and labels go on a plain SvgLayer;
the overlay (the growing lifespan bars and family edges) goes on an
SvgAnimLayer, so each verse's highlight draws itself in once and then holds,
keeping the "play once, no flashing" motion of the WebP.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_genealogy_svg.py
"""

import os
import time

from svg_surface import SvgCanvas, SvgLayer, SvgAnimLayer
from generate_tabernacle import W, H, BG, out_path
from generate_genealogy import (
    ChapterData, build_g5_specs, build_g11_specs, draw_frame_on,
    resolve_names, G5_KEYS, G11_KEYS,
)
from passages import PassageError, TRANSLATIONS

# One reveal ~ the raster grow (24 frames x 120 ms, complete by ~92%).
DUR = "2.6s"


def render_verse_svg(cd, verse, spec, names):
    base, over = SvgLayer(), SvgAnimLayer(dur=DUR)
    draw_frame_on(base, over, cd, verse, spec, names, t=1.0)   # held final
    c = SvgCanvas(W, H, bg=BG)
    c.raw(base.elements())
    c.raw(over.elements())
    return c


def render_chapter(chapter, names, suffix):
    cd = ChapterData(chapter)
    specs = build_g5_specs(names) if chapter == 5 else build_g11_specs(names)
    total = 0
    for verse, spec in sorted(specs.items()):
        c = render_verse_svg(cd, verse, spec, names)
        out = out_path("Genesis", chapter,
                       f"Genesis_{chapter}_{verse}{suffix}.svg")
        c.save(out)
        total += os.path.getsize(out)
    return len(specs), total


def main():
    codes = [code for code, *_ in TRANSLATIONS]
    resolved = {}
    for code in codes:
        try:
            g5 = resolve_names(code, 5, G5_KEYS)
            time.sleep(0.2)
            g11 = resolve_names(code, 11, G11_KEYS)
            time.sleep(0.2)
        except PassageError as e:
            print(f"{code}: chapters unavailable ({e}) — skipped")
            continue
        resolved[code] = {5: g5, 11: g11}

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
    print(f"TOTAL: {grand_files} SVG files, {grand_bytes/1e3:.0f} KB")


if __name__ == "__main__":
    main()
