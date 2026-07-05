"""Generate per-verse animations for the genealogy of Jesus, Matthew 1:1-17.

Matthew arranges the line as three sets of fourteen generations (v17):
Abraham to David, David to the exile, the exile to the Christ. The visual is
three columns that fill in as the chapter is read — names already read are
solid, the current verse's names are bright with a growing connector, and
the women Matthew deliberately includes (Tamar, Rahab, Ruth, the wife of
Uriah, Mary) are noted beside the line. Verse 17 lights up the three
column headers with their counts — Matthew's own summary.

Name spellings are verified against each translation's fetched text (KJV
reads Booz/Roboam/Ozias/Salathiel where modern versions read Boaz/Rehoboam/
Uzziah/Shealtiel); translation-suffixed files are emitted only where the
spellings differ from the generic (WEB) set.

Run inside the project venv:  .venv\\Scripts\\python.exe generate_matthew1.py
"""

import os

from PIL import Image, ImageDraw

from generate_tabernacle import (W, H, BG, SAND, SAND_DIM,
                                 TEXT, TEXT_DIM, HL, F_SMALL, F_DIM,
                                 F_VERSE, F_TITLE, font, ease, g,
                                 dashed_line, out_path)
from generate_genealogy import resolve_names, G_FRAMES, G_FRAME_MS
from passages import TRANSLATIONS

MT_VARIANTS = {
    "Abraham": ["Abraham"], "Isaac": ["Isaac"], "Jacob": ["Jacob"],
    "Judah": ["Judah", "Judas", "Juda"],
    "Perez": ["Perez", "Phares", "Pharez"],
    "Zerah": ["Zerah", "Zara", "Zarah"],
    "Hezron": ["Hezron", "Esrom", "Esron"],
    "Ram": ["Ram", "Aram"],
    "Amminadab": ["Amminadab", "Aminadab"],
    "Nahshon": ["Nahshon", "Naasson"],
    "Salmon": ["Salmon"],
    "Boaz": ["Boaz", "Booz"],
    "Obed": ["Obed"], "Jesse": ["Jesse"], "David": ["David"],
    "Solomon": ["Solomon"],
    "Rehoboam": ["Rehoboam", "Roboam"],
    "Abijah": ["Abijah", "Abia", "Abias"],
    "Asa": ["Asa", "Asaph"],
    "Jehoshaphat": ["Jehoshaphat", "Josaphat"],
    "Joram": ["Joram", "Jehoram"],
    "Uzziah": ["Uzziah", "Ozias"],
    "Jotham": ["Jotham", "Joatham"],
    "Ahaz": ["Ahaz", "Achaz"],
    "Hezekiah": ["Hezekiah", "Ezekias", "Ezechias"],
    "Manasseh": ["Manasseh", "Manasses"],
    "Amon": ["Amon", "Amos"],
    "Josiah": ["Josiah", "Josias"],
    "Jechoniah": ["Jechoniah", "Jechonias", "Jeconiah"],
    "Shealtiel": ["Shealtiel", "Salathiel"],
    "Zerubbabel": ["Zerubbabel", "Zorobabel"],
    "Abiud": ["Abiud"],
    "Eliakim": ["Eliakim", "Eliacim"],
    "Azor": ["Azor"],
    "Zadok": ["Zadok", "Sadoc", "Sadok"],
    "Achim": ["Achim"], "Eliud": ["Eliud"],
    "Eleazar": ["Eleazar", "Eliazar"],
    "Matthan": ["Matthan", "Mathan"],
    "Joseph": ["Joseph"], "Jesus": ["Jesus"],
    "Tamar": ["Tamar", "Thamar"],
    "Rahab": ["Rahab", "Rachab"],
    "Ruth": ["Ruth"], "Mary": ["Mary"],
    "Uriah": ["Uriah", "Urias"],
}

MT_KEYS = list(MT_VARIANTS)

COLS = [
    ["Abraham", "Isaac", "Jacob", "Judah", "Perez", "Hezron", "Ram",
     "Amminadab", "Nahshon", "Salmon", "Boaz", "Obed", "Jesse", "David"],
    ["Solomon", "Rehoboam", "Abijah", "Asa", "Jehoshaphat", "Joram",
     "Uzziah", "Jotham", "Ahaz", "Hezekiah", "Manasseh", "Amon", "Josiah",
     "Jechoniah"],
    ["Shealtiel", "Zerubbabel", "Abiud", "Eliakim", "Azor", "Zadok",
     "Achim", "Eliud", "Eleazar", "Matthan", "Jacob", "Joseph", "Jesus"],
]

HEADERS = ["Abraham to David", "David to the exile", "the exile to the Christ"]

# (column, row) -> woman noted beside that name ("U" = the wife of Uriah)
WOMEN = {(0, 4): "Tamar", (0, 10): "Rahab", (0, 11): "Ruth",
         (1, 0): "U", (2, 12): "Mary"}

F_MT_NAME = font(16)
F_MT_ANCHOR = font(16, bold=True)
ANCHOR_CELLS = {(0, 0), (0, 13), (2, 12)}   # Abraham, David, Jesus (v1)


def build_specs(n):
    """verse -> (caption, [(col,row) highlighted], mark_read?)"""
    def c(*keys):
        return ", ".join(n[k] for k in keys)

    return {
        1: (f"Jesus Christ, the son of {n['David']}, the son of "
            f"{n['Abraham']}",
            [(0, 0), (0, 13), (2, 12)], False),
        2: (f"{n['Abraham']} fathered {n['Isaac']}; {n['Isaac']}, "
            f"{n['Jacob']}; {n['Jacob']}, {n['Judah']} and his brothers",
            [(0, 0), (0, 1), (0, 2), (0, 3)], True),
        3: (f"{n['Judah']} fathered {n['Perez']} and {n['Zerah']} by "
            f"{n['Tamar']}; then {n['Hezron']}, {n['Ram']}",
            [(0, 4), (0, 5), (0, 6)], True),
        4: (f"{c('Amminadab', 'Nahshon', 'Salmon')}",
            [(0, 7), (0, 8), (0, 9)], True),
        5: (f"{n['Boaz']} by {n['Rahab']}; {n['Obed']} by {n['Ruth']}; "
            f"then {n['Jesse']}",
            [(0, 10), (0, 11), (0, 12)], True),
        6: (f"{n['Jesse']} fathered {n['David']} the king; {n['David']}, "
            f"{n['Solomon']} by the wife of {n['Uriah']}",
            [(0, 13), (1, 0)], True),
        7: (f"{c('Rehoboam', 'Abijah', 'Asa')}",
            [(1, 1), (1, 2), (1, 3)], True),
        8: (f"{c('Jehoshaphat', 'Joram', 'Uzziah')}",
            [(1, 4), (1, 5), (1, 6)], True),
        9: (f"{c('Jotham', 'Ahaz', 'Hezekiah')}",
            [(1, 7), (1, 8), (1, 9)], True),
        10: (f"{c('Manasseh', 'Amon', 'Josiah')}",
             [(1, 10), (1, 11), (1, 12)], True),
        11: (f"{n['Josiah']} fathered {n['Jechoniah']} and his brothers, "
             "at the deportation to Babylon",
             [(1, 13)], True),
        12: (f"after the exile: {n['Jechoniah']} fathered "
             f"{n['Shealtiel']}; {n['Shealtiel']}, {n['Zerubbabel']}",
             [(2, 0), (2, 1)], True),
        13: (f"{c('Abiud', 'Eliakim', 'Azor')}",
             [(2, 2), (2, 3), (2, 4)], True),
        14: (f"{c('Zadok', 'Achim', 'Eliud')}",
             [(2, 5), (2, 6), (2, 7)], True),
        15: (f"{n['Eleazar']}, {n['Matthan']}, and {n['Jacob']}",
             [(2, 8), (2, 9), (2, 10)], True),
        16: (f"{n['Joseph']}, the husband of {n['Mary']}, of whom was "
             "born Jesus, who is called Christ",
             [(2, 11), (2, 12)], True),
        17: ("fourteen generations, and fourteen, and fourteen",
             [], True),
    }


# first verse in which each (col,row) name is read (v1 anchors excluded)
def first_read_map(specs):
    first = {}
    for verse in sorted(specs):
        caption, cells, mark = specs[verse]
        if not mark:
            continue
        for cell in cells:
            first.setdefault(cell, verse)
    return first


COL_X = [118, 452, 786]
ROW_Y0, ROW_STEP = 138, 27
HEADER_Y = 108
FOOT_Y = ROW_Y0 + 14 * ROW_STEP + 6   # under the columns


def row_y(r):
    return ROW_Y0 + r * ROW_STEP


def draw_frame(verse, spec, specs, names, first_read, t):
    ring_alpha = 1.0                       # static — nothing flashes
    grow = ease(min(1.0, t / 0.92))
    caption, cells, _ = spec

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    d.text((28, 20), "The Genealogy of Jesus — Matthew 1", font=F_TITLE,
           fill=TEXT)
    d.text((28, 52), f"verse {verse} — {caption}", font=F_VERSE, fill=HL)

    highlighted = set(cells)
    is_summary = (verse == 17)

    for ci, col in enumerate(COLS):
        x = COL_X[ci]
        header_col = HL if is_summary else TEXT_DIM
        d.text((x, HEADER_Y), HEADERS[ci], font=F_SMALL, fill=header_col,
               anchor="lm")
        for r, key in enumerate(col):
            y = row_y(r)
            cell = (ci, r)
            fv = first_read.get(cell)
            read = is_summary or (fv is not None and verse >= fv)
            cur = cell in highlighted and not is_summary

            if r < len(col) - 1:
                nfv = first_read.get((ci, r + 1))
                seg_read = is_summary or (nfv is not None and verse > nfv)
                d.line([(x, y + 6), (x, y + ROW_STEP - 6)],
                       fill=SAND if seg_read else SAND_DIM, width=2)

            dot_col = SAND if read else SAND_DIM
            d.ellipse([x - 4, y - 4, x + 4, y + 4], outline=dot_col, width=2)
            if cur:
                od.ellipse([x - 8, y - 8, x + 8, y + 8],
                           outline=g(ring_alpha), width=2)

            name = names[key]
            name_font = (F_MT_ANCHOR if cell in ANCHOR_CELLS
                         else F_MT_NAME)
            if cur:
                fill = HL
            elif read:
                fill = TEXT
            else:
                fill = TEXT_DIM
            d.text((x + 14, y), name, font=name_font, fill=fill, anchor="lm")

            wkey = WOMEN.get(cell)
            if wkey:
                note = ("the wife of " + names["Uriah"] if wkey == "U"
                        else "by " + names[wkey] if wkey != "Mary"
                        else "of " + names["Mary"])
                nx = x + 14 + d.textlength(name, font=name_font) + 8
                d.text((nx, y + 1), f"· {note}", font=F_SMALL,
                       fill=HL if cur else TEXT_DIM, anchor="lm")

    # growing connector through the current verse's names (same column)
    if cells and not is_summary:
        by_col = {}
        for ci, r in cells:
            by_col.setdefault(ci, []).append(r)
        for ci, rows in by_col.items():
            if len(rows) > 1:
                y0, y1 = row_y(min(rows)), row_y(max(rows))
                od.line([(COL_X[ci], y0),
                         (COL_X[ci], y0 + (y1 - y0) * grow)],
                        fill=g(0.95), width=4)

    # exile marker under column 2
    exile_bright = verse in (11, 12)
    dashed_line(d, (COL_X[1] - 12, FOOT_Y + 4), (COL_X[1] + 210, FOOT_Y + 4),
                HL if exile_bright else SAND_DIM, 1)
    d.text((COL_X[1], FOOT_Y + 16), "carried away to Babylon",
           font=F_SMALL, fill=HL if exile_bright else TEXT_DIM, anchor="lm")

    if is_summary:
        for ci in range(3):
            d.text((COL_X[ci], HEADER_Y + 16), "fourteen generations",
                   font=F_DIM, fill=HL, anchor="lm")

    d.text((28, H - 26), "Matthew counts three sets of fourteen (v. 17)",
           font=F_SMALL, fill=TEXT_DIM)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def render_chapter(names, suffix):
    specs = build_specs(names)
    first_read = first_read_map(specs)
    total_bytes = 0
    for verse, spec in sorted(specs.items()):
        frames = [draw_frame(verse, spec, specs, names, first_read,
                             i / (G_FRAMES - 1))
                  for i in range(G_FRAMES)]
        out = out_path("Matthew", 1, f"Matthew_1_{verse}{suffix}.webp")
        frames[0].save(out, save_all=True, append_images=frames[1:],
                       duration=G_FRAME_MS, loop=1, quality=82, method=4)
        total_bytes += os.path.getsize(out)
    return len(specs), total_bytes


if __name__ == "__main__":
    import time

    from passages import PassageError

    codes = [code for code, *_ in TRANSLATIONS]
    resolved = {}
    for code in codes:
        try:
            resolved[code] = resolve_names(code, 1, MT_KEYS, book="Matthew",
                                           variants=MT_VARIANTS)
        except PassageError as e:
            print(f"{code}: chapter unavailable ({e}) — skipped")
            continue
        time.sleep(2.5)
        print(f"{code}: {resolved[code]['Boaz']}/{resolved[code]['Rehoboam']}"
              f"/{resolved[code]['Uzziah']}/{resolved[code]['Shealtiel']}")

    generic = resolved["WEB"]
    grand_files = grand_bytes = 0
    n_files, n_bytes = render_chapter(generic, "")
    grand_files, grand_bytes = n_files, n_bytes
    print(f"Matthew 1 generic: {n_files} files")
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
    print(f"TOTAL: {grand_files} files, {grand_bytes/1e6:.1f} MB")
