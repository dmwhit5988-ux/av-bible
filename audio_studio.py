"""Audio Renderer -- batch-render chapter narration MP3s for the web app.

Generalizes generate_showcase_audio.py into a GUI: pick a book and a chapter
range, and render neural narration in the house voice
(tts_engine.HOUSE_VOICE at HOUSE_RATE) through the same production path the
desktop reader uses (tts_engine.synthesize, which applies pronunciation
respelling). The one voice picker in the Studio lives here, as an advanced
override for a single render. Output lands in web/audio/ and
web/audio/manifest.json exactly as generate_showcase_audio.py writes them
(see that module's docstring for the key and filename format), so the web
player picks it up.

Before rendering, shows the projected new-file count against the ~20k
file-count ceiling of Cloudflare's Workers static assets
(publish_studio.DEPLOY_FILE_LIMIT; docs/architecture.md, "File budget"),
counting what a deploy ships the way Publish does
(publish_studio.count_deploy_files).

The engine (tts_engine.ENGINES) picks who speaks: free Edge with respellings,
or Azure, which speaks names from their IPA (use_ipa) and is metered -- the
confirm step shows the Azure characters a render would bill against the
free tier's (azure_tts.usage). The choice is remembered (config
"render_engine").

    python audio_studio.py
"""

import os
import queue
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import azure_tts
import books
import config
import generate_showcase_audio as showcase_audio
import tts_engine
from passages import load_chapter, PassageError
from publish_studio import DEPLOY_FILE_LIMIT, count_deploy_files


# ----- worker threads --------------------------------------------------------
# These get the event queue, the cancel flag and plain data, never the App or
# a widget. The render thread is not a daemon, so a Studio close waits for the
# verse it is on and the manifest save; it can therefore outlive every window,
# and a thread that drops the last reference to a Tk object at exit aborts the
# whole process ("Tcl_AsyncDelete: async handler deleted by the wrong thread").
# Each worker posts exactly one closing event, whatever happens, so the window
# always leaves its busy state.

def _scan(events, book, chapters, voice, force, engine):
    """Load each chapter to count new-vs-existing verses, so the confirm
    dialog can show the real projected file count. Passages loaded here
    are reused by the render pass -- no double load. Overwrites (force)
    don't add files, so they never count against the ceiling -- only
    genuinely new files do. Also counts what Azure would be sent: the
    verses to render that the engine routes to Azure and the cache
    doesn't already hold."""
    outcome = ("failed", "The scan stopped unexpectedly.")
    try:
        manifest = showcase_audio._load_manifest()
        passages = {}
        new_files = 0
        total_verses = 0
        azure_verses = azure_chars = 0
        azure_paths = set()       # a repeated verse is synthesized once
        for ch in chapters:
            try:
                passage = load_chapter(book, ch)
            except PassageError as e:
                events.put(("scan_error", f"{book} {ch}: {e}"))
                continue
            passages[ch] = passage
            safe_book = book.replace(" ", "_")
            for num, text in passage.verses:
                total_verses += 1
                base = f"{safe_book}_{ch}_{num}"
                key = showcase_audio._manifest_key(base)
                out_path = os.path.join(showcase_audio.AUDIO_DIR,
                                        showcase_audio._audio_filename(base))
                present = key in manifest and os.path.exists(out_path)
                if not present:
                    new_files += 1
                if present and not force:
                    continue                  # skipped: nothing synthesized
                r = tts_engine.route(text, voice, tts_engine.HOUSE_RATE, engine,
                                     ref=f"{book} {ch}:{num}")
                if (r.engine == tts_engine.ENGINE_AZURE and not r.cached
                        and r.path not in azure_paths):
                    azure_paths.add(r.path)
                    azure_verses += 1
                    azure_chars += r.chars
        if not passages:
            outcome = ("render_done", 0, 0, 0, 0, None)
            return
        current_total = count_deploy_files()
        outcome = ("confirm", book, chapters, voice, passages, manifest,
                   new_files, current_total, total_verses, force, engine,
                   azure_verses, azure_chars)
    except Exception as e:
        outcome = ("failed", f"Scan failed: {type(e).__name__}: {e}")
    finally:
        events.put(outcome)


def _render(events, cancel, book, chapters, voice, passages, manifest, force,
            engine):
    """Render the chapters, stopping before the next verse once cancel is
    set. The manifest is saved after every chapter, including one that
    failed partway, so whatever was written stays registered."""
    done = 0
    totals = {"written": 0, "skipped": 0, "degraded": 0, "failed": 0}
    error = "The render stopped unexpectedly."

    def on_verse(num, status, ch_ref):
        nonlocal done
        done += 1
        totals[status] += 1
        events.put(("progress", done, f"{book} {ch_ref}:{num} — {status}"))

    try:
        for ch in chapters:
            if cancel.is_set():
                break
            passage = passages.get(ch)
            if passage is None:
                continue
            try:
                showcase_audio.generate_chapter(
                    book, ch, manifest, voice=voice,
                    rate=tts_engine.HOUSE_RATE, passage=passage,
                    on_verse=(lambda num, status, ch=ch:
                              on_verse(num, status, ch)),
                    should_stop=cancel.is_set, force=force, engine=engine)
            finally:
                # Per chapter, so an interrupted render resumes.
                showcase_audio._save_manifest(manifest)
        error = None
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
    finally:
        events.put(("render_done", totals["written"], totals["skipped"],
                    totals["degraded"], totals["failed"], error))


class App:
    def __init__(self, root, book=None, chapter=None, verse=None):
        """verse is accepted for the shared tool contract; renders work in
        whole chapters, so it is not used."""
        self.root = root
        self.events: queue.Queue = queue.Queue()
        self.busy = False     # a scan, its confirm dialog or a render
        self._cancel = threading.Event()

        root.title("Audio Renderer")
        root.geometry("660x560")
        root.minsize(600, 520)
        root.protocol("WM_DELETE_WINDOW", self._on_close)
        # The shell may destroy this window itself (closing the main window),
        # so stopping a render hangs off <Destroy>, not the close button.
        root.bind("<Destroy>", self._on_destroy, add="+")

        self._build_ui()

        if book not in books.BOOK_NAMES:
            book, chapter = "Genesis", 1
        self._show_chapter(book, chapter)

        self._poll_events()

    def _show_chapter(self, book, chapter):
        """Set the range to the single chapter book chapter."""
        self.book_var.set(book)
        self._on_book_change()
        n = books.chapters_in(book)
        chapter = max(1, min(int(chapter or 1), n))
        self.from_var.set(str(chapter))
        self.to_var.set(str(chapter))

    def set_passage(self, book, chapter, verse=None, *, ask=False) -> bool:
        """Follow book chapter. A chapter already inside the From..To range
        leaves the range alone (True), so a range built by hand survives the
        main window moving through it; any other chapter becomes the whole
        range. Refused (False) while a render is scanning, confirming or
        running. There is nothing unsaved here, so ask changes nothing."""
        if book not in books.BOOK_NAMES:
            return False
        current, chapters = self._chapter_range()
        if book == current and int(chapter or 1) in chapters:
            return True
        if self.busy:
            return False
        self._show_chapter(book, chapter)
        return True

    # ----- UI construction -----------------------------------------------
    def _build_ui(self):
        top = ttk.Frame(self.root, padding=(10, 10))
        top.pack(fill="x")

        ttk.Label(top, text="Book:").grid(row=0, column=0, sticky="w")
        self.book_var = tk.StringVar()
        self.book_cb = ttk.Combobox(top, textvariable=self.book_var, width=16,
                                    state="readonly", values=books.BOOK_NAMES)
        self.book_cb.grid(row=0, column=1, padx=(4, 14), sticky="w")
        self.book_cb.bind("<<ComboboxSelected>>", lambda e: self._on_book_change())

        ttk.Label(top, text="Chapters:").grid(row=0, column=2, sticky="w")
        chframe = ttk.Frame(top)
        chframe.grid(row=0, column=3, sticky="w", padx=(4, 0))
        self.from_var = tk.StringVar()
        self.from_cb = ttk.Combobox(chframe, textvariable=self.from_var, width=4,
                                    state="readonly")
        self.from_cb.pack(side="left")
        ttk.Label(chframe, text=" to ").pack(side="left")
        self.to_var = tk.StringVar()
        self.to_cb = ttk.Combobox(chframe, textvariable=self.to_var, width=4,
                                  state="readonly")
        self.to_cb.pack(side="left")

        # Advanced: the house voice is the default and the norm; another
        # voice is an override for one render, not a setting (not saved).
        ttk.Label(top, text="Voice override:").grid(row=1, column=0, sticky="w",
                                                    pady=(8, 0))
        self.voice_var = tk.StringVar(value=tts_engine.HOUSE_VOICE)
        ttk.Combobox(top, textvariable=self.voice_var, width=22, state="readonly",
                     values=tts_engine.EDGE_VOICES).grid(
            row=1, column=1, padx=(4, 14), pady=(8, 0), sticky="w")
        ttk.Label(top, foreground="#888888",
                  text=f"advanced — the house voice is "
                       f"{tts_engine.HOUSE_VOICE}").grid(
            row=1, column=2, columnspan=2, sticky="w", pady=(8, 0))

        self.force_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            top, variable=self.force_var,
            text="Overwrite existing files (re-render after a pronunciation "
                 "or voice change)").grid(
            row=2, column=0, columnspan=4, sticky="w", pady=(6, 0))

        # Who speaks. Azure is the only way to use IPA, and it is metered, so
        # its options are greyed out until the key is set.
        ttk.Label(top, text="Engine:").grid(row=3, column=0, sticky="nw",
                                            pady=(10, 0))
        engines = ttk.Frame(top)
        engines.grid(row=3, column=1, columnspan=3, sticky="w", pady=(10, 0))
        saved = config.load().get("render_engine")
        self.engine_var = tk.StringVar(
            value=saved if saved in tts_engine.ENGINES else tts_engine.ENGINE_EDGE)
        azure_ok, self.azure_why = azure_tts.available()
        if not azure_ok:
            self.engine_var.set(tts_engine.ENGINE_EDGE)
        for engine in tts_engine.ENGINES:
            ttk.Radiobutton(
                engines, text=tts_engine.ENGINE_LABELS[engine],
                value=engine, variable=self.engine_var,
                command=self._on_engine_change,
                state=("normal" if azure_ok or engine == tts_engine.ENGINE_EDGE
                       else "disabled")).pack(anchor="w")

        btns = ttk.Frame(self.root, padding=(10, 6))
        btns.pack(fill="x")
        self.render_btn = ttk.Button(btns, text="Render", command=self.start_render)
        self.render_btn.pack(side="left")
        self.cancel_btn = ttk.Button(btns, text="Cancel", command=self.cancel,
                                     state="disabled")
        self.cancel_btn.pack(side="left", padx=(6, 0))

        prog = ttk.Frame(self.root, padding=(10, 4))
        prog.pack(fill="x")
        self.progress = ttk.Progressbar(prog, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x")

        bottom = ttk.Frame(self.root, padding=(10, 8))
        bottom.pack(fill="both", expand=True)
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(bottom, textvariable=self.status_var, wraplength=600,
                  justify="left").pack(anchor="w")
        self.count_var = tk.StringVar()
        ttk.Label(bottom, textvariable=self.count_var, foreground="#888888").pack(
            anchor="w", pady=(10, 0))
        self.azure_var = tk.StringVar()
        ttk.Label(bottom, textvariable=self.azure_var, foreground="#888888").pack(
            anchor="w")
        self._refresh_file_count()

    def _refresh_file_count(self):
        try:
            n = count_deploy_files()
            self.count_var.set(
                f"Current deploy: {n:,} files under web/ "
                f"(~{DEPLOY_FILE_LIMIT:,} Cloudflare limit)")
        except OSError:
            self.count_var.set("")
        ok, _ = azure_tts.available()
        self.azure_var.set(azure_tts.usage_text() if ok else self.azure_why)

    def _on_engine_change(self):
        config.update(render_engine=self.engine_var.get())

    def _on_book_change(self):
        n = books.chapters_in(self.book_var.get())
        values = [str(i) for i in range(1, n + 1)]
        self.from_cb.configure(values=values)
        self.to_cb.configure(values=values)
        if self.from_var.get() not in values:
            self.from_var.set("1")
        if self.to_var.get() not in values:
            self.to_var.set(values[-1] if values else "1")

    # ----- render: scan -> confirm -> render ------------------------------
    def _chapter_range(self):
        book = self.book_var.get()
        try:
            lo, hi = int(self.from_var.get()), int(self.to_var.get())
        except ValueError:
            return book, []
        if lo > hi:
            lo, hi = hi, lo
        return book, list(range(lo, hi + 1))

    def start_render(self):
        if self.busy:
            return
        book, chapters = self._chapter_range()
        if not chapters:
            messagebox.showerror("Audio Renderer", "Pick a valid chapter range.",
                                 parent=self.root)
            return
        voice = self.voice_var.get()
        force = self.force_var.get()
        engine = self.engine_var.get()
        self.busy = True
        # Cleared here, not when the render starts: from now on only closing
        # the window sets it, which the confirm step checks.
        self._cancel.clear()
        self.render_btn.configure(state="disabled")
        self.status_var.set(f"Scanning {book} {chapters[0]}-{chapters[-1]}…")
        # A daemon: the scan only reads, so there is nothing to wait for.
        threading.Thread(target=_scan,
                         args=(self.events, book, chapters, voice, force, engine),
                         daemon=True).start()

    def _do_confirm(self, book, chapters, voice, passages, manifest,
                     new_files, current_total, total_verses, force, engine,
                     azure_verses, azure_chars):
        resulting = current_total + new_files
        over = resulting > DEPLOY_FILE_LIMIT
        overwrites = total_verses - new_files if force else 0
        work = (f"{new_files} new file(s), {overwrites} overwrite(s)"
                if force else f"{new_files} new file(s)")
        msg = (f"{book} {chapters[0]}-{chapters[-1]}: "
               f"{total_verses} verse(s), {work} to render.\n\n"
               f"Current deploy: {current_total:,} files under web/\n"
               f"Resulting total: {resulting:,} files "
               f"(limit ~{DEPLOY_FILE_LIMIT:,})\n\n")
        if voice != tts_engine.HOUSE_VOICE:
            msg += (f"Voice: {voice} — an override, not the house voice "
                    f"({tts_engine.HOUSE_VOICE}).\n\n")
        if over:
            msg += "This would EXCEED Cloudflare's file-count ceiling.\n\n"
        azure_over = False
        if engine != tts_engine.ENGINE_EDGE:
            used = azure_tts.usage()
            azure_over = used + azure_chars > azure_tts.FREE_CHARS
            minutes = azure_verses * azure_tts.MIN_INTERVAL / 60
            msg += (f"Engine: {tts_engine.ENGINE_LABELS[engine]}.\n"
                    f"Azure: {azure_verses} verse(s), about {azure_chars:,} "
                    f"characters (at least {minutes:.0f} min at the free "
                    f"tier's 20 a minute).\n"
                    f"Used in the last {azure_tts.WINDOW_DAYS} days: {used:,} "
                    f"of {azure_tts.FREE_CHARS:,}.\n\n")
            if azure_over:
                msg += ("This would go PAST the free tier's characters; Azure "
                        "refuses requests once they run out.\n\n")
        msg += "Continue?"
        # parent= keeps the dialog owned by this window (not the main studio's
        # root), so dismissing it hands focus back here; the lift/focus_force
        # belt-and-suspenders covers Windows restacking anyway.
        proceed = messagebox.askyesno(
            "Confirm render", msg,
            icon="warning" if over or azure_over else "question",
            parent=self.root)
        if self._cancel.is_set():
            return  # the window was closed while asking: start nothing
        self.root.lift()
        self.root.focus_force()
        if not proceed:
            self._idle()
            self.status_var.set("Cancelled before rendering.")
            return
        self.cancel_btn.configure(state="normal")
        self.progress.configure(maximum=max(total_verses, 1), value=0)
        # Not a daemon: closing the Studio mid-render then finishes the
        # current verse and saves the manifest instead of being cut off
        # mid-write. Every step it can wait on is bounded (edge-tts 10 s
        # connect / 60 s receive, the SAPI fallback 120 s, Azure 30 s a try
        # with one retry, or about 2 min of backoff while it throttles), so
        # it can't hang.
        threading.Thread(target=_render, name="audio-render",
                         args=(self.events, self._cancel, book, chapters,
                               voice, passages, manifest, force, engine),
                         daemon=False).start()

    def _idle(self):
        """Back to ready: not busy, Render enabled, Cancel disabled."""
        self.busy = False
        self.render_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")

    def _fail(self, msg):
        """Back to ready after a failure, and say what went wrong."""
        self._idle()
        self.status_var.set(msg)
        messagebox.showerror("Audio Renderer", msg, parent=self.root)

    def cancel(self):
        self._cancel.set()
        self.cancel_btn.configure(state="disabled")
        self.status_var.set("Cancelling after the current verse…")

    # ----- event pump (worker thread -> UI thread) -------------------------
    def _poll_events(self):
        try:
            while True:
                try:
                    event = self.events.get_nowait()
                except queue.Empty:
                    break
                self._handle_event(event)
        finally:
            # Rescheduled even when a handler raised, so a later closing
            # event still clears busy; but not on a destroyed window.
            try:
                alive = self.root.winfo_exists()
            except tk.TclError:
                alive = False
            if alive:
                self.root.after(80, self._poll_events)

    def _handle_event(self, event):
        kind = event[0]
        if kind == "scan_error":
            self.status_var.set(f"Skipped: {event[1]}")
        elif kind == "confirm":
            try:
                self._do_confirm(*event[1:])
            except Exception as e:      # never leave the window stuck busy
                if not self._cancel.is_set():
                    self._fail(f"Could not start the render: "
                               f"{type(e).__name__}: {e}")
        elif kind == "progress":
            _, done, msg = event
            self.progress.configure(value=done)
            self.status_var.set(msg)
        elif kind == "render_done":
            _, written, skipped, degraded, failed, error = event
            counts = (f"{written} written, {skipped} already present"
                      + (f", {degraded} degraded/skipped" if degraded else "")
                      + (f", {failed} refused by Azure" if failed else ""))
            if error:
                self._fail(f"Render failed ({counts} before it stopped): "
                           f"{error}")
            else:
                self._idle()
                tag = " (cancelled)" if self._cancel.is_set() else ""
                self.status_var.set(f"Done{tag}: {counts}.")
            self._refresh_file_count()
        elif kind == "failed":
            self._fail(event[1])

    def can_close(self) -> bool:
        """True when the window may close now; asks while a render is in
        progress. Saying yes doesn't stop it yet: the main window may still
        abort its close, so the render stops when the window is destroyed,
        after the verse it is on (the process waits for that and the
        manifest save)."""
        if not self.busy:
            return True
        return messagebox.askyesno(
            "Audio Renderer",
            "A render is in progress. Close anyway? It will finish the "
            "current verse, then stop.", parent=self.root)

    def _on_close(self):
        if self.can_close():
            self.root.destroy()

    def _on_destroy(self, event):
        # <Destroy> on a window fires for each of its children too.
        if event.widget is self.root:
            self._cancel.set()  # a running render stops after this verse


def main():
    # Optional argv: <book> <chapter> -- opens the tool on that passage (same
    # argv convention as pronunciation_tool.py).
    start_book, start_chapter = "Genesis", 1
    argv = sys.argv[1:]
    if argv:
        try:
            start_chapter = int(argv[-1])
            start_book = " ".join(argv[:-1]) or start_book
        except ValueError:
            pass  # malformed args -- fall back to the Genesis 1 default

    root = tk.Tk()
    App(root, start_book, start_chapter)
    root.mainloop()


if __name__ == "__main__":
    main()
