#!/usr/bin/env python3
"""Scan visuals/ and generate manifest.json — schema v2.

v2 keeps v1's keys (exact file stems: "Genesis_5_3.KJV", "Genesis_5_3",
"default") but each entry is a list of per-file records instead of bare
paths, so the web app can filter/present by metadata without re-deriving it:

    {
      "version": 2,
      "entries": {
        "Acts_13_1": [
          {"file": "Acts/13/Acts_13_1.svg",
           "kind": "map",
           "animated": true,
           "still": "Acts/13/Acts_13_1.still.svg"}
        ]
      }
    }

Record fields:
  file      relative path from visuals/, forward slashes (as v1)
  kind      classification for future display modes. Resolution order:
            1. data-kind="…" on the SVG root element (hand-author override,
               travels inside the file itself)
            2. the owning generator family's "kind" (svg_generators.json)
            3. extension default: png/jpg -> photo, txt/rtf -> note,
               everything else -> infographic
  animated  SMIL sniff for .svg; gif/webp are the animated raster formats
            and count as true; static formats false
  still     present only when a <stem>.still.svg reduced-motion twin exists
            (built by build_stills.py). Still files are attached here, never
            indexed as entries of their own.

Only web/js/visuals.js consumes this file; the desktop app probes the
filesystem directly (visual_stage.py).
"""

import json
import re
from pathlib import Path
from collections import defaultdict

import svg_registry
from svg_freeze import svg_is_animated

VISUALS_DIR = Path("visuals")
MANIFEST_PATH = VISUALS_DIR / "manifest.json"

# Extensions supported: vector diagrams (.svg), raster images, plus text
# files (.txt/.rtf), which the app renders as an on-stage text panel styled
# like the translator notes.
IMAGE_EXTS = {".svg", ".webp", ".gif", ".png", ".jpg", ".jpeg", ".txt", ".rtf"}

STILL_SUFFIX = ".still"

_KIND_BY_EXT = {
    ".png": "photo", ".jpg": "photo", ".jpeg": "photo",
    ".txt": "note", ".rtf": "note",
}
_DEFAULT_KIND = "infographic"

_DATA_KIND_RE = re.compile(r'<svg\b[^>]*\bdata-kind="([^"]+)"')
# Verse-key shape after stripping variant suffixes: Book_ch or Book_ch_v,
# where Book may itself contain underscores (Song_of_Solomon).
_KEY_RE = re.compile(r"^(.+?)_(\d+)(?:_(\d+))?$")


def _book_chapter_verse(stem: str) -> tuple[str, int, int | None] | None:
    """(book, chapter, verse) parsed from a verse-key stem (translation/mobile
    suffixes already stripped), or None for non-verse keys ("default"). The
    verse is None for a chapter-level key ("Genesis_1"); it matters because a
    chapter can be split between two generator families (Genesis 11)."""
    m = _KEY_RE.match(stem)
    if not m:
        return None
    return (m.group(1).replace("_", " "), int(m.group(2)),
            int(m.group(3)) if m.group(3) else None)


def _base_stem(stem: str) -> str:
    """Strip variant suffixes (.KJV / .mobile / …) down to the verse key:
    "Genesis_5_3.KJV.mobile" -> "Genesis_5_3"."""
    return stem.split(".", 1)[0]


def _classify(path: Path, rel_path: str, stem: str) -> dict:
    """Build the metadata record for one visual file."""
    ext = path.suffix.lower()
    svg_text = None
    if ext == ".svg":
        try:
            svg_text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            svg_text = None

    kind = None
    if svg_text is not None:
        m = _DATA_KIND_RE.search(svg_text)
        if m:
            kind = m.group(1)
    if kind is None:
        parsed = _book_chapter_verse(_base_stem(stem))
        if parsed:
            family = svg_registry.owner_of(*parsed)
            if family is not None:
                kind = family.kind
    if kind is None:
        kind = _KIND_BY_EXT.get(ext, _DEFAULT_KIND)

    if svg_text is not None:
        animated = svg_is_animated(svg_text)
    else:
        animated = ext in (".gif", ".webp")

    return {"file": rel_path, "kind": kind, "animated": animated}


def _scan_files():
    """Yield every manifest-relevant file: (path, rel_path, stem)."""
    seen = set()
    # Nested layout: visuals/<Book>/<chapter>/<Book>_<ch>_<v>[.CODE].ext
    for book_dir in VISUALS_DIR.glob("*"):
        if not book_dir.is_dir() or book_dir.name.startswith("."):
            continue
        for chapter_dir in book_dir.glob("*"):
            if not chapter_dir.is_dir() or chapter_dir.name.startswith("."):
                continue
            for f in chapter_dir.glob("*"):
                if f.is_file() and f.suffix.lower() in IMAGE_EXTS:
                    rel = f.relative_to(VISUALS_DIR).as_posix()
                    seen.add(rel)
                    yield f, rel, f.stem
    # Flat layout: visuals/<Book>_<ch>[_<v>][.CODE].ext and visuals/default.*
    for f in VISUALS_DIR.glob("*"):
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS:
            rel = f.name
            if rel not in seen:
                yield f, rel, f.stem


def build_manifest():
    """Scan visuals/ and build the v2 manifest. Returns the entries dict."""
    entries = defaultdict(list)
    stills = {}  # base rel_path ("Acts/13/Acts_13_1.svg") -> still rel_path

    for path, rel_path, stem in _scan_files():
        # A .still.svg is metadata on its base file, not an entry: index it
        # under the base's rel_path and attach after the scan.
        if stem.endswith(STILL_SUFFIX) and path.suffix.lower() == ".svg":
            base_rel = rel_path[: -len(STILL_SUFFIX + ".svg")] + ".svg"
            stills[base_rel] = rel_path
            continue
        # Key by the exact stem: "Genesis_5_3.KJV" for a translation-suffixed
        # file, "Genesis_5_3" for a plain one. Do NOT also add suffixed files
        # under the plain key — that would make the generic (no-translation)
        # lookup randomly pick up another translation's file.
        entries[stem].append(_classify(path, rel_path, stem))

    for records in entries.values():
        for record in records:
            still = stills.pop(record["file"], None)
            if still:
                record["still"] = still
        records.sort(key=lambda r: r["file"])

    if stills:
        print(f"[WARN] {len(stills)} orphaned .still.svg file(s) with no "
              f"base SVG (run build_stills.py to clean up):")
        for still in sorted(stills.values()):
            print(f"  - {still}")

    manifest = {"version": 2, "entries": dict(entries)}
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

    return dict(entries)


if __name__ == "__main__":
    entries = build_manifest()
    n_stills = sum(1 for recs in entries.values() for r in recs if "still" in r)
    n_animated = sum(1 for recs in entries.values()
                     for r in recs if r["animated"])
    print(f"[OK] Written {len(entries)} verse keys to {MANIFEST_PATH} "
          f"(schema v2; {n_animated} animated file(s), "
          f"{n_stills} with a still variant)")
    print("\nSample entries:")
    for key, recs in list(entries.items())[:3]:
        print(f"  {key}:")
        for r in recs[:2]:
            print(f"    - {r}")
        if len(recs) > 2:
            print(f"    ... and {len(recs) - 2} more")
