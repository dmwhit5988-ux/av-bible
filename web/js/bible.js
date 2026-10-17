// Fetches chapter JSON from bibles/WEB/<Book>_<ch>.json — the on-disk shape
// import_translation.py writes and passages.py reads (book, chapter,
// canonical, verses:[[num,text],...]; the files' notes field is unused).

const BASE = "/bibles/WEB";

const cache = new Map();

export class PassageError extends Error {}

export function safeBookName(book) {
  return book.replace(/ /g, "_");
}

export async function fetchChapter(book, chapter) {
  const key = `${book}|${chapter}`;
  if (cache.has(key)) return cache.get(key);
  const url = `${BASE}/${safeBookName(book)}_${chapter}.json`;
  let resp;
  try {
    resp = await fetch(url);
  } catch (e) {
    throw new PassageError(`Could not load ${book} ${chapter}: ${e.message}`);
  }
  if (!resp.ok) {
    throw new PassageError(`${book} ${chapter} is not available.`);
  }
  const data = await resp.json();
  cache.set(key, data);
  return data;
}
