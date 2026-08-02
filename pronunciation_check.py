"""Pronunciation Verifier -- check what the voice *actually says* against the list.

Tuning pronunciations in ``pronunciation_tool.py`` is done entirely by ear, and
by ear is also the only way it gets re-checked. That works fine for the name in
front of you and not at all for the 1500+ behind it: a respelling that used to
sound right can drift when the voice model changes, and a name marked
``override: false`` may have been wrong all along.

This tool closes that loop mechanically. For every name it:

  1. builds the exact text the pipeline would speak -- the lowercased ``say``
     when ``override`` is true, otherwise the name itself,
  2. synthesizes it with the real edge-tts voice (same cache as playback) --
     alone for short names, inside a carrier sentence for longer ones,
  3. transcribes the audio back to IPA acoustically (``ipa_asr``), and
  4. scores that against the ``ipa`` stored in pronunciations.json.

Low scores are where to look. High scores are not proof of correctness -- see
the honesty notes in ``ipa_asr`` -- so this ranks suspicion, it does not issue
verdicts. Even a perfectly-said name routinely lands around 0.8, and short names
carry more noise than long ones, so read the ordering rather than the number.
Nothing is changed automatically; "Use heard IPA" is a manual per-row action for
filling in or correcting a reference value.

Results are cached in ``cache/ipa_checks.json`` keyed by the spoken text and
voice, so a long sweep survives a restart and only genuinely changed entries
are re-checked.

    python pronunciation_check.py
"""

import copy
import json
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import config
import ipa_asr
import pronunciation
import tts_engine
from audio_player import AudioPlayer

RATE = 0
CACHE_PATH = os.path.join(config.CACHE_DIR, "ipa_checks.json")

# Score bands. Deliberately loose: the transcriber's own error rate means a
# perfect respelling routinely lands around 0.8, so only the bottom band is
# worth treating as a real signal.
OK_AT = 0.80
WARN_AT = 0.55

# Every name is checked inside a carrier phrase rather than alone: spoken in
# isolation the voice clips them ("Mahalalel" came back as "mahalla"), which
# looks like a pronunciation fault but is an artefact of the recognizer, which
# was trained on connected speech. ipa_asr.strip_carrier() then cuts the
# carrier words back off using their own fixed phones as anchors.
CARRIER = ipa_asr.CARRIER

FILTERS = (
    "All names",
    "Custom (override) only",
    "Not measured this run",
    "Disagreements only",
    "Missing IPA",
    # These read the status saved in pronunciations.json rather than this run's
    # cache, so a sweep can skip whole books that are already settled.
    "Never verified",
    "Marked still wrong",
    "Marked fine as spelled",
)


def spoken_for(name: str, info: dict) -> str:
    """The exact string the TTS pipeline feeds the voice for this name."""
    if info.get("override") and info.get("say"):
        return info["say"].lower()
    return name


class App:
    def __init__(self, root):
        self.root = root
        self.player = AudioPlayer()
        self.names = copy.deepcopy(pronunciation.load(force=True))
        self.results = self._load_cache()   # name -> {spoken, voice, heard, score}
        self.dirty = False
        self.running = False
        self._stop = False
        self.sort_col = None
        self.sort_desc = False

        root.title("Pronunciation Verifier")
        root.geometry("1180x720")
        root.minsize(900, 480)
        root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_top()
        self._build_tree()
        self._build_bottom()
        self.refresh()

        ok, msg = ipa_asr.available()
        if not ok:
            self.status_var.set("Transcriber unavailable — " + msg.replace("\n\n", "  "))

    # ----- layout -------------------------------------------------------
    def _build_top(self):
        bar = ttk.Frame(self.root, padding=(10, 8))
        bar.pack(fill="x")

        ttk.Label(bar, text="Voice:").pack(side="left")
        self.voice_var = tk.StringVar(value=config.load().get("voice", tts_engine.EDGE_VOICES[0]))
        vcb = ttk.Combobox(bar, textvariable=self.voice_var, width=22, state="readonly",
                           values=tts_engine.EDGE_VOICES)
        vcb.pack(side="left", padx=(4, 12))
        vcb.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        ttk.Label(bar, text="Show:").pack(side="left")
        self.filter_var = tk.StringVar(value=FILTERS[1])
        fcb = ttk.Combobox(bar, textvariable=self.filter_var, width=22, state="readonly",
                           values=FILTERS)
        fcb.pack(side="left", padx=(4, 12))
        fcb.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        self.check_btn = ttk.Button(bar, text="Check shown", command=self.check_shown)
        self.check_btn.pack(side="left")
        self.check_sel_btn = ttk.Button(bar, text="Check selected", command=self.check_selected)
        self.check_sel_btn.pack(side="left", padx=4)
        self.stop_btn = ttk.Button(bar, text="Stop", command=self.stop, state="disabled")
        self.stop_btn.pack(side="left")

        self.progress = ttk.Progressbar(bar, mode="determinate", length=180)
        self.progress.pack(side="right")

    def _build_tree(self):
        outer = ttk.Frame(self.root)
        outer.pack(fill="both", expand=True, padx=10)

        cols = ("name", "spoken", "expected", "heard", "score")
        headings = {
            "name": ("Name", 150),
            "spoken": ("Spoken as", 190),
            "expected": ("Expected IPA", 210),
            "heard": ("Heard IPA", 300),
            "score": ("Score", 70),
        }
        self.tree = ttk.Treeview(outer, columns=cols, show="headings", selectmode="extended")
        for c in cols:
            label, width = headings[c]
            self.tree.heading(c, text=label, command=lambda cc=c: self._sort_by(cc))
            self.tree.column(c, width=width, anchor="w",
                             stretch=(c in ("heard", "expected")))
        vsb = ttk.Scrollbar(outer, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.tag_configure("ok", background="#e8f6ea")
        self.tree.tag_configure("warn", background="#fdf3e0")
        self.tree.tag_configure("bad", background="#fce9e9")
        self.tree.tag_configure("none", background="")
        self.tree.bind("<Double-1>", lambda e: self.play_selected())

    def _build_bottom(self):
        bar = ttk.Frame(self.root, padding=(10, 8))
        bar.pack(fill="x")
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(bar, textvariable=self.status_var).pack(side="left")

        self.save_btn = ttk.Button(bar, text="Save  (JSON + .md)", command=self.save)
        self.save_btn.pack(side="right")
        ttk.Button(bar, text="Use heard IPA",
                   command=self.use_heard).pack(side="right", padx=6)
        ttk.Button(bar, text="▶ Play", command=self.play_selected).pack(side="right")

    # ----- result cache -------------------------------------------------
    def _load_cache(self) -> dict:
        try:
            with open(CACHE_PATH, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return {}

    def _save_cache(self):
        os.makedirs(config.CACHE_DIR, exist_ok=True)
        try:
            with open(CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.results, f, indent=1, ensure_ascii=False)
        except OSError:
            pass  # a lost cache only costs time on the next sweep

    def _result_for(self, name):
        """Cached result for ``name``, or None if stale (voice/spelling changed)."""
        r = self.results.get(name)
        if not r:
            return None
        info = self.names.get(name, {})
        # The mode tag also versions the cache: results recorded by an older
        # measuring method are discarded rather than silently compared.
        if (r.get("spoken") != spoken_for(name, info)
                or r.get("voice") != self.voice_var.get()
                or r.get("mode") != "carrier-avg"):
            return None
        return r

    # ----- listing ------------------------------------------------------
    def _visible_names(self):
        mode = self.filter_var.get()
        out = []
        for name, info in self.names.items():
            r = self._result_for(name)
            if mode == "Custom (override) only" and not info.get("override"):
                continue
            if mode == "Not measured this run" and r is not None:
                continue
            if mode in ("Never verified", "Marked still wrong", "Marked fine as spelled"):
                want = {"Never verified": pronunciation.STATUS_UNCHECKED,
                        "Marked still wrong": pronunciation.STATUS_UNFIXED,
                        "Marked fine as spelled": pronunciation.STATUS_OK}[mode]
                if pronunciation.status_of(info) != want:
                    continue
            # An unmeasured name (score None) is not a disagreement.
            if mode == "Disagreements only" and (
                    r is None or r["score"] is None or r["score"] >= WARN_AT):
                continue
            if mode == "Missing IPA" and info.get("ipa"):
                continue
            out.append(name)
        return out

    def _band(self, score):
        if score is None:
            return "none"
        if score >= OK_AT:
            return "ok"
        return "warn" if score >= WARN_AT else "bad"

    def refresh(self, keep_status=False):
        selected = set(self.tree.selection()) if self.tree.get_children() else set()
        self.tree.delete(*self.tree.get_children())
        names = self._visible_names()

        rows = []
        for name in names:
            info = self.names[name]
            r = self._result_for(name)
            score = r["score"] if r else None
            rows.append((name, spoken_for(name, info), info.get("ipa", ""),
                         (r["heard"] or "(nothing heard)") if r else "", score))

        if self.sort_col:
            idx = ("name", "spoken", "expected", "heard", "score").index(self.sort_col)
            # Unchecked rows have a None score; keep them together at one end
            # rather than letting them collide with the numeric comparison.
            rows.sort(key=lambda t: (t[idx] is None, t[idx] if t[idx] is not None else 0),
                      reverse=self.sort_desc)

        for name, spoken, expected, heard, score in rows:
            self.tree.insert(
                "", "end", iid=name,
                values=(name, spoken, expected, heard,
                        "" if score is None else f"{score:.2f}"),
                tags=(self._band(score),))

        for iid in selected:
            if self.tree.exists(iid):
                self.tree.selection_add(iid)

        if not keep_status:
            done = sum(1 for n in names if self._result_for(n))
            self.status_var.set(f"{len(names)} name(s) shown — {done} checked, "
                                f"{len(names) - done} pending.")

    def _sort_by(self, col):
        self.sort_desc = not self.sort_desc if self.sort_col == col else False
        self.sort_col = col
        self.refresh(keep_status=True)

    # ----- checking -----------------------------------------------------
    def check_shown(self):
        self._start([n for n in self._visible_names() if not self._result_for(n)])

    def check_selected(self):
        self._start(list(self.tree.selection()))

    def _start(self, names):
        if self.running:
            return
        ok, msg = ipa_asr.available()
        if not ok:
            messagebox.showerror("Transcriber unavailable", msg)
            return
        if not names:
            self.status_var.set("Nothing to check — everything shown is already done.")
            return
        self.running, self._stop = True, False
        self.check_btn.configure(state="disabled")
        self.check_sel_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress.configure(maximum=len(names), value=0)
        threading.Thread(target=self._worker, args=(names,), daemon=True).start()

    def stop(self):
        self._stop = True
        self.status_var.set("Stopping after the current name…")

    def _worker(self, names):
        voice = self.voice_var.get()
        post = lambda fn, *a: self.root.after(0, fn, *a)  # noqa: E731
        for i, name in enumerate(names, 1):
            if self._stop:
                break
            info = self.names.get(name)
            if info is None:
                continue
            spoken = spoken_for(name, info)
            expected = info.get("ipa", "")
            post(self.status_var.set, f"[{i}/{len(names)}] {name} — “{spoken}”…")
            # Measure in every carrier and average. One reading is too noisy to
            # change a pronunciation on: the same name can keep or lose a
            # consonant depending only on the word that follows it.
            scores, spans, failed = [], [], False
            for text_fmt, head, tail in ipa_asr.CARRIERS:
                try:
                    path = tts_engine.synthesize(text_fmt.format(spoken), voice,
                                                 RATE, apply_respell=False)
                    heard = ipa_asr.transcribe(
                        path, status=lambda m: post(self.status_var.set, m))
                except Exception as e:  # noqa: BLE001 - one bad name must not kill the sweep
                    post(self.status_var.set, f"{name}: {e}")
                    failed = True
                    break
                span = ipa_asr.strip_carrier(heard, head, tail)
                if span:
                    spans.append(span)
                    scores.append(ipa_asr.similarity(expected, span))
            if failed:
                post(self._bump, i)  # keep the bar honest even when a name fails
                continue
            # No span in any carrier: a failure to measure, not a bad
            # pronunciation -- leave it unscored rather than reporting 0.00.
            score = (sum(scores) / len(scores)) if scores else None
            post(self._apply_result, name, {
                "spoken": spoken, "voice": voice, "mode": "carrier-avg",
                "heard": " / ".join(spans),
                "score": None if score is None else round(score, 3)}, i)
        post(self._finish)

    def _bump(self, i):
        self.progress.configure(value=i)

    def _apply_result(self, name, result, i):
        self.results[name] = result
        # A measurement is unsaved work: mark dirty so closing offers to keep the
        # verdicts rather than discarding a sweep that took an hour.
        self._mark_dirty()
        score = result["score"]
        if self.tree.exists(name):
            self.tree.item(name, values=(name, result["spoken"],
                                         self.names[name].get("ipa", ""),
                                         result["heard"] or "(nothing heard)",
                                         "—" if score is None else f"{score:.2f}"),
                           tags=(self._band(score),))
        self.progress.configure(value=i)
        if i % 25 == 0:
            self._save_cache()

    def _finish(self):
        self.running = False
        self.check_btn.configure(state="normal")
        self.check_sel_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self._save_cache()
        scores = [self.results[n]["score"] for n in self._visible_names()
                  if self._result_for(n)]
        checked = [s for s in scores if s is not None]
        unmeasured = len(scores) - len(checked)
        bad = sum(1 for s in checked if s < WARN_AT)
        warn = sum(1 for s in checked if WARN_AT <= s < OK_AT)
        self.status_var.set(
            f"Done — {len(checked)} checked: {bad} disagree, {warn} borderline, "
            f"{len(checked) - bad - warn} agree"
            + (f", {unmeasured} too short to measure" if unmeasured else "")
            + ".  Sort by Score to see the worst first.")

    # ----- per-row actions ----------------------------------------------
    def _selected_names(self):
        return [n for n in self.tree.selection() if n in self.names]

    def play_selected(self):
        names = self._selected_names()
        if not names or self.running:
            return
        name = names[0]
        info = self.names[name]
        spoken = spoken_for(name, info)
        # Play the primary carrier -- one of the two that were scored -- so what
        # you hear is what the transcriber heard.
        text = CARRIER.format(spoken)
        voice = self.voice_var.get()

        def work():
            try:
                path = tts_engine.synthesize(text, voice, RATE, apply_respell=False)
                self.player.load(path)
                self.player.play()
                msg = f"Playing “{text}”"
            except Exception as e:  # noqa: BLE001
                msg = f"Error: {e}"
            self.root.after(0, lambda: self.status_var.set(msg))

        threading.Thread(target=work, daemon=True).start()

    def use_heard(self):
        """Copy the transcribed IPA into the entry's reference ``ipa`` field."""
        names = [n for n in self._selected_names() if self._result_for(n)]
        if not names:
            self.status_var.set("Select one or more checked rows first.")
            return
        # The dangerous case: a name that already has a reference IPA which the
        # audio disagrees with. A low score there usually means the voice got it
        # wrong -- adopting what was heard would quietly enshrine the error.
        risky = [n for n in names
                 if self.names[n].get("ipa")
                 and self.results[n]["score"] is not None
                 and self.results[n]["score"] < OK_AT]
        if risky and not messagebox.askyesno(
                "Overwrite a disagreeing reference?",
                f"{len(risky)} of the selected name(s) — e.g. {risky[0]} — already "
                f"have an IPA that disagrees with the audio.\n\nA low score usually "
                f"means the voice is mispronouncing the name, not that the reference "
                f"is wrong. Overwriting would record the mispronunciation as "
                f"correct.\n\nOverwrite anyway?"):
            return
        for name in names:
            heard = self.results[name]["heard"]  # already display-ready IPA
            if not heard:
                continue
            self.names[name]["ipa"] = f"/{heard}/"
            # The stored reference just changed, so the old score is meaningless.
            self.results[name]["score"] = ipa_asr.similarity(
                self.names[name]["ipa"], self.results[name]["heard"])
        self._mark_dirty()
        self.refresh(keep_status=True)
        self.status_var.set(f"Set IPA from audio on {len(names)} name(s). Save to keep.")

    def _mark_dirty(self):
        if not self.dirty:
            self.dirty = True
            self.root.title("Pronunciation Verifier  *unsaved*")

    def _record_verdicts(self):
        """Fold this session's measurements into each entry's status.

        A sweep is only worth running if its conclusion is kept: without this,
        "checked and fine" would be indistinguishable from "never opened" the
        moment the window closes.
        """
        n = 0
        for name, r in self.results.items():
            info = self.names.get(name)
            if info is None or self._result_for(name) is None:
                continue           # stale result: the spelling or voice changed
            score = r.get("score")
            if info.get("override"):
                status = pronunciation.STATUS_FIXED
            elif score is None:
                continue           # could not be measured; leave the verdict alone
            elif score >= OK_AT:
                status = pronunciation.STATUS_OK
            else:
                status = pronunciation.STATUS_UNFIXED
            pronunciation.set_status(info, status, score)
            n += 1
        return n

    def save(self):
        recorded = self._record_verdicts()
        try:
            pronunciation.save_names(self.names)
        except Exception as e:  # noqa: BLE001
            messagebox.showerror("Save failed", str(e))
            return
        self.dirty = False
        self.root.title("Pronunciation Verifier")
        self._save_cache()
        self.status_var.set(f"Saved {len(self.names)} names to pronunciations.json "
                            f"+ PRONUNCIATIONS.md — recorded {recorded} verdict(s).")

    def _on_close(self):
        if self.running:
            self._stop = True
        if self.dirty:
            ans = messagebox.askyesnocancel("Unsaved changes", "Save your IPA changes?")
            if ans is None:
                return
            if ans:
                self.save()
        self._save_cache()
        self.player.close()
        self.root.destroy()


def main():
    config.ensure_dirs()
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
