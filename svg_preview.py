"""Faithful SMIL preview for the SVG Studio (SVG_STUDIO_DESIGN.md section 2).

One tiny local HTTP server, one wrapper page — served identically to the
embedded pywebview window and to the system-browser fallback, so the
fallback is "open the same URL in the default browser" and nothing else
changes. The page polls /state; when the studio bumps the generation
counter (debounced pane edits, verse navigation, Replay) the page
re-fetches /verse.svg and re-injects it inline — re-insertion is what
reliably restarts SMIL from t=0 — and, on navigation/replay (not on
keystrokes), restarts the verse's narration MP3 alongside it.

The server binds 127.0.0.1 on an ephemeral port and runs on a daemon
thread. The studio pushes content with set_content(); that lock-guarded
snapshot is the entire cross-thread surface.
"""

import http.server
import json
import os
import sys
import threading
import time
import urllib.request

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(REPO_ROOT, "web", "audio")

PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>SVG Studio preview</title>
<style>
  body { background: #101018; color: #d8c68f; margin: 0;
         font-family: Georgia, serif; display: flex; flex-direction: column;
         min-height: 100vh; }
  #stage { flex: 1; display: flex; align-items: center;
           justify-content: center; padding: 12px; }
  #stage svg { max-width: 100%; max-height: calc(100vh - 70px);
               height: auto; }
  #bar { padding: 8px 14px; display: flex; gap: 14px; align-items: center;
         background: #181824; }
  button { background: #2a2a3a; color: #d8c68f; border: 1px solid #555;
           padding: 4px 14px; font-family: Georgia, serif; cursor: pointer; }
  #ref { font-style: italic; }
  #err { color: #cc7777; font-size: 13px; }
</style>
</head>
<body>
<div id="stage"></div>
<div id="bar">
  <button id="replay">Replay &#9654;</button>
  <span id="ref"></span>
  <span id="err"></span>
</div>
<audio id="narration"></audio>
<script>
  let gen = -1;
  let lastState = null;

  async function tick() {
    let s;
    try {
      s = await (await fetch("/state")).json();
    } catch (e) {
      return; // studio closed or restarting; keep polling quietly
    }
    if (s.gen !== gen) {
      gen = s.gen;
      lastState = s;
      await reload(s, s.cause !== "edit");
    }
  }

  async function reload(s, withAudio) {
    const err = document.getElementById("err");
    err.textContent = "";
    let svg = "";
    try {
      svg = await (await fetch("/verse.svg?g=" + gen)).text();
    } catch (e) {
      err.textContent = "fetch failed";
      return;
    }
    // Re-inserting inline SVG restarts its SMIL animations from t=0.
    document.getElementById("stage").innerHTML = svg;
    document.getElementById("ref").textContent = s.ref || "";
    const a = document.getElementById("narration");
    document.getElementById("replay").style.opacity = s.audio ? 1 : 0.4;
    if (withAudio && s.audio) {
      a.src = "/verse.mp3?g=" + gen;
      a.currentTime = 0;
      // Browsers block autoplay before a user gesture; the embedded
      // window disables that policy via browser args. Swallow the
      // rejection — the Replay button is the designed gesture.
      a.play().catch(() => {});
    } else if (!s.audio) {
      a.removeAttribute("src");
    }
  }

  document.getElementById("replay").onclick = () => {
    if (lastState) reload(lastState, true);
  };
  setInterval(tick, 500);
  tick();
</script>
</body>
</html>
"""


def resolve_audio(book: str, chapter: int, verse: int,
                  variant: str) -> str | None:
    """The narration MP3 for a verse, honoring the audio manifest's naming:
    translation-suffixed files (Book_c_v.KJV.mp3) for non-WEB narration,
    plain Book_c_v.mp3 for WEB. A translation variant prefers its own
    narration and falls back to the plain (WEB) file; the generic variant
    plays the plain file."""
    base = f"{book.replace(' ', '_')}_{chapter}_{verse}"
    candidates = [f"{base}.mp3"]
    if variant not in ("generic", "", None, "WEB"):
        candidates.insert(0, f"{base}.{variant}.mp3")
    for name in candidates:
        path = os.path.join(AUDIO_DIR, name)
        if os.path.exists(path):
            return path
    return None


class PreviewServer:
    """Serves the wrapper page, the working SVG buffer, the verse MP3 and
    the generation state. start() binds an ephemeral port; .url is the
    address both preview hosts open."""

    def __init__(self):
        self._lock = threading.Lock()
        self._gen = 0
        self._svg = b"<svg xmlns='http://www.w3.org/2000/svg'/>"
        self._audio_path = None
        self._ref = ""
        self._cause = "nav"
        self._httpd = None
        self._thread = None

    # ----- studio-side API (main thread) ------------------------------------

    def set_content(self, svg_text: str, audio_path: str | None,
                    ref: str, cause: str):
        """Publish a new snapshot. cause is 'nav' (navigation/replay: page
        restarts narration too) or 'edit' (debounced keystrokes: silent
        re-inject so the MP3 doesn't stutter while typing)."""
        with self._lock:
            self._gen += 1
            self._svg = svg_text.encode("utf-8")
            self._audio_path = audio_path
            self._ref = ref
            self._cause = cause

    def snapshot(self):
        with self._lock:
            return (self._gen, self._svg, self._audio_path, self._ref,
                    self._cause)

    @property
    def url(self) -> str:
        host, port = self._httpd.server_address[:2]
        return f"http://127.0.0.1:{port}/preview.html"

    def start(self):
        if self._httpd is not None:
            return
        server = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass  # keep the studio's console quiet

            def _send(self, code, ctype, body, ranges_none=False):
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                if ranges_none:
                    # http.server has no range support; telling Chromium so
                    # up front makes <audio> take the whole-file response.
                    self.send_header("Accept-Ranges", "none")
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                path = self.path.split("?")[0]
                gen, svg, audio_path, ref, cause = server.snapshot()
                try:
                    if path in ("/", "/preview.html"):
                        self._send(200, "text/html; charset=utf-8",
                                   PAGE.encode("utf-8"))
                    elif path == "/verse.svg":
                        self._send(200, "image/svg+xml; charset=utf-8", svg)
                    elif path == "/state":
                        body = json.dumps({
                            "gen": gen, "audio": bool(audio_path),
                            "ref": ref, "cause": cause,
                        }).encode("utf-8")
                        self._send(200, "application/json", body)
                    elif path == "/verse.mp3" and audio_path:
                        with open(audio_path, "rb") as f:
                            self._send(200, "audio/mpeg", f.read(),
                                       ranges_none=True)
                    else:
                        self._send(404, "text/plain", b"not found")
                except (ConnectionAbortedError, BrokenPipeError):
                    pass  # page navigated away mid-response; harmless

        self._httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0),
                                                      Handler)
        self._thread = threading.Thread(target=self._httpd.serve_forever,
                                        daemon=True)
        self._thread.start()

    def stop(self):
        if self._httpd is not None:
            self._httpd.shutdown()
            self._httpd.server_close()
            self._httpd = None
            self._thread = None


# ---------------------------------------------------------------------------
# Embedded-window host. Run as a subprocess by the studio:
#
#     python svg_preview.py --url http://127.0.0.1:PORT/preview.html
#
# pywebview's webview.start() blocks and owns its own (WinForms) message
# pump, which is exactly why this never runs inside the studio's tkinter
# process (SVG_STUDIO_DESIGN.md section 2.3 / 7.2). All state flows over
# HTTP; the only IPC is the URL argument. Exit codes: 0 = window closed
# normally, 3 = pywebview missing/broken (studio falls back to the system
# browser and persists that choice).
# ---------------------------------------------------------------------------

def _orphan_watchdog(url: str, destroy):
    """Close the window if the studio's server stops answering — covers a
    hard-killed studio that could not terminate its child."""
    base = url.rsplit("/", 1)[0]
    misses = 0
    while True:
        time.sleep(3)
        try:
            urllib.request.urlopen(base + "/state", timeout=2).read()
            misses = 0
        except Exception:
            misses += 1
            if misses >= 4:  # ~12s unreachable
                try:
                    destroy()
                finally:
                    os._exit(0)


def run_embedded(url: str) -> int:
    # WebView2 honors this Chromium switch, letting the narration MP3
    # autoplay on reload without a click (the system browser does not,
    # which is why the page also has a Replay button).
    os.environ.setdefault(
        "WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS",
        "--autoplay-policy=no-user-gesture-required")
    try:
        import webview
    except Exception as e:  # ImportError, or pythonnet/clr-loader blowups
        print(f"pywebview unavailable: {e}", file=sys.stderr)
        return 3
    try:
        window = webview.create_window("SVG Studio preview", url,
                                       width=1104, height=736,
                                       background_color="#101018")
        threading.Thread(target=_orphan_watchdog,
                         args=(url, window.destroy), daemon=True).start()
        webview.start()
    except Exception as e:
        print(f"pywebview failed to start: {e}", file=sys.stderr)
        return 3
    return 0


def main() -> int:
    args = sys.argv[1:]
    if len(args) >= 2 and args[0] == "--url":
        return run_embedded(args[1])
    print("usage: svg_preview.py --url http://127.0.0.1:PORT/preview.html",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
