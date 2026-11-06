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

    def test_wording(self):
        # the corrections the Leviticus 1-7 inventories found against the WEB
        o = OF.OFFERING
        whos = [r.who for r in o["sin"].brought]
        self.assertIn("can't afford a lamb", whos)            # 5:7
        self.assertIn("can't afford two turtledoves", whos)         # 5:11
        self.assertFalse({"the poor", "the poorest"} & set(whos))
        # "all of it" (1:9, 13) is not "no one eats it"
        self.assertEqual([r.flag for r in o["burnt"].eaten], [SN.DERIVED])
        self.assertIn("in the place of the ashes",
                      o["burnt"].burns[1].what)              # 1:16
        # 2:9 names only "its memorial": no handful, no frankincense
        for r in o["meal"].burns:
            if ("Leviticus", 2, 9) in _covered(r.ref, "Leviticus"):
                self.assertNotIn("handful", r.what)
                self.assertNotIn("frankincense", r.what)
            if "handful" in r.what:
                self.assertIn("handful", _text(r.ref, "Leviticus"))
        own = [r for r in o["meal"].brought if r.who == "the priests' own"][0]
        self.assertIn("in a griddle", own.what)               # 6:21
        self.assertIn("in the day when he is anointed", own.what)   # 6:20
        # 4:18 doesn't name the altar of sweet incense: only 4:7 does
        for r in o["sin"].blood:
            cov = _covered(r.ref, "Leviticus")
            if ("Leviticus", 4, 18) in cov:
                self.assertEqual(r.flag, SN.DERIVED)
                self.assertNotIn(("Leviticus", 4, 7), cov)
        # "which is by the loins" wherever the text says it
        for key, ref in (("peace", "Lev 3:4"), ("sin", "Lev 4:9"),
                         ("trespass", "Lev 7:4")):
            said = [r for r in o[key].burns
                    if _covered(ref, "Leviticus") <= _covered(r.ref,
                                                             "Leviticus")]
            self.assertTrue(said, key)
            for r in said:
                self.assertIn("which is by the loins", r.what, key)
        lamb = [r for r in o["peace"].burns if r.who == "a lamb"][0]
        self.assertIn("close to the backbone", lamb.what)      # 3:9
        # "made known to him" is 4:14, 23 and 28's, not 4:2's
        self.assertNotIn("(4:2, 14", o["sin"].when.value)
        # the silver as the ram's estimation is a reading
        silver = [r for r in o["trespass"].brought if r.who == "the silver"]
        self.assertEqual([r.flag for r in silver], [SN.DERIVED])


# ---------------------------------------------------------------------------
# The Leviticus 1-7 tables: sanctuary.PLACES and offerings' CUTS, RITES and
# boards
# ---------------------------------------------------------------------------

LEV17 = _covered("Lev 1-7", "Leviticus")


def _web(ref):
    """_text in Leviticus, with the WEB's curly apostrophes made plain."""
    return _text(ref, "Leviticus").replace("’", "'")


def _words(label):
    return re.findall(r"[a-z']+", label.lower())


class LeviticusTables(unittest.TestCase):
    def _in_lev17(self, ref, what):
        cov = _covered(ref, "Leviticus")
        self.assertTrue(cov, (what, ref))
        self.assertTrue(cov <= LEV17, (what, ref))

    def test_places(self):
        self.assertEqual([p.key for p in SN.PLACES],
                         ["ash_place", "north_side", "clean_place"])
        self.assertFalse(set(SN.PLACE) & set(SN.PART))
        x0, y0, x1, y1 = SN.plan_box("altar")
        for p in SN.PLACES:
            self.assertIn(p.flag, FLAGS, p.key)
            self.assertTrue(len(p.label.split()) <= 4, p.key)
            self.assertIn(p.label.lower(), _web(p.ref), p.key)
            for ref in (p.ref, p.derived):
                if ref:
                    self._in_lev17(ref, p.key)
            for pt in [p.pt] + ([p.box[:2], p.box[2:]] if p.box else []):
                if pt:
                    cx0, cy0, cx1, cy1 = SN.COURT
                    self.assertTrue(cx0 <= pt[0] <= cx1 and
                                    cy0 <= pt[1] <= cy1, p.key)
        ash, north, clean = (SN.PLACE[k] for k in
                             ("ash_place", "north_side", "clean_place"))
        # east of the altar (x runs east), level with it; distance not given
        self.assertGreater(ash.pt[0], x1)
        self.assertTrue(y0 < ash.pt[1] < y1)
        self.assertEqual(ash.flag, SN.DERIVED)
        # the altar's own width, north of it (y runs south)
        self.assertEqual(north.box, (x0, y0 - (y1 - y0), x1, y0))
        self.assertEqual(north.pt, ((x0 + x1) / 2, y0 - (y1 - y0) / 2))
        self.assertEqual(north.flag, SN.STATED)
        self.assertIn("north side", _web(north.ref))
        # off the plan, outside the camp
        self.assertIsNone(clean.pt)
        self.assertIsNone(clean.box)
        self.assertEqual(clean.flag, SN.NOT_GIVEN)
        self.assertIn("outside", _web(clean.ref))

    def test_cuts_are_drawn(self):
        """Every cut is a part, with an anchor, on each beast it names."""
        import svg_figures as F
        for c in OF.CUTS:
            for beast in c.beasts:
                if beast == "bird":                 # dove() overlays
                    continue
                parts, anchors = F.beast_parts(beast)
                self.assertIn(c.key, parts, (c.key, beast))
                self.assertIn(c.key, anchors, (c.key, beast))

    def test_ram_keeps_the_ewe_box(self):
        """The horned ram fits the box the ewe does, so a table icon fitted
        to its bbox isn't shrunk (a horn-ridge loop once rebound bx)."""
        import svg_figures as F
        ewe = F.bbox((F.sheep(), 0))
        for kw in ({}, {"lying": True}, {"lamb": True}):
            ram = F.bbox((F.sheep(ram=True, **kw), 0))
            base = F.bbox((F.sheep(**kw), 0))
            self.assertLessEqual(ram[1], base[1] + 1, kw)
            self.assertGreaterEqual(ram[0], base[0] - 6, kw)
        self.assertEqual(F.bbox((F.sheep(ram=True), 0))[1], ewe[1])

    def test_cuts(self):
        keys = ["skin", "head", "legs", "meat", "pieces", "innards",
                "fat_cover", "fat_on", "kidneys", "kidney_fat", "loins",
                "liver", "liver_cover", "backbone", "tail_fat", "breast",
                "right_thigh", "dung", "crop", "wings"]
        self.assertEqual(sorted(c.key for c in OF.CUTS), sorted(keys))
        self.assertEqual(OF.CUT["tail_fat"].beasts, ("sheep", "ram"))
        self.assertEqual(OF.CUT["dung"].beasts, ("bull",))
        self.assertEqual(OF.CUT["crop"].beasts, ("bird",))
        self.assertEqual(OF.CUT["wings"].beasts, ("bird",))
        for c in OF.CUTS:
            self._in_lev17(c.ref, c.key)
            self.assertTrue(c.beasts, c.key)
            self.assertTrue(set(c.beasts) <= {"bull", "sheep", "ram", "goat",
                                              "bird"}, c.key)
            self.assertEqual("bird" in c.beasts, c.key in ("crop", "wings"))
            self.assertTrue(len(c.label.split()) <= 4, c.key)
            # the WEB's words, said in the verses it cites
            said = set(_words(_web(c.ref)))
            for w in _words(c.label):
                self.assertIn(w, said, (c.key, w))

    def test_rites(self):
        places = set(SN.PART) | set(SN.PLACE)
        for r in OF.RITES:
            what = (r.offering, r.case, r.ref)
            self.assertIn(r.offering, OF.OFFERING, what)
            self.assertTrue(r.case and r.act, what)
            self.assertTrue(r.place == "" or r.place in places, what)
            self.assertIn(r.flag, FLAGS, what)
            self._in_lev17(r.ref, what)
        # the north side is said of the flock's burnt offering only (1:11);
        # "where they kill the burnt offering" puts the rest there
        for r in OF.RITES:
            if r.place == "north_side":
                want = SN.STATED if r.ref == "Lev 1:11" else SN.DERIVED
                self.assertEqual(r.flag, want, r.ref)
        north = {v for r in OF.RITES if r.place == "north_side"
                 for v in _covered(r.ref, "Leviticus")}
        place = SN.PLACE["north_side"]
        self.assertEqual(north, _covered(f"{place.ref}; {place.derived}",
                                         "Leviticus"))
        # the hand on the head, where the text says it
        hands = {v for r in OF.RITES if "hand" in r.act
                 for v in _covered(r.ref, "Leviticus")}
        for c, v in ((1, 4), (3, 2), (3, 8), (3, 13), (4, 4), (4, 15), (4, 24),
                     (4, 29), (4, 33)):
            self.assertIn(("Leviticus", c, v), hands)

    BOARDS = ("CAUSES", "WRONGS", "BREADS", "DAYS", "VESSELS", "FORGIVEN",
              "MOST_HOLY", "ONE_LAW", "PENALTIES", "LAW_ORDER", "SINAI")

    def test_boards(self):
        for name in self.BOARDS:
            board = getattr(OF, name)
            self.assertTrue(board, name)
            keys = [e.key for e in board]
            self.assertEqual(len(keys), len(set(keys)), name)
            for e in board:
                what = (name, e.key)
                self.assertIn(e.flag, FLAGS, what)
                self._in_lev17(e.ref, what)
                self.assertTrue(len(e.label.split()) <= 4, what)
                # the WEB's own words, as said in its verse
                self.assertIn(e.label.lower(), _web(e.ref), what)
                if getattr(e, "offering", ""):
                    self.assertIn(e.offering, OF.OFFERING, what)

    def test_board_contents(self):
        # 7:12's three kinds and 7:13's leavened
        self.assertEqual([e.ref for e in OF.BREADS], ["Lev 7:12"] * 3 +
                         ["Lev 7:13"])
        # the nine verses that say "forgiven"
        forgiven = {v for e in OF.FORGIVEN
                    for v in _covered(e.ref, "Leviticus")}
        said = {(b, c, v) for b, c, v in LEV17
                if "forgiven" in _web(f"Lev {c}:{v}")}
        self.assertEqual(forgiven, said)
        self.assertEqual(len(said), 9)
        for e in OF.FORGIVEN:
            self.assertIn("forgiven", _web(e.ref), e.key)
        # "cut off", each where it is said
        cut = {v for e in OF.PENALTIES for v in _covered(e.ref, "Leviticus")}
        self.assertEqual(cut, {(b, c, v) for b, c, v in LEV17
                               if "cut off" in _web(f"Lev {c}:{v}")})
        for e in OF.PENALTIES:
            self.assertIn("cut off", _web(e.ref), e.key)
        # 7:37's order, and the consecration, which is no offering
        law = _web("Lev 7:37")
        at = [law.index(e.label.lower()) for e in OF.LAW_ORDER]
        self.assertEqual(at, sorted(at))
        self.assertEqual([e.offering or e.key for e in OF.LAW_ORDER],
                         ["burnt", "meal", "sin", "trespass", "consecration",
                          "peace"])
        self.assertEqual(sorted(e.offering for e in OF.MOST_HOLY),
                         ["meal", "sin", "trespass"])
        for e in OF.MOST_HOLY:
            for v in _covered(e.ref, "Leviticus"):
                self.assertIn("most holy",
                              _web(f"Lev {v[1]}:{v[2]}"), (e.key, v))
        self.assertEqual({d.day for d in OF.DAYS}, {1, 2, 3})
        self.assertEqual({v.kind for v in OF.VESSELS},
                         {"oven", "griddle", "pan", "pot"})


if __name__ == "__main__":
    unittest.main()
