# Pronunciation

The narration voice is the neural voice `en-US-AndrewNeural` at rate 0 (`tts_engine.HOUSE_VOICE`, `HOUSE_RATE`), and it mispronounces many Bible names. There are two ways to fix a name:

- **Respelling**, for every render. The name is **respelled in the text sent to the voice**. The free edge-tts service escapes its input, so this is the only fix it can carry.
- **IPA**, for Azure renders only. The same voice on Azure takes SSML, so a name can be spoken from its IPA ([IPA through Azure](#ipa-through-azure)).

A word that only one verse needs said differently, such as a heteronym, has its own fix: [one verse's words](#one-verses-words).

In every case, the text on screen never changes. Respellings apply to the pre-rendered MP3s and to Studio playback; IPA applies only to MP3s rendered with an Azure engine and to ▶ IPA, because Studio playback always uses Edge. The browser's Web Speech fallback, used for verses with no MP3, reads the plain WEB text.

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

## One verse's words

Some words are read two ways, so no list-wide fix is right. In Acts 13:2, "Separate Barnabas and Saul for me" is the verb (SEP-uh-rate), but the voice reads the adjective (SEP-rit). Respelling every "separate" would break the adjective elsewhere. So a verse can carry its own words:

- They live in the `verses` section of `pronunciations.json`, keyed by reference: `"Acts 13:2": {"Separate": "Sep-uh-rate"}`.
- The key is the exact text in that verse, whole-word and case-sensitive, like a name. A longer phrase ("Separate Barnabas") tells two readings in one verse apart.
- The value is what the voice reads instead, used as typed, not lowercased. A name inside it is still respelled.
- `pronunciation.for_verse(ref, text)` swaps them in before `respell()` or `ssml()`. `tts_engine.route()` and `synthesize()` call it when they are given `ref`, and every narration path passes it: the Audio tool's renders (`generate_showcase_audio.generate_chapter`), Studio playback, and Video Studio's on-the-fly verses. A changed entry changes the spoken text, so it misses the TTS cache like a changed respelling.
- `pronunciation.save_verse(ref, words)` writes one verse. It re-reads the file first, so names and other verses saved by other tools are kept; `save_names()` keeps the `verses` section in turn.

## IPA through Azure

Azure AI Speech serves the same `en-US-AndrewNeural` as edge-tts, and it accepts SSML. So a name whose `use_ipa` is on can be spoken from its `ipa` with `<phoneme alphabet="ipa" ph="…">`, instead of respelled by trial and error. Azure is metered, so it is used only where a render asks for it.

**Setup.** The key and region come from the environment and are never written to a file. Set them once, then restart the Studio:

```bat
setx AZURE_SPEECH_KEY <your key>
setx AZURE_SPEECH_REGION eastus
```

**The engines** (`tts_engine.ENGINES`), chosen in the Audio tool:

| Engine | Who speaks | Use it |
|---|---|---|
| `edge` | edge-tts for every verse, with respellings. IPA is not used. | The free default. |
| `mixed` | Azure for verses that name someone with `use_ipa`; edge-tts for the rest. | The normal way to use IPA. Only those verses spend characters. |
| `azure` | Azure for every verse. | While edge-tts is down. A verse already in the TTS cache costs nothing. |

The two services give the same audio. One sentence rendered by both on 2026-10-18 matched in length to the sample, in leading and trailing silence and in loudness (waveform correlation 0.998), so a chapter can mix them. Azure never falls back to anything: a verse it refuses is skipped and reported, not shipped without its IPA.

**What Azure is sent.** `pronunciation.ssml(text)` is the Azure counterpart of `respell()`. It is used only for en-US voices (`tts_engine.IPA_LOCALE`), because the converted IPA is in Azure's en-US phone set; with another voice override, names are respelled as on Edge. In what it builds:

- each `use_ipa` name becomes `<phoneme alphabet="ipa" ph="…">Name</phoneme>`;
- a possessive goes inside the tag, with its sound added to the IPA ("Moses's" ends `.ɪz`), because a `'s` left outside is read as "ess";
- every other `override` name is respelled as usual, and the text is XML-escaped.

**Converting the IPA.** `pronunciation.azure_ipa()` rewrites a stored `ipa` into what Azure takes. The stored value is never changed. It fixes two traps, both measured against the live service on 2026-10-18:
- **Unknown symbols fail the whole request** (HTTP 400), so one bad name would cost its verse. The converter maps the list's notation onto Azure's en-US phone set: `r` → `ɹ`, `ɡ` → ASCII `g`, length marks dropped, British vowels to American (`ɒ` → `ɑ`, `ɜːr` → `ɝ`, `ɛər` → `ɛɹ`, `əʊ` → `oʊ`, a bare `e` → `ɛ`; `ɪə` and `ʊə` → `ɪɹ` and `ʊɹ` before an r, at the end or when stressed, but two vowels otherwise, so `/ˈsæmjʊəl/` stays three syllables), `ər` → `ɚ` (`ɝ` when stressed, as Azure's table has it), the Verifier's `ᵻ`, `eː` and `oː` → `ɪ`, `eɪ` and `oʊ`, tie bars and parentheses removed, `n̩` → `ən`. A symbol with no equivalent raises `ValueError`, and that name falls back to its respelling, or to the plain spelling if it has none (`pronunciation.ipa_problem()` says why). A reference holding alternatives ("a / b") is spoken from the first.
- **Stress is honoured only when every syllable is dotted.** Otherwise Azure stresses the syllable *before* the mark: `tɑˈtɑ` and `ˈtɑ.tɑ` came back identical. Most of the list is written `/mɪˈθuː.ʃeɪ.ɛl/`, with no dot before the stress. So the converter splits every name into syllables, at a written `.` where there is one, at a stress mark written before a consonant, and otherwise by the longest legal English onset. It then puts each mark at the start of its syllable: `mɪ.ˈθu.ʃeɪ.ɛl`.

- **British references, American voice.** Besides the vowels above, the converter drops the "y" after t, d, n, s, z, th or l in a stressed or first syllable, as American speech does: `/kəˈtjʊər.ə/` goes as `kə.ˈtʊɹ.ə`, where Azure had read the `tj` as "ch". In an unstressed syllable, or across a syllable break, the "y" stays (`/ˈmæθ.juː/` is still "MATH-yoo").

All 3,125 stored references convert (`test_azure_tts`). Converting doesn't make a reference right: a wrong `ipa` (Coniah's is `/səˈni.əh/`) is spoken exactly as wrong. That is what ▶ IPA is for.

**How well it works.** On 2026-10-18, 87 names were spoken by Azure from their IPA in the Verifier's carriers, and scored the Verifier's way (`ipa_asr.similarity` against the same `ipa`):

| Names | Edge today (stored score) | Azure from IPA |
|---|---|---|
| 50 marked `unfixed` | mean 0.69; none at 0.80 | mean 0.84; 33 at 0.80 or more. 41 better, 2 worse |
| 12 marked `fixed` (respelled by hand) | mean 0.83 | mean 0.86 |
| 10 marked `ok` | mean 0.91 | mean 0.96 |

The score says how closely the audio follows the IPA, not whether the IPA is right, so a name still needs an ear before **Use** is ticked. Some references score well and are wrong (Coniah). Some unstressed syllables are reduced more than a listener might like: Beersheba's first syllable came back as "ber" (0.79, where Edge's plain reading scored 0.93), because its IPA marks no secondary stress.

**Cost.** Azure bills every character inside `<voice>`, markup included. A `<phoneme>` tag adds about 40 characters plus its IPA to each occurrence. The free tier (F0) allows 500,000 characters a month and 20 requests a minute; `azure_tts` paces itself to one request every 3.1 seconds and retries a 429 with backoff. The whole WEB is 3,946,301 characters, so the free tier covers about an eighth of it, which is why `mixed` exists.

**The meter.** Azure has no usage API a Speech key can read, so every billed request is logged to `azure_usage.jsonl` beside `config.json` (`config.AZURE_USAGE_PATH`, ignored). `azure_tts.usage()` sums the last 31 days; whether the free month is a calendar month or a rolling 30 days isn't documented, and a 31-day sum is never lower than either. A request is logged as soon as Azure answers it, since it is billed then even if the audio never arrives. The Audio tool's confirm dialog shows what a render would add. The authority is the Azure portal: the Speech resource's **Metrics**, "Synthesized Characters", aggregated by Sum.

**Errors.** A 400 skips that verse ("refused by Azure"). A bad key (401), a refusal (403), throttling that outlasts the retries (429, which is also what a used-up month looks like) or no network stops the render; it resumes like any other.

## `pronunciations.json`

The file is `{"_readme": …, "names": {…}}`.

**Keys are WEB spellings:** the exact form a name takes in the World English Bible, including its two-word forms (`Beth Zur`, `Baal Meon`). A key that never occurs in the WEB text never matches anything. The 194 entries for spellings WEB doesn't use are kept in `pronunciations_archive.json`, which nothing reads.

| Field | Meaning |
|---|---|
| `say` | The pronunciation, tuned by ear: whatever sounds right when spoken (`HAVih-lah`). Lowercased, it is what the voice is fed when `override` is true. |
| `ipa` | A formal reference pronunciation. The Verifier scores against it. |
| `ref` | The first place the name appears (`Genesis 2:11`). The file is sorted by it. |
| `override` | `true` means respell before synthesis; `false` means speak as spelled. Only this field decides whether `respell()` substitutes. |
| `use_ipa` | `true` means Azure renders speak the name from `ipa`, which wins over `override` there. Edge renders ignore it. It is written only when `true`. |
| `status` | What checking the audio concluded (below). |
| `score` | The agreement measured at that check, 0–1. |
| `ipa_src` | Where `ipa` came from: `isbe` (ISBE 1915), `cmudict`, `wiktionary`, `wikipedia` or `generated`. Absent means none is recorded; `PRONUNCIATION_TODO.md` labels it "curated". |

**Statuses**, with counts on 2026-10-17 (3,137 names):

| Status | Meaning | Names |
|---|---|---|
| `ok` | Checked; the plain spelling reads correctly | 1,442 |
| `fixed` | Checked; an override (or, on Azure, the IPA) is in place and works | 809 |
| `unfixed` | Checked; the plain spelling is wrong and no respelling has worked yet | 569 |
| `unsure` | Checked only against a `generated` reference, so a disagreement may be the reference's fault. It needs an ear, not another sweep. | 162 |
| `suggested` | A better spelling is known but not applied, because the plain reading was close. Decide by ear. | 155 |
| absent | Never checked. This is not the same as `ok`. | 0 |

No current tool assigns `unsure`. The Pronunciation tool lists those names under its "Unsure (guessed IPA)" filter.

**Reference sources:** `isbe` 975, `cmudict` 232, `generated` 224, `wiktionary` 62, `wikipedia` 13. The other 1,631 entries have no `ipa_src`.

The file can also hold `verses`, the words single verses say differently ([One verse's words](#one-verses-words)).

**Writing the file.** Every write of the names goes through `pronunciation.save_names(names, base)`, and every write of a verse through `pronunciation.save_verse(ref, words)`:
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
- **▶ IPA** (or Enter in the IPA box) has Azure say the name from the IPA as typed, so an edit can be heard before it is saved. If it is wrong, correct the IPA rather than respelling. An edited IPA is saved as curated (its `ipa_src` is dropped).
- Tick **Use** (beside ▶ IPA) to turn `use_ipa` on. The tick is refused when Azure couldn't take the IPA as written.
- **✓ Fine** records that the plain spelling is right, and clears both ticks.
- Filters show unchecked, fine, overridden, suggested, still-wrong and unsure names, names spoken from IPA, or names not in the list yet.
- Previews use the house voice and rate, so what you hear is what will be rendered.
- ▶ IPA is the only preview that costs anything: about 40 characters plus the IPA, once (replays come from the TTS cache). The bottom line shows the Azure meter. Without the key, ▶ IPA is greyed out.
- Names are keyed by spelling, so tuning "Nahor" in Genesis 11 tunes it everywhere.
- **Verse words…** opens a window for the words one verse needs said differently. Pick the verse, type the exact **Words** from it and what to **Say** instead, then press **▶ Verse** to hear the whole verse the way Edge will render it. **Save verse** writes it straight away, apart from the main **Save**. It refuses words that aren't in the verse as typed, capitals included. **✕** clears a row, and saving a verse with no rows removes its entry.

### Verifier (`pronunciation_check.py`, `ipa_asr.py`)

**Opening it.** In the Studio, press **Verifier** in the Author group. It works across the whole list, not one chapter, as a separate process, one copy at a time. To run it on its own:

```
.venv/Scripts/python.exe pronunciation_check.py
```

**Requirements.** It needs the optional packages in `requirements.txt` (`torch transformers scipy`), and soundfile, which `requirements.txt` installs anyway. On first use it downloads the phoneme model `facebook/wav2vec2-lv-60-espeak-cv-ft` (about 1.2 GB).

**For each name it:**
1. builds the exact text the pipeline would speak: the lowercased `say` when `override` is true, otherwise the name;
2. synthesizes it in the house voice, inside carrier sentences (`ipa_asr.CARRIERS`), because a name spoken alone gets clipped;
3. transcribes the audio to IPA by ear (`ipa_asr.transcribe`) and cuts the carrier words back off;
4. scores the result against `ipa` (`ipa_asr.similarity`, after `fold()` puts both notations on one coarse alphabet).

**Reading the scores.** A score ranks suspicion; it is not a verdict. A perfectly said name often scores about 0.8, so read the ordering rather than the number. The bands are `OK_AT = 0.80` and `WARN_AT = 0.55`.

**Saving.**
- On save, each name measured in this session gets a verdict:
  - with an override or `use_ipa`, `fixed`. The Verifier measures the Edge reading, which an Azure render of a `use_ipa` name doesn't use, so it can't demote one;
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
   - **otherwise:** `fixed` if the name already has an override or `use_ipa` (a name with `use_ipa` is never given a suggestion), `ok` at 0.80 or above, and `unfixed` below that.
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

A changed `say`, `override`, `ipa` or `use_ipa` makes every published MP3 of a verse containing that name stale. A verse's own words make only that verse stale.

1. **Fix and save** in the Pronunciation tool, or let `isbe_sweep.py` adopt a respelling.
2. **Render the chapters that contain the name again** in the Audio tool (**Audio** in the Studio's Produce group). Choose the book and chapter range and press **Render**; leave **Overwrite** unticked. The render finds the verses whose MP3 no longer matches today's spoken text (`generate_showcase_audio.is_current`), re-renders just those and skips the rest. The confirm dialog says how many it found. For a name fixed by IPA, choose the engine **Azure for verses with IPA names**; the confirm dialog shows the Azure characters it will use.
3. **If the chapter is 1 Chronicles 1–9 or Matthew 1, re-run its generator** (`generate_1chronicles_tree_svg.py` or `generate_matthew1_svg.py`). Their cameras are timed from the MP3 lengths in `web/audio/` (`svg_chronicles_world.AUDIO_DIR`).
4. **Publish.** It commits `pronunciations.json` along with the MP3s, so the list in git matches the audio it rendered.

Staleness is judged by comparing bytes with the TTS cache (`cache/audio/tts/`), so if the cache is cleared, every verse looks stale. The confirm dialog shows that before anything is synthesized. A whole-site report of stale verses, the stale-narration check in the planned Studio lint, is on the [roadmap](../ROADMAP.md).

Order the work so each chapter is re-rendered once: batch the fixes for a chapter first. Clear the names of a new chapter before its audio is first rendered.
