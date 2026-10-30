"""Render Joshua 13-19 as per-verse vector SVGs: a camera tour of the
allotment of the land.

One map of the land is drawn in every verse and seen through a moving
camera (svg_map_camera.Flight), as in Numbers 34: each verse opens on the
previous verse's rest camera and flies to its own, so played in order the
seven chapters are one continuous flight.

Everything drawn is a point fact. The land, lakes and rivers are
gazetteer.py's (acts_geography's coast north of Beirut), and every place is
a gazetteer place (SITES, JERUSALEM or BEYOND). What each verse names, in
order, and the border it walks, are allotment.py's.

- **Each verse lights what it names:** its places (a highlighted dot and
  name), its waters and lands (an italic name). The camera frames them, or,
  for a verse that names nothing it can place, holds on the lot so far.
- **As the narrator says it:** each name, its disc, each leg of a walk and
  each name on the "not located" plate comes in as the MP3 says it, timed
  by narration_clock (the pauses in the audio matched to the verse's
  punctuation). On the map, a name said during the flight comes in as the
  camera lands; the plate, off the map, takes its names as they're said.
- **A tribe's land is its towns, drawn soft:** each place a verse gives a
  tribe keeps a pale disc of the tribe's colour, so the lots fill in as the
  chapters go. No border is drawn that the text doesn't walk.
- **A border walk** (the text going landmark by landmark) is a dotted line
  through the landmarks it names that have a point, drawn leg by leg as the
  verse names them; unplaced landmarks are passed over. Between two points
  of one shore or river it follows that line (`leg`), so a border along
  the sea or the Jordan is drawn on it. It stays, fainter, for the rest of
  the tribe's verses (and through verses that give no tribe), and fainter
  still after that. A walk changes its look only once the camera lands, so
  nothing dims during a flight.
- **Not located:** the verse's names with no point are listed on a plate at
  top right, so a town list with no known sites still shows its names.
- An overview inset (bottom left) shows the whole land with the camera's
  view boxed whenever the camera is in close.
- **The closings:** at "This is the inheritance of..." the camera rises to
  the whole land, the lot lights as the tribe is named, and its name joins
  a key in the sea and desert margins with a line to the lot (CLOSINGS).
  The key comes in by zoom on the whole land, so it grows to every lot by
  19:48. Levi stands in it with no line; Manasseh twice.
- **Zelophehad's daughters** (17:2-5): the camera dives into Manasseh's
  branch of the family tree (joshua17_tree.py), with a stage under it for
  17:4, and rises back to the map in 17:5.
- **At Shiloh** (18:1-11, 19:51) the camera dives from Shiloh's dot into a
  scene card of the Tent of Meeting and the congregation
  (joshua18_shiloh.py), flying the card's legs (its LEGS) and surfacing to
  the map for 18:5-7 and 18:9. While the card fills the frame the map is
  switched off and holds the last verse's names, and the compass fades.

The camera times itself to each verse's MP3, so re-run this whenever one
is re-rendered. A verse with no MP3 is paced on an estimate from its words.

    .venv\\Scripts\\python.exe generate_joshua1319_svg.py
It prints any name it had to drop or force, and anything that would land
after the narration.
"""

import os
import re
from typing import NamedTuple, Optional
from xml.sax.saxutils import escape

import acts_geography as G
import mediterranean as M
import allotment as AL
import gazetteer as GZ
import joshua17_tree as ZT
import joshua18_shiloh as SH
import narration_clock
import svg_figures as F
from config import WEB_AUDIO_DIR
from generate_israel_atlas import TEXT_WEB
from generate_tabernacle import (BG, H, HL, SAND, SAND_DIM, TEXT, TEXT_DIM, W,
                                 out_path)
from generate_tribal_maps import LAND, RIVER, SEA, TRIBE_COL, WATER_TXT
from passages import verse_numbers
from svg_chronicles_world import AUDIO_SLACK, _mp3_seconds
from svg_map_camera import (
    Ctx, Flight, Projection, SAFE, circle_hits_rect, dot_state, S_AREA, S_CUR, S_OTHER,
    Unit as MapUnit, _same, cam_duration, compass_rect, compass_scale_svg, discrete,
    emit_class as emit_px, emit_label_layers, emit_labels, extent_check, fade, held_labels,
    identities, ink, inset_view_rect, layout, midflight_qc, op_anim, poly_el, prev_state,
    rest_dots, rgb, screen_ring, title_rect, title_svg, to_screen, unchanged,
)
from svg_scene_card import (CARD_COVER, CARD_IN, card_ends, card_extent, card_op, cards_seen,
                            figure_svg)
from svg_surface import FONT_FAMILY, _fmt

BOOK = "Joshua"
CHAPTERS = range(13, 20)
REFS = [(c, v) for c in CHAPTERS for v in verse_numbers(BOOK, c)]
ALL = {**GZ.SITES, **GZ.JERUSALEM, **GZ.BEYOND}


def _mp3(c, v):
    return os.path.join(WEB_AUDIO_DIR, f"{BOOK}_{c}_{v}.mp3")


def _narration(c, v):
    sec = _mp3_seconds(_mp3(c, v))
    return round(sec, 1) if sec else None


def _estimate(c, v):
    """A verse with no MP3: the verse at the house voice's pace, about 3.5
    words a second."""
    return round(max(2.0, 1.2 + len(TEXT_WEB[(BOOK, c, v)].split()) / 3.5), 1)


NARR = {cv: _narration(*cv) or _estimate(*cv) for cv in REFS}

SAY_LEAD = 0.1                # a name starts to light this long before it's said
CLOCKS = {}                   # cv -> its narration_clock.Clock (None: no MP3)


def said(cv):
    """When the narration says each of the verse's names, in allotment's
    order: seconds into the MP3 (narration_clock), or None for every name
    when the verse has no MP3."""
    text = TEXT_WEB[(BOOK, *cv)]
    clk = CLOCKS[cv] = narration_clock.clock(text, _mp3(*cv))
    out, pos = [], 0
    for n in AL.VERSES[cv].names:
        word = re.compile(r"(?<!\w)" + re.escape(n.web) + r"(?!\w)")
        m = word.search(text, pos)
        if m:
            pos = m.end()
        else:
            m = word.search(text)
        out.append(round(clk(m.start()), 2) if clk and m else None)
    return out

# ---------------------------------------------------------------------------
# The world: 100 world units a degree of latitude, as Numbers 34
# ---------------------------------------------------------------------------

LAT_TOP, LAT_BOT, LON_L, LON_R = 34.45, 30.30, 33.75, 36.95
PROJ = Projection(LAT_TOP, LON_L, 32.3)
K, EFF = PROJ.k, PROJ.eff
P, PS, shot, fit = PROJ.P, PROJ.PS, PROJ.shot, PROJ.fit

# The coast: acts_geography's down the Lebanese shore to where gazetteer.COAST
# starts (south of Beirut), gazetteer's to the brook of Egypt, and
# mediterranean.AFRICA's west along Sinai. The world runs MARGIN degrees past
# the sheet on every side, so a wide shot on a wide screen never sees its edge.
MARGIN = 2.5
_LEVANT = [i for i, p in enumerate(G.MAIN_COAST) if p[1] > 35.3]
_FROM = next(i for i in _LEVANT if G.MAIN_COAST[i][0] < LAT_TOP + MARGIN)
_TO = next(i for i, p in enumerate(G.MAIN_COAST) if p[0] < 33.75)
COAST = (G.MAIN_COAST[_FROM:_TO] + GZ.COAST
         + [p for p in M.AFRICA[1:] if p[1] > LON_L - MARGIN])
LAND_RING = COAST + [(COAST[-1][0], LON_L - MARGIN - 1), (LAT_BOT - MARGIN - 1, LON_L - MARGIN - 1),
                     (LAT_BOT - MARGIN - 1, LON_R + MARGIN + 1),
                     (LAT_TOP + MARGIN + 1, LON_R + MARGIN + 1),
                     (LAT_TOP + MARGIN + 1, COAST[0][1])]
LAKES = list(GZ.LAKES.values())
RIVERS = list(GZ.RIVERS.values())

# ---------------------------------------------------------------------------
# What each verse names
# ---------------------------------------------------------------------------


# generate_tribal_maps' colours, but Reuben's and Gad's moved off Judah's
# brown and Ephraim's green, which face them across the river, and Benjamin's
# and Asher's off Manasseh's teal (they were one blue-teal family on the whole
# land): each new one is at least 11 CIEDE2000 from every other lot, the
# water and the gold, and about 20 from the lots beside it
LOT_COL = dict(TRIBE_COL, REUBEN=(190, 100, 128), GAD=(80, 178, 196),
               BENJAMIN=(168, 149, 187), ASHER=(198, 159, 139))


def lot_key(tribe, c):
    """A tribe's lot as LOT_COL keys it (Manasseh's half by its chapter)."""
    if not tribe or tribe == "Levi":
        return None
    if tribe == "Manasseh":
        return "MANASSEH_E" if c == 13 else "MANASSEH_W"
    return tribe.upper()


def tribe_col(tribe, c):
    """The colour of a tribe's lot."""
    key = lot_key(tribe, c)
    return LOT_COL[key] if key else None


def point(n):
    if n.kind == AL.SITE:
        s = ALL[n.key]
        return (s.lat, s.lon)
    if n.kind == AL.WATER:
        return n.at
    if n.kind == AL.REGION:
        r = GZ.REGIONS[n.key]
        return (r.lat, r.lon)
    return None


def site_text(n):
    """A place's name as the map writes it, and the gazetteer name under it
    where the verse calls it otherwise (Baalah, Kiriath Jearim)."""
    s = ALL[n.key]
    if n.web.endswith(("ite", "ites", "ians")):
        return s.label or s.name, None              # the Gazites: Gaza
    names = {s.name, *[x.strip() for x in s.label.split("·")], *s.aka}
    if n.web in names or s.name in n.web:
        short = (s.label or s.name) if n.web in names else n.web
        # the shorter of the verse's word and the map's name for one place
        return (short if len(short) < len(n.web) else n.web), None
    return n.web, s.label or s.name


# the gazetteer's own lines a border can run along: the coast, the lakes'
# shores (rings) and the rivers, each with its points' places in it
SHORES = [(ln, ring, {(round(a, 4), round(b, 4)): i for i, (a, b) in reversed(list(enumerate(ln)))})
          for ln, ring in [(GZ.COAST, False), *[(lk, True) for lk in GZ.LAKES.values()],
                           *[(rv, False) for rv in GZ.RIVERS.values()]]]


def _length(pts):
    return sum(((a[0] - b[0]) ** 2 + ((a[1] - b[1]) * EFF) ** 2) ** 0.5
               for a, b in zip(pts, pts[1:]))


def leg(a, b):
    """The walk from one landmark to the next: along the coast, a lake's
    shore (the shorter way round) or a river where both are points of it,
    else straight."""
    ka, kb = (round(a[0], 4), round(a[1], 4)), (round(b[0], 4), round(b[1], 4))
    best = None
    for ln, ring, at in SHORES:
        if ka not in at or kb not in at:
            continue
        i, j, n = at[ka], at[kb], len(ln)
        if ring:
            ways = [[ln[(i + k) % n] for k in range((j - i) % n + 1)],
                    [ln[(i - k) % n] for k in range((i - j) % n + 1)]]
        else:
            ways = [ln[i:j + 1] if i <= j else ln[j:i + 1][::-1]]
        for w in ways:
            if best is None or _length(w) < _length(best):
                best = w
    return best or [a, b]


def walk_runs(cv, prev_end, times=None):
    """The verse's border walk as runs of the landmarks it names that have a
    point, in order ("|" breaks a run): carried on from the last verse's end
    when the text carries it on, or from the place it turns at. A water
    walked for a stretch gives the stretch's ends. Each landmark is
    (point, when the narration names it), from `times` (said()'s); a
    stretch's far end takes the time of the landmark that next names its
    point (13:27's Jordan runs 'to the sea of Chinnereth')."""
    v = AL.VERSES[cv]
    by_web = {}
    for i, n in enumerate(v.names):
        by_web.setdefault(n.web, (n, times[i] if times else None))
    first = prev_end if v.cont else ((ALL[v.start].lat, ALL[v.start].lon) if v.start else None)
    runs, cur = [], ([(first, None)] if first else [])
    open_end = False              # cur's last point is a stretch's far end, its time not yet named
    for w in v.walk:
        if w == "|":
            runs.append(cur)
            cur, open_end = [], False
            continue
        n, t = by_web[w]
        if n.kind not in (AL.SITE, AL.WATER):
            continue
        for p in ((n.along[0], n.at, n.along[1]) if n.along else (point(n),)):
            if not cur or cur[-1][0] != p:
                cur.append((p, t))
                open_end = False
            elif open_end and t is not None:
                cur[-1] = (p, max(t, cur[-1][1] or t))
                open_end = False
        open_end = bool(n.along)
    runs.append(cur)
    return runs


def walk_legs(cv, prev_end, times=None):
    """The verse's border walk as legs from landmark to landmark, each with
    when the narration names the landmark it reaches."""
    if not AL.VERSES[cv].walk:
        return []
    return [(leg(a, b), tb) for r in walk_runs(cv, prev_end, times)
            for (a, _ta), (b, tb) in zip(r, r[1:])]


# names the plate leaves off: peoples, the tribes' lands, and what isn't a place
NOT_LOCATED_SKIP = {"Canaan", "Egypt", "Midian", "Avvim", "Tent of Meeting", "Judah", "Asher",
                    "Issachar", "Zebulun"}


def unplaced(cv):
    """The verse's names with no point, for the 'not located' plate."""
    seen, out = set(), []
    for n in AL.VERSES[cv].names:
        if (n.kind == AL.UNPLACED and n.web not in seen and n.web[:1].isupper()
                and not n.web.endswith("ites") and n.web not in NOT_LOCATED_SKIP):
            seen.add(n.web)
            out.append(n.web)
    return out


def walk_end(cv, prev_end):
    """Where the border stands after the verse: its walk's last landmark with
    a point; the last verse's, when this one walks nowhere or carries on
    from it without placing any."""
    if not AL.VERSES[cv].walk:
        return prev_end
    return next((r[-1][0] for r in reversed(walk_runs(cv, prev_end)) if r), None)


# ---------------------------------------------------------------------------
# The shot list: each verse frames what it names
# ---------------------------------------------------------------------------

WIDE = fit(30.55, 33.65, 33.95, 36.75, (0, 14, W, H - 14))      # the whole land
NORTH = fit(32.9, 34.35, 34.6, 36.6, (0, 14, W, H - 14))         # Joshua 13:4-6
VIEW = (150, 80, W - 70, H - 56)       # the framing box, clear of the title, inset and scale
PX_MIN, PX_CAP, PX_MAX = 120.0, 600.0, 6000.0
SPREAD_PX = 80                # a cluster zooms in (past PX_CAP) until its places are this far apart


def frame(pts, cv=None):
    """A rest camera on the points, inside VIEW and below the verse's
    'not located' plate: close enough to part the two nearest places (up to
    PX_MAX), else no closer than PX_CAP, with a margin round them that
    narrows as a cluster tightens."""
    lats = [p[0] for p in pts]
    lons = [p[1] for p in pts]
    near = min((((a[0] - b[0]) ** 2 + ((a[1] - b[1]) * EFF) ** 2) ** 0.5
                for i, a in enumerate(pts) for b in pts[i + 1:] if a != b), default=None)
    cap = PX_CAP if near is None else min(PX_MAX, max(PX_CAP, SPREAD_PX / near))
    pad = PX_CAP / cap
    la0, la1 = min(lats) - 0.06 * pad, max(lats) + 0.06 * pad
    lo0, lo1 = min(lons) - 0.08 * pad, max(lons) + 0.08 * pad
    vx0, vy0, vx1, vy1 = VIEW
    pr = plate_rect(cv) if cv else None
    if pr:
        vy0 = max(vy0, pr[3] + 14)
    pxdeg = min((vx1 - vx0) / max(0.01, (lo1 - lo0) * EFF), (vy1 - vy0) / max(0.01, la1 - la0))
    pxdeg = max(PX_MIN, min(cap, pxdeg))
    return shot((la0 + la1) / 2, (lo0 + lo1) / 2, round(pxdeg),
                (vx0 + vx1) / 2, (vy0 + vy1) / 2)


# ---------------------------------------------------------------------------
# Scene cards the camera dives into: Manasseh's branch of the family tree
# (joshua17_tree.py) for Zelophehad's daughters, 17:2-5, and the Tent of
# Meeting at Shiloh (joshua18_shiloh.py) for 18:1-4, 18:8, 18:10-11 and 19:51. A card's verses
# fly its legs (its module's LEGS); a leg to "map" goes to the verse's camera
# on the map, which map_at sets where the default framing wouldn't do.
# ---------------------------------------------------------------------------

def word_time(cv, word):
    """When the narration says `word` (its first time in the verse), or None."""
    text = TEXT_WEB[(BOOK, *cv)]
    if cv not in CLOCKS:
        CLOCKS[cv] = narration_clock.clock(text, _mp3(*cv))
    clk = CLOCKS[cv]
    m = re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", text)
    return round(clk(m.start()), 2) if clk and m else None


SHILOH = ALL["shiloh"]
# the card times its beats by the narration's words, as the map does
SHI = SH.build(P(SHILOH.lat, SHILOH.lon), LOT_COL, word_time)
# Zelophehad's daughters (17:2-5): Manasseh's branch of the family tree, hung
# at the hill country of west Manasseh (the region's point: it has no dot)
SAMARIA = GZ.REGIONS["samaria"]
ZEL = ZT.build(P(SAMARIA.lat, SAMARIA.lon), word_time)
CARDS = [(SHI, SH), (ZEL, ZT)]   # (card, its module: SHOTS and LEGS)
S_CARD = SH.S_CARD            # one camera scale at every card's zoom 1


def card_of(cv):
    """The card a verse flies into, and its module, or (None, None)."""
    return next(((card, mod) for card, mod in CARDS if cv in mod.LEGS), (None, None))
CAP_S = CARD_IN[0] * S_CARD   # the scale bar stops following the camera here, as the card shows


def lot_points(state, keys):
    return [(ALL[k].lat, ALL[k].lon) for key in keys for k in state["lots"].get(key, [])]


def coming_lots():
    """The places the seven lots of 18:11-19:48 will give, in the order the
    verses name them: what 18:9's men surveyed "by cities"."""
    out = []
    for cv in REFS[REFS.index((18, 11)):REFS.index((19, 49))]:
        verse = AL.VERSES[cv]
        if verse.kind not in ("towns", "border") or not verse.tribe:
            continue
        for n in verse.names:
            if (n.kind == AL.SITE and n.key in GZ.SITES and n.key not in out
                    and (verse.tribe in GZ.SITES[n.key].tribe
                         or (verse.kind == "towns" and not GZ.SITES[n.key].tribe))):
                out.append(n.key)
    return out


def map_at(cv, state):
    """A verse's camera on the map where the default framing wouldn't do:
    the lots 18:5 and 18:7 name, the "here" of 18:6, and the whole land the
    tour ends on."""
    if cv == (18, 5):
        return frame(lot_points(state, ("JUDAH", "EPHRAIM", "MANASSEH_W")), cv)
    if cv == (18, 6):
        return frame([(SHILOH.lat, SHILOH.lon)], cv)
    if cv == (18, 7):
        pts = lot_points(state, ("REUBEN", "GAD", "MANASSEH_E"))
        top = max(pts)                      # Bashan, the half-tribe's north
        return frame(pts + [point(n) for n in AL.VERSES[cv].names]
                     + [(top[0] + 0.12, top[1])], cv)
    if cv == (18, 11):
        return frame([p for p in lot_points(state, ("JUDAH",)) if p[0] > 31.55]
                     + [p for p in lot_points(state, ("EPHRAIM",)) if p[0] < 32.25], cv)
    if cv in ((14, 3), (19, 51)):
        return WIDE
    if cv in CLOSINGS and CLOSINGS[cv].rise is None:
        return WIDE                         # a closing that opens on the formula
    return None


def map_shot(name, cv, state):
    """A named map camera a card's legs fly to on the way (LEGS)."""
    if name == "survey":
        return frame([(ALL[k].lat, ALL[k].lon) for k in coming_lots()
                      if k not in state["allotted"]] + [(SHILOH.lat, SHILOH.lon)], cv)
    raise KeyError(name)


def card_legs(cv, cam_map, state):
    """A card verse's legs, shortened together if they'd run past the
    narration (they are tuned to today's MP3s)."""
    card, mod = card_of(cv)
    total = sum(d for _k, _t, d in mod.LEGS[cv])
    fit = min(1.0, (NARR[cv] - AUDIO_SLACK) / total)
    legs = []
    for kind, target, dur in mod.LEGS[cv]:
        if target is None:
            cam = None
        elif target in mod.SHOTS:
            cam = card.cam(*mod.SHOTS[target])
        elif target == "map":
            cam = cam_map
        else:
            cam = map_shot(target, cv, state)
        legs.append((kind, cam, round(dur * fit, 2)))
    return legs


# A lot the narration names lights as it's said (18:5, 18:7, 18:11, and every
# lot at 19:49's "by its borders"; the closings light theirs too): its discs come
# up and its walked borders take its colour; the next verse lets it go on
# landing. Each is (the word, the lots).
LIFT = {(18, 5): [("Judah", ("JUDAH",)), ("Joseph", ("EPHRAIM", "MANASSEH_W"))],
        (18, 7): [("Gad", ("GAD",)), ("Reuben", ("REUBEN",)), ("Manasseh", ("MANASSEH_E",))],
        (18, 11): [("Judah", ("JUDAH",)), ("Joseph", ("EPHRAIM", "MANASSEH_W"))],
        (14, 3): [("two", ("REUBEN", "GAD", "MANASSEH_E"))],
        (19, 49): [("borders", tuple(k for k in LOT_COL if k != "MANASSEH_E") + ("MANASSEH_E",))]}
# a place a verse names by another word: 18:6's "here" is Shiloh (18:8)
SAID_AS = {(18, 6): ("shiloh", "here")}


# ---------------------------------------------------------------------------
# The closings: "This is the inheritance of ..."
#
# At each tribe's closing words the camera rises to the whole land (WIDE).
# As the tribe is named its lot lights in the one look a named lot has
# (LIFT's: its discs again over themselves, its walked borders in its
# colour), and its name joins a key in the sea and desert margins, with a
# thin line to the lot. The key grows by one name at each closing and comes
# in by zoom whenever the camera is on the whole land, so by 19:48 it holds
# every lot. Levi has no land: LEVI stands at the foot of the east column
# with no line, and at 13:14's "made by fire" the horned altar (Exodus 27)
# beside it, in that verse only. Manasseh is written twice, once for each
# half. A verse that says the formula mid-verse (13:23, 16:8, ...) shows its
# own names first, holds them at least DWELL, then rises (the lot lights as
# the tribe is named, during the rise; the key's name waits for the
# landing); one that opens on it, or names nothing of its own (Levi's), flies
# straight to the land.
# ---------------------------------------------------------------------------

class Closing(NamedTuple):
    lot: Optional[str]            # the lot it lights (LOT_COL's key), None for Levi
    rise: Optional[str]           # the word the rise starts at; None: the verse opens on it
    name: str                     # the tribe's word, its first time after `rise`
    entry: Optional[str]          # the key entry it writes, None if written already


CLOSINGS = {
    (13, 14): Closing(None, None, "Levi", "LEVI"),
    (13, 23): Closing("REUBEN", "This", "Reuben", "REUBEN"),
    (13, 28): Closing("GAD", None, "Gad", "GAD"),
    (13, 31): Closing("MANASSEH_E", "were", "Manasseh", "MANASSEH_E"),
    (13, 33): Closing(None, None, "Levi", None),
    (15, 20): Closing("JUDAH", None, "Judah", "JUDAH"),
    (16, 8): Closing("EPHRAIM", "This", "Ephraim", "EPHRAIM"),
    (17, 10): Closing("MANASSEH_W", None, "Manasseh", "MANASSEH_W"),
    (18, 20): Closing("BENJAMIN", "This", "Benjamin", "BENJAMIN"),
    (18, 28): Closing("BENJAMIN", "This", "Benjamin", None),
    (19, 8): Closing("SIMEON", "This", "Simeon", "SIMEON"),
    (19, 16): Closing("ZEBULUN", None, "Zebulun", "ZEBULUN"),
    (19, 23): Closing("ISSACHAR", None, "Issachar", "ISSACHAR"),
    (19, 31): Closing("ASHER", None, "Asher", "ASHER"),
    (19, 39): Closing("NAPHTALI", None, "Naphtali", "NAPHTALI"),
    (19, 48): Closing("DAN", None, "Dan", "DAN"),
}
RISE = 2.6                    # seconds, the rise to the whole land
DWELL = 1.5                   # a verse's own names stand fully in at least this long, then fade with the rise
KEY_PX, KEY_ROW = 15, 28      # the key's names, and its rows' least spacing
KEY_X = (360, 690)            # where the west names end and the east names start, at WIDE
KEY_WEST = ("ASHER", "ZEBULUN", "MANASSEH_W", "EPHRAIM", "DAN", "JUDAH", "SIMEON")
KEY_EAST = ("NAPHTALI", "MANASSEH_E", "ISSACHAR", "GAD", "BENJAMIN", "REUBEN")
ALTAR_PX = 30                 # Levi's altar, its height on screen


def word_after(cv, word, after=None):
    """When the narration says `word`, its first time after `after` (a word
    said earlier in the verse), or None."""
    text = TEXT_WEB[(BOOK, *cv)]
    word_time(cv, word)                       # reads the verse's clock
    clk = CLOCKS[cv]
    start = 0
    if after:
        m = re.search(r"(?<!\w)" + re.escape(after) + r"(?!\w)", text)
        start = m.start() if m else 0
    m = re.compile(r"(?<!\w)" + re.escape(word) + r"(?!\w)").search(text, start)
    return round(clk(m.start()), 2) if clk and m else None


def gives(cv, allotted):
    """The places a verse gives its tribe, in the order it names them."""
    verse = AL.VERSES[cv]
    out = []
    if verse.tribe and verse.tribe != "Levi" and verse.kind in ("towns", "border"):
        for n in verse.names:
            if (n.kind == AL.SITE and n.key not in allotted and n.key in GZ.SITES
                    and n.key not in out
                    and (verse.tribe in GZ.SITES[n.key].tribe
                         or (verse.kind == "towns" and not GZ.SITES[n.key].tribe))):
                out.append(n.key)
    return out


_FINAL = {}


def final_lots():
    """Every lot's places once all are given: what the key's lines point at."""
    if not _FINAL:
        allotted = set()
        for cv in REFS:
            for k in gives(cv, allotted):
                allotted.add(k)
                _FINAL.setdefault(lot_key(AL.VERSES[cv].tribe, cv[0]), []).append(k)
    return _FINAL


def lot_centre(key):
    """Where a lot's line ends, at WIDE: the middle of its places, leaving
    out any far from the rest (Dan's Leshem in the far north)."""
    pts = [to_screen(WIDE, P(ALL[k].lat, ALL[k].lon)) for k in final_lots()[key]]
    mx = sorted(p[0] for p in pts)[len(pts) // 2]
    my = sorted(p[1] for p in pts)[len(pts) // 2]
    near = [p for p in pts if abs(p[0] - mx) + abs(p[1] - my) < 90] or pts
    return (sum(p[0] for p in near) / len(near), sum(p[1] for p in near) / len(near))


def key_tint(key):
    c = LOT_COL[key] if key != "LEVI" else TEXT_DIM
    return tuple(int(v + (245 - v) * 0.35) for v in c)


def key_text(key):
    return key.split("_")[0]


_KEY = {}


# a lot whose own places lie in other lots' land (west Manasseh's are its
# towns in Issachar and Asher, 17:11) points at its hill country instead
KEY_AT = {"MANASSEH_W": "samaria"}
DOT_AIR = 7                   # px a key line keeps from any other place's dot


def key_ends(key):
    """Where a lot's line may end, best first: on one of its own places,
    nearest the lot's middle first, so its end dot is a town of the lot."""
    if key in KEY_AT:
        r = GZ.REGIONS[KEY_AT[key]]
        return [to_screen(WIDE, P(r.lat, r.lon))]
    c = lot_centre(key)
    pts = [to_screen(WIDE, P(ALL[k].lat, ALL[k].lon)) for k in final_lots()[key]]
    return sorted(pts, key=lambda p: (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2)


def all_dots():
    """Every place's dot at WIDE once all the lots are given."""
    return [to_screen(WIDE, P(ALL[k].lat, ALL[k].lon))
            for ks in final_lots().values() for k in ks]


def line_air(pts, marks):
    """How near a key line (its points, text end first) comes to any dot
    but its own end."""
    end = pts[-1]
    return min((seg_dist(m, a, b) for m in marks
                if abs(m[0] - end[0]) + abs(m[1] - end[1]) > 1.5
                for a, b in zip(pts, pts[1:])), default=99)


def key_layout():
    """Each key entry at WIDE: its text's anchor (screen), which side, its
    line (text end to a town of its lot) and its ink box. A column's rows
    follow its lots' latitudes, KEY_ROW apart, so no two lines cross; a row
    moves, and a line ends on another of its lot's towns, as little as it
    must to keep the line off every other dot (DOT_AIR) and the places the
    whole-land verses mark (MARK_AIR); where no straight line can, it runs
    level from the name and turns once, near its town (a knee)."""
    if _KEY:
        return _KEY
    written = {c.entry: cv for cv, c in CLOSINGS.items() if c.entry}
    dots = all_dots()
    for side, keys, x in (("west", KEY_WEST, KEY_X[0]), ("east", KEY_EAST, KEY_X[1])):
        rows = sorted((key_ends(k)[0][1], k) for k in keys)
        ys, y_prev = [], -1e9
        for y, _k in rows:
            y_prev = max(y, y_prev + KEY_ROW)
            ys.append(y_prev)
        over = ys[-1] - (H - 70) if side == "west" else ys[-1] - (H - 110)
        if over > 0:
            ys = [y - over for y in ys]
        x0 = x + (6 if side == "west" else -6)
        ends = {}
        for i, (_y, k) in enumerate(rows):
            marks = wide_marks(written[k])
            best = None
            for rank, end in enumerate(key_ends(k)):
                for dy in range(-90, 91, 2):
                    y = ys[i] + dy
                    if (not 60 <= y <= H - 70
                            or any(abs(y - o) < KEY_ROW - 6 for j, o in enumerate(ys) if j != i)):
                        continue
                    for knee in (None, 20, 30, 45, 60):
                        if knee is None:
                            pts = [(x0, y), end]
                        else:
                            kx = end[0] + (knee if side == "east" else -knee)
                            if (kx - x0) * (end[0] - x0) <= 0 or abs(y - end[1]) < 6:
                                continue
                            pts = [(x0, y), (kx, y), end]
                        if any(_cross(s1, s2) for other in ends.values()
                               for s1 in zip(pts, pts[1:]) for s2 in zip(other, other[1:])):
                            continue
                        air = min(line_air(pts, dots) / DOT_AIR, line_air(pts, marks) / MARK_AIR)
                        cost = rank * 6 + abs(dy) / 2 + (0 if knee is None else 20)
                        score = (air < 1, cost if air >= 1 else -air)
                        if best is None or score < best[0]:
                            best = (score, y, pts)
            _s, ys[i], ends[k] = best
        for (_y, k), y in zip(rows, ys):
            _KEY[k] = dict(side=side, at=(x, y), line=ends[k])
    last = max(e["at"][1] for e in _KEY.values() if e["side"] == "east")
    _KEY["LEVI"] = dict(side="east", at=(KEY_X[1], last + KEY_ROW + 8), line=None)
    for k, e in _KEY.items():
        x, y = e["at"]
        b = ink(key_text(k), KEY_PX, True, False, "lm" if e["side"] == "east" else "rm")
        e["box"] = (x + b[0], y + b[1], x + b[2], y + b[3])
    return _KEY


MARK_AIR = 10                 # px a key line keeps from a place's dot


def wide_marks(since=None):
    """The dots the verses that rest on the whole land mark, at WIDE (from
    verse `since` on, when a key entry is written): what a key line must not
    pass over."""
    out = []
    for cv in REFS[REFS.index(since) if since else 0:]:
        if cv in ((14, 3), (19, 49)) or (cv in CLOSINGS and CLOSINGS[cv].rise is None):
            out += [to_screen(WIDE, P(*point(n))) for n in AL.VERSES[cv].names
                    if n.kind in (AL.SITE, AL.WATER)]
    return out


def seg_dist(p, a, b):
    """The distance from point p to the segment a-b."""
    ax, ay = a
    dx, dy = b[0] - ax, b[1] - ay
    t = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / max(1e-9, dx * dx + dy * dy)))
    return ((p[0] - ax - t * dx) ** 2 + (p[1] - ay - t * dy) ** 2) ** 0.5


def key_rects(present, altar=False):
    """The key's names, and Levi's altar where it stands, as plates the map's
    names keep off (at WIDE)."""
    out = []
    for k in present:
        e = key_layout()[k]
        x0, y0, x1, y1 = e["box"]
        if k == "LEVI" and altar:
            x1 += 12 + ALTAR_PX * 1.8
            y0, y1 = min(y0, e["at"][1] - ALTAR_PX / 2), max(y1, e["at"][1] + ALTAR_PX / 2)
        out.append(("key:" + k, (x0 - 10, y0 - 8, x1 + 10, y1 + 8)))
    return out


def key_lines(present):
    """The key's lines for the map's clash test, wide enough that a name
    keeps a clear gap from them."""
    return [(list(e["line"]), 8.0, "leader", None)
            for e in (key_layout()[k] for k in present) if e["line"]]


def key_op(cam):
    """The key shows only on the whole land, where it was laid out: it comes
    in over the last of a rise and goes over the first of a dive, by zoom
    and by how far the camera is from WIDE (not on 18:9's survey shot)."""
    s, wx, wy = cam
    off = ((wx - WIDE[1]) ** 2 + (wy - WIDE[2]) ** 2) ** 0.5 * WIDE[0]
    return max(0.0, min(1.0, (1.6 - s / WIDE[0]) / 0.45, (50 - off) / 30))


def world_at(xy):
    """A WIDE screen point in world units."""
    s, wx, wy = WIDE
    return ((xy[0] - W / 2) / s + wx, (xy[1] - H / 2) / s + wy)


def key_svg(fl, present, new=None, t_new=None, altar=None):
    """The key in world units, held at screen size: the names closed so far,
    `new` coming in at t_new, and Levi's altar ((t, fades in) or None)."""
    ops = [key_op(cm) for cm in fl.cams]
    keys = list(present) + ([new] if new else [])
    if not keys or max(ops) <= 0:
        return ""
    seen = [i for i, o in enumerate(ops) if o > 0]
    ks = [f"{1 / cm[0]:.5g}" for cm in fl.cams]
    k0, kanim = ks[0], seen_anim(fl, "transform", ks, seen, "scale")
    sw = [f"{1.2 / cm[0]:.4g}" for cm in fl.cams]
    dw = [f"{5.0 / cm[0]:.4g}" for cm in fl.cams]
    swa, dwa = seen_anim(fl, "stroke-width", sw, seen), seen_anim(fl, "stroke-width", dw, seen)
    sw, dw = f'stroke-width="{sw[0]}"', f'stroke-width="{dw[0]}"'
    tags = [f"{o:.2f}" for o in ops]
    out = [f'<g opacity="{tags[0]}">{seen_anim(fl, "opacity", tags, range(len(tags)))}']
    for k in keys:
        e = key_layout()[k]
        tint = rgb(key_tint(k))
        el = ""
        if e["line"]:
            wpts = [world_at(p) for p in e["line"]]
            bx, by = wpts[-1]
            el += (f'<g {sw} stroke="{tint}" stroke-opacity="0.8" fill="none" '
                   f'stroke-linejoin="round">{swa}'
                   f'<polyline points="{" ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in wpts)}"/></g>')
            if k not in KEY_AT:           # the end dot sits on a town of the lot
                el += (f'<g {dw} stroke="{tint}" stroke-linecap="round">{dwa}'
                       f'<path d="M{_fmt(bx)} {_fmt(by)}h0"/></g>')
        wx, wy = world_at(e["at"])
        anchor = "end" if e["side"] == "west" else "start"
        el += (f'<g transform="translate({_fmt(wx)} {_fmt(wy)})"><g transform="scale({k0})">{kanim}'
               f'<text x="0" y="0" font-size="{KEY_PX}" font-weight="bold" letter-spacing="1.2" '
               f'text-anchor="{anchor}" dominant-baseline="central" fill="{tint}" '
               f'stroke="{rgb(BG)}" stroke-width="4" stroke-opacity="0.85" '
               f'paint-order="stroke">{key_text(k)}</text>')
        if k == "LEVI" and altar:
            t, comes = altar
            w = e["box"][2] - e["box"][0]
            parts = F.altar("horned", fire=True)
            x0, x1, _y0, y1 = F.bbox((parts, 0))
            fig = figure_svg(parts, ALTAR_PX, TEXT_DIM, LAND, unit_h=y1)
            half = (x1 - x0) / 2 * ALTAR_PX / y1
            body = f'<g transform="translate({_fmt(w + 12 + half)} {ALTAR_PX / 2 - 2})">{fig}</g>'
            el += (f'<g opacity="0">{fade(t, 0.6)}{body}</g>' if comes else body)
        el += "</g></g>"
        out.append(f'<g opacity="0">{fade(t_new, 0.5)}{el}</g>' if k == new else el)
    out.append("</g>")
    return "".join(out)


def seen_anim(fl, attr, vals, seen, typ=None):
    """An animation of the flight's keyframe values kept only where the
    thing is seen (and where its value changes), so a key that shows for
    the last second of a long flight doesn't carry every keyframe."""
    if fl.static or len(set(vals)) == 1:
        return ""
    n = len(vals) - 1
    seen = set(seen)
    keep = [i for i in range(n + 1)
            if i in (0, n) or i in seen or i - 1 in seen or i + 1 in seen
            or (vals[i] != vals[i - 1] and vals[i] != vals[i + 1] and
                (i - 1 in seen or i + 1 in seen))]
    if len(keep) == n + 1:
        return fl._anim(attr, vals, typ)
    kind = "animateTransform" if typ else "animate"
    t = f' type="{typ}"' if typ else ""
    return (f'<{kind} attributeName="{attr}"{t} values="{";".join(vals[i] for i in keep)}" '
            f'keyTimes="{";".join(f"{i / n:.4f}" for i in keep)}" dur="{fl.dur:.2f}s" '
            f'begin="0s" fill="freeze"/>')


def key_qc():
    """The finished key at WIDE: no name touches another name, a lot's disc
    or a place's dot, and no two lines cross."""
    from svg_map_camera import rr_hit, seg_hits_rect
    probs = []
    lay = key_layout()
    discs = [to_screen(WIDE, P(ALL[k].lat, ALL[k].lon))
             for ks in final_lots().values() for k in ks]
    written = {c.entry: cv for cv, c in CLOSINGS.items() if c.entry}
    dots = all_dots()
    for k, e in lay.items():
        if not e["line"]:
            continue
        if line_air(e["line"], wide_marks(written[k])) < MARK_AIR:
            probs.append(f"line of {k} passes over a place the whole land marks")
        if line_air(e["line"], dots) < DOT_AIR:
            probs.append(f"line of {k} passes {line_air(e['line'], dots):.1f} px from a place's dot")
        if k not in KEY_AT and min(abs(e["line"][-1][0] - d[0]) + abs(e["line"][-1][1] - d[1])
                                   for d in key_ends(k)) > 1.5:
            probs.append(f"line of {k} doesn't end on a town of its lot")
    for k, e in lay.items():
        for k2, e2 in lay.items():
            if k < k2 and rr_hit(e["box"], e2["box"]):
                probs.append(f"key {k} touches {k2}")
        if any(circle_hits_rect(d, DISC_PX / 2, e["box"]) for d in discs):
            probs.append(f"key {key_text(k)} touches a lot's disc")
        if e["line"]:
            segs = list(zip(e["line"], e["line"][1:]))
            for k2, e2 in lay.items():
                if k2 != k and any(seg_hits_rect(a, b, e2["box"]) for a, b in segs):
                    probs.append(f"line of {k} crosses the name {key_text(k2)}")
                if k < k2 and e2["line"] and any(_cross(s1, s2) for s1 in segs
                                                 for s2 in zip(e2["line"], e2["line"][1:])):
                    probs.append(f"lines of {k} and {k2} cross")
    return probs


def _cross(a, b):
    def orient(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    (p1, p2), (p3, p4) = a, b
    return (orient(p1, p2, p3) * orient(p1, p2, p4) < 0
            and orient(p3, p4, p1) * orient(p3, p4, p2) < 0)


def coming_frame(cv):
    """A lot's first verse that names nothing it can place frames what the
    lot's next verses name: the camera dives from the whole land to it."""
    i = REFS.index(cv)
    key = lot_key(AL.VERSES[cv].tribe, cv[0])
    pts = []
    for nxt in REFS[i + 1:]:
        if lot_key(AL.VERSES[nxt].tribe, nxt[0]) != key:
            break
        pts += [point(n) for n in AL.VERSES[nxt].names
                if n.kind in (AL.SITE, AL.WATER, AL.REGION)]
    if not pts:
        return None
    mla = sorted(p[0] for p in pts)[len(pts) // 2]
    mlo = sorted(p[1] for p in pts)[len(pts) // 2]
    pts = [p for p in pts if abs(p[0] - mla) + abs(p[1] - mlo) < 0.7] or pts
    cam = frame(pts, cv)
    if cam[0] * K > PX_CAP:
        # the dive names nothing yet: no closer than a town close-up
        lat, lon = PROJ.latlon(cam[1], cam[2])
        cam = shot(lat, lon, PX_CAP)
    return cam


# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------

class Unit(MapUnit):
    proj = PROJ


def dot_cands(lat, lon):
    return [(lat, lon, c) for c in ("r", "l", "a", "b")]


FIXED = [
    ("sea", "The Great Sea", [(32.70, 34.35, "c"), (32.20, 34.40, "c"), (33.40, 34.85, "c"),
                              (31.75, 34.15, "c"), (31.45, 33.95, "c"), (33.95, 35.30, "c")],
     "great_sea"),
    ("salt", "Salt Sea", [(31.30, 35.57, "r"), (31.45, 35.58, "r"), (31.15, 35.53, "r")],
     "salt_sea"),
    ("chin", "Chinnereth", [(32.80, 35.64, "r"), (32.86, 35.64, "r"), (32.80, 35.52, "l")],
     "galilee"),
]


def units(cv, state, times=None):
    """The verse's names to lay out. Each of its own carries `said`: when the
    narration first says it (from `times`, said()'s), or None."""
    v = AL.VERSES[cv]
    col = tribe_col(v.tribe, cv[0])
    U, seen = [], set()
    by_key = {}

    def heard(u, t):
        if t is not None and (u.said is None or t < u.said):
            u.said = t
    for i, n in enumerate(v.names):
        p = point(n)
        t = times[i] if times else None
        if p is None:
            continue
        if n.web in seen:
            continue
        seen.add(n.web)
        if n.kind == AL.SITE:
            if n.key in by_key:
                heard(by_key[n.key], t)
                continue
            text, sub = site_text(n)
            u = Unit(n.key, text, [S_CUR, 18.0], HL, bold=True, cands=dot_cands(*p),
                     sub=sub, dot=HL, prio=1, new=True, must=True, home=p, min_px=16)
        elif n.kind == AL.WATER:
            # two waters at one point (the Salt Sea where the Jordan meets it)
            # share a name; a water at a place the verse names is that place's
            word = n.web[:1].upper() + n.web[1:]
            same = next((u for u in U if u.key.startswith("w:") and u.home == p), None)
            if same:
                same.text += " · " + word
                heard(same, t)
                continue
            if any(abs(point(m)[0] - p[0]) + abs(point(m)[1] - p[1]) < 0.01
                   for m in v.names if m.kind == AL.SITE):
                continue
            u = Unit(f"w:{n.web}@{p[0]:.4f},{p[1]:.4f}", word,
                     [S_AREA, S_OTHER],
                     WATER_TXT, italic=True, cands=dot_cands(*p), dot=HL, prio=2, must=True,
                     new=True, home=p)
        else:
            r = GZ.REGIONS[n.key]
            # the verse's own word where it says it otherwise (the hill country of Ephraim)
            word = n.web if n.web.lower() != r.name.lower() else r.name
            word = word[:1].upper() + word[1:]
            u = Unit("r:" + n.key, word, [S_AREA, S_OTHER], TEXT, italic=True,
                     cands=[(p[0], p[1], "c")], prio=3, new=True, gmax=1.25)
        u.said = None
        heard(u, t)
        U.append(u)
        by_key[u.key] = u
    if cv in SAID_AS:
        key, word = SAID_AS[cv]
        s = ALL[key]
        u = Unit(key, s.label or s.name, [S_CUR, 18.0], HL, bold=True,
                 cands=dot_cands(s.lat, s.lon), dot=HL, prio=1, new=True, must=True,
                 home=(s.lat, s.lon), min_px=16)
        u.said = word_time(cv, word)
        U.append(u)
    cur = {u.key for u in U}
    # the lot so far: its places named in earlier verses, dim (by lot, not
    # colour: Manasseh's two halves share one)
    if col:
        for key in state["lots"].get(lot_key(v.tribe, cv[0]), []):
            if key in cur:
                continue
            s = ALL[key]
            U.append(Unit(key, s.label or s.name, [S_OTHER, 14.0], TEXT_DIM,
                          cands=dot_cands(s.lat, s.lon), dot=SAND, prio=4,
                          home=(s.lat, s.lon)))
    named_waters = {n.key for n in v.names if n.kind == AL.WATER}
    for key, text, cands, wkey in FIXED:
        if wkey not in named_waters:
            U.append(Unit(key, text, [S_AREA, S_OTHER], WATER_TXT, italic=True,
                          cands=cands, prio=6, gmax=1.25, in_sea=key == "sea"))
    return U


def _over(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if w > 0 and h > 0 else 0.0


def unforce(placed, problems, cam, dots, hud):
    """A name the layout had to force sits wherever its first in-frame spot
    was. Move each to the spot, of all it may take, that overlaps the other
    names, the dots and the plates least."""
    forced = {k for k, _why in problems}
    for u in placed:
        if u.key not in forced:
            continue
        others = [r for o in placed if o is not u for r in o.rest_rects]
        blobs = [(x - 7, y - 7, x + 7, y + 7) for k, (x, y) in dots if k != u.key]
        plates = [r for _k, r in hud]
        best = None
        for cand in list(u.cands) + u.auto_cands(cam):
            rs, lead = u.rects(cam, cand)
            if any(r[0] < SAFE[0] or r[1] < SAFE[1] or r[2] > SAFE[2] or r[3] > SAFE[3]
                   for r in rs):
                continue
            cost = sum(_over(r, o) for r in rs for o in others) * 4
            cost += sum(_over(r, b) for r in rs for b in blobs) * 2
            cost += sum(_over(r, b) for r in rs for b in plates) * 4
            cost += 40 if lead else 0
            if best is None or cost < best[0]:
                best = (cost, cand, rs, lead)
        if best:
            _c, u.place, u.rest_rects, u.lead = best


# ---------------------------------------------------------------------------
# The HUD (screen space, never scaled)
# ---------------------------------------------------------------------------

SCALE_KMS = (50, 20, 10, 5, 2, 1)
SCALE_MAX_PX = 170
SCALE_OF = {}                 # cv -> the scale bar's km


def scale_km(fl, cap=None):
    """The longest round scale bar that stays short at the rest camera (or,
    for a verse in the card, at `cap`, where the bar stops following it)."""
    s = min(fl.cam1[0], cap) if cap else fl.cam1[0]
    for km in SCALE_KMS:
        if km / 111.0 * K * s <= SCALE_MAX_PX:
            return km
    return SCALE_KMS[-1]

INSET_RECT = (14, H - 14 - 168, 14 + 118, H - 14)
INSET_BOX = (30.30, 34.45, 33.80, 36.85)       # lat0, lat1, lon0, lon1
INSET_OFF, INSET_RAMP = 0.80, 0.07
PLATE_W = 300
FS_PLATE = 16
PLATE_ASCENT = 14.7           # Georgia's at FS_PLATE, from a row's top to its baseline


def title(cv):
    c, v = cv
    tribe = AL.VERSES[cv].tribe
    if tribe and tribe != "Levi":
        half = " (east)" if tribe == "Manasseh" and c == 13 else ""
        return f"The lot of {tribe}{half} — Joshua {c}"
    return f"The inheritance — Joshua {c}"


def inset_opacity(cam):
    la0, la1, _a, _b = INSET_BOX
    hfrac = (H / cam[0] / K) / (la1 - la0)
    return max(0.0, min(1.0, (INSET_OFF - hfrac) / INSET_RAMP))


def plate_rows(cv):
    """The verse's unplaced names, wrapped to the plate's rows."""
    rows, cur = [], []
    for nm in unplaced(cv):
        t = " · ".join(cur + [nm])
        x0, _y0, x1, _y1 = ink(t, FS_PLATE, False, False, "ra")
        if x1 - x0 > PLATE_W and cur:
            rows.append(cur)
            cur = [nm]
        else:
            cur.append(nm)
    if cur:
        rows.append(cur)
    return rows[:7]


def plate_lines(cv):
    """The plate's rows as the lines it writes."""
    return [" · ".join(r) for r in plate_rows(cv)]


def plate_rect(cv):
    lines = plate_lines(cv)
    if not lines:
        return None
    w = max(ink(t, FS_PLATE, False, False, "ra")[2] - ink(t, FS_PLATE, False, False, "ra")[0]
            for t in lines + ["not located"])
    return (W - 18 - w - 14, 6, W - 6, 6 + 12 + 22 * (len(lines) + 1) + 6)


def hud_rects(cv, cam):
    hud = [("title", title_rect(title(cv))), ("compass", compass_rect(PROJ, cam[0], SCALE_OF[cv]))]
    pr = plate_rect(cv)
    if pr:
        hud.append(("plate", pr))
    if inset_opacity(cam) > 0.05:
        hud.append(("inset", INSET_RECT))
    return hud


PLATE_IN = 0.3                # the plate comes in no sooner, as the last verse's leaves
NAME_FADE = 0.5


def plate_body(cv, shown=None):
    """The plate, its names written whole; or, with `shown` (name -> when
    it comes in), each name coming in at its time, its row already laid
    out, so nothing shifts. A name is hidden only by its animation (a set,
    then a fade), so a browser that doesn't animate a tspan shows it. The
    baselines are written out: WebKit doesn't carry a text's
    dominant-baseline into its tspans, which sat a row on the one above."""
    r = plate_rect(cv)
    out = [f'<rect x="{_fmt(r[0])}" y="{_fmt(r[1])}" width="{_fmt(r[2] - r[0])}" '
           f'height="{_fmt(r[3] - r[1])}" rx="8" fill="{rgb(BG)}" fill-opacity="0.82"/>',
           f'<text x="{W - 18}" y="{_fmt(r[1] + 10 + PLATE_ASCENT)}" font-size="{FS_PLATE}" '
           f'font-style="italic" fill="{rgb(TEXT_DIM)}" text-anchor="end">not located</text>']
    for i, row in enumerate(plate_rows(cv)):
        spans = []
        for j, nm in enumerate(row):
            s = escape((" · " if j else "") + nm)
            spans.append(s if shown is None else
                         f'<tspan><set attributeName="fill-opacity" to="0" begin="0s"/>'
                         f'{op_anim(0, 1, shown[nm], NAME_FADE)}{s}</tspan>')
        out.append(f'<text x="{W - 18}" y="{_fmt(r[1] + 10 + 22 * (i + 1) + PLATE_ASCENT)}" '
                   f'font-size="{FS_PLATE}" fill="{rgb(TEXT)}" text-anchor="end">{"".join(spans)}</text>')
    return "".join(out)


def plate_svg(cv, prev_cv, heard=None, late=None):
    """The 'not located' plate, fading over from the last verse's. With
    `heard` (name -> when the narration says it), it comes in just before
    its first name is said and each name as it's said (by `late` at the
    latest)."""
    now = plate_lines(cv)
    was = plate_lines(prev_cv) if prev_cv else []
    if now == was:
        return plate_body(cv) if now else ""
    out = ""
    if was:
        out += f'<g>{fade(0.0, 0.35, out=True)}{plate_body(prev_cv)}</g>'
    if now:
        t_in, shown = PLATE_IN, None
        if heard:
            names = [nm for row in plate_rows(cv) for nm in row]
            shown, t = {}, PLATE_IN
            for nm in names:
                said_at = heard.get(nm)
                t = max(t, PLATE_IN, said_at - SAY_LEAD if said_at is not None else t)
                shown[nm] = round(min(t, late), 2) if late is not None else round(t, 2)
            t_in = max(PLATE_IN, min(shown.values()) - 0.3)
        out += f'<g opacity="0">{fade(t_in, 0.5)}{plate_body(cv, shown)}</g>'
    return out


def inset_svg(fl, state, coming=(), card=False):
    """The overview inset; in a verse with the card it fades as the card
    comes in, so it never covers the people."""
    x0, y0, x1, y1 = INSET_RECT
    ops = [f"{inset_opacity(c) * (1 - card_op(c[0] / S_CARD) if card else 1):.2f}"
           for c in fl.cams]
    la0, la1, lo0, lo1 = INSET_BOX
    iw, ih = x1 - x0 - 8, y1 - y0 - 8
    k = min(iw / ((lo1 - lo0) * EFF), ih / (la1 - la0))
    ox = x0 + 4 + (iw - (lo1 - lo0) * EFF * k) / 2
    oy = y0 + 4 + (ih - (la1 - la0) * k) / 2

    def ip(lat, lon):
        return (ox + (lon - lo0) * EFF * k, oy + (la1 - lat) * k)
    out = [f'<g opacity="{ops[0]}">{fl._anim("opacity", ops)}',
           f'<defs><clipPath id="insetclip"><rect x="{x0}" y="{y0}" width="{x1 - x0}" '
           f'height="{y1 - y0}" rx="6"/></clipPath></defs><g clip-path="url(#insetclip)">',
           f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{rgb(SEA)}"/>',
           poly_el([ip(a, b) for a, b in LAND_RING], fill=LAND, closed=True)]
    for lk in LAKES:
        out.append(poly_el([ip(a, b) for a, b in lk], fill=SEA, closed=True))
    for key, col in state["allotted"].items():
        x, y = ip(ALL[key].lat, ALL[key].lon)
        out.append(f'<circle cx="{_fmt(x)}" cy="{_fmt(y)}" r="1.6" fill="{rgb(col)}"/>')
    for key, col, t in coming:
        x, y = ip(ALL[key].lat, ALL[key].lon)
        out.append(f'<circle cx="{_fmt(x)}" cy="{_fmt(y)}" r="1.6" fill="{rgb(col)}" '
                   f'opacity="0">{fade(t, DISC_FADE)}</circle>')
    out.append(inset_view_rect(fl, PROJ, ip, HL))
    out.append("</g>")
    out.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="6" '
               f'fill="none" stroke="{rgb(SAND_DIM)}" stroke-width="1.5"/></g>')
    return "".join(out)


# ---------------------------------------------------------------------------
# The world, per verse
# ---------------------------------------------------------------------------

DISC_PX = 26                  # a place's soft disc in its tribe's colour, on screen
DISC_OP = 0.30
DISC_FADE = 0.8
CLS_PX = {"w1": 1.0, "w2": 2.0, "riv": 1.6, "walk_old": 2.0, "walk_tribe": 2.6,
          "walk_lift": 3.6, "walk_cur": 3.6, "dots": 5.0, "survey": 6.5, "discs": DISC_PX}
DOTTED = (0.1, 7.0)
LET_GO = 0.8
WALK_STROKE = {"walk_old": SAND_DIM, "walk_tribe": SAND, "walk_cur": HL}
WALK_ORDER = ("walk_old", "walk_tribe", "walk_cur")     # bottom to top


def emit_class(fl, name, els):
    dash = DOTTED if name.startswith("walk") else None
    extra = (' stroke-linecap="round"' if name.startswith("walk") or name in ("dots", "survey", "discs")
             else "")
    return emit_px(fl, CLS_PX[name], els, extra, dash)


def disc(key, col):
    """A round blob the size of DISC_PX on screen (a zero-length path with a
    round cap, its width held by the camera's inverse scale)."""
    s = ALL[key]
    x, y = P(s.lat, s.lon)
    return (f'<path d="M{_fmt(x)} {_fmt(y)}h0" stroke="{rgb(col)}" '
            f'stroke-opacity="{DISC_OP}"/>')


def base_world():
    x0, y0 = P(LAT_TOP + MARGIN, LON_L - MARGIN)
    return [f'<rect x="{_fmt(x0)}" y="{_fmt(y0)}" '
            f'width="{_fmt((LON_R - LON_L + 2 * MARGIN) * EFF * K)}" '
            f'height="{_fmt((LAT_TOP - LAT_BOT + 2 * MARGIN) * K)}" fill="{rgb(SEA)}"/>',
            poly_el(PS(LAND_RING), fill=LAND, closed=True)]


# ---------------------------------------------------------------------------
# Verse assembly
# ---------------------------------------------------------------------------

NEED_AFTER = 1.6              # seconds left after landing, for the names and the walk
LEG_GAP = 0.35                # legs named together come in this far apart
LEG_FADE = 0.6


def heard_at(t_said, t_land, late, floor=0.05):
    """When something the narration says at `t_said` comes in: as it's said,
    but not before the camera lands, nor so late it ends after the
    narration. Unsaid (None) is on landing."""
    t = t_land + floor if t_said is None else max(t_land + floor, t_said - SAY_LEAD)
    return round(min(t, max(t_land + floor, late)), 2)


def walk_el(lg, was, now, t_land):
    """An earlier walk's leg in this verse's class, `now`. Where that differs
    from the class it ended the last verse in, `was`, it keeps the old look
    through the flight and takes the new once the camera lands: the upper
    copy fades over the lower."""
    def el(name):
        return poly_el(PS(lg), stroke=WALK_STROKE[name])
    if was == now:
        return {now: el(now)}
    if WALK_ORDER.index(was) > WALK_ORDER.index(now):
        return {now: el(now), was: f'<g>{fade(t_land, LET_GO, out=True)}{el(was)}</g>'}
    return {was: el(was), now: f'<g opacity="0">{fade(t_land, LET_GO)}{el(now)}</g>'}


def build_all():
    # state["walks"]: [colour, leg, the class it ended the last verse in, its lot]
    # state["lots"]: lot key (LOT_COL's) -> the places given it so far
    state = {"allotted": {}, "lots": {}, "walks": [], "walk_end": None,
             "lifted": [], "key": []}
    prev, prev_cv, prev_col, report = None, None, None, []
    last_lot = None               # the last tribe's: a verse with no tribe keeps its walks up
    last_lab = None               # the last verse that laid out names (a card verse doesn't)
    cam_prev = WIDE               # the last rest camera on the map
    last_cam = WIDE               # the last rest camera, on the map or in the card
    for cv in REFS:
        c, v = cv
        verse = AL.VERSES[cv]
        col = tribe_col(verse.tribe, c)
        lot = lot_key(verse.tribe, c)
        narr = NARR[cv]
        times = said(cv)
        late = narr - AUDIO_SLACK - NAME_FADE      # the last a name may start to come in
        legs_t = walk_legs(cv, state["walk_end"], times)
        legs = [lg for lg, _t in legs_t]
        named = [point(n) for n in verse.names if n.kind in (AL.SITE, AL.WATER, AL.REGION)]
        own = [p for lg in legs for p in lg
               if not (verse.cont and p == state["walk_end"])]
        pts = named + own
        if map_at(cv, state):
            cam_map = map_at(cv, state)
        elif cv[0] == 13 and 4 <= v <= 6:
            cam_map = NORTH
        elif pts:
            cam_map = frame(pts, cv)
        elif lot and state["lots"].get(lot):
            cam_map = frame([(ALL[k].lat, ALL[k].lon) for k in state["lots"][lot]], cv)
        elif cv == REFS[0] or (col and col != prev_col):
            cam_map = (cv != REFS[0] and coming_frame(cv)) or WIDE
        else:
            cam_map = cam_prev
        cam0 = last_cam
        card, mod = card_of(cv)
        clo = CLOSINGS.get(cv)
        # a closing said mid-verse: the verse's own frame first, then the rise
        two = clo is not None and clo.rise is not None and not _same(cam_map, WIDE)
        squeezed = False
        if card:
            fl = Flight(cam0, card_legs(cv, cam_map, state))
        elif two:
            D1 = cam_duration(cam0, cam_map)
            if D1:
                D1 = round(max(0.9, min(D1, 2.6)), 2)
            # its own names stand DWELL fully in, counted from when each comes
            # in: as said, or on landing (the lot so far, a name said in flight)
            dwell = [D1] + [max(D1 + 0.05, t - SAY_LEAD) + NAME_FADE + DWELL
                            for t in times if t is not None]
            if D1:
                dwell.append(D1 + 0.05 + NAME_FADE + DWELL)
            t_word = word_time(cv, clo.rise)
            t_rise = max(([round(t_word - SAY_LEAD, 2)] if t_word is not None else []) + dwell)
            latest = narr - AUDIO_SLACK - 1.2 - RISE     # the name and the key after landing
            if t_rise > latest:
                squeezed = t_rise > latest + 0.1          # short of DWELL by more than a tenth
                t_rise = round(max(D1 + 0.6, latest), 2)
            fl = Flight(cam0, [("to", cam_map, D1), ("hold", None, round(t_rise - D1, 2)),
                               ("to", WIDE, RISE)])
            fl_own = Flight(cam0, [("to", cam_map, D1)])
        else:
            D = cam_duration(cam0, cam_map)
            if D:
                D = round(max(0.9, min(D, narr - AUDIO_SLACK - NEED_AFTER)), 2)
            fl = Flight(cam0, [("to", cam_map, D)])
            assert _same(fl.cam1, cam_map), cv
        cam1 = fl.cam1
        t_land = fl.dur
        # the verse's own things (its names, discs and walk) come in as its own
        # frame lands; in a closing said mid-verse, before the rise
        t_own = fl_own.dur if two else t_land
        cam_own = cam_map if two else cam1
        if two:
            late = min(late, t_rise - NAME_FADE - 0.2)
        SCALE_OF[cv] = scale_km(fl_own if two else fl, CAP_S if card else None)
        zs = [cm[0] / S_CARD for cm in fl.cams]
        show_card = cards_seen(fl, [card], S_CARD) if card else []
        in_card = bool(show_card) and zs[-1] >= 0.2        # it rests inside the card
        show_map = min(zs) < CARD_COVER                     # the map is seen at all
        # the last moment the card shows: a name said before it isn't drawn on the map
        card_until = max((i * fl.dur / max(1, len(zs) - 1) for i, z in enumerate(zs)
                          if z >= CARD_IN[0]), default=None) if show_card else None

        # the places this verse gives its tribe, each as it's said
        new_keys = gives(cv, state["allotted"]) if col else []
        key_said = {}
        for n, t in zip(verse.names, times):
            if n.kind == AL.SITE and t is not None:
                key_said.setdefault(n.key, t)
        t_new = {k: heard_at(key_said.get(k), t_own, min(late, narr - AUDIO_SLACK - DISC_FADE), 0.1)
                 for k in new_keys}

        # ------ the world ------------------------------------------------
        cls = {k: [] for k in CLS_PX}
        qc = []
        overlay = []                  # screen space, over the map
        fills = base_world()
        for lk in LAKES:
            fills.append(poly_el(PS(lk), fill=SEA, closed=True))
        cls["discs"] = [disc(k, cl) for k, cl in state["allotted"].items()]
        for k in new_keys:
            cls["discs"].append(f'<g opacity="0">{fade(t_new[k], DISC_FADE)}{disc(k, col)}</g>')
        for lk in LAKES:
            cls["w1"].append(poly_el(PS(lk), stroke=SAND_DIM, closed=True))
            qc.append((PS(lk + lk[:1]), "lake"))
        cls["w2"].append(poly_el(PS(COAST), stroke=SAND_DIM))
        qc.append((PS(COAST), "coast"))
        for rv in RIVERS:
            cls["riv"].append(poly_el(PS(rv), stroke=RIVER))
            qc.append((PS(rv), "river"))
        for w in state["walks"]:
            lg, was = w[1], w[2]
            w[2] = "walk_tribe" if w[3] == (lot or last_lot) else "walk_old"
            for name, el in walk_el(lg, was, w[2], t_own).items():
                cls[name].append(el)
            qc.append((PS(lg), "border"))
        # the lots the last verse lit let go as this one lands (or, diving
        # into the card, at once); this verse's light as they're named
        t_go = 0.3 if show_card and fl.cams[0][0] < fl.cams[-1][0] else t_own
        # (a lot this verse lights again holds instead: no dim and relight)
        relit = {k for _w, ks in LIFT.get(cv, []) for k in ks}
        for key in state["lifted"]:
            for name, el in lift_els(key, state):
                cls[name].append(el if key in relit else
                                 f'<g>{fade(t_go, LET_GO, out=True)}{el}</g>')
        lifted = []
        for word, keys in LIFT.get(cv, []):
            t = heard_at(word_time(cv, word), t_own, late)
            for key in keys:
                if key in state["lifted"]:
                    lifted.append(key)
                    continue
                for name, el in lift_els(key, state):
                    cls[name].append(f'<g opacity="0">{fade(t, LET_GO)}{el}</g>')
                lifted.append(key)
        # 18:9 surveyed it by cities: the places the seven lots will give come
        # in nearest to Shiloh first, unnamed; they go under 18:10's dive
        if cv in ((18, 9), (18, 10)):
            sx, sy = P(SHILOH.lat, SHILOH.lon)
            todo = sorted((k for k in coming_lots() if k not in state["allotted"]),
                          key=lambda k: (P(ALL[k].lat, ALL[k].lon)[0] - sx) ** 2
                          + (P(ALL[k].lat, ALL[k].lon)[1] - sy) ** 2)
            # (18:9 surfaces from the card, then holds before closing on Shiloh)
            t0 = (round(max(word_time(cv, "surveyed") - SAY_LEAD, SH.LEGS[cv][0][2] + 0.1), 2)
                  if cv == (18, 9) else None)
            for i, k in enumerate(todo):
                x, y = P(ALL[k].lat, ALL[k].lon)
                el = f'<path d="M{_fmt(x)} {_fmt(y)}h0" stroke="{rgb(TEXT)}"/>'
                if t0 is not None:
                    el = f'<g opacity="0">{fade(round(t0 + 1.6 * i / len(todo), 2), 0.4)}{el}</g>'
                cls["survey"].append(el)
        # this verse's walk, each leg as the landmark it reaches is said (or,
        # with no narration clock, evenly through the verse)
        walk_dur = max(0.0, min(late + NAME_FADE, narr - AUDIO_SLACK) - t_own - 0.4)
        step = min(0.9, walk_dur / len(legs)) if legs else 0
        ends, t_prev = [t_land] + [t + DISC_FADE for t in t_new.values()], None
        for i, (lg, ts) in enumerate(legs_t):
            t = (heard_at(ts, t_own, late, 0.1) if ts is not None
                 else round(t_own + 0.1 + i * step, 2))
            if t_prev is not None:
                # one after another, and none past the narration's end
                t = round(min(max(t, t_prev + LEG_GAP), max(t, late)), 2)
            t_prev = t
            cls["walk_cur"].append(
                f'<g opacity="0">{fade(t, LEG_FADE)}'
                + poly_el(PS(lg), stroke=HL) + "</g>")
            ends.append(t + LEG_FADE)
            qc.append((PS(lg), "border"))
        # the closing: as the tribe is named (on landing, if it's said during
        # the rise) its lot lights, with this verse's discs and legs, and its
        # name joins the key
        key_new, t_key, altar = None, None, None
        if clo:
            t_name = word_after(cv, clo.name, clo.rise)
            t_key = heard_at(t_name, t_land, narr - AUDIO_SLACK - 0.6)
            if clo.lot:
                # discs and borders show at any zoom: the lot lights as it's
                # named, during the rise if need be
                t_light = heard_at(t_name, t_rise if two else t_land, narr - AUDIO_SLACK - LET_GO)
                own_els = (lift_els(clo.lot, state)
                           + [("discs", disc(k, col)) for k in new_keys]
                           + [("walk_lift", poly_el(PS(lg), stroke=LOT_COL[clo.lot])) for lg in legs])
                for name, el in own_els:
                    cls[name].append(f'<g opacity="0">{fade(t_light, LET_GO)}{el}</g>')
                if clo.lot not in lifted:
                    lifted.append(clo.lot)
                ends.append(t_light + LET_GO)
            if clo.entry:
                key_new = clo.entry
                ends.append(t_key + 0.5)
        if cv == (13, 14):                    # "made by fire": the altar, this verse only
            altar = (heard_at(word_time(cv, "fire"), t_land, narr - AUDIO_SLACK - 0.6), True)
            ends.append(altar[0] + 0.6)
        elif cv == (13, 15):
            altar = (0.0, False)              # it leaves with the dive
        # the other tribes' places, as small dots
        cur_named = {n.key for n in verse.names if n.kind == AL.SITE}
        for k, cl in state["allotted"].items():
            if k not in cur_named:
                x, y = P(ALL[k].lat, ALL[k].lon)
                cls["dots"].append(f'<path d="M{_fmt(x)} {_fmt(y)}h0" stroke="{rgb(cl)}"/>')
        if two:
            # a closing's own places keep a dot as their names go with the rise
            # (the next verse opens with them)
            given = dict(state["allotted"], **{k: col for k in new_keys})
            for k in cur_named & set(given):
                x, y = P(ALL[k].lat, ALL[k].lon)
                cls["dots"].append(f'<g opacity="0">{fade(t_rise + 0.2, 0.4)}'
                                   f'<path d="M{_fmt(x)} {_fmt(y)}h0" stroke="{rgb(given[k])}"/></g>')

        # ------ labels ---------------------------------------------------
        hud = hud_rects(cv, cam_own)
        at_wide = _same(cam1, WIDE)
        key_here = state["key"] + ([key_new] if key_new else [])
        if at_wide and not two:
            hud = hud + key_rects(key_here, bool(altar))     # the map's names keep off the key
        if prev_cv != last_lab:
            prev = None               # names last placed before the card
        lab, held, placed, dropped, problems, U = None, None, [], [], [], []
        if in_card:
            # no names to place on a map nobody sees: the last verse's stay as
            # they were until the card covers them
            held = prev if show_map else None
        else:
            # the lot's earlier places are named only where their dot rests
            # clear of the frame's edge and the plates; a name said while the
            # card is in frame isn't drawn on the map
            U = [u for u in units(cv, state, times)
                 if (u.prio < 4 or dot_state(to_screen(cam_own, P(*u.cands[0][:2])), hud) == "in")
                 and not (card_until is not None and u.prio < 4
                          and getattr(u, "said", None) is not None and u.said < card_until)]
            lines = [([to_screen(cam_own, p) for p in pts_], 3.0 if kind == "border" else 2.0,
                      kind, None) for pts_, kind in qc]
            if at_wide and not two:
                lines += key_lines(key_here)
            lines_w = [(pts_, 3.0 if kind == "border" else 2.0) for pts_, kind in qc]
            dots = rest_dots(PROJ, U, cam_own, hud)
            land = [to_screen(cam_own, P(a, b)) for a, b in LAND_RING]
            # a name never sits on a disc this verse lights (LIFT, a closing)
            lit_keys = [key for _w, keys in LIFT.get(cv, []) for key in keys]
            if clo and clo.lot and at_wide and not two:
                lit_keys.append(clo.lot)
            lit = [(k, to_screen(cam_own, P(ALL[k].lat, ALL[k].lon)))
                   for key in lit_keys for k in state["lots"].get(key, [])]

            wide_discs = ([to_screen(WIDE, P(ALL[k].lat, ALL[k].lon)) for k in state["allotted"]]
                          if at_wide and not two else [])

            def off_lit(u, cand, rs, lead, centre, lit=lit, wide_discs=wide_discs):
                hit = any(k != u.key and circle_hits_rect(xy, DISC_PX / 2 + 2, r)
                          for k, xy in lit for r in rs)
                hit = hit or (u.prio == 6 and any(circle_hits_rect(xy, DISC_PX / 2 + 2, r)
                                                  for xy in wide_discs for r in rs))
                return ["lit-disc"] if hit else []
            ctx = Ctx(PROJ, cam_own, lines, dots, hud, (), {}, land,
                      extra=off_lit if lit or wide_discs else None)
            placed, dropped, problems = layout(U, ctx, prev)
            unforce(placed, problems, cam_own, dots, hud)
            prev_units = prev["units"] if prev else {}
            cur_ident = identities(placed, cam_own)
            for u in U:
                u.t_in = None
                if unchanged(u, cur_ident, prev_units):
                    continue
                if u.new:
                    u.t_in = heard_at(getattr(u, "said", None), t_own, late)
            lab = emit_labels(PROJ, U, placed, cur_ident, prev, prev is not None, cam0, cam_own,
                              fl_own if two else fl, t_own, hud,
                              lambda cam, cv=cv: hud_rects(cv, cam), lines_w, problems)
            if two:
                # the verse's own names go as it rises; the land's come in as it
                # lands, clear of the key, and are what the next verse inherits
                lab_own, placed_own = lab, placed
                hud_w = hud_rects(cv, WIDE) + key_rects(key_here)
                U_w = [u for u in units(cv, state, times) if u.prio == 6]
                lines_wide = [([to_screen(WIDE, p) for p in pts_], 2.0, kind, None)
                              for pts_, kind in qc if kind != "border"] + key_lines(key_here)
                discs_w = [to_screen(WIDE, P(ALL[k].lat, ALL[k].lon))
                           for k in list(state["allotted"]) + new_keys]

                def off_discs(u, cand, rs, lead, centre, discs_w=discs_w):
                    return (["lot-disc"] if any(circle_hits_rect(xy, DISC_PX / 2 + 2, r)
                                                for xy in discs_w for r in rs) else [])
                ctx_w = Ctx(PROJ, WIDE, lines_wide, [], hud_w, (), {},
                            [to_screen(WIDE, P(a, b)) for a, b in LAND_RING], extra=off_discs)
                placed, dropped_w, problems_w = layout(U_w, ctx_w, None)
                unforce(placed, problems_w, WIDE, [], hud_w)
                problems += problems_w
                cur_ident = identities(placed, WIDE)
                for u in U_w:
                    u.t_in = round(t_land - 0.4, 2)
                lab = emit_labels(PROJ, U_w, placed, cur_ident, None, False, cam_own, WIDE,
                                  fl, t_land, hud_w, lambda cam, cv=cv: hud_rects(cv, cam),
                                  [], problems)
        # 18:6 "here": a ring goes out once from Shiloh's dot as it's said
        if cv in SAID_AS:
            key, word = SAID_AS[cv]
            xy = to_screen(cam1, P(ALL[key].lat, ALL[key].lon))
            u = next(u for u in placed if u.key == key)
            gap = min(max(r[0] - xy[0], xy[0] - r[2], r[1] - xy[1], xy[1] - r[3])
                      for r in u.rest_rects)
            overlay.append(screen_ring(xy, heard_at(word_time(cv, word), t_land, late),
                                       6, max(9, round(gap - 3)), 1.2, HL))

        # ------ assemble -------------------------------------------------
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
               f'height="{H}" font-family="{FONT_FAMILY}">',
               f'<rect width="{W}" height="{H}" fill="{rgb(BG)}"/>',
               fl.open_camera()]
        if show_map:
            if show_card:
                # the map is switched off while the card fills the frame
                vis = ["hidden" if z >= CARD_COVER else "visible" for z in zs]
                svg.append(f'<g visibility="{vis[0]}">' + discrete(fl, "visibility", vis))
            svg += fills
            for name in ("discs", "w1", "w2", "riv", "walk_old", "walk_tribe", "dots", "survey",
                         "walk_cur", "walk_lift"):
                svg.append(emit_class(fl, name, cls[name]))
            if two:
                svg.append(f'<g>{fade(t_rise, 0.5, out=True)}'
                           + "".join(emit_label_layers(fl_own, lab_own)) + "</g>")
            if lab is not None:
                svg += emit_label_layers(fl, lab)
            elif held:
                svg += held_labels(fl, held, PROJ)
            svg.append(key_svg(fl, state["key"], key_new, t_key, altar))
            if show_card:
                svg.append("</g>")
        if show_card:
            ops = [f"{card_op(z):.2f}" for z in zs]
            for shown in show_card:
                svg.append(f'<g opacity="{ops[0]}">{fl._anim("opacity", ops)}'
                           + shown.svg(cv, fl, 18, TEXT, HL) + "</g>")
        svg.append("</g></g>")
        if show_map:
            svg += overlay
        svg.append(title_svg(title(cv), TEXT))
        heard = {}
        for n, t in zip(verse.names, times):
            if n.kind == AL.UNPLACED and t is not None:
                heard.setdefault(n.web, t)
        svg.append(plate_svg(cv, prev_cv, heard if CLOCKS[cv] else None, late))
        if show_card:
            svg.append(card_hud(fl, zs, cv))
        else:
            svg.append(map_hud(fl, cv))
        svg.append(inset_svg(fl, state, [(k, col, t_new[k]) for k in new_keys],
                             bool(show_card)))
        svg.append("</svg>")
        text = "".join(svg)
        with open(out_path(BOOK, c, f"{BOOK}_{c}_{v}.svg"), "w", encoding="utf-8") as f:
            f.write(text)

        # ------ QC -------------------------------------------------------
        if two:
            mid = midflight_qc(fl_own, placed_own, lab_own["exiting"])
        else:
            mid = midflight_qc(fl, placed, lab["exiting"]) if lab is not None else []
        end = max(ends + card_ends(cv, show_card)
                  + [getattr(u, "t_show", 0) + 0.5 for u in placed
                     if getattr(u, "t_show", 0) > 0] + [fl.dur])
        clk = CLOCKS[cv]
        report.append(dict(
            cv=cv, pxdeg=round(cam1[0] * K), end=round(end, 2), narr=narr,
            clock=(clk.matched, clk.marks) if clk else None,
            kb=round(len(text.encode()) / 1024, 1),
            dropped=[u.key for u in U if u.key in dropped and u.prio <= 3],
            problems=problems, mid=mid, ext=extent_check(fl, PROJ, (LAT_BOT - MARGIN, LAT_TOP + MARGIN),
                                                         (LON_L - MARGIN, LON_R + MARGIN)),
            card=card_extent(fl, show_card, S_CARD) if show_card else None,
            squeezed=squeezed))

        # ------ what the next verse inherits ----------------------------
        for k in new_keys:
            state["allotted"][k] = col
            state["lots"].setdefault(lot, []).append(k)
        if col:
            state["walks"] += [[col, lg, "walk_cur", lot] for lg in legs]
            last_lot = lot
        state["walk_end"] = walk_end(cv, state["walk_end"])
        state["lifted"] = lifted
        if key_new:
            state["key"].append(key_new)
        if lab is not None:
            prev = prev_state(cam1, placed, cur_ident, lab["cur_dots"])
            last_lab = cv
            cam_prev = cam1
        prev_cv = cv
        prev_col = col
        last_cam = cam1
    return report


def lift_els(key, state):
    """A lot lit: its discs again over themselves, and its walked borders in
    its colour, as (class, element) pairs."""
    col = LOT_COL[key]
    out = [("discs", disc(k, col)) for k in state["lots"].get(key, [])]
    out += [("walk_lift", poly_el(PS(w[1]), stroke=col))
            for w in state["walks"] if w[3] == key]
    return out


def map_hud(fl, cv):
    """The compass and scale over a map verse; the bar fades while it would
    run longer than at any rest (a rise from a close frame to the land)."""
    bar = [SCALE_OF[cv] / 111.0 * K * cm[0] for cm in fl.cams]
    ops = [max(0.0, min(1.0, (1.5 * SCALE_MAX_PX - b) / (0.5 * SCALE_MAX_PX))) for b in bar]
    if min(ops) >= 1.0:
        return compass_scale_svg(fl, PROJ, SCALE_OF[cv])
    tags = [f"{o:.2f}" for o in ops]
    return (f'<g opacity="{tags[0]}">{fl._anim("opacity", tags)}'
            + compass_scale_svg(fl, PROJ, SCALE_OF[cv]) + "</g>")


def card_hud(fl, zs, cv):
    """The compass and scale over a verse that goes into the card: they fade
    as the card comes in, and the bar stops following the camera once it
    does."""
    capped = Flight(fl.cam0, [])
    capped.cams = [(min(cm[0], CAP_S), cm[1], cm[2]) for cm in fl.cams]
    # and it waits while the bar would run longer than at any rest
    bar = [SCALE_OF[cv] / 111.0 * K * cm[0] for cm in capped.cams]
    ops = [f"{(1.0 - card_op(z)) * max(0.0, min(1.0, (1.5 * SCALE_MAX_PX - b) / (0.5 * SCALE_MAX_PX))):.2f}"
           for z, b in zip(zs, bar)]
    if max(float(o) for o in ops) <= 0:
        return ""
    capped.static, capped.pure_pan, capped.dur = fl.static, fl.pure_pan, fl.dur
    return (f'<g opacity="{ops[0]}">{fl._anim("opacity", ops)}'
            + compass_scale_svg(capped, PROJ, SCALE_OF[cv]) + "</g>")


def main():
    report = build_all()
    for r in report:
        notes = []
        if r["dropped"]:
            notes.append("dropped " + ", ".join(r["dropped"]))
        for k, why in r["problems"]:
            notes.append(f"FORCED {k}: {', '.join(why)}")
        for a, b, t0, t1 in r["mid"]:
            notes.append(f"mid-flight overlap {a} x {b} at {t0}-{t1}s")
        if r["end"] > r["narr"] - 0.2:
            notes.append(f"LATE: lands at {r['end']}s, narration {r['narr']}s")
        if r["ext"]:
            notes.append("WORLD EDGE visible")
        if r["card"]:
            notes.append(r["card"])
        if r.get("squeezed"):
            notes.append("closing: its own names stand less than DWELL before the rise")
        for n in notes:
            print(f"  {r['cv'][0]}:{r['cv'][1]}: {n}")
    for prob in key_qc():
        print(f"  key: {prob}")
    for card, mod in CARDS:
        for prob in (mod.qc(card) if hasattr(mod, "qc") else []):
            print(f"  card {card.key}: {prob}")
    missing = sum(1 for cv in REFS if _narration(*cv) is None)
    if missing:
        print(f"  {missing} verses have no MP3: paced on an estimate from their words")
    clocks = [r["clock"] for r in report if r["clock"]]
    whole = sum(1 for m, b in clocks if m == b)
    print(f"Narration clock: {len(clocks)} verses timed, a pause at every mark in {whole}")
    kb = [r["kb"] for r in report]
    print(f"Joshua 13-19: {len(report)} SVG files, {sum(kb):.0f} KB (largest {max(kb)} KB)")


if __name__ == "__main__":
    main()
