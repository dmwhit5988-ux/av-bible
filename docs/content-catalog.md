# Bible Infographic Candidate Catalog

A book-by-book pass over the entire canon (per the 66-book list in `books.py`) identifying which passages best support an infographic — map, timeline, genealogy, architectural diagram, process diagram, comparison chart, or symbolic diagram — and why. Chapters already produced are included inline, marked `✅ Built`, so this is a single complete reference rather than just a gap list.

Not every chapter is a candidate. Long stretches of law, poetry, and personal correspondence resist visual treatment; those books get a one-line note instead of forced entries. Names and quotations in the entries describe the subject; anything lettered on a graphic is taken from the WEB text in `web/bibles/WEB/`.

**This file is machine-read.** The Studio's Coverage tool (`coverage_studio._parse_candidates`) reads every `- **<Book> <chapters> …** — <status> · <types> …` line under a `### <Book>` heading and marks those chapters with the entry's priority. Keep these rules when editing:
- The chapters go in the bold label. A label with no chapter number is invisible to Coverage, so a whole-book entry spells out its span (`Psalms 1–150`). In a label like `3:1–8` only the chapter (3) counts.
- A label that runs into another book counts only this section's chapters, so a span across two books gets an entry under each.
- Coverage takes the priority to be High if that word appears anywhere after the dash, otherwise Med, otherwise Low, so an entry's text must not contain those words, even inside another word ("Medes", "Highlands"). Where entries overlap, a chapter keeps the higher priority.

## Legend

**Status**
- `✅ Built` — the chapter has entries in `web/visuals/manifest.json` (its SVGs are in `web/visuals/<Book>/<chapter>/`, spaces in the book name as underscores). 73 chapters in 11 books, every verse covered.
- `🆕 Candidate` — not yet built

**Priority** (for candidates)
- **High** — flagship/iconic subject, rich and specific source material, produce first
- **Med** — solid candidate, good supporting material, but thinner or overlapping with a stronger entry
- **Low** — plausible but thin, repetitive with another entry, or a stretch

**Infographic type**
- 🗺️ Map — journeys, campaigns, territories, empires
- ⏳ Timeline / Chronology
- 🌳 Genealogy / Family Tree
- 🏛️ Architectural / Structural Diagram — tabernacle, temple, ark, city walls, New Jerusalem
- 🔄 Process / Cycle Diagram — rituals, sacrifices, recurring narrative cycles
- 📊 Comparison / Parallel Chart — kings lists, "better than" arguments, contrasted lists
- 🔢 Numeric / Statistical Infographic — censuses, structured manifests
- 💡 Symbolic / Conceptual Diagram — visions, dream-images, structured teaching

## Navigation

### By Book — Old Testament
[Genesis](#genesis) · [Exodus](#exodus) · [Leviticus](#leviticus) · [Numbers](#numbers) · [Deuteronomy](#deuteronomy) · [Joshua](#joshua) · [Judges](#judges) · [Ruth](#ruth) · [1 Samuel](#1-samuel) · [2 Samuel](#2-samuel) · [1 Kings](#1-kings) · [2 Kings](#2-kings) · [1 Chronicles](#1-chronicles) · [2 Chronicles](#2-chronicles) · [Ezra](#ezra) · [Nehemiah](#nehemiah) · [Esther](#esther) · [Job](#job) · [Psalms](#psalms) · [Proverbs](#proverbs) · [Ecclesiastes](#ecclesiastes) · [Song of Solomon](#song-of-solomon) · [Isaiah](#isaiah) · [Jeremiah](#jeremiah) · [Lamentations](#lamentations) · [Ezekiel](#ezekiel) · [Daniel](#daniel) · [Hosea](#hosea) · [Joel](#joel) · [Amos](#amos) · [Obadiah](#obadiah) · [Jonah](#jonah) · [Micah](#micah) · [Nahum](#nahum) · [Habakkuk](#habakkuk) · [Zephaniah](#zephaniah) · [Haggai](#haggai) · [Zechariah](#zechariah) · [Malachi](#malachi)

### By Book — New Testament
[Matthew](#matthew) · [Mark](#mark) · [Luke](#luke) · [John](#john) · [Acts](#acts) · [Romans](#romans) · [1 Corinthians](#1-corinthians) · [2 Corinthians](#2-corinthians) · [Galatians](#galatians) · [Ephesians](#ephesians) · [Philippians](#philippians) · [Colossians](#colossians) · [1 Thessalonians](#1-thessalonians) · [2 Thessalonians](#2-thessalonians) · [1 Timothy](#1-timothy) · [2 Timothy](#2-timothy) · [Titus](#titus) · [Philemon](#philemon) · [Hebrews](#hebrews) · [James](#james) · [1 Peter](#1-peter) · [2 Peter](#2-peter) · [1 John](#1-john) · [2 John](#2-john) · [3 John](#3-john) · [Jude](#jude) · [Revelation](#revelation)

### By Type — High-Priority Highlights

Every unbuilt High entry, grouped by the types it carries (an entry with two types appears under both), then the built chapters of the same type.

- **🗺️ Map:** [Genesis 12–25](#genesis), [Genesis 25–36](#genesis), [Genesis 37–50](#genesis), [Exodus 12–14](#exodus), [Numbers 10–14](#numbers), [Numbers 33](#numbers), [Numbers 35](#numbers), [Joshua 1–5](#joshua), [Joshua 9–12](#joshua), [Joshua 13–19](#joshua), [1 Samuel 18–27](#1-samuel), [2 Samuel 5, 8, 10](#2-samuel), [1 Kings 12](#1-kings), [1 Kings 17–19](#1-kings), [2 Kings 17](#2-kings), [2 Kings 24–25](#2-kings), [Ezra 1–2](#ezra), [Nehemiah 3](#nehemiah), [Isaiah 13–23](#isaiah), [Ezekiel 47–48](#ezekiel), [Daniel 8](#daniel), [Daniel 10–12](#daniel), [Amos 1–2](#amos), [Jonah 1–2](#jonah), [Matthew 2](#matthew), [Acts 1–2](#acts), [Acts 19–21](#acts), [Acts 27–28](#acts), [Revelation 2–3](#revelation) — plus already-built Genesis 2, Genesis 10, Numbers 32, Numbers 34, Zephaniah 1–3, Acts 13–14, Acts 15–18
- **⏳ Timeline:** [Leviticus 23](#leviticus), [Leviticus 25](#leviticus), [Numbers 33](#numbers), [Judges 3–16](#judges), [1 Kings 12–22 and 2 Kings 1–17](#1-kings), [2 Kings 24–25](#2-kings), [Ecclesiastes 3:1–8](#ecclesiastes), [Daniel 9](#daniel), [Daniel 10–12](#daniel), [Matthew 21–27](#matthew), [Luke 1–2](#luke), [Revelation 6–16](#revelation), [Revelation 19–20](#revelation) — plus already-built Genesis 6–9, Hebrews 1–13, 2 Peter 1–3
- **🌳 Genealogy:** already-built — Genesis 4, Genesis 5, Genesis 10, Genesis 11:10–32, 1 Chronicles 1–9, Matthew 1, Luke 3, Hebrews 7 (the negative genealogy of Melchizedek)
- **🏛️ Architectural:** [Joshua 6](#joshua), [1 Kings 6–7](#1-kings), [Nehemiah 3](#nehemiah), [Ezekiel 40–43](#ezekiel), [Haggai 1](#haggai), [Ephesians 6:10–18](#ephesians), [Revelation 21–22](#revelation) — plus already-built Genesis 6–9, Exodus 25–27, Exodus 28, Numbers 1–2, Hebrews 1–13, Hebrews 9
- **🔄 Process/Cycle:** [Exodus 12](#exodus), [Leviticus 16](#leviticus), [Joshua 6](#joshua), [Judges 2–16](#judges), [Ezekiel 4](#ezekiel), [Haggai 2](#haggai), [Revelation 6–16](#revelation) — plus already-built Acts 15
- **📊 Comparison Chart:** [Leviticus 1–7](#leviticus), [Judges 3–16](#judges), [1 Kings 12–22 and 2 Kings 1–17](#1-kings), [1 Chronicles 22–27](#1-chronicles), [Amos 1–2](#amos), [Haggai 1](#haggai), [Matthew 5–7](#matthew), [Matthew 13](#matthew), [John 2–11](#john), [John 6–15](#john), [1 Corinthians 12](#1-corinthians), [Galatians 5](#galatians), [3 John 1](#3-john), [Revelation 2–3](#revelation) — plus already-built Genesis 1, Numbers 3–4, Zephaniah 1–3, Romans 1–16, Hebrews 10:11–12, Hebrews 12:18–24, 2 Peter 1–3
- **🔢 Numeric/Statistical:** [Exodus 5–11](#exodus), [Joshua 9–12](#joshua), [1 Chronicles 22–27](#1-chronicles), [Ezra 1–2](#ezra) — plus already-built Numbers 1–2
- **💡 Symbolic/Conceptual:** [Exodus 19–20](#exodus), [1 Samuel 17](#1-samuel), [Ecclesiastes 3:1–8](#ecclesiastes), [Ezekiel 1 & 10](#ezekiel), [Ezekiel 4](#ezekiel), [Daniel 2](#daniel), [Daniel 7](#daniel), [Daniel 8](#daniel), [Haggai 2](#haggai), [Zechariah 1–6](#zechariah), [1 Corinthians 12](#1-corinthians), [Ephesians 6:10–18](#ephesians), [2 John 1](#2-john), [3 John 1](#3-john), [Revelation 4–5](#revelation) — plus already-built Genesis 3, Genesis 11:1–9, Zephaniah 1–3, Hebrews 1–13, 2 Peter 1–3

---

## Old Testament

### Genesis
*50 chapters. Extremely rich — origins narrative, three generations of patriarchal travel. **Chapters 1–11 are complete — every verse has a visual.** The patriarchal journey maps are the big gap.*

- **Genesis 1 (Day Structure)** — ✅ Built · 📊 Comparison chart. The six days as a forming-then-filling parallel: Day 1 (light/dark) pairs with Day 4 (sun, moon, stars); Day 2 (sky/sea separated) with Day 5 (birds, fish); Day 3 (land/plants) with Day 6 (land animals, humans); Day 7 is rest. Two columns, three paired rows, a seven-day bar along the foot. *(`generate_genesis1_svg.py`)*
- **Genesis 2** — ✅ Built · 🗺️ Map/Diagram. A schematic garden plan: the river out of Eden parting into four labelled heads (Pishon, Gihon, Hiddekel, Euphrates), the two named trees, the man and the woman, the animals named. Verses 1–3 close Genesis 1's seventh day. *(`generate_genesis2_svg.py`)*
- **Genesis 3** — ✅ Built · 💡 Symbolic/Conceptual. The chapter has no numbers or geography, so the graphic is built from what it does have: a speaker strip (serpent, woman, man, God) with an arc from speaker to hearer on every line of dialogue — the blame arcs of 12–13 staying on screen so the chain reads whole — and a ledger pairing each Genesis 2 statement with the verse that reverses it. Three body modes: the garden (1–13), the three sentences as a triptych (14–19), the expulsion (20–24), closing with a flaming sword that turns every way. *(`generate_genesis3_svg.py`)*
- **Genesis 4** — ✅ Built · 🌳 Genealogy. Cain's line down seven generations to Lamech and his three sons (herding, music, metalwork), with the murder story played across the tree and Seth/Enosh in Adam's other line. Covers all 26 verses. *(`generate_genesis4_svg.py`)*
- **Genesis 5** — ✅ Built · 🌳 Genealogy. Adam to Noah, lifespans visualized. *(`generate_genealogy_svg.py`, from the tables in `generate_genealogy.py`)*
- **Genesis 6–9** — ✅ Built · 🏛️ Architectural + ⏳ Timeline. The ark to scale as a side elevation (300×50×30 cubits, three levels, door, roof) with a 50×30 end-view callout; the water level rises and falls verse by verse and the ark grounds on Ararat at 8:4; a 13-stop dated timeline along the foot carries the chronology. *(`generate_genesis69_svg.py`)*
- **Genesis 10** — ✅ Built · 🌳 Genealogy + 🗺️ Map. The Table of Nations as both: a map of the known world with the three lines as bands and the son-level peoples as dots, plus a panel carrying the running name list and the per-line tallies that add to seventy. *(`generate_genesis10_svg.py`)*
- **Genesis 11** — ✅ Built · 💡 Babel (1–9) + 🌳 Genealogy (10–32). Babel runs on the chapter's own vertical axis: men build up (a ziggurat rising course by course, its top never reaching the sky band it claims) while God comes down; the one-language band breaks into threads at v7, and a Genesis 10 map inset marks Shinar and fires the scattering back out of it. The panel carries the three “Come, let's…” summons — twice from below, once from above. Verses 10–32 remain the Shem-to-Abram genealogy. *(`generate_genesis11_svg.py` owns 1–9, `generate_genealogy_svg.py` owns 10–32 — the project's first split chapter, hence the `verses` ranges in `svg_generators.json`)*
- **Genesis 12–25** — 🆕 High · 🗺️ Map. Abraham's travels: Ur → Haran → Canaan → Egypt (famine) → back to Canaan, plus the Lot separation and the rescue campaign in ch. 14. A career-spanning journey map.
- **Genesis 14** — 🆕 Med · 🗺️ Map. The war of the four kings against five — a short, self-contained campaign map.
- **Genesis 25:12–18** — 🆕 Low · 🌳 Genealogy. Ishmael's twelve sons/tribal princes.
- **Genesis 25–36** — 🆕 High · 🗺️ Map. Jacob's travels: Beersheba → Haran (Laban) → Peniel → back to Canaan, including the wrestling match and reunion with Esau.
- **Genesis 36** — 🆕 Med · 🌳 Genealogy. Esau's line — the origin of Edom's chiefs and kings.
- **Genesis 37–50** — 🆕 High · 🗺️ Map. Joseph sold into slavery, taken to Egypt, then the family's migration to Goshen during the famine — a compact, emotionally loaded journey map.
- **Genesis 49** — 🆕 Med · 📊 Chart. Jacob's blessings over the twelve sons — pairs well as a "tribal characteristics" comparison chart.

### Exodus
*40 chapters. Exodus 25–28, the tabernacle and the priestly garments, are built; several neighboring chapters are equally strong.*

- **Exodus 5–11** — 🆕 High · 🔢 Sequence infographic. The ten plagues, in order, each with its narrative trigger and outcome — a classic numbered-sequence subject.
- **Exodus 12** — 🆕 High · 🔄 Process diagram. Passover's instructions: the lamb, the blood on doorposts, the meal eaten in haste — a ritual-steps diagram.
- **Exodus 12–14** — 🆕 High · 🗺️ Map. The Exodus route from Egypt (Rameses) to the Red Sea crossing.
- **Exodus 16–19** — 🆕 Med · 🗺️ Map. Wilderness route to Sinai: manna and quail, water from the rock at Rephidim, the battle with Amalek, Jethro's visit.
- **Exodus 19–20** — 🆕 High · 💡 Symbolic/structural diagram. Sinai's setting and the Ten Commandments as two tablets — duty to God (1–4) vs. duty to neighbor (5–10). One of the most iconic possible subjects.
- **Exodus 25–27** — ✅ Built · 🏛️ Architectural. Tabernacle diagrams: each verse is the courtyard plan, with a detail inset where the verse describes a part up close, and the part the verse describes pulsing on an overlay. *(drawing and spec in `generate_tabernacle.py`; `generate_exodus26_svg.py` renders chapter 26, `generate_exodus2527_svg.py` chapters 25 and 27)*
- **Exodus 28** — ✅ Built · 🏛️ Architectural. The chapter is a build list — v4 names six garments, then makes them in that order for thirty-five verses — so the frame is what the chapter already has: a priest at full height dressed a garment per verse, v4's manifest ticking off down the left edge as the whole progress indicator, and a working drawing on the right at the scale you can read it. Garments are drawn in **wearing** order and gated by the verse that makes them, so the coat made last at v39 comes out underneath the robe made at v31. Three things a costume plate leaves out are what the drawing carries: the twelve names borne twice (six and six on the shoulder stones at v12, all twelve over the heart at v29 — v29 puts both bearings in one frame), the signet mark that recurs wherever a name is cut (vv11, 21, 36), and the stakes, since v35 and v43 both end on death ("that he not die", "that they don't bear iniquity, and die"). The five materials of v5 run as warp stripes in the cloth rather than sitting in a key, and re-light whenever the text names them again (vv6, 8, 15). The breeches of v42 are appended below the manifest's six, because the chapter adds a seventh garment after the list it gave. *(`generate_exodus28_svg.py` + `svg_priest.py`, the garment geometry it shares with Hebrews)*
- **Exodus 29** — 🆕 Med · 🔄 Process diagram. The consecration of Aaron and his sons, step by step over seven days — the ordination Exodus 28:41 names in three words and Leviticus 8–9 narrates.
- **Exodus 30** — 🆕 Med · 🏛️ Architectural. Incense altar, bronze laver, anointing oil recipe — a natural extension of the 25–27 diagram set.
- **Exodus 35–40** — 🆕 Low · 🏛️ Architectural. The tabernacle's actual construction and erection — largely repeats 25–27's content from the building side.

### Leviticus
*27 chapters. Ritual law translates unusually well into charts and cycle diagrams.*

- **Leviticus 1–7** — 🆕 High · 📊 Comparison chart. The five offerings (burnt, grain, peace, sin, trespass) — what's offered, by whom, and why, side by side.
- **Leviticus 8–9** — 🆕 Med · 🔄 Process diagram. The ordination of Aaron and his sons, step by step.
- **Leviticus 11** — 🆕 Med · 📊 Chart. Clean vs. unclean animals — a natural two-column chart.
- **Leviticus 16** — 🆕 High · 🔄 Process diagram. The Day of Atonement's precise ritual sequence — the two goats, the entry behind the veil.
- **Leviticus 23** — 🆕 High · ⏳ Calendar/timeline. The seven set feasts of Yahweh (Passover, Unleavened Bread, Firstfruits, Weeks, Trumpets, Atonement, Tabernacles) laid out across the year.
- **Leviticus 25** — 🆕 High · ⏳ Cyclical timeline. The sabbatical year (every 7th) and Jubilee (every 50th) — a nested-cycle diagram.
- **Leviticus 26** — 🆕 Low · 📊 Chart. Conditional blessings vs. curses.

### Numbers
*36 chapters. Numbers 1–4, 32 and 34 are already built; the rest of the book is just as map-rich.*

- **Numbers 1–2** — ✅ Built · 🔢 + 🏛️ Camp diagram. Two halves of one world: on the left a plan of the four camps around the Tent of Meeting drawn with **east at the top** (the door faced the sunrise, Judah camps there and marches first, so the order of march reads clockwise); on the right the twelve tribes as a roster — a name, a bar on one shared scale, a number — with Levi held out on a dashed row and the running total climbing to 603,550. Chapter 1 drives the roster, chapter 2 the plan. A prince's name appears only on the row the current verse is naming. *(`generate_numbers1_2_svg.py`)*
- **Numbers 3–4** — ✅ Built · 📊 Chart. An organization chart of the tribe Numbers 1 left out: Aaron's four sons across the top (two struck out at 3:4; the two who remain are the names the rest reports to), then Gershon, Kohath and Merari as three columns carrying families, prince, camp side, and — the body of each column — a drawing of what that clan is responsible for with its pieces labelled a word or two each. Both chapters' lists name the same objects, so chapter 3's standing duty and chapter 4's burden on the march simply light up parts of one drawing rather than being written out. The Kohathite panel drapes its six holy objects one at a time in the blue, scarlet and purple of 4:5–14. Below each column, both counts; on the right, the Levite ring and the 3:40–51 redemption ledger. *(`generate_numbers3_4_svg.py`)*
- **Numbers 7** — 🆕 Low · 🔢 Chart. Twelve tribal leaders' dedication gifts — identical items repeated 12 times; a numeric roster more than a narrative.
- **Numbers 10–14** — 🆕 High · 🗺️ Map. Departure from Sinai, the twelve spies' 40-day reconnaissance route into Canaan, and the report that triggers the wilderness sentence.
- **Numbers 20–21** — 🆕 Med · 🗺️ Map. Edom's refusal of passage, Aaron's death at Hor, the bronze serpent, and the conquest of Sihon and Og — sets up the already-built Numbers 32 map.
- **Numbers 22–24** — 🆕 Med · 🗺️ Map. Balaam's journey and his oracles overlooking the Israelite camp.
- **Numbers 26** — 🆕 Med · 🔢 Comparison chart. The second census, tribe by tribe, set against the first census in ch. 1.
- **Numbers 32** — ✅ Built · 🗺️ Map (Transjordan). *(`generate_numbers32_svg.py`, on the map geometry in `generate_tribal_maps.py`)*
- **Numbers 33** — 🆕 High · 🗺️ Map + ⏳ Timeline. The full 42-station itinerary of the wilderness years, named stop by stop — the natural single map/timeline that ties the whole wilderness period together.
- **Numbers 34** — ✅ Built · 🗺️ Map (Canaan's borders + tribal allotment). *(`generate_numbers34_svg.py`, on the same `generate_tribal_maps.py` geometry)*
- **Numbers 35** — 🆕 High · 🗺️ Map. The six cities of refuge, positioned across both sides of the Jordan.

### Deuteronomy
*34 chapters. Largely sermon and legal recap — lower visual density than the other Pentateuch books.*

- **Deuteronomy 1–3** — 🆕 Low · 🗺️ Map. Historical recap of the wilderness route — mostly redundant with Numbers' fuller treatment.
- **Deuteronomy 27–28** — 🆕 Med · 🗺️ + 💡 Diagram. The blessing/curse ceremony split across Mount Gerizim and Mount Ebal — an unusual geographic-ceremonial layout.
- **Deuteronomy 34** — 🆕 Med · 🗺️ Map. Moses' view of the promised land from Mount Nebo before his death — a viewpoint/vista map.

### Joshua
*24 chapters. One of the strongest map books in the OT.*

- **Joshua 1–5** — 🆕 High · 🗺️ Map. Crossing the Jordan on dry ground and the memorial stones set up at Gilgal.
- **Joshua 6** — 🆕 High · 🏛️ + 🔄 Diagram. The siege of Jericho: the seven-day march sequence culminating in the walls' collapse — an ideal process/sequence diagram.
- **Joshua 7–8** — 🆕 Med · 🗺️ Map. Ai's defeat, then its capture on the second attempt.
- **Joshua 9–12** — 🆕 High · 🗺️ + 🔢 Map. The southern and northern campaigns, plus the summary list of 31 defeated kings in ch. 12 — a classic military-campaign map.
- **Joshua 13–19** — 🆕 High · 🗺️ Map. The actual tribal land allotment west of the Jordan — the natural companion piece to the already-built Numbers 34 border map.
- **Joshua 20** — 🆕 Med · 🗺️ Map. Cities of refuge confirmed — cross-references Numbers 35.
- **Joshua 21** — 🆕 Med · 🗺️ + 🔢 Map. The 48 Levitical cities distributed among the other tribes.

### Judges
*21 chapters. The judges' repeating pattern is one of the best conceptual-diagram subjects in the OT.*

- **Judges 1** — 🆕 Med · 🗺️ Map. The incomplete conquest — which tribes failed to drive out the Canaanites, and where.
- **Judges 2–16 (the judges' cycle)** — 🆕 High · 🔄 Cycle diagram. Sin → oppression → cry for help → deliverer raised up → peace → relapse. A textbook recurring-cycle diagram.
- **Judges 3–16 (the judges' roster)** — 🆕 High · ⏳ + 📊 Timeline/chart. Each of the twelve judges with their tribe, oppressor, years of oppression, and years of peace that followed — a natural chronological chart.
- **Judges 4–5** — 🆕 Med · 🗺️ Map. Deborah, Barak, and Jael's defeat of Sisera.
- **Judges 6–8** — 🆕 Med · 🗺️ + 🔄 Map. Gideon's 300 men and the rout of the Midianite camp.

### Ruth
*4 chapters. Short and mostly personal narrative — light on candidates.*

- **Ruth 1** — 🆕 Low · 🗺️ Map. Naomi's round trip Bethlehem → Moab → Bethlehem.
- **Ruth 4** — 🆕 Med · 🌳 Genealogy. Boaz → Obed → Jesse → David — a short fragment that bridges directly into the already-built Matthew 1 genealogy.

### 1 Samuel
*31 chapters. David's fugitive years are a first-rate map subject.*

- **1 Samuel 4–6** — 🆕 Med · 🗺️ Map. The Ark of the Covenant's travels — captured by the Philistines, moved between cities, then returned.
- **1 Samuel 13–14** — 🆕 Med · 🗺️ Map. Saul and Jonathan's early battles against the Philistines.
- **1 Samuel 17** — 🆕 High · 💡 Symbolic/scale diagram. David and Goliath: the armies' positions across the Valley of Elah, plus the size contrast between the two combatants (Goliath's height and armor weight are given in detail).
- **1 Samuel 18–27** — 🆕 High · 🗺️ Map. David's fugitive years fleeing Saul — Nob, Gath, the cave of Adullam, Keilah, the wilderness of En-gedi, Ziklag. One of the best-documented personal-journey routes in the OT.
- **1 Samuel 28–31** — 🆕 Med · 🗺️ Map. Saul's final battle and death on Mount Gilboa.

### 2 Samuel
*24 chapters.*

- **2 Samuel 1–5** — 🆕 Med · 🗺️ Map. David crowned first over Judah at Hebron, then over all Israel; the capital moves to Jerusalem.
- **2 Samuel 5, 8, 10** — 🆕 High · 🗺️ Map. David's military campaigns and the kingdom's expansion — Philistines, Moab, Ammon, Aram, Edom — the kingdom of David at its territorial height.
- **2 Samuel 6** — 🆕 Med · 🗺️ Map. The Ark brought up to Jerusalem.
- **2 Samuel 11–18** — 🆕 Med · 🗺️ Map. Absalom's rebellion and David's flight route out of Jerusalem across the Jordan.

### 1 Kings
*22 chapters. Solomon's Temple and the divided-kingdom timeline are flagship subjects.*

- **1 Kings 4** — 🆕 Med · 🗺️ + 📊 Map. Solomon's twelve administrative districts, each supplying the court for one month.
- **1 Kings 6–7** — 🆕 High · 🏛️ Architectural. Solomon's Temple and palace complex, with precise dimensions — arguably the best architectural-diagram candidate in the historical books.
- **1 Kings 10** — 🆕 Low · 🗺️ Map. The Queen of Sheba's visit — a trade-route map.
- **1 Kings 12** — 🆕 High · 🗺️ Map. The kingdom splits into Israel (north) and Judah (south) — the foundational map for the rest of Kings and Chronicles.
- **1 Kings 17–19** — 🆕 High · 🗺️ Map. Elijah's travels — the Kerith Ravine, Zarephath, Mount Carmel, the 40-day journey to Horeb.
- **1 Kings 18** — 🆕 Med · 💡 + 🔄 Scene diagram. The contest on Mount Carmel between Elijah and the prophets of Baal.
- **1 Kings 12–22 and 2 Kings 1–17 (parallel kings)** — 🆕 High · ⏳ + 📊 Parallel timeline. The kings of Israel and Judah reigning side by side, with the prophets active in each period — one of the most famous Bible infographics in existence, spanning both books. The OT timeline sheet already dates the kings of both kingdoms, with Ussher's and Thiele's years (`docs/design/ot-timeline.md`).

### 2 Kings
*25 chapters. Chapters 1–17 continue the parallel-kings timeline from 1 Kings.*

- **2 Kings 2–8** — 🆕 Med · 🗺️ Map. Elisha's travels and miracles across several towns.
- **2 Kings 17** — 🆕 High · 🗺️ Map. The fall of Samaria — Israel's deportation to Assyria and resettlement with foreign peoples.
- **2 Kings 1–17 (parallel kings, with 1 Kings 12–22)** — 🆕 High · ⏳ + 📊 Parallel timeline. The second half of the 1 Kings entry: one design across both books, down to the fall of Samaria.
- **2 Kings 18–19** — 🆕 Med · 🗺️ Map. Sennacherib's Assyrian invasion of Judah and the siege of Jerusalem.
- **2 Kings 24–25** — 🆕 High · 🗺️ + ⏳ Map/timeline. The fall of Jerusalem and the waves of deportation to Babylon — sets up Ezra and Nehemiah's return narrative.

### 1 Chronicles
*29 chapters. Chapters 1–9, the genealogies, are built.*

- **1 Chronicles 1–9** — ✅ Built · 🌳 Genealogy. Nine chapters of genealogies from Adam through the returned exiles — the single largest genealogical block in Scripture, rendered as one welded family tree from Adam on, with every verse of the nine chapters a camera move over it. *(`generate_1chronicles_tree_svg.py`: scenes and verse matching from `generate_1chronicles.py`, the tree from `chronicles_tree.py`, the camera in `svg_chronicles_world.py`)* Sections within it: ch. 1 (nations table, parallels Genesis 10), chs. 2–4 (Judah's line to David), ch. 6 (priestly/Levitical line), ch. 9 (post-exilic residents of Jerusalem).
- **1 Chronicles 11–12** — 🆕 Med · 📊 Roster chart. David's mighty men, listed with their individual exploits.
- **1 Chronicles 22–27** — 🆕 High · 📊 + 🔢 Organizational chart. David's organization of temple service — 24 priestly divisions, Levite duties, army divisions by month, tribal leaders — an unusually structured administrative chart.
- **1 Chronicles 28–29** — 🆕 Med · 🏛️ Architectural. The temple's plans handed to Solomon — ties directly to 1 Kings 6–7.

### 2 Chronicles
*36 chapters. Mostly parallels Kings; distinct material below.*

- **2 Chronicles 2–4** — 🆕 Med · 🏛️ Architectural. Temple construction detail, complementing 1 Kings 6–7.
- **2 Chronicles 20** — 🆕 Med · 🗺️ + 💡 Map. Jehoshaphat sends the choir ahead of the army — an unusual battle-strategy diagram.
- **2 Chronicles 32** — 🆕 Med · 🏛️ Engineering diagram. Hezekiah's tunnel and water-system preparations for Sennacherib's siege — a real, still-extant engineering feature.
- **2 Chronicles 36** — 🆕 Low · 🗺️ Map. The final fall of Jerusalem and Cyrus's decree — cross-references 2 Kings 24–25 and Ezra 1.

### Ezra
*10 chapters.*

- **Ezra 1–2** — 🆕 High · 🗺️ + 🔢 Map/manifest. Cyrus's decree and the first wave of returnees from exile, listed by family with headcounts.
- **Ezra 3–6** — 🆕 Med · ⏳ Timeline. The temple's rebuilding, halted by opposition, then completed.
- **Ezra 7–8** — 🆕 Med · 🗺️ Map. Ezra's own return journey, the second wave.

### Nehemiah
*13 chapters. Chapter 3 is an unusually strong, precise candidate.*

- **Nehemiah 1–2** — 🆕 Med · 🗺️ Map. Nehemiah's journey to Jerusalem and his night inspection of the ruined walls.
- **Nehemiah 3** — 🆕 High · 🏛️ + 🗺️ Architectural map. A gate-by-gate, section-by-section list of who rebuilt which part of Jerusalem's wall — a genuinely excellent, precise diagram subject.
- **Nehemiah 4, 6** — 🆕 Med · ⏳ Timeline. Opposition to the rebuilding, and its completion in 52 days.
- **Nehemiah 11–12** — 🆕 Low · 🔢 + 🌳 Chart. Post-exilic population lists and priestly genealogies.

### Esther
*10 chapters.*

- **Esther 1** — 🆕 Med · 🗺️ Map. The Persian Empire's extent — 127 provinces from India to Ethiopia — and the setting at Shushan.
- **Esther 1–10 (overall timeline)** — 🆕 Med · ⏳ Timeline. Events span roughly a decade of Ahasuerus' reign with specific dates given (e.g., the 13th of Adar).
- **Esther 3–9** — 🆕 Low · 💡 Reversal diagram. Haman's plot flipped into Mordecai's triumph — a before/after contrast diagram.

### Job
*42 chapters. Mostly poetic dialogue — low visual density overall.*

- **Job 1–2** — 🆕 Low · 💡 Diagram. The heavenly council framing narrative.
- **Job 38–41** — 🆕 Med · 💡 + 🔢 Catalog. God's speech from the whirlwind catalogs creation — stars, weather, wild animals, Behemoth, Leviathan — a "catalog of creation" infographic.

### Psalms
*150 chapters/psalms. Devotional poetry — very low density for maps/timelines, but two structural candidates stand out.*

- **Psalm 119** — 🆕 Med · 🔤 Structure diagram. A 22-stanza acrostic, one stanza per Hebrew letter, 8 verses each.
- **Psalms 1–150 (the five books)** — 🆕 Med · 📊 Organizational chart. The Psalter's five "books," each closing in a doxology.
- **Psalm 23** — 🆕 Low · 💡 Conceptual. Shepherd/sheep imagery — popular subject, but conceptual rather than diagrammatic.

### Proverbs
*31 chapters. Aphoristic — resists infographic treatment.*

- **Proverbs 31** — 🆕 Low · 🔤 Structure diagram. The virtuous woman poem is also a 22-line acrostic.
- **Proverbs 1–9 (Wisdom vs. Folly)** — 🆕 Low · 📊 Chart. Wisdom and Folly personified and contrasted.

### Ecclesiastes
*12 chapters.*

- **Ecclesiastes 3:1–8** — 🆕 High · ⏳ + 💡 List/wheel diagram. "A time for every purpose" — 14 paired opposites, very well suited to a wheel or paired-list infographic.

### Song of Solomon
*8 chapters. Love poetry with essentially no spatial, chronological, or structural content — no entries; not a fit for this format.*

### Isaiah
*66 chapters.*

- **Isaiah 6** — 🆕 Med · 💡 Vision diagram. The throne-room vision, seraphim, and the burning coal.
- **Isaiah 13–23** — 🆕 High · 🗺️ Map. Oracles against the surrounding nations (Babylon, Moab, Egypt, Tyre, and others) — maps cleanly onto a regional map.
- **Isaiah 36–37** — 🆕 Low · 🗺️ Map. The Assyrian invasion — cross-references 2 Kings 18–19.
- **Isaiah 40–55 (Servant Songs)** — 🆕 Med · 📊 Chart. The four Servant Songs (42, 49, 50, 52–53) compared side by side.
- **Isaiah 65–66** — 🆕 Low · 💡 Conceptual. The new heavens and new earth.

### Jeremiah
*52 chapters.*

- **Jeremiah 18–19** — 🆕 Low · 💡 Sign-act diagram. The potter's house.
- **Jeremiah 25, 27–28** — 🆕 Med · ⏳ Timeline. The 70-years-of-captivity prophecy — ties directly to Daniel 9.
- **Jeremiah 37–39** — 🆕 Low · 🗺️ Map. Siege and fall of Jerusalem — cross-references 2 Kings 25.
- **Jeremiah 46–51** — 🆕 Med · 🗺️ Map. Oracles against the nations (Egypt, Philistia, Moab, Ammon, Edom, Damascus, Babylon) — a regional map, similar to Isaiah 13–23.

### Lamentations
*5 chapters.*

- **Lamentations 1–4** — 🆕 Med · 🔤 Structure diagram. Each chapter is an acrostic (chapter 3 is a triple acrostic of 66 verses) — similar treatment to Psalm 119.

### Ezekiel
*48 chapters. One of the richest books in the whole Bible for this project — rivals Exodus and Daniel.*

- **Ezekiel 1 & 10** — 🆕 High · 💡 Symbolic diagram. The wheel/throne vision — four living creatures and "a wheel within a wheel."
- **Ezekiel 4** — 🆕 High · 🔄 + 💡 Diagram. Siege sign-acts: lying on his side for a set number of days (each day representing a year) and building a model siege of Jerusalem on a clay tile — a genuinely literal diagram Ezekiel himself constructs.
- **Ezekiel 8–11** — 🆕 Med · 🏛️ Diagram. Vision of temple abominations and Yahweh's glory departing.
- **Ezekiel 37** — 🆕 Med · 💡 Sequence diagram. The valley of dry bones — bones, then sinews, then flesh, then breath.
- **Ezekiel 38–39** — 🆕 Med · 🗺️ Map. The Gog/Magog invasion.
- **Ezekiel 40–43** — 🆕 High · 🏛️ Architectural. The new temple, measured room by room by the man with the measuring reed — arguably the single best architectural-diagram candidate in the entire Bible.
- **Ezekiel 47–48** — 🆕 High · 🗺️ Map. The river flowing from the temple, and the land re-allotted to the twelve tribes — the natural companion to Numbers 34 and Joshua 13–19.

### Daniel
*12 chapters. Along with Ezekiel and Exodus, one of the three richest books for this project.*

- **Daniel 2** — 🆕 High · 💡 Symbolic diagram. Nebuchadnezzar's statue (gold, silver, bronze, iron, clay = four kingdoms) — one of the single most iconic infographic subjects in all of Scripture.
- **Daniel 3** — 🆕 Low · 💡 Scene diagram. The fiery furnace.
- **Daniel 4** — 🆕 Low · 💡 Conceptual. Nebuchadnezzar's tree vision and madness.
- **Daniel 5** — 🆕 Low · 💡 Conceptual. The handwriting on the wall.
- **Daniel 7** — 🆕 High · 💡 Symbolic diagram. Four beasts — the direct companion piece to chapter 2's four kingdoms.
- **Daniel 8** — 🆕 High · 💡 + 🗺️ Symbolic diagram. The ram and the goat (Medo-Persia and Greece) and the four horns.
- **Daniel 9** — 🆕 High · ⏳ Timeline. The seventy-weeks prophecy — an extremely popular chronology infographic subject, tied to the coming of Christ.
- **Daniel 10–12** — 🆕 High · ⏳ + 🗺️ Timeline/map. The kings of the north and south conflict, and the end-times timeline — a complex, popular study subject.

### Hosea
*14 chapters. Mostly poetic judgment oracles and the marriage metaphor — low density overall.*

- **Hosea 1–3** — 🆕 Low · 💡 Structure diagram. The marriage-as-metaphor structure (Gomer/Israel).

### Joel
*3 chapters. One landscape for the whole book — a field, a city on a rise behind it, a valley below.*

- **Joel 1** — 🆕 Med · 🔄 + 🔢 Four passes over one field. The four locusts of v4 (swarming locust, great locust, grasshopper, caterpillar) each eat what the last one left, and the produce ledger empties crop by crop. *(design: `docs/design/short-books.md`)*
- **Joel 2** — 🆕 Med · 💡 + 🔄 The swarm redrawn as an army in ranks going up the city wall; the trumpet that gathers; the restoration read straight off chapter 1's ledger (v25); the Spirit poured out on four named groups (quoted in Acts 2). *(design: `docs/design/short-books.md`)*
- **Joel 3** — 🆕 Med · 🗺️ + 📊 The valley of decision: a trade ring of the nations whose arrows reverse (vv1–8), the plowshares beaten into swords, and a watered map with Egypt and Edom left dry. *(design: `docs/design/short-books.md`)*

### Amos
*9 chapters.*

- **Amos 1–2** — 🆕 High · 🗺️ + 📊 Map/chart. Oracles against eight nations, each introduced with the repeated "for three transgressions..., yes, for four" formula — a highly structured list that doubles as a regional map.
- **Amos 7–9** — 🆕 Med · 💡 + 📊 Sequence chart. Five visions of judgment (locusts, fire, plumb line, basket of summer fruit, the Lord beside the altar).

### Obadiah
*1 chapter.*

- **Obadiah 1** — 🆕 Med · 💡 + 🗺️ Judgment on Edom as one cliff drawn in section: the nest set among the stars, the camera falling down the face as the oracle proceeds, the crossroads of v14 as the set-piece, and a territory map for vv19–21. *(design: `docs/design/short-books.md`)*

### Jonah
*4 chapters.*

- **Jonah 1–2** — 🆕 High · 🗺️ Map. Jonah's voyage — Joppa, an attempted flight to Tarshish, the storm, the fish, then Nineveh. A beloved, highly teachable map candidate.

### Micah
*7 chapters.*

- **Micah 5:2** — 🆕 Low · 💡 Conceptual. Bethlehem prophesied as the ruler's birthplace — single-verse, thematic rather than diagrammatic.

### Nahum
*3 chapters. Judgment on Nineveh: one city approached, entered, and set beside a city that already fell. Geographically it pairs with Jonah.*

- **Nahum 1** — 🆕 Med · 💡 + 📊 The storm front crossing three named ridges (Bashan, Carmel, Lebanon), then the hinge of vv7–8 as a two-column ledger: a stronghold standing in the rising flood. *(design: `docs/design/short-books.md`)*
- **Nahum 2** — 🆕 Med · 🏛️ + 🔄 The city in cutaway, taken piece by piece: chariots in the streets, the river gates opening on v6 and the water taking the palace, the spoil emptied, and the lions' den drawn empty. *(design: `docs/design/short-books.md`)*
- **Nahum 3** — 🆕 Med · 📊 Nineveh set beside No-Amon (Thebes): the same row of defences and allies under both cities, Thebes' already struck through, Nineveh's struck one at a time. *(design: `docs/design/short-books.md`)*

### Habakkuk
*3 chapters. A dialogue, a watchtower, and a march — three different geometries.*

- **Habakkuk 1** — 🆕 Med · 💡 + 📊 A two-speaker exchange on the Genesis 3 speaker-strip device: two complaints and the answer between them, ending on men taken like fish with the hook and the net. *(design: `docs/design/short-books.md`)*
- **Habakkuk 2** — 🆕 Med · 🏛️ + 📊 The watchtower and the tablet of v2 ("make it plain on tablets"), with the five woes cut into it as five emblems. *(design: `docs/design/short-books.md`)*
- **Habakkuk 3** — 🆕 Med · 🗺️ + 🔢 A march across named ground (Teman, Mount Paran, Cushan, Midian), then six empty stalls and bins, all counted, all nothing (vv17–19). *(design: `docs/design/short-books.md`)*

### Zephaniah
*3 chapters. Complete — every verse has a visual. Read for structure rather than theme, the book carries three strong geometries; the design is in `docs/design/short-books.md`.*

- **Zephaniah 1–3** — ✅ Built · 💡 + 🗺️ + 📊. Chapter 1 draws the created world as three registers — sky, land, sea — and sweeps them in the order 1:3 gives (man, animal, birds, fish), which is the filling of Genesis 1 run backwards; then the hand stretched out, the rooftop worshippers who swear two ways at once, the sacrifice and its bidden guests, a plan of the city searched quarter by quarter with a lamp, and the nine words of 1:15 as a bar that goes to black one word at a time. Chapter 2 lays a compass over Judah and takes the oracles round the points in the text's own order — west (the four Philistine cities), east (Moab and Ammon), south (Cush), north (Nineveh) — with a corner compass as the whole progress indicator; Nineveh's ruin is a building labelled by the creatures now occupying its named parts (capitals, windows, thresholds, cedar beams). Chapter 3 holds one centre point through three occupants: Yahweh bringing justice to light every morning while the four offices fail around him (3:5), the afflicted and poor left in place of the proud (3:12), and the King who rejoices with singing (3:17). *(`generate_zephaniah_svg.py`)*

### Haggai
*2 chapters. Five dates in Darius' second year run under both chapters as one date rail; it ties into the Ezra 3–6 rebuilding. One of the two best next builds among the short books.*

- **Haggai 1** — 🆕 High · 📊 + 🏛️ Two houses at one scale — the paneled private house finished, Yahweh's house a bare foundation — and the futility ledger of v6: five inputs that never arrive at their outputs, ending in the bag with holes. *(design: `docs/design/short-books.md`)*
- **Haggai 2** — 🆕 High · 💡 + 🔄 The first temple ghosted behind the new work at true scale; the priests' two rulings (vv12–13) as one contact chain drawn twice, holiness stopping after the first link and uncleanness running down every link; the shortfall jars of vv16–19; the signet ring. *(design: `docs/design/short-books.md`)*

### Zechariah
*14 chapters.*

- **Zechariah 1–6 (eight night visions)** — 🆕 High · 💡 Sequence diagram. Horsemen, four horns, a measuring line, a flying scroll, a woman in a basket, four chariots, and more — a rich sequence-of-visions infographic, comparable to Ezekiel's and Daniel's visions.
- **Zechariah 9–14** — 🆕 Med · ⏳ + 💡 Timeline. Messianic prophecies — the triumphal entry, thirty pieces of silver, the pierced one, the final battle for Jerusalem.

### Malachi
*4 chapters. Disputational oracles — low density, no standout diagram candidate.*

---

## New Testament

### Matthew
*28 chapters. Strong across the board — genealogy already built, several other flagship candidates remain.*

- **Matthew 1** — ✅ Built · 🌳 Genealogy. Verses 1–17 are a camera over the real Old Testament family tree — the welded tree 1 Chronicles 1–9 is read against, which already held thirty-six of Matthew's names in his order — so the generations he passes over sit on the sheet unlit and his fourteens can be seen being made. Verses 18–25 move to a figure stage for the Nativity, closing on the manger. *(`generate_matthew1_svg.py`: the grafts and verse table in `matthew_tree.py`, the camera in `svg_matthew_world.py`, the stage in `svg_matthew_nativity.py`; design in `docs/design/matthew-1.md`)*
- **Matthew 2** — 🆕 High · 🗺️ Map. The wise men's journey from the East, and the flight to Egypt then Nazareth.
- **Matthew 3–4** — 🆕 Low · 🗺️ Map. Baptism, temptation, and the geography of the Galilean ministry base.
- **Matthew 5–7** — 🆕 High · 📊 Structural chart. The Sermon on the Mount's outline — the Beatitudes, the "you have heard... but I tell you" antitheses, the Lord's Prayer, the Golden Rule.
- **Matthew 8–9** — 🆕 Med · 📊 Catalog chart. A concentrated sequence of miracles.
- **Matthew 13** — 🆕 High · 📊 Comparison chart. Seven kingdom parables in a single chapter.
- **Matthew 16–17** — 🆕 Low · 💡 Conceptual. Caesarea Philippi confession and the Transfiguration.
- **Matthew 21–27** — 🆕 High · ⏳ Timeline. Holy Week, day by day, from the triumphal entry to the crucifixion — one of the most popular infographic subjects in the whole Bible.
- **Matthew 24–25** — 🆕 Med · ⏳ + 💡 Timeline. The Olivet Discourse — signs of the end, the ten virgins, the talents, the sheep and the goats.

### Mark
*16 chapters. Mostly parallels Matthew/Luke's already-covered events; two distinct entries.*

- **Mark 1–2** — 🆕 Med · 📊 Chart. Mark's characteristic "a day in the life" density — a rapid sequence of miracles and encounters compressed into one busy day.
- **Mark 11–16** — 🆕 Low · ⏳ Timeline. Passion week — cross-references the Matthew 21–27 entry rather than duplicating it.

### Luke
*24 chapters. Genealogy already built; the birth narrative and travel narrative are strong additional candidates.*

- **Luke 1–2** — 🆕 High · ⏳ Timeline. The nativity timeline — Zechariah's vision, Mary's conception, the visitation, the birth, the shepherds, the presentation, the boy Jesus at twelve.
- **Luke 3** — ✅ Built · 🌳 Genealogy (back to Adam, 77 names). Verses 1–22 are one held scene at the surface, building to the ax laid at the root of the trees (v9); verses 23–38 are a camera descending one long taproot from Jesus to "the son of God". *(`generate_luke3_svg.py`, names and geometry in `generate_luke3.py`)*
- **Luke 9–19 (the travel narrative)** — 🆕 Med · 🗺️ Map. Luke structures a large central section of the Gospel as a single journey toward Jerusalem, naming villages along the way.
- **Luke 15** — 🆕 Med · 📊 Comparison chart. Three parables of the lost — sheep, coin, son — presented side by side.
- **Luke 22–23** — 🆕 Low · ⏳ Timeline. Passion week — cross-references the Matthew 21–27 entry.
- **Luke 24** — 🆕 Low · 🗺️ Map. The road to Emmaus.

### John
*21 chapters. Two of the strongest structural candidates in the entire NT.*

- **John 2–11 (seven signs)** — 🆕 High · 📊 Structural chart. The seven sign-miracles that structure the Gospel (water to wine, the official's son, the lame man, feeding the 5,000, walking on water, the blind man, Lazarus) — a famous literary-structure infographic unique to John.
- **John 6–15 (seven "I am" statements)** — 🆕 High · 📊 Structural chart. Bread of life, light of the world, the door, the good shepherd, the resurrection and the life, the way/truth/life, the true vine — pairs naturally with the seven signs.
- **John 13–17** — 🆕 Low · 💡 Conceptual. The Upper Room Discourse — mostly extended teaching, thin on diagrammatic content.
- **John 18–19** — 🆕 Med · 🔄 Sequence diagram. The distinct stages of the Jewish and Roman trials, as its own process diagram.

### Acts
*28 chapters. Along with Genesis/Exodus/Ezekiel/Daniel, one of the richest books in the Bible for this project — the missionary journeys are some of the best-known Bible maps in existence.*

- **Acts 1–2** — 🆕 High · 🗺️ Map. The Ascension and Pentecost, including the list of nations/languages represented in Jerusalem.
- **Acts 6–8** — 🆕 Med · 🗺️ Map. Stephen's martyrdom, the gospel's spread to Samaria, and the Ethiopian eunuch's road.
- **Acts 9** — 🆕 Med · 🗺️ Map. Paul's conversion on the Damascus road.
- **Acts 13–14** — ✅ Built · 🗺️ Map. Paul's First Missionary Journey as a camera tour over one large map (as Numbers 34), the road traced leg by leg and the road home a double line. The camera dives into three drawn scenes: the synagogue at Antioch of Pisidia, where the sermon starts and ends and the two Sabbaths are acted out; Jerusalem (13:27–37), where the Chi-Rho (Jesus, never drawn as a man) is crucified, buried and rises, and David's sealed tomb stands beside the open one; and Lystra (14:8–20), where the lame man leaps up, the crowd takes Barnabas and Paul for Jupiter and Mercury, and Paul is stoned and rises. Between them the sermon flies Israel's story over the map (13:17–26) ([design/acts-13-14.md](design/acts-13-14.md)). *(`generate_acts1314_svg.py`, `acts_geography.py`, `acts1314_synagogue.py`, `acts1314_jerusalem.py`, `acts1314_lystra.py`)*
- **Acts 15** — ✅ Built · 🔄 Process diagram. The Jerusalem Council's decision process — a road with a bar across it, argued above and lifted by the decree. Built as the first break-away of the second-journey generator. *(`generate_acts1518_svg.py`)*
- **Acts 15–18** — ✅ Built · 🗺️ Map. Paul's Second Missionary Journey — Asia Minor into Macedonia and Greece. Only ~30 of the 143 verses travel, so the map carries those and steps aside for five set-pieces: the council, Philippi, Thessalonica & Beroea, the Areopagus, and Corinth. *(`generate_acts1518_svg.py`)*
- **Acts 19–21** — 🆕 High · 🗺️ Map. Paul's Third Missionary Journey, which starts at 18:23 — centered on Ephesus, then the return to Jerusalem. Acts 18 is built with the second journey above, so the work is chapters 19–21 on the same coastline (`MED`/`PELOPONNESE`/`ISLANDS` in `generate_acts1518_svg.py`).
- **Acts 27–28** — 🆕 High · 🗺️ Map. The voyage to Rome and the shipwreck at Malta — a richly detailed, highly mappable nautical journey.

### Romans
*16 chapters. Complete — every verse has a visual. See `docs/design/romans.md` for the design.*

- **Romans 1–16** — ✅ Built · 📊 Doctrinal flow chart. One full-frame scene per chapter (two for chapters 1 and 3, which turn hard mid-chapter), threaded by the Romans Road: a Roman road the letter keeps returning to, where each classic Road verse (3:23, 5:6–11, 6:23, 10:8–13) plants an engraved milestone and each return shows the milestones already planted. Chapter 5's Adam/Christ parallel is drawn as two doorways and chapter 11 is the olive tree. Nothing on the canvas counts the verses; short engraved phrases mark the hinge verses only. *(`generate_romans_svg.py`)*

### 1 Corinthians
*16 chapters.*

- **1 Corinthians 12** — 🆕 High · 💡 + 📊 Diagram. The body of Christ / spiritual gifts — many members, one body. A perennially popular diagram subject.
- **1 Corinthians 15** — 🆕 Med · ⏳ Sequence. The resurrection order — "Christ the first fruits, then those who are Christ's, at his coming."

### 2 Corinthians
*13 chapters. Personal and defensive in tone — low density.*

- **2 Corinthians 11** — 🆕 Low · 🔢 Catalog. Paul's catalog of sufferings and trials.

### Galatians
*6 chapters.*

- **Galatians 3–4** — 🆕 Med · 📊 Chart. The law-vs-grace, promise-vs-law argument, including the Hagar/Sarah allegory.
- **Galatians 5** — 🆕 High · 📊 Contrast chart. Works of the flesh vs. fruit of the Spirit — two contrasted lists, a very popular subject.

### Ephesians
*6 chapters.*

- **Ephesians 6:10–18** — 🆕 High · 🏛️ + 💡 Diagram. The armor of God — six named pieces, each explained. One of the most popular Bible infographics ever produced.
- **Ephesians 2** — 🆕 Med · 💡 Conceptual. Grace through faith, and the "middle wall of partition" between Jew and Gentile broken down.
- **Ephesians 4:11** — 🆕 Low · 📊 Chart. The five-fold ministry gifts.

### Philippians
*4 chapters. Low density otherwise.*

- **Philippians 2:5–11** — 🆕 Med · 💡 Shape diagram. The kenosis hymn — Christ's descent then exaltation, a natural V-shaped diagram.

### Colossians
*4 chapters. Low density.*

- **Colossians 1:15–20** — 🆕 Low · 💡 Conceptual. The supremacy of Christ — creator, head of the church, firstborn from the dead.

### 1 Thessalonians
*5 chapters.*

- **1 Thessalonians 4:13–18** — 🆕 Med · ⏳ Sequence diagram. The resurrection/rapture sequence — the dead in Christ rising first, then the living caught up.

### 2 Thessalonians
*3 chapters.*

- **2 Thessalonians 1** — 🆕 Med · 📊 A balance that tips at the revealing (vv5–10): those who afflict on one pan, the afflicted on the other, and the loads swap sides. *(design: `docs/design/short-books.md`)*
- **2 Thessalonians 2** — 🆕 Med · ⏳ + 🔄 A gated sequence the text insists on — the rebellion, the one who restrains until he is taken out of the way, the man of sin revealed — with a counter-sequence for the readers running the other way. Pairs with the 1 Thessalonians entry and, further out, Daniel 9 and Revelation. *(design: `docs/design/short-books.md`)*
- **2 Thessalonians 3** — 🆕 Med · 🔄 + 💡 Two walks side by side with the rule of v10 as the gate between them, discipline drawn as distance rather than expulsion, and Paul's own hand at v17 answering the letter "as if from us" of 2:2. *(design: `docs/design/short-books.md`)*

### 1 Timothy
*6 chapters.*

- **1 Timothy 3** — 🆕 Med · 📊 Comparison chart. Qualifications for bishops and deacons, listed side by side.

### 2 Timothy
*4 chapters. A personal farewell letter — no standout candidate.*

### Titus
*3 chapters.*

- **Titus 1** — 🆕 Med · 🗺️ + 📊 Crete as an island map, its cities filled one by one as elders are appointed (v5); the qualifications of vv6–9 as a two-sided checklist against one figure (parallels 1 Timothy 3); then the houses overthrown against the cities set in order. *(design: `docs/design/short-books.md`)*
- **Titus 2** — 🆕 Med · 📊 + ⏳ The household table of vv1–10 (five groups, five charges, three purpose clauses), and the two appearings of vv11–13 as a bracket around "this present age". *(design: `docs/design/short-books.md`)*
- **Titus 3** — 🆕 Med · 📊 + 🔄 Were / now, hinged on the washing of regeneration (vv3–7); a three-step process for the factious man; a short route strip to Nicopolis. *(design: `docs/design/short-books.md`)*

### Philemon
*1 chapter. A single-chapter personal letter with three subjects that fit on one page.*

- **Philemon 1** — 🆕 Med · 💡 + 🔢 + 🗺️ The cast inside the house of v2; Onesimus's label changing on its own verse (useless → useful, slave → beloved brother) over the round trip Colossae → Rome → Colossae; and the ledger of vv18–19, the debt moved to Paul's account in his own hand. *(design: `docs/design/short-books.md`)*

### Hebrews
*13 chapters, 303 verses. Complete — every verse has a visual. See `docs/design/hebrews.md` for the design and what the build changed.*

- **Hebrews 1–13** — ✅ Built · 🏛️ + 💡 + ⏳. One vertical section drawn twice: the heavenly structure solid at the top of the frame, the earthly tabernacle below it as the **shadow it casts** (8:5 *a copy and shadow*, 9:24 *representations of the true*, 10:1 *a shadow… not the very image*). The camera's height on that column is the whole progress indicator, and the book is read as an approach — *drift away* (2:1), *enter into … rest* (3–4), *within the veil* (6:19), *a new and living way* (10:20) — until 12:27 shakes the shadow layer off and 13:13 deliberately reverses, dropping the camera below the camp because the altar moved. Chapters 11–12 leave the column for a ground plane: a road of pilgrims walking toward a city none of them reach (11:39), whose gap becomes the racetrack at 12:1 and whose destination is the top of the same column at 12:2. Threads: voice-arcs for every OT quotation (Hebrews says *he says*, never *it is written*), the five warnings, and the eleven **BETTER** verses.
- **Hebrews 7** — ✅ Built · 🌳 Genealogy (break-away), in three sub-scenes. Melchizedek drawn as a genealogy node with the parent sockets empty and the lifespan bar running off both edges (*without father, without mother, without genealogy*), Levi nested inside Abraham at the moment of the tithe (7:9–10), and a row of priest figures each struck through by death against one unstruck (7:23–25).
- **Hebrews 9** — ✅ Built · 🏛️ Architectural, in five sub-scenes. The tabernacle in section, reusing the built Exodus 25–27 geometry directly — the shadow layer *is* that drawing, flattened. Its best idea is the traffic diagram of 9:6–7: many worn paths into the first room, one thin dated path into the second.
- **Hebrews 10:11–12** — ✅ Built · 📊 Set-piece. Every priest *stands* day by day offering the same sacrifices; one offered a single sacrifice and **sat down**. Pays off a frame-wide omission — there is no seat anywhere in the lower structure.
- **Hebrews 12:18–24** — ✅ Built · 📊 Set-piece. Sinai against Zion, seven items a side in the text's own order — the sharpest single contrast in the book.

### James
*5 chapters. Practical wisdom letter — low density.*

- **James 1** — 🆕 Low · 🔄 Process diagram. Trials → patience → maturity.

### 1 Peter
*5 chapters. Low-to-medium density.*

- **1 Peter 2** — 🆕 Low · 💡 Conceptual. Living stones / spiritual house metaphor.

### 2 Peter
*3 chapters. Complete — every verse has a visual. One of the two built short books (1–3 chapters), with Zephaniah; `docs/design/short-books.md` holds its design and those of the other eleven.*

- **2 Peter 1–3** — ✅ Built · 📊 + 💡 + ⏳. Three chapters, three geometries. Chapter 1 is the ladder of 1:5–7, eight rungs added a clause at a time, with a sight gauge on the right — because the charge in v9 against the man who lacks them is that he is blind, "seeing only what is near", and what he cannot see is the entrance of v11, drawn at the far end of that same horizon; then the tent Peter is shortly to put off set against the mount that stands, and the three light sources of v19 in the order the verse gives them. Chapter 2 puts the three judgment precedents on one rail with the count that came out of each (0, 8, 1), draws v11's withheld accusation as a power comparison, and closes the proverbs of v22 as a loop that returns the last frame to the first. Chapter 3 breaks the mockers' unbroken line into three worlds divided by water and fire, lays v8's two rulers at true relative length, and brings chapter 1's ladder back at 3:18 with one more rung. *(`generate_2peter_svg.py`)*

### 1 John
*5 chapters.*

- **1 John 2–5 (tests of genuine faith)** — 🆕 Med · 📊 Chart. The repeated "by this we know" tests of fellowship and true faith (2:3 to 5:2).

### 2 John
*1 chapter. Designed with 3 John as a diptych — the same threshold drawn twice, in opposite senses; with Haggai, the best next build among the short books.*

- **2 John 1** — 🆕 High · 💡 A threshold, rightly closed: the chosen lady's house with one door, truth and love going in, the deceivers approaching, and the door shut at vv10–11; closing on paper and ink set aside for face to face. *(design: `docs/design/short-books.md`)*

### 3 John
*1 chapter. The other half of the 2 John diptych.*

- **3 John 1** — 🆕 High · 📊 + 💡 Three doorways, one per named man: Gaius open (vv1–8), Diotrephes wrongly bolted (vv9–11), Demetrius with the testimony of all over the lintel (v12); the ending drawn to match 2 John's. *(design: `docs/design/short-books.md`)*

### Jude
*1 chapter.*

- **Jude 1** — 🆕 Med · 📊 + 💡 + 🌳 Jude thinks in threes: three judgment precedents on one rail (Egypt, the angels, Sodom and Gomorrah), three routes off one road (Cain, Balaam, Korah), six things failing at their own job (vv12–13), Enoch as the seventh from Adam lit on the Genesis 5 line, and a three-way triage (vv22–23). *(design: `docs/design/short-books.md`)*

### Revelation
*22 chapters. Alongside Genesis/Exodus/Ezekiel/Daniel/Acts, the richest book in the Bible for this project.*

- **Revelation 1** — 🆕 Med · 💡 Vision diagram. Christ among the seven lampstands.
- **Revelation 2–3** — 🆕 High · 🗺️ + 📊 Map/chart. The seven churches of Asia Minor, each with its location, commendation, rebuke, and promise — one of the best-known map+chart combinations in the NT.
- **Revelation 4–5** — 🆕 High · 💡 Symbolic diagram. The throne room — 24 elders, four living creatures, the sealed scroll.
- **Revelation 6–16** — 🆕 High · ⏳ + 🔄 Sequence diagram. Seven seals → seven trumpets → seven bowls — an escalating structured sequence, arguably the single best diagram candidate in the whole NT.
- **Revelation 12** — 🆕 Med · 💡 Symbolic diagram. The woman, the child, and the dragon.
- **Revelation 13** — 🆕 Med · 💡 Symbolic diagram. The two beasts.
- **Revelation 17** — 🆕 Low · 💡 Conceptual. The great harlot / Babylon.
- **Revelation 19–20** — 🆕 High · ⏳ Timeline. The return of Christ, the millennium, and the final judgment — the text's own event sequence, independent of any particular interpretive framework.
- **Revelation 21–22** — 🆕 High · 🏛️ Architectural. The New Jerusalem — precise measurements (the city measured with the reed, its length, width and height equal; the wall; twelve named gates and foundations). A spectacular architectural-diagram candidate that rivals Ezekiel 40–43 and the tabernacle.
