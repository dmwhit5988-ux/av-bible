"""Video Studio -- render a verse range to a finished, YouTube-ready MP4.

Pick a passage (it may cross chapters: Genesis 1:1 to Genesis 3:24), a
resolution and a frame rate, and this assembles the narration MP3s and the
animated SVG visuals the project already produces into one video, plus the
sidecar files an upload wants: captions, a description with chapter
timestamps, and a thumbnail. Verses without a published MP3 are narrated in
the house voice (tts_engine.HOUSE_VOICE at HOUSE_RATE); there is no voice
choice here.

All the actual work lives in video_render.py; this is the front end, built on
the same pattern as the Audio Renderer (audio_studio.py) -- a worker thread
posting events to a queue that the Tk loop drains.

    python video_studio.py [<book> <chapter>]
"""

import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import books
import tts_engine
import video_render as vr

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
RENDERS_DIR = os.path.join(REPO_ROOT, "renders")


def _render(events, cancel, spec):
    """The render thread. It gets the event queue, the cancel flag and the
    spec, never the App or a widget: it is not a daemon, so it can outlive
    every window, and a thread that drops the last reference to a Tk object
    at exit aborts the whole process ("Tcl_AsyncDelete: async handler
    deleted by the wrong thread"). Exactly one closing event, "done" or
    "failed", is posted whatever happens."""
    outcome = ("failed", "The render stopped unexpectedly.")
    try:
        outcome = ("done", vr.render(
            spec,
            on_status=lambda s: events.put(("status", s)),
            on_progress=lambda phase, done, total, label:
                events.put(("progress", phase, done, total, label)),
            cancel=cancel.is_set))
    except vr.RenderError as e:
        outcome = ("failed", str(e))
    except Exception as e:                          # unexpected: still report
        outcome = ("failed", f"{type(e).__name__}: {e}")
    finally:
        events.put(outcome)


class App:
    def __init__(self, root, book=None, chapter=None, verse=None):
        self.root = root
        self.events: queue.Queue = queue.Queue()
        self.busy = False              # a render is in flight
        self._cancel = threading.Event()
        self.result = None
        self._out_chosen = False       # has the user picked a filename by hand?
        self._range_edited = False     # ...or changed the passage range?
        self._showing = False          # _show_range is writing the pickers

        root.title("Video Studio")
        root.geometry("720x620")
        root.minsize(660, 560)
        root.protocol("WM_DELETE_WINDOW", self._on_close)
        # The shell may destroy this window itself (closing the main window),
        # so stopping a render hangs off <Destroy>, not the close button.
        root.bind("<Destroy>", self._on_destroy, add="+")

        self._build_ui()

        if book not in books.BOOK_NAMES:
            book, chapter, verse = "Genesis", 1, 1
        self._show_range(book, chapter, verse)
        self._sync_out_path()
        # Trace rather than bind: the filename then follows the passage however
        # it was changed -- picker, keyboard, or set from the calling app.
        for var in (self.book_var, self.from_ch_var, self.to_ch_var):
            var.trace_add("write", self._sync_out_path)
        for var in (self.book_var, self.from_ch_var, self.from_v_var,
                    self.to_ch_var, self.to_v_var):
            var.trace_add("write", self._on_range_edit)

        self._poll_events()
        self._check_tools()

    def _show_range(self, book, chapter, verse=None):
        """Set the range to run from book chapter:verse to the end of that
        chapter. A range set here is not one edited by hand."""
        self._showing = True
        try:
            self.book_var.set(book)
            self._on_book_change()
            n = books.chapters_in(book)
            chapter = max(1, min(int(chapter or 1), n))
            self.from_ch_var.set(str(chapter))
            self.from_v_var.set(str(max(1, int(verse or 1))))
            self.to_ch_var.set(str(chapter))
            self.to_v_var.set("")
        finally:
            self._showing = False
        self._range_edited = False

    def _on_range_edit(self, *_):
        if not self._showing:
            self._range_edited = True

    def _covers(self, book, chapter) -> bool:
        """Whether the range's From..To chapters include book chapter."""
        if book != self.book_var.get():
            return False
        try:
            lo, hi = int(self.from_ch_var.get()), int(self.to_ch_var.get())
        except ValueError:
            return False
        return min(lo, hi) <= int(chapter or 1) <= max(lo, hi)

    def set_passage(self, book, chapter, verse=None, *, ask=False) -> bool:
        """Follow book chapter:verse: the range then starts there and ends
        with that chapter. A range edited by hand is kept (True) while the
        chapter lies inside its From..To chapters, so the main window moving
        through it doesn't undo it; a chapter outside it is followed, as
        every move is for a range never edited. Refused (False) while a
        render runs. There is nothing unsaved here, so ask changes nothing."""
        if book not in books.BOOK_NAMES:
            return False
        if self._range_edited and self._covers(book, chapter):
            return True
        if self.busy:
            return False
        self._show_range(book, chapter, verse)
        return True

    # ----- UI construction -------------------------------------------------
    def _build_ui(self):
        pad = {"padx": (4, 14), "pady": (6, 0)}

        passage = ttk.LabelFrame(self.root, text="Passage", padding=(10, 8))
        passage.pack(fill="x", padx=10, pady=(10, 4))

        ttk.Label(passage, text="Book:").grid(row=0, column=0, sticky="w")
        self.book_var = tk.StringVar()
        self.book_cb = ttk.Combobox(passage, textvariable=self.book_var,
                                    width=18, state="readonly",
                                    values=books.BOOK_NAMES)
        self.book_cb.grid(row=0, column=1, sticky="w", **pad)
        self.book_cb.bind("<<ComboboxSelected>>",
                          lambda e: (self._on_book_change(),
                                     self._sync_out_path()))

        ttk.Label(passage, text="From:").grid(row=0, column=2, sticky="w")
        from_frame = ttk.Frame(passage)
        from_frame.grid(row=0, column=3, sticky="w", **pad)
        self.from_ch_var = tk.StringVar(value="1")
        self.from_ch_cb = ttk.Combobox(from_frame, textvariable=self.from_ch_var,
                                       width=4, state="readonly")
        self.from_ch_cb.pack(side="left")
        self.from_ch_cb.bind("<<ComboboxSelected>>",
                             lambda e: self._sync_out_path())
        ttk.Label(from_frame, text=":").pack(side="left")
        self.from_v_var = tk.StringVar(value="1")
        ttk.Entry(from_frame, textvariable=self.from_v_var,
                  width=4).pack(side="left")

        ttk.Label(passage, text="To:").grid(row=1, column=2, sticky="w",
                                            pady=(6, 0))
        to_frame = ttk.Frame(passage)
        to_frame.grid(row=1, column=3, sticky="w", **pad)
        self.to_ch_var = tk.StringVar(value="1")
        self.to_ch_cb = ttk.Combobox(to_frame, textvariable=self.to_ch_var,
                                     width=4, state="readonly")
        self.to_ch_cb.pack(side="left")
        self.to_ch_cb.bind("<<ComboboxSelected>>",
                           lambda e: self._sync_out_path())
        ttk.Label(to_frame, text=":").pack(side="left")
        self.to_v_var = tk.StringVar(value="")
        ttk.Entry(to_frame, textvariable=self.to_v_var, width=4).pack(
            side="left")
        ttk.Label(to_frame, text=" (blank = end)",
                  foreground="#888888").pack(side="left")

        ttk.Label(passage, foreground="#888888",
                  text=f"Verses without a published MP3 are narrated on the "
                       f"fly, in the house voice ({tts_engine.HOUSE_VOICE}).").grid(
            row=2, column=0, columnspan=4, sticky="w", pady=(6, 0))

        # -- output ---------------------------------------------------------
        out = ttk.LabelFrame(self.root, text="Video", padding=(10, 8))
        out.pack(fill="x", padx=10, pady=4)

        ttk.Label(out, text="Resolution:").grid(row=0, column=0, sticky="w")
        self.res_var = tk.StringVar(value=vr.DEFAULT_RESOLUTION)
        ttk.Combobox(out, textvariable=self.res_var, width=24,
                     state="readonly", values=list(vr.RESOLUTIONS)).grid(
            row=0, column=1, sticky="w", **pad)

        ttk.Label(out, text="Frame rate:").grid(row=0, column=2, sticky="w")
        self.fps_var = tk.StringVar(value="60")
        ttk.Combobox(out, textvariable=self.fps_var, width=5, state="readonly",
                     values=[str(f) for f in vr.FRAME_RATES]).grid(
            row=0, column=3, sticky="w", **pad)

        ttk.Label(out, text="Pause between verses:").grid(row=1, column=0,
                                                          sticky="w",
                                                          pady=(6, 0))
        self.gap_var = tk.DoubleVar(value=vr.DEFAULT_GAP)
        gapf = ttk.Frame(out)
        gapf.grid(row=1, column=1, sticky="w", **pad)
        tk.Scale(gapf, from_=0.0, to=2.0, resolution=0.05, orient="horizontal",
                 variable=self.gap_var, length=120, showvalue=True).pack(
            side="left")

        ttk.Label(out, text="Encoder jobs:").grid(row=1, column=2, sticky="w",
                                                  pady=(6, 0))
        self.workers_var = tk.StringVar(value=str(vr.DEFAULT_ENCODE_JOBS))
        ttk.Combobox(out, textvariable=self.workers_var, width=5,
                     state="readonly",
                     values=[str(n) for n in
                             range(1, vr.MAX_ENCODE_JOBS + 1)]).grid(
            row=1, column=3, sticky="w", **pad)

        self.title_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(out, variable=self.title_var,
                        text="Open with a title card").grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(6, 0))
        self.publish_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(out, variable=self.publish_var,
                        text="Also publish new narration to web/audio").grid(
            row=2, column=2, columnspan=2, sticky="w", pady=(6, 0))

        ttk.Label(out, text="Save to:").grid(row=3, column=0, sticky="w",
                                             pady=(8, 0))
        pathf = ttk.Frame(out)
        pathf.grid(row=3, column=1, columnspan=3, sticky="we", pady=(8, 0),
                   padx=(4, 0))
        out.columnconfigure(3, weight=1)
        self.out_var = tk.StringVar()
        ttk.Entry(pathf, textvariable=self.out_var).pack(
            side="left", fill="x", expand=True)
        ttk.Button(pathf, text="…", width=3, command=self._browse).pack(
            side="left", padx=(4, 0))

        # -- actions ---------------------------------------------------------
        btns = ttk.Frame(self.root, padding=(10, 8))
        btns.pack(fill="x")
        self.render_btn = ttk.Button(btns, text="Render video",
                                     command=self.start_render)
        self.render_btn.pack(side="left")
        self.cancel_btn = ttk.Button(btns, text="Cancel", command=self.cancel,
                                     state="disabled")
        self.cancel_btn.pack(side="left", padx=(6, 0))
        self.open_btn = ttk.Button(btns, text="Show in folder",
                                   command=self._reveal, state="disabled")
        self.open_btn.pack(side="left", padx=(6, 0))

        prog = ttk.Frame(self.root, padding=(10, 0))
        prog.pack(fill="x")
        self.progress = ttk.Progressbar(prog, orient="horizontal",
                                        mode="determinate")
        self.progress.pack(fill="x")

        bottom = ttk.Frame(self.root, padding=(10, 8))
        bottom.pack(fill="both", expand=True)
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(bottom, textvariable=self.status_var, wraplength=660,
                  justify="left").pack(anchor="w")
        self.log = tk.Text(bottom, height=9, wrap="word", relief="flat",
                           bg="#f6f4ef", font=("Consolas", 9), state="disabled")
        self.log.pack(fill="both", expand=True, pady=(8, 0))

    # ----- helpers ---------------------------------------------------------
    def _say(self, line: str):
        self.log.configure(state="normal")
        self.log.insert("end", line + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _on_book_change(self):
        n = books.chapters_in(self.book_var.get())
        values = [str(i) for i in range(1, n + 1)]
        self.from_ch_cb.configure(values=values)
        self.to_ch_cb.configure(values=values)
        if self.from_ch_var.get() not in values:
            self.from_ch_var.set("1")
        if self.to_ch_var.get() not in values:
            self.to_ch_var.set("1")

    def _sync_out_path(self, *_):
        """Keep the filename following the passage -- unless the filename was
        chosen by hand, in which case changing chapters must not throw it
        away."""
        if self._out_chosen:
            return
        book = self.book_var.get().replace(" ", "_")
        lo, hi = self.from_ch_var.get(), self.to_ch_var.get()
        span = lo if lo == hi else f"{lo}-{hi}"
        self.out_var.set(os.path.join(RENDERS_DIR, f"{book}_{span}.mp4"))

    def _browse(self):
        path = filedialog.asksaveasfilename(
            parent=self.root, defaultextension=".mp4",
            filetypes=[("MP4 video", "*.mp4")],
            initialfile=os.path.basename(self.out_var.get()),
            initialdir=os.path.dirname(self.out_var.get()) or RENDERS_DIR)
        if path:
            self._out_chosen = True
            self.out_var.set(path)

    def _reveal(self):
        if self.result and os.path.exists(self.result.out_path):
            subprocess.Popen(["explorer", "/select,",
                              os.path.normpath(self.result.out_path)])

    def _check_tools(self):
        """Say up front if ffmpeg or a browser is missing -- far better than
        discovering it forty minutes into a render."""
        try:
            vr.find_ffmpeg()
            vr.find_browser()
        except vr.RenderError as e:
            self.status_var.set("Not ready to render.")
            self._say(str(e))
            self.render_btn.configure(state="disabled")

    def _spec(self):
        try:
            from_ch = int(self.from_ch_var.get())
            to_ch = int(self.to_ch_var.get())
            from_v = int(self.from_v_var.get() or 1)
            to_v = int(self.to_v_var.get()) if self.to_v_var.get().strip() else None
        except ValueError:
            raise ValueError("Chapter and verse must be numbers.")
        if (to_ch, to_v or 10 ** 6) < (from_ch, from_v):
            raise ValueError("The end of the range comes before its start.")
        width, height = vr.RESOLUTIONS[self.res_var.get()]
        out_path = self.out_var.get().strip()
        if not out_path:
            raise ValueError("Choose where to save the video.")
        return vr.RenderSpec(
            book=self.book_var.get(),
            start_chapter=from_ch, start_verse=from_v,
            end_chapter=to_ch, end_verse=to_v,
            out_path=out_path,
            voice=tts_engine.HOUSE_VOICE, rate=tts_engine.HOUSE_RATE,
            width=width, height=height, fps=int(self.fps_var.get()),
            gap=float(self.gap_var.get()),
            title_card=bool(self.title_var.get()),
            publish_new_audio=bool(self.publish_var.get()),
            workers=int(self.workers_var.get()))

    # ----- render ----------------------------------------------------------
    def start_render(self):
        if self.busy:
            return
        try:
            spec = self._spec()
        except ValueError as e:
            messagebox.showerror("Video Studio", str(e), parent=self.root)
            return
        if os.path.exists(spec.out_path) and not messagebox.askyesno(
                "Video Studio",
                f"{os.path.basename(spec.out_path)} already exists. "
                f"Overwrite it?", parent=self.root):
            return

        self.busy = True
        self._cancel.clear()
        self.result = None
        self.render_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.open_btn.configure(state="disabled")
        self.progress.configure(value=0, maximum=100)
        self._say(f"── {spec.reference} · {spec.width}x{spec.height} @ "
                  f"{spec.fps}fps ──")
        # Not a daemon: closing the Studio mid-render then lets it stop after
        # the current verse and clean up -- finish the encodes in flight,
        # terminate headless Chrome (video_render.Chrome.__aexit__) and
        # delete its temp folders -- instead of leaving Chrome running. Each
        # step it can wait on is bounded: CDP commands and captures time out,
        # Chrome startup gives up after 30 s and is killed 10 s after
        # terminate, edge-tts and the SAPI fallback time out, and ffmpeg only
        # reads files.
        threading.Thread(target=_render, name="video-render",
                         args=(self.events, self._cancel, spec),
                         daemon=False).start()

    def cancel(self):
        self._cancel.set()
        self.cancel_btn.configure(state="disabled")
        self.status_var.set("Cancelling after the current verse…")

    # ----- event pump ------------------------------------------------------
    def _poll_events(self):
        try:
            while True:
                try:
                    event = self.events.get_nowait()
                except queue.Empty:
                    break
                self._handle(event)
        finally:
            # Rescheduled even when a handler raised, so a later closing
            # event still clears busy; but not on a destroyed window.
            try:
                alive = self.root.winfo_exists()
            except tk.TclError:
                alive = False
            if alive:
                self.root.after(80, self._poll_events)

    def _idle(self):
        """Back to ready: not busy, Render enabled, Cancel disabled."""
        self.busy = False
        self.render_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")

    def _handle(self, event):
        kind = event[0]
        if kind == "status":
            self.status_var.set(event[1])
            self._say(event[1])
        elif kind == "progress":
            _, phase, done, total, label = event
            self.progress.configure(maximum=max(total, 1), value=done)
            word = "Narration" if phase == "audio" else "Frames"
            self.status_var.set(f"{word} {done}/{total} — {label}")
        elif kind == "done":
            result = event[1]
            self.result = result
            self._idle()
            self.open_btn.configure(state="normal")
            self.progress.configure(value=self.progress["maximum"])
            try:
                size = f"{os.path.getsize(result.out_path) / 1_000_000:.0f} MB"
            except OSError:
                size = "size unknown"
            self.status_var.set(
                f"Done — {vr._stamp(result.duration)}, {size}, "
                f"rendered in {result.seconds / 60:.1f} min.")
            self._say(f"Wrote {result.out_path}")
            for path in result.sidecars:
                self._say(f"  + {os.path.basename(path)}")
            for warning in result.warnings:
                self._say(f"  ! {warning}")
        elif kind == "failed":
            self._idle()
            self.status_var.set("Render cancelled." if self._cancel.is_set()
                                else "Render failed — see the log.")
            self._say(event[1])

    def can_close(self) -> bool:
        """True when the window may close now; asks while a render is in
        progress. Saying yes doesn't stop it yet: the main window may still
        abort its close, so the render stops when the window is destroyed,
        after the verse it is on (the process waits for that and for
        Chrome's shutdown)."""
        if not self.busy:
            return True
        return messagebox.askyesno(
            "Video Studio",
            "A render is in progress. Close anyway? It will stop after "
            "the current verse.", parent=self.root)

    def _on_close(self):
        if self.can_close():
            self.root.destroy()

    def _on_destroy(self, event):
        # <Destroy> on a window fires for each of its children too.
        if event.widget is self.root:
            self._cancel.set()  # a running render stops after this verse


def main():
    # Optional argv: <book> <chapter> -- same convention as the other studios,
    # so this can open on a given passage.
    start_book, start_chapter = "Genesis", 1
    argv = sys.argv[1:]
    if argv:
        try:
            start_chapter = int(argv[-1])
            start_book = " ".join(argv[:-1]) or start_book
        except ValueError:
            pass
    root = tk.Tk()
    App(root, start_book, start_chapter)
    root.mainloop()


if __name__ == "__main__":
    main()
