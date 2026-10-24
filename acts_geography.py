"""Geography of Paul's first journey (Acts 13-14), in (lat, lon).

A library for generate_acts1314_svg.py: the coasts of southern Asia Minor,
Syria and Cyprus, the Anatolian lakes and rivers a close-up shows, the
Taurus crest lines, the sites, the roads the route follows, and (for the
sermon, 13:17-26) the places of Israel's story from Egypt to the Jordan.

How it was made. Every commented point is one named place (a town, village,
cape, river mouth, harbour, mound or ancient site) whose coordinate was
taken as a single fact from Wikidata (CC0) or Wikipedia, or for two ancient
sites from vici.org; where the place sits back from the water the point is
the shore nearest it. Points marked "~" are our own interpolation, drawn
from general knowledge of the shore between the anchors. No line geometry
was copied, traced or sampled from OpenStreetMap, Google or any other map or
dataset. Coasts are modern; lakes are drawn at high water.

The far world (Greece, the Aegean, Libya) is the coarse context line of the
Acts 15-18 map; the Levant, Egypt, the Jordan and the tribal lands come from
generate_tribal_maps.py. Sites like Lystra and Derbe are scholarly
identifications; the sermon's places are schematic, as every atlas's are.
"""

# ===========================================================================
# The mainland coast and its rivers
# ===========================================================================

# The mainland coast as one line, west to east along southern Asia Minor,
# round the Gulf of Iskenderun, then south down the Levant to Ras Naqoura.
# Land lies to the left of the direction of travel throughout.
MAIN_COAST = [
    # --- Lycia: Fethiye round the Kayakoy peninsula to Oludeniz
    (36.637, 29.121),   # Fethiye (port, head of the inner bay)
    (36.626, 29.113),   # Fethiye (town quay)
    (36.622, 29.101),   # Karagozler (marina)
    (36.646, 29.088),   # ~ point opposite Sovalye Island
    (36.651, 29.072),   # ~
    (36.646, 29.055),   # ~ facing Kizilada
    (36.630, 29.043),   # ~
    (36.565, 29.015),   # ~
    (36.545, 29.010),   # Dokukbasi Burnu
    (36.567, 29.030),   # ~ north of Balaban Island
    (36.569, 29.048),   # ~
    (36.561, 29.075),   # Gemiler (beach, inside Gemiler Island)
    (36.552, 29.092),   # ~
    (36.550, 29.112),   # Oludeniz (Belcekiz beach)
    (36.538, 29.124),   # ~
    (36.467, 29.101),   # Aktas Burnu
    (36.459, 29.117),   # Kabak (bay)
    (36.415, 29.127),   # ~
    (36.352, 29.134),   # Inkakalar Burnu
    (36.337, 29.155),   # ~ Yediburun cliffs
    (36.332, 29.182),   # Kilic Burnu
    (36.330, 29.231),   # Pydnae (shore)
    (36.294, 29.261),   # Esen Cayi (Xanthos river) mouth
    (36.257, 29.307),   # Patara (old harbour mouth)
    (36.256, 29.380),   # ~
    (36.262, 29.414),   # Kalkan (harbour)
    (36.229, 29.450),   # Kaputas Beach
    (36.206, 29.515),   # ~
    (36.198, 29.562),   # ~ Bucak bay entrance
    (36.172, 29.630),   # Gata Burnu
    (36.197, 29.640),   # Kas (harbour)
    (36.142, 29.667),   # ~
    (36.129, 29.686),   # Uluburun
    (36.158, 29.712),   # ~ inside Kormen Island
    (36.185, 29.754),   # Bogazcik (inlet)
    (36.187, 29.770),   # Sahilkilincli (shore)
    (36.160, 29.785),   # Aperlae
    (36.150, 29.797),   # ~ tip of the Sicak peninsula
    (36.194, 29.846),   # Ucagiz
    (36.189, 29.862),   # Simena (Kalekoy), behind Kekova Island
    (36.195, 29.877),   # ~
    (36.216, 29.898),   # ~ inside Kisneli and Asirli islands
    (36.197, 29.915),   # Geyikova Burnu
    (36.222, 29.951),   # Andriake (port of Myra)
    (36.233, 30.011),   # Demre Creek (Myros) mouth
    (36.254, 30.054),   # Beymelek (beach before the lagoon)
    (36.259, 30.069),   # Dalyan Bogazi (Beymelek lagoon outlet)
    (36.249, 30.100),   # Bunda Burnu
    (36.257, 30.114),   # Akliman (bay)
    (36.263, 30.137),   # ~ headland opposite Guvercin Island
    (36.282, 30.152),   # Suluin Cave (sea cave on the shore south of Finike)
    (36.297, 30.149),   # Finike (harbour)
    # --- the Finike-Kumluca beach, Cape Gelidonya, Olympos, Kemer
    (36.304, 30.158),   # Kum, Finike (shore)
    (36.316, 30.253),   # Alakir Cayi mouth
    (36.308, 30.303),   # ~ below Mavikent
    (36.288, 30.347),   # Gagai (shore)
    (36.255, 30.392),   # Karaoz (bay)
    (36.232, 30.404),   # Dikici Burnu
    (36.213, 30.410),   # Cape Gelidonya (lighthouse; Besadalar offshore)
    (36.250, 30.430),   # ~ headland north of the cape
    (36.252, 30.450),   # Kelleci Burnu (Suluada offshore)
    (36.300, 30.486),   # Fener Burnu
    (36.319, 30.475),   # Adrasan (beach at the head of Adrasan Bay)
    (36.338, 30.527),   # Atrasan Burnu
    (36.396, 30.479),   # Olympos (beach)
    (36.437, 30.488),   # Corycus (Atbuku)
    (36.450, 30.508),   # Tatlisu (bay)
    (36.503, 30.535),   # Tekirova (shore)
    (36.521, 30.555),   # Phaselis (Asar Burnu)
    (36.552, 30.567),   # Camyuva (shore)
    (36.567, 30.576),   # Kiris
    (36.578, 30.586),   # Av Burnu
    (36.600, 30.571),   # Kemer (marina)
    (36.612, 30.560),   # ~ Kemer north beach
    (36.640, 30.552),   # ~ Arslanbucak bay (seaward of its beach resorts)
    (36.668, 30.566),   # Goynuk (beach)
    (36.704, 30.575),   # Azmak Burnu
    (36.723, 30.571),   # Beldibi (shore)
    (36.802, 30.584),   # Sican Islet (shore inside it)
    # --- Pamphylia: Attalia, the Cestrus and Eurymedon mouths, Side
    (36.834, 30.611),   # Port of Antalya
    (36.846, 30.618),   # Liman, Konyaalti (shore)
    (36.854, 30.627),   # Bogacay mouth
    (36.864, 30.643),   # Konyaalti Beach
    (36.884, 30.701),   # Antalya Harbour (Attalia)
    (36.880, 30.702),   # ~ below the Hidirlik Tower
    (36.873, 30.711),   # ~ cliffs below Karaalioglu Park
    (36.860, 30.728),   # ~ cliffs
    (36.843, 30.758),   # Baba Burnu
    (36.851, 30.784),   # ~ lower Duden falls
    (36.848, 30.813),   # Lara (beach)
    (36.853, 30.893),   # ~
    (36.854, 30.920),   # Aksu Brook (Cestrus) mouth
    (36.856, 31.005),   # ~ below Kadriye
    (36.855, 31.033),   # ~
    (36.847, 31.058),   # Belek (beach)
    (36.841, 31.084),   # Eleri Burnu
    (36.838, 31.124),   # Acisu Brook mouth
    (36.830, 31.173),   # Koprucay River (Eurymedon) mouth
    (36.817, 31.267),   # Aktas Burnu (Side)
    (36.821, 31.290),   # ~ Colakli beach
    (36.811, 31.325),   # ~ Kumkoy beach
    (36.800, 31.357),   # ~
    (36.786, 31.378),   # ~
    (36.776, 31.385),   # ~ beach north of the Side peninsula
    (36.763, 31.386),   # Side (tip of the peninsula)
    (36.770, 31.401),   # ~ Side east beach
    (36.754, 31.452),   # ~ Sorgun beach
    (36.737, 31.494),   # Manavgat River (Melas) mouth
    (36.727, 31.535),   # Kizilagac (shore)
    (36.688, 31.618),   # Cenger (shore)
    (36.664, 31.662),   # Alara Brook mouth
    (36.646, 31.675),   # Karaburun (Kibyra Minor)
    (36.644, 31.705),   # Okurcalar (shore)
    (36.638, 31.737),   # Incekum (shore)
    (36.617, 31.766),   # Avsallar (shore)
    (36.606, 31.775),   # Fidan Burnu
    (36.603, 31.799),   # Kargi River mouth
    (36.593, 31.856),   # Payallar (shore)
    (36.579, 31.893),   # Konakli (shore)
    (36.553, 31.971),   # Kleopatra beach
    (36.544, 31.983),   # Damlatas beach
    (36.527, 31.986),   # Dildarde Burnu
    (36.523, 31.993),   # ~ south tip of the Alanya peninsula
    (36.537, 32.001),   # Alanya Port (Kizil Kule)
    (36.542, 32.010),   # People's beach (Keykubat)
    (36.540, 32.028),   # ~
    # --- Rough Cilicia: Alanya, Selinus, Cape Anamur, Aydincik
    (36.523, 32.055),   # Dim River mouth
    (36.487, 32.103),   # Mahmutlar (shore)
    (36.451, 32.127),   # Kargagedik Burnu
    (36.443, 32.145),   # Syedra (below the site)
    (36.432, 32.160),   # ~
    (36.399, 32.181),   # ~ below Kesefli
    (36.347, 32.214),   # ~ below Ugrak
    (36.320, 32.232),   # Iotape (Aytap, on its promontory)
    (36.287, 32.276),   # Bickici Creek mouth
    (36.258, 32.282),   # Selinus (Gazipasa castle hill)
    (36.240, 32.311),   # ~ below Gazipasa
    (36.192, 32.371),   # ~ below Beyrebucak
    (36.164, 32.390),   # Kesik Burnu
    (36.155, 32.416),   # Antiochia ad Cragum
    (36.123, 32.484),   # Zeytinada (shore)
    (36.110, 32.489),   # Aksay Burnu
    (36.099, 32.550),   # Yakacik (shore)
    (36.104, 32.562),   # Charadros (Kaladran)
    (36.083, 32.600),   # Karga Burnu
    (36.078, 32.620),   # ~ below Ucari
    (36.041, 32.681),   # Karatas Burnu
    (36.043, 32.700),   # ~ below Platanus
    (36.034, 32.740),   # Coban Castle (shore)
    (36.029, 32.783),   # ~
    (36.017, 32.803),   # Cape Anamur (lighthouse), southernmost point of Asia Minor
    (36.024, 32.806),   # Anemurium (shore below the walls)
    (36.038, 32.811),   # ~
    (36.051, 32.825),   # ~
    (36.081, 32.895),   # Mamure Castle
    (36.098, 32.974),   # Bozyazi (Nagidussa islet just off)
    (36.097, 33.010),   # ~ below Softa Castle
    (36.068, 33.066),   # Kizilburun bay
    (36.068, 33.080),   # Kizilliman Burnu
    (36.095, 33.100),   # Kirse Burnu
    (36.123, 33.115),   # Mandane (shore)
    (36.130, 33.185),   # Gozsuzce (shore)
    (36.127, 33.236),   # ~
    (36.131, 33.300),   # Karabiyik Burnu
    (36.142, 33.322),   # Aydincik (harbour)
    (36.148, 33.343),   # ~ inside the Aydincik Islands
    (36.146, 33.365),   # ~ inside Yelkenli Island
    (36.131, 33.396),   # Aydincik Lighthouse (point)
    (36.137, 33.406),   # Berenike (Kilikya)
    (36.158, 33.457),   # Pisourgia (shore)
    (36.151, 33.485),   # Babadil Port (bay)
    (36.129, 33.524),   # ~ inside the Babadil Islands
    (36.125, 33.541),   # Craunos
    (36.158, 33.546),   # Babadil Creek mouth
    (36.181, 33.592),   # ~
    (36.187, 33.622),   # ~ head of the Gulf of Ovacik
    (36.186, 33.656),   # Yesilovacik (fishing port)
    (36.134, 33.683),   # Cape Tisan
    (36.145, 33.693),   # ~ inside Ovacik Island
    (36.160, 33.698),   # Koselik (site)
    (36.175, 33.712),   # ~
    (36.204, 33.764),   # Kargincik Bogazi (inside Dana Adasi)
    (36.250, 33.806),   # Egribuk (Philaea)
    (36.264, 33.815),   # Porto Pini
    (36.270, 33.826),   # Bogsak
    (36.279, 33.836),   # Liman Castle
    (36.303, 33.853),   # Mylae
    (36.311, 33.863),   # Holmi
    (36.316, 33.884),   # Tasucu (harbour)
    # --- the Goksu (Calycadnus) delta and Cape Sarpedon
    (36.272, 33.904),   # Aga Limani (bay)
    (36.261, 33.920),   # ~
    (36.248, 33.962),   # Cape Sarpedon (Incekum, tip of the delta)
    (36.255, 33.985),   # ~ seaward face of the Paradeniz spit
    (36.278, 34.028),   # ~
    (36.297, 34.047),   # River Goksu (Calycadnus) mouth
    (36.345, 34.064),   # ~ below Arkum
    (36.408, 34.079),   # Korasion
    (36.426, 34.099),   # Cebicini Creek mouth
    # --- Plain Cilicia: Korykos, Mersin, the Seyhan and Ceyhan deltas
    (36.441, 34.113),   # Narlikuyu
    (36.456, 34.135),   # Akkum (port)
    (36.461, 34.147),   # Kizkalesi (Korykos; Maiden's Castle offshore)
    (36.486, 34.177),   # Ayas (Elaiussa Sebaste)
    (36.513, 34.204),   # Tirtar (shore)
    (36.557, 34.248),   # Limonlu Cayi (Lamos) mouth
    (36.598, 34.307),   # Erdemli (shore)
    (36.604, 34.320),   # Alata Creek mouth
    (36.619, 34.342),   # ~ Deliali
    (36.671, 34.414),   # ~ below Kargipinari
    (36.702, 34.461),   # Tece (shore)
    (36.738, 34.542),   # Soli Pompeiopolis (ancient harbour)
    (36.766, 34.576),   # Mersin Marina
    (36.786, 34.621),   # Muftu River mouth
    (36.797, 34.640),   # Port of Mersin
    (36.808, 34.707),   # Delicay mouth (shore below Karaduvar)
    (36.809, 34.755),   # Kazanli (shore)
    (36.785, 34.840),   # ~
    (36.751, 34.894),   # Berdan Brook (Cydnus) mouth
    (36.728, 34.906),   # Deli Burnu (Seyhan / Sarus mouth)
    (36.706, 35.000),   # ~
    (36.681, 35.082),   # ~
    (36.667, 35.122),   # ~ below Tabur
    (36.637, 35.200),   # ~
    (36.613, 35.270),   # ~
    (36.576, 35.317),   # ~
    (36.557, 35.327),   # Dalyan Bogazi (lagoon channel)
    (36.540, 35.340),   # Karatas Burnu
    (36.561, 35.378),   # Karatas (Magarsa, harbour)
    (36.568, 35.400),   # ~ below Kucuk Island
    (36.573, 35.460),   # ~
    (36.565, 35.559),   # Ceyhan River (Pyramus) mouth
    (36.585, 35.578),   # ~
    (36.635, 35.620),   # ~
    (36.685, 35.662),   # ~
    (36.726, 35.697),   # Uzunburun Dili (spit tip)
    (36.734, 35.655),   # Arap Bogazi (lagoon channel)
    (36.749, 35.636),   # Dar Bogaz (lagoon channel)
    (36.766, 35.684),   # Aran Creek mouth
    (36.766, 35.717),   # Bagirsak Creek mouth
    (36.765, 35.791),   # Yumurtalik (Ayas / Aigeai; Yumurtalik Island off)
    # --- round the Gulf of Iskenderun
    (36.778, 35.807),   # Akyuva (shore)
    (36.822, 35.866),   # Sugozu (shore)
    (36.869, 35.917),   # Kamisli Burun
    (36.881, 35.933),   # Botas (terminal)
    (36.912, 35.966),   # Toros Gubre (port)
    (36.920, 35.990),   # ~
    (36.921, 36.039),   # Burnaz Plaji (head of the gulf)
    (36.917, 36.063),   # ~
    (36.897, 36.105),   # ~
    (36.867, 36.133),   # Botas Dortyol Oil Terminal
    (36.845, 36.161),   # Kinet Hoyuk / Issus (shore)
    (36.830, 36.168),   # Deli Brook mouth
    (36.753, 36.190),   # Payas River (Pinarus) mouth
    (36.686, 36.200),   # Assan Port Iskenderun
    (36.660, 36.210),   # Sariseki (shore)
    (36.633, 36.209),   # Denizciler (shore)
    (36.594, 36.182),   # Port of Iskenderun
    (36.597, 36.164),   # Iskenderun (Alexandria by Issus; seafront by the Naval Museum)
    (36.588, 36.150),   # ~
    (36.570, 36.133),   # Karaagac (shore)
    (36.565, 36.112),   # Myriandrus
    (36.553, 36.094),   # ~
    (36.507, 36.040),   # ~
    (36.479, 35.996),   # ~
    (36.467, 35.952),   # Gulcihan (shore)
    (36.412, 35.886),   # Arsuz (Rhosus)
    (36.365, 35.828),   # Avcilar Brook mouth (Konacik)
    (36.318, 35.781),   # Ras el-Khanzir (Akinci Burnu, lighthouse)
    (36.290, 35.790),   # Kale (shore)
    (36.241, 35.827),   # Holtakayasi Burnu
    (36.173, 35.879),   # Hirlavuk Burnu
    (36.123, 35.917),   # Seleucia Pieria (Cevlik, Suveydiye bay)
    (36.106, 35.929),   # ~
    (36.045, 35.963),   # Orontes River mouth
    # --- Syria: Ras al-Bassit, Latakia, Jableh, Baniyas, Tartus
    (36.005, 35.953),   # ~
    (35.944, 35.934),   # Denizgoren (shore, below Jebel Aqra)
    (35.905, 35.904),   # ~
    (35.862, 35.850),   # ~
    (35.853, 35.826),   # Ras el Meydan
    (35.858, 35.814),   # Ras al-Malaha
    (35.854, 35.801),   # Ras al-Bassit
    (35.786, 35.835),   # ~
    (35.763, 35.840),   # ~ below Umm al-Tuyour
    (35.709, 35.816),   # Ras al-Khanzir (Syria)
    (35.679, 35.777),   # Ras al-Fasuri
    (35.637, 35.781),   # Ras al-Barsum
    (35.607, 35.776),   # Minet el-Beida (harbour of Ugarit)
    (35.594, 35.751),   # Ras Ibn Hani
    (35.587, 35.718),   # Ras al-Fanar (tip of Ras Ibn Hani)
    (35.579, 35.721),   # Ras al-Kuwayk
    (35.577, 35.735),   # Mina al-Qabban (cove)
    (35.568, 35.741),   # ~
    (35.558, 35.739),   # Ras al-Aawaj
    (35.550, 35.753),   # Masbah Afamiya
    (35.537, 35.765),   # ~ inside Jazirat as-Sayd
    (35.524, 35.769),   # ~
    (35.514, 35.765),   # Port of Latakia (Laodicea)
    (35.501, 35.735),   # Ras Ziyara (Latakia)
    (35.494, 35.752),   # ~
    (35.494, 35.800),   # Nahr al-Kabir al-Shamali mouth
    (35.471, 35.853),   # Tilul al-Bahr (dunes)
    (35.416, 35.910),   # Mina al-Rus (bay)
    (35.378, 35.917),   # Gabala (ancient harbour)
    (35.360, 35.917),   # Jableh
    (35.306, 35.921),   # Tell Sukas
    (35.263, 35.924),   # Ras Baldat al-Malik
    (35.245, 35.930),   # ~
    (35.182, 35.935),   # Baniyas (harbour)
    (35.172, 35.924),   # Ras al-Marj
    (35.149, 35.917),   # Ras al-Burj
    (35.070, 35.902),   # ~
    (35.040, 35.894),   # ~
    (34.989, 35.878),   # Ras al-Hasan (Busayra island just off)
    (34.939, 35.882),   # Carne (shore)
    (34.913, 35.876),   # Tartus Port
    (34.887, 35.879),   # Tartus (Arwad island offshore)
    (34.840, 35.893),   # ~ Amrit
    (34.818, 35.893),   # ~ inside al-Abbas island
    (34.794, 35.898),   # ~ inside the Fanais islands
    (34.770, 35.908),   # ~
    (34.717, 35.932),   # Orthosia (shore)
    (34.663, 35.961),   # ~
    (34.638, 35.973),   # Nahr al-Kabir al-Janoubi mouth (Syria-Lebanon border)
    # --- Phoenicia (Lebanon): Tripoli, Byblos, Beirut, Sidon, Tyre
    (34.610, 35.977),   # ~
    (34.560, 35.972),   # ~
    (34.513, 35.953),   # Nahr al-Bared mouth (Orthosias)
    (34.471, 35.898),   # Ras al-Ladus
    (34.459, 35.843),   # Ras Borj en Nahr (Abu Ali / Kadisha mouth)
    (34.457, 35.829),   # Port of Tripoli
    (34.451, 35.805),   # Jouret el Aabd (west tip of al-Mina)
    (34.424, 35.819),   # El Ammine
    (34.388, 35.782),   # Kalamos (Qalamoun)
    (34.375, 35.737),   # Ras en Natour
    (34.325, 35.725),   # ~ inside the Anfeh islets
    (34.308, 35.692),   # Ras ech Chaqaa (Theoprosopon)
    (34.267, 35.656),   # Ras Kubba (Nahr al-Jaouz mouth)
    (34.255, 35.655),   # Batroun
    (34.211, 35.649),   # Nahr Madfoun mouth
    (34.193, 35.646),   # El Berbara
    (34.150, 35.632),   # Ras Amshit
    (34.120, 35.642),   # Byblos (harbour)
    (34.100, 35.646),   # ~
    (34.063, 35.641),   # Abraham River (Nahr Ibrahim) mouth
    (34.019, 35.627),   # Ras al-Ma'amiltayn
    (34.013, 35.634),   # Ed Daoura
    (33.993, 35.636),   # Baie de Jounie (head)
    (33.985, 35.628),   # Jounieh beach
    (33.971, 35.604),   # Mina el Hadid
    (33.958, 35.596),   # Nahr al-Kalb mouth
    (33.950, 35.588),   # Ras al-Kalb
    (33.933, 35.587),   # Dbayeh (shore)
    (33.922, 35.580),   # ~ Antelias
    (33.904, 35.542),   # Beirut River mouth
    (33.908, 35.518),   # Port of Beirut
    (33.900, 35.497),   # Ras ash-Shamiyah
    (33.901, 35.484),   # Ras al-Mudawwar
    (33.899, 35.473),   # Old Beirut Lighthouse
    (33.893, 35.469),   # Ras Beirut
    (33.887, 35.473),   # Ras al-Gharah (Raouche; shore facing the Pigeon Rocks)
    (33.877, 35.477),   # ~ Ramlet al-Baida beach
    (33.862, 35.481),   # ~ Jnah
    (33.824, 35.482),   # Chatt el Ouzaai (beach)
    (33.786, 35.475),   # ~
    (33.733, 35.450),   # Ras al-Misri
    (33.705, 35.438),   # Damour River mouth
    (33.689, 35.416),   # Ras es Saadiyat
    (33.648, 35.399),   # Ras Nabi Younes
    (33.589, 35.384),   # Awali River mouth
    (33.565, 35.370),   # Sidon (sea castle; Zira island off)
    (33.537, 35.360),   # Sayniq River mouth
    (33.495, 35.334),   # Zahrani River mouth
    (33.472, 35.309),   # Dahr el Burj
    (33.462, 35.288),   # Ras ash-Shaqq
    (33.448, 35.284),   # ~ Sarafand (Zarephath)
    (33.381, 35.251),   # Ras Abu Zeid
    (33.339, 35.244),   # Litani River mouth
    (33.308, 35.224),   # Ras ad-Din
    (33.294, 35.219),   # Ibrial (beach)
    (33.280, 35.203),   # Bahr al-Mubarakah (north bay of Tyre)
    (33.276, 35.193),   # Tyre Lighthouse
    (33.267, 35.191),   # Ras Minat ar-Rasas
    (33.260, 35.204),   # Bahr es Slaiyeb (south bay of Tyre)
    (33.232, 35.213),   # ~ Rashidieh
    (33.198, 35.197),   # ~
    (33.165, 35.168),   # Ras al-Bayada
    (33.144, 35.155),   # Ras ad-Drijat
    (33.111, 35.113),   # Ras al-Madfoun
    (33.093, 35.104),   # Ras Naqoura (Rosh HaNikra)
]


# --- Rivers, each listed from upstream down to its mouth (the mouth is the
# matching MAIN_COAST point).

# The Orontes from the Ghab below Apamea, north past Jisr al-Shughur and
# Darkush, round by the Iron Bridge to Antioch, and down to the sea.
ORONTES = [
    (35.400, 36.383),   # ~ below Qalaat al-Madiq (Apamea), in the Ghab
    (35.440, 36.378),   # ~
    (35.490, 36.372),   # ~
    (35.540, 36.365),   # ~
    (35.587, 36.356),   # ~ in the Al-Ghab plain
    (35.640, 36.346),   # ~
    (35.689, 36.336),   # Al-Ziyarah
    (35.744, 36.320),   # Qarqur
    (35.813, 36.318),   # Jisr al-Shughur
    (35.850, 36.330),   # ~
    (35.921, 36.358),   # Kafr Debbin
    (35.993, 36.390),   # Darkush
    (36.069, 36.371),   # Hacipasa (Turkish border)
    (36.150, 36.378),   # ~
    (36.190, 36.374),   # ~
    (36.248, 36.353),   # Demirkopru (the Iron Bridge)
    (36.220, 36.248),   # ~
    (36.202, 36.160),   # Antioch (Antakya, old bridge)
    (36.182, 36.105),   # ~
    (36.161, 36.013),   # Westayaz Bridge (Batiayaz)
    (36.078, 35.989),   # ~ below Samandag
    (36.045, 35.963),   # Orontes River mouth
]

# Aksu Cayi (Cestrus): from the Karacaoren-2 dam down past Perga to the sea.
CESTRUS = [
    (37.307, 30.809),   # Karacaoren-2 Dam
    (37.270, 30.822),   # ~
    (37.190, 30.857),   # ~
    (37.110, 30.882),   # ~
    (37.070, 30.888),   # ~
    (36.995, 30.887),   # ~
    (36.944, 30.897),   # Aksu Bridge
    (36.876, 30.912),   # Kundu (beside the river)
    (36.854, 30.920),   # Aksu Brook mouth
]

# Kopru Cayi (Eurymedon): from the Roman bridge in the Koprulu canyon below
# Selge, past Aspendos to the sea.
EURYMEDON = [
    (37.192, 31.181),   # Eurymedon Bridge (Oluk Koprusu, Koprulu canyon)
    (37.145, 31.198),   # Beskonak
    (37.085, 31.201),   # ~
    (37.025, 31.193),   # ~
    (36.939, 31.176),   # Aspendos
    (36.914, 31.164),   # Eurymedon Bridge (Aspendos)
    (36.890, 31.162),   # ~
    (36.830, 31.173),   # Koprucay River mouth
]

# Manavgat Cayi (Melas): from the Oymapinar dam, past the Manavgat dam and
# waterfall, through Manavgat to the sea east of Side.
MELAS = [
    (36.909, 31.532),   # Oymapinar Dam
    (36.835, 31.518),   # Manavgat Dam
    (36.825, 31.450),   # Naras Bridge
    (36.813, 31.454),   # Manavgat Waterfall
    (36.787, 31.448),   # Manavgat Bridge (Manavgat town)
    (36.774, 31.453),   # ~
    (36.737, 31.494),   # Manavgat River mouth
]

# Goksu (Calycadnus): from Mut down the Goksu canyon past the Barbarossa
# memorial, through Silifke (Seleucia) and the delta to the sea.
CALYCADNUS = [
    (36.640, 33.440),   # Mut (stone bridge)
    (36.560, 33.475),   # ~ below Koselerli
    (36.514, 33.518),   # Kayraktepe Dam
    (36.508, 33.540),   # Kurtsuyu
    (36.480, 33.605),   # ~
    (36.448, 33.680),   # ~
    (36.437, 33.720),   # ~
    (36.413, 33.800),   # ~
    (36.401, 33.840),   # Frederick Barbarossa Memorial (below it)
    (36.398, 33.865),   # ~ below Eksiler (opposite bank)
    (36.379, 33.925),   # Silifke (Tas Kopru, the Roman bridge)
    (36.342, 33.983),   # ~
    (36.297, 34.047),   # River Goksu mouth
]

# Berdan Cayi / Tarsus Cayi (Cydnus): from the Berdan dam, over the Tarsus
# waterfall and through Tarsus to the sea.
CYDNUS = [
    (36.966, 34.895),   # Berdan Dam
    (36.933, 34.898),   # Tarsus Waterfall
    (36.921, 34.919),   # Bac Bridge (Tarsus)
    (36.835, 34.905),   # ~
    (36.751, 34.894),   # Berdan Brook mouth
]

# Seyhan (Sarus): from the Seyhan dam, through Adana, south and then
# south-west across the plain to Deli Burnu.
SARUS = [
    (37.039, 35.332),   # Seyhan Dam
    (36.986, 35.335),   # Adana (Taskopru, the Roman bridge)
    (36.912, 35.339),   # ~
    (36.843, 35.334),   # ~ beside Dogankent
    (36.820, 35.300),   # ~
    (36.800, 35.250),   # ~
    (36.781, 35.190),   # ~
    (36.765, 35.130),   # ~
    (36.752, 35.070),   # ~
    (36.743, 35.010),   # ~ beside Tabaklar
    (36.728, 34.906),   # Seyhan River mouth (Deli Burnu)
]

# Ceyhan (Pyramus): from Ceyhan town, past Misis (Mopsuestia) and Mallos
# to the mouth east of Karatas.
PYRAMUS = [
    (37.029, 35.813),   # Ceyhan (town)
    (37.020, 35.775),   # ~
    (36.990, 35.695),   # ~
    (36.957, 35.626),   # Misis Bridge (Mopsuestia)
    (36.917, 35.567),   # Abdioglu Cumhuriyet (beside the river)
    (36.840, 35.522),   # ~
    (36.758, 35.487),   # Malus Bridge (Mallos, Kiziltahta)
    (36.722, 35.505),   # ~
    (36.690, 35.533),   # Kaldirim (beside the river)
    (36.632, 35.544),   # Adali
    (36.565, 35.559),   # Ceyhan River mouth
]


# ===========================================================================
# Cyprus
# ===========================================================================

# Whole island as one closed ring, clockwise (north up), starting at Cape
# Arnauti on the Akamas: Chrysochou Bay -> Tylliria -> Morphou Bay ->
# Kormakitis -> Kyrenia -> Karpas north shore -> Cape Apostolos Andreas ->
# Karpas south shore -> Famagusta Bay -> Cape Greco -> Larnaca Bay ->
# Limassol -> Akrotiri -> Episkopi Bay -> Paphos -> Akamas west shore.
# The first point is not repeated at the end.
CYPRUS = [
    # Akamas, north-east shore, into Chrysochou Bay
    (35.104, 32.284),   # Cape Arnauti (Akrotirio Arnaoutis)
    (35.083, 32.305),   # Blue Lagoon (inside Nisida tis Chamilis islet)
    (35.075, 32.319),   # Argaki ton Kolympoudion (mouth), inshore of St George's islet
    (35.057, 32.347),   # Baths of Aphrodite (Argaki tou Pyrgou mouth)
    (35.046, 32.363),   # Argaki tou Vato (mouth)
    (35.041, 32.395),   # Latchi (harbour)
    (35.045, 32.420),   # Chrysochou river mouth (Polis)
    (35.055, 32.454),   # Limni (old mine pier)
    (35.068, 32.469),   # Makounta river mouth
    (35.073, 32.489),   # Argaka (shore)
    (35.094, 32.495),   # Xeropotamos mouth (Gialia)
    (35.121, 32.509),   # Agia Marina Chrysochous (shore)
    (35.148, 32.531),   # Argaki tou Symvoulo (mouth, Nea Dimmata)
    (35.163, 32.545),   # Livadi river mouth (Pomos)
    (35.176, 32.555),   # Pomos Point (Akro Pomos)
    # Tylliria coast to Morphou Bay
    (35.172, 32.585),   # Pachyammos
    (35.181, 32.607),   # Rotsos ton Skafon (Kokkina / Erenkoy)
    (35.193, 32.623),   # Cape Stavromeni
    (35.193, 32.671),   # Cape Kokkina (Akro Kokkina), past Mansoura and Geronisos
    (35.187, 32.688),   # Kato Pyrgos
    (35.181, 32.713),   # ~ (below the Ammadies woods)
    (35.1785, 32.7425), # Cape Limniti (Limnitis / Yesilirmak), inshore of Petra tou Limniti
    (35.165, 32.765),   # ~ (below Loutros and Vouni)
    (35.160, 32.788),   # Mersinaki
    (35.145, 32.805),   # Karavostasi (Potamos tou Kampou mouth)
    (35.139, 32.826),   # Soli / Gemikonagi (shore)
    (35.148, 32.849),   # Xeros river mouth (Setrachos)
    (35.158, 32.866),   # Karkotis river mouth
    (35.170, 32.891),   # Atsas (river mouth)
    (35.201, 32.916),   # ~ head of Morphou Bay, below Leivadia hill
    (35.228, 32.925),   # Serrachis river mouth (Stoma tou Potamou)
    (35.263, 32.932),   # ~ (below Angoulos hill)
    (35.303, 32.934),   # Palaiokastro (Agia Eirini / Akdeniz)
    (35.335, 32.929),   # ~ (west of Papa Vasilis)
    (35.4038, 32.921),  # Cape Kormakitis (lighthouse on the tip)
    # North coast to Kyrenia
    (35.395, 32.942),   # ~
    (35.385, 32.957),   # Livera (Sadrazamkoy)
    (35.376, 32.996),   # Foni (shore)
    (35.369, 33.032),   # Orga (Kayalar, shore)
    (35.363, 33.080),   # ~ (Yeorgious Bay)
    (35.369, 33.114),   # Vavilas Point
    (35.354, 33.186),   # Mavrolimni (stream mouth, Lapithos)
    (35.359, 33.199),   # Lambousa (ancient Lapathos)
    (35.357, 33.216),   # Acheiropoietos (point, monastery by Lambousa)
    (35.346, 33.233),   # Pentemili beach, inshore of Kalamoulia islet
    (35.350, 33.260),   # Trachia (headland, Agios Georgios / Karaoglanoglu)
    (35.343, 33.320),   # Kyrenia (castle and harbour)
    # Kyrenia to Kaplica
    (35.336, 33.360),   # Argaki ton Kamaron (mouth), below Achelias hill
    (35.333, 33.428),   # Vrysi (Agios Epiktitos / Catalkoy)
    (35.335, 33.492),   # Alagadi Beach
    (35.343, 33.522),   # Argaki ton Limnon (mouth)
    (35.348, 33.570),   # Argaki tou Kalogyro (mouth, Esentepe), inshore of Choti islet
    (35.360, 33.608),   # Cape Stazousa
    (35.363, 33.662),   # Argaki ton Kankellion (mouth, Kalograia / Bahceli)
    (35.370, 33.686),   # Viklari (stream mouth)
    (35.389, 33.716),   # Angouloi (stream mouth)
    (35.4087, 33.7531), # Kara Burun (point)
    (35.408, 33.762),   # Eliopotamos mouth (Akanthou / Tatlisu)
    (35.4138, 33.7758), # Yayvan Burnu (point)
    (35.412, 33.842),   # Fytefta (stream mouth, below Melissa hill)
    (35.424, 33.898),   # Stouppos (stream mouth, Davlos / Kaplica)
    (35.436, 33.917),   # Karavopetra (headland)
    # Karpas north shore
    (35.435, 33.933),   # Villoures (stream mouth)
    (35.451, 33.954),   # Galounia (headland)
    (35.458, 34.009),   # Potamos tis Agias (mouth)
    (35.470, 34.029),   # Cape Giouti, inshore of Skales islet
    (35.470, 34.046),   # ~ (inshore of Chernos islet)
    (35.481, 34.058),   # Kourtoulla (stream mouth)
    (35.498, 34.100),   # Kamara (stream mouth, Vouppes)
    (35.531, 34.151),   # Potamos tou Pavloudiou (mouth)
    (35.546, 34.171),   # ~ (inshore of Skamni islet)
    (35.560, 34.177),   # Cape Plakoti, inshore of Koutoullis and Daimoniaris islets
    (35.552, 34.187),   # ~
    (35.541, 34.193),   # Yialousa (Yeni Erenkoy, shore)
    (35.562, 34.209),   # Parmakli Burun (point)
    (35.561, 34.2215),  # Cape Glykiotissa
    (35.571, 34.255),   # Agios Thyrsos
    (35.589, 34.313),   # Therio (stream mouth)
    (35.604, 34.327),   # Kergo Point (Ronnas Bay)
    (35.6226, 34.3468), # Lempos (point)
    (35.627, 34.365),   # Krikos Point (Karpasia / Agios Philon)
    (35.6377, 34.3964), # Pyra Chorafia (point)
    (35.642, 34.419),   # Argaki tis Gournas (mouth), north of Rizokarpaso
    (35.649, 34.444),   # Aphendrika (Ourania)
    (35.675, 34.508),   # Mora Psaria (cape)
    (35.6755, 34.530),  # ~ (inshore of the Kordylia islets)
    (35.689, 34.545),   # Cape Proti
    (35.696, 34.589),   # Cape Apostolos Andreas (Kastros)
    # Karpas south shore, back down to Famagusta Bay
    (35.680, 34.584),   # ~
    (35.659, 34.574),   # Apostolos Andreas Monastery (shore)
    (35.642, 34.562),   # Cape Galounopetra
    (35.634, 34.531),   # Cape Pachyammos, past Golden Beach (Nangomi)
    (35.626, 34.505),   # Cape Kiles
    (35.583, 34.433),   # Khiomi Point
    (35.5915, 34.4265), # ~ (cove head, inshore of Nisi Asiro / Aspro Island)
    (35.5816, 34.4168), # Litharkes (stream mouth, Chelones)
    (35.558, 34.408),   # Melissakros Point
    (35.550, 34.390),   # Morosyko (stream mouth)
    (35.542, 34.372),   # ~ (south shore below Rizokarpaso / Dipkarpaz)
    (35.521, 34.340),   # ~ (below Kamares hill)
    (35.497, 34.300),   # ~ (below Perdikia hill and Galinoporni / Kaleburnu)
    (35.476, 34.266),   # Mavroyi (stream mouth), past Nitovikla
    (35.465, 34.214),   # Neta (Taslica, shore)
    (35.438, 34.171),   # Agia (stream mouth, Skalifourda)
    (35.4185, 34.1405), # ~ (shore below Koma tou Gialou / Kumyali, village ~1.4 km inland)
    (35.410, 34.128),   # Derin Dere (Titsiro Potamos, mouth), east of the Koronia woods
    (35.380, 34.096),   # Agia Thekla (chapel on the shore, Bafra)
    (35.357, 34.080),   # Palloura (point, below Vokolida)
    (35.327, 34.063),   # Cape Elaia
    (35.3242, 34.047),  # Cape Elea lighthouse (shore)
    (35.331, 34.003),   # ~ (below Gastria / Kalecik)
    (35.323, 33.981),   # Gastria Castle
    (35.316, 33.957),   # Bogaz (Bogazi harbour)
    # Famagusta Bay
    (35.304, 33.942),   # Yeropotamos (mouth)
    (35.256, 33.905),   # Long Beach (Iskele / Trikomo shore)
    (35.200, 33.901),   # ~ (below the Kolympos woods)
    (35.180, 33.907),   # Salamis (Kampanopetra basilica, shore)
    (35.157, 33.922),   # Karakol Burnu, past the Pedieos and Gialias mouths
    (35.128, 33.946),   # Famagusta (Othello Castle, harbour)
    (35.117, 33.958),   # Glossa point
    (35.100, 33.963),   # Varosha (Chrysi Akti)
    (35.051, 34.012),   # Kapparis (shore)
    (35.036, 34.039),   # Protaras (Kalamies)
    (35.013, 34.0595),  # Fig Tree Bay
    (34.984, 34.072),   # Konnos Bay
    (34.956, 34.087),   # Cape Greco (tip, just past the lighthouse)
    # South coast: Ayia Napa, Larnaca Bay
    (34.958, 34.074),   # ~ (below the Cape Greco radio masts)
    (34.9595, 34.0655), # ~ (below Gkreko hill)
    (34.968, 34.055),   # Cape Greco sea caves
    (34.982, 34.004),   # Ayia Napa (harbour)
    (34.988, 33.969),   # Nissi Beach
    (34.980, 33.953),   # Makronissos (tombs)
    (34.976, 33.930),   # ~ (Ayia Thekla)
    (34.964, 33.895),   # ~ (Potamos Liopetriou)
    (34.943, 33.857),   # Cape Pyla
    (34.962, 33.833),   # ~ (below Xylofagou)
    (34.979, 33.797),   # ~
    (34.985, 33.770),   # Ormideia (shore)
    (34.983, 33.735),   # Dhekelia
    (34.971, 33.700),   # ~
    (34.956, 33.668),   # Oroklini (shore below the lake)
    (34.926, 33.646),   # Larnaca (port)
    (34.911, 33.640),   # Larnaca (Kition; castle on the seafront)
    (34.865, 33.638),   # Dades Point (Larnaca airport), past Mackenzie
    (34.840, 33.622),   # ~
    (34.816, 33.602),   # Cape Kiti
    # Cape Kiti to Limassol
    (34.809, 33.575),   # ~ (below Perivolia)
    (34.795, 33.535),   # ~
    (34.777, 33.496),   # Cape Petounta (below Mazotos)
    (34.763, 33.452),   # ~
    (34.750, 33.412),   # Pentaschoinos river mouth (below Alaminos)
    (34.731, 33.368),   # Agios Minas stream mouth (below Maroni)
    (34.729, 33.339),   # Zygi
    (34.708, 33.272),   # Cape Dolos (Governor's Beach), past Vasilikos
    (34.707, 33.196),   # Argaki tis Monis (mouth), past White Rocks
    (34.711, 33.143),   # Amathus
    (34.697, 33.097),   # Germasogeia (beach)
    (34.676, 33.051),   # Limassol (Molos seafront)
    (34.662, 33.027),   # Garyllis river mouth (Limassol), past the old port
    # Akrotiri peninsula
    (34.633, 33.008),   # Lady's Mile, past the Port of Limassol
    (34.600, 33.016),   # ~
    (34.566, 33.030),   # Cape Gata
    (34.5633, 33.024),  # Cape Gata lighthouse (shore)
    (34.571, 32.991),   # Aetokremnos
    (34.569, 32.964),   # Kavos Ayios Syllas (Dreamer's Bay)
    (34.567, 32.934),   # Cape Zevgari
    (34.605, 32.920),   # ~ (west of Akrotiri village)
    (34.646, 32.899),   # Kouris river mouth
    (34.660, 32.885),   # Kourion (below the acropolis)
    (34.666, 32.872),   # Kourion Beach
    # Episkopi Bay to Paphos
    (34.664, 32.816),   # Symvoulos (stream mouth, Episkopi Bay)
    (34.658, 32.762),   # Evdhimou river mouth (Avdimou Beach)
    (34.656, 32.728),   # Pissouri Bay (shore)
    (34.641, 32.716),   # Cape Aspro
    (34.651, 32.680),   # Argaki tis Chchyllas (mouth)
    (34.664, 32.628),   # Petra tou Romiou
    (34.683, 32.589),   # Chapotami (mouth)
    (34.695, 32.561),   # Diarizos river mouth (below Kouklia / Palaepaphos)
    (34.703, 32.494),   # Zephyrion (Paphos airport)
    (34.729, 32.457),   # Ezousa river mouth (below Geroskipou)
    (34.749, 32.423),   # Vrysoudia Beach (Paphos)
    (34.753, 32.410),   # Nea Paphos (harbour and castle)
    (34.756, 32.400),   # Paphos Point
    # West coast, Paphos to the Akamas
    (34.785, 32.401),   # Koskinas (stream mouth), past the Tombs of the Kings
    (34.831, 32.391),   # Apis (stream mouth, Blue Coral Beach, Kissonerga)
    (34.853, 32.363),   # Maa-Palaiokastro (Coral Bay)
    (34.877, 32.336),   # Argaki tis Michainas (mouth)
    (34.900, 32.316),   # Cape Drepanum (Agios Georgios), inshore of Yeronisos
    (34.912, 32.326),   # White River (Aspros Potamos) mouth
    (34.921, 32.326),   # Toxeftra Beach (Avagas gorge mouth)
    (34.951, 32.304),   # Lara Point
    (34.991, 32.311),   # Argaki tous Kalogyrous (mouth)
    (35.018, 32.290),   # Cape Geranissos
    (35.041, 32.278),   # Argaki tou Kountourokampo (mouth), past Koppos islet
    (35.070, 32.269),   # Argaki tou Plakio (mouth)
    (35.094, 32.276),   # Argaki tis Farkonias (mouth)
]

# Acts 13:6 "gone through the island to Paphos": Salamis -> Kition ->
# Amathus -> Kourion -> Paphos, kept a few km inland of the south coast
# except at the coastal cities themselves. Waypoints are named villages.
CYPRUS_ROAD = [
    (35.185, 33.900),   # Salamis
    (35.055, 33.785),   # Achna
    (35.014, 33.692),   # Pyla
    (34.923, 33.630),   # Kition (Larnaca)
    (34.849, 33.575),   # Kiti
    (34.758, 33.357),   # Maroni
    (34.738, 33.242),   # Pentakomo
    (34.712, 33.142),   # Amathus
    (34.671, 32.934),   # Kolossi
    (34.664, 32.888),   # Kourion
    (34.694, 32.763),   # Avdimou
    (34.710, 32.573),   # Kouklia (Palaepaphos)
    (34.757, 32.449),   # Geroskipou
    (34.757, 32.405),   # Nea Paphos
]

# Relief labels (optional).
TROODOS = (34.937, 32.864)   # Mount Olympos (Chionistra), Troodos summit, 1952 m

KYRENIA_RANGE = [   # crest centreline, west to east
    (35.330, 33.129),   # Mount Kornos
    (35.319, 33.162),   # Mount Selvili (Kyparissovouno), 1024 m
    (35.312, 33.281),   # Saint Hilarion Castle
    (35.288, 33.410),   # Buffavento Castle
    (35.288, 33.472),   # Pentadaktylos
    (35.323, 33.627),   # Zygovounos
    (35.368, 33.797),   # Kefales
    (35.406, 33.923),   # Kantara Castle
]


# ===========================================================================
# Inland: lakes, crest lines, sites, roads
# ===========================================================================

# ---------------------------------------------------------------------------
# LAKES
# ---------------------------------------------------------------------------

# Lake Egirdir (916 m), with its northern Hoyran part: a "peanut" pinched at
# the Kemer strait. Clockwise from the west bank of the strait round the
# Hoyran part, then the Egirdir part's east shore south to the Kovada outlet
# and its west shore north past Egirdir and Barla. Yalvac (Pisidian Antioch)
# lies 28 km east of the north end.
EGIRDIR = [
    (38.143, 30.837),   # ~ Kemer strait (Kemer Bogazi), west bank
    (38.152, 30.822),   # ~
    (38.160, 30.806),   # Akkecili (shore north-east of the village)
    (38.172, 30.785),   # ~
    (38.188, 30.765),   # ~
    (38.206, 30.751),   # ~
    (38.222, 30.746),   # Gencali (shore 1.5 km north of the village, by the Via Sebaste milestone)
    (38.235, 30.770),   # ~
    (38.250, 30.795),   # ~
    (38.263, 30.815),   # Tasevi (shore below the village)
    (38.274, 30.840),   # ~ (Asagikasikara to the north)
    (38.281, 30.865),   # Hoyran (the marsh at the north end, Hoyran Golu)
    (38.273, 30.880),   # ~
    (38.261, 30.884),   # Gaziri / Limnae (shore west of the village)
    (38.243, 30.878),   # ~
    (38.222, 30.871),   # Hoyran rock tombs (cliffs on the east shore)
    (38.200, 30.867),   # ~ below Kirisli Dagi
    (38.178, 30.862),   # ~ (Akdag village on the hill to the east)
    (38.160, 30.857),   # ~
    (38.147, 30.855),   # ~ Kemer strait, east bank
    (38.135, 30.866),   # ~
    (38.128, 30.888),   # ~ below Catal Tepe
    (38.123, 30.912),   # ~
    (38.116, 30.932),   # Yenice (shore south-west of the village)
    (38.101, 30.947),   # Yalvac Brook (Akcay) mouth, approximate
    (38.075, 30.953),   # ~ (Gelendost 7 km north-east)
    (38.047, 30.950),   # Iskele Hoyuk
    (38.030, 30.955),   # Hacilar (shore)
    (38.010, 30.959),   # ~ (Esinyurt inland)
    (37.993, 30.961),   # Ertokus Han (shore west of the caravanserai)
    (37.968, 30.951),   # ~
    (37.947, 30.938),   # ~
    (37.930, 30.927),   # Mahmatlar (shore)
    (37.909, 30.920),   # ~
    (37.889, 30.915),   # Sorkuncak (shore)
    (37.870, 30.901),   # ~
    (37.856, 30.888),   # Goktas (shore west of the village)
    (37.846, 30.874),   # ~ southern tip, head of the Kovada canal
    (37.856, 30.864),   # ~
    (37.870, 30.860),   # ~ east side of the Egirdir promontory
    (37.8835, 30.8695), # Yesil Ada (Nis island), off the tip of the promontory
    (37.8775, 30.852),  # Egirdir castle (west side of the promontory)
    (37.878, 30.838),   # ~
    (37.878, 30.823),   # Egirdir railway station (shore)
    (37.890, 30.816),   # Egirdir Hoyuk
    (37.920, 30.809),   # ~
    (37.955, 30.803),   # ~
    (37.985, 30.800),   # ~
    (38.012, 30.800),   # Barla (shore east of the village)
    (38.045, 30.803),   # ~
    (38.078, 30.809),   # ~
    (38.108, 30.817),   # ~
    (38.130, 30.827),   # ~
]

# Lake Beysehir (1,123 m), the largest freshwater lake in Turkey: steep
# western shore under the Anamas range, low eastern shore, about 33 islands
# (Mada, Haciakif, Orta, Aygir, Igdeli, Kizkalesi, Akburun, Kulbent,
# Yilanli). Clockwise from Karci Burnu at the north-west corner. The outlet
# (Carsamba Cayi) leaves at Beysehir town in the south-east and runs to Sugla.
BEYSEHIR = [
    (37.9475, 31.3847), # Karci Burnu (cape at the north-west end)
    (37.937, 31.414),   # ~
    (37.925, 31.442),   # ~
    (37.914, 31.468),   # ~ (Neapolis / Kiyakdede and Fele on the plain to the north)
    (37.912, 31.4955),  # Tolca (lakeside village)
    (37.918, 31.515),   # ~
    (37.921, 31.536),   # Kireli (lakeside town)
    (37.908, 31.556),   # ~ (Huyuk 4 km north-east)
    (37.890, 31.567),   # Cukurkent (shore)
    (37.866, 31.565),   # Budak (shore)
    (37.850, 31.574),   # ~
    (37.833, 31.578),   # Kusluca (shore)
    (37.810, 31.583),   # ~
    (37.790, 31.585),   # ~
    (37.776, 31.592),   # ~ Akburun point (Akburun Island lies off it)
    (37.7785, 31.607),  # Akburun (lakeside village; shore just south of it)
    (37.788, 31.630),   # ~
    (37.781, 31.655),   # ~ head of the bay with Kulbent Island
    (37.763, 31.672),   # Erbaba mound (shore west of the mound)
    (37.746, 31.666),   # Golkasi
    (37.730, 31.684),   # Ciftlik (shore)
    (37.712, 31.700),   # ~
    (37.695, 31.714),   # ~
    (37.6807, 31.7228), # Beysehir: Taskopru regulator at the outlet
    (37.668, 31.708),   # ~
    (37.655, 31.683),   # ~
    (37.641, 31.652),   # Karadiken (shore)
    (37.626, 31.630),   # ~
    (37.605, 31.606),   # ~
    (37.584, 31.584),   # Ustunler (lakeside village)
    (37.568, 31.556),   # ~
    (37.556, 31.526),   # ~
    (37.550, 31.497),   # ~
    (37.548, 31.474),   # Yesildag (lakeside village, landing for Haciakif Island)
    (37.565, 31.459),   # ~
    (37.592, 31.452),   # ~
    (37.622, 31.441),   # ~
    (37.655, 31.429),   # ~
    (37.690, 31.416),   # Kurucuova (shore)
    (37.707, 31.428),   # Golkonak (lakeside village)
    (37.718, 31.445),   # Golyaka (lakeside village)
    (37.7435, 31.4405), # Kubadabad Palace (west shore, just lakeward of the palace)
    (37.768, 31.426),   # ~
    (37.795, 31.411),   # ~
    (37.822, 31.396),   # ~ (Igdeli Island offshore)
    (37.848, 31.376),   # ~
    (37.870, 31.357),   # ~
    (37.893, 31.337),   # Gedikli (lakeside village; Mada Island just offshore)
    (37.915, 31.354),   # ~
    (37.935, 31.371),   # ~
]

# Lake Burdur (845 m): a tectonic trough lake running WSW-ENE, its north-west
# side a steep fault scarp, Burdur town close to its south-east shore near
# the north-east end. Clockwise from the south-west tip.
BURDUR = [
    (37.706, 29.990),   # ~ south-west end of the lake
    (37.714, 30.002),   # Kavacik (shore)
    (37.719, 30.030),   # Cimbilli (shore)
    (37.723, 30.062),   # ~
    (37.729, 30.095),   # ~
    (37.733, 30.117),   # Kapu Burnu (cape on the north-west shore)
    (37.750, 30.130),   # ~
    (37.770, 30.143),   # Ilyas (shore south-east of the village)
    (37.784, 30.172),   # ~
    (37.793, 30.200),   # Ardicli (shore)
    (37.800, 30.230),   # ~
    (37.804, 30.260),   # Kuyucak / Senir (shore)
    (37.800, 30.288),   # ~ north-east end
    (37.784, 30.302),   # ~
    (37.763, 30.300),   # ~ (Askeriye inland to the east)
    (37.742, 30.284),   # Burdur (shore north-west of the town)
    (37.725, 30.258),   # ~
    (37.710, 30.230),   # ~
    (37.697, 30.200),   # ~
    (37.678, 30.175),   # Cendik / Suludere (shore)
    (37.668, 30.135),   # Bayindir Brook mouth
    (37.658, 30.100),   # Eren and Boz brook mouths
    (37.667, 30.087),   # ~
    (37.683, 30.083),   # Karakent Burnu (cape)
    (37.699, 30.066),   # Lysinia / Karakent (shore north of the village)
    (37.702, 30.040),   # ~
    (37.704, 30.012),   # ~ (Yaylabeli inland)
]

# Lake Aksehir (955-960 m), shallow and reedy, in the graben between the
# Sultan Daglari (south-west) and Emir Dagi (north-east); Aksehir town is
# 10 km south of it. Fed from Lake Eber by the Taskopru channel at its
# north-west end. Clockwise from the channel's mouth.
AKSEHIR = [
    (38.560, 31.305),   # ~ mouth of the Eber channel (Taskopru lies 2 km west)
    (38.582, 31.330),   # ~
    (38.598, 31.360),   # Karayatak plain (south edge)
    (38.607, 31.392),   # ~
    (38.613, 31.425),   # Uckuyu (shore south of the village)
    (38.605, 31.460),   # ~ (Ala Dag to the north)
    (38.590, 31.495),   # ~
    (38.572, 31.528),   # ~
    (38.553, 31.556),   # Karacaovasi (west edge of the plain)
    (38.528, 31.569),   # Pazarkaya (shore)
    (38.505, 31.562),   # ~
    (38.485, 31.545),   # ~
    (38.468, 31.515),   # Ortakoy / Tipikoy (shore)
    (38.460, 31.495),   # Adiyan Brook mouth
    (38.452, 31.470),   # Engili Creek mouth, approximate
    (38.447, 31.440),   # ~
    (38.446, 31.410),   # Sorkun (shore north of the village and its springs)
    (38.452, 31.378),   # ~
    (38.460, 31.350),   # ~
    (38.468, 31.328),   # Golcayir
    (38.490, 31.312),   # ~
    (38.515, 31.302),   # ~
    (38.540, 31.300),   # ~
]

# Lake Eber (967 m), largely reed-bed, between Bolvadin (north-west), Cay
# (south-west) and the Karabag villages (north-east). The Akarcay enters
# from the west; the outflow leaves the east end for Lake Aksehir.
EBER = [
    (38.647, 31.093),   # Akarcay River mouth
    (38.665, 31.097),   # Akar Brook mouth
    (38.682, 31.110),   # ~ (Bolvadin 5 km north-west)
    (38.695, 31.130),   # ~ (Dipevler inland to the north)
    (38.701, 31.158),   # ~
    (38.700, 31.185),   # Derekarabag (shore)
    (38.692, 31.212),   # ~
    (38.681, 31.234),   # Ortakarabag (shore)
    (38.667, 31.252),   # ~
    (38.650, 31.264),   # ~ east end, outflow towards Taskopru and Lake Aksehir
    (38.633, 31.260),   # ~ (Sarimsakli Hoyuk inland to the east)
    (38.620, 31.240),   # ~
    (38.613, 31.215),   # Yavsan plain (north edge)
    (38.612, 31.190),   # ~
    (38.617, 31.162),   # Kocaoguz Hoyugu (shore)
    (38.614, 31.140),   # ~
    (38.611, 31.125),   # Eber (village, shore)
    (38.617, 31.110),   # ~
    (38.630, 31.098),   # ~
    (38.640, 31.094),   # ~
]

# Lake Sugla (Karaviran), seasonal, in the polje south-east of Seydisehir,
# fed by the Carsamba Cayi from Lake Beysehir. Drawn at a wet-season extent.
SUGLA = [
    (37.392, 31.985),   # Bagra Hoyuk, where the Carsamba Cayi (Beysehir Brook) comes in
    (37.398, 32.008),   # Kumluca (shore south of the village)
    (37.390, 32.035),   # ~
    (37.377, 32.058),   # ~
    (37.366, 32.075),   # Asagikaraoren (shore)
    (37.351, 32.086),   # ~ (Ortakaraviran Hoyuk)
    (37.336, 32.092),   # Yahyali Hoyuk (shore)
    (37.320, 32.091),   # ~ (Saraykoy inland to the east)
    (37.304, 32.080),   # Yalihuyuk (shore)
    (37.292, 32.060),   # ~
    (37.286, 32.035),   # ~ (Homana and Catmakaya to the south)
    (37.289, 32.008),   # ~
    (37.297, 31.982),   # ~ (Kizil Dag to the south)
    (37.306, 31.958),   # Susuz (shore)
    (37.322, 31.941),   # ~
    (37.343, 31.932),   # Golyuzu (shore)
    (37.362, 31.941),   # ~
    (37.377, 31.958),   # ~
    (37.386, 31.972),   # ~
]

# Lake Tuz (905 m), the great salt lake, drawn whole: broad in the south,
# narrowing north to its tip beyond Sereflikochisar. Seasonally flooded salt
# steppe lies to the south and south-west. Clockwise from the south end.
TUZ = [
    (38.515, 33.420),   # ~ south end (Eskil 13 km south)
    (38.517, 33.350),   # ~
    (38.531, 33.290),   # ~ (Tosun Hoyuk to the south-west)
    (38.543, 33.240),   # ~
    (38.560, 33.205),   # Golyazi (shore)
    (38.605, 33.170),   # ~
    (38.655, 33.143),   # ~ (Cihanbeyli 18 km west)
    (38.710, 33.124),   # ~
    (38.760, 33.118),   # Yavsan Tuzlasi (salt works on the west shore)
    (38.815, 33.138),   # ~
    (38.870, 33.170),   # ~
    (38.920, 33.203),   # ~
    (38.952, 33.225),   # Tuzyaka (shore)
    (38.985, 33.285),   # ~ (Bozan inland)
    (39.020, 33.342),   # ~
    (39.052, 33.398),   # ~ north end
    (39.045, 33.442),   # ~
    (39.015, 33.476),   # ~ (Vayvay)
    (38.975, 33.502),   # ~
    (38.938, 33.516),   # Sereflikochisar (shore west of the town)
    (38.900, 33.487),   # ~
    (38.870, 33.448),   # Hamzali / Cavuskoy (shore)
    (38.850, 33.417),   # Kara Burun (cape)
    (38.836, 33.455),   # ~ (Hacisunni spring)
    (38.832, 33.510),   # Karamollausagi (shore)
    (38.815, 33.552),   # ~ (Sadagolthina)
    (38.798, 33.597),   # Menzil Hani (shore west of the caravanserai)
    (38.755, 33.620),   # ~
    (38.700, 33.633),   # ~
    (38.645, 33.638),   # ~
    (38.600, 33.628),   # ~ (the Melendiz comes in from the south-east)
    (38.575, 33.590),   # ~
    (38.548, 33.548),   # ~
    (38.530, 33.500),   # ~
    (38.519, 33.460),   # ~
]

ANATOLIA_LAKES = {
    "egirdir": EGIRDIR,
    "beysehir": BEYSEHIR,
    "burdur": BURDUR,
    "aksehir": AKSEHIR,
    "eber": EBER,
    "sugla": SUGLA,
    "tuz": TUZ,
}

# ---------------------------------------------------------------------------
# RELIEF: crest lines for rows of peaks and range labels, each through named
# summits and passes (coordinates from Wikidata).
# ---------------------------------------------------------------------------

# The Western Taurus between Lake Egirdir and the Gulf of Antalya, west to
# east across the Pisidian highlands, ending where the Central Taurus begins.
TAURUS_WEST = [
    (37.4676, 30.3245), # Katrancik Daglari
    (37.5258, 30.4433), # Koru Dagi
    (37.5458, 30.6508), # Alakeci Dagi
    (37.5340, 30.8183), # Karakeris Tepesi
    (37.548, 30.960),   # ~ (Adada lies in the range here)
    (37.5500, 31.1000), # Kuyucak Dagi
    (37.4833, 31.2167), # Kordikmen Dagi
    (37.4086, 31.3127), # Dumanli Dag
    (37.3333, 31.3892), # Kel Dag
]

# The Central Taurus: Geyik Daglari and the watershed north of Alanya and
# Anamur, east to the Sertavul pass on the Karaman-Mut road.
TAURUS_CENTRAL = [
    (37.2667, 31.5000), # Seytan Daglari
    (37.2709, 31.6430), # Kizildag
    (37.2628, 31.7131), # Karadag
    (37.2303, 31.7781), # Teke Pass
    (37.1608, 31.7983), # Cakilgedik Pass
    (37.1000, 31.8900), # Yarpuz Dagi
    (37.1058, 31.9778), # Geyik Daglari
    (37.0567, 32.1850), # Haydar Dagi
    (37.0311, 32.2547), # Demirli Dagi
    (37.0100, 32.4292), # Akdag (by Hadim)
    (36.9639, 32.4858), # Ibrim Dag
    (36.9644, 32.6844), # Kartal Dagi
    (36.9825, 32.8628), # Ulu Tepe
    (36.9927, 32.9757), # Cedik Dag
    (36.9800, 33.1137), # Kemer Dagi
    (36.9142, 33.2661), # Sertavul Pass
]

# The Bolkar Daglari north of Mersin, west-south-west to east-north-east up
# to Medetsiz (3,524 m), then down to the Cilician Gates.
BOLKAR = [
    (37.1333, 33.9833), # Cavdar Dagi
    (37.1744, 34.0425), # Bolkar Dagi
    (37.2367, 34.2400), # Kirkpinar Dagi
    (37.2480, 34.3643), # Bolkar Daglari (range centre)
    (37.3258, 34.4698), # Kekrecik Dagi
    (37.3917, 34.5392), # Bolgar Dagi
    (37.3931, 34.6309), # Medetsiz (summit)
    (37.3567, 34.7442), # Elmali Dag
    (37.2853, 34.7861), # Cilician Gates (Gulek Bogazi)
]

# The Sultan Daglari: a ridge running north-west to south-east with Pisidian
# Antioch (Yalvac) at its south-west foot and Philomelium (Aksehir) at its
# north-east foot.
SULTAN = [
    (38.5048, 31.0981), # Gelincikana Tepe
    (38.4236, 31.2398), # Hacialabaz Dagi
    (38.345, 31.295),   # ~
    (38.2692, 31.3483), # Kizil Tepe
    (38.2500, 31.3833), # Engilibel Pass
    (38.220, 31.445),   # ~
    (38.1907, 31.4988), # Akpinar Dagi
    (38.1692, 31.5183), # Boztepeler
    (38.0992, 31.5808), # Kale Dagi
]

RELIEF = {
    "TAURUS_WEST": TAURUS_WEST,
    "TAURUS_CENTRAL": TAURUS_CENTRAL,
    "BOLKAR": BOLKAR,
    "SULTAN": SULTAN,
}

# ---------------------------------------------------------------------------
# SITES: name -> (lat, lon), each with its source. Keys match the CITIES of
# generate_acts1314_svg.py where they exist.
# ---------------------------------------------------------------------------

SITES = {
    "antioch": (36.2025, 36.1606),         # Antioch on the Orontes: Antakya, Wikipedia
    "seleucia": (36.1239, 35.9219),        # Seleucia Pieria, Wikipedia
    "salamis": (35.1833, 33.9000),         # Salamis, Cyprus, Wikipedia
    "kition": (34.9233, 33.6305),          # Kition (Larnaca), Wikipedia
    "amathus": (34.7125, 33.1417),         # Amathus, Wikipedia
    "kourion": (34.6642, 32.8877),         # Kourion, Wikipedia
    "paphos": (34.7600, 32.4070),          # Nea Paphos (ancient city), Wikipedia
    "perga": (36.9614, 30.8539),           # Perga, Wikipedia
    "attalia": (36.8844, 30.7022),         # Attalia: Antalya old harbour (Kaleici), Wikidata
    "aspendos": (36.9389, 31.1722),        # Aspendos, Wikipedia
    "side": (36.7667, 31.3889),            # Side, Wikipedia
    "pantioch": (38.3061, 31.1892),        # Pisidian Antioch, 1 km north-east of Yalvac, Wikipedia
    "iconium": (37.8744, 32.4931),         # Iconium: Konya (Alaeddin hill), Wikipedia
    "lystra": (37.6019, 32.3383),          # Lystra: Zoldera mound, 1.5 km north-west of Hatunsaray, Wikipedia
    "derbe": (37.3493, 33.3617),           # Derbe: Kerti Hoyuk (Ballance 1956), Wikipedia;
                                           # alternative Devri Sehri (Ballance 1964), about
                                           # 4 km south-east, near (37.324, 33.394)
    "tarsus": (36.9165, 34.8951),          # Tarsus, Wikipedia
    "cilician_gates": (37.2853, 34.7861),  # Cilician Gates (Gulek Bogazi), Wikipedia
    "jerusalem": (31.7767, 35.2342),       # Jerusalem: Old City, Wikipedia
}

# ---------------------------------------------------------------------------
# ROADS: likely first-century routes as waypoints, each a named ancient or
# modern place (coordinates from Wikipedia / Wikidata / vici.org). Each road
# runs between two SITES; the generator swaps its end points for the cities.
# ---------------------------------------------------------------------------

# Perga to Pisidian Antioch by the Via Sebaste. Chosen over the shorter
# Cestrus (Aksu) valley path by Adada because the Via Sebaste was the made
# Roman road between exactly these two places: Augustus built it in 6 BC
# from Antioch, its caput viae, through the Climax pass (Doseme Bogazi) down
# to Perga, with a mansio in the pass and milestones along it, linking the
# colonies at Antioch, Apollonia and Comama. The Adada path (Ramsay's
# proposal) has no attested first-century road. The line follows David
# French's survey: up the Doseme pass to Comama, north past the Augustan
# milestone at Yarikoy, round the west end of Lake Burdur (the usual
# reconstruction; a recent proposal takes it along the south-east shore
# through Burdur instead), through Keciborlu to Apollonia and Tymandos, then
# along the north shore of Lake Egirdir, where milestones at Gencali give 28
# miles to Antioch. Cremna lay on a branch off it.
PERGA_ANTIOCH = [
    (36.9614, 30.8539), # Perga
    (36.9981, 30.7250), # Lyrboton Kome (Roman village north of Attalia)
    (37.1756, 30.5998), # Doseme Bogazi mansio (the Climax pass)
    (37.2024, 30.5666), # Via Sebaste paving at the head of the pass
    (37.1923, 30.5045), # Dagbeli
    (37.3196, 30.3344), # Comama (Seref Hoyuk, near Urkutlu), vici.org
    (37.3750, 30.3217), # Cretopolis
    (37.5053, 30.1194), # Kormasa
    (37.6219, 30.0619), # Yarikoy (Augustan Via Sebaste milestone)
    (37.6981, 29.9456), # Cardak
    (37.7603, 29.9942), # Ulupinar
    (37.7861, 30.1181), # Ilyas
    (37.9528, 30.2917), # Keciborlu
    (38.0706, 30.4732), # Apollonia (Sozopolis), Uluborlu
    (38.1040, 30.6070), # Tymandos
    (38.2225, 30.7420), # Gencali milestones, by the lake shore
    (38.2758, 30.8233), # Tasevi
    (38.2989, 30.8439), # Asagikasikara (round the north edge of the Hoyran marsh)
    (38.2922, 30.9592), # Gokceali
    (38.3061, 31.1892), # Pisidian Antioch
]

# The alternative, for reference: Ramsay's Cestrus valley path by Adada,
# round the south end of Lake Egirdir and up its east shore.
PERGA_ANTIOCH_ADADA = [
    (36.9614, 30.8539), # Perga
    (37.1642, 30.8253), # Kirbas
    (37.2911, 30.8108), # Kargi
    (37.4833, 30.9833), # Sutculer
    (37.5752, 30.9853), # Adada
    (37.6297, 30.8839), # Lake Kovada
    (37.6958, 30.8547), # Yukarigokdere
    (37.8550, 30.8992), # Goktas
    (37.8892, 30.9292), # Sorkuncak
    (37.9303, 30.9319), # Mahmatlar
    (37.9928, 30.9708), # Ertokus Han
    (38.0308, 30.9583), # Hacilar
    (38.1167, 31.0167), # Gelendost
    (38.1292, 31.1539), # Kecili
    (38.1886, 31.1614), # Bahtiyar
    (38.3061, 31.1892), # Pisidian Antioch
]

# Pisidian Antioch to Iconium by the Via Sebaste south of the Sultan
# Daglari: down the Anthius valley to Neapolis, past the north end of Lake
# Beysehir to Pappa Tiberiopolis and across the plain to Iconium. Chosen over
# the road north over the range to Philomelium because this was the Augustan
# road linking the colonies Antioch and Iconium (French traced the Via
# Sebaste from Yalvac to Konya), it is shorter and keeps to one valley, and
# Acts names no place between. The northern road (later the main Byzantine
# highway) is below. Some reconstructions run it further south by Misthia
# (near Beysehir); this line keeps north of the lake.
ANTIOCH_ICONIUM = [
    (38.3061, 31.1892), # Pisidian Antioch
    (38.1906, 31.2418), # Dortyol Hoyuk
    (38.1336, 31.2728), # Goksogut
    (38.0794, 31.3664), # Sarkikaraagac
    (38.0039, 31.4719), # Kireli caravanserai
    (37.9686, 31.4814), # Neapolis (Kiyakdede)
    (37.9539, 31.5975), # Huyuk
    (37.9184, 31.6734), # Imrenler
    (37.9344, 31.7347), # Camlica
    (37.9484, 31.8229), # Karaali
    (37.9042, 31.9234), # Pappa Tiberiopolis (Yunuslar)
    (37.8656, 32.1143), # Kiziloren
    (37.8926, 32.2794), # Degirmenkoy
    (37.8744, 32.4931), # Iconium
]

# The alternative, for reference: north over the Engilibel pass to
# Philomelium and east along the plateau road by Tyriaion and Laodicea.
ANTIOCH_ICONIUM_NORTH = [
    (38.3061, 31.1892), # Pisidian Antioch
    (38.2175, 31.2722), # Bagkonak
    (38.2500, 31.3833), # Engilibel Pass
    (38.3371, 31.3922), # Tekkekoy
    (38.3555, 31.4160), # Philomelium (Aksehir)
    (38.3461, 31.5144), # Karahuyuk
    (38.2915, 31.7108), # Argithani
    (38.2826, 31.9043), # Tyriaion (Ilgin)
    (38.2397, 32.2114), # Kadinhani
    (38.1922, 32.3740), # Laodicea Combusta (Ladik)
    (37.8744, 32.4931), # Iconium
]

# Iconium south-south-west to Lystra up the Meram valley, past the Hittite
# relief at Hatip.
ICONIUM_LYSTRA = [
    (37.8744, 32.4931), # Iconium
    (37.8046, 32.4236), # Kozagac
    (37.7659, 32.4065), # Hatip (Hittite relief)
    (37.7210, 32.4020), # Pamukcu
    (37.6755, 32.4136), # Bayat
    (37.6477, 32.3843), # Sarikiz
    (37.6298, 32.3715), # Karaagac
    (37.6019, 32.3383), # Lystra
]

# Lystra to Derbe: no Roman road is attested, so this keeps to the southern
# edge of the Konya plain, where the villages and water are, and passes south
# of the Karadag volcano (Binbirkilise) to Kerti Hoyuk.
LYSTRA_DERBE = [
    (37.6019, 32.3383), # Lystra
    (37.5599, 32.4498), # Kavak
    (37.4911, 32.5518), # Ahmediye
    (37.4232, 32.6350), # Doganli
    (37.3894, 32.7516), # Avdul
    (37.3655, 32.8491), # Erentepe
    (37.3708, 32.9092), # Sinci
    (37.3647, 33.0133), # Islihisar
    (37.3386, 33.0583), # Demiryurt
    (37.3275, 33.0992), # Eminler
    (37.3250, 33.1864), # Kilbasan
    (37.3222, 33.2417), # Hamidiye
    (37.3493, 33.3617), # Derbe (Kerti Hoyuk)
]

# Perga across the plain to Attalia's east gate and harbour.
PERGA_ATTALIA = [
    (36.9614, 30.8539), # Perga
    (36.9475, 30.8477), # Aksu
    (36.9003, 30.7928), # Antalya Airport
    (36.8853, 30.7083), # Hadrian's Gate (Attalia's east gate)
    (36.8844, 30.7022), # Attalia (old harbour)
]

ROADS = {
    "PERGA_ANTIOCH": PERGA_ANTIOCH,
    "ANTIOCH_ICONIUM": ANTIOCH_ICONIUM,
    "ICONIUM_LYSTRA": ICONIUM_LYSTRA,
    "LYSTRA_DERBE": LYSTRA_DERBE,
    "PERGA_ATTALIA": PERGA_ATTALIA,
}

# alternatives not drawn by default
ROADS_ALT = {
    "PERGA_ANTIOCH_ADADA": PERGA_ANTIOCH_ADADA,
    "ANTIOCH_ICONIUM_NORTH": ANTIOCH_ICONIUM_NORTH,
}


# --- The far world, for the widest shots: coarse, never labelled. Taken from
# the Acts 15-18 map (generate_acts1518_svg.MED, PELOPONNESE, ISLANDS).

# Epirus round Greece, the Dardanelles and Marmara, and down the Aegean
# shore of Asia Minor to Lycia, where MAIN_COAST takes over

AEGEAN_SHORE = [
    (39.10, 20.60), (38.95, 20.75), (38.85, 20.95), (38.60, 21.10),
    (38.35, 21.15), (38.42, 21.50), (38.48, 22.05), (38.52, 22.60),
    (38.30, 23.00), (38.10, 23.22), (38.05, 23.50), (37.96, 23.62),
    (37.90, 23.72), (37.75, 23.90), (37.65, 24.03), (37.90, 24.05),
    (38.10, 24.05), (38.30, 23.90), (38.45, 23.60), (38.60, 23.30),
    (38.80, 23.10), (39.00, 23.10), (39.20, 23.00), (39.35, 22.90),
    (39.25, 23.20), (39.20, 23.35), (39.45, 23.05), (39.60, 22.90),
    (39.90, 22.75), (40.10, 22.65), (40.30, 22.60), (40.45, 22.70),
    (40.55, 22.85), (40.65, 23.00), (40.50, 23.10), (40.30, 23.30),
    (40.10, 23.45), (40.30, 23.55), (40.20, 23.80), (40.35, 23.90),
    (40.15, 24.15), (40.40, 24.20), (40.60, 24.05), (40.80, 23.90),
    (40.85, 24.20), (40.90, 24.40), (40.85, 24.80), (40.90, 25.20),
    (40.85, 25.60), (40.80, 26.00), (40.60, 26.10), (40.40, 26.30),
    (40.30, 26.55), (40.40, 26.90), (40.60, 27.30), (40.75, 27.80),
    (40.85, 28.40), (40.98, 28.95), (40.80, 29.30), (40.77, 29.90),
    (40.72, 29.30), (40.45, 28.90), (40.38, 28.30), (40.35, 27.60),
    (40.40, 27.00), (40.25, 26.70), (40.10, 26.35), (40.00, 26.20),
    (39.80, 26.10), (39.60, 26.20), (39.50, 26.35), (39.30, 26.55),
    (39.10, 26.70), (38.95, 26.85), (38.80, 26.90), (38.65, 26.75),
    (38.45, 26.55), (38.35, 26.30), (38.40, 26.85), (38.42, 27.15),
    (38.30, 26.90), (38.20, 26.75), (38.05, 26.90), (37.95, 27.20),
    (37.85, 27.05), (37.70, 27.15), (37.55, 27.25), (37.40, 27.25),
    (37.20, 27.35), (37.05, 27.42), (36.95, 27.30), (36.80, 27.40),
    (36.70, 27.70), (36.72, 28.10), (36.80, 28.25), (36.75, 28.60),
    (36.70, 29.00),
]

# the African shore west of Egypt

LIBYA_SHORE = [
    (31.35, 27.24), (31.56, 25.15), (31.60, 23.50), (32.20, 22.80),
    (32.85, 22.30), (32.90, 21.80), (32.60, 21.20), (32.30, 20.60),
]

PELOPONNESE = [
    (38.05, 21.35), (38.05, 21.60), (38.08, 22.00), (38.02, 22.45),
    (37.96, 22.85), (37.99, 23.04), (37.86, 23.12), (37.75, 23.15),
    (37.60, 23.15), (37.35, 23.15), (37.10, 23.15), (36.80, 23.05),
    (36.43, 23.20), (36.75, 22.90), (36.60, 22.65), (36.40, 22.48),
    (36.63, 22.25), (36.80, 22.15), (36.75, 21.90), (37.05, 21.65),
    (37.30, 21.55), (37.60, 21.35), (37.85, 21.30),
]

FAR_ISLANDS = [
    [(35.25, 23.52), (35.42, 23.75), (35.50, 24.10), (35.40, 24.70), (35.35, 25.20), (35.42, 25.75), (35.30, 26.30), (35.05, 26.10), (34.92, 25.70), (34.98, 25.10), (35.00, 24.60), (35.15, 24.10), (35.10, 23.60)],  # CRETE
    [(38.15, 24.10), (38.45, 23.70), (38.70, 23.30), (38.95, 23.15), (39.05, 23.20), (38.85, 23.55), (38.60, 23.90), (38.35, 24.25), (38.15, 24.30)],  # EUBOEA
    [(39.38, 26.00), (39.42, 26.35), (39.28, 26.60), (39.05, 26.55), (38.98, 26.25), (39.15, 26.05)],  # LESBOS
    [(38.60, 25.95), (38.58, 26.15), (38.30, 26.20), (38.22, 26.00), (38.40, 25.90)],  # CHIOS
    [(37.80, 26.60), (37.82, 27.05), (37.70, 27.05), (37.68, 26.65)],  # SAMOS
    [(36.45, 28.20), (36.28, 28.25), (36.10, 27.95), (36.20, 27.70)],  # RHODES
    [(40.78, 24.60), (40.78, 24.78), (40.60, 24.78), (40.60, 24.60)],  # THASOS
    [(37.85, 24.90), (37.78, 25.05), (37.68, 24.92), (37.78, 24.80)],  # CYCLADES_1
    [(37.20, 25.55), (37.05, 25.60), (37.00, 25.40), (37.15, 25.38)],  # CYCLADES_2
    [(36.75, 24.45), (36.68, 24.60), (36.62, 24.42), (36.72, 24.35)],  # CYCLADES_3
]


# The Levant south of Ras Naqoura and the Egyptian shore, from the Numbers
# maps, so the mainland is one line from Epirus round to Libya.
from generate_tribal_maps import COAST as _LEVANT, COAST_WEST as _EGYPT  # noqa: E402
from generate_tribal_maps import (GULF_SUEZ, GULF_AQABA, RED_SEA,  # noqa: E402
                                  LAKES as _LV_LAKES, RIVERS as _LV_RIVERS,
                                  TRIBE_RINGS, TRIBE_COL, WEST_TRIBES,
                                  EAST_TRIBES)

MAINLAND = (AEGEAN_SHORE + MAIN_COAST
            + [p for p in reversed(_LEVANT) if p[0] < MAIN_COAST[-1][0] - 0.02]
            + list(reversed(_EGYPT))[:-1] + LIBYA_SHORE)
ISLANDS = [CYPRUS, PELOPONNESE] + FAR_ISLANDS
GULFS = [GULF_SUEZ, GULF_AQABA, RED_SEA]

# every lake and river the map draws
LAKES = dict(ANATOLIA_LAKES, dead_sea=_LV_LAKES[0], galilee=_LV_LAKES[1],
             huleh=_LV_LAKES[2])
RIVERS = {
    "orontes": ORONTES, "cestrus": CESTRUS, "eurymedon": EURYMEDON,
    "melas": MELAS, "calycadnus": CALYCADNUS, "cydnus": CYDNUS,
    "sarus": SARUS, "pyramus": PYRAMUS,
    "jordan_up": _LV_RIVERS[0], "jordan": _LV_RIVERS[1],
    "arnon": _LV_RIVERS[2], "jabbok": _LV_RIVERS[3],
    "yarmouk": _LV_RIVERS[4],
    # the Nile from Memphis to its two mouths
    "nile": [(29.85, 31.25), (30.02, 31.22), (30.15, 31.15)],
    "nile_rosetta": [(30.15, 31.15), (30.45, 30.95), (30.80, 30.75),
                     (31.15, 30.50), (31.45, 30.37)],
    "nile_damietta": [(30.15, 31.15), (30.50, 31.25), (30.85, 31.38),
                      (31.15, 31.55), (31.47, 31.80)],
}

# Antioch down the Orontes valley to its port (13:4, 14:26), along the
# river until it bends south for its mouth, then over to Seleucia
_i = min(range(len(ORONTES)), key=lambda k: (ORONTES[k][0] - SITES["antioch"][0]) ** 2
         + (ORONTES[k][1] - SITES["antioch"][1]) ** 2)
ROADS["ORONTES_ROAD"] = ([SITES["antioch"]]
                        + [q for q in ORONTES[_i + 1:]
                           if q[0] > SITES["seleucia"][0] + 0.02]
                        + [SITES["seleucia"]])
ROADS["CYPRUS_ROAD"] = CYPRUS_ROAD


# --- The sermon's places (Acts 13:17-26). Patriarchs, Egypt and the
# wilderness follow the traditional southern-Sinai route; the judges' towns
# are one each for Othniel (Debir), Ehud (Gilgal), Deborah (the palm between
# Ramah and Bethel), Gideon (Ophrah), Jephthah (Mizpah of Gilead) and Samson
# (Zorah). Schematic, as every atlas's is.
SERMON_SITES = {
    "hebron": (31.53, 35.10), "beersheba": (31.24, 34.80),
    "goshen": (30.80, 31.83), "succoth": (30.55, 32.10),
    "crossing": (30.05, 32.55), "far_shore": (29.95, 32.72),
    "marah": (29.60, 32.85), "elim": (29.25, 33.05), "sin": (28.95, 33.25),
    "sinai": (28.54, 33.97), "hazeroth": (28.95, 34.40),
    "kadesh": (30.69, 34.49), "ezion_geber": (29.55, 34.97),
    "arnon": (31.45, 35.85), "moab": (31.80, 35.65),
    "gilgal": (31.86, 35.48),
    "debir": (31.43, 34.97), "palm": (31.90, 35.22),
    "ophrah": (32.55, 35.30), "mizpah_gilead": (32.20, 35.75),
    "zorah": (31.77, 34.98),
    "ramathaim": (32.05, 35.02), "gibeah": (31.823, 35.233),
    "bethlehem": (31.705, 35.205), "bethany_jordan": (31.837, 35.55),
    "aenon": (32.40, 35.55),
    "caesarea": (32.50, 34.89), "tyre": (33.27, 35.20),
    "sidon": (33.56, 35.37),
}
EDOM_WAY = [(30.25, 35.15), (30.50, 35.65), (31.10, 35.85)]
TOWERS = [(31.55, 35.05), (31.75, 35.00), (31.95, 35.20), (32.20, 35.25),
          (32.50, 35.20), (32.75, 35.35), (33.00, 35.40)]
JUDGES = ["debir", "gilgal", "palm", "ophrah", "mizpah_gilead", "zorah"]


def _via(*keys):
    return [SERMON_SITES[k] if isinstance(k, str) else k for k in keys]


# Israel's story as routes, each traced on its own verse
STORY = {
    "going_down": _via("hebron", "beersheba", (30.95, 33.20),
                       (30.85, 32.40), "goshen"),
    "exodus": _via("goshen", "succoth", "crossing", "far_shore"),
    "wilderness": _via("far_shore", "marah", "elim", "sin", "sinai",
                       "hazeroth", (29.60, 34.62), "ezion_geber",
                       (30.10, 34.70), "kadesh", (30.40, 34.95),
                       *EDOM_WAY, "arnon", "moab"),
    "crossing": _via("moab", "gilgal"),
    "john_course": _via("bethany_jordan", (31.95, 35.53), (32.10, 35.54),
                        (32.25, 35.54), "aenon"),
    "word": _via((31.778, 35.235), (32.10, 35.00), "caesarea",
                 (32.95, 35.15), "tyre", "sidon", (34.10, 35.75),
                 (34.80, 36.05), (35.50, 36.05), (36.202, 36.160)),
}


# Antioch of Pisidia's territory (13:50 "out of their borders"): an uneven
# ring about 0.55 x 0.75 degrees round the city, its west edge by Lake
# Egirdir, its east edge on the Sultan Daglari. Schematic.
ANTIOCH_TERRITORY = [
    (38.3, 31.62), (38.409, 31.58), (38.488, 31.475), (38.544, 31.352),
    (38.554, 31.21), (38.544, 31.068), (38.509, 30.915), (38.409, 30.84),
    (38.3, 30.86), (38.202, 30.878), (38.106, 30.937), (38.045, 31.061),
    (38.014, 31.21), (38.045, 31.359), (38.128, 31.453), (38.202, 31.542),
]
