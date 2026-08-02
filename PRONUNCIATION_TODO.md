# Pronunciation to-do

Names the Pronunciation Verifier (`python pronunciation_check.py`) could **not** settle, across Genesis 1–11 and all of 1 Chronicles. Everything else in those chapters either reads correctly as spelled or now has a working override in `pronunciations.json`.

**How to read this.** "Voice says now" is what the neural voice actually produces for the plain scripture spelling, transcribed back from the audio; two readings are shown because each name is measured inside two different carrier sentences and the score is the average. A correctly-said name usually lands around 0.85–1.00. Treat the number as a ranking, not a verdict — the final call is your ear, via the play buttons in the Pronunciation Studio.

**⚑ marks a name whose reference IPA I authored** rather than one that was already in your list. Those references were not checked against an external source, so for those rows the target itself may be wrong.

**The same caveat applies everywhere, more mildly:** every score is measured against the reference IPA in `pronunciations.json`, which was never independently verified.

Spelling tricks that worked repeatedly:

- **`gh` forces a hard g** — Regem needed `ree-ghem`; `ree-gem` stayed soft.
- **Double a final consonant so it survives** — `zurr`, `may-azz`, `shay-aff`, `kuhnn`, `shay-uhll`.
- **`eye`/`y` for a long i** — `geyehon`, `pyson`, `omreye`, `meyeshuhm`.
- **Caps are cosmetic.** `respell()` feeds the voice `say.lower()`, so stress comes from the letters and hyphens, never the capitals.

## Suggested, not applied

96 names where a respelling measured better but the plain spelling was already close (0.70–0.79). Nothing was changed for these: at that margin the disagreement is as often an artefact of the transcriber as a fault in the voice — Samuel scored 0.75 only because the recogniser heard a /w/ glide that is not actually there. Listen, and apply any you agree with in the Pronunciation Studio.

| Name | Reference IPA | Voice says now | Suggested say | That gives | Score |
| --- | --- | --- | --- | --- | --- |
| **Jeremoth** | /ˈdʒɛr.ə.mɒθ/ | `dʒɛɹimɑθ / dʒɛɹimɑf` (0.79) | `jehr-a-moth` | `dʒɛɹəmɑθ / dʒɛɹəmɑθ` | 1.00 |
| **Kabzeel** | /ˈkæb.zi.ɛl/ | `kæbzil / kæbzi` (0.79) | `kab-zee-ehll` | `kæbziɛl / kæbziɛl` | 1.00 |
| **Jozabad** | /ˈdʒɒz.ə.bæd/ | `dʒoʊzɐbæd / dʒoʊzəbæt` (0.79) | `joz-uh-bad` | `dʒɑzɐbæd / dʒɑzɐbæd` | 1.00 |
| **Zabdiel** | /ˈzæb.di.ɛl/ | `zæbdil / zæbdɪl` (0.79) | `zab-dee-ehll` | `zæbdiɛl / zæbdiɛl` | 1.00 |
| **Beth-shean** ⚑ | /bɛθˈʃiː.ən/ | `bɛθʃin / bɛðʃin` (0.79) | `behth-shee-an` | `bɛθʃiən / bɛθʃiən` | 1.00 |
| **Jehozabad** | /dʒəˈhɒz.ə.bæd/ | `dʒihoʊzɐbæd / dʒihoʊzəbæd` (0.78) | `jahozuhbad` | `dʒɐhɑzɐbæd / dʒɐhɑzəbæt` | 0.94 |
| **Hizkiah** | /hɪzˈkaɪ.ə/ | `hɪzkiɚ / hɪzkiɐ` (0.77) | `hiz-keye-uh` | `hɪzkaɪɚ / hɪzkaɪɐ` | 0.93 |
| **Ebal** | /ˈiː.bəl/ | `ɛbəl / ɛbəl` (0.75) | `eebal` | `ibəl / ibəl` | 1.00 |
| **Epher** | /ˈiː.fər/ | `ɛfɚ / ɛfɚ` (0.75) | `eefuhr` | `ifɚ / ifɚ` | 1.00 |
| **Ezer** | /ˈiː.zər/ | `ɛzɚ / ɛzɚ` (0.75) | `eezar` | `izɚ / izɚ` | 1.00 |
| **Bela** | /ˈbiː.lə/ | `bɛlɐ / bɛlɐ` (0.75) | `beela` | `bilə / bilɐ` | 1.00 |
| **Beor** | /ˈbiː.ɔːr/ | `biɚ / biɚ` (0.75) | `beeawr` | `bijɔɹ / biɔɹ` | 0.90 |
| **Ithream** | /ˈɪθ.ri.æm/ | `ɪθɹim / ɪfɹim` (0.75) | `ith-ree-am` | `ɪθɹiæm / ɪθɹiæm` | 1.00 |
| **Joash** | /ˈdʒoʊ.æʃ/ | `dʒoʊʃ / dʒoʊʃ` (0.75) | `joh-ash` | `dʒoʊæʃ / dʒoʊæʃ` | 1.00 |
| **Shealtiel** | /ʃiˈæl.ti.ɛl/ | `ʃiltiəl / ʃiltil` (0.75) | `shee-al-tee-ehll` | `ʃiɐltioʊl / ʃiæltiɛl` | 0.88 |
| **Malchiram** | /mælˈkaɪ.rəm/ | `mælkɚɹeɪm / mælkɚɹeɪm` (0.75) | `mal-keye-ruhm` | `mælkaɪɹʊm / mælkaɪɹʌm` | 0.94 |
| **Hoshama** | /ˈhɒʃ.ə.mə/ | `haʃəmɐ / haʃmɐ` (0.75) | `hoshuhmuh` | `hɑʃəmɐ / haʃəmɐ` | 0.92 |
| **Rapha** | /ˈreɪ.fə/ | `ɹæfə / ɹæfɐ` (0.75) | `rayfa` | `ɹeɪfɚ / ɹeɪfə` | 0.90 |
| **Ezem** | /ˈiː.zɛm/ | `izəm / izəm` (0.75) | `ee-zehm` | `izæm / izɛm` | 0.88 |
| **Jeshohaiah** | /ˌdʒɛʃ.oʊˈheɪ.jə/ | `dʒɛʃoʊheɪ / dʒeʃoʊheɪɐ` (0.75) | `jehsh-oh-hay-yuh` | `dʒɛʃoʊheɪjɐ / dʒeʃoʊheɪɐ` | 0.88 |
| **Meon** | /ˈmiː.ɒn/ | `min / min` (0.75) | `mee-on` | `miɔn / miɔn` | 1.00 |
| **Jorai** | /ˈdʒɔːr.aɪ/ | `dʒoʊɹaɪ / dʒoʊɹaɪ` (0.75) | `jawr-eye` | `dʒɔɹɹaɪ / dʒɚɹaɪ` | 0.88 |
| **Mahli** | /ˈmɑː.laɪ/ | `mɑli / mɑli` (0.75) | `mahleye` | `mɑlaɪ / mɑlaɪ` | 1.00 |
| **Samuel** | /ˈsæm.jʊ.əl/ | `sæmjuwəl / sæmjuwəl` (0.75) | `samyuuuhl` | `sæmjuəl / sæmjuəl` | 0.86 |
| **Hukok** | /ˈhjuː.kɒk/ | `hukɑk / kukɑk` (0.75) | `hyookok` | `haɪjukɑk / haɪjukɑk` | 0.86 |
| **Jahziel** | /ˈdʒɑː.zi.ɛl/ | `dʒɑzəl / dʒɑziəl` (0.75) | `jah-zee-el` | `dʒɑziɛl / dʒɑziɛl` | 1.00 |
| **Japhlet** | /ˈdʒæf.lɛt/ | `dʒæfwɪt / dʒæflɪt` (0.75) | `jaf-leht` | `dʒæflɛt / dʒæflɛt` | 1.00 |
| **Nohah** | /ˈnoʊ.hə/ | `noʊɐ / noʊɐ` (0.75) | `noh-huh` | `noʊhɜ / noʊhɑ` | 0.88 |
| **Addar** | /ˈæd.ɑːr/ | `ædɚ / æɾɚ` (0.75) | `ad-ahrr` | `æɾɔɹ / ædɑɹ` | 1.00 |
| **Gera** | /ˈɡɪər.ə/ | `ɡɛɹɐ / ɡɛɹɐ` (0.75) | `geerra` | `ɡɪɹə / ɡɪɹɐ` | 1.00 |
| **Shaharaim** | /ˌʃeɪ.həˈreɪ.ɪm/ | `ʃɑhɚɹeɪm / ʃɑhɚɹeɪm` (0.75) | `shay-huh-ray-ihmm` | `ʃeɪhɚɹeɪɪm / ʃeɪhɚɹeɪɪm` | 1.00 |
| **Elpaal** | /ɛlˈpeɪ.əl/ | `hɛlpəl / ɛlpəl` (0.75) | `ehlpayuhl` | `ɐlpeɪəl / ɛlpeɪəl` | 0.92 |
| **Eder** | /ˈiː.dər/ | `ɛdɚ / ɛɾɚ` (0.75) | `ee-duhr` | `idɚ / idɚ` | 1.00 |
| **Eshek** | /ˈiː.ʃɛk/ | `ɐʃɛk / ɪʃɛk` (0.75) | `eeshehk` | `iʃɛk / iʃɛk` | 1.00 |
| **Imri** | /ˈɪm.raɪ/ | `ɪmɹi / ɪmɹi` (0.75) | `ihmreye` | `ɪmɹaɪ / ɪmɹaɪ` | 1.00 |
| **Ahohite** | /əˈhoʊ.haɪt/ | `æhoʊhaɪd / æhoʊhaɪt` (0.75) | `uh-hoh-heyet` | `ɐhoʊhaɪ / ɐhoʊhaɪt` | 0.92 |
| **Ribai** | /ˈraɪ.baɪ/ | `ɹᵻbaɪ / ɹɪbaɪ` (0.75) | `reyebeye` | `ɹaɪbaɪ / ɹaɪbaɪ` | 1.00 |
| **Gaash** | /ˈɡeɪ.æʃ/ | `ɡæʃ / ɡæʃ` (0.75) | `gay-ash` | `ɡeɪæʃ / ɡeɪæʃ` | 1.00 |
| **Ezbai** | /ˈɛz.baɪ/ | `ɪzbaɪ / æzbaɪ` (0.75) | `ehzbeye` | `æzbaɪ / ɛzbaɪ` | 0.88 |
| **Shama** | /ˈʃeɪ.mə/ | `ʃɑmɐ / ʃɑmɐ` (0.75) | `shay-muh` | `ʃeɪmɐ / ʃeɪmɐ` | 1.00 |
| **Ithmah** | /ˈɪθ.mə/ | `ɪfmɐ / ɪfmɐ` (0.75) | `ihthmuh` | `ɪθmɐ / ɪfmɐ` | 0.88 |
| **Tyre** | /taɪər/ | `taɪɚ / taɪ` (0.75) | `teyear` | `taɪɚ / taɪɚ` | 1.00 |
| **Alamoth** | /ˈæl.ə.mɒθ/ | `ɑləmɑf / ɑləmɑθ` (0.75) | `al-uh-moth` | `ælɐmɑθ / æləmɑθ` | 1.00 |
| **Lahmi** | /ˈlɑː.maɪ/ | `lɑmi / lɑmi` (0.75) | `lahmeye` | `lɑmaɪ / lɑmaɪ` | 1.00 |
| **Zina** | /ˈzaɪ.nə/ | `zinɐ / zinɐ` (0.75) | `zeye-nuh` | `zaɪnoʊ / zaɪnɐ` | 0.88 |
| **Jehezkel** | /dʒəˈhɛz.kɛl/ | `dʒəhɛskəl / dʒɐhɛskəl` (0.75) | `juh-hehz-kehl` | `dʒuɛzkɛl / dʒəhɛzkɛl` | 0.88 |
| **Shubael** | /ˈʃuː.beɪ.ɛl/ | `ʃubeɪ / ʃubeɪl` (0.75) | `shoo-bay-el` | `ʃubeɪɛl / ʃubeɪɛl` | 1.00 |
| **Ibri** | /ˈɪb.raɪ/ | `ɪbɹi / ɪbɹi` (0.75) | `ihb-reye` | `ɪbɹaɪ / ɪbɹaɪ` | 1.00 |
| **Ezri** | /ˈɛz.raɪ/ | `ɛzɹi / ɛzɹi` (0.75) | `ehzreye` | `ɛzɹaɪ / ɛzɹaɪ` | 1.00 |
| **Hushai** | /ˈhuː.ʃaɪ/ | `hɑʃaɪ / hʌʃaɪ` (0.75) | `hoo-shy` | `huʃaɪ / puʃaɪ` | 0.88 |
| **Ezar** ⚑ | /ˈiː.zɑːr/ | `izɚ / izɚ` (0.75) | `ee-zahr` | `iizɔɹɹ / izɑɹ` | 1.00 |
| **Ashur** ⚑ | /ˈæʃ.ər/ | `ɑʃɚ / ɑʃɚ` (0.75) | `ash-uhr` | `æʃɚ / æʃɚ` | 1.00 |
| **Ataroth** ⚑ | /ˈæt.ə.rɒθ/ | `æɾɚɹɑf / æɾɚɹɑθ` (0.75) | `atuhroth` | `ætɚɹɑθ / ætɚɹɑθ` | 1.00 |
| **Socho** ⚑ | /ˈsoʊ.koʊ/ | `soʊtʃoʊ / soʊtʃoʊ` (0.75) | `soh-koh` | `soʊkoʊ / soʊkoʊ` | 1.00 |
| **Tilgath-pilneser** ⚑ | /ˌtɪl.ɡæθ.pɪlˈniː.zər/ | `tɪlɡɪθpɪlmɪsɚ / tɪlɡɪθpɪlnəsɚ` (0.75) | `tihlgathpihlneezuhr` | `tɪlɡæfpəlnizɚ / tɪlɡæθpəlnizɚ` | 0.89 |
| **Jeziel** ⚑ | /ˈdʒiː.zi.ɛl/ | `dʒizəl / dʒiziəl` (0.75) | `jee-zee-el` | `dʒiziɛl / dʒiziɛl` | 1.00 |
| **Perez-uzza** ⚑ | /ˌpɛr.ɛzˈʌz.ə/ | `pɚɹɪzʌzɐ / pɚɹɐzʌzɐ` (0.75) | `pehr-ehz-uhz-uh` | `pɛɹeɪzɐzɐ / pɛɹeɪzɐzɐ` | 0.88 |
| **Beth-rapha** ⚑ | /bɛθˈreɪ.fə/ | `vɛθɹæfɚ / bɛθɹæfə` (0.74) | `behth-ray-fuhh` | `bɛθɹeɪfɚ / bɛθɹeɪfəl` | 0.88 |
| **Shimri** | /ˈʃɪm.raɪ/ | `ʃɪmɚɹi / ʃɪmɹi` (0.73) | `shim-reye` | `ʃɪmɹaɪ / ʃɪmɚɹaɪ` | 0.92 |
| **Dalaiah** ⚑ | /dəˈleɪ.ə/ | `dəlaɪɚ / dəlaɪɐ` (0.73) | `duh-lay-uhh` | `dɐleɪɐ / dəleɪɐ` | 1.00 |
| **Mecherathite** | /məˈkɛr.ə.θaɪt/ | `məʃɪɹɪθaɪt / məʃɛɹɪθaɪt` (0.72) | `muh-kehr-uh-theyett` | `mɐkɛɹɐθeɪt / məkɛɹɐθeɪ` | 0.83 |
| **Hazar-shual** ⚑ | /ˌheɪ.zɑːrˈʃuː.əl/ | `hɐzɑɹɹʃu / hɑzɑɹʃul` (0.72) | `hay-zahr-shoo-uhll` | `heɪzɑɹʃuoʊl / heɪzɑɹʃuəl` | 0.94 |
| **Magdiel** | /ˈmæɡ.di.ɛl/ | `mædiəl / mæɡiəl` (0.71) | `mag-dee-ehll` | `mæɡdiɛl / mæɡdiɛl` | 1.00 |
| **Johanan** | /dʒoʊˈheɪ.næn/ | `dʒoʊhɑnən / dʒoʊhɑnən` (0.71) | `joh-hay-nan` | `dʒoʊheɪneɪn / dʒoʊheɪneɪn` | 0.86 |
| **Shelomith** | /ʃəˈloʊ.mɪθ/ | `ʃɛləmɪθ / ʃɛləmɪθ` (0.71) | `shuh-loh-mihth` | `ʃuloʊmɪθ / ʃuloʊmɪθ` | 0.86 |
| **Joshibiah** | /ˌdʒɒʃ.ɪˈbaɪ.ə/ | `dʒɑʃəbiɐ / dʒɑʃəbiɐ` (0.71) | `jahshihbeyeuh` | `dʒɑʃɨbaɪɐ / dʒɑʃᵻbaɪ` | 0.93 |
| **Phinehas** | /ˈfɪn.i.əs/ | `fɪnəhəs / fɪnɐhəs` (0.71) | `fihneeuhs` | `fɪniəs / fɪniəs` | 1.00 |
| **Baaseiah** | /ˌbeɪ.əˈsiː.jə/ | `bəsiɐ / bəsiɐ` (0.71) | `bay-uh-see-yuh` | `beɪɐsiɐ / beɪɐsiɐ` | 0.86 |
| **Jokmeam** | /ˈdʒɒk.mi.æm/ | `dʒɑkmi / dʒɑkmi` (0.71) | `jok-mee-am` | `dʒɑkmieɪm / dʒɑkmieɪm` | 0.86 |
| **Malchiel** | /ˈmæl.ki.ɛl/ | `mælki / mælkəl` (0.71) | `mal-kee-ehll` | `mælkiioʊl / maʊlkiɛl` | 0.86 |
| **Birzaith** | /bərˈzeɪ.ɪθ/ | `bɚzeɪf / bɜzeɪθ` (0.71) | `buhr-zay-ihthh` | `bɚzeɪɪθ / bɚzeɪɪθ` | 1.00 |
| **Shilonites** | /ˈʃaɪ.lə.naɪts/ | `ʃiloʊnaɪts / ʃɪloʊnaɪts` (0.71) | `shyluhneyets` | `ʃɑlənaɪts / ʃaɪlənaɪts` | 0.93 |
| **Ahiezer** | /ˌeɪ.haɪˈiː.zər/ | `ɐhizɚ / ɐhizɚ` (0.71) | `ayhyeezuhr` | `eɪhaɪjizɚ / eɪhaɪizɚ` | 0.94 |
| **Haruphite** | /həˈruː.faɪt/ | `hɛɹəfaɪt / hɛɹəfaɪt` (0.71) | `huhroofeyet` | `hɜɹəfaɪt / hɜɹəfaɪt` | 0.86 |
| **Rehabiah** | /ˌriː.həˈbaɪ.ə/ | `ɹiɐbaɪɚ / ɹioʊbaɪɐ` (0.71) | `reehuhbeyeuh` | `ɹihɐbaɪɐ / ɹihɐbaɪɐ` | 1.00 |
| **Izharites** | /ˈɪz.hɑːr.aɪts/ | `ɪzɚɹaɪts / ɪzɚɹaɪts` (0.71) | `iz-hahr-eyets` | `hɪzhɑɹɹaɪɪts / ɪzhɑɹɹaɪɪts` | 0.83 |
| **Machbenah** ⚑ | /mækˈbiː.nə/ | `mɑtʃbinə / mɑtʃbinɐ` (0.71) | `mak-bee-nuh` | `mækbinoʊ / mækbinɑ` | 0.86 |
| **Jeaterai** ⚑ | /dʒiːˈæt.ə.raɪ/ | `dʒidɚɹaɪ / dʒidɚɹaɪ` (0.71) | `jee-at-uh-reye` | `dʒiædɐɹaɪ / dʒiædɐɹaɪ` | 0.86 |
| **Machbanai** ⚑ | /ˈmæk.bə.naɪ/ | `mɑkbənaɪ / mɑpənaɪ` (0.71) | `makbuhneye` | `mækbənaɪ / mækbənaɪ` | 1.00 |
| **Asuppim** ⚑ | /əˈsʌp.ɪm/ | `ɐsʌpɚm / ɐsʌpɚm` (0.71) | `uh-suhp-ihmm` | `ɐsʌpɪm / ɐsʌpɪm` | 1.00 |
| **Esau** | /ˈiː.sɔː/ | `hisɑ / isaʊ` (0.71) | `ee-saw` | `hiisɑ / isɑ` | 0.88 |
| **Rimmono** | /rɪˈmoʊ.noʊ/ | `ɹᵻmɑnəl / ɹᵻmɑnoʊ` (0.70) | `rihmohnoh` | `ɹɪmənoʊ / ɹɪmənoʊ` | 0.83 |
| **Eldaah** | /ɛlˈdeɪ.ə/ | `ɛldɚ / ɛldə` (0.70) | `el-day-uh` | `ɛldeɪɐ / ɐldeɪɐ` | 0.90 |
| **Eshban** | /ˈɛʃ.bæn/ | `ɛʃbeɪn / ɛʃpeɪn` (0.70) | `ehsh-ban` | `eɪʃbæn / eɪʃbæn` | 0.80 |
| **Adaiah** | /əˈdeɪ.jə/ | `ɐdeɪɚ / ɐdeɪɐ` (0.70) | `uh-day-yuhh` | `ɐdeɪjeɪ / ɐdeɪɐ` | 0.80 |
| **Mashal** | /ˈmeɪ.ʃæl/ | `mɪʃæl / mɪʃɛl` (0.70) | `may-shal` | `meɪʃəl / meɪʃəl` | 0.80 |
| **Bedan** | /ˈbiː.dæn/ | `bɪdeɪn / bᵻdæn` (0.70) | `bee-dan` | `bideɪn / bideɪn` | 0.80 |
| **Ashvath** | /ˈæʃ.væθ/ | `ɑʃvɑθ / aʃvɑθ` (0.70) | `ashvath` | `aʃvɑθ / aʃvɑθ` | 0.80 |
| **Ashbel** | /ˈæʃ.bɛl/ | `æʃbəl / æʃpəl` (0.70) | `ash-bel` | `æʃbɛl / æʃbɛl` | 1.00 |
| **Jakim** | /ˈdʒeɪ.kɪm/ | `dʒækəm / dʒækɪm` (0.70) | `jay-kihm` | `dʒeɪkɪm / dʒeɪkɪm` | 1.00 |
| **Melech** | /ˈmiː.lɛk/ | `mɛlɛk / mɛlɪk` (0.70) | `mee-lehk` | `milɛk / milɛk` | 1.00 |
| **Tarea** | /təˈriː.ə/ | `tɛɹɐ / tɛɹiɐ` (0.70) | `tuh-ree-uh` | `tɚɹioʊ / tɚɹiɐ` | 0.90 |
| **Galal** | /ˈɡeɪ.læl/ | `ɡeɪvəl / ɡeɪləl` (0.70) | `gay-lall` | `ɡeɪloʊl / ɡeɪlɔl` | 0.80 |
| **Tizite** | /ˈtaɪ.zaɪt/ | `təzaɪt / təzaɪd` (0.70) | `teyezeyet` | `taɪzaɪɪ / taɪzaɪ` | 0.80 |
| **Zidon** ⚑ | /ˈzaɪ.dɒn/ | `zaɪdən / zaɪdɪŋ` (0.70) | `zeye-don` | `zaɪdɔn / zaɪdɔn` | 1.00 |
| **Pharez** ⚑ | /ˈfɛər.ɛz/ | `fɛɹəz / fɛɹɪs` (0.70) | `fairr-ehz` | `fɛɹeɪz / fɛɹeɪz` | 0.80 |

## Genesis 1–11

### Nothing worked (8)

No respelling tried improved on the plain spelling. Many are near-misses on a single vowel and may be fine in a sentence.

| Name | Reference IPA | Voice says now | Best try | That gives | Score |
| --- | --- | --- | --- | --- | --- |
| **Hul** | /hʌl/ | `hɑl / hoʊ` (0.50) | `huhl` | `hɑl / hoʊ` | 0.50 |
| **Abimael** | /əˈbɪm.eɪ.ɛl/ | `abimɐɛl / abimaɪɛl` (0.57) | `uhbihmayehl` | `ʌbɚmeɪl / ʌbɐmeɪl` | 0.64 |
| **Tekoa** | /təˈkoʊ.ə/ | `tikoʊ / tikoʊ` (0.60) | `tuh-koh-uh` | `tɐkaʊwɐ / tʌkaʊwɐ` | 0.67 |
| **Cush** | /kʌʃ/ | `kʊʃ / kʊʃ` (0.67) | `kuhsh` | `kuʃ / kuʃ` | 0.67 |
| **Ham** | /hæm/ | `heɪm / heɪm` (0.67) | `ham` | `heɪm / heɪm` | 0.67 |
| **Ararat** | /ˈær.ə.ræt/ | `ɛɹɚɹæt / ɛɹæt` (0.67) | `aruhrat` | `ɐɹɚɹæt / ɹuɹæt` | 0.75 |
| **Put** | /pʌt/ | `pʊt / pʊt` (0.67) | `puht` | `put / put` | 0.67 |
| **Zeboim** | /zɪˈboʊ.ɪm/ | `ziboʊm / ziboɪm` (0.75) | `zi-boh-ihm` | `ziboʊim / ziboʊim` | 0.67 |

## 1 Chronicles 2

### Improved, but not confirmed (2)

A respelling beat the plain spelling but did not reach 0.80. Probably better than what is there now, unproven.

| Name | Reference IPA | Voice says now | Best try | That gives | Score |
| --- | --- | --- | --- | --- | --- |
| **Oren** | /ˈɔːr.ɛn/ | `oʊɹən / wɔɹɹən` (0.55) | `awrehn` | `ɚɹɛn / ɚɹɛn` | 0.75 |
| **Abihail** | /ˌæb.ɪˈheɪ.ɪl/ | `eɪbəheɪl / eɪbəheɪl` (0.57) | `aabihhayihl` | `æbiheɪl / æbiheɪl` | 0.71 |

<details><summary>Spellings already tried</summary>

- **Abihail** — `aabihhayihl` 0.71, `abihhayihl` 0.64, `ab-ee-hail` 0.57, `aab-ih-hay-ihl` 0.34, `ab-ih-hay-il` 0.33, `ab-ih-hay-ihl` 0.33, `abi-hay-il` 0.33
- **Oren** — `awrehn` 0.75, `awren` 0.75, `awr-ehn` 0.68, `or-en` 0.68, `awr-en` 0.60, `or-ren` 0.55, `oh-ren` 0.50

</details>

### Nothing worked (7)

No respelling tried improved on the plain spelling. Many are near-misses on a single vowel and may be fine in a sentence.

| Name | Reference IPA | Voice says now | Best try | That gives | Score |
| --- | --- | --- | --- | --- | --- |
| **Bunah** | /ˈbjuː.nə/ | `binɜ / binɐ` (0.60) | `bew-nuh` | `bunɑ / bunɐ` | 0.70 |
| **Ephlal** | /ˈɛf.læl/ | `ɛfəl / ɛfəl` (0.60) | `efla-al` | `ɛfleɪaʊl / ɛfliaʊ` | 0.63 |
| **Shimeathites** | /ˈʃɪm.i.ə.θaɪts/ | `ʃaɪmæθaɪts / ʃaɪmæθaɪts` (0.62) | `shim-ee-uh-theyets` | `ʃɪmiɐθeɪɪs / ʃɪmθeɪɪts` | 0.58 |
| **Attai** | /ˈæt.aɪ/ | `ɐtaɪ / ɐtaɪ` (0.67) | `at-y` | `ætwaɪ / ætwaɪ` | 0.75 |
| **Kiriath** | /ˈkɪr.i.æθ/ | `kɪɹəθ / kɪɹɪθ` (0.67) | `kihreeath` | `kɚɹiθ / kɚɹiθ` | 0.67 |
| **Korah** | /ˈkɔːr.ə/ | `koʊɹɐ / koʊɹɐ` (0.75) | `kawra` | `koʊɹɐ / koʊɹɐ` | 0.75 |
| **Tappuah** | /təˈpjuː.ə/ | `tæpjuɐ / tæpjuwɐ` (0.77) | `tap-poo-uh` | `tæpuwʌ / tæpuɐ` | 0.58 |

## 1 Chronicles (rest of the book)

### Improved, but not confirmed (80)

A respelling beat the plain spelling but did not reach 0.80. Probably better than what is there now, unproven.

| Name | Reference IPA | Voice says now | Best try | That gives | Score |
| --- | --- | --- | --- | --- | --- |
| **Puah** | /ˈpjuː.ə/ | `pwɑ / pwɑ` (0.25) | `pyoo-uh` | `paɪwʌ / paɪwʌ` | 0.50 |
| **Shallecheth** | /ˈʃæl.ə.kɛθ/ | `ʃəlɛʃɪd / ʃəlɛʃɪt` (0.29) | `shaaluhkehth` | `ʃɑləkɛf / ʃɑləkɛθ` | 0.79 |
| **Bathshua** | /bæθˈʃuː.ə/ | `bætswʌ / vætswɑ` (0.33) | `bath-shoo-uhh` | `bæθʃiwɑ / bæθʃuɐ` | 0.79 |
| **Ain** | /ˈeɪ.ɪn/ | `aɪn / aɪn` (0.33) | `ay-ihn` | `aɪɪn / aɪɪn` | 0.67 |
| **Ahi** | /ˈeɪ.haɪ/ | `aɪ / ɑhi` (0.33) | `ay-heye` | `aɪhaɪ / aɪhaɪ` | 0.67 |
| **Pul** | /pʌl/ | `pu / pu` (0.33) | `puhl` | `pɔl / hɔl` | 0.50 |
| **Jediael** | /dʒəˈdaɪ.eɪ.ɛl/ | `dʒidiəl / dʒiniəl` (0.36) | `ja-deye-ay-ehl` | `dʒɐdaɪeɪtʃɛl / dʒʌdaɪeɪdʒoʊ` | 0.80 |
| **Amal** | /ˈeɪ.mæl/ | `ɐmɔ / ɐmɔl` (0.38) | `aymal` | `eɪmoʊ / eɪməl` | 0.62 |
| **Beri** | /ˈbɪər.aɪ/ | `vɛɹi / bɛɹi` (0.38) | `beerr-eye` | `biɹaɪ / biɹaɪ` | 0.75 |
| **Shephuphan** | /ʃəˈfjuː.fæn/ | `ʃɛpɚfeɪn / ʃɛpəfeɪn` (0.38) | `shuhfyoofan` | `ʃəfiufən / ʃʊfiʊfɪn` | 0.69 |
| **Asiel** | /ˈeɪ.si.ɛl/ | `æziəl / æziəl` (0.40) | `aysiehl` | `eɪsjəl / eɪsɪəl` | 0.60 |
| **Jeiel** | /dʒəˈaɪ.əl/ | `dʒioʊ / dʒiəl` (0.40) | `juh-eye-uhll` | `dʒwaɪoʊl / dʒwaɪəl` | 0.70 |
| **Igeal** ⚑ | /ˈɪɡ.i.əl/ | `aɪdʒioʊ / aɪdʒiəl` (0.40) | `ihgheeuhl` | `aɪɡəl / aɪɡjəl` | 0.60 |
| **Isuah** ⚑ | /ˈɪs.ju.ə/ | `ɪʒwɐ / ɪʒɐ` (0.40) | `is-yoo-uh` | `ɪzjuwɚ / ɪzjuwɐ` | 0.62 |
| **Danites** | /ˈdæn.aɪts/ | `dænitɛz / dænitɛz` (0.43) | `daan-eyets` | `dɑnaɪɪts / dɑnaɪɪts` | 0.67 |
| **Chenaniah** | /ˌkɛn.əˈnaɪ.ə/ | `ʃəneɪniɐ / ʃəneɪniɐ` (0.43) | `kehn-uh-neye-uh` | `kɛnəneɪɑ / keɪnɐneɪɐ` | 0.71 |
| **Giddalti** | /ɡɪˈdæl.taɪ/ | `pɪdɑldi / pɪdɑldi` (0.43) | `gihdalteye` | `ɡaɪdəltaɪ / ɡaɪdəltaɪ` | 0.71 |
| **Jesimiel** | /dʒəˈsɪm.i.ɛl/ | `dʒɛzəmi / dʒɛzəmil` (0.44) | `juh-sim-ee-ehl` | `dʒusɪmieɪtʃɛl / dʒusɪmieɪtʃɛl` | 0.70 |
| **Pas-dammim** ⚑ | /pæsˈdæm.ɪm/ | `pɑdeɪməm / hɑdeɪməm` (0.44) | `pasdamihm` | `pæstəmɪm / pæstɪmɪm` | 0.75 |
| **Baal-hanan** ⚑ | /ˌbeɪ.əlˈheɪ.næn/ | `bɑlənɑn / bɑlənɑn` (0.44) | `bay-uhl-hay-nan` | `beɪjulheɪnæn / beɪjulheɪneɪn` | 0.75 |
| **Jehaleleel** ⚑ | /dʒɪˈhæl.ɪ.liːl/ | `dʒihoʊlioʊ / dʒihoʊlioʊ` (0.44) | `jihhalihleel` | `dʒɐhæləllioʊ / dʒɐhæləlliəl` | 0.68 |
| **Eliada** | /ɪˈlaɪ.ə.də/ | `ɛliɑɹdə / ɛliɑdə` (0.46) | `i-leye-uh-duh` | `aɪleɪɐdʌ / aleɪɐdɐ` | 0.67 |
| **Hori** | /ˈhɔːr.aɪ/ | `hoʊɹi / hoʊɹi` (0.50) | `hawr-eye` | `hoʊɹaɪ / hoʊɹaɪ` | 0.75 |
| **Ahinoam** | /əˈhɪn.oʊ.æm/ | `vɐhaɪnʊm / ɐhaɪnʊm` (0.50) | `uh-hihn-oh-am` | `ɐhɪnoʊəm / ɑhɪnoʊləm` | 0.74 |
| **Igal** | /ˈaɪ.ɡæl/ | `ɐɡɑl / ɪɡɑl` (0.50) | `eyegal` | `aɪɡæ / aɪɡæ` | 0.75 |
| **Naam** | /ˈneɪ.æm/ | `nɑm / nɑm` (0.50) | `nay-am` | `neɪeɪm / neɪeɪm` | 0.75 |
| **Biri** | /ˈbɪr.aɪ/ | `baɪɹi / baɪɹi` (0.50) | `bihr-eye` | `biɹaɪ / biɹaɪ` | 0.75 |
| **Asaiah** | /əˈseɪ.jə/ | `ɐsaɪɚ / ɐsaɪɐ` (0.50) | `uh-say-yuhh` | `ɐseɪjɛ / ɐseɪæ` | 0.70 |
| **Azaz** | /ˈeɪ.zæz/ | `ɐzɑz / ɑzɑz` (0.50) | `ay-zaz` | `aɪzæz / aɪzæz` | 0.75 |
| **Ahimaaz** | /əˈhɪm.eɪ.æz/ | `ɐhɐmɑz / ɑhɐmɑz` (0.50) | `uh-hihm-ay-azz` | `ɐhaɪmaɪæz / ɐhaɪmaɪhæz` | 0.67 |
| **Asaph** | /ˈeɪ.sæf/ | `æzæf / æzæf` (0.50) | `ay-saf` | `aɪsæf / aɪsæf` | 0.75 |
| **Anem** | /ˈeɪ.nɛm/ | `ænəm / ænəm` (0.50) | `aynehm` | `eɪnəm / eɪnəm` | 0.75 |
| **Arad** | /ˈɛər.æd/ | `ɐɹɑd / ɚɹɑd` (0.50) | `airr-ad` | `eɪɹæd / ɪɹæd` | 0.75 |
| **Kore** | /ˈkɔːr.i/ | `koʊɹeɪ / koʊɹeɪ` (0.50) | `kawr-i` | `kɔɹɹaɪ / kɔɹɹaɪ` | 0.75 |
| **Eliphal** | /ɪˈlaɪ.fæl/ | `ɐlɪfəl / ɐlɪfəl` (0.50) | `ileyefal` | `ɪliifəl / ɪliifəl` | 0.67 |
| **Elihu** | /ɪˈlaɪ.hjuː/ | `ɛlɪhu / ɛlɪhu` (0.50) | `ileyehyoo` | `ɪlihu / ɪlihu` | 0.67 |
| **Pelethites** | /ˈpɛl.ə.θaɪts/ | `pɛlɪfaɪdiz / pɛlɪθaɪdiz` (0.50) | `pehl-uh-theyets` | `pɛlɐθeɪɪts / pɛlɐθeɪɪts` | 0.75 |
| **Bukkiah** | /bəˈkaɪ.ə/ | `bukaɪjɑ / bukaɪjɑ` (0.50) | `ba-keye-uh` | `bikaɪə / bieɪkaɪɐ` | 0.73 |
| **Tebaliah** | /ˌtɛb.əˈlaɪ.ə/ | `tibɛlɚ / tibɛlə` (0.50) | `teb-uh-leye-uh` | `tɛbɐleɪoʊ / tɛbəleɪɐ` | 0.79 |
| **Ephratah** ⚑ | /ˈɛf.rə.tɑː/ | `æfɹɪkɐ / ɛfɹᵻtə` (0.50) | `ef-ruh-tah` | `jɛfɹutɑ / jɛfɹutɑ` | 0.71 |
| **Kirjath-jearim** ⚑ | /ˌkɜːr.dʒæθˈdʒiː.ə.rɪm/ | `kɪɹdʒɐdʒɪɹəm / kɪɹdʒɐdʒɪɹəm` (0.50) | `kerr-jath-jee-uh-rihmm` | `kɚdʒæθɚɹɪm / kɜdʒæfjɚɹɪm` | 0.75 |
| **Bath-shua** ⚑ | /bæθˈʃuː.ə/ | `bæfʃwɑ / bæfʃwɑ` (0.50) | `bath-shoo-uhh` | `bæθʃiwɑ / bæθʃuɐ` | 0.79 |
| **Asareel** ⚑ | /əˈsær.i.ɛl/ | `eɪsɚɹi / eɪsɚɹiəl` (0.50) | `uh-sar-ee-ehll` | `ɐsɔɹioʊl / ɐsɑɹɹiɛl` | 0.79 |
| **Hasenuah** ⚑ | /ˌhæs.ɪˈnjuː.ə/ | `hazɐnuwɐ / hɑzənuɐ` (0.50) | `hasihnyoouh` | `hæzɐnju / hæzɪnju` | 0.69 |
| **Hothan** ⚑ | /ˈhoʊ.θæn/ | `hɑfən / hɑθən` (0.50) | `hohthan` | `haʊθən / hoʊθən` | 0.70 |
| **Peulthai** ⚑ | /piːˈʌl.θaɪ/ | `poʊlfaɪ / poʊlfaɪ` (0.50) | `peeuhltheye` | `pilfaɪ / pilfaɪ` | 0.67 |
| **Haniel** ⚑ | /ˈhæn.i.ɛl/ | `hɛnjʊl / hænjoʊəl` (0.54) | `haneeehl` | `həniəl / həniəl` | 0.67 |
| **Jashubilehem** | /dʒəˌʃuː.bɪˈliː.hɛm/ | `dʒæʃəbəlhɪm / dʒæʃəbəlhɪm` (0.55) | `juh-shoo-bi-lee-hehm` | `dʒuʃubaɪlihɛm / dʒuʃubaɪlihɪm` | 0.77 |
| **Aher** | /ˈeɪ.hər/ | `ɑheɪɹ / ɑheɪɚ` (0.55) | `ay-huhr` | `aɪhɚ / aɪhɚ` | 0.75 |
| **Meshelemiah** | /məˌʃɛl.əˈmaɪ.ə/ | `mɛʃəlimiɐ / mɛʃəlimiɐ` (0.56) | `muhshehluhmeyeuh` | `mɐʃɐlɐmiɐ / maʃəlʊmiɐ` | 0.67 |
| **Kirjathaim** ⚑ | /ˌkɜːr.dʒəˈθeɪ.ɪm/ | `kɪdʒəθeɪm / kɪdʒᵻfeɪm` (0.56) | `kerrjuhthayihm` | `kɜɹdʒəθeɪm / kɛdʒəθeɪɐm` | 0.78 |
| **Ramathite** | /ˈreɪ.mə.θaɪt/ | `ɹæmæthaɪt / ɹeɪmæɾhaɪt` (0.56) | `ray-muh-theyett` | `ɹeɪməθeɪt / ɹeɪməθeɪ` | 0.79 |
| **Bezaleel** ⚑ | /bɪˈzæl.i.ɛl/ | `bɛzəlioʊ / bɛzəlliəl` (0.56) | `bizaleeehl` | `bɪzəliəl / vɪzəliəl` | 0.69 |
| **Nethaneel** ⚑ | /nɪˈθæn.i.ɛl/ | `nɛθəniəl / nɛθəmiəll` (0.56) | `nihthaneeehl` | `nɪθəniəll / nɪθəniəl` | 0.75 |
| **Penuel** | /pəˈnjuː.əl/ | `pɛnəl / pɛnəl` (0.57) | `panyoouhl` | `pænjəl / pænjəl` | 0.71 |
| **Perazim** | /pəˈreɪ.zɪm/ | `pɛɹɪzəm / pɛɹɪzəm` (0.57) | `puh-ray-zim` | `puɹeɪzɪm / huɹeɪzɪm` | 0.79 |
| **Gedaliah** | /ˌɡɛd.əˈlaɪ.ə/ | `ɡɐdeɪlɐ / ɡədeɪliɐ` (0.57) | `ged-uh-leye-uh` | `ɡɛɾɐleɪaʊ / ɡɛɾɐleɪɐ` | 0.79 |
| **Jathniel** | /ˈdʒæθ.ni.ɛl/ | `dʒeɪðnil / dʒeɪðnil` (0.57) | `jathneeehl` | `dʒæfniəl / dʒæfniəl` | 0.71 |
| **Peullethai** | /piˈʌl.ə.θaɪ/ | `pulɛθaɪ / pulɛθaɪ` (0.57) | `piuhluhtheye` | `piləθaɪ / pjuləθaɪ` | 0.79 |
| **Shelemiah** | /ˌʃɛl.əˈmaɪ.ə/ | `ʃəlimɪɐ / ʃəlimɪɐ` (0.57) | `shel-uh-meye-uh` | `ʃɛlɐmeɪaʊ / ʃɛlɐmeɪɐ` | 0.79 |
| **Ahuzam** ⚑ | /əˈhjuː.zæm/ | `ɐhoʊzəmm / ɐhoʊzəm` (0.57) | `uhhyoozam` | `ɐhaɪjuzəm / ɐhaɪjuzəm` | 0.75 |
| **Josibiah** ⚑ | /ˌdʒɒs.ɪˈbaɪ.ə/ | `dʒoʊzɪbiɐ / dʒoʊzɪbiɐ` (0.57) | `jahsihbeyeuh` | `dʒɑsibaɪɚ / dʒɑsibaɪ` | 0.73 |
| **Azareel** ⚑ | /əˈzær.i.ɛl/ | `æzɐɹiəl / æzɐɹiəl` (0.57) | `uhzareeehl` | `ʌzɐɹiəl / ʌzɐɹiəl` | 0.71 |
| **Benaiah** | /bəˈneɪ.jə/ | `bənaɪɚ / bənaɪɐ` (0.58) | `banayyuh` | `bəneɪəl / bəneɪɐ` | 0.75 |
| **Aijalon** | /ˈædʒ.ə.lɒn/ | `aɪdʒʊlən / aɪdʒəllən` (0.58) | `aaj-uh-lon` | `eɪdʒeɪɐlɔn / eɪdʒiɐlɔn` | 0.71 |
| **Taanach** | /ˈteɪ.ə.næk/ | `teɪnɪk / tænɪk` (0.58) | `tay-uh-nakk` | `teɪɔnækt / teɪɔnæk` | 0.77 |
| **Shimeam** | /ˈʃɪm.i.æm/ | `ʃaɪmim / ʃaɪmi` (0.58) | `shim-ee-am` | `ʃɪmijeɪm / ʃɪmieɪm` | 0.77 |
| **Jezoar** ⚑ | /dʒɪˈzoʊ.ɑːr/ | `dʒizoʊ / dʒizoɹ` (0.58) | `jih-zoh-ahrr` | `dʒaɪzoʊɑɹɹ / dʒaɪzoʊwɑɹ` | 0.77 |
| **Aliah** | /əˈlaɪ.ə/ | `ɐliɐ / oʊliɐ` (0.62) | `uh-leye-uhh` | `ɐleɪɐ / ɐleɪɐ` | 0.75 |
| **Eglah** | /ˈɛɡ.lə/ | `iɡloʊ / iɡlɐ` (0.62) | `egluh` | `ɛɡlu / ɛɡlʊ` | 0.75 |
| **Ziza** | /ˈzaɪ.zə/ | `zizoʊ / zizə` (0.62) | `zeye-zuh` | `zaɪzu / zaɪzu` | 0.75 |
| **Assir** | /ˈæs.ər/ | `ɐsɜ / ɐsɚ` (0.62) | `aasuhr` | `ɑsɚ / ɑsɚ` | 0.75 |
| **Amzi** | /ˈæm.zaɪ/ | `eɪmzi / æmzi` (0.62) | `am-zeye` | `eɪmzaɪ / eɪmzaɪ` | 0.75 |
| **Shean** | /ˈʃiː.æn/ | `ʃi / ʃin` (0.62) | `shee-an` | `ʃiən / ʃiɪn` | 0.75 |
| **Shiza** | /ˈʃaɪ.zə/ | `ʃizoʊ / ʃizə` (0.62) | `shy-zuh` | `ʃaɪzu / ʃaɪzu` | 0.75 |
| **Caphthorim** ⚑ | /ˈkæf.θɔː.rɪm/ | `kæθɹəm / kæfθɚɹən` (0.62) | `kafthawrihm` | `kæfθoɹɹəm / kæfθoɹm` | 0.75 |
| **Manassites** | /məˈnæs.aɪts/ | `mɑnəssaɪts / mɑdɪssaɪts` (0.64) | `muhnaseyets` | `mɔnəsaɪts / mʌnəsaɪts` | 0.79 |
| **Gath-rimmon** ⚑ | /ɡæθˈrɪm.ɒn/ | `ɡæfɹɚmən / ɡæθɹəmən` (0.65) | `gath-rihm-onn` | `ɡæfɹɚmɑn / ɡæθɹəmɑn` | 0.77 |
| **Husham** | /ˈhjuː.ʃəm/ | `hʌʃəm / hʌʃəm` (0.67) | `hyooshuhm` | `haɪjuʃam / haɪjuʃʌm` | 0.79 |
| **Oholibamah** | /oʊˌhɒl.ɪˈbɑː.mə/ | `oʊhalɐbəmɐ / oʊhaləbʊmɐ` (0.67) | `ohholihbahmuh` | `oʊholʊbɑmɐ / oʊhoʊlɐbɑmɐ` | 0.78 |

<details><summary>Spellings already tried</summary>

- **Aher** — `ay-huhr` 0.75, `ayhuhr` 0.75, `ayhar` 0.75, `ay-huhrr` 0.75, `ay-har` 0.25
- **Ahi** — `ay-heye` 0.67, `ayheye` 0.67, `ay-hy` 0.67, `ayhy` 0.33, `ay-heyee` 0.20
- **Ahimaaz** — `uh-hihm-ay-azz` 0.71, `uh-hihm-ay-az` 0.57, `uhhihmayaz` 0.57, `ahihmayaz` 0.57, `a-hihm-ay-az` 0.43, `uh-him-ay-az` 0.29
- **Ahinoam** — `uh-hihn-oh-am` 0.86, `ahihnoham` 0.86, `uh-hin-oh-am` 0.86, `uh-hihn-oh-amm` 0.86, `a-hihn-oh-am` 0.71, `uhhihnoham` 0.62
- **Ahuzam** — `uhhyoozam` 0.75, `uh-hyoo-zaam` 0.75, `uh-hyoo-zamm` 0.75, `uh-hyoo-zam` 0.71, `a-hyoo-zam` 0.71, `ahyoozam` 0.57
- **Aijalon** — `aaj-uh-lon` 0.71, `aajuhlon` 0.67, `aj-a-lon` 0.67, `aj-uh-lonn` 0.67, `aj-uh-lon` 0.57, `ajuhlon` 0.50
- **Ain** — `ay-ihn` 0.67, `ay-in` 0.67, `ay-ihnn` 0.50, `ayin` 0.33, `ayihn` 0.25
- **Aliah** — `uh-leye-uhh` 0.75, `uh-ly-uh` 0.67, `uh-leye-uh` 0.50, `aleyeuh` 0.50, `uhleyeuh` 0.25, `a-leye-uh` 0.25
- **Amal** — `aymal` 0.50, `ay-maal` 0.50, `aymaal` 0.50, `ay-mall` 0.50, `ay-mal` 0.25
- **Amzi** — `am-zeye` 0.75, `amzeye` 0.75, `aamzeye` 0.75, `aam-zeye` 0.60, `am-zy` 0.50, `am-zeyee` 0.50
- **Anem** — `aynehm` 0.75, `aynem` 0.75, `ay-nehm` 0.50, `ay-nem` 0.50, `ay-nehmm` 0.50
- **Arad** — `airr-ad` 0.75, `airrad` 0.75, `airr-add` 0.75, `airr-aad` 0.60, `airraad` 0.25
- **Asaiah** — `uhsayyuh` 0.80, `uh-say-yuhh` 0.80, `uh-say-yuh` 0.60, `a-say-yuh` 0.60, `asayyuh` 0.60, `uh-say-ya` 0.60
- **Asaph** — `ay-saf` 0.75, `aysaf` 0.75, `ay-saff` 0.75, `ay-saaf` 0.50, `aysaaf` 0.50
- **Asareel** — `uhsareeehl` 0.71, `uh-sar-ee-ehll` 0.71, `uh-sar-ee-ehl` 0.67, `uh-saar-ee-ehl` 0.67, `asareeehl` 0.57, `a-sar-ee-ehl` 0.56
- **Asiel** — `aysiehl` 0.60, `ay-see-ehl` 0.57, `ay-si-ehl` 0.50, `ayseeehl` 0.40, `ay-see-el` 0.40, `ay-see-ehll` 0.40
- **Assir** — `aasuhr` 0.75, `as-uhrr` 0.75, `asuhr` 0.50, `aas-uhr` 0.40, `as-ar` 0.40, `as-uhr` 0.25
- **Azareel** — `uhzareeehl` 0.71, `uh-zar-ee-ehl` 0.67, `uh-zaar-ee-ehl` 0.67, `azareeehl` 0.57, `uh-zar-ee-ehll` 0.57, `a-zar-ee-ehl` 0.56
- **Azaz** — `ay-zaz` 0.75, `ayzaz` 0.75, `ayzaaz` 0.75, `ay-zazz` 0.75, `ay-zaaz` 0.50
- **Baal-hanan** — `bay-uhl-hay-nan` 0.80, `bay-uhl-hay-nann` 0.80, `bay-al-hay-nan` 0.78, `bayalhaynan` 0.78, `bay-uhl-hay-naan` 0.70, `bayuhlhaynan` 0.67
- **Bath-shua** — `bath-shoo-uh` 0.71, `bath-shoo-uhh` 0.57, `bathshoouh` 0.50, `bath-shoo-a` 0.50, `baath-shoo-uh` 0.43, `baathshoouh` 0.33
- **Bathshua** — `bath-shoo-uh` 0.71, `bath-shoo-uhh` 0.57, `bathshoouh` 0.50, `bath-shoo-a` 0.50, `baath-shoo-uh` 0.43, `baathshoouh` 0.33
- **Benaiah** — `banayyuh` 0.67, `buh-nay-yuhh` 0.57, `ba-nay-yuh` 0.50, `buh-nay-yuh` 0.43, `buh-nay-ya` 0.43, `buhnayyuh` 0.33
- **Beri** — `beerr-eye` 0.75, `beerreye` 0.75, `beerr-eyee` 0.75, `beerr-y` 0.60, `beerry` 0.50
- **Bezaleel** — `bizaleeehl` 0.75, `bi-zal-ee-ehl` 0.70, `bih-zal-ee-ehl` 0.50, `bih-zaal-ee-ehl` 0.46, `bihzaleeehl` 0.38, `bih-zal-ee-ehll` 0.25
- **Biri** — `bihr-eye` 0.75, `bihreye` 0.75, `bireye` 0.75, `bihr-eyee` 0.75, `bihr-y` 0.60, `bir-eye` 0.50
- **Bukkiah** — `ba-keye-uh` 0.80, `buh-keye-uh` 0.71, `buh-keye-uhh` 0.71, `buhkeyeuh` 0.60, `buh-ky-uh` 0.56, `bakeyeuh` 0.40
- **Caphthorim** — `kafthawrihm` 0.75, `kaaf-thaw-rihm` 0.75, `kaf-thaw-rihm` 0.62, `kaafthawrihm` 0.62, `kaf-thaw-rim` 0.62, `kaf-thaw-rihmm` 0.62
- **Chenaniah** — `kehn-uh-neye-uh` 0.71, `ken-uh-neye-uh` 0.71, `kehn-a-neye-uh` 0.71, `kenuhneyeuh` 0.57, `kehn-uh-neye-uhh` 0.57, `kehnuhneyeuh` 0.44
- **Danites** — `daan-eyets` 0.67, `dan-eyetss` 0.67, `dan-eyets` 0.50, `daneyets` 0.50, `daaneyets` 0.50, `dan-yts` 0.33
- **Eglah** — `egluh` 0.75, `ehg-la` 0.75, `ehg-luh` 0.50, `ehgluh` 0.50, `ehg-luhh` 0.50, `eg-luh` 0.20
- **Eliada** — `i-leye-uh-duh` 0.67, `ileyeuhduh` 0.50, `ih-leye-uh-duhh` 0.44, `ihleyeuhduh` 0.43, `ih-leye-uh-duh` 0.33, `ih-ly-uh-duh` 0.25
- **Elihu** — `ileyehyoo` 0.67, `i-leye-hyoo` 0.57, `ihleyehyoo` 0.38, `ih-leye-hyoo` 0.14, `ih-leye-hyooo` 0.14, `ih-ly-hyoo` 0.00
- **Eliphal** — `ileyefal` 0.67, `ihleyefal` 0.50, `ih-leye-fall` 0.38, `i-leye-fal` 0.33, `ih-leye-fal` 0.14, `ih-ly-fal` 0.12
- **Ephratah** — `ef-ruh-tah` 0.71, `ehf-ruh-tah` 0.56, `ehf-ruh-tahh` 0.56, `ehf-ra-tah` 0.40, `efruhtah` 0.33, `ehfruhtah` 0.29
- **Gath-rimmon** — `gath-rihm-on` 0.67, `gath-rihm-onn` 0.67, `gaath-rihm-on` 0.62, `gath-rim-on` 0.62, `gathrihmon` 0.50, `gaathrihmon` 0.50
- **Gedaliah** — `ged-uh-leye-uh` 0.71, `gehd-uh-leye-uhh` 0.62, `geduhleyeuh` 0.57, `gehd-a-leye-uh` 0.57, `gehd-uh-leye-uh` 0.50, `gehduhleyeuh` 0.29
- **Giddalti** — `gihdalteye` 0.71, `gih-dal-teye` 0.57, `gidalteye` 0.57, `gih-daal-teye` 0.57, `gih-dal-teyee` 0.44, `gi-dal-teye` 0.38
- **Haniel** — `haneeehl` 0.67, `haaneeehl` 0.67, `han-ee-ehl` 0.62, `haan-ee-ehl` 0.62, `han-i-ehl` 0.62, `han-ee-ehll` 0.33
- **Hasenuah** — `hasihnyoouh` 0.62, `haasihnyoouh` 0.62, `has-ih-nyoo-uh` 0.40, `haas-ih-nyoo-uh` 0.40, `has-i-nyoo-uh` 0.38, `has-ih-nyoo-uhh` 0.12
- **Hori** — `hawr-eye` 0.75, `hawreye` 0.75, `hawr-eyee` 0.75, `hawr-y` 0.60, `hawry` 0.50
- **Hothan** — `hoh-than` 0.60, `hohthan` 0.60, `hoh-thaan` 0.60, `hohthaan` 0.60, `hoh-thann` 0.60
- **Husham** — `hyooshuhm` 0.71, `hyoo-shuhmm` 0.71, `hyoo-shuhm` 0.67, `hyoo-sham` 0.67, `hyoosham` 0.67
- **Igal** — `eye-gal` 0.75, `eyegal` 0.75, `eye-gall` 0.75, `y-gal` 0.60, `ygal` 0.50, `eye-gaal` 0.50
- **Igeal** — `ihgheeuhl` 0.60, `ihg-ee-uhll` 0.60, `ihg-ee-uhl` 0.40, `ihgeeuhl` 0.40, `igeeuhl` 0.20, `ihg-i-uhl` 0.20, `ig-ee-uhl` 0.00, `ihgh-ee-uhl` 0.00
- **Isuah** — `is-yoo-uh` 0.57, `ihsyoouh` 0.40, `isyoouh` 0.40, `ihs-yoo-uh` 0.25, `ihs-yoo-a` 0.12, `ihs-yoo-uhh` 0.12
- **Jashubilehem** — `juh-shoo-bi-lee-hehm` 0.82, `juhshoobihleehehm` 0.73, `jashoobihleehehm` 0.73, `juh-shoo-bih-lee-hehm` 0.61, `ja-shoo-bih-lee-hehm` 0.61, `juh-shoo-bih-lee-hehmm` 0.50
- **Jathniel** — `jathneeehl` 0.71, `jath-nee-ehll` 0.71, `jath-ni-ehl` 0.70, `jath-nee-ehl` 0.67, `jaathneeehl` 0.57, `jaath-nee-ehl` 0.50
- **Jediael** — `ja-deye-ay-ehl` 0.88, `juh-deye-ay-ehl` 0.75, `juhdeyeayehl` 0.71, `juh-dy-ay-ehl` 0.60, `juh-deye-ay-ehll` 0.57, `jadeyeayehl` 0.43
- **Jehaleleel** — `jihhalihleel` 0.67, `ji-hal-ih-leel` 0.60, `jih-hal-ih-leel` 0.50, `jih-haal-ih-leel` 0.50, `jih-hal-ih-leell` 0.50, `jihalihleel` 0.44
- **Jeiel** — `juh-eye-uhll` 0.60, `juh-eye-uhl` 0.40, `ja-eye-uhl` 0.40, `juh-y-uhl` 0.33, `juheyeuhl` 0.20, `jaeyeuhl` 0.20
- **Jesimiel** — `juh-sim-ee-ehl` 0.70, `juhsihmeeehl` 0.62, `jasihmeeehl` 0.62, `juh-sihm-ee-ehl` 0.60, `ja-sihm-ee-ehl` 0.60, `juh-sihm-ee-ehll` 0.38
- **Jezoar** — `jih-zoh-ahrr` 0.83, `jih-zoh-ahr` 0.71, `jihzohahr` 0.71, `ji-zoh-ahr` 0.71, `jizohahr` 0.71
- **Josibiah** — `jahsihbeyeuh` 0.75, `jos-i-beye-uh` 0.71, `jos-ih-beye-uhh` 0.56, `jahs-ih-beye-uh` 0.50, `jos-ih-beye-uh` 0.44, `josihbeyeuh` 0.29
- **Kirjath-jearim** — `kerr-jath-jee-uh-rihmm` 0.83, `kerr-jath-jee-uh-rihm` 0.75, `kerr-jath-jee-a-rihm` 0.75, `kerr-jaath-jee-uh-rihm` 0.67, `kerrjaathjeeuhrihm` 0.58, `kerrjathjeeuhrihm` 0.50
- **Kirjathaim** — `kerrjuhthayihm` 0.89, `kerr-ja-thay-ihm` 0.78, `kerr-juh-thay-im` 0.67, `kerr-juh-thay-ihmm` 0.67, `kerr-juh-thay-ihm` 0.56, `kerrjathayihm` 0.56
- **Kore** — `kawr-ee` 0.75, `kawr-i` 0.75, `kawri` 0.75, `kawr-eee` 0.60, `kawree` 0.50
- **Manassites** — `ma-nas-eyets` 0.75, `muhnaseyets` 0.71, `manaseyets` 0.71, `muh-naas-eyets` 0.67, `muh-nas-eyets` 0.56, `muh-nas-eyetss` 0.50
- **Meshelemiah** — `muhshehluhmeyeuh` 0.78, `muh-shehl-uh-meye-uh` 0.67, `ma-shehl-uh-meye-uh` 0.67, `muh-shel-uh-meye-uh` 0.67, `muh-shehl-uh-meye-uhh` 0.67, `mashehluhmeyeuh` 0.56
- **Naam** — `nay-am` 0.75, `nayam` 0.75, `nay-aam` 0.75, `nay-amm` 0.75, `nayaam` 0.50
- **Nethaneel** — `nihthaneeehl` 0.75, `nithaneeehl` 0.75, `ni-than-ee-ehl` 0.46, `nih-than-ee-ehl` 0.42, `nih-thaan-ee-ehl` 0.39, `nih-than-ee-ehll` 0.25
- **Oholibamah** — `ohholihbahmuh` 0.78, `oh-hahl-ih-bah-muh` 0.70, `ohhahlihbahmuh` 0.67, `oh-hol-i-bah-muh` 0.67, `oh-hol-ih-bah-muh` 0.60, `oh-hol-ih-bah-muhh` 0.55
- **Pas-dammim** — `pasdamihm` 0.75, `paasdamihm` 0.62, `pas-dam-ihmm` 0.62, `pas-dam-ihm` 0.50, `paas-dam-ihm` 0.50, `pas-daam-ihm` 0.50
- **Pelethites** — `pel-uh-theyets` 0.86, `pehl-uh-theyets` 0.75, `pehl-uh-theyetss` 0.75, `pehl-a-theyets` 0.71, `pehluhtheyets` 0.50, `peluhtheyets` 0.50
- **Penuel** — `pa-nyoo-uhl` 0.75, `panyoouhl` 0.71, `puh-nyoo-uhl` 0.43, `puhnyoouhl` 0.43, `puh-nyoo-al` 0.43, `puh-nyoo-uhll` 0.43
- **Perazim** — `puh-ray-zim` 0.86, `parayzihm` 0.78, `puh-ray-zihm` 0.71, `pa-ray-zihm` 0.71, `puh-ray-zihmm` 0.71, `puhrayzihm` 0.67
- **Peullethai** — `piuhluhtheye` 0.86, `pee-uhl-uh-theye` 0.57, `peeuhluhtheye` 0.57, `pee-uhl-a-theye` 0.50, `pee-uhl-uh-theyee` 0.44, `pi-uhl-uh-theye` 0.38
- **Peulthai** — `peeuhltheye` 0.67, `pee-uhl-thy` 0.50, `peeuhlthy` 0.50, `pee-uhl-theye` 0.33, `pee-uhl-theyee` 0.29
- **Puah** — `pyoo-uh` 0.50, `pyooa` 0.50, `pyoouh` 0.25, `pyoo-a` 0.25, `pyoo-uhh` 0.25
- **Pul** — `puhl` 0.67, `puhll` 0.33
- **Ramathite** — `ray-muh-theyett` 0.86, `raymuhtheyet` 0.71, `raymatheyet` 0.71, `ray-muh-theyet` 0.57, `ray-muh-thyt` 0.50, `ray-ma-theyet` 0.43
- **Shallecheth** — `shaaluhkehth` 0.71, `shal-uh-kehth` 0.57, `shaluhkehth` 0.57, `shaal-uh-kehth` 0.57, `shal-a-kehth` 0.57, `shal-uh-kehthh` 0.57
- **Shean** — `shee-an` 0.75, `sheean` 0.75, `shee-aan` 0.75, `sheeaan` 0.75, `shee-ann` 0.75
- **Shelemiah** — `shehl-uh-meye-uh` 0.71, `shel-uh-meye-uh` 0.71, `shehl-a-meye-uh` 0.71, `shehl-uh-meye-uhh` 0.71, `shehluhmeyeuh` 0.50, `sheluhmeyeuh` 0.38
- **Shephuphan** — `shuhfyoofan` 0.75, `shuh-fyoo-fan` 0.62, `shafyoofan` 0.62, `shuh-fyoo-faan` 0.62, `sha-fyoo-fan` 0.50, `shuh-fyoo-fann` 0.50
- **Shimeam** — `shim-ee-am` 0.71, `shihm-ee-am` 0.67, `shihmeeam` 0.67, `shimeeam` 0.67, `shihm-i-am` 0.50, `shihm-ee-amm` 0.50
- **Shiza** — `shy-zuh` 0.75, `shyzuh` 0.75, `sheye-zuh` 0.50, `sheyezuh` 0.50, `sheye-zuhh` 0.50, `sheye-za` 0.40
- **Taanach** — `tay-uh-nakk` 0.71, `tayuhnak` 0.67, `tay-uh-naak` 0.67, `tay-a-nak` 0.62, `tay-uh-nak` 0.50, `tayanak` 0.50
- **Tebaliah** — `teb-uh-leye-uh` 0.71, `tebuhleyeuh` 0.71, `tehb-a-leye-uh` 0.71, `tehb-uh-leye-uhh` 0.71, `tehb-uh-leye-uh` 0.57, `tehbuhleyeuh` 0.57
- **Ziza** — `zeye-zuh` 0.75, `zeyezuh` 0.75, `zyzuh` 0.75, `zeye-zuhh` 0.75, `zeye-za` 0.60, `zy-zuh` 0.50

</details>

### Nothing worked (142)

No respelling tried improved on the plain spelling. Many are near-misses on a single vowel and may be fine in a sentence.

| Name | Reference IPA | Voice says now | Best try | That gives | Score |
| --- | --- | --- | --- | --- | --- |
| **Anetothite** ⚑ | /əˈnɛt.ə.θaɪt/ | `ænɛdɪfaɪd / ɐnɛdɪfaɪd` (0.44) | `uh-neht-uh-theyett` | `ɔnɛtəθeɪəɾ / ɔnɛtaθeɪ` | 0.53 |
| **Bithiah** | /bɪˈθaɪ.ə/ | `ɐfaɪɚ / bəθaɪɐ` (0.50) | `bihtheyeuh` | `bɪθiju / bɪθiu` | 0.55 |
| **Ashan** | /ˈeɪ.ʃæn/ | `æʃən / æʃən` (0.50) | `ay-shan` | `aɪʃɑn / aɪʃɑn` | 0.50 |
| **Huri** | /ˈhjʊər.aɪ/ | `kuɹi / huɹi` (0.50) | `hyoorr-eye` | `haɪɚɹaɪ / haɪɚɹaɪ` | 0.60 |
| **Guni** | /ˈɡjuː.naɪ/ | `ɡəni / ɡʊni` (0.50) | `gyoony` | `dʒaɪjuni / dʒaɪjuni` | 0.50 |
| **Shual** | /ˈʃuː.əl/ | `ʃu / ʃu` (0.50) | `shoo-uhl` | `ʃuju / ʃujul` | 0.55 |
| **Ner** | /nɜːr/ | `noʊ / nə` (0.50) | `nerr` | `neɪ / neɪ` | 0.33 |
| **Jesiah** ⚑ | /dʒɪˈsaɪ.ə/ | `dᵻzaɪɚ / dʒəzaɪɐ` (0.55) | `jih-sy-uh` | `dʒaɪɐswaɪɚ / dʒaɪɐswaɪɐ` | 0.54 |
| **Eliehoenai** | /ɪˌlaɪ.ə.hoʊˈiː.naɪ/ | `ᵻlaɪɾoʊnɐ / ɪlaɪroʊnə` (0.56) | `ileyeuhhoheeneye` | `ɪliuhoʊhini / ɪliuhoʊhini` | 0.60 |
| **Jehudijah** ⚑ | /ˌdʒɛ.hjuːˈdaɪ.dʒə/ | `dʒɪhulədʒɐ / dʒixudədʒɐ` (0.56) | `jeh-hyoo-deye-juh` | `dʒeɪhaɪudaɪdʒu / dʒɐhaɪjoʊdaɪdʒu` | 0.63 |
| **Jaareshiah** | /ˌdʒeɪ.ə.rəˈʃaɪ.ə/ | `dʒɚʃiɐ / dʒɪɹɪʃiɐ` (0.56) | `jay-uh-ruh-sheye-uh` | `dʒeɪɹuʃeɪɐ / dʒeɪɹʃeɪɐ` | 0.62 |
| **Eliashib** | /ɪˈlaɪ.ə.ʃɪb/ | `ɪlʃɪp / ɪliᵻʃɪp` (0.57) | `i-leye-uh-shihb` | `aɪleɪɐʃaɪb / aɪleɪɐʃaɪb` | 0.57 |
| **Mattaniah** | /ˌmæt.əˈnaɪ.ə/ | `məteɪniɐ / məteɪniɐ` (0.57) | `mat-uh-neye-uh` | `mærəneɪɔ / mærəneɪɑ` | 0.57 |
| **Elipheleh** ⚑ | /ɪˈlɪf.ɪ.lɛ/ | `ɐlɪfəllɐ / ɐlɪfəllɐ` (0.57) | `ilihfihleh` | `ɪləfaɪlɐ / ɪləfaɪlɐ` | 0.57 |
| **Anah** | /ˈeɪ.nə/ | `ɛnɚ / ænɐ` (0.58) | `aynuh` | `eɪnʊ / eɪnu` | 0.67 |
| **Eleadah** | /ˌɛl.iˈeɪ.də/ | `ɐlidɚ / ɐlidɐ` (0.58) | `el-ee-ay-duh` | `ɛliɐdɑ / ʌliɐdʌ` | 0.67 |
| **Hanniel** | /ˈhæn.i.ɛl/ | `hɛnjəll / hænjəl` (0.58) | `haneeehl` | `həniəl / həniəl` | 0.67 |
| **Mahalah** ⚑ | /ˈmæh.ə.lə/ | `mɐhæloʊ / mɐhælɐ` (0.58) | `mahuhluh` | `mɐhɔlu / mɐhoʊlu` | 0.50 |
| **Anthothijah** | /ˌæn.θoʊˈθaɪ.dʒə/ | `æntᵻfaɪdʒɚ / æntəfaɪdʒɐ` (0.59) | `an-thoh-thy-juh` | `ændθoʊðaɪdʒu / ændθoʊðaɪdʒu` | 0.67 |
| **Reaiah** | /riˈeɪ.jə/ | `ɹiɐ / ɹiɐ` (0.60) | `ree-ay-yuh` | `ɹiaɪɐ / ɹiaɪɐ` | 0.60 |
| **Hormah** | /ˈhɔːr.mə/ | `hoʊmɐ / humɐ` (0.60) | `hawr-muhh` | `hɔɹmoʊ / hoʊmɐ` | 0.70 |
| **Adiel** | /ˈeɪ.di.ɛl/ | `ɑdioʊl / ɑɾiəl` (0.60) | `aydiehl` | `eɪɾioʊ / eɪdiəl` | 0.70 |
| **Maasai** | /ˈmeɪ.ə.saɪ/ | `mɑsaɪ / mɑsaɪ` (0.60) | `mayuhseye` | `maɪsaɪ / maɪɐsaɪ` | 0.70 |
| **Ishuai** ⚑ | /ˈɪʃ.ju.aɪ/ | `ɪʃuwaɪ / ɪʃuwaɪ` (0.60) | `ihsh-yoo-eye` | `ɪʃuwaɪ / ɪʃiwaɪ` | 0.60 |
| **Mattithiah** | /ˌmæt.ɪˈθaɪ.ə/ | `mædɐfaɪɚ / mædɐθaɪɐ` (0.61) | `matihtheyeuh` | `mɪtɪθiu / mətɪθiu` | 0.57 |
| **Hammolecheth** | /hæˈmɒl.ə.kɛθ/ | `hæməlɛkɪθ / hɛməllɛkɪθ` (0.61) | `ha-mol-uh-kehth` | `hɑmoʊlɐkeɪf / hamoʊlɐkeɪθ` | 0.67 |
| **Hammoleketh** ⚑ | /həˈmɒl.ɪ.kɛθ/ | `hæməlkɛf / hæməlkɛθ` (0.61) | `huhmolihkehth` | `hʌməllaɪkɪθ / hʌmlaɪkɪθ` | 0.67 |
| **Shuthelah** | /ʃuːˈθiː.lə/ | `ʃuθəllʊŋ / ʃɪθəllɐ` (0.62) | `shootheela` | `ʃʊdhilɐ / ʃʊthilɐ` | 0.71 |
| **Anathothite** | /ˈæn.ə.θɒθ.aɪt/ | `ɐnæθəθaɪt / ɐnæθəθaɪt` (0.62) | `an-uh-thoth-eyet` | `ɐnʌθɚvaɪt / ɐnʌθəlfaɪt` | 0.56 |
| **Aram-maacah** | /ˌɛər.əm ˈmeɪ.ə.kə/ | `ɛɹɐmɑkɐ / ɛɹəmɑkɐ` (0.62) | `airr-uhm-may-uh-kuh` | `ɛɹɐmeɪɐku / ɛɹɐmeɪɐlku` | 0.71 |
| **Uzzen-sherah** ⚑ | /ˌʌz.ɛnˈʃɪər.ə/ | `ʌzəntʃeɪɹɐ / ʌzəntʃɛɹɐ` (0.62) | `uhz-ehn-sheerr-uh` | `ʌzɪnʃiɹɑ / ʌzɪnʃiɹɑ` | 0.62 |
| **Caleb-ephratah** ⚑ | /ˌkeɪ.lɛbˈɛf.rə.tɑː/ | `keɪləbæfɹɪtɐ / keɪləbɛfɚtɐ` (0.64) | `kay-lehb-ehf-ruh-tahh` | `keɪlɐbitʃɛfɹutɑ / keɪlɛbitʃɛfɹutɑ` | 0.73 |
| **Aiah** | /eɪˈaɪ.ə/ | `aɪɐ / aɪɐ` (0.67) | `ay-eye-uh` | `aɪaɪɚ / aɪaɪɐ` | 0.50 |
| **Jeshaiah** | /dʒəˈʃeɪ.jə/ | `dəʃeɪɚ / dʒəʃeɪɐ` (0.67) | `ja-shay-yuh` | `dʒɐʃeɪɐ / dʒɑʃeɪɐ` | 0.75 |
| **Shemaiah** | /ʃəˈmeɪ.jə/ | `ʃəmaɪɐ / ʃəmaɪɐ` (0.67) | `shuh-may-yuh` | `ʃumeɪɐ / ʃumeɪɐ` | 0.67 |
| **Seraiah** | /səˈreɪ.jə/ | `sɚɹaɪɐ / sɚɹaɪɐ` (0.67) | `suh-ray-yuh` | `suɹeɪɐ / suɹeɪɐ` | 0.67 |
| **Abdiel** | /ˈæb.di.ɛl/ | `ɐdil / æbdil` (0.67) | `ab-dee-ehll` | `ɐbdiɛl / ʌvdiɛl` | 0.75 |
| **Abihu** | /əˈbaɪ.hjuː/ | `ɐbihʊ / ɐbihu` (0.67) | `uhbeyehyoo` | `ɐbaɪɐhu / ɐbaɪɐhu` | 0.67 |
| **Asriel** | /ˈæs.ri.ɛl/ | `ɪsɹiəl / ɪsɹiəl` (0.67) | `as-ree-ehll` | `æzɹiɛl / æzɹioʊl` | 0.75 |
| **Dor** | /dɔːr/ | `doʊ / dɔɹ` (0.67) | `dawr` | `doʊ / dɔɹ` | 0.67 |
| **Arah** | /ˈeɪ.rə/ | `ɛɹɐ / ɛɹɐ` (0.67) | `ayruh` | `ɛɹi / eɪɹu` | 0.50 |
| **Huram** | /ˈhjʊər.əm/ | `hiɹəm / hɪɹəm` (0.67) | `hyoorr-uhm` | `haɪɹʌm / haɪɚɹʌm` | 0.67 |
| **Zillethai** | /ˈzɪl.ə.θaɪ/ | `zɪlɪfaɪ / zɪlɪfaɪ` (0.67) | `zihl-uh-theye` | `zɪlɐðeɪ / zɪlɐðeɪ` | 0.67 |
| **Beraiah** | /bəˈreɪ.jə/ | `bɚɹaɪɐ / bɚɹaɪɐ` (0.67) | `buh-ray-yuhh` | `bʌtɹeɪjæ / bʌtɹeɪɐ` | 0.69 |
| **Gederathite** | /ɡəˈdɛr.ə.θaɪt/ | `ɡɛɾɚɹɪθaɪt / ɡɛɾɚɹɪθaɪt` (0.67) | `guhdehruhtheyet` | `ɡʊdɚɹʌθiət / ɡʊdɚɹʌθiət` | 0.60 |
| **Tou** | /ˈtoʊ.uː/ | `tu / tu` (0.67) | `toh-ooo` | `toʊoʊ / toʊaʊ` | 0.67 |
| **Manahethites** ⚑ | /ˈmæn.ə.hɛθ.aɪts/ | `mɛnᵻhæfaɪts / mɛnəhəθaɪts` (0.67) | `man-a-hehth-eyets` | `mɛnɐheɪθaɪts / mɛnɐheɪθaɪɪts` | 0.74 |
| **Masrekah** | /ˈmæs.rə.kə/ | `mɪsɹikɚ / mɪsɹikɐ` (0.67) | `mas-ruh-kuh` | `mɑsɹuku / mɑsɹuku` | 0.57 |
| **Shebuel** | /ʃɪˈbjuː.ɛl/ | `ʃɚbjuəl / ʃəbjuəl` (0.67) | `shih-byoo-el` | `ʃibaɪwɛl / ʃibaɪwɛl` | 0.57 |
| **Massa** | /ˈmæs.ə/ | `mɑsɚ / mɑsə` (0.68) | `mas-uh` | `mɑsə / mɑsə` | 0.75 |
| **Geba** | /ˈɡiː.bə/ | `ɡeɪbɚ / ɡeɪbɐ` (0.68) | `geebuh` | `ɡibu / ɡibu` | 0.75 |
| **Hazelelponi** ⚑ | /ˌhæz.ɪˈlɛl.poʊ.naɪ/ | `hæzɐləlpoʊni / hæzələpoʊni` (0.68) | `haz-i-lehl-poh-neye` | `hæzaɪloʊlpoʊneɪ / hɐzaɪloʊlpoʊneɪ` | 0.68 |
| **Jashubi-lehem** ⚑ | /dʒəˌʃuː.bɪˈliː.hɛm/ | `dəʃubliəm / dʒəʃʊbiliəm` (0.68) | `juh-shoo-bi-lee-hehm` | `dʒuʃubaɪlihɛm / dʒuʃubaɪlihɪm` | 0.77 |
| **Jeduthun** | /dʒəˈdjuː.θən/ | `dʒəduθɪn / dəduθɪn` (0.69) | `ja-dyoo-thuhn` | `dʒɐdaɪɐθɔn / dʒədaɪɐθʌn` | 0.69 |
| **Pasdammim** | /pæsˈdæm.ɪm/ | `pæsdeɪməm / pæsteɪməm` (0.69) | `pasdamihm` | `pæstəmɪm / pæstɪmɪm` | 0.75 |
| **Gibeonite** | /ˈɡɪb.i.ə.naɪt/ | `ɡɪbɪnaɪd / ɡɪbɪənaɪt` (0.69) | `gihbeeuhneyet` | `ɡɪbinaɪ / ɡɪbjunaɪ` | 0.69 |
| **Alian** | /ˈeɪ.li.ən/ | `eɪlən / eɪlɪən` (0.70) | `ay-lee-uhn` | `aɪliɔn / aɪliɔn` | 0.60 |
| **Achbor** | /ˈæk.bɔːr/ | `eɪkboɹ / eɪkbɔɹ` (0.70) | `ak-bawr` | `ɐkeɪbɔɹ / ɪkeɪbɔɹ` | 0.67 |
| **Ammiel** | /ˈæm.i.ɛl/ | `æmiəl / æmjəl` (0.70) | `aam-ee-ehl` | `eɪmitʃɛl / eɪmiɪtʃɛl` | 0.62 |
| **Keilah** | /kiˈaɪ.lə/ | `kɪlə / kilɐ` (0.70) | `kee-eye-luh` | `hiaɪlu / kiaɪlu` | 0.70 |
| **Uzziel** | /ˈʌz.i.ɛl/ | `ʌzioʊ / ʌziəl` (0.70) | `uhzeeehl` | `ɐzi / ɐziəll` | 0.70 |
| **Ahoah** | /əˈhoʊ.ə/ | `ɐhaʊwɔ / ɐhoʊɐ` (0.70) | `ahohuh` | `ɐhoʊʊ / ɐhoʊhu` | 0.68 |
| **Shavsha** ⚑ | /ˈʃæv.ʃə/ | `ʃɑfʃə / ʃafʃɐ` (0.70) | `shav-shuh` | `ʃæfʃu / ʃæfʃu` | 0.60 |
| **Syria-maachah** ⚑ | /ˌsɪr.i.əˈmeɪ.ə.kə/ | `sɪɹiɐmɑtʃɐ / sɪɹiɐmɑtʃɐ` (0.70) | `sireeuhmayuhkuh` | `saɪɹɐmeɪkɐku / saɪɹəmeɪjukəku` | 0.55 |
| **Keturah** | /kəˈtjʊər.ə/ | `kətɚɹɐ / kətɚɹɐ` (0.71) | `kuh-tyoorr-uh` | `kutaɪɹɑ / kutaɪɹɑ` | 0.43 |
| **Manahath** | /ˈmæn.ə.hæθ/ | `meɪnɐhæf / mɛnɐhæf` (0.71) | `man-uh-hath` | `mɛnɐhæv / mænɐhæf` | 0.79 |
| **Adonijah** | /ˌæd.oʊˈnaɪ.dʒə/ | `æɾɐnidʒɐ / æɾɐnidʒə` (0.71) | `ad-oh-neye-juh` | `ædoʊneɪdʒu / ædoʊneɪdʒu` | 0.71 |
| **Shaaraim** | /ˌʃeɪ.əˈreɪ.ɪm/ | `ʃɚɹeɪm / ʃɚɹeɪm` (0.71) | `shayuhrayihm` | `ʃeɪɹeɪm / ʃeɪɹeɪm` | 0.71 |
| **Chenaanah** | /kəˈneɪ.ə.nə/ | `ʃəneɪnə / ʃəneɪnɐ` (0.71) | `kuhnayuhnuh` | `kənaɪnu / kənaɪnu` | 0.57 |
| **Jehoiada** | /dʒəˈhɔɪ.ə.də/ | `dʒɐhoʊᵻdɐ / dʒəhoɪᵻdɐ` (0.71) | `ja-hoy-uh-duh` | `dʒɑhwjɐdə / dʒahoʊɐdə` | 0.67 |
| **Amramites** | /ˈæm.ræm.aɪts/ | `ɑmɹəmaɪts / ɑmɹəmaɪts` (0.71) | `am-ram-eyets` | `ɪmɹəmaɪts / ɛmɹəmaɪɪts` | 0.67 |
| **Zerahites** | /ˈzɛr.ə.haɪts/ | `zɪɹᵻhaɪts / zeɪɹᵻhaɪts` (0.71) | `zehr-uh-heyets` | `zɪɹɐhaɪts / zɪɹɐhaɪɪts` | 0.80 |
| **Gederite** | /ˈɡɛd.ə.raɪt/ | `ɡɛtɹaɪt / jɛdɹaɪt` (0.71) | `geduhreyet` | `ɡɐdɚɹᵻt / ɡədɚɹiɪt` | 0.67 |
| **Jehoadah** ⚑ | /dʒɪˈhoʊ.ə.də/ | `dʒɐhoʊdɐ / dʒɐhoʊdɐ` (0.71) | `ji-hoh-uh-duh` | `dʒihoʊɐdɑ / dʒihoʊɐdʌ` | 0.79 |
| **Shaalbonite** | /ˌʃeɪ.ælˈboʊ.naɪt/ | `ʃɑlbənaɪt / ʃælbənaɪt` (0.72) | `shay-al-boh-neyet` | `ʃeɪɐlboʊneɪt / ʃeɪaʊlboʊneɪɪ` | 0.72 |
| **Jezreelitess** | /ˈdʒɛz.ri.ə.laɪ.tɛs/ | `dʒɛzɹiəliɾəs / dʒɛzɹiəlidəs` (0.73) | `jehzreeuhleyetehs` | `dʒɛzɹiɐlaɪɾəs / dʒɛzɹiɐlaɪdəz` | 0.77 |
| **Romamti-Ezer** | /roʊˌmæm.taɪ ˈiː.zər/ | `ɹoʊməmtiɛzɚ / ɹoʊməmtiɛzɚ` (0.73) | `rohmaamteyeeezuhr` | `ɹoʊmæntaɪizᵻzɚ / ɹoʊmæntaɪjizᵻzɚ` | 0.74 |
| **Nemuel** | /ˈnɛm.jʊ.əl/ | `nɛmjwəl / nɛmjuwəl` (0.73) | `nehmyuuuhl` | `nɛmjəl / nɛmjuəl` | 0.79 |
| **Hilen** | /ˈhaɪ.lɛn/ | `haɪlən / haɪlənd` (0.73) | `heye-lehn` | `haɪleɪn / haɪleɪn` | 0.80 |
| **Kushaiah** | /kuːˈʃaɪ.ə/ | `kəʃaɪɚ / kɐʃaɪɐ` (0.73) | `koo-shy-uh` | `kuʃaɪjaʊ / kuʃaɪɐ` | 0.83 |
| **Ornan** | /ˈɔːr.næn/ | `wɔɹnən / ɔɹnən` (0.73) | `awr-nan` | `ɔɹneɪn / wɔɹnæn` | 0.82 |
| **Ahiah** ⚑ | /əˈhaɪ.ə/ | `ðɐhaɪɚ / ɐhaɪɚ` (0.73) | `uh-heye-uh` | `ɐhaɪɚ / ɐhaɪɚ` | 0.80 |
| **Ismaiah** ⚑ | /ɪzˈmaɪ.ə/ | `ɪzmeɪɚ / ɪzmeɪɐ` (0.73) | `ihz-my-uh` | `aɪzmaɪə / aɪzmaɪɐ` | 0.80 |
| **Dinhabah** | /ˈdɪn.hə.bə/ | `dɪnɚbəl / dɪnhʌbɑ` (0.74) | `dihnhuhbuh` | `dɪnhɑbu / dɪnhʌbu` | 0.79 |
| **Girgashite** | /ˈɡɜːr.ɡə.ʃaɪt/ | `ɡɜdᵻʃaɪt / ɡɜɡəʃaɪt` (0.75) | `gerrguhsheyet` | `ɡɜɡɪʃaɪd / ɡɜɡɪʃaɪt` | 0.69 |
| **Isaac** | /ˈaɪ.zək/ | `aɪzɪk / aɪzɪk` (0.75) | `eye-zuhk` | `aɪzuk / aɪzuk` | 0.75 |
| **Shammah** | /ˈʃæm.ə/ | `ʃeɪmɐ / ʃeɪmɐ` (0.75) | `sham-uh` | `ʃeɪmɐ / ʃeɪmɐ` | 0.75 |
| **Hamran** | /ˈhæm.ræn/ | `hɛmɹæn / hɛmɹeɪn` (0.75) | `ham-rann` | `hæmɹæn / heɪmɹɪn` | 0.83 |
| **Aran** | /ˈɛər.æn/ | `ɛɹən / ɛɹən` (0.75) | `airr-an` | `ɛɹən / ɛɹən` | 0.75 |
| **Eliphelet** | /ɪˈlɪf.ə.lɛt/ | `ɐlɪfəllɪt / ɐlɪfəlɪt` (0.75) | `i-lihf-uh-leht` | `aɪlɪfɚlɛt / aɪlɪfəllɛt` | 0.83 |
| **Ahaz** | /ˈeɪ.hæz/ | `ɐhæz / ɐhæz` (0.75) | `ay-haz` | `aɪhæz / aɪhæz` | 0.75 |
| **Jehoiakim** | /dʒəˈhɔɪ.ə.kɪm/ | `dʒəhoɪkɪm / dʒəhoɪɪkɪm` (0.75) | `ja-hoy-uh-kihm` | `dʒɐhoɪɐkɪm / dʒɐhoɪɐkɪm` | 0.78 |
| **Hashubah** | /həˈʃuː.bə/ | `ɑʃubə / haʃʊbɐ` (0.75) | `huh-shoo-ba` | `hɐʃubieɪ / haʃubieɪ` | 0.64 |
| **Rephaiah** | /rəˈfeɪ.jə/ | `ɹəfeɪ / ɹəfeɪɐ` (0.75) | `ruhfayyuh` | `ɹɐfeɪju / ɹəfeɪju` | 0.83 |
| **Akkub** | /ˈæk.əb/ | `ɐkʌb / ɐkʌb` (0.75) | `aak-uhb` | `ɑkɐb / ɑkʌb` | 0.75 |
| **Ophrah** | /ˈɒf.rə/ | `ɑfɚ / ɑfɹə` (0.75) | `ofruh` | `ɑfɚ / ɑfɚ` | 0.50 |
| **Ishbah** | /ˈɪʃ.bə/ | `ɪʃbɑ / ɪʃbɑ` (0.75) | `ihsh-buhh` | `ɪʃbəl / ɪʃbʊ` | 0.78 |
| **Pharaoh** | /ˈfɛər.oʊ/ | `feɪɹoʊ / feɪɹoʊ` (0.75) | `fairr-oh` | `feɪɹoʊ / feɪɹoʊ` | 0.75 |
| **Joshah** | /ˈdʒoʊ.ʃə/ | `dʒɑʃə / dʒɑʃɐ` (0.75) | `joh-shuh` | `dʒoʊʃu / dʒoʊʃu` | 0.75 |
| **Pallu** | /ˈpæl.uː/ | `pælᵻ / hælu` (0.75) | `paloo` | `pəllu / pəlu` | 0.75 |
| **Pilneser** | /pɪlˈniː.zər/ | `pɪlnəsɚ / pɪlnəsɚ` (0.75) | `pihlneezuhr` | `pɪlmizɚ / pəmizɚ` | 0.75 |
| **Jeshishai** | /dʒəˈʃɪʃ.aɪ/ | `dʒɛʃəʃaɪ / dʒɛʃɪʃaɪ` (0.75) | `juh-shihsh-eye` | `dʒuʃɪʃaɪ / dʒuʃɪʃaɪ` | 0.83 |
| **Azriel** | /ˈæz.ri.ɛl/ | `ɑzɹɛl / ɑzɹiɛl` (0.75) | `azreeehl` | `æzɹiəl / æzɹi` | 0.75 |
| **Hara** | /ˈhɛər.ə/ | `hɔɹɐ / hɔɹɐ` (0.75) | `hairra` | `haɪɹə / haɪɹə` | 0.75 |
| **Zerahiah** | /ˌzɛr.əˈhaɪ.ə/ | `zɪɹɐhaɪɚ / zɪɹɐhaɪɚ` (0.75) | `zehr-uh-heye-uh` | `zɪɹɐhaɪɐ / zɪɹɐhaɪɚ` | 0.80 |
| **Meraioth** | /məˈreɪ.ɒθ/ | `mɚɹeɪɪf / mɚɹeɪəθ` (0.75) | `muh-ray-oth` | `mɚɹeɪɑf / mɚɹeɪɑf` | 0.83 |
| **Anathoth** | /ˈæn.ə.θɒθ/ | `ænɐfɑf / ænəfɑθ` (0.75) | `aanuhthoth` | `ɐnuθɑθ / ɐnuθɑθ` | 0.67 |
| **Shemuel** | /ʃəˈmjuː.əl/ | `ʃɛmjuwəl / ʃɛmjuwəl` (0.75) | `shamyoouhl` | `ʃæməl / ʃæmiəl` | 0.57 |
| **Isshiah** | /ɪˈʃaɪ.ə/ | `ɪʃiɐ / ɪʃiɐ` (0.75) | `isheyeuh` | `ɪʃiu / ɪʃiu` | 0.50 |
| **Iri** | /ˈaɪ.raɪ/ | `aɪɚɹaɪ / aɪɑɹɹaɪ` (0.75) | `y-reye` | `waɪɹaɪ / waɪɹaɪ` | 0.75 |
| **Aramitess** | /ˈɛər.əm.aɪ.tɛs/ | `ɛɹəmaɪɾəs / ɛɹəmaɪɾəs` (0.75) | `airr-uhm-eye-tehss` | `ɛɹəmaɪteɪst / ɛɹəmaɪteɪs` | 0.83 |
| **Uzzen** | /ˈʌz.ɛn/ | `ʌzən / ʌzən` (0.75) | `uhz-ehn` | `ɐzɪn / ɐzɪn` | 0.75 |
| **Telah** | /ˈtiː.lə/ | `tɛlə / tɛlɐ` (0.75) | `tee-luh` | `tilu / tilu` | 0.75 |
| **Serah** | /ˈsɪər.ə/ | `sɛɹɐ / sɛɹɐ` (0.75) | `seerra` | `siɛɹɐ / siɛɹɐ` | 0.60 |
| **Shamma** | /ˈʃæm.ə/ | `ʃɑmɐ / ʃɑmɐ` (0.75) | `sham-uh` | `ʃeɪmɐ / ʃeɪmɐ` | 0.75 |
| **Jehoiarib** | /dʒəˈhɔɪ.ə.rɪb/ | `dʒɐhoɪɹɪb / dʒəhoɪɹɪb` (0.75) | `juhhoyuhrihb` | `dʒəhoɪɹɪb / dʒəhoɪɹɪb` | 0.75 |
| **Elishua** | /ˌɛl.ɪˈʃuː.ə/ | `ᵻlɪʃuɐ / ᵻlɪʃwɐ` (0.75) | `ehlihshoouh` | `eɪlɪʃu / eɪlɪʃu` | 0.67 |
| **Jaaziel** | /dʒeɪˈeɪ.zi.ɛl/ | `dʒeɪzəl / dʒeɪziəl` (0.75) | `jayayzeeehl` | `dʒeɪziəl / dʒeɪziəl` | 0.83 |
| **Jehiel** | /dʒəˈhaɪ.ɛl/ | `dʒihaɪɛl / dʒihaɪəl` (0.75) | `juh-heye-ehll` | `dʒuhaɪɛl / dʒoʊhaɪɛl` | 0.83 |
| **Gershonites** | /ˈɡɜːr.ʃən.aɪts/ | `dʒɜʃənaɪts / dʒɜʃənaɪts` (0.75) | `gerrshuhneyets` | `ɡɚʃɔnɪtss / ɡɚʃɔnɪts` | 0.71 |
| **Haziel** | /ˈheɪ.zi.ɛl/ | `heɪzəl / heɪziəl` (0.75) | `hayzeeehl` | `heɪziəl / heɪziəl` | 0.83 |
| **Huppah** | /ˈhʌp.ə/ | `hɑpoʊ / hʌpɐ` (0.75) | `huhp-uhh` | `hɑpɐ / hʌpɑ` | 0.75 |
| **Mallothi** | /ˈmæl.ə.θaɪ/ | `mælətaɪ / mɛlətaɪ` (0.75) | `mal-uh-theye` | `mælɐðeɪ / mælɐðeɪ` | 0.67 |
| **Achsa** ⚑ | /ˈæk.sə/ | `ɑksə / ɑksə` (0.75) | `ak-suhh` | `ɐkeɪsʌ / ɐkeɪsɐ` | 0.60 |
| **Reaia** ⚑ | /riːˈeɪ.ə/ | `ɹiɐ / ɹiɐ` (0.75) | `reeaya` | `ɹiɐ / ɹiɐ` | 0.75 |
| **Ishiah** ⚑ | /ɪˈʃaɪ.ə/ | `ɪʃiɐ / ɪʃiɐ` (0.75) | `isheyeuh` | `ɪʃiu / ɪʃiu` | 0.50 |
| **Jezliah** ⚑ | /dʒɛzˈlaɪ.ə/ | `dʒɛzliɐ / dʒɛsliɐ` (0.75) | `jehz-leye-uh` | `dʒeɪzliɐ / dʒeɪzliɐ` | 0.67 |
| **Antothijah** ⚑ | /ˌæn.toʊˈθaɪ.dʒə/ | `ændɐθaɪdʒɐ / æntᵻfaɪdʒɐ` (0.75) | `antohtheyejuh` | `æntoʊfidʒu / æntoʊθidʒu` | 0.69 |
| **Hazzelelponi** | /ˌhæz.ə.lɛlˈpoʊ.naɪ/ | `hæzɐləlpoʊni / hæzɐləpoʊni` (0.77) | `haz-uh-lehl-poh-neyee` | `hæzɐlɛlpoʊneɪi / hæzɐloʊlpoʊnii` | 0.83 |
| **Eliahba** | /ɪˈlaɪ.ə.bə/ | `ɐlaɪɐbɚ / ᵻlaɪbɐ` (0.77) | `ihleyeuhbuh` | `ɐlaɪubu / ɐlaɪjubu` | 0.46 |
| **Iphedeiah** ⚑ | /ˌɪf.ɪˈdiː.ə/ | `ɪfɐdiɚ / ɪfɐdiɐ` (0.77) | `ihf-i-dee-uh` | `ɪfaɪdiɐ / ɪfaɪdiɐ` | 0.83 |
| **Jehallelel** | /dʒəˈhæl.ə.lɛl/ | `dʒɐhæləlloʊ / dʒɐhæləllaʊ` (0.78) | `juh-hal-uh-lehl` | `dʒuhælɐloʊl / dʒʊhælɐlɛl` | 0.83 |
| **Kiriathaim** | /ˌkɪr.i.əˈθeɪ.ɪm/ | `kɪɹiθeɪm / kɪɹiəfeɪm` (0.78) | `kihr-ee-uh-thay-ihmm` | `kɪɹəθeɪm / kuɹəθeɪm` | 0.72 |
| **Jehezekel** ⚑ | /dʒɪˈhɛz.ɪ.kɛl/ | `dʒᵻhizɪkəl / dʒɪhizɪkəl` (0.78) | `jihhehzihkehl` | `dʒɐheɪzikɛl / dʒɐheɪzikɛl` | 0.67 |
| **Meshullam** | /məˈʃʊl.əm/ | `mɐʃɑləm / mɪʃʌləm` (0.79) | `muh-shuul-uhm` | `mɐʃoʊlɐm / mɪʃʊlam` | 0.79 |
| **Elioenai** | /ˌɛl.i.oʊˈiː.naɪ/ | `ɪlioʊeɪnaɪ / ɪlioʊinaɪ` (0.79) | `ehleeoheeneye` | `ɐlioʊhinaɪ / əlioʊhinaɪ` | 0.75 |
| **Jaakobah** | /ˌdʒeɪ.əˈkoʊ.bə/ | `dʒᵻkoʊbə / dʒəkoʊbɐ` (0.79) | `jay-uh-koh-buh` | `dʒeɪɐkoʊbɑt / dʒeɪɐkoʊbaɪt` | 0.75 |
| **Babylon** | /ˈbæb.ɪ.lən/ | `bæbᵻlɔn / bæbəllɔn` (0.79) | `babihluhn` | `ɐbɪlən / bəbɪlən` | 0.79 |
| **Hushathite** | /ˈhuː.ʃə.θaɪt/ | `hɔʃɐθaɪ / hʌʃəθaɪt` (0.79) | `hooshuhtheyet` | `hʊʃəfit / hʊʃɪθjɪ` | 0.64 |
| **Moabites** | /ˈmoʊ.ə.baɪts/ | `mʌləbaɪts / moʊləbaɪts` (0.79) | `mohabeyets` | `moʊhɑbaɪts / moʊhɑbaɪts` | 0.71 |
| **Cherethites** | /ˈkɛr.ə.θaɪts/ | `tʃɛɹəθaɪts / tʃɛɹɪθaɪts` (0.79) | `kehr-a-theyets` | `kɛɹɐθeɪɪts / kɛɹəθeɪɪts` | 0.75 |
| **Jaresiah** ⚑ | /ˌdʒær.ɪˈsaɪ.ə/ | `dʒɚɹɪsaɪɐ / dʒɛɹəsaɪɐ` (0.79) | `jaarihseyeuh` | `dʒɛɹisɑju / dʒɛɹisaɪju` | 0.44 |

---

_Genesis 1–11 and 1 Chronicles swept in WEB + KJV spellings; voice en-US-AndrewNeural; each name measured in two carrier sentences. 406 of 1772 names in the list now carry an override._
