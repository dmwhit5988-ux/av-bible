#!/usr/bin/env python3
"""Scan visuals/ and generate manifest.json — schema v2.

Keys are verse keys ("Genesis_5_3"), or "Genesis_5" for a whole-chapter
graphic; each entry is a list of per-file records, so readers can
filter/present by metadata without re-deriving it. Two ways a key can point
at a file other than its own (D17, one picture across several verses):
  - a range file, Book_c_v1-v2.svg, supplies every WEB verse in its range
    that has no file of its own;
  - a verse whose SVG is byte-identical to the previous verse's points at
    the first file of that run (unless its family sets "replay_identical").
The web app keeps a picture running while the next verse shows the same file.


    {
      "version": 2,
      "entries": {
        "Acts_13_1": [
          {"file": "Acts/13/Acts_13_1.svg",
           "kind": "map",
           "animated": true}
        ]
      }
    }

Record fields:
  file      relative path from visuals/, forward slashes (as v1)
  kind      classification for future display modes. Resolution order:
            1. data-kind="…" on the SVG root element (hand-author override,
               travels inside the file itself)
            2. the owning generator family's "kind" (svg_generators.json)
            3. extension default: png/jpg -> photo, everything else ->
               infographic
  animated  SMIL sniff for .svg; gif/webp are the animated raster formats
            and count as true; static formats false

Read by web/js/visuals.js (verse key, then chapter key), coverage_studio.py
and svg_studio.py; the desktop stage probes the filesystem directly
(visual_stage.py).

WEB is the only translation, so visual files carry no translation suffix. A
suffixed name (Genesis_5_3.KJV.svg) is a leftover that nothing serves;
build_manifest() warns about any it finds under visuals/.
"""

import hashlib
import json
import re
from pathlib import Path
from collections import defaultdict

import passages
import svg_registry
from svg_freeze import svg_is_animated

# Beside this file, not under the cwd, so it runs from any folder.
VISUALS_DIR = Path(__file__).resolve().parent / "visuals"
MANIFEST_PATH = VISUALS_DIR / "manifest.json"

# Extensions indexed: vector diagrams (.svg) and raster images. Anything
# else under visuals/ (manifest.json itself) is not a visual.
IMAGE_EXTS = {".svg", ".webp", ".gif", ".png", ".jpg", ".jpeg"}

_KIND_BY_EXT = {
    ".png": "photo", ".jpg": "photo", ".jpeg": "photo",
}
_DEFAULT_KIND = "infographic"

_DATA_KIND_RE = re.compile(r'<svg\b[^>]*\bdata-kind="([^"]+)"')
# Verse-key shape after stripping a .mobile suffix: Book_ch or Book_ch_v,
# where Book may itself contain underscores (Song_of_Solomon).
_KEY_RE = re.compile(r"^(.+?)_(\d+)(?:_(\d+))?$")
# One picture tied to a verse range on purpose (D17): Numbers_32_16-32.svg.
_RANGE_RE = re.compile(r"^(.+?)_(\d+)_(\d+)-(\d+)$")
# Retired variants (same pattern as test_registry.RETIRED): a translation
# suffix (Genesis_5_3.KJV.svg, or a .WEB.svg that would shadow the plain file;
# WEB is the only translation) or a reduced-motion .still.svg twin (D4).
_RETIRED_RE = re.compile(
    r"\.(KJV|ASV|BBE|BSB|DARBY|DRA|YLT|OEB|WEB)\.|\.still\.svg$")


def _book_chapter_verse(stem: str) -> tuple[str, int, int | None] | None:
    """(book, chapter, verse) parsed from a verse-key stem, or None for a
    stem that isn't one. The verse is None for a chapter-level key
    ("Genesis_1"); it matters because a chapter can be split between two
    generator families (Genesis 11)."""
    r = _RANGE_RE.match(stem)
    if r:  # a range file belongs to whoever owns its first verse
        return r.group(1).replace("_", " "), int(r.group(2)), int(r.group(3))
    m = _KEY_RE.match(stem)
    if not m:
        return None
    return (m.group(1).replace("_", " "), int(m.group(2)),
            int(m.group(3)) if m.group(3) else None)


def _base_stem(stem: str) -> str:
    """Strip a .mobile suffix down to the verse key:
    "Genesis_5_3.mobile" -> "Genesis_5_3"."""
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
    # Nested layout: visuals/<Book>/<chapter>/<Book>_<ch>_<v>.ext
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
    # Flat layout: visuals/<Book>_<ch>[_<v>].ext
    for f in VISUALS_DIR.glob("*"):
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS:
            rel = f.name
            if rel not in seen:
                yield f, rel, f.stem


def _retired_leftovers() -> list[str]:
    """Every retired variant file anywhere under visuals/, as sorted
    visuals/-relative paths."""
    return sorted(f.relative_to(VISUALS_DIR).as_posix()
                  for f in VISUALS_DIR.rglob("*")
                  if f.is_file() and _RETIRED_RE.search(f.name))


def _file_digest(rel_path: str) -> str | None:
    try:
        return hashlib.sha1((VISUALS_DIR / rel_path).read_bytes()).hexdigest()
    except OSError:
        return None


def _share_identical_runs(entries) -> int:
    """Point a verse whose picture is byte-identical to the previous verse's
    at the first file of the run, so the web app shows one picture across
    the run instead of replaying it (D17). Recomputed on every build, so a
    run splits by itself once a generator makes two verses differ. A family
    with "replay_identical": true in the registry opts out. Returns how many
    verses now share their previous verse's picture."""
    chapters = defaultdict(list)
    for key, records in entries.items():
        m = _KEY_RE.match(key)
        if m and m.group(3) and len(records) == 1:
            chapters[(m.group(1), int(m.group(2)))].append((int(m.group(3)), key))
    shared = 0
    for (book, chapter), verses in chapters.items():
        verses.sort()
        prev_digest = prev_file = None
        for verse, key in verses:
            record = entries[key][0]
            digest = _file_digest(record["file"])
            family = svg_registry.owner_of(book.replace("_", " "), chapter, verse)
            # A deliberate range file is never re-pointed at a copy: it is
            # the picture its verses were meant to share.
            from_range = bool(_RANGE_RE.match(Path(record["file"]).stem))
            if (digest is not None and digest == prev_digest
                    and not from_range
                    and not (family and family.replay_identical)):
                entries[key] = [dict(record, file=prev_file)]
            if entries[key][0]["file"] == prev_file:
                shared += 1  # this verse shows the previous verse's file
            prev_file = entries[key][0]["file"]
            prev_digest = digest
    return shared


def build_manifest():
    """Scan visuals/ and build the v2 manifest. Returns the entries dict."""
    entries = defaultdict(list)
    ranges = []  # (range stem, path, rel_path) from Book_c_v1-v2 files

    for path, rel_path, stem in _scan_files():
        if path.name.endswith(".still.svg"):
            continue  # a retired twin is never a key of its own; reported below
        if _RANGE_RE.match(stem):
            ranges.append((stem, path, rel_path))
            continue
        # Key by the exact stem ("Genesis_5_3"). Never also file a suffixed
        # name under the plain key: the plain lookup would then pick up
        # whichever file sorts first.
        entries[stem].append(_classify(path, rel_path, stem))

    # A range file supplies every WEB verse in its range, except a verse that
    # has a file of its own: the more specific file wins. Where two ranges
    # overlap, the one whose name sorts first wins (video_render.resolve_svg
    # picks the same one).
    filled_by = {}  # verse key -> the range stem that supplied it
    for stem, path, rel_path in sorted(ranges):
        r = _RANGE_RE.match(stem)
        lo, hi = int(r.group(3)), int(r.group(4))
        if lo > hi:
            print(f"[WARN] {rel_path}: verse range {lo}-{hi} is backwards "
                  f"- skipped")
            continue
        book, chapter = r.group(1), int(r.group(2))
        try:
            web_verses = set(passages.verse_numbers(book.replace("_", " "), chapter))
        except passages.PassageError:
            print(f"[WARN] {rel_path}: {book.replace('_', ' ')} {chapter} is "
                  f"not a WEB chapter - skipped")
            continue
        missing = [v for v in range(lo, hi + 1) if v not in web_verses]
        if missing:
            print(f"[WARN] {rel_path}: WEB has no verse(s) {missing} - "
                  f"those are left out")
        record = _classify(path, rel_path, stem)
        for verse in range(lo, hi + 1):
            if verse not in web_verses:
                continue
            key = f"{book}_{chapter}_{verse}"
            if key in filled_by:
                print(f"[WARN] {key} is in both {filled_by[key]}.svg and "
                      f"{stem}.svg - {filled_by[key]}.svg wins")
            elif key in entries:
                print(f"[WARN] {key} has its own file and is also inside "
                      f"{stem}.svg - its own file wins")
            else:
                entries[key].append(dict(record))
                filled_by[key] = stem

    for records in entries.values():
        records.sort(key=lambda r: r["file"])

    shared = _share_identical_runs(entries)
    if shared:
        print(f"[OK] {shared} verse(s) share the previous verse's picture "
              f"(range files and identical copies play once across the run)")

    retired = _retired_leftovers()
    if retired:
        print(f"[WARN] {len(retired)} retired variant file(s) under visuals/ "
              f"(translation-suffixed or .still.svg) - nothing serves them "
              f"(a stale backup copied back in?):")
        for rel in retired[:20]:
            print(f"  - {rel}")
        if len(retired) > 20:
            print(f"  ... and {len(retired) - 20} more")

    manifest = {"version": 2, "entries": dict(entries)}
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

    return dict(entries)


if __name__ == "__main__":
    entries = build_manifest()
    n_animated = sum(1 for recs in entries.values()
                     for r in recs if r["animated"])
    print(f"[OK] Written {len(entries)} verse keys to {MANIFEST_PATH} "
          f"(schema v2; {n_animated} animated file(s))")
    print("\nSample entries:")
    for key, recs in list(entries.items())[:3]:
        print(f"  {key}:")
        for r in recs[:2]:
            print(f"    - {r}")
        if len(recs) > 2:
            print(f"    ... and {len(recs) - 2} more")
