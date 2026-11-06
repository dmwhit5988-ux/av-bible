"""The Near East beyond the Levant: every point of its lines is a point fact,
none copies an atlas-traced map, the lines meet where they should and run off
the Acts 7 map's sheet, the rivers run downhill to the sea, and each place's
verses name it.

    .venv\\Scripts\\python.exe -m unittest test_near_east
"""

import inspect
import math
import re
import unittest

import generate_israel_atlas as A
import mediterranean as M
import near_east as NE
from test_gazetteer import _traced_points

POINT = r"^\s+\([\d.]+, [\d.]+\),\s+# (~( .+)?|.+\(Q\d+\))$"

# the Acts 7 map's drawn world (generate_acts7_svg.WORLD_LAT, WORLD_LON)
LAT, LON = (26.4, 38.6), (20.5, 48.8)


def inside(p):
    return LAT[0] < p[0] < LAT[1] and LON[0] < p[1] < LON[1]


class Lines(unittest.TestCase):
    def test_every_point_is_a_point_fact(self):
        """Each point of a line is one named place's coordinate (its Wikidata
        item in the comment) or marked ~ as our own."""
        src = inspect.getsource(NE)
        for name in list(NE.COASTS) + list(NE.RIVERS):
            const = name.upper()
            m = re.search(rf"^{const} = \[\n(.*?)^\]", src, re.M | re.S)
            self.assertIsNotNone(m, const)
            for line in m.group(1).splitlines():
                with self.subTest(const=const, line=line):
                    self.assertRegex(line, POINT)

    def test_no_point_copies_a_traced_map(self):
        traced = _traced_points()
        for name, pts in list(NE.COASTS.items()) + list(NE.RIVERS.items()):
            for p in pts:
                with self.subTest(name=name, p=p):
                    self.assertNotIn((round(p[0], 3), round(p[1], 3)), traced)

    def test_the_lines_meet(self):
        mouths = {(round(a, 4), round(b, 4)) for a, b in M.AFRICA}
        self.assertIn(NE.NILE_ROSETTA[-1], mouths)
        self.assertIn(NE.NILE_DAMIETTA[-1], mouths)
        self.assertEqual(NE.NILE_ROSETTA[0], NE.NILE[-1])
        self.assertEqual(NE.NILE_DAMIETTA[0], NE.NILE[-1])
        self.assertEqual(NE.RED_SEA_WEST[-1], NE.RED_SEA_EAST[0])
        self.assertEqual(NE.EUPHRATES[-1], NE.TIGRIS[-1])
        self.assertEqual(NE.SHATT_AL_ARAB[0], NE.EUPHRATES[-1])
        self.assertIn(NE.SHATT_AL_ARAB[-1], NE.GULF_HEAD)
        self.assertIn(NE.BALIKH[-1], NE.EUPHRATES)

    def test_the_coasts_run_off_the_sheet(self):
        for name, pts in NE.COASTS.items():
            with self.subTest(name):
                self.assertFalse(inside(pts[0]) and inside(pts[-1]))
        self.assertFalse(inside(NE.RED_SEA_WEST[0]))
        self.assertFalse(inside(NE.RED_SEA_EAST[-1]))
        self.assertFalse(inside(NE.GULF_HEAD[0]))
        self.assertFalse(inside(NE.GULF_HEAD[-1]))

    def test_no_long_jumps(self):
        """Neighbouring points are under 2.2 degrees apart, so no stretch of a
        line is a long straight guess."""
        for name, pts in list(NE.COASTS.items()) + list(NE.RIVERS.items()):
            for a, b in zip(pts, pts[1:]):
                with self.subTest(name=name, a=a):
                    self.assertLess(math.dist(a, b), 2.2)

    def test_no_point_twice_in_a_row(self):
        for name, pts in list(NE.COASTS.items()) + list(NE.RIVERS.items()):
            for a, b in zip(pts, pts[1:]):
                with self.subTest(name=name, a=a):
                    self.assertNotEqual(a, b)


class Places(unittest.TestCase):
    def test_on_the_sheet(self):
        for key, p in NE.SITES.items():
            with self.subTest(key):
                self.assertTrue(inside((p.lat, p.lon)))
        for key, r in NE.REGIONS.items():
            with self.subTest(key):
                self.assertTrue(inside((r.lat, r.lon)))

    def test_fields(self):
        for key, p in NE.SITES.items():
            with self.subTest(key):
                self.assertIn(p.certainty, (NE.KNOWN, NE.PROBABLE, NE.POSSIBLE))
                self.assertRegex(p.qid, r"^Q\d+$")
                self.assertTrue(p.modern)
                self.assertTrue(p.why)

    def test_each_verse_names_its_place(self):
        """Every verse in a place's refs names it, by its name or one of its
        other names (or, for a people, their name: Alexandrians)."""
        for key, p in NE.SITES.items():
            names = [p.name] + list(p.aka)
            pat = re.compile("|".join(r"\b" + re.escape(n.split()[0])
                                      for n in names))
            for v in A.verses(p.refs):
                with self.subTest(key=key, verse=v):
                    self.assertRegex(A.TEXT_WEB[v], pat)


if __name__ == "__main__":
    unittest.main()
