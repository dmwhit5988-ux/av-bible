"""Publish — one-click author→deploy pipeline for the web app.

Runs the whole publish chain that used to be three manual steps:

    1. build_manifest.py   rebuild visuals/manifest.json (schema v2)
    2. prepare-deploy.ps1  mirror web/ + bibles/ + visuals/ into deploy_bundle/
    3. git add/commit/push CONTENT paths only (web/audio, bibles, visuals
                           and their deploy_bundle/ copies) — pushing is the
                           deploy: the GitHub-side integration uploads to
                           Cloudflare (local wrangler can't run on ARM64)

Code changes (*.py, docs, the web app's own js/css/html) are deliberately
left out of the publish commit — commit those yourself, so a content
publish never sweeps up half-finished code. Both the add and the commit
are limited to CONTENT_PATHS, so anything you had staged elsewhere stays
staged and uncommitted. When the web app's own files have uncommitted
changes, Publish says so: they (and the copies step 2 makes of them in
deploy_bundle/) stay unpublished until you commit them by hand.

Between steps 2 and 3 you get a confirm dialog with the change summary and
the file-count budget: files, not bytes, are the ceiling of Cloudflare's
Workers static assets (DEPLOY_FILE_LIMIT; docs/architecture.md, "File
budget"). A persistent budget meter at the top of the window tracks the same
number while you author; count_deploy_files() is also the count behind the
Studio's meter and the Audio Renderer's projection.

"Dry run (no commit / push)" runs steps 1 and 2, logs the change summary,
the commit message and the budget, and stops before git: nothing is staged,
committed or pushed. Steps 1 and 2 still rewrite visuals/manifest.json and
deploy_bundle/, as a real publish would; that is what the summary describes.

    python publish_studio.py
"""

import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import config

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# Cloudflare's Workers static assets take at most this many files in one
# deployed version (20,000 on the Free plan). It is not a Pages limit: the
# site deploys as a Worker serving deploy_bundle/ (wrangler.toml [assets]).
# The Studio's meter (app.py) and the Audio Renderer read it from here.
DEPLOY_FILE_LIMIT = 20000

# Only these paths go into a publish commit. Content folders only, never the
# web app shell: prepare-deploy.ps1 copies web/* (js, css, index.html) into
# the deploy_bundle root, so listing plain "web" or "deploy_bundle" would ship
# half-finished web code under "Publish: …".
CONTENT_PATHS = ["web/audio", "bibles", "visuals",
                 "deploy_bundle/audio", "deploy_bundle/bibles",
                 "deploy_bundle/visuals"]

# The web app's own files: everything under web/ but the narration (js, css,
# index.html, icons, manifest.webmanifest). Never in a publish commit;
# web_app_changes() finds the uncommitted ones so Publish can warn.
WEB_APP_PATHS = ["web", ":(exclude)web/audio"]

# The visual files a change summary counts: the set build_manifest.IMAGE_EXTS
# indexes. The rest of visuals/ (manifest.json, the reference pages) is
# committed too but counted as "other".
_PICTURE_EXTS = (".svg", ".webp", ".gif", ".png", ".jpg", ".jpeg")

# The content a change summary counts, as (tally area, singular, plural).
_COUNTED = (("visuals", "visual", "visuals"),
            ("mp3s", "MP3", "MP3s"),
            ("chapters", "Bible chapter", "Bible chapters"))


def count_deploy_files() -> int:
    """Count the files a deploy would ship, mirroring the bundle
    prepare-deploy.ps1 builds: all of web/, the *.json in each bibles/
    subfolder (one level, not recursive; only WEB exists), and visuals/
    minus *.xml. Counted from those sources rather than deploy_bundle/,
    which is only rebuilt by a publish."""
    count = 0
    for _, _, files in os.walk(config.WEB_DIR):
        count += len(files)
    if os.path.isdir(config.BIBLES_DIR):
        for sub in os.listdir(config.BIBLES_DIR):
            sub_dir = os.path.join(config.BIBLES_DIR, sub)
            if os.path.isdir(sub_dir):
                count += sum(1 for f in os.listdir(sub_dir)
                             if f.lower().endswith(".json"))
    for _, _, files in os.walk(config.VISUALS_DIR):
        count += sum(1 for f in files if not f.lower().endswith(".xml"))
    return count


def add_argv() -> list[str]:
    """The `git add` the publish runs: stage content changes only."""
    return ["git", "add", "-A", "--"] + CONTENT_PATHS


def commit_argv(msg: str) -> list[str]:
    """The `git commit` the publish runs. The pathspec matters: without it
    git commits the whole index, which is how a publish once deleted a
    generator someone had staged for removal."""
    return ["git", "commit", "-m", msg, "--"] + CONTENT_PATHS


def _run(cmd, timeout=600, env=None):
    """Run a command from the repo root; returns CompletedProcess. Output is
    read as UTF-8 (git's encoding for paths), never failing on a byte."""
    return subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          timeout=timeout, env=env)


def git_content_changes() -> list[tuple[str, str]]:
    """[(change, path)] for every file under the content paths that the
    publish commit would record, sorted by path. change is "deleted" when
    the file is gone from the working tree, else "changed" (new or
    modified). One entry per file: a new folder is listed file by file, not
    as one "folder/" line, and a rename is a deletion plus an addition.
    Paths are repo-relative with forward slashes, never quoted (-z)."""
    proc = _run(["git", "status", "--porcelain", "-z",
                 "--untracked-files=all", "--no-renames", "--"]
                + CONTENT_PATHS, timeout=120)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git status failed")
    changes = {}
    for record in proc.stdout.split("\0"):
        if len(record) < 4:
            continue
        status, path = record[:2], record[3:]
        if status != "??" and not os.path.lexists(
                os.path.join(REPO_ROOT, path)):
            if status[0] == "A":
                continue    # staged as new, since deleted: nothing to commit
            changes[path] = "deleted"
        else:
            changes[path] = "changed"
    return [(change, path) for path, change in sorted(changes.items())]


def web_app_changes() -> list[str]:
    """The web app's own files (WEB_APP_PATHS) that differ from HEAD, new
    ones included, as sorted repo-relative paths. Publish never commits
    them, so it warns while there are any."""
    found = set()
    for argv in (["git", "diff", "--name-only", "-z", "HEAD"],
                 ["git", "ls-files", "-z", "--others", "--exclude-standard"]):
        proc = _run(argv + ["--"] + WEB_APP_PATHS, timeout=120)
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or f"git {argv[1]} failed")
        found.update(p for p in proc.stdout.split("\0") if p)
    return sorted(found)


def _area(path: str) -> str:
    """The tally a changed content path counts towards: "visuals" (a
    picture under visuals/), "mp3s" (narration under web/audio/),
    "chapters" (a Bible chapter, bibles/<code>/<chapter>.json), "bundle"
    (anything under deploy_bundle/, the served copies of those) or "other"
    (the two manifests and the like)."""
    low = path.lower()
    if path.startswith("deploy_bundle/"):
        return "bundle"
    if path.startswith("visuals/") and low.endswith(_PICTURE_EXTS):
        return "visuals"
    if path.startswith("web/audio/") and low.endswith(".mp3"):
        return "mp3s"
    if (path.startswith("bibles/") and path.count("/") == 2
            and low.endswith(".json")):
        return "chapters"
    return "other"


def tally_changes(changes) -> dict[str, dict[str, int]]:
    """{area: {"changed": n, "deleted": n}} for a git_content_changes()
    list, with every area _area() names present."""
    tally = {area: {"changed": 0, "deleted": 0}
             for area in ("visuals", "mp3s", "chapters", "bundle", "other")}
    for change, path in changes:
        tally[_area(path)][change] += 1
    return tally


def _count(n: int, singular: str, plural: str) -> str:
    return f"{n:,} {singular if n == 1 else plural}"


def _counted(tally, change: str) -> str:
    """The visuals, MP3s and Bible chapters with this change, as
    "12 visuals, 30 MP3s"; "" when there are none."""
    return ", ".join(_count(tally[area][change], one, many)
                     for area, one, many in _COUNTED if tally[area][change])


def commit_message(changes) -> str:
    """The publish commit's message: the visuals, MP3s and Bible chapters
    it adds or changes, then the ones it deletes, e.g. "Publish: 12
    visuals, 30 MP3s; deleted 2 visuals". The manifests and the
    deploy_bundle/ copies that go along aren't counted; a commit of only
    those is a "content update"."""
    tally = tally_changes(changes)
    changed, deleted = _counted(tally, "changed"), _counted(tally, "deleted")
    detail = "; ".join(filter(None, [changed,
                                     deleted and f"deleted {deleted}"]))
    return f"Publish: {detail or 'content update'}"


def summarize_changes(changes) -> str:
    """Human summary of a change list, one line per kind of change."""
    if not changes:
        return "no content changes"
    tally = tally_changes(changes)
    lines = []
    changed, deleted = _counted(tally, "changed"), _counted(tally, "deleted")
    if changed:
        lines.append(f"new or changed: {changed}")
    if deleted:
        lines.append(f"deleted: {deleted}")
    other = sum(tally["other"].values())
    if other:
        lines.append(_count(other, "other content file", "other content files")
                     + " (the manifests and the like)")
    bundle = sum(tally["bundle"].values())
    if bundle:
        lines.append(_count(bundle, "file", "files")
                     + " under deploy_bundle/ (the copies Cloudflare serves)")
    return "\n".join(lines)


def web_app_warning(paths) -> str:
    """What Publish says when the web app's own files have uncommitted
    changes (paths from web_app_changes()); "" when they have none."""
    if not paths:
        return ""
    shown = ", ".join(paths[:3])
    if len(paths) > 3:
        shown += f" and {len(paths) - 3} more"
    return (f"The web app's own files have uncommitted changes ({shown}). "
            f"Publish doesn't commit them (its commit takes content paths "
            f"only), so they stay unpublished until you commit them, and "
            f"their deploy_bundle/ copies, by hand.")


class App:
    def __init__(self, root):
        self.root = root
        self.events: queue.Queue = queue.Queue()
        self.busy = False       # a publish is in flight (any step)
        self._confirming = False  # ...and is asking whether to commit
        self._pushing = False   # ...or has reached git add/commit/push

        root.title("Publish")
        root.geometry("720x520")
        root.minsize(620, 420)
        root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._refresh_meter()
        self._poll_events()

    def set_passage(self, book, chapter, verse=None, *, ask=False) -> bool:
        """Publish works on the whole site, not a passage: nothing to do."""
        return True

    def can_close(self) -> bool:
        """True when no publish is running, so closing is instant then.
        While one runs, refuses (False) and says to wait: closing would
        orphan it partway (during git, perhaps committed but not pushed),
        and a second Publish could then start alongside it. Every step has
        a timeout, so the wait always ends."""
        if not self.busy:
            return True
        if self._pushing:
            msg = ("Publish is committing and pushing to GitHub. Wait for it "
                   "to finish, then close.")
        elif self._confirming:
            msg = ("Publish is asking whether to commit and push. Answer it, "
                   "then close.")
        else:
            msg = ("Publish is still preparing (manifest and deploy bundle). "
                   "Wait for it to finish, then close.")
        messagebox.showinfo("Publish", msg, parent=self.root)
        return False

    def _on_close(self):
        if self.can_close():
            self.root.destroy()

    # ----- UI construction -----------------------------------------------
    def _build_ui(self):
        meter = ttk.LabelFrame(self.root, text="Deploy budget (file count)",
                               padding=(10, 6))
        meter.pack(fill="x", padx=10, pady=(10, 4))
        self.meter_bar = ttk.Progressbar(meter, orient="horizontal",
                                         mode="determinate",
                                         maximum=DEPLOY_FILE_LIMIT)
        self.meter_bar.pack(fill="x")
        self.meter_var = tk.StringVar(value="counting…")
        self.meter_label = ttk.Label(meter, textvariable=self.meter_var)
        self.meter_label.pack(anchor="w", pady=(4, 0))

        btns = ttk.Frame(self.root, padding=(10, 6, 10, 0))
        btns.pack(fill="x")
        self.publish_btn = ttk.Button(btns, text="🚀 Publish…",
                                      command=self.start_publish)
        self.publish_btn.pack(side="left")
        ttk.Button(btns, text="Refresh", command=self._refresh_meter).pack(
            side="left", padx=(6, 0))
        self.dry_run_var = tk.BooleanVar(value=False)
        self.dry_run_check = ttk.Checkbutton(
            btns, text="Dry run (no commit / push)",
            variable=self.dry_run_var)
        self.dry_run_check.pack(side="left", padx=(12, 0))
        ttk.Label(self.root, foreground="#888888", padding=(10, 2, 10, 4),
                  text="Publishes content only (web/audio, bibles, visuals "
                       "and their deploy_bundle/ copies) — code commits stay "
                       "yours.").pack(anchor="w")

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
                n = count_deploy_files()
            except OSError:
                n = -1
            self.events.put(("meter", n))
        threading.Thread(target=worker, daemon=True).start()

    def _set_meter(self, n):
        if n < 0:
            self.meter_var.set("count unavailable")
            return
        pct = 100 * n / DEPLOY_FILE_LIMIT
        self.meter_bar.configure(value=min(n, DEPLOY_FILE_LIMIT))
        warn = "  ⚠ near the ceiling!" if pct >= 90 else ""
        self.meter_var.set(
            f"{n:,} / {DEPLOY_FILE_LIMIT:,} files ({pct:.0f}% of Cloudflare's "
            f"limit){warn}")

    # ----- publish pipeline ------------------------------------------------
    def start_publish(self):
        if self.busy:
            return
        self.busy = True
        dry_run = self.dry_run_var.get()
        self.publish_btn.configure(state="disabled")
        self.dry_run_check.configure(state="disabled")
        self.status_var.set("Dry run…" if dry_run else "Publishing…")
        threading.Thread(target=self._prepare_worker, args=(dry_run,),
                         daemon=True).start()

    def _prepare_worker(self, dry_run):
        """Steps 1–2 + change scan, then hand off to the confirm dialog (or,
        for a dry run, to the report)."""
        put = self.events.put
        try:
            put(("log", "— Step 1/3: visuals manifest —"))
            proc = _run([sys.executable,
                         os.path.join(REPO_ROOT, "build_manifest.py")],
                        timeout=120,
                        env=dict(os.environ, PYTHONIOENCODING="utf-8"))
            if proc.returncode != 0:
                raise RuntimeError("build_manifest.py failed: "
                                   + proc.stderr.strip()[:300])
            lines = [ln for ln in proc.stdout.splitlines() if ln.startswith("[")]
            for line in lines or ["ok"]:
                put(("log", "  " + line))

            put(("log", "— Step 2/3: deploy bundle —"))
            proc = _run(["powershell", "-NoProfile", "-ExecutionPolicy",
                         "Bypass", "-File",
                         os.path.join(REPO_ROOT, "prepare-deploy.ps1")])
            if proc.returncode != 0:
                raise RuntimeError("prepare-deploy.ps1 failed: "
                                   + (proc.stderr or "").strip()[:300])
            for line in (proc.stdout or "").strip().splitlines()[-2:]:
                put(("log", "  " + line))

            put(("log", "— Step 3/3: git (dry run: status only) —" if dry_run
                 else "— Step 3/3: git —"))
            put(("log", "  scanning content changes "
                        "(large bundle rebuilds take a moment)…"))
            changes = git_content_changes()
            try:
                web_app = web_app_changes()
            except Exception as e:  # only a warning: never stop the publish
                put(("log", f"  could not check the web app's own files: "
                            f"{type(e).__name__}: {e}"))
                web_app = []
            bundle_files = sum(
                len(files) for _, _, files
                in os.walk(os.path.join(REPO_ROOT, "deploy_bundle")))
            put(("confirm", changes, bundle_files, web_app, dry_run))
        except Exception as e:
            put(("fail", str(e)))

    def _do_confirm(self, changes, bundle_files, web_app, dry_run):
        over = bundle_files > DEPLOY_FILE_LIMIT
        budget = (f"Deploy bundle: {bundle_files:,} files "
                  f"(limit ~{DEPLOY_FILE_LIMIT:,})")
        over_note = ("This EXCEEDS Cloudflare's file-count ceiling — the "
                     "deploy will likely fail.") if over else ""
        warning = web_app_warning(web_app)
        if dry_run:
            self._dry_run_report(changes, budget, over_note, warning)
            return
        if not changes:
            self._finish(f"No content changes to commit.\n{warning}"
                         if warning else
                         "Everything is already published — no content "
                         "changes to commit.")
            return
        summary = "\n".join("  " + line
                            for line in summarize_changes(changes).splitlines())
        msg = (f"Ready to publish {len(changes):,} file(s):\n\n"
               f"{summary}\n\n"
               f"Commit message: {commit_message(changes)}\n\n"
               f"{budget}\n\n")
        for note in (over_note, warning):
            if note:
                msg += f"{note}\n\n"
        msg += ("Commit and push to GitHub now? The push is the deploy — "
                "GitHub uploads the bundle to Cloudflare.")
        self._confirming = True
        try:
            proceed = messagebox.askyesno(
                "Publish", msg, parent=self.root,
                icon="warning" if over or warning else "question")
        finally:
            self._confirming = False
        if not proceed:
            self._finish("Publish cancelled — nothing was committed.")
            return
        threading.Thread(target=self._push_worker, args=(changes,),
                         daemon=True).start()
        self._pushing = True    # set once the thread runs (see "confirm")
        self.status_var.set("Committing and pushing…")

    def _dry_run_report(self, changes, budget, over_note, warning):
        """Log what a publish would commit, then stop: no git add, commit
        or push."""
        if changes:
            self._log(f"  would commit {len(changes):,} file(s):")
            for line in summarize_changes(changes).splitlines():
                self._log("    " + line)
            self._log(f"  commit message: {commit_message(changes)}")
        else:
            self._log("  no content changes to commit")
        self._log("  " + budget)
        for note in (over_note, warning):
            if note:
                self._log("  ⚠ " + note)
        self._finish("Dry run finished — nothing was staged, committed or "
                     "pushed.")

    def _push_worker(self, changes):
        put = self.events.put
        try:
            proc = _run(add_argv(), timeout=300)
            if proc.returncode != 0:
                raise RuntimeError("git add failed: " + proc.stderr.strip())
            msg = commit_message(changes)
            proc = _run(commit_argv(msg), timeout=300)
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
        self._confirming = False
        self._pushing = False
        self.publish_btn.configure(state="normal")
        self.dry_run_check.configure(state="normal")
        self.status_var.set(status)
        self._log(status)
        self._refresh_meter()

    # ----- event pump (worker thread -> UI thread) --------------------------
    def _poll_events(self):
        try:
            while True:
                try:
                    event = self.events.get_nowait()
                except queue.Empty:
                    break
                self._handle_event(event)
        finally:
            # Rescheduled even when a handler raised: can_close refuses while
            # busy, so the "done"/"fail" that clears it must always arrive.
            try:
                alive = self.root.winfo_exists()
            except tk.TclError:
                alive = False
            if alive:
                self.root.after(80, self._poll_events)

    def _handle_event(self, event):
        kind = event[0]
        if kind == "log":
            self._log(event[1])
        elif kind == "meter":
            self._set_meter(event[1])
        elif kind == "confirm":
            try:
                self._do_confirm(*event[1:])
            except Exception as e:
                if not self._pushing:   # no push thread started: not busy
                    self._log(f"FAILED: {type(e).__name__}: {e}")
                    self._finish("Publish failed — see the log.")
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
