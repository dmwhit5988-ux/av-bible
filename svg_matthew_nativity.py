"""Matthew 1:18-25 — the birth narrative, played out in figures.

Verses 1-17 are a camera over the Old Testament family tree
(`svg_matthew_world`). At verse 18 the chapter stops reciting and starts
telling, and a tree cannot tell a story: what happens from here is a man, a
woman, an angel and a child, and the drawing has to be them.

So this half is a STAGE. One ground line, the same two people standing on it
for eight verses, and each verse changes what they are doing. Nothing is
rebuilt between verses — Joseph is in the same place in verse 25 that he was
in verse 18, having crossed the stage twice — because the whole force of the
passage is that it is one continuous thing happening to two people over a
few days.

Three things carry the sense, and they are the three the text itself uses:

  * THE GAP between Joseph and Mary. It is the plot. Verse 18 opens it
    ("before they came together"), verse 19 widens it and turns Joseph away,
    verse 24 closes it, and there is no verse where the gap means nothing.
  * THE LIGHT from above, on Mary at verse 18 and on the child at verse 25 —
    "of the Holy Spirit", which is the one thing in this chapter that no
    genealogy could have produced.
  * THE LINE, faint, running down from the top of the frame to Joseph. It is
    the last inch of the thread the first seventeen verses drew. The angel
    calls him "Joseph, son of David" and the line brightens as it is said,
    because that address is the reason the genealogy was read at all.

Rendered by generate_matthew1_svg.py. Figures come from `svg_figures` — see
that module's docstring for the one-unit / feet-on-zero conventions, and
`angel()` for what is and is not drawn on a messenger.
"""


import math

import svg_figures as F
from svg_surface import SvgCanvas, _rgb
from generate_tabernacle import (W, H, BG, SAND, SAND_DIM, TEXT, TEXT_DIM,
                                 GOLD, HL, F_TITLE, font)
from svg_chronicles_world import HUD_H, dim
from svg_surface import SvgLayer
# The marriage colour the family tree uses, so a join drawn here and a join
# drawn on the tree are the same mark.
from generate_ot_family_tree_svg import FEMALE as F_FEMALE

VERSES = range(18, 26)

# -- the stage --------------------------------------------------------------

GROUND = 470                    # the line everyone stands on
MAN_PX = 210                    # a grown figure, in pixels head to heel
SCALE = MAN_PX / 100.0          # svg_figures authors a man ~100 units tall

JOSEPH_HOME = 400               # where he stands when the two are together
MARY_HOME = 648
APART = 74                      # extra half-gap in the verses they are apart

SKY = HUD_H + 10
LABEL_Y = GROUND + 46

DUR = 2.6                       # seconds; the stage settles well inside the
                                # shortest narration in the passage (5.4 s)


def _dur(narr):
    """The move lands a beat before the reader finishes, as everywhere else
    in the project. Short verses get a short move rather than a cut."""
    if not narr:
        return DUR
    return round(max(1.4, min(DUR, narr - 1.4)), 2)


# ---------------------------------------------------------------------------
# The beats
# ---------------------------------------------------------------------------
#
# Each verse says where the two of them are, what they are doing, and what
# else is on the stage. Read down the `note` column and it is the passage.

BEATS = {
    18: dict(gap=APART, joseph="stand", mary="stand", light="mary",
             bond="betrothed",
             note="betrothed · before they came together"),
    19: dict(gap=APART * 1.45, joseph="away", mary="stand", bond="severed",
             note="a righteous man · minded to put her away secretly"),
    20: dict(gap=APART * 1.45, joseph="asleep", mary="stand", bond="severed",
             angel="raised", sonof=True,
             note="an angel of the Lord appeared to him in a dream"),
    21: dict(gap=APART * 1.45, joseph="asleep", mary="stand", bond="severed",
             angel="furled", name="JESUS",
             note="he shall save his people from their sins"),
    # The angel is gone from 22 and 23 — not because he leaves, but because
    # these two verses are not his. Matthew stops the scene to say what it
    # fulfils, and the prophet who takes the angel's place on the stage is
    # the drawing of that interruption.
    22: dict(gap=APART * 1.45, joseph="asleep", mary="stand", bond="severed",
             prophet=True,
             note="that it might be fulfilled which was spoken by the Lord"),
    23: dict(gap=APART * 1.45, joseph="asleep", mary="stand", bond="severed",
             prophet=True, immanuel=True, light="mary",
             note="“Immanuel” — God with us"),
    24: dict(gap=0, joseph="stand", mary="stand", bond="married",
             note="Joseph arose · and took his wife to himself"),
    25: dict(gap=0, joseph="stand", mary="stand", manger=True,
             bond="married", name="JESUS",
             note="her firstborn son · he named him Jesus"),
}


def _places(beat):
    """Where the two of them stand this verse."""
    g = beat.get("gap", 0)
    return JOSEPH_HOME - g, MARY_HOME + g


# ---------------------------------------------------------------------------
# What is NEW this verse
# ---------------------------------------------------------------------------
#
# Only a mark that arrives in this verse draws itself. A mark that was
# already standing at the end of the previous verse is emitted statically,
# at the state it finished in.
#
# This matters because the verses are watched back to back with the
# narration: the bond is cut once at verse 19, and verses 20-23 are all
# still severed, so tracing the cut in each of them made the same two
# strokes slash across the stage four more times. The same went for the
# prophet's quotation, drawn again in verse 23 having crossed the stage in
# verse 22. It is the same rule the tree half already follows — arrivals
# brighten, they do not rebuild — stated for a stage instead of a camera.
#
# Both tests read BEATS and nothing else, so a verse can still be rendered
# on its own, which the video renderer and the still builder rely on.

def _appeared(v, key):
    """The verse a thing comes ON the stage: falsy before, truthy now."""
    return bool(BEATS[v].get(key)) and not BEATS.get(v - 1, {}).get(key)


def _changed(v, key):
    """The verse a thing takes a new value — for the bond, which is never
    absent from verse 18 on but goes betrothed, severed, married."""
    return BEATS[v].get(key) != BEATS.get(v - 1, {}).get(key)


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

class NativityFrame:
    """The stage, one verse at a time.

    Holds nothing between verses on purpose: every verse is drawn from its
    own beat, and continuity comes from the beats agreeing with each other
    rather than from state. That is what makes a verse re-renderable on its
    own, which the video renderer and the still builder both rely on.
    """

    def __init__(self, narr=None):
        self.narr = narr or {}

    # -- pieces ------------------------------------------------------------

    def _ground(self, c):
        c.line((90, GROUND), (W - 90, GROUND), dim(SAND_DIM, 0.55), 1.2)

    def _figure(self, c, parts, x, col, dur, arrive=False, flip=1,
                gy=None, scale=None):
        if arrive:
            c._emit('<g opacity="0">')
        F.draw(c, parts, x, GROUND if gy is None else gy,
               SCALE if scale is None else scale, col, BG, flip=flip)
        if arrive:
            c._emit(f'<animate attributeName="opacity" values="0;1" '
                    f'dur="{dur * 0.55:.2f}s" begin="{dur * 0.25:.2f}s" '
                    f'fill="freeze"/></g>')

    def _beam(self, c, x, dur, top=SKY, foot=None, grow=True):
        """Light from above: a narrowing wedge, drawn as a mass rather than
        as rays. Rays at this size read as a fan of sticks; a wedge reads as
        light, and it is the only bright shape on the stage."""
        foot = GROUND if foot is None else foot
        half_hi, half_lo = 46, 18
        pts = [(x - half_hi, top), (x + half_hi, top),
               (x + half_lo, foot), (x - half_lo, foot)]
        # `grown` takes OPACITIES, not the y bounds the shape already
        # carries — passing the bounds animated the wedge to solid gold and
        # buried the figure it was supposed to fall on.
        if grow:
            c.grown(pts, GOLD, 0.0, 0.17, dur=f"{dur * 0.7:.2f}s")
        else:
            c.polygon(pts, fill=dim(GOLD, 0.17))

    def _descent(self, c, x, dur, bright):
        """The last inch of the genealogy, arriving from off the top of the
        frame. Faint in every verse, and lit in the one that names it."""
        col = dim(HL, 0.85) if bright else dim(SAND_DIM, 0.45)
        pts = [(x, SKY - 6), (x, GROUND - MAN_PX + 34)]
        if bright:
            c.traced(pts, col, 3.0, dur=f"{dur * 0.6:.2f}s")
        else:
            c.polyline(pts, col, 1.6, dash="6 7")

    def _severed(self, c, x0, x1, dur, trace=True):
        """The join between them, broken. A dashed span with a gap bitten
        out of the middle: not an absence of a line, which reads as nothing
        drawn, but a line that has been cut, which is what verse 19 is."""
        y = GROUND - 96
        mid = (x0 + x1) / 2
        for a, b in ((x0 + 26, mid - 26), (mid + 26, x1 - 26)):
            c.line((a, y), (b, y), dim(SAND_DIM, 0.6), 1.3, dash="5 6")
        # The cut itself is what moves — on the verse it happens, and only
        # there. Verse 19 was the one frame in the chapter with no motion at
        # all before this went in; verses 20-23 are still severed, and drew
        # the same two strokes again every time until `trace` was added.
        for sx in (-1, 1):
            pts = [(mid + sx * 22, y - 9), (mid + sx * 14, y + 9)]
            if trace:
                c.traced(pts, dim(TEXT_DIM, 0.8), 1.8,
                         dur=f"{dur * 0.5:.2f}s")
            else:
                c.polyline(pts, dim(TEXT_DIM, 0.8), 1.8)

    def _betrothed(self, c, x0, x1, dur, trace=True):
        """Engaged, and not yet come together: the marriage line's colour,
        drawn as one thin dashed span rather than the doubled solid one. A
        real bond, and not the finished one — which is the whole situation
        verse 18 puts them in, and what verse 19 has something to cut."""
        y = GROUND - 96
        pts = [(x0 + 26, y), (x1 - 26, y)]
        if trace:
            c.traced(pts, dim(F_FEMALE, 0.7), 1.4, dur=f"{dur * 0.6:.2f}s")
        else:
            c.polyline(pts, dim(F_FEMALE, 0.7), 1.4, dash="7 7")

    def _joined(self, c, x0, x1, dur, trace=True):
        """And made again — the doubled line the family tree draws for a
        marriage, so the two halves of the chapter speak the same language.
        """
        y = GROUND - 96
        for off in (0, 4):
            col = dim(F_FEMALE, 0.9 if off == 0 else 0.55)
            wdt = 1.6 if off == 0 else 1.0
            pts = [(x0 + 26, y + off), (x1 - 26, y + off)]
            if trace:
                c.traced(pts, col, wdt, dur=f"{dur * 0.6:.2f}s")
            else:
                c.polyline(pts, col, wdt)

    MANGER_S = 1.06                 # `manger()` is already at true size
                                    # against a man; this is a nudge, not a
                                    # scale — at 1.55 the trough came to
                                    # their chests and hid both their legs
    MOUTH_UP = 54 * 0.62            # local rim height, in shared units

    def _manger(self, c, x, dur):
        """The child, drawn as the manger and what comes out of it.

        A stylised toddler standing between his parents was the first cut and
        it was wrong twice: `child()` is a child of seven, and a newborn who
        can stand is not a newborn. The manger solves the figure problem and
        is the better picture besides — every other light in this chapter
        falls ON somebody from above, and this one is the only thing on the
        stage that gives light instead of taking it.

        Order matters: the bloom and the rays go down BEFORE the trough, so
        the wood is lit from in front of the glow rather than floating on
        top of a bright disc.
        """
        s = SCALE * self.MANGER_S
        my = GROUND - self.MOUTH_UP * s              # the mouth, in the scene

        # The bloom is a radial gradient, not a stack of discs: nested
        # ellipses at stepped alpha showed their own edges and read as
        # concentric rings — a target, not a glow.
        c._emit(
            f'<defs><radialGradient id="mangerglow">'
            f'<stop offset="0%" stop-color="{_rgb(GOLD)}" '
            f'stop-opacity="0.30"/>'
            f'<stop offset="38%" stop-color="{_rgb(GOLD)}" '
            f'stop-opacity="0.12"/>'
            f'<stop offset="100%" stop-color="{_rgb(GOLD)}" '
            f'stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="{x:.1f}" cy="{my:.1f}" rx="290" ry="180" '
            f'fill="url(#mangerglow)" opacity="0">'
            f'<animate attributeName="opacity" values="0;1" '
            f'dur="{dur * 0.7:.2f}s" begin="{dur * 0.12:.2f}s" '
            f'fill="freeze"/></ellipse>')

        # And the rays. Twelve, unequal — an even fan of equal spokes reads
        # as a wheel — drawn outward from the mouth as the verse is read.
        for k in range(12):
            th = math.pi * (0.15 + 0.70 * k / 11)     # the upper half only,
            r0, r1 = 44, 92 + 52 * ((k * 7) % 5) / 4  # and kept off the two
                                                      # of them: the flatter
                                                      # rays lay across their
                                                      # robes like scratches
            c.traced([(x - r0 * math.cos(th), my - r0 * math.sin(th) * 0.8),
                      (x - r1 * math.cos(th), my - r1 * math.sin(th) * 0.8)],
                     dim(GOLD, 0.42), 1.5,
                     dur=f"{dur * 0.55:.2f}s")

        F.draw(c, F.manger(), x, GROUND, s, HL, BG)

    def _plate(self, c, x, y, text, dur, size=17, bold=False, delay=0.5):
        fnt = font(size, bold=bold)
        tw = fnt.getlength(text)
        pad = 13
        sub = SvgCanvas(W, H)
        sub.rect(x - tw / 2 - pad, y - size, tw + 2 * pad, size * 2,
                 fill=BG + (232,), stroke=dim(SAND_DIM, 0.9), width=1.1,
                 rx=9)
        sub.text((x, y), text, size, HL if bold else TEXT, anchor="mm",
                 bold=bold)
        c._emit(f'<g opacity="0">{"".join(sub._els)}'
                f'<animate attributeName="opacity" values="0;1" '
                f'dur="{dur * 0.4:.2f}s" begin="{dur * delay:.2f}s" '
                f'fill="freeze"/></g>')

    # -- one verse ---------------------------------------------------------

    def render(self, v):
        beat = BEATS[v]
        dur = _dur(self.narr.get(v))
        jx, mx = _places(beat)
        c = SvgCanvas(W, H, bg=BG)
        self._ground(c)

        if beat.get("light") == "mary":
            self._beam(c, mx, dur, grow=_appeared(v, "light"))

        bond, fresh = beat.get("bond"), _changed(v, "bond")
        if bond == "severed":
            self._severed(c, jx, mx, dur, trace=fresh)
        elif bond == "betrothed":
            self._betrothed(c, jx, mx, dur, trace=fresh)
        elif bond == "married":
            self._joined(c, jx, mx, dur, trace=fresh)

        # Joseph. "away" turns him around; "asleep" sits him down, which is
        # as much as this figure set will say about a dream — and enough,
        # with an angel standing over him.
        if beat["joseph"] == "asleep":
            self._figure(c, F.man(pose="sit"), jx, dim(TEXT, 0.75), dur)
            for k in range(3):                       # the sleep
                r = 3.0 + k * 1.6
                c.circle(jx + 46 + k * 20, GROUND - 128 - k * 20, r,
                         fill=None, stroke=dim(SAND_DIM, 0.6 - k * 0.14),
                         width=1.2)
        elif beat["joseph"] == "away":
            self._figure(c, F.man(pose="walk"), jx, dim(TEXT, 0.7), dur,
                         flip=-1)
        else:
            self._figure(c, F.man(), jx, TEXT, dur)

        # Mary.
        self._figure(c, F.woman(), mx,
                     HL if beat.get("light") == "mary" else TEXT, dur)

        if beat.get("angel"):
            # Over him, not beside him. Beside, an angel is a third person
            # in the room having a conversation; above a sleeping man it is
            # a dream, which is what the verse says it is — and it clears
            # the stage, which at this gap has no floor left to stand on.
            self._figure(c, F.angel(wings=beat["angel"],
                                    arms="down" if beat["angel"] == "raised"
                                    else "point_r"),
                         jx - 104, GOLD, dur, arrive=_appeared(v, "angel"),
                         gy=GROUND - 148, scale=SCALE * 0.74)

        if beat.get("prophet"):
            # Seven hundred years off to one side, and a line across the gap
            # — the prophet is not in the scene, he is quoted into it.
            px = 116
            fresh = _appeared(v, "prophet")
            self._figure(c, F.man(staff=True), px, dim(TEXT_DIM, 0.85), dur,
                         arrive=fresh)
            F.draw(c, F.scroll(), px + 6, GROUND - 246, SCALE * 0.62,
                   dim(SAND, 0.9), BG)
            # The quotation crossing the stage — seven hundred years of it,
            # arriving while the verse is read. It crosses ONCE, at verse 22;
            # verse 23 is the quotation itself and the line is already there.
            quote = [(px + 46, GROUND - 236), (mx - 54, GROUND - 236)]
            if fresh:
                c.traced(quote, dim(GOLD, 0.5), 1.4,
                         dur=f"{dur * 0.75:.2f}s")
            else:
                c.polyline(quote, dim(GOLD, 0.5), 1.4)
            c.text((px, LABEL_Y), "the prophet", 15, dim(TEXT_DIM, 0.9),
                   anchor="mm", italic=True)

        if beat.get("manger"):
            self._manger(c, (jx + mx) / 2, dur)

        if beat.get("immanuel"):
            self._plate(c, W / 2 + 90, GROUND - 300,
                        "IMMANUEL · God with us",
                        dur, size=20, bold=True)
        elif beat.get("name"):
            self._plate(c, (jx + mx) / 2, GROUND - 250, beat["name"], dur,
                        size=26, bold=True)

        # The thread out of the genealogy comes down onto Joseph, and it is
        # verse 20 — "Joseph, son of David" — that it belongs to. Drawn
        # last: on verse 20 the angel hangs in the air right where it falls,
        # and underneath it the one bright mark on the stage was invisible.
        self._descent(c, jx, dur, bright=bool(beat.get("sonof")))

        # Names under the feet.
        c.text((jx, LABEL_Y), "Joseph", 17, TEXT_DIM, anchor="mm")
        c.text((mx, LABEL_Y), "Mary", 17, TEXT_DIM, anchor="mm")
        self._hud(c, v)
        return c

    def _hud(self, c, v):
        hud = SvgLayer()
        hud.rectangle([0, 0, W, HUD_H], fill=BG + (236,))
        hud.text((28, 20), "The birth of Jesus Christ — Matthew 1",
                 font=F_TITLE, fill=TEXT)
        c.raw(hud.elements())
        c.line((0, HUD_H), (W, HUD_H), dim(SAND_DIM, 0.6), 1.0)
