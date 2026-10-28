"""Verse references as the data modules write them, read into verses.

The family tree's boxes carry refs written for the eye ("Gen 11:29,
22:20-23", "2 Kgs 8:18, 26, 2 Chr 22:10-12", "1 Sam 1-4", "7:19; Num
26:32"). A reference page needs them as verses it can link to, so
`parse()` reads one such string into `Ref`s:

- a book named in full or by the short forms in ABBREV, which then carries
  on to the parts after it;
- a bare "c:v" or "c" with no book takes the caller's default book (the
  tree's own 1 Chronicles refs are written "2:3");
- a bare number after a "c:v" is another verse of that chapter ("Ruth 1:2,
  20");
- a range ends at a verse ("22:20-23"), at a chapter and verse
  ("29:16-30:21") or, for whole chapters, at a chapter ("1 Sam 1-4");
- a range across two books ("1 Kgs 12 - 2 Kgs 17") is read as its two ends;
- anything after " — " is a remark, not a reference.

Every verse is checked against WEB's own versification
(passages.verse_numbers), and a ref that names a verse WEB doesn't have
raises: a link to a verse that isn't there is a broken link on the site.
"""

import re
from typing import NamedTuple, Optional

from books import BOOK_NAMES, chapters_in
from passages import verse_numbers

# Short forms, as the data modules write them. Full names (BOOK_NAMES) are
# accepted too.
ABBREV = {
    "Gen": "Genesis", "Ex": "Exodus", "Exod": "Exodus", "Lev": "Leviticus",
    "Num": "Numbers", "Deut": "Deuteronomy", "Josh": "Joshua",
    "Judg": "Judges", "1 Sam": "1 Samuel", "2 Sam": "2 Samuel",
    "1 Kgs": "1 Kings", "2 Kgs": "2 Kings", "1 Chr": "1 Chronicles",
    "2 Chr": "2 Chronicles", "Neh": "Nehemiah", "Est": "Esther",
    "Esth": "Esther", "Ps": "Psalms", "Psa": "Psalms", "Prov": "Proverbs",
    "Eccl": "Ecclesiastes", "Song": "Song of Solomon", "Isa": "Isaiah",
    "Jer": "Jeremiah", "Lam": "Lamentations", "Ezek": "Ezekiel",
    "Dan": "Daniel", "Hos": "Hosea", "Obad": "Obadiah", "Mic": "Micah",
    "Nah": "Nahum", "Hab": "Habakkuk", "Zeph": "Zephaniah", "Hag": "Haggai",
    "Zech": "Zechariah", "Mal": "Malachi", "Matt": "Matthew", "Mk": "Mark",
    "Lk": "Luke", "Jn": "John", "Rom": "Romans", "1 Cor": "1 Corinthians",
    "2 Cor": "2 Corinthians", "Gal": "Galatians", "Eph": "Ephesians",
    "Phil": "Philippians", "Col": "Colossians",
    "1 Thess": "1 Thessalonians", "2 Thess": "2 Thessalonians",
    "1 Tim": "1 Timothy", "2 Tim": "2 Timothy", "Phlm": "Philemon",
    "Heb": "Hebrews", "Jas": "James", "1 Pet": "1 Peter", "2 Pet": "2 Peter",
    "Rev": "Revelation",
}
_NAMES = {**{b: b for b in BOOK_NAMES}, **ABBREV}
# Longest first, so "1 Chr" is tried before "1" could be read as a chapter
# and "Judges" before "Jude".
_BOOK_RE = "|".join(re.escape(b) for b in sorted(_NAMES, key=len, reverse=True))
_PART = re.compile(
    rf"^(?:(?P<book>{_BOOK_RE})\.?\s+)?"
    r"(?P<c1>\d+)(?::(?P<v1>\d+))?"
    r"(?:\s*[-–]\s*"
    rf"(?:(?P<book2>{_BOOK_RE})\.?\s+)?"
    r"(?P<a>\d+)(?::(?P<b>\d+))?)?$")


class Ref(NamedTuple):
    """One reference: a verse, a verse range, a chapter or a chapter range.
    `v1` is None for a whole chapter; `c2`/`v2` are None for a single one."""
    book: str
    c1: int
    v1: Optional[int] = None
    c2: Optional[int] = None
    v2: Optional[int] = None

    def first(self):
        """(chapter, verse) a link to this ref opens at."""
        return self.c1, self.v1 if self.v1 is not None else \
            verse_numbers(self.book, self.c1)[0]

    def verses(self):
        """Every (book, chapter, verse) the ref covers, in order."""
        c2 = self.c2 if self.c2 is not None else self.c1
        out = []
        for c in range(self.c1, c2 + 1):
            for v in verse_numbers(self.book, c):
                if c == self.c1 and self.v1 is not None and v < self.v1:
                    continue
                last = self.v2 if self.v2 is not None else (
                    self.v1 if self.c2 is None else None)
                if c == c2 and last is not None and v > last:
                    continue
                out.append((self.book, c, v))
        return out


def parse(text, default_book):
    """-> [Ref] for one ref string, every verse checked against WEB."""
    text = text.split(" — ")[0].strip()
    refs = []
    book, chapter, had_verse = default_book, None, False
    for raw in re.split(r"\s*[,;]\s*", text):
        if not raw:
            continue
        m = _PART.match(raw)
        if not m:
            raise ValueError(f"can't read {raw!r} in ref {text!r}")
        if m["book"]:
            book, chapter, had_verse = _NAMES[m["book"]], None, False
        c1, v1 = int(m["c1"]), m["v1"] and int(m["v1"])
        a, b = m["a"] and int(m["a"]), m["b"] and int(m["b"])
        if m["book2"] and _NAMES[m["book2"]] != book:
            # a range across books: read as its two ends
            refs.append(_check(Ref(book, c1, v1)))
            book, chapter = _NAMES[m["book2"]], a
            refs.append(_check(Ref(book, a, b)))
            had_verse = b is not None
            continue
        if v1 is None and not m["book"] and had_verse and chapter is not None:
            # "Ruth 1:2, 20": a bare number after c:v is a verse
            ref = Ref(book, chapter, c1, None, a) if a is not None \
                else Ref(book, chapter, c1)
        elif v1 is None:
            ref = Ref(book, c1, None, a)
        elif b is not None:
            ref = Ref(book, c1, v1, a, b)
        else:
            ref = Ref(book, c1, v1, None, a)
        refs.append(_check(ref))
        chapter = ref.c2 if ref.c2 is not None and ref.v2 is not None \
            else ref.c1
        had_verse = ref.v1 is not None
    return refs


def _check(ref):
    if ref.book not in BOOK_NAMES:
        raise ValueError(f"no book {ref.book!r}")
    for c in (ref.c1, ref.c2):
        if c is not None and not 1 <= c <= chapters_in(ref.book):
            raise ValueError(f"{ref.book} has no chapter {c}")
    c2 = ref.c2 if ref.c2 is not None else ref.c1
    if c2 < ref.c1:
        raise ValueError(f"{ref} runs backwards")
    for c, v in ((ref.c1, ref.v1), (c2, ref.v2)):
        if v is not None and v not in verse_numbers(ref.book, c):
            raise ValueError(f"WEB has no {ref.book} {c}:{v}")
    if ref.c2 is None and ref.v1 is not None and ref.v2 is not None \
            and ref.v2 < ref.v1:
        raise ValueError(f"{ref} runs backwards")
    return ref
