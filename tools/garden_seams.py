# -*- coding: utf-8 -*-
"""Genesis 2-3 on real frames, by hand: what garden_qc.py can't see from the geometry. It takes SMIL
frames through a headless Chromium browser, so it isn't run at generation.

    .venv\\Scripts\\python.exe tools\\garden_seams.py seams [folder]
    .venv\\Scripts\\python.exe tools\\garden_seams.py air [folder]

folder holds the verse files as <stem>.svg, a build not yet published; left out, it is what is
published under web/visuals/Genesis.

seams: each verse's end against the next verse's start, pixels over 40 of 255, largest first. A
chapter plays as one flight, so these should be small, and each large one is something to look at.
A verse opens on the last one's rest, but what moves on it, and a name's placing, can differ a
little.

air: a name's ink, from the frame with the names against the frame without them, grown by 3 px: is
anything of the picture under it a strong edge? That is over 70 of 255 in FIND_EDGES, which the
land's faint engraved lines are under. A name may sit on a flat or a gentle wash, never against a
line, a figure or the art. Over 6 such pixels is reported as TOUCHES, to be looked at. The frames
come from the story as the code tells it, on the clock, so that they follow a re-rendered MP3 (and
a folder should be a build of the same code): each name's first and last whole moments, the
verse's rest among them wherever a name is whole then, and, under a name over something that still
moves (SWEPT), a frame every SWEEP_S while it is whole: 3:24's wheel turns under its name. A few
px of difference on their own (a run of under INK_SPECK), away from any letter, are the captures',
not a name's ink, and are left out: on a river's bank they would read as a name against its line.

A capture can come out with a dark strip along the bottom of the frame. Such a frame is taken again.
A capture can also come out a little off in a way no strip shows, and then the difference between
the two frames is far more than the names' ink. So air takes each pair twice: if the two measures
of the names' ink disagree, both are taken again, and a frame whose captures never agree is said to
be unsteady and isn't judged, rather than reported as touching. Frames go in a temp folder, which
goes when the tool is done.
"""
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageChops, ImageFilter

# Run from anywhere: the repo is this file's parent folder.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config  # noqa: E402
import garden_stage as S  # noqa: E402
import video_render  # noqa: E402

THREADS = 4
RETRIES = 5
SEAM_OVER = 40              # of 255, a seam's pixel difference
GLITCHED = 3000             # a seam this far apart may be a capture's dark strip: take it again
NAME_INK_OVER = 30          # of 255, the difference that is a name's ink
INK_AGREES = (20, .05)      # two captures' ink agree within this many px, or this share of it
INK_SPECK = 6               # px: a run of difference smaller than this is no letter of a name
EDGE_OVER = 70              # of 255, in FIND_EDGES
TOUCHES = 6                 # strong edge pixels by a name, before it is reported
TITLE_BOX = (0, 0, 372, 52)
PAGE = (17, 20, 32)         # the colour of a capture's dark strip
SWEPT = ("a flaming sword",)    # names over something that still moves: 3:24's wheel
SWEEP_S = .2                # how often such a name is framed while it is whole
_TEXT = re.compile(r"<text\b.*?</text>", re.S)


def stem(ref):
    c, v = S.cv(ref)
    return f"{S.BOOK}_{c}_{v}"


def source(ref, folder):
    if folder:
        return os.path.join(folder, stem(ref) + ".svg")
    return os.path.join(str(config.VISUALS_DIR), S.BOOK, str(S.cv(ref)[0]), stem(ref) + ".svg")


def shoot(svg, t, work, tag):
    """A frame of an SVG's text at t seconds, its SMIL paused and set. -> the PNG's path."""
    page = os.path.join(work, tag + ".html")
    png = os.path.join(work, tag + ".png")
    with open(page, "w", encoding="utf-8") as f:
        f.write("<!doctype html><html><head><meta charset='utf-8'></head>"
                "<body style='margin:0;background:#000'>" + svg
                + "<script>const s=document.querySelector('svg');s.pauseAnimations();"
                f"s.setCurrentTime({t});</script></body></html>")
    with tempfile.TemporaryDirectory(dir=work) as profile:
        subprocess.run([video_render.find_browser(), "--headless=new", "--disable-gpu",
                        "--hide-scrollbars", "--window-size=1024,576",
                        f"--user-data-dir={profile}", "--virtual-time-budget=4000",
                        f"--screenshot={png}", "file:///" + page.replace("\\", "/")],
                       capture_output=True, timeout=120)
    return png


def glitched(png):
    """Whether the frame has the capture's dark strip along its bottom."""
    if not os.path.exists(png):
        return True
    im = Image.open(png).convert("RGB")
    spots = ((120, 572), (512, 572), (900, 572), (300, 560), (760, 560))
    return sum(sum(abs(a - b) for a, b in zip(im.getpixel(q), PAGE)) < 12 for q in spots) >= 4


def take(job):
    """A frame, taken again if it came out with the dark strip."""
    png = None
    for _ in range(RETRIES):
        png = shoot(*job)
        if not glitched(png):
            break
    return png


def over(a, b, level):
    d = ImageChops.difference(Image.open(a).convert("RGB"), Image.open(b).convert("RGB"))
    return sum(1 for v in d.convert("L").tobytes() if v > level)


def seams(folder, work):
    refs = S.chapter_refs(2) + S.chapter_refs(3)
    jobs = []
    for i, (a, b) in enumerate(zip(refs, refs[1:])):
        with open(source(a, folder), encoding="utf-8") as f:
            jobs.append((f.read(), S.verse_dur(a), work, f"seam{i}a"))
        with open(source(b, folder), encoding="utf-8") as f:
            jobs.append((f.read(), 0, work, f"seam{i}b"))
    with ThreadPoolExecutor(THREADS) as pool:
        frames = list(pool.map(take, jobs))
    rows = []
    for i, (a, b) in enumerate(zip(refs, refs[1:])):
        n = over(frames[2 * i], frames[2 * i + 1], SEAM_OVER)
        for _ in range(RETRIES):
            if n < GLITCHED:
                break
            frames[2 * i], frames[2 * i + 1] = take(jobs[2 * i]), take(jobs[2 * i + 1])
            n = min(n, over(frames[2 * i], frames[2 * i + 1], SEAM_OVER))
        rows.append((n, a, b))
    for n, a, b in sorted(rows, reverse=True):
        print(f"{a:>5s} -> {b:5s} {n:7d}")
    print(f"{sum(n < 20 for n, _a, _b in rows)} of {len(rows)} seams under 20 px")


def without_specks(mask, least=INK_SPECK):
    """A mask less its runs (8-connected) of fewer than `least` px."""
    w, h = mask.size
    on = bytearray(mask.tobytes())
    seen = bytearray(len(on))
    for i in range(len(on)):
        if not on[i] or seen[i]:
            continue
        run, todo = [], [i]
        seen[i] = 1
        while todo:
            j = todo.pop()
            run.append(j)
            x, y = j % w, j // w
            for k in (j - w - 1, j - w, j - w + 1, j - 1, j + 1, j + w - 1, j + w, j + w + 1):
                if 0 <= k < len(on) and abs(k % w - x) <= 1 and abs(k // w - y) <= 1 and on[k]                         and not seen[k]:
                    seen[k] = 1
                    todo.append(k)
        if len(run) < least:
            for j in run:
                on[j] = 0
    return Image.frombytes("L", (w, h), bytes(on))


def measure(on_png, off_png):
    """(the names' ink in px, the strong edges within 3 px of it) from a frame with the names and
    the same frame without them."""
    on = Image.open(on_png).convert("RGB")
    off = Image.open(off_png).convert("RGB")
    ink = ImageChops.difference(on, off).convert("L").point(
        lambda v: 255 if v > NAME_INK_OVER else 0)
    ink.paste(0, TITLE_BOX)
    ink = without_specks(ink)
    grown = ink.filter(ImageFilter.MaxFilter(7))
    edges = off.convert("L").filter(ImageFilter.FIND_EDGES).point(
        lambda v: 255 if v > EDGE_OVER else 0)
    edges.paste(0, (0, 0, 1024, 1))
    edges.paste(0, (0, 575, 1024, 576))
    return (sum(1 for v in ink.tobytes() if v),
            sum(1 for a, b in zip(grown.tobytes(), edges.tobytes()) if a and b))


def agree(a, b):
    """Whether two captures' measures of the names' ink are the same picture's."""
    return abs(a - b) <= max(INK_AGREES[0], INK_AGREES[1] * min(a, b))


def air_frames(story):
    """[(verse, time)]: each name's first and last whole moments, and every SWEEP_S through one in
    SWEPT, from the names each verse pins on its Flight as it is drawn."""
    out = set()
    for ref in S.chapter_refs(2) + S.chapter_refs(3):
        dur = story.verses[ref].dur
        story.verse_file(ref)
        for n in story.drawn[ref].names:
            first = 0.0 if n.t is None else min(dur, n.t + S.NAME_IN_S)
            last = dur if n.gone is None else n.gone[0]
            if last < first:
                continue
            times = {first, last}
            if n.text in SWEPT:
                times |= {first + i * SWEEP_S for i in range(int((last - first) / SWEEP_S) + 1)}
            out |= {(ref, round(t, 2)) for t in times}
    return sorted(out, key=lambda q: (S.cv(q[0]), q[1]))


def air(folder, work):
    frames_at = air_frames(S.build_story())
    jobs = []
    for i, (ref, t) in enumerate(frames_at):
        with open(source(ref, folder), encoding="utf-8") as f:
            svg = f.read()
        for k in (0, 1):
            jobs += [(svg, t, work, f"air{i}on{k}"), (_TEXT.sub("", svg), t, work, f"air{i}off{k}")]
    with ThreadPoolExecutor(THREADS) as pool:
        frames = list(pool.map(take, jobs))
    touching = unsteady = 0
    for i, (ref, t) in enumerate(frames_at):
        a, b = measure(*frames[4 * i:4 * i + 2]), measure(*frames[4 * i + 2:4 * i + 4])
        for k in range(RETRIES):
            if agree(a[0], b[0]):
                break
            again = [(*q[:3], f"{q[3]}r{k}") for q in jobs[4 * i:4 * i + 4]]
            a, b = (measure(take(again[0]), take(again[1])),
                    measure(take(again[2]), take(again[3])))
        if not agree(a[0], b[0]):
            print(f"{ref:5s} @{t:<5} the captures are unsteady: name ink {a[0]} and {b[0]} px. "
                  f"Not judged")
            unsteady += 1
            continue
        ink, n = a
        print(f"{ref:5s} @{t:<5} name ink {ink:6d} px   strong "
              f"edges within 3 px of it {n:5d}{'  TOUCHES' if n > TOUCHES else ''}")
        touching += n > TOUCHES
    print(f"{len(frames_at)} frames, {touching} to look at"
          + (f", {unsteady} not judged: their captures never agreed" if unsteady else ""))


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else ""
    if what not in ("seams", "air"):
        sys.exit(__doc__)
    folder = sys.argv[2] if len(sys.argv) > 2 else None
    with tempfile.TemporaryDirectory(prefix="garden_seams") as work:
        (seams if what == "seams" else air)(folder, work)


if __name__ == "__main__":
    main()
