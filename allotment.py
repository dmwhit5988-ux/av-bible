"""Joshua 13-19 verse by verse: the tribe whose lot each verse gives, what
kind of verse it is, every place, land, water and landmark it names in the
order it names them, the border it walks, and the count it gives. For the
allotment map (generate_joshua1319_svg.py), which draws it on gazetteer.py.

How it was made. Gathered verse by verse on 2026-10-29 from the WEB and
checked by script: every SITE key is a gazetteer place (SITES, JERUSALEM or
BEYOND), every REGION a gazetteer.REGIONS key, and every WATER's point an
existing point of that water's gazetteer line (the coast, a lake or a
river), chosen for the part of it the verse means. A name with no agreed
site, or no point fact for it, is UNPLACED, and its note says why. Nothing
here places anything of its own.

- **VERSES** are keyed (chapter, verse). `tribe` is the tribe whose lot the
  verse gives (or none: the land that remained, the eastern tribes'
  summary); Caleb's story (14:6-15, 15:13-19) is Judah's, told within its
  lot. `kind` is "border" (the text walks a border
  landmark by landmark), "towns" (a list of cities), "story" or "summary".
- **names** run in the verse's own order, each the WEB's word: Gazites at
  Gaza, the Sidonians at Sidon, Baalah at Kiriath Jearim, where the verse
  means that place.
- **walk** is the border's names in order (a subset of `names`); `cont`
  says it carries on from the verse before. "|" breaks a walk the text
  gives in two pieces (13:26).
- **count** is a count the verse itself gives, in its words.
"""

from typing import NamedTuple

SITE, WATER, REGION, UNPLACED = "site", "water", "region", "unplaced"


class N(NamedTuple):
    web: str                     # the name as the verse spells it
    kind: str                    # SITE, WATER, REGION or UNPLACED
    key: str = ""                # gazetteer key (SITES/JERUSALEM/BEYOND, WATERS, REGIONS)
    at: tuple = ()               # a WATER's point: an existing point of its line
    note: str = ""


class Verse(NamedTuple):
    tribe: str
    kind: str
    names: tuple
    walk: tuple = ()
    cont: bool = False
    count: str = ""


VERSES = {
    (13, 1): Verse("", "story", ()),
    (13, 2): Verse("", "summary", (
        N("Philistines", REGION, "philistia"),
        N("Geshurites", UNPLACED, "", (), note="The southern Geshurites beside Philistia (1 Sam 27:8, 'on the way to Shur'), a people of the north-western Negev, not the Geshur of 13:11, 13; no site or point."),
    )),
    (13, 3): Verse("", "summary", (
        N("Shihor", WATER, "brook_of_egypt", (31.1457, 33.8065)),
        N("Egypt", UNPLACED, "", (), note="The land of Egypt, beyond the map's south-west edge; no region key."),
        N("Ekron", SITE, "ekron"),
        N("Gazites", SITE, "gaza"),
        N("Ashdodites", SITE, "ashdod"),
        N("Ashkelonites", SITE, "ashkelon"),
        N("Gittites", SITE, "gath"),
        N("Ekronites", SITE, "ekron"),
        N("Avvim", UNPLACED, "", (), note="A people who 'lived in villages as far as Gaza' (Deut 2:23), south of Gaza; no site. Not the Benjamite town Avvim of Josh 18:23."),
    ), count="the five lords of the Philistines"),
    (13, 4): Verse("", "summary", (
        N("Canaanites", UNPLACED, "", (), note="'all the land of the Canaanites': Canaan as a whole; no region key and no point."),
        N("Mearah", UNPLACED, ""),
        N("Sidonians", SITE, "sidon"),
        N("Aphek", SITE, "aphek_lebanon"),
        N("Amorites", UNPLACED, "", (), note="'the border of the Amorites', usually read as the land of Amurru in Syria north of Lebanon; a land with no point or region key."),
    )),
    (13, 5): Verse("", "summary", (
        N("Gebalites", SITE, "gebal"),
        N("Lebanon", REGION, "lebanon"),
        N("Baal Gad", UNPLACED, "", (), note="In UNPLACED: 'Baal Gad under Mount Hermon' is unidentified (Banias and Hasbaya are guesses)."),
        N("Mount Hermon", SITE, "mount_hermon"),
        N("entrance of Hamath", SITE, "lebo_hamath"),
    )),
    (13, 6): Verse("", "summary", (
        N("Lebanon", REGION, "lebanon"),
        N("Misrephoth Maim", SITE, "misrephoth_maim"),
        N("Sidonians", SITE, "sidon"),
    )),
    (13, 7): Verse("", "summary", ()),
    (13, 8): Verse("", "summary", (
        N("Jordan", WATER, "jordan", (31.8742, 35.5408), note="'beyond the Jordan eastward': the river opposite Jericho, where Israel crossed."),
    )),
    (13, 9): Verse("", "summary", (
        N("Aroer", SITE, "aroer_arnon"),
        N("Arnon", WATER, "arnon", (31.4444, 35.8175), note="'the edge of the valley of the Arnon' at Aroer: the Mujib Dam, the Arnon point just below 'Ara'ir, from RIVERS['arnon']."),
        N("the city that is in the middle of the valley", UNPLACED, "", (), note="An unnamed town in the Arnon gorge; sometimes taken for Ar of Moab or Khirbet el-Medeiyineh, but nothing is agreed."),
        N("Medeba", SITE, "medeba"),
        N("Dibon", SITE, "dibon"),
    )),
    (13, 10): Verse("", "summary", (
        N("Heshbon", SITE, "heshbon"),
        N("Ammon", REGION, "ammon"),
    )),
    (13, 11): Verse("", "summary", (
        N("Gilead", REGION, "gilead"),
        N("Geshurites", UNPLACED, "", (), note="Geshur, the Aramean land east of the Sea of Galilee (the Golan); a district with no agreed capital and no region key."),
        N("Maacathites", UNPLACED, "", (), note="Maacah, the Aramean land north of Geshur, below Hermon; a district with no point or region key."),
        N("Mount Hermon", SITE, "mount_hermon"),
        N("Bashan", REGION, "bashan"),
        N("Salecah", SITE, "salecah"),
    )),
    (13, 12): Verse("", "summary", (
        N("Bashan", REGION, "bashan"),
        N("Ashtaroth", SITE, "ashtaroth"),
        N("Edrei", SITE, "edrei"),
    )),
    (13, 13): Verse("", "story", (
        N("Geshurites", UNPLACED, "", (), note="Geshur east of the Sea of Galilee: a district, no point or region key."),
        N("Maacathites", UNPLACED, "", (), note="Maacah below Hermon: a district, no point or region key."),
        N("Geshur", UNPLACED, "", (), note="The land of Geshur; no point or region key."),
        N("Maacath", UNPLACED, "", (), note="The land of Maacah (spelled Maacath here only); no point or region key."),
    )),
    (13, 14): Verse("Levi", "summary", ()),
    (13, 15): Verse("Reuben", "summary", ()),
    (13, 16): Verse("Reuben", "border", (
        N("Aroer", SITE, "aroer_arnon"),
        N("Arnon", WATER, "arnon", (31.4444, 35.8175), note="'the edge of the valley of the Arnon' at Aroer: the Mujib Dam point below 'Ara'ir, from RIVERS['arnon']."),
        N("the city that is in the middle of the valley", UNPLACED, "", (), note="An unnamed town in the Arnon gorge; Ar of Moab and Khirbet el-Medeiyineh are guesses, nothing agreed."),
        N("Medeba", SITE, "medeba"),
    ), walk=("Aroer", "Arnon")),
    (13, 17): Verse("Reuben", "towns", (
        N("Heshbon", SITE, "heshbon"),
        N("plain", UNPLACED, "", (), note="'the plain' (the Mishor), the tableland north of the Arnon round Medeba and Heshbon; no region key."),
        N("Dibon", SITE, "dibon"),
        N("Bamoth Baal", UNPLACED, ""),
        N("Beth Baal Meon", SITE, "baal_meon"),
    )),
    (13, 18): Verse("Reuben", "towns", (
        N("Jahaz", SITE, "jahaz"),
        N("Kedemoth", UNPLACED, ""),
        N("Mephaath", SITE, "mephaath"),
    )),
    (13, 19): Verse("Reuben", "towns", (
        N("Kiriathaim", SITE, "kiriathaim_moab"),
        N("Sibmah", UNPLACED, ""),
        N("Zereth Shahar", UNPLACED, ""),
        N("mount of the valley", UNPLACED, "", (), note="A description of where Zereth Shahar stood (a hill above the valley, perhaps the Salt Sea's rift), not a placed landmark."),
    )),
    (13, 20): Verse("Reuben", "towns", (
        N("Beth Peor", UNPLACED, ""),
        N("Pisgah", SITE, "mount_nebo"),
        N("Beth Jeshimoth", SITE, "beth_jeshimoth"),
    )),
    (13, 21): Verse("Reuben", "summary", (
        N("plain", UNPLACED, "", (), note="'all the cities of the plain' (the Mishor north of the Arnon); no region key."),
        N("Heshbon", SITE, "heshbon"),
        N("Midian", UNPLACED, "", (), note="'the chiefs of Midian', a people, not a place in the allotment; Midian's land lies far to the south-east and has no region key."),
    )),
    (13, 22): Verse("", "story", ()),
    (13, 23): Verse("Reuben", "border", (
        N("Jordan", WATER, "jordan", (31.8011, 35.5481), note="'the bank of the Jordan' as Reuben's western border: the lowest reach, above the Salt Sea and opposite Beth Jeshimoth."),
    ), walk=("Jordan",)),
    (13, 24): Verse("Gad", "summary", ()),
    (13, 25): Verse("Gad", "border", (
        N("Jazer", SITE, "jazer"),
        N("Gilead", REGION, "gilead"),
        N("Ammon", REGION, "ammon"),
        N("Aroer", UNPLACED, "", (), note="In UNPLACED: Aroer 'that is near Rabbah', an Ammonite-border town, not located."),
        N("Rabbah", SITE, "rabbah_ammon"),
    ), walk=("Jazer", "Aroer")),
    (13, 26): Verse("Gad", "border", (
        N("Heshbon", SITE, "heshbon"),
        N("Ramath Mizpeh", UNPLACED, ""),
        N("Betonim", UNPLACED, ""),
        N("Mahanaim", SITE, "mahanaim"),
        N("Debir", UNPLACED, ""),
    ), walk=("Heshbon", "Ramath Mizpeh", "Betonim", "|", "Mahanaim", "Debir")),
    (13, 27): Verse("Gad", "border", (
        N("valley", UNPLACED, "", (), note="'in the valley': the Jordan valley east of the river; no region key (REGIONS arabah is labelled south of the Salt Sea and skips this sense)."),
        N("Beth Haram", SITE, "beth_haram"),
        N("Beth Nimrah", SITE, "beth_nimrah"),
        N("Succoth", SITE, "succoth"),
        N("Zaphon", UNPLACED, "", (), note="In UNPLACED: Tell el-Qos, Tell es-Sa'idiyeh and Tell el-Mazar proposed; no consensus, no point."),
        N("Heshbon", SITE, "heshbon"),
        N("Jordan", WATER, "jordan", (32.1153, 35.5431)),
        N("sea of Chinnereth", WATER, "galilee", (32.7116, 35.5732), note="'the uttermost part of the sea of Chinnereth': its south end, where the Jordan leaves the lake."),
    ), walk=("Jordan", "sea of Chinnereth")),
    (13, 28): Verse("Gad", "summary", ()),
    (13, 29): Verse("Manasseh", "summary", ()),
    (13, 30): Verse("Manasseh", "border", (
        N("Mahanaim", SITE, "mahanaim"),
        N("Bashan", REGION, "bashan"),
        N("villages of Jair", UNPLACED, "", (), note="In UNPLACED (Havvoth Jair): a district of Bashan, not a point."),
    ), walk=("Mahanaim",), count="sixty cities"),
    (13, 31): Verse("Manasseh", "towns", (
        N("Gilead", REGION, "gilead"),
        N("Ashtaroth", SITE, "ashtaroth"),
        N("Edrei", SITE, "edrei"),
        N("Bashan", REGION, "bashan"),
    )),
    (13, 32): Verse("", "summary", (
        N("Moab", REGION, "moab"),
        N("Jordan", WATER, "jordan", (31.8742, 35.5408), note="'beyond the Jordan at Jericho': the river due east of Jericho."),
        N("Jericho", SITE, "jericho"),
    )),
    (13, 33): Verse("Levi", "summary", ()),
    (14, 1): Verse("", "summary", (
        N("Canaan", UNPLACED, "", (), note="'the land of Canaan': the whole land west of the Jordan; no region key."),
    )),
    (14, 2): Verse("", "summary", ()),
    (14, 3): Verse("", "summary", (
        N("Jordan", WATER, "jordan", (31.8742, 35.5408), note="'beyond the Jordan': the river as the eastern tribes' frontier, taken opposite Jericho where Israel crossed."),
    )),
    (14, 4): Verse("", "summary", ()),
    (14, 5): Verse("", "summary", ()),
    (14, 6): Verse("Judah", "story", (
        N("Gilgal", SITE, "gilgal_jericho"),
        N("Kadesh Barnea", SITE, "kadesh_barnea"),
    )),
    (14, 7): Verse("Judah", "story", (
        N("Kadesh Barnea", SITE, "kadesh_barnea"),
    )),
    (14, 8): Verse("Judah", "story", ()),
    (14, 9): Verse("Judah", "story", ()),
    (14, 10): Verse("Judah", "story", ()),
    (14, 11): Verse("Judah", "story", ()),
    (14, 12): Verse("Judah", "story", (
        N("hill country", REGION, "judah"),
    )),
    (14, 13): Verse("Judah", "story", (
        N("Hebron", SITE, "hebron"),
    )),
    (14, 14): Verse("Judah", "story", (
        N("Hebron", SITE, "hebron"),
    )),
    (14, 15): Verse("Judah", "story", (
        N("Hebron", SITE, "hebron"),
        N("Kiriath Arba", SITE, "hebron"),
    )),
    (15, 1): Verse("Judah", "summary", (
        N("Edom", REGION, "edom"),
        N("wilderness of Zin", REGION, "zin"),
    )),
    (15, 2): Verse("Judah", "border", (
        N("Salt Sea", WATER, "salt_sea", (30.9975, 35.4352), note="'the uttermost part of the Salt Sea, the bay that looks southward': the sea's southern end, at the mouth of Wadi Arabah (SALT_SEA)"),
    ), walk=("Salt Sea",)),
    (15, 3): Verse("Judah", "border", (
        N("Akrabbim", SITE, "akrabbim"),
        N("Zin", REGION, "zin"),
        N("Kadesh Barnea", SITE, "kadesh_barnea"),
        N("Hezron", UNPLACED, "", (), note="Not identified. Numbers 34:4 joins Hezron and Addar as one place, Hazar Addar. Springs near Kadesh Barnea ('Ain Qedeis and others) have been proposed, with no agreement and no point fact."),
        N("Addar", UNPLACED, "", (), note="Not identified. Hazar Addar in Numbers 34:4. The proposed springs near Kadesh have no agreement."),
        N("Karka", UNPLACED, "", (), note="Not identified. 'Ain el-Qoseimeh has been proposed, but others put Azmon there. No agreed site."),
    ), walk=("Akrabbim", "Zin", "Kadesh Barnea", "Hezron", "Addar", "Karka"), cont=True),
    (15, 4): Verse("Judah", "border", (
        N("Azmon", SITE, "azmon"),
        N("brook of Egypt", WATER, "brook_of_egypt", (30.8278, 34.1397), note="'went out at the brook of Egypt': the point where the border from Azmon meets the wadi. Rawafa Dam is the BROOK_OF_EGYPT point nearest to Kadesh and Azmon. The border then runs down the wadi to its mouth."),
        N("sea", WATER, "great_sea", (31.1457, 33.8065), note="'the border ended at the sea': the great sea at the mouth of Wadi el-Arish (COAST, last point)"),
    ), walk=("Azmon", "brook of Egypt", "sea"), cont=True),
    (15, 5): Verse("Judah", "border", (
        N("Salt Sea", WATER, "salt_sea", (31.4617, 35.3997), note="The east border is the whole west shore, from the southern end up to the Jordan's mouth. Taken at Nahal Arugot on the En Gedi shore, about midway (SALT_SEA)."),
        N("Jordan", WATER, "jordan", (31.7614, 35.5583), note="'the end of the Jordan': its mouth in the Salt Sea (JORDAN_LOWER, last point). The verse names it twice, and both times it is the mouth."),
        N("bay of the sea", WATER, "salt_sea", (31.7614, 35.5583), note="'the bay of the sea at the end of the Jordan': the Salt Sea's north shore at the Jordan's mouth (SALT_SEA, first point), where the north border starts"),
    ), walk=("Salt Sea", "Jordan", "bay of the sea")),
    (15, 6): Verse("Judah", "border", (
        N("Beth Hoglah", SITE, "beth_hoglah"),
        N("Beth Arabah", UNPLACED, "", (), note="Listed in UNPLACED: candidates ('Ain el-Gharabeh) exist, but none is settled. The arabah region skips this verse."),
        N("stone of Bohan", UNPLACED, "", (), note="A boundary stone near the north end of the Salt Sea (also Josh 18:17). Not identified (Hajar el-Asbah has been proposed), and there is no point fact."),
    ), walk=("Beth Hoglah", "Beth Arabah", "stone of Bohan"), cont=True),
    (15, 7): Verse("Judah", "border", (
        N("Debir", UNPLACED, "", (), note="Thoghret ed-Debr on the Jericho road has been proposed, but it has no point fact."),
        N("valley of Achor", UNPLACED, "", (), note="Debated: el-Buqei'a above Qumran, Wadi en-Nuweimeh north of Jericho, or Wadi Qelt."),
        N("Gilgal", UNPLACED, "", (), note="Not identified."),
        N("Adummim", SITE, "ascent_of_adummim"),
        N("river", UNPLACED, "", (), note="The wadi below the ascent of Adummim, not named (usually taken to be Wadi Qelt). It has no point of its own."),
        N("En Shemesh", UNPLACED, "", (), note="'the waters of En Shemesh'."),
        N("En Rogel", SITE, "en_rogel"),
    ), walk=("valley of Achor", "Debir", "Gilgal", "En Shemesh", "En Rogel"), cont=True),
    (15, 8): Verse("Judah", "border", (
        N("valley of the son of Hinnom", SITE, "valley_of_hinnom"),
        N("Jebusite", SITE, "jerusalem"),
        N("Jerusalem", SITE, "jerusalem"),
        N("top of the mountain", UNPLACED, "", (), note="Not named: the ridge west of the Hinnom valley at the north end of the valley of Rephaim. It has no point of its own, so the head of the valley of Rephaim stands for it."),
        N("valley of Hinnom", SITE, "valley_of_hinnom"),
        N("valley of Rephaim", SITE, "valley_of_rephaim"),
    ), walk=("valley of the son of Hinnom", "Jebusite", "top of the mountain", "valley of Rephaim"), cont=True),
    (15, 9): Verse("Judah", "border", (
        N("top of the mountain", UNPLACED, "", (), note="The unnamed mountain of verse 8"),
        N("Nephtoah", SITE, "nephtoah"),
        N("Mount Ephron", UNPLACED, "", (), note="'the cities of Mount Ephron'. Not identified; the ridge by el-Qastel and Motza has been suggested."),
        N("Baalah", SITE, "kiriath_jearim"),
        N("Kiriath Jearim", SITE, "kiriath_jearim"),
    ), walk=("top of the mountain", "Nephtoah", "Mount Ephron", "Baalah"), cont=True),
    (15, 10): Verse("Judah", "border", (
        N("Baalah", SITE, "kiriath_jearim"),
        N("Mount Seir", UNPLACED, "", (), note="Judah's Mount Seir, west of Kiriath Jearim, not Edom's."),
        N("Mount Jearim", SITE, "chesalon"),
        N("Chesalon", SITE, "chesalon"),
        N("Beth Shemesh", SITE, "beth_shemesh"),
        N("Timnah", SITE, "timnah_dan"),
    ), walk=("Baalah", "Mount Seir", "Mount Jearim", "Beth Shemesh", "Timnah"), cont=True),
    (15, 11): Verse("Judah", "border", (
        N("Ekron", SITE, "ekron"),
        N("Shikkeron", UNPLACED, "", (), note="Listed in UNPLACED: not identified (Tell el-Ful by the Sorek has been proposed)"),
        N("Mount Baalah", UNPLACED, "", (), note="Listed in UNPLACED: not identified. It is not Baalah = Kiriath Jearim, whose skip includes Josh 15:11."),
        N("Jabneel", SITE, "jabneh"),
        N("sea", WATER, "great_sea", (31.9419, 34.7073), note="'the goings out of the border were at the sea': the great sea at the mouth of Nahal Sorek, where reconstructions bring Judah's north border down to the coast (COAST)."),
    ), walk=("Ekron", "Shikkeron", "Mount Baalah", "Jabneel", "sea"), cont=True),
    (15, 12): Verse("Judah", "border", (
        N("great sea", WATER, "great_sea", (31.5252, 34.4311), note="'the shore of the great sea': the west border is the whole shore from the Sorek's mouth to the brook of Egypt. Taken at the Port of Gaza, about midway (COAST)."),
    ), walk=("great sea",)),
    (15, 13): Verse("Judah", "story", (
        N("Kiriath Arba", SITE, "hebron"),
        N("Hebron", SITE, "hebron"),
    )),
    (15, 14): Verse("Judah", "story", ()),
    (15, 15): Verse("Judah", "story", (
        N("Debir", SITE, "debir_judah"),
        N("Kiriath Sepher", SITE, "debir_judah"),
    )),
    (15, 16): Verse("Judah", "story", (
        N("Kiriath Sepher", SITE, "debir_judah"),
    )),
    (15, 17): Verse("Judah", "story", ()),
    (15, 18): Verse("Judah", "story", ()),
    (15, 19): Verse("Judah", "story", (
        N("the South", REGION, "south"),
        N("upper springs", UNPLACED, "", (), note="Springs given with Debir."),
        N("lower springs", UNPLACED, "", (), note="As for the upper springs"),
    )),
    (15, 20): Verse("Judah", "summary", ()),
    (15, 21): Verse("Judah", "towns", (
        N("Edom", REGION, "edom"),
        N("the South", REGION, "south"),
        N("Kabzeel", UNPLACED, "", (), note="Listed in UNPLACED (Negev towns)."),
        N("Eder", UNPLACED, "", (), note="Not identified; it may be a corrupt reading of Arad"),
        N("Jagur", UNPLACED, "", (), note="Not identified"),
    )),
    (15, 22): Verse("Judah", "towns", (
        N("Kinah", UNPLACED, "", (), note="Listed in UNPLACED: Horvat Uza is a candidate, but no name ties it there"),
        N("Dimonah", UNPLACED, "", (), note="Not identified; perhaps the Dibon of Neh 11:25"),
        N("Adadah", UNPLACED, "", (), note="Not identified."),
    )),
    (15, 23): Verse("Judah", "towns", (
        N("Kedesh", UNPLACED, "", (), note="The Kedesh of the Negev. Not identified; some equate it with Kadesh Barnea. It is not Kedesh of Naphtali, whose skip includes this verse."),
        N("Hazor", UNPLACED, "", (), note="A Hazor of the Negev, not identified. It is not Hazor of Naphtali, whose skip includes Josh 15:23."),
        N("Ithnan", UNPLACED, "", (), note="Not identified"),
    )),
    (15, 24): Verse("Judah", "towns", (
        N("Ziph", UNPLACED, "", (), note="Not identified."),
        N("Telem", UNPLACED, "", (), note="Perhaps the Telaim of 1 Sam 15:4. Not identified."),
        N("Bealoth", UNPLACED, "", (), note="Perhaps Baalath Beer (Josh 19:8). Not identified."),
    )),
    (15, 25): Verse("Judah", "towns", (
        N("Hazor Hadattah", UNPLACED, "", (), note="Not identified"),
        N("Kerioth Hezron", SITE, "kerioth_hezron"),
        N("Hazor", SITE, "kerioth_hezron"),
    )),
    (15, 26): Verse("Judah", "towns", (
        N("Amam", UNPLACED, "", (), note="Not identified"),
        N("Shema", UNPLACED, "", (), note="Perhaps the Sheba of Josh 19:2. Not identified."),
        N("Moladah", UNPLACED, "", (), note="Listed in UNPLACED (Negev towns): Khereibet el-Waten and Tel Malhata are proposed."),
    )),
    (15, 27): Verse("Judah", "towns", (
        N("Hazar Gaddah", UNPLACED, "", (), note="Not identified"),
        N("Heshmon", UNPLACED, "", (), note="Not identified"),
        N("Beth Pelet", UNPLACED, "", (), note="Listed in UNPLACED (Negev towns): not identified"),
    )),
    (15, 28): Verse("Judah", "towns", (
        N("Hazar Shual", UNPLACED, "", (), note="Listed in UNPLACED (Negev towns): debated"),
        N("Beersheba", SITE, "beersheba"),
        N("Biziothiah", UNPLACED, "", (), note="Not identified. The Greek reads 'and their villages' here, so it may not be a town name at all."),
    )),
    (15, 29): Verse("Judah", "towns", (
        N("Baalah", UNPLACED, "", (), note="The Negev Baalah (Balah, Josh 19:3; Bilhah, 1 Chr 4:29), not Baalah = Kiriath Jearim, whose skip includes Josh 15:29. Not identified."),
        N("Iim", UNPLACED, "", (), note="Not identified"),
        N("Ezem", UNPLACED, "", (), note="Umm el-'Azam has been proposed."),
    )),
    (15, 30): Verse("Judah", "towns", (
        N("Eltolad", UNPLACED, "", (), note="Not identified (Tolad, 1 Chr 4:29)"),
        N("Chesil", UNPLACED, "", (), note="Bethul in Simeon's list (Josh 19:4). Not identified."),
        N("Hormah", SITE, "hormah"),
    )),
    (15, 31): Verse("Judah", "towns", (
        N("Ziklag", SITE, "ziklag"),
        N("Madmannah", UNPLACED, "", (), note="Listed in UNPLACED (Negev towns): Khirbet Umm Deimneh has been proposed, and there is no point fact"),
        N("Sansannah", UNPLACED, "", (), note="Listed in UNPLACED (Negev towns). Hazar Susah in Josh 19:5; Khirbet esh-Shamsaniyat has been proposed."),
    )),
    (15, 32): Verse("Judah", "towns", (
        N("Lebaoth", UNPLACED, "", (), note="Beth Lebaoth (Josh 19:6). Not identified."),
        N("Shilhim", UNPLACED, "", (), note="Perhaps Sharuhen (Josh 19:6), which is itself debated (Tell el-Far'ah South, Tell el-Ajjul, Tel Haror). Not identified."),
        N("Ain", UNPLACED, "", (), note="Listed in UNPLACED (Ain and Rimmon). Often read with Rimmon as En Rimmon (Neh 11:29); Khirbet Umm er-Rammamin by Tel Halif has been proposed."),
        N("Rimmon", UNPLACED, "", (), note="Listed in UNPLACED. It is not Rimmon of Benjamin or of Zebulun, whose skips both include Josh 15:32."),
    ), count="All the cities are twenty-nine, with their villages"),
    (15, 33): Verse("Judah", "towns", (
        N("lowland", UNPLACED, "", (), note="The Shephelah. REGIONS has no key for it (sites carry region='the lowland' as a string only)."),
        N("Eshtaol", SITE, "eshtaol"),
        N("Zorah", SITE, "zorah"),
        N("Ashnah", UNPLACED, "", (), note="In UNPLACED (Josh 15:33-41 note): unidentified, no coordinate. Not the Ashnah of v43."),
    )),
    (15, 34): Verse("Judah", "towns", (
        N("Zanoah", SITE, "zanoah_shephelah"),
        N("En Gannim", UNPLACED, "", (), note="In UNPLACED (Josh 15:33-41 note): unidentified, no coordinate."),
        N("Tappuah", UNPLACED, "", (), note="In UNPLACED (Josh 15:33-41 note): the lowland Tappuah is unidentified."),
        N("Enam", UNPLACED, "", (), note="In UNPLACED (Josh 15:33-41 note): unidentified, no coordinate. It may be the Enaim of Gen 38."),
    )),
    (15, 35): Verse("Judah", "towns", (
        N("Jarmuth", SITE, "jarmuth_judah"),
        N("Adullam", SITE, "adullam"),
        N("Socoh", SITE, "socoh_shephelah"),
        N("Azekah", SITE, "azekah"),
    )),
    (15, 36): Verse("Judah", "towns", (
        N("Shaaraim", SITE, "shaaraim"),
        N("Adithaim", UNPLACED, "", (), note="Unidentified; no point fact."),
        N("Gederah", UNPLACED, "", (), note="In UNPLACED (Josh 15:33-41 note): debated, no coordinate."),
        N("Gederothaim", UNPLACED, "", (), note="The WEB gives it as an alternative to Gederah ('or Gederothaim'). Unidentified."),
    ), count="fourteen cities with their villages"),
    (15, 37): Verse("Judah", "towns", (
        N("Zenan", UNPLACED, "", (), note="Unidentified; often equated with Zaanan (Mic 1:11). No point fact."),
        N("Hadashah", UNPLACED, "", (), note="Unidentified."),
        N("Migdal Gad", UNPLACED, ""),
    )),
    (15, 38): Verse("Judah", "towns", (
        N("Dilean", UNPLACED, "", (), note="Unidentified."),
        N("Mizpah", UNPLACED, "", (), note="Mizpeh of the lowland, in UNPLACED (Josh 15:33-41 note)."),
        N("Joktheel", UNPLACED, "", (), note="The lowland Joktheel is unidentified."),
    )),
    (15, 39): Verse("Judah", "towns", (
        N("Lachish", SITE, "lachish"),
        N("Bozkath", UNPLACED, "", (), note="Wikipedia: in the Shephelah, but its exact location is unknown."),
        N("Eglon", SITE, "eglon"),
    )),
    (15, 40): Verse("Judah", "towns", (
        N("Cabbon", UNPLACED, "", (), note="Unidentified."),
        N("Lahmam", UNPLACED, "", (), note="Khirbet el-Lahm near Beit Guvrin has been proposed."),
        N("Chitlish", UNPLACED, "", (), note="Unidentified."),
    )),
    (15, 41): Verse("Judah", "towns", (
        N("Gederoth", UNPLACED, "", (), note="In UNPLACED (Josh 15:33-41 note): no coordinate."),
        N("Beth Dagon", UNPLACED, "", (), note="In UNPLACED (Josh 15:33-41 note): Judah's Beth Dagon is unidentified. Not Asher's (Josh 19:27)."),
        N("Naamah", UNPLACED, "", (), note="In UNPLACED (Josh 15:33-41 note): unidentified."),
        N("Makkedah", SITE, "makkedah"),
    ), count="sixteen cities with their villages"),
    (15, 42): Verse("Judah", "towns", (
        N("Libnah", SITE, "libnah"),
        N("Ether", UNPLACED, ""),
        N("Ashan", UNPLACED, "", (), note="Debated (Khirbet 'Asan near Beersheba and others), with no point fact. Also a town of Simeon (Josh 19:7) and a Levite town (1 Chr 6:59)."),
    )),
    (15, 43): Verse("Judah", "towns", (
        N("Iphtah", UNPLACED, "", (), note="Tarqumiya has been proposed, but this is not settled and no source ties the town's point to Iphtah."),
        N("Ashnah", UNPLACED, "", (), note="The second Ashnah."),
        N("Nezib", UNPLACED, ""),
    )),
    (15, 44): Verse("Judah", "towns", (
        N("Keilah", SITE, "keilah"),
        N("Achzib", UNPLACED, "", (), note="Achzib of Judah, in UNPLACED: Tell el-Beida has been proposed, with no coordinate."),
        N("Mareshah", SITE, "mareshah"),
    ), count="nine cities with their villages"),
    (15, 45): Verse("Judah", "towns", (
        N("Ekron", SITE, "ekron"),
    )),
    (15, 46): Verse("Judah", "towns", (
        N("Ekron", SITE, "ekron"),
        N("sea", WATER, "great_sea", (31.7803, 34.6222)),
        N("Ashdod", SITE, "ashdod"),
    )),
    (15, 47): Verse("Judah", "towns", (
        N("Ashdod", SITE, "ashdod"),
        N("Gaza", SITE, "gaza"),
        N("brook of Egypt", WATER, "brook_of_egypt", (31.1457, 33.8065)),
        N("great sea", WATER, "great_sea", (31.5252, 34.4311), note="'the great sea with its coastline': the western edge from the Wadi el-Arish mouth north past Gaza and Ashdod."),
    )),
    (15, 48): Verse("Judah", "towns", (
        N("hill country", REGION, "judah"),
        N("Shamir", UNPLACED, "", (), note="Judah's Shamir is unidentified (UNPLACED covers 'the other minor towns of Josh 15:48-60'). Not Tola's Shamir in Ephraim (Judg 10:1)."),
        N("Jattir", SITE, "jattir"),
        N("Socoh", UNPLACED, "", (), note="Socoh of the hill country (Khirbet Shuweikeh, south-west of Hebron), in UNPLACED with no coordinate."),
    )),
    (15, 49): Verse("Judah", "towns", (
        N("Dannah", UNPLACED, "", (), note="Unidentified."),
        N("Kiriath Sannah", SITE, "debir_judah"),
        N("Debir", SITE, "debir_judah"),
    )),
    (15, 50): Verse("Judah", "towns", (
        N("Anab", SITE, "anab"),
        N("Eshtemoh", SITE, "eshtemoa"),
        N("Anim", UNPLACED, "", (), note="In UNPLACED (Khirbet Ghuwein keeps the name, but there is no item with a coordinate)."),
    )),
    (15, 51): Verse("Judah", "towns", (
        N("Goshen", UNPLACED, "", (), note="Judah's Goshen is unidentified (ed-Dhahiriya has been suggested). Not the Goshen in Egypt."),
        N("Holon", UNPLACED, "", (), note="Unidentified; no point fact."),
        N("Giloh", UNPLACED, "", (), note="Ahithophel's town. Khirbet Jala near Beit Ummar is the other proposal. No agreed point."),
    ), count="eleven cities with their villages"),
    (15, 52): Verse("Judah", "towns", (
        N("Arab", UNPLACED, "", (), note="Khirbet er-Rabiyeh has been proposed, with no point fact."),
        N("Dumah", UNPLACED, "", (), note="In UNPLACED (Khirbet Domeh keeps the name, but there is no item with a coordinate)."),
        N("Eshan", UNPLACED, "", (), note="Unidentified."),
    )),
    (15, 53): Verse("Judah", "towns", (
        N("Janim", UNPLACED, "", (), note="Unidentified."),
        N("Beth Tappuah", SITE, "beth_tappuah"),
        N("Aphekah", UNPLACED, "", (), note="Unidentified."),
    )),
    (15, 54): Verse("Judah", "towns", (
        N("Humtah", UNPLACED, "", (), note="Unidentified."),
        N("Kiriath Arba", SITE, "hebron"),
        N("Hebron", SITE, "hebron"),
        N("Zior", SITE, "zior"),
    ), count="nine cities with their villages"),
    (15, 55): Verse("Judah", "towns", (
        N("Maon", SITE, "maon_judah"),
        N("Carmel", SITE, "carmel_judah"),
        N("Ziph", SITE, "ziph_judah"),
        N("Jutah", SITE, "juttah"),
    )),
    (15, 56): Verse("Judah", "towns", (
        N("Jezreel", UNPLACED, "", (), note="Jezreel of Judah, near Maon and Carmel, is unidentified (Ahinoam's town, 1 Sam 25:43)."),
        N("Jokdeam", UNPLACED, ""),
        N("Zanoah", UNPLACED, "", (), note="The hill-country Zanoah."),
    )),
    (15, 57): Verse("Judah", "towns", (
        N("Kain", UNPLACED, ""),
        N("Gibeah", UNPLACED, "", (), note="Gibeah of Judah is unidentified."),
        N("Timnah", UNPLACED, "", (), note="The hill-country Timnah, south-east of Hebron, is unidentified."),
    ), count="ten cities with their villages"),
    (15, 58): Verse("Judah", "towns", (
        N("Halhul", SITE, "halhul"),
        N("Beth Zur", SITE, "beth_zur"),
        N("Gedor", UNPLACED, ""),
    )),
    (15, 59): Verse("Judah", "towns", (
        N("Maarath", SITE, "maarath"),
        N("Beth Anoth", SITE, "beth_anoth"),
        N("Eltekon", UNPLACED, "", (), note="Unidentified. Not eltekeh (Dan)."),
    ), count="six cities with their villages"),
    (15, 60): Verse("Judah", "towns", (
        N("Kiriath Baal", SITE, "kiriath_jearim"),
        N("Kiriath Jearim", SITE, "kiriath_jearim"),
        N("Rabbah", UNPLACED, "", (), note="Rabbah of Judah, near Kiriath Jearim, is unidentified."),
    ), count="two cities with their villages"),
    (15, 61): Verse("Judah", "towns", (
        N("wilderness", REGION, "judah"),
        N("Beth Arabah", UNPLACED, "", (), note="In UNPLACED (Josh 16-18 note): candidates exist, none settled."),
        N("Middin", UNPLACED, "", (), note="In UNPLACED (Josh 15:61-62 note): tied to the Buqei'a forts only by debated proposals."),
        N("Secacah", UNPLACED, "", (), note="In UNPLACED (Josh 15:61-62 note): debated proposals only."),
    )),
    (15, 62): Verse("Judah", "towns", (
        N("Nibshan", UNPLACED, "", (), note="In UNPLACED (Josh 15:61-62 note): debated proposals only."),
        N("City of Salt", UNPLACED, "", (), note="In UNPLACED (Josh 15:61-62 note): debated, sometimes put at Qumran."),
        N("En Gedi", SITE, "en_gedi"),
    ), count="six cities with their villages"),
    (15, 63): Verse("Judah", "story", (
        N("Jerusalem", SITE, "jerusalem"),
        N("Jerusalem", SITE, "jerusalem"),
    )),
    (16, 1): Verse("Ephraim", "border", (
        N("Jordan", WATER, "jordan", (31.8742, 35.5408)),
        N("Jericho", SITE, "jericho"),
        N("waters of Jericho", SITE, "jericho"),
        N("wilderness", UNPLACED, "", (), note="The wilderness between Jericho and Bethel (the wilderness of Beth Aven, 18:12). There's no region or point for it"),
        N("hill country", UNPLACED, "", (), note="Here it is only a general word for the hills between Jericho and Bethel"),
        N("Bethel", SITE, "bethel"),
    ), walk=("Jordan", "Jericho", "waters of Jericho", "Bethel")),
    (16, 2): Verse("Ephraim", "border", (
        N("Bethel", SITE, "bethel"),
        N("Luz", SITE, "bethel"),
        N("Archites", UNPLACED, "", (), note="'The border of the Archites' is a clan's district (Hushai the Archite's clan), somewhere between Bethel and Ataroth. It has no site"),
        N("Ataroth", UNPLACED, "", (), note="Probably Ataroth Addar (16:5; 18:13), which UNPLACED lists as having candidates but none settled."),
    ), walk=("Bethel", "Luz", "Archites", "Ataroth"), cont=True),
    (16, 3): Verse("Ephraim", "border", (
        N("Japhletites", UNPLACED, "", (), note="A clan's district (cf. Japhlet, 1 Chr 7:32-33). Unknown"),
        N("Beth Horon the lower", SITE, "beth_horon_lower"),
        N("Gezer", SITE, "gezer"),
        N("sea", WATER, "great_sea", (31.9419, 34.7073), note="where the line west from Gezer meets the coast. The text names no point there. This is the first COAST point north of Yavne-Yam (the end of Judah's border at Jabneel, 15:11): the Nahal Sorek (Rubin) mouth"),
    ), walk=("Japhletites", "Beth Horon the lower", "Gezer", "sea"), cont=True),
    (16, 4): Verse("", "summary", ()),
    (16, 5): Verse("Ephraim", "border", (
        N("Ataroth Addar", UNPLACED, "", (), note="UNPLACED: candidates exist (Khirbet Raddana, Tell en-Nasbeh, Khirbet ed-Dariya), but none is settled"),
        N("Beth Horon the upper", SITE, "beth_horon_upper"),
    ), walk=("Ataroth Addar", "Beth Horon the upper")),
    (16, 6): Verse("Ephraim", "border", (
        N("Michmethath", UNPLACED, "", (), note="UNPLACED: 'before Shechem' (17:7). Khirbet Makhneh el-Foqa and Khirbet Juleijil are proposed, and none is settled"),
        N("Taanath Shiloh", SITE, "taanath_shiloh"),
        N("Janoah", SITE, "janoah_ephraim"),
    ), walk=("Michmethath", "Taanath Shiloh", "Janoah")),
    (16, 7): Verse("Ephraim", "border", (
        N("Janoah", SITE, "janoah_ephraim"),
        N("Ataroth", UNPLACED, "", (), note="This eastern Ataroth, between Janoah and Naarah, is a different place from Ataroth Addar. Tell Sheikh edh-Dhiab and Khirbet el-Oga are proposed; neither is agreed and neither has a point"),
        N("Naarah", UNPLACED, "", (), note="UNPLACED (Naarath; Tell el-Jisr or Khirbet el-Ayash by Ain Duq are proposed)"),
        N("Jericho", SITE, "jericho"),
        N("Jordan", WATER, "jordan", (31.8742, 35.5408)),
    ), walk=("Janoah", "Ataroth", "Naarah", "Jericho", "Jordan"), cont=True),
    (16, 8): Verse("Ephraim", "border", (
        N("Tappuah", SITE, "tappuah"),
        N("brook of Kanah", UNPLACED, "", (), note="Wadi Qana (Nahal Kana), which runs into the Yarkon, is the agreed identification."),
        N("sea", WATER, "great_sea", (32.1039, 34.7758), note="the Kanah runs into the Yarkon, so the border reaches the sea at the Yarkon mouth (COAST)"),
    ), walk=("Tappuah", "brook of Kanah", "sea")),
    (16, 9): Verse("Ephraim", "summary", ()),
    (16, 10): Verse("Ephraim", "story", (
        N("Gezer", SITE, "gezer"),
    )),
    (17, 1): Verse("Manasseh", "summary", (
        N("Gilead", REGION, "gilead"),
        N("Bashan", REGION, "bashan"),
    )),
    (17, 2): Verse("Manasseh", "story", ()),
    (17, 3): Verse("Manasseh", "story", ()),
    (17, 4): Verse("Manasseh", "story", ()),
    (17, 5): Verse("Manasseh", "summary", (
        N("Gilead", REGION, "gilead"),
        N("Bashan", REGION, "bashan"),
        N("Jordan", WATER, "jordan", (32.1026, 35.5351)),
    ), count="Ten parts"),
    (17, 6): Verse("Manasseh", "summary", (
        N("Gilead", REGION, "gilead"),
    )),
    (17, 7): Verse("Manasseh", "border", (
        N("Asher", UNPLACED, "", (), note="Read either as the tribe's land or as a town Asher (Eusebius' Aser on the Shechem-Scythopolis road, put at Teyasir). There's no agreed site"),
        N("Michmethath", UNPLACED, "", (), note="UNPLACED (see 16:6)"),
        N("Shechem", SITE, "shechem"),
        N("En Tappuah", SITE, "tappuah"),
    ), walk=("Asher", "Michmethath", "En Tappuah")),
    (17, 8): Verse("Manasseh", "summary", (
        N("Tappuah", SITE, "tappuah"),
        N("Tappuah", SITE, "tappuah"),
    )),
    (17, 9): Verse("Manasseh", "border", (
        N("brook of Kanah", UNPLACED, ""),
        N("sea", WATER, "great_sea", (32.1039, 34.7758), note="where the Kanah, through the Yarkon, reaches the sea: the Yarkon mouth (COAST)"),
    ), walk=("brook of Kanah", "sea"), cont=True),
    (17, 10): Verse("Manasseh", "summary", (
        N("sea", WATER, "great_sea", (32.5023, 34.8892), note="'the sea was his border': Manasseh's coast, from the Yarkon to Dor. The middle of that stretch is Caesarea, Herod's harbour (COAST)"),
        N("Asher", UNPLACED, "", (), note="The tribe's territory, to the north. Gazetteer has no region for a tribe"),
        N("Issachar", UNPLACED, "", (), note="The tribe's territory, to the east. Gazetteer has no region for a tribe"),
    )),
    (17, 11): Verse("Manasseh", "towns", (
        N("three heights", UNPLACED, "", (), note="Hebrew 'the three Napheth' (cf. Naphoth Dor, 11:2; 12:23). It is read variously, either as a third district or as Dor's heights, and is not three named places"),
        N("Issachar", UNPLACED, "", (), note="The tribe's territory. Gazetteer has no region for it"),
        N("Asher", UNPLACED, "", (), note="The tribe's territory. Gazetteer has no region for it"),
        N("Beth Shean", SITE, "beth_shean"),
        N("Ibleam", SITE, "ibleam"),
        N("Dor", SITE, "dor"),
        N("Endor", SITE, "endor"),
        N("Taanach", SITE, "taanach"),
        N("Megiddo", SITE, "megiddo"),
    ), count="three heights"),
    (17, 12): Verse("Manasseh", "story", ()),
    (17, 13): Verse("Manasseh", "story", ()),
    (17, 14): Verse("", "story", ()),
    (17, 15): Verse("", "story", (
        N("land of the Perizzites", UNPLACED, "", (), note="A people's land, the wooded hills. It has no region or point"),
        N("Rephaim", UNPLACED, "", (), note="'the land of ... the Rephaim': the people, not the valley of Rephaim (18:16). It has no point"),
        N("hill country of Ephraim", REGION, "samaria"),
    )),
    (17, 16): Verse("", "story", (
        N("hill country", REGION, "samaria"),
        N("land of the valley", UNPLACED, "", (), note="A general term for the lowland plains, which the verse goes on to name as Beth Shean and the valley of Jezreel"),
        N("Beth Shean", SITE, "beth_shean"),
        N("valley of Jezreel", SITE, "jezreel_issachar"),
    )),
    (17, 17): Verse("", "story", ()),
    (17, 18): Verse("", "story", (
        N("hill country", REGION, "samaria"),
    )),
    (18, 1): Verse("", "story", (
        N("Shiloh", SITE, "shiloh"),
    )),
    (18, 2): Verse("", "story", (), count="Seven tribes"),
    (18, 3): Verse("", "story", ()),
    (18, 4): Verse("", "story", (), count="three men from each tribe"),
    (18, 5): Verse("", "story", (), count="seven portions"),
    (18, 6): Verse("", "story", (), count="seven parts"),
    (18, 7): Verse("", "story", (
        N("Jordan", WATER, "jordan", (32.1026, 35.5351)),
    )),
    (18, 8): Verse("", "story", (
        N("Shiloh", SITE, "shiloh"),
    )),
    (18, 9): Verse("", "story", (
        N("Shiloh", SITE, "shiloh"),
    ), count="seven portions"),
    (18, 10): Verse("", "story", (
        N("Shiloh", SITE, "shiloh"),
    )),
    (18, 11): Verse("Benjamin", "summary", ()),
    (18, 12): Verse("Benjamin", "border", (
        N("Jordan", WATER, "jordan", (31.8742, 35.5408)),
        N("Jericho", SITE, "jericho"),
        N("hill country", UNPLACED, "", (), note="Here it is only a general word for the hills west of Jericho"),
        N("wilderness of Beth Aven", UNPLACED, "", (), note="UNPLACED: Beth Aven is near Ai, east of Bethel, and Tell Maryam and Burqa are proposed. bethel already skips this verse"),
    ), walk=("Jordan", "Jericho", "wilderness of Beth Aven")),
    (18, 13): Verse("Benjamin", "border", (
        N("Luz", SITE, "bethel"),
        N("Bethel", SITE, "bethel"),
        N("Ataroth Addar", UNPLACED, "", (), note="UNPLACED (see 16:5)"),
        N("the mountain that lies on the south of Beth Horon the lower", UNPLACED, "", (), note="An unnamed ridge just south of Lower Beth Horon"),
        N("Beth Horon the lower", SITE, "beth_horon_lower"),
    ), walk=("Luz", "Ataroth Addar", "the mountain that lies on the south of Beth Horon the lower", "Beth Horon the lower"), cont=True),
    (18, 14): Verse("Benjamin", "border", (
        N("the mountain that lies before Beth Horon southward", UNPLACED, "", (), note="The same unnamed ridge as in 18:13"),
        N("Beth Horon", SITE, "beth_horon_lower"),
        N("Kiriath Baal", SITE, "kiriath_jearim"),
        N("Kiriath Jearim", SITE, "kiriath_jearim"),
    ), walk=("the mountain that lies before Beth Horon southward", "Beth Horon", "Kiriath Baal"), cont=True),
    (18, 15): Verse("Benjamin", "border", (
        N("Kiriath Jearim", SITE, "kiriath_jearim"),
        N("spring of the waters of Nephtoah", SITE, "nephtoah"),
    ), walk=("Kiriath Jearim", "spring of the waters of Nephtoah"), cont=True),
    (18, 16): Verse("Benjamin", "border", (
        N("the mountain that lies before the valley of the son of Hinnom", UNPLACED, "", (), note="The unnamed ridge west of the Hinnom valley, at the north end of the valley of Rephaim. It has no point"),
        N("valley of the son of Hinnom", SITE, "valley_of_hinnom"),
        N("valley of Rephaim", SITE, "valley_of_rephaim"),
        N("valley of Hinnom", SITE, "valley_of_hinnom"),
        N("the Jebusite", SITE, "jerusalem"),
        N("En Rogel", SITE, "en_rogel"),
    ), walk=("the mountain that lies before the valley of the son of Hinnom", "valley of Hinnom", "the Jebusite", "En Rogel"), cont=True),
    (18, 17): Verse("Benjamin", "border", (
        N("En Shemesh", UNPLACED, ""),
        N("Geliloth", UNPLACED, "", (), note="Unknown. It is often taken as the same as the Gilgal 'that faces the ascent of Adummim' in 15:7, which is not Joshua's Gilgal by Jericho"),
        N("ascent of Adummim", SITE, "ascent_of_adummim"),
        N("stone of Bohan", UNPLACED, "", (), note="'The stone of Bohan the son of Reuben' is an unidentified landmark on the slope down to the Jordan plain"),
    ), walk=("En Shemesh", "Geliloth", "stone of Bohan"), cont=True),
    (18, 18): Verse("Benjamin", "border", (
        N("Arabah", UNPLACED, "", (), note="The Jordan plain by Beth Hoglah, north of the Salt Sea; the Arabah of the atlas lies south of the sea."),
    ), walk=("Arabah",), cont=True),
    (18, 19): Verse("Benjamin", "border", (
        N("Beth Hoglah", SITE, "beth_hoglah"),
        N("Salt Sea", WATER, "salt_sea", (31.7614, 35.5583)),
        N("Jordan", WATER, "jordan", (31.7614, 35.5583)),
    ), walk=("Beth Hoglah", "Salt Sea", "Jordan"), cont=True),
    (18, 20): Verse("Benjamin", "border", (
        N("Jordan", WATER, "jordan", (31.8371, 35.5465), note="the eastern border, which is the river from the Salt Sea's mouth up to opposite Jericho."),
    ), walk=("Jordan",), cont=True),
    (18, 21): Verse("Benjamin", "towns", (
        N("Jericho", SITE, "jericho"),
        N("Beth Hoglah", SITE, "beth_hoglah"),
        N("Emek Keziz", UNPLACED, "", (), note="Unknown. It was perhaps in the Jordan plain near Jericho, but it has no proposed site with a point"),
    )),
    (18, 22): Verse("Benjamin", "towns", (
        N("Beth Arabah", UNPLACED, "", (), note="UNPLACED ('Ain el-Gharabeh is proposed)"),
        N("Zemaraim", UNPLACED, "", (), note="UNPLACED (Ras ez-Zeimara is proposed; cf. Mount Zemaraim, 2 Chr 13:4)"),
        N("Bethel", SITE, "bethel"),
    )),
    (18, 23): Verse("Benjamin", "towns", (
        N("Avvim", UNPLACED, "", (), note="Unknown. Some take it for Ai (Aiath); not the Avvim people of Deut 2:23 and Josh 13:3"),
        N("Parah", SITE, "parah"),
        N("Ophrah", SITE, "ophrah_benjamin"),
    )),
    (18, 24): Verse("Benjamin", "towns", (
        N("Chephar Ammoni", UNPLACED, "", (), note="Unknown. Kafr 'Ana north of Bethel has been suggested, but there is no agreement and no point"),
        N("Ophni", UNPLACED, "", (), note="UNPLACED."),
        N("Geba", SITE, "geba"),
    ), count="twelve cities with their villages"),
    (18, 25): Verse("Benjamin", "towns", (
        N("Gibeon", SITE, "gibeon"),
        N("Ramah", SITE, "ramah_benjamin"),
        N("Beeroth", UNPLACED, "", (), note="UNPLACED: el-Bireh, Nebi Samwil, Khirbet el-Burj and Biddu are all proposed"),
    )),
    (18, 26): Verse("Benjamin", "towns", (
        N("Mizpeh", SITE, "mizpah_benjamin"),
        N("Chephirah", SITE, "chephirah"),
        N("Mozah", SITE, "emmaus"),
    )),
    (18, 27): Verse("Benjamin", "towns", (
        N("Rekem", UNPLACED, "", (), note="Unknown. Not the Midianite king Rekem (Num 31:8; Josh 13:21) or the Judahite Rekem (1 Chr 2:43-44)"),
        N("Irpeel", UNPLACED, "", (), note="Unknown (Rafat north of Jerusalem has been suggested), with no agreed site or point"),
        N("Taralah", UNPLACED, "", (), note="Unknown"),
    )),
    (18, 28): Verse("Benjamin", "towns", (
        N("Zelah", UNPLACED, "", (), note="UNPLACED (also Saul's family tomb, 2 Sam 21:14)"),
        N("Eleph", UNPLACED, "", (), note="UNPLACED. Some read 'Zelah Eleph' as one name"),
        N("the Jebusite", SITE, "jerusalem"),
        N("Jerusalem", SITE, "jerusalem"),
        N("Gibeath", SITE, "gibeah_benjamin"),
        N("Kiriath", SITE, "kiriath_jearim"),
    ), count="fourteen cities with their villages"),
    (19, 1): Verse("Simeon", "summary", (
        N("Judah", UNPLACED, "", (), note="the inheritance of the children of Judah (Josh 15), Judah's whole allotment with the Negev; REGIONS judah stands only for the hill country and its wilderness, so it is not used here"),
    )),
    (19, 2): Verse("Simeon", "towns", (
        N("Beersheba", SITE, "beersheba"),
        N("Sheba", SITE, "beersheba"),
        N("Moladah", UNPLACED, ""),
    )),
    (19, 3): Verse("Simeon", "towns", (
        N("Hazar Shual", UNPLACED, "", (), note="unidentified; UNPLACED (Negev towns of Josh 15:21-32 and 19:2-7)"),
        N("Balah", UNPLACED, "", (), note="Baalah of Josh 15:29 or Bilhah of 1 Chr 4:29; unidentified"),
        N("Ezem", UNPLACED, ""),
    )),
    (19, 4): Verse("Simeon", "towns", (
        N("Eltolad", UNPLACED, "", (), note="unidentified (Tolad in 1 Chr 4:29)"),
        N("Bethul", UNPLACED, ""),
        N("Hormah", SITE, "hormah"),
    )),
    (19, 5): Verse("Simeon", "towns", (
        N("Ziklag", SITE, "ziklag"),
        N("Beth Marcaboth", UNPLACED, "", (), note="unidentified (perhaps Madmannah of Josh 15:31)"),
        N("Hazar Susah", UNPLACED, "", (), note="unidentified (perhaps Sansannah of Josh 15:31); Sbalat Abu Susein is only a guess from the name"),
    )),
    (19, 6): Verse("Simeon", "towns", (
        N("Beth Lebaoth", UNPLACED, "", (), note="Lebaoth of Josh 15:32; unidentified"),
        N("Sharuhen", SITE, "sharuhen"),
    ), count="thirteen cities with their villages"),
    (19, 7): Verse("Simeon", "towns", (
        N("Ain", UNPLACED, "", (), note="Ain and Rimmon (En Rimmon, Neh 11:29) are debated, with Tel Halif and Khirbet Umm er-Ramamin proposed; UNPLACED (Negev towns)"),
        N("Rimmon", UNPLACED, ""),
        N("Ether", UNPLACED, ""),
        N("Ashan", UNPLACED, ""),
    ), count="four cities with their villages"),
    (19, 8): Verse("Simeon", "towns", (
        N("Baalath Beer", UNPLACED, "", (), note="the same place as Ramah of the South, the southern limit of Simeon's villages; unidentified"),
        N("Ramah of the South", UNPLACED, ""),
    )),
    (19, 9): Verse("Simeon", "summary", (
        N("Judah", UNPLACED, "", (), note="the part, or portion, of the children of Judah: Judah's allotment, not a REGIONS point"),
    )),
    (19, 10): Verse("Zebulun", "border", (
        N("Sarid", SITE, "sarid"),
    ), walk=("Sarid",)),
    (19, 11): Verse("Zebulun", "border", (
        N("Maralah", UNPLACED, "", (), note="debated (Tell Ghalta or Tel Shor proposed); UNPLACED (Zebulun)"),
        N("Dabbesheth", UNPLACED, "", (), note="debated (Tell esh-Shammam proposed); UNPLACED (Zebulun)"),
        N("the brook that is before Jokneam", WATER, "kishon", (32.6853, 35.1097), note="The Kishon where it passes Jokneam: the RIVERS['kishon'] point at Tel Qashish, on the north bank about 2 km from Tel Yokneam. Most atlases (Aharoni among them) take the brook to be the Kishon; some take it for the Wadi el-Milh."),
        N("Jokneam", SITE, "jokneam"),
    ), walk=("Maralah", "Dabbesheth", "the brook that is before Jokneam"), cont=True),
    (19, 12): Verse("Zebulun", "border", (
        N("Sarid", SITE, "sarid"),
        N("Chisloth Tabor", SITE, "chesulloth"),
        N("Daberath", SITE, "daberath"),
        N("Japhia", SITE, "japhia"),
    ), walk=("Sarid", "Chisloth Tabor", "Daberath", "Japhia")),
    (19, 13): Verse("Zebulun", "border", (
        N("Gath Hepher", SITE, "gath_hepher"),
        N("Ethkazin", UNPLACED, "", (), note="unidentified; UNPLACED (Zebulun)"),
        N("Rimmon", SITE, "rimmon_zebulun"),
        N("Neah", UNPLACED, "", (), note="unidentified; UNPLACED (Zebulun)"),
    ), walk=("Gath Hepher", "Ethkazin", "Rimmon", "Neah"), cont=True),
    (19, 14): Verse("Zebulun", "border", (
        N("Hannathon", SITE, "hannathon"),
        N("valley of Iphtah El", UNPLACED, "", (), note="often taken as Wadi el-Malik or the Beth Netofa valley, but no point; UNPLACED (Zebulun)"),
    ), walk=("Hannathon", "valley of Iphtah El"), cont=True),
    (19, 15): Verse("Zebulun", "towns", (
        N("Kattath", UNPLACED, "", (), note="unidentified (perhaps Kitron, Judg 1:30); UNPLACED (Zebulun)"),
        N("Nahalal", UNPLACED, "", (), note="debated (Tell en-Nahl and Ma'lul are proposed); UNPLACED (Zebulun)"),
        N("Shimron", SITE, "shimron"),
        N("Idalah", UNPLACED, "", (), note="unidentified; UNPLACED (Zebulun)"),
        N("Bethlehem", SITE, "bethlehem_zebulun"),
    ), count="twelve cities with their villages"),
    (19, 16): Verse("Zebulun", "summary", ()),
    (19, 17): Verse("Issachar", "summary", ()),
    (19, 18): Verse("Issachar", "towns", (
        N("Jezreel", SITE, "jezreel_issachar"),
        N("Chesulloth", SITE, "chesulloth"),
        N("Shunem", SITE, "shunem"),
    )),
    (19, 19): Verse("Issachar", "towns", (
        N("Hapharaim", UNPLACED, "", (), note="debated (et-Taiyibeh proposed); UNPLACED (Issachar)"),
        N("Shion", UNPLACED, "", (), note="debated; UNPLACED (Issachar)"),
        N("Anaharath", UNPLACED, ""),
    )),
    (19, 20): Verse("Issachar", "towns", (
        N("Rabbith", UNPLACED, "", (), note="perhaps a corruption of Daberath (Josh 21:28); UNPLACED (Issachar)"),
        N("Kishion", SITE, "kishion"),
        N("Ebez", UNPLACED, "", (), note="unidentified; UNPLACED (Issachar)"),
    )),
    (19, 21): Verse("Issachar", "towns", (
        N("Remeth", UNPLACED, "", (), note="Ramoth or Jarmuth of Issachar (1 Chr 6:73; Josh 21:29); debated (Kokab el-Hawa proposed); UNPLACED (Issachar)"),
        N("Engannim", SITE, "en_gannim_issachar"),
        N("En Haddah", UNPLACED, "", (), note="debated (el-Hadatha proposed); UNPLACED (Issachar)"),
        N("Beth Pazzez", UNPLACED, "", (), note="unidentified; UNPLACED (Issachar)"),
    )),
    (19, 22): Verse("Issachar", "border", (
        N("Tabor", SITE, "mount_tabor"),
        N("Shahazumah", UNPLACED, "", (), note="unidentified; UNPLACED (Issachar)"),
        N("Beth Shemesh", UNPLACED, "", (), note="El-'Abeidiyeh, Tel Yin'am and Khirbet Sheikh esh-Shamsawi are all proposed, with none agreed."),
        N("Jordan", WATER, "jordan", (32.6889, 35.5617), note="Issachar's border ends on the Jordan between the lake and the Yarmuk, and el-'Abeidiyeh is one proposal for its Beth Shemesh."),
    ), walk=("Tabor", "Shahazumah", "Beth Shemesh", "Jordan"), count="sixteen cities with their villages"),
    (19, 23): Verse("Issachar", "summary", ()),
    (19, 24): Verse("Asher", "summary", ()),
    (19, 25): Verse("Asher", "border", (
        N("Helkath", UNPLACED, "", (), note="debated (Tell el-Qassis or Tell el-Harbaj proposed); UNPLACED (Asher)"),
        N("Hali", UNPLACED, "", (), note="debated; UNPLACED (Asher)"),
        N("Beten", UNPLACED, "", (), note="debated; UNPLACED (Asher)"),
        N("Achshaph", SITE, "achshaph"),
    ), walk=("Helkath", "Hali", "Beten", "Achshaph")),
    (19, 26): Verse("Asher", "border", (
        N("Allammelech", UNPLACED, "", (), note="unidentified; UNPLACED (Asher)"),
        N("Amad", UNPLACED, "", (), note="unidentified; UNPLACED (Asher)"),
        N("Mishal", UNPLACED, "", (), note="the levitical Mashal (Josh 21:30); debated; UNPLACED (Asher)"),
        N("Carmel", SITE, "mount_carmel"),
        N("Shihorlibnath", UNPLACED, "", (), note="a stream or place south of Carmel (Nahal Tanninim and the Kishon are proposed); UNPLACED (Asher)"),
    ), walk=("Allammelech", "Amad", "Mishal", "Carmel", "Shihorlibnath"), cont=True),
    (19, 27): Verse("Asher", "border", (
        N("Beth Dagon", UNPLACED, "", (), note="Beth Dagon of Asher, unidentified; UNPLACED (Asher)"),
        N("Zebulun", UNPLACED, "", (), note="Zebulun's allotment, where Asher's border touches it; REGIONS has no Zebulun"),
        N("valley of Iphtah El", UNPLACED, "", (), note="the same valley as v14; no point; UNPLACED (Zebulun)"),
        N("Beth Emek", UNPLACED, ""),
        N("Neiel", UNPLACED, "", (), note="debated (Khirbet Ya'nin proposed); UNPLACED (Asher)"),
        N("Cabul", SITE, "cabul"),
    ), walk=("Beth Dagon", "valley of Iphtah El", "Beth Emek", "Neiel", "Cabul"), cont=True),
    (19, 28): Verse("Asher", "border", (
        N("Ebron", UNPLACED, "", (), note="It is not in UNPLACED."),
        N("Rehob", UNPLACED, "", (), note="one of Asher's two Rehobs; debated; UNPLACED (Asher)"),
        N("Hammon", UNPLACED, ""),
        N("Kanah", SITE, "kanah_asher"),
        N("great Sidon", SITE, "sidon"),
    ), walk=("Ebron", "Rehob", "Hammon", "Kanah", "great Sidon"), cont=True),
    (19, 29): Verse("Asher", "border", (
        N("Ramah", UNPLACED, ""),
        N("Tyre", SITE, "tyre"),
        N("Hosah", UNPLACED, "", (), note="Usu of the Assyrian texts, on the mainland opposite Tyre (Tell Rashidiyeh proposed); UNPLACED (Asher)"),
        N("sea", WATER, "great_sea", (33.0481, 35.1017), note="The border 'ended at the sea by the region of Achzib'."),
        N("Achzib", SITE, "achzib_asher"),
    ), walk=("Ramah", "Tyre", "Hosah", "sea", "Achzib"), cont=True),
    (19, 30): Verse("Asher", "towns", (
        N("Ummah", UNPLACED, "", (), note="perhaps a slip for Acco (Judg 1:31); unidentified; UNPLACED (Asher)"),
        N("Aphek", SITE, "aphek_asher"),
        N("Rehob", UNPLACED, "", (), note="Asher's second Rehob; debated; UNPLACED (Asher)"),
    ), count="twenty-two cities with their villages"),
    (19, 31): Verse("Asher", "summary", ()),
    (19, 32): Verse("Naphtali", "summary", ()),
    (19, 33): Verse("Naphtali", "border", (
        N("Heleph", UNPLACED, "", (), note="debated (Khirbet 'Irbadeh by Tabor proposed); UNPLACED (Naphtali)"),
        N("the oak in Zaanannim", UNPLACED, "", (), note="also Judg 4:11; debated; UNPLACED (Naphtali)"),
        N("Adami-nekeb", UNPLACED, ""),
        N("Jabneel", UNPLACED, ""),
        N("Lakkum", UNPLACED, "", (), note="debated (Khirbet el-Mansurah near the lake's outlet proposed); UNPLACED (Naphtali)"),
        N("Jordan", WATER, "jordan", (32.7116, 35.5732), note="The southern border runs from Heleph east, by Jabneel and Lakkum, to the river below the lake."),
    ), walk=("Heleph", "the oak in Zaanannim", "Adami-nekeb", "Jabneel", "Lakkum", "Jordan")),
    (19, 34): Verse("Naphtali", "border", (
        N("Aznoth Tabor", UNPLACED, ""),
        N("Hukkok", SITE, "hukkok"),
        N("Zebulun", UNPLACED, "", (), note="the neighbouring allotment on the south; REGIONS has no Zebulun"),
        N("Asher", UNPLACED, "", (), note="the neighbouring allotment on the west; REGIONS has no Asher"),
        N("Judah", UNPLACED, "", (), note="'to Judah at the Jordan' is a known crux: Judah's allotment does not touch Naphtali. The phrase is read as Havvoth-Jair, or the text is thought corrupt (the LXX lacks 'Judah'). REGIONS judah, in the Judean hills, would mislead here."),
        N("Jordan", WATER, "jordan", (33.0103, 35.6283)),
    ), walk=("Aznoth Tabor", "Hukkok")),
    (19, 35): Verse("Naphtali", "towns", (
        N("Ziddim", UNPLACED, "", (), note="The Talmud's Kefar Hittaya (Hattin) and Hajar ed-Damm are both proposed."),
        N("Zer", UNPLACED, "", (), note="unidentified (perhaps a dittography of Ziddim); not in UNPLACED"),
        N("Hammath", SITE, "hammath_naphtali"),
        N("Rakkath", UNPLACED, ""),
        N("Chinnereth", SITE, "chinnereth"),
    )),
    (19, 36): Verse("Naphtali", "towns", (
        N("Adamah", UNPLACED, ""),
        N("Ramah", SITE, "ramah_naphtali"),
        N("Hazor", SITE, "hazor_naphtali"),
    )),
    (19, 37): Verse("Naphtali", "towns", (
        N("Kedesh", SITE, "kedesh_naphtali"),
        N("Edrei", UNPLACED, "", (), note="Edrei of Naphtali, not the Bashan Edrei (edrei, at Daraa); unidentified; not in UNPLACED"),
        N("En Hazor", UNPLACED, ""),
    )),
    (19, 38): Verse("Naphtali", "towns", (
        N("Iron", SITE, "iron_naphtali"),
        N("Migdal El", UNPLACED, ""),
        N("Horem", UNPLACED, ""),
        N("Beth Anath", UNPLACED, "", (), note="several Upper Galilee candidates; UNPLACED"),
        N("Beth Shemesh", UNPLACED, ""),
    ), count="nineteen cities with their villages"),
    (19, 39): Verse("Naphtali", "summary", ()),
    (19, 40): Verse("Dan", "summary", ()),
    (19, 41): Verse("Dan", "towns", (
        N("Zorah", SITE, "zorah"),
        N("Eshtaol", SITE, "eshtaol"),
        N("Irshemesh", SITE, "beth_shemesh"),
    )),
    (19, 42): Verse("Dan", "towns", (
        N("Shaalabbin", SITE, "shaalbim"),
        N("Aijalon", SITE, "aijalon"),
        N("Ithlah", UNPLACED, "", (), note="no accepted identification; UNPLACED"),
    )),
    (19, 43): Verse("Dan", "towns", (
        N("Elon", UNPLACED, "", (), note="no accepted identification; UNPLACED"),
        N("Timnah", SITE, "timnah_dan"),
        N("Ekron", SITE, "ekron"),
    )),
    (19, 44): Verse("Dan", "towns", (
        N("Eltekeh", SITE, "eltekeh"),
        N("Gibbethon", SITE, "gibbethon"),
        N("Baalath", UNPLACED, "", (), note="no accepted identification; UNPLACED"),
    )),
    (19, 45): Verse("Dan", "towns", (
        N("Jehud", SITE, "jehud"),
        N("Bene Berak", SITE, "bene_berak"),
        N("Gath Rimmon", SITE, "gath_rimmon_dan"),
    )),
    (19, 46): Verse("Dan", "towns", (
        N("Me Jarkon", WATER, "yarkon", (32.1039, 34.7758)),
        N("Rakkon", UNPLACED, ""),
        N("Joppa", SITE, "joppa"),
    )),
    (19, 47): Verse("Dan", "story", (
        N("Leshem", SITE, "dan"),
        N("Dan", SITE, "dan"),
    )),
    (19, 48): Verse("Dan", "summary", ()),
    (19, 49): Verse("", "summary", ()),
    (19, 50): Verse("", "story", (
        N("Timnathserah", SITE, "timnathserah"),
        N("hill country of Ephraim", REGION, "samaria"),
    )),
    (19, 51): Verse("", "summary", (
        N("Shiloh", SITE, "shiloh"),
        N("Tent of Meeting", UNPLACED, "", (), note="the tabernacle pitched at Shiloh (Josh 18:1): a landmark at Shiloh's point, with no point of its own"),
    )),
}
