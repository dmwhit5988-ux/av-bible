"""Re-import the World English Bible from its eBible.org USFX source.

Turns ``bibles/eng-web.usfx.xml`` into ``bibles/WEB/<Book>_<Chapter>.json``,
one file per chapter, in the shape ``passages.load_chapter`` reads. This keeps
XML parsing off the playback thread -- the app only ever reads small JSON files.

USFX marks chapters and verses with milestones (``<c id/>``, ``<v id/>`` ...
``<ve/>``) and lets the text flow between them, so anything outside a verse
range (front matter, section headings, psalm superscriptions) is ignored
automatically. ``<f>`` footnotes are collected as per-verse notes.

Each file keeps its "translation" and "notes" fields. The loader ignores both,
but writing them means a re-import reproduces the committed files byte for byte.

Usage:
    python import_translation.py [xml_path] [--out DIR]

``--out`` defaults to bibles/WEB; point it at a temp dir to dry-run and diff.
"""

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

from books import BOOK_NAMES, CHAPTER_COUNTS
from config import BIBLES_DIR
from passages import TRANSLATION

SOURCE_XML = os.path.join(BIBLES_DIR, "eng-web.usfx.xml")
OUT_DIR = os.path.join(BIBLES_DIR, TRANSLATION)

# The 66-book Protestant canon in order, so it zips straight onto books.py
# BOOK_NAMES. Codes not listed (FRT front matter, the deuterocanon) are skipped.
_USFM_CODES = ("GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR "
               "NEH EST JOB PSA PRO ECC SNG ISA JER LAM EZK DAN HOS JOL AMO "
               "OBA JON MIC NAM HAB ZEP HAG ZEC MAL MAT MRK LUK JHN ACT ROM "
               "1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM HEB JAS 1PE "
               "2PE 1JN 2JN 3JN JUD REV").split()
USFM_TO_BOOK = dict(zip(_USFM_CODES, BOOK_NAMES))

# Inside a verse range these carry no spoken text: footnotes are captured
# separately; cross refs, figures, alt verse numbers, headings etc. are dropped.
_NOTE_TAGS = {"f", "fe"}
_SKIP_TAGS = {"x", "fig", "va", "vp", "cl", "ca", "d", "s", "s1", "s2",
              "id", "h", "toc", "ide", "rem", "sts"}


def _tag(el) -> str:
    """Local tag name, namespace stripped."""
    return el.tag.rpartition("}")[2]


def _number(value):
    m = re.search(r"\d+", value or "")
    return int(m.group()) if m else None


class _VerseState:
    """Accumulates flowing text between milestone markers into chapters."""

    def __init__(self):
        self.chapters = {}          # ch -> (verses, notes)
        self.ch = 0
        self.vnum = None
        self.buf = []
        self.vnotes = []

    def set_chapter(self, n: int):
        self.close()
        self.ch = n

    def start_verse(self, n: int):
        self.close()
        self.vnum = n

    def text(self, s: str):
        if self.vnum is not None and s:
            self.buf.append(s)

    def note(self, s: str):
        if self.vnum is not None and s:
            self.vnotes.append(s)

    def close(self):
        if self.vnum is None:
            return
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if text and self.ch:
            verses, notes = self.chapters.setdefault(self.ch, ([], []))
            verses.append((self.vnum, text))
            notes.append(list(self.vnotes))
        self.vnum = None
        self.buf = []
        self.vnotes = []


def _inline_text(el, skip: set) -> str:
    """Collect el's text in document order, dropping `skip` subtrees."""
    parts = []

    def walk(e):
        if e.text:
            parts.append(e.text)
        for c in e:
            if _tag(c).lower() not in skip:
                walk(c)
            if c.tail:
                parts.append(c.tail)

    walk(el)
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def _visit(child, st: _VerseState) -> bool:
    """Act on one element; True means it is ordinary content to recurse into."""
    tag = _tag(child).lower()
    if tag == "c":
        n = _number(child.get("id"))
        if n:
            st.set_chapter(n)
    elif tag == "v":
        n = _number(child.get("id"))
        if n:
            st.start_verse(n)
    elif tag == "ve":
        st.close()
    elif tag in _NOTE_TAGS:
        # drop the <fr> verse-reference prefix, keep the note wording
        st.note(_inline_text(child, skip={"fr", "xo"}))
    elif tag in _SKIP_TAGS:
        pass
    else:
        return True  # ordinary content (p, q, w, add, wj...)
    return False


def _walk(el, st: _VerseState) -> None:
    """Feed el's children to the verse state in document order."""
    for child in el:
        if _visit(child, st):
            if child.text:
                st.text(child.text)
            _walk(child, st)
        if child.tail:
            st.text(child.tail)


def parse_usfx(xml_path: str) -> dict:
    """Return {book: {ch: (verses, notes)}} for the 66 canonical books."""
    root = ET.parse(xml_path).getroot()
    out = {}
    skipped = set()
    for book_el in root:
        if _tag(book_el).lower() != "book":
            continue
        code = (book_el.get("id") or "").upper()
        book = USFM_TO_BOOK.get(code)
        if not book:
            if code != "FRT":  # front matter is expected, not worth a mention
                skipped.add(code or "?")
            continue
        st = _VerseState()
        _walk(book_el, st)
        st.close()
        if st.chapters:
            out[book] = st.chapters
    if skipped:
        print(f"  note: skipped {len(skipped)} book(s) outside the 66-book "
              f"canon: {', '.join(sorted(skipped))}")
    return out


def write_passages(parsed: dict, out_dir: str) -> int:
    """Write one JSON per chapter into out_dir. Returns files written."""
    os.makedirs(out_dir, exist_ok=True)
    written = 0
    for book, chapters in parsed.items():
        for cnum, (verses, notes) in chapters.items():
            payload = {
                "book": book,
                "chapter": cnum,
                "canonical": f"{book} {cnum}",
                "translation": TRANSLATION,
                "verses": verses,
                "notes": notes,
            }
            safe_book = book.replace(" ", "_")
            path = os.path.join(out_dir, f"{safe_book}_{cnum}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f)
            written += 1
    return written


def report_coverage(parsed: dict) -> None:
    """Warn about any book/chapter in the 66-book canon that is missing."""
    missing_books = [b for b in BOOK_NAMES if b not in parsed]
    if missing_books:
        print(f"  WARNING: {len(missing_books)} book(s) absent: "
              f"{', '.join(missing_books)}")
    gaps = 0
    for book in BOOK_NAMES:
        chapters = parsed.get(book)
        if not chapters:
            continue  # whole book already reported above
        for cnum in range(1, CHAPTER_COUNTS[book] + 1):
            if cnum not in chapters:
                gaps += 1
                print(f"  WARNING: missing {book} {cnum}")
    if not missing_books and not gaps:
        print("  coverage: complete 66-book canon, no gaps.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("xml_path", nargs="?", default=SOURCE_XML,
                    help="the WEB USFX file (default: bibles/eng-web.usfx.xml)")
    ap.add_argument("--out", default=OUT_DIR,
                    help="output directory (default: bibles/WEB)")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.xml_path):
        print(f"error: no such file: {args.xml_path}", file=sys.stderr)
        return 2

    print(f"Parsing {args.xml_path} ...")
    parsed = parse_usfx(args.xml_path)
    if not parsed:
        print("error: no books parsed -- is this really a USFX file?",
              file=sys.stderr)
        return 1
    report_coverage(parsed)
    count = write_passages(parsed, args.out)
    print(f"Wrote {count} chapter file(s) to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
