"""Lystra (Acts 14:8-20) as a scene card the camera dives into.

A side view of the town: houses round a plaza, the wall and its gate, the
altar before the gate, the temple of Jupiter on a rise outside the city, the
road east past the fields, and hills under the sky. The camera comes down
into it out of Lystra's dot at 14:8 and surfaces at 14:20 for the road to
Derbe (generate_acts1314_svg.py flies it; svg_scene_card.py draws it).

The story is acted, not captioned: the lame man sits, is looked at, leaps up
and walks; the crowd comes in and lifts its arms; plinths rise under
Barnabas and Paul and the names Jupiter and Mercury appear on them; the
priest leads garlanded oxen down from the temple; the two tear their
clothes, jump down and run in among the people, and the names are struck
("We also are men"); the sun, birds, sheep, paths, rain and harvest come in
without words for the speech of 14:15-17; Paul is stoned in the gateway,
dragged out past the temple, and rises with the disciples round him.

Card px: 3200 x 1900, the ground at y 1400. A man is 110 px tall, so at the
card's zoom 1 he is 110 px on screen.
"""

import svg_figures as F
from svg_scene_card import Actor, Card, figure_svg, MAN_H
from svg_map_camera import fade, rgb, traced_el
from svg_surface import _fmt
from generate_tabernacle import BG, SAND, SAND_DIM, TEXT, TEXT_DIM, HL

GROUND = 1400
MAN = 110.0                     # a man, card px
SKY = (22, 24, 34)
EARTH = (34, 35, 29)
PAVE = (40, 40, 33)
HILL = (28, 30, 25)
S_CARD = 200                    # camera scale at the card's zoom 1
ANCHOR = (450, 1260)            # the card point hung on Lystra's dot
SIZE = (4200, 2200)              # x from -1000 (ORIGIN) to 3200
ORIGIN = (-1000, 0)


def shifted(parts, dx, dy):
    """A figure's parts moved by (dx, dy) units: to hang a garland on a
    head or a neck."""
    out = []
    for kind, data, mat in parts:
        if kind == "dot":
            out.append((kind, (data[0] + dx, data[1] + dy, data[2]), mat))
        else:
            out.append((kind, [(x + dx, y + dy) for x, y in data], mat))
    return out


def scaled_h(name):
    """A thing's drawn height in card px at true size against a man."""
    return MAN * F.UNIT[name]


_PERSONS = {}


def person(kind="man", **fixed):
    """One maker per kind of person, so every man in the crowd shares the
    same drawings (svg_scene_card draws each pose once per file)."""
    k = (kind, tuple(sorted(fixed.items())))
    if k not in _PERSONS:
        maker = {"man": F.man, "woman": F.woman, "child": F.child}[kind]

        def make(**pose):
            return maker(**dict(fixed, **pose))
        _PERSONS[k] = make
    return _PERSONS[k]


def priest_make(**pose):
    return F.man(**pose) + shifted(F.garland(), 0, 86)


def ox_make(**_pose):
    return F.ox() + shifted(F.garland(swag=True), 47, 47)


def static(fn, *a, **kw):
    def make(**_pose):
        return fn(*a, **kw)
    return make


def build(town_xy):
    """The Lystra card hung at the town's world point."""
    c = Card("lys", town_xy, ANCHOR, SIZE, S_CARD, page=EARTH, sky=SKY,
             ground_y=GROUND, origin=ORIGIN)
    X0 = ORIGIN[0]
    W_, H_ = 3200, SIZE[1]

    # -- scenery: far hills, ground, plaza, road, fields, houses, wall ---
    hills = [(X0, 1200), (-700, 1260), (-400, 1170), (0, 1250),
             (300, 1180), (620, 1230), (900, 1150),
             (1250, 1220), (1600, 1130), (1950, 1170), (2300, 1080),
             (2650, 1150), (2950, 1090), (3200, 1140), (3200, GROUND),
             (X0, GROUND)]
    c.scenery.append(f'<polygon points="'
                     + " ".join(f"{x},{y}" for x, y in hills)
                     + f'" fill="{rgb(HILL)}" stroke="{rgb(SAND_DIM)}" '
                     f'stroke-width="2"/>')
    c.scenery.append(f'<rect x="{X0}" y="{GROUND}" width="{W_ - X0}" '
                     f'height="{H_ - GROUND}" fill="{rgb(EARTH)}"/>')
    c.scenery.append(f'<rect x="{X0}" y="{GROUND}" width="{1480 - X0}" '
                     f'height="40" fill="{rgb(PAVE)}"/>')
    c.scenery.append(f'<line x1="{X0}" y1="{GROUND}" x2="{W_}" '
                     f'y2="{GROUND}" stroke="{rgb(SAND_DIM)}" '
                     f'stroke-width="2"/>')
    # the road east from the gate, and the furrows of the fields
    c.scenery.append(f'<rect x="1640" y="{GROUND}" width="{W_ - 1640}" '
                     f'height="22" fill="{rgb(PAVE)}"/>')
    for k in range(9):
        y = GROUND + 40 + k * 26
        c.scenery.append(f'<line x1="2420" y1="{y}" x2="{3150 - k * 12}" '
                         f'y2="{y}" stroke="{rgb(SAND_DIM)}" '
                         f'stroke-width="2" stroke-dasharray="18 10"/>')
    hp = F.palette(SAND_DIM, EARTH)
    # houses set apart round the plaza, so they read as houses and not
    # as a second wall
    for k, x in enumerate((-880, -480, -90, 300, 690, 1060, 1380)):
        f = 0.78 if k % 2 else 0.9
        c.scenery.append(figure_svg_at(F.house(), x, GROUND,
                                       scaled_h("house") * f, SAND_DIM,
                                       unit_h=MAN_H * F.UNIT["house"]))
    # the town wall either side of its gate
    for x0, x1 in ((1480, 1530), (1650, 1700)):
        c.scenery.append(f'<rect x="{x0}" y="{GROUND - 270}" '
                         f'width="{x1 - x0}" height="270" '
                         f'fill="{rgb((40, 40, 33))}" '
                         f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    c.scenery.append(figure_svg_at(F.gate(), 1590, GROUND, scaled_h("gate"),
                                   SAND_DIM, unit_h=MAN_H * F.UNIT["gate"]))
    # the rise the temple stands on
    c.scenery.append(f'<path d="M1820 {GROUND} C1900 {GROUND - 70} '
                     f'2200 {GROUND - 70} 2300 {GROUND}Z" '
                     f'fill="{rgb(HILL)}" stroke="{rgb(SAND_DIM)}" '
                     f'stroke-width="2"/>')

    # -- the cast, drawn in this order -----------------------------------
    sun = c.add(Actor("sun", static(F.sun), 2700, 1210, h=90,
                      unit_h=MAN_H * F.UNIT["sun"], ink=HL))
    c.add(Actor("hills_near", static(near_hills), 0, 0, h=1, unit_h=1,
                ink=SAND_DIM, shown=True))
    for k, (x, y) in enumerate(((2050, 860), (2350, 820), (2600, 900))):
        c.add(Actor(f"cloud{k}", static(F.cloud), x + 420, y, h=150,
                    unit_h=41, ink=SAND))
    for k, x in enumerate((1900, 2050, 2200)):
        c.add(Actor(f"bird{k}", static(F.bird, pose="glide"), x - 500,
                    760 + k * 40, h=36, unit_h=MAN_H * F.UNIT["bird"],
                    ink=SAND))
    temple = c.add(Actor("temple", static(F.temple), 2060, GROUND - 52,
                         h=scaled_h("temple") * 0.86,
                         unit_h=MAN_H * F.UNIT["temple"], ink=SAND,
                         shown=True))
    t_scale = temple.h / temple.unit_h          # card px per unit
    c.add(Actor("idol", static(F.idol, "seated"), 2060,
                GROUND - 52 - F.TEMPLE_FLOOR * t_scale,
                h=scaled_h("idol") * 0.86, unit_h=MAN_H * F.UNIT["idol"],
                ink=SAND, shown=True))
    c.add(Actor("altar", static(F.altar, "stone"), 1740, GROUND,
                h=scaled_h("altar_stone") * 0.8,
                unit_h=MAN_H * F.UNIT["altar_stone"], ink=SAND, shown=True))
    for k, x in enumerate((2480, 2600, 2760, 2900)):
        c.add(Actor(f"sheep{k}", static(F.sheep), x, GROUND + 60 + k % 2 * 50,
                    h=scaled_h("sheep") * 0.8,
                    unit_h=MAN_H * F.UNIT["sheep"], ink=SAND,
                    flip=-1 if k % 2 else 1))
    # the harvest of 14:17
    for k, (name, x, fn, kw) in enumerate((
            ("grass0", 2460, F.grass, {}), ("grass1", 2560, F.grass, {}),
            ("herb0", 2640, F.herb, {}), ("vine0", 2740, F.vine,
                                          {"fruit": 2}),
            ("vine1", 2840, F.vine, {"fruit": 2}),
            ("tree0", 3010, F.tree, {"fruit": 3}),
            ("grass2", 2940, F.grass, {}))):
        unit = name.rstrip("0123456789")
        c.add(Actor(name, static(fn, **kw), x, GROUND + 30,
                    h=scaled_h(unit), unit_h=MAN_H * F.UNIT[unit], ink=SAND))
    c.add(Actor("basket", static(F.basket), 2380, GROUND + 26,
                h=scaled_h("basket"), unit_h=MAN_H * F.UNIT["basket"],
                ink=SAND))
    c.add(Actor("bread", static(F.bread), 2412, GROUND + 26,
                h=scaled_h("bread") * 0.7, unit_h=MAN_H * F.UNIT["bread"],
                ink=SAND))
    for key, x in (("plinth_m", 680), ("plinth_j", 820)):
        c.add(Actor(key, static(F.plinth), x, GROUND,
                    h=scaled_h("plinth"), unit_h=MAN_H * F.UNIT["plinth"],
                    ink=SAND, label_y=-_pl() * 0.45))
    c.add(Actor("lame", person("man"), 420, GROUND, ink=TEXT,
                pose={"pose": "sit"}, shown=True, flip=1))
    crowd = []
    spots = [1040 + k * 18 for k in range(24)]
    kinds = ["man", "woman", "man", "child", "woman", "man"]
    for k, x in enumerate(spots):
        kind = kinds[k % len(kinds)]
        crowd.append(c.add(Actor(f"crowd{k}", person(kind), x,
                                 GROUND + (k % 3) * 14, ink=SAND,
                                 flip=-1 if k % 4 else 1)))
    c.add(Actor("paul", person("man"), 680, GROUND, ink=TEXT,
                pose={"arms": "open"}, flip=-1))
    c.add(Actor("barnabas", person("man", staff=True), 820, GROUND,
                ink=TEXT, flip=-1, label_y=-(MAN + 46)))
    c.add(Actor("priest", priest_make, 2060, GROUND - 52, ink=SAND, flip=-1))
    for k in range(2):
        c.add(Actor(f"ox{k}", ox_make, 2130 + k * 120, GROUND - 52,
                    h=scaled_h("ox"), unit_h=MAN_H * F.UNIT["ox"], ink=SAND,
                    flip=-1))
    for k in range(4):
        c.add(Actor(f"newcomer{k}", person("man"), -60 - k * 40, GROUND,
                    ink=SAND, flip=1))
    for k, (kind, x) in enumerate((("man", 2300), ("man", 2336),
                                   ("man", 2460), ("woman", 2500))):
        c.add(Actor(f"disciple{k}", person(kind), x, GROUND + 6, ink=SAND,
                    flip=1 if x < 2400 else -1))
    for k in range(6):
        c.add(Actor(f"stone{k}", static(F.stone), 1560 + (k - 2.5) * 26,
                    GROUND + 8 + (k % 2) * 6, h=scaled_h("stone") * 0.4,
                    unit_h=MAN_H * F.UNIT["stone"], ink=SAND))

    c.refs = [(14, v) for v in range(8, 21)]
    lyst_events(c, crowd)
    return c


def figure_svg_at(parts, x, y, h, ink, unit_h=MAN_H, flip=1):
    return (f'<g transform="translate({_fmt(x)} {_fmt(y)})">'
            + figure_svg(parts, h, ink, EARTH, flip, unit_h=unit_h) + "</g>")


def near_hills():
    """The ridge in front of the sun, so it can rise from behind it."""
    pts = [(2450, 1210), (2600, 1160), (2760, 1190), (2900, 1150),
           (3050, 1200), (3200, 1170), (3200, 1260), (2450, 1260)]
    return [("fill", [(x, -y) for x, y in pts], "far")]


def lyst_events(c, crowd):
    on = c.on
    # 14:8 the man who never walked, sitting by a house
    on((14, 8), ("pulse", "lame", 3.8, 0.8, None))
    # 14:9 Paul and Barnabas, facing him; Paul looks at him
    on((14, 9),
       ("show", "paul", 1.0, 0.6, None), ("label", "paul", 1.6, 0, "Paul"),
       ("show", "barnabas", 1.2, 0.6, None),
       ("label", "barnabas", 1.8, 0, "Barnabas"),
       ("pulse", "lame", 4.1, 0.8, None))
    # 14:10 Stand upright on your feet! He leaped up and walked
    on((14, 10),
       ("pose", "paul", 1.0, 0.3, {"arms": "point_l"}),
       ("pose", "lame", 2.9, 0.3, {"pose": "stand", "arms": "up"}),
       ("hop", "lame", 2.9, 0.6, 40),
       ("pose", "lame", 3.5, 0.2, {"pose": "walk", "arms": "down"}),
       ("move", "lame", 3.5, 1.0, (90, 0)),
       ("pose", "lame", 4.5, 0.2, {"pose": "stand"}))
    # 14:11 the multitude comes, and lifts up its voice
    for k, a in enumerate(crowd):
        t = 1.6 + (k % 12) * 0.2
        on((14, 11), ("show", a.key, t, 0.4, None),
           ("move", a.key, t, 0.8, (-40 if k % 2 else -60, 0)))
        on((14, 11), ("pose", a.key, 5.0 + k * 0.04, 0.3, {"arms": "up"}))
    # 14:12 Jupiter and Mercury: plinths lift them
    on((14, 12),
       ("show", "plinth_j", 1.6, 0.5, None), ("show", "plinth_m", 1.8, 0.5,
                                               None),
       ("move", "barnabas", 1.6, 0.8, (0, -_pl())),
       ("move", "paul", 1.8, 0.8, (0, -_pl())),
       ("label", "plinth_j", 2.6, 0, "Jupiter"),
       ("label", "plinth_m", 3.2, 0, "Mercury"),
       ("pose", "paul", 4.0, 0.4, {"arms": "open"}))
    # 14:13 the priest brings oxen and garlands to the gates
    on((14, 13),
       ("pulse", "temple", 2.4, 0.8, None),
       ("show", "priest", 2.8, 0.4, None), ("show", "ox0", 3.0, 0.4, None),
       ("show", "ox1", 3.2, 0.4, None),
       ("move", "priest", 3.0, 3.0, (-260, 52)),
       ("move", "ox0", 3.2, 3.0, (-260, 52)),
       ("move", "ox1", 3.4, 3.0, (-260, 52)))
    for k in range(4):
        on((14, 13), ("move", crowd[20 + k].key, 6.4 + k * 0.2, 1.0,
                      (150 + k * 20, 0)))
    # 14:14 they tear their clothes, jump down and run in among them
    on((14, 14),
       ("move", "paul", 3.4, 0.4, (0, _pl())),
       ("move", "barnabas", 3.4, 0.4, (0, _pl())),
       ("pose", "paul", 3.8, 0.2, {"pose": "walk", "arms": "down"}),
       ("pose", "barnabas", 3.8, 0.2, {"pose": "walk"}),
       ("flip", "paul", 3.8, 0.2, 1), ("flip", "barnabas", 3.8, 0.2, 1),
       ("move", "paul", 3.8, 2.0, (420, 0)),
       ("move", "barnabas", 3.8, 2.0, (380, 0)),
       ("pose", "paul", 5.8, 0.2, {"pose": "stand", "arms": "up"}),
       ("pose", "barnabas", 5.8, 0.2, {"pose": "stand", "arms": "up"}))
    # 14:15 We also are men: the names struck, the idols dimmed, and the
    # sky, the earth and all that is in them
    on((14, 15),
       ("strike", "plinth_j", 2.4, 0.5, None),
       ("strike", "plinth_m", 2.6, 0.5, None),
       ("ink", "temple", 7.6, 0.8, SAND_DIM), ("ink", "idol", 7.6, 0.8,
                                               SAND_DIM),
       ("ink", "altar", 7.6, 0.8, SAND_DIM),
       ("ink", "plinth_j", 7.6, 0.8, SAND_DIM),
       ("ink", "plinth_m", 7.6, 0.8, SAND_DIM),
       ("show", "sun", 9.6, 0.4, None), ("move", "sun", 9.6, 1.4, (0, -120)),
       ("pose", "paul", 0.4, 0.4, {"arms": "open"}),
       ("pose", "barnabas", 0.4, 0.4, {"arms": "down"}))
    for k in range(3):
        on((14, 15), ("show", f"bird{k}", 10.6 + k * 0.3, 0.3, None),
           ("move", f"bird{k}", 10.6 + k * 0.3, 1.6, (500, -20)))
    for k in range(4):
        on((14, 15), ("show", f"sheep{k}", 11.4 + k * 0.25, 0.5, None))
    # 14:17 rains from the sky and fruitful seasons, food and gladness
    for k in range(3):
        on((14, 17), ("show", f"cloud{k}", 1.0 + k * 0.2, 0.4, None),
           ("move", f"cloud{k}", 1.0 + k * 0.2, 1.4, (-420, 0)))
    for k, name in enumerate(("grass0", "grass1", "herb0", "vine0", "vine1",
                              "grass2", "tree0")):
        on((14, 17), ("show", name, 4.8 + k * 0.45, 0.6, None),
           ("grow", name, 4.8 + k * 0.45, 0.8, None))
    on((14, 17), ("show", "basket", 8.6, 0.6, None),
       ("show", "bread", 8.8, 0.6, None))
    # 14:18 they hardly stopped the multitudes from sacrificing
    on((14, 18),
       ("pose", "paul", 0.6, 0.2, {"pose": "walk", "arms": "down"}),
       ("pose", "barnabas", 0.6, 0.2, {"pose": "walk", "arms": "down"}),
       ("move", "paul", 1.0, 1.4, (460, 0)),
       ("move", "barnabas", 1.0, 1.4, (300, 0)),
       ("pose", "paul", 2.4, 0.3, {"pose": "stand", "arms": "open"}),
       ("pose", "barnabas", 2.4, 0.3, {"pose": "stand", "arms": "open"}),
       ("flip", "paul", 2.4, 0.3, -1), ("flip", "barnabas", 2.4, 0.3, -1),
       ("pulse", "altar", 2.8, 0.8, None))
    for a in crowd[:12]:
        on((14, 18), ("move", a.key, 1.6, 1.0, (30, 0)))
    # 14:19 Jews from Antioch and Iconium; Paul stoned, dragged out
    for k in range(4):
        on((14, 19), ("show", f"newcomer{k}", 0.8 + k * 0.2, 0.4, None),
           ("move", f"newcomer{k}", 0.8 + k * 0.2, 2.4, (1120 + k * 30, 0)))
    for a in crowd[:12]:
        on((14, 19), ("pose", a.key, 3.6, 0.4, {"arms": "point_r"}))
    for k in range(6):
        on((14, 19), ("show", f"stone{k}", 5.0 + k * 0.1, 0.2, None))
    on((14, 19),
       ("rot", "paul", 5.4, 0.4, -90),
       ("ink", "paul", 5.4, 0.4, SAND_DIM),
       ("move", "paul", 6.4, 2.0, (820, 0)))
    # 14:20 the disciples stand round him; he rises and goes back in
    for k in range(4):
        on((14, 20), ("show", f"disciple{k}", 0.1 + k * 0.15, 0.6, None))
    on((14, 20),
       ("rot", "paul", 1.0, 0.6, 90), ("ink", "paul", 1.0, 0.6, TEXT),
       ("pose", "paul", 1.6, 0.2, {"pose": "walk", "arms": "down"}),
       ("move", "paul", 2.0, 1.0, (-180, 0)))
    effects(c)


def _pl():
    """How far a plinth lifts a man: its top, in card px."""
    return F.PLINTH_TOP / 97.0 * MAN


# camera shots inside the card: (x, y, zoom)
SHOTS = {
    (14, 8): (450, 1260, 1.15), (14, 9): (600, 1260, 1.0),
    (14, 10): (600, 1260, 1.0), (14, 11): (850, 1200, 0.62),
    (14, 12): (760, 1260, 1.0), (14, 13): (1900, 1220, 0.7),
    (14, 14): (1250, 1260, 0.75), (14, 15): (1700, 1020, 0.45),
    (14, 16): (1950, 1020, 0.45), (14, 17): (2340, 1200, 0.6),
    (14, 18): (1700, 1260, 0.85), (14, 19): (2230, 1280, 0.8),
    (14, 20): (2230, 1280, 0.8),
}
# shots on the way: (verse) -> [(kind, (x, y, z) or None, seconds)]
LEGS = {
    (14, 14): [("to", (1100, 1260, 0.75), 1.6), ("hold", None, 2.2),
               ("to", (1250, 1260, 0.75), 2.2)],
    (14, 15): [("hold", None, 5.0), ("to", (1700, 1020, 0.45), 4.0)],
    (14, 19): [("to", (1450, 1260, 0.8), 1.4), ("hold", None, 5.0),
               ("to", (2230, 1280, 0.8), 2.2)],
}
DUR = {(14, 8): 3.4, (14, 9): 1.4, (14, 11): 2.0, (14, 12): 1.5,
       (14, 13): 2.4, (14, 16): 3.0, (14, 17): 2.0, (14, 18): 1.8}


def effects(c):
    """The marks a verse draws over the cast."""
    g = GROUND
    # 14:9 Paul fastens his eyes on him (14:10: the look lets go)
    gaze = [(690, g - 102), (430, g - 66)]
    el, _L = traced_el(gaze, TEXT_DIM, 2.4, 0.8)
    c.effect((14, 9), f'<g stroke-width="2" stroke-dasharray="3 6">{el}</g>')
    c.effect((14, 10), f'<g stroke-width="2">{fade(0.0, 0.6, out=True)}'
                       f'<polyline points="690,{g - 102} 430,{g - 66}" '
                       f'fill="none" stroke="{rgb(TEXT_DIM)}" '
                       f'stroke-dasharray="3 6"/></g>')
    # 14:14 they tore their clothes: a rent down the front of each robe,
    # drawn on the figure so it goes where they go
    tear = (f'<polyline points="-3,-80 3,-70 -3,-60 3,-50 -2,-42" '
            f'fill="none" stroke="{rgb(BG)}" stroke-width="2.4"/>')
    c.on((14, 14), ("mark", "paul", 2.6, 0.6, tear),
         ("mark", "barnabas", 2.8, 0.6, tear))
    # 14:16 the nations each walking in their own ways: paths across the
    # plain, a walker on each
    paths = [[(2440, g + 6), (2380, 1270), (2300, 1180)],
             [(2470, g + 8), (2560, 1300), (2660, 1200)],
             [(2500, g + 10), (2700, 1340), (2900, 1250)],
             [(2520, g + 12), (2760, 1430), (3000, 1470)],
             [(2460, g + 14), (2440, 1500), (2420, 1600)]]
    now, after = [], []
    for k, pts in enumerate(paths):
        el, L = traced_el(pts, SAND, 0.4 + k * 0.2, 2.2)
        now.append(el)
        d = "M" + " L".join(f"{x} {y}" for x, y in pts)
        now.append(f'<circle r="5" fill="{rgb(TEXT)}" opacity="0">'
                   f'<set attributeName="opacity" to="1" '
                   f'begin="{1.0 + k * 0.2:.2f}s"/>'
                   f'<animateMotion path="{d}" begin="{1.0 + k * 0.2:.2f}s" '
                   f'dur="2.4s" fill="freeze"/></circle>')
        after.append(f'<polyline points="'
                     + " ".join(f"{x},{y}" for x, y in pts)
                     + f'" fill="none" stroke="{rgb(SAND_DIM)}"/>')
    c.effect((14, 16), '<g stroke-width="3" stroke-dasharray="4 8" '
                       'stroke-linecap="round">' + "".join(now) + "</g>",
             '<g stroke-width="3" stroke-dasharray="4 8" '
             'stroke-linecap="round">' + "".join(after) + "</g>")
    # 14:17 rains from the sky, under the clouds, once
    rain = []
    for k, (cx, cy) in enumerate(((2050, 880), (2350, 840), (2600, 920))):
        for j in range(7):
            x0 = cx - 60 + j * 22
            t = 2.6 + k * 0.2 + (j % 3) * 0.15
            rain.append(f'<line x1="{x0}" y1="{cy + 20}" x2="{x0 - 30}" '
                        f'y2="{g - 20}" stroke="{rgb(TEXT_DIM)}" '
                        f'stroke-width="2" stroke-dasharray="40 4000" '
                        f'stroke-dashoffset="40" opacity="0">'
                        f'<set attributeName="opacity" to="1" '
                        f'begin="{t:.2f}s"/>'
                        f'<animate attributeName="stroke-dashoffset" '
                        f'values="40;{-(g - cy)}" begin="{t:.2f}s" '
                        f'dur="1.0s" fill="freeze"/></line>')
    c.effect((14, 17), "".join(rain))
