import { BOOKS, TRANSLATIONS, TRANSLATION_ATTRIBUTION, DEFAULTS, chaptersIn } from "./data.js";
import { fetchChapter, PassageError } from "./bible.js";
import { VisualStage, bookGradient } from "./visuals.js";
import { Player } from "./tts.js";

const $ = (id) => document.getElementById(id);

const els = {
  translation: $("sel-translation"),
  book: $("sel-book"),
  chapter: $("sel-chapter"),
  verse: $("sel-verse"),
  attribution: $("attribution"),
  stageWrap: $("stage-wrap"),
  stage: $("stage"),
  stageBg: $("stage-bg"),
  stageImg: $("stage-img"),
  stageText: $("stage-text"),
  idleMessage: $("idle-message"),
  notesBox: $("notes-box"),
  referenceBox: $("reference-box"),
  btnPlay: $("btn-play"),
  btnStagePlay: $("btn-stage-play"),
  btnPrev: $("btn-prev"),
  btnNext: $("btn-next"),
  verseProgress: $("verse-progress"),
  chkNotes: $("chk-notes"),
  chkReference: $("chk-reference"),
  rateSlider: $("rate-slider"),
  versePanel: $("verse-panel"),
};

const STORE_KEY = "avbible.web.selection";

const stage = new VisualStage();
let passage = null; // current fetched chapter {book,chapter,canonical,translation,verses,notes}
let lastImagePath = null;
let stageTextToken = 0; // invalidates in-flight text-visual fetches
let audioManifest = {}; // "Book_ch_v" -> "Book_ch_v.mp3", pre-generated neural narration

const player = new Player({
  onVerseChange: (index) => renderVerse(index),
  onStateChange: (state) => updatePlayButtons(state),
});
player.resolveAudio = resolveAudio;

// Pre-generated neural mp3s (generate_showcase_audio.py) narrate the fixed
// WEB text for a handful of showcase chapters — much better quality than
// the browser's Web Speech voice. Only usable when WEB is selected; every
// other translation, and every verse without a clip, falls back to speech.
async function loadAudioManifest() {
  try {
    const resp = await fetch("audio/manifest.json");
    audioManifest = resp.ok ? await resp.json() : {};
  } catch {
    audioManifest = {};
  }
}

function resolveAudio(index) {
  if (!passage || passage.translation !== "WEB" || !passage.verses[index]) return null;
  const [num] = passage.verses[index];
  const key = `${passage.book.replace(/ /g, "_")}_${passage.chapter}_${num}`;
  const filename = audioManifest[key];
  return filename ? `audio/${filename}` : null;
}

// ---------------------------------------------------------------------
// Picker population
// ---------------------------------------------------------------------

function populateTranslations() {
  els.translation.innerHTML = TRANSLATIONS.map(
    ([code, label]) => `<option value="${code}">${label}</option>`
  ).join("");
}

function populateBooks() {
  els.book.innerHTML = BOOKS.map(
    ([name]) => `<option value="${name}">${name}</option>`
  ).join("");
}

function populateChapters(book) {
  const n = chaptersIn(book);
  const opts = [];
  for (let c = 1; c <= n; c++) opts.push(`<option value="${c}">${c}</option>`);
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
  try {
    return { ...DEFAULTS, ...JSON.parse(localStorage.getItem(STORE_KEY) || "{}") };
  } catch {
    return { ...DEFAULTS };
  }
}

function saveSelection() {
  localStorage.setItem(
    STORE_KEY,
    JSON.stringify({
      translation: els.translation.value,
      book: els.book.value,
      chapter: Number(els.chapter.value),
    })
  );
}

// ---------------------------------------------------------------------
// Chapter loading
// ---------------------------------------------------------------------

async function loadChapter({ resetStage = true } = {}) {
  const code = els.translation.value;
  const book = els.book.value;
  const chapter = Number(els.chapter.value);
  player.stop();
  els.attribution.textContent = TRANSLATION_ATTRIBUTION[code] || "";
  try {
    passage = await fetchChapter(code, book, chapter);
  } catch (e) {
    passage = null;
    showIdle(e instanceof PassageError ? e.message : "Could not load this chapter.");
    els.versePanel.innerHTML = "";
    els.verse.innerHTML = "";
    return;
  }
  populateVerses(passage.verses);
  renderVersePanel();
  player.load(passage.verses, 0);
  player.voice = pickVoice();
  saveSelection();
  if (resetStage) showIdle();
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
        `<p data-index="${i}"><span class="vnum">${num}</span>${escapeHtml(text)}</p>`
    )
    .join("");
  els.versePanel.querySelectorAll("p").forEach((p) => {
    p.addEventListener("click", () => {
      const i = Number(p.dataset.index);
      player.unlock();
      player.jumpTo(i);
      if (player.state !== "playing") player.play();
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

function showIdle(message) {
  els.idleMessage.style.display = "flex";
  if (message) els.idleMessage.textContent = message;
  else els.idleMessage.textContent = "AV Bible\n\nChoose a passage and press Play";
  els.stageImg.classList.remove("visible");
  els.stageText.classList.remove("visible");
  els.notesBox.textContent = "";
  els.referenceBox.textContent = "";
  els.stageBg.style.background = "#101018";
  els.verseProgress.textContent = " ";
  clearCurrentHighlight();
}

function clearCurrentHighlight() {
  els.versePanel.querySelectorAll("p.current").forEach((p) => p.classList.remove("current"));
}

function renderVerse(index) {
  if (!passage) return;
  const [num, text] = passage.verses[index];
  const ctx = {
    book: passage.book,
    chapter: passage.chapter,
    verse: num,
    translation: passage.translation,
    notes: (passage.notes && passage.notes[index]) || [],
    reference: `${passage.canonical}:${num} (${passage.translation})`,
  };

  els.idleMessage.style.display = "none";

  const { top, bottom } = bookGradient(ctx.book);
  els.stageBg.style.background = `linear-gradient(180deg, ${top}, ${bottom})`;

  const imgPath = stage.findImage(ctx);
  if (imgPath && stage.isText(imgPath)) {
    // A .txt/.rtf visual: show its contents as a centered text panel over
    // the book gradient, styled like the notes box.
    els.stageImg.classList.remove("visible");
    els.stageImg.removeAttribute("src");
    lastImagePath = null;
    const token = ++stageTextToken;
    stage.loadText(imgPath).then((text) => {
      if (token !== stageTextToken) return; // verse changed while loading
      els.stageText.textContent = text;
      els.stageText.classList.toggle("visible", Boolean(text));
    });
  } else if (imgPath) {
    stageTextToken++;
    els.stageText.classList.remove("visible");
    const diagram = stage.isDiagram(imgPath);
    els.stageImg.classList.toggle("diagram", diagram);
    if (imgPath === lastImagePath) {
      // Same file as last verse (e.g. a shared default/book image, or a
      // play-once loop=1 animation) — force the browser to restart the
      // decode from frame 0 rather than silently keeping the old element.
      els.stageImg.src = "";
      els.stageImg.src = `${imgPath}?r=${Date.now()}`;
    } else {
      els.stageImg.src = imgPath;
    }
    els.stageImg.classList.add("visible");
    lastImagePath = imgPath;
  } else {
    stageTextToken++;
    els.stageText.classList.remove("visible");
    els.stageImg.classList.remove("visible");
    els.stageImg.removeAttribute("src");
    lastImagePath = null;
  }

  els.notesBox.textContent =
    els.chkNotes.checked && ctx.notes.length
      ? "Translator-supplied words:  " + ctx.notes.map((n) => `“${n}”`).join("   ")
      : "";
  els.referenceBox.textContent = els.chkReference.checked ? ctx.reference : "";

  const neural = resolveAudio(index) ? " · neural narration" : "";
  els.verseProgress.textContent =
    `Verse ${index + 1} of ${passage.verses.length} — ${ctx.reference}${neural}`;
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

function updatePlayButtons(state) {
  const playing = state === "playing";
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

els.btnPrev.addEventListener("click", () => { player.unlock(); player.prev(); });
els.btnNext.addEventListener("click", () => { player.unlock(); player.next(); });

els.chkNotes.addEventListener("change", () => { if (passage) renderVerse(player.index); });
els.chkReference.addEventListener("change", () => { if (passage) renderVerse(player.index); });
els.rateSlider.addEventListener("input", () => { player.rate = Number(els.rateSlider.value); });

els.translation.addEventListener("change", () => loadChapter());
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

// Landscape lock for mobile fullscreen. Two mechanisms, because no single
// one works everywhere:
//  - Screen Orientation API (Android Chrome, some desktops): a real lock.
//  - CSS rotate fallback (iOS Safari, which supports neither element
//    requestFullscreen on a <div> nor orientation.lock): when the device is
//    held in portrait we rotate the stage 90° so it presents as landscape.
// Re-evaluated on every orientation/resize change while fullscreen.
function applyFullscreenOrientation() {
  if (!isFullscreen()) {
    els.stageWrap.classList.remove("rotate-cw");
    try { screen.orientation?.unlock?.(); } catch {}
    return;
  }
  try { screen.orientation?.lock?.("landscape").catch(() => {}); } catch {}
  // If a real lock (or the physical device) already has us in landscape,
  // don't also rotate. Only rotate coarse-pointer devices still in portrait.
  const portrait = window.matchMedia("(orientation: portrait)").matches;
  const coarse = window.matchMedia("(pointer: coarse)").matches;
  els.stageWrap.classList.toggle("rotate-cw", portrait && coarse);
}

function stageRotated() {
  return els.stageWrap.classList.contains("rotate-cw");
}

function setFullscreen(on) {
  els.stageWrap.classList.toggle("fullscreen", on);
  if (on && els.stageWrap.requestFullscreen) {
    els.stageWrap.requestFullscreen().catch(() => {});
  } else if (!on && document.fullscreenElement) {
    document.exitFullscreen().catch(() => {});
  }
  applyFullscreenOrientation();
  updateFsButton();
  revealControls();
}

// Exiting API fullscreen via a system gesture (Back, swipe) must also
// clear the CSS overlay so both mechanisms stay in sync.
document.addEventListener("fullscreenchange", () => {
  if (!document.fullscreenElement) els.stageWrap.classList.remove("fullscreen");
  applyFullscreenOrientation();
  updateFsButton();
});

// A phone rotated to true landscape (or back) while fullscreen: drop or
// re-apply the CSS rotation to match.
window.addEventListener("resize", () => {
  if (isFullscreen()) applyFullscreenOrientation();
});

fsBtn.addEventListener("click", (e) => {
  e.stopPropagation(); // not a stage tap
  setFullscreen(!isFullscreen());
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
    // When the stage is rotated 90° CW for landscape (see
    // applyFullscreenOrientation), the visual left/right axis is the
    // screen's vertical axis: content-left (prev) sits at the top.
    const firstHalf = stageRotated()
      ? e.clientY - rect.top < rect.height / 2
      : e.clientX - rect.left < rect.width / 2;
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
  if (e.code === "Space") { e.preventDefault(); togglePlay(); }
  else if (e.code === "ArrowRight") player.next();
  else if (e.code === "ArrowLeft") player.prev();
  else if (e.code === "Escape") setFullscreen(false);
});

updateFsButton();

// ---------------------------------------------------------------------
// Boot
// ---------------------------------------------------------------------

async function boot() {
  populateTranslations();
  populateBooks();
  await Promise.all([stage.loadManifest(), loadAudioManifest()]);

  const saved = loadSelection();
  els.translation.value = saved.translation;
  els.book.value = saved.book;
  populateChapters(saved.book);
  els.chapter.value = String(saved.chapter);

  await loadChapter();
}

boot();
