"""The kings, prophets, foreign kings and judges of the Kings and prophets page:
Ussher's years are chronology.BIND's, each verse says what it is cited for,
and every name ties to its reign.

    .venv\\Scripts\\python.exe -m unittest test_kings
"""

import glob
import json
import os
import re
import unittest

import chronology as C
import generate_kings_reference as G
import kings as K
import prophets as PR
import verse_refs
from config import BIBLES_DIR

TEXT = {}
for _p in glob.glob(os.path.join(BIBLES_DIR, "WEB", "*.json")):
    _d = json.load(open(_p, encoding="utf-8"))
    for _n, _t in _d["verses"]:
        TEXT[(_d["book"], _d["chapter"], int(_n))] = _t


def words(ref):
    return " ".join(TEXT[v] for r in verse_refs.parse(ref, "Genesis") for v in r.verses())


def first(s):
    return re.match(r"[\w’']+", s).group(0)


def says(ref, *names):
    t = words(ref)
    return any(re.search(r"\b" + re.escape(n) + r"\b", t, re.I) for n in names if n)


class Reigns(unittest.TestCase):
    def test_ussher_is_bind(self):
        """Every reign chronology.BIND dates is a reign here of that name,
        with the same years: the house count is typed once."""
        for loc, x in C.BIND:
            if x.kind == "reign":
                years = (C.bc(x.t0), C.bc(x.t1))
                with self.subTest(loc[-1]):
                    self.assertTrue(any(r.ussher == years and loc[-1] in (r.name, *r.aka)
                                        for r in K.REIGNS.values()), (loc[-1], years))

    def test_orders_and_years(self):
        for realm in ("united", "judah", "israel"):
            orders = sorted(r.order for r in K.REIGNS.values() if r.realm == realm)
            self.assertEqual(orders, list(range(1, len(orders) + 1)), realm)
        for key, r in K.REIGNS.items():
            with self.subTest(key):
                self.assertGreaterEqual(r.ussher[0], r.ussher[1])
                if r.realm != "united":
                    self.assertTrue(r.thiele, "a Thiele date for every divided-kingdom reign")
                if r.thiele:
                    self.assertGreaterEqual(r.thiele[0], r.thiele[1])

    def test_each_verse_says_it(self):
        for key, r in K.REIGNS.items():
            names = (r.name, *r.aka)
            with self.subTest(key):
                if r.synchronism_ref:
                    self.assertTrue(says(r.synchronism_ref, *names), r.synchronism_ref)
                if r.mother_ref:
                    self.assertTrue(says(r.mother_ref, first(r.mother)), r.mother_ref)
                if r.father_ref:
                    self.assertTrue(says(r.father_ref, first(r.father)), r.father_ref)
                if r.buried_ref:
                    self.assertTrue(says(r.buried_ref, "buried"), r.buried_ref)
                if r.verdict_ref and r.verdict in ("right", "evil", "right, but"):
                    self.assertTrue(says(r.verdict_ref, "right", "evil", "sins", "sin"),
                                    r.verdict_ref)
                for f in ("kings_refs", "chronicles_refs"):
                    if getattr(r, f):
                        self.assertTrue(says(getattr(r, f), *names), f)


class Ties(unittest.TestCase):
    def test_events_anchor_to_a_reign(self):
        """An event's verse names its foreign king (or his nation, where the
        text names no king), and its Ussher year falls in the reign it is
        dated by."""
        for key, e in K.EVENTS.items():
            with self.subTest(key):
                bc, _exact = G.event_year(e, key_=key)
                self.assertIsNotNone(bc)
                who = e.nation.split()[0] if e.foreign_king.lower().startswith("the king of") \
                    else first(e.foreign_king)
                self.assertTrue(says(e.ref, who, f"king of {first(e.nation)}",
                                     *(["Pharaoh"] if "Egypt" in e.nation else [])),
                                (e.ref, who))
                anchor = G.find_king(e.anchor_king)
                # Evil-merodach is dated by Jehoiachin's captivity, not his reign
                if anchor and "captivity" not in e.anchor_year:
                    a, b = K.REIGNS[anchor].ussher
                    self.assertTrue(b - 1 <= bc <= a, (anchor, bc, (a, b)))

    def test_prophets_name_their_kings(self):
        for key, p in PR.PROPHETS.items():
            with self.subTest(key):
                israelite = [t for t in p.kings if re.search(r"\((Judah|Israel|united Israel)\)", t)]
                for t in israelite:
                    self.assertIsNotNone(G.find_king(t), t)
                if p.refs:
                    self.assertTrue(says(p.refs, p.name.split()[0] if not p.name.startswith("the ")
                                         else "God", *p.aka))

    def test_bars_hold_their_names(self):
        """Every reign's bar is tall enough for its name, however short the
        reign (Zimri's seven days)."""
        for key in K.REIGNS:
            x0, y0, x1, y1 = G.bar_box(key)
            with self.subTest(key):
                self.assertGreaterEqual(y1 - y0, G.MINBAR - 0.5)


if __name__ == "__main__":
    unittest.main()
