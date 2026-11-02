"""Genesis 2-3 (garden_stage.py, garden_qc.py and the two chapters), with no clock and no writing:
every word a beat is cued to is in its verse, every camera leg goes somewhere, the marks and the
re-shots hold, nothing begins on his name, stone is only what is spoken of, every pose is on the
list, a body is never two at once and an arm or a head moves as a limb, nobody is switched off in
sight, the art keeps clear of the river, the trim drops nothing a frame can see (its boxes checked
against the ink, read here by a path reader of its own), the engraved dashes keep their pattern, a plate comes and goes by a cut, its own ground covers the frame
whenever it is in, and the scene is off only under it, and the QC is clear and has teeth.
write_story runs the QC on the clock. test_garden_bytes.py, run by hand, is the slow check on the
neighbours' bytes.

    .venv\\Scripts\\python.exe -m unittest test_garden
"""

import functools
import math
import os
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import garden_art as G
import garden_qc as Q
import garden_stage as S
import genesis2_garden as G2
import genesis3_garden as G3
import svg_figures as F
import svg_map_camera as C
from generate_tabernacle import BG, BROWN, GOLD, HL

REFS = S.chapter_refs(2) + S.chapter_refs(3)
BEASTS = ("lion1", "lion2", "wolf1", "wolf2", "ox1", "ox2", "sheep1", "sheep2", "don1", "don2")
# Rule 22, on the card. By hand, they stand in 2:24 and 3:15
STONE_ACTORS = {"dig", "lest"}
STONE_VERSES = {"2:24", "2:25", "3:15", "3:16", "3:17", "3:18", "3:19", "3:22", "3:23"}
ROCK_WEST = 660                     # the art's rock east of his plot: garden_art.ROCKS
CREEP = .08                         # a creep's reach from its shot's zoom, creep on creep included
# Where the re-shots are used: the frames a viewer has seen before, by name (garden_stage's SHOTS),
# which docs/design/genesis-garden.md's "The reversals, seen" turns on
USED = {"pair": ("2:5", "2:25", "3:7"), "every": ("2:9", "2:16", "3:2", "3:22"),
        "plot": ("2:15", "3:17"), "fruit": ("2:17", "3:3", "3:6"), "alone": ("2:18", "2:20")}
# When his name is said on today's MP3s: garden_qc.name_windows asks the clock
TODAY = {
    "2:2": [(1.1, 1.3)], "2:3": [(.15, .35)], "2:4": [(5.93, 6.52)], "2:5": [(5.63, 6.21)],
    "2:7": [(.15, .8)], "2:8": [(.15, .81)], "2:9": [(1.1, 1.71)], "2:15": [(.15, .82)],
    "2:16": [(.15, .81)], "2:18": [(.15, .93)], "2:19": [(1.13, 1.76)], "2:21": [(.14, .81)],
    "2:22": [(.15, .72)], "3:1": [(3.61, 4.19), (6.63, 6.86)], "3:3": [(3.4, 3.63)],
    "3:5": [(.36, .55), (5.1, 5.67)], "3:8": [(.73, 1.42), (7.22, 7.76)], "3:9": [(.15, .78)],
    "3:11": [(.13, .37)], "3:13": [(.15, .73)], "3:14": [(.15, .78)], "3:21": [(.15, .82)],
    "3:22": [(.15, .93)], "3:23": [(.7, 1.26)],
}


def today(ref):
    return TODAY.get(ref, [])


def said():
    """Every (verse, word, n) the verses ask the narration for."""
    words = []

    def say(ref, word, n=0, lead=0.0):
        words.append((ref, word, n))
        return None                     # so each beat keeps its hand value
    S.build_story(say=say)
    return words


@functools.cache
def told():
    """The whole story on today's values, and nothing drawn yet."""
    return S.build_story(say=None)


@functools.cache
def whole():
    """The whole story and all its files, once. A test that breaks something breaks its own."""
    story = S.build_story(say=None)
    return story, {ref: story.verse_file(ref) for ref in REFS}


def one(ref):
    """A story of its own to break, and this verse's file."""
    story = S.build_story(say=None)
    return story, story.verse_file(ref)


def rest(story, ref):
    """Every actor's state at the verse's end."""
    return Q.state_then(story.card, ref, story.verses[ref].dur)


class Cues(unittest.TestCase):
    def test_every_word_is_in_its_verse(self):
        """A misspelt word would keep its hand value for good, with no complaint."""
        words = said()
        self.assertGreater(len(words), 250)
        for ref, word, n in sorted(set(words)):
            with self.subTest(verse=ref, word=word, n=n):
                self.assertGreater(len(S.occurrences(ref, word)), n)

    def test_a_misspelt_word_does_not_build(self):
        with self.assertRaises(KeyError):
            S.say("2:1", "earthh")


class Legs(unittest.TestCase):
    def test_every_leg_goes_somewhere(self):
        story = told()

        def near_a_shot(cam):
            z, x, y = cam
            return any(x == sx and y == sy and abs(z / sz - 1) <= CREEP
                       for sx, sy, sz in S.SHOTS.values())
        for ref, v in story.verses.items():
            last = 0.0
            for t0, t1, cam in sorted(v.keys, key=lambda k: k[:2]):
                with self.subTest(verse=ref, leg=(t0, t1)):
                    self.assertTrue(near_a_shot(cam), cam)
                    self.assertTrue(t1 > t0 or (t1 == t0 and t0 in v.cuts))
                    self.assertGreaterEqual(t0, last - 1e-6)
                    self.assertLessEqual(t1, v.dur)
                last = t1

    def test_a_plate_comes_and_goes_by_a_cut(self):
        """Every verse with a plate cuts to it or from it, and none dives to one or flies out."""
        story, _files = whole()
        for ref in REFS:
            fl = story.drawn[ref]
            plates = fl.plates
            with self.subTest(verse=ref):
                self.assertEqual(bool(plates), bool(fl.cut_keys))
                for zin, _off, _on in plates:
                    n = len(fl.cams) - 1
                    for i in range(n):
                        if i not in fl.cut_keys:
                            # no key list crosses a plate's zoom but by a cut
                            self.assertEqual(fl.cams[i][0] >= zin, fl.cams[i + 1][0] >= zin,
                                             (i, fl.cams[i][0], fl.cams[i + 1][0]))


class Marks(unittest.TestCase):
    def test_no_one_rests_under_the_east_fruit(self):
        for mark in (S.M0, S.W0, S.W_REACH, S.M_BY, S.M_APART, S.W_APART, S.M_REACH, S.M_FIG,
                     S.M_PLOT, S.HIDE_M, S.HIDE_W, S.M_OUT, S.W_OUT, S.W_FRONT, S.W_T, S.W_RULE):
            self.assertFalse(690 <= mark <= 780, mark)
        story = told()
        for ref in REFS:
            st = rest(story, ref)
            for key in Q.PEOPLE:
                if st[key]["shown"]:
                    with self.subTest(verse=ref, who=key):
                        self.assertFalse(690 <= st[key]["x"] <= 780, st[key]["x"])

    def test_his_plot_and_the_shoot(self):
        """2:15 and 3:17 both read them: the shoot wilts where he raised it, and he is there."""
        story = told()
        self.assertEqual(rest(story, "2:15")["man"]["x"], S.M_PLOT)
        self.assertEqual(story.card.state_at("3:17")["man"]["x"], S.M_PLOT)
        self.assertEqual(rest(story, "2:15")["shoot"]["x"], S.SHOOT_X)
        self.assertTrue(rest(story, "2:15")["shoot"]["shown"])
        self.assertFalse(rest(story, "3:17")["shoot"]["shown"])
        self.assertIn(f"translate({S.SHOOT_X} ", S.after_curse())

    def test_the_shoot_is_off_the_rock(self):
        self.assertLess(S.SHOOT_X, ROCK_WEST)

    def test_the_serpents_marks_are_in_order_along_the_road(self):
        marks = (S.S_IN, S.S_NAMED, S.S_OUT, S.S_CLOSE, S.s_at((-6, 1404)), S.S_FELL, S.S_END,
                 S.S_REAR)
        self.assertEqual(list(marks), sorted(set(marks)))
        self.assertLessEqual(S.S_REAR, S.SN.L)

    def test_he_comes_into_sight_by_moving(self):
        """As 3:1 opens on 2:25's frame, all of him lies on the road beyond its edge, his head too,
        so that he never fades in in plain view."""
        x0, y0, x1, y1 = C.visible_world(S.camera("pair"))
        self.assertGreaterEqual(S.S_IN - S.SN.body, 0)
        for s in range(int(S.S_IN - S.SN.body), int(S.S_IN) + 1):
            x, y, _ang = S.SN.at(s)
            self.assertTrue(x > x1 + S.SN.girth or y < y0 - S.SN.girth, (s, x, y))
        x, _y, ang = S.SN.at(S.S_IN)
        self.assertGreater(x + S.SNOUT * math.cos(math.radians(ang)), x1 + 4)

    def test_the_reshots_are_used_where_they_are_said_to_be(self):
        story = told()
        for shot, refs in USED.items():
            for ref in refs:
                with self.subTest(shot=shot, verse=ref):
                    self.assertIn(S.camera(shot), [k[2] for k in story.verses[ref].keys])


class Reshots(unittest.TestCase):
    def test_same_camera(self):
        """A re-shot that drifts is the design gone."""
        story = told()
        pair = S.camera("pair")
        self.assertEqual(story.verses["2:5"].flight().cam1, pair)
        three8 = story.verses["3:8"].flight()
        self.assertEqual(story.verses["3:7"].flight().cam1, pair)
        self.assertEqual(three8.cam0, pair)
        self.assertEqual(min(k[0] for k in story.verses["3:8"].keys), 7.76)
        for t in (0.0, 3.0, 7.7):
            self.assertAlmostEqual(three8.at(t)[0], pair[0], places=6)
            self.assertAlmostEqual(three8.at(t)[1], pair[1], places=3)
            self.assertAlmostEqual(three8.at(t)[2], pair[2], places=3)
        self.assertEqual(story.verses["2:25"].flight().cam1, story.verses["3:7"].flight().cam1)
        plot = S.camera("plot")
        self.assertEqual(story.verses["2:15"].flight().cam1, plot)
        self.assertEqual(sum(k[2] == plot for k in story.verses["3:17"].keys), 2)


class Names(unittest.TestCase):
    def test_nothing_begins_on_his_name(self):
        """Over the events and legs, from today's values, with the lead. 2:21's beasts are already
        walking."""
        story = told()

        def on_it(t, windows):
            return any(a - Q.NAME_LEAD <= t < b - .011 for a, b in windows)
        for ref, windows in TODAY.items():
            for t0, _t1, _cam in story.verses[ref].keys:
                with self.subTest(verse=ref, leg=t0):
                    self.assertFalse(on_it(t0, windows))
            for kind, key, t, _d, _val in story.card.events.get(ref, []):
                if ref == "2:21" and key in BEASTS and kind == "move":
                    continue
                with self.subTest(verse=ref, event=(kind, key, t)):
                    self.assertFalse(on_it(t, windows))


class Stone(unittest.TestCase):
    def test_paint(self):
        """Pale and warm, one solid treatment, the head lighter than the face so that a cap and a
        beard never read as a hood."""
        stone = S.PAINTS["stone"]
        self.assertGreater(sum(stone["hair"][0]), sum(stone["skin"]))
        for colour in (stone["skin"], stone["far"], stone["near"], stone["hair"][0]):
            self.assertGreaterEqual(colour[0], colour[1])
            self.assertGreaterEqual(colour[1], colour[2])
        self.assertGreater(sum(stone["skin"]), sum(S.PAINTS["live"]["key"]))

    def test_only_spoken_of(self):
        """Only the two stone men carry stone on the card, and it never changes on anyone, and only
        the verses of rule 22 draw it. All the living, 3:20, are warm."""
        story, files = whole()
        for key, actor in story.card.actors.items():
            self.assertEqual(actor.start["pose"].get("paint") == "stone", key in STONE_ACTORS, key)
        for ref in REFS:
            for kind, key, _t, _d, val in story.card.events.get(ref, []):
                if kind == "pose" and "paint" in val:
                    self.fail(f"{ref}: {key} changes paint")
        skin = G._hex(S.PAINTS["stone"]["skin"])
        self.assertEqual({ref for ref, svg in files.items() if skin in svg}, STONE_VERSES)


class Poses(unittest.TestCase):
    def test_on_the_list(self):
        self.assertEqual(Q.poses_on_the_list(told().card), [])

    def test_the_words_are_in_their_verses(self):
        for ref, _key, _change, word in Q.POSES:
            with self.subTest(verse=ref, word=word):
                self.assertTrue(S.occurrences(ref, word))

    def test_a_stride_is_not_listed(self):
        self.assertFalse([p for p in Q.POSES if "walk" in p[2]])


class Looks(unittest.TestCase):
    """Rule 21 on the Stage: a body is never see-through, and never two."""

    STAND, WALK = {"legs": "stand", "arms": "down"}, {"legs": "walk", "arms": "swing"}

    def test_a_stride_starts_and_stops_at_once(self):
        """Striding legs faded in over standing ones would be two pairs of legs."""
        self.assertTrue(S.whole_body(self.STAND, 1, self.WALK, 1))
        self.assertTrue(S.whole_body(self.WALK, 1, self.STAND, 1))
        self.assertFalse(S.whole_body(self.STAND, 1, dict(self.STAND, up=12), 1))
        evs = [("pose", "man", 1.0, .12, self.WALK), ("pose", "man", 3.0, .14, self.STAND)]
        s0 = {"pose": dict(self.STAND), "flip": 1}
        self.assertEqual([e[3] for e in S.Stage._turns_at_once(s0, evs)], [S.TURN_S, S.TURN_S])

    def test_a_look_goes_when_a_later_one_is_whole(self):
        """A look still fading in, overtaken by one that comes in at once: the look before both
        goes when the second is whole, and not when the first would have been."""
        c = S.Stage()
        S.add_cast(c)
        fl = S.VerseFlight((1.0, 0, 1300), [])
        c._wk, c._wb, c._syms, c._sym_defs = S.coarse(fl, S.key_w), S.coarse(fl, S.body_w), {}, []
        s0 = {"x": 0.0, "y": 0.0, "shown": True, "flip": 1, "pose": {"arms": "down"}}
        evs = [("pose", "man", 1.0, .2, {"up": 12}),
               ("pose", "man", 1.05, .12, dict(self.WALK, _flip=-1))]
        svg = c._actor(c.actors["man"], s0, evs)
        self.assertEqual(re.findall(r'values="1;0" begin="([\d.]+)s"', svg), ["1.09", "1.09"])

    def test_an_arm_or_a_head_alone_is_a_limb(self):
        """A change of the arms, the head or the lean alone, made while they are in sight, moves as
        a limb: a new arm faded in over the old would be a second arm, seen through."""
        self.assertEqual(limbs_faded(told().card), [])
        card = S.build_story(say=None).card
        card.on("3:3", ("pose", "wom", 5.0, .2, {"arms": "down"}))
        self.assertEqual(limbs_faded(card), [("3:3", "wom", 5.0)])

    def test_no_one_is_switched_off_in_sight(self):
        """A person on the card is out of the frame, or under a plate, when they are switched off:
        at 3:24 that follows from the camera, wherever 3:23's narration has left them."""
        story, _files = whole()
        self.assertEqual(switched_off_in_sight(story), [])
        story, _svg = one("3:24")
        evs = story.card.events["3:24"]
        evs[:] = [e[:2] + (4.0,) + e[3:] if e[0] == "hide" and e[1] == "wom" else e for e in evs]
        self.assertEqual(switched_off_in_sight(story, ("3:24",)), [("3:24", "wom", 4.0)])


# Where a drawing takes a person over at the moment they are switched off: 3:19's dust, as he sinks
TAKEN_OVER = {("3:19", "dig")}


def switched_off_in_sight(story, refs=REFS):
    """Every hide of a person whose ink is in the frame then, with no plate over it: (verse, who,
    when)."""
    out = []
    for ref in refs:
        fl = story.drawn[ref]
        for kind, key, t, _d, _val in story.card.events.get(ref, []):
            if kind != "hide" or key not in Q.PEOPLE or (ref, key) in TAKEN_OVER:
                continue
            st = Q.state_then(story.card, ref, t - .001)
            x0, y0, x1, y1 = C.visible_world(fl.at(t))
            pts = Q.ink_of(story.card, key, st[key])[0]
            if not fl.covered(t) and any(x0 <= x <= x1 and y0 <= y <= y1 for x, y in pts):
                out.append((ref, key, t))
    return out


def limbs_faded(card):
    """Every change of the arms, the head or the lean alone, of someone in sight, that isn't a
    limb's move: (verse, who, when)."""
    out = []
    for ref in REFS:
        st = card.state_at(ref)
        seen_from = {k: (-1.0 if s["shown"] else None) for k, s in st.items()}
        for kind, key, t, _d, val in sorted(card.events.get(ref, []), key=lambda e: e[2]):
            if kind == "show":
                seen_from[key] = t
            elif kind == "hide":
                seen_from[key] = None
            elif kind == "flip":
                st[key]["flip"] = val
            elif kind == "pose":
                p0 = {k: v for k, v in st[key]["pose"].items() if k != "_morph"}
                p1 = {k: v for k, v in dict(p0, **val).items() if k != "_morph"}
                changed = {k for k in set(p0) | set(p1) if p0.get(k) != p1.get(k)}
                if (key in Q.PEOPLE and seen_from[key] is not None and seen_from[key] < t
                        and changed and changed <= {"arms", "up", "lean"} and "_morph" not in val
                        and not S.whole_body(p0, st[key]["flip"], p1, st[key]["flip"])):
                    out.append((ref, key, t))
                st[key]["pose"] = dict(st[key]["pose"], **val)
    return out


class Art(unittest.TestCase):
    def test_no_acacia_on_a_head(self):
        """The whole tree, its foot and the crown standing above it, is clear of every head's
        ribbon, since the river is drawn over it; and its foot is on Cush, between the first two
        ridges."""
        x0, x1, _y0, y1 = F.bbox((G.acacia(), 0))
        for x, d, k in G.CUSH_ACACIAS:
            px, py = G.acacia_at(x, d, k)
            top, half_w = py - y1 * G.ACACIA_S * k, max(-x0, x1) * G.ACACIA_S * k
            for sx in range(int(px - half_w), int(px + half_w) + 1, 10):
                for run in G._HEAD_PTS.values():
                    for (ax, ay, aw), (bx, by, bw) in zip(run, run[1:]):
                        if min(ax, bx) <= sx <= max(ax, bx):
                            u = (sx - ax) / ((bx - ax) or 1)
                            cy = ay + (by - ay) * u
                            half = (aw + (bw - aw) * u) * G.PLAN_K["head"] / 2
                            with self.subTest(acacia=(x, d), at=sx):
                                self.assertTrue(top > cy + half or py < cy - half)
            ridges = [at_x([(rx, G.GROUND - rd) for rx, rd in r], px) for r in G.RIDGES[:2]]
            with self.subTest(acacia=(x, d)):
                self.assertTrue(ridges[0] < py < ridges[1])

    def test_no_thorn_on_the_rivers_bands(self):
        """A clump of thorns is plants at depths of their own, its nearest well south of its point.
        So each clump's whole drawing, near ones and the thorn land's alike, stands north of every
        edge of every run of the river across its width: none of them in the water."""
        land = G.panorama("planted", lean=True, heroes=False, thorns_too=True)
        boxes = G._drawing_boxes(land.defs)
        edges = [e for run in [G._MAIN] + list(G._HEADS.values())
                 for e in G._ribbon_points(G._cut_side(run))]
        clumps = [(gid, x, G.ground_y(x) + drop, k, False) for gid, x, drop, k in G.NEAR_THORNS]
        clumps += [(m.group(1), float(m.group(2)), float(m.group(3)), abs(float(m.group(4))),
                    float(m.group(4)) < 0) for m in G._USE_TF.finditer(land.outside)]
        self.assertGreater(len(clumps), len(G.NEAR_THORNS))
        for gid, x, y, k, flip in clumps:
            b = boxes[gid]
            x0, x1 = (x - b[2] * k, x - b[0] * k) if flip else (x + b[0] * k, x + b[2] * k)
            for sx in [x0 + (x1 - x0) * i / 20 for i in range(21)]:
                for edge in edges:
                    ey = at_x(edge, sx)
                    if ey is not None:
                        with self.subTest(clump=(gid, round(x)), at=round(sx)):
                            self.assertLess(y + b[3] * k, ey)
        near = S.dimmed(G.thorns_near())
        self.assertIn(near, S.garden(S.VerseFlight(S.camera("toil"), []), "3:20").outside)

    def test_the_river_is_drawn_after_what_is_under_it(self):
        world = G2.plan_world({"defs": "", "land": "<land/>", "garden": "<garden/>",
                               "river": "<river/>", "named": "<named/>"},
                              {"Pishon": "<head/>"}, "<lands/>")
        order = [world.index(q) for q in ("<land/>", "<lands/>", "<garden/>", "<river/>",
                                          "<head/>", "<named/>")]
        self.assertEqual(order, sorted(order))
        near = G.river_svg()["near"]
        side = G.panorama("planted", lean=True, heroes=False)
        self.assertIn(near, side.front)
        self.assertLess(side.front.index(near), side.front.index(G.bank_svg("planted", True, 0)))
        self.assertGreater(len(side.behind), 0)


def at_x(line, x):
    """A polyline's y at x, or None if it doesn't reach there."""
    for (ax, ay), (bx, by) in zip(line, line[1:]):
        if min(ax, bx) <= x <= max(ax, bx):
            return ay + (by - ay) * (x - ax) / ((bx - ax) or 1)
    return None


_TOKEN = re.compile(r"[A-Za-z]|[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")
_ARGS = {"m": 2, "l": 2, "h": 1, "v": 1, "c": 6, "s": 4, "q": 4, "t": 2, "a": 7, "z": 0}


def _arc(p0, rx, ry, phi, large, sweep, p1, steps=24):
    """Points along an SVG arc, by the spec's endpoint-to-centre conversion."""
    if p0 == p1:
        return []
    if not rx or not ry:
        return [p1]
    rx, ry = abs(rx), abs(ry)
    c, s = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    dx, dy = (p0[0] - p1[0]) / 2, (p0[1] - p1[1]) / 2
    x1, y1 = c * dx + s * dy, -s * dx + c * dy
    lam = x1 * x1 / (rx * rx) + y1 * y1 / (ry * ry)
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1
    k = math.sqrt(max(0.0, num / (rx * rx * y1 * y1 + ry * ry * x1 * x1)))
    k = -k if large == sweep else k
    cx1, cy1 = k * rx * y1 / ry, -k * ry * x1 / rx
    cx = c * cx1 - s * cy1 + (p0[0] + p1[0]) / 2
    cy = s * cx1 + c * cy1 + (p0[1] + p1[1]) / 2

    def ang(ux, uy, vx, vy):
        return math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
    a0 = ang(1, 0, (x1 - cx1) / rx, (y1 - cy1) / ry)
    da = ang((x1 - cx1) / rx, (y1 - cy1) / ry, (-x1 - cx1) / rx, (-y1 - cy1) / ry)
    if not sweep and da > 0:
        da -= 2 * math.pi
    elif sweep and da < 0:
        da += 2 * math.pi
    out = []
    for i in range(1, steps + 1):
        a = a0 + da * i / steps
        ex, ey = rx * math.cos(a), ry * math.sin(a)
        out.append((c * ex - s * ey + cx, s * ex + c * ey + cy))
    return out


def drawn_points(d, steps=12):
    """Points along everything a path's `d` draws, by a reading of SVG's path grammar of its own:
    curves and arcs sampled, so that a box made from them is the ink's, not its controls'."""
    toks = _TOKEN.findall(d)
    pts, i, cmd = [], 0, ""
    cur = start = (0.0, 0.0)
    prev_c = prev_q = None
    while i < len(toks):
        if toks[i].isalpha():
            cmd = toks[i]
            i += 1
        low, rel = cmd.lower(), cmd.islower()
        if low == "z":
            cur, prev_c, prev_q = start, None, None
            pts.append(cur)
            continue
        a = [float(q) for q in toks[i:i + _ARGS[low]]]
        i += _ARGS[low]
        ox, oy = cur if rel else (0.0, 0.0)

        def p(k):
            return ox + a[k], oy + a[k + 1]
        c_next = q_next = None
        if low == "m":
            cur = start = p(0)
            pts.append(cur)
            cmd = "l" if rel else "L"
        elif low == "l":
            cur = p(0)
            pts.append(cur)
        elif low == "h":
            cur = (ox + a[0], cur[1])
            pts.append(cur)
        elif low == "v":
            cur = (cur[0], oy + a[0])
            pts.append(cur)
        elif low in "cs":
            c1 = p(0) if low == "c" else ((2 * cur[0] - prev_c[0], 2 * cur[1] - prev_c[1])
                                          if prev_c else cur)
            c2, end = (p(2), p(4)) if low == "c" else (p(0), p(2))
            for j in range(1, steps + 1):
                t = j / steps
                u = 1 - t
                pts.append(tuple(u ** 3 * cur[k] + 3 * u * u * t * c1[k] + 3 * u * t * t * c2[k]
                                 + t ** 3 * end[k] for k in (0, 1)))
            cur, c_next = end, c2
        elif low in "qt":
            ctrl = p(0) if low == "q" else ((2 * cur[0] - prev_q[0], 2 * cur[1] - prev_q[1])
                                            if prev_q else cur)
            end = p(2) if low == "q" else p(0)
            for j in range(1, steps + 1):
                t = j / steps
                u = 1 - t
                pts.append(tuple(u * u * cur[k] + 2 * u * t * ctrl[k] + t * t * end[k]
                                 for k in (0, 1)))
            cur, q_next = end, ctrl
        elif low == "a":
            end = p(5)
            pts += _arc(cur, a[0], a[1], a[2], int(a[3]), int(a[4]), end)
            cur = end
        prev_c, prev_q = c_next, q_next
    return pts


def box_of(pts, grow=0.0):
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    return min(xs) - grow, min(ys) - grow, max(xs) + grow, max(ys) + grow


def inside(inner, outer, tol=1e-6):
    return (inner[0] >= outer[0] - tol and inner[1] >= outer[1] - tol
            and inner[2] <= outer[2] + tol and inner[3] <= outer[3] + tol)


class Trim(unittest.TestCase):
    """What a frame can see: `Scene.trimmed` leaves out what a verse's camera never meets, by
    garden_art's own boxes, so a box that comes up short would drop something in frame for good."""

    PATHS = ("M10 10L20 30H40V5C50 0 60 40 70 10S90 0 100 20Q110 40 120 10T140 10"
             "A10 20 30 1 1 160 10Z",
             "m10 10l10 20h20v-25c10-5 20 35 30 5s20-10 30 10q10 20 20-10t20 0a10 20 30 0 0 20 0z",
             "M0 0 10 10 20 0m5 5 3 3",
             "M-5.5-6.5q3.2 8.4 7.1-2.2t4 3 -2 7.5 4.4-1z",
             "M3 4h.001M50 50a2 2 0 1 1 4 0a2 2 0 1 1 -4 0z")

    # Each holds only by the command it ends on, which nothing before it can widen enough
    ALONE = ("M0 0C5 0 10 -20 10 0S30 0 30 0", "M0 0c5 0 10-20 10 0s20 0 20 0",
             "M0 0A10 10 0 1 1 2 0", "M0 0a10 20 30 1 0 4 1", "M0 0A1 100 0 0 1 10 0",
             "M0 0Q10 -20 20 0T40 0")

    def test_a_paths_box_holds_all_it_draws(self):
        """Each hand-written path, and each of them cut after every one of its commands, so that no
        command's ink is held only by another's."""
        ds = list(self.ALONE)
        for d in self.PATHS:
            cuts = [m.start() for m in re.finditer(r"[A-Za-z]", d)][1:] + [len(d)]
            ds += [d[:i] for i in cuts]
        for prec in (0, 1):
            d = G._D(prec)
            d.poly([(0, 0), (40.25, -12.5), (55, 30), (-7.5, 22)], True)
            d.closed_curve([(100, 100), (160, 80), (190, 140), (150, 190), (110, 175), (90, 130)])
            d.open_curve([(-50, 0), (-20, -40), (10, 20)])
            d.open_curve([(-50, 0), (-20, -40), (10, 20), (30, -15), (70, 5), (90, 60)])
            d.dot(-30.4, 60.2, 6.3)
            d.pip(12.5, -8.25)
            ds.append(d.text())
        land = G.panorama("planted", lean=True, heroes=False)
        ds += [m.group(1) for m in G._PATH_EL.finditer(land.behind)][:300]
        for d in ds:
            with self.subTest(d=d[:60]):
                self.assertTrue(inside(box_of(drawn_points(d)), G._path_box(d)), d[:60])

    def test_in_frame_drops_only_what_a_frame_never_meets(self):
        defs = '<g id="aa"><path fill="#123456" d="M0 0L10 0L10 10L0 10Z"/></g>'
        rect = (0, 0, 100, 100)
        cases = {
            "in": ('<path fill="#000" d="M20 20L30 30"/>', True),
            "out": ('<path fill="#000" d="M200 200L230 230"/>', False),
            "across": ('<path fill="#000" d="M-50 50L150 50"/>', True),
            "generous: a control in frame, the ink not": (
                '<path fill="#000" d="M-40 -40Q50 30 140 -40"/>', True),
            "a wide stroke reaching in": ('<path fill="none" stroke="#000" stroke-width="12" '
                                          'd="M104 50L120 50"/>', True),
            "a thin stroke just out": ('<path fill="none" stroke="#000" stroke-width="1" '
                                       'd="M104 50L120 50"/>', False),
            "a rect in": ('<rect x="90" y="90" width="40" height="40" fill="#000"/>', True),
            "a rect out": ('<rect x="101" y="0" width="40" height="40" fill="#000"/>', False),
            "a drawing in": (G._use("aa", 95, 95), True),
            "a drawing out": (G._use("aa", 103, 50), False),
            "a drawing turned round, in": (G._use("aa", 105, 50, flip=True), True),
            "a drawing scaled out": (G._use("aa", 150, 50, k=2.0), False),
            "a drawing rising in": (G._grow_use("aa", 95, 50), True),
            "a drawing rising out": (G._grow_use("aa", 120, 50, k=1.5), False),
            "an unknown drawing": (G._use("zz", 900, 900), True),
        }
        for name, (svg, kept) in cases.items():
            with self.subTest(name):
                self.assertEqual(svg in G.in_frame(svg, rect, defs), kept, name)
        many = '<path fill="#000" d="M20 20L30 30M300 300L310 310M90 90L120 120"/>'
        self.assertEqual(G.in_frame(many, rect, defs),
                         '<path fill="#000" d="M20 20L30 30M90 90L120 120"/>')
        self.assertEqual(G.in_frame('<g><path d="M300 300L310 310"/></g>', rect, defs), "")

    def test_on_the_land_nothing_in_frame_is_dropped(self):
        """Every path, piece of a path and drawing the trim takes out of the real side view, by
        its ink sampled here, lies wholly outside the frame."""
        land = G.panorama("planted", lean=True, heroes=False, thorns_too=True)
        drawings = {}
        for gid, body in G._G_ID.findall(land.defs):
            boxes = []
            for m in G._D_ATTR.finditer(body):
                w = G._WIDTH.search(m.group(0))
                ink = drawn_points(m.group(1))
                if ink:
                    boxes.append(box_of(ink, float(w.group(1)) / 2 if w else 0.0))
            if boxes:
                drawings[gid] = (min(b[0] for b in boxes), min(b[1] for b in boxes),
                                 max(b[2] for b in boxes), max(b[3] for b in boxes))
        for shot in ("every", "plot", "toil", "last"):
            rect = C.visible_world(S.camera(shot))
            for part in (land.behind, land.front, land.outside):
                kept = G.in_frame(part, rect, land.defs)
                for m in G._PATH_EL.finditer(part):
                    d = m.group(1)
                    w = G._WIDTH.search(m.group(0))
                    half = float(w.group(1)) / 2 if w else 0.0
                    for piece in (re.split(r"(?=M)", d)[1:] if d.count("M") > 1 else [d]):
                        if piece not in kept:
                            with self.subTest(shot=shot, piece=piece[:40]):
                                self.assertFalse(G._meets(rect, *box_of(drawn_points(piece), half)))
                for m in G._USE_TF.finditer(part):
                    if m.group(0) not in kept and m.group(1) in drawings:
                        k = float(m.group(4))
                        placed = G._placed(drawings[m.group(1)], float(m.group(2)),
                                           float(m.group(3)), k, float(m.group(5) or k))
                        with self.subTest(shot=shot, use=m.group(0)[:50]):
                            self.assertFalse(G._meets(rect, *placed))
                for m in G._USE_AT.finditer(part):
                    if m.group(0) not in kept and m.group(1) in drawings:
                        placed = G._placed(drawings[m.group(1)], float(m.group(2)),
                                           float(m.group(3)), 1.0, 1.0)
                        with self.subTest(shot=shot, use=m.group(0)[:50]):
                            self.assertFalse(G._meets(rect, *placed))

    def test_the_engravers_dashes(self):
        """Each dash is the next on-length of FORM_DASH along the curve, each gap the next
        off-length, and every dash lies on the curve."""
        for run in ([(0.0, 0.0), (2000.0, 0.0)],
                    [(-300.0, 40.0), (0.0, -20.0), (420.0, 60.0), (900.0, 10.0), (1500.0, 90.0)]):
            curve = G._curve_points(run)
            along, at = [0.0], 0.0
            for a, b in zip(curve, curve[1:]):
                at += math.dist(a, b)
                along.append(at)

            def where(q):
                """How far along the curve a point is, and how far off it."""
                best = (math.inf, 0.0)
                for (a, b), s0 in zip(zip(curve, curve[1:]), along):
                    L = math.dist(a, b)
                    dot = (q[0] - a[0]) * (b[0] - a[0]) + (q[1] - a[1]) * (b[1] - a[1])
                    u = max(0.0, min(1.0, dot / (L * L or 1)))
                    off = math.dist(q, (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u))
                    best = min(best, (off, s0 + u * L))
                return best
            dashes = G._dashes(run)
            self.assertGreater(len(dashes), 3)
            pattern = G.FORM_DASH
            pos = 0.0
            for n, dash in enumerate(dashes):
                for q in dash:
                    self.assertLess(where(q)[0], 1e-6)
                s0, s1 = where(dash[0])[1], where(dash[-1])[1]
                on, off = pattern[(2 * n) % len(pattern)], pattern[(2 * n + 1) % len(pattern)]
                with self.subTest(run=len(run), dash=n):
                    self.assertAlmostEqual(s0, pos, places=6)
                    if abs(s1 - along[-1]) < 1e-6:          # the curve ends inside this dash
                        self.assertEqual(n, len(dashes) - 1)
                        self.assertLessEqual(s1 - s0, on + 1e-6)
                    else:
                        self.assertAlmostEqual(s1 - s0, on, places=6)
                    if n == len(dashes) - 1 and s1 < along[-1]:     # or in the gap after it
                        self.assertLess(along[-1] - s1, off + 1e-6)
                pos = s0 + on + off


class SceneOff(unittest.TestCase):
    """A plate is in by a cut while the camera is at its zoom or closer, and under it the scene is
    switched off, so a close-up costs only its own drawing. That is only right while the plate's
    own opaque ground covers the whole frame, and the plate's being in at all is only right while
    it does."""

    @staticmethod
    def schedule(fl):
        """The scene's visibility at each of the flight's keys, as written."""
        first, switch = fl.scene_visibility()
        n = len(fl.cams)
        if not switch:
            return [first] * n
        vals = re.search(r'values="([^"]*)"', switch).group(1).split(";")
        at = [round(float(k) * (n - 1)) for k in
              re.search(r'keyTimes="([^"]*)"', switch).group(1).split(";")]
        return [next(v for a, v in zip(reversed(at), reversed(vals)) if a <= i) for i in range(n)]

    def test_a_plate_cuts_in_and_the_scene_goes_inside_it(self):
        fl = S.VerseFlight((1.0, 0, 1300), [("to", (8.0, 0, 1300), 2.0), ("hold", None, 1.0),
                                             ("to", (1.0, 0, 1300), 2.0)])
        self.assertEqual(set(self.schedule(fl)), {"visible"})
        fl.plates.append((4.0, None, None))
        ins, sched = fl.keys_in(fl.plates[0]), self.schedule(fl)
        n = len(fl.cams) - 1
        for i in range(n + 1):
            with self.subTest(key=i):
                # in from a key to the next only if the camera is at its zoom at both
                self.assertEqual(ins[i], fl.cams[i][0] >= 4.0 and fl.cams[min(i + 1, n)][0] >= 4.0)
                self.assertEqual(fl.covered(i / n * fl.dur), ins[i])
                # the scene off only inside the plate's run, a key in from either end
                self.assertEqual(sched[i] == "hidden",
                                 ins[max(i - 1, 0)] and ins[i] and ins[min(i + 1, n)])
        self.assertIn("hidden", sched)
        self.assertEqual(sched[0], "visible")
        self.assertEqual(sched[-1], "visible")
        # whole or not there: no opacity between
        drawn = S.plate(S.VerseFlight(fl.cam0, [("to", (8.0, 0, 1300), 2.0), ("hold", None, 1.0),
                                                ("to", (1.0, 0, 1300), 2.0)]), "<rect/>", 4.0)
        self.assertTrue(set(re.findall(r'opacity="([^"]*)"|values="([^"]*)"', drawn)) <=
                        {("0", ""), ("1", ""), ("", "0;1;0"), ("", "hidden;visible;hidden")},
                        drawn[:200])
        # a plate that goes when the verse says so, though the camera is still close
        fl.plates[0] = (4.0, 2.5, None)
        self.assertTrue(all(v == "visible" for i, v in enumerate(self.schedule(fl))
                            if i / n * fl.dur > 2.5))
        self.assertFalse(S.VerseFlight((1.0, 0, 1300), []).covered(0.0))

    def test_a_cut(self):
        """A cut is between two keys: the camera holds the first until the second's time and is on
        the second at once, and so is everything baked on the keys, the plate with them."""
        legs = [("hold", None, 1.0), ("cut", (8.0, 40, 1300), 0.0), ("hold", None, 1.0),
                ("cut", (1.0, 0, 1300), 0.0), ("to", (1.2, 0, 1300), 1.0)]
        fl = S.VerseFlight((1.0, 0, 1300), legs)
        n = len(fl.cams) - 1
        step = fl.dur / n
        self.assertAlmostEqual(fl.dur, 3.0)
        self.assertEqual(len(fl.cut_keys), 2)
        for k, (before, after) in zip(fl.cut_keys, ((1.0, 8.0), (8.0, 1.0))):
            self.assertEqual(fl.cams[k][0], before)
            self.assertAlmostEqual(fl.cams[k + 1][0], after, places=2)
            # held through the step, and the next at once
            self.assertEqual(fl.at((k + .5) * step)[0], before)
            self.assertAlmostEqual(fl.at((k + 1) * step + 1e-6)[0], after, places=2)
        # the camera's animation repeats the key time at each cut, and is otherwise the Flight's
        anim = fl.open_camera()
        kt = re.search(r'type="scale" values="[^"]*" keyTimes="([^"]*)"', anim).group(1).split(";")
        self.assertEqual(len(kt) - len(set(kt)), 2)
        self.assertEqual(Q.key_times("3:1", anim), [])
        self.assertTrue(all(Q._baked(a, fl) for a in Q._ANIM.findall(anim)))
        # the plate is in from the cut in to the cut out, and nothing between
        fl.plates.append((4.0, None, None))
        ins = fl.keys_in(fl.plates[0])
        a, b = fl.cut_keys
        self.assertEqual([i for i, q in enumerate(ins) if q], list(range(a + 1, b + 1)))
        # an edit is not a move
        self.assertEqual(Q.camera_speed("3:1", fl), [])
        # and a leg of no length that isn't a cut is a leg a word has crossed
        cam = S.camera("alone")
        self.assertEqual(Q.camera_legs("2:18", [(1.0, 1.0, cam)], 6.0, {1.0}), [])
        self.assertTrue(Q.camera_legs("2:18", [(1.0, 1.0, cam)], 6.0))

    def test_a_plate_covers_the_frame_whenever_it_is_in(self):
        story, files = whole()
        seen = off = 0
        for ref in REFS:
            fl, svg = story.drawn[ref], files[ref]
            if not fl.plates:
                continue
            first, switch = fl.scene_visibility()
            self.assertIn(f'<g visibility="{first}">{switch}' if first == "hidden"
                          else switch, svg)
            plates = plate_grounds(svg, fl)
            n = len(fl.cams) - 1
            for i, v in enumerate(self.schedule(fl)):
                if v == "hidden":
                    off += 1
                    with self.subTest(verse=ref, key=i, scene="off"):
                        self.assertTrue(any(ins[i] and ground for ground, ins in plates))
            for ground, ins in plates:
                for i in (i for i, q in enumerate(ins) if q and ground):
                    seen += 1
                    # across a cut the camera holds the key before it
                    frames = [fl.cams[i], fl.at((i + .5) / n * fl.dur) if n else fl.cams[i]]
                    if i not in fl.cut_keys:
                        frames.append(fl.cams[min(i + 1, n)])
                    with self.subTest(verse=ref, key=i):
                        self.assertTrue(all(inside(C.visible_world(cam), ground) for cam in frames),
                                        f"{ref}: a plate is in at {i / max(n, 1) * fl.dur:.2f} s "
                                        "and its ground doesn't cover the frame")
        self.assertGreater(off, 100)
        self.assertGreater(seen, off)


_TAG = re.compile(r"<(/?)([a-zA-Z]+)\b([^>]*?)(/?)>")
_GROUND = re.compile(r'(?:<defs>.*?</defs>)?<rect x="(-?[\d.]+)" y="(-?[\d.]+)" '
                     r'width="([\d.]+)" height="([\d.]+)"', re.S)


def plate_grounds(svg, fl):
    """[(a plate's ground in world px or None, whether it is in from each camera key to the next)]
    in a verse's file, in the order the verse hung them: a plate is `garden_stage.plate`'s group,
    found by the switch its flight gives it, its ground the rect it begins with, moved by the
    translates of the groups it is in, inside the card's. 3:15's foot has no ground of its own."""
    out, at = [], svg.index('<g transform="translate(0 0) scale(1) translate(0 0)">')
    stack, scanned = [], at
    for p in fl.plates:
        ins = fl.keys_in(p)
        (op, op_an), (vis, vis_an) = fl.switch(ins, "opacity"), fl.switch(ins)
        head = f'<g opacity="{op}" visibility="{vis}">{op_an}{vis_an}'
        at = svg.index(head, at)
        for m in _TAG.finditer(svg, scanned, at):
            closing, tag, attrs, empty = m.groups()
            if closing:
                if stack and stack[-1][0] == tag:
                    stack.pop()
            elif not empty:
                t = re.search(r'transform="translate\((-?[\d.]+) (-?[\d.]+)\)"$', attrs.strip())
                stack.append((tag, (float(t.group(1)), float(t.group(2))) if t else (0.0, 0.0)))
        scanned = at
        r = _GROUND.match(svg, at + len(head))
        ground = None
        if r:
            dx, dy = sum(q[1][0] for q in stack), sum(q[1][1] for q in stack)
            x, y, w, h = (float(q) for q in r.groups())
            ground = (x + dx, y + dy, x + w + dx, y + h + dy)
        out.append((ground, ins))
    return out


class Speed(unittest.TestCase):
    def test_limits(self):
        """From the legs alone: no verse's camera is seasick."""
        for ref, v in told().verses.items():
            with self.subTest(verse=ref):
                pan, _a, zoom, _b = Q.camera_peak(v.flight())
                self.assertLessEqual(pan, Q.PAN_MAX)
                self.assertLessEqual(zoom, Q.ZOOM_MAX)


class QC(unittest.TestCase):
    def test_all_clear(self):
        """The whole story, on today's values. write_story asks the same on the clock."""
        story, files = whole()
        problems, report = Q.run(story, files, today, None)
        self.assertEqual(problems, [])
        self.assertEqual(len(report), len(REFS) + 7)

    def test_it_has_teeth(self):
        # a name moved onto a person: 2:23's "Man", down onto the man himself
        story, svg = one("2:23")
        fl = story.drawn["2:23"]
        self.assertEqual(Q.name_air(story, "2:23"), [])
        at = next(i for i, n in enumerate(fl.names) if n.text == "Man")
        fl.names[at] = fl.names[at]._replace(y=S.gy(S.M0) - 60)
        self.assertTrue(any("Man touches man" in p for p in Q.name_air(story, "2:23")))
        # a list of keyTimes that goes back, on a copy of a real file
        self.assertEqual(Q.key_times("2:23", svg), [])
        self.assertTrue(svg.count('keyTimes="0;1"') > 0)
        broken = svg.replace('keyTimes="0;1"', 'keyTimes="0;1;.5"', 1)
        self.assertTrue(Q.key_times("2:23", broken))
        # and the shape it once took in 3:16, which WebKit and Edge drop silently
        broken = svg.replace('keyTimes="0;1"', 'keyTimes="0;.250;.241;1"', 1)
        self.assertTrue(any("keyTimes 0;.250;.241;1" in p for p in Q.key_times("2:23", broken)))
        # a loop on the wrong verse, on a copy of a real file
        dur = story.verses["2:23"].dur
        self.assertEqual(Q.one_loop("2:23", svg, dur), [])
        looping = svg.replace('fill="freeze"', 'repeatCount="indefinite"', 1)
        self.assertTrue(any("loops" in p for p in Q.one_loop("2:23", looping, dur)))

    def test_a_name_cut_or_under_the_title(self):
        story, _svg = one("2:23")
        fl = story.drawn["2:23"]
        cam = fl.cam1
        at = next(i for i, n in enumerate(fl.names) if n.text == "Man")
        fl.names[at] = fl.names[at]._replace(x=cam[1] + 512 / cam[0], y=cam[2])
        self.assertTrue(any("cut by the frame" in p for p in Q.name_air(story, "2:23")))
        fl.names[at] = fl.names[at]._replace(x=cam[1] - 400 / cam[0], y=cam[2] - 265 / cam[0])
        self.assertTrue(any("under the title" in p for p in Q.name_air(story, "2:23")))
        woman = next(n for n in fl.names if n.text == "woman")
        fl.names[at] = fl.names[at]._replace(x=woman.x + 5, y=woman.y)
        self.assertTrue(any("Man touches woman" in p for p in Q.name_air(story, "2:23")))

    def test_figures_out_of_frame(self):
        story, svg = one("2:22")
        self.assertEqual(Q.figures_in_frame(story, "2:22", svg), [])
        story.card.on("2:22", ("move", "wom", 4.0, .1, (400, 0)))
        found = Q.figures_in_frame(story, "2:22", svg)
        self.assertTrue(any("wom is not wholly" in p for p in found))
        story, svg = one("3:14")
        self.assertEqual(Q.figures_in_frame(story, "3:14", svg), [])
        story.drawn["3:14"] = S.VerseFlight((1.0, 2000, 1322), [])
        found = Q.figures_in_frame(story, "3:14", svg)
        self.assertTrue(any("serpent is out of frame" in p for p in found))

    def test_a_plate_covers_them(self):
        story, svg = one("2:17")
        self.assertEqual(Q.figures_in_frame(story, "2:17", svg), [])
        story.drawn["2:17"].plates.clear()
        self.assertTrue(Q.figures_in_frame(story, "2:17", svg))

    def test_under_the_floor(self):
        story, _svg = one("2:22")
        self.assertEqual(Q.the_floor(story, "2:22")[0], [])
        story.drawn["2:22"] = S.VerseFlight((.3, -126, 1330), [])
        self.assertTrue(any("under the floor" in p for p in Q.the_floor(story, "2:22")[0]))
        # and the people drawn by hand: all the living, made smaller than the floor allows
        story, _svg = one("3:20")
        fl = story.drawn["3:20"]
        self.assertEqual(len(fl.figures), len(G3.LIVING))
        self.assertEqual(Q.the_floor(story, "3:20")[0], [])
        fl.figures[:] = [f._replace(k=.3) for f in fl.figures]
        self.assertTrue(any("the living is" in p for p in Q.the_floor(story, "3:20")[0]))

    def test_the_budget(self):
        story, svg = one("3:9")
        self.assertEqual(Q.budget("3:9", svg)[0], [])
        self.assertTrue(Q.budget("3:9", svg + " " * (Q.MAX_KB * 1024))[0])
        self.assertTrue(Q.budget("3:9", svg + "<set/>" * Q.MAX_ANIMS)[0])
        self.assertTrue(Q.budget("3:9", svg + "<text/>" * Q.MAX_TEXTS)[0])

    def test_still_time_and_stills_anywhere(self):
        story, svg = one("3:9")
        self.assertEqual(Q.check_verse(story, "3:9", svg, today("3:9"))[0], [])
        story.verses["3:9"].dur += 2.5
        found = Q.check_verse(story, "3:9", svg, today("3:9"))[0]
        self.assertTrue(any("still after its last motion" in p for p in found))
        self.assertTrue(any("nothing moves" in p for p in found))
        # the verse that rests is let rest
        story, svg = one("2:2")
        self.assertEqual(Q.check_verse(story, "2:2", svg, today("2:2"))[0], [])

    def test_the_chapters_share_of_still_time(self):
        story, svg = one("3:9")
        story.verses["3:9"].dur += 1.4
        problems = Q.run(story, {"3:9": svg}, today, None)[0]
        self.assertTrue(any("the chapters" in p for p in problems))

    def test_stills_read_the_motion_not_the_keys(self):
        """A key list that holds isn't moving, and the water doesn't count."""
        held = ('<animate attributeName="x" values="1;1;2" keyTimes="0;.5;1" begin="2s" dur="2s" '
                'fill="freeze"/>')
        self.assertEqual(Q._moving(held), [(3.0, 4.0)])
        self.assertEqual(Q.still_time(f"<svg>{held}</svg>", 6.0), (2.0, 2.0))
        water = f'<animate values="0;9" begin="0s" dur="6s" {Q._WATER}/>'
        self.assertEqual(Q.still_time(f"<svg>{held}{water}</svg>", 6.0), (0.0, 2.0))

    def test_the_camera_too_fast(self):
        far = S.VerseFlight((1.0, 0, 1300), [("to", (1.0, 3000, 1300), 1.0)])
        self.assertTrue(any("pans" in p for p in Q.camera_speed("3:1", far)))
        deep = S.VerseFlight((.5, 0, 1300), [("to", (8.0, 0, 1300), 1.0)])
        self.assertTrue(any("zooms" in p for p in Q.camera_speed("3:1", deep)))
        calm = S.VerseFlight((1.0, 0, 1300), [("to", (1.0, 100, 1300), 2.0)])
        self.assertEqual(Q.camera_speed("3:1", calm), [])

    def test_a_leg_crossed_by_a_rerendered_word(self):
        cam = S.camera("alone")
        v = told().verses["2:18"]
        self.assertEqual(Q.camera_legs("2:18", v.keys, 6.41, v.cuts), [])
        self.assertTrue(any("backward" in p for p in Q.camera_legs("2:18", [(2.0, 1.0, cam)], 6.0)))
        crossed = [(0.0, 2.0, cam), (1.0, 3.0, cam)]
        self.assertTrue(any("before the last" in p for p in Q.camera_legs("2:18", crossed, 6.0)))
        self.assertTrue(any("after the narration" in p
                            for p in Q.camera_legs("2:18", [(0.0, 7.0, cam)], 6.0)))

    def test_a_verse_that_runs_past_its_narration(self):
        story, svg = one("3:9")
        dur = story.verses["3:9"].dur
        self.assertEqual(Q.one_loop("3:9", svg, dur), [])
        self.assertTrue(any("after the narration" in p for p in Q.one_loop("3:9", svg, dur - 2)))
        self.assertTrue(any("wheel" in p for p in Q.one_loop("3:24", "<svg/>", 9.0)))

    def test_something_begins_on_his_name(self):
        story, svg = one("2:18")
        windows = today("2:18")
        self.assertEqual(Q.his_name(story, "2:18", svg, windows), [])

        def with_(a):
            return Q.his_name(story, "2:18", svg.replace("</svg>", a + "</svg>"), windows)
        self.assertTrue(with_('<animate attributeName="opacity" values="0;1" begin="0.40s" '
                              'dur="1s" fill="freeze"/>'))
        # a thing that comes by a <set>, or by a switch, comes all the same
        self.assertTrue(with_('<set attributeName="visibility" to="visible" begin="0.40s"/>'))
        self.assertTrue(with_('<animate attributeName="visibility" values="hidden;visible" '
                              'keyTimes="0;.2" calcMode="discrete" begin="0s" dur="2s" '
                              'fill="freeze"/>'))
        # a key list that holds hasn't begun, though it begins with the verse: it is the camera's
        # only if it is baked on the camera's keys
        self.assertTrue(with_('<animate attributeName="opacity" values="0;0;1" keyTimes="0;.2;1" '
                              'begin="0s" dur="2s" fill="freeze"/>'))
        self.assertEqual(with_('<animate attributeName="opacity" values="0;0;1" keyTimes="0;.9;1" '
                               'begin="0s" dur="2.00s" fill="freeze"/>'), [])
        fl = story.drawn["2:18"]
        line = ";".join(f"{S.key_w(c[0]):.3g}" for c in fl.cams)
        self.assertEqual(with_(f'<animate attributeName="stroke-width" values="{line}" '
                               f'dur="{fl.dur:.2f}s" begin="0s" fill="freeze"/>'), [])
        story.verses["2:18"].keys = [(.4, 1.0, S.camera("alone"))]
        self.assertTrue(any("camera leg" in p for p in Q.his_name(story, "2:18", svg, windows)))

    def test_what_may_carry_on_through_his_name(self):
        """2:21's beasts walk on from 2:20 under his name; 2:9's trees go on rising. Nothing else
        that moves them may begin there."""
        story, files = whole()
        for ref in ("2:9", "2:21"):
            with self.subTest(verse=ref):
                self.assertEqual(Q.his_name(story, ref, files[ref], today(ref)), [])
        svg = files["2:21"]
        walks = Q._under_way(story, "2:21", svg)
        self.assertEqual(len(walks), len(BEASTS))
        w0, _w1 = today("2:21")[0]
        new = S.Stage.move_anim(w0, 1.0, (40, 0, S.STEADY))
        self.assertTrue(Q.his_name(story, "2:21", svg.replace("</svg>", new + "</svg>"),
                                   today("2:21")))
        svg = files["2:9"]
        w0, _w1 = today("2:9")[0]
        rock = G._grow_use("ra", 0, 0, 1.0, False, w0, 1.0)
        tree = G._grow_use("o", 0, 0, 1.0, False, w0, 1.0)
        self.assertTrue(Q.his_name(story, "2:9", svg.replace("</svg>", rock + "</svg>"),
                                   today("2:9")))
        self.assertEqual(Q.his_name(story, "2:9", svg.replace("</svg>", tree + "</svg>"),
                                    today("2:9")), [])

    def test_a_thing_that_turns_back_on_his_name(self):
        """Inside one key list, a thing that is moved and turns back, or sets off again after a
        hold, begins anew: 3:1's head drawing back on "God". A fade in, a hold and a fade out are
        one beat."""
        story, svg = one("3:1")
        windows = today("3:1")
        self.assertEqual(Q.his_name(story, "3:1", svg, windows), [])
        w0, w1 = windows[-1]
        b = f'begin="{(w0 + w1) / 2 - 1:.2f}s" dur="2.00s" fill="freeze"/></svg>'
        back = f'<animate attributeName="x" values="0;5;0" keyTimes="0;.5;1" {b}'
        self.assertTrue(Q.his_name(story, "3:1", svg.replace("</svg>", back), windows))
        again = ('<animateTransform attributeName="transform" type="translate" '
                 f'values="0 0;5 0;5 0;9 0" keyTimes="0;.25;.5;1" {b}')
        self.assertTrue(Q.his_name(story, "3:1", svg.replace("</svg>", again), windows))
        pulse = f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.25;.5;1" {b}'
        self.assertEqual(Q.his_name(story, "3:1", svg.replace("</svg>", pulse), windows), [])

    def test_a_pose_off_the_list(self):
        card = S.build_story(say=None).card
        S.pose(card, "2:18", "man", 2.0, arms="raise")
        self.assertTrue(any("not on the list" in p for p in Q.poses_on_the_list(card)))
        card = S.build_story(say=None).card
        card.events["3:7"] = [e for e in card.events["3:7"] if e[0] != "pose" or e[1] != "wom"]
        self.assertTrue(any("isn't told" in p for p in Q.poses_on_the_list(card)))

    def test_a_pose_away_from_its_word(self):
        card = told().card
        self.assertEqual(Q.poses_on_the_list(card, lambda ref, word: [t for r, k, _c, t in
                                                                      Q.pose_events(card)
                                                                      if r == ref]), [])
        self.assertTrue(Q.poses_on_the_list(card, lambda ref, word: [99.0]))

    def test_file_rules(self):
        story, svg = one("3:9")
        fl = story.drawn["3:9"]
        self.assertEqual(Q.file_rules("3:9", svg, fl), [])
        for bad in ("<filter/>", "<mask/>", "<script/>", "<style/>", "<image/>", "<tspan/>",
                    '<use xlink:href="#a"/>', '<use href="http://example.com/a"/>',
                    '<use href="#nothing"/>', '<rect fill="url(#nothing)"/>', "<a id=", "<text/>"):
            with self.subTest(bad=bad):
                self.assertTrue(Q.file_rules("3:9", svg.replace("</svg>", bad + "</svg>"), fl))
        self.assertTrue(Q.file_rules("3:9", svg.replace('width="1024"', 'width="800"', 1), fl))
        dup = svg.replace("</svg>", '<defs><g id="x1"/><g id="x1"/></defs></svg>')
        self.assertTrue(any("used twice" in p for p in Q.file_rules("3:9", dup, fl)))

    def test_key_times_and_their_neighbours(self):
        ok = '<animate values="0;1;2" keyTimes="0;.5;1" keySplines="0 0 1 1;0 0 1 1"/>'
        self.assertEqual(Q.key_times("2:1", ok), [])
        self.assertEqual(Q.key_times("2:1", '<animate values="a;b" keyTimes="0;.5" '
                                            'calcMode="discrete"/>'), [])
        for bad in ('<animate values="0;1;2" keyTimes="0;1"/>',
                    '<animate values="0;1" keyTimes=".1;1"/>',
                    '<animate values="0;1" keyTimes="0;.5"/>',
                    '<animate values="0;1;2" keyTimes="0;.5;1" keySplines="0 0 1 1"/>',
                    '<animateMotion keyPoints="0;1;1" keyTimes="0;1"/>',
                    '<animate values="0;1" begin="1s" dur="-0.40s"/>'):
            with self.subTest(bad=bad):
                self.assertTrue(Q.key_times("2:1", bad))

    def test_it_writes_nothing_if_anything_fails(self):
        story = mock.Mock(verses={"2:1": None})
        story.verse_file.return_value = "<svg/>"

        def no_writing(*_args):
            raise AssertionError("it tried to write")
        with (mock.patch.object(S, "build_story", return_value=story),
              mock.patch.object(Q, "run", return_value=(["2:1: broken"], [])),
              mock.patch.object(S, "out_path", no_writing),
              mock.patch("builtins.print")):
            self.assertEqual(S.write_story(), [])

    def test_it_writes_both_chapters(self):
        """Chapter 3 opens where chapter 2 ends, so a change to either can move the other: they are
        written together, whichever generator runs."""
        story = mock.Mock(verses=dict.fromkeys(REFS))
        story.verse_file.side_effect = lambda ref: f"<svg>{ref}</svg>"
        with (tempfile.TemporaryDirectory() as out,
              mock.patch.object(S, "build_story", return_value=story),
              mock.patch.object(Q, "run", return_value=([], [])),
              mock.patch("builtins.print")):
            paths = S.write_story(out)
            self.assertEqual(sorted(os.listdir(out)),
                             sorted(f"Genesis_{c}_{v}.svg" for c, v in map(S.cv, REFS)))
            with open(os.path.join(out, "Genesis_3_24.svg"), encoding="utf-8") as f:
                self.assertEqual(f.read(), "<svg>3:24</svg>")
        self.assertEqual(len(paths), len(REFS))


class Palette(unittest.TestCase):
    def test_values(self):
        """Genesis 1 and Numbers 1-2 import these, and their bytes hang on them."""
        from generate_genesis2_svg import EARTH, GREEN, GREEN_DIM, _mix, garden_paint
        self.assertEqual(GREEN, (86, 122, 78))
        self.assertEqual(GREEN_DIM, (52, 70, 50))
        self.assertEqual(EARTH, (58, 48, 38))
        self.assertEqual(_mix((0, 0, 0), (10, 20, 30), .5), (5, 10, 15))
        lit, plain, dead = garden_paint(True), garden_paint(False), garden_paint(False, True)
        self.assertEqual(plain["wood"], (_mix(BG, BROWN, .62), BROWN, 1.4))
        self.assertEqual(lit["wood"][1], GOLD)
        self.assertEqual(plain["fleece"], (_mix(BG, GREEN, .55), GREEN_DIM, 1.5))
        self.assertEqual(lit["fleece"], (_mix(BG, GREEN, .55), HL, 2.5))
        self.assertEqual(dead["fleece"][0], _mix(BG, EARTH, .55))
        self.assertEqual(plain["fruit"], (_mix(BG, GOLD, .75), GOLD, 1.0))

    def test_its_import_stays_cheap(self):
        code = ("import sys, generate_genesis2_svg, generate_genesis3_svg; "
                "sys.exit(any(m in sys.modules for m in "
                "('garden_stage', 'garden_art', 'soundfile')))")
        self.assertEqual(subprocess.run([sys.executable, "-c", code]).returncode, 0)


if __name__ == "__main__":
    unittest.main()
