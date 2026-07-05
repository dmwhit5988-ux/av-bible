"""Convert a full Bible XML file into the app's per-chapter JSON format.

Run once per translation to populate ``bibles/<CODE>/`` with one file per
chapter (``<Book>_<Chapter>.json``) in the exact shape ``passages.load_local``
reads. This keeps live XML parsing off the playback thread — the app only ever
reads small JSON files.

Supported input schemas (auto-detected from the root element):

- **Zefania**: ``<BIBLEBOOK>`` -> ``<CHAPTER>`` -> ``<VERS>``. Container-based.
- **USFX** (eBible.org): milestone markers ``<c id/>`` / ``<v id/>``...``<ve/>``
  with text flowing between them. ``<f>`` footnotes go to per-verse notes.
- **OSIS**: milestone markers ``<chapter sID/>`` / ``<verse sID/>``...
  ``<verse eID/>``. ``<note>`` elements go to per-verse notes.

For the milestone formats, anything outside a verse range (front matter,
section headings, psalm superscriptions) is ignored automatically.

Usage:
    python import_translation.py <bible.xml> <CODE> [--format auto]

Examples:
    python import_translation.py bibles/eng-bsb.usfx.xml BSB
    python import_translation.py bibles/eng-kjv.osis.xml KJV
"""

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

from books import BOOK_NAMES, CHAPTER_COUNTS
from config import BIBLES_DIR
# Reuse the exact cleaning the live bible-api.com path uses so notes and
# supplied-word handling stay consistent across sources.
from passages import _ANNOTATION, _SUPPLIED

# Zefania numbers books 1..66 in Protestant canonical order, matching
# BOOK_NAMES. bname is unreliable across files, so bnumber is preferred.
_NORMALIZE = re.compile(r"[^a-z0-9]")

# Sub-elements whose text must never be read aloud (study notes, cross refs).
_SKIP_TAGS = {"NOTE", "XREF"}


def _normalize(name: str) -> str:
    return _NORMALIZE.sub("", (name or "").lower())


_BOOK_BY_NORMALIZED = {_normalize(n): n for n in BOOK_NAMES}


def _verse_text(vers_el) -> str:
    """Collect a <VERS> element's readable text, skipping notes/cross-refs."""
    parts = []
    if vers_el.text:
        parts.append(vers_el.text)
    for child in vers_el:
        if child.tag.rpartition("}")[2].upper() not in _SKIP_TAGS:
            # itertext() picks up nested <STYLE>/<GRAM> readable content.
            parts.append("".join(child.itertext()))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def _clean(raw: str):
    """Match fetch_public: drop <..>/{..} headers, pull [supplied] into notes."""
    raw = _ANNOTATION.sub("", raw)
    verse_notes = [re.sub(r"\s+", " ", m).strip() for m in _SUPPLIED.findall(raw)]
    text = _SUPPLIED.sub(r"\1", raw)          # keep the words, drop the brackets
    text = re.sub(r"\s+", " ", text).strip()
    return text, [n for n in verse_notes if n]


def _resolve_book(bnumber: str, bname: str) -> str | None:
    """Map a Zefania book to the app's canonical name."""
    try:
        idx = int(bnumber) - 1
        if 0 <= idx < len(BOOK_NAMES):
            return BOOK_NAMES[idx]
    except (TypeError, ValueError):
        pass
    return _BOOK_BY_NORMALIZED.get(_normalize(bname))


def parse_zefania(xml_path: str) -> dict:
    """Return {book_name: {chapter_int: (verses, notes)}} from a Zefania file."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    out: dict = {}
    unknown = set()
    for book_el in root.iter():
        if book_el.tag.rpartition("}")[2].upper() != "BIBLEBOOK":
            continue
        book = _resolve_book(book_el.get("bnumber"), book_el.get("bname"))
        if not book:
            unknown.add(book_el.get("bname") or book_el.get("bnumber") or "?")
            continue
        for chap_el in book_el:
            if chap_el.tag.rpartition("}")[2].upper() != "CHAPTER":
                continue
            try:
                cnum = int(chap_el.get("cnumber"))
            except (TypeError, ValueError):
                continue
            verses, notes = [], []
            for vers_el in chap_el:
                if vers_el.tag.rpartition("}")[2].upper() != "VERS":
                    continue
                try:
                    vnum = int(vers_el.get("vnumber"))
                except (TypeError, ValueError):
                    continue
                text, vnotes = _clean(_verse_text(vers_el))
                if text:
                    verses.append((vnum, text))
                    notes.append(vnotes)
            if verses:
                out.setdefault(book, {})[cnum] = (verses, notes)
    if unknown:
        print(f"  note: skipped {len(unknown)} unrecognized book(s): "
              f"{', '.join(sorted(unknown))}")
    return out


# ---------------------------------------------------------------------------
# USFX / OSIS (milestone-marker formats)
# ---------------------------------------------------------------------------

def _tag(el) -> str:
    """Local tag name, namespace stripped."""
    return el.tag.rpartition("}")[2]


# Both sequences are the 66-book Protestant canon in order, so they zip
# straight onto books.py BOOK_NAMES. Codes not listed (USFX FRT front matter,
# OSIS apocrypha like Tob/Jdt/1Macc) are skipped and reported.
_USFM_CODES = ("GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR "
               "NEH EST JOB PSA PRO ECC SNG ISA JER LAM EZK DAN HOS JOL AMO "
               "OBA JON MIC NAM HAB ZEP HAG ZEC MAL MAT MRK LUK JHN ACT ROM "
               "1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM HEB JAS 1PE "
               "2PE 1JN 2JN 3JN JUD REV").split()
_OSIS_CODES = ("Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs "
               "1Chr 2Chr Ezra Neh Esth Job Ps Prov Eccl Song Isa Jer Lam "
               "Ezek Dan Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech "
               "Mal Matt Mark Luke John Acts Rom 1Cor 2Cor Gal Eph Phil Col "
               "1Thess 2Thess 1Tim 2Tim Titus Phlm Heb Jas 1Pet 2Pet 1John "
               "2John 3John Jude Rev").split()
USFM_TO_BOOK = dict(zip(_USFM_CODES, BOOK_NAMES))
OSIS_TO_BOOK = dict(zip(_OSIS_CODES, BOOK_NAMES))

# Inside a verse range these carry no spoken text: footnotes/cross-refs are
# captured separately; figures, alt verse numbers, headings etc. are dropped.
_USFX_NOTE_TAGS = {"f", "fe"}
_USFX_SKIP_TAGS = {"x", "fig", "va", "vp", "cl", "ca", "d", "s", "s1", "s2",
                   "id", "h", "toc", "ide", "rem", "sts"}
_OSIS_NOTE_TAGS = {"note"}
_OSIS_SKIP_TAGS = {"title", "figure", "catchWord", "rdg"}


class _VerseState:
    """Accumulates flowing text between milestone markers into chapters."""

    def __init__(self):
        self.chapters = {}          # ch -> (verses, notes) matching parse_zefania
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
        raw = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        # Same convention as the Zefania path: [bracketed] translator-supplied
        # words stay in the spoken text and are also collected as notes
        # (YLT uses these heavily, e.g. "Jehovah [is] my shepherd").
        supplied = [re.sub(r"\s+", " ", m).strip()
                    for m in _SUPPLIED.findall(raw)]
        text = _SUPPLIED.sub(r"\1", raw).strip()
        if text and self.ch:
            verses, notes = self.chapters.setdefault(self.ch, ([], []))
            verses.append((self.vnum, text))
            notes.append([n for n in supplied if n] + list(self.vnotes))
        self.vnum = None
        self.buf = []
        self.vnotes = []


def _first_int(*values):
    for v in values:
        m = re.search(r"\d+", v or "")
        if m:
            return int(m.group())
    return None


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


def _milestone_walk(el, st: _VerseState, handle) -> None:
    """Generic doc-order walk; `handle(child, st)` returns True to recurse."""
    for child in el:
        if handle(child, st):
            if child.text:
                st.text(child.text)
            _milestone_walk(child, st, handle)
        if child.tail:
            st.text(child.tail)


def _usfx_handle(child, st) -> bool:
    tag = _tag(child).lower()
    if tag == "c":
        n = _first_int(child.get("id"))
        if n:
            st.set_chapter(n)
    elif tag == "v":
        n = _first_int(child.get("id"))
        if n:
            st.start_verse(n)
    elif tag == "ve":
        st.close()
    elif tag in _USFX_NOTE_TAGS:
        # drop the <fr> verse-reference prefix, keep the note wording
        st.note(_inline_text(child, skip={"fr", "xo"}))
    elif tag in _USFX_SKIP_TAGS:
        pass
    else:
        return True  # ordinary content (p, q, w, add, wj...) — recurse
    return False


def _osis_handle(child, st) -> bool:
    tag = _tag(child)
    if tag == "chapter":
        if child.get("sID") or (child.get("osisID") and not child.get("eID")):
            n = _first_int(child.get("n"),
                           (child.get("osisID") or "").split(".")[-1])
            if n:
                st.set_chapter(n)
    elif tag == "verse":
        if child.get("sID"):
            n = _first_int(child.get("n"),
                           (child.get("osisID") or "").split(".")[-1])
            if n:
                st.start_verse(n)
        elif child.get("eID"):
            st.close()
    elif tag.lower() in _OSIS_NOTE_TAGS:
        st.note(_inline_text(child, skip={"reference"}))
    elif tag.lower() in _OSIS_SKIP_TAGS:
        pass
    else:
        return True  # p, lg, l, w, seg, transChange, q... — recurse
    return False


def parse_usfx(xml_path: str) -> dict:
    """Return {book: {ch: (verses, notes)}} from a USFX (eBible.org) file."""
    root = ET.parse(xml_path).getroot()
    out = {}
    unknown = set()
    for book_el in root:
        if _tag(book_el).lower() != "book":
            continue
        code = (book_el.get("id") or "").upper()
        book = USFM_TO_BOOK.get(code)
        if not book:
            if code != "FRT":  # front matter is expected, not worth a warning
                unknown.add(code or "?")
            continue
        st = _VerseState()
        _milestone_walk(book_el, st, _usfx_handle)
        st.close()
        if st.chapters:
            out[book] = st.chapters
    if unknown:
        print(f"  note: skipped {len(unknown)} unrecognized book(s): "
              f"{', '.join(sorted(unknown))}")
    return out


def parse_osis(xml_path: str) -> dict:
    """Return {book: {ch: (verses, notes)}} from an OSIS file."""
    root = ET.parse(xml_path).getroot()
    out = {}
    unknown = set()
    for div in root.iter():
        if _tag(div) != "div" or div.get("type") != "book":
            continue
        book = OSIS_TO_BOOK.get(div.get("osisID") or "")
        if not book:
            unknown.add(div.get("osisID") or "?")
            continue
        st = _VerseState()
        _milestone_walk(div, st, _osis_handle)
        st.close()
        if st.chapters:
            out[book] = st.chapters
    if unknown:
        print(f"  note: skipped {len(unknown)} non-canon book(s): "
              f"{', '.join(sorted(unknown))}")
    return out


PARSERS = {"zefania": parse_zefania, "usfx": parse_usfx, "osis": parse_osis}


def detect_format(xml_path: str) -> str:
    """Sniff the schema from the root element name."""
    for _, el in ET.iterparse(xml_path, events=("start",)):
        root_tag = _tag(el).lower()
        break
    if root_tag == "xmlbible":
        return "zefania"
    if root_tag in PARSERS:
        return root_tag
    raise SystemExit(f"error: unrecognized root element <{root_tag}> — "
                     f"expected XMLBIBLE (zefania), usfx, or osis")


def write_passages(parsed: dict, code: str) -> int:
    """Write one JSON per chapter into bibles/<CODE>/. Returns files written."""
    out_dir = os.path.join(BIBLES_DIR, code)
    os.makedirs(out_dir, exist_ok=True)
    written = 0
    for book, chapters in parsed.items():
        for cnum, (verses, notes) in chapters.items():
            payload = {
                "book": book,
                "chapter": cnum,
                "canonical": f"{book} {cnum}",
                "translation": code,
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
    ap.add_argument("xml_path", help="path to the source Bible XML file")
    ap.add_argument("code", help="translation code, e.g. BSB")
    ap.add_argument("--format", default="auto",
                    choices=["auto", "zefania", "usfx", "osis"],
                    help="input XML schema (default: sniff the root element)")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.xml_path):
        print(f"error: no such file: {args.xml_path}", file=sys.stderr)
        return 2

    fmt = detect_format(args.xml_path) if args.format == "auto" else args.format
    code = args.code.upper()
    print(f"Parsing {args.xml_path} ({fmt}) -> {code} ...")
    parsed = PARSERS[fmt](args.xml_path)
    if not parsed:
        print(f"error: no books parsed — is this really a {fmt} file?",
              file=sys.stderr)
        return 1
    report_coverage(parsed)
    count = write_passages(parsed, code)
    print(f"Wrote {count} chapter file(s) to "
          f"{os.path.join(BIBLES_DIR, code)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
