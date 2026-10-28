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


if __name__ == "__main__":
    unittest.main()
