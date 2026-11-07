"""The wilderness journey: the camps of Numbers 33 from Rameses to the plains
of Moab, the sea crossing, what happened at the camps, the text's own dates
and lengths of time, and the other itineraries (Numbers 21, Deuteronomy 2
and 10, Judges 11). For the wilderness journey reference page
(generate_wilderness_reference.py), drawn on sinai.py's gulfs and lakes and
gazetteer's Levant.

How it was gathered (2026-11-06). Every name is spelled as the WEB spells it
in its Numbers 33 verse (`misspelled()` checks this against the text), and
every ref was read with verse_refs.parse, so each verse exists in the WEB.
A site's point is one point fact: its Wikidata item's coordinate (P625),
or, where an item has none, the Wikipedia article's that the `wiki` field
names. A camp that is also a place of gazetteer.SITES (Kadesh, Dibon Gad,
Nebo, Beth Jeshimoth, Abel Shittim) takes gazetteer's site as it stands;
Rameses and Mount Sinai take near_east's. Nothing is placed from
acts_geography.SERMON_SITES, whose wilderness points are schematic.

- **STATIONS** are the forty-two camps of Numbers 33 in its order, Rameses
  first. Each has its WEB name, its Numbers 33 verses (`num33`, from the
  verse where they encamp to the verse where they leave), its other WEB
  names, the other verses that name it (`refs`), where the narrative tells
  of it (`story`, for a page opened from a verse), its card and its site.
- **A site** has a certainty: KNOWN (the name survives, or inscriptions or
  excavation fix it), PROBABLE (most scholars agree), POSSIBLE (one
  proposal of several) or TRADITIONAL (held by tradition, on the southern
  route, and not otherwise shown). Most camps have none (`site` is None):
  they are not identified, and the page draws them in their order along the
  route, never at a point. `proposed` keeps their candidates for the record.
- **CROSSING** is "through the middle of the sea" (Numbers 33:8), at the
  traditional place by Clysma (Suez), with the other proposals.
- **EVENTS** are what happened at a camp (`at`, a station key), or between
  two camps where the text names none (`at`, a pair of keys: the bronze
  serpent between Mount Hor and Oboth).
- **DATES** are the verses that give a month and day, a month, or a year,
  counted from the exodus as year 1; `stated` is whether the verse itself
  gives the year, and `inferred` says how the rest was worked out. **SPANS**
  are the lengths of time the text gives, with their dates where those
  follow: `derived` where the length itself is worked out from two dates,
  `placed` where the text gives the length and only its start is inferred.
- **VARIANTS** are the other lists of the route, given as lists: no point
  is placed for a name they alone have.
- **ROUTE_VIA** holds our own points ("~") for the line between two camps
  with sites, where a straight line would cross the sea or a lake, where
  the traditional route runs along a coast or a valley, or where the line
  back north from Ezion Geber would cross the way down at a camp: the line
  is ours, as the page says.
"""

import json
import os
import re
from typing import NamedTuple, Optional

import gazetteer as _GZ
import near_east as _NE
from config import BIBLES_DIR
from gazetteer import KNOWN, POSSIBLE, PROBABLE, Region

TRADITIONAL = "traditional"
CERTAINTIES = (KNOWN, PROBABLE, POSSIBLE, TRADITIONAL)


class Site(NamedTuple):
    name: str                    # what the dot marks, for the card
    lat: float
    lon: float
    certainty: str
    qid: str = ""                # its Wikidata item
    wiki: str = ""               # or the Wikipedia article the point is from
    why: str = ""
    since: str = ""              # for a traditional site: who has held it, since when
    gazetteer: str = ""          # the gazetteer.SITES key it is taken from
    source: str = ""             # how the point was chosen, for the record


class Station(NamedTuple):
    key: str
    name: str                    # as Numbers 33 spells it
    num33: str                   # its verses in Numbers 33
    card: str
    aka: tuple = ()              # its other WEB names
    refs: str = ""               # the other verses that name it
    story: str = ""              # the passages that tell of it
    site: Optional[Site] = None
    proposed: str = ""           # candidate sites, for the record (no site)
    namesakes: str = ""
    differs: str = ""            # where Numbers 33 and the narrative differ
    more: tuple = ()             # other verse groups: (label, refs)
    ends: tuple = ()             # a camp that stretches between two places


class Event(NamedTuple):
    key: str
    label: str                   # four words at most, the WEB's
    refs: str
    note: str                    # what happened, in the WEB's words
    at: object                   # a station key, or (from, to) between two


class Date(NamedTuple):
    ref: str
    year: int                    # from the exodus, as year 1
    month: Optional[int]
    day: Optional[int]
    stated: bool                 # the verse itself gives the year
    station: str
    label: str
    card: str
    inferred: str = ""           # how the year, month or day was worked out
    also: str = ""
    end_day: int = 0


class Span(NamedTuple):
    ref: str
    length: str
    days: Optional[int]
    years: Optional[int]
    station: Optional[str]
    label: str
    card: str
    start: tuple = ()            # (year, month, day) where it follows
    end: tuple = ()
    also: str = ""
    note: str = ""
    derived: bool = False        # worked out from two dates, not stated
    to: str = ""
    placed: bool = False         # a length the text gives, its start inferred


class Variant(NamedTuple):
    key: str
    title: str
    ref: str
    names: tuple                 # in the text's order, its own spellings
    note: str


def _gz(key, **kw):
    """A gazetteer site, as it stands there."""
    s = _GZ.SITES[key]
    out = Site(s.modern or s.name, s.lat, s.lon, s.certainty, qid=s.qid, why=s.why,
               gazetteer=key)
    return out._replace(**kw)


_RAMESES = _NE.SITES["rameses"]
_SINAI = _NE.SITES["mount_sinai"]


# ===========================================================================
# The camps of Numbers 33
# ===========================================================================

_UNPLACED = ("A camp named only in Numbers 33. It is not identified.")

STATIONS = [
    Station(
        "rameses", "Rameses", "Num 33:3, 5",
        "Rameses is where the march began, on the fifteenth day of the first "
        "month (Numbers 33:3); Raamses is also one of the storage cities "
        "Israel built (Exodus 1:11). Most scholars take it to be "
        "Pi-Ramesses, Ramesses II's delta capital, whose ruins lie at Qantir.",
        aka=("Raamses",),
        refs="Gen 47:11; Exod 1:11; 12:37",
        story="Exod 12:1-36; Num 33:1-4",
        site=Site("Pi-Ramesses, at Qantir in the eastern delta", _RAMESES.lat, _RAMESES.lon,
                  PROBABLE, qid=_RAMESES.qid,
                  why="Pi-Ramesses is fixed at Qantir by Bietak's mapping of the old "
                      "Pelusiac branch of the Nile and the Austrian excavations; Tanis, "
                      "the older proposal, holds only monuments moved there later. That "
                      "the Bible's Rameses is Pi-Ramesses is the usual modern view; "
                      "Saadia Gaon put it at Ain Shams.",
                  source="near_east.SITES['rameses']"),
        differs="Numbers 33:3-4 dates only the start, and adds that the Egyptians "
                "were burying their firstborn as Israel left, and that Yahweh executed "
                "judgments on their gods (promised in Exodus 12:12)."),
    Station(
        "succoth", "Succoth", "Num 33:5-6",
        "Succoth was the first camp out of Rameses (Exodus 12:37; Numbers 33:5). "
        "It is often taken to be Egyptian Tjeku in Wadi Tumilat, perhaps Tell "
        "el-Maskhuta, but that mound is also claimed for Pithom, so the site is "
        "only a proposal.",
        refs="Exod 12:37; 13:20",
        story="Exod 12:37-13:19",
        site=Site("Tell el-Maskhuta, in Wadi Tumilat", 30.5528, 32.0994, POSSIBLE,
                  wiki="de:Tell el-Maschuta",
                  why="Succoth is usually read as Egyptian Tjeku, the district at the "
                      "east end of Wadi Tumilat. Kitchen and the Italian excavators put "
                      "Succoth at Tell el-Maskhuta, while Naville, Petrie, Holladay and "
                      "Redford take that mound for Pithom, and Gardiner rejected both.",
                  source="Wikidata has no point for Tell el-Maskhuta; German Wikipedia's "
                         "agrees with Wikidata's Pithom point (Q1630019)."),
        namesakes="Succoth in the Jordan valley (Genesis 33:17; Judges 8) is another "
                  "place."),
    Station(
        "etham", "Etham", "Num 33:6-7",
        "Etham lay “in the edge of the wilderness” (Exodus 13:20; Numbers "
        "33:6), and Numbers 33:8 calls the land beyond the sea “the wilderness "
        "of Etham.” The place is not identified.",
        refs="Exod 13:20",
        story="Exod 13:20-22",
        proposed="Egeria (late 4th century) was shown an Etham on her road to Clysma "
                 "(Suez), but not where. Wikidata gives the item a point north of "
                 "Suez with no source, so no site is drawn."),
    Station(
        "pihahiroth", "Pihahiroth", "Num 33:7-8",
        "Here Israel turned back and camped by the sea, before Baal Zephon and "
        "Migdol, and Pharaoh's army caught up with them (Exodus 14:2, 9; Numbers "
        "33:7). None of the three places is identified.",
        aka=("Hahiroth",),
        refs="Exod 14:2, 9",
        story="Exod 14:1-20",
        proposed="Egeria was shown Migdol and Pihahiroth on her road to Clysma. "
                 "Wikidata gives the item a point on the shore south-west of Suez "
                 "with no source, so no site is drawn. Baal Zephon has been put at "
                 "Mount Casius by Lake Bardawil, north-east of Wadi Tumilat, and on "
                 "the Gulf of Suez.",
        differs="Numbers 33:7 has them turn back to Pihahiroth “which is before "
                "Baal Zephon” and encamp before Migdol; Exodus 14:2 has them encamp "
                "“before Pihahiroth, between Migdol and the sea, before Baal "
                "Zephon”. Numbers 33:8 shortens the name to Hahiroth.",
        more=(("Migdol and Baal Zephon", "Exod 14:2, 9; Num 33:7"),)),
    Station(
        "marah", "Marah", "Num 33:8-9",
        "After three days without water they came to Marah, whose waters were "
        "bitter until Moses threw in the tree Yahweh showed him (Exodus "
        "15:22-25). Tradition puts it at the bitter spring of Ain Hawarah in "
        "western Sinai, but the place is not identified.",
        refs="Exod 15:23",
        story="Exod 15:22-26",
        proposed="Ain Hawarah, a bitter spring about 47 miles south-east of Suez, is "
                 "the traditional Marah of the southern route (nineteenth-century "
                 "travellers and surveys; Easton's Bible Dictionary, 1897: "
                 "“probably”). Some propose Bir el-Mura, whose Arabic name is akin "
                 "to Marah, and routes that cross further north put Marah near the "
                 "Bitter Lakes. Ain Hawarah has no point fact, and Wikidata's point "
                 "for biblical Marah has no source, so no site is drawn.",
        differs="Numbers 33:8 calls the three days the wilderness of Etham; Exodus "
                "15:22 calls it the wilderness of Shur. Numbers 33 says nothing of "
                "the bitter water."),
    Station(
        "elim", "Elim", "Num 33:9-10",
        "Elim had twelve springs of water and seventy palm trees, and Israel "
        "camped there by the waters (Exodus 15:27; Numbers 33:9). It is "
        "traditionally placed at the oasis of Wadi Gharandel in western Sinai, "
        "which is not proven.",
        refs="Exod 15:27; 16:1",
        story="Exod 15:27",
        site=Site("Wadi Gharandel, an oasis in western Sinai", 29.2547, 32.9158,
                  TRADITIONAL, qid="Q22935877",
                  why="Elim is generally thought to be the oasis of Wadi Gharandel, "
                      "about 100 km south-east of Suez, on the southern route. Menashe "
                      "Har-El proposed 'Uyun Musa instead, which Hoffmeier finds too "
                      "close to the crossing.",
                  since="Nineteenth-century travellers and the Sinai survey of 1868-69; "
                        "Stewart (1857) has “Wadi Gherundel probably Elim”."),
        differs="Numbers 33:9 keeps Elim's twelve springs and seventy palm trees, as "
                "Exodus 15:27 does."),
    Station(
        "red_sea_camp", "Red Sea", "Num 33:10-11",
        "After Elim they “encamped by the Red Sea” (Numbers 33:10), a camp "
        "that Exodus does not mention. Its place is not known; on the southern "
        "route it would be on the shore of the Gulf of Suez, south of Elim.",
        proposed="Often put near Abu Zenima, on the shore; no point is fixed.",
        differs="Only Numbers 33 has this camp: Exodus 16:1 goes from Elim to the "
                "wilderness of Sin."),
    Station(
        "wilderness_of_sin", "wilderness of Sin", "Num 33:11-12",
        "The wilderness of Sin lies “between Elim and Sinai” (Exodus 16:1); "
        "there the people grumbled for food and Yahweh gave quail and manna. "
        "Where it lies depends on where Sinai is; tradition puts it on the "
        "coastal plain of el-Markha.",
        refs="Exod 16:1; 17:1",
        story="Exod 16:1-36",
        proposed="The plain of el-Markha, on the Gulf of Suez, follows from the Jebel "
                 "Musa tradition for Sinai; no point fact was found for it.",
        namesakes="“Sin, the stronghold of Egypt” (Ezekiel 30:15-16) is an "
                  "Egyptian city, not this wilderness.",
        differs="Numbers 33:11 lists it as a camp; Exodus 16:1 says they came to it on "
                "the fifteenth day of the second month."),
    Station(
        "dophkah", "Dophkah", "Num 33:12-13",
        "Dophkah is named only in Numbers 33:12-13, between the wilderness of Sin "
        "and Alush. It is not identified; one proposal links the name to the "
        "Egyptian turquoise mines at Serabit el-Khadim.",
        site=Site("Serabit el-Khadim, the Egyptian turquoise mines", 29.0367, 33.4594,
                  POSSIBLE, qid="Q1462523",
                  why="Some link Dophkah with the Egyptian word for turquoise and so "
                      "with the mines at Serabit el-Khadim or Wadi Maghareh; the "
                      "derivation is unproven. Easton's put it somewhere in Wadi "
                      "Feiran."),
        differs="Dophkah and Alush are only in Numbers 33: Exodus 17:1 goes from the "
                "wilderness of Sin to Rephidim."),
    Station(
        "alush", "Alush", "Num 33:13-14",
        "Alush is named only in Numbers 33:13-14, the last camp before Rephidim. "
        "Its place is not known.",
        differs="Dophkah and Alush are only in Numbers 33: Exodus 17:1 goes from the "
                "wilderness of Sin to Rephidim."),
    Station(
        "rephidim", "Rephidim", "Num 33:14-15",
        "At Rephidim there was no water until Moses struck the rock in Horeb, and "
        "the place was named Massah and Meribah; there too Israel fought Amalek "
        "(Exodus 17). Tradition places it at the oasis of Wadi Feiran, which is "
        "not proven.",
        aka=("Massah", "Meribah"),
        refs="Exod 17:1, 7, 8; 19:2",
        story="Exod 17:1-16",
        site=Site("Wadi Feiran, an oasis in southern Sinai", 28.7187, 33.6202,
                  TRADITIONAL, qid="Q18191741",
                  why="The oasis of Wadi Feiran is the classic Rephidim of the southern "
                      "route, argued by E. H. Palmer of the 1868-69 survey. Others "
                      "propose Wadi Refayid in south-west Sinai, or, for those who put "
                      "Sinai in Midian, a site north of al-Bad'.",
                  since="Feiran is Byzantine Pharan, a monastic centre on the pilgrims' "
                        "road to Sinai, where Egeria stopped; the Rephidim "
                        "identification is the 19th-century surveyors'."),
        differs="Numbers 33:14 keeps “no water for the people to drink” but leaves "
                "out the rock in Horeb, the names Massah and Meribah, and the battle "
                "with Amalek.",
        more=(("Massah and Meribah", "Deut 6:16; 9:22; 33:8; Ps 95:8"),)),
    Station(
        "wilderness_of_sinai", "wilderness of Sinai", "Num 33:15-16",
        "In the third month they came into the wilderness of Sinai and camped "
        "before the mountain, where Yahweh gave the commandments; they set out "
        "again in the second month of the second year (Exodus 19:1-2; Numbers "
        "10:11-12). The mountain is traditionally Jebel Musa above Saint "
        "Catherine's Monastery, held since at least the 4th century; scholars "
        "propose several others.",
        aka=("Mount Sinai", "Sinai", "Horeb"),
        refs="Exod 19:1-2; Lev 7:38; Num 1:1, 19; 3:4, 14; 9:1, 5; 10:12; 26:64",
        story="Exod 19-40; Lev 1-27; Num 1:1-10:36; Deut 1:6-18",
        site=Site("Jebel Musa, above Saint Catherine's Monastery", _SINAI.lat, _SINAI.lon,
                  TRADITIONAL, qid=_SINAI.qid,
                  why="Jebel Musa is the Christian and Muslim traditional Sinai. Jebel "
                      "Serbal, Jebel Katarina beside it, Har Karkom in the Negev and "
                      "Jabal al-Lawz in Midian are among the others proposed; none is "
                      "proven.",
                  since="Egeria (late 4th century) found a church on the summit and monks "
                        "on the mountain; the monastery at its foot was built in the 6th "
                        "century.",
                  source="near_east.SITES['mount_sinai']"),
        differs="Numbers 33:15 names only the wilderness of Sinai; Exodus has them "
                "encamp before the mountain, which it calls Mount Sinai (19:2, 11), "
                "and puts the rock in Horeb at Rephidim (17:6).",
        more=(("The mountain: Mount Sinai, Horeb, the Mountain of God",
               "Exod 3:1; 17:6; 18:5; 19:11, 18, 20, 23; 24:16; 31:18; 33:6; 34:2, 4, 29, "
               "32; Lev 7:38; 25:1; 26:46; 27:34; Num 3:1; 28:6; Deut 1:2, 6, 19; 4:10, "
               "15; 5:2; 9:8; 18:16; 29:1; 33:2; Judg 5:5; 1 Kgs 8:9; 19:8; 2 Chr 5:10; "
               "Neh 9:13; Ps 68:8, 17; 106:19; Mal 4:4; Acts 7:30, 38; Gal 4:24, 25"),)),
    Station(
        "kibroth_hattaavah", "Kibroth Hattaavah", "Num 33:16-17",
        "The first camp after Sinai, where the people craved meat: quail came on "
        "the wind, and a plague followed. Its name means graves of craving. It is "
        "not identified.",
        refs="Num 11:34, 35; Deut 9:22",
        story="Num 11:4-35",
        proposed="Rueis el-Ebeirig, north-east of Jebel Musa (Palmer; Janzen). "
                 "Wikidata's point for it is an arc-minute shared with its Hazeroth, "
                 "so it marks no site."),
    Station(
        "hazeroth", "Hazeroth", "Num 33:17-18",
        "Here Miriam and Aaron spoke against Moses, and Miriam was struck with "
        "leprosy and shut outside the camp seven days. Tradition puts Hazeroth "
        "at the oasis of Ain Hudra, north-east of the traditional Sinai.",
        refs="Num 11:35; 12:16; Deut 1:1",
        story="Num 12:1-16",
        site=Site("Ain Hudra, an oasis north-east of Jebel Musa", 28.89682, 34.42156,
                  TRADITIONAL, wiki="he:חצרות",
                  why="The oasis of Ain Hudra is the long-held Hazeroth for those who put "
                      "Sinai at Jebel Musa, from the likeness of the names. Those who put "
                      "Sinai elsewhere place it elsewhere: Jarvis put it at Hadhira, "
                      "under Jebel Halal.",
                  since="Burckhardt (early 19th century), followed by most dictionaries.",
                  source="Hebrew Wikipedia's Hazeroth article gives the point for Ein "
                         "Hudra; no Wikidata or English Wikipedia point exists for it."),
        differs="Deuteronomy 1:1 names a Hazeroth among places in the Arabah over "
                "against Suf; most take it for this camp."),
    Station("rithmah", "Rithmah", "Num 33:18-19", _UNPLACED,
            proposed="Wadi el-Rutmi or Wadi Abu Retemat (Janzen); the name means "
                     "broom bush."),
    Station("rimmon_perez", "Rimmon Perez", "Num 33:19-20", _UNPLACED,
            proposed="Rarra Rarmun (Janzen)."),
    Station("libnah", "Libnah", "Num 33:20-21",
            "A camp in the wilderness, not the Libnah of Judah that Joshua took. It "
            "is not identified.",
            proposed="Wadi el-Beidha or Jebel Libni (Janzen).",
            namesakes="Libnah of Judah, the town Joshua took and a Levite city (Joshua "
                      "10:29-39; 21:13; 2 Kings 19:8), is another place."),
    Station("rissah", "Rissah", "Num 33:21-22", _UNPLACED,
            proposed="Jebel Ruisset el-Negin (Janzen)."),
    Station("kehelathah", "Kehelathah", "Num 33:22-23", _UNPLACED,
            proposed="Perhaps Kuntillet Ajrud (Janzen); some take Makheloth (33:25) for "
                     "the same name twice."),
    Station("mount_shepher", "Mount Shepher", "Num 33:23-24",
            "A mountain camp named only in Numbers 33. It is not identified.",
            proposed="Jebel esh-Shereif (Janzen)."),
    Station("haradah", "Haradah", "Num 33:24-25", _UNPLACED,
            proposed="Perhaps Ras el-Khorasha (Janzen)."),
    Station("makheloth", "Makheloth", "Num 33:25-26", _UNPLACED,
            proposed="None; perhaps the same name as Kehelathah (Janzen)."),
    Station("tahath", "Tahath", "Num 33:26-27", _UNPLACED,
            namesakes="Tahath the Levite and the Ephraimites named Tahath (1 Chronicles "
                      "6:24, 37; 7:20) are people."),
    Station("terah", "Terah", "Num 33:27-28",
            "A camp named only in Numbers 33, not Abraham's father Terah. It is not "
            "identified.",
            proposed="Tara umm Haluf or Jebel Taret um-Basis (Janzen).",
            namesakes="Terah, Abraham's father (Genesis 11:24-32; Joshua 24:2; Luke "
                      "3:34), is a person."),
    Station("mithkah", "Mithkah", "Num 33:28-29", _UNPLACED),
    Station("hashmonah", "Hashmonah", "Num 33:29-30", _UNPLACED,
            proposed="Perhaps el-Qusaima, near Wadi el-Hashmim (Janzen)."),
    Station(
        "moseroth", "Moseroth", "Num 33:30-31",
        "Deuteronomy calls it Moserah and says Aaron died and was buried there; "
        "Numbers puts his death on Mount Hor. It is not identified.",
        aka=("Moserah",),
        refs="Deut 10:6",
        proposed="Bir al-Hafir (Janzen); others put it near Mount Hor, to square "
                 "Deuteronomy 10:6 with Numbers 20:22-29.",
        differs="Deuteronomy 10:6 goes from Beeroth Bene Jaakan to Moserah; Numbers "
                "33:30-31 goes from Moseroth to Bene Jaakan."),
    Station(
        "bene_jaakan", "Bene Jaakan", "Num 33:31-32",
        "Deuteronomy calls it Beeroth Bene Jaakan, the wells of the sons of Jaakan, "
        "and puts it before Moserah, not after. It is not identified.",
        aka=("Beeroth Bene Jaakan",),
        refs="Deut 10:6",
        proposed="Birein, near Nabataean Nitzana (Janzen).",
        namesakes="Jaakan the Horite (1 Chronicles 1:42) is a person; the name may "
                  "mean the wells of his sons."),
    Station(
        "hor_haggidgad", "Hor Haggidgad", "Num 33:32-33",
        "Deuteronomy calls it Gudgodah. It is not identified.",
        aka=("Gudgodah",),
        refs="Deut 10:7",
        proposed="Wadi Hadahad (Janzen)."),
    Station(
        "jotbathah", "Jotbathah", "Num 33:33-34",
        "Deuteronomy calls it a land of brooks of water. It is not identified; "
        "springs in the Arabah north of Eilat and at Taba south of it are "
        "proposed.",
        refs="Deut 10:7",
        proposed="The spring at Sabkhat et-Taba in the Arabah north of Eilat, the "
                 "only candidate with remains; Ein Ghadian by Kibbutz Yotvata, which "
                 "took the name; or Bir Taba south of Eilat (Rothenberg). No point fact "
                 "was found for any of them."),
    Station(
        "abronah", "Abronah", "Num 33:34-35",
        "A camp in the Arabah before Ezion Geber, named only in Numbers 33. The "
        "spring 'Ain ed-Defiyeh north of Eilat, at the place now called Avrona, "
        "is one proposal.",
        site=Site("Avrona, by the spring 'Ain ed-Defiyeh, north of Eilat", 29.66558, 35.01253,
                  POSSIBLE, wiki="he:עברונה",
                  why="'Ain ed-Defiyeh, a small spring in the Arabah 15-20 km north of "
                      "Eilat, is proposed by those who put Jotbathah at Ein Ghadian; the "
                      "site beside it keeps the name Avrona. Those who put Jotbathah at "
                      "Taba place Abronah at the head of the gulf instead.",
                  source="Hebrew Wikipedia's point for the Avrona site, beside the spring.")),
    Station(
        "ezion_geber", "Ezion Geber", "Num 33:35-36",
        "The camp at the head of the Gulf of Aqaba, beside Elath; later Solomon "
        "built a fleet here. Tell el-Kheleifeh, west of Aqaba, is the usual site, "
        "but its dating is disputed, and Pharaoh's Island off Sinai is the other "
        "proposal.",
        refs="Deut 2:8; 1 Kgs 9:26; 22:48; 2 Chr 8:17; 20:36",
        site=Site("Tell el-Kheleifeh, at the head of the Gulf of Aqaba", 29.547222, 34.980278,
                  POSSIBLE, qid="Q2402239",
                  why="Glueck dug Tell el-Kheleifeh (1938-40) as Solomon's Ezion Geber; "
                      "Pratico's reappraisal (1993) found no 10th-century level, so it "
                      "may be Elath or a later Ezion Geber. Petrie and Rothenberg "
                      "proposed the island harbour of Pharaoh's Island, 12 km "
                      "south-west.")),
    Station(
        "kadesh", "Kadesh", "Num 33:36-37",
        "Kadesh in the wilderness of Zin, the oasis on Canaan's southern edge. From "
        "here the spies were sent and came back; here Miriam died, Moses struck "
        "the rock at Meribah, and Edom refused them passage. Tell el-Qudeirat, by "
        "the region's richest spring, is the usual site.",
        aka=("Kadesh Barnea", "En Mishpat", "Meribah of Kadesh", "Meriboth Kadesh",
             "Meribath Kadesh"),
        refs="Gen 14:7; 16:14; 20:1; Num 13:26; 20:1, 14, 16, 22; 27:14; 32:8; 34:4; "
             "Deut 1:2, 19, 46; 2:14; 9:23; 32:51; Josh 10:41; 14:6, 7; 15:3; "
             "Judg 11:16, 17; Ezek 47:19; 48:28",
        story="Num 13:1-14:45; 20:1-21; Deut 1:19-46",
        site=_gz("kadesh_barnea", name="Tell el-Qudeirat, by Ein el-Qudeirat"),
        differs="The narrative brings Israel to Kadesh twice: the spies come back "
                "“to the wilderness of Paran, to Kadesh” in the second year "
                "(Numbers 13:26), and “the whole congregation came into the "
                "wilderness of Zin in the first month” (20:1), in the fortieth. "
                "Numbers 33 names Kadesh once, at 33:36, after Ezion Geber: the second "
                "arrival. Deuteronomy 1:46 has them stay “many days”."),
    Station(
        "mount_hor", "Mount Hor", "Num 33:37-41",
        "On Mount Hor, at the edge of Edom, Aaron was stripped of his garments, "
        "which were put on Eleazar, and he died on the top of the mountain at "
        "123. Tradition puts it at Jebel Harun above Petra, where a shrine of "
        "Aaron stands.",
        refs="Num 20:22, 23, 25, 27; 21:4; Deut 32:50",
        story="Num 20:22-21:3",
        site=Site("Jebel Harun, above Petra", 30.316777, 35.406538, TRADITIONAL,
                  qid="Q2915115",
                  why="Josephus put Aaron's death on a high mountain by Petra, and the "
                      "shrine of Aaron crowns Jebel Harun; but that peak stands inside "
                      "Edom, not at its edge (Numbers 33:37). Jebel Madurah, north-east "
                      "of Kadesh, and Ras el-Khorasha are the main other proposals.",
                  since="Josephus (1st century), and the shrine on the summit."),
        namesakes="The Mount Hor on the northern border (Numbers 34:7-8) is another "
                  "mountain.",
        differs="Numbers puts Aaron's death on Mount Hor (20:22-29; 33:38-39), in the "
                "fortieth year; Deuteronomy 10:6 puts it at Moserah. Numbers 33:40 "
                "repeats the king of Arad hearing of Israel (21:1-3)."),
    Station("zalmonah", "Zalmonah", "Num 33:41-42",
            "The first camp after Mount Hor, named only in Numbers 33. It is not "
            "identified.",
            proposed="'Ain es-Salmaneh, in the Arabah (Janzen)."),
    Station(
        "punon", "Punon", "Num 33:42-43",
        "A camp on the east side of the Arabah, at the copper-mining district of "
        "Feinan in Edom, where the name survives.",
        site=Site("Khirbet Feinan, in the copper district of the Arabah", 30.62775, 35.493647,
                  KNOWN, qid="Q28408071",
                  why="The name survives at Feinan (Eusebius's Phaino, the Roman copper "
                      "mines), and Khirbet Feinan is almost certainly Punon (MacDonald, "
                      "2015). Known for the town; the camp may have stood near it.")),
    Station(
        "oboth", "Oboth", "Num 33:43-44",
        "The first camp Numbers 21 names after the bronze serpent, on the way round "
        "Edom. It is not identified.",
        refs="Num 21:10, 11",
        story="Num 21:10",
        proposed="'Ain el-Weiba, Khirbet Ghweibah, el-Husub, or 'Ayna north of the "
                 "Zered (Janzen). There is no agreement."),
    Station(
        "iye_abarim", "Iye Abarim", "Num 33:44-45",
        "The ruins of Abarim, in the border of Moab, toward the sunrise. Numbers "
        "33:45 calls it Iyim, and Numbers 21:11 Iyeabarim. It is not identified.",
        aka=("Iyim", "Iyeabarim"),
        refs="Num 21:11",
        story="Num 21:11",
        proposed="On Moab's south-east border, near the Zered: 'Ayna on the King's "
                 "Highway, Khirbet Ay south-west of Kerak, or Khirbet el-Medeiyineh "
                 "(Janzen).",
        differs="Numbers 33:44-45 gives the camp two names in two verses: Iye Abarim "
                "where they encamp, Iyim where they leave."),
    Station(
        "dibon_gad", "Dibon Gad", "Num 33:45-46",
        "Dibon, north of the Arnon, which the children of Gad built, hence Dibon "
        "Gad. It is Dhiban in Jordan, where the Mesha Stele was found.",
        aka=("Dibon", "Dimon"),
        refs="Num 21:30; 32:3, 34; Josh 13:9, 17; Isa 15:2, 9; Jer 48:18, 22",
        site=_gz("dibon", name="Dhiban, in Jordan"),
        namesakes="Dibon in Judah (Nehemiah 11:25) is another place."),
    Station(
        "almon_diblathaim", "Almon Diblathaim", "Num 33:46-47",
        "A camp between Dibon and the mountains of Abarim, usually taken for the "
        "Beth Diblathaim of Jeremiah and the Mesha Stele. It is not identified; "
        "the ruins of Deleilat north of Dibon are proposed.",
        aka=("Beth Diblathaim",),
        refs="Jer 48:22",
        proposed="Khirbet Deleilat esh-Sherqiyeh or el-Gharbiyeh, north of Dibon, or "
                 "Nitl (Janzen).",
        namesakes="Almon of Benjamin (Joshua 21:18) is another place."),
    Station(
        "mountains_of_abarim", "mountains of Abarim", "Num 33:47-48",
        "The range at the edge of Moab's tableland above the Jordan valley, where "
        "they camped before Nebo. From this mountain of Abarim Moses was told to "
        "see the land and die. The dot marks Mount Nebo, which Numbers 33:47 "
        "names; the camp lay somewhere on the range before it.",
        aka=("mountain of Abarim", "Abarim"),
        refs="Num 27:12; Deut 32:49; Jer 22:20",
        story="Num 27:12-14; Deut 3:23-29; 32:48-52; 34:1-7",
        site=_gz("mount_nebo", name="Mount Nebo, the landmark the verse names")),
    Station(
        "plains_of_moab", "plains of Moab", "Num 33:48-49",
        "The last camp, in the Jordan valley across from Jericho, stretching from "
        "Beth Jeshimoth to Abel Shittim. Here Balaam looked down on them, Israel "
        "sinned at Baal Peor, the second census was taken, Moses died on Nebo "
        "above, and Joshua sent the spies.",
        refs="Num 22:1; 26:3, 63; 31:12; 33:50; 35:1; 36:13; Deut 34:1, 8; Josh 13:32",
        story="Num 22:1-32:42; 33:50-36:13; Deut 1:1-5; 3:12-22; 34:8-12; Josh 1-3",
        ends=("beth_jeshimoth", "shittim")),
]

STATION = {s.key: s for s in STATIONS}

# The two ends of the plains of Moab (Numbers 33:49), from gazetteer
ENDS = {
    "beth_jeshimoth": Station(
        "beth_jeshimoth", "Beth Jeshimoth", "Num 33:49",
        "The southern end of the camp, near the Jordan's mouth at the Salt Sea; "
        "later a town of Reuben. Its name lingers at Sweimeh; the mound itself is "
        "debated.",
        refs="Josh 12:3; 13:20; Ezek 25:9",
        site=_gz("beth_jeshimoth")),
    "shittim": Station(
        "shittim", "Abel Shittim", "Num 33:49",
        "The northern end of the camp, called Shittim, the acacias. Here Israel "
        "joined itself to Baal Peor, and from here Joshua sent the spies and set "
        "out for the Jordan.",
        aka=("Shittim",),
        refs="Num 25:1; Josh 2:1; 3:1; Mic 6:5",
        site=_gz("shittim"),
        namesakes="The valley of Shittim (Joel 3:18) is another, perhaps the Kidron."),
}


# ===========================================================================
# The sea
# ===========================================================================

class Crossing(NamedTuple):
    name: str
    num33: str
    card: str
    refs: str
    story: str
    site: Site
    landing: Site
    proposals: tuple             # (name, note)
    differs: str


CROSSING = Crossing(
    "through the middle of the sea", "Num 33:8",
    "Numbers 33:8 says only that they “crossed through the middle of the sea "
    "into the wilderness”; Exodus calls it the Red Sea (15:4, 22). Tradition "
    "since at least Egeria (late 4th century) put the crossing at Clysma, by "
    "Suez, with the landing at the springs of 'Uyun Musa. The other proposals "
    "are below, and none is agreed.",
    refs="Exod 13:18; 14:21-31; 15:1-21, 22; Deut 11:4; Josh 2:10; 4:23; 24:6-7; "
         "Neh 9:9-11; Ps 66:6; 78:13; 106:7-11; 136:13-15; Isa 51:10; 63:12-13; "
         "Acts 7:36; 1 Cor 10:1-2; Heb 11:29",
    story="Exod 14:21-15:21",
    site=Site("Clysma (al-Qulzum), at the head of the Gulf of Suez", 29.954611, 32.573972,
              TRADITIONAL, qid="Q3775676",
              why="Egeria was told that Clysma, named from its fort, is where the "
                  "children of Israel crossed the Red Sea.",
              since="Egeria (late 4th century)."),
    landing=Site("'Uyun Musa, the springs of Moses", 29.87694, 32.65833, TRADITIONAL,
                 qid="Q2903692",
                 why="Springs on the east shore of the gulf, south of Suez, named for "
                     "Moses: the landing of the traditional crossing."),
    proposals=(
        ("Lake Timsah", "On the isthmus, by Ismailia (Haynes, 1896)."),
        ("The Bitter Lakes", "On the isthmus; Kitchen and Hoffmeier favour the "
                             "isthmus in general."),
        ("Lake Bardawil (Sirbonis)", "The lagoon on the Mediterranean shore "
                                     "(Schleiden, Brugsch)."),
        ("Nuweiba, on the Gulf of Aqaba", "Ron Wyatt, Bob Cornuke and others."),
    ),
    differs="Numbers 33 says only that they crossed through the middle of the sea; "
            "Exodus names the Red Sea and tells the whole crossing.")


# ===========================================================================
# What happened, camp by camp
# ===========================================================================

EVENTS = [
    Event("firstborn-struck", "the firstborn struck", "Exod 12:29-31",
          "At midnight, Yahweh struck all the firstborn in the land of Egypt, and "
          "Pharaoh said, “Rise up, get out from among my people.”", "rameses"),
    Event("high-hand", "a high hand", "Num 33:3-4",
          "On the next day after the Passover, the children of Israel went out with "
          "a high hand in the sight of all the Egyptians, while the Egyptians were "
          "burying all their firstborn.", "rameses"),
    Event("unleavened-cakes", "unleavened cakes", "Exod 12:39",
          "They baked unleavened cakes of the dough which they brought out of Egypt, "
          "because they were thrust out of Egypt and couldn’t wait.", "succoth"),
    Event("pillar-of-cloud", "pillar of cloud", "Exod 13:20-22",
          "They encamped in Etham, in the edge of the wilderness, and Yahweh went "
          "before them by day in a pillar of cloud, and by night in a pillar of "
          "fire.", "etham"),
    Event("turned-back", "turned back", "Exod 14:1-4",
          "Yahweh told them to turn back and encamp before Pihahiroth, between Migdol "
          "and the sea, before Baal Zephon.", "pihahiroth"),
    Event("pharaoh-overtakes", "Pharaoh overtakes", "Exod 14:9-10",
          "Pharaoh’s army overtook them encamping by the sea, beside Pihahiroth, "
          "before Baal Zephon, and they were very afraid.", "pihahiroth"),
    Event("sea-divided", "the sea divided", "Exod 14:21-22",
          "Yahweh caused the sea to go back by a strong east wind all night, and the "
          "children of Israel went into the middle of the sea on the dry ground.",
          "crossing"),
    Event("waters-returned", "the waters returned", "Exod 14:26-30",
          "The waters returned, and covered the chariots and the horsemen, even all "
          "Pharaoh’s army that went in after them into the sea.", "crossing"),
    Event("song", "the song of Moses", "Exod 15:1-21",
          "Moses and the children of Israel sang, and Miriam answered them, “The "
          "horse and his rider he has thrown into the sea.”", "crossing"),
    Event("bitter-water", "bitter water sweetened", "Exod 15:22-25",
          "They couldn’t drink from the waters of Marah, for they were bitter; "
          "Yahweh showed Moses a tree, he threw it into the waters, and the waters "
          "were made sweet.", "marah"),
    Event("statute", "a statute and ordinance", "Exod 15:25-26",
          "There he made a statute and an ordinance for them, and there he tested "
          "them: “I am Yahweh who heals you.”", "marah"),
    Event("twelve-springs", "twelve springs", "Exod 15:27",
          "They came to Elim, where there were twelve springs of water, and seventy "
          "palm trees: and they encamped there by the waters.", "elim"),
    Event("quail-and-manna", "quail and manna", "Exod 16:11-21, 31",
          "In the evening, quail came up and covered the camp; and in the morning, on "
          "the surface of the wilderness was a small round thing. “The house of "
          "Israel called its name Manna” (16:31).", "wilderness_of_sin"),
    Event("sabbath", "the Sabbath", "Exod 16:22-30",
          "On the sixth day they gathered twice as much bread, for “tomorrow is a "
          "solemn rest, a holy Sabbath to Yahweh.”", "wilderness_of_sin"),
    Event("rock-in-horeb", "water from the rock", "Exod 17:1-7",
          "Moses struck the rock in Horeb, and he called the name of the place "
          "Massah, and Meribah, because the children of Israel quarreled.",
          "rephidim"),
    Event("amalek", "battle with Amalek", "Exod 17:8-16",
          "Amalek came and fought with Israel in Rephidim; when Moses held up his "
          "hand, Israel prevailed, and Joshua defeated Amalek.", "rephidim"),
    Event("jethro", "Jethro's counsel", "Exod 18:1-27",
          "Jethro came with Moses’ wife and sons “into the wilderness where he "
          "was encamped, at the Mountain of God” (18:5), and counselled him to "
          "appoint rulers over the people. Exodus tells it before Israel comes into "
          "the wilderness of Sinai (19:1-2); Deuteronomy 1:6-18 puts the appointing "
          "of the rulers at Horeb.", "wilderness_of_sinai"),
    Event("commandments", "the ten commandments", "Exod 19:16-20:17",
          "Yahweh came down on Mount Sinai in fire, and God spoke all these words: "
          "“I am Yahweh your God, who brought you out of the land of Egypt.”",
          "wilderness_of_sinai"),
    Event("golden-calf", "the golden calf", "Exod 32:1-35",
          "When Moses delayed to come down from the mountain, Aaron made a molten "
          "calf.", "wilderness_of_sinai"),
    Event("tabernacle-raised", "the tabernacle raised", "Exod 40:17-38",
          "In the first month in the second year, on the first day of the month, the "
          "tabernacle was raised up, and the cloud covered the Tent of Meeting.",
          "wilderness_of_sinai"),
    Event("census", "the census", "Num 1:1-46",
          "Yahweh spoke to Moses in the wilderness of Sinai: “Take a census of all "
          "the congregation of the children of Israel.”", "wilderness_of_sinai"),
    Event("cloud-lifts", "the cloud lifted", "Num 10:11-12",
          "In the second year, in the second month, on the twentieth day, the cloud "
          "was taken up, and they went forward out of the wilderness of Sinai.",
          "wilderness_of_sinai"),
    Event("taberah", "fire at Taberah", "Num 11:1-3",
          "The people complained, and Yahweh’s fire burned among them; the name of "
          "that place was called Taberah. Numbers 33 doesn't list it; the narrative "
          "tells it on the way from Sinai, before Kibroth Hattaavah.",
          ("wilderness_of_sinai", "kibroth_hattaavah")),
    Event("seventy-elders", "seventy elders", "Num 11:16-30",
          "Yahweh took of the Spirit that was on Moses and put it on the seventy "
          "elders, and they prophesied.", "kibroth_hattaavah"),
    Event("quail-plague", "quail and plague", "Num 11:31-34",
          "A wind from Yahweh brought quails from the sea, and while the meat was "
          "still between their teeth Yahweh struck the people with a very great "
          "plague.", "kibroth_hattaavah"),
    Event("miriam-leprous", "Miriam made leprous", "Num 12:1-15",
          "Miriam and Aaron spoke against Moses, and Miriam was leprous, as white as "
          "snow, and was shut up outside of the camp seven days.", "hazeroth"),
    Event("aaron-moserah", "Aaron died (Deuteronomy)", "Deut 10:6",
          "The children of Israel traveled from Beeroth Bene Jaakan to Moserah. There "
          "Aaron died, and there he was buried.", "moseroth"),
    Event("brooks", "brooks of water", "Deut 10:7",
          "From Gudgodah to Jotbathah, a land of brooks of water.", "jotbathah"),
    Event("spies-return", "the spies return", "Num 13:25-33",
          "They returned from spying out the land at the end of forty days, to the "
          "wilderness of Paran, to Kadesh, and brought back word.", "kadesh"),
    Event("forty-years", "forty years decreed", "Num 14:26-35",
          "“Your dead bodies shall fall in this wilderness… your children shall be "
          "wanderers in the wilderness forty years.”", "kadesh"),
    Event("miriam-died", "Miriam died", "Num 20:1",
          "The people stayed in Kadesh. Miriam died there, and was buried there.",
          "kadesh"),
    Event("meribah", "the waters of Meribah", "Num 20:2-13",
          "Moses struck the rock with his rod twice, and water came out abundantly; "
          "these are the waters of Meribah.", "kadesh"),
    Event("edom-refuses", "Edom refuses passage", "Num 20:14-21",
          "Moses sent messengers from Kadesh to the king of Edom, but Edom refused to "
          "give Israel passage through his border.", "kadesh"),
    Event("aaron-died", "Aaron died", "Num 20:22-29",
          "Moses stripped Aaron of his garments, and put them on Eleazar his son. "
          "Aaron died there on the top of the mountain.", "mount_hor"),
    Event("arad", "the king of Arad", "Num 21:1-3",
          "The Canaanite, the king of Arad, fought against Israel; Israel destroyed "
          "their cities and called the place Hormah.", "mount_hor"),
    Event("bronze-serpent", "the bronze serpent", "Num 21:4-9",
          "They traveled from Mount Hor by the way to the Red Sea, to go around the "
          "land of Edom; Moses made a serpent of brass, and set it on the pole. The "
          "text tells it between Mount Hor and Oboth and places it at no camp.",
          ("mount_hor", "oboth")),
    Event("sihon", "Sihon defeated", "Num 21:21-32; Deut 2:24-37",
          "Sihon would not allow Israel to pass through his border, and fought "
          "against Israel at Jahaz; Israel took all his cities, from the Arnon to the "
          "Jabbok, and lived in Heshbon. Numbers 21 tells it after they crossed the "
          "Arnon and before the camp in the plains of Moab.",
          ("dibon_gad", "plains_of_moab")),
    Event("og", "Og defeated", "Num 21:33-35; Deut 3:1-11",
          "Og the king of Bashan went out against them, to battle at Edrei, north of "
          "this map; they struck him and possessed his land. Numbers 21 tells it after "
          "Sihon, before the camp in the plains of Moab.",
          ("dibon_gad", "plains_of_moab")),
    Event("see-the-land", "see the land", "Num 27:12-14",
          "Yahweh said to Moses, “Go up into this mountain of Abarim, and see the "
          "land which I have given to the children of Israel.”",
          "mountains_of_abarim"),
    Event("moses-died", "Moses died", "Deut 34:1-7",
          "Moses went up from the plains of Moab to Mount Nebo, to the top of Pisgah; "
          "Yahweh showed him all the land, and Moses died there in the land of Moab.",
          "mountains_of_abarim"),
    Event("balaam", "Balaam's oracles", "Num 22:1-24:25",
          "Balak the king of Moab sent for Balaam to curse Israel camped in the plains "
          "of Moab, but he blessed them.", "plains_of_moab"),
    Event("baal-peor", "Baal Peor", "Num 25:1-9",
          "Israel stayed in Shittim; and the people began to play the prostitute with "
          "the daughters of Moab, and joined himself to Baal Peor.", "plains_of_moab"),
    Event("second-census", "the second census", "Num 26:1-65",
          "These are those who were counted by Moses and Eleazar the priest in the "
          "plains of Moab by the Jordan at Jericho.", "plains_of_moab"),
    Event("this-law", "this law declared", "Deut 1:1-5",
          "Beyond the Jordan, in the land of Moab, Moses began to declare this law.",
          "plains_of_moab"),
    Event("mourned", "Moses mourned", "Deut 34:8",
          "The children of Israel wept for Moses in the plains of Moab thirty days.",
          "plains_of_moab"),
    Event("spies-jericho", "spies to Jericho", "Josh 2:1",
          "Joshua the son of Nun secretly sent two men out of Shittim as spies, "
          "saying, “Go, view the land, including Jericho.”", "plains_of_moab"),
]


# ===========================================================================
# The text's dates, counted from the exodus as year 1
# ===========================================================================

DATES = [
    Date("Exod 12:2", 1, 1, None, False, "rameses", "first month",
         "“This month shall be to you the beginning of months. It shall be the "
         "first month of the year to you.”",
         inferred="Year 1 by definition: the exodus year, whose first month this "
                  "verse sets. Exodus 13:4 names it the month Abib."),
    Date("Exod 12:3", 1, 1, 10, False, "rameses", "lamb chosen",
         "On the tenth day of this month every man was to take a lamb for his "
         "household.",
         inferred="The month from Exodus 12:2 (“this month”, the first month); "
                  "year 1 is the exodus year."),
    Date("Exod 12:6", 1, 1, 14, False, "rameses", "first Passover",
         "The lamb was kept until the fourteenth day of the same month, and the whole "
         "assembly killed it at evening; at midnight Yahweh struck all the firstborn "
         "in the land of Egypt (Exodus 12:29).",
         inferred="The month from Exodus 12:2; year 1 is the exodus year.",
         also="Exod 12:29"),
    Date("Exod 12:18", 1, 1, 14, False, "rameses", "unleavened bread",
         "In the first month, from the fourteenth day at evening until the twenty "
         "first day at evening, they were to eat unleavened bread.",
         inferred="Year 1 is the exodus year; the verse gives the month and the days "
                  "(the 14th to the 21st).",
         end_day=21),
    Date("Num 33:3", 1, 1, 15, False, "rameses", "out of Egypt",
         "They traveled from Rameses on the fifteenth day of the first month, the "
         "next day after the Passover, and went out with a high hand in the sight of "
         "all the Egyptians.",
         inferred="Year 1 is the exodus year; the verse gives the month and day. "
                  "Exodus 12:41 has the armies go out at the end of four hundred "
                  "thirty years, “to the day”, and 12:51 “that same day”.",
         also="Exod 12:41, 51; 13:4"),
    Date("Exod 16:1", 1, 2, 15, False, "wilderness_of_sin", "wilderness of Sin",
         "From Elim the whole congregation came to the wilderness of Sin, between Elim "
         "and Sinai, on the fifteenth day of the second month after their departing "
         "out of Egypt.",
         inferred="Year 1: the second month “after their departing” can only be "
                  "in the exodus year."),
    Date("Exod 19:1", 1, 3, None, False, "wilderness_of_sinai", "reach Sinai",
         "In the third month after they had gone out of Egypt, on that same day, they "
         "came into the wilderness of Sinai, and there Israel encamped before the "
         "mountain (Exodus 19:2).",
         inferred="Year 1: the third month after going out. The day is not given; "
                  "“on that same day” is often read as the first of the month."),
    Date("Exod 40:2", 2, 1, 1, False, "wilderness_of_sinai", "tabernacle commanded",
         "“On the first day of the first month you shall raise up the tabernacle of "
         "the Tent of Meeting.”",
         inferred="The month and day are stated; year 2 is taken from Exodus 40:17, "
                  "where it was done."),
    Date("Exod 40:17", 2, 1, 1, True, "wilderness_of_sinai", "tabernacle raised",
         "In the first month in the second year, on the first day of the month, the "
         "tabernacle was raised up; then the cloud covered the Tent of Meeting, and "
         "Yahweh’s glory filled the tabernacle (Exodus 40:34).",
         also="Exod 40:34"),
    Date("Num 7:1", 2, 1, 1, False, "wilderness_of_sinai", "altar dedicated",
         "On the day that Moses had finished setting up the tabernacle and anointed "
         "it, the princes gave offerings for the dedication of the altar, each prince "
         "on his day (Numbers 7:10-11).",
         inferred="Numbers 7:1 dates by “the day that Moses had finished setting up "
                  "the tabernacle”, which Exodus 40:17 puts on the first day of the "
                  "first month of the second year (also Numbers 9:15).",
         also="Num 7:10-11; 9:15"),
    Date("Num 9:5", 2, 1, 14, False, "wilderness_of_sinai", "Passover at Sinai",
         "They kept the Passover in the first month, on the fourteenth day of the "
         "month, at evening, in the wilderness of Sinai.",
         inferred="The year and month from Numbers 9:1 (“the first month of the "
                  "second year”), the day from 9:3 and 9:5. It is a month before "
                  "Numbers 1:1.",
         also="Num 9:1, 3"),
    Date("Num 1:1", 2, 2, 1, True, "wilderness_of_sinai", "census commanded",
         "Yahweh spoke to Moses in the wilderness of Sinai, in the Tent of Meeting, on "
         "the first day of the second month, in the second year after they had come "
         "out of the land of Egypt."),
    Date("Num 1:18", 2, 2, 1, False, "wilderness_of_sinai", "census taken",
         "They assembled all the congregation together on the first day of the second "
         "month, and declared their ancestry from twenty years old and upward.",
         inferred="The month and day are stated; year 2 from Numbers 1:1."),
    Date("Num 9:11", 2, 2, 14, False, "wilderness_of_sinai", "second-month Passover",
         "Those unclean because of a dead body were to keep the Passover in the "
         "second month, on the fourteenth day at evening.",
         inferred="A rule given in the second year (Numbers 9:1); the verse gives the "
                  "month and day. The text does not say it was kept that year.",
         also="Num 9:1"),
    Date("Num 10:11", 2, 2, 20, True, "wilderness_of_sinai", "cloud lifts",
         "In the second year, in the second month, on the twentieth day of the month, "
         "the cloud was taken up from over the tabernacle, and they went forward out "
         "of the wilderness of Sinai (Numbers 10:12).",
         also="Num 10:12"),
    Date("Num 20:1", 40, 1, None, False, "kadesh", "Miriam dies",
         "The whole congregation came into the wilderness of Zin in the first month. "
         "The people stayed in Kadesh. Miriam died there, and was buried there.",
         inferred="The verse gives the first month but no year. Year 40 is inferred: "
                  "from Kadesh they went to Mount Hor (Numbers 20:22; 33:37), where "
                  "Aaron died in the fortieth year, in the fifth month (33:38); and "
                  "Deuteronomy 2:14 puts thirty-eight years between Kadesh Barnea and "
                  "the brook Zered.",
         also="Num 20:22; 33:37, 38; Deut 2:14"),
    Date("Num 33:38", 40, 5, 1, True, "mount_hor", "Aaron dies",
         "Aaron the priest went up into Mount Hor at the commandment of Yahweh, and "
         "died there, in the fortieth year after the children of Israel had come out "
         "of the land of Egypt, in the fifth month, on the first day of the month. "
         "He was one hundred twenty-three years old (Numbers 33:39).",
         also="Num 33:39; 20:28"),
    Date("Deut 1:3", 40, 11, 1, True, "plains_of_moab", "Moses speaks",
         "In the fortieth year, in the eleventh month, on the first day of the month, "
         "Moses spoke to the children of Israel, beyond the Jordan, in the land of "
         "Moab (Deuteronomy 1:5).",
         also="Deut 1:5"),
    Date("Deut 34:5", 40, None, None, False, "plains_of_moab", "Moses dies",
         "Moses the servant of Yahweh died there in the land of Moab, one hundred "
         "twenty years old (Deuteronomy 34:7); the children of Israel wept for him in "
         "the plains of Moab thirty days (34:8).",
         inferred="Not dated. It falls after Deuteronomy 1:3 (the eleventh month of "
                  "year 40), and thirty days of mourning and the three days of Joshua "
                  "3:2 come before Joshua 4:19 (the tenth day of the first month), so "
                  "it was in the eleventh or twelfth month of year 40. He went up from "
                  "the plains of Moab (Deuteronomy 34:1).",
         also="Deut 34:1, 7, 8"),
    Date("Josh 4:19", 41, 1, 10, False, "gilgal", "cross the Jordan",
         "The people came up out of the Jordan on the tenth day of the first month, "
         "and encamped in Gilgal, on the east border of Jericho.",
         inferred="The month and day are stated. Year 41 is inferred: it is the first "
                  "month after Deuteronomy 1:3 (the eleventh month of year 40), and "
                  "Joshua 5:6 says they walked forty years in the wilderness. It is "
                  "the same day of the year as the lamb was chosen (Exodus 12:3).",
         also="Josh 5:6; Exod 12:3"),
    Date("Josh 5:10", 41, 1, 14, False, "gilgal", "Passover at Gilgal",
         "The children of Israel encamped in Gilgal. They kept the Passover on the "
         "fourteenth day of the month at evening in the plains of Jericho.",
         inferred="The month from Joshua 4:19, with no other month between; year 41, "
                  "as for 4:19."),
    Date("Josh 5:11", 41, 1, 15, False, "gilgal", "produce eaten",
         "They ate unleavened cakes and parched grain of the produce of the land on "
         "the next day after the Passover.",
         inferred="The day after the 14th (Joshua 5:10); year 41, as for 4:19."),
    Date("Josh 5:12", 41, 1, 16, False, "gilgal", "manna ceases",
         "The manna ceased on the next day, after they had eaten of the produce of "
         "the land; they ate of the fruit of the land of Canaan that year.",
         inferred="Read as the day after Joshua 5:11 (the 15th), so the 16th; the "
                  "words could also mean the 15th, the day after the Passover. Exodus "
                  "16:35 says they ate the manna forty years.",
         also="Exod 16:35"),
]

SPANS = [
    Span("Exod 12:18-19", "7 days", 7, None, "rameses", "unleavened bread",
         "From the fourteenth day of the first month at evening until the twenty "
         "first day at evening they ate unleavened bread; no yeast for seven days.",
         start=(1, 1, 14), end=(1, 1, 21)),
    Span("Exod 15:22", "3 days", 3, None, "marah", "three days without water",
         "From the Red Sea they went three days in the wilderness of Shur and found "
         "no water, until they came to Marah.",
         also="Exod 15:23; Num 33:8",
         note="Numbers 33:8 calls it three days’ journey in the wilderness of "
              "Etham."),
    Span("Num 33:3; Exod 16:1", "1 month", 30, None, "wilderness_of_sin", "a month out",
         "They left Rameses on the fifteenth day of the first month and came to the "
         "wilderness of Sin on the fifteenth day of the second month.",
         start=(1, 1, 15), end=(1, 2, 15), derived=True,
         note="Worked out from two dates, not stated as a length of time."),
    Span("Exod 19:10-16", "3 days", 3, None, "wilderness_of_sinai", "ready by the third day",
         "The people were sanctified today and tomorrow and made ready against the "
         "third day, when there were thunders and lightnings and a thick cloud on "
         "the mountain."),
    Span("Exod 24:16", "6 days", 6, None, "wilderness_of_sinai", "the cloud six days",
         "Yahweh’s glory settled on Mount Sinai, and the cloud covered it six days; "
         "the seventh day he called to Moses out of the middle of the cloud."),
    Span("Exod 24:18", "40 days", 40, None, "wilderness_of_sinai", "forty days on the mountain",
         "Moses entered the cloud and was on the mountain forty days and forty "
         "nights; at the end of them Yahweh gave him the two stone tablets "
         "(Deuteronomy 9:11).",
         also="Deut 9:9, 11"),
    Span("Exod 34:28", "40 days", 40, None, "wilderness_of_sinai", "forty days again",
         "He was there with Yahweh forty days and forty nights; he neither ate bread "
         "nor drank water, and wrote on the tablets the ten commandments.",
         also="Deut 10:10; 9:18, 25",
         note="Deuteronomy 9:18 and 9:25 (falling down before Yahweh forty days, "
              "“as at the first”) may be these forty days or another forty."),
    Span("Exod 29:35", "7 days", 7, None, "wilderness_of_sinai", "the priests consecrated",
         "Aaron and his sons were to be consecrated seven days, and atonement made "
         "for the altar seven days (Exodus 29:37).",
         also="Exod 29:37; Lev 8:33-35",
         note="Commanded here, and done in Leviticus 8:33-35. Not dated."),
    Span("Num 7:12, 78", "12 days", 12, None, "wilderness_of_sinai", "the princes' twelve days",
         "Each prince offered on his day for the dedication of the altar, Nahshon on "
         "the first day through Ahira the son of Enan on the twelfth day.",
         start=(2, 1, 1), end=(2, 1, 12), placed=True,
         note="It starts on the day the tabernacle was set up (Numbers 7:1; Exodus "
              "40:17). Whether the first prince’s day is the 1st or the 2nd is not "
              "said."),
    Span("Exod 19:1; Num 10:11", "about 11 months", 349, None, "wilderness_of_sinai",
         "the year at Sinai",
         "They came into the wilderness of Sinai in the third month after leaving "
         "Egypt, and the cloud was taken up on the twentieth day of the second month "
         "in the second year.",
         start=(1, 3, None), end=(2, 2, 20), derived=True,
         note="Worked out, not stated: about eleven months and nineteen days if "
              "Exodus 19:1 means the first day of the third month, about eleven "
              "months and five days if it means the fifteenth."),
    Span("Num 10:33", "3 days", 3, None, None, "three days’ journey",
         "They set forward from the Mount of Yahweh three days’ journey, the ark "
         "going before them to seek out a resting place for them."),
    Span("Num 11:19-20", "a whole month", 30, None, "kibroth_hattaavah", "a whole month of quail",
         "“You will not eat one day, nor two days, nor five days, neither ten days, "
         "nor twenty days, but a whole month.” The place was called Kibroth "
         "Hattaavah (Numbers 11:34).",
         also="Num 11:34",
         note="Numbers 11:32 has them gathering quail all that day, all that night "
              "and all the next day."),
    Span("Num 12:14-15", "7 days", 7, None, "hazeroth", "Miriam shut out",
         "Miriam was shut up outside of the camp seven days, and the people didn’t "
         "travel until Miriam was brought in again.",
         also="Num 11:35; 12:16"),
    Span("Num 13:25", "40 days", 40, None, "kadesh", "forty days spying",
         "They returned from spying out the land at the end of forty days, to the "
         "wilderness of Paran, to Kadesh (Numbers 13:26); it was the time of the "
         "first-ripe grapes (13:20).",
         also="Num 13:20, 26"),
    Span("Num 14:33-34", "40 years", None, 40, "kadesh", "a year for each day",
         "After the number of the days in which you spied out the land, even forty "
         "days, for every day a year, you will bear your iniquities, even forty "
         "years.",
         note="The forty years are the whole count from the exodus, which already "
              "includes the year and more before Kadesh."),
    Span("Exod 16:35", "40 years", None, 40, None, "manna forty years",
         "The children of Israel ate the manna forty years, until they came to the "
         "borders of the land of Canaan; it ceased at Gilgal (Joshua 5:12).",
         start=(1, 2, 16), end=(41, 1, 16), also="Exod 16:13-15; Josh 5:12",
         note="It began in the wilderness of Sin, after the fifteenth day of the "
              "second month (Exodus 16:1, 13-15); the exact day is not given."),
    Span("Josh 5:6", "40 years", None, 40, None, "forty years in the wilderness",
         "The children of Israel walked forty years in the wilderness, until all the "
         "men of war who came out of Egypt were consumed.",
         start=(1, 1, 15), end=(41, 1, 10), also="Num 14:33; 32:13; Deut 2:7",
         note="Drawn from leaving Rameses to coming up out of the Jordan: forty years "
              "less five days."),
    Span("Num 20:29", "30 days", 30, None, "mount_hor", "mourning for Aaron",
         "When all the congregation saw that Aaron was dead, they wept for Aaron "
         "thirty days, even all the house of Israel.",
         start=(40, 5, 1), end=(40, 6, 1), placed=True,
         note="It starts on the day Aaron died (Numbers 33:38)."),
    Span("Deut 1:2", "11 days", 11, None, None, "Horeb to Kadesh Barnea",
         "It is eleven days’ journey from Horeb by the way of Mount Seir to Kadesh "
         "Barnea.",
         note="A distance in days of travel, not the time Israel took."),
    Span("Deut 1:46", "many days", None, None, "kadesh", "many days at Kadesh",
         "So you stayed in Kadesh many days, according to the days that you "
         "remained.",
         note="The text gives no number."),
    Span("Deut 2:1", "many days", None, None, None, "around Mount Seir",
         "We turned and took our journey into the wilderness by the way to the Red "
         "Sea, and encircled Mount Seir many days.",
         note="The text gives no number; it falls inside the thirty-eight years of "
              "Deuteronomy 2:14."),
    Span("Deut 2:14", "38 years", None, 38, "kadesh", "thirty-eight years",
         "The days from Kadesh Barnea until we had come over the brook Zered were "
         "thirty-eight years, until all the generation of the men of war were "
         "consumed.",
         also="Deut 2:13; Num 21:12", to="brook Zered",
         note="Neither end is dated: they left Kadesh Barnea after the spies came "
              "back, in the second year or later, and crossed the Zered after "
              "Aaron’s death in the fifth month of the fortieth year (Numbers "
              "21:4-12). Its ends are drawn dashed."),
    Span("Deut 34:8", "30 days", 30, None, "plains_of_moab", "mourning for Moses",
         "The children of Israel wept for Moses in the plains of Moab thirty days, "
         "until the days of weeping in the mourning for Moses were ended."),
    Span("Josh 3:2", "3 days", 3, None, "plains_of_moab", "three days by the Jordan",
         "They moved from Shittim and came to the Jordan, and camped there before "
         "they crossed over; after three days the officers went through the middle "
         "of the camp.",
         also="Josh 3:1; 1:11",
         note="How these three days and the three of Joshua 1:11 relate is not "
              "said."),
]

# What the year count is, and the stretch between the years the text dates,
# for the strip's bands
YEARS = {
    "count": ("Exod 12:2; 40:17; Num 1:1; 33:38",
              "The text counts years “after they had come out of the land of "
              "Egypt”: the second year (Exodus 40:17) is the year after the "
              "exodus year, so the exodus year is year 1, and Numbers 33:38’s "
              "“fortieth year” is year 40. Each year is drawn from its first "
              "month (Exodus 12:2), twelve months of thirty days; the text doesn’t "
              "say when the year number changes."),
    "between": ("Num 15-19; Deut 1:46; 2:1, 14",
                "Between the second year and the fortieth the text gives no date. "
                "They stayed in Kadesh “many days” (Deuteronomy 1:46) and "
                "encircled Mount Seir “many days” (2:1), inside the "
                "thirty-eight years from Kadesh Barnea to the brook Zered (2:14). "
                "Numbers 15-19 (the laws, Korah, Aaron’s rod) are told without a "
                "date or a camp. Numbers 33:18-35, the camps from Rithmah to Ezion "
                "Geber, fill these years; the list never names the first stay at "
                "Kadesh."),
    "forty": ("Josh 4:19; 5:6; Deut 1:3",
              "Joshua gives no year. The first month after Deuteronomy 1:3 (the "
              "eleventh month of the fortieth year) is year 41 in this count: the "
              "end of the forty years, forty years less five days after they left "
              "Rameses, not a forty-first year of wandering."),
    "plains": ("Deut 1:3; 34:5-8; Josh 3:2; 4:19",
               "From Deuteronomy 1:3 (the first day of the eleventh month of year "
               "40) to Joshua 4:19 (the tenth day of the first month) is about 69 "
               "days. Inside them fall Moses’ death, thirty days of mourning and "
               "three days by the Jordan; their order and overlaps are not stated."),
}


# ===========================================================================
# The other itineraries
# ===========================================================================

VARIANTS = [
    Variant("numbers21", "Numbers 21", "Num 21:4-20",
            ("Mount Hor", "Oboth", "Iyeabarim", "the valley of Zered",
             "the other side of the Arnon", "Beer", "Mattanah", "Nahaliel", "Bamoth",
             "the valley that is in the field of Moab", "the top of Pisgah"),
            "The narrative leaves Mount Hor “by the way to the Red Sea, to go around "
            "the land of Edom” (21:4), tells of the bronze serpent (21:5-9), and then "
            "names Oboth (21:10). It has no Zalmonah or Punon. After Iyeabarim it runs "
            "the valley of Zered, the far side of the Arnon, Beer (the well), "
            "Mattanah, Nahaliel and Bamoth to the top of Pisgah (21:12-20), where "
            "Numbers 33 has Dibon Gad, Almon Diblathaim and the mountains of Abarim "
            "before Nebo; only Oboth and Iye Abarim are in both. The camp in the "
            "plains of Moab follows at 22:1."),
    Variant("deuteronomy10", "Deuteronomy 10", "Deut 10:6-7",
            ("Beeroth Bene Jaakan", "Moserah", "Gudgodah", "Jotbathah"),
            "Numbers 33:30-33 runs Moseroth, Bene Jaakan, Hor Haggidgad, Jotbathah; "
            "Deuteronomy runs Beeroth Bene Jaakan to Moserah, then Gudgodah and "
            "Jotbathah, so the first two are the other way round. Deuteronomy says "
            "Aaron died and was buried at Moserah (10:6), where Numbers puts his death "
            "on Mount Hor, several camps later and after Kadesh and Ezion Geber "
            "(Numbers 20:22-29; 33:37-39)."),
    Variant("deuteronomy2", "Deuteronomy 2", "Deut 2:1-37",
            ("the Red Sea", "Mount Seir", "Elath", "Ezion Geber", "the wilderness of Moab",
             "the brook Zered", "Ar", "the valley of the Arnon",
             "the wilderness of Kedemoth", "Jahaz", "Aroer"),
            "From Kadesh, where they stayed many days (1:46), they turned “by the way "
            "to the Red Sea” and encircled Mount Seir many days (2:1), then turned "
            "north (2:3), passing Esau’s children by the way of the Arabah from Elath "
            "and Ezion Geber (2:8), and went by the wilderness of Moab. They crossed "
            "the brook Zered thirty-eight years after leaving Kadesh Barnea (2:13-14), "
            "passed Ar, the border of Moab (2:18), crossed the Arnon (2:24), sent to "
            "Sihon from the wilderness of Kedemoth (2:26) and fought him at Jahaz "
            "(2:32). It names no camps, and it passes Ezion Geber going north, where "
            "Numbers 33 goes from Ezion Geber to Kadesh (33:36)."),
    Variant("judges11", "Judges 11", "Judg 11:16-18",
            ("the Red Sea", "Kadesh", "the other side of the Arnon"),
            "Jephthah’s summary: through the wilderness to the Red Sea, to Kadesh, "
            "where they stayed after Edom and Moab refused them passage; then round "
            "Edom and Moab by Moab’s east side, to camp beyond the Arnon, and so to "
            "fight Sihon at Jahaz (11:20)."),
]


# ===========================================================================
# The lands and waters, named in the WEB's words
# ===========================================================================

# Where the page writes a land's name, chosen by hand: no border is drawn.
REGIONS = {
    "egypt": Region("Egypt", 29.55, 31.62, r"\bEgypt\b"),
    "goshen": Region("Goshen", 30.62, 31.55, r"\bGoshen\b",
                     note="The land of Goshen, in the eastern delta, where Israel lived "
                          "(Genesis 47:27)."),
    "shur": Region("Wilderness of Shur", 30.55, 33.20, r"\bwilderness of Shur\b|\bShur\b",
                   note="Exodus 15:22 calls the three days after the sea the wilderness of "
                        "Shur; Numbers 33:8 calls them the wilderness of Etham."),
    "etham": Region("Wilderness of Etham", 29.80, 33.05, r"\bwilderness of Etham\b",
                    note="Numbers 33:8’s name for the three days after the sea."),
    "sin": Region("Wilderness of Sin", 29.22, 33.42, r"\bwilderness of Sin\b",
                  note="“Between Elim and Sinai” (Exodus 16:1); where it lies depends "
                       "on where Sinai is."),
    "sinai": Region("Wilderness of Sinai", 28.08, 33.98, r"\bwilderness of Sinai\b",
                    note="The wilderness before the mountain (Exodus 19:1-2)."),
    "paran": Region("Wilderness of Paran", 29.85, 34.15, r"\bParan\b",
                    note="Where the cloud rested after Hazeroth (Numbers 10:12; 12:16), and "
                         "from which the spies were sent (13:3). Its bounds are not "
                         "given."),
    "zin": Region("Wilderness of Zin", 30.90, 34.85, r"\bwilderness of Zin\b",
                  note="Kadesh’s wilderness (Numbers 20:1; 33:36), on the land’s "
                       "southern border (34:3)."),
    "edom": Region("Edom", 30.40, 35.78, r"\bEdom\b", skip=_GZ.REGIONS["edom"].skip,
                   aka=("Seir", "Mount Seir"),
                   note="Esau’s land, east of the Arabah, which refused Israel passage "
                        "(Numbers 20:14-21)."),
    "moab": Region("Moab", 31.20, 36.05, r"\bMoab\b", skip=_GZ.REGIONS["moab"].skip,
                   note="The tableland east of the Salt Sea; the plains of Moab are its "
                        "Jordan valley."),
    "midian": Region("Midian", 28.15, 35.55, r"\bMidian\b",
                     note="Where Moses kept Jethro’s flock (Exodus 3:1), east of the "
                          "Gulf of Aqaba as most place it."),
    "canaan": Region("Canaan", 31.55, 35.00, r"\bland of Canaan\b",
                     note="The land Israel was going to (Numbers 33:51)."),
}


# ===========================================================================
# The line between the camps (ours)
# ===========================================================================

# Between two camps with sites, the line runs through these points of ours
# ("~"), placed to keep it on land and off the lakes, along the coast or the
# valley where the traditional route runs, and over the Zered and the Arnon
# where Numbers 21 and Deuteronomy 2 cross them. A camp with no site is
# drawn on this line in its order, spaced evenly between its neighbours.
ROUTE_VIA = {
    ("succoth", "crossing"): [
        (30.3000, 32.2200),   # ~ west of the Bitter Lakes, past Fayed
        (30.0600, 32.3800),   # ~ the plain north-west of Suez
    ],
    ("elim", "dophkah"): [
        (29.0600, 33.1500),   # ~ inland of Ras Abu Zanimah, the shore road
        (28.9300, 33.2400),   # ~ the coastal plain of el-Markha
    ],
    ("hazeroth", "abronah"): [
        (29.1500, 34.5200),   # ~ the uplands west of Nuweiba
        (29.4500, 34.6800),   # ~ the uplands west of Taba
        (29.6200, 34.9000),   # ~ the edge of the Arabah, north-west of Eilat
    ],
    ("ezion_geber", "kadesh"): [
        (29.7280, 34.8580),   # ~ so the line back north crosses the way down between Hor Haggidgad and Jotbathah, clear of both
    ],
    ("punon", "dibon_gad"): [
        (30.8300, 35.6600),   # ~ up from the Arabah toward the Zered
        # the Zered crossing, as gazetteer.ZERED
        (30.9441, 35.7791),   # Confluence of Wadi 'Anmayn (Q35305936)
        # the Arnon crossing, as gazetteer.ARNON
        (31.4403, 35.8217),   # Mujib Reservoir (Q16895507)
    ],
}

# Where the text puts camps with no site before a point of the line: the
# via point (its place in ROUTE_VIA's list) and the last camp before it.
# Numbers 21:11-12 encamps at Iyeabarim, then in the valley of Zered, so
# Oboth and Iye Abarim are spaced between Punon and the Zered.
ROUTE_BREAKS = {
    ("punon", "dibon_gad"): (1, "iye_abarim"),
}

# The narrative's own verses for a move from one camp to the next, beside
# Numbers 33's (Deuteronomy 10 runs Beeroth Bene Jaakan to Moserah, the
# other way round)
LEG_REFS = {
    ("rameses", "succoth"): "Exod 12:37",
    ("succoth", "etham"): "Exod 13:20",
    ("etham", "pihahiroth"): "Exod 14:2",
    ("pihahiroth", "marah"): "Exod 15:22-23",
    ("marah", "elim"): "Exod 15:27",
    ("red_sea_camp", "wilderness_of_sin"): "Exod 16:1",
    ("alush", "rephidim"): "Exod 17:1",
    ("rephidim", "wilderness_of_sinai"): "Exod 19:2",
    ("wilderness_of_sinai", "kibroth_hattaavah"): "Num 10:12, 33",
    ("kibroth_hattaavah", "hazeroth"): "Num 11:35",
    ("hazeroth", "rithmah"): "Num 12:16",
    ("moseroth", "bene_jaakan"): "Deut 10:6",
    ("hor_haggidgad", "jotbathah"): "Deut 10:7",
    ("ezion_geber", "kadesh"): "Num 20:1",
    ("kadesh", "mount_hor"): "Num 20:22",
    ("mount_hor", "zalmonah"): "Num 21:4",
    ("punon", "oboth"): "Num 21:10",
    ("oboth", "iye_abarim"): "Num 21:11",
    ("mountains_of_abarim", "plains_of_moab"): "Num 22:1",
}

# The traditional crossing, drawn as a span over the water from shore to
# shore: Suez Bay's west shore under Jebel Ataqa, south of Clysma, to the
# Sinai shore at 'Uyun Musa. Both are points of sinai.py's shores.
CROSSING_SPAN = [
    (29.8964, 32.4644),   # Mina' 'Ataqah, Ataqa port, of SUEZ_WEST_SHORE (Q23954920)
    (29.8350, 32.6336),   # Mousa Coast Resort, of SINAI_WEST_SHORE (Q111999178)
]


# ===========================================================================
# Checks
# ===========================================================================

def _numbers33():
    path = os.path.join(BIBLES_DIR, "WEB", "Numbers_33.json")
    with open(path, encoding="utf-8") as f:
        return {int(n): t for n, t in json.load(f)["verses"]}


def num33_verses(station):
    """The verse numbers of a station's Numbers 33 ref."""
    out = []
    for part in station.num33.replace("Num 33:", "").split(","):
        a, _, b = part.strip().partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return out


def misspelled():
    """The stations whose name, as the page writes it, isn't spelled so in
    any of their Numbers 33 verses (a name that starts a phrase, "the
    wilderness of Sinai", is matched as it stands)."""
    text = _numbers33()
    out = []
    for s in STATIONS + list(ENDS.values()):
        vs = " ".join(text[v] for v in num33_verses(s))
        if not re.search(r"\b%s\b" % re.escape(s.name), vs):
            out.append(s.key)
    return out
