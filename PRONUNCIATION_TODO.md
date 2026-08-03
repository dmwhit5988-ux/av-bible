# Pronunciation to-do — whole canon

Every proper noun in the WEB text has now been checked against real audio. The list holds 3327 names; this file is what checking could **not** settle.

| Verdict | Names |
| --- | --- |
| unchecked | 0 |
| fine as spelled | 1303 |
| overridden | 516 |
| suggestion waiting | 133 |
| still wrong | 384 |
| unsure (guessed IPA) | 991 |

## How much to trust each of these

The reference each name is judged against is not equally solid, and the file records which is which in `ipa_src`:

| Reference | Names | Meaning |
| --- | --- | --- |
| curated | 1830 | already in your list, or authored by hand |
| cmudict | 232 | from the CMU Pronouncing Dictionary |
| generated | 1265 | a rule-based guess — see below |

**The generated guesses are weaker than the voice they judge.** Measured against the 1570 references that predate this work, the generator agrees 0.72 of the time; the neural voice manages 0.77 against those same references. So where a guessed reference and the voice disagree, the guess is the more likely culprit. Those names are marked **unsure** rather than wrong, and no override was ever applied on a guess alone.

## Still wrong — worth acting on

Judged against a curated or CMUdict reference, so the disagreement is real. No respelling tried has fixed these.

| Name | Reference | Voice says | Score |
| --- | --- | --- | --- |
| **Puah** | /ˈpjuː.ə/ | `` | 0.25 |
| **Coos** | /ˈkoʊ.ɒs/ | `` | 0.25 |
| **Shallecheth** | /ˈʃæl.ə.kɛθ/ | `` | 0.29 |
| **Beer** | /bˈɪr/ | `bi / bi` | 0.33 |
| **Roi** | /rˈɔɪ/ | `ɹoɪ / ɹoɪ` | 0.33 |
| **Ain** | /ˈeɪ.ɪn/ | `` | 0.33 |
| **Pul** | /pʌl/ | `` | 0.33 |
| **Bathshua** | /bæθˈʃuː.ə/ | `` | 0.33 |
| **Ahi** | /ˈeɪ.haɪ/ | `` | 0.33 |
| **Tokhath** | /ˈtɒk.hæθ/ | `toʊkeɪð / toʊkeɪð` | 0.33 |
| **Jediael** | /dʒəˈdaɪ.eɪ.ɛl/ | `` | 0.36 |
| **Amal** | /ˈeɪ.mæl/ | `` | 0.38 |
| **Beri** | /ˈbɪər.aɪ/ | `` | 0.38 |
| **Shephuphan** | /ʃəˈfjuː.fæn/ | `` | 0.38 |
| **Hadar** | /hˈædɚ/ | `hɐdɔ / hɐdɔ` | 0.40 |
| **Goshen** | /ɡˈoʊʃɪn/ | `is / ɡoʊʃən` | 0.40 |
| **Barak** | /bˈɑrək/ | `ɹɑk / ɐɹɑk` | 0.40 |
| **Hillel** | /hɪlˈɛl/ | `hɐloʊ / hɐloʊ` | 0.40 |
| **Kir** | /kˈɪr/ | `keɪaɪɔɹ / keɪaɪɔɹ` | 0.40 |
| **Igeal** | /ˈɪɡ.i.əl/ | `` | 0.40 |
| **Asiel** | /ˈeɪ.si.ɛl/ | `` | 0.40 |
| **Jeiel** | /dʒəˈaɪ.əl/ | `` | 0.40 |
| **Isuah** | /ˈɪs.ju.ə/ | `` | 0.40 |
| **Baasha** | /ˈbeɪ.ə.ʃə/ | `bɑʃɑ / bɑʃɑ` | 0.40 |
| **Cephas** | /sˈɛfəz/ | `sifæs / sifæs` | 0.40 |
| **Melchizedek** | /mɛkˈiːzɛdɛk/ | `i / mɛlkɪzədɛk` | 0.41 |
| **Shimeath** | /ˈʃɪm.i.æθ/ | `ʃaɪmɪð / ʃaɪmɪθ` | 0.42 |
| **Aquila** | /ˈæk.wɪ.lə/ | `` | 0.42 |
| **Ithrites** | /ˈɪθ.raɪts/ | `` | 0.43 |
| **Chenaniah** | /ˌkɛn.əˈnaɪ.ə/ | `` | 0.43 |
| **Giddalti** | /ɡɪˈdæl.taɪ/ | `` | 0.43 |
| **Eliakim** | /ɪˈlaɪ.ə.kɪm/ | `ɛliɑkim / ɛliɑkim` | 0.43 |
| **Jesimiel** | /dʒəˈsɪm.i.ɛl/ | `` | 0.44 |
| **Pas-dammim** | /pæsˈdæm.ɪm/ | `` | 0.44 |
| **Anetothite** | /əˈnɛt.ə.θaɪt/ | `` | 0.44 |
| **Mattathias** | /ˌmæt.əˈθaɪ.əs/ | `mətæfi / mətæθiəs` | 0.44 |
| **Baal-hanan** | /ˌbeɪ.əlˈheɪ.næn/ | `` | 0.44 |
| **Jehaleleel** | /dʒɪˈhæl.ɪ.liːl/ | `` | 0.44 |
| **Eliada** | /ɪˈlaɪ.ə.də/ | `` | 0.46 |
| **Phanuel** | /fəˈnjuː.ɛl/ | `vænjuwəl / fænuwəl` | 0.46 |
| **Attalia** | /ˌæt.əˈlaɪ.ə/ | `` | 0.46 |
| **Canaanite** | /kˈeɪnənaɪt/ | `hisɛ / keɪnənaɪt` | 0.50 |
| **Guni** | /ˈɡjuː.naɪ/ | `` | 0.50 |
| **Igal** | /ˈaɪ.ɡæl/ | `` | 0.50 |
| **Arad** | /ˈɛər.æd/ | `` | 0.50 |
| **Aven** | /ɑvˈeɪn/ | `eɪvən / eɪvən` | 0.50 |
| **Shual** | /ˈʃuː.əl/ | `` | 0.50 |
| **Ashan** | /ˈeɪ.ʃæn/ | `` | 0.50 |
| **Ahimaaz** | /əˈhɪm.eɪ.æz/ | `` | 0.50 |
| **Ahinoam** | /əˈhɪn.oʊ.æm/ | `` | 0.50 |
| **Ner** | /nɜːr/ | `` | 0.50 |
| **Gai** | /ɡˈeɪ/ | `ɡaɪ / ɡaɪ` | 0.50 |
| **Asaph** | /ˈeɪ.sæf/ | `` | 0.50 |
| **Asaiah** | /əˈseɪ.jə/ | `` | 0.50 |
| **Ephratah** | /ˈɛf.rə.tɑː/ | `` | 0.50 |
| **Kirjath-jearim** | /ˌkɜːr.dʒæθˈdʒiː.ə.rɪm/ | `` | 0.50 |
| **Bath-shua** | /bæθˈʃuː.ə/ | `` | 0.50 |
| **Naam** | /ˈneɪ.æm/ | `` | 0.50 |
| **Asareel** | /əˈsær.i.ɛl/ | `` | 0.50 |
| **Bithiah** | /bɪˈθaɪ.ə/ | `` | 0.50 |
| **Biri** | /ˈbɪr.aɪ/ | `` | 0.50 |
| **Azaz** | /ˈeɪ.zæz/ | `` | 0.50 |
| **Huri** | /ˈhjʊər.aɪ/ | `` | 0.50 |
| **Anem** | /ˈeɪ.nɛm/ | `` | 0.50 |
| **Hasenuah** | /ˌhæs.ɪˈnjuː.ə/ | `` | 0.50 |
| **Kore** | /ˈkɔːr.i/ | `` | 0.50 |
| **Eliphal** | /ɪˈlaɪ.fæl/ | `` | 0.50 |
| **Hothan** | /ˈhoʊ.θæn/ | `` | 0.50 |
| **Elihu** | /ɪˈlaɪ.hjuː/ | `` | 0.50 |
| **Pelethites** | /ˈpɛl.ə.θaɪts/ | `` | 0.50 |
| **Bukkiah** | /bəˈkaɪ.ə/ | `` | 0.50 |
| **Peulthai** | /piːˈʌl.θaɪ/ | `` | 0.50 |
| **Tebaliah** | /ˌtɛb.əˈlaɪ.ə/ | `` | 0.50 |
| **Jehuel** | /dʒəˈhjuː.ɛl/ | `dʒihʊl / dʒihwəl` | 0.50 |
| **Miniamin** | /mɪˈnaɪ.ə.mɪn/ | `mɛnimin / mɛniæmən` | 0.50 |
| **Ahasuerus** | /əhæʃəwˈɛrəs/ | `ɐhæzjuɹɪs / ɐhæzjuɚɹɪs` | 0.50 |
| **Negev** | /nˈɛɡɛv/ | `nɛdʒəf / nɛdʒəv` | 0.50 |
| **Aramaic** | /ɑrɑmˈɛjɪk/ | `ɛɹəmeɪɪk / ɛɹəmeɪɪk` | 0.50 |
| **Ezekiel** | /ˈɛzɪkiːl/ | `ɪzikɪəl / ɪzikiəl` | 0.50 |
| **Dura** | /dˈʊrə/ | `dʒɚɹə / dʒɚɹə` | 0.50 |
| **Salome** | /səlˈoʊmiː/ | `sɑləmeɪ / sɑləmeɪ` | 0.50 |
| **Semein** | /ˈsɛm.i.ɪn/ | `səmeɪn / səmeɪn` | 0.50 |
| **Bethsphage** | /ˈbɛθ.sfə.dʒiː/ | `vɛθsɪdʒ / vɛθsɪdʒ` | 0.50 |
| **Cleopas** | /ˈkliː.ə.pəs/ | `klioʊpɑ / plioʊpɑ` | 0.50 |
| **Nathanael** | /nˈæθəneɪl/ | `nəθænjəl / nəθænjəl` | 0.50 |
| **Manaen** | /ˈmæn.eɪ.ɛn/ | `` | 0.50 |
| **Melita** | /ˈmɛl.ɪ.tə/ | `` | 0.50 |
| **Puteoli** | /pjuːˈtiː.ə.laɪ/ | `` | 0.50 |
| **Eunice** | /jˈuːnəs/ | `is / junɪs` | 0.50 |
| **Haniel** | /ˈhæn.i.ɛl/ | `` | 0.54 |
| **Jashubilehem** | /dʒəˌʃuː.bɪˈliː.hɛm/ | `` | 0.55 |
| **Oren** | /ˈɔːr.ɛn/ | `` | 0.55 |
| **Aher** | /ˈeɪ.hər/ | `` | 0.55 |
| **Jesiah** | /dʒɪˈsaɪ.ə/ | `` | 0.55 |
| **Jehudijah** | /ˌdʒɛ.hjuːˈdaɪ.dʒə/ | `` | 0.56 |
| **Kirjathaim** | /ˌkɜːr.dʒəˈθeɪ.ɪm/ | `` | 0.56 |
| **Meshelemiah** | /məˌʃɛl.əˈmaɪ.ə/ | `` | 0.56 |
| **Eliehoenai** | /ɪˌlaɪ.ə.hoʊˈiː.naɪ/ | `` | 0.56 |
| **Moabitess** | /ˈmoʊ.ə.baɪ.tɛs/ | `moʊlʊbaɪɾəs / mʌləbaɪɾəs` | 0.56 |
| **Bezaleel** | /bɪˈzæl.i.ɛl/ | `` | 0.56 |
| **Jaareshiah** | /ˌdʒeɪ.ə.rəˈʃaɪ.ə/ | `` | 0.56 |
| **Nethaneel** | /nɪˈθæn.i.ɛl/ | `` | 0.56 |
| **Ramathite** | /ˈreɪ.mə.θaɪt/ | `` | 0.56 |
| **Barsabas** | /ˈbɑːr.sə.bəs/ | `` | 0.56 |
| **Abimael** | /əˈbɪm.eɪ.ɛl/ | `` | 0.57 |
| **Abihail** | /ˌæb.ɪˈheɪ.ɪl/ | `` | 0.57 |
| **Penuel** | /pəˈnjuː.əl/ | `` | 0.57 |
| **Mattaniah** | /ˌmæt.əˈnaɪ.ə/ | `` | 0.57 |
| **Eliashib** | /ɪˈlaɪ.ə.ʃɪb/ | `` | 0.57 |
| **Ahuzam** | /əˈhjuː.zæm/ | `` | 0.57 |
| **Josibiah** | /ˌdʒɒs.ɪˈbaɪ.ə/ | `` | 0.57 |
| **Azareel** | /əˈzær.i.ɛl/ | `` | 0.57 |
| **Danites** | /ˈdæn.aɪts/ | `` | 0.57 |
| **Perazim** | /pəˈreɪ.zɪm/ | `` | 0.57 |
| **Elipheleh** | /ɪˈlɪf.ɪ.lɛ/ | `` | 0.57 |
| **Gedaliah** | /ˌɡɛd.əˈlaɪ.ə/ | `` | 0.57 |
| **Jathniel** | /ˈdʒæθ.ni.ɛl/ | `` | 0.57 |
| **Peullethai** | /piˈʌl.ə.θaɪ/ | `` | 0.57 |
| **Shelemiah** | /ˌʃɛl.əˈmaɪ.ə/ | `` | 0.57 |
| **Jechiliah** | /ˌdʒɛk.ɪˈlaɪ.ə/ | `dʒɐtʃɪlɐ / dʒɐtʃɪliɐ` | 0.57 |
| **Conaniah** | /ˌkɒn.əˈnaɪ.ə/ | `kəneɪniɐ / koʊneɪniɐ` | 0.57 |
| **Tertius** | /tˈɚtiːɪs/ | `tɜʃiəs / tɜʃiəs` | 0.57 |
| **Artemas** | /ˈɑrtɪməz/ | `ɑɹɾəməs / ɑɹdəməs` | 0.57 |
| **Annas** | /ˈæn.əs/ | `` | 0.57 |
| **Hanniel** | /ˈhæn.i.ɛl/ | `` | 0.58 |
| **Aijalon** | /ˈædʒ.ə.lɒn/ | `` | 0.58 |
| **Taanach** | /ˈteɪ.ə.næk/ | `` | 0.58 |
| **Benaiah** | /bəˈneɪ.jə/ | `` | 0.58 |
| **Jezoar** | /dʒɪˈzoʊ.ɑːr/ | `` | 0.58 |
| **Mahalah** | /ˈmæh.ə.lə/ | `` | 0.58 |
| **Eleadah** | /ˌɛl.iˈeɪ.də/ | `` | 0.58 |
| **Shimeam** | /ˈʃɪm.i.æm/ | `` | 0.58 |
| **Anthothijah** | /ˌæn.θoʊˈθaɪ.dʒə/ | `` | 0.59 |
| **Immanuel** | /ˈɪmənʊl/ | `ɪmænuwɛl / ɪmænjuwɛl` | 0.59 |
| **Dothan** | /dˈɑθən/ | `doʊθɪn / dʒoʊθən` | 0.60 |
| **Hormah** | /ˈhɔːr.mə/ | `` | 0.60 |
| **Balak** | /bɑlək/ | `bælɪk / bælɪk` | 0.60 |
| **Racal** | /rˈækəl/ | `ɹeɪsəl / ɹeɪsəl` | 0.60 |
| **Bunah** | /ˈbjuː.nə/ | `` | 0.60 |
| **Eker** | /ˈiː.kər/ | `` | 0.60 |
| **Ephlal** | /ˈɛf.læl/ | `` | 0.60 |
| **Reaiah** | /riˈeɪ.jə/ | `` | 0.60 |
| **Adiel** | /ˈeɪ.di.ɛl/ | `` | 0.60 |
| **Ishuai** | /ˈɪʃ.ju.aɪ/ | `` | 0.60 |
| **Maasai** | /ˈmeɪ.ə.saɪ/ | `` | 0.60 |
| **Tobadonijah** | /ˌtɒb.æd.oʊˈnaɪ.dʒə/ | `toʊbədɑnɪdʒə / toʊbədɑnɪdʒɐ` | 0.60 |
| **Hosea** | /hoʊsˈiːə/ | `hoʊzeɪɐ / hoʊzeɪɐ` | 0.60 |
| **Salim** | /sˈælɪm/ | `səlim / səlim` | 0.60 |
| **Deity** | /dˈiːətiː/ | `diɪɾi / diɪɾi` | 0.60 |
| **Mattithiah** | /ˌmæt.ɪˈθaɪ.ə/ | `` | 0.61 |
| **Hammolecheth** | /hæˈmɒl.ə.kɛθ/ | `` | 0.61 |
| **Hammoleketh** | /həˈmɒl.ɪ.kɛθ/ | `` | 0.61 |
| **Gennesaret** | /ɡəˈnɛs.ə.rɛt/ | `dʒɛnəsɚɹɛt / dʒɛnɪsɚɹɛd` | 0.61 |
| **Shuthelah** | /ʃuːˈθiː.lə/ | `` | 0.62 |
| **Adalia** | /ɑdˈɑliːə/ | `ɐdeɪliɐl / ɐdeɪliɐ` | 0.62 |
| **Assir** | /ˈæs.ər/ | `` | 0.62 |
| **YAHWEH** | /jˈɑwɛ/ | `jaʊweɪ / jɑweɪ` | 0.62 |
| **Shean** | /ˈʃiː.æn/ | `` | 0.62 |
| **Eglah** | /ˈɛɡ.lə/ | `` | 0.62 |
| **Caphthorim** | /ˈkæf.θɔː.rɪm/ | `` | 0.62 |
| **Aliah** | /əˈlaɪ.ə/ | `` | 0.62 |
| **Shimeathites** | /ˈʃɪm.i.ə.θaɪts/ | `` | 0.62 |
| **Ziza** | /ˈzaɪ.zə/ | `` | 0.62 |
| **Amzi** | /ˈæm.zaɪ/ | `` | 0.62 |
| **Uzzen-sherah** | /ˌʌz.ɛnˈʃɪər.ə/ | `` | 0.62 |
| **Anathothite** | /ˈæn.ə.θɒθ.aɪt/ | `` | 0.62 |
| **Shiza** | /ˈʃaɪ.zə/ | `` | 0.62 |
| **Aram-maacah** | /ˌɛər.əm ˈmeɪ.ə.kə/ | `` | 0.62 |
| **Eloth** | /ˈiː.lɒθ/ | `ɐlɑf / ɐlɑθ` | 0.62 |
| **Cana** | /kˈænə/ | `tɑnə / kɑnɐ` | 0.62 |
| **Mitylene** | /ˌmɪt.ɪˈliː.ni/ | `` | 0.62 |
| **Orion** | /oʊrˈaɪən/ | `ɚɹaɪn / wɜɹaɪən` | 0.63 |
| **Beroea** | /bəˈriː.ə/ | `` | 0.63 |
| **Caleb-ephratah** | /ˌkeɪ.lɛbˈɛf.rə.tɑː/ | `` | 0.64 |
| **Menahem** | /mənˈɑhəm/ | `menɐhʊm / menəhəm` | 0.64 |
| **Thyatira** | /ˌθaɪ.əˈtaɪ.rə/ | `` | 0.64 |
| **Cenchrea** | /ˈsɛŋ.krɪ.ə/ | `` | 0.64 |
| **Jethro** | /dʒˈɛθroʊ/ | `dʒɛfɚɹə / dʒɛfɹoʊ` | 0.65 |
| **Euroclydon** | /jʊˈrɒk.lɪ.dɒn/ | `` | 0.65 |
| **Gath-rimmon** | /ɡæθˈrɪm.ɒn/ | `` | 0.65 |
| **Cush** | /kʌʃ/ | `` | 0.67 |
| **Cain** | /keɪn/ | `` | 0.67 |
| **Seth** | /sɛθ/ | `` | 0.67 |
| **Ham** | /hæm/ | `` | 0.67 |
| **Put** | /pʌt/ | `` | 0.67 |
| **Zeboim** | /zɪˈboʊ.ɪm/ | `` | 0.67 |
| **Hul** | /hʌl/ | `` | 0.67 |
| **Dan** | /dæn/ | `` | 0.67 |
| **Almighty** | /ɔlmˈaɪtiː/ | `ɔmaɪɾi / ɔmaɪɾi` | 0.67 |
| **Kiriath** | /ˈkɪr.i.æθ/ | `` | 0.67 |
| **Luz** | /lˈəz/ | `luz / luz` | 0.67 |
| **Benoni** | /bɛnˈoʊniː/ | `bənoʊnaɪ / bənoʊnaɪ` | 0.67 |
| **Oholibamah** | /oʊˌhɒl.ɪˈbɑː.mə/ | `` | 0.67 |
| **Aiah** | /eɪˈaɪ.ə/ | `` | 0.67 |
| **Husham** | /ˈhjuː.ʃəm/ | `` | 0.67 |
| **Abihu** | /əˈbaɪ.hjuː/ | `` | 0.67 |
| **Hur** | /hɜːr/ | `` | 0.67 |
| **Ar** | /ˈɑr/ | `eɪɔɹ / eɪɑɹ` | 0.67 |
| **Asriel** | /ˈæs.ri.ɛl/ | `` | 0.67 |
| **Dor** | /dɔːr/ | `` | 0.67 |

_…and 184 more; filter to "Still wrong" in the Pronunciation Studio for the full set._

## Suggestions waiting

A better spelling is known but was not applied, because the plain reading was close enough that the disagreement may be the transcriber's error.

| Name | Reference | Voice says | Score |
| --- | --- | --- | --- |
| Jarha | /ˈdʒɑːr.hə/ | `` | 0.40 |
| Kenites | /ˈkiː.naɪts/ | `` | 0.60 |
| Tekoa | /təˈkoʊ.ə/ | `` | 0.60 |
| Molid | /ˈmoʊ.lɪd/ | `` | 0.60 |
| Jaaziel | /dʒeɪˈeɪ.zi.ɛl/ | `` | 0.64 |
| Heman | /ˈhiː.mən/ | `` | 0.67 |
| Eldaah | /ɛlˈdeɪ.ə/ | `` | 0.70 |
| Ashbel | /ˈæʃ.bɛl/ | `` | 0.70 |
| Bedan | /ˈbiː.dæn/ | `` | 0.70 |
| Adaiah | /əˈdeɪ.jə/ | `` | 0.70 |
| Melech | /ˈmiː.lɛk/ | `` | 0.70 |
| Zidon | /ˈzaɪ.dɒn/ | `` | 0.70 |
| Pharez | /ˈfɛər.ɛz/ | `` | 0.70 |
| Mashal | /ˈmeɪ.ʃæl/ | `` | 0.70 |
| Ashvath | /ˈæʃ.væθ/ | `` | 0.70 |
| Jakim | /ˈdʒeɪ.kɪm/ | `` | 0.70 |
| Tarea | /təˈriː.ə/ | `` | 0.70 |
| Galal | /ˈɡeɪ.læl/ | `` | 0.70 |
| Tizite | /ˈtaɪ.zaɪt/ | `` | 0.70 |
| Lubim | /ˈluː.bɪm/ | `lʊbəm / lɪbəm` | 0.70 |
| Jonan | /ˈdʒoʊ.næn/ | `dʒoʊnɪn / dʒoʊnɪ` | 0.70 |
| Paulus | /ˈpɔː.ləs/ | `` | 0.70 |
| Rimmono | /rɪˈmoʊ.noʊ/ | `` | 0.70 |
| Esau | /ˈiː.sɔː/ | `` | 0.71 |
| Malchiel | /ˈmæl.ki.ɛl/ | `` | 0.71 |
| Phinehas | /ˈfɪn.i.əs/ | `` | 0.71 |
| Shelomith | /ʃəˈloʊ.mɪθ/ | `` | 0.71 |
| Jokmeam | /ˈdʒɒk.mi.æm/ | `` | 0.71 |
| Johanan | /dʒoʊˈheɪ.næn/ | `` | 0.71 |
| Machbenah | /mækˈbiː.nə/ | `` | 0.71 |
| Joshibiah | /ˌdʒɒʃ.ɪˈbaɪ.ə/ | `` | 0.71 |
| Jeaterai | /dʒiːˈæt.ə.raɪ/ | `` | 0.71 |
| Baaseiah | /ˌbeɪ.əˈsiː.jə/ | `` | 0.71 |
| Birzaith | /bərˈzeɪ.ɪθ/ | `` | 0.71 |
| Ahiezer | /ˌeɪ.haɪˈiː.zər/ | `` | 0.71 |
| Haruphite | /həˈruː.faɪt/ | `` | 0.71 |
| Machbanai | /ˈmæk.bə.naɪ/ | `` | 0.71 |
| Rehabiah | /ˌriː.həˈbaɪ.ə/ | `` | 0.71 |
| Asuppim | /əˈsʌp.ɪm/ | `` | 0.71 |
| Abilene | /ˌæb.ɪˈliː.ni/ | `æbəllin / æbəllin` | 0.71 |
| Candace | /ˈkæn.də.siː/ | `` | 0.71 |
| Sopater | /ˈsoʊ.pə.tər/ | `` | 0.71 |
| Salmone | /sælˈmoʊ.ni/ | `` | 0.71 |
| Publius | /ˈpʌb.li.əs/ | `` | 0.71 |
| Hazar-shual | /ˌheɪ.zɑːrˈʃuː.əl/ | `` | 0.72 |
| Mecherathite | /məˈkɛr.ə.θaɪt/ | `` | 0.72 |
| Dalaiah | /dəˈleɪ.ə/ | `` | 0.73 |
| Shimri | /ˈʃɪm.raɪ/ | `` | 0.73 |
| Hilen | /ˈhaɪ.lɛn/ | `` | 0.73 |
| Ahiah | /əˈhaɪ.ə/ | `` | 0.73 |
| Ismaiah | /ɪzˈmaɪ.ə/ | `` | 0.73 |
| Kushaiah | /kuːˈʃaɪ.ə/ | `` | 0.73 |
| Ornan | /ˈɔːr.næn/ | `` | 0.73 |
| Beth-rapha | /bɛθˈreɪ.fə/ | `` | 0.74 |
| Epher | /ˈiː.fər/ | `` | 0.75 |
| Eder | /ˈiː.dər/ | `` | 0.75 |
| Ezer | /ˈiː.zər/ | `` | 0.75 |
| Gera | /ˈɡɪər.ə/ | `` | 0.75 |
| Mahli | /ˈmɑː.laɪ/ | `` | 0.75 |
| Meon | /ˈmiː.ɒn/ | `` | 0.75 |
| Addar | /ˈæd.ɑːr/ | `` | 0.75 |
| Ezem | /ˈiː.zɛm/ | `` | 0.75 |
| Joash | /ˈdʒoʊ.æʃ/ | `` | 0.75 |
| Ithream | /ˈɪθ.ri.æm/ | `` | 0.75 |
| Eliphelet | /ɪˈlɪf.ə.lɛt/ | `` | 0.75 |
| Ezar | /ˈiː.zɑːr/ | `` | 0.75 |
| Ashur | /ˈæʃ.ər/ | `` | 0.75 |
| Ataroth | /ˈæt.ə.rɒθ/ | `` | 0.75 |
| Shealtiel | /ʃiˈæl.ti.ɛl/ | `` | 0.75 |
| Hoshama | /ˈhɒʃ.ə.mə/ | `` | 0.75 |
| Malchiram | /mælˈkaɪ.rəm/ | `` | 0.75 |
| Rephaiah | /rəˈfeɪ.jə/ | `` | 0.75 |
| Rapha | /ˈreɪ.fə/ | `` | 0.75 |
| Socho | /ˈsoʊ.koʊ/ | `` | 0.75 |
| Jeshohaiah | /ˌdʒɛʃ.oʊˈheɪ.jə/ | `` | 0.75 |
| Tilgath-pilneser | /ˌtɪl.ɡæθ.pɪlˈniː.zər/ | `` | 0.75 |
| Jorai | /ˈdʒɔːr.aɪ/ | `` | 0.75 |
| Jeshishai | /dʒəˈʃɪʃ.aɪ/ | `` | 0.75 |
| Meraioth | /məˈreɪ.ɒθ/ | `` | 0.75 |
| Zerahiah | /ˌzɛr.əˈhaɪ.ə/ | `` | 0.75 |

## Unsure — needs an ear, not another sweep

991 names whose only reference is a rule-based guess. A low score here is as likely to mean the guess is wrong as the voice. The worst are listed; the Studio's "Unsure (guessed IPA)" filter shows them all.

| Name | Guessed reference | Voice says | Score |
| --- | --- | --- | --- |
| Iye | /ˈi.ə.iː/ | `aɪ / aɪ` | 0.00 |
| Ahzai | /ˈeɪ.zeɪ/ | `aʊsaɪ / aʊtsaɪ` | 0.00 |
| Shuphamites | /ʃəˈfeɪ.mi.təs/ | `ʃɑpɛðəmaɪt / ʃɛpæðəmaɪt` | 0.11 |
| Berites | /ˈbiː.ri.təs/ | `vuɹaɪɾiz / vɪɹaɪɾiz` | 0.14 |
| Idumaea | /iˈdjuː.mə.iː/ | `eɪdʒɐmiɐ / eɪdʒəmiɐ` | 0.14 |
| Hor | /ˈhɒr/ | `hoʊ / pu` | 0.17 |
| Berothai | /ˈbiː.rə.θeɪ/ | `vɛɹoʊtaɪ / vɛɹoʊtaɪ` | 0.17 |
| Toi | /ˈtɔɪ/ | `toɪ / soɪ` | 0.17 |
| Hiel | /ˈhaɪl/ | `ɡi / hi` | 0.17 |
| Aiath | /ˈeɪ.əθ/ | `aɪɐv / aɪɪð` | 0.17 |
| Giloh | /ˈɡi.ləh/ | `dʒaɪloʊ / dʒaɪloʊ` | 0.20 |
| Cabul | /ˈseɪ.bəl/ | `kɐbu / kəboʊ` | 0.20 |
| Ithlah | /ˈi.θləh/ | `ɪfloʊ / ɪflaɪ` | 0.20 |
| Uriah | /əˈri.əh/ | `juɹaɪɐ / juɹaɪɐ` | 0.20 |
| Necoh | /ˈniː.səh/ | `nɛkoʊ / nɛkoʊ` | 0.20 |
| Uphaz | /ˈjuː.fəz/ | `ʌphæz / ʌphæz` | 0.20 |
| Pau | /ˈpɔː/ | `paʊ / haʊ` | 0.25 |
| Sion | /ˈsi.ən/ | `ʃaʊn / ʃaʊn` | 0.25 |
| Giah | /ˈɡi.əh/ | `dʒaɪɚ / dʒaɪɐ` | 0.25 |
| Arieh | /ˈeɪ.raɪh/ | `ɑɹɹiɐ / ɑɹɹiɐ` | 0.25 |
| Bezai | /ˈbiː.zeɪ/ | `vɛzaɪ / vɛzaɪ` | 0.25 |
| Jahzeiah | /dʒəˈzaɪ.əh/ | `dʒɑsiɚ / dʒɑtsiə` | 0.25 |
| Athlai | /ˈeɪ.θleɪ/ | `æflaɪ / æflaɪ` | 0.25 |
| Shashai | /ˈʃeɪ.ʃeɪ/ | `ʃɑsaɪ / ʃɑsaɪ` | 0.25 |
| Elul | /ˈiː.ləl/ | `ɛloʊ / ɛloʊ` | 0.25 |
| Pathros | /ˈpeɪ.θrəs/ | `hæfɹoʊs / hæfɹoʊz` | 0.25 |
| Ulai | /ˈjuː.leɪ/ | `boʊlɛ / boʊlɛ` | 0.25 |
| Quartus | /ˈkjuː.ər.təs/ | `pɔɹdᵻ / kɔɹdɪs` | 0.25 |
| Aretas | /ˈeɪ.rə.təs/ | `ɚɹɛdəz / ɚɹɛdᵻz` | 0.25 |
| Raamses | /ˈreɪ.əm.səs/ | `ɹæmzɪz / ɹæmzɪz` | 0.29 |
| Eliasaph | /əˈli.ə.səf/ | `ɪlaɪzæf / ɪlaɪzæf` | 0.29 |
| Belaites | /ˈbiː.leɪ.təs/ | `vɛləaɪts / vɛləaɪts` | 0.29 |
| Geliloth | /ˈɡiː.li.ləθ/ | `dʒɛləlɑf / dʒɛloʊlɑf` | 0.29 |
| Paltite | /ˈpæl.ti.tiː/ | `pɑldaɪd / pɑldaɪd` | 0.29 |
| Jedidah | /ˈdʒiː.di.dəh/ | `dʒɛɾədɐ / s` | 0.29 |
| Agagite | /əˈɡeɪ.ɡi.tiː/ | `æɡədʒaɪt / æɡədʒaɪt` | 0.29 |
| Thaddaeus | /ˈθæd.də.juːs/ | `ðæɾɪz / ðæɾɪz` | 0.29 |
| Timaeus | /ˈti.mə.juːs/ | `tɪmiəz / tɪmiəz` | 0.29 |
| Hattaavah | /hətˈteɪ.ə.vəh/ | `hædɐvɑvɚ / hædɐvɑvɐ` | 0.29 |
| Eloi | /ˈiː.lɔɪ/ | `ɐloɪ / ɐloʊ` | 0.29 |
| Betah | /ˈbiː.təh/ | `beɪɾɚ / veɪtɑ` | 0.30 |
| Paarai | /ˈpeɪ.ə.reɪ/ | `hisɛd / pɚɹaɪ` | 0.30 |
| Calno | /ˈsæl.nə/ | `kaʊnoʊ / kɔlnoʊ` | 0.30 |
| Gehazi | /ˈɡiː.hə.zə/ | `ɡɐhɑsi / ɡɐhɑtsi` | 0.31 |
| Hathach | /ˈheɪ.θək/ | `hædhæk / hæthækt` | 0.31 |
| Boanerges | /ˈboʊ.nər.ɡəs/ | `vɔnɜɡz / vɔlnɜɡz` | 0.31 |
| Ithiel | /ˈi.θaɪl/ | `ɪθioʊ / ɪθiəl` | 0.33 |
| Nicolaitans | /niˈsoʊ.leɪ.təns/ | `nɪkəllaɪɾænz / nɪkəllaɪɾænts` | 0.33 |
| Asenath | /ˈeɪ.sə.nəθ/ | `ɐsɛnæf / ɐsɛnæf` | 0.33 |
| Eri | /ˈiː.rə/ | `eɪɹi / ɛɹi` | 0.33 |
| Ehi | /ˈiː.hə/ | `ɐhaɪ / eɪhaɪ` | 0.33 |
| Mishael | /ˈmi.ʃə.əl/ | `mɪsheɪl / mɪsheɪl` | 0.33 |
| Pagiel | /ˈpeɪ.ɡaɪl/ | `pædʒiəl / pædʒiəl` | 0.33 |
| Gemalli | /ˈɡiː.məl.lə/ | `dʒəmælaɪ / dʒəmælaɪ` | 0.33 |
| Balaam | /ˈbeɪ.lə.əm/ | `wɐlɑm / vɐlɑm` | 0.33 |
| Huzoth | /ˈhjuː.zəθ/ | `hiwzɑf / hiwzɑf` | 0.33 |
| Ashbelites | /əˈʃbiː.li.təs/ | `æʃbɪlɪɾiz / æʃbɪlɪɾiz` | 0.33 |
| Hupham | /ˈhjuː.fəm/ | `hʌphɛm / hʌphɛm` | 0.33 |
| Huphamites | /həˈfeɪ.mi.təs/ | `hɑpɾəmaɪts / hʌpðəmaɪt` | 0.33 |
| Tophel | /ˈtoʊ.fəl/ | `tɑphɛl / tɑphɛl` | 0.33 |
| Maacath | /ˈmeɪ.ə.səθ/ | `mækɪθ / mækɪθ` | 0.33 |
| Evi | /ˈiː.və/ | `ɛvi / ɛvi` | 0.33 |
| Maareh | /ˈmeɪ.ə.rəh/ | `meɪ / meɪ` | 0.33 |
| Saph | /ˈsæf/ | `sɪv / sʌv` | 0.33 |
| Ahasbai | /ˈeɪ.həs.beɪ/ | `ɐhæzbaɪ / ɐhæzbaɪ` | 0.33 |
| Cuth | /ˈsʌθ/ | `kʊθ / kʊθ` | 0.33 |
| Abi | /ˈeɪ.bə/ | `ɑbi / ɑbi` | 0.33 |
| Artaxerxes | /ərˈteɪ.ksər.ksəs/ | `ɑɹɾəzɜksiz / ɑɹɾəzɜksiz` | 0.33 |
| Maai | /ˈmeɪ.eɪ/ | `maɪ / maɪ` | 0.33 |
| Harsith | /ˈhær.sɪθ/ | `hɜsif / hɜsif` | 0.33 |
| Baalis | /ˈbeɪ.ə.lɪs/ | `bɑliz / bɑliz` | 0.33 |
| Apelles | /ˈeɪ.pəl.ləs/ | `ɐpɛliz / ɐpɛliz` | 0.33 |
| Bartimaeus | /bərˈti.mə.juːs/ | `bɑɹdəmiəs / ɑɹdəmiəs` | 0.35 |
| Potiphar | /ˈpoʊ.ti.fər/ | `pɑdɐfɔ / pɑdᵻfɔɹ` | 0.36 |
| Cushite | /ˈsjuː.ʃi.tiː/ | `kuʃaɪt / kuʃaɪd` | 0.36 |
| Secacah | /ˈsiː.sə.səh/ | `sɛkɪkɚ / sɛkəkɐ` | 0.36 |
| Ararite | /əˈreɪ.ri.tiː/ | `ɛɹɹaɪt / ɛɹɚɹaɪt` | 0.36 |
| Bethlehemite | /bə.θləˈhiː.mi.tiː/ | `bɛfliəmaɪt / bɛfliəmaɪt` | 0.36 |
| Taphath | /ˈteɪ.fəθ/ | `tæpæθ / tæphæθ` | 0.37 |
| Shunites | /ˈʃjuː.ni.təs/ | `ʃunaɪdiz / ʃunaɪdiz` | 0.38 |
| Jogbehah | /ˈdʒɒɡ.bə.həh/ | `dʒabihɑ / dʒabiha` | 0.38 |
| Anath | /ˈeɪ.nəθ/ | `ɐnæf / ɐnæθ` | 0.38 |
| Ephrathite | /əˈfreɪ.θi.tiː/ | `ɛfɹᵻfaɪt / ɛfɹɚθaɪt` | 0.38 |
| Athach | /ˈeɪ.θək/ | `æfɪk / æθɪk` | 0.38 |
| Jedidiah | /dʒə.diˈdi.əh/ | `dʒɛddaɪɐ / dʒɛddaɪɐ` | 0.38 |
| Basshebeth | /ˈbæs.ʃə.bəθ/ | `veɪshibɪθ / veɪshibɪθ` | 0.38 |
| Hasupha | /ˈheɪ.sə.fə/ | `hæʒəkə / hæʒɪkvɚ` | 0.38 |
| Bavvai | /ˈbæv.veɪ/ | `bəvaɪ / əvaɪ` | 0.38 |
| Nahamani | /nəˈheɪ.mə.nə/ | `naʊmɑni / naʊmɑni` | 0.38 |
| UPHARSIN | /ˈjuː.fər.sɪn/ | `ɐpɑɹsən / ɐpɑɹsən` | 0.38 |
| Elkoshite | /əlˈkoʊ.ʃi.tiː/ | `ɛlkoʊsaɪd / ɛlkoʊsaɪd` | 0.38 |
| Tahanites | /təˈheɪ.ni.təs/ | `tɑxɑnaɪs / tɑkɑnaɪts` | 0.39 |
| Shuhamites | /ʃəˈheɪ.mi.təs/ | `ʃuðəmaɪts / ʃuʌvɐmaɪs` | 0.39 |
| Decapolis | /dəˈseɪ.pə.lɪs/ | `dɛkəpoʊləs / dʒɛkəpoʊləs` | 0.39 |
| Moreh | /ˈmoʊ.rəh/ | `mɔɹ / mɔɹ` | 0.40 |
| Birsha | /ˈbɪr.ʃə/ | `bɜʃɑ / bɜʃɑ` | 0.40 |
| Eshcol | /ˈiː.ʃsəl/ | `ɛʃkɑl / ɛʃkɔl` | 0.40 |
| Phicol | /ˈfi.səl/ | `faɪkɑl / vaɪkəl` | 0.40 |
| Elohe | /ˈiː.lə.hiː/ | `iloʊ / iloʊ` | 0.40 |
| Bacuth | /ˈbeɪ.səθ/ | `bəkʊθ / bəkʊθ` | 0.40 |

## Structural faults found and fixed

These were caught without relying on any reference, by checking the audio against what the spelling itself implies — scripture `ch` is /k/, `g` before a back vowel is hard, and the syllable count should roughly match. That is why they could be fixed even where the reference was only a guess.

| Name | Fault | Now spelled |
| --- | --- | --- |
| Chezib | ch read as /tʃ/, should be /k/ | `kezib` |
| Perezites | dropped 2 syllable(s) (4->2) | `perezitess` |
| Helekites | dropped 2 syllable(s) (4->2) | `helekitess` |
| Shechemites | ch read as /tʃ/, should be /k/ | `shekemites` |
| Becherites | ch read as /tʃ/, should be /k/ | `bekerites` |
| Malchielites | ch read as /tʃ/, should be /k/ | `malkielites` |
| Og | g read as /dʒ/, should be hard | `ogh` |
| Chinnereth | ch read as /tʃ/, should be /k/ | `kinnereth` |
| Chislon | ch read as /tʃ/, should be /k/ | `kislon` |
| Chinneroth | ch read as /tʃ/, should be /k/ | `kinneroth` |
| Chesalon | ch read as /tʃ/, should be /k/ | `kesalon` |
| Chesil | ch read as /tʃ/, should be /k/ | `kesil` |
| Chitlish | ch read as /tʃ/, should be /k/ | `kitlish` |
| Archites | ch read as /tʃ/, should be /k/ | `arkites` |
| Chisloth | ch read as /tʃ/, should be /k/ | `kisloth` |
| Chesulloth | ch read as /tʃ/, should be /k/ | `kesulloth` |
| Asherites | dropped 2 syllable(s) (4->2) | `asheritess` |
| Bochim | ch read as /tʃ/, should be /k/ | `bokim` |
| Chilion | ch read as /tʃ/, should be /k/ | `kilion` |
| Michmash | ch read as /tʃ/, should be /k/ | `mikmash` |
| Hachilah | ch read as /tʃ/, should be /k/ | `hakilah` |
| Maoch | ch read as /tʃ/, should be /k/ | `maok` |
| Jerahmeelites | dropped 2 syllable(s) (5->3) | `jerahmeelitess` |
| Chileab | ch read as /tʃ/, should be /k/ | `kileab` |
| Chimham | ch read as /tʃ/, should be /k/ | `kimham` |
| Cherith | ch read as /tʃ/, should be /k/ | `kerith` |
| Azgad | g read as /dʒ/, should be hard | `azghad` |
| Pochereth | ch read as /tʃ/, should be /k/ | `pokereth` |
| Chelal | ch read as /tʃ/, should be /k/ | `kelal` |
| Chislev | ch read as /tʃ/, should be /k/ | `kislev` |
| Haccherem | ch read as /tʃ/, should be /k/ | `hackerem` |
| Chenani | ch read as /tʃ/, should be /k/ | `kenani` |
| Malluchi | ch read as /tʃ/, should be /k/ | `malluki` |
| Barachel | ch read as /tʃ/, should be /k/ | `barakel` |
| Chebar | ch read as /tʃ/, should be /k/ | `kebar` |
| Chilmad | ch read as /tʃ/, should be /k/ | `kilmad` |
| Sychar | ch read as /tʃ/, should be /k/ | `sykar` |
| Stachys | ch read as /tʃ/, should be /k/ | `stakys` |

One caution from that pass: the `ch` rule is a Hebrew-transliteration convention and does not hold for every name. It turned **Rachel** into "rakel" before CMUdict overruled it. If a fix above looks wrong for a familiar name, that is the likely cause.

---

_Generated from a whole-canon verifier sweep of the WEB text (1189 chapters, voice en-US-AndrewNeural). Scores are two-carrier averages._
