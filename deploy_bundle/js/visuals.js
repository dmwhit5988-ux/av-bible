import { BOOKS } from "./data.js";

// Looks visuals up in visuals/manifest.json (built by build_manifest.py),
// which maps "Book_ch_v" (and, for a whole-chapter graphic, "Book_ch") to a
// list of file records {file, kind, animated}. Every visual is an SVG,
// letterboxed on the stage.

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
    this._illustrated = null;
    try {
      // "no-cache" = always revalidate with the server (cheap 304 when
      // unchanged). Without it, browsers heuristically cache the manifest
      // and returning visitors keep pointing at old files after a visuals
      // deploy.
      const resp = await fetch("/visuals/manifest.json", { cache: "no-cache" });
      const raw = resp.ok ? await resp.json() : {};
      this.manifest = (raw && raw.entries) || {};
    } catch {
      this.manifest = {};
    }
  }

  // Map of book name (with spaces, as in BOOKS) -> Set of chapter numbers
  // that have at least one chapter- or verse-level graphic. Only books with
  // at least one such chapter appear in the map.
  illustratedChapters() {
    if (this._illustrated) return this._illustrated;
    const map = new Map();
    if (this.manifest) {
      const bookByKey = new Map(
        BOOKS.map(([name]) => [name.replace(/ /g, "_"), name])
      );
      for (const key of Object.keys(this.manifest)) {
        const m = /^(.+?)_(\d+)(?:_\d+)?$/.exec(key);
        if (!m) continue;
        const book = bookByKey.get(m[1]);
        if (!book) continue;
        if (!map.has(book)) map.set(book, new Set());
        map.get(book).add(Number(m[2]));
      }
    }
    this._illustrated = map;
    return map;
  }

  // ctx: {book, chapter, verse}
  // Returns the verse's visual (or its chapter's), with a resolved URL:
  //   {url, kind, animated, file} — or null when nothing is drawn for it.
  findVisual(ctx) {
    if (!this.manifest) return null;
    const book = ctx.book.replace(/ /g, "_");
    for (const key of [`${book}_${ctx.chapter}_${ctx.verse}`, `${book}_${ctx.chapter}`]) {
      const records = this.manifest[key] || [];
      const record = records.find((r) => r.file.endsWith(".svg")) || records[0];
      if (record) {
        return {
          url: `/visuals/${record.file}`,
          kind: record.kind || null,
          animated: Boolean(record.animated),
          file: record.file,
        };
      }
    }
    return null;
  }
}
