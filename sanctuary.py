"""The Tabernacle as one model, in cubits.

Every drawing of the Tabernacle takes its court, tent and furnishings from
here: the Exodus 25-27 plan (generate_tabernacle.draw_plan and its hl_*
highlights), the small courts at the heart of the camp in Numbers 1-2 and
3-4, and the Tabernacle reference page (generate_tabernacle_reference.py).
Before this module each drew its own, and they disagreed about where the
altar, the basin and the tent stand.

**The plan frame.** x runs east from the west hanging, y south from the
north hanging, both in cubits; the court is (0, 0)-(100, 50) and its gate is
in the east (Exodus 27:13). `Plan` maps it onto a drawing at any scale, with
east to the right (the Exodus plan) or up (the camp in Numbers).
`Elevation` maps it onto the east face seen from the gate (the Tent of
Meeting at Shiloh, Joshua 18-19), with the tent's height and the door's
pillars from ELEVATION.

**What the text gives, and what it doesn't.** Each measurement is marked:

- STATED: the text gives the figure (the court is 100 by 50, 27:18);
- DERIVED: it follows from figures the text gives (the tent is 30 cubits
  long because twenty boards a cubit and a half wide stand on each side,
  26:16-18);
- NOT GIVEN: the text has no figure (the lamp stand and the basin have no
  size at all).

Placements are marked the same way. The text says which side a thing
stands on or what it stands between (the table on the north, the lamp
stand on the south, 26:35; the basin between the tent and the altar,
30:18), but it gives no distances inside the court. The spots used here
are one common arrangement: the tent stands 10 cubits from the west
hanging, the Most Holy Place is its western 10 cubits, the basin stands 10
cubits east of the door and the altar of burnt offering 35 cubits inside
the gate.

**The coordinates are the drawings' own literals** (13.75, 21.2, ...)
rather than computed values, so the Exodus 25-27 pictures, which print them
to two decimals, came out as they were where the model agreed with them.
It corrected two things there: the pillars, which are now sixty, one every
five cubits round the court with the gate's four at 20-35 (before, the plan
drew five uneven posts across the gate and its highlight four others); and
the Numbers 1-4 courts, which had put the altar, the basin and the tent
somewhere else. Pixel sizes for the things the text gives no size (the lamp
stand's and basin's marks) belong to each drawing, not to the model.

Names follow the WEB ("lamp stand", "basin", "brass", "mercy seat");
`aka` holds the common names a reader may search for.
"""

from typing import NamedTuple, Optional, Tuple

STATED, DERIVED, NOT_GIVEN = "stated", "derived", "not given"


# ---------------------------------------------------------------------------
# Drawing the plan frame
# ---------------------------------------------------------------------------

class Plan:
    """Plan cubits -> drawing pixels. (ox, oy) is where the court's
    north-west corner falls when east is to the right; with east up it is
    the court's north-east corner (the top-left of a court standing on its
    gate end), so the court still runs from (ox, oy) to the right and down.
    `s` is pixels per cubit."""

    def __init__(self, ox, oy, s, east="right"):
        assert east in ("right", "up")
        self.ox, self.oy, self.s, self.east = ox, oy, s, east

    def pt(self, x, y):
        if self.east == "right":
            return self.ox + x * self.s, self.oy + y * self.s
        return self.ox + y * self.s, self.oy + (COURT[2] - x) * self.s

    def box(self, x0, y0, x1, y1):
        """(left, top, width, height) of a plan rectangle."""
        (ax, ay), (bx, by) = self.pt(x0, y0), self.pt(x1, y1)
        return min(ax, bx), min(ay, by), abs(bx - ax), abs(by - ay)


class Elevation:
    """Plan cubits -> drawing pixels for the east face, as one sees it from
    outside the gate: north on the right, heights up. (ox, gy) is where the
    court's middle (y 25) meets the ground; `s` is pixels per cubit."""

    def __init__(self, ox, gy, s):
        self.ox, self.gy, self.s = ox, gy, s

    def x(self, y):
        return self.ox + ((COURT[1] + COURT[3]) / 2 - y) * self.s

    def y(self, height):
        return self.gy - height * self.s


# ---------------------------------------------------------------------------
# The court, the gate and the pillars                      (Exodus 27:9-19)
# ---------------------------------------------------------------------------

COURT = (0, 0, 100, 50)            # 100 by 50 cubits (27:18)
HANGING_HEIGHT = 5                 # "five cubits high" (27:18)
GATE = (15, 35)                    # y along the east side: 20 cubits (27:16)
FLANKS = ((0, 15), (35, 50))       # 15 cubits each side of it (27:14-15)

# Sixty pillars: twenty on the south, twenty on the north, ten on the west,
# and on the east three for each flank and four for the gate (27:10-16).
# The text gives the counts, not the spacing. A pillar every five cubits
# round the 300-cubit court makes exactly sixty when each side counts one
# corner as its own; on the east the flanks' posts are 5, 10, 15 and 40,
# 45, 50, and the screen hangs from the post at 15 across the gate's four.
GATE_PILLARS = (20, 25, 30, 35)
PILLARS = {
    "north": [(x, 0) for x in range(5, 101, 5)],
    "south": [(x, 50) for x in range(0, 100, 5)],
    "west": [(0, y) for y in range(0, 50, 5)],
    "east": [(100, y) for y in range(5, 51, 5)],
    "gate": [(100, y) for y in GATE_PILLARS],
}


def pillar_points():
    """Every pillar once, sixty: the order the plan draws them in."""
    return (PILLARS["north"] + PILLARS["south"] + PILLARS["west"]
            + PILLARS["east"])


# ---------------------------------------------------------------------------
# The tent                                                  (Exodus 26)
# ---------------------------------------------------------------------------

TENT = (10, 20, 40, 30)            # 30 by 10, 10 cubits from the west hanging
VEIL_X = 20                        # the veil, 10 cubits inside the west wall
DOOR_X = 40                        # the door screen, the tent's east end
MOST_HOLY = (10, 20, VEIL_X, 30)
HOLY_PLACE = (VEIL_X, 20, DOOR_X, 30)

# Standing it up: the plan has no heights but the hangings', so a drawing of
# the Tabernacle seen from the side takes these. Each is marked in ELEVATION.
TENT_HEIGHT = 10                   # a board's length (26:16)
# the screen for the door hangs on five pillars (26:37): the text gives the
# count, not the spacing, so here they stand evenly across the door, one at
# each corner
DOOR_PILLARS = tuple((DOOR_X, TENT[1] + k * (TENT[3] - TENT[1]) / 4)
                     for k in range(5))
ELEVATION = {
    "tent height": (f"{TENT_HEIGHT} cubits, the length of a board", DERIVED,
                    "Exod 26:16"),
    "door pillars": ("five", STATED, "Exod 26:37"),
    "door pillar spacing": ("not given; here evenly, one at each corner",
                            NOT_GIVEN, ""),
    "the tent's top": ("not given; here flat, the coverings laid over it",
                       NOT_GIVEN, ""),
}


# ---------------------------------------------------------------------------
# The parts, for cards and labels
# ---------------------------------------------------------------------------

class Dim(NamedTuple):
    what: str                      # "length", "height", "curtains", ...
    value: str                     # as said: "2½ cubits", "ten, 28 by 4"
    flag: str                      # STATED | DERIVED | NOT_GIVEN
    ref: str                       # where the text says it ("" if not)


class Part(NamedTuple):
    key: str
    name: str                      # WEB's wording
    aka: Tuple[str, ...]           # other names a reader may search for
    # On the plan: a rectangle (x0, y0, x1, y1) in plan cubits, or a point
    # (x, y) for a thing the text gives no size.
    plan: Optional[tuple]
    dims: Tuple[Dim, ...]
    place: Tuple[str, str, str]    # (where it stands, flag, ref)
    material: str
    carried: str                   # who carried it on the march (Numbers 4)
    verses: Tuple[Tuple[str, str], ...]    # (group, ref string)
    note: str = ""


def _refs(**groups):
    order = ("commanded", "made", "set_up", "named")
    label = {"commanded": "Commanded", "made": "Made", "set_up": "Set up",
             "named": "Also named"}
    return tuple((label[g], groups[g]) for g in order if g in groups)


PARTS = [
    Part("court", "the court", ("courtyard", "hangings", "pillars"),
         COURT,
         (Dim("length", "100 cubits, north and south", STATED, "Exod 27:9-11"),
          Dim("width", "50 cubits, west and east", STATED, "Exod 27:12-13"),
          Dim("height", "5 cubits, of fine twined linen", STATED, "Exod 27:18"),
          Dim("pillars", "twenty on the south, twenty on the north, ten on "
              "the west, and on the east three, three and four for the gate",
              STATED, "Exod 27:10-16"),
          Dim("pillars in all", "sixty", DERIVED, "Exod 27:10-16"),
          Dim("spacing", "a pillar every five cubits, each corner counted "
              "once", DERIVED, "")),
         ("around the tabernacle; the text gives no distances inside it",
          STATED, "Exod 27:17; 40:8, 33"),
         "fine twined linen; pillars on sockets of brass, with silver hooks "
         "and fillets", "Merari, the pillars, sockets, pins and cords; "
         "Gershon, the hangings",
         _refs(commanded="Exod 27:9-15, 17-19", made="Exod 38:9-17, 20",
               set_up="Exod 40:8, 33",
               named="Exod 35:17-18; 39:40; Num 3:26, 37; 4:26, 32")),
    Part("gate", "the screen for the gate of the court", ("gate", "entrance"),
         (100, GATE[0], 100, GATE[1]),
         (Dim("width", "20 cubits", STATED, "Exod 27:16"),
          Dim("height", "5 cubits", STATED, "Exod 38:18"),
          Dim("pillars", "four, on four sockets", STATED, "Exod 27:16")),
         ("in the middle of the east side", STATED, "Exod 27:13-16"),
         "blue, purple, scarlet and fine twined linen, the work of the "
         "embroiderer", "Gershon",
         _refs(commanded="Exod 27:16", made="Exod 38:18-19",
               set_up="Exod 40:8, 33",
               named="Exod 35:17; 39:40; Num 3:26; 4:26")),
    Part("tent", "the tabernacle", ("tent", "tent of meeting", "boards"),
         TENT,
         (Dim("length", "30 cubits: twenty boards on each side, each a "
              "cubit and a half wide", DERIVED, "Exod 26:16-20"),
          Dim("width", "10 cubits: six boards on the west, and two for "
              "the corners", DERIVED, "Exod 26:22-23"),
          Dim("height", "10 cubits, the length of a board", DERIVED,
              "Exod 26:16"),
          Dim("boards", "twenty on the south, twenty on the north, six on "
              "the west and two for its corners, each 10 by 1½ cubits, with "
              "two tenons", STATED, "Exod 26:16-25"),
          Dim("boards in all", "48", DERIVED, "Exod 26:18-25"),
          Dim("bars", "five for each side, the middle bar passing through "
              "from end to end", STATED, "Exod 26:26-28")),
         ("in the court; the text gives no distance from the hangings, and "
          "here it stands 10 cubits from the west", NOT_GIVEN, ""),
         "boards of acacia wood overlaid with gold, on sockets of silver",
         "Merari, the boards, bars, pillars and sockets",
         _refs(commanded="Exod 26:15-30", made="Exod 36:20-34",
               set_up="Exod 40:2, 17-19",
               named="Exod 30:26; 31:7; 35:11; 39:33; 40:9; Lev 8:10; "
                     "Num 3:36; 4:31; 7:1")),
    Part("coverings", "the curtains and coverings", ("curtains", "covering",
                                                     "goats' hair"),
         None,
         (Dim("linen curtains", "ten, each 28 by 4 cubits, with cherubim",
              STATED, "Exod 26:1-2"),
          Dim("goats' hair curtains", "eleven, each 30 by 4 cubits", STATED,
              "Exod 26:7-8"),
          Dim("rams' skins dyed red", "size not given", NOT_GIVEN,
              "Exod 26:14"),
          Dim("sea cow hides", "size not given", NOT_GIVEN, "Exod 26:14")),
         ("over the boards, the tent's roof and sides", STATED,
          "Exod 26:7, 13"),
         "fine twined linen, blue, purple and scarlet; goats' hair; rams' "
         "skins; sea cow hides", "Gershon",
         _refs(commanded="Exod 26:1-14", made="Exod 36:8-19",
               set_up="Exod 40:19",
               named="Exod 35:11; 39:34; Num 3:25; 4:25")),
    Part("most_holy", "the Most Holy Place", ("holy of holies",),
         MOST_HOLY,
         (Dim("size", "10 by 10 by 10 cubits", DERIVED, "Exod 26:33"),),
         ("within the veil, at the tent's west end: its far part is "
          "westward and its front faces the sunrise", DERIVED,
          "Exod 26:22-23, 33; Num 3:38"),
         "", "",
         _refs(named="Exod 26:33-34; Lev 16:2"),
         note="The veil hangs under the clasps (26:33), which puts it 20 "
              "cubits from the door and makes the Most Holy Place a cube."),
    Part("holy_place", "the holy place", ("holy place",),
         HOLY_PLACE,
         (Dim("size", "20 by 10 by 10 cubits", DERIVED, "Exod 26:33"),),
         ("between the veil and the door", STATED, "Exod 26:33, 35"),
         "", "",
         _refs(named="Exod 26:33, 35")),
    Part("veil", "the veil", ("curtain", "veil"),
         (VEIL_X, 20, VEIL_X, 30),
         (Dim("size", "not given", NOT_GIVEN, ""),
          Dim("pillars", "four of acacia overlaid with gold, on sockets of "
              "silver", STATED, "Exod 26:32")),
         ("under the clasps, between the holy place and the Most Holy",
          STATED, "Exod 26:33"),
         "blue, purple, scarlet and fine twined linen, with cherubim",
         "Kohath, over the ark, after the priests had covered it with "
         "the veil",
         _refs(commanded="Exod 26:31-33", made="Exod 36:35-36",
               set_up="Exod 40:3, 21",
               named="Exod 35:12; 39:34; Lev 16:2, 12, 15; Num 4:5")),
    Part("door", "the screen for the door of the tent", ("door", "screen"),
         (DOOR_X, 20, DOOR_X, 30),
         (Dim("size", "not given", NOT_GIVEN, ""),
          Dim("pillars", "five of acacia overlaid with gold, on sockets of "
              "brass", STATED, "Exod 26:37")),
         ("at the tent's east end, facing the sunrise", DERIVED,
          "Exod 26:22; Num 3:38"),
         "blue, purple, scarlet and fine twined linen, the work of the "
         "embroiderer", "Gershon",
         _refs(commanded="Exod 26:36-37", made="Exod 36:37-38",
               set_up="Exod 40:5, 28",
               named="Exod 35:15; 39:38; Num 3:25; 4:25")),
    Part("ark", "the ark of the testimony", ("ark", "ark of the covenant"),
         (13.75, 24.25, 16.25, 25.75),
         (Dim("length", "2½ cubits", STATED, "Exod 25:10"),
          Dim("width", "1½ cubits", STATED, "Exod 25:10"),
          Dim("height", "1½ cubits", STATED, "Exod 25:10")),
         ("within the veil; its spot there is not given", STATED,
          "Exod 26:33; 40:21"),
         "acacia wood overlaid with pure gold, with rings and poles",
         "Kohath, covered with the veil",
         _refs(commanded="Exod 25:10-16, 21-22", made="Exod 37:1-5",
               set_up="Exod 40:3, 20-21",
               named="Exod 26:33-34; 30:26; 31:7; 35:12; 39:35; Lev 16:2; "
                     "Num 3:31; 4:5-6; 7:89")),
    Part("mercy_seat", "the mercy seat and the cherubim",
         ("mercy seat", "cherubim", "atonement cover"),
         (13.75, 24.25, 16.25, 25.75),
         (Dim("length", "2½ cubits", STATED, "Exod 25:17"),
          Dim("width", "1½ cubits", STATED, "Exod 25:17"),
          Dim("cherubim", "two, of beaten gold, at its ends; size not given",
              NOT_GIVEN, "Exod 25:18-20")),
         ("on the ark", STATED, "Exod 25:21"),
         "pure gold", "Kohath",
         _refs(commanded="Exod 25:17-22", made="Exod 37:6-9",
               set_up="Exod 40:20",
               named="Exod 26:34; 31:7; 35:12; 39:35; Lev 16:2, 13-15; "
                     "Num 7:89")),
    Part("table", "the table", ("table of showbread", "bread of the presence"),
         (29, 21.2, 31, 22.2),
         (Dim("length", "2 cubits", STATED, "Exod 25:23"),
          Dim("width", "1 cubit", STATED, "Exod 25:23"),
          Dim("height", "1½ cubits", STATED, "Exod 25:23"),
          Dim("rim", "a handbreadth", STATED, "Exod 25:25")),
         ("on the north side of the holy place; its spot there is not given",
          STATED, "Exod 26:35; 40:22"),
         "acacia wood overlaid with pure gold", "Kohath",
         _refs(commanded="Exod 25:23-30", made="Exod 37:10-16",
               set_up="Exod 40:4, 22-23",
               named="Exod 26:35; 30:27; 31:8; 35:13; 39:36; "
                     "Lev 24:5-9; Num 3:31; 4:7-8")),
    Part("lamp_stand", "the lamp stand", ("lampstand", "menorah", "lamp"),
         (30, 28),
         (Dim("size", "not given; it took a talent of pure gold", NOT_GIVEN,
              "Exod 25:39"),
          Dim("lamps", "seven", STATED, "Exod 25:37")),
         ("on the south side of the holy place, opposite the table", STATED,
          "Exod 26:35; 40:24"),
         "pure gold, of beaten work", "Kohath",
         _refs(commanded="Exod 25:31-39", made="Exod 37:17-24",
               set_up="Exod 40:4, 24-25",
               named="Exod 26:35; 27:20-21; 30:7-8, 27; 31:8; 35:14; "
                     "39:37; Lev 24:2-4; Num 3:31; 4:9-10; 8:2-4")),
    Part("incense_altar", "the altar of incense",
         ("golden altar", "altar of incense", "incense altar"),
         (22, 24.5, 23, 25.5),
         (Dim("length", "1 cubit", STATED, "Exod 30:2"),
          Dim("width", "1 cubit", STATED, "Exod 30:2"),
          Dim("height", "2 cubits, with horns", STATED, "Exod 30:2")),
         ("before the veil; its spot there is not given", STATED,
          "Exod 30:6; 40:26"),
         "acacia wood overlaid with pure gold", "Kohath",
         _refs(commanded="Exod 30:1-10", made="Exod 37:25-28",
               set_up="Exod 40:5, 26-27",
               named="Exod 30:27; 31:8; 35:15; 39:38; Num 3:31; 4:11")),
    Part("basin", "the basin of brass", ("laver", "basin", "washing"),
         (50, 25),
         (Dim("size", "not given; it was made from the mirrors of the "
              "serving women", NOT_GIVEN, "Exod 38:8"),),
         ("between the Tent of Meeting and the altar; the distance is not "
          "given", STATED, "Exod 30:18; 40:30"),
         "brass, with a base of brass", "not named in Numbers 4",
         _refs(commanded="Exod 30:17-21", made="Exod 38:8",
               set_up="Exod 40:7, 30-32",
               named="Exod 30:28; 31:9; 35:16; 39:39; 40:11; Lev 8:11")),
    Part("altar", "the altar of burnt offering",
         ("bronze altar", "brass altar", "altar of burnt offering"),
         (62.5, 22.5, 67.5, 27.5),
         (Dim("length", "5 cubits", STATED, "Exod 27:1"),
          Dim("width", "5 cubits", STATED, "Exod 27:1"),
          Dim("height", "3 cubits, with horns, and a grating halfway down",
              STATED, "Exod 27:1-5")),
         ("before the door of the tabernacle of the Tent of Meeting; the "
          "distance is not given", STATED, "Exod 40:6, 29"),
         "acacia wood overlaid with brass", "Kohath",
         _refs(commanded="Exod 27:1-8", made="Exod 38:1-7",
               set_up="Exod 40:6, 29",
               named="Exod 29:12; 30:28; 31:9; 35:16; 39:39; 40:10; "
                     "Lev 8:11, 15; 9:7-24; Num 3:31; 4:13-14; 7:1")),
]
PART = {p.key: p for p in PARTS}


def plan_box(key):
    """A part's plan rectangle (x0, y0, x1, y1) in cubits."""
    box = PART[key].plan
    assert box is not None and len(box) == 4, key
    return box


def plan_point(key):
    """The centre of a part on the plan, in cubits."""
    p = PART[key].plan
    if len(p) == 2:
        return p
    return (p[0] + p[2]) / 2, (p[1] + p[3]) / 2


# ---------------------------------------------------------------------------
# The camp round it                                    (Numbers 2 and 3)
# ---------------------------------------------------------------------------

# The Levites camp next to the tabernacle, Moses and Aaron at its east, and
# the twelve tribes round them by their standards.
LEVITE_CAMP = {
    "east": ("Moses, and Aaron and his sons", "Num 3:38"),
    "south": ("Kohath", "Num 3:29"),
    "west": ("Gershon", "Num 3:23"),
    "north": ("Merari", "Num 3:35"),
}
TRIBE_CAMP = {
    "east": ("Judah", ("Judah", "Issachar", "Zebulun"), "Num 2:3-9"),
    "south": ("Reuben", ("Reuben", "Simeon", "Gad"), "Num 2:10-16"),
    "west": ("Ephraim", ("Ephraim", "Manasseh", "Benjamin"), "Num 2:18-24"),
    "north": ("Dan", ("Dan", "Asher", "Naphtali"), "Num 2:25-31"),
}
# What each clan of Levi carried on the march (Numbers 4).
CARRIED = {
    "Kohath": ("the ark, the table, the lamp stand, the altars, the "
               "vessels of the sanctuary and the screen, each covered first "
               "by the priests",
               "Num 3:31; 4:4-15"),
    "Gershon": ("the curtains, the tent's coverings, the screens for the "
                "door and the gate, and the hangings of the court",
                "Num 3:25-26; 4:24-26"),
    "Merari": ("the boards, bars, pillars and sockets of the tabernacle, "
               "and the court's pillars, sockets, pins and cords",
               "Num 3:36-37; 4:31-32"),
}
