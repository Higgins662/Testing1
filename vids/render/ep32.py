import sys, math, random
import numpy as np
from PIL import Image, ImageDraw
from pf import *

STYLE = 'jazz'
lines, durs, starts, DUR = timeline('ep32', gap=0.28, gaps={0: 0.45, 2: 0.32, 4: 0.3, 6: 0.38})
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={0: ['PUB', 'JOKE'], 1: ['2003,'], 3: ['30'], 6: ['WORLD.'], 7: ['DARE.']})
END_TAG = starts[-1] + durs[-1] + 0.35

STACHE = (78, 52, 36)
SKIN = [(236, 196, 160), (198, 150, 112), (150, 104, 76), (222, 176, 140), (176, 128, 96)]
SHIRT = [(120, 150, 110), (170, 110, 90), (90, 110, 150), (200, 170, 100), (140, 110, 150), (110, 140, 140)]
HAIR = [(60, 44, 34), (120, 84, 50), (40, 34, 36), (170, 130, 80), (90, 60, 40)]

# ------------------------------------------------------------ mustaches (canvas 240x120, centre 120,60)
HALF = {
    'handlebar': [(120, 50), (96, 46), (72, 52), (54, 62), (38, 58), (28, 44), (34, 34), (40, 44), (44, 56), (58, 70), (90, 70), (120, 62)],
    'walrus': [(120, 40), (90, 38), (62, 46), (46, 68), (48, 94), (62, 86), (74, 96), (90, 86), (104, 94), (120, 80)],
    'pencil': [(120, 54), (80, 52), (56, 56), (80, 61), (120, 60)],
    'chevron': [(120, 42), (84, 40), (60, 50), (54, 76), (84, 70), (120, 72)],
    'horseshoe': [(120, 44), (84, 42), (62, 52), (54, 108), (66, 110), (74, 64), (120, 60)],
    'brush': [(120, 46), (86, 44), (64, 50), (60, 70), (90, 72), (120, 70)],
}
KINDS = list(HALF)

def full(kind):
    h = HALF[kind]
    return h + [(240 - x, y) for x, y in reversed(h)]

def mustache(pen, kind, col=STACHE):
    pen.poly(full(kind), col, w=4, amp=1.0)
    if kind in ('walrus', 'brush', 'chevron'):
        for k in range(7):
            x = 70 + 16 * k
            pen.line([(x, 52), (x + 3, 66)], (110, 80, 58), 2.5, amp=0.3)

# ------------------------------------------------------------ people (canvas 220x330)
def person(pen, i, smile=True):
    sk, sh, hr = SKIN[i % 5], SHIRT[i % 6], HAIR[(i * 3) % 5]
    pen.poly([(40, 330), (52, 220), (110, 196), (168, 220), (180, 330)], sh, w=4.5)
    pen.poly([(92, 196), (110, 230), (128, 196)], (240, 236, 226), w=3)
    pen.ell(110, 120, 66, 74, fill=sk, w=4.5)
    style = i % 4
    if style == 0:
        pen.poly([(48, 104), (60, 58), (110, 42), (160, 58), (172, 104), (150, 84), (110, 76), (70, 84)], hr, w=3.5)
    elif style == 1:
        pen.ell(110, 64, 62, 26, fill=hr, w=3.5)
    elif style == 2:
        pen.poly([(52, 96), (70, 54), (150, 54), (168, 96), (166, 70), (110, 46), (54, 70)], hr, w=3.5)
        pen.ell(110, 50, 70, 16, fill=(60, 70, 96), w=3.5)
    else:
        pen.poly([(46, 120), (56, 60), (110, 40), (164, 60), (174, 120), (160, 92), (110, 70), (60, 92)], hr, w=3.5)
    for ex in (86, 134):
        pen.dot(ex, 118, 7.5, (24, 20, 26)); pen.dot(ex + 2.5, 115, 2.5, (255, 255, 255))
    pen.dot(70, 146, 8, (232, 150, 140)); pen.dot(150, 146, 8, (232, 150, 140))
    if smile:
        pen.line([(96, 168), (110, 176), (124, 168)], OUT, 4, amp=0.3)

# ------------------------------------------------------------ props
def pint(pen):
    pen.poly([(20, 20), (100, 20), (92, 170), (28, 170)], (214, 150, 60), w=4)
    pen.poly([(20, 20), (100, 20), (100, 44), (20, 44)], (250, 242, 220), w=3.5, amp=1.6)
    pen.line([(36, 60), (40, 150)], (240, 196, 120), 5)

def pub_bg():
    img = bg_canvas([(0, (92, 60, 44)), (0.55, (120, 78, 52)), (1, (70, 46, 34))],
                    glows=[(270, 420, 420, (255, 200, 130), 0.55), (810, 420, 420, (255, 200, 130), 0.5)])
    def fn(pen):
        for x in range(0, 1100, 180):
            pen.line([(x, 0), (x, 1000)], (78, 50, 36), 5, amp=1.5)
        pen.poly([(-20, 560), (1100, 560), (1100, 600), (-20, 600)], (96, 62, 42), w=4)
        rng = random.Random(4)
        for k in range(14):
            x = 60 + k * 72
            h = rng.uniform(90, 150)
            col = rng.choice([(70, 110, 70), (120, 70, 50), (170, 140, 80), (60, 80, 110)])
            pen.poly(capsule(x, 555 - h + 20, x, 555 - 10, 18), col, w=3)
            pen.poly([(x - 6, 555 - h - 10), (x + 6, 555 - h - 10), (x + 6, 555 - h + 20), (x - 6, 555 - h + 20)], col, w=3)
        for lx in (270, 810):
            pen.line([(lx, 0), (lx, 230)], (40, 30, 26), 4)
            pen.poly([(lx - 70, 300), (lx - 40, 230), (lx + 40, 230), (lx + 70, 300)], (60, 90, 70), w=4)
            pen.ell(lx, 304, 40, 12, fill=(255, 236, 170), w=3)
        pen.poly([(-20, 1080), (1100, 1080), (1100, 1180), (-20, 1180)], (120, 76, 46), w=5)
        pen.poly([(-20, 1180), (1100, 1180), (1100, 1940), (-20, 1940)], (64, 42, 30), w=4)
        for x in range(40, 1080, 160):
            pen.line([(x, 1110), (x + 90, 1110)], (150, 100, 64), 3)
    return make_sprite(W, H, fn, seed=2, base=img)

def street_bg():
    img = bg_canvas([(0, (120, 186, 232)), (0.5, (204, 228, 240)), (1, (204, 228, 240))], glows=[(820, 260, 300, (255, 248, 210), 0.8)])
    def fn(pen):
        pen.ell(820, 260, 90, 90, fill=(255, 226, 140), w=4)
        cols = [(214, 186, 150), (190, 150, 120), (226, 210, 180), (170, 140, 130), (200, 176, 140)]
        x = -20
        for k, (wd, ht) in enumerate([(220, 520), (200, 420), (240, 600), (210, 470), (240, 540)]):
            pen.poly([(x, 1060), (x, 1060 - ht), (x + wd, 1060 - ht), (x + wd, 1060)], cols[k], w=4.5)
            for r in range(int(ht / 120)):
                for c in range(2):
                    wx, wy = x + 40 + c * (wd - 110), 1060 - ht + 50 + r * 120
                    pen.poly([(wx, wy), (wx + 50, wy), (wx + 50, wy + 70), (wx, wy + 70)], (150, 190, 214), w=3)
            x += wd
        pen.poly([(-20, 1060), (1100, 1060), (1100, 1940), (-20, 1940)], (120, 118, 124), w=4)
        pen.poly([(-20, 1060), (1100, 1060), (1100, 1110), (-20, 1110)], (190, 184, 176), w=4)
        for y in (1290, 1330):
            pen.line([(-20, y), (1100, y)], (80, 78, 84), 6, amp=0.5)
        pen.line([(-20, 600), (1100, 590)], (50, 46, 50), 3, amp=0.5)
    return make_sprite(W, H, fn, seed=3, base=img)

def tram(pen):
    pen.poly(rrect(20, 100, 680, 330, 30), (60, 130, 90), w=5)
    pen.poly([(20, 250), (680, 250), (680, 290), (20, 290)], (240, 226, 186), w=3.5)
    for k in range(6):
        x = 50 + k * 104
        pen.poly(rrect(x, 130, x + 80, 220, 10), (170, 214, 232), w=3.5)
    pen.poly([(300, 100), (300, 60), (400, 60), (400, 100)], (50, 110, 76), w=4)
    pen.line([(350, 60), (470, 8)], (50, 46, 50), 5)
    for wx in (140, 560):
        pen.ell(wx, 340, 34, 34, fill=(50, 46, 50), w=4)
        pen.dot(wx, 340, 10, (150, 150, 150))
    pen.ell(668, 220, 12, 14, fill=(255, 236, 160), w=3)

def calendar(pen, word, sub):
    pen.poly(rrect(20, 40, 440, 500, 20), (250, 248, 240), w=5)
    pen.poly([(20, 60), (440, 60), (440, 150), (20, 150)], (200, 80, 70), w=4.5)
    for x in (110, 230, 350):
        pen.ell(x, 40, 14, 26, fill=(220, 220, 220), w=3.5)
    pen.text((230, 108), sub, 44, (252, 248, 240), font=FONT_CAP)
    pen.text((230, 330), word, 150 if len(word) <= 4 else 74, (60, 48, 56), font=FONT_CAP)

def banner(pen, word):
    pen.poly([(10, 30), (590, 30), (560, 80), (590, 130), (10, 130), (40, 80)], (250, 220, 120), w=5)
    pen.text((300, 82), word, 62, (60, 40, 40), font=FONT_CAP)

# ------------------------------------------------------------ globe pieces
GLOBE_R = 300
def strip(pen):
    rng = random.Random(9)
    blobs = [(180, 220, 150, 110), (420, 300, 120, 180), (700, 200, 210, 120), (900, 380, 110, 90),
             (1120, 260, 170, 140), (1320, 420, 90, 70), (1480, 200, 140, 120)]
    for (x, y, rx, ry) in blobs:
        pts = [(x + rx * math.cos(a) * (1 + 0.22 * math.sin(3 * a + x)), y + ry * math.sin(a) * (1 + 0.2 * math.cos(2 * a + y)))
               for a in np.linspace(0, 2 * math.pi, 26)]
        pen.poly(pts, (130, 176, 110), outline=(70, 100, 64), w=4, amp=2)
STRIP_W = 1600

# ------------------------------------------------------------ fuzz mustache (canvas 320x170)
def fuzz_stache(pen):
    rng = random.Random(pen.seed)
    half = [(160, 52), (128, 42), (92, 46), (62, 64), (40, 70), (22, 56), (20, 34), (36, 22), (44, 36), (40, 50), (54, 52),
            (78, 92), (112, 104), (140, 96), (160, 84)]
    shape = half + [(320 - x, y) for x, y in reversed(half)]
    pen.poly(shape, (88, 74, 70), w=5, amp=1.6)
    for i in range(90):
        a = rng.uniform(0.08, 0.92)
        x = 30 + 260 * a
        y0 = 58 + 26 * abs(a - 0.5) * 2 * (1 if abs(a - 0.5) > 0.25 else 0.4)
        pen.line([(x, y0 + rng.uniform(-6, 14)), (x + rng.uniform(-5, 5), y0 + rng.uniform(20, 36))],
                 rng.choice([(120, 100, 92), (70, 58, 56), (140, 118, 104)]), 3, amp=0.3)
    pen.ell(160, 56, 14, 10, fill=(70, 58, 56), w=3)

# ------------------------------------------------------------ assets
print('assets...', file=sys.stderr)
PUB = pub_bg()
STREET = street_bg()
PEOPLE = [[make_sprite(220, 330, lambda p, i=i: person(p, i), seed=s) for s in (1, 2, 3)] for i in range(6)]
TINY = [make_sprite(220, 330, lambda p, i=i: person(p, i + 2, smile=False), seed=1 + i) for i in range(10)]
STACHES = {k: make_sprite(240, 120, lambda p, k=k: mustache(p, k), seed=7) for k in KINDS}
PINT = make_sprite(120, 190, pint, seed=4)
TRAM = [make_sprite(700, 380, tram, seed=s) for s in (1, 2, 3)]
CAL = make_sprite(460, 520, lambda p: calendar(p, '2003', 'MELBOURNE'), seed=5)
CAL_NOV = make_sprite(460, 520, lambda p: calendar(p, 'NOV', 'ALL MONTH'), seed=6)
BAN = make_sprite(600, 160, lambda p: banner(p, 'ABOUT 30 GUYS'), seed=8)
STRIP = make_sprite(STRIP_W, 600, strip, seed=9)
FUZZ = fuzz_sprites('happy')
FSTACHE = [make_sprite(320, 170, fuzz_stache, seed=s) for s in (1, 2, 3)]
NIGHT = downsample(bg_canvas([(0, (40, 46, 74)), (1, (22, 24, 40))], glows=[(540, 700, 700, (90, 110, 170), 0.5)]), W, H)
WARMBG = downsample(bg_canvas([(0, (120, 80, 56)), (1, (70, 46, 34))], glows=[(540, 820, 620, (255, 196, 120), 0.6)]), W, H)

_mask = Image.new('L', (2 * GLOBE_R, 2 * GLOBE_R), 0)
ImageDraw.Draw(_mask).ellipse([0, 0, 2 * GLOBE_R - 1, 2 * GLOBE_R - 1], fill=255)

def globe(rot_px, frame):
    g = Image.new('RGBA', (2 * GLOBE_R, 2 * GLOBE_R), (96, 160, 206, 255))
    off = int(rot_px) % STRIP_W
    g.alpha_composite(STRIP, (0, 0), (off, 0, min(STRIP_W, off + 2 * GLOBE_R), 600))
    if off + 2 * GLOBE_R > STRIP_W:
        g.alpha_composite(STRIP, (STRIP_W - off, 0), (0, 0, off + 2 * GLOBE_R - STRIP_W, 600))
    sh = Image.new('RGBA', g.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([GLOBE_R * 0.55, -GLOBE_R * 0.2, GLOBE_R * 2.6, GLOBE_R * 2.2], fill=(10, 20, 50, 70))
    g.alpha_composite(sh)
    out = Image.new('RGBA', g.size, (0, 0, 0, 0)); out.paste(g, (0, 0), _mask)
    d = ImageDraw.Draw(out)
    d.ellipse([3, 3, 2 * GLOBE_R - 4, 2 * GLOBE_R - 4], outline=OUT, width=8)
    return out

# ------------------------------------------------------------ scenes
B = [0] + [starts[i] - 0.15 for i in (1, 3, 5, 7)] + [DUR]

SEATS = [(250, 800), (540, 770), (830, 800)]
def s1(tl, frame, sd):
    img = PUB.copy()
    for k, (x, y) in enumerate(SEATS):
        bob = 6 * math.sin(tl * 3 + k)
        paste(img, PEOPLE[k * 2][boil(frame, off=k)], x, y + bob, 1.25)
        t0 = 1.1 + 0.35 * k
        u = ease_back(seg(tl, t0, t0 + 0.35), 2.6)
        if u > 0.02:
            kind = ['handlebar', 'walrus', 'chevron'][k]
            paste(img, STACHES[kind], x, y + (157 - 165) * 1.25 + bob, 0.6 * u, rot=4 * math.sin(tl * 9 + k) * (1 - seg(tl, t0, t0 + 1)))
            if tl < t0 + 0.5:
                d = ImageDraw.Draw(img)
                for j in range(3):
                    yy = y - 160 + bob - 30 * j * seg(tl, t0, t0 + 0.4)
                    d.line([(x - 70, yy), (x - 90, yy - 12), (x - 70, yy - 24)], fill=(250, 240, 210), width=5)
    for k, x in enumerate((180, 420, 660, 900)):
        paste(img, PINT, x, 1080, 0.9)
    return camera(img, lerp(1.04, 1.12, ease(tl / sd)), 540, 900)

def s2(tl, frame, sd):
    img = STREET.copy()
    tx = lerp(1500, -500, seg(tl, 0.3, sd + 1.5))
    paste(img, TRAM[boil(frame)], tx, 1130 + 3 * math.sin(tl * 12), 1.1)
    u = ease_back(seg(tl, 0.0, 0.5), 1.6)
    flip = seg(tl, 0.25, 0.55)
    paste(img, CAL, 540, lerp(-300, 520, u), 1.0, sy=max(0.05, abs(math.cos(math.pi * (1 - flip) / 2))) if flip < 1 else 1.0)
    return img

def s3(tl, frame, sd):
    img = STREET.copy()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, H], fill=(236, 226, 206))
    rows = [(560, 0.42), (760, 0.46), (980, 0.5)]
    n = 0
    for r, (y, sc) in enumerate(rows):
        for c in range(10):
            x = 75 + c * 103 + (r % 2) * 18
            t0 = 0.15 + n * 0.055
            u = ease_back(seg(tl, t0, t0 + 0.25), 2.2)
            if u > 0.02:
                paste(img, TINY[(n * 7) % 10], x, y + 8 * math.sin(tl * 4 + n), sc * u)
                kind = KINDS[(n * 5 + r) % len(KINDS)]
                paste(img, STACHES[kind], x, y + (157 - 165) * sc + 8 * math.sin(tl * 4 + n), sc * 0.6 * u)
            n += 1
    paste(img, BAN, 540, 300, ease_back(seg(tl, 0.3, 0.7), 2.0))
    t_nov = starts[4] - B[2]
    if tl > t_nov - 0.2:
        u = ease_back(seg(tl, t_nov - 0.2, t_nov + 0.25), 1.6)
        paste(img, CAL_NOV, 540, lerp(2300, 1180, u), 0.8, rot=-4)
    return img

PINS = [(0.12, 0.42), (0.3, 0.3), (0.45, 0.55), (0.58, 0.35), (0.7, 0.6), (0.85, 0.4), (0.22, 0.65), (0.62, 0.22), (0.4, 0.75), (0.78, 0.72)]
def s4(tl, frame, sd):
    img = NIGHT.copy()
    d = ImageDraw.Draw(img)
    rng = random.Random(2)
    for k in range(60):
        x, y = rng.uniform(0, W), rng.uniform(0, 1300)
        tw = 0.5 + 0.5 * math.sin(tl * 3 + k)
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 250, 220, int(150 + 100 * tw)))
    cx, cy = 540, 820
    img.alpha_composite(globe(tl * 160, frame), (cx - GLOBE_R, cy - GLOBE_R))
    for k, (px, py) in enumerate(PINS):
        t0 = 0.4 + k * 0.35
        u = ease_back(seg(tl, t0, t0 + 0.3), 2.4)
        if u > 0.02:
            x = cx - GLOBE_R + px * 2 * GLOBE_R; y = cy - GLOBE_R + py * 2 * GLOBE_R
            paste(img, STACHES[KINDS[k % len(KINDS)]], x, y, 0.5 * u, rot=8 * math.sin(tl * 5 + k))
    t_world = starts[6] - B[3]
    if tl > t_world:
        glow(img, cx, cy, 420, (255, 220, 160), 0.35 * seg(tl, t_world, t_world + 0.5))
        for k in range(8):
            a = 2 * math.pi * k / 8 + tl
            sparkle(img, cx + 360 * math.cos(a), cy + 360 * math.sin(a), 22 * seg(tl, t_world, t_world + 0.4))
    return img

def s5(tl, frame, sd):
    img = WARMBG.copy()
    u = ease_back(seg(tl, 0.0, 0.45), 1.8)
    sc = 2.1 * u
    fx, fy = 540, 860 + 10 * math.sin(tl * 3)
    paste(img, FUZZ[boil(frame)], fx, fy, sc)
    if u > 0.05:
        droop = 6 * math.sin(tl * 4)
        paste(img, FSTACHE[boil(frame)], fx, fy + (180 - 150) * sc, sc * 0.72 * ease_back(seg(tl, 0.35, 0.8), 2.6), rot=droop)
    return img

SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate([s1, s2, s3, s4, s5])]
EP = Episode('ep32', SCENES, CHUNKS, DUR, END_TAG)

def audio_plan():
    import pf_audio as A
    sfx = [(A.rustle(), 0.05, 1.0, 0), (A.crowd(B[1]), 0.0, 0.45, 0)]
    sfx += [(A.boing(), 1.1 + 0.35 * k, 0.55, (-0.4, 0, 0.4)[k]) for k in range(3)]
    sfx += [(A.whoosh(0.4), B[1] + 0.05, 0.6, 0), (A.rustle(0.3), B[1] + 0.3, 0.6, 0)]
    sfx += [(A.chime(1318.5), B[1] + 0.9, 0.35, 0.3), (A.chime(1318.5), B[1] + 1.15, 0.3, 0.3), (A.engine(2.0, 60), B[1] + 0.6, 0.25, 0)]
    sfx += [(A.pop(), B[2] + 0.15 + n * 0.055, 0.18, (n % 5 - 2) * 0.2) for n in range(0, 30, 2)]
    sfx += [(A.whoosh(0.4, False), starts[4] - 0.2, 0.5, 0)]
    sfx += [(A.whoosh(0.8), B[3] + 0.05, 0.6, 0)] + [(A.pop(), B[3] + 0.4 + k * 0.35, 0.3, 0) for k in range(10)]
    sfx += [(A.sparkles(), starts[6], 0.4, 0)]
    sfx += [(A.boing(), B[4] + 0.4, 0.6, 0), (A.pop(), END_TAG, 0.7, 0), (A.chime(1318.5), END_TAG + 0.05, 0.4, 0)]
    cues = [(f'/home/claude/eps/ep32_vo_{i}.wav', s) for i, s in enumerate(starts)]
    return cues, sfx

if __name__ == '__main__':
    if sys.argv[1] == 'audio':
        import pf_audio as A
        cues, sfx = audio_plan()
        A.build(DUR, cues, sfx, '/home/claude/eps/ep32/audio.wav', style=STYLE)
        print('audio ok')
    else:
        EP.main(sys.argv)
