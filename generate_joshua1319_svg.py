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

The camera times itself to each verse's MP3, so re-run this whenever one
is re-rendered. A verse with no MP3 is paced on an estimate from its words.

    .venv\\Scripts\\python.exe generate_joshua1319_svg.py
It prints any name it had to drop or force, and anything that would land
after the narration.
"""

import os
import re
from xml.sax.saxutils import escape

import acts_geography as G
import mediterranean as M
import allotment as AL
import gazetteer as GZ
import narration_clock
from config import WEB_AUDIO_DIR
from generate_israel_atlas import TEXT_WEB
from generate_tabernacle import (BG, H, HL, SAND, SAND_DIM, TEXT, TEXT_DIM, W,
                                 out_path)
from generate_tribal_maps import LAND, RIVER, SEA, TRIBE_COL, WATER_TXT
from passages import verse_numbers
from svg_chronicles_world import AUDIO_SLACK, _mp3_seconds
from svg_map_camera import (
    Ctx, Flight, Projection, SAFE, dot_state, S_AREA, S_CUR, S_OTHER,
    Unit as MapUnit, _same, cam_duration, compass_rect, compass_scale_svg,
    emit_class as emit_px, emit_label_layers, emit_labels, extent_check, fade,
    identities, ink, inset_view_rect, layout, midflight_qc, op_anim, poly_el, prev_state,
    rest_dots, rgb, title_rect, title_svg, to_screen, unchanged,
)
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
# brown and Ephraim's green, which face them across the river
LOT_COL = dict(TRIBE_COL, REUBEN=(190, 100, 128), GAD=(80, 178, 196))


def tribe_col(tribe, c):
    """The colour of a tribe's lot (Manasseh's half by its chapter)."""
    if not tribe or tribe == "Levi":
        return None
    if tribe == "Manasseh":
        return LOT_COL["MANASSEH_E" if c == 13 else "MANASSEH_W"]
    return LOT_COL[tribe.upper()]


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
    cur = {u.key for u in U}
    # the lot so far: its places named in earlier verses, dim
    if col:
        for key in state["by_col"].get(col, []):
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


def scale_km(fl):
    """The longest round scale bar that stays short at the rest camera."""
    for km in SCALE_KMS:
        if km / 111.0 * K * fl.cam1[0] <= SCALE_MAX_PX:
            return km
    return SCALE_KMS[-1]

INSET_RECT = (14, H - 14 - 168, 14 + 118, H - 14)
INSET_BOX = (30.30, 34.45, 33.80, 36.85)       # lat0, lat1, lon0, lon1
INSET_OFF, INSET_RAMP = 0.80, 0.07
PLATE_W = 300
FS_PLATE = 16


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
    then a fade), so a browser that doesn't animate a tspan shows it."""
    r = plate_rect(cv)
    out = [f'<rect x="{_fmt(r[0])}" y="{_fmt(r[1])}" width="{_fmt(r[2] - r[0])}" '
           f'height="{_fmt(r[3] - r[1])}" rx="8" fill="{rgb(BG)}" fill-opacity="0.82"/>',
           f'<text x="{W - 18}" y="{r[1] + 10}" font-size="{FS_PLATE}" font-style="italic" '
           f'fill="{rgb(TEXT_DIM)}" text-anchor="end" dominant-baseline="text-before-edge">'
           f'not located</text>']
    for i, row in enumerate(plate_rows(cv)):
        spans = []
        for j, nm in enumerate(row):
            s = escape((" · " if j else "") + nm)
            spans.append(s if shown is None else
                         f'<tspan><set attributeName="fill-opacity" to="0" begin="0s"/>'
                         f'{op_anim(0, 1, shown[nm], NAME_FADE)}{s}</tspan>')
        out.append(f'<text x="{W - 18}" y="{r[1] + 10 + 22 * (i + 1)}" font-size="{FS_PLATE}" '
                   f'fill="{rgb(TEXT)}" text-anchor="end" '
                   f'dominant-baseline="text-before-edge">{"".join(spans)}</text>')
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


def inset_svg(fl, state, coming=()):
    x0, y0, x1, y1 = INSET_RECT
    ops = [f"{inset_opacity(c):.2f}" for c in fl.cams]
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
          "walk_cur": 3.6, "dots": 5.0, "discs": DISC_PX}
DOTTED = (0.1, 7.0)
LET_GO = 0.8
WALK_STROKE = {"walk_old": SAND_DIM, "walk_tribe": SAND, "walk_cur": HL}
WALK_ORDER = ("walk_old", "walk_tribe", "walk_cur")     # bottom to top


def emit_class(fl, name, els):
    dash = DOTTED if name.startswith("walk") else None
    extra = ' stroke-linecap="round"' if name.startswith("walk") or name in ("dots", "discs") else ""
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
    # state["walks"]: [colour, leg, the class it ended the last verse in]
    state = {"allotted": {}, "by_col": {}, "walks": [], "walk_end": None}
    prev, prev_cv, prev_col, report = None, None, None, []
    last_col = None               # the last tribe's: a verse with no tribe keeps its walks up
    cam_prev = WIDE
    for cv in REFS:
        c, v = cv
        verse = AL.VERSES[cv]
        col = tribe_col(verse.tribe, c)
        narr = NARR[cv]
        times = said(cv)
        late = narr - AUDIO_SLACK - NAME_FADE      # the last a name may start to come in
        legs_t = walk_legs(cv, state["walk_end"], times)
        legs = [lg for lg, _t in legs_t]
        named = [point(n) for n in verse.names if n.kind in (AL.SITE, AL.WATER, AL.REGION)]
        own = [p for lg in legs for p in lg
               if not (verse.cont and p == state["walk_end"])]
        pts = named + own
        if cv[0] == 13 and 4 <= v <= 6:
            cam1 = NORTH
        elif pts:
            cam1 = frame(pts, cv)
        elif col and state["by_col"].get(col):
            cam1 = frame([(ALL[k].lat, ALL[k].lon) for k in state["by_col"][col]], cv)
        elif cv == REFS[0] or (col and col != prev_col):
            cam1 = WIDE
        else:
            cam1 = cam_prev
        cam0 = WIDE if prev is None else prev["cam1"]
        D = cam_duration(cam0, cam1)
        if D:
            D = round(max(0.9, min(D, narr - AUDIO_SLACK - NEED_AFTER)), 2)
        fl = Flight(cam0, [("to", cam1, D)])
        assert _same(fl.cam1, cam1), cv
        t_land = fl.dur
        SCALE_OF[cv] = scale_km(fl)

        # the places this verse gives its tribe, each as it's said
        new_keys = []
        if col and verse.kind in ("towns", "border"):
            for n in verse.names:
                if (n.kind == AL.SITE and n.key not in state["allotted"]
                        and n.key in GZ.SITES and n.key not in new_keys
                        and (verse.tribe in GZ.SITES[n.key].tribe
                             or (verse.kind == "towns" and not GZ.SITES[n.key].tribe))):
                    new_keys.append(n.key)
        key_said = {}
        for n, t in zip(verse.names, times):
            if n.kind == AL.SITE and t is not None:
                key_said.setdefault(n.key, t)
        t_new = {k: heard_at(key_said.get(k), t_land, narr - AUDIO_SLACK - DISC_FADE, 0.1)
                 for k in new_keys}

        # ------ the world ------------------------------------------------
        cls = {k: [] for k in CLS_PX}
        qc = []
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
            wcol, lg, was = w
            w[2] = "walk_tribe" if wcol == (col or last_col) else "walk_old"
            for name, el in walk_el(lg, was, w[2], t_land).items():
                cls[name].append(el)
            qc.append((PS(lg), "border"))
        # this verse's walk, each leg as the landmark it reaches is said (or,
        # with no narration clock, evenly through the verse)
        walk_dur = max(0.0, narr - AUDIO_SLACK - t_land - 0.4)
        step = min(0.9, walk_dur / len(legs)) if legs else 0
        ends, t_prev = [t_land] + [t + DISC_FADE for t in t_new.values()], None
        for i, (lg, ts) in enumerate(legs_t):
            t = (heard_at(ts, t_land, late, 0.1) if ts is not None
                 else round(t_land + 0.1 + i * step, 2))
            if t_prev is not None:
                # one after another, and none past the narration's end
                t = round(min(max(t, t_prev + LEG_GAP), max(t, late)), 2)
            t_prev = t
            cls["walk_cur"].append(
                f'<g opacity="0">{fade(t, LEG_FADE)}'
                + poly_el(PS(lg), stroke=HL) + "</g>")
            ends.append(t + LEG_FADE)
            qc.append((PS(lg), "border"))
        # the other tribes' places, as small dots
        cur_named = {n.key for n in verse.names if n.kind == AL.SITE}
        for k, cl in state["allotted"].items():
            if k not in cur_named:
                x, y = P(ALL[k].lat, ALL[k].lon)
                cls["dots"].append(f'<path d="M{_fmt(x)} {_fmt(y)}h0" stroke="{rgb(cl)}"/>')

        # ------ labels ---------------------------------------------------
        hud = hud_rects(cv, cam1)
        # the lot's earlier places are named only where their dot rests clear
        # of the frame's edge and the plates
        U = [u for u in units(cv, state, times) if u.prio < 4 or
             dot_state(to_screen(cam1, P(*u.cands[0][:2])), hud) == "in"]
        lines = [([to_screen(cam1, p) for p in pts_], 3.0 if kind == "border" else 2.0, kind, None)
                 for pts_, kind in qc]
        lines_w = [(pts_, 3.0 if kind == "border" else 2.0) for pts_, kind in qc]
        dots = rest_dots(PROJ, U, cam1, hud)
        land = [to_screen(cam1, P(a, b)) for a, b in LAND_RING]
        ctx = Ctx(PROJ, cam1, lines, dots, hud, (), {}, land)
        placed, dropped, problems = layout(U, ctx, prev)
        unforce(placed, problems, cam1, dots, hud)
        prev_units = prev["units"] if prev else {}
        cur_ident = identities(placed, cam1)
        for u in U:
            u.t_in = None
            if unchanged(u, cur_ident, prev_units):
                continue
            if u.new:
                u.t_in = heard_at(getattr(u, "said", None), t_land, late)
        lab = emit_labels(PROJ, U, placed, cur_ident, prev, prev is not None, cam0, cam1, fl,
                          t_land, hud, lambda cam, cv=cv: hud_rects(cv, cam), lines_w,
                          problems)

        # ------ assemble -------------------------------------------------
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
               f'height="{H}" font-family="{FONT_FAMILY}">',
               f'<rect width="{W}" height="{H}" fill="{rgb(BG)}"/>',
               fl.open_camera()]
        svg += fills
        for name in ("discs", "w1", "w2", "riv", "walk_old", "walk_tribe", "dots", "walk_cur"):
            svg.append(emit_class(fl, name, cls[name]))
        svg += emit_label_layers(fl, lab)
        svg.append("</g></g>")
        svg.append(title_svg(title(cv), TEXT))
        heard = {}
        for n, t in zip(verse.names, times):
            if n.kind == AL.UNPLACED and t is not None:
                heard.setdefault(n.web, t)
        svg.append(plate_svg(cv, prev_cv, heard if CLOCKS[cv] else None, late))
        svg.append(compass_scale_svg(fl, PROJ, SCALE_OF[cv]))
        svg.append(inset_svg(fl, state, [(k, col, t_new[k]) for k in new_keys]))
        svg.append("</svg>")
        text = "".join(svg)
        with open(out_path(BOOK, c, f"{BOOK}_{c}_{v}.svg"), "w", encoding="utf-8") as f:
            f.write(text)

        # ------ QC -------------------------------------------------------
        mid = midflight_qc(fl, placed, lab["exiting"])
        end = max(ends + [getattr(u, "t_show", 0) + 0.5 for u in placed
                          if getattr(u, "t_show", 0) > 0] + [fl.dur])
        clk = CLOCKS[cv]
        report.append(dict(
            cv=cv, pxdeg=round(cam1[0] * K), end=round(end, 2), narr=narr,
            clock=(clk.matched, clk.marks) if clk else None,
            kb=round(len(text.encode()) / 1024, 1),
            dropped=[u.key for u in U if u.key in dropped and u.prio <= 3],
            problems=problems, mid=mid, ext=extent_check(fl, PROJ, (LAT_BOT - MARGIN, LAT_TOP + MARGIN),
                                                         (LON_L - MARGIN, LON_R + MARGIN))))

        # ------ what the next verse inherits ----------------------------
        for k in new_keys:
            state["allotted"][k] = col
            state["by_col"].setdefault(col, []).append(k)
        if col:
            state["walks"] += [[col, lg, "walk_cur"] for lg in legs]
            last_col = col
        state["walk_end"] = walk_end(cv, state["walk_end"])
        prev = prev_state(cam1, placed, cur_ident, lab["cur_dots"])
        prev_cv = cv
        prev_col = col
        cam_prev = cam1
    return report


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
        for n in notes:
            print(f"  {r['cv'][0]}:{r['cv'][1]}: {n}")
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
