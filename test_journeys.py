"""Paul's journeys: its places sit on the sheet, each verse names its place,
the stops, roads, courses and letters hang together, the coasts are point
facts that meet where they should and copy no atlas-traced map, and a
voyage keeps to the sea.

    .venv\\Scripts\\python.exe -m unittest test_journeys
"""

import inspect
import math
import re
import unittest

import acts_geography as G
import gazetteer as GZ
import generate_israel_atlas as A
import generate_journeys_reference as R
import journeys as J
import mediterranean as M
import verse_refs
from books import BOOK_NAMES
from test_gazetteer import _traced_points

POINT = r"^\s+\([\d.]+, [\d.]+\),\s+# (~( .+)?|.+\(Q\d+\))$"


def curve(d, n=16):
    """Points along a path of M, L and C commands (A.smooth's)."""
    toks = re.findall(r"[MLC]|-?[\d.]+,-?[\d.]+", d)
    pts, i = [], 0
    while i < len(toks):
        t = toks[i]
        xy = lambda k: tuple(map(float, toks[i + k].split(",")))
        if t in "ML":
            q = xy(1)
            if t == "L":
                pts += [(pts[-1][0] + (q[0] - pts[-1][0]) * u / n,
                         pts[-1][1] + (q[1] - pts[-1][1]) * u / n) for u in range(1, n)]
            pts.append(q)
            i += 2
        else:
            p0, c1, c2, q = pts[-1], xy(1), xy(2), xy(3)
            pts += [tuple((1 - u) ** 3 * a + 3 * (1 - u) ** 2 * u * b + 3 * (1 - u) * u ** 2 * c
                          + u ** 3 * e for a, b, c, e in zip(p0, c1, c2, q))
                    for u in (k / n for k in range(1, n + 1))]
            i += 4
    return pts


def names(p):
    """A place's WEB names: its name and its other names."""
    return re.compile(A.names_pattern([p.name] + list(p.aka)))


class Places(unittest.TestCase):
    def test_on_the_sheet(self):
        for key, p in J.PLACES.items():
            with self.subTest(key):
                self.assertTrue(R.LAT_BOT < p.lat < R.LAT_TOP and R.LON_L < p.lon < R.LON_R)

    def test_fields(self):
        roles = {"journey1", "journey2", "journey3", "rome", "other_acts", "letter_to",
                 "letter_from", "assembly_rev"}
        for key, p in J.PLACES.items():
            with self.subTest(key):
                self.assertIn(p.certainty, (J.KNOWN, J.PROBABLE, J.POSSIBLE))
                self.assertRegex(p.qid, r"^Q\d+$")
                self.assertTrue(p.modern)
                self.assertFalse(set(p.roles) - roles)

    def test_card_text_is_for_readers(self):
        """Working notes (code keys, Wikidata ids, coordinates) go in
        `source`, not in the text a card shows."""
        for key, p in J.PLACES.items():
            for field in ("modern", "why", "region", "letters", "note", "point"):
                with self.subTest(key=key, field=field):
                    self.assertNotRegex(getattr(p, field),
                                        r"\b[a-z]+_[a-z_]+\b|\bQ\d+|P625|\d+\.\d{3}")

    def test_each_verse_names_its_place(self):
        for key, p in J.PLACES.items():
            pat = names(p)
            for v in A.verses(p.refs):
                with self.subTest(key=key, verse=v):
                    self.assertRegex(A.TEXT_WEB[v], pat)

    def test_skips_are_found_and_not_checked_refs(self):
        for key, p in J.PLACES.items():
            found = {v for n in R.place_names(p) for v in A.word_verses(n)}
            skip = set(A.verses(p.skip))
            with self.subTest(key):
                self.assertFalse(skip - found, "skips nothing finds")
                self.assertFalse(skip & set(A.verses(p.refs)), "skips a checked ref")

    def test_a_shared_name_is_not_searched(self):
        """Two places of one name (the Antiochs) take only their refs."""
        by = {}
        for key, p in J.PLACES.items():
            by.setdefault(p.name.split(" of ")[0], []).append(key)
        for keys in by.values():
            if len(keys) > 1:
                for k in keys:
                    with self.subTest(k):
                        self.assertFalse(J.PLACES[k].search)


class Journeys(unittest.TestCase):
    def test_stops(self):
        for jk, j in J.JOURNEYS.items():
            self.assertEqual(j.stops[0].by, "start", jk)
            for a, s in zip(j.stops, j.stops[1:]):
                with self.subTest(journey=jk, stop=s.place, ref=s.ref):
                    self.assertIn(s.place, {**J.PLACES, **J.REGIONS})
                    self.assertIn(s.by, ("land", "sea"))
                    self.assertNotEqual(a.place, s.place)
                    self.assertTrue(not s.via or s.via in J.ROADS or s.via in J.COURSES)
                    self.assertTrue(A.verses(s.ref))

    def test_a_road_runs_between_its_stops(self):
        """A leg on a road starts and ends near the road: within 6 km."""
        for jk, i, a, s, line in R.legs():
            if s.via in J.ROADS:
                pts = J.ROADS[s.via].points
                for end in (line[0], line[-1]):
                    with self.subTest(journey=jk, leg=i, end=end):
                        self.assertLess(min(R.km_along([end, q]) for q in pts), 6)

    def test_a_named_stop_is_in_its_verses(self):
        """A stop the text names (`certain`) is named in its verses."""
        for jk, j in J.JOURNEYS.items():
            for s in j.stops:
                if s.place in J.PLACES and s.certain and s.by != "start":
                    vs = A.verses(s.ref)
                    with self.subTest(journey=jk, stop=s.place):
                        self.assertTrue(any(names(J.PLACES[s.place]).search(A.TEXT_WEB[v])
                                            for v in vs))

    def test_voyages_keep_to_the_sea(self):
        """A leg by sea, as drawn, crosses no more than 6 km of land between
        leaving the shore and reaching it again (Beroea, Perga, Athens,
        Ephesus and Miletus stand inland, and the line runs to them)."""
        rings = [R.PROJ.PS(r) for r in R.land_rings() + R.ISLANDS]
        for jk, i, a, s, line in R.legs():
            if s.by != "sea":
                continue
            pts = curve(A.smooth(R.drawn(jk, i, line)))
            steps = [(any(A.inside(x, y, r) for r in rings), math.dist(p, (x, y)) / R.KM)
                     for p, (x, y) in zip(pts, pts[1:])]
            sea = [k for k, (on, _d) in enumerate(steps) if not on]
            land = sum(d for on, d in steps[sea[0]:sea[-1]] if on) if sea else 0
            with self.subTest(journey=jk, leg=f"{R.stop_name(a)} to {R.stop_name(s)}"):
                self.assertLess(land, 6)


class Letters(unittest.TestCase):
    def test_letters(self):
        for lt in J.LETTERS:
            with self.subTest(lt.name):
                self.assertIn(lt.name, BOOK_NAMES)
                text = " ".join(A.TEXT_WEB[v] for v in A.verses(lt.to_ref))
                for k in lt.to:
                    p = J.PLACES.get(k) or J.REGIONS[k]
                    self.assertRegex(text, names(p))
                if lt.written:
                    w = J.PLACES[lt.written]
                    self.assertIn("letter_from", w.roles)
                    self.assertRegex(" ".join(A.TEXT_WEB[v] for v in A.verses(lt.written_ref)),
                                     names(w))

    def test_assemblies(self):
        self.assertEqual(len(J.ASSEMBLIES), 7)
        for key, ref in J.ASSEMBLIES:
            with self.subTest(key):
                self.assertIn("assembly_rev", J.PLACES[key].roles)
                self.assertRegex(A.TEXT_WEB[A.verses(ref)[0]], names(J.PLACES[key]))

    def test_lands_and_waters_are_found(self):
        for key, r in {**J.REGIONS, **J.WATERS}.items():
            with self.subTest(key):
                self.assertTrue(R.finds_nt(r.find))


def _lists(mod, names):
    src = inspect.getsource(mod)
    out = []
    for n in names:
        body = re.search(r"\n    \"?%s\"?(?: = |: )\[\n(.*?)\n    ?\]" % n, src, re.S) or \
            re.search(r"\n%s = \[\n(.*?)\n\]" % n, src, re.S)
        out += [(n, ln) for ln in body.group(1).split("\n") if ln.strip().startswith("(")]
    return out


class Lines(unittest.TestCase):
    def test_every_point_is_a_point_fact(self):
        """Each coast, road and course point names its place and its
        Wikidata item, or is marked '~' as our own."""
        lines = _lists(M, ["ASIA_NORTH", "ASIA_WEST", "GREECE_WEST", "GREECE_EAST", "ITALY",
                           "AFRICA"] + [k.upper() for k in M.ISLANDS])
        lines += _lists(J, [k.upper() for k in ("via_egnatia", "thessalonica_beroea",
                                                "troas_assos", "puteoli_rome",
                                                "antioch_derbe", "antioch_ephesus",
                                                "caesarea_jerusalem",
                                                "ptolemais_caesarea")])
        lines += _lists(J, list(J.COURSES))
        self.assertGreater(len(lines), 2500)
        for name, ln in lines:
            with self.subTest(list=name, line=ln.strip()):
                self.assertRegex(ln, POINT)

    def test_no_point_copies_a_traced_map(self):
        traced = _traced_points()
        for n in ("AEGEAN_SHORE", "LIBYA_SHORE", "PELOPONNESE", "FAR_ISLANDS"):
            for line in getattr(G, n) if n == "FAR_ISLANDS" else [getattr(G, n)]:
                traced |= {(round(a, 3), round(b, 3)) for a, b in line}
        ours = [*M.ISLANDS.values(), M.ASIA_NORTH, M.ASIA_WEST, M.GREECE_WEST, M.GREECE_EAST,
                M.ITALY, M.AFRICA, *(r.points for r in J.ROADS.values()), *J.COURSES.values()]
        for p in (q for line in ours for q in line):
            with self.subTest(point=p):
                self.assertNotIn((round(p[0], 3), round(p[1], 3)), traced)

    def test_the_coasts_meet(self):
        self.assertEqual(M.ASIA_NORTH[-1], M.ASIA_WEST[0])
        self.assertEqual(M.ASIA_WEST[-1], G.MAIN_COAST[0])
        self.assertEqual(M.AFRICA[0], GZ.COAST_SOUTH[-1])
        self.assertLess(R.km_along([M.GREECE_WEST[-1], M.GREECE_EAST[0]]), 7)   # the Isthmus

    def test_the_coasts_run_off_the_sheet(self):
        self.assertGreater(M.ASIA_NORTH[0][1], R.LON_R)
        self.assertLess(M.AFRICA[-1][1], R.LON_L)
        for line in (M.GREECE_WEST[0], M.GREECE_EAST[-1], M.ITALY[0], M.ITALY[-1]):
            self.assertGreater(line[0], R.LAT_TOP)


if __name__ == "__main__":
    unittest.main()
