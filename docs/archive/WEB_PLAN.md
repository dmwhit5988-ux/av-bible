# AV Bible — Web Phase Plan

Goal: free, demo-quality web version hosted on Cloudflare, usable full-screen on iPhone.
Total cost: $0 (optional ~$10/yr domain later via Cloudflare Registrar).

Run each phase in a **fresh Claude Code session from this folder**, switching models
with `/model` first. Escalate to Opus/Fable only for a gnarly bug Sonnet can't crack
(paste just the symptom + relevant file, not the whole history).

---

## Phase 0 — Accounts and tools (you, no Claude, ~20 min)

1. Create a free Cloudflare account at dash.cloudflare.com
2. Install Node.js LTS from nodejs.org (only needed for the `wrangler` deploy CLI)

---

## Phase 1 — Git + asset manifest — model: **Haiku 4.5**

Prompt:

> Prepare this project for a web phase. 1) `git init` this folder with a .gitignore
> excluding `.venv/`, `cache/`, `__pycache__/`, `config.json`, `backups/`, and
> `bibles/*.xml` (keep `bibles/<CODE>/` JSON dirs and `visuals/` tracked), then make
> an initial commit. 2) Write `build_manifest.py` that scans `visuals/` (nested
> `<Book>/<chapter>/` layout plus legacy flat files) and writes
> `visuals/manifest.json` mapping every verse key like `Genesis_5_3` (and
> translation-suffixed variants like `Genesis_5_3.KJV`) to its file path — the web
> app will use this instead of probing for files. Run it and show me a sample of
> the output.

---

## Phase 2 — Build the web app — model: **Sonnet 5**

Prompt:

> Build a static web version of this Bible app in a new `web/` folder — plain
> HTML/CSS/JS, no build step, no framework, mobile-first for iPhone Safari. Read
> `passages.py`, `visual_stage.py`, `books.py`, and the project memory first.
> Requirements: (1) Translation/Book/Chapter/Verse pickers matching the desktop
> app's 9 local translations, fetching chapter JSON directly from
> `bibles/<CODE>/<Book>_<ch>.json`. (2) Read-aloud via the Web Speech API, one
> utterance per verse so verse boundaries are exact, with play/pause/next/prev;
> must start from a tap (iOS requires a user gesture). (3) A visual stage that
> ports the `_find_image` fallback chain from visual_stage.py using
> `visuals/manifest.json` — animated WebP/GIF letterboxed, photos cover-cropped,
> translation-suffixed files preferred, verse→chapter→book→default fallback.
> (4) Show translator notes while a verse is read, and the attribution line.
> (5) The stage fills the screen in a tap-to-toggle fullscreen mode. Serve locally
> with `python -m http.server` from the project root for testing so `bibles/` and
> `visuals/` resolve.

Then test in your desktop browser AND on your iPhone over Wi-Fi
(`http://<pc-ip>:8000/web/` — Claude can tell you your PC's local IP).
Note what feels wrong on the phone; you'll paste it into Phase 3.

---

## Phase 3 — iPhone polish + PWA full-screen — model: **Sonnet 5**

Prompt:

> Make `web/` a proper installable PWA polished for iPhone: manifest.json +
> apple-touch-icon so Add to Home Screen launches standalone full-screen;
> `viewport-fit=cover` with safe-area-inset padding for the notch; use `100dvh`
> not `100vh`; portrait layout with controls reachable one-handed and a landscape
> mode that goes stage-only; Wake Lock API so the screen stays on during playback;
> make sure speech keeps advancing verses when the visual stage is fullscreen.
> Test issues I found: [paste whatever felt wrong on your phone].

---

## Phase 4 — Deploy to Cloudflare — model: **Haiku 4.5**

Prompt:

> Deploy this project's `web/` app to Cloudflare using wrangler direct upload
> (I have a Cloudflare account and Node installed). Set up the config so the
> deployed site contains `web/` at the root plus the `bibles/<CODE>/` JSON dirs
> and `visuals/` — but NOT the XML source files, cache, or Python code. Walk me
> through `wrangler login` and do the first deploy, then give me the URL.

Result: a live `https://….pages.dev` URL with HTTPS, openable on your iPhone.
Redeploys after new visuals are one command (only changed files upload).

---

## Phase 5 (optional) — Neural audio for showcase chapters — model: **Haiku 4.5**

Web Speech voices are decent; this adds edge-tts neural quality for the chapters
that have visuals (Gen 1/5/11, Ex 25–27, Num 32/34, Mt 1, Lk 3 ≈ 330 verses ≈ 15 MB).

Prompt:

> Write a script that uses the existing edge-tts pipeline in tts_engine.py to
> pre-generate per-verse MP3s for the chapters that have visuals (Genesis 1, 5,
> 11; Exodus 25-27; Numbers 32, 34; Matthew 1; Luke 3), WEB translation only for
> now, into `web/audio/<Book>_<ch>_<v>.mp3`. Then update the web player to prefer
> a pre-generated MP3 when one exists and fall back to Web Speech otherwise.
> Redeploy.

---

## Later, if the demo graduates

- Real domain: buy in Cloudflare dashboard (Registrar sells at cost, ~$10/yr) — no Claude needed
- Free Cloudflare Web Analytics toggle for visitor counts

## Gotchas

- Project lives in OneDrive: if git or deploy staging hits file-lock errors, pause OneDrive sync
- Animated WebP needs iOS 16+ (fine on modern iPhones)
- Dashboard drag-and-drop deploy caps at ~1,000 files — that's why we use wrangler (~11k files here)
