"""The lands beyond the Levant in (lat, lon): the Nile and its delta, the Red
Sea's two gulfs and the Sinai between them, the Euphrates and the Tigris and
the head of the Persian Gulf, and the places of Israel's story that stand
there (Ur, Haran, Babylon, Rameses, Midian, Mount Sinai). For the Acts 7 map
(generate_acts7_svg.py), with mediterranean.py's coasts, acts_geography's
southern Asia Minor and Cyprus, and gazetteer.py's Levant.

How it was made. As in gazetteer and mediterranean, every commented point
is one named place (a town, cape, lighthouse, dam, spring or ancient site)
whose coordinate is that place's own Wikidata P625 (CC0, the item named in
the comment), gathered on 2026-11-05. Points marked "~" are our own
interpolation, from general knowledge of the shore between two named
neighbours. No line geometry was copied, traced or sampled from
OpenStreetMap, Google or any map or atlas, and no point is one of
generate_tribal_maps', generate_acts1518_svg's or acts_geography's
far-world or Egypt points, which are atlas traces.

The lines are coarse: a town on a river stands on its bank, and a town on
a shore may stand a little back from the water. They are drawn for a map
of the whole Near East at under 100 px a degree, and for close-ups of a
few hundred, not for anything closer.

- **Rivers** run from source to mouth. A mouth is the matching coast or river
  point, so the lines meet: the Nile's two branches end at
  mediterranean.AFRICA's Rosetta and Damietta mouths, the Euphrates and the
  Tigris meet at al-Qurnah, where the Shatt al-Arab begins, and the Shatt
  ends on GULF_HEAD at al-Faw. The Balikh, Haran's river, ends on the
  Euphrates at Raqqa.
- **The Euphrates** is drawn by the Hillah branch, the river's old course past
  Babylon, not the Hindiya branch the main stream takes today.
- **Coasts** run with the land on the left. RED_SEA_WEST runs north up the
  African shore to Suez; RED_SEA_EAST runs from Suez down the Sinai's west
  shore, round Ras Muhammad, up the Gulf of Aqaba to Aqaba and down the
  Arabian shore. Together they are the Red Sea's one shore, open to the south.
  GULF_HEAD runs north up the Arabian shore of the Persian Gulf to al-Faw and
  east along the Iranian shore. Their far ends run off the map's sheet.
- **Left out on purpose:** Bubiyan (drawn as one with the Kuwaiti shore), the
  Bitter Lakes and the canal, Lake Manzala and Lake Burullus, the reservoirs
  behind the Euphrates' and the Nile's modern dams, and the Nile above Qena.
- **SITES** are gazetteer Sites; **REGIONS** gazetteer Regions, a point for
  the name of a land.
"""

from gazetteer import Site, Region, KNOWN, PROBABLE, POSSIBLE

# ===========================================================================
# The Nile
# ===========================================================================

# from Qena down to the head of the delta at the Delta Barrage, where it
# parts into the Rosetta and Damietta branches
NILE = [
    (26.1667, 32.7167),   # Qena (Q336661)
    (26.0500, 32.2500),   # Nag Hammadi (Q270754)
    (26.5606, 31.6917),   # Sohag (Q388108)
    (27.1869, 31.1714),   # Asyut (Q29962)
    (27.7306, 30.8425),   # Mallawi (Q393498)
    (28.0833, 30.7500),   # Minya (Q310117)
    (28.3122, 30.7100),   # Samalut (Q950924)
    (28.6483, 30.8422),   # Maghagha (Q1827283)
    (29.0667, 31.0833),   # Beni Suef (Q394080)
    (29.3372, 31.2036),   # al-Wasta (Q4105094)
    (29.8493, 31.3327),   # Helwan (Q771345)
    (30.0069, 31.2250),   # Nilometer on Roda Island, Cairo (Q1992209)
    (30.1844, 31.1167),   # Delta Barrage (Q5254573)
]

NILE_ROSETTA = [
    (30.1844, 31.1167),   # Delta Barrage (Q5254573)
    (30.8197, 30.8242),   # Kafr el-Zayat (Q951867)
    (31.2028, 30.5503),   # Fuwwah (Q4119537)
    (31.4014, 30.4194),   # Rosetta (Rashid) (Q243699)
    (31.4685, 30.3651),   # Rosetta Mouth (Q23938832)
]

NILE_DAMIETTA = [
    (30.1844, 31.1167),   # Delta Barrage (Q5254573)
    (30.4628, 31.1797),   # Benha (Q336966)
    (30.7119, 31.2394),   # Zefta (Q2392142)
    (31.0500, 31.3833),   # Mansoura (Q223587)
    (31.3297, 31.7147),   # Faraskur (Q4166604)
    (31.4167, 31.8214),   # Damietta (Q189383)
    (31.5269, 31.8447),   # Damietta Mouth (Q23951846)
]

# ===========================================================================
# The Red Sea, its two gulfs and the Sinai
# ===========================================================================

# the African shore, north from El-Quseir to Suez at the head of its gulf
RED_SEA_WEST = [
    (26.1091, 34.2760),   # El-Quseir (Q310751)
    (26.7517, 33.9344),   # Safaga (Q986325)
    (27.2578, 33.8117),   # Hurghada (Q187284)
    (27.3850, 33.6792),   # El Gouna (Q286510)
    (28.1380, 33.2701),   # Ras Shukeir, its mosque by the shore (Q138136975)
    (28.3517, 33.1100),   # Ras Gharib Lighthouse (Q115161310)
    (29.1117, 32.6650),   # Zafarana lighthouse (Q112106772)
    (29.6450, 32.3344),   # Ain Sokhna (Q405881)
    (29.9667, 32.5333),   # Suez (Q134514)
]

# from Suez down the Sinai's west shore, round Ras Muhammad, up the Gulf of
# Aqaba to its head and down the Arabian shore past Midian
RED_SEA_EAST = [
    (29.9667, 32.5333),   # Suez (Q134514)
    (29.8769, 32.6583),   # Oyun Musa, the springs of Moses (Q2903692)
    (29.5917, 32.7167),   # Ras Sudr (Q2915909)
    (29.0454, 33.1107),   # Abu Zenima (Q4670429)
    (28.8833, 33.1833),   # Abu Rudeis (Q2889728)
    (28.2333, 33.6167),   # El-Tor (Q867603)
    (27.7267, 34.2483),   # Ras Muhammad Lighthouse (Q115161312)
    (27.8519, 34.3050),   # Sharm el-Sheikh (Q644)
    (28.4931, 34.5047),   # Dahab (Q370495)
    (29.0340, 34.6591),   # Nuweiba (Q1011488)
    (29.4925, 34.8969),   # Taba (Q867592)
    (29.5500, 34.9500),   # Eilat (Q134762)
    (29.5322, 35.0061),   # Aqaba (Q180522)
    (29.2861, 34.9386),   # Haql (Q97291597)
    (28.4000, 34.7600),   # ~ Maqna, the shore below al-Bad'
    (27.9300, 34.5900),   # ~ Ras al-Sheikh Hamid, at the Strait of Tiran
    (27.7500, 35.1000),   # ~ the shore east of the cape
    (27.3493, 35.6962),   # Duba (Q27225)
    (26.2833, 36.4167),   # Al Wajh (Q97291213)
]

# ===========================================================================
# The rivers of Mesopotamia and the head of the Persian Gulf
# ===========================================================================

EUPHRATES = [
    (38.8069, 38.7569),   # Keban Dam (Q1737672)
    (38.2265, 39.1357),   # Karakaya Dam (Q152556)
    (37.4817, 38.3175),   # Ataturk Dam (Q753776)
    (37.0250, 37.9769),   # Birecik (Q849497)
    (36.8297, 38.0150),   # Carchemish (Q283680)
    (35.8722, 38.5667),   # Euphrates Dam at Tabqa (Q372823)
    (35.9500, 39.0100),   # Raqqa (Q283368)
    (35.3333, 40.1500),   # Deir ez-Zor (Q239097)
    (35.0208, 40.4533),   # Mayadin (Q310895)
    (34.4500, 40.9186),   # Abu Kamal (Q152828)
    (34.3912, 40.9876),   # Al-Qa'im (Q2353905)
    (34.3686, 41.9819),   # Anah (Q2627750)
    (34.1397, 42.3725),   # Haditha (Q944368)
    (33.6417, 42.8250),   # Hit (Q2422345)
    (33.4258, 43.2992),   # Ramadi (Q192961)
    (33.3500, 43.7833),   # Fallujah (Q191170)
    (32.7839, 44.2764),   # Musayyib (Q4120374)
    (32.4833, 44.4333),   # Hillah (Q243846)
    (31.9892, 44.9247),   # Al Diwaniyah (Q694939)
    (31.3167, 45.2833),   # Samawah (Q750679)
    (31.0439, 46.2575),   # Nasiriyah (Q38811)
    (30.8969, 46.4478),   # Souq al-Shuyukh (Q4165411)
    (30.9549, 46.9751),   # Al-Chibayish (Q60761652)
    (31.0158, 47.4306),   # Al-Qurnah (Q2574863)
]

TIGRIS = [
    (37.9108, 40.2367),   # Diyarbakir (Q83387)
    (37.7306, 41.4161),   # Hasankeyf (Q756957)
    (37.3302, 42.1848),   # Cizre (Q821363)
    (36.3417, 43.1292),   # Mosul (Q83317)
    (34.6000, 43.6833),   # Tikrit (Q165444)
    (34.1959, 43.8857),   # Samarra (Q170047)
    (33.3153, 44.3661),   # Baghdad (Q1530)
    (32.5147, 45.8189),   # Kut (Q328030)
    (32.4617, 46.6878),   # Ali al-Gharbi (Q4062224)
    (31.8333, 47.1500),   # Amarah (Q366010)
    (31.5247, 47.2919),   # Qal'at Saleh (Q43966851)
    (31.0158, 47.4306),   # Al-Qurnah (Q2574863)
]

SHATT_AL_ARAB = [
    (31.0158, 47.4306),   # Al-Qurnah (Q2574863)
    (30.5150, 47.8100),   # Basra (Q48195)
    (30.3392, 48.3042),   # Abadan (Q63049)
    (29.9800, 48.4700),   # Al-Faw (Q1164081)
]

# Haran's river, from the plain below the town to the Euphrates
BALIKH = [
    (36.6975, 38.9567),   # Tell Abyad (Q1896205)
    (35.9500, 39.0100),   # Raqqa (Q283368)
]

# the Arabian shore north to the Shatt's mouth, then the Iranian shore east
GULF_HEAD = [
    (27.3170, 48.8670),   # Tanajib (Q7682241)
    (28.4033, 48.5428),   # Ras al-Khafji (Q32153579)
    (29.0667, 48.1667),   # Mina Al Ahmadi (Q111386896)
    (29.3750, 47.9800),   # Kuwait City (Q35178)
    (29.3500, 47.6833),   # Al Jahra, the head of Kuwait Bay (Q1077024)
    (29.5500, 47.9200),   # ~ Subiya, the bay's north shore
    (29.6200, 48.1000),   # ~ Bubiyan's south shore
    (29.9000, 48.3800),   # ~ Bubiyan's east shore, on the Khor Abdullah
    (29.9800, 48.4700),   # Al-Faw (Q1164081)
    (29.9789, 48.5206),   # Arvandkenar (Q744176)
    (29.8700, 48.8000),   # ~ the Shatt's mouth, its east bank
    (29.9500, 49.2000),   # ~ the Iranian shore, toward Khor Musa
]

COASTS = {"red_sea_west": RED_SEA_WEST, "red_sea_east": RED_SEA_EAST,
          "gulf_head": GULF_HEAD}
RIVERS = {"nile": NILE, "nile_rosetta": NILE_ROSETTA,
          "nile_damietta": NILE_DAMIETTA, "euphrates": EUPHRATES,
          "tigris": TIGRIS, "shatt_al_arab": SHATT_AL_ARAB, "balikh": BALIKH}

# ===========================================================================
# Places
# ===========================================================================

SITES = {
    "ur": Site(
        "Ur", 30.9622, 46.1044, "Q5699", PROBABLE,
        modern="Tell el-Muqayyar, west of Nasiriyah",
        point="the tell and its ziggurat",
        why="Woolley's excavations fix Ur at Tell el-Muqayyar. That it is Abraham's Ur of the Chaldees is the usual reading; a northern Ur near Haran, at Urfa, is the other proposal.",
        aka=("Ur of the Chaldees",),
        refs="Gen 11:28, 31; 15:7; Neh 9:7"),
    "haran": Site(
        "Haran", 36.8708, 39.025, "Q199547", KNOWN,
        modern="Harran, south-east of Sanliurfa",
        point="the mound beside the modern village",
        why="Continuous name; the Harran of Assyrian texts and of the moon god's temple",
        aka=("Harran", "Carrhae"),
        refs="Gen 11:31-32; 12:4-5; Acts 7:2, 4"),
    "babylon": Site(
        "Babylon", 32.5425, 44.4211, "Q5684", KNOWN,
        modern="Babylon, north of Hillah",
        point="the ruin field",
        why="Continuous name; Koldewey's excavations",
        refs="Acts 7:43"),
    "rameses": Site(
        "Rameses", 30.7994, 31.8342, "Q937930", PROBABLE,
        modern="Qantir, in the eastern delta",
        point="Pi-Ramesses",
        why="Rameses (Exod 1:11; 12:37) is taken to be Pi-Ramesses, the delta capital of the 19th dynasty, now placed at Qantir by Bietak's excavations; Tanis was the older proposal.",
        aka=("Raamses", "Pi-Ramesses"),
        refs="Gen 47:11; Exod 1:11; 12:37; Num 33:3, 5"),
    "on": Site(
        "On", 30.1295, 31.2889, "Q191687", KNOWN,
        modern="Heliopolis, in north-east Cairo",
        point="the temple ground at Matariya",
        why="On is Heliopolis, the sun's city (Gen 41:45, the priest of On); its obelisk still stands at Matariya.",
        aka=("Heliopolis",),
        refs="Gen 41:45, 50; 46:20"),
    "mount_sinai": Site(
        "Mount Sinai", 28.5384, 33.9752, "Q377485", POSSIBLE, kind="mount",
        modern="Jebel Musa, above Saint Catherine's",
        point="the summit",
        why="The traditional mountain since the fourth century. Jebel Serbal, Jebel Sin Bishar, and Jebel al-Lawz in Midian are among the others proposed.",
        aka=("Horeb", "Jebel Musa"),
        refs="Acts 7:30, 38"),
    "bad": Site(
        "Midian", 28.4947, 35.0122, "Q22935639", POSSIBLE,
        label="al-Bad'",
        modern="al-Bad', in north-west Saudi Arabia",
        point="the oasis and its wells",
        why="Ptolemy's and the Arab geographers' Madiama, with the 'wells of Moses' (Mugha'ir Shu'ayb). Where Moses kept Jethro's flocks is not known.",
        aka=("Madiama",),
        refs="Exod 2:15; Acts 7:29"),
    "kadesh": Site(
        "Kadesh", 30.6483, 34.4222, "Q954599", PROBABLE,
        modern="'Ain el-Qudeirat, in north-east Sinai",
        point="the spring and its fort",
        why="Most scholars put Kadesh Barnea at 'Ain el-Qudeirat, the richest spring of the region, near 'Ain Qadeis, which keeps the name.",
        aka=("Kadesh Barnea",),
        refs="Num 20:1; 32:8; 33:36"),
    "alexandria": Site(
        "Alexandria", 31.1975, 29.8925, "Q87", KNOWN,
        modern="Alexandria",
        why="Continuous name; Alexander's city",
        refs="Acts 6:9; 18:24; 27:6; 28:11"),
    "cyrene": Site(
        "Cyrene", 32.8167, 21.85, "Q44112", KNOWN,
        modern="Shahhat, in eastern Libya",
        why="Continuous ruin; the Greek city of Cyrenaica",
        refs="Matt 27:32; Acts 2:10; 11:20; 13:1"),
}

REGIONS = {
    "mesopotamia": Region("Mesopotamia", 34.9, 41.2, r"\bMesopotamia\b",
                          note="The land between the Euphrates and the Tigris."),
    "chaldea": Region("Chaldea", 31.4, 45.6, r"\bChaldaeans?\b",
                      note="The south of Mesopotamia, Ur's land."),
    "egypt": Region("Egypt", 29.4, 30.6, r"\bEgypt\b"),
    "goshen": Region("Goshen", 30.8722, 31.4775, r"\bGoshen\b",
                     note="The eastern delta, round Rameses."),
    "midian": Region("Midian", 28.5, 35.0, r"\bMidian\b",
                     note="The land east of the Gulf of Aqaba."),
    "sinai": Region("Sinai", 29.5, 34.0, note="The peninsula between the gulfs."),
    "canaan": Region("Canaan", 31.6, 35.0, r"\bCanaan\b"),
}
