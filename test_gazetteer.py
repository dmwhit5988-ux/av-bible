"""The Land of Israel gazetteer: its places sit in the atlas, each verse
names its place, its lines are point facts that meet where they should, and
none of them is a point of the old atlas-traced maps.

    .venv\\Scripts\\python.exe -m unittest test_gazetteer
"""

import inspect
import re
import unittest

import gazetteer as GZ
import generate_acts1518_svg
import generate_israel_atlas as A
import generate_tribal_maps

ALL = {**GZ.SITES, **GZ.JERUSALEM, **GZ.BEYOND}
TRIBES = {k.split()[0] for k in A.ALLOTMENT}


class Places(unittest.TestCase):
    def test_in_the_atlas(self):
        for key, s in {**GZ.SITES, **GZ.JERUSALEM}.items():
            with self.subTest(key):
                self.assertTrue(A.LAT_BOT < s.lat < A.LAT_TOP
                                and A.LON_L < s.lon < A.LON_R)

    def test_fields(self):
        for key, s in ALL.items():
            with self.subTest(key):
                self.assertIn(s.certainty, (GZ.KNOWN, GZ.PROBABLE, GZ.POSSIBLE))
                self.assertIn(s.kind, ("town", "mount", "valley", "plain", "cave",
                                       "well", "spring", "pool"))
                self.assertRegex(s.qid, r"^Q\d+$")
                self.assertTrue(s.modern)
                self.assertFalse(set(s.tribe) - TRIBES)

    def test_card_text_is_for_readers(self):
        """Working notes (code keys, Wikidata ids, coordinates) go in
        `source`, not in the text a card shows."""
        for key, s in ALL.items():
            for field in ("modern", "why", "namesakes", "point"):
                with self.subTest(key=key, field=field):
                    self.assertNotRegex(getattr(s, field),
                                        r"\b[a-z]+_[a-z_]+\b|\bQ\d+|P625|\d+\.\d{3}")

    def test_named_in_the_web(self):
        for key, s in ALL.items():
            with self.subTest(key):
                self.assertTrue(A.in_web(s.name), s.name)

    def test_each_verse_names_its_place(self):
        """A ref is a verse with the place's name in it, or one of its
        other names (Luz, Kiriath Arba)."""
        for key, s in ALL.items():
            pat = re.compile(A.names_pattern(A.site_names(s)))
            for v in A.verses(s.refs):
                with self.subTest(key=key, verse=v):
                    self.assertRegex(A.TEXT_WEB[v], pat)

    def test_skips_are_found_and_not_checked_refs(self):
        """A skipped verse is one the place's names find, and never one of
        its checked refs."""
        for key, s in ALL.items():
            found = {v for n in A.site_names(s) for v in A.word_verses(n)}
            skip = set(A.verses(s.skip))
            with self.subTest(key):
                self.assertFalse(skip - found, "skips nothing finds")
                self.assertFalse(skip & set(A.verses(s.refs)), "skips a checked ref")

    def test_one_place_a_point(self):
        """No two drawn places share a point (a duplicate, Lod and Lydda,
        is one place with two names)."""
        seen = {}
        for key, s in GZ.SITES.items():
            p = (round(s.lat, 3), round(s.lon, 3))
            with self.subTest(key):
                self.assertNotIn(p, seen, f"{key} and {seen.get(p)}")
            seen[p] = key


def _gazetteer_lines():
    """Every point line of the module's own lists, as source text."""
    src = inspect.getsource(GZ)
    names = ["COAST_SOUTH", "GALILEE", "HULEH", "SALT_SEA", "HASBANI", "DAN", "BANIAS",
             "JORDAN_UPPER", "JORDAN_LOWER", "YARMUK", "JABBOK", "ARNON", "ZERED",
             "KISHON", "YARKON", "BROOK_OF_EGYPT"]
    out = []
    for n in names:
        body = re.search(r"\n%s = \[\n(.*?)\n\]" % n, src, re.S).group(1)
        out += [(n, ln) for ln in body.split("\n") if ln.strip()]
    return out


def _traced_points():
    """The old maps' atlas-traced geometry, which no point may copy."""
    pts = set()

    def walk(x):
        if isinstance(x, tuple) and len(x) == 2 and all(isinstance(v, float) for v in x):
            pts.add((round(x[0], 3), round(x[1], 3)))
        elif isinstance(x, (list, tuple)):
            for y in x:
                walk(y)
        elif isinstance(x, dict):
            for y in x.values():
                walk(y)
    for mod, names in ((generate_tribal_maps, ("COAST", "COAST_WEST", "LAKES", "RIVERS",
                                               "TRIBE_RINGS", "GULF_SUEZ", "GULF_AQABA",
                                               "RED_SEA")),
                       (generate_acts1518_svg, ("MED", "PELOPONNESE", "ISLANDS"))):
        for n in names:
            walk(getattr(mod, n))
    return pts


class Lines(unittest.TestCase):
    def test_every_point_is_a_point_fact(self):
        """Each point names its place and its Wikidata item, or is marked
        '~' as our own interpolation."""
        for name, ln in _gazetteer_lines():
            with self.subTest(list=name, line=ln.strip()):
                self.assertRegex(ln, r"^\s+\([\d.]+, [\d.]+\),\s+# (~ .+|.+\(Q\d+\))$")

    def test_no_point_copies_a_traced_map(self):
        traced = _traced_points()
        lines = [GZ.COAST_SOUTH, *GZ.LAKES.values(), *GZ.RIVERS.values()]
        for p in (q for line in lines for q in line):
            with self.subTest(point=p):
                self.assertNotIn((round(p[0], 3), round(p[1], 3)), traced)

    def test_rivers_meet_their_water(self):
        """A river's mouth is a point of the coast, a lake or a river, so
        the lines join."""
        points = set(GZ.COAST) | {p for ring in GZ.LAKES.values() for p in ring}
        for key, line in GZ.RIVERS.items():
            others = {p for k, ln in GZ.RIVERS.items() if k != key for p in ln}
            with self.subTest(key):
                self.assertIn(line[-1], points | others)

    def test_the_coast_runs_off_the_sheet(self):
        self.assertGreater(GZ.COAST[0][0], A.LAT_TOP)
        self.assertLess(GZ.COAST[-1][1], A.LON_L + 0.01)

    def test_waters_and_lands_are_found(self):
        for key, x in {**GZ.WATERS, **GZ.REGIONS}.items():
            if x.find:
                with self.subTest(key):
                    self.assertTrue(A.finds(x.find, x.skip))


if __name__ == "__main__":
    unittest.main()
