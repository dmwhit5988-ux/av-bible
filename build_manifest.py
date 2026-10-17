#!/usr/bin/env python3
"""Scan visuals/ and generate manifest.json — schema v2.

v2 keeps v1's keys (exact file stems: "Genesis_5_3" for a verse, or
"Genesis_5" for a whole-chapter graphic) but each entry is a list of per-file
records instead of bare paths, so readers can filter/present by metadata
without re-deriving it:

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

import json
import re
from pathlib import Path
from collections import defaultdict

import svg_registry
from svg_freeze import svg_is_animated

VISUALS_DIR = Path("visuals")
MANIFEST_PATH = VISUALS_DIR / "manifest.json"

# Extensions indexed: vector diagrams (.svg) and raster images. Text files
# (README, CREDITS) are documentation, not visuals.
IMAGE_EXTS = {".svg", ".webp", ".gif", ".png", ".jpg", ".jpeg"}

_KIND_BY_EXT = {
    ".png": "photo", ".jpg": "photo", ".jpeg": "photo",
}
_DEFAULT_KIND = "infographic"

_DATA_KIND_RE = re.compile(r'<svg\b[^>]*\bdata-kind="([^"]+)"')
# Verse-key shape after stripping a .mobile suffix: Book_ch or Book_ch_v,
# where Book may itself contain underscores (Song_of_Solomon).
_KEY_RE = re.compile(r"^(.+?)_(\d+)(?:_(\d+))?$")
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


def build_manifest():
    """Scan visuals/ and build the v2 manifest. Returns the entries dict."""
    entries = defaultdict(list)

    for path, rel_path, stem in _scan_files():
        if path.name.endswith(".still.svg"):
            continue  # a retired twin is never a key of its own; reported below
        # Key by the exact stem ("Genesis_5_3"). Never also file a suffixed
        # name under the plain key: the plain lookup would then pick up
        # whichever file sorts first.
        entries[stem].append(_classify(path, rel_path, stem))

    for records in entries.values():
        records.sort(key=lambda r: r["file"])

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
