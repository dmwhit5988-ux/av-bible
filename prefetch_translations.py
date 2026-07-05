"""Download public-domain API translations into permanent local copies.

The six bible-api.com translations (KJV, WEB, ASV, BBE, DARBY, DRA) are public
domain, so we can bundle them for offline use. This walks the 66-book canon,
fetches each chapter through the existing ``passages.fetch_public`` (identical
parsing + translator-note extraction), and writes it into ``bibles/<CODE>/`` in
the same JSON shape ``load_local`` reads. Once populated, ``fetch_passage``
serves these from disk with no network and no rate limit.

It is **resumable** (skips chapters already written) and **rate-limit aware**
(bible-api.com allows ~15 requests / 30s; default 2.2s spacing stays under that,
with exponential backoff on 429). A full six-translation run is long (~40 min
each) but only has to happen once — run it in the background.

Usage:
    python prefetch_translations.py                 # all six, full canon
    python prefetch_translations.py WEB KJV         # just these codes
    python prefetch_translations.py WEB --books "Obadiah,Jude"   # a subset
"""

import argparse
import json
import os
import sys
import time

from books import BOOK_NAMES, CHAPTER_COUNTS
import passages
from passages import (TRANSLATION_SOURCES, PassageError, fetch_public,
                      polite_throttle, _local_path)

# Codes that come from bible-api.com and are safe to bundle (public domain).
API_CODES = [code for code, source in TRANSLATION_SOURCES.items()
             if source == "api"]

THROTTLE_SECONDS = 2.2      # under the ~15 req / 30s limit
MAX_RETRIES = 5


def _write_local(passage) -> None:
    path = _local_path(passage.translation, passage.book, passage.chapter)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".part"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(passage.__dict__, f)
    os.replace(tmp, path)


def prefetch_chapter(code: str, book: str, chapter: int) -> str:
    """Fetch one chapter with backoff. Returns 'written' | 'skip' | 'fail'."""
    if os.path.exists(_local_path(code, book, chapter)):
        return "skip"
    delay = THROTTLE_SECONDS
    for attempt in range(1, MAX_RETRIES + 1):
        polite_throttle(THROTTLE_SECONDS)
        try:
            passage = fetch_public(code, book, chapter)
            _write_local(passage)
            return "written"
        except PassageError as e:
            msg = str(e).lower()
            if "rate limit" in msg and attempt < MAX_RETRIES:
                delay = min(delay * 2, 60)
                print(f"    rate-limited on {book} {chapter}; "
                      f"waiting {delay:.0f}s (attempt {attempt})")
                time.sleep(delay)
                continue
            print(f"    FAILED {code} {book} {chapter}: {e}")
            return "fail"
    return "fail"


def prefetch_code(code: str, books: list) -> None:
    total = sum(CHAPTER_COUNTS[b] for b in books)
    print(f"[{code}] {total} chapter(s) across {len(books)} book(s)")
    written = skipped = failed = 0
    for book in books:
        for chapter in range(1, CHAPTER_COUNTS[book] + 1):
            result = prefetch_chapter(code, book, chapter)
            if result == "written":
                written += 1
            elif result == "skip":
                skipped += 1
            else:
                failed += 1
        done = written + skipped + failed
        print(f"  {book:<16} done  (written {written}, "
              f"skipped {skipped}, failed {failed}, {done}/{total})")
    print(f"[{code}] complete: {written} written, {skipped} already present, "
          f"{failed} failed\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("codes", nargs="*", default=None,
                    help="translation codes (default: all public-domain API ones)")
    ap.add_argument("--books", default=None,
                    help="comma-separated subset of book names (default: all 66)")
    args = ap.parse_args(argv)

    codes = [c.upper() for c in args.codes] if args.codes else list(API_CODES)
    bad = [c for c in codes if c not in API_CODES]
    if bad:
        print(f"error: not public-domain API translations: {', '.join(bad)}\n"
              f"available: {', '.join(API_CODES)}", file=sys.stderr)
        return 2

    if args.books:
        books = [b.strip() for b in args.books.split(",") if b.strip()]
        unknown = [b for b in books if b not in CHAPTER_COUNTS]
        if unknown:
            print(f"error: unknown book(s): {', '.join(unknown)}", file=sys.stderr)
            return 2
    else:
        books = list(BOOK_NAMES)

    for code in codes:
        prefetch_code(code, books)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
