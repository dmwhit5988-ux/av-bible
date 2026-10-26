"""Everything else in the Old Testament that ties into the Chronicles tree.

Chronicles is the canon's own genealogical spine — it is the only book that
runs Adam to the exile in one sweep — but it is not the whole story. Genesis
names the wives the lines run through and gives Dan, Zebulun and Gad the only
sons they ever get; Exodus fills in Levi's house and marries Aaron into Judah;
Ruth brings Moab into David's line; Samuel and Kings give Saul's house and
the northern dynasties; Ezra and Nehemiah carry the priesthood past the point
where 1 Chronicles 6 stops.

This module grafts all of that onto `chronicles_tree.build()`. The rule for
inclusion is the one the chart is for: **it has to join up**. A person goes on
only if the text gives a join — a father, a wife, a tribe, or a line that
lands on somebody already here. Isaiah son of Amoz is not on the chart,
because "son of Amoz" joins nothing; Zephaniah is, because his four
generations run back to a Hezekiah in Josiah's day.

Where a graft rests on an inference rather than a statement, the edge is
dashed and the note says what the inference is. Where two books disagree —
and they do, often — both are drawn and the disagreement is written on the
node rather than quietly resolved.

Every entry cites its verse. Spellings are the WEB's throughout.
"""

from chronicles_tree import N, walk


def _note(n, text):
    n.note = f"{n.note} · {text}" if n.note else text
    return n


def W(label, note=None, kids=None, ref=None, icon=None):
    return N(label, note, kids, kind="woman", link="wife", ref=ref, icon=icon)


def H(label, note=None, kids=None, ref=None, icon=None):
    return N(label, note, kids, kind="house", link="dash", ref=ref, icon=icon)


def D(label, note=None, kids=None, ref=None, kind="person", icon=None):
    return N(label, note, kids, kind=kind, link="dash", ref=ref, icon=icon)


def chainof(*specs):
    """(label, note) pairs -> a single-child descent, top first."""
    out = None
    for spec in reversed(specs):
        label, note = spec if isinstance(spec, tuple) else (spec, None)
        n = N(label, note)
        if out is not None:
            n.kids.append(out)
        out = n
    return out


# ===========================================================================
# Genesis
# ===========================================================================

def _genesis(T):
    # -- 4:1-24  the other line out of Adam ------------------------------
    adam = T.root
    eve = W("Eve", "“the mother of all living” — Genesis 3:20; she bore "
            "Cain, Abel and Seth", ref="Gen 3:20")
    cain = N("Cain", "a tiller of the ground, who rose up against his "
             "brother in the field and was made a fugitive and a wanderer "
             "in the earth", ref="Gen 4:1-16", icon="plough")
    abel = N("Abel", "a keeper of sheep, whose offering Yahweh respected — "
             "and whose blood cried from the ground", ref="Gen 4:2-10",
             icon="sheep")
    cain.kids = [chainof(("Enoch", "Cain built a city and called it after "
                          "him"), "Irad", "Mehujael", "Methushael",
                         ("Lamech", "“if Cain will be avenged seven times, "
                          "truly Lamech seventy-seven times”"))]
    lamech = next(m for m in walk(cain) if m.label == "Lamech")
    lamech.kids = [
        W("Adah", "Lamech's first wife", ref="Gen 4:19-21", kids=[
            N("Jabal", "the father of those who dwell in tents and have "
              "livestock", icon="tent"),
            N("Jubal", "the father of all who handle the harp and pipe",
              icon="harp")]),
        W("Zillah", "Lamech's second wife", ref="Gen 4:22", kids=[
            N("Tubal Cain", "the forger of every cutting instrument of "
              "brass and iron", icon="axe"),
            N("Naamah", "Tubal Cain's sister", kind="woman")])]
    adam.kids[0:0] = [eve, cain, abel]
    _note(T.find("Seth"), "“God has given me another child instead of "
          "Abel, for Cain killed him” — Genesis 4:25")

    # -- Genesis 10 against 1 Chronicles 1 --------------------------------
    for label, other in (("Diphath", "Riphath"), ("Rodanim", "Dodanim"),
                         ("Ebal", "Obal"), ("Meshech", "Mash"),
                         ("Sabteca", "Sabteca"), ("Homam", "Hemam"),
                         ("Alian", "Alvan"), ("Shephi", "Shepho"),
                         ("Hamran", "Hemdan"), ("Jaakan", "Akan"),
                         ("Zephi", "Zepho"), ("Amram", "Hemdan")):
        if label == other:
            continue
        try:
            n = T.find(label)
        except KeyError:
            continue
        _note(n, f"Genesis 10 / 36 spells it {other}")

    # -- 11:26-32, 19:36-38, 22:20-24  Terah's other sons -----------------
    terah = T.find("Terah")
    haran = N("Haran", "who died before his father Terah, in Ur of the "
              "Chaldees", ref="Gen 11:28")
    lot = N("Lot", "who went with Abram out of Ur", ref="Gen 11:31")
    # Daughters, not wives: no verse calls it a marriage, so they hang by
    # the plain line, as Haran's daughters do.
    lot.kids = [
        N("his firstborn daughter", "in the cave after Sodom · with child "
          "by her father, Gen 19:36", kind="woman", ref="Gen 19:37",
          kids=[N("Moab", "the father of the Moabites to this day",
                  ref="Gen 19:37")]),
        N("his younger daughter", "with child by her father, Gen 19:36",
          kind="woman", ref="Gen 19:38",
          kids=[N("Ben Ammi", "the father of the children of Ammon to this "
                  "day", ref="Gen 19:38")])]
    haran.kids = [lot,
                  N("Milcah", "who married her uncle Nahor", kind="woman",
                    ref="Gen 11:29"),
                  N("Iscah", None, kind="woman", ref="Gen 11:29")]

    nahor = N("Nahor", "Abram's brother, who married Milcah his niece",
              ref="Gen 11:29")
    bethuel = N("Bethuel", None, ref="Gen 22:22", kids=[
        N("Rebekah", "whom Abraham's servant brought back for Isaac",
          kind="woman", ref="Gen 24:67"),
        N("Laban", "the Aramean, in Paddan Aram", ref="Gen 24:29", kids=[
            N("Leah", "the elder, whom Jacob was given first", kind="woman",
              ref="Gen 29:16-25"),
            N("Rachel", "for whom Jacob served seven years, and seven more; "
              "she died bearing Benjamin on the way to Ephrath",
              kind="woman", ref="Gen 29:18, 35:16-19")])])
    nahor.kids = [
        W("Milcah", "Haran's daughter — these eight she bore to Nahor",
          ref="Gen 22:20-23", kids=[
              N("Uz", "his firstborn"), N("Buz"),
              N("Kemuel", "the father of Aram"), N("Chesed"), N("Hazo"),
              N("Pildash"), N("Jidlaph"), bethuel]),
        W("Reumah", "his concubine", ref="Gen 22:24", kids=[
            N("Tebah"), N("Gaham"), N("Tahash"), N("Maacah")])]
    terah.kids[0:0] = [nahor, haran]

    T.link(T.find("Rebekah"), T.find("Isaac"),
           "Isaac's wife came back out of Nahor's house — Genesis 24")

    # -- Abraham's household ----------------------------------------------
    ab = T.find("Abram · Abraham")
    ab.kids[0:0] = [
        W("Sarai · Sarah", "barren until Isaac; she died at Hebron and was "
          "buried in the cave of Machpelah", ref="Gen 11:30, 21:2, 23:19"),
        W("Hagar", "Sarai's Egyptian servant, Ishmael's mother",
          ref="Gen 16:1-15")]
    _note(T.find("Isaac"), "Sarah bore him when Abraham was a hundred")
    _note(T.find("Ishmael"), "Hagar the Egyptian bore him")

    # -- 36:1-14  Esau's wives, and the second marriage into Seir ---------
    esau = T.find("Esau")
    esau.kids[0:0] = [
        W("Adah", "the daughter of Elon the Hittite — she bore Eliphaz",
          ref="Gen 36:2, 4"),
        W("Basemath", "Ishmael's daughter, sister of Nebaioth — she bore "
          "Reuel", ref="Gen 36:3, 4"),
        W("Oholibamah", "the daughter of Anah, the daughter of Zibeon the "
          "Hivite — she bore Jeush, Jalam and Korah", ref="Gen 36:2, 5")]
    T.link(T.find("Basemath"), T.find("Nebaioth"),
           "Esau married his uncle Ishmael's daughter — Genesis 36:3")
    T.link(T.find("Oholibamah", 1), T.find("Anah", 1),
           "and married into Seir a second time — Genesis 36:2")
    _note(T.find("Timna", 1),
          "Genesis 36:12 makes her Eliphaz's concubine and Amalek's "
          "mother; 1 Chr 1:36 lists her among Eliphaz's sons")

    # -- 29-35  Israel's four wives, and Dinah ----------------------------
    isr = T.find("Israel")
    mothers = {
        "Reuben": "Leah", "Simeon": "Leah", "Levi": "Leah", "Judah": "Leah",
        "Issachar": "Leah", "Zebulun": "Leah",
        "Joseph": "Rachel", "Benjamin": "Rachel",
        "Dan": "Bilhah", "Naphtali": "Bilhah",
        "Gad": "Zilpah", "Asher": "Zilpah"}
    for son, mum in mothers.items():
        try:
            _note(T.find(son, under=isr), f"of {mum} — Genesis 35:23-26")
        except KeyError:
            pass
    isr.kids[0:0] = [
        W("Leah", "Laban's elder daughter — six sons and Dinah",
          ref="Gen 29:31-35, 30:17-21", kids=[
              N("Dinah", "his daughter", kind="woman", ref="Gen 30:21")]),
        W("Rachel", "Laban's younger daughter — Joseph and Benjamin; she "
          "died on the way to Ephrath, which is Bethlehem",
          ref="Gen 35:16-19"),
        W("Bilhah", "Rachel's servant — Dan and Naphtali", ref="Gen 30:1-8"),
        W("Zilpah", "Leah's servant — Gad and Asher", ref="Gen 30:9-13")]
    T.link(T.find("Leah", 2), T.find("Leah", 1),
           "Jacob's wives were Laban's daughters, of Nahor's house")

    # -- 46:8-27  the seventy who went down into Egypt --------------------
    #
    # This is where Dan, Zebulun and Gad get the only sons the canon ever
    # gives them, and where several tribes get a second, different list.
    T.children("Zebulun", N("Zebulun", kids=[
        N("Sered"), N("Elon"), N("Jahleel")]), under=isr, ref="Gen 46:14")
    _note(T.find("Zebulun", under=isr),
          "Chronicles never traces him; these three are all the sons he is "
          "given anywhere")
    T.children("Dan", N("Dan", kids=[
        N("Hushim", "Numbers 26:42 calls him Shuham")]), under=isr,
        ref="Gen 46:23")
    _note(T.find("Dan", under=isr),
          "Chronicles never traces him either — one son, and the tribe "
          "counted 64,400 (Numbers 26:43)")

    T.child("Simeon", D("Ohad", "Genesis 46:10 has him among Simeon's sons; "
                        "the Chronicles list drops him", ref="Gen 46:10"))
    for lbl, alt in (("Nemuel", "Jemuel"), ("Jarib", "Jachin"),
                     ("Zerah", "Zohar")):
        try:
            _note(T.find(lbl, under=T.find("Simeon")),
                  f"Genesis 46:10 has {alt}")
        except KeyError:
            pass
    for lbl, alt, tribe in (("Puah", "Puvah", "Issachar"),
                            ("Jashub", "Iob", "Issachar"),
                            ("Jahziel", "Jahzeel", "Naphtali"),
                            ("Shallum", "Shillem", "Naphtali")):
        try:
            _note(T.find(lbl, under=T.find(tribe, under=isr)),
                  f"Genesis 46 has {alt}")
        except KeyError:
            pass

    # Gad's own sons, ahead of everything else under him. The men of
    # 1 Chr 5:11-17 are a later register of Gadites in Bashan, already hung
    # in their own house (chronicles_tree._reuben_gad_manasseh).
    gad = T.find("Gad", under=isr)
    gad.kids[0:0] = [
        N("Ziphion", "Numbers 26:15 calls him Zephon"), N("Haggi"),
        N("Shuni"), N("Ezbon", "Numbers 26:16 calls him Ozni"), N("Eri"),
        N("Arodi", "Numbers 26:17 calls him Arod"), N("Areli")]
    gad.ref = gad.ref or "Gen 46:16"
    _note(gad, "Chronicles never names his sons; these seven are Genesis "
          "46:16 and Numbers 26:15-17")
    T.child("Benjamin", H("the sons of Benjamin (Genesis 46:21)",
                          "ten — a third list, against 7:6 and 8:1",
                          ref="Gen 46:21",
                          kids=[N(x, link="dash") for x in
                                ("Bela", "Becher", "Ashbel", "Gera",
                                 "Naaman", "Ehi", "Rosh", "Muppim",
                                 "Huppim", "Ard")]), under=isr, link="dash")
    T.child("Joseph", W("Asenath", "the daughter of Potiphera, priest of "
                        "On, who bore Manasseh and Ephraim in Egypt",
                        ref="Gen 46:20"), link="wife")


# ===========================================================================
# Exodus
# ===========================================================================

def _exodus(T):
    amram = T.find("Amram", 1)
    amram.kids.insert(0, W("Jochebed", "Amram's father's sister, whom he "
                           "took to wife — she bore Aaron and Moses",
                           ref="Ex 6:20"))
    _note(amram, "he lived a hundred and thirty-seven years")

    kohath = T.find("Kohath", 1)
    T.children("Izhar", N("Izhar", kids=[
        N("Korah", "who rose against Moses, and the earth swallowed him — "
          "Numbers 16"),
        N("Nepheg"), N("Zichri")]), under=kohath, ref="Ex 6:21")
    T.children("Uzziel", N("Uzziel", kids=[
        N("Mishael"), N("Elzaphan"), N("Sithri")]), under=kohath,
        ref="Ex 6:22")
    T.link(T.find("Korah", 3), T.find("Korah", 2),
           "Izhar's son Korah and the Korah of 6:22 — the same rebel house")

    aaron = T.find("Aaron")
    aaron.kids.insert(0, W("Elisheba", "the daughter of Amminadab, the "
                           "sister of Nahshon — she bore Nadab, Abihu, "
                           "Eleazar and Ithamar", ref="Ex 6:23"))
    T.link(T.find("Elisheba"), T.find("Nahshon"),
           "Aaron married into the royal tribe — Exodus 6:23")

    T.child("Eleazar", W("a daughter of Putiel", "she bore Phinehas",
                         ref="Ex 6:25"), nth=1, under=aaron, link="wife")

    moses = T.find("Moses")
    moses.kids.append(W("Zipporah", "the daughter of Reuel the priest of "
                        "Midian, who is Jethro", ref="Ex 2:21, 18:2", kids=[
                            N("Gershom", "“I have lived as a foreigner in a "
                              "foreign land”", ref="Ex 2:22"),
                            N("Eliezer", "“my father's God was my help and "
                              "delivered me from Pharaoh's sword”",
                              ref="Ex 18:4")]))
    jethro = D("Reuel · Jethro", "the priest of Midian, Moses' "
               "father-in-law, who had seven daughters",
               ref="Ex 2:16-18, 18:1")
    T.child("Midian", jethro, link="dash")
    T.link(jethro, T.find("Zipporah"),
           "Moses married into Keturah's line — Exodus 2:21")


# ===========================================================================
# Numbers, Joshua, Judges
# ===========================================================================

PRINCES = [                                        # Numbers 1:5-15
    ("Reuben", "Elizur", "Shedeur"), ("Simeon", "Shelumiel", "Zurishaddai"),
    ("Issachar", "Nethanel", "Zuar"), ("Zebulun", "Eliab", "Helon"),
    ("Manasseh", "Gamaliel", "Pedahzur"), ("Benjamin", "Abidan", "Gideoni"),
    ("Dan", "Ahiezer", "Ammishaddai"), ("Asher", "Pagiel", "Ochran"),
    ("Gad", "Eliasaph", "Deuel"), ("Naphtali", "Ahira", "Enan"),
]

SPIES = [                                          # Numbers 13:4-15
    ("Reuben", "Shammua", "Zaccur"), ("Simeon", "Shaphat", "Hori"),
    ("Issachar", "Igal", "Joseph"), ("Benjamin", "Palti", "Raphu"),
    ("Zebulun", "Gaddiel", "Sodi"), ("Manasseh", "Gaddi", "Susi"),
    ("Dan", "Ammiel", "Gemalli"), ("Asher", "Sethur", "Michael"),
    ("Naphtali", "Nahbi", "Vophsi"), ("Gad", "Geuel", "Machi"),
]


def _numbers(T, jos):
    for tr, prince, father in PRINCES:
        T.child(tr, D(father, f"the prince of {tr} in the wilderness was "
                      f"his son", ref="Num 1:5-15",
                      kids=[N(prince, "prince of the tribe, who stood with "
                              "Moses at the census")]),
                under=None if tr not in ("Manasseh",) else jos, link="dash")
    for tr, spy, father in SPIES:
        T.child(tr, D(father, "his son was sent to spy out the land",
                      ref="Num 13:4-15",
                      kids=[N(spy, "one of the twelve spies")]),
                under=None if tr not in ("Manasseh",) else jos, link="dash")
    _note(T.find("Ammihud", under=T.find("Ephraim", under=jos)),
          "Numbers 1:10 makes his son Elishama prince of Ephraim — the "
          "same Elishama, Joshua's grandfather")

    # -- Machir's house: Numbers 26:29-33 against 1 Chronicles 7 ---------
    machir = T.find("Machir")
    gilead = D("Gilead", "1 Chr 7:14 calls Machir his father; Numbers "
               "26:29-33 hangs Manasseh's whole clan list on him",
               ref="Num 26:29")
    gilead.kids = [N(x, link="dash") for x in
                   ("Iezer", "Helek", "Asriel", "Shechem", "Shemida")]
    gilead.kids.append(N("Hepher", "Numbers 26:33 makes Zelophehad his son; "
                         "1 Chr 7:15 makes Zelophehad Machir's",
                         link="dash", ref="Num 26:33"))
    machir.kids.append(gilead)
    zel = T.find("Zelophehad")
    zel.kids = [N(d, "one of the five who came before Moses and got their "
                  "father's inheritance", kind="woman", ref="Num 27:1")
                for d in ("Mahlah", "Noah", "Hoglah", "Milcah", "Tirzah")]
    _note(zel, "who had no sons")

    # -- Judges ----------------------------------------------------------
    T.child("Abiezer", D("Joash", "the Abiezrite, of Ophrah",
                         ref="Judg 6:11", kids=[
                             N("Gideon", "who threw down the altar of Baal "
                               "and had seventy sons; his concubine in "
                               "Shechem bore him one more",
                               ref="Judg 6-8", icon="trumpet", kids=[
                                   N("Abimelech", "who killed his seventy "
                                     "brothers on one stone and reigned "
                                     "three years", ref="Judg 9",
                                     kind="king")])]), link="dash")
    T.child("Gilead", D("Jephthah", "the Gileadite, a mighty man of valor, "
                        "the son of a prostitute, whom his brothers drove "
                        "out — and who judged Israel six years",
                        ref="Judg 11:1-2", icon="sword"), link="dash")
    T.link(T.find("Jair", 1), T.find("Jephthah"),
           "Jair the Gileadite, who judged Israel — Judges 10:3")
    T.child("Dan", D("Manoah", "of Zorah, of the family of the Danites",
                     ref="Judg 13:2", kids=[
                         N("Samson", "who judged Israel twenty years",
                           icon="lion", ref="Judg 13:24")]),
            under=T.find("Israel"), link="dash")


# ===========================================================================
# Ruth
# ===========================================================================

def _ruth(T):
    elim = D("Elimelech", "an Ephrathite of Bethlehem Judah, who went to "
             "live in the country of Moab in the days when the judges "
             "judged", ref="Ruth 1:1-2")
    naomi = W("Naomi", "his wife, who came back empty and was called Mara",
              ref="Ruth 1:2, 20")
    mahlon = N("Mahlon", "who took Ruth the Moabitess, and died",
               ref="Ruth 1:4-5, 4:10")
    chilion = N("Chilion", "who took Orpah the Moabitess, and died",
                ref="Ruth 1:4-5")
    mahlon.kids = [W("Ruth", "the Moabitess, who would not leave her "
                     "mother-in-law", ref="Ruth 1:16")]
    chilion.kids = [W("Orpah", "who kissed her mother-in-law and went back",
                      ref="Ruth 1:14")]
    naomi.kids = [mahlon, chilion]
    elim.kids = [naomi]
    T.child("Judah", elim, link="dash")

    boaz = T.find("Boaz")
    _note(boaz, "who bought all that was Elimelech's, and took Ruth to "
                "raise up the name of the dead on his inheritance — "
                "Ruth 4:9-10")
    ruth2 = W("Ruth", "the Moabitess — “a son is born to Naomi”; the women "
              "named him Obed", ref="Ruth 4:13-17")
    boaz.kids.insert(0, ruth2)
    T.link(mahlon.kids[0], ruth2, "Mahlon's widow became Boaz's wife")
    T.link(ruth2, T.find("Moab"),
           "Moab in David's line, four generations back — Ruth 4:17-22")
    _note(T.find("Obed", under=boaz),
          "Ruth 4:17 — “he is the father of Jesse, the father of David”")


# ===========================================================================
# Samuel
# ===========================================================================

def _samuel(T):
    # -- Eli's house, of Ithamar (1 Chr 24:3) -----------------------------
    eli = D("Eli", "the priest at Shiloh, who judged Israel forty years and "
            "fell backward from his seat when the ark was taken; of the "
            "sons of Ithamar — 1 Chr 24:3", ref="1 Sam 1-4", kind="priest",
            icon="priest")
    phin = N("Phinehas", "who died in the same day as his brother, when the "
             "ark of God was taken", ref="1 Sam 4:11", kids=[
                 N("Ichabod", "“the glory has departed from Israel” — his "
                   "mother named him and died", ref="1 Sam 4:21"),
                 N("Ahitub", "Ichabod's brother", ref="1 Sam 14:3", kids=[
                     N("Ahijah", "who wore the ephod in Saul's day",
                       ref="1 Sam 14:3", kind="priest"),
                     N("Ahimelech", "who gave David the show bread, and "
                       "whom Saul had killed with eighty-five priests",
                       ref="1 Sam 21-22", kind="priest", kids=[
                           N("Abiathar", "who escaped and fled after David; "
                             "Solomon put him out of the priesthood to "
                             "Anathoth", ref="1 Sam 22:20, 1 Kgs 2:26-27",
                             kind="priest")])])])
    eli.kids = [N("Hophni", "a son of Belial, who didn't know Yahweh",
                  ref="1 Sam 2:12"), phin]
    T.child("Ithamar", eli, link="dash")

    # -- Samuel's mother --------------------------------------------------
    sam = T.find("Samuel")
    elk = sam.parent
    if elk is not None:
        elk.kids.insert(0, W("Hannah", "who was in bitterness of soul and "
                             "vowed her son to Yahweh all the days of his "
                             "life", ref="1 Sam 1:11"))
        elk.kids.insert(1, W("Peninnah", "his other wife, who had children "
                             "and provoked her", ref="1 Sam 1:2"))
        _note(elk, "of Ramathaim Zophim in the hill country of Ephraim — "
                   "1 Sam 1:1 traces him back through Jeroham, Elihu, Tohu "
                   "and Zuph, the same line as 6:26-27")

    # -- Saul's house -----------------------------------------------------
    saul = T.find("Saul")
    kish = saul.parent
    if kish is not None:
        _note(kish, "1 Sam 9:1 traces him through Abiel, Zeror, Becorath "
                    "and Aphiah, and 14:51 makes him Ner's brother, not "
                    "his son")
    saul.kids[0:0] = [
        W("Ahinoam", "the daughter of Ahimaaz", ref="1 Sam 14:50"),
        W("Rizpah", "the daughter of Aiah, his concubine", ref="2 Sam 21:8",
          kids=[N("Armoni", "whom the Gibeonites hanged"),
                N("Mephibosheth", "whom the Gibeonites hanged")])]
    saul.kids.append(N("Merab", "the firstborn daughter, given to Adriel "
                       "the son of Barzillai the Meholathite",
                       kind="woman", ref="1 Sam 14:49, 2 Sam 21:8"))
    saul.kids.append(N("Michal", "the younger daughter, who was David's "
                       "wife and had no child to the day of her death",
                       kind="woman", ref="1 Sam 14:49, 2 Sam 6:23"))
    ner = T.find("Ner", 1)
    ner.kids.append(N("Abner", "the captain of Saul's army — 14:50 makes "
                      "him Saul's cousin, and Joab killed him at Hebron",
                      ref="1 Sam 14:50, 2 Sam 3:27", icon="sword"))

    # -- David's wives, and Ahithophel ------------------------------------
    dav = T.find("David")
    dav.kids[0:0] = [
        W("Ahinoam", "the Jezreelitess — Amnon's mother", ref="2 Sam 3:2"),
        W("Abigail", "the Carmelite, Nabal's widow — Daniel's mother, whom "
          "2 Sam 3:3 calls Chileab", ref="1 Sam 25:39-42"),
        W("Maacah", "the daughter of Talmai king of Geshur — Absalom's and "
          "Tamar's mother", ref="2 Sam 3:3"),
        W("Haggith", "Adonijah's mother", ref="2 Sam 3:4"),
        W("Abital", "Shephatiah's mother", ref="2 Sam 3:4"),
        W("Eglah", "Ithream's mother", ref="2 Sam 3:5"),
        W("Michal", "Saul's daughter, whom he took back and who despised "
          "him when he danced before the ark", ref="2 Sam 3:13-14, 6:16")]
    T.link(T.find("Michal", 2), T.find("Michal", 1),
           "David married Saul's daughter — 1 Samuel 18:27")

    ahi = D("Ahithophel", "the Gilonite, David's counselor, whose counsel "
            "was as if a man inquired at the word of God — and who hanged "
            "himself when it was not followed", ref="2 Sam 15-17", kids=[
                N("Eliam", "one of David's thirty mighty men",
                  ref="2 Sam 23:34", kids=[
                      N("Bathsheba · Bathshua", "Uriah the Hittite's wife, "
                        "who bore Solomon", kind="woman",
                        ref="2 Sam 11:3, 1 Chr 3:5")])])
    T.child("Judah", ahi, link="dash")
    T.link(T.find("Bathsheba · Bathshua"), T.find("Solomon"),
           "Solomon's mother was David's counsellor's granddaughter")

    abs_ = T.find("Absalom")
    _note(abs_, "who stole the hearts of the men of Israel and was caught "
                "in the oak by his head — 2 Samuel 15-18")
    abs_.kids.append(H("three sons", "2 Samuel 14:27 counts them and does "
                       "not name them; 18:18 says he had no son to keep his "
                       "name in remembrance", ref="2 Sam 14:27"))
    abs_.kids.append(N("Tamar", "his daughter, a woman with a beautiful "
                       "face", kind="woman", ref="2 Sam 14:27"))
    _note(T.find("Daniel", 1), "2 Samuel 3:3 calls him Chileab")


def _has(T, label):
    try:
        T.find(label)
        return True
    except KeyError:
        return False


# ===========================================================================
# Kings — the northern house
# ===========================================================================

def _kings(T, jos):
    isr = T.find("Israel")

    # Jeroboam and Baasha are given tribes, so they hang on those tribes.
    T.child("Ephraim", D("Nebat", "of Zeredah; his widow was Zeruah",
                         ref="1 Kgs 11:26", kids=[
                             N("Jeroboam", "Solomon's servant, who lifted "
                               "up his hand against the king and made "
                               "Israel to sin — 22 years", kind="king",
                               ref="1 Kgs 11-14", kids=[
                                   N("Nadab", "2 years, whom Baasha struck "
                                     "at Gibbethon", kind="king",
                                     ref="1 Kgs 15:25-28"),
                                   N("Abijah", "who died as the prophet "
                                     "said", ref="1 Kgs 14:1-18")])]),
            under=jos, link="dash")
    T.child("Issachar", D("Ahijah", "of the house of Issachar",
                          ref="1 Kgs 15:27", kids=[
                              N("Baasha", "who destroyed all the house of "
                                "Jeroboam and reigned 24 years in Tirzah",
                                kind="king", ref="1 Kgs 15:27-16:6", kids=[
                                    N("Elah", "2 years, whom Zimri his "
                                      "servant killed as he drank himself "
                                      "drunk", kind="king",
                                      ref="1 Kgs 16:8-10")])]),
            under=isr, link="dash")

    omri = N("Omri", "the captain of the host, who bought the hill of "
             "Samaria and built on it — 12 years", kind="king",
             ref="1 Kgs 16:16-28")
    ahab = N("Ahab", "22 years — who did evil above all that were before "
             "him", kind="king", ref="1 Kgs 16:29-22:40")
    ahab.kids = [
        W("Jezebel", "the daughter of Ethbaal king of the Sidonians, whom "
          "the dogs ate by the wall of Jezreel", ref="1 Kgs 16:31"),
        N("Ahaziah", "2 years — he fell through the lattice", kind="king",
          ref="1 Kgs 22:51"),
        N("Joram", "12 years, whom Jehu shot through the heart",
          kind="king", ref="2 Kgs 3:1, 9:24"),
        N("Athaliah", "the daughter of Omri's house, who married Jehoram "
          "of Judah; when her son Ahaziah was dead she destroyed all the "
          "royal offspring of Judah and reigned six years",
          kind="woman", ref="2 Kgs 8:18, 26, 2 Chr 22:10-12")]
    omri.kids = [ahab]

    jehu = N("Jehu", "the son of Jehoshaphat the son of Nimshi, whom "
             "Elisha's servant anointed — 28 years", kind="king",
             ref="2 Kgs 9:2, 10:36", icon="chariot")
    jehu.kids = [N("Jehoahaz", "17 years", kind="king", ref="2 Kgs 13:1",
                   kids=[N("Joash", "16 years", kind="king",
                           ref="2 Kgs 13:10", kids=[
                               N("Jeroboam", "the second — 41 years",
                                 kind="king", ref="2 Kgs 14:23", kids=[
                                     N("Zechariah", "6 months — the fourth "
                                       "generation, as Yahweh said to Jehu",
                                       kind="king",
                                       ref="2 Kgs 15:8-12")])])])]

    north = H("the kings of Israel", "the ten tribes after the kingdom was "
              "rent; nine houses in two hundred years, and none of them "
              "kept it", ref="1 Kgs 12 - 2 Kgs 17")
    north.kids = [
        N("Zimri", "seven days — he burned the king's house over himself",
          kind="king", link="dash", ref="1 Kgs 16:15-18"),
        omri, jehu,
        D("Jabesh", None, ref="2 Kgs 15:10", kids=[
            N("Shallum", "one month, whom Menahem struck in Samaria",
              kind="king")]),
        D("Gadi", None, ref="2 Kgs 15:14", kids=[
            N("Menahem", "10 years, who gave Pul of Assyria a thousand "
              "talents of silver", kind="king", kids=[
                  N("Pekahiah", "2 years, whom his captain killed",
                    kind="king", ref="2 Kgs 15:23")])]),
        D("Remaliah", None, ref="2 Kgs 15:27", kids=[
            N("Pekah", "20 years — in his days Tiglath Pileser carried "
              "Naphtali away", kind="king")]),
        D("Elah", None, ref="2 Kgs 17:1", kids=[
            N("Hoshea", "9 years — the last king of Israel, in whose ninth "
              "year Samaria was taken", kind="king", icon="shackle")]),
    ]
    for k in north.kids:
        k.link = "dash" if k.link != "dash" else k.link
    T.child("Israel", north, link="dash")

    # Athaliah is the hinge between the two houses; she is drawn once, as
    # Ahab's daughter, and tied to Judah by a link rather than a second box.
    jor = T.find("Joram", 1)
    jor.kids = [k for k in jor.kids if k.label != "Athaliah"]
    _note(jor, "he walked in the way of the kings of Israel, for he married "
               "Ahab's daughter — 2 Kings 8:18")
    T.link(T.find("Athaliah", 2), jor,
           "the house of Omri married into the house of David — and very "
           "nearly ended it")


# ===========================================================================
# Ezra, Nehemiah, Esther, Daniel, the prophets
# ===========================================================================

def _after(T):
    # -- Ezra 7:1-5: the priest's own line, and it lands on Seraiah -------
    ser = T.find("Seraiah", 1)
    ser.kids.append(N("Ezra", "the scribe, skilled in the law of Moses — "
                      "Ezra 7:1-5 runs his fathers back through Azariah, "
                      "Hilkiah, Shallum, Zadok, Ahitub, Amariah, Azariah, "
                      "Meraioth, Zerahiah, Uzzi, Bukki, Abishua, Phinehas "
                      "and Eleazar to Aaron the chief priest",
                      kind="priest", ref="Ezra 7:1-5", icon="scroll"))

    # -- Nehemiah 12:10-11: the priesthood carried past the exile --------
    jehoz = T.find("Jehozadak")
    jeshua = N("Jeshua", "who with Zerubbabel built the altar and laid the "
               "foundation of the house — Ezra 3:2, 8", kind="priest",
               ref="Neh 12:10")
    jeshua.kids = [chainof(("Joiakim", None), ("Eliashib", "who built the "
                           "sheep gate with his brothers the priests — "
                           "Neh 3:1"), ("Joiada", None),
                          ("Jonathan", None),
                          ("Jaddua", "the last high priest the Old "
                           "Testament names"))]
    for m in walk(jeshua):
        m.kind = "priest"
    jehoz.kids.append(jeshua)

    # -- Zerubbabel: Chronicles and the prophets disagree on his father --
    zer = T.find("Zerubbabel")
    _note(zer, "Ezra 3:2, Haggai 1:1 and Matthew 1:12 all call him the son "
               "of Shealtiel; 1 Chr 3:19 makes him Pedaiah's")
    T.link(zer, T.find("Shealtiel"),
           "the son of Shealtiel, everywhere but here")

    # -- Esther 2:5-7 ----------------------------------------------------
    mord = D("Kish", "Esther 2:5 names Mordecai's great-grandfather with "
             "Saul's father's name, and calls him a Benjamite",
             ref="Est 2:5")
    mord.kids = [chainof("Shimei", "Jair",
                         ("Mordecai", "carried away from Jerusalem with "
                          "Jeconiah; he sat in the king's gate in Susa"))]
    m = next(x for x in walk(mord) if x.label == "Mordecai")
    m.icon = "scroll"
    m.ref = "Est 2:5-6"
    m.kids = [N("Hadassah · Esther", "his uncle's daughter, whom he took "
                "for his own daughter when her father and mother were "
                "dead — queen in Ahasuerus' place",
                kind="woman", ref="Est 2:7", link="dash")]
    T.child("Benjamin", mord, under=T.find("Israel"), link="dash")

    # -- Daniel 1:3-6 ----------------------------------------------------
    # "Of the royal offspring and of the nobles … of the children of
    # Judah": no father, no king and no generation is given, and they were
    # taken in Jehoiakim's third year, before Jeconiah reigned. The one join
    # the text states is the tribe.
    T.child("Judah", H("of the royal offspring and of the nobles",
                       "of the children of Judah — Daniel 1:3-6; taken in "
                       "Jehoiakim's third year; the text gives no father or "
                       "generation · the prince of the eunuchs renamed "
                       "them, 1:7",
                       ref="Dan 1:3-7", kids=[
                           N("Daniel", "Belteshazzar", link="dash",
                             icon="lion"),
                           N("Hananiah", "Shadrach", link="dash"),
                           N("Mishael", "Meshach", link="dash"),
                           N("Azariah", "Abednego", link="dash")]),
            under=T.find("Israel"), link="dash")

    # -- the prophets whose fathers join them to somebody -----------------
    T.child("Hezekiah", D("Amariah", "Zephaniah 1:1 runs the prophet's "
                          "fathers back four generations to a Hezekiah, in "
                          "Josiah's days", ref="Zeph 1:1", kids=[
                              N("Gedaliah"),
                              N("Cushi", None, kids=[
                                  N("Zephaniah", "the prophet, in the days "
                                    "of Josiah", icon="scroll")])]),
            link="dash")
    T.child("Abiathar", D("Hilkiah", "one of the priests who were in "
                          "Anathoth, where Solomon sent Abiathar",
                          ref="Jer 1:1, 1 Kgs 2:26", kids=[
                              N("Jeremiah", "the prophet, to whom Yahweh's "
                                "word came in the thirteenth year of "
                                "Josiah", icon="scroll", kind="priest")]),
            link="dash")
    T.child("Aaron", D("Buzi", None, ref="Ezek 1:3", kids=[
        N("Ezekiel", "the priest, by the river Chebar in the land of the "
          "Chaldeans", kind="priest", icon="scroll")]), link="dash")
    T.child("Levi", D("Iddo", "a priest who came up with Zerubbabel — "
                      "Nehemiah 12:4", ref="Zech 1:1", kids=[
                          N("Berechiah", None, kids=[
                              N("Zechariah", "the prophet, in the second "
                                "year of Darius", icon="scroll")])]),
            link="dash")

    # -- Jeremiah 35: the Rechabites -------------------------------------
    T.child("the scribes who lived at Jabez",
            D("Rechab", None, ref="Jer 35:6", kids=[
                N("Jonadab", "who commanded his sons to drink no wine, "
                  "build no house and dwell in tents — and they obeyed him",
                  icon="tent")]), link="dash")


def extend(T):
    jos = T.find("Joseph")          # captured before Numbers 13:7 adds another
    _genesis(T)
    _exodus(T)
    _numbers(T, jos)
    _ruth(T)
    _samuel(T)
    _kings(T, jos)
    _after(T)
    return T
