"""Render Acts 13-14 (Paul's First Missionary Journey) as per-verse vector SVGs.

One map, replayed for all 80 verses (Acts 13 = 52, Acts 14 = 28): a stylised
map of southern Asia Minor and Cyprus over which the journey reveals itself.
The route is drawn leg by leg as the narrative moves — the whole planned
circuit shown faintly dashed for orientation, each traversed leg solidified,
and the current leg tracing itself in bright gold (draw once, then hold, per
the house animation rules). Sea crossings (Seleucia->Cyprus, Paphos->Perga,
Attalia->Antioch) read as dotted "sailing" lines; land legs are solid.

A side panel gives the itinerary as a vertical route strip — the eleven
waypoints in order, the current one lit — plus a two-line scene note, so the
long stationary stretches (Paul's sermon at Pisidian Antioch, the Lystra
scene) still have per-verse movement in the caption and panel while the map
holds steady.

Coordinates are approximate; ancient site identifications (Lystra, Derbe) are
scholarly reconstructions and the footer says so. Geometry is hand-encoded
lat/lon simplified from standard atlas maps, projected with the same
equirectangular MapFrame the Numbers tribal maps use.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_acts1314_svg.py
"""

import math
import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, SAND, SAND_DIM, TEXT, TEXT_DIM, HL,
                                 out_path)
from generate_tribal_maps import MapFrame, SEA, LAND, RIVER, WATER_TXT

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

MAP_RECT = (24, 92, 636, 556)            # x0, y0, x1, y1 of the map window
MF = MapFrame(34.35, 38.75, 29.85, 37.00, MAP_RECT)
PANEL_X = 648
FOOTER = "route and ancient site locations are approximate"

DASH_UP = "5,6"          # upcoming (not-yet-travelled) legs
DASH_SEA = "2,6"         # a travelled sea crossing (dotted "sailing" line)


def g(alpha):
    return HL + (int(255 * alpha),)


# ---------------------------------------------------------------------------
# Geography (lat, lon) — simplified from standard Bible-atlas coastlines.
# The Mediterranean is a bite out of the south; Anatolia + Syria are one
# connected landmass around the NE corner of the sea, Cyprus a lone island.
# ---------------------------------------------------------------------------

# Mainland: whole frame is land except where the southern coast cuts the sea
# in. Traced clockwise from the NW corner, out beyond the frame so the group
# clip trims the outer edges cleanly.
MAINLAND = [
    (38.95, 29.60), (38.95, 37.10), (34.20, 37.10),         # N edge + E edge
    (34.20, 35.90),                                          # SE: Levant coast
    (34.60, 35.88), (35.00, 35.80), (35.40, 35.78),         # up the Syrian coast
    (35.75, 35.82), (35.95, 35.95), (36.10, 35.98),         # past Seleucia
    (36.30, 36.02), (36.48, 35.98), (36.60, 36.16),         # Gulf of Issus
    (36.80, 36.02), (36.87, 35.55), (36.80, 35.05),         # round to Cilicia
    (36.70, 34.72), (36.53, 34.42), (36.36, 33.98),
    (36.24, 33.55), (36.10, 33.10), (36.02, 32.80),         # Cape Anamur
    (36.11, 32.42), (36.24, 32.02), (36.37, 31.62),
    (36.47, 31.24), (36.62, 30.98), (36.82, 30.90),         # E side, Antalya gulf
    (36.93, 30.74), (36.80, 30.54), (36.60, 30.40),         # head of the gulf
    (36.49, 30.08), (36.44, 29.60),                         # Lycian coast, W edge
]

CYPRUS = [
    (34.90, 32.32), (35.05, 32.30), (35.42, 32.60),         # W cape, NW coast
    (35.28, 33.00), (35.36, 33.35), (35.42, 33.75),         # N coast (Kyrenia)
    (35.55, 34.24), (35.70, 34.58),                         # Karpas peninsula tip
    (35.52, 34.20), (35.28, 34.00), (35.12, 33.90),         # E coast (Salamis)
    (34.95, 33.70), (34.80, 33.45), (34.62, 33.02),         # SE, Cape Gata
    (34.68, 32.62), (34.70, 32.42), (34.82, 32.33),         # S coast (Paphos)
]

# region label anchors (lat, lon, text, anchor)
REGIONS = [
    (37.72, 30.62, "PISIDIA", "mm"),
    (36.55, 31.45, "PAMPHYLIA", "mm"),
    (37.12, 32.85, "LYCAONIA", "mm"),
    (38.50, 34.40, "GALATIA", "mm"),
    (36.78, 34.55, "CILICIA", "mm"),
    (35.70, 36.55, "SYRIA", "mm"),
    (34.98, 33.18, "CYPRUS", "mm"),
]
WATERS = [
    (35.02, 31.15, "The Great Sea", "mm"),
    (34.74, 31.15, "(Mediterranean)", "mm"),
]

# ---------------------------------------------------------------------------
# Cities  key -> (label, lat, lon, (dx, dy, anchor))
# ---------------------------------------------------------------------------

CITIES = {
    "ANTIOCH_SYRIA":   ("Antioch in Syria", 36.20, 36.16, (0, -12, "mb")),
    "SELEUCIA":        ("Seleucia",         36.12, 35.93, (-7, 11, "rm")),
    "SALAMIS":         ("Salamis",          35.18, 33.90, (9, 1, "lm")),
    "PAPHOS":          ("Paphos",           34.76, 32.41, (-9, 6, "rm")),
    "PERGA":           ("Perga",            36.96, 30.85, (9, -5, "lm")),
    "ATTALIA":         ("Attalia",          36.88, 30.70, (-8, 10, "rm")),
    "ANTIOCH_PISIDIA": ("Pisidian Antioch", 38.30, 31.19, (0, -12, "mb")),
    "ICONIUM":         ("Iconium",          37.87, 32.49, (10, -3, "lm")),
    "LYSTRA":          ("Lystra",           37.58, 32.30, (-9, 3, "rm")),
    "DERBE":           ("Derbe",            37.35, 33.35, (10, 4, "lm")),
}

# The itinerary, in journey order. row -> (city key, region tag)
ROUTE = [
    ("ANTIOCH_SYRIA",   "Syria — sent out"),
    ("SELEUCIA",        "the port"),
    ("SALAMIS",         "Cyprus"),
    ("PAPHOS",          "Cyprus"),
    ("PERGA",           "Pamphylia"),
    ("ANTIOCH_PISIDIA", "Pisidia"),
    ("ICONIUM",         "Lycaonia"),
    ("LYSTRA",          "Lycaonia"),
    ("DERBE",           "the turning point"),
    ("ATTALIA",         "Pamphylia"),
    ("ANTIOCH_SYRIA",   "Syria — home"),
]
SEA_AFTER = {2, 4, 10}   # a sea crossing follows these route rows (1-based)

# Which route row each city lights (Antioch's start vs return resolved by flag)
ROW_OF = {"SELEUCIA": 2, "SALAMIS": 3, "PAPHOS": 4, "PERGA": 5,
          "ANTIOCH_PISIDIA": 6, "ICONIUM": 7, "LYSTRA": 8, "DERBE": 9,
          "ATTALIA": 10}

# ---------------------------------------------------------------------------
# Journey legs  (from, to, mode, trigger reading-position)
# reading position: Acts 13 verse v -> v ; Acts 14 verse v -> 52 + v
# ---------------------------------------------------------------------------

def _p(ch, v):
    return v if ch == 13 else 52 + v

# offshore waypoints (lat, lon) keep a sea leg over water instead of letting a
# straight line cut across a headland — here, hugging the south coast and
# passing north of Cyprus on the run home from Attalia to Antioch.
HOME_VOYAGE = [(36.28, 31.70), (35.85, 32.75), (35.86, 34.25), (36.02, 35.42)]

# (from, to, mode, trigger reading-position, waypoints)
LEGS = [
    ("ANTIOCH_SYRIA", "SELEUCIA", "land", _p(13, 4), []),
    ("SELEUCIA", "SALAMIS", "sea", _p(13, 5), []),
    ("SALAMIS", "PAPHOS", "land", _p(13, 6), []),
    ("PAPHOS", "PERGA", "sea", _p(13, 13), []),
    ("PERGA", "ANTIOCH_PISIDIA", "land", _p(13, 14), []),
    ("ANTIOCH_PISIDIA", "ICONIUM", "land", _p(13, 51), []),
    ("ICONIUM", "LYSTRA", "land", _p(14, 6), []),
    ("LYSTRA", "DERBE", "land", _p(14, 20), []),
    ("PERGA", "ATTALIA", "land", _p(14, 25), []),           # the return begins
    ("ATTALIA", "ANTIOCH_SYRIA", "sea", _p(14, 26), HOME_VOYAGE),
]


def leg_pts(frm, to, way=()):
    return ([MF.pt(*CITIES[frm][1:3])]
            + [MF.pt(la, lo) for la, lo in way]
            + [MF.pt(*CITIES[to][1:3])])

# ---------------------------------------------------------------------------
# Per-verse story:  (chapter, verse) -> (focus city key, caption)
# ---------------------------------------------------------------------------

STORY = {
    (13, 1): ("ANTIOCH_SYRIA", "The church at Antioch has its prophets and teachers — among them Barnabas and Saul."),
    (13, 2): ("ANTIOCH_SYRIA", "As they worship and fast, the Spirit: “Set apart Barnabas and Saul for the work.”"),
    (13, 3): ("ANTIOCH_SYRIA", "With fasting, prayer, and the laying on of hands, they are sent away."),
    (13, 4): ("SELEUCIA", "Sent out by the Spirit, they go down to Seleucia and sail for Cyprus."),
    (13, 5): ("SALAMIS", "At Salamis they preach in the synagogues; John Mark is their attendant."),
    (13, 6): ("PAPHOS", "Across the island to Paphos — they meet Bar-Jesus, a sorcerer and false prophet."),
    (13, 7): ("PAPHOS", "The proconsul Sergius Paulus summons them, wanting to hear God’s word."),
    (13, 8): ("PAPHOS", "Elymas the sorcerer opposes them, twisting the proconsul from the faith."),
    (13, 9): ("PAPHOS", "Saul — also called Paul — filled with the Spirit, fastens his eyes on him."),
    (13, 10): ("PAPHOS", "“You son of the devil, enemy of all righteousness — will you not stop?”"),
    (13, 11): ("PAPHOS", "Struck blind by the hand of the Lord, Elymas gropes for a hand to lead him."),
    (13, 12): ("PAPHOS", "The proconsul believes, astonished at the teaching of the Lord."),
    (13, 13): ("PERGA", "They sail to Perga in Pamphylia; John Mark leaves and returns to Jerusalem."),
    (13, 14): ("ANTIOCH_PISIDIA", "On to Antioch of Pisidia; on the Sabbath they sit in the synagogue."),
    (13, 15): ("ANTIOCH_PISIDIA", "The rulers invite them: “If you have a word of exhortation, speak.”"),
    (13, 16): ("ANTIOCH_PISIDIA", "Paul stands: “Men of Israel, and you who fear God, listen.”"),
    (13, 17): ("ANTIOCH_PISIDIA", "The sermon: God chose the fathers and led Israel out of Egypt."),
    (13, 18): ("ANTIOCH_PISIDIA", "…he bore with them about forty years in the wilderness."),
    (13, 19): ("ANTIOCH_PISIDIA", "…he destroyed seven nations and gave them the land as inheritance."),
    (13, 20): ("ANTIOCH_PISIDIA", "…and gave them judges, until Samuel the prophet."),
    (13, 21): ("ANTIOCH_PISIDIA", "…then Saul son of Kish, of Benjamin, for forty years."),
    (13, 22): ("ANTIOCH_PISIDIA", "…and David, “a man after my own heart, who will do all my will.”"),
    (13, 23): ("ANTIOCH_PISIDIA", "From David’s offspring God has brought Israel a Savior, Jesus."),
    (13, 24): ("ANTIOCH_PISIDIA", "John had first preached repentance to Israel before his coming."),
    (13, 25): ("ANTIOCH_PISIDIA", "“I am not he; one comes after me whose sandal I am unworthy to untie.”"),
    (13, 26): ("ANTIOCH_PISIDIA", "“To us the word of this salvation has been sent.”"),
    (13, 27): ("ANTIOCH_PISIDIA", "Jerusalem’s rulers, not knowing him, fulfilled the prophets in condemning him."),
    (13, 28): ("ANTIOCH_PISIDIA", "Finding no cause of death, they asked Pilate to have him killed."),
    (13, 29): ("ANTIOCH_PISIDIA", "All being fulfilled, they took him down and laid him in a tomb."),
    (13, 30): ("ANTIOCH_PISIDIA", "But God raised him from the dead."),
    (13, 31): ("ANTIOCH_PISIDIA", "He appeared many days to those who came with him from Galilee."),
    (13, 32): ("ANTIOCH_PISIDIA", "“We bring you good news of the promise made to the fathers.”"),
    (13, 33): ("ANTIOCH_PISIDIA", "“…God has fulfilled it by raising Jesus: You are my Son.”"),
    (13, 34): ("ANTIOCH_PISIDIA", "“I will give you the holy and sure blessings of David.”"),
    (13, 35): ("ANTIOCH_PISIDIA", "“You will not let your Holy One see decay.”"),
    (13, 36): ("ANTIOCH_PISIDIA", "David served his generation, fell asleep, and saw decay —"),
    (13, 37): ("ANTIOCH_PISIDIA", "— but the one whom God raised up saw no decay."),
    (13, 38): ("ANTIOCH_PISIDIA", "“Through this man forgiveness of sins is proclaimed to you.”"),
    (13, 39): ("ANTIOCH_PISIDIA", "“By him everyone who believes is justified — as the law could not.”"),
    (13, 40): ("ANTIOCH_PISIDIA", "“Beware, lest what is spoken in the prophets come upon you.”"),
    (13, 41): ("ANTIOCH_PISIDIA", "“Behold, you scoffers — I work a work you would never believe.”"),
    (13, 42): ("ANTIOCH_PISIDIA", "As they leave, the people beg to hear these words the next Sabbath."),
    (13, 43): ("ANTIOCH_PISIDIA", "Many Jews and devout proselytes follow Paul and Barnabas."),
    (13, 44): ("ANTIOCH_PISIDIA", "The next Sabbath almost the whole city gathers to hear God’s word."),
    (13, 45): ("ANTIOCH_PISIDIA", "The Jews, filled with jealousy, contradict Paul and blaspheme."),
    (13, 46): ("ANTIOCH_PISIDIA", "“It was necessary to speak to you first — now we turn to the Gentiles.”"),
    (13, 47): ("ANTIOCH_PISIDIA", "“I have set you as a light for the Gentiles, to the ends of the earth.”"),
    (13, 48): ("ANTIOCH_PISIDIA", "The Gentiles rejoice; as many as were appointed to life believe."),
    (13, 49): ("ANTIOCH_PISIDIA", "The word of the Lord spreads through the whole region."),
    (13, 50): ("ANTIOCH_PISIDIA", "Stirred-up leaders raise persecution and drive them out of their borders."),
    (13, 51): ("ICONIUM", "They shake the dust off their feet against them and come to Iconium."),
    (13, 52): ("ICONIUM", "And the disciples were filled with joy and with the Holy Spirit."),
    (14, 1): ("ICONIUM", "At Iconium a great many, both Jews and Greeks, believe."),
    (14, 2): ("ICONIUM", "But unbelieving Jews embitter the Gentiles against the brothers."),
    (14, 3): ("ICONIUM", "They stay a long time; the Lord grants signs and wonders by their hands."),
    (14, 4): ("ICONIUM", "The city is divided — part with the Jews, part with the apostles."),
    (14, 5): ("ICONIUM", "A violent attempt is made to mistreat and stone them —"),
    (14, 6): ("LYSTRA", "— so they flee to the Lycaonian cities: Lystra, Derbe, and around."),
    (14, 7): ("LYSTRA", "And there they keep preaching the Good News."),
    (14, 8): ("LYSTRA", "At Lystra a man crippled from birth, who never walked, sits listening."),
    (14, 9): ("LYSTRA", "Paul, fastening his eyes on him, sees he has faith to be made whole."),
    (14, 10): ("LYSTRA", "“Stand upright on your feet!” — he leaps up and walks."),
    (14, 11): ("LYSTRA", "The crowds cry in Lycaonian: “The gods have come down to us as men!”"),
    (14, 12): ("LYSTRA", "They call Barnabas “Jupiter” and Paul “Mercury,” the chief speaker."),
    (14, 13): ("LYSTRA", "The priest of Jupiter brings oxen and garlands to sacrifice to them."),
    (14, 14): ("LYSTRA", "The apostles tear their clothes and rush into the crowd, crying out:"),
    (14, 15): ("LYSTRA", "“We are only men! Turn from these vain things to the living God.”"),
    (14, 16): ("LYSTRA", "“…who let all the nations walk in their own ways in past generations,”"),
    (14, 17): ("LYSTRA", "“…yet gave witness — rains, fruitful seasons, food, and gladness.”"),
    (14, 18): ("LYSTRA", "Even so, they scarcely stop the crowds from sacrificing to them."),
    (14, 19): ("LYSTRA", "Jews from Antioch and Iconium come; they stone Paul and leave him for dead."),
    (14, 20): ("DERBE", "But he rises; the next day he and Barnabas go on to Derbe."),
    (14, 21): ("ANTIOCH_PISIDIA", "Having made many disciples in Derbe, they turn back through Lystra, Iconium, and Antioch."),
    (14, 22): ("ANTIOCH_PISIDIA", "…strengthening the disciples: “through many afflictions we enter God’s Kingdom.”"),
    (14, 23): ("ANTIOCH_PISIDIA", "They appoint elders in every church, with prayer and fasting."),
    (14, 24): ("PERGA", "They pass through Pisidia and come to Pamphylia."),
    (14, 25): ("ATTALIA", "Having spoken the word in Perga, they go down to Attalia."),
    (14, 26): ("ANTIOCH_SYRIA", "From there they sail back to Antioch, where they were commended to grace."),
    (14, 27): ("ANTIOCH_SYRIA", "They gather the church and report a door of faith opened to the nations."),
    (14, 28): ("ANTIOCH_SYRIA", "And they stay there a long time with the disciples."),
}

# scene notes (two lines) keyed by the first verse of the scene's run
SCENES = [
    ((13, 1), ["Sent by the Spirit from", "the church at Antioch."]),
    ((13, 4), ["First field: Cyprus,", "Barnabas’ home island."]),
    ((13, 6), ["Paphos: Elymas struck blind;", "the proconsul believes."]),
    ((13, 13), ["Crossing to the mainland;", "John Mark turns back."]),
    ((13, 14), ["In the synagogue Paul preaches", "Israel’s story, fulfilled in Jesus."]),
    ((13, 42), ["Jews grow jealous; they turn", "to the Gentiles, then are expelled."]),
    ((14, 1), ["Iconium: many believe,", "but a plot to stone them forms."]),
    ((14, 6), ["Lystra: a cripple healed;", "the crowds take them for gods."]),
    ((14, 19), ["Paul is stoned, yet rises", "and presses on to Derbe."]),
    ((14, 21), ["Retracing their steps,", "strengthening every church."]),
    ((14, 24), ["Back through Pamphylia", "to the port of Attalia."]),
    ((14, 26), ["Home to Antioch: a door of", "faith opened to the nations."]),
]


def scene_note(ch, v):
    p = _p(ch, v)
    chosen = SCENES[0][1]
    for (sch, sv), lines in SCENES:
        if _p(sch, sv) <= p:
            chosen = lines
    return chosen


def is_returning(ch, v):
    return ch == 14 and v >= 21

# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def _len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1])
               for a, b in zip(pts, pts[1:]))


def point_dir(pts, frac):
    """Point at `frac` of the arc length, plus the local unit direction."""
    total = _len(pts) or 1.0
    target = total * frac
    run = 0.0
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if run + seg >= target and seg > 0:
            t = (target - run) / seg
            px = a[0] + (b[0] - a[0]) * t
            py = a[1] + (b[1] - a[1]) * t
            ux, uy = (b[0] - a[0]) / seg, (b[1] - a[1]) / seg
            return (px, py), (ux, uy)
        run += seg
    a, b = pts[-2], pts[-1]
    seg = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    return b, ((b[0] - a[0]) / seg, (b[1] - a[1]) / seg)


def arrow(c, pts, color, frac=0.55, size=7):
    (px, py), (ux, uy) = point_dir(pts, frac)
    nx, ny = -uy, ux
    tip = (px + ux * size, py + uy * size)
    back = (px - ux * size * 0.6, py - uy * size * 0.6)
    left = (back[0] + nx * size * 0.6, back[1] + ny * size * 0.6)
    right = (back[0] - nx * size * 0.6, back[1] - ny * size * 0.6)
    c.polygon([tip, left, right], fill=color)


def draw_legs(c, ch, v):
    p = _p(ch, v)
    # upcoming legs first (dashed dim underlay), then travelled solid legs,
    # then the current leg tracing itself on top.
    current = None
    for frm, to, mode, trig, way in LEGS:
        pts = leg_pts(frm, to, way)
        if trig > p:
            c.polyline(pts, stroke=SAND_DIM + (255,), width=1.5, dash=DASH_UP)
        elif trig < p:
            if mode == "sea":
                c.polyline(pts, stroke=RIVER, width=2.5, dash=DASH_SEA)
                arrow(c, pts, RIVER, size=6)
            else:
                c.polyline(pts, stroke=SAND + (255,), width=3)
                arrow(c, pts, SAND)
        else:
            current = (pts, mode)
    if current:
        pts, mode = current
        c.polyline(pts, stroke=SAND_DIM + (255,), width=1, dash=DASH_UP)
        c.traced(pts, stroke=g(0.95), width=4, dur="2.4s")


def draw_cities(c, ch, v):
    focus_key = STORY[(ch, v)][0]
    p = _p(ch, v)
    # a city is "reached" once any leg ending there has fired (or it's the
    # start), so past stops read as solid and the road ahead stays dim.
    reached = {"ANTIOCH_SYRIA"}
    for frm, to, mode, trig, way in LEGS:
        if trig <= p:
            reached.add(to)
            reached.add(frm)
    for key, (label, la, lo, (dx, dy, anch)) in CITIES.items():
        x, y = MF.pt(la, lo)
        cur = (key == focus_key)
        if cur:
            c.circle(x, y, 7, fill=HL, stroke=BG, width=2)
            c.circle(x, y, 11, stroke=g(0.9), width=2)
        elif key in reached:
            c.circle(x, y, 4, fill=SAND, stroke=BG, width=1)
        else:
            c.circle(x, y, 3.5, fill=SEA, stroke=SAND_DIM, width=1.5)
        fill = HL if cur else (TEXT if key in reached else TEXT_DIM)
        c.text((x + dx, y + dy), label, 15 if cur else 14, fill, anch,
               bold=cur)


def compass_scale(c):
    x, y = MF.mw - 26, MF.mh - 66
    c.line((x, y + 22), (x, y), TEXT_DIM, 2)
    c.line((x - 5, y + 8), (x, y), TEXT_DIM, 2)
    c.line((x + 5, y + 8), (x, y), TEXT_DIM, 2)
    c.text((x - 10, y + 2), "N", 14, TEXT_DIM, "rm")
    bar = 50 * MF.s / 111.0
    bx, by = MF.mw - 18 - bar, MF.mh - 18
    c.line((bx, by), (bx + bar, by), TEXT_DIM, 2)
    c.line((bx, by - 3), (bx, by + 3), TEXT_DIM, 2)
    c.line((bx + bar, by - 3), (bx + bar, by + 3), TEXT_DIM, 2)
    c.text((bx + bar / 2, by - 6), "50 km", 14, TEXT_DIM, "mb", italic=True)


# ---------------------------------------------------------------------------
# Side panel — the itinerary as a vertical route strip
# ---------------------------------------------------------------------------

ROW0, ROWH = 168, 27


def draw_panel(c, ch, v):
    focus_key = STORY[(ch, v)][0]
    returning = is_returning(ch, v)
    if focus_key == "ANTIOCH_SYRIA":
        cur_row = 11 if returning else 1
    else:
        cur_row = ROW_OF[focus_key]

    c.text((PANEL_X, 108), "PAUL’S FIRST JOURNEY", 20, TEXT, "la",
           bold=True)
    c.text((PANEL_X, 134), "Acts 13–14  ·  about AD 46–48", 14,
           TEXT_DIM, "la", italic=True)

    dot_x, name_x = PANEL_X + 9, PANEL_X + 26
    top_y = ROW0
    bot_y = ROW0 + (len(ROUTE) - 1) * ROWH
    # the spine
    c.line((dot_x, top_y), (dot_x, bot_y), SAND_DIM, 2)

    for i, (key, tag) in enumerate(ROUTE, start=1):
        y = ROW0 + (i - 1) * ROWH
        label = CITIES[key][0]
        cur = (i == cur_row)
        # a sea crossing between this row and the next
        if i in SEA_AFTER:
            c.line((dot_x, y + 4), (dot_x, y + ROWH - 4), RIVER, 2,
                   dash="2,4")
        if cur:
            c.circle(dot_x, y, 6, fill=HL, stroke=BG, width=1)
        else:
            c.circle(dot_x, y, 4, fill=SAND if i < cur_row or (returning and i > cur_row) else SEA,
                     stroke=SAND_DIM, width=1.5)
        name_fill = HL if cur else TEXT
        c.text((name_x, y - 6), label, 15 if cur else 14, name_fill, "lm",
               bold=cur)
        c.text((name_x, y + 8), tag, 11, TEXT_DIM, "lm", italic=True)

    if returning:
        c.text((PANEL_X, bot_y + 24), "↩  returning to Antioch", 13, HL,
               "la", italic=True)

    # scene note
    ny = bot_y + 52
    for line in scene_note(ch, v):
        c.text((PANEL_X, ny), line, 14, TEXT_DIM, "la", italic=True)
        ny += 20


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

def render(ch, v):
    focus_key, caption = STORY[(ch, v)]
    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 20), f"Paul’s First Missionary Journey — Acts {ch}",
           24, TEXT, "la", bold=True)
    c.text((28, 54), f"verse {v} — {caption}", 17, HL, "la", italic=True)
    c.text((28, H - 22), FOOTER, 13, TEXT_DIM, "la", italic=True)

    with c.group(MF.px, MF.py, clip=(MF.mw, MF.mh)):
        c.rect(0, 0, MF.mw, MF.mh, fill=SEA)
        c.polygon(MF.pts(MAINLAND), fill=LAND, stroke=SAND_DIM, width=2)
        c.polygon(MF.pts(CYPRUS), fill=LAND, stroke=SAND_DIM, width=2)

        for la, lo, txt, anch in REGIONS:
            c.text(MF.pt(la, lo), txt, 13, TEXT_DIM, anch)
        for la, lo, txt, anch in WATERS:
            c.text(MF.pt(la, lo), txt, 14, WATER_TXT, anch, italic=True)

        draw_legs(c, ch, v)
        draw_cities(c, ch, v)
        compass_scale(c)
    c.rect(MF.px - 1, MF.py - 1, MF.mw + 1, MF.mh + 1, stroke=SAND_DIM, width=1)

    draw_panel(c, ch, v)
    return c


def main():
    total = 0
    count = 0
    for ch, last in ((13, 52), (14, 28)):
        for v in range(1, last + 1):
            c = render(ch, v)
            out = out_path("Acts", ch, f"Acts_{ch}_{v}.svg")
            c.save(out)
            total += os.path.getsize(out)
            count += 1
    print(f"Acts 13-14: {count} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
