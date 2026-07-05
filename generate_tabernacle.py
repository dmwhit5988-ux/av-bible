"""Generate per-verse tabernacle animations for Exodus 25, 26, and 27.

Draws a to-scale top-down plan of the tabernacle courtyard (dimensions taken
from the text: courtyard 100x50 cubits, tent 30x10, bronze altar 5x5x3, gate
20 cubits) plus detail "inset" panels — the ark and mercy seat, the table of
showbread, the golden lampstand, the curtains, the board frames, the veil,
and the bronze altar — and renders one looping animated WebP per verse into
visuals/ (Exodus_25_1.webp ... Exodus_27_21.webp), highlighting whatever each
verse describes.

Run inside the project venv:  .venv\\Scripts\\python.exe generate_tabernacle.py

This is a dev tool, not part of the running app. To cover more passages, add
entries to the CHAPTERS spec tables (and new inset drawers if needed).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
VISUALS = os.path.join(BASE, "visuals")


def out_path(book: str, chapter, filename: str) -> str:
    """Visuals live in visuals/<Book>/<chapter>/ for easy human navigation."""
    d = os.path.join(VISUALS, book.replace(" ", "_"), str(chapter))
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, filename)

# ---------------------------------------------------------------------------
# Canvas & palette
# ---------------------------------------------------------------------------

W, H = 1024, 576
FRAMES = 16
FRAME_MS = 130

BG = (16, 16, 24)
PANEL = (26, 26, 38)
SAND = (138, 129, 95)          # base linework
SAND_DIM = (74, 70, 56)
SILVER = (176, 180, 190)
TEXT = (216, 198, 143)
TEXT_DIM = (140, 130, 100)
GOLD = (255, 212, 94)          # decorative gold accents
HL = (255, 244, 170)           # highlight — bright, near-white gold so it
                               # stands out against gold/sand base linework
BRONZE = (208, 138, 62)
RED = (170, 70, 60)
BROWN = (120, 88, 58)
GRAY = (120, 116, 108)
WHITE_LINEN = (200, 196, 178)
GATE_COLORS = [(122, 134, 216), (154, 95, 176), (200, 85, 85),
               (200, 196, 178)]  # blue, purple, scarlet, fine linen

S = 6.6                        # px per cubit (plan)
PX0, PY0 = 96, 118             # plan origin (west/north corner of courtyard)

def cub(x, y):
    """Cubit coords (x from west, y from north) -> pixel coords."""
    return PX0 + x * S, PY0 + y * S


def font(size, bold=False, italic=False):
    name = "georgia"
    if bold:
        name += "b"
    elif italic:
        name += "i"
    try:
        return ImageFont.truetype(name + ".ttf", size)
    except OSError:
        return ImageFont.load_default()


F_TITLE = font(24, bold=True)
F_LABEL = font(15)
F_SMALL = font(14, italic=True)
F_DIM = font(14, bold=True)
F_VERSE = font(18, italic=True)


def ease(t):
    return t * t * (3 - 2 * t)


def pulse(t):
    return 0.5 - 0.5 * math.cos(2 * math.pi * t)


def g(alpha):
    return HL + (int(255 * alpha),)


def dashed_line(dr, p0, p1, fill, width=2, dash=6, gap=5):
    x0, y0 = p0
    x1, y1 = p1
    dist = math.hypot(x1 - x0, y1 - y0)
    if dist < 1:
        return
    ux, uy = (x1 - x0) / dist, (y1 - y0) / dist
    s = 0.0
    while s < dist:
        e = min(s + dash, dist)
        dr.line([(x0 + ux * s, y0 + uy * s), (x0 + ux * e, y0 + uy * e)],
                fill=fill, width=width)
        s += dash + gap


def dashed_rect(dr, box, fill, width=2):
    x0, y0, x1, y1 = box
    dashed_line(dr, (x0, y0), (x1, y0), fill, width)
    dashed_line(dr, (x1, y0), (x1, y1), fill, width)
    dashed_line(dr, (x1, y1), (x0, y1), fill, width)
    dashed_line(dr, (x0, y1), (x0, y0), fill, width)


# ---------------------------------------------------------------------------
# Static plan (drawn once per frame, optionally dimmed)
# ---------------------------------------------------------------------------

def draw_plan(d, dim=False):
    line = SAND_DIM if dim else SAND
    text = TEXT_DIM if dim else TEXT
    linen = tuple(c // 2 for c in WHITE_LINEN) if dim else WHITE_LINEN

    d.line([cub(0, 0), cub(100, 0)], fill=linen, width=3)      # north
    d.line([cub(0, 50), cub(100, 50)], fill=linen, width=3)    # south
    d.line([cub(0, 0), cub(0, 50)], fill=linen, width=3)       # west
    d.line([cub(100, 0), cub(100, 15)], fill=linen, width=3)   # east NE
    d.line([cub(100, 35), cub(100, 50)], fill=linen, width=3)  # east SE
    seg = 20 / len(GATE_COLORS)
    for i, col in enumerate(GATE_COLORS):
        c = tuple(v // 2 for v in col) if dim else col
        d.line([cub(100, 15 + i * seg), cub(100, 15 + (i + 1) * seg)],
               fill=c, width=5)

    def pillars(points):
        for x, y in points:
            px, py = cub(x, y)
            d.ellipse([px - 2.6, py - 2.6, px + 2.6, py + 2.6], fill=line)
    pillars([(x, 0) for x in range(0, 101, 5)])
    pillars([(x, 50) for x in range(0, 101, 5)])
    pillars([(0, y) for y in range(5, 50, 5)])
    pillars([(100, y) for y in (5, 10, 15, 20, 26.67, 33.33, 35, 40, 45)])

    d.rectangle([cub(10, 20), cub(40, 30)], outline=line, width=3)
    d.line([cub(20, 20), cub(20, 30)], fill=line, width=2)   # veil
    d.rectangle([cub(13.75, 24.25), cub(16.25, 25.75)], outline=text, width=2)
    d.rectangle([cub(22, 24.5), cub(23, 25.5)], outline=line, width=1)
    d.rectangle([cub(29, 21.2), cub(31, 22.2)], outline=line, width=1)
    lx, ly = cub(30, 28)
    d.ellipse([lx - 4, ly - 4, lx + 4, ly + 4], outline=line, width=2)
    vx, vy = cub(50, 25)
    d.ellipse([vx - 6, vy - 6, vx + 6, vy + 6], outline=line, width=2)
    d.rectangle([cub(62.5, 22.5), cub(67.5, 27.5)],
                outline=BRONZE if not dim else tuple(c // 2 for c in BRONZE),
                width=3)

    d.text(cub(25, 17.5), "TENT OF MEETING", font=F_SMALL, fill=text,
           anchor="mm")
    d.text(cub(15, 31.2), "Most Holy", font=F_SMALL, fill=text, anchor="ma")
    d.text(cub(65, 30.5), "Bronze Altar", font=F_SMALL, fill=text,
           anchor="ma")
    d.text(cub(50, 28.5), "Laver", font=F_SMALL, fill=text, anchor="ma")
    d.text(cub(104, 25), "GATE", font=F_SMALL, fill=text, anchor="lm")
    d.text(cub(50, 53.5), "COURTYARD  —  100 × 50 cubits", font=F_SMALL,
           fill=text, anchor="ma")
    # Compass with drawn arrowheads — Georgia has no ↑/→ glyphs, so text
    # arrows render as missing-glyph boxes.
    ox, oy = W - 84, 56
    d.line([(ox, oy), (ox, oy - 30)], fill=line, width=2)
    d.line([(ox - 4, oy - 23), (ox, oy - 30), (ox + 4, oy - 23)],
           fill=line, width=2, joint="curve")
    d.line([(ox, oy), (ox + 30, oy)], fill=line, width=2)
    d.line([(ox + 23, oy - 4), (ox + 30, oy), (ox + 23, oy + 4)],
           fill=line, width=2, joint="curve")
    d.text((ox, oy - 40), "N", font=F_LABEL, fill=text, anchor="mm")
    d.text((ox + 40, oy), "E", font=F_LABEL, fill=text, anchor="lm")


def draw_chrome(d, chapter, verse, caption):
    d.text((28, 20), f"The Tabernacle — Exodus {chapter}", font=F_TITLE,
           fill=TEXT)
    d.text((28, 52), f"verse {verse} — {caption}", font=F_VERSE, fill=GOLD)
    d.text((28, H - 26), "1 cubit ≈ 18 in / 45 cm", font=F_SMALL,
           fill=TEXT_DIM)


# ---------------------------------------------------------------------------
# Plan highlights
# ---------------------------------------------------------------------------

def hl_wall(od, side, alpha, frac):
    a = g(alpha)
    if side == "south":
        x0, y0 = cub(0, 50); x1, _ = cub(100 * frac, 50)
        od.line([(x0, y0), (x1, y0)], fill=a, width=6)
    elif side == "north":
        x0, y0 = cub(0, 0); x1, _ = cub(100 * frac, 0)
        od.line([(x0, y0), (x1, y0)], fill=a, width=6)
    elif side == "west":
        x0, y0 = cub(0, 0); _, y1 = cub(0, 50 * frac)
        od.line([(x0, y0), (x0, y1)], fill=a, width=6)
    elif side == "east_full":
        x0, y0 = cub(100, 0); _, y1 = cub(100, 50 * frac)
        od.line([(x0, y0), (x0, y1)], fill=a, width=6)
    elif side == "east_flank_s":
        x0, y0 = cub(100, 35); _, y1 = cub(100, 35 + 15 * frac)
        od.line([(x0, y0), (x0, y1)], fill=a, width=6)
    elif side == "east_flank_n":
        x0, y0 = cub(100, 0); _, y1 = cub(100, 15 * frac)
        od.line([(x0, y0), (x0, y1)], fill=a, width=6)
    elif side == "gate":
        x0, y0 = cub(100, 15); _, y1 = cub(100, 15 + 20 * frac)
        od.line([(x0, y0), (x0, y1)], fill=a, width=8)


def hl_pillars(od, side, alpha, frac=1.0):
    pts = {"south": [(x, 50) for x in range(0, 101, 5)],
           "north": [(x, 0) for x in range(0, 101, 5)],
           "west": [(0, y) for y in range(0, 51, 5)],
           "gate": [(100, y) for y in (15, 21.67, 28.33, 35)],
           "all": ([(x, 50) for x in range(0, 101, 5)]
                   + [(x, 0) for x in range(0, 101, 5)]
                   + [(0, y) for y in range(5, 50, 5)]
                   + [(100, y) for y in (5, 10, 15, 21.67, 28.33, 35,
                                          40, 45)])}[side]
    n = max(1, int(len(pts) * frac))
    for x, y in pts[:n]:
        px, py = cub(x, y)
        od.ellipse([px - 5, py - 5, px + 5, py + 5], outline=g(alpha),
                   width=3)


def hl_altar_plan(od, alpha, frac=1.0):
    od.rectangle([cub(62.5, 22.5), cub(67.5, 27.5)], outline=g(alpha),
                 width=5)


def hl_ark_plan(od, alpha, frac=1.0):
    od.rectangle([cub(13.75, 24.25), cub(16.25, 25.75)], outline=g(alpha),
                 width=4)


def hl_table_plan(od, alpha, frac=1.0):
    od.rectangle([cub(29, 21.2), cub(31, 22.2)], outline=g(alpha), width=4)


def hl_veil_plan(od, alpha, frac=1.0):
    od.line([cub(20, 20), cub(20, 30)], fill=g(alpha), width=5)


def hl_tent_wall(od, side, alpha, frac=1.0):
    a = g(alpha)
    if side == "south":
        od.line([cub(10, 30), cub(10 + 30 * frac, 30)], fill=a, width=5)
    elif side == "north":
        od.line([cub(10, 20), cub(10 + 30 * frac, 20)], fill=a, width=5)
    elif side == "west":
        od.line([cub(10, 20), cub(10, 20 + 10 * frac)], fill=a, width=5)
    elif side == "door":
        od.line([cub(40, 20), cub(40, 20 + 10 * frac)], fill=a, width=5)


def hl_whole(od, alpha, frac=1.0):
    od.rectangle([cub(-3, -3), cub(103, 53)], outline=g(alpha * 0.8),
                 width=3)


def hl_pegs(od, alpha, frac=1.0):
    pts = ([(x, -1.6) for x in range(2, 100, 7)]
           + [(x, 51.6) for x in range(2, 100, 7)]
           + [(-1.6, y) for y in range(4, 50, 7)]
           + [(101.6, y) for y in range(4, 50, 7)])
    n = max(1, int(len(pts) * frac))
    for x, y in pts[:n]:
        px, py = cub(x, y)
        od.line([(px - 3, py - 3), (px + 3, py + 3)], fill=g(alpha), width=2)
        od.line([(px - 3, py + 3), (px + 3, py - 3)], fill=g(alpha), width=2)


def hl_lamp(od, alpha, frac=1.0):
    lx, ly = cub(30, 28)
    od.ellipse([lx - 5, ly - 5, lx + 5, ly + 5], outline=g(alpha), width=3)
    for r in (10, 16, 22):
        od.ellipse([lx - r, ly - r, lx + r, ly + r],
                   outline=HL + (int(255 * alpha * (0.75 - r / 100)),),
                   width=2)


def hl_tent(od, alpha, frac=1.0):
    od.rectangle([cub(10, 20), cub(40, 30)], outline=g(alpha), width=4)
    od.line([cub(20, 20), cub(20, 30)], fill=g(alpha), width=3)


def hl_dims(od, alpha, frac=1.0):
    a = g(alpha)

    def arrow(p0, p1):
        od.line([p0, p1], fill=a, width=2)
        for p, q in ((p0, p1), (p1, p0)):
            ang = math.atan2(q[1] - p[1], q[0] - p[0])
            for da in (0.5, -0.5):
                od.line([p, (p[0] + 10 * math.cos(ang + da),
                             p[1] + 10 * math.sin(ang + da))], fill=a,
                        width=2)
    x0, y = cub(0, 57); x1, _ = cub(100, 57)
    arrow((x0, y), (x1, y))
    x, y0 = cub(107, 0); _, y1 = cub(107, 50)
    arrow((x, y0), (x, y1))


DIM_LABELS = [("100 cubits", 50, 60.5), ("50 cubits", 110, 30)]


# ---------------------------------------------------------------------------
# Inset framework
# ---------------------------------------------------------------------------

IX, IY, IW, IH = 636, 112, 356, 380
CAPY1 = IY + IH - 56
CAPY2 = IY + IH - 32
ICX = IX + IW // 2


def panel(d, title, subtitle=None):
    d.rounded_rectangle([IX, IY, IX + IW, IY + IH], radius=10, fill=PANEL,
                        outline=SAND_DIM, width=2)
    d.text((ICX, IY + 22), title, font=F_LABEL, fill=TEXT, anchor="mm")
    if subtitle:
        d.text((ICX, IY + 44), subtitle, font=F_SMALL, fill=TEXT_DIM,
               anchor="mm")


def cap(od, alpha, line1, line2=None):
    od.text((ICX, CAPY1), line1, font=F_DIM, fill=g(alpha), anchor="mm")
    if line2:
        od.text((ICX, CAPY2), line2, font=F_SMALL, fill=g(alpha), anchor="mm")


# --- bronze altar (Exodus 27:1-8) ------------------------------------------

AS = 52
AX = IX + (IW - 5 * AS) // 2
AY = IY + 92
AW, AH = 5 * AS, 3 * AS


def inset_altar(d, od, part, alpha, frac):
    panel(d, "THE BRONZE ALTAR", "acacia wood overlaid with bronze")
    body = [AX, AY, AX + AW, AY + AH]
    d.rectangle(body, outline=BRONZE, width=3)
    horns = [[AX - 6, AY - 22, AX + 16, AY],
             [AX + AW - 16, AY - 22, AX + AW + 6, AY]]
    for hx0, hy0, hx1, hy1 in horns:
        d.polygon([(hx0, hy1), (hx1, hy1), ((hx0 + hx1) / 2, hy0)],
                  outline=BRONZE, width=2)
    my = AY + AH / 2
    d.line([(AX - 14, my), (AX + AW + 14, my)], fill=SAND, width=2)
    step, right = 13, AX + AW
    for x in range(int(AX), int(right), step):
        run = min(AH / 2, right - x)
        d.line([(x, my), (x + run, my + run)], fill=SAND_DIM, width=1)
        d.line([(x, AY + AH), (x + run, AY + AH - run)], fill=SAND_DIM,
               width=1)
    py = AY + AH / 2 - 8
    d.line([(AX - 46, py), (AX - 6, py)], fill=SAND, width=4)
    d.line([(AX + AW + 6, py), (AX + AW + 46, py)], fill=SAND, width=4)
    for rx in (AX - 6, AX + AW + 6):
        d.ellipse([rx - 6, py - 6, rx + 6, py + 6], outline=BRONZE, width=2)
    d.text((ICX, CAPY2), "5 × 5 cubits square, 3 cubits high", font=F_SMALL,
           fill=TEXT_DIM, anchor="mm")

    a = g(alpha)
    if part == "body":
        od.rectangle(body, outline=a, width=5)
        cap(od, alpha, "5 wide × 5 deep × 3 high")
    elif part == "horns":
        for hx0, hy0, hx1, hy1 in horns:
            od.polygon([(hx0, hy1), (hx1, hy1), ((hx0 + hx1) / 2, hy0)],
                       outline=a, width=4)
        cap(od, alpha, "horns on its four corners, of one piece")
    elif part == "utensils":
        cap(od, alpha, "pots · shovels · basins · forks · firepans")
    elif part == "grate":
        od.rectangle([AX, my, AX + AW, AY + AH], outline=a, width=4)
        cap(od, alpha, "a grating, a network of bronze")
    elif part == "grate_mid":
        od.line([(AX - 20, my), (AX + AW + 20, my)], fill=a, width=4)
        cap(od, alpha, "the grate reaches halfway up the altar")
    elif part == "poles":
        od.line([(AX - 46, py), (AX - 6, py)], fill=a, width=6)
        od.line([(AX + AW + 6, py), (AX + AW + 46, py)], fill=a, width=6)
        cap(od, alpha, "poles of acacia wood, overlaid with bronze")
    elif part == "rings":
        for rx in (AX - 6, AX + AW + 6):
            od.ellipse([rx - 9, py - 9, rx + 9, py + 9], outline=a, width=4)
        cap(od, alpha, "poles through rings, for carrying")
    elif part == "hollow":
        od.rectangle([AX + 14, AY + 14, AX + AW - 14, AY + AH - 14],
                     outline=a, width=3)
        cap(od, alpha, "hollow, made with boards")


# --- materials list (Exodus 25:3-7) ----------------------------------------

MATERIAL_ROWS = [
    ("metals", "gold, silver, and bronze"),
    ("fabrics", "blue, purple, scarlet · fine linen · goats' hair"),
    ("skins_wood", "rams' skins dyed red · fine leather · acacia"),
    ("oil_spice", "oil for the light · spices for oil and incense"),
    ("stones", "onyx and setting stones, for ephod and breastpiece"),
]


def inset_materials(d, od, part, alpha, frac):
    panel(d, "MATERIALS FOR THE SANCTUARY", "a freewill offering")
    for i, (key, text) in enumerate(MATERIAL_ROWS):
        y = IY + 96 + i * 46
        d.ellipse([IX + 26, y - 3, IX + 32, y + 3], fill=SAND_DIM)
        if key == part:
            od.ellipse([IX + 23, y - 6, IX + 35, y + 6], outline=g(alpha),
                       width=2)
            od.text((IX + 44, y), text, font=F_DIM, fill=g(alpha),
                    anchor="lm")
        else:
            d.text((IX + 44, y), text, font=F_SMALL, fill=TEXT_DIM,
                   anchor="lm")


# --- the ark & mercy seat (Exodus 25:10-22) ---------------------------------

KSC = 60
KW, KH = int(2.5 * KSC), int(1.5 * KSC)          # 150 x 90
KX0 = IX + (IW - KW) // 2
KY1 = IY + 296
KY0 = KY1 - KH
KSY0, KSY1 = KY0 - 14, KY0                       # mercy seat slab
KCX = IX + IW // 2


def _cherubs():
    """[(body_box, wing_polygon), ...] for the two cherubim."""
    out = []
    for bx, dr in ((KX0 + 30, 1), (KX0 + KW - 30, -1)):
        body = [bx - 8, KSY0 - 26, bx + 8, KSY0]
        wing = [(bx + dr * 2, KSY0 - 18), (bx + dr * 42, KSY0 - 58),
                (bx + dr * 16, KSY0 - 4)]
        out.append((body, wing))
    return out


def inset_ark(d, od, part, alpha, frac):
    panel(d, "THE ARK OF THE TESTIMONY", "with the mercy seat and cherubim")
    d.rectangle([KX0, KY0, KX0 + KW, KY1], outline=SAND, width=3)
    d.rectangle([KX0 - 4, KSY0, KX0 + KW + 4, KSY1], outline=SAND, width=2)
    for fx in (KX0 + 8, KX0 + KW - 20):
        d.rectangle([fx, KY1, fx + 12, KY1 + 9], outline=SAND, width=2)
    ry = KY1 - 10
    d.line([(KX0 - 44, ry), (KX0 + KW + 44, ry)], fill=SAND, width=4)
    for rx in (KX0 + 6, KX0 + KW - 6):
        d.ellipse([rx - 7, ry - 7, rx + 7, ry + 7], outline=SAND, width=2)
    dashed_rect(d, [KCX - 22, KY0 + 20, KCX + 22, KY0 + 68], SAND_DIM)
    for body, wing in _cherubs():
        d.ellipse(body, outline=SAND, width=2)
        d.polygon(wing, outline=SAND, width=2)

    a = g(alpha)
    if part == "body":
        od.rectangle([KX0, KY0, KX0 + KW, KY1], outline=a, width=5)
        cap(od, alpha, "2½ long × 1½ wide × 1½ high", "of acacia wood")
    elif part == "gold":
        od.rectangle([KX0 - 3, KY0 - 3, KX0 + KW + 3, KY1 + 3], outline=a,
                     width=4)
        cap(od, alpha, "overlaid with pure gold, inside and out",
            "with a molding of gold around it")
    elif part == "rings":
        for rx in (KX0 + 6, KX0 + KW - 6):
            od.ellipse([rx - 10, ry - 10, rx + 10, ry + 10], outline=a,
                       width=4)
        cap(od, alpha, "four rings of cast gold, on its four feet")
    elif part == "poles":
        od.line([(KX0 - 44, ry), (KX0 + KW + 44, ry)], fill=a, width=6)
        cap(od, alpha, "poles of acacia wood, overlaid with gold")
    elif part == "poles_in":
        od.line([(KX0 - 44, ry), (KX0 + KW + 44, ry)], fill=a, width=6)
        for rx in (KX0 + 6, KX0 + KW - 6):
            od.ellipse([rx - 10, ry - 10, rx + 10, ry + 10], outline=a,
                       width=3)
        cap(od, alpha, "the poles in the rings, to carry the ark")
    elif part == "poles_stay":
        od.line([(KX0 - 44, ry), (KX0 + KW + 44, ry)], fill=a, width=6)
        cap(od, alpha, "the poles remain in the rings", "never removed")
    elif part == "testimony":
        dashed_rect(od, [KCX - 24, KY0 + 18, KCX + 24, KY0 + 70], a, 3)
        cap(od, alpha, "the testimony, placed within the ark")
    elif part == "mercy":
        od.rectangle([KX0 - 5, KSY0 - 2, KX0 + KW + 5, KSY1 + 2], outline=a,
                     width=4)
        cap(od, alpha, "the mercy seat: pure gold", "2½ × 1½ cubits")
    elif part == "cherub_two":
        for body, wing in _cherubs():
            od.ellipse(body, outline=a, width=3)
            od.polygon(wing, outline=a, width=3)
        cap(od, alpha, "two cherubim of hammered gold")
    elif part == "cherub_ends":
        for body, wing in _cherubs():
            od.ellipse(body, outline=a, width=3)
        cap(od, alpha, "one at each end",
            "of one piece with the mercy seat")
    elif part == "wings":
        for body, wing in _cherubs():
            od.polygon(wing, outline=a, width=4)
        cap(od, alpha, "wings spread upward",
            "faces toward the mercy seat")
    elif part == "seat_on_ark":
        od.rectangle([KX0 - 5, KSY0 - 2, KX0 + KW + 5, KSY1 + 2], outline=a,
                     width=3)
        dashed_rect(od, [KCX - 24, KY0 + 18, KCX + 24, KY0 + 70], a, 2)
        cap(od, alpha, "the mercy seat above, the testimony within")
    elif part == "meet":
        mx, my2 = KCX, KSY0 - 62
        for r in (8, 16, 24):
            od.ellipse([mx - r, my2 - r, mx + r, my2 + r],
                       outline=HL + (int(255 * alpha * (1 - r / 40)),),
                       width=2)
        cap(od, alpha, "“There I will meet with you …”",
            "from between the two cherubim")


# --- the table of showbread (Exodus 25:23-30) --------------------------------

TW = int(2 * 62)
TX0 = IX + (IW - TW) // 2
TY0 = IY + 196
TLEG = 78


def inset_table(d, od, part, alpha, frac):
    panel(d, "THE TABLE FOR THE BREAD", "of the Presence")
    d.rectangle([TX0, TY0, TX0 + TW, TY0 + 10], outline=SAND, width=3)
    rim = [TX0 - 5, TY0 + 12, TX0 + TW + 5, TY0 + 21]
    d.rectangle(rim, outline=SAND, width=2)
    for lx in (TX0 + 7, TX0 + TW - 17):
        d.rectangle([lx, TY0 + 21, lx + 10, TY0 + 21 + TLEG], outline=SAND,
                    width=2)
    ry = TY0 + 30
    rings = [(TX0 + 12, ry), (TX0 + TW - 12, ry)]
    for rx, ryy in rings:
        d.ellipse([rx - 6, ryy - 6, rx + 6, ryy + 6], outline=SAND, width=2)
    d.line([(TX0 - 42, ry), (TX0 - 8, ry)], fill=SAND, width=4)
    d.line([(TX0 + TW + 8, ry), (TX0 + TW + 42, ry)], fill=SAND, width=4)
    bread = []
    for sx in (TX0 + 14, TX0 + 52):
        for i in range(3):
            bread.append([sx, TY0 - 9 - i * 7, sx + 26, TY0 - 3 - i * 7])
    for b in bread:
        d.rectangle(b, outline=SAND, width=1)
    vessels = [[TX0 + TW - 34, TY0 - 15, TX0 + TW - 24, TY0 - 2],
               [TX0 + TW - 18, TY0 - 9, TX0 + TW - 4, TY0 - 2]]
    d.rectangle(vessels[0], outline=SAND, width=1)
    d.arc(vessels[1], 180, 360, fill=SAND, width=2)

    a = g(alpha)
    if part == "body":
        od.rectangle([TX0, TY0, TX0 + TW, TY0 + 21 + TLEG], outline=a,
                     width=4)
        cap(od, alpha, "2 long × 1 wide × 1½ high", "of acacia wood")
    elif part == "gold":
        od.rectangle([TX0 - 2, TY0 - 2, TX0 + TW + 2, TY0 + 12], outline=a,
                     width=4)
        cap(od, alpha, "overlaid with pure gold", "a molding of gold around it")
    elif part == "rim":
        od.rectangle(rim, outline=a, width=4)
        cap(od, alpha, "a rim a handbreadth wide", "with a gold molding")
    elif part == "rings":
        for rx, ryy in rings:
            od.ellipse([rx - 9, ryy - 9, rx + 9, ryy + 9], outline=a,
                       width=4)
        cap(od, alpha, "four rings of gold, at the four corners")
    elif part == "rings_frame":
        for rx, ryy in rings:
            od.ellipse([rx - 9, ryy - 9, rx + 9, ryy + 9], outline=a,
                       width=3)
        od.rectangle(rim, outline=a, width=3)
        cap(od, alpha, "rings close by the rim", "holders for the poles")
    elif part == "poles":
        od.line([(TX0 - 42, ry), (TX0 - 8, ry)], fill=a, width=6)
        od.line([(TX0 + TW + 8, ry), (TX0 + TW + 42, ry)], fill=a, width=6)
        cap(od, alpha, "poles of acacia, overlaid with gold",
            "to carry the table")
    elif part == "vessels":
        for v in vessels:
            od.rectangle([v[0] - 3, v[1] - 3, v[2] + 3, v[3] + 3], outline=a,
                         width=2)
        cap(od, alpha, "plates, dishes, pitchers, and bowls",
            "all of pure gold")
    elif part == "bread":
        for b in bread:
            od.rectangle(b, outline=a, width=2)
        cap(od, alpha, "the bread of the Presence",
            "before the LORD always")


# --- the golden lampstand (Exodus 25:31-39) ----------------------------------

LCX = ICX
LTOP = IY + 140
LBASE = IY + 306
LRS = (26, 46, 66)


def _branch_arcs():
    arcs = []
    for r in LRS:
        ys = LTOP + r
        arcs.append(([LCX, ys - r, LCX + 2 * r, ys + r], 180, 270))
        arcs.append(([LCX - 2 * r, ys - r, LCX, ys + r], 270, 360))
    return arcs


def _flame_points():
    return [(LCX, LTOP)] + [(LCX + s * r, LTOP) for r in LRS
                            for s in (1, -1)]


def inset_lampstand(d, od, part, alpha, frac):
    panel(d, "THE GOLDEN LAMPSTAND", "hammered from one talent of pure gold")
    d.line([(LCX, LBASE), (LCX, LTOP)], fill=SAND, width=4)
    d.polygon([(LCX - 26, LBASE), (LCX + 26, LBASE), (LCX + 12, LBASE - 13),
               (LCX - 12, LBASE - 13)], outline=SAND, width=2)
    for bbox, a0, a1 in _branch_arcs():
        d.arc(bbox, a0, a1, fill=SAND, width=3)
    for fx, fy in _flame_points():
        d.line([(fx, fy), (fx, fy - 7)], fill=SAND, width=3)
        d.ellipse([fx - 4, fy - 17, fx + 4, fy - 6], outline=BRONZE, width=2)

    a = g(alpha)
    if part in ("whole", "one_piece"):
        od.line([(LCX, LBASE), (LCX, LTOP)], fill=a, width=6)
        for bbox, a0, a1 in _branch_arcs():
            od.arc(bbox, a0, a1, fill=a, width=4)
        if part == "whole":
            cap(od, alpha, "base, shaft, cups, buds, and flowers",
                "of hammered work, one piece")
        else:
            cap(od, alpha, "all of it a single hammered piece",
                "of pure gold")
    elif part == "branches":
        for bbox, a0, a1 in _branch_arcs():
            od.arc(bbox, a0, a1, fill=a, width=5)
        cap(od, alpha, "six branches — three on each side")
    elif part == "cups_branches":
        for r in LRS:
            ys = LTOP + r
            for base_ang, s in ((0, 1), (0, -1)):
                for ang in (200, 228, 255):
                    th = math.radians(ang if s == 1 else 540 - ang)
                    px = LCX + s * r + r * math.cos(th)
                    py = ys + r * math.sin(th)
                    od.ellipse([px - 4, py - 4, px + 4, py + 4], outline=a,
                               width=2)
        cap(od, alpha, "three cups like almond blossoms",
            "on every branch")
    elif part == "cups_shaft":
        for i in range(4):
            y = LTOP + 22 + i * 24
            od.ellipse([LCX - 5, y - 5, LCX + 5, y + 5], outline=a, width=2)
        cap(od, alpha, "and four cups on the lampstand itself")
    elif part == "buds":
        for r in LRS:
            y = LTOP + r
            od.ellipse([LCX - 6, y - 6, LCX + 6, y + 6], outline=a, width=3)
        cap(od, alpha, "a bud under each pair of branches")
    elif part == "lamps":
        for fx, fy in _flame_points():
            od.ellipse([fx - 7, fy - 20, fx + 7, fy - 3], outline=a, width=3)
        cap(od, alpha, "seven lamps, giving light in front of it")
    elif part == "tools":
        cap(od, alpha, "its snuffers and their trays", "of pure gold")
    elif part == "talent":
        cap(od, alpha, "made from a talent of pure gold",
            "about 75 pounds / 34 kg")


# --- curtains (Exodus 26:1-13) -----------------------------------------------

def _strip_boxes(n, w, gap=3, h=170):
    total = n * w + (n - 1) * gap
    x0 = IX + (IW - total) // 2
    y0 = IY + 80
    return [[x0 + i * (w + gap), y0, x0 + i * (w + gap) + w, y0 + h]
            for i in range(n)]


def inset_curtains(d, od, part, alpha, frac, kind="linen"):
    if kind == "linen":
        panel(d, "THE TABERNACLE CURTAINS",
              "fine linen — blue, purple, and scarlet")
        boxes = _strip_boxes(10, 25)
        for i, b in enumerate(boxes):
            col = tuple(c // 2 for c in GATE_COLORS[i % 3])
            d.rectangle(b, fill=col, outline=SAND_DIM)
        split = 5
    else:
        panel(d, "THE TENT OF GOATS' HAIR", "spread over the tabernacle")
        boxes = _strip_boxes(11, 23, gap=2)
        for b in boxes:
            d.rectangle(b, fill=(58, 56, 52), outline=SAND_DIM)
        split = 5 if part != "six_five" else 5
    mid_l = boxes[split - 1][2]
    mid_r = boxes[split][0]
    y0, y1 = boxes[0][1], boxes[0][3]

    a = g(alpha)
    if part in ("ten", "eleven"):
        for b in boxes:
            od.rectangle(b, outline=a, width=2)
        if part == "ten":
            cap(od, alpha, "ten curtains, cherubim worked into them")
        else:
            cap(od, alpha, "eleven curtains — a tent over the tabernacle")
    elif part == "size":
        od.rectangle(boxes[2], outline=a, width=3)
        if kind == "linen":
            cap(od, alpha, "each curtain 28 cubits by 4", "all one measure")
        else:
            cap(od, alpha, "each curtain 30 cubits by 4", "all one measure")
    elif part == "five_five":
        od.rectangle([boxes[0][0] - 4, y0 - 4, mid_l + 2, y1 + 4],
                     outline=a, width=3)
        od.rectangle([mid_r - 2, y0 - 4, boxes[-1][2] + 4, y1 + 4],
                     outline=a, width=3)
        cap(od, alpha, "five joined to five — two great sets")
    elif part == "six_five":
        od.rectangle([boxes[0][0] - 4, y0 - 4, mid_l + 2, y1 + 4],
                     outline=a, width=3)
        od.rectangle([mid_r - 2, y0 - 4, boxes[-1][2] + 4, y1 + 4],
                     outline=a, width=3)
        b6 = boxes[5]
        od.rectangle([b6[0], y0 - 12, b6[2], y0 + 10], outline=a, width=3)
        cap(od, alpha, "five and six — the sixth doubled",
            "at the front of the tent")
    elif part == "loops_edge":
        for i in range(6):
            y = y0 + 12 + i * 28
            od.arc([mid_l - 8, y - 5, mid_l + 4, y + 5], 270, 90, fill=a,
                   width=2)
        cap(od, alpha, "loops of blue on the edge",
            "of the end curtain")
    elif part == "loops_50":
        for i in range(6):
            y = y0 + 12 + i * 28
            od.arc([mid_l - 8, y - 5, mid_l + 4, y + 5], 270, 90, fill=a,
                   width=2)
            od.arc([mid_r - 4, y - 5, mid_r + 8, y + 5], 90, 270, fill=a,
                   width=2)
        cap(od, alpha, "fifty loops on each edge",
            "opposite one another")
    elif part in ("clasps_gold", "clasps_bronze"):
        col = a if part == "clasps_gold" else BRONZE + (int(255 * alpha),)
        for i in range(8):
            y = y0 + 8 + i * 22
            od.ellipse([(mid_l + mid_r) / 2 - 4, y - 4,
                        (mid_l + mid_r) / 2 + 4, y + 4], outline=col,
                       width=2)
        if part == "clasps_gold":
            cap(od, alpha, "fifty clasps of gold — one tabernacle")
        else:
            cap(od, alpha, "fifty clasps of bronze — one tent")
    elif part == "overhang":
        dashed_rect(od, [boxes[0][0], y1 + 6, boxes[-1][2], y1 + 26], a, 2)
        cap(od, alpha, "the extra half curtain hangs over",
            "the back of the tabernacle")
    elif part == "sides":
        dashed_rect(od, [boxes[0][0] - 18, y0, boxes[0][0] - 6, y1], a, 2)
        dashed_rect(od, [boxes[-1][2] + 6, y0, boxes[-1][2] + 18, y1], a, 2)
        cap(od, alpha, "a cubit of overhang on either side",
            "to cover the tabernacle")


def inset_coverings(d, od, part, alpha, frac):
    panel(d, "THE COVERINGS OF THE TENT", "layered over the curtains")
    layers = [("fine leather, above all", BROWN),
              ("rams' skins, dyed red", RED),
              ("curtains of goats' hair", (85, 82, 76)),
              ("fine linen with cherubim (innermost)",
               tuple(c // 2 for c in WHITE_LINEN))]
    boxes = []
    for i, (name, col) in enumerate(layers):
        y = IY + 92 + i * 50
        box = [IX + 40, y, IX + IW - 40, y + 34]
        boxes.append(box)
        d.rectangle(box, fill=col, outline=SAND_DIM)
        d.text((ICX, y + 17), name, font=F_SMALL, fill=WHITE_LINEN,
               anchor="mm")
    od.rectangle([b - 3 for b in boxes[0][:2]] + [b + 3 for b in boxes[0][2:]],
                 outline=g(alpha), width=3)
    od.rectangle([b - 3 for b in boxes[1][:2]] + [b + 3 for b in boxes[1][2:]],
                 outline=g(alpha), width=3)
    cap(od, alpha, "two outer coverings for the tent")


# --- boards / frames (Exodus 26:15-30) ---------------------------------------

def _board_boxes(n):
    gap = 2
    w = min(14, (300 - (n - 1) * gap) // n)
    total = n * w + (n - 1) * gap
    x0 = IX + (IW - total) // 2
    y0 = IY + 96
    return [[x0 + i * (w + gap), y0, x0 + i * (w + gap) + w, y0 + 150]
            for i in range(n)], w


def _draw_boards(d, boxes, w):
    for b in boxes:
        d.rectangle(b, outline=SAND, width=2)
        bw = max(3, w // 3)
        d.rectangle([b[0], b[3] + 3, b[0] + bw, b[3] + 10], fill=SILVER)
        d.rectangle([b[2] - bw, b[3] + 3, b[2], b[3] + 10], fill=SILVER)


BAR_ROWS = (0.16, 0.33, 0.5, 0.67, 0.84)


def inset_boards(d, od, part, alpha, frac):
    panel(d, "THE BOARDS OF THE TABERNACLE",
          "standing acacia frames, in silver bases")
    a = g(alpha)
    if part in ("dims", "tenons"):
        b = [ICX - 26, IY + 82, ICX + 26, IY + 282]
        d.rectangle(b, outline=SAND, width=3)
        d.line([(b[0], b[3] - 40), (b[2], b[3] - 40)], fill=SAND_DIM, width=1)
        tabs = [[ICX - 20, b[3], ICX - 8, b[3] + 16],
                [ICX + 8, b[3], ICX + 20, b[3] + 16]]
        for tb in tabs:
            d.rectangle(tb, outline=SAND, width=2)
        if part == "dims":
            od.rectangle(b, outline=a, width=4)
            cap(od, alpha, "each board ten cubits long",
                "a cubit and a half wide")
        else:
            for tb in tabs:
                od.rectangle(tb, outline=a, width=3)
            cap(od, alpha, "two tenons in each board",
                "fitted one against another")
        return

    n = {"generic": 8, "south20": 20, "north20": 20, "bases40": 20,
         "west6": 6, "corners": 8, "corner_detail": 8, "eight16": 8,
         "bars": 20, "middle_bar": 20, "gold": 20}.get(part, 12)
    boxes, w = _board_boxes(n)
    _draw_boards(d, boxes, w)
    y0, y1 = boxes[0][1], boxes[0][3]
    x0, x1 = boxes[0][0], boxes[-1][2]

    if part == "generic":
        for b in boxes[2:6]:
            od.rectangle(b, outline=a, width=2)
        cap(od, alpha, "upright boards of acacia wood")
    elif part in ("south20", "north20"):
        m = max(1, int(n * frac))
        for b in boxes[:m]:
            od.rectangle(b, outline=a, width=2)
        side = "south" if part == "south20" else "north"
        cap(od, alpha, f"twenty boards for the {side} side")
    elif part == "bases40":
        for b in boxes:
            od.rectangle([b[0] - 1, b[3] + 1, b[2] + 1, b[3] + 12],
                         outline=a, width=2)
        cap(od, alpha, "forty bases of silver", "two under every board")
    elif part == "west6":
        for b in boxes:
            od.rectangle(b, outline=a, width=2)
        cap(od, alpha, "six boards for the west side, the rear")
    elif part == "corners":
        for b in (boxes[0], boxes[-1]):
            od.rectangle(b, outline=a, width=3)
        cap(od, alpha, "and two boards for the rear corners")
    elif part == "corner_detail":
        for b in (boxes[0], boxes[-1]):
            od.rectangle(b, outline=a, width=2)
            od.ellipse([(b[0] + b[2]) / 2 - 6, b[1] - 12,
                        (b[0] + b[2]) / 2 + 6, b[1]], outline=a, width=2)
        cap(od, alpha, "doubled beneath, joined at the top",
            "into a single ring")
    elif part == "eight16":
        for b in boxes:
            od.rectangle(b, outline=a, width=2)
        cap(od, alpha, "eight boards, with sixteen bases of silver")
    elif part in ("bars", "middle_bar"):
        for i, fy in enumerate(BAR_ROWS):
            y = y0 + (y1 - y0) * fy
            full = (i == 2)
            bx0 = x0 if (full or i in (0, 3)) else (x0 + x1) / 2
            bx1 = x1 if (full or i in (1, 4)) else (x0 + x1) / 2
            col = a if (part == "bars" or full) else SAND + (200,)
            width = 5 if (part == "middle_bar" and full) else 3
            od.line([(bx0, y), (bx1, y)], fill=col, width=width)
        if part == "bars":
            cap(od, alpha, "five bars of acacia for the boards")
        else:
            cap(od, alpha, "the middle bar runs through the boards",
                "from end to end")
    elif part == "gold":
        for b in boxes:
            od.rectangle(b, outline=a, width=2)
        y = y0 + (y1 - y0) * 0.5
        od.line([(x0, y), (x1, y)], fill=a, width=3)
        cap(od, alpha, "boards and bars overlaid with gold",
            "with rings of gold for the bars")


# --- the veil and the screen (Exodus 26:31-37) --------------------------------

def inset_hanging(d, od, part, alpha, frac, npillars=4, base_col=SILVER,
                  title="THE VEIL", subtitle="before the Most Holy Place"):
    panel(d, title, subtitle)
    cx0, cy0 = IX + 68, IY + 84
    cw, ch = 220, 150
    band = cw // 3
    for i in range(3):
        d.rectangle([cx0 + i * band, cy0, cx0 + (i + 1) * band, cy0 + ch],
                    fill=tuple(c // 2 for c in GATE_COLORS[i]),
                    outline=SAND_DIM)
    d.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], outline=WHITE_LINEN, width=2)
    d.text((cx0 + cw / 2, cy0 + ch / 2), "· cherubim ·", font=F_SMALL,
           fill=WHITE_LINEN, anchor="mm")
    pxs = [cx0 + cw * (i + 0.5) / npillars for i in range(npillars)]
    for px in pxs:
        d.line([(px, cy0 + ch), (px, cy0 + ch + 34)], fill=SAND, width=4)
        d.rectangle([px - 7, cy0 + ch + 34, px + 7, cy0 + ch + 44],
                    fill=base_col)

    a = g(alpha)
    if part in ("veil", "colors"):
        od.rectangle([cx0 - 3, cy0 - 3, cx0 + cw + 3, cy0 + ch + 3],
                     outline=a, width=4)
        if part == "veil":
            cap(od, alpha, "blue, purple, scarlet, and fine linen",
                "with cherubim skillfully worked")
        else:
            cap(od, alpha, "embroidered blue, purple, and scarlet",
                "the screen for the door of the tent")
    elif part in ("pillars4", "pillars5"):
        for px in pxs:
            od.line([(px, cy0 + ch), (px, cy0 + ch + 34)], fill=a, width=6)
            od.rectangle([px - 9, cy0 + ch + 32, px + 9, cy0 + ch + 46],
                         outline=a, width=2)
        if part == "pillars4":
            cap(od, alpha, "four pillars of acacia, overlaid with gold",
                "on bases of silver")
        else:
            cap(od, alpha, "five pillars of acacia, overlaid with gold",
                "on bases of bronze")
    elif part == "divide":
        dashed_line(od, (cx0 + cw / 2, cy0 - 8), (cx0 + cw / 2,
                    cy0 + ch + 16), a, 3)
        od.text((cx0 + cw / 2 - 56, cy0 + 22), "MOST HOLY", font=F_DIM,
                fill=a, anchor="mm")
        od.text((cx0 + cw / 2 + 56, cy0 + 22), "HOLY PLACE", font=F_DIM,
                fill=a, anchor="mm")
        cap(od, alpha, "the veil divides the Holy Place",
            "from the Most Holy")


INSETS = {
    "altar": inset_altar,
    "materials": inset_materials,
    "ark": inset_ark,
    "table": inset_table,
    "lamp": inset_lampstand,
    "linen": lambda d, od, p, a, f: inset_curtains(d, od, p, a, f, "linen"),
    "goat": lambda d, od, p, a, f: inset_curtains(d, od, p, a, f, "goat"),
    "coverings": inset_coverings,
    "boards": inset_boards,
    "veil": inset_hanging,
    "screen": lambda d, od, p, a, f: inset_hanging(
        d, od, p, a, f, npillars=5, base_col=BRONZE,
        title="THE SCREEN FOR THE DOOR", subtitle="the entrance of the tent"),
}


# ---------------------------------------------------------------------------
# Verse specs
# ---------------------------------------------------------------------------
# verse: (caption, [(plan_fn, kwargs, grows)], (inset_name, part) | None,
#         [(label, x_cubit, y_cubit)])

def wall(side):
    return (hl_wall, {"side": side}, True)


CH25 = {
    1: ("the LORD spoke to Moses", [(hl_whole, {}, False)], None, []),
    2: ("an offering from everyone whose heart is willing",
        [(hl_whole, {}, False)], None, []),
    3: ("the offering: gold, silver, and bronze", [], ("materials", "metals"), []),
    4: ("yarns, fine linen, and goats' hair", [], ("materials", "fabrics"), []),
    5: ("skins, leather, and acacia wood", [], ("materials", "skins_wood"), []),
    6: ("oil for the light, spices for oil and incense", [], ("materials", "oil_spice"), []),
    7: ("onyx and setting stones", [], ("materials", "stones"), []),
    8: ("“let them make me a sanctuary, that I may dwell among them”",
        [(hl_tent, {}, False)], None, []),
    9: ("after the pattern of the tabernacle, exactly as shown",
        [(hl_whole, {}, False)], None, []),
    10: ("an ark of acacia wood", [(hl_ark_plan, {}, False)], ("ark", "body"), []),
    11: ("overlaid with pure gold", [(hl_ark_plan, {}, False)], ("ark", "gold"), []),
    12: ("four rings of gold, on its four feet", [(hl_ark_plan, {}, False)], ("ark", "rings"), []),
    13: ("poles of acacia wood, overlaid with gold", [(hl_ark_plan, {}, False)], ("ark", "poles"), []),
    14: ("the poles in the rings, to carry the ark", [(hl_ark_plan, {}, False)], ("ark", "poles_in"), []),
    15: ("the poles shall not be taken from it", [(hl_ark_plan, {}, False)], ("ark", "poles_stay"), []),
    16: ("put the testimony into the ark", [(hl_ark_plan, {}, False)], ("ark", "testimony"), []),
    17: ("a mercy seat of pure gold", [(hl_ark_plan, {}, False)], ("ark", "mercy"), []),
    18: ("two cherubim of hammered gold", [(hl_ark_plan, {}, False)], ("ark", "cherub_two"), []),
    19: ("one cherub at each end, of one piece", [(hl_ark_plan, {}, False)], ("ark", "cherub_ends"), []),
    20: ("wings spread upward, faces to one another", [(hl_ark_plan, {}, False)], ("ark", "wings"), []),
    21: ("the mercy seat on the ark; the testimony within", [(hl_ark_plan, {}, False)], ("ark", "seat_on_ark"), []),
    22: ("“there I will meet with you”", [(hl_ark_plan, {}, False)], ("ark", "meet"), []),
    23: ("a table of acacia wood", [(hl_table_plan, {}, False)], ("table", "body"), []),
    24: ("overlaid with pure gold, with a gold molding", [(hl_table_plan, {}, False)], ("table", "gold"), []),
    25: ("a rim of a handbreadth around it", [(hl_table_plan, {}, False)], ("table", "rim"), []),
    26: ("four gold rings at the four corners", [(hl_table_plan, {}, False)], ("table", "rings"), []),
    27: ("the rings close by the rim, to hold the poles", [(hl_table_plan, {}, False)], ("table", "rings_frame"), []),
    28: ("poles of acacia, overlaid with gold", [(hl_table_plan, {}, False)], ("table", "poles"), []),
    29: ("its plates, dishes, pitchers, and bowls of gold", [(hl_table_plan, {}, False)], ("table", "vessels"), []),
    30: ("the bread of the Presence, before me always", [(hl_table_plan, {}, False)], ("table", "bread"), []),
    31: ("a lampstand of hammered pure gold", [(hl_lamp, {}, False)], ("lamp", "whole"), []),
    32: ("six branches going out of its sides", [(hl_lamp, {}, False)], ("lamp", "branches"), []),
    33: ("three almond-blossom cups on each branch", [(hl_lamp, {}, False)], ("lamp", "cups_branches"), []),
    34: ("four cups on the lampstand itself", [(hl_lamp, {}, False)], ("lamp", "cups_shaft"), []),
    35: ("a bud under each pair of branches", [(hl_lamp, {}, False)], ("lamp", "buds"), []),
    36: ("all of it one hammered piece of pure gold", [(hl_lamp, {}, False)], ("lamp", "one_piece"), []),
    37: ("seven lamps, giving light in front of it", [(hl_lamp, {}, False)], ("lamp", "lamps"), []),
    38: ("its snuffers and trays of pure gold", [(hl_lamp, {}, False)], ("lamp", "tools"), []),
    39: ("made from a talent of pure gold", [(hl_lamp, {}, False)], ("lamp", "talent"), []),
    40: ("“after the pattern shown you on the mountain”",
         [(hl_whole, {}, False)], None, []),
}

CH26 = {
    1: ("ten curtains of fine linen — blue, purple, scarlet",
        [(hl_tent, {}, False)], ("linen", "ten"), []),
    2: ("each curtain 28 cubits by 4", [], ("linen", "size"), []),
    3: ("five coupled together, and five", [], ("linen", "five_five"), []),
    4: ("loops of blue on the edge of the end curtain", [], ("linen", "loops_edge"), []),
    5: ("fifty loops, opposite one another", [], ("linen", "loops_50"), []),
    6: ("fifty clasps of gold — one tabernacle", [], ("linen", "clasps_gold"), []),
    7: ("eleven curtains of goats' hair, for a tent",
        [(hl_tent, {}, False)], ("goat", "eleven"), []),
    8: ("each curtain 30 cubits by 4", [], ("goat", "size"), []),
    9: ("five and six; the sixth doubled at the front", [], ("goat", "six_five"), []),
    10: ("fifty loops on the edges of the sets", [], ("goat", "loops_50"), []),
    11: ("fifty clasps of bronze — one tent", [], ("goat", "clasps_bronze"), []),
    12: ("the remnant hangs over the back", [], ("goat", "overhang"), []),
    13: ("a cubit of overhang on either side", [], ("goat", "sides"), []),
    14: ("coverings of rams' skins dyed red, and fine leather", [], ("coverings", ""), []),
    15: ("upright boards of acacia wood", [(hl_tent, {}, False)], ("boards", "generic"), []),
    16: ("each board ten cubits by a cubit and a half", [], ("boards", "dims"), []),
    17: ("two tenons in each board", [], ("boards", "tenons"), []),
    18: ("twenty boards for the south side",
         [(hl_tent_wall, {"side": "south"}, True)], ("boards", "south20"), []),
    19: ("forty silver bases — two under each board",
         [(hl_tent_wall, {"side": "south"}, False)], ("boards", "bases40"), []),
    20: ("twenty boards for the north side",
         [(hl_tent_wall, {"side": "north"}, True)], ("boards", "north20"), []),
    21: ("and their forty bases of silver",
         [(hl_tent_wall, {"side": "north"}, False)], ("boards", "bases40"), []),
    22: ("six boards for the west, the rear",
         [(hl_tent_wall, {"side": "west"}, True)], ("boards", "west6"), []),
    23: ("two boards for the corners at the rear",
         [(hl_tent_wall, {"side": "west"}, False)], ("boards", "corners"), []),
    24: ("doubled beneath, joined at the top in one ring",
         [(hl_tent_wall, {"side": "west"}, False)], ("boards", "corner_detail"), []),
    25: ("eight boards, sixteen bases of silver",
         [(hl_tent_wall, {"side": "west"}, False)], ("boards", "eight16"), []),
    26: ("five bars of acacia for the one side",
         [(hl_tent_wall, {"side": "south"}, False)], ("boards", "bars"), []),
    27: ("five for the other side, five for the rear",
         [(hl_tent_wall, {"side": "north"}, False),
          (hl_tent_wall, {"side": "west"}, False)], ("boards", "bars"), []),
    28: ("the middle bar, from end to end",
         [(hl_tent, {}, False)], ("boards", "middle_bar"), []),
    29: ("boards overlaid with gold, rings of gold for the bars",
         [(hl_tent, {}, False)], ("boards", "gold"), []),
    30: ("“raise up the tabernacle according to its plan”",
         [(hl_tent, {}, False)], None, []),
    31: ("a veil of blue, purple, and scarlet, with cherubim",
         [(hl_veil_plan, {}, False)], ("veil", "veil"), []),
    32: ("on four gold-overlaid pillars, in silver bases",
         [(hl_veil_plan, {}, False)], ("veil", "pillars4"), []),
    33: ("the veil separates the Holy Place from the Most Holy",
         [(hl_veil_plan, {}, False), (hl_ark_plan, {}, False)],
         ("veil", "divide"), []),
    34: ("the mercy seat on the ark, in the Most Holy Place",
         [(hl_ark_plan, {}, False)], None,
         [("the mercy seat, in the Most Holy", 25, 36.5)]),
    35: ("the table on the north; the lampstand on the south",
         [(hl_table_plan, {}, False), (hl_lamp, {}, False)], None,
         [("table north · lampstand south", 25, 36.5)]),
    36: ("a screen for the door of the tent, embroidered",
         [(hl_tent_wall, {"side": "door"}, False)], ("screen", "colors"), []),
    37: ("five pillars of acacia, with bases of bronze",
         [(hl_tent_wall, {"side": "door"}, False)], ("screen", "pillars5"), []),
}

CH27 = {
    1: ("the altar — five cubits square, three high", [(hl_altar_plan, {}, False)], ("altar", "body"), []),
    2: ("horns on its four corners", [(hl_altar_plan, {}, False)], ("altar", "horns"), []),
    3: ("its vessels — pots, shovels, basins, forks, firepans", [(hl_altar_plan, {}, False)], ("altar", "utensils"), []),
    4: ("a grating, a network of bronze", [(hl_altar_plan, {}, False)], ("altar", "grate"), []),
    5: ("the grate set halfway up the altar", [(hl_altar_plan, {}, False)], ("altar", "grate_mid"), []),
    6: ("poles of acacia, overlaid with bronze", [(hl_altar_plan, {}, False)], ("altar", "poles"), []),
    7: ("poles in the rings, to carry it", [(hl_altar_plan, {}, False)], ("altar", "rings"), []),
    8: ("hollow, made with boards", [(hl_altar_plan, {}, False)], ("altar", "hollow"), []),
    9: ("south side — hangings of 100 cubits", [wall("south")], None,
        [("100 cubits of fine twined linen", 50, 44)]),
    10: ("its twenty pillars on bronze sockets", [(hl_pillars, {"side": "south"}, True)], None,
         [("20 pillars · bronze sockets · silver hooks", 50, 44)]),
    11: ("north side likewise — 100 cubits, twenty pillars",
         [wall("north"), (hl_pillars, {"side": "north"}, True)], None,
         [("100 cubits · 20 pillars", 50, 6)]),
    12: ("west side — hangings of 50 cubits, ten pillars",
         [wall("west"), (hl_pillars, {"side": "west"}, True)], None,
         [("50 cubits · 10 pillars", 13, 6)]),
    13: ("the east side, toward the sunrise — 50 cubits",
         [wall("east_full")], None, [("50 cubits", 88, 6)]),
    14: ("fifteen cubits of hangings on one side of the gate",
         [wall("east_flank_s")], None, [("15 cubits · 3 pillars", 85, 44)]),
    15: ("fifteen cubits on the other side",
         [wall("east_flank_n")], None, [("15 cubits · 3 pillars", 85, 6)]),
    16: ("the gate — a 20-cubit screen of blue, purple, and scarlet",
         [wall("gate"), (hl_pillars, {"side": "gate"}, False)], None,
         [("embroidered screen · 4 pillars", 80, 40)]),
    17: ("all the pillars — silver bands, bronze sockets",
         [(hl_pillars, {"side": "all"}, True)], None,
         [("silver hooks and bands · bronze sockets", 50, 44)]),
    18: ("the court: 100 long, 50 wide, 5 high",
         [(hl_dims, {}, False)], None,
         [("hangings 5 cubits high, of fine twined linen", 50, 44)]),
    19: ("all the pegs of the court — bronze",
         [(hl_pegs, {}, True)], None, [("bronze tent pegs", 50, 44)]),
    20: ("pure beaten olive oil, for the lamp to burn continually",
         [(hl_lamp, {}, False)], None, [("the lampstand", 30, 33)]),
    21: ("Aaron tends the lamp in the tent, outside the veil",
         [(hl_tent, {}, False), (hl_lamp, {}, False)], None,
         [("evening to morning, before the LORD", 25, 36.5)]),
}

CHAPTERS = {25: CH25, 26: CH26, 27: CH27}


# ---------------------------------------------------------------------------
# Frame renderer
# ---------------------------------------------------------------------------

def render_verse(chapter, verse):
    caption, highlights, inset, labels = CHAPTERS[chapter][verse]
    frames = []
    for i in range(FRAMES):
        t = i / FRAMES
        alpha = 0.62 + 0.38 * pulse(t)
        grow = ease(min(1.0, t / 0.55)) if FRAMES > 1 else 1.0

        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        draw_plan(d, dim=bool(inset))
        draw_chrome(d, chapter, verse, caption)

        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)

        if inset:
            name, part = inset
            INSETS[name](d, od, part, alpha, grow)
        for fn, kwargs, grows in highlights:
            fn(od, alpha=alpha, frac=grow if grows else 1.0, **kwargs)
        la = int(255 * min(1.0, grow * 1.4))
        for text, x, y in labels:
            od.text(cub(x, y), text, font=F_DIM, fill=HL + (la,),
                    anchor="mm")
        if chapter == 27 and verse == 18:
            for text, x, y in DIM_LABELS:
                od.text(cub(x, y), text, font=F_DIM,
                        fill=HL + (int(255 * alpha),), anchor="mm")

        img = Image.alpha_composite(img.convert("RGBA"), overlay)
        frames.append(img.convert("RGB"))

    out = out_path("Exodus", chapter, f"Exodus_{chapter}_{verse}.webp")
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=FRAME_MS, loop=0, quality=82, method=4)
    return out


if __name__ == "__main__":
    grand = 0
    for chapter in sorted(CHAPTERS):
        total = 0
        for v in sorted(CHAPTERS[chapter]):
            out = render_verse(chapter, v)
            total += os.path.getsize(out)
        print(f"Exodus {chapter}: {len(CHAPTERS[chapter])} animations, "
              f"{total/1e6:.1f} MB")
        grand += total
    print(f"TOTAL: {sum(len(c) for c in CHAPTERS.values())} files, "
          f"{grand/1e6:.1f} MB")
