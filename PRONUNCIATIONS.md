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
| Shechem | SHEK-uhm | /ˈʃɛk.əm/ | Genesis 12:6 |  | fine as spelled (1.00) |
| Ai | Ai |  | Genesis 12:8 |  | fine as spelled |
| Bethel | BETH-el | /ˈbɛθ.əl/ | Genesis 12:8 |  | fine as spelled (0.90) |
| South | South |  | Genesis 12:9 |  | fine as spelled |
| Pharaoh | FAIR-oh | /ˈfɛər.oʊ/ | Genesis 12:15 |  | still wrong (0.75) |
| Jordan | JOR-duhn | /ˈdʒɔːr.dən/ | Genesis 13:10 |  | fine as spelled (1.00) |
| Hebron | HEE-bruhn | /ˈhiː.brən/ | Genesis 13:18 |  | fine as spelled (1.00) |
| Bela | BEEla | /ˈbiː.lə/ | Genesis 14:2 | ✅ | overridden (1.00) |
| Kiriathaim | kir-ee-uh-THAY-im | /ˌkɪr.i.əˈθeɪ.ɪm/ | Genesis 14:5 |  | still wrong (0.78) |
| Seir | SEE-ur | /ˈsiː.ər/ | Genesis 14:6 |  | fine as spelled (1.00) |
| Amalekites | AM-uh-lek-ites | /ˈæm.ə.lɛk.aɪts/ | Genesis 14:7 |  | fine as spelled (0.94) |
| Tamar | TAY-mar | /ˈteɪ.mɑːr/ | Genesis 14:7 |  | fine as spelled (1.00) |
| Amorite | AM-uh-rite | /ˈæm.ə.raɪt/ | Genesis 14:13 | ✅ | overridden (1.00) |
| Aner | AY-ner | /ˈeɪ.nər/ | Genesis 14:13 |  | fine as spelled (1.00) |
| Dan | DAN | /dæn/ | Genesis 14:14 |  | still wrong (0.67) |
| Eliezer | el-ee-EE-zer | /ˌɛl.iˈiː.zər/ | Genesis 15:2 |  | fine as spelled (0.86) |
| Kenites | KEE-nites | /ˈkiː.naɪts/ | Genesis 15:19 |  | suggestion waiting (0.60) |
| Ishmael | ISH-may-el | /ˈɪʃ.meɪ.əl/ | Genesis 16:11 |  | fine as spelled (0.83) |
| Bered | BEERR-ehd | /ˈbɪər.ɛd/ | Genesis 16:14 | ✅ | overridden (0.80) |
| Abraham | AY-bruh-ham | /ˈeɪ.brə.hæm/ | Genesis 17:5 |  | fine as spelled (0.93) |
| Isaac | EYE-zuhk | /ˈaɪ.zək/ | Genesis 17:19 |  | still wrong (0.75) |
| Moab | MOH-ab | /ˈmoʊ.æb/ | Genesis 19:37 |  | fine as spelled (1.00) |
| Ben | BEN | /bɛn/ | Genesis 19:38 |  | fine as spelled (1.00) |
| Beersheba | beerrsheeba | /bɪərˈʃiː.bə/ | Genesis 21:14 | ✅ | overridden (0.93) |
| Buz | BUHZ | /bʌz/ | Genesis 22:21 |  | fine as spelled (1.00) |
| Bethuel | buh-THYOO-el | /bəˈθjuː.əl/ | Genesis 22:22 |  | fine as spelled (0.80) |
| Maacah | MAY-uh-kuh | /ˈmeɪ.ə.kə/ | Genesis 22:24 | ✅ | overridden (0.70) |
| Kiriath | KIR-ee-ath | /ˈkɪr.i.æθ/ | Genesis 23:2 |  | still wrong (0.67) |
| Keturah | kuh-TYOO-ruh | /kəˈtjʊər.ə/ | Genesis 25:1 |  | still wrong (0.71) |
| Ishbak | ISH-bak | /ˈɪʃ.bæk/ | Genesis 25:2 |  | fine as spelled (1.00) |
| Jokshan | JOK-shan | /ˈdʒɒk.ʃæn/ | Genesis 25:2 |  | fine as spelled (0.83) |
| Medan | MEE-dan | /ˈmiː.dæn/ | Genesis 25:2 | ✅ | overridden (1.00) |
| Midian | MID-ee-uhn | /ˈmɪd.i.ən/ | Genesis 25:2 |  | fine as spelled (0.83) |
| Shuah | SHOO-uh | /ˈʃuː.ə/ | Genesis 25:2 |  | fine as spelled (0.88) |
| Zimran | ZIM-ran | /ˈzɪm.ræn/ | Genesis 25:2 |  | fine as spelled (0.83) |
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
| Esau | EE-saw | /ˈiː.sɔː/ | Genesis 25:25 |  | suggestion waiting (0.71) |
| Edom | EE-duhm | /ˈiː.dəm/ | Genesis 25:30 |  | fine as spelled (1.00) |
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
| Joseph | JOH-zef | /ˈdʒoʊ.zəf/ | Genesis 30:24 |  | fine as spelled (0.80) |
| Gilead | GIL-ee-uhd | /ˈɡɪl.i.əd/ | Genesis 31:21 |  | fine as spelled (0.83) |
| Mahanaim | mayhanayihm | /ˌmeɪ.həˈneɪ.ɪm/ | Genesis 32:2 | ✅ | overridden (0.94) |
| Israel | IZ-ray-el | /ˈɪz.reɪ.əl/ | Genesis 32:28 |  | fine as spelled |
| Hivite | HYvite | /ˈhaɪ.vaɪt/ | Genesis 34:2 | ✅ | overridden (1.00) |
| Beth | BETH | /bɛθ/ | Genesis 35:7 |  | fine as spelled (1.00) |
| Allon | AL-on | /ˈæl.ɒn/ | Genesis 35:8 |  | fine as spelled (1.00) |
| Ephrath | EF-rath | /ˈɛf.ræθ/ | Genesis 35:16 |  | fine as spelled (0.80) |
| Benjamin | BEN-juh-min | /ˈbɛn.dʒə.mɪn/ | Genesis 35:18 |  | still wrong (0.75) |
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
| Amalek | AM-uh-lek | /ˈæm.ə.lɛk/ | Genesis 36:12 |  | fine as spelled (0.92) |
| Timna | TIM-nuh | /ˈtɪm.nə/ | Genesis 36:12 |  | fine as spelled (0.90) |
| Mizzah | MIZ-uh | /ˈmɪz.ə/ | Genesis 36:13 |  | fine as spelled (0.90) |
| Nahath | nayhath | /ˈneɪ.hæθ/ | Genesis 36:13 | ✅ | overridden (0.90) |
| Shammah | SHAM-uh | /ˈʃæm.ə/ | Genesis 36:13 |  | still wrong (0.75) |
| Zerah | ZAIR-uh | /ˈzɪər.ə/ | Genesis 36:13 | ✅ | overridden (0.88) |
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
| Aiah | ay-EYE-uh | /eɪˈaɪ.ə/ | Genesis 36:24 |  | still wrong (0.67) |
| Cheran | KEERR-an | /ˈkɪər.æn/ | Genesis 36:26 | ✅ | overridden (0.80) |
| Eshban | ESH-ban | /ˈɛʃ.bæn/ | Genesis 36:26 |  | still wrong (0.70) |
| Ithran | IHTH-ran | /ˈɪθ.ræn/ | Genesis 36:26 | ✅ | overridden (0.80) |
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
| Matred | maytrehd | /ˈmeɪ.trɛd/ | Genesis 36:39 | ✅ | overridden (1.00) |
| Mehetabel | mahehtuhbehl | /məˈhɛt.ə.bɛl/ | Genesis 36:39 | ✅ | overridden (0.89) |
| Mezahab | MEZ-uh-hab | /ˈmɛz.ə.hæb/ | Genesis 36:39 |  | fine as spelled (0.93) |
| Jetheth | jeethehth | /ˈdʒiː.θɛθ/ | Genesis 36:40 | ✅ | overridden (0.80) |
| Elah | EE-luh | /ˈiː.lə/ | Genesis 36:41 |  | fine as spelled (0.83) |
| Pinon | peyenon | /ˈpaɪ.nɒn/ | Genesis 36:41 | ✅ | overridden (0.92) |
| Mibzar | MIB-zar | /ˈmɪb.zɑːr/ | Genesis 36:42 |  | fine as spelled (0.83) |
| Iram | eyeruhm | /ˈaɪ.rəm/ | Genesis 36:43 | ✅ | overridden (1.00) |
| Magdiel | MAG-dee-el | /ˈmæɡ.di.ɛl/ | Genesis 36:43 | ✅ | overridden (1.00) |
| Shua | shooa | /ˈʃuː.ə/ | Genesis 38:2 | ✅ | overridden (0.83) |
| Er | urr | /ɜːr/ | Genesis 38:3 | ✅ | overridden (1.00) |
| Onan | OH-nan | /ˈoʊ.næn/ | Genesis 38:4 |  | still wrong (0.75) |
| Perez | PEE-rez | /ˈpiː.rɛz/ | Genesis 38:29 |  | fine as spelled (0.80) |
| Manasseh | muh-NAS-uh | /məˈnæs.ə/ | Genesis 41:51 |  | fine as spelled (1.00) |
| Ephraim | eefray-ihmm | /ˈiː.freɪ.ɪm/ | Genesis 41:52 | ✅ | overridden (1.00) |
| Carmi | KAR-my | /ˈkɑːr.maɪ/ | Genesis 46:9 |  | fine as spelled (1.00) |
| Hezron | HEZ-ron | /ˈhɛz.rɒn/ | Genesis 46:9 |  | fine as spelled (0.83) |
| Pallu | PAL-oo | /ˈpæl.uː/ | Genesis 46:9 |  | still wrong (0.75) |
| Jachin | JAY-kihn | /ˈdʒeɪ.kɪn/ | Genesis 46:10 | ✅ | overridden (1.00) |
| Jamin | JAY-mihn | /ˈdʒeɪ.mɪn/ | Genesis 46:10 | ✅ | overridden (1.00) |
| Gershon | GUR-shon | /ˈɡɜːr.ʃɒn/ | Genesis 46:11 |  | fine as spelled (1.00) |
| Kohath | KOH-hath | /ˈkoʊ.hæθ/ | Genesis 46:11 |  | fine as spelled (0.90) |
| Merari | muh-RAY-reye | /məˈreɪ.raɪ/ | Genesis 46:11 | ✅ | overridden (1.00) |
| Hamul | HAY-muhl | /ˈheɪ.məl/ | Genesis 46:12 |  | fine as spelled (0.80) |
| Shimron | SHIM-ron | /ˈʃɪm.rɒn/ | Genesis 46:13 |  | fine as spelled (0.83) |
| Tola | TOH-luh | /ˈtoʊ.lə/ | Genesis 46:13 |  | fine as spelled (1.00) |
| Ezbon | EZ-bon | /ˈɛz.bɒn/ | Genesis 46:16 |  | fine as spelled (0.80) |
| Beriah | buh-RY-uh | /bəˈraɪ.ə/ | Genesis 46:17 |  | fine as spelled (1.00) |
| Heber | HEE-ber | /ˈhiː.bər/ | Genesis 46:17 |  | fine as spelled (0.90) |
| Imnah | IM-nuh | /ˈɪm.nə/ | Genesis 46:17 |  | fine as spelled (1.00) |
| Ishvah | ISH-vuh | /ˈɪʃ.və/ | Genesis 46:17 |  | fine as spelled (1.00) |
| Ishvi | ihshveye | /ˈɪʃ.vaɪ/ | Genesis 46:17 | ✅ | overridden (1.00) |
| Malchiel | MAL-kee-el | /ˈmæl.ki.ɛl/ | Genesis 46:17 |  | suggestion waiting (0.71) |
| Serah | SEE-ruh | /ˈsɪər.ə/ | Genesis 46:17 |  | still wrong (0.75) |
| Ashbel | ASH-bel | /ˈæʃ.bɛl/ | Genesis 46:21 |  | suggestion waiting (0.70) |
| Becher | beekuhr | /ˈbiː.kər/ | Genesis 46:21 | ✅ | overridden (1.00) |
| Gera | GEE-ruh | /ˈɡɪər.ə/ | Genesis 46:21 |  | suggestion waiting (0.75) |
| Huppim | HUP-im | /ˈhʌp.ɪm/ | Genesis 46:21 |  | fine as spelled (0.80) |
| Naaman | NAY-uh-muhn | /ˈneɪ.ə.mən/ | Genesis 46:21 | ✅ | overridden (0.83) |
| Hushim | hyooshihm | /ˈhjuː.ʃɪm/ | Genesis 46:23 | ✅ | overridden (0.86) |
| Guni | GYOO-ny | /ˈɡjuː.naɪ/ | Genesis 46:24 |  | still wrong (0.50) |
| Jezer | JEE-zer | /ˈdʒiː.zər/ | Genesis 46:24 |  | fine as spelled (0.80) |
| Machir | maykuhr | /ˈmeɪ.kər/ | Genesis 50:23 | ✅ | overridden (1.00) |
| Puah | PYOO-uh | /ˈpjuː.ə/ | Exodus 1:15 |  | still wrong (0.25) |
| Moses | MOH-ziz | /ˈmoʊ.zɪz/ | Exodus 2:10 |  | fine as spelled (1.00) |
| Gershom | GUR-shuhm | /ˈɡɜːr.ʃəm/ | Exodus 2:22 |  | fine as spelled (0.83) |
| Jebusite | JEB-yoo-site | /ˈdʒɛb.jʊ.saɪt/ | Exodus 3:8 | ✅ | overridden (1.00) |
| Aaron | AIR-uhn | /ˈɛər.ən/ | Exodus 4:14 |  | fine as spelled (1.00) |
| fathers' | fathers | /ˈfɑː.ðərz/ | Exodus 6:14 | ✅ | overridden (1.00) |
| fathers’ | fathers | /ˈfɑː.ðərz/ | Exodus 6:14 | ✅ | overridden (1.00) |
| Libni | LIB-ny | /ˈlɪb.naɪ/ | Exodus 6:17 |  | fine as spelled (0.80) |
| Shimei | SHIM-ee-eye | /ˈʃɪm.i.aɪ/ | Exodus 6:17 |  | fine as spelled (0.80) |
| Amram | AM-ram | /ˈæm.ræm/ | Exodus 6:18 | ✅ | overridden (0.90) |
| Izhar | IZ-har | /ˈɪz.hɑːr/ | Exodus 6:18 |  | fine as spelled (0.80) |
| Uzziel | UZ-ee-el | /ˈʌz.i.ɛl/ | Exodus 6:18 |  | still wrong (0.70) |
| Levites | LEE-vites | /ˈliː.vaɪts/ | Exodus 6:19 |  |  |
| Mahli | MAH-ly | /ˈmɑː.laɪ/ | Exodus 6:19 |  | suggestion waiting (0.75) |
| Mushi | myoosheye | /ˈmjuː.ʃaɪ/ | Exodus 6:19 | ✅ | overridden (0.80) |
| Nepheg | NEE-feg | /ˈniː.fɛɡ/ | Exodus 6:21 |  | fine as spelled (0.80) |
| Zichri | ZIHK-reye | /ˈzɪk.raɪ/ | Exodus 6:21 | ✅ | overridden (1.00) |
| Abihu | uh-BY-hyoo | /əˈbaɪ.hjuː/ | Exodus 6:23 |  | still wrong (0.67) |
| Amminadab | uh-MIHN-uh-dab | /əˈmɪn.ə.dæb/ | Exodus 6:23 | ✅ | overridden (1.00) |
| Eleazar | el-ee-AY-zer | /ˌɛl.iˈeɪ.zər/ | Exodus 6:23 |  | fine as spelled (1.00) |
| Ithamar | ITH-uh-mar | /ˈɪθ.ə.mɑːr/ | Exodus 6:23 |  | fine as spelled (1.00) |
| Nadab | NAY-dab | /ˈneɪ.dæb/ | Exodus 6:23 |  | fine as spelled (1.00) |
| Nahshon | NAH-shon | /ˈnɑː.ʃɒn/ | Exodus 6:23 | ✅ | overridden (1.00) |
| Assir | AS-ur | /ˈæs.ər/ | Exodus 6:24 |  | still wrong (0.62) |
| Elkanah | el-KAY-nuh | /ɛlˈkeɪ.nə/ | Exodus 6:24 | ✅ | overridden (0.92) |
| Korahites | KOR-uh-hites | /ˈkɔːr.ə.haɪts/ | Exodus 6:24 |  | fine as spelled (0.88) |
| Phinehas | FIN-ee-uhs | /ˈfɪn.i.əs/ | Exodus 6:25 |  | suggestion waiting (0.71) |
| Miriam | MIR-ee-uhm | /ˈmɪr.i.əm/ | Exodus 15:20 |  | fine as spelled (1.00) |
| Joshua | JOSH-oo-uh | /ˈdʒɒʃ.u.ə/ | Exodus 17:9 |  | fine as spelled (0.92) |
| Hur | HUR | /hɜːr/ | Exodus 17:10 |  | still wrong (0.67) |
| Bezalel | BEZ-uh-lel | /ˈbɛz.ə.lɛl/ | Exodus 31:2 |  | still wrong (0.71) |
| Uri | YOORR-eye | /ˈjʊər.aɪ/ | Exodus 31:2 | ✅ | overridden (0.75) |
| Nun | NUHN | /nʌn/ | Exodus 33:11 |  | fine as spelled (1.00) |
| Shelomith | shuh-LOH-mith | /ʃəˈloʊ.mɪθ/ | Leviticus 24:11 |  | suggestion waiting (0.71) |
| Nethanel | nuh-THAN-el | /nəˈθæn.əl/ | Numbers 1:8 |  | still wrong (0.71) |
| Eliab | ee-LY-ab | /ɪˈlaɪ.æb/ | Numbers 1:9 |  | fine as spelled (0.80) |
| Ammihud | ameyehuhd | /əˈmaɪ.hʌd/ | Numbers 1:10 | ✅ | overridden (1.00) |
| Elishama | ihlihshuhmuh | /ɪˈlɪʃ.ə.mə/ | Numbers 1:10 | ✅ | overridden (0.86) |
| Kohathites | KOH-hath-ites | /ˈkoʊ.hæθ.aɪts/ | Numbers 3:27 |  | fine as spelled (0.88) |
| Abihail | ab-ih-HAY-il | /ˌæb.ɪˈheɪ.ɪl/ | Numbers 3:35 |  | still wrong (0.57) |
| Zaccur | ZAK-er | /ˈzæk.ər/ | Numbers 13:4 |  | fine as spelled (1.00) |
| Shaphat | SHAY-fat | /ˈʃeɪ.fæt/ | Numbers 13:5 | ✅ | overridden (1.00) |
| Caleb | KAY-leb | /ˈkeɪ.ləb/ | Numbers 13:6 |  | fine as spelled (1.00) |
| Jephunneh | juh-FUN-uh | /dʒəˈfʌn.ə/ | Numbers 13:6 |  | fine as spelled (0.83) |
| Igal | EYE-gal | /ˈaɪ.ɡæl/ | Numbers 13:7 |  | still wrong (0.50) |
| Ammiel | AM-ee-el | /ˈæm.i.ɛl/ | Numbers 13:12 |  | still wrong (0.70) |
| Michael | MY-kuhl | /ˈmaɪ.kəl/ | Numbers 13:13 |  | fine as spelled (1.00) |
| Rehob | REE-hob | /ˈriː.hɒb/ | Numbers 13:21 |  | fine as spelled (0.90) |
| Ahiman | uh-HY-muhn | /əˈhaɪ.mən/ | Numbers 13:22 |  | fine as spelled (1.00) |
| Talmai | TAL-my | /ˈtæl.maɪ/ | Numbers 13:22 |  | fine as spelled (1.00) |
| Hormah | HOR-muh | /ˈhɔːr.mə/ | Numbers 14:45 |  | still wrong (0.60) |
| Peleth | PEE-lehth | /ˈpiː.lɛθ/ | Numbers 16:1 | ✅ | overridden (0.80) |
| Arad | AIR-ad | /ˈɛər.æd/ | Numbers 21:1 |  | still wrong (0.50) |
| Heshbon | HEHSH-bon | /ˈhɛʃ.bɒn/ | Numbers 21:25 | ✅ | overridden (1.00) |
| Jazer | JAY-zer | /ˈdʒeɪ.zər/ | Numbers 21:32 |  | fine as spelled (0.80) |
| Bashan | BAY-shan | /ˈbeɪ.ʃæn/ | Numbers 21:33 |  | fine as spelled (0.80) |
| Jericho | JER-ih-koh | /ˈdʒɛr.ɪ.koʊ/ | Numbers 22:1 |  | fine as spelled (1.00) |
| Zimri | zihmreye | /ˈzɪm.raɪ/ | Numbers 25:14 | ✅ | overridden (1.00) |
| Zur | zurr | /zɜːr/ | Numbers 25:15 | ✅ | overridden (1.00) |
| Reubenites | ROO-ben-ites | /ˈruː.bən.aɪts/ | Numbers 26:7 |  | fine as spelled (0.84) |
| Nemuel | NEM-yoo-el | /ˈnɛm.jʊ.əl/ | Numbers 26:9 |  | still wrong (0.73) |
| Jashub | JAY-shub | /ˈdʒeɪ.ʃʌb/ | Numbers 26:24 |  | fine as spelled (0.80) |
| Asriel | AS-ree-el | /ˈæs.ri.ɛl/ | Numbers 26:31 |  | still wrong (0.67) |
| Hepher | HEE-fer | /ˈhiː.fər/ | Numbers 26:32 |  | fine as spelled (0.80) |
| Shemida | shuh-MY-duh | /ʃəˈmaɪ.də/ | Numbers 26:32 | ✅ | overridden (0.83) |
| Mahlah | MAH-luh | /ˈmɑː.lə/ | Numbers 26:33 |  | fine as spelled (1.00) |
| Zelophehad | zuh-LOH-fuh-had | /zəˈloʊ.fə.hæd/ | Numbers 26:33 | ✅ | overridden (0.83) |
| Shuthelah | shoo-THEE-luh | /ʃuːˈθiː.lə/ | Numbers 26:35 |  | still wrong (0.62) |
| Tahan | TAY-han | /ˈteɪ.hæn/ | Numbers 26:35 | ✅ | overridden (0.80) |
| Rekem | REE-kem | /ˈriː.kɛm/ | Numbers 31:8 |  | fine as spelled (0.80) |
| Nebo | NEE-boh | /ˈniː.boʊ/ | Numbers 32:3 |  | fine as spelled (1.00) |
| Aroer | uh-ROH-uhrr | /əˈroʊ.ər/ | Numbers 32:34 | ✅ | overridden (1.00) |
| Meon | MEE-on | /ˈmiː.ɒn/ | Numbers 32:38 |  | suggestion waiting (0.75) |
| Jair | jayuhr | /ˈdʒeɪ.ər/ | Numbers 32:41 | ✅ | overridden (1.00) |
| Kenath | KEE-naath | /ˈkiː.næθ/ | Numbers 32:42 | ✅ | overridden (0.70) |
| Rimmon | RIM-uhn | /ˈrɪm.ən/ | Numbers 33:19 |  | fine as spelled (1.00) |
| Libnah | LIB-nuh | /ˈlɪb.nə/ | Numbers 33:20 |  | fine as spelled (0.80) |
| Tahath | TAY-hath | /ˈteɪ.hæθ/ | Numbers 33:26 | ✅ | overridden (0.80) |
| Jaakan | JAY-uh-kan | /ˈdʒeɪ.ə.kæn/ | Numbers 33:31 | ✅ | overridden (0.83) |
| Addar | AD-ar | /ˈæd.ɑːr/ | Numbers 34:4 |  | suggestion waiting (0.75) |
| Hazar | HAY-zar | /ˈheɪ.zɑːr/ | Numbers 34:4 |  | fine as spelled (0.80) |
| Ain | AY-in | /ˈeɪ.ɪn/ | Numbers 34:11 |  | still wrong (0.33) |
| Shemuel | shuh-MYOO-el | /ʃəˈmjuː.əl/ | Numbers 34:20 |  | still wrong (0.75) |
| Bukki | buhkeye | /ˈbʌk.aɪ/ | Numbers 34:22 | ✅ | overridden (1.00) |
| Hanniel | HAN-ee-el | /ˈhæn.i.ɛl/ | Numbers 34:23 |  | still wrong (0.58) |
| Ahihud | uh-HEYE-huhd | /əˈhaɪ.hʌd/ | Numbers 34:27 | ✅ | overridden (1.00) |
| Ashtaroth | ASH-tuh-roth | /ˈæʃ.tə.rɒθ/ | Deuteronomy 1:4 |  | fine as spelled (1.00) |
| Kedemoth | KED-uh-moth | /ˈkɛd.ə.mɒθ/ | Deuteronomy 2:26 |  | fine as spelled (1.00) |
| Hermon | HUR-muhn | /ˈhɜːr.mən/ | Deuteronomy 3:8 |  | fine as spelled (0.83) |
| Senir | SEE-nuhr | /ˈsiː.nər/ | Deuteronomy 3:9 | ✅ | overridden (1.00) |
| Salecah | SAL-uh-kuh | /ˈsæl.ə.kə/ | Deuteronomy 3:10 | ✅ | overridden (0.83) |
| Gadites | GAD-ites | /ˈɡæd.aɪts/ | Deuteronomy 3:12 |  | fine as spelled (0.83) |
| Bezer | BEE-zer | /ˈbiː.zər/ | Deuteronomy 4:43 |  | fine as spelled (0.80) |
| Golan | GOH-lan | /ˈɡoʊ.læn/ | Deuteronomy 4:43 |  | fine as spelled (0.80) |
| Ramoth | raymahth | /ˈreɪ.mɒθ/ | Deuteronomy 4:43 | ✅ | overridden (1.00) |
| Girgashite | GUR-guh-shite | /ˈɡɜːr.ɡə.ʃaɪt/ | Deuteronomy 7:1 |  | still wrong (0.75) |
| Zabdi | ZAB-deye | /ˈzæb.daɪ/ | Joshua 7:1 | ✅ | overridden (1.00) |
| Gibeon | GIB-ee-uhn | /ˈɡɪb.i.ən/ | Joshua 9:3 |  | fine as spelled (0.92) |
| Jearim | JEE-uh-rihm | /ˈdʒiː.ə.rɪm/ | Joshua 9:17 | ✅ | overridden (1.00) |
| Jerusalem | juh-ROO-suh-lem | /dʒəˈruː.sə.ləm/ | Joshua 10:1 |  | fine as spelled (1.00) |
| Debir | DEE-buhr | /ˈdiː.bər/ | Joshua 10:3 | ✅ | overridden (1.00) |
| Japhia | juhfeyeuh | /dʒəˈfaɪ.ə/ | Joshua 10:3 | ✅ | overridden (0.80) |
| Horon | HOR-on | /ˈhɔːr.ɒn/ | Joshua 10:10 |  | fine as spelled (0.80) |
| Aijalon | AJ-uh-lon | /ˈædʒ.ə.lɒn/ | Joshua 10:12 |  | still wrong (0.58) |
| Gezer | GEE-zer | /ˈɡiː.zər/ | Joshua 10:33 |  | fine as spelled (0.80) |
| Dor | DOR | /dɔːr/ | Joshua 11:2 |  | still wrong (0.67) |
| Gath | GATH | /ɡæθ/ | Joshua 11:22 |  | fine as spelled (0.83) |
| Tappuah | tuh-PYOO-uh | /təˈpjuː.ə/ | Joshua 12:17 |  | still wrong (0.77) |
| Megiddo | muh-GID-oh | /məˈɡɪd.oʊ/ | Joshua 12:21 |  | fine as spelled (0.83) |
| Taanach | TAY-uh-nak | /ˈteɪ.ə.næk/ | Joshua 12:21 |  | still wrong (0.58) |
| Kedesh | KEE-desh | /ˈkiː.dɛʃ/ | Joshua 12:22 |  | fine as spelled (0.80) |
| Geshur | GESH-uhr | /ˈɡɛʃ.ər/ | Joshua 13:13 | ✅ | overridden (0.90) |
| Mephaath | muh-FAY-athh | /məˈfeɪ.æθ/ | Joshua 13:18 | ✅ | overridden (0.92) |
| Zereth | ZEE-reth | /ˈzɪər.ɛθ/ | Joshua 13:19 |  | fine as spelled (0.80) |
| Shemesh | SHEM-esh | /ˈʃɛm.ɛʃ/ | Joshua 15:7 |  | fine as spelled (1.00) |
| Achsah | AK-suh | /ˈæk.sə/ | Joshua 15:16 |  | fine as spelled (1.00) |
| Othniel | OTH-nee-el | /ˈɒθ.ni.əl/ | Joshua 15:17 |  | fine as spelled (0.83) |
| Ziph | ZIF | /zɪf/ | Joshua 15:24 |  | fine as spelled (1.00) |
| Moladah | MOH-la-duh | /ˈmoʊ.lə.də/ | Joshua 15:26 | ✅ | overridden (1.00) |
| Shema | SHEE-muh | /ˈʃiː.mə/ | Joshua 15:26 |  | fine as spelled (1.00) |
| Pelet | PEE-let | /ˈpiː.lɛt/ | Joshua 15:27 | ✅ | overridden (0.90) |
| Shual | SHOO-uhl | /ˈʃuː.əl/ | Joshua 15:28 |  | still wrong (0.50) |
| Ezem | EE-zem | /ˈiː.zɛm/ | Joshua 15:29 |  | suggestion waiting (0.75) |
| Madmannah | mad-MANN-uh | /mædˈmæn.ə/ | Joshua 15:31 | ✅ | overridden (0.86) |
| Ziklag | ZIK-lag | /ˈzɪk.læɡ/ | Joshua 15:31 |  | fine as spelled (1.00) |
| Zanoah | zuh-NOH-uh | /zəˈnoʊ.ə/ | Joshua 15:34 |  | fine as spelled (1.00) |
| Gederah | gadeerruh | /ɡəˈdɪər.ə/ | Joshua 15:36 | ✅ | overridden (1.00) |
| Shaaraim | shay-uh-RAY-im | /ˌʃeɪ.əˈreɪ.ɪm/ | Joshua 15:36 |  | still wrong (0.71) |
| Ashan | AY-shan | /ˈeɪ.ʃæn/ | Joshua 15:42 |  | still wrong (0.50) |
| Keilah | kee-EYE-luh | /kiˈaɪ.lə/ | Joshua 15:44 |  | still wrong (0.70) |
| Mareshah | muh-REESH-uh | /məˈriː.ʃə/ | Joshua 15:44 | ✅ | overridden (1.00) |
| Jattir | JAT-ur | /ˈdʒæt.ər/ | Joshua 15:48 |  | fine as spelled (0.80) |
| Maon | MAY-on | /ˈmeɪ.ɒn/ | Joshua 15:55 |  | still wrong (0.75) |
| Jezreel | JEZ-ree-el | /ˈdʒɛz.ri.əl/ | Joshua 15:56 |  | fine as spelled (1.00) |
| Gedor | geedawr | /ˈɡiː.dɔːr/ | Joshua 15:58 | ✅ | overridden (0.80) |
| Naarah | NAY-a-ruh | /ˈneɪ.ə.rə/ | Joshua 16:7 | ✅ | overridden (0.80) |
| Abiezer | ay-bee-EE-zer | /ˌeɪ.biˈiː.zər/ | Joshua 17:2 |  | still wrong (0.71) |
| Shean | SHEE-an | /ˈʃiː.æn/ | Joshua 17:11 |  | still wrong (0.62) |
| Ophrah | OF-ruh | /ˈɒf.rə/ | Joshua 18:23 |  | still wrong (0.75) |
| Geba | GEE-buh | /ˈɡiː.bə/ | Joshua 18:24 |  | still wrong (0.68) |
| Marcaboth | MAR-kuh-both | /ˈmɑːr.kə.bɒθ/ | Joshua 19:5 |  | fine as spelled (0.94) |
| Daberath | DAB-uh-rath | /ˈdæb.ə.ræθ/ | Joshua 19:12 |  | fine as spelled (0.93) |
| Tabor | TAY-ber | /ˈteɪ.bər/ | Joshua 19:12 |  | fine as spelled (1.00) |
| Hammon | HAM-uhn | /ˈhæm.ən/ | Joshua 19:28 |  | fine as spelled (0.90) |
| Hammath | hamath | /ˈhæm.æθ/ | Joshua 19:35 | ✅ | overridden (0.70) |
| Galilee | GAL-ih-lee | /ˈɡæl.ɪ.liː/ | Joshua 20:7 |  | fine as spelled (0.83) |
| Eshtemoa | esh-tuh-MOH-uh | /ˌɛʃ.təˈmoʊ.ə/ | Joshua 21:14 |  | fine as spelled (0.88) |
| Anathoth | AN-uh-thoth | /ˈæn.ə.θɒθ/ | Joshua 21:18 |  | still wrong (0.75) |
| Abdon | AB-don | /ˈæb.dɒn/ | Joshua 21:30 |  | fine as spelled (0.80) |
| Ehud | eehud | /ˈiː.hʌd/ | Judges 3:15 | ✅ | overridden (1.00) |
| Joash | JOH-ash | /ˈdʒoʊ.æʃ/ | Judges 6:11 |  | suggestion waiting (0.75) |
| Penuel | puh-NYOO-el | /pəˈnjuː.əl/ | Judges 8:8 |  | still wrong (0.57) |
| Jether | JEE-thuhr | /ˈdʒiː.θər/ | Judges 8:20 | ✅ | overridden (0.90) |
| Jotham | JOH-thuhm | /ˈdʒoʊ.θəm/ | Judges 9:5 |  | fine as spelled (0.80) |
| Etam | eetum | /ˈiː.təm/ | Judges 15:8 | ✅ | overridden (0.75) |
| Micah | MY-kuh | /ˈmaɪ.kə/ | Judges 17:1 |  | fine as spelled (1.00) |
| Jonathan | JON-uh-thuhn | /ˈdʒɒn.ə.θən/ | Judges 18:30 |  | fine as spelled (1.00) |
| Boaz | BOH-az | /ˈboʊ.æz/ | Ruth 2:1 |  | fine as spelled (1.00) |
| Ephrathah | EF-ruh-thuh | /ˈɛf.rə.θə/ | Ruth 4:11 |  | fine as spelled (0.83) |
| David | DAY-vid | /ˈdeɪ.vɪd/ | Ruth 4:17 |  | fine as spelled (1.00) |
| Jesse | JES-ee | /ˈdʒɛs.i/ | Ruth 4:17 |  | fine as spelled (1.00) |
| Obed | OH-bed | /ˈoʊ.bɛd/ | Ruth 4:17 |  | still wrong (0.75) |
| Ram | RAM | /ræm/ | Ruth 4:19 |  | fine as spelled (1.00) |
| Jeroham | juh-ROH-ham | /dʒəˈroʊ.hæm/ | 1 Samuel 1:1 | ✅ | overridden (0.86) |
| Zuph | ZUHF | /zʌf/ | 1 Samuel 1:1 |  | fine as spelled (1.00) |
| Samuel | SAM-yoo-el | /ˈsæm.jʊ.əl/ | 1 Samuel 1:20 |  | still wrong (0.75) |
| Abinadab | uh-BIN-uh-dab | /əˈbɪn.ə.dæb/ | 1 Samuel 7:1 |  | fine as spelled (1.00) |
| Abijah | uh-BY-juh | /əˈbaɪ.dʒə/ | 1 Samuel 8:2 |  | fine as spelled (0.80) |
| Joel | JOH-uhll | /ˈdʒoʊ.əl/ | 1 Samuel 8:2 | ✅ | overridden (1.00) |
| Kish | KISH | /kɪʃ/ | 1 Samuel 9:1 |  | fine as spelled (1.00) |
| Saul | SAWL | /sɔːl/ | 1 Samuel 9:2 |  | fine as spelled (0.83) |
| Nahash | NAY-hash | /ˈneɪ.hæʃ/ | 1 Samuel 11:1 | ✅ | overridden (1.00) |
| Bedan | BEE-dan | /ˈbiː.dæn/ | 1 Samuel 12:11 |  | suggestion waiting (0.70) |
| Ahijah | uh-HY-juh | /əˈhaɪ.dʒə/ | 1 Samuel 14:3 |  | fine as spelled (0.80) |
| Ahitub | uh-HEYE-tuhb | /əˈhaɪ.tʌb/ | 1 Samuel 14:3 | ✅ | overridden (1.00) |
| Malchishua | mal-keye-SHOO-uh | /ˌmæl.kaɪˈʃuː.ə/ | 1 Samuel 14:49 | ✅ | overridden (0.83) |
| Ahimaaz | uh-HIM-ay-az | /əˈhɪm.eɪ.æz/ | 1 Samuel 14:50 |  | still wrong (0.50) |
| Ahinoam | uh-HIN-oh-am | /əˈhɪn.oʊ.æm/ | 1 Samuel 14:50 |  | still wrong (0.50) |
| Ner | NUR | /nɜːr/ | 1 Samuel 14:50 |  | still wrong (0.50) |
| Abigail | AB-ih-gayl | /ˈæb.ɪ.ɡeɪl/ | 1 Samuel 25:3 |  | fine as spelled (1.00) |
| Abishai | uh-BISH-eye | /əˈbɪʃ.aɪ/ | 1 Samuel 26:6 |  | fine as spelled (0.83) |
| Joab | JOH-ab | /ˈdʒoʊ.æb/ | 1 Samuel 26:6 |  | fine as spelled (1.00) |
| Zeruiah | zeh-roo-EYE-uh | /ˌzɛr.uːˈaɪ.ə/ | 1 Samuel 26:6 | ✅ | overridden (0.83) |
| Carmelitess | KAR-mel-ite-ess | /ˈkɑːr.mə.laɪ.tɛs/ | 1 Samuel 27:3 |  | fine as spelled (0.80) |
| Jezreelitess | JEZ-ree-el-ite-ess | /ˈdʒɛz.ri.ə.laɪ.tɛs/ | 1 Samuel 27:3 |  | still wrong (0.73) |
| Asahel | AS-uh-hel | /ˈæs.ə.hɛl/ | 2 Samuel 2:18 |  | fine as spelled (1.00) |
| Amnon | AM-non | /ˈæm.nɒn/ | 2 Samuel 3:2 |  | fine as spelled (0.90) |
| Absalom | AB-suh-luhm | /ˈæb.sə.ləm/ | 2 Samuel 3:3 |  | fine as spelled (1.00) |
| Abital | uh-BY-tuhl | /əˈbaɪ.təl/ | 2 Samuel 3:4 | ✅ | overridden (0.92) |
| Adonijah | ad-oh-NY-juh | /ˌæd.oʊˈnaɪ.dʒə/ | 2 Samuel 3:4 |  | still wrong (0.71) |
| Haggith | HAG-ith | /ˈhæɡ.ɪθ/ | 2 Samuel 3:4 |  | fine as spelled (1.00) |
| Shephatiah | shef-uh-TY-uh | /ˌʃɛf.əˈtaɪ.ə/ | 2 Samuel 3:4 |  | fine as spelled (0.94) |
| Eglah | EG-luh | /ˈɛɡ.lə/ | 2 Samuel 3:5 |  | still wrong (0.62) |
| Ithream | ITH-ree-am | /ˈɪθ.ri.æm/ | 2 Samuel 3:5 |  | suggestion waiting (0.75) |
| Rechab | REE-kab | /ˈriː.kæb/ | 2 Samuel 4:2 | ✅ | overridden (1.00) |
| Nathan | NAY-thuhn | /ˈneɪ.θən/ | 2 Samuel 5:14 |  | fine as spelled (1.00) |
| Shobab | SHOH-bab | /ˈʃoʊ.bæb/ | 2 Samuel 5:14 |  | fine as spelled (1.00) |
| Solomon | SOL-uh-muhn | /ˈsɒl.ə.mən/ | 2 Samuel 5:14 |  | fine as spelled (1.00) |
| Ibhar | IB-har | /ˈɪb.hɑːr/ | 2 Samuel 5:15 |  | fine as spelled (0.83) |
| Eliada | ee-LY-uh-duh | /ɪˈlaɪ.ə.də/ | 2 Samuel 5:16 |  | still wrong (0.46) |
| Eliphelet | ee-LIF-uh-let | /ɪˈlɪf.ə.lɛt/ | 2 Samuel 5:16 |  | suggestion waiting (0.75) |
| Ahio | uh-HY-oh | /əˈhaɪ.oʊ/ | 2 Samuel 6:3 |  | fine as spelled (0.80) |
| Uzzah | UZ-uh | /ˈʌz.ə/ | 2 Samuel 6:3 |  | fine as spelled (0.88) |
| Joram | JOR-uhm | /ˈdʒɔːr.əm/ | 2 Samuel 8:10 |  | fine as spelled (0.80) |
| Jehoshaphat | juh-HOSH-uh-fat | /dʒəˈhɒʃ.ə.fæt/ | 2 Samuel 8:16 |  | fine as spelled (1.00) |
| Seraiah | suh-RAY-yuh | /səˈreɪ.jə/ | 2 Samuel 8:17 |  | still wrong (0.67) |
| Zadok | ZAY-dok | /ˈzeɪ.dɒk/ | 2 Samuel 8:17 |  | fine as spelled (0.80) |
| Benaiah | buh-NAY-yuh | /bəˈneɪ.jə/ | 2 Samuel 8:18 |  | still wrong (0.58) |
| Mica | MY-kuh | /ˈmaɪ.kə/ | 2 Samuel 9:12 |  | fine as spelled (0.90) |
| Shimeah | SHIM-ee-uh | /ˈʃɪm.i.ə/ | 2 Samuel 13:3 |  | fine as spelled (0.80) |
| Tekoa | tuh-KOH-uh | /təˈkoʊ.ə/ | 2 Samuel 14:2 |  | suggestion waiting (0.60) |
| Amasa | uh-MAY-suh | /əˈmeɪ.sə/ | 2 Samuel 17:25 | ✅ | overridden (0.80) |
| Sheva | SHEE-vuh | /ˈʃiː.və/ | 2 Samuel 20:25 |  | fine as spelled (1.00) |
| Helez | HEE-lez | /ˈhiː.lɛz/ | 2 Samuel 23:26 |  | fine as spelled (0.80) |
| Azmaveth | az-MAY-veth | /æzˈmeɪ.vɛθ/ | 2 Samuel 23:31 |  | fine as spelled (0.86) |
| Maacathite | may-AK-uh-thite | /meɪˈæk.ə.θaɪt/ | 2 Samuel 23:34 |  | fine as spelled (0.88) |
| Bani | bayneye | /ˈbeɪ.naɪ/ | 2 Samuel 23:36 | ✅ | overridden (1.00) |
| Azariah | az-uh-RY-uh | /ˌæz.əˈraɪ.ə/ | 1 Kings 4:2 |  | fine as spelled (1.00) |
| Hesed | heesehd | /ˈhiː.sɛd/ | 1 Kings 4:10 | ✅ | overridden (1.00) |
| Jokmeam | JOK-mee-am | /ˈdʒɒk.mi.æm/ | 1 Kings 4:12 |  | suggestion waiting (0.71) |
| Iddo | ID-oh | /ˈɪd.oʊ/ | 1 Kings 4:14 |  | fine as spelled (1.00) |
| Calcol | kaalkol | /ˈkæl.kɒl/ | 1 Kings 4:31 | ✅ | overridden (0.83) |
| Ethan | EE-thuhn | /ˈiː.θən/ | 1 Kings 4:31 |  | fine as spelled (1.00) |
| Jeroboam | jer-uh-BOH-uhm | /ˌdʒɛr.əˈboʊ.əm/ | 1 Kings 11:26 |  | fine as spelled (1.00) |
| Rehoboam | ree-huh-BOH-uhm | /ˌriː.həˈboʊ.əm/ | 1 Kings 11:43 |  | fine as spelled (0.81) |
| Shemaiah | shuh-MAY-yuh | /ʃəˈmeɪ.jə/ | 1 Kings 12:22 |  | still wrong (0.67) |
| Josiah | joh-SY-uh | /dʒoʊˈsaɪ.ə/ | 1 Kings 13:2 |  | fine as spelled (0.80) |
| Asa | AY-suh | /ˈeɪ.sə/ | 1 Kings 15:8 |  | fine as spelled (0.83) |
| Jehu | JEE-hyoo | /ˈdʒiː.hjuː/ | 1 Kings 16:1 | ✅ | overridden (0.72) |
| Omri | omreye | /ˈɒm.raɪ/ | 1 Kings 16:16 | ✅ | overridden (1.00) |
| Shemer | SHEE-mer | /ˈʃiː.mər/ | 1 Kings 16:24 |  | fine as spelled (0.80) |
| Segub | SEE-gub | /ˈsiː.ɡʌb/ | 1 Kings 16:34 |  | fine as spelled (0.80) |
| Elijah | ee-LY-juh | /ɪˈlaɪ.dʒə/ | 1 Kings 17:1 |  | fine as spelled (1.00) |
| Obadiah | oh-buh-DY-uh | /ˌoʊ.bəˈdaɪ.ə/ | 1 Kings 18:3 |  | fine as spelled (0.93) |
| Chenaanah | kuh-NAY-uh-nuh | /kəˈneɪ.ə.nə/ | 1 Kings 22:11 |  | still wrong (0.71) |
| Zedekiah | zed-uh-KY-uh | /ˌzɛd.əˈkaɪ.ə/ | 1 Kings 22:11 |  | fine as spelled (0.86) |
| Amon | aymuhn | /ˈeɪ.mən/ | 1 Kings 22:26 | ✅ | overridden (1.00) |
| Ahaziah | ay-huh-ZY-uh | /ˌeɪ.həˈzaɪ.ə/ | 1 Kings 22:40 |  | fine as spelled (0.83) |
| Azubah | uh-ZOO-buh | /əˈzuː.bə/ | 1 Kings 22:42 |  | fine as spelled (0.83) |
| Athaliah | ath-uh-LY-uh | /ˌæθ.əˈlaɪ.ə/ | 2 Kings 8:26 |  | fine as spelled (0.92) |
| Amaziah | am-uh-ZY-uh | /ˌæm.əˈzaɪ.ə/ | 2 Kings 12:21 |  | fine as spelled (0.92) |
| Shomer | SHOH-mer | /ˈʃoʊ.mər/ | 2 Kings 12:21 |  | fine as spelled (1.00) |
| Zechariah | zek-uh-RY-uh | /ˌzɛk.əˈraɪ.ə/ | 2 Kings 14:29 |  | fine as spelled (1.00) |
| Shallum | SHAL-uhm | /ˈʃæl.əm/ | 2 Kings 15:10 |  | fine as spelled (1.00) |
| Uzziah | uh-ZY-uh | /əˈzaɪ.ə/ | 2 Kings 15:13 |  | fine as spelled (0.90) |
| Pul | PUHL | /pʌl/ | 2 Kings 15:19 |  | still wrong (0.33) |
| Ahaz | AY-haz | /ˈeɪ.hæz/ | 2 Kings 15:38 |  | still wrong (0.75) |
| Hezekiah | hez-uh-KY-uh | /ˌhɛz.əˈkaɪ.ə/ | 2 Kings 16:20 |  | fine as spelled (0.86) |
| Gozan | GOH-zan | /ˈɡoʊ.zæn/ | 2 Kings 17:6 |  | fine as spelled (0.80) |
| Habor | HAY-bor | /ˈheɪ.bɔːr/ | 2 Kings 17:6 |  | fine as spelled (0.80) |
| Halah | HAY-la | /ˈheɪ.lə/ | 2 Kings 17:6 | ✅ | overridden (1.00) |
| Babylon | BAB-ih-luhn | /ˈbæb.ɪ.lən/ | 2 Kings 17:24 |  | still wrong (0.79) |
| Asaph | AY-saf | /ˈeɪ.sæf/ | 2 Kings 18:18 |  | still wrong (0.50) |
| Hilkiah | hil-KY-uh | /hɪlˈkaɪ.ə/ | 2 Kings 18:18 |  | fine as spelled (0.83) |
| Joah | JOH-uh | /ˈdʒoʊ.ə/ | 2 Kings 18:18 |  | fine as spelled (1.00) |
| Uzza | UZ-uh | /ˈʌz.ə/ | 2 Kings 21:18 |  | fine as spelled (0.88) |
| Adaiah | uh-DAY-yuh | /əˈdeɪ.jə/ | 2 Kings 22:1 |  | suggestion waiting (0.70) |
| Meshullam | muh-SHOOL-uhm | /məˈʃʊl.əm/ | 2 Kings 22:3 |  | still wrong (0.79) |
| Asaiah | uh-SAY-yuh | /əˈseɪ.jə/ | 2 Kings 22:12 |  | still wrong (0.50) |
| Melech | MEE-lek | /ˈmiː.lɛk/ | 2 Kings 23:11 |  | suggestion waiting (0.70) |
| Jeremiah | jer-uh-MY-uh | /ˌdʒɛr.əˈmaɪ.ə/ | 2 Kings 23:31 |  | fine as spelled (1.00) |
| Jehoiakim | juh-HOY-uh-kim | /dʒəˈhɔɪ.ə.kɪm/ | 2 Kings 23:34 |  | still wrong (0.71) |
| Pedaiah | puhdayyuh | /pəˈdeɪ.jə/ | 2 Kings 23:36 | ✅ | overridden (0.83) |
| Nebuchadnezzar | neb-yoo-kuhd-NEZ-er | /ˌnɛb.jʊ.kədˈnɛz.ər/ | 2 Kings 24:1 |  | fine as spelled (0.85) |
| Mattaniah | mat-uh-NY-uh | /ˌmæt.əˈnaɪ.ə/ | 2 Kings 24:17 |  | still wrong (0.57) |
| Zephaniah | zef-uh-NY-uh | /ˌzɛf.əˈnaɪ.ə/ | 2 Kings 25:18 |  | fine as spelled (1.00) |
| Johanan | joh-HAY-nan | /dʒoʊˈheɪ.næn/ | 2 Kings 25:23 |  | suggestion waiting (0.71) |
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
| Jeuel | juh-YOO-el | /dʒəˈjuː.əl/ | 1 Chronicles 9:6 |  |  |
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
| Kue | KOO-ay | /ˈkuː.eɪ/ | 2 Chronicles 1:16 |  |  |
| Lebanon | LEB-uh-nuhn | /ˈlɛb.ə.nən/ | 2 Chronicles 2:8 |  |  |
| Joppa | JOP-uh | /ˈdʒɒp.ə/ | 2 Chronicles 2:16 |  | fine as spelled (0.90) |
| Moriah | muh-RY-uh | /məˈraɪ.ə/ | 2 Chronicles 3:1 |  |  |
| Parvaim | par-VAY-im | /pɑːrˈveɪ.ɪm/ | 2 Chronicles 3:6 |  |  |
| Succoth | SUHK-oth | /ˈsʌk.ɒθ/ | 2 Chronicles 4:17 |  |  |
| Zeredah | ZER-eh-duh | /ˈzɛr.ə.də/ | 2 Chronicles 4:17 |  |  |
| Horeb | HOR-eb | /ˈhɔːr.ɛb/ | 2 Chronicles 5:10 |  |  |
| Tadmor | TAD-mor | /ˈtæd.mɔːr/ | 2 Chronicles 8:4 |  |  |
| Baalath | BAY-uh-lath | /ˈbeɪ.ə.læθ/ | 2 Chronicles 8:6 |  |  |
| Amorites | AM-uh-rites | /ˈæm.ə.raɪts/ | 2 Chronicles 8:7 |  | fine as spelled (1.00) |
| Hittites | HIT-ites | /ˈhɪt.aɪts/ | 2 Chronicles 8:7 |  |  |
| Hivites | HY-vites | /ˈhaɪ.vaɪts/ | 2 Chronicles 8:7 |  | fine as spelled (0.83) |
| Perizzites | PER-ih-zites | /ˈpɛr.ɪ.zaɪts/ | 2 Chronicles 8:7 |  |  |
| Eloth | EE-loth | /ˈiː.lɒθ/ | 2 Chronicles 8:17 |  |  |
| Ezion | EE-zee-on | /ˈiː.zi.ɒn/ | 2 Chronicles 8:17 |  |  |
| Geber | GEE-ber | /ˈɡiː.bər/ | 2 Chronicles 8:17 |  |  |
| Arabia | uh-RAY-bee-uh | /əˈreɪ.bi.ə/ | 2 Chronicles 9:14 |  |  |
| Nebat | NEE-bat | /ˈniː.bæt/ | 2 Chronicles 9:29 |  |  |
| Shilonite | SHY-luh-nite | /ˈʃaɪ.lə.naɪt/ | 2 Chronicles 9:29 |  |  |
| Azekah | uh-ZEE-kuh | /əˈziː.kə/ | 2 Chronicles 11:9 |  |  |
| Lachish | LAY-kish | /ˈleɪ.kɪʃ/ | 2 Chronicles 11:9 |  |  |
| Mahalath | MAY-huh-lath | /ˈmeɪ.hə.læθ/ | 2 Chronicles 11:18 |  |  |
| Shemariah | shem-uh-RY-uh | /ˌʃɛm.əˈraɪ.ə/ | 2 Chronicles 11:19 |  | fine as spelled (0.86) |
| Zaham | ZAY-ham | /ˈzeɪ.hæm/ | 2 Chronicles 11:19 |  |  |
| Shishak | SHY-shak | /ˈʃaɪ.ʃæk/ | 2 Chronicles 12:2 |  |  |
| Lubim | LOO-bim | /ˈluː.bɪm/ | 2 Chronicles 12:3 |  |  |
| Sukkiim | SUHK-ee-im | /ˈsʌk.i.ɪm/ | 2 Chronicles 12:3 |  |  |
| Ammonitess | AM-uh-nite-ess | /ˈæm.ə.naɪ.tɛs/ | 2 Chronicles 12:13 |  |  |
| Naamah | NAY-uh-muh | /ˈneɪ.ə.mə/ | 2 Chronicles 12:13 | ✅ | overridden (1.00) |
| Micaiah | my-KAY-yuh | /maɪˈkeɪ.ə/ | 2 Chronicles 13:2 |  |  |
| Zemaraim | zem-uh-RAY-im | /ˌzɛm.əˈreɪ.ɪm/ | 2 Chronicles 13:4 |  |  |
| Ephron | EE-fron | /ˈiː.frɒn/ | 2 Chronicles 13:19 |  |  |
| Jeshanah | JESH-uh-nuh | /ˈdʒɛʃ.ə.nə/ | 2 Chronicles 13:19 |  |  |
| Asherah | uh-SHEER-uh | /əˈʃɪr.ə/ | 2 Chronicles 14:3 |  |  |
| Zephathah | ZEF-uh-thuh | /ˈzɛf.ə.θə/ | 2 Chronicles 14:10 |  |  |
| Gerar | geerrahr | /ˈɡɪər.ɑːr/ | 2 Chronicles 14:13 | ✅ | overridden (0.80) |
| Oded | OH-ded | /ˈoʊ.dɛd/ | 2 Chronicles 15:1 |  |  |
| Kidron | KID-ruhn | /ˈkɪd.rən/ | 2 Chronicles 15:16 |  |  |
| Baasha | BAY-uh-shuh | /ˈbeɪ.ə.ʃə/ | 2 Chronicles 16:1 |  |  |
| Ramah | RAY-muh | /ˈreɪ.mə/ | 2 Chronicles 16:1 |  |  |
| Abel | AY-buhl | /ˈeɪ.bəl/ | 2 Chronicles 16:4 |  | fine as spelled (1.00) |
| Ijon | EYE-jon | /ˈaɪ.dʒɒn/ | 2 Chronicles 16:4 |  |  |
| Maim | MAY-im | /ˈmeɪ.ɪm/ | 2 Chronicles 16:4 |  |  |
| Mizpah | MIZ-puh | /ˈmɪz.pə/ | 2 Chronicles 16:6 |  |  |
| Rama | RAY-muh | /ˈreɪ.mə/ | 2 Chronicles 16:6 |  |  |
| Baals | BAY-uhlz | /ˈbeɪ.əlz/ | 2 Chronicles 17:3 |  |  |
| Jehonathan | juh-HON-uh-thuhn | /dʒəˈhɒn.ə.θən/ | 2 Chronicles 17:8 |  | fine as spelled (0.89) |
| Jehoram | juh-HOR-uhm | /dʒəˈhɔːr.əm/ | 2 Chronicles 17:8 |  |  |
| Tobadonijah | tob-ad-oh-NY-juh | /ˌtɒb.æd.oʊˈnaɪ.dʒə/ | 2 Chronicles 17:8 |  |  |
| Tobijah | toh-BY-juh | /toʊˈbaɪ.dʒə/ | 2 Chronicles 17:8 |  |  |
| Arabians | uh-RAY-bee-uhnz | /əˈreɪ.bi.ənz/ | 2 Chronicles 17:11 |  | fine as spelled (1.00) |
| Amasiah | am-uh-SY-uh | /ˌæm.əˈsaɪ.ə/ | 2 Chronicles 17:16 |  |  |
| Ahab | AY-hab | /ˈeɪ.hæb/ | 2 Chronicles 18:1 |  |  |
| Imla | IM-luh | /ˈɪm.lə/ | 2 Chronicles 18:7 |  |  |
| Asheroth | ASH-uh-roth | /ˈæʃ.ə.rɒθ/ | 2 Chronicles 19:3 |  |  |
| Ammonites | AM-uh-nites | /ˈæm.ə.naɪts/ | 2 Chronicles 20:1 |  |  |
| Gedi | GED-ee | /ˈɡɛd.i/ | 2 Chronicles 20:2 |  |  |
| Hazazon | HAZ-uh-zon | /ˈhæz.ə.zɒn/ | 2 Chronicles 20:2 |  |  |
| Levite | LEE-vite | /ˈliː.vaɪt/ | 2 Chronicles 20:14 |  | fine as spelled (1.00) |
| Jeruel | juh-ROO-el | /dʒəˈruː.ɛl/ | 2 Chronicles 20:16 |  |  |
| Ziz | ZIZ | /zɪz/ | 2 Chronicles 20:16 |  |  |
| Beracah | BEHR-a-kuh | /ˈbɛr.ə.kə/ | 2 Chronicles 20:26 | ✅ | overridden (0.83) |
| Shilhi | SHIL-hy | /ˈʃɪl.haɪ/ | 2 Chronicles 20:31 |  |  |
| Dodavahu | doh-duh-VAY-hyoo | /ˌdoʊ.dəˈveɪ.huː/ | 2 Chronicles 20:37 |  |  |
| Jehoahaz | juh-HOH-uh-haz | /dʒəˈhoʊ.ə.hæz/ | 2 Chronicles 21:17 |  |  |
| Hazael | HAZ-ay-el | /ˈhæz.eɪ.ɛl/ | 2 Chronicles 22:5 |  |  |
| Nimshi | NIM-shy | /ˈnɪm.ʃaɪ/ | 2 Chronicles 22:7 |  |  |
| Jehoshabeath | jee-hoh-SHAB-ee-ath | /ˌdʒiː.hoʊˈʃæb.i.æθ/ | 2 Chronicles 22:11 |  |  |
| Elishaphat | ih-LISH-uh-fat | /ɪˈlɪʃ.ə.fæt/ | 2 Chronicles 23:1 |  |  |
| Mattan | MAT-an | /ˈmæt.æn/ | 2 Chronicles 23:17 |  |  |
| Zibiah | ZIB-ee-uh | /ˈzɪb.i.ə/ | 2 Chronicles 24:1 |  |  |
| Moabitess | MOH-uh-bite-ess | /ˈmoʊ.ə.baɪ.tɛs/ | 2 Chronicles 24:26 |  |  |
| Shimeath | SHIM-ee-ath | /ˈʃɪm.i.æθ/ | 2 Chronicles 24:26 |  |  |
| Shimrith | SHIM-rith | /ˈʃɪm.rɪθ/ | 2 Chronicles 24:26 |  |  |
| Jehoaddan | jee-hoh-AD-an | /ˌdʒiː.hoʊˈæd.æn/ | 2 Chronicles 25:1 |  |  |
| Jechiliah | jek-ih-LY-uh | /ˌdʒɛk.ɪˈlaɪ.ə/ | 2 Chronicles 26:3 |  |  |
| Ashdod | ASH-dod | /ˈæʃ.dɒd/ | 2 Chronicles 26:6 |  |  |
| Jabneh | JAB-neh | /ˈdʒæb.nə/ | 2 Chronicles 26:6 |  |  |
| Gur | GOOR | /ɡʊər/ | 2 Chronicles 26:7 |  |  |
| Amoz | AY-moz | /ˈeɪ.mɒz/ | 2 Chronicles 26:22 |  |  |
| Isaiah | eye-ZAY-uh | /aɪˈzeɪ.ə/ | 2 Chronicles 26:22 |  | fine as spelled (1.00) |
| Jerushah | juh-ROO-shuh | /dʒəˈruː.ʃə/ | 2 Chronicles 27:1 |  |  |
| Ophel | OH-fel | /ˈoʊ.fɛl/ | 2 Chronicles 27:3 |  |  |
| Hinnom | HIN-uhm | /ˈhɪn.əm/ | 2 Chronicles 28:3 |  |  |
| Pekah | PEE-kuh | /ˈpiː.kə/ | 2 Chronicles 28:6 |  |  |
| Remaliah | rem-uh-LY-uh | /ˌrɛm.əˈlaɪ.ə/ | 2 Chronicles 28:6 |  |  |
| Hadlai | HAD-lye | /ˈhæd.laɪ/ | 2 Chronicles 28:12 |  |  |
| Jehizkiah | jee-hiz-KY-uh | /ˌdʒiː.hɪzˈkaɪ.ə/ | 2 Chronicles 28:12 |  |  |
| Meshillemoth | muh-SHIL-eh-moth | /məˈʃɪl.ə.mɒθ/ | 2 Chronicles 28:12 |  |  |
| Gederoth | guh-DEE-roth | /ɡəˈdiː.rɒθ/ | 2 Chronicles 28:18 |  |  |
| Gimzo | GIM-zoh | /ˈɡɪm.zoʊ/ | 2 Chronicles 28:18 |  |  |
| Timnah | TIM-nuh | /ˈtɪm.nə/ | 2 Chronicles 28:18 |  | fine as spelled (1.00) |
| Eden | EE-duhn | /ˈiː.dən/ | 2 Chronicles 29:12 |  | fine as spelled (1.00) |
| Jehuel | juh-HYOO-el | /dʒəˈhjuː.ɛl/ | 2 Chronicles 29:14 |  |  |
| Conaniah | kon-uh-NY-uh | /ˌkɒn.əˈnaɪ.ə/ | 2 Chronicles 31:12 |  |  |
| Ismachiah | is-muh-KY-uh | /ˌɪs.məˈkaɪ.ə/ | 2 Chronicles 31:13 |  |  |
| Miniamin | mih-NY-uh-min | /mɪˈnaɪ.ə.mɪn/ | 2 Chronicles 31:15 |  |  |
| Sennacherib | suh-NAK-er-ib | /səˈnæk.ər.ɪb/ | 2 Chronicles 32:1 |  |  |
| Gihon | geyehon | /ˈɡaɪ.hɒn/ | 2 Chronicles 32:30 | ✅ | overridden (1.00) |
| Hozai | HOH-zy | /ˈhoʊ.zaɪ/ | 2 Chronicles 33:19 |  |  |
| Azaliah | az-uh-LY-uh | /ˌæz.əˈlaɪ.ə/ | 2 Chronicles 34:8 |  |  |
| Joahaz | JOH-uh-haz | /ˈdʒoʊ.ə.hæz/ | 2 Chronicles 34:8 |  |  |
| Shaphan | SHAY-fan | /ˈʃeɪ.fæn/ | 2 Chronicles 34:8 |  |  |
| Ahikam | uh-HY-kam | /əˈhaɪ.kæm/ | 2 Chronicles 34:20 |  |  |
| Hasrah | HAZ-ruh | /ˈhæz.rə/ | 2 Chronicles 34:22 |  |  |
| Huldah | HUHL-duh | /ˈhʌl.də/ | 2 Chronicles 34:22 |  |  |
| Tokhath | TOK-hath | /ˈtɒk.hæθ/ | 2 Chronicles 34:22 |  |  |
| Carchemish | KAR-keh-mish | /ˈkɑːr.kə.mɪʃ/ | 2 Chronicles 35:20 |  |  |
| Neco | NEE-koh | /ˈniː.koʊ/ | 2 Chronicles 35:20 |  |  |
| Eliakim | ih-LY-uh-kim | /ɪˈlaɪ.ə.kɪm/ | 2 Chronicles 36:4 |  |  |
| Jehoiachin | juh-HOY-uh-kin | /dʒəˈhɔɪ.ə.kɪn/ | 2 Chronicles 36:8 |  |  |
| Chaldeans | kal-DEE-uhnz | /kælˈdiː.ənz/ | 2 Chronicles 36:17 |  |  |
| Persia | PUR-zhuh | /ˈpɜːr.ʒə/ | 2 Chronicles 36:20 |  |  |
| Cyrus | SY-ruhs | /ˈsaɪ.rəs/ | 2 Chronicles 36:22 |  |  |
| Theophilus | thee-OF-ih-luhs | /θiˈɒf.ɪ.ləs/ | Luke 1:3 |  | still wrong (0.75) |
| Elizabeth | ih-LIZ-uh-beth | /ɪˈlɪz.ə.bɛθ/ | Luke 1:5 |  |  |
| Herod | HAIR-uhd | /ˈhɛr.əd/ | Luke 1:5 |  | fine as spelled (0.80) |
| Judea | joo-DEE-uh | /dʒuːˈdiː.ə/ | Luke 1:5 |  | fine as spelled (1.00) |
| Zacharias | zak-uh-RY-uhs | /ˌzæk.əˈraɪ.əs/ | Luke 1:5 |  |  |
| John | JON | /dʒɒn/ | Luke 1:13 |  | fine as spelled (1.00) |
| Gabriel | GAY-bree-el | /ˈɡeɪ.bri.əl/ | Luke 1:19 |  |  |
| Nazareth | NAZ-uh-reth | /ˈnæz.ə.rɛθ/ | Luke 1:26 |  | fine as spelled (0.86) |
| Mary | MAIR-ee | /ˈmɛər.i/ | Luke 1:27 |  | fine as spelled (1.00) |
| Augustus | aw-GUS-tuhs | /ɔːˈɡʌs.təs/ | Luke 2:1 |  | still wrong (0.79) |
| Caesar | SEE-zer | /ˈsiː.zər/ | Luke 2:1 |  | fine as spelled (1.00) |
| Quirinius | kwih-RIN-ee-uhs | /kwɪˈrɪn.i.əs/ | Luke 2:2 |  |  |
| Christ | KRYST | /kraɪst/ | Luke 2:11 |  | fine as spelled (1.00) |
| Jesus | JEE-zuhs | /ˈdʒiː.zəs/ | Luke 2:21 |  | fine as spelled (1.00) |
| Anna | AN-uh | /ˈæn.ə/ | Luke 2:36 |  |  |
| Phanuel | fuh-NYOO-el | /fəˈnjuː.ɛl/ | Luke 2:36 |  |  |
| Abilene | ab-ih-LEE-nee | /ˌæb.ɪˈliː.ni/ | Luke 3:1 |  |  |
| Ituraea | it-yoo-REE-uh | /ˌɪt.jʊˈriː.ə/ | Luke 3:1 |  |  |
| Lysanias | ly-SAY-nee-uhs | /laɪˈseɪ.ni.əs/ | Luke 3:1 |  |  |
| Philip | FIL-ip | /ˈfɪl.ɪp/ | Luke 3:1 |  | fine as spelled (1.00) |
| Pilate | PY-luht | /ˈpaɪ.lət/ | Luke 3:1 |  | fine as spelled (1.00) |
| Pontius | PON-shuhs | /ˈpɒn.ʃəs/ | Luke 3:1 |  | fine as spelled (0.83) |
| Tiberius | ty-BEER-ee-uhs | /taɪˈbɪr.i.əs/ | Luke 3:1 |  |  |
| Trachonitis | trak-oh-NY-tis | /ˌtræk.oʊˈnaɪ.tɪs/ | Luke 3:1 |  |  |
| Annas | AN-uhs | /ˈæn.əs/ | Luke 3:2 |  | still wrong (0.57) |
| Caiaphas | KAY-uh-fuhs | /ˈkeɪ.ə.fəs/ | Luke 3:2 |  | suggestion waiting (0.75) |
| Herodias | huh-ROH-dee-uhs | /həˈroʊ.di.əs/ | Luke 3:19 |  |  |
| Heli | HEE-ly | /ˈhiː.laɪ/ | Luke 3:23 |  |  |
| Jannai | JAN-eye | /ˈdʒæn.aɪ/ | Luke 3:24 |  |  |
| Matthat | MAT-that | /ˈmæt.θæt/ | Luke 3:24 |  |  |
| Melchi | MEL-ky | /ˈmɛl.kaɪ/ | Luke 3:24 |  |  |
| Amos | AY-muhs | /ˈeɪ.məs/ | Luke 3:25 |  |  |
| Esli | ES-ly | /ˈɛs.laɪ/ | Luke 3:25 |  |  |
| Mattathias | mat-uh-THY-uhs | /ˌmæt.əˈθaɪ.əs/ | Luke 3:25 |  |  |
| Naggai | NAG-eye | /ˈnæɡ.aɪ/ | Luke 3:25 |  |  |
| Nahum | NAY-huhm | /ˈneɪ.həm/ | Luke 3:25 |  |  |
| Maath | MAY-ath | /ˈmeɪ.æθ/ | Luke 3:26 |  |  |
| Semein | SEM-ee-in | /ˈsɛm.i.ɪn/ | Luke 3:26 |  |  |
| Joanan | joh-AY-nan | /dʒoʊˈeɪ.næn/ | Luke 3:27 |  |  |
| Neri | NEE-ry | /ˈniː.raɪ/ | Luke 3:27 |  |  |
| Rhesa | REE-suh | /ˈriː.sə/ | Luke 3:27 |  |  |
| Addi | AD-eye | /ˈæd.aɪ/ | Luke 3:28 |  |  |
| Cosam | KOH-sam | /ˈkoʊ.sæm/ | Luke 3:28 |  |  |
| Elmodam | el-MOH-dam | /ɛlˈmoʊ.dæm/ | Luke 3:28 |  |  |
| Jorim | JOR-im | /ˈdʒɔːr.ɪm/ | Luke 3:29 |  |  |
| Jose | JOH-see | /ˈdʒoʊ.siː/ | Luke 3:29 |  |  |
| Jonan | JOH-nan | /ˈdʒoʊ.næn/ | Luke 3:30 |  |  |
| Mattatha | MAT-uh-thuh | /ˈmæt.ə.θə/ | Luke 3:31 |  |  |
| Melea | MEL-ee-uh | /ˈmɛl.i.ə/ | Luke 3:31 |  |  |
| Menan | MEE-nan | /ˈmiː.næn/ | Luke 3:31 |  |  |
| Salmon | SAL-muhn | /ˈsæl.mən/ | Luke 3:32 |  |  |
| Arphaxad | ar-FAK-sad | /ɑːrˈfæk.sæd/ | Luke 3:36 |  | fine as spelled (1.00) |
| Enos | eenas | /ˈiː.nəs/ | Luke 3:38 | ✅ | overridden (1.00) |
| Satan | SAY-tuhn | /ˈseɪ.tən/ | Luke 4:8 |  | fine as spelled (1.00) |
| Capernaum | kuh-PUR-nay-uhm | /kəˈpɜːr.neɪ.əm/ | Luke 4:23 |  |  |
| Zarephath | ZAIR-uh-fath | /ˈzɛr.ə.fæθ/ | Luke 4:26 |  |  |
| Elisha | ih-LY-shuh | /ɪˈlaɪ.ʃə/ | Luke 4:27 |  |  |
| Simon | SY-muhn | /ˈsaɪ.mən/ | Luke 4:38 |  | fine as spelled (1.00) |
| Gennesaret | guh-NES-uh-ret | /ɡəˈnɛs.ə.rɛt/ | Luke 5:1 |  |  |
| Peter | PEE-ter | /ˈpiː.tər/ | Luke 5:8 |  | fine as spelled (0.80) |
| James | JAYMZ | /dʒeɪmz/ | Luke 5:10 |  | fine as spelled (1.00) |
| Zebedee | ZEB-uh-dee | /ˈzɛb.ə.diː/ | Luke 5:10 |  |  |
| Pharisees | FAIR-ih-seez | /ˈfær.ɪ.siːz/ | Luke 5:17 |  | fine as spelled (0.86) |
| Alphaeus | al-FEE-uhs | /ælˈfiː.əs/ | Luke 6:15 |  | fine as spelled (1.00) |
| Iscariot | is-KAIR-ee-uht | /ɪsˈkær.i.ət/ | Luke 6:16 |  |  |
| Judas | JOO-duhs | /ˈdʒuː.dəs/ | Luke 6:16 |  | fine as spelled (0.90) |
| Nain | NAYN | /neɪn/ | Luke 7:11 |  |  |
| Pharisee | FAIR-ih-see | /ˈfær.ɪ.siː/ | Luke 7:36 |  | fine as spelled (0.83) |
| Magdalene | MAG-duh-leen | /ˈmæɡ.də.liːn/ | Luke 8:2 |  |  |
| Chuzas | KOO-zuhs | /ˈkuː.zəs/ | Luke 8:3 |  |  |
| Joanna | joh-AN-uh | /dʒoʊˈæn.ə/ | Luke 8:3 |  |  |
| Gadarenes | GAD-uh-reenz | /ˈɡæd.ə.riːnz/ | Luke 8:26 |  |  |
| Jairus | JY-ruhs | /ˈdʒaɪ.rəs/ | Luke 8:41 |  |  |
| Bethsaida | beth-SAY-ih-duh | /bɛθˈseɪ.ɪ.də/ | Luke 9:10 |  |  |
| Samaritans | suh-MAIR-ih-tuhnz | /səˈmær.ɪ.tənz/ | Luke 9:52 |  | fine as spelled (0.85) |
| Sodom | SOD-uhm | /ˈsɒd.əm/ | Luke 10:12 |  | fine as spelled (1.00) |
| Chorazin | koh-RAY-zin | /koʊˈreɪ.zɪn/ | Luke 10:13 |  |  |
| Hades | HAY-deez | /ˈheɪ.diːz/ | Luke 10:15 |  | fine as spelled (1.00) |
| Samaritan | suh-MAIR-ih-tuhn | /səˈmær.ɪ.tən/ | Luke 10:33 |  |  |
| Martha | MAR-thuh | /ˈmɑːr.θə/ | Luke 10:38 |  |  |
| Beelzebul | bee-EL-zeh-buhl | /biˈɛl.zə.bʌl/ | Luke 11:15 |  |  |
| Jonah | JOH-nuh | /ˈdʒoʊ.nə/ | Luke 11:29 |  |  |
| Ninevites | NIN-uh-vites | /ˈnɪn.ə.vaɪts/ | Luke 11:30 |  |  |
| Nineveh | NIN-uh-vuh | /ˈnɪn.ə.və/ | Luke 11:32 |  | fine as spelled (0.83) |
| Zachariah | zak-uh-RY-uh | /ˌzæk.əˈraɪ.ə/ | Luke 11:51 |  |  |
| Gehenna | guh-HEN-uh | /ɡəˈhɛn.ə/ | Luke 12:5 |  |  |
| Galileans | gal-ih-LEE-uhnz | /ˌɡæl.ɪˈliː.ənz/ | Luke 13:1 |  | fine as spelled (0.89) |
| Siloam | sy-LOH-uhm | /saɪˈloʊ.əm/ | Luke 13:4 |  |  |
| Mammon | MAM-uhn | /ˈmæm.ən/ | Luke 16:13 |  |  |
| Lazarus | LAZ-uh-ruhs | /ˈlæz.ə.rəs/ | Luke 16:20 |  |  |
| Zacchaeus | za-KEE-uhs | /zæˈkiː.əs/ | Luke 19:2 |  |  |
| Bethany | BETH-uh-nee | /ˈbɛθ.ə.ni/ | Luke 19:29 |  |  |
| Bethsphage | BETH-sfuh-jee | /ˈbɛθ.sfə.dʒiː/ | Luke 19:29 |  |  |
| Olivet | ahlihveht | /ˈɒl.ɪ.vɛt/ | Luke 19:29 | ✅ | overridden (0.92) |
| Sadducees | SAD-joo-seez | /ˈsædʒ.ə.siːz/ | Luke 20:27 |  | fine as spelled (1.00) |
| Galilean | gal-ih-LEE-uhn | /ˌɡæl.ɪˈliː.ən/ | Luke 22:59 |  |  |
| Barabbas | buh-RAB-uhs | /bəˈræb.əs/ | Luke 23:18 |  |  |
| Arimathaea | air-ih-muh-THEE-uh | /ˌær.ɪ.məˈθiː.ə/ | Luke 23:51 |  |  |
| Emmaus | eh-MAY-uhs | /ɛˈmeɪ.əs/ | Luke 24:13 |  |  |
| Cleopas | KLEE-oh-puhs | /ˈkliː.ə.pəs/ | Luke 24:18 |  |  |
| Nazarene | naz-uh-REEN | /ˌnæz.əˈriːn/ | Luke 24:19 |  |  |
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
| Phenice | fihneyesee | /fɪˈnaɪ.siː/ | Acts 11:19 | ✅ | overridden (0.86) |
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
| Syracuse | SIHR-a-kyooz | /ˈsɪr.ə.kjuːz/ | Acts 28:12 | ✅ | overridden (0.88) |
| Puteoli | pyoo-TEE-oh-ly | /pjuːˈtiː.ə.laɪ/ | Acts 28:13 |  | still wrong (0.50) |
| Rhegium | REE-jee-uhm | /ˈriː.dʒi.əm/ | Acts 28:13 |  | fine as spelled (1.00) |
| Appii | AP-ee-eye | /ˈæp.i.aɪ/ | Acts 28:15 |  | fine as spelled (1.00) |
| Appius | AP-ee-uhs | /ˈæp.i.əs/ | Acts 28:15 |  | fine as spelled (1.00) |

**Checked:** 171 unchecked, 824 fine as spelled, 436 overridden, 122 suggestion waiting, 277 still wrong.

_1830 names — 436 respelled for the voice, 1394 reference-only._
