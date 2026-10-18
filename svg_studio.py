"""SVG Studio — verse-aware orchestrator for the visuals pipeline.

The studio owns the verse workflow (navigate, know when a file is
generator-owned), the XML editing pane, and the pipeline glue (save into
web/visuals/<Book>/<chapter>/, manifest rebuild). Deploying is Publish's job
(publish_studio.py). It deliberately does NOT own vector drawing — that is
the XML pane and/or Inkscape (docs/svg-studio.md, "Option 3").

Usable standalone or as a Toplevel from app.py, with the same window-tool
contract as the other studios: App(root, book, chapter, verse),
set_passage() to follow the main window's passage, and can_close() before
the window goes.

    python svg_studio.py [Book] [chapter]
"""

import datetime
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import tkinter as tk
import webbrowser
import xml.etree.ElementTree as ET
from tkinter import ttk, messagebox

import books
import config
import svg_freeze
import svg_preview
import svg_registry

# How soon a preview-subprocess exit counts as "pywebview is broken" rather
# than "the user closed the window" (docs/svg-studio.md section 2.5).
EMBEDDED_FAIL_WINDOW_MS = 10_000

# One-off hand edits to generator-owned files get flagged with this so the
# pre-regeneration scan can warn before clobbering them. Informational —
# nothing blocks (detect and route, never block).
HAND_EDIT_MARK = "<!-- hand-edited"

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
VISUALS_DIR = config.VISUALS_DIR
MANIFEST_PATH = os.path.join(VISUALS_DIR, "manifest.json")

# House canvas size (generate_tabernacle.W/H — not imported: that module
# loads PIL fonts at import time, which the studio doesn't need).
CANVAS_W, CANVAS_H = 1024, 576
FONT_FAMILY = "Georgia, 'Times New Roman', serif"

SKELETON = (
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
    f'width="{CANVAS_W}" height="{CANVAS_H}" '
    f'font-family="{FONT_FAMILY}">\n'
    f'<rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'fill="rgb(16,16,24)"/>\n'
    f'<!-- draw here -->\n'
    f'</svg>\n'
)


def pretty_svg(text: str) -> str:
    """Indent single-line generator output for the editor pane. Preserves
    comments (the hand-edited marker!) and element text; returns the input
    unchanged when it doesn't parse. Whitespace between SVG elements is
    insignificant, so the rendered result is identical."""
    try:
        parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
        root = ET.fromstring(text, parser=parser)
    except ET.ParseError:
        return text
    ET.indent(root)
    out = ET.tostring(root, encoding="unicode")
    return out if out.endswith("\n") else out + "\n"


def verse_base(book: str, chapter: int, verse: int) -> str:
    return f"{book.replace(' ', '_')}_{chapter}_{verse}"


def chapter_dir(book: str, chapter: int) -> str:
    return os.path.join(VISUALS_DIR, book.replace(" ", "_"), str(chapter))


def verse_path(book: str, chapter: int, verse: int) -> str:
    """The verse's one SVG: web/visuals/<Book>/<ch>/<Book>_<ch>_<v>.svg."""
    return os.path.join(chapter_dir(book, chapter),
                        f"{verse_base(book, chapter, verse)}.svg")


class App:
    def __init__(self, root, book=None, chapter=None, verse=None):
        self.root = root
        self.family: svg_registry.FamilyInfo | None = None
        self.current_path: str | None = None
        self._loaded = None     # (book, chapter, verse) the pane holds
        self.dirty = False
        self.editable = False
        self._loading = False   # suppress dirty-marking while loading the pane
        self.preview_server: svg_preview.PreviewServer | None = None
        self._edit_debounce = None  # after() id for debounced preview pushes
        self._preview_proc: subprocess.Popen | None = None
        self._embedded_deaths = 0   # early exits this session (2 = give up)
        self._hand_edit_mode = False  # unlocked a generator-owned file
        self.busy = False             # a generator re-run is in flight
        self.events: queue.Queue = queue.Queue()

        root.title("SVG Studio")
        root.geometry("980x640")
        root.minsize(820, 520)
        root.protocol("WM_DELETE_WINDOW", self._on_close)
        # The shell may destroy this window itself (closing the main window),
        # so the preview cleanup hangs off <Destroy>, not the close button.
        root.bind("<Destroy>", self._on_destroy, add="+")

        self._build_ui()

        if book not in books.BOOK_NAMES:
            book, chapter, verse = "Genesis", 1, 1
        self._show_selection(book, chapter, verse)
        self._load_selection()
        self._poll_events()

    # ----- UI construction --------------------------------------------------

    def _build_ui(self):
        nav = ttk.Frame(self.root, padding=(10, 10, 10, 4))
        nav.pack(fill="x")

        ttk.Label(nav, text="Book:").pack(side="left")
        self.book_var = tk.StringVar()
        self.book_cb = ttk.Combobox(nav, textvariable=self.book_var, width=16,
                                    state="readonly", values=books.BOOK_NAMES)
        self.book_cb.pack(side="left", padx=(4, 12))
        self.book_cb.bind("<<ComboboxSelected>>",
                          lambda e: self._on_book_change())

        ttk.Label(nav, text="Chapter:").pack(side="left")
        self.chapter_var = tk.StringVar()
        self.chapter_cb = ttk.Combobox(nav, textvariable=self.chapter_var,
                                       width=4, state="readonly")
        self.chapter_cb.pack(side="left", padx=(4, 12))
        self.chapter_cb.bind("<<ComboboxSelected>>",
                             lambda e: self._on_selection_change())

        ttk.Label(nav, text="Verse:").pack(side="left")
        self.verse_var = tk.StringVar(value="1")
        verse_sb = ttk.Spinbox(nav, textvariable=self.verse_var, width=5,
                               from_=1, to=176,
                               command=self._on_selection_change)
        verse_sb.pack(side="left", padx=(4, 12))
        verse_sb.bind("<Return>", lambda e: self._on_selection_change())
        verse_sb.bind("<FocusOut>", lambda e: self._on_selection_change())

        # Generator-ownership banner — hidden for hand-authored verses.
        self.banner = ttk.Frame(self.root, padding=(10, 6))
        self.banner_var = tk.StringVar()
        ttk.Label(self.banner, textvariable=self.banner_var,
                  foreground="#b8860b", wraplength=700,
                  justify="left").pack(side="left")
        self.banner_btns = ttk.Frame(self.banner)
        self.banner_btns.pack(side="right")
        self.edit_spec_btn = ttk.Button(self.banner_btns,
                                        text="Edit spec (durable)",
                                        command=self.edit_spec)
        self.edit_spec_btn.pack(side="left", padx=(6, 0))
        self.rerun_btn = ttk.Button(self.banner_btns, text="Re-run generator",
                                    command=self.rerun_generator)
        self.rerun_btn.pack(side="left", padx=(6, 0))
        self.hand_edit_btn = ttk.Button(self.banner_btns,
                                        text="Hand-edit anyway (one-off)",
                                        command=self.hand_edit_anyway)
        self.hand_edit_btn.pack(side="left", padx=(6, 0))

        # Main split: XML pane left, actions right.
        body = ttk.Frame(self.root, padding=(10, 6))
        body.pack(fill="both", expand=True)

        pane_frame = ttk.Frame(body)
        pane_frame.pack(side="left", fill="both", expand=True)
        ttk.Label(pane_frame, foreground="#888888",
                  text="SVG source (XML). The graphic itself renders in the "
                       "preview window — tkinter cannot display SVG/SMIL."
                  ).grid(row=0, column=0, sticky="w", pady=(0, 3))
        self.text = tk.Text(pane_frame, wrap="none", undo=True,
                            font=("Consolas", 10), background="#101018",
                            foreground="#e8e0cc", insertbackground="#e8e0cc")
        ys = ttk.Scrollbar(pane_frame, orient="vertical",
                           command=self.text.yview)
        xs = ttk.Scrollbar(pane_frame, orient="horizontal",
                           command=self.text.xview)
        self.text.configure(yscrollcommand=ys.set, xscrollcommand=xs.set)
        self.text.grid(row=1, column=0, sticky="nsew")
        ys.grid(row=1, column=1, sticky="ns")
        xs.grid(row=2, column=0, sticky="ew")
        pane_frame.rowconfigure(1, weight=1)
        pane_frame.columnconfigure(0, weight=1)
        self.text.bind("<<Modified>>", self._on_text_modified)
        self.text.bind("<Control-s>", lambda e: (self.save(), "break")[1])

        actions = ttk.Frame(body, padding=(10, 0, 0, 0))
        actions.pack(side="right", fill="y")
        self.preview_btn = ttk.Button(actions, text="Open preview",
                                      command=self.open_preview)
        self.preview_btn.pack(fill="x", pady=(0, 6))
        self.replay_btn = ttk.Button(actions, text="Replay ▶",
                                     command=self.replay)
        self.replay_btn.pack(fill="x", pady=(0, 6))
        self.continue_btn = ttk.Button(actions,
                                       text="Start from prev. frame",
                                       command=self.start_from_previous)
        self.continue_btn.pack(fill="x", pady=(0, 6))
        ttk.Button(actions, text="Open in Inkscape",
                   command=self.open_in_inkscape).pack(fill="x", pady=(0, 6))
        ttk.Button(actions, text="Reload from disk",
                   command=self.reload_from_disk).pack(fill="x", pady=(0, 6))
        ttk.Separator(actions).pack(fill="x", pady=6)
        self.save_btn = ttk.Button(actions, text="Save + manifest",
                                   command=self.save_and_manifest)
        self.save_btn.pack(fill="x", pady=(0, 6))
        ttk.Button(actions, text="Save only", command=self.save).pack(
            fill="x", pady=(0, 6))
        # "Try embedded preview again" escape hatch: once pywebview fails,
        # the studio persists browser mode and skips re-probing; unticking
        # and re-ticking this clears that record.
        self.embedded_var = tk.BooleanVar(
            value=config.load().get("svg_preview_host",
                                    "embedded") == "embedded")
        ttk.Checkbutton(actions, text="Preview in own window",
                        variable=self.embedded_var,
                        command=self._on_embedded_toggle).pack(
            fill="x", pady=(12, 0))
        ttk.Label(actions, foreground="#888888", wraplength=160,
                  justify="left",
                  text="Unticked: preview opens in your web browser "
                       "instead.").pack(fill="x", pady=(2, 0))

        # Status line.
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(self.root, textvariable=self.status_var, wraplength=900,
                  justify="left", padding=(10, 4)).pack(anchor="w")

    # ----- navigation --------------------------------------------------------

    def _on_book_change(self):
        self._fill_chapters()
        self._on_selection_change()

    def _fill_chapters(self, keep_chapter=None):
        n = books.chapters_in(self.book_var.get())
        values = [str(i) for i in range(1, n + 1)]
        self.chapter_cb.configure(values=values)
        wanted = str(keep_chapter) if keep_chapter else self.chapter_var.get()
        self.chapter_var.set(wanted if wanted in values else "1")

    def _show_selection(self, book, chapter, verse):
        """Point the pickers at book chapter:verse without loading it."""
        self.book_var.set(book)
        self._fill_chapters(keep_chapter=chapter)
        self.verse_var.set(str(max(1, int(verse or 1))))

    def _selection(self):
        book = self.book_var.get()
        try:
            chapter = int(self.chapter_var.get())
        except ValueError:
            chapter = 1
        try:
            verse = max(1, int(self.verse_var.get()))
        except ValueError:
            verse = 1
        return book, chapter, verse

    def _confirm_discard(self) -> bool:
        if not self.dirty:
            return True
        base = os.path.basename(self.current_path or "") or "this verse"
        return messagebox.askyesno(
            "SVG Studio", f"Discard unsaved changes to {base}?",
            icon="warning", parent=self.root)

    def _on_selection_change(self):
        """A picker moved. Load the verse it names, unless that verse is
        already loaded; if the user keeps unsaved edits instead, put the
        pickers back so they still name the verse in the pane."""
        if self._selection() == self._loaded:
            return
        if not self._confirm_discard():
            self._show_selection(*self._loaded)
            return
        self._load_selection()

    def set_passage(self, book, chapter, verse=None, *, ask=False) -> bool:
        """Move to book chapter:verse; verse None means verse 1 of a new
        chapter, or the current verse of this one. Stays put and returns
        False while a generator runs, or while the pane has unsaved edits
        that the user keeps (ask=True) or wasn't asked about (ask=False)."""
        if book not in books.BOOK_NAMES:
            return False
        chapter = max(1, min(int(chapter or 1), books.chapters_in(book)))
        if verse is None:
            same = self._loaded and self._loaded[:2] == (book, chapter)
            verse = self._loaded[2] if same else 1
        target = (book, chapter, max(1, int(verse)))
        if target == self._loaded:
            return True
        where = f"{book} {chapter}:{target[2]}"
        if self.busy:
            if ask:  # following quietly keeps the generator's progress shown
                self.status_var.set(f"A generator is running — not moving "
                                    f"to {where} yet.")
            return False
        if self.dirty and not (ask and self._confirm_discard()):
            self.status_var.set(f"Not moving to {where} — the pane has "
                                f"unsaved edits.")
            return False
        self._show_selection(*target)
        # Following the main window on its own (ask=False) swaps the preview
        # quietly: a 'nav' would start this verse's narration over whatever
        # the main window is playing. An explicit re-click may narrate.
        self._load_selection("nav" if ask else "edit")
        return True

    def _load_selection(self, cause="nav"):
        """Load the verse the pickers name (unsaved edits already settled)
        and push it to the preview with cause: 'nav' plays its narration,
        'edit' swaps the picture silently."""
        book, chapter, verse = self._selection()
        self._loaded = (book, chapter, verse)
        self.family = svg_registry.owner_of(book, chapter, verse)
        self._update_banner()
        # Generator families build cumulatively from their spec already —
        # freeze-and-continue is a hand-authoring affordance only.
        self.continue_btn.configure(
            state="disabled" if self.family is not None else "normal")
        self._load_selected_file()
        self._push_preview(cause)

    def _update_banner(self):
        if self.family is None:
            self.banner.pack_forget()
            return
        self.banner_var.set(
            f"⚙ Generated by {self.family.generator} — the Python spec is "
            f"the source of truth; hand edits are lost on regeneration. "
            f"Spec: " + "; ".join(
                f"{p.file} ({p.edit})" for p in self.family.spec))
        self.banner.pack(fill="x", before=self.text.master.master)

    # ----- pane load/save ----------------------------------------------------

    def _set_pane(self, content: str, editable: bool):
        self._loading = True
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", pretty_svg(content))
        self.text.edit_reset()
        self.text.edit_modified(False)
        if not editable:
            self.text.configure(state="disabled")
        self.editable = editable
        self.dirty = False
        self._loading = False
        self._update_title()

    def _load_selected_file(self):
        book, chapter, verse = self._loaded
        path = verse_path(book, chapter, verse)
        self.current_path = path
        self._hand_edit_mode = False
        base = os.path.basename(path)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                content = f.read()
            marked = HAND_EDIT_MARK in content
            if self.family is not None:
                # Generator-owned: read-only until "Hand-edit anyway" —
                # routing beats blocking, but accidental edits shouldn't be
                # the default.
                self._set_pane(content, editable=False)
                note = (" ⚠ has one-off hand edits — a re-run discards them."
                        if marked else "")
                self.status_var.set(
                    f"{base} — generator-owned ({self.family.label}); "
                    f"pane is read-only.{note}")
            else:
                self._set_pane(content, editable=True)
                self.status_var.set(f"{base} — loaded.")
        else:
            self._set_pane(SKELETON, editable=True)
            self.status_var.set(
                f"{base} — no file yet; skeleton loaded, Save creates "
                f"it. (Or: Start from prev. frame.)")

    def _on_text_modified(self, _event):
        if self._loading:
            self.text.edit_modified(False)
            return
        if self.text.edit_modified():
            self.dirty = True
            self._update_title()
            self.text.edit_modified(False)
            # Debounced live-reload push: silent re-inject (no narration
            # restart) so the preview follows keystrokes without stutter.
            if self._edit_debounce is not None:
                self.root.after_cancel(self._edit_debounce)
            self._edit_debounce = self.root.after(
                400, lambda: self._push_preview("edit"))

    def _update_title(self):
        base = os.path.basename(self.current_path or "")
        mark = " •" if self.dirty else ""
        self.root.title(f"SVG Studio — {base}{mark}" if base else "SVG Studio")

    def pane_text(self) -> str:
        return self.text.get("1.0", "end-1c")

    def save(self):
        if not self.editable:
            self.status_var.set("Pane is read-only — nothing saved.")
            return
        if not self.current_path:
            return
        content = self.pane_text()
        try:
            ET.fromstring(content)
        except ET.ParseError as e:
            if not messagebox.askyesno(
                    "SVG Studio",
                    f"The XML does not parse:\n\n{e}\n\nSave anyway?",
                    icon="warning", parent=self.root):
                self.status_var.set(f"Not saved — XML error: {e}")
                return
        if self._hand_edit_mode and HAND_EDIT_MARK not in content:
            # Flag the one-off so the pre-regeneration scan can warn before
            # the generator clobbers it. Insert right after the <svg …> tag.
            gt = content.find(">", content.find("<svg"))
            if gt != -1:
                today = datetime.date.today().isoformat()
                marker = (f"{HAND_EDIT_MARK} {today}; regenerating via "
                          f"{self.family.generator if self.family else '?'} "
                          f"will discard this -->")
                content = content[:gt + 1] + marker + content[gt + 1:]
                self._set_pane(content, editable=True)
                self.dirty = False
        os.makedirs(os.path.dirname(self.current_path), exist_ok=True)
        with open(self.current_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        self.dirty = False
        self._update_title()
        self.status_var.set(f"Saved {os.path.basename(self.current_path)}.")

    # ----- generator routing -------------------------------------------------

    def edit_spec(self):
        """Open the family's spec file(s) in the user's editor — the durable
        way to change a generated visual. Honors an optional "editor"
        command template in config.json (e.g. "code -g {file}"); falls back
        to the OS file association."""
        if self.family is None:
            return
        editor = config.load().get("editor")
        opened = []
        for pointer in self.family.spec:
            path = os.path.join(REPO_ROOT, pointer.file)
            try:
                if editor:
                    subprocess.Popen(editor.format(file=path), shell=True)
                else:
                    os.startfile(path)
                opened.append(f"{pointer.file} — {pointer.edit}")
            except OSError as e:
                self.status_var.set(f"Could not open {pointer.file}: {e}")
                return
        self.status_var.set(
            "Editing spec: " + " | ".join(opened) +
            " — Re-run generator when done.")

    def _marked_files_in_family(self) -> list:
        """One-off hand-edited files a re-run would clobber."""
        if self.family is None:
            return []
        marked = []
        for chapter in self.family.chapters:
            d = chapter_dir(self.family.book, chapter)
            if not os.path.isdir(d):
                continue
            for name in sorted(os.listdir(d)):
                if not name.endswith(".svg"):
                    continue
                path = os.path.join(d, name)
                try:
                    with open(path, encoding="utf-8") as f:
                        head = f.read(4096)
                except OSError:
                    continue
                if HAND_EDIT_MARK in head:
                    marked.append(name)
        return marked

    def rerun_generator(self):
        if self.family is None or self.busy:
            return
        if not self._confirm_discard():
            return
        marked = self._marked_files_in_family()
        note = ""
        if marked:
            shown = ", ".join(marked[:6]) + ("…" if len(marked) > 6 else "")
            note = (f"\n\n⚠ {len(marked)} file(s) carry one-off hand edits "
                    f"that will be DISCARDED:\n{shown}\n")
        if not messagebox.askyesno(
                "Re-run generator",
                f"Run {self.family.generator}? It rewrites every "
                f"{self.family.label} SVG from the Python spec.{note}"
                f"\nContinue?",
                icon="warning" if marked else "question", parent=self.root):
            return
        self.busy = True
        self.rerun_btn.configure(state="disabled")
        self.status_var.set(f"Running {self.family.generator}…")
        threading.Thread(target=self._rerun_worker,
                         args=(self.family.generator,), daemon=True).start()

    def _rerun_worker(self, generator):
        try:
            proc = subprocess.Popen(
                [sys.executable, os.path.join(REPO_ROOT, generator)],
                cwd=REPO_ROOT, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True,
                encoding="utf-8", errors="replace")
            for line in proc.stdout:
                line = line.strip()
                if line:
                    self.events.put(("rerun_line", line))
            code = proc.wait()
        except OSError as e:
            self.events.put(("rerun_done", 1, str(e)))
            return
        self.events.put(("rerun_done", code, ""))

    # ----- event pump (worker thread -> UI thread) ---------------------------

    def _poll_events(self):
        try:
            while True:
                self._handle_event(self.events.get_nowait())
        except queue.Empty:
            pass
        if self.root.winfo_exists():
            self.root.after(100, self._poll_events)

    def _handle_event(self, event):
        kind = event[0]
        if kind == "rerun_line":
            self.status_var.set(event[1])
        elif kind == "rerun_done":
            _, code, err = event
            self.busy = False
            self.rerun_btn.configure(state="normal")
            if code != 0:
                self.status_var.set(
                    f"Generator failed (exit {code}) {err} — see console.")
            elif self.dirty:
                # Edits made in the pane while it ran stay; reloading would
                # silently throw them away.
                self.status_var.set(
                    "Generator finished — the pane has unsaved edits, so it "
                    "was not reloaded (Reload from disk shows the new file).")
            else:
                self._load_selected_file()
                self._push_preview("nav")
                self.status_var.set(
                    "Generator finished — file reloaded from disk.")
        elif kind == "manifest_done":
            self.status_var.set(event[1])

    def hand_edit_anyway(self):
        """Unlock the pane on a generator-owned file. The save path stamps a
        hand-edited marker so a later re-run warns before discarding it."""
        if self.family is None or self.editable:
            return
        self.text.configure(state="normal")
        self.editable = True
        self._hand_edit_mode = True
        self.status_var.set(
            f"Hand-edit mode: your changes are a one-off — re-running "
            f"{self.family.generator} will discard them. Save stamps the "
            f"file so the re-run confirm warns first.")

    # ----- freeze and continue ------------------------------------------------

    def start_from_previous(self):
        """Load verse N-1's file, freeze its play-once animations to their
        end state, demote to a static base group, and put the result in the
        pane as verse N's unsaved starting point."""
        if self.family is not None:
            self.status_var.set(
                "This family is generated; the generator already carries "
                "state between verses. Edit the spec instead.")
            return
        book, chapter, verse = self._loaded
        if verse < 2:
            self.status_var.set("Verse 1 has no previous verse to "
                                "continue from.")
            return
        if not self._confirm_discard():
            return
        prev_path = verse_path(book, chapter, verse - 1)
        if not os.path.exists(prev_path):
            self.status_var.set(
                f"No SVG exists for {book} {chapter}:{verse - 1} to "
                f"continue from.")
            return
        with open(prev_path, encoding="utf-8") as f:
            prev_text = f.read()
        from_key = verse_base(book, chapter, verse - 1)
        result = svg_freeze.freeze_to_base(prev_text, from_key,
                                           new_verse=verse)
        self._set_pane(result.svg_text, editable=True)
        self.dirty = True
        self._update_title()
        self._push_preview("nav")
        note = (f" — {len(result.warnings)} warning(s): "
                + " | ".join(result.warnings) if result.warnings else "")
        self.status_var.set(
            f"Started from {os.path.basename(prev_path)}'s final frame — "
            f"unsaved; add verse {verse}'s elements in the overlay "
            f"group{note}")

    # ----- preview -----------------------------------------------------------

    def _push_preview(self, cause: str):
        """Publish the pane's current text to the preview server. cause is
        'nav' (restart narration too) or 'edit' (silent re-inject)."""
        if self.preview_server is None:
            return
        book, chapter, verse = self._loaded
        audio = svg_preview.resolve_audio(book, chapter, verse)
        # XML validity feedback without blocking the live preview — the
        # browser shows whatever it gets, which is honest live feedback.
        parse_note = ""
        try:
            ET.fromstring(self.pane_text())
        except ET.ParseError as e:
            parse_note = f" — XML error: {e}"
        self.preview_server.set_content(
            self.pane_text(), audio, f"{book} {chapter}:{verse}", cause)
        if parse_note:
            self.status_var.set(f"Preview updated{parse_note}")

    def _ensure_server(self) -> svg_preview.PreviewServer:
        if self.preview_server is None:
            self.preview_server = svg_preview.PreviewServer()
            self.preview_server.start()
        return self.preview_server

    def _on_embedded_toggle(self):
        host = "embedded" if self.embedded_var.get() else "browser"
        config.update(svg_preview_host=host)
        if host == "embedded":
            self._embedded_deaths = 0
            self.status_var.set(
                "Embedded preview re-enabled — next Open preview re-probes "
                "pywebview.")

    def _persist_browser_fallback(self, why: str):
        config.update(svg_preview_host="browser")
        self.embedded_var.set(False)
        server = self._ensure_server()
        webbrowser.open(server.url)
        self.status_var.set(
            f"Embedded preview unavailable ({why}) — using the system "
            f"browser instead. Tick 'Preview in own window' to try again "
            f"after fixing pywebview.")

    def _open_embedded(self):
        server = self._ensure_server()
        if self._preview_proc is not None and self._preview_proc.poll() is None:
            return  # window already open and polling; nothing to do
        script = os.path.join(REPO_ROOT, "svg_preview.py")
        try:
            self._preview_proc = subprocess.Popen(
                [sys.executable, script, "--url", server.url],
                cwd=REPO_ROOT, stderr=subprocess.PIPE)
        except OSError as e:
            self._persist_browser_fallback(str(e))
            return
        self.status_var.set("Opening embedded preview…")
        proc = self._preview_proc
        self.root.after(EMBEDDED_FAIL_WINDOW_MS,
                        lambda: self._check_embedded_alive(proc))

    def _check_embedded_alive(self, proc):
        """A *nonzero* exit within the fail window means pywebview is broken
        (import error, missing WebView2). Exit code 0 is the user closing
        the window — a normal exit that must NOT trip the browser fallback,
        or a quick glance-and-close would silently lock the studio out of
        embedded mode."""
        if proc.poll() is None:
            self.status_var.set("Embedded preview running.")
            return
        if proc.returncode == 0:
            self.status_var.set("Embedded preview closed.")
            return
        try:
            err = (proc.stderr.read() or b"").decode(errors="replace").strip()
        except Exception:
            err = ""
        self._embedded_deaths += 1
        why = err.splitlines()[-1] if err else f"exit code {proc.returncode}"
        self._persist_browser_fallback(why)

    def open_preview(self):
        server = self._ensure_server()
        self._push_preview("nav")
        # The checkbox mirrors the persisted svg_preview_host: the toggle and
        # the browser fallback each write both.
        if self.embedded_var.get() and self._embedded_deaths < 2:
            self._open_embedded()
        else:
            webbrowser.open(server.url)
            self.status_var.set(
                f"Preview at {server.url} — edits live-reload; Replay "
                f"restarts animation + narration.")

    def replay(self):
        if self.preview_server is None:
            self.open_preview()
            return
        self._push_preview("nav")

    # ----- publish glue + Inkscape --------------------------------------------

    def save_and_manifest(self):
        """Save, then rebuild web/visuals/manifest.json so the web app can
        see the file. The manifest only feeds the web app, so plain Save skips
        this while iterating."""
        before_dirty = self.dirty
        self.save()
        if before_dirty and self.dirty:
            return  # save was aborted (XML error dialog)
        threading.Thread(target=self._manifest_worker, daemon=True).start()

    def _manifest_worker(self):
        try:
            proc = subprocess.run(
                [sys.executable, os.path.join(REPO_ROOT, "build_manifest.py")],
                cwd=REPO_ROOT, capture_output=True, text=True, timeout=120)
            if proc.returncode != 0:
                self.events.put(("manifest_done",
                                 f"manifest rebuild failed: "
                                 f"{proc.stderr.strip()[:200]}"))
                return
            with open(MANIFEST_PATH, encoding="utf-8") as f:
                data = json.load(f)
            # Schema v2 wraps the key map in {version, entries}.
            keys = len(data.get("entries", data))
            self.events.put(("manifest_done",
                             f"web/visuals/manifest.json rebuilt — {keys} "
                             "verse keys."))
        except Exception as e:
            self.events.put(("manifest_done", f"manifest rebuild failed: {e}"))

    def _find_inkscape(self) -> str | None:
        exe = shutil.which("inkscape")
        if exe:
            return exe
        for base in (os.environ.get("ProgramFiles", r"C:\Program Files"),
                     os.environ.get("ProgramFiles(x86)",
                                    r"C:\Program Files (x86)")):
            candidate = os.path.join(base, "Inkscape", "bin", "inkscape.exe")
            if os.path.exists(candidate):
                return candidate
        return None

    def open_in_inkscape(self):
        """Optional convenience — the XML pane is always the fallback."""
        if not self.current_path or not os.path.exists(self.current_path):
            self.status_var.set("Save the file first, then open it in "
                                "Inkscape.")
            return
        exe = self._find_inkscape()
        if exe is None:
            if messagebox.askyesno(
                    "Inkscape not found",
                    "Inkscape is a free vector editor — handy for visual "
                    "editing, never required (the XML pane always works).\n\n"
                    "Open the download page (inkscape.org)?",
                    parent=self.root):
                webbrowser.open("https://inkscape.org/release/")
            return
        subprocess.Popen([exe, self.current_path])
        self.status_var.set(
            f"Opened in Inkscape — click 'Reload from disk' after saving "
            f"there.")

    def reload_from_disk(self):
        if not self._confirm_discard():
            return
        self._load_selected_file()
        self._push_preview("nav")

    def can_close(self) -> bool:
        """True when the window may close now. Otherwise asks: a generator
        still running (closing the app breaks its output pipe, so it can
        stop partway through rewriting its SVGs), then unsaved edits."""
        if self.busy and not messagebox.askyesno(
                "SVG Studio",
                "A generator re-run is still in progress. Closing now may "
                "stop it partway through rewriting its SVGs. Close anyway?",
                icon="warning", parent=self.root):
            return False
        return self._confirm_discard()

    def _on_close(self):
        if self.can_close():
            self.root.destroy()

    def _on_destroy(self, event):
        # <Destroy> on a window fires for each of its children too.
        if event.widget is not self.root:
            return
        if self._preview_proc is not None and self._preview_proc.poll() is None:
            self._preview_proc.terminate()
        if self.preview_server is not None:
            self.preview_server.stop()
            self.preview_server = None


def main():
    # Optional argv: <book> <chapter> — same convention as audio_studio.py /
    # pronunciation_tool.py, so the studio can open on a given passage.
    book, chapter = "Genesis", 1
    argv = sys.argv[1:]
    if argv:
        try:
            chapter = int(argv[-1])
            book = " ".join(argv[:-1]) or book
        except ValueError:
            pass
    root = tk.Tk()
    App(root, book, chapter)
    root.mainloop()


if __name__ == "__main__":
    main()
