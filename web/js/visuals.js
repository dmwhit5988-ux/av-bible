// Ports visual_stage.py's _find_image fallback chain using
// visuals/manifest.json (built by build_manifest.py) instead of probing the
// filesystem. Priority per location: verse -> chapter -> book -> default,
// and at each location a translation-suffixed file (e.g. Genesis_5_3.KJV)
// wins over the generic one. Animated formats (webp/gif) are letterboxed
// like diagrams; static photos (png/jpg) are cover-cropped.

const ANIM_EXTS = [".gif", ".webp"];
const PHOTO_EXTS = [".png", ".jpg", ".jpeg"];
const EXT_PRIORITY = [...ANIM_EXTS, ...PHOTO_EXTS];

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
    const suffixes = ctx.translation ? [`.${ctx.translation}`, ""] : [""];
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
}
