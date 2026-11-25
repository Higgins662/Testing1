import sys, math, random
import numpy as np
from PIL import Image, ImageDraw
from pf import *

STYLE = 'synth'
lines, durs, starts, DUR = timeline('ep19', gap=0.26, gaps={0: 0.42, 3: 0.32, 5: 0.36, 6: 0.36})
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={0: ['ACTUAL', 'BUG.'], 1: ['1947,'], 3: ['MOTH'], 5: ['BUG'], 7: ['MOTHS.']})
END_TAG = starts[-1] + durs[-1] + 0.35

MOTH = (176, 160, 136)
MOTH_D = (130, 116, 98)

# ------------------------------------------------------------ moth (canvas 300x240, centre 150,120)
def moth(pen, dazed=False, flat=False):
    for d in (-1, 1):
        pen.poly([(150, 110), (150 + d * 40, 50), (150 + d * 120, 40), (150 + d * 138, 90), (150 + d * 90, 130)], MOTH, w=4)
        pen.poly([(150, 128), (150 + d * 70, 140), (150 + d * 100, 190), (150 + d * 50, 200)], MOTH_D, w=4)
        pen.ell(150 + d * 80, 80, 16, 12, fill=(150, 134, 112), w=2.5)
    pen.ell(150, 128, 18, 56, fill=(110, 96, 80), w=4)
    pen.ell(150, 76, 20, 18, fill=(110, 96, 80), w=4)
    for d in (-1, 1):
        pen.line([(150 + d * 6, 62), (150 + d * 26, 30), (150 + d * 40, 26)], OUT, 3.5)
    if dazed:
        for d in (-1, 1):
            cx = 150 + d * 9
            pen.line([(cx - 5, 72), (cx + 5, 80)], OUT, 3); pen.line([(cx + 5, 72), (cx - 5, 80)], OUT, 3)
    elif not flat:
        pen.dot(143, 74, 5, OUT); pen.dot(157, 74, 5, OUT)
        pen.dot(144, 73, 1.8, (255, 255, 255)); pen.dot(158, 73, 1.8, (255, 255, 255))

def crown(pen):
    pen.poly([(10, 70), (20, 20), (45, 50), (60, 10), (75, 50), (100, 20), (110, 70)], (240, 196, 80), w=3.5)

# ------------------------------------------------------------ relay panel / computer room
def relay_panel():
    img = bg_canvas([(0, (40, 44, 52)), (1, (26, 28, 34))], glows=[(540, 800, 700, (110, 120, 110), 0.4)])
    def fn(pen):
        pen.poly([(60, 160), (1020, 160), (1020, 1280), (60, 1280)], (86, 96, 92), w=6)
        for r in range(7):
            for c in range(6):
                x, y = 140 + c * 150, 240 + r * 150
                pen.poly(rrect(x - 50, y - 50, x + 50, y + 50, 10), (170, 160, 136), w=4)
                pen.poly([(x - 30, y - 30), (x + 30, y - 30), (x + 30, y + 30), (x - 30, y + 30)], (120, 110, 92), w=3)
                pen.line([(x - 30, y), (x + 30, y)], (200, 190, 160), 3)
        for k in range(12):
            pen.line([(60, 200 + k * 92), (20, 210 + k * 92)], (60, 60, 70), 6)
    return make_sprite(W, H, fn, seed=2, base=img)

BULBS = [(140 + c * 150 + 40, 240 + r * 150 - 40) for r in range(7) for c in range(6)]

def room_bg():
    img = bg_canvas([(0, (56, 62, 70)), (1, (34, 36, 44))], glows=[(540, 500, 600, (120, 130, 120), 0.35)])
    def fn(pen):
        pen.poly([(-20, 1200), (1100, 1200), (1100, 1940), (-20, 1940)], (70, 62, 58), w=4)
        for k in range(6):
            x = -20 + k * 190
            pen.poly([(x, 1200), (x, 340), (x + 180, 340), (x + 180, 1200)], (110, 116, 108), w=5)
            for r in range(7):
                for c in range(3):
                    bx, by = x + 34 + c * 56, 400 + r * 110
                    pen.ell(bx, by, 14, 14, fill=(80, 84, 80), w=2.5)
            pen.poly([(x + 20, 1140), (x + 160, 1140), (x + 160, 1180), (x + 20, 1180)], (90, 94, 88), w=3)
        for k in range(8):
            x0 = 60 + k * 130
            pen.line([(x0, 340), (x0 + 40, 250), (x0 + 120, 230), (x0 + 160, 120)], (40, 40, 46), 6, amp=4)
    return make_sprite(W, H, fn, seed=3, base=img)

def engineer(pen, k):
    coat = (232, 230, 222) if k == 0 else (120, 130, 150)
    pen.poly([(60, 520), (80, 260), (150, 220), (220, 260), (240, 520)], coat, w=5)
    pen.ell(150, 160, 70, 76, fill=(70, 66, 76), w=4.5)
    pen.poly([(84, 140), (96, 90), (150, 76), (204, 90), (216, 140), (190, 112), (110, 112)], (50, 46, 54), w=3.5)
    pen.poly(capsule(200, 300, 300, 250, 24), coat, w=4)
    pen.poly([(296, 230), (350, 220), (356, 256), (300, 270)], (60, 60, 66), w=4)
    pen.ell(354, 238, 10, 20, fill=(255, 240, 190), w=3)

def tweezers(pen):
    pen.poly([(30, 20), (50, 20), (140, 380), (128, 384)], (200, 204, 210), w=4)
    pen.poly([(70, 20), (90, 20), (150, 384), (138, 386)], (180, 184, 190), w=4)
    pen.poly([(26, 10), (94, 10), (94, 34), (26, 34)], (160, 164, 170), w=4)

def logbook(pen):
    pen.poly([(20, 30), (900, 20), (910, 1060), (30, 1070)], (240, 232, 206), w=6, amp=2)
    for k in range(20):
        y = 110 + k * 46
        pen.line([(70, y), (870, y - 4)], (170, 196, 214), 2.5, amp=0.6)
    pen.line([(150, 40), (156, 1060)], (220, 140, 140), 3)
    rng = random.Random(2)
    for row in [0, 1, 2, 3, 9, 10, 11, 14, 15, 16, 17]:
        y = 100 + row * 46
        x = 180
        while x < 800:
            wlen = rng.uniform(40, 110)
            pts = [(x + i * wlen / 8, y - 8 + 8 * math.sin(i * 1.7 + row)) for i in range(9)]
            pen.line(pts, (60, 70, 110), 3, amp=0.8)
            x += wlen + rng.uniform(16, 30)
    pen.text((110, 100), '1545', 30, (60, 70, 110), font=FONT_HAND)

def tape(pen):
    pen.poly([(10, 20), (150, 10), (156, 60), (14, 70)], (250, 240, 190, 225), outline=(196, 178, 120), w=3, amp=0.8)

def museum_frame(pen):
    pen.poly([(0, 0), (1000, 0), (1000, 1160), (0, 1160)], None, outline=(120, 86, 50), w=28, amp=0.5)
    pen.poly([(20, 20), (980, 20), (980, 1140), (20, 1140)], None, outline=(210, 170, 90), w=8, amp=0.5)

def plaque(pen):
    pen.poly(rrect(10, 10, 430, 130, 14), (60, 50, 44), w=4)
    pen.text((220, 52), 'LOGBOOK, 1947', 38, (240, 220, 170), font=FONT_CAP)
    pen.text((220, 100), 'moth included', 34, (220, 200, 160), font=FONT_HAND)

def laptop(pen):
    pen.poly([(80, 40), (720, 40), (720, 440), (80, 440)], (60, 64, 72), w=6)
    pen.poly([(110, 70), (690, 70), (690, 410), (110, 410)], (236, 240, 246), w=3)
    pen.poly([(110, 70), (690, 70), (690, 120), (110, 120)], (200, 210, 226), w=3)
    for k in range(4):
        y = 160 + k * 60
        pen.poly(rrect(140, y, 660, y + 40, 8), (226, 230, 238), outline=(214, 218, 226), w=2)
    pen.text((400, 300), 'INBOX: 0', 44, (150, 156, 170), font=FONT_CAP)
    pen.poly([(20, 440), (780, 440), (740, 490), (60, 490)], (90, 94, 104), w=5)

def flashlight(pen):
    pen.poly(capsule(20, 60, 130, 60, 22), (230, 196, 70), w=4)
    pen.poly([(130, 36), (170, 26), (170, 94), (130, 84)], (200, 170, 60), w=4)

# ------------------------------------------------------------ assets
print('assets...', file=sys.stderr)
PANEL = relay_panel()
ROOM = room_bg()
MOTHS = [make_sprite(300, 240, moth, seed=s) for s in (1, 2, 3)]
MOTH_DAZED = [make_sprite(300, 240, lambda p: moth(p, dazed=True), seed=s) for s in (1, 2, 3)]
MOTH_FLAT = make_sprite(300, 240, lambda p: moth(p, flat=True), seed=4)
CROWN = make_sprite(120, 80, crown, seed=5)
ENG = [make_sprite(380, 540, lambda p, k=k: engineer(p, k), seed=6 + k) for k in (0, 1)]
TWEEZ = make_sprite(180, 400, tweezers, seed=7)
BOOK = make_sprite(940, 1100, logbook, seed=8)
TAPE = make_sprite(170, 80, tape, seed=9)
FRAME = make_sprite(1000, 1160, museum_frame, seed=10)
PLAQUE = make_sprite(440, 140, plaque, seed=11)
LAPTOP = make_sprite(800, 500, laptop, seed=12)
TORCH = make_sprite(190, 120, flashlight, seed=13)
FUZZ = fuzz_sprites('happy')
DESK = downsample(bg_canvas([(0, (64, 60, 84)), (1, (40, 38, 54))], glows=[(540, 820, 700, (160, 150, 200), 0.45)]), W, H)
GALLERY = downsample(bg_canvas([(0, (120, 106, 92)), (1, (80, 70, 62))], glows=[(540, 700, 650, (255, 230, 180), 0.55)]), W, H)

def blink_bulbs(img, tl, n=42):
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for k, (x, y) in enumerate(BULBS[:n]):
        on = (math.sin(tl * 6 + k * 1.7) + math.sin(tl * 2.3 + k)) > 0.6
        c = (255, 220, 120, 255) if on else (90, 80, 60, 255)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=c, outline=OUT, width=3)
    img.alpha_composite(lay)

def beam(img, x0, y0, x1, y1, w0=20, w1=180, alpha=0.35):
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    ang = math.atan2(y1 - y0, x1 - x0); nx, ny = -math.sin(ang), math.cos(ang)
    d.polygon([(x0 + nx * w0, y0 + ny * w0), (x1 + nx * w1, y1 + ny * w1), (x1 - nx * w1, y1 - ny * w1), (x0 - nx * w0, y0 - ny * w0)],
              fill=(255, 244, 190, int(255 * alpha)))
    img.alpha_composite(lay)

# ------------------------------------------------------------ scenes
B = [0] + [starts[i] - 0.15 for i in (1, 3, 4, 7)] + [DUR]

def s1(tl, frame, sd):
    img = PANEL.copy()
    blink_bulbs(img, tl)
    proud = 1 + 0.04 * math.sin(tl * 3)
    paste(img, MOTHS[boil(frame)], 540, 760, 1.6 * proud)
    paste(img, CROWN, 540, 760 - 150 * proud, 1.0 * ease_back(seg(tl, 0.6, 1.0), 2.0), rot=-8)
    return camera(img, lerp(1.25, 1.12, ease(tl / sd)), 540, 800)

def s2(tl, frame, sd):
    img = ROOM.copy()
    paste(img, ENG[0], 330, 1040, 1.15)
    paste(img, ENG[1], 800, 1060, 1.1, flip=True)
    sweep = math.sin(tl * 1.4)
    beam(img, 330 + 1.15 * 200, 1040 - 1.15 * 30, 560 + 200 * sweep, 620, alpha=0.3)
    beam(img, 800 - 1.1 * 200, 1060 - 1.1 * 25, 520 - 160 * sweep, 700, alpha=0.3)
    d = ImageDraw.Draw(img)
    d.text((540, 200), '1947', font=font(FONT_CAP, 120), fill=HL, anchor='mm', stroke_width=10, stroke_fill=OUT)
    return img

def s3(tl, frame, sd):
    img = PANEL.copy()
    blink_bulbs(img, tl)
    img = camera(img, 1.6, 540, 760)
    lift = ease(seg(tl, 0.5, 1.8))
    my = lerp(820, 520, lift)
    paste(img, MOTH_DAZED[boil(frame)] if lift > 0.05 else MOTHS[boil(frame)], 540 + 10 * math.sin(tl * 5) * lift, my + 60, 1.5, rot=12 * math.sin(tl * 4) * lift)
    paste(img, TWEEZ, 560, my - 150, 1.3)
    if lift > 0.6:
        for k in range(4):
            a = tl * 4 + k * math.pi / 2
            sparkle(img, 540 + 110 * math.cos(a), my - 40 + 40 * math.sin(a), 22, color=(255, 240, 150))
    return img

def s4(tl, frame, sd):
    t_mus = starts[6] - B[3]
    m = ease(seg(tl, t_mus - 0.1, t_mus + 0.7))
    img = DESK.copy() if m < 0.01 else Image.blend(DESK.convert('RGB'), GALLERY.convert('RGB'), m).convert('RGBA')
    sc = lerp(1.0, 0.82, m)
    paste(img, BOOK, 540, 760, sc, rot=-2)
    tu = ease_back(seg(tl, 0.3, 0.7), 1.6)
    paste(img, MOTH_FLAT, 540, 600 * 1 + (760 - 600) * (1 - sc), 1.0 * sc * max(0.05, tu))
    tape_u = ease_out(seg(tl, 0.8, 1.2))
    if tape_u > 0.02:
        my_ = 600 + (760 - 600) * (1 - sc)
        paste(img, TAPE, 540 - 120 * sc, my_ - 50 * sc, sc * 0.75 * tape_u, rot=35)
        paste(img, TAPE, 540 + 120 * sc, my_ - 50 * sc, sc * 0.75 * tape_u, rot=-35)
    if tl > starts[5] - B[3] - 0.1:
        d = ImageDraw.Draw(img)
        k = int(30 * seg(tl, starts[5] - B[3], starts[5] - B[3] + 1.8))
        sq = [(400 + i * 10 * sc, (600 + (760 - 600) * (1 - sc)) + 150 * sc + 14 * math.sin(i * 1.3)) for i in range(k)]
        if len(sq) > 1:
            d.line(sq, fill=(60, 70, 110), width=5)
    if m > 0.02:
        paste(img, FRAME, 540, 760, sc * 1.0, alpha=m)
        paste(img, PLAQUE, 540, 1220, 0.9 * m, alpha=m)
    return img

def s5(tl, frame, sd):
    img = DESK.copy()
    paste(img, LAPTOP, 540, 880, 1.15)
    peek = ease_back(seg(tl, 0.2, 0.7), 1.8)
    sway = 120 * math.sin(tl * 1.6)
    fx = 540 + 330 * math.copysign(1, math.sin(tl * 0.8 + 0.3))
    fy = lerp(1000, 600, peek)
    paste(img, FUZZ[boil(frame)], 860, lerp(1100, 560, peek), 0.75)
    paste(img, TORCH, 720, lerp(1100, 600, peek), 0.7, rot=20, flip=True)
    if peek > 0.5:
        beam(img, 680, lerp(1100, 600, peek), 320 + sway, 520, w0=10, w1=110, alpha=0.3)
    return img

SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate([s1, s2, s3, s4, s5])]
EP = Episode('ep19', SCENES, CHUNKS, DUR, END_TAG)

def audio_plan():
    import pf_audio as A
    sfx = [(A.rustle(), 0.05, 1.0, 0)] + [(A.tick(1100 + 200 * (k % 3), 0.05, 0.4), 0.2 + k * 0.23, 0.25, ((k % 5) - 2) * 0.2) for k in range(14)]
    sfx += [(A.chime(1046.5), 0.75, 0.3, 0)]
    sfx += [(A.engine(B[2] - B[1], 55), B[1], 0.25, 0), (A.tick(700, 0.06, 0.6), B[1] + 0.3, 0.5, -0.3), (A.tick(700, 0.06, 0.6), B[1] + 0.5, 0.5, 0.3)]
    sfx += [(A.tick(2400, 0.05, 0.5), B[2] + 0.5, 0.5, 0), (A.sparkles(), B[2] + 1.9, 0.35, 0)]
    sfx += [(A.whoosh(0.3, False), B[3] + 0.3, 0.4, 0), (A.rustle(0.25), B[3] + 0.85, 0.7, -0.2), (A.rustle(0.25), B[3] + 1.0, 0.7, 0.2)]
    sfx += [(A.scribble(1.8), starts[5], 0.6, 0.2), (A.chime(784.0), starts[6] + 0.2, 0.35, 0)]
    sfx += [(A.tick(900, 0.05, 0.5), B[4] + 0.6, 0.4, 0.3), (A.pop(), END_TAG, 0.7, 0), (A.chime(1318.5), END_TAG + 0.05, 0.4, 0)]
    cues = [(f'/home/claude/eps/ep19_vo_{i}.wav', s) for i, s in enumerate(starts)]
    return cues, sfx

if __name__ == '__main__':
    if sys.argv[1] == 'audio':
        import pf_audio as A
        cues, sfx = audio_plan()
        A.build(DUR, cues, sfx, '/home/claude/eps/ep19/audio.wav', style=STYLE)
        print('audio ok')
    else:
        EP.main(sys.argv)
