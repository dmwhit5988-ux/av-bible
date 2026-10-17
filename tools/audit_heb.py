import glob, os, re, sys
# Run from anywhere: the repo is this file's parent folder.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from svg_vocab import text_w
W, H = 1024, 576
CH = {1: 14, 2: 18, 3: 19, 4: 16, 5: 14, 6: 20, 7: 28, 8: 13, 9: 28,
      10: 39, 11: 40, 12: 29, 13: 25}
TEXT_RE = re.compile(r'<text ([^>]*)>(.*?)</text>', re.S)
ATTR = re.compile(r'(\S+)="([^"]*)"')

def boxes(src):
    out = []
    for attrs, body in TEXT_RE.findall(src):
        a = dict(ATTR.findall(attrs))
        s = (body.replace('&amp;', '&').replace('&lt;', '<')
             .replace('&gt;', '>').replace('&#39;', "'").replace('&quot;', '"'))
        if not s.strip():
            continue
        size = float(a.get('font-size', 12))
        bold = a.get('font-weight') == 'bold'
        it = a.get('font-style') == 'italic'
        w = text_w(s, size, bold=bold, italic=it)
        x, y = float(a['x']), float(a['y'])
        an = a.get('text-anchor', 'start')
        x0 = x if an == 'start' else (x - w / 2 if an == 'middle' else x - w)
        out.append((x0, y - size * 0.62, w, size * 1.16, s))
    return out

def ov(a, b):
    return not (a[0] + a[2] <= b[0] or b[0] + b[2] <= a[0]
                or a[1] + a[3] <= b[1] or b[1] + b[3] <= a[1])

off = coll = 0
prev = None
runs = []
run = 1
runstart = None
for ch in sorted(CH):
    d = f'visuals/Hebrews/{ch}'
    if not os.path.isdir(d):
        continue
    for v in range(1, CH[ch] + 1):
        p = f'{d}/Hebrews_{ch}_{v}.svg'
        if not os.path.exists(p):
            continue
        src = open(p, encoding='utf-8').read()
        bs = boxes(src)
        for b in bs:
            if b[0] < 0 or b[1] < 0 or b[0] + b[2] > W or b[1] + b[3] > H:
                off += 1
                print(f'  {ch}:{v} OFF x={b[0]:.0f} y={b[1]:.0f} '
                      f'w={b[2]:.0f} {b[4]!r}')
        for i in range(len(bs)):
            for j in range(i + 1, len(bs)):
                if ov(bs[i], bs[j]):
                    coll += 1
                    print(f'  {ch}:{v} OVERLAP {bs[i][4]!r} x {bs[j][4]!r}')
        body = re.sub(r'<text[^>]*>v\d+</text>', '', src)
        if prev is not None and body == prev:
            run += 1
        else:
            if run > 3:
                runs.append((run, runstart))
            run = 1
            runstart = f'{ch}:{v}'
        prev = body
if run > 3:
    runs.append((run, runstart))
print(f'\noff-canvas {off} | overlaps {coll}')
for r, at in runs:
    print(f'  identical run of {r} from {at}')
if not runs:
    print('  no identical run longer than 3')
