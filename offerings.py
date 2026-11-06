"""The five offerings of Leviticus 1-7, side by side, in WEB's words.

The Tabernacle reference page's Offerings view (generate_tabernacle_reference)
tables them: what is brought and by whom, what burns on the altar, what is
done with the blood, who eats, what is not eaten, and when. Leviticus gives
each offering twice:

- Lev 1:1-6:7, the law for the one who brings it ("Speak to the children of
  Israel", 1:2): the burnt offering (1), the meal offering (2), the sacrifice
  of peace offerings (3), the sin offering (4:1-5:13) and the trespass
  offering (5:14-6:7);
- Lev 6:8-7:38, the law for the priests ("Command Aaron and his sons", 6:9):
  the burnt offering (6:8-13), the meal offering (6:14-23), the sin offering
  (6:24-30), the trespass offering (7:1-7), the priests' shares (7:8-10) and
  the peace offerings (7:11-21, 28-36; between them, 7:22-27 forbids all
  fat and blood), summed up in 7:37-38, which every offering cites as "The
  law".

The WEB numbers Leviticus as the English Bibles do: chapter 5 ends at 5:19
and the trespass offering runs on to 6:7 (the Hebrew text's 5:20-26), so
the law of the burnt offering begins at 6:8.

**Rows.** `brought`, `burns`, `blood`, `eaten` and `not_eaten` are `Row`s:
`who` is who brings it or which kind it is (the anointed priest, from the
herd, of the pan), `what` is the full phrase for the card, `ref` is where
the text says it, and `short` is a noun label of up to five words for the
table on the drawing; a row whose `short` is empty is on the card only.
`not_eaten` is what is neither burned on the altar nor eaten: the burnt
offering's skin and ashes, the sin offering's bull, the fat and the blood.
A sin offering's `brought` row names in `things` the figures its line on
the drawing shows. Each row carries a flag like sanctuary.Dim's: STATED,
DERIVED or NOT_GIVEN.

**When and by whom.** `when` is a Dim for the card and `when_short` the
table's word for it ("freewill or required"); `by` is who brings it, where
the text says "anyone" (the sin offering's ranks are its `brought` rows
instead), and `by_short` the table's word.

**Names follow the WEB** ("meal offering", "sacrifice of peace offerings",
"trespass offering"); `aka` holds the names a reader may search for.

**THINGS** gives each offering's animals and things as keys a drawing can
map to figures ("bull", "lamb", "turtledove", "fine flour", ...), each with
the WEB's phrase, its verse, and the table's label where it isn't the key.

**What the rows don't hold**, for the Leviticus 1-7 verse pictures
(generate_leviticus17_svg), each entry with a label of at most four words in
the WEB's wording, its ref and a flag:

- `CUTS`: the parts of the animal, keyed to svg_figures.beast_parts' parts
  ("fat_cover" is "fat that covers"), each with the beasts it is said of;
  "crop" and "wings" are the bird's;
- `RITES`: who lays a hand on the head, where it is killed and who acts, a
  `place` being a sanctuary.PARTS or sanctuary.PLACES key ("" where the text
  names none: "before Yahweh");
- the small boards: `CAUSES` (5:1-4), `WRONGS` (6:2-3), `BREADS` (7:12-13),
  `DAYS` (7:15-18), `VESSELS` (2:4-7; 6:21, 28; 7:9), `FORGIVEN` (the nine
  verses that say it), `MOST_HOLY`, `ONE_LAW` (7:7), `PENALTIES` ("cut off",
  7:20-27), `LAW_ORDER` (7:37's six laws, in its order) and `SINAI` (7:38).
"""

from typing import NamedTuple, Optional, Tuple

from sanctuary import DERIVED, NOT_GIVEN, STATED, Dim


class Row(NamedTuple):
    who: str                       # who brings it, or which kind
    what: str                      # the full phrase, for the card
    ref: str
    short: str = ""                # the drawing's label ("": card only)
    flag: str = STATED
    things: Tuple[str, ...] = ()   # a sin offering's figures (THING_KEYS)


class Offering(NamedTuple):
    key: str
    name: str                      # WEB's wording
    aka: Tuple[str, ...]
    brought: Tuple[Row, ...]
    burns: Tuple[Row, ...]         # what goes on the altar
    blood: Tuple[Row, ...]         # empty: no blood (the meal offering)
    eaten: Tuple[Row, ...]         # who eats
    not_eaten: Tuple[Row, ...]     # neither on the altar nor eaten
    when: Dim                      # for the card
    when_short: str                # for the table
    by: Optional[Dim]              # who brings it; None: `brought`'s ranks
    by_short: str
    law_ref: str                   # the law for the priests, Lev 6-7
    verses: Tuple[Tuple[str, str], ...]    # (group, ref string)
    note: str = ""


class Thing(NamedTuple):
    key: str                       # a figure key: THING_KEYS
    label: str                     # WEB's phrase
    ref: str
    short: str = ""                # the table's label, if not the key


# Leviticus 7:37-38, the law of all five (and of the consecration).
LAW = "Lev 7:37-38"


def _refs(**groups):
    order = ("people", "priests", "law", "named")
    label = {"people": "For the people", "priests": "For the priests",
             "law": "The law", "named": "Also named"}
    return tuple((label[g], groups[g]) for g in order if g in groups)


OFFERINGS = [
    Offering(
        "burnt", "burnt offering", ("whole burnt offering", "holocaust"),
        brought=(
            Row("from the herd", "a male without defect, at the door of the "
                "Tent of Meeting; he lays his hand on its head", "Lev 1:3-5",
                "herd, a male"),
            Row("from the flock", "a male without defect, of the sheep or of "
                "the goats", "Lev 1:10", "flock, a male"),
            Row("of birds", "turtledoves or young pigeons", "Lev 1:14",
                "turtledoves or young pigeons"),
        ),
        burns=(
            Row("from the herd or the flock", "all of it: the pieces, the "
                "head and the fat, and the innards and legs washed with water",
                "Lev 1:8-9, 12-13", "the whole"),
            Row("of birds", "the whole bird, torn by its wings but not divided; "
                "its crop with its filth is cast beside the altar on the east "
                "part, in the place of the ashes", "Lev 1:15-17",
                "the whole bird"),
            Row("the fire", "kept burning on the altar continually; it shall "
                "not go out", "Lev 6:9, 12-13"),
        ),
        blood=(
            Row("from the herd or the flock", "sprinkled around on the altar "
                "by Aaron's sons, the priests", "Lev 1:5, 11",
                "around the altar"),
            Row("of birds", "drained out on the side of the altar",
                "Lev 1:15", "the altar's side"),
        ),
        eaten=(
            # the text says the priest burns "all of it" and "the whole", not
            # that no one eats it
            Row("no one", "none of it: the priest burns all of it",
                "Lev 1:9, 13", "no one", DERIVED),
        ),
        not_eaten=(
            Row("the skin", "the priest who offers it has the skin for "
                "himself", "Lev 7:8", "the skin: the priest's"),
            Row("the ashes", "the priest, in his linen garment and his linen "
                "breeches, puts them beside the altar; then he puts on other "
                "garments and carries them outside the camp to a clean place",
                "Lev 6:10, 11", "the ashes: outside the camp"),
        ),
        when=Dim("when", "freewill or required: Leviticus 1 names no occasion "
                 "(“When anyone of you offers an offering”); the text "
                 "requires it in the continual burnt offering, morning and "
                 "evening (Exod 29:38-42), as the second bird of the sin "
                 "offering (Lev 5:10), and on the Day of Atonement (16:3)",
                 DERIVED, "Lev 1:2; Exod 29:38-42; Lev 5:10; 16:3"),
        when_short="freewill or required",
        by=Dim("by whom", "anyone (“When anyone of you offers an "
               "offering”)", STATED, "Lev 1:2"),
        by_short="anyone",
        law_ref="Lev 6:8-13; 7:8",
        verses=_refs(
            people="Lev 1:1-17",
            priests="Lev 6:8-13; 7:8",
            law=LAW,
            named="Exod 29:18, 42; 40:29; Lev 8:18-21; 9:2-3, 12-14, 16; "
                  "16:3, 5, 24; Num 7:15; 15:3, 5, 8; Heb 10:6, 8"),
        note="An offering made by fire, of a pleasant aroma to Yahweh (1:9). "
             "Two lambs were to be offered as a continual burnt offering, one "
             "in the morning and one at evening (Exod 29:38-42). The fire on "
             "the altar is never to go out (6:12-13)."),
    Offering(
        "meal", "meal offering", ("grain offering", "cereal offering"),
        brought=(
            Row("of fine flour", "fine flour, with oil poured on it and "
                "frankincense put on it", "Lev 2:1", "flour, oil, frankincense"),
            Row("baked in the oven", "unleavened cakes of fine flour mixed "
                "with oil, or unleavened wafers anointed with oil", "Lev 2:4",
                "cakes or wafers"),
            Row("on a griddle", "unleavened fine flour mixed with oil, cut in "
                "pieces, with oil poured on it", "Lev 2:5-6",
                "from the griddle"),
            Row("of the pan", "fine flour with oil", "Lev 2:7",
                "from the pan"),
            Row("of first fruits", "grain in the ear parched with fire, "
                "bruised grain of the fresh ear, with oil and frankincense",
                "Lev 2:14-15", "parched grain"),
            Row("every one", "seasoned with salt; no meal offering is made "
                "with yeast, and no yeast or honey is burned as an offering "
                "made by fire", "Lev 2:11, 13", "salt, no yeast"),
            Row("the priests' own", "a tenth of an ephah of fine flour, half "
                "in the morning and half in the evening, made with oil in a "
                "griddle, in the day when he is anointed", "Lev 6:20-21",
                "tenth of an ephah"),
        ),
        burns=(
            Row("of fine flour", "a handful of its fine flour and its oil, "
                "with all its frankincense, as its memorial", "Lev 2:2; 6:15",
                "a handful"),
            # 2:9 names no handful and no frankincense: only "its memorial"
            Row("of the oven, griddle or pan", "its memorial", "Lev 2:9"),
            Row("of first fruits", "part of its bruised grain and part of its "
                "oil, with all its frankincense, as its memorial", "Lev 2:16",
                "part of it"),
            Row("the priests' own", "all of it", "Lev 6:22-23", "all of it"),
        ),
        blood=(),
        eaten=(
            Row("Aaron and his sons", "what is left, without yeast, in a holy "
                "place, the court of the Tent of Meeting; every male among "
                "them", "Lev 2:3, 10; 6:16-18", "the priests"),
            Row("the priest who offers it", "one baked in the oven, or "
                "dressed in the pan or on the griddle", "Lev 7:9",
                "the priest"),
            Row("all the sons of Aaron", "one mixed with oil, or dry",
                "Lev 7:10", "the priests"),
        ),
        not_eaten=(
            Row("a priest's own", "every meal offering of a priest is wholly "
                "burned; it shall not be eaten", "Lev 6:23",
                "a priest's own"),
        ),
        when=Dim("when", "freewill or required: Leviticus 2 names no occasion "
                 "(“When anyone offers an offering of a meal offering”); "
                 "the text requires one with each lamb of the continual burnt "
                 "offering (Exod 29:40-41), and the priests' own, perpetually "
                 "(Lev 6:20)", DERIVED, "Lev 2:1; Exod 29:40-41; Lev 6:20"),
        when_short="freewill or required",
        by=Dim("by whom", "anyone (“When anyone offers an offering of a "
               "meal offering”)", STATED, "Lev 2:1"),
        by_short="anyone",
        law_ref="Lev 6:14-23; 7:9-10",
        verses=_refs(
            people="Lev 2:1-16",
            priests="Lev 6:14-23; 7:9-10",
            law=LAW,
            named="Exod 29:41; 40:29; Lev 9:4, 17; Num 7:13; 15:4, 6, 9"),
        note="It has no blood. What is left of it is most holy (2:3; 6:17). "
             "Yeast and honey may be offered as first fruits, but they shall "
             "not rise up for a pleasant aroma on the altar (2:11-12)."),
    Offering(
        "peace", "sacrifice of peace offerings",
        ("peace offering", "fellowship offering", "thanksgiving", "vow",
         "freewill offering"),
        brought=(
            Row("from the herd", "male or female, without defect",
                "Lev 3:1", "male or female"),
            Row("from the flock, a lamb", "male or female, without defect",
                "Lev 3:6-7", "a lamb"),
            Row("from the flock, a goat", "a goat", "Lev 3:12", "a goat"),
            Row("for a thanksgiving", "with it, unleavened cakes mixed with "
                "oil, unleavened wafers anointed with oil, cakes mixed with "
                "oil, and cakes of leavened bread", "Lev 7:12-13",
                "cakes and wafers"),
            Row("the one who offers it", "brings the fat with the breast with "
                "his own hands", "Lev 7:29-30", "with his own hands"),
        ),
        burns=(
            Row("from the herd, or a goat", "the fat that covers the innards "
                "and all the fat on them, the two kidneys and the fat on them, "
                "which is by the loins, and the cover on the liver",
                "Lev 3:3-5, 14-16", "the fat"),
            Row("a lamb", "the same, and the entire tail fat, taken away close "
                "to the backbone", "Lev 3:9-11", "the fat, the tail"),
        ),
        blood=(
            Row("every one", "sprinkled around on the altar by Aaron's sons",
                "Lev 3:2, 8, 13", "around the altar"),
        ),
        eaten=(
            Row("Aaron and his sons", "the breast, waved for a wave offering",
                "Lev 7:30-31, 34", "the breast"),
            Row("the priest who sprinkles the blood", "the right thigh, a "
                "heave offering, and one of each kind of the thanksgiving "
                "cakes", "Lev 7:14, 32-33", "the right thigh"),
            Row("everyone who is clean", "the meat: a thanksgiving's on its "
                "day, a vow's or a freewill offering's by the next day",
                "Lev 7:15-16, 19", "the offerer"),
        ),
        not_eaten=(
            Row("all the fat, and the blood", "Yahweh's: Israel eats no fat "
                "of bull, sheep or goat, and no blood of bird or animal",
                "Lev 3:16-17; 7:22-27", "the fat, the blood"),
            Row("on the third day", "what remains of the meat is burned with "
                "fire", "Lev 7:17-18", "third day's meat"),
            Row("unclean", "meat that touches any unclean thing is burned "
                "with fire", "Lev 7:19-21", "unclean meat"),
        ),
        when=Dim("when", "for a thanksgiving, or a vow, or a freewill "
                 "offering", STATED, "Lev 7:12, 16"),
        when_short="thanksgiving, vow or freewill",
        by=Dim("by whom", "anyone: 3:1's “his offering” is 1:2's "
               "“anyone of you”", DERIVED, "Lev 3:1"),
        by_short="anyone",
        law_ref="Lev 7:11-21, 28-36",
        verses=_refs(
            people="Lev 3:1-17",
            priests="Lev 7:11-21, 28-36",
            law=LAW,
            named="Exod 29:28; Lev 9:4, 18-21; Num 7:17; 15:8"),
        note="All the fat is Yahweh's; Israel eats neither fat nor blood "
             "(3:16-17; 7:22-27). That the one who offers it eats the meat "
             "is the text's “everyone who is clean may eat it” (7:19). The "
             "waved breast and the heaved thigh are the anointing portion of "
             "Aaron and his sons, their portion forever (7:34-36)."),
    Offering(
        "sin", "sin offering", ("purification offering", "offering for sin"),
        brought=(
            Row("the anointed priest", "a young bull without defect",
                "Lev 4:3-4", "a young bull", things=("bull",)),
            Row("the whole congregation", "a young bull; the elders lay their "
                "hands on its head", "Lev 4:13-15", "a young bull",
                things=("bull",)),
            Row("a ruler", "a goat, a male without defect", "Lev 4:22-23",
                "a male goat", things=("male goat",)),
            Row("one of the common people", "a goat, a female without defect, "
                "or a lamb, a female without defect", "Lev 4:27-28, 32",
                "a female goat or lamb", things=("female goat", "lamb")),
            Row("one guilty of 5:1–4", "a female from the flock, a lamb or a "
                "goat, after he confesses", "Lev 5:5-6",
                "a female goat or lamb", things=("female goat", "lamb")),
            Row("can't afford a lamb", "two turtledoves, or two young "
                "pigeons: one for a sin offering, and the other for a burnt "
                "offering", "Lev 5:7", "two turtledoves or young pigeons",
                things=("turtledove", "pigeon")),
            Row("can't afford two turtledoves", "a tenth of an ephah of fine flour, "
                "with no oil and no frankincense", "Lev 5:11",
                "a tenth of an ephah", things=("fine flour",)),
        ),
        burns=(
            Row("a bull", "all its fat: the fat that covers the innards and "
                "all the fat on them, the two kidneys and the fat on them, "
                "which is by the loins, and the cover on the liver, as it is "
                "taken from the peace offerings; on the altar of burnt "
                "offering", "Lev 4:8-10, 19", "the fat"),
            Row("a goat or a lamb", "all its fat, as it is taken from the "
                "peace offerings", "Lev 4:26, 31, 35", "the fat"),
            Row("two birds", "the second is offered for a burnt offering",
                "Lev 5:10"),
            Row("fine flour", "a handful as the memorial portion", "Lev 5:12",
                "a handful"),
        ),
        blood=(
            Row("the anointed priest's and the congregation's bull",
                "brought into the Tent of Meeting and sprinkled seven times "
                "before the veil, put on the horns of the altar of sweet "
                "incense; the rest poured out at the base of the altar of "
                "burnt offering", "Lev 4:5-7, 16-17", "before the veil"),
            # 4:18 says "the altar which is before Yahweh, that is in the Tent
            # of Meeting"; only 4:7 names it the altar of sweet incense. Card
            # only, so the table keeps one "before the veil" for both bulls.
            Row("the congregation's bull",
                "put on the horns of the altar which is before Yahweh, that "
                "is in the Tent of Meeting (the altar of sweet incense, 4:7); "
                "the rest poured out at the base of the altar of burnt "
                "offering", "Lev 4:18", "", DERIVED),
            Row("a ruler's or one of the people's", "put on the horns of the "
                "altar of burnt offering; the rest poured out at its base",
                "Lev 4:25, 30, 34", "on the altar's horns"),
            Row("a bird", "sprinkled on the side of the altar; the rest "
                "drained out at its base", "Lev 5:9", "the altar's side"),
        ),
        eaten=(
            Row("the priest who offers it", "in a holy place, the court of the "
                "Tent of Meeting; every male among the priests", "Lev 6:26, 29",
                "the priests"),
            Row("the priest", "the rest of the fine flour, as the meal "
                "offering", "Lev 5:13", "the remaining flour"),
        ),
        not_eaten=(
            Row("a young bull", "the anointed priest's and the congregation's "
                "bull: its skin, meat, head, legs, innards and dung, carried "
                "outside the camp to a clean place, where the ashes are poured "
                "out, and burned", "Lev 4:11-12, 21",
                "the bull: outside the camp"),
            Row("blood brought in", "no sin offering whose blood is brought "
                "into the Tent of Meeting to make atonement is eaten: it is "
                "burned with fire", "Lev 6:30", "blood in the Tent: burned"),
        ),
        when=Dim("when", "required: when anyone sins unintentionally (4:2) "
                 "and it is made known to him (4:23, 28), or is known (4:14), "
                 "or when he is "
                 "guilty of one of these (5:1-5)", STATED,
                 "Lev 4:2, 14, 23, 28; 5:1-5"),
        when_short="required",
        by=None,
        by_short="",
        law_ref="Lev 6:24-30",
        verses=_refs(
            people="Lev 4:1-5:13",
            priests="Lev 6:24-30",
            law=LAW,
            named="Exod 29:14, 36; Lev 8:14-17; 9:2-3, 7-11, 15; 16:3, 5-6, "
                  "9, 11, 15, 25, 27; Num 7:16; 15:24-27; Heb 10:6, 8, 18; "
                  "13:11"),
        note="Most holy (6:25, 29). The WEB's 5:6-7 calls what is brought "
             "there “his trespass offering”, “for a sin "
             "offering”; it is the sin offering's law, and 5:9, 11-12 "
             "call it a sin offering, so it is tabled here. Of the two birds, "
             "the second is a burnt offering (5:10)."),
    Offering(
        "trespass", "trespass offering", ("guilt offering",
                                          "reparation offering"),
        brought=(
            Row("a trespass in the holy things", "a ram without defect from "
                "the flock, according to your estimation in silver by shekels, "
                "after the shekel of the sanctuary; he makes restitution and "
                "adds a fifth part, given to the priest", "Lev 5:15-16",
                "a ram, a fifth"),
            # a reading of "according to your estimation in silver by shekels"
            Row("the silver", "the ram's estimation, not a second thing "
                "brought", "Lev 5:15", flag=DERIVED),
            Row("a sin he didn't know", "a ram without defect from the flock, "
                "according to your estimation", "Lev 5:17-18", "a ram"),
            Row("a wrong against his neighbor", "he restores it in full and "
                "adds a fifth part more, to its owner; then a ram without "
                "defect from the flock", "Lev 6:2-6", "a fifth, a ram"),
        ),
        burns=(
            Row("the ram", "all its fat: the fat tail, the fat that covers the "
                "innards, the two kidneys and the fat on them, which is by the "
                "loins, and the cover on the liver", "Lev 7:3-5", "the fat"),
        ),
        blood=(
            Row("the ram", "sprinkled around on the altar", "Lev 7:2",
                "around the altar"),
        ),
        eaten=(
            Row("every male among the priests", "in a holy place; the priest "
                "who makes atonement with it has it", "Lev 7:6-7",
                "the priests"),
        ),
        not_eaten=(),
        when=Dim("when", "required: for a trespass in the holy things, a sin "
                 "he didn't know, or a wrong against his neighbor; with "
                 "restitution and a fifth part more where something was "
                 "taken (5:16; 6:5)", STATED, "Lev 5:15-18; 6:2-6"),
        when_short="required",
        by=Dim("by whom", "anyone (“If anyone commits a trespass”, “If "
               "anyone sins”)", STATED, "Lev 5:15, 17; 6:2"),
        by_short="anyone",
        law_ref="Lev 7:1-7",
        verses=_refs(
            people="Lev 5:14-6:7",
            priests="Lev 7:1-7",
            law=LAW,
            named="Lev 14:12-14, 21, 24-25; 19:21-22; Num 6:12; 18:9"),
        note="Most holy (7:1, 6). “As is the sin offering, so is the "
             "trespass offering; there is one law for them” (7:7). It is "
             "killed where the burnt offering is killed (7:2)."),
]
OFFERING = {o.key: o for o in OFFERINGS}


# ---------------------------------------------------------------------------
# What is brought, as keys a drawing can map to figures
# ---------------------------------------------------------------------------

THINGS = {
    "burnt": (Thing("bull", "a male of the herd", "Lev 1:3, 5"),
              Thing("male sheep", "a male of the sheep", "Lev 1:10"),
              Thing("male goat", "a male of the goats", "Lev 1:10"),
              Thing("turtledove", "turtledoves", "Lev 1:14"),
              Thing("pigeon", "young pigeons", "Lev 1:14")),
    "meal": (Thing("fine flour", "fine flour", "Lev 2:1"),
             Thing("oil", "oil", "Lev 2:1"),
             Thing("frankincense", "frankincense", "Lev 2:1"),
             Thing("cakes", "unleavened cakes", "Lev 2:4"),
             Thing("wafers", "unleavened wafers", "Lev 2:4"),
             Thing("first fruits", "grain in the ear parched with fire",
                   "Lev 2:14"),
             Thing("salt", "salt", "Lev 2:13")),
    "peace": (Thing("herd", "from the herd, male or female", "Lev 3:1"),
              Thing("lamb", "a lamb", "Lev 3:7"),
              Thing("goat", "a goat", "Lev 3:12"),
              Thing("cakes", "unleavened cakes", "Lev 7:12"),
              Thing("wafers", "unleavened wafers", "Lev 7:12"),
              Thing("leavened bread", "cakes of leavened bread", "Lev 7:13")),
    "sin": (Thing("bull", "a young bull", "Lev 4:3, 14"),
            Thing("male goat", "a goat, a male", "Lev 4:23"),
            Thing("female goat", "a goat, a female", "Lev 4:28; 5:6"),
            Thing("lamb", "a lamb, a female", "Lev 4:32; 5:6"),
            Thing("turtledove", "two turtledoves", "Lev 5:7"),
            Thing("pigeon", "two young pigeons", "Lev 5:7"),
            Thing("fine flour", "a tenth of an ephah of fine flour",
                  "Lev 5:11")),
    "trespass": (Thing("ram", "a ram without defect", "Lev 5:15, 18; 6:6"),
                 Thing("silver", "according to your estimation in silver by "
                       "shekels: the ram's value, not a second thing brought",
                       "Lev 5:15", short="estimation in silver")),
}
THING_KEYS = sorted({t.key for things in THINGS.values() for t in things})


# ---------------------------------------------------------------------------
# The parts of the animal                (svg_figures.beast_parts' parts)
# ---------------------------------------------------------------------------

class Cut(NamedTuple):
    key: str                       # a beast_parts part
    label: str                     # WEB's words, at most four
    ref: str
    beasts: Tuple[str, ...]        # bull, sheep, ram, goat; or bird


_HERD_FLOCK = ("bull", "sheep", "goat")             # burnt, peace, sin
_FAT = ("bull", "sheep", "ram", "goat")             # peace, sin, trespass
_INNER = "Lev 3:4, 10, 15; 4:9; 7:4"                # kidneys, loins, liver

CUTS = [
    Cut("skin", "skin", "Lev 1:6; 4:11; 7:8", _HERD_FLOCK),
    Cut("head", "head", "Lev 1:8, 12; 4:11", _HERD_FLOCK),
    Cut("legs", "legs", "Lev 1:9, 13; 4:11", _HERD_FLOCK),
    Cut("meat", "all its meat", "Lev 4:11", ("bull",)),
    Cut("pieces", "pieces", "Lev 1:6, 8, 12", _HERD_FLOCK),
    Cut("innards", "innards", "Lev 1:9, 13; 4:11", _HERD_FLOCK),
    Cut("fat_cover", "fat that covers", "Lev 3:3, 9, 14; 4:8; 7:3", _FAT),
    # 3:9 spells it "inwards"; the ram's 7:3 has no "fat on" them
    Cut("fat_on", "fat on the innards", "Lev 3:3, 9, 14; 4:8",
        _HERD_FLOCK),
    Cut("kidneys", "the two kidneys", _INNER, _FAT),
    Cut("kidney_fat", "fat by the loins", _INNER, _FAT),
    Cut("loins", "by the loins", _INNER, _FAT),
    Cut("liver", "the liver", _INNER, _FAT),
    Cut("liver_cover", "cover on the liver", _INNER, _FAT),
    Cut("backbone", "close to the backbone", "Lev 3:9", ("sheep",)),
    # the lamb's "entire tail fat" (3:9) and the ram's "fat tail" (7:3)
    Cut("tail_fat", "the entire tail fat", "Lev 3:9; 7:3", ("sheep", "ram")),
    Cut("breast", "the breast", "Lev 7:30-31, 34", _HERD_FLOCK),
    Cut("right_thigh", "right thigh", "Lev 7:32-34", _HERD_FLOCK),
    Cut("dung", "its dung", "Lev 4:11", ("bull",)),
    Cut("crop", "its crop", "Lev 1:16", ("bird",)),
    Cut("wings", "its wings", "Lev 1:17", ("bird",)),
]
CUT = {c.key: c for c in CUTS}


# ---------------------------------------------------------------------------
# Who does what, and where
# ---------------------------------------------------------------------------

class Rite(NamedTuple):
    offering: str                  # an OFFERING key
    case: str                      # which kind ("from the herd", "a ruler")
    act: str                       # in the WEB's words
    place: str                     # a sanctuary PARTS or PLACES key, or ""
    by: str                        # who acts ("": the text names no one)
    ref: str
    flag: str = STATED             # DERIVED: the place or the actor inferred


RITES = [
    # the burnt offering                                         (Lev 1)
    Rite("burnt", "from the herd", "offers it at the door of the Tent of "
         "Meeting", "door", "the offerer", "Lev 1:3"),
    Rite("burnt", "from the herd", "lays his hand on the head", "",
         "the offerer", "Lev 1:4"),
    Rite("burnt", "from the herd", "kills the bull before Yahweh", "",
         "the offerer", "Lev 1:5"),
    Rite("burnt", "from the herd", "sprinkle the blood around on the altar",
         "altar", "Aaron's sons, the priests", "Lev 1:5"),
    Rite("burnt", "from the herd", "flays it, and cuts it into pieces", "",
         "the offerer", "Lev 1:6"),
    Rite("burnt", "from the herd", "put fire on the altar, and lay wood in "
         "order on the fire", "altar", "the sons of Aaron", "Lev 1:7"),
    Rite("burnt", "from the herd", "lay the pieces, the head, and the fat in "
         "order on the wood", "altar", "Aaron's sons, the priests",
         "Lev 1:8"),
    Rite("burnt", "from the herd", "washes its innards and its legs with "
         "water", "", "the offerer", "Lev 1:9"),
    Rite("burnt", "from the herd", "burns all of it on the altar", "altar",
         "the priest", "Lev 1:9"),
    Rite("burnt", "from the flock", "kills it on the north side of the altar",
         "north_side", "the offerer", "Lev 1:11"),
    Rite("burnt", "from the flock", "sprinkle its blood around on the altar",
         "altar", "Aaron's sons, the priests", "Lev 1:11"),
    Rite("burnt", "from the flock", "cuts it into its pieces", "",
         "the offerer", "Lev 1:12"),
    Rite("burnt", "from the flock", "lays them in order on the wood",
         "altar", "the priest", "Lev 1:12"),
    Rite("burnt", "of birds", "brings it to the altar, and wrings off its "
         "head", "altar", "the priest", "Lev 1:15"),
    Rite("burnt", "of birds", "casts its crop beside the altar on the east "
         "part", "ash_place", "the priest", "Lev 1:16"),
    Rite("burnt", "of birds", "tears it by its wings, but shall not divide it "
         "apart", "", "the priest", "Lev 1:17"),
    # the law of the burnt offering                              (Lev 6)
    Rite("burnt", "the ashes", "puts them beside the altar", "ash_place",
         "the priest", "Lev 6:10", DERIVED),
    Rite("burnt", "the ashes", "carries them outside the camp to a clean "
         "place", "clean_place", "the priest", "Lev 6:11"),
    # the meal offering                                       (Lev 2; 6)
    Rite("meal", "of fine flour", "brings it to Aaron's sons, the priests",
         "", "the offerer", "Lev 2:2"),
    Rite("meal", "of the oven, griddle or pan", "presented to the priest, "
         "who brings it to the altar", "altar", "the priest", "Lev 2:8"),
    Rite("meal", "every one", "offer it before Yahweh, before the altar",
         "altar", "the sons of Aaron", "Lev 6:14"),
    # the sacrifice of peace offerings                           (Lev 3)
    Rite("peace", "from the herd", "lays his hand on the head", "",
         "the offerer", "Lev 3:2"),
    Rite("peace", "from the herd", "kills it at the door of the Tent of "
         "Meeting", "door", "the offerer", "Lev 3:2"),
    Rite("peace", "from the herd", "sprinkle the blood around on the altar",
         "altar", "Aaron's sons, the priests", "Lev 3:2"),
    Rite("peace", "a lamb", "lays his hand on the head", "", "the offerer",
         "Lev 3:8"),
    # "before the Tent of Meeting": the door, by 3:2
    Rite("peace", "a lamb", "kills it before the Tent of Meeting", "door",
         "the offerer", "Lev 3:8", DERIVED),
    Rite("peace", "a lamb", "sprinkle its blood around on the altar",
         "altar", "Aaron's sons", "Lev 3:8"),
    Rite("peace", "a goat", "lays his hand on its head", "", "the offerer",
         "Lev 3:13"),
    Rite("peace", "a goat", "kills it before the Tent of Meeting", "door",
         "the offerer", "Lev 3:13", DERIVED),
    Rite("peace", "a goat", "sprinkle its blood around on the altar",
         "altar", "the sons of Aaron", "Lev 3:13"),
    # the sin offering                                       (Lev 4-5; 6)
    Rite("sin", "the anointed priest", "brings the bull to the door of the "
         "Tent of Meeting", "door", "the anointed priest", "Lev 4:4"),
    Rite("sin", "the anointed priest", "lays his hand on the head of the "
         "bull, and kills the bull before Yahweh", "", "the anointed priest",
         "Lev 4:4"),
    Rite("sin", "the anointed priest", "brings some of the blood to the Tent "
         "of Meeting", "tent", "the anointed priest", "Lev 4:5"),
    Rite("sin", "the anointed priest", "sprinkles it seven times before the "
         "veil", "veil", "the priest", "Lev 4:6"),
    Rite("sin", "the anointed priest", "puts it on the horns of the altar of "
         "sweet incense", "incense_altar", "the priest", "Lev 4:7"),
    Rite("sin", "the anointed priest", "pours out the rest at the base of "
         "the altar of burnt offering", "altar", "the priest", "Lev 4:7"),
    Rite("sin", "the anointed priest", "carries the whole bull outside of the "
         "camp to a clean place", "clean_place", "the priest", "Lev 4:12"),
    # "before the Tent of Meeting": the door, by 4:4
    Rite("sin", "the whole congregation", "brings it before the Tent of "
         "Meeting", "door", "the assembly", "Lev 4:14", DERIVED),
    Rite("sin", "the whole congregation", "lay their hands on the head of the "
         "bull", "", "the elders of the congregation", "Lev 4:15"),
    Rite("sin", "the whole congregation", "the bull shall be killed before "
         "Yahweh", "", "", "Lev 4:15"),
    Rite("sin", "the whole congregation", "brings some of the blood of the "
         "bull to the Tent of Meeting", "tent", "the anointed priest",
         "Lev 4:16"),
    Rite("sin", "the whole congregation", "sprinkles it seven times before "
         "the veil", "veil", "the priest", "Lev 4:17"),
    # 4:18's "altar which is before Yahweh": the altar of sweet incense by 4:7
    Rite("sin", "the whole congregation", "puts it on the horns of the altar "
         "which is before Yahweh", "incense_altar", "the priest", "Lev 4:18",
         DERIVED),
    Rite("sin", "the whole congregation", "pours out the rest at the base "
         "of the altar of burnt offering", "altar", "the priest", "Lev 4:18"),
    # "outside the camp": to the clean place, as the first bull (4:12)
    Rite("sin", "the whole congregation", "carries the bull outside the camp",
         "clean_place", "the anointed priest", "Lev 4:21", DERIVED),
    Rite("sin", "a ruler", "lays his hand on the head of the goat", "",
         "the ruler", "Lev 4:24"),
    # "where they kill the burnt offering": the north side, by 1:11
    Rite("sin", "a ruler", "kills it in the place where they kill the burnt "
         "offering", "north_side", "the ruler", "Lev 4:24", DERIVED),
    Rite("sin", "a ruler", "puts it on the horns of the altar of burnt "
         "offering", "altar", "the priest", "Lev 4:25"),
    Rite("sin", "a ruler", "pours out the rest of its blood at the base of "
         "the altar of burnt offering", "altar", "the priest", "Lev 4:25"),
    Rite("sin", "one of the common people", "lays his hand on the head of the "
         "sin offering", "", "the offerer", "Lev 4:29"),
    Rite("sin", "one of the common people", "kills the sin offering in the "
         "place of burnt offering", "north_side", "the offerer", "Lev 4:29",
         DERIVED),
    Rite("sin", "one of the common people", "puts it on the horns of the "
         "altar of burnt offering", "altar", "the priest", "Lev 4:30"),
    Rite("sin", "one of the common people", "pours out the rest of its blood "
         "at the base of the altar", "altar", "the priest", "Lev 4:30"),
    Rite("sin", "one of the common people", "lays his hand on the head of the "
         "sin offering", "", "the offerer", "Lev 4:33"),
    Rite("sin", "one of the common people", "kills it in the place where they "
         "kill the burnt offering", "north_side", "the offerer", "Lev 4:33",
         DERIVED),
    Rite("sin", "one of the common people", "puts it on the horns of the "
         "altar of burnt offering", "altar", "the priest", "Lev 4:34"),
    Rite("sin", "one of the common people", "pours out all the rest of its "
         "blood at the base of the altar", "altar", "the priest", "Lev 4:34"),
    Rite("sin", "can't afford a lamb", "wrings off its head from its neck, "
         "but shall not sever it completely", "", "the priest", "Lev 5:8"),
    Rite("sin", "can't afford a lamb", "sprinkles some of the blood on the "
         "side of the altar", "altar", "the priest", "Lev 5:9"),
    Rite("sin", "can't afford a lamb", "the rest of the blood shall be "
         "drained out at the base of the altar", "altar", "", "Lev 5:9"),
    Rite("sin", "every one", "killed in the place where the burnt offering "
         "is killed", "north_side", "", "Lev 6:25", DERIVED),
    Rite("sin", "every one", "eaten in a holy place, in the court of the "
         "Tent of Meeting", "court", "the priest who offers it", "Lev 6:26"),
    # the trespass offering                                      (Lev 7)
    Rite("trespass", "every one", "kills it in the place where they kill the "
         "burnt offering", "north_side", "", "Lev 7:2", DERIVED),
    Rite("trespass", "every one", "sprinkles its blood around on the altar",
         "altar", "", "Lev 7:2"),
]


# ---------------------------------------------------------------------------
# The small boards
# ---------------------------------------------------------------------------

class Entry(NamedTuple):
    key: str
    label: str                     # WEB's words, at most four
    ref: str
    flag: str = STATED
    offering: str = ""             # an OFFERING key, where it is one's


# The four causes of 5:1-4, each "hidden from him" until he knows of it.
CAUSES = [
    Entry("witness", "a witness", "Lev 5:1"),
    Entry("seen", "seen", "Lev 5:1"),
    Entry("known", "known", "Lev 5:1"),
    Entry("carcass", "the carcass", "Lev 5:2"),
    Entry("unclean_animal", "an unclean animal", "Lev 5:2"),
    Entry("unclean_livestock", "unclean livestock", "Lev 5:2"),
    Entry("creeping_things", "unclean creeping things", "Lev 5:2"),
    Entry("uncleanness_of_man", "the uncleanness of man", "Lev 5:3"),
    Entry("oath", "an oath", "Lev 5:4"),
    Entry("evil", "to do evil", "Lev 5:4"),
    Entry("good", "to do good", "Lev 5:4"),
]

# The wrongs against a neighbor of 6:2-3.
WRONGS = [
    Entry("deposit", "deposit", "Lev 6:2"),
    Entry("bargain", "bargain", "Lev 6:2"),
    Entry("robbery", "robbery", "Lev 6:2"),
    Entry("oppressed", "oppressed his neighbor", "Lev 6:2"),
    Entry("lost", "that which was lost", "Lev 6:3"),
    Entry("lie", "swearing to a lie", "Lev 6:3"),
]

# The thanksgiving's breads: 7:12's three kinds and 7:13's leavened.
BREADS = [
    Entry("cakes", "unleavened cakes", "Lev 7:12", offering="peace"),
    Entry("wafers", "unleavened wafers", "Lev 7:12", offering="peace"),
    Entry("oil_cakes", "cakes mixed with oil", "Lev 7:12", offering="peace"),
    Entry("leavened", "leavened bread", "Lev 7:13", offering="peace"),
]


class Day(NamedTuple):
    key: str
    label: str                     # WEB's words, at most four
    day: int                       # 1, 2 or 3
    ref: str
    flag: str = STATED


# How long the peace offering's meat may be eaten (7:15-18).
DAYS = [
    Day("thanksgiving", "thanksgiving", 1, "Lev 7:15"),
    Day("morning", "until the morning", 1, "Lev 7:15"),
    Day("vow", "a vow", 2, "Lev 7:16"),
    Day("freewill", "a freewill offering", 2, "Lev 7:16"),
    Day("next_day", "the next day", 2, "Lev 7:16"),
    Day("third_day", "the third day", 3, "Lev 7:17"),
    Day("burned", "burned with fire", 3, "Lev 7:17"),
    Day("not_accepted", "not be accepted", 3, "Lev 7:18"),
    Day("abomination", "an abomination", 3, "Lev 7:18"),
]


class Vessel(NamedTuple):
    key: str
    label: str                     # WEB's words, at most four
    kind: str                      # svg_figures.cookware's kind
    ref: str
    flag: str = STATED


VESSELS = [
    Vessel("oven", "oven", "oven", "Lev 2:4; 7:9"),
    Vessel("griddle", "griddle", "griddle", "Lev 2:5; 6:21; 7:9"),
    Vessel("pan", "pan", "pan", "Lev 2:7; 7:9"),
    # the sin offering's flesh is boiled in them (6:28)
    Vessel("earthen", "earthen vessel", "pot", "Lev 6:28"),
    Vessel("bronze", "bronze vessel", "pot", "Lev 6:28"),
]

# The nine verses that say "forgiven", for the HUD's chip.
FORGIVEN = [
    Entry("congregation", "forgiven", "Lev 4:20", offering="sin"),
    Entry("ruler", "forgiven", "Lev 4:26", offering="sin"),
    Entry("common_goat", "forgiven", "Lev 4:31", offering="sin"),
    Entry("common_lamb", "forgiven", "Lev 4:35", offering="sin"),
    Entry("birds", "forgiven", "Lev 5:10", offering="sin"),
    Entry("flour", "forgiven", "Lev 5:13", offering="sin"),
    Entry("holy_things", "forgiven", "Lev 5:16", offering="trespass"),
    Entry("didnt_know", "forgiven", "Lev 5:18", offering="trespass"),
    Entry("neighbor", "forgiven", "Lev 6:7", offering="trespass"),
]

# What Leviticus 1-7 calls most holy. 6:17 says it of the meal offering,
# "as the sin offering, and as the trespass offering".
MOST_HOLY = [
    Entry("meal", "most holy", "Lev 2:3, 10; 6:17", offering="meal"),
    Entry("sin", "most holy", "Lev 6:17, 25, 29", offering="sin"),
    Entry("trespass", "most holy", "Lev 6:17; 7:1, 6", offering="trespass"),
]

# "As is the sin offering, so is the trespass offering" (7:7).
ONE_LAW = [
    Entry("sin", "sin offering", "Lev 7:7", offering="sin"),
    Entry("trespass", "trespass offering", "Lev 7:7", offering="trespass"),
    Entry("one_law", "one law for them", "Lev 7:7"),
]

# "That soul shall be cut off from his people" (7:20-27).
PENALTIES = [
    Entry("unclean_eats", "cut off", "Lev 7:20", offering="peace"),
    Entry("touched_eats", "cut off", "Lev 7:21", offering="peace"),
    Entry("eats_fat", "cut off", "Lev 7:25"),
    Entry("eats_blood", "cut off", "Lev 7:27"),
]

# 7:37's six laws, in its order; the consecration is no offering here.
LAW_ORDER = [
    Entry("burnt", "burnt offering", "Lev 7:37", offering="burnt"),
    Entry("meal", "meal offering", "Lev 7:37", offering="meal"),
    Entry("sin", "sin offering", "Lev 7:37", offering="sin"),
    Entry("trespass", "trespass offering", "Lev 7:37", offering="trespass"),
    Entry("consecration", "the consecration", "Lev 7:37"),
    Entry("peace", "sacrifice of peace offerings", "Lev 7:37",
          offering="peace"),
]

SINAI = [
    Entry("moses", "Moses", "Lev 7:38"),
    Entry("mount", "Mount Sinai", "Lev 7:38"),
    Entry("wilderness", "wilderness of Sinai", "Lev 7:38"),
]
