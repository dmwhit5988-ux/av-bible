# Theoria cleanup & roadmap

> **Archived 2026-10-17, after WS6.** The cleanup is done: Step 0 and WS1–WS7 landed (see each workstream's status). The forward plan is now [ROADMAP.md](../../ROADMAP.md), which also carries the two optional items left here, WS4f (serve `web/` directly) and WS4g (history slim). The text below is kept as written, so its paths and line numbers describe the repo before the cleanup.

*This is a plan; nothing in the repo has been changed. All 16 decisions were answered on 2026-10-16 (§2), and the workstreams reflect those answers. Line numbers come from the working tree on 2026-10-06. Many files have large uncommitted diffs, so the numbers will drift after Step 0; search for the symbol named next to each number rather than relying on the number.*

*Shells: blocks marked **(Git Bash)** use `grep`, `xargs`, `cut`, `wc` or `{a,b}` brace expansion and only work in Git Bash. Blocks marked **(PowerShell)** use `.ps1` scripts, `C:\…` paths or `.venv\Scripts\python.exe`. Plain `git` commands with no pipe work in either.*

**Execution order at a glance:** Step 0 → WS1 (1a + 1b + 1c in one push, then 1d) → WS2 → WS3 → WS7 → WS5 → WS4a–e → WS6 → WS4f / D7(c). (WS4g, the history rewrite, is not scheduled; D8.) WS4a–e can also be done any time after Step 0; they only have to come before 4f.

---

## 1. Summary

### 1.1 What changes and why

- **WEB becomes the only translation.** For a WEB reader almost nothing changes:
  - The unsuffixed visuals for Genesis 5, Genesis 11 and Luke 3 already use WEB spellings. The generators build them from `resolved["WEB"]` (generate_genealogy_svg.py:67, generate_luke3_svg.py:560).
  - The PC app already reads `bibles/WEB/*.json` from disk. `fetch_passage` prefers the local file (passages.py:369-370), and all 1,189 WEB chapters exist. The "api" source on WEB is a fallback that is never reached.
  - What goes: 8 translation folders (8,818 chapter files), 836 translation-suffixed visuals, 32 KJV MP3s and 4 visuals for verses WEB doesn't have (Romans 16:25-27, Acts 15:34). Each of these exists twice, once in the source folders and once in `deploy_bundle/`.
- **The toggles that no longer earn their place are removed.**
  - Web: Translation, Notes, Still graphics and Speed are removed, along with the whole toggles row (D5).
  - PC: Version, Translator notes, Reference, Voice, Speed and the Auto-continue checkbox are removed (playback always continues into the next chapter, as on the web).
  - WEB's "notes" are 1,161 real footnotes, such as "or, seed" and unit conversions. All three renderers label them "Translator-supplied words:", which is wrong.
- **The reduced-motion stills go:** 1,613 `.still.svg` files in each copy, plus the `build_stills` step in Publish and every line of still code. Nothing replaces them: the site no longer offers reduced-motion support (D4).
- **The PC app becomes "Theoria Studio".** It is an authoring tool, not a reader. Coverage is the home view, a Preview shows exactly what the website shows, every tool follows one shared passage, and a pre-publish lint gate checks the work.
- **The repo is made truthful before anything is deleted.** Today:
  - 19 Python modules (18,454 lines) are not in git.
  - GitHub `main` cannot regenerate Matthew 1, because a Publish commit deleted `generate_matthew1.py`.
  - Publish commits the whole git index, not just content.
  - `prepare-deploy.ps1` is gitignored.
  - The registry would overwrite the published 1 Chronicles v3 visuals with the old v2 generator.
  Step 0 fixes all of these.
- **The docs are reorganised.** 16 root doc files become README, ROADMAP, CLAUDE.md and CREDITS, plus a `docs/` tree with design records and an archive.
- **A live-site bug is fixed along the way.** `visuals/default.txt` ("I've only built visuals for a few passages … WEB translation has better audio") shows on about 93% of verses (28,857 of 31,098; only 2,241 WEB verses have their own visual) on the deployed site. It is replaced by a built-in "isn't illustrated yet" line with a button into the ✦ list (D6).

### 1.2 Before / after

| Measure | Today | After WS1–WS6 | Notes |
|---|---|---|---|
| Tracked files | 33,727 | ~11,700 (deploy_bundle still tracked) / ~5,900 (D7 option c) | 11,014 content files removed from each copy, plus ~20 dead files; ~40 code/doc files added in Step 0 |
| Deploy file count (cap ~20,000) | 16,822 (84%) | ~5,800 (29%) | bibles 10,007→1,189; visuals 4,416→~2,248; web 2,399→2,363 (with the D15 default) |
| Headroom under the cap | ~3,200 files | ~14,200 files (~7,000 more verses at 1 SVG + 1 MP3 each) | |
| Translations | 9 (ASV, BBE, BSB, DARBY, DRA, KJV, OEB, WEB, YLT) | 1 (WEB) | |
| Translation-suffixed visuals / MP3s | 836 / 32 (each ×2) | 0 / 0 | the unsuffixed files are already the WEB versions |
| `.still.svg` files | 1,613 + 1,613 | 0 | 289 of them are also translation-suffixed |
| `visuals/manifest.json` keys | 2,795 | 2,241 | −547 suffixed, −4 orphan verses, −3 `.txt` notes |
| `web/audio/manifest.json` keys | 2,384 | 2,348 | the 32 `.KJV` keys go (2,352 after WS1), then the 4 Psalms 119 keys (D15 default); the `.WEB` key format stays (D11) |
| Web controls | 8 (Translation, Book, Chapter, Start at verse, ✦, Notes, Still graphics, Speed) | 4 (Book, Chapter, Verse, ✦) | plus transport and fullscreen |
| PC main-window controls | 6 pickers + 4 transport + 3 checkboxes + 8 tool buttons (the bar needs 1,463 px in a 1,180 px window; 2–5 buttons are hidden) | Passage bar + grouped tools + Preview | |
| Root plan/idea docs | 15 `.md` + 1 `.xlsx` (7 untracked) | 4 root docs + `docs/` | |
| Root Python modules | 80 (19 untracked, 17 with uncommitted edits) | ~69, all tracked | 11 deleted; Studio phases later remove `visual_stage.py`/`svg_stage.py` and add a few shared modules |
| Pronunciation entries | 3,331 (218 are spellings WEB never uses) | ~3,137 (24 re-keyed to WEB spacing, 194 archived) | |
| Repo `.git` | ~293 MiB (262.6 packed + 30.5 loose) | unchanged with plain `git rm`; ~147 MiB after an optional history rewrite (D8) | |
| `deploy_bundle/` on disk | 296.9 MiB | ~178 MiB, or gone (D7 c) | |

Appendix D records where the underlying audits disagreed and how each conflict was resolved.

---

## 2. Decisions (answered 2026-10-16)

All 16 decisions are settled. Five differ from the original recommendation and are marked **changed**; the workstreams below have been updated to match.

| # | Decision | Answer |
|---|---|---|
| D1 | What the PC app becomes | **Studio first, with a Preview pane** that embeds the real web app. A slimmed tkinter player stays only until the Preview passes the S4 acceptance checklist (§5.5); then `PlaybackSession`, `visual_stage.py` (619 lines) and `svg_stage.py` (418 lines) are deleted. |
| D2 | Display window (projection) | **Remove** `FullscreenStage` (visual_stage.py:598-619, app.py:489-492). The website's fullscreen covers this. |
| D3 | Studio window model | **A hub main window, with tools as separate windows** that follow one shared passage. Tabs only if separate windows become annoying. |
| D4 | Reduced motion once the stills are gone | **Changed: no reduced-motion support.** The stills and all still code go, and nothing replaces them. The stage keeps its `<img>`; no inline renderer. |
| D5 | Web controls | **Changed: no speed control.** Book, Chapter, Verse, ✦ Illustrated, Prev/Play/Next and fullscreen. |
| D6 | The stage on verses without a visual | **Changed: a built-in pointer to the illustrated chapters, not a text file.** See below. |
| D7 | `deploy_bundle/` | The recommended path: keep it tracked through WS1–WS3, then serve `web/` directly, with one standing requirement: **deploying stays one button, Publish in the Studio.** See below. |
| D8 | History | **Plain `git rm`.** No history rewrite is scheduled; WS4g stays documented for later only. |
| D9 | Translation-suffixed visuals | Delete the 836 files, the variant machinery and the 4 orphan-verse visuals (Romans 16:25-27, Acts 15:34). WEB's verse numbering is the generators' source of truth. This also closes the `.WEB.svg` trap, where SVG Studio's leftover "WEB" variant chip would write a file that `visuals.js:158` serves instead of the generic one. |
| D10 | Folders | No Python folders: 223 bare-name imports and 29 `__file__`-relative paths make it costly. Docs move to `docs/`; content moves only as part of D7(c). |
| D11 | Data formats | Unchanged: per-chapter `bibles/WEB` JSON (its `notes` and `translation` fields stay in the files), `.WEB` audio-manifest keys, visuals manifest v2 minus `still`. |
| D12 | SVG Studio hand-authoring features | Retire them in Studio phase 2 and keep a read-only Source view. "Stage for deploy" goes in WS5. |
| D13 | The 218 pronunciation entries WEB never uses | Re-key the 24 hyphenated entries to WEB's two-word form, move the other 194 to `pronunciations_archive.json`, and regenerate the reports. |
| D14 | Reference wall charts | **Changed: deploy them all, link none, archive none.** See below. |
| D15 | Psalms 119's 4 test MP3s | Delete them and their manifest keys. |
| D16 | Small web choices | Rename the storage key to `theoria.selection` (with a one-time read of the old key), allow pinch-zoom, and open on Genesis 1. |
| D17 | The same picture on consecutive verses *(added 2026-10-16)* | **Keep playing, don't restart.** An SVG can be tied to a verse range (`Book_c_v1-v2.svg`), and byte-identical consecutive copies count as one picture automatically. See WS7. |

**D4: what "no reduced-motion support" means in practice**
- WS2d deletes the whole web still path (the checkbox, `prefersReducedMotion`, `stillUrl`); WS3 deletes the Python side and the 1,613 files. No `pauseAnimations`, no `prefers-reduced-motion` CSS, no inline SVG renderer.
- Visitors who turn on their OS "reduce motion" setting will see the animations, including the 99 SVGs that loop indefinitely (the Exodus 25–27 pulse and the Genesis 3:24 sword). That is the trade-off of this choice.
- The stage keeps `<img>`. Its `?r=Date.now()` branch (app.js:344-352), which restarts a picture when the next verse shows the same file, is replaced in WS7 by "same picture, keep playing" (D17).
- If you want reduced motion back later, the design that was dropped is recorded in Appendix D.

**D6: the pointer on verses without a visual**
- `visuals/default.txt` and the whole text-visual feature are deleted (WS2b). In their place is a small element built into the page, so it is not a visual file and costs nothing against the file cap.
- What it shows: the book gradient, the reference ("Genesis 12:3"), one line of text, and a **✦ See illustrated chapters** button that opens the existing ✦ list.
  - Chapter with no visuals at all: "Genesis 12 isn't illustrated yet."
  - A verse without a visual inside an illustrated chapter: "This verse isn't illustrated yet." All 73 illustrated chapters are complete today, so this wording first appears when a chapter is published partly built.
  - The data is already there: `stage.illustratedChapters()` (visuals.js:118) is what puts the ✦ marks in the pickers.
- The Studio Preview shows the same pointer, so gaps stay visible while you author.

**D7: keeping deployment easy**
- Your routine doesn't change: author in the Studio, press **Publish**, and the site updates.
- The cleanup's own hand-written commits (WS1–WS4) are done in Claude sessions. You don't have to run git or PowerShell yourself.
- Every change to the deploy layout updates Publish in the same commit and is checked with a Publish dry run (0.7, and again at D7(c)). Studio phase 3 adds a pre-publish lint and a dry-run box.
- Step 0.2's Cloudflare dashboard check needs your sign-in. Sign in from the browser pane and Claude can read the settings with you; it takes a few minutes.

**D17: one picture across several verses**
- Today 33 verses replay an animation that is identical to the previous verse's; 19 of them are a visible redraw in Numbers 32. Each copy is a separate file, so the browser treats it as a new image.
- New rule everywhere verses play in sequence (web, the Studio Preview, Video Studio): if the next verse shows the same picture, leave it running.
- Two ways to share a picture: a range file you or a generator writes on purpose, and automatic matching of identical copies when the manifest is built (with a per-family opt-out).

**D14: the reference charts**
- Everything in `visuals/reference/` stays and deploys: the OT family tree, its V6 heir-spine variant, the 1–2 Chronicles tree, and the OT timeline (first deployed in Step 0.8b).
- Nothing on the site links to them yet, because you are still deciding which family-tree version belongs in the app. "Deployed but unlinked" means anyone with the exact URL can open them, but nothing points there.
- Publish carries your chart tweaks like any other visuals change.
- The 1–2 Chronicles chart has no generator in the repo (`generate_ot_family_tree_svg.py:38` writes only `Old_Testament_family_tree`). `docs/reference-charts.md` records it as a frozen file.
- The Charts link moves to the roadmap as **Later: when you choose the version** (§6.2).

---

## 3. Step 0: safety first

Nothing in WS1–WS6 should start until Step 0 is done. Step 0 changes nothing on the site except the deliberate content commits in 0.8b (the OT timeline, and a regeneration catch-up only if drift is found).

> **Status (2026-10-16): done, except three follow-ups.** Commits `2b95df2b`…`8d0eb310` were pushed with the `pre-cleanup` tag. The backups and `pre-cleanup.bundle` are in `C:\Dev\Theoria-archive\`. The 24 tests pass in a clean checkout of the tag. The Publish fix was verified in a throwaway worktree. The regeneration baseline: 1 Chronicles (407) and Matthew 1 (25) are byte-identical, and all 24 generators run cleanly. Follow-ups:
> 1. **0.2 Cloudflare check, partly answered.** Cloudflare's GitHub check run on `8d0eb310` confirms that `av-bible` is a **Worker using Workers Builds**, not Pages, and that the production build of today's push succeeded. Still needed, from the build log or Settings → Build: the build and deploy commands (expected: no build command, `npx wrangler deploy`), branch and watch-path settings, and the live URL. Only WS4f/D7(c) depends on these. The Apple passkey doesn't work in the in-app browser, so use Edge.
> 2. **Genesis 1–3 drift. Decided 2026-10-16: leave as is.** 19 files differ from the current `svg_figures.py`: a brighter sun outline in Genesis 1:14-19, and sub-pixel shape changes in 2:19-25 and 3:2-13. The published versions stay. The list in `C:\Dev\Theoria-archive\regen-drift.txt` is known noise for later "expect no change" checks. The drift will ship naturally whenever Genesis 1–3 are regenerated for another reason.
> 3. ~~Delete the merged `acts-second-journey` branch~~ **Done 2026-10-16**, locally and on GitHub; it was 0 commits ahead of `main`.

**0.1 Freeze risky actions until Step 0 is complete**
- [ ] Don't press **Publish**. It runs `git add -A` on `web bibles visuals deploy_bundle` and then `git commit` with no pathspec (publish_studio.py:247, 252), so it commits anything staged. That is how commit `368016f4` deleted `generate_matthew1.py`.
- [ ] Don't press **Re-run generator** on any 1 Chronicles verse. The registry still names the v2 generator (svg_generators.json, 1 Chronicles family), and it writes the same 407 file paths.
- [ ] Don't run `git add -A` or `git add .` at the repo root. `_scratch/` (738 files) and `mockups/` (128 files) are not ignored.

**0.2 Record what you can't see from the repo** *(you sign in to Cloudflare in the browser pane; Claude reads the settings with you; see D7)*
- [ ] In the Cloudflare dashboard, write down:
  - whether `av-bible` is a Worker (expected, since wrangler.toml uses `[assets]`) or a Pages project;
  - the connected repo and branch, build command, deploy command and root directory;
  - whether non-production branch builds are on, and any watch paths;
  - the plan tier;
  - whether the latest deployment matches commit `78b7ddad`.
- [ ] Note the live URL for the README.

**0.3 Backups (outside the repo folder, in `C:\Dev\Theoria-archive\`)**

The git bundle is made in 0.9, after the catch-up commits; a bundle made now would miss every untracked file. Until then, these copies are the backup:
- [ ] Everything git doesn't hold yet **(Git Bash)**:
  ```
  mkdir -p /c/Dev/Theoria-archive
  git ls-files -o --exclude-standard -z | tar --null -T - -cf /c/Dev/Theoria-archive/untracked.tar
  git diff --binary > /c/Dev/Theoria-archive/uncommitted.patch
  ```
  The tar holds the 19 `.py`, the 7 `.md`, the timeline pair, `branding/`, `_scratch/` (43.6 MiB) and `mockups/` (~4.6 MB). The patch holds the 17 modified `.py` and the other uncommitted edits.
- [ ] The irreplaceable ignored files:
  - `cache/ipa_checks.json` (224 KB). This is the Verifier's whole-canon verdict store; rebuilding it means a full ASR sweep.
  - `bibles/eng-web.usfx.xml` (6.2 MB). The only source for regenerating `bibles/WEB`.
  - `config.json`
  - `prepare-deploy.ps1`, `deploy.ps1`, `deploy-api.ps1`
  - `backups/` (245 MiB)
  - `renders/` (356 MiB, Video Studio output)
- [ ] Don't clear `cache/audio/tts` (22,381 files, 510 MiB). Stale-narration detection depends on it (Studio phase 3).

**0.3b Rescue the scratch scripts the roadmap reuses** (before 0.4 ignores `_scratch/`)
- [ ] Copy into a tracked `tools/` folder, as reference code rather than finished tools:
  - `_scratch/audit_heb.py`, the SVG overlap/overflow audit that S3 promotes (it hard-codes `C:\Dev\AV Bible` at L2);
  - `_scratch/layout_lab.py`, the V6 rebuild source named in visuals/reference/README.txt:61. It finds the repo through its parent folder (L52-53), which still works from `tools/`.
- [ ] **Don't rescue** `_scratch/build_one.py`, `build_compare.py` or `build_grid.py`. They are a one-off Exodus 25–27 restyle comparison, not a contact sheet: `build_one.py:11` and `build_compare.py:6` hard-code `SRC = _scratch/ex_restyle` (33 mockup SVGs), and `build_compare`'s `TITLES` are fixed Exodus 25–27 captions, so a copy in `tools/` could not run after the WS4e prune. They stay in the 0.3 `untracked.tar` for reference; S5's contact sheet is a new script driven by the registry and manifest.
- [ ] The two rescued scripts go into Commit A. The WS4e `_scratch/` prune waits for this step.

**0.4 `.gitignore` before any commit**
- [ ] Add `_scratch/` (after 0.3b), `mockups/figures/`, `isbe_cache/`, `tools/ffmpeg/` and `.claude/settings.local.json`. (`video_render.find_ffmpeg` looks for a dropped-in ffmpeg under `tools/ffmpeg/bin/`, video_render.py:199, so the new tracked `tools/` folder must not sweep in binaries.)
- [ ] Keep the pending `renders/` line, which is uncommitted today.
- [ ] Remove the `prepare-deploy.ps1` line (.gitignore:14). The script is 32 lines, copies files only and holds no secrets. Keep `deploy.ps1` and `deploy-api.ps1` ignored until WS4 deletes them.

**0.5 Which untracked files the committed or working code needs**

| Untracked file(s) | Needed by | What breaks without it |
|---|---|---|
| `svg_figures.py` | `generate_tabernacle.py:22` (top-level import in the working tree); generate_tabernacle is imported by 33 modules; 12 modified generators | Every generator fails to import |
| `video_studio.py`, `video_render.py` | `app.py:23` (working tree) | The app doesn't start |
| `chronicles_tree.py`, `ot_grafts.py`, `matthew_tree.py`, `generate_ot_family_tree_svg.py`, `svg_chronicles_world.py`, `svg_matthew_world.py`, `svg_matthew_nativity.py` | `generate_matthew1_svg.py` (working tree) and the 1 Chronicles v3 generator | Matthew 1 and 1 Chronicles can't be regenerated (HEAD's Matthew 1 generator imports the deleted `generate_matthew1`) |
| `svg_vocab.py`, `svg_priest.py`, `generate_exodus28_svg.py`, `generate_hebrews_svg.py` | `svg_generators.json` (working tree) | SVG Studio registry paths point at missing files |
| `generate_1chronicles_tree_svg.py`, `generate_2peter_svg.py`, `generate_zephaniah_svg.py` | Published output: 407 + 61 + 53 SVGs | The only source of those visuals |
| `generate_ot_timeline_svg.py`, `chronology.py` | `visuals/reference/Old_Testament_timeline.{svg,html}` (also untracked) | The only source of the chart |
| `prepare-deploy.ps1` (gitignored) | `publish_studio.py:200-202`, `svg_studio.py:846-848` | Publish can't run from a fresh clone |
| `VIDEO_STUDIO.md`, `TIMELINE.md`, `*_IDEAS.md` (5) | README.md:130 link (working tree); docstrings in chronology.py:1,37, generate_hebrews_svg.py:2, generate_2peter_svg.py:3, generate_zephaniah_svg.py:3; svg_generators.json:202,223 | Dead pointers |
| `branding/` (5 SVGs, ~10 KB) | Source art for `web/icons/*` | Logo sources exist only on this disk |
| *Not needed:* `_scratch/` (apart from the two scripts rescued in 0.3b), `mockups/` | Referenced only by idea docs and the `generate_luke3.py:23` docstring | — |

**0.6 Review, then make the catch-up commits**
- [ ] Skim the 19 untracked `.py` files and the diffs of the 17 modified ones for half-finished scratch content (+5,000 / −1,675 lines; the biggest is `generate_romans_svg.py` at +2,389/−822).
- [ ] **Commit A, "code catch-up" (atomic).** Contents:
  - all 19 untracked `.py` files;
  - the 17 modified `.py` files;
  - `svg_generators.json`;
  - `prepare-deploy.ps1`;
  - `.gitignore`;
  - `tools/` (the two scripts from 0.3b);
  - `visuals/reference/Old_Testament_timeline.{svg,html}`. This does not deploy it: the bundle copy is decided in 0.8b.
  Don't split app.py from video_studio, or any generator from svg_figures.
- [ ] **Commit B, "docs as-is":** the 7 untracked `.md` files, plus the modified README.md and INFOGRAPHIC_CANDIDATES.md (31 lines marking Exodus 28, Hebrews, 2 Peter and Zephaniah as built).
- [ ] **Commit C:** `pronunciations.json` and `PRONUNCIATIONS.md` (uncommitted pronunciation work).
- [ ] **Commit D:** `branding/`.

**0.7 Fixes that must land before any Publish**
- [ ] `publish_studio.py:252`: commit only content paths, i.e. `["git","commit","-m",msg,"--",*CONTENT_PATHS]`. Optionally refuse to publish when non-content paths are staged.
- [ ] `publish_studio.py:40`: narrow `CONTENT_PATHS` from `["web", "bibles", "visuals", "deploy_bundle"]` to `web/audio`, `bibles`, `visuals`, `deploy_bundle/audio`, `deploy_bundle/bibles`, `deploy_bundle/visuals`. Listing only the bundle's content folders matters: `prepare-deploy.ps1:11` copies the working-tree `web\*` into the bundle root, and `deploy_bundle/` tracks 14 shell files (`index.html`, `manifest.webmanifest`, `js/*`, `css/style.css`, `icons/*`). With plain `deploy_bundle` in the list, half-finished WS2/WS3 web code would still ship under "Publish: …". That is how `78b7ddad`, `2973589b` and `cb6f080a` shipped code. Web code then ships only by the bundle rule in §4.
- [ ] Registry fixes in `svg_generators.json`:
  - [ ] 1 Chronicles: point it at `generate_1chronicles_tree_svg.py`, with specs `generate_1chronicles.py`, `chronicles_tree.py`, `ot_grafts.py`, `svg_chronicles_world.py` and `generate_ot_family_tree_svg.py`.
  - [ ] Add families for 2 Peter and Zephaniah, with kinds and spec pointers (each generator plus `svg_vocab.py` and `svg_figures.py`). Today the manifest gives all 114 of their records the fallback kind "infographic".
  - [ ] Matthew 1 specs: add `svg_chronicles_world.py` and `generate_ot_family_tree_svg.py`.
  - [ ] Romans spec text: it names `STOPS`/`BEATS`/`TRACK`, none of which exist. It should name `SCENES` (generate_romans_svg.py:2529) and `draw_ch1..16`.
- [ ] **Verify the Publish fix** in a throwaway worktree, so nothing touches `main`'s checkout or index:
  1. Commit the two `publish_studio.py` fixes above, then `git worktree add --detach ..\publish-probe HEAD` so the fixed code is in it, and work inside `..\publish-probe`.
  2. Set up the three hazards: create and `git add` a non-content file (`tools/_probe.txt`); edit `web/js/app.js` and `deploy_bundle/js/app.js` (one comment line each); create one content file (`visuals/_probe.txt`) so the commit isn't empty.
  3. Run exactly the argv the worker builds: `git add -A -- <CONTENT_PATHS>` then `git commit -m probe -- <CONTENT_PATHS>`, with the six paths from `CONTENT_PATHS` (or call a small `_commit_argv()` helper factored out of `_push_worker` so the test and the worker share it).
  4. `git show --stat HEAD` must list **only** `visuals/_probe.txt`. `git status --short` must still show `tools/_probe.txt` staged and both `app.js` edits unstaged.
  5. `git worktree remove --force ..\publish-probe`. The detached commit is unreferenced and harmless.
  - Repeat this after D7(c), when `CONTENT_PATHS` becomes `web/audio web/visuals web/bibles`; the `web/js` edit must again stay out.

**0.8 Safety net tests (small; added before anything is deleted)**
- [ ] `test_imports.py`: import every root module, skipping the lazy-heavy `ipa_asr` internals **and the modules with import-time side effects**:
  - `isbe_apply.py` has no `__main__` guard and calls `pronunciation.save_names(names)` at module level (L55). **Importing it rewrites `pronunciations.json`.**
  - `isbe_benchmark.py` has no guard and runs an ASR benchmark at import.
  - `isbe_apply`, `isbe_benchmark`, `isbe_repair` and `isbe_sweep` do `os.chdir(r"C:\Dev\AV Bible")` at import (e.g. isbe_sweep.py:24-25), so in a separate worktree they would silently switch to the main checkout.
  Skip all `isbe_*` modules until WS4d deletes or fixes them.
- [ ] `test_registry.py`:
  - every generator and spec path in the registry exists and imports;
  - no two families claim the same verse;
  - every `visuals/<Book>/<ch>` folder that holds verse SVGs has an owner. This check would have caught 2 Peter and Zephaniah.

**0.8b Sync the bundle and take a regeneration baseline**

Several generators changed after their published output was written. By file times, `generate_genealogy.py` and `generate_luke3.py` (2026-08-12 22:04) are newer than `Genesis_5_3.svg` (08-11 22:14) and `Luke_3_23.svg` (08-12 21:43). `svg_figures.py` (08-20) is newer than all of those outputs and is imported at top level by `generate_tabernacle.py:22`, which 33 modules import. Without a baseline, a later "expect no change" check can't tell cleanup damage from drift that was already there.
1. **(PowerShell)** `powershell -File prepare-deploy.ps1`, then `git status --short deploy_bundle`. Expect only the two `Old_Testament_timeline.*` copies. Per D14, commit them alone ("Deploy OT timeline wall chart (unlinked)"). Add no link to it anywhere on the site.
2. Re-run every registered generator: the `generator` field of each family in `svg_generators.json`, 24 scripts after 0.7. Use `--out <scratch dir>` where it exists (the 1 Chronicles tree and Matthew 1). Both write **flat** files (`1_Chronicles_<ch>_<v>.svg`, generate_1chronicles_tree_svg.py:83-84; generate_matthew1_svg.py:118-119), while `visuals/` nests by chapter and also holds `.still.svg` twins, so `git diff --no-index` would report every file as added or deleted. Compare per file instead **(Git Bash)**:
   ```
   S=/c/Dev/Theoria-archive/regen-1chr   # one --out folder per generator (regen-matthew1 for the other)
   for f in "$S"/*.svg; do n=${f##*/}; stem=${n%.svg}; rest=${stem%_*}; ch=${rest##*_}; book=${rest%_*}
     cmp -s "$f" "visuals/$book/$ch/$n" || echo "DIFF $n"; done
   ls "$S"/*.svg | wc -l                                         # 407 for 1 Chronicles, 25 for Matthew 1
   ls visuals/1_Chronicles/*/*.svg | grep -vc '\.still\.svg$'    # 407 today; must equal the scratch count
   ```
   Run the rest in place, then `git status --short visuals` and `git clean -n visuals`.
3. If anything drifted, review it:
   - Intended: run `build_stills.py` (the twins exist until WS3), `build_manifest.py` and `prepare-deploy.ps1`. Commit as "Regenerate: catch up to current generators", by hand and not through Publish.
   - Not intended: save the list (`git status --short visuals > C:\Dev\Theoria-archive\regen-drift.txt`), restore the files, and treat that list as known noise in the later checks.
- Every later "byte-identical" or "expect no change" check (WS1, WS4d, WS4) is measured against this baseline.

**0.9 Tag, back up, verify, push**
- [ ] `git tag pre-cleanup`.
- [ ] **(PowerShell)** `git bundle create C:\Dev\Theoria-archive\pre-cleanup.bundle --all`. It now holds the catch-up commits and the tag. Make another bundle before 4g.
- [ ] `git worktree add ..\theoria-check pre-cleanup`, then run `test_imports.py`, `test_registry.py` and `test_svg_freeze.py` there. Expect 20 tests to pass. The Matthew 1 generator will refuse to run in a clean worktree because of its `backups/` guard (generate_matthew1_svg.py:82-86); this is fixed in WS4.
- [ ] Push `main`. This is one Cloudflare deploy whose only content changes are the 0.8b commits (the OT timeline, plus a regeneration catch-up only if you chose one). It also repairs GitHub's broken Matthew 1 import.
- [ ] Delete the merged branch `acts-second-journey`, both locally and on GitHub (it is 44 commits behind `main` and 0 ahead).
- [ ] Optional: do WS1–WS6 on a `cleanup` branch and fast-forward `main` at each milestone. First check whether Cloudflare builds non-production branches.

---

## 4. Workstreams

| # | Workstream | Effort | Must come after | Ships together with |
|---|---|---|---|---|
| WS1 | WEB-only: data and Python code | M | Step 0 | The WS2 translation-picker removal (same push) |
| WS2 | Web UI simplification | M | WS1 for the picker; other parts are independent | — |
| WS3 | Retire the reduced-motion stills | S | WS2d, which removes the web side of the stills; then 3b before 3c | — |
| WS4 | Repo and deploy hygiene | M | Step 0 for 4a–e; WS1 and WS3 live for 4f | — |
| WS5 | PC app → Studio shell cleanup | M | WS1 (shares app.py, passages.py) | — |
| WS6 | Docs cleanup | M | Write README/ROADMAP last, against the cleaned code | — |
| WS7 | Shared visuals: one SVG across several verses (D17) | S–M | WS1 and WS3c (both edit `build_manifest.py`) | — |

Each content-deleting step is a **hand-written commit, not a Publish**, so the history says what happened. Rebuild the manifest and the bundle (`build_manifest.py`, then `prepare-deploy.ps1`) before committing.

**Bundle rule for web code (until D7 c).** `wrangler.toml` serves `./deploy_bundle`, so a `web/` edit alone never reaches the site, and after 0.7 Publish no longer carries it. Every web-code commit (WS1b, WS2) runs `prepare-deploy.ps1` and includes the bundle shell (`deploy_bundle/index.html`, `manifest.webmanifest`, `js/`, `css/`, `icons/`) in the same commit. Check it on the `web-static` launch config, which serves `deploy_bundle`. Under D7(c) this rule goes away.

### WS1 — WEB-only: data and Python code

> **Status (2026-10-16): done, committed locally as `ce4b81c6` (1a), `796ac064` (1b), `62506892` (1c) and `bef1bfb2` (1d); 1e moved, not deleted, into `C:\Dev\Theoria-archive\ignored\`.** Pushed as `193adf3c`; Cloudflare's Workers Build succeeded about a minute later.
> - **Verified:** 25 tests pass; all 24 generators reproduce the pre-cleanup output; the importer reproduces all 1,189 WEB files; a returning "KJV" visitor loads WEB on the web-static server; Romans 14:26, Romans 16:24, Acts 15:33/35, Genesis 5:9 and Luke 3:36 render; Genesis 1 plays neural MP3s; Coverage shows Romans 16 24/24 and Acts 15 40/40.
> - **Numbers:** tracked files 33,727 → 14,385; deploy bundle 16,824 → 7,133.
> - **Beyond the plan:** seven more generators iterate `verse_numbers()`; `test_registry` fails on any translation-suffixed visual; the visuals manifest gives 2 Peter and Zephaniah kind "diagram".
> - **Follow-ups:**
>   - Nine narrated verses are stale after 1d (Numbers 32:38; 1 Chronicles 2:45, 3:20, 4:12, 4:20, 5:8, 5:23, 8:34, 9:40).
>   - Check the 8 re-keyed "fixed" names by ear in the Verifier.
>   - The web and PC attribution wording differ (WS2 unifies them).
>   - SVG Studio's verse spinbox isn't bounded by WEB's verse count (small, optional).

**Goal.** One translation everywhere. Python has no translation parameter, no network text path and no notes. The 8 other translations, the suffixed visuals, the KJV MP3s and the orphan-verse visuals are deleted.

**1a. Python code (one commit; all importers change together)**
- [ ] **`passages.py`** (390 → ~60–100 lines). New contents:
  - `TRANSLATION = "WEB"`
  - `ATTRIBUTION = "World English Bible — public domain."`
  - `Passage(book, chapter, canonical, verses)`
  - `load_chapter(book, ch)`, which **picks keys explicitly**. `load_local` (L355) and `_cache_get` (L101) currently call `Passage(**data)`, and every WEB JSON carries `translation` and `notes`.
  - `verse_numbers(book, ch)`, the single versification source
  - `PassageError`

  Delete:
  - the `TRANSLATIONS` registry and its derived dicts (L37-62);
  - ESV constants, eviction and the ESV fetchers (L25-29, L113-240);
  - the passage cache (L88-114);
  - `fetch_public`, `_query_candidates`, `_SINGLE_CHAPTER_MAX` (L243-324);
  - `_last_fetch` and `polite_throttle` (L380-390; the def is at L383).

  Either keep `fetch_passage(book, ch)` as a thin shim for one cycle, or update all 7 callers:
  - app.py:638, audio_studio.py:224, generate_genealogy.py:90, generate_luke3.py:119, generate_showcase_audio.py:127, pronunciation_tool.py:210, video_render.py:482;
  - the 4 direct `bibles/WEB` readers: chronicles_tree.py:1345, generate_1chronicles.py:43, svg_matthew_world.py:84, coverage_studio.py:37.
- [ ] **Import fixes:**
  - Move `_ANNOTATION` and `_SUPPLIED` into `import_translation.py`, which imports them at L38 (`from passages import _ANNOTATION, _SUPPLIED`).
  - `video_studio.py:27` imports `fetch_passage` but never uses it.
  - `generate_genealogy_svg.py:25` imports `PassageError`.
- [ ] **`config.py`:**
  - Drop `esv_api_key` (L17), `translation` (L18), `show_notes` (L23) and `PASSAGE_CACHE_DIR` (L10, L47).
  - Keep `CACHE_DIR` and `AUDIO_CACHE_DIR`; `tts_engine.py:22,48` and `regen_pronunciation_todo.py:12` use them.
  - Add `OBSOLETE_KEYS` popped in `load()`: `esv_api_key, translation, show_notes, mode`. The local config.json has an orphan `mode`.
- [ ] **`requirements.txt`:** drop `requests` (only passages.py:20 imports it). Add `aiohttp`, which video_render.py:768 imports and which today arrives only through edge-tts.
- [ ] **`app.py`:**
  - Translation: imports L25-27; migration L258-261; Version combo L313-324; `selected_translation` / `_on_version_change` L445-453; `play()` L634; `refresh_attribution` L464-466 becomes a constant; `_save_position` L731; the translation argv passed to the Pronunciation Studio L504-506; `(WEB)` in references L745, L779, L829.
  - ESV (dies with passages): docstring L1; `import webbrowser` L12; `fetch_esv_audio` import L25; the narration event L47 and L824; `mode`/`api_key` params L53-64; run() branch L126-129; `_run_narration` L173-193; `SettingsDialog` L196-246; `open_settings` L486-487, which has no caller; api_key L633, L638, L658; the always-true `mode == "tts"` guards L80, L679, L690, L757.
  - Notes: checkbox L355-360; L456; L734; L774-781.
  - Welcome hint: delete `_show_hint` (L424-438) and its call (L422). Its text ("Pick a book, chapter, and version… All six versions are public domain… ASV and Darby include translator notes") is wrong as soon as WS1 lands.
- [ ] **`visual_stage.py`:**
  - The suffix probe in `_find_image` (L197-213) becomes `[""]`.
  - Remove `VerseContext.translation`/`.notes` (L75-76), the notes overlay (L405-427; the label is at L408), the cache keys with translation (L334, L466) and `ctx.notes` passed to `set_verse` (L468).
- [ ] **`svg_stage.py`:** remove the notes band: CSS L76-78, div L84, JS L110-117 ("Translator-supplied words:" L112), `_notes` L139-168 and `/state` L194-203.
- [ ] **Audio:**
  - `audio_studio.py`: `_LABEL_TO_CODE` L36-38, Translation combo L118-125, the "every translation you render" warning L134-138, and translation threading L202-302.
  - `generate_showcase_audio.py`: delete `_migrate_manifest` (L73-86) and its call in `_load_manifest` (L89-98). `TRANSLATION` stays `"WEB"`, so `_manifest_key` still yields `Book_c_v.WEB` (D11).
- [ ] **Video:**
  - `video_render.py`: `RenderSpec.translation` L412; `--translation` L1263, L1286; the `resolve_svg` suffix chain L300-327 (L320); `TRANSLATION_ATTRIBUTION` L77, L537, L1157 becomes `passages.ATTRIBUTION`.
  - `video_studio.py`: `_LABEL_TO_CODE` L32, combo L116-122, RenderSpec argument L291.
- [ ] **Pronunciation:**
  - `pronunciation_tool.py`: docstring L24-29, import L44, `start_translation` L90/L119, combo L140-146, load L208-210, argv L429-441.
  - `pronunciation.py` `_readme` text L62-76: replace the "add KJV spellings" advice with "keys are WEB spellings". Note that "Mahalaleel" is WEB's own spelling at Luke 3:37.
- [ ] **Coverage:** `_scan_audio` (L135-152) and `_fmt_chapter` (L221-224) become a single audio count.
- [ ] **SVG Studio variant model (D9):**
  - `svg_studio.py`: L33 import; L63-64 `TRANSLATION_CODES`/`GENERIC`; L90-115 `variant_path`/`existing_variants`/`resolve_for_translation`; L182-190 chips and the "readers get" readout; L336-361; L417-426 copy-to-variant; L554-556 the rerun note; L651-657 freeze-and-continue variant handling.
  - `svg_preview.resolve_audio` (L113-128) becomes `Book_c_v.mp3`.
  - `svg_registry.py` L39, L66: drop `translation_suffixed`.
  - `svg_generators.json`: drop `translation_suffixed` from all 23 families, and rewrite the Genesis 5 spec text ("name-variant tables used by resolve_names()").
  - `build_manifest.py`: fix the comments at L4, L69-83, L153-156. Add a warning when any file matches `.(KJV|ASV|BBE|BSB|DARBY|DRA|YLT|OEB|WEB).` so a stale backup copied back in gets caught.
- [ ] **Genealogy and Luke 3 generators:**
  - `generate_genealogy.py`: `NAME_VARIANTS` (L50-75) and `resolve_names` (L83-109) go. The first variant is already WEB's spelling for all 26 keys, so use `G5_KEYS`/`G11_KEYS` directly. Delete the broken `__main__` (L669-706), which calls an undefined `render_chapter`. Keep `G_FRAMES`, `G_FRAME_MS`, `ChapterData`, `build_*_specs` and `draw_frame_on`.
  - `generate_genealogy_svg.py` main (L53-86): one generic render, no `time.sleep` loop.
  - `generate_luke3.py`: `extract_line` reads WEB only. Drop the OEB `_names_from_list` (L83-93) and the `Noe` variant (L62). Delete the broken `__main__` (L249-278) and the dead raster helpers `tree_segments`, `root_points`, `draw_tree`, `draw_glow` (L180-195, 211-240). **Keep `strata_bands`** (L197-208), which is live, and the v23 "Jesus" exclusion.
  - `generate_luke3_svg.py` main (L549-576): one render.
- [ ] **Versification:**
  - `generate_romans_svg.py`: set `CH_LEN[16] = 24`, replace the "MAXIMUM across every translation" comment (L83-89), and delete the dead doxology branch `since(pos, 16, 25)` (~L2446-2466).
  - `generate_acts1518_svg.py`: in `main()` (L1237-1244), skip verses WEB lacks. Keep `CH_LEN[15] = 41` for the `P()` maths, and drop the empty caption `34: ""` (L815).
  - Generators iterate `passages.verse_numbers()`.
- [ ] **Stale docstrings:**
  - generate_matthew1_svg.py L35-40 and `stale_files()` (L58-70; a no-op after 1c); generate_acts1518_svg.py:26-27; generate_acts1314_svg.py:487; generate_1chronicles.py:28;
  - prose that cites config.json's `translation` key (removed above) or other versions: generate_hebrews_svg.py:63-66 ("per config.json … all nine translations agree … one set of files serves every version"), generate_exodus28_svg.py:43 ("per config.json"), generate_zephaniah_svg.py:33 ("config.json"). Replace with "WEB is the only text (passages.TRANSLATION)".
  - `wrangler.toml:1-3` comment: "AV Bible" → "Theoria", and `/bibles/<CODE>/` → `/bibles/WEB/`. Commit it with 1c.
- [ ] **Delete `prefetch_translations.py`.**
- [ ] **Slim `import_translation.py` to a WEB-only USFX re-importer (~150 lines).** It must keep writing `"translation": "WEB"`. Before trusting it, dry-run it into a temp dir and diff all 1,189 files against `bibles/WEB`; both were last touched in the initial commit.
- [ ] **`test_svg_freeze.py:269-273`:** repoint `Genesis_5_3.KJV.svg` to `Genesis_5_3.svg`.

**1b. Web translation removal (same push as 1c)**
- [ ] `index.html:26-28`: delete the Translation `<select>`. Attribution (L40) becomes static text (moved to a footer in WS2).
- [ ] `app.js`:
  - the import (L1), `els.translation`/`els.attribution` (L9, L13);
  - `populateTranslations` (L120-124) and its boot call (L661), and the restore at L668;
  - `translation` in `saveSelection` (L173);
  - `code` and the attribution in `loadChapter` (L185, L189); call `fetchChapter(book, chapter)` (L191);
  - the change listener (L434);
  - `ctx.translation` (L309) and `(${passage.translation})` (L311);
  - the stale OEB comments (L221, L237) and the "Keyed by translation" audio comment (L95-98).
  - **`resolveAudio` (L112) becomes the constant `${key}.WEB`**, so it no longer depends on the JSON field.
- [ ] `data.js:48-65`: delete `TRANSLATIONS`/`TRANSLATION_ATTRIBUTION`, and `translation` in `DEFAULTS` (L68).
- [ ] `bible.js`: drop the import (L4); use constant base `/bibles/WEB` (L17); drop `code` from the cache key (L15); make the 404 message translation-free (L25-26).
- [ ] `visuals.js:158`: remove the suffix list; drop the comments at L5-6 and L141.
- [ ] A returning visitor with saved `{translation:"KJV"}` is handled automatically once the select and field are gone. Without this, today's code would request `/bibles//Book_ch.json`.

**1c. Data deletion (one dedicated commit; push 1a + 1b + 1c together)**
- [ ] The 8 other translations, 17,636 files:
  - **(Git Bash)** `git rm -r -q bibles/{ASV,BBE,BSB,DARBY,DRA,KJV,OEB,YLT} deploy_bundle/bibles/{ASV,BBE,BSB,DARBY,DRA,KJV,OEB,YLT}`
  - **(PowerShell)** `foreach ($c in 'ASV','BBE','BSB','DARBY','DRA','KJV','OEB','YLT') { git rm -r -q -- "bibles/$c" "deploy_bundle/bibles/$c" }`
- [ ] Suffixed files, **1,736 in all**: 836 × 2 visuals (547 animated + 289 stills such as `Genesis_11_10.BSB.still.svg`) plus 32 × 2 MP3s. The `(still\.)?` group is required; without it the stills don't match and only 1,158 files go.
  - **(Git Bash)**
    ```
    git ls-files -z -- visuals deploy_bundle/visuals web/audio deploy_bundle/audio \
     | grep -zE '\.(ASV|BBE|BSB|DARBY|DRA|KJV|OEB|YLT)\.(still\.)?(svg|mp3)$' | xargs -0 git rm -q --
    ```
  - **(PowerShell)**
    ```
    git ls-files -- visuals deploy_bundle/visuals web/audio deploy_bundle/audio |
      Where-Object { $_ -match '\.(ASV|BBE|BSB|DARBY|DRA|KJV|OEB|YLT)\.(still\.)?(svg|mp3)$' } |
      git rm -q --pathspec-from-file=-
    ```
  - Check first by swapping the `git rm` for a count; expect 1,736.
- [ ] Orphan verses (× 2 with the bundle): `visuals/Romans/16/Romans_16_25.svg`, `Romans_16_25.still.svg`, `Romans_16_26.svg`, `Romans_16_27.svg`, `visuals/Acts/15/Acts_15_34.svg`.
- [ ] Remove the 32 `.KJV` keys from `web/audio/manifest.json`.
- [ ] `prepare-deploy.ps1` **needs no change**. It copies whatever `bibles/` subdirectories exist (Get-ChildItem -Directory). `audio_studio.count_deploy_files` also corrects itself.
- [ ] Run `build_manifest.py`, then `prepare-deploy.ps1`, then commit with a hand-written message. The 1b shell edits go in the same push under the §4 bundle rule.

**1d. Pronunciation prune (D13; its own commit)**
- [ ] Scripted, using `respell()`'s rule (whole word, case-sensitive):
  1. Re-key the 24 hyphenated entries that have a WEB spaced form (statuses: ok 9, fixed 8, suggested 5, unfixed 2).
  2. Move the other 194 to `pronunciations_archive.json`.
  3. Never drop a `BOOK_NAMES` token; none of the 218 is one. Note that `fathers'` is among the 218 and isn't a name.
- [ ] **Regression check.** Before and after the prune, dump `pronunciation.respell(text)` for all 31,098 WEB verses (one line per `Book c:v`) and diff the two dumps. Expect changes only in verses that contain one of the 24 re-keyed WEB spaced forms; the 194 archived keys never match WEB text, so they change nothing. Confirm the entry count is 3,137 (no re-keyed name collides with an existing spaced key). The changed verses will then show as stale narration (S3) and join the §6.1 re-render list.
- [ ] Re-verify the 8 re-keyed "fixed" names in the Verifier: `Beth Zur`, `Jushab Hesed`, `Ir Nahash`, `Ben Hanan`, `Baal Meon`, `Baal Hermon`, `Merib Baal`, `Baal Perazim`.
- [ ] Regenerate `PRONUNCIATIONS.md` (`python pronunciation.py`) and `PRONUNCIATION_TODO.md` (`regen_pronunciation_todo.py`).

**1e. Local-only tidy (nothing to commit)**
- [ ] Delete `cache/passages` (1,234 files, 1,190 of them BBE).
- [ ] Delete the 7 non-WEB source XMLs in `bibles/` (52.1 MB). Keep `eng-web.usfx.xml`.

**Dependencies and what breaks if done out of order.**
- If **1c runs before 1a**, the "api" fallback makes any re-run of Genesis 5/11 or Luke 3 download five translations and write `.KJV.svg` and similar files again. The PC Version combo also silently goes online.
- If **1c ships without 1b**, the old web picker offers KJV and 404s.
- **1a must be one commit**, because 10 modules import `TRANSLATIONS`, `TRANSLATION_LABELS` or `TRANSLATION_ATTRIBUTION`.

**Effort.** 1a is M; 1b–1e are S each. About 2–3 focused sessions.

**Risks.**
- `Passage(**data)` raises a TypeError if the dataclass loses fields and the loader doesn't filter keys. That breaks every chapter load.
- If the web audio key changes but the producers don't, narration silently falls back to robotic Web Speech.
- A missed importer stops the app starting with no visible error. Launch with `.venv\Scripts\python.exe app.py`, not `pythonw`, during this work.

**Verify.**
- [ ] Code search:
  ```
  git grep -n -E "TRANSLATIONS|TRANSLATION_LABELS|TRANSLATION_ATTRIBUTION|fetch_public|fetch_esv|translation_suffixed|show_notes|esv_api_key|polite_throttle" -- "*.py" "*.json"
  ```
  Expect zero hits, apart from `import_translation.py`'s own WEB constant if it is kept.
- [ ] Prose search, since the grep above misses docstrings: `git grep -n -i -E "translation|KJV|nine" -- "*.py"`. Review every hit against the expected residue: `import_translation.py`, the `TRANSLATION`/`ATTRIBUTION` constants and their uses, and `generate_showcase_audio`'s `.WEB` key.
- [ ] **(Git Bash)** `git ls-files bibles | cut -d/ -f2 | sort -u` returns `WEB` (and nothing else under bibles but the 1,189 files).
- [ ] **(Git Bash)** `git ls-files | grep -cE '\.(ASV|BBE|BSB|DARBY|DRA|KJV|OEB|YLT)\.'` returns 0 (it returns 578 if the 1c regex missed the suffixed stills).
- [ ] The visuals manifest has 2,244 keys; the audio manifest has 2,352 (2,348 after D15).
- [ ] Re-run `generate_genealogy_svg.py`, `generate_luke3_svg.py` and `generate_romans_svg.py`, then `git status --short visuals/Genesis visuals/Luke visuals/Romans`. Expect no change against the 0.8b baseline: the outputs are byte-identical and Romans 16:25-27 is not re-created.
- [ ] `test_svg_freeze.py`: 20 tests pass. `test_imports.py` and `test_registry.py` pass.
- [ ] Web, served by the `web-static` launch config on `deploy_bundle`:
  - Genesis 5:9 shows Enosh, Kenan and Mahalalel; Luke 3:36 renders.
  - Romans 14:24-26 shows the doxology; Romans 16 ends at 24; Acts 15 goes 33 → 35.
  - Genesis 1 plays neural MP3s (the Network tab shows `Genesis_1_1.mp3`).
  - With `localStorage['avbible.web.selection']` set to `{"translation":"KJV","book":"Genesis","chapter":5}`, the page loads WEB and no request goes to `/bibles/KJV`.
- [ ] PC:
  - The app launches and plays Genesis 1.
  - Audio Renderer, Video Studio, Pronunciation Studio, SVG Studio and Coverage open with no translation controls.
  - Coverage shows Romans 16 as 24/24 and Acts 15 as 40/40.

### WS2 — Web UI simplification

> **Status (2026-10-16): done, pushed as `442a6d8a`; Cloudflare's Workers Build succeeded.**
> - **Checked** on the web-static server at 375×812 and desktop. An adversarial review found 1 major issue (the progress line was truncated at 375 px) and 9 minor ones; all are fixed and re-tested.
> - **Beyond the plan:**
>   - Prev/Next/Play shrink to icons on phones.
>   - The ✦ dialog makes the page behind it inert.
>   - Wake Lock is held across chapter rollovers.
>   - Stored selections are validated.
>   - `findVisual` prefers `.svg`.
>   - The pointer sits in the lower part of the stage, clear of the center Play button.
> - **Still to check on a real iPhone:** Wake Lock (the test browser refuses the permission) and pinch-zoom.

**Goal.** A two-row header, no toggles row, a stage that never shows stale text and points to ✦ when a verse isn't illustrated, no still code left in the web app, and a few fixes that were never built (Wake Lock, focus handling, keyboard access).

**Final web control list (D5)**

| Control | Today | After |
|---|---|---|
| Translation select | header | **removed** (WS1b) |
| Book, Chapter | header | kept |
| "Start at verse" | header (it tracks the playing verse, so "start at" is misleading) | renamed **Verse** |
| ✦ Illustrated | header | kept; focus moves into the dialog and back |
| Notes checkbox | toggles row (mislabelled footnotes) | **removed** |
| Still graphics checkbox | toggles row | **removed**, with all still code; no reduced-motion support (D4) |
| Speed slider 0.6–1.6 | toggles row; not saved; only takes effect at the next verse; no readout | **removed** (D5); narration plays at 1× |
| Prev / Play-Pause / Next | transport | kept |
| Fullscreen ⛶, landscape auto-fullscreen, double-tap, Space / ← / → / Esc | stage | kept |
| Attribution | header, per translation | static footer: "Scripture: World English Bible (public domain)" |
| Progress line | "Verse 3 of 31 — Genesis 1:3 (WEB) · neural narration" | "Genesis 1:3 · 3/31" |

Layout:
- Row 1: brand, with ✦ on the right.
- Row 2: Book (flex 2), Chapter, Verse.
- Transport: `[←] [▶ Play] [→]  Genesis 1:3 · 3/31`.
- About 80 px of portrait height goes back to the stage.

**2a. Safe deletions (no data dependency)**
- [ ] **Notes:**
  - index.html: notes box (L51) and checkbox label (L65);
  - app.js: L20, L26, the comment at L39, L292, L310, L328-329, L363-366, L431;
  - style.css: L290-306 and the comment at L252-253;
  - visuals.js:17; bible.js:2-3 comment.
- [ ] **`.mobile` lookup** (0 such files exist anywhere): delete visuals.js `MOBILE_QUERY`/`isMobileScreen` (L59-69) and the suffix expansion (L154-161). Move the misplaced `hashBook` comment (L56-58).
- [ ] **Manifest v1 normaliser:** visuals.js L36-54, L101-107. v2 shipped 2026-07-12 and the manifest is fetched `no-cache`.
- [ ] **Raster machinery and dead helpers:**
  - visuals.js: `EXT_PRIORITY`/`pickBestRecord`/`ANIM_EXTS`/`PHOTO_EXTS` (L10-34), `findImage` (L179-183, never called), `isDiagram` (L185-188);
  - app.js:342-343;
  - style.css:224 and L228 (always letterbox);
  - also the stale `findImage` docstring at svg_studio.py:105-109.
- [ ] **Storage guard:** add a `safeGet`/`safeSet` helper. The unguarded `localStorage` call at app.js:67 runs at import time and stops the whole app from starting when storage throws. `saveSelection` (L170-177) is unguarded too.
- [ ] **D16 choices:** the storage-key rename (app.js:36), dropping `maximum-scale=1` with 16px selects, and the Genesis 1 default (data.js:67-71).
- [ ] **Metas:** add `<meta name="mobile-web-app-capable" content="yes">` (index.html:9) and `"id": "/"` in `manifest.webmanifest`.
- [ ] **Progress text:** app.js:311 and L368-371. Rename the label at index.html:35. Keep one copy of the idle text (index.html:48-50 duplicates app.js:289).

**2b. Empty stage (D6)**
- [ ] Delete `visuals/default.txt` (and its bundle copy).
- [ ] Remove the text-visual feature:
  - visuals.js `TEXT_EXTS` (L17-19) and `loadText`/`rtfToPlainText` (L194-241);
  - app.js `stageText` (L18), `showIdle`'s `els.stageText` line (L291), `stageTextToken` (L42) and L327-338, L340-341, L356-357;
  - index.html `#stage-text` (L47);
  - style.css L252-274.
- [ ] `findVisual` looks up the verse key, then the chapter key, and nothing else (visuals.js:148-153).
- [ ] **The "not illustrated yet" pointer (D6).** Add one element inside `#stage`, e.g. `<div id="stage-empty">`, which `renderVerse` shows whenever `findVisual` returns nothing and hides otherwise (the `else` branch at app.js:355-361 today). It holds:
  - the reference, centred ("Genesis 12:3");
  - one line: "Genesis 12 isn't illustrated yet." when `stage.illustratedChapters().get(book)` lacks the chapter, otherwise "This verse isn't illustrated yet.";
  - a **✦ See illustrated chapters** button that calls `openIllustrated()` (app.js:485).
- [ ] The button handler calls `e.stopPropagation()`, so the stage's tap-to-reveal and double-tap prev/next handlers (app.js:503-539) don't also fire.
- [ ] In fullscreen it calls `setFullscreen(false)` (app.js:543) first. The ✦ overlay sits outside `#stage-wrap`, and real `requestFullscreen()` (L545-546) renders only the fullscreen element, so otherwise the list would open invisibly.
- [ ] Style it small and quiet, below the reference rather than over the middle of the stage, so the book gradient stays the main thing on screen.
- [ ] `build_manifest.py`: drop `.txt`/`.rtf` from `IMAGE_EXTS` (L51-58). README and CREDITS then stop being indexed as "note" visuals.
- [ ] The PC fallback is the same feature (visual_stage.py:192, L290-345) and goes in WS5.

**2c. Audio details**
- [ ] Fetch `audio/manifest.json` with `cache: 'no-cache'` (app.js:101), like the visuals manifest.
- [ ] Apply D15: `git rm web/audio/Psalms_119_[1-4].mp3 deploy_bundle/audio/Psalms_119_[1-4].mp3` (git expands the glob, so it works in either shell), remove the 4 `Psalms_119_*.WEB` manifest keys, and commit by hand.

**2d. Polish**
- [ ] **Remove the Speed slider (D5):** index.html:67-69, app.js:28 (`rateSlider`) and L432 (the `input` listener). The tts.js Player keeps `this.rate = 1` (tts.js:30) as a constant for Web Speech; MP3s play at their natural speed.
- [ ] **Remove the toggles row:** index.html:64-70; style.css:415-424 and the `.toggles` rule in the L457 media query.
- [ ] **In the same commit, remove the entire web still path (D4)**, or the site goes blank: `initMotionToggle()` runs at module load (app.js:82) and does `els.chkMotion.checked = …` (L68), so with `#chk-motion` gone it throws a TypeError during module evaluation and `boot()` (L676) never runs.
  - app.js:27 (`chkMotion`); L41 and L315 (`lastRenderedIndex`); L44-50 (comment and `STILL_KEY`); L51-57 (`REDUCED_MOTION`, `prefersReducedMotion`); L59-82 (`rerenderCurrentVerse`, `initMotionToggle` and its call).
  - L320-326: the `imgPath` choice becomes `visual ? visual.url : null`.
  - visuals.js:143-144 and L168 (`stillUrl`).
  - Leave the `?r=Date.now()` branch (app.js:344-352) for now; WS7a replaces it.
  - Optionally clear the old choice once: `localStorage.removeItem('avbible.web.stillGraphics')`, inside the 2a storage guard.
  - The notes checkbox and its JS (L26, L431) already went in 2a. The Speed slider's JS (L28, L432) goes with the item above, which must land in this same commit.
  - The `.still.svg` files themselves stay on disk until WS3c; nothing in the web app reads them after this commit.
- [ ] **Header and footer:** index.html:19-41; style.css:189-195 rules reused for the footer.
- [ ] **Screen Wake Lock** (~15 lines): call `navigator.wakeLock?.request('screen')` while playing, release it otherwise, and re-request on `visibilitychange`. It was planned in WEB_PLAN.md:69 and never built.
- [ ] **✦ dialog focus:** move focus in on open and return it on close (app.js:485-491).
- [ ] **Verse panel keyboard access:** `tabindex=0`, `role=button` and an Enter/Space handler (app.js:260-273).
- [ ] Optional: say "Psalm 23:1" rather than "Psalms 23:1" in references.

**2e. Ship**
- [ ] Apply the §4 bundle rule to every WS2 commit: run `prepare-deploy.ps1`, commit the `deploy_bundle` shell files with the `web/` edits, and check on `web-static`. Pushing the `web/` edits alone changes nothing on the site.

**Dependencies and what breaks.**
- The WS1b picker removal must ship in the same deploy as the bibles deletion.
- **Every element removed from `index.html` loses its JS in the same commit.** app.js looks elements up at module load (L9-33) and calls methods on them there (L82, L431-434), so one `null` throws during module evaluation and the whole site goes blank. This applies to the translation select (WS1b), the notes box and checkbox (2a), `#stage-text` (2b) and the toggles row (2d).
- 2b changes the PC stage too, which uses the same `default` fallback; that is harmless.
- The rest is independent of the other workstreams.

**Effort.** S per item, M overall.

**Risks.**
- Layout at 375 px has not been rendered, so check it.
- Wake Lock in an installed iOS home-screen app reportedly needed a later iOS fix. Feature-detect it and fail silently.

**Verify.**
- [ ] Chrome DevTools at 375×812 (mobile preset): header in two rows, no horizontal scroll, the progress line on one line.
- [ ] After every WS2 commit, load the page with the DevTools Console open: no errors, and Genesis 1 plays.
- [ ] Block site data in Chrome: the app still boots.
- [ ] Genesis 12:3 shows the gradient, the reference and "Genesis 12 isn't illustrated yet.", not the old text panel. **(Git Bash)** `grep -c '"default"' visuals/manifest.json` returns 0.
- [ ] Genesis 1:3 shows its visual and no pointer. (No illustrated chapter is partial today, so test the "This verse…" wording by pointing `findVisual` at a missing key in DevTools, or wait for the first partly built chapter.)
- [ ] The ✦ button on the pointer opens the illustrated list, both normally and from fullscreen (fullscreen exits first), and tapping it doesn't skip a verse.
- [ ] No Speed control, Still graphics checkbox or toggles row is left; **(Git Bash)** `grep -n -E 'stillUrl|STILL_KEY|prefersReducedMotion|REDUCED_MOTION|rateSlider|chkMotion' web/js/*.js` finds nothing.
- [ ] Pinch-zoom works on Android.
- [ ] Tab into the ✦ dialog; Esc returns focus to ✦.
- [ ] On the iPhone, the screen doesn't dim during a 5-minute chapter.

### WS3 — Retire the reduced-motion stills

> **Status (2026-10-17): done, pushed as `a92ac8dc` (3b `7c2ef29e`, 3c `9c30c3f0`); Cloudflare's Workers Build succeeded.**
> - **Done:** 2,646 `.still.svg` deleted and none recreated by a publish dry run. `build_stills.py` is gone, and Publish is three steps.
> - **Checks:** the manifest keeps the same 2,241 keys and records minus `still`. 19 tests pass (14 freeze, 4 registry, 1 import sweep). SVG Studio's "Save + manifest" succeeds.
> - **Numbers:** deploy bundle 7,128 → 5,805 files; tracked files 11,729.
> - **Review:** the adversarial review found no blocker or major issue.
> - **Beyond the plan:** `build_manifest` skips and reports any `.still.svg` copied back from `backups/` (which holds 1,405); `test_registry` fails on one; `svg_is_animated` keeps two test assertions.

**Goal.** Zero `.still.svg` files and no stills step anywhere. There is no reduced-motion replacement (D4), so this is deletion only: the web side already went in WS2d, and what is left is the Python side (3b) and the files (3c).

**Order. Follow it exactly:** WS2d deployed → 3b → 3c.

**3b. Python stops making stills (one commit, before any file deletion)**
- [ ] `publish_studio.py`: remove L5 and the top-level `import build_stills` (L34). Remove step 1 (L180-188) and renumber "1/4…4/4".
- [ ] `svg_studio.py:799-820`: remove the stills refresh in `_manifest_worker`, including the lazy import at L801 and `still_note` at L816. If it stays, Save + manifest stops rebuilding the manifest and shows "No module named build_stills".
- [ ] Leave `build_manifest.py` alone in this commit; its still logic changes in 3c. If the `STILL_SUFFIX` skip goes while `.still.svg` files still exist, the next manifest rebuild (SVG Studio's Save + manifest runs one) indexes each still as its own verse key, e.g. `Acts_13_1.still`.
- [ ] `svg_freeze.py`: delete `strip_remaining_animations` and `freeze_still` (L131-176), and drop the build_stills mention from the `svg_is_animated` docstring (L51-53). Keep `freeze_animations`/`freeze_to_base` for now: SVG Studio's "Start from prev. frame" still calls `freeze_to_base` (svg_studio.py:667). Studio phase 2 retires that button (D12), and its 11 tests go with it.
- [ ] `test_svg_freeze.py`: delete `StillCases` (L171-252, 6 tests) **and remove `freeze_still` from the top-level import (L11-12)**; otherwise the whole module fails with ImportError. `.venv\Scripts\python.exe -m unittest test_svg_freeze` then reports 14 tests.
- [ ] `generate_matthew1_svg.py`: remove the still references at L62-68 and L134.
- [ ] `app.py:573`: fix the docstring.
- [ ] Delete `build_stills.py` (112 lines). Leave the house note in `generate_genesis3_svg.py:402-409`; it is harmless.

**3c. Delete the files (dedicated commit)**
- [ ] `git rm -q -- '*.still.svg'`. The pathspec matches at every depth. It removes 1,323 per copy (WS1 already removed 289 suffixed stills and 1 orphan).
- [ ] In the same commit, `build_manifest.py`: remove `STILL_SUFFIX` (L54) and the still attach and orphan report (L30-31, L144-186). **Keep `svg_is_animated`** (L44, L111), because the manifest keeps its `animated` field (D11). Nothing in the web app reads it today; it costs nothing and keeps the schema stable.
- [ ] Run `build_manifest.py` and `prepare-deploy.ps1`, then commit. Don't run any manifest rebuild between the `git rm` and the `build_manifest.py` edit.

**Dependencies and what breaks.**
- 3b before 3c. Otherwise the next Publish rewrites and commits all 1,613 stills.
- 3b must edit `publish_studio.py` before `build_stills.py` is deleted. Otherwise `app.py` dies on import (app.py:21 imports `publish_studio`, which imports `build_stills` at L34), silently, because `run.bat:16` launches `pythonw`.
- 3b must edit `test_svg_freeze.py`'s import in the same commit that deletes `freeze_still`, or every later test run (0.9 trio, WS4 verify) fails at import.
- WS2d before 3c: once the files are gone, any web code still asking for `stillUrl` would request missing files.
- `video_render.py` and `svg_preview.py` don't use stills; Video Studio is unaffected.

**Effort.** S.

**Risks.**
- Low. The one trap is the order: deleting `build_stills.py` before editing `publish_studio.py` stops the Studio from starting (see above).

**Verify.**
- [ ] **(Git Bash)** `git ls-files | grep -c '\.still\.svg$'` returns 0. `grep -c '"still"' visuals/manifest.json` returns 0.
- [ ] `python -m unittest test_svg_freeze` runs 14 tests, all passing; `test_imports.py` and `test_registry.py` pass.
- [ ] The app launches with `python.exe`. Press SVG Studio "Save + manifest" on Genesis 1:1: the status shows success.
- [ ] **Publish dry run.** Until a dry-run box exists (WS4), run `python build_manifest.py`, then `powershell -File prepare-deploy.ps1`, then `git status --short -- web visuals bibles deploy_bundle`. Expect no new `.still.svg`, then discard.
- [ ] On the live site, Genesis 1:1 and Exodus 26:1 still animate, and the Network tab shows no request for a `.still.svg`.

### WS7 — Shared visuals: one SVG across several verses (D17)

> **Status (2026-10-17): done, pushed as `ffef57c0`; Cloudflare's Workers Build succeeded.**
> - **Checks:** 125 verses share the previous verse's picture (Numbers 32:16-32 are one picture with one download). Play on the verse already shown still restarts its picture, so it stays in step with the narration. A real Video Studio render of Numbers 32:15-20 draws the trace once. 33 tests pass, 14 of them new.
> - **Beyond the plan:**
>   - single-verse and past-the-end ranges are handled;
>   - overlapping ranges have a deterministic winner;
>   - a range file is never taken over by a copy;
>   - Video Studio honours the opt-out and restarts copies at a chapter boundary;
>   - a picture that fails to load is retried.
> - **Not done:** the `out_path` companion. Generators already pass any filename to `out_path`, so it isn't needed.
> - **Known gaps:**
>   - SVG Studio doesn't know range files yet (roadmap §6.3, "Shared visuals in the Studio").
>   - The interim PC stage (`visual_stage.py`) doesn't look them up. It is retired after S4.

**Goal.** When the next verse shows the same picture, it keeps playing instead of starting over. One SVG can be tied to a range of verses on purpose, and today's identical copies are treated as one picture automatically.

**What happens today (measured 2026-10-16).** No two manifest keys share a file. But 125 consecutive verse pairs (62 runs) are byte-identical copies, and because each copy has its own URL, the browser treats each verse as a new image and replays its animation. 33 of those repeats are animated:
- Numbers 32 (19 verses, e.g. 32:17-32): a stroke-dash trace visibly redraws the same line on every verse. This is the replay you have been seeing.
- 1 Chronicles (13): the camera animates from a position to the *same* position, so the replay is invisible.
- Exodus 25:2 (1): a loop restarts its phase.

Video Studio does the same: every verse's SVG is timed from zero (video_render.py:594), including the previous verse's artwork when a verse has no visual of its own (L497-501).

**7a. The playback rule (web, so also the Studio Preview)**
- [ ] app.js:344-352: replace the `?r=Date.now()` restart branch with "if `imgPath === lastImagePath`, leave the `<img>` alone". The animation keeps running, or stays finished, and nothing is downloaded again.
- [ ] Keep `lastImagePath = null` wherever the image is hidden (app.js:332, L360, `showIdle`), so coming back from idle or from an un-illustrated verse loads the picture fresh and plays it once.
- [ ] Behaviour to expect: Prev, Next and the verse picker inside a shared run don't restart the picture; jumping into the middle of a run from outside plays it once. The rule is "restart only when the picture changes."

**7b. Tying one SVG to a verse range on purpose**
- [ ] Naming: `visuals/<Book>/<ch>/<Book>_<ch>_<v1>-<v2>.svg`, e.g. `Numbers_32_16-32.svg`.
- [ ] `build_manifest.py`: expand a range stem into one key per verse (`Numbers_32_16` … `Numbers_32_32`), every key pointing at the same file. A per-verse file inside the range wins over the range for that one verse; report the overlap as a warning (an S3 lint warning later).
- [ ] `video_render.resolve_svg` (L299-327) finds visuals by path, not through the manifest, so it also needs to look for a range file covering the verse (until Studio phase 2's single resolver reads the manifest instead).
- [ ] Generators get a small `out_path` companion in `generate_tabernacle.py` for writing a range file. It is used only when a generator chooses to; nothing is converted now.

**7c. Today's identical copies, automatically**
- [ ] `build_manifest.py`: walk each chapter in verse order. When a verse's SVG is byte-identical to the previous verse's, point its manifest record at the **first** file of the run. With 7a, the 62 runs then hold instead of replaying. No generator changes and no file deletions are needed; the copies stay on disk.
- [ ] It maintains itself: once a generator makes two verses differ, the next manifest build stops treating them as one picture.
- [ ] Opt-out: a registry flag `"replay_identical": true` on a family keeps per-verse replays. No family uses it today.

**7d. Video Studio**
- [ ] When a verse's SVG text equals the previous item's (an identical copy, a range file, or the held artwork for a verse with no visual), continue the previous item's clock: render its frames from `t = previous offset + previous duration` instead of from 0, and compute `motion_seconds` against that offset (video_render.py:590-596). Play-once art then stays finished, and loops continue without a jump.

**Not changed:** the interim PC player (`svg_stage.py`) still re-injects per verse. It is deleted after the S4 Preview checklist passes, and the Preview runs the real web app, which follows 7a.

**Order and dependencies.** After WS1 (no suffixed keys left) and WS3c (both edit `build_manifest.py`). Web code follows the §4 bundle rule.

**Effort.** S for 7a and 7c, S for 7b, S–M for 7d.

**Verify.**
- [ ] Web, Numbers 32:16 → 32:32: the trace draws once at 32:16 and holds through 32:32; the Network panel shows one request for the shared file.
- [ ] Opening Numbers 32:20 directly plays the picture once.
- [ ] Genesis 1:1 → 1:3 (different pictures) still animate on every verse.
- [ ] **(Git Bash)** `grep -c '"file": "Numbers/32/Numbers_32_16.svg"' visuals/manifest.json` returns 17 (vv16-32).
- [ ] A Video Studio render of Numbers 32:16-20 shows the trace once.
- [ ] A test range file (`Genesis_12_1-3.svg` in a scratch copy) gives three manifest keys and holds across the three verses.

### WS4 — Repo and deploy hygiene

> **Status (2026-10-17): 4a–e done, pushed as `3d133a4f`; Cloudflare's Workers Build succeeded.** 4f and 4g are not started.
> - **Checks:** tracked files 11,716. Every generator re-ran with output unchanged against the 0.8b baseline. 33 tests pass, and `isbe_sweep.py` is import-tested again.
> - **Moved out:** `backups/`, `renders/`, `_scratch/` and `mockups/figures/` are now in `C:\Dev\Theoria-archive\` (`config.ARCHIVE_DIR`, `config.RENDERS_DIR`). The archive copies were verified identical before the repo copies were removed. `deploy_temp/` and the old deploy scripts are deleted.
> - **Beyond the plan:**
>   - Publish's web-code guard covers all of `web/` except `web/audio`, plus new untracked files.
>   - The 1 Chronicles back-up-once step is dropped, like Matthew 1's. With the archive moved, it would have saved the current design under the old design's name.
>   - The 1 Chronicles `--dry` size report works.
> - **4f still needs** the Cloudflare build log (Step 0.2).

**Goal.** Publish commits only content. The deploy is fully defined in the repo. Dead modules and clutter are gone. Optionally, `deploy_bundle` is retired and history is slimmed.

**4a. Publish correctness (beyond the Step 0.7 pathspec and `CONTENT_PATHS` fixes)**
- [ ] Optional guard: Publish warns when `git diff --quiet HEAD -- web/js web/css web/index.html` fails, so you know unfinished web code is sitting in the working tree (and in the bundle copy, which 0.7 keeps out of the commit). Under D7(c) `CONTENT_PATHS` becomes `web/audio`, `web/visuals`, `web/bibles`.
- [ ] `commit_message` (L76-86) counts only `visuals/` and MP3s. Make it count deletions and the bibles, and stop counting `deploy_bundle` copies.
- [ ] Add a "Dry run (no commit / push)" checkbox.
- [ ] Rename `CLOUDFLARE_PAGES_FILE_LIMIT` (audio_studio.py:33); this is a Workers static-assets limit. Move `count_deploy_files` (L41-59) into `publish_studio` so Publish and SVG Studio stop importing the Audio Renderer for it.

**4b. Deploy scripts**
- [ ] `prepare-deploy.ps1` is now tracked (Step 0). Delete `deploy.ps1` (the "R2" script that only builds `deploy_temp/`), `deploy-api.ps1` (POSTs to an invented Pages endpoint), `deploy_temp/` (1,037 files, 169 MiB) and their `.gitignore` lines.
- [ ] Fix `svg_chronicles_world.py:77-78` `AUDIO_DIR = deploy_bundle/audio` so it uses `web/audio` (through a config constant). It is the only code that reads the mirror. The 1 Chronicles and Matthew 1 cameras are timed from these MP3s and fall back to an estimated pace when a file is missing.
- [ ] `build_manifest.py:46`: anchor `VISUALS_DIR` on `Path(__file__).parent`. Today it works only when run with cwd = repo root.

**4c. `.gitignore` target**
`.venv/`, `__pycache__/`, `*.pyc`, `config.json`, `.claude/settings.local.json`, `cache/`, `isbe_cache/`, `renders/`, `backups/`, `_scratch/`, `mockups/`, `bibles/*.xml` (or `sources/*.xml` under D7 c), `PRONUNCIATIONS.md`, `PRONUNCIATION_TODO.md`, `node_modules/`, `.wrangler/`, `.DS_Store`, `Thumbs.db`, `desktop.ini`, `~$*`. Add `deploy_bundle/` only under D7(b).
- [ ] `git rm --cached PRONUNCIATIONS.md PRONUNCIATION_TODO.md`. Both are tracked, and an ignore line alone doesn't untrack a file; `pronunciation.save_names` rewrites PRONUNCIATIONS.md on every save (pronunciation.py:230 → L278), which is where its 15 commits of churn came from.
- [ ] `git rm --cached .claude/settings.local.json`. It is a personal permissions list with 19 stale OneDrive paths and no secrets. Keep `.claude/launch.json` and repoint `web-static` at the served directory.

**4d. Dead modules and files**
- [ ] `generate_1chronicles_svg.py` (72 lines) and `svg_1chronicles_render.py` (498). These are the superseded v2 renderer, unreachable after the Step 0 registry fix; their output is archived in `backups/1_Chronicles_svg_v2_camera/`. Update the mentions in generate_1chronicles.py:31, svg_chronicles_world.py:3,324 and INFOGRAPHIC_CANDIDATES.md.
- [ ] The ISBE one-off pipeline, **except `isbe_sweep.py`**: delete `isbe_harvest`, `isbe_to_ipa`, `isbe_apply`, `isbe_benchmark`, `isbe_repair`, `isbe_repair_legacy` (753 lines), plus `name_ipa.py` (171) and `isbe_index.json` (324 KB). All of them were a single 2026-08-04 session; the `pre-cleanup` tag keeps them.
- [ ] **Keep `isbe_sweep.py` (252 lines) and `isbe_harvest.json` (170 KB).** It is the only headless tool that measures names by ear and proposes or adopts respellings; the Verifier measures but generates no candidates, and 616 names are still unfixed. It is self-contained (imports only config, ipa_asr, pronunciation, tts_engine; reads `isbe_harvest.json` beside itself, L39). Fix its hard-coded `sys.path.insert`/`os.chdir(r"C:\Dev\AV Bible")` (L24-25) to use `os.path.dirname(__file__)`, and point `VOICE` (L33) at `tts_engine.HOUSE_VOICE` (WS5). If you'd rather work the backlog only in the Verifier, delete it too.
- [ ] Update the prose that `regen_pronunciation_todo.py:83-92,137` generates (it cites the deleted scripts).
- [ ] `INFOGRAPHIC_CANDIDATES.xlsx`: 212 rows, only 8 marked Built, read by nothing.
- [ ] Dead raster code in live libraries:
  - `generate_tribal_maps.py`: 15 functions, 419 lines (`seg_partial` … `render_32`), `FRAME_A/B/C`, the WebP docstring and the closing comment (L926-930). Keep the data constants and `MapFrame`.
  - `generate_tabernacle.py`: rewrite the docstring (L1-15, still "animated WebP per verse") and remove `pulse()` (L91).
  - `svg_vocab.lying_beast` (L174), `svg_figures._man` (L600), `chronicles_tree.kids_of` (L193) and `P` (L310).
- [ ] Afterwards, regenerate Numbers 32/34 and Acts 13-18 and confirm `git status` shows no SVG changes against the 0.8b baseline.

**4e. Local clutter (disk only)**
- [ ] Before moving `backups/` out of the repo, fix the code that depends on it:
  - `generate_matthew1_svg.py:55,82-86` **refuses to run** without `backups/matthew1_fractal_tree`. Its check also runs before `--dry`. Replace it with a create-once backup like `generate_1chronicles_tree_svg.py:31-40`, or drop it.
  - `generate_1chronicles_tree_svg.py:28-39` copies into `backups/`. Point both at a `config.ARCHIVE_DIR`.
- [ ] Then move `backups/` (245 MiB) and `renders/` (356 MiB) to `C:\Dev\Theoria-archive\`. Keep `backups/{png,webp}_replaced_by_svg` until any history rewrite is finished.
- [ ] Move `cache/ipa_checks.json` to a tracked `data/ipa_checks.json` via config. It is read and written by pronunciation_check.py:46, isbe_sweep.py:35 (kept), isbe_repair_legacy.py:34 (deleted) and regen_pronunciation_todo.py:12; repoint all three survivors through one config constant.
- [ ] `_scratch/`: prune, only after 0.3b has moved the two reused scripts into `tools/` and the 0.3 tar holds the rest. It is ignored after Step 0.
- [ ] `mockups/figures/` (109 throwaway QC SVGs): delete. `mockups/luke3` and `mockups/matthew1` (19 PNGs) go with their docs (WS6).

**4f. Retire `deploy_bundle/` (D7 c; its own push, after WS1 and WS3 are live)**
- [ ] `git mv visuals web/visuals` and `git mv bibles/WEB web/bibles/WEB`. The source XML moves to an ignored `sources/`.
- [ ] Centralise `SITE_DIR`, `VISUALS_DIR`, `AUDIO_DIR` and `BIBLE_DIR` in `config.py`. The sites to update:
  - config.py:11,14; `generate_tabernacle.out_path` (VISUALS at L25, used by 33 modules); build_manifest.py:46; svg_studio.py:45, L811;
  - audio_studio.py:46-49, L56; coverage_studio.py:37-39; generate_showcase_audio.py:55; svg_preview.py:26;
  - generate_ot_family_tree_svg.py:37; generate_1chronicles_tree_svg.py:36; svg_chronicles_world.py:78;
  - chronicles_tree.py:1345; generate_1chronicles.py:43; svg_matthew_world.py:84;
  - test_svg_freeze.py:240, L259; `publish_studio.CONTENT_PATHS`; both `.claude/launch.json` entries.
- [ ] `wrangler.toml`: `[assets] directory = "./web"`. Add `web/.assetsignore`.
- [ ] `git rm -r deploy_bundle`. Delete `prepare-deploy.ps1` and remove Publish step 3 and SVG Studio's "Stage for deploy".
- [ ] Publish becomes: manifest → `git add -A -- web/audio web/visuals web/bibles` → commit → push.
- [ ] Fallback (b), if the dashboard has a custom build: keep the folders where they are, commit `build_site.py`, gitignore `deploy_bundle/` and set the dashboard Build command.

**4g. History slim: not scheduled (D8 chose plain `git rm`); kept here only in case you ask for it later**
1. Start from a clean working tree with D7(c) landed. Make a `git bundle --all` backup.
2. Install git-filter-repo (`py -m pip install git-filter-repo`; pure Python). Mirror-clone the repo.
3. Run **(Git Bash)**:
   ```
   git filter-repo --invert-paths \
     --path-regex '^(deploy_bundle/)?bibles/(ASV|BBE|BSB|DARBY|DRA|KJV|OEB|YLT)/' \
     --path-regex '\.still\.svg$' \
     --path-regex '\.(ASV|BBE|BSB|DARBY|DRA|KJV|OEB|YLT)\.(svg|webp|png|mp3)$' \
     --path-regex '^(deploy_bundle/)?visuals/.*\.(webp|png|gif|jpe?g)$' \
     --path deploy_bundle/
   ```
4. Check that `git rev-parse main^{tree}` is **unchanged**. Then force-push.
5. Locally, run `git fetch`, `git reset --hard origin/main`, `git reflog expire --expire=now --all`, `git gc --prune=now`.

Expect about 147 MiB. All SHAs change, and any other clone must re-clone.

**Dependencies.**
- 4a after Step 0.
- 4b's `AUDIO_DIR` fix and 4e's backup guards must come before 4f or before moving `backups/`.
- 4f must come after WS1 and WS3 are deployed and verified.
- 4g comes last of all.

**Effort.** M overall; 4f is the largest piece (M).

**Risks.**
- The Cloudflare build settings can't be seen from the repo.
- A wrong `.assetsignore` could publish repo files. Under (c) only `web/` is served, which limits that.

**Verify.**
- [ ] **(Git Bash)** `git ls-files | wc -l` is about 11,700, or about 5,900 after 4f.
- [ ] The Cloudflare build log shows about 5,8xx assets. `/`, `/audio/manifest.json`, `/bibles/WEB/Genesis_1.json` and `/visuals/Genesis/1/Genesis_1_1.svg` all load.
- [ ] `python -m http.server 8000 -d web` previews identically.
- [ ] A fresh `git clone` into a temp folder can launch the app and run a Publish dry run.
- [ ] `test_imports.py` and `test_registry.py` pass. Matthew 1 `--dry` works in a clean worktree.
- [ ] Regenerating 1 Chronicles 1 leaves `git status` clean against the 0.8b baseline.

### WS5 — PC app → Studio shell cleanup

> **Status (2026-10-17): done, pushed as `f55eb258`; Cloudflare's Workers Build succeeded.** Every checklist item landed, plus `app.ico` deleted.
> - **Review:** 2 reviewers, then a fix round (15 fixes) and a re-check.
> - **Checks:** the real window, checked at 900 px as `run.bat` starts it, fits both bars. 33 tests pass.
> - **Beyond the plan:**
>   - a user passage move stops playback, and verses are clamped to real ones;
>   - Prev/Next while stopped step verses, and ◀ ▶ step chapters;
>   - worker-thread errors are logged;
>   - Audio/Video renders finish their current verse on close;
>   - Publish refuses to close mid-push;
>   - Audio/Video keep a hand-built range when it already contains the passage;
>   - SVG Studio follows quietly, without narrating;
>   - Coverage Rescan (broken before) works.
> - **Known, accepted:**
>   - Pronunciation saves and the audio manifest lock only within one process. Two processes saving within milliseconds could still lose one edit.
>   - The meter can read one file low right after closing Audio mid-render.

**Goal.** The main window stops being a reader with bolted-on buttons. Every studio-wide hazard found in the audit is fixed. This is Studio phase 1 (§5).

**Final PC control set (D1/D2)**
- Passage bar: Book, Chapter, Verse, plus ◀ ▶ chapter buttons.
- Grouped tools:
  - **Plan:** Coverage (a button until S4 makes it the home pane)
  - **Author:** Visuals (SVG Studio), Pronunciation, Verifier
  - **Produce:** Audio, Video
  - **Ship:** Publish, with the deploy budget meter next to it
- Preview controls: Play, Stop, Prev, Next, until Preview becomes the embedded web app.
- **Kept inside SVG Studio:** "Preview in own window" (svg_studio.py:266-271). It is not a display preference but the recovery switch for `svg_preview_host`: once pywebview fails, the studio persists browser mode and skips re-probing (L711, L720), and re-ticking this is the only way back. It folds into `web_view.py` in S2.
- **Removed:** Version, Translator notes and the welcome hint (all in WS1), Reference, Voice, Speed, the Auto-continue checkbox (the player always continues, as the web does), and the Display window (D2).

**Checklist**
- [ ] **Reference toggle and overlay:** app.py:362-367, L457, L735; visual_stage.py:429-444; svg_stage.py:75, L85, L107-109; config.py:24.
- [ ] **House voice:**
  - Add `tts_engine.HOUSE_VOICE = "en-US-AndrewNeural"` and `HOUSE_RATE = 0`.
  - Remove the main-window Voice combo (app.py:326-331) and Speed slider (L333-337).
  - Point the other uses at the constant: config.py:19, generate_showcase_audio.py:41, pronunciation_tool.py:152-153, pronunciation_check.py:114-116, video_render.py:413/1264, video_studio.py:126-127, isbe_sweep.py:33.
  - Keep at most one "advanced" voice picker, in the Audio Renderer.
  - config.py:20 says the rate range is −50..50, but the slider is −40..40.
- [ ] **Auto-continue:** remove the checkbox (app.py:351-353) and the `self.auto_var.get()` guard (L842), keeping the roll-over at L843-848: the PC then always plays into the next chapter and stops after Revelation, matching the web's `advanceToNextChapter` (app.js:211-223), which D1's faithful-preview argument relies on.
- [ ] **Raster and text stage pipeline** (0 raster visuals remain; the last were deleted 2026-08-12):
  - visual_stage.py: `_rtf_to_text` L41-62; Pillow guard L34-38; `_Animation` L100-164; `_is_animated`/`_get_animation`/`_load_image`/`_load_text` L221-304; the raster/text branches of `render()` L342-400; the `default` fallback L192 (D6); the salted-`hash()` book gradient L308-313.
  - Also the Renderer extension point (L80-97, L576-578), `show_idle` (L584-588) and `VerseContext.text` (L70-71).
  - In `audio_player.py`: `pause`, `resume`, `position_ms`, `length_ms` (L52-60, L82-98).
  - In app.py: the narration-only replay branches (L685-686, L696-697).
- [ ] **`requirements.txt`:** pywebview is effectively **required** now; without it the stage shows nothing. Update the comment at L4-8. List the external tools: ffmpeg and Chrome/Edge for Video Studio, the WebView2 runtime, Inkscape (optional), PowerShell.
- [ ] **`run.bat`:** re-run `pip install -r requirements.txt` when the file's hash changes (today it installs only when `.venv` is missing, L5-14). On startup failure, fall back to `python.exe` with a visible console.
- [ ] **Startup robustness:**
  - Import each tool lazily inside its registry factory, so one broken tool can't take down the shell (app.py:18-23 imports everything at load).
  - Wrap `main()` so a failure shows a messagebox and writes a log.
- [ ] **Tool registry:** replace the five copy-pasted `open_*` blocks (app.py:526-608) and their attributes (L267-272) with `TOOLS = {key: (label, group, factory, kind)}`. The same registry drives the buttons and a Tools menu.
- [ ] **Shared passage:**
  - Re-clicking a tool moves it to the current passage instead of just raising it (L529-533, L544-548, L559-564).
  - Pass the verse to SVG Studio, which already accepts `start_verse` (svg_studio.py:119-120).
  - Add a `<<PassageChanged>>` event that tools follow. SVG Studio asks before discarding unsaved edits.
- [ ] **Close checks:** `_on_close` (app.py:852-855) destroys every Toplevel without running its own checks. Ask each open tool's `can_close()` first. The checks being skipped:
  - SVG Studio's unsaved-XML confirmation (L897-904);
  - render-in-progress in Audio (L345-353) and Video (L388-397);
  - Publish has no close handler at all; add one.
- [ ] **pronunciations.json clobbering:**
  - Pronunciation Studio and the Verifier are untracked subprocesses (app.py:505, L521). Each copies the whole file at start and writes it all back on save, so whichever saves last wins.
  - Make both single-instance (keep the Popen handle).
  - In `pronunciation.save_names` (L223-230), merge per name against a fresh load and warn on an mtime change; `_mtime` already exists (L128-151).
  - Give both tools the same `tk scaling 1.25`.
- [ ] **config.json last-writer-wins:** `app.py` (L256) and `svg_studio.py` (L129) each hold their own dict. Add `config.update(**changes)`, which re-reads, merges and writes. Slim `DEFAULTS` to `last_book`, `last_chapter`, `last_verse`, `svg_preview_host`, `editor`, and pop all obsolete keys.
- [ ] **Audio manifest writes:** `generate_showcase_audio._save_manifest` (L101-103) opens with `'w'` and writes no temp file, while Audio Renderer and Video Studio can both write it. Re-read and merge under a lock, then write to a temp file and `os.replace`.
- [ ] **MCI alias collision:** `audio_player.AudioPlayer` aliases restart at `avbible1` per instance (L42). Use a module-level counter before Pronunciation Studio ever runs in-process.
- [ ] **SVG Studio:** remove "Stage for deploy" (L260-261, L824-856); it duplicates Publish step 3.
- [ ] **Rebrand:**
  - `APP_TITLE` and title text: app.py:1, L33, L283, L427; visual_stage.py:549, L603; svg_stage.py:62, L395; run.bat:2.
  - Icon: `root.iconphoto(True, PhotoImage(file="web/icons/icon-192.png"))`. The tracked Theoria PNG is easier than building an `.ico`.
  - `git rm app.ico`: the old cross-and-book art, tracked but referenced by no `.py`, `.bat`, `.toml` or `.json` in the repo.
  - Optionally rename `run.bat` to `theoria-studio.bat`, keeping a shim.
- [ ] **Display window (D2):** FullscreenStage (visual_stage.py:598-619) and app.py:489-492.

**Dependencies.**
- WS1 first; both edit `app.py`, `visual_stage.py` and `svg_stage.py`.
- The MCI fix comes before any in-process Pronunciation Studio.
- The close checks need the registry.

**Effort.** M (about 2 sessions).

**Risks.** It is tkinter UI work, so check it by screenshot at 900 px and 1,180 px. The shared-passage behaviour has to respect each tool's busy and dirty state.

**Verify.**
- [ ] At the 900 px minimum width, every tool button is visible. Today the bar requests 1,463 px: at 1,180 px Display and Audio are hidden, and at 900 px five buttons are hidden.
- [ ] `python.exe app.py` starts with no traceback. Temporarily break one tool module: the shell still starts and names the tool that failed.
- [ ] In Coverage, jump to Genesis 10, then click Visuals: SVG Studio is on Genesis 10, at the selected verse.
- [ ] Close the main window with an unsaved SVG edit: you get a prompt.
- [ ] Edit different names in Pronunciation Studio and the Verifier and save both: both edits are in `pronunciations.json`.
- [ ] Force the SVG preview's browser fallback, close the main window, reopen: `svg_preview_host` is still `browser`.

### WS6 — Docs cleanup

> **Status (2026-10-17): done, committed locally as `3601be4e`…`824d2f66`, with this plan archived after them.**
> - **Moves:** 15 docs moved into `docs/`, one `git mv` per commit with its pointers. `STUDIO_COMMANDS.md` and `visuals/README.txt` were deleted. The Matthew 1 alternates were split into `docs/archive/`. The three `visuals/*.txt` files left the deploy bundle (5,805 → 5,802 files). `mockups/luke3` and `mockups/matthew1` went to `C:\Dev\Theoria-archive\mockups\`.
> - **New:** a rewritten README, ROADMAP.md, CLAUDE.md, CREDITS.md, `docs/architecture.md`, `docs/studio.md`, `docs/visuals.md`, `docs/pronunciation.md` and `docs/archive/README.md`.
> - **Checks:**
>   - Coverage went from 520 to 719 candidate chapters, from 447 to 646 gaps and from 213 to 254 High gaps, with none lost. Haggai 1–2, 2 and 3 John, John 2–11 and John 6–15 are present as High.
>   - The one High demotion is the built Acts 18. The Third Journey is now `Acts 19–21`, so Coverage counts it as still to build.
>   - The old-doc `git grep` shows only pointers into `docs/archive`.
>   - Every relative link resolves, and `deploy_bundle/visuals` holds 0 `.txt` files.
>   - The 33 tests pass. The `.py` edits are comments and docstrings only (`ast.dump` is identical).
> - **Also:** the memory notes are refreshed.
> - **Open:** the live workers.dev URL isn't recorded anywhere. README.md carries a `<!-- live URL: fill in -->` marker.

**Goal.** Every doc is current or archived. The forward plan lives in one place, and generated reports stop pretending to be docs.

**Disposition of every doc**

| File | Tracked? | Disposition | Reason |
|---|---|---|---|
| `README.md` | yes (1 commit, 2026-07-04) | **Rewrite**, last | Describes an ESV desktop app on bible-api.com with PNG/WebP visuals. It has 18 factual errors (wrong title, 6 versions, translator notes, `default.png`, `generate_matthew1.py`), no web app, and no deploy section. |
| `ROADMAP.md` | new | **Create** | §6 of this plan |
| `CLAUDE.md` | new | **Create** | Session rules: ARM64 with emulated x64 Python; deploy only via GitHub; static vanilla JS with no build step; tools are `tk.Toplevel`; never hand-edit generated SVGs; WEB-only; no stills; no captions; mind the file budget. Salvaged from STUDIO_COMMANDS.md:208-215 and your memory notes. |
| `CREDITS.md` | new | **Create** | WEB (public domain), the edge-tts voice `en-US-AndrewNeural`, pronunciation sources (ISBE 1915: 975, CMUdict: 232, Wiktionary: 62, Wikipedia: 13; check the share-alike terms), and a pointer to the archived photo credits |
| `WEB_PLAN.md` | yes | **Archive** → `docs/archive/` | Every phase shipped. Pages and direct upload, OneDrive, 9 translations and WebP are obsolete. Domain, analytics and Wake Lock move to ROADMAP. |
| `STUDIO_PLAN.md` | yes | **Archive**; its core idea (L10-25) opens `docs/studio.md` | Built 2026-07-09. Feature C (multi-translation audio) is being reversed. It doesn't cover publish, coverage, stills or video. |
| `STUDIO_COMMANDS.md` | yes | **Delete** after copying L208-215 into CLAUDE.md | A finished prompt log ("ALL STEPS DONE"); git history keeps it at `7089ee22` |
| `SVG_STUDIO_DESIGN.md` | yes | **Update** → `docs/svg-studio.md` | Still cited by 6 `.py` files and `svg_generators.json:2`. Stale on four points: "no code exists yet" (L7); "desktop can't render SVG" (L54, L437-438, L466, §6); the §5 translation chips (L412-438); open questions 1–5, which are resolved or moot. |
| `VIDEO_STUDIO.md` | **no** | **Keep** → `docs/video-studio.md` | Accurate. Commit it in Step 0. Remove its translation mention (L132). |
| `TIMELINE.md` | **no** | **Keep** → `docs/design/ot-timeline.md` | Build record for the OT timeline (built 2026-09-13) |
| `INFOGRAPHIC_CANDIDATES.md` | yes | **Update** → `docs/content-catalog.md` | **Machine-read** by `coverage_studio.py:40` (`_parse_candidates` L57-110); keep the `### Book` and `- **Book N** — 🆕 Prio` format. Fix L78 (`visuals/Exodus/25-27/` doesn't exist), L352 (Matthew 1 "three columns"), L401 (Romans "rail"). Merge in the short books. **Give every chapterless entry an explicit chapter span**: `_parse_candidates` skips any label without a chapter number, so Coverage and the S5 Next-up queue can't see them. That includes three of the 64 unbuilt **High** entries (`Judges (the judges' cycle roster)` L133 → Judges 3–16; `John — seven signs` L381 → John 2–11; `John — seven "I am" statements` L382 → John 6–15), two Med (`Esther (overall)` L214, `Psalms (overall)` L227) and three Low (`Obadiah` L308, `Haggai (temple rebuilding)` L334, `Jude …` L501). For whole-book entries such as Psalms, either give the span or add a book-level rule to the parser. |
| `INFOGRAPHIC_CANDIDATES.xlsx` | yes | **Delete** | Stale export (8 Built vs 30 in the `.md`); nothing reads it |
| `HEBREWS_IDEAS.md` | **no** | **Keep** → `docs/design/hebrews.md` | Built record. Its soft spots (L52-58) and audit method (L713-729) feed the ROADMAP. Update svg_generators.json:202 and L223. |
| `ROMANS_IDEAS.md` | **no** | **Keep** → `docs/design/romans.md` | Built record. Its house rules (L134-149) go into `docs/visuals.md`; the audit method (L151-159) goes into the Studio lint. |
| `MATTHEW1_IDEAS.md` | **no** | **Split**: record (L3-87, L154) → `docs/design/matthew-1.md`; alternates (L178-271) → archive | The chapter has shipped. Keep the 41-vs-42 note (L273-281). |
| `LUKE3_IDEAS.md` | **no** | **Archive** with `mockups/luke3/` | Idea #1 shipped; #2-#5 are superseded. Carry the time-depth counter idea (#6) into ROADMAP as Later. |
| `SHORT_BOOKS_IDEAS.md` | **no** | **Split**: Zephaniah (L339-399) and 2 Peter (L615-680) → `docs/design/short-books.md` with the long-form unbuilt concepts; the 22 unbuilt chapters → catalog entries | It holds the best-developed unbuilt designs. Apply its own WEB-wording warning (L15-24). Drop the "AV canon" phrasing (L26, L60). |
| `PRONUNCIATIONS.md` | yes (287 KB, 48% of all doc bytes) | **Untrack and ignore** (`git rm --cached` + ignore line, WS4c); regenerate with `python pronunciation.py`. | Generated ("Do not hand-edit"), 15 commits of churn; the Studio already shows this data |
| `PRONUNCIATION_TODO.md` | yes | **Untrack and ignore** (WS4c, same as above); regenerate with `regen_pronunciation_todo.py` (OUT at L13-14) | Generated and stale: says 3,327 names / 635 wrong; the data now has 3,331 / 616. It depends on an ignored cache. |
| `visuals/README.txt` | yes, and **deployed** | **Replace** with `docs/visuals.md`; delete from `visuals/` | Documents PNG/WebP/GIF, `.KJV` and `.mobile`, retired photo sets, and "translator notes … toggleable" (L14, L23-57). Indexed as a manifest "note" entry. Linked from README.md:75. |
| `visuals/CREDITS.txt` | yes, and **deployed** | **Archive** → `docs/archive/genesis1-photo-credits.txt` | Credits photos retired 2026-07-29. Update `generate_genesis1_svg.py:18`. |
| `visuals/default.txt` | yes, and **deployed** | **Delete** (D6) | Stale text shown on about 93% of verses |
| `visuals/reference/README.txt` | yes, and deployed | **Update** → `docs/reference-charts.md` | Leaves out the 1–2 Chronicles tree (say it is a frozen artifact with no generator, D14) and the OT timeline; its V6 rebuild pointer (L61) becomes `tools/layout_lab.py` (0.3b); V6 moves to archive (D14) |
| `package.json` | yes | **Update** | Description says "reads the Bible aloud (ESV)". Add `"private": true`; drop the dummy `main` and `test`. Keep the wrangler 4.107.0 pin if the cloud build installs from the lockfile. |
| `requirements.txt` comments | yes | **Update** (WS5) | Promises a raster fallback that doesn't exist |
| `pronunciations.json` `_readme` | yes | **Update** via `pronunciation.py` L61-76 | Advises adding KJV spellings |
| `branding/` | no | **Commit** (Step 0) | Logo sources |
| `mockups/` | no | Delete `figures/`; `luke3/` and `matthew1/` go with their docs | Throwaway QC output |
| `.claude/settings.local.json` | yes | **Untrack** | Personal, stale OneDrive paths |
| Your Claude memory notes (outside the repo) | — | **Refresh** after cleanup | `av-bible-project.md` (ESV), `studio-plan.md`, `web-phase-plan.md`, `theoria-branding.md` (logos now in `branding/`), `versification-differs-by-translation.md` (the max-verse rule is retired), `pronunciation-verifier.md` (417 / 616 counts), `svg-visuals-pipeline.md` (no stills), `hosting-scale-limits.md` (deploy ~16.8k → ~5.8k files), `deploy-arm64-github.md` (D7 c changes what wrangler serves), `chronicles-verses-on-master-tree.md` (`AUDIO_DIR` moves off `deploy_bundle`), `video-studio.md` (publish-narration option retired), `figure-swap-procedure.md` (L36-37: the `build_stills` → manifest step), `tree-layout-is-near-optimal.md` (L15: `_scratch/layout_lab.py` → `tools/`), `tts-pronunciation.md` (L21 "add translation-specific spellings (KJV…)"; L105 the `deploy_bundle`/`prepare-deploy.ps1` publish steps), `ot-timeline-chart.md` (L14: TIMELINE.md → `docs/design/ot-timeline.md`), `matthew1-on-the-ot-tree.md` (L13: `backups/matthew1_fractal_tree/` → `C:\Dev\Theoria-archive`; L25-29 the KJV-variant caveat), and the `MEMORY.md` index lines for each |

**Pointer updates (every move must update these)**
- **Functional paths:**
  - `coverage_studio.py:40` (`CANDIDATES_MD`). (The pronunciation reports stay at the root, untracked, so `pronunciation.py:59` and `regen_pronunciation_todo.py:13-14` don't change.)
- **Data and docs:**
  - `svg_generators.json:2`, L202, L223;
  - `pronunciations.json` `_readme`; README.md:75;
  - INFOGRAPHIC_CANDIDATES.md:464, L483; HEBREWS_IDEAS.md:291; SHORT_BOOKS_IDEAS.md:29, L40.
- **Docstrings (20 `.py` files):**
  - svg_studio, svg_preview, svg_registry, svg_freeze, svg_stage, test_svg_freeze (SVG_STUDIO_DESIGN);
  - publish_studio.py:19, audio_studio.py:12 (STUDIO_PLAN);
  - generate_hebrews_svg.py:2, generate_romans_svg.py:4, generate_luke3.py:23, generate_2peter_svg.py:3, generate_zephaniah_svg.py:3;
  - chronology.py:1, L37, generate_ot_timeline_svg.py:1;
  - generate_genesis1_svg.py:18.

**Order.**
1. `git mv` the existing docs into the new tree, one move per commit, and fix the pointers. Commit immediately; never leave moves staged.
2. Re-test Coverage's Candidate column.
3. Update the catalog and SVG Studio design doc.
4. Write README, ROADMAP, CLAUDE.md and CREDITS against the cleaned code.
5. Refresh the memory notes.

**Effort.** M.

**Risk.** Moving or reformatting the catalog can silently empty Coverage's Candidate column.

**Verify.**
- [ ] `git grep -n -E "WEB_PLAN|STUDIO_PLAN|STUDIO_COMMANDS|SVG_STUDIO_DESIGN|_IDEAS\.md|INFOGRAPHIC_CANDIDATES\.md"` shows only intended pointers.
- [ ] Coverage's "Candidate gaps" count is at least today's, with Haggai 1–2 and 2 John 1 now visible, and Coverage marks a High candidate in every chapter claimed by the 64 unbuilt High entries (including Judges, and John 2–11 and 6–15).
- [ ] README links resolve on GitHub.
- [ ] **(Git Bash)** `git ls-files deploy_bundle/visuals | grep -c '\.txt$'` returns 0.

---

## 5. The Studio: vision and phased plan

### 5.1 Target shape

```
+------------------------------------------------------------------------------------------+
| THEORIA STUDIO   Passage: [Book v][Ch v][V v]  ◀ ▶         Files 5,8xx / 20,000  [Publish] |
+---------------------------------+--------------------------------------------------------+
| COVERAGE (home)                 | PREVIEW                                                |
| filter: [Next up v]             |  the real web app at /?b=..&c=..&v=.. (site layout)    |
| Genesis                         |  (shipped MP3s, real stage CSS, ✦ pointer)            |
|  1  31v  V 31/31  A 31/31  N 0  |  [Rebuild manifest]  [Open in browser]                 |
|  2  25v  V 25/25  A 25/25  N 2  |                                                        |
+---------------------------------+--------------------------------------------------------+
| Author: [Visuals] [Pronunciation] [Verifier]   Produce: [Audio] [Video]    status ...      |
+------------------------------------------------------------------------------------------+
```

Principles:
- The website is the product. The Studio authors, checks and ships content for it.
- Deploying stays one button: **Publish** (D7). Every layout change keeps it that way, and the S3 lint and dry-run box make it safer, not longer.
- One house configuration: WEB text, `en-US-AndrewNeural` at rate 0, SVG-only visuals. No per-user display toggles in the Studio.
- Generators are the source of truth for every visual. The Studio sets up, runs, previews, checks and publishes; it doesn't draw. Drawing happens in Claude sessions.
- Local tkinter plus the WebView2 embedding already proven by `svg_stage.py`. No web framework, and no new native dependencies on this ARM64 machine.

### 5.2 The end-to-end chapter workflow it optimises

1. Pick a chapter from **Next up** (high-priority catalog candidates with no visuals). The pane shows its catalog entry, any `docs/design` notes and the WEB verse count.
2. **Names.** Clear unreviewed names in Pronunciation Studio before rendering audio, because audio depends on them.
3. **Audio.** Render the chapter. Stale-narration flags appear whenever a respelling changes later.
4. **Visuals.** "New visual family…" writes a generator from a template and a registry entry, and copies a ready-to-paste Claude prompt (the catalog entry, design notes, WEB text and house rules). The drawing is written in a Claude Code session. Then regenerate into a scratch folder, preview each verse with narration, and **Accept**.
5. **Preview.** Watch the chapter end to end exactly as the website will show it.
6. **Publish.** Lint runs first: visual keys equal WEB verses, audio is complete and fresh, a registry owner exists, sources are committed, the budget is under the cap. Then a content commit, an optional separate sources commit, and push.
7. **Video** (optional): a 4K MP4 with captions, description and thumbnail.

### 5.3 What to retire

- Reader identity: the Version, Notes, Reference, Voice, Speed and Auto-continue controls, the Display window (D2), and eventually `PlaybackSession`, `visual_stage.py` and `svg_stage.py` (D1, phase 4).
- All translation pickers and variants; build_stills and the stills; the ESV code.
- SVG Studio's hand-authoring set (D12) and "Stage for deploy".
- The CLI `main()` and `SHOWCASE_CHAPTERS` in `generate_showcase_audio.py`. It becomes a `narration.py` library.
- The Video Studio "Also publish new narration" option (video_studio.py:173-176); the Audio tab and lint cover it.
- The one-off ISBE scripts (all but `isbe_sweep.py`), `name_ipa.py`, and the v2 1 Chronicles renderer.

### 5.4 What not to build

- A vector editor or in-app drawing; an in-app code editor ("open in editor" is enough).
- Anything multi-translation, including "just in case" hooks.
- A browser or Electron rewrite of the Studio.
- Loading the Verifier's torch model (~1.2 GB) into the main process.
- A task tracker or database; the catalog plus measured state is the backlog.
- CI-driven content builds or automatic publishing.
- A video engine rework (`video_render.py` works; it only gets re-hosted).

### 5.5 Phases

| Phase | Contents | Effort |
|---|---|---|
| **S1 Harden** (= WS5) | Strip toggles; house voice; tool registry; lazy imports; close checks; single-instance tools plus merge-on-save; config merge; atomic audio-manifest writes; shared passage, first cut; MCI alias fix; rebrand | M |
| **S2 Consolidate** | `studio_core.py` (verse keys and paths, WEB verse lists, deploy budget, house W/H/palette without `generate_tabernacle`'s PIL import side effects). `narration.py` (the audio naming and manifest helpers from `generate_showcase_audio`, made public). `ui_common.py` (ChapterPicker, EventPump, LogPane; today there are 5 pickers and 6 queue pumps). **One visual resolver** replacing the 3 Python copies (visual_stage `_find_image`, video_render `resolve_svg`, svg_preview `resolve_audio`). One `web_view.py` merging `svg_preview.py` and `svg_stage.py` (identical `_orphan_watchdog` and `run_embedded`). Each `App` takes a parent frame. Retire the hand-authoring features (D12). | M |
| **S3 Lint + Publish** | `lint.py` (pure checks with a CLI). Blockers and warnings, with today's results: file budget (16,824 now); orphan verse keys (4 now, 0 after WS1); WEB verses missing a visual in started chapters (0); **partial-audio chapters** (Psalms 119 at 4/176; this needs its own rule because it has no visuals); **stale narration** from the TTS cache (see below); **audio-timed visuals** (1 Chronicles + Matthew 1, 432 verses) flagged when their MP3 changes; every visuals folder has a registry owner; generator and spec files tracked and clean; SVGs parse; manifest newer than the newest SVG; no suffixed or still files; an SVG audit (overlap, overflow, off-canvas) promoted from `tools/audit_heb.py` (rescued in 0.3b). Publish shows the report, refuses on blockers, has a dry-run box, and offers "commit sources" as a separate commit. | M |
| **S4 Hub window** | Coverage becomes the home pane (needs the chrome/content split, coverage_studio.py:286-288). Preview = a daemon `http.server` on 127.0.0.1 plus the embedded WebView2, showing `/?b=&c=&v=`, with the `--autoplay-policy` flag `svg_preview` already sets and "Rebuild manifest" beside it. **It must serve the production layout at `/`,** because the web app fetches root-absolute paths (`/visuals/manifest.json` visuals.js:99, `/visuals/${file}` L167, `/bibles/${code}/…` bible.js:17). A repo-root server only works while `visuals/` and `bibles/` sit at the root, and D7(c) moves them into `web/`. So: before D7(c), a small `translate_path` override maps `/visuals/*` → `visuals/`, `/bibles/*` → `bibles/` and everything else → `web/` (serving `deploy_bundle` would also work but lags until `prepare-deploy.ps1` runs); after D7(c), serve `web/` as is. Depends on the web deep-link change and on the D7 decision. Grouped tool bar and the budget meter in the header. Pronunciation Studio runs in-process (after the MCI fix); the Verifier stays a separate process. Only after the Preview passes the acceptance checklist below, delete `PlaybackSession` and the transport code (app.py:40-193, L610-848), `visual_stage.py` and `svg_stage.py`. | L |
| **S5 Workflow features** | **Generator CLI contract** `--only CH[:V]`, `--out DIR`, `--dry`, with a `cli` capability field in the registry. After the Step 0 registry fix, 1 of the 24 registered generators accepts `--only`: `generate_1chronicles_tree_svg.py` (docstring L9-11, parsing L44-50), which also has `--out` and `--dry` and is the reference implementation. `generate_matthew1_svg.py` (L76-79) has `--out` and `--dry`. **Regenerate to scratch → compare → Accept.** **New visual family…** (template plus registry entry plus Claude prompt; the template iterates `verse_numbers()`, not a hard-coded `CH_LEN`). **Next-up queue** linked to the design records. **Chapter contact sheet** (settled end frames of one chapter, driven by the registry and manifest; a new script, since the `_scratch/build_*` prototype only compared Exodus 25–27 mockups, see 0.3b). | M each |
| **S6 Optional** | Tabs instead of windows (D3 a); `svg_palette.py` extracted, with `generate_tabernacle` re-exporting it (also sets up colour themes); a figure-vocabulary browser for `svg_figures` (51 figures) and `svg_vocab`; a Video render queue and thumbnail composer | S–M |

**S4 Preview acceptance (the parity check before the old player is deleted).** Run each on this ARM64 PC in the embedded Preview (Appendix C item 5):
- [ ] `/?b=Genesis&c=1&v=3`, `/?b=1%20Chronicles&c=1&v=1` and `/?b=Romans&c=16&v=24` each land on that verse, and the passage bar follows.
- [ ] Neural MP3s play with no click, thanks to the `--autoplay-policy=no-user-gesture-required` flag (svg_preview.py:267); the Network panel shows `Genesis_1_1.mp3`.
- [ ] A chapter with no MP3s (e.g. Genesis 12) falls back to Web Speech and is audible.
- [ ] An un-illustrated chapter (e.g. Genesis 12) shows the "isn't illustrated yet" pointer, and its ✦ button opens the list inside the Preview.
- [ ] Playing the last verse of Genesis 1 rolls into Genesis 2:1 and keeps playing.
- [ ] Regenerate one verse, press "Rebuild manifest": the Preview shows the new SVG without restarting the Studio.
- [ ] Closing the Studio leaves no `http.server` thread or WebView2 process behind.

**Stale narration can be measured today, with no new state file.** `tts_engine._cache_file` (tts_engine.py:45-50) names every synthesis `cache/audio/tts/<voice with dashes removed>_<rate:+d>_<md5(f"{voice}|{rate}|{respelled text}")[:16]>.mp3`, e.g. `enUSAndrewNeural_+0_<digest>.mp3`. Lint must call `tts_engine._cache_file(voice, rate, pronunciation.respell(text), "mp3")` (or a public wrapper), passing the same text the Audio Renderer passes to `synthesize()`, rather than re-deriving the name. Comparing each published MP3 against the cache entry for the *current* respelling gives:
- 2,237 of 2,352 match;
- 91 have no entry;
- 24 differ.

That makes **115 likely-stale verses**: Numbers 3 (22), Exodus 34 (15), Luke 3 (14), Numbers 1 (13), Numbers 32 (13), Numbers 2 (12), Numbers 4 (10), Matthew 1 (6), and a few others. Lint should use this comparison, and a fingerprint file can act as a backstop in case the cache is ever cleared.

---

## 6. New plans for the future (ROADMAP)

This replaces the scattered idea docs. **Now** means alongside or immediately after the cleanup; **Next** means the next 1–3 months; **Later** has no date.

### 6.1 Content

The full backlog is the catalog (`INFOGRAPHIC_CANDIDATES.md`, becoming `docs/content-catalog.md`): 64 unbuilt High entries today. The first three rows set policy for audio (what gets narrated, and fixing what is already narrated); the rest is a reuse-first selection from the catalog, cheapest first, building on geometry and libraries that already exist, plus a decision on video. Each fully produced verse costs about 2 deploy files.

| When | Item | Rationale | Source |
|---|---|---|---|
| Now | **Narration policy** (decide once): neural MP3s for whole chapters only, and only for illustrated chapters. Today all 73 illustrated chapters are narrated; the 4 narrated-only chapters are Acts 2, Acts 12 and Exodus 34 (illustrated by rows below) and Psalms 119 (removed by D15). Everything else stays on Web Speech until a §6.4 file-cap lever is pulled. Render a chapter's audio when its visuals start, so the S3 partial-audio rule stays green. | Every narrated verse costs a deploy file (×2 while the bundle is tracked); without a rule narration spreads with no budget | audio vs visuals manifests; §6.4 |
| Now → Next | **Pronunciation backlog.** 616 names are `unfixed` (pronunciations.json statuses). About 190 of them occur in the 77 narrated chapters (whole-word scan of the WEB text), so shipped audio says them wrong. Order: names in narrated chapters first, then the names of each next content chapter before its audio is rendered (§5.2 step 2). `isbe_sweep.py` proposes respellings; the Verifier confirms by ear. | Every fix makes narration stale, so batch fixes before re-renders | pronunciations.json; memory pronunciation-verifier |
| Now | Re-render the ~115 likely-stale narrations, plus whatever the pronunciation pass on narrated chapters just made stale, so each chapter is re-rendered once. Then re-run the 1 Chronicles and Matthew 1 generators if their MP3s changed (their cameras are timed to audio) | Correctness of what has already shipped | Stale-audio measurement (§5.5); svg_chronicles_world.py:593-596 |
| Next | **Numbers 33** (map plus timeline, High) | Reuses the `generate_tribal_maps.py` geometry from Numbers 32/34 | catalog |
| Next | **Joshua 13–19** (allotment map, High) | `TRIBES`/`PRINCES` already exist (generate_tribal_maps.py:146, 506) | catalog |
| Next | **Acts 19–21 and 27–28** (maps, High) | Reuses the `MED`/`PELOPONNESE`/`ISLANDS` coastline (generate_acts1518_svg.py:90/151/168); completes Paul's journeys. Acts 18 is already built. | catalog |
| Next | **Haggai 1–2**, then the **2 John + 3 John diptych** | Ranked best next builds in SHORT_BOOKS_IDEAS.md:681-695 (the catalog's "Low/none" ratings get reconciled in WS6). Check WEB wording first. | SHORT_BOOKS_IDEAS.md |
| Next after these | Neighbours that reuse the same geometry: **Numbers 10–14**, **Numbers 35** and **Joshua 1–5, 6, 9–12** (`generate_tribal_maps`); **Exodus 12–14** (pairs with the Numbers 33 itinerary); **Acts 1–2** (the Acts `MED` coastline) | Same libraries as the rows above | catalog L75, L101, L108, L120-123, L389 |
| Next | **Acts 12 and Exodus 34**, which already have full neural narration but no visuals (Acts 2 is in the row above) | The audio is paid for; a visual completes the chapter. Exodus 34 is also on the stale-narration list, so re-render it first. | audio vs visuals manifests (77 narrated chapters, 73 illustrated) |
| Next (decide) | **Video output.** Video Studio is built and three renders sit in `renders/` (Genesis 1, 1 Chronicles 1–2, Matthew 1, each with `.srt`, description and thumbnail; upload steps at VIDEO_STUDIO.md:137-147). Either publish to YouTube (re-render the three after their stale narration is fixed, since Matthew 1 has 6 stale verses; then one video per completed chapter as it ships, at a cadence you choose), or mark video "not planned" and leave Video Studio as it is. | Built tooling with no publishing plan; custom thumbnails need a verified channel | VIDEO_STUDIO.md; `renders/` |
| Later | **Matthew 21–27, Holy Week** (timeline, High) | A day-by-day timeline; the catalog calls it one of the most popular subjects | catalog L359 |
| Later | **Genesis 12–25, 25–36, 37–50** (maps, High) | Completes Genesis; reuses the Genesis 10 world map and the OT tree | catalog |
| Later | **1 Kings 12 – 2 Kings 17** on the timeline sheet (High) | The OT timeline already has 41 reigns with Ussher and Thiele rails; use a per-verse camera over it, as 1 Chronicles does over the tree | TIMELINE.md:10-44 |
| Later | **Leviticus 16, Leviticus 1–7** (High), **Exodus 29** (Med), **1 Kings 6–7** temple (High) | Reuse `svg_priest.py` and the tabernacle plan | catalog; HEBREWS_IDEAS.md §6 |
| Later | **Matthew 2** (map) and **Luke 1–2** (timeline), both High | Neighbours of built chapters; reuse the `svg_matthew_nativity` stage | catalog |
| Later | Remaining short books: Habakkuk 3, Nahum 2, Obadiah, Joel 1–3, Philemon, Jude, Titus 1–3, 2 Thessalonians 1–3 (about 405 verses across all 11 short books) | Designs already exist | SHORT_BOOKS_IDEAS.md |
| Later | Symbolic and architectural set pieces: Daniel 2/7/8/9, Ezekiel 1/10 and 40–43, Zechariah 1–6, Revelation 4–5 and 21–22 | High priority, but no reuse | catalog |
| Later | Revisits: the Hebrews 5 ledger density and a shared mark for the five warnings; keep the Matthew 1 41-vs-42 count consistent; the Luke 3 time-depth counter | Polish | HEBREWS_IDEAS.md:52-58; MATTHEW1_IDEAS.md:273-281; LUKE3_IDEAS.md #6 |

### 6.2 Web

| When | Item | Source |
|---|---|---|
| Now | WEB-only UI, the "isn't illustrated yet" pointer to ✦, Wake Lock, accessibility fixes (WS1–WS2) | this plan |
| Next | **Deep links** (`?b=&c=&v=`, or a hash form). Shareable, and needed by the Studio Preview. Today `web/js` has no location/URLSearchParams handling. | memory studio-plan; `grep URLSearchParams web/js` finds nothing |
| Next | **`theoria.bible` domain + Cloudflare Web Analytics**; then rename the worker and repo from `av-bible` (renaming changes the workers.dev URL) | WEB_PLAN.md:106-109; memory theoria-branding |
| Later | **Charts entry** next to ✦, once you've chosen which family-tree version belongs in the app (OT tree, V6 heir spine, 1–2 Chronicles tree, OT timeline are all deployed but unlinked) | D14 |
| Later | Selectable colour themes (cheap only while 0 SVGs are hand-edited) | memory svg-color-themes-research |
| Later | Open Graph preview cards per verse (would reuse the freeze logic, restored from history) | memory studio-plan |
| Later | App-shell service worker (cache-first shell; runtime caching only for chapters visited). It is not needed for installing the app, and iOS evicts storage anyway. | `web/` has a `manifest.webmanifest` but no service worker |
| Later | Show the reference in fullscreen alongside the tap-to-reveal controls | app.js:508-539 (fullscreen tap-to-reveal) |

### 6.3 Studio

| When | Item |
|---|---|
| Now | S1 Harden (WS5) |
| Next | S2 Consolidate; S3 Lint + Publish (including the stale-narration and partial-audio checks) |
| Next | S4 Hub window with the embedded web Preview (after web deep links; its server layout follows the D7 decision) |
| Next | Shared visuals in the Studio (D17): SVG Studio labels a verse "shared with vv16-32" when its picture is a range file or an identical copy, editing it says it affects the whole run, and the S3 lint warns when a per-verse file overlaps a range file |
| Later | S5 workflow features (CLI contract, regenerate-to-scratch, New visual family with an option to write range files, Next-up queue, contact sheets); S6 optional items |

### 6.4 Infrastructure

| When | Item |
|---|---|
| Now | Step 0 (backups, catch-up commits, Publish pathspec and `CONTENT_PATHS`, tracked `prepare-deploy.ps1`, registry fixes, import and registry tests, regeneration baseline, timeline deploy decision, `pre-cleanup` tag and bundle, delete the merged branch) |
| Now | WS4a–e, any time after Step 0 (Publish commit message and dry-run box, `.gitignore` and untracking the generated reports, dead modules, `AUDIO_DIR` fix, backup guards, `ipa_checks.json` to `data/`) |
| Next | **D7(c): serve `web/` directly** and stop tracking `deploy_bundle`; Cloudflare build watch paths (`web/**`, `wrangler.toml`) so code-only commits don't redeploy; README "Deploy" section |
| Later | Optional history slim (D8) |
| Later | **R2 / file-cap levers.** After cleanup the deploy is about 5,800 files with about 14,200 of headroom, roughly 7,000 more verses at 1 SVG + 1 MP3. Neural narration of the whole canon (31,098 MP3s) cannot fit under 20,000 on its own. **Trigger:** the Publish budget meter passes 16,000 (80%), or you decide to narrate whole books beyond about 7,000 more verses. Levers, cheapest first: (1) per-book bible JSON (−1,123 files); (2) chapter-level MP3s with a verse timing table (check against the iPad verse-change-pop fix, which relies on per-verse elements); (3) move audio to R2 behind the existing manifest lookup; (4) the Workers Paid static-asset limit, believed to be 100,000 per version but **verify in current docs**. At the August–September build pace this is many months away. |

---

## 7. Proposed doc structure after cleanup

```
README.md              What Theoria is (narrated WEB Bible + per-verse animated SVG), live URL,
                       how it's made (Studio → Publish → git push → Cloudflare Workers static assets),
                       quick start (open the site / run the Studio), repo map, requirements
                       (Python 3.14 venv, pywebview, optional torch for the Verifier, ffmpeg + Chrome for video),
                       Deploy section (push to main deploys; file budget; rollback), links below.
ROADMAP.md             §6 of this plan: Now / Next / Later for content, web, studio, infrastructure.
CLAUDE.md              Session rules (ARM64 + emulated x64 Python, GitHub-only deploys, vanilla JS no build,
                       Toplevel tools, spec is source of truth, WEB-only, no stills, no captions, file budget).
CREDITS.md             WEB, voice, pronunciation sources, pointer to archived photo credits.
branding/              theoria_logo.svg, icon_maskable_source.svg (+ alternates/ if kept)
tools/                 reference scripts rescued from _scratch/ (audit_heb SVG audit, layout_lab)
docs/
  architecture.md      Data flow bibles/WEB → generators → visuals → manifest → web; audio pipeline;
                       Publish → GitHub → Cloudflare; ~20k file budget.
  studio.md            NEW design of record for Theoria Studio: every tool, what it reads/writes,
                       the chapter workflow, generator CLI contract, lint checks.
  svg-studio.md        ← SVG_STUDIO_DESIGN.md (corrected)
  video-studio.md      ← VIDEO_STUDIO.md
  visuals.md           ← visuals/README.txt rewritten: SVG/SMIL only, Book_c_v.svg naming, manifest v2,
                       registry, house rules (from ROMANS_IDEAS.md:134-159 + "less is more").
  pronunciation.md     respell(), Verifier, how the list is maintained.
  content-catalog.md   ← INFOGRAPHIC_CANDIDATES.md (machine-read; coverage_studio.py:40 repointed)
  reference-charts.md  ← visuals/reference/README.txt (+ 1–2 Chronicles tree, OT timeline; all charts
                       deployed, unlinked, still in progress — D14)
  design/
    hebrews.md  romans.md  matthew-1.md  short-books.md  ot-timeline.md
  archive/
    WEB_PLAN.md  STUDIO_PLAN.md  LUKE3_IDEAS.md  matthew-1-alternates.md
    genesis1-photo-credits.txt
    mockups/ (luke3, matthew1 PNGs — or delete)
data/
  ipa_checks.json      Verifier verdict store (moved out of cache/)
```

Removed from the root: WEB_PLAN.md, STUDIO_PLAN.md, STUDIO_COMMANDS.md, SVG_STUDIO_DESIGN.md, VIDEO_STUDIO.md, TIMELINE.md, all five `*_IDEAS.md`, INFOGRAPHIC_CANDIDATES.{md,xlsx}, PRONUNCIATIONS.md and PRONUNCIATION_TODO.md (now generated and ignored). Removed from `visuals/`: README.txt, CREDITS.txt, default.txt.

---

## Appendix A. Module-by-module classification (80 root `.py` files)

Key: **Keep**; **Slim** (edits in the named workstream); **Delete**; **Commit** (currently untracked; commit in Step 0). "Importers" counts repo modules that import it.

### Tracked (61)

| Module | Lines | Role | Importers / launched by | Action |
|---|---|---|---|---|
| app.py | 869 | App entry (run.bat) | — | Slim (WS1 translation/ESV/notes; WS5 toggles, registry, rebrand); reader parts deleted in S4 |
| audio_player.py | 108 | Library (MCI) | app, pronunciation_tool, pronunciation_check | Keep; drop dead methods, fix alias counter (WS5) |
| audio_studio.py | 375 | Studio: Audio Renderer | app; publish_studio, svg_studio (deploy count) | Slim (WS1 picker); move deploy count out (WS4) |
| books.py | 28 | Library | 11 | Keep |
| build_manifest.py | 193 | Build (subprocess) | publish_studio, svg_studio | Slim (WS2 .txt; WS3 still; WS4 path anchor) |
| build_stills.py | 112 | Build: stills | publish_studio, svg_studio | **Delete** (WS3) |
| config.py | 48 | Library | 12 | Slim (WS1, WS5) |
| coverage_studio.py | 445 | Studio: Coverage | app | Keep; single audio count (WS1); home pane (S4) |
| generate_1chronicles.py | 1265 | Library: 1 Chronicles scene data | chronicles_tree, svg_chronicles_world, both 1 Chronicles generators | Keep; use loader (WS1) |
| generate_1chronicles_svg.py | 72 | Superseded v2 generator (registered today!) | registry | Repoint registry (Step 0); **Delete** (WS4) |
| generate_acts1314_svg.py | 941 | Generator | — | Keep; docstring L487 |
| generate_acts1518_svg.py | 1249 | Generator | — | Slim (skip 15:34, WS1) |
| generate_exodus2527_svg.py | 47 | Generator | — | Keep |
| generate_exodus26_svg.py | 70 | Generator + palette | exodus2527 | Keep |
| generate_genealogy.py | 706 | Library: Genesis 5/11 spec | genealogy_svg, luke3 | Slim (variants, broken `__main__`, WS1) |
| generate_genealogy_svg.py | 90 | Generator (translation-suffixed) | — | Slim to WEB (WS1) |
| generate_genesis1_svg.py | 392 | Generator | — | Keep; L18 pointer (WS6) |
| generate_genesis2_svg.py | 423 | Generator + palette | genesis1, genesis3, numbers1_2 | Keep |
| generate_genesis3_svg.py | 538 | Generator | — | Keep |
| generate_genesis4_svg.py | 444 | Generator | — | Keep |
| generate_genesis69_svg.py | 1138 | Generator | — | Keep |
| generate_genesis10_svg.py | 441 | Generator + palette | genesis11 | Keep |
| generate_genesis11_svg.py | 334 | Generator | — | Keep |
| generate_luke3.py | 278 | Library: Luke 3 extraction | luke3_svg | Slim (WS1) |
| generate_luke3_svg.py | 579 | Generator (translation-suffixed) | — | Slim to WEB (WS1) |
| generate_matthew1_svg.py | 139 | Generator (HEAD import broken) | — | Commit working-tree version (Step 0); fix backup guard (WS4); drop still refs (WS3) |
| generate_numbers1_2_svg.py | 477 | Generator | — | Keep |
| generate_numbers3_4_svg.py | 620 | Generator | — | Keep |
| generate_numbers32_svg.py | 219 | Generator | — | Keep |
| generate_numbers34_svg.py | 252 | Generator + library | numbers32 | Keep |
| generate_romans_svg.py | 2554 | Generator | — | Slim (CH_LEN, dead doxology branch, WS1) |
| generate_showcase_audio.py | 185 | Library with a stale CLI | audio_studio, video_render | Slim (WS1); becomes `narration.py` (S2) |
| generate_tabernacle.py | 1637 | Library hub (palette, out_path, font) + Exodus 25–27 spec | 33 | Keep; docstring, `pulse` (WS4); `svg_palette` later (S6) |
| generate_tribal_maps.py | 931 | Library (map data, MapFrame) | 10 | Slim (−419 raster lines, WS4) |
| import_translation.py | 427 | One-off importer | — | Slim to a WEB USFX re-importer (WS1) |
| ipa_asr.py | 431 | Library (Verifier ear; heavy optional deps) | pronunciation_check | Keep |
| isbe_apply.py | 58 | One-off | — | **Delete** (WS4) |
| isbe_benchmark.py | 74 | One-off | — | **Delete** |
| isbe_harvest.py | 170 | One-off | isbe_benchmark | **Delete** |
| isbe_repair.py | 113 | One-off | — | **Delete** |
| isbe_repair_legacy.py | 187 | One-off | — | **Delete** |
| isbe_sweep.py | 252 | Tool: headless measure-and-propose respelling sweep | isbe_repair (deleted) | **Keep** with `isbe_harvest.json`; fix hard-coded path L24-25 and voice L33 (WS4d) |
| isbe_to_ipa.py | 151 | One-off | isbe_apply, isbe_benchmark | **Delete** |
| name_ipa.py | 171 | One-off | — | **Delete** |
| passages.py | 390 | Library | 13 | **Rewrite** (~60–100 lines, WS1) |
| prefetch_translations.py | 123 | Dead | — | **Delete** (WS1) |
| pronunciation.py | 364 | Library | 9 | Slim (`_readme` WS1; merge-on-save WS5) |
| pronunciation_check.py | 514 | Studio: Verifier (subprocess) | app | Keep; single-instance (WS5); optional rename |
| pronunciation_tool.py | 453 | Studio: Pronunciation (subprocess) | app | Slim (WS1); in-process in S4; optional rename |
| publish_studio.py | 309 | Studio: Publish | app | Slim (Step 0 pathspec and content paths; WS3 step 1; WS4 commit message, dry run) |
| regen_pronunciation_todo.py | 174 | Tool | — | Keep; update ISBE prose (WS4) |
| svg_1chronicles_render.py | 498 | Superseded v2 renderer | generate_1chronicles_svg | **Delete** (WS4) |
| svg_freeze.py | 236 | Library | build_manifest, build_stills, svg_studio, test | Slim (drop `freeze_still`, WS3); `freeze_to_base` per D12 |
| svg_preview.py | 296 | Studio helper (pywebview, subprocess) | svg_studio | Slim (WS1); merge into `web_view.py` (S2) |
| svg_registry.py | 94 | Library | svg_studio, build_manifest | Slim (WS1) |
| svg_stage.py | 418 | PC stage (WebView2) | visual_stage | Slim (WS1, WS5); delete or merge in S2/S4 |
| svg_studio.py | 925 | Studio: SVG Studio | app | Slim (WS1 variants, WS3 stills, WS5 Stage-for-deploy, D12) |
| svg_surface.py | 550 | Library | 27 | Keep |
| test_svg_freeze.py | 293 | Tests (20) | — | Slim (WS1 fixture, WS3 StillCases) |
| tts_engine.py | 149 | Library | 9 | Keep; `HOUSE_VOICE` (WS5) |
| visual_stage.py | 619 | PC stage | app | Slim to SVG-only (WS5); delete in S4 |

### Untracked (19); all are **Commit** in Step 0

| Module | Lines | Role | Importers / notes |
|---|---|---|---|
| chronicles_tree.py | 1378 | Library (welded tree) | 7 importers; dead `kids_of`, `P` (WS4) |
| chronology.py | 429 | Library | generate_ot_timeline_svg |
| generate_1chronicles_tree_svg.py | 98 | **Live** 1 Chronicles v3 generator (407 files) | Register (Step 0) |
| generate_2peter_svg.py | 1653 | Generator (61 files) | Register (Step 0) |
| generate_exodus28_svg.py | 816 | Generator (43 files) | Registered in working-tree JSON |
| generate_hebrews_svg.py | 2542 | Generator (303 files) | Registered in working-tree JSON |
| generate_ot_family_tree_svg.py | 835 | Wall chart + library | svg_chronicles_world, svg_matthew_world, svg_matthew_nativity, ot_timeline |
| generate_ot_timeline_svg.py | 649 | Wall chart | — |
| generate_zephaniah_svg.py | 1446 | Generator (53 files) | Register (Step 0) |
| matthew_tree.py | 301 | Library | chronology, ot_timeline, svg_matthew_world |
| ot_grafts.py | 732 | Library | chronicles_tree |
| svg_chronicles_world.py | 1127 | Library | 1 Chronicles tree, svg_matthew_*; `AUDIO_DIR` fix (WS4) |
| svg_figures.py | 3059 | Library | 18, including `generate_tabernacle` at top level |
| svg_matthew_nativity.py | 421 | Library | generate_matthew1_svg |
| svg_matthew_world.py | 421 | Library | generate_matthew1_svg |
| svg_priest.py | 548 | Library | exodus28, hebrews |
| svg_vocab.py | 274 | Library | 2peter, exodus28, hebrews, zephaniah; dead `lying_beast` |
| video_render.py | 1309 | Studio engine + CLI | video_studio |
| video_studio.py | 416 | Studio: Video | app |

Net result: 11 modules deleted (`build_stills`, `prefetch_translations`, `generate_1chronicles_svg`, `svg_1chronicles_render`, six `isbe_*`, `name_ipa`; 12 if `import_translation.py` goes later), about 2,150 lines. About 900 more lines of dead raster, ESV, variant and stills code come out of live modules. About 69 modules remain, all tracked.

---

## Appendix B. Measured counts (as of 2026-10-06; verifier-corrected)

Supporting measurements and how each was taken. The headline before/after figures are in §1.2 only (the after-cleanup projection there was computed with `git ls-tree` and the removal set applied).

| Item | Count | How measured |
|---|---|---|
| deploy_bundle tracked | 16,822 (audio 2,385; bibles 10,007; visuals 4,416; shell 14) | `git ls-files deploy_bundle` |
| deploy_bundle blobs identical to their sources | 16,822 of 16,822 | blob SHA comparison |
| bibles per code | ASV, BBE, BSB, DARBY, KJV, WEB, YLT: 1,189 each; DRA: 1,193; OEB: 491; non-WEB total 8,818 (34.4 MB per copy) | `git ls-tree` |
| WEB verses / chapters | 31,098 / 1,189 | bibles/WEB |
| WEB notes | 1,161 notes on 1,064 verses in 567 chapters (63 of 66 books); median 40 chars | JSON scan |
| Translation-suffixed visuals | 836 per copy (547 animated + 289 stills): Genesis 5 204, Genesis 11 200, Luke 3 432; 176 byte-identical to generic | `git ls-files` + blob hash |
| `.WEB.`-suffixed files | 0 | `git ls-files` |
| `.still.svg` | 1,613 per copy (59.07 MiB) | `git ls-files` |
| Orphan verse visuals | Acts 15:34; Romans 16:25, 26, 27 (5 files including 1 still) per copy | manifest vs WEB verse sets |
| Visuals manifest | v2, 2,795 keys (2,245 verse + 547 suffixed + 3 notes), 518,019 bytes, 21 KB gzipped | file |
| Verse visuals | 73 chapters in 11 books; 2,792 SVGs + 3 TXT; 0 raster; 0 `.mobile` | manifest |
| SVG motion | 99 indefinite loops; 224 animations > 5 s; max 6.78 s; 193 share `id="clip1"`; 2,792 contain `<text>` | SVG scan |
| Audio | 2,352 WEB MP3s + 32 KJV; manifest 2,384 keys; neural audio for 77 chapters (Psalms 119 4/176) | web/audio |
| Likely-stale narration | 115 (91 with no cache entry, 24 differing) | TTS cache comparison |
| Pronunciations | 3,331 (ok 1,524, fixed 861, unfixed 616, suggested 168, unsure 162); 218 never in WEB; 40 hyphenated; 24 with WEB spaced form | JSON vs WEB tokens |
| Root Python | 80 (61 tracked, 19 untracked = 18,454 lines); 17 tracked files modified (+5,000/−1,675) | `git status`, `wc -l` |
| Import graph | 223 import statements (217 edges); generate_tabernacle 33 importers, svg_surface 27, svg_figures 18, passages 13, config 12 | AST scan |
| Registry | 23 families / 22 generator scripts (working tree; HEAD: 21 families); after Step 0, 25 families / 24 scripts, of which 1 (the 1 Chronicles tree) accepts `--only` | svg_generators.json |
| Commits | 98, of which 54 are "Publish:"; last non-Publish commit `99e23ed6` (2026-08-04) | `git log` |
| `.git` | 262.6 MiB packed + 30.5 MiB loose; blobs 291.3 MiB, of which ~145 MiB is purgeable (raster 109.0, stills 20.2, translations 11.7, suffixed 4.5) | `git count-objects`, `cat-file` |
| Local clutter | `_scratch` 738 files / 43.6 MiB; `mockups` 128 / ~4.6 MB; `backups` 3,768 / 245 MiB; `renders` 356 MiB; `deploy_temp` 1,037 / 169 MiB; `cache/passages` 1,234; `cache/audio/tts` 22,381 / 510 MiB; 7 non-WEB XMLs 52.1 MB | `find`, `du` |
| Root docs | 15 `.md` + 1 `.xlsx`, 597,037 bytes; pronunciation reports 312,775 (52%) | `ls` |
| PC control bar | Needs 1,463 px vs a 1,180 px window (900 px minimum); tool buttons 799 px | Tk reconstruction at scaling 1.25 |

---

## Appendix C. Open risks and things not verified

1. **Cloudflare configuration can't be seen from the repo**: Workers Builds vs Pages, build and deploy commands, branch builds, plan tier. D7(c) depends on it; check it in Step 0.2.
2. *(Moot: D4 dropped reduced-motion support, so there is no inline renderer to test on iOS.)*
3. **Wake Lock** in an installed home-screen app on iOS. Unverified.
4. **Phone layout widths** (the two-row header and one-line progress at 375 px) are estimates; nothing was rendered.
5. **pywebview-embedded Preview of the full web app on ARM64** has been proven only for SVG Studio's page, not for the full web app (served at `/`, S4) with autoplay audio. The S4 acceptance checklist (§5.5) is the gate before the old player is deleted.
6. **Workers Paid static-asset limit** (believed 100,000 per version) is unverified.
7. **The stale-narration count (115)** depends on `cache/audio/tts` never having been partially cleared, and it was measured once.
8. **`import_translation.py` output** has never been diffed against the committed `bibles/WEB`. Dry-run it before trusting it.
9. **Line numbers** are from today's working tree with large uncommitted diffs. After the Step 0 commits they are still valid, but every later edit shifts them, so search by symbol.
10. **Half-finished code in the 36 uncommitted files**: the Step 0 catch-up commit captures whatever state they are in. Review the diffs first; the `pre-cleanup` tag is a snapshot, not a quality gate.
11. **Whether the cloud build installs wrangler from `package-lock.json`** (the 4.107.0 pin) is unknown, so don't delete `package*.json` until you have checked.
12. **The re-keyed pronunciation entries** (e.g. `Beth Zur`) change how those names are spoken. Re-verify the 8 tuned ones by ear.
13. **The Acts 15 continuity check** (15:33 → 15:35) was reasoned from code (nothing first draws at `P(15,34)`), not watched.
14. **The 99 looping SVGs keep looping for everyone,** including visitors with an OS reduce-motion setting (D4's accepted trade-off).
15. **The history rewrite (D8)** invalidates any other clone, including a Claude cloud session's checkout.

---

## Appendix D. Where the audits disagreed, and how this plan resolves each one

This plan merged seven audits (translation layer, web UI, PC shell, Studio tools, deploy and repo weight, docs, Python module graph) and a verification pass over each; where a verifier corrected an auditor, the plan uses the corrected figure. Disagreements already settled as decisions are not repeated here: the PC app's identity and the Display window (D1, D2), the window model (D3), `deploy_bundle` (D7), the history rewrite (D8) and folder layout (D10). The stills order is in WS3 (the web audit's "either order" holds for the web only). The rest:

| Topic | Positions | Resolved as |
|---|---|---|
| Audio manifest key format | Web audit: switch to bare keys. Three verifiers: keep `.WEB`. | **Keep** `Book_c_v.WEB` (D11). `_migrate_manifest` (generate_showcase_audio.py:73-98) would add `.WEB` back on the next Audio Renderer run, and `coverage_studio._scan_audio` (`rpartition('.')`, L144) would show zero audio. The web lookup becomes the constant `${key}.WEB` (WS1b). |
| Manifest v3 | Web audit: a slim v3. Verifier: keep v2. | **Keep v2**; only `still` goes. v3 saves about 7 KB gzipped and breaks `coverage_studio._scan_visuals` and `svg_studio`. |
| Notes data | Leave in JSON vs. strip at re-import; `Passage(**data)` TypeError | Remove notes from all code and UI; **leave the JSON untouched**, and have the loader pick keys explicitly. Keep `"translation":"WEB"` too, for D11 (no churn in 1,189 files) and so `import_translation.py` round-trips byte-identically. After WS1b the web no longer reads the field (`resolveAudio` uses the constant `${key}.WEB`), so it is not load-bearing. |
| "The PC app reads WEB from bible-api.com" (deploy audit) | Refuted by the verifier | The PC already reads local JSON. The live hazard is the opposite: deleting the folders **before** the code changes makes the "api" fallback re-download KJV, DRA and the others and write `.KJV.svg` files again. Hence code first (WS1). |
| isbe_* scripts | Module graph: delete all. Studio: move to `tools/pronunciation/`. Verifier: `isbe_sweep` is the only headless respelling proposer. | Delete the six one-offs, `name_ipa.py` and `isbe_index.json`; **keep `isbe_sweep.py` + `isbe_harvest.json` at the root** for the 616 unfixed names (WS4d). No `tools/pronunciation/`: one script doesn't need a folder. |
| `svg_freeze.freeze_still` | Keep for future link-preview cards vs. delete | Delete with the stills (46 lines plus 6 tests); restore from history if preview cards are built. |
| Non-WEB pronunciation keys | Docs audit: 239. Others: 218. | **218** with `respell()`'s own rule; 239 was not reproducible (D13). |
| Reduced motion after the stills (dropped by D4) | Inline renderer vs. none | **None** (D4). Recorded in case you want it back: render the stage SVG inline (`DOMParser` → `replaceChildren`, which restarts SMIL), mark it `aria-hidden`, and under `matchMedia('(prefers-reduced-motion: reduce)')` call `pauseAnimations(); setCurrentTime(60)` in a requestAnimationFrame (longest animation measured: 6.78 s). Needs `user-select:none` on `#stage`, text-only prefetch (193 SVGs share `id="clip1"`), and an iPhone/iPad check. About M effort. |
