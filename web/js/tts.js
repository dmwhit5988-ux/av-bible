// One utterance/clip per verse, so "ended" gives an exact verse-change event
// (mirrors the desktop app's per-verse-clip design). Two interchangeable
// backends per verse:
//   - "speech": Web Speech API (SpeechSynthesisUtterance) — always available.
//   - "audio":  a pre-generated neural mp3 (see generate_showcase_audio.py),
//     used when `resolveAudio(index)` returns a URL for the current verse.
// state: "stopped" | "playing" | "paused"

// A near-silent one-sample WAV, used only to "prime" the shared <audio>
// element inside a real user gesture so later programmatic .play() calls
// (triggered by a previous clip's "ended" event, not a fresh tap) are still
// allowed under iOS Safari's autoplay policy.
const SILENT_WAV =
  "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=";

export class Player {
  constructor({ onVerseChange, onStateChange, onEnd }) {
    this.synth = window.speechSynthesis;
    this.audioEl = new Audio();
    this.queue = []; // [[num, text], ...]
    this.index = 0;
    this.state = "stopped";
    this.backend = null; // "speech" | "audio" | null
    this.rate = 1;
    this.voice = null;
    this.resolveAudio = null; // (index) => url string | null
    this.onVerseChange = onVerseChange || (() => {});
    this.onStateChange = onStateChange || (() => {});
    // Fired when playback runs off the end of the queue (auto-advance) or the
    // user hits Next on the last verse. The host uses it to roll into the next
    // chapter. Passed whether playback was running so it can keep playing.
    this.onEnd = onEnd || (() => {});
    this._keepAlive = null;
    this._unlocked = false;
    this.audioEl.addEventListener("ended", () => this._onClipEnded());
    this.audioEl.addEventListener("error", () => this._onClipError());
  }

  // Must be called synchronously inside a user-gesture handler (tap) so iOS
  // Safari grants both speech and audio-element playback before any real
  // clip is queued.
  unlock() {
    if (this._unlocked) return;
    this._unlocked = true;
    const u = new SpeechSynthesisUtterance(" ");
    u.volume = 0;
    this.synth.speak(u);
    try {
      this.audioEl.src = SILENT_WAV;
      const p = this.audioEl.play();
      if (p && p.catch) p.catch(() => {});
      this.audioEl.pause();
    } catch {
      // Autoplay policies vary; a failed priming attempt just means the
      // first real clip may need another tap, not worth surfacing.
    }
  }

  load(verses, startIndex = 0) {
    this.stop();
    this.queue = verses;
    this.index = Math.min(Math.max(startIndex, 0), Math.max(verses.length - 1, 0));
  }

  play() {
    if (!this.queue.length) return;
    if (this.state === "paused") {
      this.state = "playing";
      this.onStateChange(this.state);
      if (this.backend === "audio") this.audioEl.play().catch(() => this._onClipError());
      else {
        this.synth.resume();
        this._startKeepAlive();
      }
      return;
    }
    this.state = "playing";
    this.onStateChange(this.state);
    this._playCurrent();
  }

  pause() {
    if (this.state !== "playing") return;
    if (this.backend === "audio") this.audioEl.pause();
    else this.synth.pause();
    this.state = "paused";
    this._stopKeepAlive();
    this.onStateChange(this.state);
  }

  stop() {
    this._haltPlayback();
    this.state = "stopped";
    this._stopKeepAlive();
    this.onStateChange(this.state);
  }

  next() {
    if (this.index >= this.queue.length - 1) {
      this.onEnd(this.state === "playing");
      return;
    }
    this.index++;
    this._afterManualNav();
  }

  prev() {
    if (this.index <= 0) return;
    this.index--;
    this._afterManualNav();
  }

  jumpTo(i) {
    this.index = i;
    this._afterManualNav();
  }

  _haltPlayback() {
    this.synth.cancel();
    this.audioEl.pause();
  }

  // A stale paused clip belongs to whatever verse we just navigated away
  // from — resuming it would play/speak the wrong text. Drop back to
  // "stopped" so the next Play tap starts fresh at the new index instead.
  _afterManualNav() {
    if (this.state === "playing") {
      this._playCurrent();
      return;
    }
    if (this.state === "paused") {
      this._haltPlayback();
      this.state = "stopped";
      this._stopKeepAlive();
      this.onStateChange(this.state);
    }
    this.onVerseChange(this.index);
  }

  _playCurrent() {
    this._haltPlayback();
    const url = this.resolveAudio ? this.resolveAudio(this.index) : null;
    this.onVerseChange(this.index);
    if (url) {
      this.backend = "audio";
      this.audioEl.src = url;
      this.audioEl.playbackRate = this.rate;
      this.audioEl.play().catch(() => this._onClipError());
    } else {
      this.backend = "speech";
      this._speakCurrent();
    }
  }

  _speakCurrent() {
    const [, text] = this.queue[this.index];
    const u = new SpeechSynthesisUtterance(text);
    u.rate = this.rate;
    if (this.voice) u.voice = this.voice;
    u.onend = () => this._onClipEnded();
    u.onerror = () => this._onClipError();
    this.synth.speak(u);
    this._startKeepAlive();
  }

  _onClipEnded() {
    if (this.state !== "playing") return;
    if (this.index < this.queue.length - 1) {
      this.index++;
      this._playCurrent();
    } else {
      // End of chapter reached mid-playback. Pause the audio machinery but
      // stay in "playing" so the host can roll straight into the next chapter;
      // if there is no next chapter it will stop us.
      this._haltPlayback();
      this._stopKeepAlive();
      this.onEnd(true);
    }
  }

  _onClipError() {
    // A pre-generated clip that failed to load (offline, bad path) falls
    // back to Web Speech for just this verse rather than stalling playback.
    this._stopKeepAlive();
    if (this.state === "playing" && this.backend === "audio") {
      this.backend = "speech";
      this._speakCurrent();
    }
  }

  // Chrome/WebKit both have a known bug where long-running speech silently
  // stops after ~15s of the tab/page being idle. Nudging pause/resume keeps
  // the queue alive without restarting the current utterance. Only applies
  // to the speech backend — audio-element playback isn't affected.
  _startKeepAlive() {
    this._stopKeepAlive();
    this._keepAlive = setInterval(() => {
      if (this.backend === "speech" && this.synth.speaking && !this.synth.paused) {
        this.synth.pause();
        this.synth.resume();
      }
    }, 4000);
  }

  _stopKeepAlive() {
    if (this._keepAlive) clearInterval(this._keepAlive);
    this._keepAlive = null;
  }
}
