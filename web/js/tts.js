// One utterance/clip per verse, so "ended" gives an exact verse-change event
// (mirrors the desktop app's per-verse-clip design). Two interchangeable
// backends per verse:
//   - "speech": Web Speech API (SpeechSynthesisUtterance) — always available.
//   - "audio":  a pre-generated neural mp3 (see generate_showcase_audio.py),
//     used when `resolveAudio(index)` returns a URL for the current verse.
// state: "stopped" | "playing" | "paused"

// A WAV with no samples, used only to "prime" the shared <audio> element
// inside a real user gesture so later programmatic .play() calls (triggered
// by a previous clip's "ended" event, or by the wait in _playAudioEl(), not a
// fresh tap) are still allowed under iOS Safari's autoplay policy.
const SILENT_WAV =
  "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=";

// iPadOS 13+ reports itself as "Macintosh", so the user-agent string alone
// misses iPads entirely — a Mac with a touchscreen is the tell.
const IS_IOS =
  /iPad|iPhone|iPod/.test(navigator.userAgent) ||
  (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);

// iOS: how long the first mp3 waits after unlock()'s primer reports done, and
// the cap, from the tap, for when it never does (see _whenPrimerDone()).
const PRIMER_SETTLE_MS = 400;
const PRIMER_MAX_WAIT_MS = 2000;
// iOS: after a wait that ended at the cap, how long from the tap one pause
// the player didn't ask for is retried, and how the retry is timed (see
// _onAudioPause()).
const RETRY_UNTIL_MS = 5000;
const RETRY_DELAY_MS = 250;
const RETRY_CHECK_MS = 1500;

export class Player {
  constructor({ onVerseChange, onStateChange, onEnd, onStart }) {
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
    // The mirror of onEnd: the user hit Prev on the first verse. The host uses
    // it to roll back into the previous chapter's last verse. Passed whether
    // playback was running so it can keep playing.
    this.onStart = onStart || (() => {});
    this._keepAlive = null;
    this._unlocked = false;
    // Generation counter: bumped every time the active clip is torn down.
    // Both backends deliver their end/error events asynchronously, so a
    // callback belonging to a clip we already abandoned can land after the
    // next clip has started. Every callback captures the generation it was
    // armed under and does nothing if it no longer matches.
    this._gen = 0;
    this._audioGen = -1; // generation that owns whatever is in audioEl
    this._utter = null; // utterance currently queued with the synth
    this._prefetchEl = null;
    this._prefetchedUrl = null;
    // iOS: pending until unlock()'s primer is done with the audio session;
    // the first mp3 waits for it (null once settled, and always off iOS).
    this._primerDone = null;
    // iOS: until this time a pause the player didn't ask for is retried once;
    // 0 = not armed, which it only is when that wait ended at the cap.
    this._retryUntil = 0;
    this.audioEl.addEventListener("pause", () => this._onAudioPause());
    this.audioEl.addEventListener("ended", () => {
      if (this._audioGen !== this._gen) return;
      this._onClipEnded();
    });
    this.audioEl.addEventListener("error", () => {
      // audioEl.error is cleared by the media load algorithm whenever a new
      // src is set, so a null here means this event belongs to a clip that
      // has already been replaced.
      if (this._audioGen !== this._gen || !this.audioEl.error) return;
      this._onClipError();
    });
  }

  // Must be called synchronously inside a user-gesture handler (tap) so iOS
  // Safari grants both speech and audio-element playback before any real
  // clip is queued.
  //
  // The primer is a volume-0 space, and it has to be spoken here even when
  // the verse is an mp3: iOS silently drops any speak() made outside a gesture
  // until one has been made inside one, and auto-advance can roll from an mp3
  // chapter into a Web Speech chapter with no tap. On iOS the first mp3 then
  // waits for the primer to finish — see _whenPrimerDone().
  //
  // The primer is deliberately never stored in `_utter`: that is how
  // _haltPlayback() tells it apart from a real verse and leaves it alone when
  // the clip about to start is an mp3 — see the note there.
  unlock() {
    if (this._unlocked) return;
    this._unlocked = true;
    const u = new SpeechSynthesisUtterance(" ");
    u.volume = 0;
    if (IS_IOS) this._primerDone = this._whenPrimerDone(u);
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

  // Why the first mp3 on iOS waits for the primer. WebKit hands speech to the
  // browser app's process, which speaks on the app's own audio session, while
  // media plays on a separate session of WebKit's own, and neither mixes with
  // the other. The first utterance after the page loads takes a second or so
  // to get going, and when it does its session takes over: WebKit treats that
  // as an interruption and pauses the mp3 that started in the same tap, and
  // nothing resumes it. That was the "plays for a second, then stops, but only
  // on the first Play" bug. Cancelling the primer doesn't help, because the
  // synthesizer still starts up. Once the primer is done, a play() takes the
  // session back from the idle synth, which is why every later Play worked.
  //
  // Resolves PRIMER_SETTLE_MS after the primer's end event (or an error other
  // than a cancel), so the hand-over has time to land. A cancel doesn't count,
  // because the synthesizer still starts up after one: a cancelled primer,
  // like one iOS never reports on, waits for the cap at PRIMER_MAX_WAIT_MS
  // after the tap. A wait that ends at the cap can't rule out the primer
  // starting on top of the first mp3, so it arms the one retry in
  // _onAudioPause() until RETRY_UNTIL_MS after the tap, or until a late report
  // from the primer has had its hand-over time.
  _whenPrimerDone(u) {
    const tappedAt = performance.now();
    return new Promise((resolve) => {
      let settled = false;
      const settle = (delay) => {
        if (settled) return;
        settled = true;
        setTimeout(() => {
          this._primerDone = null;
          resolve();
        }, delay);
      };
      const reported = () => {
        if (settled) setTimeout(() => { this._retryUntil = 0; }, PRIMER_SETTLE_MS);
        settle(PRIMER_SETTLE_MS);
      };
      u.onend = reported;
      u.onerror = (e) => {
        if (e.error !== "canceled" && e.error !== "interrupted") reported();
      };
      setTimeout(() => {
        if (settled) return;
        this._retryUntil = tappedAt + RETRY_UNTIL_MS;
        settle(0);
      }, PRIMER_MAX_WAIT_MS);
    });
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
      if (this.backend === "audio") this._playAudioEl();
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
    if (this.index <= 0) {
      this.onStart(this.state === "playing");
      return;
    }
    this.index--;
    this._afterManualNav();
  }

  jumpTo(i) {
    this.index = i;
    this._afterManualNav();
  }

  // Tear down whatever is sounding right now and orphan its callbacks.
  // synth.cancel() fires the pending utterance's "end"/"error" on a later
  // task, and swapping the <audio> element's src rejects its in-flight
  // play() promise — both of which used to arrive *after* the next verse had
  // started and were mistaken for that verse failing, which is how Web
  // Speech ended up reading over the top of a neural mp3 during fast skips.
  //
  // `cancelSpeech: false` says "the clip replacing this one is an mp3, so
  // leave the synth queue alone unless we actually put something in it".
  // That spares unlock()'s primer, which on the first tap is still queued: on
  // iOS the first mp3 waits for the primer to finish (_whenPrimerDone()), and
  // a cancel would report it finished at once while the synthesizer was still
  // starting up. Every utterance the player itself queues sets `_utter`, so
  // this can never suppress a cancel the fast-skip fix above depends on.
  _haltPlayback({ cancelSpeech = true } = {}) {
    this._gen++;
    const hadUtterance = Boolean(this._utter);
    if (this._utter) {
      this._utter.onend = null;
      this._utter.onerror = null;
      this._utter = null;
    }
    if (cancelSpeech || hadUtterance) this.synth.cancel();
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
    const url = this.resolveAudio ? this.resolveAudio(this.index) : null;
    // Resolve the next clip *before* tearing the old one down, so the
    // teardown knows whether it is handing over to the synth or to the mp3
    // element and can leave the other one's audio session untouched.
    this._haltPlayback({ cancelSpeech: !url });
    this.onVerseChange(this.index);
    if (url) {
      this.backend = "audio";
      this._audioGen = this._gen;
      this.audioEl.src = url;
      this.audioEl.playbackRate = this.rate;
      this._playAudioEl();
    } else {
      this.backend = "speech";
      this._speakCurrent();
    }
    this._prefetchNext();
  }

  _playAudioEl() {
    const gen = this._gen;
    if (this._primerDone) {
      // The first mp3 after unlock() on iOS waits for the primer (see
      // _whenPrimerDone()). Its src is already set, so it buffers meanwhile;
      // a Pause, Next or Stop in the meantime supersedes the wait.
      this._primerDone.then(() => {
        if (gen === this._gen && this.state === "playing" && this.backend === "audio") {
          this._playAudioEl();
        }
      });
      return;
    }
    const p = this.audioEl.play();
    if (!p || !p.catch) return;
    p.catch((err) => {
      if (gen !== this._gen) return; // superseded by a newer clip
      // AbortError means the play was interrupted by a pause or a new src,
      // not that the clip is unplayable — falling back to speech here is
      // what made both voices sound at once on rapid Next taps.
      if (err && err.name === "AbortError") return;
      // NotAllowedError on iOS means WebKit wants a fresh tap before this
      // element plays (the deferred first play() relies on the tap's priming
      // still counting), and the clip itself is fine: show Play, and that tap
      // resumes it. On a hidden page there is no one to tap, so the verse is
      // read with Web Speech as before.
      if (IS_IOS && err && err.name === "NotAllowedError" && document.visibilityState === "visible") {
        this._dropToPaused();
        return;
      }
      this._onClipError();
    });
  }

  // A pause the player didn't ask for. The player's own pauses stop at the
  // first two checks: pause() and stop() change the state first, a clip swap
  // bumps the generation (and setting the new src cancels the queued event),
  // _onClipError() switches the backend, and a clip that ran to its end
  // reports `ended`.
  //
  // Such a pause is left as it is — the remote Play that follows a Control
  // Center pause restarts the element without telling the player, and
  // auto-advance carries on only while the state still says "playing" — with
  // one exception. On iOS, when the wait for the primer ended at the cap
  // (_whenPrimerDone()), the primer may still start on top of the first mp3
  // and pause it, so until RETRY_UNTIL_MS after the tap one such pause on a
  // visible page is retried, and if the retry doesn't take, the button shows
  // Play so one tap resumes.
  _onAudioPause() {
    if (this._audioGen !== this._gen || this.state !== "playing" || this.backend !== "audio") return;
    if (!this.audioEl.paused || this.audioEl.ended) return;
    if (performance.now() > this._retryUntil || document.visibilityState !== "visible") return;
    this._retryUntil = 0; // once
    const gen = this._gen;
    const stillStopped = () =>
      gen === this._gen && this.state === "playing" && this.backend === "audio" && this.audioEl.paused;
    setTimeout(() => {
      if (!stillStopped() || document.visibilityState !== "visible") return;
      const p = this.audioEl.play();
      if (p && p.catch) p.catch(() => {}); // judged by the check below, never the speech fallback
      setTimeout(() => {
        if (stillStopped()) this._dropToPaused();
      }, RETRY_CHECK_MS);
    }, RETRY_DELAY_MS);
  }

  // The clip stopped without being asked to: show Play rather than a Pause
  // button over silence. The clip stays loaded, so the next tap resumes it
  // where it stopped (play()'s paused branch).
  _dropToPaused() {
    if (this.state !== "playing" || this.backend !== "audio") return;
    this.state = "paused";
    this._stopKeepAlive();
    this.onStateChange(this.state);
  }

  _speakCurrent() {
    const gen = this._gen;
    const [, text] = this.queue[this.index];
    const u = new SpeechSynthesisUtterance(text);
    u.rate = this.rate;
    if (this.voice) u.voice = this.voice;
    u.onend = () => { if (gen === this._gen) this._onClipEnded(); };
    u.onerror = () => { if (gen === this._gen) this._onClipError(); };
    this._utter = u;
    this.synth.speak(u);
    this._startKeepAlive();
  }

  // Warm the next verse's mp3 so a quick Next has it ready instead of
  // stalling on the network.
  //
  // Everywhere but iOS this is a detached element that is never played — some
  // browsers treat preload as a hint and ignore it, which costs nothing.
  //
  // On iOS that second media element is a liability: it is loaded from the
  // "ended" handler of the previous verse rather than from a user gesture, so
  // WebKit ignores the preload and warms nothing, while still poking the one
  // audio session the playing element is using — on iPad that clicked at
  // every verse change. A plain fetch stays clear of the audio session. It
  // doesn't fill the browser cache entry the element reads, because WebKit
  // keys cached responses by their Range header and the element's loads are
  // range requests, but it does warm Cloudflare's edge and the connection for
  // the next clip.
  _prefetchNext() {
    const url = this.resolveAudio ? this.resolveAudio(this.index + 1) : null;
    if (!url || url === this._prefetchedUrl) return;
    this._prefetchedUrl = url;
    try {
      if (IS_IOS) {
        fetch(url, { cache: "force-cache" }).catch(() => {});
        return;
      }
      const el = this._prefetchEl || (this._prefetchEl = new Audio());
      el.preload = "auto";
      el.src = url;
      el.load();
    } catch {
      // Prefetch is opportunistic; a failure just means the normal load path.
    }
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
      this.audioEl.pause(); // make sure the dud clip can't sound underneath
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
