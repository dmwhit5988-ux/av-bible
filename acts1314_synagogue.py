"""The synagogue at Antioch of Pisidia (Acts 13:15-16, 13:38-50) as a scene
card the camera dives into.

A side view of the town's synagogue cut open: the ark niche with its shut
scrolls, a lampstand, a bench of men on the left, the reading desk with the
two rulers seated behind it, a bench on the right where Paul and Barnabas sit
with the God-fearers; the east door and its steps; the street and the plaza;
the town wall and its gate; the road out over the hills.

The camera comes down into it at 13:15 and leaves at 13:17 to fly Israel's
story over the map; it comes back at 13:38 for the end of the sermon and stays
for the two Sabbaths: the hall empties, the followers trail the two out, the
whole city fills the plaza, the objectors gather on the steps, the Chi-Rho
(who is Jesus, never drawn as a man) goes out of the synagogue to Paul and
Barnabas and the doors shut behind it, the believers walk out of the gate,
and at 13:50 the two are driven out with it.

Card px: x from -1000 to 3400, y 0 to 2200, the ground at y 1400 and the hall
floor three steps higher. A man is 110 px tall.
"""

import svg_figures as F
from svg_scene_card import Actor, Card, MAN_H
from svg_map_camera import rgb
from svg_surface import _fmt
from generate_tabernacle import BG, SAND, SAND_DIM, TEXT, HL
from acts1314_lystra import (MAN, SKY, EARTH, PAVE, HILL, S_CARD, person,
                             static, scaled_h, figure_svg_at)

GROUND = 1400
FLOOR = 1370                    # the hall stands on a podium, three steps up
HALL = (520, 1580)
EAVES, RIDGE = 1100, 1010
ANCHOR = (1050, 1260)
ORIGIN = (-1000, 0)
SIZE = (4700, 2200)            # x from -1000 to 3700
SEAT_Y = FLOOR - 33             # a bench plank, at a seated man's hips
NAME_SIT, NAME_STAND = -100, -132
CHIRHO_OUT = (1852, GROUND)     # where the Chi-Rho stands, 13:46-49
CHIRHO_H = F.bbox((F.chi_rho(), 0))[3]   # its height, figure units
WALL = (42, 42, 34)
HALL_IN = (30, 31, 27)


def build(town_xy):
    c = Card("syn", town_xy, ANCHOR, SIZE, S_CARD, page=EARTH, sky=SKY,
             ground_y=GROUND, origin=ORIGIN)
    X0, X1 = ORIGIN[0], ORIGIN[0] + SIZE[0]
    sc = c.scenery

    # far hills, the ground, the plaza
    hills = [(X0, 1220), (-500, 1170), (0, 1230), (500, 1150), (1000, 1200),
             (1700, 1130), (2300, 1180), (2800, 1090), (3400, 1150),
             (X1, GROUND), (X0, GROUND)]
    sc.append(f'<polygon points="' + " ".join(f"{x},{y}" for x, y in hills)
              + f'" fill="{rgb(HILL)}" stroke="{rgb(SAND_DIM)}" '
              f'stroke-width="2"/>')
    sc.append(f'<rect x="{X0}" y="{GROUND}" width="{X1 - X0}" '
              f'height="{SIZE[1] - GROUND}" fill="{rgb(EARTH)}"/>')
    sc.append(f'<rect x="1620" y="{GROUND}" width="880" height="40" '
              f'fill="{rgb(PAVE)}"/>')
    sc.append(f'<line x1="{X0}" y1="{GROUND}" x2="{X1}" y2="{GROUND}" '
              f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    sc.append(f'<rect x="2660" y="{GROUND}" width="{X1 - 2660}" height="22" '
              f'fill="{rgb(PAVE)}"/>')
    for k, x in enumerate((-900, -520, -140, 230, 1760, 2050, 2330)):
        f = 0.78 if k % 2 else 0.9
        sc.append(figure_svg_at(F.house(), x, GROUND, scaled_h("house") * f,
                                SAND_DIM, unit_h=MAN_H * F.UNIT["house"]))
    # the town wall and its east gate
    for x0, x1 in (("2470", "2560"), ("2640", "2700")):
        sc.append(f'<rect x="{x0}" y="{GROUND - 270}" '
                  f'width="{int(x1) - int(x0)}" height="270" '
                  f'fill="{rgb(WALL)}" stroke="{rgb(SAND_DIM)}" '
                  f'stroke-width="2"/>')
    sc.append(figure_svg_at(F.gate(), 2600, GROUND, scaled_h("gate"),
                            SAND_DIM, unit_h=MAN_H * F.UNIT["gate"]))

    # the synagogue, cut open: podium, back wall, roof, walls, steps
    h0, h1 = HALL
    sc.append(f'<rect x="{h0}" y="{FLOOR}" width="{h1 - h0}" '
              f'height="{GROUND - FLOOR}" fill="{rgb(WALL)}" '
              f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    sc.append(f'<rect x="{h0}" y="{EAVES}" width="{h1 - h0}" '
              f'height="{FLOOR - EAVES}" fill="{rgb(HALL_IN)}"/>')
    sc.append(f'<polygon points="{h0 - 30},{EAVES} {(h0 + h1) / 2},{RIDGE} '
              f'{h1 + 30},{EAVES}" fill="{rgb(WALL)}" '
              f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    sc.append(f'<rect x="{h0}" y="{EAVES}" width="20" '
              f'height="{FLOOR - EAVES}" fill="{rgb(WALL)}" '
              f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    sc.append(f'<rect x="{h1 - 20}" y="{EAVES}" width="20" height="120" '
              f'fill="{rgb(WALL)}" stroke="{rgb(SAND_DIM)}" '
              f'stroke-width="2"/>')
    for k in range(3):                              # the steps down
        sc.append(f'<rect x="{h1 + k * 27}" y="{FLOOR + k * 10}" '
                  f'width="{80 - k * 27}" height="10" fill="{rgb(WALL)}" '
                  f'stroke="{rgb(SAND_DIM)}" stroke-width="1.5"/>')
    # the ark niche in the west wall
    sc.append(f'<path d="M560 {FLOOR - 40} L560 {FLOOR - 140} '
              f'Q590 {FLOOR - 172} 620 {FLOOR - 140} L620 {FLOOR - 40}Z" '
              f'fill="{rgb(BG)}" stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    # the benches
    for b0, b1 in ((710, 1040), (1170, 1500)):
        sc.append(f'<rect x="{b0}" y="{SEAT_Y}" width="{b1 - b0}" height="7" '
                  f'fill="{rgb(SAND_DIM)}"/>')
        for x in (b0 + 10, (b0 + b1) / 2, b1 - 14):
            sc.append(f'<rect x="{_fmt(x)}" y="{SEAT_Y}" width="5" '
                      f'height="{FLOOR - SEAT_Y}" fill="{rgb(SAND_DIM)}"/>')

    # -- the cast, in drawing order ----------------------------------------
    for k, x in enumerate((572, 590, 608)):
        c.add(Actor(f"ark{k}", static(F.scroll, shut=True), x, FLOOR - 44,
                    h=scaled_h("scroll"),
                    unit_h=MAN_H * F.UNIT["scroll"], ink=SAND, shown=True))
    c.add(Actor("lampstand", static(F.lampstand), 662, FLOOR,
                h=scaled_h("lampstand"), unit_h=MAN_H * F.UNIT["lampstand"],
                ink=SAND, shown=True))
    left = []
    for k in range(8):
        left.append(c.add(Actor(f"left{k}", person("man"), 728 + k * 42,
                                FLOOR, ink=SAND, pose={"pose": "sit"},
                                shown=True, flip=1)))
    for k, x in enumerate((1052, 1112)):
        c.add(Actor(f"ruler{k}", person("man"), x, FLOOR, ink=SAND,
                    pose={"pose": "sit"}, shown=True,
                    flip=1 if k else -1))
    c.add(Actor("desk", static(F.table, span=0.5), 1082, FLOOR,
                h=scaled_h("table"), unit_h=MAN_H * F.UNIT["table"],
                ink=SAND, shown=True))
    top = 35 * F.UNIT["table"] * MAN / MAN_H      # the desk's top, card px
    c.add(Actor("desk_scroll", static(F.scroll), 1082, FLOOR - top,
                h=scaled_h("scroll") * 0.8, unit_h=MAN_H * F.UNIT["scroll"],
                ink=SAND, shown=True))
    c.add(Actor("rulers_name", static(lambda: []), 1082, FLOOR, h=1,
                unit_h=1, label_y=NAME_SIT - 40, shown=True))
    right = []
    for k, (kind, x) in enumerate((("man", 1300), ("woman", 1338),
                                   ("man", 1376), ("woman", 1414),
                                   ("man", 1452), ("woman", 1488))):
        right.append(c.add(Actor(f"right{k}", person(kind), x, FLOOR,
                                 ink=SAND, pose={"pose": "sit"}, shown=True,
                                 flip=-1)))
    c.add(Actor("paul", person("man"), 1182, FLOOR, ink=TEXT,
                pose={"pose": "sit"}, shown=True, flip=-1,
                label_y=NAME_SIT))
    c.add(Actor("barnabas", person("man", staff=True), 1240, FLOOR,
                ink=TEXT, pose={"pose": "sit"}, shown=True, flip=-1,
                label_y=NAME_SIT - 30, label_dx=40))
    # the city that comes to hear (13:44), and the chief men and women
    crowd = []
    kinds = ["man", "woman", "man", "child", "woman", "man"]
    for k in range(60):
        kind = kinds[k % len(kinds)]
        tx = 1660 + (k * 137) % 820             # where each one ends up
        ty = GROUND + (k % 3) * 12
        sx = 2640 if k % 2 == 0 else 1580       # in by the gate or the street
        a = c.add(Actor(f"crowd{k}", person(kind), sx, ty, ink=SAND,
                        flip=-1 if k % 3 else 1))
        a.target_x = tx
        crowd.append(a)
    for k, (kind, x) in enumerate((("woman", 2230), ("woman", 2262),
                                   ("man", 2300), ("man", 2336))):
        c.add(Actor(f"chief{k}", person(kind, **({"staff": True}
                                                if kind == "man" else {})),
                    x, GROUND + 4, ink=SAND, flip=-1))
    c.add(Actor("chirho", static(F.chi_rho), 1082, FLOOR - 190, h=70,
                unit_h=CHIRHO_H, ink=HL))
    c.add(Actor("door", static(door_slab), HALL[1] - 20, FLOOR, h=1,
                unit_h=1, ink=SAND))

    c.refs = [(13, v) for v in list(range(15, 17)) + list(range(38, 51))]
    events(c, left, right, crowd)
    return c


def door_slab():
    """The east door, shut: a slab filling the doorway, its hinge on the
    wall (x 0), so a scale from the hinge swings it to."""
    return [("fill", [(0, 0), (20, 0), (20, 128), (0, 128)], "wood"),
            ("line", [(10, 4), (10, 124)], "rule")]


def events(c, left, right, crowd):
    on = c.on
    # 13:15 the reading, and the rulers' invitation
    on((13, 15), ("pulse", "desk_scroll", 4.2, 0.8, None),
       ("pose", "ruler0", 5.6, 0.4, {"arms": "open"}),
       ("pose", "ruler1", 5.6, 0.4, {"arms": "open"}),
       ("label", "rulers_name", 6.0, 0, "rulers"),
       ("label", "paul", 6.3, 0, "Paul"),
       ("label", "barnabas", 6.5, 0, "Barnabas"))
    # 13:16 Paul stood up, and beckoning with his hand
    on((13, 16), ("pose", "paul", 0.5, 0.5, {"pose": "stand"}),
       ("name_dy", "paul", 0.5, 0.5, NAME_STAND - NAME_SIT),
       ("pose", "paul", 1.0, 0.4, {"arms": "point_r"}))
    for a in left:
        on((13, 16), ("pulse", a.key, 2.4, 0.8, None))
    for a in right:
        on((13, 16), ("pulse", a.key, 3.8, 0.8, None))
    # 13:38 proclaimed to you
    on((13, 38), ("pose", "paul", 5.4, 0.4, {"arms": "open"}))
    # 13:39 everyone who believes; the law of Moses
    for a in left + right:
        on((13, 39), ("pulse", a.key, 2.2, 0.8, None))
    for k in range(3):
        on((13, 39), ("pulse", f"ark{k}", 5.4, 0.8, None))
    # 13:40 spoken in the prophets
    on((13, 40), ("pulse", "desk_scroll", 2.8, 0.8, None))
    # 13:41 I work a work in your days
    on((13, 41), ("show", "chirho", 4.0, 0.8, None),
       ("move", "chirho", 4.0, 0.8, (0, -12)),
       ("pose", "paul", 6.2, 0.4, {"arms": "point_l"}))

    # 13:42 the Jews go out; the Gentiles beg to hear more
    for k, a in enumerate(left):
        t = 1.2 + k * 0.3
        tx = 1690 + k * 26 - a.start["x"]
        on((13, 42), ("pose", a.key, 0.4, 0.6, {"pose": "stand"}),
           ("pose", a.key, t, 0.2, {"pose": "walk"}),
           ("flip", a.key, t, 0.2, -1 if k < 4 else 1),
           ("move", a.key, t, 2.6 - k * 0.15, (tx, GROUND - FLOOR)),
           ("pose", a.key, t + 2.6 - k * 0.15, 0.2, {"pose": "stand"}))
    for a in right:
        on((13, 42), ("pose", a.key, 2.0, 0.4, {"pose": "stand"}),
           ("pose", a.key, 2.6, 0.4, {"arms": "open"}))
    # 13:43 Paul and Barnabas go out; many follow them
    on((13, 43), ("pose", "barnabas", 1.6, 0.4, {"pose": "stand"}),
       ("name_dy", "barnabas", 1.6, 0.4, NAME_STAND - NAME_SIT))
    for key, dx in (("paul", 640), ("barnabas", 640)):
        on((13, 43), ("pose", key, 2.0, 0.2, {"pose": "walk", "arms": "down"}),
           ("flip", key, 2.0, 0.2, 1),
           ("move", key, 2.0, 2.5, (dx, GROUND - FLOOR)),
           ("pose", key, 4.5, 0.2, {"pose": "stand"}),
           ("pose", key, 6.0, 0.4, {"arms": "open"}))
    followers = left[:4] + right[:3]
    for k, a in enumerate(followers):
        t = 2.6 + k * 0.3
        x_now = 1690 + k * 26 if k < 4 else a.start["x"]
        dy = 0 if k < 4 else GROUND - FLOOR
        on((13, 43), ("pose", a.key, t, 0.2, {"pose": "walk",
                                              "arms": "down"}),
           ("flip", a.key, t, 0.2, 1),
           ("move", a.key, t, 2.2, (1960 + k * 30 - x_now, dy)),
           ("pose", a.key, t + 2.2, 0.2, {"pose": "stand"}),
           ("flip", a.key, t + 2.2, 0.2, -1))
    # 13:44 almost the whole city gathered together
    for k, a in enumerate(crowd):
        t = 1.0 + (k % 20) * 0.13
        on((13, 44), ("show", a.key, t, 0.3, None),
           ("move", a.key, t, 1.0, (a.target_x - a.start["x"], 0)))
    # 13:45 jealousy: the men on the steps contradict Paul
    steps = left[4:] + crowd[:2]
    for k, a in enumerate(steps):
        x_now = 1690 + (k + 4) * 26 if k < 4 else a.target_x
        on((13, 45), ("move", a.key, 1.6 + k * 0.1, 1.0,
                      (1588 + k * 12 - x_now, -8 + k % 2 * 6)),
           ("flip", a.key, 2.6, 0.4, 1),
           ("pose", a.key, 3.0, 0.4, {"arms": "point_r"}),
           ("pulse", a.key, 3.6, 0.8, None))
    # 13:46 to you first; you thrust it from you; we turn to the Gentiles
    on((13, 46), ("flip", "paul", 1.6, 0.4, -1),
       ("flip", "barnabas", 1.6, 0.4, -1),
       ("pose", "paul", 1.6, 0.4, {"arms": "point_l"}),
       ("pose", "barnabas", 1.6, 0.4, {"arms": "point_l"}),
       ("move", "chirho", 6.0, 1.4, (CHIRHO_OUT[0] - 1082,
                                    GROUND - (FLOOR - 202))),
       ("show", "door", 7.4, 0.2, None), ("grow_x", "door", 7.4, 0.8, None),
       ("flip", "paul", 11.4, 0.4, 1), ("flip", "barnabas", 11.4, 0.4, 1),
       ("pose", "paul", 11.4, 0.4, {"arms": "point_r"}),
       ("pose", "barnabas", 11.4, 0.4, {"arms": "point_r"}))
    # 13:47 a light for the Gentiles
    on((13, 47), ("scale", "chirho", 1.0, 1.0, 1.6))
    # 13:48 the Gentiles were glad; as many as were appointed believed
    on((13, 48), ("scale", "chirho", 0.4, 3.0, 1 / 1.6))
    order = sorted(crowd[2:], key=lambda a: a.target_x)
    for k, a in enumerate(order):
        on((13, 48), ("pose", a.key, 4.0 + k * 0.02, 0.3, {"arms": "up"}))
    for a in order[10:18]:
        on((13, 48), ("pulse", a.key, 5.4, 0.8, None))
    # 13:49 the word spread abroad throughout all the region
    for k, a in enumerate(order[-4:]):
        t = 0.4 + k * 0.12
        on((13, 49), ("pose", a.key, t, 0.2, {"pose": "walk",
                                              "arms": "down"}),
           ("flip", a.key, t, 0.2, 1),
           ("move", a.key, t, 2.0,
            (2900 + k * 110 - a.target_x, -150 - k * 30)),
           ("scale", a.key, t, 2.0, 0.6))
    # 13:50 the chief men and women; they are thrown out
    for k in range(4):
        on((13, 50), ("show", f"chief{k}", 1.0 + k * 0.2, 0.6, None))
    for a in order[:12]:
        on((13, 50), ("pose", a.key, 3.4, 0.6, {"arms": "point_r"}))
    on((13, 50),
       ("pose", "paul", 4.4, 0.2, {"pose": "walk", "arms": "down"}),
       ("pose", "barnabas", 4.4, 0.2, {"pose": "walk", "arms": "down"}),
       ("move", "paul", 4.6, 1.8, (880, 0)),
       ("move", "barnabas", 4.6, 1.8, (880, 0)),
       ("move", "chirho", 4.6, 1.8, (880, 0)))
    for a in order[:3]:
        on((13, 50), ("move", a.key, 4.8, 1.6, (300, 0)))


# camera shots inside the card: (x, y, zoom)
SHOTS = {
    (13, 15): (1080, 1300, 1.08), (13, 16): (1150, 1300, 1.2),
    (13, 38): (1050, 1250, 0.6), (13, 39): (1000, 1270, 0.75),
    (13, 40): (1080, 1290, 1.2), (13, 41): (1050, 1250, 0.62),
    (13, 42): (1250, 1240, 0.75), (13, 43): (1720, 1260, 0.8),
    (13, 44): (1650, 1150, 0.45), (13, 45): (1680, 1260, 0.8),
    (13, 46): (1950, 1260, 0.72), (13, 48): (2000, 1240, 0.75),
    (13, 49): (2700, 1240, 0.7), (13, 50): (2300, 1260, 0.8),
}
# the flights inside a verse: [(kind, (x, y, z) or None, seconds)]
LEGS = {
    (13, 15): [("to", (1050, 1290, 1.0), 3.8), ("hold", None, 2.8),
               ("to", (1080, 1300, 1.08), 3.0)],
    (13, 46): [("to", (1650, 1260, 0.72), 1.6), ("hold", None, 10.0),
               ("to", (1950, 1260, 0.72), 1.6)],
}
DUR = {(13, 16): 1.4, (13, 38): 5.4, (13, 39): 1.6, (13, 40): 1.4,
       (13, 41): 2.6, (13, 42): 1.4, (13, 43): 2.0, (13, 44): 2.0,
       (13, 45): 1.6, (13, 48): 3.6, (13, 49): 1.4, (13, 50): 1.2}
