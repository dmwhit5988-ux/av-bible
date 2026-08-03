# Bible proper-noun pronunciation guide

Master list used to help the neural text-to-speech read scripture names
correctly. Generated from `pronunciations.json` -- edit with the GUI
(`python pronunciation_tool.py`) or the JSON, then rebuild with
`python pronunciation.py`. Do not hand-edit this file.

- **Say it** — the pronunciation fed to the voice (tuned by ear).
- **TTS** — ✅ means the audio pipeline substitutes this spelling before
  synthesis; blank means the name is spoken exactly as spelled.
- **Checked** — what listening to the real audio concluded. Blank means
  nobody has checked it yet, which is not the same as it being right.

| Name | Say it | IPA | First appears | TTS | Checked |
| --- | --- | --- | --- | --- | --- |
| Spirit | Spirit |  | Genesis 1:2 |  | fine as spelled |
| Havilah | HAVih-lah | /ˈhæv.ɪ.lə/ | Genesis 2:11 | ✅ | overridden (0.83) |
| Pishon | PIE-shon | /ˈpaɪ.ʃɒn/ | Genesis 2:11 | ✅ | overridden (1.00) |
| Pison | pyson | /ˈpaɪ.sɒn/ | Genesis 2:11 | ✅ | overridden (1.00) |
| Bdellium | DEL-eeum | /ˈdɛl.i.əm/ | Genesis 2:12 | ✅ | overridden (1.00) |
| Cush | KUSH | /kʌʃ/ | Genesis 2:13 |  | still wrong (0.67) |
| Assyria | uh-SEER-ee-uh | /əˈsɪr.i.ə/ | Genesis 2:14 |  | fine as spelled (0.83) |
| Euphrates | yoo-FRAY-teez | /juːˈfreɪ.tiːz/ | Genesis 2:14 |  | fine as spelled (0.88) |
| Hiddekel | HID-uh-kel | /ˈhɪd.ə.kɛl/ | Genesis 2:14 | ✅ | overridden (1.00) |
| Man | Man |  | Genesis 2:23 |  | fine as spelled |
| Cherubim | CHER-uh-bim | /ˈtʃɛr.ə.bɪm/ | Genesis 3:24 |  | fine as spelled (1.00) |
| Cain | KAYN | /keɪn/ | Genesis 4:1 |  | still wrong (0.67) |
| Eve | EEV | /iːv/ | Genesis 4:1 |  | fine as spelled (1.00) |
| Nod | NOD | /nɒd/ | Genesis 4:16 |  | fine as spelled (1.00) |
| Irad | EYE-rad | /ˈaɪ.ræd/ | Genesis 4:18 | ✅ | overridden (0.75) |
| Mehujael | muh-HYOO-jay-el | /mɪˈhjuː.dʒeɪ.ɛl/ | Genesis 4:18 | ✅ | overridden (0.80) |
| Methusael | meth-YOO-say-el | /mɪˈθjuː.seɪ.ɛl/ | Genesis 4:18 | ✅ | overridden (0.89) |
| Methushael | muh-THOO-shay-el | /mɪˈθuː.ʃeɪ.ɛl/ | Genesis 4:18 | ✅ | overridden (0.62) |
| Adah | AY-duh | /ˈeɪ.də/ | Genesis 4:19 | ✅ | overridden (0.46) |
| Zillah | ZIL-uh | /ˈzɪl.ə/ | Genesis 4:19 |  | still wrong (0.75) |
| Jabal | JAY-bul | /ˈdʒeɪ.bəl/ | Genesis 4:20 | ✅ | overridden (0.90) |
| Jubal | JOO-bul | /ˈdʒuː.bəl/ | Genesis 4:21 | ✅ | overridden (1.00) |
| Tubal | TOO-buhl | /ˈtuː.bəl/ | Genesis 4:22 |  | fine as spelled (1.00) |
| Tubal-cain | TOO-bal-kayn | /ˈtjuː.bəl.keɪn/ | Genesis 4:22 |  | fine as spelled (0.89) |
| Adam | AD-uhm | /ˈæd.əm/ | Genesis 5:1 |  | fine as spelled (1.00) |
| Seth | SETH | /sɛθ/ | Genesis 5:3 |  | still wrong (0.67) |
| Enosh | eenosh | /ˈiː.nɒʃ/ | Genesis 5:6 | ✅ | overridden (1.00) |
| Cainan | Caynen | /ˈkeɪ.nən/ | Genesis 5:9 | ✅ | overridden (1.00) |
| Kenan | KEE-nan | /ˈkiː.nən/ | Genesis 5:9 |  | fine as spelled (1.00) |
| Mahalaleel | muh-HAL-uh-lel | /məˈhæl.ə.lɛl/ | Genesis 5:12 | ✅ | overridden (1.00) |
| Mahalalel | muh-HAL-uh-lel | /məˈhæl.ə.lɛl/ | Genesis 5:12 | ✅ | overridden (1.00) |
| Jared | JAIR-ed | /ˈdʒɛər.ɛd/ | Genesis 5:15 |  | fine as spelled (0.80) |
| Enoch | EE-nuhk | /ˈiː.nək/ | Genesis 5:18 |  | still wrong (0.75) |
| Methuselah | muh-THOO-zuh-luh | /məˈθuː.zə.lə/ | Genesis 5:21 |  | fine as spelled (0.88) |
| Lamech | LAY-mek | /ˈleɪ.mɛk/ | Genesis 5:25 | ✅ | overridden (1.00) |
| Noah | NOH-uh | /ˈnoʊ.ə/ | Genesis 5:29 |  | fine as spelled (1.00) |
| Yahweh | YAH-way | /ˈjɑː.weɪ/ | Genesis 5:29 |  | fine as spelled |
| Ham | HAM | /hæm/ | Genesis 5:32 |  | still wrong (0.67) |
| Japheth | JAY-feth | /ˈdʒeɪ.fɛθ/ | Genesis 5:32 | ✅ | overridden (1.00) |
| Shem | SHEM | /ʃɛm/ | Genesis 5:32 |  | fine as spelled (1.00) |
| Nephilim | NEFelim | /ˈnɛf.ɪ.lɪm/ | Genesis 6:4 | ✅ | overridden (0.64) |
| Ararat | AIR-uh-rat | /ˈær.ə.ræt/ | Genesis 8:4 |  | fine as spelled (0.83) |
| Gomer | GOH-mer | /ˈɡoʊ.mər/ | Genesis 10:2 |  | fine as spelled (1.00) |
| Javan | JAY-van | /ˈdʒeɪ.væn/ | Genesis 10:2 | ✅ | overridden (0.80) |
| Madai | MAYdye | /ˈmeɪ.daɪ/ | Genesis 10:2 | ✅ | overridden (1.00) |
| Magog | MAY-gog | /ˈmeɪ.ɡɒɡ/ | Genesis 10:2 |  | fine as spelled (1.00) |
| Meshech | MEEshech | /ˈmiː.ʃɛk/ | Genesis 10:2 | ✅ | overridden (1.00) |
| Tiras | TYruss | /ˈtaɪ.rəs/ | Genesis 10:2 | ✅ | overridden (1.00) |
| Ashkenaz | ASH-kuh-naz | /ˈæʃ.kə.næz/ | Genesis 10:3 |  | fine as spelled (1.00) |
| Riphath | RYE-fath | /ˈraɪ.fæθ/ | Genesis 10:3 | ✅ | overridden (0.80) |
| Togarmah | toh-GAR-muh | /toʊˈɡɑːr.mə/ | Genesis 10:3 |  | fine as spelled (0.86) |
| Dodanim | dahduhnihm | /ˈdɒd.ə.nɪm/ | Genesis 10:4 | ✅ | overridden (0.86) |
| Elishah | Elai-sha | /ɪˈlaɪ.ʃə/ | Genesis 10:4 | ✅ | overridden (0.70) |
| Kittim | KIT-im | /ˈkɪt.ɪm/ | Genesis 10:4 |  | fine as spelled (0.83) |
| Tarshish | TAR-shish | /ˈtɑːr.ʃɪʃ/ | Genesis 10:4 |  | fine as spelled (1.00) |
| Mizraim | mizRAYim | /mɪzˈreɪ.ɪm/ | Genesis 10:6 | ✅ | overridden (0.79) |
| Phut | FUT | /fʌt/ | Genesis 10:6 |  | fine as spelled (1.00) |
| Put | PUT | /pʌt/ | Genesis 10:6 |  | still wrong (0.67) |
| Dedan | DEE-dan | /ˈdiː.dæn/ | Genesis 10:7 | ✅ | overridden (0.90) |
| Raamah | RAY-uh-muh | /ˈreɪ.ə.mə/ | Genesis 10:7 | ✅ | overridden (0.90) |
| Sabtah | SAB-tuh | /ˈsæb.tə/ | Genesis 10:7 |  | fine as spelled (0.80) |
| Sabteca | SAB-tuck-uhh | /ˈsæb.tə.kə/ | Genesis 10:7 | ✅ | overridden (0.71) |
| Sabtechah | SAB-tih-kah | /ˈsæb.tɪ.kɑː/ | Genesis 10:7 | ✅ | overridden (0.86) |
| Seba | SEEba | /ˈsiː.bə/ | Genesis 10:7 | ✅ | overridden (1.00) |
| Sheba | SHEE-buh | /ˈʃiː.bə/ | Genesis 10:7 |  | fine as spelled (1.00) |
| Nimrod | NIM-rod | /ˈnɪm.rɒd/ | Genesis 10:8 |  | fine as spelled (1.00) |
| Accad | AK-ad | /ˈæk.æd/ | Genesis 10:10 |  | fine as spelled (1.00) |
| Calneh | KAL-neh | /ˈkæl.nɛ/ | Genesis 10:10 | ✅ | overridden (0.50) |
| Erech | EH-rek | /ˈɛr.ɛk/ | Genesis 10:10 | ✅ | overridden (0.75) |
| Calah | KAY-luh | /ˈkeɪ.lə/ | Genesis 10:11 | ✅ | overridden (0.75) |
| Ir | ear | /ɪər/ | Genesis 10:11 | ✅ | overridden (0.00) |
| Rehoboth | ruh-HOH-both | /rəˈhoʊ.bɒθ/ | Genesis 10:11 |  | fine as spelled (0.86) |
| Resen | REE-sen | /ˈriː.sɛn/ | Genesis 10:12 | ✅ | overridden (0.80) |
| Anamim | AN-uh-mim | /ˈæn.ə.mɪm/ | Genesis 10:13 |  | fine as spelled (0.83) |
| Lehabim | laHAY-bim | /ləˈheɪ.bɪm/ | Genesis 10:13 | ✅ | overridden (1.00) |
| Ludim | LOO-dim | /ˈluː.dɪm/ | Genesis 10:13 |  | fine as spelled (0.80) |
| Naphtuhim | naftoohihm | /næfˈtuː.hɪm/ | Genesis 10:13 | ✅ | overridden (1.00) |
| Caphtorim | KAFtarim | /ˈkæf.tə.rɪm/ | Genesis 10:14 |  | fine as spelled (1.00) |
| Casluhim | KAS-loo-him | /ˈkæs.luː.hɪm/ | Genesis 10:14 | ✅ | overridden (0.94) |
| Pathrusim | path-ROO-sim | /pæθˈruː.sɪm/ | Genesis 10:14 |  | fine as spelled (0.88) |
| Philistim | fih-LIS-tim | /fɪˈlɪs.tɪm/ | Genesis 10:14 |  | fine as spelled (0.88) |
| Philistines | FILihsteenz | /ˈfɪl.ɪ.stiːnz/ | Genesis 10:14 | ✅ | overridden (1.00) |
| Heth | hetth | /hɛθ/ | Genesis 10:15 | ✅ | overridden (0.67) |
| Sidon | SY-duhn | /ˈsaɪ.dən/ | Genesis 10:15 |  | fine as spelled (1.00) |
| Girgashites | GUR-guh-shites | /ˈɡɜːr.ɡə.ʃaɪts/ | Genesis 10:16 | ✅ | overridden (0.44) |
| Girgasite | gerrguhseyet | /ˈɡɜːr.ɡə.saɪt/ | Genesis 10:16 | ✅ | overridden (0.81) |
| Arkites | AR-kites | /ˈɑːr.kaɪts/ | Genesis 10:17 |  | fine as spelled (1.00) |
| Sinites | SIGH-nites | /ˈsaɪ.naɪts/ | Genesis 10:17 | ✅ | overridden (1.00) |
| Arvadites | AR-vuh-dites | /ˈɑːr.və.daɪts/ | Genesis 10:18 |  | fine as spelled (1.00) |
| Canaanites | KAY-nuh-nites | /ˈkeɪ.nə.naɪts/ | Genesis 10:18 |  | fine as spelled (1.00) |
| Hamathites | HAY-muh-thites | /ˈheɪ.mə.θaɪts/ | Genesis 10:18 |  | fine as spelled (0.88) |
| Zemarites | ZEM-uh-rites | /ˈzɛm.ə.raɪts/ | Genesis 10:18 |  | fine as spelled (0.88) |
| Admah | AD-muh | /ˈæd.mə/ | Genesis 10:19 |  | fine as spelled (1.00) |
| Gomorrah | guh-MOR-uh | /ɡəˈmɒr.ə/ | Genesis 10:19 |  | fine as spelled (1.00) |
| Lasha | LAY-shuh | /ˈleɪ.ʃə/ | Genesis 10:19 | ✅ | overridden (0.75) |
| Zeboiim | zuh-BOY-im | /zɪˈbɔɪ.ɪm/ | Genesis 10:19 | ✅ | overridden (0.54) |
| Zeboim | zeh-BOH-im | /zɪˈboʊ.ɪm/ | Genesis 10:19 |  | still wrong (0.67) |
| Aram | AIR-uhm | /ˈɛər.əm/ | Genesis 10:22 |  | fine as spelled (1.00) |
| Asshur | ASH-er | /ˈæʃ.ər/ | Genesis 10:22 | ✅ | overridden (1.00) |
| Elam | EEluhm | /ˈiː.ləm/ | Genesis 10:22 | ✅ | overridden (1.00) |
| Lud | LUHD | /lʌd/ | Genesis 10:22 | ✅ | overridden (0.50) |
| Gether | GuEE-ther | /ˈɡiː.θər/ | Genesis 10:23 | ✅ | overridden (0.80) |
| Hul | HUHL | /hʌl/ | Genesis 10:23 |  | still wrong (0.67) |
| Mash | MASH | /mæʃ/ | Genesis 10:23 |  | fine as spelled (1.00) |
| Uz | UHZ | /ʌz/ | Genesis 10:23 | ✅ | overridden (1.00) |
| Salah | SAY-la | /ˈseɪ.lə/ | Genesis 10:24 | ✅ | overridden (1.00) |
| Joktan | JOKtan | /ˈdʒɒk.tæn/ | Genesis 10:25 |  | fine as spelled (0.83) |
| Almodad | al-MOHdad | /ælˈmoʊ.dæd/ | Genesis 10:26 | ✅ | overridden (0.86) |
| Hazar-maveth | hay-zahr-MAY-vehth | /ˌheɪ.zɑːrˈmeɪ.vɛθ/ | Genesis 10:26 | ✅ | overridden (1.00) |
| Hazarmaveth | hay-zahr-MAY-vehth | /ˌheɪ.zɑːrˈmeɪ.vɛθ/ | Genesis 10:26 | ✅ | overridden (1.00) |
| Jerah | jeerah | /ˈdʒɪər.ə/ | Genesis 10:26 | ✅ | overridden (1.00) |
| Sheleph | SHEE-lef | /ˈʃiː.lɛf/ | Genesis 10:26 |  | fine as spelled (0.80) |
| Diklah | DIK-luh | /ˈdɪk.lə/ | Genesis 10:27 |  | fine as spelled (0.80) |
| Hadoram | huh-DAWR-uhm | /həˈdɔːr.əm/ | Genesis 10:27 | ✅ | overridden (0.86) |
| Uzal | YOO-zuhl | /ˈjuː.zəl/ | Genesis 10:27 |  | fine as spelled (1.00) |
| Abimael | uh-BIM-ay-el | /əˈbɪm.eɪ.ɛl/ | Genesis 10:28 |  | still wrong (0.57) |
| Obal | OH-bal | /ˈoʊ.bæl/ | Genesis 10:28 | ✅ | overridden (0.62) |
| Jobab | JOH-bab | /ˈdʒoʊ.bæb/ | Genesis 10:29 |  | fine as spelled (1.00) |
| Ophir | OH-fer | /ˈoʊ.fər/ | Genesis 10:29 |  | fine as spelled (1.00) |
| Mesha | MEE-shuh | /ˈmiː.ʃə/ | Genesis 10:30 |  | fine as spelled (1.00) |
| Sephar | SEE-far | /ˈsiː.fɑːr/ | Genesis 10:30 | ✅ | overridden (1.00) |
| Shinar | SHY-narr | /ˈʃaɪ.nɑːr/ | Genesis 11:2 | ✅ | overridden (0.90) |
| Babel | BAY-bul | /ˈbeɪ.bəl/ | Genesis 11:9 |  | fine as spelled (0.80) |
| Arpachshad | arpackshad | /ɑːrˈpæk.ʃæd/ | Genesis 11:10 | ✅ | overridden (0.94) |
| Shelah | sheelah | /ˈʃiː.lə/ | Genesis 11:12 | ✅ | overridden (1.00) |
| Eber | eeber | /ˈiː.bər/ | Genesis 11:14 | ✅ | overridden (1.00) |
| Peleg | PEElegg | /ˈpiː.lɛg/ | Genesis 11:16 | ✅ | overridden (1.00) |
| Reu | reeyou | /ˈriː.uː/ | Genesis 11:18 | ✅ | overridden (0.83) |
| Serug | SEE-rug | /ˈsiː.rʌg/ | Genesis 11:20 | ✅ | overridden (1.00) |
| Nahor | NAY-hor | /ˈneɪ.hɔːr/ | Genesis 11:22 | ✅ | overridden (0.90) |
| Terah | TAIR-uh | /ˈtɛər.ə/ | Genesis 11:24 | ✅ | overridden (0.62) |
| Abram | AY-bram | /ˈeɪ.bræm/ | Genesis 11:26 |  | fine as spelled (0.80) |
| Haran | HAIR-uhn | /ˈhɛər.ən/ | Genesis 11:26 | ✅ | overridden (0.60) |
| Lot | LOT | /lɒt/ | Genesis 11:27 |  | fine as spelled (1.00) |
| Chaldees | kaldeez | /kælˈdiːz/ | Genesis 11:28 | ✅ | overridden (1.00) |
| Ur | urr | /ɜːr/ | Genesis 11:28 | ✅ | overridden (1.00) |
| Iscah | isskah | /ˈɪs.kə/ | Genesis 11:29 | ✅ | overridden (0.75) |
| Milcah | milkah | /ˈmɪl.kə/ | Genesis 11:29 | ✅ | overridden (0.90) |
| Sarai | SAIR-eye | /ˈsɛər.aɪ/ | Genesis 11:29 | ✅ | overridden (0.75) |
| Canaan | Canaan | /ˈkeɪ.nən/ | Genesis 11:31 |  | fine as spelled (1.00) |
| Moreh | Moreh | /ˈmoʊ.rəh/ | Genesis 12:6 |  | unsure (guessed IPA) (0.40) |
| Shechem | SHEK-uhm | /ˈʃɛk.əm/ | Genesis 12:6 |  | fine as spelled (1.00) |
| Ai | Ai |  | Genesis 12:8 |  | fine as spelled |
| Bethel | BETH-el | /ˈbɛθ.əl/ | Genesis 12:8 |  | fine as spelled (0.90) |
| South | South |  | Genesis 12:9 |  | fine as spelled |
| Pharaoh | FAIR-oh | /ˈfɛər.oʊ/ | Genesis 12:15 |  | still wrong (0.75) |
| Jordan | JOR-duhn | /ˈdʒɔːr.dən/ | Genesis 13:10 |  | fine as spelled (1.00) |
| Zoar | Zoar | /ˈzəʊ.ɑː/ | Genesis 13:10 |  | still wrong (0.67) |
| Hebron | HEE-bruhn | /ˈhiː.brən/ | Genesis 13:18 |  | fine as spelled (1.00) |
| Mamre | Mamre | /ˈmæmri/ | Genesis 13:18 |  | still wrong (0.60) |
| Amraphel | Amraphel | /ˈæmrəˌfɛl/ | Genesis 14:1 |  | still wrong (0.73) |
| Arioch | Arioch | /ˈeɪ.ri.ək/ | Genesis 14:1 |  | unsure (guessed IPA) (0.60) |
| Chedorlaomer | Chedorlaomer | /ˌkɛdərˈleɪəmər/ | Genesis 14:1 |  | still wrong (0.73) |
| Ellasar | Ellasar | /ˈɛl.lə.sər/ | Genesis 14:1 |  | unsure (guessed IPA) (0.50) |
| Goiim | Goiim | /ˈɡɔɪ.ɪm/ | Genesis 14:1 |  | unsure (guessed IPA) (0.75) |
| Tidal | Tidal | /tˈaɪdəl/ | Genesis 14:1 |  | fine as spelled (1.00) |
| Bela | BEEla | /ˈbiː.lə/ | Genesis 14:2 | ✅ | overridden (1.00) |
| Bera | Bera | /bˈɛrə/ | Genesis 14:2 |  | fine as spelled (1.00) |
| Birsha | Birsha | /ˈbɪr.ʃə/ | Genesis 14:2 |  | unsure (guessed IPA) (0.40) |
| Shemeber | Shemeber | /ˈʃiː.mə.bər/ | Genesis 14:2 |  | unsure (guessed IPA) (0.71) |
| Shinab | Shinab | /ˈʃi.nəb/ | Genesis 14:2 |  | unsure (guessed IPA) (0.50) |
| Siddim | Siddim | /ˈsɪd.dɪm/ | Genesis 14:3 |  | fine as spelled (1.00) |
| Ashteroth | Ashteroth | /ˈeɪ.ʃtə.rəθ/ | Genesis 14:5 |  | unsure (guessed IPA) (0.64) |
| Emim | Emim | /ˈiː.mɪm/ | Genesis 14:5 |  | unsure (guessed IPA) (0.75) |
| Karnaim | Karnaim | /ˈkær.neɪm/ | Genesis 14:5 |  | unsure (guessed IPA) (0.75) |
| Kiriathaim | kir-ee-uh-THAY-im | /ˌkɪr.i.əˈθeɪ.ɪm/ | Genesis 14:5 |  | still wrong (0.78) |
| Shaveh | Shaveh | /ˈʃeɪ.vəh/ | Genesis 14:5 |  | unsure (guessed IPA) (0.60) |
| Zuzim | Zuzim | /ˈzjuː.zɪm/ | Genesis 14:5 |  | unsure (guessed IPA) (0.67) |
| El | El | /ˈɛl/ | Genesis 14:6 |  | fine as spelled (1.00) |
| Horites | Horites | /ˈhoʊ.ri.təs/ | Genesis 14:6 |  | unsure (guessed IPA) (0.71) |
| Paran | Paran | /ˈpeɪ.rən/ | Genesis 14:6 |  | unsure (guessed IPA) (0.60) |
| Seir | SEE-ur | /ˈsiː.ər/ | Genesis 14:6 |  | fine as spelled (1.00) |
| Amalekites | AM-uh-lek-ites | /ˈæm.ə.lɛk.aɪts/ | Genesis 14:7 |  | fine as spelled (0.94) |
| En | En | /ˈɛn/ | Genesis 14:7 |  | still wrong (0.75) |
| Kadesh | Kadesh | /ˈkeɪˌdɛʃ/ | Genesis 14:7 |  | fine as spelled (0.80) |
| Mishpat | Mishpat | /ˈmi.ʃpət/ | Genesis 14:7 |  | unsure (guessed IPA) (0.67) |
| Tamar | TAY-mar | /ˈteɪ.mɑːr/ | Genesis 14:7 |  | fine as spelled (1.00) |
| Amorite | AM-uh-rite | /ˈæm.ə.raɪt/ | Genesis 14:13 | ✅ | overridden (1.00) |
| Aner | AY-ner | /ˈeɪ.nər/ | Genesis 14:13 |  | fine as spelled (1.00) |
| Eshcol | Eshcol | /ˈɛʃˌkɒl/ | Genesis 14:13 |  | fine as spelled (1.00) |
| Hebrew | Hebrew | /hˈiːbruː/ | Genesis 14:13 |  | fine as spelled (1.00) |
| Dan | DAN | /dæn/ | Genesis 14:14 |  | still wrong (0.67) |
| Hobah | Hobah | /ˈhoʊ.bəh/ | Genesis 14:15 |  | fine as spelled (0.80) |
| Salem | Salem | /sˈeɪləm/ | Genesis 14:18 |  | fine as spelled (1.00) |
| Eliezer | el-ee-EE-zer | /ˌɛl.iˈiː.zər/ | Genesis 15:2 |  | fine as spelled (0.86) |
| Kadmonites | Kadmonites | /kədˈmoʊ.ni.təs/ | Genesis 15:19 |  | unsure (guessed IPA) (0.60) |
| Kenites | KEE-nites | /ˈkiː.naɪts/ | Genesis 15:19 |  | suggestion waiting (0.60) |
| Kenizzites | Kenizzites | /kəˈnɪz.zi.təs/ | Genesis 15:19 |  | unsure (guessed IPA) (0.61) |
| Egyptian | Egyptian | /ɪdʒˈɪpʃən/ | Genesis 16:1 |  | fine as spelled (1.00) |
| Hagar | Hagar | /hˈeɪɡɑr/ | Genesis 16:1 |  | fine as spelled (1.00) |
| Shur | Shur | /ʃˈɚ/ | Genesis 16:7 |  | fine as spelled (0.83) |
| Ishmael | ISH-may-el | /ˈɪʃ.meɪ.əl/ | Genesis 16:11 |  | fine as spelled (0.83) |
| Beer | Beer | /bˈɪr/ | Genesis 16:14 |  | still wrong (0.33) |
| Bered | BEERR-ehd | /ˈbɪər.ɛd/ | Genesis 16:14 | ✅ | overridden (0.80) |
| Lahai | Lahai | /ˈleɪ.heɪ/ | Genesis 16:14 |  | unsure (guessed IPA) (0.50) |
| Roi | Roi | /rˈɔɪ/ | Genesis 16:14 |  | still wrong (0.33) |
| Almighty | Almighty | /ɔlmˈaɪtiː/ | Genesis 17:1 |  | still wrong (0.67) |
| Abraham | AY-bruh-ham | /ˈeɪ.brə.hæm/ | Genesis 17:5 |  | fine as spelled (0.93) |
| Sarah | Sarah | /sˈɛrə/ | Genesis 17:15 |  | fine as spelled (1.00) |
| Isaac | EYE-zuhk | /ˈaɪ.zək/ | Genesis 17:19 |  | still wrong (0.75) |
| Moab | MOH-ab | /ˈmoʊ.æb/ | Genesis 19:37 |  | fine as spelled (1.00) |
| Ammi | Ammi | /ˈæm.mə/ | Genesis 19:38 |  | unsure (guessed IPA) (0.67) |
| Ben | BEN | /bɛn/ | Genesis 19:38 |  | fine as spelled (1.00) |
| Beersheba | beerrsheeba | /bɪərˈʃiː.bə/ | Genesis 21:14 | ✅ | overridden (0.93) |
| Phicol | Phicol | /ˈfi.səl/ | Genesis 21:22 |  | unsure (guessed IPA) (0.40) |
| Buz | BUHZ | /bʌz/ | Genesis 22:21 |  | fine as spelled (1.00) |
| Bethuel | buh-THYOO-el | /bəˈθjuː.əl/ | Genesis 22:22 |  | fine as spelled (0.80) |
| Hazo | Hazo | /ˈheɪ.zə/ | Genesis 22:22 |  | unsure (guessed IPA) (0.78) |
| Jidlaph | Jidlaph | /ˈdʒɪd.ləf/ | Genesis 22:22 |  | fine as spelled (0.83) |
| Pildash | Pildash | /ˈpɪl.dəʃ/ | Genesis 22:22 |  | fine as spelled (0.83) |
| Rebekah | Rebekah | /ˈriː.bə.kəh/ | Genesis 22:23 |  | unsure (guessed IPA) (0.57) |
| Gaham | Gaham | /ˈɡeɪ.həm/ | Genesis 22:24 |  | unsure (guessed IPA) (0.60) |
| Maacah | MAY-uh-kuh | /ˈmeɪ.ə.kə/ | Genesis 22:24 | ✅ | overridden (0.70) |
| Reumah | Reumah | /ˈrjuː.məh/ | Genesis 22:24 |  | unsure (guessed IPA) (0.67) |
| Tahash | Tahash | /ˈteɪ.həʃ/ | Genesis 22:24 |  | unsure (guessed IPA) (0.60) |
| Tebah | Tebah | /ˈtiː.bəh/ | Genesis 22:24 |  | unsure (guessed IPA) (0.60) |
| Arba | Arba | /ˈɑrbə/ | Genesis 23:2 |  | fine as spelled (1.00) |
| Kiriath | KIR-ee-ath | /ˈkɪr.i.æθ/ | Genesis 23:2 |  | still wrong (0.67) |
| Zohar | Zohar | /ˈzoʊ.hər/ | Genesis 23:8 |  | unsure (guessed IPA) (0.70) |
| Machpelah | Machpelah | /ˈmeɪ.kpə.ləh/ | Genesis 23:9 |  | unsure (guessed IPA) (0.62) |
| Laban | Laban | /lˈeɪbən/ | Genesis 24:29 |  | fine as spelled (1.00) |
| Keturah | kuh-TYOO-ruh | /kəˈtjʊər.ə/ | Genesis 25:1 |  | still wrong (0.71) |
| Ishbak | ISH-bak | /ˈɪʃ.bæk/ | Genesis 25:2 |  | fine as spelled (1.00) |
| Jokshan | JOK-shan | /ˈdʒɒk.ʃæn/ | Genesis 25:2 |  | fine as spelled (0.83) |
| Medan | MEE-dan | /ˈmiː.dæn/ | Genesis 25:2 | ✅ | overridden (1.00) |
| Midian | MID-ee-uhn | /ˈmɪd.i.ən/ | Genesis 25:2 |  | fine as spelled (0.83) |
| Shuah | SHOO-uh | /ˈʃuː.ə/ | Genesis 25:2 |  | fine as spelled (0.88) |
| Zimran | ZIM-ran | /ˈzɪm.ræn/ | Genesis 25:2 |  | fine as spelled (0.83) |
| Asshurim | Asshurim | /ˈæs.ʃə.rɪm/ | Genesis 25:3 |  | unsure (guessed IPA) (0.50) |
| Letushim | Letushim | /ˈliː.tə.ʃɪm/ | Genesis 25:3 |  | unsure (guessed IPA) (0.64) |
| Leummim | Leummim | /ˈljuːm.mɪm/ | Genesis 25:3 |  | unsure (guessed IPA) (0.58) |
| Abida | uh-BY-duh | /əˈbaɪ.də/ | Genesis 25:4 |  | fine as spelled (0.92) |
| Eldaah | el-DAY-uh | /ɛlˈdeɪ.ə/ | Genesis 25:4 |  | suggestion waiting (0.70) |
| Ephah | EE-fuh | /ˈiː.fə/ | Genesis 25:4 |  | fine as spelled (1.00) |
| Epher | EE-fer | /ˈiː.fər/ | Genesis 25:4 |  | suggestion waiting (0.75) |
| Hanoch | HAY-nok | /ˈheɪ.nɒk/ | Genesis 25:4 | ✅ | overridden (1.00) |
| Adbeel | AD-bee-el | /ˈæd.biː.ɛl/ | Genesis 25:13 | ✅ | overridden (1.00) |
| Kedar | KEE-duhr | /ˈkiː.dər/ | Genesis 25:13 | ✅ | overridden (1.00) |
| Mibsam | MIB-sam | /ˈmɪb.sæm/ | Genesis 25:13 |  | fine as spelled (0.83) |
| Nebaioth | nuh-BAY-oth | /nəˈbeɪ.ɒθ/ | Genesis 25:13 |  | fine as spelled (0.83) |
| Dumah | DOO-muh | /ˈduː.mə/ | Genesis 25:14 |  | fine as spelled (1.00) |
| Massa | MASsah | /ˈmæs.ə/ | Genesis 25:14 | ✅ | overridden (0.90) |
| Mishma | MISH-muh | /ˈmɪʃ.mə/ | Genesis 25:14 |  | fine as spelled (1.00) |
| Hadad | HAY-dad | /ˈheɪ.dæd/ | Genesis 25:15 | ✅ | overridden (1.00) |
| Jetur | JEE-tuhr | /ˈdʒiː.tər/ | Genesis 25:15 | ✅ | overridden (1.00) |
| Kedemah | kehduhmuh | /ˈkɛd.ə.mə/ | Genesis 25:15 | ✅ | overridden (0.83) |
| Naphish | NAY-fish | /ˈneɪ.fɪʃ/ | Genesis 25:15 |  | fine as spelled (1.00) |
| Tema | TEE-muh | /ˈtiː.mə/ | Genesis 25:15 |  | fine as spelled (1.00) |
| Paddan | Paddan | /ˈpæd.dən/ | Genesis 25:20 |  | unsure (guessed IPA) (0.70) |
| Syrian | Syrian | /sˈɪriːən/ | Genesis 25:20 |  | fine as spelled (1.00) |
| Esau | EE-saw | /ˈiː.sɔː/ | Genesis 25:25 |  | suggestion waiting (0.71) |
| Edom | EE-duhm | /ˈiː.dəm/ | Genesis 25:30 |  | fine as spelled (1.00) |
| Esek | Esek | /ˈiː.sək/ | Genesis 26:20 |  | unsure (guessed IPA) (0.50) |
| Sitnah | Sitnah | /ˈsɪt.nəh/ | Genesis 26:21 |  | unsure (guessed IPA) (0.58) |
| Ahuzzath | Ahuzzath | /ˈeɪ.həz.zəθ/ | Genesis 26:26 |  | unsure (guessed IPA) (0.50) |
| Shibah | Shibah | /ˈʃi.bəh/ | Genesis 26:33 |  | fine as spelled (0.80) |
| Basemath | Basemath | /ˈbeɪ.sə.məθ/ | Genesis 26:34 |  | unsure (guessed IPA) (0.71) |
| Beeri | Beeri | /ˈbiː.rə/ | Genesis 26:34 |  | unsure (guessed IPA) (0.62) |
| Elon | Elon | /ˈiːlɔːn/ | Genesis 26:34 |  | fine as spelled (1.00) |
| Judith | Judith | /dʒˈuːdəθ/ | Genesis 26:34 |  | fine as spelled (0.80) |
| Luz | Luz | /lˈəz/ | Genesis 28:19 |  | still wrong (0.67) |
| Rachel | Rachel | /rˈeɪtʃəl/ | Genesis 29:6 |  | fine as spelled (1.00) |
| Leah | Leah | /lˈiːə/ | Genesis 29:16 |  | fine as spelled (1.00) |
| Zilpah | Zilpah | /ˈzɪl.pəh/ | Genesis 29:24 |  | unsure (guessed IPA) (0.58) |
| Bilhah | BIL-huh | /ˈbɪl.hə/ | Genesis 29:29 |  | fine as spelled (0.90) |
| Reuben | ROO-ben | /ˈruː.bən/ | Genesis 29:32 |  | fine as spelled (1.00) |
| Simeon | SIM-ee-uhn | /ˈsɪm.i.ən/ | Genesis 29:33 |  | fine as spelled (0.83) |
| Levi | LEE-vy | /ˈliː.vaɪ/ | Genesis 29:34 |  | fine as spelled (1.00) |
| Judah | JOO-duh | /ˈdʒuː.də/ | Genesis 29:35 |  | fine as spelled (1.00) |
| Naphtali | NAF-tuh-ly | /ˈnæf.tə.laɪ/ | Genesis 30:8 |  | fine as spelled (0.86) |
| Gad | GAD | /ɡæd/ | Genesis 30:11 |  | fine as spelled (1.00) |
| Asher | ASH-er | /ˈæʃ.ər/ | Genesis 30:13 |  | fine as spelled (1.00) |
| Issachar | IS-uh-kar | /ˈɪs.ə.kɑːr/ | Genesis 30:18 |  | fine as spelled (1.00) |
| Zebulun | ZEB-yoo-luhn | /ˈzɛb.jʊ.lən/ | Genesis 30:20 |  | fine as spelled (1.00) |
| Dinah | Dinah | /dˈaɪnə/ | Genesis 30:21 |  | fine as spelled (1.00) |
| Joseph | JOH-zef | /ˈdʒoʊ.zəf/ | Genesis 30:24 |  | fine as spelled (0.80) |
| Gilead | GIL-ee-uhd | /ˈɡɪl.i.əd/ | Genesis 31:21 |  | fine as spelled (0.83) |
| I’m | I’m | /ˈɪm/ | Genesis 31:35 |  | unsure (guessed IPA) (0.50) |
| Galeed | Galeed | /ˈɡeɪ.liːd/ | Genesis 31:47 |  | fine as spelled (0.80) |
| Jegar | Jegar | /ˈdʒiː.ɡər/ | Genesis 31:47 |  | fine as spelled (0.80) |
| Sahadutha | Sahadutha | /səˈheɪ.də.θə/ | Genesis 31:47 |  | unsure (guessed IPA) (0.44) |
| Mahanaim | mayhanayihm | /ˌmeɪ.həˈneɪ.ɪm/ | Genesis 32:2 | ✅ | overridden (0.94) |
| Jabbok | Jabbok | /ˈdʒæb.bək/ | Genesis 32:22 |  | fine as spelled (0.80) |
| Israel | IZ-ray-el | /ˈɪz.reɪ.əl/ | Genesis 32:28 |  | fine as spelled |
| Peniel | Peniel | /ˈpiː.naɪl/ | Genesis 32:30 |  | unsure (guessed IPA) (0.45) |
| Elohe | Elohe | /ˈiː.lə.hiː/ | Genesis 33:20 |  | unsure (guessed IPA) (0.40) |
| Hivite | HYvite | /ˈhaɪ.vaɪt/ | Genesis 34:2 | ✅ | overridden (1.00) |
| Beth | BETH | /bɛθ/ | Genesis 35:7 |  | fine as spelled (1.00) |
| Allon | AL-on | /ˈæl.ɒn/ | Genesis 35:8 |  | fine as spelled (1.00) |
| Bacuth | Bacuth | /ˈbeɪ.səθ/ | Genesis 35:8 |  | unsure (guessed IPA) (0.40) |
| Ephrath | EF-rath | /ˈɛf.ræθ/ | Genesis 35:16 |  | fine as spelled (0.80) |
| Benjamin | BEN-juh-min | /ˈbɛn.dʒə.mɪn/ | Genesis 35:18 |  | still wrong (0.75) |
| Benoni | Benoni | /bɛnˈoʊniː/ | Genesis 35:18 |  | still wrong (0.67) |
| Bethlehem | BETH-lih-hem | /ˈbɛθ.lɪ.hɛm/ | Genesis 35:19 |  | still wrong (0.75) |
| Eder | EE-der | /ˈiː.dər/ | Genesis 35:21 |  | suggestion waiting (0.75) |
| Anah | Aina | /ˈeɪ.nə/ | Genesis 36:2 | ✅ | overridden (1.00) |
| Oholibamah | oh-hol-ih-BAH-muh | /oʊˌhɒl.ɪˈbɑː.mə/ | Genesis 36:2 |  | still wrong (0.67) |
| Zibeon | ZIB-ee-uhn | /ˈzɪb.i.ən/ | Genesis 36:2 |  | fine as spelled (1.00) |
| Eliphaz | EL-ih-faz | /ˈɛl.ɪ.fæz/ | Genesis 36:4 |  | fine as spelled (0.92) |
| Reuel | ROO-el | /ˈruː.ɛl/ | Genesis 36:4 |  | fine as spelled (1.00) |
| Jalam | JAY-luhm | /ˈdʒeɪ.ləm/ | Genesis 36:5 |  | fine as spelled (0.80) |
| Jeush | JEE-uhsh | /ˈdʒiː.ʌʃ/ | Genesis 36:5 | ✅ | overridden (0.88) |
| Korah | KOR-uh | /ˈkɔːr.ə/ | Genesis 36:5 |  | fine as spelled |
| Gatam | GAY-tuhm | /ˈɡeɪ.təm/ | Genesis 36:11 | ✅ | overridden (1.00) |
| Kenaz | KEE-naz | /ˈkiː.næz/ | Genesis 36:11 | ✅ | overridden (0.90) |
| Omar | OH-mar | /ˈoʊ.mɑːr/ | Genesis 36:11 |  | fine as spelled (1.00) |
| Teman | TEE-muhn | /ˈtiː.mən/ | Genesis 36:11 |  | fine as spelled (0.80) |
| Zepho | Zepho | /ˈziː.fə/ | Genesis 36:11 |  | unsure (guessed IPA) (0.55) |
| Amalek | AM-uh-lek | /ˈæm.ə.lɛk/ | Genesis 36:12 |  | fine as spelled (0.92) |
| Timna | TIM-nuh | /ˈtɪm.nə/ | Genesis 36:12 |  | fine as spelled (0.90) |
| Mizzah | MIZ-uh | /ˈmɪz.ə/ | Genesis 36:13 |  | fine as spelled (0.90) |
| Nahath | nayhath | /ˈneɪ.hæθ/ | Genesis 36:13 | ✅ | overridden (0.90) |
| Shammah | SHAM-uh | /ˈʃæm.ə/ | Genesis 36:13 |  | still wrong (0.75) |
| Zerah | ZAIR-uh | /ˈzɪər.ə/ | Genesis 36:13 | ✅ | overridden (0.88) |
| Horite | Horite | /ˈhoʊ.ri.tiː/ | Genesis 36:20 |  | unsure (guessed IPA) (0.67) |
| Lotan | lohtan | /ˈloʊ.tæn/ | Genesis 36:20 | ✅ | overridden (0.82) |
| Shobal | SHOH-buhl | /ˈʃoʊ.bəl/ | Genesis 36:20 |  | fine as spelled (0.80) |
| Dishan | DEYE-shan | /ˈdaɪ.ʃæn/ | Genesis 36:21 | ✅ | overridden (0.80) |
| Dishon | DEYE-shon | /ˈdaɪ.ʃɒn/ | Genesis 36:21 | ✅ | overridden (1.00) |
| Ezer | EE-zer | /ˈiː.zər/ | Genesis 36:21 |  | suggestion waiting (0.75) |
| Heman | HEE-muhn | /ˈhiː.mən/ | Genesis 36:22 |  | suggestion waiting (0.67) |
| Hori | HOR-eye | /ˈhɔːr.aɪ/ | Genesis 36:22 | ✅ | overridden (0.75) |
| Ebal | EEbul | /ˈiː.bəl/ | Genesis 36:23 | ✅ | overridden (1.00) |
| Manahath | MAN-uh-hath | /ˈmæn.ə.hæθ/ | Genesis 36:23 |  | still wrong (0.71) |
| Onam | OH-nam | /ˈoʊ.næm/ | Genesis 36:23 |  | fine as spelled |
| Shepho | Shepho | /ˈʃiː.fə/ | Genesis 36:23 |  | unsure (guessed IPA) (0.78) |
| Aiah | ay-EYE-uh | /eɪˈaɪ.ə/ | Genesis 36:24 |  | still wrong (0.67) |
| Cheran | KEERR-an | /ˈkɪər.æn/ | Genesis 36:26 | ✅ | overridden (0.80) |
| Eshban | ESH-ban | /ˈɛʃ.bæn/ | Genesis 36:26 |  | still wrong (0.70) |
| Ithran | IHTH-ran | /ˈɪθ.ræn/ | Genesis 36:26 | ✅ | overridden (0.80) |
| Akan | Akan | /ˈækæn/ | Genesis 36:27 |  | still wrong (0.50) |
| Bilhan | BIL-han | /ˈbɪl.hæn/ | Genesis 36:27 |  | fine as spelled (0.83) |
| Zaavan | ZAY-uh-van | /ˈzeɪ.ə.væn/ | Genesis 36:27 | ✅ | overridden (0.83) |
| Aran | AIR-an | /ˈɛər.æn/ | Genesis 36:28 |  | still wrong (0.75) |
| Beor | BEE-or | /ˈbiː.ɔːr/ | Genesis 36:32 | ✅ | overridden (0.90) |
| Dinhabah | DIN-huh-buh | /ˈdɪn.hə.bə/ | Genesis 36:32 |  | still wrong (0.74) |
| Bozrah | BOZ-ruh | /ˈbɒz.rə/ | Genesis 36:33 |  | fine as spelled (1.00) |
| Husham | HYOO-shuhm | /ˈhjuː.ʃəm/ | Genesis 36:34 |  | still wrong (0.67) |
| Temanites | TEE-muh-nites | /ˈtiː.mə.naɪts/ | Genesis 36:34 |  | fine as spelled (0.88) |
| Avith | ayvith | /ˈeɪ.vɪθ/ | Genesis 36:35 | ✅ | overridden (1.00) |
| Bedad | BEE-dad | /ˈbiː.dæd/ | Genesis 36:35 |  | fine as spelled (0.80) |
| Masrekah | MAS-ruh-kuh | /ˈmæs.rə.kə/ | Genesis 36:36 |  | still wrong (0.67) |
| Samlah | SAM-luh | /ˈsæm.lə/ | Genesis 36:36 |  | fine as spelled (1.00) |
| Shaul | SHAY-uhll | /ˈʃeɪ.əl/ | Genesis 36:37 | ✅ | overridden (1.00) |
| Achbor | AK-bor | /ˈæk.bɔːr/ | Genesis 36:38 |  | still wrong (0.70) |
| Baal | bayal | /ˈbeɪ.əl/ | Genesis 36:38 | ✅ | overridden (1.00) |
| Hanan | haynan | /ˈheɪ.næn/ | Genesis 36:38 | ✅ | overridden (0.90) |
| Hadar | Hadar | /hˈædɚ/ | Genesis 36:39 |  | still wrong (0.40) |
| Matred | maytrehd | /ˈmeɪ.trɛd/ | Genesis 36:39 | ✅ | overridden (1.00) |
| Mehetabel | mahehtuhbehl | /məˈhɛt.ə.bɛl/ | Genesis 36:39 | ✅ | overridden (0.89) |
| Mezahab | MEZ-uh-hab | /ˈmɛz.ə.hæb/ | Genesis 36:39 |  | fine as spelled (0.93) |
| Pau | Pau | /ˈpɔː/ | Genesis 36:39 |  | unsure (guessed IPA) (0.25) |
| Alvah | Alvah | /ælvˈɑ/ | Genesis 36:40 |  | still wrong (0.75) |
| Jetheth | jeethehth | /ˈdʒiː.θɛθ/ | Genesis 36:40 | ✅ | overridden (0.80) |
| Elah | EE-luh | /ˈiː.lə/ | Genesis 36:41 |  | fine as spelled (0.83) |
| Pinon | peyenon | /ˈpaɪ.nɒn/ | Genesis 36:41 | ✅ | overridden (0.92) |
| Mibzar | MIB-zar | /ˈmɪb.zɑːr/ | Genesis 36:42 |  | fine as spelled (0.83) |
| Iram | eyeruhm | /ˈaɪ.rəm/ | Genesis 36:43 | ✅ | overridden (1.00) |
| Magdiel | MAG-dee-el | /ˈmæɡ.di.ɛl/ | Genesis 36:43 | ✅ | overridden (1.00) |
| Dothan | Dothan | /dˈɑθən/ | Genesis 37:17 |  | still wrong (0.60) |
| Ishmaelites | Ishmaelites | /i.ʃməˈiː.li.təs/ | Genesis 37:25 |  | unsure (guessed IPA) (0.50) |
| Midianites | Midianites | /mi.diˈeɪ.ni.təs/ | Genesis 37:28 |  | unsure (guessed IPA) (0.50) |
| Sheol | Sheol | /ˈʃi.oʊl/ | Genesis 37:35 |  | still wrong (0.75) |
| Potiphar | Potiphar | /ˈpɒt.ɪ.fɑː/ | Genesis 37:36 |  | still wrong (0.69) |
| Adullamite | Adullamite | /ə.dəlˈleɪ.mi.tiː/ | Genesis 38:1 |  | unsure (guessed IPA) (0.67) |
| Hirah | Hirah | /ˈhi.rəh/ | Genesis 38:1 |  | unsure (guessed IPA) (0.60) |
| Canaanite | Canaanite | /kˈeɪnənaɪt/ | Genesis 38:2 |  | still wrong (0.50) |
| Shua | shooa | /ˈʃuː.ə/ | Genesis 38:2 | ✅ | overridden (0.83) |
| Er | urr | /ɜːr/ | Genesis 38:3 | ✅ | overridden (1.00) |
| Onan | OH-nan | /ˈoʊ.næn/ | Genesis 38:4 |  | still wrong (0.75) |
| Chezib | kezib | /ˈkiː.zɪb/ | Genesis 38:5 | ✅ | overridden (0.80) |
| Enaim | Enaim | /ˈiː.neɪm/ | Genesis 38:14 |  | unsure (guessed IPA) (0.75) |
| Perez | PEE-rez | /ˈpiː.rɛz/ | Genesis 38:29 |  | fine as spelled (0.80) |
| Hebrews | Hebrews | /hˈiːbruːz/ | Genesis 40:15 |  | fine as spelled (1.00) |
| Asenath | Asenath | /ˈæsɪnæθ/ | Genesis 41:45 |  | still wrong (0.50) |
| Potiphera | Potiphera | /pəˈti.fə.rə/ | Genesis 41:45 |  | fine as spelled (0.88) |
| Zaphenath-Paneah | Zaphenath-Paneah | /ˈzeɪ.fə.nəθ.ˈpeɪ.niːh/ | Genesis 41:45 |  | unsure (guessed IPA) (0.58) |
| Manasseh | muh-NAS-uh | /məˈnæs.ə/ | Genesis 41:51 |  | fine as spelled (1.00) |
| Ephraim | eefray-ihmm | /ˈiː.freɪ.ɪm/ | Genesis 41:52 | ✅ | overridden (1.00) |
| Goshen | Goshen | /ɡˈoʊʃɪn/ | Genesis 45:10 |  | still wrong (0.40) |
| Carmi | KAR-my | /ˈkɑːr.maɪ/ | Genesis 46:9 |  | fine as spelled (1.00) |
| Hezron | HEZ-ron | /ˈhɛz.rɒn/ | Genesis 46:9 |  | fine as spelled (0.83) |
| Pallu | PAL-oo | /ˈpæl.uː/ | Genesis 46:9 |  | still wrong (0.75) |
| Jachin | JAY-kihn | /ˈdʒeɪ.kɪn/ | Genesis 46:10 | ✅ | overridden (1.00) |
| Jamin | JAY-mihn | /ˈdʒeɪ.mɪn/ | Genesis 46:10 | ✅ | overridden (1.00) |
| Ohad | Ohad | /ˈoʊ.həd/ | Genesis 46:10 |  | unsure (guessed IPA) (0.62) |
| Gershon | GUR-shon | /ˈɡɜːr.ʃɒn/ | Genesis 46:11 |  | fine as spelled (1.00) |
| Kohath | KOH-hath | /ˈkoʊ.hæθ/ | Genesis 46:11 |  | fine as spelled (0.90) |
| Merari | muh-RAY-reye | /məˈreɪ.raɪ/ | Genesis 46:11 | ✅ | overridden (1.00) |
| Hamul | HAY-muhl | /ˈheɪ.məl/ | Genesis 46:12 |  | fine as spelled (0.80) |
| Iob | Iob | /ˈi.əb/ | Genesis 46:13 |  | unsure (guessed IPA) (0.67) |
| Puvah | Puvah | /ˈpjuː.vəh/ | Genesis 46:13 |  | unsure (guessed IPA) (0.75) |
| Shimron | SHIM-ron | /ˈʃɪm.rɒn/ | Genesis 46:13 |  | fine as spelled (0.83) |
| Tola | TOH-luh | /ˈtoʊ.lə/ | Genesis 46:13 |  | fine as spelled (1.00) |
| Jahleel | Jahleel | /ˈdʒeɪ.liːl/ | Genesis 46:14 |  | unsure (guessed IPA) (0.45) |
| Areli | Areli | /ˈeɪ.rə.lə/ | Genesis 46:16 |  | unsure (guessed IPA) (0.40) |
| Arodi | Arodi | /ˈeɪ.rə.də/ | Genesis 46:16 |  | unsure (guessed IPA) (0.40) |
| Eri | Eri | /ˈiː.rə/ | Genesis 46:16 |  | unsure (guessed IPA) (0.33) |
| Ezbon | EZ-bon | /ˈɛz.bɒn/ | Genesis 46:16 |  | fine as spelled (0.80) |
| Haggi | Haggi | /ˈhæɡ.ɡə/ | Genesis 46:16 |  | unsure (guessed IPA) (0.75) |
| Shuni | Shuni | /ˈʃjuː.nə/ | Genesis 46:16 |  | unsure (guessed IPA) (0.60) |
| Beriah | buh-RY-uh | /bəˈraɪ.ə/ | Genesis 46:17 |  | fine as spelled (1.00) |
| Heber | HEE-ber | /ˈhiː.bər/ | Genesis 46:17 |  | fine as spelled (0.90) |
| Imnah | IM-nuh | /ˈɪm.nə/ | Genesis 46:17 |  | fine as spelled (1.00) |
| Ishvah | ISH-vuh | /ˈɪʃ.və/ | Genesis 46:17 |  | fine as spelled (1.00) |
| Ishvi | ihshveye | /ˈɪʃ.vaɪ/ | Genesis 46:17 | ✅ | overridden (1.00) |
| Malchiel | MAL-kee-el | /ˈmæl.ki.ɛl/ | Genesis 46:17 |  | suggestion waiting (0.71) |
| Serah | SEE-ruh | /ˈsɪər.ə/ | Genesis 46:17 |  | still wrong (0.75) |
| Ard | Ard | /ˈɑrd/ | Genesis 46:21 |  | fine as spelled (1.00) |
| Ashbel | ASH-bel | /ˈæʃ.bɛl/ | Genesis 46:21 |  | suggestion waiting (0.70) |
| Becher | beekuhr | /ˈbiː.kər/ | Genesis 46:21 | ✅ | overridden (1.00) |
| Ehi | Ehi | /ˈiː.hə/ | Genesis 46:21 |  | unsure (guessed IPA) (0.33) |
| Gera | GEE-ruh | /ˈɡɪər.ə/ | Genesis 46:21 |  | suggestion waiting (0.75) |
| Huppim | HUP-im | /ˈhʌp.ɪm/ | Genesis 46:21 |  | fine as spelled (0.80) |
| Muppim | Muppim | /ˈmʌp.pɪm/ | Genesis 46:21 |  | fine as spelled (0.80) |
| Naaman | NAY-uh-muhn | /ˈneɪ.ə.mən/ | Genesis 46:21 | ✅ | overridden (0.83) |
| Rosh | Rosh | /rˈɔʃ/ | Genesis 46:21 |  | fine as spelled (1.00) |
| Hushim | hyooshihm | /ˈhjuː.ʃɪm/ | Genesis 46:23 | ✅ | overridden (0.86) |
| Guni | GYOO-ny | /ˈɡjuː.naɪ/ | Genesis 46:24 |  | still wrong (0.50) |
| Jezer | JEE-zer | /ˈdʒiː.zər/ | Genesis 46:24 |  | fine as spelled (0.80) |
| Shillem | Shillem | /ˈʃɪl.ləm/ | Genesis 46:24 |  | fine as spelled (1.00) |
| Rameses | Rameses | /rˈæməsiːz/ | Genesis 47:11 |  | fine as spelled (0.86) |
| Atad | Atad | /ˈeɪ.təd/ | Genesis 50:10 |  | unsure (guessed IPA) (0.50) |
| Machir | maykuhr | /ˈmeɪ.kər/ | Genesis 50:23 | ✅ | overridden (1.00) |
| Raamses | Raamses | /ˈreɪ.əm.səs/ | Exodus 1:11 |  | unsure (guessed IPA) (0.29) |
| Puah | PYOO-uh | /ˈpjuː.ə/ | Exodus 1:15 |  | still wrong (0.25) |
| Shiphrah | Shiphrah | /ˈʃi.frəh/ | Exodus 1:15 |  | unsure (guessed IPA) (0.67) |
| Moses | MOH-ziz | /ˈmoʊ.zɪz/ | Exodus 2:10 |  | fine as spelled (1.00) |
| Zipporah | Zipporah | /ˈzɪpəɹə/ | Exodus 2:21 |  | fine as spelled (0.83) |
| Gershom | GUR-shuhm | /ˈɡɜːr.ʃəm/ | Exodus 2:22 |  | fine as spelled (0.83) |
| Jethro | Jethro | /dʒˈɛθroʊ/ | Exodus 3:1 |  | still wrong (0.65) |
| Jebusite | JEB-yoo-site | /ˈdʒɛb.jʊ.saɪt/ | Exodus 3:8 | ✅ | overridden (1.00) |
| Perizzite | Perizzite | /pəˈrɪz.zi.tiː/ | Exodus 3:8 |  | unsure (guessed IPA) (0.50) |
| Aaron | AIR-uhn | /ˈɛər.ən/ | Exodus 4:14 |  | fine as spelled (1.00) |
| fathers' | fathers | /ˈfɑː.ðərz/ | Exodus 6:14 | ✅ | overridden (1.00) |
| fathers’ | fathers | /ˈfɑː.ðərz/ | Exodus 6:14 | ✅ | overridden (1.00) |
| Libni | LIB-ny | /ˈlɪb.naɪ/ | Exodus 6:17 |  | fine as spelled (0.80) |
| Shimei | SHIM-ee-eye | /ˈʃɪm.i.aɪ/ | Exodus 6:17 |  | fine as spelled (0.80) |
| Amram | AM-ram | /ˈæm.ræm/ | Exodus 6:18 | ✅ | overridden (0.90) |
| Izhar | IZ-har | /ˈɪz.hɑːr/ | Exodus 6:18 |  | fine as spelled (0.80) |
| Uzziel | UZ-ee-el | /ˈʌz.i.ɛl/ | Exodus 6:18 |  | still wrong (0.70) |
| Levites | LEE-vites | /ˈliː.vaɪts/ | Exodus 6:19 |  | fine as spelled (1.00) |
| Mahli | MAH-ly | /ˈmɑː.laɪ/ | Exodus 6:19 |  | suggestion waiting (0.75) |
| Mushi | myoosheye | /ˈmjuː.ʃaɪ/ | Exodus 6:19 | ✅ | overridden (0.80) |
| Jochebed | Jochebed | /ˈjɒkɪbɛd/ | Exodus 6:20 |  | fine as spelled (0.86) |
| Nepheg | NEE-feg | /ˈniː.fɛɡ/ | Exodus 6:21 |  | fine as spelled (0.80) |
| Zichri | ZIHK-reye | /ˈzɪk.raɪ/ | Exodus 6:21 | ✅ | overridden (1.00) |
| Elzaphan | Elzaphan | /ˈɛl.zə.fən/ | Exodus 6:22 |  | fine as spelled (0.86) |
| Sithri | Sithri | /ˈsi.θrə/ | Exodus 6:22 |  | unsure (guessed IPA) (0.60) |
| Abihu | uh-BY-hyoo | /əˈbaɪ.hjuː/ | Exodus 6:23 |  | still wrong (0.67) |
| Amminadab | uh-MIHN-uh-dab | /əˈmɪn.ə.dæb/ | Exodus 6:23 | ✅ | overridden (1.00) |
| Eleazar | el-ee-AY-zer | /ˌɛl.iˈeɪ.zər/ | Exodus 6:23 |  | fine as spelled (1.00) |
| Elisheba | Elisheba | /əˈli.ʃə.bə/ | Exodus 6:23 |  | fine as spelled (0.86) |
| Ithamar | ITH-uh-mar | /ˈɪθ.ə.mɑːr/ | Exodus 6:23 |  | fine as spelled (1.00) |
| Nadab | NAY-dab | /ˈneɪ.dæb/ | Exodus 6:23 |  | fine as spelled (1.00) |
| Nahshon | NAH-shon | /ˈnɑː.ʃɒn/ | Exodus 6:23 | ✅ | overridden (1.00) |
| Abiasaph | Abiasaph | /əˈbi.ə.səf/ | Exodus 6:24 |  | unsure (guessed IPA) (0.71) |
| Assir | AS-ur | /ˈæs.ər/ | Exodus 6:24 |  | still wrong (0.62) |
| Elkanah | el-KAY-nuh | /ɛlˈkeɪ.nə/ | Exodus 6:24 | ✅ | overridden (0.92) |
| Korahites | KOR-uh-hites | /ˈkɔːr.ə.haɪts/ | Exodus 6:24 |  | fine as spelled (0.88) |
| Phinehas | FIN-ee-uhs | /ˈfɪn.i.əs/ | Exodus 6:25 |  | suggestion waiting (0.71) |
| Putiel | Putiel | /ˈpjuː.taɪl/ | Exodus 6:25 |  | unsure (guessed IPA) (0.57) |
| Israelites | Israelites | /ˈɪzrəlaɪts/ | Exodus 9:7 |  | fine as spelled (0.83) |
| Passover | Passover | /pˈæsoʊvɚ/ | Exodus 12:11 |  | fine as spelled (1.00) |
| Abib | Abib | /ˈeɪ.bɪb/ | Exodus 13:4 |  | unsure (guessed IPA) (0.50) |
| Etham | Etham | /ˈiː.θəm/ | Exodus 13:20 |  | unsure (guessed IPA) (0.75) |
| Migdol | Migdol | /ˈmɪɡ.dəl/ | Exodus 14:2 |  | fine as spelled (0.83) |
| Pihahiroth | Pihahiroth | /piˈheɪ.hi.rəθ/ | Exodus 14:2 |  | unsure (guessed IPA) (0.56) |
| Zephon | Zephon | /ˈziː.fən/ | Exodus 14:2 |  | unsure (guessed IPA) (0.70) |
| Philistia | Philistia | /fɪlˈɪstiːə/ | Exodus 15:14 |  | fine as spelled (1.00) |
| Miriam | MIR-ee-uhm | /ˈmɪr.i.əm/ | Exodus 15:20 |  | fine as spelled (1.00) |
| Marah | Marah | /ˈmɑːɹə/ | Exodus 15:23 |  | fine as spelled (1.00) |
| Elim | Elim | /ˈiː.lɪm/ | Exodus 15:27 |  | unsure (guessed IPA) (0.50) |
| Rephidim | Rephidim | /ˈriː.fi.dɪm/ | Exodus 17:1 |  | unsure (guessed IPA) (0.64) |
| Nile | Nile | /nˈaɪl/ | Exodus 17:5 |  | fine as spelled (1.00) |
| Massah | Massah | /ˈmæs.səh/ | Exodus 17:7 |  | fine as spelled (0.80) |
| Meribah | Meribah | /ˈmiː.ri.bəh/ | Exodus 17:7 |  | unsure (guessed IPA) (0.71) |
| Joshua | JOSH-oo-uh | /ˈdʒɒʃ.u.ə/ | Exodus 17:9 |  | fine as spelled (0.92) |
| Hur | HUR | /hɜːr/ | Exodus 17:10 |  | still wrong (0.67) |
| Meeting | Meeting | /mˈiːtɪŋ/ | Exodus 27:21 |  | fine as spelled (0.80) |
| Thummim | Thummim | /ˈθʌm.mɪm/ | Exodus 28:30 |  | unsure (guessed IPA) (0.70) |
| Urim | Urim | /ˈjuː.rɪm/ | Exodus 28:30 |  | fine as spelled (0.80) |
| YAHWEH | YAHWEH | /jˈɑwɛ/ | Exodus 28:36 |  | still wrong (0.62) |
| Bezalel | BEZ-uh-lel | /ˈbɛz.ə.lɛl/ | Exodus 31:2 |  | still wrong (0.71) |
| Uri | YOORR-eye | /ˈjʊər.aɪ/ | Exodus 31:2 | ✅ | overridden (0.75) |
| Ahisamach | Ahisamach | /əˈhi.sə.mək/ | Exodus 31:6 |  | unsure (guessed IPA) (0.56) |
| Oholiab | Oholiab | /əˈhoʊ.li.əb/ | Exodus 31:6 |  | unsure (guessed IPA) (0.71) |
| Sabbaths | Sabbaths | /sˈæbəθs/ | Exodus 31:13 |  | fine as spelled (0.92) |
| Nun | NUHN | /nʌn/ | Exodus 33:11 |  | fine as spelled (1.00) |
| Mishael | Mishael | /ˈmi.ʃə.əl/ | Leviticus 10:4 |  | unsure (guessed IPA) (0.33) |
| Molech | Molech | /ˈmoʊ.lək/ | Leviticus 18:21 |  | fine as spelled (0.80) |
| Israelite | Israelite | /ˈɪzrəlaɪt/ | Leviticus 24:10 |  | still wrong (0.75) |
| Dibri | Dibri | /ˈdɪb.rə/ | Leviticus 24:11 |  | unsure (guessed IPA) (0.73) |
| Shelomith | shuh-LOH-mith | /ʃəˈloʊ.mɪθ/ | Leviticus 24:11 |  | suggestion waiting (0.71) |
| Shedeur | Shedeur | /ˈʃiː.djuːr/ | Numbers 1:5 |  | unsure (guessed IPA) (0.50) |
| Zurishaddai | Zurishaddai | /zəˈri.ʃəd.deɪ/ | Numbers 1:6 |  | unsure (guessed IPA) (0.62) |
| Nethanel | nuh-THAN-el | /nəˈθæn.əl/ | Numbers 1:8 |  | still wrong (0.71) |
| Zuar | Zuar | /ˈzjuː.ər/ | Numbers 1:8 |  | fine as spelled (0.80) |
| Eliab | ee-LY-ab | /ɪˈlaɪ.æb/ | Numbers 1:9 |  | fine as spelled (0.80) |
| Helon | Helon | /ˈhiː.lən/ | Numbers 1:9 |  | fine as spelled (0.80) |
| Ammihud | ameyehuhd | /əˈmaɪ.hʌd/ | Numbers 1:10 | ✅ | overridden (1.00) |
| Elishama | ihlihshuhmuh | /ɪˈlɪʃ.ə.mə/ | Numbers 1:10 | ✅ | overridden (0.86) |
| Pedahzur | Pedahzur | /ˈpiː.də.zər/ | Numbers 1:10 |  | unsure (guessed IPA) (0.57) |
| Gideoni | Gideoni | /ɡiˈdiː.ə.nə/ | Numbers 1:11 |  | unsure (guessed IPA) (0.57) |
| Ammishaddai | Ammishaddai | /əmˈmi.ʃəd.deɪ/ | Numbers 1:12 |  | unsure (guessed IPA) (0.43) |
| Ochran | Ochran | /ˈoʊ.krən/ | Numbers 1:13 |  | fine as spelled (0.80) |
| Deuel | Deuel | /dˈuːɛl/ | Numbers 1:14 |  | still wrong (0.75) |
| Enan | Enan | /ˈiː.nən/ | Numbers 1:15 |  | unsure (guessed IPA) (0.50) |
| Elizur | Elizur | /ˈiː.li.zər/ | Numbers 2:10 |  | unsure (guessed IPA) (0.67) |
| Shelumiel | Shelumiel | /ʃəˈljuː.maɪl/ | Numbers 2:12 |  | unsure (guessed IPA) (0.56) |
| Eliasaph | Eliasaph | /əˈli.ə.səf/ | Numbers 2:14 |  | unsure (guessed IPA) (0.29) |
| Abidan | Abidan | /ˈeɪ.bi.dən/ | Numbers 2:22 |  | unsure (guessed IPA) (0.50) |
| Pagiel | Pagiel | /ˈpeɪ.ɡaɪl/ | Numbers 2:27 |  | unsure (guessed IPA) (0.33) |
| Ahira | Ahira | /ˈeɪ.hi.rə/ | Numbers 2:29 |  | unsure (guessed IPA) (0.60) |
| Libnites | Libnites | /ˈlɪb.ni.təs/ | Numbers 3:21 |  | unsure (guessed IPA) (0.62) |
| Shimeites | Shimeites | /ˈʃi.maɪ.təs/ | Numbers 3:21 |  | unsure (guessed IPA) (0.71) |
| Lael | Lael | /ˈleɪ.əl/ | Numbers 3:24 |  | unsure (guessed IPA) (0.50) |
| Kohathites | KOH-hath-ites | /ˈkoʊ.hæθ.aɪts/ | Numbers 3:27 |  | fine as spelled (0.88) |
| Mahlites | Mahlites | /ˈmeɪ.li.təs/ | Numbers 3:33 |  | unsure (guessed IPA) (0.57) |
| Mushites | Mushites | /ˈmjuː.ʃi.təs/ | Numbers 3:33 |  | unsure (guessed IPA) (0.44) |
| Abihail | ab-ih-HAY-il | /ˌæb.ɪˈheɪ.ɪl/ | Numbers 3:35 |  | still wrong (0.57) |
| Zuriel | Zuriel | /ˈzjuː.raɪl/ | Numbers 3:35 |  | unsure (guessed IPA) (0.50) |
| Nazirite | Nazirite | /nəˈzi.ri.tiː/ | Numbers 6:2 |  | unsure (guessed IPA) (0.50) |
| Hobab | Hobab | /ˈhoʊ.bəb/ | Numbers 10:29 |  | fine as spelled (0.80) |
| Midianite | Midianite | /mi.diˈeɪ.ni.tiː/ | Numbers 10:29 |  | unsure (guessed IPA) (0.50) |
| Taberah | Taberah | /ˈteɪ.bə.rəh/ | Numbers 11:3 |  | unsure (guessed IPA) (0.64) |
| Eldad | Eldad | /ˈɛl.dəd/ | Numbers 11:26 |  | unsure (guessed IPA) (0.70) |
| Medad | Medad | /ˈmiː.dəd/ | Numbers 11:26 |  | unsure (guessed IPA) (0.60) |
| Hattaavah | Hattaavah | /hətˈteɪ.ə.vəh/ | Numbers 11:34 |  | unsure (guessed IPA) (0.29) |
| Kibroth | Kibroth | /ˈkɪb.rəθ/ | Numbers 11:34 |  | unsure (guessed IPA) (0.67) |
| Hazeroth | Hazeroth | /ˈheɪ.zə.rəθ/ | Numbers 11:35 |  | unsure (guessed IPA) (0.64) |
| Cushite | Cushite | /ˈsjuː.ʃi.tiː/ | Numbers 12:1 |  | unsure (guessed IPA) (0.36) |
| Shammua | Shammua | /ˈʃæm.mə.ə/ | Numbers 13:4 |  | unsure (guessed IPA) (0.58) |
| Zaccur | ZAK-er | /ˈzæk.ər/ | Numbers 13:4 |  | fine as spelled (1.00) |
| Shaphat | SHAY-fat | /ˈʃeɪ.fæt/ | Numbers 13:5 | ✅ | overridden (1.00) |
| Caleb | KAY-leb | /ˈkeɪ.ləb/ | Numbers 13:6 |  | fine as spelled (1.00) |
| Jephunneh | juh-FUN-uh | /dʒəˈfʌn.ə/ | Numbers 13:6 |  | fine as spelled (0.83) |
| Igal | EYE-gal | /ˈaɪ.ɡæl/ | Numbers 13:7 |  | still wrong (0.50) |
| Palti | Palti | /ˈpæl.tə/ | Numbers 13:9 |  | unsure (guessed IPA) (0.60) |
| Raphu | Raphu | /ˈreɪ.fə/ | Numbers 13:9 |  | unsure (guessed IPA) (0.55) |
| Gaddiel | Gaddiel | /ˈɡæd.daɪl/ | Numbers 13:10 |  | unsure (guessed IPA) (0.63) |
| Sodi | Sodi | /ˈsoʊ.də/ | Numbers 13:10 |  | unsure (guessed IPA) (0.75) |
| Gaddi | Gaddi | /ˈɡæd.də/ | Numbers 13:11 |  | unsure (guessed IPA) (0.50) |
| Susi | Susi | /sˈuːsiː/ | Numbers 13:11 |  | still wrong (0.75) |
| Ammiel | AM-ee-el | /ˈæm.i.ɛl/ | Numbers 13:12 |  | still wrong (0.70) |
| Gemalli | Gemalli | /ˈɡiː.məl.lə/ | Numbers 13:12 |  | unsure (guessed IPA) (0.33) |
| Michael | MY-kuhl | /ˈmaɪ.kəl/ | Numbers 13:13 |  | fine as spelled (1.00) |
| Sethur | Sethur | /ˈsiː.θər/ | Numbers 13:13 |  | unsure (guessed IPA) (0.70) |
| Nahbi | Nahbi | /ˈneɪ.bə/ | Numbers 13:14 |  | unsure (guessed IPA) (0.50) |
| Vophsi | Vophsi | /ˈvoʊ.fsə/ | Numbers 13:14 |  | unsure (guessed IPA) (0.60) |
| Geuel | Geuel | /ˈɡjuː.əl/ | Numbers 13:15 |  | unsure (guessed IPA) (0.40) |
| Machi | Machi | /mˈɑkiː/ | Numbers 13:15 |  | fine as spelled (1.00) |
| Rehob | REE-hob | /ˈriː.hɒb/ | Numbers 13:21 |  | fine as spelled (0.90) |
| Zin | Zin | /ˈzɪn/ | Numbers 13:21 |  | fine as spelled (1.00) |
| Ahiman | uh-HY-muhn | /əˈhaɪ.mən/ | Numbers 13:22 |  | fine as spelled (1.00) |
| Anak | Anak | /ˈeɪnæk/ | Numbers 13:22 |  | still wrong (0.50) |
| Sheshai | Sheshai | /ˈʃiːˌʃaɪ/ | Numbers 13:22 |  | still wrong (0.75) |
| Talmai | TAL-my | /ˈtæl.maɪ/ | Numbers 13:22 |  | fine as spelled (1.00) |
| Zoan | Zoan | /ˈzoʊn/ | Numbers 13:22 |  | unsure (guessed IPA) (0.75) |
| Amalekite | Amalekite | /ə.məˈliː.ki.tiː/ | Numbers 14:25 |  | unsure (guessed IPA) (0.44) |
| Hormah | HOR-muh | /ˈhɔːr.mə/ | Numbers 14:45 |  | still wrong (0.60) |
| Abiram | Abiram | /ˈeɪ.bi.rəm/ | Numbers 16:1 |  | unsure (guessed IPA) (0.67) |
| Dathan | Dathan | /ˈdeɪ.θən/ | Numbers 16:1 |  | fine as spelled (1.00) |
| Peleth | PEE-lehth | /ˈpiː.lɛθ/ | Numbers 16:1 | ✅ | overridden (0.80) |
| Hor | Hor | /ˈhɒr/ | Numbers 20:22 |  | unsure (guessed IPA) (0.17) |
| Arad | AIR-ad | /ˈɛər.æd/ | Numbers 21:1 |  | still wrong (0.50) |
| Atharim | Atharim | /ˈeɪ.θə.rɪm/ | Numbers 21:1 |  | unsure (guessed IPA) (0.46) |
| Oboth | Oboth | /ˈoʊ.bəθ/ | Numbers 21:10 |  | fine as spelled (0.88) |
| Iyeabarim | Iyeabarim | /i.əˈiː.bə.rɪm/ | Numbers 21:11 |  | unsure (guessed IPA) (0.50) |
| Zered | Zered | /ˈziː.rəd/ | Numbers 21:12 |  | unsure (guessed IPA) (0.60) |
| Arnon | Arnon | /ˈær.nən/ | Numbers 21:13 |  | unsure (guessed IPA) (0.60) |
| Suphah | Suphah | /ˈsjuː.fəh/ | Numbers 21:14 |  | unsure (guessed IPA) (0.67) |
| Ar | Ar | /ˈɑr/ | Numbers 21:15 |  | still wrong (0.67) |
| Mattanah | Mattanah | /ˈmæt.tə.nəh/ | Numbers 21:18 |  | unsure (guessed IPA) (0.64) |
| Bamoth | Bamoth | /ˈbeɪ.məθ/ | Numbers 21:19 |  | unsure (guessed IPA) (0.70) |
| Nahaliel | Nahaliel | /nəˈheɪ.laɪl/ | Numbers 21:19 |  | unsure (guessed IPA) (0.71) |
| Pisgah | Pisgah | /ˈpɪs.ɡəh/ | Numbers 21:20 |  | unsure (guessed IPA) (0.67) |
| Sihon | Sihon | /ˈsi.hən/ | Numbers 21:21 |  | unsure (guessed IPA) (0.40) |
| Jahaz | Jahaz | /ˈdʒeɪ.həz/ | Numbers 21:23 |  | unsure (guessed IPA) (0.60) |
| Heshbon | HEHSH-bon | /ˈhɛʃ.bɒn/ | Numbers 21:25 | ✅ | overridden (1.00) |
| Chemosh | Chemosh | /ˈkiː.məʃ/ | Numbers 21:29 |  | fine as spelled (0.80) |
| Dibon | Dibon | /ˈdi.bən/ | Numbers 21:30 |  | fine as spelled (0.80) |
| Nophah | Nophah | /ˈnoʊ.fəh/ | Numbers 21:30 |  | fine as spelled (0.80) |
| Jazer | JAY-zer | /ˈdʒeɪ.zər/ | Numbers 21:32 |  | fine as spelled (0.80) |
| Bashan | BAY-shan | /ˈbeɪ.ʃæn/ | Numbers 21:33 |  | fine as spelled (0.80) |
| Edrei | Edrei | /ˈɛd.raɪ/ | Numbers 21:33 |  | fine as spelled (0.80) |
| Jericho | JER-ih-koh | /ˈdʒɛr.ɪ.koʊ/ | Numbers 22:1 |  | fine as spelled (1.00) |
| Balak | Balak | /bɑlək/ | Numbers 22:2 |  | still wrong (0.60) |
| Zippor | Zippor | /ˈzɪp.pər/ | Numbers 22:2 |  | fine as spelled (0.83) |
| Balaam | Balaam | /ˈbeɪləm/ | Numbers 22:5 |  | still wrong (0.40) |
| Pethor | Pethor | /ˈpiː.θər/ | Numbers 22:5 |  | unsure (guessed IPA) (0.70) |
| Huzoth | Huzoth | /ˈhjuː.zəθ/ | Numbers 22:39 |  | unsure (guessed IPA) (0.33) |
| Zophim | Zophim | /ˈzoʊ.fɪm/ | Numbers 23:14 |  | fine as spelled (0.90) |
| Peor | Peor | /ˈpiː.ər/ | Numbers 23:28 |  | unsure (guessed IPA) (0.62) |
| Agag | Agag | /ˈeɪɡæɡ/ | Numbers 24:7 |  | fine as spelled (0.88) |
| Kenite | Kenite | /ˈkiː.ni.tiː/ | Numbers 24:21 |  | unsure (guessed IPA) (0.58) |
| Kain | Kain | /kˈeɪn/ | Numbers 24:22 |  | fine as spelled (0.83) |
| Shittim | Shittim | /ˈʃɪt.tɪm/ | Numbers 25:1 |  | unsure (guessed IPA) (0.60) |
| Salu | Salu | /ˈseɪ.lə/ | Numbers 25:14 |  | unsure (guessed IPA) (0.50) |
| Zimri | zihmreye | /ˈzɪm.raɪ/ | Numbers 25:14 | ✅ | overridden (1.00) |
| Cozbi | Cozbi | /ˈsɒz.bə/ | Numbers 25:15 |  | unsure (guessed IPA) (0.60) |
| Zur | zurr | /zɜːr/ | Numbers 25:15 | ✅ | overridden (1.00) |
| Hanochites | Hanochites | /həˈnoʊ.ki.təs/ | Numbers 26:5 |  | unsure (guessed IPA) (0.56) |
| Palluites | Palluites | /ˈpæl.luː.təs/ | Numbers 26:5 |  | unsure (guessed IPA) (0.47) |
| Carmites | Carmites | /ˈsær.mi.təs/ | Numbers 26:6 |  | unsure (guessed IPA) (0.50) |
| Hezronites | Hezronites | /həzˈroʊ.ni.təs/ | Numbers 26:6 |  | unsure (guessed IPA) (0.60) |
| Reubenites | ROO-ben-ites | /ˈruː.bən.aɪts/ | Numbers 26:7 |  | fine as spelled (0.84) |
| Nemuel | NEM-yoo-el | /ˈnɛm.jʊ.əl/ | Numbers 26:9 |  | still wrong (0.73) |
| Jachinites | Jachinites | /dʒəˈki.ni.təs/ | Numbers 26:12 |  | unsure (guessed IPA) (0.56) |
| Jaminites | Jaminites | /dʒəˈmi.ni.təs/ | Numbers 26:12 |  | unsure (guessed IPA) (0.56) |
| Nemuelites | Nemuelites | /nə.məˈiː.li.təs/ | Numbers 26:12 |  | unsure (guessed IPA) (0.40) |
| Shaulites | Shaulites | /ˈʃɔː.li.təs/ | Numbers 26:13 |  | unsure (guessed IPA) (0.64) |
| Haggites | Haggites | /ˈhæɡ.ɡi.təs/ | Numbers 26:15 |  | unsure (guessed IPA) (0.71) |
| Shunites | Shunites | /ˈʃjuː.ni.təs/ | Numbers 26:15 |  | unsure (guessed IPA) (0.38) |
| Zephonites | Zephonites | /zəˈfoʊ.ni.təs/ | Numbers 26:15 |  | unsure (guessed IPA) (0.56) |
| Erites | Erites | /ˈiː.ri.təs/ | Numbers 26:16 |  | unsure (guessed IPA) (0.50) |
| Ozni | Ozni | /ˈɒz.nə/ | Numbers 26:16 |  | unsure (guessed IPA) (0.75) |
| Oznites | Oznites | /ˈɒz.ni.təs/ | Numbers 26:16 |  | unsure (guessed IPA) (0.71) |
| Arelites | Arelites | /əˈriː.li.təs/ | Numbers 26:17 |  | unsure (guessed IPA) (0.50) |
| Arod | Arod | /ˈeɪ.rəd/ | Numbers 26:17 |  | unsure (guessed IPA) (0.50) |
| Arodites | Arodites | /əˈroʊ.di.təs/ | Numbers 26:17 |  | unsure (guessed IPA) (0.50) |
| Perezites | perezitess | /pəˈriː.zi.təs/ | Numbers 26:20 | ✅ | overridden (0.72) |
| Shelanites | Shelanites | /ʃəˈleɪ.ni.təs/ | Numbers 26:20 |  | unsure (guessed IPA) (0.56) |
| Hamulites | Hamulites | /həˈmjuː.li.təs/ | Numbers 26:21 |  | unsure (guessed IPA) (0.70) |
| Punites | Punites | /ˈpjuː.ni.təs/ | Numbers 26:23 |  | unsure (guessed IPA) (0.44) |
| Tolaites | Tolaites | /ˈtoʊ.leɪ.təs/ | Numbers 26:23 |  | unsure (guessed IPA) (0.57) |
| Jashub | JAY-shub | /ˈdʒeɪ.ʃʌb/ | Numbers 26:24 |  | fine as spelled (0.80) |
| Jashubites | Jashubites | /dʒəˈʃjuː.bi.təs/ | Numbers 26:24 |  | unsure (guessed IPA) (0.55) |
| Shimronites | Shimronites | /ʃɪmˈroʊ.ni.təs/ | Numbers 26:24 |  | fine as spelled (0.80) |
| Elonites | Elonites | /əˈloʊ.ni.təs/ | Numbers 26:26 |  | unsure (guessed IPA) (0.44) |
| Jahleelites | Jahleelites | /dʒəˈliː.li.təs/ | Numbers 26:26 |  | unsure (guessed IPA) (0.56) |
| Sered | Sered | /ˈsiː.rəd/ | Numbers 26:26 |  | unsure (guessed IPA) (0.60) |
| Seredites | Seredites | /səˈriː.di.təs/ | Numbers 26:26 |  | unsure (guessed IPA) (0.50) |
| Zebulunites | Zebulunites | /zə.bəˈljuː.ni.təs/ | Numbers 26:27 |  | unsure (guessed IPA) (0.42) |
| Gileadites | Gileadites | /ɡiˈliː.di.təs/ | Numbers 26:29 |  | unsure (guessed IPA) (0.50) |
| Machirites | Machirites | /məˈki.ri.təs/ | Numbers 26:29 |  | unsure (guessed IPA) (0.67) |
| Helek | Helek | /ˈhiː.lək/ | Numbers 26:30 |  | unsure (guessed IPA) (0.60) |
| Helekites | helekitess | /həˈliː.ki.təs/ | Numbers 26:30 | ✅ | overridden (0.56) |
| Iezer | Iezer | /ˈaɪ.zər/ | Numbers 26:30 |  | unsure (guessed IPA) (0.68) |
| Iezerites | Iezerites | /aɪˈziː.ri.təs/ | Numbers 26:30 |  | unsure (guessed IPA) (0.50) |
| Asriel | AS-ree-el | /ˈæs.ri.ɛl/ | Numbers 26:31 |  | still wrong (0.67) |
| Asrielites | Asrielites | /əsˈraɪ.li.təs/ | Numbers 26:31 |  | unsure (guessed IPA) (0.56) |
| Shechemites | shekemites | /ʃəˈkiː.mi.təs/ | Numbers 26:31 | ✅ | overridden (0.56) |
| Hepher | HEE-fer | /ˈhiː.fər/ | Numbers 26:32 |  | fine as spelled (0.80) |
| Hepherites | Hepherites | /həˈfiː.ri.təs/ | Numbers 26:32 |  | unsure (guessed IPA) (0.44) |
| Shemida | shuh-MY-duh | /ʃəˈmaɪ.də/ | Numbers 26:32 | ✅ | overridden (0.83) |
| Shemidaites | Shemidaites | /ʃəˈmi.deɪ.təs/ | Numbers 26:32 |  | fine as spelled (0.89) |
| Hoglah | Hoglah | /ˈhɒɡ.ləh/ | Numbers 26:33 |  | fine as spelled (0.83) |
| Mahlah | MAH-luh | /ˈmɑː.lə/ | Numbers 26:33 |  | fine as spelled (1.00) |
| Tirzah | Tirzah | /ˈtɪr.zəh/ | Numbers 26:33 |  | unsure (guessed IPA) (0.50) |
| Zelophehad | zuh-LOH-fuh-had | /zəˈloʊ.fə.hæd/ | Numbers 26:33 | ✅ | overridden (0.83) |
| Becherites | bekerites | /bəˈkiː.ri.təs/ | Numbers 26:35 | ✅ | overridden (0.56) |
| Shuthelah | shoo-THEE-luh | /ʃuːˈθiː.lə/ | Numbers 26:35 |  | still wrong (0.62) |
| Shuthelahites | Shuthelahites | /ʃə.θəˈleɪ.hi.təs/ | Numbers 26:35 |  | unsure (guessed IPA) (0.46) |
| Tahan | TAY-han | /ˈteɪ.hæn/ | Numbers 26:35 | ✅ | overridden (0.80) |
| Tahanites | Tahanites | /təˈheɪ.ni.təs/ | Numbers 26:35 |  | unsure (guessed IPA) (0.39) |
| Eran | Eran | /ˈiː.rən/ | Numbers 26:36 |  | unsure (guessed IPA) (0.50) |
| Eranites | Eranites | /əˈreɪ.ni.təs/ | Numbers 26:36 |  | unsure (guessed IPA) (0.56) |
| Ahiram | Ahiram | /ˈeɪ.hi.rəm/ | Numbers 26:38 |  | unsure (guessed IPA) (0.50) |
| Ahiramites | Ahiramites | /ə.hiˈreɪ.mi.təs/ | Numbers 26:38 |  | unsure (guessed IPA) (0.60) |
| Ashbelites | Ashbelites | /əˈʃbiː.li.təs/ | Numbers 26:38 |  | unsure (guessed IPA) (0.33) |
| Belaites | Belaites | /ˈbiː.leɪ.təs/ | Numbers 26:38 |  | unsure (guessed IPA) (0.29) |
| Hupham | Hupham | /ˈhjuː.fəm/ | Numbers 26:39 |  | unsure (guessed IPA) (0.33) |
| Huphamites | Huphamites | /həˈfeɪ.mi.təs/ | Numbers 26:39 |  | unsure (guessed IPA) (0.33) |
| Shephupham | Shephupham | /ˈʃiː.fə.fəm/ | Numbers 26:39 |  | unsure (guessed IPA) (0.40) |
| Shuphamites | Shuphamites | /ʃəˈfeɪ.mi.təs/ | Numbers 26:39 |  | unsure (guessed IPA) (0.11) |
| Ardites | Ardites | /ˈær.di.təs/ | Numbers 26:40 |  | unsure (guessed IPA) (0.50) |
| Naamites | Naamites | /nəˈeɪ.mi.təs/ | Numbers 26:40 |  | unsure (guessed IPA) (0.50) |
| Shuham | Shuham | /ˈʃjuː.həm/ | Numbers 26:42 |  | unsure (guessed IPA) (0.67) |
| Shuhamites | Shuhamites | /ʃəˈheɪ.mi.təs/ | Numbers 26:42 |  | unsure (guessed IPA) (0.39) |
| Berites | Berites | /ˈbiː.ri.təs/ | Numbers 26:44 |  | unsure (guessed IPA) (0.14) |
| Imnites | Imnites | /ˈɪm.ni.təs/ | Numbers 26:44 |  | unsure (guessed IPA) (0.71) |
| Ishvites | Ishvites | /ˈi.ʃvi.təs/ | Numbers 26:44 |  | unsure (guessed IPA) (0.57) |
| Heberites | Heberites | /həˈbiː.ri.təs/ | Numbers 26:45 |  | unsure (guessed IPA) (0.44) |
| Malchielites | malkielites | /məlˈkaɪ.li.təs/ | Numbers 26:45 | ✅ | overridden (0.40) |
| Gunites | Gunites | /ˈɡjuː.ni.təs/ | Numbers 26:48 |  | unsure (guessed IPA) (0.50) |
| Jahzeel | Jahzeel | /ˈdʒeɪ.ziːl/ | Numbers 26:48 |  | unsure (guessed IPA) (0.63) |
| Jahzeelites | Jahzeelites | /dʒəˈziː.li.təs/ | Numbers 26:48 |  | unsure (guessed IPA) (0.56) |
| Jezerites | Jezerites | /dʒəˈziː.ri.təs/ | Numbers 26:49 |  | unsure (guessed IPA) (0.56) |
| Shillemites | Shillemites | /ʃɪlˈliː.mi.təs/ | Numbers 26:49 |  | unsure (guessed IPA) (0.67) |
| Merarites | Merarites | /məˈreɪ.ri.təs/ | Numbers 26:57 |  | unsure (guessed IPA) (0.56) |
| Abarim | Abarim | /ˈeɪ.bə.rɪm/ | Numbers 27:12 |  | unsure (guessed IPA) (0.58) |
| Reba | Reba | /rˈiːbə/ | Numbers 31:8 |  | fine as spelled (1.00) |
| Rekem | REE-kem | /ˈriː.kɛm/ | Numbers 31:8 |  | fine as spelled (0.80) |
| Beon | Beon | /ˈbiː.ən/ | Numbers 32:3 |  | unsure (guessed IPA) (0.75) |
| Elealeh | Elealeh | /ˈiː.liː.ləh/ | Numbers 32:3 |  | unsure (guessed IPA) (0.50) |
| Nebo | NEE-boh | /ˈniː.boʊ/ | Numbers 32:3 |  | fine as spelled (1.00) |
| Nimrah | Nimrah | /ˈnɪm.rəh/ | Numbers 32:3 |  | fine as spelled (0.83) |
| Sebam | Sebam | /ˈsiː.bəm/ | Numbers 32:3 |  | fine as spelled (1.00) |
| Barnea | Barnea | /ˈbær.niː/ | Numbers 32:8 |  | unsure (guessed IPA) (0.58) |
| Kenizzite | Kenizzite | /kəˈnɪz.zi.tiː/ | Numbers 32:12 |  | unsure (guessed IPA) (0.56) |
| Og | ogh | /ˈɑɡ/ | Numbers 32:33 | ✅ | overridden (1.00) |
| Aroer | uh-ROH-uhrr | /əˈroʊ.ər/ | Numbers 32:34 | ✅ | overridden (1.00) |
| Jogbehah | Jogbehah | /ˈdʒɒɡ.bə.həh/ | Numbers 32:35 |  | unsure (guessed IPA) (0.38) |
| Meon | MEE-on | /ˈmiː.ɒn/ | Numbers 32:38 |  | suggestion waiting (0.75) |
| Sibmah | Sibmah | /ˈsɪb.məh/ | Numbers 32:38 |  | fine as spelled (0.83) |
| Havvoth | Havvoth | /ˈhæv.vəθ/ | Numbers 32:41 |  | fine as spelled (0.80) |
| Jair | jayuhr | /ˈdʒeɪ.ər/ | Numbers 32:41 | ✅ | overridden (1.00) |
| Kenath | KEE-naath | /ˈkiː.næθ/ | Numbers 32:42 | ✅ | overridden (0.70) |
| Nobah | Nobah | /ˈnoʊ.bəh/ | Numbers 32:42 |  | fine as spelled (0.80) |
| Hahiroth | Hahiroth | /ˈheɪ.hi.rəθ/ | Numbers 33:8 |  | unsure (guessed IPA) (0.50) |
| Dophkah | Dophkah | /ˈdoʊ.fkəh/ | Numbers 33:12 |  | unsure (guessed IPA) (0.50) |
| Alush | Alush | /ˈeɪ.ləʃ/ | Numbers 33:13 |  | unsure (guessed IPA) (0.75) |
| Rithmah | Rithmah | /ˈri.θməh/ | Numbers 33:18 |  | unsure (guessed IPA) (0.67) |
| Rimmon | RIM-uhn | /ˈrɪm.ən/ | Numbers 33:19 |  | fine as spelled (1.00) |
| Libnah | LIB-nuh | /ˈlɪb.nə/ | Numbers 33:20 |  | fine as spelled (0.80) |
| Rissah | Rissah | /ˈrɪs.səh/ | Numbers 33:21 |  | fine as spelled (0.80) |
| Kehelathah | Kehelathah | /kəˈhiː.lə.θəh/ | Numbers 33:22 |  | unsure (guessed IPA) (0.78) |
| Shepher | Shepher | /ˈʃiː.fər/ | Numbers 33:23 |  | unsure (guessed IPA) (0.55) |
| Haradah | Haradah | /ˈheɪ.rə.dəh/ | Numbers 33:24 |  | unsure (guessed IPA) (0.57) |
| Makheloth | Makheloth | /ˈmæk.hə.ləθ/ | Numbers 33:25 |  | unsure (guessed IPA) (0.62) |
| Tahath | TAY-hath | /ˈteɪ.hæθ/ | Numbers 33:26 | ✅ | overridden (0.80) |
| Mithkah | Mithkah | /ˈmi.θkəh/ | Numbers 33:28 |  | unsure (guessed IPA) (0.42) |
| Hashmonah | Hashmonah | /ˈheɪ.ʃmə.nəh/ | Numbers 33:29 |  | unsure (guessed IPA) (0.75) |
| Moseroth | Moseroth | /ˈmoʊ.sə.rəθ/ | Numbers 33:30 |  | unsure (guessed IPA) (0.57) |
| Bene | Bene | /bˈɛnə/ | Numbers 33:31 |  | still wrong (0.75) |
| Jaakan | JAY-uh-kan | /ˈdʒeɪ.ə.kæn/ | Numbers 33:31 | ✅ | overridden (0.83) |
| Haggidgad | Haggidgad | /ˈhæɡ.ɡɪd.ɡəd/ | Numbers 33:32 |  | unsure (guessed IPA) (0.62) |
| Jotbathah | Jotbathah | /ˈdʒɒt.bə.θəh/ | Numbers 33:33 |  | unsure (guessed IPA) (0.50) |
| Abronah | Abronah | /ˈæb.rə.nəh/ | Numbers 33:34 |  | unsure (guessed IPA) (0.57) |
| Zalmonah | Zalmonah | /ˈzæl.mə.nəh/ | Numbers 33:41 |  | unsure (guessed IPA) (0.56) |
| Punon | Punon | /ˈpjuː.nən/ | Numbers 33:42 |  | unsure (guessed IPA) (0.67) |
| Iye | Iye | /ˈi.ə.iː/ | Numbers 33:44 |  | unsure (guessed IPA) (0.00) |
| Iyim | Iyim | /ˈi.ə.ɪm/ | Numbers 33:45 |  | unsure (guessed IPA) (0.50) |
| Almon | Almon | /ˈɑlmən/ | Numbers 33:46 |  | still wrong (0.70) |
| Diblathaim | Diblathaim | /ˈdɪb.lə.θeɪm/ | Numbers 33:46 |  | fine as spelled (0.94) |
| Jeshimoth | Jeshimoth | /ˈdʒiː.ʃi.məθ/ | Numbers 33:49 |  | unsure (guessed IPA) (0.57) |
| Addar | AD-ar | /ˈæd.ɑːr/ | Numbers 34:4 |  | suggestion waiting (0.75) |
| Akrabbim | Akrabbim | /ˈæk.rəb.bɪm/ | Numbers 34:4 |  | unsure (guessed IPA) (0.57) |
| Azmon | Azmon | /ˈæz.mən/ | Numbers 34:4 |  | fine as spelled (1.00) |
| Hazar | HAY-zar | /ˈheɪ.zɑːr/ | Numbers 34:4 |  | fine as spelled (0.80) |
| Zedad | Zedad | /ˈziː.dəd/ | Numbers 34:8 |  | unsure (guessed IPA) (0.60) |
| Ziphron | Ziphron | /ˈzi.frən/ | Numbers 34:9 |  | unsure (guessed IPA) (0.71) |
| Shepham | Shepham | /ˈʃiː.fəm/ | Numbers 34:10 |  | fine as spelled (0.80) |
| Ain | AY-in | /ˈeɪ.ɪn/ | Numbers 34:11 |  | still wrong (0.33) |
| Chinnereth | kinnereth | /ˈkɪn.nə.rəθ/ | Numbers 34:11 | ✅ | overridden (0.86) |
| Riblah | Riblah | /ˈrɪb.ləh/ | Numbers 34:11 |  | fine as spelled (0.83) |
| Shemuel | shuh-MYOO-el | /ʃəˈmjuː.əl/ | Numbers 34:20 |  | still wrong (0.75) |
| Chislon | kislon | /ˈkɪs.lən/ | Numbers 34:21 | ✅ | overridden (0.92) |
| Elidad | Elidad | /ˈiː.li.dəd/ | Numbers 34:21 |  | unsure (guessed IPA) (0.67) |
| Bukki | buhkeye | /ˈbʌk.aɪ/ | Numbers 34:22 | ✅ | overridden (1.00) |
| Jogli | Jogli | /ˈdʒɒɡ.lə/ | Numbers 34:22 |  | fine as spelled (0.80) |
| Hanniel | HAN-ee-el | /ˈhæn.i.ɛl/ | Numbers 34:23 |  | still wrong (0.58) |
| Shiphtan | Shiphtan | /ˈʃi.ftən/ | Numbers 34:24 |  | fine as spelled (0.83) |
| Parnach | Parnach | /ˈpær.nək/ | Numbers 34:25 |  | unsure (guessed IPA) (0.58) |
| Azzan | Azzan | /ˈæz.zən/ | Numbers 34:26 |  | fine as spelled (1.00) |
| Paltiel | Paltiel | /ˈpæl.taɪl/ | Numbers 34:26 |  | unsure (guessed IPA) (0.43) |
| Ahihud | uh-HEYE-huhd | /əˈhaɪ.hʌd/ | Numbers 34:27 | ✅ | overridden (1.00) |
| Shelomi | Shelomi | /ˈʃiː.lə.mə/ | Numbers 34:27 |  | unsure (guessed IPA) (0.50) |
| Pedahel | Pedahel | /ˈpiː.də.həl/ | Numbers 34:28 |  | unsure (guessed IPA) (0.71) |
| Arabah | Arabah | /ˈeɪ.rə.bəh/ | Deuteronomy 1:1 |  | unsure (guessed IPA) (0.58) |
| Dizahab | Dizahab | /ˈdi.zə.həb/ | Deuteronomy 1:1 |  | unsure (guessed IPA) (0.71) |
| Suf | Suf | /ˈsʌf/ | Deuteronomy 1:1 |  | unsure (guessed IPA) (0.67) |
| Tophel | Tophel | /ˈtoʊ.fəl/ | Deuteronomy 1:1 |  | unsure (guessed IPA) (0.33) |
| Ashtaroth | ASH-tuh-roth | /ˈæʃ.tə.rɒθ/ | Deuteronomy 1:4 |  | fine as spelled (1.00) |
| Anakim | Anakim | /ˈeɪ.nə.kɪm/ | Deuteronomy 1:28 |  | unsure (guessed IPA) (0.67) |
| Elath | Elath | /ˈiː.ləθ/ | Deuteronomy 2:8 |  | unsure (guessed IPA) (0.54) |
| Zamzummim | Zamzummim | /ˈzam.zʌmˌmɪm/ | Deuteronomy 2:20 |  | still wrong (0.69) |
| Avvim | Avvim | /ˈæv.vɪm/ | Deuteronomy 2:23 |  | unsure (guessed IPA) (0.75) |
| Caphtor | Caphtor | /ˈseɪ.ftər/ | Deuteronomy 2:23 |  | unsure (guessed IPA) (0.67) |
| Kedemoth | KED-uh-moth | /ˈkɛd.ə.mɒθ/ | Deuteronomy 2:26 |  | fine as spelled (1.00) |
| Argob | Argob | /ˈær.ɡəb/ | Deuteronomy 3:4 |  | unsure (guessed IPA) (0.60) |
| Hermon | HUR-muhn | /ˈhɜːr.mən/ | Deuteronomy 3:8 |  | fine as spelled (0.83) |
| Senir | SEE-nuhr | /ˈsiː.nər/ | Deuteronomy 3:9 | ✅ | overridden (1.00) |
| Sirion | Sirion | /ˈsi.ri.ən/ | Deuteronomy 3:9 |  | unsure (guessed IPA) (0.50) |
| Salecah | SAL-uh-kuh | /ˈsæl.ə.kə/ | Deuteronomy 3:10 | ✅ | overridden (0.83) |
| Gadites | GAD-ites | /ˈɡæd.aɪts/ | Deuteronomy 3:12 |  | fine as spelled (0.83) |
| Geshurites | Geshurites | /ɡəˈʃjuː.ri.təs/ | Deuteronomy 3:14 |  | unsure (guessed IPA) (0.50) |
| Maacathites | Maacathites | /mə.əˈseɪ.θi.təs/ | Deuteronomy 3:14 |  | unsure (guessed IPA) (0.40) |
| Bezer | BEE-zer | /ˈbiː.zər/ | Deuteronomy 4:43 |  | fine as spelled (0.80) |
| Golan | GOH-lan | /ˈɡoʊ.læn/ | Deuteronomy 4:43 |  | fine as spelled (0.80) |
| Ramoth | raymahth | /ˈreɪ.mɒθ/ | Deuteronomy 4:43 | ✅ | overridden (1.00) |
| Sion | Sion | /ˈsaɪ.ən/ | Deuteronomy 4:48 |  | still wrong (0.25) |
| Girgashite | GUR-guh-shite | /ˈɡɜːr.ɡə.ʃaɪt/ | Deuteronomy 7:1 |  | still wrong (0.75) |
| Beeroth | Beeroth | /ˈbiː.rəθ/ | Deuteronomy 10:6 |  | unsure (guessed IPA) (0.70) |
| Moserah | Moserah | /ˈmoʊ.sə.rəh/ | Deuteronomy 10:6 |  | unsure (guessed IPA) (0.57) |
| Gudgodah | Gudgodah | /ˈɡʌd.ɡə.dəh/ | Deuteronomy 10:7 |  | unsure (guessed IPA) (0.75) |
| Gerizim | Gerizim | /ˈɡiː.ri.zɪm/ | Deuteronomy 11:29 |  | unsure (guessed IPA) (0.43) |
| Gilgal | Gilgal | /ˈɡɪl.ɡəl/ | Deuteronomy 11:30 |  | unsure (guessed IPA) (0.75) |
| Edomite | Edomite | /ˈiː.dəˌmaɪt/ | Deuteronomy 23:7 |  | fine as spelled (1.00) |
| Jeshurun | Jeshurun | /ˈdʒiː.ʃə.rən/ | Deuteronomy 32:15 |  | unsure (guessed IPA) (0.79) |
| Rahab | Rahab | /ˈreɪ.həb/ | Joshua 2:1 |  | fine as spelled (0.80) |
| Zarethan | Zarethan | /ˈzeɪ.rə.θən/ | Joshua 3:16 |  | unsure (guessed IPA) (0.57) |
| Achan | Achan | /ˈeɪ.kən/ | Joshua 7:1 |  | unsure (guessed IPA) (0.75) |
| Zabdi | ZAB-deye | /ˈzæb.daɪ/ | Joshua 7:1 | ✅ | overridden (1.00) |
| Aven | Aven | /ɑvˈeɪn/ | Joshua 7:2 |  | still wrong (0.50) |
| Shebarim | Shebarim | /ˈʃiː.bə.rɪm/ | Joshua 7:5 |  | fine as spelled (0.93) |
| Babylonian | Babylonian | /bæbəlˈoʊniːən/ | Joshua 7:21 |  | fine as spelled (0.90) |
| Achor | Achor | /ˈeɪkɚ/ | Joshua 7:24 |  | fine as spelled (1.00) |
| Gibeon | GIB-ee-uhn | /ˈɡɪb.i.ən/ | Joshua 9:3 |  | fine as spelled (0.92) |
| Chephirah | Chephirah | /ˈkiː.fi.rəh/ | Joshua 9:17 |  | unsure (guessed IPA) (0.57) |
| Jearim | JEE-uh-rihm | /ˈdʒiː.ə.rɪm/ | Joshua 9:17 | ✅ | overridden (1.00) |
| Adoni-Zedek | Adoni-Zedek | /ˈeɪ.də.nə.ˈziː.dək/ | Joshua 10:1 |  | unsure (guessed IPA) (0.50) |
| Jerusalem | juh-ROO-suh-lem | /dʒəˈruː.sə.ləm/ | Joshua 10:1 |  | fine as spelled (1.00) |
| Debir | DEE-buhr | /ˈdiː.bər/ | Joshua 10:3 | ✅ | overridden (1.00) |
| Eglon | Eglon | /ˈɛɡ.lən/ | Joshua 10:3 |  | fine as spelled (0.80) |
| Hoham | Hoham | /ˈhoʊ.həm/ | Joshua 10:3 |  | unsure (guessed IPA) (0.70) |
| Japhia | juhfeyeuh | /dʒəˈfaɪ.ə/ | Joshua 10:3 | ✅ | overridden (0.80) |
| Jarmuth | Jarmuth | /ˈdʒær.məθ/ | Joshua 10:3 |  | unsure (guessed IPA) (0.67) |
| Piram | Piram | /ˈpi.rəm/ | Joshua 10:3 |  | unsure (guessed IPA) (0.60) |
| Horon | HOR-on | /ˈhɔːr.ɒn/ | Joshua 10:10 |  | fine as spelled (0.80) |
| Makkedah | Makkedah | /ˈmæk.kə.dəh/ | Joshua 10:10 |  | unsure (guessed IPA) (0.57) |
| Aijalon | AJ-uh-lon | /ˈædʒ.ə.lɒn/ | Joshua 10:12 |  | still wrong (0.58) |
| Jashar | Jashar | /ˈdʒeɪ.ʃər/ | Joshua 10:13 |  | fine as spelled (0.80) |
| Gezer | GEE-zer | /ˈɡiː.zər/ | Joshua 10:33 |  | fine as spelled (0.80) |
| Horam | Horam | /ˈhoʊ.rəm/ | Joshua 10:33 |  | fine as spelled (0.80) |
| Achshaph | Achshaph | /ˈeɪ.kʃəf/ | Joshua 11:1 |  | unsure (guessed IPA) (0.60) |
| Hazor | Hazor | /ˈheɪ.zər/ | Joshua 11:1 |  | fine as spelled (1.00) |
| Jabin | Jabin | /ˈdʒeɪ.bɪn/ | Joshua 11:1 |  | unsure (guessed IPA) (0.55) |
| Madon | Madon | /ˈmeɪ.dən/ | Joshua 11:1 |  | fine as spelled (0.80) |
| Chinneroth | kinneroth | /ˈkɪn.nə.rəθ/ | Joshua 11:2 | ✅ | overridden (0.79) |
| Dor | DOR | /dɔːr/ | Joshua 11:2 |  | still wrong (0.67) |
| Merom | Merom | /ˈmiː.rəm/ | Joshua 11:5 |  | fine as spelled (0.80) |
| Misrephoth | Misrephoth | /ˈmɪs.rə.fəθ/ | Joshua 11:8 |  | unsure (guessed IPA) (0.72) |
| Halak | Halak | /ˈheɪ.lək/ | Joshua 11:17 |  | fine as spelled (0.80) |
| Anab | Anab | /ˈeɪ.nəb/ | Joshua 11:21 |  | unsure (guessed IPA) (0.50) |
| Gath | GATH | /ɡæθ/ | Joshua 11:22 |  | fine as spelled (0.83) |
| Geder | Geder | /ˈɡiː.dər/ | Joshua 12:13 |  | fine as spelled (0.80) |
| Tappuah | tuh-PYOO-uh | /təˈpjuː.ə/ | Joshua 12:17 |  | still wrong (0.77) |
| Aphek | Aphek | /ˈeɪ.fək/ | Joshua 12:18 |  | unsure (guessed IPA) (0.45) |
| Lassharon | Lassharon | /ˈlæs.ʃə.rən/ | Joshua 12:18 |  | unsure (guessed IPA) (0.62) |
| Meron | Meron | /ˈmiː.rən/ | Joshua 12:20 |  | unsure (guessed IPA) (0.60) |
| Megiddo | muh-GID-oh | /məˈɡɪd.oʊ/ | Joshua 12:21 |  | fine as spelled (0.83) |
| Taanach | TAY-uh-nak | /ˈteɪ.ə.næk/ | Joshua 12:21 |  | still wrong (0.58) |
| Carmel | Carmel | /kɑrmˈɛl/ | Joshua 12:22 |  | fine as spelled (0.83) |
| Jokneam | Jokneam | /ˈdʒoʊ.niːm/ | Joshua 12:22 |  | unsure (guessed IPA) (0.53) |
| Kedesh | KEE-desh | /ˈkiː.dɛʃ/ | Joshua 12:22 |  | fine as spelled (0.80) |
| Ashdodites | Ashdodites | /əˈʃdoʊ.di.təs/ | Joshua 13:3 |  | unsure (guessed IPA) (0.44) |
| Ashkelonites | Ashkelonites | /ə.ʃkəˈloʊ.ni.təs/ | Joshua 13:3 |  | unsure (guessed IPA) (0.64) |
| Ekron | Ekron | /ˈɛk.rən/ | Joshua 13:3 |  | fine as spelled (1.00) |
| Ekronites | Ekronites | /əkˈroʊ.ni.təs/ | Joshua 13:3 |  | unsure (guessed IPA) (0.56) |
| Gazites | Gazites | /ˈɡeɪ.zi.təs/ | Joshua 13:3 |  | unsure (guessed IPA) (0.57) |
| Gittites | Gittites | /ˈɡɪt.ti.təs/ | Joshua 13:3 |  | unsure (guessed IPA) (0.71) |
| Mearah | Mearah | /ˈmiː.rəh/ | Joshua 13:4 |  | unsure (guessed IPA) (0.60) |
| Gebalites | Gebalites | /ɡəˈbeɪ.li.təs/ | Joshua 13:5 |  | unsure (guessed IPA) (0.44) |
| Geshur | GESH-uhr | /ˈɡɛʃ.ər/ | Joshua 13:13 | ✅ | overridden (0.90) |
| Maacath | Maacath | /ˈmeɪ.ə.səθ/ | Joshua 13:13 |  | unsure (guessed IPA) (0.33) |
| Mephaath | muh-FAY-athh | /məˈfeɪ.æθ/ | Joshua 13:18 | ✅ | overridden (0.92) |
| Shahar | Shahar | /ʃəhˈɑr/ | Joshua 13:19 |  | fine as spelled (0.80) |
| Zereth | ZEE-reth | /ˈzɪər.ɛθ/ | Joshua 13:19 |  | fine as spelled (0.80) |
| Evi | Evi | /ˈiː.və/ | Joshua 13:21 |  | unsure (guessed IPA) (0.33) |
| Betonim | Betonim | /ˈbiː.tə.nɪm/ | Joshua 13:26 |  | unsure (guessed IPA) (0.57) |
| Mizpeh | Mizpeh | /ˈmɪz.pəh/ | Joshua 13:26 |  | unsure (guessed IPA) (0.50) |
| Ramath | Ramath | /ˈreɪ.məθ/ | Joshua 13:26 |  | fine as spelled (0.80) |
| Haram | Haram | /ˈheɪ.rəm/ | Joshua 13:27 |  | unsure (guessed IPA) (0.60) |
| Zaphon | Zaphon | /ˈzeɪ.fən/ | Joshua 13:27 |  | unsure (guessed IPA) (0.40) |
| Karka | Karka | /ˈkær.kə/ | Joshua 15:3 |  | fine as spelled (0.80) |
| Bohan | Bohan | /bˈoʊhən/ | Joshua 15:6 |  | fine as spelled (0.90) |
| Adummim | Adummim | /ˈeɪ.dəm.mɪm/ | Joshua 15:7 |  | unsure (guessed IPA) (0.67) |
| Rogel | Rogel | /rˈoʊɡəl/ | Joshua 15:7 |  | fine as spelled (1.00) |
| Shemesh | SHEM-esh | /ˈʃɛm.ɛʃ/ | Joshua 15:7 |  | fine as spelled (1.00) |
| Nephtoah | Nephtoah | /ˈniː.ftoʊh/ | Joshua 15:9 |  | unsure (guessed IPA) (0.67) |
| Chesalon | kesalon | /ˈkiː.sə.lən/ | Joshua 15:10 | ✅ | overridden (0.71) |
| Jabneel | Jabneel | /ˈdʒæb.niːl/ | Joshua 15:11 |  | fine as spelled (0.86) |
| Shikkeron | Shikkeron | /ˈʃɪk.kə.rən/ | Joshua 15:11 |  | fine as spelled (0.86) |
| Sepher | Sepher | /ˈsiː.fər/ | Joshua 15:15 |  | unsure (guessed IPA) (0.55) |
| Achsah | AK-suh | /ˈæk.sə/ | Joshua 15:16 |  | fine as spelled (1.00) |
| Othniel | OTH-nee-el | /ˈɒθ.ni.əl/ | Joshua 15:17 |  | fine as spelled (0.83) |
| Jagur | Jagur | /ˈdʒeɪ.ɡər/ | Joshua 15:21 |  | fine as spelled (0.80) |
| Adadah | Adadah | /ˈeɪ.də.dəh/ | Joshua 15:22 |  | unsure (guessed IPA) (0.50) |
| Dimonah | Dimonah | /ˈdi.mə.nəh/ | Joshua 15:22 |  | unsure (guessed IPA) (0.50) |
| Ithnan | Ithnan | /ˈi.θnən/ | Joshua 15:23 |  | unsure (guessed IPA) (0.50) |
| Bealoth | Bealoth | /ˈbiː.ləθ/ | Joshua 15:24 |  | unsure (guessed IPA) (0.70) |
| Telem | Telem | /ˈtiː.ləm/ | Joshua 15:24 |  | fine as spelled (0.80) |
| Ziph | ZIF | /zɪf/ | Joshua 15:24 |  | fine as spelled (1.00) |
| Hadattah | Hadattah | /ˈheɪ.dət.təh/ | Joshua 15:25 |  | unsure (guessed IPA) (0.40) |
| Kerioth | Kerioth | /ˈkiː.ri.əθ/ | Joshua 15:25 |  | unsure (guessed IPA) (0.58) |
| Moladah | MOH-la-duh | /ˈmoʊ.lə.də/ | Joshua 15:26 | ✅ | overridden (1.00) |
| Shema | SHEE-muh | /ˈʃiː.mə/ | Joshua 15:26 |  | fine as spelled (1.00) |
| Gaddah | Gaddah | /ˈɡæd.dəh/ | Joshua 15:27 |  | fine as spelled (0.80) |
| Heshmon | Heshmon | /ˈhiː.ʃmən/ | Joshua 15:27 |  | fine as spelled (0.83) |
| Pelet | PEE-let | /ˈpiː.lɛt/ | Joshua 15:27 | ✅ | overridden (0.90) |
| Biziothiah | Biziothiah | /bi.zi.əˈθi.əh/ | Joshua 15:28 |  | unsure (guessed IPA) (0.61) |
| Shual | SHOO-uhl | /ˈʃuː.əl/ | Joshua 15:28 |  | still wrong (0.50) |
| Ezem | EE-zem | /ˈiː.zɛm/ | Joshua 15:29 |  | suggestion waiting (0.75) |
| Iim | Iim | /ˈi.ɪm/ | Joshua 15:29 |  | unsure (guessed IPA) (0.50) |
| Chesil | kesil | /ˈkiː.sɪl/ | Joshua 15:30 | ✅ | overridden (0.40) |
| Madmannah | mad-MANN-uh | /mædˈmæn.ə/ | Joshua 15:31 | ✅ | overridden (0.86) |
| Sansannah | Sansannah | /ˈsæn.sən.nəh/ | Joshua 15:31 |  | unsure (guessed IPA) (0.62) |
| Ziklag | ZIK-lag | /ˈzɪk.læɡ/ | Joshua 15:31 |  | fine as spelled (1.00) |
| Shilhim | Shilhim | /ˈʃɪl.hɪm/ | Joshua 15:32 |  | unsure (guessed IPA) (0.67) |
| Ashnah | Ashnah | /ˈeɪ.ʃnəh/ | Joshua 15:33 |  | unsure (guessed IPA) (0.40) |
| Eshtaol | Eshtaol | /ˈiː.ʃtə.əl/ | Joshua 15:33 |  | unsure (guessed IPA) (0.50) |
| Zorah | Zorah | /zˈɔrə/ | Joshua 15:33 |  | still wrong (0.75) |
| Enam | Enam | /ˈiː.nəm/ | Joshua 15:34 |  | unsure (guessed IPA) (0.50) |
| Gannim | Gannim | /ˈɡæn.nɪm/ | Joshua 15:34 |  | unsure (guessed IPA) (0.60) |
| Zanoah | zuh-NOH-uh | /zəˈnoʊ.ə/ | Joshua 15:34 |  | fine as spelled (1.00) |
| Socoh | Socoh | /ˈsoʊ.səh/ | Joshua 15:35 |  | unsure (guessed IPA) (0.40) |
| Adithaim | Adithaim | /ˈeɪ.di.θeɪm/ | Joshua 15:36 |  | unsure (guessed IPA) (0.67) |
| Gederah | gadeerruh | /ɡəˈdɪər.ə/ | Joshua 15:36 | ✅ | overridden (1.00) |
| Gederothaim | Gederothaim | /ɡəˈdiː.rə.θeɪm/ | Joshua 15:36 |  | unsure (guessed IPA) (0.61) |
| Shaaraim | shay-uh-RAY-im | /ˌʃeɪ.əˈreɪ.ɪm/ | Joshua 15:36 |  | still wrong (0.71) |
| Hadashah | Hadashah | /ˈheɪ.də.ʃəh/ | Joshua 15:37 |  | unsure (guessed IPA) (0.57) |
| Migdal | Migdal | /mˈɪɡdəl/ | Joshua 15:37 |  | fine as spelled (0.83) |
| Joktheel | Joktheel | /ˈdʒɒk.θiːl/ | Joshua 15:38 |  | fine as spelled (0.83) |
| Bozkath | Bozkath | /ˈbɒz.kəθ/ | Joshua 15:39 |  | unsure (guessed IPA) (0.67) |
| Chitlish | kitlish | /ˈkɪt.lɪʃ/ | Joshua 15:40 | ✅ | overridden (1.00) |
| Lahmam | Lahmam | /ˈleɪ.məm/ | Joshua 15:40 |  | fine as spelled (0.80) |
| Ashan | AY-shan | /ˈeɪ.ʃæn/ | Joshua 15:42 |  | still wrong (0.50) |
| Ether | Ether | /ˈiːθɚ/ | Joshua 15:42 |  | fine as spelled (1.00) |
| Nezib | Nezib | /ˈniː.zɪb/ | Joshua 15:43 |  | unsure (guessed IPA) (0.70) |
| Achzib | Achzib | /ˈeɪ.kzɪb/ | Joshua 15:44 |  | unsure (guessed IPA) (0.60) |
| Keilah | kee-EYE-luh | /kiˈaɪ.lə/ | Joshua 15:44 |  | still wrong (0.70) |
| Mareshah | muh-REESH-uh | /məˈriː.ʃə/ | Joshua 15:44 | ✅ | overridden (1.00) |
| Jattir | JAT-ur | /ˈdʒæt.ər/ | Joshua 15:48 |  | fine as spelled (0.80) |
| Sannah | Sannah | /ˈsæn.nəh/ | Joshua 15:49 |  | unsure (guessed IPA) (0.40) |
| Anim | Anim | /ˈeɪ.nɪm/ | Joshua 15:50 |  | unsure (guessed IPA) (0.50) |
| Eshtemoh | Eshtemoh | /ˈiː.ʃtə.məh/ | Joshua 15:50 |  | unsure (guessed IPA) (0.43) |
| Giloh | Giloh | /ˈɡi.ləh/ | Joshua 15:51 |  | unsure (guessed IPA) (0.20) |
| Holon | Holon | /ˈhoʊ.lən/ | Joshua 15:51 |  | fine as spelled (0.80) |
| Eshan | Eshan | /ˈiː.ʃən/ | Joshua 15:52 |  | unsure (guessed IPA) (0.50) |
| Aphekah | Aphekah | /ˈeɪ.fə.kəh/ | Joshua 15:53 |  | unsure (guessed IPA) (0.50) |
| Zior | Zior | /ˈzi.ər/ | Joshua 15:54 |  | unsure (guessed IPA) (0.75) |
| Jutah | Jutah | /ˈdʒjuː.təh/ | Joshua 15:55 |  | unsure (guessed IPA) (0.50) |
| Maon | MAY-on | /ˈmeɪ.ɒn/ | Joshua 15:55 |  | still wrong (0.75) |
| Jezreel | JEZ-ree-el | /ˈdʒɛz.ri.əl/ | Joshua 15:56 |  | fine as spelled (1.00) |
| Jokdeam | Jokdeam | /ˈdʒɒk.diːm/ | Joshua 15:56 |  | fine as spelled (0.92) |
| Gedor | geedawr | /ˈɡiː.dɔːr/ | Joshua 15:58 | ✅ | overridden (0.80) |
| Anoth | Anoth | /ˈeɪ.nəθ/ | Joshua 15:59 |  | unsure (guessed IPA) (0.50) |
| Eltekon | Eltekon | /ˈɛl.tə.kən/ | Joshua 15:59 |  | unsure (guessed IPA) (0.79) |
| Middin | Middin | /ˈmɪd.dɪn/ | Joshua 15:61 |  | fine as spelled (1.00) |
| Secacah | Secacah | /ˈsiː.sə.səh/ | Joshua 15:61 |  | unsure (guessed IPA) (0.36) |
| Archites | arkites | /ˈær.ki.təs/ | Joshua 16:2 | ✅ | overridden (0.57) |
| Japhletites | Japhletites | /dʒəˈfliː.ti.təs/ | Joshua 16:3 |  | unsure (guessed IPA) (0.60) |
| Janoah | Janoah | /ˈdʒeɪ.noʊh/ | Joshua 16:6 |  | unsure (guessed IPA) (0.60) |
| Michmethath | Michmethath | /ˈmi.kmə.θəθ/ | Joshua 16:6 |  | unsure (guessed IPA) (0.69) |
| Shiloh | Shiloh | /ʃˈaɪloʊ/ | Joshua 16:6 |  | fine as spelled (1.00) |
| Taanath | Taanath | /ˈteɪ.ə.nəθ/ | Joshua 16:6 |  | unsure (guessed IPA) (0.75) |
| Naarah | NAY-a-ruh | /ˈneɪ.ə.rə/ | Joshua 16:7 | ✅ | overridden (0.80) |
| Kanah | Kanah | /ˈkeɪ.nəh/ | Joshua 16:8 |  | fine as spelled (0.80) |
| Abiezer | ay-bee-EE-zer | /ˌeɪ.biˈiː.zər/ | Joshua 17:2 |  | still wrong (0.71) |
| Endor | Endor | /ˈɛn.dər/ | Joshua 17:11 |  | fine as spelled (0.90) |
| Ibleam | Ibleam | /ˈɪb.liːm/ | Joshua 17:11 |  | fine as spelled (1.00) |
| Shean | SHEE-an | /ˈʃiː.æn/ | Joshua 17:11 |  | still wrong (0.62) |
| Geliloth | Geliloth | /ˈɡiː.li.ləθ/ | Joshua 18:17 |  | unsure (guessed IPA) (0.29) |
| Emek | Emek | /ˈiː.mək/ | Joshua 18:21 |  | unsure (guessed IPA) (0.50) |
| Keziz | Keziz | /ˈkiː.zɪz/ | Joshua 18:21 |  | unsure (guessed IPA) (0.60) |
| Ophrah | OF-ruh | /ˈɒf.rə/ | Joshua 18:23 |  | still wrong (0.75) |
| Parah | Parah | /ˈpeɪ.rəh/ | Joshua 18:23 |  | unsure (guessed IPA) (0.60) |
| Ammoni | Ammoni | /ˈæm.mə.nə/ | Joshua 18:24 |  | unsure (guessed IPA) (0.40) |
| Geba | GEE-buh | /ˈɡiː.bə/ | Joshua 18:24 |  | still wrong (0.68) |
| Ophni | Ophni | /ˈoʊ.fnə/ | Joshua 18:24 |  | unsure (guessed IPA) (0.50) |
| Mozah | Mozah | /ˈmoʊ.zəh/ | Joshua 18:26 |  | fine as spelled (0.80) |
| Irpeel | Irpeel | /ˈɪr.piːl/ | Joshua 18:27 |  | unsure (guessed IPA) (0.63) |
| Taralah | Taralah | /ˈteɪ.rə.ləh/ | Joshua 18:27 |  | unsure (guessed IPA) (0.57) |
| Eleph | Eleph | /ˈiː.ləf/ | Joshua 18:28 |  | unsure (guessed IPA) (0.62) |
| Gibeath | Gibeath | /ˈɡi.biːθ/ | Joshua 18:28 |  | unsure (guessed IPA) (0.42) |
| Balah | Balah | /ˈbeɪ.ləh/ | Joshua 19:3 |  | unsure (guessed IPA) (0.60) |
| Bethul | Bethul | /ˈbiː.θəl/ | Joshua 19:4 |  | unsure (guessed IPA) (0.50) |
| Marcaboth | MAR-kuh-both | /ˈmɑːr.kə.bɒθ/ | Joshua 19:5 |  | fine as spelled (0.94) |
| Susah | Susah | /ˈsjuː.səh/ | Joshua 19:5 |  | unsure (guessed IPA) (0.58) |
| Lebaoth | Lebaoth | /ˈliː.bə.əθ/ | Joshua 19:6 |  | unsure (guessed IPA) (0.42) |
| Sharuhen | Sharuhen | /ˈʃeɪ.rə.hən/ | Joshua 19:6 |  | unsure (guessed IPA) (0.57) |
| Sarid | Sarid | /ˈseɪ.rɪd/ | Joshua 19:10 |  | fine as spelled (0.80) |
| Dabbesheth | Dabbesheth | /ˈdæb.bə.ʃəθ/ | Joshua 19:11 |  | unsure (guessed IPA) (0.79) |
| Maralah | Maralah | /ˈmeɪ.rə.ləh/ | Joshua 19:11 |  | unsure (guessed IPA) (0.57) |
| Chisloth | kisloth | /ˈkɪs.ləθ/ | Joshua 19:12 | ✅ | overridden (0.83) |
| Daberath | DAB-uh-rath | /ˈdæb.ə.ræθ/ | Joshua 19:12 |  | fine as spelled (0.93) |
| Tabor | TAY-ber | /ˈteɪ.bər/ | Joshua 19:12 |  | fine as spelled (1.00) |
| Ethkazin | Ethkazin | /ˈiː.θkə.zɪn/ | Joshua 19:13 |  | unsure (guessed IPA) (0.71) |
| Neah | Neah | /ˈniːh/ | Joshua 19:13 |  | unsure (guessed IPA) (0.67) |
| Hannathon | Hannathon | /ˈhæn.nə.θən/ | Joshua 19:14 |  | unsure (guessed IPA) (0.64) |
| Iphtah | Iphtah | /ˈi.ftəh/ | Joshua 19:14 |  | unsure (guessed IPA) (0.50) |
| Idalah | Idalah | /ˈi.də.ləh/ | Joshua 19:15 |  | unsure (guessed IPA) (0.50) |
| Nahalal | Nahalal | /ˈneɪ.hə.ləl/ | Joshua 19:15 |  | unsure (guessed IPA) (0.43) |
| Chesulloth | kesulloth | /ˈkiː.səl.ləθ/ | Joshua 19:18 | ✅ | overridden (0.43) |
| Shunem | Shunem | /ˈʃu.nəm/ | Joshua 19:18 |  | fine as spelled (0.90) |
| Anaharath | Anaharath | /əˈneɪ.hə.rəθ/ | Joshua 19:19 |  | unsure (guessed IPA) (0.69) |
| Shion | Shion | /ˈʃi.ən/ | Joshua 19:19 |  | unsure (guessed IPA) (0.50) |
| Ebez | Ebez | /ˈiː.bəz/ | Joshua 19:20 |  | unsure (guessed IPA) (0.50) |
| Kishion | Kishion | /ˈki.ʃi.ən/ | Joshua 19:20 |  | unsure (guessed IPA) (0.67) |
| Engannim | Engannim | /ˈɛn.ɡən.nɪm/ | Joshua 19:21 |  | unsure (guessed IPA) (0.50) |
| Haddah | Haddah | /ˈhæd.dəh/ | Joshua 19:21 |  | unsure (guessed IPA) (0.60) |
| Pazzez | Pazzez | /ˈpæz.zəz/ | Joshua 19:21 |  | unsure (guessed IPA) (0.70) |
| Shahazumah | Shahazumah | /ʃəˈheɪ.zə.məh/ | Joshua 19:22 |  | unsure (guessed IPA) (0.50) |
| Beten | Beten | /ˈbiː.tən/ | Joshua 19:25 |  | unsure (guessed IPA) (0.60) |
| Hali | Hali | /ˈheɪ.lə/ | Joshua 19:25 |  | unsure (guessed IPA) (0.50) |
| Helkath | Helkath | /ˈhɛl.kəθ/ | Joshua 19:25 |  | fine as spelled (0.83) |
| Amad | Amad | /ˈeɪ.məd/ | Joshua 19:26 |  | unsure (guessed IPA) (0.50) |
| Mishal | Mishal | /ˈmi.ʃəl/ | Joshua 19:26 |  | fine as spelled (0.80) |
| Shihorlibnath | Shihorlibnath | /ʃiˈhɒr.lɪb.nəθ/ | Joshua 19:26 |  | unsure (guessed IPA) (0.50) |
| Cabul | Cabul | /ˈseɪ.bəl/ | Joshua 19:27 |  | unsure (guessed IPA) (0.20) |
| Neiel | Neiel | /ˈnaɪ.əl/ | Joshua 19:27 |  | unsure (guessed IPA) (0.75) |
| Ebron | Ebron | /ˈɛbrən/ | Joshua 19:28 |  | fine as spelled (1.00) |
| Hammon | HAM-uhn | /ˈhæm.ən/ | Joshua 19:28 |  | fine as spelled (0.90) |
| Adami-nekeb | Adami-nekeb | /ˈeɪ.də.mə.ˈniː.kəb/ | Joshua 19:33 |  | unsure (guessed IPA) (0.60) |
| Heleph | Heleph | /ˈhiː.ləf/ | Joshua 19:33 |  | fine as spelled (0.80) |
| Lakkum | Lakkum | /ˈlæk.kəm/ | Joshua 19:33 |  | fine as spelled (1.00) |
| Zaanannim | Zaanannim | /zəˈeɪ.nən.nɪm/ | Joshua 19:33 |  | unsure (guessed IPA) (0.62) |
| Aznoth | Aznoth | /ˈæz.nəθ/ | Joshua 19:34 |  | unsure (guessed IPA) (0.60) |
| Hukkok | Hukkok | /ˈhʌk.kək/ | Joshua 19:34 |  | unsure (guessed IPA) (0.70) |
| Hammath | hamath | /ˈhæm.æθ/ | Joshua 19:35 | ✅ | overridden (0.70) |
| Rakkath | Rakkath | /ˈræk.kəθ/ | Joshua 19:35 |  | unsure (guessed IPA) (0.70) |
| Zer | Zer | /ˈzɛr/ | Joshua 19:35 |  | unsure (guessed IPA) (0.67) |
| Ziddim | Ziddim | /ˈzɪd.dɪm/ | Joshua 19:35 |  | fine as spelled (0.80) |
| Anath | Anath | /ˈeɪ.nəθ/ | Joshua 19:38 |  | unsure (guessed IPA) (0.38) |
| Horem | Horem | /ˈhoʊ.rəm/ | Joshua 19:38 |  | fine as spelled (0.90) |
| Irshemesh | Irshemesh | /ˈɪr.ʃə.məʃ/ | Joshua 19:41 |  | fine as spelled (0.86) |
| Ithlah | Ithlah | /ˈi.θləh/ | Joshua 19:42 |  | unsure (guessed IPA) (0.20) |
| Gibbethon | Gibbethon | /ˈɡɪb.bə.θən/ | Joshua 19:44 |  | unsure (guessed IPA) (0.71) |
| Berak | Berak | /ˈbiː.rək/ | Joshua 19:45 |  | unsure (guessed IPA) (0.50) |
| Jarkon | Jarkon | /ˈdʒær.kən/ | Joshua 19:46 |  | unsure (guessed IPA) (0.67) |
| Rakkon | Rakkon | /ˈræk.kən/ | Joshua 19:46 |  | fine as spelled (1.00) |
| Leshem | Leshem | /ˈliː.ʃəm/ | Joshua 19:47 |  | fine as spelled (0.80) |
| Timnathserah | Timnathserah | /tɪmˈneɪ.θsə.rəh/ | Joshua 19:50 |  | unsure (guessed IPA) (0.50) |
| Galilee | GAL-ih-lee | /ˈɡæl.ɪ.liː/ | Joshua 20:7 |  | fine as spelled (0.83) |
| Eshtemoa | esh-tuh-MOH-uh | /ˌɛʃ.təˈmoʊ.ə/ | Joshua 21:14 |  | fine as spelled (0.88) |
| Juttah | Juttah | /ˈdʒʌt.təh/ | Joshua 21:16 |  | unsure (guessed IPA) (0.60) |
| Anathoth | AN-uh-thoth | /ˈæn.ə.θɒθ/ | Joshua 21:18 |  | still wrong (0.75) |
| Elteke | Elteke | /ˈɛl.tə.kiː/ | Joshua 21:23 |  | unsure (guessed IPA) (0.67) |
| Eshterah | Eshterah | /ˈiː.ʃtə.rəh/ | Joshua 21:27 |  | unsure (guessed IPA) (0.71) |
| Abdon | AB-don | /ˈæb.dɒn/ | Joshua 21:30 |  | fine as spelled (0.80) |
| Hammothdor | Hammothdor | /ˈhæm.mə.θdər/ | Joshua 21:32 |  | unsure (guessed IPA) (0.75) |
| Kartan | Kartan | /ˈkær.tən/ | Joshua 21:32 |  | unsure (guessed IPA) (0.75) |
| Kartah | Kartah | /ˈkær.təh/ | Joshua 21:34 |  | unsure (guessed IPA) (0.50) |
| Bezek | Bezek | /bˈɛzɛk/ | Judges 1:4 |  | fine as spelled (0.80) |
| Adoni-Bezek | Adoni-Bezek | /ˈeɪ.də.nə.ˈbiː.zək/ | Judges 1:5 |  | unsure (guessed IPA) (0.50) |
| Zephath | Zephath | /ˈziː.fəθ/ | Judges 1:17 |  | unsure (guessed IPA) (0.60) |
| Ashkelon | Ashkelon | /ˈæʃkəlɒn/ | Judges 1:18 |  | fine as spelled (1.00) |
| Kitron | Kitron | /ˈkɪt.rən/ | Judges 1:30 |  | fine as spelled (0.83) |
| Nahalol | Nahalol | /ˈneɪ.hə.ləl/ | Judges 1:30 |  | unsure (guessed IPA) (0.64) |
| Acco | Acco | /ˈækoʊ/ | Judges 1:31 |  | still wrong (0.75) |
| Ahlab | Ahlab | /ˈeɪ.ləb/ | Judges 1:31 |  | unsure (guessed IPA) (0.62) |
| Aphik | Aphik | /ˈeɪ.fɪk/ | Judges 1:31 |  | fine as spelled (1.00) |
| Helbah | Helbah | /ˈhɛl.bəh/ | Judges 1:31 |  | unsure (guessed IPA) (0.75) |
| Asherites | asheritess | /əˈʃiː.ri.təs/ | Judges 1:32 | ✅ | overridden (0.62) |
| Heres | Heres | /ˈhiː.rəs/ | Judges 1:35 |  | unsure (guessed IPA) (0.60) |
| Shaalbim | Shaalbim | /ˈʃeɪ.əl.bɪm/ | Judges 1:35 |  | unsure (guessed IPA) (0.64) |
| Bochim | bokim | /ˈboʊ.kɪm/ | Judges 2:1 | ✅ | overridden (0.80) |
| Timnath | Timnath | /ˈtɪm.nəθ/ | Judges 2:9 |  | unsure (guessed IPA) (0.75) |
| Cushan | Cushan | /ˈsjuː.ʃən/ | Judges 3:8 |  | unsure (guessed IPA) (0.50) |
| Rishathaim | Rishathaim | /ˈri.ʃə.θeɪm/ | Judges 3:8 |  | fine as spelled (0.86) |
| Benjamite | Benjamite | /ˈbɛn.d͡ʒəˌmaɪt/ | Judges 3:15 |  | fine as spelled (1.00) |
| Ehud | eehud | /ˈiː.hʌd/ | Judges 3:15 | ✅ | overridden (1.00) |
| Seirah | Seirah | /ˈsaɪ.rəh/ | Judges 3:26 |  | fine as spelled (0.80) |
| Shamgar | Shamgar | /ˈʃæm.ɡər/ | Judges 3:31 |  | unsure (guessed IPA) (0.67) |
| Gentiles | Gentiles | /dʒˈɛntaɪlz/ | Judges 4:2 |  | fine as spelled (1.00) |
| Harosheth | Harosheth | /ˈheɪ.rə.ʃəθ/ | Judges 4:2 |  | unsure (guessed IPA) (0.64) |
| Sisera | Sisera | /ˈsi.sə.rə/ | Judges 4:2 |  | unsure (guessed IPA) (0.67) |
| Deborah | Deborah | /dˈɛbɚə/ | Judges 4:4 |  | fine as spelled (1.00) |
| Lappidoth | Lappidoth | /ˈlæp.pi.dəθ/ | Judges 4:4 |  | unsure (guessed IPA) (0.57) |
| Abinoam | Abinoam | /ˈeɪ.bi.noʊm/ | Judges 4:6 |  | unsure (guessed IPA) (0.57) |
| Barak | Barak | /bˈɑrək/ | Judges 4:6 |  | still wrong (0.40) |
| Kishon | Kishon | /ˈki.ʃən/ | Judges 4:7 |  | fine as spelled (0.80) |
| Jael | Jael | /ˈdʒeɪəl/ | Judges 4:17 |  | still wrong (0.75) |
| Meroz | Meroz | /ˈmiː.rəz/ | Judges 5:23 |  | unsure (guessed IPA) (0.60) |
| Abiezrite | Abiezrite | /əˈbaɪz.ri.tiː/ | Judges 6:11 |  | unsure (guessed IPA) (0.62) |
| Gideon | Gideon | /ɡˈɪdiːən/ | Judges 6:11 |  | fine as spelled (0.92) |
| Joash | JOH-ash | /ˈdʒoʊ.æʃ/ | Judges 6:11 |  | suggestion waiting (0.75) |
| Abiezrites | Abiezrites | /əˈbaɪz.ri.təs/ | Judges 6:24 |  | unsure (guessed IPA) (0.67) |
| Jerub-Baal | Jerub-Baal | /ˈdʒiː.rəb.ˈbeɪ.əl/ | Judges 6:32 |  | unsure (guessed IPA) (0.56) |
| Harod | Harod | /ˈheɪ.rəd/ | Judges 7:1 |  | unsure (guessed IPA) (0.60) |
| Jerubbaal | Jerubbaal | /dʒəˈrʌb.bə.əl/ | Judges 7:1 |  | fine as spelled (0.81) |
| Purah | Purah | /ˈpjuː.rəh/ | Judges 7:10 |  | unsure (guessed IPA) (0.50) |
| Meholah | Meholah | /ˈmiː.hə.ləh/ | Judges 7:22 |  | unsure (guessed IPA) (0.57) |
| Shittah | Shittah | /ˈʃɪt.təh/ | Judges 7:22 |  | unsure (guessed IPA) (0.60) |
| Tabbath | Tabbath | /ˈtæb.bəθ/ | Judges 7:22 |  | unsure (guessed IPA) (0.70) |
| Zererah | Zererah | /ˈziː.rə.rəh/ | Judges 7:22 |  | unsure (guessed IPA) (0.57) |
| Barah | Barah | /ˈbeɪ.rəh/ | Judges 7:24 |  | unsure (guessed IPA) (0.60) |
| Oreb | Oreb | /ˈoʊ.rəb/ | Judges 7:25 |  | fine as spelled (1.00) |
| Zeeb | Zeeb | /zˈiːb/ | Judges 7:25 |  | fine as spelled (1.00) |
| Zalmunna | Zalmunna | /ˈzæl.mən.nə/ | Judges 8:5 |  | unsure (guessed IPA) (0.71) |
| Zebah | Zebah | /ˈziː.bəh/ | Judges 8:5 |  | fine as spelled (0.80) |
| Penuel | puh-NYOO-el | /pəˈnjuː.əl/ | Judges 8:8 |  | still wrong (0.57) |
| Karkor | Karkor | /ˈkær.kər/ | Judges 8:10 |  | unsure (guessed IPA) (0.67) |
| Jether | JEE-thuhr | /ˈdʒiː.θər/ | Judges 8:20 | ✅ | overridden (0.90) |
| Berith | Berith | /ˈbiː.rɪθ/ | Judges 8:33 |  | fine as spelled (0.80) |
| Jotham | JOH-thuhm | /ˈdʒoʊ.θəm/ | Judges 9:5 |  | fine as spelled (0.80) |
| Ebed | Ebed | /ˈiː.bəd/ | Judges 9:26 |  | unsure (guessed IPA) (0.50) |
| Gaal | Gaal | /ɡˈɑl/ | Judges 9:26 |  | fine as spelled (1.00) |
| Zebul | Zebul | /ˈziː.bəl/ | Judges 9:28 |  | fine as spelled (1.00) |
| Meonenim | Meonenim | /məˈoʊ.nə.nɪm/ | Judges 9:37 |  | unsure (guessed IPA) (0.50) |
| Arumah | Arumah | /ˈeɪ.rə.məh/ | Judges 9:41 |  | unsure (guessed IPA) (0.50) |
| Elberith | Elberith | /ˈɛl.bə.rɪθ/ | Judges 9:46 |  | fine as spelled (1.00) |
| Zalmon | Zalmon | /ˈzæl.mən/ | Judges 9:48 |  | unsure (guessed IPA) (0.75) |
| Thebez | Thebez | /ˈθiː.bəz/ | Judges 9:50 |  | fine as spelled (0.80) |
| Gileadite | Gileadite | /ɡiˈliː.di.tiː/ | Judges 10:3 |  | unsure (guessed IPA) (0.50) |
| Kamon | Kamon | /ˈkeɪ.mən/ | Judges 10:5 |  | fine as spelled (1.00) |
| Maonites | Maonites | /məˈoʊ.ni.təs/ | Judges 10:12 |  | unsure (guessed IPA) (0.50) |
| Jephthah | Jephthah | /ˈdʒiː.fθəh/ | Judges 11:1 |  | unsure (guessed IPA) (0.67) |
| Tob | Tob | /ˈtɒb/ | Judges 11:3 |  | fine as spelled (1.00) |
| Abelcheramim | Abelcheramim | /ə.bəlˈkiː.rə.mɪm/ | Judges 11:33 |  | unsure (guessed IPA) (0.73) |
| Minnith | Minnith | /ˈmɪn.nɪθ/ | Judges 11:33 |  | fine as spelled (1.00) |
| Ephraimite | Ephraimite | /ˈi.fɹi.əˌmaɪt/ | Judges 12:5 |  | still wrong (0.75) |
| Ephraimites | Ephraimites | /əˈfreɪ.mi.təs/ | Judges 12:5 |  | unsure (guessed IPA) (0.50) |
| Ibzan | Ibzan | /ˈɪb.zən/ | Judges 12:8 |  | fine as spelled (1.00) |
| Zebulunite | Zebulunite | /ˈzɛ.bjʊ.ləˌnaɪt/ | Judges 12:11 |  | fine as spelled (0.95) |
| Hillel | Hillel | /hɪlˈɛl/ | Judges 12:13 |  | still wrong (0.40) |
| Pirathon | Pirathon | /ˈpi.rə.θən/ | Judges 12:15 |  | unsure (guessed IPA) (0.57) |
| Manoah | Manoah | /ˈmeɪ.noʊh/ | Judges 13:2 |  | unsure (guessed IPA) (0.60) |
| Samson | Samson | /sˈæmsən/ | Judges 13:24 |  | fine as spelled (1.00) |
| Mahaneh | Mahaneh | /ˈmeɪ.hə.nəh/ | Judges 13:25 |  | unsure (guessed IPA) (0.57) |
| Timnite | Timnite | /ˈtɪm.ni.tiː/ | Judges 15:6 |  | unsure (guessed IPA) (0.64) |
| Etam | eetum | /ˈiː.təm/ | Judges 15:8 | ✅ | overridden (0.75) |
| Lehi | Lehi | /ˈliːhaɪ/ | Judges 15:9 |  | fine as spelled (1.00) |
| Hakkore | Hakkore | /ˈhæk.kə.riː/ | Judges 15:19 |  | unsure (guessed IPA) (0.67) |
| Delilah | Delilah | /dəlˈaɪlə/ | Judges 16:4 |  | fine as spelled (0.83) |
| Sorek | Sorek | /ˈsoʊ.rək/ | Judges 16:4 |  | fine as spelled (0.80) |
| Micah | MY-kuh | /ˈmaɪ.kə/ | Judges 17:1 |  | fine as spelled (1.00) |
| Laish | Laish | /ˈleɪʃ/ | Judges 18:7 |  | unsure (guessed IPA) (0.67) |
| Jonathan | JON-uh-thuhn | /ˈdʒɒn.ə.θən/ | Judges 18:30 |  | fine as spelled (1.00) |
| Maareh | Maareh | /ˈmeɪ.ə.rəh/ | Judges 20:33 |  | unsure (guessed IPA) (0.33) |
| Gidom | Gidom | /ˈɡi.dəm/ | Judges 20:45 |  | unsure (guessed IPA) (0.60) |
| Lebonah | Lebonah | /ˈliː.bə.nəh/ | Judges 21:19 |  | unsure (guessed IPA) (0.43) |
| Chilion | kilion | /ˈki.li.ən/ | Ruth 1:2 | ✅ | overridden (0.50) |
| Elimelech | Elimelech | /əˈli.mə.lək/ | Ruth 1:2 |  | unsure (guessed IPA) (0.75) |
| Ephrathites | Ephrathites | /əˈfreɪ.θi.təs/ | Ruth 1:2 |  | unsure (guessed IPA) (0.44) |
| Mahlon | Mahlon | /mˈeɪlɔn/ | Ruth 1:2 |  | fine as spelled (0.80) |
| Naomi | Naomi | /neɪˈoʊmiː/ | Ruth 1:2 |  | fine as spelled (1.00) |
| Orpah | Orpah | /ˈɔrpɑ/ | Ruth 1:4 |  | fine as spelled (1.00) |
| Ruth | Ruth | /rˈuːθ/ | Ruth 1:4 |  | fine as spelled (0.83) |
| Mara | Mara | /mˈɑrə/ | Ruth 1:20 |  | fine as spelled (0.88) |
| Boaz | BOH-az | /ˈboʊ.æz/ | Ruth 2:1 |  | fine as spelled (1.00) |
| Ephrathah | EF-ruh-thuh | /ˈɛf.rə.θə/ | Ruth 4:11 |  | fine as spelled (0.83) |
| David | DAY-vid | /ˈdeɪ.vɪd/ | Ruth 4:17 |  | fine as spelled (1.00) |
| Jesse | JES-ee | /ˈdʒɛs.i/ | Ruth 4:17 |  | fine as spelled (1.00) |
| Obed | OH-bed | /ˈoʊ.bɛd/ | Ruth 4:17 |  | still wrong (0.75) |
| Ram | RAM | /ræm/ | Ruth 4:19 |  | fine as spelled (1.00) |
| Jeroham | juh-ROH-ham | /dʒəˈroʊ.hæm/ | 1 Samuel 1:1 | ✅ | overridden (0.86) |
| Ramathaim | Ramathaim | /ˈreɪ.mə.θeɪm/ | 1 Samuel 1:1 |  | fine as spelled (0.86) |
| Tohu | Tohu | /ˈtoʊ.hjuː/ | 1 Samuel 1:1 |  | unsure (guessed IPA) (0.70) |
| Zuph | ZUHF | /zʌf/ | 1 Samuel 1:1 |  | fine as spelled (1.00) |
| Hannah | Hannah | /hˈænə/ | 1 Samuel 1:2 |  | fine as spelled (0.88) |
| Peninnah | Peninnah | /ˈpiː.nɪn.nəh/ | 1 Samuel 1:2 |  | unsure (guessed IPA) (0.71) |
| Eli | Eli | /ˈiːlaɪ/ | 1 Samuel 1:3 |  | fine as spelled (1.00) |
| Hophni | Hophni | /ˈhoʊ.fnə/ | 1 Samuel 1:3 |  | unsure (guessed IPA) (0.60) |
| Samuel | SAM-yoo-el | /ˈsæm.jʊ.əl/ | 1 Samuel 1:20 |  | still wrong (0.75) |
| Ebenezer | Ebenezer | /ɛbɪnˈiːzɚ/ | 1 Samuel 4:1 |  | fine as spelled (0.88) |
| Ichabod | Ichabod | /ˈɪkəbɒd/ | 1 Samuel 4:21 |  | fine as spelled (1.00) |
| Abinadab | uh-BIN-uh-dab | /əˈbɪn.ə.dæb/ | 1 Samuel 7:1 |  | fine as spelled (1.00) |
| Kar | Kar | /ˈkær/ | 1 Samuel 7:11 |  | unsure (guessed IPA) (0.67) |
| Shen | Shen | /ʃˈɛn/ | 1 Samuel 7:12 |  | still wrong (0.67) |
| Abijah | uh-BY-juh | /əˈbaɪ.dʒə/ | 1 Samuel 8:2 |  | fine as spelled (0.80) |
| Joel | JOH-uhll | /ˈdʒoʊ.əl/ | 1 Samuel 8:2 | ✅ | overridden (1.00) |
| Aphiah | Aphiah | /əˈfi.əh/ | 1 Samuel 9:1 |  | unsure (guessed IPA) (0.60) |
| Becorath | Becorath | /ˈbiː.sə.rəθ/ | 1 Samuel 9:1 |  | unsure (guessed IPA) (0.57) |
| Kish | KISH | /kɪʃ/ | 1 Samuel 9:1 |  | fine as spelled (1.00) |
| Zeror | Zeror | /ˈziː.rər/ | 1 Samuel 9:1 |  | fine as spelled (0.90) |
| Saul | SAWL | /sɔːl/ | 1 Samuel 9:2 |  | fine as spelled (0.83) |
| Shaalim | Shaalim | /ˈʃeɪ.ə.lɪm/ | 1 Samuel 9:4 |  | unsure (guessed IPA) (0.67) |
| Shalishah | Shalishah | /ˈʃeɪ.li.ʃəh/ | 1 Samuel 9:4 |  | unsure (guessed IPA) (0.71) |
| Zelzah | Zelzah | /ˈzɛl.zəh/ | 1 Samuel 10:2 |  | fine as spelled (0.83) |
| Matrites | Matrites | /ˈmæt.ri.təs/ | 1 Samuel 10:21 |  | unsure (guessed IPA) (0.75) |
| Nahash | NAY-hash | /ˈneɪ.hæʃ/ | 1 Samuel 11:1 | ✅ | overridden (1.00) |
| Bedan | BEE-dan | /ˈbiː.dæn/ | 1 Samuel 12:11 |  | suggestion waiting (0.70) |
| Michmash | mikmash | /ˈmi.kməʃ/ | 1 Samuel 13:2 | ✅ | overridden (0.67) |
| Migron | Migron | /ˈmɪɡ.rən/ | 1 Samuel 14:2 |  | fine as spelled (0.83) |
| Ahijah | uh-HY-juh | /əˈhaɪ.dʒə/ | 1 Samuel 14:3 |  | fine as spelled (0.80) |
| Ahitub | uh-HEYE-tuhb | /əˈhaɪ.tʌb/ | 1 Samuel 14:3 | ✅ | overridden (1.00) |
| Bozez | Bozez | /ˈboʊ.zəz/ | 1 Samuel 14:4 |  | fine as spelled (0.80) |
| Seneh | Seneh | /ˈsiː.nəh/ | 1 Samuel 14:4 |  | unsure (guessed IPA) (0.40) |
| Malchishua | mal-keye-SHOO-uh | /ˌmæl.kaɪˈʃuː.ə/ | 1 Samuel 14:49 | ✅ | overridden (0.83) |
| Merab | Merab | /ˈmiː.rəb/ | 1 Samuel 14:49 |  | unsure (guessed IPA) (0.50) |
| Ahimaaz | uh-HIM-ay-az | /əˈhɪm.eɪ.æz/ | 1 Samuel 14:50 |  | still wrong (0.50) |
| Ahinoam | uh-HIN-oh-am | /əˈhɪn.oʊ.æm/ | 1 Samuel 14:50 |  | still wrong (0.50) |
| Ner | NUR | /nɜːr/ | 1 Samuel 14:50 |  | still wrong (0.50) |
| Telaim | Telaim | /ˈtiː.leɪm/ | 1 Samuel 15:4 |  | fine as spelled (0.80) |
| Bethlehemite | Bethlehemite | /bə.θləˈhiː.mi.tiː/ | 1 Samuel 16:1 |  | unsure (guessed IPA) (0.36) |
| Ephesdammim | Ephesdammim | /əˈfɛs.dəm.mɪm/ | 1 Samuel 17:1 |  | unsure (guessed IPA) (0.56) |
| Philistine | Philistine | /fˈɪləstiːn/ | 1 Samuel 17:8 |  | still wrong (0.75) |
| Ephrathite | Ephrathite | /əˈfreɪ.θi.tiː/ | 1 Samuel 17:12 |  | unsure (guessed IPA) (0.38) |
| Gai | Gai | /ɡˈeɪ/ | 1 Samuel 17:52 |  | still wrong (0.50) |
| Adriel | Adriel | /ədrˈiːl/ | 1 Samuel 18:19 |  | still wrong (0.67) |
| Meholathite | Meholathite | /mə.həˈleɪ.θi.tiː/ | 1 Samuel 18:19 |  | unsure (guessed IPA) (0.55) |
| Naioth | Naioth | /ˈneɪ.əθ/ | 1 Samuel 19:18 |  | fine as spelled (0.88) |
| Secu | Secu | /ˈsiː.sə/ | 1 Samuel 19:22 |  | unsure (guessed IPA) (0.55) |
| Ezel | Ezel | /ˈiː.zəl/ | 1 Samuel 20:19 |  | unsure (guessed IPA) (0.75) |
| Nob | Nob | /ˈnɒb/ | 1 Samuel 21:1 |  | fine as spelled (1.00) |
| Doeg | Doeg | /ˈdoʊɡ/ | 1 Samuel 21:7 |  | fine as spelled (1.00) |
| Achish | Achish | /ˈeɪ.kɪʃ/ | 1 Samuel 21:10 |  | fine as spelled (1.00) |
| Hereth | Hereth | /ˈhiː.rəθ/ | 1 Samuel 22:5 |  | unsure (guessed IPA) (0.60) |
| Hachilah | hakilah | /ˈheɪ.ki.ləh/ | 1 Samuel 23:19 | ✅ | overridden (0.71) |
| Ziphites | Ziphites | /ˈzi.fi.təs/ | 1 Samuel 23:19 |  | unsure (guessed IPA) (0.57) |
| Hammahlekoth | Hammahlekoth | /həmˈmeɪ.lə.kəθ/ | 1 Samuel 23:28 |  | unsure (guessed IPA) (0.56) |
| Sela | Sela | /sˈɛlə/ | 1 Samuel 23:28 |  | still wrong (0.75) |
| Abigail | AB-ih-gayl | /ˈæb.ɪ.ɡeɪl/ | 1 Samuel 25:3 |  | fine as spelled (1.00) |
| Nabal | Nabal | /ˈneɪ.bəl/ | 1 Samuel 25:3 |  | fine as spelled (0.80) |
| Gallim | Gallim | /ˈɡæl.lɪm/ | 1 Samuel 25:44 |  | fine as spelled (0.80) |
| Abishai | uh-BISH-eye | /əˈbɪʃ.aɪ/ | 1 Samuel 26:6 |  | fine as spelled (0.83) |
| Joab | JOH-ab | /ˈdʒoʊ.æb/ | 1 Samuel 26:6 |  | fine as spelled (1.00) |
| Zeruiah | zeh-roo-EYE-uh | /ˌzɛr.uːˈaɪ.ə/ | 1 Samuel 26:6 | ✅ | overridden (0.83) |
| Maoch | maok | /ˈmeɪ.ək/ | 1 Samuel 27:2 | ✅ | overridden (0.50) |
| Carmelitess | KAR-mel-ite-ess | /ˈkɑːr.mə.laɪ.tɛs/ | 1 Samuel 27:3 |  | fine as spelled (0.80) |
| Jezreelitess | JEZ-ree-el-ite-ess | /ˈdʒɛz.ri.ə.laɪ.tɛs/ | 1 Samuel 27:3 |  | still wrong (0.73) |
| Girzites | Girzites | /ˈɡɪr.zi.təs/ | 1 Samuel 27:8 |  | unsure (guessed IPA) (0.56) |
| Jerahmeelites | jerahmeelitess | /dʒə.rəˈmiː.li.təs/ | 1 Samuel 27:10 | ✅ | overridden (0.77) |
| Besor | Besor | /ˈbiː.sər/ | 1 Samuel 30:9 |  | unsure (guessed IPA) (0.70) |
| Siphmoth | Siphmoth | /ˈsi.fməθ/ | 1 Samuel 30:28 |  | unsure (guessed IPA) (0.67) |
| Racal | Racal | /rˈækəl/ | 1 Samuel 30:29 |  | still wrong (0.60) |
| Athach | Athach | /ˈeɪ.θək/ | 1 Samuel 30:30 |  | unsure (guessed IPA) (0.38) |
| Borashan | Borashan | /ˈboʊ.rə.ʃən/ | 1 Samuel 30:30 |  | unsure (guessed IPA) (0.50) |
| Shan | Shan | /ʃˈæn/ | 1 Samuel 31:10 |  | still wrong (0.67) |
| Ishbosheth | Ishbosheth | /ˈi.ʃbə.ʃəθ/ | 2 Samuel 2:8 |  | unsure (guessed IPA) (0.50) |
| Ashurites | Ashurites | /əˈʃjuː.ri.təs/ | 2 Samuel 2:9 |  | unsure (guessed IPA) (0.44) |
| Hazzurim | Hazzurim | /ˈhæz.zə.rɪm/ | 2 Samuel 2:16 |  | fine as spelled (0.86) |
| Asahel | AS-uh-hel | /ˈæs.ə.hɛl/ | 2 Samuel 2:18 |  | fine as spelled (1.00) |
| Ammah | Ammah | /ˈæm.məh/ | 2 Samuel 2:24 |  | unsure (guessed IPA) (0.62) |
| Giah | Giah | /ˈɡi.əh/ | 2 Samuel 2:24 |  | unsure (guessed IPA) (0.25) |
| Bithron | Bithron | /ˈbi.θrən/ | 2 Samuel 2:29 |  | unsure (guessed IPA) (0.63) |
| Amnon | AM-non | /ˈæm.nɒn/ | 2 Samuel 3:2 |  | fine as spelled (0.90) |
| Absalom | AB-suh-luhm | /ˈæb.sə.ləm/ | 2 Samuel 3:3 |  | fine as spelled (1.00) |
| Chileab | kileab | /ˈki.liːb/ | 2 Samuel 3:3 | ✅ | overridden (0.80) |
| Abital | uh-BY-tuhl | /əˈbaɪ.təl/ | 2 Samuel 3:4 | ✅ | overridden (0.92) |
| Adonijah | ad-oh-NY-juh | /ˌæd.oʊˈnaɪ.dʒə/ | 2 Samuel 3:4 |  | still wrong (0.71) |
| Haggith | HAG-ith | /ˈhæɡ.ɪθ/ | 2 Samuel 3:4 |  | fine as spelled (1.00) |
| Shephatiah | shef-uh-TY-uh | /ˌʃɛf.əˈtaɪ.ə/ | 2 Samuel 3:4 |  | fine as spelled (0.94) |
| Eglah | EG-luh | /ˈɛɡ.lə/ | 2 Samuel 3:5 |  | still wrong (0.62) |
| Ithream | ITH-ree-am | /ˈɪθ.ri.æm/ | 2 Samuel 3:5 |  | suggestion waiting (0.75) |
| Rizpah | Rizpah | /ˈrɪz.pəh/ | 2 Samuel 3:7 |  | unsure (guessed IPA) (0.67) |
| Bahurim | Bahurim | /ˈbeɪ.hə.rɪm/ | 2 Samuel 3:16 |  | unsure (guessed IPA) (0.57) |
| Sirah | Sirah | /ˈsi.rəh/ | 2 Samuel 3:26 |  | fine as spelled (0.80) |
| Beerothite | Beerothite | /biːˈroʊ.θi.tiː/ | 2 Samuel 4:2 |  | unsure (guessed IPA) (0.50) |
| Rechab | REE-kab | /ˈriː.kæb/ | 2 Samuel 4:2 | ✅ | overridden (1.00) |
| Beerothites | Beerothites | /biːˈroʊ.θi.təs/ | 2 Samuel 4:3 |  | unsure (guessed IPA) (0.56) |
| Gittaim | Gittaim | /ˈɡɪt.teɪm/ | 2 Samuel 4:3 |  | fine as spelled (1.00) |
| Mephibosheth | Mephibosheth | /məˈfɪb.əˌʃɛθ/ | 2 Samuel 4:4 |  | still wrong (0.56) |
| Nathan | NAY-thuhn | /ˈneɪ.θən/ | 2 Samuel 5:14 |  | fine as spelled (1.00) |
| Shobab | SHOH-bab | /ˈʃoʊ.bæb/ | 2 Samuel 5:14 |  | fine as spelled (1.00) |
| Solomon | SOL-uh-muhn | /ˈsɒl.ə.mən/ | 2 Samuel 5:14 |  | fine as spelled (1.00) |
| Ibhar | IB-har | /ˈɪb.hɑːr/ | 2 Samuel 5:15 |  | fine as spelled (0.83) |
| Eliada | ee-LY-uh-duh | /ɪˈlaɪ.ə.də/ | 2 Samuel 5:16 |  | still wrong (0.46) |
| Eliphelet | ee-LIF-uh-let | /ɪˈlɪf.ə.lɛt/ | 2 Samuel 5:16 |  | suggestion waiting (0.75) |
| Baale | Baale | /ˈbeɪ.ə.liː/ | 2 Samuel 6:2 |  | unsure (guessed IPA) (0.60) |
| Ahio | uh-HY-oh | /əˈhaɪ.oʊ/ | 2 Samuel 6:3 |  | fine as spelled (0.80) |
| Uzzah | UZ-uh | /ˈʌz.ə/ | 2 Samuel 6:3 |  | fine as spelled (0.88) |
| Nacon | Nacon | /ˈneɪ.sən/ | 2 Samuel 6:6 |  | unsure (guessed IPA) (0.60) |
| Syrians | Syrians | /sˈɪriːənz/ | 2 Samuel 8:5 |  | fine as spelled (0.86) |
| Berothai | Berothai | /ˈbiː.rə.θeɪ/ | 2 Samuel 8:8 |  | unsure (guessed IPA) (0.17) |
| Betah | Betah | /ˈbiː.təh/ | 2 Samuel 8:8 |  | unsure (guessed IPA) (0.30) |
| Toi | Toi | /ˈtɔɪ/ | 2 Samuel 8:9 |  | unsure (guessed IPA) (0.17) |
| Joram | JOR-uhm | /ˈdʒɔːr.əm/ | 2 Samuel 8:10 |  | fine as spelled (0.80) |
| Jehoshaphat | juh-HOSH-uh-fat | /dʒəˈhɒʃ.ə.fæt/ | 2 Samuel 8:16 |  | fine as spelled (1.00) |
| Seraiah | suh-RAY-yuh | /səˈreɪ.jə/ | 2 Samuel 8:17 |  | still wrong (0.67) |
| Zadok | ZAY-dok | /ˈzeɪ.dɒk/ | 2 Samuel 8:17 |  | fine as spelled (0.80) |
| Benaiah | buh-NAY-yuh | /bəˈneɪ.jə/ | 2 Samuel 8:18 |  | still wrong (0.58) |
| Ziba | Ziba | /ˈzi.bə/ | 2 Samuel 9:2 |  | fine as spelled (1.00) |
| Debar | Debar | /ˈdiː.bər/ | 2 Samuel 9:4 |  | unsure (guessed IPA) (0.60) |
| Mica | MY-kuh | /ˈmaɪ.kə/ | 2 Samuel 9:12 |  | fine as spelled (0.90) |
| Helam | Helam | /ˈhiː.ləm/ | 2 Samuel 10:16 |  | fine as spelled (0.80) |
| Shobach | Shobach | /ˈʃoʊ.bək/ | 2 Samuel 10:16 |  | fine as spelled (1.00) |
| Bathsheba | Bathsheba | /bæθʃˈiːbə/ | 2 Samuel 11:3 |  | fine as spelled (0.86) |
| Eliam | Eliam | /əˈli.əm/ | 2 Samuel 11:3 |  | unsure (guessed IPA) (0.60) |
| Uriah | Uriah | /jʊəˈɹaɪə/ | 2 Samuel 11:3 |  | fine as spelled (1.00) |
| Jerubbesheth | Jerubbesheth | /dʒəˈrʌb.bə.ʃəθ/ | 2 Samuel 11:21 |  | unsure (guessed IPA) (0.67) |
| Jedidiah | Jedidiah | /ˌd͡ʒɛdɪˈdaɪə/ | 2 Samuel 12:25 |  | still wrong (0.71) |
| Jonadab | Jonadab | /ˈdʒoʊ.nə.dəb/ | 2 Samuel 13:3 |  | unsure (guessed IPA) (0.71) |
| Shimeah | SHIM-ee-uh | /ˈʃɪm.i.ə/ | 2 Samuel 13:3 |  | fine as spelled (0.80) |
| Ammihur | Ammihur | /ˈæm.mi.hjuːr/ | 2 Samuel 13:37 |  | unsure (guessed IPA) (0.64) |
| Tekoa | tuh-KOH-uh | /təˈkoʊ.ə/ | 2 Samuel 14:2 |  | suggestion waiting (0.60) |
| Gilonite | Gilonite | /ɡiˈloʊ.ni.tiː/ | 2 Samuel 15:12 |  | unsure (guessed IPA) (0.44) |
| Merhak | Merhak | /ˈmɛr.hək/ | 2 Samuel 15:17 |  | fine as spelled (0.83) |
| Ittai | Ittai | /ˈɪt.teɪ/ | 2 Samuel 15:19 |  | unsure (guessed IPA) (0.50) |
| Amasa | uh-MAY-suh | /əˈmeɪ.sə/ | 2 Samuel 17:25 | ✅ | overridden (0.80) |
| Ithra | Ithra | /ˈi.θrə/ | 2 Samuel 17:25 |  | unsure (guessed IPA) (0.62) |
| Barzillai | Barzillai | /ˈbær.zɪl.leɪ/ | 2 Samuel 17:27 |  | unsure (guessed IPA) (0.71) |
| Lodebar | Lodebar | /ˈloʊ.də.bər/ | 2 Samuel 17:27 |  | fine as spelled (0.86) |
| Rogelim | Rogelim | /ˈroʊ.ɡə.lɪm/ | 2 Samuel 17:27 |  | unsure (guessed IPA) (0.57) |
| Shobi | Shobi | /ˈʃoʊ.bə/ | 2 Samuel 17:27 |  | unsure (guessed IPA) (0.75) |
| Chimham | kimham | /ˈkɪm.həm/ | 2 Samuel 19:37 | ✅ | overridden (0.83) |
| Bichri | Bichri | /ˈbi.krə/ | 2 Samuel 20:1 |  | unsure (guessed IPA) (0.50) |
| Sheva | SHEE-vuh | /ˈʃiː.və/ | 2 Samuel 20:25 |  | fine as spelled (1.00) |
| Jairite | Jairite | /ˈdʒeɪ.ri.tiː/ | 2 Samuel 20:26 |  | unsure (guessed IPA) (0.58) |
| Gibeonites | Gibeonites | /ɡi.bəˈoʊ.ni.təs/ | 2 Samuel 21:1 |  | unsure (guessed IPA) (0.40) |
| Armoni | Armoni | /ˈær.mə.nə/ | 2 Samuel 21:8 |  | unsure (guessed IPA) (0.50) |
| Zela | Zela | /ˈziː.lə/ | 2 Samuel 21:14 |  | unsure (guessed IPA) (0.75) |
| Ishbibenob | Ishbibenob | /iˈʃbi.bə.nəb/ | 2 Samuel 21:16 |  | unsure (guessed IPA) (0.67) |
| Gob | Gob | /ɡˈɑb/ | 2 Samuel 21:18 |  | fine as spelled (1.00) |
| Saph | Saph | /ˈsæf/ | 2 Samuel 21:18 |  | unsure (guessed IPA) (0.33) |
| Jaare-Oregim | Jaare-Oregim | /ˈdʒeɪ.ə.riː.ˈoʊ.rə.ɡɪm/ | 2 Samuel 21:19 |  | unsure (guessed IPA) (0.46) |
| Adino | Adino | /ˈeɪ.di.nə/ | 2 Samuel 23:8 |  | unsure (guessed IPA) (0.40) |
| Basshebeth | Basshebeth | /ˈbæs.ʃə.bəθ/ | 2 Samuel 23:8 |  | unsure (guessed IPA) (0.38) |
| Eznite | Eznite | /ˈɛz.ni.tiː/ | 2 Samuel 23:8 |  | unsure (guessed IPA) (0.42) |
| Tahchemonite | Tahchemonite | /tə.kəˈmoʊ.ni.tiː/ | 2 Samuel 23:8 |  | unsure (guessed IPA) (0.40) |
| Agee | Agee | /ˈeɪdʒˈiː/ | 2 Samuel 23:11 |  | fine as spelled (1.00) |
| Elika | Elika | /ˈiː.li.kə/ | 2 Samuel 23:25 |  | unsure (guessed IPA) (0.60) |
| Harodite | Harodite | /həˈroʊ.di.tiː/ | 2 Samuel 23:25 |  | unsure (guessed IPA) (0.50) |
| Helez | HEE-lez | /ˈhiː.lɛz/ | 2 Samuel 23:26 |  | fine as spelled (0.80) |
| Paltite | Paltite | /ˈpæl.ti.tiː/ | 2 Samuel 23:26 |  | unsure (guessed IPA) (0.29) |
| Mebunnai | Mebunnai | /ˈmiː.bən.neɪ/ | 2 Samuel 23:27 |  | unsure (guessed IPA) (0.67) |
| Hiddai | Hiddai | /ˈhɪd.deɪ/ | 2 Samuel 23:30 |  | unsure (guessed IPA) (0.45) |
| Azmaveth | az-MAY-veth | /æzˈmeɪ.vɛθ/ | 2 Samuel 23:31 |  | fine as spelled (0.86) |
| Barhumite | Barhumite | /bərˈhjuː.mi.tiː/ | 2 Samuel 23:31 |  | unsure (guessed IPA) (0.40) |
| Jashen | Jashen | /ˈdʒeɪ.ʃən/ | 2 Samuel 23:32 |  | fine as spelled (0.80) |
| Ahiam | Ahiam | /əˈhi.əm/ | 2 Samuel 23:33 |  | fine as spelled (0.80) |
| Ararite | Ararite | /əˈreɪ.ri.tiː/ | 2 Samuel 23:33 |  | unsure (guessed IPA) (0.36) |
| Sharar | Sharar | /ʃɚˈɑr/ | 2 Samuel 23:33 |  | fine as spelled (1.00) |
| Ahasbai | Ahasbai | /ˈeɪ.həs.beɪ/ | 2 Samuel 23:34 |  | unsure (guessed IPA) (0.33) |
| Maacathite | may-AK-uh-thite | /meɪˈæk.ə.θaɪt/ | 2 Samuel 23:34 |  | fine as spelled (0.88) |
| Arbite | Arbite | /ˈær.bi.tiː/ | 2 Samuel 23:35 |  | unsure (guessed IPA) (0.50) |
| Paarai | Paarai | /ˈpeɪ.ə.reɪ/ | 2 Samuel 23:35 |  | unsure (guessed IPA) (0.30) |
| Bani | bayneye | /ˈbeɪ.naɪ/ | 2 Samuel 23:36 | ✅ | overridden (1.00) |
| Gadite | Gadite | /ˈɡæ.daɪt/ | 2 Samuel 23:36 |  | fine as spelled (1.00) |
| Hodshi | Hodshi | /ˈhɒd.ʃə/ | 2 Samuel 24:6 |  | unsure (guessed IPA) (0.40) |
| Jaan | Jaan | /jˈɑn/ | 2 Samuel 24:6 |  | still wrong (0.67) |
| Tahtim | Tahtim | /ˈteɪ.tɪm/ | 2 Samuel 24:6 |  | unsure (guessed IPA) (0.40) |
| Araunah | Araunah | /ˈeɪ.rɔː.nəh/ | 2 Samuel 24:16 |  | unsure (guessed IPA) (0.50) |
| Abishag | Abishag | /ˈæbɪʃæg/ | 1 Kings 1:3 |  | still wrong (0.67) |
| Shunammite | Shunammite | /ʃəˈnæm.mi.tiː/ | 1 Kings 1:3 |  | unsure (guessed IPA) (0.62) |
| Rei | Rei | /ˈraɪ/ | 1 Kings 1:8 |  | unsure (guessed IPA) (0.50) |
| Zoheleth | Zoheleth | /ˈzoʊ.hə.ləθ/ | 1 Kings 1:9 |  | unsure (guessed IPA) (0.71) |
| Azariah | az-uh-RY-uh | /ˌæz.əˈraɪ.ə/ | 1 Kings 4:2 |  | fine as spelled (1.00) |
| Shisha | Shisha | /ˈʃi.ʃə/ | 1 Kings 4:3 |  | unsure (guessed IPA) (0.75) |
| Abda | Abda | /ˈæb.də/ | 1 Kings 4:6 |  | fine as spelled (0.90) |
| Adoniram | Adoniram | /ædəˈnaɪrəm/ | 1 Kings 4:6 |  | fine as spelled (1.00) |
| Deker | Deker | /ˈdiː.kər/ | 1 Kings 4:9 |  | fine as spelled (1.00) |
| Makaz | Makaz | /ˈmeɪ.kəz/ | 1 Kings 4:9 |  | unsure (guessed IPA) (0.60) |
| Arubboth | Arubboth | /ˈeɪ.rəb.bəθ/ | 1 Kings 4:10 |  | unsure (guessed IPA) (0.58) |
| Hesed | heesehd | /ˈhiː.sɛd/ | 1 Kings 4:10 | ✅ | overridden (1.00) |
| Taphath | Taphath | /ˈteɪ.fəθ/ | 1 Kings 4:11 |  | unsure (guessed IPA) (0.37) |
| Jokmeam | JOK-mee-am | /ˈdʒɒk.mi.æm/ | 1 Kings 4:12 |  | suggestion waiting (0.71) |
| Iddo | ID-oh | /ˈɪd.oʊ/ | 1 Kings 4:14 |  | fine as spelled (1.00) |
| Paruah | Paruah | /ˈpeɪ.rə.əh/ | 1 Kings 4:17 |  | unsure (guessed IPA) (0.50) |
| Ela | Ela | /ˈɛlə/ | 1 Kings 4:18 |  | fine as spelled (1.00) |
| Tiphsah | Tiphsah | /ˈti.fsəh/ | 1 Kings 4:24 |  | unsure (guessed IPA) (0.58) |
| Calcol | kaalkol | /ˈkæl.kɒl/ | 1 Kings 4:31 | ✅ | overridden (0.83) |
| Darda | Darda | /ˈdær.də/ | 1 Kings 4:31 |  | fine as spelled (0.80) |
| Ethan | EE-thuhn | /ˈiː.θən/ | 1 Kings 4:31 |  | fine as spelled (1.00) |
| Ezrahite | Ezrahite | /əzˈreɪ.hi.tiː/ | 1 Kings 4:31 |  | unsure (guessed IPA) (0.44) |
| Mahol | Mahol | /ˈmeɪ.həl/ | 1 Kings 4:31 |  | unsure (guessed IPA) (0.50) |
| Ziv | Ziv | /zˈɪv/ | 1 Kings 6:1 |  | fine as spelled (1.00) |
| Bul | Bul | /ˈbʌl/ | 1 Kings 6:38 |  | unsure (guessed IPA) (0.50) |
| Ethanim | Ethanim | /ˈiː.θə.nɪm/ | 1 Kings 8:2 |  | unsure (guessed IPA) (0.67) |
| Ashtoreth | Ashtoreth | /ˈeɪ.ʃtə.rəθ/ | 1 Kings 11:5 |  | unsure (guessed IPA) (0.71) |
| Milcom | Milcom | /ˈmɪl.səm/ | 1 Kings 11:5 |  | unsure (guessed IPA) (0.50) |
| Tahpenes | Tahpenes | /ˈtɑːpəniːz/ | 1 Kings 11:19 |  | fine as spelled (1.00) |
| Genubath | Genubath | /ˈɡiː.nə.bəθ/ | 1 Kings 11:20 |  | unsure (guessed IPA) (0.43) |
| Rezon | Rezon | /ˈriː.zən/ | 1 Kings 11:23 |  | fine as spelled (1.00) |
| Jeroboam | jer-uh-BOH-uhm | /ˌdʒɛr.əˈboʊ.əm/ | 1 Kings 11:26 |  | fine as spelled (1.00) |
| Zeruah | Zeruah | /ˈziː.rə.əh/ | 1 Kings 11:26 |  | unsure (guessed IPA) (0.50) |
| Rehoboam | ree-huh-BOH-uhm | /ˌriː.həˈboʊ.əm/ | 1 Kings 11:43 |  | fine as spelled (0.81) |
| Adoram | Adoram | /ˈeɪ.də.rəm/ | 1 Kings 12:18 |  | unsure (guessed IPA) (0.50) |
| Shemaiah | shuh-MAY-yuh | /ʃəˈmeɪ.jə/ | 1 Kings 12:22 |  | still wrong (0.67) |
| Josiah | joh-SY-uh | /dʒoʊˈsaɪ.ə/ | 1 Kings 13:2 |  | fine as spelled (0.80) |
| Abijam | Abijam | /ˈeɪ.bi.dʒəm/ | 1 Kings 15:1 |  | unsure (guessed IPA) (0.67) |
| Abishalom | Abishalom | /əˈbi.ʃə.ləm/ | 1 Kings 15:2 |  | fine as spelled (0.88) |
| Asa | AY-suh | /ˈeɪ.sə/ | 1 Kings 15:8 |  | fine as spelled (0.83) |
| Hezion | Hezion | /ˈhiː.zi.ən/ | 1 Kings 15:18 |  | unsure (guessed IPA) (0.67) |
| Tabrimmon | Tabrimmon | /ˈtæb.rɪm.mən/ | 1 Kings 15:18 |  | unsure (guessed IPA) (0.75) |
| Jehu | JEE-hyoo | /ˈdʒiː.hjuː/ | 1 Kings 16:1 | ✅ | overridden (0.72) |
| Arza | Arza | /ˈær.zə/ | 1 Kings 16:9 |  | unsure (guessed IPA) (0.75) |
| Omri | omreye | /ˈɒm.raɪ/ | 1 Kings 16:16 | ✅ | overridden (1.00) |
| Ginath | Ginath | /ˈɡi.nəθ/ | 1 Kings 16:21 |  | unsure (guessed IPA) (0.40) |
| Tibni | Tibni | /ˈtɪb.nə/ | 1 Kings 16:21 |  | fine as spelled (0.80) |
| Shemer | SHEE-mer | /ˈʃiː.mər/ | 1 Kings 16:24 |  | fine as spelled (0.80) |
| Ethbaal | Ethbaal | /ˈiː.θbə.əl/ | 1 Kings 16:31 |  | unsure (guessed IPA) (0.42) |
| Jezebel | Jezebel | /ˈd͡ʒɛzəˌbɛl/ | 1 Kings 16:31 |  | fine as spelled (1.00) |
| Bethelite | Bethelite | /bəˈθiː.li.tiː/ | 1 Kings 16:34 |  | unsure (guessed IPA) (0.56) |
| Hiel | Hiel | /ˈhaɪl/ | 1 Kings 16:34 |  | unsure (guessed IPA) (0.17) |
| Segub | SEE-gub | /ˈsiː.ɡʌb/ | 1 Kings 16:34 |  | fine as spelled (0.80) |
| Elijah | ee-LY-juh | /ɪˈlaɪ.dʒə/ | 1 Kings 17:1 |  | fine as spelled (1.00) |
| Tishbite | Tishbite | /ˈti.ʃbi.tiː/ | 1 Kings 17:1 |  | unsure (guessed IPA) (0.57) |
| Cherith | kerith | /ˈkiː.rɪθ/ | 1 Kings 17:3 | ✅ | overridden (0.50) |
| Obadiah | oh-buh-DY-uh | /ˌoʊ.bəˈdaɪ.ə/ | 1 Kings 18:3 |  | fine as spelled (0.93) |
| Jezreelite | Jezreelite | /dʒəzˈriː.li.tiː/ | 1 Kings 21:1 |  | unsure (guessed IPA) (0.56) |
| Naboth | Naboth | /ˈneɪbɒθ/ | 1 Kings 21:1 |  | fine as spelled (0.90) |
| Imlah | Imlah | /ˈɪm.ləh/ | 1 Kings 22:8 |  | fine as spelled (0.80) |
| Chenaanah | kuh-NAY-uh-nuh | /kəˈneɪ.ə.nə/ | 1 Kings 22:11 |  | still wrong (0.71) |
| Zedekiah | zed-uh-KY-uh | /ˌzɛd.əˈkaɪ.ə/ | 1 Kings 22:11 |  | fine as spelled (0.86) |
| Amon | aymuhn | /ˈeɪ.mən/ | 1 Kings 22:26 | ✅ | overridden (1.00) |
| Ahaziah | ay-huh-ZY-uh | /ˌeɪ.həˈzaɪ.ə/ | 1 Kings 22:40 |  | fine as spelled (0.83) |
| Azubah | uh-ZOO-buh | /əˈzuː.bə/ | 1 Kings 22:42 |  | fine as spelled (0.83) |
| Zebub | Zebub | /ˈziː.bəb/ | 2 Kings 1:2 |  | fine as spelled (0.90) |
| Hareseth | Hareseth | /ˈheɪ.rə.səθ/ | 2 Kings 3:25 |  | unsure (guessed IPA) (0.57) |
| Kir | Kir | /kˈɪr/ | 2 Kings 3:25 |  | still wrong (0.40) |
| Gehazi | Gehazi | /ˈɡiː.hə.zə/ | 2 Kings 4:12 |  | unsure (guessed IPA) (0.31) |
| Abanah | Abanah | /ˈeɪ.bə.nəh/ | 2 Kings 5:12 |  | unsure (guessed IPA) (0.50) |
| Pharpar | Pharpar | /ˈfær.pər/ | 2 Kings 5:12 |  | fine as spelled (0.83) |
| Benhadad | Benhadad | /ˈbɛn.hə.dəd/ | 2 Kings 6:24 |  | unsure (guessed IPA) (0.62) |
| Zair | Zair | /ˈzeɪr/ | 2 Kings 8:21 |  | unsure (guessed IPA) (0.67) |
| Athaliah | ath-uh-LY-uh | /ˌæθ.əˈlaɪ.ə/ | 2 Kings 8:26 |  | fine as spelled (0.92) |
| Bidkar | Bidkar | /ˈbɪd.kər/ | 2 Kings 9:25 |  | unsure (guessed IPA) (0.77) |
| Jehonadab | Jehonadab | /dʒəˈhoʊ.nə.dəb/ | 2 Kings 10:15 |  | unsure (guessed IPA) (0.78) |
| Jehosheba | Jehosheba | /dʒəˈhoʊ.ʃə.bə/ | 2 Kings 11:2 |  | fine as spelled (0.88) |
| Carites | Carites | /ˈseɪ.ri.təs/ | 2 Kings 11:4 |  | unsure (guessed IPA) (0.43) |
| Sur | Sur | /sˈɚ/ | 2 Kings 11:6 |  | still wrong (0.67) |
| Jehoash | Jehoash | /ˈdʒiː.hoʊʃ/ | 2 Kings 12:1 |  | fine as spelled (0.80) |
| Silla | Silla | /ˈsɪl.lə/ | 2 Kings 12:20 |  | fine as spelled (1.00) |
| Amaziah | am-uh-ZY-uh | /ˌæm.əˈzaɪ.ə/ | 2 Kings 12:21 |  | fine as spelled (0.92) |
| Jozacar | Jozacar | /ˈdʒoʊ.zə.sər/ | 2 Kings 12:21 |  | unsure (guessed IPA) (0.71) |
| Shomer | SHOH-mer | /ˈʃoʊ.mər/ | 2 Kings 12:21 |  | fine as spelled (1.00) |
| Jehoaddin | Jehoaddin | /ˈdʒiː.hoʊd.dɪn/ | 2 Kings 14:2 |  | unsure (guessed IPA) (0.71) |
| Amittai | Amittai | /əˈmɪt.aɪ/ | 2 Kings 14:25 |  | fine as spelled (0.80) |
| Zechariah | zek-uh-RY-uh | /ˌzɛk.əˈraɪ.ə/ | 2 Kings 14:29 |  | fine as spelled (1.00) |
| Jecoliah | Jecoliah | /dʒə.səˈli.əh/ | 2 Kings 15:2 |  | unsure (guessed IPA) (0.50) |
| Shallum | SHAL-uhm | /ˈʃæl.əm/ | 2 Kings 15:10 |  | fine as spelled (1.00) |
| Uzziah | uh-ZY-uh | /əˈzaɪ.ə/ | 2 Kings 15:13 |  | fine as spelled (0.90) |
| Gadi | Gadi | /ˈɡeɪ.də/ | 2 Kings 15:14 |  | unsure (guessed IPA) (0.50) |
| Menahem | Menahem | /mənˈɑhəm/ | 2 Kings 15:14 |  | still wrong (0.64) |
| Pul | PUHL | /pʌl/ | 2 Kings 15:19 |  | still wrong (0.33) |
| Pekahiah | Pekahiah | /ˌpɛkəˈhaɪə/ | 2 Kings 15:22 |  | fine as spelled (0.94) |
| Arieh | Arieh | /ˈeɪ.raɪh/ | 2 Kings 15:25 |  | unsure (guessed IPA) (0.25) |
| Pileser | Pileser | /ˈpi.lə.sər/ | 2 Kings 15:29 |  | unsure (guessed IPA) (0.50) |
| Tiglath | Tiglath | /ˈtɪɡ.ləθ/ | 2 Kings 15:29 |  | unsure (guessed IPA) (0.50) |
| Jerusha | Jerusha | /dʒˈɛrəʃə/ | 2 Kings 15:33 |  | still wrong (0.67) |
| Rezin | Rezin | /rəˌziːn/ | 2 Kings 15:37 |  | still wrong (0.60) |
| Ahaz | AY-haz | /ˈeɪ.hæz/ | 2 Kings 15:38 |  | still wrong (0.75) |
| Urijah | Urijah | /ˈjuː.ri.dʒəh/ | 2 Kings 16:10 |  | unsure (guessed IPA) (0.43) |
| Hezekiah | hez-uh-KY-uh | /ˌhɛz.əˈkaɪ.ə/ | 2 Kings 16:20 |  | fine as spelled (0.86) |
| Gozan | GOH-zan | /ˈɡoʊ.zæn/ | 2 Kings 17:6 |  | fine as spelled (0.80) |
| Habor | HAY-bor | /ˈheɪ.bɔːr/ | 2 Kings 17:6 |  | fine as spelled (0.80) |
| Halah | HAY-la | /ˈheɪ.lə/ | 2 Kings 17:6 | ✅ | overridden (1.00) |
| Avva | Avva | /ˈæv.və/ | 2 Kings 17:24 |  | unsure (guessed IPA) (0.75) |
| Babylon | BAB-ih-luhn | /ˈbæb.ɪ.lən/ | 2 Kings 17:24 |  | still wrong (0.79) |
| Cuthah | Cuthah | /ˈsjuː.θəh/ | 2 Kings 17:24 |  | unsure (guessed IPA) (0.50) |
| Sepharvaim | Sepharvaim | /ˈsiː.fər.veɪm/ | 2 Kings 17:24 |  | fine as spelled (0.88) |
| Ashima | Ashima | /ˈeɪ.ʃi.mə/ | 2 Kings 17:30 |  | fine as spelled (0.80) |
| Benoth | Benoth | /ˈbiː.nəθ/ | 2 Kings 17:30 |  | unsure (guessed IPA) (0.40) |
| Cuth | Cuth | /ˈsʌθ/ | 2 Kings 17:30 |  | unsure (guessed IPA) (0.33) |
| Nergal | Nergal | /ˈnɛr.ɡəl/ | 2 Kings 17:30 |  | unsure (guessed IPA) (0.67) |
| Adrammelech | Adrammelech | /ədˈræm.mə.lək/ | 2 Kings 17:31 |  | fine as spelled (0.89) |
| Anammelech | Anammelech | /əˈnæm.mə.lək/ | 2 Kings 17:31 |  | fine as spelled (0.88) |
| Avvites | Avvites | /ˈæv.vi.təs/ | 2 Kings 17:31 |  | unsure (guessed IPA) (0.58) |
| Nibhaz | Nibhaz | /ˈnɪb.həz/ | 2 Kings 17:31 |  | unsure (guessed IPA) (0.75) |
| Sepharvites | Sepharvites | /səˈfær.vi.təs/ | 2 Kings 17:31 |  | unsure (guessed IPA) (0.55) |
| Tartak | Tartak | /ˈtær.tək/ | 2 Kings 17:31 |  | unsure (guessed IPA) (0.67) |
| Abi | Abi | /ˈeɪ.bə/ | 2 Kings 18:2 |  | unsure (guessed IPA) (0.33) |
| Nehushtan | Nehushtan | /nəˈhʊʃtən/ | 2 Kings 18:4 |  | fine as spelled (0.88) |
| Shalmaneser | Shalmaneser | /ʃəlˈmeɪ.nə.sər/ | 2 Kings 18:9 |  | unsure (guessed IPA) (0.55) |
| Rabsaris | Rabsaris | /ˈræb.sə.rɪs/ | 2 Kings 18:17 |  | fine as spelled (0.88) |
| Rabshakeh | Rabshakeh | /ˈræb.ʃə.kəh/ | 2 Kings 18:17 |  | unsure (guessed IPA) (0.62) |
| Tartan | Tartan | /tˈɑrtən/ | 2 Kings 18:17 |  | fine as spelled (1.00) |
| Asaph | AY-saf | /ˈeɪ.sæf/ | 2 Kings 18:18 |  | still wrong (0.50) |
| Hilkiah | hil-KY-uh | /hɪlˈkaɪ.ə/ | 2 Kings 18:18 |  | fine as spelled (0.83) |
| Joah | JOH-uh | /ˈdʒoʊ.ə/ | 2 Kings 18:18 |  | fine as spelled (1.00) |
| Shebnah | Shebnah | /ˈʃɛb.nəh/ | 2 Kings 18:18 |  | fine as spelled (0.83) |
| Arpad | Arpad | /ˈær.pəd/ | 2 Kings 18:34 |  | unsure (guessed IPA) (0.60) |
| Hena | Hena | /ˈhiː.nə/ | 2 Kings 18:34 |  | fine as spelled (1.00) |
| Ivvah | Ivvah | /ˈɪv.vəh/ | 2 Kings 18:34 |  | unsure (guessed IPA) (0.75) |
| Shebna | Shebna | /ˈʃɛb.nə/ | 2 Kings 18:37 |  | fine as spelled (0.90) |
| Tirhakah | Tirhakah | /ˈtɪr.hə.kəh/ | 2 Kings 19:9 |  | unsure (guessed IPA) (0.50) |
| Rezeph | Rezeph | /ˈriː.zəf/ | 2 Kings 19:12 |  | fine as spelled (0.80) |
| Telassar | Telassar | /ˈtiː.ləs.sər/ | 2 Kings 19:12 |  | unsure (guessed IPA) (0.71) |
| Assyrians | Assyrians | /əsˈɪriːənz/ | 2 Kings 19:35 |  | fine as spelled (1.00) |
| Haddon | Haddon | /hˈædən/ | 2 Kings 19:37 |  | fine as spelled (1.00) |
| Nisroch | Nisroch | /ˈnɪs.rək/ | 2 Kings 19:37 |  | unsure (guessed IPA) (0.75) |
| Sharezer | Sharezer | /ˈʃeɪ.rə.zər/ | 2 Kings 19:37 |  | unsure (guessed IPA) (0.71) |
| Baladan | Baladan | /ˈbeɪ.lə.dən/ | 2 Kings 20:12 |  | unsure (guessed IPA) (0.57) |
| Berodach | Berodach | /ˈbiː.rə.dək/ | 2 Kings 20:12 |  | unsure (guessed IPA) (0.57) |
| Hephzibah | Hephzibah | /ˈhɛpzɪbə/ | 2 Kings 21:1 |  | still wrong (0.38) |
| Uzza | UZ-uh | /ˈʌz.ə/ | 2 Kings 21:18 |  | fine as spelled (0.88) |
| Haruz | Haruz | /ˈheɪ.rəz/ | 2 Kings 21:19 |  | unsure (guessed IPA) (0.50) |
| Jotbah | Jotbah | /ˈdʒɒt.bəh/ | 2 Kings 21:19 |  | unsure (guessed IPA) (0.50) |
| Meshullemeth | Meshullemeth | /məˈʃʌl.lə.məθ/ | 2 Kings 21:19 |  | unsure (guessed IPA) (0.67) |
| Adaiah | uh-DAY-yuh | /əˈdeɪ.jə/ | 2 Kings 22:1 |  | suggestion waiting (0.70) |
| Jedidah | Jedidah | /ˈdʒiː.di.dəh/ | 2 Kings 22:1 |  | unsure (guessed IPA) (0.29) |
| Meshullam | muh-SHOOL-uhm | /məˈʃʊl.əm/ | 2 Kings 22:3 |  | still wrong (0.79) |
| Asaiah | uh-SAY-yuh | /əˈseɪ.jə/ | 2 Kings 22:12 |  | still wrong (0.50) |
| Harhas | Harhas | /ˈhær.həs/ | 2 Kings 22:14 |  | unsure (guessed IPA) (0.50) |
| Tikvah | Tikvah | /ˈtɪk.vəh/ | 2 Kings 22:14 |  | unsure (guessed IPA) (0.75) |
| Topheth | Topheth | /ˈtoʊ.fəθ/ | 2 Kings 23:10 |  | fine as spelled (0.80) |
| Melech | MEE-lek | /ˈmiː.lɛk/ | 2 Kings 23:11 |  | suggestion waiting (0.70) |
| Necoh | Necoh | /ˈniː.səh/ | 2 Kings 23:29 |  | unsure (guessed IPA) (0.20) |
| Hamutal | Hamutal | /ˈheɪ.mə.təl/ | 2 Kings 23:31 |  | unsure (guessed IPA) (0.50) |
| Jeremiah | jer-uh-MY-uh | /ˌdʒɛr.əˈmaɪ.ə/ | 2 Kings 23:31 |  | fine as spelled (1.00) |
| Jehoiakim | juh-HOY-uh-kim | /dʒəˈhɔɪ.ə.kɪm/ | 2 Kings 23:34 |  | still wrong (0.71) |
| Pedaiah | puhdayyuh | /pəˈdeɪ.jə/ | 2 Kings 23:36 | ✅ | overridden (0.83) |
| Rumah | Rumah | /ˈrjuː.məh/ | 2 Kings 23:36 |  | unsure (guessed IPA) (0.67) |
| Zebidah | Zebidah | /ˈziː.bi.dəh/ | 2 Kings 23:36 |  | unsure (guessed IPA) (0.71) |
| Nebuchadnezzar | neb-yoo-kuhd-NEZ-er | /ˌnɛb.jʊ.kədˈnɛz.ər/ | 2 Kings 24:1 |  | fine as spelled (0.85) |
| Elnathan | Elnathan | /ˈɛl.nə.θən/ | 2 Kings 24:8 |  | unsure (guessed IPA) (0.79) |
| Nehushta | Nehushta | /ˈniː.hə.ʃtə/ | 2 Kings 24:8 |  | unsure (guessed IPA) (0.71) |
| Mattaniah | mat-uh-NY-uh | /ˌmæt.əˈnaɪ.ə/ | 2 Kings 24:17 |  | still wrong (0.57) |
| Chaldean | Chaldean | /kælˈdi.ən/ | 2 Kings 25:5 |  | fine as spelled (0.93) |
| Nebuzaradan | Nebuzaradan | /nə.bəˈzeɪ.rə.dən/ | 2 Kings 25:8 |  | unsure (guessed IPA) (0.52) |
| Zephaniah | zef-uh-NY-uh | /ˌzɛf.əˈnaɪ.ə/ | 2 Kings 25:18 |  | fine as spelled (1.00) |
| Jaazaniah | Jaazaniah | /dʒə.ə.zəˈni.əh/ | 2 Kings 25:23 |  | unsure (guessed IPA) (0.56) |
| Johanan | joh-HAY-nan | /dʒoʊˈheɪ.næn/ | 2 Kings 25:23 |  | suggestion waiting (0.71) |
| Kareah | Kareah | /ˈkeɪ.riːh/ | 2 Kings 25:23 |  | unsure (guessed IPA) (0.50) |
| Tanhumeth | Tanhumeth | /ˈtæn.hə.məθ/ | 2 Kings 25:23 |  | unsure (guessed IPA) (0.69) |
| Evilmerodach | Evilmerodach | /ə.vɪlˈmiː.rə.dək/ | 2 Kings 25:27 |  | unsure (guessed IPA) (0.64) |
| Sheth | seth | /sɛθ/ | 1 Chronicles 1:1 | ✅ | overridden (0.83) |
| Henoch | HEE-nok | /ˈhiː.nɒk/ | 1 Chronicles 1:3 |  | fine as spelled (0.80) |
| Diphath | DYfath | /ˈdaɪ.fæθ/ | 1 Chronicles 1:6 | ✅ | overridden (0.80) |
| Rodanim | ROH-duh-nim | /ˈroʊ.də.nɪm/ | 1 Chronicles 1:7 |  | fine as spelled (0.86) |
| Raama | RAY-uh-muh | /ˈreɪ.ə.mə/ | 1 Chronicles 1:9 | ✅ | overridden (0.90) |
| Sabta | SAB-tuh | /ˈsæb.tə/ | 1 Chronicles 1:9 |  | fine as spelled (0.83) |
| Sabtecha | SAB-tih-kah | /ˈsæb.tɪ.kɑː/ | 1 Chronicles 1:9 | ✅ | overridden (0.86) |
| Napthtuhim | naftoohihm | /næfˈtuː.hɪm/ | 1 Chronicles 1:11 | ✅ | overridden (1.00) |
| Caphthorim | KAF-thor-im | /ˈkæf.θɔː.rɪm/ | 1 Chronicles 1:12 |  | still wrong (0.62) |
| Zidon | ZY-don | /ˈzaɪ.dɒn/ | 1 Chronicles 1:13 |  | suggestion waiting (0.70) |
| Arkite | AR-kite | /ˈɑːr.kaɪt/ | 1 Chronicles 1:15 |  | fine as spelled (0.80) |
| Sinite | Sainite | /ˈsaɪ.naɪt/ | 1 Chronicles 1:15 | ✅ | overridden (0.90) |
| Arvadite | AR-vuh-dite | /ˈɑːr.və.daɪt/ | 1 Chronicles 1:16 |  | fine as spelled (1.00) |
| Hamathite | HAYmathite | /ˈheɪ.mə.θaɪt/ | 1 Chronicles 1:16 | ✅ | overridden (0.93) |
| Zemarite | ZEM-uh-rite | /ˈzɛm.ə.raɪt/ | 1 Chronicles 1:16 |  | fine as spelled (0.86) |
| Jaalam | JAY-a-lam | /ˈdʒeɪ.ə.læm/ | 1 Chronicles 1:35 | ✅ | overridden (0.83) |
| Zephi | zeefeye | /ˈziː.faɪ/ | 1 Chronicles 1:36 | ✅ | overridden (1.00) |
| Ezar | EE-zar | /ˈiː.zɑːr/ | 1 Chronicles 1:38 |  | suggestion waiting (0.75) |
| Homam | HOH-mam | /ˈhoʊ.mæm/ | 1 Chronicles 1:39 |  | fine as spelled (0.80) |
| Alian | AYleeun | /ˈeɪ.li.ən/ | 1 Chronicles 1:40 | ✅ | overridden (0.70) |
| Shephi | SHEE-fy | /ˈʃiː.faɪ/ | 1 Chronicles 1:40 |  | fine as spelled (1.00) |
| Hamran | HAM-ran | /ˈhæm.ræn/ | 1 Chronicles 1:41 |  | still wrong (0.75) |
| Jakan | JAY-kan | /ˈdʒeɪ.kæn/ | 1 Chronicles 1:42 | ✅ | overridden (0.80) |
| Zavan | ZAY-van | /ˈzeɪ.væn/ | 1 Chronicles 1:42 | ✅ | overridden (0.80) |
| River | River |  | 1 Chronicles 1:48 |  | fine as spelled |
| Baal-hanan | bay-al-HAY-nan | /ˌbeɪ.əlˈheɪ.næn/ | 1 Chronicles 1:49 |  | still wrong (0.44) |
| Pai | PAY-eye | /ˈpeɪ.aɪ/ | 1 Chronicles 1:50 | ✅ | overridden (1.00) |
| Aliah | uh-LY-uh | /əˈlaɪ.ə/ | 1 Chronicles 1:51 |  | still wrong (0.62) |
| Aholibamah | uh-hol-ih-BAH-muh | /ə.hɒl.ɪˈbɑː.mə/ | 1 Chronicles 1:52 |  | fine as spelled (0.89) |
| Canaanitess | KAY-nuh-nite-ess | /ˈkeɪ.nə.naɪ.tɛs/ | 1 Chronicles 2:3 |  | still wrong (0.78) |
| Pharez | FAIR-ez | /ˈfɛər.ɛz/ | 1 Chronicles 2:4 |  | suggestion waiting (0.70) |
| Dara | DAIRR-uh | /ˈdɛər.ə/ | 1 Chronicles 2:6 | ✅ | overridden (0.88) |
| Achar | aykarr | /ˈeɪ.kɑːr/ | 1 Chronicles 2:7 | ✅ | overridden (0.88) |
| Chelubai | kuhloobeye | /kəˈluː.baɪ/ | 1 Chronicles 2:9 | ✅ | overridden (0.83) |
| Jerahmeel | juh-RAH-mee-el | /dʒəˈrɑː.mi.əl/ | 1 Chronicles 2:9 | ✅ | overridden (0.88) |
| Salma | sallmuh | /ˈsæl.mə/ | 1 Chronicles 2:11 | ✅ | overridden (0.70) |
| Shimea | shimmee-uh | /ˈʃɪm.i.ə/ | 1 Chronicles 2:13 | ✅ | overridden (0.80) |
| Shimma | SHIM-uh | /ˈʃɪm.ə/ | 1 Chronicles 2:13 |  | fine as spelled (1.00) |
| Raddai | RAD-eye | /ˈræd.aɪ/ | 1 Chronicles 2:14 |  | fine as spelled (1.00) |
| Ozem | OH-zem | /ˈoʊ.zɛm/ | 1 Chronicles 2:15 |  | still wrong (0.75) |
| Ishmaelite | ISH-may-el-ite | /ˈɪʃ.meɪ.ə.laɪt/ | 1 Chronicles 2:17 |  | still wrong (0.75) |
| Ishmeelite | ISH-mee-uh-lite | /ˈɪʃ.miː.ə.laɪt/ | 1 Chronicles 2:17 |  | fine as spelled (0.88) |
| Ardon | AR-don | /ˈɑːr.dɒn/ | 1 Chronicles 2:18 |  | fine as spelled (0.80) |
| Jerioth | JER-ee-oth | /ˈdʒɛr.i.ɒθ/ | 1 Chronicles 2:18 |  | fine as spelled (0.83) |
| Jesher | JEE-sher | /ˈdʒiː.ʃər/ | 1 Chronicles 2:18 |  | fine as spelled (0.80) |
| Bezaleel | bih-ZAL-ee-el | /bɪˈzæl.i.ɛl/ | 1 Chronicles 2:20 |  | still wrong (0.56) |
| Abiah | uh-BY-uh | /əˈbaɪ.ə/ | 1 Chronicles 2:24 | ✅ | overridden (0.90) |
| Ashhur | ASH-herr | /ˈæʃ.hɜːr/ | 1 Chronicles 2:24 | ✅ | overridden (0.80) |
| Ashur | ASH-ur | /ˈæʃ.ər/ | 1 Chronicles 2:24 |  | suggestion waiting (0.75) |
| Caleb-ephratah | kay-leb-EF-ruh-tah | /ˌkeɪ.lɛbˈɛf.rə.tɑː/ | 1 Chronicles 2:24 |  | still wrong (0.64) |
| Bunah | BYOO-nuh | /ˈbjuː.nə/ | 1 Chronicles 2:25 |  | still wrong (0.60) |
| Oren | OR-en | /ˈɔːr.ɛn/ | 1 Chronicles 2:25 |  | still wrong (0.55) |
| Atarah | AT-uh-ruh | /ˈæt.ə.rə/ | 1 Chronicles 2:26 |  | fine as spelled (0.80) |
| Eker | EE-ker | /ˈiː.kər/ | 1 Chronicles 2:27 |  | still wrong (0.60) |
| Maaz | MAY-azz | /ˈmeɪ.æz/ | 1 Chronicles 2:27 | ✅ | overridden (1.00) |
| Abishur | AB-ih-shoor | /ˈæb.ɪ.ʃʊər/ | 1 Chronicles 2:28 |  | fine as spelled (0.83) |
| Jada | JAY-duh | /ˈdʒeɪ.də/ | 1 Chronicles 2:28 |  | fine as spelled (1.00) |
| Shammai | SHAM-eye | /ˈʃæm.aɪ/ | 1 Chronicles 2:28 |  | still wrong (0.75) |
| Ahban | AH-ban | /ˈɑː.bæn/ | 1 Chronicles 2:29 |  | still wrong (0.75) |
| Molid | MOH-lid | /ˈmoʊ.lɪd/ | 1 Chronicles 2:29 |  | suggestion waiting (0.60) |
| Appaim | AP-ay-im | /ˈæp.eɪ.ɪm/ | 1 Chronicles 2:30 |  | fine as spelled (0.80) |
| Seled | SEE-led | /ˈsiː.lɛd/ | 1 Chronicles 2:30 |  | fine as spelled (0.80) |
| Ahlai | ahleye | /ˈɑː.laɪ/ | 1 Chronicles 2:31 | ✅ | overridden (0.67) |
| Ishi | IHSH-eye | /ˈɪʃ.aɪ/ | 1 Chronicles 2:31 | ✅ | overridden (1.00) |
| Sheshan | SHEE-shan | /ˈʃiː.ʃæn/ | 1 Chronicles 2:31 |  | fine as spelled (0.80) |
| Zaza | ZAY-zuh | /ˈzeɪ.zə/ | 1 Chronicles 2:33 |  | still wrong (0.75) |
| Jarha | JAR-huh | /ˈdʒɑːr.hə/ | 1 Chronicles 2:34 |  | suggestion waiting (0.40) |
| Attai | AT-eye | /ˈæt.aɪ/ | 1 Chronicles 2:35 |  | still wrong (0.67) |
| Zabad | ZAY-bad | /ˈzeɪ.bæd/ | 1 Chronicles 2:36 | ✅ | overridden (1.00) |
| Ephlal | EF-lal | /ˈɛf.læl/ | 1 Chronicles 2:37 |  | still wrong (0.60) |
| Eleasah | ehleeaysuh | /ˌɛl.iˈeɪ.sə/ | 1 Chronicles 2:39 | ✅ | overridden (0.83) |
| Sisamai | SIS-uh-my | /ˈsɪs.ə.maɪ/ | 1 Chronicles 2:40 |  | fine as spelled (0.93) |
| Sismai | SIS-my | /ˈsɪs.maɪ/ | 1 Chronicles 2:40 |  | fine as spelled (1.00) |
| Jekamiah | jek-uh-MY-uh | /ˌdʒɛk.əˈmaɪ.ə/ | 1 Chronicles 2:41 |  | fine as spelled (0.88) |
| Jorkeam | JOR-kee-am | /ˈdʒɔːr.ki.æm/ | 1 Chronicles 2:44 |  | still wrong (0.71) |
| Jorkoam | JOR-koh-am | /ˈdʒɔːr.koʊ.æm/ | 1 Chronicles 2:44 |  | fine as spelled (0.86) |
| Raham | RAY-ham | /ˈreɪ.hæm/ | 1 Chronicles 2:44 | ✅ | overridden (0.80) |
| Beth-zur | bethzerr | /bɛθˈzɜːr/ | 1 Chronicles 2:45 | ✅ | overridden (0.83) |
| Gazez | GAY-zez | /ˈɡeɪ.zɛz/ | 1 Chronicles 2:46 |  | fine as spelled (0.80) |
| Moza | MOH-zuh | /ˈmoʊ.zə/ | 1 Chronicles 2:46 |  | fine as spelled (0.80) |
| Gesham | geeshaam | /ˈɡiː.ʃæm/ | 1 Chronicles 2:47 | ✅ | overridden (0.80) |
| Geshan | geeshaan | /ˈɡiː.ʃæn/ | 1 Chronicles 2:47 | ✅ | overridden (0.80) |
| Jahdai | JAH-dye | /ˈdʒɑː.daɪ/ | 1 Chronicles 2:47 |  | fine as spelled (1.00) |
| Jothan | JO-thann | /ˈdʒoʊ.θæn/ | 1 Chronicles 2:47 | ✅ | overridden (0.70) |
| Regem | REE-ghem | /ˈriː.ɡɛm/ | 1 Chronicles 2:47 | ✅ | overridden (0.90) |
| Shaaph | SHAY-aff | /ˈʃeɪ.æf/ | 1 Chronicles 2:47 | ✅ | overridden (1.00) |
| Sheber | SHEE-ber | /ˈʃiː.bər/ | 1 Chronicles 2:48 |  | fine as spelled (0.80) |
| Tirhanah | tur-HAY-nuh | /tɜːrˈheɪ.nə/ | 1 Chronicles 2:48 |  | still wrong (0.71) |
| Achsa | AK-suh | /ˈæk.sə/ | 1 Chronicles 2:49 |  | still wrong (0.75) |
| Gibea | GIB-ee-uh | /ˈɡɪb.i.ə/ | 1 Chronicles 2:49 |  | fine as spelled (0.80) |
| Machbena | mak-BEE-nuh | /mækˈbiː.nə/ | 1 Chronicles 2:49 |  | still wrong (0.71) |
| Machbenah | mak-BEE-nuh | /mækˈbiː.nə/ | 1 Chronicles 2:49 |  | suggestion waiting (0.71) |
| Ephratah | EF-ruh-tah | /ˈɛf.rə.tɑː/ | 1 Chronicles 2:50 |  | still wrong (0.50) |
| Kirjath-jearim | kur-jath-JEE-uh-rim | /ˌkɜːr.dʒæθˈdʒiː.ə.rɪm/ | 1 Chronicles 2:50 |  | still wrong (0.50) |
| Beth-gader | beth-GAY-der | /bɛθˈɡeɪ.dər/ | 1 Chronicles 2:51 |  | fine as spelled (1.00) |
| Gader | GAY-der | /ˈɡeɪ.dər/ | 1 Chronicles 2:51 |  | fine as spelled (1.00) |
| Hareph | HAIR-ef | /ˈhɛər.ɛf/ | 1 Chronicles 2:51 |  | fine as spelled (0.80) |
| Haroeh | huroh-eh | /həˈroʊ.ɛ/ | 1 Chronicles 2:52 | ✅ | overridden (0.70) |
| Manahethites | MAN-uh-heth-ites | /ˈmæn.ə.hɛθ.aɪts/ | 1 Chronicles 2:52 |  | still wrong (0.70) |
| Menuhoth | muh-NOO-hoth | /məˈnuː.hɒθ/ | 1 Chronicles 2:52 | ✅ | overridden (0.79) |
| Eshtaolites | ESH-tay-uh-lites | /ˈɛʃ.teɪ.ə.laɪts/ | 1 Chronicles 2:53 |  | still wrong (0.75) |
| Eshtaulites | ESH-taw-lites | /ˈɛʃ.tɔː.laɪts/ | 1 Chronicles 2:53 |  | fine as spelled (1.00) |
| Ithrites | ITH-rites | /ˈɪθ.raɪts/ | 1 Chronicles 2:53 |  | still wrong (0.43) |
| Mishraites | MISH-ruh-ites | /ˈmɪʃ.rə.aɪts/ | 1 Chronicles 2:53 |  | still wrong (0.71) |
| Puhites | PYOO-hites | /ˈpjuː.haɪts/ | 1 Chronicles 2:53 |  | fine as spelled (0.93) |
| Puthites | PYOO-thites | /ˈpjuː.θaɪts/ | 1 Chronicles 2:53 |  | fine as spelled (0.83) |
| Shumathites | SHOO-muh-thites | /ˈʃuː.mə.θaɪts/ | 1 Chronicles 2:53 |  | fine as spelled (0.86) |
| Zareathites | ZAR-ee-uh-thites | /ˈzær.i.ə.θaɪts/ | 1 Chronicles 2:53 |  | fine as spelled (0.89) |
| Zorathites | ZOR-uh-thites | /ˈzɔːr.ə.θaɪts/ | 1 Chronicles 2:53 |  | fine as spelled (0.86) |
| Ataroth | AT-uh-roth | /ˈæt.ə.rɒθ/ | 1 Chronicles 2:54 |  | suggestion waiting (0.75) |
| Atroth | AT-roth | /ˈæt.rɒθ/ | 1 Chronicles 2:54 | ✅ | overridden (1.00) |
| Manahathites | MAN-uh-hath-ites | /ˈmæn.ə.hæθ.aɪts/ | 1 Chronicles 2:54 |  | still wrong (0.67) |
| Netophathites | nuh-TOF-uh-thites | /nəˈtɒf.ə.θaɪts/ | 1 Chronicles 2:54 |  | fine as spelled (1.00) |
| Zorites | ZOR-ites | /ˈzɔːr.aɪts/ | 1 Chronicles 2:54 |  | fine as spelled (1.00) |
| Hemath | HEE-math | /ˈhiː.mæθ/ | 1 Chronicles 2:55 |  | fine as spelled (0.80) |
| Jabez | JAY-bez | /ˈdʒeɪ.bɛz/ | 1 Chronicles 2:55 |  | fine as spelled (1.00) |
| Shimeathites | SHIM-ee-uh-thites | /ˈʃɪm.i.ə.θaɪts/ | 1 Chronicles 2:55 |  | still wrong (0.62) |
| Sucathites | SOO-kuh-thites | /ˈsuː.kə.θaɪts/ | 1 Chronicles 2:55 |  | fine as spelled (1.00) |
| Suchathites | SOO-kuh-thites | /ˈsuː.kə.θaɪts/ | 1 Chronicles 2:55 |  | fine as spelled (0.94) |
| Tirathites | TY-ruh-thites | /ˈtaɪ.rə.θaɪts/ | 1 Chronicles 2:55 |  | still wrong (0.71) |
| Daniel | DAN-yuhl | /ˈdæn.jəl/ | 1 Chronicles 3:1 |  | fine as spelled (1.00) |
| Maachah | MAY-a-kuh | /ˈmeɪ.ə.kə/ | 1 Chronicles 3:2 | ✅ | overridden (0.82) |
| Bath-shua | bath-SHOO-uh | /bæθˈʃuː.ə/ | 1 Chronicles 3:5 |  | still wrong (0.50) |
| Bathshua | bath-SHOO-uh | /bæθˈʃuː.ə/ | 1 Chronicles 3:5 |  | still wrong (0.33) |
| Nogah | NOH-guh | /ˈnoʊ.ɡə/ | 1 Chronicles 3:7 |  | fine as spelled (1.00) |
| Abia | uh-BY-uh | /əˈbaɪ.ə/ | 1 Chronicles 3:10 | ✅ | overridden (0.90) |
| Jeconiah | jek-uh-NY-uh | /ˌdʒɛk.əˈnaɪ.ə/ | 1 Chronicles 3:16 |  | fine as spelled (1.00) |
| Salathiel | suhlaytheeehl | /səˈleɪ.θi.ɛl/ | 1 Chronicles 3:17 | ✅ | overridden (0.81) |
| Shealtiel | shee-AL-tee-el | /ʃiˈæl.ti.ɛl/ | 1 Chronicles 3:17 |  | suggestion waiting (0.75) |
| Hoshama | HOSH-uh-muh | /ˈhɒʃ.ə.mə/ | 1 Chronicles 3:18 |  | suggestion waiting (0.75) |
| Jecamiah | jek-uh-MY-uh | /ˌdʒɛk.əˈmaɪ.ə/ | 1 Chronicles 3:18 |  | fine as spelled (1.00) |
| Malchiram | mal-KY-ruhm | /mælˈkaɪ.rəm/ | 1 Chronicles 3:18 |  | suggestion waiting (0.75) |
| Nedabiah | ned-uh-BY-uh | /ˌnɛd.əˈbaɪ.ə/ | 1 Chronicles 3:18 |  | fine as spelled (0.87) |
| Shenazar | shih-NAZ-er | /ʃɪˈnæz.ər/ | 1 Chronicles 3:18 |  | fine as spelled (0.86) |
| Shenazzar | shuh-NAZ-er | /ʃəˈnæz.ər/ | 1 Chronicles 3:18 |  | fine as spelled (1.00) |
| Hananiah | han-uh-NY-uh | /ˌhæn.əˈnaɪ.ə/ | 1 Chronicles 3:19 |  | fine as spelled (0.80) |
| Zerubbabel | zuh-RUB-uh-buhl | /zəˈrʌb.ə.bəl/ | 1 Chronicles 3:19 |  | fine as spelled (0.95) |
| Berechiah | behr-uh-KEYE-uh | /ˌbɛr.əˈkaɪ.ə/ | 1 Chronicles 3:20 | ✅ | overridden (1.00) |
| Hasadiah | has-uh-DY-uh | /ˌhæs.əˈdaɪ.ə/ | 1 Chronicles 3:20 |  | fine as spelled (0.94) |
| Hashubah | huh-SHOO-buh | /həˈʃuː.bə/ | 1 Chronicles 3:20 |  | still wrong (0.75) |
| Jushab | jooshab | /ˈdʒuː.ʃæb/ | 1 Chronicles 3:20 | ✅ | overridden (1.00) |
| Jushab-hesed | joo-shaab-HEE-sehd | /ˌdʒuː.ʃæbˈhiː.sɛd/ | 1 Chronicles 3:20 | ✅ | overridden (0.90) |
| Ohel | OH-hehl | /ˈoʊ.hɛl/ | 1 Chronicles 3:20 | ✅ | overridden (1.00) |
| Arnan | AR-nan | /ˈɑːr.næn/ | 1 Chronicles 3:21 |  | fine as spelled (0.80) |
| Jesaiah | jih-ZEYE-uh | /dʒɪˈzaɪ.ə/ | 1 Chronicles 3:21 | ✅ | overridden (0.80) |
| Jeshaiah | juh-SHAY-yuh | /dʒəˈʃeɪ.jə/ | 1 Chronicles 3:21 |  | still wrong (0.67) |
| Pelatiah | pel-uh-TY-uh | /ˌpɛl.əˈtaɪ.ə/ | 1 Chronicles 3:21 |  | fine as spelled (0.86) |
| Rephaiah | ruh-FAY-yuh | /rəˈfeɪ.jə/ | 1 Chronicles 3:21 |  | suggestion waiting (0.75) |
| Shecaniah | shek-uh-NY-uh | /ˌʃɛk.əˈnaɪ.ə/ | 1 Chronicles 3:21 |  | fine as spelled (1.00) |
| Shechaniah | shek-uh-NY-uh | /ˌʃɛk.əˈnaɪ.ə/ | 1 Chronicles 3:21 |  | fine as spelled (1.00) |
| Bariah | buh-RY-uh | /bəˈraɪ.ə/ | 1 Chronicles 3:22 |  | fine as spelled (1.00) |
| Hattush | HAT-oosh | /ˈhæt.ʊʃ/ | 1 Chronicles 3:22 | ✅ | overridden (1.00) |
| Igeal | IG-ee-ul | /ˈɪɡ.i.əl/ | 1 Chronicles 3:22 |  | still wrong (0.40) |
| Neariah | nee-uh-RY-uh | /ˌniː.əˈraɪ.ə/ | 1 Chronicles 3:22 |  | fine as spelled (0.92) |
| Azrikam | az-RY-kuhm | /æzˈraɪ.kəm/ | 1 Chronicles 3:23 |  | fine as spelled (0.86) |
| Elioenai | el-ee-oh-EE-ny | /ˌɛl.i.oʊˈiː.naɪ/ | 1 Chronicles 3:23 |  | still wrong (0.79) |
| Hizkiah | hiz-KY-uh | /hɪzˈkaɪ.ə/ | 1 Chronicles 3:23 |  | suggestion waiting (0.77) |
| Akkub | AK-uhb | /ˈæk.əb/ | 1 Chronicles 3:24 |  | still wrong (0.75) |
| Anani | uhnayneye | /əˈneɪ.naɪ/ | 1 Chronicles 3:24 | ✅ | overridden (1.00) |
| Dalaiah | duh-LAY-uh | /dəˈleɪ.ə/ | 1 Chronicles 3:24 |  | suggestion waiting (0.73) |
| Delaiah | duh-LAY-yuhh | /dəˈleɪ.jə/ | 1 Chronicles 3:24 | ✅ | overridden (0.92) |
| Eliashib | ee-LY-uh-shib | /ɪˈlaɪ.ə.ʃɪb/ | 1 Chronicles 3:24 |  | still wrong (0.57) |
| Hodaiah | hoh-DY-uh | /hoʊˈdaɪ.ə/ | 1 Chronicles 3:24 |  | fine as spelled (0.92) |
| Hodaviah | hod-uh-VY-uh | /ˌhɒd.əˈvaɪ.ə/ | 1 Chronicles 3:24 |  | fine as spelled (0.80) |
| Pelaiah | puhlayyuh | /pəˈleɪ.jə/ | 1 Chronicles 3:24 | ✅ | overridden (0.83) |
| Ahumai | uh-HYOO-my | /əˈhjuː.maɪ/ | 1 Chronicles 4:2 |  | fine as spelled (0.83) |
| Jahath | JAY-hath | /ˈdʒeɪ.hæθ/ | 1 Chronicles 4:2 | ✅ | overridden (0.80) |
| Lahad | LAY-had | /ˈleɪ.hæd/ | 1 Chronicles 4:2 | ✅ | overridden (1.00) |
| Reaiah | ree-AY-yuh | /riˈeɪ.jə/ | 1 Chronicles 4:2 |  | still wrong (0.60) |
| Hazelelponi | haz-ih-LEL-poh-ny | /ˌhæz.ɪˈlɛl.poʊ.naɪ/ | 1 Chronicles 4:3 |  | still wrong (0.68) |
| Hazzelelponi | haz-uh-lel-POH-ny | /ˌhæz.ə.lɛlˈpoʊ.naɪ/ | 1 Chronicles 4:3 |  | suggestion waiting (0.77) |
| Idbash | ID-bash | /ˈɪd.bæʃ/ | 1 Chronicles 4:3 |  | fine as spelled (0.80) |
| Ishma | ISH-muh | /ˈɪʃ.mə/ | 1 Chronicles 4:3 |  | fine as spelled (1.00) |
| Hushah | hyoosha | /ˈhjuː.ʃə/ | 1 Chronicles 4:4 | ✅ | overridden (0.82) |
| Helah | HEE-luh | /ˈhiː.lə/ | 1 Chronicles 4:5 |  | fine as spelled (1.00) |
| Ahuzam | uh-HYOO-zam | /əˈhjuː.zæm/ | 1 Chronicles 4:6 |  | still wrong (0.57) |
| Ahuzzam | uh-HUZ-am | /əˈhʌz.æm/ | 1 Chronicles 4:6 |  | fine as spelled (0.83) |
| Haahashtari | hay-uh-HASH-tuh-reye | /ˌheɪ.əˈhæʃ.tə.raɪ/ | 1 Chronicles 4:6 | ✅ | overridden (1.00) |
| Temeni | TEM-uh-ny | /ˈtɛm.ə.naɪ/ | 1 Chronicles 4:6 |  | fine as spelled (0.83) |
| Ethnan | EHTH-nan | /ˈɛθ.næn/ | 1 Chronicles 4:7 | ✅ | overridden (0.80) |
| Jezoar | jih-ZOH-ar | /dʒɪˈzoʊ.ɑːr/ | 1 Chronicles 4:7 |  | still wrong (0.58) |
| Aharhel | uh-HAR-hel | /əˈhɑːr.hɛl/ | 1 Chronicles 4:8 |  | fine as spelled (1.00) |
| Anub | aynuhb | /ˈeɪ.nʌb/ | 1 Chronicles 4:8 | ✅ | overridden (1.00) |
| Coz | koz | /kɒz/ | 1 Chronicles 4:8 | ✅ | overridden (0.88) |
| Hakkoz | HAK-oz | /ˈhæk.ɒz/ | 1 Chronicles 4:8 |  | fine as spelled (1.00) |
| Harum | HAIR-uhm | /ˈhɛər.əm/ | 1 Chronicles 4:8 |  | fine as spelled (1.00) |
| Zobebah | zoh-BEE-buh | /zoʊˈbiː.bə/ | 1 Chronicles 4:8 |  | fine as spelled (1.00) |
| Chelub | KEE-lub | /ˈkiː.lʌb/ | 1 Chronicles 4:11 |  | fine as spelled (0.80) |
| Eshton | ESH-ton | /ˈɛʃ.tɒn/ | 1 Chronicles 4:11 |  | fine as spelled (0.80) |
| Mehir | MEE-hur | /ˈmiː.hər/ | 1 Chronicles 4:11 |  | fine as spelled (1.00) |
| Shuhah | SHOO-huh | /ˈʃuː.hə/ | 1 Chronicles 4:11 | ✅ | overridden (0.88) |
| Beth-rapha | beth-RAY-fuh | /bɛθˈreɪ.fə/ | 1 Chronicles 4:12 |  | suggestion waiting (0.74) |
| Ir-nahash | eerr-NAY-haash | /ɪərˈneɪ.hæʃ/ | 1 Chronicles 4:12 | ✅ | overridden (1.00) |
| Paseah | puh-SEE-uh | /pəˈsiː.ə/ | 1 Chronicles 4:12 |  | fine as spelled (0.80) |
| Rapha | RAY-fuh | /ˈreɪ.fə/ | 1 Chronicles 4:12 |  | suggestion waiting (0.75) |
| Recah | REE-kuh | /ˈriː.kə/ | 1 Chronicles 4:12 |  | fine as spelled (1.00) |
| Rechah | reeka | /ˈriː.kə/ | 1 Chronicles 4:12 | ✅ | overridden (1.00) |
| Tehinnah | tuh-HIN-uh | /təˈhɪn.ə/ | 1 Chronicles 4:12 |  | fine as spelled (1.00) |
| Hathath | haythath | /ˈheɪ.θæθ/ | 1 Chronicles 4:13 | ✅ | overridden (1.00) |
| Charashim | KAR-uh-shihmm | /ˈkær.ə.ʃɪm/ | 1 Chronicles 4:14 | ✅ | overridden (0.86) |
| Ge | gay | /ɡeɪ/ | 1 Chronicles 4:14 | ✅ | overridden (1.00) |
| Harashim | huh-RASH-ihmm | /həˈræʃ.ɪm/ | 1 Chronicles 4:14 | ✅ | overridden (1.00) |
| Meonothai | mee-ON-oh-thy | /miˈɒn.oʊ.θaɪ/ | 1 Chronicles 4:14 |  | fine as spelled (0.86) |
| Iru | eyeroo | /ˈaɪ.ruː/ | 1 Chronicles 4:15 | ✅ | overridden (1.00) |
| Naam | NAY-am | /ˈneɪ.æm/ | 1 Chronicles 4:15 |  | still wrong (0.50) |
| Asareel | uh-SAR-ee-el | /əˈsær.i.ɛl/ | 1 Chronicles 4:16 |  | still wrong (0.50) |
| Asarel | AS-uh-rel | /ˈæs.ə.rɛl/ | 1 Chronicles 4:16 |  | fine as spelled (0.83) |
| Jehaleleel | jih-HAL-ih-leel | /dʒɪˈhæl.ɪ.liːl/ | 1 Chronicles 4:16 |  | still wrong (0.44) |
| Jehallelel | juh-HAL-uh-lel | /dʒəˈhæl.ə.lɛl/ | 1 Chronicles 4:16 |  | suggestion waiting (0.78) |
| Tiria | TIR-ee-uh | /ˈtɪr.i.ə/ | 1 Chronicles 4:16 |  | fine as spelled (1.00) |
| Ziphah | ZY-fuh | /ˈzaɪ.fə/ | 1 Chronicles 4:16 |  | fine as spelled (0.90) |
| Ezra | EZ-ruh | /ˈɛz.rə/ | 1 Chronicles 4:17 |  | fine as spelled (1.00) |
| Ezrah | EZ-ruh | /ˈɛz.rə/ | 1 Chronicles 4:17 |  | fine as spelled (1.00) |
| Ishbah | ISH-buh | /ˈɪʃ.bə/ | 1 Chronicles 4:17 |  | still wrong (0.75) |
| Jalon | JAY-lon | /ˈdʒeɪ.lɒn/ | 1 Chronicles 4:17 |  | fine as spelled (0.80) |
| Mered | meerehd | /ˈmiː.rɛd/ | 1 Chronicles 4:17 | ✅ | overridden (1.00) |
| Bithiah | bih-THY-uh | /bɪˈθaɪ.ə/ | 1 Chronicles 4:18 |  | still wrong (0.50) |
| Jehudijah | jeh-hyoo-DY-juh | /ˌdʒɛ.hjuːˈdaɪ.dʒə/ | 1 Chronicles 4:18 |  | still wrong (0.56) |
| Jekuthiel | juh-KYOO-thee-el | /dʒəˈkjuː.θi.əl/ | 1 Chronicles 4:18 |  | fine as spelled (0.89) |
| Jered | JEERR-ehd | /ˈdʒɪər.ɛd/ | 1 Chronicles 4:18 | ✅ | overridden (1.00) |
| Jewess | Jewess | /dʒˈuːəs/ | 1 Chronicles 4:18 |  | still wrong (0.75) |
| Socho | SOH-koh | /ˈsoʊ.koʊ/ | 1 Chronicles 4:18 |  | suggestion waiting (0.75) |
| Soco | SOH-koh | /ˈsoʊ.koʊ/ | 1 Chronicles 4:18 |  | fine as spelled (1.00) |
| Garmite | GAR-mite | /ˈɡɑːr.maɪt/ | 1 Chronicles 4:19 |  | fine as spelled (1.00) |
| Hodiah | hoh-DY-uh | /hoʊˈdaɪ.ə/ | 1 Chronicles 4:19 |  | fine as spelled (0.92) |
| Maachathite | muh-AK-uh-thite | /məˈæk.ə.θaɪt/ | 1 Chronicles 4:19 |  | fine as spelled (0.81) |
| Naham | NAY-ham | /ˈneɪ.hæm/ | 1 Chronicles 4:19 | ✅ | overridden (0.80) |
| Ben-hanan | behn-HAY-nan | /bɛnˈheɪ.næn/ | 1 Chronicles 4:20 | ✅ | overridden (0.88) |
| Ben-zoheth | ben-ZOH-heth | /bɛnˈzoʊ.hɛθ/ | 1 Chronicles 4:20 |  | fine as spelled (0.94) |
| Rinnah | RIN-uh | /ˈrɪn.ə/ | 1 Chronicles 4:20 |  | fine as spelled (1.00) |
| Shimon | sheyemuhn | /ˈʃaɪ.mən/ | 1 Chronicles 4:20 | ✅ | overridden (1.00) |
| Tilon | TY-lon | /ˈtaɪ.lɒn/ | 1 Chronicles 4:20 |  | fine as spelled (0.80) |
| Zoheth | ZOH-heth | /ˈzoʊ.hɛθ/ | 1 Chronicles 4:20 |  | fine as spelled (1.00) |
| Ashbea | ash-BEE-uh | /æʃˈbiː.ə/ | 1 Chronicles 4:21 |  | fine as spelled (0.80) |
| Laadah | LAY-uh-da | /ˈleɪ.ə.də/ | 1 Chronicles 4:21 | ✅ | overridden (0.92) |
| Lecah | LEE-kuh | /ˈliː.kə/ | 1 Chronicles 4:21 |  | fine as spelled (1.00) |
| Chozeba | koh-ZEE-buh | /koʊˈziː.bə/ | 1 Chronicles 4:22 |  | fine as spelled (1.00) |
| Cozeba | koh-ZEE-buh | /koʊˈziː.bə/ | 1 Chronicles 4:22 |  | fine as spelled (1.00) |
| Jashubi-lehem | juh-shoo-bih-LEE-hem | /dʒəˌʃuː.bɪˈliː.hɛm/ | 1 Chronicles 4:22 |  | still wrong (0.68) |
| Jashubilehem | juh-shoo-bih-LEE-hem | /dʒəˌʃuː.bɪˈliː.hɛm/ | 1 Chronicles 4:22 |  | still wrong (0.55) |
| Jokim | JOH-kim | /ˈdʒoʊ.kɪm/ | 1 Chronicles 4:22 |  | fine as spelled (1.00) |
| Saraph | SAIR-af | /ˈsɛər.æf/ | 1 Chronicles 4:22 |  | fine as spelled (0.80) |
| Netaim | nuhtayihm | /nəˈteɪ.ɪm/ | 1 Chronicles 4:23 | ✅ | overridden (0.83) |
| Jarib | JAIR-ib | /ˈdʒeɪ.rɪb/ | 1 Chronicles 4:24 |  | fine as spelled (0.80) |
| Hammuel | HAM-yoo-el | /ˈhæm.jʊ.əl/ | 1 Chronicles 4:26 |  | fine as spelled (0.80) |
| Zacchur | ZAK-ur | /ˈzæk.ər/ | 1 Chronicles 4:26 |  | fine as spelled (1.00) |
| Beer-sheba | beer-SHEE-buh | /ˌbɪərˈʃiː.bə/ | 1 Chronicles 4:28 |  | fine as spelled (1.00) |
| Hazar-shual | hay-zar-SHOO-ul | /ˌheɪ.zɑːrˈʃuː.əl/ | 1 Chronicles 4:28 |  | suggestion waiting (0.72) |
| Hazarshual | hay-zar-SHOO-uhl | /ˌheɪ.zɑːrˈʃuː.əl/ | 1 Chronicles 4:28 |  | fine as spelled (0.89) |
| Tolad | TOH-lad | /ˈtoʊ.læd/ | 1 Chronicles 4:29 |  | fine as spelled (1.00) |
| Beth-birei | beth-BIR-ee-eye | /bɛθˈbɪr.i.aɪ/ | 1 Chronicles 4:31 |  | fine as spelled (0.88) |
| Beth-marcaboth | beth-MAR-kuh-both | /bɛθˈmɑːr.kə.bɒθ/ | 1 Chronicles 4:31 |  | fine as spelled (0.95) |
| Biri | BIR-eye | /ˈbɪr.aɪ/ | 1 Chronicles 4:31 |  | still wrong (0.50) |
| Hazar-susim | hay-zar-SOO-sim | /ˌheɪ.zɑːrˈsuː.sɪm/ | 1 Chronicles 4:31 |  | fine as spelled (0.90) |
| Susim | SOO-sim | /ˈsuː.sɪm/ | 1 Chronicles 4:31 |  | fine as spelled (0.90) |
| Tochen | TOH-ken | /ˈtoʊ.kɛn/ | 1 Chronicles 4:32 |  | fine as spelled (0.80) |
| Jamlech | JAM-lek | /ˈdʒæm.lɛk/ | 1 Chronicles 4:34 |  | fine as spelled (0.92) |
| Joshah | JOH-shuh | /ˈdʒoʊ.ʃə/ | 1 Chronicles 4:34 |  | still wrong (0.75) |
| Meshobab | muh-SHOH-bab | /məˈʃoʊ.bæb/ | 1 Chronicles 4:34 | ✅ | overridden (1.00) |
| Asiel | AY-see-el | /ˈeɪ.si.ɛl/ | 1 Chronicles 4:35 |  | still wrong (0.40) |
| Joshibiah | josh-ih-BY-uh | /ˌdʒɒʃ.ɪˈbaɪ.ə/ | 1 Chronicles 4:35 |  | suggestion waiting (0.71) |
| Josibiah | jos-ih-BY-uh | /ˌdʒɒs.ɪˈbaɪ.ə/ | 1 Chronicles 4:35 |  | still wrong (0.57) |
| Adiel | AY-dee-el | /ˈeɪ.di.ɛl/ | 1 Chronicles 4:36 |  | still wrong (0.60) |
| Jaakobah | jay-uh-KOH-buh | /ˌdʒeɪ.əˈkoʊ.bə/ | 1 Chronicles 4:36 |  | still wrong (0.79) |
| Jeshohaiah | jesh-oh-HAY-yuh | /ˌdʒɛʃ.oʊˈheɪ.jə/ | 1 Chronicles 4:36 |  | suggestion waiting (0.75) |
| Jesimiel | juh-SIM-ee-el | /dʒəˈsɪm.i.ɛl/ | 1 Chronicles 4:36 |  | still wrong (0.44) |
| Jedaiah | ja-DAY-yuh | /dʒəˈdeɪ.jə/ | 1 Chronicles 4:37 | ✅ | overridden (0.83) |
| Shimri | SHIM-ry | /ˈʃɪm.raɪ/ | 1 Chronicles 4:37 |  | suggestion waiting (0.73) |
| Shiphi | sheyefeye | /ˈʃaɪ.faɪ/ | 1 Chronicles 4:37 | ✅ | overridden (1.00) |
| Ziza | ZY-zuh | /ˈzaɪ.zə/ | 1 Chronicles 4:37 |  | still wrong (0.62) |
| Meunim | muh-YOO-nim | /məˈjuː.nɪm/ | 1 Chronicles 4:41 | ✅ | overridden (0.93) |
| Gog | GOG | /ɡɒɡ/ | 1 Chronicles 5:4 |  | fine as spelled (1.00) |
| Reaia | ree-AY-uh | /riːˈeɪ.ə/ | 1 Chronicles 5:5 |  | still wrong (0.75) |
| Beerah | bee-EE-ruh | /biˈɪər.ə/ | 1 Chronicles 5:6 |  | fine as spelled (0.80) |
| Pilneser | pil-NEE-zer | /pɪlˈniː.zər/ | 1 Chronicles 5:6 |  | still wrong (0.75) |
| Tilgath | TIL-gath | /ˈtɪl.ɡæθ/ | 1 Chronicles 5:6 |  | fine as spelled (0.83) |
| Tilgath-pilneser | til-gath-pil-NEE-zer | /ˌtɪl.ɡæθ.pɪlˈniː.zər/ | 1 Chronicles 5:6 |  | suggestion waiting (0.75) |
| Jeiel | juh-EYE-el | /dʒəˈaɪ.əl/ | 1 Chronicles 5:7 |  | still wrong (0.40) |
| Azaz | AY-zaz | /ˈeɪ.zæz/ | 1 Chronicles 5:8 |  | still wrong (0.50) |
| Baal-meon | bay-al-MEE-on | /ˌbeɪ.əlˈmiː.ɒn/ | 1 Chronicles 5:8 | ✅ | overridden (0.88) |
| Hagarites | HAG-uh-rites | /ˈhæɡ.ə.raɪts/ | 1 Chronicles 5:10 |  | fine as spelled (1.00) |
| Hagrites | HAG-rites | /ˈhæɡ.raɪts/ | 1 Chronicles 5:10 |  | fine as spelled (0.93) |
| Salchah | SAL-kuh | /ˈsæl.kə/ | 1 Chronicles 5:11 |  | fine as spelled (0.90) |
| Jaanai | jayuhneye | /ˈdʒeɪ.ə.naɪ/ | 1 Chronicles 5:12 | ✅ | overridden (1.00) |
| Janai | jayneye | /ˈdʒeɪ.naɪ/ | 1 Chronicles 5:12 | ✅ | overridden (1.00) |
| Shapham | SHAY-fam | /ˈʃeɪ.fæm/ | 1 Chronicles 5:12 | ✅ | overridden (0.80) |
| Jacan | JAY-kan | /ˈdʒeɪ.kæn/ | 1 Chronicles 5:13 | ✅ | overridden (0.80) |
| Jachan | JAY-kan | /ˈdʒeɪ.kæn/ | 1 Chronicles 5:13 | ✅ | overridden (0.80) |
| Jorai | JOR-eye | /ˈdʒɔːr.aɪ/ | 1 Chronicles 5:13 |  | suggestion waiting (0.75) |
| Zia | ZEYE-uh | /ˈzaɪ.ə/ | 1 Chronicles 5:13 | ✅ | overridden (0.88) |
| Huri | HYOOR-eye | /ˈhjʊər.aɪ/ | 1 Chronicles 5:14 |  | still wrong (0.50) |
| Jahdo | JAH-doh | /ˈdʒɑː.doʊ/ | 1 Chronicles 5:14 |  | fine as spelled (1.00) |
| Jaroah | juh-ROH-uh | /dʒəˈroʊ.ə/ | 1 Chronicles 5:14 |  | fine as spelled (1.00) |
| Jeshishai | juh-SHISH-eye | /dʒəˈʃɪʃ.aɪ/ | 1 Chronicles 5:14 |  | suggestion waiting (0.75) |
| Abdiel | AB-dee-el | /ˈæb.di.ɛl/ | 1 Chronicles 5:15 |  | still wrong (0.67) |
| Ahi | AY-hy | /ˈeɪ.haɪ/ | 1 Chronicles 5:15 |  | still wrong (0.33) |
| Sharon | SHAIR-uhn | /ˈʃær.ən/ | 1 Chronicles 5:16 |  | fine as spelled (0.80) |
| Nephish | NEE-fish | /ˈniː.fɪʃ/ | 1 Chronicles 5:19 |  | fine as spelled (0.80) |
| Nodab | NOH-dab | /ˈnoʊ.dæb/ | 1 Chronicles 5:19 |  | fine as spelled (1.00) |
| Baal-hermon | bay-al-HERR-mon | /ˌbeɪ.əlˈhɜːr.mɒn/ | 1 Chronicles 5:23 | ✅ | overridden (0.90) |
| Azriel | AZ-ree-el | /ˈæz.ri.ɛl/ | 1 Chronicles 5:24 |  | still wrong (0.75) |
| Eliel | EE-lee-ehll | /ˈiː.li.ɛl/ | 1 Chronicles 5:24 | ✅ | overridden (1.00) |
| Jahdiel | JAH-dee-el | /ˈdʒɑː.di.ɛl/ | 1 Chronicles 5:24 |  | fine as spelled (0.83) |
| Hara | HAIR-uh | /ˈhɛər.ə/ | 1 Chronicles 5:26 |  | still wrong (0.75) |
| Abishua | uh-BISH-oo-uh | /əˈbɪʃ.u.ə/ | 1 Chronicles 6:4 |  | fine as spelled (1.00) |
| Uzzi | UHZ-eye | /ˈʌz.aɪ/ | 1 Chronicles 6:5 | ✅ | overridden (1.00) |
| Meraioth | muh-RAY-oth | /məˈreɪ.ɒθ/ | 1 Chronicles 6:6 |  | suggestion waiting (0.75) |
| Zerahiah | zer-uh-HY-uh | /ˌzɛr.əˈhaɪ.ə/ | 1 Chronicles 6:6 |  | suggestion waiting (0.75) |
| Amariah | am-a-REYE-uh | /ˌæm.əˈraɪ.ə/ | 1 Chronicles 6:7 | ✅ | overridden (0.83) |
| Jehozadak | juh-HOZ-uh-dak | /dʒəˈhɒz.ə.dæk/ | 1 Chronicles 6:14 |  | fine as spelled (0.95) |
| Zimmah | ZIM-uh | /ˈzɪm.ə/ | 1 Chronicles 6:20 |  | fine as spelled (1.00) |
| Jeaterai | jee-AT-uh-ry | /dʒiːˈæt.ə.raɪ/ | 1 Chronicles 6:21 |  | suggestion waiting (0.71) |
| Jeatherai | jaathuhreye | /dʒəˈæθ.ə.raɪ/ | 1 Chronicles 6:21 | ✅ | overridden (0.86) |
| Ebiasaph | uh-BY-uh-saf | /əˈbaɪ.ə.sæf/ | 1 Chronicles 6:23 | ✅ | overridden (1.00) |
| Uriel | yoorriehl | /ˈjʊər.i.ɛl/ | 1 Chronicles 6:24 | ✅ | overridden (0.83) |
| Ahimoth | uh-HEYE-moth | /əˈhaɪ.mɒθ/ | 1 Chronicles 6:25 | ✅ | overridden (1.00) |
| Amasai | uh-MAS-eye | /əˈmæs.aɪ/ | 1 Chronicles 6:25 | ✅ | overridden (0.80) |
| Zophai | ZOH-fy | /ˈzoʊ.faɪ/ | 1 Chronicles 6:26 |  | fine as spelled (1.00) |
| Vashni | VASH-ny | /ˈvæʃ.naɪ/ | 1 Chronicles 6:28 |  | fine as spelled (0.80) |
| Haggiah | huh-GY-uh | /həˈɡaɪ.ə/ | 1 Chronicles 6:30 |  | fine as spelled (0.86) |
| Toah | TOH-uh | /ˈtoʊ.ə/ | 1 Chronicles 6:34 |  | fine as spelled (1.00) |
| Mahath | MAY-hath | /ˈmeɪ.hæθ/ | 1 Chronicles 6:35 | ✅ | overridden (0.80) |
| Berachiah | behr-uh-KEYE-uh | /ˌbɛr.əˈkaɪ.ə/ | 1 Chronicles 6:39 | ✅ | overridden (1.00) |
| Baaseiah | bay-uh-SEE-yuh | /ˌbeɪ.əˈsiː.jə/ | 1 Chronicles 6:40 |  | suggestion waiting (0.71) |
| Malchiah | mal-KY-uh | /mælˈkaɪ.ə/ | 1 Chronicles 6:40 |  | fine as spelled (0.92) |
| Malchijah | mal-KEYE-juh | /mælˈkaɪ.dʒə/ | 1 Chronicles 6:40 | ✅ | overridden (0.86) |
| Ethni | ehthneye | /ˈɛθ.naɪ/ | 1 Chronicles 6:41 | ✅ | overridden (0.88) |
| Abdi | abdeye | /ˈæb.daɪ/ | 1 Chronicles 6:44 | ✅ | overridden (1.00) |
| Kishi | KIHSH-eye | /ˈkɪʃ.aɪ/ | 1 Chronicles 6:44 | ✅ | overridden (1.00) |
| Malluch | MAL-uhk | /ˈmæl.ək/ | 1 Chronicles 6:44 |  | fine as spelled (0.80) |
| Hashabiah | hash-uh-BY-uh | /ˌhæʃ.əˈbaɪ.ə/ | 1 Chronicles 6:45 |  | fine as spelled (0.86) |
| Amzi | AM-zy | /ˈæm.zaɪ/ | 1 Chronicles 6:46 |  | still wrong (0.62) |
| Shamer | SHAY-mer | /ˈʃeɪ.mər/ | 1 Chronicles 6:46 |  | fine as spelled (1.00) |
| Hilen | HY-len | /ˈhaɪ.lɛn/ | 1 Chronicles 6:58 |  | suggestion waiting (0.73) |
| Beth-shemesh | beth-SHEM-esh | /bɛθˈʃɛm.ɛʃ/ | 1 Chronicles 6:59 |  | fine as spelled (0.94) |
| Allemeth | AL-uh-meth | /ˈæl.ə.mɛθ/ | 1 Chronicles 6:60 |  | fine as spelled (1.00) |
| Beth-horon | beth-HOR-on | /bɛθˈhɔːr.ɒn/ | 1 Chronicles 6:68 |  | fine as spelled (0.88) |
| Gath-rimmon | gath-RIM-on | /ɡæθˈrɪm.ɒn/ | 1 Chronicles 6:69 |  | still wrong (0.65) |
| Bileam | billeeuhm | /ˈbɪl.i.əm/ | 1 Chronicles 6:70 | ✅ | overridden (1.00) |
| Anem | AY-nem | /ˈeɪ.nɛm/ | 1 Chronicles 6:73 |  | still wrong (0.50) |
| Mashal | MAY-shal | /ˈmeɪ.ʃæl/ | 1 Chronicles 6:74 |  | suggestion waiting (0.70) |
| Hukok | HYOO-kok | /ˈhjuː.kɒk/ | 1 Chronicles 6:75 |  | suggestion waiting (0.75) |
| Kirjathaim | kur-juh-THAY-im | /ˌkɜːr.dʒəˈθeɪ.ɪm/ | 1 Chronicles 6:76 |  | still wrong (0.56) |
| Rimmono | rih-MOH-noh | /rɪˈmoʊ.noʊ/ | 1 Chronicles 6:77 |  | suggestion waiting (0.70) |
| Jahzah | JAH-zuh | /ˈdʒɑː.zə/ | 1 Chronicles 6:78 |  | fine as spelled (1.00) |
| Shimrom | SHIM-rom | /ˈʃɪm.rɒm/ | 1 Chronicles 7:1 |  | fine as spelled (0.83) |
| Ibsam | IB-sam | /ˈɪb.sæm/ | 1 Chronicles 7:2 |  | fine as spelled (0.80) |
| Jahmai | JAH-my | /ˈdʒɑː.maɪ/ | 1 Chronicles 7:2 |  | fine as spelled (1.00) |
| Jeriel | jeerreeehl | /ˈdʒɪər.i.ɛl/ | 1 Chronicles 7:2 | ✅ | overridden (0.83) |
| Jibsam | JIHB-samm | /ˈdʒɪb.sæm/ | 1 Chronicles 7:2 | ✅ | overridden (1.00) |
| Ishiah | ih-SHY-uh | /ɪˈʃaɪ.ə/ | 1 Chronicles 7:3 |  | still wrong (0.75) |
| Isshiah | ih-SHY-uh | /ɪˈʃaɪ.ə/ | 1 Chronicles 7:3 |  | still wrong (0.75) |
| Izrahiah | iz-ruh-HY-uh | /ˌɪz.rəˈhaɪ.ə/ | 1 Chronicles 7:3 |  | fine as spelled (0.81) |
| Jediael | juh-DY-ay-el | /dʒəˈdaɪ.eɪ.ɛl/ | 1 Chronicles 7:6 |  | still wrong (0.36) |
| Iri | EYE-ry | /ˈaɪ.raɪ/ | 1 Chronicles 7:7 |  | still wrong (0.75) |
| Jerimoth | JER-ih-moth | /ˈdʒɛr.ɪ.mɒθ/ | 1 Chronicles 7:7 |  | fine as spelled (0.86) |
| Alameth | AL-uh-meth | /ˈæl.ə.mɛθ/ | 1 Chronicles 7:8 |  | fine as spelled (0.83) |
| Alemeth | AL-uh-mehth | /ˈæl.ə.mɛθ/ | 1 Chronicles 7:8 | ✅ | overridden (0.92) |
| Jeremoth | JER-uh-moth | /ˈdʒɛr.ə.mɒθ/ | 1 Chronicles 7:8 |  | suggestion waiting (0.79) |
| Zemirah | zuh-MY-ruh | /zəˈmaɪ.rə/ | 1 Chronicles 7:8 |  | fine as spelled (0.83) |
| Ahishahar | uh-HISH-uh-har | /əˈhɪʃ.ə.hɑːr/ | 1 Chronicles 7:10 |  | fine as spelled (1.00) |
| Tharshish | THAR-shish | /ˈθɑːr.ʃɪʃ/ | 1 Chronicles 7:10 |  | fine as spelled (0.92) |
| Zethan | ZEE-thann | /ˈziː.θæn/ | 1 Chronicles 7:10 | ✅ | overridden (0.80) |
| Aher | AY-hur | /ˈeɪ.hər/ | 1 Chronicles 7:12 |  | still wrong (0.55) |
| Shuppim | SHUP-im | /ˈʃʌp.ɪm/ | 1 Chronicles 7:12 |  | fine as spelled (0.80) |
| Jahziel | JAH-zee-el | /ˈdʒɑː.zi.ɛl/ | 1 Chronicles 7:13 |  | suggestion waiting (0.75) |
| Aramitess | AIR-uhm-ite-ess | /ˈɛər.əm.aɪ.tɛs/ | 1 Chronicles 7:14 |  | suggestion waiting (0.75) |
| Peresh | PEE-resh | /ˈpiː.rɛʃ/ | 1 Chronicles 7:16 |  | fine as spelled (0.80) |
| Rakem | RAY-kem | /ˈreɪ.kɛm/ | 1 Chronicles 7:16 |  | fine as spelled (0.80) |
| Sheresh | SHEE-resh | /ˈʃiː.rɛʃ/ | 1 Chronicles 7:16 |  | fine as spelled (0.80) |
| Ulam | YOO-lam | /ˈjuː.læm/ | 1 Chronicles 7:16 |  | fine as spelled (1.00) |
| Hammolecheth | ha-MOL-uh-keth | /hæˈmɒl.ə.kɛθ/ | 1 Chronicles 7:18 |  | still wrong (0.61) |
| Hammoleketh | huh-MOL-ih-keth | /həˈmɒl.ɪ.kɛθ/ | 1 Chronicles 7:18 |  | still wrong (0.61) |
| Ishhod | ISH-hod | /ˈɪʃ.hɒd/ | 1 Chronicles 7:18 |  | fine as spelled (0.80) |
| Ishod | EYE-shod | /ˈaɪ.ʃɒd/ | 1 Chronicles 7:18 | ✅ | overridden (0.88) |
| Mahalah | MAH-uh-luh | /ˈmæh.ə.lə/ | 1 Chronicles 7:18 |  | still wrong (0.58) |
| Ahian | uh-HEYE-uhn | /əˈhaɪ.ən/ | 1 Chronicles 7:19 | ✅ | overridden (0.80) |
| Aniam | uh-NEYE-uhm | /əˈnaɪ.əm/ | 1 Chronicles 7:19 | ✅ | overridden (0.80) |
| Likhi | LIK-heye | /ˈlɪk.haɪ/ | 1 Chronicles 7:19 | ✅ | overridden (0.90) |
| Shemidah | shih-MY-duh | /ʃɪˈmaɪ.də/ | 1 Chronicles 7:19 | ✅ | overridden (0.83) |
| Eladah | EL-uh-duh | /ˈɛl.ə.də/ | 1 Chronicles 7:20 | ✅ | overridden (0.90) |
| Eleadah | el-ee-AY-duh | /ˌɛl.iˈeɪ.də/ | 1 Chronicles 7:20 |  | still wrong (0.58) |
| Elead | ellyad | /ˈɛl.i.æd/ | 1 Chronicles 7:21 | ✅ | overridden (1.00) |
| Sheerah | SHEE-uh-ruh | /ˈʃiː.ə.rə/ | 1 Chronicles 7:24 |  | fine as spelled (0.80) |
| Sherah | SHEER-uh | /ˈʃɪər.ə/ | 1 Chronicles 7:24 |  | fine as spelled (0.88) |
| Uzzen | UZ-en | /ˈʌz.ɛn/ | 1 Chronicles 7:24 |  | still wrong (0.75) |
| Uzzen-sherah | uz-en-SHEER-uh | /ˌʌz.ɛnˈʃɪər.ə/ | 1 Chronicles 7:24 |  | still wrong (0.62) |
| Rephah | REE-fuh | /ˈriː.fə/ | 1 Chronicles 7:25 |  | fine as spelled (0.90) |
| Resheph | REE-shef | /ˈriː.ʃɛf/ | 1 Chronicles 7:25 |  | fine as spelled (1.00) |
| Telah | TEE-luh | /ˈtiː.lə/ | 1 Chronicles 7:25 |  | still wrong (0.75) |
| Ladan | LAY-dan | /ˈleɪ.dæn/ | 1 Chronicles 7:26 |  | fine as spelled (0.80) |
| Jehoshuah | jih-HOSH-oo-uh | /dʒɪˈhɒʃ.u.ə/ | 1 Chronicles 7:27 |  | fine as spelled (0.80) |
| Azzah | AZ-uh | /ˈæz.ə/ | 1 Chronicles 7:28 |  | fine as spelled (1.00) |
| Naaran | NAY-uh-ran | /ˈneɪ.ə.ræn/ | 1 Chronicles 7:28 | ✅ | overridden (0.83) |
| Beth-shean | beth-SHEE-un | /bɛθˈʃiː.ən/ | 1 Chronicles 7:29 |  | suggestion waiting (0.79) |
| Ishuai | ISH-yoo-eye | /ˈɪʃ.ju.aɪ/ | 1 Chronicles 7:30 |  | still wrong (0.60) |
| Isuah | IS-yoo-uh | /ˈɪs.ju.ə/ | 1 Chronicles 7:30 |  | still wrong (0.40) |
| Birzaith | bur-ZAY-ith | /bərˈzeɪ.ɪθ/ | 1 Chronicles 7:31 |  | suggestion waiting (0.71) |
| Birzavith | BUR-zuh-vith | /ˈbɜːr.zə.vɪθ/ | 1 Chronicles 7:31 |  | fine as spelled (0.81) |
| Hotham | HOH-thuhm | /ˈhoʊ.θəm/ | 1 Chronicles 7:32 |  | fine as spelled (0.80) |
| Japhlet | JAF-let | /ˈdʒæf.lɛt/ | 1 Chronicles 7:32 |  | suggestion waiting (0.75) |
| Ashvath | ASH-vath | /ˈæʃ.væθ/ | 1 Chronicles 7:33 |  | suggestion waiting (0.70) |
| Bimhal | BIM-hal | /ˈbɪm.hæl/ | 1 Chronicles 7:33 |  | fine as spelled (0.83) |
| Pasach | PAY-sak | /ˈpeɪ.sæk/ | 1 Chronicles 7:33 | ✅ | overridden (1.00) |
| Jehubbah | juh-HUB-uh | /dʒəˈhʌb.ə/ | 1 Chronicles 7:34 |  | fine as spelled (0.83) |
| Rohgah | ROH-guh | /ˈroʊ.ɡə/ | 1 Chronicles 7:34 |  | fine as spelled (1.00) |
| Amal | AY-mal | /ˈeɪ.mæl/ | 1 Chronicles 7:35 |  | still wrong (0.38) |
| Helem | HEE-lem | /ˈhiː.lɛm/ | 1 Chronicles 7:35 | ✅ | overridden (1.00) |
| Imna | IM-nuh | /ˈɪm.nə/ | 1 Chronicles 7:35 |  | fine as spelled (1.00) |
| Shelesh | SHEE-lesh | /ˈʃiː.lɛʃ/ | 1 Chronicles 7:35 |  | fine as spelled (0.80) |
| Zophah | ZOH-fuh | /ˈzoʊ.fə/ | 1 Chronicles 7:35 |  | fine as spelled (0.80) |
| Beri | BEER-eye | /ˈbɪər.aɪ/ | 1 Chronicles 7:36 |  | still wrong (0.38) |
| Harnepher | har-NEE-fer | /hɑːrˈniː.fər/ | 1 Chronicles 7:36 |  | fine as spelled (0.88) |
| Imrah | IM-ruh | /ˈɪm.rə/ | 1 Chronicles 7:36 |  | fine as spelled (1.00) |
| Suah | SOO-uh | /ˈsuː.ə/ | 1 Chronicles 7:36 |  | fine as spelled (0.88) |
| Beera | bee-EE-ruh | /biˈɪər.ə/ | 1 Chronicles 7:37 |  | fine as spelled (0.80) |
| Hod | HOD | /hɒd/ | 1 Chronicles 7:37 |  | fine as spelled (1.00) |
| Shamma | SHAM-uh | /ˈʃæm.ə/ | 1 Chronicles 7:37 |  | still wrong (0.75) |
| Shilshah | SHIL-shuh | /ˈʃɪl.ʃə/ | 1 Chronicles 7:37 |  | fine as spelled (1.00) |
| Ara | AIR-uh | /ˈɛər.ə/ | 1 Chronicles 7:38 |  | fine as spelled (0.83) |
| Pispa | PIS-puh | /ˈpɪs.pə/ | 1 Chronicles 7:38 |  | fine as spelled (0.83) |
| Pispah | PIS-puh | /ˈpɪs.pə/ | 1 Chronicles 7:38 |  | fine as spelled (0.92) |
| Arah | AY-ruh | /ˈeɪ.rə/ | 1 Chronicles 7:39 |  | still wrong (0.67) |
| Haniel | HAN-ee-el | /ˈhæn.i.ɛl/ | 1 Chronicles 7:39 |  | still wrong (0.54) |
| Rezia | rih-ZY-uh | /rɪˈzaɪ.ə/ | 1 Chronicles 7:39 |  | fine as spelled (0.80) |
| Rizia | rih-ZY-uh | /rɪˈzaɪ.ə/ | 1 Chronicles 7:39 |  | fine as spelled (0.80) |
| Ulla | uhla | /ˈʌl.ə/ | 1 Chronicles 7:39 | ✅ | overridden (1.00) |
| Aharah | uh-HAIR-uh | /əˈhɛər.ə/ | 1 Chronicles 8:1 |  | fine as spelled (0.80) |
| Nohah | NOH-huh | /ˈnoʊ.hə/ | 1 Chronicles 8:2 |  | suggestion waiting (0.75) |
| Abihud | uh-BY-huhd | /əˈbaɪ.hʌd/ | 1 Chronicles 8:3 | ✅ | overridden (1.00) |
| Ahoah | uh-HOH-uh | /əˈhoʊ.ə/ | 1 Chronicles 8:4 |  | still wrong (0.70) |
| Huram | HYOOR-uhm | /ˈhjʊər.əm/ | 1 Chronicles 8:5 |  | still wrong (0.67) |
| Shephuphan | shuh-FYOO-fan | /ʃəˈfjuː.fæn/ | 1 Chronicles 8:5 |  | still wrong (0.38) |
| Ahiah | uh-HY-uh | /əˈhaɪ.ə/ | 1 Chronicles 8:7 |  | suggestion waiting (0.73) |
| Baara | BAY-a-ruh | /ˈbeɪ.ə.rə/ | 1 Chronicles 8:8 | ✅ | overridden (0.80) |
| Shaharaim | shay-huh-RAY-im | /ˌʃeɪ.həˈreɪ.ɪm/ | 1 Chronicles 8:8 |  | suggestion waiting (0.75) |
| Hodesh | HOH-desh | /ˈhoʊ.dɛʃ/ | 1 Chronicles 8:9 |  | fine as spelled (1.00) |
| Malcam | MAL-kam | /ˈmæl.kæm/ | 1 Chronicles 8:9 |  | fine as spelled (0.83) |
| Malcham | MAL-kam | /ˈmæl.kæm/ | 1 Chronicles 8:9 |  | fine as spelled (0.83) |
| Zibia | ZIB-ee-uh | /ˈzɪb.i.ə/ | 1 Chronicles 8:9 |  | fine as spelled (1.00) |
| Jeuz | JEE-uhz | /ˈdʒiː.ʌz/ | 1 Chronicles 8:10 | ✅ | overridden (1.00) |
| Mirma | MUR-muh | /ˈmɜːr.mə/ | 1 Chronicles 8:10 |  | fine as spelled (0.80) |
| Mirmah | MUR-muh | /ˈmɜːr.mə/ | 1 Chronicles 8:10 |  | fine as spelled (0.80) |
| Shachia | shuh-KEYE-uh | /ʃəˈkaɪ.ə/ | 1 Chronicles 8:10 | ✅ | overridden (0.80) |
| Abitub | uh-BY-tuhb | /əˈbaɪ.tʌb/ | 1 Chronicles 8:11 | ✅ | overridden (0.92) |
| Elpaal | el-PAY-uhl | /ɛlˈpeɪ.əl/ | 1 Chronicles 8:11 |  | suggestion waiting (0.75) |
| Lod | LOD | /lɒd/ | 1 Chronicles 8:12 |  | fine as spelled (1.00) |
| Misham | meyeshuhm | /ˈmaɪ.ʃəm/ | 1 Chronicles 8:12 | ✅ | overridden (1.00) |
| Ono | OH-noh | /ˈoʊ.noʊ/ | 1 Chronicles 8:12 |  | fine as spelled (0.83) |
| Shamed | SHAY-med | /ˈʃeɪ.mɛd/ | 1 Chronicles 8:12 |  | fine as spelled (0.80) |
| Shemed | SHEE-mehd | /ˈʃiː.mɛd/ | 1 Chronicles 8:12 | ✅ | overridden (1.00) |
| Shashak | SHAY-shak | /ˈʃeɪ.ʃæk/ | 1 Chronicles 8:14 | ✅ | overridden (1.00) |
| Ader | AY-der | /ˈeɪ.dər/ | 1 Chronicles 8:15 |  | fine as spelled (0.90) |
| Zebadiah | zeb-uh-DY-uh | /ˌzɛb.əˈdaɪ.ə/ | 1 Chronicles 8:15 |  | fine as spelled (0.80) |
| Ishpah | ISH-puh | /ˈɪʃ.pə/ | 1 Chronicles 8:16 |  | fine as spelled (0.88) |
| Ispah | IS-puh | /ˈɪs.pə/ | 1 Chronicles 8:16 |  | fine as spelled (0.90) |
| Joha | JOH-huh | /ˈdʒoʊ.hə/ | 1 Chronicles 8:16 |  | fine as spelled (0.88) |
| Hezeki | hehzihkeye | /ˈhɛz.ɪ.kaɪ/ | 1 Chronicles 8:17 | ✅ | overridden (1.00) |
| Hizki | HIZ-keye | /ˈhɪz.kaɪ/ | 1 Chronicles 8:17 | ✅ | overridden (1.00) |
| Ishmerai | ISH-muh-ry | /ˈɪʃ.mə.raɪ/ | 1 Chronicles 8:18 |  | fine as spelled (1.00) |
| Izliah | iz-LY-uh | /ɪzˈlaɪ.ə/ | 1 Chronicles 8:18 |  | fine as spelled (0.80) |
| Jezliah | jez-LY-uh | /dʒɛzˈlaɪ.ə/ | 1 Chronicles 8:18 |  | still wrong (0.75) |
| Jakim | JAY-kim | /ˈdʒeɪ.kɪm/ | 1 Chronicles 8:19 |  | suggestion waiting (0.70) |
| Elienai | el-ee-EE-ny | /ˌɛl.iˈiː.naɪ/ | 1 Chronicles 8:20 |  | fine as spelled (0.83) |
| Zillethai | ZIL-uh-thy | /ˈzɪl.ə.θaɪ/ | 1 Chronicles 8:20 |  | still wrong (0.67) |
| Zilthai | ZIL-thy | /ˈzɪl.θaɪ/ | 1 Chronicles 8:20 |  | fine as spelled (0.80) |
| Beraiah | buh-RAY-yuh | /bəˈreɪ.jə/ | 1 Chronicles 8:21 |  | still wrong (0.67) |
| Shimhi | SHIM-heye | /ˈʃɪm.haɪ/ | 1 Chronicles 8:21 | ✅ | overridden (1.00) |
| Shimrath | SHIM-rath | /ˈʃɪm.ræθ/ | 1 Chronicles 8:21 |  | fine as spelled (0.86) |
| Ishpan | ISH-pan | /ˈɪʃ.pæn/ | 1 Chronicles 8:22 |  | fine as spelled (0.80) |
| Anthothijah | an-thoh-THY-juh | /ˌæn.θoʊˈθaɪ.dʒə/ | 1 Chronicles 8:24 |  | still wrong (0.59) |
| Antothijah | an-toh-THY-juh | /ˌæn.toʊˈθaɪ.dʒə/ | 1 Chronicles 8:24 |  | still wrong (0.75) |
| Iphdeiah | if-DEE-yuh | /ɪfˈdiː.jə/ | 1 Chronicles 8:25 |  | fine as spelled (0.83) |
| Iphedeiah | if-ih-DEE-uh | /ˌɪf.ɪˈdiː.ə/ | 1 Chronicles 8:25 |  | suggestion waiting (0.77) |
| Shamsherai | SHAM-shuh-ry | /ˈʃæm.ʃə.raɪ/ | 1 Chronicles 8:26 |  | fine as spelled (0.94) |
| Shehariah | shee-huh-REYE-uh | /ˌʃiː.həˈraɪ.ə/ | 1 Chronicles 8:26 | ✅ | overridden (0.93) |
| Eliah | ih-LY-uh | /ɪˈlaɪ.ə/ | 1 Chronicles 8:27 |  | fine as spelled (0.80) |
| Jaareshiah | jay-uh-ruh-SHY-uh | /ˌdʒeɪ.ə.rəˈʃaɪ.ə/ | 1 Chronicles 8:27 |  | still wrong (0.56) |
| Jaresiah | jar-ih-SY-uh | /ˌdʒær.ɪˈsaɪ.ə/ | 1 Chronicles 8:27 |  | still wrong (0.79) |
| Zacher | ZAY-ker | /ˈzeɪ.kər/ | 1 Chronicles 8:31 |  | fine as spelled (0.80) |
| Zecher | ZEE-ker | /ˈziː.kər/ | 1 Chronicles 8:31 |  | fine as spelled (0.80) |
| Mikloth | MIK-loth | /ˈmɪk.lɒθ/ | 1 Chronicles 8:32 |  | fine as spelled (0.83) |
| Esh-baal | eshbayuhl | /ɛʃˈbeɪ.əl/ | 1 Chronicles 8:33 | ✅ | overridden (0.92) |
| Eshbaal | eshbayuhl | /ɛʃˈbeɪ.əl/ | 1 Chronicles 8:33 | ✅ | overridden (0.92) |
| Malchi-shua | mal-keye-SHOO-uh | /ˌmæl.kaɪˈʃuː.ə/ | 1 Chronicles 8:33 | ✅ | overridden (0.83) |
| Merib | MER-ib | /ˈmɛr.ɪb/ | 1 Chronicles 8:34 |  | fine as spelled (0.90) |
| Merib-baal | mehr-ihb-BAY-uhll | /ˌmɛr.ɪbˈbeɪ.əl/ | 1 Chronicles 8:34 | ✅ | overridden (0.88) |
| Pithon | peyethon | /ˈpaɪ.θɒn/ | 1 Chronicles 8:35 | ✅ | overridden (1.00) |
| Tarea | tuh-REE-uh | /təˈriː.ə/ | 1 Chronicles 8:35 |  | suggestion waiting (0.70) |
| Jehoadah | jih-HOH-uh-duh | /dʒɪˈhoʊ.ə.də/ | 1 Chronicles 8:36 |  | still wrong (0.71) |
| Jehoaddah | juh-HOH-ad-uh | /dʒəˈhoʊ.æd.ə/ | 1 Chronicles 8:36 |  | fine as spelled (0.86) |
| Azel | AY-zel | /ˈeɪ.zəl/ | 1 Chronicles 8:37 |  | fine as spelled (1.00) |
| Binea | BIN-ee-uh | /ˈbɪn.i.ə/ | 1 Chronicles 8:37 |  | fine as spelled (1.00) |
| Raphah | RAY-fuh | /ˈreɪ.fə/ | 1 Chronicles 8:37 |  | fine as spelled (0.90) |
| Bocheru | BOK-uh-roo | /ˈbɒk.ə.ruː/ | 1 Chronicles 8:38 |  | fine as spelled (0.83) |
| Sheariah | shee-uh-RY-uh | /ˌʃiː.əˈraɪ.ə/ | 1 Chronicles 8:38 |  | fine as spelled (0.92) |
| Eshek | EE-shek | /ˈiː.ʃɛk/ | 1 Chronicles 8:39 |  | suggestion waiting (0.75) |
| Jehush | JEE-hush | /ˈdʒiː.hʌʃ/ | 1 Chronicles 8:39 |  | fine as spelled (0.90) |
| Nethinims | NETH-ih-nimz | /ˈnɛθ.ɪ.nɪmz/ | 1 Chronicles 9:2 |  | fine as spelled (0.88) |
| Imri | IM-ry | /ˈɪm.raɪ/ | 1 Chronicles 9:4 |  | suggestion waiting (0.75) |
| Uthai | yootheye | /ˈjuː.θaɪ/ | 1 Chronicles 9:4 | ✅ | overridden (0.88) |
| Shilonites | SHY-luh-nites | /ˈʃaɪ.lə.naɪts/ | 1 Chronicles 9:5 |  | suggestion waiting (0.75) |
| Jeuel | juh-YOO-el | /dʒəˈjuː.əl/ | 1 Chronicles 9:6 |  | still wrong (0.67) |
| Hasenuah | has-ih-NYOO-uh | /ˌhæs.ɪˈnjuː.ə/ | 1 Chronicles 9:7 |  | still wrong (0.50) |
| Hassenuah | has-uh-NOO-uh | /ˌhæs.əˈnuː.ə/ | 1 Chronicles 9:7 |  | fine as spelled (0.94) |
| Sallu | SAL-oo | /ˈsæl.uː/ | 1 Chronicles 9:7 |  | fine as spelled (0.88) |
| Ibneiah | ihbneeyuh | /ɪbˈniː.jə/ | 1 Chronicles 9:8 | ✅ | overridden (0.83) |
| Ibnijah | ib-NY-juh | /ɪbˈnaɪ.dʒə/ | 1 Chronicles 9:8 |  | fine as spelled (0.83) |
| Michri | MIK-reye | /ˈmɪk.raɪ/ | 1 Chronicles 9:8 | ✅ | overridden (1.00) |
| Jehoiarib | juh-HOY-uh-rib | /dʒəˈhɔɪ.ə.rɪb/ | 1 Chronicles 9:10 |  | still wrong (0.75) |
| Immer | IM-er | /ˈɪm.ər/ | 1 Chronicles 9:12 |  | fine as spelled (1.00) |
| Jahzerah | JAH-zuh-ruh | /ˈdʒɑː.zə.rə/ | 1 Chronicles 9:12 |  | fine as spelled (0.92) |
| Maasai | MAY-uh-sy | /ˈmeɪ.ə.saɪ/ | 1 Chronicles 9:12 |  | still wrong (0.60) |
| Maasiai | maayseeeye | /məˈeɪ.si.aɪ/ | 1 Chronicles 9:12 | ✅ | overridden (0.83) |
| Meshillemith | muh-SHIL-uh-mith | /məˈʃɪl.ə.mɪθ/ | 1 Chronicles 9:12 |  | fine as spelled (0.89) |
| Pashhur | PASH-er | /ˈpæʃ.ər/ | 1 Chronicles 9:12 |  | fine as spelled (0.86) |
| Pashur | PASH-ur | /ˈpæʃ.ər/ | 1 Chronicles 9:12 |  | fine as spelled (1.00) |
| Hasshub | hashuhb | /ˈhæʃ.əb/ | 1 Chronicles 9:14 | ✅ | overridden (1.00) |
| Bakbakkar | bak-BAK-er | /bækˈbæk.ər/ | 1 Chronicles 9:15 |  | fine as spelled (1.00) |
| Galal | GAY-lal | /ˈɡeɪ.læl/ | 1 Chronicles 9:15 |  | suggestion waiting (0.70) |
| Heresh | HEE-resh | /ˈhiː.rɛʃ/ | 1 Chronicles 9:15 |  | fine as spelled (0.80) |
| Jeduthun | juh-DYOO-thuhn | /dʒəˈdjuː.θən/ | 1 Chronicles 9:16 |  | still wrong (0.69) |
| Talmon | TAL-muhn | /ˈtæl.mən/ | 1 Chronicles 9:17 |  | fine as spelled (0.83) |
| Kore | KOR-ee | /ˈkɔːr.i/ | 1 Chronicles 9:19 |  | still wrong (0.50) |
| Meshelemiah | muh-shel-uh-MY-uh | /məˌʃɛl.əˈmaɪ.ə/ | 1 Chronicles 9:21 |  | still wrong (0.56) |
| Korahite | KOR-uh-hite | /ˈkɔːr.ə.haɪt/ | 1 Chronicles 9:31 |  | fine as spelled (0.93) |
| Mattithiah | mat-ih-THY-uh | /ˌmæt.ɪˈθaɪ.ə/ | 1 Chronicles 9:31 |  | still wrong (0.61) |
| Shimeam | SHIM-ee-am | /ˈʃɪm.i.æm/ | 1 Chronicles 9:38 |  | still wrong (0.58) |
| Tahrea | tah-REE-uh | /tɑːˈriː.ə/ | 1 Chronicles 9:41 |  | fine as spelled (1.00) |
| Jarah | JAIR-uh | /ˈdʒɛər.ə/ | 1 Chronicles 9:42 |  | fine as spelled (1.00) |
| Gilboa | gil-BOH-uh | /ɡɪlˈboʊ.ə/ | 1 Chronicles 10:1 |  | fine as spelled (0.92) |
| Dagon | DAY-gon | /ˈdeɪ.ɡɒn/ | 1 Chronicles 10:10 |  | fine as spelled (1.00) |
| Jabesh | JAY-besh | /ˈdʒeɪ.bɛʃ/ | 1 Chronicles 10:11 |  | fine as spelled (0.80) |
| Jabesh-gilead | jay-besh-GIL-ee-ud | /ˌdʒeɪ.bɛʃˈɡɪl.i.əd/ | 1 Chronicles 10:11 |  | fine as spelled (0.86) |
| Jebus | JEE-buhs | /ˈdʒiː.bəs/ | 1 Chronicles 11:4 |  | fine as spelled (0.90) |
| Jebusites | JEB-yoo-sites | /ˈdʒɛb.jʊ.saɪts/ | 1 Chronicles 11:4 |  | fine as spelled (1.00) |
| Zion | ZY-uhn | /ˈzaɪ.ən/ | 1 Chronicles 11:5 |  | fine as spelled (0.88) |
| Millo | MIL-oh | /ˈmɪl.oʊ/ | 1 Chronicles 11:8 |  | fine as spelled (1.00) |
| Hachmonite | HAK-moh-nite | /ˈhæk.mə.naɪt/ | 1 Chronicles 11:11 |  | fine as spelled (0.94) |
| Ahohite | uh-HOH-hite | /əˈhoʊ.haɪt/ | 1 Chronicles 11:12 |  | suggestion waiting (0.75) |
| Dodo | DOH-doh | /ˈdoʊ.doʊ/ | 1 Chronicles 11:12 |  | fine as spelled (1.00) |
| Pas-dammim | pas-DAM-im | /pæsˈdæm.ɪm/ | 1 Chronicles 11:13 |  | still wrong (0.44) |
| Pasdammim | pas-DAM-im | /pæsˈdæm.ɪm/ | 1 Chronicles 11:13 |  | still wrong (0.69) |
| Adullam | uh-DUHL-uhm | /əˈdʌl.əm/ | 1 Chronicles 11:15 |  | fine as spelled (1.00) |
| Rephaim | REHF-ay-ihmm | /ˈrɛf.eɪ.ɪm/ | 1 Chronicles 11:15 | ✅ | overridden (0.83) |
| Ariel | AIR-ee-el | /ˈɛər.i.ɛl/ | 1 Chronicles 11:22 |  | fine as spelled (0.80) |
| Jehoiada | juh-HOY-uh-duh | /dʒəˈhɔɪ.ə.də/ | 1 Chronicles 11:22 |  | still wrong (0.67) |
| Kabzeel | KAB-zee-el | /ˈkæb.zi.ɛl/ | 1 Chronicles 11:22 |  | suggestion waiting (0.79) |
| Elhanan | el-HAY-nan | /ɛlˈheɪ.næn/ | 1 Chronicles 11:26 | ✅ | overridden (0.93) |
| Harorite | HAIR-oh-rite | /ˈhɛər.ə.raɪt/ | 1 Chronicles 11:27 |  | fine as spelled (0.86) |
| Pelonite | PEL-oh-nite | /ˈpɛl.ə.naɪt/ | 1 Chronicles 11:27 |  | fine as spelled (0.86) |
| Abi-ezer | aybeyeeezuhr | /ˌeɪ.baɪˈiː.zər/ | 1 Chronicles 11:28 | ✅ | overridden (1.00) |
| Anathothite | AN-uh-thoth-ite | /ˈæn.ə.θɒθ.aɪt/ | 1 Chronicles 11:28 |  | still wrong (0.62) |
| Antothite | AN-tuh-thite | /ˈæn.tə.θaɪt/ | 1 Chronicles 11:28 |  | fine as spelled (0.86) |
| Ikkesh | IK-esh | /ˈɪk.ɛʃ/ | 1 Chronicles 11:28 |  | fine as spelled (1.00) |
| Tekoite | tuh-KOH-eyett | /təˈkoʊ.aɪt/ | 1 Chronicles 11:28 | ✅ | overridden (0.86) |
| Hushathite | HOO-shuh-thite | /ˈhuː.ʃə.θaɪt/ | 1 Chronicles 11:29 |  | still wrong (0.79) |
| Ilai | eyeleye | /ˈaɪ.laɪ/ | 1 Chronicles 11:29 | ✅ | overridden (1.00) |
| Baanah | BAY-uh-nuh | /ˈbeɪ.ə.nə/ | 1 Chronicles 11:30 | ✅ | overridden (0.80) |
| Heled | HEE-led | /ˈhiː.lɛd/ | 1 Chronicles 11:30 | ✅ | overridden (1.00) |
| Netophathite | nih-TOF-uh-thite | /nɪˈtɒf.ə.θaɪt/ | 1 Chronicles 11:30 |  | fine as spelled (0.83) |
| Gibeah | GIB-ee-uh | /ˈɡɪb.i.ə/ | 1 Chronicles 11:31 |  | fine as spelled (1.00) |
| Pirathonite | pih-RATH-oh-nite | /pɪˈræθ.ə.naɪt/ | 1 Chronicles 11:31 |  | fine as spelled (0.83) |
| Ribai | RY-by | /ˈraɪ.baɪ/ | 1 Chronicles 11:31 |  | suggestion waiting (0.75) |
| Abiel | aybiehl | /ˈeɪ.bi.ɛl/ | 1 Chronicles 11:32 | ✅ | overridden (0.80) |
| Arbathite | AR-buh-thite | /ˈɑːr.bə.θaɪt/ | 1 Chronicles 11:32 |  | fine as spelled (1.00) |
| Gaash | GAY-ash | /ˈɡeɪ.æʃ/ | 1 Chronicles 11:32 |  | suggestion waiting (0.75) |
| Baharumite | buh-HAY-rum-ite | /bəˈheɪ.rə.maɪt/ | 1 Chronicles 11:33 |  | fine as spelled (0.89) |
| Eliahba | ih-LY-ah-buh | /ɪˈlaɪ.ə.bə/ | 1 Chronicles 11:33 |  | still wrong (0.77) |
| Shaalbonite | shay-al-BOH-nite | /ˌʃeɪ.ælˈboʊ.naɪt/ | 1 Chronicles 11:33 |  | still wrong (0.72) |
| Gizonite | GY-zoh-nite | /ˈɡaɪ.zə.naɪt/ | 1 Chronicles 11:34 |  | fine as spelled (0.86) |
| Hararite | HAIR-uh-rite | /ˈhɛər.ə.raɪt/ | 1 Chronicles 11:34 |  | fine as spelled (0.86) |
| Hashem | HAY-shehm | /ˈheɪ.ʃɛm/ | 1 Chronicles 11:34 | ✅ | overridden (1.00) |
| Shage | SHAY-ghee | /ˈʃeɪ.ɡiː/ | 1 Chronicles 11:34 | ✅ | overridden (1.00) |
| Shagee | SHAY-ghee | /ˈʃeɪ.ɡiː/ | 1 Chronicles 11:34 | ✅ | overridden (1.00) |
| Eliphal | ih-LY-fal | /ɪˈlaɪ.fæl/ | 1 Chronicles 11:35 |  | still wrong (0.50) |
| Sacar | SAY-kahr | /ˈseɪ.kɑːr/ | 1 Chronicles 11:35 | ✅ | overridden (1.00) |
| Mecherathite | muh-KER-uh-thite | /məˈkɛr.ə.θaɪt/ | 1 Chronicles 11:36 |  | suggestion waiting (0.72) |
| Carmelite | KAR-muh-lite | /ˈkɑːr.mə.laɪt/ | 1 Chronicles 11:37 |  | fine as spelled (1.00) |
| Ezbai | EZ-by | /ˈɛz.baɪ/ | 1 Chronicles 11:37 |  | suggestion waiting (0.75) |
| Naarai | NAY-uh-ry | /ˈneɪ.ə.raɪ/ | 1 Chronicles 11:37 |  | fine as spelled (0.80) |
| Haggeri | HAG-uh-ry | /ˈhæɡ.ə.raɪ/ | 1 Chronicles 11:38 |  | fine as spelled (0.83) |
| Hagri | HAG-ry | /ˈhæɡ.raɪ/ | 1 Chronicles 11:38 |  | fine as spelled (0.80) |
| Mibhar | MIB-har | /ˈmɪb.hɑːr/ | 1 Chronicles 11:38 |  | fine as spelled (1.00) |
| Ammonite | AM-uh-nite | /ˈæm.ə.naɪt/ | 1 Chronicles 11:39 |  | fine as spelled (1.00) |
| Berothite | BEE-roh-thite | /ˈbiː.rə.θaɪt/ | 1 Chronicles 11:39 |  | fine as spelled (0.86) |
| Naharai | NAY-huh-ry | /ˈneɪ.hə.raɪ/ | 1 Chronicles 11:39 |  | fine as spelled (0.83) |
| Gareb | GAIR-eb | /ˈɡɛər.ɛb/ | 1 Chronicles 11:40 |  | fine as spelled (0.80) |
| Ithrite | ITH-rite | /ˈɪθ.raɪt/ | 1 Chronicles 11:40 |  | fine as spelled (0.90) |
| Hittite | HIT-tite | /ˈhɪt.aɪt/ | 1 Chronicles 11:41 |  | fine as spelled (1.00) |
| Reubenite | ROO-ben-ite | /ˈruː.bən.aɪt/ | 1 Chronicles 11:42 |  | fine as spelled (0.83) |
| Shiza | SHY-zuh | /ˈʃaɪ.zə/ | 1 Chronicles 11:42 |  | still wrong (0.62) |
| Joshaphat | JOSH-uh-fat | /ˈdʒɒʃ.ə.fæt/ | 1 Chronicles 11:43 |  | fine as spelled (1.00) |
| Mithnite | MITH-nite | /ˈmɪθ.naɪt/ | 1 Chronicles 11:43 |  | fine as spelled (1.00) |
| Aroerite | uh-ROH-er-ite | /əˈroʊ.ər.aɪt/ | 1 Chronicles 11:44 |  | fine as spelled (0.86) |
| Ashterathite | ASH-tuh-rath-ite | /ˈæʃ.tə.ræθ.aɪt/ | 1 Chronicles 11:44 |  | fine as spelled (0.83) |
| Hothan | HOH-than | /ˈhoʊ.θæn/ | 1 Chronicles 11:44 |  | still wrong (0.50) |
| Shama | SHAY-muh | /ˈʃeɪ.mə/ | 1 Chronicles 11:44 |  | suggestion waiting (0.75) |
| Tizite | TY-zite | /ˈtaɪ.zaɪt/ | 1 Chronicles 11:45 |  | suggestion waiting (0.70) |
| Elnaam | el-NAY-am | /ɛlˈneɪ.æm/ | 1 Chronicles 11:46 | ✅ | overridden (0.83) |
| Ithmah | ITH-muh | /ˈɪθ.mə/ | 1 Chronicles 11:46 |  | suggestion waiting (0.75) |
| Jeribai | JER-ih-by | /ˈdʒɛr.ɪ.baɪ/ | 1 Chronicles 11:46 |  | fine as spelled (0.83) |
| Joshaviah | josh-uh-VY-uh | /ˌdʒɒʃ.əˈvaɪ.ə/ | 1 Chronicles 11:46 |  | fine as spelled (0.86) |
| Mahavite | mayhuhveyet | /ˈmeɪ.hə.vaɪt/ | 1 Chronicles 11:46 | ✅ | overridden (0.93) |
| Moabite | MOH-uh-bite | /ˈmoʊ.ə.baɪt/ | 1 Chronicles 11:46 |  | fine as spelled (0.86) |
| Jaasiel | jay-AY-see-el | /dʒeɪˈeɪ.si.ɛl/ | 1 Chronicles 11:47 | ✅ | overridden (0.86) |
| Jasiel | jayseeehl | /ˈdʒeɪ.si.ɛl/ | 1 Chronicles 11:47 | ✅ | overridden (0.83) |
| Mesobaite | misohbayeyet | /mɪˈsoʊ.beɪ.aɪt/ | 1 Chronicles 11:47 | ✅ | overridden (0.88) |
| Mezobaite | muh-ZOH-bay-eyett | /məˈzoʊ.beɪ.aɪt/ | 1 Chronicles 11:47 | ✅ | overridden (0.94) |
| Ahiezer | ay-hy-EE-zer | /ˌeɪ.haɪˈiː.zər/ | 1 Chronicles 12:3 |  | suggestion waiting (0.71) |
| Berachah | BEHR-a-kuh | /ˈbɛr.ə.kə/ | 1 Chronicles 12:3 | ✅ | overridden (0.83) |
| Gibeathite | GIB-ee-uh-thite | /ˈɡɪb.i.ə.θaɪt/ | 1 Chronicles 12:3 |  | fine as spelled (0.81) |
| Jeziel | JEE-zee-el | /ˈdʒiː.zi.ɛl/ | 1 Chronicles 12:3 |  | suggestion waiting (0.75) |
| Shemaah | shuhmayuh | /ʃəˈmeɪ.ə/ | 1 Chronicles 12:3 | ✅ | overridden (0.80) |
| Gederathite | guh-DER-uh-thite | /ɡəˈdɛr.ə.θaɪt/ | 1 Chronicles 12:4 |  | still wrong (0.67) |
| Gibeonite | GIB-ee-uh-nite | /ˈɡɪb.i.ə.naɪt/ | 1 Chronicles 12:4 |  | still wrong (0.69) |
| Ismaiah | iz-MY-uh | /ɪzˈmaɪ.ə/ | 1 Chronicles 12:4 |  | suggestion waiting (0.73) |
| Josabad | JOS-uh-bad | /ˈdʒɒs.ə.bæd/ | 1 Chronicles 12:4 | ✅ | overridden (1.00) |
| Jozabad | JOZ-uh-bad | /ˈdʒɒz.ə.bæd/ | 1 Chronicles 12:4 |  | suggestion waiting (0.79) |
| Bealiah | bee-uh-LY-uh | /ˌbiː.əˈlaɪ.ə/ | 1 Chronicles 12:5 |  | fine as spelled (0.93) |
| Haruphite | huh-ROO-fite | /həˈruː.faɪt/ | 1 Chronicles 12:5 |  | suggestion waiting (0.71) |
| Azareel | uh-ZAR-ee-el | /əˈzær.i.ɛl/ | 1 Chronicles 12:6 |  | still wrong (0.57) |
| Azarel | azuhrehl | /ˈæz.ə.rɛl/ | 1 Chronicles 12:6 | ✅ | overridden (1.00) |
| Jashobeam | juhshohbeeam | /dʒəˈʃoʊ.bi.æm/ | 1 Chronicles 12:6 | ✅ | overridden (0.88) |
| Jesiah | jih-SY-uh | /dʒɪˈsaɪ.ə/ | 1 Chronicles 12:6 |  | still wrong (0.55) |
| Joezer | joh-EE-zer | /dʒoʊˈiː.zər/ | 1 Chronicles 12:6 |  | fine as spelled (0.83) |
| Korhites | KAWR-heyetss | /ˈkɔːr.haɪts/ | 1 Chronicles 12:6 | ✅ | overridden (1.00) |
| Joelah | joh-EE-luh | /dʒoʊˈiː.lə/ | 1 Chronicles 12:7 |  | fine as spelled (1.00) |
| Elzabad | el-ZAY-bad | /ɛlˈzeɪ.bæd/ | 1 Chronicles 12:12 |  | fine as spelled (0.86) |
| Machbanai | MAK-buh-ny | /ˈmæk.bə.naɪ/ | 1 Chronicles 12:13 |  | suggestion waiting (0.71) |
| Machbannai | mak-BAN-eye | /mækˈbæn.aɪ/ | 1 Chronicles 12:13 | ✅ | overridden (0.86) |
| Adnah | AD-nuh | /ˈæd.nə/ | 1 Chronicles 12:20 |  | fine as spelled (1.00) |
| Elihu | ih-LY-hyoo | /ɪˈlaɪ.hjuː/ | 1 Chronicles 12:20 |  | still wrong (0.50) |
| Aaronites | AIR-uh-nites | /ˈɛər.ə.naɪts/ | 1 Chronicles 12:27 |  | fine as spelled (1.00) |
| Danites | DAN-ites | /ˈdæn.aɪts/ | 1 Chronicles 12:35 |  | still wrong (0.57) |
| Egypt | EE-jipt | /ˈiː.dʒɪpt/ | 1 Chronicles 13:5 |  | fine as spelled (1.00) |
| Hamath | HAY-math | /ˈheɪ.mæθ/ | 1 Chronicles 13:5 | ✅ | overridden (1.00) |
| Shihor | SHY-hawr | /ˈʃaɪ.hɔːr/ | 1 Chronicles 13:5 | ✅ | overridden (0.80) |
| Baalah | BAY-uh-la | /ˈbeɪ.ə.lə/ | 1 Chronicles 13:6 | ✅ | overridden (0.90) |
| Chidon | KEYE-don | /ˈkaɪ.dɒn/ | 1 Chronicles 13:9 | ✅ | overridden (1.00) |
| Perez-uzza | per-ez-UZ-uh | /ˌpɛr.ɛzˈʌz.ə/ | 1 Chronicles 13:11 |  | suggestion waiting (0.75) |
| Gittite | GIT-ite | /ˈɡɪt.aɪt/ | 1 Chronicles 13:13 |  | fine as spelled (0.90) |
| Obed-Edom | OH-bed EE-duhm | /ˌoʊ.bɛd ˈiː.dəm/ | 1 Chronicles 13:13 |  | fine as spelled (0.88) |
| Obed-edom | oh-bed-EE-dum | /ˌoʊ.bɛdˈiː.dəm/ | 1 Chronicles 13:13 |  | fine as spelled (0.88) |
| Hiram | HY-rum | /ˈhaɪ.rəm/ | 1 Chronicles 14:1 |  | fine as spelled (1.00) |
| Tyre | TIRE | /taɪər/ | 1 Chronicles 14:1 |  | suggestion waiting (0.75) |
| Elishua | el-ih-SHOO-uh | /ˌɛl.ɪˈʃuː.ə/ | 1 Chronicles 14:5 |  | still wrong (0.75) |
| Elpalet | el-PAY-let | /ɛlˈpeɪ.lɛt/ | 1 Chronicles 14:5 |  | fine as spelled (0.86) |
| Elpelet | el-PEE-leht | /ɛlˈpiː.lɛt/ | 1 Chronicles 14:5 | ✅ | overridden (0.93) |
| Beeliada | bee-uh-LEYE-uh-duhh | /ˌbiː.əˈlaɪ.ə.də/ | 1 Chronicles 14:7 | ✅ | overridden (0.88) |
| Eliphalet | ih-LIF-uh-let | /ɪˈlɪf.ə.lɛt/ | 1 Chronicles 14:7 |  | fine as spelled (0.88) |
| Baal-perazim | bay-uhl-puh-RAY-zihmm | /ˌbeɪ.əl.pəˈreɪ.zɪm/ | 1 Chronicles 14:11 | ✅ | overridden (0.83) |
| Perazim | puh-RAY-zim | /pəˈreɪ.zɪm/ | 1 Chronicles 14:11 |  | still wrong (0.57) |
| Gazer | GAY-zer | /ˈɡeɪ.zər/ | 1 Chronicles 14:16 |  | fine as spelled (1.00) |
| Elizaphan | ih-LIZ-uh-fan | /ɪˈlɪz.ə.fæn/ | 1 Chronicles 15:8 |  | fine as spelled (0.81) |
| Abiathar | uh-BY-uh-thar | /əˈbaɪ.ə.θɑːr/ | 1 Chronicles 15:11 |  | fine as spelled (0.86) |
| Kushaiah | koo-SHY-uh | /kuːˈʃaɪ.ə/ | 1 Chronicles 15:17 |  | suggestion waiting (0.73) |
| Elipheleh | ih-LIF-ih-leh | /ɪˈlɪf.ɪ.lɛ/ | 1 Chronicles 15:18 |  | still wrong (0.57) |
| Eliphelehu | i-lihf-uh-LEE-hoo | /ɪˌlɪf.əˈliː.huː/ | 1 Chronicles 15:18 | ✅ | overridden (0.89) |
| Jaaziel | jay-AY-zee-el | /dʒeɪˈeɪ.zi.ɛl/ | 1 Chronicles 15:18 |  | suggestion waiting (0.64) |
| Jehiel | juh-HY-el | /dʒəˈhaɪ.ɛl/ | 1 Chronicles 15:18 |  | suggestion waiting (0.75) |
| Maaseiah | may-uh-SAY-uhh | /ˌmeɪ.əˈseɪ.ə/ | 1 Chronicles 15:18 | ✅ | overridden (1.00) |
| Mikneiah | mik-NEE-yuh | /mɪkˈniː.ə/ | 1 Chronicles 15:18 |  | fine as spelled (0.93) |
| Shemiramoth | shuh-MEER-uh-moth | /ʃəˈmɪr.ə.mɒθ/ | 1 Chronicles 15:18 |  | fine as spelled (1.00) |
| Unni | UHN-eye | /ˈʌn.aɪ/ | 1 Chronicles 15:18 | ✅ | overridden (1.00) |
| Alamoth | AL-uh-moth | /ˈæl.ə.mɒθ/ | 1 Chronicles 15:20 |  | suggestion waiting (0.75) |
| Aziel | AY-zee-el | /ˈeɪ.zi.ɛl/ | 1 Chronicles 15:20 |  | fine as spelled (0.80) |
| Azaziah | az-uh-ZY-uh | /ˌæz.əˈzaɪ.ə/ | 1 Chronicles 15:21 |  | fine as spelled (0.93) |
| Sheminith | SHEM-ih-nith | /ˈʃɛm.ɪ.nɪθ/ | 1 Chronicles 15:21 |  | fine as spelled (0.86) |
| Chenaniah | ken-uh-NY-uh | /ˌkɛn.əˈnaɪ.ə/ | 1 Chronicles 15:22 |  | still wrong (0.43) |
| Jehiah | juh-HY-uh | /dʒəˈhaɪ.ə/ | 1 Chronicles 15:24 |  | fine as spelled (0.92) |
| Nethaneel | nih-THAN-ee-el | /nɪˈθæn.i.ɛl/ | 1 Chronicles 15:24 |  | still wrong (0.56) |
| Shebaniah | sheb-uh-NY-uh | /ˌʃɛb.əˈnaɪ.ə/ | 1 Chronicles 15:24 |  | fine as spelled (1.00) |
| Michal | MY-kal | /ˈmaɪ.kæl/ | 1 Chronicles 15:29 |  | fine as spelled (0.80) |
| Jahaziel | juh-HAY-zee-ehll | /dʒəˈheɪ.zi.ɛl/ | 1 Chronicles 16:6 | ✅ | overridden (0.88) |
| Jacob | JAY-kub | /ˈdʒeɪ.kəb/ | 1 Chronicles 16:13 |  | fine as spelled (1.00) |
| Hosah | hohsa | /ˈhoʊ.sə/ | 1 Chronicles 16:38 | ✅ | overridden (0.88) |
| Moabites | MOH-uh-bites | /ˈmoʊ.ə.baɪts/ | 1 Chronicles 18:2 |  | fine as spelled (0.81) |
| Hadadezer | had-ad-EE-zer | /ˌhæd.ædˈiː.zər/ | 1 Chronicles 18:3 |  | fine as spelled (0.89) |
| Hadarezer | had-ur-EE-zer | /ˌhæd.ərˈiː.zər/ | 1 Chronicles 18:3 |  | fine as spelled (0.94) |
| Zobah | ZOH-buh | /ˈzoʊ.bə/ | 1 Chronicles 18:3 |  | fine as spelled (1.00) |
| Damascus | duh-MASS-kuhs | /dəˈmæs.kəs/ | 1 Chronicles 18:5 |  | fine as spelled (1.00) |
| Syria | SEER-ee-uh | /ˈsɪr.i.ə/ | 1 Chronicles 18:6 |  | fine as spelled (1.00) |
| Syria-damascus | sir-ee-uh-duh-MAS-kus | /ˌsɪr.i.ə.dəˈmæs.kəs/ | 1 Chronicles 18:6 |  | fine as spelled (0.96) |
| Chun | kuhnn | /kʌn/ | 1 Chronicles 18:8 | ✅ | overridden (1.00) |
| Cun | kuhnn | /kʌn/ | 1 Chronicles 18:8 | ✅ | overridden (1.00) |
| Tibhath | TIB-hath | /ˈtɪb.hæθ/ | 1 Chronicles 18:8 |  | fine as spelled (0.92) |
| Tou | TOH-oo | /ˈtoʊ.uː/ | 1 Chronicles 18:9 |  | still wrong (0.67) |
| Ammon | AM-uhn | /ˈæm.ən/ | 1 Chronicles 18:11 |  | fine as spelled (1.00) |
| Edomites | EE-duhm-ites | /ˈiː.dəm.aɪts/ | 1 Chronicles 18:12 |  | fine as spelled (1.00) |
| Ahilud | uhheyeluhd | /əˈhaɪ.lʌd/ | 1 Chronicles 18:15 | ✅ | overridden (1.00) |
| Abimelech | uh-BIM-eh-lek | /əˈbɪm.ə.lɛk/ | 1 Chronicles 18:16 |  | fine as spelled (1.00) |
| Shavsha | SHAV-shuh | /ˈʃæv.ʃə/ | 1 Chronicles 18:16 |  | still wrong (0.70) |
| Cherethites | KER-eh-thites | /ˈkɛr.ə.θaɪts/ | 1 Chronicles 18:17 |  | fine as spelled (0.81) |
| Pelethites | PEL-eh-thites | /ˈpɛl.ə.θaɪts/ | 1 Chronicles 18:17 |  | still wrong (0.50) |
| Hanun | HAY-nuhn | /ˈheɪ.nən/ | 1 Chronicles 19:2 |  | fine as spelled (0.90) |
| Aram-maacah | AIR-uhm MAY-uh-kuh | /ˌɛər.əm ˈmeɪ.ə.kə/ | 1 Chronicles 19:6 |  | still wrong (0.62) |
| Mesopotamia | mes-uh-puh-TAY-mee-uh | /ˌmɛs.ə.pəˈteɪ.mi.ə/ | 1 Chronicles 19:6 |  | fine as spelled (0.95) |
| Syria-maachah | sir-ee-uh-MAY-uh-kuh | /ˌsɪr.i.əˈmeɪ.ə.kə/ | 1 Chronicles 19:6 |  | still wrong (0.70) |
| Medeba | MEHD-uh-buhh | /ˈmɛd.ə.bə/ | 1 Chronicles 19:7 | ✅ | overridden (0.84) |
| Shophach | SHOH-fak | /ˈʃoʊ.fæk/ | 1 Chronicles 19:16 | ✅ | overridden (0.92) |
| Rabbah | RAB-uh | /ˈræb.ə/ | 1 Chronicles 20:1 |  | fine as spelled (1.00) |
| Sibbecai | SIB-eh-ky | /ˈsɪb.ə.kaɪ/ | 1 Chronicles 20:4 |  | fine as spelled (0.92) |
| Sibbechai | SIB-ih-ky | /ˈsɪb.ɪ.kaɪ/ | 1 Chronicles 20:4 |  | fine as spelled (0.83) |
| Sippai | SIP-eye | /ˈsɪp.aɪ/ | 1 Chronicles 20:4 |  | fine as spelled (1.00) |
| Goliath | guh-LY-uhth | /ɡəˈlaɪ.əθ/ | 1 Chronicles 20:5 |  | fine as spelled (0.83) |
| Lahmi | LAH-my | /ˈlɑː.maɪ/ | 1 Chronicles 20:5 |  | suggestion waiting (0.75) |
| Ornan | OR-nan | /ˈɔːr.næn/ | 1 Chronicles 21:15 |  | suggestion waiting (0.73) |
| Sidonians | sy-DOH-nee-uhnz | /saɪˈdoʊ.ni.ənz/ | 1 Chronicles 22:4 |  | fine as spelled (1.00) |
| Zidonians | zy-DOH-nee-unz | /zaɪˈdoʊ.ni.ənz/ | 1 Chronicles 22:4 |  | fine as spelled (1.00) |
| Gershonites | GUR-shuhn-ites | /ˈɡɜːr.ʃən.aɪts/ | 1 Chronicles 23:7 |  | still wrong (0.78) |
| Laadan | LAY-uh-dan | /ˈleɪ.ə.dæn/ | 1 Chronicles 23:7 | ✅ | overridden (0.83) |
| Zetham | ZEE-tham | /ˈziː.θæm/ | 1 Chronicles 23:8 |  | fine as spelled (0.80) |
| Haziel | HAY-zee-el | /ˈheɪ.zi.ɛl/ | 1 Chronicles 23:9 |  | suggestion waiting (0.75) |
| Zina | ZY-nuh | /ˈzaɪ.nə/ | 1 Chronicles 23:10 |  | suggestion waiting (0.75) |
| Zizah | ZY-zuh | /ˈzaɪ.zə/ | 1 Chronicles 23:11 |  | fine as spelled (0.90) |
| Rehabiah | ree-huh-BY-uh | /ˌriː.həˈbaɪ.ə/ | 1 Chronicles 23:17 |  | suggestion waiting (0.71) |
| Jekameam | jek-uh-MEE-am | /ˌdʒɛk.əˈmiː.æm/ | 1 Chronicles 23:19 |  | fine as spelled (0.88) |
| Ahimelech | uh-HIM-eh-lek | /əˈhɪm.ə.lɛk/ | 1 Chronicles 24:3 |  | fine as spelled (0.94) |
| Harim | HAY-rihm | /ˈheɪ.rɪm/ | 1 Chronicles 24:8 | ✅ | overridden (1.00) |
| Seorim | see-OR-im | /siˈɔːr.ɪm/ | 1 Chronicles 24:8 |  | fine as spelled (0.83) |
| Mijamin | MIHJ-uh-mihn | /ˈmɪdʒ.ə.mɪn/ | 1 Chronicles 24:9 | ✅ | overridden (0.94) |
| Jeshua | JESH-oo-uh | /ˈdʒɛʃ.u.ə/ | 1 Chronicles 24:11 |  | fine as spelled (1.00) |
| Huppah | HUP-uh | /ˈhʌp.ə/ | 1 Chronicles 24:13 |  | still wrong (0.75) |
| Jeshebeab | jushebbyab | /dʒəˈʃɛb.i.æb/ | 1 Chronicles 24:13 | ✅ | overridden (0.88) |
| Bilgah | BIL-guh | /ˈbɪl.ɡə/ | 1 Chronicles 24:14 |  | fine as spelled (1.00) |
| Aphses | AF-seez | /ˈæf.siːz/ | 1 Chronicles 24:15 |  | fine as spelled (0.80) |
| Happizzez | HAP-ih-zez | /ˈhæp.ɪ.zɛz/ | 1 Chronicles 24:15 |  | still wrong (0.75) |
| Hezir | HEE-zer | /ˈhiː.zər/ | 1 Chronicles 24:15 |  | fine as spelled (1.00) |
| Jehezekel | jih-HEZ-ih-kel | /dʒɪˈhɛz.ɪ.kɛl/ | 1 Chronicles 24:16 |  | still wrong (0.78) |
| Jehezkel | juh-HEZ-kel | /dʒəˈhɛz.kɛl/ | 1 Chronicles 24:16 |  | suggestion waiting (0.75) |
| Pethahiah | peth-uh-HY-uh | /ˌpɛθ.əˈhaɪ.ə/ | 1 Chronicles 24:16 |  | fine as spelled (0.80) |
| Gamul | GAY-muhl | /ˈɡeɪ.məl/ | 1 Chronicles 24:17 |  | fine as spelled (0.80) |
| Maaziah | may-uh-ZEYE-uh | /ˌmeɪ.əˈzaɪ.ə/ | 1 Chronicles 24:18 | ✅ | overridden (1.00) |
| Jehdeiah | jeh-DEE-uh | /dʒɛˈdiː.ə/ | 1 Chronicles 24:20 | ✅ | overridden (0.80) |
| Shubael | SHOO-bay-el | /ˈʃuː.beɪ.ɛl/ | 1 Chronicles 24:20 |  | suggestion waiting (0.75) |
| Izharites | IZ-har-ites | /ˈɪz.hɑːr.aɪts/ | 1 Chronicles 24:22 |  | suggestion waiting (0.75) |
| Shelomoth | SHEL-uh-moth | /ˈʃɛl.ə.mɒθ/ | 1 Chronicles 24:22 |  | fine as spelled (0.93) |
| Michah | MY-kuh | /ˈmaɪ.kə/ | 1 Chronicles 24:24 |  | fine as spelled (1.00) |
| Shamir | shaymihr | /ˈʃeɪ.mɪr/ | 1 Chronicles 24:24 | ✅ | overridden (0.80) |
| Beno | BEE-noh | /ˈbiː.noʊ/ | 1 Chronicles 24:26 |  | fine as spelled (0.88) |
| Jaaziah | jay-uh-ZEYE-uh | /ˌdʒeɪ.əˈzaɪ.ə/ | 1 Chronicles 24:26 | ✅ | overridden (1.00) |
| Ibri | IB-ry | /ˈɪb.raɪ/ | 1 Chronicles 24:27 |  | suggestion waiting (0.75) |
| Shoham | SHOH-ham | /ˈʃoʊ.hæm/ | 1 Chronicles 24:27 | ✅ | overridden (0.80) |
| Asarelah | as-uh-REE-luh | /ˌæs.əˈriː.lə/ | 1 Chronicles 25:2 |  | fine as spelled (1.00) |
| Asharelah | ash-uh-REE-luh | /ˌæʃ.əˈriː.lə/ | 1 Chronicles 25:2 |  | fine as spelled (0.93) |
| Nethaniah | neth-uh-NY-uh | /ˌnɛθ.əˈnaɪ.ə/ | 1 Chronicles 25:2 |  | fine as spelled (1.00) |
| Gedaliah | ged-uh-LY-uh | /ˌɡɛd.əˈlaɪ.ə/ | 1 Chronicles 25:3 |  | still wrong (0.57) |
| Zeri | zeereye | /ˈziː.raɪ/ | 1 Chronicles 25:3 | ✅ | overridden (1.00) |
| Bukkiah | buh-KY-uh | /bəˈkaɪ.ə/ | 1 Chronicles 25:4 |  | still wrong (0.50) |
| Eliathah | ih-LY-uh-thuh | /ɪˈlaɪ.ə.θə/ | 1 Chronicles 25:4 |  | fine as spelled (0.83) |
| Giddalti | gih-DAL-ty | /ɡɪˈdæl.taɪ/ | 1 Chronicles 25:4 |  | still wrong (0.43) |
| Hanani | hanayneye | /həˈneɪ.naɪ/ | 1 Chronicles 25:4 | ✅ | overridden (0.83) |
| Hothir | hohthuhr | /ˈhoʊ.θər/ | 1 Chronicles 25:4 | ✅ | overridden (1.00) |
| Joshbekashah | jahshbuhkayshuh | /ˌdʒɒʃ.bəˈkeɪ.ʃə/ | 1 Chronicles 25:4 | ✅ | overridden (0.89) |
| Mahazioth | muh-HAY-zee-oth | /məˈheɪ.zi.ɒθ/ | 1 Chronicles 25:4 | ✅ | overridden (0.88) |
| Mallothi | MAL-oh-thy | /ˈmæl.ə.θaɪ/ | 1 Chronicles 25:4 |  | still wrong (0.75) |
| Romamti-Ezer | roh-MAM-ty EE-zer | /roʊˌmæm.taɪ ˈiː.zər/ | 1 Chronicles 25:4 |  | still wrong (0.73) |
| Romamti-ezer | roh-mam-tee-EE-zer | /roʊˌmæm.tiˈiː.zər/ | 1 Chronicles 25:4 |  | fine as spelled (0.82) |
| Shebuel | shih-BYOO-el | /ʃɪˈbjuː.ɛl/ | 1 Chronicles 25:4 |  | still wrong (0.67) |
| Izri | ihzreye | /ˈɪz.raɪ/ | 1 Chronicles 25:11 | ✅ | overridden (1.00) |
| Jesharelah | jehsh-uh-REE-luh | /ˌdʒɛʃ.əˈriː.lə/ | 1 Chronicles 25:14 | ✅ | overridden (0.88) |
| Jathniel | JATH-nee-el | /ˈdʒæθ.ni.ɛl/ | 1 Chronicles 26:2 |  | still wrong (0.57) |
| Eliehoenai | ih-ly-eh-hoh-EE-ny | /ɪˌlaɪ.ə.hoʊˈiː.naɪ/ | 1 Chronicles 26:3 |  | still wrong (0.56) |
| Jehohanan | jee-hoh-HAY-nan | /ˌdʒiː.hoʊˈheɪ.næn/ | 1 Chronicles 26:3 | ✅ | overridden (0.89) |
| Jehozabad | juh-HOZ-uh-bad | /dʒəˈhɒz.ə.bæd/ | 1 Chronicles 26:4 |  | suggestion waiting (0.78) |
| Peullethai | pee-UL-eh-thy | /piˈʌl.ə.θaɪ/ | 1 Chronicles 26:5 |  | still wrong (0.57) |
| Peulthai | pee-UL-thy | /piːˈʌl.θaɪ/ | 1 Chronicles 26:5 |  | still wrong (0.50) |
| Rephael | REHF-ay-el | /ˈrɛf.eɪ.ɛl/ | 1 Chronicles 26:7 | ✅ | overridden (0.83) |
| Semachiah | sehm-uh-KEYE-uh | /ˌsɛm.əˈkaɪ.ə/ | 1 Chronicles 26:7 | ✅ | overridden (1.00) |
| Tebaliah | teb-uh-LY-uh | /ˌtɛb.əˈlaɪ.ə/ | 1 Chronicles 26:11 |  | still wrong (0.50) |
| Shelemiah | shel-uh-MY-uh | /ˌʃɛl.əˈmaɪ.ə/ | 1 Chronicles 26:14 |  | still wrong (0.57) |
| Asuppim | uh-SUP-im | /əˈsʌp.ɪm/ | 1 Chronicles 26:15 |  | suggestion waiting (0.71) |
| Shallecheth | SHAL-eh-keth | /ˈʃæl.ə.kɛθ/ | 1 Chronicles 26:16 |  | still wrong (0.29) |
| Parbar | PAR-bar | /ˈpɑːr.bɑːr/ | 1 Chronicles 26:18 |  | fine as spelled (0.83) |
| Gershonite | GUR-shuhn-ite | /ˈɡɜːr.ʃən.aɪt/ | 1 Chronicles 26:21 |  | fine as spelled (0.88) |
| Jehieli | ja-HEYE-uh-leye | /dʒəˈhaɪ.ə.laɪ/ | 1 Chronicles 26:21 | ✅ | overridden (0.86) |
| Amramites | AM-ram-ites | /ˈæm.ræm.aɪts/ | 1 Chronicles 26:23 |  | still wrong (0.75) |
| Hebronites | HEE-bruhn-ites | /ˈhiː.brən.aɪts/ | 1 Chronicles 26:23 |  | fine as spelled (1.00) |
| Uzzielites | azeyeuhleyets | /əˈzaɪ.əl.aɪts/ | 1 Chronicles 26:23 | ✅ | overridden (0.86) |
| Abner | AB-ner | /ˈæb.nər/ | 1 Chronicles 26:28 |  | fine as spelled (1.00) |
| Jerijah | juh-REYE-juh | /dʒəˈraɪ.dʒə/ | 1 Chronicles 26:31 | ✅ | overridden (0.83) |
| Manassites | muh-NAS-ites | /məˈnæs.aɪts/ | 1 Chronicles 26:32 |  | still wrong (0.69) |
| Zabdiel | ZAB-dee-el | /ˈzæb.di.ɛl/ | 1 Chronicles 27:2 |  | suggestion waiting (0.79) |
| Dodai | DOH-deye | /ˈdoʊ.daɪ/ | 1 Chronicles 27:4 | ✅ | overridden (1.00) |
| Ammizabad | uh-MIHZ-uh-bad | /əˈmɪz.ə.bæd/ | 1 Chronicles 27:6 | ✅ | overridden (1.00) |
| Izrahite | ihzruhheyet | /ˈɪz.rə.haɪt/ | 1 Chronicles 27:8 | ✅ | overridden (0.87) |
| Shamhuth | SHAM-huth | /ˈʃæm.hʌθ/ | 1 Chronicles 27:8 |  | fine as spelled (0.83) |
| Ira | EYE-ruh | /ˈaɪ.rə/ | 1 Chronicles 27:9 |  | fine as spelled (1.00) |
| Zarhites | zahrheyets | /ˈzɑːr.haɪts/ | 1 Chronicles 27:11 | ✅ | overridden (0.88) |
| Zerahites | ZER-uh-hites | /ˈzɛr.ə.haɪts/ | 1 Chronicles 27:11 |  | suggestion waiting (0.75) |
| Anetothite | uh-NET-uh-thite | /əˈnɛt.ə.θaɪt/ | 1 Chronicles 27:12 |  | still wrong (0.44) |
| Benjamites | BEHN-ja-meyets | /ˈbɛn.dʒə.maɪts/ | 1 Chronicles 27:12 | ✅ | overridden (0.94) |
| Maharai | MAY-huh-ry | /ˈmeɪ.hə.raɪ/ | 1 Chronicles 27:13 |  | fine as spelled (0.83) |
| Heldai | HEL-dye | /ˈhɛl.daɪ/ | 1 Chronicles 27:15 |  | fine as spelled (0.80) |
| Simeonites | SIM-ee-uhn-ites | /ˈsɪm.i.ən.aɪts/ | 1 Chronicles 27:16 |  | fine as spelled (0.89) |
| Kemuel | KEHM-yoo-el | /ˈkɛm.ju.ɛl/ | 1 Chronicles 27:17 | ✅ | overridden (0.81) |
| Ishmaiah | ish-MAY-yuh | /ɪʃˈmeɪ.ə/ | 1 Chronicles 27:19 |  | fine as spelled (1.00) |
| Hoshea | hoh-SHEE-uh | /hoʊˈʃiː.ə/ | 1 Chronicles 27:20 |  | fine as spelled (0.80) |
| Ezri | EZ-ry | /ˈɛz.raɪ/ | 1 Chronicles 27:26 |  | suggestion waiting (0.75) |
| Ramathite | RAY-muh-thite | /ˈreɪ.mə.θaɪt/ | 1 Chronicles 27:27 |  | still wrong (0.56) |
| Shiphmite | SHIHF-meyet | /ˈʃɪf.maɪt/ | 1 Chronicles 27:27 | ✅ | overridden (1.00) |
| Gederite | GED-uh-rite | /ˈɡɛd.ə.raɪt/ | 1 Chronicles 27:28 |  | still wrong (0.71) |
| Adlai | AD-lay | /ˈæd.leɪ/ | 1 Chronicles 27:29 |  | fine as spelled (1.00) |
| Sharonite | SHAIR-uhn-ite | /ˈʃɛər.ən.aɪt/ | 1 Chronicles 27:29 |  | fine as spelled (0.86) |
| Shitrai | shih-TRY | /ʃɪˈtraɪ/ | 1 Chronicles 27:29 |  | fine as spelled (0.83) |
| Hagrite | HAG-rite | /ˈhæɡ.raɪt/ | 1 Chronicles 27:30 |  | fine as spelled (1.00) |
| Jaziz | JAY-zihzz | /ˈdʒeɪ.zɪz/ | 1 Chronicles 27:30 | ✅ | overridden (1.00) |
| Meronothite | muh-RON-oh-thite | /məˈrɒn.ə.θaɪt/ | 1 Chronicles 27:30 |  | fine as spelled (0.95) |
| Obil | OH-bil | /ˈoʊ.bɪl/ | 1 Chronicles 27:30 |  | fine as spelled (1.00) |
| Hagerite | haguhreyet | /ˈhæɡ.ə.raɪt/ | 1 Chronicles 27:31 | ✅ | overridden (1.00) |
| Hachmoni | hakmuhneye | /ˈhæk.mə.naɪ/ | 1 Chronicles 27:32 | ✅ | overridden (1.00) |
| Ahithophel | uh-HITH-uh-fehl | /əˈhɪθ.ə.fɛl/ | 1 Chronicles 27:33 | ✅ | overridden (0.94) |
| Archite | AR-kite | /ˈɑːr.kaɪt/ | 1 Chronicles 27:33 |  | fine as spelled (0.80) |
| Hushai | HOO-shy | /ˈhuː.ʃaɪ/ | 1 Chronicles 27:33 |  | suggestion waiting (0.75) |
| Kue | kooay | /ˈkuː.eɪ/ | 2 Chronicles 1:16 | ✅ | overridden (1.00) |
| Lebanon | LEB-uh-nuhn | /ˈlɛb.ə.nən/ | 2 Chronicles 2:8 |  | fine as spelled (0.86) |
| Joppa | JOP-uh | /ˈdʒɒp.ə/ | 2 Chronicles 2:16 |  | fine as spelled (0.90) |
| Moriah | muh-RY-uh | /məˈraɪ.ə/ | 2 Chronicles 3:1 |  | fine as spelled (1.00) |
| Parvaim | par-VAY-im | /pɑːrˈveɪ.ɪm/ | 2 Chronicles 3:6 |  | still wrong (0.79) |
| Succoth | SUHK-oth | /ˈsʌk.ɒθ/ | 2 Chronicles 4:17 | ✅ | overridden (0.80) |
| Zeredah | ZEHR-uh-duh | /ˈzɛr.ə.də/ | 2 Chronicles 4:17 | ✅ | overridden (0.83) |
| Horeb | HAWR-ehb | /ˈhɔːr.ɛb/ | 2 Chronicles 5:10 | ✅ | overridden (0.80) |
| Tadmor | TAD-mor | /ˈtæd.mɔːr/ | 2 Chronicles 8:4 |  | fine as spelled (0.83) |
| Baalath | BAY-uh-lath | /ˈbeɪ.ə.læθ/ | 2 Chronicles 8:6 | ✅ | overridden (0.83) |
| Amorites | AM-uh-rites | /ˈæm.ə.raɪts/ | 2 Chronicles 8:7 |  | fine as spelled (1.00) |
| Hittites | HIT-ites | /ˈhɪt.aɪts/ | 2 Chronicles 8:7 |  | fine as spelled (1.00) |
| Hivites | HY-vites | /ˈhaɪ.vaɪts/ | 2 Chronicles 8:7 |  | fine as spelled (0.83) |
| Perizzites | PER-ih-zites | /ˈpɛr.ɪ.zaɪts/ | 2 Chronicles 8:7 |  | fine as spelled (1.00) |
| Eloth | EE-loth | /ˈiː.lɒθ/ | 2 Chronicles 8:17 |  | still wrong (0.62) |
| Ezion | EE-zee-on | /ˈiː.zi.ɒn/ | 2 Chronicles 8:17 |  | fine as spelled (0.80) |
| Geber | GEE-ber | /ˈɡiː.bər/ | 2 Chronicles 8:17 |  | fine as spelled (0.80) |
| Arabia | uh-RAY-bee-uh | /əˈreɪ.bi.ə/ | 2 Chronicles 9:14 |  | fine as spelled (1.00) |
| Nebat | NEE-batt | /ˈniː.bæt/ | 2 Chronicles 9:29 | ✅ | overridden (0.80) |
| Shilonite | SHY-luh-nite | /ˈʃaɪ.lə.naɪt/ | 2 Chronicles 9:29 |  | fine as spelled (0.86) |
| Azekah | uh-ZEE-kuh | /əˈziː.kə/ | 2 Chronicles 11:9 |  | fine as spelled (0.92) |
| Lachish | LAY-kish | /ˈleɪ.kɪʃ/ | 2 Chronicles 11:9 |  | fine as spelled (1.00) |
| Mahalath | MAY-huh-lath | /ˈmeɪ.hə.læθ/ | 2 Chronicles 11:18 |  | still wrong (0.79) |
| Shemariah | shem-uh-RY-uh | /ˌʃɛm.əˈraɪ.ə/ | 2 Chronicles 11:19 |  | fine as spelled (0.86) |
| Zaham | ZAY-ham | /ˈzeɪ.hæm/ | 2 Chronicles 11:19 | ✅ | overridden (0.80) |
| Shishak | SHY-shak | /ˈʃaɪ.ʃæk/ | 2 Chronicles 12:2 |  | fine as spelled (0.80) |
| Ethiopians | Ethiopians | /iːθiːˈoʊpiːənz/ | 2 Chronicles 12:3 |  | fine as spelled (1.00) |
| Lubim | LOO-bim | /ˈluː.bɪm/ | 2 Chronicles 12:3 |  | suggestion waiting (0.70) |
| Sukkiim | SUHK-ee-im | /ˈsʌk.i.ɪm/ | 2 Chronicles 12:3 |  | fine as spelled (0.83) |
| Ammonitess | AM-uh-nite-ess | /ˈæm.ə.naɪ.tɛs/ | 2 Chronicles 12:13 |  | still wrong (0.75) |
| Naamah | NAY-uh-muh | /ˈneɪ.ə.mə/ | 2 Chronicles 12:13 | ✅ | overridden (1.00) |
| Micaiah | my-KAY-uh | /maɪˈkeɪ.ə/ | 2 Chronicles 13:2 | ✅ | overridden (0.92) |
| Zemaraim | zem-uh-RAY-im | /ˌzɛm.əˈreɪ.ɪm/ | 2 Chronicles 13:4 |  | fine as spelled (0.81) |
| Ephron | EE-fron | /ˈiː.frɒn/ | 2 Chronicles 13:19 | ✅ | overridden (0.92) |
| Jeshanah | JESH-uh-nuh | /ˈdʒɛʃ.ə.nə/ | 2 Chronicles 13:19 |  | still wrong (0.67) |
| Asherah | uh-SHEER-uh | /əˈʃɪr.ə/ | 2 Chronicles 14:3 |  | fine as spelled (0.80) |
| Ethiopian | Ethiopian | /iːθiːˈoʊpiːən/ | 2 Chronicles 14:9 |  | fine as spelled (1.00) |
| Zephathah | ZEF-uh-thuh | /ˈzɛf.ə.θə/ | 2 Chronicles 14:10 |  | fine as spelled (0.92) |
| Gerar | geerrahr | /ˈɡɪər.ɑːr/ | 2 Chronicles 14:13 | ✅ | overridden (0.80) |
| Oded | OH-ded | /ˈoʊ.dɛd/ | 2 Chronicles 15:1 |  | fine as spelled (1.00) |
| Kidron | KID-ruhn | /ˈkɪd.rən/ | 2 Chronicles 15:16 |  | fine as spelled (0.83) |
| Baasha | BAY-uh-shuh | /ˈbeɪ.ə.ʃə/ | 2 Chronicles 16:1 |  | still wrong (0.40) |
| Ramah | RAY-muh | /ˈreɪ.mə/ | 2 Chronicles 16:1 |  | suggestion waiting (0.75) |
| Abel | AY-buhl | /ˈeɪ.bəl/ | 2 Chronicles 16:4 |  | fine as spelled (1.00) |
| Ijon | EYE-jon | /ˈaɪ.dʒɒn/ | 2 Chronicles 16:4 |  | suggestion waiting (0.75) |
| Maim | MAY-im | /ˈmeɪ.ɪm/ | 2 Chronicles 16:4 |  | suggestion waiting (0.75) |
| Mizpah | MIHZ-pa | /ˈmɪz.pə/ | 2 Chronicles 16:6 | ✅ | overridden (0.80) |
| Rama | RAY-muh | /ˈreɪ.mə/ | 2 Chronicles 16:6 |  | suggestion waiting (0.75) |
| Baals | BAY-uhlz | /ˈbeɪ.əlz/ | 2 Chronicles 17:3 |  | fine as spelled (0.80) |
| Jehonathan | juh-HON-uh-thuhn | /dʒəˈhɒn.ə.θən/ | 2 Chronicles 17:8 |  | fine as spelled (0.89) |
| Jehoram | juh-HOR-uhm | /dʒəˈhɔːr.əm/ | 2 Chronicles 17:8 |  | fine as spelled (0.86) |
| Tobadonijah | tob-ad-oh-NY-juh | /ˌtɒb.æd.oʊˈnaɪ.dʒə/ | 2 Chronicles 17:8 |  | still wrong (0.60) |
| Tobijah | tohbeyejuh | /toʊˈbaɪ.dʒə/ | 2 Chronicles 17:8 | ✅ | overridden (1.00) |
| Arabians | uh-RAY-bee-uhnz | /əˈreɪ.bi.ənz/ | 2 Chronicles 17:11 |  | fine as spelled (1.00) |
| Amasiah | am-uh-SY-uh | /ˌæm.əˈsaɪ.ə/ | 2 Chronicles 17:16 |  | fine as spelled (0.86) |
| Ahab | AY-hab | /ˈeɪ.hæb/ | 2 Chronicles 18:1 |  | fine as spelled (0.88) |
| Imla | IM-luh | /ˈɪm.lə/ | 2 Chronicles 18:7 |  | fine as spelled (0.88) |
| Asheroth | ASH-uh-roth | /ˈæʃ.ə.rɒθ/ | 2 Chronicles 19:3 |  | suggestion waiting (0.75) |
| Ammonites | AM-uh-nites | /ˈæm.ə.naɪts/ | 2 Chronicles 20:1 |  | fine as spelled (1.00) |
| Gedi | GED-ee | /ˈɡɛd.i/ | 2 Chronicles 20:2 |  | still wrong (0.75) |
| Hazazon | HAZ-uh-zon | /ˈhæz.ə.zɒn/ | 2 Chronicles 20:2 |  | fine as spelled (1.00) |
| Levite | LEE-vite | /ˈliː.vaɪt/ | 2 Chronicles 20:14 |  | fine as spelled (1.00) |
| Jeruel | juh-ROO-ehll | /dʒəˈruː.ɛl/ | 2 Chronicles 20:16 | ✅ | overridden (0.92) |
| Ziz | ZIZ | /zɪz/ | 2 Chronicles 20:16 |  | fine as spelled (1.00) |
| Beracah | BEHR-a-kuh | /ˈbɛr.ə.kə/ | 2 Chronicles 20:26 | ✅ | overridden (0.83) |
| Shilhi | SHIL-hy | /ˈʃɪl.haɪ/ | 2 Chronicles 20:31 |  | fine as spelled (1.00) |
| Dodavahu | doh-duh-VAY-hyoo | /ˌdoʊ.dəˈveɪ.huː/ | 2 Chronicles 20:37 |  | fine as spelled (0.81) |
| Jehoahaz | juh-HOH-uh-haz | /dʒəˈhoʊ.ə.hæz/ | 2 Chronicles 21:17 |  | fine as spelled (1.00) |
| Hazael | HAZ-ay-el | /ˈhæz.eɪ.ɛl/ | 2 Chronicles 22:5 | ✅ | overridden (0.83) |
| Nimshi | NIM-shy | /ˈnɪm.ʃaɪ/ | 2 Chronicles 22:7 |  | fine as spelled (0.80) |
| Jehoshabeath | jee-hoh-SHAB-ee-athh | /ˌdʒiː.hoʊˈʃæb.i.æθ/ | 2 Chronicles 22:11 | ✅ | overridden (0.91) |
| Elishaphat | ih-LISH-uh-fat | /ɪˈlɪʃ.ə.fæt/ | 2 Chronicles 23:1 |  | fine as spelled (1.00) |
| Mattan | maatan | /ˈmæt.æn/ | 2 Chronicles 23:17 | ✅ | overridden (0.80) |
| Zibiah | ZIB-ee-uh | /ˈzɪb.i.ə/ | 2 Chronicles 24:1 |  | fine as spelled (1.00) |
| Moabitess | MOH-uh-bite-ess | /ˈmoʊ.ə.baɪ.tɛs/ | 2 Chronicles 24:26 |  | still wrong (0.56) |
| Shimeath | SHIM-ee-ath | /ˈʃɪm.i.æθ/ | 2 Chronicles 24:26 |  | still wrong (0.42) |
| Shimrith | SHIM-rith | /ˈʃɪm.rɪθ/ | 2 Chronicles 24:26 |  | fine as spelled (1.00) |
| Jehoaddan | jee-hoh-AD-an | /ˌdʒiː.hoʊˈæd.æn/ | 2 Chronicles 25:1 | ✅ | overridden (0.88) |
| Jechiliah | jek-ih-LY-uh | /ˌdʒɛk.ɪˈlaɪ.ə/ | 2 Chronicles 26:3 |  | still wrong (0.57) |
| Ashdod | ASH-dod | /ˈæʃ.dɒd/ | 2 Chronicles 26:6 |  | fine as spelled (1.00) |
| Jabneh | JAB-neh | /ˈdʒæb.nə/ | 2 Chronicles 26:6 |  | fine as spelled (1.00) |
| Gur | GOOR | /ɡʊər/ | 2 Chronicles 26:7 |  | still wrong (0.67) |
| Amoz | AY-moz | /ˈeɪ.mɒz/ | 2 Chronicles 26:22 |  | still wrong (0.68) |
| Isaiah | eye-ZAY-uh | /aɪˈzeɪ.ə/ | 2 Chronicles 26:22 |  | fine as spelled (1.00) |
| Jerushah | juh-ROO-shuh | /dʒəˈruː.ʃə/ | 2 Chronicles 27:1 |  | fine as spelled (0.83) |
| Ophel | OH-fehl | /ˈoʊ.fɛl/ | 2 Chronicles 27:3 | ✅ | overridden (1.00) |
| Hinnom | HIN-uhm | /ˈhɪn.əm/ | 2 Chronicles 28:3 |  | fine as spelled (1.00) |
| Pekah | peeka | /ˈpiː.kə/ | 2 Chronicles 28:6 | ✅ | overridden (1.00) |
| Remaliah | rem-uh-LY-uh | /ˌrɛm.əˈlaɪ.ə/ | 2 Chronicles 28:6 |  | fine as spelled (0.86) |
| Hadlai | HAD-lye | /ˈhæd.laɪ/ | 2 Chronicles 28:12 |  | fine as spelled (1.00) |
| Jehizkiah | jee-hihz-KEYE-uh | /ˌdʒiː.hɪzˈkaɪ.ə/ | 2 Chronicles 28:12 | ✅ | overridden (0.88) |
| Meshillemoth | muh-SHIL-eh-moth | /məˈʃɪl.ə.mɒθ/ | 2 Chronicles 28:12 |  | fine as spelled (0.89) |
| Gederoth | gadeeroth | /ɡəˈdiː.rɒθ/ | 2 Chronicles 28:18 | ✅ | overridden (1.00) |
| Gimzo | GIM-zoh | /ˈɡɪm.zoʊ/ | 2 Chronicles 28:18 |  | fine as spelled (1.00) |
| Timnah | TIM-nuh | /ˈtɪm.nə/ | 2 Chronicles 28:18 |  | fine as spelled (1.00) |
| Eden | EE-duhn | /ˈiː.dən/ | 2 Chronicles 29:12 |  | fine as spelled (1.00) |
| Jehuel | juh-HYOO-el | /dʒəˈhjuː.ɛl/ | 2 Chronicles 29:14 |  | still wrong (0.50) |
| Passovers | Passovers | /ˈpæs.sə.vərs/ | 2 Chronicles 30:17 |  | unsure (guessed IPA) (0.75) |
| Conaniah | kon-uh-NY-uh | /ˌkɒn.əˈnaɪ.ə/ | 2 Chronicles 31:12 |  | still wrong (0.57) |
| Ismachiah | is-muh-KY-uh | /ˌɪs.məˈkaɪ.ə/ | 2 Chronicles 31:13 |  | still wrong (0.79) |
| Miniamin | mih-NY-uh-min | /mɪˈnaɪ.ə.mɪn/ | 2 Chronicles 31:15 |  | still wrong (0.50) |
| Sennacherib | suh-NAK-er-ib | /səˈnæk.ər.ɪb/ | 2 Chronicles 32:1 |  | fine as spelled (1.00) |
| Gihon | geyehon | /ˈɡaɪ.hɒn/ | 2 Chronicles 32:30 | ✅ | overridden (1.00) |
| Hozai | HOH-zy | /ˈhoʊ.zaɪ/ | 2 Chronicles 33:19 |  | suggestion waiting (0.75) |
| Azaliah | az-uh-LY-uh | /ˌæz.əˈlaɪ.ə/ | 2 Chronicles 34:8 |  | fine as spelled (0.84) |
| Joahaz | JOH-uh-haz | /ˈdʒoʊ.ə.hæz/ | 2 Chronicles 34:8 |  | fine as spelled (0.83) |
| Shaphan | SHAY-fan | /ˈʃeɪ.fæn/ | 2 Chronicles 34:8 | ✅ | overridden (0.80) |
| Ahikam | uh-HY-kam | /əˈhaɪ.kæm/ | 2 Chronicles 34:20 | ✅ | overridden (0.86) |
| Hasrah | HAZ-ruh | /ˈhæz.rə/ | 2 Chronicles 34:22 | ✅ | overridden (0.83) |
| Huldah | HUHL-duh | /ˈhʌl.də/ | 2 Chronicles 34:22 |  | still wrong (0.73) |
| Tokhath | TOK-hath | /ˈtɒk.hæθ/ | 2 Chronicles 34:22 |  | still wrong (0.33) |
| Carchemish | KAR-keh-mish | /ˈkɑːr.kə.mɪʃ/ | 2 Chronicles 35:20 |  | suggestion waiting (0.75) |
| Neco | NEE-koh | /ˈniː.koʊ/ | 2 Chronicles 35:20 |  | fine as spelled (0.88) |
| Eliakim | ih-LY-uh-kim | /ɪˈlaɪ.ə.kɪm/ | 2 Chronicles 36:4 |  | still wrong (0.43) |
| Jehoiachin | juh-HOY-uh-kin | /dʒəˈhɔɪ.ə.kɪn/ | 2 Chronicles 36:8 |  | still wrong (0.67) |
| Chaldeans | kal-DEE-uhnz | /kælˈdiː.ənz/ | 2 Chronicles 36:17 |  | fine as spelled (0.94) |
| Persia | PUR-zhuh | /ˈpɜːr.ʒə/ | 2 Chronicles 36:20 |  | fine as spelled (0.80) |
| Cyrus | SY-ruhs | /ˈsaɪ.rəs/ | 2 Chronicles 36:22 |  | fine as spelled (1.00) |
| Mithredath | Mithredath | /ˈmi.θrə.dəθ/ | Ezra 1:8 |  | unsure (guessed IPA) (0.62) |
| Sheshbazzar | Sheshbazzar | /ˈʃiː.ʃbəz.zər/ | Ezra 1:8 |  | unsure (guessed IPA) (0.75) |
| Bigvai | Bigvai | /ˈbɪɡ.veɪ/ | Ezra 2:2 |  | fine as spelled (0.83) |
| Bilshan | Bilshan | /ˈbɪl.ʃən/ | Ezra 2:2 |  | fine as spelled (0.83) |
| Mispar | Mispar | /ˈmɪs.pər/ | Ezra 2:2 |  | unsure (guessed IPA) (0.75) |
| Mordecai | Mordecai | /mˈɔrdəkaɪ/ | Ezra 2:2 |  | still wrong (0.71) |
| Nehemiah | Nehemiah | /niːəmˈaɪə/ | Ezra 2:2 |  | fine as spelled (1.00) |
| Reelaiah | Reelaiah | /riːˈleɪ.əh/ | Ezra 2:2 |  | unsure (guessed IPA) (0.67) |
| Rehum | Rehum | /ˈriː.hjuːm/ | Ezra 2:2 |  | unsure (guessed IPA) (0.67) |
| Parosh | Parosh | /ˈpeɪ.rəʃ/ | Ezra 2:3 |  | unsure (guessed IPA) (0.60) |
| Pahathmoab | Pahathmoab | /ˈpeɪ.hə.θmoʊb/ | Ezra 2:6 |  | unsure (guessed IPA) (0.45) |
| Zattu | Zattu | /ˈzæt.tə/ | Ezra 2:8 |  | unsure (guessed IPA) (0.50) |
| Zaccai | Zaccai | /ˈzæs.seɪ/ | Ezra 2:9 |  | unsure (guessed IPA) (0.75) |
| Bebai | Bebai | /ˈbiː.beɪ/ | Ezra 2:11 |  | unsure (guessed IPA) (0.45) |
| Azgad | azghad | /ˈæz.ɡəd/ | Ezra 2:12 | ✅ | overridden (0.80) |
| Adonikam | Adonikam | /əˈdoʊ.ni.kəm/ | Ezra 2:13 |  | fine as spelled (0.81) |
| Adin | Adin | /ədˈɪn/ | Ezra 2:15 |  | still wrong (0.75) |
| Ater | Ater | /ˈeɪtɚ/ | Ezra 2:16 |  | still wrong (0.75) |
| Bezai | Bezai | /ˈbiː.zeɪ/ | Ezra 2:17 |  | unsure (guessed IPA) (0.25) |
| Jorah | Jorah | /ˈdʒoʊ.rəh/ | Ezra 2:18 |  | fine as spelled (0.80) |
| Hashum | Hashum | /ˈheɪ.ʃəm/ | Ezra 2:19 |  | fine as spelled (0.80) |
| Gibbar | Gibbar | /ˈɡɪb.bər/ | Ezra 2:20 |  | unsure (guessed IPA) (0.60) |
| Netophah | Netophah | /ˈniː.tə.fəh/ | Ezra 2:22 |  | unsure (guessed IPA) (0.43) |
| Arim | Arim | /ˈeɪ.rɪm/ | Ezra 2:25 |  | unsure (guessed IPA) (0.75) |
| Michmas | Michmas | /ˈmɪkmæʃ/ | Ezra 2:27 |  | still wrong (0.50) |
| Magbish | Magbish | /ˈmæɡ.bɪʃ/ | Ezra 2:30 |  | fine as spelled (1.00) |
| Hadid | Hadid | /hɑdˈiːd/ | Ezra 2:33 |  | still wrong (0.70) |
| Senaah | Senaah | /ˈsiː.nə.əh/ | Ezra 2:35 |  | unsure (guessed IPA) (0.50) |
| Kadmiel | Kadmiel | /ˈkæd.maɪl/ | Ezra 2:40 |  | unsure (guessed IPA) (0.71) |
| Hatita | Hatita | /ˈheɪ.ti.tə/ | Ezra 2:42 |  | unsure (guessed IPA) (0.46) |
| Shobai | Shobai | /ˈʃoʊ.beɪ/ | Ezra 2:42 |  | unsure (guessed IPA) (0.75) |
| Hasupha | Hasupha | /ˈheɪ.sə.fə/ | Ezra 2:43 |  | unsure (guessed IPA) (0.38) |
| Tabbaoth | Tabbaoth | /ˈtæb.bə.əθ/ | Ezra 2:43 |  | unsure (guessed IPA) (0.42) |
| Ziha | Ziha | /ˈzi.hə/ | Ezra 2:43 |  | unsure (guessed IPA) (0.75) |
| Keros | Keros | /ˈkiː.rəs/ | Ezra 2:44 |  | unsure (guessed IPA) (0.50) |
| Padon | Padon | /ˈpeɪ.dən/ | Ezra 2:44 |  | unsure (guessed IPA) (0.60) |
| Siaha | Siaha | /ˈsi.ə.hə/ | Ezra 2:44 |  | unsure (guessed IPA) (0.60) |
| Hagabah | Hagabah | /ˈheɪ.ɡə.bəh/ | Ezra 2:45 |  | unsure (guessed IPA) (0.71) |
| Lebanah | Lebanah | /ˈliː.bə.nəh/ | Ezra 2:45 |  | unsure (guessed IPA) (0.57) |
| Hagab | Hagab | /ˈheɪ.ɡəb/ | Ezra 2:46 |  | fine as spelled (0.80) |
| Shamlai | Shamlai | /ˈʃæm.leɪ/ | Ezra 2:46 |  | unsure (guessed IPA) (0.60) |
| Gahar | Gahar | /ˈɡeɪ.hər/ | Ezra 2:47 |  | unsure (guessed IPA) (0.60) |
| Giddel | Giddel | /ˈɡɪd.dəl/ | Ezra 2:47 |  | fine as spelled (1.00) |
| Gazzam | Gazzam | /ˈɡæz.zəm/ | Ezra 2:48 |  | fine as spelled (1.00) |
| Nekoda | Nekoda | /ˈniː.kə.də/ | Ezra 2:48 |  | unsure (guessed IPA) (0.67) |
| Besai | Besai | /ˈbiː.seɪ/ | Ezra 2:49 |  | unsure (guessed IPA) (0.62) |
| Asnah | Asnah | /ˈæs.nəh/ | Ezra 2:50 |  | fine as spelled (0.80) |
| Nephisim | Nephisim | /ˈniː.fi.sɪm/ | Ezra 2:50 |  | unsure (guessed IPA) (0.43) |
| Bakbuk | Bakbuk | /ˈbæk.bək/ | Ezra 2:51 |  | fine as spelled (0.86) |
| Hakupha | Hakupha | /ˈheɪ.kə.fə/ | Ezra 2:51 |  | unsure (guessed IPA) (0.50) |
| Harhur | Harhur | /ˈhær.hjuːr/ | Ezra 2:51 |  | unsure (guessed IPA) (0.50) |
| Bazluth | Bazluth | /ˈbæz.ləθ/ | Ezra 2:52 |  | unsure (guessed IPA) (0.75) |
| Harsha | Harsha | /hˈɑrʃə/ | Ezra 2:52 |  | fine as spelled (1.00) |
| Mehida | Mehida | /ˈmiː.hi.də/ | Ezra 2:52 |  | unsure (guessed IPA) (0.75) |
| Barkos | Barkos | /ˈbær.kəs/ | Ezra 2:53 |  | unsure (guessed IPA) (0.50) |
| Temah | Temah | /ˈtiː.məh/ | Ezra 2:53 |  | fine as spelled (0.80) |
| Hatipha | Hatipha | /ˈheɪ.ti.fə/ | Ezra 2:54 |  | unsure (guessed IPA) (0.46) |
| Neziah | Neziah | /nəˈzi.əh/ | Ezra 2:54 |  | unsure (guessed IPA) (0.67) |
| Hassophereth | Hassophereth | /həsˈsoʊ.fə.rəθ/ | Ezra 2:55 |  | unsure (guessed IPA) (0.67) |
| Peruda | Peruda | /ˈpiː.rə.də/ | Ezra 2:55 |  | unsure (guessed IPA) (0.67) |
| Sotai | Sotai | /ˈsoʊ.teɪ/ | Ezra 2:55 |  | unsure (guessed IPA) (0.75) |
| Darkon | Darkon | /ˈdær.kən/ | Ezra 2:56 |  | unsure (guessed IPA) (0.67) |
| Jaalah | Jaalah | /ˈdʒeɪ.ə.ləh/ | Ezra 2:56 |  | unsure (guessed IPA) (0.42) |
| Ami | Ami | /ˈɑmiː/ | Ezra 2:57 |  | fine as spelled (0.88) |
| Hattil | Hattil | /ˈhæt.tɪl/ | Ezra 2:57 |  | fine as spelled (1.00) |
| Hazzebaim | Hazzebaim | /ˈhæz.zə.beɪm/ | Ezra 2:57 |  | fine as spelled (1.00) |
| Pochereth | pokereth | /ˈpoʊ.kə.rəθ/ | Ezra 2:57 | ✅ | overridden (0.86) |
| Addan | Addan | /ˈæd.dən/ | Ezra 2:59 |  | fine as spelled (1.00) |
| Melah | Melah | /ˈmiː.ləh/ | Ezra 2:59 |  | unsure (guessed IPA) (0.60) |
| Tel | Tel | /tˈɛl/ | Ezra 2:59 |  | fine as spelled (1.00) |
| Tobiah | Tobiah | /təˈbi.əh/ | Ezra 2:60 |  | unsure (guessed IPA) (0.42) |
| Habaiah | Habaiah | /həˈbeɪ.əh/ | Ezra 2:61 |  | unsure (guessed IPA) (0.67) |
| Jozadak | Jozadak | /ˈdʒoʊ.zə.dək/ | Ezra 3:2 |  | fine as spelled (0.86) |
| Henadad | Henadad | /ˈhiː.nə.dəd/ | Ezra 3:9 |  | unsure (guessed IPA) (0.71) |
| Esar | Esar | /ˈiː.sər/ | Ezra 4:2 |  | unsure (guessed IPA) (0.50) |
| Darius | Darius | /dɚˈaɪəs/ | Ezra 4:5 |  | still wrong (0.67) |
| Ahasuerus | Ahasuerus | /əhæʃəwˈɛrəs/ | Ezra 4:6 |  | still wrong (0.50) |
| Artaxerxes | Artaxerxes | /ˌɑːtə(ɡ)ˈzɜːksiːz/ | Ezra 4:7 |  | still wrong (0.58) |
| Bishlam | Bishlam | /ˈbi.ʃləm/ | Ezra 4:7 |  | fine as spelled (0.83) |
| Tabeel | Tabeel | /ˈteɪ.biːl/ | Ezra 4:7 |  | unsure (guessed IPA) (0.63) |
| Shimshai | Shimshai | /ˈʃɪm.ʃeɪ/ | Ezra 4:8 |  | fine as spelled (0.80) |
| Apharsathchites | Apharsathchites | /ə.fərˈseɪ.θki.təs/ | Ezra 4:9 |  | unsure (guessed IPA) (0.67) |
| Apharsites | Apharsites | /əˈfær.si.təs/ | Ezra 4:9 |  | unsure (guessed IPA) (0.61) |
| Archevites | Archevites | /ərˈkiː.vi.təs/ | Ezra 4:9 |  | unsure (guessed IPA) (0.56) |
| Babylonians | Babylonians | /bæbəlˈoʊniːənz/ | Ezra 4:9 |  | fine as spelled (0.86) |
| Dehaites | Dehaites | /ˈdiː.heɪ.təs/ | Ezra 4:9 |  | fine as spelled (0.86) |
| Dinaites | Dinaites | /ˈdi.neɪ.təs/ | Ezra 4:9 |  | unsure (guessed IPA) (0.57) |
| Shushanchites | Shushanchites | /ʃəˈʃæn.ki.təs/ | Ezra 4:9 |  | unsure (guessed IPA) (0.55) |
| Tarpelites | Tarpelites | /tərˈpiː.li.təs/ | Ezra 4:9 |  | unsure (guessed IPA) (0.70) |
| Osnappar | Osnappar | /ˈɒs.nəp.pər/ | Ezra 4:10 |  | fine as spelled (0.80) |
| Haggai | Haggai | /ˈhæɡaɪ/ | Ezra 5:1 |  | fine as spelled (0.80) |
| Shetharbozenai | Shetharbozenai | /ʃə.θərˈboʊ.zə.neɪ/ | Ezra 5:3 |  | unsure (guessed IPA) (0.73) |
| Tattenai | Tattenai | /ˈtæt.tə.neɪ/ | Ezra 5:3 |  | unsure (guessed IPA) (0.58) |
| Apharsachites | Apharsachites | /ə.fərˈseɪ.ki.təs/ | Ezra 5:6 |  | unsure (guessed IPA) (0.55) |
| Achmetha | Achmetha | /ˈeɪ.kmə.θə/ | Ezra 6:2 |  | unsure (guessed IPA) (0.75) |
| Media | Media | /mˈiːdiːə/ | Ezra 6:2 |  | fine as spelled (0.80) |
| Adar | Adar | /ədˈɑr/ | Ezra 6:15 |  | fine as spelled (1.00) |
| Josiphiah | Josiphiah | /dʒə.siˈfi.əh/ | Ezra 8:10 |  | unsure (guessed IPA) (0.62) |
| Hakkatan | Hakkatan | /ˈhæk.kə.tən/ | Ezra 8:12 |  | unsure (guessed IPA) (0.71) |
| Zabbud | Zabbud | /ˈzæb.bəd/ | Ezra 8:14 |  | fine as spelled (0.90) |
| Ahava | Ahava | /ˈeɪ.hə.və/ | Ezra 8:15 |  | unsure (guessed IPA) (0.55) |
| Joiarib | Joiarib | /ˈdʒɔɪ.ə.rɪb/ | Ezra 8:16 |  | unsure (guessed IPA) (0.67) |
| Casiphia | Casiphia | /səˈsi.fi.ə/ | Ezra 8:17 |  | unsure (guessed IPA) (0.64) |
| Sherebiah | Sherebiah | /ʃə.rəˈbi.əh/ | Ezra 8:18 |  | unsure (guessed IPA) (0.75) |
| Binnui | Binnui | /ˈbɪn.nuː/ | Ezra 8:33 |  | fine as spelled (0.80) |
| Meremoth | Meremoth | /ˈmiː.rə.məθ/ | Ezra 8:33 |  | unsure (guessed IPA) (0.64) |
| Noadiah | Noadiah | /noʊˈdi.əh/ | Ezra 8:33 |  | unsure (guessed IPA) (0.67) |
| Jahzeiah | Jahzeiah | /dʒəˈzaɪ.əh/ | Ezra 10:15 |  | unsure (guessed IPA) (0.25) |
| Shabbethai | Shabbethai | /ˈʃæb.bə.θeɪ/ | Ezra 10:15 |  | fine as spelled (0.83) |
| Elasah | Elasah | /ˈiː.lə.səh/ | Ezra 10:22 |  | unsure (guessed IPA) (0.50) |
| Kelaiah | Kelaiah | /kəˈleɪ.əh/ | Ezra 10:23 |  | unsure (guessed IPA) (0.67) |
| Kelita | Kelita | /ˈkiː.li.tə/ | Ezra 10:23 |  | unsure (guessed IPA) (0.50) |
| Izziah | Izziah | /ɪzˈzi.əh/ | Ezra 10:25 |  | fine as spelled (0.80) |
| Aziza | Aziza | /ˈeɪ.zi.zə/ | Ezra 10:27 |  | unsure (guessed IPA) (0.73) |
| Athlai | Athlai | /ˈeɪ.θleɪ/ | Ezra 10:28 |  | unsure (guessed IPA) (0.25) |
| Zabbai | Zabbai | /ˈzæb.beɪ/ | Ezra 10:28 |  | unsure (guessed IPA) (0.75) |
| Sheal | Sheal | /ˈʃiːl/ | Ezra 10:29 |  | unsure (guessed IPA) (0.75) |
| Chelal | kelal | /ˈkiː.ləl/ | Ezra 10:30 | ✅ | overridden (1.00) |
| Isshijah | Isshijah | /ˈɪs.ʃi.dʒəh/ | Ezra 10:31 |  | unsure (guessed IPA) (0.57) |
| Shimeon | Shimeon | /ˈʃi.mə.ən/ | Ezra 10:31 |  | unsure (guessed IPA) (0.58) |
| Jeremai | Jeremai | /ˈdʒiː.rə.meɪ/ | Ezra 10:33 |  | unsure (guessed IPA) (0.50) |
| Mattattah | Mattattah | /ˈmæt.tət.təh/ | Ezra 10:33 |  | unsure (guessed IPA) (0.43) |
| Mattenai | Mattenai | /ˈmæt.tə.neɪ/ | Ezra 10:33 |  | unsure (guessed IPA) (0.67) |
| Uel | Uel | /ˈjuː.əl/ | Ezra 10:34 |  | fine as spelled (1.00) |
| Bedeiah | Bedeiah | /bəˈdaɪ.əh/ | Ezra 10:35 |  | unsure (guessed IPA) (0.75) |
| Cheluhi | Cheluhi | /ˈkiː.lə.hə/ | Ezra 10:35 |  | unsure (guessed IPA) (0.50) |
| Jaasu | Jaasu | /ˈdʒeɪ.ə.sə/ | Ezra 10:37 |  | unsure (guessed IPA) (0.40) |
| Sharai | Sharai | /ˈʃeɪ.reɪ/ | Ezra 10:40 |  | unsure (guessed IPA) (0.50) |
| Shashai | Shashai | /ˈʃeɪ.ʃeɪ/ | Ezra 10:40 |  | unsure (guessed IPA) (0.25) |
| Zebina | Zebina | /ˈziː.bi.nə/ | Ezra 10:43 |  | fine as spelled (0.83) |
| Chislev | kislev | /ˈkɪs.ləv/ | Nehemiah 1:1 | ✅ | overridden (0.67) |
| Hacaliah | Hacaliah | /hə.səˈli.əh/ | Nehemiah 1:1 |  | unsure (guessed IPA) (0.50) |
| Shushan | Shushan | /ˈˈʃuːˌʃɑn/ | Nehemiah 1:1 |  | fine as spelled (0.80) |
| Nisan | Nisan | /ˈni.sən/ | Nehemiah 2:1 |  | fine as spelled (0.80) |
| Horonite | Horonite | /həˈroʊ.ni.tiː/ | Nehemiah 2:10 |  | unsure (guessed IPA) (0.50) |
| Sanballat | Sanballat | /ˈsæn.bəl.lət/ | Nehemiah 2:10 |  | unsure (guessed IPA) (0.62) |
| Ammontite | Ammontite | /əmˈmɒn.ti.tiː/ | Nehemiah 2:19 |  | unsure (guessed IPA) (0.50) |
| Arabian | Arabian | /ərˈeɪbiːən/ | Nehemiah 2:19 |  | fine as spelled (1.00) |
| Geshem | Geshem | /ˈɡiː.ʃəm/ | Nehemiah 2:19 |  | fine as spelled (0.80) |
| Hammeah | Hammeah | /ˈhæm.miːh/ | Nehemiah 3:1 |  | unsure (guessed IPA) (0.60) |
| Hananel | Hananel | /ˈheɪ.nə.nəl/ | Nehemiah 3:1 |  | fine as spelled (0.93) |
| Hassenaah | Hassenaah | /həsˈsiː.nə.əh/ | Nehemiah 3:3 |  | unsure (guessed IPA) (0.50) |
| Baana | Baana | /ˈbeɪ.ə.nə/ | Nehemiah 3:4 |  | unsure (guessed IPA) (0.60) |
| Meshezabel | Meshezabel | /məˈʃiː.zə.bəl/ | Nehemiah 3:4 |  | fine as spelled (0.89) |
| Tekoites | Tekoites | /ˈtiː.kɔɪ.təs/ | Nehemiah 3:5 |  | unsure (guessed IPA) (0.57) |
| Besodeiah | Besodeiah | /bə.səˈdaɪ.əh/ | Nehemiah 3:6 |  | unsure (guessed IPA) (0.56) |
| Jadon | Jadon | /ˈdʒeɪ.dən/ | Nehemiah 3:7 |  | fine as spelled (1.00) |
| Melatiah | Melatiah | /mə.ləˈti.əh/ | Nehemiah 3:7 |  | unsure (guessed IPA) (0.56) |
| Harhaiah | Harhaiah | /hərˈheɪ.əh/ | Nehemiah 3:8 |  | unsure (guessed IPA) (0.57) |
| Harumaph | Harumaph | /ˈheɪ.rə.məf/ | Nehemiah 3:10 |  | unsure (guessed IPA) (0.57) |
| Hashabneiah | Hashabneiah | /hə.ʃəbˈnaɪ.əh/ | Nehemiah 3:10 |  | unsure (guessed IPA) (0.67) |
| Hallohesh | Hallohesh | /ˈhæl.lə.həʃ/ | Nehemiah 3:12 |  | fine as spelled (0.86) |
| Haccherem | hackerem | /ˈhæs.kə.rəm/ | Nehemiah 3:14 | ✅ | overridden (0.81) |
| Colhozeh | Colhozeh | /ˈsɒl.hə.zəh/ | Nehemiah 3:15 |  | unsure (guessed IPA) (0.50) |
| Azbuk | Azbuk | /ˈæz.bək/ | Nehemiah 3:16 |  | fine as spelled (1.00) |
| Bavvai | Bavvai | /ˈbæv.veɪ/ | Nehemiah 3:18 |  | unsure (guessed IPA) (0.38) |
| Baruch | Baruch | /bɑrˈuːk/ | Nehemiah 3:20 |  | fine as spelled (0.80) |
| Ananiah | Ananiah | /ə.nəˈni.əh/ | Nehemiah 3:23 |  | unsure (guessed IPA) (0.71) |
| Uzai | Uzai | /ˈjuː.zeɪ/ | Nehemiah 3:25 |  | unsure (guessed IPA) (0.75) |
| Zalaph | Zalaph | /ˈzeɪ.ləf/ | Nehemiah 3:30 |  | fine as spelled (0.80) |
| Hammiphkad | Hammiphkad | /ˈhæm.mi.fkəd/ | Nehemiah 3:31 |  | unsure (guessed IPA) (0.50) |
| Gashmu | Gashmu | /ˈɡeɪ.ʃmə/ | Nehemiah 6:6 |  | unsure (guessed IPA) (0.70) |
| Elul | Elul | /ˈiː.ləl/ | Nehemiah 6:15 |  | unsure (guessed IPA) (0.25) |
| Mispereth | Mispereth | /ˈmɪs.pə.rəθ/ | Nehemiah 7:7 |  | fine as spelled (0.81) |
| Nahamani | Nahamani | /nəˈheɪ.mə.nə/ | Nehemiah 7:7 |  | unsure (guessed IPA) (0.38) |
| Nehum | Nehum | /ˈniː.hjuːm/ | Nehemiah 7:7 |  | unsure (guessed IPA) (0.50) |
| Raamiah | Raamiah | /rə.əˈmi.əh/ | Nehemiah 7:7 |  | unsure (guessed IPA) (0.57) |
| Hariph | Hariph | /ˈheɪ.rɪf/ | Nehemiah 7:24 |  | fine as spelled (0.80) |
| Hodevah | Hodevah | /ˈhoʊ.də.vəh/ | Nehemiah 7:43 |  | unsure (guessed IPA) (0.71) |
| Sia | Sia | /ˈsi.ə/ | Nehemiah 7:47 |  | fine as spelled (0.88) |
| Hagaba | Hagaba | /ˈheɪ.ɡə.bə/ | Nehemiah 7:48 |  | unsure (guessed IPA) (0.58) |
| Lebana | Lebana | /ˈliː.bə.nə/ | Nehemiah 7:48 |  | unsure (guessed IPA) (0.67) |
| Salmai | Salmai | /ˈsæl.meɪ/ | Nehemiah 7:48 |  | unsure (guessed IPA) (0.50) |
| Nephushesim | Nephushesim | /nəˈfjuː.ʃə.sɪm/ | Nehemiah 7:52 |  | unsure (guessed IPA) (0.60) |
| Bazlith | Bazlith | /ˈbæz.lɪθ/ | Nehemiah 7:54 |  | fine as spelled (1.00) |
| Perida | Perida | /ˈpiː.ri.də/ | Nehemiah 7:57 |  | fine as spelled (0.83) |
| Sophereth | Sophereth | /ˈsoʊ.fə.rəθ/ | Nehemiah 7:57 |  | unsure (guessed IPA) (0.71) |
| Jaala | Jaala | /ˈdʒeɪ.ə.lə/ | Nehemiah 7:58 |  | unsure (guessed IPA) (0.50) |
| Addon | Addon | /ˈæd.dən/ | Nehemiah 7:61 |  | fine as spelled (1.00) |
| Hobaiah | Hobaiah | /həˈbeɪ.əh/ | Nehemiah 7:63 |  | unsure (guessed IPA) (0.50) |
| Anaiah | Anaiah | /əˈneɪ.əh/ | Nehemiah 8:4 |  | unsure (guessed IPA) (0.60) |
| Hashbaddanah | Hashbaddanah | /həˈʃbæd.də.nəh/ | Nehemiah 8:4 |  | unsure (guessed IPA) (0.55) |
| Bunni | Bunni | /bˈuːniː/ | Nehemiah 9:4 |  | fine as spelled (1.00) |
| Chenani | kenani | /ˈkiː.nə.nə/ | Nehemiah 9:4 | ✅ | overridden (0.50) |
| Ginnethon | Ginnethon | /ˈɡɪn.nə.θən/ | Nehemiah 10:6 |  | unsure (guessed IPA) (0.57) |
| Bilgai | Bilgai | /ˈbɪl.ɡeɪ/ | Nehemiah 10:8 |  | fine as spelled (0.80) |
| Azaniah | Azaniah | /ə.zəˈni.əh/ | Nehemiah 10:9 |  | unsure (guessed IPA) (0.57) |
| Beninu | Beninu | /ˈbiː.ni.nə/ | Nehemiah 10:13 |  | unsure (guessed IPA) (0.67) |
| Azzur | Azzur | /ˈæz.zər/ | Nehemiah 10:17 |  | fine as spelled (1.00) |
| Nobai | Nobai | /ˈnoʊ.beɪ/ | Nehemiah 10:19 |  | unsure (guessed IPA) (0.75) |
| Jaddua | Jaddua | /ˈdʒæd.də.ə/ | Nehemiah 10:21 |  | unsure (guessed IPA) (0.55) |
| Pilha | Pilha | /ˈpɪl.hə/ | Nehemiah 10:24 |  | fine as spelled (0.92) |
| Shobek | Shobek | /ˈʃoʊ.bək/ | Nehemiah 10:24 |  | fine as spelled (0.80) |
| Hashabnah | Hashabnah | /ˈheɪ.ʃəb.nəh/ | Nehemiah 10:25 |  | unsure (guessed IPA) (0.56) |
| Anan | Anan | /ˈeɪ.nən/ | Nehemiah 10:26 |  | fine as spelled (1.00) |
| Hazaiah | Hazaiah | /həˈzeɪ.əh/ | Nehemiah 11:5 |  | unsure (guessed IPA) (0.67) |
| Ithiel | Ithiel | /ˈi.θaɪl/ | Nehemiah 11:7 |  | unsure (guessed IPA) (0.33) |
| Joed | Joed | /ˈdʒoʊd/ | Nehemiah 11:7 |  | fine as spelled (1.00) |
| Kolaiah | Kolaiah | /kəˈleɪ.əh/ | Nehemiah 11:7 |  | unsure (guessed IPA) (0.67) |
| Gabbai | Gabbai | /ˈɡæb.beɪ/ | Nehemiah 11:8 |  | unsure (guessed IPA) (0.75) |
| Sallai | Sallai | /ˈsæl.leɪ/ | Nehemiah 11:8 |  | unsure (guessed IPA) (0.75) |
| Pelaliah | Pelaliah | /pə.ləˈli.əh/ | Nehemiah 11:12 |  | unsure (guessed IPA) (0.62) |
| Ahzai | Ahzai | /ˈeɪ.zeɪ/ | Nehemiah 11:13 |  | unsure (guessed IPA) (0.00) |
| Amashsai | Amashsai | /ˈeɪ.mə.ʃseɪ/ | Nehemiah 11:13 |  | unsure (guessed IPA) (0.46) |
| Haggedolim | Haggedolim | /həɡˈɡiː.də.lɪm/ | Nehemiah 11:14 |  | unsure (guessed IPA) (0.78) |
| Bakbukiah | Bakbukiah | /bək.bəˈki.əh/ | Nehemiah 11:17 |  | unsure (guessed IPA) (0.72) |
| Gishpa | Gishpa | /ˈɡi.ʃpə/ | Nehemiah 11:21 |  | unsure (guessed IPA) (0.70) |
| Jekabzeel | Jekabzeel | /ˈdʒiː.kəb.ziːl/ | Nehemiah 11:25 |  | fine as spelled (0.81) |
| Meconah | Meconah | /ˈmiː.sə.nəh/ | Nehemiah 11:28 |  | unsure (guessed IPA) (0.43) |
| Aija | Aija | /ˈeɪ.dʒə/ | Nehemiah 11:31 |  | unsure (guessed IPA) (0.67) |
| Neballat | Neballat | /ˈniː.bəl.lət/ | Nehemiah 11:34 |  | unsure (guessed IPA) (0.57) |
| Ginnethoi | Ginnethoi | /ˈɡɪn.nə.θɔɪ/ | Nehemiah 12:4 |  | unsure (guessed IPA) (0.57) |
| Maadiah | Maadiah | /mə.əˈdi.əh/ | Nehemiah 12:5 |  | unsure (guessed IPA) (0.57) |
| Amok | Amok | /əmˈək/ | Nehemiah 12:7 |  | fine as spelled (1.00) |
| Unno | Unno | /ˈʌn.nə/ | Nehemiah 12:9 |  | unsure (guessed IPA) (0.58) |
| Joiada | Joiada | /ˈdʒɔɪ.ə.də/ | Nehemiah 12:10 |  | unsure (guessed IPA) (0.50) |
| Joiakim | Joiakim | /ˈdʒɔɪ.ə.kɪm/ | Nehemiah 12:10 |  | unsure (guessed IPA) (0.67) |
| Meraiah | Meraiah | /məˈreɪ.əh/ | Nehemiah 12:12 |  | unsure (guessed IPA) (0.67) |
| Malluchi | malluki | /ˈmæl.lə.kə/ | Nehemiah 12:14 | ✅ | overridden (0.50) |
| Adna | Adna | /ˈæd.nə/ | Nehemiah 12:15 |  | fine as spelled (0.90) |
| Helkai | Helkai | /ˈhɛl.keɪ/ | Nehemiah 12:15 |  | unsure (guessed IPA) (0.50) |
| Moadiah | Moadiah | /moʊˈdi.əh/ | Nehemiah 12:17 |  | unsure (guessed IPA) (0.46) |
| Piltai | Piltai | /ˈpɪl.teɪ/ | Nehemiah 12:17 |  | fine as spelled (0.80) |
| Kallai | Kallai | /ˈkæl.leɪ/ | Nehemiah 12:20 |  | unsure (guessed IPA) (0.50) |
| Persian | Persian | /pˈɚʒən/ | Nehemiah 12:22 |  | fine as spelled (0.83) |
| Hoshaiah | Hoshaiah | /həˈʃeɪ.əh/ | Nehemiah 12:32 |  | unsure (guessed IPA) (0.58) |
| Gilalai | Gilalai | /ˈɡi.lə.leɪ/ | Nehemiah 12:36 |  | unsure (guessed IPA) (0.67) |
| Maai | Maai | /ˈmeɪ.eɪ/ | Nehemiah 12:36 |  | unsure (guessed IPA) (0.33) |
| Milalai | Milalai | /ˈmi.lə.leɪ/ | Nehemiah 12:36 |  | unsure (guessed IPA) (0.50) |
| Jezrahiah | Jezrahiah | /dʒəz.rəˈhi.əh/ | Nehemiah 12:42 |  | unsure (guessed IPA) (0.67) |
| India | India | /ˈɪndiːə/ | Esther 1:1 |  | fine as spelled (1.00) |
| Vashti | Vashti | /vˈæʃtiː/ | Esther 1:9 |  | fine as spelled (1.00) |
| Abagtha | Abagtha | /ˈeɪ.bəɡ.θə/ | Esther 1:10 |  | unsure (guessed IPA) (0.62) |
| Bigtha | Bigtha | /ˈbɪɡ.θə/ | Esther 1:10 |  | unsure (guessed IPA) (0.70) |
| Biztha | Biztha | /ˈbɪz.θə/ | Esther 1:10 |  | unsure (guessed IPA) (0.70) |
| Harbona | Harbona | /ˈhær.bə.nə/ | Esther 1:10 |  | unsure (guessed IPA) (0.71) |
| Mehuman | Mehuman | /ˈmiː.hə.mən/ | Esther 1:10 |  | unsure (guessed IPA) (0.67) |
| Zethar | Zethar | /ˈziː.θər/ | Esther 1:10 |  | fine as spelled (1.00) |
| Admatha | Admatha | /ˈæd.mə.θə/ | Esther 1:14 |  | fine as spelled (0.92) |
| Carshena | Carshena | /ˈsær.ʃə.nə/ | Esther 1:14 |  | unsure (guessed IPA) (0.50) |
| Marsena | Marsena | /ˈmær.sə.nə/ | Esther 1:14 |  | unsure (guessed IPA) (0.71) |
| Memucan | Memucan | /ˈmiː.mə.sən/ | Esther 1:14 |  | unsure (guessed IPA) (0.50) |
| Meres | Meres | /ˈmiː.rəs/ | Esther 1:14 |  | unsure (guessed IPA) (0.45) |
| Shethar | Shethar | /ˈʃiː.θər/ | Esther 1:14 |  | fine as spelled (0.80) |
| Persians | Persians | /pˈɚʒənz/ | Esther 1:19 |  | fine as spelled (0.86) |
| Hegai | Hegai | /ˈhiː.ɡeɪ/ | Esther 2:3 |  | unsure (guessed IPA) (0.50) |
| Susa | Susa | /sˈuːsə/ | Esther 2:3 |  | fine as spelled (0.88) |
| Jew | Jew | /dʒˈuː/ | Esther 2:5 |  | fine as spelled (1.00) |
| Esther | Esther | /ˈɛstɚ/ | Esther 2:7 |  | fine as spelled (1.00) |
| Hadassah | Hadassah | /həˈdæsə/ | Esther 2:7 |  | still wrong (0.73) |
| Shaashgaz | Shaashgaz | /ˈʃeɪ.ə.ʃɡəz/ | Esther 2:14 |  | unsure (guessed IPA) (0.57) |
| Tebeth | Tebeth | /ˈtiː.bəθ/ | Esther 2:16 |  | unsure (guessed IPA) (0.40) |
| Bigthan | Bigthan | /ˈbɪɡ.θən/ | Esther 2:21 |  | unsure (guessed IPA) (0.67) |
| Teresh | Teresh | /ˈtiː.rəʃ/ | Esther 2:21 |  | unsure (guessed IPA) (0.60) |
| Agagite | Agagite | /əˈɡeɪ.ɡi.tiː/ | Esther 3:1 |  | unsure (guessed IPA) (0.29) |
| Haman | Haman | /hˈeɪmən/ | Esther 3:1 |  | fine as spelled (1.00) |
| Hammedatha | Hammedatha | /həmˈmiː.də.θə/ | Esther 3:1 |  | unsure (guessed IPA) (0.59) |
| Pur | Pur | /pˈɚ/ | Esther 3:7 |  | fine as spelled (0.83) |
| Hathach | Hathach | /ˈheɪ.θək/ | Esther 4:5 |  | unsure (guessed IPA) (0.31) |
| Zeresh | Zeresh | /ˈziː.rəʃ/ | Esther 5:10 |  | fine as spelled (0.80) |
| Bigthana | Bigthana | /ˈbɪɡ.θə.nə/ | Esther 6:2 |  | unsure (guessed IPA) (0.73) |
| Jewish | Jewish | /dʒˈuːɪʃ/ | Esther 6:13 |  | fine as spelled (1.00) |
| Harbonah | Harbonah | /ˈhær.bə.nəh/ | Esther 7:9 |  | unsure (guessed IPA) (0.62) |
| Sivan | Sivan | /ˈsi.vən/ | Esther 8:9 |  | unsure (guessed IPA) (0.55) |
| Aspatha | Aspatha | /ˈæs.pə.θə/ | Esther 9:7 |  | unsure (guessed IPA) (0.75) |
| Dalphon | Dalphon | /ˈdæl.fən/ | Esther 9:7 |  | fine as spelled (0.83) |
| Parshandatha | Parshandatha | /pərˈʃæn.də.θə/ | Esther 9:7 |  | fine as spelled (0.80) |
| Adalia | Adalia | /ɑdˈɑliːə/ | Esther 9:8 |  | still wrong (0.62) |
| Aridatha | Aridatha | /əˈri.də.θə/ | Esther 9:8 |  | unsure (guessed IPA) (0.79) |
| Aridai | Aridai | /ˈeɪ.ri.deɪ/ | Esther 9:9 |  | unsure (guessed IPA) (0.55) |
| Arisai | Arisai | /ˈeɪ.ri.seɪ/ | Esther 9:9 |  | unsure (guessed IPA) (0.60) |
| Vaizatha | Vaizatha | /ˈveɪ.zə.θə/ | Esther 9:9 |  | unsure (guessed IPA) (0.62) |
| Purim | Purim | /pˈʊrəm/ | Esther 9:26 |  | fine as spelled (0.80) |
| Job | Job | /dʒˈɑb/ | Job 1:1 |  | fine as spelled (1.00) |
| Sabeans | Sabeans | /ˈseɪ.biːns/ | Job 1:15 |  | unsure (guessed IPA) (0.57) |
| Bildad | Bildad | /ˈbɪl.dəd/ | Job 2:11 |  | fine as spelled (0.83) |
| Naamathite | Naamathite | /nə.əˈmeɪ.θi.tiː/ | Job 2:11 |  | unsure (guessed IPA) (0.44) |
| Shuhite | Shuhite | /ˈʃjuː.hi.tiː/ | Job 2:11 |  | unsure (guessed IPA) (0.43) |
| Temanite | Temanite | /təˈmeɪ.ni.tiː/ | Job 2:11 |  | unsure (guessed IPA) (0.50) |
| Zophar | Zophar | /ˈzoʊ.fər/ | Job 2:11 |  | fine as spelled (1.00) |
| Orion | Orion | /oʊrˈaɪən/ | Job 9:9 |  | still wrong (0.63) |
| Pleiades | Pleiades | /plˈiːədiːz/ | Job 9:9 |  | fine as spelled (0.86) |
| Abaddon | Abaddon | /əˈbæ.dn̩/ | Job 26:6 |  | fine as spelled (0.83) |
| Barachel | barakel | /ˈbeɪ.rə.kəl/ | Job 32:2 | ✅ | overridden (0.71) |
| Buzite | Buzite | /ˈbjuː.zi.tiː/ | Job 32:2 |  | unsure (guessed IPA) (0.64) |
| Happuch | Happuch | /ˈhæp.pək/ | Job 42:14 |  | unsure (guessed IPA) (0.70) |
| Jemimah | Jemimah | /dʒɛmˈaɪmə/ | Job 42:14 |  | fine as spelled (0.83) |
| Keren | Keren | /kˈɛrɛn/ | Job 42:14 |  | still wrong (0.70) |
| Keziah | Keziah | /kəzˈiːə/ | Job 42:14 |  | fine as spelled (0.80) |
| Mizar | Mizar | /mˈaɪzɑr/ | Psalms 42:6 |  | fine as spelled (1.00) |
| Yah | Yah | /jˈɑ/ | Psalms 68:4 |  | still wrong (0.75) |
| Melchizedek | Melchizedek | /mɛkˈiːzɛdɛk/ | Psalms 110:4 |  | still wrong (0.41) |
| Negev | Negev | /nˈɛɡɛv/ | Psalms 126:4 |  | still wrong (0.50) |
| Jaar | Jaar | /ˈdʒeɪ.ər/ | Psalms 132:6 |  | unsure (guessed IPA) (0.50) |
| Agur | Agur | /ˈeɪ.ɡər/ | Proverbs 30:1 |  | unsure (guessed IPA) (0.62) |
| Jakeh | Jakeh | /ˈdʒeɪ.kəh/ | Proverbs 30:1 |  | unsure (guessed IPA) (0.70) |
| Ucal | Ucal | /ˈjuː.səl/ | Proverbs 30:1 |  | fine as spelled (0.80) |
| Lemuel | Lemuel | /ˈlɛm.jə(wə)l/ | Proverbs 31:1 |  | still wrong (0.55) |
| Creator | Creator | /kriːˈeɪtɚ/ | Ecclesiastes 12:1 |  | fine as spelled (0.86) |
| Bether | Bether | /ˈbiː.θər/ | Song of Solomon 2:17 |  | unsure (guessed IPA) (0.60) |
| Amana | Amana | /əmˈænə/ | Song of Solomon 4:8 |  | fine as spelled (0.92) |
| Shulammite | Shulammite | /ʃəˈlæm.mi.tiː/ | Song of Solomon 6:13 |  | unsure (guessed IPA) (0.50) |
| Bathrabbim | Bathrabbim | /ˈbeɪ.θrəb.bɪm/ | Song of Solomon 7:4 |  | unsure (guessed IPA) (0.56) |
| Hamon | Hamon | /hˈæmən/ | Song of Solomon 8:11 |  | fine as spelled (0.90) |
| Shearjashub | Shearjashub | /ˈʃiːr.dʒə.ʃəb/ | Isaiah 7:3 |  | unsure (guessed IPA) (0.69) |
| Immanuel | Immanuel | /ˈɪmənʊl/ | Isaiah 7:14 |  | still wrong (0.59) |
| Baz | Baz | /bˈæz/ | Isaiah 8:1 |  | fine as spelled (1.00) |
| Hash | Hash | /hˈæʃ/ | Isaiah 8:1 |  | fine as spelled (1.00) |
| Maher | Maher | /mˈɑr/ | Isaiah 8:1 |  | fine as spelled (1.00) |
| Shalal | Shalal | /ˈʃeɪ.ləl/ | Isaiah 8:1 |  | unsure (guessed IPA) (0.40) |
| Jeberechiah | Jeberechiah | /dʒə.bə.rəˈki.əh/ | Isaiah 8:2 |  | unsure (guessed IPA) (0.75) |
| Shiloah | Shiloah | /ˈʃi.loʊh/ | Isaiah 8:6 |  | unsure (guessed IPA) (0.60) |
| Assyrian | Assyrian | /əsˈɪriːən/ | Isaiah 10:5 |  | fine as spelled (1.00) |
| Calno | Calno | /ˈsæl.nə/ | Isaiah 10:9 |  | unsure (guessed IPA) (0.30) |
| Aiath | Aiath | /ˈeɪ.əθ/ | Isaiah 10:28 |  | unsure (guessed IPA) (0.17) |
| Laishah | Laishah | /ˈleɪ.ʃəh/ | Isaiah 10:30 |  | unsure (guessed IPA) (0.40) |
| Gebim | Gebim | /ˈɡiː.bɪm/ | Isaiah 10:31 |  | unsure (guessed IPA) (0.40) |
| Pathros | Pathros | /ˈpeɪ.θrəs/ | Isaiah 11:11 |  | unsure (guessed IPA) (0.25) |
| Bayith | Bayith | /ˈbeɪ.ɪθ/ | Isaiah 15:2 |  | fine as spelled (1.00) |
| Eglath | Eglath | /ˈɛɡ.ləθ/ | Isaiah 15:5 |  | unsure (guessed IPA) (0.40) |
| Horonaim | Horonaim | /ˈhoʊ.rə.neɪm/ | Isaiah 15:5 |  | unsure (guessed IPA) (0.79) |
| Luhith | Luhith | /ˈljuː.hɪθ/ | Isaiah 15:5 |  | unsure (guessed IPA) (0.58) |
| Shelishiyah | Shelishiyah | /ʃə.liˈʃi.ə.əh/ | Isaiah 15:5 |  | unsure (guessed IPA) (0.56) |
| Nimrim | Nimrim | /ˈnɪm.rɪm/ | Isaiah 15:6 |  | fine as spelled (0.83) |
| Eglaim | Eglaim | /ˈɛɡ.leɪm/ | Isaiah 15:8 |  | fine as spelled (0.80) |
| Dimon | Dimon | /dˈɪmən/ | Isaiah 15:9 |  | still wrong (0.67) |
| Memphis | Memphis | /mˈɛmfəs/ | Isaiah 19:13 |  | fine as spelled (0.83) |
| Sargon | Sargon | /ˈsær.ɡən/ | Isaiah 20:1 |  | fine as spelled (0.83) |
| Dedanites | Dedanites | /dəˈdeɪ.ni.təs/ | Isaiah 21:13 |  | unsure (guessed IPA) (0.56) |
| Hanes | Hanes | /hˈeɪnz/ | Isaiah 30:4 |  | fine as spelled (1.00) |
| Aramaic | Aramaic | /ɑrɑmˈɛjɪk/ | Isaiah 36:11 |  | still wrong (0.50) |
| Merodach | Merodach | /ˈmiː.rə.dək/ | Isaiah 39:1 |  | unsure (guessed IPA) (0.57) |
| Sinim | Sinim | /ˈsi.nɪm/ | Isaiah 49:12 |  | unsure (guessed IPA) (0.60) |
| Repairer | Repairer | /ˈriː.peɪ.rər/ | Isaiah 58:12 |  | unsure (guessed IPA) (0.71) |
| Restorer | Restorer | /rɪstˈɔrɚ/ | Isaiah 58:12 |  | fine as spelled (0.88) |
| Beulah | Beulah | /bjˈuːlə/ | Isaiah 62:4 |  | fine as spelled (0.80) |
| Destiny | Destiny | /dˈɛstəniː/ | Isaiah 65:11 |  | fine as spelled (1.00) |
| Fortune | Fortune | /fˈɔrtʃən/ | Isaiah 65:11 |  | fine as spelled (1.00) |
| Tahpanhes | Tahpanhes | /ˈteɪ.pən.həs/ | Jeremiah 2:16 |  | unsure (guessed IPA) (0.50) |
| Uphaz | Uphaz | /ˈjuː.fəz/ | Jeremiah 10:9 |  | unsure (guessed IPA) (0.20) |
| Harsith | Harsith | /ˈhær.sɪθ/ | Jeremiah 19:2 |  | unsure (guessed IPA) (0.33) |
| Magormissabib | Magormissabib | /mə.ɡərˈmɪs.sə.bɪb/ | Jeremiah 20:3 |  | fine as spelled (0.92) |
| Coniah | Coniah | /səˈni.əh/ | Jeremiah 22:24 |  | unsure (guessed IPA) (0.50) |
| Sheshach | Sheshach | /ˈʃiː.ʃək/ | Jeremiah 25:26 |  | unsure (guessed IPA) (0.60) |
| Morashtite | Morashtite | /məˈreɪ.ʃti.tiː/ | Jeremiah 26:18 |  | unsure (guessed IPA) (0.56) |
| Gemariah | Gemariah | /ɡə.məˈri.əh/ | Jeremiah 29:3 |  | unsure (guessed IPA) (0.50) |
| Nehelamite | Nehelamite | /nə.həˈleɪ.mi.tiː/ | Jeremiah 29:24 |  | unsure (guessed IPA) (0.50) |
| Goah | Goah | /ˈɡoʊh/ | Jeremiah 31:39 |  | unsure (guessed IPA) (0.67) |
| Hanamel | Hanamel | /ˈheɪ.nə.məl/ | Jeremiah 32:7 |  | unsure (guessed IPA) (0.71) |
| Mahseiah | Mahseiah | /məˈsaɪ.əh/ | Jeremiah 32:12 |  | unsure (guessed IPA) (0.67) |
| Neriah | Neriah | /nəˈri.əh/ | Jeremiah 32:12 |  | unsure (guessed IPA) (0.67) |
| Hebrewess | Hebrewess | /ˈhɛb.rə.wəss/ | Jeremiah 34:9 |  | unsure (guessed IPA) (0.44) |
| Rechabites | Rechabites | /ˈrɛkəbaɪts/ | Jeremiah 35:2 |  | fine as spelled (1.00) |
| Habazziniah | Habazziniah | /hə.bəz.ziˈni.əh/ | Jeremiah 35:3 |  | unsure (guessed IPA) (0.60) |
| Igdaliah | Igdaliah | /ɪɡ.dəˈli.əh/ | Jeremiah 35:4 |  | unsure (guessed IPA) (0.56) |
| Cushi | Cushi | /ˈsjuː.ʃə/ | Jeremiah 36:14 |  | unsure (guessed IPA) (0.40) |
| Jehudi | Jehudi | /ˈdʒiː.hə.də/ | Jeremiah 36:14 |  | unsure (guessed IPA) (0.50) |
| Abdeel | Abdeel | /ˈæb.diːl/ | Jeremiah 36:26 |  | unsure (guessed IPA) (0.70) |
| Jehucal | Jehucal | /ˈdʒiː.hə.səl/ | Jeremiah 37:3 |  | unsure (guessed IPA) (0.50) |
| Irijah | Irijah | /ˈi.ri.dʒəh/ | Jeremiah 37:13 |  | unsure (guessed IPA) (0.67) |
| Jucal | Jucal | /ˈdʒjuː.səl/ | Jeremiah 38:1 |  | unsure (guessed IPA) (0.67) |
| Ebedmelech | Ebedmelech | /əˈbɛd.mə.lək/ | Jeremiah 38:7 |  | fine as spelled (0.89) |
| Rabmag | Rabmag | /ˈræb.məɡ/ | Jeremiah 39:3 |  | unsure (guessed IPA) (0.62) |
| Samgarnebo | Samgarnebo | /səmˈɡær.nə.bə/ | Jeremiah 39:3 |  | unsure (guessed IPA) (0.55) |
| Sarsechim | Sarsechim | /ˈsær.sə.kɪm/ | Jeremiah 39:3 |  | unsure (guessed IPA) (0.75) |
| Nebushazban | Nebushazban | /nəˈbjuː.ʃəz.bən/ | Jeremiah 39:13 |  | unsure (guessed IPA) (0.68) |
| Ephai | Ephai | /ˈiː.feɪ/ | Jeremiah 40:8 |  | unsure (guessed IPA) (0.67) |
| Jezaniah | Jezaniah | /dʒə.zəˈni.əh/ | Jeremiah 40:8 |  | unsure (guessed IPA) (0.62) |
| Baalis | Baalis | /ˈbeɪ.ə.lɪs/ | Jeremiah 40:14 |  | unsure (guessed IPA) (0.33) |
| Geruth | Geruth | /ˈɡiː.rəθ/ | Jeremiah 41:17 |  | unsure (guessed IPA) (0.40) |
| Hophra | Hophra | /ˈhoʊ.frə/ | Jeremiah 44:30 |  | unsure (guessed IPA) (0.60) |
| Madmen | Madmen | /mˈædmən/ | Jeremiah 48:2 |  | fine as spelled (1.00) |
| Bel | Bel | /bˈɛl/ | Jeremiah 50:2 |  | fine as spelled (1.00) |
| Merathaim | Merathaim | /ˈmiː.rə.θeɪm/ | Jeremiah 50:21 |  | unsure (guessed IPA) (0.71) |
| Pekod | Pekod | /ˈpiː.kəd/ | Jeremiah 50:21 |  | fine as spelled (0.80) |
| Lebkamai | Lebkamai | /ˈlɛb.kə.meɪ/ | Jeremiah 51:1 |  | unsure (guessed IPA) (0.64) |
| Chaldea | Chaldea | /ˈkæl.diː/ | Jeremiah 51:24 |  | fine as spelled (0.83) |
| Minni | Minni | /ˈmɪn.nə/ | Jeremiah 51:27 |  | unsure (guessed IPA) (0.50) |
| Chebar | kebar | /ˈkiː.bər/ | Ezekiel 1:1 | ✅ | overridden (0.50) |
| Buzi | Buzi | /ˈbjuː.zə/ | Ezekiel 1:3 |  | fine as spelled (0.80) |
| Ezekiel | Ezekiel | /ˈɛzɪkiːl/ | Ezekiel 1:3 |  | still wrong (0.50) |
| Aviv | Aviv | /ɑvˈiːv/ | Ezekiel 3:15 |  | still wrong (0.75) |
| Diblah | Diblah | /ˈdɪb.ləh/ | Ezekiel 6:14 |  | fine as spelled (0.83) |
| Tammuz | Tammuz | /ˈtæm.məz/ | Ezekiel 8:14 |  | unsure (guessed IPA) (0.60) |
| Bamah | Bamah | /ˈbeɪ.məh/ | Ezekiel 20:29 |  | unsure (guessed IPA) (0.60) |
| Oholah | Oholah | /ˈoʊ.hə.ləh/ | Ezekiel 23:4 |  | unsure (guessed IPA) (0.67) |
| Oholibah | Oholibah | /əˈhoʊ.li.bəh/ | Ezekiel 23:4 |  | unsure (guessed IPA) (0.50) |
| Koa | Koa | /ˈkoʊ/ | Ezekiel 23:23 |  | unsure (guessed IPA) (0.50) |
| Shoa | Shoa | /ˈʃoʊ/ | Ezekiel 23:23 |  | unsure (guessed IPA) (0.67) |
| Arvad | Arvad | /ɑrvˈæd/ | Ezekiel 27:8 |  | fine as spelled (0.90) |
| Gebal | Gebal | /ˈɡiː.bəl/ | Ezekiel 27:9 |  | fine as spelled (0.80) |
| Helbon | Helbon | /ˈhɛl.bən/ | Ezekiel 27:18 |  | fine as spelled (0.83) |
| Canneh | Canneh | /ˈsæn.nəh/ | Ezekiel 27:23 |  | unsure (guessed IPA) (0.50) |
| Chilmad | kilmad | /ˈkɪl.məd/ | Ezekiel 27:23 | ✅ | overridden (0.83) |
| Seveneh | Seveneh | /ˈsiː.və.nəh/ | Ezekiel 29:10 |  | unsure (guessed IPA) (0.71) |
| Pibeseth | Pibeseth | /ˈpi.bə.səθ/ | Ezekiel 30:17 |  | unsure (guessed IPA) (0.43) |
| Tehaphnehes | Tehaphnehes | /təˈheɪ.fnə.həs/ | Ezekiel 30:18 |  | unsure (guessed IPA) (0.50) |
| Hethlon | Hethlon | /ˈhiː.θlən/ | Ezekiel 47:15 |  | unsure (guessed IPA) (0.58) |
| Berothah | Berothah | /ˈbiː.rə.θəh/ | Ezekiel 47:16 |  | unsure (guessed IPA) (0.57) |
| Hatticon | Hatticon | /ˈhæt.ti.sən/ | Ezekiel 47:16 |  | unsure (guessed IPA) (0.57) |
| Hauran | Hauran | /ˈhɔː.rən/ | Ezekiel 47:16 |  | fine as spelled (0.90) |
| Sibraim | Sibraim | /ˈsɪb.reɪm/ | Ezekiel 47:16 |  | fine as spelled (1.00) |
| Enon | Enon | /ˈiː.nən/ | Ezekiel 47:17 |  | unsure (guessed IPA) (0.75) |
| Meriboth | Meriboth | /ˈmiː.ri.bəθ/ | Ezekiel 47:19 |  | unsure (guessed IPA) (0.57) |
| Meribath | Meribath | /ˈmiː.ri.bəθ/ | Ezekiel 48:28 |  | unsure (guessed IPA) (0.57) |
| Ashpenaz | Ashpenaz | /ˈeɪ.ʃpə.nəz/ | Daniel 1:3 |  | unsure (guessed IPA) (0.64) |
| Abednego | Abednego | /əˈbɛd.nə.ɡə/ | Daniel 1:7 |  | fine as spelled (0.81) |
| Belteshazzar | Belteshazzar | /bəlˈtiː.ʃəz.zər/ | Daniel 1:7 |  | unsure (guessed IPA) (0.70) |
| Meshach | Meshach | /ˈmi.ʃæk/ | Daniel 1:7 |  | still wrong (0.70) |
| Shadrach | Shadrach | /ˈʃæd.rək/ | Daniel 1:7 |  | unsure (guessed IPA) (0.75) |
| Dura | Dura | /dˈʊrə/ | Daniel 3:1 |  | still wrong (0.50) |
| Belshazzar | Belshazzar | /ˈbɛl.ʃəz.zər/ | Daniel 5:1 |  | unsure (guessed IPA) (0.75) |
| MENE | MENE | /ˈmiː.niː/ | Daniel 5:25 |  | unsure (guessed IPA) (0.67) |
| TEKEL | TEKEL | /ˈtiː.kəl/ | Daniel 5:25 |  | fine as spelled (0.80) |
| UPHARSIN | UPHARSIN | /ˈjuː.fər.sɪn/ | Daniel 5:25 |  | unsure (guessed IPA) (0.38) |
| Mede | Mede | /miːd/ | Daniel 5:31 |  | fine as spelled (1.00) |
| Ulai | Ulai | /ˈjuː.leɪ/ | Daniel 8:2 |  | unsure (guessed IPA) (0.25) |
| Libyans | Libyans | /lˈɪbiːənz/ | Daniel 11:43 |  | fine as spelled (0.93) |
| Hosea | Hosea | /hoʊsˈiːə/ | Hosea 1:1 |  | still wrong (0.60) |
| Diblaim | Diblaim | /ˈdɪb.leɪm/ | Hosea 1:3 |  | unsure (guessed IPA) (0.67) |
| Lo-Ruhamah | Lo-Ruhamah | /ˈloʊ.ˈrjuː.hə.məh/ | Hosea 1:6 |  | unsure (guessed IPA) (0.60) |
| Lo-Ammi | Lo-Ammi | /ˈloʊ.ˈæm.mə/ | Hosea 1:9 |  | unsure (guessed IPA) (0.60) |
| Jareb | Jareb | /ˈdʒeɪ.rəb/ | Hosea 5:13 |  | unsure (guessed IPA) (0.60) |
| Arbel | Arbel | /ˈɑrbəl/ | Hosea 10:14 |  | fine as spelled (0.80) |
| Shalman | Shalman | /ˈʃæl.mən/ | Hosea 10:14 |  | unsure (guessed IPA) (0.67) |
| Pethuel | Pethuel | /ˈpiː.θə.əl/ | Joel 1:1 |  | unsure (guessed IPA) (0.50) |
| Greeks | Greeks | /ɡrˈiːks/ | Joel 3:6 |  | fine as spelled (1.00) |
| Nazirites | Nazirites | /nəˈzi.ri.təs/ | Amos 2:11 |  | unsure (guessed IPA) (0.56) |
| Harmon | Harmon | /hˈɑrmən/ | Amos 4:3 |  | fine as spelled (1.00) |
| Sepharad | Sepharad | /ˈsɛfəræd/ | Obadiah 1:20 |  | fine as spelled (0.86) |
| Shaphir | Shaphir | /ˈʃeɪ.fɪr/ | Micah 1:11 |  | unsure (guessed IPA) (0.63) |
| Zaanan | Zaanan | /ˈzeɪ.ə.nən/ | Micah 1:11 |  | unsure (guessed IPA) (0.58) |
| Maroth | Maroth | /ˈmeɪ.rəθ/ | Micah 1:12 |  | unsure (guessed IPA) (0.40) |
| Moresheth | Moresheth | /ˈmoʊ.rə.ʃəθ/ | Micah 1:14 |  | unsure (guessed IPA) (0.57) |
| Elkoshite | Elkoshite | /əlˈkoʊ.ʃi.tiː/ | Nahum 1:1 |  | unsure (guessed IPA) (0.38) |
| No-Amon | No-Amon | /ˈnoʊ.ˈeɪ.mən/ | Nahum 3:8 |  | unsure (guessed IPA) (0.67) |
| Habakkuk | Habakkuk | /həˈbæk.ək/ | Habakkuk 1:1 |  | still wrong (0.64) |
| Maktesh | Maktesh | /ˈmæk.təʃ/ | Zephaniah 1:11 |  | unsure (guessed IPA) (0.75) |
| Cushites | Cushites | /ˈsjuː.ʃi.təs/ | Zephaniah 2:12 |  | unsure (guessed IPA) (0.44) |
| Shebat | Shebat | /ˈʃiː.bət/ | Zechariah 1:7 |  | unsure (guessed IPA) (0.50) |
| Hadrach | Hadrach | /ˈhæd.rək/ | Zechariah 9:1 |  | fine as spelled (0.92) |
| Union | Union | /jˈuːnjən/ | Zechariah 11:7 |  | fine as spelled (0.83) |
| Hadadrimmon | Hadadrimmon | /həˈdæd.rɪm.mən/ | Zechariah 12:11 |  | unsure (guessed IPA) (0.70) |
| Megiddon | Megiddon | /ˈmiː.ɡɪd.dən/ | Zechariah 12:11 |  | unsure (guessed IPA) (0.79) |
| Malachi | Malachi | /ˈmæləkaɪ/ | Malachi 1:1 |  | fine as spelled (0.83) |
| Jechoniah | Jechoniah | /dʒə.kəˈni.əh/ | Matthew 1:11 |  | unsure (guessed IPA) (0.56) |
| Abiud | Abiud | /ˈeɪ.bi.əd/ | Matthew 1:13 |  | unsure (guessed IPA) (0.60) |
| Azor | Azor | /ˈeɪ.zər/ | Matthew 1:13 |  | unsure (guessed IPA) (0.62) |
| Achim | Achim | /ˈeɪ.kɪm/ | Matthew 1:14 |  | unsure (guessed IPA) (0.75) |
| Eliud | Eliud | /ˈiː.li.əd/ | Matthew 1:14 |  | unsure (guessed IPA) (0.50) |
| Matthan | Matthan | /ˈmæt.θən/ | Matthew 1:15 |  | unsure (guessed IPA) (0.58) |
| Archelaus | Archelaus | /ˌɑɹ.kəˈleɪ.əs/ | Matthew 2:22 |  | still wrong (0.75) |
| Baptizer | Baptizer | /ˈbæp.ti.zər/ | Matthew 3:1 |  | fine as spelled (0.88) |
| Decapolis | Decapolis | /dəˈseɪ.pə.lɪs/ | Matthew 4:25 |  | unsure (guessed IPA) (0.39) |
| Gergesenes | Gergesenes | /ɡərˈɡiː.sə.nəs/ | Matthew 8:28 |  | unsure (guessed IPA) (0.40) |
| Thaddaeus | Thaddaeus | /ˈθædiːəs/ | Matthew 10:3 |  | still wrong (0.33) |
| Magdala | Magdala | /mɑɡdˈɑlə/ | Matthew 15:39 |  | fine as spelled (1.00) |
| Gentile | Gentile | /dʒˈɛntaɪl/ | Matthew 18:17 |  | fine as spelled (1.00) |
| Scriptures | Scriptures | /skrˈɪptʃɚz/ | Matthew 21:42 |  | fine as spelled (1.00) |
| Herodians | Herodians | /həˈroʊ.di.əns/ | Matthew 22:16 |  | unsure (guessed IPA) (0.74) |
| Rabbi | Rabbi | /rˈæbaɪ/ | Matthew 23:7 |  | fine as spelled (1.00) |
| Barachiah | Barachiah | /bə.rəˈki.əh/ | Matthew 23:35 |  | unsure (guessed IPA) (0.75) |
| Gethsemane | Gethsemane | /ɡɛθˈsɛməni/ | Matthew 26:36 |  | still wrong (0.67) |
| Praetorium | Praetorium | /prə.əˈtoʊ.ri.əm/ | Matthew 27:27 |  | unsure (guessed IPA) (0.60) |
| JESUS | JESUS | /dʒˈiːzəs/ | Matthew 27:37 |  | fine as spelled (1.00) |
| JEWS | JEWS | /dʒˈuːz/ | Matthew 27:37 |  | fine as spelled (1.00) |
| Idumaea | Idumaea | /iˈdjuː.mə.iː/ | Mark 3:8 |  | unsure (guessed IPA) (0.14) |
| Boanerges | Boanerges | /ˈboʊ.nər.ɡəs/ | Mark 3:17 |  | unsure (guessed IPA) (0.31) |
| Legion | Legion | /lˈiːdʒən/ | Mark 5:9 |  | fine as spelled (1.00) |
| Corban | Corban | /kˈɔrbən/ | Mark 7:11 |  | still wrong (0.67) |
| Greek | Greek | /ɡrˈiːk/ | Mark 7:26 |  | fine as spelled (1.00) |
| Syrophoenician | Syrophoenician | /sə.rə.foʊˈni.si.ən/ | Mark 7:26 |  | unsure (guessed IPA) (0.58) |
| Dalmanutha | Dalmanutha | /dəlˈmeɪ.nə.θə/ | Mark 8:10 |  | unsure (guessed IPA) (0.63) |
| Bartimaeus | Bartimaeus | /bərˈti.mə.juːs/ | Mark 10:46 |  | unsure (guessed IPA) (0.35) |
| Timaeus | Timaeus | /taɪˈmiːəs/ | Mark 10:46 |  | still wrong (0.67) |
| Rufus | Rufus | /rˈuːfəs/ | Mark 15:21 |  | fine as spelled (1.00) |
| Golgotha | Golgotha | /ˈɡɒl.ɡə.θə/ | Mark 15:22 |  | fine as spelled (0.94) |
| Eloi | Eloi | /ˈiːlɔɪ/ | Mark 15:34 |  | still wrong (0.29) |
| Salome | Salome | /səlˈoʊmiː/ | Mark 15:40 |  | still wrong (0.50) |
| Theophilus | thee-OF-ih-luhs | /θiˈɒf.ɪ.ləs/ | Luke 1:3 |  | still wrong (0.75) |
| Elizabeth | ih-LIZ-uh-beth | /ɪˈlɪz.ə.bɛθ/ | Luke 1:5 |  | fine as spelled (0.88) |
| Herod | HAIR-uhd | /ˈhɛr.əd/ | Luke 1:5 |  | fine as spelled (0.80) |
| Judea | joo-DEE-uh | /dʒuːˈdiː.ə/ | Luke 1:5 |  | fine as spelled (1.00) |
| Zacharias | zak-uh-RY-uhs | /ˌzæk.əˈraɪ.əs/ | Luke 1:5 |  | fine as spelled (0.94) |
| John | JON | /dʒɒn/ | Luke 1:13 |  | fine as spelled (1.00) |
| Gabriel | GAY-bree-el | /ˈɡeɪ.bri.əl/ | Luke 1:19 |  | fine as spelled (1.00) |
| Nazareth | NAZ-uh-reth | /ˈnæz.ə.rɛθ/ | Luke 1:26 |  | fine as spelled (0.86) |
| Mary | MAIR-ee | /ˈmɛər.i/ | Luke 1:27 |  | fine as spelled (1.00) |
| Augustus | aw-GUS-tuhs | /ɔːˈɡʌs.təs/ | Luke 2:1 |  | still wrong (0.79) |
| Caesar | SEE-zer | /ˈsiː.zər/ | Luke 2:1 |  | fine as spelled (1.00) |
| Quirinius | kwih-RIN-ee-uhs | /kwɪˈrɪn.i.əs/ | Luke 2:2 |  | still wrong (0.78) |
| Christ | KRYST | /kraɪst/ | Luke 2:11 |  | fine as spelled (1.00) |
| Jesus | JEE-zuhs | /ˈdʒiː.zəs/ | Luke 2:21 |  | fine as spelled (1.00) |
| Anna | AN-uh | /ˈæn.ə/ | Luke 2:36 |  | fine as spelled (0.83) |
| Phanuel | fuh-NYOO-el | /fəˈnjuː.ɛl/ | Luke 2:36 |  | still wrong (0.46) |
| Abilene | ab-ih-LEE-nee | /ˌæb.ɪˈliː.ni/ | Luke 3:1 |  | suggestion waiting (0.71) |
| Ituraea | it-yuu-REE-uh | /ˌɪt.jʊˈriː.ə/ | Luke 3:1 | ✅ | overridden (0.93) |
| Lysanias | ly-SAY-nee-uhs | /laɪˈseɪ.ni.əs/ | Luke 3:1 |  | fine as spelled (1.00) |
| Philip | FIL-ip | /ˈfɪl.ɪp/ | Luke 3:1 |  | fine as spelled (1.00) |
| Pilate | PY-luht | /ˈpaɪ.lət/ | Luke 3:1 |  | fine as spelled (1.00) |
| Pontius | PON-shuhs | /ˈpɒn.ʃəs/ | Luke 3:1 |  | fine as spelled (0.83) |
| Tiberius | ty-BEER-ee-uhs | /taɪˈbɪr.i.əs/ | Luke 3:1 |  | fine as spelled (0.94) |
| Trachonitis | trak-oh-NY-tis | /ˌtræk.oʊˈnaɪ.tɪs/ | Luke 3:1 |  | still wrong (0.70) |
| Annas | AN-uhs | /ˈæn.əs/ | Luke 3:2 |  | still wrong (0.57) |
| Caiaphas | KAY-uh-fuhs | /ˈkeɪ.ə.fəs/ | Luke 3:2 |  | suggestion waiting (0.75) |
| Herodias | huh-ROH-dee-uhs | /həˈroʊ.di.əs/ | Luke 3:19 |  | fine as spelled (0.81) |
| Heli | heeleye | /ˈhiː.laɪ/ | Luke 3:23 | ✅ | overridden (0.88) |
| Jannai | JAN-eye | /ˈdʒæn.aɪ/ | Luke 3:24 |  | still wrong (0.75) |
| Matthat | MAT-thatt | /ˈmæt.θæt/ | Luke 3:24 | ✅ | overridden (0.83) |
| Melchi | MEHL-keye | /ˈmɛl.kaɪ/ | Luke 3:24 | ✅ | overridden (1.00) |
| Amos | AY-muhs | /ˈeɪ.məs/ | Luke 3:25 |  | fine as spelled (0.88) |
| Esli | ES-ly | /ˈɛs.laɪ/ | Luke 3:25 |  | suggestion waiting (0.75) |
| Mattathias | mat-uh-THY-uhs | /ˌmæt.əˈθaɪ.əs/ | Luke 3:25 |  | still wrong (0.44) |
| Naggai | NAG-eye | /ˈnæɡ.aɪ/ | Luke 3:25 |  | fine as spelled (0.80) |
| Nahum | NAY-huhm | /ˈneɪ.həm/ | Luke 3:25 |  | fine as spelled (0.80) |
| Maath | MAY-ath | /ˈmeɪ.æθ/ | Luke 3:26 |  | still wrong (0.75) |
| Semein | SEM-ee-in | /ˈsɛm.i.ɪn/ | Luke 3:26 |  | still wrong (0.50) |
| Joanan | joh-AY-nan | /dʒoʊˈeɪ.næn/ | Luke 3:27 | ✅ | overridden (0.83) |
| Neri | neereye | /ˈniː.raɪ/ | Luke 3:27 | ✅ | overridden (1.00) |
| Rhesa | REE-suh | /ˈriː.sə/ | Luke 3:27 |  | fine as spelled (0.90) |
| Addi | AD-eye | /ˈæd.aɪ/ | Luke 3:28 | ✅ | overridden (1.00) |
| Cosam | KOH-sam | /ˈkoʊ.sæm/ | Luke 3:28 |  | fine as spelled (0.80) |
| Elmodam | el-MOH-dam | /ɛlˈmoʊ.dæm/ | Luke 3:28 |  | fine as spelled (0.93) |
| Jorim | jawrim | /ˈdʒɔːr.ɪm/ | Luke 3:29 | ✅ | overridden (0.80) |
| Jose | JOH-see | /ˈdʒoʊ.siː/ | Luke 3:29 | ✅ | overridden (1.00) |
| Jonan | JOH-nan | /ˈdʒoʊ.næn/ | Luke 3:30 |  | suggestion waiting (0.70) |
| Mattatha | MAT-uh-thuh | /ˈmæt.ə.θə/ | Luke 3:31 |  | still wrong (0.67) |
| Melea | MEL-ee-uh | /ˈmɛl.i.ə/ | Luke 3:31 |  | fine as spelled (0.80) |
| Menan | MEE-nan | /ˈmiː.næn/ | Luke 3:31 | ✅ | overridden (0.90) |
| Salmon | SAL-muhn | /ˈsæl.mən/ | Luke 3:32 |  | fine as spelled (0.83) |
| Arphaxad | ar-FAK-sad | /ɑːrˈfæk.sæd/ | Luke 3:36 |  | fine as spelled (1.00) |
| Enos | eenas | /ˈiː.nəs/ | Luke 3:38 | ✅ | overridden (1.00) |
| Satan | SAY-tuhn | /ˈseɪ.tən/ | Luke 4:8 |  | fine as spelled (1.00) |
| Capernaum | kuh-PERR-nay-uhm | /kəˈpɜːr.neɪ.əm/ | Luke 4:23 | ✅ | overridden (0.94) |
| Zarephath | ZAIR-uh-fath | /ˈzɛr.ə.fæθ/ | Luke 4:26 |  | fine as spelled (0.93) |
| Elisha | ih-LY-shuh | /ɪˈlaɪ.ʃə/ | Luke 4:27 |  | still wrong (0.70) |
| Simon | SY-muhn | /ˈsaɪ.mən/ | Luke 4:38 |  | fine as spelled (1.00) |
| Gennesaret | guh-NES-uh-ret | /ɡəˈnɛs.ə.rɛt/ | Luke 5:1 |  | still wrong (0.61) |
| Peter | PEE-ter | /ˈpiː.tər/ | Luke 5:8 |  | fine as spelled (0.80) |
| James | JAYMZ | /dʒeɪmz/ | Luke 5:10 |  | fine as spelled (1.00) |
| Zebedee | ZEB-uh-dee | /ˈzɛb.ə.diː/ | Luke 5:10 |  | fine as spelled (0.83) |
| Pharisees | FAIR-ih-seez | /ˈfær.ɪ.siːz/ | Luke 5:17 |  | fine as spelled (0.86) |
| Alphaeus | al-FEE-uhs | /ælˈfiː.əs/ | Luke 6:15 |  | fine as spelled (1.00) |
| Iscariot | is-KAIR-ee-uht | /ɪsˈkær.i.ət/ | Luke 6:16 |  | still wrong (0.69) |
| Judas | JOO-duhs | /ˈdʒuː.dəs/ | Luke 6:16 |  | fine as spelled (0.90) |
| Nain | nayn | /neɪn/ | Luke 7:11 | ✅ | overridden (1.00) |
| Pharisee | FAIR-ih-see | /ˈfær.ɪ.siː/ | Luke 7:36 |  | fine as spelled (0.83) |
| Magdalene | MAG-duh-leen | /ˈmæɡ.də.liːn/ | Luke 8:2 |  | fine as spelled (1.00) |
| Chuzas | KOO-zuhss | /ˈkuː.zəs/ | Luke 8:3 | ✅ | overridden (1.00) |
| Joanna | joh-AN-uh | /dʒoʊˈæn.ə/ | Luke 8:3 |  | fine as spelled (1.00) |
| Gadarenes | GAD-uh-reenz | /ˈɡæd.ə.riːnz/ | Luke 8:26 |  | fine as spelled (1.00) |
| Jairus | JY-ruhs | /ˈdʒaɪ.rəs/ | Luke 8:41 |  | fine as spelled (0.80) |
| Bethsaida | behth-SAY-i-duh | /bɛθˈseɪ.ɪ.də/ | Luke 9:10 | ✅ | overridden (0.83) |
| Samaritans | suh-MAIR-ih-tuhnz | /səˈmær.ɪ.tənz/ | Luke 9:52 |  | fine as spelled (0.85) |
| Sodom | SOD-uhm | /ˈsɒd.əm/ | Luke 10:12 |  | fine as spelled (1.00) |
| Chorazin | koh-RAY-zihn | /koʊˈreɪ.zɪn/ | Luke 10:13 | ✅ | overridden (1.00) |
| Hades | HAY-deez | /ˈheɪ.diːz/ | Luke 10:15 |  | fine as spelled (1.00) |
| Samaritan | suh-MAIR-ih-tuhn | /səˈmær.ɪ.tən/ | Luke 10:33 |  | fine as spelled (0.89) |
| Martha | MAR-thuh | /ˈmɑːr.θə/ | Luke 10:38 |  | fine as spelled (1.00) |
| Beelzebul | bee-EHL-zuh-buhll | /biˈɛl.zə.bʌl/ | Luke 11:15 | ✅ | overridden (0.89) |
| Jonah | JOH-nuh | /ˈdʒoʊ.nə/ | Luke 11:29 |  | fine as spelled (1.00) |
| Ninevites | NIN-uh-vites | /ˈnɪn.ə.vaɪts/ | Luke 11:30 |  | still wrong (0.75) |
| Nineveh | NIN-uh-vuh | /ˈnɪn.ə.və/ | Luke 11:32 |  | fine as spelled (0.83) |
| Zachariah | zak-uh-RY-uh | /ˌzæk.əˈraɪ.ə/ | Luke 11:51 |  | fine as spelled (0.93) |
| Gehenna | gahehnuh | /ɡəˈhɛn.ə/ | Luke 12:5 | ✅ | overridden (0.83) |
| Galileans | gal-ih-LEE-uhnz | /ˌɡæl.ɪˈliː.ənz/ | Luke 13:1 |  | fine as spelled (0.89) |
| Siloam | sylohuhm | /saɪˈloʊ.əm/ | Luke 13:4 | ✅ | overridden (0.86) |
| Mammon | MAM-uhn | /ˈmæm.ən/ | Luke 16:13 |  | fine as spelled (1.00) |
| Lazarus | LAZ-uh-ruhs | /ˈlæz.ə.rəs/ | Luke 16:20 |  | fine as spelled (1.00) |
| Zacchaeus | za-KEE-uhs | /zæˈkiː.əs/ | Luke 19:2 |  | fine as spelled (0.83) |
| Bethany | BETH-uh-nee | /ˈbɛθ.ə.ni/ | Luke 19:29 |  | fine as spelled (0.92) |
| Bethsphage | BETH-sfuh-jee | /ˈbɛθ.sfə.dʒiː/ | Luke 19:29 |  | still wrong (0.50) |
| Olivet | ahlihveht | /ˈɒl.ɪ.vɛt/ | Luke 19:29 | ✅ | overridden (0.92) |
| Sadducees | SAD-joo-seez | /ˈsædʒ.ə.siːz/ | Luke 20:27 |  | fine as spelled (1.00) |
| Galilean | gal-ih-LEE-uhn | /ˌɡæl.ɪˈliː.ən/ | Luke 22:59 |  | fine as spelled (0.88) |
| Barabbas | buh-RAB-uhss | /bəˈræb.əs/ | Luke 23:18 | ✅ | overridden (0.88) |
| Latin | Latin | /lˈætən/ | Luke 23:38 |  | fine as spelled (0.80) |
| Paradise | Paradise | /pˈɛrədaɪs/ | Luke 23:43 |  | fine as spelled (0.86) |
| Arimathaea | air-ih-muh-THEE-uh | /ˌær.ɪ.məˈθiː.ə/ | Luke 23:51 |  | still wrong (0.71) |
| Emmaus | eh-MAY-uhs | /ɛˈmeɪ.əs/ | Luke 24:13 |  | fine as spelled (0.80) |
| Cleopas | KLEE-oh-puhs | /ˈkliː.ə.pəs/ | Luke 24:18 |  | still wrong (0.50) |
| Nazarene | naz-uh-REEN | /ˌnæz.əˈriːn/ | Luke 24:19 |  | fine as spelled (1.00) |
| Messiah | Messiah | /məsˈaɪə/ | John 1:41 |  | fine as spelled (1.00) |
| Cephas | Cephas | /sˈɛfəz/ | John 1:42 |  | still wrong (0.40) |
| Nathanael | Nathanael | /nˈæθəneɪl/ | John 1:45 |  | still wrong (0.50) |
| Cana | Cana | /kˈænə/ | John 2:1 |  | still wrong (0.62) |
| Nicodemus | Nicodemus | /nɪkəˈdiːməs/ | John 3:1 |  | fine as spelled (0.94) |
| Salim | Salim | /sˈælɪm/ | John 3:23 |  | still wrong (0.60) |
| Sychar | sykar | /ˈsaɪ.kər/ | John 4:5 | ✅ | overridden (0.80) |
| Tiberias | Tiberias | /taɪˈbɪəɹi.æs/ | John 6:1 |  | fine as spelled (0.88) |
| Dispersion | Dispersion | /dɪspˈɚʒən/ | John 7:35 |  | fine as spelled (0.89) |
| Didymus | Didymus | /ˈdi.də.məs/ | John 11:16 |  | unsure (guessed IPA) (0.71) |
| Romans | Romans | /rˈoʊmənz/ | John 11:48 |  | fine as spelled (1.00) |
| Malchus | Malchus | /ˈmæl.kəs/ | John 18:10 |  | fine as spelled (1.00) |
| NAZARETH | NAZARETH | /nˈæzərɪθ/ | John 19:19 |  | fine as spelled (1.00) |
| Clopas | Clopas | /ˈkloʊ.pəs/ | John 19:25 |  | unsure (guessed IPA) (0.77) |
| Roman | Roman | /rˈoʊmən/ | John 19:39 |  | fine as spelled (1.00) |
| Holy | Holy |  | Acts 1:2 |  | fine as spelled |
| Kingdom | Kingdom |  | Acts 1:3 |  | fine as spelled |
| Father | Father |  | Acts 1:4 |  | fine as spelled |
| Judaea | joo-DEE-uh | /dʒuːˈdiː.ə/ | Acts 1:8 |  | fine as spelled (0.80) |
| Samaria | Samairia | /səˈmɛər.i.ə/ | Acts 1:8 | ✅ | overridden (0.00) |
| Sabbath | Sabbath |  | Acts 1:12 |  | fine as spelled |
| Andrew | AN-droo | /ˈæn.druː/ | Acts 1:13 |  | fine as spelled (1.00) |
| Bartholomew | bar-THOL-uh-myoo | /bɑːrˈθɒl.ə.mjuː/ | Acts 1:13 |  | fine as spelled (0.95) |
| Matthew | MATH-yoo | /ˈmæθ.juː/ | Acts 1:13 |  | fine as spelled (1.00) |
| Thomas | TOM-uhs | /ˈtɒm.əs/ | Acts 1:13 |  | fine as spelled (1.00) |
| Zealot | Zealot |  | Acts 1:13 |  | fine as spelled |
| Zelotes | zi-LOH-teez | /zɪˈloʊ.tiːz/ | Acts 1:13 | ✅ | overridden (0.86) |
| Scripture | Scripture |  | Acts 1:16 |  | fine as spelled |
| Aceldama | uh-KEL-duh-muh | /əˈkɛl.də.mə/ | Acts 1:19 |  | fine as spelled (0.88) |
| Psalms | Psalms |  | Acts 1:20 |  | fine as spelled |
| Barsabas | BAR-suh-bus | /ˈbɑːr.sə.bəs/ | Acts 1:23 |  | still wrong (0.56) |
| Barsabbas | Bar-sabbas | /bɑːrˈsæb.əs/ | Acts 1:23 | ✅ | overridden (0.00) |
| Justus | JUS-tuhs | /ˈdʒʌs.təs/ | Acts 1:23 |  | fine as spelled (0.83) |
| Matthias | muh-THY-uhs | /məˈθaɪ.əs/ | Acts 1:23 |  | fine as spelled (1.00) |
| Pentecost | PEN-tih-kost | /ˈpɛn.tɪ.kɒst/ | Acts 2:1 |  | fine as spelled (1.00) |
| Jews | Jews |  | Acts 2:5 |  | fine as spelled |
| Galilaeans | gal-ih-LEE-unz | /ˌɡæl.ɪˈliː.ənz/ | Acts 2:7 |  | fine as spelled (0.89) |
| Asia | AY-zhuh | /ˈeɪ.ʒə/ | Acts 2:9 |  | fine as spelled (1.00) |
| Cappadocia | kap-uh-DOH-shuh | /ˌkæp.əˈdoʊ.ʃə/ | Acts 2:9 |  | fine as spelled (0.83) |
| Elamites | EE-luh-mites | /ˈiː.lə.maɪts/ | Acts 2:9 |  | fine as spelled (0.93) |
| Medes | MEEDZ | /miːdz/ | Acts 2:9 |  | fine as spelled (1.00) |
| Pontus | PON-tuhs | /ˈpɒn.təs/ | Acts 2:9 |  | still wrong (0.75) |
| Libya | LIB-ee-uh | /ˈlɪb.i.ə/ | Acts 2:10 |  | fine as spelled (1.00) |
| Pamphylia | pam-FIL-ee-uh | /pæmˈfɪl.i.ə/ | Acts 2:10 |  | fine as spelled (0.94) |
| Rome | ROHM | /roʊm/ | Acts 2:10 |  | fine as spelled (1.00) |
| Beautiful | Beautiful |  | Acts 3:2 |  | fine as spelled |
| Gate | Gate |  | Acts 3:10 |  | fine as spelled |
| Servant | Servant |  | Acts 3:13 |  | fine as spelled |
| Righteous | Righteous |  | Acts 3:14 |  | fine as spelled |
| Prince | Prince |  | Acts 3:15 |  | fine as spelled |
| Alexander | al-ig-ZAN-der | /ˌæl.ɪɡˈzæn.dər/ | Acts 4:6 |  | fine as spelled (1.00) |
| Barnabas | BAR-nuh-buhs | /ˈbɑːr.nə.bəs/ | Acts 4:36 |  | fine as spelled (1.00) |
| Cyprus | SY-pruhs | /ˈsaɪ.prəs/ | Acts 4:36 |  | fine as spelled (1.00) |
| Joses | JOH-seez | /ˈdʒoʊ.siːz/ | Acts 4:36 | ✅ | overridden (1.00) |
| Ananias | an-uh-NY-uhs | /ˌæn.əˈnaɪ.əs/ | Acts 5:1 |  | fine as spelled (0.93) |
| Sapphira | suhfeyeruh | /səˈfaɪ.rə/ | Acts 5:1 | ✅ | overridden (0.83) |
| Gamaliel | guh-MAY-lee-el | /ɡəˈmeɪ.li.əl/ | Acts 5:34 |  | fine as spelled (1.00) |
| Theudas | thoodas | /ˈθuː.dəs/ | Acts 5:36 | ✅ | overridden (1.00) |
| Grecians | GREE-shunz | /ˈɡriː.ʃənz/ | Acts 6:1 |  | fine as spelled (1.00) |
| Hellenists | HEL-uh-nists | /ˈhɛl.ə.nɪsts/ | Acts 6:1 |  | fine as spelled (1.00) |
| Antioch | AN-tee-ok | /ˈæn.ti.ɒk/ | Acts 6:5 |  | fine as spelled (0.92) |
| Nicanor | ny-KAY-nor | /naɪˈkeɪ.nɔːr/ | Acts 6:5 |  | fine as spelled (0.86) |
| Nicolas | NIK-uh-lus | /ˈnɪk.ə.ləs/ | Acts 6:5 |  | fine as spelled (0.93) |
| Nicolaus | nik-uh-LAY-uhs | /ˌnɪk.əˈleɪ.əs/ | Acts 6:5 |  | fine as spelled (0.88) |
| Parmenas | PAR-muh-nuhs | /ˈpɑːr.mə.nəs/ | Acts 6:5 |  | still wrong (0.75) |
| Prochorus | PROK-uh-ruhss | /ˈprɒk.ə.rəs/ | Acts 6:5 | ✅ | overridden (1.00) |
| Stephen | STEE-vuhn | /ˈstiː.vən/ | Acts 6:5 |  | fine as spelled (1.00) |
| Timon | TY-muhn | /ˈtaɪ.mən/ | Acts 6:5 |  | fine as spelled (1.00) |
| Alexandrians | al-ig-ZAN-dree-uhnz | /ˌæl.ɪɡˈzæn.dri.ənz/ | Acts 6:9 |  | fine as spelled (1.00) |
| Cilicia | sih-LISH-uh | /sɪˈlɪʃ.ə/ | Acts 6:9 |  | fine as spelled (0.83) |
| Cyrenians | sy-REE-nee-uhnz | /saɪˈriː.ni.ənz/ | Acts 6:9 |  | fine as spelled (0.94) |
| Libertines | LIB-er-teenz | /ˈlɪb.ər.tiːnz/ | Acts 6:9 |  | fine as spelled (1.00) |
| Charran | karuhn | /ˈkær.ən/ | Acts 7:2 | ✅ | overridden (0.90) |
| Chaldaeans | kal-DEE-uhnz | /kælˈdiː.ənz/ | Acts 7:4 |  | fine as spelled (1.00) |
| Chanaan | KAY-nann | /ˈkeɪ.næn/ | Acts 7:11 | ✅ | overridden (1.00) |
| Emmor | EHM-awr | /ˈɛm.ɔːr/ | Acts 7:16 | ✅ | overridden (1.00) |
| Hamor | HAY-mawr | /ˈheɪ.mɔːr/ | Acts 7:16 | ✅ | overridden (1.00) |
| Sychem | SY-kem | /ˈsaɪ.kɛm/ | Acts 7:16 |  | fine as spelled (0.80) |
| Egyptians | ee-JIP-shuhnz | /iˈdʒɪp.ʃənz/ | Acts 7:22 |  | fine as spelled (0.88) |
| Madian | MAY-dee-un | /ˈmeɪ.di.ən/ | Acts 7:29 |  | fine as spelled (0.83) |
| Sina | SY-nuh | /ˈsaɪ.nə/ | Acts 7:30 |  | still wrong (0.68) |
| Sinai | SY-ny | /ˈsaɪ.naɪ/ | Acts 7:30 |  | fine as spelled (1.00) |
| Moloch | MOH-lok | /ˈmoʊ.lɒk/ | Acts 7:43 |  | fine as spelled (0.90) |
| Remphan | REM-fan | /ˈrɛm.fæn/ | Acts 7:43 |  | fine as spelled (0.83) |
| Rephan | REE-fann | /ˈriː.fæn/ | Acts 7:43 | ✅ | overridden (1.00) |
| Gaza | GAH-zuh | /ˈɡɑː.zə/ | Acts 8:26 |  | still wrong (0.75) |
| Candace | KAN-duh-see | /ˈkæn.də.siː/ | Acts 8:27 |  | suggestion waiting (0.71) |
| Ethiopia | ee-thee-OH-pee-uh | /ˌiː.θiˈoʊ.pi.ə/ | Acts 8:27 |  | fine as spelled (1.00) |
| Esaias | izayuhs | /ɪˈzeɪ.əs/ | Acts 8:28 | ✅ | overridden (1.00) |
| Azotus | uh-ZOH-tuhss | /əˈzoʊ.təs/ | Acts 8:40 | ✅ | overridden (0.92) |
| Tarsus | TAR-suhs | /ˈtɑːr.səs/ | Acts 9:11 |  | fine as spelled (0.83) |
| Lydda | LID-uh | /ˈlɪd.ə/ | Acts 9:32 |  | fine as spelled (0.90) |
| Aeneas | ih-NEE-uhs | /ɪˈniː.əs/ | Acts 9:33 |  | fine as spelled (1.00) |
| Saron | SAIRR-on | /ˈsɛər.ɒn/ | Acts 9:35 | ✅ | overridden (1.00) |
| Dorcas | DOR-kuhs | /ˈdɔːr.kəs/ | Acts 9:36 |  | still wrong (0.75) |
| Tabitha | TAB-ih-thuh | /ˈtæb.ɪ.θə/ | Acts 9:36 |  | fine as spelled (1.00) |
| Cornelius | kor-NEEL-yuhs | /kɔːrˈniːl.jəs/ | Acts 10:1 |  | fine as spelled (0.83) |
| Italian | Italian | /ɪtˈæljən/ | Acts 10:1 |  | fine as spelled (0.93) |
| Regiment | Regiment | /rˈɛdʒəmənt/ | Acts 10:1 |  | fine as spelled (0.88) |
| Phenice | fihneyesee | /fɪˈnaɪ.siː/ | Acts 11:19 | ✅ | overridden (0.86) |
| Christians | Christians | /krˈɪstʃənz/ | Acts 11:26 |  | fine as spelled (0.94) |
| Agabus | AGga-bus | /ˈæɡ.ə.bəs/ | Acts 11:28 | ✅ | overridden (1.00) |
| Claudius | KLAW-dee-uhs | /ˈklɔː.di.əs/ | Acts 11:28 |  | fine as spelled (1.00) |
| Mark | MARK | /mɑːrk/ | Acts 12:12 |  | fine as spelled (1.00) |
| Rhoda | ROH-duh | /ˈroʊ.də/ | Acts 12:13 |  | fine as spelled (1.00) |
| Caesarea | sessa-Rheea | /ˌsɛs.əˈriː.ə/ | Acts 12:19 | ✅ | overridden (0.00) |
| Blastus | BLAS-tuhs | /ˈblæs.təs/ | Acts 12:20 |  | still wrong (0.71) |
| Cyrene | siereen | /saɪˈriːn/ | Acts 13:1 | ✅ | overridden (0.00) |
| Lucius | LOO-shuhs | /ˈluː.ʃəs/ | Acts 13:1 |  | fine as spelled (1.00) |
| Manaen | MAN-ay-en | /ˈmæn.eɪ.ɛn/ | Acts 13:1 |  | still wrong (0.50) |
| Niger | NY-jer | /ˈnaɪ.dʒər/ | Acts 13:1 |  | fine as spelled (1.00) |
| Seleucia | suh-LOO-shuh | /səˈluː.ʃə/ | Acts 13:4 |  | fine as spelled (0.86) |
| Salamis | Salamiss | /ˈsæl.ə.mɪs/ | Acts 13:5 | ✅ | overridden (0.00) |
| Bar-jesus | bar-JEE-zus | /bɑːrˈdʒiː.zəs/ | Acts 13:6 |  | fine as spelled (0.94) |
| Paphos | PAYfose | /ˈpeɪ.fɒs/ | Acts 13:6 | ✅ | overridden (0.80) |
| Paulus | PAW-luhs | /ˈpɔː.ləs/ | Acts 13:7 |  | suggestion waiting (0.70) |
| Sergius | SUR-jee-uhs | /ˈsɜːr.dʒi.əs/ | Acts 13:7 |  | fine as spelled (0.86) |
| Elymas | ehlihmuhs | /ˈɛl.ɪ.məs/ | Acts 13:8 | ✅ | overridden (0.83) |
| Paul | PAWL | /pɔːl/ | Acts 13:9 |  | fine as spelled (1.00) |
| Perga | PUR-guh | /ˈpɜːr.ɡə/ | Acts 13:13 |  | fine as spelled (0.80) |
| Pisidia | pih-SID-ee-uh | /pɪˈsɪd.i.ə/ | Acts 13:14 |  | fine as spelled (0.93) |
| Cis | SIS | /sɪs/ | Acts 13:21 |  | fine as spelled (1.00) |
| Iconium | eye-KOH-nee-uhm | /aɪˈkoʊ.ni.əm/ | Acts 13:51 |  | fine as spelled (1.00) |
| Derbe | DERR-bee | /ˈdɜːr.bi/ | Acts 14:6 | ✅ | overridden (1.00) |
| Lycaonia | lik-ay-OH-nee-uh | /ˌlɪk.eɪˈoʊ.ni.ə/ | Acts 14:6 |  | fine as spelled (0.81) |
| Lystra | LIS-truh | /ˈlɪs.trə/ | Acts 14:6 |  | fine as spelled (0.86) |
| Jupiter | JOO-pih-ter | /ˈdʒuː.pɪ.tər/ | Acts 14:12 |  | fine as spelled (0.86) |
| Mercurius | mur-KYOOR-ee-us | /mɜːrˈkjʊər.i.əs/ | Acts 14:12 |  | fine as spelled (0.90) |
| Attalia | at-uh-LY-uh | /ˌæt.əˈlaɪ.ə/ | Acts 14:25 |  | still wrong (0.46) |
| Phoenicia | Phoneesha | /fəˈniː.ʃə/ | Acts 15:3 | ✅ | overridden (0.00) |
| Silas | SY-luhs | /ˈsaɪ.ləs/ | Acts 15:22 |  | fine as spelled (1.00) |
| Timotheus | tih-MOH-thee-us | /tɪˈmoʊ.θi.əs/ | Acts 16:1 |  | fine as spelled (0.88) |
| Timothy | TIM-uh-thee | /ˈtɪm.ə.θi/ | Acts 16:1 |  | fine as spelled (1.00) |
| Galatia | guh-LAY-shuh | /ɡəˈleɪ.ʃə/ | Acts 16:6 |  | fine as spelled (0.93) |
| Phrygia | FRIJ-ee-uh | /ˈfrɪdʒ.i.ə/ | Acts 16:6 |  | fine as spelled (1.00) |
| Bithynia | bih-THIN-ee-uh | /bɪˈθɪn.i.ə/ | Acts 16:7 |  | still wrong (0.71) |
| Mysia | MISH-ee-uh | /ˈmɪʃ.i.ə/ | Acts 16:7 |  | fine as spelled (1.00) |
| Troas | TROH-az | /ˈtroʊ.æz/ | Acts 16:8 |  | fine as spelled (0.80) |
| Macedonia | mas-uh-DOH-nee-uh | /ˌmæs.əˈdoʊ.ni.ə/ | Acts 16:9 |  | fine as spelled (0.94) |
| Neapolis | nee-AP-oh-lis | /niˈæp.ə.lɪs/ | Acts 16:11 |  | still wrong (0.75) |
| Samothrace | SAM-oh-thrayss | /ˈsæm.ə.θreɪs/ | Acts 16:11 |  | fine as spelled (0.88) |
| Samothracia | sam-oh-THRAY-shuh | /ˌsæm.oʊˈθreɪ.ʃə/ | Acts 16:11 |  | still wrong (0.79) |
| Philippi | fih-LIP-eye | /fɪˈlɪp.aɪ/ | Acts 16:12 |  | fine as spelled (0.83) |
| Lydia | LID-ee-uh | /ˈlɪd.i.ə/ | Acts 16:14 |  | fine as spelled (1.00) |
| Thyatira | thy-uh-TY-ruh | /ˌθaɪ.əˈtaɪ.rə/ | Acts 16:14 |  | still wrong (0.64) |
| Amphipolis | am-FIP-oh-lis | /æmˈfɪp.ə.lɪs/ | Acts 17:1 |  | fine as spelled (0.89) |
| Apollonia | ap-uh-LOH-nee-uh | /ˌæp.əˈloʊ.ni.ə/ | Acts 17:1 |  | fine as spelled (1.00) |
| Thessalonica | thes-uh-loh-NY-kuh | /ˌθɛs.ə.loʊˈnaɪ.kə/ | Acts 17:1 |  | fine as spelled (0.80) |
| Jason | JAY-suhn | /ˈdʒeɪ.sən/ | Acts 17:5 |  | fine as spelled (1.00) |
| Berea | buh-REE-uh | /bəˈriː.ə/ | Acts 17:10 |  | fine as spelled (1.00) |
| Beroea | buh-REE-uh | /bəˈriː.ə/ | Acts 17:10 |  | still wrong (0.63) |
| Athens | ATH-inz | /ˈæθ.ɪnz/ | Acts 17:15 |  | fine as spelled (0.80) |
| Epicurean | ep-ih-kyoo-REE-un | /ˌɛp.ɪ.kjʊˈriː.ən/ | Acts 17:18 |  | fine as spelled (1.00) |
| Epicureans | ep-ih-kyoo-REE-unz | /ˌɛp.ɪ.kjʊˈriː.ənz/ | Acts 17:18 |  | fine as spelled (0.95) |
| Stoic | STOH-ik | /ˈstoʊ.ɪk/ | Acts 17:18 |  | fine as spelled (1.00) |
| Stoicks | STOH-iks | /ˈstoʊ.ɪks/ | Acts 17:18 |  | fine as spelled (1.00) |
| Areopagus | air-ee-OP-uh-guhs | /ˌær.iˈɒp.ə.ɡəs/ | Acts 17:19 |  | still wrong (0.78) |
| Athenians | uh-THEE-nee-uhnz | /əˈθiː.ni.ənz/ | Acts 17:21 |  | fine as spelled (1.00) |
| Mars | MARZ | /mɑːrz/ | Acts 17:22 |  | fine as spelled (1.00) |
| Areopagite | air-ee-OP-uh-jite | /ˌær.iˈɒp.ə.dʒaɪt/ | Acts 17:34 |  | fine as spelled (0.89) |
| Damaris | DAM-uh-ris | /ˈdæm.ə.rɪs/ | Acts 17:34 |  | still wrong (0.71) |
| Dionysius | dy-uh-NISH-ee-uhs | /ˌdaɪ.əˈnɪʃ.i.əs/ | Acts 17:34 |  | fine as spelled (0.89) |
| Corinth | KOR-inth | /ˈkɔːr.ɪnθ/ | Acts 18:1 |  | fine as spelled (0.83) |
| Aquila | AK-wih-luh | /ˈæk.wɪ.lə/ | Acts 18:2 |  | still wrong (0.42) |
| Italy | IT-uh-lee | /ˈɪt.ə.li/ | Acts 18:2 |  | fine as spelled (0.80) |
| Priscilla | prih-SIL-uh | /prɪˈsɪl.ə/ | Acts 18:2 |  | fine as spelled (1.00) |
| Corinthians | kuh-RIN-thee-uhnz | /kəˈrɪn.θi.ənz/ | Acts 18:8 |  | fine as spelled (0.91) |
| Crispus | KRIS-pus | /ˈkrɪs.pəs/ | Acts 18:8 |  | fine as spelled (1.00) |
| Achaia | a-KAY-uh | /əˈkeɪ.ə/ | Acts 18:12 | ✅ | overridden (0.90) |
| Gallio | GAL-ee-oh | /ˈɡæl.i.oʊ/ | Acts 18:12 |  | fine as spelled (0.90) |
| Sosthenes | SOS-thuh-neez | /ˈsɒs.θə.niːz/ | Acts 18:17 |  | suggestion waiting (0.75) |
| Cenchrea | SENG-krih-uh | /ˈsɛŋ.krɪ.ə/ | Acts 18:18 |  | still wrong (0.64) |
| Cenchreae | sehn-KREE-ee | /sɛnˈkriː.iː/ | Acts 18:18 | ✅ | overridden (1.00) |
| Ephesus | EF-uh-suhs | /ˈɛf.ə.səs/ | Acts 18:19 |  | still wrong (0.67) |
| Alexandrian | al-ig-ZAN-dree-uhn | /ˌæl.ɪɡˈzæn.dri.ən/ | Acts 18:24 |  | fine as spelled (0.96) |
| Apollos | uh-POL-uhs | /əˈpɒl.əs/ | Acts 18:24 |  | fine as spelled (0.83) |
| Tyrannus | ty-RAN-uhs | /taɪˈræn.əs/ | Acts 19:9 |  | fine as spelled (0.86) |
| Sceva | SEE-vuh | /ˈsiː.və/ | Acts 19:14 |  | fine as spelled (0.90) |
| Erastus | ih-RAS-tuhs | /ɪˈræs.təs/ | Acts 19:22 |  | fine as spelled (1.00) |
| Artemis | AR-tuh-mis | /ˈɑːr.tə.mɪs/ | Acts 19:24 |  | fine as spelled (0.86) |
| Demetrius | dih-MEE-tree-uhs | /dɪˈmiː.tri.əs/ | Acts 19:24 |  | fine as spelled (0.94) |
| Diana | dy-AN-uh | /daɪˈæn.ə/ | Acts 19:24 |  | fine as spelled (1.00) |
| Ephesians | ih-FEE-zhuhnz | /ɪˈfiː.ʒənz/ | Acts 19:28 |  | fine as spelled (1.00) |
| Aristarchus | air-is-TAR-kuhs | /ˌær.ɪsˈtɑːr.kəs/ | Acts 19:29 |  | fine as spelled (0.80) |
| Gaius | GAY-uhs | /ˈɡeɪ.əs/ | Acts 19:29 |  | fine as spelled (0.88) |
| Asiarchs | AY-zhee-arks | /ˈeɪ.ʒi.ɑːrks/ | Acts 19:31 |  | still wrong (0.79) |
| Zeus | ZOOS | /zuːs/ | Acts 19:35 |  | fine as spelled (1.00) |
| Greece | GREESS | /ɡriːs/ | Acts 20:2 |  | fine as spelled (1.00) |
| Secundus | suh-KUN-duhs | /səˈkʌn.dəs/ | Acts 20:4 |  | fine as spelled (0.88) |
| Sopater | SOH-puh-ter | /ˈsoʊ.pə.tər/ | Acts 20:4 |  | suggestion waiting (0.71) |
| Thessalonians | thes-uh-LOH-nee-uhnz | /ˌθɛs.əˈloʊ.ni.ənz/ | Acts 20:4 |  | fine as spelled (0.91) |
| Trophimus | TROF-ih-muhs | /ˈtrɒf.ɪ.məs/ | Acts 20:4 |  | fine as spelled (0.88) |
| Tychicus | TIK-ih-kuhs | /ˈtɪk.ɪ.kəs/ | Acts 20:4 |  | fine as spelled (0.93) |
| Eutychus | YOO-tih-kuhs | /ˈjuː.tɪ.kəs/ | Acts 20:9 |  | fine as spelled (0.86) |
| Assos | AS-os | /ˈæs.ɒs/ | Acts 20:13 |  | fine as spelled (1.00) |
| Mitylene | mit-ih-LEE-nee | /ˌmɪt.ɪˈliː.ni/ | Acts 20:14 |  | still wrong (0.62) |
| Chios | KY-os | /ˈkaɪ.ɒs/ | Acts 20:15 |  | fine as spelled (1.00) |
| Miletus | my-LEE-tuhs | /maɪˈliː.təs/ | Acts 20:15 | ✅ | overridden (0.93) |
| Samos | SAY-mos | /ˈseɪ.mɒs/ | Acts 20:15 |  | fine as spelled (1.00) |
| Trogyllium | troh-JIL-ee-uhm | /troʊˈdʒɪl.i.əm/ | Acts 20:15 |  | suggestion waiting (0.75) |
| Coos | KOH-os | /ˈkoʊ.ɒs/ | Acts 21:1 |  | still wrong (0.25) |
| Cos | KOS | /kɒs/ | Acts 21:1 |  | fine as spelled (0.83) |
| Patara | PAT-uh-ruh | /ˈpæt.ə.rə/ | Acts 21:1 |  | still wrong (0.69) |
| Rhodes | ROHDZ | /roʊdz/ | Acts 21:1 |  | fine as spelled (1.00) |
| Phenicia | fihnihshuh | /fɪˈnɪʃ.ə/ | Acts 21:2 | ✅ | overridden (0.83) |
| Ptolemais | tol-uh-MAY-is | /ˌtɒl.əˈmeɪ.ɪs/ | Acts 21:7 |  | still wrong (0.75) |
| Mnason | NAY-suhn | /ˈneɪ.sən/ | Acts 21:16 |  | fine as spelled (1.00) |
| Ephesian | ih-FEE-zhuhn | /ɪˈfiː.ʒən/ | Acts 21:29 |  | fine as spelled (1.00) |
| Assassins | Assassins | /əsˈæsənz/ | Acts 21:38 |  | fine as spelled (0.86) |
| Felix | FEE-liks | /ˈfiː.lɪks/ | Acts 23:24 |  | fine as spelled (1.00) |
| Lysias | LIS-ee-uhs | /ˈlɪs.i.əs/ | Acts 23:26 |  | fine as spelled (1.00) |
| Antipatris | an-TIP-uh-tris | /ænˈtɪp.ə.trɪs/ | Acts 23:31 |  | fine as spelled (0.80) |
| Tertullus | tuhr-TUHL-uhss | /tərˈtʌl.əs/ | Acts 24:1 | ✅ | overridden (0.88) |
| Nazarenes | naz-uh-REENZ | /ˌnæz.əˈriːnz/ | Acts 24:5 |  | fine as spelled (1.00) |
| Drusilla | droo-SIL-uh | /druːˈsɪl.ə/ | Acts 24:24 |  | fine as spelled (1.00) |
| Festus | FES-tuhs | /ˈfɛs.təs/ | Acts 24:27 |  | still wrong (0.75) |
| Porcius | pawrshas | /ˈpɔːr.ʃəs/ | Acts 24:27 | ✅ | overridden (0.83) |
| Agrippa | uh-GRIP-uh | /əˈɡrɪp.ə/ | Acts 25:13 |  | fine as spelled (0.93) |
| Bernice | ber-NEE-see | /bərˈniː.siː/ | Acts 25:13 |  | fine as spelled (0.86) |
| Christian | Christian | /krˈɪstʃən/ | Acts 26:28 |  | fine as spelled (0.93) |
| Augustan | aw-GUS-tuhn | /ɔːˈɡʌs.tən/ | Acts 27:1 |  | still wrong (0.79) |
| Julius | JOOL-yuhs | /ˈdʒuːl.jəs/ | Acts 27:1 |  | fine as spelled (0.83) |
| Adramyttium | ad-ruh-MIT-ee-uhm | /ˌæd.rəˈmɪt.i.əm/ | Acts 27:2 |  | fine as spelled (0.90) |
| Macedonian | mas-uh-DOH-nee-uhn | /ˌmæs.əˈdoʊ.ni.ən/ | Acts 27:2 |  | fine as spelled (1.00) |
| Lycia | LISH-ee-uh | /ˈlɪʃ.i.ə/ | Acts 27:5 |  | fine as spelled (0.80) |
| Myra | MY-ruh | /ˈmaɪ.rə/ | Acts 27:5 |  | fine as spelled (1.00) |
| Alexandria | al-ig-ZAN-dree-uh | /ˌæl.ɪɡˈzæn.dri.ə/ | Acts 27:6 |  | fine as spelled (0.95) |
| Cnidus | NY-duhs | /ˈnaɪ.dəs/ | Acts 27:7 |  | fine as spelled (1.00) |
| Crete | KREET | /kriːt/ | Acts 27:7 |  | fine as spelled (0.88) |
| Salmone | sal-MOH-nee | /sælˈmoʊ.ni/ | Acts 27:7 |  | suggestion waiting (0.71) |
| Havens | Havens | /hˈeɪvənz/ | Acts 27:8 |  | fine as spelled (1.00) |
| Lasea | luh-SEE-uh | /ləˈsiː.ə/ | Acts 27:8 |  | fine as spelled (0.80) |
| Phoenix | FEE-niks | /ˈfiː.nɪks/ | Acts 27:12 |  | fine as spelled (1.00) |
| Euroclydon | yoo-ROK-lih-don | /jʊˈrɒk.lɪ.dɒn/ | Acts 27:14 |  | still wrong (0.65) |
| Clauda | KLAW-duh | /ˈklɔː.də/ | Acts 27:16 |  | fine as spelled (0.92) |
| Syrtis | SUR-tis | /ˈsɜːr.tɪs/ | Acts 27:17 |  | still wrong (0.67) |
| Adria | AY-dree-uh | /ˈeɪ.dri.ə/ | Acts 27:27 |  | fine as spelled (0.80) |
| Adriatic | ay-dree-AT-ik | /ˌeɪ.driˈæt.ɪk/ | Acts 27:27 |  | fine as spelled (0.88) |
| Malta | MAWL-tuh | /ˈmɔːl.tə/ | Acts 28:1 |  | fine as spelled (0.92) |
| Melita | MEL-ih-tuh | /ˈmɛl.ɪ.tə/ | Acts 28:1 |  | still wrong (0.50) |
| Publius | PUB-lee-uhs | /ˈpʌb.li.əs/ | Acts 28:7 |  | suggestion waiting (0.71) |
| Castor | KAS-ter | /ˈkæs.tər/ | Acts 28:11 |  | suggestion waiting (0.75) |
| Pollux | POL-uks | /ˈpɒl.əks/ | Acts 28:11 |  | fine as spelled (0.83) |
| Twin | Twin | /twˈɪn/ | Acts 28:11 |  | fine as spelled (1.00) |
| Syracuse | SIHR-a-kyooz | /ˈsɪr.ə.kjuːz/ | Acts 28:12 | ✅ | overridden (0.88) |
| Puteoli | pyoo-TEE-oh-ly | /pjuːˈtiː.ə.laɪ/ | Acts 28:13 |  | still wrong (0.50) |
| Rhegium | REE-jee-uhm | /ˈriː.dʒi.əm/ | Acts 28:13 |  | fine as spelled (1.00) |
| Appii | AP-ee-eye | /ˈæp.i.aɪ/ | Acts 28:15 |  | fine as spelled (1.00) |
| Appius | AP-ee-uhs | /ˈæp.i.əs/ | Acts 28:15 |  | fine as spelled (1.00) |
| Taverns | Taverns | /tˈævɚnz/ | Acts 28:15 |  | fine as spelled (1.00) |
| Illyricum | Illyricum | /ɪlˈlaɪ.ri.səm/ | Romans 15:19 |  | unsure (guessed IPA) (0.50) |
| Spain | Spain | /spˈeɪn/ | Romans 15:24 |  | fine as spelled (1.00) |
| Phoebe | Phoebe | /fˈiːbiː/ | Romans 16:1 |  | fine as spelled (1.00) |
| Prisca | Prisca | /ˈprɪs.sə/ | Romans 16:3 |  | fine as spelled (0.83) |
| Epaenetus | Epaenetus | /ə.pəˈiː.nə.təs/ | Romans 16:5 |  | unsure (guessed IPA) (0.50) |
| Andronicus | Andronicus | /ˌændɹəˈnaɪkəs/ | Romans 16:7 |  | fine as spelled (0.80) |
| Junia | Junia | /jˈuːniːə/ | Romans 16:7 |  | fine as spelled (1.00) |
| Amplias | Amplias | /ˈæm.pli.əs/ | Romans 16:8 |  | fine as spelled (0.86) |
| Stachys | stakys | /ˈsteɪ.kəs/ | Romans 16:9 | ✅ | overridden (0.67) |
| Urbanus | Urbanus | /ˈʌr.bə.nəs/ | Romans 16:9 |  | fine as spelled (0.86) |
| Apelles | Apelles | /əˈpɛliːz/ | Romans 16:10 |  | fine as spelled (1.00) |
| Aristobulus | Aristobulus | /ə.rɪsˈtoʊ.bə.ləs/ | Romans 16:10 |  | unsure (guessed IPA) (0.67) |
| Herodion | Herodion | /həˈroʊ.di.ən/ | Romans 16:11 |  | unsure (guessed IPA) (0.75) |
| Narcissus | Narcissus | /nɑrsˈɪsəs/ | Romans 16:11 |  | fine as spelled (0.88) |
| Persis | Persis | /pˈɚsɪs/ | Romans 16:12 |  | fine as spelled (0.83) |
| Tryphaena | Tryphaena | /trəˈfeɪ.ə.nə/ | Romans 16:12 |  | unsure (guessed IPA) (0.56) |
| Tryphosa | Tryphosa | /ˈtraɪ.fə.sə/ | Romans 16:12 |  | unsure (guessed IPA) (0.71) |
| Asyncritus | Asyncritus | /əˈsɪn.kri.təs/ | Romans 16:14 |  | unsure (guessed IPA) (0.55) |
| Hermas | Hermas | /ˈhɛr.məs/ | Romans 16:14 |  | unsure (guessed IPA) (0.42) |
| Hermes | Hermes | /hˈɚmiːz/ | Romans 16:14 |  | fine as spelled (0.83) |
| Patrobas | Patrobas | /ˈpæt.rə.bəs/ | Romans 16:14 |  | unsure (guessed IPA) (0.71) |
| Phlegon | Phlegon | /ˈfliː.ɡən/ | Romans 16:14 |  | fine as spelled (0.83) |
| Julia | Julia | /dʒˈuːljə/ | Romans 16:15 |  | fine as spelled (0.80) |
| Nereus | Nereus | /ˈnɪəriəs/ | Romans 16:15 |  | fine as spelled (1.00) |
| Olympas | Olympas | /ˈoʊ.ləm.pəs/ | Romans 16:15 |  | unsure (guessed IPA) (0.79) |
| Philologus | Philologus | /fiˈloʊ.lə.ɡəs/ | Romans 16:15 |  | unsure (guessed IPA) (0.67) |
| Sosipater | Sosipater | /səˈsi.pə.tər/ | Romans 16:21 |  | unsure (guessed IPA) (0.56) |
| Tertius | Tertius | /tˈɚtiːɪs/ | Romans 16:22 |  | still wrong (0.57) |
| Quartus | Quartus | /ˈkjuː.ər.təs/ | Romans 16:23 |  | unsure (guessed IPA) (0.25) |
| Chloe | Chloe | /klˈoʊiː/ | 1 Corinthians 1:11 |  | fine as spelled (0.88) |
| Stephanas | Stephanas | /ˈstiː.fə.nəs/ | 1 Corinthians 1:16 |  | unsure (guessed IPA) (0.75) |
| Achaicus | Achaicus | /ˈeɪ.keɪ.səs/ | 1 Corinthians 16:17 |  | unsure (guessed IPA) (0.50) |
| Fortunatus | Fortunatus | /fərˈtjuː.nə.təs/ | 1 Corinthians 16:17 |  | unsure (guessed IPA) (0.55) |
| Silvanus | Silvanus | /ˈsɪl.və.nəs/ | 2 Corinthians 1:19 |  | fine as spelled (0.88) |
| Titus | Titus | /tˈaɪtəs/ | 2 Corinthians 2:13 |  | fine as spelled (0.80) |
| Belial | Belial | /ˈbiː.li.əl/ | 2 Corinthians 6:15 |  | fine as spelled (1.00) |
| Aretas | Aretas | /ˈeɪ.rə.təs/ | 2 Corinthians 11:32 |  | unsure (guessed IPA) (0.25) |
| Damascenes | Damascenes | /dəˈmæs.sə.nəs/ | 2 Corinthians 11:32 |  | unsure (guessed IPA) (0.50) |
| Galatians | Galatians | /ɡəˈleɪʃənz/ | Galatians 3:1 |  | fine as spelled (0.88) |
| Epaphroditus | Epaphroditus | /ə.pəˈfroʊ.di.təs/ | Philippians 2:25 |  | unsure (guessed IPA) (0.52) |
| Euodia | Euodia | /juːˈoʊ.di.ə/ | Philippians 4:2 |  | fine as spelled (0.92) |
| Syntyche | Syntyche | /ˈsɪn.tə.kiː/ | Philippians 4:2 |  | unsure (guessed IPA) (0.57) |
| Clement | Clement | /klˈɛmənt/ | Philippians 4:3 |  | fine as spelled (1.00) |
| Philippians | Philippians | /fəˈlɪpiənz/ | Philippians 4:15 |  | fine as spelled (0.89) |
| Colossae | Colossae | /kəˈlɒsi/ | Colossians 1:2 |  | fine as spelled (1.00) |
| Epaphras | Epaphras | /ˈiː.pə.frəs/ | Colossians 1:7 |  | unsure (guessed IPA) (0.62) |
| Laodicea | Laodicea | /ˌleɪ.ədɪˈsiːə/ | Colossians 2:1 |  | still wrong (0.71) |
| Deity | Deity | /dˈiːətiː/ | Colossians 2:9 |  | still wrong (0.60) |
| Scythian | Scythian | /sˈɪθiːən/ | Colossians 3:11 |  | fine as spelled (1.00) |
| Onesimus | Onesimus | /əˈniː.si.məs/ | Colossians 4:9 |  | unsure (guessed IPA) (0.50) |
| Hierapolis | Hierapolis | /haɪˈreɪ.pə.lɪs/ | Colossians 4:13 |  | fine as spelled (0.84) |
| Demas | Demas | /dˈiːməs/ | Colossians 4:14 |  | fine as spelled (0.80) |
| Nymphas | Nymphas | /ˈnɪm.fəs/ | Colossians 4:15 |  | fine as spelled (1.00) |
| Laodiceans | Laodiceans | /ləˈoʊ.di.siːns/ | Colossians 4:16 |  | unsure (guessed IPA) (0.50) |
| Archippus | Archippus | /ærkˈɪpəs/ | Colossians 4:17 |  | still wrong (0.71) |
| Hymenaeus | Hymenaeus | /həˈmiː.nə.juːs/ | 1 Timothy 1:20 |  | unsure (guessed IPA) (0.44) |
| Eunice | Eunice | /jˈuːnəs/ | 2 Timothy 1:5 |  | still wrong (0.50) |
| Lois | Lois | /lˈoʊəs/ | 2 Timothy 1:5 |  | still wrong (0.75) |
| Hermogenes | Hermogenes | /hərˈmoʊ.ɡə.nəs/ | 2 Timothy 1:15 |  | unsure (guessed IPA) (0.40) |
| Phygelus | Phygelus | /ˈfaɪ.ɡə.ləs/ | 2 Timothy 1:15 |  | unsure (guessed IPA) (0.57) |
| Onesiphorus | Onesiphorus | /ə.nəˈsi.fə.rəs/ | 2 Timothy 1:16 |  | fine as spelled (0.80) |
| Philetus | Philetus | /ˈfi.lə.təs/ | 2 Timothy 2:17 |  | unsure (guessed IPA) (0.50) |
| Jambres | Jambres | /ˈdʒæm.brəs/ | 2 Timothy 3:8 |  | unsure (guessed IPA) (0.50) |
| Jannes | Jannes | /ˈdʒæn.nəs/ | 2 Timothy 3:8 |  | unsure (guessed IPA) (0.40) |
| God-breathed | God-breathed | /ˈɡɒd.ˈbriː.θəd/ | 2 Timothy 3:16 |  | unsure (guessed IPA) (0.72) |
| Dalmatia | Dalmatia | /dælˈmeɪʃə/ | 2 Timothy 4:10 |  | fine as spelled (0.86) |
| Luke | Luke | /lˈuːk/ | 2 Timothy 4:11 |  | fine as spelled (1.00) |
| Carpus | Carpus | /ˈsær.pəs/ | 2 Timothy 4:13 |  | unsure (guessed IPA) (0.50) |
| Claudia | Claudia | /klˈɔdiːə/ | 2 Timothy 4:21 |  | fine as spelled (1.00) |
| Linus | Linus | /lˈaɪnəs/ | 2 Timothy 4:21 |  | fine as spelled (1.00) |
| Pudens | Pudens | /ˈpjuː.dəns/ | 2 Timothy 4:21 |  | fine as spelled (1.00) |
| Artemas | Artemas | /ˈɑrtɪməz/ | Titus 3:12 |  | still wrong (0.57) |
| Nicopolis | Nicopolis | /niˈsoʊ.pə.lɪs/ | Titus 3:12 |  | unsure (guessed IPA) (0.67) |
| Zenas | Zenas | /zˈiːnəz/ | Titus 3:13 |  | fine as spelled (0.90) |
| Philemon | Philemon | /fəlˈeɪmən/ | Philemon 1:1 |  | still wrong (0.71) |
| Apphia | Apphia | /ˈæp.fi.ə/ | Philemon 1:2 |  | fine as spelled (0.80) |
| Levitical | Levitical | /ləˈvi.ti.səl/ | Hebrews 7:11 |  | unsure (guessed IPA) (0.56) |
| Holies | Holies | /ˈhoʊ.laɪs/ | Hebrews 9:3 |  | unsure (guessed IPA) (0.60) |
| Italians | Italians | /ɪtˈæljənz/ | Hebrews 13:24 |  | fine as spelled (0.94) |
| Tartarus | Tartarus | /ˈtɑː(r)tərəs/ | 2 Peter 2:4 |  | still wrong (0.65) |
| Antichrist | Antichrist | /ˈantiˌkɹaɪst/ | 1 John 2:18 |  | fine as spelled (0.89) |
| Diotrephes | Diotrephes | /diˈɒt.rə.fəs/ | 3 John 1:9 |  | unsure (guessed IPA) (0.56) |
| Alpha | Alpha | /ˈælfə/ | Revelation 1:8 |  | fine as spelled (1.00) |
| Omega | Omega | /oʊmˈɛɡə/ | Revelation 1:8 |  | fine as spelled (0.80) |
| Patmos | Patmos | /ˈpæt.məs/ | Revelation 1:9 |  | unsure (guessed IPA) (0.75) |
| Pergamum | Pergamum | /ˈpɜːɡəməm/ | Revelation 1:11 |  | fine as spelled (1.00) |
| Philadelphia | Philadelphia | /fɪlədˈɛlfiːə/ | Revelation 1:11 |  | fine as spelled (0.85) |
| Sardis | Sardis | /ˈsær.dɪs/ | Revelation 1:11 |  | fine as spelled (0.83) |
| Smyrna | Smyrna | /smˈɚnə/ | Revelation 1:11 |  | fine as spelled (0.83) |
| Nicolaitans | Nicolaitans | /niˈsoʊ.leɪ.təns/ | Revelation 2:6 |  | unsure (guessed IPA) (0.33) |
| Antipas | Antipas | /ˈæn.ti.pəs/ | Revelation 2:13 |  | fine as spelled (0.86) |
| BABYLON | BABYLON | /bˈæbəlɑn/ | Revelation 17:5 |  | fine as spelled (0.93) |

**Checked:** 0 unchecked, 1345 fine as spelled, 516 overridden, 133 suggestion waiting, 417 still wrong, 916 unsure (guessed IPA).

_3327 names — 516 respelled for the voice, 2811 reference-only._
