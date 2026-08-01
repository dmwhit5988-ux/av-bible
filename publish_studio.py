"""Publish — one-click author→deploy pipeline for the web app.

Runs the whole publish chain that used to be four manual steps:

    1. build_stills        refresh reduced-motion .still.svg twins
    2. build_manifest.py   rebuild visuals/manifest.json (schema v2)
    3. prepare-deploy.ps1  mirror web/ + bibles/ + visuals/ into deploy_bundle/
    4. git add/commit/push CONTENT paths only (web/, bibles/, visuals/,
                           deploy_bundle/) — pushing is the deploy: the
                           GitHub-side integration uploads to Cloudflare
                           (local wrangler can't run on ARM64)

Code changes (*.py, docs, …) are deliberately left out of the publish
commit — commit those yourself, so a content publish never sweeps up
half-finished code.

Between steps 3 and 4 you get a confirm dialog with the change summary and
the file-count budget: files, not bytes, are the Cloudflare ceiling
(~20k, STUDIO_PLAN.md Feature C caveat 2). A persistent budget meter at the
top of the window tracks the same number while you author.

    python publish_studio.py
"""

import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import audio_studio
import build_stills

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
FILE_LIMIT = audio_studio.CLOUDFLARE_PAGES_FILE_LIMIT

# Only these paths go into a publish commit.
CONTENT_PATHS = ["web", "bibles", "visuals", "deploy_bundle"]


def _run(cmd, timeout=600):
    """Run a command from the repo root; returns CompletedProcess."""
    return subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True,
                          text=True, timeout=timeout)


def git_content_changes() -> list[tuple[str, str]]:
    """[(status, path)] for uncommitted changes under the content paths.
    status is porcelain's two-letter code, e.g. ' M', '??', ' D'."""
    proc = _run(["git", "status", "--porcelain", "--"] + CONTENT_PATHS,
                timeout=120)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git status failed")
    changes = []
    for line in proc.stdout.splitlines():
        if len(line) > 3:
            changes.append((line[:2], line[3:].strip()))
    return changes


def summarize_changes(changes) -> str:
    """Human summary of a porcelain change list, grouped by content area."""
    if not changes:
        return "no content changes"
    areas = {}
    for _, path in changes:
        area = path.split("/", 1)[0]
        areas[area] = areas.get(area, 0) + 1
    parts = [f"{n} file(s) under {area}/"
             for area, n in sorted(areas.items())]
    return ", ".join(parts)


def commit_message(changes) -> str:
    visuals = sum(1 for _, p in changes if p.startswith("visuals/"))
    audio = sum(1 for _, p in changes
                if p.startswith("web/audio/") and p.endswith(".mp3"))
    parts = []
    if visuals:
        parts.append(f"{visuals} visual file(s)")
    if audio:
        parts.append(f"{audio} audio file(s)")
    detail = ", ".join(parts) if parts else "content update"
    return f"Publish: {detail}"


class App:
    def __init__(self, root):
        self.root = root
        self.events: queue.Queue = queue.Queue()
        self.busy = False

        root.title("Publish")
        root.geometry("720x520")
        root.minsize(620, 420)

        self._build_ui()
        self._refresh_meter()
        self._poll_events()

    # ----- UI construction -----------------------------------------------
    def _build_ui(self):
        meter = ttk.LabelFrame(self.root, text="Deploy budget (file count)",
                               padding=(10, 6))
        meter.pack(fill="x", padx=10, pady=(10, 4))
        self.meter_bar = ttk.Progressbar(meter, orient="horizontal",
                                         mode="determinate",
                                         maximum=FILE_LIMIT)
        self.meter_bar.pack(fill="x")
        self.meter_var = tk.StringVar(value="counting…")
        self.meter_label = ttk.Label(meter, textvariable=self.meter_var)
        self.meter_label.pack(anchor="w", pady=(4, 0))

        btns = ttk.Frame(self.root, padding=(10, 6))
        btns.pack(fill="x")
        self.publish_btn = ttk.Button(btns, text="🚀 Publish…",
                                      command=self.start_publish)
        self.publish_btn.pack(side="left")
        ttk.Button(btns, text="Refresh", command=self._refresh_meter).pack(
            side="left", padx=(6, 0))
        ttk.Label(btns, foreground="#888888",
                  text="Publishes content only (web/ bibles/ visuals/ "
                       "deploy_bundle/) — code commits stay yours.").pack(
            side="left", padx=(12, 0))

        logframe = ttk.LabelFrame(self.root, text="Log", padding=(6, 4))
        logframe.pack(fill="both", expand=True, padx=10, pady=(4, 4))
        self.log = tk.Text(logframe, height=12, state="disabled",
                           wrap="word", font=("Consolas", 9))
        scroll = ttk.Scrollbar(logframe, command=self.log.yview)
        self.log.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.log.pack(fill="both", expand=True)

        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(self.root, textvariable=self.status_var, padding=(10, 4),
                  wraplength=680, justify="left").pack(anchor="w")

    def _log(self, line):
        self.log.configure(state="normal")
        self.log.insert("end", line + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _refresh_meter(self):
        def worker():
            try:
                n = audio_studio.count_deploy_files()
            except OSError:
                n = -1
            self.events.put(("meter", n))
        threading.Thread(target=worker, daemon=True).start()

    def _set_meter(self, n):
        if n < 0:
            self.meter_var.set("count unavailable")
            return
        pct = 100 * n / FILE_LIMIT
        self.meter_bar.configure(value=min(n, FILE_LIMIT))
        warn = "  ⚠ near the ceiling!" if pct >= 90 else ""
        self.meter_var.set(
            f"{n:,} / {FILE_LIMIT:,} files ({pct:.0f}% of the Cloudflare "
            f"limit){warn}")

    # ----- publish pipeline ------------------------------------------------
    def start_publish(self):
        if self.busy:
            return
        self.busy = True
        self.publish_btn.configure(state="disabled")
        self.status_var.set("Publishing…")
        threading.Thread(target=self._prepare_worker, daemon=True).start()

    def _prepare_worker(self):
        """Steps 1–3 + change scan, then hand off to the confirm dialog."""
        put = self.events.put
        try:
            put(("log", "— Step 1/4: reduced-motion stills —"))
            stats = build_stills.build_stills(
                on_progress=lambda line: put(("log", "  " + line)))
            put(("log", f"  {stats.summary()}"))
            for rel, msg in stats.warnings[:10]:
                put(("log", f"  [warn] {rel}: {msg}"))
            if len(stats.warnings) > 10:
                put(("log", f"  … and {len(stats.warnings) - 10} more "
                            f"warning(s)"))

            put(("log", "— Step 2/4: visuals manifest —"))
            proc = _run([sys.executable,
                         os.path.join(REPO_ROOT, "build_manifest.py")],
                        timeout=120)
            if proc.returncode != 0:
                raise RuntimeError("build_manifest.py failed: "
                                   + proc.stderr.strip()[:300])
            put(("log", "  " + (proc.stdout.strip().splitlines() or ["ok"])[0]))

            put(("log", "— Step 3/4: deploy bundle —"))
            proc = _run(["powershell", "-NoProfile", "-ExecutionPolicy",
                         "Bypass", "-File",
                         os.path.join(REPO_ROOT, "prepare-deploy.ps1")])
            if proc.returncode != 0:
                raise RuntimeError("prepare-deploy.ps1 failed: "
                                   + (proc.stderr or "").strip()[:300])
            for line in (proc.stdout or "").strip().splitlines()[-2:]:
                put(("log", "  " + line))

            put(("log", "— Step 4/4: git —"))
            put(("log", "  scanning content changes "
                        "(large bundle rebuilds take a moment)…"))
            changes = git_content_changes()
            bundle_files = sum(
                len(files) for _, _, files
                in os.walk(os.path.join(REPO_ROOT, "deploy_bundle")))
            put(("confirm", changes, bundle_files))
        except Exception as e:
            put(("fail", str(e)))

    def _do_confirm(self, changes, bundle_files):
        if not changes:
            self._finish("Everything is already published — no content "
                        "changes to commit.")
            return
        over = bundle_files > FILE_LIMIT
        msg = (f"Ready to publish:\n\n"
               f"  {summarize_changes(changes)}\n"
               f"  ({len(changes)} file(s) total in the commit)\n\n"
               f"Deploy bundle: {bundle_files:,} files "
               f"(limit ~{FILE_LIMIT:,})\n\n")
        if over:
            msg += ("This EXCEEDS the Cloudflare file-count ceiling — the "
                    "deploy will likely fail.\n\n")
        msg += ("Commit and push to GitHub now? The push is the deploy — "
                "GitHub uploads the bundle to Cloudflare.")
        if not messagebox.askyesno("Publish", msg, parent=self.root,
                                   icon="warning" if over else "question"):
            self._finish("Publish cancelled — nothing was committed.")
            return
        self.status_var.set("Committing and pushing…")
        threading.Thread(target=self._push_worker, args=(changes,),
                         daemon=True).start()

    def _push_worker(self, changes):
        put = self.events.put
        try:
            proc = _run(["git", "add", "-A", "--"] + CONTENT_PATHS,
                        timeout=300)
            if proc.returncode != 0:
                raise RuntimeError("git add failed: " + proc.stderr.strip())
            msg = commit_message(changes)
            proc = _run(["git", "commit", "-m", msg], timeout=300)
            if proc.returncode != 0:
                raise RuntimeError("git commit failed: "
                                   + (proc.stderr or proc.stdout).strip()[:300])
            put(("log", f"  committed: {msg}"))
            put(("log", "  pushing to GitHub…"))
            proc = _run(["git", "push"], timeout=600)
            if proc.returncode != 0:
                raise RuntimeError(
                    "git push failed (the commit is safe locally — fix the "
                    "connection/credentials and push manually): "
                    + (proc.stderr or "").strip()[:300])
            put(("log", "  pushed — GitHub will deploy to Cloudflare."))
            put(("done", f"Published: {msg}"))
        except Exception as e:
            put(("fail", str(e)))

    def _finish(self, status):
        self.busy = False
        self.publish_btn.configure(state="normal")
        self.status_var.set(status)
        self._log(status)
        self._refresh_meter()

    # ----- event pump (worker thread -> UI thread) --------------------------
    def _poll_events(self):
        try:
            while True:
                event = self.events.get_nowait()
                self._handle_event(event)
        except queue.Empty:
            pass
        if self.root.winfo_exists():
            self.root.after(80, self._poll_events)

    def _handle_event(self, event):
        kind = event[0]
        if kind == "log":
            self._log(event[1])
        elif kind == "meter":
            self._set_meter(event[1])
        elif kind == "confirm":
            self._do_confirm(*event[1:])
        elif kind == "done":
            self._finish(event[1])
        elif kind == "fail":
            self._log("FAILED: " + event[1])
            self._finish("Publish failed — see the log.")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
