"""Leviticus 1-7 workbench: the dock (the offerings table's working column)
and the file view (the real table, into which a column is filed).

The dock (bench.DOCK, 686, 8, 330, 560): five tabs over one column panel.
Each offering has its own column, laid out to its own content from the
reference's own words (offerings.py through generate_leviticus17_svg's
table_units and _entries_rows, which follow the reference's entries(),
ranks() and wrap()), with the reference's icons (draw_thing): the header (the
WEB name, 18 px bold), then BROUGHT, ON THE ALTAR, THE BLOOD, WHO EATS and
NOT EATEN, labels 11 px bold caps in a 66 px gutter, entries 14 px, who-lines
12 px italic. BROUGHT's icon rows spread into what room the column has
left (THING_ROW apart at most), and an icon is as tall as its row lets it be
under the name above it. There is no WHEN row (those cells lift in the 7:37 file view).
Every unit not yet lit is a placeholder bar. Every dock slot belongs to one
table unit id (generate_leviticus17_svg.table_units(): "burnt.blood:around
the altar", "sin.who:a ruler", "sin.rank3", "sin.icon3:lamb",
"meal.thing:oil", "<off>.head", "<off>.by", an entry's "/who"), so a section
lights the same ids the table has. The sin column fits by putting its ranks'
icons in the gutter under BROUGHT and, where a who-line fits, on its
entry's line.

API (T is global, from bench.cue):

    active(T)                  the offering whose column shows at T
    switch(off, T, head=True, name=True)
                               the column crossfades to `off` (0.6 s); its tab
                               is named (0.9 s later, with its header unit, the
                               first time) or the highlight moves; no-op if it
                               shows already. name=False: the column only, the
                               tab left veiled (sin's column must show from 4:3's
                               "anointed priest", but "sin offering" is said at
                               9.48). Returns when it's done.
    name(off, T, head=True)    the tab named (and highlighted) with its header unit
    light(unit, T, link=(), group=None, who=None, steady_out=None)
                               a unit's veil lifts in place with one pulse (and its
                               who-line, unless REACH holds it to a later verse;
                               who=False never, who=True always); `link` is
                               [(region, points, closed)] outlines pulsed in the
                               same group (the bench figure it names). Already
                               lit: a steady outline instead ("current again")
                               until steady_out (default 1.8 s, within the file).
                               Returns "lit" or "steady".
    fly(s, src, unit, T_up, T_go=None, who=None, lead=None)
                               a 14 px chip lifts off at src (its text's left-
                               middle, bench or strip px) at T_up, glides on a
                               shallow arc to the unit's slot (from T_go, default
                               T_up + 0.3) and the unit's veil lifts as it lands;
                               `lead` (x, y) ties a chip that starts clear of its
                               thing to it with a leader until it goes.
                               Already lit: no flight, a steady outline (returns
                               None). Returns the landing T. Raises if it would
                               land after the file's limit.
    steady(unit, T, T_out)     a steady outline round the unit
    pulse(unit, T, group=None) one pulse round the unit
    case_outline(units, T, T_out=None)   the current case: a steady outline round
                               those units (BROUGHT's icons), kept under the
                               words of the row above; returns its El (give it
                               an "out" when the case ends)
    current(unit, T, link=(), group=None, how="pulse")
                               a unit named again: lit, one pulse (or a steady
                               outline, how="steady"), with the link pulses;
                               not lit yet, it lights
    forgiven(off, T)           the "forgiven" chip at the header's right (sin,
                               trespass); again: a pulse that fits the file
    column_pulse(off, T)       one pulse round the whole column ("<off>.col")
    unit_box(unit, who=True)   the unit's screen box in the dock
    slot_xy(unit)              where its text starts (a flight's landing)
    lit(unit, T)               lit before T (bench.is_lit)

    file_view(off, T_in, T_back=None, hold=1.2, glide_at=None, glide_dur=1.4,
              back_dur=1.0, low=30) -> FileView
        The workshop crossfades (0.8 s) to the reference's own table
        (draw_offerings at FV_S 0.44, the units not lit before T_in under
        bars, readable keys over its column names and row labels); the dock's
        live column (a <use> of it) glides into `off`'s slot from glide_at
        (default T_in + 0.8; glide_dur s) and becomes the real column. It
        takes the low road: `low` px down and across to under its slot,
        shrinking to the slot's width, then up into it (low=0: straight, full
        size for the first half). The keys are drawn under the gliding
        column, and `off`'s own key comes in only as it lands, so its words
        never meet a key. It holds at least `hold` s after landing; at T_back
        the workshop crossfades back (back_dur s). T_back None: it stays
        (7:37). The table is a `cover`: a file it covers whole leaves out
        what is under it (bench.render_file). Use P.case_clear(T_in, group="fileview") to clear the bench
        under the crossfade. The handle: .t_glide, .t_land, .lift(unit, T)
        (a table unit's veil lifts in the view: the WHEN cells at 7:37),
        .pulse_column(off, T), .xy(wx, wy) (table world -> screen).
"""

import re

import generate_leviticus17_svg as G
import generate_tabernacle_reference as R
import leviticus17_bench as B
import offerings as OF
import sanctuary as SN
from generate_tabernacle import BG, HL, PANEL, SAND, SAND_DIM, TEXT, TEXT_DIM
from svg_vocab import mix

from svg_surface import _fmt
from leviticus17_bench import (El, add, f2, rgb, text, tbox, chip, LeanCanvas, pulse_el,
                               rect_pts, box_pts, arc_path, path_len, glide)

W, H = B.W, B.H
D_X0, D_Y0, D_W, D_H = B.DOCK
TAB_H = 28
COL_Y = D_Y0 + TAB_H + 2                # the column panel's top
COL_BOT = D_Y0 + D_H                    # its bottom
D_GUT = 66
D_EX = D_X0 + D_GUT + 12                # the entries' left edge
D_EW = D_X0 + D_W - 10 - D_EX           # their width
ENTRY, WHO_PX, LABEL_PX, HEAD_PX, ICON_NAME = 14, 12, 11, 18, 12
TAB_W = D_W / 5
SUB = R.SUB
SKELETON = G.SKELETON
FLIGHT_PEAK = 790                       # px/s, a chip flight's eased peak
ROWS = (("BROUGHT", "brought"), ("ON THE ALTAR", "burns"), ("THE BLOOD", "blood"),
        ("WHO EATS", "eaten"), ("NOT EATEN", "not_eaten"))
OFFER = {o.key: o for o in OF.OFFERINGS}
ORDER = [o.key for o in OF.OFFERINGS]
FORGIVEN_OFFS = ("sin", "trespass")


class Slot:
    """A dock slot: one line of a unit (its first line has the unit's id,
    more lines "<id>#1"...; a who-line "<id>/who")."""

    def __init__(self, key, kind, txt, x, y, size=ENTRY, italic=False, bold=False,
                 anchor="lm", thing=None, box=None, icon=None):
        self.key, self.kind, self.txt = key, kind, txt
        self.x, self.y, self.size, self.italic, self.bold = x, y, size, italic, bold
        self.anchor, self.thing, self.icon = anchor, thing, icon
        self.box = box or (tbox(txt, x, y, size, anchor, bold, italic) if txt else None)

    def text_box(self):
        if self.kind == "thing":
            return tbox(self.txt, self.x, self.y, ICON_NAME, "mm")
        if self.kind == "icon":
            return None
        return self.box


def _gutter_lines(lab):
    if R.wrap(lab, LABEL_PX, D_GUT - 6, bold=True) == [lab]:
        return [lab]
    w = lab.split(" ")
    return [" ".join(w[:-1]), w[-1]]


def _sin_groups(o):
    """The sin offering's BROUGHT as table_units groups it: [(i, things,
    whos, rank short)]."""
    groups = []
    for r in o.brought:
        for g in groups:
            if g[0] == (r.things, r.short):
                g[1].append(r.who)
                break
        else:
            groups.append([(r.things, r.short), [r.who]])
    return [(i, things, whos, short) for i, ((things, short), whos) in enumerate(groups, 1)]


MODES = [
    dict(gap=16, row=56, lh=17, wh=15, eg=5, inline=False, head=44),
    dict(gap=10, row=54, lh=17, wh=15, eg=5, inline=False, head=44),
    dict(gap=6, row=52, lh=17, wh=15, eg=5, inline=False, head=42),
    dict(gap=2, row=50, lh=17, wh=14, eg=4, inline=False, head=40),
    dict(gap=0, row=48, lh=16, wh=14, eg=3, inline=False, head=38),
    dict(gap=-2, row=46, lh=16, wh=13, eg=3, inline=False, head=36),
    dict(gap=0, row=46, lh=16, wh=13, eg=3, inline=True, head=36),
    dict(gap=-2, row=46, lh=16, wh=13, eg=2, inline=True, head=34),
    dict(gap=-3, row=44, lh=16, wh=13, eg=2, inline=True, head=32),
]


THING_ROW = 56                          # BROUGHT's icon rows, at most this far apart
ICON_H, ICON_GAP = 30, 3                # an icon's height; its clearance over the name above


def dock_layout(o):
    """(slots, skeleton, bottom, mode) for offering o: the roomiest mode
    that fits the column; what room is left spreads BROUGHT's icon rows
    (up to THING_ROW apart), so an icon clears the name above it."""
    for i, m in enumerate(MODES):
        slots, skel, y = _layout(o, m)
        if y <= COL_BOT - 6:
            break
    else:
        i = len(MODES) - 1
    rows = -(-len(OF.THINGS.get(o.key, ())) // 3) if o.by is not None else 0
    if rows > 1 and m["row"] < THING_ROW:
        bump = min((COL_BOT - 6 - y) // (rows - 1), THING_ROW - m["row"])
        if bump > 0:
            m = dict(m, row=m["row"] + bump)
            slots, skel, y = _layout(o, m)
    return slots, skel, y, i


def head_x(o):
    """The header's centre: left of the "forgiven" chip where there is one."""
    if o.key in FORGIVEN_OFFS:
        return D_X0 + (D_W - 84) / 2 + 4
    return D_X0 + D_W / 2


FORGIVEN_XY = (D_X0 + D_W - 46, None)


def _layout(o, m):
    slots, skel = {}, []
    units = G.table_units()
    lh, wh, eg = m["lh"], m["wh"], m["eg"]
    y = COL_Y + m["head"] / 2 + 1
    slots[f"{o.key}.head"] = Slot(f"{o.key}.head", "head", o.name, head_x(o), y, HEAD_PX,
                                  bold=True, anchor="mm")
    y = COL_Y + m["head"]
    for lab, field in ROWS:
        skel.append(("rule", y))
        top = y
        glines = _gutter_lines(lab)
        for i, ln in enumerate(glines):
            skel.append(("label", ln, D_X0 + 9, top + 14 + i * 13))
        if field == "brought" and o.by is None:
            y += 4
            for gi, things, whos, short in _sin_groups(o):
                g0 = y
                for who in whos:
                    key = f"{o.key}.who:{who}"
                    assert key in units, key
                    for j, ln in enumerate(R.wrap(who, ENTRY, D_EW)):
                        k_ = key if j == 0 else f"{key}#{j}"
                        slots[k_] = Slot(k_, "text", ln, D_EX, y + 7)
                        y += lh
                key = f"{o.key}.rank{gi}"
                assert key in units, key
                for j, ln in enumerate(R.wrap(short, WHO_PX, D_EW, italic=True)):
                    k_ = key if j == 0 else f"{key}#{j}"
                    slots[k_] = Slot(k_, "rank", ln, D_EX, y + 6, WHO_PX, italic=True)
                    y += wh
                # the rank's drawings in the gutter, under the row's label
                n = len(things)
                gx0, gx1 = D_X0 + 8, D_X0 + D_GUT + 4
                iw = (gx1 - gx0) / n
                ih = min(26, max(20, y - g0 - 6))
                ibot = max(g0 + 3 + ih, top + 24 + ih if gi == 1 else 0, (g0 + y) / 2 + ih / 2)
                for j, th in enumerate(things):
                    key = f"{o.key}.icon{gi}:{th}"
                    assert key in units, key
                    icx = gx0 + iw * (j + 0.5)
                    s_ = Slot(key, "icon", "", icx, ibot, thing=th,
                              box=(icx - iw / 2 + 1, ibot - ih - 2, icx + iw / 2 - 1, ibot + 2),
                              icon=(icx, ibot, iw - 4, ih))
                    slots[key] = s_
                y = max(y, ibot + 2) + eg + 1
            y += 2
        elif field == "brought":
            y += 14
            slots[f"{o.key}.by"] = Slot(f"{o.key}.by", "text", o.by_short, D_EX, y)
            y += 12
            things = OF.THINGS[o.key]
            per = 3
            sw = D_EW / per
            # the icons as tall as the rows let them be under the names above
            name_b = max(tbox(t.short or t.key, 0, 9, ICON_NAME, "mm")[3] for t in things)
            ih = min(ICON_H, m["row"] - 8 - name_b - ICON_GAP)
            for i, t in enumerate(things):
                r, k = divmod(i, per)
                tcx = D_EX + k * sw + sw / 2
                base = y + 40 + r * m["row"]
                key = f"{o.key}.thing:{t.key}"
                assert key in units, key
                nm = t.short or t.key
                s_ = Slot(key, "thing", nm, tcx, base + 9, ICON_NAME, anchor="mm", thing=t.key,
                          box=(tcx - sw / 2 + 3, base - 4 - ih, tcx + sw / 2 - 3, base + 17),
                          icon=(tcx, base - 8, round(52 * ih / ICON_H), ih))
                slots[key] = s_
            y += 40 + (-(-len(things) // per) - 1) * m["row"] + 22
        else:
            y += 14
            es = G._entries_rows(getattr(o, field), field != "not_eaten")
            shorts = [mm for mm, _s, _r in es]
            y += 2
            if not es:
                skel.append(("dash", D_EX, y + 7))
                y += lh
            for main, sub, _rs in es:
                key = f"{o.key}.{field}:{main}"
                if shorts.count(main) > 1:
                    key += f"|{sub}"
                assert key in units, key
                mains = R.wrap(main, ENTRY, D_EW)
                last_end = None
                for j, ln in enumerate(mains):
                    k_ = key if j == 0 else f"{key}#{j}"
                    slots[k_] = Slot(k_, "text", ln, D_EX, y + 7)
                    last_end = slots[k_].box[2]
                    y += lh
                if sub:
                    wkey = key + "/who"
                    assert wkey in units, wkey
                    ww = tbox(sub, 0, 0, WHO_PX, "lm", italic=True)
                    if m["inline"] and len(mains) == 1 and last_end + 10 + (ww[2] - ww[0]) <= D_EX + D_EW:
                        slots[wkey] = Slot(wkey, "who", sub, last_end + 10, y - lh + 7 + 1, WHO_PX,
                                           italic=True)
                    else:
                        for j, ln in enumerate(R.wrap(sub, WHO_PX, D_EW, italic=True)):
                            k_ = wkey + ("" if j == 0 else f"#{j}")
                            slots[k_] = Slot(k_, "who", ln, D_EX, y + 6, WHO_PX, italic=True)
                            y += wh
                y += eg
        y = max(y, top + 14 + 13 * (len(glines) - 1) + 12)
        y += m["gap"]
    return slots, skel, y


def slot_text_svg(s_):
    if s_.kind == "head":
        return text(s_.txt, s_.x, s_.y, s_.size, TEXT, "mm", bold=True)
    if s_.kind in ("who", "rank"):
        return text(s_.txt, s_.x, s_.y, s_.size, SUB, "lm", italic=True)
    if s_.kind in ("thing", "icon"):
        tcx, bot, bw, bh = s_.icon
        did = f"ic{int(bw)}x{int(bh)}_" + re.sub(r"\W", "_", s_.thing)
        if did not in B.DEFS:
            c = LeanCanvas(0.25)
            R.draw_thing(c, s_.thing, 0, 0, bw, bh)
            B.define(did, "".join(c._els))
        out = B.use(did, tcx, bot)
        if s_.kind == "thing":
            out += text(s_.txt, tcx, s_.y, ICON_NAME, TEXT, "mm")
        return out
    return text(s_.txt, s_.x, s_.y, s_.size, TEXT, "lm")


def slot_bar_svg(s_):
    def bar(x, y, w, h=9):
        return (f'<rect x="{f2(x)}" y="{f2(y - h / 2)}" width="{f2(max(12, w))}" height="{h}" '
                f'rx="{h / 2}" fill="{rgb(SKELETON)}"/>')
    if s_.kind == "thing":
        tcx, bot, bw, bh = s_.icon
        return bar(tcx - 18, bot + 2, 36, 9)
    if s_.kind == "icon":
        tcx, bot, bw, bh = s_.icon
        return bar(tcx - min(14, bw / 2 - 2), bot - bh / 2, min(28, bw - 4), 8)
    x0, _y0, x1, _y1 = s_.box
    if s_.kind == "head":
        return bar(s_.x - 60, s_.y, 120, 11)
    return bar(s_.x, s_.y, x1 - x0, 9 if s_.kind == "text" else 7)


def skel_svg(skel):
    out = []
    for item in skel:
        if item[0] == "rule":
            out.append(f'<line x1="{D_X0 + 8}" y1="{f2(item[1])}" x2="{D_X0 + D_W - 8}" '
                       f'y2="{f2(item[1])}" stroke="{rgb(mix(PANEL, SAND, .45))}" stroke-width="1"/>')
        elif item[0] == "label":
            out.append(text(item[1], item[2], item[3], LABEL_PX, SUB, "lm", bold=True))
        elif item[0] == "dash":
            out.append(text("—", item[1], item[2], ENTRY, SUB, "lm"))
    return "".join(out)


LAYOUT = {o.key: dock_layout(o) for o in OF.OFFERINGS}


def _check_units():
    """Every table unit but the WHEN cells has a dock slot (1:1)."""
    have = set()
    for off, (slots, _sk, _y, _m) in LAYOUT.items():
        for k in slots:
            have.add(k.split("#")[0])
    want = {k for k in G.table_units() if not k.endswith(".when")}
    missing = want - have
    extra = have - set(G.table_units())
    if missing or extra:
        raise AssertionError(f"dock units: missing {sorted(missing)}, extra {sorted(extra)}")


_check_units()


def tab_rect(i):
    return (D_X0 + i * TAB_W + 1, D_Y0, TAB_W - 2, TAB_H)


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

ACTIVE = []                     # [(T, off)]: the column showing from T
TAB_ON = []                     # [(T, off or None)]: the highlighted tab from T
NAMED = {}                      # off -> T its tab was named


def _last(lst, T):
    out = None
    for t, v in lst:
        if t <= T + 1e-6:
            out = v
    return out


def active(T):
    """The offering whose column shows at T."""
    return _last(ACTIVE, T)


def tab_on(T):
    return _last(TAB_ON, T)


def lit(unit, T):
    return B.is_lit(unit, T)


def unit_slots(unit):
    off = unit.split(".")[0]
    slots = LAYOUT[off][0]
    return [k for k in slots if k == unit or k.startswith(unit + "#")]


def unit_box(unit, who=True):
    off = unit.split(".")[0]
    slots = LAYOUT[off][0]
    ks = unit_slots(unit) + (unit_slots(unit + "/who") if who else [])
    if not ks:
        raise KeyError(f"no dock slot for {unit!r}")
    bs = [slots[k].box for k in ks]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs),
            max(b[3] for b in bs))


def slot_xy(unit):
    off = unit.split(".")[0]
    s_ = LAYOUT[off][0][unit_slots(unit)[0]]
    if s_.kind in ("thing", "icon"):
        b = s_.text_box() or s_.box
        return (b[0], (b[1] + b[3]) / 2)
    if s_.anchor == "mm":
        b = s_.box
        return (b[0], s_.y)
    return (s_.x, s_.y)


_N = {"n": 0}


def _uid(prefix):
    _N["n"] += 1
    return f"{prefix}{_N['n']}"


def _col(off):
    return f"col.{off}"


def _check_active(off, T, what):
    if active(T) != off:
        raise ValueError(f"{what}: the {off} column isn't showing at {B.local(T)} "
                         f"(the {active(T)} column is; dock.switch first)")


# ---------------------------------------------------------------------------
# Tabs and switching
# ---------------------------------------------------------------------------

def name_tab(off, T, dur=0.5, group="tab"):
    """The tab named and highlighted (the first time an offering is named)."""
    if off in NAMED and NAMED[off] < T - 1e-6:
        return
    B.ELS[f"tab.{off}.bar"].ev("out", T, 0.4, group=group)
    B.ELS[f"tab.{off}.active"].ev("in", T, dur, group=group)
    NAMED[off] = T
    TAB_ON.append((T, off))


def name(off, T, head=True, group="tab"):
    """The tab named and highlighted, with its header unit (the first time
    the offering is named: after a switch(..., name=False))."""
    _check_active(off, T, f"name {off}")
    on = tab_on(T)
    if on == off:
        return T
    if off in NAMED and NAMED[off] < T - 1e-6:
        B.ELS[f"tab.{off}.name"].ev("out", T, 0.6, group=group)
        B.ELS[f"tab.{off}.active"].ev("in", T, 0.6, group=group)
        TAB_ON.append((T, off))
        return T + 0.6
    name_tab(off, T, group=group)
    if head and not lit(f"{off}.head", T):
        light(f"{off}.head", T, group=group, pulse=False)
    return T + 0.6


def switch(off, T, head=True, dur=0.6, group="swap", name=True):
    """The dock's column crossfades to `off`; its tab named (0.9 s later,
    the first time, with its header) or its highlight moved. name=False:
    the column only, the tab left veiled (name it later with name(off, T)
    when the verse says it). Returns the T the switch is done."""
    cur = active(T)
    on = tab_on(T)
    if cur == off:
        if on != off and name:
            if off not in NAMED:
                name_tab(off, T, group=group)
                if head and not lit(f"{off}.head", T):
                    light(f"{off}.head", T, group=group, pulse=False)
            else:
                B.ELS[f"tab.{off}.name"].ev("out", T, dur, group=group)
                B.ELS[f"tab.{off}.active"].ev("in", T, dur, group=group)
                TAB_ON.append((T, off))
        return T + dur
    B.ELS[_col(cur)].ev("out", T, dur, group=group)
    B.ELS[_col(off)].ev("in", T, dur, group=group)
    ACTIVE.append((T, off))
    if on is not None:
        B.ELS[f"tab.{on}.active"].ev("out", T, dur, group=group)
        B.ELS[f"tab.{on}.name"].ev("in", T, dur, group=group)
        TAB_ON.append((T, None))
    if not name:
        return T + dur
    if off not in NAMED:
        t2 = T + 0.9
        name_tab(off, t2, group=group + ":name")
        if head and not lit(f"{off}.head", t2):
            light(f"{off}.head", t2, group=group + ":name", pulse=False)
        return t2 + 0.6
    B.ELS[f"tab.{off}.name"].ev("out", T, dur, group=group)
    B.ELS[f"tab.{off}.active"].ev("in", T, dur, group=group)
    TAB_ON.append((T, off))
    return T + dur


# ---------------------------------------------------------------------------
# Units: light, fly, steady, pulse
# ---------------------------------------------------------------------------

def _who_allowed(unit, T):
    w = unit + "/who"
    if w not in G.table_units():
        return False
    reach, _ex = B.reach_tables()
    at = reach.get(w)
    return not at or at <= B.verse_of(T + B.SAY_LEAD)


def _reveal(unit, T, dur, group):
    off = unit.split(".")[0]
    ks = unit_slots(unit)
    if not ks:
        raise KeyError(f"no dock slot for {unit!r}")
    for k in ks:
        B.ELS[f"col.{off}.bar.{k}"].ev("out", T, dur, group=group)
        B.ELS[f"col.{off}.txt.{k}"].ev("in", T, dur, group=group)
    B.mark_lit(unit, T, "unveil")


def light(unit, T, link=(), group=None, who=None, pulse=True, steady_out=None, dur=0.5):
    """A unit's veil lifts in place (with its who-line) and its outline
    pulses once; already lit, it takes a steady outline. See the module
    docstring."""
    off = unit.split(".")[0]
    _check_active(off, T, f"light {unit}")
    group = group or unit
    for region, pts, closed in link:
        pulse_el(_uid(f"link.{region}."), region, pts, T, closed=closed, group=group)
    if lit(unit, T):
        steady(unit, T, steady_out if steady_out is not None else T + 1.8, group=group)
        return "steady"
    _reveal(unit, T, dur, group)
    with_who = _who_allowed(unit, T) if who is None else who
    if with_who and not lit(unit + "/who", T):
        _reveal(unit + "/who", T, dur, group)
    tp = min(T + 0.45, B.file_limit(T) - 0.9)        # the pulse, if the file has room
    if pulse and tp >= T - 1e-6:
        x0, y0, x1, y1 = unit_box(unit, who=with_who)
        pulse_el(_uid(f"col.{off}.p"), "dock", rect_pts(x0 - 5, y0 - 3, x1 + 5, y1 + 3),
                 tp, group=group, parent=_col(off))
    return "lit"


def steady(unit, T, T_out, group=None):
    off = unit.split(".")[0]
    _check_active(off, T, f"steady {unit}")
    x0, y0, x1, y1 = unit_box(unit, who=lit(unit + "/who", T + 1e-3))
    T_out = min(T_out, B.file_limit(T) - 0.4)
    return B.steady_el(_uid(f"col.{off}.st"), "dock", rect_pts(x0 - 5, y0 - 3, x1 + 5, y1 + 3),
                       T, T_out, group=group or unit, parent=_col(off))


def pulse(unit, T, group=None):
    off = unit.split(".")[0]
    _check_active(off, T, f"pulse {unit}")
    x0, y0, x1, y1 = unit_box(unit, who=lit(unit + "/who", T + 1e-3))
    return pulse_el(_uid(f"col.{off}.p"), "dock", rect_pts(x0 - 5, y0 - 3, x1 + 5, y1 + 3), T,
                    group=group or unit, parent=_col(off))


def case_outline(units, T, T_out=None, pad=4, group=None, dur_in=0.35):
    """The current case: a steady outline round the units' boxes, its top
    kept under the words of the row above (BROUGHT's icon rows are close)."""
    off = units[0].split(".")[0]
    _check_active(off, T, "case outline")
    bs = [unit_box(u, who=False) for u in units]
    x0, y0 = min(b[0] for b in bs) - pad, min(b[1] for b in bs) - pad
    x1, y1 = max(b[2] for b in bs) + pad, max(b[3] for b in bs) + pad
    top = min(b[1] for b in bs)
    for o in LAYOUT[off][0].values():
        tb = o.text_box()
        if tb and tb[3] <= top + 1 and tb[0] < x1 and tb[2] > x0:
            y0 = max(y0, tb[3] + 2)
    pts = rect_pts(x0, y0, x1, y1)
    return B.steady_el(_uid(f"col.{off}.case"), "dock", pts, T, T_out, dur_in=dur_in,
                       group=group, parent=_col(off))


def forgiven(off, T, group="forgiven"):
    """The "forgiven" chip at the header's right; again, a pulse."""
    _check_active(off, T, "forgiven")
    key = f"col.{off}.forgiven"
    el = B.ELS[key]
    if el.state(T)[0]:
        dur = min(0.9, B.file_limit(T) - T)          # a pulse that fits the file
        if dur < 0.35:
            return None
        return pulse_el(_uid(f"col.{off}.fp"), "dock", box_pts(el.fbox, 2), T, dur=dur,
                        group=group, parent=_col(off))
    el.ev("in", T, B.fit(T, 0.5), group=group)
    tp = min(T + 0.3, B.file_limit(T) - 0.9)          # its pulse, if the file has room
    if tp >= T - 1e-6:
        pulse_el(_uid(f"col.{off}.fp"), "dock", box_pts(el.fbox, 2), tp, group=group,
                 parent=_col(off))
    return el


def current(unit, T, link=(), group=None, how="pulse", T_out=None):
    """A unit named again: lit already, one pulse round it (how="pulse") or a
    steady outline until T_out (how="steady"), with the link pulses; not lit
    yet, it lights (light)."""
    if not lit(unit, T):
        return light(unit, T, link=link, group=group)
    group = group or unit
    for region, pts, closed in link:
        pulse_el(_uid(f"link.{region}."), region, pts, T, closed=closed, group=group)
    if how == "steady":
        return steady(unit, T, T_out if T_out is not None else T + 1.8, group=group)
    return pulse(unit, T, group=group)


def column_pulse(off, T, group=None):
    _check_active(off, T, "column pulse")
    return pulse_el(_uid(f"col.{off}.cp"), "dock",
                    rect_pts(D_X0 + 3, COL_Y + 3, D_X0 + D_W - 3, COL_BOT - 3), T,
                    group=group or f"{off}.col", parent=_col(off))


def fly(s, src, unit, T_up, T_go=None, who=None, group=None, lead=None):
    """A chip lifts off the thing just built (src: its text's left-middle)
    and glides on a shallow arc to the unit's slot; the slot's veil lifts as
    it lands. `lead` (x, y): a leader ties the chip to that point until it
    goes (a chip that must start clear of its thing). Returns the landing T,
    or None when the unit is lit already (then a steady outline)."""
    off = unit.split(".")[0]
    if lit(unit, T_up):
        _check_active(off, T_up, f"fly {unit}")
        steady(unit, T_up, T_up + 1.8, group=group)
        return None
    dst = slot_xy(unit)
    svg, box = chip(s, src[0], src[1], 14, "lm")
    region = "strip" if src[1] < B.STRIP[1] + B.STRIP[3] else "bench"
    name = _uid("fly.")
    el = add(El(name, region, svg, z=95, texts=[(box, 14, "flight chip")]))
    rel = (dst[0] - src[0], dst[1] - src[1])
    path = arc_path((0, 0), rel)
    L = path_len(path, True)
    dur = max(0.8, L * B.EASE_PEAK / FLIGHT_PEAK)
    el.ev("in", T_up, 0.4 if T_go else 0.3, how="lift", lift=6, group=name)
    t_go = T_go if T_go is not None else T_up + 0.3
    if lead is not None:
        lsvg = chip(s, src[0], src[1], 14, "lm", lead)[0]
        lsvg = lsvg[:lsvg.index("<rect")]                # the leader alone
        ld = add(El(name + ".lead", region, lsvg, z=94))
        ld.ev("in", T_up, 0.3, group=name)
        ld.ev("out", max(t_go, T_up + 0.3), 0.2, group=name)
    glide(el, t_go, path, dur, f"{s}: to {unit}", "chip flight", quad=True, group=name)
    land = t_go + dur
    _check_active(off, land - 0.25, f"fly {unit}")
    el.ev("out", land - 0.22, 0.3, group=name)
    _reveal(unit, land - 0.25, 0.35, name)
    B.LIT_BY[unit] = "flight"
    with_who = _who_allowed(unit, land) if who is None else who
    if with_who and not lit(unit + "/who", land - 0.25):
        _reveal(unit + "/who", land - 0.25, 0.35, name)
    if land + 0.1 > B.file_limit(T_up) + 1e-6:
        raise ValueError(f"fly {unit}: lands at {B.local(land)}, after the file's limit")
    return land


# ---------------------------------------------------------------------------
# The file view
# ---------------------------------------------------------------------------

FV_S = 0.44
FV_TX, FV_TY = 83 - R.OFF_X * FV_S, 8 - G.TY * FV_S
FV_TEXTS = []                   # the readable keys' (box, size)


def fv_xy(wx, wy):
    return FV_TX + wx * FV_S, FV_TY + wy * FV_S


_FV_CACHE = {}


def _table_parts():
    """The reference's draw_offerings, split: (base, {unit: part}), each part
    a pair (shapes, texts): the shapes drawn in screen px already (FV_S
    applied, so their numbers are short), the texts in the table's own
    world px, to go under one scale transform (FileView.tr)."""
    if "parts" in _FV_CACHE:
        return _FV_CACHE["parts"]
    units = G.table_units()
    base, per_unit = ([], []), {}
    wy, wh = G.row_tops()["when"]
    flags = {SN.DERIVED, SN.NOT_GIVEN}

    def M(p):
        return fv_xy(*p)

    def dash_(d):
        return " ".join(_fmt(float(q) * FV_S) for q in d.replace(",", " ").split()) if d else d

    class UC(LeanCanvas):
        def _route(self, pts):
            if not pts:
                return None
            cx = sum(p[0] for p in pts) / len(pts)
            cy = sum(p[1] for p in pts) / len(pts)
            for u in units.values():
                x0, y0, x1, y1 = u.box
                if x0 <= cx <= x1 and y0 <= cy <= y1:
                    return u.key
            return None

        def _put(self, key, s, is_text=False):
            part = base if key is None else per_unit.setdefault(key, ([], []))
            part[1 if is_text else 0].append(s)

        def text(self, xy, s, size, fill, anchor="lm", bold=False, italic=False):
            if xy[1] < G.TY:                     # the reference page's heading
                return
            if italic and s in flags and wy <= xy[1] <= wy + wh:
                return                           # the WHEN cells' source flag
            n = len(self._els)
            super().text(xy, s, size, fill, anchor, bold, italic)
            self._put(self._route([xy]), self._els.pop(n), True)

        def polygon(self, points, fill=None, stroke=None, width=1):
            n = len(self._els)
            super().polygon([M(q) for q in points], fill, stroke, width * FV_S)
            self._put(self._route(list(points)), self._els.pop(n))

        def polyline(self, points, stroke, width=1, dash=None, closed=False, fill=None,
                     linejoin="round"):
            n = len(self._els)
            super().polyline([M(q) for q in points], stroke, width * FV_S, dash_(dash), closed,
                             fill, linejoin)
            self._put(self._route(list(points)), self._els.pop(n))

        def circle(self, cx, cy, r, fill=None, stroke=None, width=1):
            n = len(self._els)
            super().circle(*M((cx, cy)), r * FV_S, fill, stroke, width * FV_S)
            self._put(self._route([(cx, cy)]), self._els.pop(n))

        def rect(self, x, y, w, h, fill=None, stroke=None, width=1, rx=None):
            n = len(self._els)
            super().rect(*M((x, y)), w * FV_S, h * FV_S, fill, stroke, width * FV_S,
                         None if rx is None else rx * FV_S)
            base[0].append(self._els.pop(n))

        def line(self, p0, p1, stroke, width=1, dash=None, linecap="butt"):
            n = len(self._els)
            super().line(M(p0), M(p1), stroke, width * FV_S, dash_(dash), linecap)
            base[0].append(self._els.pop(n))

    c = UC(0.3)
    R.draw_offerings(c)
    _FV_CACHE["parts"] = (base, per_unit)
    return base, per_unit


def _compose(parts, tr, extra_texts=""):
    """Shapes, then one transformed group of texts (and veils)."""
    shapes = "".join(s for sh, _t in parts for s in sh)
    texts = "".join(s for _sh, tx in parts for s in tx) + extra_texts
    return shapes + (f"<g {tr}>{texts}</g>" if texts else "")


def _veil_svg(u):
    kind, m = G.veil_mark(u.box, u.anchor, ".thing:" in u.key or ".icon" in u.key)
    if kind == "disc":
        return m[:-2] + f' fill="{rgb(SKELETON)}"/>'
    bx, by, bw = m
    return (f'<rect x="{f2(bx)}" y="{f2(by - 4)}" width="{f2(bw)}" height="8" rx="4" '
            f'fill="{rgb(SKELETON)}"/>')


class FileView:
    def __init__(self, n, off, T_in, T_back, glide_at=None, glide_dur=1.4, back_dur=1.0):
        self.n, self.off, self.T_in, self.T_back = n, off, T_in, T_back
        self.t_glide = T_in + 0.8 if glide_at is None else glide_at
        self.glide_dur = glide_dur
        self.t_land = self.t_glide + glide_dur
        self.back_dur = back_dur
        self.lifts = {}
        self.tr = f'transform="translate({f2(FV_TX)} {f2(FV_TY)}) scale({FV_S})"'

    def xy(self, wx, wy):
        return fv_xy(wx, wy)

    def _later(self, key):
        return key in self.lifts

    def table_svg(self):
        base, per_unit = _table_parts()
        units = G.table_units()
        T = self.T_in
        shown, veils = [], []
        for k, u in units.items():
            if k in self.lifts:
                continue
            if B.LIT.get(k, 1e9) < T - 1e-6:
                if not (self.off and k.startswith(self.off + ".")):
                    shown.append(per_unit.get(k, ([], [])))
            elif not (self.off and k.startswith(self.off + ".") and B.LIT.get(k, 1e9) < self.t_land):
                veils.append(_veil_svg(u))
        return (f'<rect width="{W}" height="{H}" fill="{rgb(BG)}"/>'
                + _compose([base] + shown, self.tr, "".join(veils)))

    def column_svg(self):
        _base, per_unit = _table_parts()
        T = self.T_in
        ks = [k for k in G.table_units() if k.startswith(self.off + ".") and k not in self.lifts
              and B.LIT.get(k, 1e9) < T - 1e-6]
        return _compose([per_unit.get(k, ([], [])) for k in ks], self.tr)

    def lift(self, unit, T, dur=0.6, group=None):
        """A table unit's veil lifts in the view at T (the WHEN cells)."""
        u = G.table_units()[unit]
        _base, per_unit = _table_parts()
        self.lifts[unit] = T
        veil = add(El(f"fv{self.n}.veil.{unit}", "top", f'<g {self.tr}>{_veil_svg(u)}</g>', z=101))
        veil.ev("show", self.T_in, group="fileview")
        veil.ev("out", T, dur, group=group or "fvlift")
        cont = add(El(f"fv{self.n}.unit.{unit}", "top",
                      lambda: _compose([per_unit.get(unit, ([], []))], self.tr), z=101))
        cont.ev("in", T, dur, group=group or "fvlift")
        if self.T_back is not None:
            veil.ev("hide", self.T_back + self.back_dur)
            cont.ev("out", self.T_back, self.back_dur, group="fileview")
        B.mark_lit(unit, T, "file view")

    def pulse_column(self, off, T, group=None):
        x, y, w, h = R.offer_columns()[off]
        a, b = fv_xy(x + 3, y + 3), fv_xy(x + w - 3, y + h - 3)
        return pulse_el(f"fv{self.n}.cp.{off}.{_uid('')}", "top", rect_pts(a[0], a[1], b[0], b[1]),
                        T, group=group or "fvpulse", z=104)


def _keys_svg(T, off, own=False):
    """Readable keys over the table: the named columns' names (14 px bold)
    and the row names (11 px bold caps). own=True: only the key of `off`, the
    column being filed (it comes in as the column lands, so the gliding
    column's words never meet it); own=False: every other key."""
    units = G.table_units()
    cols = R.offer_columns()
    out, texts = [], []
    for o in OF.OFFERINGS:
        if own != (o.key == off):
            continue
        if not (B.LIT.get(f"{o.key}.head", 1e9) < T - 1e-6 or o.key == off):
            continue
        x0, y0, x1, y1 = units[f"{o.key}.head"].box
        cx_ = fv_xy((x0 + x1) / 2, 0)[0]
        sy0 = fv_xy(0, y0)[1]
        out.append(f'<rect x="{f2(fv_xy(x0, 0)[0] + 2)}" y="{f2(sy0)}" '
                   f'width="{f2((x1 - x0) * FV_S - 4)}" height="{f2((y1 - y0) * FV_S)}" '
                   f'fill="{rgb(PANEL)}"/>')
        nm = o.name if tbox(o.name, 0, 0, 14, "mm", True)[2] * 2 <= (x1 - x0) * FV_S - 6 else \
            {"peace": "peace offerings"}.get(o.key, o.name)
        out.append(text(nm, cx_, sy0 + 14, 14, TEXT, "mm", bold=True))
        out.append(text(R.OFFER_SUB[o.key], cx_, sy0 + 31, 11, SUB, "mm", italic=True))
        texts += [(tbox(nm, cx_, sy0 + 14, 14, "mm", True), 14),
                  (tbox(R.OFFER_SUB[o.key], cx_, sy0 + 31, 11, "mm", italic=True), 11)]
    if own:
        return "".join(out), texts
    gx0, gx1 = fv_xy(R.OFF_X, 0)[0] + 3, fv_xy(cols["burnt"][0], 0)[0] - 3
    y = G.TY + R.OFF_HEAD
    for lab, _sub, _kind, _content, rh in R.OFF_ROWS:
        top = fv_xy(0, y)[1]
        if R.wrap(lab, LABEL_PX, gx1 - gx0 - 8, bold=True) == [lab]:
            lines = [lab]
        else:
            lines = [" ".join(lab.split(" ")[:-1]), lab.split(" ")[-1]]
        out.append(f'<rect x="{f2(gx0)}" y="{f2(top + 3)}" width="{f2(gx1 - gx0)}" '
                   f'height="{f2(min(rh * FV_S - 5, 32))}" fill="{rgb(PANEL)}"/>')
        for i, ln in enumerate(lines):
            out.append(text(ln, gx0 + 4, top + 13 + i * 13, LABEL_PX, SUB, "lm", bold=True))
            texts.append((tbox(ln, gx0 + 4, top + 13 + i * 13, LABEL_PX, "lm", True), LABEL_PX))
        y += rh
    return "".join(out), texts


KEYS_Z, GLIDE_Z = 101.5, 102            # the keys under the gliding column


def file_view(off, T_in, T_back=None, hold=1.2, glide_at=None, glide_dur=1.4, back_dur=1.0,
              low=30):
    """See the module docstring."""
    n = len(B.FILE_VIEWS) + 1
    fv = FileView(n, off, T_in, T_back, glide_at, glide_dur, back_dur)
    if fv.t_glide < T_in + 0.8 - 1e-6:
        raise ValueError(f"file view {off}: the glide begins before the table is in")
    if T_back is not None and T_back < fv.t_land + hold - 1e-6:
        raise ValueError(f"file view {off}: back at {B.local(T_back)}, before the land "
                         f"{B.local(fv.t_land)} + hold {hold}")
    if off:
        _check_active(off, T_in, f"file view {off}")
    B.FILE_VIEWS.append((T_in, off, B.OWNER))
    tab = add(El(f"fv{n}.table", "top", fv.table_svg, z=100))
    tab.cover = True                    # opaque, full frame: what is under it is hidden
    tab.ev("in", T_in, 0.8, group="fileview")
    ktexts = _keys_svg(T_in, off)[1]
    kk = add(El(f"fv{n}.keys", "top", lambda: _keys_svg(T_in, off)[0], z=KEYS_Z,
                texts=[(b, size, "file view key") for b, size in ktexts]))
    kk.ev("in", T_in, 0.8, group="fileview")
    FV_TEXTS.extend(ktexts)
    fv.key_els = [kk]
    if T_back is not None:
        tab.ev("out", T_back, back_dur, group="fileview")
        kk.ev("out", T_back, back_dur, group="fileview")
    if off:
        lit_el = add(El(f"fv{n}.lit", "top", fv.column_svg, z=101))
        lit_el.ev("in", fv.t_land, 0.5, group="fileview")
        # the filed column's own key, veiled until the column lands on it
        otexts = _keys_svg(T_in, off, own=True)[1]
        ok = add(El(f"fv{n}.ownkey", "top", lambda: _keys_svg(T_in, off, own=True)[0], z=KEYS_Z,
                    hidden0=True, texts=[(b, size, "file view key") for b, size in otexts]))
        ok.ev("in", fv.t_land, 0.5, group="fileview")
        FV_TEXTS.extend(otexts)
        fv.key_els.append(ok)
        if T_back is not None:
            lit_el.ev("out", T_back, back_dur, group="fileview")
            ok.ev("out", T_back, back_dur, group="fileview")
        cx_, cy_, cw_, ch_ = R.offer_columns()[off]
        k = cw_ * FV_S / D_W
        snap = (f'<rect x="{D_X0}" y="{COL_Y}" width="{D_W}" height="{COL_BOT - COL_Y}" rx="10" '
                f'fill="{rgb(PANEL)}" stroke="{rgb(SAND_DIM)}" stroke-width="2"/><use href="#dockcol"/>')
        gl = add(El(f"fv{n}.glide", "top", snap, z=GLIDE_Z, hidden0=True))
        gl.ev("show", T_in, group="fileview")
        to = fv_xy(cx_, cy_)
        kw = {"from": (D_X0, COL_Y), "to": to, "k": round(k, 4)}
        if low:
            # the low road: the column slides `low` px down and across to
            # under its slot, shrinking to the slot's width as it goes, then
            # rises into it, so it passes under the keys of the columns it
            # crosses (and is no wider than its slot when it reaches them)
            via = (to[0], max(COL_Y, to[1]) + low)
            L1 = ((via[0] - D_X0) ** 2 + (via[1] - COL_Y) ** 2) ** 0.5
            L2 = ((to[0] - via[0]) ** 2 + (to[1] - via[1]) ** 2) ** 0.5
            f = round(L1 / (L1 + L2), 3)
            kw.update(via=(round(via[0], 2), round(via[1], 2)), via_at=f, scale_by=f)
            L = L1 + L2
        else:
            L = ((to[0] - D_X0) ** 2 + (to[1] - COL_Y) ** 2) ** 0.5
        gl.ev("glide", fv.t_glide, glide_dur, hold=not low, group="fileview", off=off, **kw)
        gl.ev("out", fv.t_land, 0.5, group="fileview")
        B.travel(fv.t_glide, f"the {off} column filed into its slot", L, glide_dur,
                 "filing glide", keys=[gl.key], group="fileview")
    return fv


# ---------------------------------------------------------------------------
# setup: the dock's panel, tabs and columns
# ---------------------------------------------------------------------------

def setup():
    ACTIVE.clear()
    TAB_ON.clear()
    NAMED.clear()
    _N["n"] = 0
    ACTIVE.append((-1.0, "burnt"))
    TAB_ON.append((-1.0, None))
    add(El("dock.panel", "dock",
           f'<rect x="{D_X0}" y="{COL_Y}" width="{D_W}" height="{COL_BOT - COL_Y}" rx="10" '
           f'fill="{rgb(PANEL)}" stroke="{rgb(SAND_DIM)}" stroke-width="2"/>', z=0, keep=True))
    for i, o in enumerate(OF.OFFERINGS):
        x, y, w, h = tab_rect(i)
        nm = o.key
        add(El(f"tab.{o.key}.frame", "dock",
               f'<rect x="{f2(x)}" y="{y}" width="{f2(w)}" height="{h}" rx="6" '
               f'fill="{rgb(BG)}" stroke="{rgb(SAND_DIM)}" stroke-width="1.2"/>', z=1, keep=True))
        add(El(f"tab.{o.key}.bar", "dock",
               f'<rect x="{f2(x + 14)}" y="{y + h / 2 - 4.5}" width="{f2(w - 28)}" height="9" '
               f'rx="4.5" fill="{rgb(SKELETON)}"/>', z=2, keep=True))
        add(El(f"tab.{o.key}.active", "dock",
               f'<rect x="{f2(x)}" y="{y}" width="{f2(w)}" height="{h + 4}" rx="6" '
               f'fill="{rgb(PANEL)}" stroke="{rgb(SAND_DIM)}" stroke-width="1.2"/>'
               f'<rect x="{f2(x + 1.2)}" y="{y + h - 2}" width="{f2(w - 2.4)}" height="8" '
               f'fill="{rgb(PANEL)}"/>' + text(nm, x + w / 2, y + h / 2 + 1, 13, TEXT, "mm", bold=True),
               z=3, keep=True, hidden0=True,
               texts=[(tbox(nm, x + w / 2, y + h / 2 + 1, 13, "mm", True), 13, "tab")]))
        add(El(f"tab.{o.key}.name", "dock",
               text(nm, x + w / 2, y + h / 2 + 1, 13, TEXT_DIM, "mm"), z=2, keep=True, hidden0=True,
               texts=[(tbox(nm, x + w / 2, y + h / 2 + 1, 13, "mm"), 13, "tab")]))
    for o in OF.OFFERINGS:
        slots, skel, _y, _m = LAYOUT[o.key]
        col = add(El(_col(o.key), "dock", "", z=4, keep=True, hidden0=o.key != "burnt"))
        del col
        add(El(f"col.{o.key}.skel", "dock", skel_svg(skel), z=4, keep=True,
               texts=[(tbox(it[1], it[2], it[3], LABEL_PX, "lm", True), LABEL_PX, "label")
                      for it in skel if it[0] == "label"]), parent=_col(o.key))
        for sk, s_ in slots.items():
            add(El(f"col.{o.key}.bar.{sk}", "dock", slot_bar_svg(s_), z=5, keep=True),
                parent=_col(o.key))
            tb = s_.text_box()
            add(El(f"col.{o.key}.txt.{sk}", "dock", slot_text_svg(s_), z=6, keep=True,
                   hidden0=True, texts=[(tb, s_.size if s_.kind != "thing" else ICON_NAME, s_.kind)]
                   if tb else []), parent=_col(o.key))
        if o.key in FORGIVEN_OFFS:
            hy = COL_Y + MODES[LAYOUT[o.key][3]]["head"] / 2 + 1
            svg, box = chip("forgiven", D_X0 + D_W - 12, hy, 13, "rm", edge=HL)
            fe = add(El(f"col.{o.key}.forgiven", "dock", svg, z=7, keep=True, hidden0=True,
                        texts=[(box, 13, "forgiven")]), parent=_col(o.key))
            fe.fbox = box
