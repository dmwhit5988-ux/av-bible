"""The visual layer: renders graphics for whichever verse is being spoken.

Architecture (built for the future custom-graphics work):

- Playback emits a `VerseContext` every time the spoken verse changes.
- A `StageController` broadcasts that context to every registered `StageView`
  (the in-app panel and, optionally, a fullscreen display window).
- Each view draws using the active `Renderer`. To add custom graphics later,
  write a new class with a `render(canvas, ctx, width, height)` method and
  call `controller.set_renderer(...)` — nothing else changes.
- Even sooner: drop PNG images into the `visuals/` folder and the default
  renderer picks them up automatically as verse backgrounds, most specific
  file wins:
      visuals/John_3_16.png   (exact verse)
      visuals/John_3.png      (whole chapter)
      visuals/John.png        (whole book)
      visuals/default.png     (everything else)
"""

import colorsys
import os
import re
import time
import tkinter as tk
from dataclasses import dataclass

from config import VISUALS_DIR

try:
    from PIL import Image, ImageSequence, ImageTk
    _HAS_PIL = True
except ImportError:  # app still works, just with rougher image scaling
    _HAS_PIL = False


def _rtf_to_text(rtf: str) -> str:
    """Minimal RTF -> plain text for simple WordPad/Word prose files.

    Drops non-text destination groups, maps \\par/\\line/\\tab and escaped
    characters, then strips remaining control words and braces.
    """
    s = re.sub(
        r"\{\\(?:\*|fonttbl|colortbl|stylesheet|info|pict|themedata"
        r"|listtable|listoverridetable|generator)"
        r"[^{}]*(?:\{[^{}]*\}[^{}]*)*\}",
        "", rtf)
    s = re.sub(r"\\par[d]?\b\s?", "\n", s)
    s = re.sub(r"\\line\b\s?", "\n", s)
    s = re.sub(r"\\tab\b\s?", "\t", s)
    s = re.sub(r"\\'([0-9a-fA-F]{2})",
               lambda m: chr(int(m.group(1), 16)), s)
    s = re.sub(r"\\u(-?\d+)\s?\??",
               lambda m: chr(int(m.group(1)) % 65536), s)
    s = re.sub(r"\\([{}\\])", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+-?\d*\s?", "", s)
    s = s.replace("{", "").replace("}", "")
    return re.sub(r"\n{3,}", "\n\n", s).strip()


@dataclass
class VerseContext:
    book: str
    chapter: int
    verse: int          # 0 means "whole chapter" (intro/narration)
    text: str           # verse text (not drawn by the default renderer,
                        # but available to custom renderers)
    reference: str      # e.g. "John 3:16 (KJV)"
    index: int          # 0-based position within the playlist
    total: int
    translation: str
    notes: list = None  # translator notes to display, or None/empty
    show_reference: bool = True  # draw the reference line at the bottom


class Renderer:
    """Base class for verse visuals. Subclass and override render().

    render() may return an integer: milliseconds until the view should call
    render() again (used for animation frames). Return None for a static
    image. Custom renderers can use the same mechanism to drive their own
    animations.
    """

    def render(self, canvas: tk.Canvas, ctx: VerseContext,
               width: int, height: int):
        raise NotImplementedError


class _Animation:
    """Decoded, pre-scaled frames of an animated image (GIF/WebP/APNG).

    Frames are letterboxed to fit inside the view (not cover-cropped like
    photos) so diagrams and maps are never clipped. Frame choice is based
    on the wall clock, keeping every stage view in sync.
    """

    MAX_FRAMES = 100
    PIXEL_BUDGET = 256 * 1024 * 1024  # ~256 MB of decoded RGBA frames
    # Every file is charged for at least this many frames when applying the
    # budget, so the displayed size depends only on the source and view
    # dimensions — never on frame count. WebP collapses fully-static verses
    # to 1 frame, so within one chapter files alternate 1 / ~22 frames; if
    # the budget shrank only the multi-frame ones, fullscreen would bounce
    # between image sizes on alternating verses. All shipped generators use
    # at most 24 frames.
    NOMINAL_FRAMES = 24

    def __init__(self, path: str, box_w: int, box_h: int):
        src = Image.open(path)
        # Honor the file's loop count: 0 = loop forever (default),
        # N = play N times, then hold the final frame (used by the
        # genealogy visuals so growth animations run once, not endlessly).
        self.loop = int(src.info.get("loop", 0) or 0)
        self.started = time.time()
        n = min(getattr(src, "n_frames", 1), self.MAX_FRAMES)
        scale = min(box_w / src.width, box_h / src.height)
        w = max(1, round(src.width * scale))
        h = max(1, round(src.height * scale))
        budget_n = max(n, self.NOMINAL_FRAMES)
        if budget_n * w * h * 4 > self.PIXEL_BUDGET:
            shrink = (self.PIXEL_BUDGET / (budget_n * w * h * 4)) ** 0.5
            w = max(1, int(w * shrink))
            h = max(1, int(h * shrink))
        self.frames = []
        self.durations = []
        for i, frame in enumerate(ImageSequence.Iterator(src)):
            if i >= n:
                break
            # LANCZOS: the diagrams are text-heavy and usually upscaled to
            # fullscreen; bilinear visibly blurs small labels.
            fr = frame.convert("RGBA").resize((w, h), Image.LANCZOS)
            self.frames.append(ImageTk.PhotoImage(fr))
            self.durations.append(
                max(20, int(frame.info.get("duration") or 100)))
        self.total = sum(self.durations) or 100

    def restart(self):
        self.started = time.time()

    def frame_now(self):
        """Return (frame, ms until the next frame is due; None = hold)."""
        if len(self.frames) <= 1:
            return self.frames[0], None
        elapsed = int((time.time() - self.started) * 1000)
        if self.loop and elapsed >= self.total * self.loop:
            return self.frames[-1], None  # finished — hold the last frame
        t = elapsed % self.total
        acc = 0
        for img, dur in zip(self.frames, self.durations):
            acc += dur
            if t < acc:
                return img, acc - t
        return self.frames[-1], self.durations[-1]


class DefaultRenderer(Renderer):
    """Book-tinted gradient (or a visuals/ image) with the verse text."""

    def __init__(self):
        self._image_cache = {}
        self._anim_cache = {}
        self._animated_flags = {}
        self._text_cache = {}
        self._last_verse_key = None

    # -- image lookup ------------------------------------------------------

    def _find_image(self, ctx: VerseContext):
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
            (VISUALS_DIR, "default"),
        ]
        # Animated formats first, so an added .gif/.webp wins over an
        # existing .png for the same verse. A translation-suffixed file
        # (e.g. Genesis_5_3.KJV.webp) wins over the generic one, letting
        # visuals that contain text match the translation being read.
        # Text files (.txt/.rtf) come last so any real image wins; they
        # render as a centered text panel styled like the notes overlay.
        exts = ((".gif", ".webp", ".png", ".jpg", ".jpeg", ".txt", ".rtf")
                if _HAS_PIL else (".png", ".txt", ".rtf"))
        suffixes = [f".{ctx.translation}", ""] if ctx.translation else [""]
        for directory, base in locations:
            for suffix in suffixes:
                for ext in exts:
                    path = os.path.join(directory, base + suffix + ext)
                    if os.path.exists(path):
                        return path
        return None

    def _is_animated(self, path: str) -> bool:
        if not _HAS_PIL:
            return False
        mtime = os.path.getmtime(path)
        key = (path, mtime)
        if key not in self._animated_flags:
            try:
                with Image.open(path) as im:
                    self._animated_flags[key] = bool(
                        getattr(im, "is_animated", False))
            except Exception:
                self._animated_flags[key] = False
            if len(self._animated_flags) > 64:
                self._animated_flags.pop(next(iter(self._animated_flags)))
        return self._animated_flags[key]

    def _get_animation(self, path: str, width: int, height: int) -> _Animation:
        key = (path, os.path.getmtime(path), width, height)
        anim = self._anim_cache.get(key)
        if anim is None:
            anim = _Animation(path, width, height)
            while len(self._anim_cache) >= 2:  # panel + fullscreen sizes
                self._anim_cache.pop(next(iter(self._anim_cache)))
            self._anim_cache[key] = anim
        return anim

    def _load_image(self, path: str, width: int, height: int):
        mtime = os.path.getmtime(path)
        if _HAS_PIL:
            # Smooth cover-scale: fill the canvas, center-crop the overflow.
            key = (path, mtime, width, height)
            img = self._image_cache.get(key)
            if img is None:
                src = Image.open(path).convert("RGB")
                scale = max(width / src.width, height / src.height)
                src = src.resize(
                    (max(width, round(src.width * scale)),
                     max(height, round(src.height * scale))),
                    Image.LANCZOS)
                left = (src.width - width) // 2
                top = (src.height - height) // 2
                src = src.crop((left, top, left + width, top + height))
                img = ImageTk.PhotoImage(src)
                while len(self._image_cache) >= 4:  # panel + fullscreen sizes
                    self._image_cache.pop(next(iter(self._image_cache)))
                self._image_cache[key] = img
            return img
        # Fallback without Pillow: integer zoom/subsample, roughly fitted.
        key = (path, mtime)
        if key not in self._image_cache:
            self._image_cache.clear()
            self._image_cache[key] = tk.PhotoImage(file=path)
        img = self._image_cache[key]
        iw, ih = img.width(), img.height()
        if iw and ih:
            if iw < width or ih < height:
                factor = max(1, min((width + iw - 1) // iw,
                                    (height + ih - 1) // ih, 8))
                if factor > 1:
                    img = img.zoom(factor)
            elif iw > 2 * width and ih > 2 * height:
                factor = min(iw // width, ih // height)
                if factor > 1:
                    img = img.subsample(factor)
        return img

    # -- text visuals ------------------------------------------------------

    def _load_text(self, path: str) -> str:
        """Contents of a .txt/.rtf visual as plain text (cached by mtime)."""
        mtime = os.path.getmtime(path)
        key = (path, mtime)
        if key not in self._text_cache:
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except OSError:
                text = ""
            if path.lower().endswith(".rtf"):
                text = _rtf_to_text(text)
            if len(self._text_cache) > 32:
                self._text_cache.clear()
            self._text_cache[key] = text.strip()
        return self._text_cache[key]

    # -- gradient ----------------------------------------------------------

    def _book_colors(self, book: str):
        hue = (hash(book) % 360) / 360.0
        top = colorsys.hsv_to_rgb(hue, 0.55, 0.22)
        bottom = colorsys.hsv_to_rgb(hue, 0.65, 0.08)
        to_hex = lambda rgb: "#%02x%02x%02x" % tuple(int(c * 255) for c in rgb)
        return to_hex(top), to_hex(bottom)

    def _draw_gradient(self, canvas, width, height, top_hex, bottom_hex):
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

    # -- main draw ---------------------------------------------------------

    def render(self, canvas, ctx, width, height):
        # A new verse restarts play-once animations from their first frame.
        vkey = (ctx.book, ctx.chapter, ctx.verse, ctx.translation)
        if vkey != self._last_verse_key:
            self._last_verse_key = vkey
            for anim in self._anim_cache.values():
                anim.restart()
        image_path = self._find_image(ctx)
        drew_image = False
        next_frame_ms = None
        # Text visuals (.txt/.rtf): book gradient plus a centered text
        # panel, styled like the translator-notes overlay.
        if image_path and image_path.lower().endswith((".txt", ".rtf")):
            top, bottom = self._book_colors(ctx.book)
            self._draw_gradient(canvas, width, height, top, bottom)
            text = self._load_text(image_path)
            if text:
                margin_t = max(30, width // 14)
                size = max(11, min(22, width // 48))
                text_id = canvas.create_text(
                    width // 2, height // 2,
                    text=text,
                    width=width - 2 * margin_t,
                    font=("Georgia", size, "italic"),
                    fill="#e8e0cc",
                    justify="center",
                )
                bbox = canvas.bbox(text_id)
                if bbox:
                    pad = 14
                    rect = canvas.create_rectangle(
                        bbox[0] - pad, bbox[1] - pad,
                        bbox[2] + pad, bbox[3] + pad,
                        fill="#000000", outline="", stipple="gray50",
                    )
                    canvas.tag_lower(rect, text_id)
            drew_image = True
            image_path = None
        # WebP/GIF are diagram/animation formats: letterboxed, never
        # cropped (even single-frame ones). PNG/JPG are photos: scaled to
        # fill and center-cropped.
        is_diagram = bool(image_path) and _HAS_PIL and \
            image_path.lower().endswith((".webp", ".gif"))
        if is_diagram:
            try:
                anim = self._get_animation(image_path, width, height)
                # Gradient shows through letterbox bars and transparency.
                top, bottom = self._book_colors(ctx.book)
                self._draw_gradient(canvas, width, height, top, bottom)
                img, next_frame_ms = anim.frame_now()
                canvas.create_image(width // 2, height // 2, image=img)
                canvas._bg_image_ref = img
                drew_image = True
            except Exception:
                drew_image = False
                next_frame_ms = None
        if not drew_image and image_path:
            try:
                img = self._load_image(image_path, width, height)
                canvas.create_rectangle(0, 0, width, height,
                                        fill="#000000", outline="")
                canvas.create_image(width // 2, height // 2, image=img)
                canvas._bg_image_ref = img  # prevent garbage collection
                drew_image = True
            except tk.TclError:
                pass
        if not drew_image:
            top, bottom = self._book_colors(ctx.book)
            self._draw_gradient(canvas, width, height, top, bottom)

        ref_size = max(12, min(26, width // 42))
        margin = max(30, width // 14)

        # Translator notes (when provided) sit above the reference line.
        if ctx.notes:
            note_size = max(10, min(18, width // 60))
            note_text = ("Translator-supplied words:  "
                         + "   ".join(f"“{n}”" for n in ctx.notes))
            text_id = canvas.create_text(
                width // 2, height - max(70, height // 5),
                text=note_text,
                width=width - 2 * margin,
                font=("Georgia", note_size, "italic"),
                fill="#e8e0cc",
                justify="center",
                anchor="s",
            )
            bbox = canvas.bbox(text_id)
            if bbox:
                pad = 10
                rect = canvas.create_rectangle(
                    bbox[0] - pad, bbox[1] - pad,
                    bbox[2] + pad, bbox[3] + pad,
                    fill="#000000", outline="", stipple="gray50",
                )
                canvas.tag_lower(rect, text_id)

        if ctx.show_reference:
            ref_id = canvas.create_text(
                width // 2, height - max(28, height // 12),
                text=ctx.reference,
                font=("Georgia", ref_size, "italic"),
                fill="#d8c68f",
            )
            bbox = canvas.bbox(ref_id)
            if bbox:
                pad_x, pad_y = 14, 6
                ref_rect = canvas.create_rectangle(
                    bbox[0] - pad_x, bbox[1] - pad_y,
                    bbox[2] + pad_x, bbox[3] + pad_y,
                    fill="#000000", outline="", stipple="gray50",
                )
                canvas.tag_lower(ref_rect, ref_id)
        return next_frame_ms


class StageView:
    """A canvas that shows the current verse; re-renders on resize."""

    def __init__(self, parent, controller, **canvas_kwargs):
        canvas_kwargs.setdefault("bg", "#101018")
        canvas_kwargs.setdefault("highlightthickness", 0)
        self.canvas = tk.Canvas(parent, **canvas_kwargs)
        self.controller = controller
        self._anim_id = None
        self.canvas.bind("<Configure>", lambda e: self.redraw())
        controller.register(self)

    def _cancel_tick(self):
        if self._anim_id is not None:
            try:
                self.canvas.after_cancel(self._anim_id)
            except tk.TclError:
                pass
            self._anim_id = None

    def redraw(self):
        canvas = self.canvas
        if not canvas.winfo_exists():
            return
        self._cancel_tick()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width < 10 or height < 10:
            return
        canvas.delete("all")
        ctx = self.controller.current
        if ctx is not None:
            delay = self.controller.renderer.render(canvas, ctx,
                                                    width, height)
            if isinstance(delay, int) and delay > 0:
                self._anim_id = canvas.after(max(20, delay), self.redraw)
        else:
            canvas.create_rectangle(0, 0, width, height,
                                    fill="#101018", outline="")
            canvas.create_text(
                width // 2, height // 2,
                text=self.controller.idle_message,
                font=("Georgia", max(12, min(24, width // 34)), "italic"),
                fill="#8a8aa0",
                width=width - 60,
                justify="center",
            )

    def destroy(self):
        self._cancel_tick()
        self.controller.unregister(self)
        if self.canvas.winfo_exists():
            self.canvas.destroy()


class StageController:
    """Holds current verse context + renderer; broadcasts to all views."""

    def __init__(self):
        self.renderer: Renderer = DefaultRenderer()
        self.current: VerseContext | None = None
        self.idle_message = "AV Bible\n\nChoose a passage and press Play"
        self._views: list[StageView] = []

    def register(self, view: StageView):
        if view not in self._views:
            self._views.append(view)

    def unregister(self, view: StageView):
        if view in self._views:
            self._views.remove(view)

    def set_renderer(self, renderer: Renderer):
        self.renderer = renderer
        self._broadcast()

    def show_verse(self, ctx: VerseContext):
        self.current = ctx
        self._broadcast()

    def show_idle(self, message: str | None = None):
        if message:
            self.idle_message = message
        self.current = None
        self._broadcast()

    def _broadcast(self):
        for view in list(self._views):
            if view.canvas.winfo_exists():
                view.redraw()
            else:
                self.unregister(view)


class FullscreenStage:
    """A borderless fullscreen window mirroring the stage — for projection."""

    def __init__(self, root, controller):
        self.top = tk.Toplevel(root)
        self.top.title("AV Bible Display")
        self.top.configure(bg="black")
        self.top.attributes("-fullscreen", True)
        self.view = StageView(self.top, controller, bg="black")
        self.view.canvas.pack(fill="both", expand=True)
        self.top.bind("<Escape>", lambda e: self.close())
        self.top.bind("<F11>", lambda e: self.close())
        self.top.protocol("WM_DELETE_WINDOW", self.close)
        # Grab keyboard focus so Escape works immediately, without needing
        # a click on the fullscreen window first.
        self.top.focus_force()
        self.view.canvas.focus_set()

    def close(self):
        self.view.destroy()
        if self.top.winfo_exists():
            self.top.destroy()
