# Video Studio: passages as finished videos

Video Studio renders a verse range to a single YouTube-ready MP4, built from assets the project already produces:
- the narration MP3s in `web/audio/`;
- the animated SVG pictures in `web/visuals/`.

Ranges cross chapters freely: a video is a *passage*, not a chapter.

- `video_render.py` is the engine. It is importable, and a CLI on its own.
- `video_studio.py` is the Tk front end. It opens from the Studio's **Video** button (Produce group), or with `python video_studio.py [Book] [chapter]`. How it follows the Studio's passage is in [studio.md](studio.md#video-video-studio-video_studiopy).

```bash
python video_render.py Genesis 1
python video_render.py "1 Chronicles" 1:1 9:44
```

The CLI takes `--out`, `--voice`, `--resolution`, `--fps`, `--gap`, `--workers` and `--no-title`. Without `--out` it writes `<Book>_<first>-<last chapter>.mp4` into `config.RENDERS_DIR` (see [What it writes](#what-it-writes)).

## Requirements

| | |
|---|---|
| **ffmpeg** | `winget install BtbN.FFmpeg.GPL`. On this machine winget installs the native **winarm64** build, so encoding is not emulated. `find_ffmpeg()` looks for it in this order: a portable copy in `tools/ffmpeg/bin/`; this process's `PATH`; winget's `Links` folder; then `PATH` as the registry has it, so a fresh install works without signing out. |
| **Chrome or Edge** | Used headless as the rasterizer. It is the same engine the Studio's stage and the website use, so the video matches the site. |

Everything else is in `requirements.txt`. The DevTools client is built on `aiohttp`.

## How it works

**Nothing in the Python stack renders SMIL.** resvg, Pillow and cairosvg all draw the `t=0` frame, so the animations, the whole point of these pictures, would be lost.

Frames therefore come from headless Chrome over the DevTools Protocol. They are driven deterministically rather than screen-recorded: `svg.pauseAnimations()`, then `svg.setCurrentTime(t)` per frame. A render is reproducible and can't drop or tear a frame.

Screenshotting 4K costs about 180 ms a frame, so capturing every frame of a long passage would be absurd. It is also unnecessary, because most pictures move only briefly:

| How the verse's SVG moves | Today | What is captured |
|---|---|---|
| A short play-once reveal | 1,224 SVGs (median about 1.7 s, at most 7 s) | the reveal |
| No animation at all | 918 | one frame |
| A loop that never settles (`repeatCount="indefinite"`: the Exodus 25–27 pulse, Genesis 3:24) | 99 | every frame of the verse |

So each verse becomes

```
[ motion frames captured at fps ]  +  [ one still frame held by ffmpeg ]
```

Render time is proportional to *seconds of animation*, not to video length. All of Genesis 1 holds about 7 s of motion across its 31 verses (about 420 frames at 60 fps), for a video over four minutes long.

### Pictures shared across verses (D17)

When a verse shows the same picture as the item before it, its frames continue that picture's clock (`Item.clock_offset`) instead of starting again at 0. Only the motion left after that offset is captured. So a finished reveal stays finished, and a loop carries on without a jump.

"The same picture" means one of two things:
- **The same file:** a range file `Book_c_v1-v2.svg`, or the previous verse's artwork held over a verse that has no picture of its own.
- **A byte-identical copy in the same chapter,** as on the website, unless its family sets `"replay_identical": true` in `svg_generators.json`.

A copy across a chapter boundary is *not* the same picture: it restarts.

`resolve_svg()` finds a verse's picture by path, most specific first: the verse's own file, then a range file covering it, then the chapter file. A verse with no picture holds the previous verse's artwork. If there is none, it gets a plain card with the reference.

### The three passes

1. **Audio.**
   - Each verse's MP3 is decoded to raw PCM and appended to one track.
   - Verses without a published MP3 are synthesized through `tts_engine.synthesize()` in the house voice. That is the same path, with the same pronunciation respelling, that the Audio Renderer uses, so an unpublished range still renders.
   - With "Also publish new narration to web/audio" ticked, freshly synthesized neural MP3s are also copied into `web/audio/` and its manifest. The offline SAPI fallback is never published. This option is planned to retire; the Audio Renderer covers it.
2. **Video.** One browser page captures frames, in order, while the ffmpeg encodes run concurrently behind it. A verse becomes up to two pieces, the reveal and then the held still. Separate ffmpeg runs encode them, reading frames as *files*, never through a pipe.
3. **Mux.** The pieces are joined with `-c:v copy`, so the video is encoded exactly once, and married to the narration.

Three details in step 2 are scars, and worth keeping:

- **One capture page, not several.** Driving several pages at once measured only about 1.5× faster per frame (180 ms → 122 ms), and it wedged in every real render: pages simply stopped answering part-way through. Once a held still is most of each verse, encoding is where the time goes, and encoding parallelizes without touching the browser. So the browser does one thing at a time and the encoders keep up behind it. That is faster than the multi-page version *and* reliable.
- **No pipes.** Frames reach ffmpeg as numbered files. Piping them deadlocked twice, in two different ways:
  - a mixed pipe/`-loop` input, where ffmpeg buffered the looped image until its filter queue filled and then stopped draining stdin;
  - later, a plain pipe that stalled on its own.

  Capture runs at most "encoder jobs" verses ahead of encoding, which bounds the motion frames on disk: each verse's frame folder is deleted once it is encoded. Each verse's held still (one PNG at the output resolution; the title card has one too) and its encoded pieces stay in the temporary work folder until the render finishes.
- **Encoders are thread-capped.** Left unbounded, x264 at 4K takes every core and starves the page producing frames. Captures that normally take 0.2 s were measured at 2.3 s while two encodes ran.

**Timeouts.**
- Every protocol call is bounded by a timeout, because a wedged renderer answers nothing forever, and a render that waits politely simply never finishes.
- An item whose page stops answering is retried once on a fresh page.
- A page is also retired after 40 captures, well short of where pages were seen to fail.
- Seeking is absolute, so a page can be replaced mid-verse without losing progress.

**A/V sync is exact by construction.** Each verse's narration is padded with silence out to a whole number of frames, and its segment is built to that same count, so nothing drifts over a 400-verse render.

## Render targets

The defaults are **3840×2160 at 60 fps**. Both are settable; here is the reasoning.

**4K is the right default, and it is nearly free here.**
- The artwork is vector, so it rasterizes perfectly at any size. 4K isn't upscaling; it's asking for more of what is already there.
- These are dense text-and-line infographics, and resolution is precisely what buys legibility on small labels.
- YouTube gates its codecs on resolution: uploads at 1440p and above are encoded with VP9 rather than AVC. So a 4K upload looks better **at every playback resolution**, 1080p included. Thin gold strokes on near-black are close to the worst case for AVC chroma, and that is exactly what these pictures are made of.

**60 fps costs almost nothing, because motion is a small fraction of the runtime.** At 30 fps Genesis 1 would capture about half as many frames, under a minute's difference on a chapter. The reveals are short opacity and stroke-dash animations, and they are visibly smoother at 60. The 30 fps option exists for a motion-heavy book where the capture pass does start to dominate.

**1440p and 1080p** are there for a quick proof, or for a passage you want turned around fast. 1080p drops below YouTube's VP9 threshold.

**Encoding.** The encoder is `libx264`, CRF 16, High profile, `yuv420p`, with a 2-second GOP. Audio is AAC 384 kbps at 48 kHz.

**The output bitrate looks low,** around 1–2 Mbps at 4K, because the content genuinely is simple. Mostly static flat vector art compresses to almost nothing at a CRF that is visually lossless. That is the source being efficient, not degraded. YouTube re-encodes from what it receives, and what it receives here is clean.

**Loudness.** Audio is normalized to **−14 LUFS**, which is what YouTube normalizes to, so YouTube's normalization becomes a no-op instead of pulling the whole video down.

## What it writes

The studio saves to `config.RENDERS_DIR`, which is `renders\` in the archive beside the repo (`C:\Dev\Theoria-archive\renders`). The default name is `<Book>_<chapter or chapters>.mp4`. "Save to" picks another path.

Beside `<name>.mp4`:

| file | what it's for |
|---|---|
| `.srt` | Captions carrying the verse text. Upload them: scripture video without captions is invisible to YouTube search, and captions keep the text off the artwork, where it doesn't belong. |
| `.description.txt` | A description for the description box. It has the WEB attribution line (`passages.ATTRIBUTION`), the narration voice and **chapter timestamps**. A passage of three or more Bible chapters marks the chapters. A shorter one marks runs of verses, each grown to at least 12 seconds, so every marker clears YouTube's ten-second minimum. |
| `.thumbnail.jpg` | A 1920×1080 grab of the first verse's settled frame, the shape YouTube's custom-thumbnail slot wants. It is a starting point, not a finished thumbnail. |

A title card (book, reference and attribution, 3 s) opens the video unless it is turned off.

## Uploading

- Upload the MP4 untouched. Don't re-encode it first: every extra generation costs quality, and YouTube is going to transcode anyway.
- Add the `.srt` under Subtitles, and paste the `.description.txt` chapters into the description. Chapters need to start at `0:00`, number at least three, and run at least ten seconds each. The generated file already obeys all three.
- Expect 4K processing to lag. YouTube publishes the low resolutions first, and the 2160p rendition can take hours to appear. The video is not broken.
- A custom thumbnail needs a verified channel.

## Options in the studio

| Option | Default |
|---|---|
| Resolution | 2160p |
| Frame rate | 60 fps (or 30) |
| Pause between verses | 0.45 s (0–2 s) |
| Open with a title card | on |
| Encoder jobs | 3 (1–4) |
| Also publish new narration to web/audio | off |

**Encoder jobs** is the throughput knob: how many verses may be encoding at once. Raising it past the point where the encoders saturate the machine is counterproductive, because the capture page has to share it.

There is no voice choice: verses without an MP3 are narrated in the house voice (`tts_engine.HOUSE_VOICE`).

## Measured

On this machine, at 4K60:

| | |
|---|---|
| Genesis 1: 31 verses, 4:21 of video | about 5 min, 495 frames captured (title card included) |
| Genesis 1:29–2:4: 7 verses, 1:04 | about 1.4 min |

That is roughly realtime, and dominated by encoding rather than capture. This is why the render time is much closer to *video length* than to verse count.
