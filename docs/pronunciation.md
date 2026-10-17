# Pronunciation

The narration voice is the edge-tts neural voice `en-US-AndrewNeural` at rate 0 (`tts_engine.HOUSE_VOICE`, `HOUSE_RATE`), and it mispronounces many Bible names. edge-tts escapes its input, so SSML `<phoneme>` tags can't be used. Instead, the name is **respelled in the text sent to the voice**. The text on screen never changes.

The list applies to the pre-rendered MP3s and to Studio playback. The browser's Web Speech fallback, used for verses with no MP3, reads the plain WEB text.

## How a respelling reaches the audio

- `pronunciation.respell(text)` replaces every whole-word occurrence of a name whose entry has `override: true` with that entry's `say`, lowercased.
  - Matching is whole-word and case-sensitive, so "Ham" never hits "Hamath".
  - The longest names are tried first, so a name that contains another still matches whole.
  - A possessive such as "Methuselah's" still matches.
- `tts_engine.synthesize(text, voice, rate)` calls `respell()` before synthesis. Pronunciation previews pass `apply_respell=False` to speak a string verbatim.
- Synthesized audio is cached in `cache/audio/tts/`. The file name hashes the voice, the rate and the *respelled* text (`tts_engine._cache_file`).
  - A changed respelling misses the cache and is synthesized fresh.
  - Verses whose spoken text didn't change come straight from the cache.
- `pronunciation.load()` reloads the list whenever `pronunciations.json` changes on disk, so a running Studio picks up edits saved by the other tools.

## `pronunciations.json`

The file is `{"_readme": …, "names": {…}}`.

**Keys are WEB spellings:** the exact form a name takes in the World English Bible, including its two-word forms (`Beth Zur`, `Baal Meon`). A key that never occurs in the WEB text never matches anything. The 194 entries for spellings WEB doesn't use are kept in `pronunciations_archive.json`, which nothing reads.

| Field | Meaning |
|---|---|
| `say` | The pronunciation, tuned by ear: whatever sounds right when spoken (`HAVih-lah`). Lowercased, it is what the voice is fed when `override` is true. |
| `ipa` | A formal reference pronunciation. The Verifier scores against it. |
| `ref` | The first place the name appears (`Genesis 2:11`). The file is sorted by it. |
| `override` | `true` means respell before synthesis; `false` means speak as spelled. Only this field decides whether `respell()` substitutes. |
| `status` | What checking the audio concluded (below). |
| `score` | The agreement measured at that check, 0–1. |
| `ipa_src` | Where `ipa` came from: `isbe` (ISBE 1915), `cmudict`, `wiktionary`, `wikipedia` or `generated`. Absent means none is recorded; `PRONUNCIATION_TODO.md` labels it "curated". |

**Statuses**, with counts on 2026-10-17 (3,137 names):

| Status | Meaning | Names |
|---|---|---|
| `ok` | Checked; the plain spelling reads correctly | 1,442 |
| `fixed` | Checked; an override is in place and works | 809 |
| `unfixed` | Checked; the plain spelling is wrong and no respelling has worked yet | 569 |
| `unsure` | Checked only against a `generated` reference, so a disagreement may be the reference's fault. It needs an ear, not another sweep. | 162 |
| `suggested` | A better spelling is known but not applied, because the plain reading was close. Decide by ear. | 155 |
| absent | Never checked. This is not the same as `ok`. | 0 |

No current tool assigns `unsure`. The Pronunciation tool lists those names under its "Unsure (guessed IPA)" filter.

**Reference sources:** `isbe` 975, `cmudict` 232, `generated` 224, `wiktionary` 62, `wikipedia` 13. The other 1,631 entries have no `ipa_src`.

**Writing the file.** Every write goes through `pronunciation.save_names(names, base)`:
- It applies only the names that changed since the caller loaded the file, on top of a fresh read. So the Pronunciation tool and the Verifier, which run as separate processes, don't undo each other's saves.
- It writes a temporary file and swaps it in, sorts by `ref`, rewrites `_readme` from `pronunciation.README`, and rebuilds `PRONUNCIATIONS.md`.
- The merge lock works within one process only. Two processes saving within milliseconds of each other could still lose one edit; a cross-process lock is on the [roadmap](../ROADMAP.md).

## The tools

### Pronunciation (`pronunciation_tool.py`)

**Opening it.** In the Studio, press **Pronunciation** in the Author group. It opens on the shared passage's chapter, as a separate process, one copy at a time. To run it on its own:

```
.venv/Scripts/python.exe pronunciation_tool.py [book] [chapter]
```

**What it does.**
- Lists every proper noun in the chapter (`pronunciation.scan_proper_nouns`).
- **▶ Name** plays the plain spelling as the voice reads it unrespelled.
- Type a **Say it** spelling, then **▶ Say** (or Enter) to hear it. That is what narration uses when **Custom** is ticked.
- Tick **Custom** to turn the override on.
- **✓ Fine** records that the plain spelling is right.
- Filters show unchecked, fine, overridden, suggested, still-wrong and unsure names, or names not in the list yet.
- Previews use the house voice and rate, so what you hear is what will be rendered.
- Names are keyed by spelling, so tuning "Nahor" in Genesis 11 tunes it everywhere.

### Verifier (`pronunciation_check.py`, `ipa_asr.py`)

**Opening it.** In the Studio, press **Verifier** in the Author group. It works across the whole list, not one chapter, as a separate process, one copy at a time. To run it on its own:

```
.venv/Scripts/python.exe pronunciation_check.py
```

**Requirements.** It needs the optional packages in `requirements.txt` (`torch transformers soundfile scipy`). On first use it downloads the phoneme model `facebook/wav2vec2-lv-60-espeak-cv-ft` (about 1.2 GB).

**For each name it:**
1. builds the exact text the pipeline would speak: the lowercased `say` when `override` is true, otherwise the name;
2. synthesizes it in the house voice, inside carrier sentences (`ipa_asr.CARRIERS`), because a name spoken alone gets clipped;
3. transcribes the audio to IPA by ear (`ipa_asr.transcribe`) and cuts the carrier words back off;
4. scores the result against `ipa` (`ipa_asr.similarity`, after `fold()` puts both notations on one coarse alphabet).

**Reading the scores.** A score ranks suspicion; it is not a verdict. A perfectly said name often scores about 0.8, so read the ordering rather than the number. The bands are `OK_AT = 0.80` and `WARN_AT = 0.55`.

**Saving.**
- On save, each name measured in this session gets a verdict:
  - with an override, `fixed`;
  - otherwise `ok` at 0.80 or above;
  - otherwise `unfixed`.
- Nothing else changes automatically. **Use heard IPA** is a manual action for one row.

**Stored results.** Measurements live in `data/ipa_checks.json` (`config.IPA_CHECKS_PATH`). The file is tracked, because rebuilding it means a whole-canon sweep. Each record is keyed by name and holds the spoken text, voice, method, what was heard and the score. A record is measured again when the spoken text or voice changes.

### `isbe_sweep.py`

A headless sweep over the names whose reference comes from ISBE:

1. It measures the plain reading as the Verifier does.
2. If that scores below 0.55 (below 0.80 with `--pass2`) and the name has no override, it tests respelling candidates built from the ISBE syllables in `isbe_harvest.json` (beside the script).
3. It records a verdict:
   - **adopted:** a candidate that scores at least 0.70 and beats the plain reading by 0.10 becomes the `say`, with the override on (`fixed`);
   - **suggested:** a candidate that beats the plain reading by 0.10 but scores lower is stored as the `say` with the override left off (`suggested`);
   - **otherwise:** `fixed` if the name already has an override, `ok` at 0.80 or above, and `unfixed` below that.
4. It stores the measurements in `data/ipa_checks.json` and saves through the same merge.

```
.venv/Scripts/python.exe isbe_sweep.py              # every ISBE-referenced name
.venv/Scripts/python.exe isbe_sweep.py --pass2      # only those marked unfixed, reusing stored measurements
.venv/Scripts/python.exe isbe_sweep.py NAME ...     # just these (ISBE-referenced) names
```

## Generated reports

Both reports sit at the repo root and are untracked and ignored. Never edit them by hand.

| Report | What it is | Rebuild with |
|---|---|---|
| `PRONUNCIATIONS.md` | The whole list as a readable table, with a status count | `.venv/Scripts/python.exe pronunciation.py` (every save rebuilds it too) |
| `PRONUNCIATION_TODO.md` | The work list by status, with what the Verifier heard | `.venv/Scripts/python.exe regen_pronunciation_todo.py`, after a sweep (it only reads `pronunciations.json` and `data/ipa_checks.json`) |

## After a fix

A changed `say` or `override` makes every published MP3 of a verse containing that name stale.

1. **Fix and save** in the Pronunciation tool, or let `isbe_sweep.py` adopt a respelling.
2. **Re-render the chapters that contain the name** in the Audio tool (**Audio** in the Studio's Produce group). Choose the book and chapter range, tick **Overwrite existing files (re-render after a pronunciation or voice change)**, then press **Render**. Unchanged verses come from the TTS cache, so only the changed ones are synthesized.
3. **If the chapter is 1 Chronicles 1–9 or Matthew 1, re-run its generator** (`generate_1chronicles_tree_svg.py` or `generate_matthew1_svg.py`). Their cameras are timed from the MP3 lengths in `web/audio/` (`svg_chronicles_world.AUDIO_DIR`).
4. **Publish.**

Nothing yet reports which published verses a change made stale. The stale-narration check in the planned Studio lint is on the [roadmap](../ROADMAP.md).

Order the work so each chapter is re-rendered once: batch the fixes for a chapter first. Clear the names of a new chapter before its audio is first rendered.
