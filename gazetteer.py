"""The Land of Israel in (lat, lon): its coast, lakes, rivers and places,
for the reference atlas (generate_israel_atlas.py) and the verse maps to
come.

How it was made. As in acts_geography, every commented point of a line is
one named place (a town, cape, beach, river mouth, bridge, spring, dam or
ancient site) whose coordinate was taken as a single fact from Wikidata
(CC0, the item named in the comment) or Wikipedia. Points marked "~" are
our own interpolation. No line geometry was copied, traced or sampled from
OpenStreetMap, Google or any map or atlas. The coast is today's; the two
lakes that have shrunk are drawn at high water: the Salt Sea as it stood
early in the 20th century (about -390 m, the southern basin full), and Lake
Huleh before it was drained in the 1950s.

- **COAST** runs north to south with the land on the left: acts_geography's
  MAIN_COAST from Ras al-Misri, south of Beirut, to Ras Naqoura, then the
  points gathered here (2026-10-27) to the mouth of the brook of Egypt
  (Wadi el-Arish).
- **LAKES** are rings, not closed (the last point joins the first), with
  the water on the right.
- **RIVERS** run from source to mouth. A mouth is the matching coast, lake
  or river point, so the lines meet.
- **SITES** are the places the WEB names, each at the tell, ruin or village
  it is identified with (`qid`, its Wikidata item; `point` says which
  where it matters), with:
  - `certainty`: KNOWN (the name survives, or inscriptions or excavation
    fix it), PROBABLE (most scholars agree) or POSSIBLE (one proposal of
    several; `why` names the others);
  - `refs`: verses that name this place, each checked to contain the name
    or one of its WEB names. A namesake's verses are not among them, and
    `namesakes` says which are;
  - `tribe`, `levitical` and `refuge` from the town lists of Joshua 13-21;
  - `label`, where the drawing names it otherwise (Lod · Lydda), and
    `kind` (town, mount, valley, plain, cave, well);
  - `point`, what the dot marks where it matters (the tell, the village),
    and `source`, how the coordinate was chosen, for the record;
  - `skip`: the verses its names find in the WEB that are about something
    else (a namesake, a person, a word), so every other verse that names it
    is its own. Sorted verse by verse, and checked, on 2026-10-28.
- **JERUSALEM** holds places in or against the city, too close together to
  draw on the atlas.
- **WATERS** and **REGIONS** name the lines and lands with their verses:
  `find` is the pattern that finds them in the WEB (`skip`, the verses it
  wrongly finds). A region's lat/lon is only where the atlas writes its
  name, chosen by hand: no border is drawn.
- **UNPLACED** holds notes on the places left off: those with no agreed
  site or no point fact to put them at, and a few names the WEB doesn't use.
"""

from typing import NamedTuple

from acts_geography import MAIN_COAST as _MAIN_COAST

KNOWN, PROBABLE, POSSIBLE = "known", "probable", "possible"


class Site(NamedTuple):
    name: str
    lat: float
    lon: float
    qid: str
    certainty: str
    label: str = ""
    kind: str = "town"
    modern: str = ""
    point: str = ""
    why: str = ""
    aka: tuple = ()
    region: str = ""
    tribe: tuple = ()
    levitical: bool = False
    refuge: bool = False
    refs: str = ""
    namesakes: str = ""
    source: str = ""             # where the point came from, for the record
    skip: str = ""               # verses its names find that are about something else


class Water(NamedTuple):
    name: str
    lines: tuple
    find: str = ""
    skip: str = ""
    aka: tuple = ()
    note: str = ""


class Region(NamedTuple):
    name: str
    lat: float
    lon: float
    find: str = ""
    skip: str = ""
    aka: tuple = ()
    note: str = ""
    nt: bool = False             # a name of Jesus' day


# ===========================================================================
# The coast
# ===========================================================================

# acts_geography's coast south of Beirut, to Ras Naqoura
_NORTH = _MAIN_COAST[next(i for i, p in enumerate(_MAIN_COAST) if p[0] < 33.75):]

# Ras Naqoura (the end of _NORTH) south to the mouth of the brook of Egypt
COAST_SOUTH = [
    (33.0880, 35.1058),   # Misrephoth Maim (WEB Misrephoth Maim, Josh 11:8; 13:6) (Q7059481)
    (33.0761, 35.1064),   # Nahal Betzet (lower course at the shore) (Q2908288)
    (33.0481, 35.1017),   # Az-Zeeb, Achziv (WEB Achzib, Josh 19:29; Judg 1:31) (Q4831969)
    (33.0095, 35.0895),   # Nahariya (Canaanite temple on the beach) (Q114696301)
    (32.9796, 35.0822),   # Shavei Tzion (Q571191)
    (32.9592, 35.0758),   # Nahal Yasaf (lower course at the shore) (Q35498018)
    (32.9377, 35.0729),   # Acre, Northern Sea Promenade (Q107378660)
    (32.9193, 35.0665),   # Akko Light, SW tip of old Acre (WEB Acco, Judg 1:31; Ptolemais, Acts 21:7) (Q2891457)
    (32.9194, 35.0697),   # Acre Port (Q2985605)
    (32.9100, 35.0822),   # Na'aman (Belus) River mouth (Q2509879)
    (32.8408, 35.0575),   # Hof Yammit (beach, Kiryat Yam) (Q26771093)
    (32.8331, 35.0511),   # Kiryat Haim beach (Q26771094)
    (32.8227, 35.0359),   # Haifa Bay Port (Namal HaMifratz) (Q20502324)
    (32.8144, 35.0261),   # Kishon River mouth (WEB Kishon, Judg 5:21; 1 Kgs 18:40) (Q1743701)
    (32.8201, 35.0045),   # Port of Haifa (Q1376739)
    (32.8341, 34.9769),   # Bat Galim Casino (Bat Galim shore) (Q7001296)
    (32.8304, 34.9625),   # Rosh HaKarmel, Cape Carmel below Stella Maris (WEB Carmel, Josh 19:26) (Q26763723)
    (32.8249, 34.9553),   # Tel Shikmona (Q2919810)
    (32.8061, 34.9567),   # Khayat Beach (Q84564737)
    (32.7469, 34.9511),   # Tel Hreiz (Kfar Galim shore) (Q49004181)
    (32.7237, 34.9477),   # Tel Megadim (Tel Sahar) (Q6954831)
    (32.7085, 34.9408),   # Atlit beach (Q6807372)
    (32.7053, 34.9339),   # Atlit, Chateau Pelerin (headland) (Q597606)
    (32.6936, 34.9283),   # Neve Yam coast reserve (Q26769758)
    (32.6700, 34.9286),   # Nahal Me'arot mouth (Q79354422)
    (32.6419, 34.9242),   # Dor Habonim Beach (Q7069023)
    (32.6174, 34.9164),   # Tel Dor, beside Tantura (WEB Dor, Josh 17:11; Judg 1:27; 1 Kgs 4:11) (Q1243563)
    (32.5889, 34.9150),   # Nahal Daliya mouth (Q7217998)
    (32.5396, 34.9020),   # Nahal Taninim mouth (Q972150)
    (32.5211, 34.9003),   # Caesarea Beach National Park (aqueduct beach) (Q26771066)
    (32.5023, 34.8892),   # Caesarea, Herod's harbour (WEB Caesarea, Acts 10:1) (Q55649272)
    (32.4907, 34.8929),   # Sdot Yam (Q1325255)
    (32.4643, 34.8835),   # Hadera Stream mouth (Q2498901)
    (32.4461, 34.8781),   # Hof Zevulun (beach, Givat Olga) (Q26771053)
    (32.4286, 34.8744),   # Tel Gador (Q49004173)
    (32.4025, 34.8661),   # Mikhmoret, Abu Zabura harbour (Q87751771)
    (32.3958, 34.8653),   # Alexander River mouth (Q1962200)
    (32.3797, 34.8631),   # Beit Yanai (Q2920020)
    (32.3686, 34.8606),   # Neurim Beach National Park (Q26771042)
    (32.3306, 34.8506),   # Netanya, Independence Square (on the cliff) (Q6967386)
    (32.2681, 34.8357),   # Poleg Stream mouth (Q2578736)
    (32.2436, 34.8258),   # Hof HaSharon National Park (cliffs) (Q12041645)
    (32.1952, 34.8068),   # Apollonia (Arsuf) (Q1024886)
    (32.1736, 34.8003),   # Zvulun Beach, Herzliya (Q30184246)
    (32.1592, 34.7978),   # Tel Michal (Herzliya) (Q6448087)
    (32.1306, 34.7878),   # Tel Rakit (Tel Baruch shore) (Q12412096)
    (32.1039, 34.7758),   # Yarkon River mouth (WEB Me Jarkon, Josh 19:46) (Q927016)
    (32.0978, 34.7732),   # Tel Aviv Port (Q2889387)
    (32.0905, 34.7692),   # Hilton Beach, Tel Aviv (Q56376795)
    (32.0746, 34.7645),   # Jerusalem Beach, Tel Aviv (Q56377589)
    (32.0653, 34.7611),   # Charles Clore Park (Q2776516)
    (32.0536, 34.7494),   # Jaffa Port (WEB Joppa, Jonah 1:3; Acts 9:36) (Q2911475)
    (32.0364, 34.7472),   # Givat Aliyah, Jaffa (Q2897142)
    (32.0217, 34.7387),   # Bat Yam Seafront (Q105979237)
    (31.9962, 34.7325),   # Tel Yona (Q6913764)
    (31.9419, 34.7073),   # Nahal Sorek (Rubin) mouth (Q252254)
    (31.9303, 34.7008),   # Palmachim beach (Q7212122)
    (31.9228, 34.6933),   # Yavne-Yam (Q5115556)
    (31.9074, 34.6890),   # Mesad Hashavyahu (Q5115690)
    (31.8474, 34.6509),   # HaDarom Port, Ashdod (Q20502320)
    (31.8303, 34.6413),   # Port of Ashdod (Q2914934)
    (31.8153, 34.6408),   # Lachish River mouth (Q131192605)
    (31.7947, 34.6281),   # Ashdod Marina (Q4804770)
    (31.7803, 34.6222),   # Ashdod-Yam (fortress) (Q1068119)
    (31.7411, 34.5992),   # Nahal Evtah mouth (Nitzanim) (Q2897190)
    (31.6821, 34.5560),   # Ashkelon Marina (Q6578434)
    (31.6619, 34.5461),   # Ascalon, ancient city (WEB Ashkelon, Judg 1:18) (Q104664899)
    (31.6369, 34.5267),   # Ashkelon desalination plant (Q6973244)
    (31.6128, 34.5044),   # Zikim Beach (Q123753331)
    (31.5410, 34.4520),   # Anthedon (Q2377463)
    (31.5322, 34.4454),   # Al-Shati camp (Q2829277)
    (31.5252, 34.4311),   # Port of Gaza (WEB Gaza, Judg 16:1; the city lies inland) (Q7231144)
    (31.5134, 34.4281),   # Sheikh Ijlin (Q7492931)
    (31.4642, 34.3757),   # Wadi Gaza mouth (Q35256691)
    (31.4258, 34.3406),   # Deir al-Balah Camp (Q3021326)
    (31.4153, 34.3281),   # Tell Ruqeish (Q12203030)
    (31.4042, 34.3158),   # Tel Katifa (Q2909775)
    (31.3812, 34.2856),   # Tell Ridan (Q135691126)
    (31.3633, 34.2711),   # Shirat HaYam (Q2909110)
    (31.3525, 34.2586),   # Kfar Yam (former settlement on the Khan Yunis shore) (Q2909483)
    (31.3289, 34.2300),   # Al-Mawasi, Rafah (Q4702878)
    (31.3233, 34.2208),   # Al Qarya as-Suwaydiya (Rafah, at the border) (Q123376507)
    (31.2464, 34.0971),   # Dayan Rock (Sheikh Zuweid shore) (Q12219882)
    (31.1817, 33.9405),   # Atzmona (Sinai) (Q61125082)
    (31.1519, 33.8536),   # Neot Sinai (Q7217768)
    (31.1540, 33.8371),   # El Arish port (Q12246911)
    (31.1508, 33.8331),   # El Arish Lighthouse (Q115161263)
    (31.1457, 33.8065),   # Wadi al-Arish mouth (WEB brook of Egypt, Num 34:5; Josh 15:4, 47) (Q10719024)
]

COAST = _NORTH + COAST_SOUTH


# ===========================================================================
# Lakes, at high water
# ===========================================================================

# The sea of Galilee, clockwise from the Jordan's inflow: down the east
# shore, round the south end by the outflow at Degania, up the west shore
# past Tiberias, and east along the north shore.
GALILEE = [
    (32.8962, 35.6117),   # Jordan inflow (mouth of the Jordan into the Sea of Galilee) (Q132237279)
    (32.8933, 35.6192),   # el-Araj, at the Jordan mouth (a Bethsaida candidate) (Q141807569)
    (32.8564, 35.6456),   # Hof Kinnar (Kinar beach) (Q26765696)
    (32.8517, 35.6478),   # Hof Dugit (Dugit beach) (Q26765694)
    (32.8411, 35.6486),   # Hof Ze'elon (beach north of Kursi) (Q26765691)
    (32.8194, 35.6450),   # Hof Halluqim (beach just south of Kursi) (Q26765699)
    (32.8094, 35.6428),   # Ein Gafra (shore spring) (Q26765685)
    (32.7903, 35.6394),   # Hof Susita (beach below Hippos) (Q26765689)
    (32.7856, 35.6358),   # Ein Gev harbour (Q136799639)
    (32.7653, 35.6383),   # Hof HaEla (beach) (Q26765703)
    (32.7567, 35.6361),   # Hof Kaneh (beach) (Q26765705)
    (32.7481, 35.6336),   # Hof Rotem (beach) (Q26765707)
    (32.7247, 35.6218),   # Ha'On (kibbutz on the south-east shore) (Q2889225)
    (32.7231, 35.6172),   # al-Samra (former shore village) (Q4703186)
    (32.7063, 35.5999),   # Ma'agan (kibbutz on the south shore) (Q2916656)
    (32.7064, 35.5892),   # Hof Tzemah (Samakh beach) (Q26764706)
    (32.7116, 35.5732),   # Degania Dam (the Jordan's outflow) (Q6843666)
    (32.7180, 35.5719),   # Khirbet Kerak / Beit Yerah (tell on the shore) (Q2063503)
    (32.7233, 35.5706),   # Hof Shaldag (beach) (Q26764704)
    (32.7342, 35.5700),   # Hof Tzinabri (beach) (Q26764702)
    (32.7417, 35.5686),   # Hof Shahaf (beach) (Q26764700)
    (32.7578, 35.5614),   # Hof Shikmim (beach) (Q26764699)
    (32.7667, 35.5511),   # Hamat Tiberias (Hammath, Josh 19:35) (Q2916538)
    (32.7753, 35.5469),   # Tiberias municipal beach (HaHof HaIroni) (Q26769118)
    (32.7866, 35.5432),   # Tiberias, old-city waterfront (Sea Mosque) (Q6557418)
    (32.7936, 35.5422),   # HaHof HaShaket, Tiberias (beach) (Q26769121)
    (32.8008, 35.5364),   # Hof HaDekel, Tiberias (beach) (Q26764691)
    (32.8064, 35.5256),   # Tel Raqqat (Rakkath, Josh 19:35) (Q107521937)
    (32.8214, 35.5181),   # Hof Migdala (beach) (Q26764690)
    (32.8250, 35.5156),   # Magdala / Tarichaea, the ruins on the shore (Q55634713)
    (32.8333, 35.5172),   # Villa Melchett, Migdal (on the shore) (Q12407117)
    (32.8394, 35.5228),   # Hof Tamar (beach) (Q26764685)
    (32.8443, 35.5252),   # Ginosar shore (the Sea of Galilee Boat) (Q7440096)
    (32.8650, 35.5389),   # Karei Deshe (on the shore south of Tabgha) (Q6786300)
    (32.8719, 35.5503),   # Tabgha (Church of the Primacy of St Peter, on the shore) (Q2109794)
    (32.8811, 35.5750),   # Capernaum (Q59174)
    (32.8869, 35.5869),   # Hof Sappirit (beach) (Q26764679)
    (32.8894, 35.5947),   # Amnon Bay (Q26764665)
]

# Lake Huleh before its draining, clockwise from the Jordan's outlet at the
# south tip: up the west shore, along the papyrus swamp's edge on the north,
# and down the east shore under the Golan.
HULEH = [
    (33.0406, 35.6292),   # Gesher HaPkak, the Jordan's outlet at the 'plug' at the lake's south end (Q7190334)
    (33.0509, 35.6199),   # Tulayl (former village on a hill by the lake) (Q7851976)
    (33.0589, 35.6161),   # Yesud HaMa'ala fishermen's pier (built by Hulata on the lake shore) (Q131354161)
    (33.0875, 35.6220),   # ~ north shore at the swamp edge, between the Hula reserve and al-Dirbashiyya
    (33.0889, 35.6470),   # al-Dirbashiyya (former village 'bordering Hula Lake', north-east corner) (Q4702346)
    (33.0703, 35.6356),   # mouth of Wadi al-Fajir (east shore) (Q34941815)
    (33.0553, 35.6408),   # Ein Ashmura (east-shore spring) (Q26764471)
    (33.0513, 35.6399),   # al-Dirdara / Dardara (on the lake's east shore) (Q4702345)
    (33.0453, 35.6318),   # mouth of Wadi Julaybina (south-east, near the outlet) (Q34942864)
]

# The Salt Sea at its early-20th-century high water, clockwise from the
# Jordan's mouth: down the Moab shore, round the Lisan, down the southern
# basin to its end, and north up the west shore past En Gedi.
SALT_SEA = [
    (31.7614, 35.5583),   # Jordan mouth (Q40059)
    (31.7690, 35.5761),   # mouth of Wadi al-'Uzaymi (north-east shore) (Q35241643)
    (31.7222, 35.5853),   # mouth of Wadi al-Mukhayris (Sweimeh shore) (Q49773205)
    (31.7042, 35.5825),   # mouth of Wadi ad-Dardur (Q49771701)
    (31.6803, 35.5736),   # mouth of Wadi al-Manshal (Q49772921)
    (31.6464, 35.5722),   # Madashsh Wadi Himarah (point at the Himara mouth) (Q27122911)
    (31.6225, 35.5667),   # mouth of Wadi Zarqa Ma'in (Q35297247)
    (31.5970, 35.5593),   # Ayn al-Zara (Callirrhoe) (Q11910919)
    (31.5782, 35.5576),   # mouth of Wadi Khashabah (Q49770827)
    (31.5508, 35.5539),   # mouth of Wadi 'Atun (Q35308108)
    (31.4931, 35.5644),   # mouth of Wadi Umm Ghuraybah (Q35293002)
    (31.4838, 35.5683),   # Al Mumallah (point) (Q27125265)
    (31.4671, 35.5634),   # mouth of the Arnon (Wadi Mujib) (Q697112)
    (31.4044, 35.5514),   # mouth of Wadi ash-Shuqayq (Q35245804)
    (31.3706, 35.5447),   # mouth of Wadi an-Nusur (Q49773689)
    (31.3461, 35.5453),   # mouth of Wadi al-Ajawid (Q49771888)
    (31.3319, 35.5453),   # mouth of Wadi Abu ad-Darat (Q49771276)
    (31.3106, 35.5550),   # mouth of Wadi al-Jarrah (Q49772460)
    (31.3039, 35.5272),   # Ghor al-Haditha (north side of the Lisan's neck) (Q27123739)
    (31.3500, 35.4833),   # Cape Costigan (the Lisan's north tip) (Q27124592)
    (31.2500, 35.4333),   # Cape Molineux (the Lisan's west tip, on the Lynch Strait) (Q27122522)
    (31.2651, 35.5280),   # al-Mazra'a / Ghor al-Mazra'a (south side of the Lisan's neck) (Q33766489)
    (31.2064, 35.5283),   # Wadi Uhaymir (south-east shore) (Q35295141)
    (31.1336, 35.5267),   # Wadi an-Numayrah, at Numeira (Q35242550)
    (31.0636, 35.4614),   # mouth of Wadi al-Hasa (the Zered) (Q35239366)
    (31.0264, 35.4567),   # Ghor es-Safi (the plain of Zoara / Zoar) (Q27121739)
    (30.9975, 35.4352),   # mouth of Wadi Arabah (the southern end, at the Sebkha) (Q35306136)
    (31.0725, 35.3982),   # Sodom potash works of 1934, at the foot of Mount Sodom on the southern basin's shore (Q12409398)
    (31.0849, 35.3957),   # Lot's Wife pillar, east face of Mount Sodom (Q24566570)
    (31.1106, 35.3892),   # Ein Shedim (spring at Mount Sodom's north end) (Q26764138)
    (31.1150, 35.3894),   # Ein Ashlag (spring) (Q26764137)
    (31.1521, 35.3652),   # Neve Zohar (Q2975481)
    (31.2000, 35.3639),   # Ein Bokek (Q679158)
    (31.3282, 35.3886),   # Bar Yehuda airfield, on the plain below Masada (-378 m, just above the old waterline) (Q1934910)
    (31.4188, 35.3769),   # Hamei Mazor (the Ein Gedi spa hot springs) (Q26763564)
    (31.4525, 35.3942),   # Hamei Yesha (hot spring below En Gedi) (Q26768856)
    (31.4617, 35.3997),   # Nahal Arugot (En Gedi shore) (Q1138503)
    (31.5125, 35.3883),   # Nahal Kedem (Q7218512)
    (31.5497, 35.4004),   # Mineral Beach (Q27499079)
    (31.5677, 35.4182),   # Lower Nahal Darga / Wadi Daraja (Murabba'at delta) (Q49771698)
    (31.6047, 35.4076),   # Einot Samar / 'Ayn at-Turabah (springs) (Q35241472)
    (31.6226, 35.4103),   # Ain el-Ghuweir (Einot Kane) (Q106087842)
    (31.6671, 35.4486),   # mouth of Wadi an-Nar (the Kidron) (Q35242686)
    (31.6818, 35.4425),   # Khirbet Mazin (Hasmonean anchorage) (Q6632565)
    (31.7146, 35.4504),   # Ein Feshkha ('Ayn Fashkhah spring) (Q35241797)
    (31.7455, 35.4794),   # mouth of Wadi Jawfat Zaban (the shore below Qumran) (Q35260497)
    (31.7733, 35.5078),   # Kalia beach (north shore) (Q6576987)
]

LAKES = {"galilee": GALILEE, "huleh": HULEH, "salt_sea": SALT_SEA}


# ===========================================================================
# Rivers, source to mouth
# ===========================================================================

# The Jordan's three headstreams meet north of Huleh
HASBANI = [
    (33.4141, 35.6878),   # Hasbani River source, above Hasbaya (the river item's source point) (Q1432225)
    (33.4086, 35.6728),   # Nahr al-Hasbani spring, west of Hasbaya (Q21569408)
    (33.3201, 35.6414),   # Meri (village in the Hasbani valley) (Q12238221)
    (33.2727, 35.6235),   # Ghajar (village on the Hasbani, by the Wazzani spring) (Q1261045)
    (33.2382, 35.6246),   # Hasbani (Nahal Snir) at the Snir reserve (the river item's own point) (Q1432225)
    (33.2252, 35.6245),   # HaGoshrim (Neolithic site on the Hasbani bank) (Q25488940)
    (33.1867, 35.6192),   # Confluence of the Hasbani and the Dan: source of the Jordan (Q40059)
]

DAN = [
    (33.2490, 35.6520),   # Dan springs at Tel Dan (the Dan River's source point) (Q393137)
    (33.2300, 35.6386),   # Dafna (kibbutz amid the Dan's streams) (Q545232)
    (33.1959, 35.6260),   # Banias joins the Dan, north of Sde Nehemia (Banias mouth) (Q1410413)
    (33.1867, 35.6192),   # Confluence of the Dan and the Hasbani: source of the Jordan (Q40059)
]

BANIAS = [
    (33.2484, 35.6945),   # Banias spring, below the cave of Pan (Banias River source) (Q1410413)
    (33.2410, 35.6819),   # Banias waterfall (Q106287995)
    (33.2164, 35.6406),   # Al-Mansura (former village on the Banias) (Q4702826)
    (33.1987, 35.6330),   # Al-'Abisiyya (former village by the Banias) (Q4702130)
    (33.1959, 35.6260),   # Banias mouth, joining the Dan (Q1410413)
]

# through Lake Huleh to the sea of Galilee
JORDAN_UPPER = [
    (33.1867, 35.6192),   # Source of the Jordan: confluence of the Hasbani and the Dan (Q40059)
    (33.1833, 35.6175),   # Gesher Yosef (bridge) (Q11855552)
    (33.1722, 35.6097),   # Kfar Blum (kibbutz on the Jordan) (Q1019478)
    (33.1033, 35.6092),   # Lake Huleh (the lake item's own point, at its northern marsh edge) (Q3215195)
    (33.0406, 35.6292),   # Gesher HaPkak, at the Huleh outlet (Q7190334)
    (33.0222, 35.6284),   # Jordan River Dureijat (riverbank site) (Q105592443)
    (33.0103, 35.6283),   # Daughters of Jacob Bridge (Jisr Banat Yaqub) (Q2916595)
    (32.9581, 35.6294),   # Khirbet a-Rafid (a few hundred m east of the river) (Q16132257)
    (32.9318, 35.6224),   # HaDodot Bridge (ford-bridge, near Karkom) (Q97216294)
    (32.9220, 35.6258),   # Khirbet ed-Dikke (synagogue on the east bank) (Q20740740)
    (32.9015, 35.6132),   # Arik Bridge (Q12405018)
    (32.8962, 35.6117),   # Mouth of the Jordan into the Sea of Galilee (Q132237279)
]

# the sea of Galilee to the Salt Sea
JORDAN_LOWER = [
    (32.7116, 35.5732),   # Degania Dam, at the Sea of Galilee outlet (Q6843666)
    (32.7023, 35.5631),   # Alumot Dam (Q6843294)
    (32.6889, 35.5617),   # Tell Ubeidiya (beside the river) (Q4702134)
    (32.6478, 35.5643),   # Yarmuk confluence at Naharayim (Yarmuk mouth) (Q849470)
    (32.6247, 35.5647),   # Jisr el-Majami (bridge), Gesher (Q20384748)
    (32.5906, 35.5750),   # Tel Kittan, west bank by the mouth of Nahal Tavor (Q26769803)
    (32.5667, 35.5638),   # Yardena (moshav on the Jordan) (Q2777486)
    (32.4969, 35.5756),   # Sheikh Hussein Bridge (Jordan River Crossing) (Q2671245)
    (32.4411, 35.5681),   # Confluence of Wadi 'Ayn Sa'dah (Q35307413)
    (32.4141, 35.5570),   # Confluence of Wadi Shubash (Nahal Bezeq) (Q7217870)
    (32.3889, 35.5542),   # Israel-Jordan-West Bank north tripoint, on the river (Q27391576)
    (32.3647, 35.5480),   # Ein Sukkot (spring by the border fence) (Q25496565)
    (32.3503, 35.5589),   # Confluence of Wadi al-Qarn (Q49773398)
    (32.3197, 35.5594),   # Confluence of Wadi Abu Kharrub (Q49771418)
    (32.2736, 35.5617),   # Confluence of Wadi Kufrinja (Q35267422)
    (32.2516, 35.5619),   # Confluence of Wadi Sadd al-Balqawi (Q35281750)
    (32.1916, 35.5620),   # Confluence of Wadi Abu Sidrah (Q49771544)
    (32.1153, 35.5431),   # Confluence of the Jabbok (Zarqa mouth) (Q798460)
    (32.1026, 35.5351),   # Damiya Bridge (Jisr ed-Damiye), by Adam (Q2916379)
    (31.9916, 35.5465),   # Zahrat Umm al-Awtad (east bank) (Q27121035)
    (31.8794, 35.5393),   # Confluence of Wadi Shu'ayb (Q4102306)
    (31.8742, 35.5408),   # Allenby Bridge (King Hussein Bridge) (Q712133)
    (31.8371, 35.5465),   # Qasr al-Yahud (baptism site) (Q1574073)
    (31.8011, 35.5481),   # King Abdullah Bridge (Q6411207)
    (31.7614, 35.5583),   # Mouth of the Jordan in the Dead Sea (Q40059)
]

YARMUK = [
    (32.7342, 35.8714),   # Al-Wehda Dam (Maqarin) (Q2635974)
    (32.7297, 35.8530),   # Yarmouk railway bridge (Q25498041)
    (32.7251, 35.8406),   # 'Ayn al-Habis (spring) (Q27123731)
    (32.7431, 35.7879),   # Tall Abu al-'Anatir (south bank) (Q27125513)
    (32.7417, 35.7506),   # Confluence of Wadi Ruqqad (Q2897196)
    (32.7090, 35.6932),   # Al-Yarmuk (village) (Q12251739)
    (32.6840, 35.6654),   # Hamat Gader (hot springs on the north bank) (Q2599137)
    (32.6794, 35.6467),   # Yarmuk valley glider bridge (railway) (Q107745802)
    (32.6478, 35.5643),   # Yarmuk mouth at Naharayim, into the Jordan (Q849470)
]

# from Rabbah (Amman) round by Zarqa and west to the Jordan
JABBOK = [
    (31.9344, 35.9231),   # Ras al-Ain, Amman: head of the Seil Amman (the stream item's point) (Q133278737)
    (31.9505, 35.9361),   # Nymphaeum of Amman (Rabbah), on the Seil (Q22948574)
    (31.9880, 35.9760),   # 'Ain Ghazal, where the Seil Amman meets the Zarqa (Q423625)
    (32.0178, 36.0464),   # Russeifa (Q2361176)
    (32.0874, 36.0708),   # Khirbet al-Batrawy (above the Zarqa, Zarqa city) (Q3814996)
    (32.1307, 36.0756),   # As-Sukhnah (El-Sokhna) (Q26678767)
    (32.2039, 36.0089),   # Kharaysin, at the Wadi Kharaysin confluence (Q24961074)
    (32.2254, 35.8948),   # Confluence of Wadi Jarash (Q35260158)
    (32.2156, 35.8649),   # Confluence of Wadi at-Tawahin (Q35248387)
    (32.1904, 35.7983),   # King Talal Dam (Q2898401)
    (32.1856, 35.6866),   # Tulul adh-Dhahab (twin tells either side of the Jabbok) (Q656842)
    (32.1948, 35.6490),   # Tell Hammeh, where the Zarqa valley opens into the Jordan valley (Q3517364)
    (32.1421, 35.5815),   # Tell Umm Hammad (Q27121077)
    (32.1153, 35.5431),   # Zarqa mouth, into the Jordan (Q798460)
]

ARNON = [
    (31.4210, 35.9502),   # Khirbet Mudayna as-Saliya (fortress on the Wadi as-Saliya headwater) (Q114845920)
    (31.4408, 35.8731),   # Confluence of Wadi Umm Sumayt (Q35294243)
    (31.4403, 35.8217),   # Mujib Reservoir (Q16895507)
    (31.4444, 35.8175),   # Mujib Dam (Q1951988)
    (31.4265, 35.6788),   # Confluence of Wadi Umm al-Wi'al (Q35291978)
    (31.4658, 35.5733),   # Wadi Mujib canyon outlet (the canyon item's point) (Q2120208)
    (31.4671, 35.5634),   # Arnon mouth, Dead Sea shore (Q697112)
]

ZERED = [
    (30.8550, 35.9048),   # Wadi al-Hasa, upper course (GeoNames-derived item) (Q35239380)
    (30.8893, 35.8708),   # Umm Ubtulah (site in the Hasa valley) (Q98804527)
    (30.9314, 35.8130),   # Confluence of Wadi Salahah (Q35299271)
    (30.9441, 35.7791),   # Confluence of Wadi 'Anmayn (Q35305936)
    (30.9557, 35.7571),   # Confluence of Wadi Ja'is (Q35261607)
    (30.9727, 35.7134),   # Tannur Dam, below Khirbet et-Tannur (Q27126194)
    (30.9703, 35.6828),   # Wadi al-Hasa, middle course (GeoNames-derived item) (Q35239373)
    (30.9819, 35.6402),   # Confluence of Wadi 'Afra (Q35305273)
    (31.0006, 35.6133),   # Confluence of Wadi ad-Dafali (Q49771678)
    (31.0636, 35.4614),   # mouth of Wadi al-Hasa, on the Salt Sea's high-water shore (Q35239366)
]

KISHON = [
    (32.4783, 35.3042),   # Kishon source north of Jenin (the river item's source point) (Q1743701)
    (32.5833, 35.2500),   # Confluence of Wadi 'Azzam (Nahal Oz) (Q35307842)
    (32.6537, 35.1685),   # Tel Shor (about 1 km NE of the channel) (Q12058552)
    (32.6853, 35.1097),   # Tel Qashish, on the north bank (Q4220548)
    (32.7249, 35.0978),   # Turkish railway bridge over the Kishon (Q65249669)
    (32.7452, 35.0826),   # Mouth of Nahal Yagur (Q4025114)
    (32.7867, 35.0592),   # Nahal Kishon nature reserve (Q26769778)
    (32.8144, 35.0261),   # Kishon mouth, Haifa Bay (Q1743701)
]

# the Yarkon (Me Jarkon), from the springs below Aphek to the sea
YARKON = [
    (32.1044, 34.9268),   # Rosh HaAyin springs, below Tel Afek (Aphek, Antipatris) (Q7368794)
    (32.1119, 34.9158),   # Al-Mirr (former village and mill) (Q4702905)
    (32.1273, 34.9111),   # Beit Leah (building on the bank) (Q16130131)
    (32.1239, 34.8986),   # Abu Rabah watermill (Q6601921)
    (32.1156, 34.8700),   # Yarkon Cemetery (Q2897414)
    (32.0964, 34.8086),   # Seven Mills (Sheva Tahanot) (Q7059220)
    (32.0997, 34.8017),   # Confluence of the Ayalon (the Ayalon item's point) (Q412019)
    (32.0980, 34.7938),   # Yarkon Bridge (Q12405017)
    (32.1039, 34.7758),   # Yarkon mouth (Q927016)
]

# Wadi el-Arish, its lower course
BROOK_OF_EGYPT = [
    (30.8278, 34.1397),   # Rawafa Dam on Wadi el-Arish (Q12215572)
    (30.8381, 34.1175),   # Abu Ageila spring (Q23956264)
    (30.8900, 34.0200),   # Magdhaba (the 1916 battle's site item; no place item found) (Q2889191)
    (30.9789, 33.9008),   # Confluence of Wadi Huraydin (Q23949933)
    (31.1457, 33.8065),   # Mouth of Wadi el-Arish at El Arish (the wadi item's point) (Q10719024)
]

RIVERS = {
    "hasbani": HASBANI, "dan": DAN, "banias": BANIAS,
    "jordan_upper": JORDAN_UPPER, "jordan_lower": JORDAN_LOWER,
    "yarmuk": YARMUK, "jabbok": JABBOK, "arnon": ARNON, "zered": ZERED,
    "kishon": KISHON, "yarkon": YARKON, "brook_of_egypt": BROOK_OF_EGYPT,
}


# ===========================================================================
# The waters and lands, by name
# ===========================================================================

WATERS = {
    "great_sea": Water(
        "The great sea", (), r"\b[Gg]reat [Ss]ea\b", skip="Dan 7:2",
        aka=("Mediterranean", "sea of the Philistines", "western sea")),
    "salt_sea": Water(
        "Salt Sea", ("salt_sea",), r"\bSalt Sea\b|\bsea of the Arabah\b",
        aka=("Dead Sea", "sea of the Arabah"),
        note="Drawn at its high water of about 1900. The southern basin is "
             "now dry."),
    "galilee": Water(
        "Sea of Galilee", ("galilee",),
        r"\b[Ss]ea of Galilee\b|\b[Ss]ea of Tiberias\b|\blake of Gennesaret\b"
        r"|\bChinnereth\b|\bChinneroth\b",
        skip="Josh 19:35",                       # Chinnereth the town
        aka=("sea of Chinnereth", "Sea of Tiberias", "lake of Gennesaret",
             "Kinneret"),
        note="Chinnereth or Chinneroth on its own (Deuteronomy 3:17; Joshua "
             "11:2; 1 Kings 15:20) is the lake or the land round it, not the "
             "town."),
    "huleh": Water(
        "Huleh", ("huleh",), aka=("Lake Huleh", "waters of Merom"),
        note="The Bible doesn't name it. Some take it for the waters of "
             "Merom (Joshua 11:5, 7), which others put at the spring of "
             "Meiron. Drawn as it was before it was drained in the 1950s."),
    "jordan": Water(
        "Jordan", ("hasbani", "dan", "banias", "jordan_upper",
                   "jordan_lower"), r"\bJordan\b",
        note="Its three headstreams, from Mount Hermon, meet north of Huleh."),
    "yarmuk": Water(
        "Yarmuk", ("yarmuk",),
        note="The Bible doesn't name it. It divided Bashan from Gilead."),
    "jabbok": Water("Jabbok", ("jabbok",), r"\bJabbok\b",
                    aka=("Zarqa",)),
    "arnon": Water("Arnon", ("arnon",), r"\bArnon\b", aka=("Wadi Mujib",)),
    "zered": Water("Zered", ("zered",), r"\bZered\b",
                   aka=("Wadi al-Hasa",)),
    "kishon": Water("Kishon", ("kishon",), r"\bKishon\b",
                    aka=("Nahal Kishon",)),
    "yarkon": Water("Me Jarkon", ("yarkon",), r"\bMe Jarkon\b",
                    aka=("Yarkon",),
                    note="'The waters of the Yarkon', on Dan's border."),
    "brook_of_egypt": Water(
        "brook of Egypt", ("brook_of_egypt",), r"\bbrook of Egypt\b",
        aka=("Wadi el-Arish", "river of Egypt"),
        note="The land's south-western border (Numbers 34:5)."),
}

REGIONS = {
    "lebanon": Region("Lebanon", 33.50, 35.62, r"\bLebanon\b",
        skip="1 Kgs 7:2; 10:17, 21; 2 Chr 9:16, 20; Jer 22:23; Ezek 17:3"),
    "syria": Region("Syria", 33.22, 36.42, r"\bSyria\b", aka=("Aram",)),
    "phoenicia": Region("Phoenicia", 33.42, 35.40, r"\bPhoenicia\b",
                        nt=True),
    "galilee": Region("Galilee", 32.93, 35.33,
                      r"(?<!sea of )\bGalilee\b"),
    "samaria": Region("Samaria", 32.36, 35.12, r"\bSamaria\b",
                      note="The land round the city of Samaria, the hill "
                           "country of Ephraim and Manasseh.",
        skip="1 Kgs 16:24, 28, 29, 32; 18:2; 20:1, 10, 17, 34, 43; 21:1, 18; 22:10, 37, 38, 51; 2 Kgs 1:2, 3; 2:25; 3:1, 6; 5:3; 6:19, 20, 24, 25; 7:1, 18; 10:1, 12, 17, 35, 36; 13:1, 6, 9, 10, 13; 14:14, 16, 23; 15:8, 13, 14, 17, 23, 25, 27; 17:1, 5, 6; 18:9, 10, 34; 21:13; 2 Chr 18:2, 9; 22:9; 25:13, 24; 28:8, 9, 15; Ezra 4:10, 17; Neh 4:2; Isa 7:9; 8:4; 9:9; 10:9, 10, 11; 36:19; Jer 23:13; 41:5; Ezek 16:46, 51, 53, 55; 23:4, 33; Hos 7:1; 10:5, 7; 13:16; Amos 3:9, 12; 4:1; 6:1; 8:14; Mic 1:1, 5, 6; Acts 8:5"),
    "sharon": Region("Sharon", 32.45, 34.95, r"\bSharon\b",
                     note="The coastal plain from the Yarkon to Mount Carmel. "
                          "1 Chronicles 5:16's Sharon is another, east of the "
                          "Jordan.",
        skip="1 Chr 5:16"),
    "judah": Region("Judah", 31.66, 35.31,
                    note="The hill country of Judah and its wilderness."),
    "judea": Region("Judea", 31.47, 35.27, r"\bJudea\b", nt=True),
    "philistia": Region("Philistia", 31.57, 34.66, r"\bPhilistia\b"),
    "south": Region("The South", 31.02, 34.78, r"\bthe South\b",
                    aka=("Negev",),
                    note="The dry land south of Hebron, round Beersheba.",
        skip="Josh 19:8; 1 Sam 30:27; Ezek 20:46, 47; Luke 11:31"),
    "zin": Region("Wilderness of Zin", 30.80, 34.70,
                  r"\bwilderness of Zin\b"),
    "arabah": Region("The Arabah", 30.60, 35.28, r"\bArabah\b",
        skip="Josh 3:16; 15:6, 61; 18:22; 2 Kgs 14:25; Amos 6:14"),
    "gilead": Region("Gilead", 32.30, 35.80,
                     r"(?<!Ramoth )(?<!Jabesh )\bGilead\b",
        skip="Num 26:29, 30; 27:1; 36:1; Josh 17:3; Judg 7:3; 11:1, 2; 1 Chr 2:21, 23; 5:14; 7:14, 17"),
    "bashan": Region("Bashan", 32.92, 36.22, r"\bBashan\b"),
    "decapolis": Region("Decapolis", 32.7167, 35.8, r"\bDecapolis\b",
                        nt=True, aka=("the Ten Cities",),
                        note="A league of Greek cities, most of them east of "
                             "the Jordan."),
    "ammon": Region("Ammon", 31.88, 36.12, r"\bAmmon\b"),
    "moab": Region("Moab", 31.33, 35.86, r"\bMoab\b",
        skip="Gen 19:37"),
    "edom": Region("Edom", 30.66, 35.66, r"\bEdom\b",
        skip="Gen 25:30; 36:1, 8, 19; 2 Sam 6:10, 11, 12; 1 Chr 13:13, 14; 15:18, 21, 24, 25; 16:5, 38; 26:4, 8, 15; 2 Chr 25:24"),
}


# ===========================================================================
# Sites
# ===========================================================================

SITES = {
    "abdon_asher": Site(
        "Abdon", 33.0477, 35.1619, "Q30526945", PROBABLE,
        modern="Tel Avdon (Khirbet Abdeh), inland from Achziv",
        point="the mound",
        why="Name preserved at Khirbet Abdeh; accepted by most atlases",
        aka=("Tel Avdon", "Khirbet Abdeh"),
        region="Plain of Acco",
        tribe=("Asher",),
        levitical=True,
        refs="Josh 21:30; 1 Chr 6:74",
        skip="Judg 12:13, 15; 1 Chr 8:23, 30; 9:36; 2 Chr 34:20",
    ),
    "abel_beth_maacah": Site(
        "Abel Beth Maacah", 33.2581, 35.581, "Q2911724", KNOWN,
        modern="Tel Abel Beth Maacah (Abil el-Qamh)",
        point="the tell",
        why="Continuous name (Abil el-Qamh); excavated since 2013 on the Israel-Lebanon border",
        aka=("Abel of Beth Maacah", "Abel Maim", "Abel", "Abil el-Qamh", "Tel Abel Beth Maacah"),
        region="Huleh Valley",
        refs="2 Sam 20:14, 15, 18; 1 Kgs 15:20; 2 Kgs 15:29; 2 Chr 16:4",
        namesakes="Abel Meholah, Abel Keramim, Abel Shittim and Abel Mizraim are other places",
        skip="Gen 4:2, 4, 8, 9, 25; 50:11; Num 33:49; Judg 7:22; 1 Kgs 4:12; 19:16; Matt 23:35; Luke 11:51; Heb 11:4; 12:24",
    ),
    "acco": Site(
        "Acco", 32.9211, 35.0883, "Q12412094", KNOWN,
        modern="Tel Akko (Tell el-Fukhar), east of the Old City of Acre",
        point="the tell",
        why="Continuous name (Akko); the Bronze and Iron Age mound, renamed Ptolemais under the Ptolemies",
        aka=("Accho", "Acre", "Akko", "Ptolemais", "Tel Akko", "Tell el-Fukhar"),
        region="Plain of Acco",
        refs="Judg 1:31; Acts 21:7",
    ),
    "achshaph": Site(
        "Achshaph", 32.8728, 35.1513, "Q55634890", POSSIBLE,
        modern="Tell Keisan, in the Acco plain",
        point="Tell Keisan",
        source="Wikidata's Achshaph item (Q4157407) gives 32.9518, 35.1738, by Kafr Yasif; the point is Tell Keisan's",
        why="Debated: Tell Keisan (Aharoni) is the leading candidate; Tel Regev (Khirbet el-Harbaj) is also argued",
        aka=("Tell Keisan",),
        region="Plain of Acco",
        tribe=("Asher",),
        refs="Josh 11:1; 12:20; 19:25",
    ),
    "achzib_asher": Site(
        "Achzib", 33.0483, 35.1027, "Q340747", KNOWN,
        modern="Tel Achziv (ez-Zib), Achziv National Park",
        point="the tell",
        why="Continuous name (ez-Zib); excavated Iron Age harbour town with Phoenician cemeteries",
        aka=("Achziv", "Ecdippa"),
        region="Plain of Acco",
        tribe=("Asher",),
        refs="Josh 19:29; Judg 1:31",
        namesakes="Achzib in the Shephelah of Judah (Josh 15:44; Mic 1:14)",
        skip="Josh 15:44; Mic 1:14",
    ),
    "adam": Site(
        "Adam", 32.1037, 35.5471, "Q27124611", PROBABLE,
        modern="Tell ed-Damiyeh (Tall Damiya) by the Damiya bridge, east bank",
        point="the tell",
        why="The name survives at Damiya, at the Jabbok's mouth on the Jordan; where Josh 3:16 heaps the waters up",
        aka=("Damiya", "Tell ed-Damiyeh"),
        region="Jordan Valley",
        refs="Josh 3:16",
        namesakes="Not Adam the first man (Gen 3-5); some read Hos 6:7 'at Adam' as this town",
        skip="Gen 3:17, 21; 4:25; 5:1, 2, 3, 4, 5; 1 Chr 1:1; Job 31:33; Hos 6:7; Luke 3:38; Rom 5:14; 1 Cor 15:22, 45; 1 Tim 2:13, 14; Jude 1:14",
    ),
    "adullam": Site(
        "Adullam", 31.6547, 35.0031, "Q2914860", PROBABLE,
        modern="Tel Adullam (Khirbet esh-Sheikh Madhkur)",
        why="The name survives at nearby Khirbet Id el-Ma; Eusebius; consensus",
        aka=("Khirbet esh-Sheikh Madhkur", "Tel Adullam"),
        region="the lowland",
        tribe=("Judah",),
        refs="Josh 12:15; 15:35; 1 Sam 22:1; 2 Sam 23:13; 1 Chr 11:15; 2 Chr 11:7; Neh 11:30; Mic 1:15",
    ),
    "ai": Site(
        "Ai", 31.9169, 35.2611, "Q403166", PROBABLE,
        modern="et-Tell, east of Beitin",
        point="the site",
        why="East of Bethel as Gen 12:8 and Josh 8:9 say; Marquet-Krause and Callaway excavations; but no Late Bronze city, so Khirbet el-Maqatir and Khirbet Nisya are argued too",
        aka=("Hai", "Aiath", "Aija"),
        region="Benjamin",
        refs="Gen 12:8; 13:3; Josh 7:2, 4; 8:1, 9, 28; 10:1; 12:9; Ezra 2:28; Neh 7:32",
        namesakes="Ai of Ammon (Jer 49:3) is another town",
        skip="Jer 49:3",
    ),
    "aijalon": Site(
        "Aijalon", 31.8411, 35.0236, "Q6986308", KNOWN,
        modern="Tel Ayalon (Yalo), at the head of the Aijalon valley",
        why="The name survives in Yalo.",
        aka=("Ajalon", "Tel Ayalon", "Yalo"),
        region="the lowland",
        tribe=("Dan",),
        levitical=True,
        refs="Josh 10:12; 19:42; 21:24; Judg 1:35; 1 Sam 14:31; 1 Chr 6:69; 8:13; 2 Chr 11:10; 28:18",
        namesakes="Aijalon in Zebulun, Elon's burial place (Judg 12:12)",
        skip="Judg 12:12",
    ),
    "akrabbim": Site(
        "Akrabbim", 30.9067, 35.1317, "Q7371401", PROBABLE,
        modern="Ma'ale Akrabbim, the pass from the Arabah up to the Negev highlands",
        point="the pass",
        source="the first of the item's Wikidata coordinates",
        why="The main ascent south-west of the Dead Sea, on Judah's south border; the modern name follows the biblical one",
        aka=("Scorpion Pass", "Ma'ale Akrabbim", "Naqb es-Safa"),
        region="the South",
        refs="Num 34:4; Josh 15:3; Judg 1:36",
    ),
    "almon": Site(
        "Almon", 31.8256, 35.2708, "Q109951711", PROBABLE,
        modern="Khirbet Almit, NE of 'Anata",
        point="the site",
        why="Name preserved (Allemeth of 1 Chr 6:60); a priests' town beside Anathoth (Josh 21:18)",
        aka=("Allemeth", "Khirbet Almit"),
        region="Benjamin",
        tribe=("Benjamin",),
        levitical=True,
        refs="Josh 21:18",
        namesakes="Almon Diblathaim (Num 33:46-47) is a camp in Moab",
        skip="Num 33:46, 47",
    ),
    "anab": Site(
        "Anab", 31.4038, 34.9443, "Q4750540", PROBABLE,
        modern="Khirbet Anab, south-west of Hebron",
        why="The name survives at Khirbet Anab; which of the two Anab ruins is uncertain",
        aka=("Khirbet Anab es-Saghir", "Anab al-Kabir"),
        region="Judah",
        tribe=("Judah",),
        refs="Josh 11:21; 15:50",
        source="the biblical city's Wikidata item",
    ),
    "anathoth": Site(
        "Anathoth", 31.8141, 35.2647, "Q2662138", PROBABLE,
        modern="Ras el-Kharrubeh in 'Anata, NE of Jerusalem",
        why="The name survives in 'Anata; Alt's Ras el-Kharrubeh hill within it is the usual site (Biran preferred Khirbet Deir es-Sidd nearby)",
        aka=("Ras el-Kharrubeh",),
        region="Benjamin",
        tribe=("Benjamin",),
        levitical=True,
        refs="Josh 21:18; 1 Kgs 2:26; 1 Chr 6:60; Ezra 2:23; Neh 11:32; Isa 10:30; Jer 1:1; 11:21; 32:7, 9",
        namesakes="Anathoth is also a person (1 Chr 7:8; Neh 10:19)",
        source="Wikidata's 'Anathoth' item; the town is Q2061100",
        skip="1 Chr 7:8; Neh 10:19",
    ),
    "aphek_asher": Site(
        "Aphek", 32.8461, 35.1119, "Q2910426", PROBABLE,
        modern="Tel Afek (Tell Kurdani), at the springs of Nahal Na'aman",
        point="the tell",
        why="Scholarly consensus for Asher's Aphek, a large Bronze-Iron Age tell at the Na'aman springs",
        aka=("Aphik", "Tel Afek", "Tell Kurdani"),
        region="Plain of Acco",
        tribe=("Asher",),
        refs="Josh 19:30; Judg 1:31",
        namesakes="Aphek in the Sharon (1 Sam 4:1; 29:1), Aphek in the Golan (1 Kgs 20:26), Aphek of the Sidonians (Josh 13:4), Aphekah in Judah",
        skip="Josh 12:18; 13:4; 1 Sam 4:1; 29:1; 1 Kgs 20:26, 30; 2 Kgs 13:17",
    ),
    "aphek_sharon": Site(
        "Aphek", 32.105, 34.9304, "Q682612", KNOWN,
        modern="Tel Afek / Antipatris (Ras el-Ain), at the Yarkon springs",
        why="Antipatris is certain: Herod's city at the Yarkon springs. Biblical Aphek on the same tell is the consensus, from Egyptian texts, Josephus and the Tel Aphek excavations.",
        aka=("Antipatris", "Pegai", "Ras el-Ain", "Tel Afek"),
        region="Sharon",
        refs="Josh 12:18; 1 Sam 4:1; 29:1; Acts 23:31",
        namesakes="Aphek of Asher (Josh 19:30), Aphek of the Sidonians (Josh 13:4), Aphek east of the Sea of Galilee (1 Kgs 20:26-30; 2 Kgs 13:17)",
        skip="Josh 13:4; 19:30; 1 Kgs 20:26, 30; 2 Kgs 13:17",
    ),
    "ar_moab": Site(
        "Ar", 31.2667, 35.7333, "Q847351", POSSIBLE,
        modern="er-Rabba (Rabbath-Moab, Areopolis), Jordan",
        point="the village",
        source="the village, to the arc-minute",
        why="Eusebius equated Ar with Areopolis (er-Rabba); many now place Ar near the Arnon (e.g. Khirbet el-Balu') or read it as a district.",
        aka=("Ar of Moab", "Areopolis"),
        region="Moab",
        refs="Num 21:15, 28; Deut 2:9, 18, 29; Isa 15:1",
    ),
    "arad": Site(
        "Arad", 31.2808, 35.125, "Q2063578", PROBABLE,
        modern="Tel Arad (Israelite fortress and Early Bronze city)",
        why="The Arad ostraca and Shishak's list name it, but it has no Late Bronze level, so the Canaanite Arad of Num 21 may be Tel Malhata",
        aka=("Tel Arad", "Tell Arad"),
        region="the South",
        refs="Num 21:1; 33:40; Josh 12:14; Judg 1:16",
        skip="1 Chr 8:15",
    ),
    "arimathaea": Site(
        "Arimathaea", 32.0281, 35.0194, "Q7293548", POSSIBLE,
        modern="Rantis village, NW of Ramallah",
        point="the village of Rantis",
        source="no Wikidata item for an ancient site",
        why="Eusebius' Armathem Sipha/Remphthis near Diospolis; one of several candidates (also er-Ram, Ramla's medieval tradition)",
        aka=("Arimathea", "Ramathaim Zophim", "Ramathaim-zophim", "Rantis", "Rathamin", "Remphthis"),
        region="Samaria",
        refs="Matt 27:57; Mark 15:43; Luke 23:51; John 19:38",
        namesakes="If Samuel's Ramathaim Zophim (1 Sam 1:1) is Arimathaea, his Ramah is here; others put Ramathaim Zophim at er-Ram",
    ),
    "aroer_arnon": Site(
        "Aroer", 31.4667, 35.8167, "Q4540437", KNOWN,
        modern="Khirbet 'Ara'ir on the Arnon's north rim, Jordan",
        point="the village of 'Ara'ir",
        source="the 'Ara'ir village item, to the arc-minute; Wikidata's Aroer item has a mistaken longitude on the Dead Sea shore",
        why="Continuous name ('Ara'ir); Aroer of the Mesha Stele; excavated fort on the Wadi Mujib rim.",
        aka=("Khirbet 'Ara'ir",),
        region="Moab",
        tribe=("Reuben",),
        refs="Num 32:34; Deut 2:36; 3:12; 4:48; Josh 12:2; 13:9, 16; Judg 11:26; 2 Kgs 10:33; 1 Chr 5:8; Jer 48:19",
        namesakes="Aroer near Rabbah in Gad (Joshua 13:25); Aroer in the Negev of Judah (1 Samuel 30:28); the 'cities of Aroer' (Isaiah 17:2)",
        skip="Josh 13:25; Judg 11:33; 1 Sam 30:28; Isa 17:2",
    ),
    "aroer_negev": Site(
        "Aroer", 31.1521, 34.9789, "Q108552789", PROBABLE,
        modern="Tel Aroer, south-east of Beersheba",
        why="The name survives in Ar'arah; excavated Iron Age town (Biran)",
        aka=("Tel Aroer", "Khirbet Ar'arah"),
        region="the South",
        refs="1 Sam 30:28",
        namesakes="Aroer on the Arnon (Deuteronomy 2:36) and Aroer near Rabbah in Gad (Joshua 13:25)",
        skip="Num 32:34; Deut 2:36; 3:12; 4:48; Josh 12:2; 13:9, 16, 25; Judg 11:26, 33; 2 Sam 24:5; 2 Kgs 10:33; 1 Chr 5:8; Isa 17:2; Jer 48:19",
    ),
    "arumah": Site(
        "Arumah", 32.1476, 35.3216, "Q30527603", PROBABLE,
        modern="Khirbet el-'Ormeh, SE of Nablus",
        point="the site",
        why="Name preserved; a hill fortress within reach of Shechem (Judg 9:41)",
        aka=("Khirbet el-'Ormeh", "Khirbet el-Urma"),
        region="Samaria",
        refs="Judg 9:41",
    ),
    "ashdod": Site(
        "Ashdod", 31.7578, 34.6586, "Q12412087", KNOWN,
        modern="Tel Ashdod (Isdud), southeast of modern Ashdod",
        why="The name has never changed (Isdud), and Dothan excavated Tel Ashdod.",
        aka=("Azotus", "Isdud", "Tel Ashdod"),
        region="Philistia",
        tribe=("Judah",),
        refs="Josh 15:46, 47; 1 Sam 5:1, 6; 6:17; 2 Chr 26:6; Neh 13:23; Isa 20:1; Amos 1:8; Zeph 2:4; Acts 8:40",
    ),
    "ashkelon": Site(
        "Ashkelon", 31.6619, 34.5461, "Q104664899", KNOWN,
        modern="Tel Ashkelon (Ascalon), in Ashkelon National Park",
        why="The name has never changed ('Asqalan), and Tel Ashkelon has been excavated (the Leon Levy Expedition).",
        aka=("Ascalon", "Ashqelon", "Tel Ashkelon"),
        region="Philistia",
        refs="Judg 1:18; 14:19; 1 Sam 6:17; 2 Sam 1:20; Jer 47:5, 7; Amos 1:8; Zeph 2:4, 7; Zech 9:5",
    ),
    "ashtaroth": Site(
        "Ashtaroth", 32.81, 36.02, "Q7697381", KNOWN,
        modern="Tell Ashtara, Syria",
        point="the mound",
        why="Name preserved at Tell Ashtara; Ashtartu of the Amarna letters and Tiglath-pileser III's relief; Og's city.",
        aka=("Be Eshterah", "Ashtartu", "Tell Ashtara"),
        region="Bashan",
        tribe=("Manasseh",),
        levitical=True,
        refs="Deut 1:4; Josh 9:10; 12:4; 13:12, 31; 21:27; 1 Chr 6:71",
        namesakes="The Ashtaroth, images of the goddess (Judges 2:13; 1 Samuel 7:3-4; 31:10), not a place",
        skip="Judg 2:13; 10:6; 1 Sam 7:3, 4; 12:10; 31:10",
    ),
    "ashteroth_karnaim": Site(
        "Ashteroth Karnaim", 32.8358, 36.035, "Q4703239", POSSIBLE,
        modern="ash-Shaykh Sa'd, Syria",
        point="the village; Tell Sa'd beside it",
        why="Karnaim is usually put at Sheikh Sa'd, 4 km N of Tell Ashtara; some read Ashteroth Karnaim as Ashtaroth itself.",
        aka=("Karnaim", "Carnaim", "Sheikh Sa'd"),
        region="Bashan",
        refs="Gen 14:5",
        namesakes="Ashtaroth (Tell Ashtara), the neighbouring city",
    ),
    "ataroth_moab": Site(
        "Ataroth", 31.5744, 35.6648, "Q100233378", KNOWN,
        modern="Khirbat Ataruz, Jordan",
        point="the site",
        why="Name preserved (Ataruz, Jebel Atarus); Ataroth of the Mesha Stele; excavated Iron Age temple-town.",
        aka=("Khirbet Ataruz",),
        region="Moab",
        refs="Num 32:3, 34",
        namesakes="Ataroth and Ataroth Addar on the Ephraim-Benjamin border (Joshua 16:2, 5, 7; 18:13); Atrothshophan (Numbers 32:35)",
        skip="Josh 16:2, 5, 7; 18:13",
    ),
    "azekah": Site(
        "Azekah", 31.7003, 34.9358, "Q723564", PROBABLE,
        modern="Tel Azekah (Tell Zakariya)",
        why="Scholarly consensus, from Eusebius and the Elah-valley geography of 1 Sam 17:1. Excavated by the Lautenschläger Azekah Expedition.",
        aka=("Tel Azekah", "Tell Zakariya"),
        region="the lowland",
        tribe=("Judah",),
        refs="Josh 10:10, 11; 15:35; 1 Sam 17:1; 2 Chr 11:9; Neh 11:30; Jer 34:7",
    ),
    "baal_hazor": Site(
        "Baal Hazor", 31.9786, 35.2861, "Q2917302", PROBABLE,
        modern="Tall Asur (Jebel Asur), the highest summit of the central hills, NE of Bethel",
        point="the summit",
        why="Name preserved; 'beside Ephraim' (2 Sam 13:23), i.e. near Ophrah/Ephraim at Taybeh",
        aka=("Tall Asur", "Jebel Asur"),
        region="Samaria",
        refs="2 Sam 13:23",
        namesakes="Not Hazor in Galilee, nor Hazor of Benjamin (Neh 11:33)",
    ),
    "baal_meon": Site(
        "Baal Meon", 31.6808, 35.7323, "Q12238281", PROBABLE,
        modern="Ma'in, Jordan",
        point="the village",
        why="Name preserved in Ma'in; Baal-meon of the Mesha Stele; widely accepted.",
        aka=("Beth Baal Meon", "Beth Meon", "Ma'in"),
        region="Moab",
        tribe=("Reuben",),
        refs="Num 32:38; Josh 13:17; 1 Chr 5:8; Jer 48:23; Ezek 25:9",
    ),
    "beersheba": Site(
        "Beersheba", 31.2447, 34.8408, "Q534596", PROBABLE,
        modern="Tel Be'er Sheva, 5 km east of the modern city centre",
        point="the tell",
        source="the first of the item's Wikidata coordinates",
        why="Aharoni's excavated Iron Age town; the name continues in Bir es-Seba, where some put the patriarchal wells",
        aka=("Tel Be'er Sheva", "Tell es-Seba", "Bir es-Seba"),
        region="the South",
        tribe=("Judah", "Simeon"),
        refs="Gen 21:31, 33; 26:23, 33; 28:10; 46:1; Josh 15:28; 19:2; Judg 20:1; 1 Sam 8:2; 1 Kgs 19:3; 2 Kgs 23:8",
    ),
    "bene_berak": Site(
        "Bene Berak", 32.0367, 34.8277, "Q12412086", KNOWN,
        modern="Tel Bnei Brak (Ibn Ibraq, al-Khayriyya), near Ramat Gan",
        why="The name survives in Ibn Ibraq, and Sennacherib's annals list Banai-barqa.",
        aka=("Tel Bnei Brak", "Ibn Ibraq"),
        region="Coastal plain",
        tribe=("Dan",),
        refs="Josh 19:45",
    ),
    "beracah_valley": Site(
        "Beracah Valley", 31.6437, 35.1438, "Q115694624", PROBABLE,
        kind="valley",
        modern="Khirbet Bereikut (Horvat Berachot), a ruin above the valley between Bethlehem and Hebron",
        why="The name survives in Khirbet and Wadi Bereikut, west of Tekoa",
        aka=("Valley of Berachah", "Wadi Bereikut", "Khirbet Bereikut", "Horvat Berachot"),
        region="Judah",
        refs="2 Chr 20:26",
    ),
    "beth_haccherem": Site(
        "Beth Haccherem", 31.7399, 35.2169, "Q47466657", POSSIBLE,
        modern="Ramat Rachel",
        point="the archaeological park",
        why="Aharoni's identification of the Judahite royal citadel; Ein Karem and Herodium are also proposed",
        aka=("Ramat Rachel", "Khirbet Salih"),
        region="Judah",
        refs="Neh 3:14; Jer 6:1",
    ),
    "beth_haram": Site(
        "Beth Haram", 31.8256, 35.6444, "Q85805483", POSSIBLE,
        modern="Tell er-Rameh, Jordan",
        point="the mound",
        why="Name kept at Tell er-Rameh (Josephus's Betharamphtha, Livias); nearby Tell Iktanu is preferred by some for the Iron Age town.",
        aka=("Beth Haran", "Betharamphtha", "Livias", "Tell er-Rameh"),
        region="Jordan Valley",
        tribe=("Gad",),
        refs="Num 32:36; Josh 13:27",
    ),
    "beth_hoglah": Site(
        "Beth Hoglah", 31.8203, 35.5019, "Q12212349", PROBABLE,
        modern="Deir Hajla monastery, SE of Jericho",
        point="the monastery",
        source="the monastery, the nearest named place; the first of two Wikidata coordinates",
        why="The name survives in 'Ain Hajla and Deir Hajla; the Judah-Benjamin border corner near the Jordan mouth (Josh 15:6; 18:19)",
        aka=("Deir Hajla",),
        region="Jordan Valley",
        tribe=("Benjamin",),
        refs="Josh 15:6; 18:19, 21",
        namesakes="Hoglah daughter of Zelophehad (Num 26:33) is a person",
    ),
    "beth_horon_lower": Site(
        "Beth Horon the lower", 31.895, 35.0836, "Q2905332", KNOWN,
        modern="Beit Ur al-Tahta village",
        point="the village",
        source="no Wikidata item for the tell; the first of two Wikidata coordinates",
        why="Continuous name Beit 'Ur; the foot of the ascent, fortified by Solomon (1 Kgs 9:17)",
        aka=("Lower Beth Horon", "Beit Ur al-Tahta"),
        region="Benjamin",
        tribe=("Ephraim",),
        levitical=True,
        refs="Josh 16:3; 18:13; 1 Kgs 9:17; 1 Chr 7:24; 2 Chr 8:5",
        namesakes="Beth Horon the upper, its twin 3 km east. Where the text says only 'Beth Horon' (Josh 10:10-11; 18:13-14; 21:22; 1 Sam 13:18; 2 Chr 25:13) it means the pair",
    ),
    "beth_horon_upper": Site(
        "Beth Horon the upper", 31.8858, 35.1142, "Q2905277", KNOWN,
        modern="Beit Ur al-Fauqa village",
        point="the village",
        source="no Wikidata item for the tell; the first of two Wikidata coordinates",
        why="Continuous name Beit 'Ur; Eusebius; the head of the ascent from the Aijalon valley (Josh 10:10)",
        aka=("Upper Beth Horon", "Beit Ur al-Fauqa"),
        region="Benjamin",
        tribe=("Ephraim",),
        levitical=True,
        refs="Josh 16:5; 2 Chr 8:5",
        namesakes="Beth Horon the lower, its twin 3 km west. Where the text says only 'Beth Horon' (Josh 10:10-11; 18:13-14; 21:22; 1 Sam 13:18; 2 Chr 25:13) it means the pair",
    ),
    "beth_jeshimoth": Site(
        "Beth Jeshimoth", 31.7659, 35.5984, "Q110921589", POSSIBLE,
        modern="Sweimeh, Jordan, near the Jordan's mouth",
        point="the village",
        source="the Iron Age candidate Tell el-Azeimeh is nearby",
        why="Name kept at Khirbet es-Suweimeh (Eusebius's Bethsimuth); the mound itself is debated.",
        aka=("Bethsimuth", "Sweimeh", "Tell el-Azeimeh"),
        region="Jordan Valley",
        tribe=("Reuben",),
        refs="Num 33:49; Josh 12:3; 13:20; Ezek 25:9",
    ),
    "beth_nimrah": Site(
        "Beth Nimrah", 31.9091, 35.6387, "Q4897428", PROBABLE,
        modern="Tell Nimrin, Jordan",
        why="Name kept in Tell Nimrin / Wadi Nimrin (Bethennabris); Glueck's sequence Tell Bleibil then Tell Nimrin.",
        aka=("Nimrah", "Bethennabris", "Tell Nimrin"),
        region="Jordan Valley",
        tribe=("Gad",),
        refs="Num 32:3, 36; Josh 13:27",
        source="Wikidata's Beth Nimrah item",
    ),
    "beth_shean": Site(
        "Beth Shean", 32.5036, 35.5031, "Q49004168", KNOWN,
        modern="Tel Beth Shean (Tell el-Husn), above Roman Scythopolis",
        point="the tell",
        why="Continuous name (Beisan); excavated Egyptian garrison with stelae of Seti I and Ramesses II",
        aka=("Beth Shan", "Scythopolis", "Beisan", "Beit She'an", "Tell el-Husn", "Tel Beth Shean"),
        region="Beth Shean Valley",
        tribe=("Manasseh",),
        refs="Josh 17:11, 16; Judg 1:27; 1 Sam 31:10, 12; 2 Sam 21:12; 1 Kgs 4:12; 1 Chr 7:29",
    ),
    "beth_shemesh": Site(
        "Beth Shemesh", 31.7506, 34.9747, "Q12412084", KNOWN,
        modern="Tel Beth Shemesh ('Ain Shems)",
        why="The name survives in 'Ain Shems. The tell was excavated by Grant, and later by Bunimovitz and Lederman.",
        aka=("Irshemesh", "Tel Beth Shemesh"),
        region="the lowland",
        tribe=("Judah", "Dan"),
        levitical=True,
        refs="Josh 15:10; 19:41; 21:16; 1 Sam 6:9, 12, 13, 19; 1 Kgs 4:9; 2 Kgs 14:11, 13; 1 Chr 6:59; 2 Chr 28:18",
        namesakes="Beth Shemesh of Issachar (Josh 19:22), of Naphtali (Josh 19:38; Judg 1:33), and in Egypt (Jer 43:13)",
        skip="Josh 19:22, 38; Judg 1:33; Jer 43:13",
    ),
    "beth_tappuah": Site(
        "Beth Tappuah", 31.5392, 35.0531, "Q7674962", KNOWN,
        modern="Taffuh, west of Hebron",
        point="the modern village",
        why="Continuous name",
        aka=("Taffuh",),
        region="Judah",
        tribe=("Judah",),
        refs="Josh 15:53",
        namesakes="Tappuah in the Shephelah (Joshua 15:34) and on Ephraim's border (Joshua 16:8)",
    ),
    "beth_zur": Site(
        "Beth Zur", 31.5833, 35.1, "Q4897432", PROBABLE,
        modern="Khirbet et-Tubeiqa, by Burj es-Sur",
        why="Excavated fortress (Sellers 1931, 1957); the name survives at nearby Burj es-Sur",
        aka=("Khirbet et-Tubeiqa", "Beth-zur", "Bethsura"),
        region="Judah",
        tribe=("Judah",),
        refs="Josh 15:58; 1 Chr 2:45; 2 Chr 11:7; Neh 3:16",
        source="Wikidata's coordinate is coarse, to the minute",
    ),
    "bethany": Site(
        "Bethany", 31.7714, 35.2613, "Q831190", KNOWN,
        modern="al-Eizariya, on the east slope of the Mount of Olives (the village; Tomb of Lazarus)",
        why="Continuous name (al-Azariya from Lazarion); Eusebius and the Bordeaux Pilgrim; 15 stadia from Jerusalem (John 11:18) fits",
        aka=("Lazarion",),
        region="Judah",
        refs="Matt 21:17; 26:6; Mark 11:1, 11; 14:3; Luke 19:29; 24:50; John 11:1, 18; 12:1",
        namesakes="Bethany beyond the Jordan (John 1:28)",
        skip="John 1:28",
    ),
    "bethany_beyond_jordan": Site(
        "Bethany beyond the Jordan", 31.8372, 35.5503, "Q12193567", POSSIBLE,
        modern="Al-Maghtas (Wadi el-Kharrar), east bank opposite Jericho",
        point="the archaeological site",
        why="The Madaba map and Byzantine pilgrims; UNESCO's 'Baptism Site Bethany Beyond the Jordan'; others place it in Batanea (Bashan) or at a northern ford",
        aka=("Al-Maghtas", "Bethabara", "Wadi al-Kharrar", "Wadi el-Kharrar"),
        region="Jordan Valley",
        refs="John 1:28",
        namesakes="Bethany of Lazarus near Jerusalem (John 11:1, 18; 12:1; Mark 11:1) is another village",
    ),
    "bethel": Site(
        "Bethel", 31.9228, 35.2414, "Q3876767", PROBABLE,
        modern="Beitin, NE of Ramallah",
        point="the village of Beitin",
        source="Wikidata's 'Bethel' biblical-place item; the village is Q2898916",
        why="Name echoed in Beitin; Eusebius 12 miles north of Jerusalem on the Neapolis road; Albright and Kelso excavations; Livingston's el-Bireh is a minority view",
        aka=("Luz", "Beitin", "Beth Aven"),
        region="Benjamin",
        tribe=("Benjamin",),
        refs="Gen 12:8; 28:19; 35:1; Josh 7:2; 16:2; 18:22; Judg 1:22; 4:5; 1 Kgs 12:29; 2 Kgs 2:2; 23:15; Amos 7:13",
        namesakes="Bethel of 1 Sam 30:27 is another town in the Negev (Bethul, Josh 19:4); Beth Aven of Josh 7:2 and 18:12 is a separate place near Ai",
        skip="Josh 18:12; Judg 1:26; 1 Sam 13:5; 14:23; 30:27",
    ),
    "bethlehem_judah": Site(
        "Bethlehem", 31.7044, 35.2061, "Q5776", KNOWN,
        modern="Bethlehem",
        point="the town, by the Church of the Nativity",
        why="Continuous name; Eusebius; Nativity church since the 4th century",
        aka=("Beit Lahm", "Bethlehem Ephrathah", "Bethlehem Judah", "Bethlehem of Judea", "David's city", "Ephrath", "Ephrathah"),
        region="Judah",
        refs="Gen 35:19; Ruth 1:1, 19; 1 Sam 16:4; 17:12; 2 Sam 23:15; Mic 5:2; Matt 2:1, 6, 16; Luke 2:4, 15; John 7:42",
        namesakes="Bethlehem of Zebulun in Galilee (Joshua 19:15)",
        skip="Josh 19:15; Judg 12:8, 10; 1 Chr 2:19, 24, 50; Ps 132:6",
    ),
    "bethlehem_zebulun": Site(
        "Bethlehem", 32.7356, 35.1906, "Q604557", PROBABLE,
        modern="Bethlehem of Galilee (Beit Lahm), west of Nazareth",
        point="the modern village",
        why="Continuous name, with ancient remains at the village",
        aka=("Bethlehem of Galilee", "Beit Lahm", "Bethlehem of Zebulun"),
        region="Lower Galilee",
        tribe=("Zebulun",),
        refs="Josh 19:15",
        namesakes="Bethlehem of Judah (Ruth 1:1; Matt 2:1)",
        skip="Gen 35:19; 48:7; Judg 12:8, 10; 17:7, 8, 9; 19:1, 2, 18; Ruth 1:1, 2, 19, 22; 2:4; 4:11; 1 Sam 16:4; 17:12, 15; 20:6, 28; 2 Sam 2:32; 23:14, 15, 16, 24; 1 Chr 2:51, 54; 4:4; 11:16, 17, 18, 26; 2 Chr 11:6; Ezra 2:21; Neh 7:26; Jer 41:17; Mic 5:2; Matt 2:1, 5, 6, 8, 16; Luke 2:4, 15; John 7:42",
    ),
    "bethsaida": Site(
        "Bethsaida", 32.91, 35.6305, "Q501773", POSSIBLE,
        modern="et-Tell, north-east of the lake, east of the Jordan inflow",
        point="the et-Tell excavation",
        source="el-Araj (32.8933, 35.6192) is the rival site",
        why="Debated: et-Tell (excavated by Arav) against el-Araj (excavated since 2016, by the shore)",
        aka=("Bethsaida Julias", "Bethsaida-Julias", "Julias"),
        region="Sea of Galilee",
        refs="Matt 11:21; Mark 6:45; 8:22; Luke 9:10; 10:13; John 1:44; 12:21",
    ),
    "bethphage": Site(
        "Bethsphage", 31.7772, 35.2508, "Q2193088", PROBABLE,
        modern="Bethphage at the Franciscan church on the Mount of Olives' east slope, Kafr et-Tur (ancient site)",
        why="Crusader and Franciscan tradition at et-Tur, between Bethany and the summit; the Talmud's Beit Pagi marks Jerusalem's outer limit there",
        aka=("Bethphage", "Kafr et-Tur", "Beit Pagi"),
        region="Judah",
        refs="Matt 21:1; Mark 11:1; Luke 19:29",
    ),
    "bezek_samaria": Site(
        "Bezek", 32.3688, 35.3974, "Q49354325", PROBABLE,
        modern="Khirbet Ibziq, NE of Tubas",
        point="the ruin",
        why="Name preserved; Eusebius' Bezek 17 miles from Neapolis toward Scythopolis; a mustering point facing Jabesh Gilead across the Jordan (1 Sam 11:8)",
        aka=("Khirbet Ibziq",),
        region="Samaria",
        refs="1 Sam 11:8",
        namesakes="The Bezek of Adoni-Bezek (Judg 1:4-5) is another place, in Judah's lands",
        skip="Judg 1:4, 5, 6, 7",
    ),
    "bozrah_edom": Site(
        "Bozrah", 30.7458, 35.6039, "Q4952895", PROBABLE,
        modern="Buseirah (Busaira), Jordan",
        point="the town over the tell",
        why="Continuous name; Crystal Bennett's excavation found the Edomite capital's monumental buildings; widely accepted.",
        aka=("Buseirah", "Busaira"),
        region="Edom",
        refs="Gen 36:33; 1 Chr 1:44; Isa 34:6; 63:1; Jer 49:13, 22; Amos 1:12; Mic 2:12",
        namesakes="Bozrah of Moab (Jeremiah 48:24)",
        skip="Jer 48:24",
    ),
    "cabul": Site(
        "Cabul", 32.8697, 35.2022, "Q5015855", PROBABLE,
        modern="Cabul, at Kabul village (Horvat Rosh Zayit is the Iron Age fort nearby)",
        why="Continuous name (Kabul); the 'land of Cabul' Solomon gave Hiram",
        aka=("Kabul", "Land of Cabul"),
        region="Plain of Acco",
        tribe=("Asher",),
        refs="Josh 19:27; 1 Kgs 9:13",
        source="Wikidata's biblical-place item",
    ),
    "caesarea": Site(
        "Caesarea", 32.5011, 34.8923, "Q319242", KNOWN,
        modern="Caesarea Maritima (Caesarea National Park)",
        why="The name has never changed (Qaisariyye). Herod's harbour city has been excavated, and the Pilate inscription was found there.",
        aka=("Caesarea Maritima", "Qaisariya", "Qaisariyye", "Qesarya", "Strato's Tower"),
        region="Sharon",
        refs="Acts 8:40; 9:30; 10:1, 24; 12:19; 18:22; 21:8; 23:23, 33; 25:1, 6, 13",
        namesakes="Caesarea Philippi (Matt 16:13; Mark 8:27)",
        skip="Matt 16:13; Mark 8:27",
    ),
    "caesarea_philippi": Site(
        "Caesarea Philippi", 33.2461, 35.6933, "Q2484244", KNOWN,
        modern="Banias, at the Banias spring below Hermon",
        point="the ancient Roman city",
        why="Continuous name (Banias from Panias); excavated city and the cave sanctuary of Pan",
        aka=("Banias", "Banyas", "Neronias", "Paneas", "Panias"),
        region="Huleh Valley",
        refs="Matt 16:13; Mark 8:27",
        namesakes="Caesarea on the coast (Acts 10:1)",
    ),
    "cana": Site(
        "Cana", 32.8222, 35.3027, "Q17199012", PROBABLE,
        modern="Khirbet Qana, on the north edge of the Beth Netofa valley",
        point="the archaeological site",
        why="Excavated 1st-century village with the name and a Byzantine pilgrim cave; Kafr Kanna is the later tradition",
        aka=("Cana of Galilee", "Kafr Kanna", "Khirbet Qana"),
        region="Lower Galilee",
        refs="John 2:1, 11; 4:46; 21:2",
    ),
    "capernaum": Site(
        "Capernaum", 32.8811, 35.575, "Q59174", KNOWN,
        modern="Capernaum (Tell Hum), on the north shore",
        point="the archaeological site",
        why="Continuous name (Kefar Nahum / Tell Hum); excavated synagogue and the house-church of Peter",
        aka=("Kefar Nahum", "Kfar Nahum", "Tell Hum"),
        region="Sea of Galilee",
        refs="Matt 4:13; 8:5; 11:23; 17:24; Mark 1:21; 2:1; 9:33; Luke 4:31; 7:1; John 2:12; 4:46; 6:17, 59",
    ),
    "carmel_judah": Site(
        "Carmel", 31.4225, 35.1311, "Q2904870", KNOWN,
        modern="Khirbet el-Kirmil, beside the village of al-Karmil",
        why="Continuous name; Eusebius",
        aka=("Khirbet el-Kirmil",),
        region="Judah",
        tribe=("Judah",),
        refs="Josh 15:55; 1 Sam 15:12; 25:2, 5, 7, 40",
        namesakes="Mount Carmel on the coast (Joshua 19:26; 1 Kings 18:19)",
        source="the biblical city's Wikidata item",
        skip="Josh 12:22; 19:26; 1 Kgs 18:19, 20, 42; 2 Kgs 2:25; 4:25; Song 7:5; Isa 33:9; 35:2; Jer 46:18; 50:19; Amos 1:2; 9:3; Nah 1:4",
    ),
    "mount_carmel": Site(
        "Carmel", 32.7299, 35.0497, "Q4159530", KNOWN,
        kind="mount",
        modern="Mount Carmel ridge",
        point="its summit, Rom Carmel (546 m)",
        why="Continuous name (Karmel); the traditional site of Elijah's contest is el-Muhraqa on the south-east end",
        aka=("Mount Carmel", "Jabal Mar Elyas", "Rom Carmel"),
        region="Mount Carmel",
        tribe=("Asher",),
        refs="Josh 12:22; 19:26; 1 Kgs 18:19, 20, 42; 2 Kgs 2:25; 4:25; Song 7:5; Isa 35:2; Jer 46:18; Amos 1:2",
        namesakes="Carmel in the hill country of Judah (Josh 15:55; 1 Sam 25:2)",
        skip="Josh 15:55; 1 Sam 15:12; 25:2, 5, 7, 40",
    ),
    "chephirah": Site(
        "Chephirah", 31.8309, 35.1068, "Q6401754", PROBABLE,
        modern="Khirbet Kefireh, west of el-Jib",
        point="the ruin",
        source="Wikidata's Chephirah item Q6563685 has no coordinate",
        why="Name preserved; one of the four Gibeonite towns with Gibeon, Beeroth and Kiriath Jearim (Josh 9:17)",
        aka=("Khirbet Kefireh", "Kephirah"),
        region="Benjamin",
        tribe=("Benjamin",),
        refs="Josh 9:17; 18:26; Ezra 2:25; Neh 7:29",
    ),
    "chesulloth": Site(
        "Chesulloth", 32.6825, 35.3244, "Q2915526", PROBABLE,
        modern="Iksal, south-east of Nazareth at the Jezreel valley's edge",
        point="the modern village",
        why="Name preserved at Iksal (Josephus's Exaloth); the same place as Chisloth Tabor (Josh 19:12)",
        aka=("Chisloth Tabor", "Iksal", "Exaloth"),
        region="Lower Galilee",
        tribe=("Issachar",),
        refs="Josh 19:12, 18",
    ),
    "chinnereth": Site(
        "Chinnereth", 32.8694, 35.5383, "Q49004184", PROBABLE,
        modern="Tel Kinrot (Tell el-Oreimeh), on the lake's north-west shore",
        point="the tell",
        why="Consensus: the excavated Iron Age city above Ginosar that named the lake",
        aka=("Chinneroth", "Kinneret", "Tel Kinrot", "Tell el-Oreimeh"),
        region="Sea of Galilee",
        tribe=("Naphtali",),
        refs="Josh 19:35",
        skip="Num 34:11; Deut 3:17; Josh 11:2; 12:3; 13:27; 1 Kgs 15:20",
    ),
    "chorazin": Site(
        "Chorazin", 32.9114, 35.5639, "Q2456076", KNOWN,
        modern="Chorazin (Khirbet Karazeh), in the hills north of Capernaum",
        point="the archaeological site",
        why="Continuous name (Karazeh); excavated Roman-Byzantine town and basalt synagogue",
        aka=("Khirbet Karazeh", "Korazim", "Korazin"),
        region="Sea of Galilee",
        refs="Matt 11:21; Luke 10:13",
    ),
    "daberath": Site(
        "Daberath", 32.6914, 35.3703, "Q2915531", PROBABLE,
        modern="Daburiyya, at the west foot of Mount Tabor",
        point="the modern village",
        why="Name preserved at Daburiyya (Josephus's Dabaritta)",
        aka=("Daburiyya", "Dabaritta"),
        region="Lower Galilee",
        tribe=("Issachar",),
        levitical=True,
        refs="Josh 19:12; 21:28; 1 Chr 6:72",
    ),
    "damascus": Site(
        "Damascus", 33.5111, 36.3064, "Q3678596", KNOWN,
        modern="The Ancient City of Damascus (the old walled city, with the Roman street called Straight)",
        why="Continuous name and occupation; the Roman grid survives in the old city",
        aka=("Dimashq",),
        region="Syria",
        refs="Gen 14:15; 2 Sam 8:6; 1 Kgs 19:15; 2 Kgs 5:12; 16:9; Isa 17:1; Amos 1:3; Acts 9:2, 8; 22:6; 2 Cor 11:32; Gal 1:17",
    ),
    "dan": Site(
        "Dan", 33.249, 35.652, "Q1346856", KNOWN,
        modern="Tel Dan (Tell el-Qadi), at the Dan springs",
        point="the tell",
        why="Firm: the bilingual 'to the god who is in Dan' inscription and the Tel Dan stele, by the Jordan springs",
        aka=("Laish", "Leshem", "Tel Dan", "Tell el-Qadi"),
        region="Huleh Valley",
        tribe=("Dan",),
        refs="Gen 14:14; Deut 34:1; Josh 19:47; Judg 18:7, 29; 20:1; 1 Sam 3:20; 1 Kgs 4:25; 12:29; 15:20; 2 Kgs 10:29; Amos 8:14",
        namesakes="Mahaneh Dan by Kiriath Jearim (Judg 18:12); the tribe's first allotment round Zorah (Josh 19:40-46)",
        skip="Gen 30:6; 35:25; 46:23; 49:16, 17; Exod 1:4; 31:6; 35:34; 38:23; Lev 24:11; Num 1:12, 38, 39; 2:25, 31; 7:66; 10:25; 13:12; 26:42; 34:22; Deut 27:13; 33:22; Josh 19:40, 48; 21:5, 23; Judg 1:34; 5:17; 13:25; 18:2, 12, 16, 22, 23, 25, 26, 30; 1 Sam 25:44; 2 Sam 3:15; 24:6; 1 Chr 2:2; 27:22; 2 Chr 2:14; Ezek 48:1, 2, 32",
    ),
    "debir_judah": Site(
        "Debir", 31.4333, 35.0167, "Q7278816", PROBABLE,
        modern="Khirbet Rabud, south-west of Hebron",
        point="the village of Rabud, at the tell",
        source="the Debir and Tel Debir items have no coordinate",
        why="Khirbet Rabud (Kochavi), whose upper and lower springs fit Josh 15:19, is now preferred; Albright's Tell Beit Mirsim is the older view",
        aka=("Kiriath Sepher", "Kiriath Sannah", "Khirbet Rabud", "Tel Debir"),
        region="Judah",
        tribe=("Judah",),
        levitical=True,
        refs="Josh 10:38, 39; 11:21; 12:13; 15:15, 49; 21:15; Judg 1:11; 1 Chr 6:58",
        namesakes="Debir on Judah's northern border by the Valley of Achor (Joshua 15:7); Debir in Gad (Joshua 13:26)",
        skip="Josh 10:3; 13:26; 15:7",
    ),
    "dibon": Site(
        "Dibon", 31.5019, 35.7767, "Q126716537", KNOWN,
        modern="Tell Dhiban, Jordan",
        point="the ancient city walls",
        source="Wikidata's item for the walls, beside the modern town",
        why="Continuous name (Dhiban); the Mesha Stele was found there; excavated.",
        aka=("Dimon", "Dibon Gad", "Dhiban"),
        region="Moab",
        tribe=("Reuben",),
        refs="Num 21:30; 32:3, 34; 33:45, 46; Josh 13:9, 17; Isa 15:2; Jer 48:18, 22",
        namesakes="Dibon in Judah (Nehemiah 11:25)",
        skip="Neh 11:25",
    ),
    "dor": Site(
        "Dor", 32.6174, 34.9164, "Q1243563", KNOWN,
        modern="Tel Dor (Khirbet el-Burj), by Tantura on the Carmel coast",
        why="The name survives (Dor/Dora at Tantura), and Tel Dor has been excavated over many seasons.",
        aka=("Tel Dor", "Dora", "Khirbet el-Burj", "Tantura"),
        region="Sharon",
        tribe=("Manasseh",),
        refs="Josh 11:2; 12:23; 17:11; Judg 1:27; 1 Kgs 4:11; 1 Chr 7:29",
    ),
    "dothan": Site(
        "Dothan", 32.4135, 35.2399, "Q2916407", KNOWN,
        modern="Tell Dothan, south of Jenin",
        point="the tell",
        why="Continuous name; Eusebius 12 miles north of Sebaste; J. P. Free's excavations",
        aka=("Tell Dothan", "Dothaim"),
        region="Samaria",
        refs="Gen 37:17; 2 Kgs 6:13",
    ),
    "edrei": Site(
        "Edrei", 32.6253, 36.1061, "Q238217", KNOWN,
        modern="Daraa, Syria",
        point="the modern city, which covers the ancient mound",
        why="Continuous name (Adraa of Eusebius and the Roman road, Arabic Der'a); Og's city.",
        aka=("Adraa", "Der'a", "Daraa"),
        region="Bashan",
        tribe=("Manasseh",),
        refs="Num 21:33; Deut 1:4; 3:1, 10; Josh 12:4; 13:12, 31",
        namesakes="Edrei in Naphtali (Joshua 19:37)",
        skip="Josh 19:37",
    ),
    "eglon": Site(
        "Eglon", 31.4903, 34.9284, "Q12412091", POSSIBLE,
        modern="Tel 'Eton (Tell 'Aitun) (one candidate)",
        why="Debated. Tel 'Eton is favoured by Rainey and Faust; Tell el-Hesi was the older identification.",
        aka=("Tel 'Eton", "Tell 'Aitun"),
        region="the lowland",
        tribe=("Judah",),
        refs="Josh 10:3, 5, 23, 34, 36, 37; 12:12; 15:39",
        namesakes="Eglon king of Moab (Judg 3:12-17) is a person",
        source="Wikidata's Eglon (Q1940256) has no coordinate; Tell el-Hesi is Q2067518",
        skip="Judg 3:12, 14, 15, 17",
    ),
    "ekron": Site(
        "Ekron", 31.7789, 34.8511, "Q1323557", KNOWN,
        modern="Tel Miqne (Khirbet el-Muqanna)",
        why="An inscription: the 7th-century BC royal dedicatory inscription found at Tel Miqne names Ekron and its king Achish.",
        aka=("Tel Miqne", "Khirbet el-Muqanna", "Accaron"),
        region="Philistia",
        tribe=("Judah", "Dan"),
        refs="Josh 13:3; 15:11, 45; 19:43; Judg 1:18; 1 Sam 5:10; 6:16; 7:14; 17:52; 2 Kgs 1:2; Amos 1:8; Zeph 2:4",
    ),
    "valley_of_elah": Site(
        "Elah", 31.6806, 34.9891, "Q862725", KNOWN,
        kind="valley",
        modern="The valley of Elah (Wadi es-Sant, Emek HaEla)",
        why="A label point for the valley below Socoh and Azekah where 1 Sam 17:1-2 sets the camps. WEB says 'the valley of Elah'.",
        aka=("Elah valley", "Wadi es-Sant", "Emek HaEla"),
        region="the lowland",
        refs="1 Sam 17:2, 19; 21:9",
        namesakes="Elah is also a personal name (king Elah, 1 Kgs 16:6-14; others)",
        skip="Gen 36:41; 1 Kgs 16:6, 8, 13, 14; 2 Kgs 15:30; 17:1; 18:1, 9; 1 Chr 1:52; 4:15; 9:8",
    ),
    "elealeh": Site(
        "Elealeh", 31.8167, 35.8333, "Q4705021", KNOWN,
        modern="el-'Al (Al-Al), Jordan",
        point="the village",
        source="the village, to the arc-minute",
        why="Continuous name (el-'Al), 3 km NE of Hesban, always paired with Heshbon.",
        region="Moab",
        refs="Num 32:3, 37; Isa 15:4; 16:9; Jer 48:34",
    ),
    "eltekeh": Site(
        "Eltekeh", 31.8925, 34.7678, "Q26768806", POSSIBLE,
        modern="Tel Shalaf (one candidate)",
        why="Debated. Tel Shalaf (Mazar, Rainey) is one candidate for Sennacherib's Altaqu. Khirbet el-Muqanna, once proposed, is now known to be Ekron.",
        aka=("Elteke", "Altaqu", "Tel Shalaf"),
        region="Philistia",
        tribe=("Dan",),
        levitical=True,
        refs="Josh 19:44; 21:23",
    ),
    "emmaus": Site(
        "Emmaus", 31.7939, 35.1639, "Q2898847", POSSIBLE,
        modern="Qalunya (Roman Colonia) at Motza, west of Jerusalem",
        why="Chosen of four. Luke puts it sixty stadia (about 11 km) from Jerusalem. Motza (Roman Colonia) is Josephus' Emmaus; el-Qubeibeh and Abu Ghosh are the others, and Emmaus Nicopolis ('Imwas), Eusebius' choice, lies 160 stadia off.",
        aka=("Motza", "Qalunya", "Colonia"),
        region="Judah",
        refs="Luke 24:13",
        namesakes="Emmaus of the Maccabean battles (1 Macc 3-4) is Nicopolis",
    ),
    "en_gannim_issachar": Site(
        "En Gannim", 32.4611, 35.3, "Q374748", PROBABLE,
        modern="Jenin, at the Jezreel valley's south edge",
        point="the modern city",
        why="Name preserved at Jenin (Josephus's Ginae); the usual identification, the Anem of 1 Chr 6:73",
        aka=("Engannim", "Anem", "Jenin", "Ginae"),
        region="Jezreel Valley",
        tribe=("Issachar",),
        levitical=True,
        refs="Josh 19:21; 21:29",
        namesakes="En Gannim in the Shephelah of Judah (Josh 15:34)",
        skip="Josh 15:34",
    ),
    "en_gedi": Site(
        "En Gedi", 31.4681, 35.3883, "Q25489001", KNOWN,
        modern="Ein Gedi archaeological site (Tel Goren) by the Dead Sea",
        why="Continuous name (Ein Jidi); Iron Age to Byzantine town excavated",
        aka=("Hazazon Tamar", "Ein Gedi", "Engedi", "Tel Goren"),
        region="the wilderness of Judah",
        tribe=("Judah",),
        refs="Josh 15:62; 1 Sam 23:29; 24:1; 2 Chr 20:2; Song 1:14; Ezek 47:10",
    ),
    "endor": Site(
        "Endor", 32.6365, 35.3813, "Q12060732", PROBABLE,
        modern="Indur, the Arab village (to 1948) on the Hill of Moreh's north side",
        point="the village",
        source="Wikidata's 'Endor' item, Q431722, sits 8 km east by Tel Rekhesh",
        why="Name preserved at Indur; the Iron Age mound is put at Khirbet Safsafa by the spring 'En Dor, about 1 km north-east",
        aka=("En Dor", "Indur", "Khirbet Safsafa"),
        region="Jezreel Valley",
        tribe=("Manasseh",),
        refs="Josh 17:11; 1 Sam 28:7; Ps 83:10",
    ),
    "enon": Site(
        "Enon", 32.3992, 35.5264, "Q12058546", POSSIBLE,
        label="Enon · Salim",
        modern="The springs round Tel Shalem (Eusebius's Salim), 12 km south of Beth Shean on the west side of the Jordan valley; the point is Tel Shalem's",
        why="Eusebius: 8 miles south of Scythopolis near Salim, and John 3:26 puts it west of the Jordan; rivals are 'Ainun near Salim east of Nablus, and the east-bank site of the Madaba map",
        aka=("Aenon", "Salim", "Tel Shalem"),
        region="Jordan Valley",
        refs="John 3:23",
        namesakes="Hazar Enon on the northern border (Num 34:9; Ezek 47:17), unrelated",
        skip="Ezek 47:17",
    ),
    "eshtaol": Site(
        "Eshtaol", 31.7804, 35.011, "Q2902157", PROBABLE,
        modern="Ishwa', the depopulated village beside moshav Eshtaol",
        why="Ishwa' keeps the name, near Zorah, and Eusebius puts Esthaol north of Eleutheropolis. Not excavated.",
        aka=("Ishwa'", "Eshwa"),
        region="the lowland",
        tribe=("Judah", "Dan"),
        refs="Josh 15:33; 19:41; Judg 13:25; 16:31; 18:2, 8, 11",
    ),
    "eshtemoa": Site(
        "Eshtemoa", 31.4004, 35.0673, "Q64363172", KNOWN,
        modern="as-Samu', south of Hebron",
        point="the synagogue",
        source="the ancient settlement's Wikidata item",
        why="Continuous name; Eusebius; ancient synagogue",
        aka=("Eshtemoh",),
        region="Judah",
        tribe=("Judah",),
        levitical=True,
        refs="Josh 21:14; 1 Sam 30:28; 1 Chr 4:17, 19; 6:57",
    ),
    "gadara": Site(
        "Gadarenes", 32.6555, 35.6778, "Q56322109", KNOWN,
        modern="Gadara at Umm Qais, Jordan",
        point="the ancient city's site",
        why="Gadara = Umm Qais by inscriptions, coins and continuous occupation; the swine miracle happened somewhere on its district's lake shore.",
        aka=("Gadara", "Umm Qais"),
        region="Decapolis",
        refs="Mark 5:1; Luke 8:26, 37",
        namesakes="The Gergesenes (Matthew 8:28), the same story placed at Gergesa",
    ),
    "gath": Site(
        "Gath", 31.6997, 34.8469, "Q1348441", KNOWN,
        modern="Tell es-Safi (Tel Tzafit)",
        why="Firm excavation (Maeir) of the largest Iron Age Philistine city, with a siege-and-destruction layer that fits Hazael (2 Kgs 12:17). No inscription has been found.",
        aka=("Tell es-Safi", "Tel Tzafit", "Gimti"),
        region="Philistia",
        refs="Josh 11:22; 1 Sam 5:8; 6:17; 7:14; 17:4; 21:10; 27:2; 2 Sam 1:20; 2 Kgs 12:17; 1 Chr 18:1; 2 Chr 26:6; Amos 6:2",
        namesakes="Gath Hepher (Zebulun), Gath Rimmon (Dan; also one in Manasseh), Moresheth Gath. WEB verses with those names are left out.",
        skip="Josh 19:13, 45; 21:24, 25; 2 Kgs 14:25; 1 Chr 6:69; Mic 1:14",
    ),
    "gath_hepher": Site(
        "Gath Hepher", 32.7417, 35.325, "Q5527338", PROBABLE,
        modern="Tel Gat Hefer (Khirbet ez-Zurra') by Mashhad",
        why="Jerome and an old tradition (the tomb of Jonah at Mashhad) place it here; accepted by most atlases",
        aka=("Tel Gat Hefer", "Khirbet ez-Zurra'", "Mashhad"),
        region="Lower Galilee",
        tribe=("Zebulun",),
        refs="Josh 19:13; 2 Kgs 14:25",
        source="Wikidata's Gath-hepher item",
    ),
    "gath_rimmon_dan": Site(
        "Gath Rimmon", 32.0917, 34.8075, "Q7695568", POSSIBLE,
        modern="Tel Gerisa (Tell Jerisheh), on the Yarkon in Tel Aviv (one candidate)",
        why="Debated. Mazar proposed Tel Gerisa; there is no inscription, and other tells near the Yarkon have been put forward.",
        aka=("Tel Gerisa", "Tell Jerisheh"),
        region="Coastal plain",
        tribe=("Dan",),
        levitical=True,
        refs="Josh 19:45; 21:24; 1 Chr 6:69",
        namesakes="Gath Rimmon of western Manasseh (Josh 21:25)",
        skip="Josh 21:25",
    ),
    "gaza": Site(
        "Gaza", 31.5075, 34.4597, "Q47492", KNOWN,
        modern="Gaza City",
        point="the city, on the ancient mound",
        why="The name has never changed (Ghazzah). The ancient mound lies under the old city.",
        aka=("Azzah", "Gaza City", "Ghazzah"),
        region="Philistia",
        tribe=("Judah",),
        refs="Gen 10:19; Deut 2:23; Josh 10:41; 15:47; Judg 1:18; 16:1, 21; 1 Sam 6:17; 1 Kgs 4:24; 2 Kgs 18:8; Amos 1:6, 7; Acts 8:26",
        namesakes="Azzah, a town of Ephraim (1 Chr 7:28), has the same Hebrew name",
        skip="1 Chr 7:28",
    ),
    "geba": Site(
        "Geba", 31.8575, 35.2611, "Q6109776", PROBABLE,
        modern="Jaba' village, NE of Jerusalem",
        point="the village",
        source="no Wikidata item for an ancient site",
        why="Name preserved; across the gorge from Michmash (1 Sam 14:5); Judah's northern limit 'from Geba to Beersheba' (2 Kgs 23:8)",
        aka=("Jaba'", "Geba of Benjamin", "Maareh Geba"),
        region="Benjamin",
        tribe=("Benjamin",),
        levitical=True,
        refs="Josh 18:24; 21:17; 1 Sam 13:3, 16; 14:5; 1 Kgs 15:22; 2 Kgs 23:8; 1 Chr 6:60; Neh 11:31; Isa 10:29; Zech 14:10",
        namesakes="Easily confused with Gibeah and Gibeon in the Hebrew; 2 Sam 5:25 'from Geba to Gezer' is Gibeon in 1 Chr 14:16",
    ),
    "gennesaret": Site(
        "Gennesaret", 32.8475, 35.5228, "Q1525069", KNOWN,
        kind="plain",
        modern="The plain of Ginosar on the NW shore, between Magdala and Tel Kinrot; label point at Kibbutz Ginosar (modern)",
        why="Continuous name (Ginosar); Josephus describes the fertile plain; a label point for the plain, not a town",
        aka=("Plain of Ginosar",),
        region="Galilee",
        refs="Matt 14:34; Mark 6:53",
        namesakes="Chinnereth, the OT town at the plain's north end (Tel Kinrot), gave the plain its name",
        skip="Luke 5:1",
    ),
    "gerar": Site(
        "Gerar", 31.3821, 34.6065, "Q770842", PROBABLE,
        modern="Tel Haror (Tell Abu Hureira) on Nahal Gerar",
        point="the tell",
        source="the preferred Wikidata coordinate; the Gerar item's own is deprecated",
        why="Oren's identification, now the consensus; Tell Jemmeh was proposed earlier",
        aka=("Tel Haror", "Tell Abu Hureira"),
        region="the South",
        refs="Gen 10:19; 20:1, 2; 26:1, 6, 17, 20, 26; 2 Chr 14:13, 14",
    ),
    "gergesa": Site(
        "Gergesenes", 32.8261, 35.6504, "Q2469418", POSSIBLE,
        modern="Kursi on the east shore of the Sea of Galilee",
        point="the Byzantine monastery site",
        why="Origen's Gergesa, kept by the Byzantine shrine at Kursi, where a steep slope meets the shore; tradition, not proof.",
        aka=("Gergesa", "Kursi"),
        region="Golan",
        refs="Matt 8:28",
        namesakes="The Gadarenes (Mark 5:1; Luke 8:26), the same story",
    ),
    "gezer": Site(
        "Gezer", 31.8599, 34.9196, "Q1466687", KNOWN,
        modern="Tel Gezer (Tell Jezer / Tell Abu Shusha)",
        why="Inscriptions: Hebrew boundary stones reading 'boundary of Gezer' are cut into the rock around the tell. Excavated by Macalister and Dever.",
        aka=("Tel Gezer", "Tell Jezer", "Tell Abu Shusha"),
        region="the lowland",
        tribe=("Ephraim",),
        levitical=True,
        refs="Josh 10:33; 12:12; 16:3, 10; 21:21; Judg 1:29; 2 Sam 5:25; 1 Kgs 9:15, 16, 17; 1 Chr 14:16; 20:4",
    ),
    "gibbethon": Site(
        "Gibbethon", 31.8545, 34.8659, "Q11298139", PROBABLE,
        modern="Tel Malot (Tell el-Melat), by Gibbeton",
        why="Scholarly consensus for Tel Malot. Sargon II's reliefs show the siege of Gabbutunu.",
        aka=("Tel Malot", "Tell el-Melat"),
        region="Philistia",
        tribe=("Dan",),
        levitical=True,
        refs="Josh 19:44; 21:23; 1 Kgs 15:27; 16:15, 17",
    ),
    "gibeah_benjamin": Site(
        "Gibeah", 31.8233, 35.2311, "Q137920796", PROBABLE,
        modern="Tell el-Ful, north Jerusalem",
        point="the tell",
        source="Wikidata's Gibeah item Q1021662 carries the same point at deprecated rank",
        why="Robinson and Albright; Albright and Lapp excavations; Josephus' Gabath Saoul 30 stadia from Jerusalem; a minority (Miller, Arnold) holds Saul's Gibeah was Geba",
        aka=("Gibeah of Saul", "Gibeah of Benjamin", "Gibeath", "Tell el-Ful"),
        region="Benjamin",
        tribe=("Benjamin",),
        refs="Judg 19:12, 14; 20:4, 13; 1 Sam 10:26; 11:4; 15:34; 22:6; 2 Sam 21:6; Isa 10:29; Hos 5:8; 9:9",
        namesakes="Gibeah of Judah (Josh 15:57) is another town. Josh 24:33's 'hill of Phinehas' in Ephraim and the 'hill' at Kiriath Jearim (1 Sam 7:1) translate gibeah but are other places. Geba is a different town, though the two are confused (Judg 20:10, 33; 1 Sam 13:3)",
        skip="Josh 15:57",
    ),
    "gibeon": Site(
        "Gibeon", 31.8475, 35.1864, "Q889398", KNOWN,
        modern="el-Jib village and mound, NW of Jerusalem",
        point="the ancient city",
        why="Inscribed jar handles reading gb'n found by Pritchard (1956-62), with the great rock-cut pool (2 Sam 2:13); name preserved in el-Jib",
        region="Benjamin",
        tribe=("Benjamin",),
        levitical=True,
        refs="Josh 9:3, 17; 10:12; 18:25; 21:17; 2 Sam 2:13; 20:8; 1 Kgs 3:4; 1 Chr 16:39; 2 Chr 1:3; Jer 28:1; 41:12",
    ),
    "mount_gilboa": Site(
        "Gilboa", 32.4372, 35.4167, "Q794523", KNOWN,
        kind="mount",
        modern="Mount Gilboa (Jebel Fuqu'a)",
        point="its highest summit, Mount Malkishua (536 m)",
        why="Continuous identification; the name survives in the village of Jelbon on the ridge",
        aka=("Mount Gilboa", "Jebel Fuqu'a", "Mount Malkishua"),
        region="Jezreel Valley",
        refs="1 Sam 28:4; 31:1, 8; 2 Sam 1:6, 21; 21:12; 1 Chr 10:1, 8",
    ),
    "gilgal_ephraim": Site(
        "Gilgal", 32.0306, 35.225, "Q12205684", POSSIBLE,
        modern="Jiljilya village, north of Bethel",
        point="the village",
        source="no Wikidata item for an ancient site",
        why="Name preserved; proposed for the Gilgal Elijah and Elisha left 'down to Bethel' (2 Kgs 2:1-2); others take it as the Jordan-valley Gilgal",
        aka=("Jiljilya", "Elisha's Gilgal"),
        region="Samaria",
        refs="2 Kgs 2:1; 4:38",
        namesakes="Gilgal by Jericho is Joshua's camp; Elisha's Gilgal (2 Kgs 2:1; 4:38) is perhaps this one",
        skip="Deut 11:30; Josh 4:19, 20; 5:9, 10; 9:6; 10:6, 7, 9, 15, 43; 12:23; 14:6; 15:7; Judg 2:1; 3:19; 1 Sam 7:16; 10:8; 11:14, 15; 13:4, 7, 8, 12, 15; 15:12, 21, 33; 2 Sam 19:15, 40; Neh 12:29; Hos 4:15; 9:15; 12:11; Amos 4:4; 5:5; Mic 6:5",
    ),
    "gilgal_jericho": Site(
        "Gilgal", 31.8819, 35.4598, "Q2456319", POSSIBLE,
        modern="near Khirbet el-Mafjar (Hisham's Palace), 2 km NE of Tell es-Sultan",
        point="Hisham's Palace, by the candidate",
        source="the palace's preferred Wikidata coordinate; Wikidata's Gilgal item (Q2289734, 32.0330, 35.4757) is the Neolithic Gilgal I",
        why="'On the east border of Jericho' (Josh 4:19); Muilenburg found Iron Age sherds by Khirbet el-Mafjar, and Khirbet en-Nitla was dug without result. The Neolithic site called Gilgal I, 17 km north, is not Joshua's",
        aka=("Khirbet el-Mafjar", "Hisham's Palace"),
        region="Jordan Valley",
        refs="Josh 4:19, 20; 5:9, 10; 9:6; 10:7; Judg 2:1; 1 Sam 7:16; 11:15; 13:8; 15:33; 2 Sam 19:15",
        namesakes="Elisha's Gilgal (2 Kgs 2:1; 4:38) is perhaps Jiljilya, the other Gilgal on the map; Gilgal by the oaks of Moreh near Shechem (Deut 11:30) and 'Goiim in Gilgal' (Josh 12:23) are not placed; the Gilgal facing the ascent of Adummim (Josh 15:7; Geliloth in Josh 18:17) is on Judah's border; and Beth Gilgal (Neh 12:29)",
        skip="Deut 11:30; Josh 12:23; 15:7; 2 Kgs 2:1; 4:38; Neh 12:29",
    ),
    "gimzo": Site(
        "Gimzo", 31.9308, 34.9464, "Q2907137", KNOWN,
        modern="Jimzu, a depopulated village by moshav Gimzo",
        why="The name survives in Jimzu, southeast of Lod.",
        aka=("Jimzu", "Gimzu"),
        region="Coastal plain",
        refs="2 Chr 28:18",
    ),
    "golan": Site(
        "Golan", 32.7811, 35.9347, "Q4118554", POSSIBLE,
        modern="Saham al-Jawlan, Syria",
        point="the village",
        why="Proposed by Schumacher from the name and Eusebius's 'large village of Gaulon in Batanaea'; not excavated, debated.",
        aka=("Gaulanitis", "Sahem el-Jaulan"),
        region="Bashan",
        tribe=("Manasseh",),
        levitical=True,
        refuge=True,
        refs="Deut 4:43; Josh 20:8; 21:27; 1 Chr 6:71",
        namesakes="The modern Golan Heights takes its name from the district, not the town",
    ),
    "hadid": Site(
        "Hadid", 31.9639, 34.9512, "Q12412089", KNOWN,
        modern="Tel Hadid (al-Haditha)",
        why="The name survives in al-Haditha (the Adida of Maccabees), and Tel Hadid has been excavated.",
        aka=("Adida", "Tel Hadid"),
        region="Coastal plain",
        refs="Ezra 2:33; Neh 7:37; 11:34",
    ),
    "halhul": Site(
        "Halhul", 31.5789, 35.0992, "Q2574933", KNOWN,
        modern="Halhul",
        point="the modern town",
        why="Continuous name",
        region="Judah",
        tribe=("Judah",),
        refs="Josh 15:58",
    ),
    "hammath_naphtali": Site(
        "Hammath", 32.7667, 35.5511, "Q2916538", PROBABLE,
        modern="Hammat Tiberias, the hot springs south of Tiberias",
        point="the national park and archaeological site",
        why="Name (hot springs) preserved at Hammam Tabariyeh; usually taken as the levitical Hammothdor (Josh 21:32)",
        aka=("Hammothdor", "Hammon", "Hammat Tiberias", "Hammam Tabariyeh"),
        region="Sea of Galilee",
        tribe=("Naphtali",),
        levitical=True,
        refs="Josh 19:35; 21:32",
        skip="Josh 19:28; 1 Chr 2:55",
    ),
    "hannathon": Site(
        "Hannathon", 32.7856, 35.2569, "Q2900275", PROBABLE,
        modern="Tel Hanaton (Tell el-Badawiyeh), at the Beth Netofa valley's west end",
        point="the tell",
        why="Consensus: Hinnatuna of the Amarna letters, on the route from Acco to the lake",
        aka=("Tel Hanaton", "Tell el-Badawiyeh", "Hinnatuna"),
        region="Lower Galilee",
        tribe=("Zebulun",),
        refs="Josh 19:14",
    ),
    "hazor_naphtali": Site(
        "Hazor", 33.0183, 35.5692, "Q740138", KNOWN,
        modern="Tel Hazor (Tell el-Qedah)",
        point="the tell",
        why="Firm: the great tell excavated by Yadin and Ben-Tor matches Hazor of the Mari and Amarna texts; six-chambered gate (1 Kgs 9:15)",
        aka=("Tel Hazor", "Tell el-Qedah"),
        region="Upper Galilee",
        tribe=("Naphtali",),
        refs="Josh 11:1, 10, 13; 12:19; 19:36; Judg 4:2, 17; 1 Sam 12:9; 1 Kgs 9:15; 2 Kgs 15:29",
        namesakes="Hazor in the Negev of Judah (Josh 15:23, 25), Hazor of Benjamin (Neh 11:33), Hazor in Arabia (Jer 49:28)",
        skip="Josh 15:23, 25; 19:37; 2 Sam 13:23; Neh 11:33; Jer 49:28, 30, 33",
    ),
    "hebron": Site(
        "Hebron", 31.5251, 35.1022, "Q13577875", KNOWN,
        modern="Tel Rumeida, the ancient mound in Hebron",
        why="Continuous name; Bronze and Iron Age city excavated on Tel Rumeida",
        aka=("Kiriath Arba", "Tel Rumeida"),
        region="Judah",
        tribe=("Judah",),
        levitical=True,
        refuge=True,
        refs="Gen 13:18; 23:2; Num 13:22; Josh 10:36; 14:13; 15:54; 20:7; 21:13; 2 Sam 2:1, 11; 5:3; 15:10",
        skip="Exod 6:18; Num 3:19; 1 Chr 2:43; 6:2, 18; 15:9; 23:12, 19; 24:23",
    ),
    "mount_hermon": Site(
        "Hermon", 33.4165, 35.8578, "Q131619088", KNOWN,
        kind="mount",
        modern="Mount Hermon (Jebel esh-Sheikh)",
        point="its summit (2,814 m)",
        why="Continuous identification of the Anti-Lebanon's southern massif, Israel's northern landmark",
        aka=("Mount Hermon", "Sirion", "Senir", "Mount Sion", "Jebel esh-Sheikh"),
        region="Mount Hermon",
        refs="Deut 3:8, 9; 4:48; Josh 11:17; 12:1; 13:11; Judg 3:3; 1 Chr 5:23; Ps 89:12; 133:3; Song 4:8",
    ),
    "heshbon": Site(
        "Heshbon", 31.8008, 35.8089, "Q1615584", PROBABLE,
        modern="Tell Hesban, Jordan",
        point="the tell",
        source="from the Wikipedia article: Wikidata's two coordinates disagree and lie 1.6-2 km off it",
        why="Continuous name (Esbus, Hesban) and Iron II remains; but no Late Bronze town, so Sihon's Heshbon is debated (Jalul proposed).",
        aka=("Esbus", "Tell Hesban"),
        region="Moab",
        tribe=("Reuben",),
        levitical=True,
        refs="Num 21:25, 26, 30; 32:37; Deut 2:24; Josh 12:2; 13:17; 21:39; Judg 11:26; Song 7:4; Isa 15:4; Jer 48:2",
    ),
    "hormah": Site(
        "Hormah", 31.2131, 34.9666, "Q3517239", POSSIBLE,
        modern="Tel Masos (Khirbet el-Meshash), east of Beersheba",
        why="One of several candidates (Tel Masos, Tel Halif, Tel Ira)",
        aka=("Zephath", "Tel Masos", "Khirbet el-Meshash"),
        region="the South",
        tribe=("Judah", "Simeon"),
        refs="Num 14:45; 21:3; Deut 1:44; Josh 12:14; 15:30; 19:4; Judg 1:17; 1 Sam 30:30; 1 Chr 4:30",
    ),
    "hukkok": Site(
        "Hukkok", 32.8847, 35.4789, "Q18608506", PROBABLE,
        modern="Huqoq (Yaquq), above the Ginosar plain",
        point="the ancient village site",
        why="Name preserved at Yaquq (Talmudic Huqoq); some prefer a site farther west for Naphtali's border",
        aka=("Huqoq", "Yaquq"),
        region="Lower Galilee",
        tribe=("Naphtali",),
        refs="Josh 19:34",
        namesakes="Hukok, a levitical town of Asher (1 Chr 6:75)",
    ),
    "ibleam": Site(
        "Ibleam", 32.4459, 35.2926, "Q7049086", KNOWN,
        modern="Khirbet Bal'ama, south of Jenin",
        point="the archaeological site",
        why="Continuous name (Bal'ama); listed by Thutmose III; Bileam of 1 Chr 6:70",
        aka=("Bileam", "Khirbet Bal'ama", "Belameh"),
        region="Jezreel Valley",
        tribe=("Manasseh",),
        refs="Josh 17:11; Judg 1:27; 2 Kgs 9:27; 1 Chr 6:70",
    ),
    "ijon": Site(
        "Ijon", 33.3453, 35.59, "Q15949767", PROBABLE,
        modern="Tell Dibbine, in the Marj Ayyun plain, Lebanon",
        point="the tell",
        why="The name survives in the plain of Marj Ayyun; Tell ed-Dibbin is the accepted tell (Robinson onward)",
        aka=("Tell Dibbine", "Tell ed-Dibbin", "Marj Ayyun"),
        region="Huleh Valley",
        refs="1 Kgs 15:20; 2 Kgs 15:29; 2 Chr 16:4",
    ),
    "iron_naphtali": Site(
        "Iron", 33.0833, 35.4167, "Q4119114", PROBABLE,
        modern="Yaroun, Lebanon",
        point="the modern village",
        why="Name preserved at Yaroun in Naphtali's hill country; accepted by most atlases",
        aka=("Yiron", "Yaroun"),
        region="Upper Galilee",
        tribe=("Naphtali",),
        refs="Josh 19:38",
        namesakes="iron, the metal (Job 28:2; Prov 27:17)",
        skip="Job 28:2; Prov 27:17",
    ),
    "jabesh_gilead": Site(
        "Jabesh Gilead", 32.399, 35.5951, "Q2905361", POSSIBLE,
        modern="Tell Abu al-Kharaz, Jordan",
        point="the tell",
        source="Wikidata's Jabesh-Gilead item carries the same coordinate",
        why="Tell Abu al-Kharaz on Wadi Yabis, which keeps the name (Glueck, Fischer), vs Tell el-Maqlub 8 km upstream (fits Eusebius's 6 miles from Pella); debated.",
        aka=("Jabesh", "Tell Abu al-Kharaz"),
        region="Gilead",
        refs="Judg 21:8, 10, 12; 1 Sam 11:1, 9; 31:11, 13; 2 Sam 2:4, 5; 21:12; 1 Chr 10:12",
        namesakes="Jabesh the father of Shallum (2 Kings 15:10-14), a person",
        skip="2 Kgs 15:10, 13, 14",
    ),
    "jabneh": Site(
        "Jabneh", 31.8656, 34.7479, "Q86000570", KNOWN,
        modern="Tel Yavne (Yibna), in modern Yavne",
        why="The name has never changed (Yibna/Yavne). Josh 15:11's Jabneel, the end of Judah's north border at the sea, is the same town. Jamnia is not a WEB name.",
        aka=("Jabneel", "Jamnia", "Yavne", "Yibna"),
        region="Philistia",
        tribe=("Judah",),
        refs="Josh 15:11; 2 Chr 26:6",
        namesakes="Jabneel of Naphtali (Josh 19:33)",
        skip="Josh 19:33",
    ),
    "jacobs_well": Site(
        "Jacob’s well", 32.2094, 35.2854, "Q1679519", KNOWN,
        kind="well",
        modern="Bir Ya'qub, in the Greek Orthodox church at Balata, Nablus",
        point="the well",
        why="Continuous tradition since the Bordeaux Pilgrim (333) and Eusebius; a deep well below Mount Gerizim, about 600 m from Tell Balata",
        aka=("Bir Ya'qub", "Jacob's Well"),
        region="Samaria",
        refs="John 4:6",
    ),
    "jahaz": Site(
        "Jahaz", 31.589, 35.908, "Q132891416", POSSIBLE,
        modern="Khirbat al-Mudayna on the Wadi ath-Thamad, Jordan",
        point="the site",
        why="Proposed by Dearman and its excavators (an Iron Age fort fitting Mesha's Yahas); Khirbet Libb, Jalul and others also named.",
        aka=("Jahzah", "Yahas", "Khirbet el-Mudayna"),
        region="Moab",
        tribe=("Reuben",),
        levitical=True,
        refs="Num 21:23; Deut 2:32; Josh 13:18; 21:36; Judg 11:20; 1 Chr 6:78; Isa 15:4; Jer 48:21, 34",
    ),
    "janoah_ephraim": Site(
        "Janoah", 32.1454, 35.3557, "Q8048992", PROBABLE,
        modern="Yanun village, SE of Nablus",
        point="the village",
        source="no Wikidata item for Khirbet Yanun",
        why="Name preserved; Eusebius' Ianoa 12 miles east of Neapolis; fits Ephraim's border going down toward the Jordan (Josh 16:6-7)",
        aka=("Yanun", "Khirbet Yanun"),
        region="Samaria",
        tribe=("Ephraim",),
        refs="Josh 16:6, 7",
        namesakes="Janoah taken by Tiglath-pileser (2 Kgs 15:29) is another town, in Naphtali",
        skip="2 Kgs 15:29",
    ),
    "japhia": Site(
        "Japhia", 32.6869, 35.2753, "Q2468131", PROBABLE,
        modern="Yafa an-Naseriyye, south-west of Nazareth",
        point="the modern village",
        why="Name preserved at Yafa (Josephus's Japha)",
        aka=("Yafa an-Naseriyye", "Japha"),
        region="Lower Galilee",
        tribe=("Zebulun",),
        refs="Josh 19:12",
        skip="Josh 10:3; 2 Sam 5:15; 1 Chr 3:7; 14:6",
    ),
    "jarmuth_judah": Site(
        "Jarmuth", 31.7083, 34.975, "Q786554", PROBABLE,
        modern="Tel Yarmuth (Khirbet Yarmuk)",
        why="The name survives in Khirbet Yarmuk, and the setting fits. De Miroschedji excavated the site, but the identification rests on the name.",
        aka=("Tel Yarmuth", "Khirbet Yarmuk"),
        region="the lowland",
        tribe=("Judah",),
        refs="Josh 10:3, 5, 23; 12:11; 15:35; Neh 11:29",
        namesakes="Jarmuth of Issachar, a Levites' city (Josh 21:29)",
        skip="Josh 21:29",
    ),
    "jattir": Site(
        "Jattir", 31.3525, 35.0161, "Q11978271", KNOWN,
        modern="Khirbet Attir, on the south edge of the Hebron hills",
        why="Continuous name; Eusebius",
        aka=("Khirbet Attir", "Khirbet Yattir", "Horvat Yatir"),
        region="Judah",
        tribe=("Judah",),
        levitical=True,
        refs="Josh 15:48; 21:14; 1 Sam 30:27; 1 Chr 6:57",
        source="the first coordinate of the biblical town's Wikidata item",
    ),
    "jazer": Site(
        "Jazer", 31.9445, 35.8301, "Q86670632", POSSIBLE,
        modern="Khirbet es-Sar, western Amman, Jordan",
        point="the site",
        why="One of several candidates (Khirbet es-Sar, Tell el-'Areme, Khirbet Jazzir); the Amorite city on Ammon's border is unfixed.",
        aka=("Jazer of Gilead", "Khirbet es-Sar"),
        region="Gilead",
        tribe=("Gad",),
        levitical=True,
        refs="Num 21:32; 32:1, 3, 35; Josh 13:25; 21:39; 2 Sam 24:5; 1 Chr 6:81; 26:31; Isa 16:8, 9; Jer 48:32",
    ),
    "jehud": Site(
        "Jehud", 32.0333, 34.8833, "Q1000887", PROBABLE,
        modern="Yehud (al-Yahudiyya)",
        why="The name survives in al-Yahudiyya, now the town of Yehud.",
        aka=("Yehud",),
        region="Coastal plain",
        tribe=("Dan",),
        refs="Josh 19:45",
    ),
    "jericho": Site(
        "Jericho", 31.8717, 35.4446, "Q2402267", KNOWN,
        modern="Tell es-Sultan, beside the spring 'Ein es-Sultan, north of modern Jericho (er-Riha)",
        point="the tell",
        why="Spring and continuous name in er-Riha; Garstang, Kenyon and Italian-Palestinian excavations. In Jesus' day the town lay 2 km south, by Herod's winter palaces at Tulul Abu el-Alayiq",
        aka=("Ariha", "Tell es-Sultan"),
        region="Jordan Valley",
        tribe=("Benjamin",),
        refs="Josh 2:1; 5:13; 6:1, 2, 26; 16:1; 18:21; 1 Kgs 16:34; 2 Kgs 2:4, 5, 18; 25:5; Matt 20:29; Mark 10:46; Luke 10:30; 18:35; 19:1; Heb 11:30",
    ),
    "jerusalem": Site(
        "Jerusalem", 31.7767, 35.2342, "Q213274", KNOWN,
        modern="Old City of Jerusalem",
        point="the walled Old City",
        source="the City of David ridge, Q1177750 at 31.7730, 35.2348, lies 400 m south",
        why="Continuous name and occupation; City of David and Temple Mount excavations",
        aka=("Jebus", "Salem", "Zion", "David's city", "City of David", "Old City"),
        region="Judah",
        tribe=("Benjamin",),
        refs="Josh 10:1; 15:8, 63; 18:28; 2 Sam 5:6; 1 Kgs 8:1; 2 Kgs 25:9; 2 Chr 3:1; Neh 2:17; Matt 21:10; Luke 2:22; Acts 1:8",
        skip="Gal 4:26; Heb 12:22; Rev 3:12; 14:1; 21:2, 10",
    ),
    "jezreel_issachar": Site(
        "Jezreel", 32.5579, 35.328, "Q2914898", KNOWN,
        modern="Tel Jezreel (Zir'in), on the Gilboa spur",
        point="the tell",
        why="Continuous name (Zir'in); excavated Omride royal enclosure",
        aka=("Tel Jezreel", "Zir'in"),
        region="Jezreel Valley",
        tribe=("Issachar",),
        refs="Josh 19:18; 1 Sam 29:1; 2 Sam 4:4; 1 Kgs 18:45, 46; 21:1, 23; 2 Kgs 9:30, 36; 10:11; Hos 1:4",
        namesakes="Jezreel in the hill country of Judah (Josh 15:56; 1 Sam 25:43)",
        skip="Josh 15:56; 1 Sam 25:43; 1 Chr 4:3; Hos 1:11; 2:22",
    ),
    "jogbehah": Site(
        "Jogbehah", 32.0256, 35.8644, "Q3505791", PROBABLE,
        modern="al-Jubayhah (el-Jubeihat), a district of Amman, Jordan",
        point="the district",
        why="Continuous name (el-Jubeihat / Ajbeihat) on the road east of Gideon's pursuit; consensus.",
        aka=("Jubeiha",),
        region="Gilead",
        refs="Num 32:35; Judg 8:11",
    ),
    "jokneam": Site(
        "Jokneam", 32.6641, 35.1083, "Q4026101", KNOWN,
        modern="Tel Yokneam (Tell Qamun), at the Jezreel valley's north-west pass",
        point="the tell",
        why="Name preserved in Qamun (Cyamon); excavated Bronze-Iron Age tell",
        aka=("Tel Yokneam", "Tell Qamun", "Cyamon"),
        region="Jezreel Valley",
        tribe=("Zebulun",),
        levitical=True,
        refs="Josh 12:22; 19:11; 21:34",
        namesakes="Jokmeam (1 Kgs 4:12; 1 Chr 6:68), a different town",
    ),
    "joppa": Site(
        "Joppa", 32.0522, 34.7531, "Q180294", KNOWN,
        modern="Jaffa (Tel Yafo), Tel Aviv-Yafo",
        why="The name has never changed (Yafa/Jaffa), and the ancient mound, Tel Yafo, has been excavated.",
        aka=("Jaffa", "Japho", "Yafo"),
        region="Coastal plain",
        tribe=("Dan",),
        refs="Josh 19:46; 2 Chr 2:16; Ezra 3:7; Jonah 1:3; Acts 9:36, 38, 43; 10:5, 23; 11:5",
    ),
    "juttah": Site(
        "Juttah", 31.4478, 35.09, "Q2282208", KNOWN,
        modern="Yatta, south of Hebron",
        point="the modern town, over the ancient site",
        why="Continuous name; Eusebius",
        aka=("Jutah", "Yatta"),
        region="Judah",
        tribe=("Judah",),
        levitical=True,
        refs="Josh 21:16",
    ),
    "kadesh_barnea": Site(
        "Kadesh Barnea", 30.642, 34.4382, "Q60790475", PROBABLE,
        modern="Tell el-Qudeirat by Ein el-Qudeirat, in Sinai",
        why="The region's richest spring, with an Iron Age fort; the name lingers at Ein Qadeis, 8 km south-east",
        aka=("Kadesh", "En Mishpat", "Meribah of Kadesh", "Tell el-Qudeirat", "Ein el-Qudeirat"),
        region="the wilderness of Zin",
        refs="Num 32:8; 34:4; Deut 1:2, 19; 2:14; 9:23; Josh 10:41; 14:6, 7; 15:3",
        namesakes="Kedesh in Galilee (Joshua 20:7) and Kedesh in the Negev (Joshua 15:23)",
        skip="Ps 29:8",
    ),
    "kamon": Site(
        "Kamon", 32.5717, 35.7344, "Q12233554", POSSIBLE,
        modern="Qumaym (Qamm), Irbid district, Jordan",
        point="the village",
        why="Name likeness to Polybius's Kamous and modern Qamm/Qumeim in north Gilead; Jair's burial place, otherwise unknown.",
        aka=("Qamm", "Qumeim", "Camus"),
        region="Gilead",
        refs="Judg 10:5",
    ),
    "kanah_asher": Site(
        "Kanah", 33.2092, 35.2992, "Q753812", PROBABLE,
        modern="Qana, Lebanon, about 11 km south-east of Tyre",
        point="the modern village",
        why="Name preserved at Qana in Asher's north; most atlases (Aharoni, Rainey) place it there",
        aka=("Qana",),
        region="Phoenicia",
        tribe=("Asher",),
        refs="Josh 19:28",
        namesakes="The brook Kanah, the Ephraim-Manasseh border (Josh 16:8; 17:9)",
        skip="Josh 16:8; 17:9",
    ),
    "kedesh_naphtali": Site(
        "Kedesh", 33.1116, 35.5295, "Q2585161", KNOWN,
        modern="Tel Kedesh (Qadas), above the Huleh valley",
        point="the tell",
        why="Continuous name (Qadas); excavated tell with a Persian-Hellenistic administrative building",
        aka=("Kedesh in Galilee", "Kedesh Naphtali", "Tel Kedesh", "Qadas"),
        region="Upper Galilee",
        tribe=("Naphtali",),
        levitical=True,
        refuge=True,
        refs="Josh 12:22; 19:37; 20:7; 21:32; Judg 4:6, 9, 10; 2 Kgs 15:29; 1 Chr 6:76",
        namesakes="Kedesh in the Negev of Judah (Josh 15:23); Kedesh of Issachar (1 Chr 6:72, Kishion); a Kedesh near the lake is argued for Judg 4:11",
        skip="Josh 15:23; Judg 4:11; 1 Chr 6:72",
    ),
    "keilah": Site(
        "Keilah", 31.6163, 35.003, "Q7267724", KNOWN,
        modern="Khirbet Qila",
        point="the village of Qila, by the ruin",
        source="the Keilah item has no coordinate",
        why="Continuous name; Eusebius",
        aka=("Khirbet Qeila", "Khirbet Qeiyla", "Khirbet Qila", "Qila"),
        region="the lowland",
        tribe=("Judah",),
        refs="Josh 15:44; 1 Sam 23:1, 2, 5, 7, 8, 12, 13; Neh 3:17, 18",
    ),
    "kenath": Site(
        "Kenath", 32.7556, 36.6167, "Q763167", PROBABLE,
        modern="Qanawat, Syria",
        point="the village among the ruins of Kanatha",
        why="Kenath = Graeco-Roman Kanatha = Qanawat is the usual view, from the name; some separate Kenath and Kanatha.",
        aka=("Nobah", "Kanatha", "Qanawat"),
        region="Bashan",
        refs="Num 32:42; 1 Chr 2:23",
        namesakes="Nobah is also the man who renamed it (Numbers 32:42) and a place by Jogbehah (Judges 8:11)",
        skip="Judg 8:11",
    ),
    "kir_hareseth": Site(
        "Kir Hareseth", 31.1844, 35.705, "Q31572", PROBABLE,
        modern="al-Karak (Kerak), Jordan, on its isolated plateau",
        point="the town",
        why="Name chain Kir -> Aramaic Karak -> Charachmoba -> al-Karak (Targum reads 'Kerak of Moab'); no Iron Age excavation.",
        aka=("Kir Heres", "Kir of Moab", "Charachmoba", "Kerak"),
        region="Moab",
        refs="2 Kgs 3:25; Isa 15:1; 16:7, 11; Jer 48:31, 36",
        namesakes="Kir in Mesopotamia, where the Arameans were exiled (2 Kings 16:9; Amos 1:5; 9:7)",
    ),
    "kiriath_jearim": Site(
        "Kiriath Jearim", 31.809, 35.1038, "Q3303084", PROBABLE,
        modern="Tel Qiryat Ye'arim (Deir el-Azar), above Abu Ghosh",
        point="the tell",
        why="Eusebius 9-10 miles from Jerusalem on the road to Diospolis; Robinson; Finkelstein-Romer excavations (2017-19)",
        aka=("Abu Ghosh", "Baalah", "Baale Judah", "Deir el-Azar", "Deir el-Azhar", "Kiriath", "Kiriath Arim", "Kiriath Baal"),
        region="Judah",
        tribe=("Judah",),
        refs="Josh 9:17; 15:9, 60; 18:14, 15; Judg 18:12; 1 Sam 6:21; 7:1, 2; 2 Sam 6:2; 1 Chr 13:5; 2 Chr 1:4; Jer 26:20",
        namesakes="Judah's city on the Judah-Benjamin border (Josh 15:60; also in Benjamin's list as 'Kiriath', Josh 18:28); not Kiriath Arba (Hebron) or Kiriathaim (Moab)",
        skip="Gen 23:2; 35:27; Num 22:39; Josh 14:15; 15:11, 13, 15, 16, 29, 49, 54; 20:7; 21:11; Judg 1:10, 11, 12; Neh 11:25",
    ),
    "kiriathaim_moab": Site(
        "Kiriathaim", 31.5406, 35.6861, "Q4704662", POSSIBLE,
        modern="Khirbet el-Qureiyat / al-Qurayyat, Jordan, S of Ataroth",
        point="the al-Qurayyat settlement",
        why="Name likeness (Qureiyat) near Ataroth; one of several candidates (also Qaryat el-Mekhaiyet by Nebo).",
        aka=("Shaveh Kiriathaim", "Qaryaten", "Khirbet el-Qureiyat"),
        region="Moab",
        tribe=("Reuben",),
        refs="Gen 14:5; Num 32:37; Josh 13:19; Jer 48:1, 23; Ezek 25:9",
        namesakes="Kiriathaim in Naphtali, a Levite town (1 Chronicles 6:76)",
        skip="1 Chr 6:76",
    ),
    "kishion": Site(
        "Kishion", 32.6619, 35.3936, "Q12058510", POSSIBLE,
        modern="Tel Qishyon (Khirbet Qasyun), south of Mount Tabor",
        point="the tell",
        why="Proposed from the name Qasyun; Tell el-Muqarqash and other sites are also argued",
        aka=("Tel Qishyon", "Khirbet Qasyun", "Kedesh of Issachar"),
        region="Lower Galilee",
        tribe=("Issachar",),
        levitical=True,
        refs="Josh 19:20; 21:28",
    ),
    "lachish": Site(
        "Lachish", 31.5653, 34.8492, "Q848509", KNOWN,
        modern="Tell ed-Duweir (Tel Lachish)",
        why="Firm excavation: Eusebius's distance from Eleutheropolis, the Lachish ostraca, and the siege ramp that matches Sennacherib's relief.",
        aka=("Tel Lachish", "Tell ed-Duweir"),
        region="the lowland",
        tribe=("Judah",),
        refs="Josh 10:3, 31, 32; 12:11; 15:39; 2 Kgs 14:19; 18:14; 19:8; 2 Chr 11:9; Neh 11:30; Jer 34:7; Mic 1:13",
    ),
    "lebonah": Site(
        "Lebonah", 32.0711, 35.2411, "Q4702744", KNOWN,
        modern="al-Lubban ash-Sharqiya village",
        point="the village",
        source="no Wikidata item for an ancient tell",
        why="Continuous name; north of Shiloh on the Bethel-Shechem road, as Judg 21:19 says",
        region="Samaria",
        refs="Judg 21:19",
    ),
    "libnah": Site(
        "Libnah", 31.6299, 34.8735, "Q7695565", POSSIBLE,
        modern="Tel Burna (one candidate)",
        why="Debated. Tel Burna is the leading current proposal (Shai's excavations), and Tel Zayit and others have been put forward.",
        aka=("Tel Burna",),
        region="the lowland",
        tribe=("Judah",),
        levitical=True,
        refs="Josh 10:29, 31, 39; 12:15; 15:42; 21:13; 2 Kgs 8:22; 19:8; 23:31; 1 Chr 6:57; Isa 37:8",
        namesakes="Libnah, a wilderness camp (Num 33:20-21)",
        skip="Num 33:20, 21",
    ),
    "lod": Site(
        "Lod", 31.9571, 34.9058, "Q11951104", KNOWN,
        label="Lod · Lydda",
        modern="Tel Lod, the ancient mound in the modern city of Lod",
        why="The name has never changed (al-Ludd/Lod). Tel Lod is the city's ancient mound.",
        aka=("Lydda", "Diospolis", "Ludd"),
        region="Coastal plain",
        refs="1 Chr 8:12; Ezra 2:33; Neh 7:37; 11:35; Acts 9:32, 35, 38",
    ),
    "machpelah": Site(
        "Machpelah", 31.5247, 35.1108, "Q204200", PROBABLE,
        kind="cave",
        modern="Cave of the Patriarchs (Haram al-Ibrahimi) in Hebron",
        why="Tradition marked by Herod's enclosure; Josephus",
        aka=("Cave of the Patriarchs", "Haram al-Ibrahimi"),
        region="Judah",
        refs="Gen 23:9, 17, 19; 25:9; 49:30; 50:13",
    ),
    "madon": Site(
        "Madon", 32.7997, 35.4597, "Q1411801", POSSIBLE,
        modern="Qarne Hittin (Horns of Hattin), west of Tiberias",
        point="the hill",
        why="Aharoni's identification, the name kept at nearby Khirbet Madin; not certain",
        aka=("Qarne Hittin", "Horns of Hattin", "Khirbet Madin"),
        region="Lower Galilee",
        refs="Josh 11:1; 12:19",
    ),
    "magdala": Site(
        "Magdala", 32.8271, 35.5136, "Q6844059", PROBABLE,
        modern="Magdala excavations at al-Majdal (Migdal), west shore",
        point="the synagogue site",
        source="Wikidata's Magdala item, Q4880851, sits 1.4 km north-west of the dig",
        why="Name preserved at al-Majdal; excavated 1st-century town and synagogue on the shore",
        aka=("Magadan", "Migdal", "Migdal Nunaya", "Migdal Nunayya", "Tarichaea", "Taricheae"),
        region="Sea of Galilee",
        refs="Matt 15:39",
        skip="Josh 15:37; 19:38",
    ),
    "mahanaim": Site(
        "Mahanaim", 32.1857, 35.6867, "Q27124634", POSSIBLE,
        modern="Tell edh-Dhahab el-Gharbi, the western of the twin Tulul adh-Dhahab on the Jabbok, Jordan",
        point="that tell",
        why="Western twin of Tulul adh-Dhahab is one proposal (with Penuel on the eastern); Tell Hajjaj and Khirbet Mahneh also argued.",
        aka=("Tell edh-Dhahab el-Gharbi",),
        region="Gilead",
        tribe=("Gad",),
        levitical=True,
        refs="Gen 32:2; Josh 13:26, 30; 21:38; 2 Sam 2:8, 29; 17:24, 27; 1 Kgs 2:8; 4:14; 1 Chr 6:80",
        skip="Song 6:13",
    ),
    "makkedah": Site(
        "Makkedah", 31.5347, 34.9666, "Q4132286", POSSIBLE,
        modern="Khirbet el-Qom (one candidate), near Beit Maqdum",
        why="Debated. Khirbet el-Qom (Dorsey, Rainey) lies by Beit Maqdum, whose name echoes Makkedah, but no excavation confirms it.",
        aka=("Khirbet el-Qom", "Beit Maqdum"),
        region="the lowland",
        tribe=("Judah",),
        refs="Josh 10:10, 16, 17, 21, 28, 29; 12:16; 15:41",
    ),
    "mamre": Site(
        "Mamre", 31.5565, 35.1053, "Q2143048", PROBABLE,
        modern="Ramat el-Khalil, 3 km north of Hebron (Herodian and Constantinian enclosure)",
        why="Josephus, Eusebius and Constantine's basilica place Abraham's oak here",
        aka=("Ramat el-Khalil", "Haram Ramet el-Khalil", "Elonei Mamre"),
        region="Judah",
        refs="Gen 13:18; 18:1; 23:17, 19; 25:9; 35:27; 49:30; 50:13",
        namesakes="Mamre the Amorite, Abram's ally (Gen 14:13, 24)",
        skip="Gen 14:24",
    ),
    "maon_judah": Site(
        "Maon", 31.4094, 35.1338, "Q6983688", KNOWN,
        modern="Khirbet Ma'in (Tel Maon), south of Hebron",
        why="Continuous name",
        aka=("Khirbet Ma'in", "Tel Maon"),
        region="Judah",
        tribe=("Judah",),
        refs="Josh 15:55; 1 Sam 23:24, 25; 25:2",
        source="the biblical site's Wikidata item",
        skip="1 Chr 2:45",
    ),
    "mareshah": Site(
        "Mareshah", 31.593, 34.8982, "Q1507676", KNOWN,
        modern="Tel Maresha (Tell Sandahanna), Beit Guvrin National Park",
        why="Eusebius's Maresa beside Eleutheropolis, and Hellenistic tomb inscriptions that name Marisa. The site has been excavated.",
        aka=("Marisa", "Tel Maresha", "Tell Sandahanna"),
        region="the lowland",
        tribe=("Judah",),
        refs="Josh 15:44; 2 Chr 11:8; 14:9, 10; 20:37; Mic 1:15",
        namesakes="Also a man's name (1 Chr 2:42); 1 Chr 4:21's 'father of Mareshah' is the town's founder",
        skip="1 Chr 2:42",
    ),
    "medeba": Site(
        "Medeba", 31.7167, 35.8, "Q1683958", KNOWN,
        modern="Madaba, Jordan, a town on its ancient mound",
        point="the modern town",
        source="the modern town, to the arc-minute",
        why="Continuous name; named in the Mesha Stele; the tell lies under the town centre.",
        aka=("Mehadaba", "Madaba"),
        region="Moab",
        tribe=("Reuben",),
        refs="Num 21:30; Josh 13:9, 16; 1 Chr 19:7; Isa 15:2",
    ),
    "megiddo": Site(
        "Megiddo", 32.5853, 35.1844, "Q208379", KNOWN,
        modern="Tel Megiddo (Tell el-Mutesellim)",
        point="the tell",
        why="Firm: excavated city with Egyptian records of Thutmose III's siege and the Shoshenq stele fragment",
        aka=("Megiddon", "Tel Megiddo", "Tell el-Mutesellim", "Armageddon"),
        region="Jezreel Valley",
        tribe=("Manasseh",),
        refs="Josh 12:21; 17:11; Judg 1:27; 5:19; 1 Kgs 4:12; 9:15; 2 Kgs 9:27; 23:29, 30; 2 Chr 35:22; Zech 12:11; Rev 16:16",
    ),
    "mephaath": Site(
        "Mephaath", 31.4997, 35.9197, "Q822842", PROBABLE,
        modern="Umm ar-Rasas, Jordan",
        point="the site",
        why="Byzantine mosaic inscriptions name the place Kastron Mefaa; the Iron Age town is presumed the same or close by.",
        aka=("Kastron Mefaa", "Umm ar-Rasas"),
        region="Moab",
        tribe=("Reuben",),
        levitical=True,
        refs="Josh 13:18; 21:37; 1 Chr 6:79; Jer 48:21",
    ),
    "michmash": Site(
        "Michmash", 31.8719, 35.2761, "Q3809153", KNOWN,
        modern="Mukhmas village",
        point="the village",
        source="Wikidata's 'Michmash' item; the village is Q6849813",
        why="Continuous name Mukhmas; facing Geba across the Wadi Suwenit gorge exactly as 1 Sam 14:4-5 describes",
        aka=("Michmas", "Mukhmas"),
        region="Benjamin",
        refs="1 Sam 13:2, 5, 16, 23; 14:5, 31; Neh 11:31; Isa 10:28",
    ),
    "misrephoth_maim": Site(
        "Misrephoth Maim", 33.088, 35.1059, "Q7059481", POSSIBLE,
        modern="Khirbet el-Musheirefeh, below Rosh HaNikra",
        point="the archaeological site",
        why="Name echoed at Khirbet el-Musheirefeh near Rosh HaNikra; others take it as the Litani mouth",
        aka=("Khirbet el-Musheirefeh",),
        region="Plain of Acco",
        refs="Josh 11:8; 13:6",
    ),
    "mizpah_benjamin": Site(
        "Mizpah", 31.8851, 35.2164, "Q1755389", PROBABLE,
        modern="Tell en-Nasbeh, south of el-Bireh",
        point="the tell",
        source="Wikidata's 'Mizpah in Benjamin' item, on the tell Q7697543",
        why="Bade's excavation found a massive Iron Age wall and a Babylonian-period town fitting 1 Kgs 15:22 and Jer 40-41; Nebi Samwil is the main rival",
        aka=("Mizpeh", "Tell en-Nasbeh"),
        region="Benjamin",
        tribe=("Benjamin",),
        refs="Judg 20:1; 21:1; 1 Sam 7:5, 16; 10:17; 1 Kgs 15:22; 2 Kgs 25:23; Neh 3:7; Jer 40:6; 41:1",
        namesakes="Mizpah of Gilead, Jephthah's (Gen 31:49; Judg 10:17; 11:11, 29, 34; Ramath Mizpeh, Josh 13:26); Mizpeh of Moab (1 Sam 22:3); the land of Mizpah under Hermon (Josh 11:3, 8); Mizpeh of the lowland (Josh 15:38). Joshua 18:26 spells this one Mizpeh; Hos 5:1 is unclear",
        skip="Gen 31:49; Josh 11:3, 8; 13:26; 15:38; Judg 10:17; 11:11, 29, 34; 1 Sam 22:3; Hos 5:1",
    ),
    "moresheth_gath": Site(
        "Moresheth Gath", 31.6334, 34.9166, "Q7056545", PROBABLE,
        modern="Tell ej-Judeideh (Tel Goded)",
        why="The usual identification: Eusebius puts Morasthi just east of Eleutheropolis. No inscription confirms it.",
        aka=("Tell ej-Judeideh", "Tel Goded"),
        region="the lowland",
        refs="Mic 1:14",
    ),
    "mount_ebal": Site(
        "Mount Ebal", 32.234, 35.2733, "Q1975866", KNOWN,
        kind="mount",
        modern="Mount Ebal (Jebel Eslamiyeh), north of Nablus",
        point="the mountain",
        why="Continuous name; facing Gerizim across Shechem's pass (Deut 11:29; Josh 8:33); the Iron I installation on its NE slope (Zertal) is a separate point",
        aka=("Jebel Eslamiyeh", "Har Eval"),
        region="Samaria",
        refs="Deut 11:29; 27:4, 13; Josh 8:30, 33",
        namesakes="Ebal is also a son of Shobal (Gen 36:23; 1 Chr 1:40) and of Joktan (1 Chr 1:22)",
    ),
    "mount_gerizim": Site(
        "Mount Gerizim", 32.1994, 35.2728, "Q1288751", KNOWN,
        kind="mount",
        modern="Mount Gerizim (Jebel et-Tur), south of Nablus",
        point="the mountain",
        why="Continuous name and Samaritan tradition; the Samaritan temple precinct excavated on the summit (Magen); faces Ebal across the Shechem pass (Deut 27:12)",
        aka=("Jebel et-Tur", "Har Gerizim"),
        region="Samaria",
        refs="Deut 11:29; 27:12; Josh 8:33; Judg 9:7",
        namesakes="John 4:20's 'this mountain' is Gerizim but does not name it",
    ),
    "mount_nebo": Site(
        "Mount Nebo", 31.7678, 35.7256, "Q680161", KNOWN,
        kind="mount",
        modern="Mount Nebo (Jebel Neba / Siyagha memorial summit), Jordan",
        point="the summit",
        why="Continuous name (Jebel Neba); Byzantine Moses memorial at Siyagha. Pisgah's 'top' is equated with it in Deut 34:1.",
        aka=("Pisgah", "Jebel Neba", "Ras es-Siyagha"),
        region="Moab",
        tribe=("Reuben",),
        refs="Num 21:20; 23:14; Deut 3:27; 32:49; 34:1",
        namesakes="The town of Nebo (Numbers 32:38), not placed",
    ),
    "mount_of_olives": Site(
        "Mount of Olives", 31.7779, 35.2457, "Q205976", KNOWN,
        kind="mount",
        modern="Mount of Olives",
        point="the summit ridge at et-Tur",
        source="the preferred-rank coordinate, by the Chapel of the Ascension",
        why="Continuous name; the ridge east of the Kidron",
        aka=("Olivet", "Jebel et-Tur", "Har HaZeitim"),
        region="Judah",
        refs="2 Sam 15:30; Zech 14:4; Matt 21:1; 24:3; 26:30; Mark 13:3; Luke 19:37; 22:39; John 8:1",
    ),
    "nain": Site(
        "Nain", 32.6333, 35.35, "Q934904", KNOWN,
        modern="Nein, on the north slope of the Hill of Moreh",
        point="the modern village",
        why="Continuous name (Nein)",
        aka=("Na'im", "Nein"),
        region="Jezreel Valley",
        refs="Luke 7:11",
    ),
    "nazareth": Site(
        "Nazareth", 32.7021, 35.2978, "Q430776", KNOWN,
        modern="Nazareth",
        point="the city, over the ancient village",
        why="Continuous name; 1st-century houses excavated beneath the old city",
        aka=("Natzrat", "Nazareth of Galilee"),
        region="Lower Galilee",
        refs="Matt 2:23; 4:13; 21:11; Mark 1:9; Luke 1:26; 2:4, 39, 51; 4:16; John 1:45, 46; Acts 10:38",
    ),
    "neballat": Site(
        "Neballat", 31.9856, 34.9567, "Q4874905", KNOWN,
        modern="Bayt Nabala, a depopulated village",
        why="The name survives in Bayt Nabala, northeast of Lod.",
        aka=("Bayt Nabala", "Beit Nabala"),
        region="Coastal plain",
        refs="Neh 11:34",
    ),
    "ono": Site(
        "Ono", 32.0272, 34.8681, "Q2905286", KNOWN,
        modern="Kafr 'Ana, a depopulated village now within Or Yehuda",
        why="The name survives in Kafr 'Ana, beside Lod and Hadid (Ezra 2:33).",
        aka=("Kafr 'Ana",),
        region="Coastal plain",
        refs="1 Chr 8:12; Ezra 2:33; Neh 6:2; 7:37; 11:35",
    ),
    "ophrah_benjamin": Site(
        "Ophrah", 31.9544, 35.3003, "Q931667", PROBABLE,
        label="Ophrah · Ephraim",
        modern="Taybeh (et-Taiyibeh) village, NE of Ramallah",
        point="the village",
        source="no Wikidata item for an ancient site",
        why="Eusebius' Aphra, five miles east of Bethel. The town called Ephraim near the wilderness (John 11:54), and Ephron (2 Chr 13:19), are probably the same place.",
        aka=("Ephraim", "Ephron", "Aphairema", "Taybeh"),
        region="Benjamin",
        tribe=("Benjamin",),
        refs="Josh 18:23; 1 Sam 13:17; 2 Sam 13:23; John 11:54",
        namesakes="Gideon's Ophrah of the Abiezrites (Judg 6:11; 8:27) is another town, in Manasseh, not placed; the tribe and hill country of Ephraim are not this town.",
        skip="Gen 23:8, 10, 13, 14, 16, 17; 25:9; 41:52; 46:20; 48:1, 5, 13, 14, 17, 20; 49:29, 30; 50:13, 23; Num 1:10, 32, 33; 2:18, 24; 7:48; 10:22; 13:8; 26:28, 35, 37; 34:24; Deut 33:17; 34:2; Josh 14:4; 15:9; 16:4, 5, 8, 9, 10; 17:8, 9, 10, 15, 17; 19:50; 20:7; 21:5, 20, 21; 24:30, 33; Judg 1:29; 2:9; 3:27; 4:5; 5:14; 6:11, 24; 7:24; 8:1, 2, 27, 32; 9:5; 10:1, 9; 12:1, 4, 5, 6, 15; 17:1, 8; 18:2, 13; 19:1, 16, 18; 1 Sam 1:1; 9:4; 14:22; 2 Sam 2:9; 18:6; 20:21; 1 Kgs 4:8; 12:25; 2 Kgs 5:22; 14:13; 1 Chr 4:14; 6:66, 67; 7:20, 22; 9:3; 12:30; 27:10, 14, 20; 2 Chr 13:4; 15:8, 9; 17:2; 19:4; 25:7, 10, 23; 28:7, 12; 30:1, 10, 18; 31:1; 34:6, 9; Neh 8:16; 12:39; Ps 60:7; 78:9, 67; 80:2; 108:8; Isa 7:2, 5, 8, 9, 17; 9:9, 21; 11:13; 17:3; 28:1, 3; Jer 4:15; 7:15; 31:6, 9, 18, 20; 50:19; Ezek 37:16, 19; 48:5, 6; Hos 4:17; 5:3, 5, 9, 11, 12, 13, 14; 6:4, 10; 7:1, 8, 11; 8:9, 11; 9:3, 8, 11, 13, 16; 10:6, 11; 11:3, 8, 9, 12; 12:1, 8, 14; 13:1, 12; 14:8; Obad 1:19; Mic 1:10; Zech 9:10, 13; 10:7",
    ),
    "penuel": Site(
        "Penuel", 32.1833, 35.7, "Q733822", PROBABLE,
        modern="Tell edh-Dhahab esh-Sharqi, the eastern of the twin Tulul adh-Dhahab, Jordan",
        why="The fortified eastern twin on the Jabbok fits Jeroboam's Penuel and Gideon's tower; widely accepted, not proven.",
        aka=("Peniel", "Tell edh-Dhahab esh-Sharqi"),
        region="Gilead",
        refs="Gen 32:30, 31; Judg 8:8, 9, 17; 1 Kgs 12:25",
        namesakes="Penuel, two men of Judah and Benjamin (1 Chronicles 4:4; 8:25)",
        source="Wikidata's Penuel item, to the arc-minute",
        skip="1 Chr 4:4; 8:25",
    ),
    "pirathon": Site(
        "Pirathon", 32.1906, 35.1658, "Q12230582", PROBABLE,
        modern="Far'ata village, SW of Nablus",
        point="the village of Far'ata",
        source="Wikidata's Pirathon item Q2946726 has no coordinate",
        why="Name preserved in Far'ata; 'in the land of Ephraim, in the hill country of the Amalekites' (Judg 12:15)",
        aka=("Far'ata", "Pharathon"),
        region="Samaria",
        refs="Judg 12:15",
        namesakes="Abdon and Benaiah are called Pirathonites (Judg 12:13; 2 Sam 23:30).",
    ),
    "rabbah_ammon": Site(
        "Rabbah", 31.9547, 35.9343, "Q3157009", KNOWN,
        modern="Amman Citadel (Jebel el-Qal'a), Amman, Jordan",
        point="the citadel hill",
        why="Continuous city: Rabbath-Ammon, Ptolemaic Philadelphia, Arabic Amman; Iron Age Ammonite remains on the citadel.",
        aka=("Rabbath Ammon", "Philadelphia", "Amman"),
        region="Ammon",
        refs="Deut 3:11; Josh 13:25; 2 Sam 11:1; 12:26, 27, 29; 17:27; 1 Chr 20:1; Jer 49:2; Ezek 21:20; 25:5; Amos 1:14",
        namesakes="Rabbah in the hill country of Judah (Joshua 15:60); its Greek name Philadelphia is not Revelation's (Revelation 1:11; 3:7)",
        skip="Josh 15:60; Rev 1:11; 3:7",
    ),
    "ramah_benjamin": Site(
        "Ramah", 31.85, 35.2317, "Q926868", PROBABLE,
        modern="er-Ram, north of Jerusalem",
        point="the village of er-Ram",
        source="Wikidata's 'Ramah in Benjamin' item; the town is Q775087",
        why="Name preserved; Eusebius 6 miles north of Jerusalem; fits Judg 19:13, Isa 10:29 and Asa-Baasha's border fort (1 Kgs 15:17-22)",
        region="Benjamin",
        tribe=("Benjamin",),
        refs="Josh 18:25; Judg 4:5; 19:13; 1 Kgs 15:17, 22; Ezra 2:26; Neh 11:33; Isa 10:29; Jer 31:15; 40:1; Hos 5:8; Matt 2:18",
        namesakes="Samuel's Ramah (1 Sam 1:19; 7:17; 8:4; 15:34; 16:13; 19:18; 25:1; 28:3) is Ramathaim Zophim (1 Sam 1:1), put at er-Ram by many and at Rantis (Arimathaea) by others; Ramah of Naphtali (Josh 19:36) is on the map; Ramah of Asher (Josh 19:29), 'Ramah of the South' in Simeon (Josh 19:8) and Ramah meaning Ramoth Gilead (2 Kgs 8:29; 2 Chr 22:6) are other places",
        skip="Josh 19:8, 29, 36; 1 Sam 1:19; 2:11; 7:17; 8:4; 15:34; 16:13; 19:18, 19, 22, 23; 20:1; 22:6; 25:1; 28:3; 2 Kgs 8:29; 2 Chr 22:6",
    ),
    "ramah_naphtali": Site(
        "Ramah", 32.9393, 35.3671, "Q2915661", PROBABLE,
        modern="Rameh, at the foot of the Upper Galilee scarp",
        point="the modern village",
        why="Name preserved at er-Rama in Naphtali; the usual identification",
        aka=("Rameh",),
        region="Upper Galilee",
        tribe=("Naphtali",),
        refs="Josh 19:36",
        namesakes="Ramah of Benjamin (Josh 18:25), Ramah of Asher (Josh 19:29), Ramah of the Negev (Josh 19:8), Samuel's Ramah (1 Sam 1:19), Ramoth Gilead",
        skip="Josh 18:25; 19:8, 29; Judg 4:5; 19:13; 1 Sam 1:19; 2:11; 7:17; 8:4; 15:34; 16:13; 19:18, 19, 22, 23; 20:1; 22:6; 25:1; 28:3; 1 Kgs 15:17, 21, 22; 2 Kgs 8:29; 2 Chr 16:1, 5; 22:6; Ezra 2:26; Neh 7:30; 11:33; Isa 10:29; Jer 31:15; 40:1; Hos 5:8; Matt 2:18",
    ),
    "ramoth_gilead": Site(
        "Ramoth Gilead", 32.5, 36.0167, "Q2006096", PROBABLE,
        modern="Tell er-Rumeith, Jordan",
        point="the tell",
        source="Wikidata's Ramoth-Gilead item, to the arc-minute",
        why="Glueck's and Lapp's Tell er-Rumeith (Iron Age fort, destroyed 9th-8th c.) is the majority view; er-Ramtha and Jal'ad also proposed.",
        aka=("Ramoth in Gilead", "Tell er-Rumeith"),
        region="Gilead",
        tribe=("Gad",),
        levitical=True,
        refuge=True,
        refs="Deut 4:43; Josh 20:8; 21:38; 1 Kgs 4:13; 22:3, 29; 2 Kgs 8:28; 9:1, 14; 1 Chr 6:80; 2 Chr 18:28",
        namesakes="Ramah, Ramath Mizpeh (Joshua 13:26) and other Ramahs west of the Jordan",
    ),
    "rehoboth_negev": Site(
        "Rehoboth", 31.0317, 34.565, "Q125923693", POSSIBLE,
        modern="Ruheibeh (Rehovot-in-the-Negev), a Nabataean-Byzantine town south-west of Beersheba",
        point="the ruins",
        source="the first of the item's Wikidata coordinates",
        why="The name survives in Ruheibeh, but nothing of the patriarchal period was found",
        aka=("Rehovot-in-the-Negev", "Ruheibeh"),
        region="the South",
        refs="Gen 26:22",
        namesakes="Rehoboth Ir in Assyria (Genesis 10:11); Rehoboth by the River (Genesis 36:37)",
        skip="Gen 10:11; 36:37; 1 Chr 1:48",
    ),
    "rimmon_rock": Site(
        "Rimmon", 31.9297, 35.2989, "Q7289744", PROBABLE,
        modern="Rammun village, east of Bethel",
        point="the village",
        source="no Wikidata item for the crag itself",
        why="Name preserved; a cave-pocked limestone hill on the edge of the wilderness east of Bethel (Judg 20:45-47); Eusebius' Remmon 15 miles north of Jerusalem",
        aka=("Rammun",),
        region="Benjamin",
        refs="Judg 20:45, 47; 21:13",
        namesakes="Rimmon of Simeon (Josh 15:32; 19:7; Zech 14:10), Rimmon of Zebulun (Josh 19:13), Gath Rimmon (Josh 19:45), the god Rimmon (2 Kgs 5:18) and Rimmon the Beerothite (2 Sam 4:2) are others",
        skip="Num 33:19, 20; Josh 15:32; 19:7, 13, 45; 21:24, 25; 2 Sam 4:2, 5, 9; 2 Kgs 5:18; 1 Chr 4:32; 6:69; Neh 11:29; Zech 14:10",
    ),
    "rimmon_zebulun": Site(
        "Rimmon", 32.7881, 35.3106, "Q2547954", PROBABLE,
        modern="Rumana (Rummaneh), north of Nazareth",
        point="the modern village",
        why="Name preserved at Rummaneh, on Zebulun's eastern border",
        aka=("Rimmono", "Rummaneh", "Rumana"),
        region="Lower Galilee",
        tribe=("Zebulun",),
        refs="Josh 19:13; 1 Chr 6:77",
        namesakes="Rimmon of Simeon/Judah (Josh 15:32; 19:7), the rock of Rimmon in Benjamin (Judg 20:45), Gath Rimmon",
        skip="Num 33:19, 20; Josh 15:32; 19:7, 45; 21:24, 25; Judg 20:45, 47; 21:13; 2 Sam 4:2, 5, 9; 2 Kgs 5:18; 1 Chr 4:32; 6:69; Neh 11:29; Zech 14:10",
    ),
    "rogelim": Site(
        "Rogelim", 32.5324, 35.7732, "Q140774816", POSSIBLE,
        modern="Barsinia (Khirbet Barsiniya), west of Irbid, Jordan",
        point="the site",
        why="F.-M. Abel's identification, disputed; Barzillai's home in north Gilead.",
        aka=("Tell Barsina", "Khirbet Barsiniya"),
        region="Gilead",
        refs="2 Sam 17:27; 19:31",
    ),
    "salecah": Site(
        "Salecah", 32.4914, 36.7106, "Q24343", KNOWN,
        modern="Salkhad, Syria",
        point="the modern town and its citadel hill",
        why="Continuous name (Salkhad, Nabataean Salkhad); Bashan's eastern limit.",
        aka=("Salkhad", "Salcah"),
        region="Bashan",
        refs="Deut 3:10; Josh 12:5; 13:11; 1 Chr 5:11",
    ),
    "samaria": Site(
        "Samaria", 32.2761, 35.195, "Q1757438", KNOWN,
        modern="Sebastia: the ancient city mound",
        point="the site",
        why="Omri's capital (1 Kgs 16:24); continuous name Sebaste > Sebastia; Harvard and Crowfoot excavations, Samaria ostraca",
        aka=("Sebaste", "Sebastia", "Shomron"),
        region="Samaria",
        refs="1 Kgs 16:24, 29; 20:1; 22:37; 2 Kgs 6:24; 17:5, 6; 18:10; Isa 7:9; Amos 4:1; Mic 1:6; Acts 8:5",
        namesakes="Samaria is also the land round it and the northern kingdom (1 Kgs 13:32; Luke 17:11; John 4:4; Acts 1:8; 8:1)",
        skip="1 Kgs 13:32; 2 Kgs 17:24, 26, 28; 23:18, 19; Jer 31:5; Hos 8:5, 6; Obad 1:19; Luke 17:11; John 4:4, 5, 7; Acts 1:8; 8:1, 9, 14; 9:31; 15:3",
    ),
    "sarid": Site(
        "Sarid", 32.6604, 35.2342, "Q6759594", PROBABLE,
        modern="Tel Shadud, on the Jezreel valley's north edge",
        point="the tell",
        why="Consensus (reading Sadid for Sarid); the tell by kibbutz Sarid",
        aka=("Tel Shadud", "Tell Shadud"),
        region="Lower Galilee",
        tribe=("Zebulun",),
        refs="Josh 19:10, 12",
    ),
    "sela_edom": Site(
        "Sela", 30.7714, 35.5831, "Q489724", POSSIBLE,
        modern="es-Sela, a rock fortress near Buseirah, Jordan",
        point="the site",
        why="Es-Sela (name kept, Babylonian Nabonidus relief) vs Umm el-Biyara at Petra; debated.",
        aka=("Selah", "Joktheel"),
        region="Edom",
        refs="2 Kgs 14:7; Isa 42:11",
        namesakes="Sela Hammahlekoth in the wilderness of Maon (1 Samuel 23:28); 'Selah' the psalm word",
        skip="Josh 15:38; 1 Sam 23:28; Ps 3:2, 4, 8; 4:2, 4; 7:5; 9:16, 20; 20:3; 21:2; 24:6, 10; 32:4, 5, 7; 39:5, 11; 44:8; 46:3, 7, 11; 47:4; 48:8; 49:13, 15; 50:6; 52:3, 5; 54:3; 55:7, 19; 57:3, 6; 59:5, 13; 60:4; 61:4; 62:4, 8; 66:4, 7, 15; 67:1, 4; 68:7, 19, 32; 75:3; 76:3, 9; 77:3, 9, 15; 81:7; 82:2; 83:8; 84:4, 8; 85:2; 87:3, 6; 88:7, 10; 89:4, 37, 45, 48; 140:3, 5, 8; 143:6; Hab 3:3, 9, 13",
    ),
    "shaalbim": Site(
        "Shaalbim", 31.8693, 34.9863, "Q7403743", PROBABLE,
        modern="Salbit, a depopulated village by kibbutz Sha'alvim",
        why="Scholarly consensus: Salbit (Selbit), near Aijalon, keeps the name.",
        aka=("Shaalabbin", "Salbit", "Sha'alvim"),
        region="the lowland",
        tribe=("Dan",),
        refs="Josh 19:42; Judg 1:35; 1 Kgs 4:9",
    ),
    "shechem": Site(
        "Shechem", 32.2136, 35.2819, "Q7951237", KNOWN,
        modern="Tell Balata, at the east edge of Nablus",
        point="the tell",
        why="Eusebius puts Sychem by Neapolis; the pass between Gerizim and Ebal; Sellin and G. E. Wright excavations; Amarna letters' Shakmu",
        aka=("Sychem", "Sichem", "Tell Balata", "Neapolis/Nablus"),
        region="Samaria",
        tribe=("Ephraim",),
        levitical=True,
        refuge=True,
        refs="Gen 12:6; 33:18; 37:12; Josh 17:7; 20:7; 21:21; 24:1, 32; Judg 9:6; 1 Kgs 12:1, 25; Acts 7:16",
        namesakes="Shechem is also a person: the son of Hamor (Gen 34) and a clan of Manasseh (Num 26:31; Josh 17:2)",
        skip="Gen 33:19; 34:2, 4, 6, 8, 11, 13, 18, 20, 24, 26; Num 26:31; Josh 17:2; 1 Chr 7:19",
    ),
    "shiloh": Site(
        "Shiloh", 32.0557, 35.2895, "Q985542", KNOWN,
        modern="Khirbet Seilun (Tel Shiloh)",
        point="the tell",
        why="Name preserved; exactly where Judg 21:19 puts it (north of Bethel, east of the Bethel-Shechem road, south of Lebonah); Danish and Finkelstein excavations",
        aka=("Khirbet Seilun", "Tel Shiloh"),
        region="Samaria",
        refs="Josh 18:1, 8; 19:51; 21:2; 22:9; Judg 18:31; 21:19; 1 Sam 1:3; 4:3; 1 Kgs 14:2; Ps 78:60; Jer 7:12",
        namesakes="Taanath Shiloh (Josh 16:6) is a different place on Ephraim's border",
        skip="Josh 16:6",
    ),
    "shimron": Site(
        "Shimron", 32.7039, 35.2133, "Q2916430", PROBABLE,
        modern="Tel Shimron (Tell Semuniyeh), on the Jezreel valley's north edge",
        point="the tell",
        why="Name preserved at Semuniyeh (Josephus's Simonias); excavated large Bronze-Iron Age tell",
        aka=("Shimron Meron", "Tel Shimron", "Khirbet Sammuniyeh", "Simonias"),
        region="Lower Galilee",
        tribe=("Zebulun",),
        refs="Josh 11:1; 12:20; 19:15",
        skip="Gen 46:13; Num 26:24; 1 Chr 7:1",
    ),
    "shittim": Site(
        "Shittim", 31.8402, 35.6737, "Q55634648", PROBABLE,
        modern="Tell el-Hammam, Jordan",
        point="the tell",
        why="Glueck's Tell el-Hammam, the chief Iron Age mound of the plains, is the usual view; Tell Kafrayn (Josephus's Abila) also proposed.",
        aka=("Abel Shittim", "Abila of Peraea", "Tell el-Hammam"),
        region="Jordan Valley",
        refs="Num 25:1; 33:49; Josh 2:1; 3:1; Mic 6:5",
        namesakes="The valley of Shittim in Joel 3:18 (prophetic, perhaps the Kidron)",
        skip="Joel 3:18",
    ),
    "shunem": Site(
        "Shunem", 32.6056, 35.3343, "Q2916070", KNOWN,
        modern="Sulam, on the south slope of the Hill of Moreh",
        point="the village",
        source="Wikidata's Shunem item",
        why="Continuous name (Sulam); Shunama in Egyptian and Amarna texts",
        aka=("Sulam", "Solem"),
        region="Jezreel Valley",
        tribe=("Issachar",),
        refs="Josh 19:18; 1 Sam 28:4; 2 Kgs 4:8",
    ),
    "sidon": Site(
        "Sidon", 33.5606, 35.3758, "Q163490", KNOWN,
        modern="Saida (Sidon), Lebanon",
        point="the modern city",
        why="Continuous name (Saida); Phoenician royal inscriptions (Eshmunazar, Bodashtart) found there",
        aka=("Great Sidon", "Saida", "Sayda", "Zidon"),
        region="Phoenicia",
        tribe=("Asher",),
        refs="Gen 10:19; 49:13; Josh 11:8; 19:28; Judg 1:31; 18:28; 1 Kgs 17:9; Isa 23:4; Ezek 28:22; Matt 15:21; Mark 7:24, 31; Luke 6:17; Acts 27:3",
        skip="Gen 10:15; 1 Chr 1:13",
    ),
    "socoh_shephelah": Site(
        "Socoh", 31.6821, 34.9739, "Q16605124", KNOWN,
        modern="Khirbet Shuweikeh / Khirbet Abbad (Tel Sokho), above the Elah valley",
        why="The name survives in Khirbet Shuweikeh, above the Elah valley; this is also Eusebius's Socchoth.",
        aka=("Soco", "Sokho", "Khirbet Shuweikeh", "Khirbet Abbad"),
        region="the lowland",
        tribe=("Judah",),
        refs="Josh 15:35; 1 Sam 17:1; 2 Chr 11:7; 28:18",
        namesakes="Socoh in the hill country of Judah (Josh 15:48; Khirbet Shuweika near Hebron); Socoh in the Sharon (1 Kgs 4:10)",
        skip="Josh 15:48; 1 Kgs 4:10; 1 Chr 4:18",
    ),
    "succoth": Site(
        "Succoth", 32.1966, 35.6212, "Q27124629", PROBABLE,
        modern="Tell Deir 'Alla, east bank near the Jabbok",
        point="the tell",
        source="a GeoNames item; Wikidata's Succoth item Q1554834 has no coordinate",
        why="The Jerusalem Talmud equates Succoth with Tar'ala (Deir 'Alla); Glueck; Franken excavations (Franken himself doubted and suggested Tell el-Ekhsas)",
        aka=("Tell Deir 'Alla", "Dar'ala", "Tell Deir Alla", "Tar'ala"),
        region="Jordan Valley",
        tribe=("Gad",),
        refs="Gen 33:17; Josh 13:27; Judg 8:5, 6, 8, 14, 16; 1 Kgs 7:46; 2 Chr 4:17; Ps 60:6; 108:7",
        namesakes="Succoth in Egypt (Exod 12:37; 13:20; Num 33:5-6) is the first camp of the Exodus; Succoth Benoth (2 Kgs 17:30) is a deity",
        skip="Exod 12:37; 13:20; Num 33:5, 6; 2 Kgs 17:30",
    ),
    "sychar": Site(
        "Sychar", 32.2199, 35.2974, "Q4302319", POSSIBLE,
        modern="Askar, east of Nablus",
        point="the camp of Askar, by the old village",
        source="Wikidata has no item for the old village",
        why="Debated: the village of Askar near Jacob's well echoes the name, but many take Sychar as Shechem itself (the Syriac reads Shechem)",
        aka=("Askar",),
        region="Samaria",
        refs="John 4:5",
    ),
    "taanach": Site(
        "Taanach", 32.5215, 35.2191, "Q2920206", KNOWN,
        modern="Tel Taanach (Tell Ti'innik), south-east of Megiddo",
        point="the tell",
        why="Continuous name (Ti'innik); excavated tell with cuneiform tablets",
        aka=("Tell Ti'innik", "Tel Ta'anakh"),
        region="Jezreel Valley",
        tribe=("Manasseh",),
        levitical=True,
        refs="Josh 12:21; 17:11; 21:25; Judg 1:27; 5:19; 1 Kgs 4:12; 1 Chr 7:29",
    ),
    "mount_tabor": Site(
        "Tabor", 32.6863, 35.3929, "Q193785", KNOWN,
        kind="mount",
        modern="Mount Tabor (Jebel et-Tur)",
        point="its summit",
        why="Continuous identification of the isolated dome at the Jezreel valley's north-east corner",
        aka=("Mount Tabor", "Jebel et-Tur"),
        region="Lower Galilee",
        tribe=("Issachar",),
        refs="Josh 19:22; Judg 4:6, 12, 14; 8:18; Ps 89:12; Jer 46:18; Hos 5:1",
        namesakes="The oak of Tabor in Benjamin (1 Sam 10:3); the levitical town Tabor of Zebulun (1 Chr 6:77); Chisloth Tabor and Aznoth Tabor",
        skip="Josh 19:12, 34; 1 Sam 10:3; 1 Chr 6:77",
    ),
    "tamar": Site(
        "Tamar", 30.8087, 35.2459, "Q12409412", POSSIBLE,
        modern="Metzad Hatzeva (Ein Hatzeva), in the Arabah",
        why="Cohen's identification of the Iron Age fortress as Ezekiel's south-east corner; other sites are proposed",
        aka=("Tamar in the wilderness", "Ein Hatzeva", "Metzad Hatzeva"),
        region="the Arabah",
        refs="1 Kgs 9:18; Ezek 47:19; 48:28",
        namesakes="Baal Tamar in Benjamin (Judges 20:33); Hazazon Tamar is En Gedi (2 Chronicles 20:2)",
        skip="Gen 14:7; 38:6, 11, 13, 24; Judg 20:33; Ruth 4:12; 2 Sam 13:1, 2, 4, 5, 6, 7, 8, 10, 19, 20, 22, 32; 14:27; 1 Chr 2:4; 3:9; 2 Chr 20:2; Matt 1:3",
    ),
    "tappuah": Site(
        "Tappuah", 32.103, 35.2405, "Q31796638", PROBABLE,
        modern="Sheikh Abu Zarad (Tall Abu Zarad), above Yasuf",
        point="the hill",
        source="a GeoNames item",
        why="Scholarly consensus (Alt, Abel) for the Ephraim-Manasseh border town; the spring En Tappuah at Yasuf below; the name is not preserved",
        aka=("En Tappuah", "Sheikh Abu Zarad", "Tel Tappuah"),
        region="Samaria",
        tribe=("Ephraim",),
        refs="Josh 12:17; 16:8; 17:7, 8",
        namesakes="Tappuah of the Shephelah (Josh 15:34) and Beth Tappuah near Hebron (Josh 15:53) are other towns; Tappuah son of Hebron (1 Chr 2:43) is a person",
        skip="Josh 15:34, 53; 1 Chr 2:43",
    ),
    "tekoa": Site(
        "Tekoa", 31.6341, 35.2102, "Q12412177", KNOWN,
        modern="Khirbet Tuqu'",
        point="the ruin, by the village of Tuqu'",
        source="the ancient town's Wikidata item",
        why="Continuous name; Eusebius; ruins with a Byzantine church",
        aka=("Khirbet Tuqu'", "Teqoa"),
        region="Judah",
        refs="2 Sam 14:2, 4, 9; 2 Chr 11:6; 20:20; Jer 6:1; Amos 1:1",
    ),
    "thebez": Site(
        "Thebez", 32.3222, 35.3686, "Q275919", PROBABLE,
        modern="Tubas",
        point="the modern town",
        source="no Wikidata item for an ancient tell",
        why="The name survives in Tubas; Eusebius puts Thebes 13 miles from Neapolis on the road to Scythopolis",
        aka=("Tubas",),
        region="Samaria",
        refs="Judg 9:50; 2 Sam 11:21",
    ),
    "tiberias": Site(
        "Tiberias", 32.7897, 35.5247, "Q151920", KNOWN,
        modern="Tiberias, west shore",
        point="the modern city (Antipas's city lies at its south end)",
        why="Continuous name; the city Herod Antipas founded about AD 20",
        aka=("Tabariyya", "Teverya", "Tverya"),
        region="Sea of Galilee",
        refs="John 6:23",
        skip="John 6:1; 21:1",
    ),
    "timnah_dan": Site(
        "Timnah", 31.7864, 34.9108, "Q2916736", PROBABLE,
        modern="Tel Batash (Tell el-Batashi), in the Sorek valley",
        why="Scholarly consensus, from the line of Judah's border in Josh 15:10. Excavated by Kelm and Mazar.",
        aka=("Tel Batash", "Tell el-Batashi"),
        region="the lowland",
        tribe=("Judah", "Dan"),
        refs="Josh 15:10; 19:43; Judg 14:1, 2, 5; 2 Chr 28:18",
        namesakes="Timnah in the hill country of Judah (Josh 15:57; perhaps Gen 38:12-14); Timnath Heres in Ephraim (Judg 2:9)",
        skip="Gen 38:12, 13, 14; Josh 15:57",
    ),
    "timnathserah": Site(
        "Timnathserah", 32.0083, 35.1111, "Q17006899", PROBABLE,
        modern="Khirbet Tibnah, NW of Ramallah",
        point="the site",
        why="Name preserved in Tibnah, with large rock-cut tombs (Guerin, Conder); Samaritan and Jewish tradition puts Joshua's tomb at Kifl Haris instead",
        aka=("Timnath Heres", "Khirbet Tibnah"),
        region="Samaria",
        tribe=("Ephraim",),
        refs="Josh 19:50; 24:30",
        namesakes="Not Timnah of Judah and Dan (Josh 15:10; Judg 14:1)",
    ),
    "tirzah": Site(
        "Tirzah", 32.2874, 35.3378, "Q2002121", PROBABLE,
        modern="Tell el-Far'ah (North), at the head of Wadi Far'a",
        point="the tell",
        why="Albright's identification, de Vaux's excavations; a capital before Samaria fits 1 Kgs 14-16; the name is not preserved",
        aka=("Tell el-Far'ah",),
        region="Samaria",
        refs="Josh 12:24; 1 Kgs 14:17; 15:21, 33; 16:8, 15, 23; 2 Kgs 15:14; Song 6:4",
        namesakes="Tirzah is also a daughter of Zelophehad (Num 26:33; 27:1; 36:11; Josh 17:3), whose clan names the district",
        skip="Num 26:33; 27:1; 36:11; Josh 17:3",
    ),
    "tyre": Site(
        "Tyre", 33.2667, 35.2, "Q82070", KNOWN,
        modern="Sur (Tyre), Lebanon, the former island city",
        point="the modern city",
        why="Continuous name (Sur); the island city joined to the shore by Alexander's mole",
        aka=("Sor", "Tsor", "Tyros"),
        region="Phoenicia",
        tribe=("Asher",),
        refs="Josh 19:29; 2 Sam 5:11; 24:7; 1 Kgs 5:1; 9:11; Isa 23:1; Ezek 26:3; 27:3; Amos 1:9; Matt 15:21; Mark 7:24, 31; Acts 12:20; 21:3, 7",
    ),
    "zanoah_shephelah": Site(
        "Zanoah", 31.7186, 35.0007, "Q111475167", KNOWN,
        modern="Khirbet Zanoah (Khirbet Zanu'), south of Beth Shemesh",
        why="The name survives in Khirbet Zanu'; Eusebius calls it Zanoua.",
        aka=("Khirbet Zanu'", "Khirbet Zanoah"),
        region="the lowland",
        tribe=("Judah",),
        refs="Josh 15:34; Neh 3:13; 11:30",
        namesakes="Zanoah in the hill country of Judah (Josh 15:56)",
        skip="Josh 15:56; 1 Chr 4:18",
    ),
    "zarephath": Site(
        "Zarephath", 33.4575, 35.2958, "Q616837", KNOWN,
        modern="Ras el-Qantara tell by Sarafand, Lebanon (Sarepta)",
        point="the tell",
        why="Continuous name (Sarafand); the Phoenician harbour town excavated by Pritchard, 1969-74",
        aka=("Sarafand", "Sarepta"),
        region="Phoenicia",
        refs="1 Kgs 17:9, 10; Obad 1:20; Luke 4:26",
    ),
    "zarethan": Site(
        "Zarethan", 32.2677, 35.5772, "Q1260218", POSSIBLE,
        modern="Tell es-Sa'idiyeh, east bank",
        point="the tell",
        source="its first Wikidata coordinate, 32.3219, 35.56, is a stray 6 km off, so the second is used",
        why="Pritchard's identification, with Bronze and Iron Age metalwork fitting 1 Kgs 7:46; rivals are Tell Umm Hamad (Glueck) and Qarn Sartaba",
        aka=("Tell es-Sa'idiyeh", "Zeredah", "Zererah"),
        region="Jordan Valley",
        refs="Josh 3:16; 1 Kgs 4:12; 7:46; 2 Chr 4:17",
        namesakes="Zeredah of 1 Kgs 11:26, Jeroboam's town in Ephraim, is another place on the map",
        skip="1 Kgs 11:26",
    ),
    "zeredah": Site(
        "Zeredah", 32.0542, 35.0566, "Q6737832", POSSIBLE,
        modern="Horvat Tsreda by 'Ain Seridah, west of Deir Ghassaneh",
        why="The name survives at 'Ain Seridah; an Ephraimite hometown for Jeroboam (1 Kgs 11:26); a proposal, not excavated",
        aka=("Horvat Tsreda", "Khirbet Banat Barr"),
        region="Samaria",
        refs="1 Kgs 11:26",
        namesakes="Zeredah of 2 Chr 4:17 is the Jordan-valley Zarethan (1 Kgs 7:46), not this town",
        source="imported to Wikidata from Hebrew Wikipedia",
        skip="2 Chr 4:17",
    ),
    "ziklag": Site(
        "Ziklag", 31.3912, 34.6816, "Q578876", POSSIBLE,
        modern="Tel Sera' (Tell esh-Shari'a), north-west of Beersheba",
        why="Debated; Tel Sera' (Oren) is the usual choice, but Khirbet al-Ra'i (Garfinkel 2019), Tel Halif and Tel Haror are argued",
        aka=("Tel Sera'", "Tell esh-Shari'a"),
        region="the South",
        tribe=("Judah", "Simeon"),
        refs="Josh 15:31; 19:5; 1 Sam 27:6; 30:1, 14, 26; 2 Sam 1:1; 4:10; 1 Chr 12:1, 20; Neh 11:28",
    ),
    "ziph_judah": Site(
        "Ziph", 31.4748, 35.1351, "Q8072636", KNOWN,
        modern="Tel Zif, south-east of Hebron",
        why="Continuous name",
        aka=("Tel Zif", "Tell Zif"),
        region="Judah",
        tribe=("Judah",),
        refs="Josh 15:55; 1 Sam 23:14, 15, 24; 26:2; 2 Chr 11:8",
        namesakes="Ziph in the Negev (Joshua 15:24)",
        source="the ancient town's Wikidata item",
        skip="Josh 15:24; 1 Chr 4:16",
    ),
    "zoar": Site(
        "Zoar", 31.0469, 35.5025, "Q218016", PROBABLE,
        modern="Byzantine Zoara at Ghor es-Safi, south-east of the Dead Sea",
        why="The Madaba map's Zoora and Lot's cave monastery (Deir Ain Abata); holds only if the cities of the plain lay south of the Dead Sea",
        aka=("Bela", "Ghor es-Safi", "Segor", "Zoara"),
        region="Moab",
        refs="Gen 13:10; 14:2, 8; 19:22, 23, 30; Deut 34:3; Isa 15:5; Jer 48:34",
        skip="Gen 36:32, 33; 46:21; Num 26:38, 40; 1 Chr 1:43, 44; 5:8; 7:6, 7; 8:1, 3",
    ),
    "zorah": Site(
        "Zorah", 31.7751, 34.9853, "Q2916162", KNOWN,
        modern="Tel Tzora (Sar'a), above the Sorek valley",
        why="The name survives in Sar'a.",
        aka=("Tel Tzora", "Sar'a"),
        region="the lowland",
        tribe=("Judah", "Dan"),
        refs="Josh 15:33; 19:41; Judg 13:2, 25; 16:31; 18:2, 8, 11; 2 Chr 11:10; Neh 11:29",
    ),
}

# In and against the city, too close to draw on the atlas
JERUSALEM = {
    "en_rogel": Site(
        "En Rogel", 31.7672, 35.236, "Q2919936", PROBABLE,
        kind="spring",
        modern="Bir Ayyub, where the Kidron and Hinnom valleys meet",
        why="The spring on the Judah-Benjamin border below the city (Josh 15:7); consensus",
        aka=("Ein Rogel", "Bir Ayyub", "Job's Well"),
        region="Judah",
        refs="Josh 15:7; 18:16; 2 Sam 17:17; 1 Kgs 1:9",
    ),
    "gethsemane": Site(
        "Gethsemane", 31.7794, 35.2394, "Q205333", PROBABLE,
        modern="Garden of Gethsemane at the foot of the Mount of Olives (Church of All Nations)",
        why="Tradition since the 4th-century church; fits the Gospels' setting across the Kidron",
        aka=("Church of All Nations",),
        region="Judah",
        refs="Matt 26:36; Mark 14:32",
    ),
    "gihon_spring": Site(
        "Gihon", 31.7729, 35.2364, "Q204601", KNOWN,
        kind="spring",
        modern="Gihon Spring on the east side of the City of David",
        why="Hezekiah's tunnel runs from it to Siloam (Siloam inscription); excavated",
        aka=("Gihon Spring", "Ain Umm ed-Daraj", "Virgin's Fountain"),
        region="Judah",
        refs="1 Kgs 1:33, 38, 45; 2 Chr 32:30; 33:14",
        namesakes="Gihon, a river of Eden (Genesis 2:13)",
        skip="Gen 2:13",
    ),
    "golgotha": Site(
        "Golgotha", 31.7784, 35.2298, "Q187702", PROBABLE,
        modern="Church of the Holy Sepulchre",
        point="the Church of the Holy Sepulchre",
        why="Tradition since Constantine (AD 326), outside the wall of Jesus' day; the Garden Tomb is a minority view",
        aka=("Calvary",),
        region="Judah",
        refs="Matt 27:33; Mark 15:22; John 19:17",
    ),
    "siloam": Site(
        "Siloam", 31.7706, 35.235, "Q1483483", KNOWN,
        kind="pool",
        modern="Pool of Siloam at the south tip of the City of David",
        point="the pool",
        source="the first Wikidata coordinate; the item's second is 1.5 km off",
        why="End of Hezekiah's tunnel; the Second Temple pool was excavated in 2004; the name continues in Silwan",
        aka=("Pool of Siloam", "Shiloah", "Silwan"),
        region="Judah",
        refs="Luke 13:4; John 9:7, 11",
    ),
}


# ===========================================================================
# Not placed
# ===========================================================================

UNPLACED = [
    "Nebo, the town (Num 32:3, 38; 1 Chr 5:8; Isa 15:2; Jer 48:1, 22): Khirbet al-Mukhayyat, south-east of Mount Nebo, is the usual site, but neither Wikidata nor Wikipedia gives the ruin a point (the village item Q6401771 is rounded to the arc-minute and lies west of the mountain).",
    "Waters of Merom (Josh 11:5, 7): debated between the spring at Meiron, Tell el-Khirbe near Marun er-Ras, and the old view that it is Lake Huleh. Wikidata's item Q65091150 has no coordinate.",
    "Harosheth of the Gentiles (Judg 4:2, 13, 16): proposed for Tell el-'Amr/el-Harithiyeh by the Kishon, for el-Ahwat (Zertal), or read as a wooded region rather than a town. Wikidata's item Q2920321 has no coordinate.",
    "Dalmanutha (Mark 8:10): unidentified, perhaps a name for an anchorage near Magdala. No site holds.",
    "Rakkath (Josh 19:35): the Talmud equates it with Tiberias, others put it at Tell Eqlatiyeh. Wikidata's item Q128758422 has no coordinate.",
    "Beth Shemesh and Beth Anath of Naphtali (Josh 19:38; Judg 1:33): several Upper Galilee candidates, none agreed.",
    "Baal Gad 'in the valley of Lebanon under Mount Hermon' (Josh 11:17; 12:7; 13:5) and the valley or land of Mizpah under Hermon (Josh 11:3, 8): unidentified.",
    "Asher's border and levitical towns Helkath, Mishal, Rehob (two of them), Hosah, Hammon, Ummah, Ramah of Asher, Beth Emek, Neiel, Hali, Beten, Allammelech, Amad, Shihorlibnath and Beth Dagon (Josh 19:25-30; 21:30-31): debated, or with no Wikidata point for the proposed tell. For Beth Emek, Tell Mimas is proposed, but Wikidata has no point for it.",
    "Zebulun's Maralah, Dabbesheth, Ethkazin, Neah, Kattath, Nahalal, Idalah, the valley of Iphtah El, and the levitical Kartah and Dimnah (Josh 19:11-15; 21:34-35): debated.",
    "Issachar's Hapharaim, Shion, Anaharath (Tel Rekhesh, Q7223664, is Aharoni's candidate), Rabbith, Ebez, Remeth, En Haddah, Beth Pazzez and Shahazumah (Josh 19:19-22): debated.",
    "Naphtali's southern border points Heleph, the oak in Zaanannim (also Judg 4:11), Adami-nekeb, Jabneel, Lakkum and Aznoth Tabor (Josh 19:33-34), and the levitical Kartan (Josh 21:32): debated. Tel Adami (Q12058479) and Yavne'el (Q1676894) are candidates for Adami-nekeb and Jabneel.",
    "Rumah (2 Kgs 23:36): Horvat Ruma in the Beth Netofa valley (Q12407395, 32.7889, 35.2932) is the usual candidate, but some read it as Arumah near Shechem. Left out as contested and minor.",
    "Nob (1 Sam 21:1; 22:19; Isa 10:32): the priests' town in sight of Jerusalem, put on Mount Scopus, el-Isawiya or Ras el-Mesharif; no agreed site, and Wikidata's Nob item (Q11991625) has no coordinate",
    "Abel Meholah (Judg 7:22; 1 Kgs 4:12; 19:16): Elisha's town; Eusebius 10 miles south of Beth Shan; the leading candidate Tell Abu Sus (west bank, by Mehola) has no Wikidata or Wikipedia coordinate, and Wikidata's Abel-meholah item (Q4666524) has none; Glueck's Tell el-Maqlub (Q111165906, 32.3990, 35.6801) is on the east bank and also argued as Jabesh Gilead",
    "Beeroth (Josh 9:17; 18:25; 2 Sam 4:2): Gibeonite town; el-Bireh, Nebi Samwil, Khirbet el-Burj and Biddu are all proposed; Wikidata's point (Q4880075, 31.8322, 35.1519, from enwiki) marks no named site",
    "Jeshanah (2 Chr 13:19): Burj el-Isaneh is the usual identification, but Wikidata's point (Q22948654, 31.9667, 35.2167) is rounded to the arc-minute",
    "Ophrah of the Abiezrites (Judg 6:11, 24; 8:27, 32; 9:5): Gideon's town in Manasseh; Afula, et-Taiyibeh (Galilee) and others proposed; no agreement",
    "Beth Aven (Josh 7:2; 18:12; 1 Sam 13:5; 14:23): near Ai, east of Bethel; Tell Maryam and Burqa proposed; Hosea's Beth Aven (4:15; 5:8; 10:5) is a taunt name for Bethel",
    "Mount Gaash and the brooks of Gaash (Josh 24:30; Judg 2:9; 2 Sam 23:30): near Timnathserah, no named summit",
    "Shamir (Judg 10:1-2): Tola's town in the hill country of Ephraim, unknown (Samaria itself has been suggested)",
    "Kibzaim (Josh 21:22): levitical city of Ephraim, unknown",
    "Ebenezer (1 Sam 7:12, between Mizpah and Shen) and Shen: unknown; the Ebenezer of 1 Sam 4:1 by Aphek is often put at Izbet Sartah, outside this region",
    "Zelah and Eleph (Josh 18:28; 2 Sam 21:14, Saul's family tomb): unknown",
    "Migron, Gallim, Laishah, Madmenah, Gebim (Isa 10:28-32): stations of the Assyrian advance, no agreed sites",
    "Ataroth Addar, Naarah, Michmethath, Zemaraim, Ophni, Beth Arabah (Josh 16-18 border and town lists): candidates exist but none is settled enough to place",
    "Beth Shittah, Tabbath, Beth Barah (Judg 7:22-24): stations of Midian's flight down the Jordan valley, unknown",
    "Gibeah of Phinehas, 'the hill of Phinehas' (Josh 24:33): Awarta or Jibia proposed",
    "Brook Cherith (1 Kgs 17:3, 5): 'before the Jordan', Wadi Qelt by tradition or an eastern wadi; a stream, not a point",
    "Netophah (Ezra 2:22, Neh 7:26): Khirbet Bedd Faluh near Bethlehem is proposed, but neither the Netophah item (Q6999828) nor its Wikipedia article has a coordinate.",
    "Etam (2 Chr 11:6): placed at Khirbet el-Khokh by Ain Atan near Artas, but neither the Etam item (Q5402401) nor its Wikipedia article has a coordinate.",
    "Gedor (Josh 15:58): Khirbet Jedur near Beit Ummar; no Wikidata or Wikipedia coordinate found (the 'Gedor' item Q25492515 is a Benjamin Gedor with an unknown-value coordinate).",
    "Hill of Hachilah (1 Sam 23:19, 26:1), Sela Hammahlekoth (1 Sam 23:28) and David's strongholds: unidentified points in the wilderness of Ziph and Maon.",
    "Cave of Adullam (1 Sam 22:1): the city is placed; the cave itself is not identified (the Khureitun cave near Tekoa is a medieval tradition).",
    "City of Salt, Nibshan, Middin, Secacah (Josh 15:61-62): wilderness towns tied to Qumran and the Buqei'a forts only by debated proposals.",
    "En Eglaim (Ezek 47:10): Ein Feshkha is one proposal among several.",
    "Negev towns of Josh 15:21-32 and 19:2-7 (Kabzeel, Moladah, Hazar Shual, Madmannah, Sansannah, Ain and Rimmon, Beth Pelet, Ramah of the South, Siphmoth): identifications are debated or unknown; Horvat Uza (Kinah?) and Tel Malhata are candidates with no firm name.",
    "Socoh of the hill country, Anim, Dumah and the other minor towns of Josh 15:48-60: Khirbet Shuweikeh, Khirbet Ghuwein and Khirbet Domeh keep the names, but no Wikidata item with a coordinate turned up for them, so they are not placed.",
    "Beer Lahai Roi (Gen 16:14) and the ascent of Ziz (2 Chr 20:16): unidentified.",
    "Lehi (Judg 15:9-19): Samson's jawbone site; no accepted identification.",
    "Valley of Sorek (Judg 16:4): Wikidata's Nahal Sorek (Q252254) gives only the stream's source near Jerusalem and its mouth, with no point for the valley at Zorah and Timnah. It could be labelled from Zorah/Timnah, but only as an interpolated point.",
    "Rakkon (Josh 19:46): Tell er-Reqqeit has been proposed, but there is no consensus and no Wikidata coordinate.",
    "Baalath (Josh 19:44), Ithlah (19:42), Elon (19:43): Danite towns with no accepted identification.",
    "Achzib of Judah (Josh 15:44; Mic 1:14): Tell el-Beida has been proposed, but there is no Wikidata or Wikipedia coordinate.",
    "Beth Dagon of Judah (Josh 15:41), Gederoth (Josh 15:41; 2 Chr 28:18), Naamah, Gederah, Ashnah, Enam, En Gannim, Tappuah, Mizpeh of the lowland (Josh 15:33-41): unidentified or debated, with no coordinate.",
    "Shikkeron and Mount Baalah (Josh 15:11), on Judah's northern border: unidentified.",
    "Mahaneh Dan (Judg 13:25; 18:12): a camp between Zorah and Eshtaol, or west of Kiriath Jearim; not a fixed site.",
    "Hepher / the land of Hepher (Josh 12:17; 1 Kgs 4:10): debated between Tel Ifshar (Q26764655) in the Sharon and Tell el-Muhaffar in the Dothan valley.",
    "Socoh of the Sharon (1 Kgs 4:10): Khirbet Shuweiket er-Ras near Tulkarm, but no Wikidata coordinate was found.",
    "Lassharon (Josh 12:18): uncertain; it may not be in this region.",
    "Gittaim (2 Sam 4:3; Neh 11:33): unidentified (Ras Abu Hamid near Ramla has been proposed).",
    "Bezer (Deuteronomy 4:43; Joshua 20:8; 21:36; 1 Chronicles 6:78), Reuben's city of refuge and a Levite city: Umm el-'Amad and Jalul are both proposed and neither is accepted. Wikidata's Bezer item (Q3376309) has no coordinate and there is no item for the Umm el-'Amad site, so it is left out rather than guessed.",
    "Mizpah of Gilead (Judges 11:29; with Mizpah in Genesis 31:49, Judges 10:17, 11:11, 11:34) and Ramath Mizpeh (Joshua 13:26): Khirbet Jal'ad, Tell er-Rumeith and es-Salt are all proposed, there is no consensus, and Wikidata has no site point.",
    "Lo Debar / Lodebar (2 Samuel 9:4-5; 17:27): Umm ed-Dabar, Tell el-Hammeh and Khirbet Ibsar are proposed. Wikidata's Lo-debar item (Q6663061) has no coordinate; only a wadi item for Umm ad-Dabar exists.",
    "Tishbe: not in WEB, which has only 'Elijah the Tishbite' (1 Kings 17:1 etc.), so omitted. The traditional Listib / Tell Mar Elias (Q7697429, 32.3622, 35.7222) is available if a marker for the gentilic is ever wanted.",
    "Tob (Judges 11:3, 5; 2 Samuel 10:6, 8): 'the land of Tob' is a district. et-Taiyibeh is only a guess from the name, and there are several Taiyibehs.",
    "Beth Peor (Deuteronomy 3:29; 4:46; 34:6; Joshua 13:20): Khirbet 'Ayun Musa and Khirbet esh-Sheikh Jayil are proposed; there is no agreed site and no Wikidata point.",
    "Kedemoth (Deuteronomy 2:26; Joshua 13:18; 21:37; 1 Chronicles 6:79), a Reubenite Levite city: Qasr ez-Za'faran and 'Aleiyan are proposed; Wikidata's item (Q6382564) has no coordinate.",
    "Zaphon (Joshua 13:27): Tell el-Qos, Tell es-Sa'idiyeh and Tell el-Mazar are proposed; no consensus and no point.",
    "Aroer 'that is near Rabbah' (Joshua 13:25): an Ammonite-border town, not located.",
    "Minnith (Judges 11:33; Ezekiel 27:17) and Abelcheramim (Judges 11:33): not located in Ammon (Tall al-'Umayri, Sahab and Na'ur have been suggested for Abel-keramim).",
    "Betonim and Debir on Gad's border (Joshua 13:26): no Wikidata site (Khirbet Batneh is proposed for Betonim).",
    "The Moabite names Bamoth Baal, Sibmah and Zereth Shahar (Joshua 13:17-19), Beth Diblathaim / Almon Diblathaim, Beth Gamul, Kerioth of Moab, Mizpeh of Moab, Horonaim, Luhith, the waters of Nimrim, Nophah, and the itinerary stops Iye Abarim / Iyim, Mattanah, Nahaliel and Bamoth: none has a secure site or a Wikidata point.",
    "Teman (Jeremiah 49:7, 20; Ezekiel 25:13; Amos 1:12; Obadiah 1:9; Habakkuk 3:3): a district or clan of Edom with no town fixed (Tawilan was proposed and then rejected); Wikidata's item (Q1546303) has no coordinate.",
    "Gerasa (Jerash), Pella and Machaerus are not named in WEB, so they are omitted. WEB's wording is 'Gadarenes' (Mark 5:1; Luke 8:26) and 'Gergesenes' (Matthew 8:28); WEB has no 'Gerasenes'.",
    "Beth Barah (Judges 7:24): a Jordan ford that has not been located.",
    "Argob and Havvoth Jair (Deuteronomy 3:4, 13-14; 1 Kings 4:13): districts of Bashan, not points.",
    "Ituraea, Trachonitis (Luke 3:1), Idumaea (Mark 3:8), Phoenicia (Acts 11:19; 15:3; 21:2), Sharon (Acts 9:35): regions, no point fact; left for region labels",
]
