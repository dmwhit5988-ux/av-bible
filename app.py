"""Theoria Studio — the PC authoring hub for the Theoria web app.

The main window holds the shared passage (Book, Chapter, Verse) and opens the
Studio's tools, which follow that passage. It also previews the passage: the
World English Bible read aloud in the house voice, with the per-verse SVG
stage (visual_stage.py). A Preview pane embedding the real web app is planned
to replace this player (ROADMAP.md, Studio).

Run with:  python app.py   (or double-click run.bat)
"""

import importlib
import os
import queue
import subprocess
import sys
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

import tkinter as tk
from tkinter import ttk, messagebox

import config
from books import BOOK_NAMES, chapters_in
from passages import (ATTRIBUTION, Passage, PassageError, load_chapter,
                      verse_numbers)
from tts_engine import HOUSE_RATE, HOUSE_VOICE, synthesize
from audio_player import AudioPlayer
from visual_stage import StageController, StageView, VerseContext

APP_TITLE = "Theoria Studio"
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(config.WEB_DIR, "icons", "icon-192.png")
ERROR_LOG = os.path.join(config.CACHE_DIR, "studio_error.log")


_LOG_LOCK = threading.Lock()  # worker threads log too (_on_thread_error)


def log_note(context: str, text: str) -> None:
    """Append an entry to cache/studio_error.log. run.bat starts the Studio
    with pythonw, which has no console to print it to."""
    if sys.stderr is not None:
        print(text, file=sys.stderr)
    try:
        with _LOG_LOCK:
            os.makedirs(config.CACHE_DIR, exist_ok=True)
            with open(ERROR_LOG, "a", encoding="utf-8") as f:
                f.write(f"--- {time.strftime('%Y-%m-%d %H:%M:%S')} {context}"
                        f"\n{text}\n")
    except OSError:
        pass


def log_error(context: str, exc: BaseException) -> None:
    """Append a traceback to cache/studio_error.log."""
    log_note(context, "".join(traceback.format_exception(exc)))


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------
#
# TOOLS = {key: (label, group, factory, kind)} drives both the grouped
# buttons and the Tools menu. A factory is called as
# factory(shell, toplevel, book, chapter, verse) and imports its module only
# then, so one broken tool can't stop the Studio starting; the failure is
# reported naming that tool.
#
# kind "window": a Toplevel in this process, returning the tool's App. The
# App follows the shared passage through two methods:
#   set_passage(book, chapter, verse=None, *, ask=False) -> bool
#       Move to that passage. False when it is busy, or when it has unsaved
#       edits and ask=False; with ask=True it asks before discarding them.
#   can_close() -> bool
#       True when the window may close now (it asks about unsaved edits or
#       work in progress).
# kind "process": a separate process (toplevel is None), returning its
# Popen. One copy at a time: the Pronunciation Studio and the Verifier each
# hold the whole pronunciations.json, and whichever saves last would win.

def _passage_tool(module):
    def factory(shell, top, book, chapter, verse):
        return importlib.import_module(module).App(
            top, book=book, chapter=chapter, verse=verse)
    return factory


def _open_coverage(shell, top, book, chapter, verse):
    # Coverage is the backlog: its "Go to chapter" sets the shared passage.
    return importlib.import_module("coverage_studio").App(
        top, book=book, chapter=chapter, verse=verse, goto=shell.go_to)


def _open_publish(shell, top, book, chapter, verse):
    return importlib.import_module("publish_studio").App(top)


def _spawn(script, *args):
    return subprocess.Popen(
        [sys.executable, os.path.join(REPO_ROOT, script), *args])


def _launch_pronunciation(shell, top, book, chapter, verse):
    return _spawn("pronunciation_tool.py", book, str(chapter))


def _launch_verifier(shell, top, book, chapter, verse):
    # No passage: the Verifier works across the whole pronunciations.json
    # list rather than one chapter's names.
    return _spawn("pronunciation_check.py")


TOOLS = {
    "coverage":      ("Coverage", "Plan", _open_coverage, "window"),
    "visuals":       ("Visuals", "Author", _passage_tool("svg_studio"),
                      "window"),
    "pronunciation": ("Pronunciation", "Author", _launch_pronunciation,
                      "process"),
    "verifier":      ("Verifier", "Author", _launch_verifier, "process"),
    "audio":         ("Audio", "Produce", _passage_tool("audio_studio"),
                      "window"),
    "video":         ("Video", "Produce", _passage_tool("video_studio"),
                      "window"),
    "publish":       ("Publish", "Ship", _open_publish, "window"),
}


# ---------------------------------------------------------------------------
# Playback session (worker thread)
# ---------------------------------------------------------------------------

class PlaybackSession(threading.Thread):
    """Plays one passage in the house voice. Emits events to the UI through
    a queue:

    ('status', sid, message)
    ('error', sid, message)
    ('verse', sid, index)           index into passage.verses
    ('intro', sid)                  chapter announcement is playing
    ('done', sid, completed)        completed=False when stopped early
    """

    _next_sid = 0

    def __init__(self, events: queue.Queue, passage: Passage, start_index: int):
        super().__init__(daemon=True)
        PlaybackSession._next_sid += 1
        self.sid = PlaybackSession._next_sid
        self.events = events
        self.passage = passage
        self.start_index = max(0, min(start_index, len(passage.verses) - 1))
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
        # Drop the verses queued ahead: the pool's threads aren't daemons,
        # so Python's exit would otherwise wait for every one to synthesize.
        self._executor.shutdown(wait=False, cancel_futures=True)

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
                        synthesize, text, HOUSE_VOICE, HOUSE_RATE)
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
                intro_path = synthesize(intro_text, HOUSE_VOICE, HOUSE_RATE)
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
        config.ensure_dirs()
        cfg = config.load()

        self.events: queue.Queue = queue.Queue()
        self.session: PlaybackSession | None = None
        self.current_sid = 0
        self.passage: Passage | None = None  # the chapter being played
        self.stage = StageController()
        self.windows: dict[str, tuple[tk.Toplevel, object]] = {}
        self.procs: dict[str, subprocess.Popen] = {}
        self._verses: list[int] = [1]  # WEB's verse numbers, this chapter
        self._load_seq = 0             # bumped per Play; stale loads ignored
        self._loading = False          # a chapter is loading to play
        self._counting = False         # a deploy-file count is running
        self._recount_again = False    # files changed while it ran
        self._asking_close = False     # _on_close is asking the tools
        self._closing = False

        self._build_ui(cfg)
        # The passage last saved and sent to the tools (_passage_changed).
        self._announced = self.selected_passage()
        root.bind("<<PassageChanged>>", self._on_passage_changed)
        root.report_callback_exception = self._on_callback_error
        root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._poll_events()
        root.after(500, self.recount_deploy_files)

    # -- UI construction ----------------------------------------------------

    def _build_ui(self, cfg: dict):
        root = self.root
        root.title(APP_TITLE)
        root.geometry("1180x700")
        root.minsize(900, 540)
        try:
            self._icon = tk.PhotoImage(file=ICON_PATH)
            root.iconphoto(True, self._icon)  # True: tool windows too
        except tk.TclError:
            pass  # a missing icon is cosmetic

        self._build_menu()

        # Passage bar, with the preview controls on the right.
        top = ttk.Frame(root, padding=(10, 8, 10, 4))
        top.pack(fill="x")

        ttk.Label(top, text="Book:").pack(side="left")
        book = cfg["last_book"]
        self.book_var = tk.StringVar(
            value=book if book in BOOK_NAMES else BOOK_NAMES[0])
        self.book_combo = ttk.Combobox(
            top, textvariable=self.book_var, values=BOOK_NAMES,
            state="readonly", width=15)
        self.book_combo.pack(side="left", padx=(4, 10))
        self.book_combo.bind("<<ComboboxSelected>>", self._on_book_change)

        ttk.Label(top, text="Chapter:").pack(side="left")
        self.chapter_var = tk.StringVar(value=str(cfg["last_chapter"]))
        self.chapter_combo = ttk.Combobox(
            top, textvariable=self.chapter_var, state="readonly", width=4)
        self.chapter_combo.pack(side="left", padx=(4, 10))
        self.chapter_combo.bind("<<ComboboxSelected>>",
                                self._on_chapter_change)

        ttk.Label(top, text="Verse:").pack(side="left")
        self.verse_var = tk.StringVar(value=str(cfg["last_verse"]))
        self.verse_combo = ttk.Combobox(
            top, textvariable=self.verse_var, state="readonly", width=4)
        self.verse_combo.pack(side="left", padx=(4, 8))
        self.verse_combo.bind("<<ComboboxSelected>>", self._on_verse_pick)
        self._refresh_chapters()
        self._refresh_verses()

        ttk.Button(top, text="◀", width=3,
                   command=lambda: self._go_chapter(-1)).pack(side="left")
        ttk.Button(top, text="▶", width=3,
                   command=lambda: self._go_chapter(+1)).pack(
            side="left", padx=(2, 0))

        transport = ttk.Frame(top)
        transport.pack(side="right")
        self.play_btn = ttk.Button(transport, text="▶ Play", width=7,
                                   command=self.play)
        self.play_btn.pack(side="left")
        self.stop_btn = ttk.Button(transport, text="⏹ Stop", width=7,
                                   command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=(4, 10))
        ttk.Button(transport, text="◀ Prev", width=7,
                   command=self.prev_item).pack(side="left")
        ttk.Button(transport, text="Next ▶", width=7,
                   command=self.next_item).pack(side="left", padx=(4, 0))

        # Tool bar: the registry's groups, Publish's deploy budget beside it.
        bar = ttk.Frame(root, padding=(10, 2, 10, 6))
        bar.pack(fill="x")
        groups = list(dict.fromkeys(group for _, group, _, _ in TOOLS.values()))
        for n, group in enumerate(groups):
            if n:
                ttk.Separator(bar, orient="vertical").pack(
                    side="left", fill="y", padx=8)
            ttk.Label(bar, text=f"{group}:", foreground="#777777").pack(
                side="left", padx=(0, 4))
            for key, (label, g, _factory, _kind) in TOOLS.items():
                if g == group:
                    ttk.Button(bar, text=label, width=0,
                               command=lambda k=key: self.open_tool(k)).pack(
                        side="left", padx=(0, 4))
        self.budget_var = tk.StringVar(value="Files …")
        self.budget_label = ttk.Label(bar, textvariable=self.budget_var,
                                      foreground="#555555", cursor="hand2")
        self.budget_label.pack(side="left", padx=(4, 0))
        self.budget_label.bind("<Button-1>",
                               lambda e: self.recount_deploy_files())

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

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        tools = tk.Menu(menubar, tearoff=False)
        last_group = None
        for key, (label, group, _factory, _kind) in TOOLS.items():
            if last_group is not None and group != last_group:
                tools.add_separator()
            last_group = group
            tools.add_command(label=label,
                              command=lambda k=key: self.open_tool(k))
        tools.add_separator()
        tools.add_command(label="Recount deploy files",
                          command=self.recount_deploy_files)
        menubar.add_cascade(label="Tools", menu=tools)
        self.root.configure(menu=menubar)

    # -- small UI helpers ----------------------------------------------------

    def set_status(self, msg: str):
        self.status_var.set(msg)

    def _on_callback_error(self, exc_type, exc, tb):
        """Errors in Tk callbacks, this window's or any tool window's, go to
        the error log and the status bar instead of a console nobody sees."""
        log_error("callback", exc)
        try:
            self.set_status(f"Error: {exc_type.__name__}: {exc} "
                            f"(details in {ERROR_LOG})")
        except tk.TclError:
            pass

    def _on_thread_error(self, args):
        """threading.excepthook (installed by _run): an exception escaping a
        worker thread, this window's or any tool's, goes to the error log,
        and to the status bar through the event queue, since only Tk's own
        thread may touch the window. Never blocks: the queue is unbounded."""
        if issubclass(args.exc_type, SystemExit):
            return  # the default hook ignores these too
        name = args.thread.name if args.thread is not None else "a thread"
        if args.exc_value is None:
            text = f"{args.exc_type.__name__}\n"
        else:
            text = "".join(traceback.format_exception(
                args.exc_type, args.exc_value, args.exc_traceback))
        log_note(f"thread {name}", text)
        self.events.put(("thread_error", name,
                         f"{args.exc_type.__name__}: {args.exc_value}"))

    # -- the shared passage ----------------------------------------------------

    def selected_passage(self) -> tuple[str, int, int]:
        """The pickers' passage, the verse clamped to one the chapter has."""
        return (self.book_var.get(), self._chapter(),
                self._clamp_verse(self._selected_verse_number()))

    def _clamp_verse(self, verse: int) -> int:
        """`verse` if the pickers' chapter has it, else the next verse it
        does have (its last verse, past the end)."""
        if verse in self._verses:
            return verse
        return next((v for v in self._verses if v >= verse), self._verses[-1])

    def _refresh_chapters(self):
        book = self.book_var.get()
        count = chapters_in(book)
        self.chapter_combo["values"] = [str(i) for i in range(1, count + 1)]
        if not (1 <= self._chapter() <= count):
            self.chapter_var.set("1")

    def _refresh_verses(self):
        """Fill the Verse picker with WEB's verse numbers for the chapter."""
        try:
            self._verses = list(verse_numbers(self.book_var.get(),
                                              self._chapter())) or [1]
        except PassageError:
            self._verses = [1]
        self.verse_combo["values"] = [str(v) for v in self._verses]
        verse = self._clamp_verse(self._selected_verse_number())
        if self.verse_var.get() != str(verse):
            self.verse_var.set(str(verse))

    def _chapter(self) -> int:
        try:
            return int(self.chapter_var.get())
        except ValueError:
            return 1

    def _selected_verse_number(self) -> int:
        try:
            return max(1, int(self.verse_var.get().strip()))
        except (ValueError, AttributeError):
            return 1

    def _on_book_change(self, _event=None):
        self._stop_for_move()
        self._set_passage(self.book_var.get(), 1, 1)

    def _on_chapter_change(self, _event=None):
        self._stop_for_move()
        self._set_passage(self.book_var.get(), self._chapter(), 1)

    def _on_verse_pick(self, _event=None):
        """A verse picked while its chapter plays is a jump, as in the web
        player; anything else stops playback and moves the passage."""
        p = self.passage
        if (self._playing() and p is not None
                and (self.book_var.get(), self._chapter())
                == (p.book, p.chapter)):
            self.session.request_jump(
                self._index_for_verse(p, self._selected_verse_number()))
            return
        self._stop_for_move()
        self._passage_changed()

    def _stop_for_move(self):
        """A passage move the user makes stops playback first, and a chapter
        still loading to play, as the web player does: the pickers then stay
        where the user put them."""
        if self._stop_session():
            self.stop_btn.configure(state="disabled")
            self.set_status("Stopped.")

    def _set_passage(self, book: str, chapter: int, verse: int = 1):
        self.book_var.set(book)
        self._refresh_chapters()
        self.chapter_var.set(str(chapter))
        self.verse_var.set(str(verse))
        self._refresh_verses()
        self._passage_changed()

    def _passage_changed(self):
        """Save the passage and tell the open tools (<<PassageChanged>>), once
        per actual change. The verse ticking along during playback is not a
        change; the verse playback stopped on is."""
        passage = self.selected_passage()
        book, chapter, verse = passage
        if self.verse_var.get() != str(verse):
            self.verse_var.set(str(verse))  # the clamped verse, shown
        if passage == self._announced:
            return
        self._announced = passage
        config.update(last_book=book, last_chapter=chapter, last_verse=verse)
        self.root.event_generate("<<PassageChanged>>", when="tail")

    def _on_passage_changed(self, _event=None):
        """Every open tool window follows unless it is busy or has unsaved
        edits; clicking its button later brings it over (asking first)."""
        book, chapter, verse = self.selected_passage()
        stayed = [TOOLS[key][0] for key, _top, app in self._open_windows()
                  if not self._tool_call(key, app, "set_passage", False,
                                         book, chapter, verse, ask=False)]
        if stayed:
            self.set_status(
                f"{', '.join(stayed)} stayed put (busy or unsaved edits); "
                f"click a tool's button to bring it to {book} {chapter}:{verse}.")

    def go_to(self, book: str, chapter: int):
        """Coverage's "Go to chapter": point the shared passage at a row."""
        if book not in BOOK_NAMES:
            return
        self._stop_for_move()
        self._set_passage(book, int(chapter), 1)
        self.root.deiconify()
        self.root.lift()
        self.set_status(f"Coverage: jumped to {book} {chapter} — "
                        f"press Play or open a tool.")

    @staticmethod
    def _neighbour_chapter(book: str, chapter: int, delta: int):
        """(book, chapter) one chapter before (delta -1) or after (+1),
        across book boundaries; None before Genesis 1 or after Revelation."""
        chapter += delta
        idx = BOOK_NAMES.index(book)
        if chapter < 1:
            if idx == 0:
                return None
            book = BOOK_NAMES[idx - 1]
            chapter = chapters_in(book)
        elif chapter > chapters_in(book):
            if idx == len(BOOK_NAMES) - 1:
                return None
            book = BOOK_NAMES[idx + 1]
            chapter = 1
        return book, chapter

    def _go_chapter(self, delta: int):
        """The ◀ ▶ buttons: the previous or next chapter, from verse 1."""
        target = self._neighbour_chapter(self.book_var.get(), self._chapter(),
                                         delta)
        if target:
            self._stop_for_move()
            self._set_passage(*target, 1)

    def _step_verse(self, delta: int):
        """Prev/Next while stopped: the previous or next verse, rolling into
        the neighbouring chapter at either end, as the web player does."""
        verse = self._selected_verse_number()
        i = self._verses.index(verse) + delta if verse in self._verses else 0
        if 0 <= i < len(self._verses):
            self.verse_var.set(str(self._verses[i]))
            self._passage_changed()
            return
        target = self._neighbour_chapter(self.book_var.get(), self._chapter(),
                                         delta)
        if target is None:
            return
        verse = 1
        if delta < 0:
            try:
                verse = verse_numbers(*target)[-1]
            except (PassageError, IndexError):
                pass
        self._set_passage(*target, verse)

    # -- tools ------------------------------------------------------------------

    def open_tool(self, key: str):
        """Open a tool on the shared passage, or bring an open one to it."""
        label, _group, factory, kind = TOOLS[key]
        book, chapter, verse = self.selected_passage()

        if kind == "process":
            proc = self.procs.get(key)
            if proc is not None and proc.poll() is None:
                self.set_status(
                    f"{label} is already running; switch to its window. (One "
                    f"copy at a time: two would overwrite each other's "
                    f"pronunciations.json edits.)")
                return
            try:
                self.procs[key] = factory(self, None, book, chapter, verse)
            except Exception as e:
                self._tool_failed(label, e)
                return
            self.set_status(f"{label} launched.")
            return

        entry = self.windows.get(key)
        if entry is not None and entry[0].winfo_exists():
            top, app = entry
            # Shown first, so a question set_passage asks (unsaved edits) is
            # never owned by a minimized or buried window.
            top.deiconify()
            top.lift()
            top.focus_force()
            moved = self._tool_call(key, app, "set_passage", False,
                                    book, chapter, verse, ask=True)
            if not moved:
                self.set_status(f"{label} kept its passage.")
            return

        top = tk.Toplevel(self.root)
        try:
            app = factory(self, top, book, chapter, verse)
        except Exception as e:
            top.destroy()
            self._tool_failed(label, e)
            return
        self.windows[key] = (top, app)
        top.bind("<Destroy>",
                 lambda e, k=key, t=top: self._on_tool_destroyed(k, t, e),
                 add="+")
        self.set_status(f"{label} opened.")

    def _open_windows(self):
        """[(key, toplevel, app)] for every tool window still open."""
        live = []
        for key, (top, app) in list(self.windows.items()):
            if top.winfo_exists():
                live.append((key, top, app))
            else:
                del self.windows[key]
        return live

    def _tool_call(self, key: str, app, method: str, default, *args, **kwargs):
        """Call one of a tool window's contract methods. A tool that lacks it
        or raises gets `default`; the error is logged, never raised."""
        try:
            return getattr(app, method)(*args, **kwargs)
        except Exception as e:
            label = TOOLS[key][0]
            log_error(f"{label}.{method}", e)
            self.set_status(f"{label}: {method} failed "
                            f"({type(e).__name__}: {e}).")
            return default

    def _tool_failed(self, label: str, exc: Exception):
        log_error(f"opening {label}", exc)
        self.set_status(f"{label} failed to open: {type(exc).__name__}: {exc}")
        messagebox.showerror(
            APP_TITLE,
            f"{label} could not open:\n\n{type(exc).__name__}: {exc}\n\n"
            f"The rest of the Studio still works. The full error is in "
            f"{ERROR_LOG}.", parent=self.root)

    def _on_tool_destroyed(self, key: str, top: tk.Toplevel, event):
        if str(event.widget) != str(top):
            return  # one of the window's own widgets
        if self.windows.get(key, (None,))[0] is top:
            del self.windows[key]
        # Any tool can change what Publish would deploy (Audio's and
        # Video's narration, SVG Studio's saves, a publish), so the meter
        # recounts whenever one closes.
        if not self._closing:
            self.recount_deploy_files()

    def recount_deploy_files(self):
        """Count the files Publish would deploy against the file limit of
        Cloudflare's Workers static assets (publish_studio's count and
        limit), on a worker thread (it walks web/, the site root)."""
        if self._counting:
            self._recount_again = True  # the running count may predate it
            return
        self._counting = True
        self.budget_var.set("Files: counting…")

        def worker():
            try:
                publish = importlib.import_module("publish_studio")
                self.events.put(("budget", publish.count_deploy_files(),
                                 publish.DEPLOY_FILE_LIMIT))
            except Exception as e:
                log_error("counting deploy files", e)
                self.events.put(("budget_error", f"{type(e).__name__}: {e}"))

        threading.Thread(target=worker, daemon=True).start()

    def _count_finished(self):
        self._counting = False
        if self._recount_again and not self._closing:
            self._recount_again = False
            self.recount_deploy_files()

    # -- transport controls --------------------------------------------------

    @staticmethod
    def _index_for_verse(passage: Passage, verse_number: int) -> int:
        for i, (num, _) in enumerate(passage.verses):
            if num >= verse_number:
                return i
        return len(passage.verses) - 1

    def play(self, start_index: int | None = None):
        self._stop_session()
        book, chapter, verse_number = self.selected_passage()
        self.set_status(f"Loading {book} {chapter}…")
        self.play_btn.configure(state="disabled")
        self._load_seq += 1
        self._loading = True
        seq = self._load_seq

        def worker():
            try:
                passage = load_chapter(book, chapter)
                self.events.put(("fetched", seq, passage, start_index,
                                 verse_number))
            except PassageError as e:
                self.events.put(("fetch_error", seq, str(e)))
            except Exception as e:
                self.events.put(("fetch_error", seq,
                                 f"Unexpected error: {e}"))

        threading.Thread(target=worker, daemon=True).start()

    def _start_session(self, passage: Passage, start: int):
        self.passage = passage
        self._render_passage(passage)
        # The pickers show what is playing (a move while the chapter loaded
        # cancelled the load, so this is where they already were).
        self._set_passage(passage.book, passage.chapter,
                          passage.verses[start][0])
        self.session = PlaybackSession(self.events, passage, start)
        self.current_sid = self.session.sid
        self.session.start()
        self.play_btn.configure(state="normal")
        self.stop_btn.configure(state="normal")

    def _playing(self) -> bool:
        return self.session is not None and self.session.is_alive()

    def _stop_session(self) -> bool:
        """Stop the playing session, and forget a chapter still loading to
        play. True when either was going."""
        # A session whose 'done' isn't handled yet counts: that event is
        # about to go stale, and with it the autoplay into the next chapter.
        was = self.session is not None or self._loading
        if self._playing():
            self.session.stop()
        self.session = None
        self.current_sid = 0
        if self._loading:
            self._loading = False
            self._load_seq += 1  # its 'fetched' is now stale
            self.play_btn.configure(state="normal")
        return was

    def stop(self):
        self._stop_session()
        self.stop_btn.configure(state="disabled")
        self.set_status("Stopped.")
        self._passage_changed()  # the tools catch up with the stopped verse

    def next_item(self):
        if self._playing():
            idx = self._current_index()
            if idx is not None:
                self.session.request_jump(idx + 1)
            return
        self._stop_for_move()  # a chapter loading to play
        self._step_verse(+1)

    def prev_item(self):
        if self._playing():
            idx = self._current_index()
            if idx is not None:
                self.session.request_jump(idx - 1)
            return
        self._stop_for_move()
        self._step_verse(-1)

    def _current_index(self):
        ctx = self.stage.current
        if ctx is None or self.passage is None:
            return None
        return ctx.index

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
        if self._playing():
            self.session.request_jump(idx)
            return
        # The text shows the chapter last played, which the pickers may have
        # left since; play that one, from the verse clicked.
        p = self.passage
        self._set_passage(p.book, p.chapter, p.verses[idx][0])
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
        return VerseContext(book=p.book, chapter=p.chapter,
                            verse=p.verses[idx][0], index=idx)

    # -- event pump ------------------------------------------------------------

    def _poll_events(self):
        while True:
            try:
                event = self.events.get_nowait()
            except queue.Empty:
                break
            try:
                self._handle_event(event)
            except Exception as e:  # one bad event mustn't stop the pump
                self._on_callback_error(type(e), e, e.__traceback__)
        self.root.after(60, self._poll_events)

    def _handle_event(self, event):
        kind = event[0]

        if kind in ("fetched", "fetch_error"):
            if event[1] != self._load_seq:
                return  # a load since stopped by a move, Stop or close
            self._loading = False
            if kind == "fetch_error":
                self.play_btn.configure(state="normal")
                self.set_status(event[2])
                return
            _, _seq, passage, start_index, verse_number = event
            if start_index is None:
                start_index = self._index_for_verse(passage, verse_number)
            self._start_session(passage, start_index)
            return
        if kind == "thread_error":
            _, name, message = event
            self.set_status(f"Error in {name}: {message} "
                            f"(details in {ERROR_LOG})")
            return
        if kind == "budget":
            _, count, limit = event
            self.budget_var.set(f"Files {count:,} / {limit:,}")
            self.budget_label.configure(
                foreground="#b00020" if count > limit else
                "#a06000" if count > 0.9 * limit else "#555555")
            self._count_finished()
            return
        if kind == "budget_error":
            self.budget_var.set("Files ?")
            self.set_status(f"Could not count the deploy files: {event[1]}")
            self._count_finished()
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
            p = self.passage
            self._highlight_verse(idx)
            # Track playback in the verse dropdown (like the web app),
            # so Stop followed by Play resumes from the verse being
            # read instead of restarting the chapter. Only while the
            # pickers show the chapter playing: this verse number means
            # nothing in another chapter.
            if (self.book_var.get(), self._chapter()) == (p.book, p.chapter):
                self.verse_var.set(str(p.verses[idx][0]))
            self.stage.show_verse(self._verse_context(idx))
        elif kind == "intro":
            p = self.passage
            self._highlight_verse(None)
            self.stage.show_verse(VerseContext(
                book=p.book, chapter=p.chapter, verse=0, index=0))
        elif kind == "done":
            completed = event[2]
            self.stop_btn.configure(state="disabled")
            self.session = None
            self.current_sid = 0
            if completed and self.passage:
                p = self.passage
                self.set_status(f"Finished {p.canonical}.")
                # Like the web player, play on into the next chapter, and
                # stop after Revelation (back at the top of its last
                # chapter, as a finished chapter always is).
                target = self._neighbour_chapter(p.book, p.chapter, +1)
                if target:
                    self._set_passage(*target, 1)
                    self.play(start_index=0)
                else:
                    self._set_passage(p.book, p.chapter, 1)

    # -- shutdown ---------------------------------------------------------------

    def _on_close(self):
        """Each open tool window may veto (unsaved edits, a render or a push
        in progress); one "no" keeps the Studio open. After every yes, the
        tool windows go first, which cancels their renders, then this one.
        The Pronunciation and Verifier processes are left running."""
        if self._asking_close or self._closing:
            return  # a second click while a tool's question is open
        self._asking_close = True
        try:
            tools = self._open_windows()
            for key, top, app in tools:
                if not top.winfo_exists():
                    continue  # closed by hand while another tool asked
                # Shown first, so its question is never owned by a
                # minimized window.
                top.deiconify()
                top.lift()
                if not self._tool_call(key, app, "can_close", True):
                    self.set_status(f"Close cancelled by {TOOLS[key][0]}.")
                    return
        finally:
            self._asking_close = False
        self._closing = True
        self._stop_session()
        book, chapter, verse = self.selected_passage()
        config.update(last_book=book, last_chapter=chapter, last_verse=verse)
        # Only Audio's and Video's renders outlive their window (their
        # threads aren't daemons); the other tools' work just stops.
        busy = [TOOLS[key][0] for key, _top, app in tools
                if key in ("audio", "video") and self._tool_busy(app)]
        if busy:
            # Their render threads aren't daemons: the process stays until
            # each finishes the verse (or step) it is on.
            note = (f"Stopping renders… ({', '.join(busy)}: each finishes "
                    f"its current step first)")
            self.set_status(note)
            log_note("closing", note)
            try:
                self.root.update_idletasks()
            except tk.TclError:
                pass
        # Destroying a tool's window sets its cancel flag (its <Destroy>
        # handler); the window going needs nothing from the render itself.
        for key, top, _app in tools:
            try:
                top.destroy()
            except tk.TclError:
                pass  # already gone
        self.root.destroy()

    @staticmethod
    def _tool_busy(app) -> bool:
        try:
            return bool(getattr(app, "busy", False))
        except Exception:
            return False


def _run():
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.25)
    except tk.TclError:
        pass
    try:
        app = App(root)
    except BaseException:
        root.destroy()
        raise
    # Worker threads' uncaught exceptions (playback, counts, every tool's
    # renders) would otherwise go to pythonw's missing console. Left in
    # place after the window closes: renders finishing their last verse
    # still log.
    threading.excepthook = app._on_thread_error
    # A settings write that fails (config.json locked or read-only) would
    # otherwise only print to the console pythonw doesn't have.
    config.warn_hook = lambda text: log_note("config", text)
    root.mainloop()


def main() -> int:
    """Start the Studio. A failure is written to cache/studio_error.log and
    shown in a message box: run.bat uses pythonw, which has no console."""
    try:
        _run()
    except Exception as e:
        log_error("startup", e)
        try:
            messagebox.showerror(
                APP_TITLE,
                f"{APP_TITLE} could not start:\n\n{type(e).__name__}: {e}"
                f"\n\nThe full error is in {ERROR_LOG}.")
        except tk.TclError:
            pass
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
