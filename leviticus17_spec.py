"""The verse plan of the Leviticus 1-7 offerings pictures: data only.

generate_leviticus17_svg.py reads this module and draws one file a verse
(or a range, RANGES) as a camera over one world sheet: the Tabernacle
reference page's court plan and offerings table at their own coordinates,
and the stations round them (leviticus17_stations). Nothing here draws;
the design is docs/design/leviticus-1-7.md.

The verse format
----------------

    VERSES[(c, v)] = V(stops, beast="", note="")      one verse's file
    VERSES[(c, v1, v2)] = V(...)                       a range file (RANGES)

A verse is a list of STOPS, each a shot the camera flies to and rests on,
with the BEATS that happen while it is there:

    V(S("plan:altar",
        ("light", "plan.priests", "Aaron's"),
        ("light", "plan.ring", "around")),
      S("cell:burnt:blood",
        ("light", "burnt.blood:around the altar", "@")))

Each file starts where the file before it ends (the last stop of the
previous verse, in canonical order), so the stops are only where this
verse goes. A verse with no stops holds the previous shot. Every file
1:1-7:38 has its plan here; `stub()` (a plan not written yet, which holds)
is refused by test_leviticus17.

`beast` names the animal of the parts board (B) and the cast's close-up
(C.head): "bull", "sheep", "ram" or "goat" (and "lamb", "fgoat" on C).

Shots
-----
- "plan:court", "plan:tent", "plan:door", "plan:altar", "plan:camp": SHOTS
  below, world px (s, x, y): world point (x, y) at the screen's centre at
  scale s;
- "col:<offering>": a column of the table, its header and BROUGHT, s 1.0;
- "cell:<offering>:<row>": one cell, s 1.4; rows are brought, burns,
  blood, eaten, not_eaten, when;
- "cells:<offering>:<row1>:<row2>": the cells from row1 to row2, fitted;
- "table": the whole table, s 0.45;
- "<St>" a station whole at s 1 ("A"), "<St>.<shot>" one of its close-ups
  ("A.fire", "B.inner", "C.head"): each station's `shots()`.

Beats
-----
A beat is (verb, target, cue) or (verb, target, cue, {options}).

Verbs:
- "light": the target comes in. The first time it is lit (in canonical
  order) it is drawn in on its cue, its veil fades if it is a table unit,
  and its outline pulses once; after that it is drawn from the first frame
  and "light" puts a steady outline on it instead (current again). So the
  spec says only what the verse names; whether that is new is worked out.
- "pulse": one pulse of the target's outline, new or not.
- "current": a steady outline, no pulse.
- "move": a token's walk (the target's own path), shown at the stop's
  arrival (or options "show": a cue) and moving on the cue.
- "flare": the altar's fire flares once (A.fire).
- "not": the not-mark traced over the target.
- "hud": the title plate changes to the target text ("sin offering").
- "forgiven": the HUD's "forgiven" chip comes in (target None; FORGIVEN
  is the whole beat).

Cues:
- a word or phrase of the verse, matched whole (a capital means that very
  word; a small letter matches either case; curly quotes are straightened,
  so "Aaron's" is "Aaron’s"); "pieces#2" is its second time. A cue the
  verse doesn't say fails the build (KeyError). The beat starts 0.1 s
  before the word is said, and never before the camera reaches its stop;
- "@": when the camera reaches the stop; "@+0.4" a little after;
- "word+0.5": after the word;
- "t=2.5": at 2.5 s.

Targets
-------
"<station>.<name>" for a station's things (leviticus17_stations: "A.fire",
"B.kidneys", "C.ox", "plan.ring"), and for the table's units:
- "<off>.head" the offering's name; "<off>.by" its by-line ("anyone");
- "<off>.thing:<key>" a drawn thing in BROUGHT (offerings.THINGS keys:
  "burnt.thing:bull");
- "<off>.<field>:<short>" an entry of burns, blood, eaten or not_eaten by
  its table label ("burnt.blood:around the altar"); when two entries share
  a label, "<off>.<field>:<short>|<who>";
- "sin.who:<who>" a sin offering rank's who-line, "sin.rank<n>" its group's
  line of what is brought (1-5, top down), "sin.icon<n>:<key>" its drawing;
- "<off>.when" the WHEN cell;
- "<off>.col" a column's frame, an outline only (pulse it: 4:1-2, 7:37).

State persists: what was lit stays lit, derived from this spec in
canonical order, so any subset of files renders as the whole run would.

The other tables
----------------
- RANGES: the nine range files (c, v1, v2).
- REACH: {unit: (c, v)}, where a unit is first lit when that isn't the
  first verse that offerings.py cites for it (a name said later than its
  row's first ref).
- EXCUSED: {(unit, (c, v)) or unit: reason}, a cited verse that doesn't
  light its unit.
- REACHED_OFFSCREEN: {unit: (c, v)}, a unit reached in a verse that can't
  afford the flight to it; it shows at full strength from the next file.
"""

from typing import NamedTuple, Tuple

BOOK = "Leviticus"
CHAPTERS = tuple(range(1, 8))

# The plan's rest cameras, world px (sanctuary.Plan(730, 440, 14)): the
# court is x 730-2130, y 440-1140, the tent x 870-1290, the altar
# 1605-1675 x 755-825.
SHOTS = {
    "plan:court": (0.7, 1430, 790),
    "plan:tent": (1.6, 1080, 790),
    "plan:door": (1.9, 1515, 800),           # left edge past the tent's "lamp stand"
    "plan:altar": (2.6, 1650, 772),
    "plan:camp": (0.5, 1600, 800),

    # The table two columns wide. A one-column frame ("col:", "cell:") puts
    # its edges inside the columns either side and cuts their words once
    # they are unveiled; at s 1.39 centred on the line between two columns
    # the frame holds those two whole and the words either side wholly
    # outside. Each y is one where the top and bottom edges cut no word of
    # the table, veiled or not. mp: meal | peace (x 3830), ps: peace | sin
    # (x 4190), st: sin | trespass (x 4550).
    "mp:head": (1.39, 3830, 1740),           # names, by-lines, two rows of things
    "mp:brought": (1.39, 3830, 1822),        # by-lines and the three rows of things
    "mp:burns": (1.39, 3830, 2226),          # ON THE ALTAR, with THE BLOOD
    "mp:eaten": (1.39, 3830, 2513),          # WHO EATS
    "mp:low": (1.39, 3830, 2600),            # WHO EATS, NOT EATEN, WHEN
    "ps:head": (1.39, 4190, 1740),
    "ps:burns": (1.39, 4190, 2226),
    "ps:blood": (1.39, 4190, 2416),
    "st:head": (1.39, 4550, 1745),           # the names, rank groups 1-4, trespass's things
    "st:brought": (1.39, 4550, 1847),        # sin's five rank groups
    "st:burns": (1.39, 4550, 2140),          # ON THE ALTAR, THE BLOOD down to the horns
    "st:altar": (1.39, 4550, 2217),          # ON THE ALTAR and THE BLOOD down to the side
    "st:eaten": (1.39, 4550, 2620),          # WHO EATS, NOT EATEN, WHEN
    "st:low": (1.39, 4550, 2605),
    # the gate, the camp edge and the clean place: plan:camp puts the clean
    # place's words past the right edge
    "st:out": (1.0, 2350, 830),
}

# A part's chip in the words of the verse that names it, where they aren't
# offerings.CUT's (B keeps it so in the later verses of its board).
CUT_WORDS = {
    (3, 9): {"fat_on": "fat on the inwards"},
    (7, 3): {"tail_fat": "the fat tail"},
}

# The camera before 1:1.
OPENING = "plan:court"

# Each station's top-left corner on the world sheet; every station is 1024
# x 576 (L, Sinai, is the far card to the west of the camp).
STATIONS = {
    "H": (330, 1400), "A": (1450, 1400),
    "C": (330, 2072), "B": (1450, 2072),
    "G": (2960, 2920), "K": (4080, 2920),
    "M": (2960, 100), "T": (4080, 100),
    "D": (2960, 772), "S": (4080, 772),
    "L": (-560, 100),
}

RANGES = [(4, 1, 2), (5, 13, 14), (5, 18, 19), (6, 7, 8), (6, 18, 19),
          (6, 23, 24), (7, 21, 22), (7, 27, 28), (7, 35, 36)]

# Where each case begins: a new beast or bringing (the herd, the flock, the
# birds; the ruler's goat, the common person's lamb...). The altar's stack
# and blood, the kitchen's not-marks and the cast are each case's own
# (leviticus17_stations.case_of), so the ram's fat isn't on the altar when
# the bird is burned, nor the lamb beside the goat of 3:12.
CASES = [(1, 1), (1, 3), (1, 10), (1, 14),
         (2, 1), (2, 4), (2, 11), (2, 14),
         (3, 1), (3, 6), (3, 12), (3, 17),
         (4, 1), (4, 13), (4, 22), (4, 27), (4, 32),
         (5, 1), (5, 7), (5, 11), (5, 14), (5, 17),
         (6, 1), (6, 8), (6, 14), (6, 19), (6, 24),
         (7, 1), (7, 11), (7, 22), (7, 28), (7, 37)]


class S(NamedTuple):
    """One stop: a shot and the beats while the camera is there."""
    shot: str
    beats: Tuple[tuple, ...] = ()


class V(NamedTuple):
    """One file's plan."""
    stops: Tuple[S, ...] = ()
    beast: str = ""
    stub: bool = False
    note: str = ""


def s(shot, *beats):
    return S(shot, tuple(beats))


def v(*stops, beast="", note=""):
    return V(tuple(stops), beast, False, note)


def stub(note=""):
    return V((), "", True, note)


# Where a unit is first lit, when that isn't the first verse offerings.py
# cites for it.
REACH = {
    "burnt.head": (1, 3),                    # "burnt offering" first at 1:3
    "burnt.burns:the whole": (1, 9),         # 1:8 is the pieces on the wood
    "burnt.burns:the whole bird": (1, 17),   # its row cites 1:15-17; 1:17 burns it whole
    "sin.blood:before the veil": (4, 7),     # 4:5-7; the cell is seen when 4:7 lands
    "sin.head": (4, 3),                      # "sin offering" first at 4:3
    "sin.rank3": (4, 32),                    # "a female goat or lamb": the lamb at 4:32
    "meal.thing:salt": (2, 13),
    "trespass.head": (5, 15),                # 5:14 is the formula
    "peace.eaten:the offerer": (7, 19),      # "everyone who is clean"
    "peace.eaten:the right thigh": (7, 33),
    # the entry's who-line names the congregation's bull, which is 4:13-21
    "sin.blood:before the veil/who": (4, 16),
    "burnt.when": (7, 37), "meal.when": (7, 37), "peace.when": (7, 37),
    "sin.when": (7, 37), "trespass.when": (7, 37),
    "peace.burns:the fat": (3, 5),            # 3:3-4 take it away; 3:5 burns it
    "peace.blood:around the altar": (3, 8),   # the plan unveils it at 3:8
    # its who-line, "from the herd, or a goat", names the goat of 3:12-16
    "peace.burns:the fat/who": (3, 16),
    "sin.burns:the fat|a bull": (4, 10),        # 4:8-10 name the fat; it burns at 4:10
    "sin.not_eaten:the bull: outside the camp": (4, 12),   # 4:11 lists; 4:12 carries it out
    "sin.rank2": (4, 23),                       # "a male goat" is said at 4:23
    # the who-lines name what is said later: "one of the people's" (4:27),
    # "a lamb" (4:32)
    "sin.blood:on the altar's horns/who": (4, 30),
    "sin.burns:the fat|a goat or a lamb/who": (4, 35),
    "sin.who:one guilty of 5:1–4": (5, 6),      # 5:5 is the confession; 5:6 brings the female
    "trespass.thing:silver": (5, 16),           # the plan unveils it with the fifth
    # 7:17 names the third day; its row's cell is reached at 7:18
    "peace.not_eaten:third day's meat": (7, 18),
    # the breast's who-line, "Aaron and his sons", is 7:31's words
    "peace.eaten:the breast/who": (7, 31),
}

EXCUSED = {
    ("peace.eaten:the right thigh", (7, 14)):
        "7:14 is the breads heaved to the priest; the thigh is 7:32-33",
    "burnt.when": "a summary; the five WHEN cells lift together at 7:37",
    "meal.when": "a summary; the five WHEN cells lift together at 7:37",
    "peace.when": "a summary; the five WHEN cells lift together at 7:37",
    "sin.when": "a summary; the five WHEN cells lift together at 7:37",
    "trespass.when": "a summary; the five WHEN cells lift together at 7:37",
    # cited verses shown on a station, the unit reached in an earlier file
    ("burnt.thing:bull", (1, 5)): "1:5 kills the bull: the blood ring and its cell",
    ("burnt.burns:the whole", (1, 12)): "the ram's pieces laid on the fire (B, A); reached at 1:9",
    ("burnt.burns:the whole", (1, 13)): "the ram burned whole on the fire (A); reached at 1:9",
    ("burnt.eaten:no one", (1, 13)): "the ram burned whole on the fire (A); reached at 1:9",
    ("burnt.blood:around the altar", (1, 11)): "the blood ring on the plan; reached at 1:5",
    ("burnt.not_eaten:the ashes: outside the camp", (6, 10)):
        "6:10 puts the ashes beside the altar (A, plan); 6:11 carries them out",
    ("meal.burns:a handful", (6, 15)): "the handful on G and the memorial on the fire (A); reached at 2:2",
    ("meal.burns:all of it", (6, 23)):
        "6:23-24's stop is the cell below it, a priest's own; reached at 6:22",
    ("meal.eaten:the priests|Aaron and his sons", (6, 17)): "most holy, on G; reached at 2:3",
    ("meal.eaten:the priests|Aaron and his sons", (6, 18)): "every male eats it, on G; reached at 2:3",
    ("peace.burns:the fat", (3, 14)): "the goat's fat on B; the cell is seen at 3:16",
    ("peace.burns:the fat", (3, 15)): "the goat's kidneys and fat on B; the cell is seen at 3:16",
    ("peace.burns:the fat, the tail", (3, 10)): "the sheep's kidneys and fat on B; reached at 3:9",
    ("peace.burns:the fat, the tail", (3, 11)): "the fat on the fire (A); reached at 3:9",
    ("peace.blood:around the altar", (3, 13)): "the goat at the door and the ring (plan); reached at 3:8",
    ("peace.eaten:the breast", (7, 30)): "the breast waved on B; reached off camera at 7:31",
    ("peace.eaten:the breast", (7, 34)): "the waved breast on B; reached off camera at 7:31",
    ("peace.not_eaten:the fat, the blood", (3, 16)): "3:16 burns the fat (A); the ban is 3:17's",
    ("peace.not_eaten:the fat, the blood", (7, 22)): "the bans on S; reached at 3:17",
    ("peace.not_eaten:the fat, the blood", (7, 23)): "the bans on S; reached at 3:17",
    ("peace.not_eaten:the fat, the blood", (7, 24)): "the bans on S; reached at 3:17",
    ("peace.not_eaten:the fat, the blood", (7, 25)): "the bans on S; reached at 3:17",
    ("peace.not_eaten:the fat, the blood", (7, 26)): "the bans on S; reached at 3:17",
    ("peace.not_eaten:the fat, the blood", (7, 27)): "the bans on S; reached at 3:17",
    ("peace.not_eaten:unclean meat", (7, 20)): "cut off, on D; reached off camera at 7:19",
    ("peace.not_eaten:unclean meat", (7, 21)): "cut off, on D; reached off camera at 7:19",
    ("sin.who:the anointed priest", (4, 4)): "the bull at the door and the hand on its head (plan, C)",
    ("sin.rank1", (4, 4)): "the bull at the door and the hand on its head (plan, C)",
    ("sin.who:the whole congregation", (4, 15)): "the elders' hands on the bull's head (C)",
    ("sin.rank1", (4, 15)): "the elders' hands on the bull's head (C)",
    ("sin.rank3", (5, 5)): "5:5 is the confession (M)",
    ("sin.burns:the fat|a bull", (4, 19)): "all its fat on the fire (A); reached at 4:10",
    ("sin.burns:the fat|a goat or a lamb", (4, 31)): "the fat on the fire (A); reached at 4:26",
    ("sin.burns:the fat|a goat or a lamb", (4, 35)): "the lamb's fat on B and the fire (A); reached at 4:26",
    ("sin.blood:before the veil", (4, 16)): "the blood's path to the veil (plan); reached at 4:7",
    ("sin.blood:before the veil", (4, 17)): "the seven drops before the veil (H); reached at 4:7",
    ("sin.blood:on the altar's horns", (4, 30)): "the horns and the base on A; reached at 4:25",
    ("sin.blood:on the altar's horns", (4, 34)): "the horns and the base on A; reached at 4:25",
    ("sin.eaten:the priests", (6, 29)): "every male eats it, on G; reached at 6:26",
    ("sin.not_eaten:the bull: outside the camp", (4, 21)):
        "the bull carried out to the clean place (plan); reached at 4:12",
    ("trespass.by", (5, 17)): "the one who sins is T's man",
    ("trespass.by", (6, 2)): "the one who sins is T's man",
    ("trespass.thing:ram", (6, 6)): "the ram to the priest on T; 'priest' is the verse's last word",
    ("trespass.burns:the fat", (7, 3)): "the ram's fat on B; reached off camera at 7:5",
    ("trespass.burns:the fat", (7, 4)): "the ram's kidneys and fat on B; reached off camera at 7:5",
    ("trespass.eaten:the priests", (7, 7)): "one law for both, on G; reached at 7:6",
}

REACHED_OFFSCREEN = {
    # a cell whose word comes too late in its verse for the flight to the
    # table (the flight would be a jump, or the stop unseen before the next
    # verse leaves): reached off camera, seen the next time a camera rests
    # there
    "burnt.blood:around the altar": (1, 5),
    "burnt.blood:around the altar/who": (1, 5),
    "burnt.blood:the altar's side": (1, 15),
    "burnt.blood:the altar's side/who": (1, 15),
    "meal.thing:cakes": (2, 4),
    "meal.thing:wafers": (2, 4),
    "peace.burns:the fat, the tail": (3, 9),
    "peace.burns:the fat, the tail/who": (3, 9),
    "sin.burns:the fat|a bull": (4, 10),
    "sin.burns:the fat|a bull/who": (4, 10),
    "sin.blood:on the altar's horns": (4, 25),
    "sin.blood:the altar's side": (5, 9),
    "sin.blood:the altar's side/who": (5, 9),
    "burnt.not_eaten:the ashes: outside the camp": (6, 11),
    "trespass.burns:the fat": (7, 5),
    "meal.eaten:the priest": (7, 9),
    "peace.thing:leavened bread": (7, 13),
    "peace.eaten:the breast": (7, 31),
    # 3:17's last word is "blood": no time left to fly to the cell
    "peace.not_eaten:the fat, the blood": (3, 17),
    "sin.blood:before the veil/who": (4, 16),
    "sin.blood:on the altar's horns/who": (4, 30),
    "sin.burns:the fat|a goat or a lamb/who": (4, 35),
    # 7:2's "around" comes too late for the flight; seen at 7:6
    "trespass.blood:around the altar": (7, 2),
    "trespass.blood:around the altar/who": (7, 2),
    # the who-lines of the core's off-camera entries
    "trespass.burns:the fat/who": (7, 5),
    "meal.eaten:the priest/who": (7, 9),
    "peace.eaten:the breast/who": (7, 31),
    # 7:12's third bread is the verse's end; seen at 7:29
    "peace.thing:cakes": (7, 12),
    "peace.thing:wafers": (7, 12),
    # 7:19's "clean" is the verse's end; seen at 7:33 and 7:37
    "peace.not_eaten:unclean meat": (7, 19),
    "peace.eaten:the offerer": (7, 19),
    "peace.eaten:the offerer/who": (7, 19),
}

# The title plate's "forgiven" chip (it has no target).
FORGIVEN = ("forgiven", None, "forgiven")


# ---------------------------------------------------------------------------
# The verses
# ---------------------------------------------------------------------------

VERSES = {
    # ---- Leviticus 1: the burnt offering -------------------------------
    (1, 1): v(S("plan:tent", (
        ("light", "plan.moses", "Moses"),
        ("pulse", "plan.tent", "Tent of Meeting")))),
    (1, 2): v(
        s("col:burnt", ("light", "burnt.by", "anyone")),
        s("C", ("light", "C.ox", "herd"),
          ("light", "C.sheep", "flock"),
          ("light", "C.goat", "flock+0.3"))),
    (1, 3): v(
        s("cell:burnt:brought",
          ("hud", "burnt offering", "burnt offering"),
          ("light", "burnt.head", "burnt offering"),
          ("light", "burnt.thing:bull", "herd")),
        s("plan:door", ("move", "plan.ox", "door", {"chip": "male"}))),
    (1, 4): v(
        s("C.head", ("light", "C.ox", "@"), ("light", "C.offerer", "@"),
          ("light", "C.hand", "hand"),
          ("pulse", "C.head", "head")),
        beast="bull"),
    (1, 5): v(
        s("plan:altar", ("light", "plan.priests", "Aaron's"),
          ("light", "plan.ring", "around"))),
    (1, 6): v(
        s("B", ("light", "B.skin", "flay"), ("light", "B.pieces", "pieces")),
        beast="bull"),
    (1, 7): v(s("A", ("light", "A.fire", "fire"),
                ("light", "A.wood", "wood"))),
    (1, 8): v(s("A.fire", ("light", "A.slot.pieces", "pieces"),
                ("light", "A.slot.head", "head"),
                ("light", "A.slot.fat", "fat"))),
    (1, 9): v(
        s("B", ("light", "B.innards", "innards"),
          ("light", "B.legs", "legs"),
          ("light", "B.water", "water")),
        s("A.fire", ("flare", "A.fire", "burn")),
        s("cells:burnt:burns:eaten",
          ("light", "burnt.burns:the whole", "@"),
          ("light", "burnt.eaten:no one", "@+0.4")),
        beast="bull"),
    # the cast on its words, then the icons ("male sheep", "male goat")
    # once "a male" is said
    (1, 10): v(
        s("C", ("light", "C.ram", "sheep"), ("light", "C.goat", "goats")),
        s("cell:burnt:brought",
          ("light", "burnt.thing:male sheep", "male"),
          ("light", "burnt.thing:male goat", "male+0.2"))),
    (1, 11): v(s("plan:altar", ("light", "plan.north", "north"),
                 ("move", "plan.sheep", "north"),
                 ("light", "plan.ring", "around"))),
    (1, 12): v(
        s("B", ("light", "B.pieces", "pieces"), ("light", "B.head", "head"),
          ("light", "B.fat", "fat")),
        s("A.fire", ("light", "A.slot.pieces", "order"),
          ("light", "A.slot.head", "order"),
          ("light", "A.slot.fat", "order")),
        beast="ram"),
    (1, 13): v(
        s("B", ("light", "B.innards", "innards"), ("light", "B.legs", "legs"),
          ("light", "B.water", "water")),
        s("A.fire", ("light", "A.whole", "whole"), ("flare", "A.fire", "burn")),
        beast="ram"),
    (1, 14): v(s("cell:burnt:brought",
                 ("light", "burnt.thing:turtledove", "turtledoves"),
                 ("light", "burnt.thing:pigeon", "pigeons"))),
    (1, 15): v(
        s("A.bird", ("light", "A.neck", "head"),
          ("light", "A.slot.bird", "burn"),
          ("light", "A.side", "drained"))),
    (1, 16): v(s("plan:altar", ("move", "plan.crop", "east", {"show": "crop"}),
                 ("light", "plan.ash", "ashes"))),
    (1, 17): v(
        s("A.bird", ("light", "A.wings", "wings"),
          ("light", "A.notdivided", "divide")),
        s("A.fire", ("light", "A.slot.bird", "burn"),
          ("flare", "A.fire", "burn")),
        s("cell:burnt:burns", ("light", "burnt.burns:the whole bird", "@"))),

    # ---- Leviticus 2: the meal offering ---------------------------------
    (2, 1): v(s("mp:head",
                ("light", "meal.by", "anyone"),
                ("hud", "meal offering", "meal offering"),
                ("light", "meal.head", "meal offering"),
                ("light", "meal.thing:fine flour", "fine flour"),
                ("light", "meal.thing:oil", "oil"),
                ("light", "meal.thing:frankincense", "frankincense"))),
    (2, 2): v(
        s("G.supplies", ("light", "G.oil", "@"), ("light", "G.flour", "@+0.2"),
          ("light", "G.frankincense", "@+0.4"),
          ("light", "G.handful", "handful"),
          ("move", "G.handful", "oil")),
        s("A.fire", ("flare", "A.fire", "burn"),
          ("light", "A.slot.memorial", "memorial")),
        s("mp:burns", ("light", "meal.burns:a handful", "@"))),
    # the table first (it is beside 2:2's last stop), then the split bar
    (2, 3): v(
        s("mp:eaten",
          ("light", "meal.eaten:the priests|Aaron and his sons", "Aaron's")),
        s("G", ("light", "G.memorial", "@"),
          ("light", "G.rest", "@+0.2"),
          ("light", "G.most_holy", "most holy"))),
    (2, 4): v(
        s("K.cook", ("light", "K.oven", "oven"),
          ("light", "K.cakes", "unleavened cakes"),
          ("light", "K.wafers", "unleavened wafers"))),
    (2, 5): v(
        s("K.cook", ("light", "K.griddle", "griddle"),
          ("light", "K.mixed", "mixed with oil"))),
    (2, 6): v(s("K.griddle", ("light", "K.cut", "pieces"),
                ("light", "K.oil", "oil"))),
    (2, 7): v(
        s("K.cook", ("light", "K.pan", "pan")),
        s("mp:head", ("current", "meal.thing:fine flour", "@"),
          ("current", "meal.thing:oil", "@+0.2"))),
    (2, 8): v(s("plan:door", ("move", "plan.bread", "priest", {"show": "meal offering"}),
                ("pulse", "plan.priests", "priest"))),
    (2, 9): v(s("A.fire", ("light", "A.slot.memorial", "memorial"),
                ("flare", "A.fire", "burn"))),
    (2, 10): v(
        s("G", ("light", "G.rest", "Aaron's")),
        s("mp:eaten",
          ("light", "meal.eaten:the priests|Aaron and his sons", "@"))),
    (2, 11): v(s("K.rules", ("light", "K.yeast", "yeast"),
                 ("light", "K.altar", "burn no"),
                 ("light", "K.not:yeast", "yeast#2"),
                 ("light", "K.honey", "honey"),
                 ("light", "K.not:honey", "honey+0.4"))),
    (2, 12): v(s("K.rules", ("light", "K.first_fruits", "first fruits"),
                 ("current", "K.altar", "altar"))),
    (2, 13): v(
        s("mp:brought", ("light", "meal.thing:salt", "salt")),
        s("K.rules", ("light", "K.salt", "@"),
          ("light", "K.covenant", "covenant"),
          ("light", "K.names", "all your offerings"))),
    # the icon on the first "first fruits", then the ears
    (2, 14): v(
        s("mp:head", ("light", "meal.thing:first fruits", "first fruits")),
        s("G.fruits", ("light", "G.fruits", "first fruits#2"),
          ("light", "G.parched", "parched"),
          ("light", "G.bruised", "bruised"))),
    (2, 15): v(s("G.fruits", ("light", "G.fruit_oil", "oil"),
                 ("light", "G.fruit_frankincense", "frankincense"))),
    (2, 16): v(
        s("A.fire", ("flare", "A.fire", "burn"),
          ("light", "A.slot.memorial", "memorial")),
        s("G.fruits", ("light", "G.part", "part#2"),
          ("light", "G.all_frankincense", "all its frankincense")),
        s("mp:burns", ("light", "meal.burns:part of it", "@"))),

    # ---- Leviticus 3: the peace offering --------------------------------
    (3, 1): v(
        s("ps:head", ("light", "peace.by", "his offering"),
          ("hud", "sacrifice of peace offerings", "peace offerings"),
          ("light", "peace.head", "peace offerings"),
          ("light", "peace.thing:herd", "female")),
        s("C", ("light", "C.ox", "@"),
          ("light", "C.chip:left:male or female", "@"))),
    (3, 2): v(
        s("C.head", ("light", "C.offerer", "@"), ("light", "C.hand", "hand"),
          ("pulse", "C.head", "head")),
        s("plan:door", ("move", "plan.ox", "door"),
          ("current", "plan.ring", "around")),
        beast="bull"),
    (3, 3): v(s("B", ("light", "B.fat_cover", "covers"),
                ("light", "B.fat_on", "all the fat")),
              beast="bull"),
    (3, 4): v(s("B.inner", ("light", "B.kidneys", "kidneys"),
                ("light", "B.kidney_fat", "loins"),
                ("light", "B.loins", "loins"),
                ("light", "B.liver_cover", "liver")),
              beast="bull"),
    (3, 5): v(
        s("A.fire", ("light", "A.slot.fat", "burn"),
          ("flare", "A.fire", "burn+0.2"),
          ("light", "A.slot.burnt", "burnt offering")),
        s("ps:burns", ("light", "peace.burns:the fat", "@"))),
    (3, 6): v(s("C", ("light", "C.sheep", "flock"),
                ("light", "C.goat", "flock+0.3"),
                ("light", "C.chip:mid:male or female", "female"))),
    (3, 7): v(s("ps:head", ("light", "peace.thing:lamb", "lamb"))),
    (3, 8): v(
        s("C.head", ("light", "C.lamb", "@"), ("light", "C.offerer", "@"),
          ("light", "C.hand", "hand"), ("pulse", "C.head", "head")),
        s("ps:blood", ("light", "peace.blood:around the altar", "around")),
        beast="lamb"),
    (3, 9): v(
        s("B", ("light", "B.tail_fat", "tail fat"),
          ("light", "B.backbone", "backbone"),
          ("light", "B.fat_cover", "covers"),
          ("light", "B.fat_on", "all the fat")),
        beast="sheep"),
    (3, 10): v(s("B.inner", ("light", "B.kidneys", "kidneys"),
                 ("light", "B.kidney_fat", "loins"),
                 ("light", "B.loins", "loins"),
                 ("light", "B.liver_cover", "liver")),
               beast="sheep"),
    # beast: the file opens on 3:10's board (the lamb's)
    (3, 11): v(s("A.fire", ("light", "A.slot.fat", "burn"),
                 ("flare", "A.fire", "burn+0.2"),
                 ("light", "A.chip:food", "food")),
               beast="sheep"),
    (3, 12): v(s("ps:head", ("light", "peace.thing:goat", "goat"))),
    (3, 13): v(
        s("C.head", ("light", "C.goat", "@"), ("light", "C.offerer", "@"),
          ("light", "C.hand", "hand"), ("pulse", "C.head", "head")),
        s("plan:door", ("move", "plan.goat", "Tent of Meeting", {"to": "door", "dur": 1.1}),
          ("current", "plan.ring", "around")),
        beast="goat"),
    (3, 14): v(s("B", ("light", "B.fat_cover", "covers"),
                 ("light", "B.fat_on", "all the fat")),
               beast="goat"),
    (3, 15): v(s("B.inner", ("light", "B.kidneys", "kidneys"),
                 ("light", "B.kidney_fat", "loins"),
                 ("light", "B.loins", "loins"),
                 ("light", "B.liver_cover", "liver")),
               beast="goat"),
    # beast: the file opens on 3:15's board (the goat's)
    (3, 16): v(
        s("A.fire", ("light", "A.slot.fat", "burn"),
          ("flare", "A.fire", "burn+0.2")),
        s("ps:burns", ("light", "peace.burns:the fat", "@")),
        beast="goat"),
    (3, 17): v(s("S.bans", ("light", "S.dwellings", "dwellings"),
                 ("light", "S.fat", "fat"), ("not", "S.fat", "fat"),
                 ("light", "S.blood", "blood"), ("not", "S.blood", "blood"))),

    # ---- Leviticus 4: the sin offering ---------------------------------
    # 4:1's 2.2 s formula; nothing unveiled ("sin offering" is first said
    # at 4:3); the column's frame pulses.
    (4, 1, 2): v(s("st:head", ("pulse", "sin.col", "@"))),
    (4, 3): v(s("st:head",
                ("light", "sin.who:the anointed priest", "anointed priest"),
                ("light", "sin.rank1", "young bull"),
                ("light", "sin.icon1:bull", "young bull"),
                ("light", "sin.head", "sin offering"),
                ("hud", "sin offering", "sin offering"))),
    (4, 4): v(
        s("plan:door", ("move", "plan.ox", "door", {"dur": 2.0})),
        s("C.head", ("light", "C.bull", "@"), ("light", "C.offerer", "@"),
          ("light", "C.hand", "hand"),
          ("pulse", "C.head", "head")),
        beast="bull"),
    # the path on "bring": "Tent of Meeting" ends the verse
    (4, 5): v(s("plan:tent", ("light", "plan.bloodpath", "bring"))),
    (4, 6): v(s("H.veil", ("light", "H.veil", "veil"),
                ("light", "H.drops", "seven times"))),
    (4, 7): v(
        s("H.incense", ("light", "H.incense", "incense"),
          ("light", "H.horns", "horns")),
        s("A", ("light", "A.pool", "base")),
        s("st:altar", ("light", "sin.blood:before the veil", "@"))),
    (4, 8): v(s("B", ("light", "B.fat_cover", "fat that covers"),
                ("light", "B.fat_on", "fat that is on")),
              beast="bull"),
    (4, 9): v(s("B.inner", ("light", "B.kidneys", "kidneys"),
                ("light", "B.kidney_fat", "loins"),
                ("light", "B.loins", "loins"),
                ("light", "B.liver_cover", "liver")),
              beast="bull"),
    (4, 10): v(
        s("A.fire", ("light", "A.slot.fat", "burn"),
          ("flare", "A.fire", "burn"))),
    (4, 11): v(s("B", ("light", "B.skin", "skin"), ("light", "B.meat", "meat"),
                 ("light", "B.head", "head"), ("light", "B.legs", "legs"),
                 ("light", "B.innards", "innards"), ("light", "B.dung", "dung")),
               beast="bull"),
    (4, 12): v(
        s("st:out", ("move", "plan.bull_out", "outside of the camp", {"dur": 2.1}),
          ("light", "plan.outpath", "outside of the camp"),
          ("light", "plan.clean", "clean place")),
        s("st:eaten",
          ("light", "sin.not_eaten:the bull: outside the camp", "@"))),
    (4, 13): v(s("st:head",
                 ("light", "sin.who:the whole congregation", "whole congregation"),
                 ("current", "sin.rank1", "@+0.3"))),
    (4, 14): v(
        s("st:head", ("light", "sin.icon1:bull", "young bull"),
          ("current", "sin.who:the whole congregation", "@"),
          ("current", "sin.rank1", "young bull"))),
    (4, 15): v(s("C.elders", ("light", "C.bull", "@"), ("light", "C.elders", "elders"),
                 ("light", "C.hand", "hands")),
               beast="bull"),
    (4, 16): v(s("plan:tent", ("light", "plan.bloodpath", "Tent of Meeting"))),
    (4, 17): v(s("H", ("light", "H.veil", "veil"),
                 ("pulse", "H.drops", "seven"))),
    (4, 18): v(
        s("H.incense", ("light", "H.horns", "horns")),
        s("A", ("light", "A.pool", "base"))),
    (4, 19): v(s("A.fire", ("light", "A.slot.fat", "burn"),
                 ("flare", "A.fire", "burn"),
                 ("light", "A.chip:all its fat", "All its fat"))),
    (4, 20): v(s("st:head",
                 ("pulse", "sin.who:the anointed priest", "as he did"),
                 ("pulse", "sin.who:the whole congregation", "with this"),
                 FORGIVEN)),
    (4, 21): v(s("st:out", ("move", "plan.bull_out", "outside the camp"),
                 ("light", "plan.clean", "outside the camp+0.4"))),
    (4, 22): v(s("st:head", ("light", "sin.who:a ruler", "ruler"))),
    (4, 23): v(s("st:head",
                 ("current", "sin.who:a ruler", "@"),
                 ("light", "sin.icon2:male goat", "goat"),
                 ("light", "sin.rank2", "male"))),
    (4, 24): v(
        s("C.head", ("light", "C.goat", "goat"),
          ("light", "C.offerer", "@"),
          ("light", "C.hand", "hand"),
          ("pulse", "C.head", "head")),
        s("plan:altar", ("light", "plan.north", "burnt offering")),
        beast="goat"),
    (4, 25): v(
        s("A", ("light", "A.horns", "horns"), ("light", "A.pool", "base"))),
    (4, 26): v(
        s("A.fire", ("light", "A.slot.fat", "fat"),
          ("flare", "A.fire", "burn")),
        s("st:burns", ("light", "sin.burns:the fat|a goat or a lamb", "@"),
          FORGIVEN)),
    (4, 27): v(s("st:head",
                 ("light", "sin.who:one of the common people", "common people"))),
    (4, 28): v(s("st:head",
                 ("current", "sin.who:one of the common people", "@"),
                 ("light", "sin.icon3:female goat", "female"))),
    (4, 29): v(s("plan:altar", ("move", "plan.fgoat", "kill"),
                 ("light", "plan.north", "burnt offering"))),
    (4, 30): v(s("A", ("light", "A.horns", "horns"), ("light", "A.pool", "base"))),
    (4, 31): v(s("A.fire", ("light", "A.slot.fat", "burn"),
                 ("flare", "A.fire", "burn"),
                 ("light", "A.chip:pleasant aroma", "pleasant aroma"), FORGIVEN)),
    (4, 32): v(s("st:head",
                 ("current", "sin.who:one of the common people", "@"),
                 ("light", "sin.icon3:lamb", "lamb"),
                 ("light", "sin.rank3", "lamb+0.3"))),
    (4, 33): v(s("plan:altar", ("move", "plan.lamb", "kill"),
                 ("light", "plan.north", "burnt offering"))),
    (4, 34): v(s("A", ("light", "A.horns", "horns"), ("light", "A.pool", "base"))),
    (4, 35): v(
        s("B", ("light", "B.tail_fat", "fat"), ("light", "B.kidneys", "fat"),
          ("light", "B.liver_cover", "fat")),
        s("A.fire", ("light", "A.slot.fat", "burn"),
          ("flare", "A.fire", "burn"), FORGIVEN),
        beast="sheep"),

    # ---- Leviticus 5: the causes, the poor, the trespass offering -------
    (5, 1): v(s("M.c1", ("light", "M.witness", "witness"),
                ("light", "M.seen", "seen"), ("light", "M.known", "known"))),
    (5, 2): v(s("M", ("light", "M.carcass", "carcass"),
                ("light", "M.unclean_animal", "unclean animal"),
                ("light", "M.unclean_livestock", "unclean livestock"),
                ("light", "M.creeping_things", "creeping things"))),
    (5, 3): v(s("M.c3", ("light", "M.uncleanness_of_man", "uncleanness of man"))),
    (5, 4): v(s("M", ("light", "M.evil", "evil"), ("light", "M.good", "good"),
                ("light", "M.oath", "oath"))),
    (5, 5): v(s("M", ("pulse", "M.cells", "one of these"),
                ("light", "M.confess", "confess"))),
    (5, 6): v(s("st:head",
                ("light", "sin.who:one guilty of 5:1–4", "female"),
                ("light", "sin.icon3:lamb", "lamb"),
                ("light", "sin.icon3:female goat", "goat"),
                ("current", "sin.rank3", "goat+0.3"),
                ("hud", "sin offering", "sin offering"))),
    (5, 7): v(
        s("st:head",
          ("light", "sin.who:can't afford a lamb", "can't afford a lamb"),
          ("light", "sin.icon4:turtledove", "turtledoves"),
          ("light", "sin.icon4:pigeon", "pigeons"),
          ("light", "sin.rank4", "pigeons+0.3")),
        s("A.bird", ("light", "A.bird", "one"), ("light", "A.bird2", "other"))),
    (5, 8): v(s("A.bird", ("pulse", "A.bird", "first"),
                ("pulse", "A.neck", "wring"),
                ("light", "A.notdivided", "sever"))),
    (5, 9): v(
        s("A", ("light", "A.side", "side"), ("light", "A.pool", "base"))),
    (5, 10): v(s("A.fire", ("light", "A.slot.bird", "burnt offering"),
                 ("flare", "A.fire", "burnt offering+0.3"), FORGIVEN)),
    (5, 11): v(
        s("st:brought",
          ("light", "sin.who:can't afford two turtledoves", "can't afford two turtledoves"),
          ("light", "sin.rank5", "tenth"),
          ("light", "sin.icon5:fine flour", "fine flour")),
        s("K.measure", ("light", "K.measure", "@"), ("light", "K.tenth", "@+0.3"),
          ("light", "K.flour", "@+0.6"),
          ("light", "K.jar", "no oil"), ("light", "K.not:oil", "no oil+0.4"),
          ("light", "K.cup", "frankincense"),
          ("light", "K.not:frankincense", "frankincense+0.4"))),
    (5, 12): v(
        s("G.supplies", ("not", "G.oil", "@+0.2"), ("not", "G.frankincense", "@+0.4"),
          ("light", "G.handful", "handful"),
          ("light", "G.memorial_portion", "memorial portion")),
        s("A.fire", ("light", "A.slot.memorial", "burn"),
          ("flare", "A.fire", "burn")),
        s("st:burns", ("light", "sin.burns:a handful", "@"))),
    (5, 13, 14): v(
        s("G.supplies", ("not", "G.oil", "@+0.2"), ("not", "G.frankincense", "@+0.4"),
          FORGIVEN, ("light", "G.remnant", "rest"),
          ("light", "G.the_priests", "priest's")),
        s("st:eaten", ("light", "sin.eaten:the remaining flour", "@"))),
    (5, 15): v(
        s("st:head", ("light", "trespass.by", "anyone"),
          ("light", "trespass.head", "trespass offering"),
          ("hud", "trespass offering", "trespass offering"),
          ("light", "trespass.thing:ram", "ram")),
        s("T", ("light", "T.ram", "@"),
          ("light", "T.estimation", "estimation"),
          ("light", "T.silver", "silver"),
          ("light", "T.shekel", "shekel of the sanctuary"))),
    (5, 16): v(
        s("T.bar", ("light", "T.bar", "restitution"),
          ("light", "T.fifth", "fifth part"),
          ("light", "T.to_priest", "priest")),
        s("st:head", ("light", "trespass.thing:silver", "@"),
          ("light", "trespass.thing:ram", "@+0.3"), FORGIVEN)),
    (5, 17): v(s("T", ("light", "T.man", "anyone"),
                 ("light", "T.didnt_know", "didn't know"),
                 ("light", "T.guilty", "guilty"))),
    (5, 18, 19): v(
        s("T", ("light", "T.ram", "ram"),
          ("light", "T.estimation", "estimation"),
          ("light", "T.ram_to_priest", "priest")),
        s("st:head", ("light", "trespass.thing:ram", "@"), FORGIVEN)),

    # ---- Leviticus 6:1-7: the trespass offering's wrongs ------------------
    # the whole card: T.wrongs cut the top band's drawings at its edge
    (6, 1): v(s("T")),
    (6, 2): v(s("T",
                ("light", "T.man", "anyone"),
                ("light", "T.neighbor", "neighbor"),
                ("light", "T.deposit", "deposit"),
                ("light", "T.bargain", "bargain"),
                ("light", "T.robbery", "robbery"),
                ("light", "T.oppressed", "oppressed"))),
    (6, 3): v(s("T",
                ("light", "T.lost", "lost"),
                ("light", "T.lie", "lie"))),
    (6, 4): v(s("T",
                ("light", "T.return:robbery", "robbery"),
                ("light", "T.return:oppressed", "oppression"),
                ("light", "T.return:deposit", "deposit"),
                ("light", "T.return:lost", "lost thing"))),
    # the 'sworn' arrow is in the bottom band, which T.bar doesn't see
    (6, 5): v(s("T", ("light", "T.return:lie", "sworn")),
              s("T.bar",
                ("light", "T.bar", "in full"),
                ("light", "T.in_full", "in full+0.3"),
                ("light", "T.fifth", "fifth"),
                ("light", "T.owner", "belongs"),
                ("light", "T.in_the_day", "day"))),
    # "priest" is the verse's last word: no flight to the table after it,
    # and the table has no new unit here (the ram is 5:15's)
    (6, 6): v(s("T",
                ("hud", "trespass offering", "trespass offering"),
                ("light", "T.ram", "ram"),
                ("light", "T.estimation", "estimation"),
                ("light", "T.ram_to_priest", "priest"))),
    (6, 7, 8): v(s("plan:altar",
                   ("light", "plan.priests", "before Yahweh"),
                   FORGIVEN)),

    # ---- 6:8-13: the law of the burnt offering ---------------------------
    # one stop on the whole card: A.days cuts the fire's chip (a core shot)
    (6, 9): v(s("A",
                ("hud", "burnt offering", "burnt offering"),
                ("light", "A.slot.burnt", "burnt offering#2"),
                ("light", "A.fire", "burnt offering#2+0.4"),
                ("light", "A.days", "all night"),
                ("light", "A.morning", "morning"))),
    # the priest's two chips: "linen breeches" comes 0.6 s after him
    (6, 10): v(s("A",
                 ("light", "A.priest", "linen garment+1.6"),
                 ("light", "A.ashes", "ashes")),
               s("plan:altar",
                 ("move", "plan.ashes", "beside the altar"),
                 ("light", "plan.ash", "beside the altar"))),
    # st:out for plan:camp (see SHOTS)
    (6, 11): v(s("st:out",
                 ("move", "plan.ash_out", "outside the camp", {"dur": 2.2}),
                 ("light", "plan.clean", "clean place"))),
    (6, 12): v(s("A",
                 ("light", "A.wood", "wood"),
                 ("current", "A.morning", "morning"),
                 ("light", "A.slot.burnt", "burnt offering"),
                 ("light", "A.slot.fat", "fat"),
                 ("light", "A.chip:peace offerings", "peace offerings"))),
    # the whole altar card: A.days cuts the fire's chip (a core shot)
    (6, 13): v(s("A", ("light", "A.continual", "continually"))),

    # ---- 6:14-23: the law of the meal offering ---------------------------
    (6, 14): v(s("plan:altar",
                 ("hud", "meal offering", "meal offering"),
                 ("light", "plan.priests", "before the altar"))),
    (6, 15): v(s("G",
                 ("light", "G.handful", "handful"),
                 ("light", "G.flour", "fine flour"),
                 ("light", "G.oil", "oil"),
                 ("light", "G.frankincense", "frankincense"),
                 ("move", "G.handful", "frankincense")),
               s("A.fire",
                 ("flare", "A.fire", "burn"),
                 ("light", "A.slot.memorial", "memorial"))),
    # the table only: at plan:court (s 0.7) the priests' "Aaron's sons"
    # touches a plan label, and no other shot shows the court
    (6, 16): v(s("mp:eaten",
                 ("light", "meal.eaten:the priests|Aaron and his sons",
                  "Aaron and his sons"))),
    (6, 17): v(s("G",
                 ("light", "G.bracket", "most holy"),
                 ("light", "G.name_sin", "sin offering"),
                 ("light", "G.name_trespass", "trespass offering"))),
    (6, 18, 19): v(s("G",
                     ("light", "G.males", "Every male"),
                     ("light", "G.forever", "forever"),
                     ("light", "G.touch", "holy"))),
    # "evening" is 0.4 s from the end: no table stop after it (and the
    # meal column has no "tenth of an ephah" unit)
    (6, 20): v(s("K.measure",
                 ("light", "K.tenth", "tenth"),
                 ("light", "K.morning", "morning"),
                 ("light", "K.evening", "evening"))),
    (6, 21): v(s("K.cook",
                 ("light", "K.griddle", "griddle"),
                 ("light", "K.oil", "oil"),
                 ("light", "K.soaked", "soaked"),
                 ("light", "K.baked_pieces", "baked pieces"))),
    # "wholly burned" is the verse's end: the table only
    (6, 22): v(s("mp:burns",
                 ("light", "meal.burns:all of it", "wholly burned"))),
    (6, 23, 24): v(s("mp:low",
                     ("light", "meal.not_eaten:a priest's own", "not be eaten"))),

    # ---- 6:24-30: the law of the sin offering ----------------------------
    (6, 25): v(s("plan:altar",
                 ("hud", "sin offering", "sin offering"),
                 ("light", "plan.north", "burnt offering is killed")),
               s("G", ("light", "G.name_sin", "most holy"))),
    # the table only (plan:court: see 6:16)
    (6, 26): v(s("st:low", ("light", "sin.eaten:the priests", "eat"))),
    (6, 27): v(s("K.vessels",
                 ("light", "K.holy", "touch"),
                 ("light", "K.coat", "garment"),
                 ("light", "K.wash", "wash"),
                 ("light", "K.holy_place", "holy place"))),
    (6, 28): v(s("K.vessels",
                 ("light", "K.earthen", "earthen vessel"),
                 ("light", "K.broken", "broken"),
                 ("light", "K.bronze", "bronze vessel"),
                 ("light", "K.scoured", "scoured"),
                 ("light", "K.rinsed", "rinsed"))),
    (6, 29): v(s("G",
                 ("light", "G.males", "Every male"),
                 ("light", "G.most_holy", "most holy"))),
    (6, 30): v(s("plan:tent", ("light", "plan.bloodpath", "Tent of Meeting")),
               s("st:low",
                 ("light", "sin.not_eaten:blood in the Tent: burned", "burned"))),

    # ---- Leviticus 7:1-10: the trespass offering's law, the priests' shares
    (7, 1): v(s("st:head",
                ("hud", "trespass offering", "trespass offering"),
                ("light", "trespass.head", "trespass offering"),
                ("light", "trespass.thing:ram", "trespass offering+0.3"))),
    # "around" is 1.4 s from the end: the blood entry is reached off camera
    # and seen at 7:6
    (7, 2): v(s("plan:altar",
                ("light", "plan.north", "burnt offering"),
                ("move", "plan.sheep", "trespass offering"),
                ("light", "plan.ring", "around"))),
    (7, 3): v(s("B",
                ("light", "B.tail_fat", "fat tail"),
                ("light", "B.fat_cover", "covers")),
              beast="ram"),
    (7, 4): v(s("B.inner",
                ("light", "B.kidneys", "kidneys"),
                ("light", "B.kidney_fat", "loins"),
                ("light", "B.liver_cover", "liver")),
              beast="ram"),
    # beast: the file opens on 7:4's board (the ram)
    (7, 5): v(s("A.fire",
                ("light", "A.slot.fat", "burn"),
                ("flare", "A.fire", "burn")),
              beast="ram"),
    (7, 6): v(s("st:low",
                ("light", "trespass.eaten:the priests", "Every male"))),
    (7, 7): v(s("G",
                ("light", "G.one_law", "one law"),
                ("light", "G.to_priest", "priest"))),
    (7, 8): v(s("S.shares",
                ("hud", "burnt offering", "burnt offering"),
                ("light", "S.priest", "priest"),
                ("light", "S.skin", "skin")),
              s("cells:burnt:eaten:not_eaten",
                ("light", "burnt.not_eaten:the skin: the priest's", "@"))),
    (7, 9): v(s("S.shares",
                ("hud", "meal offering", "meal offering"),
                ("light", "S.oven", "oven"),
                ("light", "S.pan", "pan"),
                ("light", "S.griddle", "griddle"),
                ("light", "S.baked", "priest's"))),
    (7, 10): v(s("S.shares",
                 ("light", "S.mixed", "mixed with oil"),
                 ("light", "S.dry", "dry"),
                 ("light", "S.sons", "sons of Aaron")),
               s("mp:eaten",
                 ("light", "meal.eaten:the priests|all the sons of Aaron", "@"))),

    # ---- 7:11-21: the law of the sacrifice of peace offerings -----------
    (7, 11): v(s("D.breads",
                 ("hud", "sacrifice of peace offerings", "peace offerings"),
                 ("light", "D.shelf", "law"))),
    # the third bread is said 1.4 s from the end: the table's cakes and
    # wafers are reached off camera and seen at 7:29
    (7, 12): v(s("D.breads",
                 ("light", "D.thanksgiving", "thanksgiving"),
                 ("light", "D.cakes", "unleavened cakes"),
                 ("light", "D.wafers", "unleavened wafers"),
                 ("light", "D.oil_cakes", "cakes mixed with oil#2"))),
    (7, 13): v(s("D.breads", ("light", "D.leavened", "leavened bread"))),
    (7, 14): v(s("D.breads",
                 ("move", "D.heave", "sprinkles", {"show": "one out of each"}),
                 ("light", "D.heave", "heave"),
                 ("light", "D.priest", "priest's"),
                 ("light", "D.sprinkles", "sprinkles"))),
    (7, 15): v(s("D.days",
                 ("light", "D.day1", "day"),
                 ("light", "D.morning", "morning"))),
    (7, 16): v(s("D.days",
                 ("light", "D.vow", "vow"),
                 ("light", "D.freewill", "freewill offering"),
                 ("light", "D.day2", "next day"))),
    (7, 17): v(s("D.days",
                 ("light", "D.day3", "third day"),
                 ("light", "D.fire3", "burned with fire"))),
    (7, 18): v(s("D.days",
                 ("light", "D.eat3", "eaten"),
                 ("not", "D.eat3", "eaten+0.3"),
                 ("light", "D.not_accepted", "accepted"),
                 ("light", "D.abomination", "abomination")),
               s("mp:low",
                 ("light", "peace.not_eaten:third day's meat", "@"))),
    # "clean" is 1.2 s from the end: the two table units are reached off
    # camera and seen at 7:33 and 7:37
    (7, 19): v(s("D.split",
                 ("light", "D.split", "meat"),
                 ("light", "D.unclean", "unclean"),
                 ("move", "D.unclean", "burned"),
                 ("light", "D.clean", "clean"))),
    (7, 20): v(s("D.split", ("light", "D.cut_off", "cut off"))),
    (7, 21, 22): v(s("D.split",
                     ("light", "D.uncleanness_of_man", "uncleanness of man"),
                     ("light", "D.unclean_animal", "unclean animal"),
                     ("current", "D.cut_off", "cut off"))),

    # ---- 7:22-27: no fat, no blood --------------------------------------
    (7, 23): v(s("S.bans",
                 ("light", "S.ox", "bull"),
                 ("light", "S.sheep", "sheep"),
                 ("light", "S.goat", "goat"),
                 ("not", "S.fat", "fat"))),
    (7, 24): v(s("S.bans",
                 ("light", "S.no_eat", "fat"),
                 ("light", "S.died", "dies of itself"),
                 ("light", "S.torn", "torn"),
                 ("light", "S.service", "service"),
                 ("not", "S.no_eat", "eat"))),
    (7, 25): v(s("S.bans", ("light", "S.cut_off_fat", "cut off"))),
    (7, 26): v(s("S.bans",
                 ("light", "S.dove", "bird"),
                 ("light", "S.animal", "animal"),
                 ("not", "S.blood", "blood"),
                 ("current", "S.dwellings", "dwellings"))),
    (7, 27, 28): v(s("S.bans", ("light", "S.cut_off_blood", "cut off"))),

    # ---- 7:28-36: the wave breast and the heave thigh -------------------
    (7, 29): v(s("C",
                 ("light", "C.ox", "offers"),
                 ("light", "C.offerer", "offers")),
               s("mp:head",
                 ("light", "peace.thing:herd", "@"),
                 ("light", "peace.thing:lamb", "@+0.2"),
                 ("light", "peace.thing:goat", "@+0.4")),
               beast="bull"),
    # "waved" is near the verse's end: the wave is the verse, and the
    # breast's cell is reached off camera at 7:31 (seen at 7:33)
    (7, 30): v(s("B.breast",
                 ("light", "B.fat", "fat"),
                 ("light", "B.breast", "breast"),
                 ("move", "B.breast", "waved", {"chip": "wave offering"})),
               beast="bull"),
    (7, 31): v(s("B",
                 ("light", "B.share_altar", "burn"),
                 ("move", "B.fat", "fat", {"to": "altar"}),
                 ("move", "B.breast", "breast", {"to": "priests"}),
                 ("light", "B.share_priests", "Aaron's")),
               beast="bull"),
    (7, 32): v(s("B", ("light", "B.right_thigh", "right thigh"),
                 ("move", "B.right_thigh", "heave offering", {"chip": "heave offering"})),
               beast="bull"),
    (7, 33): v(s("B",
                 ("light", "B.share_priests", "sons of Aaron"),
                 ("pulse", "B.right_thigh", "blood")),
               s("mp:eaten",
                 ("light", "peace.eaten:the right thigh", "right thigh")),
               beast="bull"),
    (7, 34): v(s("B",
                 ("pulse", "B.breast", "waved breast"),
                 ("pulse", "B.right_thigh", "heaved thigh"),
                 ("light", "B.share_priests", "Aaron the priest"),
                 ("light", "B.chip:forever", "forever")),
               beast="bull"),
    (7, 35, 36): v(s("B",
                     ("pulse", "B.breast", "anointing portion"),
                     ("pulse", "B.right_thigh", "anointing portion+0.3"),
                     ("light", "B.share_priests", "anointing portion#2"),
                     ("light", "B.chip:anointing portion", "anointing portion")),
                   beast="bull"),

    # ---- 7:37-38: the law, and Sinai ------------------------------------
    (7, 37): v(s("table",
                 ("hud", "the law", "law"),
                 ("pulse", "burnt.col", "burnt offering"),
                 ("pulse", "meal.col", "meal offering"),
                 ("pulse", "sin.col", "sin offering"),
                 ("pulse", "trespass.col", "trespass offering"),
                 ("light", "trespass.consecration", "consecration"),
                 ("pulse", "peace.col", "peace offerings"),
                 ("light", "burnt.when", "@"),
                 ("light", "meal.when", "@+0.1"),
                 ("light", "peace.when", "@+0.2"),
                 ("light", "sin.when", "@+0.3"),
                 ("light", "trespass.when", "@+0.4")),
               beast="bull"),          # the file opens on 7:35-36's board
    (7, 38): v(s("L",
                 ("light", "L.moses", "Moses"),
                 ("light", "L.mount", "Mount Sinai"),
                 ("light", "L.wilderness", "wilderness of Sinai"))),
}
