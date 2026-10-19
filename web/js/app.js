import { BOOKS, DEFAULTS, chaptersIn, nextChapter, prevChapter } from "./data.js";
import { fetchChapter, PassageError } from "./bible.js";
import { VisualStage, bookGradient } from "./visuals.js";
import { Player } from "./tts.js";

const $ = (id) => document.getElementById(id);

const els = {
  book: $("sel-book"),
  chapter: $("sel-chapter"),
  verse: $("sel-verse"),
  stageWrap: $("stage-wrap"),
  stage: $("stage"),
  stageBg: $("stage-bg"),
  stageImgs: [$("stage-img"), $("stage-img-b")],
  idleMessage: $("idle-message"),
  stageEmpty: $("stage-empty"),
  emptyRef: $("empty-ref"),
  emptyLine: $("empty-line"),
  btnEmptyIll: $("btn-empty-ill"),
  btnPlay: $("btn-play"),
  btnStagePlay: $("btn-stage-play"),
  btnPrev: $("btn-prev"),
  btnNext: $("btn-next"),
  verseProgress: $("verse-progress"),
  versePanel: $("verse-panel"),
  btnIllustrated: $("btn-illustrated"),
  illOverlay: $("illustrated-overlay"),
  illClose: $("btn-illustrated-close"),
  illList: $("illustrated-list"),
};

const STORE_KEY = "theoria.selection";
// Keys from before the rename / the retired Still graphics toggle: the old
// selection is read once, then both are cleared.
const OLD_STORE_KEY = "avbible.web.selection";
const OLD_MOTION_PREF = "avbible.web.stillGraphics";

// localStorage can throw (blocked site data, some private modes). Every
// access goes through these so a storage failure never stops the app.
function safeGet(key) {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

function safeSet(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch {
    // nothing to do — the selection just won't be remembered
  }
}

function safeRemove(key) {
  try {
    localStorage.removeItem(key);
  } catch {
    // ignore
  }
}

// The stage's resting text, written once in index.html so it shows at first
// paint, before any of this has loaded.
const IDLE_TEXT = els.idleMessage.textContent;

const stage = new VisualStage();
let passage = null; // current fetched chapter {book,chapter,canonical,verses}
let lastImagePath = null;

// The stage has two <img>s. A new picture loads into the hidden one and is
// shown only once it has decoded. Swapping one <img>'s src made Chrome and
// Edge paint a single wrong frame - another part of the tree - at the start
// of every tree verse; iOS never did. pictureToken lets only the latest
// request win when verses change faster than pictures decode.
let frontImg = 0;
let pictureToken = 0;

function showPicture(url) {
  const my = ++pictureToken;
  const front = els.stageImgs[frontImg];
  const back = els.stageImgs[1 - frontImg];
  back.classList.remove("visible");
  back.classList.add("loading");
  back.src = url;
  back.decode().catch(() => {}).then(() => {
    if (my !== pictureToken) return;
    back.classList.remove("loading");
    back.classList.add("visible");
    front.classList.remove("visible", "loading");
    front.removeAttribute("src");
    frontImg = 1 - frontImg;
  });
}

function clearPicture() {
  ++pictureToken;
  for (const img of els.stageImgs) {
    img.classList.remove("visible", "loading");
    img.removeAttribute("src");
  }
}
// The verse on stage ("Book|chapter|index"). Rendering it again means
// playback is starting on the verse already shown (Play from stopped, or a
// tap on that verse), and its picture starts again in step with the
// narration. Moving to another verse never restarts a shared picture (D17).
let shownVerse = null;
let audioManifest = {}; // "Book_ch_v.WEB" -> "filename.mp3", pre-generated neural narration

const player = new Player({
  onVerseChange: (index) => renderVerse(index),
  onStateChange: (state) => updatePlayButtons(state),
  onEnd: (wasPlaying) => advanceToNextChapter(wasPlaying),
  onStart: (wasPlaying) => retreatToPrevChapter(wasPlaying),
});
player.resolveAudio = resolveAudio;

// Pre-generated neural mp3s (generate_showcase_audio.py / the desktop Audio
// Renderer studio) narrate a handful of showcase chapters — much better
// quality than the browser's Web Speech voice. Keys are "Book_ch_v.WEB"
// (e.g. "Genesis_1_1.WEB"), the format the producers write; every verse
// without one falls back to speech.
async function loadAudioManifest() {
  try {
    const resp = await fetch("audio/manifest.json", { cache: "no-cache" });
    audioManifest = resp.ok ? await resp.json() : {};
  } catch {
    audioManifest = {};
  }
}

function resolveAudio(index) {
  if (!passage || !passage.verses[index]) return null;
  const [num] = passage.verses[index];
  const key = `${passage.book.replace(/ /g, "_")}_${passage.chapter}_${num}`;
  const filename = audioManifest[`${key}.WEB`];
  return filename ? `audio/${filename}` : null;
}

// ---------------------------------------------------------------------
// Picker population
// ---------------------------------------------------------------------

// "✦" marks books/chapters that have visuals built (see
// VisualStage.illustratedChapters). U+2726 has no emoji presentation, so
// iOS keeps it monochrome — same reasoning as the ICON SVGs below, except
// <option> text can't hold SVG, so a safe glyph is the only choice here.
const ILL_MARK = "✦";

function populateBooks() {
  const lit = stage.illustratedChapters();
  els.book.innerHTML = BOOKS.map(([name]) => {
    const mark = lit.has(name) ? ` ${ILL_MARK}` : "";
    return `<option value="${name}">${name}${mark}</option>`;
  }).join("");
}

function populateChapters(book) {
  const n = chaptersIn(book);
  const lit = stage.illustratedChapters().get(book);
  const opts = [];
  for (let c = 1; c <= n; c++) {
    const mark = lit && lit.has(c) ? ` ${ILL_MARK}` : "";
    opts.push(`<option value="${c}">${c}${mark}</option>`);
  }
  els.chapter.innerHTML = opts.join("");
}

function populateVerses(verses) {
  els.verse.innerHTML = verses
    .map(([num]) => `<option value="${num}">${num}</option>`)
    .join("");
}

// ---------------------------------------------------------------------
// Selection persistence
// ---------------------------------------------------------------------

function loadSelection() {
  const current = safeGet(STORE_KEY);
  let selection = { ...DEFAULTS };
  try {
    const { book, chapter } = JSON.parse(current ?? safeGet(OLD_STORE_KEY) ?? "{}");
    const known = BOOKS.some(([name]) => name === book);
    if (known && Number.isInteger(chapter) && chapter >= 1 && chapter <= chaptersIn(book)) {
      selection = { book, chapter };
    }
  } catch {
    // junk in storage: fall back to the defaults
  }
  if (current === null) safeSet(STORE_KEY, JSON.stringify(selection)); // migrate first
  safeRemove(OLD_STORE_KEY);
  safeRemove(OLD_MOTION_PREF);
  return selection;
}

function saveSelection() {
  safeSet(
    STORE_KEY,
    JSON.stringify({
      book: els.book.value,
      chapter: Number(els.chapter.value),
    })
  );
}

// ---------------------------------------------------------------------
// Chapter loading
// ---------------------------------------------------------------------

async function loadChapter({ resetStage = true, startAtEnd = false } = {}) {
  const book = els.book.value;
  const chapter = Number(els.chapter.value);
  player.stop();
  try {
    passage = await fetchChapter(book, chapter);
  } catch (e) {
    passage = null;
    showIdle(e instanceof PassageError ? e.message : "Could not load this chapter.");
    els.versePanel.innerHTML = "";
    els.verse.innerHTML = "";
    return;
  }
  populateVerses(passage.verses);
  renderVersePanel();
  player.load(passage.verses, startAtEnd ? passage.verses.length - 1 : 0);
  player.voice = pickVoice();
  saveSelection();
  if (resetStage) showIdle();
}

// Roll from the last verse of the current chapter into the first verse of the
// next — triggered by playback reaching the end, or Next on the last verse.
// Keeps playing across the boundary if we were playing; otherwise just shows
// the new chapter's first verse. Stops at the end of Revelation.
async function advanceToNextChapter(wasPlaying) {
  const next = passage && nextChapter(passage.book, passage.chapter);
  if (!next) {
    player.stop();
    return;
  }
  els.book.value = next.book;
  populateChapters(next.book);
  els.chapter.value = String(next.chapter);
  rolling = wasPlaying;
  await loadChapter({ resetStage: false });
  rolling = false;
  if (passage && wasPlaying) player.play();
  else if (passage) renderVerse(0);
  syncWakeLock(); // if the load failed (e.g. offline), let the screen sleep
}

// The mirror of advanceToNextChapter: Prev on the first verse rolls back into
// the previous chapter and lands on its *last* verse, so a double-tap-left run
// walks backwards across the boundary the same way double-tap-right walks
// forwards. Keeps playing if we were playing. No-op at Genesis 1:1.
async function retreatToPrevChapter(wasPlaying) {
  const prev = passage && prevChapter(passage.book, passage.chapter);
  if (!prev) return; // nothing before Genesis 1:1 — stay put, keep playing
  els.book.value = prev.book;
  populateChapters(prev.book);
  els.chapter.value = String(prev.chapter);
  rolling = wasPlaying;
  await loadChapter({ resetStage: false, startAtEnd: true });
  rolling = false;
  if (passage && wasPlaying) player.play();
  else if (passage) renderVerse(player.index);
  syncWakeLock(); // if the load failed (e.g. offline), let the screen sleep
}

function pickVoice() {
  const voices = window.speechSynthesis.getVoices();
  return voices.find((v) => v.lang && v.lang.startsWith("en")) || voices[0] || null;
}
window.speechSynthesis?.addEventListener?.("voiceschanged", () => {
  if (player) player.voice = pickVoice();
});

// ---------------------------------------------------------------------
// Verse text panel (read-along list; stage itself stays image + reference,
// matching the desktop app's choice not to draw verse text on the stage)
// ---------------------------------------------------------------------

function renderVersePanel() {
  if (!passage) {
    els.versePanel.innerHTML = "";
    return;
  }
  els.versePanel.innerHTML = passage.verses
    .map(
      ([num, text], i) =>
        `<p data-index="${i}" tabindex="0" role="button"><span class="vnum">${num}</span>${escapeHtml(text)}</p>`
    )
    .join("");
  els.versePanel.querySelectorAll("p").forEach((p) => {
    const playFromHere = () => {
      player.unlock();
      player.jumpTo(Number(p.dataset.index));
      if (player.state !== "playing") player.play();
    };
    p.addEventListener("click", playFromHere);
    p.addEventListener("keydown", (e) => {
      if (e.code !== "Enter" && e.code !== "Space") return;
      e.preventDefault();
      e.stopPropagation(); // not the page-wide Space = play/pause
      playFromHere();
    });
  });
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

// ---------------------------------------------------------------------
// Stage rendering
// ---------------------------------------------------------------------

// The book is "Psalms", but a single psalm is "Psalm 23:1".
function refBook(book) {
  return book === "Psalms" ? "Psalm" : book;
}

function showIdle(message) {
  els.idleMessage.style.display = "flex";
  els.idleMessage.textContent = message || IDLE_TEXT;
  clearPicture();
  lastImagePath = null; // the next picture loads fresh
  shownVerse = null;
  els.stageEmpty.hidden = true;
  els.stageBg.style.background = "#101018";
  els.verseProgress.textContent = "\u00a0";
  clearCurrentHighlight();
}

// A verse with nothing drawn for it: the book gradient, the reference, and a
// way into the chapters that are illustrated.
function showNotIllustrated(ctx) {
  const lit = stage.illustratedChapters().get(ctx.book);
  els.emptyRef.textContent = ctx.reference;
  els.emptyLine.textContent =
    lit && lit.has(ctx.chapter)
      ? "This verse isn't illustrated yet."
      : `${refBook(ctx.book)} ${ctx.chapter} isn't illustrated yet.`;
  els.stageEmpty.hidden = false;
}

function clearCurrentHighlight() {
  els.versePanel.querySelectorAll("p.current").forEach((p) => p.classList.remove("current"));
}

function renderVerse(index) {
  if (!passage) return;
  const [num] = passage.verses[index];
  const verseId = `${passage.book}|${passage.chapter}|${index}`;
  const replay = verseId === shownVerse;
  shownVerse = verseId;
  const ctx = {
    book: passage.book,
    chapter: passage.chapter,
    verse: num,
    reference: `${refBook(passage.book)} ${passage.chapter}:${num}`,
  };

  els.idleMessage.style.display = "none";

  const { top, bottom } = bookGradient(ctx.book);
  els.stageBg.style.background = `linear-gradient(180deg, ${top}, ${bottom})`;

  const visual = stage.findVisual(ctx);
  const imgPath = visual ? visual.url : null;
  if (imgPath) {
    els.stageEmpty.hidden = true;
    // The same picture as the verse before (a shared range file, or an
    // identical copy the manifest points at one file) keeps running, or
    // stays finished: it restarts only when the picture changes (D17).
    if (replay) {
      // A fresh URL is the restart every browser honours (re-setting the
      // same URL can leave a cached SVG at its last frame).
      showPicture(`${imgPath}?r=${Date.now()}`);
    } else if (imgPath !== lastImagePath) {
      showPicture(imgPath);
    }
    lastImagePath = imgPath;
  } else {
    clearPicture();
    lastImagePath = null;
    showNotIllustrated(ctx);
  }

  els.verseProgress.textContent =
    `${ctx.reference} · ${index + 1}/${passage.verses.length}`;
  els.verse.value = String(num);

  clearCurrentHighlight();
  const p = els.versePanel.querySelector(`p[data-index="${index}"]`);
  if (p) {
    p.classList.add("current");
    p.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }
}

// Monochrome inline-SVG icons. Using glyphs (▶ ⏸ ⛶) instead makes iOS
// Safari render color emoji ("emoji in a circle"); SVG paths inherit the
// button's text color and stay crisp at any size.
const ICON = {
  play: '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l12-7.5z"/></svg>',
  pause:
    '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="4.5" width="4.2" height="15" rx="1.1"/><rect x="13.8" y="4.5" width="4.2" height="15" rx="1.1"/></svg>',
  enterFs:
    '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5"/></svg>',
  exitFs:
    '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 4v5H4M20 9h-5V4M15 20v-5h5M4 15h5v5"/></svg>',
};

// Screen Wake Lock: keep the screen on while a chapter plays. The browser
// drops the lock whenever the page is hidden, so it is re-requested when the
// page comes back. Unsupported or refused: the screen may dim, nothing else.
let wakeLock = null;
let playing = false;
let rolling = false; // between chapters while playing: keep the screen on

async function syncWakeLock() {
  if (!navigator.wakeLock) return;
  const wanted = playing || rolling;
  if (wanted && !wakeLock && document.visibilityState === "visible") {
    let lock;
    try {
      lock = await navigator.wakeLock.request("screen");
    } catch {
      return; // refused or unsupported: leave any lock we hold alone
    }
    if (!(playing || rolling) || wakeLock) {
      lock.release(); // stopped, or a second request won, while we waited
      return;
    }
    wakeLock = lock;
    lock.addEventListener("release", () => {
      if (wakeLock === lock) wakeLock = null;
    });
  } else if (!wanted && wakeLock) {
    const lock = wakeLock;
    wakeLock = null;
    lock.release().catch(() => {});
  }
}

document.addEventListener("visibilitychange", syncWakeLock);

function updatePlayButtons(state) {
  playing = state === "playing";
  syncWakeLock();
  els.btnPlay.innerHTML =
    (playing ? ICON.pause : ICON.play) +
    `<span class="btn-label">${playing ? "Pause" : "Play"}</span>`;
  els.btnStagePlay.innerHTML = playing ? ICON.pause : ICON.play;
  els.btnStagePlay.setAttribute("aria-label", playing ? "Pause" : "Play");
}

// ---------------------------------------------------------------------
// Controls
// ---------------------------------------------------------------------

function startVerseIndex() {
  if (!passage) return 0;
  const target = Number(els.verse.value);
  const i = passage.verses.findIndex(([num]) => num === target);
  return i >= 0 ? i : 0;
}

function togglePlay() {
  player.unlock(); // must run synchronously inside this gesture handler
  if (!passage) return;
  if (player.state === "playing") {
    player.pause();
  } else {
    // player.index already reflects wherever the verse dropdown, Prev/Next,
    // or a verse-panel tap last left it — no need to re-jump here.
    player.play();
  }
}

els.btnPlay.addEventListener("click", togglePlay);

// A picture that failed to load (offline, a flaky connection) is retried by
// the next verse or Play, even inside a run that shares it.
for (const img of els.stageImgs) {
  img.addEventListener("error", () => { lastImagePath = null; });
}

els.btnPrev.addEventListener("click", () => { player.unlock(); player.prev(); });
els.btnNext.addEventListener("click", () => { player.unlock(); player.next(); });


els.book.addEventListener("change", () => {
  populateChapters(els.book.value);
  els.chapter.value = "1";
  loadChapter();
});
els.chapter.addEventListener("change", () => loadChapter());
els.verse.addEventListener("change", () => {
  player.unlock();
  player.jumpTo(startVerseIndex());
});

// ---------------------------------------------------------------------
// Illustrated-chapters jump list: a panel listing every chapter that has
// visuals built (per visuals/manifest.json), one tap-to-jump chip each.
// Jumping renders the chapter's first verse immediately — the point is to
// *see* the visuals — unlike the pickers, which leave the stage idle.
// ---------------------------------------------------------------------

function buildIllustratedList() {
  const lit = stage.illustratedChapters();
  const parts = [];
  for (const [name] of BOOKS) {
    const chapters = lit.get(name);
    if (!chapters || chapters.size === 0) continue;
    const chips = [...chapters]
      .sort((a, b) => a - b)
      .map(
        (c) =>
          `<button class="ill-chip" data-book="${name}" data-chapter="${c}">${c}</button>`
      )
      .join("");
    parts.push(
      `<div class="ill-book"><span class="ill-book-name">${name}</span><span class="ill-chips">${chips}</span></div>`
    );
  }
  els.illList.innerHTML = parts.length
    ? parts.join("")
    : '<p class="ill-hint">No illustrated chapters yet.</p>';
  els.illList.querySelectorAll(".ill-chip").forEach((chip) => {
    chip.addEventListener("click", async () => {
      els.book.value = chip.dataset.book;
      populateChapters(chip.dataset.book);
      els.chapter.value = chip.dataset.chapter;
      illReturnFocus = els.btnPlay; // ready to press Play on the new chapter
      closeIllustrated();
      await loadChapter({ resetStage: false });
      if (passage) renderVerse(0);
    });
  });
}

// Focus moves into the dialog on open and back to whatever opened it on
// close, so keyboard users land where they were.
let illReturnFocus = null;
// Everything behind the list. Inert while it is open, so Tab stays inside the
// dialog and nothing behind it can be clicked or keyed.
const BEHIND_DIALOG = ["header", "#stage-wrap", "#controls", "#verse-panel", "footer"]
  .map((sel) => document.querySelector(sel));

function setBehindInert(on) {
  for (const el of BEHIND_DIALOG) el.inert = on;
}

function openIllustrated() {
  illReturnFocus = document.activeElement;
  setBehindInert(true);
  els.illOverlay.hidden = false;
  els.illClose.focus();
}

function closeIllustrated() {
  els.illOverlay.hidden = true;
  setBehindInert(false);
  const back = illReturnFocus && document.contains(illReturnFocus)
    ? illReturnFocus
    : els.btnIllustrated;
  illReturnFocus = null;
  back.focus();
}

els.btnIllustrated.addEventListener("click", openIllustrated);
els.illClose.addEventListener("click", closeIllustrated);
els.illOverlay.addEventListener("click", (e) => {
  if (e.target === els.illOverlay) closeIllustrated(); // backdrop tap
});

// ---------------------------------------------------------------------
// Fullscreen + stage gestures
//
// Where the Fullscreen API exists (desktop, Android) we use it for true
// fullscreen; iOS Safari refuses requestFullscreen on plain <div>s, so a
// fixed-position CSS overlay stands in. (For no-browser-chrome on iPhone,
// the app must be installed to the home screen — see manifest.webmanifest.)
//
// Gestures, video-player style: a single tap reveals the on-stage
// controls (a center Play/Pause button, plus the fullscreen toggle);
// they fade out on their own. A double tap on the left half goes back a
// verse, right half forward. The fullscreen ENTER button is a special
// case: while not in fullscreen it stays permanently visible, to nudge
// mobile users toward a fullscreen view.
// ---------------------------------------------------------------------

const fsBtn = $("btn-fullscreen");
let controlsHideTimer = null;

function isFullscreen() {
  return els.stageWrap.classList.contains("fullscreen");
}

function updateFsButton() {
  const on = isFullscreen();
  fsBtn.innerHTML = on ? ICON.exitFs : ICON.enterFs;
  fsBtn.setAttribute("aria-label", on ? "Exit full screen" : "Enter full screen");
  // Persistent when not fullscreen; transient (tap-to-reveal) in fullscreen.
  if (!on) fsBtn.classList.add("show");
}

// Reveal the transient on-stage controls, then fade them out. The center
// Play/Pause always fades; the fullscreen toggle only fades in fullscreen
// (outside fullscreen it must stay put — see updateFsButton).
function revealControls() {
  els.btnStagePlay.classList.add("show");
  fsBtn.classList.add("show");
  clearTimeout(controlsHideTimer);
  controlsHideTimer = setTimeout(() => {
    els.btnStagePlay.classList.remove("show");
    if (isFullscreen()) fsBtn.classList.remove("show");
  }, 3000);
}

function setFullscreen(on) {
  els.stageWrap.classList.toggle("fullscreen", on);
  if (on && els.stageWrap.requestFullscreen) {
    els.stageWrap.requestFullscreen().catch(() => {});
  } else if (!on && document.fullscreenElement) {
    document.exitFullscreen().catch(() => {});
  }
  updateFsButton();
  revealControls();
}

// Orientation-driven fullscreen on touch devices.
//
// A web app can't really lock the iPhone's orientation — iOS Safari has no
// Screen Orientation API — and faking a lock by rotating the stage 90° meant
// every physical rotation still re-laid-out the page underneath, which read
// as clunky. So rather than fight the rotation, follow it: turning the phone
// to landscape enters fullscreen, turning it back to portrait leaves.
//
// Manual control is untouched — the toggle still works in either
// orientation. `autoEnteredFs` records whether *we* opened fullscreen, so a
// fullscreen the user deliberately opened in portrait survives a round trip
// through landscape, and one they deliberately closed in landscape stays
// closed until the next rotation.
const LANDSCAPE = window.matchMedia
  ? window.matchMedia("(orientation: landscape)")
  : null;
const COARSE = window.matchMedia ? window.matchMedia("(pointer: coarse)") : null;
let autoEnteredFs = false;

function onOrientationChange() {
  if (!COARSE || !COARSE.matches) return; // phones/tablets only
  if (LANDSCAPE.matches) {
    if (isFullscreen()) return;
    setFullscreen(true);
    autoEnteredFs = true;
  } else if (isFullscreen() && autoEnteredFs) {
    setFullscreen(false);
    autoEnteredFs = false;
  }
}

if (LANDSCAPE) {
  if (LANDSCAPE.addEventListener) LANDSCAPE.addEventListener("change", onOrientationChange);
  else if (LANDSCAPE.addListener) LANDSCAPE.addListener(onOrientationChange);
}

// Exiting API fullscreen via a system gesture (Back, swipe) must also
// clear the CSS overlay so both mechanisms stay in sync.
document.addEventListener("fullscreenchange", () => {
  if (!document.fullscreenElement) {
    els.stageWrap.classList.remove("fullscreen");
    autoEnteredFs = false;
  }
  updateFsButton();
});

// The "not illustrated yet" pointer opens the ✦ list. The list sits outside
// #stage-wrap, and real fullscreen shows only the fullscreen element, so
// leave fullscreen first or the list would open where no one can see it.
els.btnEmptyIll.addEventListener("click", (e) => {
  e.stopPropagation(); // not a stage tap (no reveal, no double-tap nav)
  if (isFullscreen()) {
    setFullscreen(false);
    autoEnteredFs = false;
  }
  openIllustrated();
});

fsBtn.addEventListener("click", (e) => {
  e.stopPropagation(); // not a stage tap
  setFullscreen(!isFullscreen());
  autoEnteredFs = false; // an explicit choice outranks the next rotation
});

// Center Play/Pause: toggles playback, then re-reveals so the freshly
// updated icon lingers briefly before fading.
els.btnStagePlay.addEventListener("click", (e) => {
  e.stopPropagation(); // not a stage tap
  togglePlay();
  revealControls();
});

const DOUBLE_TAP_MS = 350;
let tapTimer = null;
let lastTapTime = 0;

els.stage.addEventListener("click", (e) => {
  const now = Date.now();
  if (now - lastTapTime < DOUBLE_TAP_MS) {
    // Double tap: left half = previous verse, right half = next.
    lastTapTime = 0;
    clearTimeout(tapTimer);
    tapTimer = null;
    if (!passage) return;
    const rect = els.stage.getBoundingClientRect();
    player.unlock(); // synchronous, inside the gesture handler
    const firstHalf = e.clientX - rect.left < rect.width / 2;
    if (firstHalf) player.prev();
    else player.next();
  } else {
    // Wait out the double-tap window before treating it as a single tap.
    lastTapTime = now;
    clearTimeout(tapTimer);
    tapTimer = setTimeout(() => {
      tapTimer = null;
      revealControls();
    }, DOUBLE_TAP_MS);
  }
});

document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "SELECT" || e.target.tagName === "INPUT") return;
  // Inside the ✦ dialog, keys work its chips and close button; only Escape
  // (close) is handled here.
  if (!els.illOverlay.hidden && e.code !== "Escape") return;
  if (e.code === "Space") { e.preventDefault(); togglePlay(); }
  else if (e.code === "ArrowRight") player.next();
  else if (e.code === "ArrowLeft") player.prev();
  else if (e.code === "Escape") {
    if (!els.illOverlay.hidden) { closeIllustrated(); return; }
    setFullscreen(false);
    autoEnteredFs = false;
  }
});

updateFsButton();

// ---------------------------------------------------------------------
// Boot
// ---------------------------------------------------------------------

async function boot() {
  await Promise.all([stage.loadManifest(), loadAudioManifest()]);
  // After the manifest, so book/chapter options carry their ✦ markers.
  populateBooks();
  buildIllustratedList();

  const saved = loadSelection();
  els.book.value = saved.book;
  populateChapters(saved.book);
  els.chapter.value = String(saved.chapter);

  await loadChapter();
}

boot();
