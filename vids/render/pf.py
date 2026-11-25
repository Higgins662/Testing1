"""Pocketfuzzy shared animation library."""
import math, random, sys, os, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_CAP = '/home/claude/vid/lucky.woff'
FONT_HAND = '/home/claude/vid/patrick.woff'
OUT = (24, 21, 30)

# ------------------------------------------------------------ math helpers
def clamp(x, a, b): return max(a, min(b, x))
def ease(t): t = clamp(t, 0, 1); return t * t * (3 - 2 * t)
def ease_out(t): t = clamp(t, 0, 1); return 1 - (1 - t) ** 3
def ease_in(t): t = clamp(t, 0, 1); return t ** 3
def ease_back(t, s=1.9):
    t = clamp(t, 0, 1) - 1
    return t * t * ((s + 1) * t + s) + 1
def lerp(a, b, t): return a + (b - a) * t
def seg(t, a, b): return clamp((t - a) / max(1e-6, b - a), 0, 1)

def ellpts(cx, cy, rx, ry, rot=0, n=None, a0=0, a1=360):
    n = n or max(28, int((rx + ry) / 3))
    a = math.radians(rot); ca, sa = math.cos(a), math.sin(a)
    out = []
    full = (a1 - a0) >= 360
    cnt = n if full else n + 1
    for i in range(cnt):
        t = math.radians(a0 + (a1 - a0) * i / n)
        x, y = rx * math.cos(t), ry * math.sin(t)
        out.append((cx + x * ca + y * sa, cy - x * sa + y * ca))
    return out

def capsule(x0, y0, x1, y1, r, n=12):
    ang = math.atan2(y1 - y0, x1 - x0)
    pts = []
    for i in range(n + 1):
        a = ang - math.pi / 2 + math.pi * i / n
        pts.append((x1 + r * math.cos(a), y1 + r * math.sin(a)))
    for i in range(n + 1):
        a = ang + math.pi / 2 + math.pi * i / n
        pts.append((x0 + r * math.cos(a), y0 + r * math.sin(a)))
    return pts

def rrect(x0, y0, x1, y1, r, n=6):
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def xform(pts, dx=0, dy=0, s=1, rot=0):
    a = math.radians(rot); ca, sa = math.cos(a), math.sin(a)
    return [(dx + s * (x * ca - y * sa), dy + s * (x * sa + y * ca)) for x, y in pts]

# ------------------------------------------------------------ pen
class Pen:
    def __init__(self, img, ss, seed=0):
        self.img = img; self.d = ImageDraw.Draw(img); self.ss = ss
        self.seed = seed; self.k = 0

    def _wob(self, pts, amp, closed):
        self.k += 1
        n = len(pts); out = []
        segs = n if closed else n - 1
        for i in range(segs):
            x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % n]
            L = math.hypot(x1 - x0, y1 - y0); k = max(1, int(L / 9))
            for j in range(k):
                t = j / k; out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
        if not closed: out.append(pts[-1])
        if amp > 0:
            rng = random.Random(self.seed * 1000003 + self.k * 7919)
            p1, p2, p3 = (rng.uniform(0, 6.283) for _ in range(3))
            f1, f2 = rng.uniform(0.18, 0.33), rng.uniform(0.05, 0.11)
            out = [(x + amp * (0.6 * math.sin(i * f1 + p1) + 0.4 * math.sin(i * f2 + p2)),
                    y + amp * (0.6 * math.sin(i * f1 + p3) + 0.4 * math.cos(i * f2 + p1)))
                   for i, (x, y) in enumerate(out)]
        return [(x * self.ss, y * self.ss) for x, y in out]

    def poly(self, pts, fill=None, outline=OUT, w=4, amp=1.2, closed=True):
        p = self._wob(pts, amp, closed)
        if fill is not None and closed and len(p) > 2:
            self.d.polygon(p, fill=fill)
        if outline is not None and w > 0:
            lw = max(1, int(w * self.ss))
            self.d.line(p + ([p[0]] if closed else []), fill=outline, width=lw, joint='curve')
            if not closed:
                r = lw / 2
                for (x, y) in (p[0], p[-1]):
                    self.d.ellipse([x - r, y - r, x + r, y + r], fill=outline)
        return p

    def line(self, pts, color=OUT, w=4, amp=1.0):
        return self.poly(pts, None, color, w, amp, closed=False)

    def ell(self, cx, cy, rx, ry, rot=0, fill=None, outline=OUT, w=4, amp=1.2):
        return self.poly(ellpts(cx, cy, rx, ry, rot), fill, outline, w, amp)

    def dot(self, cx, cy, r, fill):
        s = self.ss
        self.d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=fill)

    def silhouette(self, shapes, fill, outline=OUT, w=4, amp=1.2):
        ps = [self._wob(s, amp, True) for s in shapes]
        lw = max(1, int(2 * w * self.ss))
        for p in ps:
            self.d.polygon(p, fill=outline)
            self.d.line(p + [p[0]], fill=outline, width=lw, joint='curve')
        for p in ps:
            self.d.polygon(p, fill=fill)

    def text(self, xy, s, size, fill, font=FONT_CAP, anchor='mm', stroke=0, stroke_fill=None, rot=0):
        f = ImageFont.truetype(font, int(size * self.ss))
        if not rot:
            self.d.text((xy[0] * self.ss, xy[1] * self.ss), s, font=f, fill=fill, anchor=anchor,
                        stroke_width=int(stroke * self.ss), stroke_fill=stroke_fill)
            return
        tmp = Image.new('RGBA', self.img.size, (0, 0, 0, 0))
        ImageDraw.Draw(tmp).text((xy[0] * self.ss, xy[1] * self.ss), s, font=f, fill=fill, anchor=anchor,
                                 stroke_width=int(stroke * self.ss), stroke_fill=stroke_fill)
        tmp = tmp.rotate(rot, center=(xy[0] * self.ss, xy[1] * self.ss), resample=Image.BICUBIC)
        self.img.alpha_composite(tmp)

# ------------------------------------------------------------ images
def downsample(img, w, h):
    return img.convert('RGBa').resize((w, h), Image.LANCZOS).convert('RGBA')

def make_sprite(w, h, fn, seed=0, ss=2, base=None):
    img = base if base is not None else Image.new('RGBA', (w * ss, h * ss), (0, 0, 0, 0))
    pen = Pen(img, ss, seed)
    fn(pen)
    return downsample(img, w, h)

def vgrad(w, h, stops):
    ys = np.linspace(0, 1, h)
    cols = np.zeros((h, 3))
    for c in range(3):
        cols[:, c] = np.interp(ys, [s[0] for s in stops], [s[1][c] for s in stops])
    return np.repeat(cols[:, None, :], w, axis=1)

def radial_add(arr, cx, cy, r, color, strength):
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    m = np.clip(1 - d, 0, 1) ** 2 * strength
    arr += m[..., None] * (np.array(color)[None, None, :] - arr)
    return arr

def to_rgba(arr):
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')

def bg_canvas(stops, glows=(), ss=2):
    arr = vgrad(W * ss, H * ss, stops)
    for (cx, cy, r, col, st) in glows:
        arr = radial_add(arr, cx * ss, cy * ss, r * ss, col, st)
    return to_rgba(arr)

def paste(dst, spr, cx, cy, scale=1.0, rot=0.0, alpha=1.0, flip=False, sx=None, sy=None):
    if spr is None or scale <= 0.01: return
    s = spr
    if flip: s = s.transpose(Image.FLIP_LEFT_RIGHT)
    if scale != 1.0 or sx or sy:
        fx = scale * (sx or 1.0); fy = scale * (sy or 1.0)
        nw, nh = max(1, int(s.width * fx)), max(1, int(s.height * fy))
        s = s.convert('RGBa').resize((nw, nh), Image.BICUBIC).convert('RGBA')
    if rot:
        s = s.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1.0:
        a = s.getchannel('A').point(lambda v: int(v * max(0, alpha)))
        s = s.copy(); s.putalpha(a)
    x, y = int(round(cx - s.width / 2)), int(round(cy - s.height / 2))
    if x >= dst.width or y >= dst.height or x + s.width <= 0 or y + s.height <= 0: return
    dst.alpha_composite(s, (max(0, x), max(0, y)), (max(0, -x), max(0, -y)))

def sparkle(dst, cx, cy, size, alpha=1.0, color=(255, 240, 190)):
    if size < 1: return
    lay = Image.new('RGBA', (int(size * 2.6) + 4, int(size * 2.6) + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = lay.width / 2
    pts = []
    for i in range(8):
        a = math.pi / 4 * i
        r = size if i % 2 == 0 else size * 0.22
        pts.append((c + r * math.cos(a - math.pi / 2), c + r * math.sin(a - math.pi / 2)))
    d.polygon(pts, fill=color + (int(255 * alpha),))
    d.ellipse([c - size * 0.18, c - size * 0.18, c + size * 0.18, c + size * 0.18], fill=(255, 255, 255, int(255 * alpha)))
    dst.alpha_composite(lay, (int(cx - c), int(cy - c)))

def glow(dst, cx, cy, r, color, alpha):
    if alpha <= 0.01: return
    size = int(r * 2)
    yy, xx = np.mgrid[0:size, 0:size]
    d = np.sqrt((xx - r) ** 2 + (yy - r) ** 2) / r
    arr = np.zeros((size, size, 4), np.float32)
    arr[..., 0], arr[..., 1], arr[..., 2] = color
    arr[..., 3] = np.clip(1 - d, 0, 1) ** 2 * alpha * 255
    lay = Image.fromarray(arr.astype(np.uint8), 'RGBA')
    tmp = Image.new('RGBA', dst.size, (0, 0, 0, 0))
    tmp.paste(lay, (int(cx - r), int(cy - r)))
    dst.alpha_composite(tmp)

def camera(img, zoom, cx, cy):
    if zoom <= 1.0001: return img
    w, h = W / zoom, H / zoom
    x0 = clamp(cx - w / 2, 0, W - w); y0 = clamp(cy - h / 2, 0, H - h)
    return img.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))

def shake(img, amt, frame):
    if amt <= 0: return img
    r = random.Random(frame)
    dx, dy = int(r.uniform(-amt, amt)), int(r.uniform(-amt, amt))
    out = Image.new('RGBA', img.size, (0, 0, 0, 255))
    out.alpha_composite(img, (max(0, dx), max(0, dy)), (max(0, -dx), max(0, -dy)))
    return out

def boil(frame, n=3, rate=4, off=0):
    return (frame // rate + off) % n

# ------------------------------------------------------------ the Fuzz (armless)
FUZZ = (143, 163, 184)
def draw_fuzz(pen, mood='happy'):
    rng = random.Random(pen.seed * 31 + 5)
    cx, cy, r = 150, 168, 92
    pen.ell(cx, cy, r, r, fill=FUZZ, outline=None, amp=2)
    for i in range(110):
        a = 2 * math.pi * i / 110 + rng.uniform(-0.03, 0.03)
        r0 = r - rng.uniform(4, 14); r1 = r + rng.uniform(6, 18)
        col = rng.choice([(122, 142, 165), (171, 188, 205), (104, 122, 146), (150, 170, 190)])
        pen.line([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)),
                  (cx + r1 * math.cos(a + rng.uniform(-0.06, 0.06)), cy + r1 * math.sin(a + rng.uniform(-0.06, 0.06)))],
                 col, 4.5, amp=0.6)
    for i in range(70):
        a = rng.uniform(0, 6.283); rr = rng.uniform(0, r - 18)
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        b = rng.uniform(0, 6.283)
        pen.line([(x, y), (x + 9 * math.cos(b), y + 9 * math.sin(b))],
                 rng.choice([(128, 148, 170), (165, 182, 200)]), 3, amp=0.3)
    if mood == 'shock':
        for ex in (116, 184):
            pen.dot(ex, 145, 22, (250, 248, 240)); pen.ell(ex, 145, 22, 22, fill=None, w=3, amp=0.3)
            pen.dot(ex, 148, 8, (14, 14, 20))
        pen.ell(150, 200, 14, 18, fill=(40, 24, 36), w=3, amp=0.3)
    else:
        for ex in (118, 182):
            pen.dot(ex, 150, 15, (14, 14, 20)); pen.dot(ex + 5, 145, 5, (255, 255, 255))
        grin = [(118 + i * 3.5, 184 + 20 * math.sin(math.pi * i / 20)) for i in range(21)]
        pen.line(grin, (30, 24, 36), 6, amp=0.4)
        pen.poly([(160, 200), (172, 201), (166, 214)], (250, 248, 240), w=2.5, amp=0.2)
    pen.dot(100, 182, 11, (214, 150, 160)); pen.dot(200, 182, 11, (214, 150, 160))

def fuzz_sprites(mood='happy'):
    return [make_sprite(300, 300, lambda p: draw_fuzz(p, mood), seed=s) for s in (1, 2, 3)]

# ------------------------------------------------------------ timeline from VO
def timeline(ep, first=0.35, gap=0.28, gaps=None, tail=2.3):
    durs = json.load(open(os.path.join(HERE, f'{ep}_durs.json')))
    lines = json.load(open(os.path.join(HERE, f'{ep}_lines.json')))
    starts = []; t = first
    for i, d in enumerate(durs):
        starts.append(round(t, 3))
        g = (gaps or {}).get(i, gap)
        t += d + g
    end = starts[-1] + durs[-1]
    return lines, durs, starts, round(end + tail, 2)

def chunks_from(lines, durs, starts, dur_total, emph=None):
    ch = []
    for i, (ln, d, s) in enumerate(zip(lines, durs, starts)):
        t1 = starts[i + 1] - 0.06 if i + 1 < len(starts) else s + d + 0.5
        ch.append(dict(t0=max(0, s - 0.05), t1=t1, text=ln['cap'], vs=s, vd=d, emph=(emph or {}).get(i)))
    return ch

# ------------------------------------------------------------ captions + overlays
_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

HL = (255, 211, 107)
def draw_caption(img, t, chunks, end_tag_at):
    d = ImageDraw.Draw(img)
    for c in chunks:
        if not (c['t0'] <= t < c['t1']): continue
        size = 74
        f = font(FONT_CAP, size)
        words = c['text'].upper().split(' ')
        lines, cur = [], []
        for w_ in words:
            test = ' '.join(cur + [w_])
            if cur and d.textlength(test, font=f) > 900:
                lines.append(cur); cur = [w_]
            else:
                cur.append(w_)
        lines.append(cur)
        weights = [len(w_) + 2 for w_ in words]
        tot = sum(weights)
        prog = clamp((t - c['vs']) / c['vd'], 0, 0.999) * tot
        acc, active = 0, 0
        for i, wt in enumerate(weights):
            if prog >= acc: active = i
            acc += wt
        emph = set(x.upper() for x in (c.get('emph') or []))
        lh = int(size * 1.18)
        cy0 = 1360 - (len(lines) - 1) * lh / 2
        pop = ease_back(clamp((t - c['t0']) / 0.18, 0, 1), 2.2)
        yoff = (1 - pop) * 24
        sp = d.textlength(' ', font=f)
        idx = 0
        for li, line in enumerate(lines):
            widths = [d.textlength(w_, font=f) for w_ in line]
            total = sum(widths) + sp * (len(line) - 1)
            x = W / 2 - total / 2
            y = cy0 + li * lh + yoff
            for w_, ww in zip(line, widths):
                bare = ''.join(ch for ch in w_ if ch.isalnum() or ch in "'")
                hl = (idx == active) or (bare in emph)
                col = HL if hl else (252, 248, 240)
                d.text((x + 4, y + 6), w_, font=f, fill=(20, 16, 26), anchor='lm', stroke_width=9, stroke_fill=(20, 16, 26))
                d.text((x, y), w_, font=f, fill=col, anchor='lm', stroke_width=9, stroke_fill=(24, 20, 30))
                x += ww + sp; idx += 1
    if t >= end_tag_at:
        u = ease_back(clamp((t - end_tag_at) / 0.35, 0, 1), 2.0)
        f = font(FONT_HAND, int(104 * max(0.2, u)))
        d.text((W / 2, 1375), 'pocketfuzzy', font=f, fill=(252, 240, 214), anchor='mm', stroke_width=8, stroke_fill=(24, 20, 30))
        if t > end_tag_at + 0.3:
            d.text((W / 2, 1290), 'did you know?', font=font(FONT_HAND, 46), fill=HL, anchor='mm', stroke_width=6, stroke_fill=(24, 20, 30))

def build_watermark():
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((48, 1530), 'pocketfuzzy', font=font(FONT_HAND, 60), fill=(252, 240, 214, 255), anchor='ls',
           stroke_width=4, stroke_fill=(24, 20, 30, 255))
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * 0.7)))
    return lay
WATERMARK = build_watermark()

_rngg = np.random.default_rng(1)
GRAIN = [(_rngg.normal(0, 5.5, (H, W, 1))).astype(np.float32) for _ in range(6)]
_yy, _xx = np.mgrid[0:H, 0:W]
_d = np.sqrt(((_xx - W / 2) / (W * 0.75)) ** 2 + ((_yy - H / 2) / (H * 0.72)) ** 2)
VIG = np.clip(1.0 - 0.28 * np.clip(_d - 0.35, 0, 1) ** 1.4, 0.6, 1)[..., None].astype(np.float32)
WARM = np.array([1.02, 1.0, 0.96], np.float32)

# ------------------------------------------------------------ episode runner
class Episode:
    def __init__(self, name, scenes, chunks, dur, end_tag_at, xf=0.34, loop=False):
        self.name, self.scenes, self.chunks, self.dur = name, scenes, chunks, dur
        self.end_tag_at, self.xf, self.loop = end_tag_at, xf, loop

    def scene_frame(self, t, frame):
        S = self.scenes
        for i, (s0, s1, fn) in enumerate(S):
            if s0 <= t < s1 or (i == len(S) - 1 and t >= s0):
                img = fn(t - s0, frame, s1 - s0).convert('RGB')
                if i + 1 < len(S) and t >= s1 - self.xf:
                    n0, n1, nfn = S[i + 1]
                    nxt = nfn(max(0.0, t - n0), frame, n1 - n0).convert('RGB')
                    img = Image.blend(img, nxt, ease((t - (s1 - self.xf)) / self.xf))
                return img

    def render(self, frame):
        t = frame / FPS
        img = self.scene_frame(t, frame).convert('RGBA')
        draw_caption(img, t, self.chunks, self.end_tag_at)
        img.alpha_composite(WATERMARK)
        arr = np.asarray(img.convert('RGB')).astype(np.float32)
        arr = arr * VIG * WARM + GRAIN[(frame // 2) % len(GRAIN)]
        if not self.loop:   # loop episodes skip the fade so the last frame flows into the first
            if t < 0.2: arr *= ease(t / 0.2)
            if t > self.dur - 0.4: arr *= 1 - 0.85 * ease((t - (self.dur - 0.4)) / 0.4)
        return np.clip(arr, 0, 255).astype(np.uint8)

    def boundaries(self):
        """split frames into ~equal encode parts aligned to scene starts"""
        return [(s0, (self.scenes[i + 1][0] if i + 1 < len(self.scenes) else self.dur)) for i, (s0, _, _) in enumerate(self.scenes)]

    def main(self, argv):
        mode = argv[1]
        outdir = os.path.join(HERE, self.name); os.makedirs(outdir, exist_ok=True)
        if mode == 'preview':
            for ts in argv[2].split(','):
                fr = int(round(float(ts) * FPS))
                Image.fromarray(self.render(fr)).save(os.path.join(outdir, f'p_{ts}.jpg'), quality=88)
            print('preview ok', file=sys.stderr)
        elif mode == 'part':
            i = int(argv[2])
            s0, s1 = self.boundaries()[i]
            f0, f1 = int(round(s0 * FPS)), int(round(s1 * FPS))
            out = os.path.join(outdir, f'part{i}.mp4'); tmp = os.path.join(outdir, f'part{i}.tmp.mp4')
            p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                                  '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast',
                                  '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
            for fr in range(f0, f1):
                p.stdin.write(self.render(fr).tobytes())
            p.stdin.close()
            if p.wait() == 0:
                os.replace(tmp, out); print('done part', i, file=sys.stderr)
            else:
                sys.exit(1)
        elif mode == 'nparts':
            print(len(self.scenes))
        elif mode == 'dur':
            print(self.dur)
