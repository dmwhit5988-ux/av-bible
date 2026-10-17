# Video Studio — passages as finished videos

Renders a verse range to a single YouTube-ready MP4 out of assets the project
already produces: the narration MP3s in `web/audio/` and the animated SVG
visuals in `visuals/`. Ranges cross chapters freely — a video is a *passage*,
not a chapter.

- `video_render.py` — the engine. Importable, and a CLI on its own.
- `video_studio.py` — the Tk front end, opened from the main app's
  **🎬 Video Studio** button (or `python video_studio.py`).

```bash
python video_render.py Genesis 1
python video_render.py "1 Chronicles" 1:1 9:44 --out renders/Chronicles.mp4
```

## Requirements

| | |
|---|---|
| **ffmpeg** | `winget install BtbN.FFmpeg.GPL` — the only new dependency. On this machine winget installs the native **winarm64** build, so encoding is not emulated. Found automatically via PATH, winget's shim dir, or the registry's PATH (so a fresh install works without signing out). A copy in `tools/ffmpeg/bin/` also works, for a portable install. |
| **Chrome or Edge** | Already present. Used headless as the rasterizer — the same engine the stage and the web app use, so the video matches the app exactly. |

Everything else is already in `requirements.txt`; the DevTools client is built
on `aiohttp`, which arrives with `edge-tts`.

## How it works

**Nothing in the Python stack renders SMIL.** resvg, Pillow and cairosvg all
draw the `t=0` frame, so the animations — the whole point of these visuals —
would be lost. Frames therefore come from headless Chrome over the DevTools
Protocol, driven deterministically rather than screen-recorded:
`svg.pauseAnimations()`, then `svg.setCurrentTime(t)` per frame. A render is
reproducible and cannot drop or tear a frame.

Screenshotting 4K costs ~180 ms/frame, so rendering every frame of a long
passage would be absurd — and unnecessary. Each verse's SVG plays a short
reveal (0.8–4 s, always `fill="freeze"`) and is a **still** for the rest of
the narration. So each verse becomes

```
[ motion frames captured at fps ]  +  [ one still frame held by ffmpeg ]
```

Render time is proportional to *seconds of animation*, not to video length.
All of Genesis 1 contains 7.0 s of motion across its 31 verses — 422 frames at
60 fps — for a video several minutes long.

The three passes:

1. **Audio.** Each verse's MP3 is decoded to raw PCM and appended to one
   track. Verses without a published MP3 are synthesized through
   `tts_engine.synthesize()` — the same production path, and the same
   pronunciation respelling, the desktop reader uses — so an unpublished range
   still renders. Optionally the fresh audio is published to `web/audio/` on
   the way past, making a render double as an Audio Renderer pass.
2. **Video.** One browser page captures frames, in order; the ffmpeg encodes
   run concurrently behind it. A verse becomes up to two pieces — the reveal,
   then the held still — encoded by separate ffmpeg runs reading frames as
   *files*, never through a pipe.
3. **Mux.** Pieces are joined with `-c:v copy` — the video is encoded exactly
   once — and married to the narration.

Three details in step 2 are scars, and worth keeping:

- **One capture page, not several.** Driving several pages at once measured
  only ~1.5× faster per frame (180 ms → 122 ms) and wedged in every real
  render — pages simply stopped answering part-way through. Encoding, which is
  where the time actually goes once a held still is most of each verse,
  parallelizes without touching the browser. So the browser does one thing at
  a time and the encoders keep up behind it: faster than the multi-page
  version *and* reliable.
- **No pipes.** Frames reach ffmpeg as numbered files. Piping them deadlocked
  twice, in two different ways — a mixed pipe/`-loop` input where ffmpeg
  buffered the looped image until its filter queue filled and stopped draining
  stdin, and later a plain pipe that stalled on its own. Only one verse's
  frames exist at a time, so the disk cost never grows with the passage.
- **Encoders are thread-capped.** Left unbounded, x264 at 4K takes every core
  and starves the page producing frames; captures that normally take 0.2 s
  were measured at 2.3 s while two encodes ran.

Every protocol call is bounded by a timeout, and an item whose page stops
answering is retried once on a fresh page — a wedged renderer answers nothing
forever, and a render that waits politely simply never finishes. Because
seeking is absolute, a page can be replaced mid-verse without losing progress.

**A/V sync is exact by construction.** Each verse's narration is padded with
silence out to a whole number of frames and its segment is built to that same
count, so nothing drifts over a 400-verse render.

## Render targets

Defaults are **3840×2160 at 60 fps**. The reasoning, since both are settable:

**4K is the right default, and it is nearly free here.** The artwork is
vector, so it rasterizes perfectly at any size — 4K isn't upscaling, it's just
asking for more of what's already there. Two things follow. First, these are
dense text-and-line infographics, and resolution is precisely what buys
legibility on small labels. Second, YouTube gates its codecs on resolution:
uploads at 1440p and above are encoded with VP9 rather than AVC, so a 4K
upload looks better **at every playback resolution**, 1080p included. Thin
gold strokes on near-black are close to the worst case for AVC chroma, and
that is exactly what these visuals are made of.

**60 fps costs almost nothing, because motion is a small fraction of the
runtime.** At 30 fps Genesis 1 would capture 211 frames instead of 422 — under
a minute's difference on a chapter. The reveals are short opacity and
stroke-dash animations that are visibly smoother at 60. Keep it. The 30 fps
option exists for a motion-heavy book where the capture pass does start to
dominate.

**1440p and 1080p** are there for a quick proof, or for a passage you want
turned around fast. 1080p drops below YouTube's VP9 threshold.

The encoder is `libx264`, CRF 16, High profile, `yuv420p`, 2-second GOP, with
AAC 384 kbps at 48 kHz. **The output bitrate looks low** — around 1–2 Mbps at
4K — because the content genuinely is simple: mostly-static flat vector art
compresses to almost nothing at a CRF that is visually lossless. That is the
source being efficient, not the source being degraded; YouTube re-encodes from
what it receives, and what it receives here is clean.

Audio is normalized to **−14 LUFS**, which is what YouTube normalizes to, so
their normalization becomes a no-op instead of pulling the whole video down.

## What it writes

Beside `<name>.mp4`:

| file | what it's for |
|---|---|
| `.srt` | Captions carrying the verse text. Upload them — scripture video without captions is invisible to YouTube search, and this keeps the text off the artwork, where it doesn't belong. |
| `.description.txt` | A description with translation attribution and **chapter timestamps**, already formatted for the description box. A passage of three or more Bible chapters marks the chapters; a shorter one marks runs of verses grown past YouTube's ten-second minimum. |
| `.thumbnail.jpg` | 1920×1080 grab of the first verse's settled frame — the shape YouTube's custom-thumbnail slot wants. A starting point, not a finished thumbnail. |

`renders/` is gitignored.

## Uploading

- Upload the MP4 untouched. Don't re-encode it first; every extra generation
  costs quality and YouTube is going to transcode anyway.
- Add the `.srt` under Subtitles, and paste the `.description.txt` chapters
  into the description. Chapters need to start at `0:00`, number at least
  three, and run at least ten seconds each — the generated file already obeys
  all three.
- Expect 4K processing to lag: YouTube publishes the low resolutions first and
  the 2160p rendition can take hours to appear. The video is not broken.
- A custom thumbnail needs a verified channel.

## Options in the studio

Resolution · frame rate · pause between verses (default 0.45 s) · title card ·
encoder jobs · publish new narration to `web/audio/`.

**Encoder jobs** is the throughput knob — how many verses may be encoding at
once (default 3). Raising it past the point where the encoders saturate the
machine is counterproductive, because the capture page has to share it.

## Measured

On this machine, at 4K60:

| | |
|---|---|
| Genesis 1 — 31 verses, 4:21 of video | ~5 min, 495 frames captured |
| Genesis 1:29–2:4 — 7 verses, 1:04 | ~1.4 min |

Roughly realtime, and dominated by encoding rather than capture — which is
why the render time is much closer to *video length* than to verse count.
