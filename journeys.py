"""Paul's journeys in (lat, lon): the places Acts and the letters name, the
four journeys stop by stop with their verses, the roads and sea courses
between, the lands, the letters and the seven assemblies of Revelation 2-3.
For the Paul's journeys reference page (generate_journeys_reference.py),
drawn on mediterranean.py's coasts with acts_geography's and gazetteer's.

How it was made (gathered 2026-10-28, checked by script). A place's point is
its Wikidata item's own P625 (`qid`), and each of its `refs` is a verse that
names it, as in gazetteer. A road's points are named places on or by it,
each its own Wikidata coordinate, with `why` saying how sure the line is;
acts_geography's roads of Acts 13-14 are used as they are. A sea course's
points are our own ("~"): where Acts says the ship passed (under the lee of
Cyprus, through the strait off Chios) or where the sea leaves only one way
past an island or cape, nothing more.

- **PLACES** are keyed as the page's ids are. `certainty` is KNOWN,
  PROBABLE or POSSIBLE, as in gazetteer, with `why`; `roles` say what the
  place is on the page (a stop on a journey, a letter's recipient or where
  one was written, one of Revelation's assemblies); `letters` says which,
  with the verses. `search` is False where a place's name is another's too
  (two Antiochs), so only its `refs` are its verses; `skip` lists verses its
  names find that are about something else.
- **JOURNEYS** run stop by stop. A stop's `by` is how Acts has them get
  there (land or sea); `certain` is False where the stop is inferred, or
  where the text doesn't give the way and the line is ours, and `note` says
  what the text says. `via` names the
  road or sea course the leg follows (none: a straight line). A stop's
  `at` is where the line goes when the ship only passed the place.
- **REGIONS** are the lands Acts and the letters name, with where the page
  writes each name, chosen by hand: no border is drawn.
"""

from typing import NamedTuple

import acts_geography as G

KNOWN, PROBABLE, POSSIBLE = "known", "probable", "possible"


class Place(NamedTuple):
    name: str
    lat: float
    lon: float
    qid: str
    certainty: str
    modern: str = ""
    why: str = ""
    aka: tuple = ()
    region: str = ""
    refs: str = ""
    roles: tuple = ()
    letters: str = ""
    note: str = ""
    point: str = ""              # what the point is, where it isn't the item's own
    source: str = ""             # how the point was chosen, for the record
    search: bool = True          # whether its names find its verses
    skip: str = ""               # verses its names find that are about something else


class Stop(NamedTuple):
    place: str                   # a PLACES key, or a REGIONS key (no town named)
    ref: str
    by: str                      # "start", "land" or "sea"
    certain: bool = True
    note: str = ""
    via: str = ""                # a ROADS or COURSES key
    at: tuple = ()               # where the line goes, for a place only passed


class Journey(NamedTuple):
    name: str
    refs: str
    stops: list


class Road(NamedTuple):
    name: str
    points: list
    why: str = ""


class Region(NamedTuple):
    name: str
    lat: float
    lon: float
    find: str = ""
    aka: tuple = ()
    note: str = ""


class Letter(NamedTuple):
    name: str                    # the book, as books.BOOK_NAMES has it
    to: tuple                    # PLACES or REGIONS keys
    to_ref: str
    written: str = ""            # a PLACES key, only where the letter says so
    written_ref: str = ""
    note: str = ""


# ===========================================================================
# Places
# ===========================================================================

PLACES = {
    "damascus": Place(
        "Damascus", 33.5111, 36.3064, "Q3678596", KNOWN,
        modern="Old walled city of Damascus, Syria",
        why="The name and occupation are continuous, and the Roman grid (the street called Straight, Acts 9:11) survives in the old city.",
        aka=("Dimashq", "Ancient City of Damascus"),
        region="Syria; held by King Aretas's governor (2 Cor 11:32)",
        refs="Acts 9:2-3, 8, 10, 19, 22, 27; 22:5-6, 10-12; 26:12, 20; 2 Cor 11:32; Gal 1:17",
        roles=("other_acts",),
        note="Conversion on the road (9:3); let down the wall in a basket (9:25; 2 Cor 11:32-33); returned there from Arabia (Gal 1:17).",
        source="Same point as gazetteer.py.",
    ),
    "jerusalem": Place(
        "Jerusalem", 31.7767, 35.2342, "Q213274", KNOWN,
        modern="Old City of Jerusalem",
        why="Continuous name and occupation.",
        aka=("Old City of Jerusalem",),
        region="Judea (Acts 26:20; 28:21)",
        refs="Acts 9:2, 13, 21, 26, 28; 12:25; 13:13, 27, 31; 15:2, 4; 16:4; 18:21; 19:21; 20:16, 22; 21:4, 11-13, 15, 17, 31; 22:5, 17-18; 23:11; 24:11; 25:1, 3, 7, 9, 15, 20, 24; 26:4, 10, 20; 28:17; Rom 15:19, 25-26, 31; 1 Cor 16:3; Gal 1:17-18; 2:1",
        roles=("other_acts", "journey2", "journey3"),
        note="First visit 9:26-29; famine visit 12:25; council 15:2-4. The end of journey 2 is only implied (18:22 says he went up and greeted the assembly). Journey 3 ends here (21:15-17) with the arrest (21:31-33) that leads to Rome.",
        source="Same point as gazetteer.py (Wikidata 31.77667, 35.23417).",
    ),
    "caesarea": Place(
        "Caesarea", 32.5011, 34.8923, "Q319242", KNOWN,
        modern="Caesarea National Park, Israel",
        why="The name never changed; Herod's harbour city is excavated (Pilate inscription).",
        aka=("Caesarea Maritima", "Qaisariyye"),
        region="Judea (the Sharon coast)",
        refs="Acts 9:30; 18:22; 21:8, 16; 23:23, 33; 25:1, 4, 6, 13",
        roles=("other_acts", "journey2", "journey3", "rome"),
        skip="Matt 16:13; Mark 8:27",
        note="Sent off from here to Tarsus (9:30); landed here at the end of journey 2 (18:22); stayed with Philip on journey 3 (21:8); held two years (24:27). The voyage to Italy starts from here, implied in 27:1-2.",
        source="Same point as gazetteer.py.",
    ),
    "antipatris": Place(
        "Antipatris", 32.105, 34.9304, "Q682612", KNOWN,
        modern="Tel Afek at the Yarkon springs, Rosh HaAyin, Israel",
        why="Herod's city at the Yarkon springs is certain (Josephus; excavations).",
        aka=("Tel Afek", "Aphek", "Ras el-Ain"),
        region="Judea (Sharon)",
        refs="Acts 23:31",
        roles=("other_acts",),
        note="Night stage of the escort from Jerusalem to Caesarea (23:31-33).",
        source="Same point as gazetteer.py's Aphek.",
    ),
    "tarsus": Place(
        "Tarsus", 36.91667, 34.9, "Q134287", KNOWN,
        modern="Tarsus, Mersin, Turkey",
        why="Continuous name and city; the Roman city (paved street, Gozlukule mound) lies under the modern town.",
        aka=("Tarsus in Cilicia",),
        region="Cilicia (Acts 21:39; 22:3)",
        refs="Acts 9:11, 30; 11:25; 21:39; 22:3",
        roles=("other_acts",),
        note="Paul's home city. The coordinate is the town item's and is precise only to the minute. Journey 2 crosses Cilicia (15:41) without naming the city.",
        source="Wikidata's ancient-Tarsus item Q141221694 has no coordinate. Alternatives are the Gozlukule tell (Q5626760, 36.91278, 34.89444) and Saint Paul's Well (Q105944717).",
    ),
    "antioch_syria": Place(
        "Antioch", 36.20472, 36.18167, "Q200441", KNOWN,
        modern="Antakya, Hatay, Turkey",
        why="Continuous city (Antakya) on the Orontes; Seleucid and Roman capital of Syria.",
        aka=("Antioch of Syria", "Antioch on the Orontes", "Antakya"),
        region="Syria (Acts 15:23)",
        refs="Acts 6:5; 11:19-20, 22, 26-27; 13:1; 14:26; 15:22-23, 30, 35; 18:22; Gal 2:11",
        roles=("journey1", "journey2", "journey3", "other_acts"),
        search=False,
        note="Barnabas brings Saul here (11:25-26). It is the home base where journeys 1 and 2 start and end and journey 3 starts (13:1-3; 14:26; 15:35-40; 18:22-23). Antioch in Acts 13:14, 14:19, 14:21 and 2 Tim 3:11 is Pisidian Antioch.",
        source="Wikidata also carries 36.2, 36.15.",
    ),
    "seleucia": Place(
        "Seleucia", 36.12445, 35.92119, "Q1605894", KNOWN,
        modern="Cevlik, near Samandag, Hatay, Turkey",
        why="Antioch's harbour; ruins and the Titus tunnel at Cevlik.",
        aka=("Seleucia Pieria",),
        region="Syria",
        refs="Acts 13:4",
        roles=("journey1",),
        note="Port of embarkation for Cyprus.",
    ),
    "salamis": Place(
        "Salamis", 35.1751, 33.90359, "Q767089", KNOWN,
        modern="Ruins north of Famagusta, Cyprus",
        why="Excavated city with continuous identification.",
        aka=("Salamis in Cyprus",),
        region="Cyprus (Acts 13:4)",
        refs="Acts 13:5",
        roles=("journey1",),
        note="Landing on Cyprus; preaching in the synagogues.",
        source="Do not confuse it with the Salamis in Attica (Q28721684).",
    ),
    "paphos": Place(
        "Paphos", 34.75567, 32.40417, "Q12065255", KNOWN,
        modern="Paphos Archaeological Park, Kato Paphos, Cyprus",
        why="New Paphos was the Roman capital of Cyprus and seat of the proconsul (Sergius Paulus, 13:7); excavated.",
        aka=("Nea Paphos", "New Paphos", "Kato Paphos"),
        region="Cyprus",
        refs="Acts 13:6, 13",
        roles=("journey1",),
        source="This is not Old Paphos (Palaipaphos, Kouklia; Q55339028 at 34.70778, 32.5735), about 16 km to the south-east. The town item Q180918 is the modern town.",
    ),
    "perga": Place(
        "Perga", 36.96223, 30.85507, "Q719815", KNOWN,
        modern="Perge ruins at Aksu, near Antalya, Turkey",
        why="Excavated city; name preserved.",
        aka=("Perge",),
        region="Pamphylia (Acts 13:13)",
        refs="Acts 13:13-14; 14:25",
        roles=("journey1",),
        note="John Mark leaves the party here (13:13); on the way back they preach here (14:25).",
    ),
    "attalia": Place(
        "Attalia", 36.8939, 30.7003, "Q105703706", KNOWN,
        modern="Kaleici harbour, Antalya, Turkey",
        why="Continuous city and harbour (Antalya).",
        aka=("Attaleia", "Antalya"),
        region="Pamphylia (Acts 14:24-25)",
        refs="Acts 14:25",
        roles=("journey1",),
        note="They sail from here back to Antioch (14:26).",
    ),
    "antioch_pisidia": Place(
        "Antioch of Pisidia", 38.30611, 31.18917, "Q579468", KNOWN,
        modern="Ruins near Yalvac, Isparta, Turkey",
        why="Roman colony identified by inscriptions; excavated.",
        aka=("Antioch", "Pisidian Antioch", "Antiochia Caesareia"),
        region="Pisidia (Acts 13:14; 14:24); in the province of Galatia",
        refs="Acts 13:14; 14:19, 21; 2 Tim 3:11",
        roles=("journey1",),
        search=False,
        note="Synagogue sermon (13:16-41). The WEB calls it simply Antioch in 14:19, 14:21 and 2 Tim 3:11. Journey 2 probably passes nearby (16:6) but doesn't name it.",
    ),
    "iconium": Place(
        "Iconium", 37.87194, 32.49222, "Q132559332", KNOWN,
        modern="Konya (Alaeddin hill), Turkey",
        why="Continuous name (Konya); the ancient mound is Alaeddin hill.",
        aka=("Konya",),
        region="Province of Galatia; Acts 14:6 treats it as outside Lycaonia",
        refs="Acts 13:51; 14:1, 19, 21; 16:2; 2 Tim 3:11",
        roles=("journey1", "journey2"),
        source="Q132559332 is the item for Konya in Roman times; the city item is Q79857.",
    ),
    "lystra": Place(
        "Lystra", 37.6019, 32.3383, "Q535982", KNOWN,
        modern="Zoldera mound near Hatunsaray, Konya, Turkey",
        why="In 1885 Sterrett found the colony's Latin dedication naming Lystra on the site.",
        aka=("Zoldera",),
        region="Lycaonia (Acts 14:6)",
        refs="Acts 14:6, 8, 21; 16:1-2; 2 Tim 3:11",
        roles=("journey1", "journey2"),
        note="Paul is hailed as Mercury and then stoned here (14:12, 19). Timothy's home (16:1).",
        point="the Zoldera mound, by Wikipedia's coordinate",
        source="Wikidata's Lystra item gives 37.66412, 32.21071, about 13 km north-west of Zoldera; the point is Wikipedia's for Zoldera, as acts_geography has it.",
    ),
    "derbe": Place(
        "Derbe", 37.34857, 33.36145, "Q20717624", PROBABLE,
        modern="Kerti Hoyuk, north-east of Karaman, Turkey",
        why="A dedication naming Derbe, found in 1956, points to Kerti Hoyuk. The rival is Devri Sehri, a few km to the south-east, backed by a later inscription. Ramsay's older choice, Gudelisin, is abandoned.",
        aka=("Kerti Hoyuk",),
        region="Lycaonia (Acts 14:6)",
        refs="Acts 14:6, 20; 16:1; 20:4",
        roles=("journey1", "journey2"),
        note="Gaius of Derbe: 20:4.",
        source="Wikidata's item also carries a second point (37.43889, 33.16389), which is unexplained. The tell has its own item, Q134960294 (37.3492, 33.3617).",
    ),
    "troas": Place(
        "Troas", 39.75194, 26.15861, "Q1393407", KNOWN,
        modern="Dalyan, near Ezine, Canakkale, Turkey",
        why="Roman colony Alexandria Troas; ruins on the coast. It is not Troy.",
        aka=("Alexandria Troas",),
        region="Asia (Mysia, Acts 16:8)",
        refs="Acts 16:8, 11; 20:5-6; 2 Cor 2:12; 2 Tim 4:13",
        roles=("journey2", "journey3"),
        note="Here Paul has the vision of the man of Macedonia (16:9), Eutychus falls (20:9-12), and the cloak is left with Carpus (2 Tim 4:13).",
        source="Wikidata also carries 39.76128, 26.15255.",
    ),
    "samothrace": Place(
        "Samothrace", 40.50139, 25.5325, "Q123706384", KNOWN,
        modern="Palaiopolis on Samothraki island, Greece",
        why="The island is certain; the point is the ancient city and harbour on its north coast, the natural overnight anchorage.",
        aka=("Samothraki", "Palaiopolis"),
        region="North Aegean (Thrace); not named in the WEB",
        refs="Acts 16:11",
        roles=("journey2",),
        source="The island item is Q203175 (40.45, 25.5875).",
    ),
    "neapolis": Place(
        "Neapolis", 40.93361, 24.41306, "Q6984309", KNOWN,
        modern="Kavala, Greece",
        why="Port of Philippi on the Via Egnatia; continuous town (Kavala).",
        aka=("Kavala",),
        region="Macedonia",
        refs="Acts 16:11",
        roles=("journey2",),
        note="The return sailing in Acts 20:6 (from Philippi) used this port too, but the verse doesn't name it.",
    ),
    "philippi": Place(
        "Philippi", 41.01306, 24.28639, "Q379652", KNOWN,
        modern="Ruins near Krinides, Kavala, Greece",
        why="Excavated Roman colony; name preserved.",
        aka=("Filippoi",),
        region="Macedonia (Acts 16:12)",
        refs="Acts 16:12; 20:6; Phil 1:1; 1 Thess 2:2",
        skip="Matt 16:13; Mark 8:27",
        roles=("journey2", "journey3", "letter_to"),
        letters="Philippians addressed to the saints at Philippi (Phil 1:1)",
        note="Lydia and the jailer (16:14-34). Philippians is written in bonds (Phil 1:7, 13) but doesn't name the city it was written from.",
    ),
    "amphipolis": Place(
        "Amphipolis", 40.82377, 23.84777, "Q217414", KNOWN,
        modern="Ruins at Amfipoli, Serres, Greece",
        why="Excavated city on the Strymon; name preserved.",
        region="Macedonia",
        refs="Acts 17:1",
        roles=("journey2",),
        note="Passed through on the Via Egnatia.",
    ),
    "apollonia": Place(
        "Apollonia", 40.64157, 23.4874, "Q2751389", PROBABLE,
        modern="Near Nea Apollonia, south of Lake Volvi, Greece",
        why="The Via Egnatia station south of Lake Bolbe is fixed by the itineraries, but the town is unexcavated and the exact spot is uncertain.",
        aka=("Apollonia of Mygdonia",),
        region="Macedonia",
        refs="Acts 17:1",
        roles=("journey2",),
        source="Wikidata gives two points (also 40.62217, 23.46767). Do not confuse it with Apollonia in Illyria (Q505703) or the Apollonia of Chalcidice.",
    ),
    "thessalonica": Place(
        "Thessalonica", 40.63777, 22.94577, "Q16932289", KNOWN,
        modern="Thessaloniki, Greece (Roman Agora)",
        why="Continuous city; the point is its Roman forum.",
        aka=("Thessalonians", "Thessaloniki", "Salonica"),
        region="Macedonia",
        refs="Acts 17:1, 11, 13; 20:4; 27:2; Phil 4:16; 1 Thess 1:1; 2 Thess 1:1; 2 Tim 4:10",
        roles=("journey2", "letter_to"),
        letters="1 and 2 Thessalonians addressed to the assembly of the Thessalonians (1 Thess 1:1; 2 Thess 1:1)",
        note="Aristarchus of Thessalonica sails with Paul (27:2).",
        source="The city item is Q17151 (40.64028, 22.93556).",
    ),
    "beroea": Place(
        "Beroea", 40.5258, 22.2046, "Q15712213", KNOWN,
        modern="Veria, Greece",
        why="Continuous city (Veria).",
        aka=("Berea", "Veria", "Beroia"),
        region="Macedonia",
        refs="Acts 17:10, 13; 20:4",
        roles=("journey2",),
        note="The WEB spells it Beroea, not Berea. Sopater of Beroea: 20:4.",
        source="Wikidata also carries 40.51667, 22.2.",
    ),
    "athens": Place(
        "Athens", 37.975, 23.7225, "Q395367", KNOWN,
        modern="Ancient Agora of Athens, Greece",
        why="Continuous city; the point is the agora, where Paul reasoned daily (17:17), below the Areopagus (17:19, 22).",
        aka=("Areopagus", "Agora of Athens"),
        region="Achaia",
        refs="Acts 17:15-16, 22; 18:1; 1 Thess 3:1",
        roles=("journey2",),
        note="In 1 Thess 3:1 Paul recalls being left behind at Athens alone.",
        source="The city item is Q1524; the Areopagus is Q202487 (37.97222, 23.72361).",
    ),
    "corinth": Place(
        "Corinth", 37.90579, 22.87874, "Q1363688", KNOWN,
        modern="Archaia Korinthos, Greece",
        why="Excavated Roman colony beneath Acrocorinth (Gallio inscription at Delphi dates the stay).",
        aka=("Ancient Corinth",),
        region="Achaia (Acts 18:12)",
        refs="Acts 18:1; 19:1; 1 Cor 1:2; 2 Cor 1:1, 23; 2 Tim 4:20",
        roles=("journey2", "letter_to"),
        letters="1 and 2 Corinthians addressed to the assembly of God at Corinth (1 Cor 1:2; 2 Cor 1:1). Romans is usually placed here (Phoebe of Cenchreae, Rom 16:1; Erastus the city treasurer, Rom 16:23, with 2 Tim 4:20), but the letter does not name the city.",
        note="Paul stays 18 months (18:11). The three months in Greece on journey 3 (20:2-3) are generally Corinth, but the WEB says only Greece.",
        source="Modern Corinth (Q103011) is a different site on the coast.",
    ),
    "cenchreae": Place(
        "Cenchreae", 37.8824, 22.9925, "Q111565756", KNOWN,
        modern="Kechries, Corinthia, Greece",
        why="Corinth's Saronic Gulf harbour; excavated harbour works at Kechries.",
        aka=("Kenchreai", "Kechries"),
        region="Achaia",
        refs="Acts 18:18; Rom 16:1",
        roles=("journey2",),
        letters="Romans commends Phoebe of the assembly at Cenchreae (Rom 16:1)",
        note="Paul shaves his head here for a vow (18:18).",
        source="Not the Argolid or Troad namesakes (Q16554749, Q60791302).",
    ),
    "ephesus": Place(
        "Ephesus", 37.93972, 27.34083, "Q47611", KNOWN,
        modern="Ruins near Selcuk, Izmir, Turkey",
        why="Excavated city; the theatre of Acts 19:29 stands.",
        aka=("Efes",),
        region="Asia",
        refs="Acts 18:19, 21, 24; 19:1, 17, 26, 35; 20:16-17; 1 Cor 15:32; 16:8; Eph 1:1; 1 Tim 1:3; 2 Tim 1:18; 4:12; Rev 1:11; 2:1",
        roles=("journey2", "journey3", "letter_to", "letter_from", "assembly_rev"),
        letters="1 Corinthians written from Ephesus (1 Cor 16:8; cf. 16:19). Ephesians addressed to the saints at Ephesus (Eph 1:1). 1 Timothy addressed to Timothy, left at Ephesus (1 Tim 1:3). The first of the seven letters (Rev 2:1).",
        note="Brief stop on journey 2 (18:19-21); two to three years on journey 3 (19:10; 20:31); sailed past (20:16), elders called to Miletus (20:17). The words at Ephesus in Eph 1:1 are missing from some early manuscripts; the WEB has them.",
        source="Wikidata also carries 37.94058, 27.33939.",
    ),
    "assos": Place(
        "Assos", 39.49056, 26.33667, "Q744631", KNOWN,
        modern="Behramkale, Canakkale, Turkey",
        why="Excavated city with its harbour below; name preserved.",
        aka=("Behramkale",),
        region="Asia (Troad)",
        refs="Acts 20:13-14",
        roles=("journey3",),
        note="Paul walks from Troas and boards the ship here.",
    ),
    "mitylene": Place(
        "Mitylene", 39.10481, 26.55237, "Q42295059", KNOWN,
        modern="Mytilene, Lesbos, Greece",
        why="Continuous city, chief town of Lesbos.",
        aka=("Mytilene", "Lesbos"),
        region="Asia (island of Lesbos, not named in the WEB)",
        refs="Acts 20:14",
        roles=("journey3",),
        note="The WEB spells it Mitylene.",
        source="Q42295059 is the ancient polis; the modern city is Q189059.",
    ),
    "chios": Place(
        "Chios", 38.4, 26.01667, "Q160483", KNOWN,
        modern="Chios island, Greece",
        why="The island is certain; the ship only came opposite it (20:15), presumably through the strait on its east side.",
        aka=("Khios",),
        region="Asia (Aegean island)",
        refs="Acts 20:15",
        roles=("journey3",),
        note="Passed by, not landed.",
        source="The point is the island's centre; the ancient city on the east coast is Q56399450 (38.37361, 26.13694), which may suit a sailing line better.",
    ),
    "samos": Place(
        "Samos", 37.69083, 26.93833, "Q13580795", KNOWN,
        modern="Pythagoreio, Samos, Greece",
        why="The ancient city and harbour of Samos, at Pythagoreio.",
        aka=("Pythagoreio",),
        region="Asia (Aegean island)",
        refs="Acts 20:15",
        roles=("journey3",),
        note="Touched at, not stayed.",
        source="The island item is Q156882. Wikidata also carries 37.68944, 26.94306.",
    ),
    "trogyllium": Place(
        "Trogyllium", 37.6594, 27.0033, "Q24934517", PROBABLE,
        modern="Tip of the Dilek (Mycale) peninsula, Aydin, Turkey, facing Samos",
        why="Strabo's Trogilium is the Mycale promontory across the strait from Samos, but the exact anchorage is unknown.",
        aka=("Trogilium", "Cape Mycale", "Dilek Peninsula"),
        region="Asia (Ionia)",
        refs="Acts 20:15",
        roles=("journey3",),
        point="Cape Mycale, the tip of the promontory",
        note="The WEB names it: 'and stayed at Trogyllium'. The clause is missing from the oldest manuscripts but present in the Majority Text that the WEB follows.",
        source="The Trogyllium item Q24934517 has no coordinate. The point is Cape Mycale's own (Mikale Burnu, Q2937072, a point of mediterranean.ASIA_WEST); the Dilek Peninsula item Q2663933 (37.66889, 27.16167) is the promontory's middle, 14 km inland.",
    ),
    "miletus": Place(
        "Miletus", 37.53023, 27.27837, "Q169460", KNOWN,
        modern="Ruins at Balat, Didim, Aydin, Turkey",
        why="Excavated city; its theatre and harbours are now silted inland.",
        aka=("Balat",),
        region="Asia",
        refs="Acts 20:15, 17; 2 Tim 4:20",
        roles=("journey3",),
        note="Farewell to the Ephesian elders (20:17-38); Trophimus left sick here (2 Tim 4:20).",
        source="Not the Mysian namesake (Q65074836).",
    ),
    "cos": Place(
        "Cos", 36.89333, 27.29028, "Q65238016", KNOWN,
        modern="Kos town, Kos, Greece",
        why="The ancient city of Kos, under and beside the modern town.",
        aka=("Kos",),
        region="Asia (Aegean island)",
        refs="Acts 21:1",
        roles=("journey3",),
        source="The island item is Q187027.",
    ),
    "rhodes": Place(
        "Rhodes", 36.44, 28.21111, "Q13533316", KNOWN,
        modern="Rhodes town, Rhodes, Greece",
        why="The ancient city at the island's north tip, under the modern town.",
        aka=("Rodos",),
        region="Asia (Aegean island)",
        refs="Acts 21:1",
        roles=("journey3",),
        source="The island item is Q43048. Wikidata also carries 36.43333, 28.21667.",
    ),
    "patara": Place(
        "Patara", 36.26028, 29.31417, "Q233121", KNOWN,
        modern="Patara ruins near Gelemis, Antalya, Turkey",
        why="Excavated Lycian harbour city; name preserved.",
        aka=("Gelemis",),
        region="Lycia (named in Acts 27:5)",
        refs="Acts 21:1",
        roles=("journey3",),
        note="They change here to a ship bound for Phoenicia (21:2).",
    ),
    "tyre": Place(
        "Tyre", 33.2667, 35.2, "Q82070", KNOWN,
        modern="Sur (Tyre), Lebanon",
        why="Continuous name (Sur).",
        aka=("Sur", "Tyros"),
        region="Syria (Acts 21:3); Phoenicia (21:2)",
        refs="Acts 21:3, 7",
        roles=("journey3",),
        note="Seven days with the disciples; prayer on the beach (21:4-5). Acts 12:20 names Tyre in a story without Paul.",
        source="Same point as gazetteer.py (the coordinate is the modern city's and only coarse).",
    ),
    "ptolemais": Place(
        "Ptolemais", 32.9211, 35.0883, "Q12412094", KNOWN,
        modern="Akko (Acre), Israel",
        why="Continuous name (Akko); renamed Ptolemais under the Ptolemies.",
        aka=("Acco", "Akko", "Acre"),
        region="Phoenicia / Syria",
        refs="Acts 21:7",
        roles=("journey3",),
        source="Same point as gazetteer.py's Acco. The point is gazetteer.py's Tel Akko tell. The Hellenistic and Roman city spread west of it into today's Old Acre (the Acre city item Q126084 is at 32.92611, 35.08389), so a coastal point may suit Paul's harbour better.",
    ),
    "sidon": Place(
        "Sidon", 33.5606, 35.3758, "Q163490", KNOWN,
        modern="Saida (Sidon), Lebanon",
        why="Continuous name (Saida).",
        aka=("Saida",),
        region="Phoenicia",
        refs="Acts 27:3",
        roles=("rome",),
        note="Julius lets Paul visit friends here. Acts 12:20 names Sidon in a story without Paul.",
        source="Same point as gazetteer.py.",
    ),
    "myra": Place(
        "Myra", 36.25917, 29.98528, "Q652024", KNOWN,
        modern="Demre, Antalya, Turkey",
        why="Excavated Lycian city (rock tombs, theatre); its harbour was Andriake, about 5 km away.",
        aka=("Demre", "Andriake"),
        region="Lycia (Acts 27:5)",
        refs="Acts 27:5",
        roles=("rome",),
        note="They change here to the Alexandrian grain ship (27:6).",
        source="Wikidata also carries 36.2508, 29.99364.",
    ),
    "cnidus": Place(
        "Cnidus", 36.68583, 27.375, "Q690575", KNOWN,
        modern="Knidos ruins at Tekir, tip of the Datca peninsula, Turkey",
        why="The Hellenistic and Roman city with its two harbours at Tekir. An earlier city may have stood at Burgaz near Datca, but by Paul's day Cnidus was at Tekir.",
        aka=("Knidos", "Tekir"),
        region="Asia (Caria; not named in the WEB)",
        refs="Acts 27:7",
        roles=("rome",),
        note="Came with difficulty opposite it; the wind kept them from going further, and they did not land.",
        source="Wikidata also carries 36.69017, 27.37164.",
    ),
    "salmone": Place(
        "Salmone", 35.31603, 26.31155, "Q2937111", PROBABLE,
        modern="Cape Sideros, north-east tip of Crete, Greece",
        why="The ancient Samonion/Salmonion promontory is usually Cape Sidero; a minority prefer a cape a little further south on Crete's east coast.",
        aka=("Cape Sidero", "Cape Sideros", "Samonium"),
        region="Crete (Acts 27:7)",
        refs="Acts 27:7",
        roles=("rome",),
        note="The ship passes opposite it into the lee of Crete.",
        source="Wikidata's other point is 35.31, 26.3. Q2214802 (Salmone in Elis) is unrelated.",
    ),
    "fair_havens": Place(
        "Fair Havens", 34.92969, 24.80031, "Q11818846", KNOWN,
        modern="Kaloi Limenes, south coast of Heraklion, Crete",
        why="The name survives as Kaloi Limenes, a bay on Crete's south coast just east of Cape Lithino.",
        aka=("Kaloi Limenes", "Kali Limenes"),
        region="Crete",
        refs="Acts 27:8",
        roles=("rome",),
        note="Paul warns against sailing on from here (27:9-10). Acts 27:12 calls it the haven. The item is the modern village and port.",
    ),
    "lasea": Place(
        "Lasea", 34.93986, 24.82153, "Q6492763", PROBABLE,
        modern="Ruins east of Kaloi Limenes, Crete",
        why="Ruins about 2 km east of Kaloi Limenes have been taken as Lasea since the 19th century. Manuscripts spell the name variously (Lasaea, Alassa, Thalassa).",
        aka=("Lasaea", "Lasaia"),
        region="Crete",
        refs="Acts 27:8",
        roles=("rome",),
        note="Named only as the city near Fair Havens.",
        source="Wikidata also carries 34.94083, 24.81827.",
    ),
    "phoenix": Place(
        "Phoenix", 35.1965, 24.07758, "Q2088586", PROBABLE,
        modern="Loutro / Phoinikas, near Chora Sfakion, Crete",
        why="The ancient Phoenix lies on the Mouros headland at Loutro. Scholars dispute whether the harbour is Loutro bay or Phineka bay on the west side of the headland, since the WEB says it looks northeast and southeast.",
        aka=("Phoinix", "Loutro", "Phineka"),
        region="Crete (Acts 27:12)",
        refs="Acts 27:12",
        roles=("rome",),
        note="Their goal, never reached: the Euroclydon drove them off (27:14-15).",
        source="A second Phoenix item, near Sellia (Q97341098), is a different town.",
    ),
    "clauda": Place(
        "Clauda", 34.83333, 24.08333, "Q213895", KNOWN,
        modern="Gavdos island, south of Crete, Greece",
        why="Name continuity (Kaudos, Gavdos), and its position in the storm's track fits.",
        aka=("Cauda", "Gavdos"),
        region="Crete (an island to its south)",
        refs="Acts 27:16",
        roles=("rome",),
        note="Under its lee they secure the boat and undergird the ship. The WEB spells it Clauda; many manuscripts have Cauda.",
    ),
    "malta": Place(
        "Malta", 35.9, 14.45, "Q193896", PROBABLE,
        modern="Malta (traditional landing at St Paul's Bay)",
        why="The traditional identification is Malta, with the wreck at St Paul's Bay or St Paul's Islands.",
        aka=("Melita", "Melite"),
        region="Not named; the ship is driven across the Adriatic Sea (27:27), which in antiquity meant the open central Mediterranean",
        refs="Acts 28:1",
        roles=("rome",),
        note="The WEB has Malta, not Melita. Three months here, and Publius (28:7-11).",
        source="The rivals are Mljet in the Adriatic (Melite Illyrica, Q211306), argued from the Adriatic Sea of 27:27, and Cephallenia (Kefalonia). The point is the island item (Wikidata also carries 35.88333, 14.45). The traditional bay is St Paul's Bay (Q39521, 35.94833, 14.40167), and the islets are Q755984 (35.96694, 14.40222). The ancient town Melite at Mdina is Q25352142.",
    ),
    "syracuse": Place(
        "Syracuse", 37.08333, 15.28333, "Q4420718", KNOWN,
        modern="Syracuse (Ortygia), Sicily, Italy",
        why="Continuous city.",
        aka=("Siracusa",),
        region="Sicily (not named in the WEB)",
        refs="Acts 28:12",
        roles=("rome",),
        note="Three days.",
        source="Q4420718 is the ancient city; the modern comune is Q13670.",
    ),
    "rhegium": Place(
        "Rhegium", 38.10928, 15.64393, "Q3429952", KNOWN,
        modern="Reggio Calabria, Italy",
        why="Continuous city on the Strait of Messina.",
        aka=("Rhegion", "Reggio Calabria"),
        region="Italy",
        refs="Acts 28:13",
        roles=("rome",),
        note="They wait a day here for a south wind.",
        source="The modern comune is Q8471.",
    ),
    "puteoli": Place(
        "Puteoli", 40.82092, 14.11985, "Q3936300", KNOWN,
        modern="Pozzuoli (Rione Terra), Bay of Naples, Italy",
        why="Continuous town. Rione Terra is the acropolis of the Roman colony, above the harbour where the grain ships docked.",
        aka=("Pozzuoli", "Rione Terra"),
        region="Italy",
        refs="Acts 28:13",
        roles=("rome",),
        note="Seven days with the brothers (28:14, which continues the sentence without repeating the name).",
        source="The Puteoli item Q10646925 has no coordinate. The modern comune is Q72425 (40.82306, 14.12222).",
    ),
    "market_of_appius": Place(
        "The Market of Appius", 41.46639, 12.9975, "Q3748871", KNOWN,
        modern="Borgo Faiti, Latina, Italy",
        why="The Via Appia station at the 43rd mile, fixed by the itineraries and milestones; remains at Borgo Faiti.",
        aka=("Forum Appii", "Appii Forum", "Borgo Faiti"),
        region="Italy",
        refs="Acts 28:15",
        roles=("rome",),
        note="The brothers from Rome come out this far to meet Paul.",
    ),
    "three_taverns": Place(
        "The Three Taverns", 41.56194, 12.87389, "Q622536", PROBABLE,
        modern="Near Cisterna di Latina, Italy",
        why="A Via Appia station about the 33rd mile, near Cisterna; the itineraries fix it roughly, but the exact remains are uncertain.",
        aka=("Tres Tabernae",),
        region="Italy",
        refs="Acts 28:15",
        roles=("rome",),
        note="Acts 28:15 has the brothers from Rome come out as far as the Market of Appius and the Three Taverns to meet Paul.",
    ),
    "rome": Place(
        "Rome", 41.89306, 12.48278, "Q220", KNOWN,
        modern="Rome, Italy",
        why="Continuous city; the city item's point sits by the Forum.",
        aka=("Roma",),
        region="Italy",
        refs="Acts 18:2; 19:21; 23:11; 28:14, 16; Rom 1:7, 15; 2 Tim 1:17",
        roles=("rome", "letter_to"),
        letters="Romans addressed to all in Rome (Rom 1:7, 15). 2 Timothy places Paul there in chains (2 Tim 1:16-17) but does not say it was written there. Philippians mentions Caesar's household (Phil 4:22), and Acts 28:30 has the two years in a rented house; both point to Rome without naming it.",
        source="The Roman Forum is Q180212 (41.8922, 12.4852).",
    ),
    "adramyttium": Place(
        "Adramyttium", 39.4955, 26.93752, "Q3605584", PROBABLE,
        modern="Ancient site at Oren, near Burhaniye, Balikesir, Turkey (modern Edremit lies inland)",
        why="The Roman harbour town is placed on the coast at Oren (Karatas), and the name moved to inland Edremit.",
        aka=("Adramyttion", "Edremit"),
        region="Asia (Acts 27:2, places on the coast of Asia)",
        refs="Acts 27:2",
        roles=("other_acts",),
        note="Named only as the home port of the first ship on the Rome voyage. Paul did not go there, so do not draw it as a stop.",
    ),
    "smyrna": Place(
        "Smyrna", 38.41861, 27.14284, "Q1379299", KNOWN,
        modern="Izmir (Agora of Smyrna), Turkey",
        why="Continuous city; the Roman agora is excavated.",
        aka=("Izmir",),
        region="Asia",
        refs="Rev 1:11; 2:8",
        roles=("assembly_rev", "letter_to"),
        letters="Revelation's letter to the assembly in Smyrna (Rev 2:8-11)",
        source="Wikidata also carries 38.42389, 27.14278.",
    ),
    "pergamum": Place(
        "Pergamum", 39.12947, 27.18412, "Q18986", KNOWN,
        modern="Pergamon acropolis, Bergama, Turkey",
        why="Excavated city (UNESCO); name preserved in Bergama.",
        aka=("Pergamon", "Bergama"),
        region="Asia",
        refs="Rev 1:11; 2:12",
        roles=("assembly_rev", "letter_to"),
        letters="Revelation's letter to the assembly in Pergamum (Rev 2:12-17)",
        note="The WEB spells it Pergamum.",
        source="Wikidata also carries 39.11667, 27.18333 (the lower town).",
    ),
    "thyatira": Place(
        "Thyatira", 38.92083, 27.84167, "Q1135603", KNOWN,
        modern="Akhisar (Tepe Mezarligi), Manisa, Turkey",
        why="Inscriptions naming Thyatira found at Akhisar; the ruins lie in the town centre.",
        aka=("Akhisar",),
        region="Asia (Lydia)",
        refs="Acts 16:14; Rev 1:11; 2:18, 24",
        roles=("assembly_rev", "letter_to", "other_acts"),
        letters="Revelation's letter to the assembly in Thyatira (Rev 2:18-29)",
        note="Lydia, the seller of purple at Philippi, came from Thyatira (Acts 16:14).",
        source="Wikidata's description wrongly says Caria. Wikidata also carries 38.89852, 27.84924.",
    ),
    "sardis": Place(
        "Sardis", 38.48831, 28.04029, "Q232615", KNOWN,
        modern="Sart, Salihli, Manisa, Turkey",
        why="Excavated Lydian capital; name preserved in Sart.",
        aka=("Sart",),
        region="Asia (Lydia)",
        refs="Rev 1:11; 3:1, 4",
        roles=("assembly_rev", "letter_to"),
        letters="Revelation's letter to the assembly in Sardis (Rev 3:1-6)",
    ),
    "philadelphia": Place(
        "Philadelphia", 38.35, 28.51667, "Q2085773", KNOWN,
        modern="Alasehir, Manisa, Turkey",
        why="The ancient city lies under Alasehir (Byzantine basilica piers survive).",
        aka=("Alasehir",),
        region="Asia (Lydia)",
        refs="Rev 1:11; 3:7",
        roles=("assembly_rev", "letter_to"),
        letters="Revelation's letter to the assembly in Philadelphia (Rev 3:7-13)",
        note="The coordinate is precise only to the minute (the same as the Alasehir town item).",
        source="Not the Philadelphia in Jordan (Q65202798).",
    ),
    "laodicea": Place(
        "Laodicea", 37.83583, 29.1075, "Q849709", KNOWN,
        modern="Ruins near Goncali / Eskihisar, Denizli, Turkey",
        why="Excavated city on the Lycus; identification secure.",
        aka=("Laodicea on the Lycus", "Laodikeia"),
        region="Asia (Phrygia)",
        refs="Col 2:1; 4:13, 15-16; Rev 1:11; 3:14",
        roles=("assembly_rev", "letter_to"),
        letters="Revelation's letter to the assembly in Laodicea (Rev 3:14-22). Colossians is to be read in the assembly of the Laodiceans, and they are to read the letter from Laodicea (Col 4:16).",
        source="Wikidata also carries 37.85525, 29.13642. The 37.83583, 29.1075 value is the city centre, and Colossae's item wrongly repeats it.",
    ),
    "colossae": Place(
        "Colossae", 37.79055, 29.25916, "Q1001370", KNOWN,
        modern="Unexcavated mound north of Honaz, Denizli, Turkey",
        why="The hoyuk on the Lycus near Honaz, identified from coins and inscriptions; not yet excavated.",
        aka=("Colosse", "Kolossai"),
        region="Asia (Phrygia)",
        refs="Col 1:2",
        roles=("letter_to",),
        letters="Colossians addressed to the saints at Colossae (Col 1:2). Philemon is usually placed here: Onesimus is one of you (Col 4:9), and Archippus appears in Col 4:17 and Phlm 2. Philemon itself names no city.",
        source="Wikidata's second value (37.83583, 29.1075) is Laodicea's coordinate and wrong for Colossae.",
    ),
    "hierapolis": Place(
        "Hierapolis", 37.925, 29.12583, "Q7428276", KNOWN,
        modern="Hierapolis-Pamukkale, Denizli, Turkey",
        why="Excavated city above the Pamukkale travertines (UNESCO).",
        aka=("Pamukkale",),
        region="Asia (Phrygia)",
        refs="Col 4:13",
        note="Named only in Col 4:13 (Epaphras's zeal for it); none of the roles fits.",
        source="Wikidata's other point (37.9074, 29.146) lies off the site.",
    ),
    "patmos": Place(
        "Patmos", 37.325, 26.54167, "Q190053", KNOWN,
        modern="Patmos, Dodecanese, Greece",
        why="Continuous name for the island.",
        aka=("Patmos island",),
        region="Aegean island off Asia",
        refs="Rev 1:9",
        roles=("letter_from",),
        letters="Revelation, with its seven letters, written on Patmos (Rev 1:9-11)",
        note="John was on the isle when told to write and send to the seven assemblies (1:11).",
        source="The ancient town is Q123786395 (37.32564, 26.53569).",
    ),
    "nicopolis": Place(
        "Nicopolis", 39.00801, 20.73605, "Q943637", PROBABLE,
        modern="Ruins north of Preveza, Epirus, Greece",
        why="Augustus's Actian Nicopolis in Epirus is the usual choice, as the leading city on the west coast for a winter stay. The rivals are Nicopolis on the Nestus in Thrace and a Nicopolis in Cilicia.",
        aka=("Actia Nicopolis", "Nikopolis"),
        region="Epirus (not named in the WEB)",
        refs="Titus 3:12",
        note="Paul plans to winter there and asks Titus to come, so the letter was not written there (the later subscription saying it was is not in the WEB). None of the roles fits.",
        source="Not Nicopolis in Lesser Armenia (Q619704) or in Egypt.",
    ),
}


# ===========================================================================
# The journeys
# ===========================================================================

JOURNEYS = {
    "journey1": Journey("The first journey", "Acts 13:4-14:26", [
        Stop("antioch_syria", "Acts 13:1-3", "start",
             note="The assembly sends out Barnabas and Saul."),
        Stop("seleucia", "Acts 13:4", "land", via="orontes",
             note="They go down to Antioch's port."),
        Stop("salamis", "Acts 13:4-5", "sea",
             note="They sail to Cyprus and preach in the synagogues."),
        Stop("paphos", "Acts 13:6", "land", via="cyprus",
             note="Gone through the island: Bar Jesus, and the proconsul Sergius Paulus."),
        Stop("perga", "Acts 13:13", "sea", via="paphos_perga",
             note="They sail to Perga in Pamphylia; John leaves them for Jerusalem. "
                  "Perga stands inland, and where they landed isn't said."),
        Stop("antioch_pisidia", "Acts 13:14", "land", via="perga_antioch",
             note="The sermon in the synagogue, and two Sabbaths."),
        Stop("iconium", "Acts 13:51; 14:1", "land", via="antioch_iconium",
             note="A long stay, until a move to stone them."),
        Stop("lystra", "Acts 14:6-8", "land", via="iconium_lystra",
             note="The lame man healed; Paul stoned (14:19)."),
        Stop("derbe", "Acts 14:20", "land", via="lystra_derbe",
             note="He goes out with Barnabas the next day."),
        Stop("lystra", "Acts 14:21", "land", via="lystra_derbe", note="They go back."),
        Stop("iconium", "Acts 14:21", "land", via="iconium_lystra", note="They go back."),
        Stop("antioch_pisidia", "Acts 14:21-23", "land", via="antioch_iconium",
             note="Elders appointed in every assembly."),
        Stop("perga", "Acts 14:24-25", "land", via="perga_antioch",
             note="Through Pisidia to Pamphylia; they speak the word in Perga."),
        Stop("attalia", "Acts 14:25", "land", via="perga_attalia",
             note="They go down to the port."),
        Stop("seleucia", "Acts 14:26", "sea", False, via="attalia_seleucia",
             note="They sail to Antioch: the port, Seleucia, isn't named this time."),
        Stop("antioch_syria", "Acts 14:26-27", "land", via="orontes",
             note="They gather the assembly and tell what God had done."),
    ]),
    "journey2": Journey("The second journey", "Acts 15:36-18:22", [
        Stop("antioch_syria", "Acts 15:35-40", "start",
             note="Paul chooses Silas; Barnabas takes Mark to Cyprus."),
        Stop("tarsus", "Acts 15:41", "land", False, via="antioch_derbe",
             note="He goes through Syria and Cilicia. Tarsus isn't named; the road to "
                  "Derbe ran by it and through the Cilician Gates."),
        Stop("derbe", "Acts 16:1", "land", via="antioch_derbe"),
        Stop("lystra", "Acts 16:1-3", "land", via="lystra_derbe", note="Timothy joins them."),
        Stop("iconium", "Acts 16:2-4", "land", False, via="iconium_lystra",
             note="Named only as where Timothy was known; going through the cities "
                  "implies they came."),
        Stop("antioch_pisidia", "Acts 16:4-6", "land", False, via="antioch_iconium",
             note="Not named: they went through the cities, and the region of "
                  "Phrygia and Galatia."),
        Stop("mysia", "Acts 16:6-8", "land", False, at=(39.62, 28.90),
             note="Forbidden to speak in Asia, they come opposite Mysia and try for "
                  "Bithynia. No town is named, and the way isn't known."),
        Stop("troas", "Acts 16:8-10", "land", False,
             note="Passing by Mysia, they come down to Troas: the vision of the man "
                  "of Macedonia, and 'we' begins."),
        Stop("samothrace", "Acts 16:11", "sea", via="troas_samothrace",
             note="A straight course."),
        Stop("neapolis", "Acts 16:11", "sea", note="The next day."),
        Stop("philippi", "Acts 16:12", "land", via="via_egnatia",
             note="A Roman colony: Lydia, the slave girl, the prison and the "
                  "earthquake (16:13-40)."),
        Stop("amphipolis", "Acts 17:1", "land", via="via_egnatia",
             note="Passed through, on the Via Egnatia."),
        Stop("apollonia", "Acts 17:1", "land", via="via_egnatia", note="Passed through."),
        Stop("thessalonica", "Acts 17:1-9", "land", via="via_egnatia",
             note="Three Sabbaths in the synagogue; Jason's house."),
        Stop("beroea", "Acts 17:10-14", "land", via="thessalonica_beroea",
             note="Sent away by night."),
        Stop("athens", "Acts 17:14-15", "sea", False, via="beroea_athens",
             note="Sent 'as far as to the sea', then brought to Athens: by sea is "
                  "the usual reading, but neither the port nor the way is said."),
        Stop("corinth", "Acts 18:1", "land", False, via="athens_corinth",
             note="He leaves Athens for Corinth, by land or sea it doesn't say. "
                  "He stays a year and six months (18:11)."),
        Stop("cenchreae", "Acts 18:18", "land",
             note="Corinth's eastern port: he shaves his head for a vow."),
        Stop("ephesus", "Acts 18:19-21", "sea", via="cenchreae_ephesus",
             note="He sails for Syria with Priscilla and Aquila, and leaves them at "
                  "Ephesus."),
        Stop("caesarea", "Acts 18:22", "sea", False, via="ephesus_caesarea",
             note="He lands at Caesarea. The course isn't given."),
        Stop("jerusalem", "Acts 18:21-22", "land", False, via="caesarea_jerusalem",
             note="He goes up and greets the assembly: Jerusalem isn't named, but "
                  "in 18:21 he says he must keep the coming feast there."),
        Stop("antioch_syria", "Acts 18:22", "land", False, via="jerusalem_antioch",
             note="He goes down to Antioch. The way isn't said."),
    ]),
    "journey3": Journey("The third journey", "Acts 18:23-21:17", [
        Stop("antioch_syria", "Acts 18:22-23", "start",
             note="He spends some time there, then sets out."),
        Stop("tarsus", "Acts 18:23", "land", False, via="antioch_derbe",
             note="Not named: the road to Galatia ran through Cilicia, as in 15:41."),
        Stop("derbe", "Acts 18:23", "land", False, via="antioch_derbe",
             note="He goes through the region of Galatia and Phrygia in order. "
                  "No town is named."),
        Stop("lystra", "Acts 18:23", "land", False, via="lystra_derbe", note="Not named."),
        Stop("iconium", "Acts 18:23", "land", False, via="iconium_lystra", note="Not named."),
        Stop("antioch_pisidia", "Acts 18:23", "land", False, via="antioch_iconium",
             note="Not named."),
        Stop("ephesus", "Acts 19:1", "land", False,
             note="Having passed through the upper country, which way isn't said. "
                  "About three years here (19:8-10; 20:31). The common road ran by "
                  "Colossae and Laodicea, but Colossians 2:1 suggests he never saw them."),
        Stop("troas", "Acts 20:1; 2 Cor 2:12-13", "land", False, via="ephesus_troas",
             note="Acts says only that he left for Macedonia; 2 Corinthians 2:12 puts "
                  "him at Troas on the way. By land or sea isn't said."),
        Stop("macedonia", "Acts 20:1-2; 2 Cor 2:13; 7:5", "sea", False, via="troas_neapolis",
             at=(40.93361, 24.41306),
             note="He goes through those parts. No town is named."),
        Stop("corinth", "Acts 20:2-3", "land", False, via="greece",
             note="He comes into Greece and spends three months there: Corinth is "
                  "inferred (1 Cor 16:5-6; Rom 16:1, 23). A plot, as he is about to "
                  "sail for Syria."),
        Stop("philippi", "Acts 20:3-6", "land", False, via="greece_back",
             note="He returns through Macedonia; his companions are listed in 20:4. "
                  "After the days of Unleavened Bread."),
        Stop("neapolis", "Acts 20:6", "land", False, via="via_egnatia",
             note="'We sailed away from Philippi': its port was Neapolis (16:11)."),
        Stop("troas", "Acts 20:6-12", "sea", via="neapolis_troas",
             note="Five days at sea, seven days at Troas: Eutychus."),
        Stop("assos", "Acts 20:13-14", "land", via="troas_assos",
             note="Paul goes on foot while the others sail round; they take him "
                  "aboard at Assos."),
        Stop("mitylene", "Acts 20:14", "sea"),
        Stop("chios", "Acts 20:15", "sea", via="mitylene_chios", at=(38.37, 26.22),
             note="The next day they come opposite Chios: passed, not landed."),
        Stop("samos", "Acts 20:15", "sea", via="chios_samos", at=(37.683, 26.95),
             note="They touch at Samos."),
        Stop("trogyllium", "Acts 20:15", "sea",
             note="'And stayed at Trogyllium': in the WEB, though not in the oldest "
                  "manuscripts."),
        Stop("miletus", "Acts 20:15-38", "sea", via="trogyllium_miletus",
             note="He sails past Ephesus (20:16) and calls its elders to Miletus."),
        Stop("cos", "Acts 21:1", "sea", via="miletus_cos", note="A straight course."),
        Stop("rhodes", "Acts 21:1", "sea", via="cos_rhodes", note="The next day."),
        Stop("patara", "Acts 21:1-2", "sea",
             note="They find a ship crossing over to Phoenicia."),
        Stop("tyre", "Acts 21:3-6", "sea", via="patara_tyre",
             note="In sight of Cyprus, they leave it on the left hand, and land at "
                  "Tyre: seven days there."),
        Stop("ptolemais", "Acts 21:7", "sea", via="tyre_ptolemais",
             note="They finish the voyage from Tyre, and stay one day."),
        Stop("caesarea", "Acts 21:8-14", "land", False, via="ptolemais_caesarea",
             note="The way isn't said; by the coast road, most likely. Philip's "
                  "house, and Agabus."),
        Stop("jerusalem", "Acts 21:15-17", "land", via="caesarea_jerusalem",
             note="They go up to Jerusalem, to lodge with Mnason of Cyprus."),
    ]),
    "rome": Journey("The voyage to Rome", "Acts 27:1-28:16", [
        Stop("caesarea", "Acts 25:4, 13; 27:1-2", "start",
             note="Held at Caesarea (25:4-13). They embark in a ship of Adramyttium; "
                  "27:1-2 doesn't name the port."),
        Stop("sidon", "Acts 27:3", "sea", via="caesarea_sidon",
             note="The next day; Julius lets Paul go to his friends."),
        Stop("myra", "Acts 27:4-6", "sea", via="sidon_myra",
             note="Under the lee of Cyprus, as the winds were against them, then "
                  "across the sea off Cilicia and Pamphylia to Myra: a ship of "
                  "Alexandria, sailing for Italy. Which side of Cyprus is inferred."),
        Stop("cnidus", "Acts 27:7", "sea", via="myra_cnidus", at=(36.62, 27.36),
             note="Slowly, many days, and with difficulty opposite Cnidus: passed, "
                  "not landed."),
        Stop("salmone", "Acts 27:7", "sea",
             note="The wind not allowing them further, they sail under the lee of "
                  "Crete, opposite Salmone."),
        Stop("fair_havens", "Acts 27:8-12", "sea", via="salmone_fair_havens",
             note="Near the city of Lasea. Most advise going on to winter at Phoenix, "
                  "a port of Crete; they never reach it."),
        Stop("clauda", "Acts 27:13-17", "sea", at=(34.79, 24.17),
             note="Along Crete, close in, until the Euroclydon drives them; under the "
                  "lee of Clauda they secure the boat and fear the Syrtis."),
        Stop("malta", "Acts 27:18-28:10", "sea", False, at=(35.948, 14.402),
             note="Fourteen nights driven back and forth in the Adriatic Sea: the "
                  "course isn't given. The bay where two seas met (27:41) is, by "
                  "tradition, St Paul's Bay. Three months on the island."),
        Stop("syracuse", "Acts 28:11-12", "sea", via="malta_syracuse",
             note="In a ship of Alexandria, the Twin Brothers: three days."),
        Stop("rhegium", "Acts 28:13", "sea", note="They circle round to Rhegium."),
        Stop("puteoli", "Acts 28:13-14", "sea", via="rhegium_puteoli",
             note="A south wind; the second day. Brothers, and seven days."),
        Stop("market_of_appius", "Acts 28:15", "land", via="puteoli_rome",
             note="Brothers from Rome come out to meet them."),
        Stop("three_taverns", "Acts 28:15", "land", via="puteoli_rome",
             note="The brothers from Rome come out as far as here, too, to meet "
                  "them: the verse names both places."),
        Stop("rome", "Acts 28:14, 16", "land", via="puteoli_rome",
             note="Paul is allowed to stay by himself, with the soldier who guards him."),
    ]),
}


# ===========================================================================
# Courses: our own points ("~"). By sea, where Acts or the sea gives the
# ship only one way past an island or cape. By land, where the text doesn't
# give the way (the leg is dotted), the points only keep the line on land
# and through the one way a pass or isthmus leaves: they name no station
# the text doesn't.
# ===========================================================================

COURSES = {
    # out of the Cestrus mouth to Perga (13:13), as the Acts 13-14 map has it
    "paphos_perga": [
        (34.84, 32.24),   # ~ off Paphos
        (35.12, 32.17),   # ~ round the Akamas
        (36.80, 30.95),   # ~ off the Cestrus mouth
    ],
    # home from Attalia to Seleucia (14:26), between Cyprus and the mainland
    "attalia_seleucia": [
        (36.55, 31.30),   # ~ off Side
        (35.98, 32.50),   # ~ south of Cape Anamur
        (35.95, 33.40),   # ~ north of Cyprus
        (35.95, 34.40),   # ~
        (36.05, 35.30),   # ~ into the Gulf of Issus
    ],
    # Beroea to the sea, and down outside Euboea to Athens (17:14-15)
    "beroea_athens": [
        (40.37, 22.62),   # ~ the coast below Beroea (Pydna or Methone, unnamed)
        (40.05, 22.85),   # ~ the Thermaic gulf
        (39.62, 23.42),   # ~ off Magnesia
        (39.05, 23.95),   # ~ past the Sporades
        (38.35, 24.55),   # ~ off Euboea
        (38.12, 24.66),   # ~ round Cape Kafireas, between Euboea and Andros
        (37.88, 24.55),   # ~
        (37.60, 24.05),   # ~ round Sounion
        (37.88, 23.62),   # ~ into Phaleron bay
    ],
    # Athens to Corinth (18:1): by land or sea isn't said; by land, along the
    # Megarid to the Isthmus
    "athens_corinth": [
        (38.012, 23.636),   # ~ inland of the bay of Phaleron
        (38.055, 23.535),   # ~ round the head of the bay of Eleusis
        (38.005, 23.345),   # ~ the Megarid
        (37.985, 23.200),   # ~ the Scironian road
        (37.925, 23.010),   # ~ the Isthmus
    ],
    # Cenchreae to Ephesus (18:19), round Sounion and through the Cyclades
    "cenchreae_ephesus": [
        (37.85, 23.40),   # ~ north of Aegina
        (37.78, 23.70),   # ~
        (37.56, 24.12),   # ~ round Sounion
        (37.50, 24.40),   # ~ between Kea and Kythnos
        (37.35, 24.70),   # ~ between Serifos and Syros
        (37.30, 25.25),   # ~ between Mykonos and Naxos
        (37.50, 26.05),   # ~ off Ikaria
        (37.68, 26.47),   # ~ between Ikaria and Samos
        (37.87, 26.75),   # ~ north of Samos
        (37.92, 27.00),   # ~
        (37.95, 27.15),   # ~ the Cayster mouth
    ],
    # Ephesus to Caesarea (18:21-22), the course not given
    "ephesus_caesarea": [
        (37.95, 27.15),   # ~ the Cayster mouth
        (37.92, 27.00),   # ~
        (37.87, 26.75),   # ~ north of Samos
        (37.68, 26.47),   # ~ between Ikaria and Samos
        (37.50, 26.75),   # ~ south of Samos
        (37.32, 27.05),   # ~
        (37.01, 27.14),   # ~ between Calymna and the Bodrum peninsula
        (36.93, 27.30),   # ~ the strait of Cos
        (36.90, 27.36),   # ~ off the east end of Cos
        (36.80, 27.36),   # ~
        (36.64, 27.33),   # ~ round Cnidus
        (36.58, 27.60),   # ~
        (36.52, 28.15),   # ~ off Rhodes
        (34.40, 32.10),   # ~ south of Cyprus
        (33.00, 34.30),   # ~
    ],
    # Troas to Samothrace (16:11), north of Tenedos and Imbros
    "troas_samothrace": [
        (39.95, 26.06),   # ~ north of Tenedos
        (40.18, 26.04),   # ~ between Imbros and the Chersonese
        (40.36, 25.84),   # ~ north of Imbros
        (40.52, 25.64),   # ~ off Samothrace
    ],
    # Neapolis back to Troas (20:6), round Thasos and between Imbros and
    # Samothrace
    "neapolis_troas": [
        (40.88, 24.55),   # ~ between Thasos and the mainland
        (40.80, 24.85),   # ~ east of Thasos
        (40.36, 25.38),   # ~ south of Samothrace
        (40.33, 25.85),   # ~ between Samothrace and Imbros
        (40.18, 26.04),   # ~ between Imbros and the Chersonese
        (39.95, 26.06),   # ~ north of Tenedos
    ],
    "troas_neapolis": [
        (39.95, 26.06),   # ~ north of Tenedos
        (40.18, 26.04),   # ~ between Imbros and the Chersonese
        (40.33, 25.85),   # ~ between Samothrace and Imbros
        (40.36, 25.38),   # ~ south of Samothrace
        (40.80, 24.85),   # ~ east of Thasos
        (40.88, 24.55),   # ~ between Thasos and the mainland
    ],
    # Ephesus to Troas (20:1): the way isn't said; by land, round the heads of
    # the gulfs
    "ephesus_troas": [
        (38.40, 27.30),   # ~ round the head of the gulf of Smyrna
        (39.10, 27.25),   # ~ inland of the gulf of Elaea
        (39.60, 27.00),   # ~ round the head of the gulf of Adramyttium
        (39.65, 26.55),   # ~ the foothills of Ida
    ],
    # Jerusalem down to Antioch (18:22): the way isn't said; inland of the
    # Phoenician coast
    "jerusalem_antioch": [
        (33.40, 35.75),   # ~
        (34.60, 36.20),   # ~ inland of Tripoli
    ],
    # Mitylene down the strait of Chios (20:14-15), and round the west of
    # Samos to its harbour (20:15)
    "mitylene_chios": [
        (38.98, 26.64),   # ~ off the south-east of Lesbos
        (38.72, 26.30),   # ~ round Cape Mimas
        (38.48, 26.22),   # ~ into the strait of Chios
    ],
    "chios_samos": [
        (38.22, 26.24),   # ~ the strait of Chios
        (37.95, 26.55),   # ~
        (37.68, 26.47),   # ~ between Ikaria and Samos
        (37.61, 26.80),   # ~ south of Samos
        (37.645, 26.93),   # ~
    ],
    # Trogyllium to Miletus (20:15): Miletus stood on a gulf the Maeander has
    # since filled
    "trogyllium_miletus": [
        (37.58, 27.13),   # ~
        (37.52, 27.18),   # ~ the old gulf's mouth
    ],
    "miletus_cos": [
        (37.52, 27.18),   # ~ the old gulf's mouth
        (37.33, 27.14),   # ~ off Didyma
        (37.01, 27.14),   # ~ between Calymna and the Bodrum peninsula
    ],
    "cos_rhodes": [
        (36.90, 27.36),   # ~ off the east end of Cos
        (36.80, 27.36),   # ~
        (36.64, 27.33),   # ~ round Cnidus
        (36.58, 27.60),   # ~
        (36.55, 27.95),   # ~
    ],
    "tyre_ptolemais": [
        (33.22, 35.16),   # ~
        (33.09, 35.06),   # ~ off Ras Naqoura
        (32.97, 35.05),   # ~
    ],
    # Caesarea up the coast to Sidon (27:3)
    "caesarea_sidon": [
        (32.84, 34.92),   # ~ off Carmel
        (33.09, 35.06),   # ~ off Ras Naqoura
        (33.28, 35.15),   # ~ off Tyre
        (33.45, 35.25),   # ~
    ],
    # Myra west along Lycia, north of Rhodes, to opposite Cnidus (27:7)
    "myra_cnidus": [
        (36.17, 29.95),   # ~ off Andriake, Myra's port
        (36.10, 29.55),   # ~
        (36.22, 29.20),   # ~ off Patara
        (36.42, 28.75),   # ~
        (36.55, 28.30),   # ~ north of Rhodes
        (36.50, 28.00),   # ~
        (36.58, 27.65),   # ~
    ],
    # Rhegium up the strait and into the bay of Puteoli (28:13), between
    # Misenum and Nisida
    "rhegium_puteoli": [
        (38.17, 15.61),   # ~ up the strait of Messina
        (38.225, 15.62),   # ~ off Punta Pezzo
        (38.252, 15.665),   # ~ between Cannitello and Capo Peloro
        (38.285, 15.71),   # ~ out of the strait
        (40.45, 14.15),   # ~
        (40.76, 14.11),   # ~ the mouth of the bay
    ],
    # Malta round Cape Passero to Syracuse (28:11-12)
    "malta_syracuse": [
        (36.55, 15.10),   # ~
        (36.70, 15.25),   # ~ off Cape Passero
        (36.95, 15.38),   # ~
        (37.05, 15.35),   # ~ into the harbour
    ],
    # from Macedonia down through Greece to Corinth and back (20:2-3): the way
    # isn't said; by land, Tempe, Thermopylae and the Isthmus are the only ways
    "greece": [
        (40.83, 23.84),   # ~ over the Strymon
        (40.63, 23.47),   # ~ south of Lake Bolbe
        (40.68, 22.85),   # ~ round the head of the Thermaic gulf
        (40.55, 22.55),   # ~ the Macedonian plain
        (40.17, 22.49),   # ~ under Olympus
        (39.89, 22.58),   # ~ the vale of Tempe, the one way into Thessaly
        (39.62, 22.42),   # ~ Thessaly
        (38.78, 22.50),   # ~ the pass at Thermopylae
        (38.32, 23.32),   # ~ Boeotia
        (38.005, 23.345),   # ~ the Megarid
        (37.985, 23.200),   # ~ the Scironian cliffs
        (37.925, 23.010),   # ~ the Isthmus
    ],
    "greece_back": [
        (37.925, 23.010),   # ~ the Isthmus
        (37.985, 23.200),   # ~ the Scironian cliffs
        (38.005, 23.345),   # ~ the Megarid
        (38.32, 23.32),   # ~ Boeotia
        (38.78, 22.50),   # ~ the pass at Thermopylae
        (39.62, 22.42),   # ~ Thessaly
        (39.89, 22.58),   # ~ the vale of Tempe
        (40.17, 22.49),   # ~ under Olympus
        (40.60, 22.75),   # ~ the Macedonian plain
    ],
    # Patara to Tyre, leaving Cyprus on the left (21:3)
    "patara_tyre": [
        (34.40, 32.10),   # ~ south-west of Cyprus
    ],
    # Sidon to Myra (27:4-5): under the lee of Cyprus, then across the sea off
    # Cilicia and Pamphylia
    "sidon_myra": [
        (34.70, 34.95),   # ~
        (35.75, 34.65),   # ~ off Cape Andreas
        (35.70, 33.45),   # ~ north of Cyprus
        (36.00, 32.20),   # ~ the sea off Cilicia and Pamphylia
        (36.15, 30.70),   # ~
    ],
    # under the lee of Crete from Salmone to Fair Havens (27:7-8)
    "salmone_fair_havens": [
        (35.20, 26.40),   # ~ round Salmone
        (34.95, 26.20),   # ~
        (34.85, 25.60),   # ~ along the south coast
    ],
}


# ===========================================================================
# Roads
# ===========================================================================

# Via Egnatia, Neapolis to Thessalonica
# Sure in outline. The Via Egnatia is attested by Strabo and milestones, and
# the stations are those of the itineraries. Philippi, Amphipolis and
# Apollonia are Acts 17:1's own list. Domeros is the mutatio 19 Roman miles
# from Philippi and 13 from Amphipolis. Pennana and Peripidis (Euripides' tomb
# at Arethusa, in the Aulon/Rentina pass) are the Bordeaux Itinerary's
# stations between Amphipolis and Apollonia, and Bromiscus sits at the outflow
# of Lake Bolbe in the same pass. Mellisurgis is the Antonine and Peutinger
# station on the Thessalonica-Apollonia road, 20 Roman miles from
# Thessalonica. The ancient bridge at Amphipolis carried the road over the
# Strymon. Less sure: Amygdaleonas only marks the crossing of Mount Symbolon
# between Neapolis and Philippi (the modern road's line). The stretch from
# Mellisurgis to Thessalonica has no located station. The Bordeaux Itinerary's
# Heracleustibus, Duodea and ad Decimum, and ad Duodecimum east of Domeros,
# are not in Wikidata, so these legs are straight.
VIA_EGNATIA = [
    (40.9336, 24.4131),   # Neapolis (Q6984309)
    (40.9628, 24.3592),   # Amygdaleonas (Q3154319)
    (41.0121, 24.2846),   # Philippi (Q379652)
    (40.9459, 23.9223),   # Domeros (mutatio) (Q60793084)
    (40.8236, 23.8466),   # Amphipolis (Q217414)
    (40.8283, 23.8347),   # Amphipolis Bridge (over the Strymon) (Q27777827)
    (40.7556, 23.7208),   # Pennana (Asprovalta mutatio) (Q124703671)
    (40.6772, 23.6833),   # Bromiscus (Q17623020)
    (40.6566, 23.6229),   # Arethusa (Rentina pass) (Q4789100)
    (40.6222, 23.4677),   # Apollonia (Q2751389)
    (40.5927, 23.4678),   # Mellisurgis (Q16909799)
    (40.6378, 22.9458),   # Thessalonica (Q48038544)
]

# Thessalonica to Beroea across the Macedonian plain
# Low to moderate confidence. Cicero called Beroea a town off the main road
# (oppidum devium), and I could not verify an itinerary station list for this
# road. The line keeps south of the old Lake Loudias (Giannitsa) by the one
# Roman datum on it, the Roman bridge at Kleidi in Imathia. Sindos and
# Chalastra mark the Gallikos-Axios crossing west of Thessalonica, and
# Alexandreia (a modern town) only marks the plain on the way to Beroea. The
# alternative, west on the Via Egnatia to Pella and then south under Mount
# Bermion by Mieza (Pella Q213679, Mieza Q132472), is longer and no better
# attested.
THESSALONICA_BEROEA = [
    (40.6378, 22.9458),   # Thessalonica (Q48038544)
    (40.6700, 22.8081),   # Sindos (ancient) (Q111820863)
    (40.6267, 22.7322),   # Chalastra (Q1059457)
    (40.5740, 22.6225),   # Kleidi Roman Bridge (Q55355756)
    (40.5853, 22.4853),   # Alexandreia (Q15967005)
    (40.5258, 22.2046),   # Beroea (Q15712213)
]

# Troas to Assos on foot (Acts 20:13)
# Low confidence in the line, though the leg itself is certain (Acts 20:13).
# No Roman road or station is attested between Alexandria Troas and Assos.
# This is the direct inland way over the hills, about 35 km (24 Roman miles),
# which fits the 'about twenty miles' commentators give for the walk. Its only
# ancient datum is the stone-paved road at Paşaköy (Wikidata 'ancient road',
# undated). Behramkale Bridge, where the way crosses the Tuzla (Satnioeis)
# below Assos, is Ottoman. The villages only mark the way. The alternative
# coast road south by Larisa (Q6489418, 39.6153, 26.1453), the bridge near
# Tuzla (Q131402787, 39.5775, 26.1297), Tuzla (Q6550715, 39.5686, 26.1672) and
# up the Tuzla valley is about 30 Roman miles.
TROAS_ASSOS = [
    (39.7519, 26.1586),   # Troas (Alexandria Troas) (Q1393407)
    (39.6286, 26.1833),   # Kösedere (Q6596114)
    (39.6089, 26.1900),   # Babadere (Q6877065)
    (39.5875, 26.2333),   # Taşboğaz (Q10824165)
    (39.5247, 26.3128),   # Paşaköy paved ancient road (Q139428343)
    (39.4988, 26.3329),   # Behramkale Bridge (Q131402791)
    (39.4878, 26.3369),   # Assos (Q744631)
]

# Via Campana and Via Appia, Puteoli to Rome
# Sure. The Via Domitiana along the coast was built in AD 95, after Paul, so
# from Puteoli he took the Via Campana (the 'via Antica consolare campana', 21
# Roman miles). Italian Wikipedia gives its course: from the amphitheatre at
# Puteoli through the Montagna Spaccata cut at Quarto, and by Qualiano,
# Giugliano, Aversa and Teverola to the Via Appia at ancient Capua. From there
# the Via Appia runs through the itinerary stations Casilinum, Sinuessa,
# Minturnae, Formiae, Fundi, Tarracina, Forum Appii, Tripontium, Tres Tabernae
# (Ad Sponsas), Aricia and Bovillae to its start at the Porta Capena. Acts
# 28:15 names Forum Appii and Tres Tabernae on this road. From Tarracina to
# Aricia the Appia is famously straight, across the Pontine marshes. Itri and
# Monte San Biagio mark the Appia's passes between Formiae, Fundi and
# Tarracina. The whole is about 150 Roman miles, which matches the
# itineraries.
PUTEOLI_ROME = [
    (40.8209, 14.1198),   # Puteoli (Rione Terra) (Q3936300)
    (40.8259, 14.1251),   # Flavian Amphitheatre of Puteoli (Q662766)
    (40.8678, 14.1246),   # Montagna Spaccata (Q3861067)
    (40.8833, 14.1333),   # Quarto (Q72443)
    (40.9167, 14.1500),   # Qualiano (Q72438)
    (40.9283, 14.2011),   # Giugliano in Campania (Q72125)
    (40.9730, 14.2065),   # Aversa (Q19279)
    (41.0000, 14.2167),   # Teverola (Q58906)
    (41.0862, 14.2504),   # Capua (Q3136685)
    (41.1094, 14.2091),   # Casilinum (Q952753)
    (41.1539, 13.8476),   # Sinuessa (Q1349926)
    (41.2421, 13.7682),   # Minturnae (Q18170298)
    (41.2564, 13.6069),   # Formiae (Q128086)
    (41.2833, 13.5333),   # Itri (Q128092)
    (41.3500, 13.4167),   # Fundi (Q128084)
    (41.3500, 13.3500),   # Monte San Biagio (Q128107)
    (41.2833, 13.2500),   # Tarracina (Q128226)
    (41.4664, 12.9975),   # The Market of Appius (Forum Appii) (Q3748871)
    (41.5074, 12.9452),   # Tor Tre Ponti (Tripontium) (Q18453921)
    (41.5619, 12.8739),   # The Three Taverns (Tres Tabernae) (Q622536)
    (41.5839, 12.8461),   # Ad Sponsas (Q137648377)
    (41.7167, 12.6667),   # Aricia (Vallericcia) (Q4008214)
    (41.7575, 12.6217),   # Bovillae (Q743694)
    (41.8210, 12.5560),   # Casal Rotondo (Q3661405)
    (41.8520, 12.5207),   # Tomb of Caecilia Metella (Q1540920)
    (41.8839, 12.4905),   # Porta Capena (Q1632777)
]

# Antioch through the Syrian and Cilician Gates to Derbe
# For 15:41 and 18:23, where Acts names only Syria and Cilicia. The road is
# sure as far as Podandus. The Bordeaux Itinerary (AD 333) and the Antonine
# Itinerary run Antioch, Pagrae, the Syrian Gates, Alexandria, Issus,
# Mopsuestia, Adana, Tarsus, the Cilician Gates and Podandus, and Cicero
# crossed the Taurus between Cybistra and Tarsus in 51 BC. Toprakkale (a
# medieval castle) marks the pass from the Issus plain to Mopsuestia. Less
# sure from Podandus west: Ulukışla (a modern town) marks the road to Cybistra
# (Heraclea, modern Ereğli), and the leg from Cybistra along the foot of the
# Taurus to Derbe (Kerti Höyük) has no station list I could verify. Paul's
# passing through these places is inferred, not stated.
ANTIOCH_DERBE = [
    (36.2025, 36.1606),   # Antioch (Antakya) (Q80561)
    (36.4269, 36.2250),   # Pagrae (Bagras) (Q799921)
    (36.4795, 36.2320),   # Syrian Gates (Belen Pass) (Q2890848)
    (36.5872, 36.1733),   # Alexandria by Issus (İskenderun) (Q174341)
    (36.8383, 36.1644),   # Issus (Q1360503)
    (37.0504, 36.1366),   # Toprakkale (Q131901853)
    (36.9578, 35.6195),   # Mopsuestia (Q555923)
    (36.9864, 35.3253),   # Adana (Q38545)
    (36.9165, 34.8951),   # Tarsus (Q134287)
    (37.2853, 34.7861),   # Cilician Gates (Q128884)
    (37.4278, 34.8711),   # Podandus (Pozantı) (Q7124031)
    (37.5467, 34.4844),   # Ulukışla (Q1018537)
    (37.5142, 34.0480),   # Cybistra (Ereğli) (Q996056)
    (37.3486, 33.3615),   # Derbe (Kerti Höyük) (Q20717624)
]

# Antioch of Pisidia to Ephesus by Apamea and the Maeander (the common road)
# The road is attested but Paul's use of it is only possible. From Antioch the
# Via Sebaste ran west round the north of Lake Hoyran, by the milestones at
# Gençali and by Tymandus, to the colony Apollonia (the villages follow David
# French's line, as acts_geography.PERGA_ANTIOCH does). From Apollonia west to
# Apamea is a probable link. The Apamea-Ephesus stretch is Strabo's 'common
# road' (14.2.29, after Artemidorus): Ephesus, Magnesia, Tralles, Nysa,
# Antioch on the Maeander, Carura, Laodicea, Apamea. Colossae and the salt
# lake by Anaua lie between Laodicea and Celaenae/Apamea on the route of
# Herodotus (7.30) and Xenophon. But Col 2:1 implies Paul had not been seen at
# Colossae or Laodicea, and 19:1's 'upper country' is often read (Ramsay) as
# the higher road north of the Lycus and Maeander valleys, by the Cayster
# valley. I could not verify that road's stations, so it is not given. Draw
# this road as a possibility, not as Paul's route.
ANTIOCH_EPHESUS = [
    (38.3042, 31.1897),   # Antioch of Pisidia (Q579468)
    (38.2922, 30.9592),   # Gökçeali (Q10763607)
    (38.2989, 30.8439),   # Aşağıkaşıkara (Q10736761)
    (38.2090, 30.7422),   # Gençali (Via Sebaste milestones) (Q6729165)
    (38.1040, 30.6070),   # Tymandus (Q2462752)
    (38.0725, 30.4705),   # Apollonia (Sozopolis) (Q1856209)
    (38.0717, 30.1656),   # Apamea (Dinar) (Q617518)
    (37.8892, 29.8094),   # Anaua (Lake Acıgöl) (Q96372039)
    (37.7906, 29.2592),   # Colossae (Q1001370)
    (37.8358, 29.1075),   # Laodicea (Q849709)
    (37.9403, 28.8229),   # Carura (Q5047484)
    (37.8729, 28.5495),   # Antioch on the Maeander (Q579405)
    (37.8878, 28.1512),   # Nysa (Q1779332)
    (37.8444, 27.8458),   # Tralles (Q462630)
    (37.8527, 27.5271),   # Magnesia on the Maeander (Q1432674)
    (37.9406, 27.3394),   # Ephesus (Q47611)
]

# Caesarea to Jerusalem by Antipatris and Beth Horon
# For 18:22 ('went up') and 21:15-17. Well attested. Acts 23:31-33 itself puts
# Antipatris on the Jerusalem-Caesarea road. Josephus (Jewish War 2.19) has
# Cestius Gallus march from Caesarea by Antipatris and Lydda, up the Beth
# Horon ascent, and by Gibeon (Gabao) to Jerusalem in AD 66. Upper and Lower
# Beth Horon are the villages Beit Ur al-Fauqa and al-Tahta. Paul's route is
# not named in either passage, so it is likely, not certain.
CAESAREA_JERUSALEM = [
    (32.5011, 34.8923),   # Caesarea (Q319242)
    (32.1050, 34.9304),   # Antipatris (Q682612)
    (31.9656, 34.8917),   # Lydda (Lod) (Q207540)
    (31.8950, 35.0836),   # Lower Beth Horon (Beit Ur al-Tahta) (Q2905332)
    (31.8858, 35.1142),   # Upper Beth Horon (Beit Ur al-Fauqa) (Q2905277)
    (31.8475, 35.1864),   # Gibeon (Q889398)
    (31.7767, 35.2342),   # Jerusalem (Q1218)
]

# Ptolemais to Caesarea along the coast
# For 21:8, if that leg went by land, which the text does not say. The coast
# road round Carmel is attested: the Bordeaux Itinerary goes from Ptolemais by
# Calamon, Sycaminum and Certha to Caesarea, and Dora (Dor) is a coastal
# station. Sycaminum is Tel Shikmona at Carmel's point. Tell Abu Hawam marks
# the bay shore at the Kishon mouth and Tel Megadim the coast below Carmel,
# both for shape only, because Calamon and Certha are not located in Wikidata.
PTOLEMAIS_CAESAREA = [
    (32.9261, 35.0839),   # Ptolemais (Acre) (Q126084)
    (32.8008, 35.0192),   # Tell Abu Hawam (Q694326)
    (32.8249, 34.9553),   # Sycaminum (Tel Shikmona) (Q2919810)
    (32.7237, 34.9477),   # Tel Megadim (Q6954831)
    (32.6174, 34.9164),   # Dor (Tel Dor) (Q1243563)
    (32.5011, 34.8923),   # Caesarea (Q319242)
]

ROADS = {
    "orontes": Road("Antioch down the Orontes to Seleucia", G.ROADS["ORONTES_ROAD"],
                    "From the Acts 13-14 map: the valley of the Orontes."),
    "cyprus": Road("Across Cyprus, Salamis to Paphos", G.ROADS["CYPRUS_ROAD"],
                   "From the Acts 13-14 map: the coast road by Kition and Kourion."),
    "perga_antioch": Road("The Via Sebaste, Perga to Antioch of Pisidia",
                          G.ROADS["PERGA_ANTIOCH"],
                          "From the Acts 13-14 map: Augustus's road, by French's survey."),
    "antioch_iconium": Road("Antioch of Pisidia to Iconium", G.ROADS["ANTIOCH_ICONIUM"],
                            "From the Acts 13-14 map."),
    "iconium_lystra": Road("Iconium to Lystra", G.ROADS["ICONIUM_LYSTRA"],
                           "From the Acts 13-14 map."),
    "lystra_derbe": Road("Lystra to Derbe", G.ROADS["LYSTRA_DERBE"],
                         "From the Acts 13-14 map."),
    "perga_attalia": Road("Perga to Attalia", G.ROADS["PERGA_ATTALIA"],
                          "From the Acts 13-14 map."),
    "antioch_derbe": Road("Antioch through the Syrian and Cilician Gates to Derbe",
                          ANTIOCH_DERBE,
                          "Sure as far as Podandus, below the Cilician Gates. Beyond, the "
                          "road to Derbe is not attested: Ulukisla only marks the way."),
    "via_egnatia": Road("The Via Egnatia, Neapolis to Thessalonica", VIA_EGNATIA,
                        "Sure in outline: Strabo, milestones, and the itineraries' "
                        "stations, with Acts 17:1's own Philippi, Amphipolis and "
                        "Apollonia."),
    "thessalonica_beroea": Road("Thessalonica to Beroea", THESSALONICA_BEROEA,
                                "Not attested by any itinerary: across the Macedonian "
                                "plain by the Roman bridge at Kleidi."),
    "troas_assos": Road("Troas to Assos", TROAS_ASSOS,
                        "No Roman road is attested; the line keeps inland by the "
                        "villages and the bridge below Assos."),
    "puteoli_rome": Road("The Via Campana and the Via Appia, Puteoli to Rome", PUTEOLI_ROME,
                         "Sure: the Via Appia's stations, among them the Market of Appius "
                         "and the Three Taverns (28:15)."),
    "antioch_ephesus": Road("The common road, Antioch of Pisidia to Ephesus",
                            ANTIOCH_EPHESUS,
                            "Strabo's highway by Apamea, Colossae, Laodicea and the "
                            "Maeander. Not drawn as Paul's: Colossians 2:1 suggests he "
                            "never saw Colossae or Laodicea."),
    "caesarea_jerusalem": Road("Caesarea to Jerusalem", CAESAREA_JERUSALEM,
                               "By Antipatris (23:31) and Beth Horon, the soldiers' road."),
    "ptolemais_caesarea": Road("Ptolemais to Caesarea", PTOLEMAIS_CAESAREA,
                               "Along the coast, under Mount Carmel."),
}


# ===========================================================================
# Lands, waters, letters and the seven assemblies
# ===========================================================================

REGIONS = {
    "macedonia": Region("Macedonia", 40.95, 22.45, r"\bMacedonia\b"),
    "achaia": Region("Achaia", 37.62, 22.20, r"\bAchaia\b", aka=("Greece",),
                     note="Acts 20:2 calls it Greece."),
    "asia": Region("Asia", 38.60, 28.70, r"\bAsia\b",
                   note="The Roman province, on the Aegean shore of Asia Minor."),
    "mysia": Region("Mysia", 40.02, 27.70, r"\bMysia\b"),
    "bithynia": Region("Bithynia", 40.45, 30.40, r"\bBithynia\b"),
    "galatia": Region("Galatia", 39.35, 32.70, r"\bGalatia\b",
                      note="The Roman province reached south to Antioch of Pisidia, "
                           "Iconium, Lystra and Derbe."),
    "phrygia": Region("Phrygia", 38.80, 30.55, r"\bPhrygia\b"),
    "pisidia": Region("Pisidia", 37.62, 30.95, r"\bPisidia\b"),
    "pamphylia": Region("Pamphylia", 37.10, 31.55, r"\bPamphylia\b"),
    "lycaonia": Region("Lycaonia", 37.95, 33.25, r"\bLycaonia\b"),
    "cilicia": Region("Cilicia", 37.25, 35.45, r"\bCilicia\b"),
    "lycia": Region("Lycia", 36.55, 29.75, r"\bLycia\b"),
    "cappadocia": Region("Cappadocia", 38.75, 35.20, r"\bCappadocia\b"),
    "pontus": Region("Pontus", 40.75, 35.60, r"\bPontus\b"),
    "syria": Region("Syria", 35.10, 36.60, r"\bSyria\b"),
    "phoenicia": Region("Phoenicia", 33.85, 35.75, r"\bPhoenicia\b"),
    "judea": Region("Judea", 31.55, 34.95, r"\bJudea\b"),
    "cyprus": Region("Cyprus", 35.05, 33.25, r"\bCyprus\b"),
    "crete": Region("Crete", 35.22, 24.95, r"\bCrete\b|\bCretans\b"),
    "italy": Region("Italy", 41.05, 15.30, r"\bItaly\b"),
    "illyricum": Region("Illyricum", 41.55, 20.15, r"\bIllyricum\b",
                        note="Romans 15:19's far point of Paul's preaching."),
}

WATERS = {
    "cilicia_sea": Region("the sea off Cilicia and Pamphylia", 36.35, 32.40,
                          r"sea which is off Cilicia and Pamphylia"),
    "adriatic": Region("the Adriatic Sea", 36.40, 18.40, r"\bAdriatic\b",
                       note="In Paul's day the name reached south over the open sea "
                            "between Crete, Sicily and Greece."),
    "syrtis": Region("the Syrtis", 31.65, 18.60, r"\bSyrtis\b",
                     note="The shoals off Libya that the sailors feared (27:17)."),
}

# What each letter is addressed to, from its own words; and where it was
# written only where it says so (1 Corinthians 16:8, Revelation 1:9).
LETTERS = [
    Letter("Romans", ("rome",), "Rom 1:7, 15",
           note="Usually placed at Corinth, from Phoebe of Cenchreae (16:1) and "
                "Erastus (16:23), but the letter doesn't name the city."),
    Letter("1 Corinthians", ("corinth",), "1 Cor 1:2", "ephesus", "1 Cor 16:8"),
    Letter("2 Corinthians", ("corinth",), "2 Cor 1:1",
           note="Written from Macedonia, by 2 Corinthians 7:5 and 9:2, no town named."),
    Letter("Galatians", ("galatia",), "Gal 1:2"),
    Letter("Ephesians", ("ephesus",), "Eph 1:1",
           note="'At Ephesus' is missing from some early manuscripts; the WEB has it."),
    Letter("Philippians", ("philippi",), "Phil 1:1"),
    Letter("Colossians", ("colossae",), "Col 1:2",
           note="To be read at Laodicea too (4:16)."),
    Letter("1 Thessalonians", ("thessalonica",), "1 Thess 1:1"),
    Letter("2 Thessalonians", ("thessalonica",), "2 Thess 1:1"),
    Letter("1 Timothy", ("ephesus",), "1 Tim 1:3",
           note="To Timothy, whom Paul left at Ephesus."),
    Letter("Titus", ("crete",), "Titus 1:5", note="To Titus, whom Paul left in Crete."),
    Letter("Revelation", ("ephesus", "smyrna", "pergamum", "thyatira", "sardis",
                          "philadelphia", "laodicea"), "Rev 1:11", "patmos", "Rev 1:9"),
]

# Revelation 2-3, in the order the letters come, with each one's verses
ASSEMBLIES = [
    ("ephesus", "Rev 2:1-7"), ("smyrna", "Rev 2:8-11"), ("pergamum", "Rev 2:12-17"),
    ("thyatira", "Rev 2:18-29"), ("sardis", "Rev 3:1-6"),
    ("philadelphia", "Rev 3:7-13"), ("laodicea", "Rev 3:14-22"),
]
