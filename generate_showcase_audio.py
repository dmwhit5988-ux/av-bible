"""Pre-generate neural-voice narration for the web app's showcase chapters.

The web version normally reads aloud via the browser's Web Speech API, which
on most devices sounds far more robotic than the desktop app's edge-tts
neural voices (no key needed, but it's a Python library — a static site can't
call it directly). This script bridges the gap for a small, fixed set of
chapters: the ones that already have custom-generated visuals, since those
are the app's showcase pieces.

For each verse it reuses tts_engine.synthesize() (the same function the
desktop app calls during live playback) and copies the resulting neural mp3
into web/audio/<Book>_<ch>_<v>.mp3. It also writes web/audio/manifest.json —
a flat {"Book_ch_v": "Book_ch_v.mp3"} map — so the web player can look up
available narration without probing the filesystem (same pattern as
visuals/manifest.json).

WEB translation only: the pre-generated audio narrates one fixed text, so it
can only stand in when the visitor has WEB selected. Every other translation
keeps using Web Speech.

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


def _load_manifest() -> dict:
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _save_manifest(manifest: dict) -> None:
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)


def generate_chapter(book: str, chapter: int, manifest: dict) -> None:
    try:
        passage = fetch_passage("", book, chapter, TRANSLATION)
    except PassageError as e:
        print(f"  skip {book} {chapter}: {e}")
        return
    safe_book = book.replace(" ", "_")
    written = skipped = degraded = 0
    for num, text in passage.verses:
        key = f"{safe_book}_{chapter}_{num}"
        out_path = os.path.join(AUDIO_DIR, f"{key}.mp3")
        if key in manifest and os.path.exists(out_path):
            skipped += 1
            continue
        src_path = tts_engine.synthesize(text, VOICE, RATE)
        if not src_path.lower().endswith(".mp3"):
            # tts_engine fell back to the offline SAPI voice (edge-tts
            # unreachable) — don't ship degraded audio as "showcase" quality.
            degraded += 1
            print(f"    {book} {chapter}:{num} — edge-tts unavailable, "
                  f"skipped (rerun later)")
            continue
        os.makedirs(AUDIO_DIR, exist_ok=True)
        shutil.copyfile(src_path, out_path)
        manifest[key] = f"{key}.mp3"
        written += 1
    print(f"  {book} {chapter}: {written} written, {skipped} already present"
          + (f", {degraded} degraded/skipped" if degraded else ""))


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
