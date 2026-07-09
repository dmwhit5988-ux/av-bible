"""Pronunciation Studio -- a local GUI to review and tune proper-noun pronunciations.

Pick a book + chapter and the tool lists every proper noun it finds, marks which
are already customized, and lets you:

  * hear the name as the neural voice says it now  (▶ Name)
  * type your own "Say it" spelling and hear it     (▶ Say / Enter)
  * tick "Custom" when a name needs the override
  * Save -> writes pronunciations.json AND PRONUNCIATIONS.md

Names are keyed by spelling, so the same name across chapters is one shared
entry: tune "Nahor" in Genesis 11 and it's already tuned when it turns up in
Genesis 22. Preview uses the same edge-tts voice the web/desktop audio uses, so
what you hear is what will be rendered.

    python pronunciation_tool.py
"""

import copy
import glob
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import books
import generate_showcase_audio as showcase
import pronunciation
import tts_engine
from audio_player import AudioPlayer
from passages import fetch_passage, PassageError

RATE = 0
TRANSLATION = "WEB"  # the text the pre-rendered showcase audio narrates


class Row:
    __slots__ = ("name", "occ", "default_ref", "say_var", "override_var", "status",
                 "orig_say", "orig_override")

    def __init__(self, name, occ, default_ref, say, override):
        self.name = name
        self.occ = occ
        self.default_ref = default_ref
        self.say_var = tk.StringVar(value=say)
        self.override_var = tk.BooleanVar(value=override)
        self.status = None  # the status label widget, set when built
        # Baseline at load time, so _commit_rows can tell whether this row's
        # spoken form actually changed (vs. just being redisplayed unedited).
        self.orig_say = say
        self.orig_override = override


class App:
    def __init__(self, root, start_book="Genesis", start_chapter=5):
        self.root = root
        self.player = AudioPlayer()
        self.names = copy.deepcopy(pronunciation.load(force=True))
        self.rows = []
        self.cur_book = None
        self.cur_ch = None
        self.cur_verses = []
        self.dirty = False
        self.busy = False
        # (book, chapter) pairs whose displayed names actually changed since
        # they were loaded -- cleared audio cache is scoped to these, not just
        # whatever chapter happens to be on screen when Save is clicked.
        self.dirty_chapters = set()

        root.title("Pronunciation Studio")
        root.geometry("980x680")
        root.minsize(820, 460)
        root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_top()
        self._build_list()
        self._build_bottom()

        # Open on the caller's current chapter (falls back to Genesis 5, which
        # has plenty of names, if none was given or the book is unrecognized).
        if start_book not in books.BOOK_NAMES:
            start_book, start_chapter = "Genesis", 5
        self.book_var.set(start_book)
        self._on_book_change()
        n = books.chapters_in(start_book)
        start_chapter = max(1, min(int(start_chapter or 1), n))
        self.ch_var.set(str(start_chapter))
        self.load_chapter()

    # ----- top controls -------------------------------------------------
    def _build_top(self):
        bar = ttk.Frame(self.root, padding=(10, 8))
        bar.pack(fill="x")

        ttk.Label(bar, text="Book:").pack(side="left")
        self.book_var = tk.StringVar()
        self.book_cb = ttk.Combobox(bar, textvariable=self.book_var, width=16,
                                    state="readonly", values=books.BOOK_NAMES)
        self.book_cb.pack(side="left", padx=(4, 10))
        self.book_cb.bind("<<ComboboxSelected>>", lambda e: self._on_book_change())

        ttk.Label(bar, text="Chapter:").pack(side="left")
        self.ch_var = tk.StringVar()
        self.ch_cb = ttk.Combobox(bar, textvariable=self.ch_var, width=5,
                                  state="readonly")
        self.ch_cb.pack(side="left", padx=(4, 10))

        ttk.Button(bar, text="Load chapter", command=self.load_chapter).pack(side="left")

        ttk.Label(bar, text="   Voice:").pack(side="left")
        self.voice_var = tk.StringVar(value="en-US-AndrewNeural")
        ttk.Combobox(bar, textvariable=self.voice_var, width=22, state="readonly",
                     values=tts_engine.EDGE_VOICES).pack(side="left", padx=(4, 10))

        self.filter_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(bar, text="Only new names", variable=self.filter_var,
                        command=self._build_rows).pack(side="left")

    # ----- scrollable list ---------------------------------------------
    def _build_list(self):
        outer = ttk.Frame(self.root)
        outer.pack(fill="both", expand=True, padx=10)

        self.canvas = tk.Canvas(outer, highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner = ttk.Frame(self.canvas)
        self._inner_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfigure(self._inner_id, width=e.width))
        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(int(-e.delta / 120), "units"))

    # ----- bottom bar ---------------------------------------------------
    def _build_bottom(self):
        bar = ttk.Frame(self.root, padding=(10, 8))
        bar.pack(fill="x")
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(bar, textvariable=self.status_var).pack(side="left")
        self.save_btn = ttk.Button(bar, text="Save  (JSON + .md)", command=self.save)
        self.save_btn.pack(side="right")
        legend = "●new  ●custom  ●default"
        ttk.Label(bar, text=legend, foreground="#888").pack(side="right", padx=12)

    # ----- data flow ----------------------------------------------------
    def _on_book_change(self):
        n = books.chapters_in(self.book_var.get())
        self.ch_cb.configure(values=[str(i) for i in range(1, n + 1)])
        if self.ch_var.get() not in self.ch_cb["values"]:
            self.ch_var.set("1")

    def load_chapter(self):
        self._commit_rows()  # keep edits from the chapter we're leaving
        book, ch = self.book_var.get(), int(self.ch_var.get() or 1)
        try:
            passage = fetch_passage("", book, ch, TRANSLATION)
        except PassageError as e:
            messagebox.showerror("Can't load chapter", str(e))
            return
        self.cur_book, self.cur_ch, self.cur_verses = book, ch, passage.verses
        self._build_rows()

    def _build_rows(self, keep_status=False):
        for w in self.inner.winfo_children():
            w.destroy()
        self.rows = []
        if not self.cur_verses:
            return

        found = pronunciation.scan_proper_nouns(self.cur_verses, known=set(self.names))
        hdr = ("", "Name", "Seen in", "IPA", "Custom", "Say it", "", "")
        for c, text in enumerate(hdr):
            ttk.Label(self.inner, text=text, font=("Segoe UI", 9, "bold")).grid(
                row=0, column=c, sticky="w", padx=4, pady=(2, 6))

        r = 1
        for name, occ in found:
            existing = self.names.get(name)
            if self.filter_var.get() and existing is not None:
                continue
            say = existing["say"] if existing else name
            override = bool(existing.get("override")) if existing else False
            default_ref = f"{self.cur_book} {self.cur_ch}:{occ[0]}"
            row = Row(name, occ, default_ref, say, override)
            row.say_var.trace_add("write", lambda *a: self._mark_dirty())
            row.override_var.trace_add("write", lambda *a: self._mark_dirty())
            self.rows.append(row)

            row.status = tk.Label(self.inner, text="●", width=2)
            row.status.grid(row=r, column=0)
            self._paint_status(row)

            ttk.Label(self.inner, text=name, font=("Segoe UI", 10, "bold")).grid(
                row=r, column=1, sticky="w", padx=4)
            seen = "v" + ", v".join(str(v) for v in occ[:8]) + ("…" if len(occ) > 8 else "")
            ttk.Label(self.inner, text=seen, foreground="#666").grid(
                row=r, column=2, sticky="w", padx=4)
            ipa = existing.get("ipa", "") if existing else ""
            ttk.Label(self.inner, text=ipa, foreground="#888").grid(
                row=r, column=3, sticky="w", padx=4)
            ttk.Checkbutton(self.inner, variable=row.override_var,
                            command=lambda rw=row: self._paint_status(rw)).grid(row=r, column=4)
            ent = ttk.Entry(self.inner, textvariable=row.say_var, width=22)
            ent.grid(row=r, column=5, sticky="w", padx=4, pady=1)
            ent.bind("<Return>", lambda e, rw=row: self._play(rw.say_var.get().lower(),
                                                              rw.say_var.get()))
            ttk.Button(self.inner, text="▶ Say", width=6,
                       command=lambda rw=row: self._play(rw.say_var.get().lower(),
                                                         rw.say_var.get())).grid(
                row=r, column=6, padx=2)
            ttk.Button(self.inner, text="▶ Name", width=7,
                       command=lambda rw=row: self._play(rw.name, rw.name)).grid(
                row=r, column=7, padx=(2, 6))
            r += 1

        if not keep_status:
            shown = len(self.rows)
            self.status_var.set(
                f"{self.cur_book} {self.cur_ch}: {shown} name(s) shown"
                + ("  (filtered to new)" if self.filter_var.get() else ""))
        self.canvas.yview_moveto(0)

    def _paint_status(self, row):
        if row.name not in self.names and not row.override_var.get():
            row.status.configure(foreground="#e8890c")   # new / undecided
        elif row.override_var.get():
            row.status.configure(foreground="#2e9e44")   # custom pronunciation
        else:
            row.status.configure(foreground="#bbbbbb")   # reference-only / default

    # ----- edits / persistence -----------------------------------------
    def _mark_dirty(self):
        if not self.dirty:
            self.dirty = True
            self.root.title("Pronunciation Studio  *unsaved*")

    def _commit_rows(self):
        """Fold the on-screen rows back into self.names (session-wide memory).

        Also detects whether any row's *spoken* form actually changed (turned
        override on/off, or edited the say text while override is on -- editing
        say text while override is off doesn't affect audio yet) and, if so,
        marks the chapter these rows belong to for a cache clear on Save.
        """
        changed = False
        for row in self.rows:
            name = row.name
            say = row.say_var.get().strip()
            existing = self.names.get(name)
            if row.override_var.get():
                entry = dict(existing) if existing else {}
                entry["say"] = say or name
                entry["ipa"] = entry.get("ipa", "")
                entry["ref"] = entry.get("ref") or row.default_ref
                entry["override"] = True
                self.names[name] = entry
            elif existing is not None:
                existing["say"] = say or existing.get("say", name)
                existing["override"] = False

            if row.override_var.get() != row.orig_override or (
                    row.override_var.get() and say != row.orig_say):
                changed = True

        if changed and self.cur_book and self.cur_ch:
            self.dirty_chapters.add((self.cur_book, self.cur_ch))

    def _clear_chapter_audio(self, book: str, ch: int) -> int:
        """Delete pre-rendered web/audio/<book>_<ch>_*.mp3 (and their manifest
        entries) so generate_showcase_audio.py -- which skips verses whose mp3
        already exists -- is forced to re-synthesize them with the new
        pronunciation. No-op for chapters that were never pre-rendered.

        (The live desktop cache, cache/audio/tts/, needs no such clearing: it's
        keyed by a hash of the spoken text, so an edited pronunciation already
        produces a fresh cache entry automatically.)
        """
        safe_book = book.replace(" ", "_")
        paths = glob.glob(os.path.join(showcase.AUDIO_DIR, f"{safe_book}_{ch}_*.mp3"))
        if not paths:
            return 0
        manifest = showcase._load_manifest()
        removed = 0
        for path in paths:
            try:
                os.remove(path)
            except OSError:
                continue
            removed += 1
            manifest.pop(os.path.splitext(os.path.basename(path))[0], None)
        if removed:
            showcase._save_manifest(manifest)
        return removed

    def save(self):
        self._commit_rows()
        try:
            pronunciation.save_names(self.names)
        except Exception as e:  # noqa: BLE001 - surface any write error to the user
            messagebox.showerror("Save failed", str(e))
            return
        self.dirty = False
        self.root.title("Pronunciation Studio")

        cleared_chapters = sorted(self.dirty_chapters)
        cleared_files = sum(self._clear_chapter_audio(b, c) for b, c in cleared_chapters)
        self.dirty_chapters = set()

        n_over = sum(1 for v in self.names.values() if v.get("override"))
        msg = (f"Saved {len(self.names)} names ({n_over} custom) to "
              f"pronunciations.json + PRONUNCIATIONS.md.")
        if cleared_files:
            where = ", ".join(f"{b} {c}" for b, c in cleared_chapters)
            msg += (f"  Cleared {cleared_files} cached mp3(s) for {where} "
                   f"-- run generate_showcase_audio.py to re-render.")
        self.status_var.set(msg)
        self._build_rows(keep_status=True)  # refresh status dots, keep save message

    # ----- playback -----------------------------------------------------
    def _play(self, spoken, label):
        spoken = (spoken or "").strip()
        if not spoken or self.busy:
            return
        self.busy = True
        self.status_var.set(f"Synthesizing “{label}”…")
        voice = self.voice_var.get()

        def work():
            try:
                path = tts_engine.synthesize(spoken, voice, RATE, apply_respell=False)
                self.player.load(path)
                self.player.play()
                tag = "" if path.lower().endswith(".mp3") else "   [offline SAPI voice]"
                msg = f"Playing “{label}”{tag}"
            except Exception as e:  # noqa: BLE001
                msg = f"Error: {e}"
            self.root.after(0, lambda: self.status_var.set(msg))
            self.busy = False

        threading.Thread(target=work, daemon=True).start()

    def _on_close(self):
        self._commit_rows()
        if self.dirty:
            ans = messagebox.askyesnocancel(
                "Unsaved changes", "Save your pronunciation changes before closing?")
            if ans is None:
                return
            if ans:
                self.save()
        self.player.close()
        self.root.destroy()


def main():
    # Optional argv: <book> <chapter> -- lets the desktop app open the tool on
    # whatever passage is currently loaded there. Multi-word book names (e.g.
    # "1 Samuel") arrive as separate argv entries when launched via
    # subprocess.Popen([..., book, chapter]), so join everything but the last
    # (numeric) argument back into the book name.
    start_book, start_chapter = "Genesis", 5
    argv = sys.argv[1:]
    if argv:
        try:
            start_chapter = int(argv[-1])
            start_book = " ".join(argv[:-1]) or start_book
        except ValueError:
            pass  # malformed args -- fall back to the Genesis 5 default

    root = tk.Tk()
    App(root, start_book, start_chapter)
    root.mainloop()


if __name__ == "__main__":
    main()
