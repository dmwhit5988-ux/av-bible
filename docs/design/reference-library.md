# The Reference library

The Reference shelf holds pages that aren't tied to a verse: maps, timelines, plans and charts that a listener opens while the narration carries on. This doc plans the pages after the OT family tree, and the parts they share.

## Status

Proposed on 2026-10-27. Built so far: the shelf, and pages 1 and 2 as first cuts.

**The shelf.** The header's **Reference** button lists `REFERENCES` in `web/js/app.js`. An entry opens full screen over the app, framed under a bar with ← Back and ↗:
- the passage and narration carry on underneath;
- ↗ opens the page on its own, at an address that can be shared;
- turning a phone to landscape doesn't put the stage in fullscreen while a panel is open (`onOrientationChange`), because API fullscreen shows only `#stage-wrap`;
- an Escape the page handles itself (`e.defaultPrevented`) doesn't also close the frame.

Its entries are the OT family tree and the Tabernacle. The V6 heir spine, the 1–2 Chronicles tree and the OT timeline stay deployed and unlinked ([reference-charts.md](../reference-charts.md)).

**Generated pages.** A Python generator writes each page into the flat `web/visuals/reference/` folder, as `generate_ot_family_tree_svg.main` writes the tree's `.svg`, `.json` and `.html`. Publish commits the pages with the rest of `web/visuals`.

**Each page is the face of a reusable data module.** The 1 Chronicles 1–9 and Matthew 1 pictures are cameras over the tree the wall chart draws. They redraw it from `chronicles_tree` and `ot_grafts`; they don't reuse the chart's SVG. The pages below work the same way, so building a reference also builds the base for the backlog chapters it serves.

Four lenses proposed the pages: reader (what a listener needs), author (what unlocks the backlog), craft (touch and performance) and canon (reach across the Bible). Each entry names the lenses that backed it. A reviewer then checked every name and claim against the code.

**The owner's answers (2026-10-27).**
- **The OT timeline stays unlinked.** It is useful as data, but it is the genealogy laid on years, and a timeline should stand apart from the tree. Its left part, the specific lives from Adam on, is the kind of thing a timeline page should show (pages 6 and 9).
- **The Israel atlas is the first map** (page 7), ahead of Paul's journeys, because it serves more of the upcoming work.
- **The Tabernacle settles on one model** (`sanctuary.py`), and the Numbers 1–4 pictures are regenerated onto it.
- **Page 1, the tree, is built first.**

Pages keep their numbers as names; the tier says when.

**At a glance.** Effort runs S to XL; files are what a page adds to the deploy.

| # | Page | Tier | Effort | Files | Its data module |
|---|---|---|---|---|---|
| 1 | OT family tree: tap, trace, jump | First | M | +1 | stable ids, `verse_refs.py` |
| 2 | The Tabernacle (camp, Levites, garments, offerings) | First | L | 3 | `sanctuary.py` |
| 3 | Paul's journeys and the assemblies | Next | M for Journey 1, then L–XL | 3 | `journeys.py`, `gazetteer.py` |
| 4 | Kings and prophets | First | M | 2 | `prophets.py`, `timeline_axis.py` |
| 5 | The twelve tribes (and the Twelve) | First | S | 1 | `tribes.py` |
| 6 | Genesis 5 and 11: overlapping lives | Next | S | 1 | `timeline_axis.py` |
| 7 | Land of Israel atlas | First (the first map) | XL | 3 | `gazetteer.py` (Levant) |
| 8 | Solomon's Temple | Next | L | 3 | `sanctuary.py` |
| 9 | When is this? The whole-Bible timeline | Next | L | 2 | `setting.py` |
| 10 | The wilderness journey (Numbers 33) | Next | M | 2 | `wilderness.py` |
| 11 | Measures and money | Next | S | 2 | `measures.py` |
| 12 | The sacred year | Next | M | 1 | `sacred_calendar.py` |
| 13 | The Bible world, Egypt to Persia | Later | XL | 3 | `gazetteer.py` (Mesopotamia) |
| 14 | Jerusalem through the Bible | Later | L | 3 | `jerusalem.py` |
| 15 | Life of Jesus: the Gospels side by side | Later | XL | 2 | `harmony.py` |
| 16 | Ezekiel's temple and the sanctuaries compared | Later | L | +1 | `sanctuary.py` |
| 17 | Name finder | Later | M | 2 | `pronunciations.json` |

## Shared machinery

### The viewer: `reference_viewer.py`

`reference_viewer.page()` writes every chart's page, the OT timeline's included (`data=False`). It is inlined into each `.html`, so it costs no files. [reference-charts.md](../reference-charts.md) describes what it does today:
- pinch and pan;
- a sidecar (`family_tree_data.sidecar`) with ranked search over names, aliases and notes;
- the held selection outline, with its card as a bottom sheet or side panel;
- Line to Adam and verse chips;
- `#id` and `#at` in the address, with ↗ reading the frame's address;
- `viewport-fit=cover` with safe-area padding.

It still needs:

- **A settling camera.** The tree is one 26,946 × 16,736 px `<svg>` scaled by CSS, larger than iOS's biggest layer. The CSS transform should run only while a finger moves. About 120 ms after the last move, the camera goes into the `viewBox` so the vector redraws sharp. Refit on resize and rotation. The owner found the iPhone smooth without it, so it waits for the iPad test.
- **Detail bands.** The generator writes `<g data-lod>` bands, and all but one get `display:none`.
  - **Maps.** Each band's labels are placed in Python with `svg_map_camera.layout` and `clash` at the band's own scale, so they never touch. Both assume one 1024 × 576 frame today (`SAFE`, the HUD), so they are generalised to take the band's extent.
  - **The tree.** Its names sit inside boxes that `arrange` and `place` already keep apart, so its far band is the `REGIONS` titles and the heads they name.
  - **Live text.** The tree's near band holds all 1,254 boxes, far over `svg_chronicles_world.IPAD_NAMES` (268 texts) and `IPAD_BOX_RECTS` (1,050 rects and texts). So the viewer would also hide the boxes outside the view, using the sidecar's boxes. Those budgets were measured on animated camera files, so a static page is measured on the iPad before they are taken as its limit.
- **Layer chips and tours.** Chips toggle `<g data-layer>` groups. The reader steps a tour with Prev/Next. Routes and genealogies draw once in SMIL (`fill="freeze"`), and a scrubber seeks with `setCurrentTime()`.
- **Timelines.** A pinch stretches only the time axis and JS re-places the bars, so text is never CSS-scaled. Lanes are packed once in Python, in years, so JS only rescales. Its labels get their own clash test in JS, because PIL's measurements stay in Python. On a portrait phone, time runs down the screen.
- **Inline-SVG icons** instead of emoji glyphs.

### The passage protocol

Built with page 1.

- **Out.** "Open in Theoria" under a verse preview posts `{type: "theoria:goto", book, chapter, verse}` to `location.origin`. `app.js` then:
  - checks `e.origin`, `e.source` (the frame's `contentWindow`), `BOOKS` and `chaptersIn`, and closes the view;
  - sets the book, calls `populateChapters`, sets the chapter and calls `loadChapter({resetStage: false})`;
  - checks the verse against `passage.verses`, and calls `player.jumpTo(index)`;
  - focuses Play.

  `loadChapter` calls `player.stop()`, so going there stops any narration that is playing. There is no autoplay: `player.unlock()` must run inside a gesture in the app's own document, and a posted message isn't one. Each `loadChapter` takes a number (`loadSeq`), and only the newest may touch the screen, so a chapter roll still fetching when the jump arrives can't land on top of it.
- **In.** The app opens a page at `#at=<Book>.<c>.<v>`, so the page starts on the names that verse speaks, or failing those, the families whose passage it falls in.
- **Standalone.** A page opened outside the app shows the verse preview without "Open in Theoria" until the ROADMAP deep links exist.
- **Reading.** The page fetches the verse text from `/bibles/WEB/` itself, so it costs no files. Linking a verse's picture from `/visuals/manifest.json` is not built yet.

### Shared data modules

These are Python only, so they cost no deploy files.

- **`verse_refs.py`** parses warrant strings and `N.ref`, and fails the build on any ref that `passages.verse_numbers()` rejects. 127 of the tree's 296 refs are a bare `c:v` that means 1 Chronicles, so a module names its default book.
- **Stable ids**: slugs from the data, asserted unique on every build. Never `N.key`, which rebinds. `World` builds its own tree, so these ids are also how its verses map onto the chart's boxes.
- **`gazetteer.py`**: one site table and one line store.
  - **Each site** has its WEB spellings, a lat/lon from one Wikidata or Wikipedia point fact with its source, a certainty (known, probable, unknown) and refs.
  - **It takes over** `acts_geography.SITES`/`SERMON_SITES`, `generate_acts1314_svg.CITIES`, `generate_acts1518_svg.CITIES`, `generate_genesis10_svg.CITIES`, `generate_tribal_maps.CITIES32` and the geometry of `generate_tribal_maps`. It re-exports the old names, so Numbers 32 and 34, `acts_geography` and the eight generators that take its colours or `MapFrame` import unchanged.
  - **Duplicates** are dropped: the two Cyprus outlines, and `PELOPONNESE`, `AEGEAN_SHORE` and `FAR_ISLANDS`, which copy `generate_acts1518_svg`'s `PELOPONNESE`, `MED` and `ISLANDS`.
  - **Disagreements** are settled: Tarsus (24 km apart) and Lystra (4 km).
  - **Schematic points** enter as unknown. These are `SERMON_SITES`' wilderness points.
- **Point facts only.** Today only `acts_geography`'s own coasts, lakes, rivers, sites and roads are point facts: southern Asia Minor round to Ras Naqoura, and Cyprus. The rest are atlas-simplified:
  - `generate_tribal_maps`: `COAST` south of Ras Naqoura, the lakes, the Jordan, `COAST_WEST`, the gulfs and the tribal edges;
  - `generate_acts1518_svg`: `MED`, `PELOPONNESE` and `ISLANDS`, with `acts_geography.LIBYA_SHORE`;
  - `generate_genesis10_svg`: its seas.

  No reference page draws any of these at any zoom. Each is rebuilt from point facts before the first page that needs it.
- **`sanctuary.py`** holds parts in cubits, each figure flagged stated, derived or not given.
- **`measures.py`** holds units and a `CUBIT` in `svg_figures` units, which `svg_figures` lacks. The only `CUBIT` today is `generate_genesis69_svg`'s px per cubit.
- **`timeline_axis.py`** lifts `Scale`, `year_map`, `lanes` and `draw_rail` from `generate_ot_timeline_svg` and adds signed BC/AD years. Today AD 30 would print as "-30 BC" (`chronology.bc` is 4004 − AM). The new axis has no year 0.
- **`svg_surface.SvgCanvas.group()`** gains `id`, `class` and `data`.

Each row has a certainty flag, drawn the same way everywhere: a hollow dot or a dashed line.

### Labels and notes

Reference pages aren't narrated, so short labels and numbers belong on the drawing, as the wall chart's box notes do. Sentences go in the tap card, from the data module. That way the module can still feed a caption-free per-verse camera, which redraws from it rather than reusing the page's SVG. Labels use WEB's words ("assemblies", not "churches"). Cards are per item; there is no notes switch.

### Files and registration

- **Cost.** A page costs 1–3 files: the `.html`, plus an `.svg` and a `.json`, which small pages inline. The 17 pages add about 36 files (35, plus `index.json`) to today's 8. Against 5,802 today (`count_deploy_files()`), that leaves about 14,160 under `DEPLOY_FILE_LIMIT`.
- **Naming.** The folder stays flat. `build_manifest._scan_files` reads any subfolder of `web/visuals/reference/` as a chapter folder and would key its SVGs; `test_registry` reads only numbered folders. No `Book_c_v` names, and no `.xml`.
- **Registration.** Today an entry is a hand-committed line in `REFERENCES`.
  - Proposed instead: the generators write `reference/index.json` (title, blurb, href, order, chapters covered), and the app fetches it with `cache: "no-cache"`.
  - A new page then ships through Publish alone, and the list can show the current chapter's pages first.
  - The switch rewrites CLAUDE.md, `docs/reference-charts.md` and `docs/architecture.md` in the same change, because they name `REFERENCES` as the list.
- **Checks.**
  - A reference owner block beside `svg_generators.json`.
  - Tests that every ref resolves, ids are unique, a page has at most 3 files and each band keeps its text budget.
  - Moving data out of a generator means regenerating and diffing the published SVGs: `git diff --stat web/visuals` should come back empty. No test does this today; `test_svg_freeze` tests `svg_freeze`.
  - The audio-timed cameras (Numbers 34, Acts 13–14, 1 Chronicles, Matthew 1) change only on purpose.

## The pages

Effort runs from S to XL. XL means the work is mostly new, sourced data. Files are what a page adds to the deploy.

### First

**1. OT family tree: tap, trace, jump.** M · +1 file · all four lenses.
- **Built 2026-10-27, as a first cut** ([reference-charts.md](../reference-charts.md#the-old-testament-family-tree)): `reference_viewer.py`, `family_tree_data.py`, `verse_refs.py` and the `theoria:goto` message in `web/js/app.js`. It differs from the plan below in four ways:
  - Taps are hit-tested against the sidecar's boxes, so the SVG carries no `data-id` and is unchanged.
  - World's and `matthew_tree`'s boxes are matched to the chart's by walking the trees down together (`family_tree_data.pair`), not by stable id.
  - Not built yet: the Jesus chip (Matthew's line on to Jesus with Luke's beside it), the settling camera, the detail bands and the culling. The iPhone handles the sheet well without the last three.
  - A box's verses reach no further than its own ref, 1 Chronicles 1–9, Matthew 1:1–17 and Genesis 5 and 11.
- **Shows:**
  - Search ranks whole names first and tells namesakes apart ("Azariah, son of Ahimaaz"), then eases to the box.
  - A person's card shows names, parents, `N.gen`, the Ussher year where `chronology.bind` has one, the note and verse chips.
  - Line to Adam lights the ancestry.
  - A Jesus chip runs Matthew's line on to Jesus (`matthew_tree`, as the timeline does) and sets Luke's beside it (`generate_luke3`), marking where the two meet and part.
  - Opened from 1 Chronicles 1–9 or Matthew 1, it frames that verse's names.
- **Reuses:** `chronicles_tree.build(ot=True)`, `ot_grafts` and `svg_family_lines.Geometry`. Verses come from:
  - `N.ref`;
  - `svg_chronicles_world.World.lit`, reversed. World builds its own tree in the regions layout, so its nodes are matched by stable id;
  - `matthew_tree.MatthewLine.lit`;
  - `generate_genealogy.G5_LINE`/`G11_LINE`.
- **New:** stable ids, `data-id` on boxes, `Old_Testament_family_tree.json`.
- **Feeds:** Genesis 25 and 36, Ruth 4, Ezra 2, Nehemiah 11–12, Jude.
- **Risks:**
  - iPhone performance is unmeasured, so measure the settling camera and the culling on a device.
  - Adding ids must not move the layout; diff the SVG.
  - Verses come from the per-verse maps, never from name matching.

**2. The Tabernacle.** L · 3 files · all four lenses.
- **Built 2026-10-27, as a first cut** ([reference-charts.md](../reference-charts.md#the-tabernacle)): `sanctuary.py`, the one model; the Exodus 25–27 plan and the Numbers 1–4 courts redrawn onto it; and `generate_tabernacle_reference.py`'s sheet with the plan, the measurements, the camp and the Exodus drawings, and a card for each part. It differs from the plan below:
  - The court kept is `draw_plan`'s, but the Exodus 25–27 pictures still changed: the pillars are now sixty, one every five cubits, with the gate's four at 20–35, and the drawings' words are WEB's (brass, lamp stand, sea cow hides).
  - The elevations are the Exodus 25–27 insets, reused whole on the sheet, not new drawings.
  - Not built yet: the Garments tab, the offerings of Leviticus 1–7 (the "Used" tab), the tours, and incense-altar and basin drawings.
- **Shows:**
  - The court and tent in plan at cubit scale. Each furnishing opens its elevation, materials and counts.
  - Layers: dimensions, the Numbers 2 camp, and the Levite clans and loads of Numbers 3–4.
  - A Garments tab dresses the high priest in `svg_priest.WEARING_ORDER`.
  - A Used tab tables the five offerings of Leviticus 1–7 (what is brought, what burns, who eats) with their verses.
  - Cards group verses as commanded (Exodus 25–27, 30), made (35–39), set up (40) and used (Leviticus 16, Hebrews 9).
  - Tours: gate to ark, and Exodus 40:18–33 raising each piece once.
- **Reuses:** `generate_tabernacle` (`draw_plan`, `INSETS`, `hl_*`, palette, primitives), `svg_priest`, and the Exodus 28 and Numbers 1–4 tables.
- **New:**
  - `sanctuary.py` replaces the literals in `draw_plan` and the `hl_*` overlays.
  - It settles three disagreeing courts:
    - `draw_plan` puts the bronze altar 32–37 cubits inside the gate, the laver at 50 and the tent 10 cubits from the west curtain;
    - `generate_numbers1_2_svg.draw_tabernacle` has 12–17, 27 and 14;
    - `generate_numbers3_4_svg.draw_ring` is a third, a schematic 38 × 70 px court with no altar or laver.
  - Incense-altar and laver insets.
- **Feeds:** Exodus 29–30 and 35–40, Leviticus 1–9 and 16, Numbers 7 (about 19 chapters). The built Exodus 25–27 and Numbers 1–4 pictures move onto one model, and the Temple builds on it. Hebrews draws its own schematic tent, not the plan, and stays as it is.
- **Risks:**
  - The furniture's positions are conventional, and the lampstand and laver are unmeasured; the cards say so.
  - The published Numbers 1–4 pictures change, and (as built) the Exodus 25–27 pictures' pillars and wording too; see the Built note above.

**7. Land of Israel atlas.** XL · 3 files · all four lenses.
- **Shows:** Dan to Beersheba, with 150–250 sites. One layer at a time: the allotments with the cities of refuge, David and Solomon, the divided kingdom, Jesus' day, Numbers 34.
- **Interactions:** alias search (Luz/Bethel), place cards with certainty and verses by book, "In this chapter" chips, distances.
- **Reuses:** `generate_tribal_maps.TRIBE_RINGS`, for which shares border which. Its edges are an atlas approximation and are not drawn.
- **New:**
  - The Levant half of the gazetteer from point facts: the coast from Ras Naqoura to the Delta, Galilee (7 points today), the Dead Sea, Huleh and the Jordan.
  - Tribe edges redrawn through the border towns Joshua 15–19 names, each a point fact, and drawn soft.
  - Kingdoms as soft hulls round named sites, as on page 13.
  - Homonym rules (the Ramahs, Aphek).
- **Feeds:** about 99 OT and 19 NT chapters, plus pages 10, 14 and 15.
- **Risks:**
  - The atlas's cost is its sites, not its coast.
  - Borders are reconstructions, drawn soft.
  - Ai, Emmaus and Bethsaida are uncertain.
  - The Dead Sea is drawn at high water, as `acts_geography` draws lakes, and the legend says so.

**4. Kings and prophets.** M · 2 files · all four lenses.
- **Shows:**
  - Judah and Israel as two lanes of reign bars from Saul to the exile, with judges above.
  - Interregna are hatched and overlaps stacked. Prophets stand beside the reigns their opening verses name, and foreign kings appear in WEB spelling.
  - A year line reads who reigned and who prophesied.
  - A king's card gives his years, the length the text states, his mother, the verdict verse, Kings and Chronicles side by side, and his place on the tree.
  - An Ussher/Thiele chip switches the dates.
- **Reuses:** `chronology.BIND` (41 reigns with warrants; Ussher's interregna are the gaps between them), `locate`, `MODERN`, `timeline_axis`.
- **New:**
  - A realm field; `draw_lanes` puts Athaliah in Israel today.
  - Reign lengths as fields.
  - David's reign (2 Sam 5:4). `BIND` holds him as a life.
  - `prophets.py`: rows keyed to the reigns their opening verses name (Isa 1:1, Hos 1:1; Jonah via 2 Kgs 14:25). Only Jeremiah, Ezekiel, Daniel, Zephaniah and Zechariah are on the tree, and they are found with `locate`. Isaiah, Hosea, Amos, Jonah and the rest have no join on it.
  - About 39 sourced Thiele rows; `MODERN` has 9.
- **Feeds:** about 70 chapters, including the ROADMAP parallel-kings camera, 2 Kings 18–25 and 2 Chronicles 10–36.
- **Risks:**
  - This is the OT's most contested chronology. Ussher is named as the house count, and the two counts are never mixed.
  - Joel, Obadiah, Nahum, Habakkuk and Malachi stay undated.
  - Mixed verdicts stay mixed.

**5. The twelve tribes.** S · 1 file · author, canon.
- **Shows:** a row per tribe. Columns: mother and birth order, Genesis 49, Deuteronomy 33, the Numbers 1 and 26 counts, princes, camp and march, breastplate stone, territory, Ezekiel 48, Revelation 7. Re-sorting by any list glides the rows, which shows how the lists differ. The same component later lays the four lists of the Twelve side by side (Matt 10:2–4, Mark 3:16–19, Luke 6:14–16, Acts 1:13).
- **New:** `tribes.py` replaces five scattered tables. It adds the Numbers 26 counts and a test that the totals match (603,550; 601,730).
- **Feeds:** Genesis 49, Numbers 7 and 26, Joshua 13–19, Ezekiel 48, Revelation 7.
- **Risks:**
  - Low. The lists are shown as they differ, never normalised.
  - The breastplate column is an inference, because Exodus 28:21 gives no order (`generate_exodus28_svg` uses birth order). Territory is a reconstruction. Both carry the certainty flag.

### Next

**3. Paul's journeys and the assemblies.** M for Journey 1, then L to XL as the coasts are rebuilt · 3 files · all four lenses.
- **Shows:**
  - Four routes (Acts 13–14, 15:36–18:22, 18:23–21:17, 27–28), with sea legs drawn apart from land legs.
  - Layers: the seven assemblies (WEB's word), the letters' recipients, and where a letter says it was written (1 Cor 16:8).
  - A step bar draws each leg once with its verse.
  - City cards list visits, letters and assembly.
  - Opened from Acts, it starts on the current leg.
- **Reuses:**
  - `acts_geography`;
  - `generate_acts1314_svg.LEGS`;
  - `generate_acts1518_svg.LEGS`, `STAGES`, `OTHER_ROADS` and `SHUT_DOORS`;
  - `svg_map_camera.Projection`, widened west and north.
- **New:** `journeys.py` holds the legs. Journey 2's land legs are straight lines between cities today, so they get roads from point facts (the Via Egnatia from Neapolis to Thessalonica). New sites:
  - Revelation 2–3 and the letters: Smyrna, Pergamum, Thyatira, Sardis, Philadelphia, Laodicea, Colossae, Patmos and Nicopolis.
  - Journey 3: Assos, Mitylene, Chios, Samos, Trogyllium, Miletus, Cos, Rhodes, Patara, Tyre and Ptolemais.
  - The voyage to Rome: Adramyttium, Myra, Cnidus, Salmone, Fair Havens, Lasea, Phoenix, Clauda, Malta, Syracuse, Rhegium, Puteoli, The Market of Appius, The Three Taverns and Rome.

  Patara and Myra are coast points in `MAIN_COAST` today, not sites.
- **Stages:**
  1. Journey 1, on `acts_geography`'s point facts as they stand.
  2. Journeys 2 and 3, once Greece and the Aegean are rebuilt from point facts.
  3. Rome, once Crete, Sicily, Italy and Malta exist as point facts. The map stops at 20.6°E today, and Crete is only the coarse atlas trace.
- **Feeds:** Acts 19–21 and 27–28 (ROADMAP Next), Acts 1–2 and 6–9, Revelation 2–3, Titus and Philemon.
- **Risks:**
  - `MED`, `AEGEAN_SHORE`, `PELOPONNESE` and the islands are atlas traces, so no stage draws them.
  - The Acts 27 course is inferred, so it is drawn dashed.
  - Ephesus and Miletus have silted up since. The map draws the modern coast, and their cards say so.

**6. Genesis 5 and 11: overlapping lives.** S · 1 file · craft; author lists it as a follow-on.
- **Shows:** lifespan bars from Adam to Abraham, using WEB's numbers. A year cursor lights every life alive at that point. A chip sets Abram's birth at Terah's 70 or 130 (`chronology.ABRAM_BIRTH`). The built Genesis 5 and 11 pictures already draw the bars (`generate_genealogy.py`). The page adds the cursor, one axis across both chapters, and the chip.
- **Reuses:** `chronology.GEN5`, `GEN11` and `spine()`, unified with `generate_genealogy.G5_LINE`/`G11_LINE`. `spine()` reads `ABRAM_BIRTH` as a module switch, so it takes the age as a parameter.
- **Why not first:** the built pictures already show the bars, and page 4 proves `timeline_axis` on its own. The draft ranked it first for that axis; the review moved it here.
- **Risks:** say "lives overlapped", never "met".

**8. Solomon's Temple.** L for a Kings-first cut · 3 files · all four lenses.
- **Shows:**
  - A plan and long section in cubits: the 60×20×30 house, the 20-cubit inner room, side chambers 5, 6 and 7 wide, the cherubim wing to wall, Jachin and Boaz, the Sea, the stands and the altar.
  - A Tabernacle overlay showing that the house doubles the tent.
  - A cut plane.
  - Kings and Chronicles side by side, with a badge where they differ: pillars 18 or 35 cubits, the Sea 2,000 or 3,000 baths, the porch 120 cubits in 2 Chr 3:4.
- **Reuses:** `sanctuary.py`, `generate_tabernacle`'s `sheet` and `cherub_parts`, `svg_figures.pillar` and `ox`.
- **New:** both readings per part. Drawings of a spread-wing cherub, the Sea, the wheeled stands, and palm and flower symbols, added to `svg_figures.py` (or beside `cherub_parts`) so the 1 Kings 6–7 pictures can reuse them.
- **Feeds:** 1 Kings 6–8, 1 Chronicles 22–29, 2 Chronicles 2–5, Ezra 3–6, Haggai.
- **Risks:**
  - The elevations are partly conjectural. The roof, the windows, the stands' panels and the capitals (5 or 3 cubits) aren't settled by the text, so they are drawn plain, dashed and marked reconstructed.
  - The drawing follows the verses, never a published reconstruction.

**9. When is this? The whole-Bible timeline.** L · 2 files · reader, canon.
- **Shows:**
  - Creation to Acts on a page sized for a phone, not the 65,030 px ribbon.
  - Eras (`chronology.ZONES`), events, and a band per book where its own text sets it.
  - Undated books in their own lane.
  - It opens on "you are here", and the bands link on to the detailed pages.
- **New:** `setting.py`, 200–300 rows mapping book ranges to years with warrants and soft ends, plus the NT in AD.
- **Feeds:** Judges, Ezra to Esther, Daniel 9, Luke 1–2, Acts.
- **Risks:**
  - Early dates are contested (215 or 430 years in Egypt).
  - Letters are placed only where the text ties them to an event.

**10. The wilderness journey (Numbers 33).** M after page 7 · 2 files · author, craft, canon.
- **Shows:** the 42 stations above a forty-year strip of the text's dates. Dragging the strip walks the route.
- **Reuses:** `acts_geography.EDOM_WAY`, and the identified sites in `SERMON_SITES` (Kadesh, Ezion Geber, the Arnon). Its schematic wilderness points (the crossing, Marah, Elim, Sin, Sinai, Hazeroth) are not reused as dots, and `STORY`'s route appears only as the dashed traditional chain.
- **New:** `wilderness.py`, plus the gulfs from point facts.
- **Feeds:** Numbers 33 (ROADMAP Next), Exodus 12–19, Numbers 10–24, Deuteronomy 1–3.
- **Risks:**
  - Most stations, and Sinai, are unidentified. They are beads on a dashed chain, never dots at invented coordinates.
  - The route is labelled traditional.

**11. Measures and money.** S · 2 files · reader, canon.
- **Shows:** lengths against a man, objects to scale (the ark, the tent, Goliath), weights, volumes and coins, with the text's own equivalences (Exod 30:13, Ezek 45:12, Matt 20:2).
- **New:** `measures.py`, with a `CUBIT` in `svg_figures` units, and a unit-to-verse index in WEB's words.
- **Feeds:** the generators that place `svg_figures` objects to scale, and 132 chapters that name units.
- **Risks:** modern values are ranges with the assumption stated. No currency conversion.

**12. The sacred year.** M · 1 file · all four lenses.
- **Shows:** a dial of WEB's month names with the farming year, the Leviticus 23 feasts, dated events and a Jubilee grid.
- **New:** `sacred_calendar.py`.
- **Feeds:** Exodus 12; Leviticus 16, 23 and 25; Numbers 28–29; Esther; Haggai; John's feasts.
- **Risks:** months are approximate ("about March–April").

### Later

These wait on the gazetteer, `sanctuary.py` or the AD axis.

**13. The Bible world, Egypt to Persia.** XL · 3 files · reader, author, canon.
- **Shows:**
  - Era layers from the patriarchs to Persia.
  - Genesis 10's nations, from `generate_genesis10_svg.CITIES`.
  - The journeys of Abram and Jacob, the deportations and the returns.
  - Cards for nations, listing their oracles.
- **New:** the Tigris, the Euphrates and the Gulf head, from point facts.
- **Feeds:** about 93 chapters, including Genesis 12–50.
- **Risks:**
  - Empires are soft hulls round named sites, never atlas traces.
  - The Gulf shore has moved since Ur's day.

**14. Jerusalem through the Bible.** L · 3 files · reader, author, canon.
- **Shows:**
  - A schematic plan with era layers.
  - Tours of Nehemiah 3's gates in the text's order, the choirs of 12:31–39, and Holy Week.
- **New:** `jerusalem.py`.
- **Feeds:** about 39 chapters.
- **Risks:**
  - The walls are disputed, so they are drawn schematically and never traced from excavation plans.
  - Golgotha is shown as a traditional site.

**15. Life of Jesus: the Gospels side by side.** XL · 2 files · reader, author, canon.
- **Shows:**
  - About 180 events in one common arrangement, with a column per Gospel and the places on the atlas.
  - A Herods and rulers panel (canon's separate idea), marking which family joins the text states and which come from Josephus.
- **New:** `harmony.py`, built from the WEB text. A public-domain harmony guides the order only.
- **Feeds:** about 55 chapters.
- **Risks:** the order is interpretive. Each Gospel keeps its own sequence, and disputed alignments are flagged.

**16. Ezekiel's temple and the sanctuaries compared.** L · +1 file on page 8 · craft, canon, reader.
- **Shows:**
  - Ezekiel 40–43 as a measuring walk with the reed of six long cubits, and its six gates drawn from one module.
  - The tent, Solomon's house and Ezekiel's on one grid.
- **Risks:** the side chambers of 41:5–11 are drawn dashed.

**17. Name finder.** M · 2 files · reader.
- **Shows:** each of the 3,152 entries in `pronunciations.json` (a few, such as "Spirit", aren't names), how Theoria says it, the chapters it appears in (from a scan of the WEB text, because an entry's `ref` is only its first occurrence), and links into the other pages.
- **Risks:**
  - It counts words, not referents.
  - It would make the house respellings public.

## What stays out

- **The OT timeline sheet as a linked page.** It is the genealogy laid on years, and the owner wants a timeline that stands apart from the tree. Pages 4, 6 and 9 do that job. It stays deployed and unlinked as data, with the V6 and 1–2 Chronicles charts.
- **Herod's temple as a page.** Scripture gives almost nothing (John 2:20, Acts 3), and the platform can't be traced from plans. At most it appears as a dashed schematic in page 16, credited to Josephus and the Mishnah.
- **Separate camp, Herods and Daniel pages.** They fold into pages 2, 15, 9 and 13.
- **A Revelation structure chart.** It serves only one book, so it waits.
- **Map tiles or a CDN map library.** The app uses no CDNs, and no line may come from OpenStreetMap, Google or an atlas.
- **Septuagint or Samaritan numbers.** WEB only. Ussher and Thiele are two chronologies of one text, not two translations.
- **Modern-currency or Gregorian conversions.** They mislead.
- **Autoplaying tours, a speed control, reduced motion, a notes toggle, still images** (D4–D6).
- **A file per place, person or event.**
- **Terrain cross-sections and a narration-following highlight.** These wait: the first for sourced spot heights, the second for a `theoria:verse` message.

## Open questions

Answered on 2026-10-27: which map comes first (the Israel atlas), whether to regenerate Numbers 1–4 onto one Tabernacle model (yes), and whether to link the OT timeline now (no). See Status.

1. Is this the right split: short labels and numbers on the drawing, sentences in the card?
2. For the kings, use Ussher with a Thiele rail (about 39 rows to source), or Ussher only?
3. For traditional sites (Sinai, the Exodus route, Golgotha), show one reading labelled "traditional", or only what is known?
4. Should Herod's temple appear as a dashed schematic credited to Josephus, or should the page stick to Scripture?
5. May a public-domain harmony (Robertson 1922, or Stevens and Burton) guide the order of the Gospel events?
6. May the name finder make the house respellings public?
7. Should a generated `index.json` replace the hand-edited `REFERENCES`?
