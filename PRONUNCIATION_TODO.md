# Pronunciation to-do — whole canon

Every proper noun in the WEB text has been checked against real audio. The list holds 3327 names; this file is what checking could **not** settle.

| Verdict | Names |
| --- | --- |
| unchecked | 0 |
| fine as spelled | 1501 |
| overridden | 859 |
| suggestion waiting | 170 |
| still wrong | 635 |
| unsure (guessed IPA) | 162 |

## Where the references come from

| Reference | Names |
| --- | --- |
| curated | 1821 |
| ISBE (1915) | 975 |
| CMUdict | 232 |
| Wiktionary | 62 |
| Wikipedia | 13 |
| generated guess | 224 |

The ISBE references were harvested from the International Standard Bible Encyclopedia (1915, public domain) — headword respellings like `a-da-li'-a`, converted to IPA (`isbe_harvest.py` → `isbe_to_ipa.py` → `isbe_apply.py`). Measured against 150 curated references the conversion agrees 0.91 — well above the 0.72 rule-generator it replaced, so these are real references, judged accordingly (ok / still wrong, not unsure).

**Known acoustic blind spot:** a hyphenated pure-vowel segment in a respelling (`ee-mim`, `el-a-sar`) is read out letter-by-letter but transcribes as a clean long vowel, so a score alone cannot clear such a spelling. `isbe_sweep.py`/`isbe_repair.py` refuse to emit them; older hand-tuned overrides that still carry one are listed at the bottom for the ear.

## Still wrong — worth acting on

Judged against a sourced reference; no tested respelling fixed them.

| Name | Reference | Source | Voice says | Score |
| --- | --- | --- | --- | --- |
| **Pau** | /ˈpɔː/ | ISBE (1915) | `paʊ / haʊ` | 0.25 |
| **Puah** | /ˈpjuː.ə/ | curated | `` | 0.25 |
| **Sion** | /ˈsaɪ.ən/ | Wiktionary | `` | 0.25 |
| **Coos** | /ˈkoʊ.ɒs/ | curated | `` | 0.25 |
| **Shallecheth** | /ˈʃæl.ə.kɛθ/ | curated | `` | 0.29 |
| **Eloi** | /ˈiːlɔɪ/ | Wiktionary | `` | 0.29 |
| **Beer** | /bˈɪr/ | CMUdict | `` | 0.33 |
| **Roi** | /rˈɔɪ/ | CMUdict | `` | 0.33 |
| **Ain** | /ˈeɪ.ɪn/ | curated | `` | 0.33 |
| **Pul** | /pʌl/ | curated | `` | 0.33 |
| **Bathshua** | /bæθˈʃuː.ə/ | curated | `` | 0.33 |
| **Ahi** | /ˈeɪ.haɪ/ | curated | `` | 0.33 |
| **Tokhath** | /ˈtɒk.hæθ/ | curated | `` | 0.33 |
| **Thaddaeus** | /ˈθædiːəs/ | Wiktionary | `` | 0.33 |
| **Jediael** | /dʒəˈdaɪ.eɪ.ɛl/ | curated | `` | 0.36 |
| **Hephzibah** | /ˈhɛpzɪbə/ | Wiktionary | `` | 0.38 |
| **Amal** | /ˈeɪ.mæl/ | curated | `` | 0.38 |
| **Beri** | /ˈbɪər.aɪ/ | curated | `` | 0.38 |
| **Shephuphan** | /ʃəˈfjuː.fæn/ | curated | `` | 0.38 |
| **Hadar** | /hˈædɚ/ | CMUdict | `` | 0.40 |
| **Goshen** | /ɡˈoʊʃɪn/ | CMUdict | `` | 0.40 |
| **Balaam** | /ˈbeɪləm/ | Wikipedia | `` | 0.40 |
| **Barak** | /bˈɑrək/ | CMUdict | `` | 0.40 |
| **Hillel** | /hɪlˈɛl/ | CMUdict | `` | 0.40 |
| **Paarai** | /ˈpeɪ.ə.raɪ/ | ISBE (1915) | `hisɛd / pɚɹaɪ` | 0.40 |
| **Kir** | /kˈɪr/ | CMUdict | `` | 0.40 |
| **Igeal** | /ˈɪɡ.i.əl/ | curated | `` | 0.40 |
| **Asiel** | /ˈeɪ.si.ɛl/ | curated | `` | 0.40 |
| **Jeiel** | /dʒəˈaɪ.əl/ | curated | `` | 0.40 |
| **Isuah** | /ˈɪs.ju.ə/ | curated | `` | 0.40 |
| **Baasha** | /ˈbeɪ.ə.ʃə/ | curated | `` | 0.40 |
| **Cephas** | /sˈɛfəz/ | CMUdict | `` | 0.40 |
| **Melchizedek** | /mɛkˈiːzɛdɛk/ | CMUdict | `` | 0.41 |
| **Shimeath** | /ˈʃɪm.i.æθ/ | curated | `` | 0.42 |
| **Pathros** | /ˈpæθ.rɒs/ | ISBE (1915) | `hæfɹoʊs / hæfɹoʊz` | 0.42 |
| **Aquila** | /ˈæk.wɪ.lə/ | curated | `` | 0.42 |
| **Ithrites** | /ˈɪθ.raɪts/ | curated | `` | 0.43 |
| **Chenaniah** | /ˌkɛn.əˈnaɪ.ə/ | curated | `` | 0.43 |
| **Giddalti** | /ɡɪˈdæl.taɪ/ | curated | `` | 0.43 |
| **Eliakim** | /ɪˈlaɪ.ə.kɪm/ | curated | `` | 0.43 |
| **Jesimiel** | /dʒəˈsɪm.i.ɛl/ | curated | `` | 0.44 |
| **Pas-dammim** | /pæsˈdæm.ɪm/ | curated | `` | 0.44 |
| **Anetothite** | /əˈnɛt.ə.θaɪt/ | curated | `` | 0.44 |
| **Mattathias** | /ˌmæt.əˈθaɪ.əs/ | curated | `` | 0.44 |
| **Baal-hanan** | /ˌbeɪ.əlˈheɪ.næn/ | curated | `` | 0.44 |
| **Jehaleleel** | /dʒɪˈhæl.ɪ.liːl/ | curated | `` | 0.44 |
| **Eliada** | /ɪˈlaɪ.ə.də/ | curated | `` | 0.46 |
| **Phanuel** | /fəˈnjuː.ɛl/ | curated | `` | 0.46 |
| **Attalia** | /ˌæt.əˈlaɪ.ə/ | curated | `` | 0.46 |
| **Akan** | /ˈækæn/ | Wiktionary | `` | 0.50 |
| **Canaanite** | /kˈeɪnənaɪt/ | CMUdict | `` | 0.50 |
| **Asenath** | /ˈæsɪnæθ/ | Wikipedia | `` | 0.50 |
| **Guni** | /ˈɡjuː.naɪ/ | curated | `` | 0.50 |
| **Igal** | /ˈaɪ.ɡæl/ | curated | `` | 0.50 |
| **Anak** | /ˈeɪnæk/ | Wikipedia | `` | 0.50 |
| **Arad** | /ˈɛər.æd/ | curated | `` | 0.50 |
| **Zalmonah** | /zæl.ˈmɒneɪ/ | ISBE (1915) | `zɐlmoʊnɐ / zoʊmoʊnɐ` | 0.50 |
| **Aven** | /ɑvˈeɪn/ | CMUdict | `` | 0.50 |
| **Shual** | /ˈʃuː.əl/ | curated | `` | 0.50 |
| **Ashan** | /ˈeɪ.ʃæn/ | curated | `` | 0.50 |
| **Balah** | /ˈbæleɪ/ | ISBE (1915) | `bɑlɐ / bɑlɐ` | 0.50 |
| **Ithlah** | /ˈɪθ.lə/ | ISBE (1915) | `ɪfloʊ / ɪflaɪ` | 0.50 |
| **Shittah** | /ˈʃɪteɪ/ | ISBE (1915) | `ʃɪɾɐ / ʃɪdɐ` | 0.50 |
| **Ahimaaz** | /əˈhɪm.eɪ.æz/ | curated | `` | 0.50 |
| **Ahinoam** | /əˈhɪn.oʊ.æm/ | curated | `` | 0.50 |
| **Ner** | /nɜːr/ | curated | `` | 0.50 |
| **Gai** | /ɡˈeɪ/ | CMUdict | `` | 0.50 |
| **Asaph** | /ˈeɪ.sæf/ | curated | `` | 0.50 |
| **Asaiah** | /əˈseɪ.jə/ | curated | `` | 0.50 |
| **Ephratah** | /ˈɛf.rə.tɑː/ | curated | `` | 0.50 |
| **Kirjath-jearim** | /ˌkɜːr.dʒæθˈdʒiː.ə.rɪm/ | curated | `` | 0.50 |
| **Bath-shua** | /bæθˈʃuː.ə/ | curated | `` | 0.50 |
| **Naam** | /ˈneɪ.æm/ | curated | `` | 0.50 |
| **Asareel** | /əˈsær.i.ɛl/ | curated | `` | 0.50 |
| **Bithiah** | /bɪˈθaɪ.ə/ | curated | `` | 0.50 |
| **Biri** | /ˈbɪr.aɪ/ | curated | `` | 0.50 |
| **Azaz** | /ˈeɪ.zæz/ | curated | `` | 0.50 |
| **Huri** | /ˈhjʊər.aɪ/ | curated | `` | 0.50 |
| **Anem** | /ˈeɪ.nɛm/ | curated | `` | 0.50 |
| **Hasenuah** | /ˌhæs.ɪˈnjuː.ə/ | curated | `` | 0.50 |
| **Kore** | /ˈkɔːr.i/ | curated | `` | 0.50 |
| **Eliphal** | /ɪˈlaɪ.fæl/ | curated | `` | 0.50 |
| **Hothan** | /ˈhoʊ.θæn/ | curated | `` | 0.50 |
| **Elihu** | /ɪˈlaɪ.hjuː/ | curated | `` | 0.50 |
| **Pelethites** | /ˈpɛl.ə.θaɪts/ | curated | `` | 0.50 |
| **Bukkiah** | /bəˈkaɪ.ə/ | curated | `` | 0.50 |
| **Peulthai** | /piːˈʌl.θaɪ/ | curated | `` | 0.50 |
| **Tebaliah** | /ˌtɛb.əˈlaɪ.ə/ | curated | `` | 0.50 |
| **Jehuel** | /dʒəˈhjuː.ɛl/ | curated | `` | 0.50 |
| **Miniamin** | /mɪˈnaɪ.ə.mɪn/ | curated | `` | 0.50 |
| **Michmas** | /ˈmɪkmæʃ/ | Wiktionary | `` | 0.50 |
| **Ahasuerus** | /əhæʃəwˈɛrəs/ | CMUdict | `` | 0.50 |
| **Kelaiah** | /ki.ˈleɪ.jə/ | ISBE (1915) | `kɐlaɪɐ / kəlaɪɐ` | 0.50 |
| **Raamiah** | /rə.ə.ˈmaɪ.ə/ | ISBE (1915) | `ɹeɪmiɐ / ɹeɪmiɐ` | 0.50 |
| **Joiada** | /ˈdʒɔɪ.ə.də/ | ISBE (1915) | `dʒɚɹɑdə / dʒoɪɑdɐ` | 0.50 |
| **Negev** | /nˈɛɡɛv/ | CMUdict | `` | 0.50 |
| **Aramaic** | /ɑrɑmˈɛjɪk/ | CMUdict | `` | 0.50 |
| **Ezekiel** | /ˈɛzɪkiːl/ | CMUdict | `` | 0.50 |
| **Dura** | /dˈʊrə/ | CMUdict | `` | 0.50 |
| **Shalman** | /ˈʃæl.mæn/ | ISBE (1915) | `ʃɑmən / ʃɑmən` | 0.50 |
| **Salome** | /səlˈoʊmiː/ | CMUdict | `` | 0.50 |
| **Semein** | /ˈsɛm.i.ɪn/ | curated | `` | 0.50 |
| **Bethsphage** | /ˈbɛθ.sfə.dʒiː/ | curated | `` | 0.50 |
| **Cleopas** | /ˈkliː.ə.pəs/ | curated | `` | 0.50 |
| **Nathanael** | /nˈæθəneɪl/ | CMUdict | `` | 0.50 |
| **Manaen** | /ˈmæn.eɪ.ɛn/ | curated | `` | 0.50 |
| **Melita** | /ˈmɛl.ɪ.tə/ | curated | `` | 0.50 |
| **Puteoli** | /pjuːˈtiː.ə.laɪ/ | curated | `` | 0.50 |
| **Eunice** | /jˈuːnəs/ | CMUdict | `` | 0.50 |
| **Haniel** | /ˈhæn.i.ɛl/ | curated | `` | 0.54 |
| **Jashubilehem** | /dʒəˌʃuː.bɪˈliː.hɛm/ | curated | `` | 0.55 |
| **Oren** | /ˈɔːr.ɛn/ | curated | `` | 0.55 |
| **Aher** | /ˈeɪ.hər/ | curated | `` | 0.55 |
| **Jesiah** | /dʒɪˈsaɪ.ə/ | curated | `` | 0.55 |
| **Lemuel** | /ˈlɛm.jə(wə)l/ | Wiktionary | `` | 0.55 |
| **Zurishaddai** | /zjʊ.ri.ˈʃæd.aɪ/ | ISBE (1915) | `zɚɹɪʃɑdaɪ / zɚɹɪʃɑdaɪ` | 0.56 |
| **Mephibosheth** | /məˈfɪb.əˌʃɛθ/ | Wiktionary | `` | 0.56 |
| **Jehudijah** | /ˌdʒɛ.hjuːˈdaɪ.dʒə/ | curated | `` | 0.56 |
| **Kirjathaim** | /ˌkɜːr.dʒəˈθeɪ.ɪm/ | curated | `` | 0.56 |
| **Meshelemiah** | /məˌʃɛl.əˈmaɪ.ə/ | curated | `` | 0.56 |
| **Eliehoenai** | /ɪˌlaɪ.ə.hoʊˈiː.naɪ/ | curated | `` | 0.56 |
| **Moabitess** | /ˈmoʊ.ə.baɪ.tɛs/ | curated | `` | 0.56 |
| **Bezaleel** | /bɪˈzæl.i.ɛl/ | curated | `` | 0.56 |
| **Jaareshiah** | /ˌdʒeɪ.ə.rəˈʃaɪ.ə/ | curated | `` | 0.56 |
| **Nethaneel** | /nɪˈθæn.i.ɛl/ | curated | `` | 0.56 |
| **Ramathite** | /ˈreɪ.mə.θaɪt/ | curated | `` | 0.56 |
| **Barsabas** | /ˈbɑːr.sə.bəs/ | curated | `` | 0.56 |
| **Abimael** | /əˈbɪm.eɪ.ɛl/ | curated | `` | 0.57 |
| **Abihail** | /ˌæb.ɪˈheɪ.ɪl/ | curated | `` | 0.57 |
| **Penuel** | /pəˈnjuː.əl/ | curated | `` | 0.57 |
| **Mattaniah** | /ˌmæt.əˈnaɪ.ə/ | curated | `` | 0.57 |
| **Eliashib** | /ɪˈlaɪ.ə.ʃɪb/ | curated | `` | 0.57 |
| **Ahuzam** | /əˈhjuː.zæm/ | curated | `` | 0.57 |
| **Josibiah** | /ˌdʒɒs.ɪˈbaɪ.ə/ | curated | `` | 0.57 |
| **Azareel** | /əˈzær.i.ɛl/ | curated | `` | 0.57 |
| **Danites** | /ˈdæn.aɪts/ | curated | `` | 0.57 |
| **Perazim** | /pəˈreɪ.zɪm/ | curated | `` | 0.57 |
| **Elipheleh** | /ɪˈlɪf.ɪ.lɛ/ | curated | `` | 0.57 |
| **Gedaliah** | /ˌɡɛd.əˈlaɪ.ə/ | curated | `` | 0.57 |
| **Jathniel** | /ˈdʒæθ.ni.ɛl/ | curated | `` | 0.57 |
| **Peullethai** | /piˈʌl.ə.θaɪ/ | curated | `` | 0.57 |
| **Shelemiah** | /ˌʃɛl.əˈmaɪ.ə/ | curated | `` | 0.57 |
| **Jechiliah** | /ˌdʒɛk.ɪˈlaɪ.ə/ | curated | `` | 0.57 |
| **Conaniah** | /ˌkɒn.əˈnaɪ.ə/ | curated | `` | 0.57 |
| **Hakupha** | /hə.ˈkjuː.fə/ | ISBE (1915) | `ɐkoʊfɚ / hɐkoʊfɐ` | 0.57 |
| **Josiphiah** | /dʒɒs.i.ˈfaɪ.ə/ | ISBE (1915) | `dʒoʊsɪfiɐ / dʒoʊsɪfiɐ` | 0.57 |
| **Mattenai** | /mæt.i.ˈneɪ.aɪ/ | ISBE (1915) | `mædənaɪ / mæɾənaɪ` | 0.57 |
| **Pethuel** | /pi.ˈθjuː.ɛl/ | ISBE (1915) | `pɛθjuəl / hɛθjwəl` | 0.57 |
| **Tertius** | /tˈɚtiːɪs/ | CMUdict | `` | 0.57 |
| **Artemas** | /ˈɑrtɪməz/ | CMUdict | `` | 0.57 |
| **Annas** | /ˈæn.əs/ | curated | `` | 0.57 |
| **Leummim** | /li.ˈʌm.ɪm/ | ISBE (1915) | `lʊməm / lʌməm` | 0.58 |
| **Hanniel** | /ˈhæn.i.ɛl/ | curated | `` | 0.58 |
| **Aijalon** | /ˈædʒ.ə.lɒn/ | curated | `` | 0.58 |
| **Taanach** | /ˈteɪ.ə.næk/ | curated | `` | 0.58 |
| **Benaiah** | /bəˈneɪ.jə/ | curated | `` | 0.58 |
| **Jezoar** | /dʒɪˈzoʊ.ɑːr/ | curated | `` | 0.58 |
| **Mahalah** | /ˈmæh.ə.lə/ | curated | `` | 0.58 |
| **Eleadah** | /ˌɛl.iˈeɪ.də/ | curated | `` | 0.58 |
| **Shimeam** | /ˈʃɪm.i.æm/ | curated | `` | 0.58 |
| **Artaxerxes** | /ˌɑːtə(ɡ)ˈzɜːksiːz/ | Wiktionary | `` | 0.58 |
| **Abdeel** | /ˈæb.di.ɛl/ | ISBE (1915) | `ɐbdi / æbdi` | 0.58 |
| **Matthan** | /ˈmæt.θæn/ | ISBE (1915) | `mæðən / mæθɪn` | 0.58 |
| **Anthothijah** | /ˌæn.θoʊˈθaɪ.dʒə/ | curated | `` | 0.59 |
| **Immanuel** | /ˈɪmənʊl/ | CMUdict | `` | 0.59 |
| **Bigthana** | /ˈbɪg.θæn/ | ISBE (1915) | `bɪɡθeɪnɚ / bɪɡfeɪnɐ` | 0.60 |
| **Mamre** | /ˈmæmri/ | Wikipedia | `` | 0.60 |
| **Goiim** | /ˈgɔɪ.jɪm/ | ISBE (1915) | `ɡoʊɪm / ɡoʊɪm` | 0.60 |
| **Dothan** | /dˈɑθən/ | CMUdict | `` | 0.60 |
| **Enaim** | /i.ˈneɪ.ɪm/ | ISBE (1915) | `ɐneɪm / ɐneɪm` | 0.60 |
| **Zuar** | /ˈzjuːɑːr/ | ISBE (1915) | `zuɚ / zuɚ` | 0.60 |
| **Hormah** | /ˈhɔːr.mə/ | curated | `` | 0.60 |
| **Balak** | /bɑlək/ | CMUdict | `` | 0.60 |
| **Keziz** | /ˈkiː.zɪz/ | ISBE (1915) | `kɐziz / kɐziz` | 0.60 |
| **Naioth** | /ˈneɪ.jɒθ/ | ISBE (1915) | `neɪəθ / neɪɪθ` | 0.60 |
| **Racal** | /rˈækəl/ | CMUdict | `` | 0.60 |
| **Rezin** | /rəˌziːn/ | Wiktionary | `` | 0.60 |
| **Jotbah** | /ˈdʒɒt.bə/ | ISBE (1915) | `dʒɑbɑ / dʒɑbɑ` | 0.60 |
| **Bunah** | /ˈbjuː.nə/ | curated | `` | 0.60 |
| **Eker** | /ˈiː.kər/ | curated | `` | 0.60 |
| **Ephlal** | /ˈɛf.læl/ | curated | `` | 0.60 |
| **Reaiah** | /riˈeɪ.jə/ | curated | `` | 0.60 |
| **Adiel** | /ˈeɪ.di.ɛl/ | curated | `` | 0.60 |
| **Ishuai** | /ˈɪʃ.ju.aɪ/ | curated | `` | 0.60 |
| **Maasai** | /ˈmeɪ.ə.saɪ/ | curated | `` | 0.60 |
| **Tobadonijah** | /ˌtɒb.æd.oʊˈnaɪ.dʒə/ | curated | `` | 0.60 |
| **Zattu** | /ˈzætjʊ/ | ISBE (1915) | `zæɾᵻ / zætu` | 0.60 |
| **Athlai** | /ˈæθ.lə.aɪ/ | ISBE (1915) | `æflaɪ / æflaɪ` | 0.60 |
| **Anaiah** | /æn.ə.ˈaɪ.ə/ | ISBE (1915) | `ɐnaɪɐ / ɐnaɪɐ` | 0.60 |
| **Laishah** | /lə.ˈaɪ.ʃə/ | ISBE (1915) | `laɪʃɑ / laɪʃɑ` | 0.60 |
| **Neriah** | /ni.ˈraɪ.ə/ | ISBE (1915) | `nɪɹiɐ / nɪɹiə` | 0.60 |
| **Tammuz** | /ˈtæm.ʌz/ | ISBE (1915) | `tɑməs / tɑməs` | 0.60 |
| **Gebal** | /ˈgiː.bæl/ | ISBE (1915) | `dʒibəl / dʒibəl` | 0.60 |
| **Hosea** | /hoʊsˈiːə/ | CMUdict | `` | 0.60 |
| **Salim** | /sˈælɪm/ | CMUdict | `` | 0.60 |
| **Deity** | /dˈiːətiː/ | CMUdict | `` | 0.60 |
| **Laodiceans** | /lə.ɒd.i.ˈsiː.ænz/ | ISBE (1915) | `leɪaʊɾəsiənz / leɪaʊɾəsiənz` | 0.60 |
| **Mattithiah** | /ˌmæt.ɪˈθaɪ.ə/ | curated | `` | 0.61 |
| **Hammolecheth** | /hæˈmɒl.ə.kɛθ/ | curated | `` | 0.61 |
| **Hammoleketh** | /həˈmɒl.ɪ.kɛθ/ | curated | `` | 0.61 |

_…and 435 more; filter to "Still wrong" in the Pronunciation Studio for the full set._

## Suggestions waiting

A better spelling is recorded in `say` but not applied (`override:false`) — it beat the plain reading without clearing the adoption bar, or a repair could not hold its score. These want an ear in the Studio.

| Name | Reference | Source | Voice says | Score |
| --- | --- | --- | --- | --- |
| **Aiath** | /ˈeɪ.jæθ/ | ISBE (1915) | `aɪɐv / aɪɪð` | 0.00 |
| **Aretas** | /ˈɑːr.i.tæs/ | ISBE (1915) | `ɚɹɛdəz / ɚɹɛdᵻz` | 0.17 |
| **Ahzai** | /ˈeɪ.zaɪ/ | ISBE (1915) | `aʊsaɪ / aʊtsaɪ` | 0.29 |
| **Gehazi** | /gi.ˈheɪ.zaɪ/ | ISBE (1915) | `ɡɐhɑsi / ɡɐhɑtsi` | 0.31 |
| **Eri** | /ˈiː.raɪ/ | ISBE (1915) | `eɪɹi / ɛɹi` | 0.33 |
| **Evi** | /ˈiː.vaɪ/ | ISBE (1915) | `ɛvi / ɛvi` | 0.33 |
| **Jedidah** | /dʒi.ˈdaɪ.də/ | ISBE (1915) | `dʒɛɾədɐ / s` | 0.33 |
| **Onesimus** | /oʊ.ˈnɛs.i.mʌs/ | ISBE (1915) | `wʌnzaɪməs / wʌnzaɪməs` | 0.38 |
| **Geuel** | /ˈgjuː.ɛl/ | ISBE (1915) | `ɡoʊl / ɡu` | 0.40 |
| **Jarha** | /ˈdʒɑːr.hə/ | curated | `` | 0.40 |
| **Hobaiah** | /hə.ˈbeɪ.jə/ | ISBE (1915) | `hoʊbaɪɚ / hoʊbaɪɐ` | 0.42 |
| **Shuthelahites** | /ˈʃuː.θi.lə/ | ISBE (1915) | `ʃəfilɐhaɪts / ʃɪθilɐhaɪts` | 0.45 |
| **Jaddua** | /ˈdʒædjʊ.ə/ | ISBE (1915) | `dʒædʒuəl / dʒædʒuɐ` | 0.46 |
| **Bichri** | /ˈbɪk.raɪ/ | ISBE (1915) | `baɪkɹi / waɪkɹii` | 0.47 |
| **Epaphroditus** | /i.pæf.roʊ.ˈdaɪ.tʌs/ | ISBE (1915) | `ɛpᵻfɹɑdᵻdəs / ɛpɚfɹɑdᵻdɪs` | 0.48 |
| **Pethor** | /ˈpiː.θɔːr/ | ISBE (1915) | `pɛθɚ / hɛθɚ` | 0.50 |
| **Idalah** | /ˈɪd.ə.lə/ | ISBE (1915) | `ɐdɑlɚ / aɪdɑlɚ` | 0.50 |
| **Jerubbaal** | /dʒərjʊ.ˈbeɪ.æl/ | ISBE (1915) | `dɚɹʌbəl / dʒɚɹʌbəl` | 0.50 |
| **Arieh** | /ˈeɪ.ri.i/ | ISBE (1915) | `ɑɹɹiɐ / ɑɹɹiɐ` | 0.50 |
| **Netophah** | /ni.ˈtoʊ.fə/ | ISBE (1915) | `nɛdəfə / nɛdəfɐ` | 0.50 |
| **Mattattah** | /ˈmæt.ə.tə/ | ISBE (1915) | `mətæɾɐ / mɪtædɐ` | 0.50 |
| **Jaasu** | /ˈdʒeɪ.əsjʊ/ | ISBE (1915) | `dʒɑsu / dʒɑsu` | 0.50 |
| **Meraiah** | /mi.ˈreɪ.jə/ | ISBE (1915) | `mɚɹaɪɐ / mɚɹaɪɐ` | 0.50 |
| **Agagite** | /ˈeɪ.gæg.aɪt/ | ISBE (1915) | `æɡədʒaɪt / æɡədʒaɪt` | 0.50 |
| **Eglaim** | /ˈɛg.lə.ɪm/ | ISBE (1915) | `ɐɡleɪm / ɪɡleɪm` | 0.50 |
| **Jehucal** | /dʒi.ˈhjuː.kæl/ | ISBE (1915) | `dʒəhɔkol / dʒəhoʊkəl` | 0.50 |
| **Sivan** | /si.ˈvæn/ | ISBE (1915) | `sɚvɑn / səvɑn` | 0.55 |
| **Kenites** | /ˈkiː.naɪts/ | curated | `` | 0.60 |
| **Beeri** | /bi.ˈiː.raɪ/ | ISBE (1915) | `biɹi / bɪɹi` | 0.60 |
| **Tekoa** | /təˈkoʊ.ə/ | curated | `` | 0.60 |
| **Abanah** | /ˈæb.ə.nə/ | ISBE (1915) | `ɐbænɚ / ɐbænɚ` | 0.60 |
| **Molid** | /ˈmoʊ.lɪd/ | curated | `` | 0.60 |
| **Jaaziel** | /dʒeɪˈeɪ.zi.ɛl/ | curated | `` | 0.64 |
| **Heman** | /ˈhiː.mən/ | curated | `` | 0.67 |
| **Eldaah** | /ɛlˈdeɪ.ə/ | curated | `` | 0.70 |
| **Ashbel** | /ˈæʃ.bɛl/ | curated | `` | 0.70 |
| **Bedan** | /ˈbiː.dæn/ | curated | `` | 0.70 |
| **Adaiah** | /əˈdeɪ.jə/ | curated | `` | 0.70 |
| **Melech** | /ˈmiː.lɛk/ | curated | `` | 0.70 |
| **Zidon** | /ˈzaɪ.dɒn/ | curated | `` | 0.70 |
| **Pharez** | /ˈfɛər.ɛz/ | curated | `` | 0.70 |
| **Mashal** | /ˈmeɪ.ʃæl/ | curated | `` | 0.70 |
| **Ashvath** | /ˈæʃ.væθ/ | curated | `` | 0.70 |
| **Jakim** | /ˈdʒeɪ.kɪm/ | curated | `` | 0.70 |
| **Tarea** | /təˈriː.ə/ | curated | `` | 0.70 |
| **Galal** | /ˈɡeɪ.læl/ | curated | `` | 0.70 |
| **Tizite** | /ˈtaɪ.zaɪt/ | curated | `` | 0.70 |
| **Lubim** | /ˈluː.bɪm/ | curated | `` | 0.70 |
| **Jonan** | /ˈdʒoʊ.næn/ | curated | `` | 0.70 |
| **Paulus** | /ˈpɔː.ləs/ | curated | `` | 0.70 |
| **Rimmono** | /rɪˈmoʊ.noʊ/ | curated | `` | 0.70 |
| **Esau** | /ˈiː.sɔː/ | curated | `` | 0.71 |
| **Malchiel** | /ˈmæl.ki.ɛl/ | curated | `` | 0.71 |
| **Phinehas** | /ˈfɪn.i.əs/ | curated | `` | 0.71 |
| **Shelomith** | /ʃəˈloʊ.mɪθ/ | curated | `` | 0.71 |
| **Jokmeam** | /ˈdʒɒk.mi.æm/ | curated | `` | 0.71 |
| **Johanan** | /dʒoʊˈheɪ.næn/ | curated | `` | 0.71 |
| **Machbenah** | /mækˈbiː.nə/ | curated | `` | 0.71 |
| **Joshibiah** | /ˌdʒɒʃ.ɪˈbaɪ.ə/ | curated | `` | 0.71 |
| **Jeaterai** | /dʒiːˈæt.ə.raɪ/ | curated | `` | 0.71 |
| **Baaseiah** | /ˌbeɪ.əˈsiː.jə/ | curated | `` | 0.71 |
| **Birzaith** | /bərˈzeɪ.ɪθ/ | curated | `` | 0.71 |
| **Ahiezer** | /ˌeɪ.haɪˈiː.zər/ | curated | `` | 0.71 |
| **Haruphite** | /həˈruː.faɪt/ | curated | `` | 0.71 |
| **Machbanai** | /ˈmæk.bə.naɪ/ | curated | `` | 0.71 |
| **Rehabiah** | /ˌriː.həˈbaɪ.ə/ | curated | `` | 0.71 |
| **Asuppim** | /əˈsʌp.ɪm/ | curated | `` | 0.71 |
| **Abilene** | /ˌæb.ɪˈliː.ni/ | curated | `` | 0.71 |
| **Candace** | /ˈkæn.də.siː/ | curated | `` | 0.71 |
| **Sopater** | /ˈsoʊ.pə.tər/ | curated | `` | 0.71 |
| **Salmone** | /sælˈmoʊ.ni/ | curated | `` | 0.71 |
| **Publius** | /ˈpʌb.li.əs/ | curated | `` | 0.71 |
| **Hazar-shual** | /ˌheɪ.zɑːrˈʃuː.əl/ | curated | `` | 0.72 |
| **Mecherathite** | /məˈkɛr.ə.θaɪt/ | curated | `` | 0.72 |
| **Dalaiah** | /dəˈleɪ.ə/ | curated | `` | 0.73 |
| **Shimri** | /ˈʃɪm.raɪ/ | curated | `` | 0.73 |
| **Hilen** | /ˈhaɪ.lɛn/ | curated | `` | 0.73 |
| **Ahiah** | /əˈhaɪ.ə/ | curated | `` | 0.73 |
| **Ismaiah** | /ɪzˈmaɪ.ə/ | curated | `` | 0.73 |
| **Kushaiah** | /kuːˈʃaɪ.ə/ | curated | `` | 0.73 |
| **Ornan** | /ˈɔːr.næn/ | curated | `` | 0.73 |
| **Beth-rapha** | /bɛθˈreɪ.fə/ | curated | `` | 0.74 |
| **Epher** | /ˈiː.fər/ | curated | `` | 0.75 |
| **Eder** | /ˈiː.dər/ | curated | `` | 0.75 |
| **Ezer** | /ˈiː.zər/ | curated | `` | 0.75 |
| **Gera** | /ˈɡɪər.ə/ | curated | `` | 0.75 |
| **Mahli** | /ˈmɑː.laɪ/ | curated | `` | 0.75 |
| **Gaddi** | /ˈgæd.aɪ/ | ISBE (1915) | `` | 0.75 |
| **Eran** | /ˈiː.ræn/ | ISBE (1915) | `` | 0.75 |
| **Meon** | /ˈmiː.ɒn/ | curated | `` | 0.75 |
| **Addar** | /ˈæd.ɑːr/ | curated | `` | 0.75 |
| **Ezem** | /ˈiː.zɛm/ | curated | `` | 0.75 |
| **Joash** | /ˈdʒoʊ.æʃ/ | curated | `` | 0.75 |
| **Ithream** | /ˈɪθ.ri.æm/ | curated | `` | 0.75 |
| **Eliphelet** | /ɪˈlɪf.ə.lɛt/ | curated | `` | 0.75 |
| **Jaare-Oregim** | /ˈdʒeɪ.ə.ri.ɔːr.i.dʒɪm/ | ISBE (1915) | `` | 0.75 |
| **Ezar** | /ˈiː.zɑːr/ | curated | `` | 0.75 |
| **Ashur** | /ˈæʃ.ər/ | curated | `` | 0.75 |
| **Ataroth** | /ˈæt.ə.rɒθ/ | curated | `` | 0.75 |
| **Shealtiel** | /ʃiˈæl.ti.ɛl/ | curated | `` | 0.75 |
| **Hoshama** | /ˈhɒʃ.ə.mə/ | curated | `` | 0.75 |
| **Malchiram** | /mælˈkaɪ.rəm/ | curated | `` | 0.75 |
| **Rephaiah** | /rəˈfeɪ.jə/ | curated | `` | 0.75 |
| **Rapha** | /ˈreɪ.fə/ | curated | `` | 0.75 |
| **Socho** | /ˈsoʊ.koʊ/ | curated | `` | 0.75 |
| **Jeshohaiah** | /ˌdʒɛʃ.oʊˈheɪ.jə/ | curated | `` | 0.75 |
| **Tilgath-pilneser** | /ˌtɪl.ɡæθ.pɪlˈniː.zər/ | curated | `` | 0.75 |
| **Jorai** | /ˈdʒɔːr.aɪ/ | curated | `` | 0.75 |
| **Jeshishai** | /dʒəˈʃɪʃ.aɪ/ | curated | `` | 0.75 |
| **Meraioth** | /məˈreɪ.ɒθ/ | curated | `` | 0.75 |
| **Zerahiah** | /ˌzɛr.əˈhaɪ.ə/ | curated | `` | 0.75 |
| **Hukok** | /ˈhjuː.kɒk/ | curated | `` | 0.75 |
| **Jahziel** | /ˈdʒɑː.zi.ɛl/ | curated | `` | 0.75 |
| **Aramitess** | /ˈɛər.əm.aɪ.tɛs/ | curated | `` | 0.75 |
| **Japhlet** | /ˈdʒæf.lɛt/ | curated | `` | 0.75 |
| **Nohah** | /ˈnoʊ.hə/ | curated | `` | 0.75 |
| **Shaharaim** | /ˌʃeɪ.həˈreɪ.ɪm/ | curated | `` | 0.75 |
| **Elpaal** | /ɛlˈpeɪ.əl/ | curated | `` | 0.75 |
| **Eshek** | /ˈiː.ʃɛk/ | curated | `` | 0.75 |
| **Imri** | /ˈɪm.raɪ/ | curated | `` | 0.75 |
| **Shilonites** | /ˈʃaɪ.lə.naɪts/ | curated | `` | 0.75 |
| **Ahohite** | /əˈhoʊ.haɪt/ | curated | `` | 0.75 |
| **Ribai** | /ˈraɪ.baɪ/ | curated | `` | 0.75 |
| **Gaash** | /ˈɡeɪ.æʃ/ | curated | `` | 0.75 |
| **Ezbai** | /ˈɛz.baɪ/ | curated | `` | 0.75 |
| **Shama** | /ˈʃeɪ.mə/ | curated | `` | 0.75 |
| **Ithmah** | /ˈɪθ.mə/ | curated | `` | 0.75 |
| **Jeziel** | /ˈdʒiː.zi.ɛl/ | curated | `` | 0.75 |
| **Perez-uzza** | /ˌpɛr.ɛzˈʌz.ə/ | curated | `` | 0.75 |
| **Tyre** | /taɪər/ | curated | `` | 0.75 |
| **Jehiel** | /dʒəˈhaɪ.ɛl/ | curated | `` | 0.75 |
| **Alamoth** | /ˈæl.ə.mɒθ/ | curated | `` | 0.75 |
| **Lahmi** | /ˈlɑː.maɪ/ | curated | `` | 0.75 |
| **Haziel** | /ˈheɪ.zi.ɛl/ | curated | `` | 0.75 |
| **Zina** | /ˈzaɪ.nə/ | curated | `` | 0.75 |
| **Jehezkel** | /dʒəˈhɛz.kɛl/ | curated | `` | 0.75 |
| **Shubael** | /ˈʃuː.beɪ.ɛl/ | curated | `` | 0.75 |
| **Izharites** | /ˈɪz.hɑːr.aɪts/ | curated | `` | 0.75 |
| **Ibri** | /ˈɪb.raɪ/ | curated | `` | 0.75 |
| **Zerahites** | /ˈzɛr.ə.haɪts/ | curated | `` | 0.75 |
| **Ezri** | /ˈɛz.raɪ/ | curated | `` | 0.75 |
| **Hushai** | /ˈhuː.ʃaɪ/ | curated | `` | 0.75 |
| **Ramah** | /ˈreɪ.mə/ | curated | `` | 0.75 |
| **Ijon** | /ˈaɪ.dʒɒn/ | curated | `` | 0.75 |
| **Maim** | /ˈmeɪ.ɪm/ | curated | `` | 0.75 |
| **Rama** | /ˈreɪ.mə/ | curated | `` | 0.75 |
| **Asheroth** | /ˈæʃ.ə.rɒθ/ | curated | `` | 0.75 |
| **Hozai** | /ˈhoʊ.zaɪ/ | curated | `` | 0.75 |
| **Carchemish** | /ˈkɑːr.kə.mɪʃ/ | curated | `` | 0.75 |
| **Ulai** | /ˈjuː.laɪ/ | ISBE (1915) | `` | 0.75 |
| **Caiaphas** | /ˈkeɪ.ə.fəs/ | curated | `` | 0.75 |
| **Esli** | /ˈɛs.laɪ/ | curated | `` | 0.75 |
| **Sosthenes** | /ˈsɒs.θə.niːz/ | curated | `` | 0.75 |
| **Trogyllium** | /troʊˈdʒɪl.i.əm/ | curated | `` | 0.75 |
| **Castor** | /ˈkæs.tər/ | curated | `` | 0.75 |
| **Hazzelelponi** | /ˌhæz.ə.lɛlˈpoʊ.naɪ/ | curated | `` | 0.77 |
| **Hizkiah** | /hɪzˈkaɪ.ə/ | curated | `` | 0.77 |
| **Iphedeiah** | /ˌɪf.ɪˈdiː.ə/ | curated | `` | 0.77 |
| **Zaanan** | /ˈzeɪ.ə.næn/ | ISBE (1915) | `` | 0.77 |
| **Jehallelel** | /dʒəˈhæl.ə.lɛl/ | curated | `` | 0.78 |
| **Jehozabad** | /dʒəˈhɒz.ə.bæd/ | curated | `` | 0.78 |
| **Jeremoth** | /ˈdʒɛr.ə.mɒθ/ | curated | `` | 0.79 |
| **Beth-shean** | /bɛθˈʃiː.ən/ | curated | `` | 0.79 |
| **Kabzeel** | /ˈkæb.zi.ɛl/ | curated | `` | 0.79 |
| **Jozabad** | /ˈdʒɒz.ə.bæd/ | curated | `` | 0.79 |
| **Zabdiel** | /ˈzæb.di.ɛl/ | curated | `` | 0.79 |
| **Ehi** | /ˈiː.haɪ/ | ISBE (1915) | `` | 0.88 |
| **Amalekite** | /ə.ˈmæl.i.kaɪt/ | ISBE (1915) | `` | 0.88 |
| **Galeed** | /ˈgæl.i.ɛd/ | ISBE (1915) | `` | 1.00 |
| **Minni** | /ˈmɪn.aɪ/ | ISBE (1915) | `` | 1.00 |

## Overrides that still carry a pure-vowel hyphen segment

Pre-existing hand-tuned spellings the automated repair did not touch. The scorer cannot judge these — only the ear can.

| Name | Say |
| --- | --- |
| Achaia | `a-KAY-uh` |
| Amariah | `am-a-REYE-uh` |
| Baara | `BAY-a-ruh` |
| Beracah | `BEHR-a-kuh` |
| Berachah | `BEHR-a-kuh` |
| Bethsaida | `behth-SAY-i-duh` |
| Cenchreae | `sehn-KREE-ee` |
| Eliel | `EE-lee-ehll` |
| Eliphelehu | `i-lihf-uh-LEE-hoo` |
| Ephron | `EE-fron` |
| Jaalam | `JAY-a-lam` |
| Jehoshabeath | `jee-hoh-SHAB-ee-athh` |
| Maachah | `MAY-a-kuh` |
| Naarah | `NAY-a-ruh` |
| Syracuse | `SIHR-a-kyooz` |

## Unsure — 162 names still on a generated guess

No entry in ISBE, CMUdict, Wiktionary or Wikipedia. A low score here is as likely to mean the guess is wrong as the voice. Closing these means listening.

---

_Generated by `regen_pronunciation_todo.py` from a whole-canon verifier sweep of the WEB text (1189 chapters, voice en-US-AndrewNeural). Scores are two-carrier averages._
