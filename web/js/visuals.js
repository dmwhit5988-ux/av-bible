// Ports visual_stage.py's _find_image fallback chain using
// visuals/manifest.json (built by build_manifest.py) instead of probing the
// filesystem. Priority per location: verse -> chapter -> book -> default,
// and at each location a translation-suffixed file (e.g. Genesis_5_3.KJV)
// wins over the generic one. Animated formats (webp/gif) are letterboxed
// like diagrams; static photos (png/jpg) are cover-cropped.

// Vector diagrams. Browsers render SVG natively via <img>; they scale to
// any size without pixelation and are letterboxed like the animated
// diagrams. Highest priority: where an SVG exists for a key it is the
// preferred, hand-editable source (see backups/ for the WebP originals).
const VECTOR_EXTS = [".svg"];
const ANIM_EXTS = [".gif", ".webp"];
const PHOTO_EXTS = [".png", ".jpg", ".jpeg"];
// Text files render as an on-stage text panel (styled like the notes box).
// Lowest priority: any real image for the same key wins over the text file.
const TEXT_EXTS = [".txt", ".rtf"];
const EXT_PRIORITY = [...VECTOR_EXTS, ...ANIM_EXTS, ...PHOTO_EXTS, ...TEXT_EXTS];

function extOf(path) {
  const m = /\.[a-z0-9]+$/i.exec(path);
  return m ? m[0].toLowerCase() : "";
}

function pickBestRecord(records) {
  if (!records || records.length === 0) return null;
  const sorted = [...records].sort(
    (a, b) =>
      EXT_PRIORITY.indexOf(extOf(a.file)) - EXT_PRIORITY.indexOf(extOf(b.file))
  );
  return sorted[0];
}

// Normalize a manifest entry to v2's per-file record shape. v1 entries are
// bare path strings; give them the metadata a v2 record would carry so the
// rest of the app never branches on schema version (matters right after a
// deploy, when a returning visitor may still hold the old manifest).
function normalizeRecord(entry) {
  if (typeof entry === "string") {
    const ext = extOf(entry);
    return {
      file: entry,
      kind: PHOTO_EXTS.includes(ext)
        ? "photo"
        : TEXT_EXTS.includes(ext)
          ? "note"
          : "infographic",
      animated: ANIM_EXTS.includes(ext),
    };
  }
  return entry;
}

// Simple deterministic string hash (Python's hash() is randomized per
// process, so there is nothing meaningful to port exactly — this just needs
// to be stable so the same book always gets the same hue).
// Phone-sized screens can opt into ".mobile" visual variants (see
// findImage). "pointer: coarse" catches phones and tablets in either
// orientation; the width clause catches small desktop windows too.
const MOBILE_QUERY =
  typeof window !== "undefined" && window.matchMedia
    ? window.matchMedia("(pointer: coarse), (max-width: 700px)")
    : null;

function isMobileScreen() {
  return Boolean(MOBILE_QUERY && MOBILE_QUERY.matches);
}

function hashBook(book) {
  let h = 0;
  for (let i = 0; i < book.length; i++) {
    h = (h * 31 + book.charCodeAt(i)) | 0;
  }
  return Math.abs(h) % 360;
}

export function bookGradient(book) {
  const hue = hashBook(book);
  return {
    top: `hsl(${hue}, 45%, 16%)`,
    bottom: `hsl(${hue}, 55%, 6%)`,
  };
}

export class VisualStage {
  constructor() {
    this.manifest = null;
  }

  async loadManifest() {
    try {
      // "no-cache" = always revalidate with the server (cheap 304 when
      // unchanged). Without it, browsers heuristically cache the manifest
      // and returning visitors keep pointing at old files after a visuals
      // deploy — e.g. a chapter's .webp that has since been replaced by .svg.
      const resp = await fetch("/visuals/manifest.json", { cache: "no-cache" });
      const raw = resp.ok ? await resp.json() : {};
      // Schema v2 wraps the key map in {version, entries}; v1 IS the key
      // map. Normalize every entry to a list of v2 records up front.
      const entries = raw && raw.version >= 2 ? raw.entries || {} : raw;
      this.manifest = {};
      for (const [key, list] of Object.entries(entries)) {
        this.manifest[key] = (list || []).map(normalizeRecord);
      }
    } catch {
      this.manifest = {};
    }
  }

  // ctx: {book, chapter, verse, translation}
  // Returns the best visual's full record, with resolved URLs:
  //   {url, stillUrl|null, kind, animated, file}
  // stillUrl is the reduced-motion twin (build_stills.py) when one exists.
  findVisual(ctx) {
    if (!this.manifest) return null;
    const book = ctx.book.replace(/ /g, "_");
    const keys = [
      `${book}_${ctx.chapter}_${ctx.verse}`,
      `${book}_${ctx.chapter}`,
      book,
      "default",
    ];
    // Filename suffix priority. On phone-sized screens a ".mobile"
    // variant (e.g. Genesis_5_3.mobile.webp, or Genesis_5_3.KJV.mobile.webp
    // for a translation-specific one) wins over the standard file, so
    // graphics can be re-cut with bigger text just where it matters.
    let suffixes = ctx.translation ? [`.${ctx.translation}`, ""] : [""];
    if (isMobileScreen()) {
      suffixes = [...suffixes.map((s) => `${s}.mobile`), ...suffixes];
    }
    for (const key of keys) {
      for (const suffix of suffixes) {
        const record = pickBestRecord(this.manifest[key + suffix]);
        if (record) {
          return {
            url: `/visuals/${record.file}`,
            stillUrl: record.still ? `/visuals/${record.still}` : null,
            kind: record.kind || null,
            animated: Boolean(record.animated),
            file: record.file,
          };
        }
      }
    }
    return null;
  }

  // Back-compat convenience: just the best file's URL.
  findImage(ctx) {
    const visual = this.findVisual(ctx);
    return visual ? visual.url : null;
  }

  isDiagram(path) {
    const ext = extOf(path);
    return ANIM_EXTS.includes(ext) || VECTOR_EXTS.includes(ext);
  }

  isText(path) {
    return TEXT_EXTS.includes(extOf(path));
  }

  // Fetch and cache the contents of a .txt/.rtf visual, returning plain
  // text ready to display. RTF is reduced to its plain text.
  async loadText(path) {
    if (!this._textCache) this._textCache = new Map();
    if (this._textCache.has(path)) return this._textCache.get(path);
    let text = "";
    try {
      const resp = await fetch(path);
      if (resp.ok) {
        text = await resp.text();
        if (extOf(path) === ".rtf") text = rtfToPlainText(text);
        text = text.trim();
      }
    } catch {
      text = "";
    }
    if (this._textCache.size > 32) this._textCache.clear();
    this._textCache.set(path, text);
    return text;
  }
}

// Minimal RTF -> plain text: drops destination groups (fonttbl, colortbl,
// stylesheet, info, pict...), maps \par/\line/\tab and escaped characters,
// strips remaining control words and braces. Good enough for the simple
// RTF files WordPad/Word produce for plain prose.
function rtfToPlainText(rtf) {
  // Remove groups whose first control word marks a non-text destination.
  const destinations =
    /\{\\(?:\*|fonttbl|colortbl|stylesheet|info|pict|themedata|listtable|listoverridetable|generator)[^{}]*(?:\{[^{}]*\}[^{}]*)*\}/g;
  let s = rtf.replace(destinations, "");
  s = s
    .replace(/\\par[d]?\b\s?/g, "\n")
    .replace(/\\line\b\s?/g, "\n")
    .replace(/\\tab\b\s?/g, "\t")
    .replace(/\\'([0-9a-fA-F]{2})/g, (_, h) =>
      String.fromCharCode(parseInt(h, 16))
    )
    .replace(/\\u(-?\d+)\s?\??/g, (_, n) => {
      let code = parseInt(n, 10);
      if (code < 0) code += 65536;
      return String.fromCharCode(code);
    })
    .replace(/\\([{}\\])/g, "$1") // escaped literals
    .replace(/\\[a-zA-Z]+-?\d*\s?/g, "") // remaining control words
    .replace(/[{}]/g, "");
  return s.replace(/\n{3,}/g, "\n\n").trim();
}
