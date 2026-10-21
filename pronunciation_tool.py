"""Pronunciation Studio -- a local GUI to review and tune proper-noun pronunciations.

Pick a book + chapter and the tool lists every proper noun it finds, marks which
are already customized, and lets you:

  * hear the name as the neural voice says it now  (▶ Name)
  * type your own "Say it" spelling and hear it     (▶ Say / Enter)
  * tick "Custom" when a name needs the override
  * hear Azure say it from its IPA                  (▶ IPA / Enter in the IPA)
    -- edit the IPA until it is right, rather than respelling by trial
  * type IPA from the ⌨ IPA keyboard pop-out, and look symbols up in the
    IPA key (ipa_keyboard.py)
  * tick "Use" to have Azure renders speak it from the IPA (use_ipa)
  * click "✓ Fine" when the plain spelling is already read correctly
  * Save -> writes pronunciations.json AND PRONUNCIATIONS.md, merging with
    anything the Verifier saved while this window was open

▶ IPA is the one preview that costs anything: Azure bills about 40
characters plus the IPA for each new one (replays come from the cache), and
the bottom bar shows the free tier's meter (azure_tts.usage).

The "Checked" column is the point of "✓ Fine": a name you have listened to and
approved used to be stored exactly like one nobody had ever opened, both being
merely ``override: false``. Recording the verdict separates the two, so the
"Unchecked only" filter shows real work rather than the whole book. Ticking
Custom records "overridden"; the Verifier (``pronunciation_check.py``) fills in
the same field from measured audio.

Names are keyed by spelling, so the same name across chapters is one shared
entry: tune "Nahor" in Genesis 11 and it's already tuned when it turns up in
Genesis 22. Preview uses the house voice and rate (tts_engine.HOUSE_VOICE,
HOUSE_RATE) that every narration is rendered with, so what you hear is what
will be rendered.

    python pronunciation_tool.py [book] [chapter]
"""

import copy
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import azure_tts
import books
import config
import ipa_keyboard
import passages
import pronunciation
import tts_engine
from audio_player import AudioPlayer

# The Studio's icon, the same one the shell (app.py) sets.
ICON_PATH = os.path.join(config.WEB_DIR, "icons", "icon-192.png")


# How each verdict is shown. Unchecked is deliberately the attention-getting
# colour: a name nobody has listened to is the one that needs work, and the
# whole point of the status field is that it stops looking like "fine".
STATUS_COLORS = {
    pronunciation.STATUS_UNCHECKED: "#e8890c",   # orange
    pronunciation.STATUS_OK:        "#2e9e44",   # green
    pronunciation.STATUS_FIXED:     "#2f6fdd",   # blue
    pronunciation.STATUS_SUGGESTED: "#b58900",   # amber
    pronunciation.STATUS_UNFIXED:   "#c0392b",   # red
    pronunciation.STATUS_UNSURE:    "#8e44ad",   # purple
}

FILTERS = (
    "All names",
    "Unchecked only",
    "Fine as spelled",
    "Overridden",
    "Suggestions waiting",
    "Still wrong",
    "Unsure (guessed IPA)",
    "Spoken from IPA",
    "Not in the list yet",
)


class Row:
    __slots__ = ("name", "occ", "default_ref", "say_var", "override_var",
                 "ipa_var", "ipa_was", "use_ipa_var", "status_var", "score",
                 "loaded", "dot", "label")

    def __init__(self, name, occ, default_ref, say, override, status, score=None,
                 ipa="", use_ipa=False):
        self.name = name
        self.occ = occ
        self.default_ref = default_ref
        self.say_var = tk.StringVar(value=say)
        self.override_var = tk.BooleanVar(value=override)
        self.ipa_var = tk.StringVar(value=ipa)
        self.ipa_was = ipa       # as loaded: an edit drops the recorded ipa_src
        self.use_ipa_var = tk.BooleanVar(value=use_ipa)
        self.status_var = tk.StringVar(value=status)
        self.score = score
        # The ticks and verdict as loaded: unticking back to them restores the
        # verdict, rather than clearing one the Verifier measured.
        self.loaded = (override, use_ipa, status, score)
        self.dot = None    # the coloured dot widget, set when built
        self.label = None  # the verdict text widget, set when built


class App:
    def __init__(self, root, start_book="Genesis", start_chapter=5):
        self.root = root
        self.player = AudioPlayer()
        self.names = copy.deepcopy(pronunciation.load(force=True))
        # What the file held when self.names was loaded; save_names merges
        # against it so the Verifier's edits since then are not undone.
        self.base = copy.deepcopy(self.names)
        self.rows = []
        self.cur_book = None
        self.cur_ch = None
        self.cur_verses = []
        self.dirty = False
        self.busy = False
        self.ipa_target = None    # the IPA box the keyboard types into
        self.ipa_keyboard = None
        self.ipa_guide = None

        root.title("Pronunciation Studio")
        root.geometry("1240x700")
        root.minsize(1000, 460)
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

        # Right side: the IPA pop-outs (most IPA isn't on a keyboard).
        ttk.Button(bar, text="IPA key", command=self._show_ipa_guide).pack(side="right")
        ttk.Button(bar, text="⌨ IPA keyboard",
                   command=self._show_ipa_keyboard).pack(side="right", padx=(0, 6))

        ttk.Label(bar, text="   Show:").pack(side="left")
        self.filter_var = tk.StringVar(value=FILTERS[0])
        fcb = ttk.Combobox(bar, textvariable=self.filter_var, width=20,
                           state="readonly", values=FILTERS)
        fcb.pack(side="left", padx=(4, 0))
        # Commit first: rebuilding the rows would otherwise drop unsaved edits.
        fcb.bind("<<ComboboxSelected>>",
                 lambda e: (self._commit_rows(), self._build_rows()))

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
        meter = ttk.Frame(self.root, padding=(10, 0))
        meter.pack(fill="x", side="bottom")
        self.azure_var = tk.StringVar()
        ttk.Label(meter, textvariable=self.azure_var, foreground="#888").pack(
            side="left")
        self._refresh_azure()
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
        try:
            passage = passages.load_chapter(book, ch)
        except passages.PassageError as e:
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
        hdr = ("", "Name", "Seen in", "IPA (Azure)", "", "Use", "Checked", "Custom",
               "Say it (Edge)", "", "", "")
        for c, text in enumerate(hdr):
            ttk.Label(self.inner, text=text, font=("Segoe UI", 9, "bold")).grid(
                row=0, column=c, sticky="w", padx=4, pady=(2, 6))

        mode = self.filter_var.get()
        azure_ok = azure_tts.available()[0]
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
                      (existing or {}).get("score"),
                      ipa=(existing or {}).get("ipa", ""),
                      use_ipa=bool((existing or {}).get("use_ipa")))
            row.say_var.trace_add("write", lambda *a: self._mark_dirty())
            row.override_var.trace_add("write", lambda *a: self._mark_dirty())
            row.ipa_var.trace_add("write", lambda *a: self._mark_dirty())
            row.use_ipa_var.trace_add("write", lambda *a: self._mark_dirty())
            self.rows.append(row)

            row.dot = tk.Label(self.inner, text="●", width=2)
            row.dot.grid(row=r, column=0)

            ttk.Label(self.inner, text=name, font=("Segoe UI", 10, "bold")).grid(
                row=r, column=1, sticky="w", padx=4)
            seen = "v" + ", v".join(str(v) for v in occ[:8]) + ("…" if len(occ) > 8 else "")
            ttk.Label(self.inner, text=seen, foreground="#666").grid(
                row=r, column=2, sticky="w", padx=4)
            ipa_ent = ttk.Entry(self.inner, textvariable=row.ipa_var, width=20)
            ipa_ent.grid(row=r, column=3, sticky="w", padx=4, pady=1)
            ipa_ent.bind("<Return>", lambda e, rw=row: self._play_ipa(rw))
            ipa_ent.bind("<FocusIn>", self._on_ipa_focus)
            ttk.Button(self.inner, text="▶ IPA", width=6,
                       state="normal" if azure_ok else "disabled",
                       command=lambda rw=row: self._play_ipa(rw)).grid(
                row=r, column=4, padx=2)
            ttk.Checkbutton(self.inner, variable=row.use_ipa_var,
                            command=lambda rw=row: self._on_use_ipa(rw)).grid(
                row=r, column=5)
            row.label = tk.Label(self.inner, anchor="w", width=17)
            row.label.grid(row=r, column=6, sticky="w", padx=4)
            ttk.Checkbutton(self.inner, variable=row.override_var,
                            command=lambda rw=row: self._on_override(rw)).grid(row=r, column=7)
            ent = ttk.Entry(self.inner, textvariable=row.say_var, width=20)
            ent.grid(row=r, column=8, sticky="w", padx=4, pady=1)
            ent.bind("<Return>", lambda e, rw=row: self._play(rw.say_var.get().lower(),
                                                              rw.say_var.get()))
            ttk.Button(self.inner, text="▶ Say", width=6,
                       command=lambda rw=row: self._play(rw.say_var.get().lower(),
                                                         rw.say_var.get())).grid(
                row=r, column=9, padx=2)
            ttk.Button(self.inner, text="▶ Name", width=7,
                       command=lambda rw=row: self._play(rw.name, rw.name)).grid(
                row=r, column=10, padx=(2, 2))
            ttk.Button(self.inner, text="✓ Fine", width=7,
                       command=lambda rw=row: self._mark_fine(rw)).grid(
                row=r, column=11, padx=(2, 6))
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
                f"{self.cur_book} {self.cur_ch}: {len(self.rows)} shown"
                + (f" — {summary}" if summary else ""))
        self.canvas.yview_moveto(0)

    def _passes(self, mode, existing, status):
        if mode == "All names":
            return True
        if mode == "Not in the list yet":
            return existing is None
        if mode == "Spoken from IPA":
            return bool((existing or {}).get("use_ipa"))
        return status == {
            "Unchecked only": pronunciation.STATUS_UNCHECKED,
            "Fine as spelled": pronunciation.STATUS_OK,
            "Overridden": pronunciation.STATUS_FIXED,
            "Suggestions waiting": pronunciation.STATUS_SUGGESTED,
            "Still wrong": pronunciation.STATUS_UNFIXED,
            "Unsure (guessed IPA)": pronunciation.STATUS_UNSURE,
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
        self._fixed_or_unchecked(row)

    def _on_use_ipa(self, row):
        """Ticking IPA is the same verdict, fixed by the IPA on Azure. Refused
        when Azure couldn't take the IPA as written."""
        if row.use_ipa_var.get():
            try:
                pronunciation.azure_ipa(row.ipa_var.get())
            except ValueError as e:
                row.use_ipa_var.set(False)
                self.status_var.set(f"{row.name}: this IPA can't be sent to "
                                    f"Azure — {e}. Fix it first.")
                return
        self._fixed_or_unchecked(row)

    def _fixed_or_unchecked(self, row):
        override, use_ipa, status, score = row.loaded
        if (row.override_var.get(), row.use_ipa_var.get()) == (override, use_ipa):
            row.status_var.set(status)      # back as it was: keep its verdict
            row.score = score
        else:
            on = row.override_var.get() or row.use_ipa_var.get()
            row.status_var.set(pronunciation.STATUS_FIXED if on
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
            row.use_ipa_var.set(False)
        row.score = None          # a human verdict, not a measured one
        self._paint_status(row)
        self._mark_dirty()

    # ----- IPA pop-outs -------------------------------------------------
    def _on_ipa_focus(self, event):
        self.ipa_target = event.widget

    def _show_ipa_keyboard(self):
        ipa_keyboard.show(self, "ipa_keyboard", lambda: ipa_keyboard.Keyboard(
            self.root, lambda: self.ipa_target, self._show_ipa_guide))

    def _show_ipa_guide(self):
        ipa_keyboard.show(self, "ipa_guide", lambda: ipa_keyboard.Guide(self.root))

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
            ipa = row.ipa_var.get().strip()
            existing = self.names.get(name)
            status = row.status_var.get()
            if row.override_var.get() or row.use_ipa_var.get():
                entry = dict(existing) if existing else {}
                entry["say"] = say or entry.get("say") or name
                entry["ref"] = entry.get("ref") or row.default_ref
                entry["override"] = row.override_var.get()
                pronunciation.set_status(entry, status or pronunciation.STATUS_FIXED,
                                         row.score)
                self.names[name] = entry
            elif existing is not None:
                entry = existing
                entry["say"] = say or existing.get("say", name)
                entry["override"] = False
                pronunciation.set_status(existing, status, row.score)
            elif status or ipa:
                # A verdict (or IPA) on a name not yet in the list is worth
                # keeping -- otherwise marking a new name "fine" would vanish.
                entry = {"say": say or name, "ref": row.default_ref,
                         "override": False}
                pronunciation.set_status(entry, status, row.score)
                self.names[name] = entry
            else:
                continue
            entry["use_ipa"] = row.use_ipa_var.get()
            if ipa != row.ipa_was:
                # Typed here, so no longer the source's: the reports call an
                # entry with no ipa_src "curated".
                entry["ipa"] = ipa
                entry.pop("ipa_src", None)
                row.ipa_was = ipa

    def save(self) -> bool:
        self._commit_rows()
        unsendable = [n for n, v in self.names.items() if v.get("use_ipa")
                      and not self._ipa_ok(v.get("ipa", ""))]
        if unsendable and not messagebox.askyesno(
                "IPA Azure can't take",
                "These names are ticked Use, but their IPA can't be sent to "
                "Azure, so Azure renders will respell them or read them plain "
                "instead:\n\n" + ", ".join(unsendable[:20])
                + ("…" if len(unsendable) > 20 else "") + "\n\nSave anyway?",
                parent=self.root):
            return False
        try:
            saved = pronunciation.save_names(self.names, base=self.base)
        except Exception as e:  # noqa: BLE001 - surface any write error to the user
            messagebox.showerror("Save failed", str(e), parent=self.root)
            return False
        # Adopt the merged list, so names the Verifier saved meanwhile show up
        # here and the next save measures this window's edits from this point.
        self.names = saved.names
        self.base = copy.deepcopy(saved.names)
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
        if saved.warning:
            messagebox.showwarning("pronunciations.json had changed", saved.warning,
                                   parent=self.root)
        return True

    # ----- playback -----------------------------------------------------
    def _play(self, spoken, label):
        spoken = (spoken or "").strip()
        if not spoken or self.busy:
            return
        self.busy = True
        self.status_var.set(f"Synthesizing “{label}”…")

        def work():
            try:
                path = tts_engine.synthesize(spoken, tts_engine.HOUSE_VOICE,
                                             tts_engine.HOUSE_RATE, apply_respell=False)
                self.player.load(path)
                self.player.play()
                tag = "" if path.lower().endswith(".mp3") else "   [offline SAPI voice]"
                msg = f"Playing “{label}”{tag}"
            except Exception as e:  # noqa: BLE001
                msg = f"Error: {e}"
            self.root.after(0, lambda: self.status_var.set(msg))
            self.busy = False

        threading.Thread(target=work, daemon=True).start()

    def _play_ipa(self, row):
        """Azure speaking the name from the IPA in the row as typed -- before
        it is saved, so an edit can be heard first."""
        ipa = row.ipa_var.get().strip()
        if self.busy:
            return
        if not ipa:
            self.status_var.set(f"{row.name} has no IPA to play.")
            return
        try:
            sent = pronunciation.azure_ipa(ipa)
        except ValueError as e:
            self.status_var.set(f"{row.name}: this IPA can't be sent to Azure — {e}.")
            return
        self.busy = True
        self.status_var.set(f"Asking Azure for “{row.name}” as /{sent}/…")

        def work():
            try:
                path = tts_engine.synthesize_ipa(row.name, ipa, tts_engine.HOUSE_VOICE,
                                                 tts_engine.HOUSE_RATE)
                self.player.load(path)
                self.player.play()
                msg = f"Playing “{row.name}” from IPA /{sent}/ (Azure)"
            except Exception as e:  # noqa: BLE001
                msg = f"Error: {e}"
            self.root.after(0, lambda: (self.status_var.set(msg), self._refresh_azure()))
            self.busy = False

        threading.Thread(target=work, daemon=True).start()

    @staticmethod
    def _ipa_ok(ipa: str) -> bool:
        try:
            pronunciation.azure_ipa(ipa)
            return True
        except ValueError:
            return False

    def _refresh_azure(self):
        ok, why = azure_tts.available()
        self.azure_var.set(azure_tts.usage_text() if ok
                           else why + " ▶ IPA needs it.")

    def _on_close(self):
        self._commit_rows()
        if self.dirty:
            ans = messagebox.askyesnocancel(
                "Unsaved changes", "Save your pronunciation changes before closing?")
            if ans is None:
                return
            if ans and not self.save():
                return            # the save failed: keep the window and the edits
        self.player.close()
        self.root.destroy()


def main():
    # Optional argv: <book> <chapter> -- lets the Studio open the tool on its
    # shared passage. Multi-word book names (e.g.
    # "1 Samuel") may arrive as separate argv entries, so join everything but
    # the last one (the chapter) back into the book name.
    start_book, start_chapter = "Genesis", 5
    argv = sys.argv[1:]
    if argv:
        try:
            start_chapter = int(argv[-1])
            start_book = " ".join(argv[:-1]) or start_book
        except ValueError:
            pass  # malformed args -- fall back to the Genesis 5 default

    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.25)   # match the main window and the Verifier
    except tk.TclError:
        pass
    try:
        icon = tk.PhotoImage(file=ICON_PATH)
        root.iconphoto(True, icon)            # True: its dialogs too
    except tk.TclError:
        pass                                  # a missing icon is cosmetic
    App(root, start_book, start_chapter)
    root.mainloop()


if __name__ == "__main__":
    main()
