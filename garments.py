"""The high priest's garments, as one record per garment, in WEB's words.

The Tabernacle reference page's Garments view (generate_tabernacle_reference)
dresses the high priest garment by garment and gives each piece a card; its
"Dressing Aaron" tour follows Leviticus 8:7-9. Both take their facts from
here, the way the plan takes the court and the furnishings from sanctuary.py.
Nothing here draws: the shapes are svg_priest's.

**What the text gives, and what it doesn't.** Each fact on a garment is a
`sanctuary.Dim`, marked the same way as the Tabernacle's measurements:

- STATED: the text says it (the breastplate is a span square, 28:16);
- DERIVED: it follows from what the text says (the sons on the shoulder
  stones are in Genesis' birth order, because 28:10 says "in the order of
  their birth" and Genesis 29-30 and 35 give that order);
- NOT GIVEN: the text has no figure (no garment but the breastplate has a
  size, and no one is told how many bells hang on the robe).

**Names follow the WEB** ("coat", "sash", "turban", "plate of pure gold",
"breastplate of judgment", "skillfully woven band"); `aka` holds the names a
reader may search for ("tunic", "mitre", "breastpiece", "girdle").

**Keys.** GARMENTS starts with one record for each key of
svg_priest.WEARING_ORDER, in that order and with those keys, because the
lays them out that way. Then come the extra records: the garments of
Aaron's sons, and the linen garments of Leviticus 16. WEARING_ORDER is the
order svg_priest layers a figure in (the sash over the breastplate) and the
order the page lays the garments out in; DRESSING is the order of the text,
where Moses ties the sash on straight after the coat and then clothes him
with the robe (Lev 8:7), and the page's dressed figure is drawn in it, so
the robe covers the sash.
"""

from typing import NamedTuple, Tuple

from sanctuary import DERIVED, NOT_GIVEN, STATED, Dim


class Garment(NamedTuple):
    key: str
    name: str                      # WEB's wording
    aka: Tuple[str, ...]           # other names a reader may search for
    dims: Tuple[Dim, ...]          # material, size, what is on it
    worn_by: str
    verses: Tuple[Tuple[str, str], ...]    # (group, ref string)
    note: str = ""


def _refs(**groups):
    order = ("commanded", "made", "put_on", "named")
    label = {"commanded": "Commanded", "made": "Made", "put_on": "Put on",
             "named": "Also named"}
    return tuple((label[g], groups[g]) for g in order if g in groups)


# Who wears the high priest's garments: Aaron, and after him the son who is
# priest in his place (29:29-30), as Eleazar was at Mount Hor (Num 20:26-28).
HIGH_PRIEST = "Aaron, and the son who is priest in his place after him"
HIGH_PRIEST_REF = "Exod 29:29-30; Num 20:26-28"


# ---------------------------------------------------------------------------
# The twelve stones and the twelve names                  (Exodus 28:9-21)
# ---------------------------------------------------------------------------

# 28:17-20 and 39:10-13, four rows of three, in the text's order. The two
# chapters name the same twelve.
STONES = (("ruby", "topaz", "beryl"),
          ("turquoise", "sapphire", "emerald"),
          ("jacinth", "agate", "amethyst"),
          ("chrysolite", "onyx", "jasper"))
STONES_REF = "Exod 28:17-20; 39:10-13"

# The sons of Israel in the order of their birth: Leah's four, Bilhah's
# two, Zilpah's two, Leah's two more, then Rachel's Joseph and Benjamin.
# 28:10 asks for birth order but names no one, so the order is Genesis'.
NAMES = ("Reuben", "Simeon", "Levi", "Judah", "Dan", "Naphtali",
         "Gad", "Asher", "Issachar", "Zebulun", "Joseph", "Benjamin")
NAMES_REF = "Gen 29:32-35; 30:5-24; 35:16-18"

# Six names on each onyx stone (28:10). Which stone sits on which shoulder
# is not given; the first six are the first stone.
SHOULDER_STONES = (NAMES[:6], NAMES[6:])
SHOULDER_ORDER = Dim(
    "order", "in the order of their birth, six on each stone; the text "
    "names no one there, so the order is Genesis'", DERIVED,
    "Exod 28:10; " + NAMES_REF)

# One name on each of the breastplate's stones (28:21). The text gives no
# order; the drawing uses birth order again, row by row.
BREASTPLATE_NAMES = tuple(zip(sum(STONES, ()), NAMES))
BREASTPLATE_ORDER = Dim(
    "order", "not given; here the order of their birth, as on the shoulder "
    "stones", NOT_GIVEN, "Exod 28:21")


def stone_list():
    """The twelve stones in the text's order, row by row."""
    return [s for row in STONES for s in row]


# ---------------------------------------------------------------------------
# The garments
# ---------------------------------------------------------------------------

GARMENTS = [
    Garment("breeches", "the linen breeches", ("breeches", "undergarments",
                                               "drawers"),
            (Dim("material", "linen", STATED, "Exod 28:42"),
             Dim("made of", "fine twined linen", STATED, "Exod 39:28"),
             Dim("length", "from the waist even to the thighs", STATED,
                 "Exod 28:42"),
             Dim("for", "to cover the flesh of their nakedness", STATED,
                 "Exod 28:42")),
            "Aaron and his sons, when they go in to the Tent of Meeting or "
            "come near to the altar",
            _refs(commanded="Exod 28:42-43", made="Exod 39:28",
                  named="Lev 6:10; 16:4; Ezek 44:18"),
            note="Not on 28:4's list of six; the chapter adds them at 28:42. "
                 "No dressing verse names them (Exod 29:5-9, Lev 8:7-9), so "
                 "the Dressing Aaron tour puts them on first, from 28:42."),
    Garment("coat", "the coat", ("tunic", "coat of checker work"),
            (Dim("material", "fine linen", STATED, "Exod 28:39"),
             Dim("weave", "checker work", STATED, "Exod 28:4, 39"),
             Dim("made", "of woven work", STATED, "Exod 39:27"),
             Dim("length", "not given", NOT_GIVEN, "")),
            HIGH_PRIEST,
            _refs(commanded="Exod 28:4, 39", made="Exod 39:27",
                  put_on="Exod 29:5; 40:13; Lev 8:7"),
            note="The first thing put on Aaron in both dressings (Exod 29:5, "
                 "Lev 8:7). His sons have coats too (28:40)."),
    Garment("robe", "the robe of the ephod", ("robe", "blue robe",
                                              "bells", "pomegranates"),
            (Dim("colour", "all of blue", STATED, "Exod 28:31"),
             Dim("made", "of woven work", STATED, "Exod 39:22"),
             Dim("opening", "a hole for the head in the middle, with a "
                 "binding of woven work round it, like the hole of a coat of "
                 "mail, that it not be torn", STATED, "Exod 28:32"),
             Dim("pomegranates", "of blue, purple and scarlet, around its "
                 "hem", STATED, "Exod 28:33"),
             Dim("bells", "of gold, between the pomegranates: a golden bell "
                 "and a pomegranate, around the hem", STATED, "Exod 28:33-34"),
             Dim("how many", "not given", NOT_GIVEN, ""),
             Dim("its sound", "heard when he goes in to the holy place and "
                 "when he comes out, that he not die", STATED, "Exod 28:35"),
             Dim("length", "not given", NOT_GIVEN, "")),
            HIGH_PRIEST,
            _refs(commanded="Exod 28:4, 31-35", made="Exod 39:22-26",
                  put_on="Exod 29:5; 40:13; Lev 8:7"),
            note="39:24 makes the pomegranates of blue, purple, scarlet and "
                 "twined linen; 39:25 makes the bells of pure gold."),
    Garment("ephod", "the ephod", ("ephod", "shoulder straps", "onyx stones",
                                   "shoulder stones", "band"),
            (Dim("material", "gold, blue, purple, scarlet and fine twined "
                 "linen, the work of the skillful workman", STATED,
                 "Exod 28:6"),
             Dim("gold", "beaten into thin plates and cut into wires, worked "
                 "in with the yarn", STATED, "Exod 39:3"),
             Dim("shoulder straps", "two, joined to its two ends", STATED,
                 "Exod 28:7"),
             Dim("skillfully woven band", "of the same piece and the same "
                 "work", STATED, "Exod 28:8"),
             Dim("onyx stones", "two, in settings of gold, on the shoulder "
                 "straps: stones of memorial", STATED, "Exod 28:9, 11-12"),
             Dim("on the onyx stones", "the names of the children of "
                 "Israel, six on each, like the engravings of a signet",
                 STATED, "Exod 28:9-11"),
             SHOULDER_ORDER,
             Dim("chains", "two, of pure gold, like cords of braided work, "
                 "on the settings", STATED, "Exod 28:13-14"),
             Dim("size", "not given", NOT_GIVEN, "")),
            HIGH_PRIEST,
            _refs(commanded="Exod 28:4, 6-14", made="Exod 39:2-7",
                  put_on="Exod 29:5; 40:13; Lev 8:7",
                  named="Exod 25:7; 35:9, 27"),
            note="Aaron bears the names on his two shoulders for a memorial "
                 "before Yahweh (28:12). Moses ties the skillfully woven band "
                 "on him and fastens the ephod with it (Lev 8:7)."),
    Garment("breastplate", "the breastplate of judgment",
            ("breastplate", "breastpiece", "twelve stones",
             "Urim and Thummim", "Urim", "Thummim"),
            (Dim("material", "like the work of the ephod: gold, blue, purple, "
                 "scarlet and fine twined linen", STATED, "Exod 28:15"),
             Dim("size", "a span long and a span wide, square and folded "
                 "double", STATED, "Exod 28:16"),
             Dim("stones", "twelve, in four rows of three, enclosed in gold "
                 "settings", STATED, "Exod 28:17-20"),
             Dim("size of the stones", "not given", NOT_GIVEN, ""),
             Dim("on the stones", "the names of the children of Israel, "
                 "one on each, like the engravings of a signet, for the "
                 "twelve tribes", STATED, "Exod 28:21"),
             BREASTPLATE_ORDER,
             Dim("fastening", "two rings of gold on the two ends of the "
                 "breastplate, and braided chains of pure gold from them to "
                 "the settings on the shoulder straps; two more rings on its "
                 "two ends, on its edge, toward the side of the ephod inward, "
                 "bound by a lace of blue to the ephod's rings above the "
                 "skillfully woven band", STATED, "Exod 28:22-28"),
             Dim("which ends", "the chained rings at its upper corners, the "
                 "laced rings at its lower, since the ephod's rings sit low "
                 "on its forepart, above the band", DERIVED, "Exod 28:25-28"),
             Dim("Urim and Thummim", "put in the breastplate, on Aaron's "
                 "heart", STATED, "Exod 28:30; Lev 8:8"),
             Dim("what the Urim and Thummim are", "not given", NOT_GIVEN, "")),
            HIGH_PRIEST,
            _refs(commanded="Exod 28:4, 15-30", made="Exod 39:8-21",
                  put_on="Exod 29:5; 40:13; Lev 8:8",
                  named="Exod 25:7; 35:9, 27; Num 27:21; Deut 33:8"),
            note="Aaron bears the names on his heart when he goes in to the "
                 "holy place (28:29), and the judgment of the children of "
                 "Israel (28:30)."),
    Garment("sash", "the sash", ("sash", "belt", "girdle"),
            (Dim("material", "fine twined linen, and blue, purple and "
                 "scarlet", STATED, "Exod 39:29"),
             Dim("work", "the work of the embroiderer", STATED,
                 "Exod 28:39; 39:29"),
             Dim("length", "not given", NOT_GIVEN, "")),
            HIGH_PRIEST,
            _refs(commanded="Exod 28:4, 39", made="Exod 39:29",
                  put_on="Exod 29:9; 40:13; Lev 8:7"),
            note="Exodus 29:9 calls it a belt (\"You shall clothe them with "
                 "belts, Aaron and his sons\"); Leviticus 8:7 ties it on "
                 "straight after the coat, and the robe goes on over it, so "
                 "on the dressed figure it is hidden."),
    Garment("turban", "the turban", ("turban", "mitre", "headdress"),
            (Dim("material", "fine linen", STATED, "Exod 28:39; 39:28"),
             Dim("size", "not given", NOT_GIVEN, "")),
            HIGH_PRIEST,
            _refs(commanded="Exod 28:4, 39", made="Exod 39:28",
                  put_on="Exod 29:6; 40:13; Lev 8:9")),
    Garment("plate", "the plate of pure gold",
            ("golden plate", "holy crown", "HOLY TO YAHWEH", "diadem",
             "frontlet"),
            (Dim("material", "pure gold", STATED, "Exod 28:36; 39:30"),
             Dim("engraved", "“HOLY TO YAHWEH,” like the engravings "
                 "of a signet", STATED, "Exod 28:36; 39:30"),
             Dim("fastened", "on a lace of blue, on the turban above, in "
                 "front", STATED, "Exod 39:31; Lev 8:9"),
             Dim("where", "on Aaron's forehead, always", STATED,
                 "Exod 28:38"),
             Dim("size", "not given", NOT_GIVEN, "")),
            HIGH_PRIEST,
            _refs(commanded="Exod 28:36-38", made="Exod 39:30-31",
                  put_on="Exod 29:6; Lev 8:9"),
            note="Called \"the plate of the holy crown\" (39:30) and \"the "
                 "golden plate, the holy crown\" (Lev 8:9). The WEB's 28:37 "
                 "puts it \"on the front of the sash\"; 39:31 and Lev 8:9 "
                 "put it on the turban, and the drawing follows them. Aaron "
                 "bears the iniquity of the holy things (28:38)."),

    # --- extra records: not in WEARING_ORDER ---------------------------------
    Garment("sons", "the garments of his sons",
            ("sons' garments", "headbands", "caps", "bonnets", "sashes"),
            (Dim("coats", "of fine linen, of woven work", STATED,
                 "Exod 28:40; 39:27"),
             Dim("sashes", "named, not described; Exodus 29:9 calls them "
                 "belts", STATED, "Exod 28:40; 29:9"),
             Dim("headbands", "linen headbands of fine linen", STATED,
                 "Exod 28:40; 39:28"),
             Dim("breeches", "linen, from the waist to the thighs, as "
                 "Aaron's", STATED, "Exod 28:42-43"),
             Dim("for", "glory and beauty", STATED, "Exod 28:40")),
            "Aaron's sons: Nadab, Abihu, Eleazar and Ithamar",
            _refs(commanded="Exod 28:40-43", made="Exod 39:27-29",
                  put_on="Exod 29:8-9; 40:14; Lev 8:13",
                  named="Exod 31:10; 35:19; 39:41")),
    Garment("linen", "the linen garments",
            ("holy garments", "holy linen coat", "linen sash",
             "linen turban", "Day of Atonement"),
            (Dim("coat", "the holy linen coat", STATED, "Lev 16:4"),
             Dim("breeches", "the linen breeches, on his body", STATED,
                 "Lev 16:4"),
             Dim("sash", "the linen sash", STATED, "Lev 16:4"),
             Dim("turban", "the linen turban", STATED, "Lev 16:4"),
             Dim("put on", "after he bathes his body in water", STATED,
                 "Lev 16:4"),
             Dim("taken off", "in the Tent of Meeting, and left there, after "
                 "he comes out of the Holy Place", STATED, "Lev 16:23"),
             Dim("when", "once in the year, the tenth day of the seventh "
                 "month", STATED, "Lev 16:29, 34")),
            "Aaron, and the anointed priest in his father's place after him",
            _refs(commanded="Lev 16:4, 32", named="Lev 16:23"),
            note="\"They are the holy garments\" (16:4). After he takes them "
                 "off he bathes again and puts on his own garments to offer "
                 "the burnt offerings (16:24)."),
]
GARMENT = {g.key: g for g in GARMENTS}


# ---------------------------------------------------------------------------
# Dressing Aaron                                          (Leviticus 8:6-9)
# ---------------------------------------------------------------------------

# Moses first washes Aaron and his sons (Lev 8:6), then dresses Aaron in the
# order below: the text's own order, one step for each thing it does.
WASHED = "Lev 8:6"

# (ref, garment keys put on at that step, in the text's order). Leviticus 8
# doesn't name the breeches; Exodus 28:42-43 says they are to be on Aaron when
# he ministers, so they go on first, from 28:42. The skillfully woven band
# is part of the ephod (8:7 ties it on "and fastened it to him with it"),
# and the Urim and Thummim go in the breastplate (8:8); neither is a garment
# of its own here.
DRESSING = [
    ("Exod 28:42", ("breeches",)),
    ("Lev 8:7", ("coat", "sash")),
    ("Lev 8:7", ("robe",)),
    ("Lev 8:7", ("ephod",)),
    ("Lev 8:8", ("breastplate",)),
    ("Lev 8:9", ("turban", "plate")),
]
