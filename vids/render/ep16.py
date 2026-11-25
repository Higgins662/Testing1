import sys, math, random
import numpy as np
from PIL import Image, ImageDraw
from pf import *

STYLE = 'folk'
lines, durs, starts, DUR = timeline('ep16', gap=0.26, gaps={1: 0.4, 3: 0.32, 5: 0.36, 7: 0.36})
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={0: ['200'], 1: ['CAR', 'ALARMS.'], 3: ['WEIRDER.'], 5: ['BEEPS.'], 7: ['ALL', 'NIGHT'], 9: ['WORSE']})
END_TAG = starts[-1] + durs[-1] + 0.35

GREY = (150, 150, 156)
GREY_D = (102, 102, 110)
BELLY = (226, 222, 214)

# ------------------------------------------------------------ mockingbird (canvas 380x300, faces right)
def bird(pen, open_=False, puff=1.0):
    pen.poly([(120, 170), (20, 210), (14, 236), (40, 232), (130, 196)], GREY_D, w=4)
    pen.line([(24, 222), (60, 214)], (240, 240, 240), 3)
    pen.ell(190, 170, 92 * puff, 70 * puff, fill=GREY, w=4.5)
    pen.ell(205, 192, 62 * puff, 44 * puff, fill=BELLY, w=3)
    pen.poly([(120, 150), (200, 136), (236, 168), (170, 200), (110, 184)], GREY_D, w=4)
    pen.poly([(160, 160), (196, 154), (200, 172), (164, 176)], (246, 246, 246), w=2.5)
    pen.ell(272, 112, 50, 46, fill=GREY, w=4.5)
    pen.dot(286, 104, 9, (20, 18, 22)); pen.dot(289, 101, 3, (255, 255, 255))
    pen.line([(270, 90), (300, 94)], OUT, 4, amp=0.3)
    pen.line([(282, 104), (300, 104)], (60, 60, 66), 3, amp=0.2)
    if open_:
        pen.poly([(316, 106), (364, 92), (322, 112)], (50, 46, 50), w=2.5, amp=0.3)
        pen.poly([(316, 116), (360, 128), (320, 120)], (50, 46, 50), w=2.5, amp=0.3)
    else:
        pen.poly([(316, 108), (360, 114), (316, 120)], (50, 46, 50), w=2.5, amp=0.3)
    for fx in (180, 214):
        pen.line([(fx, 236), (fx, 262)], (70, 60, 56), 4)
        pen.line([(fx - 10, 264), (fx + 12, 264)], (70, 60, 56), 4)

def dusk_bg():
    img = bg_canvas([(0, (84, 78, 130)), (0.45, (220, 140, 120)), (0.62, (246, 196, 140)), (1, (246, 196, 140))],
                    glows=[(800, 980, 380, (255, 220, 160), 0.7)])
    def fn(pen):
        pen.ell(800, 1010, 80, 80, fill=(255, 210, 140), outline=None)
        for (x, w_, h_) in [(-20, 260, 260), (220, 240, 210), (440, 280, 280), (700, 220, 230), (900, 220, 260)]:
            pen.poly([(x, 1060), (x, 1060 - h_), (x + w_ / 2, 1060 - h_ - 90), (x + w_, 1060 - h_), (x + w_, 1060)], (70, 62, 90), w=4)
        pen.poly([(-20, 1060), (1100, 1060), (1100, 1940), (-20, 1940)], (70, 100, 70), w=4)
        for x in range(-10, 1100, 70):
            pen.poly([(x, 1240), (x, 1010), (x + 25, 985), (x + 50, 1010), (x + 50, 1240)], (214, 200, 180), w=4)
        for y in (1060, 1180):
            pen.poly([(-20, y), (1100, y), (1100, y + 30), (-20, y + 30)], (190, 176, 156), w=4)
    return make_sprite(W, H, fn, seed=2, base=img)

def note_bubble(pen, icon):
    pen.ell(110, 100, 96, 86, fill=(252, 250, 244), w=5)
    pen.poly([(70, 170), (50, 220), (110, 182)], (252, 250, 244), w=5)
    pen.ell(110, 100, 90, 80, fill=(252, 250, 244), outline=None)
    if icon == 'note':
        pen.ell(90, 134, 22, 16, rot=-20, fill=(60, 50, 70), w=3)
        pen.line([(110, 128), (112, 56), (150, 70)], (60, 50, 70), 6)
    elif icon == 'bird':
        pen.ell(110, 110, 44, 30, fill=(214, 120, 90), w=4)
        pen.ell(146, 86, 22, 20, fill=(214, 120, 90), w=4)
        pen.poly([(166, 84), (186, 88), (166, 94)], (240, 190, 70), w=2.5)
        pen.dot(150, 82, 4, OUT)
        pen.poly([(66, 104), (40, 90), (44, 120)], (190, 100, 74), w=3)
    elif icon == 'frog':
        pen.ell(110, 120, 58, 36, fill=(110, 170, 90), w=4)
        pen.ell(84, 84, 18, 18, fill=(110, 170, 90), w=4); pen.ell(136, 84, 18, 18, fill=(110, 170, 90), w=4)
        pen.dot(84, 84, 7, OUT); pen.dot(136, 84, 7, OUT)
        pen.line([(84, 130), (110, 140), (136, 130)], OUT, 4)
    elif icon == 'gate':
        for x in (60, 90, 120, 150):
            pen.poly([(x, 150), (x, 70), (x + 10, 60), (x + 20, 70), (x + 20, 150)], (190, 150, 110), w=3)
        pen.line([(54, 90), (176, 90)], (150, 110, 80), 5); pen.line([(54, 130), (176, 130)], (150, 110, 80), 5)
        pen.line([(170, 60), (190, 44)], OUT, 4); pen.line([(178, 70), (198, 62)], OUT, 4)
    elif icon == 'beep':
        pen.poly(rrect(56, 66, 164, 140, 18), (230, 80, 70), w=4)
        pen.text((110, 104), 'BEEP', 36, (255, 250, 240), font=FONT_CAP)

def car(pen):
    body = (90, 140, 176)
    pen.poly([(30, 210), (40, 150), (150, 140), (210, 70), (420, 66), (500, 140), (610, 160), (620, 220), (590, 250), (40, 250)], body, w=5)
    pen.poly([(228, 82), (300, 80), (300, 140), (178, 144)], (190, 224, 240), w=4)
    pen.poly([(318, 80), (412, 80), (470, 140), (318, 140)], (190, 224, 240), w=4)
    pen.line([(310, 150), (310, 236)], (60, 100, 130), 4)
    for wx in (150, 500):
        pen.ell(wx, 250, 52, 52, fill=(46, 44, 50), w=5)
        pen.ell(wx, 250, 22, 22, fill=(170, 170, 176), w=3)
    pen.ell(598, 180, 14, 12, fill=(255, 240, 180), w=3)
    pen.ell(42, 176, 10, 14, fill=(220, 80, 70), w=3)

def house_bg(lit=False):
    img = bg_canvas([(0, (60, 56, 100)), (0.6, (130, 100, 130)), (1, (130, 100, 130))])
    def fn(pen):
        pen.poly([(80, 1080), (80, 520), (540, 260), (1000, 520), (1000, 1080)], (150, 130, 120), w=5)
        pen.poly([(40, 540), (540, 230), (1040, 540), (1000, 560), (540, 290), (80, 560)], (100, 70, 70), w=5)
        for (x, y) in [(220, 640), (700, 640)]:
            pen.poly([(x, y), (x + 160, y), (x + 160, y + 180), (x, y + 180)], (255, 222, 140) if (lit and x == 700) else (60, 64, 96), w=5)
            pen.line([(x + 80, y), (x + 80, y + 180)], OUT, 4); pen.line([(x, y + 90), (x + 160, y + 90)], OUT, 4)
        pen.poly([(-20, 1080), (1100, 1080), (1100, 1940), (-20, 1940)], (70, 70, 80), w=4)
        pen.poly([(-20, 1080), (1100, 1080), (1100, 1120), (-20, 1120)], (150, 146, 140), w=4)
    out = make_sprite(W, H, fn, seed=3, base=img)
    if lit:
        glow(out, 780, 730, 260, (255, 220, 140), 0.45)
    return out

def roof_bg():
    img = bg_canvas([(0, (24, 28, 56)), (1, (50, 56, 96))], glows=[(780, 330, 380, (220, 226, 255), 0.45)])
    def fn(pen):
        pen.ell(780, 330, 110, 110, fill=(244, 240, 220), w=4)
        pen.ell(750, 300, 22, 18, fill=(220, 216, 196), outline=None); pen.ell(810, 370, 14, 12, fill=(220, 216, 196), outline=None)
        rng = random.Random(5)
        for k in range(40):
            pen.dot(rng.uniform(0, 1080), rng.uniform(0, 800), rng.uniform(2, 4), (255, 250, 220))
        pen.poly([(-20, 1300), (-20, 980), (1100, 820), (1100, 1300)], (90, 70, 80), w=5)
        for k in range(9):
            y = 1010 + k * 34
            pen.line([(-20, y), (1100, y - 160 + k * 1)], (70, 54, 64), 3, amp=1.5)
        pen.poly([(760, 880), (760, 720), (860, 720), (860, 860)], (140, 80, 70), w=5)
        pen.poly([(744, 720), (876, 720), (876, 690), (744, 690)], (120, 66, 60), w=4)
        pen.poly([(-20, 1300), (1100, 1300), (1100, 1940), (-20, 1940)], (36, 34, 50), w=4)
    return make_sprite(W, H, fn, seed=4, base=img)

def cat(pen, k=0):
    c = (230, 160, 90)
    pen.poly(capsule(110, 330, 300, 340, 40), c, w=4)
    pen.ell(200, 270, 110, 100, fill=c, w=4.5)
    pen.ell(200, 140, 96, 84, fill=c, w=4.5)
    for ex, d in ((128, -1), (272, 1)):
        pen.poly([(ex - 28 * d, 90), (ex - 6 * d, 30), (ex + 30 * d, 84)], c, w=4)
    pen.line([(150, 140), (176, 146)], OUT, 5); pen.line([(224, 146), (250, 140)], OUT, 5)
    pen.line([(180, 186), (200, 178), (220, 186)], OUT, 4.5)
    pen.dot(200, 166, 8, (214, 120, 120))
    for px in (110, 290):
        pen.ell(px, 112 + 6 * math.sin(k), 38, 34, fill=(246, 214, 170), w=4)
    for k2 in range(3):
        pen.line([(270, 250 + k2 * 30), (310, 252 + k2 * 30)], (200, 130, 70), 4)

def pocket_bg():
    img = bg_canvas([(0, (70, 96, 140)), (1, (52, 70, 108))])
    def fn(pen):
        rng = random.Random(3)
        for k in range(160):
            y = rng.uniform(0, 1940); x = rng.uniform(0, 1080)
            pen.line([(x, y), (x + 40, y + 40)], (84, 110, 156), 3, amp=0.3)
        pen.poly([(140, 980), (940, 980), (900, 1600), (540, 1700), (180, 1600)], (62, 86, 128), w=6)
        pen.line([(160, 1010), (920, 1010)], (220, 170, 90), 4, amp=0.6)
        pen.line([(190, 1600), (540, 1680), (890, 1600)], (220, 170, 90), 4, amp=0.6)
    return make_sprite(W, H, fn, seed=6, base=img)

def earmuffs(pen):
    outer = ellpts(150, 172, 104, 126, a0=180, a1=360, n=30)
    inner = ellpts(150, 172, 86, 108, a0=180, a1=360, n=30)
    pen.poly(outer + list(reversed(inner)), (200, 70, 80), w=4, amp=0.6)
    for x in (52, 248):
        pen.ell(x, 172, 40, 46, fill=(250, 230, 236), w=4.5)
        pen.ell(x, 172, 24, 28, fill=(236, 200, 210), outline=None)

# ------------------------------------------------------------ assets
print('assets...', file=sys.stderr)
DUSK = dusk_bg()
BIRD = [make_sprite(380, 300, lambda p: bird(p), seed=s) for s in (1, 2, 3)]
BIRD_OPEN = [make_sprite(380, 300, lambda p: bird(p, True, 1.08), seed=s) for s in (1, 2, 3)]
BUB = {k: make_sprite(220, 230, lambda p, k=k: note_bubble(p, k), seed=5) for k in ('note', 'bird', 'frog', 'gate', 'beep')}
CAR = make_sprite(660, 320, car, seed=7)
HOUSE = house_bg(False); HOUSE_LIT = house_bg(True)
ROOF = roof_bg()
CAT = [make_sprite(400, 400, lambda p, k=k: cat(p, k), seed=s) for k, s in ((0, 1), (2, 2), (4, 3))]
POCKET = pocket_bg()
MUFFS = make_sprite(300, 230, earmuffs, seed=8)
FUZZ = fuzz_sprites('happy')

def singing(frame, tl, rate=7):
    return BIRD_OPEN[boil(frame)] if int(tl * rate) % 2 else BIRD[boil(frame)]

def alarm_waves(img, x, y, t, color=(255, 90, 70)):
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for k in range(4):
        r = ((t * 260) + k * 70) % 280 + 30
        a = int(255 * (1 - r / 310))
        d.arc([x - r, y - r, x + r, y + r], -40, 40, fill=color + (a,), width=10)
    img.alpha_composite(lay)

# ------------------------------------------------------------ scenes
B = [0] + [starts[i] - 0.15 for i in (2, 4, 6, 8)] + [DUR]

def s1(tl, frame, sd):
    img = DUSK.copy()
    t_alarm = starts[1] - 0.1
    on = tl > t_alarm
    spr = singing(frame, tl, 9) if on else BIRD[boil(frame)]
    puff = 1 + 0.05 * math.sin(tl * 3)
    paste(img, spr, 520, 870, 1.5 * puff)
    if not on:
        for k in range(4):
            u = (tl * 0.6 + k * 0.25) % 1
            paste(img, BUB['note'], 700 + 120 * u + 30 * k, 620 - 300 * u, 0.5 * math.sin(math.pi * u))
    else:
        alarm_waves(img, 760, 760, tl - t_alarm)
        if int((tl - t_alarm) * 6) % 2:
            glow(img, 540, 800, 500, (255, 90, 70), 0.18)
    return camera(img, lerp(1.02, 1.1, ease(tl / sd)), 540, 860)

def s2(tl, frame, sd):
    img = DUSK.copy()
    paste(img, singing(frame, tl, 6), 540, 900, 1.35)
    icons = ['note', 'note', 'bird', 'note', 'frog', 'note', 'gate', 'note', 'beep', 'note']
    for k in range(10):
        t0 = 0.2 + k * 0.32
        u = ease_back(seg(tl, t0, t0 + 0.3), 2.2)
        if u < 0.02: continue
        a = -math.pi / 2 + (k - 4.5) * 0.36
        r = 400 + 40 * (k % 2)
        paste(img, BUB[icons[k]], 540 + r * math.cos(a), 900 + r * math.sin(a) * 0.9 + 8 * math.sin(tl * 3 + k), 0.62 * u)
    n = int(200 * ease(seg(tl, 0.2, 3.4)))
    d = ImageDraw.Draw(img)
    d.text((540, 300), f'~{n} SONGS', font=font(FONT_CAP, 96), fill=HL, anchor='mm', stroke_width=9, stroke_fill=OUT)
    return img

def s3(tl, frame, sd):
    t_beep = starts[5] - B[2] - 0.1
    img = (HOUSE_LIT if tl > t_beep + 0.35 else HOUSE).copy()
    paste(img, CAR, 520, 1150, 1.25)
    hop = abs(60 * math.sin(math.pi * seg(tl, 0.0, 0.5)))
    paste(img, singing(frame, tl, 8) if tl > t_beep else BIRD[boil(frame)], 470, 920 - hop, 1.0)
    for k, ic in enumerate(['bird', 'frog', 'gate']):
        t0 = 0.4 + k * 0.6
        u = ease_back(seg(tl, t0, t0 + 0.3), 2.2) * (1 - seg(tl, t_beep - 0.2, t_beep))
        if u > 0.02:
            paste(img, BUB[ic], 260 + k * 280, 560 + 20 * math.sin(tl * 3 + k), 0.75 * u)
    if tl > t_beep:
        alarm_waves(img, 620, 860, tl - t_beep)
        alarm_waves(img, 330, 860, tl - t_beep + 0.3, (255, 200, 80))
        if int((tl - t_beep) * 6) % 2:
            d = ImageDraw.Draw(img)
            d.ellipse([60, 1050, 120, 1110], fill=(255, 120, 90))
    return img

def s4(tl, frame, sd):
    img = ROOF.copy()
    paste(img, singing(frame, tl, 5), 380, 905 + 4 * math.sin(tl * 4), 1.2, rot=8)
    for k in range(5):
        u = (tl * 0.5 + k * 0.2) % 1
        paste(img, BUB['note'], 520 + 260 * u, 760 - 380 * u + 30 * math.sin(k + tl), 0.45 * math.sin(math.pi * u))
    cu = ease_out(seg(tl, 0.6, 1.3))
    paste(img, CAT[boil(frame)], lerp(1300, 860, cu), 1070, 0.9)
    d = ImageDraw.Draw(img)
    d.text((540, 300), '3 AM', font=font(FONT_CAP, 100), fill=(244, 240, 220), anchor='mm', stroke_width=9, stroke_fill=OUT)
    return img

def s5(tl, frame, sd):
    img = POCKET.copy()
    rise = ease_back(seg(tl, 0.0, 0.5), 1.6)
    nod = 10 * math.sin(tl * 2 * math.pi * 1.2)
    fx, fy = 540, lerp(1250, 800, rise)
    paste(img, FUZZ[boil(frame)], fx, fy + nod, 1.9, rot=nod * 0.4)
    paste(img, MUFFS, fx, fy + nod - 39 * 1.9, 1.9, rot=nod * 0.4)
    d = ImageDraw.Draw(img)
    pd = ImageDraw.Draw(img)
    pd.polygon([(120, 1000), (960, 1000), (930, 1640), (150, 1640)], fill=(62, 86, 128))
    pd.line([(160, 1030), (920, 1030)], fill=(220, 170, 90), width=5)
    pd.line([(120, 1000), (960, 1000)], fill=OUT, width=8)
    for k in range(3):
        u = (tl * 0.7 + k * 0.33) % 1
        paste(img, BUB['note'], 820 + 80 * u, 700 - 260 * u, 0.4 * math.sin(math.pi * u))
    return img

SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate([s1, s2, s3, s4, s5])]
EP = Episode('ep16', SCENES, CHUNKS, DUR, END_TAG)

def audio_plan():
    import pf_audio as A
    t_alarm = starts[1] - 0.1
    sfx = [(A.rustle(), 0.05, 1.0, 0), (A.whistle(0.4), 0.6, 0.35, 0.3), (A.whistle(0.3), 1.6, 0.3, 0.3)]
    sfx += [(A.honk(880, 0.2), t_alarm + k * 0.3, 0.32, 0.2) for k in range(5)]
    sfx += [(A.whistle(0.25), B[1] + 0.2 + k * 0.32, 0.25, ((k % 3) - 1) * 0.4) for k in range(10)]
    sfx += [(A.whoosh(0.4), B[2] - 0.1, 0.5, 0), (A.boing(), B[2] + 0.25, 0.35, 0)]
    sfx += [(A.chime(988.0), B[2] + 0.4 + k * 0.6, 0.2, 0) for k in range(3)]
    sfx += [(A.honk(760, 0.22), starts[5] - 0.1 + k * 0.28, 0.32, 0.1) for k in range(5)]
    sfx += [(A.whistle(0.6), B[3] + 0.3, 0.3, -0.3), (A.whistle(0.5), B[3] + 1.4, 0.3, -0.3), (A.thud(), B[3] + 1.2, 0.3, 0.5)]
    sfx += [(A.pop(), B[4] + 0.2, 0.6, 0), (A.pop(), END_TAG, 0.7, 0), (A.chime(1318.5), END_TAG + 0.05, 0.4, 0)]
    cues = [(f'/home/claude/eps/ep16_vo_{i}.wav', s) for i, s in enumerate(starts)]
    return cues, sfx

if __name__ == '__main__':
    if sys.argv[1] == 'audio':
        import pf_audio as A
        cues, sfx = audio_plan()
        A.build(DUR, cues, sfx, '/home/claude/eps/ep16/audio.wav', style=STYLE)
        print('audio ok')
    else:
        EP.main(sys.argv)
