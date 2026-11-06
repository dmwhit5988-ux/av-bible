"""temple.py, the one model of Solomon's Temple: its measures, and its verses.

    .venv\\Scripts\\python.exe -m unittest test_temple -v
"""

import math
import unittest

import sanctuary as SN
import svg_figures as F
import temple as TM
import verse_refs


def _verses(part):
    """Every (book, chapter, verse) a part's card cites."""
    out = set()
    refs = [r for _g, r in part.verses] + [d.ref for d in part.dims if d.ref]
    if part.place[2]:
        refs.append(part.place[2])
    for s in refs:
        for ref in verse_refs.parse(s, "1 Kings"):
            out.update(ref.verses())
    return out


def _w(box):
    return box[2] - box[0]


def _h(box):
    return box[3] - box[1]


class Model(unittest.TestCase):
    def test_the_house(self):
        self.assertEqual((_w(TM.HOUSE), _h(TM.HOUSE)), (60, 20))     # 6:2
        self.assertEqual(TM.HOUSE_HEIGHT, 30)
        self.assertEqual((_w(TM.ORACLE), _h(TM.ORACLE)), (20, 20))   # 6:20
        self.assertEqual(TM.ORACLE_HEIGHT, 20)
        self.assertEqual(_w(TM.HOLY), 40)                            # 6:17
        self.assertEqual(TM.ORACLE[2], TM.PARTITION_X)
        self.assertEqual(TM.HOLY[0], TM.PARTITION_X)
        # the porch: 20 along the width of the house, 10 deep (6:3)
        self.assertEqual((_w(TM.PORCH), _h(TM.PORCH)), (10, 20))
        self.assertEqual(TM.PORCH[0], TM.EAST_WALL[1])

    def test_side_rooms_and_walls(self):
        # three floors 5, 6 and 7 wide, each 5 high (6:6, 10): the house's
        # wall steps in a cubit at each, so the outer wall stays put
        self.assertEqual(TM.SIDE_WIDTHS, (5, 6, 7))
        self.assertEqual(TM.FLOOR_HEIGHT, 5)
        for k, width in enumerate(TM.SIDE_WIDTHS):
            rooms = TM.side_rooms(k)
            north, south = rooms["north"], rooms["south"]
            self.assertEqual(_h(north), width)
            self.assertEqual(_h(south), width)
            self.assertEqual(TM.wall_at(k) + width + TM.OUTER_WALL,
                             TM.SIDE_DEPTH)
        self.assertEqual([TM.wall_at(k) - TM.wall_at(k + 1)
                          for k in range(2)], [1, 1])
        # round the holy place and the inner sanctuary, not the porch (6:5)
        self.assertEqual(TM.SIDE_EAST, TM.EAST_WALL[1])
        self.assertLessEqual(TM.SIDE_TOP + TM.SIDE_ROOF, TM.WINDOW_SILL)

    def test_cherubim_reach_wall_to_wall(self):
        # two, each with wings of 5, wall to wall across the 20 (6:24, 27)
        ys = sorted(y for _x, y in TM.CHERUBIM)
        spans = [(y - TM.CHERUB_WING, y + TM.CHERUB_WING) for y in ys]
        self.assertEqual(spans[0][0], TM.ORACLE[1])
        self.assertEqual(spans[0][1], spans[1][0])          # wing to wing
        self.assertEqual(spans[1][1], TM.ORACLE[3])
        # and the figure itself spreads them to ten cubits
        x0, x1, _y0, y1 = F.bbox((F.temple_cherub("front"), 0))
        self.assertAlmostEqual((x1 - x0) / F.CUBIT, 10, delta=0.15)
        self.assertAlmostEqual(y1 / F.CUBIT, TM.CHERUB_HEIGHT, delta=0.05)

    def test_pillars_and_brass(self):
        self.assertEqual(TM.PILLAR_HEIGHT + TM.CAPITAL_HEIGHT, 23)  # 7:15-16
        self.assertAlmostEqual(TM.PILLAR_D * math.pi, TM.PILLAR_ROUND)
        _x0, _x1, _y0, y1 = F.bbox((F.temple_pillar(), 0))
        self.assertAlmostEqual(y1 / F.CUBIT, 23)
        # Jachin on the right, the south; Boaz on the left (7:21)
        self.assertGreater(TM.JACHIN[1], TM.AXIS)
        self.assertLess(TM.BOAZ[1], TM.AXIS)
        self.assertGreater(TM.JACHIN[0], TM.PORCH[2])
        self.assertEqual((_w(TM.ALTAR), _h(TM.ALTAR)), (20, 20))    # 2 Chr 4:1
        self.assertEqual(TM.ALTAR_HEIGHT, 10)
        # the Sea: south-east of the house (7:39), ten across, brim to brim
        self.assertGreater(TM.SEA[0] - TM.SEA_D / 2, TM.PORCH[2])
        self.assertGreater(TM.SEA[1] - TM.SEA_D / 2, TM.HOUSE[3] + TM.WALL[0])
        x0, x1, _y0, _y1 = F.bbox((F.molten_sea(), 0))
        self.assertLess((x1 - x0) / F.CUBIT, TM.SEA_D + 0.3)
        # five bases on each side (7:39), clear of the side rooms
        bases = TM.bases()
        self.assertEqual({k: len(v) for k, v in bases.items()},
                         {"north": 5, "south": 5})
        self.assertTrue(all(b[3] < TM.OUTSIDE[1] for b in bases["north"]))
        self.assertTrue(all(b[1] > TM.OUTSIDE[3] for b in bases["south"]))
        self.assertTrue(all(_w(b) == TM.BASE for b in bases["north"]))

    def test_inside_the_house(self):
        # ten lamp stands and ten tables, five each side (7:49; 2 Chr 4:7-8)
        for d in (TM.lamp_stands(), TM.tables()):
            self.assertEqual(sorted(len(v) for v in d.values()), [5, 5])
        for x, y in sum(TM.lamp_stands().values(), []):
            self.assertTrue(TM.HOLY[0] < x < TM.HOLY[2])
        for b in sum(TM.tables().values(), []):
            self.assertTrue(TM.HOLY[0] < b[0] and b[2] < TM.HOLY[2])
        a = TM.INCENSE_ALTAR
        self.assertTrue(TM.HOLY[0] < a[0] < a[2] < TM.LAMPS_X[0])
        # the ark in the inner sanctuary, under the wings
        self.assertTrue(TM.ORACLE[0] < TM.ARK[0] < TM.ARK[2] < TM.ORACLE[2])
        self.assertAlmostEqual(TM.ARK[2] - TM.ARK[0], 2.5)

    def test_everything_in_the_court(self):
        x0, y0, x1, y1 = TM.INNER_COURT
        things = [TM.OUTSIDE, TM.ALTAR, TM.PLATFORM] + sum(
            TM.bases().values(), [])
        for b in things:
            self.assertTrue(x0 < b[0] and b[2] < x1 and y0 < b[1]
                            and b[3] < y1, b)
        sx, sy = TM.SEA
        self.assertTrue(x0 < sx - 5 and sx + 5 < x1 and sy + 5 < y1)

    def test_tabernacle_overlay(self):
        # the tent's west end on the house's, its Most Holy Place in the
        # inner sanctuary's corner, and twice its size each way
        tent = TM.tabernacle(SN.TENT)
        self.assertEqual(tent[0], TM.HOUSE[0])
        self.assertEqual((tent[1] + tent[3]) / 2, TM.AXIS)
        self.assertEqual(_w(TM.HOUSE), 2 * _w(SN.TENT))
        self.assertEqual(_h(TM.HOUSE), 2 * _h(SN.TENT))
        self.assertEqual(TM.ORACLE_HEIGHT, 2 * SN.TENT_HEIGHT)

    def test_flags_and_verses(self):
        keys = [p.key for p in TM.PARTS]
        self.assertEqual(len(keys), len(set(keys)))
        for p in TM.PARTS:
            self.assertTrue(_verses(p), p.key)
            for d in p.dims:
                self.assertIn(d.flag, (TM.STATED, TM.DERIVED, TM.NOT_GIVEN))
                # a stated or derived figure cites its verse
                if d.flag != TM.NOT_GIVEN:
                    self.assertTrue(d.ref, (p.key, d.what))
            self.assertIn(p.place[1], (TM.STATED, TM.DERIVED, TM.NOT_GIVEN))

    def test_both_accounts(self):
        # where Kings and Chronicles differ, the card carries both
        def figures(key):
            return {d.what: (d.value, d.ref) for d in TM.PART[key].dims}
        pil = figures("jachin")
        self.assertEqual(pil["height"], ("18 cubits", "1 Kgs 7:15"))
        self.assertEqual(pil["height, in Chronicles"],
                         ("35 cubits", "2 Chr 3:15"))
        sea = figures("sea")
        self.assertIn("2,000", sea["held"][0])
        self.assertIn("3,000", sea["held, in Chronicles"][0])
        self.assertIn("120", figures("porch")["height, in Chronicles"][0])


if __name__ == "__main__":
    unittest.main()
