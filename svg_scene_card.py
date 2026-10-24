"""Scene cards: a side-view picture hung inside a map camera's world.

A camera tour (svg_map_camera) can fly from a town's dot down into a drawn
scene of that town -- figures, buildings, a street -- and back out, without a
cut. The card lives in the same world as the map, hung at the town at a
deep zoom: one card px is one screen px when the camera's scale is S (the
card's `zoom 1`), so a man drawn 110 card px tall is 110 px on screen there.

The card is a cast of Actors over fixed scenery. Each verse is its own SVG
file, so an actor's state (where it stands, its pose, its ink, whether it is
up or lying down, whether it is there at all) carries from one verse to the
next: `Card.state_at(ref)` replays every earlier verse's events, and
`Card.svg(ref, ...)` draws the cast as the verse opens, with this verse's own
events animated (SMIL). A figure changes pose only when the verse narrates
it; nothing re-animates as decoration.

Event kinds, each (kind, actor, t, dur, value):
    show / hide      fade in or out
    move  (dx, dy)   walk or slide, eased; the actor's name rides with it
    hop   h          up h px and down again
    pose  {...}      cross-fade to another pose of the same figure
    ink   colour     cross-fade to another ink (to dim, say)
    rot   degrees    turn about the feet (a fall)
    grow             rise out of the ground (a plant)
    scale f          grow or shrink by f about the feet (the light)
    grow_x           swing out from the origin (a door on its hinge)
    name_dy dy       its name moves up or down (a man stands up)
    mark  svg        draw a mark on the figure, which then rides with it
    pulse            one gold pulse round the figure's outline
    label text       its name appears (constant screen size)
    strike           a rule traces through its name (the name stays)
Times are seconds from the start of the verse.
"""

from xml.sax.saxutils import escape

import svg_figures as F
from svg_surface import SvgCanvas, _fmt
from svg_map_camera import EASE, fade, rgb, to_screen, ink as ink_box
from generate_tabernacle import W, H

MAN_H = 97.0        # a man's height in figure units


def figure_svg(parts, h_px, ink, page, flip=1, rot=0.0, unit_h=MAN_H):
    """A figure in card px, feet at (0, 0)."""
    c = SvgCanvas(10, 10)
    F.draw(c, parts, 0, 0, h_px / unit_h, ink, page, flip=flip, rot=rot)
    return "".join(c._els)


def outline_svg(parts, h_px, flip=1, unit_h=MAN_H):
    pts = F.outline(parts, 0, 0, h_px / unit_h, flip)
    return " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in pts)


class Actor:
    """A figure on the card. `make(**pose)` returns its parts; `h` is how
    tall it is drawn (card px) for a figure `unit_h` units tall."""

    def __init__(self, key, make, x, y, h=110.0, unit_h=MAN_H, flip=1,
                 ink=None, pose=None, shown=False, label=None,
                 label_y=None, label_fill=None, label_italic=False,
                 label_dx=0):
        self.key, self.make = key, make
        self.h, self.unit_h = h, unit_h
        self.start = dict(x=x, y=y, flip=flip, ink=ink, pose=dict(pose or {}),
                          shown=shown, rot=0.0, label=label, scale=1.0)
        # where its name sits, card px from its feet (up is negative), and
        # how it is set (a signpost name is dim and italic)
        self.label_y = label_y if label_y is not None else -(h + 22)
        self.label_fill, self.label_italic = label_fill, label_italic
        # a sideways nudge in screen px, so two names side by side stay
        # apart at any zoom
        self.label_dx = label_dx

    def parts(self, pose):
        return self.make(**pose)


class Card:
    """A scene card: size (w, h) in card px, the point `anchor` hung at the
    town's world point, the camera scale `S` at which it is zoom 1."""

    def __init__(self, key, town_xy, anchor, size, S, page, sky, ground_y,
                 origin=(0, 0)):
        self.key, self.town_xy, self.anchor = key, town_xy, anchor
        self.size, self.S, self.page, self.sky = size, S, page, sky
        self.origin = origin
        self.ground_y = ground_y
        self.actors = {}
        self.scenery = []         # (svg, card px) drawn under the cast
        self.events = {}          # ref -> [(kind, actor, t, dur, value)]
        self.fx = {}              # ref -> svg drawn over the cast that verse
        self.fx_after = {}        # ref -> svg drawn in every later verse
        self.refs = []            # verses in reading order

    def add(self, actor):
        self.actors[actor.key] = actor
        return actor

    def on(self, ref, *events):
        self.events.setdefault(ref, []).extend(events)

    def effect(self, ref, now, after=None):
        """An effect drawn over the cast on `ref` (animated), and what it
        leaves behind for the verses after (static), if anything."""
        self.fx.setdefault(ref, []).append(now)
        if after:
            self.fx_after.setdefault(ref, []).append(after)

    # -- camera ----------------------------------------------------------

    def cam(self, x, y, z):
        """The camera that puts card point (x, y) at the screen centre at
        zoom z (one card px = z screen px)."""
        ax, ay = self.anchor
        tx, ty = self.town_xy
        return (z * self.S, tx + (x - ax) / self.S, ty + (y - ay) / self.S)

    def zoom(self, cam):
        return cam[0] / self.S

    def world(self, xy):
        """A card point in world units."""
        ax, ay = self.anchor
        tx, ty = self.town_xy
        return tx + (xy[0] - ax) / self.S, ty + (xy[1] - ay) / self.S

    # -- state -----------------------------------------------------------

    def state_at(self, ref):
        """Every actor's state as `ref` opens."""
        st = {k: dict(a.start, pose=dict(a.start["pose"]))
              for k, a in self.actors.items()}
        for r in self.refs:
            if r == ref:
                break
            for kind, key, _t, _d, val in self.events.get(r, []):
                apply_event(st[key], kind, val)
        return st

    # -- drawing ---------------------------------------------------------

    def svg(self, ref, fl, font_px, label_ink, pulse_ink):
        """The card's group in world units for this verse: scenery, then the
        cast as the verse opens with this verse's events animated.
        `font_px` is the names' screen size; the names hold it through the
        flight (font-size animated as px * S / s)."""
        st = self.state_at(ref)
        evs = sorted(self.events.get(ref, []), key=lambda e: e[2])
        ax, ay = self.anchor
        tx, ty = self.town_xy
        w, h = self.size
        x0, y0 = self.origin
        out = [f'<g transform="translate({_fmt(tx)} {_fmt(ty)}) '
               f'scale({1 / self.S:.6g}) translate({-ax} {-ay})">']
        cid = f"card_{self.key}"
        box = f'x="{x0}" y="{y0}" width="{w}" height="{h}"'
        out.append(f'<defs><clipPath id="{cid}"><rect {box} rx="24"/>'
                   f'</clipPath></defs>')
        out.append(f'<g clip-path="url(#{cid})">')
        out.append(f'<rect {box} fill="{rgb(self.sky)}"/>')
        out += [s for s in self.scenery]
        cast_at = len(out)
        ks = [f"{self.S / c[0]:.5g}" for c in fl.cams]
        self._k = (ks[0], fl._anim("transform", ks, "scale"))
        self._rest, self._open = fl.cam1, fl.cam0
        self._font_px = font_px
        names = []
        marks = {}
        for r in self.refs:
            if r == ref:
                break
            for kind, key, _t, _d, val in self.events.get(r, []):
                if kind == "mark":
                    marks.setdefault(key, []).append(val)
        self._marks0 = marks
        self._syms, self._sym_defs = {}, []
        for key, actor in self.actors.items():
            mine = [e for e in evs if e[1] == key]
            if not st[key]["shown"] and not any(e[0] == "show"
                                                for e in mine):
                continue
            el, name = self._actor(actor, st[key], mine, label_ink,
                                   pulse_ink)
            out.append(el)
            if name:
                names.append(name)
        if self._sym_defs:
            out.insert(cast_at, "<defs>" + "".join(self._sym_defs)
                       + "</defs>")
        for r in self.refs:
            if r == ref:
                break
            out += self.fx_after.get(r, [])
        out += self.fx.get(ref, [])
        if names:
            ops = [f"{name_op(c[0] / self.S):.2f}" for c in fl.cams]
            out.append(f'<g font-size="{font_px}" text-anchor="middle" '
                       f'opacity="{ops[0]}">{fl._anim("opacity", ops)}'
                       + "".join(names) + "</g>")
        out.append("</g>")
        sa, sanim = self._inverse(fl, "stroke-width", 1.5)
        out.append(f'<rect {box} rx="24" fill="none" '
                   f'stroke="rgb(74,70,56)" {sa}>{sanim}</rect>')
        out.append("</g>")
        return "".join(out)

    def _drawing(self, a, pose, ink, flip):
        """A <use> of the figure drawn once per verse file: a crowd of the
        same few people costs a few drawings, not one each."""
        parts = a.parts(pose)
        if not parts:
            return ""             # a name with no figure (a group's name)
        k = (id(a.make), tuple(sorted(pose.items())), a.h, a.unit_h,
             tuple(ink), flip)
        if k not in self._syms:
            sid = f"{self.key}{len(self._syms)}"
            self._syms[k] = sid
            self._sym_defs.append(
                f'<g id="{sid}">'
                + figure_svg(parts, a.h, ink, self.page, flip,
                             unit_h=a.unit_h) + "</g>")
        return f'<use href="#{self._syms[k]}"/>'

    def _inverse(self, fl, attr, px):
        vals = [f"{px * self.S / c[0]:.5g}" for c in fl.cams]
        return f'{attr}="{vals[0]}"', fl._anim(attr, vals)

    def _actor(self, a, s0, evs, label_ink, pulse_ink):
        """One actor: <g translate(x, y)> with its moves summed on top, a
        rotate group about the feet, and one layer per pose/ink it shows
        this verse, cross-faded at the switches."""
        s = dict(s0, pose=dict(s0["pose"]))
        moves, layers, rots, pulses, names = [], [], [], [], []
        shown_anim = []
        cur = (dict(s["pose"]), s["ink"], s["flip"])
        segs = [[cur, None, None]]                  # [look, t_in, t_out]
        for kind, _k, t, d, val in evs:
            if kind == "move":
                dx, dy = val
                moves.append(
                    f'<animateTransform attributeName="transform" '
                    f'type="translate" values="0 0;{_fmt(dx)} {_fmt(dy)}" '
                    f'additive="sum" begin="{t:.2f}s" dur="{d:.2f}s" '
                    f'fill="freeze" calcMode="spline" keyTimes="0;1" '
                    f'keySplines="{EASE}"/>')
            elif kind == "hop":
                moves.append(
                    f'<animateTransform attributeName="transform" '
                    f'type="translate" values="0 0;0 {-val};0 0" '
                    f'additive="sum" begin="{t:.2f}s" dur="{d:.2f}s" '
                    f'fill="freeze" calcMode="spline" keyTimes="0;0.5;1" '
                    f'keySplines="0 0 0.58 1;0.42 0 1 1"/>')
            elif kind in ("pose", "ink", "flip"):
                look = segs[-1][0]
                nl = (dict(look[0], **val) if kind == "pose" else look[0],
                      val if kind == "ink" else look[1],
                      val if kind == "flip" else look[2])
                segs[-1][2] = (t, d)
                segs.append([nl, (t, d), None])
            elif kind == "grow":
                rots.append(
                    f'<animateTransform attributeName="transform" '
                    f'type="scale" values="1 0.02;1 1" additive="sum" '
                    f'begin="{t:.2f}s" dur="{d:.2f}s" fill="freeze" '
                    f'calcMode="spline" keyTimes="0;1" '
                    f'keySplines="{EASE}"/>')
            elif kind == "grow_x":
                rots.append(
                    f'<animateTransform attributeName="transform" '
                    f'type="scale" values="0.05 1;1 1" additive="sum" '
                    f'begin="{t:.2f}s" dur="{d:.2f}s" fill="freeze" '
                    f'calcMode="spline" keyTimes="0;1" '
                    f'keySplines="{EASE}"/>')
            elif kind == "scale":
                f0 = 1.0
                rots.append(
                    f'<animateTransform attributeName="transform" '
                    f'type="scale" values="{f0};{val}" additive="sum" '
                    f'begin="{t:.2f}s" dur="{d:.2f}s" fill="freeze" '
                    f'calcMode="spline" keyTimes="0;1" '
                    f'keySplines="{EASE}"/>')
            elif kind == "mark":
                pulses.append(f'<g opacity="0">{fade(t, d)}{val}</g>')
            elif kind == "rot":
                rots.append(
                    f'<animateTransform attributeName="transform" '
                    f'type="rotate" values="0 0 0;{val} 0 0" '
                    f'additive="sum" begin="{t:.2f}s" dur="{d:.2f}s" '
                    f'fill="freeze" calcMode="spline" keyTimes="0;1" '
                    f'keySplines="{EASE}"/>')
            elif kind == "pulse":
                look = segs[-1][0]
                pts = outline_svg(a.parts(look[0]), a.h, look[2], a.unit_h)
                pulses.append(
                    f'<polygon points="{pts}" fill="none" '
                    f'stroke="{rgb(pulse_ink)}" stroke-width="3" '
                    f'stroke-linejoin="round" opacity="0">'
                    f'<animate attributeName="opacity" values="0;1;1;0" '
                    f'keyTimes="0;0.3;0.6;1" begin="{t:.2f}s" '
                    f'dur="{d:.2f}s" fill="freeze"/></polygon>')
            elif kind == "show":
                shown_anim.append(fade(t, d))
            elif kind == "hide":
                shown_anim.append(fade(t, d, out=True))
            elif kind == "label":
                pass
        for look, t_in, t_out in segs:
            pose, ink, flip = look
            body = self._drawing(a, pose, ink, flip)
            anim = ""
            op = "1"
            if t_in is not None:
                op = "0"
                anim += fade(t_in[0], t_in[1])
            if t_out is not None:
                anim += fade(t_out[0], t_out[1], out=True)
            layers.append(f'<g opacity="{op}">{anim}{body}</g>')
        # names: the start label, and any label event, riding the moves at
        # one screen size (a scale(S/s) group), struck when the verse says
        lab0 = s0.get("label")
        lab_evs = [(v, t) for kind, _k, t, _d, v in evs if kind == "label"]
        strikes = [(t, d) for kind, _k, t, d, _v in evs if kind == "strike"]
        struck0 = s0.get("struck", False)
        rot0 = s0.get("rot", 0.0)
        name_y = a.label_y + s0.get("name_dy", 0.0)
        drop = a.h * 0.72              # how far a name falls with a fall
        if rot0:
            name_y += drop
        falls = []
        for kind, _k, t, d, val in evs:
            if kind == "name_dy":
                falls.append(
                    f'<animateTransform attributeName="transform" '
                    f'type="translate" values="0 0;0 {_fmt(val)}" '
                    f'additive="sum" begin="{t:.2f}s" dur="{d:.2f}s" '
                    f'fill="freeze"/>')
            if kind == "rot":
                dy = drop if val and not rot0 else -drop
                falls.append(
                    f'<animateTransform attributeName="transform" '
                    f'type="translate" values="0 0;0 {_fmt(dy)}" '
                    f'additive="sum" begin="{t:.2f}s" dur="{d:.2f}s" '
                    f'fill="freeze"/>')
        k0, kanim = self._k
        ital = ' font-style="italic"' if a.label_italic else ""
        end = dict(s0, pose=dict(s0["pose"]))
        for kind, _k, _t, _d, val in evs:
            apply_event(end, kind, val)
        end_y = a.label_y + end.get("name_dy", 0.0) + (
            a.h * 0.72 if end.get("rot") else 0.0)
        start_y = a.label_y + s0.get("name_dy", 0.0) + (
            a.h * 0.72 if s0.get("rot") else 0.0)

        def cut(cam, x, y, box):
            sx, sy = to_screen(cam, self.world((x, y)))
            sx += a.label_dx
            return (sx + box[0] < 2 or sx + box[2] > W - 2 or
                    sy + box[1] < 2 or sy + box[3] > H - 2)
        for text, t in ([(lab0, None)] if lab0 else []) + lab_evs:
            # a name its rest would leave cut by the frame goes early, and
            # one the last verse left cut comes back in, not at once
            box = ink_box(text, self._font_px, False, a.label_italic, "mm")
            gone = ""
            if cut(self._rest, end["x"], end["y"] + end_y, box):
                if t is not None:
                    continue              # it would only arrive cut
                if not end["shown"] and not s0["shown"]:
                    continue
                gone = fade(0.0, 0.4, out=True)
            elif t is None and cut(self._open, s0["x"], s0["y"] + start_y,
                                   box):
                gone = (f'<set attributeName="opacity" to="0" begin="0s"/>'
                        + fade(0.3, 0.5))
            op = "" if t is None else ' opacity="0"'
            an = "" if t is None else fade(t, 0.5)
            wpx = ink_box(text, self._font_px, False, False, "mm")
            x0, x1 = wpx[0] - 3, wpx[2] + 3
            rule = ""
            if struck0:
                rule = (f'<line x1="{x0}" y1="0" x2="{x1}" y2="0" '
                        f'stroke="{rgb(label_ink)}" stroke-width="2"/>')
            for t_s, d_s in strikes:
                L = x1 - x0
                rule += (f'<line x1="{x0}" y1="0" x2="{x1}" y2="0" '
                         f'stroke="{rgb(label_ink)}" stroke-width="2" '
                         f'stroke-dasharray="{L} {L}" '
                         f'stroke-dashoffset="{L}"><animate '
                         f'attributeName="stroke-dashoffset" '
                         f'values="{L};0" begin="{t_s:.2f}s" '
                         f'dur="{d_s:.2f}s" fill="freeze"/></line>')
            names.append(
                f'<g transform="translate({_fmt(s0["x"])} {_fmt(s0["y"])})">'
                + gone + "".join(moves)
                + f'<g transform="translate(0 {_fmt(name_y)})">'
                + "".join(falls)
                + f'<g transform="scale({k0})">{kanim}'
                + f'<g transform="translate({a.label_dx} 0)"{op}>{an}'
                + f'<text x="0" y="0" dominant-baseline="central" '
                  f'fill="{rgb(a.label_fill or label_ink)}" '
                  f'stroke="{rgb(self.sky)}" stroke-width="4" '
                  f'stroke-opacity="0.8" paint-order="stroke"{ital}>'
                  f'{escape(text)}</text>'
                + rule + "</g></g></g></g>")
        op0 = "1" if s0["shown"] else "0"
        tf = []
        if rot0:
            tf.append(f"rotate({_fmt(rot0)})")
        if s0.get("scale", 1.0) != 1.0:
            tf.append(f"scale({s0['scale']:.4g})")
        rot_attr = f' transform="{" ".join(tf)}"' if tf else ""
        old_marks = "".join(self._marks0.get(a.key, []))
        el = (f'<g transform="translate({_fmt(s0["x"])} {_fmt(s0["y"])})" '
              f'opacity="{op0}">' + "".join(shown_anim) + "".join(moves)
              + f'<g{rot_attr}>' + "".join(rots) + "".join(layers)
              + old_marks + "".join(pulses) + "</g></g>")
        return el, ("".join(names) if s0["shown"] or shown_anim else "")


NAMES_AT = (0.50, 0.60)   # zooms over which the cast's names come in


def name_op(z):
    """A name is a screen size; on a card still too small to read as a
    scene it would cover the people it names, so it waits."""
    lo, hi = NAMES_AT
    return max(0.0, min(1.0, (z - lo) / (hi - lo)))


def apply_event(s, kind, val):
    """An actor's state after one event."""
    if kind == "move":
        s["x"] += val[0]
        s["y"] += val[1]
    elif kind == "pose":
        s["pose"] = dict(s["pose"], **val)
    elif kind == "ink":
        s["ink"] = val
    elif kind == "flip":
        s["flip"] = val
    elif kind == "rot":
        s["rot"] = s.get("rot", 0.0) + val
    elif kind == "show":
        s["shown"] = True
    elif kind == "hide":
        s["shown"] = False
    elif kind == "label":
        s["label"] = val
    elif kind == "strike":
        s["struck"] = True
    elif kind == "scale":
        s["scale"] = s.get("scale", 1.0) * val
    elif kind == "name_dy":
        s["name_dy"] = s.get("name_dy", 0.0) + val
