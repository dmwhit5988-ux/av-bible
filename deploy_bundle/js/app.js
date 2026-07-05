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

function updatePlayButtons(state) {
  els.btnPlay.textContent = state === "playing" ? "⏸ Pause" : "▶ Play";
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

// Tap-to-toggle fullscreen: a CSS overlay (not the Fullscreen API) so it
// works on iOS Safari, which refuses requestFullscreen on plain <div>s.
els.stage.addEventListener("click", () => {
  els.stageWrap.classList.toggle("fullscreen");
});

document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "SELECT" || e.target.tagName === "INPUT") return;
  if (e.code === "Space") { e.preventDefault(); togglePlay(); }
  else if (e.code === "ArrowRight") player.next();
  else if (e.code === "ArrowLeft") player.prev();
  else if (e.code === "Escape") els.stageWrap.classList.remove("fullscreen");
});

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
