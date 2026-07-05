// Fetches chapter JSON from bibles/<CODE>/<Book>_<ch>.json — the same
// on-disk shape passages.py writes/reads (book, chapter, canonical,
// translation, verses:[[num,text],...], notes:[[...],...]).
import { TRANSLATIONS } from "./data.js";

const cache = new Map();

export class PassageError extends Error {}

export function safeBookName(book) {
  return book.replace(/ /g, "_");
}

export async function fetchChapter(code, book, chapter) {
  const key = `${code}|${book}|${chapter}`;
  if (cache.has(key)) return cache.get(key);
  const url = `/bibles/${code}/${safeBookName(book)}_${chapter}.json`;
  let resp;
  try {
    resp = await fetch(url);
  } catch (e) {
    throw new PassageError(`Could not load ${book} ${chapter}: ${e.message}`);
  }
  if (!resp.ok) {
    const label = TRANSLATIONS.find(([c]) => c === code)?.[1] || code;
    throw new PassageError(`${book} ${chapter} is not available in ${label}.`);
  }
  const data = await resp.json();
  cache.set(key, data);
  return data;
}
