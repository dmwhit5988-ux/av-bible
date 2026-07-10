"""Audio Renderer -- batch-render chapter narration MP3s for the web app.

Generalizes generate_showcase_audio.py into a GUI: pick a book, a chapter
range, a translation, and a voice, and render neural narration through the
same production path the desktop reader uses (tts_engine.synthesize, which
applies pronunciation respelling). Output lands in web/audio/ and
web/audio/manifest.json exactly as generate_showcase_audio.py writes them
(translation-suffixed keys/filenames, see that module's docstring), so the
web player picks it up for whichever translation the visitor has selected.

Before rendering, shows the projected new-file count against the ~20k
Cloudflare Pages file-count ceiling (STUDIO_PLAN.md Feature C caveat 2),
counting the same files prepare-deploy.ps1 actually bundles. Every
translation you render multiplies the deploy file count, so render
selectively.

    python audio_studio.py
"""

import os
import queue
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import books
import generate_showcase_audio as showcase_audio
import tts_engine
from passages import fetch_passage, PassageError, TRANSLATION_LABELS

RATE = 0
CLOUDFLARE_PAGES_FILE_LIMIT = 20000
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# TRANSLATION_LABELS is {code: label}; the combobox shows labels, so keep the
# reverse lookup handy for turning a UI selection back into a code.
_LABEL_TO_CODE = {label: code for code, label in TRANSLATION_LABELS.items()}


def count_deploy_files() -> int:
    """Count files that would ship to Cloudflare Pages, mirroring the bundle
    prepare-deploy.ps1 actually builds: all of web/, bibles/<code>/*.json
    (one level, not recursive), and visuals/ minus *.xml."""
    count = 0
    web_dir = os.path.join(REPO_ROOT, "web")
    for _, _, files in os.walk(web_dir):
        count += len(files)
    bibles_dir = os.path.join(REPO_ROOT, "bibles")
    if os.path.isdir(bibles_dir):
        for code in os.listdir(bibles_dir):
            code_dir = os.path.join(bibles_dir, code)
            if os.path.isdir(code_dir):
                count += sum(1 for f in os.listdir(code_dir)
                             if f.lower().endswith(".json"))
    visuals_dir = os.path.join(REPO_ROOT, "visuals")
    for _, _, files in os.walk(visuals_dir):
        count += sum(1 for f in files if not f.lower().endswith(".xml"))
    return count


class App:
    def __init__(self, root, start_book="Genesis", start_chapter=1):
        self.root = root
        self.events: queue.Queue = queue.Queue()
        self.busy = False
        self._cancel = threading.Event()

        root.title("Audio Renderer")
        root.geometry("640x440")
        root.minsize(580, 400)
        root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()

        if start_book not in books.BOOK_NAMES:
            start_book, start_chapter = "Genesis", 1
        self.book_var.set(start_book)
        self._on_book_change()
        n = books.chapters_in(start_book)
        start_chapter = max(1, min(int(start_chapter or 1), n))
        self.from_var.set(str(start_chapter))
        self.to_var.set(str(start_chapter))

        self._poll_events()

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

        ttk.Label(top, text="Voice:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.voice_var = tk.StringVar(value=showcase_audio.VOICE)
        ttk.Combobox(top, textvariable=self.voice_var, width=22, state="readonly",
                     values=tts_engine.EDGE_VOICES).grid(
            row=1, column=1, padx=(4, 14), pady=(8, 0), sticky="w")

        ttk.Label(top, text="Translation:").grid(row=1, column=2, sticky="w",
                                                  pady=(8, 0))
        self.translation_var = tk.StringVar(
            value=TRANSLATION_LABELS.get(showcase_audio.TRANSLATION, "WEB"))
        ttk.Combobox(top, textvariable=self.translation_var, width=24,
                     state="readonly",
                     values=list(TRANSLATION_LABELS.values())).grid(
            row=1, column=3, sticky="w", padx=(4, 0), pady=(8, 0))

        ttk.Label(top, foreground="#888888", wraplength=600, justify="left",
                  text="Every translation you render is a separate set of files "
                       "on top of any others already rendered for the same "
                       "verses — watch the file-count guardrail below.").grid(
            row=2, column=0, columnspan=4, sticky="w", pady=(6, 0))

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
        self._refresh_file_count()

    def _refresh_file_count(self):
        try:
            n = count_deploy_files()
            self.count_var.set(
                f"Current deploy bundle: {n:,} files "
                f"(~{CLOUDFLARE_PAGES_FILE_LIMIT:,} Cloudflare Pages limit)")
        except OSError:
            self.count_var.set("")

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
            messagebox.showerror("Audio Renderer", "Pick a valid chapter range.")
            return
        voice = self.voice_var.get()
        translation = _LABEL_TO_CODE.get(self.translation_var.get(),
                                          showcase_audio.TRANSLATION)
        self.busy = True
        self.render_btn.configure(state="disabled")
        self.status_var.set(f"Scanning {book} {chapters[0]}-{chapters[-1]}…")
        threading.Thread(target=self._scan, args=(book, chapters, voice, translation),
                         daemon=True).start()

    def _scan(self, book, chapters, voice, translation):
        """Pre-fetch each chapter to count new-vs-existing verses, so the
        confirm dialog can show the real projected file count. Passages
        fetched here are reused by the render pass -- no double fetch."""
        manifest = showcase_audio._load_manifest()
        passages = {}
        new_files = 0
        total_verses = 0
        for ch in chapters:
            try:
                passage = fetch_passage("", book, ch, translation)
            except PassageError as e:
                self.events.put(("scan_error", f"{book} {ch}: {e}"))
                continue
            passages[ch] = passage
            safe_book = book.replace(" ", "_")
            for num, _ in passage.verses:
                total_verses += 1
                base = f"{safe_book}_{ch}_{num}"
                key = showcase_audio._manifest_key(base, translation)
                out_path = os.path.join(
                    showcase_audio.AUDIO_DIR,
                    showcase_audio._audio_filename(base, translation))
                if not (key in manifest and os.path.exists(out_path)):
                    new_files += 1
        if not passages:
            self.events.put(("render_done", 0, 0, 0))
            return
        current_total = count_deploy_files()
        self.events.put(("confirm", book, chapters, voice, translation, passages,
                         manifest, new_files, current_total, total_verses))

    def _do_confirm(self, book, chapters, voice, translation, passages, manifest,
                     new_files, current_total, total_verses):
        resulting = current_total + new_files
        over = resulting > CLOUDFLARE_PAGES_FILE_LIMIT
        msg = (f"{book} {chapters[0]}-{chapters[-1]} ({translation}): "
               f"{total_verses} verse(s), {new_files} new file(s) to render.\n\n"
               f"Current deploy bundle: {current_total:,} files\n"
               f"Resulting total: {resulting:,} files "
               f"(limit ~{CLOUDFLARE_PAGES_FILE_LIMIT:,})\n\n")
        if over:
            msg += "This would EXCEED the Cloudflare Pages file-count ceiling.\n\n"
        msg += "Continue?"
        proceed = messagebox.askyesno(
            "Confirm render", msg, icon="warning" if over else "question")
        if not proceed:
            self.busy = False
            self.render_btn.configure(state="normal")
            self.status_var.set("Cancelled before rendering.")
            return
        self._cancel.clear()
        self.cancel_btn.configure(state="normal")
        self.progress.configure(maximum=max(total_verses, 1), value=0)
        threading.Thread(target=self._render_worker,
                         args=(book, chapters, voice, translation, passages, manifest),
                         daemon=True).start()

    def _render_worker(self, book, chapters, voice, translation, passages, manifest):
        done = 0
        totals = {"written": 0, "skipped": 0, "degraded": 0}

        def on_verse(num, status, ch_ref):
            nonlocal done
            done += 1
            totals[status] += 1
            self.events.put(("progress", done, f"{book} {ch_ref}:{num} — {status}"))

        for ch in chapters:
            if self._cancel.is_set():
                break
            passage = passages.get(ch)
            if passage is None:
                continue
            showcase_audio.generate_chapter(
                book, ch, manifest, voice=voice, rate=RATE,
                translation=translation, passage=passage,
                on_verse=lambda num, status, ch=ch: on_verse(num, status, ch),
                should_stop=self._cancel.is_set)
            showcase_audio._save_manifest(manifest)  # per-chapter, resumable
        self.events.put(("render_done", totals["written"], totals["skipped"],
                         totals["degraded"]))

    def cancel(self):
        self._cancel.set()
        self.cancel_btn.configure(state="disabled")
        self.status_var.set("Cancelling after the current verse…")

    # ----- event pump (worker thread -> UI thread) -------------------------
    def _poll_events(self):
        try:
            while True:
                event = self.events.get_nowait()
                self._handle_event(event)
        except queue.Empty:
            pass
        self.root.after(80, self._poll_events)

    def _handle_event(self, event):
        kind = event[0]
        if kind == "scan_error":
            self.status_var.set(f"Skipped: {event[1]}")
        elif kind == "confirm":
            self._do_confirm(*event[1:])
        elif kind == "progress":
            _, done, msg = event
            self.progress.configure(value=done)
            self.status_var.set(msg)
        elif kind == "render_done":
            _, written, skipped, degraded = event
            self.busy = False
            self.render_btn.configure(state="normal")
            self.cancel_btn.configure(state="disabled")
            tag = " (cancelled)" if self._cancel.is_set() else ""
            self.status_var.set(
                f"Done{tag}: {written} written, {skipped} already present"
                + (f", {degraded} degraded/skipped" if degraded else "") + ".")
            self._refresh_file_count()

    def _on_close(self):
        if self.busy:
            if not messagebox.askyesno(
                "Audio Renderer",
                "A render is in progress. Close anyway? It will finish the "
                "current verse, then stop."):
                return
            self._cancel.set()
        self.root.destroy()


def main():
    # Optional argv: <book> <chapter> -- lets the desktop app open the tool
    # pre-loaded on whatever passage is currently loaded there (same argv
    # convention as pronunciation_tool.py).
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
