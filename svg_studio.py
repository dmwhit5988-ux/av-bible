"""SVG Studio — verse-aware orchestrator for the visuals pipeline.

The studio owns the verse workflow (navigate, see which translation variants
exist, know when a file is generator-owned), the XML editing pane, and the
pipeline glue (save into visuals/<Book>/<chapter>/, manifest rebuild, deploy
staging). It deliberately does NOT own vector drawing — that is the XML pane
and/or Inkscape (SVG_STUDIO_DESIGN.md, "Option 3").

Usable standalone or as a Toplevel from app.py (same constructor contract as
audio_studio.App):

    python svg_studio.py [Book] [chapter]
"""

import os
import sys
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import ttk, messagebox

import books
import svg_registry
from passages import TRANSLATIONS

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
VISUALS_DIR = os.path.join(REPO_ROOT, "visuals")

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

TRANSLATION_CODES = [code for code, *_ in TRANSLATIONS]
GENERIC = "generic"


def verse_base(book: str, chapter: int, verse: int) -> str:
    return f"{book.replace(' ', '_')}_{chapter}_{verse}"


def chapter_dir(book: str, chapter: int) -> str:
    return os.path.join(VISUALS_DIR, book.replace(" ", "_"), str(chapter))


def variant_path(book: str, chapter: int, verse: int, variant: str) -> str:
    """Path of one variant's file. variant is GENERIC or a translation code."""
    base = verse_base(book, chapter, verse)
    suffix = "" if variant == GENERIC else f".{variant}"
    return os.path.join(chapter_dir(book, chapter), f"{base}{suffix}.svg")


def existing_variants(book: str, chapter: int, verse: int) -> set:
    """Which variants (GENERIC / translation codes) have a file on disk."""
    found = set()
    for variant in [GENERIC] + TRANSLATION_CODES:
        if os.path.exists(variant_path(book, chapter, verse, variant)):
            found.add(variant)
    return found


def resolve_for_translation(code: str, found: set) -> str | None:
    """Which variant a reader on translation `code` actually gets — the
    suffix chain .CODE.svg -> .svg, mirroring web/js/visuals.js findImage
    and visual_stage._find_image (verse key only; the chapter/book/default
    fallbacks are irrelevant to an authoring tool)."""
    if code in found:
        return code
    if GENERIC in found:
        return GENERIC
    return None


class App:
    def __init__(self, root, start_book="Genesis", start_chapter=1,
                 start_verse=1):
        self.root = root
        self.family: svg_registry.FamilyInfo | None = None
        self.current_path: str | None = None
        self.dirty = False
        self.editable = False
        self._loading = False   # suppress dirty-marking while loading the pane

        root.title("SVG Studio")
        root.geometry("980x640")
        root.minsize(820, 520)
        root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()

        if start_book not in books.BOOK_NAMES:
            start_book, start_chapter = "Genesis", 1
        self.book_var.set(start_book)
        self._on_book_change(keep_chapter=start_chapter)
        self.verse_var.set(str(max(1, int(start_verse or 1))))
        self._on_selection_change()

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

        ttk.Label(nav, text="Variant:").pack(side="left")
        self.variant_frame = ttk.Frame(nav)
        self.variant_frame.pack(side="left", padx=(4, 0))
        self.variant_var = tk.StringVar(value=GENERIC)

        # What each reader translation would actually load (suffix chain).
        self.resolution_var = tk.StringVar()
        ttk.Label(self.root, textvariable=self.resolution_var,
                  foreground="#888888", padding=(10, 0)).pack(anchor="w")

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
                                        state="disabled")
        self.edit_spec_btn.pack(side="left", padx=(6, 0))
        self.rerun_btn = ttk.Button(self.banner_btns, text="Re-run generator",
                                    state="disabled")
        self.rerun_btn.pack(side="left", padx=(6, 0))
        self.hand_edit_btn = ttk.Button(self.banner_btns,
                                        text="Hand-edit anyway (one-off)",
                                        state="disabled")
        self.hand_edit_btn.pack(side="left", padx=(6, 0))

        # Main split: XML pane left, actions right.
        body = ttk.Frame(self.root, padding=(10, 6))
        body.pack(fill="both", expand=True)

        pane_frame = ttk.Frame(body)
        pane_frame.pack(side="left", fill="both", expand=True)
        self.text = tk.Text(pane_frame, wrap="none", undo=True,
                            font=("Consolas", 10), background="#101018",
                            foreground="#e8e0cc", insertbackground="#e8e0cc")
        ys = ttk.Scrollbar(pane_frame, orient="vertical",
                           command=self.text.yview)
        xs = ttk.Scrollbar(pane_frame, orient="horizontal",
                           command=self.text.xview)
        self.text.configure(yscrollcommand=ys.set, xscrollcommand=xs.set)
        self.text.grid(row=0, column=0, sticky="nsew")
        ys.grid(row=0, column=1, sticky="ns")
        xs.grid(row=1, column=0, sticky="ew")
        pane_frame.rowconfigure(0, weight=1)
        pane_frame.columnconfigure(0, weight=1)
        self.text.bind("<<Modified>>", self._on_text_modified)
        self.text.bind("<Control-s>", lambda e: (self.save(), "break")[1])

        actions = ttk.Frame(body, padding=(10, 0, 0, 0))
        actions.pack(side="right", fill="y")
        self.save_btn = ttk.Button(actions, text="Save", command=self.save)
        self.save_btn.pack(fill="x", pady=(0, 6))

        # Status line.
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(self.root, textvariable=self.status_var, wraplength=900,
                  justify="left", padding=(10, 4)).pack(anchor="w")

    # ----- navigation --------------------------------------------------------

    def _on_book_change(self, keep_chapter=None):
        n = books.chapters_in(self.book_var.get())
        values = [str(i) for i in range(1, n + 1)]
        self.chapter_cb.configure(values=values)
        wanted = str(keep_chapter) if keep_chapter else self.chapter_var.get()
        self.chapter_var.set(wanted if wanted in values else "1")
        self._on_selection_change()

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
        return messagebox.askyesno(
            "SVG Studio", "Unsaved changes in the XML pane will be lost. "
                          "Continue?", parent=self.root)

    def _on_selection_change(self):
        book, chapter, verse = self._selection()
        new_variant_default = self.variant_var.get()
        if not self._confirm_discard():
            return
        self.family = svg_registry.owner_of(book, chapter)
        found = existing_variants(book, chapter, verse)
        # Keep the chosen variant if it still exists; otherwise prefer the
        # generic file, else the first existing variant, else generic-new.
        if new_variant_default not in found:
            if GENERIC in found or not found:
                new_variant_default = GENERIC
            else:
                new_variant_default = sorted(found)[0]
        self.variant_var.set(new_variant_default)
        self._rebuild_variant_chips(found)
        self._update_resolution_readout(found)
        self._update_banner()
        self._load_selected_file()

    def _rebuild_variant_chips(self, found):
        for child in self.variant_frame.winfo_children():
            child.destroy()
        for variant in [GENERIC] + TRANSLATION_CODES:
            mark = "●" if variant in found else "○"
            rb = ttk.Radiobutton(
                self.variant_frame, text=f"{variant} {mark}",
                value=variant, variable=self.variant_var,
                command=self._on_variant_change)
            rb.pack(side="left", padx=(0, 4))

    def _on_variant_change(self):
        if not self._confirm_discard():
            return
        self._load_selected_file()

    def _update_resolution_readout(self, found):
        parts = []
        for code in TRANSLATION_CODES:
            got = resolve_for_translation(code, found)
            if got is None:
                parts.append(f"{code} → —")
            elif got == GENERIC:
                parts.append(f"{code} → generic")
            else:
                parts.append(f"{code} → .{code}.svg")
        self.resolution_var.set("readers get:  " + "   ".join(parts))

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
        self.text.insert("1.0", content)
        self.text.edit_reset()
        self.text.edit_modified(False)
        if not editable:
            self.text.configure(state="disabled")
        self.editable = editable
        self.dirty = False
        self._loading = False
        self._update_title()

    def _load_selected_file(self):
        book, chapter, verse = self._selection()
        variant = self.variant_var.get()
        path = variant_path(book, chapter, verse, variant)
        self.current_path = path
        base = os.path.basename(path)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                content = f.read()
            if self.family is not None:
                # Generator-owned: read-only until "Hand-edit anyway" (a
                # later build step wires the unlock); routing beats blocking,
                # but accidental edits shouldn't be the default.
                self._set_pane(content, editable=False)
                self.status_var.set(
                    f"{base} — generator-owned ({self.family.label}); "
                    f"pane is read-only.")
            else:
                self._set_pane(content, editable=True)
                self.status_var.set(f"{base} — loaded.")
        else:
            self._set_pane(SKELETON, editable=True)
            self.status_var.set(
                f"{base} — no file yet; skeleton loaded, Save creates it.")

    def _on_text_modified(self, _event):
        if self._loading:
            self.text.edit_modified(False)
            return
        if self.text.edit_modified():
            self.dirty = True
            self._update_title()
            self.text.edit_modified(False)

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
        os.makedirs(os.path.dirname(self.current_path), exist_ok=True)
        with open(self.current_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        self.dirty = False
        self._update_title()
        book, chapter, verse = self._selection()
        self._rebuild_variant_chips(existing_variants(book, chapter, verse))
        self._update_resolution_readout(
            existing_variants(book, chapter, verse))
        self.status_var.set(f"Saved {os.path.basename(self.current_path)}.")

    def _on_close(self):
        if not self._confirm_discard():
            return
        self.root.destroy()


def main():
    # Optional argv: <book> <chapter> — same convention as audio_studio.py /
    # pronunciation_tool.py, so app.py can open the studio on the current
    # passage.
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
