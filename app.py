"""AV Bible — reads the Bible (ESV) aloud with a per-verse visual stage.

Run with:  python app.py   (or double-click run.bat)
"""

import os
import queue
import subprocess
import sys
import threading
import time
import webbrowser
from concurrent.futures import ThreadPoolExecutor

import tkinter as tk
from tkinter import ttk

import audio_studio
import config
import svg_studio
from books import BOOK_NAMES, chapters_in
from passages import (Passage, PassageError, fetch_passage, fetch_esv_audio,
                      TRANSLATIONS, TRANSLATION_LABELS,
                      TRANSLATION_ATTRIBUTION)
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
    ('narration', sid)              whole-chapter ESV mp3 is playing
    ('done', sid, completed)        completed=False when stopped early
    """

    _next_sid = 0

    def __init__(self, events: queue.Queue, passage: Passage, start_index: int,
                 voice: str, rate: int, mode: str, api_key: str):
        super().__init__(daemon=True)
        PlaybackSession._next_sid += 1
        self.sid = PlaybackSession._next_sid
        self.events = events
        self.passage = passage
        self.start_index = max(0, min(start_index, len(passage.verses) - 1))
        self.voice = voice
        self.rate = rate
        self.mode = mode
        self.api_key = api_key
        self.player = AudioPlayer()
        self.paused = False
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

    def pause(self):
        self.paused = True
        self.player.pause()

    def resume(self):
        self.paused = False
        self.player.resume()

    def request_jump(self, index: int):
        if self.mode != "tts":
            return
        with self._jump_lock:
            self._jump = max(0, min(index, len(self.passage.verses) - 1))
        self.paused = False
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
            if mode in ("", "stopped") and not self.paused:
                return True
            time.sleep(0.06)
        return False

    # -- main loop ----------------------------------------------------------

    def run(self):
        try:
            if self.mode == "narration":
                self._run_narration()
            else:
                self._run_tts()
        except PassageError as e:
            self.emit("error", self.sid, str(e))
            self.emit("done", self.sid, False)
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

    def _run_narration(self):
        if not self.api_key.strip():
            raise PassageError(
                "ESV narration needs a free ESV API key — add one in Settings, "
                "or switch to Text-to-speech mode.")
        if self.passage.translation != "ESV":
            raise PassageError(
                "ESV narration plays the official ESV recording, so it is "
                "only offered with the ESV version selected. Switch Version "
                "to ESV or use Text-to-speech mode.")
        p = self.passage
        self.emit("status", self.sid,
                  f"Downloading ESV narration for {p.canonical}…")
        path = fetch_esv_audio(self.api_key.strip(), p.book, p.chapter)
        if self._stop.is_set():
            self.emit("done", self.sid, False)
            return
        self.emit("narration", self.sid)
        self.emit("status", self.sid, f"Playing ESV narration — {p.canonical}")
        completed = self._play_and_wait(path)
        self.emit("done", self.sid, completed and not self._stop.is_set())


# ---------------------------------------------------------------------------
# Settings dialog — currently dormant (ESV is removed from the version list
# for the proof of concept). Kept so ESV support can be re-enabled later by
# restoring the Settings button and the ESV entry in passages.TRANSLATIONS.
# ---------------------------------------------------------------------------

class SettingsDialog(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.title("Settings")
        self.resizable(False, False)
        self.transient(app.root)
        self.grab_set()

        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="ESV API key (free for personal use):").grid(
            row=0, column=0, columnspan=2, sticky="w")
        self.key_var = tk.StringVar(value=app.cfg.get("esv_api_key", ""))
        entry = ttk.Entry(frame, textvariable=self.key_var, width=52)
        entry.grid(row=1, column=0, columnspan=2, sticky="we", pady=(4, 8))
        entry.focus_set()

        link = ttk.Label(
            frame, foreground="#2255cc", cursor="hand2",
            text="Get a free key at api.esv.org (sign up → create application)")
        link.grid(row=2, column=0, columnspan=2, sticky="w")
        link.bind("<Button-1>", lambda e: webbrowser.open(
            "https://api.esv.org/account/create-application/"))

        ttk.Label(frame, foreground="#666666", wraplength=380, justify="left",
                  text=("Without a key the app plays the public-domain World "
                        "English Bible so you can try everything out. With a "
                        "key you get the ESV text plus the official ESV "
                        "narration mode.")).grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(8, 12))

        btns = ttk.Frame(frame)
        btns.grid(row=4, column=0, columnspan=2, sticky="e")
        ttk.Button(btns, text="Cancel", command=self.destroy).pack(
            side="right", padx=(6, 0))
        ttk.Button(btns, text="Save", command=self._save).pack(side="right")

    def _save(self):
        self.app.cfg["esv_api_key"] = self.key_var.get().strip()
        config.save(self.app.cfg)
        self.app.refresh_attribution()
        self.app.set_status("Settings saved.")
        self.destroy()


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.cfg = config.load()
        config.ensure_dirs()
        # Migrate configs saved when ESV (or another removed code) was
        # selectable.
        if self.cfg.get("translation") not in TRANSLATION_LABELS:
            self.cfg["translation"] = "WEB"

        self.events: queue.Queue = queue.Queue()
        self.session: PlaybackSession | None = None
        self.current_sid = 0
        self.passage: Passage | None = None
        self.fullscreen_stage: FullscreenStage | None = None
        self.audio_studio_win: tk.Toplevel | None = None
        self.svg_studio_win: tk.Toplevel | None = None
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

        ttk.Label(top, text="Version:").pack(side="left")
        self._label_to_code = {label: code for code, label, *_ in TRANSLATIONS}
        start_code = self.cfg.get("translation", "WEB")
        self.version_var = tk.StringVar(
            value=TRANSLATION_LABELS.get(start_code,
                                         TRANSLATION_LABELS["WEB"]))
        version_combo = ttk.Combobox(
            top, textvariable=self.version_var,
            values=[label for _, label, *_ in TRANSLATIONS],
            state="readonly", width=22)
        version_combo.pack(side="left", padx=(4, 14))
        version_combo.bind("<<ComboboxSelected>>", self._on_version_change)

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
        self.pause_btn = ttk.Button(bar, text="⏸ Pause",
                                    command=self.toggle_pause, state="disabled")
        self.pause_btn.pack(side="left", padx=(6, 0))
        self.stop_btn = ttk.Button(bar, text="⏹ Stop", command=self.stop,
                                   state="disabled")
        self.stop_btn.pack(side="left", padx=(6, 14))
        ttk.Button(bar, text="◀ Prev", command=self.prev_item).pack(side="left")
        ttk.Button(bar, text="Next ▶", command=self.next_item).pack(
            side="left", padx=(6, 14))

        self.auto_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(bar, text="Auto-continue",
                        variable=self.auto_var).pack(side="left")

        self.notes_var = tk.BooleanVar(value=bool(self.cfg.get("show_notes",
                                                               True)))
        ttk.Checkbutton(bar, text="Translator notes",
                        variable=self.notes_var,
                        command=self._on_display_toggle).pack(side="left",
                                                              padx=(14, 0))

        self.ref_var = tk.BooleanVar(
            value=bool(self.cfg.get("show_reference", True)))
        ttk.Checkbutton(bar, text="Reference",
                        variable=self.ref_var,
                        command=self._on_display_toggle).pack(side="left",
                                                              padx=(8, 0))

        ttk.Button(bar, text="🎨 SVG Studio",
                   command=self.open_svg_studio).pack(side="right", padx=(0, 6))
        ttk.Button(bar, text="🎙 Pronunciation Studio",
                   command=self.open_pronunciation_tool).pack(side="right", padx=(0, 6))
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
        self.text.tag_configure("hint", foreground="#888888",
                                font=("Georgia", 11, "italic"))

        stage_frame = ttk.Frame(main)
        self.stage_view = StageView(stage_frame, self.stage)
        self.stage_view.canvas.pack(fill="both", expand=True)
        main.add(stage_frame, weight=3)

        bottom = ttk.Frame(root, padding=(10, 2, 10, 6))
        bottom.pack(fill="x")
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(bottom, textvariable=self.status_var).pack(side="left")
        self.attr_var = tk.StringVar()
        ttk.Label(bottom, textvariable=self.attr_var, foreground="#777777",
                  font=("Segoe UI", 8)).pack(side="right")
        self.refresh_attribution()

        self._show_hint()

    def _show_hint(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("end", "Welcome to AV Bible\n", "title")
        self.text.insert(
            "end",
            "Pick a book, chapter, and version above, then press Play.\n\n"
            "While it reads, the current verse is highlighted here and its "
            "artwork is shown on the visual stage to the right. Click any "
            "verse to jump to it.\n\nAll six versions are public domain and "
            "need no setup. ASV and Darby include translator notes (words "
            "supplied for clarity) — turn on \"Show translator notes\" to "
            "see them on the display while the verse is read.",
            "hint")
        self.text.configure(state="disabled")

    # -- small UI helpers ----------------------------------------------------

    def set_status(self, msg: str):
        self.status_var.set(msg)

    def selected_translation(self) -> str:
        return self._label_to_code.get(self.version_var.get(), "WEB")

    def _on_version_change(self, _event=None):
        code = self.selected_translation()
        self.cfg["translation"] = code
        config.save(self.cfg)
        self.refresh_attribution()
        self.set_status(f"Version: {self.version_var.get()}")

    def _on_display_toggle(self):
        self.cfg["show_notes"] = bool(self.notes_var.get())
        self.cfg["show_reference"] = bool(self.ref_var.get())
        config.save(self.cfg)
        # Refresh the stage immediately if a verse is showing.
        ctx = self.stage.current
        if ctx is not None and self.passage is not None and ctx.verse:
            self.stage.show_verse(self._verse_context(ctx.index))

    def refresh_attribution(self):
        code = self.selected_translation()
        self.attr_var.set(TRANSLATION_ATTRIBUTION.get(code, ""))

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

    def open_settings(self):
        SettingsDialog(self)

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
        self.set_status(f"Fetching {book} {chapter}…")
        self.play_btn.configure(state="disabled")

        api_key = self.cfg.get("esv_api_key", "")
        translation = self.selected_translation()

        def worker():
            try:
                passage = fetch_passage(api_key, book, chapter, translation)
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
            mode="tts",
            api_key=self.cfg.get("esv_api_key", ""),
        )
        self.current_sid = self.session.sid
        self._save_position()
        self.session.start()
        self.play_btn.configure(state="normal")
        self.pause_btn.configure(state="normal", text="⏸ Pause")
        self.stop_btn.configure(state="normal")

    def _stop_session(self):
        if self.session and self.session.is_alive():
            self.session.stop()
        self.session = None
        self.current_sid = 0

    def stop(self):
        self._stop_session()
        self.pause_btn.configure(state="disabled", text="⏸ Pause")
        self.stop_btn.configure(state="disabled")
        self.set_status("Stopped.")

    def toggle_pause(self):
        if not (self.session and self.session.is_alive()):
            return
        if self.session.paused:
            self.session.resume()
            self.pause_btn.configure(text="⏸ Pause")
            self.set_status("Resumed.")
        else:
            self.session.pause()
            self.pause_btn.configure(text="▶ Resume")
            self.set_status("Paused.")

    def next_item(self):
        if self.session and self.session.is_alive() \
                and self.session.mode == "tts":
            idx = self._current_index()
            if idx is not None:
                self.session.request_jump(idx + 1)
            return
        self._step_chapter(+1)
        if self.session and self.session.is_alive():
            self.play()

    def prev_item(self):
        if self.session and self.session.is_alive() \
                and self.session.mode == "tts":
            idx = self._current_index()
            if idx is not None:
                self.session.request_jump(idx - 1)
            return
        self._step_chapter(-1)
        if self.session and self.session.is_alive():
            self.play()

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
            "translation": self.selected_translation(),
            "voice": self.voice_var.get(),
            "rate": int(self.rate_var.get()),
            "show_notes": bool(self.notes_var.get()),
            "show_reference": bool(self.ref_var.get()),
        })
        config.save(self.cfg)

    # -- passage rendering ----------------------------------------------------

    def _render_passage(self, passage: Passage):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("end",
                         f"{passage.canonical} ({passage.translation})\n",
                         "title")
        for idx, (num, verse_text) in enumerate(passage.verses):
            tag = f"verse{idx}"
            self.text.insert("end", f"{num} ", ("vnum", tag))
            self.text.insert("end", verse_text + "\n", (tag,))
            self.text.tag_bind(tag, "<Button-1>",
                               lambda e, i=idx: self._on_verse_click(i))
        self.text.configure(state="disabled")

    def _on_verse_click(self, idx: int):
        if self.session and self.session.is_alive() \
                and self.session.mode == "tts":
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
        notes = []
        if self.notes_var.get() and idx < len(p.notes or []):
            notes = p.notes[idx]
        return VerseContext(
            book=p.book, chapter=p.chapter, verse=num, text=verse_text,
            reference=f"{p.canonical}:{num}  ({p.translation})",
            index=idx, total=len(p.verses), translation=p.translation,
            notes=notes, show_reference=bool(self.ref_var.get()))

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
            self.stage.show_verse(self._verse_context(idx))
        elif kind in ("intro", "narration"):
            p = self.passage
            self._highlight_verse(None)
            self.stage.show_verse(VerseContext(
                book=p.book, chapter=p.chapter, verse=0, text="",
                reference=f"{p.canonical}  ({p.translation})",
                index=0, total=len(p.verses), translation=p.translation,
                show_reference=bool(self.ref_var.get())))
        elif kind == "done":
            completed = event[2]
            self.pause_btn.configure(state="disabled", text="⏸ Pause")
            self.stop_btn.configure(state="disabled")
            self.session = None
            self.current_sid = 0
            if completed and self.passage:
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
