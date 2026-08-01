"""Top-down family-tree renderer for the 1 Chronicles 1-9 genealogies (v2).

The whole chapter is laid out once as a WORLD: each scene from
generate_1chronicles.py becomes a top-down tree (children under parents,
bus connectors, big sibling sets wrapped into rows; heading-only blocks
become stacked text panels), scenes standing side by side under large
in-world titles. Every verse's SVG shows that world through a CAMERA — a
nested translate+scale animateTransform pair (the Luke 3 dolly pattern,
which svg_freeze knows how to freeze for the reduced-motion stills). The
camera starts where the previous verse's camera rested and glides to the
current verse's family; on scene changes and long jumps it pulls back
through a mid-keyframe for context, on summary verses it frames the whole
scene, and each chapter's first verse opens from a wide establishing view.

Scenes the camera does not visit in a verse are drawn as labeled ghost
boxes — zoomed out they read as chapter structure (and they keep the files
small); the camera's own scenes are drawn in full.

The previous column-list renderer (v1) is preserved in
backups/1_Chronicles_svg_v1_columns/.
"""

import math

from generate_tabernacle import (W, H, BG, SAND, SAND_DIM, TEXT, TEXT_DIM,
                                 HL, F_SMALL, F_VERSE, F_TITLE, font)
from svg_surface import SvgCanvas, SvgLayer, _fmt, _rgb

DUR = "2.6s"
EASE = "0.42 0 0.58 1"

F_NAME = font(15)
F_NAME_B = font(15, bold=True)
F_NOTE = font(11, italic=True)
F_PANEL = font(14, italic=True)
F_SCENE = font(30, bold=True)
F_GHOST_SUB = font(18, italic=True)

TITLE_Y = 26            # in-world scene title baseline
TREE_TOP = 92           # first tree level, below the title
LEVEL = 58              # generation step (extra when the parent has a note)
NOTE_EXTRA = 16
SIB_GAP = 18
UNIT_GAP = 70
SCENE_GAP = 240
ROW_MAX = 6             # leaf siblings per wrapped row
ROW_H = 34
LINE_H = 24             # text-panel line height

VIEW_TOP, VIEW_BOT = 84, H - 44
S_MIN, S_MAX = 0.06, 1.12
OPEN_S_MIN = 0.12       # the establishing shot never zooms wider than this
FOCUS_MIN_W, FOCUS_MIN_H = 420, 260

FOOT_DEFAULT = "names as spelled in the World English Bible"


def ellipsize(text, fnt, max_w):
    if fnt.getlength(text) <= max_w:
        return text
    if max_w <= 14:
        return ""
    while text and fnt.getlength(text + "…") > max_w:
        text = text[:-1].rstrip()
        if " " in text:
            text = text.rsplit(" ", 1)[0]
    return text + "…"


def _fade_el(tag, attrs):
    """A world element that fades in as the camera settles, then holds."""
    return (f'<{tag} {attrs} opacity="0">'
            f'<animate attributeName="opacity" values="0;0;1" '
            f'keyTimes="0;0.55;1" dur="{DUR}" begin="0s" fill="freeze" '
            f'calcMode="spline" keySplines="{EASE};{EASE}"/></{tag}>')


class _Node:
    __slots__ = ("row", "kids", "x", "y", "w", "textline")

    def __init__(self, row):
        self.row = row
        self.kids = []
        self.x = self.y = 0.0
        self.w = 0.0          # box width reserved for this node alone
        self.textline = False  # a stacked text-panel line (x = LEFT edge)


class SceneLayout:
    """Places one scene's rows as top-down trees + text panels; world coords
    come from shifting the whole scene by its x offset."""

    def __init__(self, scene, rows):
        self.scene = scene
        self.rows = rows
        self.nodes = [_Node(r) for r in rows]
        for n in self.nodes:
            r = n.row
            p = r.parent if r.parent is not None else r.chainprev
            if p is not None:
                self.nodes[p].kids.append(n)
        self.roots = [n for n in self.nodes
                      if n.row.parent is None and n.row.chainprev is None]
        for n in self.nodes:
            label = self.label(n)
            fnt = F_NAME_B if (n.kids and not n.row.heading) else F_NAME
            lw = fnt.getlength(label) if label else 0
            nw = min(F_NOTE.getlength("· " + n.row.note), 190) \
                if n.row.note else 0
            n.w = max(lw, nw) + 20
        self._place_units()
        right = 0.0
        for n in self.nodes:
            right = max(right, n.x + n.w if n.textline else n.x + n.w / 2)
        self.width = max(right, F_SCENE.getlength(scene["title"]) + 24) + 30
        self.height = max(n.y for n in self.nodes) + 44
        self.x0 = 0.0          # world offset, set by ChapterWorld

    @staticmethod
    def label(n):
        return n.row.label.lstrip("~").strip() if n.row.heading \
            else n.row.label

    def _is_textline(self, n):
        if not n.row.heading:
            return False
        stack = list(n.kids)
        while stack:
            k = stack.pop()
            if not k.row.heading:
                return False
            stack.extend(k.kids)
        return True

    # -- tidy layout --------------------------------------------------------

    def _wrapped(self, n):
        return len(n.kids) > ROW_MAX and all(not k.kids for k in n.kids)

    @staticmethod
    def _rows_of(kids):
        nrows = math.ceil(len(kids) / ROW_MAX)
        per = math.ceil(len(kids) / nrows)
        return [kids[i:i + per] for i in range(0, len(kids), per)]

    def _subw(self, n):
        if not n.kids:
            return n.w
        if self._wrapped(n):
            kw = max(sum(k.w for k in r) + SIB_GAP * (len(r) - 1)
                     for r in self._rows_of(n.kids))
        else:
            kw = (sum(self._subw(k) for k in n.kids)
                  + SIB_GAP * (len(n.kids) - 1))
        return max(n.w, kw)

    def _place(self, n, cx, y):
        n.x, n.y = cx, y
        if not n.kids:
            return
        step = LEVEL + (NOTE_EXTRA if n.row.note else 0)
        if self._wrapped(n):
            ry = y + step
            for r in self._rows_of(n.kids):
                rw = sum(k.w for k in r) + SIB_GAP * (len(r) - 1)
                x = cx - rw / 2
                extra = NOTE_EXTRA if any(k.row.note for k in r) else 0
                for k in r:
                    k.x, k.y = x + k.w / 2, ry
                    x += k.w + SIB_GAP
                ry += ROW_H + extra
            return
        widths = [self._subw(k) for k in n.kids]
        total = sum(widths) + SIB_GAP * (len(n.kids) - 1)
        x = cx - total / 2
        for k, kw in zip(n.kids, widths):
            self._place(k, x + kw / 2, y + step)
            x += kw + SIB_GAP

    def _place_units(self):
        cursor = 20.0
        panel = []

        def flush_panel():
            nonlocal cursor
            if not panel:
                return
            y = TREE_TOP
            width = 0.0
            for n in panel:
                n.textline = True
                n.w = F_PANEL.getlength(self.label(n)) + 20
                width = max(width, n.w)
                n.x, n.y = cursor, y          # x is the LEFT edge
                y += LINE_H
            cursor += width + UNIT_GAP
            panel.clear()

        for root in self.roots:
            if self._is_textline(root):
                stack = [root]                # preorder: root + descendants
                while stack:
                    n = stack.pop(0)
                    panel.append(n)
                    stack = list(n.kids) + stack
                continue
            flush_panel()
            w = self._subw(root)
            self._place(root, cursor + w / 2, TREE_TOP)
            cursor += w + UNIT_GAP
        flush_panel()

    # -- world-space helpers ------------------------------------------------

    def pos(self, i):
        n = self.nodes[i]
        return n.x + self.x0, n.y

    def rect(self, i):
        n = self.nodes[i]
        y0, y1 = n.y - 13, n.y + 13 + (NOTE_EXTRA if n.row.note else 0)
        if n.textline:
            return n.x + self.x0, y0, n.x + self.x0 + n.w, y1
        x = n.x + self.x0
        return x - n.w / 2, y0, x + n.w / 2, y1

    def bbox(self):
        return (self.x0, 0, self.x0 + self.width, self.height)


# ---------------------------------------------------------------------------
# Camera
# ---------------------------------------------------------------------------

def _fit(bbox, pad=70):
    """(scale, world cx, world cy) framing bbox inside the viewport band."""
    x0, y0, x1, y1 = bbox
    x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
    bw, bh = max(x1 - x0, 1), max(y1 - y0, 1)
    vw, vh = W, VIEW_BOT - VIEW_TOP
    s = min(S_MAX, max(S_MIN, min(vw / bw, vh / bh)))
    return s, (x0 + x1) / 2, (y0 + y1) / 2


def _cam_T(cam):
    s, wx, wy = cam
    cx, cy = W / 2, (VIEW_TOP + VIEW_BOT) / 2
    return cx - s * wx, cy - s * wy


def _union(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]),
            max(a[2], b[2]), max(a[3], b[3]))


def _grow_min(bbox):
    x0, y0, x1, y1 = bbox
    if x1 - x0 < FOCUS_MIN_W:
        cx = (x0 + x1) / 2
        x0, x1 = cx - FOCUS_MIN_W / 2, cx + FOCUS_MIN_W / 2
    if y1 - y0 < FOCUS_MIN_H:
        cy = (y0 + y1) / 2
        y0, y1 = cy - FOCUS_MIN_H / 2, cy + FOCUS_MIN_H / 2
    return x0, y0, x1, y1


# ---------------------------------------------------------------------------
# Chapter world
# ---------------------------------------------------------------------------

class ChapterWorld:
    """All of a chapter's scenes laid out side by side + per-verse cameras.
    render_verse must be called in verse order — the camera carries over."""

    def __init__(self, chapter, scene_data):
        """scene_data: [(scene, rows, first_read, highlights), ...]"""
        self.chapter = chapter
        self.data = scene_data
        self.layouts = []
        x = 0.0
        for scene, rows, _fr, _hl in scene_data:
            lay = SceneLayout(scene, rows)
            lay.x0 = x
            x += lay.width + SCENE_GAP
            self.layouts.append(lay)
        self.world_bbox = (0, 0, x - SCENE_GAP,
                           max(l.height for l in self.layouts) + 20)
        self._prev_cam = None
        self._prev_focus = None
        self._prev_scene = None

    # -- focus & camera per verse -------------------------------------------

    def _focus_bbox(self, si, verse):
        scene, rows, first_read, highlights = self.data[si]
        lay = self.layouts[si]
        hl = highlights.get(verse, [])
        if not hl:
            return lay.bbox(), True     # summary verse -> whole scene
        box = None
        for i in hl:
            r = lay.rect(i)
            box = r if box is None else _union(box, r)
            p = rows[i].parent if rows[i].parent is not None \
                else rows[i].chainprev
            if p is not None:
                box = _union(box, lay.rect(p))
        return _grow_min(box), False

    def _opening_cam(self, si):
        """Wide establishing shot: whole chapter if that stays readable,
        else a wide window centered on the first scene."""
        s, wx, wy = _fit(self.world_bbox, pad=40)
        if s >= OPEN_S_MIN:
            return s, wx, wy
        b = self.layouts[si].bbox()
        return OPEN_S_MIN, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2

    def _camera(self, si, verse, first_of_chapter):
        focus, is_scene_fit = self._focus_bbox(si, verse)
        cam1 = _fit(focus, pad=60 if is_scene_fit else 70)
        if first_of_chapter or self._prev_cam is None:
            cam0 = self._opening_cam(si)
        else:
            cam0 = self._prev_cam
        mid = None
        if not first_of_chapter and self._prev_focus is not None:
            dist = math.hypot(cam1[1] - cam0[1], cam1[2] - cam0[2]) \
                * max(cam0[0], cam1[0])
            if self._prev_scene != si or dist > 700:
                mid = _fit(_union(self._prev_focus, focus), pad=130)
        self._prev_cam, self._prev_focus, self._prev_scene = cam1, focus, si
        return cam0, mid, cam1

    # -- drawing ------------------------------------------------------------

    def _draw_scene(self, d, anims, si, verse):
        scene, rows, first_read, highlights = self.data[si]
        lay = self.layouts[si]
        hl = set(highlights.get(verse, []))
        lo, hi = scene["verses"]

        d.text((lay.x0 + 20, TITLE_Y), scene["title"], font=F_SCENE,
               fill=TEXT if lo <= verse <= hi else TEXT_DIM, anchor="lm")

        def read(i):
            fv = first_read.get(i)
            return fv is None or fv <= verse

        # connectors under the names
        for n in lay.nodes:
            if not n.kids or n.textline:
                continue
            px, py = lay.pos(n.row.index)
            blank = n.row.heading and not self.label_of(lay, n)
            kid_tops = [(lay.pos(k.row.index), k) for k in n.kids]
            p_read = read(n.row.index)
            if len(kid_tops) == 1:
                (kx, ky), k = kid_tops[0]
                d.line([(px, py + 13), (kx, ky - 13)],
                       fill=SAND if read(k.row.index) else SAND_DIM, width=2)
                continue
            rail_y = min(ky for (_, ky), _k in kid_tops) - 18
            if not blank:
                d.line([(px, py + 13), (px, rail_y)],
                       fill=SAND if p_read else SAND_DIM, width=2)
            xs = [kx for (kx, _), _k in kid_tops]
            d.line([(min(xs), rail_y), (max(xs), rail_y)],
                   fill=SAND if p_read else SAND_DIM, width=2)
            for (kx, ky), k in kid_tops:
                d.line([(kx, rail_y), (kx, ky - 13)],
                       fill=SAND if read(k.row.index) else SAND_DIM, width=2)

        # names
        for n in lay.nodes:
            i = n.row.index
            label = self.label_of(lay, n)
            if not label:
                continue
            x, y = lay.pos(i)
            cur = i in hl
            if n.textline:
                d.text((x, y), label, font=F_PANEL,
                       fill=HL if cur else TEXT_DIM, anchor="lm")
                if cur:
                    lw = F_PANEL.getlength(label)
                    anims.append(_fade_el(
                        "line",
                        f'x1="{_fmt(x)}" y1="{_fmt(y + 11)}" '
                        f'x2="{_fmt(x + lw)}" y2="{_fmt(y + 11)}" '
                        f'stroke="{_rgb(HL)}" stroke-width="2"'))
                continue
            if n.row.heading:
                d.text((x, y), label, font=F_NOTE,
                       fill=HL if cur else TEXT_DIM, anchor="mm")
                if cur:
                    lw = F_NOTE.getlength(label)
                    anims.append(_fade_el(
                        "line",
                        f'x1="{_fmt(x - lw / 2)}" y1="{_fmt(y + 10)}" '
                        f'x2="{_fmt(x + lw / 2)}" y2="{_fmt(y + 10)}" '
                        f'stroke="{_rgb(HL)}" stroke-width="2"'))
                continue
            fnt = F_NAME_B if n.kids else F_NAME
            d.text((x, y), label, font=fnt,
                   fill=HL if cur else (TEXT if read(i) else TEXT_DIM),
                   anchor="mm")
            if n.row.note:
                note = ellipsize("· " + n.row.note, F_NOTE, 190)
                d.text((x, y + 15), note, font=F_NOTE,
                       fill=HL if cur else TEXT_DIM, anchor="mm")
            if cur:
                x0, y0, x1, y1 = lay.rect(i)
                anims.append(_fade_el(
                    "rect",
                    f'x="{_fmt(x0 - 4)}" y="{_fmt(y0)}" '
                    f'width="{_fmt(x1 - x0 + 8)}" '
                    f'height="{_fmt(y1 - y0)}" rx="8" fill="none" '
                    f'stroke="{_rgb(HL)}" stroke-width="2"'))

    @staticmethod
    def label_of(lay, n):
        return lay.label(n)

    def _draw_ghost(self, d, si, verse):
        lay = self.layouts[si]
        scene = self.data[si][0]
        x0, y0, x1, y1 = lay.bbox()
        lo, hi = scene["verses"]
        done = verse > hi
        d.rounded_rectangle([x0, y0 + 8, x1, y1], radius=18,
                            outline=SAND if done else SAND_DIM, width=2)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        title = scene["title"]
        d.text((cx, cy - 12), title, font=F_SCENE,
               fill=TEXT if done else TEXT_DIM, anchor="mm")
        d.text((cx, cy + 22), f"verses {lo}–{hi}", font=F_GHOST_SUB,
               fill=TEXT_DIM, anchor="mm")

    # -- verse render -------------------------------------------------------

    def render_verse(self, si, verse, verse_text, first_of_chapter):
        scene = self.data[si][0]
        prev_scene = self._prev_scene
        cam0, mid, cam1 = self._camera(si, verse, first_of_chapter)

        full = {si}
        if prev_scene is not None and not first_of_chapter:
            full.add(prev_scene)        # the camera departs from there

        world = SvgLayer()
        anims = []
        for j in range(len(self.layouts)):
            if j in full:
                self._draw_scene(world, anims, j, verse)
            else:
                self._draw_ghost(world, j, verse)

        # camera: outer translate, inner scale (nested, same timing)
        t0, t1 = _cam_T(cam0), _cam_T(cam1)
        if mid:
            tm = _cam_T(mid)
            tvals = (f"{_fmt(t0[0])} {_fmt(t0[1])};"
                     f"{_fmt(tm[0])} {_fmt(tm[1])};"
                     f"{_fmt(t1[0])} {_fmt(t1[1])}")
            svals = f"{_fmt(cam0[0])};{_fmt(mid[0])};{_fmt(cam1[0])}"
            times = 'keyTimes="0;0.5;1"'
            splines = f'keySplines="{EASE};{EASE}"'
        else:
            tvals = (f"{_fmt(t0[0])} {_fmt(t0[1])};"
                     f"{_fmt(t1[0])} {_fmt(t1[1])}")
            svals = f"{_fmt(cam0[0])};{_fmt(cam1[0])}"
            times = 'keyTimes="0;1"'
            splines = f'keySplines="{EASE}"'
        grp = (
            f'<g><animateTransform attributeName="transform" '
            f'attributeType="XML" type="translate" values="{tvals}" '
            f'dur="{DUR}" begin="0s" fill="freeze" calcMode="spline" '
            f'{times} {splines}/>'
            f'<g><animateTransform attributeName="transform" '
            f'attributeType="XML" type="scale" values="{svals}" '
            f'dur="{DUR}" begin="0s" fill="freeze" calcMode="spline" '
            f'{times} {splines}/>'
            + "".join(world.elements()) + "".join(anims)
            + "</g></g>")

        c = SvgCanvas(W, H, bg=BG)
        c.raw([grp])

        # HUD band + title (screen-fixed, above the world). No caption line
        # or footer: the verse is narrated aloud, and the camera-framed names
        # carry it.
        hud = SvgLayer()
        hud.rectangle([0, 0, W, 46], fill=BG + (232,))
        hud.text((28, 20), f"{scene['title']} — 1 Chronicles {self.chapter}",
                 font=F_TITLE, fill=TEXT)
        c.raw(hud.elements())
        return c
