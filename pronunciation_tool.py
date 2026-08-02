"""Pronunciation Studio -- a local GUI to review and tune proper-noun pronunciations.

Pick a book + chapter and the tool lists every proper noun it finds, marks which
are already customized, and lets you:

  * hear the name as the neural voice says it now  (▶ Name)
  * type your own "Say it" spelling and hear it     (▶ Say / Enter)
  * tick "Custom" when a name needs the override
  * click "✓ Fine" when the plain spelling is already read correctly
  * Save -> writes pronunciations.json AND PRONUNCIATIONS.md

The "Checked" column is the point of "✓ Fine": a name you have listened to and
approved used to be stored exactly like one nobody had ever opened, both being
merely ``override: false``. Recording the verdict separates the two, so the
"Unchecked only" filter shows real work rather than the whole book. Ticking
Custom records "overridden"; the Verifier (``pronunciation_check.py``) fills in
the same field from measured audio.

Names are keyed by spelling, so the same name across chapters is one shared
entry: tune "Nahor" in Genesis 11 and it's already tuned when it turns up in
Genesis 22. Preview uses the same edge-tts voice the web/desktop audio uses, so
what you hear is what will be rendered.

A translation picker lets you scan a chapter as WEB, KJV, etc. Some names are
spelled differently across translations (e.g. KJV "Cainan" where WEB has
"Kenan") -- switch translation and the differently-spelled name shows up as a
new row. There's still just one shared pronunciations.json: each spelling is
its own key, so "Cainan" and "Kenan" sit side by side rather than needing a
separate list per translation.

    python pronunciation_tool.py
"""

import copy
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import books
import pronunciation
import tts_engine
from audio_player import AudioPlayer
from passages import fetch_passage, PassageError, TRANSLATIONS, TRANSLATION_LABELS

RATE = 0


# How each verdict is shown. Unchecked is deliberately the attention-getting
# colour: a name nobody has listened to is the one that needs work, and the
# whole point of the status field is that it stops looking like "fine".
STATUS_COLORS = {
    pronunciation.STATUS_UNCHECKED: "#e8890c",   # orange
    pronunciation.STATUS_OK:        "#2e9e44",   # green
    pronunciation.STATUS_FIXED:     "#2f6fdd",   # blue
    pronunciation.STATUS_SUGGESTED: "#b58900",   # amber
    pronunciation.STATUS_UNFIXED:   "#c0392b",   # red
}

FILTERS = (
    "All names",
    "Unchecked only",
    "Fine as spelled",
    "Overridden",
    "Suggestions waiting",
    "Still wrong",
    "Not in the list yet",
)


class Row:
    __slots__ = ("name", "occ", "default_ref", "say_var", "override_var",
                 "status_var", "score", "dot", "label")

    def __init__(self, name, occ, default_ref, say, override, status, score=None):
        self.name = name
        self.occ = occ
        self.default_ref = default_ref
        self.say_var = tk.StringVar(value=say)
        self.override_var = tk.BooleanVar(value=override)
        self.status_var = tk.StringVar(value=status)
        self.score = score
        self.dot = None    # the coloured dot widget, set when built
        self.label = None  # the verdict text widget, set when built


class App:
    def __init__(self, root, start_book="Genesis", start_chapter=5, start_translation="WEB"):
        self.root = root
        self.player = AudioPlayer()
        self.names = copy.deepcopy(pronunciation.load(force=True))
        self.rows = []
        self.cur_book = None
        self.cur_ch = None
        self.cur_verses = []
        self.dirty = False
        self.busy = False

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
        self.trans_var.set(TRANSLATION_LABELS.get(start_translation, TRANSLATION_LABELS["WEB"]))
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

        ttk.Label(bar, text="   Translation:").pack(side="left")
        self._trans_label_to_code = {label: code for code, label, *_ in TRANSLATIONS}
        self.trans_var = tk.StringVar()
        trans_cb = ttk.Combobox(bar, textvariable=self.trans_var, width=18,
                                state="readonly",
                                values=[label for _, label, *_ in TRANSLATIONS])
        trans_cb.pack(side="left", padx=(4, 10))
        trans_cb.bind("<<ComboboxSelected>>", lambda e: self.load_chapter())

        ttk.Button(bar, text="Load chapter", command=self.load_chapter).pack(side="left")

        ttk.Label(bar, text="   Voice:").pack(side="left")
        self.voice_var = tk.StringVar(value="en-US-AndrewNeural")
        ttk.Combobox(bar, textvariable=self.voice_var, width=22, state="readonly",
                     values=tts_engine.EDGE_VOICES).pack(side="left", padx=(4, 10))

        ttk.Label(bar, text="   Show:").pack(side="left")
        self.filter_var = tk.StringVar(value=FILTERS[0])
        fcb = ttk.Combobox(bar, textvariable=self.filter_var, width=20,
                           state="readonly", values=FILTERS)
        fcb.pack(side="left", padx=(4, 0))
        fcb.bind("<<ComboboxSelected>>", lambda e: self._build_rows())

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
        legend = ttk.Frame(bar)
        legend.pack(side="right", padx=12)
        for st in pronunciation.STATUS_ORDER:
            tk.Label(legend, text="●", foreground=STATUS_COLORS[st]).pack(side="left")
            tk.Label(legend, text=pronunciation.STATUS_LABELS[st],
                     foreground="#888").pack(side="left", padx=(0, 8))

    # ----- data flow ----------------------------------------------------
    def _on_book_change(self):
        n = books.chapters_in(self.book_var.get())
        self.ch_cb.configure(values=[str(i) for i in range(1, n + 1)])
        if self.ch_var.get() not in self.ch_cb["values"]:
            self.ch_var.set("1")

    def load_chapter(self):
        self._commit_rows()  # keep edits from the chapter we're leaving
        book, ch = self.book_var.get(), int(self.ch_var.get() or 1)
        translation = self._trans_label_to_code.get(self.trans_var.get(), "WEB")
        try:
            passage = fetch_passage("", book, ch, translation)
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
        hdr = ("", "Name", "Seen in", "IPA", "Checked", "Custom", "Say it", "", "", "")
        for c, text in enumerate(hdr):
            ttk.Label(self.inner, text=text, font=("Segoe UI", 9, "bold")).grid(
                row=0, column=c, sticky="w", padx=4, pady=(2, 6))

        mode = self.filter_var.get()
        r = 1
        for name, occ in found:
            existing = self.names.get(name)
            status = pronunciation.status_of(existing)
            if not self._passes(mode, existing, status):
                continue
            say = existing["say"] if existing else name
            override = bool(existing.get("override")) if existing else False
            default_ref = f"{self.cur_book} {self.cur_ch}:{occ[0]}"
            row = Row(name, occ, default_ref, say, override, status,
                      (existing or {}).get("score"))
            row.say_var.trace_add("write", lambda *a: self._mark_dirty())
            row.override_var.trace_add("write", lambda *a: self._mark_dirty())
            self.rows.append(row)

            row.dot = tk.Label(self.inner, text="●", width=2)
            row.dot.grid(row=r, column=0)

            ttk.Label(self.inner, text=name, font=("Segoe UI", 10, "bold")).grid(
                row=r, column=1, sticky="w", padx=4)
            seen = "v" + ", v".join(str(v) for v in occ[:8]) + ("…" if len(occ) > 8 else "")
            ttk.Label(self.inner, text=seen, foreground="#666").grid(
                row=r, column=2, sticky="w", padx=4)
            ipa = existing.get("ipa", "") if existing else ""
            ttk.Label(self.inner, text=ipa, foreground="#888").grid(
                row=r, column=3, sticky="w", padx=4)
            row.label = tk.Label(self.inner, anchor="w", width=17)
            row.label.grid(row=r, column=4, sticky="w", padx=4)
            ttk.Checkbutton(self.inner, variable=row.override_var,
                            command=lambda rw=row: self._on_override(rw)).grid(row=r, column=5)
            ent = ttk.Entry(self.inner, textvariable=row.say_var, width=22)
            ent.grid(row=r, column=6, sticky="w", padx=4, pady=1)
            ent.bind("<Return>", lambda e, rw=row: self._play(rw.say_var.get().lower(),
                                                              rw.say_var.get()))
            ttk.Button(self.inner, text="▶ Say", width=6,
                       command=lambda rw=row: self._play(rw.say_var.get().lower(),
                                                         rw.say_var.get())).grid(
                row=r, column=7, padx=2)
            ttk.Button(self.inner, text="▶ Name", width=7,
                       command=lambda rw=row: self._play(rw.name, rw.name)).grid(
                row=r, column=8, padx=(2, 2))
            ttk.Button(self.inner, text="✓ Fine", width=7,
                       command=lambda rw=row: self._mark_fine(rw)).grid(
                row=r, column=9, padx=(2, 6))
            self._paint_status(row)
            r += 1

        if not keep_status:
            counts = {}
            for rw in self.rows:
                counts[rw.status_var.get()] = counts.get(rw.status_var.get(), 0) + 1
            summary = ", ".join(
                f"{counts[s]} {pronunciation.STATUS_LABELS[s]}"
                for s in pronunciation.STATUS_ORDER if counts.get(s))
            self.status_var.set(
                f"{self.cur_book} {self.cur_ch} ({self.trans_var.get()}): "
                f"{len(self.rows)} shown" + (f" — {summary}" if summary else ""))
        self.canvas.yview_moveto(0)

    def _passes(self, mode, existing, status):
        if mode == "All names":
            return True
        if mode == "Not in the list yet":
            return existing is None
        return status == {
            "Unchecked only": pronunciation.STATUS_UNCHECKED,
            "Fine as spelled": pronunciation.STATUS_OK,
            "Overridden": pronunciation.STATUS_FIXED,
            "Suggestions waiting": pronunciation.STATUS_SUGGESTED,
            "Still wrong": pronunciation.STATUS_UNFIXED,
        }.get(mode)

    def _paint_status(self, row):
        st = row.status_var.get()
        text = pronunciation.STATUS_LABELS.get(st, st)
        if st and row.score is not None:
            text += f" {row.score:.2f}"
        colour = STATUS_COLORS.get(st, "#888888")
        row.dot.configure(foreground=colour)
        row.label.configure(text=text, foreground=colour)

    def _on_override(self, row):
        """Ticking Custom is itself a verdict: this name needs a respelling."""
        row.status_var.set(pronunciation.STATUS_FIXED if row.override_var.get()
                           else pronunciation.STATUS_UNCHECKED)
        row.score = None
        self._paint_status(row)

    def _mark_fine(self, row):
        """Record that the plain spelling is read correctly -- or undo that.

        This is the verdict that was previously impossible to express: without
        it, a name you have listened to and approved is stored exactly like one
        nobody has ever opened.
        """
        now = row.status_var.get()
        row.status_var.set(pronunciation.STATUS_UNCHECKED
                           if now == pronunciation.STATUS_OK
                           else pronunciation.STATUS_OK)
        if row.status_var.get() == pronunciation.STATUS_OK:
            row.override_var.set(False)
        row.score = None          # a human verdict, not a measured one
        self._paint_status(row)
        self._mark_dirty()

    # ----- edits / persistence -----------------------------------------
    def _mark_dirty(self):
        if not self.dirty:
            self.dirty = True
            self.root.title("Pronunciation Studio  *unsaved*")

    def _commit_rows(self):
        """Fold the on-screen rows back into self.names (session-wide memory)."""
        for row in self.rows:
            name = row.name
            say = row.say_var.get().strip()
            existing = self.names.get(name)
            status = row.status_var.get()
            if row.override_var.get():
                entry = dict(existing) if existing else {}
                entry["say"] = say or name
                entry["ipa"] = entry.get("ipa", "")
                entry["ref"] = entry.get("ref") or row.default_ref
                entry["override"] = True
                pronunciation.set_status(entry, status or pronunciation.STATUS_FIXED,
                                         row.score)
                self.names[name] = entry
            elif existing is not None:
                existing["say"] = say or existing.get("say", name)
                existing["override"] = False
                pronunciation.set_status(existing, status, row.score)
            elif status:
                # A verdict on a name not yet in the list is worth keeping --
                # otherwise marking a new name "fine" would silently vanish.
                entry = {"say": say or name, "ipa": "", "ref": row.default_ref,
                         "override": False}
                pronunciation.set_status(entry, status, row.score)
                self.names[name] = entry

    def save(self):
        self._commit_rows()
        try:
            pronunciation.save_names(self.names)
        except Exception as e:  # noqa: BLE001 - surface any write error to the user
            messagebox.showerror("Save failed", str(e))
            return
        self.dirty = False
        self.root.title("Pronunciation Studio")
        counts = {}
        for v in self.names.values():
            st = pronunciation.status_of(v)
            counts[st] = counts.get(st, 0) + 1
        summary = ", ".join(f"{counts.get(s, 0)} {pronunciation.STATUS_LABELS[s]}"
                            for s in pronunciation.STATUS_ORDER)
        self.status_var.set(
            f"Saved {len(self.names)} names to pronunciations.json + "
            f"PRONUNCIATIONS.md — {summary}.  The desktop app will re-render "
            f"changed verses automatically on next play.")
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
    # Optional argv: <book> <chapter> [translation] -- lets the desktop app open
    # the tool on whatever passage (and version) is currently loaded there.
    # Multi-word book names (e.g. "1 Samuel") arrive as separate argv entries
    # when launched via subprocess.Popen([..., book, chapter, translation]), so
    # join everything but the last one or two (chapter, optional translation)
    # back into the book name.
    start_book, start_chapter, start_translation = "Genesis", 5, "WEB"
    argv = sys.argv[1:]
    if argv:
        try:
            if argv[-1].upper() in TRANSLATION_LABELS:
                start_translation = argv[-1].upper()
                argv = argv[:-1]
            start_chapter = int(argv[-1])
            start_book = " ".join(argv[:-1]) or start_book
        except ValueError:
            pass  # malformed args -- fall back to the Genesis 5 default

    root = tk.Tk()
    App(root, start_book, start_chapter, start_translation)
    root.mainloop()


if __name__ == "__main__":
    main()
