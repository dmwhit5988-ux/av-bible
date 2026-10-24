# Roadmap

**Now** is the current focus, **Next** the next one to three months, and **Later** has no date.
- The content backlog is the catalog, [docs/content-catalog.md](docs/content-catalog.md).
- Long-form designs live in [docs/design/](docs/design/).
- The Studio's phases are designed in [docs/studio.md](docs/studio.md).

**Recently done:** Azure TTS beside edge-tts (2026-10-18). Names can be spoken from their IPA on Azure (`use_ipa`, ▶ IPA in the Pronunciation tool), and the Audio tool picks Edge, Azure for verses with IPA names, or Azure for everything, with a free-tier meter ([docs/pronunciation.md](docs/pronunciation.md#ipa-through-azure)). edge-tts had to go to 7.3.x the same day: Microsoft began refusing older versions' token around 2026-10-13, so every verse fell back to SAPI. Before that, the cleanup of 2026-10-16/17 (Step 0, WS1–WS7): WEB only, the simpler web app with its "isn't illustrated yet" pointer, no stills, shared pictures (D17), the Theoria Studio shell, a content-only Publish and these docs. Its last step, WS4f / D7(c), serves `web/` directly: `visuals/` and `bibles/WEB` moved into `web/`, `wrangler.toml` points at `./web` with `web/.assetsignore` beside it, `deploy_bundle/` and `prepare-deploy.ps1` are gone, and Publish is two steps (manifest, then commit and push). Each content file is now tracked once, about 5,900 tracked files in all. The Cloudflare build then builds only for pushes that touch `web/`, `wrangler.toml`, `package.json` or `package-lock.json`, and no longer pip-installs `requirements.txt` (2026-10-18). The plan and its decisions D1–D17 are in [docs/archive/CLEANUP_PLAN.md](docs/archive/CLEANUP_PLAN.md).

## Where things stand (2026-10-17)

| Measure | Today |
|---|---|
| Illustrated | 2,241 verses in 73 chapters of 11 books, every chapter complete |
| Narrated (neural MP3) | 2,348 verses in 76 chapters, every chapter complete: the 73 illustrated ones plus Acts 2, Acts 12 and Exodus 34 |
| Deploy | 5,802 of about 20,000 files (`publish_studio.DEPLOY_FILE_LIMIT`) |
| Pronunciation | 3,137 names. 569 are `unfixed`, and 195 of those occur in narrated chapters. Another 155 are `suggested` and 162 `unsure`. |
| Likely-stale narration | 122 published MP3s don't match the TTS cache entry for their verse's current respelling (98 have no entry, 24 differ) |

## Content

| When | Item | Notes |
|---|---|---|
| Now | **Narration policy** (decide once) | Proposed: neural MP3s for whole chapters only, and only for illustrated chapters; everything else stays on Web Speech until a file-cap lever (below) is pulled. Render a chapter's audio when its visuals start. Each narrated verse costs one deploy file. |
| Now | **Pronunciation backlog** | Do the 195 unfixed names in narrated chapters first. Then clear each next chapter's names before its audio is rendered. For each one, try ▶ IPA first: if Azure says the stored IPA right, tick **Use**; if the IPA is wrong, correct it. Otherwise `isbe_sweep.py` proposes respellings, and the Verifier and an ear confirm them ([docs/pronunciation.md](docs/pronunciation.md)). Render chapters with IPA names on the engine "Azure for verses with IPA names". The 155 `suggested` and 162 `unsure` names need an ear too. Every fix makes narration stale, so batch the fixes per chapter. |
| Now | **Check the 8 re-keyed "fixed" names by ear** in the Verifier | `Beth Zur`, `Jushab Hesed`, `Ir Nahash`, `Ben Hanan`, `Baal Meon`, `Baal Hermon`, `Merib Baal`, `Baal Perazim`. They were re-keyed to WEB's two-word spelling. |
| Now | **Re-render stale narration**, once per chapter, after that chapter's pronunciation pass | The 122 likely-stale verses: Numbers 3 (22), Exodus 34 (15), Luke 3 (14), Numbers 1 (13), Numbers 32 (13), Numbers 2 (12), Numbers 4 (10), Matthew 1 (6), Acts 13 (4), and 13 more across 1 Chronicles 2, 3, 4, 5, 8 and 9, Acts 2, 12 and 14, and 2 Peter 1. They include the nine verses made stale by the pronunciation prune: Numbers 32:38 and 1 Chronicles 2:45, 3:20, 4:12, 4:20, 5:8, 5:23, 8:34, 9:40. Use the Audio tool with **Overwrite existing files**. Then re-run `generate_1chronicles_tree_svg.py`, `generate_matthew1_svg.py`, `generate_numbers34_svg.py` and `generate_acts1314_svg.py`, because their cameras are timed to the MP3s. "No cache entry" may only mean the cache was cleared; a re-render settles both cases. |
| Now | **Acts 13–14 scene cards** | The Lystra card (14:8–20) is the prototype for review. Then the synagogue at Antioch of Pisidia (13:15–16, 13:38–50) and Jerusalem (13:27–37) on the same engine ([design/acts-13-14.md](docs/design/acts-13-14.md)). |
| Next | **Numbers 33** (map + timeline, High) | Reuses the `generate_tribal_maps.py` geometry from Numbers 32/34 |
| Next | **Joshua 13–19** (allotment map, High) | `TRIBES` and `PRINCES` already exist in `generate_tribal_maps.py` |
| Next | **Acts 19–21 and 27–28** (maps, High) | Reuses the `MED`/`PELOPONNESE`/`ISLANDS` coastline in `generate_acts1518_svg.py` and completes Paul's journeys. Acts 18 is built. |
| Next | **Haggai 1–2**, then the **2 John + 3 John diptych** | The next unbuilt picks in "Where to start" in [docs/design/short-books.md](docs/design/short-books.md). Check the WEB wording before lettering anything. |
| Next | Neighbours on the same geometry | **Numbers 10–14**, **Numbers 35** and **Joshua 1–5, 6, 9–12** (`generate_tribal_maps.py`); **Exodus 12–14** (pairs with the Numbers 33 itinerary); **Acts 1–2** (the Acts `MED` coastline) |
| Next | **Acts 12 and Exodus 34** | Fully narrated but not illustrated (Acts 2 is in the row above). Re-render Exodus 34's 15 stale verses first. |
| Next (decide) | **Video output** | Video Studio is built. Three renders sit in `C:\Dev\Theoria-archive\renders` (`config.RENDERS_DIR`): Genesis 1, 1 Chronicles 1–2 and Matthew 1, each with captions, description and thumbnail. Either publish to YouTube, or mark video "not planned" and leave Video Studio as it is. Publishing means re-rendering after the stale narration is fixed (Matthew 1 has 6 stale verses, 1 Chronicles 2 has 1), then one video per completed chapter at a cadence you choose. Upload steps: [docs/video-studio.md](docs/video-studio.md). Custom thumbnails need a verified channel. |
| Later | **Matthew 21–27**, Holy Week (timeline, High) | Day by day |
| Later | **Genesis 12–25, 25–36, 37–50** (maps, High) | Completes Genesis; reuses the Genesis 10 world map and the OT tree |
| Later | **1 Kings 12–22 and 2 Kings 1–17**, parallel kings (High) | A per-verse camera over the OT timeline sheet, which already dates 41 reigns (Ussher's years, with a Thiele reference rail), as 1 Chronicles does over the tree ([docs/design/ot-timeline.md](docs/design/ot-timeline.md)) |
| Later | **Leviticus 16** and **Leviticus 1–7** (High), **Exodus 29** (Med), **1 Kings 6–7** temple (High) | Reuse `svg_priest.py` and the tabernacle plan (`generate_tabernacle.draw_plan`) |
| Later | **Matthew 2** (map) and **Luke 1–2** (timeline), both High | Neighbours of built chapters; reuse the `svg_matthew_nativity.py` stage |
| Later | The other short books | Habakkuk 3 and Nahum 2 first (ranked next in [short-books.md](docs/design/short-books.md)), then Obadiah, Joel, Philemon, Jude, Titus, 2 Thessalonians and the rest of Habakkuk and Nahum. That makes 405 verses with Haggai and 2–3 John, and the designs already exist. |
| Later | Symbolic and architectural set pieces | Daniel 2, 7, 8 and 9; Ezekiel 1 and 10, and 40–43; Zechariah 1–6; Revelation 4–5 and 21–22. High priority, but nothing to reuse. |
| Later | Revisits | The Hebrews 5 ledger density and one shared mark for the five warnings ([design/hebrews.md](docs/design/hebrews.md), "Known soft spots"); keeping the Matthew 1 count of 41 names and 42 generations consistent on screen ([design/matthew-1.md](docs/design/matthew-1.md)); the Luke 3 time-depth counter (`docs/archive/LUKE3_IDEAS.md`, cross-cutting tricks) |

## Web

| When | Item | Notes |
|---|---|---|
| Now | **Check Wake Lock and pinch-zoom on a real iPhone** | Neither has been checked on a phone; the test browser refused the Wake Lock permission. Wake Lock in an installed home-screen app is the doubtful case. |
| Now | **Unify the attribution wording** | The web footer says "Scripture: World English Bible (public domain)". The Studio and Video Studio use `passages.ATTRIBUTION`, "World English Bible — public domain." |
| Next | **Deep links** (`?b=&c=&v=`, or a hash form) | Shareable, and needed by the Studio Preview. `web/js` reads nothing from the URL today. |
| Next | **Cloudflare Web Analytics** for `theoria-bible.net` | The domain is bought and live. Optionally rename the Worker and the repo from `av-bible` afterwards. Renaming the Worker changes its workers.dev URL, so check that the custom domain stays attached. |
| Later | **A Charts entry** next to ✦ | Once you choose which family-tree version belongs in the app. The OT tree, the V6 heir spine, the 1–2 Chronicles tree and the OT timeline are all deployed but unlinked (D14, [docs/reference-charts.md](docs/reference-charts.md)). |
| Later | Selectable colour themes | Cheap only while no SVG is hand-edited |
| Later | Open Graph preview cards per verse | Each card is a picture's end frame; `svg_freeze.freeze_animations` already freezes SMIL to its final values |
| Later | An app-shell service worker | Cache-first shell, with runtime caching only for chapters visited. It isn't needed to install the app (`web/manifest.webmanifest` exists), and iOS evicts storage anyway. |
| Later | The reference in fullscreen | Shown alongside the tap-to-reveal controls |

## Studio

| When | Item | Notes |
|---|---|---|
| Next | **Range files in SVG Studio** (D17) | SVG Studio labels a verse "shared with vv16–32" when its picture is a range file or an identical copy, and warns that an edit affects the whole run. Until then it sees only per-verse files. The interim PC stage stays as it is: it is retired after S4, and the Preview runs the web app, which already resolves range files. |
| Next | **Verifier for Azure renders** | The Verifier measures the Edge reading only. A `use_ipa` name it checks keeps `fixed` but gets no measurement of what Azure says. Add a mode that renders through `tts_engine.synthesize_ipa` in the carriers and scores that, at about 250 characters a name. The stale-narration lint in S3 must also judge a verse by `tts_engine.route()` for the engine it was rendered with, or every Azure verse will look stale. |
| Next | **S2 Consolidate** | `studio_core.py`, `narration.py`, `ui_common.py`, one visual resolver, one `web_view.py`; SVG Studio's hand-authoring features retire (D12) |
| Next | **S3 Lint + Publish** | `lint.py`, including the stale-narration, partial-audio and audio-timed-visual checks, a per-verse file inside a range file's run, and the text checks (overlap, overflow, off-canvas) for every family, promoted from `tools/audit_heb.py`. Publish refuses on blockers. The dry-run box already exists. Video Studio's "Also publish new narration" option retires once the Audio tool and the lint cover it. |
| Next | **S4 Hub window** with the embedded web Preview | After web deep links. Its server serves `web/` at `/`, the production layout. `PlaybackSession`, `visual_stage.py` and `svg_stage.py` are deleted only after the Preview passes its parity checklist ([docs/studio.md](docs/studio.md#phases)). |
| Later | **S5 Workflow features** | The generator CLI contract (`--only`, `--out`, `--dry`); regenerate to scratch, compare, then Accept; New visual family… with an option to write range files; the Next-up queue; chapter contact sheets |
| Later | **S6 Optional** | Tabs instead of windows; `svg_palette.py`; a figure-vocabulary browser; a Video render queue and thumbnail composer |
| Later | Bound SVG Studio's verse spinbox | It allows verses 1–176 in every chapter, instead of WEB's verse count |

## Infrastructure

| When | Item | Notes |
|---|---|---|
| Next | **Cross-process locks** for `pronunciations.json` and `web/audio/manifest.json` | Today both are locked only within one process. Two processes saving within milliseconds could lose one edit. This was accepted as low risk. |
| Later | **The workers.dev address** | The site is also public at `https://av-bible.dmwhit5988.workers.dev`. Keep it, or turn it off once `theoria-bible.net` is the only address in use. |
| Later | **WS4g: an optional history slim** | Not scheduled (D8 chose plain `git rm`). The procedure is WS4g in the archived plan. It would bring `.git` to about 147 MiB, but every SHA changes and other clones must re-clone. |
| Later | **R2 / file-cap levers** | About 14,200 files of headroom is roughly 7,000 more verses at one SVG and one MP3 each. Neural narration of the whole canon (31,098 MP3s) can't fit under 20,000 on its own. **Trigger:** the Publish budget meter passes 16,000 (80%), or you decide to narrate beyond about 7,000 more verses. **Levers, cheapest first:** (1) per-book bible JSON (1,189 → 66 files); (2) chapter-level MP3s with a verse timing table (check this against the iPad verse-change-pop fix first); (3) audio on R2 behind the existing manifest lookup; (4) the Workers Paid static-asset limit, believed to be 100,000 per version (verify in Cloudflare's current docs). |
