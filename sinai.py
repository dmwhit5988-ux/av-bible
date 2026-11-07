"""The Sinai and its two gulfs in (lat, lon): the shores of the Gulf of Suez
and the Gulf of Aqaba, the head of the Red Sea between them, the lakes of
the Suez isthmus and Lake Bardawil, and the Nile from Middle Egypt to its
Damietta mouth. For the wilderness journey reference page
(generate_wilderness_reference.py), with gazetteer's Levant (the coast to
the brook of Egypt, the Salt Sea, the Jordan, the Arnon and the Zered) and
mediterranean.AFRICA's coast west of the brook of Egypt.

How it was made. As in gazetteer and mediterranean, every commented point
is one named place (a cape, beach, harbour, lighthouse, wadi mouth, hotel,
air base, bridge or town) whose coordinate is that place's own Wikidata
P625 (CC0, the item named in the comment), fetched from Wikidata's
EntityData on 2026-11-06. One point, Fanara on the Great Bitter Lake, is
German Wikipedia's (its item has no coordinate), and the comment names the
article. Points marked "~" are our own interpolation, a point on the chord
between two named neighbours where no named place stands on the shore (one,
by Jazirat Ruwayjil, set just landward of the chord, whose midpoint fell on
the island). No line geometry was copied, traced or sampled from
OpenStreetMap, Google or any map or atlas, and no point is one of
generate_tribal_maps' (GULF_SUEZ, GULF_AQABA, RED_SEA),
generate_acts1518_svg's or acts_geography's far-world points, which are
atlas traces, or of acts_geography.SERMON_SITES, which are schematic.

The lines are coarse, for a page at about a kilometre to 9 px:

- Many capes are GeoNames imports rounded to the arc-minute (up to about a
  kilometre off), and many shore points are towns, hotels, mosques or air
  bases that stand a few hundred metres to a kilometre or two back from
  the water. Wadi points are taken to mark their mouths.
- The lakes of the isthmus are crude: Wikidata names very few places on
  their shores, so their rings run through the institutions beside them.
- The Nile is drawn by towns on its banks, 10 to 26 km apart, alternating
  banks; it follows the Damietta branch from the head of the delta.
- Bardawil's north side is mediterranean.AFRICA's own points along the
  bar, so the lagoon and the sea share that line; its western lobe is
  underdrawn.

- **The shores** run with the land on the left, and meet where they
  should: SUEZ_WEST_SHORE runs north up the African shore of the Gulf of
  Suez, from below the sheet to Port Tawfiq at its head, where
  SINAI_WEST_SHORE begins; that runs down the Sinai's west shore to Ras
  Muhammad Lighthouse (the cape itself has no item), where
  SINAI_EAST_SHORE begins (near_east.RED_SEA_EAST's Ras Muhammad); that
  runs up the Gulf of Aqaba, round its head past Eilat, to Arab Divers at
  Aqaba, where ARABIA_EAST_SHORE begins, down the Midian shore and east
  along the Red Sea past Duba, off the sheet. Zeit Bay is left out: the
  line crosses its mouth.
- **The lakes** (TIMSAH, GREAT_BITTER, LITTLE_BITTER, BARDAWIL) and the
  island of TIRAN are rings, not closed (the last point joins the first).
  The canal itself is not drawn.
- **NILE** runs from Maghagha, west of the sheet, past Cairo to the Delta
  Barrage and down the Damietta branch to its mouth, which is
  mediterranean.AFRICA's point.
"""


# ===========================================================================
# The shores of the gulfs
# ===========================================================================

SUEZ_WEST_SHORE = [
    (27.3000, 33.7500),   # Abū Sha‘r (cape north of Hurghada) (Q23956171)
    (27.3850, 33.6792),   # El Gouna (Q286510)
    (27.3979, 33.6819),   # Bellevue Beach Hotel (El Gouna) (Q57652135)
    (27.4154, 33.6727),   # DoubleTree by Hilton Mangroovy El Gouna Resort (El Gouna) (Q138863179)
    (27.4252, 33.6663),   # Casa Cook El Gouna (El Gouna) (Q111857837)
    (27.5005, 33.6424),   # ~ interpolated (between Casa Cook El Gouna (El Gouna) and Ra‘s Jamsah (Ras Gemsa))
    (27.5758, 33.6186),   # ~ interpolated (between Casa Cook El Gouna (El Gouna) and Ra‘s Jamsah (Ras Gemsa))
    (27.6511, 33.5947),   # Ra‘s Jamsah (Ras Gemsa) (Q23971852)
    (27.7625, 33.5542),   # Ra's al Baḩr (Ras el-Bahar, the spit across Zeit Bay) (Q23952743)
    (27.8000, 33.5667),   # Zeit Peninsula (Q23932478)
    (27.8167, 33.5833),   # Az Zaytīyah (point on the Zeit peninsula) (Q31873083)
    (27.8864, 33.5594),   # Ra's al ‘Ushsh (Q23933029)
    (27.9431, 33.5189),   # Ra's Zayt (Ras Zeit) (Q23932451)
    (27.9875, 33.4673),   # ~ interpolated (between Ra's Zayt (Ras Zeit) and Ra's Dubb (Ras Dib))
    (28.0319, 33.4158),   # Ra's Dubb (Ras Dib) (Q23951831)
    (28.0847, 33.3472),   # ~ interpolated (between Ra's Dubb (Ras Dib) and Ra's Shuqayr (Ras Shukeir))
    (28.1375, 33.2786),   # Ra's Shuqayr (Ras Shukeir) (Q23937163)
    (28.1921, 33.2193),   # ~ interpolated (between Ra's Shuqayr (Ras Shukeir) and El Mallaha Lighthouse)
    (28.2467, 33.1600),   # El Mallaha Lighthouse (Q115161274)
    (28.2989, 33.1359),   # ~ interpolated (between El Mallaha Lighthouse and Ra's Ghārib (Ras Gharib cape))
    (28.3511, 33.1118),   # Ra's Ghārib (Ras Gharib cape) (Q23951441)
    (28.3597, 33.0775),   # Ras Gharib (town) (Q1404020)
    (28.3919, 33.0619),   # Ra's Bakr (Q23972234)
    (28.4535, 33.0110),   # ~ interpolated (between Ra's Bakr and False Ras Gharib Lighthouse)
    (28.5150, 32.9600),   # False Ras Gharib Lighthouse (Q115161279)
    (28.5481, 32.9328),   # Ra's Abū Bakr (Q23956895)
    (28.6098, 32.8984),   # ~ interpolated (between Ra's Abū Bakr and Ra's Rawāhimī (Ras Ruahmi))
    (28.6714, 32.8641),   # ~ interpolated (between Ra's Abū Bakr and Ra's Rawāhimī (Ras Ruahmi))
    (28.7331, 32.8297),   # Ra's Rawāhimī (Ras Ruahmi) (Q23938865)
    (28.7869, 32.7956),   # Râs Issaran (Q23950071)
    (28.8372, 32.7289),   # Ra's Azabarabān (Q23952676)
    (28.8888, 32.6815),   # Wadi al-Jarf (ancient harbour) (Q11855049)
    (28.9710, 32.6561),   # ~ interpolated (between Wadi al-Jarf (ancient harbour) and Marsá Thilimit (anchorage))
    (29.0533, 32.6306),   # Marsá Thilimit (anchorage) (Q23934629)
    (29.1120, 32.6658),   # Ra's az Za‘farānah (Ras Zafarana) (Q23932320)
    (29.1640, 32.6437),   # ~ interpolated (between Ra's az Za‘farānah (Ras Zafarana) and Coral Sea Beach & Aqua Park Resort (Ain Sokhna coast))
    (29.2160, 32.6217),   # Coral Sea Beach & Aqua Park Resort (Ain Sokhna coast) (Q126488128)
    (29.2854, 32.6018),   # Cancun Sokhna Resort - Boutique Resort & Villas (Ain Sokhna coast) (Q111400551)
    (29.3632, 32.5744),   # Grand Ocean Sokhna Hotel (Ain Sokhna coast) (Q126488075)
    (29.3836, 32.5658),   # Ra's Abū Daraj (Ras Abu Darag) (Q23956929)
    (29.4402, 32.4908),   # Dome Marina Hotel & Resort Ain Sokhna (Ain Sokhna) (Q111857776)
    (29.4439, 32.4800),   # Porto Sokhna Beach Resort & Spa (Ain Sokhna) (Q111400591)
    (29.4840, 32.4440),   # Tolip Resort El Galala Majestic (Ain Sokhna) (Q111857779)
    (29.5394, 32.3710),   # Ramada El Sokhna Resort (Ain Sokhna) (Q126538490)
    (29.5450, 32.3683),   # Mövenpick Sokhna (Ain Sokhna) (Q126390820)
    (29.6017, 32.3417),   # Ayn Sukhnah Lighthouse (Q115161235)
    (29.6450, 32.3344),   # Ain Sokhna (Q405881)
    (29.6709, 32.3531),   # Stella Di Mare Grand Hotel (Ain Sokhna) (Q111400603)
    (29.6889, 32.3661),   # Shāţī Kūrāl (beach) (Q23972136)
    (29.7212, 32.3832),   # JAZ Little Venice Golf Resort (Ain Sokhna) (Q126390782)
    (29.7283, 32.3929),   # Elite Residence Tulip & Aqua Park (Ain Sokhna) (Q126488103)
    (29.7332, 32.3946),   # SeaVille Beach Hotel, Ain Soukhna by Elite Hotels & Resorts (Ain Sokhna) (Q126536203)
    (29.7460, 32.4017),   # Retal View Resort El Sokhna (Ain Sokhna) (Q111400605)
    (29.7547, 32.4128),   # Ra's al Ghubbah (Q23951504)
    (29.7828, 32.4361),   # Ra's Sidat (Q23937197)
    (29.8100, 32.4700),   # Ras Muhaggara Lighthouse (Q115161311)
    (29.8228, 32.4856),   # Ra's Muḩajjarah (Q23946342)
    (29.8643, 32.5092),   # Ra's al Adabīyah (Ras Adabiya) (Q23955754)
    (29.8731, 32.4731),   # Al-Adabiya (port) (Q12246904)
    (29.8881, 32.4658),   # Mīnāh al-Adabīyah (port) (Q23972138)
    (29.8964, 32.4644),   # Mīnā' ‘Atāqah (Ataqa port) (Q23954920)
    (29.9354, 32.4723),   # Ataqa Power Station (Suez Bay shore) (Q11959473)
    (29.9551, 32.5430),   # Lusinda Resort & Spa (Suez shore) (Q142005992)
    (29.9500, 32.5500),   # Suez Port (Q6349617)
    (29.9432, 32.5644),   # Port Tawfiq (head of the gulf, canal mouth) (Q20415996)
]

SINAI_WEST_SHORE = [
    (29.9432, 32.5644),   # Port Tawfiq (head of the gulf, canal mouth) (Q20415996)
    (29.9115, 32.5948),   # Oyoun Mousa Power Station (Ayun Musa) (Q17749722)
    (29.9067, 32.5933),   # Birket Misallat Lighthouse (Ayun Musa) (Q115161237)
    (29.8350, 32.6336),   # Mousa Coast Resort - Cairo Beach (Ayun Musa coast) (Q111999178)
    (29.8216, 32.6127),   # Ra's Misallah (Q23946247)
    (29.7592, 32.6667),   # Ra's Duhaysah (Q23952228)
    (29.6733, 32.6867),   # Lahata Lighthouse (Q115161287)
    (29.5989, 32.6828),   # Ra's Sudr (Ras Sudr cape) (Q23935262)
    (29.5833, 32.7000),   # Ras Sudr (port) (Q111386581)
    (29.5313, 32.7236),   # Palm Beach Safari Egypt - Ex Host Mark (Ras Sudr coast) (Q111999176)
    (29.4494, 32.7197),   # Ra's Maţārimah (Q23946996)
    (29.3826, 32.7747),   # ~ interpolated (between Ra's Maţārimah and Ra's Abū Suwayrah)
    (29.3158, 32.8297),   # Ra's Abū Suwayrah (Q23956220)
    (29.2544, 32.8756),   # Ra's Lajjīah (Q23948238)
    (29.2058, 32.9264),   # Ra's Mal‘ab (Q23948446)
    (29.1530, 32.9838),   # ~ interpolated (between Ra's Mal‘ab and Ra's Abū Zanīmah (cape))
    (29.1003, 33.0412),   # ~ interpolated (between Ra's Mal‘ab and Ra's Abū Zanīmah (cape))
    (29.0475, 33.0986),   # Ra's Abū Zanīmah (cape) (Q23955713)
    (29.0454, 33.1107),   # Abu Zenima (Q4670429)
    (29.0300, 33.1347),   # Cairn Point (Abu Zenima) (Q23952047)
    (28.9843, 33.1814),   # Tell Ras Budran (Q104834170)
    (28.9333, 33.1667),   # Ra's Badrān (Ras Budran) (Q23952719)
    (28.8967, 33.1742),   # Ra's Abū Rudays (cape) (Q23956114)
    (28.8833, 33.1833),   # Abou Redis (Abu Rudeis) (Q2889728)
    (28.8126, 33.1885),   # ~ interpolated (between Abou Redis (Abu Rudeis) and Ra's Sharātīb)
    (28.7418, 33.1937),   # ~ interpolated (between Abou Redis (Abu Rudeis) and Ra's Sharātīb)
    (28.6711, 33.1989),   # Ra's Sharātīb (Q23937738)
    (28.6176, 33.2279),   # ~ interpolated (between Ra's Sharātīb and Ra's Jīhān)
    (28.5641, 33.2568),   # ~ interpolated (between Ra's Sharātīb and Ra's Jīhān)
    (28.5106, 33.2858),   # Ra's Jīhān (Q23949806)
    (28.4505, 33.3451),   # ~ interpolated (between Ra's Jīhān and Ra's Shaykh al Bitān)
    (28.3903, 33.4044),   # Ra's Shaykh al Bitān (Q23937082)
    (28.3650, 33.4333),   # Ra's al Wā‘ir (Q23933077)
    (28.3322, 33.4925),   # ~ interpolated (between Ra's al Wā‘ir and Ra's Abū Şuwayrah)
    (28.2994, 33.5517),   # Ra's Abū Şuwayrah (Q23956219)
    (28.2664, 33.5964),   # Hammam Musa (hot spring, El Tor) (Q9285798)
    (28.2350, 33.6124),   # Port of Al Tor (El Tor) (Q12246909)
    (28.1597, 33.6478),   # Ra's Rāyah (Ras Raya) (Q23968909)
    (28.1144, 33.6800),   # ~ interpolated (between Ra's Rāyah (Ras Raya) and Ra's as Sabīl)
    (28.0692, 33.7122),   # Ra's as Sabīl (Q23938352)
    (28.0261, 33.7600),   # Ra's Jārrah (Q23949766)
    (27.9786, 33.8196),   # ~ interpolated (between Ra's Jārrah and Ra's Kanīsah)
    (27.9311, 33.8792),   # Ra's Kanīsah (Q23949605)
    (27.9200, 33.9047),   # Marsá al Qāḑī Yaḩyá (bight) (Q23944934)
    (27.8511, 33.9900),   # Mersa Zaraba (bay) (Q23972150)
    (27.8033, 34.1000),   # Qad Ibn Haddan Lighthouse (Q115161298)
    (27.7775, 34.2258),   # Marsá Buraykah (Marsa Bareika) (Q23952564)
    (27.7267, 34.2483),   # Ras Muhammad Lighthouse (the tip of Sinai) (Q115161312)
]

SINAI_EAST_SHORE = [
    (27.7267, 34.2483),   # Ras Muhammad Lighthouse (Q115161312)
    (27.7321, 34.2600),   # Shark Observatory (cape, Ras Muhammad) (Q14220276)
    (27.7382, 34.2570),   # Eel Garden (beach, Ras Muhammad) (Q14208294)
    (27.7656, 34.2552),   # Ras Zatar (Q9304163)
    (27.7903, 34.2591),   # Ras Ghozlani (Q14218651)
    (27.8202, 34.2712),   # ~ interpolated (between Ras Ghozlani and Sharm El Sheikh port (Sharm el-Maya))
    (27.8500, 34.2833),   # Sharm El Sheikh port (Sharm el-Maya) (Q111387146)
    (27.8564, 34.2958),   # Sharm al Mayyah (bay) (Q23947032)
    (27.8526, 34.3104),   # Reef Oasis Beach Resort (Q111400615)
    (27.8489, 34.3158),   # Ras Umm Sid (Q14218645)
    (27.8558, 34.3153),   # Safir Sharm Waterfalls Resort (Q5764716)
    (27.8644, 34.3174),   # Sunrise Diamond Beach Resort (Q111400627)
    (27.8689, 34.3200),   # Amphoras Beach (hotel) (Q111400630)
    (27.8825, 34.3257),   # Tower Bay (Q14221956)
    (27.8862, 34.3274),   # Labranda Tower Bay (Q111400634)
    (27.9048, 34.3273),   # Stella Di Mare Beach Hotel (Q111400637)
    (27.9072, 34.3290),   # Jewel Sharm El Sheikh Hotel (Q131424409)
    (27.9105, 34.3324),   # Na'ama Bay (Q3869768)
    (27.9159, 34.3327),   # Naama Bay Promenade Beach Resort (Q131424342)
    (27.9142, 34.3415),   # Movenpick Resort Sharm El Sheikh (Q111400642)
    (27.9160, 34.3501),   # Hyatt Regency Sharm el-Sheikh (Q115670160)
    (27.9168, 34.3549),   # Garden Bay (Q11813236)
    (27.9200, 34.3561),   # Continental Plaza Beach Resort (Q131411434)
    (27.9205, 34.3616),   # Reef Oasis Blue Bay Resort (Q111400645)
    (27.9212, 34.3648),   # Sheraton Sharm Hotel (Q111400646)
    (27.9290, 34.3654),   # Tiger Bay (Q14206902)
    (27.9283, 34.3714),   # Mersa Umm Mureikha (Q23957224)
    (27.9378, 34.3791),   # Pickalbatros Golf Beach Resort (Q111400647)
    (27.9409, 34.3835),   # Coral Beach Resort Tiran (Q131498605)
    (27.9512, 34.3850),   # Shark's Bay (Q9335929)
    (27.9574, 34.3912),   # Four Seasons Resort Sharm El Sheikh (Q111400653)
    (27.9605, 34.3981),   # White Knight (bay) (Q14223188)
    (27.9644, 34.3989),   # Concorde El Salam Hotel (Q131405653)
    (27.9646, 34.4044),   # Siva Sharm Resort (Q131405458)
    (27.9651, 34.4167),   # Ras Nasrani (Q14218642)
    (27.9736, 34.4247),   # Coral Sea Imperial Sensatori (Q131469447)
    (27.9800, 34.4367),   # Enterprise Passage Lighthouse (Q115161276)
    (27.9989, 34.4286),   # Charmillion Sea Life Resort (Q111400660)
    (28.0185, 34.4378),   # Tamra Beach Resort (Q131550079)
    (28.0236, 34.4400),   # Nubian Island Hotel (Q111400669)
    (28.0291, 34.4380),   # Rixos Sharm El Sheikh (Q111400670)
    (28.0322, 34.4385),   # Iberotel Redsina (Q111400671)
    (28.0407, 34.4326),   # Nabq Bay (Q14215969)
    (28.0573, 34.4376),   # JAZ Mirabel Beach (Q131549587)
    (28.0652, 34.4359),   # Barcelo Tiran Sharm (Q111400675)
    (28.1133, 34.4505),   # ~ interpolated (between Barcelo Tiran Sharm and Marsa Abu Zayd (anchorage))
    (28.1614, 34.4650),   # Marsa Abu Zayd (anchorage) (Q23955709)
    (28.2031, 34.4403),   # ~ interpolated (between Marsa Abu Zayd (anchorage) and Ra's at Tantur)
    (28.2449, 34.4156),   # Ra's at Tantur (Q23954918)
    (28.2686, 34.4084),   # Wadi al Qabilah (mouth) (Q23956801)
    (28.3019, 34.4094),   # Wadi Ghurabi (mouth) (Q23951521)
    (28.3347, 34.4172),   # Wadi Umm Tarfah (mouth) (Q23971962)
    (28.3492, 34.4283),   # Wadi Muwaylah (mouth) (Q23971964)
    (28.3594, 34.4408),   # Wadi Shajarah (mouth) (Q23971966)
    (28.3772, 34.4467),   # Wadi Umm Ikhmul (mouth) (Q23971967)
    (28.4206, 34.4561),   # Wadi Wa'irah (mouth) (Q23971969)
    (28.4412, 34.4624),   # Happy Life Village Dahab (Q111400683)
    (28.4598, 34.4676),   # Ecotel Dahab Bay View Resort (Q111400685)
    (28.4803, 34.4942),   # Swiss Inn Resort Dahab (Q111400688)
    (28.4877, 34.5138),   # Golden Plaza Dahab Resort (Q111999190)
    (28.4951, 34.5150),   # Dahab Plaza Hotel (Q111111130)
    (28.4986, 34.5181),   # Sababa Hotel Dahab (Q111111131)
    (28.5000, 34.5200),   # Dahab Lighthouse (Q115161257)
    (28.5047, 34.5195),   # El Primo Dahab Hotel (Q111857822)
    (28.5193, 34.5114),   # New Dahab Bay Hotel (Q111857820)
    (28.5517, 34.5162),   # Tropitel Dahab Oasis (Q111400695)
    (28.5570, 34.5226),   # Canyon Estate Kite Dive Beach Hotel (Q111111129)
    (28.5722, 34.5374),   # Blue Hole (Dahab) (Q885734)
    (28.5803, 34.5417),   # Al Lihlabah (point) (Q23951901)
    (28.6122, 34.5561),   # Al Hamid (point) (Q23951702)
    (28.6247, 34.5744),   # Ras Abu Galum (Q23956538)
    (28.6361, 34.5781),   # Al Qurdud (point) (Q23955500)
    (28.6869, 34.5994),   # Hasat al Hajr (point) (Q23957169)
    (28.7311, 34.6256),   # Al Mamlah (point) (Q23951905)
    (28.7657, 34.6195),   # Wadi Sukhn (mouth) (Q23957192)
    (28.8103, 34.6207),   # Wadi Amran (mouth) (Q23957194)
    (28.8561, 34.6450),   # Al Habiq (point) (Q23955398)
    (28.8769, 34.6401),   # Wadi Shaq Dayab (mouth) (Q23957199)
    (28.9077, 34.6450),   # Rawd al-Hus (wadi mouth) (Q23957201)
    (28.9285, 34.6392),   # Wadi Umm Zariq (mouth) (Q23957217)
    (28.9667, 34.6500),   # Nuweiba el Muzeina port (Q111387147)
    (28.9734, 34.6664),   # Nuweiba Port (Q113561036)
    (28.9778, 34.6819),   # Al Qarnus (point, Nuweiba) (Q23955501)
    (28.9787, 34.6756),   # Coral Resort Nuweiba (Q111400702)
    (28.9986, 34.6762),   # Zaharon (Q133824591)
    (29.0127, 34.6829),   # Ciao Hotel (Nuweiba) (Q111999209)
    (29.0226, 34.6721),   # Habiba Beach Lodge (Q111857831)
    (29.0424, 34.6640),   # Soft Beach (Nuweiba) (Q31844055)
    (29.0495, 34.6651),   # Saraya Beach (Nuweiba) (Q31844056)
    (29.0511, 34.6681),   # Nuweiba Lodge (Q111999210)
    (29.0567, 34.6708),   # Neviot (Nuweiba Tarabin) (Q6640103)
    (29.0895, 34.6764),   # ~ interpolated (between Neviot (Nuweiba Tarabin) and New Moon Island Camp)
    (29.1223, 34.6819),   # New Moon Island Camp (Q111999212)
    (29.1284, 34.6855),   # Ras El Shattain (Q7221643)
    (29.1401, 34.6868),   # Mahasch (Q1884778)
    (29.1610, 34.6970),   # Mersa Mahashsh el-Asfal (Q12122760)
    (29.1728, 34.6961),   # Ra's Schaitan (Q2124767)
    (29.1861, 34.7040),   # Wadi al Mahash al Asfal (mouth) (Q23948399)
    (29.2100, 34.7383),   # Ra's al Burqah (Q23952568)
    (29.2209, 34.7396),   # Qal'at Zaman (Q14218408)
    (29.2511, 34.7294),   # Bir Sweir (beach) (Q55649699)
    (29.2822, 34.7425),   # Marsa Abu Samrah (Q12122758)
    (29.3242, 34.7553),   # Marsa Mahash al A'la (Q12122757)
    (29.3522, 34.7678),   # Wadi al Mahash al A'la (mouth) (Q23948400)
    (29.3758, 34.7936),   # Marina Taba Heights (Q25452272)
    (29.3805, 34.8010),   # Strand Beach Resort Taba Heights (Q111400705)
    (29.3881, 34.8084),   # Mosaique Beach Resort Taba Heights (Q124115162)
    (29.3922, 34.8087),   # Miramar Resort Taba Heights (Q124114862)
    (29.3986, 34.8122),   # Al Humayrah (anchorage) (Q23951894)
    (29.4186, 34.8233),   # Wadi al Humayra al Bahri (mouth) (Q23971867)
    (29.4302, 34.8297),   # Marsa el-Marakh (Fjord Bay) (Q11770488)
    (29.4444, 34.8508),   # Wadi al Abyad (mouth) (Q23971866)
    (29.4744, 34.8636),   # Wadi Maziriz (mouth, opposite Pharaoh's Island) (Q23971863)
    (29.4892, 34.8986),   # Ra's al Misri (Taba) (Q23946272)
    (29.4904, 34.8994),   # Steigenberger Taba Resort (Q5764739)
    (29.4910, 34.9028),   # Taba Border Crossing (Q2386953)
    (29.4958, 34.9083),   # Hof Nesikha (Princess Beach) (Q26768733)
    (29.4978, 34.9117),   # Hof Ofir (Q26768731)
    (29.5003, 34.9152),   # Eilat Light (Q2891905)
    (29.5022, 34.9178),   # Hof Migdalor (Q26768730)
    (29.5080, 34.9211),   # Royal Shangri-La (Coral Beach) (Q111888204)
    (29.5130, 34.9256),   # Hof Almog (Q26764585)
    (29.5144, 34.9265),   # Hof HaKefar (Q26768734)
    (29.5263, 34.9362),   # Dolphin Reef (Q5289642)
    (29.5322, 34.9404),   # Port of Eilat (Q2915417)
    (29.5393, 34.9453),   # Mosh Beach (Q125308267)
    (29.5401, 34.9470),   # Hof HaDeqel (Q26768737)
    (29.5492, 34.9541),   # Hof Umm Rashrash (Q26768717)
    (29.5498, 34.9552),   # Hof Penina (Q26768716)
    (29.5496, 34.9574),   # Hof Moria (Q26768917)
    (29.5486, 34.9621),   # Hof Nevi'ot (Q26768722)
    (29.5481, 34.9639),   # Hof HaZahav (Q26768724)
    (29.5471, 34.9661),   # Hof Shehafim (Q26768726)
    (29.5464, 34.9686),   # Hof Mifraz HaShemesh (Q26768728)
    (29.5411, 34.9809),   # ~ interpolated (between Hof Mifraz HaShemesh and Al Manara hotel, Saraya Aqaba)
    (29.5358, 34.9933),   # Al Manara hotel, Saraya Aqaba (Q111399733)
    (29.5322, 34.9975),   # Kempinski Hotel Aqaba (Q111399734)
    (29.5308, 34.9997),   # Ayla city wall (Aqaba) (Q126709460)
    (29.5302, 35.0012),   # Arab Divers (Aqaba) (Q111123392)
]

ARABIA_EAST_SHORE = [
    (29.5302, 35.0012),   # Arab Divers (Aqaba) (Q111123392)
    (29.5215, 35.0008),   # Aqaba Flagpole (Q3126572)
    (29.5169, 34.9977),   # Mina' al 'Aqabah (Port of Aqaba) (Q27125468)
    (29.5040, 34.9936),   # Mina' al Fusfat (phosphate port) (Q31866613)
    (29.4796, 34.9863),   # ~ interpolated (between Mina' al Fusfat (phosphate port) and Aqaba Marine Reserve)
    (29.4551, 34.9791),   # ~ interpolated (between Mina' al Fusfat (phosphate port) and Aqaba Marine Reserve)
    (29.4307, 34.9718),   # Aqaba Marine Reserve (Q31866622)
    (29.4051, 34.9781),   # Movenpick Resort Tala Bay (Q111399737)
    (29.3969, 34.9681),   # Mina' az-Zuyut (oil port) (Q27125467)
    (29.3802, 34.9650),   # Wadi Nuwaybi' (mouth) (Q35276463)
    (29.3601, 34.9661),   # Jordan-Saudi Arabia border crossing (Durra) (Q68036391)
    (29.3426, 34.9534),   # Al-Durra Port Mosque (Q138057580)
    (29.3144, 34.9460),   # ~ interpolated (between Al-Durra Port Mosque and Haql)
    (29.2861, 34.9386),   # Haql (Q97291597)
    (29.2142, 34.9160),   # ~ interpolated (between Haql and Ra's al Qila', landward of Jazirat Ruwayjil)
    (29.1422, 34.8814),   # Ra's al Qila' (Q32153778)
    (29.1333, 34.8833),   # Sharm ed-Damair (cove) (Q12171726)
    (29.0994, 34.8775),   # Wadi ash Shurayh (mouth) (Q32202534)
    (29.0347, 34.8497),   # Wadi ad Dabr (mouth) (Q32192878)
    (29.0278, 34.8472),   # Ra's Abu 'Ala (Q32153326)
    (28.9664, 34.8450),   # Wadi al Hasha (mouth) (Q32198980)
    (28.9094, 34.8369),   # Wadi al Hulayb (mouth) (Q32199233)
    (28.8831, 34.8217),   # Ra's Suwayjil as Saghir (Q32154667)
    (28.8345, 34.8131),   # ~ interpolated (between Ra's Suwayjil as Saghir and Wadi al Aswad (mouth))
    (28.7860, 34.8046),   # ~ interpolated (between Ra's Suwayjil as Saghir and Wadi al Aswad (mouth))
    (28.7374, 34.7960),   # ~ interpolated (between Ra's Suwayjil as Saghir and Wadi al Aswad (mouth))
    (28.6889, 34.7875),   # Wadi al Aswad (mouth) (Q32193863)
    (28.6625, 34.7756),   # Ra's Suwayjil al Kabir (Q32154649)
    (28.6111, 34.7884),   # ~ interpolated (between Ra's Suwayjil al Kabir and Leyja)
    (28.5598, 34.8012),   # Leyja (Q124244907)
    (28.4836, 34.7767),   # Wadi Abu Duwaymah (mouth) (Q32192258)
    (28.4367, 34.7564),   # Sharm el-Qusara (cove) (Q12171727)
    (28.4025, 34.7403),   # Wadi el Maqna (mouth) (Q32191364)
    (28.3944, 34.7350),   # Maqna (Makna) (Q970317)
    (28.3258, 34.7117),   # Wadi Asmar (mouth) (Q32202682)
    (28.2656, 34.6803),   # Sharm Dabba (cove) (Q12171724)
    (28.2199, 34.6631),   # ~ interpolated (between Sharm Dabba (cove) and Sharm Mujawwan (cove))
    (28.1742, 34.6458),   # Sharm Mujawwan (cove) (Q12171725)
    (28.1330, 34.5928),   # Ras Alsheikh Hamid (Q12212737)
    (28.0968, 34.5805),   # Ra's ash Shaykh Humayd (Q32153989)
    (28.0219, 34.6319),   # Ra's al Qasbah (Q32153758)
    (28.0431, 34.6820),   # ~ interpolated (between Ra's al Qasbah and Ghubbat al Wayjil (bay))
    (28.0642, 34.7321),   # ~ interpolated (between Ra's al Qasbah and Ghubbat al Wayjil (bay))
    (28.0853, 34.7822),   # Ghubbat al Wayjil (bay) (Q12098243)
    (28.0947, 34.8333),   # Al Khurmah (bay) (Q12129135)
    (28.0731, 34.8614),   # Ra's Abu Sayf (Q32153287)
    (28.0667, 34.8667),   # Sharm el-Hodda (bay) (Q12171728)
    (28.0750, 34.9083),   # ~ interpolated (between Sharm el-Hodda (bay) and El-Funqur (cove))
    (28.0833, 34.9500),   # El-Funqur (cove) (Q12103811)
    (28.0744, 35.0020),   # ~ interpolated (between El-Funqur (cove) and Khalij 'Aynunah (bight))
    (28.0654, 35.0541),   # ~ interpolated (between El-Funqur (cove) and Khalij 'Aynunah (bight))
    (28.0564, 35.1061),   # Khalij 'Aynunah (bight) (Q32135134)
    (28.0401, 35.1579),   # ~ interpolated (between Khalij 'Aynunah (bight) and Wadi ash Sharmah (mouth))
    (28.0239, 35.2097),   # Wadi ash Sharmah (mouth) (Q32202239)
    (28.0260, 35.2480),   # Sharma (Q16123277)
    (27.9333, 35.2500),   # Sharmah port (Q111387149)
    (27.8905, 35.2852),   # ~ interpolated (between Sharmah port and Ra's Wadi Tarim)
    (27.8476, 35.3204),   # ~ interpolated (between Sharmah port and Ra's Wadi Tarim)
    (27.8047, 35.3556),   # Ra's Wadi Tarim (Q32154741)
    (27.7603, 35.4421),   # Green Duba power plant (Q105029835)
    (27.6817, 35.4737),   # Muwaylih Castle (Q20400630)
    (27.6423, 35.4954),   # ~ interpolated (between Muwaylih Castle and Dhiba Port (Duba port))
    (27.6029, 35.5170),   # ~ interpolated (between Muwaylih Castle and Dhiba Port (Duba port))
    (27.5634, 35.5386),   # Dhiba Port (Duba port) (Q6877704)
    (27.5447, 35.5314),   # Ra's Maharish (Q32154359)
    (27.4974, 35.5657),   # ~ interpolated (between Ra's Maharish and Ra's Abu Sharirah)
    (27.4500, 35.6000),   # Ra's Abu Sharirah (Q32153307)
    (27.4000, 35.6167),   # Ra's al Ghal (Q32153435)
    (27.3667, 35.6500),   # Ra's al 'Uwaynat (Q32153918)
    (27.3606, 35.6611),   # Ra's Dhahakan (Q32154141)
    (27.3493, 35.6962),   # Duba (Q27225)
    (27.3365, 35.7122),   # Beach mosque 2, Duba (masjid ash-shati' 2) (Q138091645)
    (27.2878, 35.7550),   # the mosque named Shati' Duba ('Duba beach') (Q138102168)
]

# ===========================================================================
# The lakes of the isthmus, Lake Bardawil and Tiran
# ===========================================================================

TIMSAH = [
    (30.5667, 32.2667),   # Birkat Abū Jāmūs (lagoon, west end of Lake Timsah) (Q23956540)
    (30.5833, 32.2667),   # Ismailia (city on the north-west shore) (Q217156)
    (30.5859, 32.2880),   # Mercure Ismailia Forsan Island Hotel (Forsan Island, north shore) (Q111857805)
    (30.5879, 32.2932),   # Tolip Resort El Forsan Ismailia (Forsan Island, north shore) (Q111999189)
    (30.5459, 32.3063),   # Suez Canal World War I Memorial (Jebel Mariam, south-east shore) (Q121316177)
]

GREAT_BITTER = [
    (30.2500, 32.4167),   # RAF Kasfareet (south-west shore) (Q130478594)
    (30.2806, 32.3257),   # Kriegsgefangenenlager Fanara (Fanara, west shore) (de:Kriegsgefangenenlager Fanara)
    (30.3261, 32.2986),   # Fayed (west shore) (Q1383404)
    (30.3808, 32.3036),   # Six Corners Resort (Fayed, west shore) (Q111999185)
    (30.4024, 32.3086),   # Abu Sultan Power Station (west shore) (Q56359816)
    (30.4229, 32.3354),   # Deversoir Air Base (Deversoir, north end) (Q5266913)
    (30.3272, 32.4636),   # Winter Lake (lagoon on the east shore) (Q23932211)
    (30.2858, 32.4506),   # Ar Ra's al Bayḑā' (cape on the south-east shore) (Q23952428)
]

LITTLE_BITTER = [
    (30.2458, 32.4900),   # Kibrit Air Base (Kabrit, north-west end) (Q6404068)
    (30.2667, 32.5167),   # Kibrīt (north-east end) (Q23955444)
    (30.2167, 32.5667),   # ‘Alāwī Rumayḩ (hill on the east shore) (Q23938238)
    (30.1154, 32.5604),   # الشلوفة (Shallufa, south end) (Q116037026)
    (30.1881, 32.5442),   # RAF Shandur (west shore) (Q131353898)
]

BARDAWIL = [
    (31.1420, 32.7722),   # ~ interpolated (mediterranean.AFRICA's point between Port Said East Power Plant and Bughaz al Bardawil)
    (31.1844, 33.0247),   # Bughaz al Bardawil (as mediterranean.AFRICA) (Q23952829)
    (31.2250, 33.0983),   # Ra's Burun (as mediterranean.AFRICA) (Q23952575)
    (31.2183, 33.1897),   # Bughaz 'Uways (as mediterranean.AFRICA) (Q23972200)
    (31.1744, 33.4158),   # Bughaz Asy (as mediterranean.AFRICA) (Q23956715)
    (31.1300, 33.4889),   # Bughaz az Zaraniq (as mediterranean.AFRICA) (Q23932369)
    (31.1172, 33.4319),   # Ostrakine (ancient town on the south-east shore) (Q7107719)
    (31.0728, 33.2278),   # Mīnā' at Tulūl (anchorage, south shore) (Q23956713)
    (31.0508, 33.0106),   # Shāţi' Bi'r al ‘Abd (beach, south shore) (Q23975587)
    (31.0797, 32.8933),   # Bardawil Peninsula (south-west shore) (Q23952830)
]

TIRAN = [
    (27.9989, 34.4956),   # Johnson Point (Q23957222)
    (27.9944, 34.4906),   # Mersa Shabir (Q23957223)
    (27.9558, 34.5047),   # Marsa al Mudhbah (Q23973076)
    (27.9372, 34.5261),   # Marsa Khashkhashah (Q23973077)
    (27.9139, 34.5814),   # Marsa Lesafa (Q23973078)
    (27.9178, 34.6119),   # Marsa al Qurayn (Q23973084)
    (27.9431, 34.6364),   # Bahr al A'ashiq (bay) (Q23973079)
    (27.9468, 34.6117),   # ~ interpolated (between Bahr al A'ashiq (bay) and Wadi ath Thumail (mouth))
    (27.9506, 34.5869),   # Wadi ath Thumail (mouth) (Q23973074)
    (27.9747, 34.5413),   # ~ interpolated (between Wadi ath Thumail (mouth) and Johnson Point)
]

# ===========================================================================
# The Nile
# ===========================================================================

# from Maghagha, west of the sheet, to the Delta Barrage, then down the
# Damietta branch to its mouth
NILE = [
    (28.6483, 30.8422),   # Maghagha (west bank) (Q1827283)
    (28.8222, 30.8983),   # Al Fashn (west bank) (Q953625)
    (28.9218, 30.9844),   # Biba (west bank) (Q4902946)
    (29.0667, 31.0833),   # Beni Suef (west bank) (Q394080)
    (29.2020, 31.1435),   # ~ interpolated (between Beni Suef (west bank) and al-Wasta (west bank))
    (29.3372, 31.2036),   # al-Wasta (west bank) (Q4105094)
    (29.4083, 31.2528),   # Atfih (east bank) (Q754592)
    (29.6167, 31.2500),   # El Ayyat (west bank) (Q12242255)
    (29.8514, 31.2742),   # Badrashin (west bank) (Q4165238)
    (29.9675, 31.2500),   # Maadi (east bank, Cairo) (Q589934)
    (30.0069, 31.2250),   # Nilometer in Rhoda Island (Roda Island, Cairo) (Q1992209)
    (30.0437, 31.2297),   # Qasr al-Nil Bridge (Cairo) (Q1973889)
    (30.1186, 31.2258),   # Warraq Island (Cairo) (Q3593306)
    (30.1844, 31.1167),   # Delta Barrage (head of the delta) (Q5254573)
    (30.3236, 31.1482),   # ~ interpolated (between Delta Barrage (head of the delta) and Benha (Damietta branch, east bank))
    (30.4628, 31.1797),   # Benha (Damietta branch, east bank) (Q336966)
    (30.5470, 31.2673),   # Tesfa - Kafr Shokr (Damietta branch, east bank) (Q5607284)
    (30.7192, 31.2628),   # Mit Ghamr (Damietta branch, east bank) (Q337123)
    (30.7437, 31.2406),   # Zifta dam (Damietta branch) (Q16740403)
    (30.9622, 31.2425),   # Samannud (Damietta branch, west bank) (Q1243772)
    (31.0592, 31.3767),   # Talkha (Damietta branch, opposite Mansoura) (Q952118)
    (31.1922, 31.5239),   # Sherbin (Damietta branch) (Q1524502)
    (31.3237, 31.7066),   # Faraskur Bridge (Damietta branch) (Q95567649)
    (31.4167, 31.8214),   # Damietta (Damietta branch, east bank) (Q189383)
    (31.5031, 31.8411),   # Ezbet El Borg (Damietta branch, west bank) (Q1010823)
    (31.5269, 31.8447),   # Damietta Mouth (as mediterranean.AFRICA) (Q23951846)
]

SHORES = {"suez_west": SUEZ_WEST_SHORE, "sinai_west": SINAI_WEST_SHORE,
          "sinai_east": SINAI_EAST_SHORE, "arabia_east": ARABIA_EAST_SHORE}
LAKES = {"timsah": TIMSAH, "great_bitter": GREAT_BITTER,
         "little_bitter": LITTLE_BITTER, "bardawil": BARDAWIL}
ISLANDS = {"tiran": TIRAN}
RIVERS = {"nile": NILE}
