"""Joshua 14: the opening of the allotment, and Caleb. People act where the
text has people acting, and the map carries what Caleb says, because what he
says is where he walked.

Three surfaces:
- Gilgal, a scene card (build_gil) hung at gilgal_jericho: Joshua, Eleazar, the
  jar and the twelve companies where joshua18_shiloh's card stands them, with
  no Tent; the standards come up as the text says the tribes. The camp's tents
  and the hills are behind.
- Hebron, a scene card (build_heb) hung at hebron: a far ridge, a near hill, and
  the Anakim before their wall.
- The map's cast (cast): figures pinned on the map, one screen size through a
  flight (svg_map_camera.pin, rider). One gold man on one line.
generate_joshua1319_svg.py flies the camera and hosts all three (its CARDS,
map_at and build_all); svg_scene_card.py draws the cards.

The story, verse by verse:
- 14:1 the camera dives from the whole land to the card as "Canaan" is said, the
  head of each company steps out, and the standards rise at "tribes";
- 14:2 Joshua's free hand goes over the jar and comes up with a lot, and 9 and
  1/2 come in over the row as "nine" and "half-tribe" are said;
- 14:3 the whole land, the tour's one frame of the sum: 9 1/2 in the sea, 2 1/2
  beyond the Jordan, and 0 beside LEVI in the key;
- 14:4 Joseph is two: his companies step down over a bracket. The Levites open
  empty hands; a city, a house and a far gate rise behind them, and the sheep
  and the ox walk in at "suburbs" and "livestock";
- 14:5 those go, and the leaders' arms go out across the twelve, Joshua's to the
  left and Eleazar's to the right;
- 14:6 Judah steps forward and Caleb walks out of it to speak to Joshua. The
  camera rises to the map at "spoke", and Moses, Caleb and the young Joshua
  rise at Kadesh Barnea as they are named;
- 14:7 40 joins his name; Moses points at him. At "to spy" he walks the line to an
  unnamed dot, the gold line drawing behind him (WALK_UP), the young Joshua a step
  behind him and ten dots after them. At "brought" the two walk back, and the ten
  stay at the dot;
- 14:8 the line goes dashed. The ten ride down it, and forty come in under Moses
  and Joshua and slump to a mound at "melt", while he walks on, to the wilderness
  of Zin;
- 14:9 Moses' arm goes up at "swore", the line lights at "land", a soft disc
  comes up at the dot, two children rise on it, and he walks on, to the South;
- 14:10 Joshua goes first, and then the mound and Moses' name, as the camera leaves,
  before the inset and the frame's edge can take them; Moses, the children and the
  disc go at "alive". At "these" the Salt Sea's name, which he would cross, goes, and he
  walks forty-five years the long way round (WALK_YEARS), twelve dots coming in
  beside him at "Israel"; his 40 goes as the 45 comes in, and his tag stays off
  while he passes the sea and the lots' discs. He reaches Gilgal at the second
  "Now", and 85 comes in at "eighty-five". The pin stands at the card's Caleb's
  own point, so the camera dives from the one to the other, the pin gone as the
  two come to match in size;
- 14:11 his younger self walks in beside him and they raise their arms together;
  he takes spear and shield at "war", and marches out and back;
- 14:12 the camera goes to the map at "give me this hill country", then to the
  Anakim, the wall and the towers as they are named, and he walks up in gold and
  stops short. They do not move: "It may be". The camera rises to Gilgal;
- 14:13 Joshua's arm goes up at "blessed", and at "gave" he walks straight from
  Gilgal to Hebron, its name and its disc coming in, and the straight line fades
  as he arrives; a ring goes out at "inheritance";
- 14:14 the children rise beside him at "to this day", and at "followed" the
  camera draws back and the light runs up the old line from Kadesh to his feet.
  The place he spied at 40 is the place he is given at 85;
- 14:15 the camera dives to the hill. "Hebron" and "Kiriath Arba" stand over the
  gate, the greatest of the giants steps out, and at "Then" Caleb's arms go as
  the camera rises to the whole land, as 14:1 opened.

What is not in the text. None of it carries a name on screen but Moses and Joshua
at Kadesh and "Hill country", which are the text's words and our placing of them.
- At Gilgal: Gilgal as the scene of 14:1-5 (Canaan is the only name in its sky until
  14:6); the camp's tents and the hills; the twelve companies, a woman in each, and
  their heads stepping out; the standards and their colours, a blank pennant against
  a coloured one for a lot not yet given; the jar and the pebble; Joshua's and
  Eleazar's arms; the figures 9 1/2, 2 1/2 and 0; Joseph's companies stepping down
  over a bracket; four Levites, their open hands, their city and animals (their real
  cities are Joshua 21); Caleb's arms at "said" and his point at "You".
- On the map: Moses and Joshua at Kadesh, Moses pointing, his arm at "swore", and the
  route up (Num 13:21-22); the twelve spies going up together (Num 13:8,16), Caleb and
  Joshua coming back ahead of the ten, the ten as dots and forty more (Num 13-14);
  Caleb's arms at "heart"; his walk on at "wholly"; the line lit at 14:9's "land"; the
  disc at Hebron's dot, and two children, a plural sign and not a count; the fading at
  "alive", with Joshua leaving the picture at its opening, though Num 14:30 and 14:38
  keep him alive and he is back on the card at the verse's end; the forty-five years'
  route (Num 21 and 33, Deut 2) and Israel as twelve dots beside him; "Hill country" pinned at the Judah region's point; Joshua's arm at
  "blessed"; the straight walk to Hebron and its ring; Hebron's disc in Judah's colour
  from 14:13, ahead of Judah's lot; the light up the line.
- At 14:11 and Hebron: his younger self; his spear and shield and the march; his walk
  to the Anakim, who are three and drawn with the Nephilim figure of Num 13:33; the
  wall, towers and far gates, the terraces and the far ridge; the greatest man drawn
  as one of the three, though Arba is Anak's father, and his 12%.

Card px: the Gilgal card is 5600 x 2400 with its ground at y 1400 and its middle
at x 0, as Shiloh's; the Hebron card is 4800 x 2200. A man is 110 px tall on
both.

A cue is `cue(say, ref, word, today's value, lead)`, so re-rendering an MP3 moves what
is timed by a word, and nothing else. What must then be retuned by hand:
- the camera's legs (LEGS); what ends with a leg follows it (leg_end: DIVE, HILL_OUT,
  HILL_BACK, and the beats in gil_events and _because that ask it);
- what is set against the camera, the zoom a card shows at or a place coming into
  frame: MOSES_IN, HEBRON_IN, NINE_IN, HILL_IN, KADESH_NAME_IN, JOSHUA_OFF, NAMES_OFF,
  GILGAL_OFF, GILGAL_NAME_OFF, TAG_OFF, PIN_OFF, MARK_IN, TAG_PAST, and the 0.8 s Gilgal takes to
  go at 14:14;
- the fixed lengths that must fit between two words: UP_S, HOME_S, TEN_LAG, TEN_UP_S,
  TEN_S, ZIN_S, GIVEN_S, LIGHT_S;
- the leads set by ear against today's MP3s where the clock runs late inside a long
  clause: 14:6's Judah, came, me and you, and 14:4's suburbs.
`_clock_qc` says where the words have overtaken the camera or a fixed length. It and
leg_end read LEGS as written, so an MP3 too short for its legs, which squeezes them, is
reported apart: the tour's main prints SQUEEZED for it.

`qc` checks each rest on a card for a name or number within AIR of another, of a
figure's ink, of the title, or of 14:4's bracket. `cast_qc` checks each rest on the map
and 14:10's long hold, reading what the helpers draw (`_Standing.read`): a name or
number within AIR of another, a figure, a mark, a line, the water, a lot's disc, the
key or a plate, or cut by the frame; and a figure or mark within AIR of a plate or cut
by the frame. It follows his tag along each walk and the ten along theirs, and asks
the clock (`_clock_qc`). The figures aren't followed as they walk.

The tour's main prints LATE for 14:2, 14:11 and 14:13. Those are the design's, motion
running to the end of the narration; any other is a real one.
"""

import math
import re
from typing import Callable, NamedTuple

import allotment as AL
import gazetteer as GZ
import joshua18_shiloh as SH
import svg_figures as F
from generate_tabernacle import BG, H, HL, SAND, SAND_DIM, TEXT, TEXT_DIM, W
from generate_tribal_maps import LAND
from passages import verse_numbers
from svg_map_camera import (EASE, band_dots, circle_hits_rect, ease, emit_class,
                            fade, ink, inflate, lift_in, pin, poly_el,
                            poly_hits_rect, rgb, rider, screen_ring, seg_len,
                            title_rect, to_screen, traced_el)
from svg_scene_card import (Actor, Card, MAN_H, apply_event, figure_svg, gap,
                            ink_points, name_op, person, shot_rect, static, within)
from svg_surface import _fmt

GROUND, MAN, PXU = SH.GROUND, SH.MAN, SH.PXU
SKY, EARTH, HILL, FAR_HILL = SH.SKY, SH.EARTH, SH.HILL, SH.FAR_HILL
S_CARD, ROW_Y, PEOPLE = SH.S_CARD, SH.ROW_Y, SH.PEOPLE
cue = SH.cue
REFS = [(14, v) for v in verse_numbers("Joshua", 14)]
YOUNG = (190, 178, 140)         # a man as he was: Joshua at Kadesh, Caleb at 40
DIM = (150, 140, 112)           # 14:15: the two who aren't the greatest
MARK_Y, MARK_PX = -196, 46      # a number over a man's head, from his feet (card px)
# 14:2's 9 and 1/2, in the sky over the row
SKY_Y, SKY_PX, SKY_NINE_X, SKY_HALF_X = 980, 110, -14, 64


def numeral(text, y=MARK_Y, x=0, px=MARK_PX, fill=HL):
    """A number on a card, card px: over a man's head as a `mark`, or in the
    sky as an effect. Its own <text>, so WebKit sets it on its baseline."""
    return (f'<text x="{x}" y="{y}" font-size="{px}" font-weight="bold" '
            f'fill="{rgb(fill)}" stroke="{rgb(SKY)}" stroke-width="5" '
            f'stroke-opacity="0.8" paint-order="stroke" text-anchor="middle" '
            f'dominant-baseline="central">{text}</text>')


def armed_make(armed=False, **pose):
    """Caleb: a man, or a soldier once he takes spear and shield. A soldier
    has no free hand, so his arms draw nothing new."""
    return F.soldier(**pose) if armed else F.man(**pose)


# One maker per kind, so a card's actors share their drawings (svg_scene_card.person)
GATE, HOUSE = static(F.gate), static(F.house)
TOWER, WALL = static(F.tower), static(F.wall, 380, 230)
SHEEP, OX, ANAK = static(F.sheep), static(F.ox), static(F.nephilim)


def walk(c, ref, keys, t, dur, dx, dy=0, face=None, end_face=None):
    """They walk: the walking pose, the move, and standing again."""
    for k in keys:
        ev = [("pose", k, t, 0.15, {"pose": "walk"})]
        if face is not None:
            ev.append(("flip", k, t, 0.15, face))
        ev.append(("move", k, t, dur, (dx, dy)))
        ev.append(("pose", k, round(t + dur, 2), 0.2, {"pose": "stand"}))
        if end_face is not None:
            ev.append(("flip", k, round(t + dur, 2), 0.2, end_face))
        c.on(ref, *ev)


def slide(c, ref, keys, t, dur, dx, dy=0):
    for k in keys:
        c.on(ref, ("move", k, t, dur, (dx, dy)))


# ---------------------------------------------------------------------------
# The Gilgal card: the companies where Shiloh's card will stand them
# ---------------------------------------------------------------------------

G_ANCHOR, G_SIZE, G_ORIGIN = (0, 1330), (5600, 2400), (-2800, 0)
G_RIDGE = [(-2800, 1236), (-2200, 1212), (-1500, 1240), (-800, 1222),
           (-300, 1244), (260, 1250), (1100, 1240), (1800, 1208), (2400, 1234),
           (2800, 1218)]
G_FAR = [(-2800, 1168), (-1900, 1132), (-1000, 1160), (-100, 1128), (800, 1152),
         (1700, 1116), (2800, 1146)]
G_TENTS = (-2500, -2050, -1600, -1150, -780, -440, 660, 1150, 1600, 2050, 2500)
# the lots already given when 14:1 opens (13:8-33): their pennants come up
# coloured, and the rest empty
G_LOT = {"Reuben": "REUBEN", "Gad": "GAD"}
NINE = [t for t in SH.LEFT + SH.RIGHT if t not in G_LOT and t != "Manasseh"]
HEADS = [f"{t}2" for t in SH.LEFT + SH.RIGHT]
MAN_E = (438, ROW_Y + 30)       # Manasseh's east half, its own pennant
LEVI_X, LEVI_Y = (172, 210, 248, 286), ROW_Y - 14
CITY = (205, 1262)              # 14:4: the gate on its rise, and the house by it
FAR_GATE = (-165, 1240)
# 14:4: the animals walk in from the right and stop clear of every pole and of
# the people's feet
SHEEP_X, SHEEP_STOP, SHEEP_Y = (640, 720, 800), (-20, 50, 120), (1500, 1518, 1500)
OX_X, OX_STOP, OX_Y = 960, 258, 1534
JOSEPH = ([f"Ephraim{j}" for j in range(SH.FOLK)] + ["std_Ephraim"],
          [f"Manasseh{j}" for j in range(SH.FOLK)] + ["std_Manasseh", "std_ManE"])
BRACKET = (345, 1530, 505, 1543)        # 14:4's, its box; it opens upward


def folk_x(tribe, j, gx):
    """A man of a company: Manasseh's stand apart in two halves."""
    if tribe == "Manasseh":
        return gx + (-58, -36, 2, 24, 46)[j]
    return gx - 44 + j * 22


def build_gil(town_xy, lot_col, say=None):
    """The Gilgal card hung at the town's world point. `lot_col` maps a lot's
    colour key to its colour on the map; `say(ref, word)` is when the
    narration says a word (seconds, or None), which times the beats."""
    c = Card("gil", town_xy, G_ANCHOR, G_SIZE, S_CARD, page=EARTH, sky=SKY,
             ground_y=GROUND, origin=G_ORIGIN)
    # as Shiloh's: the sky's names may show on the wider shots, the people's
    # wait for closer ones, and a name cut by a rest goes as it leaves
    c.names_at = (0.30, 0.38)
    c.cut_late = True
    c.share_bodies = True
    X0, X1 = G_ORIGIN[0], G_ORIGIN[0] + G_SIZE[0]

    # -- scenery: the hills, the city's rise, the ground, the camp's tents -
    for ridge, fill in ((G_FAR, FAR_HILL), (G_RIDGE, HILL)):
        pts = ridge + [(X1, GROUND), (X0, GROUND)]
        c.scenery.append('<polygon points="' + " ".join(f"{x},{y}" for x, y in pts)
                         + f'" fill="{rgb(fill)}" stroke="{rgb(SAND_DIM)}" '
                         f'stroke-width="2"/>')
    c.scenery.append(f'<path d="M-40 {GROUND} C 40 1282 90 1262 228 1262 C 366 1262 '
                     f'430 1282 520 {GROUND}Z" fill="{rgb(HILL)}" '
                     f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    c.scenery.append(f'<rect x="{X0}" y="{GROUND}" width="{G_SIZE[0]}" '
                     f'height="{G_SIZE[1] - GROUND}" fill="{rgb(EARTH)}"/>')
    c.scenery.append(f'<line x1="{X0}" y1="{GROUND}" x2="{X1}" y2="{GROUND}" '
                     f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    for k, x in enumerate(G_TENTS):
        c.scenery.append(SH.figure_svg_at(F.tent(), x, GROUND - 30, SAND_DIM,
                                          flip=-1 if k % 2 else 1))

    # -- 14:4's city, behind the people ------------------------------------
    c.add(Actor("city", GATE, *CITY, h=MAN * 0.4, ink=SAND))
    c.add(Actor("cityh0", HOUSE, CITY[0] - 150, CITY[1] + 10, h=MAN * 0.4, ink=SAND))
    c.add(Actor("cityh1", GATE, *FAR_GATE, h=MAN * 0.2, ink=SAND))

    # -- the congregation: Caleb is the last of Judah's near company -------
    for tribe in SH.LEFT + SH.RIGHT:
        gx = SH.company_x(tribe)
        key = G_LOT.get(tribe)
        judah = tribe == "Judah"
        c.add(Actor(f"std_{tribe}", SH.standard_make, gx + (-12 if judah else 50),
                    ROW_Y - 6, h=MAN, ink=lot_col[key] if key else SAND,
                    pose={"blank": key is None},
                    label_y=-255 if judah else None,
                    names_at=PEOPLE if judah else None))
        for j in range(SH.FOLK):
            is_caleb = judah and j == 4
            make = armed_make if is_caleb else person("woman" if j == 3 else "man")
            c.add(Actor("caleb" if is_caleb else f"{tribe}{j}", make,
                        folk_x(tribe, j, gx), ROW_Y + (j % 2) * 12, ink=SAND,
                        shown=True, flip=1 if gx < 0 else -1, names_at=PEOPLE,
                        label_y=24 if is_caleb else None))
    c.add(Actor("std_ManE", SH.standard_make, *MAN_E, h=MAN,
                ink=lot_col["MANASSEH_E"], pose={"blank": False}))
    for i, x in enumerate(LEVI_X):
        c.add(Actor(f"lev{i}", person("man"), x, LEVI_Y, ink=SAND, shown=True))
    c.add(Actor("joshua", person("man", staff=True), *SH.JOSHUA, ink=TEXT,
                shown=True, names_at=PEOPLE, label_y=-148))
    c.add(Actor("eleazar", person("priest"), *SH.ELEAZAR, ink=TEXT, shown=True,
                flip=-1, names_at=PEOPLE, label_y=-148))
    c.add(Actor("jar", static(F.jar), *SH.JAR, h=MAN, ink=SAND, shown=True))
    mouth = (SH.JAR[0], SH.JAR[1] - F.bbox((F.jar(), 0))[3] * PXU)
    c.add(Actor("lot0", static(F.lot), *mouth, h=MAN, ink=TEXT))
    for i, x in enumerate(SHEEP_X):
        c.add(Actor(f"sheep{i}", SHEEP, x, SHEEP_Y[i], h=MAN, ink=SAND, flip=-1))
    c.add(Actor("ox", OX, OX_X, OX_Y, h=MAN, ink=SAND, flip=-1))
    # names with no figure: the sky's, and the ones 14:4 writes under the people
    c.add(Actor("canaan", static(list), -60, 1050, label_y=0, shown=True,
                label_fill=TEXT_DIM, label_italic=True))
    c.add(Actor("gilgal", static(list), -60, 1090, label_y=0, shown=True,
                label_fill=TEXT_DIM, label_italic=True))
    for key, x, y in (("joseph", 425, 1566), ("n_lev", 229, LEVI_Y - 132),
                      ("n_eph", 345, ROW_Y + 72), ("n_man", 505, ROW_Y + 72)):
        c.add(Actor(key, static(list), x, y, label_y=0, shown=True,
                    names_at=PEOPLE))
    c.add(Actor("young", person("man"), -432, 1490, ink=YOUNG))
    c.refs = REFS
    gil_events(c, say)
    return c


def gil_events(c, say=None):
    on = c.on
    # 14:1 the names as they are said, the heads step out, the standards rise
    # left to right at "tribes", and the leaders open their arms at "distributed"
    r = (14, 1)
    on(r, ("label", "canaan", cue(say, r, "Canaan", 4.02, lead=-0.1), 0, "Canaan"),
       ("label", "eleazar", cue(say, r, "Eleazar", 4.83), 0, "Eleazar"),
       ("label", "joshua", cue(say, r, "Joshua", 6.21), 0, "Joshua"))
    t = cue(say, r, "heads", 8.36)
    for k in HEADS:
        on(r, ("pose", k, t, 0.15, {"pose": "walk"}), ("move", k, t, 0.8, (0, 90)),
           ("pose", k, round(t + 0.8, 2), 0.2, {"pose": "stand"}))
    t = cue(say, r, "tribes", 10.0)
    stds = sorted([f"std_{tr}" for tr in SH.LEFT + SH.RIGHT] + ["std_ManE"],
                  key=lambda k: c.actors[k].start["x"])
    for i, k in enumerate(stds):
        tt = round(t + 0.08 * i, 2)
        on(r, ("show", k, tt, 0.15, None), ("grow", k, tt, 0.6, None))
    t = cue(say, r, "distributed", 11.85)
    on(r, ("pose", "joshua", t, 0.3, {"arms": "open"}),
       ("pose", "eleazar", round(t + 0.25, 2), 0.3, {"arms": "open"}))

    # 14:2 by the lot: 18:10's move. The nine blank standards and then the half
    # glow once, and their numbers come in over the row
    r = (14, 2)
    on(r, ("hide", "canaan", 0.2, 0.5, None))
    lot = c.actors["lot0"].start
    hand = (SH.JOSHUA[0] - 20.6 * PXU, SH.JOSHUA[1] - 92 * PXU)
    t = cue(say, r, "lot", 0.29, lead=0.15)
    on(r, ("pose", "joshua", t, 0.3, {"arms": "hold_l"}),
       ("pose", "eleazar", t, 0.3, {"arms": "down"}),
       ("move", "lot0", round(t + 0.3, 2), 0.05,
        (hand[0] - lot["x"], hand[1] - lot["y"])),
       ("pose", "joshua", round(t + 0.6, 2), 0.4, {"arms": "up"}),
       ("show", "lot0", round(t + 0.9, 2), 0.3, None))
    t9 = cue(say, r, "nine", 4.38, lead=-0.05)
    for tr in NINE:
        on(r, ("pulse", f"std_{tr}", t9, 1.0, None))
    th = cue(say, r, "half-tribe", 5.69, lead=-0.05)
    on(r, ("pulse", "std_Manasseh", th, 0.8, None))
    nine = numeral("9", SKY_Y, SKY_NINE_X, SKY_PX)
    half = numeral("½", SKY_Y, SKY_HALF_X, SKY_PX)
    c.effect(r, f'<g opacity="0">{fade(t9, 0.4)}{nine}</g>'
                f'<g opacity="0">{fade(th, 0.4)}{half}</g>')

    # 14:3 they go as the camera leaves; once it is on the map, off screen, the
    # heads step back and the pebble goes
    r = (14, 3)
    c.effect(r, f'<g>{fade(0.0, 0.5, out=True)}{nine}{half}</g>')
    t = round(leg_end(r, 0) + 0.1, 2)
    for k in HEADS:
        on(r, ("move", k, t, 0.4, (0, -90)))
    on(r, ("pose", "joshua", t, 0.2, {"arms": "down"}),
       ("hide", "lot0", t, 0.2, None))

    # 14:4 Joseph is two: down over the bracket and back. No portion: open
    # hands. Except cities, and suburbs for their livestock and property
    r = (14, 4)
    on(r, ("label", "joseph", cue(say, r, "Joseph", 1.45, lead=-0.3), 0, "Joseph"))
    t = cue(say, r, "two", 1.68)
    eph, man = JOSEPH
    slide(c, r, eph + man, t, 0.7, 0, 38)
    on(r, ("label", "n_man", cue(say, r, "Manasseh", 2.44), 0, "Manasseh"),
       ("label", "n_eph", cue(say, r, "Ephraim", 3.42), 0, "Ephraim"))
    t_off = leg_end(r, 1)       # as the camera moves to the Levites
    on(r, ("hide", "joseph", t_off, 0.4, None), ("hide", "n_eph", t_off, 0.4, None),
       ("hide", "n_man", t_off, 0.4, None))
    slide(c, r, eph + man, t_off, 0.8, 0, -38)
    x0, y0, x1, y1 = BRACKET
    length = x1 - x0 + 2 * (y1 - y0)
    c.effect(r, f'<g>{fade(t_off, 0.4, out=True)}'
                f'<path d="M{x0} {y0} L{x0} {y1} L{x1} {y1} L{x1} {y0}" fill="none" '
                f'stroke="{rgb(TEXT)}" stroke-width="2.5" '
                f'stroke-dasharray="{length}" stroke-dashoffset="{length}">'
                f'<animate attributeName="stroke-dashoffset" '
                f'values="{length};0" begin="{t:.2f}s" dur="0.8s" fill="freeze"/>'
                f'</path></g>')
    t = cue(say, r, "no", 4.98)
    for i in range(len(LEVI_X)):
        on(r, ("pose", f"lev{i}", round(t + 0.05 * i, 2), 0.3, {"arms": "open"}))
    on(r, ("label", "n_lev", cue(say, r, "Levites", 5.9), 0, "Levites"))
    t = cue(say, r, "cities", 7.72)
    on(r, ("show", "city", t, 0.2, None), ("grow", "city", t, 0.9, None),
       ("show", "cityh0", round(t + 0.25, 2), 0.2, None),
       ("grow", "cityh0", round(t + 0.25, 2), 0.7, None),
       ("show", "cityh1", round(t + 0.45, 2), 0.2, None),
       ("grow", "cityh1", round(t + 0.45, 2), 0.7, None))
    for i in range(len(LEVI_X)):
        on(r, ("pose", f"lev{i}", round(t + 0.3, 2), 0.3, {"arms": "down"}))
    t = cue(say, r, "suburbs", 9.63, lead=0.25)
    for i, x in enumerate(SHEEP_X):
        tt = round(t + 0.25 * i, 2)
        on(r, ("show", f"sheep{i}", tt, 0.3, None),
           ("move", f"sheep{i}", tt, 1.6, (SHEEP_STOP[i] - x, 0)))
    t = cue(say, r, "livestock", 10.49, lead=0.2)
    on(r, ("show", "ox", t, 0.3, None), ("move", "ox", t, 1.7, (OX_STOP - OX_X, 0)))

    # 14:5 they go; at "divided" the leaders' arms go out across the twelve
    # (Eleazar is flipped, so his point_l points right)
    r = (14, 5)
    for k in ["city", "cityh0", "cityh1", "sheep0", "sheep1", "sheep2", "ox"]:
        on(r, ("hide", k, 0.2, 0.7, None))
    on(r, ("hide", "n_lev", 0.2, 0.5, None))
    t = cue(say, r, "divided", 3.79)
    on(r, ("pose", "joshua", t, 0.3, {"arms": "point_l"}),
       ("pose", "eleazar", t, 0.3, {"arms": "point_l"}))

    # 14:6 Judah comes near, and Caleb out of it: he stands under his name and
    # points at Joshua at "You"
    r = (14, 6)
    on(r, ("pose", "joshua", 0.3, 0.3, {"arms": "down"}),
       ("pose", "eleazar", 0.3, 0.3, {"arms": "down"}))
    on(r, ("label", "std_Judah", cue(say, r, "Judah", 0.97, lead=0.4), 0, "Judah"))
    t = cue(say, r, "came", 1.42, lead=0.3)
    walk(c, r, [f"Judah{j}" for j in range(4)] + ["caleb"], t, 1.1, 0, 24, face=1)
    on(r, ("move", "std_Judah", t, 1.1, (0, 24)))
    on(r, ("label", "gilgal", cue(say, r, "Gilgal", 2.91), 0, "Gilgal"))
    t = cue(say, r, "Caleb", 3.77)
    walk(c, r, ["caleb"], t, 1.2, 131, 16, face=1)
    on(r, ("ink", "caleb", t, 0.4, TEXT),
       ("label", "caleb", round(t + 0.05, 2), 0, "Caleb"))
    on(r, ("pose", "caleb", cue(say, r, "said", 6.06), 0.3, {"arms": "open"}))
    on(r, ("pose", "caleb", cue(say, r, "You", 7.19), 0.3, {"arms": "point_r"}))

    # 14:10 his arm comes down off screen; 85 comes in over the card's man as
    # the pin goes (cast: the crossing, by the camera's zoom)
    on((14, 10), ("pose", "caleb", 0.1, 0.2, {"arms": "down"}),
       ("mark", "caleb", MARK_IN, 0.4, numeral("85")))

    # 14:11 "as I was": his younger self walks in, his 40 coming in once he has
    # passed Judah's pole, and both raise their arms. At "war" he takes spear and
    # shield, and goes out and comes in
    r = (14, 11)
    t = cue(say, r, "as I was", 1.59)
    on(r, ("show", "young", t, 0.4, None), ("pose", "young", t, 0.15, {"pose": "walk"}),
       ("move", "young", t, 1.75, (160, 0)),
       ("pose", "young", round(t + 1.75, 2), 0.2, {"pose": "stand"}),
       ("mark", "young", round(t + 1.11, 2), 0.5, numeral("40", fill=TEXT)))
    on(r, ("pose", "young", cue(say, r, "my", 4.31, lead=0.05), 0.4, {"arms": "up"}))
    on(r, ("pose", "caleb", cue(say, r, "even", 5.9, lead=0.0), 0.4, {"arms": "up"}))
    on(r, ("hide", "young", cue(say, r, "now", 7.19), 0.5, None))
    on(r, ("pose", "caleb", cue(say, r, "war", 7.61, lead=0.15), 0.3,
           {"armed": True, "arms": "down"}))
    walk(c, r, ["caleb"], cue(say, r, "go", 8.34), 0.62, -90, 0, face=-1, end_face=-1)
    walk(c, r, ["caleb"], cue(say, r, "come", 9.17, lead=0.05), 0.62, 90, 0, face=1,
         end_face=1)


# ---------------------------------------------------------------------------
# The Hebron card: the hill, the Anakim and their wall
# ---------------------------------------------------------------------------

H_ANCHOR, H_SIZE, H_ORIGIN = (600, 1100), (4800, 2200), (-2400, 0)
PLAT = 1156                     # the hilltop the wall stands on
H_FAR = [(-2400, 900), (-1300, 840), (-300, 900), (600, 800), (1500, 860),
         (2400, 800)]
H_NEAR = [(-2400, 1420), (-1200, 1410), (-750, 1370), (-400, 1290), (-120, 1205),
          (120, 1160), (2400, 1150)]
ANAKIM_X = (505, 660, 830)


def build_heb(town_xy, say=None):
    """The Hebron card hung at the town's world point; `say` as build_gil's."""
    c = Card("heb", town_xy, H_ANCHOR, H_SIZE, S_CARD, page=EARTH, sky=SKY,
             ground_y=PLAT, origin=H_ORIGIN)
    c.names_at = (0.36, 0.44)
    c.cut_late = True
    c.share_bodies = True
    X0, X1 = H_ORIGIN[0], H_ORIGIN[0] + H_SIZE[0]

    # -- scenery: the far ridge, the near hill and its terraces ------------
    c.scenery.append('<polygon points="' + " ".join(
        f"{x},{y}" for x, y in H_FAR + [(X1, 1500), (X0, 1500)])
        + f'" fill="{rgb(FAR_HILL)}" stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    c.scenery.append('<polygon points="' + " ".join(
        f"{x},{y}" for x, y in H_NEAR + [(X1, 2200), (X0, 2200)])
        + f'" fill="{rgb(EARTH)}" stroke="{rgb(SAND)}" stroke-width="3"/>')
    for k in range(1, 5):
        pts = [(x, y + 44 * k) for x, y in H_NEAR]
        c.scenery.append('<polyline points="' + " ".join(f"{x},{y}" for x, y in pts)
                         + f'" fill="none" stroke="{rgb(SAND_DIM)}" stroke-width="2" '
                         f'stroke-dasharray="26 14" opacity="0.7"/>')

    # -- the city, raised at 14:12 -----------------------------------------
    for i, (x, y) in enumerate(((-480, 868), (-230, 884))):
        c.add(Actor(f"far{i}", GATE, x, y, h=MAN * 0.26, ink=SAND))
    c.add(Actor("wall_l", WALL, 300, PLAT, h=MAN, ink=SAND))
    c.add(Actor("wall_r", WALL, 1110, PLAT, h=MAN, ink=SAND))
    c.add(Actor("gate", GATE, 705, PLAT, h=MAN, ink=SAND))
    c.add(Actor("tower_l", TOWER, 80, PLAT, h=MAN, ink=SAND))
    c.add(Actor("tower_r", TOWER, 1330, PLAT, h=MAN, ink=SAND))
    for i, x in enumerate(ANAKIM_X):
        c.add(Actor(f"ana{i}", ANAK, x, PLAT + 14 + (i % 2) * 8,
                    h=MAN, ink=TEXT, flip=-1))
    c.add(Actor("anakim", static(list), 665, PLAT + 100, shown=True, label_y=0,
                label_fill=TEXT))
    c.add(Actor("caleb", armed_make, -560, 1352, h=MAN, ink=HL,
                pose={"armed": True, "pose": "walk"}, label_fill=HL, label_y=30))
    c.add(Actor("place", static(list), 705, 740, shown=True, label_y=0))
    c.add(Actor("oldname", static(list), 705, 785, shown=True, label_y=0,
                label_fill=TEXT, label_italic=True))
    c.refs = REFS
    heb_events(c, say)
    return c


def heb_events(c, say=None):
    on = c.on
    # 14:12 the Anakim, then the great and fortified cities as the camera draws
    # back. "It may be": he shows at the hill's foot, 85 over him, walks up and
    # stops short, and the giants do not move
    r = (14, 12)
    t = cue(say, r, "Anakim", 6.11)
    for i in range(len(ANAKIM_X)):
        on(r, ("show", f"ana{i}", round(t + 0.12 * i, 2), 0.5, None))
    on(r, ("label", "anakim", t, 0, "Anakim"))
    t = cue(say, r, "great", 7.58)
    for k in ("wall_l", "wall_r"):
        on(r, ("show", k, t, 0.15, None), ("grow", k, t, 0.9, None))
    t = cue(say, r, "fortified", 8.06, lead=0.2)
    for k, d in (("tower_l", 0.0), ("tower_r", 0.1), ("gate", 0.25)):
        on(r, ("show", k, round(t + d, 2), 0.15, None),
           ("grow", k, round(t + d, 2), 0.7, None))
    t = cue(say, r, "cities", 8.81)
    on(r, ("show", "far0", t, 0.15, None), ("grow", "far0", t, 0.5, None),
       ("show", "far1", round(t + 0.15, 2), 0.15, None),
       ("grow", "far1", round(t + 0.15, 2), 0.5, None))
    t = cue(say, r, "It", 9.72, lead=0.05)
    on(r, ("show", "caleb", t, 0.3, None), ("label", "caleb", t, 0, "Caleb"),
       ("mark", "caleb", t, 0.3, numeral("85")), ("move", "caleb", t, 2.3, (250, -66)))
    t = cue(say, r, "drive", 12.39, lead=0.25)
    on(r, ("move", "caleb", t, 0.8, (170, -74)),
       ("pose", "caleb", round(t + 0.8, 2), 0.2, {"pose": "stand"}))

    # 14:15 the old name, and the greatest man among them. "Then ... rest from
    # war": his spear and shield go as the camera begins to rise
    r = (14, 15)
    on(r, ("label", "place", cue(say, r, "Hebron", 0.6, lead=0.4), 0, "Hebron"),
       ("label", "oldname", cue(say, r, "Kiriath", 1.97), 0, "Kiriath Arba"))
    t = cue(say, r, "greatest", 3.62, lead=0.15)
    on(r, ("move", "ana1", t, 0.6, (0, 34)), ("scale", "ana1", t, 0.6, 1.12),
       ("ink", "ana0", t, 0.6, DIM), ("ink", "ana2", t, 0.6, DIM))
    on(r, ("pose", "caleb", cue(say, r, "Then", 5.76), 0.4, {"armed": False}))


# Camera shots inside the cards, (x, y, zoom), and each verse's legs. A leg's
# target is a shot here, "map" (the verse's own camera on the map, MAP_AT or the
# whole land) or a map camera (CAMERAS). The verses that aren't here (14:8,
# 14:13) stand still.
SHOTS = {
    "gil:leaders": (0, 1294, 0.72), "gil:twelve": (35, 1180, 0.4),
    "gil:jar": (-90, 1338, 1.0), "gil:joseph": (420, 1375, 0.8),
    "gil:levi": (240, 1332, 0.95), "gil:judah": (-230, 1318, 0.85),
    "gil:parley": (-160, 1353, 1.15), "gil:caleb85": (-170, 1353, 1.15),
    "gil:strong": (-215, 1338, 1.0),
    "heb:an": (690, 1000, 0.62), "heb:wide": (412, 1010, 0.5),
    "heb:name": (560, 1040, 0.66),
}
LEGS = {
    (14, 1): [("hold", None, 1.4), ("to", "gil:leaders", 3.4), ("hold", None, 2.5),
              ("to", "gil:twelve", 1.2)],
    (14, 2): [("to", "gil:jar", 1.3), ("hold", None, 1.2), ("to", "gil:twelve", 1.8)],
    (14, 3): [("to", "map", 2.3)],
    (14, 4): [("to", "gil:joseph", 2.4), ("hold", None, 2.0), ("to", "gil:levi", 1.4)],
    (14, 5): [("hold", None, 0.4), ("to", "gil:twelve", 4.0)],
    # it lands quick enough for Moses to rise in frame before "me"
    (14, 6): [("to", "gil:judah", 1.6), ("hold", None, 3.6), ("to", "gil:parley", 1.8),
              ("hold", None, 1.4), ("to", "map", 2.2)],
    # close on the men, then the land opens as he goes
    (14, 7): [("hold", None, 0.2), ("to", "kad_close", 1.8), ("hold", None, 1.9),
              ("to", "k_h", 1.3)],
    (14, 9): [("hold", None, 0.1), ("to", "kad_close", 1.7), ("hold", None, 0.4),
              ("to", "k_h", 1.1)],
    (14, 10): [("hold", None, 0.3), ("to", "stage", 2.3), ("hold", None, 8.6),
               ("to", "gil:caleb85", 2.4)],
    (14, 11): [("to", "gil:strong", 1.2)],
    # "give me this hill country" is the camera going to it
    (14, 12): [("hold", None, 0.7), ("to", "map", 1.9), ("hold", None, 1.3),
               ("to", "heb:an", 2.2), ("hold", None, 1.4), ("to", "heb:wide", 1.0),
               ("hold", None, 4.7), ("to", "map", 1.4)],
    (14, 14): [("hold", None, 0.2), ("to", "heb_close", 4.6), ("hold", None, 0.85),
               ("to", "k_h", 1.75)],
    (14, 15): [("to", "heb:name", 1.8), ("hold", None, 3.8), ("to", "map", 1.85)],
}


def leg_end(ref, i):
    """When a verse's leg i ends, seconds into the verse: what ends with a leg asks
    this, so it can't drift from the camera."""
    return round(sum(d for _k, _t, d in LEGS[ref][:i + 1]), 2)


# ---------------------------------------------------------------------------
# The map's places and cameras: every point is a gazetteer.py or allotment.py
# fact, and none of the walks' points is named on screen but where the text
# names it
# ---------------------------------------------------------------------------

def _site(key):
    s = GZ.SITES[key]
    return (s.lat, s.lon)


def _region(key):
    r = GZ.REGIONS[key]
    return (r.lat, r.lon)


KADESH, HEBRON, GILGAL = _site("kadesh_barnea"), _site("hebron"), _site("gilgal_jericho")
ZIN, SOUTH, HILL_COUNTRY = _region("zin"), _region("south"), _region("judah")
# what Caleb spied (Num 13:21-22): the text says only "the land"
WALK_UP = [KADESH, ZIN, SOUTH, HEBRON]
# the forty-five years, the long way round to Gilgal (Num 21 and 33, Deut 2):
# the heads of the Zered and the Arnon, and the Jordan at allotment's crossing.
# It ends at the card's Caleb's own point (caleb_on_card)
WALK_YEARS = [SOUTH, _region("arabah"), GZ.RIVERS["zered"][0], GZ.RIVERS["arnon"][0],
              _site("dibon"), _site("mount_nebo"), _site("shittim"),
              next(n.at for n in AL.VERSES[(14, 3)].names if n.web == "Jordan")]
# The map's cameras, for the tour's shot(): a place, the map's px a degree, and
# where the place falls on the screen.
CAMERAS = {
    "k_h": (*KADESH, 400, 460, 490),    # Kadesh low left, Hebron high right
    "kad_close": (*KADESH, 800, 560, 400),
    # all three, and room for Gilgal's name between the head of the Salt Sea and
    # the lots' discs
    "stage": (*HEBRON, 320, 500, 250),
    "gilm": (*GILGAL, 820, 637, 151),   # Gilgal high right, Hebron low left
    # zoom 0.055: any closer and Hebron's card would ghost in (CARD_IN)
    "heb_close": (*HEBRON, 1100, 512, 350),
}
MAP_AT = {(14, 6): "k_h", (14, 7): "k_h", (14, 8): "k_h", (14, 9): "k_h",
          (14, 12): "gilm", (14, 13): "gilm", (14, 14): "k_h"}
# The verses whose places the cast names itself, so the names persist across
# verses and nothing is drawn twice: the tour's layout (units) leaves them out.
NAMES_PLACES = {r for r in REFS if r >= (14, 6)}


class Tour(NamedTuple):
    """What the tour lends the cast: generate_joshua1319_svg imports this
    module, so not the other way round."""
    P: Callable                 # (lat, lon) to a world point
    PS: Callable                # a list of them
    shot: Callable              # (lat, lon, px a degree, screen x, y) to a camera
    say: Callable               # word_time: when the narration says a word
    wide: tuple                 # the whole land's camera
    key_layout: Callable        # the key's names, at the whole land
    lot_col: dict
    gil: Card
    plates: Callable            # hud_rects: (verse, camera) to the HUD's plates
    water: list                 # the coast, lakes and rivers, as world polylines
    discs: list                 # the lots' discs through the chapter, world points
                                # (the tour's build fills it)
    disc_r: float               # their radius, px


# ---------------------------------------------------------------------------
# The cast: what stands on the map, in screen px, feet at the pin's origin
# ---------------------------------------------------------------------------

PIN = 72                        # a man; so a child is 44 and the soldier with his spear 102
# Caleb's tag from his feet: his name's x and y, and his number's
TAG = (-44, -96, -38, -97)
ARMED_TAG = (-66, -110, -60, -111)      # over the spear, clear of its tip when he faces left
NAME_Y = -96                    # Joshua's at Gilgal, clear of the staff's tip (-82)
MOSES_DX, JOSHUA_DX = -136, -258        # from Kadesh's dot, where Caleb stands
# the Brook of Egypt ends over Moses' head, so at Kadesh the names are lower, and his
# (from him) stands to the left, over his staff's tip and under the brook's line
YOUNG_NAME_Y, MOSES_NAME = -84, (-42, -93)
MOSES_FLIP = -1                 # his staff on the far side, his free arm toward Caleb
# from Gilgal's dot: Caleb on Joshua's left, as on the card, so he walks away from
# him and his tag crosses nothing
GIL_JOSHUA_DX, GIL_CALEB_DX = -51, -146
GILGAL_NAME = (-20, 22)         # under the dot, clear of the Jordan and the sea's head
KADESH_NAME_XY, HEBRON_NAME_XY = (14, 22), (16, 20)     # right of and under their dots
DOT_R, PALE_R, DISC_R = 4.5, 3.5, 13    # a place's dot, gold and pale, and its soft disc
BAND_R = 2.7                    # a dot of the ten, or of the twelve
BLOCK_X, BLOCK_Y = -197, 56     # the people's bottom middle: under Moses and Joshua
CHILD_NEAR, CHILD_BY = 14, 30   # 14:9's two on the disc; 14:14's beside the man
NINE_XY, TWO_XY, HALF_XY = (292, 372), (874, 300), (914, 300)
SUM_PX = 56
FORTY_FIVE_XY = (842, 410)
# 14:3's 0, drawn (zero): its middle, px right of LEVI's box, its radii and its pen
ZERO_AIR, ZERO_R, ZERO_PEN = 17, (5, 7.5), 2.6
LINE_PX, LIT_PX = 2.8, 3.2      # the walked line drawing itself, and lit
UP_S, HOME_S = 1.5, 1.6         # 14:7: the walk up, and back
HOME_UP = 0.15                  # and his standing pin coming up under him at Kadesh
# 14:7: the ten leave after Joshua has passed the dot and reach Hebron with him
TEN_LAG, TEN_UP_S = 0.4, 1.15
# 14:7's rests at Hebron, px from its dot at K_H: Joshua beside Caleb, on the far side
# from his tag, and the ten at Joshua's feet (where band_dots hangs them), so the dot
# still shows
JOSHUA_UP_DX, TEN_AT = 44, (34, 26)
TEN_SHORT = 0.4                 # 14:8: how far along the first leg they stop, clear of him
ZIN_S = 1.4                     # 14:8 and 14:9: each leg as he follows wholly
TEN_S = 1.34                    # 14:8: the ten down the line
GIVEN_S = 2.03                  # 14:13: Gilgal to Hebron, from "gave" to before "inheritance"
LIGHT_S = 2.77                  # 14:14: the light up the line, to his feet
# 14:10: the part of the walk's time his tag is off, down the old line and past the
# Salt Sea, the rivers and the lots' discs, all of which it would cross. His 40 goes
# as the 45 comes in, and his name comes back alone, for the 85
TAG_PAST = (0.10, 0.80)
# hand-set against the camera: when a thing can first be seen, or must have gone
MOSES_IN = 10.25                # 14:6: Moses' rising figure comes into frame
HEBRON_IN = 4.7                 # 14:7: the pull-back brings Hebron's dot into frame
NINE_IN = 2.05                  # 14:3: as the camera lands on the whole land
HILL_IN = 2.2                   # 14:12: over the map, as the camera comes onto it
HILL_OUT = leg_end((14, 12), 2)  # until it leaves
HILL_BACK = round(leg_end((14, 12), 6) + 0.8, 2)   # and again as it comes back
KADESH_NAME_IN = 7.0            # 14:14: the draw-back brings Kadesh into frame
JOSHUA_OFF = 0.1                # 14:10: Joshua goes first, on his own and not with the
                                # people, whom Num 14:30 and 14:38 say he outlived
NAMES_OFF = 0.6                 # then Moses' name and the mound, gone by 1.1 as the
                                # flight brings Joshua's old place to the inset's edge
                                # (Moses follows at "alive")
# 14:10's crossing from the pin to the card's man, who stands on the same point. Zoom
# is 0.29 at 12.7 and 0.58 at 13.0, when the pin has gone; the card's man comes to the
# pin's size just after, at 13.06
DIVE = leg_end((14, 10), 2)     # the camera leaves the map
GILGAL_OFF = 12.2               # before the card can show Gilgal's dot
GILGAL_NAME_OFF = 11.95         # and its name before his feet and the line, which the
                                # dive slides below the dot, come down on it
TAG_OFF, PIN_OFF, MARK_IN = 12.6, 12.7, 12.9


def fig(parts, col=TEXT, flip=1):
    return figure_svg(parts, PIN, col, LAND, flip)


def txt(x, y, s, px=18, fill=TEXT, bold=True, italic=False, anchor="middle"):
    """A name or number on the map, with the BG halo: its own <text>, its
    baseline on itself, since WebKit carries none into a tspan."""
    a = (f'font-size="{px}" fill="{rgb(fill)}" text-anchor="{anchor}" '
         f'dominant-baseline="central"')
    if bold:
        a += ' font-weight="bold"'
    if italic:
        a += ' font-style="italic"'
    return (f'<text x="{_fmt(x)}" y="{_fmt(y)}" {a} stroke="{rgb(BG)}" '
            f'stroke-width="4" stroke-opacity="0.85" stroke-linejoin="round" '
            f'paint-order="stroke">{s}</text>')


def fade_in(inner, t, d=0.5):
    return f'<g opacity="0">{fade(t, d)}{inner}</g>'


def fade_out(inner, t, d=0.5):
    return f'<g>{fade(t, d, out=True)}{inner}</g>'


def swap(a, b, t, d=0.3):
    """One look cross-fading to another."""
    return fade_out(a, t, d) + fade_in(b, t, d)


def arm_up(hanging, raised, t, d=0.3):
    """An arm going up as a man stands: the raised figure fades in over the hanging
    one, which goes in the fade's second half, so he hardly dims and nothing snaps."""
    half = round(d / 2, 2)
    return fade_out(hanging, round(t + half, 2), half) + fade_in(raised, t, d)


def arm_down(raised, hanging, t, d=0.3):
    """And coming down: the hanging figure comes up in the fade's first half, under
    the raised one."""
    return fade_in(hanging, t, round(d / 2, 2)) + fade_out(raised, t, d)


def away_for(inner, t_off, off_d, t_back, back_d):
    """It goes at t_off and comes back at t_back."""
    return f'<g>{fade(t_off, off_d, out=True)}{fade(t_back, back_d)}{inner}</g>'


def at_x(dx, inner):
    return f'<g transform="translate({dx} 0)">{inner}</g>'


def dot(col=HL, r=DOT_R):
    return f'<circle r="{r}" fill="{rgb(col)}"/>'


def pale_dot():
    return dot(TEXT, PALE_R)


def disc(col, op):
    """A soft mark at a place: a <circle>, since a round cap on a path of no
    length paints twice on WebKit."""
    return f'<circle r="{DISC_R}" fill="{rgb(col)}" fill-opacity="{op}"/>'


def tag_name(armed=False):
    """Caleb's tag stands left of him, so no line touches it."""
    x, y = (ARMED_TAG if armed else TAG)[:2]
    return txt(x, y, "Caleb", 18, HL, anchor="end")


def tag_num(age, armed=False):
    x, y = (ARMED_TAG if armed else TAG)[2:]
    return txt(x, y, str(age), 30, HL, anchor="start")


def caleb(parts, age, armed=False, flip=1):
    """The gold man, the only one, with his name and his years."""
    return fig(parts, HL, flip) + tag_name(armed) + tag_num(age, armed)


def child(dx):
    """One of his children, in the people's ink: he is the only gold figure."""
    return at_x(dx, fig(F.child(), TEXT))


def staffed(arms="down"):
    """A man with a staff, his free arm acting: Moses at Kadesh, Joshua at Gilgal."""
    return F.man(staff=True, arms=arms)


def moses_fig(arms="down"):
    """Moses, flipped (MOSES_FLIP): point_l and up reach to the right of the screen,
    toward Caleb."""
    return fig(staffed(arms), TEXT, MOSES_FLIP)


def moses_name():
    return txt(*MOSES_NAME, "Moses")


def moses(arms="down"):
    return at_x(MOSES_DX, moses_fig(arms) + moses_name())


def moses_to(a, b, t, d=0.3):
    """Moses' arm going up or coming down as his name stays."""
    arm = (arm_down if b == "down" else arm_up)(moses_fig(a), moses_fig(b), t, d)
    return at_x(MOSES_DX, arm + moses_name())


def young_joshua_name():
    return txt(0, YOUNG_NAME_Y, "Joshua", 16, TEXT)


def young_joshua():
    return at_x(JOSHUA_DX, fig(F.man(), YOUNG) + young_joshua_name())


def ten():
    """The ten who went up with him."""
    return band_dots(10, cols=5, step=8, r=BAND_R)


def kadesh_name():
    return txt(*KADESH_NAME_XY, "Kadesh Barnea", 18, HL, anchor="start")


def kadesh_mark():
    return dot() + kadesh_name()


def kadesh_name_pale():
    return txt(*KADESH_NAME_XY, "Kadesh Barnea", 16, TEXT, anchor="start")


def kadesh_pale():
    return pale_dot() + kadesh_name_pale()


def kadesh_name_paling(t, d):
    """The gold name becoming the pale one: one <text>, its ink and size animated,
    so the letters neither ghost nor blink."""
    return txt(*KADESH_NAME_XY, "Kadesh Barnea"
               f'<animate attributeName="fill" values="{rgb(HL)};{rgb(TEXT)}" '
               f'begin="{t}s" dur="{d}s" fill="freeze"/>'
               f'<animate attributeName="font-size" values="18;16" '
               f'begin="{t}s" dur="{d}s" fill="freeze"/>',
               18, HL, anchor="start")


def gilgal_name():
    return txt(*GILGAL_NAME, "Gilgal", 18, HL)


def gilgal_mark():
    return dot() + gilgal_name()


def joshua_at_gilgal(arms="down"):
    return fig(staffed(arms), TEXT)


def joshua_name_at_gilgal():
    return txt(0, NAME_Y, "Joshua")


def hebron_mark():
    return dot() + txt(*HEBRON_NAME_XY, "Hebron", 18, HL, anchor="start")


def hebron_promised():
    """14:9: "the land where you walked", before it has a name."""
    return disc(HL, 0.32)


def hebron_given(tour):
    return disc(tour.lot_col["JUDAH"], 0.55)


def forty_five():
    return txt(*FORTY_FIVE_XY, "45", SUM_PX, HL)


def dashed(fl, pts, col=HL, px=2.6, op=1.0):
    """The old line, its dashes held at a screen size."""
    return emit_class(fl, px, [poly_el(pts, stroke=col)],
                      f' stroke-linecap="butt" stroke-opacity="{op}"', (9, 5))


def solid(fl, pts, px=LINE_PX):
    return emit_class(fl, px, [poly_el(pts, stroke=HL)], ' stroke-linecap="round"')


def traced(fl, pts, t, d, px=LINE_PX):
    """A line drawing itself on the rider's easing, the man at its head."""
    return emit_class(fl, px, [traced_el(pts, HL, t, d)[0]], ' stroke-linecap="round"')


BAND = ' stroke-linecap="round" stroke-opacity="0.26"'    # the light under the line


def band(fl, pts):
    return emit_class(fl, 7.0, [poly_el(pts, stroke=HL)], BAND)


def band_traced(fl, pts, t, d):
    return emit_class(fl, 7.0, [traced_el(pts, HL, t, d)[0]], BAND)


def walk_leg(fl, path, t, d, stands, walks, ends, turn=None, tag=""):
    """A man who stands at a path's start until t, walks it over d, and stands
    at its end: his standing pin comes up under the rider, which goes when it is
    up, so he doesn't dip. `turn`: he walks the other way than he stands, so at both
    ends the figure is a soft cross-fade of that length, and `tag`, which doesn't
    turn, walks as a man does, staying bright."""
    t_end = round(t + d, 2)
    if turn:
        return (pin(fl, path[0], fade_out(stands, t, turn))
                + pin(fl, path[-1], fade_in(ends, t_end, turn))
                + rider(fl, path, t, d, walks, t_hide=t_end, hide_d=turn, show_d=turn)
                + walk_leg(fl, path, t, d, tag, tag, tag))
    return (pin(fl, path[0], fade_out(stands, t, 0.1))
            + pin(fl, path[-1], fade_in(ends, t_end, 0.05))
            + rider(fl, path, t, d, walks, t_hide=round(t_end + 0.05, 2), hide_d=0.05))


# The people of 14:8-10: forty dots in a block, 8 x 5, which slump to a mound
# on the same bottom line, each dot 0.012 s after the last
def block_pts():
    out = []
    for i in range(40):
        row, c = divmod(i, 8)
        out.append((BLOCK_X + (c - 3.5) * 9.0, BLOCK_Y - row * 9.0))
    return out


def mound_pts():
    out = []
    for row, n in enumerate((16, 12, 8, 4)):
        for i in range(n):
            out.append((BLOCK_X + (i - (n - 1) / 2) * 8.2, BLOCK_Y - row * 6.2))
    return out


def people_mound():
    return "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.9" fill="{rgb(SAND)}"/>'
                   for x, y in mound_pts())


def people_melting(t_in, t_melt):
    """The block coming in row by row from t_in and slumping from t_melt, the
    lowest dots to the mound's lowest row."""
    blk, mnd = block_pts(), mound_pts()
    order = sorted(range(40), key=lambda i: blk[i][1], reverse=True)
    out = []
    for rank, i in enumerate(order):
        (bx, by), (mx, my) = blk[i], mnd[rank]
        t = round(t_melt + 0.012 * rank, 2)
        eased = (f'begin="{t:.2f}s" dur="0.8s" fill="freeze" calcMode="spline" '
                 f'keyTimes="0;1" keySplines="{EASE}"')
        plain = f'begin="{t:.2f}s" dur="0.8s" fill="freeze"'
        out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="3" fill="{rgb(TEXT)}" '
                   f'opacity="0">{fade(round(t_in + 0.12 * (rank // 8), 2), 0.3)}'
                   f'<animate attributeName="cx" values="{bx:.1f};{mx:.1f}" {eased}/>'
                   f'<animate attributeName="cy" values="{by:.1f};{my:.1f}" {eased}/>'
                   f'<animate attributeName="r" values="3;2.9" {plain}/>'
                   f'<animate attributeName="fill" values="{rgb(TEXT)};{rgb(SAND)}" '
                   f'{plain}/></circle>')
    return "".join(out)


def beside(tour, place, cam, dx, dy=0):
    """A world point dx, dy px from a place at the camera that shows it: a man's
    own place in a group, for a walk to start or end at."""
    x, y = tour.P(*place)
    s = tour.shot(*CAMERAS[cam])[0]
    return (x + dx / s, y + dy / s)


def caleb_at_gilgal(tour):
    """Where he stands at Gilgal on the map, a world point: his place in the
    Gilgal group at the camera that shows it."""
    return beside(tour, GILGAL, "gilm", GIL_CALEB_DX)


def joshua_up(tour):
    """14:7: Joshua's walk, from his own place to Caleb's side at Hebron."""
    up = tour.PS(WALK_UP)
    return [beside(tour, KADESH, "k_h", JOSHUA_DX), up[1], up[2],
            beside(tour, HEBRON, "k_h", JOSHUA_UP_DX)]


def ten_at(tour):
    """Where the ten stand from 14:7 to 14:8's "brothers", a world point."""
    return beside(tour, HEBRON, "k_h", *TEN_AT)


def ten_up(tour):
    """14:7: the ten up the line, from Kadesh's dot to their place at Hebron."""
    return tour.PS(WALK_UP)[:3] + [ten_at(tour)]


def ten_down(tour):
    """14:8: and back down it, to stop short of him."""
    up = tour.PS(WALK_UP)
    return [ten_at(tour), up[2], up[1], (up[1][0] * TEN_SHORT + up[0][0] * (1 - TEN_SHORT),
                                         up[1][1] * TEN_SHORT + up[0][1] * (1 - TEN_SHORT))]


def caleb_on_card(tour):
    """The card's Caleb's own world point, where the forty-five years end, so
    the pin stands on the card's man through the dive."""
    s = tour.gil.state_at((14, 10))["caleb"]
    return tour.gil.world((s["x"], s["y"]))


def zero_at(tour):
    levi = tour.key_layout()["LEVI"]
    return levi["box"][2] + ZERO_AIR, levi["at"][1]


def zero(tour):
    """LEVI's 0, drawn: the font's old-style zero is x-height, which beside the
    key's capitals reads as a letter. It stands a little taller than they do."""
    x, y = zero_at(tour)
    a = (f'cx="{_fmt(x)}" cy="{_fmt(y)}" rx="{ZERO_R[0]}" ry="{ZERO_R[1]}" fill="none"')
    return (f'<ellipse {a} stroke="{rgb(BG)}" stroke-width="{ZERO_PEN + 4}" '
            f'stroke-opacity="0.85"/>'
            f'<ellipse {a} stroke="{rgb(HL)}" stroke-width="{ZERO_PEN}"/>')


def sum_els(tour):
    """14:3's numerals, in the order they come in."""
    return [txt(*NINE_XY, "9½", SUM_PX, HL), txt(*TWO_XY, "2", SUM_PX, HL),
            txt(*HALF_XY, "½", SUM_PX, HL), zero(tour)]


# ---------------------------------------------------------------------------
# The walks' clock: the verses keep it and _clock_qc asks it
# ---------------------------------------------------------------------------

def _up_times(say):
    """14:7: when he goes, how long the walk up takes, and when he turns. The walk
    is over before he turns, however the words fall."""
    cv = (14, 7)
    t_go = cue(say, cv, "to spy", 5.14, lead=0.05)
    t_back = cue(say, cv, "brought", 6.78, lead=0.05)
    return t_go, min(UP_S, round(t_back - t_go - 0.05, 2)), t_back


def _wholly(say, cv):
    """14:8 and 14:9: when he walks on."""
    return cue(say, cv, "wholly", {(14, 8): 4.99, (14, 9): 8.75}[cv], lead=0.0)


def _years_times(say):
    """14:10: when he sets out, when he reaches Gilgal, and when 85 comes in."""
    cv = (14, 10)
    return (cue(say, cv, "these", 4.34, lead=0.0),
            cue(say, cv, "Now, behold, I", 11.05, lead=0.0),    # the second "Now"
            cue(say, cv, "eighty-five", 12.28, lead=0.0))


def _given_times(say):
    """14:13: when he sets out for Hebron, and when its ring goes out."""
    cv = (14, 13)
    return cue(say, cv, "gave", 1.87, lead=0.12), cue(say, cv, "inheritance", 4.31)


# ---------------------------------------------------------------------------
# Verse by verse: each -> (in the map's group, over the cards under the camera,
# over everything in screen space)
# ---------------------------------------------------------------------------

def _sum(cv, fl, tour):
    """14:3: the sum, the tour's one frame of it."""
    say = tour.say
    times = (NINE_IN, cue(say, cv, "two", 2.46, lead=0.05),
             cue(say, cv, "half-tribe", 3.46, lead=0.05),
             cue(say, cv, "inheritance among", 6.9, lead=0.05))
    return [], [], [fade_in(el, t, 0.4) for t, el in zip(times, sum_els(tour))]


def _sum_goes(cv, fl, tour):
    """14:4: they go with the dive."""
    return [], [], [fade_out("".join(sum_els(tour)), 0.0, 0.4)]


def _at_kadesh(cv, fl, tour):
    """14:6: the three at Kadesh, as he names them."""
    say = tour.say
    men = (fade_in(kadesh_mark(), cue(say, cv, "Kadesh", 12.48))
           + lift_in(moses(), max(cue(say, cv, "Moses", 9.36), MOSES_IN))
           + lift_in(fig(F.man(), HL) + tag_name(), cue(say, cv, "me", 10.97, lead=0.25))
           + lift_in(young_joshua(), cue(say, cv, "you", 12.04, lead=0.2)))
    return [], [pin(fl, tour.P(*KADESH), men)], []


def _spies(cv, fl, tour):
    """14:7: up the line to the dot and back, Joshua with him; the ten go up
    behind them and stay at the dot. The men's standing pins come up under them
    at home, and Joshua's name goes as he leaves and comes back with him."""
    say = tour.say
    kadesh, up, path = tour.P(*KADESH), tour.PS(WALK_UP), joshua_up(tour)
    t_40 = cue(say, cv, "forty", 0.36)
    t_go, up_s, t_back = _up_times(say)
    t_home = round(t_back + HOME_S, 2)
    # his arms open at "heart", and not before the rider has gone
    t_open = max(cue(say, cv, "heart", 8.5), round(t_home + HOME_UP + 0.05, 2))
    stand = fig(F.man(), HL)
    return [traced(fl, up, t_go, up_s)], [
        pin(fl, tour.P(*HEBRON), fade_in(pale_dot(), HEBRON_IN, 0.4)),
        pin(fl, kadesh, at_x(JOSHUA_DX, away_for(fig(F.man(), YOUNG), t_go, 0.1, t_home, HOME_UP)
                             + away_for(young_joshua_name(), t_go, 0.3, t_home, 0.4))),
        rider(fl, path, t_go, up_s, fig(F.man(pose="walk"), YOUNG),
              t_hide=t_back, hide_d=0.05),
        rider(fl, path[::-1], t_back, HOME_S, fig(F.man(pose="walk"), YOUNG, -1),
              t_hide=round(t_home + HOME_UP, 2), hide_d=0.05),
        rider(fl, ten_up(tour), round(t_go + TEN_LAG, 2), TEN_UP_S, ten(), show_d=0.3),
        pin(fl, kadesh, kadesh_mark() + moses_to("down", "point_l", cue(say, cv, "sent", 3.41))),
        pin(fl, kadesh, fade_out(stand + tag_name() + fade_in(tag_num(40), t_40, 0.4),
                                 t_go, 0.1)),
        pin(fl, kadesh, fade_in(arm_up(stand, fig(F.man(arms="open"), HL), t_open)
                                + tag_name() + tag_num(40), t_home, HOME_UP)),
        rider(fl, up, t_go, up_s, caleb(F.man(pose="walk"), 40),
              t_hide=t_back, hide_d=0.05),
        rider(fl, up[::-1], t_back, HOME_S, caleb(F.man(pose="walk"), 40, flip=-1),
              t_hide=round(t_home + HOME_UP, 2), hide_d=0.05),
    ], []


def _melt(cv, fl, tour):
    """14:8: the ten bring back their word, the people melt, he goes on."""
    say = tour.say
    kadesh, up = tour.P(*KADESH), tour.PS(WALK_UP)
    t_ten = cue(say, cv, "brothers", 1.16)
    t_wholly = _wholly(say, cv)
    arms_down = 0.3             # what 14:7 left raised comes down as he speaks
    return [fade_out(solid(fl, up), 0.0, 0.8), dashed(fl, up, op=0.6)], [
        pin(fl, tour.P(*HEBRON), pale_dot()),
        pin(fl, kadesh, kadesh_mark() + young_joshua()
            + moses_to("point_l", "down", arms_down)),
        # the ten stand at Hebron as 14:7 left them, then come down
        pin(fl, ten_at(tour), fade_out(ten(), t_ten, 0.05)),
        rider(fl, ten_down(tour), t_ten, TEN_S, ten(),
              t_hide=round(t_ten + TEN_S, 2), hide_d=0.3),
        pin(fl, kadesh, people_melting(cue(say, cv, "made", 2.63, lead=0.05),
                                       cue(say, cv, "melt", 3.99))),
        walk_leg(fl, up[:2], t_wholly, ZIN_S,
                 arm_down(fig(F.man(arms="open"), HL), fig(F.man(), HL), arms_down)
                 + tag_name() + tag_num(40),
                 caleb(F.man(pose="walk"), 40), caleb(F.man(), 40)),
    ], []


def _swore(cv, fl, tour):
    """14:9: the line lights at "land", the disc and the children come up on
    what he walked, and he goes on."""
    say = tour.say
    kadesh, hebron, up = tour.P(*KADESH), tour.P(*HEBRON), tour.PS(WALK_UP)
    t_land = cue(say, cv, "land", 3.27, lead=0.05)
    t_kids = cue(say, cv, "children", 6.45)
    t_wholly = _wholly(say, cv)
    return [dashed(fl, up, op=0.6), band_traced(fl, up, t_land, 1.2),
            fade_in(dashed(fl, up, px=LIT_PX), t_land, 1.2)], [
        pin(fl, hebron, fade_in(hebron_promised(), cue(say, cv, "inheritance", 4.9))),
        pin(fl, hebron, pale_dot()),
        pin(fl, hebron, lift_in(child(-CHILD_NEAR), t_kids)
            + lift_in(child(CHILD_NEAR), round(t_kids + 0.15, 2))),
        pin(fl, kadesh, kadesh_mark() + young_joshua()
            + moses_to("down", "up", cue(say, cv, "swore", 0.45)) + people_mound()),
        walk_leg(fl, up[1:3], t_wholly, ZIN_S, caleb(F.man(), 40),
                 caleb(F.man(pose="walk"), 40), caleb(F.man(), 40)),
    ], []


def _years(cv, fl, tour):
    """14:10: alone on the land, forty-five years the long way round, and the
    crossing into the card."""
    say = tour.say
    kadesh, hebron, gilgal = tour.P(*KADESH), tour.P(*HEBRON), tour.P(*GILGAL)
    up = tour.PS(WALK_UP)
    t_alive = cue(say, cv, "alive", 2.59, lead=0.05)
    t_walk, t_now, t_85 = _years_times(say)
    d = round(t_now - t_walk, 2)
    at_card = caleb_on_card(tour)
    path = tour.PS(WALK_YEARS) + [at_card]
    t_off, t_back = (round(t_walk + f * d, 2) for f in TAG_PAST)
    walker = (fig(F.man(pose="walk"), HL) + fade_out(tag_num(40), t_off, 0.3)
              + away_for(tag_name(), t_off, 0.3, t_back, 0.3))
    return [dashed(fl, up, SAND, px=2.0, op=0.8),
            fade_out(band(fl, up) + dashed(fl, up, px=LIT_PX), 0.0, 0.8),
            traced(fl, path, t_walk, d)], [
        pin(fl, hebron, fade_out(hebron_promised() + child(-CHILD_NEAR) + child(CHILD_NEAR),
                                 t_alive, 0.7) + pale_dot()),
        pin(fl, kadesh, fade_out(at_x(MOSES_DX, moses_fig("up")), t_alive, 0.7)
            + fade_out(young_joshua(), JOSHUA_OFF, 0.4)
            + fade_out(at_x(MOSES_DX, moses_name()) + people_mound(), NAMES_OFF, 0.5)
            + swap(dot(), pale_dot(), 0.0, 0.8) + kadesh_name_paling(0.0, 0.8)),
        pin(fl, tour.P(*SOUTH), fade_out(caleb(F.man(), 40), t_walk, 0.1)),
        pin(fl, at_card, fade_in(
            fade_out(fig(F.man(), HL), PIN_OFF, 0.3)
            + fade_out(tag_name() + fade_in(tag_num(85), t_85, 0.25),
                       TAG_OFF, 0.25), t_now, 0.1)),
        rider(fl, path, t_walk, d, walker, t_hide=round(t_now + 0.1, 2), hide_d=0.05),
        rider(fl, path, t_walk, d, at_x(-34, band_dots(12, step=8, r=BAND_R)),
              t_show=cue(say, cv, "Israel", 9.02, lead=0.05), t_hide=t_now, hide_d=0.3,
              show_d=0.3),
        pin(fl, gilgal, fade_in(fade_out(dot(), GILGAL_OFF, 0.35)
                                + fade_out(gilgal_name(), GILGAL_NAME_OFF, 0.35), t_now, 0.4)),
    ], [fade_out(fade_in(forty_five(), cue(say, cv, "forty-five", 4.62, lead=0.05), 0.4),
                 DIVE, 0.4)]


def _hill_country(cv, fl, tour):
    """14:12: "this hill country" is the map, in the first flight's window; and
    the camera comes back to it at the end."""
    say = tour.say
    up = tour.PS(WALK_UP)

    def seen(el):
        return (fade_in(fade_out(el, HILL_OUT, 0.35), HILL_IN, 0.35)
                + fade_in(el, HILL_BACK, 0.45))
    t_hill = max(cue(say, cv, "hill", 1.43), HILL_IN)
    hill = txt(0, 0, "Hill country", 20, TEXT, bold=False, italic=True)
    return [dashed(fl, up, op=0.7)], [
        pin(fl, tour.P(*HILL_COUNTRY), fade_in(fade_out(hill, HILL_OUT, 0.35), t_hill, 0.4)),
        pin(fl, tour.P(*HEBRON), seen(pale_dot())),
        pin(fl, tour.P(*GILGAL), seen(
            gilgal_mark()
            + at_x(GIL_JOSHUA_DX, joshua_at_gilgal() + joshua_name_at_gilgal()))),
        pin(fl, caleb_at_gilgal(tour), seen(caleb(F.soldier(), 85, armed=True))),
    ], []


def _given(cv, fl, tour):
    """14:13: blessed, and given: the straight walk to Hebron. Its line fades as
    he arrives, so at rest there is only the old one, which reaches his feet at
    14:14. He faces right at rest, and turns at each end of the walk."""
    say = tour.say
    hebron, gilgal = tour.P(*HEBRON), tour.P(*GILGAL)
    start = caleb_at_gilgal(tour)
    t_gave, t_ring = _given_times(say)
    t_named = cue(say, cv, "Hebron", 2.14)
    armed = fig(F.soldier(), HL)
    return [dashed(fl, tour.PS(WALK_UP), op=0.7),
            fade_out(traced(fl, [start, hebron], t_gave, GIVEN_S),
                     round(t_gave + GIVEN_S, 2), 0.8)], [
        pin(fl, hebron, fade_in(hebron_given(tour), t_named)),
        pin(fl, hebron, pale_dot() + fade_in(hebron_mark(), t_named)),
        pin(fl, gilgal, gilgal_mark() + at_x(GIL_JOSHUA_DX, arm_up(
            joshua_at_gilgal(), joshua_at_gilgal("up"), cue(say, cv, "blessed", 0.46))
            + joshua_name_at_gilgal())),
        walk_leg(fl, [start, hebron], t_gave, GIVEN_S, armed,
                 fig(F.soldier(pose="walk"), HL, -1), armed, turn=0.12,
                 tag=tag_name(armed=True) + tag_num(85, armed=True)),
    ], [screen_ring(to_screen(tour.shot(*CAMERAS["gilm"]), hebron), t_ring, 14, 46, 1.0, HL)]


def _because(cv, fl, tour):
    """14:14: the payoff. The children beside him, and the light up the line."""
    say = tour.say
    hebron, gilgal, up = tour.P(*HEBRON), tour.P(*GILGAL), tour.PS(WALK_UP)
    t_day = cue(say, cv, "to this day", 4.71)
    t_light = cue(say, cv, "followed", 6.13)
    return [dashed(fl, up, op=0.7),
            band_traced(fl, up, t_light, LIGHT_S),
            traced(fl, up, t_light, LIGHT_S, px=LIT_PX)], [
        pin(fl, gilgal, fade_out(gilgal_mark() + at_x(
            GIL_JOSHUA_DX, joshua_at_gilgal("up") + joshua_name_at_gilgal()),
            leg_end(cv, 0), 0.8)),
        pin(fl, hebron, hebron_given(tour)),
        pin(fl, tour.P(*KADESH), pale_dot()
            + fade_in(kadesh_name_pale(), KADESH_NAME_IN, 0.5)),
        pin(fl, hebron, hebron_mark() + caleb(F.soldier(), 85, armed=True)
            + lift_in(child(-CHILD_BY), t_day)
            + lift_in(child(CHILD_BY), round(t_day + 0.15, 2))),
    ], []


def _rest(cv, fl, tour):
    """14:15: the line, the marks and the man go as the dive begins."""
    up = tour.PS(WALK_UP)
    lit = dashed(fl, up, op=0.7) + band(fl, up) + solid(fl, up, LIT_PX)
    return [fade_out(lit, 0.0, 0.5)], [
        fade_out(pin(fl, tour.P(*HEBRON), hebron_given(tour) + hebron_mark()
                     + caleb(F.soldier(), 85, armed=True)
                     + child(-CHILD_BY) + child(CHILD_BY)), 0.0, 0.55),
        fade_out(pin(fl, tour.P(*KADESH), kadesh_pale()), 0.0, 0.5),
    ], []


VERSES = {(14, 3): _sum, (14, 4): _sum_goes, (14, 6): _at_kadesh, (14, 7): _spies,
          (14, 8): _melt, (14, 9): _swore, (14, 10): _years, (14, 12): _hill_country,
          (14, 13): _given, (14, 14): _because, (14, 15): _rest}


def held_goes(cv, tour):
    """14:10: the names held from the last verse that he would walk across go
    as he sets out, for the tour's held_labels."""
    if cv != (14, 10):
        return None
    return {"salt": fade(_years_times(tour.say)[0], 0.7, out=True)}


def cast(cv, fl, tour):
    """A verse's cast on the map, as three strings: what is drawn in the map's
    group; the pins, under the camera after the cards, so they stand over a
    card during a dive; and the overlay, in screen space."""
    if cv not in VERSES:
        return "", "", ""
    world, pins, overlay = VERSES[cv](cv, fl, tour)
    return "".join(world), "".join(pins), "".join(overlay)


_TIMED = re.compile(r'<(?:animate|animateTransform|animateMotion|set)\b[^>]*>')


def last_end(svg):
    """When the last of a piece of SVG's animations ends, for the tour's
    report (seconds)."""
    ends = [0.0]
    for tag in _TIMED.findall(svg):
        begin = re.search(r'begin="([\d.]+)s"', tag)
        dur = re.search(r'dur="([\d.]+)s"', tag)
        ends.append(float(begin[1]) + (float(dur[1]) if dur else 0.0))
    return max(ends)


# ---------------------------------------------------------------------------
# What stands at each rest on the map: the tour's layout keeps the water names
# off it, and cast_qc checks it
# ---------------------------------------------------------------------------

_TEXT = re.compile(r'<text ([^>]*)>([^<]+)')
_CIRCLE = re.compile(r'<circle ([^>]*?)/?>')
_ATTR = re.compile(r'([\w-]+)="([^"]*)"')
_ANCHOR = {"start": "l", "middle": "m", "end": "r"}


def drawn_texts(svg):
    """Each <text> in a piece of SVG, as it is drawn: (words, x, y, px, bold, anchor
    as `ink` takes it)."""
    out = []
    for attrs, words in _TEXT.findall(svg):
        a = dict(_ATTR.findall(attrs))
        out.append((words, float(a["x"]), float(a["y"]), int(a["font-size"]),
                    a.get("font-weight") == "bold", _ANCHOR[a["text-anchor"]]))
    return out


def drawn_circles(svg):
    """Each <circle> in a piece of SVG, as it is drawn: (cx, cy, r)."""
    out = []
    for attrs in _CIRCLE.findall(svg):
        a = dict(_ATTR.findall(attrs))
        out.append((float(a.get("cx", 0)), float(a.get("cy", 0)), float(a["r"])))
    return out


class _Standing:
    """A rest's cast in screen px at its camera, as the helpers draw it: names and
    numbers [(text, ink box)], figures and marks {what: ink points}, and lines."""

    def __init__(self, cam, tour):
        self.cam, self.tour = cam, tour
        self.names, self.figs, self.lines = [], {}, []

    def at(self, place):
        return to_screen(self.cam, self.tour.P(*place))

    def name(self, at, x, y, text, px=18, anchor="m", bold=True):
        b = ink(text, px, bold, False, anchor + "m")
        self.names.append((text, (at[0] + x + b[0], at[1] + y + b[1],
                                  at[0] + x + b[2], at[1] + y + b[3])))

    def fig(self, what, at, parts, dx=0, flip=1):
        self.figs[what] = ink_points(parts, at[0] + dx, at[1], PIN / MAN_H, flip)[0]

    def mark(self, what, at, r):
        self.figs[what] = [(at[0] + r * math.cos(i * math.pi / 8),
                            at[1] + r * math.sin(i * math.pi / 8)) for i in range(16)]

    def read(self, at, svg, what=None, dx=0):
        """What a helper draws, standing at `at`: its <text>s are names and numbers,
        and `what`, if given, is its dot or disc. So the QC can't drift from it."""
        for text, x, y, px, bold, anchor in drawn_texts(svg):
            self.name(at, dx + x, y, text, px, anchor, bold)
        if what:
            self.mark(what, (at[0] + dx, at[1]), drawn_circles(svg)[0][2])

    def line(self, world_pts):
        self.lines.append([to_screen(self.cam, p) for p in world_pts])

    def tag(self, at, age, armed=False, dx=0):
        self.read(at, tag_name(armed), dx=dx)
        if age:
            self.read(at, tag_num(age, armed), dx=dx)

    def caleb(self, at, parts, age, armed=False, dx=0):
        self.fig("Caleb", at, parts, dx)
        self.tag(at, age, armed, dx)

    def children(self, at, dx):
        for x in (-dx, dx):
            self.fig(f"a child at {x}", at, F.child(), x)

    def kadesh(self, moses_arms="down"):
        """The Kadesh group: Moses, the young Joshua, the dot and its name."""
        k = self.at(KADESH)
        self.read(k, kadesh_mark(), "Kadesh's dot")
        self.fig("Moses", k, staffed(moses_arms), MOSES_DX, MOSES_FLIP)
        self.read(k, moses_name(), dx=MOSES_DX)
        self.fig("Joshua", k, F.man(), JOSHUA_DX)
        self.read(k, young_joshua_name(), dx=JOSHUA_DX)
        return k

    def gilgal(self, joshua_arms="down"):
        """The Gilgal group: its dot and name, and Joshua."""
        g = self.at(GILGAL)
        self.read(g, gilgal_mark(), "Gilgal's dot")
        self.fig("Joshua", g, staffed(joshua_arms), GIL_JOSHUA_DX)
        self.read(g, joshua_name_at_gilgal(), dx=GIL_JOSHUA_DX)
        return g


def standing(cv, tour):
    """A verse's rest on the map (None where it rests in a card or the cast
    has nothing standing)."""
    if cv == (14, 3):
        s = _Standing(tour.wide, tour)
        s.read((0, 0), "".join(sum_els(tour)))
        x, y = zero_at(tour)
        rx, ry = ZERO_R[0] + ZERO_PEN / 2, ZERO_R[1] + ZERO_PEN / 2
        s.names.append(("0", (x - rx, y - ry, x + rx, y + ry)))
        return s
    if cv not in MAP_AT:
        return None
    s = _Standing(tour.shot(*CAMERAS[MAP_AT[cv]]), tour)
    up, h = tour.PS(WALK_UP), s.at(HEBRON)
    if cv in ((14, 6), (14, 7)):
        spied = cv == (14, 7)
        k = s.kadesh("point_l" if spied else "down")
        s.caleb(k, F.man(arms="open") if spied else F.man(), 40 if spied else None)
        if spied:
            s.read(h, pale_dot(), "Hebron's dot")
            s.line(up)
            s.figs["the ten"] = ten_pts(h[0] + TEN_AT[0], h[1] + TEN_AT[1])
    elif cv in ((14, 8), (14, 9)):
        k = s.kadesh("up" if cv == (14, 9) else "down")
        s.figs["the people"] = [(k[0] + x, k[1] + y) for x, y in mound_pts()]
        s.read(h, pale_dot(), "Hebron's dot")
        s.line(up)
        s.caleb(s.at(ZIN if cv == (14, 8) else SOUTH), F.man(), 40)
        if cv == (14, 9):
            s.read(h, hebron_promised(), "Hebron's disc")
            s.children(h, CHILD_NEAR)
    elif cv == (14, 12):
        g = s.gilgal()
        s.caleb(g, F.soldier(), 85, armed=True, dx=GIL_CALEB_DX)
        s.read(h, pale_dot(), "Hebron's dot")
        s.line(up)
    elif cv == (14, 13):
        s.gilgal("up")
        s.read(h, hebron_given(tour), "Hebron's disc")
        s.read(h, hebron_mark())
        s.caleb(h, F.soldier(), 85, armed=True)
        s.line(up)
    elif cv == (14, 14):
        s.read(s.at(KADESH), kadesh_pale(), "Kadesh's dot")
        s.read(h, hebron_given(tour), "Hebron's disc")
        s.read(h, hebron_mark())
        s.caleb(h, F.soldier(), 85, armed=True)
        s.children(h, CHILD_BY)
        s.line(up)
    return s


def rest_rects(cv, tour):
    """The rest's names and figures as plates, for the tour's layout, so the
    water names keep off them."""
    s = standing(cv, tour)
    if s is None:
        return []
    out = [("cast:" + text, r) for text, r in s.names]
    for what, pts in s.figs.items():
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        out.append(("cast:" + what, (min(xs), min(ys), max(xs), max(ys))))
    return out


# ---------------------------------------------------------------------------
# QC
# ---------------------------------------------------------------------------

TITLE = "The lot of Judah — Joshua 14"  # the longer of the two titles over it all
AIR = 3                                 # screen px a name or number keeps clear
ONE_NUMBER = ({"9", "½"}, {"2", "½"})   # two <text>s that read as one number
# a walk that starts this long before its camera lands is under a still one: 14:7's
# starts 0.06 s before, with Hebron's dot under 3 px from its rest
SETTLED = 0.1


def _near(rect, pts, air):
    """Whether any of these points comes within `air` of the rect."""
    return any(math.hypot(max(rect[0] - x, x - rect[2], 0),
                          max(rect[1] - y, y - rect[3], 0)) < air for x, y in pts)


def ten_pts(x, y):
    """The ten's dots hung at (x, y), screen px, as ten() draws them (each drawn
    twice, on its halo)."""
    dots = dict.fromkeys(c[:2] for c in drawn_circles(ten()))
    return [(x + cx, y + cy) for cx, cy in dots]


def _along(path, f):
    """The point a fraction f of the way along a polyline."""
    goal, acc = f * seg_len(path), 0.0
    for a, b in zip(path, path[1:]):
        step = math.hypot(b[0] - a[0], b[1] - a[1])
        if step and acc + step >= goal:
            u = (goal - acc) / step
            return (a[0] + u * (b[0] - a[0]), a[1] + u * (b[1] - a[1]))
        acc += step
    return path[-1]


def _map_touches(r, s, tour):
    """What of the map's own a name or number's rect comes within AIR of."""
    box = inflate(r, AIR)
    out = []
    if any(poly_hits_rect([to_screen(s.cam, p) for p in w], box) for w in tour.water):
        out.append("the water")
    if any(circle_hits_rect(to_screen(s.cam, xy), tour.disc_r, box) for xy in tour.discs):
        out.append("a lot's disc")
    return out


def _walks(tour):
    """Each walk under a still camera that his tag rides: (verse, path, his age,
    armed, the part of its time the tag is off, when it starts, how long it takes)."""
    say, up = tour.say, tour.PS(WALK_UP)
    t_go, up_s, t_back = _up_times(say)
    t_walk, t_now, _t_85 = _years_times(say)
    return [((14, 7), up, 40, False, None, t_go, up_s),
            ((14, 7), up[::-1], 40, False, None, t_back, HOME_S),
            ((14, 8), up[:2], 40, False, None, _wholly(say, (14, 8)), ZIN_S),
            ((14, 9), up[1:3], 40, False, None, _wholly(say, (14, 9)), ZIN_S),
            ((14, 10), tour.PS(WALK_YEARS) + [caleb_on_card(tour)], 40, False, TAG_PAST,
             t_walk, round(t_now - t_walk, 2)),
            ((14, 13), [caleb_at_gilgal(tour), tour.P(*HEBRON)], 85, True, None,
             _given_times(say)[0], GIVEN_S)]


def _walk_qc(tour, rests):
    """His tag along each walk, against what stands at that verse's rest, and
    the ten along theirs."""
    out = set()
    for cv, path, age, armed, off, _t, _d in _walks(tour):
        s = rests[cv]
        names = [(t, r) for t, r in s.names if t not in ("Caleb", str(age))]
        figs = {k: pts for k, pts in s.figs.items() if k != "Caleb"}
        for i in range(101):
            u = i / 100
            if off and off[0] <= u <= off[1]:
                continue
            me = _Standing(s.cam, tour)
            me.tag(to_screen(s.cam, _along(path, ease(u))),
                   None if off and u > off[1] else age, armed)
            for text, r in me.names:
                hits = _map_touches(r, s, tour)
                hits += [o for o, q in names if gap(r, q) < AIR]
                hits += [k for k, pts in figs.items() if _near(r, pts, AIR)]
                if any(poly_hits_rect(ln, inflate(r, AIR)) for ln in s.lines):
                    hits.append("a line")
                out |= {f"{cv[0]}:{cv[1]}: walking, his {text} touches {h}" for h in hits}
    # the ten carry no tag, but must never touch a name that stands as they ride
    for cv, path in ((14, 7), ten_up(tour)), ((14, 8), ten_down(tour)):
        s = rests[cv]
        names = [(t, r) for t, r in s.names if t not in ("Caleb", "40")]
        for i in range(101):
            pts = ten_pts(*to_screen(s.cam, _along(path, i / 100)))
            out |= {f"{cv[0]}:{cv[1]}: riding, the ten touch {t}" for t, r in names
                    if _near(r, pts, AIR + BAND_R)}
    return sorted(out)


def _still(ref):
    """When a verse's camera is still, by its legs: [(from, to)]."""
    t, out = 0.0, []
    for i, (kind, _target, _d) in enumerate(LEGS.get(ref, [])):
        if kind == "hold":
            out.append((t, leg_end(ref, i)))
        t = leg_end(ref, i)
    return out + [(t, math.inf)]


def _clock_qc(tour):
    """-> [problem]: the words against what doesn't move with them, the camera and
    the fixed lengths. A re-rendered MP3 moves the words and not these (the module's
    docstring lists them), and a verse's picture breaks quietly: each walk under a still
    camera, 14:10's ending before the dive; the walk up, and the ten's, before
    "brought"; 85 before his tag goes; his arrival at Hebron before its ring."""
    say, out = tour.say, []
    for cv, _path, _age, _armed, _off, t, d in _walks(tour):
        where, end = f"{cv[0]}:{cv[1]}", round(t + d, 2)
        leaves = next((b for a, b in _still(cv) if a - SETTLED <= t <= b), None)
        if leaves is None:
            out.append(f"{where}: his walk starts at {t}, with the camera moving")
        elif end > leaves:
            out.append(f"{where}: his walk ends at {end}, and the camera moves at {leaves}")
    t_go, up_s, t_back = _up_times(say)
    if up_s < UP_S:
        out.append(f'14:7: "brought" at {t_back} cuts his walk up to {up_s} s, from UP_S')
    if round(t_go + TEN_LAG + TEN_UP_S, 2) > t_back:
        out.append(f'14:7: the ten reach Hebron after "brought" at {t_back}')
    t_85 = _years_times(say)[2]
    if t_85 > TAG_OFF:
        out.append(f'14:10: "eighty-five" at {t_85} comes after his tag goes at {TAG_OFF}')
    t_gave, t_ring = _given_times(say)
    if round(t_gave + GIVEN_S, 2) > t_ring:
        out.append(f'14:13: he reaches Hebron after "inheritance" at {t_ring}')
    return out


def cast_qc(tour):
    """-> [problem]: at each of the cast's rests, and 14:10's long hold, a name
    or number within AIR of another, a figure, a mark, a line, the map's water, a
    lot's disc, the key's names or the HUD's plates, or cut by the frame; a figure
    or mark within AIR of a plate, or cut by the frame; his tag along each walk
    (_walks); the ten along their rides; and the clock (_clock_qc). Run it after
    the tour's build (the plates' scale bar and the discs are the build's)."""
    out = []
    rests = {cv: standing(cv, tour) for cv in [(14, 3)] + list(MAP_AT)}
    # 14:10: he walks, so what stands still round him: the old line, Kadesh, 45,
    # and Gilgal's dot and name at the walk's end
    held = _Standing(tour.shot(*CAMERAS["stage"]), tour)
    held.read(held.at(KADESH), kadesh_pale(), "Kadesh's dot")
    held.read(held.at(GILGAL), gilgal_mark(), "Gilgal's dot")
    held.read((0, 0), forty_five())
    held.line(tour.PS(WALK_UP))
    held.line(tour.PS(WALK_YEARS) + [caleb_on_card(tour)])
    rests[(14, 10)] = held
    written = [tour.key_layout()[k]["box"] for k in ("MANASSEH_E", "GAD", "REUBEN", "LEVI")]
    for cv, s in rests.items():
        where = f"{cv[0]}:{cv[1]}"
        plates = tour.plates(cv, s.cam)
        for i, (text, r) in enumerate(s.names):
            if r[0] < 2 or r[1] < 2 or r[2] > W - 2 or r[3] > H - 2:
                out.append(f"{where}: {text} is cut by the frame")
            for other, q in s.names[i + 1:]:
                if gap(r, q) < AIR and {text, other} not in ONE_NUMBER:
                    out.append(f"{where}: {text} touches {other}")
            for what, pts in s.figs.items():
                if _near(r, pts, AIR):
                    out.append(f"{where}: {text} touches {what}")
            for line in s.lines:
                if poly_hits_rect(line, inflate(r, AIR)):
                    out.append(f"{where}: {text} touches a line")
            out += [f"{where}: {text} touches {what}" for what in _map_touches(r, s, tour)]
            for what, q in plates:
                if gap(r, q) < AIR:
                    out.append(f"{where}: {text} under the {what}")
            if cv == (14, 3):
                for q in written:
                    if gap(r, q) < AIR:
                        out.append(f"{where}: {text} touches the key at {q}")
        for what, pts in s.figs.items():
            if any(x < 2 or y < 2 or x > W - 2 or y > H - 2 for x, y in pts):
                out.append(f"{where}: {what} is cut by the frame")
            for plate, q in plates:
                if _near(q, pts, AIR):
                    out.append(f"{where}: {what} under the {plate}")
    return out + _walk_qc(tour, rests) + _clock_qc(tour)


def _rests(card):
    """Where the camera stays on this card: (verse, shot, the time it leaves,
    or None for the verse's rest)."""
    out = []
    for ref, legs in LEGS.items():
        t, on = 0.0, None
        for i, (kind, target, d) in enumerate(legs):
            t += d
            if kind == "to":
                on = target if target.startswith(card.key + ":") else None
            if on and (i + 1 == len(legs) or legs[i + 1][0] == "to"):
                out.append((ref, on, None if i + 1 == len(legs) else round(t, 2)))
    return out


def _state_then(card, ref, t):
    """Every actor's state at t in the verse (None: its end)."""
    st = card.state_at(ref)
    for kind, key, ev_t, d, val in sorted(card.events.get(ref, []), key=lambda e: e[2]):
        if t is None or ev_t + d <= t:
            apply_event(st[key], kind, val)
    return st


def _card_numbers(card, ref, st, t):
    """The numbers standing on the card, card px, read from their own <text>s: the
    marks over men's heads, and at a verse's rest its effects' (14:2's 9 and 1/2)."""
    out = []

    def numbers(svg, ox, oy):
        for text, x, y, px, bold, anchor in drawn_texts(svg):
            b = ink(text, px, bold, False, anchor + "m")
            out.append((text, (ox + x + b[0], oy + y + b[1], ox + x + b[2], oy + y + b[3])))
    for r in card.refs:
        for kind, key, ev_t, d, val in card.events.get(r, []):
            if (kind == "mark" and st[key]["shown"]
                    and (r < ref or (r == ref and (t is None or ev_t + d <= t)))):
                numbers(val, st[key]["x"], st[key]["y"])
    if t is None:
        for svg in card.fx.get(ref, []):
            numbers(svg, 0, 0)
    return out


def qc(card):
    """-> [problem]: at each rest and hold on the card, a name or number that
    shows there within AIR of another, or of the ink of a figure that stands
    there (its own, staff included); or one under the title, or at gil:joseph on
    the bracket. A name its rest leaves cut by the frame goes as it leaves
    (svg_scene_card), so it isn't asked."""
    out = []
    for ref, name, t in _rests(card):
        shot = SHOTS[name]
        z = shot[2]
        where = f"{ref[0]}:{ref[1]} {name}" + ("" if t is None else f" at {t}")
        st = _state_then(card, ref, t)
        frame = shot_rect(shot, (2, 2, W - 2, H - 2))
        title = shot_rect(shot, title_rect(TITLE))
        marks = _card_numbers(card, ref, st, t)
        names = []
        for key, a in card.actors.items():
            s = st[key]
            if s["label"] and s["shown"] and name_op(z, a.names_at or card.names_at) > 0:
                b = ink(s["label"], 18, False, a.label_italic, "mm")
                x, y = s["x"], s["y"] + a.label_y
                r = (x + b[0] / z, y + b[1] / z, x + b[2] / z, y + b[3] / z)
                if within(r, frame):
                    names.append((s["label"], r))
        figs = {}
        for key, a in card.actors.items():
            s = st[key]
            parts = a.parts(dict(s["pose"]))
            if parts and s["shown"]:
                figs[key] = ink_points(parts, s["x"], s["y"],
                                       a.h / a.unit_h * s.get("scale", 1.0), s["flip"])
        air = AIR / z
        texts = names + marks
        for i, (text, r) in enumerate(texts):
            if gap(r, title) < air:
                out.append(f"{where}: {text} under the title")
            if name == "gil:joseph" and gap(r, BRACKET) < air:
                out.append(f"{where}: {text} touches the bracket")
            for other, q in texts[i + 1:]:
                if gap(r, q) < air and {text, other} not in ONE_NUMBER:
                    out.append(f"{where}: {text} touches {other}")
            for key, (pts, bb) in figs.items():
                if gap(r, bb) < air and _near(r, pts, air):
                    out.append(f"{where}: {text} touches {key}")
    return out
