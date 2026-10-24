# Credits

This file credits the sources Theoria draws on and records the licence each one
states. It does not decide how any licence applies.

## Scripture: World English Bible

The text is the **World English Bible** (WEB), which is in the public domain. The
copy in `web/bibles/WEB/` comes from eBible.org's USFX edition
(`sources/eng-web.usfx.xml`, which is not tracked), and `import_translation.py`
imports it. The import keeps the
verse text and the footnotes, though the app doesn't use the footnotes. It drops
headings and cross-references.

- **Terms.** The WEB preface says the translation may be copied, distributed and
  recorded freely. It asks two things: to maintain the integrity of God's Word, and
  to reserve the name "World English Bible" for faithful copies of the translation.
- **Where Theoria credits it.** The Studio shows `passages.ATTRIBUTION` ("World English
  Bible — public domain."). Video Studio puts the same line on title cards and in
  descriptions. The web page footer reads "Scripture: World English Bible (public
  domain)".
- **Respellings.** Pronunciation respellings change only what the voice is fed. The
  text shown on screen is never altered.

## Narration voice

The narration MP3s in `web/audio/` are spoken by **Microsoft's `en-US-AndrewNeural`
neural voice**. The [edge-tts](#python-packages) library synthesizes them through
Microsoft Edge's online text-to-speech service (`tts_engine.HOUSE_VOICE`). That
service belongs to Microsoft, and this file draws no conclusion about its terms.
Verses with names spoken from IPA are synthesized by the same voice through the
owner's Azure AI Speech resource (`azure_tts.py`), under that subscription's terms.
Verses without an MP3 are read by the visitor's own browser voice (Web Speech), so no
audio for them ships.

## Pronunciation references

Nearly every entry in `pronunciations.json` has an `ipa` reference, and the Verifier
scores the narration against it. The `ipa_src` field marks where an entry's reference
came from:

| `ipa_src` | Entries | Source | Licence, and the attribution it asks for |
|---|---|---|---|
| `isbe` | 975 | **International Standard Bible Encyclopedia** (1915). The headword respellings were harvested from its online edition at internationalstandardbible.com by the retired `isbe_harvest.py` (in the `pre-cleanup` tag), and this project converted them to IPA. `isbe_harvest.json` keeps each respelling, and each entry's `slug` names its page on that site. | Public domain. It asks for no attribution. The website's own terms aren't recorded here. |
| `cmudict` | 232 | **CMU Pronouncing Dictionary** (CMUdict), Carnegie Mellon University | A BSD-style licence: redistributions must keep its copyright notice, conditions and disclaimer (reproduced below). Its README asks users to acknowledge its origin. |
| `wiktionary` | 62 | **Wiktionary** | CC BY-SA 4.0. Credit the authors, name and link the licence ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)), say whether changes were made, and share adaptations under the same licence. |
| `wikipedia` | 13 | **Wikipedia** | CC BY-SA 4.0, as for Wiktionary. |
| `generated` | 224 | Rule-based guesses made by this project (the retired `name_ipa.py`, kept in the `pre-cleanup` tag) | None: this is the project's own work. |

The Wiktionary and Wikipedia entries don't record the page they came from.

1,631 entries have no `ipa_src`, and 12 of those have no IPA at all.
`regen_pronunciation_todo.py` labels them "curated". Their sources aren't recorded.

The `say` respellings that the voice is fed are this project's own. Some were tuned
by ear in Pronunciation Studio. Others were built by `isbe_sweep.py` from the ISBE
respellings in `isbe_harvest.json` and chosen by the speech model's score (see
[below](#pronunciation-verifier-model)). Another 194 retired entries are kept in
`pronunciations_archive.json`.

<details>
<summary>CMU Pronouncing Dictionary licence notice</summary>

```
Copyright (C) 1993-2015 Carnegie Mellon University. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
   The contents of this file are deemed to be source code.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in
   the documentation and/or other materials provided with the
   distribution.

This work was supported in part by funding from the Defense Advanced
Research Projects Agency, the Office of Naval Research and the National
Science Foundation of the United States of America, and by member
companies of the Carnegie Mellon Sphinx Speech Consortium. We acknowledge
the contributions of many volunteers to the expansion and improvement of
this dictionary.

THIS SOFTWARE IS PROVIDED BY CARNEGIE MELLON UNIVERSITY ``AS IS'' AND
ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CARNEGIE MELLON UNIVERSITY
NOR ITS EMPLOYEES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

</details>

## Pronunciation Verifier model

The Verifier (`pronunciation_check.py`) and `isbe_sweep.py` both transcribe the
rendered audio through `ipa_asr.py`, with the speech-recognition model
**`facebook/wav2vec2-lv-60-espeak-cv-ft`**. `ipa_asr.py` loads the model through the
transformers library, which downloads it from the Hugging Face Hub on first run. The
model is not in the repo. Its licence is not recorded here or in the local model
cache, so check its model card before relying on it.

The model's output reaches the project's data in three ways:

- **Verdicts.** Both tools write their measurements to `data/ipa_checks.json` and set
  the `status` and `score` fields in `pronunciations.json`.
- **Heard IPA.** The Verifier's "Use heard IPA" action copies the model's
  transcription into an entry's `ipa` field. It doesn't set or change `ipa_src`, so
  nothing marks these values as the model's, and an entry that already had an
  `ipa_src` keeps it.
- **Respellings.** For an ISBE name whose plain reading scores poorly, `isbe_sweep.py`
  tries `say` candidates built from the ISBE respelling and keeps the one the model
  scores best. It adopts that one as an override when it scores at least 0.70 and
  beats the plain reading by 0.10. If it beats the plain reading by 0.10 but scores
  lower, it records it as a suggestion.

## Python packages

These are the versions installed in `.venv` on 2026-10-17 (edge-tts on 2026-10-18), with the licences their
package metadata states: `pip show`, or, where `pip show` gives none (edge-tts,
scipy), the licence classifiers and licence files. Their own dependencies carry their
own licences.

| Package | Version | Licence | Used for |
|---|---|---|---|
| edge-tts | 7.3.1 | LGPLv3 (its `srt_composer.py` is MIT) | narration |
| aiohttp | 3.14.1 | Apache-2.0 AND MIT | edge-tts networking; Video Studio's DevTools connection to the browser |
| Pillow | 12.3.0 | MIT-CMU | the generators |
| pywebview | 6.2.1 | BSD 3-Clause | the Studio's embedded WebView2 views |
| torch | 2.13.0 | Apache-2.0 AND Apache-2.0 WITH LLVM-exception AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND MIT | the Verifier and `isbe_sweep.py` (optional) |
| transformers | 5.14.1 | Apache 2.0 | the Verifier and `isbe_sweep.py` (optional) |
| soundfile | 0.14.0 | BSD 3-Clause | the Verifier and `isbe_sweep.py` (optional) |
| scipy | 1.18.0 | BSD | the Verifier and `isbe_sweep.py` (optional) |

**Deploy tooling.** `package.json` pins wrangler 4.107.0, which `package-lock.json`
lists as MIT OR Apache-2.0.

**Video Studio** uses ffmpeg and a locally installed Chrome or Edge. Neither is
included in the repo.

## Map geography

The map lines Theoria draws (coasts, lakes, rivers, roads) are this project's own
drawings. The Acts 13–14 map (`acts_geography.py`) was drawn between anchor points,
each the coordinate of one named place (a town, cape, river mouth or ancient site)
taken as a single fact from **Wikidata**, whose data is CC0, or from **Wikipedia**;
two ancient sites (Comama and Derbe) come from **vici.org**. No line geometry was
copied, traced or sampled from OpenStreetMap or any other map or dataset. The older
maps (`generate_tribal_maps.py`, `generate_acts1518_svg.py`) are hand-encoded from
standard atlas reconstructions.

## Retired Genesis 1 photographs

Genesis 1 once used photographs, which were replaced by SVGs. Their credits are kept
in [docs/archive/genesis1-photo-credits.txt](docs/archive/genesis1-photo-credits.txt).
No current visual uses them.
