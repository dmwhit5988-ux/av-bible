# Bible Infographic Candidate Catalog

A book-by-book pass over the entire canon (per the 66-book list in `books.py`) identifying which passages best support an infographic — map, timeline, genealogy, architectural diagram, process diagram, comparison chart, or symbolic diagram — and why. The 8 chapters already produced (see `visuals/manifest.json`) are included inline, marked `✅ Built`, so this is a single complete reference rather than just a gap list.

Not every chapter is a candidate. Long stretches of law, poetry, and personal correspondence resist visual treatment; those books get a one-line note instead of forced entries.

## Legend

**Status**
- `✅ Built` — visual already exists (see `visuals/<Book>/<chapter>/`)
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

- **🗺️ Map:** [Genesis 12–25](#genesis), [Genesis 25–36](#genesis), [Genesis 37–50](#genesis), [Exodus 12–14](#exodus), [Numbers 10–14](#numbers), [Numbers 33](#numbers), [Numbers 35](#numbers), [Joshua 1–5](#joshua), [Joshua 9–12](#joshua), [Joshua 13–19](#joshua), [1 Samuel 18–27](#1-samuel), [2 Samuel 5, 8, 10](#2-samuel), [1 Kings 12](#1-kings), [1 Kings 17–19](#1-kings), [2 Kings 17](#2-kings), [2 Kings 24–25](#2-kings), [Ezra 1–2](#ezra), [Nehemiah 3](#nehemiah), [Isaiah 13–23](#isaiah), [Ezekiel 47–48](#ezekiel), [Amos 1–2](#amos), [Jonah 1–2](#jonah), [Matthew 2](#matthew), [Acts 1–2](#acts), [Acts 13–14](#acts), [Acts 15–18](#acts), [Acts 18–21](#acts), [Acts 27–28](#acts), [Revelation 2–3](#revelation)
- **⏳ Timeline:** [Genesis 6–9](#genesis), [Leviticus 23](#leviticus), [Leviticus 25](#leviticus), [Numbers 33](#numbers), [Judges — the judges' cycle roster](#judges), [1 Kings 12 – 2 Kings 17](#1-kings), [2 Kings 24–25](#2-kings), [Ecclesiastes 3:1–8](#ecclesiastes), [Daniel 9](#daniel), [Daniel 10–12](#daniel), [Matthew 21–27](#matthew), [Luke 1–2](#luke), [Hebrews 11](#hebrews), [Revelation 6–16](#revelation), [Revelation 19–20](#revelation)
- **🌳 Genealogy:** [Genesis 10](#genesis), [1 Chronicles 1–9](#1-chronicles) — plus already-built Genesis 5, Genesis 11, Matthew 1, Luke 3
- **🏛️ Architectural:** [Genesis 6–9](#genesis), [Exodus 28–29](#exodus), [1 Kings 6–7](#1-kings), [Nehemiah 3](#nehemiah), [Ezekiel 40–43](#ezekiel), [Ephesians 6:10–18](#ephesians), [Hebrews 9](#hebrews), [Revelation 21–22](#revelation) — plus already-built Exodus 25–27
- **🔄 Process/Cycle:** [Exodus 12](#exodus), [Leviticus 16](#leviticus), [Joshua 6](#joshua), [Judges — the judges' cycle](#judges), [Ezekiel 4](#ezekiel), [Revelation 6–16](#revelation)
- **📊 Comparison Chart:** [Genesis 1 (Day Structure)](#genesis), [Leviticus 1–7](#leviticus), [1 Chronicles 22–27](#1-chronicles), [Amos 1–2](#amos), [Matthew 5–7](#matthew), [Matthew 13](#matthew), [John — seven signs](#john), [John — seven "I am" statements](#john), [Romans](#romans), [Galatians 5](#galatians), [Hebrews — "better than" argument](#hebrews), [Hebrews 11](#hebrews), [Revelation 2–3](#revelation)
- **🔢 Numeric/Statistical:** [Numbers 1–2](#numbers), [Ezra 1–2](#ezra)
- **💡 Symbolic/Conceptual:** [Exodus 19–20](#exodus), [Ezekiel 1 & 10](#ezekiel), [Ezekiel 4](#ezekiel), [Daniel 2](#daniel), [Daniel 7](#daniel), [Daniel 8](#daniel), [Zechariah 1–6](#zechariah), [1 Samuel 17](#1-samuel), [1 Corinthians 12](#1-corinthians), [Ephesians 6:10–18](#ephesians), [Revelation 4–5](#revelation)

---

## Old Testament

### Genesis
*50 chapters. Extremely rich — origins narrative, three generations of patriarchal travel, and two genealogies already built.*

- **Genesis 1** — ✅ Built · 📷 Photo stills. The six creation days, each paired with a natural-world photograph. *(`visuals/Genesis/1/`)*
- **Genesis 1 (Day Structure)** — 🆕 High · 📊 Comparison chart / ⏳ Sequence diagram. The six days follow a forming-then-filling parallel: Day 1 (light/dark) pairs with Day 4 (sun, moon, stars); Day 2 (sky/sea separated) pairs with Day 5 (birds, fish); Day 3 (land/plants) pairs with Day 6 (land animals, humans); Day 7 is rest. A two-column diagram lining up days 1–3 against days 4–6 makes this literary structure visible — a strong candidate independent of and complementary to the existing photo-stills treatment.
- **Genesis 2** — 🆕 Med · 🗺️ Map/Diagram. Eden is described with four named rivers (Pishon, Gihon, Hiddekel, Euphrates) branching from one source. A simple garden-layout map fits the geographic detail given.
- **Genesis 4:17–22** — 🆕 Low · 🌳 Genealogy. Cain's line down to Lamech and his three sons (the first musician, metalworker, and herdsman). Small but a clean family-tree fragment.
- **Genesis 5** — ✅ Built · 🌳 Genealogy. Adam to Noah, lifespans visualized. *(`visuals/Genesis/5/`)*
- **Genesis 6–9** — 🆕 High · 🏛️ Architectural + ⏳ Timeline. The ark is given exact dimensions (300×50×30 cubits, three decks) and the flood is dated almost to the day (17th day of month 2 through the waters' full recession). A cutaway diagram suits the ark's structure; a dated timeline suits the flood's day-by-day chronology.
- **Genesis 10** — 🆕 High · 🌳 Genealogy + 🗺️ Map. The Table of Nations: Noah's three sons' descendants mapped onto the known ancient world's peoples. A genealogy that doubles as a map — one of the richest hybrid candidates in the OT.
- **Genesis 11** — ✅ Built (genealogy) · plus 🆕 Med · 💡 Tower of Babel (11:1–9), a dispersion diagram of one language becoming many, scattering peoples across the map already established in ch. 10.
- **Genesis 12–25** — 🆕 High · 🗺️ Map. Abraham's travels: Ur → Haran → Canaan → Egypt (famine) → back to Canaan, plus the Lot separation and the rescue campaign in ch. 14. A career-spanning journey map.
- **Genesis 14** — 🆕 Med · 🗺️ Map. The war of the four kings against five — a short, self-contained campaign map.
- **Genesis 25:12–18** — 🆕 Low · 🌳 Genealogy. Ishmael's twelve sons/tribal princes.
- **Genesis 25–36** — 🆕 High · 🗺️ Map. Jacob's travels: Beersheba → Haran (Laban) → Peniel → back to Canaan, including the wrestling match and reunion with Esau.
- **Genesis 36** — 🆕 Med · 🌳 Genealogy. Esau's line — the origin of Edom's chiefs and kings.
- **Genesis 37–50** — 🆕 High · 🗺️ Map. Joseph sold into slavery, taken to Egypt, then the family's migration to Goshen during the famine — a compact, emotionally loaded journey map.
- **Genesis 49** — 🆕 Med · 📊 Chart. Jacob's blessings over the twelve sons — pairs well as a "tribal characteristics" comparison chart.

### Exodus
*40 chapters. The tabernacle chapters are already built; several neighboring chapters are equally strong.*

- **Exodus 5–11** — 🆕 High · 🔢 Sequence infographic. The ten plagues, in order, each with its narrative trigger and outcome — a classic numbered-sequence subject.
- **Exodus 12** — 🆕 High · 🔄 Process diagram. Passover's instructions: the lamb, the blood on doorposts, the meal eaten in haste — a ritual-steps diagram.
- **Exodus 12–14** — 🆕 High · 🗺️ Map. The Exodus route from Egypt (Rameses) to the Red Sea crossing.
- **Exodus 16–19** — 🆕 Med · 🗺️ Map. Wilderness route to Sinai: manna and quail, water from the rock at Rephidim, the battle with Amalek, Jethro's visit.
- **Exodus 19–20** — 🆕 High · 💡 Symbolic/structural diagram. Sinai's setting and the Ten Commandments as two tablets — duty to God (1–4) vs. duty to neighbor (5–10). One of the most iconic possible subjects.
- **Exodus 25–27** — ✅ Built · 🏛️ Architectural. Tabernacle diagrams. *(`visuals/Exodus/25-27/`)*
- **Exodus 28–29** — 🆕 High · 🏛️ Architectural. The priestly garments — the ephod and the breastplate bearing twelve stones for the twelve tribes. Precise, detailed, and ties directly to the tribal material elsewhere.
- **Exodus 30** — 🆕 Med · 🏛️ Architectural. Incense altar, bronze laver, anointing oil recipe — a natural extension of the 25–27 diagram set.
- **Exodus 35–40** — 🆕 Low · 🏛️ Architectural. The tabernacle's actual construction and erection — largely repeats 25–27's content from the building side.

### Leviticus
*27 chapters. Ritual law translates unusually well into charts and cycle diagrams.*

- **Leviticus 1–7** — 🆕 High · 📊 Comparison chart. The five offerings (burnt, grain, peace, sin, trespass) — what's offered, by whom, and why, side by side.
- **Leviticus 8–9** — 🆕 Med · 🔄 Process diagram. The ordination of Aaron and his sons, step by step.
- **Leviticus 11** — 🆕 Med · 📊 Chart. Clean vs. unclean animals — a natural two-column chart.
- **Leviticus 16** — 🆕 High · 🔄 Process diagram. The Day of Atonement's precise ritual sequence — the two goats, the entry behind the veil.
- **Leviticus 23** — 🆕 High · ⏳ Calendar/timeline. The seven feasts of the LORD (Passover, Unleavened Bread, Firstfruits, Weeks, Trumpets, Atonement, Tabernacles) laid out across the year.
- **Leviticus 25** — 🆕 High · ⏳ Cyclical timeline. The sabbatical year (every 7th) and Jubilee (every 50th) — a nested-cycle diagram.
- **Leviticus 26** — 🆕 Low · 📊 Chart. Conditional blessings vs. curses.

### Numbers
*36 chapters. Numbers 32 and 34 are already built; the rest of the book is just as map-rich.*

- **Numbers 1–2** — 🆕 High · 🔢 + 🏛️ Camp diagram. The census totals and the tribes' fixed positions around the tabernacle, by compass direction — an iconic organizational layout.
- **Numbers 3–4** — 🆕 Med · 📊 Chart. Levite clans (Gershon, Kohath, Merari) and their assigned duties.
- **Numbers 7** — 🆕 Low · 🔢 Chart. Twelve tribal leaders' dedication gifts — identical items repeated 12 times; a numeric roster more than a narrative.
- **Numbers 10–14** — 🆕 High · 🗺️ Map. Departure from Sinai, the twelve spies' 40-day reconnaissance route into Canaan, and the report that triggers the wilderness sentence.
- **Numbers 20–21** — 🆕 Med · 🗺️ Map. Edom's refusal of passage, Aaron's death at Hor, the bronze serpent, and the conquest of Sihon and Og — sets up the already-built Numbers 32 map.
- **Numbers 22–24** — 🆕 Med · 🗺️ Map. Balaam's journey and his oracles overlooking the Israelite camp.
- **Numbers 26** — 🆕 Med · 🔢 Comparison chart. The second census, tribe by tribe, set against the first census in ch. 1.
- **Numbers 32** — ✅ Built · 🗺️ Map (Transjordan). *(`visuals/Numbers/32/`)*
- **Numbers 33** — 🆕 High · 🗺️ Map + ⏳ Timeline. The full 42-station itinerary of the wilderness years, named stop by stop — the natural single map/timeline that ties the whole wilderness period together.
- **Numbers 34** — ✅ Built · 🗺️ Map (Canaan's borders + tribal allotment). *(`visuals/Numbers/34/`)*
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
- **Judges (the judges' cycle roster)** — 🆕 High · ⏳ + 📊 Timeline/chart. Each of the twelve judges with their tribe, oppressor, years of oppression, and years of peace that followed — a natural chronological chart.
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
- **1 Kings 12 – 2 Kings 17** — 🆕 High · ⏳ + 📊 Parallel timeline. The kings of Israel and Judah reigning side by side, with the prophets active in each period — one of the most famous Bible infographics in existence, spanning both books.
- **1 Kings 17–19** — 🆕 High · 🗺️ Map. Elijah's travels — the Kerith Ravine, Zarephath, Mount Carmel, the 40-day journey to Horeb.
- **1 Kings 18** — 🆕 Med · 💡 + 🔄 Scene diagram. The contest on Mount Carmel between Elijah and the prophets of Baal.

### 2 Kings
*25 chapters. Continues the parallel-kings timeline above; distinct entries below.*

- **2 Kings 2–8** — 🆕 Med · 🗺️ Map. Elisha's travels and miracles across several towns.
- **2 Kings 17** — 🆕 High · 🗺️ Map. The fall of Samaria — Israel's deportation to Assyria and resettlement with foreign peoples.
- **2 Kings 18–19** — 🆕 Med · 🗺️ Map. Sennacherib's Assyrian invasion of Judah and the siege of Jerusalem.
- **2 Kings 24–25** — 🆕 High · 🗺️ + ⏳ Map/timeline. The fall of Jerusalem and the waves of deportation to Babylon — sets up Ezra and Nehemiah's return narrative.

### 1 Chronicles
*29 chapters. Chapters 1–9's genealogies are a major candidate on their own.*

- **1 Chronicles 1–9** — 🆕 High · 🌳 Genealogy. Nine chapters of genealogies from Adam through the returned exiles — the single largest genealogical block in Scripture. Candidates within it: ch. 1 (nations table, parallels Genesis 10), chs. 2–4 (Judah's line to David), ch. 6 (priestly/Levitical line), ch. 9 (post-exilic residents of Jerusalem).
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

- **Esther 1** — 🆕 Med · 🗺️ Map. The Persian Empire's extent — 127 provinces from India to Ethiopia — and the setting at Susa.
- **Esther (overall)** — 🆕 Med · ⏳ Timeline. Events span roughly a decade of Xerxes' reign with specific dates given (e.g., the 13th of Adar).
- **Esther 3–9** — 🆕 Low · 💡 Reversal diagram. Haman's plot flipped into Mordecai's triumph — a before/after contrast diagram.

### Job
*42 chapters. Mostly poetic dialogue — low visual density overall.*

- **Job 1–2** — 🆕 Low · 💡 Diagram. The heavenly council framing narrative.
- **Job 38–41** — 🆕 Med · 💡 + 🔢 Catalog. God's speech from the whirlwind catalogs creation — stars, weather, wild animals, Behemoth, Leviathan — a "catalog of creation" infographic.

### Psalms
*150 chapters/psalms. Devotional poetry — very low density for maps/timelines, but two structural candidates stand out.*

- **Psalm 119** — 🆕 Med · 🔤 Structure diagram. A 22-stanza acrostic, one stanza per Hebrew letter, 8 verses each.
- **Psalms (overall)** — 🆕 Med · 📊 Organizational chart. The Psalter's five "books," each closing in a doxology.
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

- **Ezekiel 1 & 10** — 🆕 High · 💡 Symbolic diagram. The wheel/throne vision — four living creatures and "wheels within wheels."
- **Ezekiel 4** — 🆕 High · 🔄 + 💡 Diagram. Siege sign-acts: lying on his side for a set number of days (each day representing a year) and building a model siege of Jerusalem on a clay tile — a genuinely literal diagram Ezekiel himself constructs.
- **Ezekiel 8–11** — 🆕 Med · 🏛️ Diagram. Vision of temple abominations and the glory of the LORD departing.
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
*3 chapters.*

- **Joel 1–2** — 🆕 Med · 💡 + ⏳ Sequence diagram. The locust plague's stages, escalating into the "Day of the LORD" and the Spirit poured out (quoted in Acts 2).

### Amos
*9 chapters.*

- **Amos 1–2** — 🆕 High · 🗺️ + 📊 Map/chart. Oracles against eight nations, each introduced with the repeated "for three transgressions... and for four" formula — a highly structured list that doubles as a regional map.
- **Amos 7–9** — 🆕 Med · 💡 + 📊 Sequence chart. Five visions of judgment (locusts, fire, plumb line, basket of summer fruit, the Lord beside the altar).

### Obadiah
*1 chapter.*

- **Obadiah** — 🆕 Low · 🗺️ Map. Judgment on Edom — a single short oracle, mappable but thin.

### Jonah
*4 chapters.*

- **Jonah 1–2** — 🆕 High · 🗺️ Map. Jonah's voyage — Joppa, an attempted flight to Tarshish, the storm, the fish, then Nineveh. A beloved, highly teachable map candidate.

### Micah
*7 chapters.*

- **Micah 5:2** — 🆕 Low · 💡 Conceptual. Bethlehem prophesied as the ruler's birthplace — single-verse, thematic rather than diagrammatic.

### Nahum
*3 chapters. Judgment on Nineveh — low density; geographically pairs with Jonah but too thin on its own for a separate entry.*

### Habakkuk
*3 chapters. A theological dialogue with God — low density, no strong visual candidates.*

### Zephaniah
*3 chapters.*

- **Zephaniah (Day of the LORD)** — 🆕 Low · ⏳ Conceptual. Pairs naturally with Joel's Day-of-the-LORD theme rather than standing alone.

### Haggai
*2 chapters.*

- **Haggai (temple rebuilding)** — 🆕 Low · ⏳ Timeline. Short book, ties directly into the Ezra temple-rebuilding timeline rather than standing alone.

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

- **Matthew 1** — ✅ Built · 🌳 Genealogy (three columns of fourteen). *(`visuals/Matthew/1/`)*
- **Matthew 2** — 🆕 High · 🗺️ Map. The wise men's journey from the East, and the flight to Egypt then Nazareth.
- **Matthew 3–4** — 🆕 Low · 🗺️ Map. Baptism, temptation, and the geography of the Galilean ministry base.
- **Matthew 5–7** — 🆕 High · 📊 Structural chart. The Sermon on the Mount's outline — the Beatitudes, the "you have heard... but I say" antitheses, the Lord's Prayer, the Golden Rule.
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
- **Luke 3** — ✅ Built · 🌳 Genealogy (back to Adam, 77 names). *(`visuals/Luke/3/`)*
- **Luke 9–19 (the travel narrative)** — 🆕 Med · 🗺️ Map. Luke structures a large central section of the Gospel as a single journey toward Jerusalem, naming villages along the way.
- **Luke 15** — 🆕 Med · 📊 Comparison chart. Three parables of the lost — sheep, coin, son — presented side by side.
- **Luke 22–23** — 🆕 Low · ⏳ Timeline. Passion week — cross-references the Matthew 21–27 entry.
- **Luke 24** — 🆕 Low · 🗺️ Map. The road to Emmaus.

### John
*21 chapters. Two of the strongest structural candidates in the entire NT.*

- **John — seven signs** — 🆕 High · 📊 Structural chart. The seven sign-miracles that structure the Gospel (water to wine, the official's son, the lame man, feeding the 5,000, walking on water, the blind man, Lazarus) — a famous literary-structure infographic unique to John.
- **John — seven "I am" statements** — 🆕 High · 📊 Structural chart. Bread of life, light of the world, the door, the good shepherd, the resurrection and the life, the way/truth/life, the true vine — pairs naturally with the seven signs.
- **John 13–17** — 🆕 Low · 💡 Conceptual. The Upper Room Discourse — mostly extended teaching, thin on diagrammatic content.
- **John 18–19** — 🆕 Med · 🔄 Sequence diagram. The distinct stages of the Jewish and Roman trials, as its own process diagram.

### Acts
*28 chapters. Along with Genesis/Exodus/Ezekiel/Daniel, one of the richest books in the Bible for this project — the missionary journeys are some of the best-known Bible maps in existence.*

- **Acts 1–2** — 🆕 High · 🗺️ Map. The Ascension and Pentecost, including the list of nations/languages represented in Jerusalem.
- **Acts 6–8** — 🆕 Med · 🗺️ Map. Stephen's martyrdom, the gospel's spread to Samaria, and the Ethiopian eunuch's road.
- **Acts 9** — 🆕 Med · 🗺️ Map. Paul's conversion on the Damascus road.
- **Acts 13–14** — 🆕 High · 🗺️ Map. Paul's First Missionary Journey — Cyprus and the Galatian region.
- **Acts 15** — 🆕 Med · 🔄 Process diagram. The Jerusalem Council's decision process.
- **Acts 15–18** — 🆕 High · 🗺️ Map. Paul's Second Missionary Journey — Asia Minor into Macedonia and Greece, including Philippi, Athens, and Corinth.
- **Acts 18–21** — 🆕 High · 🗺️ Map. Paul's Third Missionary Journey — centered on Ephesus, then the return to Jerusalem.
- **Acts 27–28** — 🆕 High · 🗺️ Map. The voyage to Rome and the shipwreck at Malta — a richly detailed, highly mappable nautical journey.

### Romans
*16 chapters.*

- **Romans (overall)** — 🆕 High · 📊 Doctrinal flow chart. The letter's argument arc — sin, law, grace, justification, sanctification, Israel's future, practical living — the basis of the popular "Romans Road" salvation outline.
- **Romans 5** — 🆕 Med · 📊 Parallel chart. Adam and Christ compared — "as in Adam all die, in Christ all live."
- **Romans 9–11** — 🆕 Med · 💡 Conceptual. Israel, the Gentiles, and the olive-tree metaphor.

### 1 Corinthians
*16 chapters.*

- **1 Corinthians 12** — 🆕 High · 💡 + 📊 Diagram. The body of Christ / spiritual gifts — many members, one body. A perennially popular diagram subject.
- **1 Corinthians 15** — 🆕 Med · ⏳ Sequence. The resurrection order — "Christ the firstfruits, afterward they that are Christ's."

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
- **Ephesians 2** — 🆕 Med · 💡 Conceptual. Grace through faith, and the "dividing wall" between Jew and Gentile broken down.
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

- **2 Thessalonians 2** — 🆕 Low · ⏳ Timeline. The man of sin and the Day of the Lord's sequence — pairs with the 1 Thessalonians entry and, further out, Daniel 9 and Revelation.

### 1 Timothy
*6 chapters.*

- **1 Timothy 3** — 🆕 Med · 📊 Comparison chart. Qualifications for bishops and deacons, listed side by side.

### 2 Timothy
*4 chapters. A personal farewell letter — no standout candidate.*

### Titus
*3 chapters.*

- **Titus 1:5–9** — 🆕 Low · 📊 Chart. Elder qualifications — parallels and cross-references 1 Timothy 3.

### Philemon
*1 chapter. A single-chapter personal letter — no infographic candidates.*

### Hebrews
*13 chapters. Exceptionally strong — the whole book is essentially structured for a comparison chart.*

- **Hebrews (the "better than" argument)** — 🆕 High · 📊 Comparison chart. Christ shown better than angels, Moses, Aaron's priesthood, and the old covenant — the entire epistle's argument is a ready-made chart.
- **Hebrews 9** — 🆕 High · 🏛️ Architectural. The earthly tabernacle vs. the heavenly sanctuary — ties directly into the already-built Exodus 25–27 tabernacle diagrams.
- **Hebrews 11** — 🆕 High · ⏳ + 📊 Timeline/chart. The "Hall of Faith" — a roughly chronological list of Old Testament figures and their acts of faith. One of the most popular infographic subjects in the NT.

### James
*5 chapters. Practical wisdom letter — low density.*

- **James 1** — 🆕 Low · 🔄 Process diagram. Trials → patience → maturity.

### 1 Peter
*5 chapters. Low-to-medium density.*

- **1 Peter 2** — 🆕 Low · 💡 Conceptual. Living stones / spiritual house metaphor.

### 2 Peter
*3 chapters.*

- **2 Peter 1:5–7** — 🆕 Med · 📊 Chain/ladder diagram. Faith → virtue → knowledge → self-control → perseverance → godliness → brotherly kindness → love — a classic "ladder" infographic.

### 1 John
*5 chapters.*

- **1 John (tests of genuine faith)** — 🆕 Med · 📊 Chart. The repeated "by this we know" tests of fellowship and true faith.

### 2 John
*1 chapter. No infographic candidates.*

### 3 John
*1 chapter. No infographic candidates.*

### Jude
*1 chapter.*

- **Jude (OT judgment examples)** — 🆕 Low · 📊 Chart. Angels, Sodom, Cain, Balaam, Korah — a small chart of judgment precedents.

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
- **Revelation 21–22** — 🆕 High · 🏛️ Architectural. The New Jerusalem — precise measurements (12,000 furlongs cubed, wall dimensions, twelve named gates and foundations). A spectacular architectural-diagram candidate that rivals Ezekiel 40–43 and the tabernacle.
