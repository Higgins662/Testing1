import sys, math, random
import numpy as np
from PIL import Image, ImageDraw
from pf import *

STYLE = 'ambient'
lines, durs, starts, DUR = timeline('ep20', gap=0.26, gaps={1: 0.42, 3: 0.34, 5: 0.34, 6: 0.32})
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={1: ['BATHROOM', 'TILES.'], 3: ['LAVA.'], 4: ['THOUSANDS'], 6: ['HONEYCOMB.'], 8: ['CHOPSTICKS']})
END_TAG = starts[-1] + durs[-1] + 0.35

STEEL = (200, 204, 214)
STEEL_D = (150, 156, 170)
TILE = (40, 40, 46)

def hexpts(cx, cy, r, rot=0):
    return [(cx + r * math.cos(math.radians(60 * i + rot)), cy + r * math.sin(math.radians(60 * i + rot))) for i in range(6)]

# ------------------------------------------------------------ rocket (canvas 920x380, nose right, belly down)
def rocket(pen):
    pen.poly([(140, 120), (60, 60), (40, 70), (90, 150)], STEEL_D, w=4)
    pen.poly([(140, 260), (60, 320), (40, 310), (90, 230)], (60, 60, 66), w=4)
    body = capsule(160, 190, 760, 190, 78)
    pen.poly(body, STEEL, w=5)
    pen.poly([(700, 112), (820, 150), (860, 190), (820, 230), (700, 268)], STEEL, w=5)
    for x in range(180, 820, 40):
        for row, y in enumerate((214, 238, 258)):
            if x + (row % 2) * 20 > 850 - (row * 30): continue
            pen.poly(hexpts(x + (row % 2) * 20, y, 13, 30), TILE, outline=(70, 70, 78), w=1.5, amp=0.2)
    pen.line([(170, 196), (840, 196)], (80, 82, 92), 4, amp=0.5)
    pen.poly([(700, 110), (780, 60), (800, 70), (760, 140)], STEEL_D, w=4)
    pen.poly([(700, 270), (780, 320), (800, 310), (760, 240)], (60, 60, 66), w=4)
    for wx in (300, 420, 540):
        pen.line([(wx, 128), (wx, 170)], (176, 182, 196), 3)
    pen.ell(640, 150, 22, 16, fill=(130, 190, 220), w=3)

def duck(pen):
    pen.ell(110, 130, 80, 56, fill=(250, 214, 70), w=4.5)
    pen.ell(150, 66, 44, 42, fill=(250, 214, 70), w=4.5)
    pen.poly([(186, 64), (226, 70), (190, 84)], (240, 140, 60), w=3)
    pen.dot(160, 56, 7, OUT); pen.dot(162, 54, 2.5, (255, 255, 255))
    pen.poly([(70, 116), (40, 96), (60, 140)], (236, 196, 60), w=3)

def thermometer(pen):
    pen.poly(capsule(80, 60, 80, 420, 32), (246, 246, 250), w=5)
    pen.ell(80, 470, 56, 56, fill=(220, 60, 50), w=5)
    for k in range(8):
        y = 110 + k * 40
        pen.line([(112, y), (132, y)], OUT, 3)

def lava(pen):
    pen.poly([(20, 160), (60, 80), (110, 110), (150, 40), (200, 100), (240, 70), (280, 160)], (240, 110, 40), w=4, amp=2)
    pen.ell(150, 150, 130, 30, fill=(200, 70, 30), w=4)

def worker(pen):
    pen.poly([(70, 600), (90, 300), (180, 260), (270, 300), (290, 600)], (240, 140, 50), w=5)
    pen.poly([(140, 280), (180, 330), (220, 280)], (230, 230, 220), w=3)
    pen.line([(110, 400), (250, 400)], (250, 240, 120), 8); pen.line([(110, 470), (250, 470)], (250, 240, 120), 8)
    pen.ell(180, 190, 74, 80, fill=(214, 170, 130), w=4.5)
    pen.poly([(96, 170), (110, 104), (180, 84), (250, 104), (264, 170)], (250, 210, 60), w=4.5)
    pen.poly([(84, 170), (276, 170), (276, 186), (84, 186)], (236, 196, 50), w=4)
    pen.dot(156, 206, 7, OUT); pen.dot(204, 206, 7, OUT)
    pen.line([(160, 240), (180, 248), (200, 240)], OUT, 4)
    pen.poly(capsule(250, 330, 360, 250, 26), (240, 140, 50), w=4)
    pen.poly(hexpts(390, 230, 46, 30), TILE, outline=OUT, w=4)

def bee(pen):
    pen.ell(80, 60, 44, 30, fill=(250, 200, 60), w=4)
    for x in (66, 90):
        pen.line([(x, 34), (x, 86)], OUT, 7)
    pen.ell(60, 24, 22, 14, rot=-30, fill=(220, 236, 250), w=3); pen.ell(100, 24, 22, 14, rot=30, fill=(220, 236, 250), w=3)
    pen.dot(118, 54, 5, OUT)

def tower(pen):
    pen.poly([(60, 1400), (60, 40), (300, 40), (300, 1400)], None, outline=(80, 84, 96), w=10, amp=0.6)
    for y in range(40, 1400, 120):
        pen.line([(60, y), (300, y)], (80, 84, 96), 7, amp=0.4)
        pen.line([(60, y), (300, y + 120)], (110, 114, 126), 5, amp=0.4)
        pen.line([(300, y), (60, y + 120)], (110, 114, 126), 5, amp=0.4)
    pen.poly([(40, 20), (320, 20), (320, 60), (40, 60)], (120, 124, 136), w=5)

def arm(pen):
    pen.poly([(10, 30), (520, 40), (540, 70), (520, 100), (10, 110)], (150, 156, 168), w=5)
    for x in range(60, 500, 80):
        pen.line([(x, 40), (x + 40, 100)], (110, 116, 128), 4)
    pen.poly([(500, 30), (560, 20), (560, 120), (500, 110)], (120, 124, 136), w=4)

def lawn_chair(pen):
    pen.line([(40, 300), (200, 120)], (190, 190, 196), 8); pen.line([(220, 300), (60, 120)], (190, 190, 196), 8)
    pen.poly([(40, 150), (220, 150), (210, 230), (50, 230)], (100, 170, 200), w=4)
    for x in range(60, 210, 30):
        pen.line([(x, 152), (x, 228)], (240, 240, 240), 4)
    pen.poly([(60, 40), (200, 40), (220, 150), (40, 150)], (100, 170, 200), w=4)
    for x in range(70, 200, 30):
        pen.line([(x, 44), (x - 6, 148)], (240, 240, 240), 4)

# ------------------------------------------------------------ assets
print('assets...', file=sys.stderr)
SKY = downsample(bg_canvas([(0, (20, 24, 50)), (0.5, (70, 110, 170)), (1, (170, 210, 236))]), W, H)
HOT = downsample(bg_canvas([(0, (30, 20, 44)), (0.6, (110, 50, 70)), (1, (200, 110, 80))], glows=[(540, 900, 600, (255, 150, 110), 0.5)]), W, H)
HULL_BG = downsample(bg_canvas([(0, (176, 180, 192)), (1, (140, 146, 160))]), W, H)
PAD = None
ROCKET = make_sprite(920, 380, rocket, seed=2)
DUCK = make_sprite(240, 200, duck, seed=3)
THERM = make_sprite(170, 540, thermometer, seed=4)
LAVA = make_sprite(300, 200, lava, seed=5)
WORKER = [make_sprite(460, 620, worker, seed=s) for s in (1, 2, 3)]
BEE = [make_sprite(160, 110, bee, seed=s) for s in (1, 2, 3)]
TOWER = make_sprite(360, 1420, tower, seed=6)
ARM = make_sprite(580, 140, arm, seed=7)
CHAIR = make_sprite(260, 320, lawn_chair, seed=8)
FUZZ = fuzz_sprites('happy')

def pad_bg():
    img = bg_canvas([(0, (110, 160, 214)), (0.7, (220, 230, 236)), (1, (220, 230, 236))], glows=[(300, 300, 300, (255, 248, 220), 0.6)])
    def fn(pen):
        pen.poly([(-20, 1500), (1100, 1500), (1100, 1940), (-20, 1940)], (180, 168, 140), w=4)
        pen.poly([(-20, 1460), (1100, 1440), (1100, 1520), (-20, 1520)], (120, 150, 100), w=4)
        for k in range(5):
            pen.ell(100 + k * 230, 300 + 60 * (k % 2), 90, 30, fill=(250, 252, 255), outline=None)
    return make_sprite(W, H, fn, seed=9, base=img)
PAD = pad_bg()

HEX_R = 52
HEXES = []
for r in range(-1, 20):
    for c in range(-1, 15):
        cx = c * HEX_R * 1.5 + 40
        cy = r * HEX_R * math.sqrt(3) + (c % 2) * HEX_R * math.sqrt(3) / 2 + 120
        HEXES.append((cx, cy))
_rng = random.Random(4)
ORDER = sorted(range(len(HEXES)), key=lambda i: (HEXES[i][1] * 0.6 + HEXES[i][0]) + _rng.uniform(-80, 80))

def tiles_layer(n, glow_amt=0.0):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in ORDER[:n]:
        cx, cy = HEXES[i]
        d.polygon(hexpts(cx, cy, HEX_R - 3), fill=(42 + int(120 * glow_amt), 42 + int(40 * glow_amt), 48), outline=(90, 92, 104))
    return lay

def honeycomb_layer(alpha):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for (cx, cy) in HEXES:
        d.polygon(hexpts(cx, cy, HEX_R - 3), fill=(240, 180, 60, int(140 * alpha)), outline=(200, 130, 40, int(255 * alpha)))
    return lay

# ------------------------------------------------------------ scenes
B = [0] + [starts[i] - 0.15 for i in (2, 4, 6, 7)] + [DUR]

def s1(tl, frame, sd):
    img = SKY.copy()
    d = ImageDraw.Draw(img)
    for k in range(14):
        y = (k * 140 - tl * 900) % 2000 - 40
        x = 80 + (k * 197) % 940
        d.line([(x, y), (x, y + 120)], fill=(220, 230, 250), width=4)
    paste(img, ROCKET, 540, 760 + 14 * math.sin(tl * 2), 1.05, rot=-6 + 2 * math.sin(tl * 1.3))
    t_tiles = starts[1] - 0.1
    if tl > t_tiles:
        for k in range(5):
            sparkle(img, 330 + k * 110, 860 + 10 * (k % 2), 26 * math.sin(math.pi * seg(tl, t_tiles + k * 0.08, t_tiles + 0.6 + k * 0.08)))
        du = seg(tl, t_tiles, t_tiles + 2.6)
        paste(img, DUCK, lerp(-150, 1250, du), 1100 - 120 * math.sin(math.pi * du), 0.9, rot=20 * math.sin(tl * 3))
    return img

def s2(tl, frame, sd):
    img = HOT.copy()
    heat = seg(tl, 0.0, 1.5)
    glow(img, 540, 900, 560, (255, 130, 160), 0.55 * heat)
    glow(img, 540, 920, 380, (255, 200, 120), 0.6 * heat)
    d = ImageDraw.Draw(img)
    for k in range(18):
        x = 140 + k * 46
        y0 = 980 + 30 * math.sin(k)
        ln = 120 + 80 * math.sin(tl * 9 + k)
        d.line([(x, y0), (x - 30, y0 + ln * heat)], fill=(255, 190, 150), width=6)
    paste(img, ROCKET, 540, 840 + 8 * math.sin(tl * 14), 1.0, rot=-4)
    t_lava = starts[3] - B[1]
    level = ease(seg(tl, 0.4, t_lava + 0.4))
    tx, ty = 900, 380
    paste(img, THERM, tx, ty, 0.6)
    d.rectangle([tx - 8, ty + 0.6 * (220 - 360 * level) - 0, tx + 8, ty + 0.6 * 225], fill=(220, 60, 50))
    if tl > t_lava + 0.4:
        u = seg(tl, t_lava + 0.4, t_lava + 1.0)
        for k in range(8):
            a = 2 * math.pi * k / 8
            sparkle(img, tx + 90 * u * math.cos(a), ty - 150 + 90 * u * math.sin(a), 24 * (1 - u * 0.5), color=(255, 120, 90))
    if tl > t_lava:
        paste(img, LAVA, 200, 380, 0.8 * ease_back(seg(tl, t_lava, t_lava + 0.4), 2.0))
        d.text((200, 500), 'LAVA', font=font(FONT_CAP, 60), fill=(255, 220, 160), anchor='mm', stroke_width=6, stroke_fill=OUT)
    return shake(img, 6 * heat, frame)

def s3(tl, frame, sd):
    img = HULL_BG.copy()
    n = int(len(HEXES) * ease(seg(tl, 0.2, sd - 0.6)))
    t_heat = starts[5] - B[2]
    gl = math.sin(math.pi * seg(tl, t_heat, t_heat + 1.2)) if tl > t_heat else 0
    img.alpha_composite(tiles_layer(n, gl))
    if gl > 0:
        d = ImageDraw.Draw(img)
        for k in range(6):
            x = 160 + k * 160
            pts = [(x + 20 * math.sin(tl * 6 + j + k), 700 - j * 40) for j in range(8)]
            d.line(pts, fill=(255, 200, 150), width=6)
    ox = 380 + 40 * math.sin(tl * 2)
    paste(img, WORKER[boil(frame)], ox, 1120, 1.0)
    d = ImageDraw.Draw(img)
    lu = ease_back(seg(tl, 0.6, 1.0), 2.0)
    if lu > 0.02:
        d.text((540, 260), 'THOUSANDS OF TILES', font=font(FONT_CAP, int(84 * lu)), fill=HL, anchor='mm', stroke_width=9, stroke_fill=OUT)
    return img

def s4(tl, frame, sd):
    img = HULL_BG.copy()
    img.alpha_composite(tiles_layer(len(HEXES)))
    u = ease(seg(tl, 0.1, 1.2))
    hc = honeycomb_layer(1.0)
    off = int(lerp(W, 0, u))
    tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tmp.alpha_composite(hc, (off, 0) if off < W else (0, 0)) if off < W else None
    img.alpha_composite(tmp)
    if u > 0.98:
        glow(img, 540, 900, 500, (255, 220, 120), 0.3 * seg(tl, 1.2, 1.6))
    for k in range(2):
        paste(img, BEE[boil(frame, off=k)], 300 + 500 * k + 80 * math.sin(tl * 3 + k), 600 + 60 * math.sin(tl * 5 + k * 2), 1.0, flip=k == 1)
    return img

def s5(tl, frame, sd):
    img = PAD.copy()
    paste(img, TOWER, 300, 1500 - 710, 1.0)
    desc = ease_out(seg(tl, 0.0, 1.8))
    ry = lerp(-300, 700, desc)
    paste(img, ROCKET, 700, ry, 0.95, rot=90)
    close = ease_back(seg(tl, 1.6, 2.2), 1.4)
    for (yy, sgn) in ((560, 1), (760, -1)):
        ang = lerp(28 * sgn, 0, close)
        paste(img, ARM, 300 + 290 * math.cos(math.radians(ang)), yy - 290 * math.sin(math.radians(ang)) * 0.5, 0.85, rot=ang)
    if close > 0.95:
        d = ImageDraw.Draw(img)
        d.text((720, 200), 'CAUGHT!', font=font(FONT_CAP, 90), fill=HL, anchor='mm', stroke_width=9, stroke_fill=OUT)
    paste(img, CHAIR, 900, 1640, 0.8)
    paste(img, FUZZ[boil(frame)], 900, 1560 + 6 * math.sin(tl * 3), 0.6)
    return img

SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate([s1, s2, s3, s4, s5])]
EP = Episode('ep20', SCENES, CHUNKS, DUR, END_TAG)

def audio_plan():
    import pf_audio as A
    t_tiles = starts[1] - 0.1
    sfx = [(A.rustle(), 0.05, 1.0, 0), (A.wind(B[1]), 0.0, 0.45, 0), (A.engine(B[1], 45), 0.0, 0.3, 0)]
    sfx += [(A.sparkles(), t_tiles, 0.35, 0), (A.honk(620, 0.15), t_tiles + 0.9, 0.3, -0.3), (A.honk(620, 0.15), t_tiles + 1.15, 0.3, 0.1)]
    sfx += [(A.whoosh(1.2), B[1], 0.7, 0), (A.wind(B[2] - B[1]), B[1], 0.6, 0), (A.pop(), starts[3] + 0.4, 0.5, 0.4)]
    sfx += [(A.tick(1600 + 100 * (k % 4), 0.05, 0.45), B[2] + 0.3 + k * 0.22, 0.3, ((k % 5) - 2) * 0.2) for k in range(20)]
    sfx += [(A.engine(1.4, 140), B[3] + 0.2, 0.18, 0), (A.chime(1046.5), B[3] + 1.25, 0.35, 0)]
    sfx += [(A.wind(1.8), B[4], 0.4, 0), (A.thud(), B[4] + 1.9, 0.7, 0.2), (A.stamp(), B[4] + 2.0, 0.4, 0.2)]
    sfx += [(A.pop(), END_TAG, 0.7, 0), (A.chime(1318.5), END_TAG + 0.05, 0.4, 0)]
    cues = [(f'/home/claude/eps/ep20_vo_{i}.wav', s) for i, s in enumerate(starts)]
    return cues, sfx

if __name__ == '__main__':
    if sys.argv[1] == 'audio':
        import pf_audio as A
        cues, sfx = audio_plan()
        A.build(DUR, cues, sfx, '/home/claude/eps/ep20/audio.wav', style=STYLE)
        print('audio ok')
    else:
        EP.main(sys.argv)
