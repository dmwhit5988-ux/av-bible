"""The Sacred year reference page: a dial of the year, with WEB's months,
the farming year, the set feasts of Leviticus 23 and Numbers 28-29 and the
days the text dates to a month, and the Sabbath years and the Jubilee beside
it.

Writes web/visuals/reference/Sacred_year.svg, its sidecar Sacred_year.json
and the viewer page Sacred_year.html (reference_viewer.page). The web app's
Reference list opens it (web/js/app.js REFERENCES). The data is
sacred_calendar.py.

The sheet is two views (the sidecar's `views`), and the page opens on the
first:

- **Year**, the dial. Month 1 (Abib) is at the top and the year runs
  clockwise, twelve equal months of thirty days: a schematic, since the
  months are lunar (the "about the dial" card says so). From the rim in:
  - **Dated days** (a layer, on): a dot for each day the text dates, in its
    story's colour, filled where the text gives the day and hollow near the
    month's middle (clear of the dated days) where it gives only the month;
    dots of one kind on one day stack outward. Each has its label on a spoke
    beyond, shown as you zoom in (<g data-fs>); where Kings and Jeremiah
    differ the label gives both days ("7 or 10").
  - **The months**: the number, WEB's names (curved) and "about Mar-Apr".
  - The days, a tick each, every fifth longer.
  - **Feasts** (a layer, on): each set feast as an arc over its days or a
    dot on its day, gold for the three pilgrim feasts, the counted feast of
    weeks and the sheaf dashed, the second Passover and Purim subdued as
    later additions, and the new moon a ring on the 1st of every month.
  - **John's feasts** (a layer, off): John 2:13, 6:4 and 11:55 by the
    Passover, 7:2 by the feast of tents, and 10:22's Dedication over the
    winter months; John 5:1's unnamed feast stands apart, in "Not on the
    dial" beside the key, with Ezekiel 26:1 and 32:17 (a day, no month),
    Ezekiel 40:1 ("the beginning of the year") and the seasons the text
    never dates.
  - **Farming** (a layer, on): the farming year in lanes, solid where the
    text ties it to a month or a feast, faded and dashed where it names only
    the season.
  - The centre: the Sabbath, the three times a year, and the daily lambs.
- **Jubilee**, to the right: seven rows of seven years, each seventh a
  Sabbath for the land, and the fiftieth, the Jubilee, proclaimed with the
  trumpet on the Day of Atonement (a small dial marks the day).

Every mark is a part with a card: its date and verses, the Numbers 28-29
offerings day by day, the rest, the farming, WEB's own words, and what the
text leaves open. Tours (`tours`) walk the year: the flood year, Egypt to the
Jordan, Leviticus 23 in order, Jerusalem falls, the return, Ezra and
Nehemiah, and Esther.

    .venv\\Scripts\\python.exe generate_sacred_year_reference.py
"""

import json
import math
import os

import reference_viewer
import sacred_calendar as SC
import verse_refs
from books import BOOK_NAMES
from config import VISUALS_DIR
from generate_tabernacle import BG, GOLD, PANEL, SAND, SAND_DIM, TEXT, TEXT_DIM
from sacred_calendar import day_of_year, ordinal
from svg_map_camera import ink
from svg_surface import SvgCanvas, _fmt, _rgb

OUT_DIR = os.path.join(VISUALS_DIR, "reference")
STEM = "Sacred_year"
TITLE = "The sacred year"

# -- the sheet -----------------------------------------------------------------
CX, CY = 1430, 1610                 # the dial's centre
R_EV = 1052                         # the first dated-day dot
EV_STEP = 17                        # between dots stacked on one day
EV_DOT = 7
R_EVL = 1192                        # where a day's label starts
EV_FS = 18
R_MON = (826, 1032)                 # the month ring
R_TICK = (796, 826)                 # the day ticks
R_FEAST = (728, 772)                # the feasts' arcs
R_MOON = 710                        # the new moons
R_SHEAF = 714
R_JOHN = 474                        # John's feasts
LANES = (290, 334, 378, 422)        # the farming lanes' middles, inside out
LANE_W = 36
R_CENTRE = 250

COL_X = 2880                        # the right-hand column
COL_W = 1000
W, H = COL_X + COL_W + 60, 3040

# -- colours -------------------------------------------------------------------
PILGRIM = GOLD
SET_DAY = (226, 120, 100)
SET_TEXT = (246, 176, 156)
LATER = (156, 144, 196)
LATER_TEXT = (196, 186, 228)
MOON = (190, 194, 206)
JOHN_COL = (150, 206, 240)
NAME_COL = (246, 236, 206)
RING_A, RING_B = (30, 30, 44), (38, 36, 52)

FARM_KIND = {"latter_rain": "rain", "former_rain": "rain", "great_rain": "rain",
             "jordan_flood": "water", "barley_harvest": "grain", "wheat_harvest": "grain",
             "grain_count": "grain", "first_ripe_grapes": "fruit", "summer_fruit": "fruit",
             "ingathering": "fruit", "plowing_sowing": "soil", "winter_house": "winter",
             "dry_harvest": "grain", "spring_figs_vines": "fruit"}
FARM_COL = {"rain": (92, 156, 228), "water": (70, 186, 190), "grain": (206, 178, 92),
            "fruit": (186, 104, 168), "soil": (176, 124, 78), "winter": (164, 182, 210)}
FARM_LANE = {"latter_rain": 3, "former_rain": 3, "barley_harvest": 2, "first_ripe_grapes": 2,
             "ingathering": 2, "plowing_sowing": 2, "jordan_flood": 1, "wheat_harvest": 1,
             "summer_fruit": 1, "winter_house": 1, "grain_count": 0, "great_rain": 0}
# the labels on the farming lanes, in the text's words where they are short
FARM_LABEL = {"latter_rain": "latter rain", "former_rain": "former rain",
              "barley_harvest": "barley harvest", "wheat_harvest": "wheat harvest",
              "grain_count": "7 weeks · 50 days", "first_ripe_grapes": "first-ripe grapes",
              "summer_fruit": "summer fruits", "ingathering": "ingathering",
              "plowing_sowing": "plowing, sowing", "jordan_flood": "Jordan",
              "winter_house": "winter", "great_rain": "great rain"}

# the story groups, as the rim colours them (Solomon's temple with the kings)
STORY_COL = {"flood": (110, 172, 244), "exodus": (240, 160, 70), "temple": (186, 142, 236),
             "kings": (186, 142, 236), "fall": (238, 92, 92), "ezekiel": (72, 204, 190),
             "other": (206, 206, 216), "return": (130, 206, 92), "nehemiah": (214, 232, 120),
             "esther": (244, 132, 196)}
LEGEND_STORIES = (("flood", "The flood"), ("exodus", "Egypt to the Jordan"),
                  ("kings", "The kings and the temple"), ("fall", "Jerusalem falls"),
                  ("ezekiel", "Ezekiel"), ("other", "Daniel"), ("return", "The return"),
                  ("nehemiah", "Nehemiah"), ("esther", "Esther"))

# the feasts on the dial: their names as drawn (a line each), the date line
# under, and where the label's block is centred (px from the dial's centre)
FEAST_DRAWN = {
    "passover": (("Passover",), "14th", (64, -640)),
    "unleavened_bread": (("unleavened", "bread"), "15th–21st", (300, -528)),
    "first_fruits_sheaf": (("the sheaf",), "after a Sabbath", (104, -530)),
    "second_passover": (("Passover",), "2nd month, 14th", (474, -430)),
    "weeks": (("feast of", "weeks"), "counted: 50 days", (566, -246)),
    "trumpets": (("blowing of", "trumpets"), "1st", (172, 626)),
    "atonement": (("Day of", "Atonement"), "10th", (-54, 590)),
    "tents": (("feast of", "tents"), "15th–21st", (-244, 562)),
    "eighth_day": (("eighth", "day"), "22nd", (-440, 440)),
    "purim": (("Purim",), "14th–15th", (-200, -612)),
    "new_moon": (("new moon",), "the 1st of every month", (470, 300)),
}
FEAST_FS, FEAST_SUB = 36, 24
FARM_FS = 26
MON_NUM, MON_NAME, MON_MOD = 72, 50, 26

TOURS = (
    ("flood", "The flood year",
     ["flood_begins", "ark_rests", "mountains_seen", "waters_dried", "earth_dry"]),
    ("exodus", "Egypt to the Jordan",
     ["passover_egypt", "leave_rameses", "wilderness_of_sin", "reach_sinai", "tabernacle_raised",
      "sinai_passover", "census_ordered", "leave_sinai", "miriam_dies", "aaron_dies",
      "moses_speaks", "cross_jordan", "gilgal_passover", "manna_ceases"]),
    ("lev23", "Leviticus 23", None),
    ("fall", "Jerusalem falls",
     ["siege_begins", "ezekiel_24", "wall_breached", "temple_burned", "gedaliah_killed",
      "city_fallen_news", "jehoiachin_released"]),
    ("return", "The return",
     ["altar_offerings", "temple_work_begins", "haggai_first", "work_resumes", "latter_glory",
      "zechariah_call", "from_today_bless", "zerubbabel_signet", "zechariah_night_visions",
      "zechariah_fasting", "second_temple_finished", "exiles_passover"]),
    ("ezra", "Ezra and Nehemiah",
     ["ezra_sets_out", "leave_ahava", "ezra_arrives", "assembly_in_rain", "inquiry_begins",
      "inquiry_ends", "news_from_jerusalem", "before_the_king", "wall_finished", "law_read",
      "law_studied", "booths_kept", "fast_and_confession"]),
    ("esther", "Esther",
     ["esther_to_king", "pur_cast", "hamans_decree", "mordecais_decree", "jews_prevail",
      "shushan_second_day", "provinces_rest", "shushan_rests", "purim_enjoined"]),
)
# Leviticus 23 in its own order, each stop with the verses that set it
LEV23 = (("sabbath", "Lev 23:3"), ("passover", "Lev 23:4-5"), ("unleavened_bread", "Lev 23:6-8"),
         ("first_fruits_sheaf", "Lev 23:9-14"), ("weeks", "Lev 23:15-22"),
         ("trumpets", "Lev 23:23-25"), ("atonement", "Lev 23:26-32"),
         ("tents", "Lev 23:33-36, 39-43"), ("eighth_day", "Lev 23:36, 39"))

# The day each feast's card gives, in words, with its flag
WHEN = {
    "sabbath": ("every seventh day", "stated"),
    "new_moon": ("the 1st of every month", "stated"),
    "daily": ("every day, morning and evening", "stated"),
    "passover": ("1st month, 14th day, at evening", "stated"),
    "unleavened_bread": ("1st month, 15th to 21st day", "stated"),
    "first_fruits_sheaf": ("the day after the Sabbath, in the days of unleavened bread",
                           "not given"),
    "weeks": ("fifty days counted from the sheaf: early in the 3rd month", "counted"),
    "trumpets": ("7th month, 1st day", "stated"),
    "atonement": ("7th month, 10th day, from the 9th at evening", "stated"),
    "tents": ("7th month, 15th to 21st day", "stated"),
    "eighth_day": ("7th month, the eighth day of the feast: the 22nd", "stated"),
    "second_passover": ("2nd month, 14th day, at evening", "stated"),
    "purim": ("12th month (Adar), 14th and 15th days", "stated"),
    "dedication": ("winter; no month or day given", "not given"),
}


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------

def ang(month, day):
    """Degrees clockwise from the top for the middle of a day."""
    return day_of_year(month, day) + 0.5


def mid(month):
    """The middle of a month, where a day the text doesn't give is set."""
    return (month - 1) * 30 + 15


def al(col, f):
    """A colour at opacity f."""
    return tuple(col[:3]) + (round(f * 255),)


def pt(r, a):
    t = math.radians(a)
    return (CX + r * math.sin(t), CY - r * math.cos(t))


def P(xy):
    return f"{_fmt(round(xy[0], 1))},{_fmt(round(xy[1], 1))}"


def sector(r0, r1, a0, a1):
    """An annular sector's path, a0 to a1 clockwise."""
    big = 1 if a1 - a0 > 180 else 0
    return (f"M{P(pt(r1, a0))}A{_fmt(r1)},{_fmt(r1)} 0 {big} 1 {P(pt(r1, a1))}"
            f"L{P(pt(r0, a1))}A{_fmt(r0)},{_fmt(r0)} 0 {big} 0 {P(pt(r0, a0))}Z")


def arc(r, a0, a1):
    big = 1 if a1 - a0 > 180 else 0
    return f"M{P(pt(r, a0))}A{_fmt(r)},{_fmt(r)} 0 {big} 1 {P(pt(r, a1))}"


def upright(a):
    """Does text along the ring at a read clockwise (the top half)?"""
    a %= 360
    return a < 90 or a > 270


def ring_boxes(r0, r1, a0, a1, step=6.0):
    """Boxes [x, y, w, h] along a ring sector, for taps."""
    n = max(1, math.ceil((a1 - a0) / step))
    out = []
    for i in range(n):
        b0, b1 = a0 + (a1 - a0) * i / n, a0 + (a1 - a0) * (i + 1) / n
        pts = [pt(r, b) for r in (r0, r1) for b in (b0, (b0 + b1) / 2, b1)]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        out.append(bx((min(xs), min(ys), max(xs), max(ys))))
    return out


def bx(b, pad=0):
    """(x0, y0, x1, y1) -> [x, y, w, h], rounded."""
    return [round(b[0] - pad, 1), round(b[1] - pad, 1),
            round(b[2] - b[0] + 2 * pad, 1), round(b[3] - b[1] + 2 * pad, 1)]


def union(bs):
    """[x, y, w, h] boxes -> their union."""
    x0 = min(b[0] for b in bs)
    y0 = min(b[1] for b in bs)
    x1 = max(b[0] + b[2] for b in bs)
    y1 = max(b[1] + b[3] for b in bs)
    return [round(x0, 1), round(y0, 1), round(x1 - x0, 1), round(y1 - y0, 1)]


def frame(b, least=560):
    """A box grown to at least `least` px each way, for the camera."""
    x, y, w, h = b
    gw, gh = max(w, least), max(h, least)
    # kept on the sheet: shifted, never shrunk
    fx = min(max(x - (gw - w) / 2, 0), max(W - gw, 0))
    fy = min(max(y - (gh - h) / 2, 0), max(H - gh, 0))
    return [round(fx, 1), round(fy, 1), round(gw, 1), round(gh, 1)]


# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def width(s, size, bold=False, italic=False):
    x0, _y0, x1, _y1 = ink(s, size, bold, italic, "lm")
    return x1 - x0


def text(c, xy, s, size, fill, anchor="mm", bold=False, italic=False, rotate=None,
         halo=None):
    ta = {"l": "start", "m": "middle", "r": "end"}[anchor[0]]
    db = {"a": "text-before-edge", "m": "central", "d": "text-after-edge",
          "s": "alphabetic"}[anchor[1]]
    a = [f'x="{_fmt(round(xy[0], 1))}"', f'y="{_fmt(round(xy[1], 1))}"',
         f'font-size="{_fmt(size)}"',
         f'text-anchor="{ta}"', f'dominant-baseline="{db}"', f'fill="{_rgb(fill)}"']
    if bold:
        a.append('font-weight="bold"')
    if italic:
        a.append('font-style="italic"')
    if rotate is not None:
        a.append(f'transform="rotate({_fmt(round(rotate, 2))} {_fmt(round(xy[0], 1))} '
                 f'{_fmt(round(xy[1], 1))})"')
    if halo:
        a.append(f'stroke="{_rgb(halo)}" stroke-width="{_fmt(max(3, size / 6))}" '
                 f'stroke-linejoin="round" paint-order="stroke"')
    c._emit(f"<text {' '.join(a)}>{esc(s)}</text>")


_PATHS = []


def curved(c, r, a0, a1, s, size, fill, bold=False, italic=False, halo=None):
    """Text centred along the ring at r between a0 and a1, upright: clockwise
    on the top half, against the clock on the bottom. `r` is where the
    text's middle runs."""
    pid = f"sy{len(_PATHS)}"
    am = (a0 + a1) / 2
    if upright(am):
        rb = r - size * 0.34
        d = arc(rb, a0, a1)
    else:
        rb = r + size * 0.34
        big = 1 if a1 - a0 > 180 else 0
        d = f"M{P(pt(rb, a1))}A{_fmt(rb)},{_fmt(rb)} 0 {big} 0 {P(pt(rb, a0))}"
    _PATHS.append(f'<path id="{pid}" d="{d}"/>')
    a = [f'font-size="{_fmt(size)}"', f'fill="{_rgb(fill)}"']
    if bold:
        a.append('font-weight="bold"')
    if italic:
        a.append('font-style="italic"')
    if halo:
        a.append(f'stroke="{_rgb(halo)}" stroke-width="{_fmt(max(3, size / 6))}" '
                 f'stroke-linejoin="round" paint-order="stroke"')
    c._emit(f"<text {' '.join(a)}><textPath xlink:href=\"#{pid}\" startOffset=\"50%\" "
            f"text-anchor=\"middle\">{esc(s)}</textPath></text>")


def spoke(c, r, a, s, size, fill, bold=False):
    """Text along the spoke at angle a from radius r outward, never upside
    down. -> boxes [x, y, w, h] along it, for taps."""
    w = width(s, size, bold)
    if (a % 360) < 180:
        text(c, pt(r, a), s, size, fill, "lm", bold=bold, rotate=a - 90)
    else:
        text(c, pt(r, a), s, size, fill, "rm", bold=bold, rotate=a - 270)
    out, n = [], max(1, math.ceil(w / size))
    for i in range(n):
        x, y = pt(r + (i + 0.5) * w / n, a)
        out.append([round(x - size * 0.7, 1), round(y - size * 0.7, 1),
                    round(size * 1.4, 1), round(size * 1.4, 1)])
    return out, r + w


# ---------------------------------------------------------------------------
# The verses
# ---------------------------------------------------------------------------

def rows(*refs):
    """Ref strings -> rows [book index, c1, v1, c2, v2] (0 = none)."""
    out = []
    for ref in refs:
        if not ref:
            continue
        for r in verse_refs.parse(ref, None):
            out.append([BOOK_NAMES.index(r.book), r.c1, r.v1 or 0, r.c2 or 0, r.v2 or 0])
    return out


def nth_month(n):
    return f"{ordinal(n)} month"


# ---------------------------------------------------------------------------
# The dial
# ---------------------------------------------------------------------------

def draw_months(c):
    """The month ring, the day ticks, and each month's boxes for taps."""
    boxes = {}
    for m in SC.MONTHS:
        a0, a1 = (m.n - 1) * 30, m.n * 30
        c.path(sector(*R_MON, a0, a1), fill=RING_A if m.n % 2 else RING_B, stroke=SAND_DIM,
               width=2)
        boxes[m.n] = ring_boxes(R_MON[0], R_MON[1], a0, a1, 7.5)
    # the days: a tick each, every fifth longer
    for d in range(360):
        a = d
        five = (d % 30) % 5 == 0 and d % 30
        r0 = R_TICK[0] if d % 30 == 0 else (R_TICK[0] + 10 if five else R_TICK[0] + 20)
        col = SAND if d % 30 == 0 or five else SAND_DIM
        c.line(pt(r0, a), pt(R_TICK[1], a), col, 2.5 if d % 30 == 0 else 1.5)
    c.circle(CX, CY, R_TICK[1], stroke=SAND_DIM, width=1.5)
    with c.group(data={"fs": 16}):
        for m in range(1, 13):
            for d in (5, 10, 15, 20, 25):
                a = (m - 1) * 30 + d - 1           # the tick before the day
                text(c, pt(R_TICK[0] - 11, a), str(d), 16, TEXT_DIM, "mm")
    for m in SC.MONTHS:
        a0, a1 = (m.n - 1) * 30, m.n * 30
        am = (a0 + a1) / 2
        # between the names (outside) and "about" (inside), wherever it stands
        text(c, pt(920, am), str(m.n), MON_NUM, TEXT, "mm", bold=True)
    with c.group(data={"fs": MON_NAME}):
        for m in SC.MONTHS:
            names = SC.month_names(m.n)
            if names:
                a0, a1 = (m.n - 1) * 30, m.n * 30
                curved(c, R_MON[1] - 38, a0 + 1, a1 - 1, names, MON_NAME, NAME_COL, bold=True)
    with c.group(data={"fs": MON_MOD}):
        for m in SC.MONTHS:
            a0, a1 = (m.n - 1) * 30, m.n * 30
            lo, hi = m.modern
            curved(c, R_MON[0] + 26, a0 + 1, a1 - 1, f"about {lo[:3]}–{hi[:3]}", MON_MOD,
                   TEXT_DIM, italic=True)
    return boxes


def draw_feasts(c):
    """The feasts' marks and labels -> {key: [boxes]} and label boxes."""
    marks, labels = {}, {}
    F = SC.FEAST
    r0, r1 = R_FEAST
    rm = (r0 + r1) / 2

    def span(key, col, dashed=False, fill_op=0.92):
        f = F[key]
        a0 = day_of_year(f.month, f.day)
        a1 = a0 + f.days
        if dashed:
            c.path(sector(r0, r1, a0, a1), fill=al(col, 0.22), stroke=col, width=3)
            c._els[-1] = c._els[-1].replace("/>", ' stroke-dasharray="10 7"/>')
        else:
            c.path(sector(r0, r1, a0, a1), fill=al(col, fill_op), stroke=BG, width=2)
        marks[key] = ring_boxes(r0 - 4, r1 + 4, a0, a1, 4)

    def dot(key, col, a=None, rr=16, dashed=False):
        f = F[key]
        a = ang(f.month, f.day) if a is None else a
        x, y = pt(rm, a)
        if dashed:
            c.circle(x, y, rr, fill=al(col, 0.3), stroke=col, width=3)
            c._els[-1] = c._els[-1].replace("/>", ' stroke-dasharray="6 5"/>')
        else:
            c.circle(x, y, rr, fill=col, stroke=BG, width=3)
        marks[key] = [bx((x - rr, y - rr, x + rr, y + rr), 6)]

    span("unleavened_bread", PILGRIM)
    span("tents", PILGRIM)
    # weeks: counted, not dated: a hollow, dashed arc early in the third month
    f = F["weeks"]
    a0, a1 = 62, 69
    c.path(sector(r0, r1, a0, a1), fill=al(PILGRIM, 0.25), stroke=PILGRIM, width=3)
    c._els[-1] = c._els[-1].replace("/>", ' stroke-dasharray="10 7"/>')
    marks["weeks"] = ring_boxes(r0 - 4, r1 + 4, a0, a1, 4)
    dot("passover", SET_DAY)
    dot("trumpets", SET_DAY)
    dot("atonement", SET_DAY)
    dot("eighth_day", SET_DAY)
    dot("second_passover", LATER, dashed=True)
    span("purim", LATER, dashed=True)
    # the sheaf: no fixed day, somewhere in the days of unleavened bread
    a0, a1 = day_of_year(1, 15), day_of_year(1, 21) + 1
    c.path(arc(R_SHEAF, a0 + 0.5, a1 - 0.5), stroke=SET_DAY, width=5)
    c._els[-1] = c._els[-1].replace("/>", ' stroke-dasharray="9 7" stroke-linecap="round"/>')
    marks["first_fruits_sheaf"] = ring_boxes(R_SHEAF - 10, R_SHEAF + 10, a0, a1, 4)
    # the new moon: a ring on the 1st of every month
    mb = []
    for m in range(1, 13):
        x, y = pt(R_MOON, ang(m, 1))
        c.circle(x, y, 8, fill=BG, stroke=MOON, width=3)
        mb.append(bx((x - 8, y - 8, x + 8, y + 8), 6))
    marks["new_moon"] = mb

    return marks


def feast_label_boxes():
    """{key: (x0, y0, x1, y1)} each feast's label block covers."""
    out = {}
    for key, (names, sub, (dx, dy)) in FEAST_DRAWN.items():
        f = SC.FEAST[key]
        lines = [(n, FEAST_FS, f.pilgrim, False) for n in names] + [(sub, FEAST_SUB, False, True)]
        hgt = len(names) * FEAST_FS * 1.08 + FEAST_SUB * 1.15
        wid = max(width(t, fs, b, i) for t, fs, b, i in lines)
        x, y = CX + dx, CY + dy
        out[key] = (x - wid / 2, y - hgt / 2, x + wid / 2, y + hgt / 2)
    return out


def draw_feast_labels(c, marks):
    """Each feast's name (a line or two) and its day, with a leader to its
    mark -> {key: box}."""
    labels = feast_label_boxes()
    keys = list(labels)
    for n, k1 in enumerate(keys):
        for k2 in keys[n + 1:]:
            a, b = labels[k1], labels[k2]
            clear = a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1]
            assert clear, f"the labels of {k1} and {k2} overlap"
    # nor sit on a new moon's ring
    for key, lb in labels.items():
        for m in range(1, 13):
            x, y = pt(R_MOON, ang(m, 1))
            near = lb[0] - 14 < x < lb[2] + 14 and lb[1] - 14 < y < lb[3] + 14
            assert not near, f"the label of {key} covers month {m}'s new moon"
    for key, lb in labels.items():
        if key == "new_moon":
            # to the nearest new moon
            mk = min(marks[key], key=lambda b: (b[0] - lb[0]) ** 2 + (b[1] - lb[1]) ** 2)
        else:
            mk = union(marks[key])
        mx, my = mk[0] + mk[2] / 2, mk[1] + mk[3] / 2
        lx = min(max(mx, lb[0] - 6), lb[2] + 6)
        ly = min(max(my, lb[1] - 6), lb[3] + 6)
        if math.hypot(mx - lx, my - ly) > 24:
            c.line((lx, ly), (mx, my), (128, 122, 104), 1.6)
    with c.group(data={"fs": FEAST_SUB}):
        for key, (names, sub, (dx, dy)) in FEAST_DRAWN.items():
            lb = labels[key]
            text(c, (CX + dx, lb[3] - FEAST_SUB * 0.6), sub, FEAST_SUB, TEXT_DIM, "mm",
                 italic=True)
    with c.group(data={"fs": FEAST_FS}):
        for key, (names, sub, (dx, dy)) in FEAST_DRAWN.items():
            f = SC.FEAST[key]
            col = (PILGRIM if f.pilgrim else LATER_TEXT if f.later else
                   MOON if key == "new_moon" else SET_TEXT)
            lb = labels[key]
            for n, name in enumerate(names):
                text(c, (CX + dx, lb[1] + FEAST_FS * (0.55 + 1.08 * n)), name, FEAST_FS, col,
                     "mm", bold=f.pilgrim)
    return labels


def draw_farming(c):
    """The farming lanes -> {key: [boxes]}."""
    boxes = {}
    for f in SC.FARMING:
        if not f.drawn:
            continue
        lane = FARM_LANE[f.key]
        r = LANES[lane]
        r0, r1 = r - LANE_W / 2, r + LANE_W / 2
        col = FARM_COL[FARM_KIND[f.key]]
        bs = []
        a_lo, a_hi = None, None
        for m0, d0, m1, d1, basis in f.drawn:
            a0 = day_of_year(m0, d0)
            a1 = day_of_year(m1, d1) + 1
            if a1 <= a0:
                a1 += 360
            a_lo = a0 if a_lo is None else a_lo
            a_hi = a1
            if f.key == "great_rain":
                x, y = pt(r, (a0 + a1) / 2)
                c.circle(x, y, 15, fill=col, stroke=BG, width=3)
                bs.append(bx((x - 15, y - 15, x + 15, y + 15), 6))
                continue
            if f.key == "grain_count":
                # the seven weeks counted, with a tick at each week's end
                c.path(arc(r + 12, a0, a1), stroke=col, width=4)
                for w in range(8):
                    aw = a0 + w * (a1 - a0) / 7
                    c.line(pt(r + 4, aw), pt(r + 20, aw), col, 3 if w in (0, 7) else 2)
                bs += ring_boxes(r0, r1, a0, a1, 6)
                continue
            if basis in ("stated", "derived"):
                c.path(sector(r0, r1, a0, a1), fill=al(col, 0.62), stroke=col, width=2)
            else:
                c.path(sector(r0, r1, a0, a1), fill=al(col, 0.2), stroke=col, width=2.5)
                c._els[-1] = c._els[-1].replace("/>", ' stroke-dasharray="9 7"/>')
            bs += ring_boxes(r0, r1, a0, a1, 6)
        boxes[f.key] = (bs, a_lo, a_hi)
    with c.group(data={"fs": FARM_FS}):
        for key, (bs, a0, a1) in boxes.items():
            r = LANES[FARM_LANE[key]]
            label = FARM_LABEL[key]
            if key == "great_rain":
                a0, a1 = a1 + 1, a1 + 34
            elif key == "grain_count":
                # under the line of the count
                curved(c, r - 7, a0, a1, label, 22, (250, 246, 236), halo=BG)
                continue
            curved(c, r, a0, a1, label, FARM_FS, (250, 246, 236), halo=BG)
    return {k: v[0] for k, v in boxes.items()}


def draw_john(c):
    """John's feasts, a chip each, on their own ring -> {ref: box}."""
    boxes = {}

    def chip(a, s, r=R_JOHN):
        x, y = pt(r, a)
        w = width(s, 24, bold=True) + 22
        c.rect(x - w / 2, y - 18, w, 36, fill=(24, 34, 48), stroke=JOHN_COL, width=2.5, rx=18)
        text(c, (x, y + 1), s, 24, JOHN_COL, "mm", bold=True)
        return bx((x - w / 2, y - 18, x + w / 2, y + 18), 4)
    p = ang(1, 14)
    boxes["John 2:13"] = chip(p - 11, "2:13")
    boxes["John 6:4"] = chip(p, "6:4")
    boxes["John 11:55"] = chip(p + 12, "11:55")
    boxes["John 7:2"] = chip(ang(7, 18), "7:2")
    # the Dedication: winter, no month: a dashed arc over the winter months
    c.path(arc(R_JOHN, 246, 324), stroke=JOHN_COL, width=3)
    c._els[-1] = c._els[-1].replace("/>", ' stroke-dasharray="4 9" stroke-linecap="round"/>')
    boxes["John 10:22-23"] = chip(285, "10:22 winter")
    text(c, pt(R_JOHN, ang(1, 14) - 25), "John", 24, JOHN_COL, "mm", italic=True)
    return boxes


def draw_centre(c):
    c.circle(CX, CY, R_CENTRE, fill=PANEL, stroke=SAND_DIM, width=2)
    boxes = {}
    text(c, (CX, CY - 130), "7", 130, TEXT, "mm", bold=True)
    with c.group(data={"fs": 42}):
        text(c, (CX, CY - 44), "Sabbath", 42, NAME_COL, "mm", bold=True)
    with c.group(data={"fs": 22}):
        text(c, (CX, CY - 8), "every seventh day", 22, TEXT_DIM, "mm", italic=True)
    boxes["sabbath"] = bx((CX - 110, CY - 200, CX + 110, CY + 6))
    c.line((CX - 180, CY + 20), (CX + 180, CY + 20), SAND_DIM, 1.5)
    with c.group(data={"fs": 34}):
        text(c, (CX, CY + 60), "3 times a year", 34, PILGRIM, "mm", bold=True)
    with c.group(data={"fs": 22}):
        text(c, (CX, CY + 98), "unleavened bread · weeks · tents", 22, PILGRIM, "mm")
    boxes["three_times"] = bx((CX - 180, CY + 34, CX + 180, CY + 114))
    c.line((CX - 150, CY + 128), (CX + 150, CY + 128), SAND_DIM, 1.5)
    with c.group(data={"fs": 24}):
        text(c, (CX, CY + 164), "every day: 2 lambs", 24, TEXT, "mm")
    boxes["daily"] = bx((CX - 130, CY + 142, CX + 130, CY + 188))
    return boxes


# ---------------------------------------------------------------------------
# The dated days on the rim
# ---------------------------------------------------------------------------

NEAR = 1.0                          # degrees: dots closer than this stack
CLEAR = 1.5                         # degrees: a month-only stack from any dated day


def month_only_angle(m, days):
    """Where a month's month-only dots stand: its middle, or the nearest
    place to it that is clear of the days dated (angles `days`), so the two
    kinds never stack together."""
    centre = mid(m)
    for k in range(0, 41):
        a = centre + (k + 1) // 2 * 0.5 * (1 if k % 2 else -1)
        if not (m - 1) * 30 + 2 <= a <= m * 30 - 2:
            continue
        if all(abs(a - d) >= CLEAR for d in days):
            return a
    return centre


def event_dots():
    """Every dot on the rim: [(angle, event key, filled, labelled)]. A day
    the text doesn't give is set near the month's middle, clear of the
    dated days; David's monthly divisions are on the month cards instead,
    and a day with no month isn't on the dial. Where Kings and Jeremiah give
    different days, the dot is Kings' and the label gives both."""
    dated, out = [], []
    for e in SC.DATED_EVENTS:
        if e.month is None or e.key == "davids_divisions":
            continue
        months = e.months or ((e.month, e.month_end) if e.month_end else (e.month,))
        for i, m in enumerate(months):
            if e.day:
                dated.append(ang(m, e.day))
            out.append((m, e.day, e.key, i == 0))
    return [(ang(m, d) if d else month_only_angle(m, dated), key, bool(d), lab)
            for m, d, key, lab in out]


def stacks(dots):
    """-> ({dot index: level}, {dot index: the top level of its stack}):
    dots of one kind (filled, or month-only) on one day, or near enough to
    touch, stack outward."""
    level = {}

    def same(i, j):
        return dots[i][2] == dots[j][2] and abs(dots[j][0] - dots[i][0]) < NEAR
    for i in sorted(range(len(dots)), key=lambda i: (dots[i][0], i)):
        taken = {level[j] for j in level if same(i, j)}
        n = 0
        while n in taken:
            n += 1
        level[i] = n
    top = {i: max(level[j] for j in level if same(i, j)) for i in level}
    return level, top


def spread(xs, gap):
    """Positions for labels wanted at xs (sorted), at least gap apart, each
    crowded run centred on what it stands for."""
    groups = [[x] for x in xs]
    while True:
        out, start, moved = [], [], False
        for g in groups:
            if out:
                n_prev = len(out[-1])
                if start[-1] + n_prev * gap > sum(g) / len(g) - (len(g) - 1) * gap / 2:
                    out[-1] = out[-1] + g
                    moved = True
                    m = sum(out[-1]) / len(out[-1])
                    start[-1] = m - (len(out[-1]) - 1) * gap / 2
                    continue
            out.append(g)
            start.append(sum(g) / len(g) - (len(g) - 1) * gap / 2)
        groups = out
        if not moved:
            break
    pos = []
    for g, s in zip(groups, start):
        pos += [s + i * gap for i in range(len(g))]
    return pos


def event_label(e):
    day = ""
    if e.day:
        day = (f"{e.day}–{e.day_end}" if e.day_end else
               f"{e.day} or {e.day_alt}" if e.day_alt else f"{e.day}")
    label = e.label
    if e.months:
        label = f"{label}: {', '.join(str(m) for m in e.months)}"
    elif e.month_end:
        label = f"{label} {e.month}–{e.month_end}"
    return f"{day} · {label}" if day else label


def draw_events(c):
    """The rim's dots, leaders and labels -> {key: (taps, label box, dot box)}."""
    dots = event_dots()
    level, top_of = stacks(dots)
    labelled = sorted([(a, i) for i, (a, _k, _f, lab) in enumerate(dots) if lab])
    # unwrap the circle at its widest gap, then spread the labels along it
    angles = [a for a, _i in labelled]
    gaps = [((angles[(j + 1) % len(angles)] - angles[j]) % 360, j) for j in range(len(angles))]
    _g, cut = max(gaps)
    order = labelled[cut + 1:] + [(a + 360, i) for a, i in labelled[:cut + 1]]
    base = order[0][0]
    order = [(a if a >= base else a + 360, i) for a, i in order]
    gap = math.degrees(EV_FS * 1.22 / R_EVL)
    placed = spread([a for a, _i in order], gap)
    out = {}
    # leaders under the dots, shown with the labels
    with c.group(data={"fs": EV_FS}):
        for (a, i), la in zip(order, placed):
            top = R_EV + top_of[i] * EV_STEP + EV_DOT + 2
            c.polyline([pt(top, dots[i][0]), pt(R_EVL - 30, la), pt(R_EVL - 12, la)],
                       (120, 116, 104), 1.2)
    for i, (a, key, filled, _lab) in enumerate(dots):
        e = SC.EVENT[key]
        col = STORY_COL[e.story]
        x, y = pt(R_EV + level[i] * EV_STEP, a)
        if filled:
            c.circle(x, y, EV_DOT, fill=col, stroke=BG, width=1.5)
        else:
            c.circle(x, y, EV_DOT - 1.5, fill=BG, stroke=col, width=3)
        b = bx((x - EV_DOT, y - EV_DOT, x + EV_DOT, y + EV_DOT), 3)
        out.setdefault(key, {"t": [], "dots": []})["dots"].append(b)
    with c.group(data={"fs": EV_FS}):
        for (a, i), la in zip(order, placed):
            key = dots[i][1]
            e = SC.EVENT[key]
            col = STORY_COL[e.story]
            x, y = pt(R_EVL - 12, la)
            c.circle(x, y, 5, fill=col)
            taps, _end = spoke(c, R_EVL, la, event_label(e), EV_FS, (236, 228, 208))
            out[key]["t"] = taps
            out[key]["la"] = la
    return out


# ---------------------------------------------------------------------------
# The Jubilee
# ---------------------------------------------------------------------------

CELL, CGAP = 112, 10
GRID_X = COL_X + (COL_W - (7 * CELL + 6 * CGAP)) / 2
GRID_Y = 420
JUB_Y = GRID_Y + 7 * (CELL + CGAP) + 50
JUB_H = 170
TRUMP_Y = JUB_Y + JUB_H + 40
SABBATH_FILL, SABBATH_TEXT = (54, 92, 60), (196, 236, 180)


def draw_jubilee(c):
    boxes = {}
    x0 = COL_X
    text(c, (x0 + COL_W / 2, 300), "Seven Sabbaths of years", 46, NAME_COL, "mm", bold=True)
    with c.group(data={"fs": 30}):
        text(c, (x0 + COL_W / 2, 362), "7 × 7 = 49 years, then the 50th", 30, TEXT_DIM, "mm",
             italic=True)
    sab = []
    for row in range(7):
        for col in range(7):
            n = row * 7 + col + 1
            x = GRID_X + col * (CELL + CGAP)
            y = GRID_Y + row * (CELL + CGAP)
            seventh = col == 6
            c.rect(x, y, CELL, CELL, fill=SABBATH_FILL if seventh else PANEL,
                   stroke=(120, 170, 110) if seventh else SAND_DIM, width=2.5 if seventh else 1.5,
                   rx=10)
            text(c, (x + CELL / 2, y + (CELL / 2 - 12 if seventh else CELL / 2)), str(n), 40,
                 SABBATH_TEXT if seventh else TEXT, "mm", bold=seventh)
            if seventh:
                sab.append(bx((x, y, x + CELL, y + CELL)))
    with c.group(data={"fs": 24}):
        for row in range(7):
            x = GRID_X + 6 * (CELL + CGAP)
            y = GRID_Y + row * (CELL + CGAP)
            text(c, (x + CELL / 2, y + CELL / 2 + 26), "Sabbath", 24, SABBATH_TEXT, "mm",
                 italic=True)
    gw = 7 * CELL + 6 * CGAP
    boxes["grid"] = bx((GRID_X, GRID_Y, GRID_X + gw, GRID_Y + 7 * (CELL + CGAP) - CGAP))
    boxes["sabbath_year"] = sab
    # the fiftieth year, set apart
    y = JUB_Y
    c.line((GRID_X + gw / 2, y - 44), (GRID_X + gw / 2, y - 6), GOLD, 3)
    c.polygon([(GRID_X + gw / 2 - 10, y - 16), (GRID_X + gw / 2 + 10, y - 16),
               (GRID_X + gw / 2, y - 2)], fill=GOLD)
    c.rect(GRID_X, y, gw, JUB_H, fill=(226, 186, 82), stroke=GOLD, width=3, rx=14)
    text(c, (GRID_X + 110, y + JUB_H / 2), "50", 96, (40, 30, 10), "mm", bold=True)
    text(c, (GRID_X + 230, y + 62), "Year of Jubilee", 50, (40, 30, 10), "lm", bold=True)
    with c.group(data={"fs": 30}):
        text(c, (GRID_X + 230, y + 122), "proclaim liberty", 30,
             (60, 44, 16), "lm", italic=True)
    boxes["jubilee"] = bx((GRID_X, y, GRID_X + gw, y + JUB_H))
    # the trumpet: the 10th day of the 7th month, on a small dial
    y = TRUMP_Y
    r = 100
    dx, dy = GRID_X + r + 10, y + r + 10
    c.circle(dx, dy, r, fill=PANEL, stroke=SAND_DIM, width=2)
    for m in range(12):
        a = m * 30
        t = math.radians(a)
        c.line((dx + (r - 26) * math.sin(t), dy - (r - 26) * math.cos(t)),
               (dx + r * math.sin(t), dy - r * math.cos(t)), SAND_DIM, 1.5)
    t = math.radians(ang(7, 10))
    c.line((dx, dy), (dx + (r - 8) * math.sin(t), dy - (r - 8) * math.cos(t)), SET_DAY, 4)
    c.circle(dx + (r - 14) * math.sin(t), dy - (r - 14) * math.cos(t), 13, fill=SET_DAY,
             stroke=BG, width=2)
    c.circle(dx, dy, 6, fill=SET_DAY)
    text(c, (dx, dy - r + 20), "1", 20, TEXT_DIM, "mm", bold=True)
    tx = dx + r + 40
    text(c, (tx, y + 50), "the trumpet sounds", 32, TEXT, "lm", italic=True)
    text(c, (tx, y + 104), "7th month, 10th day", 42, NAME_COL, "lm", bold=True)
    text(c, (tx, y + 158), "Day of Atonement", 42, SET_TEXT, "lm", bold=True)
    boxes["trumpet"] = bx((GRID_X, y, GRID_X + gw, y + 2 * r + 20))
    return boxes


# ---------------------------------------------------------------------------
# The key, and what isn't on the dial
# ---------------------------------------------------------------------------

KEY_Y = TRUMP_Y + 280
APART_Y = 2600
# why a dated day is off the dial, where it isn't simply "day, no month"
APART_WHY = {"ezekiel_40": "‘the beginning of the year’"}


def draw_key(c):
    x0, y = COL_X + 20, KEY_Y
    text(c, (x0, y), "The key", 36, NAME_COL, "lm", bold=True)
    y += 56
    rowh = 40

    def swatch(x, y, col, kind):
        if kind == "dot":
            c.circle(x + 16, y, 13, fill=col, stroke=BG, width=2)
        elif kind == "dash":
            c.rect(x, y - 13, 34, 26, fill=al(col, 0.25), stroke=col, width=2.5, rx=4)
            c._els[-1] = c._els[-1].replace("/>", ' stroke-dasharray="7 5"/>')
        elif kind == "moon":
            c.circle(x + 16, y, 9, fill=BG, stroke=col, width=3)
        elif kind == "ring":
            c.circle(x + 16, y, 7, fill=BG, stroke=col, width=3)
        else:
            c.rect(x, y - 13, 34, 26, fill=col, rx=4)

    for col, kind, label in ((PILGRIM, "bar", "pilgrim feast: 3 times a year"),
                             (SET_DAY, "dot", "a set day of the Law"),
                             (PILGRIM, "dash", "counted or not fixed: weeks, the sheaf"),
                             (LATER, "dash", "later: 2nd-month Passover, Purim"),
                             (MOON, "moon", "new moon")):
        swatch(x0, y, col, kind)
        text(c, (x0 + 52, y), label, 26, TEXT, "lm")
        y += rowh
    y += 16
    for kind, label in (("stated", "farming: the text ties it to a month"),
                        ("convention", "season only: placed by convention")):
        col = FARM_COL["grain"]
        if kind == "stated":
            c.rect(x0, y - 13, 34, 26, fill=al(col, 0.62), stroke=col, width=2, rx=4)
        else:
            swatch(x0, y, col, "dash")
        text(c, (x0 + 52, y), label, 26, TEXT, "lm")
        y += rowh
    x = x0
    for kind in ("rain", "water", "grain", "fruit", "soil", "winter"):
        c.rect(x, y - 13, 26, 26, fill=FARM_COL[kind], rx=4)
        text(c, (x + 34, y), kind, 22, TEXT_DIM, "lm")
        x += 46 + width(kind, 22)
    y += rowh + 16
    c.circle(x0 + 16, y, 7, fill=TEXT)
    text(c, (x0 + 34, y), "day given", 26, TEXT, "lm")
    c.circle(x0 + 230, y, 5.5, fill=BG, stroke=TEXT, width=3)
    text(c, (x0 + 248, y), "month only, set near its middle", 26, TEXT, "lm")
    y += rowh
    col_w = (COL_W - 40) / 2
    for n, (story, label) in enumerate(LEGEND_STORIES):
        xx = x0 + (n % 2) * col_w
        yy = y + (n // 2) * 36
        c.circle(xx + 16, yy, 9, fill=STORY_COL[story])
        text(c, (xx + 36, yy), label, 24, TEXT, "lm")
    y += (len(LEGEND_STORIES) + 1) // 2 * 36 + 24
    # the card that says what the dial is
    c.rect(x0, y - 4, 420, 54, fill=(30, 30, 44), stroke=SAND, width=2, rx=27)
    text(c, (x0 + 210, y + 23), "about the dial ▸", 28, NAME_COL, "mm", italic=True)
    return bx((COL_X, KEY_Y - 30, COL_X + COL_W, y + 54)), bx((x0, y - 4, x0 + 420, y + 50))


def draw_apart(c):
    """What the text dates but the dial can't place: a day with no month, a
    feast with no name, seasons with no month. -> {id: box}."""
    boxes = {}
    x0, y = COL_X + 20, APART_Y
    text(c, (x0, y), "Not on the dial", 36, NAME_COL, "lm", bold=True)
    y += 60
    with c.group(data={"layer": "events"}):
        for e in SC.DATED_EVENTS:
            if e.month is not None:
                continue
            key = e.key
            c.circle(x0 + 14, y, 8, fill=STORY_COL[e.story])
            s = f"{e.day} · {e.label}"
            text(c, (x0 + 34, y), s, 28, TEXT, "lm")
            why = APART_WHY.get(key, "day, no month")
            text(c, (x0 + 46 + width(s, 28), y), why, 22, TEXT_DIM, "lm", italic=True)
            right = x0 + 56 + width(s, 28) + width(why, 22, italic=True)
            boxes[key] = bx((x0, y - 22, max(x0 + 520, right), y + 22))
            y += 46
    with c.group(data={"layer": "farming"}):
        for key in ("spring_figs_vines", "dry_harvest"):
            f = SC.FARM[key]
            c.rect(x0 + 2, y - 12, 24, 24, fill=al(FARM_COL[FARM_KIND[key]], 0.3),
                   stroke=FARM_COL[FARM_KIND[key]], width=2, rx=4)
            text(c, (x0 + 34, y), f.label, 28, TEXT, "lm")
            text(c, (x0 + 46 + width(f.label, 28), y), "season, no month", 22, TEXT_DIM, "lm",
                 italic=True)
            boxes[key] = bx((x0, y - 22, x0 + 520, y + 22))
            y += 46
    with c.group(data={"layer": "john"}):
        s = "John 5:1 · a feast"
        c.rect(x0, y - 18, width(s, 24, bold=True) + 24, 36, fill=(24, 34, 48), stroke=JOHN_COL,
               width=2.5, rx=18)
        text(c, (x0 + 12, y + 1), s, 24, JOHN_COL, "lm", bold=True)
        text(c, (x0 + 40 + width(s, 24, bold=True), y), "not named", 22, TEXT_DIM, "lm",
             italic=True)
        boxes["John 5:1"] = bx((x0, y - 20, x0 + 420, y + 20))
    assert y + 30 < H, "Not on the dial runs off the sheet"
    return boxes


def draw_masthead(c):
    text(c, (60, 92), TITLE, 68, TEXT, "lm", bold=True)
    text(c, (62, 156), "the months, the feasts and the farming year, with the days the "
         "text dates", 28, TEXT_DIM, "lm", italic=True)


def build_svg():
    _PATHS.clear()
    c = SvgCanvas(W, H, bg=BG)
    draw_masthead(c)
    mb = draw_months(c)
    with c.group(data={"layer": "farming"}):
        fb = draw_farming(c)
    with c.group(data={"layer": "feasts"}):
        marks = draw_feasts(c)
        labels = draw_feast_labels(c, marks)
    with c.group(data={"layer": "john"}):
        jb = draw_john(c)
    with c.group(data={"layer": "feasts"}):
        cb = draw_centre(c)
    with c.group(data={"layer": "events"}):
        eb = draw_events(c)
    yb = draw_jubilee(c)
    kb, about = draw_key(c)
    ab = draw_apart(c)
    c._defs.extend(_PATHS)
    svg = c.tostring().replace(
        "<svg ", f'<svg xmlns:xlink="http://www.w3.org/1999/xlink" data-kind="chart" '
        f'data-title="{TITLE}" ', 1)
    return svg, dict(months=mb, farming=fb, marks=marks, labels=labels, john=jb, centre=cb,
                     events=eb, years=yb, key=kb, about=about, apart=ab)


# ---------------------------------------------------------------------------
# The sidecar
# ---------------------------------------------------------------------------

def dim(label, value, flag="", refs=()):
    return [label, value, flag, rows(*refs)]


def month_item(m, bs):
    names = [nm.name for nm in m.names]
    word = nth_month(m.n)
    lo, hi = m.modern
    it = {"id": f"month-{m.n}", "n": " · ".join(names) if names else f"The {word}",
          "s": f"the {word} · about {lo}–{hi}",
          "a": [word, f"month {m.n}"] + ([f"the {word}"] if names else []),
          "t": bs, "b": union(bs), "fr": frame(union(bs), 700)}
    dims = []
    for nm in m.names:
        dims.append(dim(nm.name, f"named in {len(nm.refs)} verse{'s' if len(nm.refs) > 1 else ''}",
                        "", nm.refs))
        if nm.name == "Abib":
            # never numbered beside its name: the month of the going out
            dims.append(dim("Numbered", f"the {word}: the month of the going out", "derived",
                            nm.numbered_by))
        elif nm.numbered_by:
            dims.append(dim("Numbered", f"{nm.name} is the {word}", "stated", nm.numbered_by))
        else:
            dims.append(dim("Numbered", f"never numbered in WEB; the {word} by the later "
                            "calendar", "not given", ()))
    if not names:
        dims.append(dim("Name", "WEB gives this month no name", "not given", ()))
    cap = [d for d in SC.DIVISIONS if d[0] == m.n][0]
    dims.append(dim("David's division", f"{cap[1]}, with 24,000", "", (cap[2],)))
    it["dims"] = dims
    tx = [["About", f"{lo}–{hi}: the usual equivalent, not the text's"]]
    notes = [nm.note.text for nm in m.names if nm.note]
    if m.n == 4:
        notes.append(SC.NOTES["tammuz"].text)
    it["tx"] = tx
    if notes:
        it["note"] = " ".join(notes)
    it["rg"] = []
    return it


def feast_item(f, taps, label_box, ly="feasts"):
    when, flag = WHEN[f.key]
    t = list(taps)
    if label_box:
        t.append(bx(label_box, 4))
    b = union(t)
    # WEB gives the second month's Passover no name of its own
    name = "Passover in the second month" if f.key == "second_passover" \
        else f.name[:1].upper() + f.name[1:]
    it = {"id": f.key.replace("_", "-"), "n": name,
          "s": when + (" · a pilgrim feast" if f.pilgrim else "") +
          (" · a later feast" if f.later else ""),
          "a": list(f.aka) + ([f.label] if f.label else []), "t": t, "b": b,
          "fr": frame(b, 620), "ly": ly}
    ref, _words = SC.DEFINED[f.key]
    dims = [dim("When", when, flag, (ref,))]
    if f.pilgrim:
        dims.append(dim("Pilgrim", "one of the three times a year", "stated", ("Deut 16:16",)))
    if f.pilgrim_note:
        dims.append(dim("Pilgrim", f.pilgrim_note.text, "", f.pilgrim_note.refs))
    dims.append(dim("Rest", f.rest.text, "", f.rest.refs))
    by_day = f.offerings_by_day
    if by_day and len(set(by_day)) > 1:
        for n, (o, r) in enumerate(zip(by_day, f.offerings_by_day_refs)):
            if f.key == "tents" and n == 7:
                break
            dims.append(dim(f"Day {n + 1}", o.row(), "", (r,)))
    elif f.offerings:
        nrefs = f.offerings_note.refs if f.offerings_note else ()
        each = " each day" if (f.days or 1) > 1 else ""
        dims.append(dim("Offerings", f.offerings.row() + each, "",
                        [r for r in nrefs if r.startswith("Num")] or nrefs))
    if f.offerings_lev23:
        lref = "Lev 23:18-19" if f.key == "weeks" else "Lev 23:12-13"
        dims.append(dim("In Leviticus 23", f.offerings_lev23.row(), "", (lref,)))
    it["dims"] = dims
    tx = []
    if f.aka:
        tx.append(["Also called", ", ".join(f.aka)])
    for label, note in (("The offerings", f.offerings_note), ("The day", f.date_note),
                        ("The name", f.name_note), ("Farming", f.farming)):
        if note and note.text not in ("None.", "None stated."):
            tx.append([label, note.text])
    it["tx"] = tx
    it["note"] = f.card.text()
    rg = [["In the Law" if not f.later else "In the text", rows(*f.refs)]]
    nt = list(f.nt_refs) + [a.ref for a in SC.ACTS if a.feast == f.key and a.ref not in f.nt_refs]
    if f.key in ("atonement",):
        nt = [a.ref for a in SC.ACTS if a.feast == f.key]
    if nt:
        rg.append(["In the New Testament", rows(*nt)])
    if f.aka_refs:
        rg.append(["Its names", rows(*[r for _n, r in f.aka_refs])])
    it["rg"] = rg
    if f.key == "atonement":
        it["tx"].append(["The Fast", "Acts 27:9's “the Fast” is usually read as the Day of "
                         "Atonement; the text doesn't name it."])
    return it


def farm_item(f, taps, ly="farming"):
    b = union(taps)
    it = {"id": "farm-" + f.key.replace("_", "-"), "n": f.label,
          "s": {"stated": "the text gives its month",
                "derived": "its month follows from the text"}.get(f.basis, "season only") +
          " · farming", "a": [FARM_LABEL.get(f.key, f.label)], "t": taps, "b": b,
          "fr": frame(b, 640), "ly": ly}
    dims = []
    for m0, d0, m1, d1, basis in f.drawn:
        span = (f"{nth_month(m0)}" if (m0, d0, d1) == (m1, 1, 30) else
                f"{nth_month(m0)}, {ordinal(d0)} day" if (m0, d0) == (m1, d1) else
                f"{nth_month(m0)} to {nth_month(m1)}" if (d0, d1) == (1, 30) else
                f"{nth_month(m0)}, {ordinal(d0)} to {nth_month(m1)}, {ordinal(d1)}")
        dims.append(dim("Drawn", span, basis, ()))
    if f.basis_note:
        dims.append(dim("In the text", f.basis_note.text, "", f.basis_note.refs))
    it["dims"] = dims
    it["tx"] = []
    it["note"] = f.card.text()
    it["rg"] = [["Verses", rows(*f.refs)]]
    return it


def event_item(e, taps, dots, la):
    when_day = (f"{nth_month(e.month)}, {ordinal(e.day)}"
                + (f" and {ordinal(e.day_end)}" if e.day_end else "") + " day"
                if e.month and e.day else
                f"{nth_month(e.month)}, no day given" if e.month else
                f"{ordinal(e.day)} day, no month given")
    if e.months:
        when_day = "the " + ", ".join(ordinal(m) for m in e.months[:-1]) + \
            f" and {ordinal(e.months[-1])} months"
    elif e.month_end:
        when_day = f"from the {nth_month(e.month)} to the {nth_month(e.month_end)}"
    t = list(taps) + list(dots)
    b = union(taps) if taps else union(dots)
    name = e.label[:1].upper() + e.label[1:]
    it = {"id": "day-" + e.key.replace("_", "-"), "n": name,
          "s": f"{when_day} · {SC.STORIES[e.story]}", "a": [SC.STORIES[e.story]],
          "t": t, "b": b, "ly": "events", "fs": EV_FS}
    if la is not None:
        rr = R_EV + 60
        x, y = pt(rr, la)
        it["fr"] = frame(union([b, [x - 1, y - 1, 2, 2]]), 620)
    dated = when_day
    if e.day_alt:
        dated += f" (Kings); the {ordinal(e.day_alt)} in Jeremiah"
    if e.month_from == "context":
        dated += ": the month carried from the verses before"
    elif e.month_from == "calendar":
        dated += ": Elul, the 6th month by the later calendar"
    # the flag is the month's and the day's together: a month the verse
    # doesn't give is derived, and no month at all is not given
    flag = ("not given" if not e.month else "derived" if e.month_from else
            "stated" if e.day else "")
    dims = [dim("Dated", dated, flag, (e.ref,)),
            dim("Year", e.when, "", ())]
    it["dims"] = dims
    it["tx"] = [["Note", e.doubt]] if e.doubt else []
    it["note"] = e.card.text()
    it["rg"] = [["Also told in", rows(*e.also)]] if e.also else []
    return it


JOHN_MARK = {"John 2:13": ("John 2:23", "John 4:45"), "John 6:4": (),
             "John 11:55": ("John 12:1", "John 12:12", "John 12:20", "John 13:1", "John 18:28",
                            "John 18:39", "John 19:14", "John 19:31"),
             "John 7:2": ("John 7:10", "John 7:14", "John 7:37"), "John 10:22-23": (),
             "John 5:1": ()}


def john_item(ref, box):
    m = [j for j in SC.JOHN if j.ref == ref][0]
    more = JOHN_MARK[ref]
    f = SC.FEAST.get(m.feast) if m.feast else None
    it = {"id": "john-" + ref.split()[1].replace(":", "-"), "n": ref,
          "s": (m.label if m.feast else "a feast of the Jews, not named") + " · John's feasts",
          "a": ["John", m.label], "b": box, "ly": "john", "fr": frame(box, 640)}
    it["dims"] = [dim("The feast", f.name if f else "not named", "" if f else "not given", (ref,))]
    tx = []
    if ref == "John 7:2":
        tx.append(["The last day", "John 7:37's “last and greatest day of the feast” isn't said "
                   "to be the seventh day or the eighth."])
    if ref == "John 10:22-23":
        tx.append(["When", "“It was winter”: WEB gives no month. The Dedication isn't one of "
                   "the Law's feasts."])
    if ref == "John 5:1":
        tx.append(["When", "John doesn't name the feast, so it has no place on the dial."])
    it["tx"] = tx
    it["note"] = m.card
    it["rg"] = [["The same feast", rows(*more)]] if more else []
    if not m.feast:
        # Acts names an unnamed feast too
        it["rg"].append(["Also unnamed", rows(*[a.ref for a in SC.ACTS if not a.feast])])
    it["feast"] = m.feast
    return it


def year_item(y, b):
    it = {"id": y.key.replace("_", "-"), "n": y.name[:1].upper() + y.name[1:],
          "s": f"every {ordinal(y.every)} year", "a": list(y.aka)}
    if isinstance(b[0], list):
        it["t"], it["b"] = b, union(b)
    else:
        it["b"] = b
    dims = []
    if y.trumpet:
        m, d, ref, _card = y.trumpet
        dims.append(dim("Proclaimed", f"{nth_month(m)}, {ordinal(d)} day: the Day of Atonement",
                        "stated", (ref,)))
    for r in y.rules:
        dims.append(dim(r.label, r.text, "", r.refs))
    it["dims"] = dims
    notes = {"sabbath_year": (SC.NOTES["release_timing"], SC.NOTES["never_kept"]),
             "jubilee": (SC.NOTES["jubilee_count"], SC.NOTES["jubilee_start"])}
    it["tx"] = [["Open", n.text] for n in notes[y.key]]
    it["note"] = y.card.text()
    it["rg"] = [["Its names", rows(*[r for _n, r in y.aka_refs])], ["Verses", rows(*y.refs)]]
    return it


ABOUT = [
    ("The months", "The months are lunar: the text keeps them by the new moon and never says "
     "how many days a month has, or how the year kept pace with the harvest. The dial draws "
     "twelve equal months of thirty days, a schematic, so a day's place on it is approximate.",
     ("Num 10:10", "Num 28:11")),
    ("The first month", "Abib, the month of the going out, is the first month of the year, "
     "drawn at the top; the year runs clockwise.", ("Exod 12:2", "Exod 13:4")),
    ("The names", "WEB numbers most dates and names a month only now and then. The fourth and "
     "fifth months have no name; Elul is never numbered, and is the sixth by the later "
     "calendar. “About March–April” and the rest are the usual equivalents, not the text's.",
     ("Neh 6:15",)),
    ("Thirty days", SC.NOTES["thirty_days"].text, SC.NOTES["thirty_days"].refs),
    ("The feasts", "Gold marks the three pilgrim feasts. The feast of weeks has no date: it is "
     "counted fifty days from the sheaf, whose own day is “the next day after the Sabbath”, so "
     "both are drawn dashed where the count puts them.", ("Lev 23:11", "Lev 23:15-16")),
    ("Farming", "Solid where the text ties it to a month or a feast; faded and dashed where the "
     "text names only the season, placed by convention.", ()),
    ("Dated days", "A filled dot where the text gives the day, a hollow one near the month's "
     "middle, clear of the dated days, where it gives only the month; dots on one day stack "
     "outward. Where Kings and Jeremiah give different days, the dot is Kings' and the label "
     "gives both. Their colours are the stories, and the labels show as you zoom in.", ()),
]


def sidecar(boxes):
    items, index = [], {}

    def add(key, it):
        index[key] = len(items)
        items.append(it)

    for m in SC.MONTHS:
        add(("m", m.n), month_item(m, boxes["months"][m.n]))
    for f in SC.FEASTS:
        if f.key in ("sabbath", "dedication"):
            continue
        add(("f", f.key), feast_item(f, boxes["marks"][f.key], boxes["labels"].get(f.key)))
    cb = boxes["centre"]
    add(("f", "sabbath"), feast_item(SC.FEAST["sabbath"], [cb["sabbath"]], None))
    add(("f", "daily"), feast_item(SC.DAILY, [cb["daily"]], None))
    tt = {"id": "three-times", "n": "Three times a year", "s": "the pilgrim feasts",
          "a": ["pilgrim feasts", "pilgrim"], "b": cb["three_times"], "ly": "feasts",
          "fr": frame(cb["three_times"], 620),
          "dims": [dim("The three", "unleavened bread, weeks and tents", "stated", ("Deut 16:16",)),
                   dim("In Exodus", "unleavened bread, harvest and ingathering", "",
                       ("Exod 23:14-17",))],
          "tx": [], "note": SC.THREE_TIMES_CARD.text(),
          "rg": [["Verses", rows(*SC.THREE_TIMES.refs)]]}
    add(("c", "three"), tt)
    jb = boxes["john"]
    jb_all = dict(jb, **{"John 5:1": boxes["apart"]["John 5:1"]})
    for ref in JOHN_MARK:
        add(("j", ref), john_item(ref, jb_all[ref]))
    ded = feast_item(SC.FEAST["dedication"], [jb["John 10:22-23"]], None, ly="john")
    ded["nohit"] = True
    add(("f", "dedication"), ded)
    for f in SC.FARMING:
        if f.key in boxes["farming"]:
            add(("a", f.key), farm_item(f, boxes["farming"][f.key]))
        else:
            add(("a", f.key), farm_item(f, [boxes["apart"][f.key]]))
    for e in SC.DATED_EVENTS:
        if e.key in boxes["events"]:
            ev = boxes["events"][e.key]
            add(("e", e.key), event_item(e, ev["t"], ev["dots"], ev.get("la")))
        elif e.key in boxes["apart"]:
            it = event_item(e, [boxes["apart"][e.key]], [], None)
            it.pop("fs")
            add(("e", e.key), it)
    yb = boxes["years"]
    grid = {"id": "seven-sabbaths", "n": "Seven Sabbaths of years",
            "s": "7 × 7 = 49 years, then the 50th", "a": ["forty-nine years"],
            "b": yb["grid"], "dims": [dim("Counted", SC.YEAR["jubilee"].rules[0].text, "stated",
                                          SC.YEAR["jubilee"].rules[0].refs)],
            "tx": [["Open", SC.NOTES["jubilee_count"].text]],
            "note": "You shall count off seven Sabbaths of years, seven times seven years",
            "rg": [["Verses", rows("Lev 25:8")]]}
    add(("y", "grid"), grid)
    add(("y", "sabbath_year"), year_item(SC.YEAR["sabbath_year"], yb["sabbath_year"]))
    add(("y", "jubilee"), year_item(SC.YEAR["jubilee"], yb["jubilee"]))
    m, d, ref, card = SC.YEAR["jubilee"].trumpet
    add(("y", "trumpet"), {
        "id": "jubilee-trumpet", "n": "The Jubilee trumpet",
        "s": f"{nth_month(m)}, {ordinal(d)} day: the Day of Atonement",
        "a": ["loud trumpet"], "b": yb["trumpet"],
        "dims": [dim("Sounded", f"the {ordinal(d)} day of the {nth_month(m)}, in the 50th year",
                     "stated", (ref,))],
        "tx": [["Open", SC.NOTES["jubilee_start"].text]], "note": card.text(), "rg": []})
    ab = {"id": "about-the-dial", "n": "About the dial", "s": "how the year is drawn",
          "a": ["key", "legend"], "b": boxes["about"],
          "dims": [dim(lbl, txt, "", refs) for lbl, txt, refs in ABOUT], "tx": [], "rg": []}
    add(("k", "about"), ab)
    key = {"id": "the-key", "n": "The key", "s": "the colours and marks", "a": [], "nos": True,
           "b": boxes["key"], "see": [index[("k", "about")]], "dims": [], "tx": [], "rg": []}
    add(("k", "key"), key)

    # the links between them
    def see(a, *bs):
        items[index[a]].setdefault("see", [])
        for b in bs:
            if b in index and index[b] not in items[index[a]]["see"]:
                items[index[a]]["see"].append(index[b])
    for f in list(SC.FEASTS) + [SC.DAILY]:
        if f.month:
            see(("f", f.key), ("m", f.month))
            see(("m", f.month), ("f", f.key))
    see(("f", "atonement"), ("y", "jubilee"), ("y", "trumpet"))
    see(("y", "jubilee"), ("y", "trumpet"), ("f", "atonement"), ("y", "sabbath_year"))
    see(("y", "trumpet"), ("f", "atonement"), ("y", "jubilee"))
    see(("y", "sabbath_year"), ("y", "jubilee"), ("f", "tents"))
    see(("y", "grid"), ("y", "sabbath_year"), ("y", "jubilee"))
    see(("f", "tents"), ("f", "eighth_day"), ("a", "ingathering"), ("y", "sabbath_year"))
    see(("f", "eighth_day"), ("f", "tents"))
    see(("f", "first_fruits_sheaf"), ("f", "weeks"), ("a", "barley_harvest"), ("a", "grain_count"))
    see(("f", "weeks"), ("f", "first_fruits_sheaf"), ("a", "wheat_harvest"), ("a", "grain_count"))
    see(("f", "passover"), ("f", "unleavened_bread"), ("f", "second_passover"))
    see(("f", "unleavened_bread"), ("f", "passover"), ("f", "first_fruits_sheaf"))
    see(("f", "second_passover"), ("f", "passover"))
    see(("f", "purim"), ("e", "purim_enjoined"))
    see(("e", "purim_enjoined"), ("f", "purim"))
    see(("c", "three"), ("f", "unleavened_bread"), ("f", "weeks"), ("f", "tents"))
    for f in ("unleavened_bread", "weeks", "tents"):
        see(("f", f), ("c", "three"))
    for ref in JOHN_MARK:
        fk = items[index[("j", ref)]].pop("feast")
        if fk:
            see(("j", ref), ("f", fk))
            see(("f", fk), ("j", ref))
    for e in SC.DATED_EVENTS:
        if e.month and ("e", e.key) in index:
            see(("e", e.key), ("m", e.month))
    for f in SC.FARMING:
        for fk, other in (("barley_harvest", "first_fruits_sheaf"), ("wheat_harvest", "weeks"),
                          ("grain_count", "weeks"), ("ingathering", "tents")):
            if f.key == fk:
                see(("a", fk), ("f", other))
    for m in SC.MONTHS:
        see(("m", m.n), *[("a", f.key) for f in SC.FARMING if f.basis != "season" and f.drawn
                          and f.drawn[0][0] == m.n])
    for it in items:
        if not it.get("see"):
            it.pop("see", None)

    # every verse a card names, for #at
    for it in items:
        flat = [r for _g, rs in it.get("rg", []) for r in rs]
        flat += [r for d in it.get("dims", []) for r in d[3]]
        it["r"] = [list(r) for r in sorted({tuple(r) for r in flat})]

    # the key's card explains the drawing: a verse it cites isn't what it names
    items[index[("k", "about")]]["r"] = []
    tours = []
    for tid, label, keys in TOURS:
        if keys is None:
            stops = [{"i": index[("f", k)], "r": rows(ref)} for k, ref in LEV23]
        else:
            stops = [{"i": index[("e", k)], "r": rows(SC.EVENT[k].ref)} for k in keys]
        tours.append({"id": tid, "label": label, "build": False, "stops": stops})

    used = sorted({r[0] for it in items for r in it["r"]}
                  | {r[0] for t in tours for s in t["stops"] for r in s["r"]})
    remap = {b: i for i, b in enumerate(used)}
    done = set()

    def re_book(rs):
        for r in rs:
            if id(r) not in done:
                done.add(id(r))
                r[0] = remap[r[0]]
    for it in items:
        re_book(it["r"])
        for _g, rs in it.get("rg", []):
            re_book(rs)
        for d in it.get("dims", []):
            re_book(d[3])
    for t in tours:
        for s in t["stops"]:
            re_book(s["r"])
    ids = [it["id"] for it in items]
    assert len(set(ids)) == len(ids), "ids collide"
    views = [{"id": "year", "label": "Year", "fr": [CX - 1040, CY - 1040, 2080, 2080]},
             {"id": "jubilee", "label": "Jubilee",
              "fr": [COL_X - 10, 250, COL_W + 20, TRUMP_Y + 240 - 250]}]
    return {"version": 1, "card": "parts", "noun": ["entry", "entries"],
            "books": [BOOK_NAMES[b] for b in used],
            "layers": [{"id": "feasts", "label": "Feasts", "on": True},
                       {"id": "farming", "label": "Farming", "on": True},
                       {"id": "events", "label": "Dated events", "on": True},
                       {"id": "john", "label": "John's feasts", "on": False}],
            "views": views, "tours": tours, "items": items}


def viewer_page():
    return reference_viewer.page(STEM, _fmt(W), _fmt(H), TITLE, data=True,
                                 placeholder="find a feast, month or day — Purim, Ziv, Haman…")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    svg, boxes = build_svg()
    path = os.path.join(OUT_DIR, STEM + ".svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    data = sidecar(boxes)
    dp = os.path.join(OUT_DIR, STEM + ".json")
    with open(dp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    vp = os.path.join(OUT_DIR, STEM + ".html")
    with open(vp, "w", encoding="utf-8") as f:
        f.write(viewer_page())
    print(path)
    print(f"  {W} x {H} px · {os.path.getsize(path) / 1024:.0f} KB")
    print(dp)
    print(f"  {len(data['items'])} cards · {os.path.getsize(dp) / 1024:.0f} KB")
    print(vp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
