"""Joshua 14's module (joshua14_caleb.py), with no build and no clock: every word
a beat is cued to is in its verse, every camera leg goes somewhere, and each
card's QC is clear and has teeth. The map's cast_qc needs the tour's build, so the
generator runs it.

    .venv\\Scripts\\python.exe -m unittest test_joshua14_caleb
"""

import re
import unittest

import joshua14_caleb as CB
from generate_israel_atlas import TEXT_WEB
from svg_map_camera import Flight

# A stand-in for the tour: what a cue asks doesn't hang on where anything stands.
LOT_COL = {key: (1, 2, 3) for key in ("REUBEN", "GAD", "MANASSEH_E", "JUDAH")}


def P(lat, lon):
    return (lon * 100.0, -lat * 100.0)


def PS(pts):
    return [P(*p) for p in pts]


def shot(lat, lon, px, _x, _y):
    return (px / 100.0, *P(lat, lon))


def key_layout():
    return {"LEVI": {"box": (0, 0, 10, 10), "at": (5, 5)}}


def cues():
    """Every (verse, word) the cards and the cast ask the narration for."""
    said = set()

    def say(ref, word):
        said.add((ref, word))
        return None                     # so each beat keeps its hand value

    gil = CB.build_gil(P(*CB.GILGAL), LOT_COL, say)
    CB.build_heb(P(*CB.HEBRON), say)
    cam = shot(*CB.CAMERAS["stage"])
    tour = CB.Tour(P, PS, shot, say, cam, key_layout, LOT_COL, gil, None, [], [], 0.0)
    fl = Flight(cam, [("to", shot(*CB.CAMERAS["k_h"]), 1.0)])
    for cv in CB.VERSES:
        CB.cast(cv, fl, tour)
    CB.held_goes((14, 10), tour)
    return said


class Cues(unittest.TestCase):
    def test_every_word_is_in_its_verse(self):
        """A misspelt word would keep its hand value for good, with no complaint."""
        said = cues()
        self.assertGreater(len(said), 70)
        for ref, word in sorted(said):
            with self.subTest(verse=ref, word=word):
                self.assertRegex(TEXT_WEB[("Joshua", *ref)],
                                 r"(?<!\w)" + re.escape(word) + r"(?!\w)")


class Legs(unittest.TestCase):
    def test_every_leg_goes_somewhere(self):
        for ref, legs in CB.LEGS.items():
            for kind, target, _d in legs:
                with self.subTest(verse=ref, target=target):
                    if kind == "hold":
                        self.assertIsNone(target)
                    else:
                        self.assertEqual(kind, "to")
                        self.assertTrue(target == "map" or target in CB.SHOTS
                                        or target in CB.CAMERAS)

    def test_the_map_verses_have_cameras(self):
        for cv, name in CB.MAP_AT.items():
            with self.subTest(cv):
                self.assertIn(name, CB.CAMERAS)


class CardQC(unittest.TestCase):
    def setUp(self):
        self.gil = CB.build_gil(P(*CB.GILGAL), LOT_COL)
        self.heb = CB.build_heb(P(*CB.HEBRON))

    def test_both_cards_are_clear(self):
        self.assertEqual(CB.qc(self.gil), [])
        self.assertEqual(CB.qc(self.heb), [])

    def test_it_reads_the_mark_as_drawn(self):
        """85 moved onto his head, in the event that draws it."""
        r = (14, 10)
        self.gil.events[r] = [(k, a, t, d, CB.numeral("85", y=-100) if k == "mark" else v)
                              for k, a, t, d, v in self.gil.events[r]]
        self.assertTrue(any("85 touches caleb" in p for p in CB.qc(self.gil)))

    def test_it_asks_at_the_bracket(self):
        self.gil.actors["n_eph"].start["y"] = 1536
        self.assertTrue(any("Ephraim touches the bracket" in p for p in CB.qc(self.gil)))


if __name__ == "__main__":
    unittest.main()
