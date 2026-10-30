"""The Tent of Meeting at Shiloh (Joshua 18:1-11 and 19:51) as a scene card
the camera dives into.

A side view from the east. The court's east face is its linen hangings on
eleven pillars, with the gate's screen in its four colours, and the door of
the tent rises behind it. All of it comes from sanctuary.py through the
svg_figures pieces. The camp's tents and the hills are behind. The
congregation stands before the gate in twelve companies, each under its
standard (Num 2:2). The five tribes that have their lot carry its colour
from the map (generate_joshua1319_svg.LOT_COL), and the seven that have not
carry an empty pennant. Joshua (a man with a staff) and Eleazar the priest
stand in the gateway with the jar of lots between them.
generate_joshua1319_svg.py flies the camera; svg_scene_card.py draws the card.

The story is acted, not captioned:
- 18:1 the congregation is there as the camera comes down, and the tent, the
  pillars, the hangings and the gate's screen go up at "set up the Tent of
  Meeting";
- 18:2 the seven empty pennants glow once;
- 18:3 Joshua speaks, and points out past the people to the land;
- 18:4 three men step out of each of the seven companies and stand before
  him;
- 18:8 they turn and go, out past the camp both ways;
- 18:9 (the camera is over the land) they come back, the first of them with
  the book;
- 18:10 Joshua's free hand goes over the jar and comes up with a lot;
- 18:11 he lays it before the jar, and Benjamin's pennant takes Benjamin's
  colour. The six lots after it do the same, off the card, at 19:1-19:40;
- 19:51 Eleazar is named, the head of each company steps forward, the seven
  lots in their row glow once at "by lot", and the camera goes to the door
  of the tent before it rises to the whole land.
The jar and its pebbles, the standards and the camp's tents are not in
Joshua's text, and none of them is named.

Card px: 5600 x 2400, the ground at y 1400, the court's middle at x 0. A man
is 110 px tall, so the court's face (50 cubits) is about 1550 px across.
"""

import sanctuary as SN
import svg_figures as F
from svg_map_camera import rgb
from svg_scene_card import Actor, Card, figure_svg, MAN_H, person, static
from svg_surface import _fmt
from generate_tabernacle import (GATE_COLORS, GOLD, SAND, SAND_DIM, TEXT,
                                 TEXT_DIM, WHITE_LINEN)

GROUND = 1400
MAN = 110.0                     # a man, card px
PXU = MAN / MAN_H               # card px a figure unit: true size against him
CU = F.CUBIT * PXU              # card px a cubit
SKY = (22, 24, 34)              # the Acts cards' sky, earth and hills
EARTH = (34, 35, 29)
HILL = (28, 30, 25)
FAR_HILL = (25, 27, 30)         # the farther ridge, halfway to the sky
S_CARD = 200                    # camera scale at the card's zoom 1, as in Acts
ANCHOR = (0, 1330)              # the card point hung on Shiloh's dot
SIZE = (5600, 2400)
ORIGIN = (-2800, 0)
EV = SN.Elevation(0, GROUND, CU)

# The twelve companies, from the gate outward: south and east on the left,
# west and north on the right, as one sees them from the east. Their lot's
# colour key (LOT_COL), or None for the seven still to come.
LEFT = ["Judah", "Issachar", "Zebulun", "Reuben", "Simeon", "Gad"]
RIGHT = ["Ephraim", "Manasseh", "Benjamin", "Dan", "Asher", "Naphtali"]
HAS_LOT = {"Judah": "JUDAH", "Reuben": "REUBEN", "Gad": "GAD",
           "Ephraim": "EPHRAIM", "Manasseh": "MANASSEH_W"}
# the seven lots in the order they come up (18:11-19:48), and the verse that
# says each
LOTS = [("Benjamin", (18, 11)), ("Simeon", (19, 1)), ("Zebulun", (19, 10)),
        ("Issachar", (19, 17)), ("Asher", (19, 24)), ("Naphtali", (19, 32)),
        ("Dan", (19, 40))]
PITCH, NEAR = 155, 345          # the companies' spacing, and the nearest's x
FOLK = 5                        # people in a company
ROW_Y = GROUND + 40             # where the companies stand
LINE_Y = GROUND + 150           # where the 21 stand before Joshua
JOSHUA = (-80, ROW_Y)
ELEAZAR = (70, ROW_Y)
PEOPLE = (0.45, 0.52)           # the zooms Joshua's and Eleazar's names show from
# the jar at Joshua's left, the hand his staff leaves free; the lots drawn
# from it are laid in a row before it
JAR = (-126, ROW_Y + 6)
LOT_ROW = (JAR[0], ROW_Y + 40, 15)      # the row's middle, and its spacing
# the ridge behind the camp, and the farther one: (x, y) along their tops
RIDGE = [(-2800, 1150), (-2300, 1090), (-1800, 1140), (-1300, 1060),
         (-800, 1120), (-300, 1080), (200, 1110), (700, 1050), (1200, 1120),
         (1700, 1070), (2200, 1130), (2800, 1080)]
FAR = [(-2800, 1020), (-2000, 980), (-1100, 1030), (-200, 990), (600, 1010),
       (1500, 960), (2300, 1010), (2800, 990)]


def company_x(tribe):
    if tribe in LEFT:
        return -(NEAR + PITCH * LEFT.index(tribe))
    return NEAR + PITCH * RIGHT.index(tribe)


def blank_tribes():
    return [t for t in LEFT + RIGHT if t not in HAS_LOT]


def figure_svg_at(parts, x, y, ink, flip=1):
    """Scenery at true size, feet at (x, y)."""
    return (f'<g transform="translate({_fmt(x)} {_fmt(y)})">'
            + figure_svg(parts, MAN, ink, EARTH, flip) + "</g>")


def standard_make(blank=False):
    return F.standard(blank=blank)


def ridge_y(x, ridge=RIDGE):
    for (x0, y0), (x1, y1) in zip(ridge, ridge[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return ridge[-1][1]


def hills():
    """The hill country behind the camp: a farther ridge, and the near one
    terraced, with trees along its top away from the court."""
    X0, X1 = ORIGIN[0], ORIGIN[0] + SIZE[0]
    out = []
    for ridge, fill in ((FAR, FAR_HILL), (RIDGE, HILL)):
        pts = ridge + [(X1, GROUND), (X0, GROUND)]
        out.append('<polygon points="' + " ".join(f"{x},{y}" for x, y in pts)
                   + f'" fill="{rgb(fill)}" stroke="{rgb(SAND_DIM)}" '
                   f'stroke-width="2"/>')
    for k in range(1, 6):                   # the terraces, following the ridge
        pts = [(x, round(y + 34 * k + (x % 7) * 1.5)) for x, y in RIDGE]
        out.append('<polyline points="' + " ".join(f"{x},{y}" for x, y in pts)
                   + f'" fill="none" stroke="{rgb(SAND_DIM)}" stroke-width="2" '
                   f'stroke-dasharray="26 14" opacity="0.6"/>')
    out.append('<defs><g id="shi_tree">'
               + figure_svg(F.tree(fruit=0), MAN * 0.25, SAND_DIM, HILL)
               + "</g></defs>")                     # drawn once, used often
    for k, x in enumerate(range(-2700, 2701, 230)):
        if abs(x) < 860:
            continue
        y = ridge_y(x) + 8 + (k % 3) * 22
        flip = " scale(-1 1)" if k % 2 else ""
        out.append(f'<use href="#shi_tree" transform="translate({x} {_fmt(y)}){flip}"/>')
    return out


def build(town_xy, lot_col, say=None):
    """The Shiloh card hung at the town's world point. `lot_col` maps a lot's
    colour key to its colour on the map; `say(ref, word)` is when the
    narration says a word (seconds, or None), which times the beats."""
    c = Card("shi", town_xy, ANCHOR, SIZE, S_CARD, page=EARTH, sky=SKY,
             ground_y=GROUND, origin=ORIGIN)
    # Shiloh's name stands in the sky, clear of the crowd, so it may show on
    # the wider shots; Joshua's and Eleazar's wait for closer ones (PEOPLE),
    # or they'd touch. A name a verse's rest leaves cut by the frame goes as
    # it leaves, not at once.
    c.names_at = (0.30, 0.38)
    c.cut_late = True
    X0, X1 = ORIGIN[0], ORIGIN[0] + SIZE[0]

    # -- scenery: the hills, the ground, the camp's tents -----------------
    c.scenery += hills()
    c.scenery.append(f'<rect x="{X0}" y="{GROUND}" width="{SIZE[0]}" '
                     f'height="{SIZE[1] - GROUND}" fill="{rgb(EARTH)}"/>')
    c.scenery.append(f'<line x1="{X0}" y1="{GROUND}" x2="{X1}" y2="{GROUND}" '
                     f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    # the camp's tents, behind the companies beyond the court's ends
    for k, x in enumerate((-2500, -2050, -1600, -1150, 1150, 1600, 2050,
                           2500)):
        c.scenery.append(figure_svg_at(F.tent(), x, GROUND - 30, SAND_DIM,
                                       flip=-1 if k % 2 else 1))

    # -- the Tabernacle, raised at 18:1: the tent behind, then the court --
    def piece(key, make, x, ink, flip=1):
        return c.add(Actor(key, make, x, GROUND, h=MAN, unit_h=MAN_H,
                           ink=ink, flip=flip))
    piece("tent", static(F.tent_east), EV.x(25), SAND_DIM)
    door_w = (SN.TENT[3] - SN.TENT[1]) / len(GATE_COLORS)
    for k, col in enumerate(GATE_COLORS):
        y = SN.TENT[3] - k * door_w                 # from the south (left)
        piece(f"door{k}", static(F.hanging, door_w, F.tent_screen_height()),
              EV.x(y), col)
    piece("door_pillars", static(F.door_pillars), EV.x(25), GOLD)
    spans = [(y, y + 5) for y in range(SN.COURT[1], SN.COURT[3], 5)]
    flank = [s for s in spans if s[1] <= SN.GATE[0] or s[0] >= SN.GATE[1]]
    for ya, yb in flank:
        # each width of linen swings out from the post nearer the gate
        if yb <= SN.GATE[0]:
            piece(f"hang{ya}", static(F.hanging, 5), EV.x(yb), WHITE_LINEN)
        else:
            piece(f"hang{ya}", static(F.hanging, 5), EV.x(ya), WHITE_LINEN,
                  flip=-1)
    gate_w = (SN.GATE[1] - SN.GATE[0]) / len(GATE_COLORS)
    for k, col in enumerate(GATE_COLORS):
        piece(f"gate{k}", static(F.hanging, gate_w),
              EV.x(SN.GATE[1] - k * gate_w), col)
    posts = sorted({y for _x, y in SN.PILLARS["east"]} | {SN.COURT[1]})
    for y in posts:
        piece(f"post{y}", static(F.court_post), EV.x(y), SAND)

    # -- the congregation ------------------------------------------------
    for tribe in LEFT + RIGHT:
        gx = company_x(tribe)
        key = HAS_LOT.get(tribe)
        c.add(Actor(f"std_{tribe}", standard_make, gx + 50, ROW_Y - 6,
                    h=MAN, unit_h=MAN_H,
                    ink=lot_col[key] if key else SAND,
                    pose={"blank": key is None}, shown=True))
        for j in range(FOLK):
            kind = "woman" if j == 3 else "man"
            c.add(Actor(f"{tribe}{j}", person(kind), gx - 44 + j * 22,
                        ROW_Y + (j % 2) * 12, ink=SAND, shown=True,
                        flip=1 if gx < 0 else -1))
    c.add(Actor("joshua", person("man", staff=True), *JOSHUA, ink=TEXT,
                shown=True, names_at=PEOPLE))
    c.add(Actor("eleazar", person("priest"), *ELEAZAR, ink=TEXT, shown=True,
                flip=-1, names_at=PEOPLE))
    c.add(Actor("jar", static(F.jar), *JAR, h=MAN, unit_h=MAN_H, ink=SAND,
                shown=True))
    mouth = (JAR[0], JAR[1] - F.bbox((F.jar(), 0))[3] * PXU)
    for k in range(len(LOTS)):
        c.add(Actor(f"lot{k}", static(F.lot), *mouth, h=MAN, unit_h=MAN_H,
                    ink=TEXT))
    # names with no figure: the place, and the heads of 19:51
    c.add(Actor("shiloh", static(list), 560, 950, shown=True,
                label_y=0, label_fill=TEXT_DIM, label_italic=True))

    c.refs = refs()
    events(c, lot_col, say)
    return c


def refs():
    """Every verse from 18:1 to 19:51 in order: the card's state carries
    through the verses it isn't drawn in (19:1's lot, say)."""
    from passages import verse_numbers
    return [(ch, v) for ch in (18, 19) for v in verse_numbers("Joshua", ch)]


def surveyors():
    """The 21 (18:4): three from each company without a lot, and where each
    stands in the line before Joshua, the left companies' left of him."""
    out = []
    left = [t for t in blank_tribes() if t in LEFT]
    right = [t for t in blank_tribes() if t in RIGHT]
    for side, tribes in ((-1, left), (1, right)):
        men = [(t, j) for t in tribes for j in range(3)]
        for i, (t, j) in enumerate(men):
            out.append((t, j, side * (232 + i * 62)))
    return out


def cue(say, ref, word, default, lead=0.1):
    """When a beat answering `word` starts: just before it's said, or
    `default` (today's MP3) when there's no clock."""
    t = say(ref, word) if say else None
    return default if t is None else round(max(0.0, t - lead), 2)


def events(c, lot_col, say=None):
    on = c.on
    # 18:1 set up the Tent of Meeting: the tent, then the posts from the
    # gate outward, the linen swinging out from them, and the gate's screen
    t1 = cue(say, (18, 1), "set", 5.05)
    tent = ["tent", "door_pillars"] + [f"door{k}" for k in range(4)]
    for key in tent:
        on((18, 1), ("show", key, t1, 0.2, None), ("grow", key, t1, 1.0, None))
    mid = (SN.COURT[1] + SN.COURT[3]) / 2
    keys = [k for k in c.actors if k.startswith("post")]
    for key in sorted(keys, key=lambda k: abs(int(k[4:]) - mid)):
        rank = abs(int(key[4:]) - mid) / 5
        t = round(t1 + 0.6 + 0.05 * rank, 2)
        on((18, 1), ("show", key, t, 0.2, None), ("grow", key, t, 0.5, None))
    for key in [k for k in c.actors if k.startswith("hang")]:
        ya = int(key[4:])
        rank = min(abs(ya - SN.GATE[0]), abs(ya + 5 - SN.GATE[1])) / 5
        t = round(t1 + 1.1 + 0.12 * rank, 2)
        on((18, 1), ("show", key, t, 0.15, None), ("grow_x", key, t, 0.6, None))
    for k in range(4):
        t = round(t1 + 1.8 + 0.08 * k, 2)
        on((18, 1), ("show", f"gate{k}", t, 0.15, None),
           ("grow", f"gate{k}", t, 0.5, None))
    on((18, 1), ("label", "shiloh", cue(say, (18, 1), "Shiloh", 4.18), 0,
                 "Shiloh"))

    # 18:2 seven tribes had not yet divided their inheritance
    t = cue(say, (18, 2), "Seven", 0.25, lead=-0.1)
    for tribe in blank_tribes():
        on((18, 2), ("pulse", f"std_{tribe}", t, 1.0, None))

    # 18:3 Joshua said ... how long will you neglect to go in
    on((18, 3),
       ("label", "joshua", cue(say, (18, 3), "Joshua", 0.3, lead=-0.15), 0,
        "Joshua"),
       ("pose", "joshua", cue(say, (18, 3), "said", 0.45), 0.3,
        {"arms": "open"}),
       ("pose", "joshua", cue(say, (18, 3), "neglect", 3.52), 0.3,
        {"arms": "point_l"}))

    # 18:4 appoint three men from each tribe: they step out and line up
    # before him; "I will send them"
    order = blank_tribes()
    t3 = cue(say, (18, 4), "three", 1.48, lead=-0.05)
    for tribe, j, lx in surveyors():
        a = c.actors[f"{tribe}{j}"].start
        t0 = round(t3 + 0.22 * order.index(tribe) + 0.08 * j, 2)
        face = 1 if lx > a["x"] else -1
        on((18, 4), ("pose", f"{tribe}{j}", t0, 0.15, {"pose": "walk"}),
           ("flip", f"{tribe}{j}", t0, 0.15, face),
           ("move", f"{tribe}{j}", t0, 1.0, (lx - a["x"], LINE_Y - a["y"])),
           ("pose", f"{tribe}{j}", t0 + 1.0, 0.2, {"pose": "stand"}),
           ("flip", f"{tribe}{j}", t0 + 1.0, 0.2, -1 if lx > 0 else 1))
    on((18, 4), ("pose", "joshua", cue(say, (18, 4), "send", 3.3, lead=0.2),
                 0.3, {"arms": "open"}))

    # 18:8 the men arose and went: they turn as the camera lands and walk
    # out past the camp; Joshua points them on with his free hand
    for tribe, j, lx in surveyors():
        key = f"{tribe}{j}"
        side = 1 if lx > 0 else -1
        t0 = round(2.1 + 0.05 * abs(lx) / 62, 2)
        on((18, 8), ("flip", key, 1.9, 0.2, side),
           ("pose", key, t0, 0.15, {"pose": "walk"}),
           ("move", key, t0, 2.8, (side * 1500, 0)),
           ("hide", key, t0 + 2.4, 0.4, None))
    on((18, 8), ("pose", "joshua", 2.1, 0.3, {"arms": "point_l"}))

    # 18:9 they came to Joshua (the camera is over the land): back in line,
    # the first of them with the book
    for tribe, j, lx in surveyors():
        key = f"{tribe}{j}"
        side = 1 if lx > 0 else -1
        on((18, 9), ("show", key, 4.0, 0.3, None),
           ("move", key, 4.0, 2.0, (-side * 1500, 0)),
           ("pose", key, 6.0, 0.2, {"pose": "stand"}),
           ("flip", key, 6.0, 0.2, -side))
    first = surveyors()[0]
    book = figure_svg_at(F.scroll(), 26, -64 * PXU, TEXT)
    on((18, 9), ("mark", f"{first[0]}{first[1]}", 6.0, 0.3, book),
       ("pose", "joshua", 4.0, 0.3, {"arms": "down"}))

    # 18:10 Joshua cast lots: his free hand goes over the jar and comes up
    # with a lot in it as the camera lands, by "before Yahweh"
    hand = (JOSHUA[0] - 20.6 * PXU, JOSHUA[1] - 92 * PXU)
    lot0 = c.actors["lot0"].start
    on((18, 10), ("pose", "joshua", 1.3, 0.3, {"arms": "hold_l"}),
       ("move", "lot0", 1.6, 0.05, (hand[0] - lot0["x"], hand[1] - lot0["y"])),
       ("pose", "joshua", 1.9, 0.4, {"arms": "up"}),
       ("show", "lot0", 2.2, 0.3, None))

    # the lots come up: each is laid in the row before the jar, and its
    # company's pennant takes its colour (18:11 on the card, glowing once so
    # the eye finds it; the six after it in the card's state only)
    for k, (tribe, ref) in enumerate(LOTS):
        spot = (LOT_ROW[0] + (k - 3) * LOT_ROW[2], LOT_ROW[1])
        col = lot_col[tribe.upper()]
        if k == 0:
            t = cue(say, ref, tribe, 1.87)
            on(ref, ("move", "lot0", 0.3, 0.7,
                     (spot[0] - hand[0], spot[1] - hand[1])),
               ("pose", "joshua", 0.3, 0.4, {"arms": "down"}),
               ("pose", f"std_{tribe}", t, 0.6, {"blank": False}),
               ("ink", f"std_{tribe}", t, 0.6, col),
               ("pulse", f"std_{tribe}", round(t + 0.5, 2), 1.0, None))
        else:
            key = f"lot{k}"
            st = c.actors[key].start
            on(ref, ("move", key, 0.5, 0.1, (spot[0] - st["x"], spot[1] - st["y"])),
               ("show", key, 0.6, 0.4, None),
               ("pose", f"std_{tribe}", 1.0, 0.6, {"blank": False}),
               ("ink", f"std_{tribe}", 1.0, 0.6, col))
    # off the card after 18:11: the 21 go back to their companies
    for tribe, j, lx in surveyors():
        a = c.actors[f"{tribe}{j}"].start
        on((18, 12), ("move", f"{tribe}{j}", 1.0, 1.0, (a["x"] - lx, a["y"] - LINE_Y)),
           ("flip", f"{tribe}{j}", 2.0, 0.1, a["flip"]))

    # 19:51 Eleazar the priest, Joshua, and the heads of the fathers'
    # houses distributed by lot at the door of the Tent of Meeting: the head
    # of each company steps out before it
    on((19, 51), ("label", "eleazar",
                  cue(say, (19, 51), "Eleazar", 2.4, lead=-0.15), 0, "Eleazar"))
    t = cue(say, (19, 51), "heads", 5.8)
    for tribe in LEFT + RIGHT:
        on((19, 51), ("pose", f"{tribe}2", t, 0.15, {"pose": "walk"}),
           ("move", f"{tribe}2", t, 0.8, (0, 90)),
           ("pose", f"{tribe}2", round(t + 0.8, 2), 0.2, {"pose": "stand"}))
    t = cue(say, (19, 51), "lot", 11.32)
    for k in range(len(LOTS)):
        on((19, 51), ("pulse", f"lot{k}", t, 1.0, None))


# Camera shots inside the card, (x, y, zoom), and each verse's legs. A leg's
# target is a shot here, "map" (the verse's own camera on the map, which the
# tour works out as for any verse), or a map shot the tour names ("survey").
SHOTS = {
    "gate": (0, 1330, 0.62), "camp": (35, 1250, 0.4),
    "left7": (-900, 1360, 0.62), "right7": (950, 1360, 0.62),
    "joshua": (-50, 1390, 0.95), "hills": (-500, 1200, 0.55),
    "line": (0, 1440, 0.62), "line_l": (-420, 1460, 0.78),
    "line_r": (520, 1460, 0.78), "wide": (35, 1250, 0.4),
    "hills_up": (0, 1100, 0.55), "jar": (-90, 1385, 1.2),
    "twelve": (35, 1320, 0.4), "door": (0, 1200, 0.85),
    "benjamin": (520, 1330, 0.66), "lots": (-60, 1400, 1.1),
}
LEGS = {
    (18, 1): [("hold", None, 1.0), ("to", "gate", 3.3), ("hold", None, 3.0),
              ("to", "camp", 1.4)],
    (18, 2): [("hold", None, 0.8), ("to", "left7", 1.8),
              ("to", "right7", 2.6)],
    (18, 3): [("to", "joshua", 2.0), ("hold", None, 2.6),
              ("to", "hills", 3.8)],
    (18, 4): [("to", "line", 1.4), ("hold", None, 2.8), ("to", "line_l", 1.4),
              ("to", "line_r", 3.0)],
    (18, 5): [("to", "map", 2.6)],
    (18, 8): [("to", "line", 2.0), ("hold", None, 0.8), ("to", "wide", 2.0),
              ("hold", None, 1.0), ("to", "hills_up", 2.4),
              ("hold", None, 1.4), ("to", "jar", 2.2)],
    (18, 9): [("to", "survey", 2.6), ("hold", None, 3.0), ("to", "map", 1.8)],
    (18, 10): [("to", "jar", 1.8), ("hold", None, 1.8), ("to", "twelve", 3.0)],
    (18, 11): [("to", "benjamin", 1.6), ("hold", None, 1.1), ("to", "map", 2.8)],
    (19, 51): [("to", "gate", 2.6), ("hold", None, 1.4), ("to", "twelve", 1.4),
               ("hold", None, 3.6), ("to", "lots", 1.8), ("hold", None, 1.2),
               ("to", "door", 1.6), ("hold", None, 0.6), ("to", "map", 2.7)],
}
