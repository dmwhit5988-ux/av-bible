"""Embedded web view for SVG verse visuals on the PC stage.

tkinter cannot render SVG (let alone SMIL animation), so .svg visuals get
the same engine the web app uses: a real Chromium (WebView2) page. The
moving parts mirror the SVG Studio preview (svg_preview.py), which proved
the pattern on this machine:

- `StageServer` — a tiny local HTTP server owned by the stage. The stage
  publishes the current verse's SVG + reference text; a wrapper page polls
  /state and re-injects the SVG inline whenever the generation counter
  bumps. Re-insertion restarts SMIL from t=0, so animations replay from
  the top of each verse exactly like the WebP path does.

- A child process (this file run with --url/--parent) hosts a frameless
  pywebview window and *reparents it into the stage's Tk frame* with
  Win32 SetParent, so it looks and resizes like a native embedded panel.
  pywebview owns its own message pump and must never run inside the
  tkinter process (SVG_STUDIO_DESIGN.md 2.3/7.2) — cross-process
  reparenting keeps that rule while still embedding the view.

- `WebPanel` — the parent-side handle: a Tk frame placed over the stage
  canvas plus the child process. If the child dies early (pywebview or
  WebView2 broken), SVG support is marked unavailable for the session and
  the stage falls back to the raster (.webp/.png) visuals it used before.
"""

import http.server
import json
import os
import subprocess
import sys
import threading
import time
import tkinter as tk
import urllib.request

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# How soon a child exit counts as "the web view is broken" rather than a
# normal shutdown (same heuristic as the studio's embedded preview).
FAIL_WINDOW_SEC = 10

_available = True
_fail_reason = ""


def available() -> bool:
    """Whether .svg visuals should be offered to the stage at all."""
    return _available


def mark_unavailable(reason: str):
    global _available, _fail_reason
    _available = False
    _fail_reason = reason


PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AV Bible stage</title>
<style>
  html, body { height: 100%; }
  body { background: #101018; margin: 0; overflow: hidden;
         font-family: Georgia, serif; }
  #stage { position: absolute; inset: 0; display: flex;
           align-items: center; justify-content: center; }
  #stage svg { max-width: 100vw; max-height: 100vh;
               width: auto; height: auto; }
  .band { position: absolute; left: 50%; transform: translateX(-50%);
          background: rgba(0,0,0,0.55); color: #d8c68f;
          padding: 4px 16px; border-radius: 3px; white-space: nowrap;
          max-width: 92vw; overflow: hidden; text-overflow: ellipsis; }
  #ref { bottom: 4vh; font-style: italic; font-size: calc(11px + 0.8vw); }
  #notes { bottom: 12vh; color: #e8e0cc; font-style: italic;
           font-size: calc(9px + 0.5vw); white-space: normal;
           text-align: center; }
  .hidden { display: none; }
</style>
</head>
<body>
<div id="stage"></div>
<div id="notes" class="band hidden"></div>
<div id="ref" class="band hidden"></div>
<script>
  let gen = -1;

  async function tick() {
    let s;
    try {
      s = await (await fetch("/state")).json();
    } catch (e) {
      return; // stage closed or restarting; keep polling quietly
    }
    if (s.gen === gen) return;
    gen = s.gen;
    let svg = "";
    try {
      svg = await (await fetch("/verse.svg?g=" + gen)).text();
    } catch (e) {
      return;
    }
    // Re-inserting inline SVG restarts its SMIL animations from t=0 —
    // the equivalent of _Animation.restart() on the canvas path.
    document.getElementById("stage").innerHTML = svg;
    const ref = document.getElementById("ref");
    ref.textContent = s.ref || "";
    ref.classList.toggle("hidden", !s.ref);
    const notes = document.getElementById("notes");
    if (s.notes && s.notes.length) {
      notes.textContent = "Translator-supplied words:  "
        + s.notes.map(n => "\\u201C" + n + "\\u201D").join("   ");
      notes.classList.remove("hidden");
    } else {
      notes.classList.add("hidden");
    }
  }
  setInterval(tick, 250);
  tick();
</script>
</body>
</html>
"""


class StageServer:
    """Publishes the current verse's SVG to however many embedded panels
    are open (the in-app stage and the fullscreen mirror each run their
    own child window; both poll the same server, so they stay in sync
    the same way canvas views share the wall clock)."""

    def __init__(self):
        self._lock = threading.Lock()
        self._gen = 0
        self._key = None
        self._svg = b"<svg xmlns='http://www.w3.org/2000/svg'/>"
        self._ref = ""
        self._notes = []
        self._httpd = None
        self._thread = None

    def set_verse(self, key, svg_path: str, ref: str, notes) -> bool:
        """Publish a verse's SVG. `key` identifies the (verse, file)
        combination — repeat calls with the same key (window resizes,
        the second stage view redrawing) do NOT bump the generation, so
        SMIL only restarts when the verse or file actually changes."""
        with self._lock:
            if key == self._key:
                return False
            with open(svg_path, "rb") as f:
                svg = f.read()
            self._key = key
            self._gen += 1
            self._svg = svg
            self._ref = ref or ""
            self._notes = list(notes or [])
            return True

    def clear(self):
        """Forget the current verse so the next set_verse always pushes
        (used when leaving the SVG path, e.g. verse without an SVG)."""
        with self._lock:
            self._key = None

    def snapshot(self):
        with self._lock:
            return self._gen, self._svg, self._ref, self._notes

    @property
    def url(self) -> str:
        host, port = self._httpd.server_address[:2]
        return f"http://127.0.0.1:{port}/stage.html"

    def start(self, port=0):
        if self._httpd is not None:
            return
        server = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def _send(self, code, ctype, body):
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                path = self.path.split("?")[0]
                gen, svg, ref, notes = server.snapshot()
                try:
                    if path in ("/", "/stage.html"):
                        self._send(200, "text/html; charset=utf-8",
                                   PAGE.encode("utf-8"))
                    elif path == "/verse.svg":
                        self._send(200, "image/svg+xml; charset=utf-8", svg)
                    elif path == "/state":
                        body = json.dumps({"gen": gen, "ref": ref,
                                           "notes": notes}).encode("utf-8")
                        self._send(200, "application/json", body)
                    else:
                        self._send(404, "text/plain", b"not found")
                except (ConnectionAbortedError, BrokenPipeError):
                    pass

        self._httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port),
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


class WebPanel:
    """Parent-side handle for one embedded web view: a Tk frame placed
    over a stage canvas, filled by a child-process WebView2 window."""

    def __init__(self, parent_widget: tk.Widget, url: str, on_fail=None):
        self.frame = tk.Frame(parent_widget, bg="#101018")
        self.url = url
        self.on_fail = on_fail
        self.proc: subprocess.Popen | None = None
        self._started_at = None

    def show(self):
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)
        self._ensure_proc()

    def hide(self):
        self.frame.place_forget()

    def destroy(self):
        if self.proc is not None and self.proc.poll() is None:
            self.proc.terminate()
        self.proc = None
        if self.frame.winfo_exists():
            self.frame.destroy()

    def _ensure_proc(self):
        if not _available:
            return
        if self.proc is not None and self.proc.poll() is None:
            return
        if self.proc is not None and self.proc.poll() not in (None, 0):
            # Died once already — a nonzero exit means pywebview/WebView2
            # is broken, not a user action (nobody can close a child
            # window). Give up for the session.
            self._fail(f"exit code {self.proc.poll()}")
            return
        # The frame must be realized before winfo_id() names a real HWND.
        self.frame.update_idletasks()
        script = os.path.join(REPO_ROOT, "svg_stage.py")
        try:
            self.proc = subprocess.Popen(
                [sys.executable, script, "--url", self.url,
                 "--parent", str(self.frame.winfo_id())])
        except OSError as e:
            self._fail(str(e))
            return
        self._started_at = time.time()
        proc = self.proc
        self.frame.after(FAIL_WINDOW_SEC * 1000,
                         lambda: self._check_alive(proc))

    def _check_alive(self, proc):
        if proc is not self.proc:
            return
        code = proc.poll()
        if code not in (None, 0):
            self._fail(f"exit code {code}")

    def _fail(self, why: str):
        mark_unavailable(why)
        self.hide()
        if self.on_fail:
            self.on_fail(why)


# ---------------------------------------------------------------------------
# Child process: a frameless pywebview window reparented into the stage
# frame. Run as:
#
#     python svg_stage.py --url http://127.0.0.1:PORT/stage.html --parent HWND
#
# Exit codes: 0 = normal shutdown, 3 = pywebview missing/broken (parent
# marks SVG support unavailable and falls back to raster visuals).
# ---------------------------------------------------------------------------

def _embed_and_track(window, parent_hwnd: int):
    """Reparent the pywebview window under the Tk frame, then keep it
    sized to the frame and exit when the frame (or the app) goes away."""
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32

    GWL_STYLE = -16
    WS_CHILD = 0x40000000
    WS_VISIBLE = 0x10000000
    WS_CLIPSIBLINGS = 0x04000000

    hwnd = None
    for _ in range(200):  # native handle appears once the window is shown
        native = getattr(window, "native", None)
        handle = getattr(native, "Handle", None)
        if handle is not None:
            try:
                hwnd = handle.ToInt64()
            except AttributeError:
                hwnd = int(str(handle))
            break
        time.sleep(0.05)
    if not hwnd:
        os._exit(3)

    # WS_CHILD before SetParent, per the SetParent contract.
    user32.SetWindowLongPtrW(wintypes.HWND(hwnd), GWL_STYLE,
                             WS_CHILD | WS_VISIBLE | WS_CLIPSIBLINGS)
    user32.SetParent(wintypes.HWND(hwnd), wintypes.HWND(parent_hwnd))

    rect = wintypes.RECT()
    last = None
    while True:
        if not user32.IsWindow(wintypes.HWND(parent_hwnd)):
            try:
                window.destroy()
            finally:
                os._exit(0)
        user32.GetClientRect(wintypes.HWND(parent_hwnd), ctypes.byref(rect))
        size = (rect.right, rect.bottom)
        if size != last and size[0] > 0 and size[1] > 0:
            user32.MoveWindow(wintypes.HWND(hwnd), 0, 0,
                              size[0], size[1], True)
            last = size
        time.sleep(0.15)


def _orphan_watchdog(url: str, destroy):
    """Exit if the stage's server stops answering — covers a hard-killed
    app that could not terminate its children."""
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


def _adopt_parent_dpi_awareness(parent_hwnd: int):
    """Match the stage process's DPI-awareness context before pywebview
    (or WebView2) can set its own. This child and Tk must measure the
    parent frame in the same units — with mismatched awareness at, say,
    200% display scaling, the embedded view comes out twice the panel
    size and its centered content drifts off the visible edge."""
    import ctypes
    from ctypes import wintypes
    try:
        user32 = ctypes.windll.user32
        user32.GetWindowDpiAwarenessContext.restype = ctypes.c_void_p
        user32.GetWindowDpiAwarenessContext.argtypes = [wintypes.HWND]
        user32.SetProcessDpiAwarenessContext.argtypes = [ctypes.c_void_p]
        ctx = user32.GetWindowDpiAwarenessContext(parent_hwnd)
        if ctx:
            user32.SetProcessDpiAwarenessContext(ctx)
    except Exception:
        pass  # pre-Win10-1607 fallback: keep pywebview's default


def run_embedded(url: str, parent_hwnd: int) -> int:
    _adopt_parent_dpi_awareness(parent_hwnd)
    try:
        import webview
    except Exception as e:  # ImportError, or pythonnet/clr-loader blowups
        print(f"pywebview unavailable: {e}", file=sys.stderr)
        return 3
    try:
        window = webview.create_window(
            "AV Bible stage", url, frameless=True,
            width=320, height=240, background_color="#101018")
        threading.Thread(target=_embed_and_track,
                         args=(window, parent_hwnd), daemon=True).start()
        threading.Thread(target=_orphan_watchdog,
                         args=(url, window.destroy), daemon=True).start()
        webview.start()
    except Exception as e:
        print(f"pywebview failed to start: {e}", file=sys.stderr)
        return 3
    return 0


def main() -> int:
    args = sys.argv[1:]
    if len(args) >= 4 and args[0] == "--url" and args[2] == "--parent":
        return run_embedded(args[1], int(args[3]))
    print("usage: svg_stage.py --url http://127.0.0.1:PORT/stage.html "
          "--parent HWND", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
