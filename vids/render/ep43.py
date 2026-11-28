"""Ep 43 Itchy Hair Darts (standard): many New World tarantulas kick barbed, itchy hairs off their abdomen
(Bertani & Guadanucci 2013, Zoologia; WCS 2015)."""
import sys, math, random
from PIL import Image, ImageDraw
from pf import *

NAME = 'ep43'
STYLE = 'lofi'
FORMAT = 'standard'
LOOP = FORMAT == 'loop'
lines, durs, starts, DUR = timeline(NAME, first=0.15, gap=0.26, gaps={0: 0.34, 3: 0.32}, tail=0.42 if LOOP else 2.3)
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={0: ['ITCHY', 'BUTTS.'], 1: ['BARBED'], 3: ['DARTS'], 4: ['VENOM,'], 5: ['EGG', 'SACS.'], 6: ['ARMOR']})
END_TAG = DUR + 99 if LOOP else starts[-1] + durs[-1] + 0.35
HOOK = 'ITCHY BUTT HAIRS'

BROWN = (104, 74, 54)
BROWN_D = (78, 54, 40)
BROWN_L = (150, 110, 78)
PATCH = (204, 150, 92)
GOLD = (238, 206, 140)
FOX = (222, 124, 62)
FOX_D = (180, 92, 44)
CREAM = (250, 236, 214)
DENIM = (82, 112, 160)
DENIM_D = (62, 88, 132)
STITCH = (232, 164, 84)
MOSS = (110, 140, 84)
MOSS_D = (80, 108, 64)

def overlay(img, text, u, y=270, size=104):
    if u <= 0.02: return
    ImageDraw.Draw(img).text((540, y), text, font=font(FONT_CAP, int(size * u)), fill=HL,
                             anchor='mm', stroke_width=11, stroke_fill=OUT)

# ------------------------------------------------------------ backgrounds
def _forest(rock=True):
    img = bg_canvas([(0, (150, 132, 176)), (0.45, (196, 170, 186)), (0.62, (214, 196, 170)), (1, (120, 100, 76))],
                    glows=[(780, 520, 560, (255, 228, 180), 0.55)])
    def fn(pen):
        for k, x in enumerate((-40, 170, 900, 1080)):                     # far tree trunks
            pen.poly([(x - 50, 1500), (x - 30, 200), (x + 30, 180), (x + 60, 1500)], (118 + k * 4, 104, 112), w=5, amp=2)
        for k in range(9):                                                 # ferns / leaf clumps
            x = 40 + k * 130
            pen.ell(x, 1290 + 20 * math.sin(k * 1.7), 110, 50, fill=(MOSS_D if k % 2 else MOSS), w=4, amp=2)
        pen.poly([(-20, 1300), (1100, 1270), (1100, 1940), (-20, 1940)], (122, 96, 70), w=6, amp=1.5)   # damp ground
        for k in range(26):
            x = (k * 97) % 1080; y = 1360 + (k * 53) % 420
            pen.line([(x, y), (x + 26, y - 6)], (98, 76, 56), 4, amp=0.8)
        if rock:
            pen.poly([(220, 1240), (290, 1110), (520, 1080), (790, 1120), (870, 1250), (820, 1330), (260, 1340)], (128, 134, 124), w=6, amp=2.5)
            pen.poly([(300, 1150), (520, 1110), (760, 1150), (720, 1180), (330, 1180)], MOSS, outline=None, amp=2)
    return make_sprite(W, H, fn, seed=3, base=img)
FOREST = _forest(True)
GROUND = _forest(False)
PLAIN = downsample(bg_canvas([(0, (238, 214, 190)), (1, (206, 178, 150))], glows=[(540, 800, 620, (255, 240, 214), 0.6)]), W, H)

# ------------------------------------------------------------ sprites
SW, SH = 560, 380          # tarantula canvas, side view facing right; ground at y~352
HIP4 = (300, 238)

def _leg(pen, pts, col, w=13):
    pen.line(pts, OUT, w + 6, amp=0.8)
    pen.line(pts, col, w, amp=0.8)
    for (x, y) in pts[1:-1]:
        pen.dot(x, y, w * 0.55, BROWN_L)

def tarantula(pen):
    _leg(pen, [(410, 222), (470, 150), (545, 350)], BROWN_D)              # far-side legs (behind the body)
    _leg(pen, [(370, 228), (390, 140), (430, 352)], BROWN_D)
    _leg(pen, [(330, 232), (290, 150), (250, 352)], BROWN_D)
    _leg(pen, [(290, 236), (190, 210), (60, 352)], BROWN_D)
    pen.ell(190, 180, 128, 100, fill=BROWN, w=6)                          # abdomen
    rng = random.Random(pen.seed)
    for i in range(80):                                                    # fuzzy outline
        a = 2 * math.pi * i / 80
        r0, r1 = rng.uniform(0.86, 0.96), rng.uniform(1.03, 1.12)
        pen.line([(190 + 128 * r0 * math.cos(a), 180 + 100 * r0 * math.sin(a)),
                  (190 + 128 * r1 * math.cos(a), 180 + 100 * r1 * math.sin(a))], BROWN_L, 3, amp=0.4)
    pen.ell(178, 112, 72, 30, fill=PATCH, outline=BROWN_D, w=3, amp=1)     # the urticating patch on top
    for i in range(18):
        x = 120 + i * 6.5
        pen.line([(x, 104 + 6 * math.sin(i)), (x + 3, 92 + 4 * math.sin(i * 1.3))], GOLD, 2.5, amp=0.3)
    pen.ell(372, 196, 86, 62, fill=BROWN_D, w=6)                           # cephalothorax
    pen.line([(330, 170), (410, 168)], BROWN_L, 3, amp=0.5)
    pen.ell(452, 222, 22, 26, fill=(60, 42, 34), w=4)                      # chelicerae
    _leg(pen, [(446, 232), (500, 232), (520, 300)], BROWN, w=10)           # pedipalp
    _leg(pen, [(420, 228), (488, 158), (552, 352)], BROWN)                 # near-side legs 1-3
    _leg(pen, [(390, 236), (420, 150), (462, 352)], BROWN)
    _leg(pen, [(352, 240), (322, 160), (282, 352)], BROWN)
    for ex, ey, r in ((404, 146, 15), (434, 150, 13)):                     # big cute eyes
        pen.dot(ex, ey, r, (14, 14, 20)); pen.dot(ex + 4, ey - 5, r * 0.35, (255, 255, 255))
    for ex, ey in ((388, 158), (452, 160), (420, 136)):
        pen.dot(ex, ey, 4, (14, 14, 20))
SPIDER = [make_sprite(SW, SH, tarantula, seed=s) for s in (1, 2, 3)]

def leg4(img, cx, cy, sc, k, flip=False):
    """the near-side back leg, drawn live; k = 0 resting on the ground .. 1 kicked up over the patch"""
    rest = [(HIP4[0], HIP4[1]), (200, 222), (84, 352)]
    kick = [(HIP4[0], HIP4[1]), (250, 108), (118, 56)]
    pts = [(lerp(a[0], b[0], k), lerp(a[1], b[1], k)) for a, b in zip(rest, kick)]
    sx = -1 if flip else 1
    scr = [(cx + sx * (x - SW / 2) * sc, cy + (y - SH / 2) * sc) for x, y in pts]
    d = ImageDraw.Draw(img)
    d.line(scr, fill=OUT, width=int(19 * sc), joint='curve')
    d.line(scr, fill=BROWN, width=int(13 * sc), joint='curve')
    x, y = scr[1]; r = 7 * sc
    d.ellipse([x - r, y - r, x + r, y + r], fill=BROWN_L)

def spider(img, cx, cy, sc, k, frame, flip=False):
    paste(img, SPIDER[boil(frame)], cx, cy, sc, flip=flip)
    leg4(img, cx, cy, sc, k, flip)

def patch_xy(cx, cy, sc, flip=False):
    return cx + (-1 if flip else 1) * (178 - SW / 2) * sc, cy + (100 - SH / 2) * sc

def darts(img, ox, oy, t, ang, n=26, spread=0.9, speed=(380, 760), seed=1, life=1.8, sc=1.0):
    """a puff of tiny barbed hairs emitted at t=0 from (ox, oy) toward angle ang (radians)"""
    if t <= 0 or t > life: return
    rng = random.Random(seed)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    sp = []
    for i in range(n):
        a = ang + rng.uniform(-spread, spread) * 0.5
        v = rng.uniform(*speed)
        tt = t * rng.uniform(0.85, 1.1)
        dist = v * (1 - math.exp(-tt * 2.2)) / 2.2                       # air drag
        x = ox + math.cos(a) * dist + 14 * math.sin(tt * 5 + i)
        y = oy + math.sin(a) * dist + 60 * tt * tt
        fade = 1 - seg(t, life * 0.65, life)
        L = 16 * sc
        dx, dy = math.cos(a) * L, math.sin(a) * L
        d.line([(x - dx, y - dy), (x + dx, y + dy)], fill=GOLD + (int(255 * fade),), width=max(2, int(3 * sc)))
        for b in (-0.4, 0.1):                                             # barbs
            bx, by = x + dx * b, y + dy * b
            d.line([(bx, by), (bx - dx * 0.4 + dy * 0.35, by - dy * 0.4 - dx * 0.35)], fill=GOLD + (int(255 * fade),), width=2)
        if i % 6 == 0 and fade > 0.2:
            sp.append((x, y, fade))
    img.alpha_composite(lay)
    for x, y, fade in sp:
        sparkle(img, x, y, 12 * sc * fade, alpha=fade)

def pocket(pen):              # canvas 300x260
    shape = [(20, 40), (280, 40), (272, 190), (150, 246), (28, 190)]
    pen.poly(shape, DENIM, w=5)
    pen.line([(20, 66), (280, 66)], DENIM_D, 4, amp=0.5)
    inner = [(42, 84), (258, 84), (252, 180), (150, 224), (48, 180), (42, 84)]
    for i in range(len(inner) - 1):
        (x0, y0), (x1, y1) = inner[i], inner[i + 1]
        n = int(math.hypot(x1 - x0, y1 - y0) / 18)
        for k in range(0, n, 2):
            pen.line([(lerp(x0, x1, k / n), lerp(y0, y1, k / n)), (lerp(x0, x1, (k + 1) / n), lerp(y0, y1, (k + 1) / n))], STITCH, 3.5, amp=0.2)
POCKET = [make_sprite(300, 260, pocket, seed=s) for s in (1, 2, 3)]
FUZZ = fuzz_sprites('happy')
FUZZ_W = fuzz_sprites('shock')

def twig(pen):                # canvas 520x200
    pen.line([(520, 60), (300, 90), (120, 120), (20, 150)], (96, 70, 50), 18, amp=1.5)
    pen.line([(300, 90), (250, 30)], (96, 70, 50), 9, amp=1)
    pen.ell(230, 26, 34, 16, rot=-30, fill=MOSS, w=3)
TWIG = make_sprite(520, 200, twig, seed=4)

def fuzz_pocket(img, x, y, tl, frame, shock=False, peek=1.0):
    paste(img, (FUZZ_W if shock else FUZZ)[boil(frame)], x, y - 60 * peek + 6 * math.sin(tl * 5), 0.5)
    paste(img, POCKET[boil(frame)], x, y + 40, 0.75)

def fox(pen, mood='sniff'):   # canvas 560x440, fox head facing left (snout to the left)
    pen.poly([(300, 90), (350, 0), (400, 110)], FOX, w=5)                                   # ears
    pen.poly([(410, 100), (500, 20), (500, 150)], FOX_D, w=5)
    pen.poly([(325, 80), (350, 30), (378, 96)], (60, 40, 40), outline=None, amp=0.4)
    pen.ell(380, 240, 160, 150, fill=FOX, w=6)                                              # head
    pen.poly([(250, 170), (40, 236), (60, 262), (250, 320)], FOX, w=6)                      # snout
    pen.poly([(240, 270), (70, 262), (110, 300), (260, 340), (360, 330)], CREAM, outline=None, amp=1)
    pen.ell(52, 246, 26, 22, fill=(30, 24, 28), w=4)                                        # nose
    pen.dot(46, 238, 6, (120, 110, 120))
    for k in range(3):
        pen.line([(150, 262 + k * 12), (70 - k * 10, 300 + k * 22)], OUT, 2.5, amp=0.4)       # whiskers
    if mood == 'sneeze':
        pen.line([(250, 170), (282, 182), (250, 194)], OUT, 6, amp=0.4)                     # squeezed eye
        pen.line([(240, 300), (210, 290)], OUT, 4)
    else:
        pen.ell(268, 182, 22, 26, fill=(250, 246, 236), w=4)
        pen.dot(260, 186, 12, (20, 18, 24)); pen.dot(256, 180, 4, (255, 255, 255))
        if mood == 'teary':
            pen.ell(250, 222, 10, 16, fill=(150, 200, 240), w=2.5)
FOX_SNIFF = [make_sprite(560, 440, fox, seed=s) for s in (1, 2, 3)]
FOX_SNEEZE = [make_sprite(560, 440, lambda p: fox(p, 'sneeze'), seed=s) for s in (1, 2, 3)]
FOX_TEARY = [make_sprite(560, 440, lambda p: fox(p, 'teary'), seed=s) for s in (1, 2, 3)]

def paw(pen):                 # canvas 220x160
    pen.ell(110, 90, 96, 60, fill=FOX_D, w=5)
    pen.ell(110, 110, 70, 34, fill=(60, 40, 36), outline=None, amp=0.6)
    for x in (60, 100, 140):
        pen.line([(x, 60), (x + 8, 130)], OUT, 3)
PAW = make_sprite(220, 160, paw, seed=5)

def egg_sac(pen):             # canvas 360x340
    rng = random.Random(pen.seed + 3)
    pen.ell(180, 180, 150, 140, fill=(244, 238, 224), w=5, amp=2)
    for i in range(30):
        a0 = rng.uniform(0, 6.28); r = rng.uniform(30, 140)
        pts = [(180 + r * math.cos(a0 + j * 0.25), 180 + r * 0.9 * math.sin(a0 + j * 0.25)) for j in range(6)]
        pen.line(pts, (210, 204, 190), 2.5, amp=0.8)
    for i in range(26):
        a = rng.uniform(0, 6.28); r = rng.uniform(20, 130)
        x, y = 180 + r * math.cos(a), 180 + r * 0.9 * math.sin(a)
        b = rng.uniform(0, 6.28)
        pen.line([(x, y), (x + 14 * math.cos(b), y + 14 * math.sin(b))], (214, 170, 100), 3, amp=0.2)
SAC = [make_sprite(360, 340, egg_sac, seed=s) for s in (1, 2, 3)]

def bubble(img, cx, cy, r, u):
    if u <= 0.02: return
    rr = r * u
    d = ImageDraw.Draw(img)
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(252, 244, 226), outline=OUT, width=8)
    # one giant barbed hair inside
    x0, y0, x1, y1 = cx - 0.62 * rr, cy + 0.5 * rr, cx + 0.6 * rr, cy - 0.55 * rr
    d.line([(x0, y0), (x1, y1)], fill=(190, 140, 80), width=max(2, int(16 * u)))
    d.polygon([(x1, y1), (x1 - 40 * u, y1 + 10 * u), (x1 - 12 * u, y1 + 38 * u)], fill=(190, 140, 80), outline=OUT)
    for k in range(7):
        f = 0.2 + k * 0.1
        bx, by = lerp(x0, x1, f), lerp(y0, y1, f)
        for s in (-1, 1):
            d.line([(bx, by), (bx - 34 * u + s * 26 * u, by + 30 * u + s * 26 * u)], fill=(170, 120, 66), width=max(2, int(7 * u)))

# ------------------------------------------------------------ scenes
B = [0, starts[1] - 0.12, starts[2] - 0.12, starts[4] - 0.12, starts[5] - 0.12, DUR]

def kick(t, t0, dur=0.7):
    return math.sin(math.pi * seg(t, t0, t0 + dur))

SX, SY, SS = 560, 1060, 1.3    # spider on the rock

def s1(tl, frame, sd):        # HOOK: mid-kick on frame 0, a glittery puff already flying
    img = FOREST.copy()
    paste(img, TWIG, 820, 640, 1.0)
    fuzz_pocket(img, 800, 700, tl, frame, shock=tl < 1.2, peek=ease_back(seg(tl, 0.1, 0.6)))
    k = max(kick(tl, -0.35), kick(tl, 2.0))
    spider(img, SX, SY, SS, k, frame)
    px, py = patch_xy(SX, SY, SS)
    darts(img, px, py, tl + 0.4, -2.4, seed=1)
    darts(img, px, py, tl - 2.25, -2.3, seed=2)
    return camera(img, lerp(1.12, 1.02, ease(tl / sd)), 560, 960)

def s2(tl, frame, sd):        # BARBED HAIRS: zoom into the patch, then one hair up close
    img = FOREST.copy()
    spider(img, SX, SY, SS, 0, frame)
    px, py = patch_xy(SX, SY, SS)
    glow(img, px, py + 20, 160, (255, 230, 150), 0.5 + 0.3 * math.sin(tl * 6))
    img = camera(img, lerp(1.0, 2.3, ease(seg(tl, 0, 1.2))), px, py + 60)
    bubble(img, 560, 800, 300, ease_back(seg(tl, 1.3, 1.8), 1.5))
    if tl > 1.8:
        for k in range(3):
            sparkle(img, 560 + 240 * math.cos(tl * 1.5 + k * 2.1), 800 + 240 * math.sin(tl * 1.5 + k * 2.1), 20)
    overlay(img, 'BARBED HAIRS', ease_back(seg(tl, 0.3, 0.6)))
    return img

FX0 = 1260
def s3(tl, frame, sd):        # HAIR DARTS: a fox sniffs too close; legs scrape; darts fly at the snout
    img = GROUND.copy()
    t_dart = starts[3] - B[2]
    ap = ease_out(seg(tl, 0.0, 1.6))
    fx = lerp(FX0, 900, ap) + 16 * math.sin(tl * 9) * (1 - seg(tl, t_dart, t_dart + 0.2))
    react = ease(seg(tl, t_dart + 0.4, t_dart + 0.9))
    fx += 120 * react
    cx, cy = 360, 1180
    scrape = 0.35 + 0.25 * math.sin(tl * 14) if t_dart - 1.2 < tl < t_dart else 0
    k = max(scrape, kick(tl, t_dart - 0.15, 0.6))
    spider(img, cx, cy, 1.2, k, frame, flip=True)
    paste(img, (FOX_SNIFF if react < 0.3 else FOX_TEARY)[boil(frame)], fx, 1030, 1.15)
    px, py = patch_xy(cx, cy, 1.2, flip=True)
    darts(img, px, py, tl - t_dart, -0.35, n=34, spread=0.7, speed=(520, 900), seed=3, life=2.0)
    overlay(img, 'HAIR DARTS', ease_back(seg(tl, t_dart - 0.05, t_dart + 0.3)))
    return img

def s4(tl, frame, sd):        # NO VENOM: sneeze, paw rub, watery eyes, back off
    img = PLAIN.copy()
    t_nv = durs[4] * 0.62
    sn = seg(tl, 0.5, 0.75)
    mood = FOX_SNEEZE if 0.45 < tl < 1.1 else FOX_TEARY
    jerk = -50 * math.sin(math.pi * sn)
    back = ease(seg(tl, sd - 1.3, sd - 0.2))
    fx, fy, fs = 660 + jerk + 240 * back, 980, lerp(1.45, 1.05, back)
    paste(img, mood[boil(frame)], fx, fy, fs, rot=6 * math.sin(math.pi * sn))
    nx = fx - 250 * fs; ny = fy + 26 * fs
    if 0.5 < tl < 1.3:                                                    # sneeze puffs
        u = seg(tl, 0.55, 1.3)
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        for k in range(5):
            r = 30 + 40 * u + k * 8
            paste_c = (int(255 * (1 - u)),)
            ImageDraw.Draw(lay).ellipse([nx - 60 - 160 * u - k * 40 - r, ny - 20 + (k - 2) * 50 * u - r,
                                         nx - 60 - 160 * u - k * 40 + r, ny - 20 + (k - 2) * 50 * u + r],
                                        fill=(255, 255, 255) + paste_c, outline=OUT + paste_c, width=3)
        img.alpha_composite(lay)
    if 1.3 < tl < 2.7:
        rub = math.sin((tl - 1.3) * 12)
        paste(img, PAW, nx + 90 * fs + 40 * rub, ny + 60 * fs, 1.0 * fs, rot=20 * rub)
    darts(img, nx - 120, ny - 120, tl + 0.3, 1.2, n=10, spread=2.5, speed=(60, 140), seed=5, life=3.5, sc=0.8)
    overlay(img, 'NO VENOM', ease_back(seg(tl, t_nv - 0.3, t_nv)))
    return img

def s5(tl, frame, sd):        # EGG SAC + FUZZY ARMOR payoff, the Fuzz bounces; end tag after the last line
    img = GROUND.copy()
    t_arm = starts[6] - B[4]
    paste(img, SAC[boil(frame)], 360, 1150, 1.15)
    cx, cy = 740, 1120
    k = kick(tl, t_arm + 0.05, 0.7)
    paste(img, TWIG, 820, 600, 1.0)
    spider(img, cx, cy, 1.25, k, frame, flip=True)
    # hairs drift from the spider's patch into the sac
    rng = random.Random(7)
    for i in range(14):
        u = seg(tl, 0.2 + i * 0.09, 1.2 + i * 0.09)
        if 0 < u < 1:
            px, py = patch_xy(cx, cy, 1.25, flip=True)
            x = lerp(px, 360 + rng.uniform(-90, 90), ease(u)); y = lerp(py, 1150 + rng.uniform(-80, 80), ease(u)) - 120 * math.sin(math.pi * u)
            ImageDraw.Draw(img).line([(x - 10, y - 4), (x + 10, y + 4)], fill=GOLD, width=3)
    if 0.9 < tl < 2.2:
        sparkle(img, 360 + 60 * math.sin(tl * 3), 1060, 22 * math.sin(math.pi * seg(tl, 0.9, 2.2)))
    px, py = patch_xy(cx, cy, 1.25, flip=True)
    darts(img, px, py, tl - t_arm - 0.3, -1.3, n=22, seed=9)
    bounce = abs(math.sin(tl * 4.2)) * 40 * seg(tl, t_arm, t_arm + 0.3)
    fuzz_pocket(img, 800, 660 - bounce, tl, frame, peek=ease_back(seg(tl, 0.0, 0.5)))
    overlay(img, 'FUZZY ARMOR', ease_back(seg(tl, t_arm - 0.05, t_arm + 0.3)))
    return img

SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate([s1, s2, s3, s4, s5])]
EP = Episode(NAME, SCENES, CHUNKS, DUR, END_TAG, loop=LOOP, hook=HOOK)

def audio_plan():
    import pf_audio as A
    sfx = [(A.whoosh(0.4), 0.0, 0.5, -0.2), (A.sparkles(6, 0.5), 0.1, 0.3, -0.2), (A.rustle(0.3), 0.35, 0.6, 0.4),
           (A.pop(), 0.5, 0.4, 0.4), (A.whoosh(0.4), 2.0, 0.45, -0.2), (A.sparkles(6, 0.5), 2.25, 0.3, -0.2)]
    sfx += [(A.whoosh(0.6), B[1] + 0.05, 0.45, 0), (A.tick(1400, 0.05, 0.5), B[1] + 1.3, 0.4, 0), (A.pop(), B[1] + 1.35, 0.5, 0),
            (A.sparkles(), B[1] + 1.9, 0.3, 0)]
    t3 = starts[3]
    sfx += [(A.rustle(0.5), B[2] + 0.2, 0.5, 0.5), (A.tick(700, 0.05, 0.5), B[2] + 1.0, 0.35, 0.5)]
    sfx += [(A.scribble(1.0), t3 - 1.2, 0.35, -0.2), (A.whoosh(0.5), t3 - 0.1, 0.55, 0.3), (A.sparkles(8, 0.6), t3 + 0.05, 0.35, 0.3)]
    sfx += [(A.honk(520, 0.22), B[3] + 0.55, 0.45, 0), (A.rustle(0.4), B[3] + 1.4, 0.5, 0), (A.rustle(0.4), B[3] + 2.0, 0.5, 0),
            (A.boing(), B[3] + durs[4] * 0.62, 0.45, 0), (A.whoosh(0.5, False), B[4] - 1.2, 0.35, 0.4)]
    sfx += [(A.sparkles(), B[4] + 0.9, 0.3, -0.3), (A.whoosh(0.4), starts[6] + 0.05, 0.45, 0),
            (A.pop(), starts[6] + 0.1, 0.5, 0.4), (A.chime(1046.5), starts[6] + 0.5, 0.35, 0),
            (A.pop(), END_TAG, 0.6, 0), (A.chime(1318.5), END_TAG + 0.05, 0.35, 0)]
    cues = [(f'/home/claude/eps/{NAME}_vo_{i}.wav', s) for i, s in enumerate(starts)]
    return cues, sfx

if __name__ == '__main__':
    if sys.argv[1] == 'audio':
        import pf_audio as A
        cues, sfx = audio_plan()
        A.build(DUR, cues, sfx, f'/home/claude/eps/{NAME}/audio.wav', style=STYLE, loop=LOOP)
        print('audio ok')
    elif sys.argv[1] == 'preview' and 'LAST' in sys.argv[2]:
        EP.main([sys.argv[0], 'preview', sys.argv[2].replace('LAST', f'{DUR - 1 / FPS:.3f}')])
    else:
        EP.main(sys.argv)
