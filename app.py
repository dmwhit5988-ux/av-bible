"""AV Bible — reads the World English Bible aloud with a per-verse visual stage.

Run with:  python app.py   (or double-click run.bat)
"""

import os
import queue
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import tkinter as tk
from tkinter import ttk

import audio_studio
import config
import coverage_studio
import publish_studio
import svg_studio
import video_studio
from books import BOOK_NAMES, chapters_in
from passages import ATTRIBUTION, Passage, PassageError, load_chapter
from tts_engine import EDGE_VOICES, synthesize
from audio_player import AudioPlayer
from visual_stage import (StageController, StageView, FullscreenStage,
                          VerseContext)

APP_TITLE = "AV Bible"


# ---------------------------------------------------------------------------
# Playback session (worker thread)
# ---------------------------------------------------------------------------

class PlaybackSession(threading.Thread):
    """Plays one passage. Emits events to the UI through a queue:

    ('status', sid, message)
    ('error', sid, message)
    ('verse', sid, index)           index into passage.verses
    ('intro', sid)                  chapter announcement is playing
    ('done', sid, completed)        completed=False when stopped early
    """

    _next_sid = 0

    def __init__(self, events: queue.Queue, passage: Passage, start_index: int,
                 voice: str, rate: int):
        super().__init__(daemon=True)
        PlaybackSession._next_sid += 1
        self.sid = PlaybackSession._next_sid
        self.events = events
        self.passage = passage
        self.start_index = max(0, min(start_index, len(passage.verses) - 1))
        self.voice = voice
        self.rate = rate
        self.player = AudioPlayer()
        self._stop = threading.Event()
        self._jump = None
        self._jump_lock = threading.Lock()
        self._executor = ThreadPoolExecutor(max_workers=2)
        self._futures = {}
        self._fut_lock = threading.Lock()

    # -- controls (called from the UI thread) ------------------------------

    def stop(self):
        self._stop.set()
        self.player.stop()

    def request_jump(self, index: int):
        with self._jump_lock:
            self._jump = max(0, min(index, len(self.passage.verses) - 1))
        self.player.stop()  # breaks the poll loop quickly

    def _take_jump(self):
        with self._jump_lock:
            j, self._jump = self._jump, None
        return j

    # -- helpers ------------------------------------------------------------

    def emit(self, *event):
        self.events.put(event)

    def _ensure_audio(self, i: int) -> str:
        n = len(self.passage.verses)
        with self._fut_lock:
            for k in range(i, min(i + 3, n)):
                if k not in self._futures:
                    text = self.passage.verses[k][1]
                    self._futures[k] = self._executor.submit(
                        synthesize, text, self.voice, self.rate)
            fut = self._futures[i]
        return fut.result()

    def _play_and_wait(self, path: str) -> bool:
        """Play a file until it ends. Returns False if interrupted."""
        self.player.load(path)
        self.player.play()
        while not self._stop.is_set():
            with self._jump_lock:
                jump_pending = self._jump is not None
            if jump_pending:
                return False
            mode = self.player.mode()
            if mode in ("", "stopped"):
                return True
            time.sleep(0.06)
        return False

    # -- main loop ----------------------------------------------------------

    def run(self):
        try:
            self._run_tts()
        except Exception as e:  # surface anything unexpected to the UI
            self.emit("error", self.sid, f"Playback error: {e}")
            self.emit("done", self.sid, False)
        finally:
            self.player.close()
            self._executor.shutdown(wait=False, cancel_futures=True)

    def _run_tts(self):
        passage = self.passage
        n = len(passage.verses)
        i = self.start_index

        if i == 0 and not self._stop.is_set():
            self.emit("intro", self.sid)
            self.emit("status", self.sid, f"Preparing {passage.canonical}…")
            intro_text = f"{passage.canonical}."
            try:
                intro_path = synthesize(intro_text, self.voice, self.rate)
                self._play_and_wait(intro_path)
            except Exception:
                pass  # a missing chapter announcement is not fatal

        while i < n and not self._stop.is_set():
            self.emit("status", self.sid,
                      f"Reading {passage.canonical}:{passage.verses[i][0]} "
                      f"({i + 1} of {n})")
            path = self._ensure_audio(i)
            if self._stop.is_set():
                break
            j = self._take_jump()
            if j is not None:
                i = j
                continue
            self.emit("verse", self.sid, i)
            self._play_and_wait(path)
            j = self._take_jump()
            i = j if j is not None else i + 1

        self.emit("done", self.sid, not self._stop.is_set())


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.cfg = config.load()
        config.ensure_dirs()

        self.events: queue.Queue = queue.Queue()
        self.session: PlaybackSession | None = None
        self.current_sid = 0
        self.passage: Passage | None = None
        self.fullscreen_stage: FullscreenStage | None = None
        self.audio_studio_win: tk.Toplevel | None = None
        self.svg_studio_win: tk.Toplevel | None = None
        self.publish_win: tk.Toplevel | None = None
        self.coverage_win: tk.Toplevel | None = None
        self.video_studio_win: tk.Toplevel | None = None
        self.stage = StageController()

        self._build_ui()
        self._poll_events()
        root.protocol("WM_DELETE_WINDOW", self._on_close)

    # -- UI construction ----------------------------------------------------

    def _build_ui(self):
        root = self.root
        root.title(f"{APP_TITLE} — Scripture reader")
        root.geometry("1180x700")
        root.minsize(900, 540)

        top = ttk.Frame(root, padding=(10, 8, 10, 4))
        top.pack(fill="x")

        ttk.Label(top, text="Book:").pack(side="left")
        self.book_var = tk.StringVar(value=self.cfg["last_book"])
        self.book_combo = ttk.Combobox(
            top, textvariable=self.book_var, values=BOOK_NAMES,
            state="readonly", width=17)
        self.book_combo.pack(side="left", padx=(4, 10))
        self.book_combo.bind("<<ComboboxSelected>>", self._on_book_change)

        ttk.Label(top, text="Chapter:").pack(side="left")
        self.chapter_var = tk.StringVar(value=str(self.cfg["last_chapter"]))
        self.chapter_combo = ttk.Combobox(
            top, textvariable=self.chapter_var, state="readonly", width=5)
        self.chapter_combo.pack(side="left", padx=(4, 10))
        self.chapter_combo.bind("<<ComboboxSelected>>",
                                lambda e: self.verse_var.set("1"))
        self._refresh_chapters()

        ttk.Label(top, text="Verse:").pack(side="left")
        self.verse_var = tk.StringVar(value="1")
        self.verse_combo = ttk.Combobox(
            top, textvariable=self.verse_var, values=["1"], width=5)
        self.verse_combo.pack(side="left", padx=(4, 14))

        ttk.Label(top, text="Voice:").pack(side="left")
        self.voice_var = tk.StringVar(value=self.cfg["voice"])
        voice_combo = ttk.Combobox(
            top, textvariable=self.voice_var, values=EDGE_VOICES,
            state="readonly", width=25)
        voice_combo.pack(side="left", padx=(4, 14))

        ttk.Label(top, text="Speed:").pack(side="left")
        self.rate_var = tk.IntVar(value=int(self.cfg["rate"]))
        tk.Scale(top, from_=-40, to=40, resolution=5, orient="horizontal",
                 variable=self.rate_var, length=110,
                 showvalue=False).pack(side="left", padx=(4, 0))

        bar = ttk.Frame(root, padding=(10, 2, 10, 6))
        bar.pack(fill="x")

        self.play_btn = ttk.Button(bar, text="▶ Play", command=self.play)
        self.play_btn.pack(side="left")
        self.stop_btn = ttk.Button(bar, text="⏹ Stop", command=self.stop,
                                   state="disabled")
        self.stop_btn.pack(side="left", padx=(6, 14))
        ttk.Button(bar, text="◀ Prev", command=self.prev_item).pack(side="left")
        ttk.Button(bar, text="Next ▶", command=self.next_item).pack(
            side="left", padx=(6, 14))

        self.auto_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(bar, text="Auto-continue",
                        variable=self.auto_var).pack(side="left")

        self.ref_var = tk.BooleanVar(
            value=bool(self.cfg.get("show_reference", True)))
        ttk.Checkbutton(bar, text="Reference",
                        variable=self.ref_var,
                        command=self._on_display_toggle).pack(side="left",
                                                              padx=(14, 0))

        ttk.Button(bar, text="🚀 Publish",
                   command=self.open_publish).pack(side="right", padx=(0, 6))
        ttk.Button(bar, text="📊 Coverage",
                   command=self.open_coverage).pack(side="right", padx=(0, 6))
        ttk.Button(bar, text="🎨 SVG Studio",
                   command=self.open_svg_studio).pack(side="right", padx=(0, 6))
        ttk.Button(bar, text="🎙 Pronunciation Studio",
                   command=self.open_pronunciation_tool).pack(side="right", padx=(0, 6))
        ttk.Button(bar, text="👂 Verifier",
                   command=self.open_pronunciation_check).pack(side="right", padx=(0, 6))
        ttk.Button(bar, text="🎬 Video Studio",
                   command=self.open_video_studio).pack(side="right", padx=(0, 6))
        ttk.Button(bar, text="🎚 Audio Renderer",
                   command=self.open_audio_studio).pack(side="right", padx=(0, 6))
        ttk.Button(bar, text="🖥 Display window",
                   command=self.open_fullscreen).pack(side="right", padx=(0, 6))

        main = ttk.PanedWindow(root, orient="horizontal")
        main.pack(fill="both", expand=True, padx=10, pady=(0, 4))

        text_frame = ttk.Frame(main)
        self.text = tk.Text(
            text_frame, wrap="word", width=44, font=("Georgia", 12),
            padx=12, pady=10, spacing3=8, cursor="hand2",
            state="disabled", bg="#fbf8f1", relief="flat")
        scroll = ttk.Scrollbar(text_frame, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        self.text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        main.add(text_frame, weight=2)

        self.text.tag_configure("vnum", foreground="#b08a2e",
                                font=("Georgia", 9, "bold"), offset=4)
        self.text.tag_configure("current", background="#fdeeba")
        self.text.tag_configure("title", font=("Georgia", 15, "bold"),
                                spacing3=12)

        stage_frame = ttk.Frame(main)
        self.stage_view = StageView(stage_frame, self.stage)
        self.stage_view.canvas.pack(fill="both", expand=True)
        main.add(stage_frame, weight=3)

        bottom = ttk.Frame(root, padding=(10, 2, 10, 6))
        bottom.pack(fill="x")
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(bottom, textvariable=self.status_var).pack(side="left")
        ttk.Label(bottom, text=ATTRIBUTION, foreground="#777777",
                  font=("Segoe UI", 8)).pack(side="right")

    # -- small UI helpers ----------------------------------------------------

    def set_status(self, msg: str):
        self.status_var.set(msg)

    def _on_display_toggle(self):
        self.cfg["show_reference"] = bool(self.ref_var.get())
        config.save(self.cfg)
        # Refresh the stage immediately if a verse is showing.
        ctx = self.stage.current
        if ctx is not None and self.passage is not None and ctx.verse:
            self.stage.show_verse(self._verse_context(ctx.index))

    def _refresh_chapters(self):
        book = self.book_var.get()
        count = chapters_in(book)
        self.chapter_combo["values"] = [str(i) for i in range(1, count + 1)]
        if not (1 <= self._chapter() <= count):
            self.chapter_var.set("1")

    def _chapter(self) -> int:
        try:
            return int(self.chapter_var.get())
        except ValueError:
            return 1

    def _on_book_change(self, _event=None):
        self._refresh_chapters()
        self.chapter_var.set("1")
        self.verse_var.set("1")

    def open_fullscreen(self):
        if self.fullscreen_stage and self.fullscreen_stage.top.winfo_exists():
            self.fullscreen_stage.close()
        self.fullscreen_stage = FullscreenStage(self.root, self.stage)

    def open_pronunciation_tool(self):
        """Launch the Pronunciation Studio in a separate process, opened on
        whatever book/chapter is currently selected here."""
        try:
            script_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "pronunciation_tool.py"
            )
            book = self.book_var.get()
            chapter = self._chapter()
            subprocess.Popen([sys.executable, script_path, book, str(chapter)])
            self.set_status(f"Pronunciation Studio launched on {book} {chapter}.")
        except Exception as e:
            self.set_status(f"Error launching Pronunciation Studio: {e}")

    def open_pronunciation_check(self):
        """Launch the Pronunciation Verifier in a separate process.

        No book/chapter is passed: unlike the Studio, the Verifier works across
        the whole pronunciations.json list rather than one chapter's names.
        """
        try:
            script_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "pronunciation_check.py"
            )
            subprocess.Popen([sys.executable, script_path])
            self.set_status("Pronunciation Verifier launched.")
        except Exception as e:
            self.set_status(f"Error launching Pronunciation Verifier: {e}")

    def open_audio_studio(self):
        """Open the Audio Renderer as a Toplevel, pre-loaded on whatever
        book/chapter is currently selected here."""
        if self.audio_studio_win is not None and self.audio_studio_win.winfo_exists():
            self.audio_studio_win.deiconify()
            self.audio_studio_win.lift()
            self.audio_studio_win.focus_force()
            return
        book = self.book_var.get()
        chapter = self._chapter()
        top = tk.Toplevel(self.root)
        audio_studio.App(top, book, chapter)
        self.audio_studio_win = top
        self.set_status(f"Audio Renderer opened on {book} {chapter}.")

    def open_svg_studio(self):
        """Open the SVG Studio as a Toplevel, pre-loaded on whatever
        book/chapter is currently selected here."""
        if self.svg_studio_win is not None and self.svg_studio_win.winfo_exists():
            self.svg_studio_win.deiconify()
            self.svg_studio_win.lift()
            self.svg_studio_win.focus_force()
            return
        book = self.book_var.get()
        chapter = self._chapter()
        top = tk.Toplevel(self.root)
        svg_studio.App(top, book, chapter)
        self.svg_studio_win = top
        self.set_status(f"SVG Studio opened on {book} {chapter}.")

    def open_video_studio(self):
        """Open the Video Studio as a Toplevel, pre-loaded on whatever
        book/chapter is currently selected here."""
        if (self.video_studio_win is not None
                and self.video_studio_win.winfo_exists()):
            self.video_studio_win.deiconify()
            self.video_studio_win.lift()
            self.video_studio_win.focus_force()
            return
        book = self.book_var.get()
        chapter = self._chapter()
        top = tk.Toplevel(self.root)
        video_studio.App(top, book, chapter)
        self.video_studio_win = top
        self.set_status(f"Video Studio opened on {book} {chapter}.")

    def open_publish(self):
        """Open the Publish tool (stills → manifest → deploy bundle → git
        push) as a Toplevel."""
        if self.publish_win is not None and self.publish_win.winfo_exists():
            self.publish_win.deiconify()
            self.publish_win.lift()
            self.publish_win.focus_force()
            return
        top = tk.Toplevel(self.root)
        publish_studio.App(top)
        self.publish_win = top
        self.set_status("Publish tool opened.")

    def open_coverage(self):
        """Open the Coverage dashboard as a Toplevel. Its "Go to chapter"
        action points the reader's pickers at the selected row."""
        if self.coverage_win is not None and self.coverage_win.winfo_exists():
            self.coverage_win.deiconify()
            self.coverage_win.lift()
            self.coverage_win.focus_force()
            return

        def goto(book, chapter):
            if book not in BOOK_NAMES:
                return
            self.book_var.set(book)
            self._on_book_change()
            self.chapter_var.set(str(chapter))
            self.root.deiconify()
            self.root.lift()
            self.set_status(f"Coverage: jumped to {book} {chapter} — "
                            f"press Play or open a studio tool.")

        top = tk.Toplevel(self.root)
        coverage_studio.App(top, goto=goto)
        self.coverage_win = top
        self.set_status("Coverage dashboard opened.")

    # -- transport controls --------------------------------------------------

    def _selected_verse_number(self) -> int:
        try:
            return max(1, int(self.verse_var.get().strip()))
        except (ValueError, AttributeError):
            return 1

    @staticmethod
    def _index_for_verse(passage: Passage, verse_number: int) -> int:
        for i, (num, _) in enumerate(passage.verses):
            if num >= verse_number:
                return i
        return len(passage.verses) - 1

    def play(self, start_index: int | None = None):
        self._stop_session()
        book = self.book_var.get()
        chapter = self._chapter()
        verse_number = self._selected_verse_number()
        self.set_status(f"Loading {book} {chapter}…")
        self.play_btn.configure(state="disabled")

        def worker():
            try:
                passage = load_chapter(book, chapter)
                self.events.put(("fetched", passage, start_index,
                                 verse_number))
            except PassageError as e:
                self.events.put(("fetch_error", str(e)))
            except Exception as e:
                self.events.put(("fetch_error", f"Unexpected error: {e}"))

        threading.Thread(target=worker, daemon=True).start()

    def _start_session(self, passage: Passage, start: int):
        self.passage = passage
        self._render_passage(passage)
        self.verse_combo["values"] = [str(num) for num, _ in passage.verses]
        self.verse_var.set(str(passage.verses[start][0]))
        self.session = PlaybackSession(
            self.events, passage, start,
            voice=self.voice_var.get(),
            rate=int(self.rate_var.get()),
        )
        self.current_sid = self.session.sid
        self._save_position()
        self.session.start()
        self.play_btn.configure(state="normal")
        self.stop_btn.configure(state="normal")

    def _stop_session(self):
        if self.session and self.session.is_alive():
            self.session.stop()
        self.session = None
        self.current_sid = 0

    def stop(self):
        self._stop_session()
        self.stop_btn.configure(state="disabled")
        self.set_status("Stopped.")

    def next_item(self):
        if self.session and self.session.is_alive():
            idx = self._current_index()
            if idx is not None:
                self.session.request_jump(idx + 1)
            return
        self._step_chapter(+1)

    def prev_item(self):
        if self.session and self.session.is_alive():
            idx = self._current_index()
            if idx is not None:
                self.session.request_jump(idx - 1)
            return
        self._step_chapter(-1)

    def _current_index(self):
        ctx = self.stage.current
        if ctx is None or self.passage is None:
            return None
        return ctx.index

    def _step_chapter(self, delta: int):
        book = self.book_var.get()
        chapter = self._chapter() + delta
        if chapter < 1:
            idx = BOOK_NAMES.index(book)
            if idx > 0:
                book = BOOK_NAMES[idx - 1]
                chapter = chapters_in(book)
            else:
                chapter = 1
        elif chapter > chapters_in(book):
            idx = BOOK_NAMES.index(book)
            if idx < len(BOOK_NAMES) - 1:
                book = BOOK_NAMES[idx + 1]
                chapter = 1
            else:
                chapter = chapters_in(book)
        self.book_var.set(book)
        self._refresh_chapters()
        self.chapter_var.set(str(chapter))
        self.verse_var.set("1")

    def _save_position(self):
        self.cfg.update({
            "last_book": self.book_var.get(),
            "last_chapter": self._chapter(),
            "voice": self.voice_var.get(),
            "rate": int(self.rate_var.get()),
            "show_reference": bool(self.ref_var.get()),
        })
        config.save(self.cfg)

    # -- passage rendering ----------------------------------------------------

    def _render_passage(self, passage: Passage):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("end", f"{passage.canonical}\n", "title")
        for idx, (num, verse_text) in enumerate(passage.verses):
            tag = f"verse{idx}"
            self.text.insert("end", f"{num} ", ("vnum", tag))
            self.text.insert("end", verse_text + "\n", (tag,))
            self.text.tag_bind(tag, "<Button-1>",
                               lambda e, i=idx: self._on_verse_click(i))
        self.text.configure(state="disabled")

    def _on_verse_click(self, idx: int):
        if self.session and self.session.is_alive():
            self.session.request_jump(idx)
        else:
            self.play(start_index=idx)

    def _highlight_verse(self, idx: int | None):
        self.text.tag_remove("current", "1.0", "end")
        if idx is None:
            return
        ranges = self.text.tag_ranges(f"verse{idx}")
        if ranges:
            self.text.tag_add("current", ranges[0], ranges[-1])
            self.text.see(ranges[0])

    def _verse_context(self, idx: int) -> VerseContext:
        p = self.passage
        num, verse_text = p.verses[idx]
        return VerseContext(
            book=p.book, chapter=p.chapter, verse=num, text=verse_text,
            reference=f"{p.canonical}:{num}",
            index=idx, total=len(p.verses),
            show_reference=bool(self.ref_var.get()))

    # -- event pump ------------------------------------------------------------

    def _poll_events(self):
        try:
            while True:
                event = self.events.get_nowait()
                self._handle_event(event)
        except queue.Empty:
            pass
        self.root.after(60, self._poll_events)

    def _handle_event(self, event):
        kind = event[0]

        if kind == "fetched":
            _, passage, start_index, verse_number = event
            if start_index is None:
                start_index = self._index_for_verse(passage, verse_number)
            self._start_session(passage, start_index)
            return
        if kind == "fetch_error":
            self.play_btn.configure(state="normal")
            self.set_status(event[1])
            return

        sid = event[1]
        if sid != self.current_sid:
            return  # stale event from a stopped session

        if kind == "status":
            self.set_status(event[2])
        elif kind == "error":
            self.set_status(event[2])
        elif kind == "verse":
            idx = event[2]
            self._highlight_verse(idx)
            # Track playback in the verse dropdown (like the web app),
            # so Stop followed by Play resumes from the verse being
            # read instead of restarting the chapter.
            self.verse_var.set(str(self.passage.verses[idx][0]))
            self.stage.show_verse(self._verse_context(idx))
        elif kind == "intro":
            p = self.passage
            self._highlight_verse(None)
            self.stage.show_verse(VerseContext(
                book=p.book, chapter=p.chapter, verse=0, text="",
                reference=p.canonical,
                index=0, total=len(p.verses),
                show_reference=bool(self.ref_var.get())))
        elif kind == "done":
            completed = event[2]
            self.stop_btn.configure(state="disabled")
            self.session = None
            self.current_sid = 0
            if completed and self.passage:
                # A finished chapter replays from the top; a chapter
                # stopped early keeps its place in the verse dropdown.
                self.verse_var.set("1")
                self.set_status(f"Finished {self.passage.canonical}.")
                if self.auto_var.get():
                    at_end = (self.book_var.get() == BOOK_NAMES[-1]
                              and self._chapter() >=
                              chapters_in(BOOK_NAMES[-1]))
                    if not at_end:
                        self._step_chapter(+1)
                        self.play(start_index=0)

    # -- shutdown ---------------------------------------------------------------

    def _on_close(self):
        self._stop_session()
        self._save_position()
        self.root.destroy()


def main():
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.25)
    except tk.TclError:
        pass
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
