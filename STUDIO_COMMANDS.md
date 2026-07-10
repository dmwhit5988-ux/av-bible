# Studio build-out — session prompts

Copy-paste prompts for driving each remaining step of `STUDIO_PLAN.md`.
Feature A (Pronunciation Studio) is **done** (commits e8b6a47…e537f37).

How to use:
- Start a **fresh session** per step, with the model shown in the header.
- Paste the prompt verbatim. Each one is self-contained (tells the model
  which files to read), so it works with zero conversation history.
- Commit and verify between steps before starting the next.

---

## Step 2 — Chapter→MP3 batch renderer, PC side only
**Model: Sonnet 5** · Effort: easy-to-moderate · Safe: touches only the desktop app

```
Read STUDIO_PLAN.md (Feature C and the Build order section) in the repo root,
then build step 2 of the build order: the Chapter→MP3 batch renderer, PC side
only, WEB translation only for now.

Generalize generate_showcase_audio.py into a built-in studio tool:
- Add an "Audio Renderer" entry in app.py that opens a tk.Toplevel, following
  the exact same integration pattern as the Pronunciation Studio (see how
  pronunciation_tool.py's App is opened from app.py, pre-loaded on the
  currently selected book/chapter).
- UI: book picker, chapter range (from/to), voice picker (same voices the
  reader offers), Render button, per-verse progress bar with a status line,
  and a working Cancel that stops between verses.
- Include a translation dropdown in the UI but keep it locked to WEB for now
  with a tooltip/label saying other translations arrive with the web-side
  manifest change (STUDIO_PLAN.md Feature C caveat 1). Structure the render
  code so translation is already a parameter, so step 3 only unlocks it.
- Rendering must go through the same production path the reader uses:
  tts_engine.synthesize with respell applied, and the same passage-fetch
  calls generate_showcase_audio.py uses. Output files and the
  web/audio/manifest.json update must match what generate_showcase_audio.py
  produces today, byte-for-byte in format, so the web player keeps working.
- Add the file-count guardrail from STUDIO_PLAN.md: before rendering, show
  projected new file count and the resulting total against the ~20k
  Cloudflare Pages ceiling (count files under web/, or the deploy_bundle
  logic in prepare-deploy.ps1 — read it to match what actually deploys).
- Keep generate_showcase_audio.py working as a standalone script; share code
  rather than duplicating it.
- Run long renders on a worker thread so the UI stays responsive (the
  Pronunciation Studio and audio_player.py show the project's threading
  patterns).

Do not touch anything under web/ in this step. When done, tell me exactly how
to verify: which app to run, which chapter to render, and what files/manifest
entries to check.
```

**Verify before moving on:** render one small chapter (e.g. Psalm 117),
confirm the MP3s appear, `web/audio/manifest.json` gains the entries, cancel
mid-render works, and the reader still plays cached showcase audio.

---

## Step 3 — Web multi-translation audio
**Model: Sonnet 5** · Effort: moderate · Touches web/ — deploy via GitHub afterwards

```
Read STUDIO_PLAN.md (Feature C, caveat 1) in the repo root. Implement step 3
of the build order: make the static web app's pre-rendered audio
translation-aware, then unlock the translation picker in the desktop Audio
Renderer tool.

Current state: web/audio/manifest.json is a flat Book_ch_v → file map with no
translation dimension, and resolveAudio in the web tts.js only swaps in an
MP3 when the visitor has WEB selected.

Required changes:
1. Key audio files and the manifest by translation (Book_ch_v.KJV.mp3 style,
   mirroring how visuals already use a translation-suffix chain like
   .KJV.svg → .svg — read how the web app resolves visuals and stay
   consistent with that convention).
2. Teach the web Player/resolveAudio to look up the visitor's currently
   selected translation, falling back to Web Speech synthesis when no MP3
   exists for that translation (the current behavior for non-WEB).
3. Migration: existing rendered files are WEB. Choose and implement the
   cleanest backward-compatible path (e.g. manifest v2 with a translation
   level plus a one-time migration in build_manifest.py or the renderer) —
   the deployed site must keep playing existing WEB audio with no re-render.
4. Update build_manifest.py and prepare-deploy.ps1 if they touch the audio
   manifest or copy audio files.
5. Desktop side: unlock the translation dropdown in the Audio Renderer tool
   (app.py) so it renders and manifests files under the new keying.
6. Keep the file-count guardrail accurate — every extra translation
   multiplies files; the projection must account for the selected
   translation (STUDIO_PLAN.md and the ~20k Cloudflare Pages file ceiling).

Constraint: the web app is static vanilla JS with no build step — keep it
that way. I deploy through GitHub, not local wrangler, so don't attempt a
local wrangler deploy; just tell me what to commit.

When done, tell me exactly how to verify locally (which file to open / local
server to run) before I push.
```

**Verify before moving on:** locally serve `web/`, confirm WEB audio still
plays, render one chapter in KJV from the desktop tool, confirm the site
plays it with KJV selected and falls back to speech synthesis for
translations without MP3s. Then push and check the deployed site.

---

## Step 4a — SVG Studio: architecture & design (no code)
**Model: Opus 4.8** · This is the one design everything hangs off — spend the tokens here

```
Read STUDIO_PLAN.md in the repo root, especially Feature B and the
"Decisions for the SVG Studio (resolved 2026-07-08)" section. Those
decisions are settled — do not relitigate them (pywebview embedded preview
with system-browser fallback; generator-owned files detected and routed to
the Python spec, never blocked; Inkscape optional with guided install).

Your job is design only — produce SVG_STUDIO_DESIGN.md, no code changes.

First re-immerse in the pipeline by reading: svg_surface.py, one or two
generators (generate_numbers34_svg.py, generate_matthew1_svg.py),
generate_acts1314_svg.py (hand-authored style), build_manifest.py,
visual_stage.py (how the desktop reader finds/renders visuals today),
prepare-deploy.ps1, and how the web app resolves the translation-suffix
chain (.KJV.svg → .svg) in visuals/manifest.json.

The design doc must cover:
1. Module layout: what new files, what changes to app.py, how the studio
   window opens (same Toplevel pattern as the Pronunciation Studio).
2. The pywebview preview: process/threading model alongside tkinter's
   mainloop, the temp-HTML wrapper, live reload on edit, and playing the
   verse's MP3 timed with the SMIL animation. Specify the system-browser
   fallback path and the exact conditions to fall back.
3. The "start from previous verse's final frame" algorithm for
   hand-authored sequences: how to freeze fill="freeze" SMIL animations to
   end values and demote to a static base <g>, precisely enough that a
   build model can implement it without design decisions. Note where it
   deliberately does NOT apply (generated families build cumulatively
   already).
4. The generator registry: file format and location mapping verse ranges →
   generator module + the spec structure to edit (CHAPTERS dicts, LANDMARKS,
   name-variant tables), and the UI flow for "Edit spec (durable)" vs
   "Hand-edit this SVG anyway (one-off)".
5. The verse navigator: translation-suffix resolution, showing which
   variants exist.
6. Save/publish glue: write .svg, re-run build_manifest.py, optional stage
   via prepare-deploy.ps1.
7. Risks: pywebview on Windows ARM64 (native-dependency pain is a known
   hazard on this machine — cairosvg/Cairo were rejected for exactly this;
   verify pywebview's ARM64 story and name the fallback trigger), tkinter +
   webview event-loop conflicts, SMIL freeze edge cases.
8. A build plan: an ordered list of 4–8 implementation tasks, each sized for
   a Sonnet session, each independently testable, with explicit "done when"
   criteria. Mark any task you judge too design-sensitive for Sonnet.

End by listing any open questions that genuinely need my input; make a
recommendation for each.
```

**Between 4a and 4b:** read `SVG_STUDIO_DESIGN.md` yourself, answer its open
questions, and commit it. The build sessions will treat it as gospel.

---

## Step 4b — SVG Studio: build (repeat per task)
**Model: Sonnet 5** · One fresh session per task from the design doc's build plan

```
Read SVG_STUDIO_DESIGN.md and STUDIO_PLAN.md (Feature B) in the repo root.
The design is settled — implement it, don't redesign it.

Implement task N of the build plan in SVG_STUDIO_DESIGN.md: "<paste the
task's title and description here>".

Tasks before N are already built and committed — read the current code
rather than assuming the doc's snapshot. Follow the existing project
patterns (Toplevel tools opened from app.py, threading style in
audio_player.py / the audio renderer).

When done, walk me through verifying the task's "done when" criteria by
hand, then stop — don't start the next task.
```

Escalate a single task to **Opus 4.8 / Fable 5** only if a Sonnet session gets
stuck (the plan flags webview integration as the likely candidate). When
escalating, say: *"A previous session attempted this and got stuck — here's
what happened: …"* and paste the failure.

---

## Odd jobs — mechanical glue
**Model: Haiku 4.5** · Use for anything purely mechanical between steps

Examples worth delegating cheaply:
- "Re-run build_manifest.py and prepare-deploy.ps1, confirm deploy_bundle
  matches web/, and list any orphaned audio/visual files."
- "Add <new tool> to the studio menu in app.py following the exact pattern
  of the existing entries."
- Batch renders themselves (no model needed — the tool from step 2 does it).

---

## Cross-session rules (put at the end of any prompt if the model drifts)

- This machine is **Windows 11 ARM64** — avoid packages with native wheels
  that lack ARM64 builds; deploys go through **GitHub**, never local wrangler.
- The web app stays **static vanilla JS, no build step, no framework**.
- The desktop app is tkinter; new tools open as `tk.Toplevel` from `app.py`.
- Never hand-edit generated SVGs expecting durability — the Python spec is
  the source of truth for generator families.
