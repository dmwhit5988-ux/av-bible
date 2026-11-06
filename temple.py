"""Solomon's Temple as one model, in cubits.

The Temple reference page (generate_temple_reference.py) and the Temple's
figures in svg_figures (the cherubim of the inner sanctuary, the pillars,
the Sea, the bases) take the house, its courts and its furnishings from
here, as every drawing of the Tabernacle takes its own from sanctuary.py.

**The plan frame.** x runs east from the inner face of the west wall, y
south from the inner face of the north wall, both in cubits; the house
inside its walls is (0, 0)-(60, 20) (1 Kings 6:2), its axis is y 10, and it
faces east. `Plan` maps it onto a drawing with east to the right;
`Section` maps a cut through it, heights up, along the axis (looking north)
or across it (looking west, north on the right).

**Two accounts.** 1 Kings 6-7 and 2 Chronicles 3-4 both measure the house,
and where they differ (the pillars, the Sea's measure, the porch's height)
the drawing follows Kings and a part's card gives Chronicles' figure beside
it, each with its verse. Where only Chronicles gives a figure (the bronze
altar), the drawing takes it.

**What the text gives, and what it doesn't**, marked as in sanctuary.py:
STATED, DERIVED (it follows from figures the text gives: the holy place is
30 cubits high because the house is) and NOT GIVEN. The text gives no
thickness for any wall, no size for either court, and no spot for anything
in the courts beyond its side. The spots used here are one arrangement:

- the house's walls at Ezekiel's six cubits (Ezek 41:5), stepping in a
  cubit at each floor of the side rooms, since the floors widen 5, 6 and 7
  on offsets in the wall (1 Kings 6:6), and the side rooms' outer wall at
  his five (Ezek 41:9);
- the porch open at its east end between its side walls, as high as the
  house, with the two pillars standing just before it;
- the altar 18 cubits before the pillars, the Sea off the house's
  south-east corner, the bases in two rows of five beside the side rooms,
  and the bronze scaffold before the altar;
- in the holy place, the lamp stands along the walls and the tables inside
  them, the golden altar before the inner sanctuary's doors.

Names follow the WEB ("the inner sanctuary", "side rooms", "bases",
"basins", "brass"); `aka` holds the names a reader may search for.
"""

import math
from typing import NamedTuple, Optional, Tuple

import sanctuary as SN
from sanctuary import DERIVED, NOT_GIVEN, STATED, Dim

# ---------------------------------------------------------------------------
# Drawing the frame
# ---------------------------------------------------------------------------


class Plan:
    """Plan cubits -> drawing pixels, east to the right. (ox, oy) is where
    the house's inner north-west corner falls; `s` is pixels per cubit."""

    def __init__(self, ox, oy, s):
        self.ox, self.oy, self.s = ox, oy, s

    def pt(self, x, y):
        return self.ox + x * self.s, self.oy + y * self.s

    def box(self, x0, y0, x1, y1):
        """(left, top, width, height) of a plan rectangle."""
        (ax, ay), (bx, by) = self.pt(x0, y0), self.pt(x1, y1)
        return min(ax, bx), min(ay, by), abs(bx - ax), abs(by - ay)


class Section:
    """A cut through the house, heights up. `along` cuts on the axis looking
    north, so h is plan x and east is to the right; `across` cuts looking
    west, so h is plan y and north is on the right. (ox, gy) is where h 0
    meets the ground; `s` is pixels per cubit."""

    def __init__(self, ox, gy, s, cut="along"):
        assert cut in ("along", "across")
        self.ox, self.gy, self.s, self.cut = ox, gy, s, cut

    def x(self, h):
        return self.ox + (h if self.cut == "along" else -h) * self.s

    def y(self, z):
        return self.gy - z * self.s

    def pt(self, h, z):
        return self.x(h), self.y(z)

    def box(self, h0, z0, h1, z1):
        """(left, top, width, height) of a rectangle in the cut."""
        ax, bx = self.x(h0), self.x(h1)
        ay, by = self.y(z0), self.y(z1)
        return min(ax, bx), min(ay, by), abs(bx - ax), abs(by - ay)


# ---------------------------------------------------------------------------
# The house                                              (1 Kings 6)
# ---------------------------------------------------------------------------

HOUSE = (0, 0, 60, 20)             # 60 by 20 (6:2)
HOUSE_HEIGHT = 30                  # (6:2)
AXIS = 10
ORACLE = (0, 0, 20, 20)            # the inner sanctuary, the back 20 (6:16)
ORACLE_HEIGHT = 20                 # a cube (6:20)
PARTITION_X = 20                   # cedar boards, floor to ceiling (6:16)
HOLY = (20, 0, 60, 20)             # "in front ... was forty cubits" (6:17)

# The walls: not given. Ezekiel's house has walls of six cubits (41:5); here
# the house's wall is six at the ground and steps in a cubit at each floor of
# the side rooms (6:6), so the beams rest on the offsets.
WALL = (6, 5, 4)                   # the house's wall, floor by floor
OUTER_WALL = 5                     # the side rooms' outer wall (Ezek 41:9)
EAST_WALL = (60, 66)               # the house's east wall, with its doors

# The side rooms: three floors against the walls all round the holy place
# and the inner sanctuary (6:5), 5, 6 and 7 cubits wide (6:6), each 5 high
# (6:10). They stop at the house's east wall: the porch has none.
FLOOR_HEIGHT = 5
SIDE_WIDTHS = (5, 6, 7)
SIDE_TOP = FLOOR_HEIGHT * len(SIDE_WIDTHS)
SIDE_ROOF = 1                      # its thickness: not given
SIDE_DEPTH = WALL[0] + SIDE_WIDTHS[0] + OUTER_WALL    # 16, wall to outside
SIDE_EAST = EAST_WALL[1]
# "The door for the middle side rooms was in the right side of the house"
# (6:8): the right hand of the house, facing east, is the south (7:39).
SIDE_DOOR = (54, 58)               # x along the south rooms' outer wall


def wall_at(floor):
    """The house's wall thickness on floor 0, 1 or 2 of the side rooms, and
    above them."""
    return WALL[min(floor, len(WALL) - 1)]


def side_rooms(floor):
    """The side rooms' plan rectangles on `floor` (0-2): north, south, west.
    The outer wall stands where it is; the house's wall steps in."""
    w = wall_at(floor)
    d = SIDE_DEPTH - OUTER_WALL            # the house's face to the outer wall
    return {
        "north": (-d, -d, SIDE_EAST, -w),
        "south": (-d, HOUSE[3] + w, SIDE_EAST, HOUSE[3] + d),
        "west": (-d, -w, -w, HOUSE[3] + w),
    }


OUTSIDE = (-SIDE_DEPTH, -SIDE_DEPTH, SIDE_EAST, HOUSE[3] + SIDE_DEPTH)

# The porch: 20 along the width of the house and 10 deep (6:3). Its height
# Kings doesn't give; Chronicles gives 120 (2 Chr 3:4). Here it is as high
# as the house, open at its east end between its side walls.
PORCH = (EAST_WALL[1], 0, EAST_WALL[1] + 10, 20)
PORCH_HEIGHT = HOUSE_HEIGHT

# The doors. The entrance of the inner sanctuary has posts "a fifth part of
# the wall" (6:31) and the house's "a fourth part" (6:33): read as a fifth
# and a fourth of the 20-cubit width, 4 and 5 cubits.
ORACLE_DOOR = (AXIS - 2, AXIS + 2)
HOUSE_DOOR = (AXIS - 2.5, AXIS + 2.5)
DOOR_HEIGHT = 10                   # not given

# The windows of fixed lattice (6:4): not placed by the text. Here they are
# high in the walls of the holy place, above the side rooms' roof.
WINDOW_SILL, WINDOW_HEAD = SIDE_TOP + SIDE_ROOF + 4, SIDE_TOP + SIDE_ROOF + 9
WINDOWS_X = (26, 32, 38, 44, 50, 56)

# ---------------------------------------------------------------------------
# The pillars and the court's brass                        (1 Kings 7)
# ---------------------------------------------------------------------------

PILLAR_HEIGHT = 18                 # (7:15; Jer 52:21)
PILLAR_ROUND = 12                  # "a line of twelve cubits" (7:15)
PILLAR_D = PILLAR_ROUND / math.pi  # derived: about 3.8
CAPITAL_HEIGHT = 5                 # (7:16)
LILY_HEIGHT = 4                    # "lily work, four cubits" (7:19)
POMEGRANATES = 200                 # round each capital, in two rows (7:20)
PILLAR_X = PORCH[2] + 3
JACHIN = (PILLAR_X, AXIS + 6)      # the right, the south (7:21)
BOAZ = (PILLAR_X, AXIS - 6)        # the left, the north

ALTAR = (PILLAR_X + 21, AXIS - 10, PILLAR_X + 41, AXIS + 10)  # 20 by 20
ALTAR_HEIGHT = 10                  # (2 Chr 4:1)
PLATFORM = (ALTAR[2] + 6, AXIS - 2.5, ALTAR[2] + 11, AXIS + 2.5)  # 5 by 5
PLATFORM_HEIGHT = 3                # (2 Chr 6:13)

SEA = (PORCH[2] + 12, HOUSE[3] + 20)   # its centre: south-east (7:39)
SEA_D = 10                         # "from brim to brim" (7:23)
SEA_HEIGHT = 5
SEA_ROUND = 30

BASE = 4                           # 4 by 4, 3 high (7:27)
BASE_HEIGHT = 3
WHEEL = 1.5                        # (7:32)
BASIN = 4                          # "every basin was four cubits" (7:38)
BASES_X = (8, 20, 32, 44, 56)      # their centres; spacing not given
BASES_Y = {"north": -SIDE_DEPTH - 6, "south": HOUSE[3] + SIDE_DEPTH + 6}


def bases():
    """The ten bases' plan rectangles: five on the left (north) and five on
    the right (south) of the house (7:39)."""
    h = BASE / 2
    return {side: [(x - h, y - h, x + h, y + h) for x in BASES_X]
            for side, y in BASES_Y.items()}


# ---------------------------------------------------------------------------
# Inside the house                       (1 Kings 6:19-28; 7:48-50; 8:6-8)
# ---------------------------------------------------------------------------

CHERUB_HEIGHT = 10                 # (6:23)
CHERUB_WING = 5                    # each wing (6:24)
# Wing to wall and wing to wing across the 20 cubits (6:27): one stands in
# each half of the room, on the cross line through its middle.
CHERUBIM = ((ORACLE[2] / 2, AXIS - CHERUB_WING),
            (ORACLE[2] / 2, AXIS + CHERUB_WING))
# The ark under their wings (8:6), its size from Exodus 25:10, its poles
# running east so that their ends were seen from the holy place (8:8).
ARK = (AXIS - 1.25, AXIS - 0.75, AXIS + 1.25, AXIS + 0.75)
ARK_LONG, ARK_HIGH = 2.5, 1.5
POLES = (ARK[0] - 3, ARK[2] + 5)   # how long: not given

INCENSE_ALTAR = (PARTITION_X + 3, AXIS - 0.5, PARTITION_X + 4, AXIS + 0.5)
LAMPS_X = (27, 32, 37, 42, 47)
LAMPS_Y = {"north": 2.5, "south": HOUSE[3] - 2.5}
TABLES_X = LAMPS_X
TABLES_Y = {"north": 5.5, "south": HOUSE[3] - 5.5}
TABLE = (2, 1)                     # drawn at Exodus 25:23's; not given


def lamp_stands():
    return {side: [(x, y) for x in LAMPS_X] for side, y in LAMPS_Y.items()}


def tables():
    w, d = TABLE
    return {side: [(x - w / 2 + 1, y - d / 2, x + w / 2 + 1, y + d / 2)
                   for x in TABLES_X] for side, y in TABLES_Y.items()}


# ---------------------------------------------------------------------------
# The courts                       (1 Kings 6:36; 7:12; 2 Chronicles 4:9)
# ---------------------------------------------------------------------------

# Neither court's size is given. The inner court is drawn round the house,
# its brass and the altar, as a dashed line; the great court lay beyond it.
INNER_COURT = (-SIDE_DEPTH - 12, AXIS - 44, PLATFORM[2] + 9, AXIS + 44)

# ---------------------------------------------------------------------------
# The Tabernacle at the same scale
# ---------------------------------------------------------------------------

# sanctuary.py's tent laid on the house: its west end on the house's west
# wall and its axis on the house's, so the Most Holy Place sits in the inner
# sanctuary's corner and the court it stood in lies round them.
TAB_DX = HOUSE[0] - SN.TENT[0]
TAB_DY = AXIS - (SN.TENT[1] + SN.TENT[3]) / 2


def tabernacle(rect):
    """A sanctuary.py plan rectangle (or point) moved onto the house."""
    if len(rect) == 2:
        return rect[0] + TAB_DX, rect[1] + TAB_DY
    x0, y0, x1, y1 = rect
    return x0 + TAB_DX, y0 + TAB_DY, x1 + TAB_DX, y1 + TAB_DY


# ---------------------------------------------------------------------------
# The parts, for cards and labels
# ---------------------------------------------------------------------------

class Part(NamedTuple):
    key: str
    name: str                      # WEB's wording
    aka: Tuple[str, ...]
    # On the plan: a rectangle (x0, y0, x1, y1) in cubits, a point (x, y)
    # for a thing drawn without a size, or None
    plan: Optional[tuple]
    dims: Tuple[Dim, ...]
    place: Tuple[str, str, str]    # (where it stands, flag, ref)
    material: str
    verses: Tuple[Tuple[str, str], ...]    # (group, ref string)
    note: str = ""
    use: str = ""                  # what it was for, where the text says


def _refs(**groups):
    order = ("planned", "built", "chron", "dedicated", "later", "named")
    label = {"planned": "Planned", "built": "Built", "chron": "Chronicles",
             "dedicated": "Dedicated", "later": "Later",
             "named": "Also named"}
    return tuple((label[g], groups[g]) for g in order if g in groups)


_PILLAR_DIMS = (
    Dim("height", "18 cubits", STATED, "1 Kgs 7:15"),
    Dim("height, in Chronicles", "35 cubits", STATED, "2 Chr 3:15"),
    Dim("round", "a line of 12 cubits", STATED, "1 Kgs 7:15"),
    Dim("across", "about 3.8 cubits", DERIVED, "1 Kgs 7:15"),
    Dim("wall", "hollow, four fingers thick", STATED, "Jer 52:21"),
    Dim("capital", "5 cubits high", STATED, "1 Kgs 7:16"),
    Dim("capital, in 2 Kings", "3 cubits", STATED, "2 Kgs 25:17"),
    Dim("lily work", "4 cubits", STATED, "1 Kgs 7:19"),
    Dim("network", "checker work, with seven wreaths of chain work",
        STATED, "1 Kgs 7:17"),
    Dim("pomegranates", "200 in rows round the capital; 400 for the two",
        STATED, "1 Kgs 7:20, 42"),
    Dim("pomegranates, in Jeremiah", "96 on the sides, 100 on the network "
        "all around", STATED, "Jer 52:23"),
)


def _pillar_refs():
    return _refs(built="1 Kgs 7:13-22, 41-42",
                 chron="2 Chr 3:15-17; 4:11-13",
                 later="2 Kgs 25:13, 16-17; Jer 52:17, 20-23")


PARTS = [
    Part("house", "Yahweh's house", ("temple", "house", "Solomon's temple",
                                     "walls"),
         HOUSE,
         (Dim("length", "60 cubits", STATED, "1 Kgs 6:2"),
          Dim("width", "20 cubits", STATED, "1 Kgs 6:2"),
          Dim("height", "30 cubits", STATED, "1 Kgs 6:2"),
          Dim("in Chronicles", "60 by 20, \"after the first measure\"",
              STATED, "2 Chr 3:3"),
          Dim("walls", "not given; here six cubits, as Ezekiel's house, "
              "stepping in a cubit at each floor of the side rooms",
              NOT_GIVEN, "Ezek 41:5"),
          Dim("roof", "beams and planks of cedar; its shape not given",
              STATED, "1 Kgs 6:9")),
         ("on Mount Moriah, on the threshing floor of Ornan the Jebusite, "
          "facing east", STATED, "2 Chr 3:1"),
         "stone made ready at the quarry, so no tool of iron was heard in "
         "the house; within, cedar from floor to ceiling with a floor of "
         "cypress, carved with cherubim, palm trees and open flowers, and "
         "all overlaid with gold",
         _refs(planned="1 Chr 28:11-12, 19",
               built="1 Kgs 6:1-2, 7, 9, 14-15, 18, 21-22, 29-30, 37-38",
               chron="2 Chr 3:1-7",
               dedicated="1 Kgs 8:10-13, 27-30; 2 Chr 5:13-14; 7:1-3",
               later="2 Kgs 25:9"),
         note="Begun in the fourth year of Solomon's reign, in the month "
              "Ziv, 480 years after the exodus, and finished in the "
              "eleventh, in the month Bul: seven years."),
    Part("oracle", "the inner sanctuary", ("most holy place", "holy of holies",
                                           "oracle"),
         ORACLE,
         (Dim("size", "20 by 20 by 20 cubits", STATED, "1 Kgs 6:20"),
          Dim("in Chronicles", "20 by 20, overlaid with fine gold, 600 "
              "talents", STATED, "2 Chr 3:8"),
          Dim("above it", "10 cubits of the house's 30; what filled them "
              "is not given", DERIVED, "1 Kgs 6:2, 20")),
         ("the back of the house, its west 20 cubits, walled off with "
          "cedar boards from floor to ceiling", STATED, "1 Kgs 6:16"),
         "cedar, overlaid with pure gold",
         _refs(planned="1 Chr 28:11",
               built="1 Kgs 6:16, 19-23, 27",
               chron="2 Chr 3:8-10",
               dedicated="1 Kgs 8:6; 2 Chr 5:7"),
         note="A cube like the Tabernacle's Most Holy Place, twice its "
              "size each way.",
         use="to set the ark of Yahweh's covenant there (1 Kings 6:19)"),
    Part("holy", "the holy place", ("temple", "main hall", "larger room",
                                    "nave", "holy place"),
         HOLY,
         (Dim("length", "40 cubits", STATED, "1 Kgs 6:17"),
          Dim("width", "20 cubits", DERIVED, "1 Kgs 6:2"),
          Dim("height", "30 cubits", DERIVED, "1 Kgs 6:2")),
         ("before the inner sanctuary, between it and the porch", STATED,
          "1 Kgs 6:17; 8:8"),
         "cedar, carved with buds and open flowers, and overlaid with gold; "
         "Chronicles gives a ceiling of cypress with palm trees and chains",
         _refs(built="1 Kgs 6:15, 17-18",
               chron="2 Chr 3:5-7",
               dedicated="1 Kgs 8:8, 10"),
         note="WEB calls it \"the temple\" (1 Kings 6:17), \"the larger "
              "room\" (2 Chronicles 3:5) and \"the holy place\" (1 Kings "
              "8:8)."),
    Part("porch", "the porch", ("vestibule", "porch"),
         PORCH,
         (Dim("length", "20 cubits, along the width of the house", STATED,
              "1 Kgs 6:3"),
          Dim("depth", "10 cubits", STATED, "1 Kgs 6:3"),
          Dim("height", "not given in Kings; here as high as the house",
              NOT_GIVEN, ""),
          Dim("height, in Chronicles", "120 cubits", STATED, "2 Chr 3:4")),
         ("in front of the house, at its east end", STATED, "1 Kgs 6:3"),
         "overlaid within with pure gold (Chronicles)",
         _refs(planned="1 Chr 28:11",
               built="1 Kgs 6:3; 7:12, 21",
               chron="2 Chr 3:4",
               later="2 Chr 29:7, 17",
               named="2 Chr 8:12; Joel 2:17; Ezek 8:16")),
    Part("side_rooms", "the side rooms", ("chambers", "side chambers",
                                          "floors", "stairs"),
         None,
         (Dim("floors", "three", STATED, "1 Kgs 6:6, 8"),
          Dim("widths", "5 cubits on the lowest floor, 6 on the middle, "
              "7 on the third", STATED, "1 Kgs 6:6"),
          Dim("height", "5 cubits each", STATED, "1 Kgs 6:10"),
          Dim("offsets", "the house's wall steps in a cubit at each floor, "
              "so the beams rest on it and are not set into it", DERIVED,
              "1 Kgs 6:6"),
          Dim("outer wall", "not given; here five cubits, as Ezekiel's",
              NOT_GIVEN, "Ezek 41:9")),
         ("against the walls all round the holy place and the inner "
          "sanctuary", STATED, "1 Kgs 6:5"),
         "resting on the house with timber of cedar",
         _refs(planned="1 Chr 28:11-12",
               built="1 Kgs 6:5-6, 8, 10"),
         note="The door for the middle rooms was on the right side of the "
              "house, the south, and winding stairs went up from the "
              "middle floor to the third (1 Kings 6:8)."),
    Part("windows", "the windows", ("windows", "lattice"),
         None,
         (Dim("size", "not given", NOT_GIVEN, ""),
          Dim("kind", "of fixed lattice work", STATED, "1 Kgs 6:4")),
         ("not given; here high in the walls of the holy place, above the "
          "side rooms", NOT_GIVEN, ""),
         "",
         _refs(built="1 Kgs 6:4")),
    Part("oracle_doors", "the doors of the inner sanctuary",
         ("doors", "chains", "entrance"),
         (PARTITION_X, ORACLE_DOOR[0], PARTITION_X, ORACLE_DOOR[1]),
         (Dim("doors", "two, of olive wood", STATED, "1 Kgs 6:31-32"),
          Dim("posts", "a fifth part of the wall: 4 cubits, if a fifth of "
              "its 20", DERIVED, "1 Kgs 6:31"),
          Dim("chains", "of gold, drawn across before the inner sanctuary",
              STATED, "1 Kgs 6:21")),
         ("in the cedar wall between the holy place and the inner "
          "sanctuary", STATED, "1 Kgs 6:31"),
         "olive wood carved with cherubim, palm trees and open flowers, "
         "overlaid with gold, on hinges of gold",
         _refs(built="1 Kgs 6:21, 31-32; 7:50",
               chron="2 Chr 4:22")),
    Part("veil", "the veil", ("curtain", "veil"),
         None,
         (Dim("size", "not given", NOT_GIVEN, ""),),
         ("not given; Kings names doors at the inner sanctuary, and "
          "Chronicles a veil", NOT_GIVEN, ""),
         "blue, purple, crimson and fine linen, with cherubim on it",
         _refs(chron="2 Chr 3:14")),
    Part("house_doors", "the doors of the house", ("doors", "door posts",
                                                   "entrance"),
         (EAST_WALL[0], HOUSE_DOOR[0], EAST_WALL[1], HOUSE_DOOR[1]),
         (Dim("doors", "two, of cypress, each of two folding leaves",
              STATED, "1 Kgs 6:34"),
          Dim("posts", "of olive wood, a fourth part of the wall: 5 "
              "cubits, if a fourth of its 20", DERIVED, "1 Kgs 6:33"),
          Dim("height", "not given", NOT_GIVEN, "")),
         ("the entrance of the holy place, from the porch", STATED,
          "1 Kgs 6:33"),
         "cypress carved with cherubim, palm trees and open flowers, "
         "overlaid with gold, on hinges of gold",
         _refs(built="1 Kgs 6:33-35; 7:50",
               chron="2 Chr 4:22",
               later="2 Kgs 18:16; 2 Chr 28:24; 29:3")),
    Part("jachin", "Jachin", ("pillars", "pillar", "Jachin", "brass pillars"),
         None,
         _PILLAR_DIMS,
         ("at the porch, on the right: the south", STATED,
          "1 Kgs 7:21; 2 Chr 3:17"),
         "cast brass, the work of Hiram of Tyre",
         _pillar_refs(),
         note="Where it stands, before the porch or holding up its roof, "
              "is not given. Boaz is its fellow on the left."),
    Part("boaz", "Boaz", ("pillars", "pillar", "Boaz", "brass pillars"),
         None,
         _PILLAR_DIMS,
         ("at the porch, on the left: the north", STATED,
          "1 Kgs 7:21; 2 Chr 3:17"),
         "cast brass, the work of Hiram of Tyre",
         _pillar_refs(),
         note="Where it stands, before the porch or holding up its roof, "
              "is not given. Jachin is its fellow on the right."),
    Part("altar", "the bronze altar", ("altar of brass", "altar of burnt "
                                       "offering", "bronze altar"),
         ALTAR,
         (Dim("length", "20 cubits", STATED, "2 Chr 4:1"),
          Dim("width", "20 cubits", STATED, "2 Chr 4:1"),
          Dim("height", "10 cubits", STATED, "2 Chr 4:1"),
          Dim("in Kings", "named, but not measured", NOT_GIVEN, "1 Kgs 8:64")),
         ("before the house, in the court; the distance is not given",
          STATED, "2 Kgs 16:14"),
         "brass",
         _refs(chron="2 Chr 4:1",
               dedicated="1 Kgs 8:22, 54, 64; 2 Chr 7:7",
               later="2 Kgs 16:14-15",
               named="1 Kgs 9:25; 2 Chr 8:12; Joel 2:17"),
         note="At the dedication it was too small for the offerings, and "
              "Solomon made the middle of the court holy for them (1 Kings "
              "8:64)."),
    Part("platform", "the bronze scaffold", ("platform", "scaffold"),
         PLATFORM,
         (Dim("length", "5 cubits", STATED, "2 Chr 6:13"),
          Dim("width", "5 cubits", STATED, "2 Chr 6:13"),
          Dim("height", "3 cubits", STATED, "2 Chr 6:13")),
         ("in the middle of the court; here before the altar", STATED,
          "2 Chr 6:13"),
         "brass",
         _refs(dedicated="2 Chr 6:12-13"),
         use="Solomon stood and knelt on it to pray at the dedication "
             "(2 Chronicles 6:13)"),
    Part("sea", "the molten sea", ("sea", "bronze sea", "molten sea",
                                   "oxen", "bulls"),
         SEA,
         (Dim("across", "10 cubits from brim to brim", STATED, "1 Kgs 7:23"),
          Dim("height", "5 cubits", STATED, "1 Kgs 7:23"),
          Dim("round", "a line of 30 cubits", STATED, "1 Kgs 7:23"),
          Dim("thickness", "a handbreadth, its brim like a lily's", STATED,
              "1 Kgs 7:26"),
          Dim("held", "2,000 baths", STATED, "1 Kgs 7:26"),
          Dim("held, in Chronicles", "3,000 baths", STATED, "2 Chr 4:5"),
          Dim("oxen", "twelve, three facing each way, hindquarters inward",
              STATED, "1 Kgs 7:25"),
          Dim("under the brim", "buds in two rows (Chronicles: oxen), cast "
              "with it", STATED, "1 Kgs 7:24; 2 Chr 4:3")),
         ("on the right side of the house, eastward, toward the south",
          STATED, "1 Kgs 7:39; 2 Chr 4:10"),
         "cast brass, the work of Hiram of Tyre",
         _refs(built="1 Kgs 7:23-26, 39, 44",
               chron="2 Chr 4:2-6, 10, 15",
               later="2 Kgs 16:17; 25:13, 16; Jer 52:17, 20"),
         use="for the priests to wash in (2 Chronicles 4:6)"),
    Part("bases", "the bases and the basins", ("bases", "basins", "stands",
                                               "lavers", "wheels"),
         None,
         (Dim("bases", "ten, each 4 by 4 cubits and 3 high", STATED,
              "1 Kgs 7:27"),
          Dim("wheels", "four, each a cubit and a half high, like a "
              "chariot's", STATED, "1 Kgs 7:30, 32-33"),
          Dim("panels", "with lions, oxen and cherubim, and wreaths",
              STATED, "1 Kgs 7:28-29, 36"),
          Dim("mouth", "a cubit within, a cubit and a half round", STATED,
              "1 Kgs 7:31"),
          Dim("band", "half a cubit high, round the top", STATED,
              "1 Kgs 7:35"),
          Dim("basins", "ten, one on each base, each 4 cubits and holding "
              "40 baths", STATED, "1 Kgs 7:38")),
         ("five on the right side of the house and five on the left; their "
          "spots there are not given", STATED, "1 Kgs 7:39; 2 Chr 4:6"),
         "cast brass, the work of Hiram of Tyre",
         _refs(built="1 Kgs 7:27-39, 43",
               chron="2 Chr 4:6, 14",
               later="2 Kgs 16:17; 25:13, 16; Jer 52:17, 20"),
         use="to wash the things that belonged to the burnt offering "
             "(2 Chronicles 4:6)"),
    Part("lamp_stands", "the lamp stands", ("lampstands", "menorah",
                                            "lamp stands", "lamps"),
         None,
         (Dim("number", "ten", STATED, "1 Kgs 7:49"),
          Dim("size", "not given", NOT_GIVEN, "")),
         ("five on the right and five on the left, before the inner "
          "sanctuary; their spots are not given", STATED,
          "1 Kgs 7:49; 2 Chr 4:7"),
         "pure gold, with flowers, lamps and tongs of gold",
         _refs(planned="1 Chr 28:15",
               built="1 Kgs 7:49",
               chron="2 Chr 4:7, 20-21",
               later="Jer 52:19")),
    Part("tables", "the tables", ("tables", "show bread", "table of show "
                                  "bread"),
         None,
         (Dim("number", "ten", STATED, "2 Chr 4:8"),
          Dim("size", "not given; drawn at the Tabernacle's 2 by 1",
              NOT_GIVEN, "")),
         ("five on the right and five on the left, in the temple; their "
          "spots are not given", STATED, "2 Chr 4:8"),
         "gold",
         _refs(planned="1 Chr 28:16",
               built="1 Kgs 7:48",
               chron="2 Chr 4:8, 19"),
         note="Kings names one table, \"the table that the show bread was "
              "on\" (1 Kings 7:48); Chronicles ten (2 Chronicles 4:8)."),
    Part("incense_altar", "the golden altar", ("altar of incense",
                                               "incense altar",
                                               "golden altar"),
         INCENSE_ALTAR,
         (Dim("size", "not given; drawn at the Tabernacle's 1 by 1",
              NOT_GIVEN, ""),),
         ("before the inner sanctuary, to which it belonged", DERIVED,
          "1 Kgs 6:22"),
         "cedar, overlaid with gold",
         _refs(planned="1 Chr 28:18",
               built="1 Kgs 6:20, 22; 7:48",
               chron="2 Chr 4:19",
               later="2 Chr 26:16")),
    Part("ark", "the ark of Yahweh's covenant", ("ark", "ark of the covenant",
                                                 "poles", "tablets"),
         ARK,
         (Dim("length", "2½ cubits", STATED, "Exod 25:10"),
          Dim("width", "1½ cubits", STATED, "Exod 25:10"),
          Dim("height", "1½ cubits", STATED, "Exod 25:10"),
          Dim("poles", "so long that their ends were seen from the holy "
              "place, but not outside", STATED, "1 Kgs 8:8")),
         ("in the inner sanctuary, under the cherubim's wings", STATED,
          "1 Kgs 8:6"),
         "acacia wood overlaid with gold; nothing in it but the two stone "
         "tablets Moses put there at Horeb",
         _refs(built="1 Kgs 6:19",
               dedicated="1 Kgs 8:1-9, 21; 2 Chr 5:2-10")),
    Part("cherubim", "the cherubim", ("cherubim", "cherub", "wings"),
         (CHERUBIM[0][0] - 1, 0, CHERUBIM[0][0] + 1, HOUSE[3]),
         (Dim("number", "two, of one measure and one form", STATED,
              "1 Kgs 6:23, 25"),
          Dim("height", "10 cubits each", STATED, "1 Kgs 6:23, 26"),
          Dim("wings", "5 cubits each, 10 from tip to tip", STATED,
              "1 Kgs 6:24"),
          Dim("all four", "20 cubits, wall to wall", STATED, "2 Chr 3:11-13")),
         ("in the inner sanctuary, standing on their feet and facing the "
          "house, a wing of each touching a wall and their other wings "
          "touching in the middle", STATED, "1 Kgs 6:27; 2 Chr 3:13"),
         "olive wood, overlaid with gold",
         _refs(planned="1 Chr 28:18",
               built="1 Kgs 6:23-28",
               chron="2 Chr 3:10-13",
               dedicated="1 Kgs 8:6-7; 2 Chr 5:7-8"),
         use="they spread their wings over the place of the ark (1 Kings "
             "8:7)"),
    Part("courts", "the courts", ("inner court", "great court", "court of "
                                  "the priests", "court"),
         INNER_COURT,
         (Dim("inner court", "size not given; walled with three courses of "
              "cut stone and a course of cedar beams", STATED, "1 Kgs 6:36"),
          Dim("great court", "size not given; walled the same way", STATED,
              "1 Kgs 7:12"),
          Dim("doors", "the great court's doors overlaid with brass", STATED,
              "2 Chr 4:9")),
         ("the inner court round the house; the great court round that, "
          "and round the king's house too", STATED, "1 Kgs 7:9, 12"),
         "cut stone and cedar",
         _refs(planned="1 Chr 28:12",
               built="1 Kgs 6:36; 7:12",
               chron="2 Chr 4:9",
               dedicated="1 Kgs 8:64; 2 Chr 7:7",
               later="2 Kgs 21:5; 23:12"),
         note="Chronicles calls the inner court the court of the priests "
              "(2 Chronicles 4:9)."),
]
PART = {p.key: p for p in PARTS}

# The Tabernacle, laid on the house at the same scale (a layer)
TABERNACLE_DIMS = (
    Dim("the tent", "30 by 10 cubits, 10 high: the house is twice as long, "
        "twice as wide and three times as high", DERIVED, "Exod 26:16-23"),
    Dim("the Most Holy Place", "a cube of 10 cubits; the inner sanctuary is "
        "one of 20", DERIVED, "Exod 26:33"),
    Dim("its court", "100 by 50 cubits", STATED, "Exod 27:18"),
)
TABERNACLE_VERSES = (("Brought up", "1 Kgs 8:4; 2 Chr 5:5"),)


def plan_point(key):
    p = PART[key].plan
    if len(p) == 2:
        return p
    return (p[0] + p[2]) / 2, (p[1] + p[3]) / 2
