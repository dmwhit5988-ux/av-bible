"""Render a verse range to a finished, YouTube-ready MP4.

The engine behind the Video Studio (video_studio.py). No tkinter here, so it
is importable, scriptable, and testable on its own:

    python video_render.py Genesis 1 --out out/Genesis1.mp4

What it assembles, per verse, from assets the project already produces:

    narration   web/audio/<Book>_<ch>_<v>.mp3, exactly what the web player
                uses. Missing verses are synthesized on the fly through
                tts_engine.synthesize() -- the same production path (and the
                same pronunciation respelling) the desktop reader uses -- so a
                range that was never published still renders.
    visual      web/visuals/<Book>/<ch>/<Book>_<ch>_<v>.svg, resolved by
                resolve_svg(): the verse's own file, then a range file
                covering it, then the chapter file -- most specific first,
                as the web manifest does (visual_stage.find_svg, the interim
                PC stage, has no range-file step).

Ranges cross chapters freely (Genesis 1:1 -> Genesis 3:24), which is the point:
a video is a *passage*, not a chapter.

--------------------------------------------------------------------------
Why it is built this way
--------------------------------------------------------------------------

The visuals are SMIL-animated SVG. Nothing in the Python stack renders SMIL
(resvg, Pillow and cairosvg all draw the t=0 frame), so frames come from a
real browser -- headless Chrome/Edge driven over the DevTools Protocol, the
same engine the stage and the web app already use, so the video looks exactly
like the app. Frames are deterministic rather than screen-recorded:
`svg.pauseAnimations()` then `svg.setCurrentTime(t)` per frame, so a render is
reproducible and never drops or tears a frame.

Screenshotting 4K is ~180 ms/frame, so rendering every frame of a 50-minute
passage would be absurd. It is also unnecessary: each verse's SVG animates a
short reveal (0.8-4 s, always `fill="freeze"`, never `repeatCount=
"indefinite"` in the house generators) and is then a *still* for the rest of
the narration. So each verse becomes one segment of

    [motion frames captured at fps]  +  [one still frame held by ffmpeg]

which is where the render time actually goes -- proportional to seconds of
animation, not to video length. Verses render concurrently across several
browser pages, each handing its frames to its own ffmpeg as files on disk (no
pipes: a frame writer and ffmpeg sharing a pipe deadlock each other, which
this renderer demonstrated twice before the pipes were removed). The pieces
are then concatenated with `-c:v copy`, so the video is encoded exactly once.

A/V sync is exact by construction: each verse's narration is padded with
silence out to a whole number of frames, and the segment is built to that same
frame count. Nothing drifts over a 400-verse render.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import concurrent.futures
import json
import math
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import xml.sax.saxutils as saxutils
from dataclasses import dataclass, field

import books
import config
import generate_showcase_audio as showcase_audio
import svg_registry
import tts_engine
from config import VISUALS_DIR
from passages import ATTRIBUTION, PassageError, load_chapter

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# Every visual in the project is authored at 1024x576, so all three presets
# are exact 16:9 scales of the same artwork with no letterboxing.
RESOLUTIONS = {
    "2160p — 4K (recommended)": (3840, 2160),
    "1440p — 2K": (2560, 1440),
    "1080p — HD": (1920, 1080),
}
DEFAULT_RESOLUTION = "2160p — 4K (recommended)"
FRAME_RATES = [60, 30]

SAMPLE_RATE = 48000          # YouTube's preferred audio rate
CHANNELS = 2
BYTES_PER_SAMPLE = 2         # s16le
PCM_BYTES_PER_SEC = SAMPLE_RATE * CHANNELS * BYTES_PER_SAMPLE

DEFAULT_GAP = 0.45           # breath between verses, seconds
DEFAULT_CRF = 16             # visually lossless for flat vector art
DEFAULT_TITLE_SECONDS = 3.0

# Everything after the last animation ends is a still, but SMIL end times and
# the browser's compositor don't have to agree to the millisecond; a short tail
# guarantees the held frame really is the settled one.
MOTION_TAIL = 0.08

# Frames are captured by one browser page, serially. Several pages measured
# only ~1.5x faster per frame (180 ms -> 122 ms) and wedged in real renders, so
# the parallelism lives on the encoding side instead, where it is just ffmpeg
# and costs nothing in reliability.
MAX_ENCODE_JOBS = 4
DEFAULT_ENCODE_JOBS = 3

# A page's renderer can wedge -- a crashed renderer answers nothing, ever, and
# a render that waits on it politely simply never finishes. So EVERY protocol
# call is bounded, and a page that misses its deadline is thrown away and
# replaced rather than nursed.
CMD_TIMEOUT = 60.0
CAPTURE_TIMEOUT = 25.0
CAPTURE_RETRIES = 3
ITEM_ATTEMPTS = 2

# A page stops answering after somewhere around 50-70 screenshots, whatever it
# is showing -- a 66-frame title card wedges its page on its own, and so does a
# verse that lands past that count on a page shared with earlier verses. Each
# 4K capture evidently leaves something behind. Since seeking is absolute, a
# page can be replaced at any moment without losing progress: the replacement
# reloads the same document and carries on at the next frame. So pages are
# retired by capture count, well short of where they fail.
PAGE_RECYCLE_CAPTURES = 40

# House palette, matching the generators (see svg_surface.py).
INK_BG = "rgb(16,16,24)"
INK_GOLD = "rgb(216,198,143)"
INK_DIM = "rgb(140,130,100)"

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0


class RenderError(Exception):
    """User-presentable render failure."""


class FFmpegMissing(RenderError):
    pass


class BrowserMissing(RenderError):
    pass


# ---------------------------------------------------------------------------
# External tools
# ---------------------------------------------------------------------------

FFMPEG_HINT = (
    "ffmpeg was not found. Install it once, then reopen the Video Studio:\n\n"
    "    winget install BtbN.FFmpeg.GPL\n\n"
    "(or drop ffmpeg.exe / ffprobe.exe in tools/ffmpeg/bin/ beside the app)."
)

_BROWSER_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def _registry_path_dirs() -> list:
    """PATH as the *registry* has it, which is not what this process inherited.

    Installing ffmpeg with winget appends to the user PATH, and already-running
    processes keep the PATH they started with -- so a just-installed ffmpeg is
    invisible to the app until a sign-out. Reading the registry directly turns
    "install it, then reopen the studio" into the truth it claims to be."""
    if os.name != "nt":
        return []
    import winreg
    dirs = []
    for root, key in ((winreg.HKEY_CURRENT_USER, r"Environment"),
                      (winreg.HKEY_LOCAL_MACHINE,
                       r"SYSTEM\CurrentControlSet\Control\Session Manager"
                       r"\Environment")):
        try:
            with winreg.OpenKey(root, key) as handle:
                value, _ = winreg.QueryValueEx(handle, "Path")
        except OSError:
            continue
        dirs += [os.path.expandvars(p.strip().strip('"'))
                 for p in str(value).split(os.pathsep) if p.strip()]
    return dirs


def find_ffmpeg() -> str:
    """Path to ffmpeg.exe, or raise FFmpegMissing with install instructions.

    Checked in order: a repo-local tools/ copy (so the app can be made
    portable without touching PATH at all), this process's PATH, winget's
    shim directory, and finally PATH as the registry currently has it."""
    local = os.path.join(REPO_ROOT, "tools", "ffmpeg", "bin", "ffmpeg.exe")
    if os.path.exists(local):
        return local
    found = shutil.which("ffmpeg")
    if found:
        return found
    links = os.path.join(os.environ.get("LOCALAPPDATA", ""),
                         "Microsoft", "WinGet", "Links", "ffmpeg.exe")
    if links and os.path.exists(links):
        return links
    for directory in _registry_path_dirs():
        candidate = os.path.join(directory, "ffmpeg.exe")
        if os.path.exists(candidate):
            return candidate
    raise FFmpegMissing(FFMPEG_HINT)


def find_browser() -> str:
    for path in _BROWSER_CANDIDATES:
        if os.path.exists(path):
            return path
    for name in ("chrome", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    raise BrowserMissing(
        "No Chrome or Edge found. The renderer needs a Chromium browser to "
        "rasterize the animated SVG visuals (the same engine the stage uses).")


def _run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True,
                          creationflags=CREATE_NO_WINDOW, **kw)


# ---------------------------------------------------------------------------
# SMIL: how long does this verse actually move?
# ---------------------------------------------------------------------------

_ANIM_RE = re.compile(
    r"<(?:animate|set|animateTransform|animateMotion)\b([^>]*)>", re.I)
_ATTR_RE = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')


def _clock(value: str) -> float | None:
    """SMIL clock value -> seconds. Handles '2s', '800ms', '1.5', and the
    'min:sec' form; returns None for anything event-based ('click', 'a.end')
    which the house generators never emit."""
    value = (value or "").strip()
    if not value:
        return None
    m = re.fullmatch(r"(-?[\d.]+)(ms|s|min|h)?", value)
    if m:
        n = float(m.group(1))
        unit = m.group(2) or "s"
        return n * {"ms": 0.001, "s": 1.0, "min": 60.0, "h": 3600.0}[unit]
    if ":" in value:  # 00:03.5
        try:
            parts = [float(p) for p in value.split(":")]
        except ValueError:
            return None
        secs = 0.0
        for p in parts:
            secs = secs * 60 + p
        return secs
    return None


def motion_end(svg_text: str, cap: float) -> float:
    """Seconds until this SVG has finished animating and become a still.

    `cap` bounds the answer -- a perpetual animation (repeatCount=
    "indefinite", the tabernacle's pulse) never settles, so the whole verse is
    treated as motion and every frame is captured. Returns 0.0 for a document
    with no SMIL at all: one frame, held."""
    end = 0.0
    for match in _ANIM_RE.finditer(svg_text):
        attrs = dict(_ATTR_RE.findall(match.group(1)))
        repeat = attrs.get("repeatCount", "1").strip()
        dur = _clock(attrs.get("dur", "")) or 0.0
        # begin may be a semicolon-separated list; the element is not settled
        # until the last timed instance has finished.
        begins = [_clock(b) for b in attrs.get("begin", "0s").split(";")]
        begin = max([b for b in begins if b is not None] or [0.0])
        if repeat == "indefinite" or attrs.get("repeatDur") == "indefinite":
            return cap
        try:
            reps = float(repeat)
        except ValueError:
            reps = 1.0
        end = max(end, begin + dur * reps)
    if end <= 0.0:
        return 0.0
    return min(end + MOTION_TAIL, cap)


# ---------------------------------------------------------------------------
# Asset resolution
# ---------------------------------------------------------------------------

def resolve_svg(book: str, chapter: int, verse: int) -> str | None:
    """The SVG the stage would show for this verse, or None.

    Most specific first, as in the web manifest: the verse's own file, then
    a range file covering the verse (Numbers_32_16-32.svg, D17; where two
    overlap the name that sorts first wins, as in build_manifest), then the
    chapter file; the book-level and global default files are legacy
    fallbacks the web no longer uses.
    """
    safe = book.replace(" ", "_")
    chapter_dir = os.path.join(VISUALS_DIR, safe, str(chapter))
    book_dir = os.path.join(VISUALS_DIR, safe)
    for directory in (chapter_dir, VISUALS_DIR):
        path = os.path.join(directory, f"{safe}_{chapter}_{verse}.svg")
        if os.path.exists(path):
            return path
    range_re = re.compile(rf"^{re.escape(safe)}_{chapter}_(\d+)-(\d+)\.svg$")
    for directory in (chapter_dir, VISUALS_DIR):
        if not os.path.isdir(directory):
            continue
        for name in sorted(os.listdir(directory)):
            m = range_re.match(name)
            if m and int(m.group(1)) <= verse <= int(m.group(2)):
                return os.path.join(directory, name)
    locations = [
        (chapter_dir, f"{safe}_{chapter}"),
        (VISUALS_DIR, f"{safe}_{chapter}"),
        (book_dir, safe),
        (VISUALS_DIR, safe),
        (VISUALS_DIR, "default"),
    ]
    for directory, base in locations:
        path = os.path.join(directory, base + ".svg")
        if os.path.exists(path):
            return path
    return None


def resolve_audio(book: str, chapter: int, verse: int, text: str,
                  voice: str, rate: int) -> tuple[str, bool]:
    """(path, was_synthesized). Prefers the published web/audio MP3 -- the
    exact file the site plays -- and falls back to synthesizing through the
    production TTS path, which caches, so a second render is instant."""
    safe = book.replace(" ", "_")
    base = f"{safe}_{chapter}_{verse}"
    published = os.path.join(showcase_audio.AUDIO_DIR,
                             showcase_audio._audio_filename(base))
    if os.path.exists(published) and os.path.getsize(published) > 500:
        return published, False
    return tts_engine.synthesize(text, voice, rate), True


def publish_audio(book: str, chapter: int, verse: int, src: str,
                  manifest: dict) -> None:
    """Copy a freshly synthesized verse into web/audio/ and register it, so a
    render doubles as an Audio Renderer pass. Only real neural MP3s ship --
    the offline SAPI .wav fallback is never published (same rule as
    generate_showcase_audio)."""
    if not src.lower().endswith(".mp3"):
        return
    safe = book.replace(" ", "_")
    base = f"{safe}_{chapter}_{verse}"
    filename = showcase_audio._audio_filename(base)
    os.makedirs(showcase_audio.AUDIO_DIR, exist_ok=True)
    shutil.copyfile(src, os.path.join(showcase_audio.AUDIO_DIR, filename))
    manifest[showcase_audio._manifest_key(base)] = filename


# ---------------------------------------------------------------------------
# Generated cards (title, and the safety net for a verse with no visual)
# ---------------------------------------------------------------------------

def _card_svg(lines, animate: bool = True) -> str:
    """A house-style card: dark ground, gold Georgia, optional fade-in.

    `lines` is [(text, font_size, color), ...] stacked and centered."""
    total = sum(size * 1.6 for _, size, _ in lines)
    y = 288 - total / 2
    body = []
    for text, size, color in lines:
        y += size * 1.6
        body.append(
            f'<text x="512" y="{y:.1f}" font-size="{size}" '
            f'text-anchor="middle" fill="{color}" '
            f'font-family="Georgia, \'Times New Roman\', serif">'
            f'{saxutils.escape(text)}</text>')
    fade = ('<animate attributeName="opacity" values="0;1" dur="1.1s" '
            'begin="0s" fill="freeze"/>') if animate else ""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 576" '
        'width="1024" height="576">'
        f'<rect x="0" y="0" width="1024" height="576" fill="{INK_BG}"/>'
        f'<g opacity="{0 if animate else 1}">{fade}{"".join(body)}</g>'
        '</svg>')


def title_card_svg(title: str, subtitle: str, footer: str) -> str:
    return _card_svg([
        (title, 58, INK_GOLD),
        (subtitle, 28, INK_DIM),
        ("", 20, INK_DIM),
        (footer, 20, INK_DIM),
    ])


def fallback_card_svg(ref: str) -> str:
    return _card_svg([(ref, 44, INK_GOLD)], animate=False)


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------

@dataclass
class RenderSpec:
    book: str
    start_chapter: int
    start_verse: int
    end_chapter: int
    end_verse: int | None          # None = to the end of end_chapter
    out_path: str
    voice: str = tts_engine.HOUSE_VOICE
    rate: int = tts_engine.HOUSE_RATE
    width: int = 3840
    height: int = 2160
    fps: int = 60
    gap: float = DEFAULT_GAP
    crf: int = DEFAULT_CRF
    title_card: bool = True
    publish_new_audio: bool = False
    workers: int = 0               # concurrent ffmpeg encodes; 0 = default

    # Set once the passage is loaded, so an open-ended range ("to the end of
    # the chapter") can name its real last verse everywhere it is displayed.
    resolved_end: tuple | None = None

    @property
    def reference(self) -> str:
        end_chapter, end_verse = (self.resolved_end
                                  or (self.end_chapter, self.end_verse))
        a = f"{self.book} {self.start_chapter}:{self.start_verse}"
        if self.start_chapter == end_chapter:
            b = str(end_verse) if end_verse else "end"
        else:
            b = f"{end_chapter}:{end_verse or 'end'}"
        return f"{a}–{b}"


@dataclass
class Item:
    """One timeline segment: a verse, or the title card."""
    kind: str                      # "verse" | "title"
    ref: str
    text: str = ""
    chapter: int = 0
    verse: int = 0
    svg_path: str | None = None
    svg_text: str = ""
    audio_path: str | None = None
    pcm: bytes | None = None       # decoded narration, filled by the audio pass
    frames: int = 0                # total frames in this segment
    motion_frames: int = 0
    motion_seconds: float = 0.0
    start_frame: int = 0
    # Seconds of this picture's timeline already shown by the items before
    # it: a verse with the same SVG as the verse before (a shared range
    # file, an identical copy, held artwork) continues that clock instead of
    # restarting at 0 (D17). Frames are captured at clock_offset + t.
    clock_offset: float = 0.0

    def duration(self, fps: int) -> float:
        return self.frames / fps

    def start(self, fps: int) -> float:
        return self.start_frame / fps


def build_plan(spec: RenderSpec, on_status=None, cancel=None):
    """Load the passage, resolve every verse's audio and visual, and return
    (items, warnings). Durations are not known yet -- the audio pass fills
    them in, because the decoded PCM length is the authoritative duration."""
    warnings: list[str] = []
    items: list[Item] = []
    say = on_status or (lambda *_: None)

    n_chapters = books.chapters_in(spec.book)
    end_chapter = min(spec.end_chapter, n_chapters)
    manifest = showcase_audio._load_manifest() if spec.publish_new_audio else None
    last_svg: str | None = None

    for chapter in range(spec.start_chapter, end_chapter + 1):
        if cancel and cancel():
            break
        say(f"Loading {spec.book} {chapter}…")
        try:
            passage = load_chapter(spec.book, chapter)
        except PassageError as e:
            warnings.append(f"{spec.book} {chapter}: {e}")
            continue
        lo = spec.start_verse if chapter == spec.start_chapter else 1
        hi = (spec.end_verse if (chapter == end_chapter and spec.end_verse)
              else 10 ** 6)
        for num, text in passage.verses:
            if cancel and cancel():
                break
            if not (lo <= num <= hi):
                continue
            ref = f"{spec.book} {chapter}:{num}"
            say(f"Preparing {ref}…")
            svg_path = resolve_svg(spec.book, chapter, num)
            if svg_path is None:
                # Hold the previous verse's artwork rather than cutting to
                # black; a passage whose visuals stop partway still reads.
                svg_path = last_svg
                if svg_path is None:
                    warnings.append(f"{ref}: no visual — using a plain card")
            else:
                last_svg = svg_path
            try:
                audio_path, fresh = resolve_audio(
                    spec.book, chapter, num, text, spec.voice, spec.rate)
            except Exception as e:                      # TTS unreachable
                raise RenderError(f"{ref}: could not get narration — {e}")
            if fresh and not audio_path.lower().endswith(".mp3"):
                warnings.append(
                    f"{ref}: edge-tts unavailable, using the offline voice")
            if fresh and manifest is not None:
                publish_audio(spec.book, chapter, num, audio_path, manifest)
            items.append(Item(
                kind="verse", ref=ref, text=text, chapter=chapter, verse=num,
                svg_path=svg_path, audio_path=audio_path,
                svg_text=(open(svg_path, encoding="utf-8").read()
                          if svg_path else fallback_card_svg(ref))))

    if manifest is not None:
        showcase_audio._save_manifest(manifest)
    if not items:
        raise RenderError("No verses in that range.")

    # Now that the passage is known, an open-ended range can name its real
    # last verse -- on the title card, in the description, everywhere.
    spec.resolved_end = (items[-1].chapter, items[-1].verse)
    if spec.title_card:
        items.insert(0, Item(
            kind="title", ref=spec.reference,
            svg_text=title_card_svg(
                spec.book,
                spec.reference.replace(spec.book + " ", ""),
                ATTRIBUTION)))
    return items, warnings


# ---------------------------------------------------------------------------
# Pass 1 — audio: decode to PCM, pad each verse to a whole number of frames
# ---------------------------------------------------------------------------

def _decode_pcm(ffmpeg: str, path: str) -> bytes:
    res = _run([ffmpeg, "-v", "error", "-i", path, "-f", "s16le",
                "-acodec", "pcm_s16le", "-ar", str(SAMPLE_RATE),
                "-ac", str(CHANNELS), "-"])
    if res.returncode != 0:
        raise RenderError(f"ffmpeg could not decode {os.path.basename(path)}: "
                          + res.stderr.decode(errors="replace")[:200])
    return res.stdout


def build_audio(ffmpeg: str, items, spec: RenderSpec, pcm_path: str,
                on_progress=None, cancel=None) -> None:
    """Decode every verse's narration into one raw PCM track, and fix each
    item's frame count.

    Each segment is padded with silence to a whole number of video frames, so
    the video timeline is frame-exact and audio never drifts against it."""
    fps = spec.fps
    done = 0
    with open(pcm_path, "wb") as out:
        # Decode in batches: parallel enough to saturate the CPU, bounded so a
        # 400-verse render never holds the whole track in memory.
        batch = 24
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            for start in range(0, len(items), batch):
                if cancel and cancel():
                    return
                chunk = items[start:start + batch]
                pcms = list(pool.map(
                    lambda it: (_decode_pcm(ffmpeg, it.audio_path)
                                if it.audio_path else b""), chunk))
                for item, pcm in zip(chunk, pcms):
                    if item.kind == "title":
                        item.frames = max(1, round(DEFAULT_TITLE_SECONDS * fps))
                    else:
                        seconds = len(pcm) / PCM_BYTES_PER_SEC + spec.gap
                        item.frames = max(1, math.ceil(seconds * fps))
                    target = int(round(item.frames / fps * PCM_BYTES_PER_SEC))
                    target -= target % (CHANNELS * BYTES_PER_SAMPLE)
                    pcm = pcm[:target] + b"\x00" * max(0, target - len(pcm))
                    out.write(pcm)
                    done += 1
                    if on_progress:
                        on_progress(done, len(items), item.ref)

    assign_clocks(items, fps, spec.book)


def _continues(prev, item, book: str | None) -> bool:
    """Whether `item` shows the same picture as `prev` and so carries on its
    clock (D17). The very same file always does (a range file, or artwork
    held over a verse with no visual of its own). A byte-identical copy does
    within a chapter, as on the web, unless its family opts out with
    "replay_identical"."""
    if prev is None or item.svg_text != prev.svg_text:
        return False
    if item.svg_path and item.svg_path == prev.svg_path:
        return True
    if item.kind != "verse" or item.chapter != prev.chapter:
        return False
    family = svg_registry.owner_of(book, item.chapter, item.verse) if book else None
    return not (family and family.replay_identical)


def assign_clocks(items, fps: int, book: str | None = None) -> None:
    """Lay the items end to end (start_frame) and work out what of each one's
    picture still moves: clock_offset carries a shared picture's timeline
    over from the item before, and motion_seconds/motion_frames count only
    what is left of it after that offset (a play-once animation that has
    finished is a held still; a perpetual one keeps going)."""
    frame = 0
    prev = None
    for item in items:
        item.start_frame = frame
        frame += item.frames
        item.clock_offset = (prev.clock_offset + prev.duration(fps)
                             if _continues(prev, item, book) else 0.0)
        # motion_end answers on the picture's own clock.
        end = motion_end(item.svg_text, item.clock_offset + item.duration(fps))
        item.motion_seconds = max(0.0, end - item.clock_offset)
        item.motion_frames = min(item.frames,
                                 math.ceil(item.motion_seconds * fps))
        prev = item


# ---------------------------------------------------------------------------
# Pass 2 — video: headless Chrome frames -> one encoded segment per verse
# ---------------------------------------------------------------------------

PAGE_HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
  html, body {{ margin:0; padding:0; width:100%; height:100%;
                background:{bg}; overflow:hidden; }}
  #stage {{ position:absolute; inset:0; }}
  /* The artwork carries its own viewBox and the default preserveAspectRatio,
     so 100%/100% scales it to fill without ever distorting it. */
  #stage > svg {{ width:100%; height:100%; display:block; }}
</style></head><body><div id="stage">{svg}</div></body></html>"""


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class _CDP:
    """One DevTools Protocol connection (browser-level or per page)."""

    def __init__(self, ws):
        self.ws = ws
        self._id = 0
        self._pending: dict = {}
        self._pump = asyncio.create_task(self._read())

    async def _read(self):
        try:
            async for msg in self.ws:
                data = json.loads(msg.data)
                fut = self._pending.pop(data.get("id"), None)
                if fut and not fut.done():
                    fut.set_result(data)
        except asyncio.CancelledError:
            raise
        except Exception:
            pass
        for fut in self._pending.values():           # connection died
            if not fut.done():
                fut.set_exception(RenderError("the browser connection closed"))

    async def cmd(self, method: str, timeout: float = CMD_TIMEOUT, **params):
        self._id += 1
        fut = asyncio.get_running_loop().create_future()
        self._pending[self._id] = fut
        await self.ws.send_str(json.dumps(
            {"id": self._id, "method": method, "params": params}))
        try:
            res = await asyncio.wait_for(fut, timeout)
        except asyncio.TimeoutError:
            self._pending.pop(self._id, None)
            raise TimeoutError(f"{method} did not answer in {timeout:.0f}s")
        if "error" in res:
            raise RenderError(f"{method} failed: {res['error']}")
        return res.get("result", {})

    async def close(self):
        self._pump.cancel()
        try:
            await self.ws.close()
        except Exception:
            pass


class _Page:
    """A browser page pinned to the output resolution, used as a frame press:
    load a verse's SVG, seek its animation clock, screenshot."""

    def __init__(self, cdp: _CDP, target_id: str, width: int, height: int,
                 chrome=None):
        self.cdp = cdp
        self.target_id = target_id
        self.width = width
        self.height = height
        self.chrome = chrome
        self.frame_id = ""
        self.captures = 0
        self._svg = ""

    async def setup(self):
        await self.cdp.cmd("Page.enable")
        await self.cdp.cmd("Emulation.setDeviceMetricsOverride",
                           width=self.width, height=self.height,
                           deviceScaleFactor=1, mobile=False)
        tree = await self.cdp.cmd("Page.getFrameTree")
        self.frame_id = tree["frameTree"]["frame"]["id"]

    async def load(self, svg_text: str):
        self._svg = svg_text
        await self.cdp.cmd(
            "Page.setDocumentContent", frameId=self.frame_id,
            html=PAGE_HTML.format(bg=INK_BG, svg=svg_text))
        # Georgia is a system font, but waiting on the font set is what makes
        # the first captured frame identical to the hundredth.
        await self.cdp.cmd("Runtime.evaluate",
                           expression="document.fonts.ready", awaitPromise=True)
        await self.cdp.cmd(
            "Runtime.evaluate",
            expression="(()=>{const s=document.querySelector('svg');"
                       "if(s&&s.pauseAnimations)s.pauseAnimations();})()")

    async def frame_at(self, t: float) -> bytes:
        """The frame at animation time `t`, deterministically.

        The page is retired first if it has taken enough screenshots to be
        near the point where pages stop answering; the replacement reloads the
        same document, and because `t` is absolute the sequence continues
        seamlessly. A capture that still hangs is abandoned and re-issued
        rather than waited on -- one long render must not die on one sulky
        frame."""
        if self.captures >= PAGE_RECYCLE_CAPTURES and self.chrome is not None:
            await self.replace()
        self.captures += 1
        await self.cdp.cmd(
            "Runtime.evaluate",
            expression=f"(()=>{{const s=document.querySelector('svg');"
                       f"if(s&&s.setCurrentTime)s.setCurrentTime({t:.6f});}})()")
        for attempt in range(CAPTURE_RETRIES):
            try:
                shot = await self.cdp.cmd(
                    "Page.captureScreenshot", timeout=CAPTURE_TIMEOUT,
                    format="png", captureBeyondViewport=False)
                return base64.b64decode(shot["data"])
            except TimeoutError:
                if attempt == CAPTURE_RETRIES - 1:
                    raise
        raise RenderError("unreachable")

    async def replace(self):
        """Swap in a brand-new page after this one stops answering. The old
        target is closed on a best-effort basis -- a wedged renderer may not
        acknowledge that either, and the browser reaps it at shutdown."""
        if self.chrome is None:
            raise RenderError("this page cannot be replaced")
        try:
            await self.cdp.close()
            await self.chrome.browser.cmd("Target.closeTarget", timeout=10.0,
                                          targetId=self.target_id)
        except Exception:
            pass
        cdp, target_id = await self.chrome.open_target()
        self.cdp, self.target_id, self.frame_id = cdp, target_id, ""
        self.captures = 0
        await self.setup()
        if self._svg:
            await self.load(self._svg)


class Chrome:
    """Headless Chromium with a pool of pages, started for one render."""

    def __init__(self, exe: str, width: int, height: int, pages: int):
        self.exe = exe
        self.width = width
        self.height = height
        self.n_pages = pages
        self.proc = None
        self.profile = None
        self.session = None
        self.port = 0
        self.browser: _CDP | None = None
        self.pages: list[_Page] = []

    async def __aenter__(self):
        import aiohttp
        port = _free_port()
        self.profile = tempfile.mkdtemp(prefix="theoria-render-")
        self.proc = subprocess.Popen(
            [self.exe, "--headless=new", f"--remote-debugging-port={port}",
             f"--user-data-dir={self.profile}", "--no-first-run",
             "--no-default-browser-check", "--disable-extensions",
             "--disable-background-networking", "--disable-sync",
             "--mute-audio", "--hide-scrollbars",
             f"--window-size={self.width},{self.height}",
             "--force-device-scale-factor=1", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW)
        self.session = aiohttp.ClientSession()

        deadline = time.time() + 30
        ws_url = None
        while time.time() < deadline:
            if self.proc.poll() is not None:
                raise BrowserMissing("the browser exited during startup")
            try:
                async with self.session.get(
                        f"http://127.0.0.1:{port}/json/version") as resp:
                    ws_url = (await resp.json())["webSocketDebuggerUrl"]
                break
            except Exception:
                await asyncio.sleep(0.1)
        if not ws_url:
            raise BrowserMissing("the browser never opened a debugging port")

        self.port = port
        self.browser = _CDP(await self.session.ws_connect(ws_url,
                                                          max_msg_size=0))
        for _ in range(self.n_pages):
            cdp, target_id = await self.open_target()
            page = _Page(cdp, target_id, self.width, self.height, chrome=self)
            await page.setup()
            self.pages.append(page)
        return self

    async def open_target(self):
        """A fresh page target and a connection to it."""
        res = await self.browser.cmd("Target.createTarget", url="about:blank")
        target_id = res["targetId"]
        ws = await self.session.ws_connect(
            f"ws://127.0.0.1:{self.port}/devtools/page/{target_id}",
            max_msg_size=0)
        return _CDP(ws), target_id

    async def __aexit__(self, *exc):
        for page in self.pages:
            await page.cdp.close()
        if self.browser:
            await self.browser.close()
        if self.session:
            await self.session.close()
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        if self.profile:
            shutil.rmtree(self.profile, ignore_errors=True)


def _encode_threads(workers: int) -> int:
    """How many threads each concurrent encode may use.

    Left unbounded, x264 at 4K takes every core and starves the browser pages
    that are producing frames for the *other* workers -- captures that
    normally take 0.2 s were measured at 2.3 s while two encodes ran. Capping
    the encoders keeps the two halves of the pipeline from fighting."""
    cpus = os.cpu_count() or 4
    return max(2, (cpus - workers - 1) // max(1, workers))


def _encode_args(spec: RenderSpec, workers: int = 1) -> list:
    """Encoder settings shared by every segment. They must match exactly --
    the segments are concatenated with `-c:v copy`, so a mismatch would be
    rejected at the join."""
    return [
        "-c:v", "libx264", "-preset", "medium", "-crf", str(spec.crf),
        "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "5.2",
        "-g", str(spec.fps * 2), "-keyint_min", str(spec.fps),
        "-r", str(spec.fps), "-threads", str(_encode_threads(workers)), "-an",
    ]


async def _ffmpeg(cmd: list, log_path: str, label: str = ""):
    """Run one ffmpeg to completion.

    Nothing is piped in or out: frames reach ffmpeg as files on disk and
    stderr goes to a log file. Every hang this renderer has produced came from
    a pipe — either ffmpeg declining to drain stdin while the writer blocked
    on it, or the reverse — so the pipes are simply gone."""
    with open(log_path, "wb") as log:
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL, stderr=log,
            creationflags=CREATE_NO_WINDOW)
        try:
            await proc.wait()
        except BaseException:
            if proc.returncode is None:
                proc.kill()
                await proc.wait()
            raise
    if proc.returncode != 0:
        with open(log_path, "rb") as log:
            err = log.read().decode(errors="replace")
        raise RenderError(f"{label}: ffmpeg failed — {err[:300]}")


async def _capture_item(page: _Page, item: Item, spec: RenderSpec,
                        workdir: str, index: int) -> str | None:
    """Draw one item's frames to disk. Returns the motion frames' directory,
    or None if the item is a single held still."""
    await page.load(item.svg_text)

    still = await page.frame_at(item.clock_offset
                                + max(item.motion_seconds, 0.0))
    with open(os.path.join(workdir, f"still_{index:05d}.png"), "wb") as f:
        f.write(still)
    if not item.motion_frames:
        return None

    frames_dir = os.path.join(workdir, f"frames_{index:05d}")
    os.makedirs(frames_dir, exist_ok=True)
    for i in range(item.motion_frames):
        png = await page.frame_at(item.clock_offset + i / spec.fps)
        with open(os.path.join(frames_dir, f"{i:05d}.png"), "wb") as f:
            f.write(png)
    return frames_dir


async def _encode_item(item: Item, spec: RenderSpec, ffmpeg: str,
                       workdir: str, index: int, frames_dir: str | None,
                       jobs: int):
    """Encode one item's captured frames into up to two pieces."""
    log_path = os.path.join(workdir, f"log_{index:05d}.txt")
    try:
        if frames_dir:
            await _ffmpeg(
                [ffmpeg, "-y", "-v", "error", "-framerate", str(spec.fps),
                 "-i", os.path.join(frames_dir, "%05d.png")]
                + _encode_args(spec, jobs)
                + [os.path.join(workdir, f"seg_{index:05d}a.mp4")],
                log_path, label=item.ref)
    finally:
        if frames_dir:
            shutil.rmtree(frames_dir, ignore_errors=True)

    hold_frames = item.frames - item.motion_frames
    if hold_frames:
        await _ffmpeg(
            [ffmpeg, "-y", "-v", "error", "-loop", "1",
             "-framerate", str(spec.fps),
             "-t", f"{hold_frames / spec.fps:.6f}",
             "-i", os.path.join(workdir, f"still_{index:05d}.png")]
            + _encode_args(spec, jobs)
            + [os.path.join(workdir, f"seg_{index:05d}b.mp4")],
            log_path, label=item.ref)


async def render_segments(items, spec: RenderSpec, ffmpeg: str, browser: str,
                          workdir: str, on_progress=None, cancel=None):
    """Capture every item and encode it, into workdir/seg_NNNN[ab].mp4.

    Capture runs on ONE browser page, in order; encoding runs concurrently
    behind it. Splitting the two that way is deliberate. Driving several pages
    at once measured only ~1.5x faster per frame, and in a real render it
    wedged: pages stopped answering part-way through, every time. Encoding, by
    contrast, is just ffmpeg and parallelizes without touching the browser --
    and since a held still is most of every verse, encoding is the long pole.
    So the browser does one thing at a time and the encoders keep up behind
    it, which is both faster than the multi-page version and reliable.

    Capture runs at most `jobs` items ahead of encoding, bounding how many
    verses' frames sit on disk at once."""
    jobs = spec.workers or DEFAULT_ENCODE_JOBS
    jobs = max(1, min(jobs, MAX_ENCODE_JOBS))
    inflight = asyncio.Semaphore(jobs)
    tasks: list = []
    done = 0
    failure: list[Exception] = []

    async def encode(index: int, item: Item, frames_dir):
        nonlocal done
        try:
            if not failure:
                await _encode_item(item, spec, ffmpeg, workdir, index,
                                   frames_dir, jobs)
                done += 1
                if on_progress:
                    on_progress(done, len(items), item.ref)
        except Exception as e:
            failure.append(e)
        finally:
            inflight.release()

    async with Chrome(browser, spec.width, spec.height, 1) as chrome:
        page = chrome.pages[0]
        for index, item in enumerate(items):
            if failure or (cancel and cancel()):
                break
            await inflight.acquire()
            if failure or (cancel and cancel()):
                inflight.release()
                break
            for attempt in range(ITEM_ATTEMPTS):
                try:
                    frames_dir = await _capture_item(page, item, spec,
                                                     workdir, index)
                    break
                except TimeoutError as e:
                    # The page stopped answering. Give this item one more go
                    # on a fresh page before giving up on the render.
                    if attempt == ITEM_ATTEMPTS - 1:
                        failure.append(RenderError(
                            f"{item.ref}: the browser stopped responding ({e})"))
                        frames_dir = None
                        break
                    try:
                        await page.replace()
                    except Exception as replace_error:
                        failure.append(RenderError(
                            f"{item.ref}: could not restart the browser page "
                            f"— {replace_error}"))
                        frames_dir = None
                        break
                except Exception as e:
                    failure.append(e)
                    frames_dir = None
                    break
            if failure:
                inflight.release()
                break
            tasks.append(asyncio.create_task(encode(index, item, frames_dir)))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    if failure:
        raise failure[0]


# ---------------------------------------------------------------------------
# Pass 3 — mux
# ---------------------------------------------------------------------------

def mux(ffmpeg: str, items, spec: RenderSpec, workdir: str, pcm_path: str,
        out_path: str) -> None:
    """Join the segments and marry them to the narration.

    Video is stream-copied: it was encoded once, in pass 2, and is not touched
    again. Audio is encoded to AAC and loudness-normalized to -14 LUFS, which
    is what YouTube normalizes to -- doing it here means YouTube's own
    normalization becomes a no-op instead of pulling the whole video down."""
    list_path = os.path.join(workdir, "segments.txt")
    pieces = 0
    with open(list_path, "w", encoding="utf-8") as f:
        for index in range(len(items)):
            # 'a' is the animated reveal, 'b' the held still; a verse has one
            # or both, and they must stay in that order.
            for part in ("a", "b"):
                seg = os.path.join(workdir, f"seg_{index:05d}{part}.mp4")
                if not os.path.exists(seg):
                    continue
                f.write("file '" + seg.replace("\\", "/").replace("'", "'\\''")
                        + "'\n")
                pieces += 1
    if not pieces:
        raise RenderError("Nothing was rendered.")

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".",
                exist_ok=True)
    cmd = [
        ffmpeg, "-y", "-v", "error",
        "-f", "concat", "-safe", "0", "-i", list_path,
        "-f", "s16le", "-ar", str(SAMPLE_RATE), "-ac", str(CHANNELS),
        "-i", pcm_path,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "384k", "-ar", str(SAMPLE_RATE),
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
        "-movflags", "+faststart", "-shortest", out_path,
    ]
    res = _run(cmd)
    if res.returncode != 0:
        raise RenderError("ffmpeg mux failed — "
                          + res.stderr.decode(errors="replace")[:400])


# ---------------------------------------------------------------------------
# Sidecars — the things that make an upload good rather than merely present
# ---------------------------------------------------------------------------

def _stamp(seconds: float, srt: bool = False) -> str:
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if srt:
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(s % 1 * 1000):03d}"
    if h:
        return f"{int(h)}:{int(m):02d}:{int(s):02d}"
    return f"{int(m)}:{int(s):02d}"


def write_srt(items, spec: RenderSpec, path: str) -> None:
    """Captions carrying the verse text. Uploaded alongside the video they
    give YouTube something to index -- scripture video without captions is
    invisible to search -- without burning text onto the artwork."""
    fps = spec.fps
    lines = []
    n = 0
    for item in items:
        if item.kind != "verse" or not item.text.strip():
            continue
        n += 1
        start = item.start(fps)
        end = start + item.duration(fps) - spec.gap * 0.5
        lines.append(f"{n}\n{_stamp(start, True)} --> {_stamp(end, True)}\n"
                     f"{item.ref}\n{item.text.strip()}\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def chapter_markers(items, spec: RenderSpec) -> list:
    """Timestamps for the video description, obeying YouTube's rules: the
    first must be 0:00, there must be at least three, and none may be shorter
    than ten seconds.

    A passage spanning three or more Bible chapters marks the chapters. A
    shorter one marks runs of verses instead, each run grown until it clears
    the ten-second floor -- verses average 6-8 seconds, so one marker per
    verse would be rejected."""
    fps = spec.fps
    verses = [i for i in items if i.kind == "verse"]
    if not verses:
        return []

    marks = []
    chapters = sorted({i.chapter for i in verses})
    if len(chapters) >= 3:
        for chapter in chapters:
            first = next(i for i in verses if i.chapter == chapter)
            marks.append((first.start(fps), f"{spec.book} {chapter}"))
    else:
        run_first = None
        for item in verses:
            if run_first is None:
                run_first = item
            end = item.start(fps) + item.duration(fps)
            if end - run_first.start(fps) >= 12.0:
                label = (run_first.ref if run_first is item
                         else f"{run_first.ref}–{item.verse}")
                marks.append((run_first.start(fps), label))
                run_first = None
        if run_first is not None:                  # trailing short run
            label = (run_first.ref if run_first is verses[-1]
                     else f"{run_first.ref}–{verses[-1].verse}")
            marks.append((run_first.start(fps), label))

    out: list = []
    for at, label in marks:
        if not out:
            # The first marker must sit at 0:00, so it swallows the title card.
            out.append((0.0, label))
        elif at - out[-1][0] < 10.0:
            continue                               # too short to be a chapter
        else:
            out.append((at, label))
    # The last chapter runs to the end of the video, and it has to clear ten
    # seconds too -- a short tail invalidates the whole list, not just itself.
    total = sum(i.frames for i in items) / fps
    while len(out) > 1 and total - out[-1][0] < 10.0:
        out.pop()
    return out if len(out) >= 3 else []


def write_description(items, spec: RenderSpec, path: str,
                      duration: float) -> None:
    marks = chapter_markers(items, spec)
    body = [
        f"{spec.book} {spec.reference.replace(spec.book + ' ', '')} — "
        f"illustrated scripture",
        "",
        f"{spec.reference}, read aloud with an illustrated diagram for every "
        f"verse.",
        "",
        ATTRIBUTION,
        f"Narration: Microsoft neural voice ({spec.voice}).",
        "Visuals: original vector infographics, one per verse.",
    ]
    if marks:
        body += ["", "Chapters"]
        body += [f"{_stamp(at)} {label}" for at, label in marks]
    body += ["", f"Runtime {_stamp(duration)} · "
                 f"{spec.width}x{spec.height} @ {spec.fps}fps"]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(body) + "\n")


def write_thumbnail(ffmpeg: str, items, workdir: str, path: str) -> None:
    """A 1920x1080 JPEG grab of the first verse's settled frame -- YouTube's
    custom-thumbnail slot wants exactly that shape, under 2 MB."""
    index = next((n for n, i in enumerate(items) if i.kind == "verse"), 0)
    still = os.path.join(workdir, f"still_{index:05d}.png")
    if not os.path.exists(still):
        return
    _run([ffmpeg, "-y", "-v", "error", "-i", still,
          "-vf", "scale=1920:1080", "-q:v", "3", path])


# ---------------------------------------------------------------------------
# Top level
# ---------------------------------------------------------------------------

@dataclass
class RenderResult:
    out_path: str
    duration: float
    verses: int
    motion_frames: int
    seconds: float
    warnings: list = field(default_factory=list)
    sidecars: list = field(default_factory=list)


def render(spec: RenderSpec, on_status=None, on_progress=None,
           cancel=None) -> RenderResult:
    """Render `spec` to an MP4 plus its sidecar files.

    `on_status(text)` for phase messages, `on_progress(phase, done, total,
    label)` for the bars, `cancel()` polled between verses.
    """
    say = on_status or (lambda *_: None)
    ffmpeg = find_ffmpeg()
    browser = find_browser()
    started = time.time()

    items, warnings = build_plan(spec, on_status=say, cancel=cancel)
    if cancel and cancel():
        raise RenderError("Cancelled.")

    workdir = tempfile.mkdtemp(prefix="theoria-video-")
    try:
        say("Rendering narration…")
        pcm_path = os.path.join(workdir, "narration.pcm")
        build_audio(ffmpeg, items, spec, pcm_path,
                    on_progress=(lambda d, t, label:
                                 on_progress and on_progress("audio", d, t,
                                                             label)),
                    cancel=cancel)
        if cancel and cancel():
            raise RenderError("Cancelled.")

        say("Rendering frames…")
        asyncio.run(render_segments(
            items, spec, ffmpeg, browser, workdir,
            on_progress=(lambda d, t, label:
                         on_progress and on_progress("video", d, t, label)),
            cancel=cancel))
        if cancel and cancel():
            raise RenderError("Cancelled.")

        say("Muxing…")
        mux(ffmpeg, items, spec, workdir, pcm_path, spec.out_path)

        stem = os.path.splitext(spec.out_path)[0]
        sidecars = []
        write_srt(items, spec, stem + ".srt")
        sidecars.append(stem + ".srt")
        total = sum(i.frames for i in items) / spec.fps
        write_description(items, spec, stem + ".description.txt", total)
        sidecars.append(stem + ".description.txt")
        write_thumbnail(ffmpeg, items, workdir, stem + ".thumbnail.jpg")
        if os.path.exists(stem + ".thumbnail.jpg"):
            sidecars.append(stem + ".thumbnail.jpg")

        return RenderResult(
            out_path=spec.out_path, duration=total,
            verses=sum(1 for i in items if i.kind == "verse"),
            motion_frames=sum(i.motion_frames for i in items),
            seconds=time.time() - started,
            warnings=warnings, sidecars=sidecars)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("book")
    ap.add_argument("start", help="chapter or chapter:verse")
    ap.add_argument("end", nargs="?", help="chapter or chapter:verse")
    ap.add_argument("--out", default=None)
    ap.add_argument("--voice", default=tts_engine.HOUSE_VOICE)
    ap.add_argument("--resolution", default=DEFAULT_RESOLUTION,
                    choices=list(RESOLUTIONS))
    ap.add_argument("--fps", type=int, default=60, choices=FRAME_RATES)
    ap.add_argument("--gap", type=float, default=DEFAULT_GAP)
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--no-title", action="store_true")
    args = ap.parse_args()

    def split(ref, default_verse):
        chapter, _, verse = ref.partition(":")
        return int(chapter), (int(verse) if verse else default_verse)

    sc, sv = split(args.start, 1)
    ec, ev = split(args.end, None) if args.end else (sc, None)
    width, height = RESOLUTIONS[args.resolution]
    out = args.out or os.path.join(
        config.RENDERS_DIR, f"{args.book.replace(' ', '_')}_{sc}-{ec}.mp4")

    spec = RenderSpec(
        book=args.book, start_chapter=sc, start_verse=sv, end_chapter=ec,
        end_verse=ev, out_path=out, voice=args.voice, width=width,
        height=height, fps=args.fps, gap=args.gap, workers=args.workers,
        title_card=not args.no_title)

    def progress(phase, done, total, label):
        print(f"\r  {phase}: {done}/{total}  {label}".ljust(70), end="")

    try:
        result = render(spec, on_status=lambda s: print(f"\n{s}"),
                        on_progress=progress)
    except RenderError as e:
        print(f"\n{e}", file=sys.stderr)
        return 1
    print(f"\n\nWrote {result.out_path}")
    print(f"  {result.verses} verses · {_stamp(result.duration)} · "
          f"{result.motion_frames} frames captured · "
          f"rendered in {result.seconds / 60:.1f} min")
    for warning in result.warnings:
        print(f"  ! {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
