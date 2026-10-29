"""Joshua 13-19 verse by verse (allotment.py): every verse is there, every
name is the verse's own word, and everything it places is a gazetteer place,
land or water point, so the allotment map draws nothing of its own.

    .venv\\Scripts\\python.exe -m unittest test_allotment
"""

import unittest

import allotment as AL
import gazetteer as GZ
import generate_israel_atlas as A
from passages import verse_numbers

PLACES = {**GZ.SITES, **GZ.JERUSALEM, **GZ.BEYOND}
TRIBES = {"", "Reuben", "Gad", "Manasseh", "Judah", "Ephraim", "Benjamin", "Simeon",
          "Zebulun", "Issachar", "Asher", "Naphtali", "Dan", "Levi"}


class Verses(unittest.TestCase):
    def test_every_verse(self):
        want = {(c, v) for c in range(13, 20) for v in verse_numbers("Joshua", c)}
        self.assertEqual(set(AL.VERSES), want)

    def test_fields(self):
        for cv, v in AL.VERSES.items():
            with self.subTest(cv):
                self.assertIn(v.tribe, TRIBES)
                self.assertIn(v.kind, ("border", "towns", "story", "summary"))

    def test_names_are_the_verse_words(self):
        for cv, v in AL.VERSES.items():
            text = A.TEXT_WEB[("Joshua", *cv)]
            for n in v.names:
                with self.subTest(verse=cv, name=n.web):
                    self.assertIn(n.web, text)

    def test_the_walk_is_the_verse_names(self):
        for cv, v in AL.VERSES.items():
            webs = {n.web for n in v.names}
            for w in v.walk:
                with self.subTest(verse=cv, name=w):
                    self.assertTrue(w == "|" or w in webs)
            if v.walk:
                self.assertEqual(v.kind, "border", cv)


class Points(unittest.TestCase):
    def test_places_lands_and_waters_are_gazetteer_s(self):
        for cv, v in AL.VERSES.items():
            for n in v.names:
                with self.subTest(verse=cv, name=n.web):
                    if n.kind == AL.SITE:
                        self.assertIn(n.key, PLACES)
                    elif n.kind == AL.REGION:
                        self.assertIn(n.key, GZ.REGIONS)
                    elif n.kind == AL.WATER:
                        self.assertIn(n.key, GZ.WATERS)
                    else:
                        self.assertEqual(n.kind, AL.UNPLACED)
                        self.assertFalse(n.at)

    def test_a_water_point_is_a_point_of_its_lines(self):
        """A water's point is copied from the coast, a lake or a river."""
        lines = [GZ.COAST, *GZ.LAKES.values(), *GZ.RIVERS.values()]
        points = {(round(a, 4), round(b, 4)) for ln in lines for a, b in ln}
        for cv, v in AL.VERSES.items():
            for n in v.names:
                if n.kind == AL.WATER:
                    with self.subTest(verse=cv, name=n.web):
                        self.assertIn((round(n.at[0], 4), round(n.at[1], 4)), points)

    def test_a_tribe_s_town_is_given_it(self):
        """A town a verse's list gives a tribe is that tribe's in the
        gazetteer."""
        for cv, v in AL.VERSES.items():
            if v.kind != "towns" or not v.tribe or v.tribe == "Levi":
                continue
            for n in v.names:
                if n.kind == AL.SITE and n.key in GZ.SITES and GZ.SITES[n.key].tribe:
                    with self.subTest(verse=cv, name=n.web):
                        self.assertIn(v.tribe, GZ.SITES[n.key].tribe)


if __name__ == "__main__":
    unittest.main()
