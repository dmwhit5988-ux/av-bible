"""Coverage — the studio's per-chapter content dashboard / authoring backlog.

One tree over the whole canon (66 books -> 1,189 chapters) showing, per
chapter:

  Verses      chapter length (from the local bibles/WEB/*.json bundle —
              complete for the whole canon, no network)
  Visuals     verses with a visual / total, plus the kinds present
              (visuals/manifest.json schema v2)
  Audio       pre-rendered narration per translation, e.g. "WEB 31/31"
              (web/audio/manifest.json)
  Names       likely proper nouns not yet in pronunciations.json — an
              unreviewed-pronunciation count (pronunciation.scan_proper_nouns
              over the local WEB text)
  Candidate   this chapter's entry in INFOGRAPHIC_CANDIDATES.md (priority +
              types), so the gap list doubles as the what-to-build-next list

Everything is computed from local files in a background thread; no network.
The Filter box narrows the tree to the interesting rows ("candidate gaps"
= flagged in the catalog but no visuals yet).

    python coverage_studio.py
"""

import json
import os
import queue
import re
import threading
import tkinter as tk
from tkinter import ttk

import books
import pronunciation

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
BIBLES_WEB = os.path.join(REPO_ROOT, "bibles", "WEB")
VISUALS_MANIFEST = os.path.join(REPO_ROOT, "visuals", "manifest.json")
AUDIO_MANIFEST = os.path.join(REPO_ROOT, "web", "audio", "manifest.json")
CANDIDATES_MD = os.path.join(REPO_ROOT, "INFOGRAPHIC_CANDIDATES.md")

_VERSE_KEY_RE = re.compile(r"^(.+?)_(\d+)_(\d+)$")
# Chapter tokens inside a candidate label (book name already stripped):
# "12–25" -> range, "3:1–8" -> chapter 3 only, "5, 8, 10" -> three chapters.
_CHAPTER_TOKEN_RE = re.compile(r"(\d+)(?::[\d–—-]+)?"
                               r"(?:\s*[–—-]\s*(\d+))?")
_TYPE_EMOJI = "🗺️⏳🌳🏛️🔄📊🔢💡"

FILTERS = ["All chapters", "Has content", "Candidate gaps (no visuals)",
           "Unreviewed names"]


# ---------------------------------------------------------------------------
# INFOGRAPHIC_CANDIDATES.md parsing
# ---------------------------------------------------------------------------

def _parse_candidates():
    """{book: {chapter: (priority, types, label)}} from the catalog's
    "- **<Book> <chapters>** — ..." entries under each "### <Book>" heading.
    Only the by-book body sections count (the Navigation block's headings
    aren't book names). Entries without a chapter number (book-level notes)
    are skipped. Overlapping entries keep the higher priority."""
    try:
        with open(CANDIDATES_MD, encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return {}
    rank = {"High": 0, "Med": 1, "Low": 2}
    out = {}
    book = None
    for line in lines:
        m = re.match(r"^### (.+?)\s*$", line)
        if m:
            book = m.group(1) if m.group(1) in books.BOOK_NAMES else None
            continue
        if book is None:
            continue
        m = re.match(r"^- \*\*(.+?)\*\*\s*[—-]\s*(.*)$", line)
        if not m:
            continue
        label, rest = m.group(1), m.group(2)
        prio = next((p for p in ("High", "Med", "Low") if p in rest), None)
        types = "".join(ch for ch in rest if ch in _TYPE_EMOJI)
        # Strip the book name, then cut at any *other* book name so a
        # cross-book span ("1 Kings 12 – 2 Kings 17") only claims chapters
        # in this section's book.
        span = label.replace(book, "", 1)
        cut = min((i for i in (span.find(b) for b in books.BOOK_NAMES
                               if b != book) if i >= 0), default=-1)
        if cut >= 0:
            span = span[:cut]
        chapters = set()
        for tok in _CHAPTER_TOKEN_RE.finditer(span):
            lo = int(tok.group(1))
            hi = int(tok.group(2)) if tok.group(2) else lo
            if hi < lo:  # mangled cross-book leftovers — take lo only
                hi = lo
            chapters.update(range(lo, min(hi, books.chapters_in(book)) + 1))
        for ch in chapters:
            if 1 <= ch <= books.chapters_in(book):
                cur = out.setdefault(book, {}).get(ch)
                if cur is None or rank.get(prio, 3) < rank.get(cur[0], 3):
                    out.setdefault(book, {})[ch] = (prio, types, label)
    return out


# ---------------------------------------------------------------------------
# Coverage scan (background thread; local files only)
# ---------------------------------------------------------------------------

def _scan_visuals():
    """{book: {chapter: (covered_verse_set, kinds_set)}} from manifest v2."""
    try:
        with open(VISUALS_MANIFEST, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}
    entries = data.get("entries", data)
    out = {}
    for key, records in entries.items():
        m = _VERSE_KEY_RE.match(key.split(".", 1)[0])
        if not m:
            continue
        book = m.group(1).replace("_", " ")
        ch, verse = int(m.group(2)), int(m.group(3))
        verses, kinds = out.setdefault(book, {}).setdefault(ch, (set(), set()))
        verses.add(verse)
        for r in records:
            kind = r.get("kind") if isinstance(r, dict) else None
            if kind:
                kinds.add(kind)
    return out


def _scan_audio():
    """{book: {chapter: {translation: verse_count}}}."""
    try:
        with open(AUDIO_MANIFEST, encoding="utf-8") as f:
            manifest = json.load(f)
    except (OSError, ValueError):
        return {}
    out = {}
    for key in manifest:
        base, _, code = key.rpartition(".")
        m = _VERSE_KEY_RE.match(base)
        if not m:
            continue
        book = m.group(1).replace("_", " ")
        ch = int(m.group(2))
        per = out.setdefault(book, {}).setdefault(ch, {})
        per[code] = per.get(code, 0) + 1
    return out


def scan_coverage(on_book=None, on_names=None):
    """Full canon scan in two passes. Returns {book: {chapter: row_dict}}.

    Pass 1 (fast, ~1s): verse totals + visuals + audio + candidates; calls
    on_book(book, chapters_dict) per book so a UI fills in immediately.
    Pass 2 (the proper-noun sweep is regex-heavy, ~30s canon-wide): fills
    each row's "unreviewed" count and calls on_names(book, {ch: count}).
    row_dict keys: verses, vis_count, kinds, audio (dict), unreviewed
    (int|None while pending), candidate ((prio, types, label)|None)."""
    visuals = _scan_visuals()
    audio = _scan_audio()
    candidates = _parse_candidates()
    known = pronunciation.load(force=True)

    result = {}
    verse_texts = {}  # (book, ch) -> verses, reused by pass 2
    for book in books.BOOK_NAMES:
        chapters = {}
        safe = book.replace(" ", "_")
        for ch in range(1, books.chapters_in(book) + 1):
            row = {"verses": None, "vis_count": 0, "kinds": set(),
                   "audio": audio.get(book, {}).get(ch, {}),
                   "unreviewed": None,
                   "candidate": candidates.get(book, {}).get(ch)}
            vis = visuals.get(book, {}).get(ch)
            if vis:
                row["vis_count"], row["kinds"] = len(vis[0]), vis[1]
            try:
                with open(os.path.join(BIBLES_WEB, f"{safe}_{ch}.json"),
                          encoding="utf-8") as f:
                    verses = json.load(f).get("verses", [])
                row["verses"] = len(verses)
                verse_texts[(book, ch)] = verses
            except (OSError, ValueError):
                pass  # chapter text missing locally — leave counts unknown
            chapters[ch] = row
        result[book] = chapters
        if on_book:
            on_book(book, chapters)

    for book in books.BOOK_NAMES:
        counts = {}
        for ch, row in result[book].items():
            verses = verse_texts.pop((book, ch), None)
            if verses is None:
                continue
            found = pronunciation.scan_proper_nouns(verses, known=known)
            row["unreviewed"] = sum(1 for name, _ in found
                                    if name not in known)
            counts[ch] = row["unreviewed"]
        if on_names:
            on_names(book, counts)
    return result


# ---------------------------------------------------------------------------
# Row formatting
# ---------------------------------------------------------------------------

def _fmt_chapter(row):
    total = row["verses"]
    vis = ""
    if row["vis_count"]:
        vis = (f"{row['vis_count']}/{total}" if total else str(row["vis_count"]))
        if row["kinds"]:
            vis += "  " + "+".join(sorted(row["kinds"]))
    aud = " · ".join(
        f"{code} {n}/{total}" if total else f"{code} {n}"
        for code, n in sorted(row["audio"].items()))
    names = "" if not row["unreviewed"] else str(row["unreviewed"])
    cand = ""
    if row["candidate"]:
        prio, types, _ = row["candidate"]
        built = "✅" if row["vis_count"] else "🆕"
        cand = " ".join(x for x in (built, prio, types) if x)
    return (total if total is not None else "", vis, aud, names, cand)


def _fmt_book(chapters):
    n = len(chapters)
    vis_ch = sum(1 for r in chapters.values() if r["vis_count"])
    aud_ch = sum(1 for r in chapters.values() if r["audio"])
    unrev = sum(r["unreviewed"] or 0 for r in chapters.values())
    # Count distinct catalog ENTRIES still to build, not chapters — a
    # "Genesis 12–25" map is one candidate, not fourteen. An entry counts
    # as built once any of its chapters has a visual.
    built_labels, open_labels = set(), {}
    for r in chapters.values():
        if not r["candidate"]:
            continue
        prio, _, label = r["candidate"]
        if r["vis_count"]:
            built_labels.add(label)
        else:
            open_labels[label] = prio
    todo = {lbl: p for lbl, p in open_labels.items()
            if lbl not in built_labels}
    high = sum(1 for p in todo.values() if p == "High")
    return (
        f"{n} ch",
        f"{vis_ch}/{n} ch" if vis_ch else "",
        f"{aud_ch} ch" if aud_ch else "",
        str(unrev) if unrev else "",
        (f"{len(todo)} to build" + (f" ({high} High)" if high else ""))
        if todo else "")


def _row_matches(row, filt):
    if filt == "Has content":
        return bool(row["vis_count"] or row["audio"])
    if filt == "Candidate gaps (no visuals)":
        return bool(row["candidate"] and not row["vis_count"])
    if filt == "Unreviewed names":
        return bool(row["unreviewed"])
    return True


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

class App:
    def __init__(self, root, goto=None):
        """goto(book, chapter), if given, points the main reader at a row
        (the dashboard is the backlog; the reader/studios do the work)."""
        self.root = root
        self.goto = goto
        self.events: queue.Queue = queue.Queue()
        self.data = {}  # book -> {chapter: row}
        self.busy = False

        root.title("Coverage")
        root.geometry("900x620")
        root.minsize(760, 480)

        self._build_ui()
        self._poll_events()
        self.rescan()

    def _build_ui(self):
        bar = ttk.Frame(self.root, padding=(10, 8))
        bar.pack(fill="x")
        ttk.Label(bar, text="Filter:").pack(side="left")
        self.filter_var = tk.StringVar(value=FILTERS[0])
        cb = ttk.Combobox(bar, textvariable=self.filter_var, width=28,
                          state="readonly", values=FILTERS)
        cb.pack(side="left", padx=(4, 10))
        cb.bind("<<ComboboxSelected>>", lambda e: self._rebuild_tree())
        self.rescan_btn = ttk.Button(bar, text="Rescan", command=self.rescan)
        self.rescan_btn.pack(side="left")
        if self.goto:
            ttk.Button(bar, text="Go to chapter in reader",
                       command=self._goto_selected).pack(side="left",
                                                         padx=(6, 0))

        cols = ("verses", "visuals", "audio", "names", "candidate")
        self.tree = ttk.Treeview(self.root, columns=cols, selectmode="browse")
        headings = {"#0": ("Book / chapter", 190), "verses": ("Verses", 60),
                    "visuals": ("Visuals", 150), "audio": ("Audio", 170),
                    "names": ("Unreviewed names", 110),
                    "candidate": ("Candidate", 170)}
        for col, (text, width) in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width,
                             anchor="w" if col in ("#0", "visuals", "audio",
                                                   "candidate") else "center")
        scroll = ttk.Scrollbar(self.root, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y", padx=(0, 10), pady=(0, 8))
        self.tree.pack(fill="both", expand=True, padx=(10, 0), pady=(0, 8))
        self.tree.bind("<Double-1>", lambda e: self._goto_selected())

        self.status_var = tk.StringVar(value="Scanning…")
        ttk.Label(self.root, textvariable=self.status_var,
                  padding=(10, 4)).pack(anchor="w")

    # ----- scan ------------------------------------------------------------
    def rescan(self):
        if self.busy:
            return
        self.busy = True
        self.rescan_btn.configure(state="disabled")
        self.data = {}
        self.status_var.set("Scanning local manifests and text…")
        threading.Thread(target=self._scan_worker, daemon=True).start()

    def _scan_worker(self):
        try:
            scan_coverage(
                on_book=lambda b, chs: self.events.put(("book", b, chs)),
                on_names=lambda b, cts: self.events.put(("names", b, cts)))
            self.events.put(("scan_done", None))
        except Exception as e:
            self.events.put(("scan_done", str(e)))

    # ----- tree ------------------------------------------------------------
    def _rebuild_tree(self):
        self.tree.delete(*self.tree.get_children())
        for book in books.BOOK_NAMES:
            chapters = self.data.get(book)
            if chapters:
                self._insert_book(book, chapters)

    def _insert_book(self, book, chapters):
        filt = self.filter_var.get()
        rows = {ch: r for ch, r in chapters.items() if _row_matches(r, filt)}
        if not rows:
            return
        node = self.tree.insert("", "end", iid=book, text=book,
                                values=_fmt_book(chapters),
                                open=(filt != FILTERS[0]))
        for ch in sorted(rows):
            self.tree.insert(node, "end", iid=f"{book}|{ch}",
                             text=f"{book} {ch}",
                             values=_fmt_chapter(rows[ch]))

    def _goto_selected(self):
        if not self.goto:
            return
        sel = self.tree.selection()
        if not sel or "|" not in sel[0]:
            return
        book, ch = sel[0].rsplit("|", 1)
        self.goto(book, int(ch))

    # ----- event pump ------------------------------------------------------
    def _poll_events(self):
        try:
            while True:
                event = self.events.get_nowait()
                self._handle_event(event)
        except queue.Empty:
            pass
        if self.root.winfo_exists():
            self.root.after(100, self._poll_events)

    def _handle_event(self, event):
        kind = event[0]
        if kind == "book":
            _, book, chapters = event
            self.data[book] = chapters
            self._insert_book(book, chapters)
            self.status_var.set(f"Scanning… {book}")
        elif kind == "names":
            _, book, counts = event
            # Pass 2: update the names column in place. self.data rows were
            # already mutated by the worker (same dicts); refresh visible
            # tree cells for this book.
            for ch, count in counts.items():
                iid = f"{book}|{ch}"
                if count and self.tree.exists(iid):
                    self.tree.set(iid, "names", str(count))
            if self.tree.exists(book):
                self.tree.item(book, values=_fmt_book(self.data[book]))
            self.status_var.set(f"Scanning proper nouns… {book}")
        elif kind == "scan_done":
            self.busy = False
            self.rescan_btn.configure(state="normal")
            err = event[1]
            if err:
                self.status_var.set(f"Scan failed: {err}")
                return
            if self.filter_var.get() != FILTERS[0]:
                self._rebuild_tree()  # filters can now see the name counts
            vis_ch = sum(1 for chs in self.data.values()
                         for r in chs.values() if r["vis_count"])
            aud_ch = sum(1 for chs in self.data.values()
                         for r in chs.values() if r["audio"])
            todo = set()
            for book, chs in self.data.items():
                built = {r["candidate"][2] for r in chs.values()
                         if r["candidate"] and r["vis_count"]}
                todo |= {(book, r["candidate"][2]) for r in chs.values()
                         if r["candidate"] and not r["vis_count"]
                         and r["candidate"][2] not in built}
            unrev = sum(r["unreviewed"] or 0 for chs in self.data.values()
                        for r in chs.values())
            self.status_var.set(
                f"{vis_ch} chapter(s) with visuals · {aud_ch} with audio · "
                f"{len(todo)} candidate infographic(s) to build · "
                f"{unrev} unreviewed name occurrence(s) canon-wide")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
