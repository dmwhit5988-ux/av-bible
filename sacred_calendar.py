"""The sacred year: WEB's months, the set feasts, the farming year, the days
the text dates to a month, the feasts in John and Acts, and the Sabbath year
and the Jubilee.

Data only, so that the Sacred year reference page
(generate_sacred_year_reference.py) and later per-verse pictures of
Leviticus 23, Numbers 28-29, Esther or Haggai draw from one table. Every ref
is a string verse_refs.parse() reads (the tests check each against WEB), and
every card's words are WEB's own: a `Card`'s fragments are each found, word
for word, in the verses it cites.

- **MONTHS**, 1 to 12 from Abib. Month 1 is the month of the going out
  (Exodus 12:2; 13:4). WEB numbers most dates ("the seventh month") and names
  a month only eleven times over: Abib and Nisan (1), Ziv (2), Sivan (3),
  Elul, Ethanim (7), Bul (8), Chislev (9), Tebeth (10), Shebat (11) and Adar
  (12). Each name lists the verses that use it and the verses that give its
  number. Elul is never numbered in WEB; it is the sixth month by the later
  calendar, and Nehemiah 6:15 and 7:73 fit that. Months 4 and 5 have no name
  in WEB. `modern` is the usual equivalent ("about March-April"), not the
  text's.
- **The months are lunar.** The text keeps them by the new moon (Numbers
  10:10; 28:11) and never says how long a month is or how the year kept pace
  with the harvest. `day_of_year` places a day on a schematic year of twelve
  30-day months, which is how the page's dial draws it; the dial's "about the
  dial" card says so.
- **FEASTS**: the Sabbath, the new moon and the set feasts of Leviticus 23
  and Numbers 28-29 (Passover, unleavened bread, the sheaf, weeks, blowing of
  trumpets, the Day of Atonement, tents and the eighth day), with the second
  Passover (Numbers 9), Purim (Esther 9) and the Dedication (John 10) as
  later additions (`later`). Each has its month and day, length, whether it
  is one of the three pilgrim feasts (Deuteronomy 16:16), its rest, the
  Numbers 28-29 offerings a day (`offerings_by_day` where they change: tents'
  bulls run 13 down to 7, then 1 on the eighth day), and Leviticus 23's own
  list where it differs (`offerings_lev23`: the sheaf, weeks). WEB's names
  are kept as WEB has them: "feast of tents" (the "Feast of Booths" only in
  John 7:2), "day of blowing of trumpets", "day of atonement" in Leviticus 23
  and "Day of Atonement" in 25:9. The feast of weeks has no date: it is
  counted fifty days from the sheaf (`counted`), which the text also leaves
  without a fixed day.
- **FARMING**: the farming year, each entry `stated` where the text ties it
  to a month or a feast (the Jordan in flood in the first month, the
  ingathering before the feast of tents, the great rain of the ninth month),
  `derived` where its month follows only by joining verses (barley begins the
  harvest, and the harvest is under way in the first month) or `season` where
  it names the season only (the former and latter rain, plowing). `drawn` is
  where a drawing places it, each stretch marked "stated", "derived" or
  "convention".
- **DATED_EVENTS**: the days the text dates to a month, from Noah's flood to
  Esther, each with its verse, the text's year (`when`), a story group
  (STORIES), a short label and a card. `also` gathers the parallel verses of
  one event (the siege in 2 Kings 25:1, Jeremiah 39:1; 52:4 and Ezekiel 24:1),
  `day_alt` the other book's day where Kings and Jeremiah differ, `months` a
  set over several months, and `month_end` and `day_end` a span. `doubt`
  says where a month or year is carried from context, and `month_from` marks
  a month the verse itself doesn't give ("context" or, for Elul, "calendar").
  Ezekiel 26:1 and 32:17 give a day but no month, and Ezekiel 40:1 gives "the
  beginning of the year", which is read as the first month or the seventh
  (`month` None for all three).
- **JOHN** and **ACTS**: where the Gospel of John and Acts name a feast,
  keyed to FEASTS. John 5:1's feast is unnamed, and so is Acts 18:21's
  "this coming feast"; Acts 27:9's "the Fast" is
  taken as the Day of Atonement, the usual reading, which the text doesn't
  state.
- **YEARS**: the seventh year (the year of release) and the Jubilee, with
  their rules, each citing its verses. The Jubilee is proclaimed with the
  trumpet on the Day of Atonement (Leviticus 25:9).
- **DAILY**, the continual burnt offering every feast's offerings are
  "besides" (Numbers 28:3-8), and **THREE_TIMES**, the three pilgrim feasts
  (Deuteronomy 16:16). **DEFINED** names the verse that sets each feast's
  day and the words that set it.
- **DIVISIONS**: David's twelve captains, one for each month (1 Chronicles
  27:1-15). **NOTES**: what the text leaves open (Elul, the counted feast,
  the Jubilee's start), for the cards, by topic.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Note:
    """A sentence for a card, and the verses it cites."""
    text: str
    refs: tuple = ()


@dataclass(frozen=True)
class Card:
    """WEB's own words: each fragment is found word for word in `refs`."""
    refs: tuple
    words: tuple

    def text(self):
        s = " … ".join(w.strip() for w in self.words)
        return s[:1].upper() + s[1:]


@dataclass(frozen=True)
class MonthName:
    name: str
    refs: tuple                 # every WEB verse that names the month
    numbered_by: tuple          # the verses that give its number
    note: Optional[Note] = None


@dataclass(frozen=True)
class Month:
    n: int
    names: tuple                # MonthName, in WEB's order (Abib before Nisan)
    modern: tuple               # ("March", "April"): approximate, not the text's


@dataclass(frozen=True)
class Offerings:
    """A day's burnt offerings (and the sin offering's goat), as Numbers
    28-29 or Leviticus 23 counts them."""
    bulls: int
    rams: int
    lambs: int
    goats: int
    peace_lambs: int = 0        # Leviticus 23:19's two lambs at weeks

    def row(self):
        """'Bulls 13, rams 2, lambs 14, goat 1'."""
        out = []
        for n, one, many in ((self.bulls, "bull", "bulls"), (self.rams, "ram", "rams"),
                             (self.lambs, "lamb", "lambs"), (self.goats, "goat", "goats")):
            if n:
                out.append(f"{one if n == 1 else many} {n}")
        if self.peace_lambs:
            out.append(f"lambs for peace offerings {self.peace_lambs}")
        s = ", ".join(out)
        return s[:1].upper() + s[1:]


@dataclass(frozen=True)
class Feast:
    key: str
    name: str                   # WEB's name
    aka: tuple                  # WEB's other names for it
    month: Optional[int]
    day: Optional[int]
    days: Optional[int]         # how many days it runs
    rest: Note
    offerings: Optional[Offerings]
    farming: Note
    refs: tuple
    card: Card
    label: str = ""             # a short name where WEB gives it none
    aka_refs: tuple = ()        # (name, the verse that uses it)
    pilgrim: bool = False       # one of the three times a year (Deut 16:16)
    counted: bool = False       # counted from another day, not dated
    later: bool = False         # not one of the Law's set feasts
    every: str = ""
    season: str = ""
    offerings_note: Optional[Note] = None
    offerings_by_day: tuple = ()
    offerings_by_day_refs: tuple = ()
    offerings_lev23: Optional[Offerings] = None
    date_note: Optional[Note] = None
    pilgrim_note: Optional[Note] = None
    name_note: Optional[Note] = None
    nt_refs: tuple = ()


@dataclass(frozen=True)
class Farm:
    key: str
    label: str
    basis: str                  # "stated", "derived" or "season"
    start: Optional[tuple]      # (month, day or None) the text gives
    end: Optional[tuple]
    refs: tuple
    card: Card
    basis_note: Optional[Note] = None
    drawn: tuple = ()           # (m0, d0, m1, d1, "stated" | "derived" | "convention")


@dataclass(frozen=True)
class Event:
    key: str
    ref: str
    month: Optional[int]
    day: Optional[int]
    label: str
    story: str
    when: str                   # the text's year, as it gives it
    card: Card
    also: tuple = ()
    months: tuple = ()
    month_end: Optional[int] = None
    day_end: Optional[int] = None
    day_alt: Optional[int] = None
    doubt: str = ""
    # where the month comes from when the verse doesn't number or name it:
    # "context" (carried from a verse nearby: "the same month", "this month",
    # "the second time") or "calendar" (Elul, which WEB never numbers)
    month_from: str = ""


@dataclass(frozen=True)
class Mention:
    """A verse of John or Acts that names a feast (`feast`, a FEASTS key)."""
    ref: str
    feast: Optional[str]
    label: str
    card: str


@dataclass(frozen=True)
class Rule:
    label: str
    text: str
    refs: tuple


@dataclass(frozen=True)
class Year:
    key: str
    name: str
    aka: tuple
    aka_refs: tuple
    every: int
    refs: tuple
    rules: tuple
    card: Card
    trumpet: Optional[tuple] = None     # (month, day, ref, Card)


def day_of_year(month, day):
    """A day's place on a schematic year of twelve 30-day months, from 0
    (the 1st of the first month) to 359. The text gives no month's length;
    this is a drawing's convention."""
    return (month - 1) * 30 + (day - 1)


def ordinal(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


STORIES = {
    "flood": "The flood",
    "exodus": "Egypt to the Jordan",
    "temple": "Solomon's temple",
    "kings": "The kings",
    "fall": "Jerusalem falls",
    "ezekiel": "Ezekiel",
    "other": "Daniel",
    "return": "The return",
    "nehemiah": "Nehemiah",
    "esther": "Esther",
}

MONTHS = (
    Month(1, (MonthName('Abib', ('Exod 13:4', 'Exod 23:15', 'Exod 34:18', 'Deut 16:1'), ('Exod 12:2', 'Exod 13:4'), note=Note('Never numbered beside its name; Exod 13:4 sets the going out in Abib, and Exod 12:2 makes that month the first.', ('Exod 13:4', 'Exod 12:2'))), MonthName('Nisan', ('Neh 2:1', 'Esth 3:7'), ('Esth 3:7',))),
          modern=('March', 'April')),
    Month(2, (MonthName('Ziv', ('1 Kgs 6:1', '1 Kgs 6:37'), ('1 Kgs 6:1',)),),
          modern=('April', 'May')),
    Month(3, (MonthName('Sivan', ('Esth 8:9',), ('Esth 8:9',)),),
          modern=('May', 'June')),
    Month(4, (),
          modern=('June', 'July')),
    Month(5, (),
          modern=('July', 'August')),
    Month(6, (MonthName('Elul', ('Neh 6:15',), (), note=Note("WEB never numbers Elul. Its place as the sixth month is the later Jewish calendar's, consistent with Neh 6:15 (wall finished 25 Elul) followed by Neh 7:73; 8:2 (the seventh month).", ('Neh 6:15', 'Neh 7:73; 8:2'))),),
          modern=('August', 'September')),
    Month(7, (MonthName('Ethanim', ('1 Kgs 8:2',), ('1 Kgs 8:2',)),),
          modern=('September', 'October')),
    Month(8, (MonthName('Bul', ('1 Kgs 6:38',), ('1 Kgs 6:38',)),),
          modern=('October', 'November')),
    Month(9, (MonthName('Chislev', ('Neh 1:1', 'Zech 7:1'), ('Zech 7:1',)),),
          modern=('November', 'December')),
    Month(10, (MonthName('Tebeth', ('Esth 2:16',), ('Esth 2:16',)),),
          modern=('December', 'January')),
    Month(11, (MonthName('Shebat', ('Zech 1:7',), ('Zech 1:7',)),),
          modern=('January', 'February')),
    Month(12, (MonthName('Adar', ('Ezra 6:15', 'Esth 3:7', 'Esth 3:13', 'Esth 8:12', 'Esth 9:1', 'Esth 9:15', 'Esth 9:17', 'Esth 9:19', 'Esth 9:21'), ('Esth 3:7', 'Esth 3:13', 'Esth 8:12', 'Esth 9:1')),),
          modern=('February', 'March')),
)

FEASTS = (
    Feast(
        key='sabbath', name='Sabbath',
        aka=('Sabbath day', 'Sabbath of solemn rest', 'the seventh day'),
        month=None, day=None, days=1,
        every='seventh day of every week',
        rest=Note('Every Sabbath: a Sabbath of solemn rest, a holy convocation; no kind of work; kindle no fire; rest even in plowing time and harvest.', ('Lev 23:3', 'Exod 35:3', 'Exod 34:21')),
        offerings=Offerings(0, 0, 2, 0),
        offerings_note=Note('Two male lambs a year old, besides the continual burnt offering.', ('Num 28:9-10',)),
        farming=Note('None by date; Exod 34:21 keeps it even in plowing time and in harvest.', ('Exod 34:21',)),
        refs=('Exod 20:8-11', 'Exod 31:13-17', 'Exod 34:21', 'Exod 35:2-3', 'Lev 23:3', 'Num 28:9-10', 'Deut 5:12-15'),
        card=Card(('Lev 23:3', 'Exod 34:21', 'Deut 5:15'), ('Six days shall work be done, but on the seventh day is a Sabbath of solemn rest, a holy convocation', 'in plowing time and in harvest you shall rest', 'You shall remember that you were a servant in the land of Egypt'))),
    Feast(
        key='new_moon', name='new moon',
        aka=('beginnings of your months', 'New Moon'),
        month=None, day=1, days=1,
        every='first day of every month',
        rest=Note('The Law sets no rest day; Amos 8:5 shows trade waiting for the new moon to be gone.', ('Amos 8:5',)),
        offerings=Offerings(2, 1, 7, 1),
        offerings_note=Note('Burnt offering of two young bulls, one ram, seven lambs, and one male goat for a sin offering; trumpets blown over the offerings.', ('Num 28:11-15', 'Num 10:10')),
        farming=Note('None.', ()),
        refs=('Num 10:10', 'Num 28:11-15', 'Num 29:6', '1 Sam 20:5', '1 Sam 20:18', '1 Sam 20:24-27', '2 Kgs 4:23', 'Ps 81:3', 'Isa 66:23', 'Amos 8:5', 'Col 2:16'),
        card=Card(('Num 28:11', 'Num 10:10'), ('In the beginnings of your months, you shall offer a burnt offering to Yahweh', 'in the beginnings of your months, you shall blow the trumpets over your burnt offerings'))),
    Feast(
        key='passover', name='Passover',
        aka=('Yahweh’s Passover', 'feast of the Passover'),
        month=1, day=14, days=1,
        rest=Note('No holy convocation is set for the 14th itself; the lamb is killed at evening.', ('Exod 12:6; Lev 23:5',)),
        offerings=None,
        offerings_note=Note('The household lamb, without defect, a male a year old, from the sheep or goats, chosen on the 10th. Numbers 28 lists no added offering for the 14th.', ('Exod 12:3-6', 'Numbers 28')),
        pilgrim_note=Note('Not in the three-times list (Deut 16:16 names the feast of unleavened bread), but Deut 16:5-6 has the Passover sacrificed only at the place Yahweh chooses.', ('Deut 16:16', 'Deut 16:5-6')),
        farming=Note('Falls in Abib, in harvest time: the Jordan overflowed its banks when Israel crossed on the 10th of the first month, and they ate the produce of the land the day after the Passover.', ('Josh 3:15; 4:19', 'Josh 5:10-11')),
        refs=('Exod 12:1-14', 'Exod 12:21-27', 'Exod 12:43-49', 'Exod 34:25', 'Lev 23:5', 'Num 9:1-5', 'Num 28:16', 'Deut 16:1-7'),
        nt_refs=('Luke 2:41', 'John 2:13', 'John 6:4', 'John 11:55', 'Matt 26:2', 'Matt 26:17-19', 'Mark 14:1', 'Mark 14:12-16', 'Luke 22:1', 'Luke 22:7-15', '1 Cor 5:7'),
        card=Card(('Lev 23:5', 'Exod 12:13', 'Deut 16:1'), ('In the first month, on the fourteenth day of the month in the evening, is Yahweh’s Passover', 'when I see the blood, I will pass over you', 'in the month of Abib Yahweh your God brought you out of Egypt by night'))),
    Feast(
        key='unleavened_bread', name='feast of unleavened bread',
        aka=('days of unleavened bread', 'days of Unleavened Bread'),
        month=1, day=15, days=7,
        pilgrim=True,
        rest=Note('Holy convocation, no regular work, on the 1st day (1/15) and the 7th day (1/21); Exod 12:16 allows only what every man must eat; Deut 16:8 calls the seventh day a solemn assembly.', ('Lev 23:7-8; Num 28:18,25', 'Exod 12:16', 'Deut 16:8')),
        offerings=Offerings(2, 1, 7, 1),
        offerings_note=Note('Each of the seven days: two young bulls, one ram, seven male lambs, one male goat for a sin offering.', ('Num 28:19-24',)),
        offerings_by_day=(Offerings(2, 1, 7, 1), Offerings(2, 1, 7, 1), Offerings(2, 1, 7, 1), Offerings(2, 1, 7, 1), Offerings(2, 1, 7, 1), Offerings(2, 1, 7, 1), Offerings(2, 1, 7, 1)),
        date_note=Note('Exod 12:18 counts it from the 14th at evening until the 21st at evening.', ('Exod 12:18',)),
        farming=Note('Barley time: Exod 9:31-32 has the barley in the ear before the exodus, and the sheaf of first fruits is waved in these days.', ('Lev 23:10-11', 'Exod 9:31-32')),
        refs=('Exod 12:15-20', 'Exod 13:3-10', 'Exod 23:15', 'Exod 34:18', 'Lev 23:6-8', 'Num 28:17-25', 'Deut 16:3-4', 'Deut 16:8', 'Deut 16:16'),
        nt_refs=('Matt 26:17', 'Mark 14:1', 'Mark 14:12', 'Luke 22:1', 'Luke 22:7', 'Acts 12:3', 'Acts 20:6'),
        card=Card(('Lev 23:6', 'Deut 16:3'), ('On the fifteenth day of the same month is the feast of unleavened bread to Yahweh', 'Seven days you shall eat unleavened bread', 'for you came out of the land of Egypt in haste'))),
    Feast(
        key='first_fruits_sheaf', name='the sheaf of the first fruits',
        aka=('sheaf of the wave offering',),
        month=1, day=None, days=1,
        rest=Note('None stated.', ()),
        offerings=None,
        offerings_note=Note('Not in Numbers 28-29. Lev 23:12-13: one male lamb a year old for a burnt offering, two tenths of an ephah of fine flour, a fourth of a hin of wine.', ('Numbers 28-29', 'Lev 23:12-13')),
        offerings_lev23=Offerings(0, 0, 1, 0),
        date_note=Note('“On the next day after the Sabbath”: inside the feast of unleavened bread, but WEB does not say which Sabbath, so it has no fixed day; the dial draws it across the 15th to the 21st.', ('Lev 23:11',)),
        farming=Note('The first of the grain harvest: no bread, roasted grain or fresh grain may be eaten until it is brought. WEB says ‘your harvest’, not barley; barley is inferred from Exod 9:31-32 and Ruth 1:22; 2:23.', ('Lev 23:14', 'Exod 9:31-32', 'Ruth 1:22; 2:23')),
        refs=('Lev 23:9-15',),
        card=Card(('Lev 23:10-11', 'Lev 23:14'), ('you shall bring the sheaf of the first fruits of your harvest to the priest', 'On the next day after the Sabbath the priest shall wave it', 'You must not eat bread, or roasted grain, or fresh grain, until this same day'))),
    Feast(
        key='weeks', name='feast of weeks',
        aka=('feast of harvest', 'the day of the first fruits', 'Pentecost'),
        aka_refs=(('feast of harvest', 'Exod 23:16'), ('the day of the first fruits', 'Num 28:26'), ('Pentecost', 'Acts 2:1')),
        month=3, day=None, days=1,
        pilgrim=True, counted=True,
        rest=Note('Holy convocation, no regular work.', ('Lev 23:21; Num 28:26',)),
        offerings=Offerings(2, 1, 7, 1),
        offerings_note=Note('Num 28:27-30: two young bulls, one ram, seven lambs, one male goat. Lev 23:18-19 gives a different list with the two loaves: seven lambs, one young bull, two rams as burnt offering, one male goat for a sin offering, two male lambs for peace offerings.', ('Num 28:27-30', 'Lev 23:18-19')),
        offerings_lev23=Offerings(1, 2, 7, 1, peace_lambs=2),
        date_note=Note('Counted, not dated: seven Sabbaths from the day the sheaf was waved, fifty days to the day after the seventh Sabbath; seven weeks from the first sickle. Fifty days from the middle of the first month lands early in the third, where the dial draws it, dashed as counted.', ('Lev 23:15-16', 'Deut 16:9')),
        farming=Note('The first fruits of wheat harvest: two loaves baked with yeast, a new meal offering.', ('Exod 34:22', 'Lev 23:16-17')),
        refs=('Exod 23:16', 'Exod 34:22', 'Lev 23:15-21', 'Num 28:26-31', 'Deut 16:9-12', 'Deut 16:16', '2 Chr 8:13'),
        nt_refs=('Acts 2:1', 'Acts 20:16', '1 Cor 16:8'),
        card=Card(('Exod 34:22', 'Lev 23:16-17'), ('You shall observe the feast of weeks with the first fruits of wheat harvest', 'even to the next day after the seventh Sabbath you shall count fifty days', 'You shall bring out of your habitations two loaves of bread for a wave offering'))),
    Feast(
        key='trumpets', name='day of blowing of trumpets',
        aka=('a memorial of blowing of trumpets',),
        aka_refs=(('a memorial of blowing of trumpets', 'Lev 23:24'),),
        month=7, day=1, days=1,
        rest=Note('A solemn rest, a holy convocation; no regular work.', ('Lev 23:24-25; Num 29:1',)),
        offerings=Offerings(1, 1, 7, 1),
        offerings_note=Note("One young bull, one ram, seven lambs, one male goat, besides the new moon's offerings.", ('Num 29:2-5', 'Num 29:6')),
        farming=Note('None stated.', ()),
        refs=('Lev 23:23-25', 'Num 29:1-6'),
        card=Card(('Lev 23:24', 'Num 29:1'), ('In the seventh month, on the first day of the month, shall be a solemn rest to you, a memorial of blowing of trumpets, a holy convocation', 'it is a day of blowing of trumpets to you'))),
    Feast(
        key='atonement', name='Day of Atonement',
        aka=('day of atonement',),
        aka_refs=(('Day of Atonement', 'Lev 25:9'), ('day of atonement', 'Lev 23:27')),
        month=7, day=10, days=1,
        rest=Note('A Sabbath of solemn rest; no kind of work; afflict your souls; kept from the 9th at evening to evening.', ('Lev 16:29-31; 23:27-32; Num 29:7',)),
        offerings=Offerings(1, 1, 7, 1),
        offerings_note=Note('One young bull, one ram, seven lambs, one male goat, besides the sin offering of atonement; the atonement rite itself is Leviticus 16.', ('Num 29:8-11', 'Leviticus 16')),
        farming=Note('None stated. In the fiftieth year the Jubilee trumpet sounds on this day.', ('Lev 25:9',)),
        refs=('Lev 16:29-34', 'Lev 23:26-32', 'Lev 25:9', 'Num 29:7-11'),
        card=Card(('Lev 23:27', 'Lev 16:30', 'Lev 16:34'), ('on the tenth day of this seventh month is the day of atonement', 'for on this day shall atonement be made for you, to cleanse you', 'to make atonement for the children of Israel once in the year because of all their sins'))),
    Feast(
        key='tents', name='feast of tents',
        aka=('feast of ingathering', 'Feast of Booths', 'the feast of Yahweh', 'the feast of the seventh month', 'feast of harvest at the year’s end'),
        aka_refs=(('feast of ingathering', 'Exod 23:16'), ('Feast of Booths', 'John 7:2'), ('the feast of Yahweh', 'Lev 23:39'), ('the feast of the seventh month', 'Neh 8:14'), ('feast of harvest at the year’s end', 'Exod 34:22')),
        month=7, day=15, days=7,
        pilgrim=True,
        rest=Note('Holy convocation, no regular work, on the 1st day (7/15). Dwell in temporary shelters seven days.', ('Lev 23:35,39; Num 29:12', 'Lev 23:42')),
        offerings=Offerings(13, 2, 14, 1),
        offerings_note=Note('The bulls fall by one a day, from thirteen to seven, with two rams, fourteen lambs and one male goat each day; the eighth day follows with its own.', ('Num 29:13-34',)),
        offerings_by_day=(Offerings(13, 2, 14, 1), Offerings(12, 2, 14, 1), Offerings(11, 2, 14, 1), Offerings(10, 2, 14, 1), Offerings(9, 2, 14, 1), Offerings(8, 2, 14, 1), Offerings(7, 2, 14, 1), Offerings(1, 1, 7, 1)),
        offerings_by_day_refs=('Num 29:13-16', 'Num 29:17-19', 'Num 29:20-22', 'Num 29:23-25', 'Num 29:26-28', 'Num 29:29-31', 'Num 29:32-34', 'Num 29:35-38'),
        farming=Note("The year's end ingathering: kept after gathering in from the threshing floor and the wine press, when the fruits of the land are gathered in.", ('Deut 16:13', 'Lev 23:39')),
        refs=('Exod 23:16', 'Exod 34:22', 'Lev 23:33-43', 'Num 29:12-34', 'Deut 16:13-16', 'Deut 31:10-13', 'Neh 8:14-18', 'Ezra 3:4', '2 Chr 8:13', 'Zech 14:16-19'),
        nt_refs=('John 7:2', 'John 7:37'),
        card=Card(('Lev 23:34', 'Deut 16:13', 'Lev 23:43'), ('On the fifteenth day of this seventh month is the feast of tents for seven days to Yahweh', 'after you have gathered in from your threshing floor and from your wine press', 'I made the children of Israel to dwell in temporary shelters, when I brought them out of the land of Egypt'))),
    Feast(
        key='eighth_day', name='the eighth day',
        aka=('solemn assembly',),
        month=7, day=22, days=1,
        rest=Note('Holy convocation, a solemn assembly, a solemn rest; no regular work.', ('Lev 23:36,39; Num 29:35',)),
        offerings=Offerings(1, 1, 7, 1),
        offerings_note=Note('One bull, one ram, seven lambs, one male goat.', ('Num 29:36-38',)),
        pilgrim_note=Note('Follows the seven days of the feast of tents; Deut 16:16 counts only the feast itself.', ('Deut 16:16',)),
        farming=Note('None stated.', ()),
        refs=('Lev 23:36', 'Lev 23:39', 'Num 29:35-38', 'Neh 8:18', '2 Chr 7:9'),
        nt_refs=('John 7:37',),
        card=Card(('Num 29:35', 'Neh 8:18'), ('On the eighth day you shall have a solemn assembly: you shall do no regular work', 'They kept the feast seven days; and on the eighth day was a solemn assembly, according to the ordinance'))),
    Feast(
        key='second_passover', name='Passover',
        label='second Passover',
        aka=(),
        month=2, day=14, days=1,
        later=True,
        rest=Note('None stated.', ()),
        offerings=None,
        offerings_note=Note('Kept by the statute of the Passover.', ('Num 9:12',)),
        name_note=Note('WEB has no name like ‘second Passover’; it is the Passover kept a month late.', ()),
        farming=Note('None stated.', ()),
        refs=('Num 9:6-14', '2 Chr 30:2-3', '2 Chr 30:13', '2 Chr 30:15'),
        card=Card(('Num 9:10-11', '2 Chr 30:15'), ('If any man of you or of your generations is unclean by reason of a dead body, or is on a journey far away, he shall still keep the Passover to Yahweh', 'In the second month, on the fourteenth day at evening they shall keep it', 'they killed the Passover on the fourteenth day of the second month'))),
    Feast(
        key='purim', name='Purim',
        aka=('days of Purim',),
        month=12, day=14, days=2,
        later=True,
        rest=Note('Days of feasting and gladness and rest from their enemies; no Mosaic work rule.', ('Esth 9:17-22',)),
        offerings=None,
        offerings_note=Note('No sacrifices; presents of food to one another and gifts to the needy.', ('Esth 9:22',)),
        date_note=Note('The 14th and 15th of Adar; the villages rested on the 14th, Shushan on the 15th.', ('Esth 9:21', 'Esth 9:17-19')),
        farming=Note('None.', ()),
        refs=('Esth 3:7', 'Esth 9:17-32'),
        card=Card(('Esth 9:21-22', 'Esth 9:26'), ('they should keep the fourteenth and fifteenth days of the month Adar yearly', 'the month which was turned to them from sorrow to gladness', 'they called these days “Purim”, from the word “Pur.”'))),
    Feast(
        key='dedication', name='Feast of the Dedication',
        aka=(),
        month=None, day=None, days=None,
        later=True,
        season='winter',
        rest=Note('Not stated.', ()),
        offerings=None,
        date_note=Note('WEB gives only ‘winter’, not a month or a day.', ('John 10:23',)),
        farming=Note('None.', ()),
        refs=('John 10:22-23',),
        card=Card(('John 10:22-23',), ('It was the Feast of the Dedication at Jerusalem', 'It was winter, and Jesus was walking in the temple, in Solomon’s porch'))),
)

FARMING = (
    Farm(
        key='jordan_flood', label='Jordan overflows', basis='stated',
        start=(1, None), end=(1, None),
        drawn=((1, 1, 1, 30, 'stated'),),
        refs=('Josh 3:15', 'Josh 4:19', '1 Chr 12:15'),
        card=Card(('Josh 3:15', 'Josh 4:19'), ('the Jordan overflows all its banks all the time of harvest', 'The people came up out of the Jordan on the tenth day of the first month'))),
    Farm(
        key='barley_harvest', label='Barley harvest', basis='derived',
        start=(1, None), end=None,
        basis_note=Note('No verse says barley and the first month together. Barley begins the harvest (‘in the first days, at the beginning of barley harvest’), and the harvest is under way in the first month: the Jordan overflows all the time of harvest when Israel crosses on the 10th, the sheaf of the first fruits of ‘your harvest’ is waved in the days of unleavened bread, and they eat parched grain the day after the Passover. So month 1, by joining them. WEB gives no end date; Ruth 2:23 ends it before the end of wheat harvest. The dial runs it through the second month by convention.', ('2 Sam 21:9', 'Josh 3:15; 4:19', 'Lev 23:10-11', 'Josh 5:11', 'Ruth 2:23')),
        drawn=((1, 1, 1, 30, 'derived'), (2, 1, 2, 30, 'convention')),
        refs=('Exod 9:31-32', 'Lev 23:10-14', 'Josh 5:11', 'Ruth 1:22', 'Ruth 2:23', 'Ruth 3:2', '2 Sam 21:9-10'),
        card=Card(('Exod 9:31', 'Ruth 1:22', 'Ruth 2:23'), ('the barley was in the ear, and the flax was in bloom', 'They came to Bethlehem in the beginning of barley harvest', 'to glean to the end of barley harvest and of wheat harvest'))),
    Farm(
        key='grain_count', label='Seven harvest weeks', basis='stated',
        start=(1, None), end=(3, None),
        basis_note=Note('Deut 16:9 counts the seven weeks from the first sickle; Lev 23:15-16 counts them from the sheaf (month 1) to the feast of weeks (about month 3).', ('Deut 16:9', 'Lev 23:15-16')),
        drawn=((1, 16, 3, 6, 'convention'),),
        refs=('Deut 16:9-10', 'Lev 23:15-16', 'Jer 5:24'),
        card=Card(('Deut 16:9', 'Jer 5:24'), ('From the time you begin to put the sickle to the standing grain you shall begin to count seven weeks', 'who preserves to us the appointed weeks of the harvest'))),
    Farm(
        key='wheat_harvest', label='Wheat harvest', basis='derived',
        start=None, end=(3, None),
        basis_note=Note('Its first fruits are brought at the feast of weeks, which is counted, not dated: fifty days from the sheaf puts it about month 3. It follows barley; WEB gives no start date. The dial starts it in the second month by convention.', ('Exod 34:22', 'Lev 23:15-16', 'Exod 9:32; Ruth 2:23')),
        drawn=((2, 1, 2, 30, 'convention'), (3, 1, 3, 30, 'derived')),
        refs=('Exod 9:32', 'Exod 34:22', 'Ruth 2:23', 'Judg 15:1', '1 Sam 6:13', '1 Sam 12:17-18'),
        card=Card(('Exod 34:22', '1 Sam 12:17-18'), ('You shall observe the feast of weeks with the first fruits of wheat harvest', 'Isn’t it wheat harvest today? I will call to Yahweh, that he may send thunder and rain', 'Yahweh sent thunder and rain that day'))),
    Farm(
        key='dry_harvest', label='Rainless harvest', basis='season',
        start=None, end=None,
        basis_note=Note("Rain in harvest is out of place; the thunder at wheat harvest was a sign; Rizpah watched from the beginning of barley harvest until rain fell. No month is given for the rain's return.", ('Prov 26:1', '1 Sam 12:17-18', '2 Sam 21:10')),
        refs=('Prov 26:1', '1 Sam 12:17-18', '2 Sam 21:10'),
        card=Card(('Prov 26:1', '2 Sam 21:10'), ('Like snow in summer, and as rain in harvest, so honor is not fitting for a fool', 'from the beginning of harvest until water poured on them from the sky'))),
    Farm(
        key='spring_figs_vines', label='Figs and blossom', basis='season',
        start=None, end=None,
        refs=('Song 2:11-13', 'Isa 18:5', 'Isa 28:4', 'Matt 24:32'),
        card=Card(('Song 2:11-13', 'Matt 24:32'), ('the winter is past. The rain is over and gone', 'The fig tree ripens her green figs. The vines are in blossom', 'When its branch has now become tender, and produces its leaves, you know that the summer is near'))),
    Farm(
        key='first_ripe_grapes', label='First-ripe grapes', basis='season',
        start=None, end=None,
        basis_note=Note("Num 13:20 dates the spies' errand only by the grapes. The text gives no month.", ('Num 13:20',)),
        drawn=((4, 1, 5, 30, 'convention'),),
        refs=('Num 13:20', 'Num 13:23'),
        card=Card(('Num 13:20', 'Num 13:23'), ('Now the time was the time of the first-ripe grapes', 'cut down from there a branch with one cluster of grapes'))),
    Farm(
        key='summer_fruit', label='Summer fruit', basis='season',
        start=None, end=(7, None),
        basis_note=Note("Season only. Jer 40:10-12 has wine, summer fruits and oil gathered before Ishmael came in the seventh month, which puts that year's gathering before month 7 but gives no month for it.", ('Jer 41:1', 'Jer 40:10-12')),
        drawn=((5, 1, 6, 30, 'convention'),),
        refs=('Jer 40:10-12', 'Jer 41:1', 'Amos 8:1-2', 'Jer 8:20', 'Mic 7:1'),
        card=Card(('Jer 40:10', 'Jer 8:20'), ('gather wine and summer fruits and oil, and put them in your vessels', 'The harvest is past. The summer has ended'))),
    Farm(
        key='ingathering', label='Ingathering', basis='stated',
        start=None, end=(7, 15),
        basis_note=Note('The feast of tents (7/15) is kept when the fruits of the land are gathered in, after the threshing floor and wine press; Exod 23:16 puts the ingathering at the end of the year. Covers grapes and olives: grain, new wine and oil.', ('Lev 23:39', 'Deut 16:13', 'Deut 11:14', 'Exod 23:16')),
        drawn=((6, 1, 6, 30, 'convention'), (7, 1, 7, 15, 'stated')),
        refs=('Exod 23:16', 'Exod 34:22', 'Lev 23:39', 'Deut 16:13', 'Deut 11:14', 'Deut 24:20-21', 'Lev 26:5'),
        card=Card(('Exod 23:16', 'Lev 23:39', 'Deut 16:13'), ('the feast of ingathering, at the end of the year, when you gather in your labors out of the field', 'on the fifteenth day of the seventh month, when you have gathered in the fruits of the land', 'after you have gathered in from your threshing floor and from your wine press'))),
    Farm(
        key='former_rain', label='Former rain', basis='season',
        start=None, end=None,
        basis_note=Note('Named, never dated. It comes before the latter rain; Ps 84:6 calls it the autumn rain in WEB. The dial draws it after the ingathering, about months 7 to 9, by convention; no verse gives its month.', ('Deut 11:14; Joel 2:23', 'Ps 84:6')),
        drawn=((7, 16, 9, 30, 'convention'),),
        refs=('Deut 11:14', 'Jer 5:24', 'Joel 2:23', 'Ps 84:6', 'James 5:7'),
        card=Card(('Deut 11:14', 'James 5:7'), ('I will give the rain of your land in its season, the former rain and the latter rain, that you may gather in your grain, your new wine, and your oil', 'the farmer waits for the precious fruit of the earth, being patient over it, until it receives the early and late rain'))),
    Farm(
        key='plowing_sowing', label='Plowing and sowing', basis='season',
        start=None, end=None,
        basis_note=Note('Plowing is in the winter; sowing follows the vintage. No month is given. The dial draws it after the ingathering, about months 8 to 10, by convention.', ('Prov 20:4', 'Lev 26:5')),
        drawn=((8, 1, 10, 30, 'convention'),),
        refs=('Gen 8:22', 'Exod 34:21', 'Lev 26:5', 'Prov 20:4', 'Eccl 11:4-6'),
        card=Card(('Prov 20:4', 'Lev 26:5', 'Eccl 11:6'), ('The sluggard will not plow by reason of the winter; therefore he shall beg in harvest, and have nothing', 'the vintage shall reach to the sowing time', 'In the morning sow your seed, and in the evening don’t withhold your hand'))),
    Farm(
        key='great_rain', label='Great rain', basis='stated',
        start=(9, 20), end=(9, 20),
        drawn=((9, 20, 9, 20, 'stated'),),
        refs=('Ezra 10:9', 'Ezra 10:13'),
        card=Card(('Ezra 10:9', 'Ezra 10:13'), ('It was the ninth month, on the twentieth day of the month', 'trembling because of this matter, and because of the great rain', 'it is a time of much rain, and we are not able to stand outside'))),
    Farm(
        key='winter_house', label='Winter house', basis='stated',
        start=(9, None), end=(9, None),
        drawn=((9, 1, 9, 30, 'stated'),),
        refs=('Jer 36:22', 'Amos 3:15'),
        card=Card(('Jer 36:22',), ('the king was sitting in the winter house in the ninth month; and there was a fire in the brazier burning before him',))),
    Farm(
        key='latter_rain', label='Latter rain', basis='season',
        start=None, end=None,
        basis_note=Note('Named, never dated. WEB calls it the latter rain, the late rain, the spring rain and rain in the spring time. The dial draws it before the barley harvest, about months 12 and 1, by convention; no verse gives its month.', ('Deut 11:14; Jer 3:3; Joel 2:23', 'James 5:7', 'Hos 6:3; Job 29:23; Prov 16:15', 'Zech 10:1')),
        drawn=((12, 1, 1, 30, 'convention'),),
        refs=('Deut 11:14', 'Jer 3:3', 'Jer 5:24', 'Joel 2:23', 'Hos 6:3', 'Zech 10:1', 'Job 29:23', 'Prov 16:15', 'James 5:7', 'Amos 4:7'),
        card=Card(('Zech 10:1', 'Hos 6:3', 'Amos 4:7'), ('Ask of Yahweh rain in the spring time', 'He will come to us like the rain, like the spring rain that waters the earth', 'I also have withheld the rain from you, when there were yet three months to the harvest'))),
)


NOTES = {
    'month_one': Note('Month 1 is the month of the exodus: ‘This month shall be to you the beginning of months’, ‘Today you go out in the month Abib’. WEB usually numbers months (first month... twelfth month) rather than naming them.', ('Exod 12:2', 'Exod 13:4')),
    'month_names': Note('Month names in WEB: Abib (1), Nisan (1), Ziv (2), Sivan (3), Elul (unnumbered, 6th by later usage), Ethanim (7), Bul (8), Chislev (9), Tebeth (10), Shebat (11), Adar (12). Abib, Ziv, Ethanim and Bul appear only in Exodus, Deuteronomy and 1 Kings; Nisan, Sivan, Elul, Chislev, Tebeth, Shebat and Adar appear only in Ezra, Nehemiah, Esther and Zechariah. WEB never names months 4 and 5.', ()),
    'tammuz': Note('Tammuz in Ezek 8:14 (‘women sit there weeping for Tammuz’) is a god, not a month: WEB gives the fourth month no name.', ('Ezek 8:14',)),
    'lunar': Note("Months follow the moon: offerings and trumpets mark ‘the beginnings of your months’, Saul's table kept the new moon, and Ps 81:3 pairs the New Moon and the full moon with ‘our feast day’. WEB never states the number of days in a month.", ('Num 10:10; 28:11-15', '1 Sam 20:5,18,24-27', 'Ps 81:3')),
    'thirty_days': Note('The flood dates imply thirty-day months but do not state them: the waters came on the 17th day of the 2nd month, prevailed 150 days, and the ship rested on the 17th day of the 7th month: five months for 150 days.', ('Gen 7:11', 'Gen 7:24; 8:3', 'Gen 8:4')),
    'twelve_months': Note("Twelve months make the year: Solomon's twelve officers each provided a month and David's twelve divisions served month by month to the twelfth month. WEB never mentions a thirteenth (leap) month; how the lunar year kept pace with the harvest is not in the text.", ('1 Kgs 4:7', '1 Chr 27:1-15')),
    'modern': Note('‘Modern’ equivalents are approximate and not from the text: month 1 (Abib) falls about March-April because barley is in the ear and harvest under way.', ('Exod 9:31', 'Josh 3:15; 4:19; Lev 23:10-11')),
    'autumn_turn': Note('The agricultural year also turns in the autumn: the feast of ingathering is ‘at the end of the year’ and ‘at the year’s end’, and kings went to war ‘at the return of the year’. WEB does not say these mark a second new year.', ('Exod 23:16', 'Exod 34:22', '2 Sam 11:1; 1 Kgs 20:22,26')),
    'tents_names': Note('WEB names the autumn feast ‘feast of tents’ in the Old Testament and ‘Feast of Booths’ only in John 7:2. Lev 23:42-43 says ‘temporary shelters’; Neh 8:14,17 says ‘booths’.', ('Lev 23:34; Deut 16:13,16; 31:10; Ezra 3:4; 2 Chr 8:13; Zech 14:16-19', 'John 7:2', 'Lev 23:42-43', 'Neh 8:14,17')),
    'feast_of_harvest': Note('‘Feast of harvest’ means the feast of weeks in Exod 23:16 (‘the first fruits of your labors’), but in Exod 34:22 ‘the feast of harvest at the year’s end’ is the autumn feast (where Exod 23:16 says ‘feast of ingathering’). So ‘feast of harvest’ is the feast of weeks only in Exod 23:16.', ('Exod 23:16', 'Exod 34:22')),
    'weeks_counted': Note('The feast of weeks has no date. It is counted: ‘seven Sabbaths shall be completed’ from the day the sheaf is waved, ‘even to the next day after the seventh Sabbath you shall count fifty days’; Deut 16:9 counts ‘seven weeks’ from the first sickle. Acts 2:1 calls it ‘the day of Pentecost’; also Acts 20:16; 1 Cor 16:8.', ('Lev 23:15-16', 'Deut 16:9', 'Acts 2:1', 'Acts 20:16', '1 Cor 16:8')),
    'sheaf_floats': Note('The sheaf of first fruits is waved ‘on the next day after the Sabbath’ without saying which Sabbath, so it too floats within the days of unleavened bread.', ('Lev 23:11',)),
    'weeks_offerings': Note('Feast of weeks offerings differ by source: Num 28:27-30 has 2 bulls, 1 ram, 7 lambs, 1 goat; Lev 23:18-19 (with the two loaves) has 1 bull, 2 rams, 7 lambs, 1 goat, plus 2 lambs for peace offerings.', ('Num 28:27-30', 'Lev 23:18-19')),
    'three_times': Note("The three pilgrim feasts (all males appear before Yahweh) are the feast of unleavened bread, the feast of weeks and the feast of tents; Exod 23:14-17 names them unleavened bread, harvest and ingathering, and Exod 34:18-23 unleavened bread, weeks, and the feast of harvest at the year's end.", ('Deut 16:16; 2 Chr 8:13', 'Exod 23:14-17', 'Exod 34:18-23')),
    'daily': Note("Daily, under every feast: the continual burnt offering of two male lambs a day, one in the morning and one at evening. Numbers 28-29's feast offerings are ‘besides’ it.", ('Num 28:3-8', 'Numbers 28-29')),
    'gospel_passovers': Note("Gospel Passovers: John 2:13,23; 4:45; 6:4; 11:55; 12:1,12,20; 13:1; 18:28,39; 19:14, and the last Passover in Matt 26:2,17-19; Mark 14:1,12-16; Luke 22:1,7-15. Luke 2:41: Jesus' parents went every year. John 7:2 is the Feast of Booths; John 7:37's ‘last and greatest day of the feast’ is not said to be the seventh or the eighth day.", ('John 2:13,23; 4:45; 6:4; 11:55; 12:1,12,20; 13:1; 18:28,39; 19:14', 'Matt 26:2,17-19', 'Mark 14:1,12-16', 'Luke 22:1,7-15', 'Luke 2:41', 'John 7:2', 'John 7:37')),
    'related_feasts': Note("Related dated feasts not in the Law: Solomon kept the feast seven days and seven more at the temple's dedication, in Ethanim (1 Kgs 8:2,65-66; 2 Chr 7:8-10, sending the people away on the 23rd of the seventh month); Hezekiah kept the Passover in the second month; Jeroboam devised a rival feast on the 15th of the eighth month at Bethel.", ('2 Chr 30:2,13,15', '1 Kgs 12:32-33', '1 Kgs 8:2,65-66', '2 Chr 7:8-10')),
    'later_fasts': Note('Later fasts: Zech 7:3,5 mentions fasting in the fifth and seventh months for seventy years, and Zech 8:19 names ‘the fasts of the fourth, fifth, seventh, and tenth months’. WEB does not say what each fast marks, so they are not set among the feasts here.', ('Zech 7:3,5', 'Zech 8:19')),
    'ezekiel_calendar': Note("Ezekiel's temple calendar sets a cleansing on the 1st and 7th of the first month, the Passover as ‘a feast of seven days’ with seven bulls and seven rams daily, and the same for the feast of the 15th of the seventh month. It is a vision and differs from Numbers 28-29.", ('Ezek 45:18-25', 'Numbers 28-29')),
    'dedication': Note('The Feast of the Dedication is the only feast whose month WEB does not give: just ‘It was winter’.', ('John 10:22', 'John 10:23')),
    'jubilee_count': Note('Jubilee count: Lev 25:8-10 counts forty-nine years and makes ‘the fiftieth year’ holy. The text does not say whether the fiftieth year is also the first year of the next seven, nor how a Jubilee following a seventh-year rest is fed (Lev 25:20-22 provides only for one fallow year).', ('Lev 25:8-10', 'Lev 25:20-22')),
    'jubilee_start': Note('Jubilee start: the trumpet sounds ‘on the tenth day of the seventh month. On the Day of Atonement’, while the months count from Abib. WEB does not say whether the Jubilee year runs from that day or from the first month.', ('Lev 25:9',)),
    'release_timing': Note('Release timing: Deut 15:1 releases debts ‘at the end of every seven years’ (a national year, read with the law at the feast of tents, Deut 31:10). The Hebrew servant goes free in the seventh year of his own service, which need not be the same year; Jer 34:14 quotes the rule as ‘At the end of seven years’.', ('Exod 21:2; Deut 15:12', 'Deut 15:1', 'Deut 31:10', 'Jer 34:14')),
    'never_kept': Note("No Sabbath year or Jubilee is ever recorded as kept in WEB; Lev 26:34-35,43 and 2 Chr 36:21 tie the seventy years of exile to the land's unkept Sabbaths. Neh 10:31 pledges to ‘forego the seventh year, and the exaction of every debt’.", ('Lev 26:34-35,43', '2 Chr 36:21', 'Neh 10:31')),
}

DATED_EVENTS = (
    Event(
        key='flood_begins', ref='Genesis 7:11', month=2, day=17,
        label='flood begins', story='flood',
        when='the six hundredth year of Noah’s life',
        card=Card(('Genesis 7:11',), ('In the six hundredth year of Noah’s life, in the second month, on the seventeenth day of the month, on the same day all the fountains of the great deep burst open, and the sky’s windows opened.',))),
    Event(
        key='ark_rests', ref='Genesis 8:4', month=7, day=17,
        label='ark rests', story='flood',
        when='the six hundredth year of Noah’s life (carried from Genesis 7:11)',
        doubt='The verse gives no year; it is the same year as Genesis 7:11 only because Genesis 8:13 then starts the six hundred first year.',
        card=Card(('Genesis 8:4',), ('The ship rested in the seventh month, on the seventeenth day of the month, on Ararat’s mountains.',))),
    Event(
        key='mountains_seen', ref='Genesis 8:5', month=10, day=1,
        label='mountaintops seen', story='flood',
        when='the six hundredth year of Noah’s life (carried from Genesis 7:11)',
        doubt='Year not restated in the verse.',
        card=Card(('Genesis 8:5',), ('The waters receded continually until the tenth month. In the tenth month, on the first day of the month, the tops of the mountains were visible.',))),
    Event(
        key='waters_dried', ref='Genesis 8:13', month=1, day=1,
        label='waters dried up', story='flood',
        when='the six hundred first year',
        card=Card(('Genesis 8:13',), ('In the six hundred first year, in the first month, the first day of the month, the waters were dried up from the earth. Noah removed the covering of the ship, and looked.',))),
    Event(
        key='earth_dry', ref='Genesis 8:14', month=2, day=27,
        label='earth dry', story='flood',
        when='the six hundred first year (carried from Genesis 8:13)',
        card=Card(('Genesis 8:14',), ('In the second month, on the twenty-seventh day of the month, the earth was dry.',))),
    Event(
        key='passover_egypt', ref='Exodus 12:6', month=1, day=14,
        month_from='context',
        label='Passover in Egypt', story='exodus',
        when='the year of the exodus (‘the first month of the year’, Exodus 12:2)',
        also=('Exodus 12:3', 'Exodus 12:28-29'),
        doubt='The day comes from the instruction (Exodus 12:6), whose ‘same month’ is the month of Exodus 12:2-3, ‘the first month of the year’; Exodus 12:28-29 tells that it was done. These verses also set the Passover itself, on the same day.',
        card=Card(('Exodus 12:6', 'Exodus 12:3', 'Exodus 12:28-29'), ('you shall keep it until the fourteenth day of the same month; and the whole assembly of the congregation of Israel shall kill it at evening.', 'At midnight, Yahweh struck all the firstborn in the land of Egypt'))),
    Event(
        key='leave_rameses', ref='Numbers 33:3', month=1, day=15,
        label='leave Rameses', story='exodus',
        when='the year of the exodus',
        also=('Exodus 13:4', 'Exodus 12:51'),
        card=Card(('Numbers 33:3', 'Exodus 13:4', 'Exodus 12:51'), ('They traveled from Rameses in the first month, on the fifteenth day of the first month; on the next day after the Passover, the children of Israel went out with a high hand in the sight of all the Egyptians',))),
    Event(
        key='wilderness_of_sin', ref='Exodus 16:1', month=2, day=15,
        label='wilderness of Sin', story='exodus',
        when='the first year, ‘after their departing out of the land of Egypt’',
        card=Card(('Exodus 16:1',), ('all the congregation of the children of Israel came to the wilderness of Sin, which is between Elim and Sinai, on the fifteenth day of the second month after their departing out of the land of Egypt.',))),
    Event(
        key='reach_sinai', ref='Exodus 19:1', month=3, day=None,
        label='reach Sinai', story='exodus',
        when='the first year, ‘after the children of Israel had gone out of the land of Egypt’',
        doubt='No day number: ‘on that same day’ is often read as the first of the month, but the text does not say so.',
        card=Card(('Exodus 19:1',), ('In the third month after the children of Israel had gone out of the land of Egypt, on that same day they came into the wilderness of Sinai.',))),
    Event(
        key='tabernacle_raised', ref='Exodus 40:17', month=1, day=1,
        label='tabernacle raised', story='exodus',
        when='the second year',
        also=('Exodus 40:2',),
        card=Card(('Exodus 40:17', 'Exodus 40:2'), ('In the first month in the second year, on the first day of the month, the tabernacle was raised up.',))),
    Event(
        key='sinai_passover', ref='Numbers 9:5', month=1, day=14,
        label='Passover at Sinai', story='exodus',
        when='the first month of the second year after they had come out of the land of Egypt (Numbers 9:1)',
        also=('Numbers 9:1-4',),
        card=Card(('Numbers 9:5', 'Numbers 9:1-4'), ('They kept the Passover in the first month, on the fourteenth day of the month, at evening, in the wilderness of Sinai.',))),
    Event(
        key='census_ordered', ref='Numbers 1:1', month=2, day=1,
        label='census', story='exodus',
        when='the second year after they had come out of the land of Egypt',
        also=('Numbers 1:18',),
        card=Card(('Numbers 1:1', 'Numbers 1:18'), ('Yahweh spoke to Moses in the wilderness of Sinai, in the Tent of Meeting, on the first day of the second month, in the second year after they had come out of the land of Egypt',))),
    Event(
        key='leave_sinai', ref='Numbers 10:11', month=2, day=20,
        label='leave Sinai', story='exodus',
        when='the second year',
        card=Card(('Numbers 10:11',), ('In the second year, in the second month, on the twentieth day of the month, the cloud was taken up from over the tabernacle of the testimony.',))),
    Event(
        key='miriam_dies', ref='Numbers 20:1', month=1, day=None,
        label='Miriam dies', story='exodus',
        when='not stated',
        doubt='The year is not given. Numbers 33:36-38 goes from Kadesh to Mount Hor, where Aaron died in the fortieth year, so it is usually read as the fortieth year; that is inference.',
        card=Card(('Numbers 20:1',), ('The children of Israel, even the whole congregation, came into the wilderness of Zin in the first month. The people stayed in Kadesh. Miriam died there, and was buried there.',))),
    Event(
        key='aaron_dies', ref='Numbers 33:38', month=5, day=1,
        label='Aaron dies', story='exodus',
        when='the fortieth year after the children of Israel had come out of the land of Egypt',
        card=Card(('Numbers 33:38',), ('Aaron the priest went up into Mount Hor at the commandment of Yahweh, and died there, in the fortieth year after the children of Israel had come out of the land of Egypt, in the fifth month, on the first day of the month.',))),
    Event(
        key='moses_speaks', ref='Deuteronomy 1:3', month=11, day=1,
        label='Moses’ address', story='exodus',
        when='the fortieth year',
        card=Card(('Deuteronomy 1:3',), ('In the fortieth year, in the eleventh month, on the first day of the month, Moses spoke to the children of Israel, according to all that Yahweh had given him in commandment to them',))),
    Event(
        key='cross_jordan', ref='Joshua 4:19', month=1, day=10,
        label='cross the Jordan', story='exodus',
        when='not stated (the spring after Moses’ death)',
        doubt='The year is not stated; it follows the fortieth year of Deuteronomy 1:3, but the text gives no number.',
        card=Card(('Joshua 4:19',), ('The people came up out of the Jordan on the tenth day of the first month, and encamped in Gilgal, on the east border of Jericho.',))),
    Event(
        key='gilgal_passover', ref='Joshua 5:10', month=1, day=14,
        month_from='context',
        label='Passover at Gilgal', story='exodus',
        when='the same year as Joshua 4:19',
        doubt='The verse names no month; the first month is carried from Joshua 4:19.',
        card=Card(('Joshua 5:10',), ('The children of Israel encamped in Gilgal. They kept the Passover on the fourteenth day of the month at evening in the plains of Jericho.',))),
    Event(
        key='manna_ceases', ref='Joshua 5:11-12', month=1, day=15,
        month_from='context',
        label='manna ceases', story='exodus',
        when='the same year as Joshua 4:19',
        doubt='Day 15 is ‘the next day after the Passover’ (as Numbers 33:3 counts it); the manna ceased ‘on the next day’ after that, which may be the 16th.',
        card=Card(('Joshua 5:11-12',), ('They ate unleavened cakes and parched grain of the produce of the land on the next day after the Passover, in the same day. The manna ceased on the next day, after they had eaten of the produce of the land.',))),
    Event(
        key='gadites_cross', ref='1 Chronicles 12:15', month=1, day=None,
        label='Gadites cross', story='kings',
        when='not stated (while David was at the stronghold, 1 Chronicles 12:8)',
        card=Card(('1 Chronicles 12:15',), ('These are those who went over the Jordan in the first month, when it had overflowed all its banks',))),
    Event(
        key='davids_divisions', ref='1 Chronicles 27:1-15', month=1, day=None,
        label='monthly divisions', story='kings',
        when='David’s reign',
        months=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
        doubt='One entry for the set: twelve captains, one per month (Jashobeam, Dodai, Benaiah, Asahel, Shamhuth, Ira, Helez, Sibbecai, Abiezer, Maharai, Benaiah, Heldai). One for each month.',
        card=Card(('1 Chronicles 27:1-15',), ('the divisions which came in and went out month by month throughout all the months of the year—of every division were twenty-four thousand.', 'Over the first division for the first month was Jashobeam the son of Zabdiel'))),
    Event(
        key='temple_begun', ref='2 Chronicles 3:2', month=2, day=2,
        label='temple begun', story='temple',
        when='the fourth year of his reign (the four hundred and eightieth year after the exodus, 1 Kings 6:1)',
        also=('1 Kings 6:1', '1 Kings 6:37'),
        doubt='The day comes only from 2 Chronicles 3:2; 1 Kings 6:1 and 6:37 give the month Ziv without a day.',
        card=Card(('2 Chronicles 3:2', '1 Kings 6:1', '1 Kings 6:37'), ('in the month Ziv, which is the second month, he began to build Yahweh’s house.', 'He began to build in the second day of the second month, in the fourth year of his reign.'))),
    Event(
        key='temple_finished', ref='1 Kings 6:38', month=8, day=None,
        label='temple finished', story='temple',
        when='the eleventh year (of Solomon)',
        card=Card(('1 Kings 6:38',), ('In the eleventh year, in the month Bul, which is the eighth month, the house was finished throughout all its parts, and according to all its specifications. So he spent seven years building it.',))),
    Event(
        key='ark_to_temple', ref='1 Kings 8:2', month=7, day=None,
        label='ark to temple', story='temple',
        when='not stated (after the house was finished)',
        also=('2 Chronicles 5:3',),
        doubt='No day; ‘the feast’ of the seventh month is presumably the feast of tents (15th), but the text does not name it. The year is not stated: the house was finished in the eighth month of the eleventh year (6:38).',
        card=Card(('1 Kings 8:2', '2 Chronicles 5:3'), ('All the men of Israel assembled themselves to king Solomon at the feast, in the month Ethanim, which is the seventh month.',))),
    Event(
        key='people_sent_home', ref='2 Chronicles 7:10', month=7, day=23,
        label='people sent home', story='temple',
        when='not stated (the dedication year)',
        also=('1 Kings 8:65-66', '2 Chronicles 7:8-9'),
        doubt='1 Kings 8:65-66 counts ‘seven days and seven more days’ and sends the people away ‘on the eighth day’; only Chronicles gives the 23rd.',
        card=Card(('2 Chronicles 7:10', '1 Kings 8:65-66', '2 Chronicles 7:8-9'), ('On the twenty-third day of the seventh month, he sent the people away to their tents, joyful and glad of heart for the goodness that Yahweh had shown to David, and to Solomon, and to Israel his people.',))),
    Event(
        key='jeroboams_feast', ref='1 Kings 12:32-33', month=8, day=15,
        label='Jeroboam’s feast', story='kings',
        when='not stated (Jeroboam’s first years)',
        card=Card(('1 Kings 12:32-33',), ('Jeroboam ordained a feast in the eighth month, on the fifteenth day of the month, like the feast that is in Judah', 'even in the month which he had devised of his own heart'))),
    Event(
        key='asa_assembly', ref='2 Chronicles 15:10', month=3, day=None,
        label='Asa’s assembly', story='kings',
        when='the fifteenth year of Asa’s reign',
        also=('2 Chronicles 15:11',),
        card=Card(('2 Chronicles 15:10', '2 Chronicles 15:11'), ('So they gathered themselves together at Jerusalem in the third month, in the fifteenth year of Asa’s reign. They sacrificed to Yahweh in that day',))),
    Event(
        key='hezekiah_begins', ref='2 Chronicles 29:17', month=1, day=1,
        label='cleansing begun', story='kings',
        when='the first year of his reign (2 Chronicles 29:3)',
        also=('2 Chronicles 29:3',),
        doubt='2 Chronicles 29:3 dates the opening of the doors to the first month, with no day; the 1st is when they began to sanctify the house.',
        card=Card(('2 Chronicles 29:17', '2 Chronicles 29:3'), ('Now they began on the first day of the first month to sanctify', 'In the first year of his reign, in the first month, he opened the doors of Yahweh’s house, and repaired them.'))),
    Event(
        key='hezekiah_cleansed', ref='2 Chronicles 29:17', month=1, day=16,
        label='temple cleansed', story='kings',
        when='the first year of his reign (2 Chronicles 29:3)',
        doubt='The same verse also dates the 8th (they reached the porch).',
        card=Card(('2 Chronicles 29:17',), ('on the eighth day of the month they came to Yahweh’s porch. They sanctified Yahweh’s house in eight days, and on the sixteenth day of the first month they finished.',))),
    Event(
        key='hezekiah_passover', ref='2 Chronicles 30:15', month=2, day=14,
        label='Hezekiah’s Passover', story='kings',
        when='not restated (after the cleansing of 2 Chronicles 29)',
        also=('2 Chronicles 30:2', '2 Chronicles 30:13', '2 Chronicles 30:21-23'),
        doubt='Chapter 30 gives no year; it is read as the first year because it follows chapter 29. 2 Chronicles 30:23 adds ‘another seven days’.',
        card=Card(('2 Chronicles 30:15', '2 Chronicles 30:2', '2 Chronicles 30:13', '2 Chronicles 30:21-23'), ('Then they killed the Passover on the fourteenth day of the second month.',))),
    Event(
        key='tithe_heaps', ref='2 Chronicles 31:7', month=3, day=None,
        label='tithe heaps', story='kings',
        when='not restated (Hezekiah’s reign)',
        month_end=7,
        doubt='Begun in the third month, finished in the seventh.',
        card=Card(('2 Chronicles 31:7',), ('In the third month they began to lay the foundation of the heaps, and finished them in the seventh month.',))),
    Event(
        key='josiah_passover', ref='2 Chronicles 35:1', month=1, day=14,
        label='Josiah’s Passover', story='kings',
        when='the eighteenth year of the reign of Josiah (2 Chronicles 35:19)',
        also=('2 Chronicles 35:19', '2 Kings 23:21-23'),
        doubt='2 Kings 23:23 gives the eighteenth year but no month or day.',
        card=Card(('2 Chronicles 35:1', '2 Chronicles 35:19', '2 Kings 23:21-23'), ('Josiah kept a Passover to Yahweh in Jerusalem. They killed the Passover on the fourteenth day of the first month.',))),
    Event(
        key='fast_proclaimed', ref='Jeremiah 36:9', month=9, day=None,
        label='fast proclaimed', story='fall',
        when='the fifth year of Jehoiakim the son of Josiah, king of Judah',
        card=Card(('Jeremiah 36:9',), ('Now in the fifth year of Jehoiakim the son of Josiah, king of Judah, in the ninth month, all the people in Jerusalem', 'proclaimed a fast before Yahweh.'))),
    Event(
        key='scroll_burned', ref='Jeremiah 36:22-23', month=9, day=None,
        label='scroll burned', story='fall',
        when='the fifth year of Jehoiakim (Jeremiah 36:9)',
        card=Card(('Jeremiah 36:22-23',), ('Now the king was sitting in the winter house in the ninth month; and there was a fire in the brazier burning before him.', 'the king cut it with the penknife, and cast it into the fire'))),
    Event(
        key='hananiah_speaks', ref='Jeremiah 28:1', month=5, day=None,
        label='Hananiah prophesies', story='fall',
        when='the beginning of the reign of Zedekiah king of Judah, in the fourth year',
        card=Card(('Jeremiah 28:1',), ('in the beginning of the reign of Zedekiah king of Judah, in the fourth year, in the fifth month, Hananiah the son of Azzur, the prophet, who was of Gibeon, spoke to me in Yahweh’s house',))),
    Event(
        key='hananiah_dies', ref='Jeremiah 28:17', month=7, day=None,
        label='Hananiah dies', story='fall',
        when='the same year (the fourth year of Zedekiah)',
        card=Card(('Jeremiah 28:17',), ('So Hananiah the prophet died the same year in the seventh month.',))),
    Event(
        key='siege_begins', ref='2 Kings 25:1', month=10, day=10,
        label='siege begins', story='fall',
        when='the ninth year of his reign (Zedekiah)',
        also=('Jeremiah 39:1', 'Jeremiah 52:4', 'Ezekiel 24:1-2'),
        card=Card(('2 Kings 25:1', 'Jeremiah 39:1', 'Jeremiah 52:4', 'Ezekiel 24:1-2'), ('In the ninth year of his reign, in the tenth month, in the tenth day of the month, Nebuchadnezzar king of Babylon came, he and all his army, against Jerusalem, and encamped against it',))),
    Event(
        key='wall_breached', ref='2 Kings 25:3-4', month=4, day=9,
        label='wall breached', story='fall',
        when='the eleventh year of king Zedekiah (2 Kings 25:2)',
        also=('Jeremiah 39:2', 'Jeremiah 52:6-7'),
        card=Card(('2 Kings 25:3-4', 'Jeremiah 39:2', 'Jeremiah 52:6-7'), ('On the ninth day of the fourth month, the famine was severe in the city, so that there was no bread for the people of the land. Then a breach was made in the city',))),
    Event(
        key='temple_burned', ref='2 Kings 25:8-9', month=5, day=7,
        label='temple burned', story='fall',
        when='the nineteenth year of king Nebuchadnezzar, king of Babylon',
        day_alt=10, also=('Jeremiah 52:12-13', 'Jeremiah 1:3'),
        doubt='Jeremiah 52:12 has ‘in the tenth day of the month’ for the same arrival of Nebuzaradan; Kings has the seventh. Jeremiah 1:3 dates ‘the carrying away of Jerusalem captive in the fifth month’.',
        card=Card(('2 Kings 25:8-9', 'Jeremiah 52:12-13', 'Jeremiah 1:3'), ('Now in the fifth month, on the seventh day of the month, which was the nineteenth year of king Nebuchadnezzar', 'He burned Yahweh’s house, the king’s house, and all the houses of Jerusalem'))),
    Event(
        key='gedaliah_killed', ref='2 Kings 25:25', month=7, day=None,
        label='Gedaliah killed', story='fall',
        when='not stated (after the city fell)',
        also=('Jeremiah 41:1-2',),
        doubt='No year is stated; it is usually read as the year the city fell.',
        card=Card(('2 Kings 25:25', 'Jeremiah 41:1-2'), ('But in the seventh month, Ishmael the son of Nethaniah, the son of Elishama, of the royal offspring came, and ten men with him, and struck Gedaliah, so that he died',))),
    Event(
        key='jehoiachin_released', ref='2 Kings 25:27', month=12, day=27,
        label='Jehoiachin released', story='fall',
        when='the thirty-seventh year of the captivity of Jehoiachin king of Judah',
        day_alt=25, also=('Jeremiah 52:31',),
        doubt='Jeremiah 52:31 has ‘the twenty-fifth day of the month’; Kings has the twenty-seventh.',
        card=Card(('2 Kings 25:27', 'Jeremiah 52:31'), ('In the thirty-seventh year of the captivity of Jehoiachin king of Judah, in the twelfth month, on the twenty-seventh day of the month, Evilmerodach king of Babylon', 'lifted up the head of Jehoiachin king of Judah out of prison'))),
    Event(
        key='ezekiel_call', ref='Ezekiel 1:1-2', month=4, day=5,
        label='visions of God', story='ezekiel',
        when='the thirtieth year … the fifth year of king Jehoiachin’s captivity',
        card=Card(('Ezekiel 1:1-2',), ('Now in the thirtieth year, in the fourth month, in the fifth of the month, as I was among the captives by the river Chebar, the heavens were opened, and I saw visions of God.',))),
    Event(
        key='ezekiel_8', ref='Ezekiel 8:1', month=6, day=5,
        label='carried to Jerusalem', story='ezekiel',
        when='the sixth year',
        also=('Ezekiel 8:3',),
        card=Card(('Ezekiel 8:1', 'Ezekiel 8:3'), ('In the sixth year, in the sixth month, in the fifth day of the month, as I sat in my house, and the elders of Judah sat before me, the Lord Yahweh’s hand fell on me there.',))),
    Event(
        key='ezekiel_20', ref='Ezekiel 20:1', month=5, day=10,
        label='elders inquire', story='ezekiel',
        when='the seventh year',
        card=Card(('Ezekiel 20:1',), ('In the seventh year, in the fifth month, the tenth day of the month, some of the elders of Israel came to inquire of Yahweh, and sat before me.',))),
    Event(
        key='ezekiel_24', ref='Ezekiel 24:1-2', month=10, day=10,
        label='write the day', story='ezekiel',
        when='the ninth year',
        doubt='The same day as the siege (2 Kings 25:1).',
        card=Card(('Ezekiel 24:1-2',), ('Again, in the ninth year, in the tenth month, in the tenth day of the month, Yahweh’s word came to me', '“Son of man, write the name of the day, this same day. The king of Babylon drew close to Jerusalem this same day.'))),
    Event(
        key='ezekiel_26', ref='Ezekiel 26:1-2', month=None, day=1,
        label='against Tyre', story='ezekiel',
        when='the eleventh year',
        doubt='The month is not given in WEB (‘in the first of the month’), so this cannot be placed on the dial without a guess.',
        card=Card(('Ezekiel 26:1-2',), ('In the eleventh year, in the first of the month, Yahweh’s word came to me', '“Son of man, because Tyre has said against Jerusalem, ‘Aha! She is broken!'))),
    Event(
        key='ezekiel_29', ref='Ezekiel 29:1-2', month=10, day=12,
        label='against Pharaoh', story='ezekiel',
        when='the tenth year',
        card=Card(('Ezekiel 29:1-2',), ('In the tenth year, in the tenth month, on the twelfth day of the month, Yahweh’s word came to me', 'set your face against Pharaoh king of Egypt'))),
    Event(
        key='ezekiel_29_17', ref='Ezekiel 29:17-18', month=1, day=1,
        label='Tyre’s wages', story='ezekiel',
        when='the twenty-seventh year',
        doubt='The latest date in Ezekiel.',
        card=Card(('Ezekiel 29:17-18',), ('It came to pass in the twenty-seventh year, in the first month, in the first day of the month, Yahweh’s word came to me', 'Nebuchadnezzar king of Babylon caused his army to serve a great service against Tyre.'))),
    Event(
        key='ezekiel_30_20', ref='Ezekiel 30:20-21', month=1, day=7,
        label='Pharaoh’s arm broken', story='ezekiel',
        when='the eleventh year',
        card=Card(('Ezekiel 30:20-21',), ('In the eleventh year, in the first month, in the seventh day of the month, Yahweh’s word came to me', '“Son of man, I have broken the arm of Pharaoh king of Egypt.'))),
    Event(
        key='ezekiel_31', ref='Ezekiel 31:1-2', month=3, day=1,
        label='Pharaoh’s greatness', story='ezekiel',
        when='the eleventh year',
        card=Card(('Ezekiel 31:1-2',), ('In the eleventh year, in the third month, in the first day of the month, Yahweh’s word came to me', 'tell Pharaoh king of Egypt, and his multitude: ‘Whom are you like in your greatness?'))),
    Event(
        key='ezekiel_32', ref='Ezekiel 32:1-2', month=12, day=1,
        label='lament for Pharaoh', story='ezekiel',
        when='the twelfth year',
        card=Card(('Ezekiel 32:1-2',), ('In the twelfth year, in the twelfth month, in the first day of the month, “Yahweh’s word came to me', 'take up a lamentation over Pharaoh king of Egypt'))),
    Event(
        key='ezekiel_32_17', ref='Ezekiel 32:17-18', month=None, day=15,
        label='wail for Egypt', story='ezekiel',
        when='the twelfth year',
        doubt='The month is not given in WEB; the twelfth month of Ezekiel 32:1 is a common reading but the text does not say so.',
        card=Card(('Ezekiel 32:17-18',), ('Also in the twelfth year, in the fifteenth day of the month, Yahweh’s word came to me', '“Son of man, wail for the multitude of Egypt'))),
    Event(
        key='city_fallen_news', ref='Ezekiel 33:21', month=10, day=5,
        label='news: city fallen', story='ezekiel',
        when='the twelfth year of our captivity',
        card=Card(('Ezekiel 33:21',), ('In the twelfth year of our captivity, in the tenth month, in the fifth day of the month, one who had escaped out of Jerusalem came to me, saying, “The city has been defeated!”',))),
    Event(
        key='ezekiel_40', ref='Ezekiel 40:1-2', month=None, day=10,
        label='new temple vision', story='ezekiel',
        when='the twenty-fifth year of our captivity … the fourteenth year after that the city was struck',
        doubt='WEB says ‘in the beginning of the year’, not a month. It is read as the first month, or as the seventh, the 10th then being the Day of Atonement; the text does not say which, so it is not placed on the dial.',
        card=Card(('Ezekiel 40:1-2',), ('In the twenty-fifth year of our captivity, in the beginning of the year, in the tenth day of the month', 'In the visions of God brought he me into the land of Israel'))),
    Event(
        key='sanctuary_cleansed', ref='Ezekiel 45:18-19', month=1, day=1,
        label='sanctuary cleansed', story='ezekiel',
        when='an ordinance in Ezekiel’s temple vision (the twenty-fifth year, Ezekiel 40:1)',
        doubt='An ordinance of the vision, not a dated event.',
        card=Card(('Ezekiel 45:18-19',), ('In the first month, in the first day of the month, you shall take a young bull without defect; and you shall cleanse the sanctuary.',))),
    Event(
        key='atonement_for_errors', ref='Ezekiel 45:20', month=1, day=7,
        month_from='context',
        label='atonement for house', story='ezekiel',
        when='an ordinance in Ezekiel’s temple vision',
        doubt='An ordinance of the vision; the month is carried from Ezekiel 45:18.',
        card=Card(('Ezekiel 45:20',), ('So you shall do on the seventh day of the month for everyone who errs, and for him who is simple. So you shall make atonement for the house.',))),
    Event(
        key='prince_passover', ref='Ezekiel 45:21-22', month=1, day=14,
        label='prince’s Passover', story='ezekiel',
        when='an ordinance in Ezekiel’s temple vision',
        doubt='Ezekiel’s vision restates the set Passover, as a feast of seven days.',
        card=Card(('Ezekiel 45:21-22',), ('In the first month, in the fourteenth day of the month, you shall have the Passover, a feast of seven days; unleavened bread shall be eaten.',))),
    Event(
        key='prince_seventh_month', ref='Ezekiel 45:25', month=7, day=15,
        label='prince’s feast', story='ezekiel',
        when='an ordinance in Ezekiel’s temple vision',
        doubt='Ezekiel’s vision restates the feast of the seventh month, without naming it. ‘like like’ is WEB’s own text.',
        card=Card(('Ezekiel 45:25',), ('In the seventh month, in the fifteenth day of the month, in the feast, he shall do like like that for seven days',))),
    Event(
        key='daniel_hiddekel', ref='Daniel 10:4', month=1, day=24,
        label='by the Hiddekel', story='other',
        when='the third year of Cyrus king of Persia (Daniel 10:1)',
        doubt='Daniel 10:2-3 says he had been mourning three whole weeks before this.',
        card=Card(('Daniel 10:4',), ('In the twenty-fourth day of the first month, as I was by the side of the great river, which is Hiddekel',))),
    Event(
        key='altar_offerings', ref='Ezra 3:6', month=7, day=1,
        label='offerings resume', story='return',
        when='not stated (the first seventh month after the return; the decree was in the first year of Cyrus, Ezra 1:1)',
        also=('Ezra 3:1-4',),
        doubt='Ezra 3:4 says they kept the feast of tents that month, without a day number.',
        card=Card(('Ezra 3:6', 'Ezra 3:1-4'), ('When the seventh month had come, and the children of Israel were in the cities, the people gathered themselves together as one man to Jerusalem.', 'From the first day of the seventh month, they began to offer burnt offerings to Yahweh'))),
    Event(
        key='temple_work_begins', ref='Ezra 3:8', month=2, day=None,
        label='work begins', story='return',
        when='the second year of their coming to God’s house at Jerusalem',
        card=Card(('Ezra 3:8',), ('Now in the second year of their coming to God’s house at Jerusalem, in the second month, Zerubbabel the son of Shealtiel, and Jeshua the son of Jozadak', 'began the work'))),
    Event(
        key='haggai_first', ref='Haggai 1:1', month=6, day=1,
        label='Haggai’s first word', story='return',
        when='the second year of Darius the king',
        doubt='Haggai spells the high priest ‘Joshua, the son of Jehozadak’; Ezra spells him ‘Jeshua the son of Jozadak’.',
        card=Card(('Haggai 1:1',), ('In the second year of Darius the king, in the sixth month, in the first day of the month, Yahweh’s word came by Haggai, the prophet, to Zerubbabel, the son of Shealtiel, governor of Judah, and to Joshua, the son of Jehozadak, the high priest',))),
    Event(
        key='work_resumes', ref='Haggai 1:14-15', month=6, day=24,
        label='work resumes', story='return',
        when='the second year of Darius the king',
        card=Card(('Haggai 1:14-15',), ('they came and worked on the house of Yahweh of Armies, their God, in the twenty-fourth day of the month, in the sixth month, in the second year of Darius the king.',))),
    Event(
        key='latter_glory', ref='Haggai 2:1', month=7, day=21,
        label='latter glory', story='return',
        when='the second year of Darius (Haggai 1:15)',
        also=('Haggai 2:9',),
        doubt='The verse gives no year; it follows Haggai 1:15. The 21st of the seventh month falls within the feast of tents.',
        card=Card(('Haggai 2:1', 'Haggai 2:9'), ('In the seventh month, in the twenty-first day of the month, Yahweh’s word came by Haggai the prophet', '‘The latter glory of this house will be greater than the former,’'))),
    Event(
        key='zechariah_call', ref='Zechariah 1:1-3', month=8, day=None,
        label='‘Return to me’', story='return',
        when='the second year of Darius',
        card=Card(('Zechariah 1:1-3',), ('In the eighth month, in the second year of Darius, Yahweh’s word came to Zechariah the son of Berechiah, the son of Iddo, the prophet', '‘Return to me,’ says Yahweh of Armies'))),
    Event(
        key='from_today_bless', ref='Haggai 2:10', month=9, day=24,
        label='from today I will bless', story='return',
        when='the second year of Darius',
        also=('Haggai 2:18-19',),
        doubt='Haggai 2:18 can be read as dating the laying of the foundation to this day; WEB’s wording leaves that open.',
        card=Card(('Haggai 2:10', 'Haggai 2:18-19'), ('In the twenty-fourth day of the ninth month, in the second year of Darius, Yahweh’s word came by Haggai the prophet', 'from the twenty-fourth day of the ninth month, since the day that the foundation of Yahweh’s temple was laid, consider it.', 'From today I will bless you.'))),
    Event(
        key='zerubbabel_signet', ref='Haggai 2:20-23', month=9, day=24,
        month_from='context',
        label='Zerubbabel a signet', story='return',
        when='the second year of Darius',
        doubt='Haggai 2:20 gives only the day; ‘the second time’ ties it to the ninth month of Haggai 2:10.',
        card=Card(('Haggai 2:20-23',), ('Yahweh’s word came the second time to Haggai in the twenty-fourth day of the month', 'will I take you, Zerubbabel, my servant, the son of Shealtiel,’ says Yahweh, ‘and will make you as a signet'))),
    Event(
        key='zechariah_night_visions', ref='Zechariah 1:7-8', month=11, day=24,
        label='night visions', story='return',
        when='the second year of Darius',
        card=Card(('Zechariah 1:7-8',), ('On the twenty-fourth day of the eleventh month, which is the month Shebat, in the second year of Darius, Yahweh’s word came to Zechariah', '“I had a vision in the night, and behold, a man riding on a red horse'))),
    Event(
        key='zechariah_fasting', ref='Zechariah 7:1-3', month=9, day=4,
        label='fasting question', story='return',
        when='the fourth year of king Darius',
        card=Card(('Zechariah 7:1-3',), ('In the fourth year of king Darius, Yahweh’s word came to Zechariah in the fourth day of the ninth month, the month of Chislev.', '“Should I weep in the fifth month, separating myself, as I have done these so many years?”'))),
    Event(
        key='fasts_to_feasts', ref='Zechariah 8:19', month=4, day=None,
        label='fasts become feasts', story='return',
        when='not stated (the answer to the question of Zechariah 7:1-3)',
        months=(4, 5, 7, 10), also=('Zechariah 7:3', 'Zechariah 7:5'),
        doubt='Four months, one entry. Linking these fasts to the dates of the fall (breach 4th, burning 5th, Gedaliah 7th, siege 10th) is a common reading; the text does not make the link. Zechariah 7:5 names the fifth and seventh.',
        card=Card(('Zechariah 8:19', 'Zechariah 7:3', 'Zechariah 7:5'), ('The fasts of the fourth, fifth, seventh, and tenth months shall be for the house of Judah joy and gladness, and cheerful feasts.',))),
    Event(
        key='second_temple_finished', ref='Ezra 6:15', month=12, day=3,
        label='house finished', story='return',
        when='the sixth year of the reign of Darius the king',
        card=Card(('Ezra 6:15',), ('This house was finished on the third day of the month Adar, which was in the sixth year of the reign of Darius the king.',))),
    Event(
        key='exiles_passover', ref='Ezra 6:19', month=1, day=14,
        label='exiles keep Passover', story='return',
        when='not restated (after the house was finished, Ezra 6:15)',
        also=('Ezra 6:20-22',),
        doubt='The year is not restated; it follows the sixth-year completion. Ezra 6:22 adds the feast of unleavened bread seven days.',
        card=Card(('Ezra 6:19', 'Ezra 6:20-22'), ('The children of the captivity kept the Passover on the fourteenth day of the first month.',))),
    Event(
        key='ezra_sets_out', ref='Ezra 7:9', month=1, day=1,
        label='Ezra sets out', story='return',
        when='the seventh year of Artaxerxes the king (Ezra 7:7)',
        card=Card(('Ezra 7:9',), ('For on the first day of the first month he began to go up from Babylon',))),
    Event(
        key='leave_ahava', ref='Ezra 8:31', month=1, day=12,
        label='leave Ahava', story='return',
        when='the seventh year of Artaxerxes (Ezra 7:7)',
        doubt='The year is carried from Ezra 7:7; Ezra 8 restates no year.',
        card=Card(('Ezra 8:31',), ('Then we departed from the river Ahava on the twelfth day of the first month, to go to Jerusalem.',))),
    Event(
        key='ezra_arrives', ref='Ezra 7:8-9', month=5, day=1,
        label='Ezra arrives', story='return',
        when='the seventh year of the king',
        doubt='Ezra 8:32-33 adds that after three days, ‘on the fourth day’, the silver and gold were weighed; that would be the 4th of the fifth month, by inference.',
        card=Card(('Ezra 7:8-9',), ('He came to Jerusalem in the fifth month, which was in the seventh year of the king.', 'on the first day of the fifth month he came to Jerusalem, according to the good hand of his God on him.'))),
    Event(
        key='assembly_in_rain', ref='Ezra 10:9', month=9, day=20,
        label='assembly in rain', story='return',
        when='not stated',
        doubt='Ezra 10 gives no year; it is usually read as the seventh year of Artaxerxes, carried from Ezra 7.',
        card=Card(('Ezra 10:9',), ('It was the ninth month, on the twentieth day of the month; and all the people sat in the wide place in front of God’s house, trembling because of this matter, and because of the great rain.',))),
    Event(
        key='inquiry_begins', ref='Ezra 10:16', month=10, day=1,
        label='inquiry begins', story='return',
        when='not stated (the same year as Ezra 10:9)',
        card=Card(('Ezra 10:16',), ('they sat down in the first day of the tenth month to examine the matter.',))),
    Event(
        key='inquiry_ends', ref='Ezra 10:17', month=1, day=1,
        label='inquiry ends', story='return',
        when='not stated (the year after Ezra 10:16, by the order of months)',
        doubt='The text gives no year; the first month after the tenth implies the next year.',
        card=Card(('Ezra 10:17',), ('They finished with all the men who had married foreign women by the first day of the first month.',))),
    Event(
        key='news_from_jerusalem', ref='Nehemiah 1:1-2', month=9, day=None,
        label='news from Jerusalem', story='nehemiah',
        when='the twentieth year',
        doubt='Chislev is the ninth month by Zechariah 7:1. Nehemiah 2:1 then puts Nisan (the first month) in the same ‘twentieth year’, so the two reckon the year differently or start it at different points; the text does not explain.',
        card=Card(('Nehemiah 1:1-2',), ('Now in the month Chislev, in the twentieth year, as I was in Shushan the palace, Hanani, one of my brothers, came, he and certain men out of Judah',))),
    Event(
        key='before_the_king', ref='Nehemiah 2:1', month=1, day=None,
        label='before the king', story='nehemiah',
        when='the twentieth year of Artaxerxes the king',
        doubt='Nisan is the first month by Esther 3:7.',
        card=Card(('Nehemiah 2:1',), ('In the month Nisan, in the twentieth year of Artaxerxes the king, when wine was before him, I picked up the wine, and gave it to the king.',))),
    Event(
        key='wall_finished', ref='Nehemiah 6:15', month=6, day=25,
        month_from='calendar',
        label='wall finished', story='nehemiah',
        when='not stated in the verse (Nehemiah’s governorship began in the twentieth year, Nehemiah 5:14)',
        doubt='WEB never numbers Elul; month 6 is the usual equation, not stated in the text.',
        card=Card(('Nehemiah 6:15',), ('So the wall was finished in the twenty-fifth day of Elul, in fifty-two days.',))),
    Event(
        key='law_read', ref='Nehemiah 8:2-3', month=7, day=1,
        label='law read', story='nehemiah',
        when='not stated (the seventh month after the wall, Nehemiah 7:73)',
        also=('Nehemiah 7:73',),
        card=Card(('Nehemiah 8:2-3', 'Nehemiah 7:73'), ('Ezra the priest brought the law before the assembly, both men and women, and all who could hear with understanding, on the first day of the seventh month. He read from it before the wide place that was in front of the water gate from early morning until midday',))),
    Event(
        key='law_studied', ref='Nehemiah 8:13-14', month=7, day=2,
        month_from='context',
        label='law studied', story='nehemiah',
        when='the same seventh month',
        doubt='‘On the second day’ is read as the second of the seventh month, following 8:2.',
        card=Card(('Nehemiah 8:13-14',), ('On the second day, the heads of fathers’ households of all the people, the priests, and the Levites were gathered together to Ezra the scribe, to study the words of the law. They found written in the law how Yahweh had commanded by Moses that the children of Israel should dwell in booths in the feast of the seventh month',))),
    Event(
        key='booths_kept', ref='Nehemiah 8:16-18', month=7, day=None,
        month_from='context',
        label='booths kept', story='nehemiah',
        when='the same seventh month',
        doubt='Kept at the set feast; the chapter gives no day numbers for it, and these verses no month: the seventh is carried from Nehemiah 8:2 and 8:14.',
        card=Card(('Nehemiah 8:16-18',), ('All the assembly of those who had come back out of the captivity made temporary shelters, and lived in the booths; for since the days of Jeshua the son of Nun to that day the children of Israel had not done so.', 'They kept the feast seven days; and on the eighth day was a solemn assembly'))),
    Event(
        key='fast_and_confession', ref='Nehemiah 9:1', month=7, day=24,
        month_from='context',
        label='fast and confession', story='nehemiah',
        when='the same seventh month (‘this month’)',
        doubt='‘this month’ is the seventh month of Nehemiah 8.',
        card=Card(('Nehemiah 9:1',), ('Now in the twenty-fourth day of this month the children of Israel were assembled with fasting, with sackcloth, and dirt on them.',))),
    Event(
        key='esther_to_king', ref='Esther 2:16-17', month=10, day=None,
        label='Esther made queen', story='esther',
        when='the seventh year of his reign (Ahasuerus)',
        card=Card(('Esther 2:16-17',), ('So Esther was taken to King Ahasuerus into his royal house in the tenth month, which is the month Tebeth, in the seventh year of his reign.', 'he set the royal crown on her head, and made her queen instead of Vashti.'))),
    Event(
        key='pur_cast', ref='Esther 3:7', month=1, day=None,
        label='Pur cast', story='esther',
        when='the twelfth year of King Ahasuerus',
        card=Card(('Esther 3:7',), ('In the first month, which is the month Nisan, in the twelfth year of King Ahasuerus, they cast Pur, that is, the lot, before Haman from day to day, and from month to month, and chose the twelfth month, which is the month Adar.',))),
    Event(
        key='hamans_decree', ref='Esther 3:12-13', month=1, day=13,
        label='Haman’s decree', story='esther',
        when='the twelfth year of King Ahasuerus (Esther 3:7)',
        card=Card(('Esther 3:12-13',), ('Then the king’s scribes were called in on the first month, on the thirteenth day of the month', 'to destroy, to kill, and to cause to perish, all Jews', 'in one day, even on the thirteenth day of the twelfth month, which is the month Adar'))),
    Event(
        key='mordecais_decree', ref='Esther 8:9', month=3, day=23,
        label='Mordecai’s decree', story='esther',
        when='the twelfth year of King Ahasuerus (carried from Esther 3:7)',
        doubt='No year is restated; it falls between the first-month decree and the twelfth-month day of the same year.',
        card=Card(('Esther 8:9',), ('Then the king’s scribes were called at that time, in the third month, which is the month Sivan, on the twenty-third day of the month; and it was written according to all that Mordecai commanded',))),
    Event(
        key='jews_prevail', ref='Esther 9:1', month=12, day=13,
        label='Jews prevail', story='esther',
        when='the twelfth year of King Ahasuerus (the day set in Esther 3:13)',
        also=('Esther 3:13', 'Esther 8:12', 'Esther 9:17'),
        card=Card(('Esther 9:1', 'Esther 3:13', 'Esther 8:12', 'Esther 9:17'), ('Now in the twelfth month, which is the month Adar, on the thirteenth day of the month', 'it was turned out the opposite happened, that the Jews conquered those who hated them'))),
    Event(
        key='shushan_second_day', ref='Esther 9:15', month=12, day=14,
        label='Shushan’s second day', story='esther',
        when='the same year',
        card=Card(('Esther 9:15',), ('The Jews who were in Shushan gathered themselves together on the fourteenth day also of the month Adar, and killed three hundred men in Shushan; but they didn’t lay their hand on the plunder.',))),
    Event(
        key='provinces_rest', ref='Esther 9:17', month=12, day=14,
        label='provinces rest', story='esther',
        when='the same year',
        card=Card(('Esther 9:17',), ('This was done on the thirteenth day of the month Adar; and on the fourteenth day of that month they rested and made it a day of feasting and gladness.',))),
    Event(
        key='shushan_rests', ref='Esther 9:18', month=12, day=15,
        month_from='context',
        label='Shushan rests', story='esther',
        when='the same year',
        doubt='‘that month’ is Adar, named in Esther 9:15 and 9:17.',
        card=Card(('Esther 9:18',), ('the Jews who were in Shushan assembled together on the thirteenth and on the fourteenth days of the month; and on the fifteenth day of that month, they rested, and made it a day of feasting and gladness.',))),
    Event(
        key='purim_enjoined', ref='Esther 9:20-21', month=12, day=14,
        label='Purim enjoined', story='esther',
        when='the same year; kept ‘yearly’ after',
        day_end=15, also=('Esther 9:19', 'Esther 9:22'),
        doubt='Mordecai’s letter sets the feast of Purim, the 14th and 15th of Adar.',
        card=Card(('Esther 9:20-21', 'Esther 9:19', 'Esther 9:22'), ('Mordecai wrote these things, and sent letters to all the Jews', 'to enjoin them that they should keep the fourteenth and fifteenth days of the month Adar yearly'))),
)

JOHN = (
    Mention('John 2:13', 'passover', 'Passover (1)', 'The Passover of the Jews was at hand, and Jesus went up to Jerusalem.'),
    Mention('John 2:23', 'passover', 'Passover (1)', 'Now when he was in Jerusalem at the Passover, during the feast, many believed in his name, observing his signs which he did.'),
    Mention('John 4:45', 'passover', 'at the feast', 'the Galileans received him, having seen all the things that he did in Jerusalem at the feast'),
    Mention('John 5:1', None, 'a feast', 'After these things, there was a feast of the Jews, and Jesus went up to Jerusalem.'),
    Mention('John 6:4', 'passover', 'Passover (2)', 'Now the Passover, the feast of the Jews, was at hand.'),
    Mention('John 7:2', 'tents', 'Feast of Booths', 'Now the feast of the Jews, the Feast of Booths, was at hand.'),
    Mention('John 7:10', 'tents', 'up in secret', 'But when his brothers had gone up to the feast, then he also went up, not publicly, but as it were in secret.'),
    Mention('John 7:14', 'tents', 'middle of feast', 'But when it was now the middle of the feast, Jesus went up into the temple and taught.'),
    Mention('John 7:37', 'tents', 'last great day', 'Now on the last and greatest day of the feast, Jesus stood and cried out, “If anyone is thirsty, let him come to me and drink!'),
    Mention('John 10:22-23', 'dedication', 'Feast of Dedication', 'It was the Feast of the Dedication at Jerusalem. It was winter, and Jesus was walking in the temple, in Solomon’s porch.'),
    Mention('John 11:55', 'passover', 'Passover (3)', 'Now the Passover of the Jews was at hand. Many went up from the country to Jerusalem before the Passover, to purify themselves.'),
    Mention('John 12:1', 'passover', 'six days before', 'Then six days before the Passover, Jesus came to Bethany, where Lazarus was, who had been dead, whom he raised from the dead.'),
    Mention('John 12:12', 'passover', 'come to the feast', 'On the next day a great multitude had come to the feast.'),
    Mention('John 12:20', 'passover', 'Greeks at the feast', 'Now there were certain Greeks among those that went up to worship at the feast.'),
    Mention('John 13:1', 'passover', 'before the feast', 'Now before the feast of the Passover, Jesus, knowing that his time had come that he would depart from this world to the Father'),
    Mention('John 18:28', 'passover', 'Praetorium', 'It was early, and they themselves didn’t enter into the Praetorium, that they might not be defiled, but might eat the Passover.'),
    Mention('John 18:39', 'passover', 'release at the Passover', 'But you have a custom, that I should release someone to you at the Passover.'),
    Mention('John 19:14', 'passover', 'Preparation Day', 'Now it was the Preparation Day of the Passover, at about the sixth hour. He said to the Jews, “Behold, your King!”'),
    Mention('John 19:31', 'passover', 'special Sabbath', 'so that the bodies wouldn’t remain on the cross on the Sabbath (for that Sabbath was a special one)'),
)

ACTS = (
    Mention('Acts 2:1', 'weeks', 'Pentecost', 'Now when the day of Pentecost had come, they were all with one accord in one place.'),
    Mention('Acts 12:3-4', 'unleavened_bread', 'Peter arrested', 'This was during the days of unleavened bread. … intending to bring him out to the people after the Passover.'),
    Mention('Acts 18:21', None, 'this coming feast', 'I must by all means keep this coming feast in Jerusalem'),
    Mention('Acts 20:6', 'unleavened_bread', 'sail from Philippi', 'We sailed away from Philippi after the days of Unleavened Bread, and came to them at Troas in five days, where we stayed seven days.'),
    Mention('Acts 20:16', 'weeks', 'hastening to Pentecost', 'he was hastening, if it were possible for him, to be in Jerusalem on the day of Pentecost.'),
    Mention('Acts 27:9', 'atonement', 'the Fast past', 'When much time had passed and the voyage was now dangerous, because the Fast had now already gone by, Paul admonished them'),
)


# Every day, under every feast (Numbers 28:3-8): what the feasts' offerings
# are "besides".
DAILY = Feast(
    key='daily', name='continual burnt offering', aka=('continually',),
    month=None, day=None, days=1, every='every day',
    rest=Note('No rest is set.', ()),
    offerings=Offerings(0, 0, 2, 0),
    offerings_note=Note('Two male lambs a year old, one in the morning and one at evening, '
                        'with their meal and drink offerings.', ('Num 28:3-8', 'Exod 29:38-42')),
    farming=Note('None.', ()),
    refs=('Exod 29:38-42', 'Num 28:3-8'),
    card=Card(('Num 28:3-4', 'Num 28:6'),
              ('male lambs a year old without defect, two day by day, for a continual burnt offering',
               'You shall offer the one lamb in the morning, and you shall offer the other lamb at evening',
               'It is a continual burnt offering, which was ordained in Mount Sinai')))

# The three pilgrim feasts, as the Law lists them.
THREE_TIMES = Note(
    'Three times a year every male appears before Yahweh: at the feast of unleavened bread, '
    'the feast of weeks and the feast of tents. Exodus 23 calls the last two the feast of '
    'harvest and the feast of ingathering.',
    ('Deut 16:16', 'Exod 23:14-17', 'Exod 34:23', '2 Chr 8:13'))
THREE_TIMES_CARD = Card(
    ('Deut 16:16',),
    ('Three times in a year all of your males shall appear before Yahweh your God in the place '
     'which he chooses: in the feast of unleavened bread, in the feast of weeks, and in the '
     'feast of tents',))

# David's twelve divisions of 24,000, one for each month (1 Chronicles
# 27:1-15): the month, its captain, and the verse that names him.
DIVISIONS = (
    (1, 'Jashobeam', '1 Chr 27:2'), (2, 'Dodai', '1 Chr 27:4'), (3, 'Benaiah', '1 Chr 27:5'),
    (4, 'Asahel', '1 Chr 27:7'), (5, 'Shamhuth', '1 Chr 27:8'), (6, 'Ira', '1 Chr 27:9'),
    (7, 'Helez', '1 Chr 27:10'), (8, 'Sibbecai', '1 Chr 27:11'), (9, 'Abiezer', '1 Chr 27:12'),
    (10, 'Maharai', '1 Chr 27:13'), (11, 'Benaiah', '1 Chr 27:14'), (12, 'Heldai', '1 Chr 27:15'),
)

YEARS = (
    Year(
        key='sabbath_year', name='the year of release',
        aka=('the seventh year', 'a Sabbath of solemn rest for the land', 'the Sabbath of the land'),
        aka_refs=(('the year of release', 'Deut 15:9'),
                  ('a Sabbath of solemn rest for the land', 'Lev 25:4'),
                  ('the Sabbath of the land', 'Lev 25:6')),
        every=7,
        refs=('Exod 23:10-11', 'Lev 25:1-7', 'Lev 25:20-22', 'Deut 15:1-11', 'Deut 31:10-13',
              'Neh 10:31', 'Lev 26:34-35', 'Lev 26:43', '2 Chr 36:21'),
        rules=(
            Rule('The land rests', 'Sow and prune six years; in the seventh the land rests: no sowing, pruning, reaping or grape gathering.', ('Lev 25:3-5', 'Exod 23:10-11')),
            Rule('Its food', 'What grows of itself is food for you, your servants, the foreigner, the poor, livestock and wild animals.', ('Lev 25:6-7', 'Exod 23:11')),
            Rule('The sixth year', "The sixth year bears for three years; sow in the eighth, eat the old store until the ninth year's harvest.", ('Lev 25:20-22',)),
            Rule('Debts', "At the end of every seven years, cancel debts to a brother; a foreigner's debt may still be required.", ('Deut 15:1-3',)),
            Rule('Lending', "Don't refuse a loan because the year of release is near.", ('Deut 15:9-10',)),
            Rule('The law read', 'Read the law before all Israel at the feast of tents in the year of release.', ('Deut 31:10-13',)),
            Rule('Servants', 'A Hebrew servant serves six years and goes free in the seventh, not empty-handed; one who will not go has his ear bored with an awl.', ('Exod 21:2-6', 'Deut 15:12-18')),
            Rule('Zedekiah', "Zedekiah's covenant freed Hebrew servants, then took them back; Yahweh proclaimed a liberty to the sword.", ('Jer 34:8-17',)),
            Rule('Unkept', 'If Israel will not keep it, the land will enjoy its Sabbaths while it lies desolate; the exile kept them, to fulfill seventy years.', ('Lev 26:34-35,43', '2 Chr 36:21')),
        ),
        card=Card(('Lev 25:4', 'Deut 15:1', '2 Chr 36:21'),
                  ('in the seventh year there shall be a Sabbath of solemn rest for the land, a Sabbath to Yahweh',
                   'At the end of every seven years, you shall cancel debts',
                   'As long as it lay desolate, it kept Sabbath, to fulfill seventy years'))),
    Year(
        key='jubilee', name='Year of Jubilee',
        aka=('jubilee', 'the fiftieth year', 'year of liberty'),
        aka_refs=(('Year of Jubilee', 'Lev 25:13'), ('jubilee', 'Lev 25:10'),
                  ('the fiftieth year', 'Lev 25:10'), ('year of liberty', 'Ezek 46:17')),
        every=50,
        refs=('Lev 25:8-55', 'Lev 27:16-24', 'Num 36:4', 'Ezek 46:17'),
        rules=(
            Rule('Counted', 'Count seven Sabbaths of years, seven times seven years, forty-nine years.', ('Lev 25:8',)),
            Rule('The trumpet', 'Sound the loud trumpet on the tenth day of the seventh month, the Day of Atonement, throughout all the land.', ('Lev 25:9',)),
            Rule('Liberty', 'Make the fiftieth year holy and proclaim liberty throughout the land; each returns to his property and his family.', ('Lev 25:10,13',)),
            Rule('The land rests', 'No sowing, no reaping what grows of itself, no gathering from undressed vines; eat from the field.', ('Lev 25:11-12',)),
            Rule('Land prices', "Land is priced by the number of crops to the Jubilee; the land is Yahweh's and is not sold in perpetuity.", ('Lev 25:14-17,23',)),
            Rule('Redeeming land', 'A kinsman may redeem sold land, or the seller himself; if not, it is released in the Jubilee.', ('Lev 25:24-28',)),
            Rule('Houses', "A house in a walled city may be redeemed only within a year and is not released; village houses and Levites' houses are released.", ('Lev 25:29-34',)),
            Rule('The poor', 'A poor brother who sells himself serves as a hired servant until the Jubilee, then returns with his children.', ('Lev 25:39-41,54',)),
            Rule('Sold to a foreigner', 'One sold to a foreigner may be redeemed, his price reckoned by the years left to the Jubilee.', ('Lev 25:47-53',)),
            Rule('Dedicated fields', "A dedicated field is valued by the years to the Jubilee; unredeemed, it becomes the priests' in the Jubilee; a bought field returns to its owner.", ('Lev 27:16-24',)),
            Rule('Inheritance', "In the jubilee a daughter's inheritance would stay with the tribe she married into.", ('Num 36:4',)),
        ),
        card=Card(('Lev 25:10', 'Lev 25:23'),
                  ('You shall make the fiftieth year holy, and proclaim liberty throughout the land to all its inhabitants',
                   'each of you shall return to his own property, and each of you shall return to his family',
                   'The land shall not be sold in perpetuity, for the land is mine')),
        trumpet=(7, 10, 'Lev 25:9',
                 Card(('Lev 25:9',),
                      ('Then you shall sound the loud trumpet on the tenth day of the seventh month',
                       'On the Day of Atonement you shall sound the trumpet throughout all your land')))),
)

# Where each feast's day is set, and the words that set it (the tests read
# them in WEB): the month and day on FEASTS are these verses'.
DEFINED = {
    'sabbath': ('Lev 23:3', ('seventh day',)),
    'new_moon': ('Num 28:11', ('beginnings of your months',)),
    'passover': ('Lev 23:5', ('first month', 'fourteenth day')),
    'unleavened_bread': ('Lev 23:6', ('fifteenth day of the same month', 'seven days')),
    'first_fruits_sheaf': ('Lev 23:11', ('next day after the Sabbath',)),
    'weeks': ('Lev 23:15-16', ('seven Sabbaths', 'fifty days')),
    'trumpets': ('Lev 23:24', ('seventh month', 'first day')),
    'atonement': ('Lev 23:27', ('tenth day of this seventh month',)),
    'tents': ('Lev 23:34', ('fifteenth day of this seventh month', 'seven days')),
    'eighth_day': ('Lev 23:36', ('eighth day',)),
    'second_passover': ('Num 9:11', ('second month', 'fourteenth day')),
    'purim': ('Esth 9:21', ('fourteenth and fifteenth days of the month Adar',)),
    'dedication': ('John 10:22-23', ('Feast of the Dedication', 'winter')),
    'daily': ('Num 28:3', ('two day by day',)),
}

MONTH = {m.n: m for m in MONTHS}
FEAST = {f.key: f for f in FEASTS + (DAILY,)}
FARM = {f.key: f for f in FARMING}
EVENT = {e.key: e for e in DATED_EVENTS}
YEAR = {y.key: y for y in YEARS}


def month_names(n):
    """'Abib · Nisan', or '' for the fourth and fifth months."""
    return " · ".join(nm.name for nm in MONTH[n].names)
