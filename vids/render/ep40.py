"""Ep 40 Bouncy Berries (loop cut): good cranberries bounce; four air pockets; the stairs story; bounce separators."""
import sys, math, random
from PIL import Image, ImageDraw
from pf import *

NAME = 'ep40'
STYLE = 'ambient'
lines, durs, starts, DUR = timeline(NAME, first=0.15, gap=0.28, gaps={0: 0.32, 3: 0.32}, tail=0.42)
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={})
NO_END_TAG = DUR + 99

RED = (206, 38, 58)
RED_D = (150, 22, 44)
FLESH = (250, 226, 214)
WOOD = (186, 128, 84)
WOOD_D = (150, 98, 62)
WATER = (70, 130, 170)

def overlay(img, text, u, y=270, size=104):
    if u <= 0.02: return
    ImageDraw.Draw(img).text((540, y), text, font=font(FONT_CAP, int(size * u)), fill=HL,
                             anchor='mm', stroke_width=11, stroke_fill=OUT)

# ------------------------------------------------------------ backgrounds
def _kitchen():
    img = downsample(bg_canvas([(0, (250, 230, 200)), (0.6, (244, 214, 178)), (1, (230, 196, 160))],
                               glows=[(760, 520, 520, (255, 244, 214), 0.6)]), W, H)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([600, 380, 960, 760], 18, fill=(196, 226, 240), outline=OUT, width=7)   # window
    d.line([(780, 380), (780, 760)], fill=OUT, width=6); d.line([(600, 570), (960, 570)], fill=OUT, width=6)
    d.rectangle([0, 1180, W, H], fill=WOOD)
    d.line([(0, 1180), (W, 1180)], fill=OUT, width=7)
    for k in range(5):
        y = 1250 + k * 110
        d.line([(0, y), (W, y + 10)], fill=WOOD_D, width=3)
    return img
KITCHEN = _kitchen()

LAB = downsample(bg_canvas([(0, (60, 56, 80)), (1, (36, 34, 52))], glows=[(540, 860, 620, (120, 90, 130), 0.5)]), W, H)

def _bog():
    img = downsample(bg_canvas([(0, (176, 206, 230)), (0.5, (214, 228, 236)), (1, (200, 214, 222))]), W, H)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 620), (300, 560), (700, 590), (1080, 540), (1080, 760), (0, 760)], fill=(110, 140, 96))
    d.rectangle([0, 740, W, H], fill=WATER)
    d.line([(0, 740), (W, 740)], fill=OUT, width=6)
    return img
BOG = _bog()

def _stairs():
    img = downsample(bg_canvas([(0, (236, 222, 208)), (1, (214, 196, 180))]), W, H)
    d = ImageDraw.Draw(img)
    for k in range(6):
        x0 = 80 + k * 150; y0 = 520 + k * 120
        d.rectangle([x0, y0, W, y0 + 120], fill=(200, 150, 110) if k % 2 else (186, 136, 98))
        d.line([(x0, y0), (W, y0)], fill=OUT, width=6)
        d.line([(x0, y0), (x0, y0 + 120)], fill=OUT, width=6)
    return img
STAIRS = _stairs()
STEP = [(80 + k * 150 + 75, 520 + k * 120) for k in range(6)]      # top surface centre of each step

def _factory():
    img = downsample(bg_canvas([(0, (206, 214, 222)), (1, (176, 186, 198))]), W, H)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1180, W, H], fill=(140, 146, 156)); d.line([(0, 1180), (W, 1180)], fill=OUT, width=7)
    return img
FACTORY = _factory()

# ------------------------------------------------------------ sprites
def berry(pen, soft=False):           # canvas 200x200
    if soft:
        pen.ell(100, 120, 78, 58, fill=(120, 30, 50), w=5)
        pen.ell(76, 104, 14, 9, fill=(160, 70, 86), outline=None, amp=0.3)
        for x in (70, 110, 140):
            pen.line([(x, 96), (x + 8, 110)], (90, 20, 38), 3, amp=0.4)
    else:
        pen.ell(100, 104, 72, 70, fill=RED, w=5)
        pen.ell(72, 78, 18, 12, fill=(250, 140, 150), outline=None, amp=0.3)
        pen.line([(100, 36), (92, 24)], (90, 60, 40), 4)
        for a in range(5):
            r = math.radians(a * 72)
            pen.line([(100, 40), (100 + 12 * math.cos(r), 40 + 12 * math.sin(r))], (120, 70, 50), 3, amp=0.2)

def splat(pen):                        # canvas 260x120
    pen.poly([(20, 90), (50, 60), (90, 70), (130, 50), (170, 68), (220, 56), (240, 92), (200, 104), (60, 106)], (130, 26, 48), w=4.5, amp=1.4)
    pen.dot(40, 40, 8, (130, 26, 48)); pen.dot(226, 36, 7, (130, 26, 48))

def cutaway(pen):                      # canvas 600x600
    pen.ell(300, 300, 270, 266, fill=RED, w=7)
    pen.ell(300, 300, 236, 232, fill=FLESH, w=4)
    for a in range(4):
        r = math.radians(45 + a * 90)
        cx, cy = 300 + 108 * math.cos(r), 300 + 108 * math.sin(r)
        pen.ell(cx, cy, 70, 52, fill=(255, 250, 246), w=4, rot=math.degrees(r))
        pen.dot(300 + 40 * math.cos(r), 300 + 40 * math.sin(r), 9, (200, 160, 110))
    pen.ell(300, 300, 20, 20, fill=(236, 190, 170), w=3)

def machine(pen):                      # canvas 900x420  conveyor with barriers
    pen.poly(rrect(20, 300, 880, 360, 26), (90, 96, 110), w=5)
    for x in range(60, 880, 70):
        pen.dot(x, 330, 12, (60, 64, 76))
    for x in (240, 520, 780):
        pen.poly(rrect(x - 14, 170, x + 14, 300, 6), WOOD, w=4.5)

def binbox(pen):                       # canvas 260x220
    pen.poly([(20, 40), (240, 40), (215, 210), (45, 210)], (120, 126, 140), w=5)
    pen.text((130, 125), 'NOPE', 52, (250, 244, 236))

BERRY = [make_sprite(200, 200, berry, seed=s) for s in (1, 2, 3)]
SOFT = [make_sprite(200, 200, lambda p: berry(p, True), seed=s) for s in (1, 2, 3)]
SPLAT = make_sprite(260, 120, splat, seed=4)
CUT = [make_sprite(600, 600, cutaway, seed=s) for s in (1, 2, 3)]
MACHINE = make_sprite(900, 420, machine, seed=5)
BIN = make_sprite(260, 220, binbox, seed=6)
FUZZ_S = fuzz_sprites('happy')
FUZZ_W = fuzz_sprites('shock')

def hop(u, h):
    """parabolic hop: 0 at u=0 and u=1, peak h at 0.5"""
    return 4 * h * u * (1 - u)

# scenes: hook | air pockets | bog | stairs story | machine | loop back
B = [0] + [starts[i] - 0.14 for i in (1, 2, 3, 4, 5)] + [DUR]

BX, BY = 400, 1110                      # berry rest position on the table

def rest_pose(p):
    return BX, BY - 4 * math.sin(p * 3.0)

def s1(tl, frame, sd):
    img = KITCHEN.copy()
    # good berry: bounces 3 times, settling
    t0 = 0.25
    y = BY
    for k, (dur, h) in enumerate([(0.62, 420), (0.42, 190), (0.28, 70)]):
        if t0 <= tl < t0 + dur:
            y = BY - hop((tl - t0) / dur, h)
        t0 += dur
    if tl < 0.25 or tl >= t0:
        y = rest_pose(tl)[1] if tl < 0.25 else BY
    sq = 1.0
    paste(img, BERRY[boil(frame)], BX, y, 1.0, sy=sq)
    # soft berry drops and splats at "Soft ones just go splat"
    t_s = starts[0] + 1.45
    if tl > t_s - 0.45:
        u = seg(tl, t_s - 0.45, t_s)
        if u < 1:
            paste(img, SOFT[boil(frame)], 760, lerp(500, BY, ease_in(u)), 1.0)
        else:
            paste(img, SPLAT, 760, BY + 40, 1.0, sy=ease_back(seg(tl, t_s, t_s + 0.2), 2.0))
    overlay(img, 'THEY BOUNCE', ease_back(seg(tl, 0.35, 0.65), 2.0) * (1 - seg(tl, t_s - 0.1, t_s)))
    overlay(img, 'SPLAT', ease_back(seg(tl, t_s, t_s + 0.25), 2.0), size=130)
    return img

def s2(tl, frame, sd):
    img = LAB.copy()
    u = ease_back(seg(tl, 0, 0.45), 1.6)
    paste(img, CUT[boil(frame)], 540, 860, max(0.05, u), rot=4 * math.sin(tl * 1.5))
    for a in range(4):
        r = math.radians(45 + a * 90)
        pu = seg(tl, 0.6 + a * 0.25, 0.9 + a * 0.25)
        if pu > 0:
            sparkle(img, 540 + 108 * math.cos(r), 860 + 108 * math.sin(r), 26 * math.sin(math.pi * pu))
    overlay(img, '4 AIR POCKETS', ease_back(seg(tl, 0.4, 0.7), 2.0))
    return img

rng = random.Random(7)
FLOAT = [(rng.uniform(40, 1040), rng.uniform(760, 1100), rng.uniform(0.25, 0.42), rng.uniform(0, 1.2)) for _ in range(70)]

def s3(tl, frame, sd):
    img = BOG.copy()
    for k, (x, y, sc, delay) in enumerate(FLOAT):
        u = ease_out(seg(tl, delay, delay + 0.9))
        yy = lerp(1500 + (k % 7) * 40, y, u) + 6 * math.sin(tl * 2 + k)
        paste(img, BERRY[(boil(frame) + k) % 3], x, yy, sc)
    d = ImageDraw.Draw(img)
    for k in range(6):
        x = (k * 210 + tl * 60) % (W + 200) - 100
        d.arc([x, 735, x + 140, 770], 200, 340, fill=(200, 226, 240), width=5)
    overlay(img, 'THEY FLOAT', ease_back(seg(tl, 0.3, 0.6), 2.0))
    return img

def s4(tl, frame, sd):
    img = STAIRS.copy()
    t_spill = 1.0
    t_fresh = starts[3] - B[3] + 2.6         # "Only the fresh ones bounced to the bottom"
    # soft berries stay on the top step
    for k in range(3):
        paste(img, SOFT[(boil(frame) + k) % 3], STEP[0][0] - 40 + k * 45, STEP[0][1] - 26, 0.42)
    # fresh berries hop down step by step
    for j in range(4):
        start = t_spill + j * 0.35
        if tl < start:
            paste(img, BERRY[(boil(frame) + j) % 3], STEP[0][0] + 60 - j * 20, STEP[0][1] - 30, 0.42)
            continue
        steps = (tl - start) / 0.38
        i = min(int(steps), 5)
        u = steps - int(steps) if steps < 5 else 1.0
        x0, y0 = STEP[i]; x1, y1 = STEP[min(i + 1, 5)]
        x = lerp(x0, x1, u); y = lerp(y0, y1, u) - hop(u, 110) - 30
        if steps >= 5:
            x, y = STEP[5][0] + 60 + j * 46 - 120, STEP[5][1] - 30
        paste(img, BERRY[(boil(frame) + j) % 3], x, y, 0.42)
    overlay(img, 'THE STAIRS TEST', ease_back(seg(tl, 0.3, 0.6), 2.0) * (1 - seg(tl, t_fresh - 0.1, t_fresh)), size=96)
    overlay(img, 'FRESH = BOUNCY', ease_back(seg(tl, t_fresh, t_fresh + 0.3), 2.0), size=96)
    return img

def s5(tl, frame, sd):
    img = FACTORY.copy()
    paste(img, MACHINE, 540, 760, 1.0)
    period = 2.4
    for j in range(6):
        ph = (tl / period + j / 6) % 1.0
        good = j % 3 != 1
        xu = lerp(1010, 40, ph)
        x, y = xu, 812
        if good:
            for bx in (330, 610, 870):
                du = ((bx + 85) - x) / 170
                if 0 <= du <= 1:
                    y -= hop(du, 210)
        elif xu < 905:
            x = 905
            fu = (905 - xu) / 260
            y = 812 + 420 * fu * fu
            if y > 1010: continue
        paste(img, (BERRY if good else SOFT)[(boil(frame) + j) % 3], x, y, 0.38)
    paste(img, BIN, 905, 1060, 0.85)
    fu = ease_back(seg(tl, 1.4, 1.8), 1.6)
    paste(img, (FUZZ_W if tl < 2.3 else FUZZ_S)[boil(frame)], 200, lerp(1260, 1010, fu), 0.7)
    overlay(img, 'NO BOUNCE', ease_back(seg(tl, 0.3, 0.6), 2.0) * (1 - seg(tl, 2.5, 2.6)))
    overlay(img, 'NO SALE', ease_back(seg(tl, 2.6, 2.9), 2.0))
    return img

def s6(tl, frame, sd):
    img = KITCHEN.copy()
    p = tl - sd
    x, y = rest_pose(p)
    u = ease_out(seg(tl, 0, 0.9))
    paste(img, BERRY[boil(frame)], x, lerp(-200, y, u) - hop(seg(tl, 0.9, 1.3), 60), 1.0)
    return img

SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate([s1, s2, s3, s4, s5, s6])]
EP = Episode(NAME, SCENES, CHUNKS, DUR, NO_END_TAG, loop=True)

def audio_plan():
    import pf_audio as A
    sfx = []
    t0 = 0.25
    for dur, g in [(0.62, 0.5), (0.42, 0.35), (0.28, 0.22)]:
        t0 += dur; sfx.append((A.boing(), t0 - 0.02, g, -0.2))
    sfx += [(A.splash(), starts[0] + 1.45, 0.45, 0.3)]
    sfx += [(A.whoosh(0.45), B[1] - 0.1, 0.5, 0)] + [(A.chime(880 + 110 * a), B[1] + 0.65 + a * 0.25, 0.25, (a - 1.5) * 0.3) for a in range(4)]
    sfx += [(A.splash(), B[2] + 0.2, 0.4, 0), (A.sparkles(), B[2] + 0.8, 0.3, 0.2)]
    for j in range(4):
        for s in range(5):
            sfx.append((A.tick(1400 + 90 * j, 0.05, 0.5), B[3] + 1.0 + j * 0.35 + (s + 1) * 0.38, 0.22, -0.4 + 0.2 * s))
    sfx += [(A.boing(), B[4] + 0.4 + k * 0.55, 0.25, 0.2 * (k % 3 - 1)) for k in range(6)]
    sfx += [(A.thud(), B[4] + 1.0, 0.3, -0.5), (A.pop(), B[4] + 1.45, 0.4, 0.4)]
    sfx += [(A.whoosh(0.7, False), B[5] - 0.05, 0.4, 0), (A.boing(), B[5] + 1.0, 0.3, 0)]
    cues = [(f'/home/claude/eps/{NAME}_vo_{i}.wav', s) for i, s in enumerate(starts)]
    return cues, sfx

if __name__ == '__main__':
    if sys.argv[1] == 'audio':
        import pf_audio as A
        cues, sfx = audio_plan()
        A.build(DUR, cues, sfx, f'/home/claude/eps/{NAME}/audio.wav', style=STYLE, loop=True)
        print('audio ok')
    elif sys.argv[1] == 'preview' and 'LAST' in sys.argv[2]:
        EP.main([sys.argv[0], 'preview', sys.argv[2].replace('LAST', f'{DUR - 1 / FPS:.3f}')])
    else:
        EP.main(sys.argv)
