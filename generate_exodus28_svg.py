"""Render Exodus 28 (43 verses) as per-verse vector SVGs — the priestly
garments, made one at a time on the body that will wear them.

The chapter is a build list, and it says so at v4: a breastplate, an ephod, a
robe, a coat of checker work, a turban, and a sash. Then it makes them, in
that order, for thirty-five verses. So the frame is the one the chapter
already has:

  * a priest at full height on the left, dressed a garment per verse;
  * the manifest of v4 down the left edge, ticking off as each is finished —
    which is the whole progress indicator, so nothing counts the verses;
  * a detail panel on the right carrying the piece currently being made, at
    the scale you can read it;
  * the five materials of v5 along the foot, lit whenever the text names
    them again (vv6, 8, 15) — which is how "like the work of the ephod you
    shall make it" gets said without a caption.

Garments are drawn in *wearing* order and gated by the verse that makes
them, so the coat made last at v39 still comes out underneath the robe made
at v31. That is the layering the chapter's own order would otherwise hide.

Three things this chapter is about that a costume plate leaves out, and that
the drawing carries instead:

  the names   Twelve tribes, borne twice — six and six on the shoulder
              stones (v12, "for a memorial") and all twelve over the heart
              (v29, "continually"). The same twelve names in two places on
              one body is the chapter's argument, so v29 draws the link.
  the signet  Everything that carries a name is cut like a seal — v11 on the
              shoulder stones, v21 on the twelve, v36 on the plate. One mark,
              three times.
  the stakes  v35 and v43 both end "that he not die", and v38 has Aaron
              bearing the iniquity of the holy things. The bells are not
              ornament; they are why he comes out again.

Two readings are worth flagging as inference rather than text. v10 orders
the shoulder-stone names "in the order of their birth" but does not list
them, so the twelve come from Genesis 29-30 and 35: Reuben, Simeon, Levi,
Judah, Dan, Naphtali, Gad, Asher, Issachar, Zebulun, Joseph, Benjamin. And
v21 gives the breastplate no order at all, so it is drawn in the same one —
noted here because the drawing cannot show a hedge.

Translation: WEB throughout, per config.json. The stone names of vv17-20
differ materially between versions (WEB ruby/turquoise/jacinth/chrysolite
against AV sardius/carbuncle/ligure/beryl), and the graphics are
translation-generic, so the WEB names are what is lettered — the same call
2 Peter made for its ladder. The tribe names, which carry the chapter's
argument, are stable across versions.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_exodus28_svg.py
"""

import os

import svg_figures as F
import svg_priest as G
from svg_surface import SvgCanvas
from svg_vocab import dim, text_w, arrow
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, TEXT,
                                 TEXT_DIM, HL, GOLD, RED, BROWN,
                                 SILVER, GATE_COLORS, out_path)

BOOK = "Exodus"
CHAPTER = 28
SLUG = "Exodus_28"

# One chapter, so the reading position is simply the verse: there is no
# cross-chapter offset for svg_vocab.reading_position to compute. Every
# element is gated on `v >= n` (draw once, then hold) and animates only where
# `v == n`.
CH_LEN = {28: 43}

# The four dyed and spun materials of v5 come from the tabernacle palette, so
# the ephod is woven in the same colours as the gate and the veil that
# Exodus 25-27 already drew, and Numbers 3-4 drapes its holy things in.
BLUE, PURPLE, SCARLET, LINEN = GATE_COLORS

FLESH = (96, 80, 66)            # the body's mass, before anything is on it
LACE = BLUE                     # "a lace of blue" — v28, v37


# ---------------------------------------------------------------------------
# The twelve, the stones, the manifest
# ---------------------------------------------------------------------------

TRIBES = ["REUBEN", "SIMEON", "LEVI", "JUDAH", "DAN", "NAPHTALI",
          "GAD", "ASHER", "ISSACHAR", "ZEBULUN", "JOSEPH", "BENJAMIN"]

# vv17-20, four rows of three, in the text's order. The colours are the
# drawing's own: at this size a stone is read by its colour, and twelve
# named-but-identical cells would say nothing the list does not already say.
STONES = [("ruby", (196, 62, 66)), ("topaz", (220, 168, 74)),
          ("beryl", (118, 186, 158)),
          ("turquoise", (84, 178, 190)), ("sapphire", (78, 104, 192)),
          ("emerald", (60, 158, 96)),
          ("jacinth", (214, 122, 62)), ("agate", (172, 146, 120)),
          ("amethyst", (150, 108, 190)),
          ("chrysolite", (196, 200, 106)), ("onyx", (108, 110, 124)),
          ("jasper", (172, 82, 78))]

MATERIALS = [("GOLD", GOLD), ("BLUE", BLUE), ("PURPLE", PURPLE),
             ("SCARLET", SCARLET), ("FINE LINEN", LINEN)]

# The verses that re-name the whole set — "like the work of the ephod you
# shall make it".
MATERIAL_VERSES = (5, 6, 8, 15)

# v4's list, with the verse each piece is finished on. The breeches of v42
# are not on it: the chapter adds a seventh garment after the six it named,
# and it is the one with "that they don't bear iniquity, and die" attached.
MANIFEST = [("BREASTPLATE", "of judgment", 15, 30),
            ("EPHOD", "the skillful workman", 6, 14),
            ("ROBE", "all of blue", 31, 35),
            ("COAT", "checker work", 39, 39),
            ("TURBAN", "fine linen", 39, 39),
            ("SASH", "the embroiderer", 39, 39)]

SONS = ["NADAB", "ABIHU", "ELEAZAR", "ITHAMAR"]


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

FX, FGY, FH = 248, 520, 390          # the priest: centre, ground, height
FORM = G.Form(FX, FGY, FH)

MX, MY, MSTEP = 26, 152, 41          # the manifest strip
PX0, PY0, PX1, PY1 = 372, 108, 1000, 528     # the detail panel
PCX = (PX0 + PX1) / 2

# The breastplate at working scale. Sized so the whole assembly of vv23-28 —
# four rings, two chains, two ephod rings and the band they are laced above —
# clears the materials key at the foot.
BP_X0, BP_Y0, BP_W = 470, 212, 248
BP_CW, BP_CH = BP_W / 3, BP_W / 4

MAT_Y = 552                          # the materials key along the foot


# ---------------------------------------------------------------------------
# Figures drawn from the shared vocabulary (v1, v3, v40, v41)
# ---------------------------------------------------------------------------

MAN_UNITS = F.bbox((F.man(), 0))[3] - F.bbox((F.man(), 0))[2]
_paint_cache = {}


def paint(col, width):
    key = (tuple(col), width)
    if key not in _paint_cache:
        k = width / 1.9
        _paint_cache[key] = {m: (f, s, w * k)
                             for m, (f, s, w) in
                             F.palette(tuple(col[:3]), BG).items()}
    return _paint_cache[key]


def person(c, x, gy, h, col, kind="man", width=1.9, arms="down"):
    parts = {"priest": F.priest, "child": F.child}.get(kind, F.man)(arms=arms)
    F.draw(c, parts, x, gy, h / MAN_UNITS, col, BG, style=paint(col, width))


# ---------------------------------------------------------------------------
# Page furniture
# ---------------------------------------------------------------------------


def header(c, v):
    c.text((28, 24), "Exodus 28", 23, TEXT, "la", bold=True)
    c.text((28, 54), f"v{v}", 13, dim(TEXT_DIM, 0.85), "la", italic=True)


def phrase(c, xy, s, size=24, col=None, first=False):
    """A hinge-verse phrase: caps, bold, ringed once on the verse it lands.
    The ring is measured off the real advance width, never estimated."""
    col = col or HL
    c.text(xy, s, size, col, "mm", bold=True)
    if first:
        w = text_w(s, size, bold=True) + size * 1.30
        h = size * 1.80
        c.pulse_rect(xy[0] - w / 2, xy[1] - h / 2, w, h, dim(col, 0.75),
                     width=1.7, first=True, rx=h / 2)


def title(c, s, sub=None):
    c.text((PX0 + 14, 120), s, 16.5, TEXT, "la", bold=True)
    if sub:
        c.text((PX0 + 14, 143), sub, 11.5, dim(TEXT_DIM, 0.95), "la",
               italic=True)


def manifest(c, v):
    """v4's six garments down the left edge. A piece is outlined when the
    chapter starts it, filled when it finishes it. This is the only thing on
    the page that tracks progress, and it tracks the chapter's progress
    rather than the verse number's."""
    c.text((MX, MY - 26), "TO BE MADE", 10.5, dim(TEXT_DIM, 0.9), "la",
           bold=True)
    for i, (name, note, starts, ends) in enumerate(MANIFEST):
        y = MY + i * MSTEP
        started, done = v >= starts, v >= ends
        live = starts <= v <= ends
        col = HL if live else (TEXT if done else dim(TEXT_DIM, 0.85))
        c.rect(MX, y - 12, 13, 13, fill=GOLD if done else None,
               stroke=col if started else dim(SAND_DIM, 0.9), width=1.5,
               rx=2)
        c.text((MX + 22, y - 6), name, 11.5, col, "la", bold=live or done)
        c.text((MX + 22, y + 8), note, 8.8, dim(TEXT_DIM, 0.8), "la",
               italic=True)
        if live and v == starts:
            c.pulse_rect(MX - 5, y - 20, 140, 34, dim(HL, 0.85), width=1.5,
                         first=True, rx=5)
    # The seventh, added after the six were named.
    if v >= 42:
        y = MY + len(MANIFEST) * MSTEP
        c.line((MX, y - 24), (MX + 128, y - 24), dim(SAND_DIM, 0.9), 1.2,
               dash="4,4")
        c.rect(MX, y - 12, 13, 13, fill=GOLD if v >= 43 else None,
               stroke=HL, width=1.5, rx=2)
        c.text((MX + 22, y - 6), "BREECHES", 11.5, HL, "la", bold=True)
        c.text((MX + 22, y + 8), "not in the list of v4", 8.8,
               dim(TEXT_DIM, 0.8), "la", italic=True)


def materials(c, v, lit=None):
    """The five of v5 along the foot. `lit` names the ones this verse calls
    for; when the verse names the whole set they all come up together."""
    lit = set(MATERIALS[i][0] for i in range(5)) if lit is None else set(lit)
    x = PX0 + 8
    for name, col in MATERIALS:
        on = name in lit and v >= 5
        c.rect(x, MAT_Y - 9, 22, 13, fill=col if on else dim(col, 0.30),
               stroke=dim(SAND_DIM, 0.9) if not on else col, width=1.0, rx=2)
        c.text((x + 28, MAT_Y - 2), name, 9.5,
               TEXT if on else dim(TEXT_DIM, 0.75), "la", bold=on)
        x += 40 + text_w(name, 9.5, bold=True)


# ---------------------------------------------------------------------------
# The priest — dressed in wearing order, gated by the verse that makes it
# ---------------------------------------------------------------------------


def robe_hem():
    return FGY - FH * 0.085


def figure(c, v):
    """The body, and every garment the chapter has made by verse `v`."""
    G.body(c, FORM, dim(SAND, 0.95), FLESH, rule=dim(SAND_DIM, 0.95),
           cloth=v < 39)

    if v >= 42:                                   # worn first, made last
        G.breeches(c, FORM, dim(LINEN, 0.85), hidden=v >= 39)
    if v >= 39:
        G.coat(c, FORM, dim(LINEN, 0.55), dim(SAND_DIM, 0.95))
    hem = robe_hem()
    if v >= 31:
        G.robe(c, FORM, dim(BLUE, 0.90), dim(SILVER, 0.75),
               hem_y=hem, collar=v >= 32)
    if v >= 33:
        # v33 already says "around its hem", so the ring goes all the way
        # round at once; v34's contribution is the alternation, which the
        # panel states and the hem highlight points at.
        G.hem_ring(c, FORM, hem, 11, GOLD, (BLUE, PURPLE, SCARLET))
    if v >= 6:
        G.ephod(c, FORM, dim(BROWN, 0.75), dim(GOLD, 0.85),
                band=dim(SCARLET, 0.85) if v >= 8 else None,
                straps=v >= 7, cols=[col for _n, col in MATERIALS])
    if v >= 12:
        G.shoulder_stones(c, FORM, dim(SILVER, 0.9), GOLD)
    if v >= 29:
        cells = [STONES[i][1] for i in range(12)]
        G.breastplate_on(c, FORM, GOLD, cells=cells)
    if v >= 39:
        G.sash(c, FORM, dim(SCARLET, 0.85), dim(GOLD, 0.8))
        G.turban(c, FORM, dim(LINEN, 0.80), dim(SAND_DIM, 0.95))
    if v >= 38:
        G.plate_on(c, FORM, GOLD, LACE)

    _figure_highlight(c, v)


def _figure_highlight(c, v):
    """The piece the panel is working on, ringed once on the figure, so the
    eye knows where on the body the working drawing belongs."""
    boxes = {
        7: (FX - FORM.shldr_hw - 12, FORM.shldr_y - 26,
            FORM.shldr_hw * 2 + 24, 48),
        12: (FX - FORM.shldr_hw - 12, FORM.shldr_y - 26,
             FORM.shldr_hw * 2 + 24, 48),
        29: (FX - FH * 0.098, FORM.chest_y - FH * 0.098,
             FH * 0.196, FH * 0.196),
        31: (FX - FORM.hem_hw - 10, FORM.shldr_y - 14,
             FORM.hem_hw * 2 + 20, robe_hem() - FORM.shldr_y + 28),
        34: (FX - FORM.hem_hw - 14, robe_hem() - 16,
             FORM.hem_hw * 2 + 28, 34),
        38: (FX - FORM.head_r * 1.5, FORM.brow_y - 14,
             FORM.head_r * 3.0, 28),
        42: (FX - FORM.waist_hw - 10, FORM.waist_y - 12,
             FORM.waist_hw * 2 + 20, FORM.thigh_y - FORM.waist_y + 24),
    }
    if v in boxes:
        x, y, w, h = boxes[v]
        c.pulse_rect(x, y, w, h, dim(HL, 0.9), width=1.8, first=True, rx=6)


# ---------------------------------------------------------------------------
# Working drawings used by more than one verse
# ---------------------------------------------------------------------------


def woven_trapezoid(c, cx, yt, yb, hwt, hwb, cols, rule, step=7.5):
    """A garment panel at working scale, woven of the five materials."""
    pts = [(cx - hwt, yt), (cx + hwt, yt), (cx + hwb, yb), (cx - hwb, yb)]
    G.weave(c, pts, cols, rule, step=step, width=step * 0.68,
            base=dim(BROWN, 0.55))
    return pts


def bp_cell(i):
    """Centre of breastplate cell `i` in the working drawing."""
    r, k = divmod(i, 3)
    return (BP_X0 + k * BP_CW + BP_CW / 2, BP_Y0 + r * BP_CH + BP_CH / 2)


BP_RINGS_TOP = [(BP_X0 + 10, BP_Y0 + 8), (BP_X0 + BP_W - 10, BP_Y0 + 8)]
BP_RINGS_BOT = [(BP_X0 + 10, BP_Y0 + BP_W - 8),
                (BP_X0 + BP_W - 10, BP_Y0 + BP_W - 8)]
EPH_RINGS = [(BP_X0 + 10, BP_Y0 + BP_W + 24),
             (BP_X0 + BP_W - 10, BP_Y0 + BP_W + 24)]
SETTINGS = [(BP_X0 + 26, BP_Y0 - 42), (BP_X0 + BP_W - 26, BP_Y0 - 42)]


def breastplate_panel(c, v):
    """vv15-30 — the breastplate, built up and then held. Everything added
    after v15 stays; nothing moves once it is placed."""
    rows = 0 if v < 17 else min(4, v - 16)
    if v >= 21:
        rows = 4
    cells = [STONES[i][1] if i < rows * 3 else None for i in range(12)]
    labels = TRIBES if v >= 21 else [""] * 12
    subs = [STONES[i][0] if i < rows * 3 else "" for i in range(12)]
    G.breastplate_plate(c, BP_X0, BP_Y0, BP_W, dim(GOLD, 0.95), GOLD,
                        cells=cells, labels=labels, sub=subs,
                        text_col=(20, 18, 14), sub_col=dim((20, 18, 14), 0.8),
                        fold=dim(SILVER, 0.9) if v >= 16 else None,
                        size=11.5, sub_size=8.5)
    if v >= 23:
        for p in BP_RINGS_TOP:
            G.ring(c, p[0], p[1], 7, GOLD, 2.2)
    if v >= 25:
        for p in SETTINGS:
            G.setting_box(c, p[0], p[1], 30, 22, dim(SILVER, 0.9), GOLD)
    if v >= 24:
        for i, p in enumerate(BP_RINGS_TOP):
            end = SETTINGS[i] if v >= 25 else (p[0], BP_Y0 - 42)
            G.braided_chain(c, p, end, GOLD, 1.9)
    if v >= 26:
        for p in BP_RINGS_BOT:
            G.ring(c, p[0], p[1], 7, GOLD, 2.2)
    if v >= 27:
        for p in EPH_RINGS:
            G.ring(c, p[0], p[1], 7, dim(GOLD, 0.8), 2.0)
        c.line((BP_X0 - 6, EPH_RINGS[0][1] + 18),
               (BP_X0 + BP_W + 6, EPH_RINGS[0][1] + 18),
               dim(SCARLET, 0.8), 6)          # the woven band, underneath
    if v >= 28:
        for i in range(2):
            c.line(BP_RINGS_BOT[i], EPH_RINGS[i], LACE, 3.0)


def shoulders_and_heart(c, v):
    """vv29-30 — the same twelve names in two places on one body.

    The working drawing of vv15-28 steps aside here, because the chapter
    does: it stops making the breastplate and starts saying what wearing it
    is for. The two shoulder stones of v12 come back at full size beside the
    twelve over the heart, which is the only place in the chapter the two
    bearings are in one frame.
    """
    top = 246
    for i, px in enumerate((500, 872)):
        G.setting_box(c, px, top, 132, 116, dim(SILVER, 0.9), GOLD)
        for j in range(6):
            c.text((px, top - 41 + j * 16.4), TRIBES[i * 6 + j], 11,
                   (18, 16, 12), "mm", bold=True)
    c.text((PCX, top - 20), "TWO", 12.5, TEXT, "mm", bold=True)
    c.text((PCX, top + 2), "SHOULDERS", 12.5, TEXT, "mm", bold=True)
    c.text((PCX, top + 26), "v12", 10, dim(TEXT_DIM, 0.9), "mm", italic=True)

    hx, hy, hw = PCX, 400, 132
    c.rect(hx - hw / 2, hy - hw / 2, hw, hw, fill=None, stroke=GOLD, width=2,
           rx=3)
    cw, ch = hw / 3, hw / 4
    for i in range(12):
        r, k = divmod(i, 3)
        c.rect(hx - hw / 2 + k * cw + 4, hy - hw / 2 + r * ch + 4,
               cw - 8, ch - 8, fill=STONES[i][1], stroke=dim(GOLD, 0.8),
               width=0.8, rx=2)
    c.text((PCX, 486), "ONE HEART", 12.5, TEXT, "mm", bold=True)
    for px, sx in ((500, 1), (872, -1)):
        arrow(c, (px, top + 62), (hx - sx * hw * 0.44, hy - hw / 2 - 6),
              dim(HL, 0.85), 1.6, 7, dash="5,4")
    if v >= 30:
        # v30 — the lots put *in* the breastplate, which the fold of v16
        # made room for.
        for nm, px, sx in (("URIM", 546, 1), ("THUMMIM", 826, -1)):
            c.ellipse(px, hy, 40, 17, fill=dim(SILVER, 0.9), stroke=HL,
                      width=1.5)
            c.text((px, hy), nm, 10, (18, 16, 12), "mm", bold=True)
            arrow(c, (px + sx * 44, hy), (hx - sx * (hw / 2 + 6), hy), HL,
                  1.8, 7)


def doorway(c, x, y, w, h, col, label=None):
    """The door of the holy place — v35's in and out, v43's going in."""
    c.rect(x - w / 2, y - h, w, h, fill=dim(PANEL, 0.9), stroke=col,
           width=2.0)
    c.line((x - w / 2 - 8, y), (x + w / 2 + 8, y), col, 2.4)
    if label:
        c.text((x, y + 18), label, 10.5, dim(TEXT_DIM, 0.95), "mm",
               italic=True)


# ---------------------------------------------------------------------------
# The panel, verse by verse
# ---------------------------------------------------------------------------


def panel(c, v, first):
    # -- vv1-5: the commission ---------------------------------------------
    if v == 1:
        title(c, "AARON AND HIS SONS",
              "brought near from among the children of Israel")
        person(c, 470, 430, 190, dim(TEXT, 0.95), kind="man")
        c.text((470, 452), "AARON", 13, HL, "mm", bold=True)
        for i, nm in enumerate(SONS):
            px = 620 + i * 100
            person(c, px, 430, 140, dim(SAND, 0.95), kind="man")
            c.text((px, 452), nm, 10.5, dim(TEXT, 0.92), "mm")
        c.text((PCX + 60, 486), "that he may minister to me "
               "in the priest's office", 11, dim(TEXT_DIM, 0.95), "mm",
               italic=True)

    elif v == 2:
        title(c, "HOLY GARMENTS", "for Aaron your brother")
        phrase(c, (PCX, 300), "FOR GLORY AND FOR BEAUTY", 26, HL, first)
        c.text((PCX, 352), "the phrase returns at v40, over his sons", 11,
               dim(TEXT_DIM, 0.9), "mm", italic=True)

    elif v == 3:
        title(c, "THE WISE-HEARTED", "whom I have filled with the spirit "
              "of wisdom")
        # The workers flank the work rather than standing on it: three
        # figures overlapping one cloth read as a crowd, not as a workshop.
        c.polygon([(576, 244), (800, 244), (814, 372), (562, 372)],
                  fill=dim(LINEN, 0.35), stroke=dim(SAND, 0.9), width=1.6)
        for px, sx in ((470, 1), (906, -1)):
            person(c, px, 430, 152, dim(SAND, 0.95), arms="open")
        c.text((PCX, 306), "AARON'S GARMENTS", 12.5, dim(TEXT, 0.9), "mm",
               bold=True)
        c.text((PCX, 470), "that they make Aaron's garments "
               "to sanctify him", 11.5, dim(TEXT_DIM, 0.95), "mm",
               italic=True)

    elif v == 4:
        title(c, "THESE ARE THE GARMENTS", "which they shall make")
        for i, (name, note, _s, _e) in enumerate(MANIFEST):
            r, k = divmod(i, 3)
            bx, by = 420 + k * 190, 200 + r * 140
            c.rect(bx, by, 160, 108, fill=None, stroke=dim(SAND, 0.95),
                   width=1.6, rx=4)
            c.text((bx + 80, by + 48), name, 14, TEXT, "mm", bold=True)
            c.text((bx + 80, by + 70), note, 10, dim(TEXT_DIM, 0.9), "mm",
                   italic=True)
        if first:
            c.pulse_rect(414, 194, 552, 254, dim(HL, 0.8), width=1.8,
                         first=True, rx=6)

    elif v == 5:
        title(c, "THEY SHALL TAKE", "the materials of every piece that "
              "follows")
        for i, (name, col) in enumerate(MATERIALS):
            bx = 410 + i * 108
            c.rect(bx, 250, 88, 110, fill=col, stroke=dim(GOLD, 0.7),
                   width=1.4, rx=4)
            c.text((bx + 44, 382), name, 11, TEXT, "mm", bold=True)

    # -- vv6-14: the ephod --------------------------------------------------
    elif v in (6, 7, 8):
        title(c, "THE EPHOD", "the work of the skillful workman")
        cols = [c_ for _n, c_ in MATERIALS]
        woven_trapezoid(c, PCX, 244, 420, 104, 122, cols, dim(GOLD, 0.9))
        if v >= 7:
            for sx in (-1, 1):
                G.weave(c, [(PCX + sx * 66, 244), (PCX + sx * 100, 244),
                            (PCX + sx * 92, 176), (PCX + sx * 58, 176)],
                        cols, dim(GOLD, 0.9), step=6.5, width=4.4,
                        base=dim(BROWN, 0.55))
            c.text((PCX, 162), "TWO SHOULDER STRAPS", 11.5, HL if v == 7
                   else dim(TEXT, 0.9), "mm", bold=v == 7)
            c.text((PCX, 200), "joined to the two ends", 9.5,
                   dim(TEXT_DIM, 0.9), "mm", italic=True)
        if v >= 8:
            c.rect(PCX - 126, 420, 252, 30, fill=dim(SCARLET, 0.85),
                   stroke=dim(GOLD, 0.9), width=1.5, rx=2)
            c.text((PCX, 435), "THE SKILLFULLY WOVEN BAND", 11,
                   (22, 18, 14), "mm", bold=True)
            c.text((PCX, 472), "like its work, and of the same piece", 11,
                   HL if v == 8 else dim(TEXT_DIM, 0.95), "mm", italic=True)

    elif v in (9, 10, 11):
        title(c, "TWO ONYX STONES", "engraved with the names of the "
              "children of Israel")
        for i, cx in enumerate((548, 824)):
            names = TRIBES[i * 6:(i + 1) * 6] if v >= 10 else ()
            G.onyx_stone(c, cx, 320, 200, 178, dim(SILVER, 0.88), GOLD,
                         names=names, text_col=(20, 18, 14), size=13.5,
                         engraved=v >= 11)
            if v >= 10:
                c.text((cx, 232), "SIX NAMES", 10, dim((20, 18, 14), 0.85),
                       "mm", italic=True)
        if v >= 10:
            c.text((PCX, 440), "in the order of their birth", 12.5,
                   HL if v == 10 else dim(TEXT, 0.9), "mm",
                   bold=v == 10, italic=True)
        if v >= 11:
            G.signet(c, PCX, 320, 30, GOLD, HL)
            c.text((PCX, 368), "like the", 9.5, dim(TEXT_DIM, 0.95), "mm",
                   italic=True)
            c.text((PCX, 382), "engravings", 9.5, dim(TEXT_DIM, 0.95), "mm",
                   italic=True)
            c.text((PCX, 396), "of a signet", 9.5, dim(TEXT_DIM, 0.95), "mm",
                   italic=True)
            c.text((PCX, 472), "enclosed in settings of gold", 11,
                   dim(TEXT, 0.92), "mm", italic=True)

    elif v == 12:
        title(c, "ON HIS TWO SHOULDERS", "stones of memorial for the "
              "children of Israel")
        for i, sx in enumerate((-1, 1)):
            px = PCX + sx * 170
            G.weave(c, [(px - 84, 452), (px + 84, 452), (px + 70, 200),
                        (px - 70, 200)], [col for _n, col in MATERIALS],
                    dim(GOLD, 0.9), step=8, width=5.4,
                    base=dim(BROWN, 0.55))
            G.setting_box(c, px, 322, 132, 116, dim(SILVER, 0.9), GOLD)
            for j in range(6):
                c.text((px, 322 - 41 + j * 16.4), TRIBES[i * 6 + j], 11,
                       (18, 16, 12), "mm", bold=True)
        phrase(c, (PCX, 500), "A MEMORIAL", 22, HL, first)
        c.text((PCX, 176), "Aaron shall bear their names before Yahweh",
               11.5, dim(TEXT, 0.92), "mm", italic=True)

    elif v in (13, 14):
        title(c, "SETTINGS OF GOLD", "and two chains of pure gold")
        G.setting_box(c, 560, 300, 130, 92, dim(SILVER, 0.88), GOLD)
        c.text((560, 372), "A SETTING", 11, TEXT, "mm", bold=v == 13)
        if v >= 14:
            for i, gy in enumerate((250, 330)):
                G.braided_chain(c, (720, gy), (960, gy), GOLD, 2.4)
            c.text((840, 388), "LIKE CORDS OF BRAIDED WORK", 11.5,
                   HL if v == 14 else dim(TEXT, 0.9), "mm", bold=v == 14)
        c.text((PCX, 470), "put the braided chains on the settings", 11,
               dim(TEXT_DIM, 0.95), "mm", italic=True)

    # -- vv15-30: the breastplate ------------------------------------------
    elif 15 <= v <= 30:
        subs = {15: "the work of the skillful workman",
                16: "square and folded double",
                17: "the first row", 18: "the second row",
                19: "the third row", 20: "the fourth row",
                21: "twelve, according to their names",
                22: "chains like cords, of braided work",
                23: "two rings of gold at the two ends",
                24: "the two braided chains in the two rings",
                25: "the other two ends, on the two settings",
                26: "two rings on the edge toward the ephod inward",
                27: "two rings on the shoulder straps underneath",
                28: "bound with a lace of blue",
                29: "on his heart, continually",
                30: "the Urim and the Thummim"}
        title(c, "THE BREASTPLATE OF JUDGMENT", subs[v])
        if v == 15:
            woven_trapezoid(c, PCX, 232, 492, 130, 130,
                            [c_ for _n, c_ in MATERIALS], dim(GOLD, 0.9))
            c.text((PCX, 512), "like the work of the ephod "
                   "you shall make it", 11, HL, "mm", italic=True)
        elif v >= 29:
            shoulders_and_heart(c, v)
        else:
            breastplate_panel(c, v)
        if v == 16:
            for (ax, ay), (bx, by), lb in (
                    ((BP_X0, BP_Y0 - 22), (BP_X0 + BP_W, BP_Y0 - 22),
                     "A SPAN"),
                    ((BP_X0 + BP_W + 22, BP_Y0),
                     (BP_X0 + BP_W + 22, BP_Y0 + BP_W), "A SPAN")):
                arrow(c, (ax, ay), (bx, by), dim(SILVER, 0.95), 1.5, 7)
                arrow(c, (bx, by), (ax, ay), dim(SILVER, 0.95), 1.5, 7)
                mx_, my_ = (ax + bx) / 2, (ay + by) / 2
                c.text((mx_ + (0 if lb == "A SPAN" and ay == by else 34),
                        my_ - (10 if ay == by else 0)), lb, 10.5,
                       dim(TEXT, 0.95), "mm", bold=True)
            c.text((820, 470), "FOLDED DOUBLE", 12, HL, "mm", bold=True)
            c.text((820, 490), "which is why v30 can put", 9.5,
                   dim(TEXT_DIM, 0.95), "mm", italic=True)
            c.text((820, 504), "anything inside it", 9.5,
                   dim(TEXT_DIM, 0.95), "mm", italic=True)
        if 17 <= v <= 20:
            r = v - 17
            c.pulse_rect(BP_X0 - 6, BP_Y0 + r * BP_CH - 4, BP_W + 12,
                         BP_CH + 8, dim(HL, 0.9), width=2, first=first, rx=4)
            c.text((BP_X0 + BP_W + 30, BP_Y0 + r * BP_CH + BP_CH / 2),
                   f"ROW {r + 1}", 12, HL, "lm", bold=True)
        if v == 21:
            G.signet(c, 840, 250, 26, GOLD, HL)
            c.text((840, 296), "everyone according", 10,
                   dim(TEXT_DIM, 0.95), "mm", italic=True)
            c.text((840, 310), "to his name", 10, dim(TEXT_DIM, 0.95), "mm",
                   italic=True)
            c.text((840, 350), "FOR THE TWELVE", 12, HL, "mm", bold=True)
            c.text((840, 368), "TRIBES", 12, HL, "mm", bold=True)
        if v == 28:
            c.text((832, 470), "that the breastplate", 11, HL, "mm")
            c.text((832, 488), "may not swing out", 11, HL, "mm", bold=True)
        if v == 29:
            phrase(c, (PCX, 516), "ON HIS HEART CONTINUALLY", 19, HL, first)

    # -- vv31-35: the robe --------------------------------------------------
    elif 31 <= v <= 35:
        subs = {31: "all of blue", 32: "that it not be torn",
                33: "pomegranates, and bells of gold between them",
                34: "a golden bell and a pomegranate, around the hem",
                35: "its sound shall be heard when he goes in"}
        title(c, "THE ROBE OF THE EPHOD", subs[v])
        RF = G.Form(PCX - 120, 470, 300)
        G.robe(c, RF, dim(BLUE, 0.9), dim(SILVER, 0.8),
               hem_y=470 - 300 * 0.085, collar=v >= 32)
        if v >= 33:
            G.hem_ring(c, RF, 470 - 300 * 0.085, 11, GOLD,
                       (BLUE, PURPLE, SCARLET))
        if v == 32:
            c.circle(RF.x, RF.shldr_y - 2, 30, fill=None, stroke=HL,
                     width=2.4)
            arrow(c, (RF.x + 90, RF.shldr_y - 40), (RF.x + 34, RF.shldr_y - 8),
                  HL, 1.6, 7)
            c.text((RF.x + 96, RF.shldr_y - 50), "a binding of woven work",
                   11, HL, "lm")
            c.text((RF.x + 96, RF.shldr_y - 32),
                   "as it were the hole of a coat of mail", 10,
                   dim(TEXT_DIM, 0.95), "lm", italic=True)
        if v in (33, 34):
            # The repeating unit, drawn once at size so the alternation on
            # the hem is legible as a rule rather than as texture.
            ux = 760
            G.bell_mark(c, ux, 300, 22, GOLD)
            G.pomegranate(c, ux + 70, 302, 22, SCARLET)
            G.bell_mark(c, ux + 140, 300, 22, GOLD)
            G.pomegranate(c, ux + 210, 302, 22, BLUE)
            c.text((ux + 105, 356), "A GOLDEN BELL AND A POMEGRANATE", 11,
                   HL if v == 34 else dim(TEXT, 0.9), "mm", bold=v == 34)
            c.text((ux + 105, 376), "around the hem of the robe", 10,
                   dim(TEXT_DIM, 0.95), "mm", italic=True)
        if v == 35:
            # The sound comes off the bells and reaches through the door, so
            # the rings start at the hem rather than at the doorway: what the
            # verse guards is that he is *heard*, going in and coming out.
            hx, hy = RF.x, 470 - 300 * 0.085
            for r in (58, 96, 134, 172):
                c.path(f"M{hx + r * 0.34},{hy - r * 0.86} "
                       f"A{r},{r} 0 0 1 {hx + r * 0.34},{hy + r * 0.86}",
                       fill=None, stroke=dim(GOLD, 0.34), width=1.5)
            doorway(c, 872, 432, 118, 196, dim(GOLD, 0.9), "the holy place")
            arrow(c, (752, 316), (832, 316), HL, 2.0, 8)
            c.text((748, 316), "GOES IN", 10.5, HL, "rm", bold=True)
            arrow(c, (832, 372), (752, 372), dim(SILVER, 0.95), 2.0, 8)
            c.text((748, 372), "COMES OUT", 10.5, dim(TEXT, 0.95), "rm",
                   bold=True)
            phrase(c, (PCX + 20, 516), "THAT HE NOT DIE", 21, HL, first)

    # -- vv36-38: the plate -------------------------------------------------
    elif 36 <= v <= 38:
        subs = {36: "a plate of pure gold",
                37: "on a lace of blue, on the front of the sash",
                38: "it shall be always on his forehead"}
        title(c, "HOLY TO YAHWEH", subs[v])
        px, py = PCX - 40, 290
        if v >= 37:
            c.line((px - 190, py - 6), (px + 190, py - 6), LACE, 5)
        c.rect(px - 130, py - 34, 260, 68, fill=GOLD, stroke=HL, width=1.8,
               rx=10)
        c.text((px, py), "HOLY TO YAHWEH", 21, (24, 20, 12), "mm", bold=True)
        if v == 36:
            G.signet(c, px + 210, py, 30, GOLD, HL)
            c.text((px + 210, py + 48), "like the engravings", 9.5,
                   dim(TEXT_DIM, 0.95), "mm", italic=True)
            c.text((px + 210, py + 62), "of a signet", 9.5,
                   dim(TEXT_DIM, 0.95), "mm", italic=True)
        if v == 38:
            c.text((PCX, 396), "Aaron shall bear the iniquity "
                   "of the holy things", 12.5, TEXT, "mm")
            c.text((PCX, 418), "which the children of Israel shall "
                   "make holy in all their holy gifts", 10.5,
                   dim(TEXT_DIM, 0.95), "mm", italic=True)
            phrase(c, (PCX, 476), "ALWAYS ON HIS FOREHEAD", 20, HL, first)
            c.text((PCX, 512), "that they may be accepted before Yahweh",
                   11, dim(TEXT, 0.9), "mm", italic=True)

    # -- v39: the last three of the six -------------------------------------
    elif v == 39:
        title(c, "THE COAT, THE TURBAN, THE SASH",
              "of fine linen — the work of the embroiderer")
        # Three body stubs, each carrying one piece where it belongs. A
        # swatch would say what the cloth is; this says where it goes.
        for px, name, note in ((496, "COAT", "checker work"),
                               (700, "TURBAN", "of fine linen"),
                               (896, "SASH", "the embroiderer")):
            SF = G.Form(px, 478, 236)
            c.polyline(G.silhouette(SF), dim(SAND_DIM, 0.85), 1.3,
                       closed=True)
            if name == "COAT":
                G.coat(c, SF, dim(LINEN, 0.55), dim(SAND_DIM, 0.95))
            elif name == "TURBAN":
                G.head(c, SF, dim(SAND, 0.95), FLESH, dim(SAND_DIM, 0.95),
                       cloth=False)
                G.turban(c, SF, dim(LINEN, 0.80), dim(SAND_DIM, 0.95))
            else:
                G.sash(c, SF, dim(SCARLET, 0.85), dim(GOLD, 0.8))
            c.text((px, 502), name, 12.5, TEXT, "mm", bold=True)
            c.text((px, 520), note, 9.5, dim(TEXT_DIM, 0.95), "mm",
                   italic=True)

    # -- vv40-43: the sons, and the statute ---------------------------------
    elif v == 40:
        title(c, "FOR AARON'S SONS", "coats, sashes, and headbands")
        for i, nm in enumerate(SONS):
            px = 470 + i * 130
            person(c, px, 400, 150, dim(TEXT, 0.92), kind="man")
            c.text((px, 424), nm, 10.5, dim(TEXT, 0.92), "mm")
        phrase(c, (PCX, 486), "FOR GLORY AND FOR BEAUTY", 22, HL, False)
        c.text((PCX, 522), "the words of v2, now over his sons", 10.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)

    elif v == 41:
        title(c, "PUT THEM ON", "and shall anoint them, and consecrate "
              "them, and sanctify them")
        for i, act in enumerate(("ANOINT", "CONSECRATE", "SANCTIFY")):
            px = 470 + i * 180
            c.circle(px, 300, 46, fill=None, stroke=GOLD, width=2.0)
            c.text((px, 300), str(i + 1), 20, dim(GOLD, 0.9), "mm", bold=True)
            c.text((px, 372), act, 12.5, TEXT, "mm", bold=True)
            if i < 2:
                arrow(c, (px + 54, 300), (px + 126, 300), dim(SAND, 0.95),
                      1.8, 8)
        c.text((PCX, 448), "that they may minister to me "
               "in the priest's office", 11.5, dim(TEXT, 0.92), "mm",
               italic=True)

    elif v == 42:
        title(c, "LINEN BREECHES", "to cover the flesh of their nakedness")
        BF = G.Form(PCX, 470, 300)
        c.polyline(G.silhouette(BF), dim(SAND_DIM, 0.9), 1.3, closed=True)
        G.breeches(c, BF, dim(LINEN, 0.95), hidden=False)
        for y, lb in ((BF.waist_y, "FROM THE WAIST"),
                      (BF.thigh_y, "EVEN TO THE THIGHS")):
            c.line((BF.x + 92, y), (BF.x + 150, y), dim(SILVER, 0.9), 1.4,
                   dash="5,4")
            c.text((BF.x + 158, y), lb, 10.5, dim(TEXT, 0.95), "lm")

    else:                                                        # v43
        title(c, "WHEN THEY GO IN", "a statute forever to him and to his "
              "offspring after him")
        doorway(c, 560, 380, 130, 200, dim(GOLD, 0.9), "the Tent of Meeting")
        c.rect(770, 300, 150, 80, fill=None, stroke=dim(BROWN, 0.95),
               width=2.0)
        for i in range(4):
            c.line((770 + i * 50, 300), (770 + i * 50, 280),
                   dim(BROWN, 0.95), 2.0)
        c.text((845, 400), "the altar", 10.5, dim(TEXT_DIM, 0.95), "mm",
               italic=True)
        c.text((PCX + 60, 440), "that they don't bear iniquity, and die",
               12.5, dim(RED, 0.95), "mm", bold=True)
        phrase(c, (PCX + 60, 496), "A STATUTE FOREVER", 21, HL, first)


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------


def render(v):
    c = SvgCanvas(W, H, bg=BG)
    header(c, v)
    manifest(c, v)
    figure(c, v)
    c.line((PX0 - 18, PY0), (PX0 - 18, PY1), dim(SAND_DIM, 0.6), 1.2)
    panel(c, v, first=True)
    materials(c, v, lit=None if v in MATERIAL_VERSES else ())
    return c


def main():
    total = 0
    for v in range(1, CH_LEN[CHAPTER] + 1):
        out = out_path(BOOK, CHAPTER, f"{SLUG}_{v}.svg")
        render(v).save(out)
        total += os.path.getsize(out)
    print(f"Exodus 28: {CH_LEN[CHAPTER]} SVG files, {total / 1e3:.0f} KB")


if __name__ == "__main__":
    main()
