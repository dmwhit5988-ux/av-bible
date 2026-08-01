# Pronunciation to-do — 1 Chronicles 2

Names from 1 Chronicles 2 that the Pronunciation Verifier (`python pronunciation_check.py`) could **not** settle automatically. 38 other names in the chapter were fixed and are already live in `pronunciations.json`; the rest of the chapter needs nothing.

**How to read this.** "Voice says now" is what the neural voice actually produces for the plain scripture spelling, transcribed from the audio. The score is agreement with the reference IPA on a 0-1 scale, where a correctly-said name typically lands around 0.80 — the transcriber has its own error rate, so treat these as a ranking, not a verdict. Two caveats worth keeping in mind: the reference IPA itself was never independently verified, so where it is wrong the score is measuring the wrong target; and the final call belongs to your ear, via the play buttons in the Pronunciation Studio.

Useful tricks found while fixing the rest of the chapter:

- **`gh` forces a hard g** — Regem needed `ree-ghem`; `ree-gem` stayed soft ("REJ-im").
- **Double a consonant so it is not swallowed** — Salma needed `sallmuh`; `sal-muh` dropped the l entirely ("SOW-muh").
- **Caps are cosmetic.** `respell()` feeds the voice `say.lower()`, so stress comes from the letters and hyphens, never from the capitals.

## Improved, but not confirmed (15)

A respelling beat the plain spelling but did not clear 0.80. Worth a listen: the proposal is probably better than what is there now, but it is not proven.

| Name | Reference IPA | Voice says now | Best try | That gives | Score |
| --- | --- | --- | --- | --- | --- |
| **Chelubai** | /kəˈluː.baɪ/ | `kɛləbaɪ` (0.67) | `kuhloobeye` | `kʌləbaɪ` | 0.83 |
| **Eleasah** | /ˌɛl.iˈeɪ.sə/ | `ᵻlisɐ` (0.67) | `ehleeaysuh` | `eɪlieɪsə` | 0.83 |
| **Hareph** | /ˈhɛər.ɛf/ | `hɛɹɪf` (0.67) | `hairr-ef` | `hɛɹiɛf` | 0.83 |
| **Abijah** | /əˈbaɪ.dʒə/ | `ɐbidʒɚ` (0.67) | `uhbeyejuh` | `ɐbaɪdʒu` | 0.80 |
| **Jerahmeel** | /dʒəˈrɑː.mi.əl/ | `dʒɜɹmi` (0.62) | `juh-rah-mee-el` | `dʒɚɹɑmiɛl` | 0.78 |
| **Shimeathites** | /ˈʃɪm.i.ə.θaɪts/ | `ʃɑmæθaɪts` (0.62) | `shim-ee-uh-theyets` | `ʃɪmiəθeɪɪts` | 0.78 |
| **Shua** | /ˈʃuː.ə/ | `ʃwɑ` (0.33) | `shooa` | `ʃuɚ` | 0.75 |
| **Achar** | /ˈeɪ.kɑːr/ | `ɐtʃɑɹ` (0.50) | `ay-kahr` | `aɪkɑɹ` | 0.75 |
| **Maaz** | /ˈmeɪ.æz/ | `mɑɹz` (0.50) | `mayaz` | `maɪæz` | 0.75 |
| **Attai** | /ˈæt.aɪ/ | `ɐtaɪt` (0.50) | `at-y` | `ætwaɪ` | 0.75 |
| **Korah** | /ˈkɔːr.ə/ | `toʊɹɐ` (0.50) | `kawra` | `koʊɹɐ` | 0.75 |
| **Zur** | /zɜːr/ | `zu` (0.33) | `zerr` | `zeɪɚ` | 0.75 |
| **Shaaph** | /ˈʃeɪ.æf/ | `ʃɑf` (0.50) | `shay-af` | `ʃeɪɛf` | 0.75 |
| **Abihail** | /ˌæb.ɪˈheɪ.ɪl/ | `eɪbəheɪl` (0.57) | `abihhayihl` | `æbiheɪəl` | 0.71 |
| **Madmannah** | /mædˈmæn.ə/ | `mɛdmɛnɑ` (0.57) | `mad-man-uh` | `mædmɛnɑ` | 0.71 |

<details><summary>Spellings already tried (so you need not repeat them)</summary>

- **Chelubai** — `kuhloobeye` 0.83, `kuh-loo-by` 0.83, `kuh-loo-beye` 0.67, `ka-loo-beye` 0.67, `kaloobeye` 0.67
- **Eleasah** — `ehleeaysuh` 0.83, `el-ee-ay-suh` 0.50, `eleeaysuh` 0.50, `ehl-ee-ay-suh` 0.44, `ehl-i-ay-suh` 0.25
- **Hareph** — `hairr-ef` 0.83, `hairref` 0.83, `hairrehf` 0.67, `hairr-ehf` 0.62
- **Abijah** — `uhbeyejuh` 0.80, `uh-by-juh` 0.80, `uh-beye-juh` 0.50, `a-beye-juh` 0.33, `abeyejuh` 0.33
- **Jerahmeel** — `juh-rah-mee-el` 0.78, `juh-rah-me-el` 0.78, `juh-rah-mee-uhl` 0.67, `ja-rah-mee-uhl` 0.67, `juh-rah-mi-uhl` 0.67, `jarahmeeuhl` 0.62, `jer-ah-mee-el` 0.62, `jrah-mee-el` 0.62, `juhrahmeeuhl` 0.38
- **Shimeathites** — `shim-ee-uh-theyets` 0.78, `shihm-ee-uh-theyets` 0.50, `shihmeeuhtheyets` 0.50, `shihm-i-uh-theyets` 0.50, `shimeeuhtheyets` 0.38
- **Shua** — `shooa` 0.75, `shoouh` 0.67, `shoo-uh` 0.50, `shoo-a` 0.25
- **Achar** — `ay-kahr` 0.75, `aykahr` 0.50
  - "ch" is read soft. ay-kahr fixes the consonant but shifts the vowel to "eye".
- **Maaz** — `mayaz` 0.75, `may-aaz` 0.75, `mayaaz` 0.75, `may-az` 0.50
- **Attai** — `at-y` 0.75, `at-eye` 0.67, `aateye` 0.67, `ateye` 0.50, `aat-eye` 0.40
  - A /t/ from the carrier word bleeds in; the score here is less reliable than most.
- **Korah** — `kawra` 0.75, `kawr-uh` 0.60, `kawruh` 0.60, `kawr-a` 0.50
  - Bare spelling is heard with a /t/ onset ("TOH-ruh"); kawra fixes that but rounds the vowel.
- **Zur** — `zerr` 0.75
  - Short name, so the vowel is hard to pin -- "zoo" bare, "ZAY-er" respelled.
- **Shaaph** — `shay-af` 0.75, `shayaf` 0.75, `shay-aaf` 0.75, `shayaaf` 0.75
- **Abihail** — `abihhayihl` 0.71, `aabihhayihl` 0.62, `ab-i-hay-ihl` 0.57, `ab-ih-hay-ihl` 0.38, `aab-ih-hay-ihl` 0.29
- **Madmannah** — `mad-man-uh` 0.71, `madmanuh` 0.71, `maad-man-uh` 0.71, `maadmanuh` 0.71, `mad-maan-uh` 0.57

</details>

## Nothing worked (8)

The plain spelling is wrong and no respelling tried improved on it. These need a human ear, and possibly a different approach than respelling.

| Name | Reference IPA | Voice says now | Best try | That gives | Score |
| --- | --- | --- | --- | --- | --- |
| **Calcol** | /ˈkæl.kɒl/ | `kaʊkɔl` (0.67) | `kal-kahl` | `keɪoʊlkɑl` | 0.71 |
| **Bunah** | /ˈbjuː.nə/ | `binə` (0.60) | `byoonuh` | `baɪjʊnu` | 0.67 |
| **Jearim** | /ˈdʒiː.ə.rɪm/ | `dʒɪɹəm` (0.50) | `jee-uh-rihm` | `dʒeɪɹɪm` | 0.67 |
| **Oren** | /ˈɔːr.ɛn/ | `ɔɹɹɪn` (0.60) | `awrehn` | `ɚɹɛn` | 0.60 |
| **Ephlal** | /ˈɛf.læl/ | `ɛfəl` (0.60) | `eflal` | `ɛfəl` | 0.60 |
| **Tappuah** | /təˈpjuː.ə/ | `tæpuɐ` (0.67) | `tuh-pyoo-uh` | `tʌpaɪwʌt` | 0.57 |
| **Er** | /ɜːr/ | `eɪ` (0.00) | `urr` | `ɜ` | 0.50 |
| **Kiriath** | /ˈkɪr.i.æθ/ | `kɪɹθ` (0.67) | `kihreeath` | `kɚɹiθ` | 0.50 |

<details><summary>Spellings already tried (so you need not repeat them)</summary>

- **Calcol** — `kal-kahl` 0.71, `kal-call` 0.71, `kaalkol` 0.67, `kahl-kol` 0.67, `kal-kol` 0.57, `kal-kol` 0.57, `cal-col` 0.50, `kalkol` 0.33, `kaal-kol` 0.17
  - First syllable turns into a diphthong ("KAY-ol-kol").
- **Bunah** — `byoonuh` 0.67, `byoona` 0.67, `byoo-nuh` 0.60, `bew-nuh` 0.60, `bue-nuh` 0.60, `b-you-nuh` 0.60, `byoo-na` 0.40, `byoo-nah` 0.40
  - The /bj/ onset is unstable -- either "BEE-nuh" or "by-YOO-nuh".
- **Jearim** — `jee-uh-rihm` 0.67, `jeeuhrihm` 0.67, `jee-a-rihm` 0.67, `jee-uh-rim` 0.67, `jee-uh-rim` 0.67, `jeeuh-rim` 0.67, `jee-a-rim` 0.67, `jeearihm` 0.50, `jee-uh-reem` 0.50
  - Two front vowels merge; "JIR-um" or "JAY-rim", never "JEE-uh-rim".
- **Oren** — `awrehn` 0.60, `awren` 0.60, `or-en` 0.60, `awr-ehn` 0.50, `oh-ren` 0.50, `or-ren` 0.50, `awr-ren` 0.50, `awr-en` 0.40
  - Comes out "or-RIN" with an intrusive r; spelling variants all landed the same.
- **Ephlal** — `eflal` 0.60, `ehflal` 0.40, `ef-lal` 0.40, `ef-lal` 0.40, `ef-lall` 0.40, `ehf-lal` 0.29, `ehf-laal` 0.29, `eff-lahl` 0.29, `eff-lal` 0.29
  - Final /l/ is dropped -- comes out "EF-uhl". Doubling it did not help.
- **Tappuah** — `tuh-pyoo-uh` 0.57, `tuhpyoouh` 0.50, `ta-pyoo-uh` 0.50, `tapyoouh` 0.50, `tuh-pyoo-a` 0.50, `ta-poo-uh` 0.50, `tuh-poo-ah` 0.50, `tap-poo-uh` 0.43, `ta-pooh-uh` 0.38
  - Plain spelling already beats every respelling tried; leave it alone.
- **Er** — `urr` 0.50, `uhr` 0.50, `ur` 0.25, `err-r` 0.25, `err` 0.00
  - Voice reads it as a hesitation sound ("ay"). Nothing tried got past 0.50.
- **Kiriath** — `kihreeath` 0.50, `kireeath` 0.50, `kihr-ee-ath` 0.43, `keer-ee-ath` 0.43, `kihr-ee-ath` 0.43, `kir-ee-ath` 0.38, `kir-ee-ath` 0.38, `kir-ry-ath` 0.29, `kihr-i-ath` 0.12
  - Middle syllable collapses -- "KIRTH". The plain spelling is the best so far.

</details>

---

_Generated from a verifier sweep of all 168 names in 1 Chronicles 2 (voice: en-US-AndrewNeural). Regenerate for another chapter by running the Verifier and sorting by Score._
