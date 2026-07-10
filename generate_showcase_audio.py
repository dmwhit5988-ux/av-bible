"""Pre-generate neural-voice narration for the web app's showcase chapters.

The web version normally reads aloud via the browser's Web Speech API, which
on most devices sounds far more robotic than the desktop app's edge-tts
neural voices (no key needed, but it's a Python library — a static site can't
call it directly). This script bridges the gap for a small, fixed set of
chapters: the ones that already have custom-generated visuals, since those
are the app's showcase pieces.

For each verse it reuses tts_engine.synthesize() (the same function the
desktop app calls during live playback) and copies the resulting neural mp3
into web/audio/, then updates web/audio/manifest.json — a flat
{"Book_ch_v.CODE": "filename.mp3"} map, one entry per (verse, translation),
mirroring the translation-suffix convention visuals/manifest.json already
uses (see build_manifest.py). The web player looks up narration by the
visitor's currently selected translation and falls back to Web Speech when
no MP3 exists for that translation.

WEB filenames keep their original unsuffixed form (Book_ch_v.mp3) so the
audio already shipped to the deployed site never needs re-rendering; only
the manifest *key* gained the ".WEB" suffix (see _migrate_manifest). New
non-WEB renders get translation-suffixed filenames (Book_ch_v.CODE.mp3) so
they can't collide with WEB's files for the same verse.

Resumable: skips verses whose mp3 already exists. Only ships real neural
audio — if edge-tts is unreachable and tts_engine falls back to the lower
quality offline SAPI voice, that verse is skipped rather than shipping
degraded "showcase" audio (rerun later once online).

Usage:
    python generate_showcase_audio.py
"""

import json
import os
import shutil

from passages import fetch_passage, PassageError
import tts_engine

VOICE = "en-US-AndrewNeural"
RATE = 0
TRANSLATION = "WEB"

# The chapters with custom-generated visuals (see visuals/<Book>/<chapter>/).
SHOWCASE_CHAPTERS = [
    ("Genesis", 1), ("Genesis", 5), ("Genesis", 11),
    ("Exodus", 25), ("Exodus", 26), ("Exodus", 27),
    ("Numbers", 32), ("Numbers", 34),
    ("Matthew", 1),
    ("Luke", 3),
    ("Acts", 13), ("Acts", 14),
]

WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
AUDIO_DIR = os.path.join(WEB_DIR, "audio")
MANIFEST_PATH = os.path.join(AUDIO_DIR, "manifest.json")


def _manifest_key(base: str, translation: str) -> str:
    """'Genesis_1_1', 'KJV' -> 'Genesis_1_1.KJV' — same suffix convention as
    visuals/manifest.json's translation-specific keys."""
    return f"{base}.{translation}"


def _audio_filename(base: str, translation: str) -> str:
    """WEB keeps its original unsuffixed filename (already deployed, never
    renamed); every other translation gets a suffixed one so it can't
    collide with WEB's file for the same verse."""
    return f"{base}.mp3" if translation == "WEB" else f"{base}.{translation}.mp3"


def _migrate_manifest(manifest: dict) -> tuple:
    """Pre-multi-translation manifests keyed plainly ('Book_ch_v' ->
    'Book_ch_v.mp3'), always WEB narration. Add the explicit '.WEB' suffix so
    every key names its translation. Filenames on disk are untouched — no
    re-render needed. Returns (migrated_manifest, changed)."""
    migrated = {}
    changed = False
    for key, filename in manifest.items():
        if "." not in key:
            migrated[_manifest_key(key, "WEB")] = filename
            changed = True
        else:
            migrated[key] = filename
    return migrated, changed


def _load_manifest() -> dict:
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except (OSError, ValueError):
        return {}
    migrated, changed = _migrate_manifest(manifest)
    if changed:
        _save_manifest(migrated)
    return migrated


def _save_manifest(manifest: dict) -> None:
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)


def generate_chapter(book: str, chapter: int, manifest: dict, voice: str = VOICE,
                      rate: int = RATE, translation: str = TRANSLATION,
                      passage=None, on_verse=None, should_stop=None) -> tuple:
    """Render one chapter's verses into web/audio/ and update `manifest`.

    Reused by both this CLI script and the Audio Renderer studio (audio_studio.py)
    so both go through the exact same synth/copy/manifest logic.

    `passage`, if given, skips the fetch (the studio pre-fetches during its
    file-count scan and reuses it here). `on_verse(num, status)` is called
    after each verse with status in {"written", "skipped", "degraded"} — lets
    a caller drive a progress bar. `should_stop()`, checked before each verse,
    lets a caller cancel between verses. Returns (written, skipped, degraded).
    """
    if passage is None:
        try:
            passage = fetch_passage("", book, chapter, translation)
        except PassageError as e:
            print(f"  skip {book} {chapter}: {e}")
            return 0, 0, 0
    safe_book = book.replace(" ", "_")
    written = skipped = degraded = 0
    for num, text in passage.verses:
        if should_stop and should_stop():
            break
        base = f"{safe_book}_{chapter}_{num}"
        key = _manifest_key(base, translation)
        filename = _audio_filename(base, translation)
        out_path = os.path.join(AUDIO_DIR, filename)
        if key in manifest and os.path.exists(out_path):
            skipped += 1
            if on_verse:
                on_verse(num, "skipped")
            continue
        src_path = tts_engine.synthesize(text, voice, rate)
        if not src_path.lower().endswith(".mp3"):
            # tts_engine fell back to the offline SAPI voice (edge-tts
            # unreachable) — don't ship degraded audio as "showcase" quality.
            degraded += 1
            print(f"    {book} {chapter}:{num} — edge-tts unavailable, "
                  f"skipped (rerun later)")
            if on_verse:
                on_verse(num, "degraded")
            continue
        os.makedirs(AUDIO_DIR, exist_ok=True)
        shutil.copyfile(src_path, out_path)
        manifest[key] = filename
        written += 1
        if on_verse:
            on_verse(num, "written")
    print(f"  {book} {chapter}: {written} written, {skipped} already present"
          + (f", {degraded} degraded/skipped" if degraded else ""))
    return written, skipped, degraded


def main() -> int:
    os.makedirs(AUDIO_DIR, exist_ok=True)
    manifest = _load_manifest()
    print(f"Generating showcase narration ({VOICE}) for "
          f"{len(SHOWCASE_CHAPTERS)} chapter(s)...")
    for book, chapter in SHOWCASE_CHAPTERS:
        generate_chapter(book, chapter, manifest)
        _save_manifest(manifest)  # save after each chapter, resumable
    total_bytes = sum(
        os.path.getsize(os.path.join(AUDIO_DIR, fn))
        for fn in manifest.values()
        if os.path.exists(os.path.join(AUDIO_DIR, fn))
    )
    print(f"\nDone: {len(manifest)} verse(s) narrated, "
          f"{total_bytes / 1_000_000:.1f} MB in {AUDIO_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
