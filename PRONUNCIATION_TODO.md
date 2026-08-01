# Pronunciation to-do — Genesis 1–11 and 1 Chronicles 2

Names the Pronunciation Verifier (`python pronunciation_check.py`) could **not** settle. Everything else in these chapters either reads correctly as spelled or now has a working override in `pronunciations.json`.

**How to read this.** "Voice says now" is what the neural voice actually produces for the plain scripture spelling, transcribed back from the audio; two readings are shown because each name is measured inside two different carrier sentences and the score is the average of both. A correctly-said name usually lands around 0.85–1.00. Treat the number as a ranking, not a verdict — the final call is your ear, via the play buttons in the Pronunciation Studio.

**One caveat worth repeating:** every score is measured against the reference IPA in `pronunciations.json`. That reference was not independently verified, so where it is wrong the score is faithfully measuring the wrong target.

Spelling tricks that worked elsewhere in these chapters:

- **`gh` forces a hard g** — Regem needed `ree-ghem`; `ree-gem` stayed soft ("REJ-im").
- **Double a consonant so it survives** — `zurr` beat `zur`, `may-azz` beat `may-az`, `shay-aff` beat `shay-af`.
- **`eye`/`y` for a long i** — `geyehon` fixed Gihon, `pyson` fixed Pison.
- **Caps are cosmetic.** `respell()` feeds the voice `say.lower()`, so stress comes from the letters and hyphens, never the capitals.

## Genesis 1–11

### Nothing worked (7)

No respelling tried improved on the plain spelling. Several of these are near-misses on a single vowel and may well be fine in a sentence.

| Name | Reference IPA | Voice says now | Best try | That gives | Score |
| --- | --- | --- | --- | --- | --- |
| **Hul** | /hʌl/ | `hɑl / hoʊ` (0.50) | `huhl` | `hɑl / hoʊ` | 0.50 |
| **Abimael** | /əˈbɪm.eɪ.ɛl/ | `abimɐɛl / abimaɪɛl` (0.57) | `uhbihmayehl` | `ʌbɚmeɪl / ʌbɐmeɪl` | 0.64 |
| **Cush** | /kʌʃ/ | `kʊʃ / kʊʃ` (0.67) | `kuhsh` | `kuʃ / kuʃ` | 0.67 |
| **Ham** | /hæm/ | `heɪm / heɪm` (0.67) | `ham` | `heɪm / heɪm` | 0.67 |
| **Ararat** | /ˈær.ə.ræt/ | `ɛɹɚɹæt / ɛɹæt` (0.67) | `aruhrat` | `ɐɹɚɹæt / ɹuɹæt` | 0.75 |
| **Put** | /pʌt/ | `pʊt / pʊt` (0.67) | `puht` | `put / put` | 0.67 |
| **Zeboim** | /zɪˈboʊ.ɪm/ | `ziboʊm / ziboɪm` (0.75) | `zi-boh-ihm` | `ziboʊim / ziboʊim` | 0.67 |

<details><summary>Spellings already tried</summary>

- **Abimael** — `uhbihmayehl` 0.64, `uh-bihm-ay-ehl` 0.61, `a-bihm-ay-ehl` 0.59, `abihmayehl` 0.57
  - Stress lands on the wrong syllable and the vowel wanders between readings.
- **Ararat** — `aruhrat` 0.75, `ar-uh-rat` 0.50, `aar-uh-rat` 0.42, `aaruhrat` 0.17
  - Extra r-colouring in the middle: "eh-ruh-RAT".
- **Cush** — `kuhsh` 0.67
  - Heard as "kuush" rather than "kush" -- a vowel hair's breadth, probably fine in a sentence.
- **Ham** — `ham` 0.67, `haam` 0.67
  - Heard as "haym". Likely the voice stressing an isolated one-syllable name.
- **Hul** — `huhl` 0.50
  - Comes out "hawl" or even "ho"; a three-letter name gives the voice little to work with.
- **Put** — `puht` 0.67
  - Heard as "puut" (as in "foot") rather than "put".
- **Zeboim** — `zi-boh-ihm` 0.67, `zee-boh-im` 0.62, `zihbohihm` 0.61, `zibohihm` 0.57, `zeh-boh-im` 0.57, `zih-boh-ihm` 0.50, `zeb-oh-im` 0.47
  - Final syllable collapses -- "zee-BOME". Every respelling tried made it worse.

</details>

## 1 Chronicles 2

### Improved, but not confirmed (3)

A respelling beat the plain spelling but did not reach 0.80. Probably better than what is there now, but unproven.

| Name | Reference IPA | Voice says now | Best try | That gives | Score |
| --- | --- | --- | --- | --- | --- |
| **Oren** | /ˈɔːr.ɛn/ | `oʊɹən / wɔɹɹən` (0.55) | `awrehn` | `ɚɹɛn / ɚɹɛn` | 0.75 |
| **Abihail** | /ˌæb.ɪˈheɪ.ɪl/ | `eɪbəheɪl / eɪbəheɪl` (0.57) | `aabihhayihl` | `æbiheɪl / æbiheɪl` | 0.71 |
| **Tekoa** | /təˈkoʊ.ə/ | `tikoʊ / tikoʊ` (0.60) | `tee-koh-uh` | `tikoʊwɐ / tikoʊɐ` | 0.73 |

<details><summary>Spellings already tried</summary>

- **Abihail** — `aabihhayihl` 0.71, `abihhayihl` 0.64, `ab-ee-hail` 0.57, `aab-ih-hay-ihl` 0.34, `ab-ih-hay-il` 0.33, `ab-ih-hay-ihl` 0.33, `abi-hay-il` 0.33
  - Four syllables, and the voice keeps reducing it to three.
- **Oren** — `awrehn` 0.75, `awren` 0.75, `awr-ehn` 0.68, `or-en` 0.68, `awr-en` 0.60, `or-ren` 0.55, `oh-ren` 0.50
  - An intrusive w or r appears at the front depending on the sentence.
- **Tekoa** — `tee-koh-uh` 0.73, `tuh-koh-uh` 0.67, `ta-koh-uh` 0.65, `teh-koh-uh` 0.63, `tuhkohuh` 0.50, `tuh-ko-ah` 0.50, `takohuh` 0.38
  - Bare gives "tee-KOH", dropping the final vowel; respellings recover it only partly.

</details>

### Nothing worked (7)

No respelling tried improved on the plain spelling. Several of these are near-misses on a single vowel and may well be fine in a sentence.

| Name | Reference IPA | Voice says now | Best try | That gives | Score |
| --- | --- | --- | --- | --- | --- |
| **Bunah** | /ˈbjuː.nə/ | `binɜ / binɐ` (0.60) | `bew-nuh` | `bunɑ / bunɐ` | 0.70 |
| **Ephlal** | /ˈɛf.læl/ | `ɛfəl / ɛfəl` (0.60) | `efla-al` | `ɛfleɪaʊl / ɛfliaʊ` | 0.63 |
| **Shimeathites** | /ˈʃɪm.i.ə.θaɪts/ | `ʃaɪmæθaɪts / ʃaɪmæθaɪts` (0.62) | `shim-ee-uh-theyets` | `ʃɪmiɐθeɪɪs / ʃɪmθeɪɪts` | 0.58 |
| **Attai** | /ˈæt.aɪ/ | `ɐtaɪ / ɐtaɪ` (0.67) | `at-y` | `ætwaɪ / ætwaɪ` | 0.75 |
| **Kiriath** | /ˈkɪr.i.æθ/ | `kɪɹəθ / kɪɹɪθ` (0.67) | `kihreeath` | `kɚɹiθ / kɚɹiθ` | 0.67 |
| **Korah** | /ˈkɔːr.ə/ | `koʊɹɐ / koʊɹɐ` (0.75) | `kawra` | `koʊɹɐ / koʊɹɐ` | 0.75 |
| **Tappuah** | /təˈpjuː.ə/ | `tæpjuɐ / tæpjuwɐ` (0.77) | `tap-poo-uh` | `tæpuwʌ / tæpuɐ` | 0.58 |

<details><summary>Spellings already tried</summary>

- **Attai** — `at-y` 0.75, `at-eye` 0.67, `ateye` 0.67, `aateye` 0.67, `attai` 0.67, `aat-eye` 0.50, `att-eye` 0.33
  - Bare is close; candidates gain little.
- **Bunah** — `bew-nuh` 0.70, `bue-nuh` 0.70, `byoona` 0.63, `byoo-nuh` 0.55, `buh-noo-uh` 0.40, `byoonuh` 0.30, `byoo-na` 0.30, `byoo-nah` 0.30
  - The /bj/ onset is unstable -- "BEE-nuh" one reading, "byoo-nuh" the next.
- **Ephlal** — `efla-al` 0.63, `eflal` 0.60, `ef-lahl` 0.45, `ehflal` 0.40, `ef-lal` 0.40, `eff-lall` 0.39, `ehf-lal` 0.29
  - Final /l/ is dropped -- "EF-uhl". Doubling it and splitting the syllable both failed.
- **Kiriath** — `kihreeath` 0.67, `kireeath` 0.67, `keer-ee-ath` 0.50, `kirry-ath` 0.47, `kihr-ee-ath` 0.44, `kir-ee-ath` 0.38
  - Middle syllable collapses: "KIR-uth" rather than "KIR-ee-ath".
- **Korah** — `kawra` 0.75, `kawr-uh` 0.62, `kawr-a` 0.62, `kor-uh` 0.62, `korr-uh` 0.62, `koh-ruh` 0.50, `kawruh` 0.38
- **Shimeathites** — `shim-ee-uh-theyets` 0.58, `shihm-ee-uh-theyets` 0.56, `shihmeeuhtheyets` 0.38, `shimeeuhtheyets` 0.38
  - Bare is heard "SHY-math-ites"; respellings shifted the vowel but lost the ending.
- **Tappuah** — `tap-poo-uh` 0.58, `tuh-pyoo-uh` 0.50, `tuhpyoouh` 0.50, `tuh-poo-ah` 0.50, `ta-pyoo-uh` 0.42, `tapyoouh` 0.42, `ta-poo-uh` 0.42

</details>

---

_Generated from verifier sweeps of Genesis 1–11 (WEB + KJV spellings) and 1 Chronicles 2. Voice: en-US-AndrewNeural. 145 of 1589 names in the list now carry an override._
