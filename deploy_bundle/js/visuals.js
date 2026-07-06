// Ports visual_stage.py's _find_image fallback chain using
// visuals/manifest.json (built by build_manifest.py) instead of probing the
// filesystem. Priority per location: verse -> chapter -> book -> default,
// and at each location a translation-suffixed file (e.g. Genesis_5_3.KJV)
// wins over the generic one. Animated formats (webp/gif) are letterboxed
// like diagrams; static photos (png/jpg) are cover-cropped.

const ANIM_EXTS = [".gif", ".webp"];
const PHOTO_EXTS = [".png", ".jpg", ".jpeg"];
// Text files render as an on-stage text panel (styled like the notes box).
// Lowest priority: any real image for the same key wins over the text file.
const TEXT_EXTS = [".txt", ".rtf"];
const EXT_PRIORITY = [...ANIM_EXTS, ...PHOTO_EXTS, ...TEXT_EXTS];

function extOf(path) {
  const m = /\.[a-z0-9]+$/i.exec(path);
  return m ? m[0].toLowerCase() : "";
}

function pickBestFile(paths) {
  if (!paths || paths.length === 0) return null;
  const sorted = [...paths].sort(
    (a, b) => EXT_PRIORITY.indexOf(extOf(a)) - EXT_PRIORITY.indexOf(extOf(b))
  );
  return sorted[0];
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
      const resp = await fetch("/visuals/manifest.json");
      this.manifest = resp.ok ? await resp.json() : {};
    } catch {
      this.manifest = {};
    }
  }

  // ctx: {book, chapter, verse, translation}
  findImage(ctx) {
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
        const entry = this.manifest[key + suffix];
        const path = pickBestFile(entry);
        if (path) return `/visuals/${path}`;
      }
    }
    return null;
  }

  isDiagram(path) {
    return ANIM_EXTS.includes(extOf(path));
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
