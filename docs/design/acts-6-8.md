# Acts 6:8–8:3: Stephen

Stephen's speech as one camera tour over the lands of Israel's story, with
a scene card of Jerusalem the camera dives into, built the way Acts 13–14 is
([acts-13-14.md](acts-13-14.md)).

## Status: first cut built (2026-11-05), the bush card added (2026-11-06), not deployed

All 71 verses are drawn and narrated, the bush at Mount Sinai (7:31–34) in
its own card. Nothing has been seen on a device, and the owner has not yet
reviewed the tour or the bush card.

| What | Where |
|---|---|
| The tour: shots, plates, titles, Israel's roads, the people on the map, the throne marks, the tally, Moses' years | `generate_acts7_svg.py` (`STAGE`, `ROADS`, `PINS`, `MARKS`, `TALLY`, `BAR_FILL`, `beats`) |
| The map beyond the Levant: the Nile, the Red Sea and Sinai, Mesopotamia's rivers, the Persian Gulf, the speech's places | `near_east.py` (tested by `test_near_east.py`) |
| The rest of the land and sea | `mediterranean.py`, `acts_geography.py` (southern Asia Minor, Cyprus, the Anatolian lakes and rivers), `gazetteer.py` (the Levant) |
| The Jerusalem card (6:8–7:1, 7:52–8:3) | `acts7_council.py` |
| The bush card (7:31–34) | `acts7_bush.py` |
| God's presence; Solomon's house; the bush and its flame; sandals | `svg_figures.prepared_throne`, `svg_figures.temple_house`, `svg_figures.bush` and `bush_flames`, `svg_figures.sandals` |
| The camera, labels, HUD and QC; the cards | `svg_map_camera.py`, `svg_scene_card.py` (which gained effects drawn under the cast, `Card.effect(under=True)`, for the throne's glow) |

## The idea

The charge at 6:13 is that Stephen speaks "against this holy place". His
answer is a tour of every place God met his people outside it: Mesopotamia
and Haran, Egypt with Joseph, Midian and Sinai, the wilderness with the
tent. The house at Jerusalem comes last and smallest (7:47–50). So the map
carries the argument, not only the story. Two devices run through it:

- **Where God appears.** A gold throne mark (the prepared throne at map
  size) comes in at Ur (7:2), in Egypt beside Joseph ("God was with him",
  7:9) and at Sinai (7:30), and stays. At 7:48 the camera rises over the
  whole speech, the marks ring, and the house at Jerusalem shrinks to a
  small one by its dot. At 7:49 the prepared throne stands large over the
  sea with "heaven" over it and "earth" on the land.
- **The deliverers rejected.** A tally under the title, headed "rejected",
  fills as the speech goes: Joseph (7:9), Moses (7:27, ringed again at 7:35
  and 7:39), "the council" at 7:51 ("as your fathers did, so you do"), and
  the prophets and the Righteous One (with the Chi-Rho) at 7:52.

## What it shows

- **6:8–6:15** in the card: Stephen in the street among the people, with two
  rings at "wonders and signs"; at 6:9 the camera rises to the eastern sea
  and holds while Cyrene, Alexandria, Cilicia and Asia light, each with a
  dashed line to Jerusalem (drawn in screen space at the hold, since the
  verse rests in the card: `synagogue_overlay`), then comes back down to the
  men of the synagogue disputing; they fall back (6:10); two men are put up
  to it (6:11); the crowd lifts its arms, the elders and scribes seize him,
  and he is led into the hall (6:12); the false witnesses point, and the
  Temple and the law on its stand are ringed (6:13–14); his face lights
  (6:15) and stays lit while he speaks.
- **7:1** the high priest named and ringed.
- **7:2–7:8**: from the hall to Mesopotamia; Abraham at Ur under the first
  throne mark; the road ahead dashed (7:3); the road up the Euphrates and the
  Balikh to Haran and on to Shechem traced, Abraham riding it (7:4); the
  empty outline of a foot by him and the land promised as a dashed line
  round Canaan (7:5); "400 years" (7:6); a line out of Egypt to the land
  (7:7); the three fathers at Hebron, the plate naming them, and the twelve
  (7:8).
- **7:9–7:16**: Joseph's road from Dothan to On; Joseph and Pharaoh at On
  (7:10); the famine darkening Egypt and Canaan (7:11); the two journeys for
  grain, numbered 1 and 2 (7:12–13); "75 souls" at Hebron (7:14) going down to
  Goshen (7:15); the bones carried to Shechem and the tomb there (7:16).
- **7:17–7:29**: the people grown many at Goshen; another king at Rameses;
  Moses a light among them, "3 months" (7:20); taken up by Pharaoh's daughter
  (7:21), grown in Pharaoh's house (7:22), back to his people at forty (7:23);
  the Egyptian struck and gone (7:24); the two brothers, one pointing
  (7:26–28); the flight to Midian and his two sons (7:29). A bar of his 120
  years in three forties (Egypt, Midian, wilderness) fills from 7:20 to 7:36,
  each forty showing "40" when full.
- **7:30**: on to Mount Sinai under the third throne mark, a small burning
  bush lifting in beside it at "a flame of fire in a bush".
- **7:31–7:34** in the bush card. At "As he came close to see" (7:31) the
  camera dives from the map into the mountain's foot: the granite massif
  behind, the flock, the thornbush burning in a soft light, its flame
  swaying slowly (never a flicker). Moses walks up to it, and the voice of
  the Lord goes out from the bush as three widening arcs, at "a voice of the
  Lord" and again at the start of each verse he speaks (7:32–34). "God of
  the fathers" and the three names on the plate (7:32); Moses shivers at
  "trembled" and goes down on his knees at "dared not look". His sandals
  come off and are set by him, and the ground about the bush lights, holy
  ground, and stays lit (7:33). A light comes down on the bush at "I have
  come down to deliver them", and at "Now come" he stands; the camera draws
  back, and he is ringed at "I will send you" (7:34).
- **7:35–7:47**: out of the card to the map, and sent back to Rameses (7:35); the exodus and the wilderness
  traced with the twelve, rings at Rameses and the crossing, "40 years"
  (7:36); the Chi-Rho at Jerusalem for a moment at "a prophet like me"
  (7:37); Sinai ringed (7:38); a line back towards Egypt (7:39); Aaron (7:40),
  the calf on its plinth and an altar (7:41); stars over the wilderness and
  "the prophets" (7:42); Moloch's tent and Rephan's star on the plate, and the
  arc from Jerusalem past Damascus down the Euphrates to beyond Babylon
  (7:43); the tabernacle from the east (from `sanctuary.py`) at Sinai (7:44),
  carried through the wilderness to Gilgal with Joshua and up to Shiloh
  (7:45); David at Jerusalem (7:46); Solomon and his house (7:47).
- **7:48–7:51** the whole speech in one frame, the throne over it, the tally
  completed.
- **7:52–7:60** back into the hall: the law ringed (7:53); the council
  pointing (7:54); the roof drawn back and the prepared throne in the sky
  over the hall, the Chi-Rho standing on its cloud and named "Jesus" (7:55);
  the council's hands up, and the rush (7:57); out through the street and
  the gate, the vision with him, three stones, the garments at the feet of
  Saul, named (7:58); three more stones and his arms raised (7:59); he kneels,
  then lies still (7:60).
- **8:1–8:3**: Saul ringed, the vision goes, and the camera rises over Judea
  and Samaria as the assembly scatters, the twelve apostles staying (8:1); a
  tomb by the city (8:2); back into the street, where Saul takes men and
  women from two houses (8:3).

## Decisions (the owner, 2026-11-05)

- **Scope: 6:8–8:3 only** (71 verses). Philip (8:4–40) is not planned here.
- **The bush gets its own card** (7:31–34). Built 2026-11-06.
- **The stoning is drawn lightly**: three stones, then three, Stephen kneels
  and lies still. Nothing more.
- **"The God of glory" is the prepared throne** (option T1), after the early
  church's hetoimasia (Santa Maria Maggiore, Rome, 430s; the Arian
  Baptistery, Ravenna, c. 500). The Chi-Rho stands on the same cloud at its
  right hand, the viewer's left. The owner liked the idea of a throne but
  found the first sketch did not read; the fix was a real throne shape, in
  the sky on cloud, with the Chi-Rho on the same ground. The sheets (seven
  marks, then five thrones) are in the archive,
  `mockups/acts678-glory-2026-11-05`.

## Defaults picked without the owner

- 7:16 is drawn as Stephen says it, Shechem, though Genesis puts Abraham's
  purchase at Hebron; 7:14 as "75", though Genesis 46:27 says seventy.
- Stephen goes out by the north gate, after the Byzantine tradition.
- Mount Sinai is at Jebel Musa, as in Acts 13–14; Midian's mark is al-Bad'.
- The council sits in a half circle (the Mishnah's description), thirteen
  figures for the seventy-one, with no group labels; the only group names
  are "council" and "high priest".
- The Temple in the card is the house as `temple.py` has it (Kings' plan,
  which Herod's kept), not Herod's own facade.
- Abraham's road follows the Euphrates and the Balikh, and goes on by
  Carchemish and Damascus to Shechem (Genesis 12:6). Joseph is sold at
  Dothan and taken down the coast road. The exodus and the wilderness are
  Acts 13's own routes (`acts_geography.STORY`), the traditional southern
  Sinai.
- The exile arc runs Jerusalem, Damascus, the Euphrates, Babylon, and a
  little beyond.
- Pharaoh (7:10) is at On with Joseph; "another king" (7:18) is at Rameses,
  the delta capital of Exodus 1:11.
- The tabernacle is drawn from the east (court, gate screen, tent behind),
  the one view narrow enough for the map. It stays at Shiloh; David's own
  tent for the ark is not drawn.
- The scattering (8:1) is eighteen dots over Judea and Samaria, the twelve
  staying at Jerusalem.
- The bush card. The camera dives in at 7:31 ("came close to see"), not
  7:30, so 7:30 keeps the map's arrival at Sinai and its throne mark. The
  flame is the appearing: no angel and no figure of God is drawn, and the
  card has no throne mark. The voice is drawn as arcs from the bush. Moses
  is drawn facing us, so "dared not look" is a kneel, not a turned face.
  The flock is Exodus 3:1's, set dressing. The sandals are drawn a third
  over true size so a pair reads. The flame sways on a loop, slowly, as the
  Tabernacle's lamps do.

## QC

The generator prints any name it dropped or forced, a verse that would land
after its narration, and a world or card edge in view. Today it reports no
late verse and no edge. Forced placements left: Shechem beside Abraham at
7:4, Hebron's and "twelve"'s names touching the Salt Sea at 7:8–7:15, the
tabernacle's name on the coast at 7:44, Shiloh beside Joshua at 7:45, and
Jerusalem's name on the coast at 7:48–51. Mount Sinai's name is pressed onto
its dot at 7:30, and dropped where the mark, Moses, Aaron and the
tabernacle crowd it (7:36–7:45 outside 7:38).
Rest frames and the 6:9, 7:2, 7:31, 7:35, 7:43, 7:52, 8:1 flights were
reviewed as contact sheets, and the bush card's beats mid-verse. The verse files are up to 300 KB, 11 MB in all; the 71
files bring the deploy to 6,611.
