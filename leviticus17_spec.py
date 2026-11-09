"""The verse plan of the Leviticus 1-7 offerings pictures: data only.

generate_leviticus17_svg.py draws one file a verse (or a range, RANGES) as
a still workbench that files (leviticus17_bench); the seven section modules
(leviticus17_wb_s1 ... _s7) build the verses, each thing on its word. This
module holds the tables they share. Nothing here draws; the design is
docs/design/leviticus-1-7.md.

- RANGES: the nine range files (c, v1, v2). A range file's clock spans its
  verses (the app leaves the <img> running across them).
- CASES: where each case begins, a new beast or bringing. A section clears
  the bench at each (leviticus17_parts.case_clear) and moves the dock's case
  outline, so one case's pieces never carry into the next.
- REACH: {unit: (c, v)}, where a table unit is first lit when that isn't the
  first verse that offerings.py cites for it (a name said later than its
  row's first ref). A section may lay its own REACH over this one.
- EXCUSED: {unit: reason}, a unit the coverage rule lets off as a whole.
"""

BOOK = "Leviticus"
CHAPTERS = tuple(range(1, 8))

RANGES = [(4, 1, 2), (5, 13, 14), (5, 18, 19), (6, 7, 8), (6, 18, 19),
          (6, 23, 24), (7, 21, 22), (7, 27, 28), (7, 35, 36)]

# Where each case begins: a new beast or bringing (the herd, the flock, the
# birds; the ruler's goat, the common person's lamb...).
CASES = [(1, 1), (1, 3), (1, 10), (1, 14),
         (2, 1), (2, 4), (2, 11), (2, 14),
         (3, 1), (3, 6), (3, 12), (3, 17),
         (4, 1), (4, 13), (4, 22), (4, 27), (4, 32),
         (5, 1), (5, 7), (5, 11), (5, 14), (5, 17),
         (6, 1), (6, 8), (6, 14), (6, 19), (6, 24),
         (7, 1), (7, 11), (7, 22), (7, 28), (7, 37)]

# Where a unit is first lit, when that isn't the first verse offerings.py
# cites for it.
REACH = {
    "burnt.head": (1, 3),                    # "burnt offering" first at 1:3
    "burnt.burns:the whole": (1, 9),         # 1:8 is the pieces on the wood
    "burnt.burns:the whole bird": (1, 17),   # its row cites 1:15-17; 1:17 burns it whole
    "sin.blood:before the veil": (4, 7),     # 4:5-7; the seventh drop is 4:7's
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
    # 7:17 names the third day; its row's cell is reached at 7:18
    "peace.not_eaten:third day's meat": (7, 18),
    # the breast's who-line, "Aaron and his sons", is 7:31's words
    "peace.eaten:the breast/who": (7, 31),
}

EXCUSED = {
    "burnt.when": "a summary; the five WHEN cells lift together at 7:37",
    "meal.when": "a summary; the five WHEN cells lift together at 7:37",
    "peace.when": "a summary; the five WHEN cells lift together at 7:37",
    "sin.when": "a summary; the five WHEN cells lift together at 7:37",
    "trespass.when": "a summary; the five WHEN cells lift together at 7:37",
}
