#!/usr/bin/env python3
"""Scan visuals/ and generate manifest.json mapping verse keys to image paths."""

import json
import os
from pathlib import Path
from collections import defaultdict

VISUALS_DIR = Path("visuals")
MANIFEST_PATH = VISUALS_DIR / "manifest.json"

# Extensions supported: images plus text files (.txt/.rtf), which the app
# renders as an on-stage text panel styled like the translator notes.
IMAGE_EXTS = {".webp", ".gif", ".png", ".jpg", ".jpeg", ".txt", ".rtf"}


def build_manifest():
    """Scan visuals/ and build a manifest of all image files."""
    manifest = defaultdict(list)

    # Scan nested layout: visuals/<Book>/<chapter>/<Book>_<ch>_<v>[.CODE].ext
    for book_dir in VISUALS_DIR.glob("*"):
        if not book_dir.is_dir() or book_dir.name.startswith("."):
            continue

        for chapter_dir in book_dir.glob("*"):
            if not chapter_dir.is_dir() or chapter_dir.name.startswith("."):
                continue

            for img_file in chapter_dir.glob("*"):
                if img_file.suffix.lower() in IMAGE_EXTS:
                    # Relative path from visuals/ root
                    rel_path = img_file.relative_to(VISUALS_DIR).as_posix()

                    # Key by the exact stem: "Genesis_5_3.KJV" for a
                    # translation-suffixed file, "Genesis_5_3" for a plain
                    # one. Do NOT also add suffixed files under the plain
                    # key — that would make the generic (no-translation)
                    # lookup randomly pick up another translation's file.
                    stem = img_file.stem  # e.g. "Genesis_5_3.KJV" or "Genesis_5_3"
                    manifest[stem].append(rel_path)

    # Scan flat layout: visuals/<Book>_<ch>[_<v>][.CODE].ext and visuals/default.*
    for img_file in VISUALS_DIR.glob("*"):
        if img_file.is_file() and img_file.suffix.lower() in IMAGE_EXTS:
            rel_path = img_file.name

            stem = img_file.stem  # e.g. "Genesis_5_3.KJV", "Genesis_5_3", "default"

            # Only add if not already indexed from the nested layout
            if stem not in manifest or rel_path not in manifest[stem]:
                manifest[stem].append(rel_path)

    # Sort file lists for consistency
    for key in manifest:
        manifest[key].sort()

    # Write manifest
    with open(MANIFEST_PATH, "w") as f:
        json.dump(dict(manifest), f, indent=2)

    return manifest


if __name__ == "__main__":
    manifest = build_manifest()
    print(f"[OK] Written {len(manifest)} verse keys to {MANIFEST_PATH}")
    print(f"\nSample entries:")

    # Show a few samples
    samples = list(manifest.items())[:5]
    for key, files in samples:
        print(f"  {key}:")
        for f in files[:2]:  # Show first 2 files per key
            print(f"    - {f}")
        if len(files) > 2:
            print(f"    ... and {len(files) - 2} more")
