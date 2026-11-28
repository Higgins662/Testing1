"""Ep 44 Krampus Night (standard): in Alpine folklore St. Nicholas has a horned sidekick, Krampus, on the night of Dec 5
(Smithsonian; National Geographic; Library of Congress Folklife Today, Dec 2025)."""
import sys, math, random
from PIL import Image, ImageDraw
from pf import *

NAME = 'ep44'
STYLE = 'bossa'
FORMAT = 'standard'
LOOP = FORMAT == 'loop'
lines, durs, starts, DUR = timeline(NAME, first=0.15, gap=0.28, gaps={0: 0.36, 3: 0.3, 4: 0.34}, tail=0.42 if LOOP else 2.3)
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={0: ['KRAMPUS'], 1: ['CLAW.'], 2: ['5TH,'], 3: ['TREATS'], 4: ['TWIGS…', 'BASKET.'], 5: ['FAST.']})
END_TAG = DUR + 99 if LOOP else starts[-1] + durs[-1] + 0.35
HOOK = "ST. NICK'S SCARY SIDEKICK"

FUR = (74, 54, 50)
FUR_D = (52, 38, 38)
FUR_L = (110, 84, 74)
HORN = (236, 222, 190)
TONGUE = (206, 76, 88)
WICKER = (184, 140, 86)
WICKER_D = (140, 100, 60)
SNOW = (236, 240, 250)
WIN = (255, 214, 130)
DENIM = (82, 112, 160)
DENIM_D = (62, 88, 132)
STITCH = (232, 164, 84)

def overlay(img, text, u, y=270, size=104):
    if u <= 0.02: return
    ImageDraw.Draw(img).text((540, y), text, font=font(FONT_CAP, int(size * u)), fill=HL,
                             anchor='mm', stroke_width=11, stroke_fill=OUT)

# ------------------------------------------------------------ backgrounds
def _village():
    img = bg_canvas([(0, (54, 58, 104)), (0.5, (104, 92, 140)), (0.75, (150, 128, 160)), (1, (200, 206, 226))],
                    glows=[(780, 380, 300, (250, 244, 220), 0.35)])
    def fn(pen):
        pen.ell(780, 380, 70, 70, fill=(246, 240, 220), outline=None, amp=1)            # moon
        rng = random.Random(4)
        for k in range(30):
            pen.dot(rng.uniform(40, 1040), rng.uniform(60, 700), rng.uniform(2, 4), (240, 236, 250))
        pen.poly([(-20, 1040), (160, 900), (300, 960), (460, 860), (640, 950), (820, 880), (1100, 960), (1100, 1300), (-20, 1300)],
                 (78, 80, 120), w=4, amp=2)                                              # mountains
        pen.poly([(160, 900), (210, 940), (120, 935)], SNOW, outline=None)
        pen.poly([(460, 860), (520, 905), (410, 900)], SNOW, outline=None)
        houses = [(110, 1060, 190, (164, 112, 96)), (360, 1020, 220, (140, 108, 120)), (640, 1050, 200, (170, 128, 98)), (900, 1030, 210, (132, 104, 112))]
        for (x, y, w, col) in houses:
            pen.poly([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + 260), (x - w / 2, y + 260)], col, w=5)
            pen.poly([(x - w / 2 - 30, y + 6), (x, y - 120), (x + w / 2 + 30, y + 6)], (96, 66, 60), w=5)
            pen.poly([(x - w / 2 - 34, y + 8), (x, y - 126), (x + w / 2 + 34, y + 8), (x + w / 2 + 6, y - 6), (x, y - 96), (x - w / 2 - 6, y - 6)], SNOW, w=4)
            for dx in (-w / 4, w / 4):
                pen.poly(rrect(x + dx - 30, y + 60, x + dx + 30, y + 130, 6), WIN, w=4)
                pen.line([(x + dx, y + 60), (x + dx, y + 130)], (150, 100, 60), 3)
        pen.poly([(-20, 1290), (300, 1270), (700, 1300), (1100, 1280), (1100, 1940), (-20, 1940)], SNOW, w=6, amp=2)
        for k in range(20):
            x = (k * 113) % 1080; y = 1360 + (k * 61) % 500
            pen.line([(x, y), (x + 40, y + 4)], (200, 210, 232), 4, amp=0.6)
    return make_sprite(W, H, fn, seed=3, base=img)
VILLAGE = _village()

def _door():
    img = bg_canvas([(0, (120, 92, 84)), (1, (84, 64, 60))], glows=[(540, 680, 520, (255, 214, 150), 0.45)])
    def fn(pen):
        for k in range(12):                                                    # wooden wall planks
            pen.line([(k * 96, 0), (k * 96 + 4, 1320)], (96, 72, 66), 4, amp=1)
        pen.poly(rrect(300, 300, 780, 1140, 20), (110, 70, 52), w=7)           # door
        for y in (440, 680, 920):
            pen.line([(330, y), (750, y)], (86, 54, 40), 5)
        pen.dot(720, 740, 16, (230, 190, 100))
        pen.poly([(200, 1130), (880, 1130), (920, 1210), (160, 1210)], (150, 150, 160), w=6)     # step
        pen.poly([(-20, 1200), (1100, 1200), (1100, 1940), (-20, 1940)], SNOW, w=6, amp=2)
        pen.poly([(160, 1200), (300, 1186), (420, 1200), (560, 1190), (700, 1202), (920, 1190), (920, 1212), (160, 1212)], SNOW, outline=None)
    return make_sprite(W, H, fn, seed=5, base=img)
DOOR = _door()
PLAIN = downsample(bg_canvas([(0, (238, 214, 186)), (1, (204, 172, 140))], glows=[(540, 800, 620, (255, 240, 214), 0.6)]), W, H)

def snowfall(img, t, n=60, seed=2):
    rng = random.Random(seed)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(n):
        x0, sp, r = rng.uniform(0, W), rng.uniform(70, 150), rng.uniform(4, 9)
        y = (rng.uniform(0, H) + sp * t) % (H + 40) - 20
        x = x0 + 30 * math.sin(t * 0.9 + i)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(250, 250, 255, 210))
    img.alpha_composite(lay)

# ------------------------------------------------------------ sprites
def krampus(pen, basket=True):     # canvas 560x660, head and shoulders, basket over the left shoulder
    if basket:
        pen.poly([(30, 140), (250, 110), (270, 330), (60, 360)], WICKER, w=6)
        for k in range(6):
            pen.line([(40 + k * 4, 170 + k * 32), (255 + k * 2, 140 + k * 32)], WICKER_D, 4, amp=0.6)
        for k in range(6):
            pen.line([(60 + k * 36, 132 - k * 4), (80 + k * 36, 350 - k * 4)], WICKER_D, 3.5, amp=0.6)
        pen.poly([(20, 140), (256, 104), (262, 124), (26, 162)], WICKER_D, w=5)     # rim
    rng = random.Random(pen.seed + 11)
    pen.ell(290, 520, 230, 170, fill=FUR, w=6)                                     # shoulders
    for i in range(70):
        a = math.pi + math.pi * i / 69
        r0, r1 = rng.uniform(0.8, 0.95), rng.uniform(1.02, 1.14)
        pen.line([(290 + 230 * r0 * math.cos(a), 520 + 170 * r0 * math.sin(a)),
                  (290 + 230 * r1 * math.cos(a + rng.uniform(-0.04, 0.04)), 520 + 170 * r1 * math.sin(a))], FUR_L, 4, amp=0.5)
    for s in (-1, 1):                                                              # curling goat horns
        pts = [(290 + s * (60 + 60 * math.sin(a)), 190 - 140 * a / 3.2 + 26 * math.sin(a * 1.6)) for a in [i * 0.16 for i in range(21)]]
        pen.line(pts, OUT, 40, amp=0.6)
        pen.line(pts, HORN, 30, amp=0.6)
        for j in range(3, 19, 3):
            x, y = pts[j]
            pen.line([(x - 12, y - 4), (x + 12, y + 4)], (200, 184, 150), 3)
        pen.poly([(290 + s * 110, 220), (290 + s * 200, 200), (290 + s * 130, 260)], FUR_L, w=5)   # ears
    pen.ell(290, 270, 130, 120, fill=FUR_L, w=6)                                   # head
    pen.ell(290, 330, 80, 56, fill=(132, 102, 90), outline=None, amp=0.8)          # muzzle
    for s in (-1, 1):
        pen.ell(290 + s * 50, 240, 34, 30, fill=(250, 214, 90), w=5)               # yellow eyes
        pen.dot(290 + s * 50 + 4, 244, 13, (20, 16, 20)); pen.dot(290 + s * 50 + 8, 236, 5, (255, 255, 255))
        pen.line([(290 + s * 20, 200), (290 + s * 86, 192)], FUR_D, 9)             # brows
    pen.ell(290, 300, 16, 11, fill=(40, 26, 30), w=3)                              # nose
    grin = [(220 + i * 7, 340 + 26 * math.sin(math.pi * i / 20)) for i in range(21)]
    pen.poly(grin + [(360, 340), (220, 340)], (60, 24, 34), w=5, amp=0.4)
    for fx_ in (236, 344):
        pen.poly([(fx_ - 8, 342), (fx_ + 8, 342), (fx_, 362)], (250, 248, 236), w=2.5, amp=0.2)
    for i in range(16):                                                            # beard fur
        x = 210 + i * 10
        pen.line([(x, 380 + 6 * math.sin(i)), (x + rng.uniform(-6, 6), 420 + 14 * math.sin(i * 1.7))], FUR_D, 5, amp=0.5)
KRAMPUS = [make_sprite(560, 660, krampus, seed=s) for s in (1, 2, 3)]

def tongue(img, cx, cy, sc, t):
    """long lolling tongue, drawn live so it wags"""
    wag = 0.25 * math.sin(t * 5)
    x0, y0 = cx + (290 - 280) * sc, cy + (360 - 330) * sc
    pts = [(x0 + 30 * sc * math.sin(wag + k * 0.25) * k / 6, y0 + k * 22 * sc) for k in range(7)]
    d = ImageDraw.Draw(img)
    d.line(pts, fill=OUT, width=int(40 * sc), joint='curve')
    d.line(pts, fill=TONGUE, width=int(30 * sc), joint='curve')
    x, y = pts[-1]; r = 15 * sc
    d.ellipse([x - r - 4, y - r - 4, x + r + 4, y + r + 4], fill=OUT); d.ellipse([x - r, y - r, x + r, y + r], fill=TONGUE)

def basket(pen):                  # canvas 300x320, the wicker basket alone, lid on top
    pen.poly([(30, 70), (270, 70), (250, 300), (50, 300)], WICKER, w=6)
    for k in range(6):
        pen.line([(36, 100 + k * 36), (264, 100 + k * 36)], WICKER_D, 4, amp=0.6)
    for k in range(7):
        pen.line([(60 + k * 32, 72), (64 + k * 30, 298)], WICKER_D, 3.5, amp=0.6)
    pen.poly([(14, 50), (286, 50), (280, 84), (20, 84)], WICKER_D, w=5)
BASKET = [make_sprite(300, 320, basket, seed=s) for s in (1, 2, 3)]
def lid(pen):                     # canvas 320x80
    pen.poly([(10, 50), (160, 14), (310, 50), (300, 70), (20, 70)], WICKER_D, w=5)
LID = make_sprite(320, 80, lid, seed=6)

def nicholas(pen):                # canvas 300x620: a dark silhouette only (bishop's hat and crook), no face
    sil = (40, 36, 70)
    pen.poly([(60, 620), (110, 250), (190, 250), (240, 620)], sil, w=4)
    pen.poly([(105, 250), (110, 120), (150, 60), (190, 120), (195, 250)], sil, w=4)
    pen.line([(150, 70), (150, 130)], (100, 96, 140), 4)
    pen.line([(260, 620), (260, 120)], sil, 12)
    pen.line([(260, 120), (262, 80), (236, 64), (214, 80), (222, 104)], sil, 12)
NICK = make_sprite(300, 620, nicholas, seed=7)

def pocket(pen):                  # canvas 300x260
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

def peg(pen):                     # canvas 200x140, a wooden coat peg
    pen.poly(rrect(10, 20, 190, 60, 10), (130, 92, 64), w=5)
    pen.line([(100, 60), (100, 110)], (110, 76, 52), 12)
PEG = make_sprite(200, 140, peg, seed=8)

def fuzz_pocket(img, x, y, tl, frame, shock=False, peek=1.0):
    paste(img, PEG, x, y - 110, 0.8)
    if peek > 0.03:
        paste(img, (FUZZ_W if shock else FUZZ)[boil(frame)], x, y - 60 * peek + 5 * math.sin(tl * 5), 0.5)
    paste(img, POCKET[boil(frame)], x, y + 40, 0.75)

def parchment(pen):               # canvas 900x700
    pen.poly([(30, 40), (870, 20), (880, 660), (20, 680)], (244, 228, 190), w=6, amp=2.5)
    for k in range(6):
        pen.line([(60, 120 + k * 100), (840, 110 + k * 100)], (226, 206, 166), 3, amp=1)
PARCH = make_sprite(900, 700, parchment, seed=9)

def claw(pen):                    # canvas 260x260, three curved claws
    pen.ell(130, 60, 100, 60, fill=FUR, w=5)
    for k in (-1, 0, 1):
        pts = [(130 + k * 56 + 16 * math.sin(a), 100 + 120 * a) for a in [i / 10 for i in range(11)]]
        pen.line(pts, OUT, 24, amp=0.4); pen.line(pts, HORN, 16, amp=0.4)
CLAW = make_sprite(260, 260, claw, seed=10)

def shoe(pen):                    # canvas 260x200, a little boot
    pen.poly([(40, 30), (130, 30), (140, 120), (240, 130), (250, 180), (30, 180)], (150, 60, 56), w=6)
    pen.poly([(30, 30), (140, 30), (140, 54), (30, 54)], (110, 44, 44), w=5)
    pen.line([(30, 172), (250, 172)], OUT, 5)
SHOE = make_sprite(260, 200, shoe, seed=11)

def candy(pen, col):              # canvas 120x60, wrapped sweet
    pen.poly([(4, 10), (30, 30), (4, 50)], col, w=3)
    pen.poly([(116, 10), (90, 30), (116, 50)], col, w=3)
    pen.ell(60, 30, 34, 22, fill=col, w=4)
    pen.line([(46, 16), (54, 44)], (255, 255, 255), 4)
CANDY = [make_sprite(120, 60, lambda p, c=c: candy(p, c), seed=12) for c in ((220, 70, 80), (90, 160, 110), (240, 200, 80))]
def orange(pen):
    pen.ell(50, 50, 40, 40, fill=(240, 150, 50), w=4); pen.ell(58, 16, 12, 6, rot=-20, fill=(90, 150, 80), w=2.5)
ORANGE = make_sprite(100, 100, orange, seed=13)
def twigs(pen):                   # canvas 200x300, a birch bundle tied with string
    for k in range(7):
        x = 70 + k * 10
        pen.line([(x, 280), (x - 30 + k * 12, 20)], (236, 230, 214), 9, amp=0.8)
        pen.line([(x - 10 + k * 6, 160), (x - 14 + k * 6, 150)], OUT, 3)
    pen.poly(rrect(60, 200, 150, 224, 6), (190, 60, 50), w=3)
TWIGS = make_sprite(200, 300, twigs, seed=14)

# ------------------------------------------------------------ scenes
B = [0, starts[1] - 0.12, starts[2] - 0.12, starts[3] - 0.12, starts[5] - 0.12, DUR]

def s1(tl, frame, sd):        # HOOK: St. Nicholas strolls past; Krampus bobs up behind him, mid-bob on frame 0
    img = VILLAGE.copy()
    nx = lerp(380, 300, ease(tl / sd))
    paste(img, NICK, nx, 1080, 1.0)
    bob = 0.75 + 0.25 * math.sin(tl * 3.2 + 1.0)
    kx, ky = 720 + 10 * math.sin(tl * 2), lerp(1180, 1010, bob)
    paste(img, KRAMPUS[boil(frame)], kx, ky, 0.95, rot=4 * math.sin(tl * 2.4))
    tongue(img, kx, ky, 0.95, tl)
    fuzz_pocket(img, 900, 640, tl, frame, shock=True, peek=ease_back(seg(tl, 0.3, 0.8)))
    snowfall(img, tl)
    return camera(img, lerp(1.1, 1.0, ease(tl / sd)), 560, 1000)

def s2(tl, frame, sd):        # CLAW: KRAMPEN scratched onto parchment
    img = PLAIN.copy()
    paste(img, PARCH, 540, 820, 1.05)
    d = ImageDraw.Draw(img)
    word = 'KRAMPEN'
    u = seg(tl, 0.1, 0.9)
    n = int(len(word) * u + 0.999) if u > 0 else 0
    f = font(FONT_HAND, 150)
    full_w = d.textlength(word, font=f)
    x0 = 540 - full_w / 2
    d.text((x0, 720), word[:n], font=f, fill=(70, 44, 40), anchor='lm')
    cxw = x0 + d.textlength(word[:max(1, n)], font=f)
    if u < 1:
        paste(img, CLAW, cxw + 40, 640 + 10 * math.sin(tl * 20), 0.8, rot=-20)
    v = ease_back(seg(tl, 1.0, 1.35), 1.6)
    if v > 0.02:
        d.text((540, 920), '= CLAW', font=font(FONT_HAND, int(120 * v)), fill=(150, 60, 50), anchor='mm')
        paste(img, CLAW, 820, 930, 0.5 * v, rot=-15)
    overlay(img, '"CLAW"', ease_back(seg(tl, 0.9, 1.2)))
    return img

def s3(tl, frame, sd):        # DEC 5: calendar page flips, Krampus roams the rooftops
    img = VILLAGE.copy()
    rx = lerp(-150, 1250, seg(tl, 0.6, sd + 0.3))
    paste(img, KRAMPUS[boil(frame)], rx, 860 + 30 * abs(math.sin(tl * 6)), 0.55, rot=8 * math.sin(tl * 6))
    snowfall(img, tl + 5)
    fl = ease_back(seg(tl, 0.0, 0.5), 1.4)
    d = ImageDraw.Draw(img)
    if fl > 0.02:
        w, h = 210, 240 * fl
        d.rounded_rectangle([540 - w, 620 - h, 540 + w, 620 + h], 18, fill=(250, 246, 236), outline=OUT, width=7)
        d.rectangle([540 - w + 4, 620 - h + 4, 540 + w - 4, 620 - h + 110 * fl], fill=(196, 64, 60))
        if fl > 0.5:
            d.text((540, 620 - h + 58 * fl), 'DECEMBER', font=font(FONT_CAP, int(56 * fl)), fill=(255, 255, 255), anchor='mm')
            d.text((540, 650 + 20 * fl), '5', font=font(FONT_CAP, int(230 * fl)), fill=(60, 40, 40), anchor='mm')
    overlay(img, 'DEC 5', ease_back(seg(tl, 0.3, 0.6)))
    return img

def s4(tl, frame, sd):        # TREATS OR TWIGS: one shoe fills with sweets, the other gets birch twigs; the basket rattles
    img = DOOR.copy()
    paste(img, SHOE, 370, 1060, 1.25)
    paste(img, SHOE, 720, 1060, 1.25, flip=True)
    t_tw = starts[4] - B[3]
    rng = random.Random(3)
    for k in range(7):                                                  # sweets drop into the left shoe
        t0 = 0.15 + k * 0.18
        u = seg(tl, t0, t0 + 0.45)
        if u <= 0: continue
        x = 360 + rng.uniform(-60, 40); y = lerp(160, 990 - (k % 3) * 20, ease_in(u))
        spr = ORANGE if k % 3 == 2 else CANDY[k % 3]
        paste(img, spr, x, y, 0.95, rot=rng.uniform(-40, 40) + 200 * (1 - u))
    if 0.6 < tl < 2.4:
        sparkle(img, 370 + 80 * math.sin(tl * 4), 940, 26 * math.sin(math.pi * seg(tl, 0.6, 2.4)))
    u = seg(tl, t_tw + 0.05, t_tw + 0.4)                                # twigs thud into the right shoe
    if u > 0:
        sh = 6 * (1 - seg(tl, t_tw + 0.4, t_tw + 0.7)) if u >= 1 else 0
        paste(img, TWIGS, 740, lerp(120, 900, ease_in(u)) + sh * math.sin(tl * 60), 0.9, rot=-8)
    b = ease_out(seg(tl, t_tw + 1.2, t_tw + 1.7))                       # the basket slides in, lid rattling
    if b > 0:
        bx = lerp(1250, 930, b)
        paste(img, BASKET[boil(frame)], bx, 760, 1.0, rot=-6)
        rat = math.sin(tl * 38) * seg(tl, t_tw + 1.6, t_tw + 1.8) * (1 - seg(tl, sd - 0.4, sd))
        paste(img, LID, bx - 4, 610 - 14 * abs(rat), 1.0, rot=-6 + 8 * rat)
        if rat:
            for k in range(2):
                sparkle(img, bx - 60 + 120 * k, 580, 10, color=(250, 214, 90))   # two eyes glinting under the lid
    overlay(img, 'TREATS OR TWIGS', ease_back(seg(tl, 0.2, 0.5)), size=96)
    return img

def s5(tl, frame, sd):        # BE GOOD: Krampus grins at camera; the Fuzz zips down into its pocket
    img = VILLAGE.copy()
    img = camera(img, 1.25, 540, 1100)
    sc = lerp(1.25, 1.4, ease(seg(tl, 0, 1.5)))
    kx, ky = 470, 1020 + 6 * math.sin(tl * 3)
    paste(img, KRAMPUS[boil(frame)], kx, ky, sc, rot=3 * math.sin(tl * 1.7))
    tongue(img, kx, ky, sc, tl)
    t_fast = durs[5] * 0.6
    peek = 1 - ease(seg(tl, t_fast, t_fast + 0.25))
    fuzz_pocket(img, 900, 640, tl, frame, shock=tl > t_fast - 0.5, peek=peek * ease_back(seg(tl, 0.0, 0.4)))
    snowfall(img, tl + 9)
    overlay(img, 'BE GOOD', ease_back(seg(tl, 0.2, 0.5)))
    return img

SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate([s1, s2, s3, s4, s5])]
EP = Episode(NAME, SCENES, CHUNKS, DUR, END_TAG, loop=LOOP, hook=HOOK)

def audio_plan():
    import pf_audio as A
    sfx = [(A.wind(2.5), 0.0, 0.35, 0), (A.thud(), 0.3, 0.45, 0.3), (A.thud(), 1.25, 0.4, 0.3), (A.rustle(0.3), 0.4, 0.5, 0.6),
           (A.thud(), 2.2, 0.4, 0.3)]
    sfx += [(A.scribble(1.2), B[1] + 0.2, 0.55, 0), (A.pop(), B[1] + 1.6, 0.45, 0)]
    sfx += [(A.rustle(0.3), B[2] + 0.05, 0.5, 0), (A.tick(900, 0.05, 0.5), B[2] + 0.4, 0.4, 0), (A.wind(2.0), B[2] + 0.6, 0.3, 0)]
    sfx += [(A.tick(1500 + 120 * k, 0.04, 0.45), B[3] + 0.6 + k * 0.18, 0.3, -0.3) for k in range(7)]
    sfx += [(A.chime(1046.5), B[3] + 1.0, 0.3, -0.3), (A.sparkles(), B[3] + 1.2, 0.25, -0.3)]
    tt = starts[4]
    sfx += [(A.whoosh(0.3, False), tt + 0.05, 0.4, 0.3), (A.thud(), tt + 0.4, 0.6, 0.3), (A.whoosh(0.4), tt + 1.2, 0.35, 0.5),
            (A.rustle(0.6), tt + 1.6, 0.6, 0.5)]
    sfx += [(A.pop(), starts[5] + 0.2, 0.4, 0), (A.whoosh(0.3, False), starts[5] + durs[5] * 0.6, 0.5, 0.4),
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
