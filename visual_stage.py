"""The visual layer: shows the SVG visual for whichever verse is being spoken.

This is the Studio's interim preview stage. It goes, with PlaybackSession,
once a Preview pane embeds the real web app (ROADMAP.md, Studio).

- Playback emits a `VerseContext` every time the spoken verse changes.
- A `StageController` broadcasts that context to every registered `StageView`
  (today the one panel in the Studio window).
- A verse's visual is the most specific SVG under visuals/ (the generators'
  output, the same vector masters the web app serves):
      visuals/John/3/John_3_16.svg   (exact verse)
      visuals/John/3/John_3.svg      (whole chapter)
      visuals/John/John.svg          (whole book)
- SVGs, SMIL animation and all, render in an embedded WebView2 panel via
  svg_stage.py, so pywebview is required. A verse without an SVG, or a
  machine where the web view failed, shows the book gradient in the same
  hue the web stage uses.
"""

import colorsys
import os
import tkinter as tk
from dataclasses import dataclass

from config import VISUALS_DIR

import svg_stage

IDLE_MESSAGE = "Theoria\n\nChoose a passage and press Play"


@dataclass
class VerseContext:
    book: str
    chapter: int
    verse: int          # 0 means "whole chapter" (the chapter intro)
    index: int          # 0-based position within the chapter's verses


def find_svg(ctx: VerseContext) -> str | None:
    """Path of the most specific SVG visual for this verse, or None."""
    book = ctx.book.replace(" ", "_")
    chapter_dir = os.path.join(VISUALS_DIR, book, str(ctx.chapter))
    book_dir = os.path.join(VISUALS_DIR, book)
    # Preferred layout is visuals/<Book>/<chapter>/; flat files directly
    # in visuals/ are still honored as a fallback. Most specific wins.
    locations = [
        (chapter_dir, f"{book}_{ctx.chapter}_{ctx.verse}"),
        (VISUALS_DIR, f"{book}_{ctx.chapter}_{ctx.verse}"),
        (chapter_dir, f"{book}_{ctx.chapter}"),
        (VISUALS_DIR, f"{book}_{ctx.chapter}"),
        (book_dir, book),
        (VISUALS_DIR, book),
    ]
    for directory, base in locations:
        path = os.path.join(directory, base + ".svg")
        if os.path.exists(path):
            return path
    return None


# -- book gradient -----------------------------------------------------------

def book_hue(book: str) -> int:
    """The book's gradient hue, 0-359. A port of hashBook in
    web/js/visuals.js (a 31x string hash in signed 32-bit arithmetic), so a
    book is the same colour here as on the web stage. Python's own hash()
    is salted per process and would change the colour on every run."""
    h = 0
    for ch in book:
        h = (h * 31 + ord(ch) + 2**31) % 2**32 - 2**31
    return abs(h) % 360


def book_colors(book: str) -> tuple[str, str]:
    """Top and bottom gradient colours, as web/js/visuals.js bookGradient
    gives them: hsl(hue, 45%, 16%) and hsl(hue, 55%, 6%)."""
    hue = book_hue(book) / 360.0

    def to_hex(lightness: float, saturation: float) -> str:
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        return "#%02x%02x%02x" % tuple(round(c * 255) for c in rgb)

    return to_hex(0.16, 0.45), to_hex(0.06, 0.55)


def _draw_gradient(canvas, width, height, top_hex, bottom_hex):
    steps = max(2, min(120, height // 4))
    t = tuple(int(top_hex[i:i + 2], 16) for i in (1, 3, 5))
    b = tuple(int(bottom_hex[i:i + 2], 16) for i in (1, 3, 5))
    band = height / steps
    for i in range(steps):
        f = i / (steps - 1)
        color = "#%02x%02x%02x" % tuple(
            int(t[c] + (b[c] - t[c]) * f) for c in range(3)
        )
        canvas.create_rectangle(
            0, int(i * band), width, int((i + 1) * band) + 1,
            fill=color, outline="",
        )


class StageView:
    """A canvas that shows the current verse: its SVG in an embedded web
    view laid over the canvas, or the book gradient. Redraws on resize."""

    def __init__(self, parent, controller, **canvas_kwargs):
        canvas_kwargs.setdefault("bg", "#101018")
        canvas_kwargs.setdefault("highlightthickness", 0)
        self.canvas = tk.Canvas(parent, **canvas_kwargs)
        self.controller = controller
        self._web_panel = None  # embedded web view for .svg visuals
        self.canvas.bind("<Configure>", lambda e: self.redraw())
        controller.register(self)

    # -- embedded SVG panel --------------------------------------------------

    def _show_svg(self, svg_path: str, ctx: VerseContext):
        server = self.controller.svg_server()
        key = (svg_path, os.path.getmtime(svg_path),
               ctx.book, ctx.chapter, ctx.verse)
        server.set_verse(key, svg_path)
        if self._web_panel is None:
            self._web_panel = svg_stage.WebPanel(
                self.canvas, server.url, on_fail=self._on_svg_fail)
        self._web_panel.show()

    def _hide_svg(self):
        if self._web_panel is not None:
            self._web_panel.hide()
        # Forget the published verse so returning to it later re-pushes
        # and restarts its SMIL animations.
        self.controller.clear_svg()

    def _on_svg_fail(self, why: str):
        # svg_stage has already marked itself unavailable; every view
        # redraws with the book gradient and the reason.
        self.controller.rebroadcast()

    def redraw(self):
        canvas = self.canvas
        if not canvas.winfo_exists():
            return
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width < 10 or height < 10:
            return
        canvas.delete("all")
        ctx = self.controller.current
        if ctx is None:
            self._hide_svg()
            canvas.create_rectangle(0, 0, width, height,
                                    fill="#101018", outline="")
            canvas.create_text(
                width // 2, height // 2,
                text=IDLE_MESSAGE,
                font=("Georgia", max(12, min(24, width // 34)), "italic"),
                fill="#8a8aa0",
                width=width - 60,
                justify="center",
            )
            return
        if svg_stage.available():
            svg_path = find_svg(ctx)
            if svg_path:
                try:
                    self._show_svg(svg_path, ctx)
                    return
                except OSError:
                    pass  # unreadable .svg: show the gradient instead
        self._hide_svg()
        top, bottom = book_colors(ctx.book)
        _draw_gradient(canvas, width, height, top, bottom)
        if not svg_stage.available():
            canvas.create_text(
                width // 2, height // 2,
                text=("The SVG view could not start "
                      f"({svg_stage.fail_reason()}).\n"
                      "It needs pywebview and the WebView2 runtime "
                      "(see requirements.txt)."),
                font=("Segoe UI", 10),
                fill="#8a8aa0",
                width=width - 60,
                justify="center",
            )


class StageController:
    """Holds the current verse context; broadcasts it to all views."""

    def __init__(self):
        self.current: VerseContext | None = None
        self._views: list[StageView] = []
        self._svg_server = None

    def svg_server(self):
        """The shared server feeding every embedded SVG panel (started
        lazily the first time a verse resolves to an .svg visual)."""
        if self._svg_server is None:
            self._svg_server = svg_stage.StageServer()
            self._svg_server.start()
        return self._svg_server

    def clear_svg(self):
        if self._svg_server is not None:
            self._svg_server.clear()

    def rebroadcast(self):
        self._broadcast()

    def register(self, view: StageView):
        if view not in self._views:
            self._views.append(view)

    def show_verse(self, ctx: VerseContext):
        self.current = ctx
        self._broadcast()

    def _broadcast(self):
        for view in list(self._views):
            if view.canvas.winfo_exists():
                view.redraw()
            else:
                self._views.remove(view)
