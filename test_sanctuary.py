"""sanctuary.py, the one Tabernacle model: its counts, and its verses.

    .venv\\Scripts\\python.exe -m unittest test_sanctuary -v
"""

import unittest

import sanctuary as SN
import verse_refs


def _verses(part):
    """Every (book, chapter, verse) a part's cards cite."""
    out = set()
    refs = [r for _g, r in part.verses] + [d.ref for d in part.dims if d.ref]
    if part.place[2]:
        refs.append(part.place[2])
    for s in refs:
        for ref in verse_refs.parse(s, "Exodus"):
            out.update(ref.verses())
    return out


class Model(unittest.TestCase):
    def test_sixty_pillars(self):
        # 20 south, 20 north, 10 west, 10 east with 4 at the gate (27:10-16)
        counts = {k: len(v) for k, v in SN.PILLARS.items()}
        self.assertEqual(counts, {"north": 20, "south": 20, "west": 10,
                                  "east": 10, "gate": 4})
        self.assertEqual(len(set(SN.pillar_points())), 60)
        self.assertTrue(set(SN.PILLARS["gate"]) <= set(SN.PILLARS["east"]))
        gate = [y for _x, y in SN.PILLARS["gate"]]
        self.assertTrue(all(SN.GATE[0] < y <= SN.GATE[1] for y in gate))

    def test_court_and_tent(self):
        self.assertEqual(SN.COURT, (0, 0, 100, 50))           # 27:18
        x0, y0, x1, y1 = SN.TENT
        self.assertEqual((x1 - x0, y1 - y0), (30, 10))
        self.assertEqual(SN.GATE[1] - SN.GATE[0], 20)         # 27:16
        self.assertEqual(SN.VEIL_X - x0, 10)                  # a cube

    def test_elevation(self):
        # five pillars across the door, one at each corner (26:37)
        self.assertEqual(len(SN.DOOR_PILLARS), 5)
        ys = [y for _x, y in SN.DOOR_PILLARS]
        self.assertEqual((ys[0], ys[-1]), (SN.TENT[1], SN.TENT[3]))
        self.assertTrue(all(x == SN.DOOR_X for x, _y in SN.DOOR_PILLARS))
        self.assertEqual(SN.TENT_HEIGHT, 10)                  # 26:16
        for value, flag, ref in SN.ELEVATION.values():
            self.assertIn(flag, (SN.STATED, SN.DERIVED, SN.NOT_GIVEN))
            self.assertEqual(bool(ref), flag != SN.NOT_GIVEN)
        # from the gate, north is on the right and the court's middle is ox
        ev = SN.Elevation(0, 100, 2)
        self.assertEqual(ev.x(25), 0)
        self.assertGreater(ev.x(0), ev.x(50))
        self.assertEqual(ev.y(SN.HANGING_HEIGHT), 90)

    def test_every_ref_reads(self):
        for p in SN.PARTS:
            self.assertTrue(_verses(p), p.key)

    def test_flags(self):
        for p in SN.PARTS:
            for d in p.dims:
                self.assertIn(d.flag, (SN.STATED, SN.DERIVED, SN.NOT_GIVEN))
            self.assertIn(p.place[1], (SN.STATED, SN.DERIVED, SN.NOT_GIVEN))


# Verses that name several parts at once: each part named must cite the
# verse, or the page opened from it would leave that part dark.
TOGETHER = {
    ("Exodus", 30, 26): ("tent", "ark"),
    ("Exodus", 30, 27): ("table", "lamp_stand", "incense_altar"),
    ("Exodus", 30, 28): ("altar", "basin"),
    ("Exodus", 31, 7): ("tent", "ark", "mercy_seat"),
    ("Exodus", 31, 8): ("table", "lamp_stand", "incense_altar"),
    ("Exodus", 31, 9): ("altar", "basin"),
    ("Exodus", 35, 12): ("ark", "mercy_seat", "veil"),
    ("Exodus", 39, 35): ("ark", "mercy_seat"),
    ("Exodus", 39, 40): ("court", "gate"),
    ("Numbers", 3, 31): ("ark", "table", "lamp_stand", "incense_altar",
                         "altar"),
}


class Verses(unittest.TestCase):
    def test_parts_named_together(self):
        cited = {p.key: _verses(p) for p in SN.PARTS}
        for verse, keys in TOGETHER.items():
            for key in keys:
                self.assertIn(verse, cited[key], f"{key} at {verse}")


# ---------------------------------------------------------------------------
# garments.py and offerings.py, the Garments and Offerings views' data
# ---------------------------------------------------------------------------

import re

import garments as GA
import offerings as OF
import passages
import svg_priest

FLAGS = (SN.STATED, SN.DERIVED, SN.NOT_GIVEN)


def _text(ref, default="Exodus"):
    """The WEB text of every verse a ref string covers, lower-cased."""
    out = []
    for r in verse_refs.parse(ref, default):
        for book, c, v in r.verses():
            verses = dict(passages.load_chapter(book, c).verses)
            out.append(verses[v])
    return " ".join(out).lower()


def _covered(ref, default):
    return {v for r in verse_refs.parse(ref, default) for v in r.verses()}


class Garments(unittest.TestCase):
    def test_keys_follow_wearing_order(self):
        keys = [g.key for g in GA.GARMENTS]
        n = len(svg_priest.WEARING_ORDER)
        self.assertEqual(tuple(keys[:n]), svg_priest.WEARING_ORDER)
        self.assertIn("sons", keys[n:])
        self.assertIn("linen", keys[n:])
        self.assertEqual(len(set(keys)), len(keys))

    def test_every_ref_reads(self):
        refs = [GA.STONES_REF, GA.NAMES_REF, GA.HIGH_PRIEST_REF, GA.WASHED]
        refs += [ref for ref, _keys in GA.DRESSING]
        for g in GA.GARMENTS:
            self.assertTrue(g.verses, g.key)
            refs += [r for _grp, r in g.verses]
            refs += [d.ref for d in g.dims if d.ref]
        for ref in refs:
            self.assertTrue(verse_refs.parse(ref, "Exodus"), ref)

    def test_flags(self):
        for g in GA.GARMENTS:
            for d in g.dims:
                self.assertIn(d.flag, FLAGS, (g.key, d.what))
                if d.flag != SN.NOT_GIVEN:
                    self.assertTrue(d.ref, (g.key, d.what))

    def test_names_are_the_webs(self):
        # each garment's name (less "the") is said in a verse it cites
        for g in GA.GARMENTS:
            name = g.name.removeprefix("the ").lower()
            said = " ".join(_text(r) for _grp, r in g.verses)
            self.assertIn(name, said, g.key)

    def test_dressing(self):
        known = set(GA.GARMENT)
        order = [k for _ref, keys in GA.DRESSING for k in keys]
        self.assertTrue(set(order) <= known)
        self.assertEqual(len(order), len(set(order)))
        # the breeches first, from Exodus 28:42 (Leviticus 8 doesn't name them)
        self.assertEqual(GA.DRESSING[0], ("Exod 28:42", ("breeches",)))
        # every step's garment is named in its verse, and Lev 8:7-9 names
        # nothing the steps leave out
        lev = _text("Lev 8:7-9")

        def word(k, text):              # "plate", not "breastplate"
            m = re.search(rf"\b{k}\b", text)
            return m and m.start()

        for ref, keys in GA.DRESSING:
            for k in keys:
                self.assertIsNotNone(word(k, _text(ref)), (ref, k))
        for k in svg_priest.WEARING_ORDER:
            if word(k, lev) is not None:
                self.assertIn(k, order, k)
        # the steps follow the text's order
        at = [word(k, lev) for k in order if k != "breeches"]
        self.assertEqual(at, sorted(at))

    def test_twelve_stones(self):
        stones = GA.stone_list()
        self.assertEqual(len(stones), 12)
        self.assertEqual([len(r) for r in GA.STONES], [3, 3, 3, 3])
        for ref in ("Exod 28:17-20", "Exod 39:10-13"):
            text = _text(ref)
            at = [text.index(s) for s in stones]
            self.assertEqual(at, sorted(at), ref)

    def test_twelve_names(self):
        self.assertEqual(len(GA.NAMES), 12)
        self.assertEqual(len(set(GA.NAMES)), 12)
        text = _text(GA.NAMES_REF, "Genesis")
        at = [text.index(n.lower()) for n in GA.NAMES]
        self.assertEqual(at, sorted(at))          # birth order
        self.assertEqual([len(s) for s in GA.SHOULDER_STONES], [6, 6])
        self.assertEqual(len(GA.BREASTPLATE_NAMES), 12)
        self.assertEqual(GA.SHOULDER_ORDER.flag, SN.DERIVED)
        self.assertEqual(GA.BREASTPLATE_ORDER.flag, SN.NOT_GIVEN)


class Offerings(unittest.TestCase):
    def _rows(self, o):
        return o.brought + o.burns + o.blood + o.eaten + o.not_eaten

    def test_five(self):
        self.assertEqual([o.key for o in OF.OFFERINGS],
                         ["burnt", "meal", "peace", "sin", "trespass"])

    def test_every_ref_reads(self):
        for o in OF.OFFERINGS:
            refs = [r.ref for r in self._rows(o)] + [o.law_ref, o.when.ref]
            if o.by is not None:
                refs.append(o.by.ref)
            refs += [r for _grp, r in o.verses]
            refs += [t.ref for t in OF.THINGS[o.key]]
            for ref in refs:
                self.assertTrue(verse_refs.parse(ref, "Leviticus"),
                                (o.key, ref))

    def test_name_in_its_verses(self):
        for o in OF.OFFERINGS:
            groups = dict(o.verses)
            self.assertIn(o.name.lower(), _text(groups["For the people"],
                                                "Leviticus"), o.key)

    def test_rows_cite_their_part_of_leviticus(self):
        # each row's verses lie in Leviticus 1-7, and the law for the priests
        # lies in 6:8-7:38
        lev17 = _covered("Lev 1-7", "Leviticus")
        law = _covered("Lev 6:8-7:38", "Leviticus")
        for o in OF.OFFERINGS:
            for r in self._rows(o):
                self.assertTrue(_covered(r.ref, "Leviticus") <= lev17,
                                (o.key, r.ref))
            self.assertTrue(_covered(o.law_ref, "Leviticus") <= law, o.key)

    def test_rows(self):
        for o in OF.OFFERINGS:
            self.assertTrue(o.brought and o.burns and o.eaten, o.key)
            self.assertEqual(bool(o.blood), o.key != "meal", o.key)
            self.assertIn(o.when.flag, FLAGS)
            # a label of a few words for the table, or none (card only)
            for r in self._rows(o):
                self.assertIn(r.flag, FLAGS)
                self.assertTrue(len(r.short.split()) <= 5, (o.key, r.short))
                for key in r.things:
                    self.assertIn(key, OF.THING_KEYS, (o.key, key))
            self.assertTrue(o.when_short)
            # by whom: "anyone", or the sin offering's ranks with their things
            self.assertEqual(o.by is None, o.key == "sin", o.key)
            if o.by is None:
                self.assertTrue(all(r.things for r in o.brought))
            else:
                self.assertTrue(o.by_short)

    def test_when_is_not_guessed(self):
        # only the sin and trespass offerings are required and nothing else;
        # the burnt and meal offerings are either, the peace offerings the
        # three kinds 7:12 and 7:16 name
        when = {o.key: o.when_short for o in OF.OFFERINGS}
        self.assertEqual(when["sin"], "required")
        self.assertEqual(when["trespass"], "required")
        self.assertEqual(when["burnt"], "freewill or required")
        self.assertEqual(when["meal"], "freewill or required")
        self.assertIn("vow", when["peace"])

    def test_law_named_for_all(self):
        # Leviticus 7:37-38 names all five: each cites it
        for o in OF.OFFERINGS:
            self.assertIn(("Leviticus", 7, 37),
                          _covered(dict(o.verses)["The law"], "Leviticus"))

    def test_things(self):
        self.assertEqual(set(OF.THINGS), set(OF.OFFERING))
        for things in OF.THINGS.values():
            for t in things:
                self.assertIn(t.key, OF.THING_KEYS)


if __name__ == "__main__":
    unittest.main()
