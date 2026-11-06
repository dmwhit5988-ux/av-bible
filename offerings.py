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
  the peace offerings (7:11-36, with the fat and the blood in 7:22-27),
  summed up in 7:37-38, which every offering cites as "The law".

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
                "its crop and its filth are cast beside the altar on the east",
                "Lev 1:15-17", "the whole bird"),
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
            Row("no one", "none of it: the priest burns all of it",
                "Lev 1:9, 13", "no one"),
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
            Row("every one", "seasoned with salt; made with no yeast and no "
                "honey", "Lev 2:11, 13", "salt, no yeast"),
            Row("the priests' own", "a tenth of an ephah of fine flour, half "
                "in the morning and half in the evening, made with oil on a "
                "griddle, from the day he is anointed", "Lev 6:20-21",
                "tenth of an ephah"),
        ),
        burns=(
            Row("every one", "a handful of its fine flour and its oil, with "
                "all its frankincense, as its memorial", "Lev 2:2, 9; 6:15",
                "a handful"),
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
             "First fruits may be offered, but not to rise for a pleasant "
             "aroma on the altar (2:12)."),
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
                "and all the fat on them, the two kidneys and their fat, and "
                "the cover on the liver", "Lev 3:3-5, 14-16", "the fat"),
            Row("a lamb", "the same, and the entire tail fat", "Lev 3:9-11",
                "the fat, the tail"),
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
            Row("the poor", "two turtledoves, or two young pigeons, if he "
                "can't afford a lamb: one for a sin offering, and the other "
                "for a burnt offering", "Lev 5:7",
                "two turtledoves or young pigeons",
                things=("turtledove", "pigeon")),
            Row("the poorest", "a tenth of an ephah of fine flour, if he can't "
                "afford two birds, with no oil and no frankincense",
                "Lev 5:11", "a tenth of an ephah", things=("fine flour",)),
        ),
        burns=(
            Row("a bull", "all its fat, the two kidneys and the cover on the "
                "liver, on the altar of burnt offering", "Lev 4:8-10, 19",
                "the fat"),
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
                "burnt offering", "Lev 4:5-7, 16-18", "before the veil"),
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
        when=Dim("when", "required: when a sin done unintentionally is made "
                 "known to him (4:2, 14, 23, 28), or when he is guilty of one "
                 "of these (5:1-5)", STATED, "Lev 4:2, 14, 23, 28; 5:1-5"),
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
            Row("a sin he didn't know", "a ram without defect from the flock, "
                "according to your estimation", "Lev 5:17-18", "a ram"),
            Row("a wrong against his neighbor", "he restores it in full and "
                "adds a fifth part more, to its owner; then a ram without "
                "defect from the flock", "Lev 6:2-6", "a fifth, a ram"),
        ),
        burns=(
            Row("the ram", "all its fat: the fat tail, the fat that covers the "
                "innards, the two kidneys and the cover on the liver",
                "Lev 7:3-5", "the fat"),
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
             "killed where the burnt offering is killed (7:2). The silver is "
             "the ram's estimation, not a second thing brought (5:15)."),
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
