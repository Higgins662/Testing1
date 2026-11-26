"""Ep 39 Wasp Face Cells (loop cut): paper wasps have face-selective brain cells (Cell, Nov 2026)."""
import sys, math, random
from PIL import Image, ImageDraw
from pf import *

NAME = 'ep39'
STYLE = 'synth'
lines, durs, starts, DUR = timeline(NAME, first=0.15, gap=0.24, gaps={0: 0.3, 4: 0.3}, tail=0.42)
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={0: ['FACE.', 'FACE', 'CELLS.'], 1: ['OWN'], 2: ['PICTURES'],
                                                     3: ['RICE-SIZED', 'WASP', 'FACES.'], 4: ['JUST', 'WASPS.'],
                                                     5: ['FIRST', 'INSECT.'], 6: ['REMEMBER:']})
NO_END_TAG = DUR + 99

# ------------------------------------------------------------ palette
BROWN = (150, 82, 46)
BROWN_D = (108, 58, 34)
YEL = (242, 198, 72)
EYE = (52, 34, 44)
AMBER = (196, 122, 60)
COMB = (198, 192, 180)
COMB_D = (150, 144, 134)
DENIM = (82, 112, 160)
DENIM_D = (62, 88, 132)
STITCH = (232, 164, 84)
PINK = (236, 186, 194)
RICE = (248, 244, 230)
GOLD = (238, 186, 70)
PAPER = (250, 248, 240)

# ------------------------------------------------------------ backgrounds
def branch_layer(pen):        # canvas 1080x560: branch, leaves and the twig the pocket hangs on
    pen.line([(-20, 210), (200, 200), (420, 230), (640, 215), (880, 250), (1100, 235)], (112, 80, 56), 26, amp=2)
    pen.line([(-20, 210), (200, 200), (420, 230), (640, 215), (880, 250), (1100, 235)], (140, 102, 72), 10, amp=2)
    rng = random.Random(4)
    for x, y, r, s in [(90, 170, -30, 1.0), (520, 190, 25, 1.2), (700, 260, 160, 0.9), (960, 200, -20, 1.1), (820, 170, 200, 0.8)]:
        pts = ellpts(0, 0, 95 * s, 40 * s, n=40)
        pen.poly(xform(pts, x, y, rot=r), (118, 150, 104), w=4)
        pen.line(xform([(-90 * s, 0), (90 * s, 0)], x, y, rot=r), (88, 118, 80), 3)

def twig(pen):                # canvas 400x80
    pen.line([(420, 40), (260, 30), (120, 44), (30, 36)], (112, 80, 56), 14, amp=1.5)
    pen.line([(200, 34), (160, 8)], (112, 80, 56), 7)

def _garden():
    img = downsample(bg_canvas([(0, (172, 196, 168)), (0.55, (210, 208, 192)), (1, (192, 180, 204))],
                               glows=[(780, 420, 560, (255, 236, 196), 0.55)]), W, H)
    paste(img, make_sprite(1080, 560, branch_layer, seed=3), 540, 280 + 280 - 230, 1.0)
    paste(img, make_sprite(400, 80, twig, seed=4), 900, 1010, 1.0)
    return img
GARDEN = _garden()

def _lineup():
    img = downsample(bg_canvas([(0, (200, 190, 214)), (1, (176, 164, 194))],
                               glows=[(540, 700, 600, (250, 240, 230), 0.4)]), W, H)
    d = ImageDraw.Draw(img)
    for k in range(7):
        y = 560 + k * 90
        d.line([(0, y), (W, y)], fill=(156, 144, 176), width=4)
    d.rectangle([0, 1160, W, H], fill=(120, 104, 120))
    d.line([(0, 1160), (W, 1160)], fill=OUT, width=6)
    return img
LINEUP = _lineup()

def _lab():
    img = downsample(bg_canvas([(0, (84, 76, 96)), (0.7, (110, 98, 110)), (1, (126, 110, 112))],
                               glows=[(260, 520, 620, (255, 226, 170), 0.45)]), W, H)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1230, W, H], fill=(166, 114, 76))
    d.line([(0, 1230), (W, 1230)], fill=OUT, width=7)
    for k in range(5):
        yy = 1290 + k * 90
        d.line([(0, yy), (W, yy + 12)], fill=(146, 98, 64), width=3)
    return img
LAB = _lab()

# ------------------------------------------------------------ sprites
FACE_PATTERNS = [
    dict(dots=[(250, 362, 16)], brows=[(170, 120, 30), (330, 120, 30)]),
    dict(dots=[(222, 350, 12), (278, 350, 12)], brows=[(200, 110, 22), (300, 110, 22)]),
    dict(stripe=True, brows=[(250, 112, 34)]),
    dict(dots=[], brows=[(160, 130, 24), (250, 105, 20), (340, 130, 24)]),
    dict(dots=[(250, 335, 10), (220, 372, 10), (280, 372, 10)], brows=[]),
]

def wasp_face(pen, pat=0, blink=False):      # canvas 500x520, head-on
    P = FACE_PATTERNS[pat]
    pen.line([(215, 140), (190, 70), (140, 26)], AMBER, 11, amp=1.0)
    pen.line([(285, 140), (310, 70), (360, 26)], AMBER, 11, amp=1.0)
    pen.dot(140, 26, 10, BROWN_D); pen.dot(360, 26, 10, BROWN_D)
    head = [(250, 480), (120, 400), (66, 260), (100, 130), (250, 82), (400, 130), (434, 260), (380, 400)]
    pen.poly(head, BROWN, w=6, amp=1.6)
    for (x, y, r) in P.get('brows', []):
        pen.ell(x, y + 40, r, r * 0.7, fill=YEL, w=3.5)
    shield = [(184, 300), (316, 300), (340, 372), (250, 440), (160, 372)]
    pen.poly(shield, YEL, w=4.5)
    for (x, y, r) in P.get('dots', []):
        pen.ell(x, y, r, r, fill=BROWN_D, w=3)
    if P.get('stripe'):
        pen.poly([(240, 304), (260, 304), (262, 420), (238, 420)], BROWN_D, w=3)
    for sgn in (-1, 1):
        ex = 250 + sgn * 128
        if blink:
            pen.ell(ex, 250, 64, 104, rot=-sgn * 12, fill=BROWN, w=5)
            pen.line([(ex - 46, 250), (ex, 276), (ex + 46, 250)], OUT, 6)
        else:
            pen.ell(ex, 250, 64, 104, rot=-sgn * 12, fill=EYE, w=5)
            pen.dot(ex - sgn * 12 - 10, 205, 17, (255, 255, 255))
            pen.dot(ex - sgn * 4 + 12, 248, 7, (255, 255, 255))
    pen.poly([(206, 438), (240, 448), (248, 478), (222, 470)], AMBER, w=4)
    pen.poly([(294, 438), (260, 448), (252, 478), (278, 470)], AMBER, w=4)
    pen.dot(150, 380, 14, (214, 130, 120)); pen.dot(350, 380, 14, (214, 130, 120))

def wasp_side(pen):           # canvas 460x340, facing right
    pen.ell(250, 110, 120, 44, rot=-18, fill=(214, 226, 238, 170), w=3)
    pen.ell(220, 120, 100, 36, rot=-30, fill=(214, 226, 238, 170), w=3)
    for x0, x1 in [(250, 230), (275, 290), (295, 340)]:
        pen.line([(x0, 190), (x0 - 10, 250), (x1, 320)], AMBER, 6)
    pen.ell(130, 200, 112, 62, rot=12, fill=BROWN, w=5)
    for k, x in enumerate((90, 135, 180)):
        pen.poly(xform([(-10, -56), (12, -58), (14, 58), (-12, 56)], x, 200 + (x - 130) * 0.2, rot=12), YEL, w=3, amp=0.6)
    pen.ell(262, 180, 56, 48, fill=BROWN, w=5)
    pen.ell(346, 166, 46, 48, fill=BROWN, w=5)
    pen.ell(368, 180, 20, 26, fill=YEL, w=3)
    pen.ell(340, 150, 18, 28, rot=10, fill=EYE, w=3); pen.dot(334, 140, 6, (255, 255, 255))
    pen.line([(352, 122), (380, 70), (420, 50)], AMBER, 6)

def nest(pen):                # canvas 520x480, papery comb seen from below
    pen.line([(260, 0), (262, 120)], (112, 80, 56), 12)
    pen.ell(260, 270, 214, 160, fill=COMB, w=5, amp=2)
    rng = random.Random(9)
    for r in range(-5, 6):
        for c in range(-6, 7):
            x = 260 + c * 34 + (17 if r % 2 else 0); y = 270 + r * 29
            if ((x - 260) / 190) ** 2 + ((y - 270) / 138) ** 2 > 1: continue
            hexp = [(x + 15 * math.cos(math.pi / 3 * i + math.pi / 6), y + 15 * math.sin(math.pi / 3 * i + math.pi / 6)) for i in range(6)]
            pen.poly(hexp, (236, 232, 222) if rng.random() < 0.2 else (178, 172, 160), outline=COMB_D, w=2.5, amp=0.4)

def pocket(pen):              # canvas 300x260, the front of a denim pocket
    shape = [(20, 40), (280, 40), (272, 190), (150, 246), (28, 190)]
    pen.poly(shape, DENIM, w=5)
    pen.line([(20, 66), (280, 66)], DENIM_D, 4, amp=0.5)
    inner = [(42, 84), (258, 84), (252, 180), (150, 224), (48, 180), (42, 84)]
    for i in range(len(inner) - 1):
        (x0, y0), (x1, y1) = inner[i], inner[i + 1]
        n = int(math.hypot(x1 - x0, y1 - y0) / 18)
        for k in range(0, n, 2):
            pen.line([(lerp(x0, x1, k / n), lerp(y0, y1, k / n)), (lerp(x0, x1, (k + 1) / n), lerp(y0, y1, (k + 1) / n))], STITCH, 3.5, amp=0.2)
    pen.dot(40, 54, 7, (200, 170, 110)); pen.dot(260, 54, 7, (200, 170, 110))

def beetle(pen):              # canvas 240x220
    for s in (-1, 1):
        for y in (90, 130, 165):
            pen.line([(120 + s * 50, y), (120 + s * 95, y + 20)], OUT, 6)
    pen.ell(120, 130, 70, 80, fill=(96, 130, 84), w=5)
    pen.line([(120, 60), (120, 208)], OUT, 4)
    pen.ell(120, 52, 34, 26, fill=(60, 70, 60), w=4)
    pen.dot(106, 46, 6, PAPER); pen.dot(134, 46, 6, PAPER)

def fly(pen):                 # canvas 240x220
    pen.ell(70, 90, 56, 30, rot=-25, fill=(220, 232, 242), w=3)
    pen.ell(170, 90, 56, 30, rot=25, fill=(220, 232, 242), w=3)
    pen.ell(120, 140, 40, 56, fill=(96, 98, 108), w=5)
    pen.ell(120, 80, 36, 30, fill=(110, 112, 120), w=4)
    pen.ell(96, 74, 16, 18, fill=(196, 70, 60), w=3); pen.ell(144, 74, 16, 18, fill=(196, 70, 60), w=3)

def brain(pen):               # canvas 380x280, a cute two-lobed insect brain
    pen.ell(120, 140, 104, 92, fill=PINK, w=5)
    pen.ell(260, 140, 104, 92, fill=PINK, w=5)
    pen.ell(190, 170, 60, 60, fill=PINK, outline=None, amp=0.5)
    for cx in (120, 260):
        pen.line([(cx - 60, 110), (cx - 30, 90), (cx, 118), (cx + 30, 92), (cx + 56, 118)], (196, 134, 148), 5)
        pen.line([(cx - 50, 170), (cx - 16, 150), (cx + 14, 178), (cx + 48, 156)], (196, 134, 148), 5)
    pen.line([(190, 60), (190, 220)], (196, 134, 148), 4)

def rice(pen):                # canvas 220x120
    pen.ell(110, 60, 96, 40, rot=-8, fill=RICE, w=5)
    pen.line([(40, 58), (170, 46)], (226, 220, 200), 4)

def rosette(pen):             # canvas 320x420
    pen.poly([(110, 220), (160, 240), (130, 410), (100, 370), (64, 396)], (196, 84, 80), w=4)
    pen.poly([(210, 220), (160, 240), (190, 410), (220, 370), (256, 396)], (196, 84, 80), w=4)
    pts = []
    for i in range(36):
        a = 2 * math.pi * i / 36
        r = 140 if i % 2 == 0 else 120
        pts.append((160 + r * math.cos(a), 160 + r * math.sin(a)))
    pen.poly(pts, GOLD, w=5)
    pen.ell(160, 160, 92, 92, fill=(250, 214, 110), w=4)
    pen.text((160, 165), '1st', 92, (120, 74, 30))

def face_sprites(pat):
    return [make_sprite(500, 520, lambda p: wasp_face(p, pat), seed=s) for s in (1, 2, 3)]
FACES = [face_sprites(k) for k in range(5)]
BLINK = [make_sprite(500, 520, lambda p: wasp_face(p, 0, True), seed=s) for s in (1, 2, 3)]
WINK3 = make_sprite(500, 520, lambda p: wasp_face(p, 3, True), seed=2)
SIDE = [make_sprite(460, 340, wasp_side, seed=s) for s in (1, 2, 3)]
NEST = [make_sprite(520, 480, nest, seed=s) for s in (1, 2, 3)]
POCKET = [make_sprite(300, 260, pocket, seed=s) for s in (1, 2, 3)]
BEETLE = make_sprite(240, 220, beetle, seed=5)
FLY = make_sprite(240, 220, fly, seed=6)
BRAIN = [make_sprite(380, 280, brain, seed=s) for s in (1, 2, 3)]
RICEG = make_sprite(220, 120, rice, seed=7)
ROSETTE = make_sprite(320, 420, rosette, seed=8)
FUZZ_S = fuzz_sprites('happy')
FUZZ_W = fuzz_sprites('shock')

def overlay(img, text, u, y=270, size=104):
    if u <= 0.02: return
    ImageDraw.Draw(img).text((540, y), text, font=font(FONT_CAP, int(size * u)), fill=HL,
                             anchor='mm', stroke_width=11, stroke_fill=OUT)

def screen(img, cx, cy, w, h, content, scale=0.5):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - w / 2 - 22, cy - h / 2 - 22, cx + w / 2 + 22, cy + h / 2 + 22], 26, fill=(60, 58, 70), outline=OUT, width=7)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 12, fill=(236, 232, 214))
    d.rectangle([cx - 20, cy + h / 2 + 22, cx + 20, cy + h / 2 + 70], fill=(60, 58, 70), outline=OUT, width=5)
    if content is not None:
        paste(img, content, cx, cy, scale)

# scene starts: hook | lineup | lab | brain (lines 3-4) | first in insects | loop back
B = [0, starts[1] - 0.12, starts[2] - 0.12, starts[3] - 0.12, starts[5] - 0.12, starts[6] - 0.12, DUR]

FACE_X, FACE_Y, FACE_S = 500, 960, 1.08
NEST_X, NEST_Y = 250, 640
POCK_X, POCK_Y = 900, 1040

def pose(p):
    """wasp, nest and Fuzz by loop phase p (0 at the first and last frame)"""
    return (FACE_X, FACE_Y + 10 * math.sin(p * 2.1), 2.0 * math.sin(p * 1.6),
            1.6 * math.sin(p * 1.3), 7 * math.sin(p * 3.2))

def garden_base(img, frame, p):
    _, _, _, nr, fb = pose(p)
    paste(img, NEST[boil(frame)], NEST_X, NEST_Y, 0.95, rot=nr)
    paste(img, FUZZ_S[boil(frame, off=1)], POCK_X, POCK_Y - 70 + fb, 0.62)
    paste(img, POCKET[boil(frame, off=2)], POCK_X, POCK_Y + 40, 0.85)

T_BLINK = 1.25

def s1(tl, frame, sd):
    img = GARDEN.copy()
    garden_base(img, frame, tl)
    x, y, r, _, _ = pose(tl)
    spr = BLINK if T_BLINK <= tl < T_BLINK + 0.16 else FACES[0]
    paste(img, spr[boil(frame)], x, y, FACE_S, rot=r)
    t_cells = starts[0] + 2.0
    g = math.sin(math.pi * seg(tl, t_cells, t_cells + 1.2))
    if g > 0:
        glow(img, x, y - 260, 130, (255, 236, 150), 0.7 * g)
        sparkle(img, x - 60, y - 300, 26 * g); sparkle(img, x + 70, y - 280, 20 * g)
    overlay(img, 'WASPS KNOW FACES', ease_back(seg(tl, 0.05, 0.35), 2.0), size=96)
    return img

LINE_X = [140, 340, 540, 740, 940]
def s2(tl, frame, sd):
    img = LINEUP.copy()
    d = ImageDraw.Draw(img)
    for k, x in enumerate(LINE_X):
        u = seg(tl, 0.1 + k * 0.2, 0.55 + k * 0.2)
        if u <= 0: continue
        xx = lerp(W + 200, x, ease_out(u))
        spr = WINK3 if (k == 3 and 1.7 <= tl < 1.95) else FACES[k][boil(frame, off=k)]
        paste(img, spr, xx, 900 + 8 * math.sin(tl * 3 + k), 0.39, rot=3 * math.sin(tl * 2 + k))
        d.rounded_rectangle([xx - 44, 1060, xx + 44, 1120], 10, fill=(40, 36, 48), outline=OUT, width=4)
        d.text((xx, 1090), str(k + 1), font=font(FONT_CAP, 46), fill=PAPER, anchor='mm')
    overlay(img, 'ALL DIFFERENT', ease_back(seg(tl, 0.3, 0.6), 2.0), size=104)
    return img

def s3(tl, frame, sd):
    img = LAB.copy()
    cam = lerp(1.0, 1.06, ease(seg(tl, 0, sd)))
    seq = [FACES[1][0], BEETLE, FACES[4][0], FLY, FACES[2][0]]
    k = int(max(0, tl - 0.3) / 0.5) % len(seq)
    sc = 0.9 if seq[k] in (BEETLE, FLY) else 0.4
    screen(img, 740, 860, 420, 320, seq[k] if tl > 0.3 else None, sc)
    paste(img, SIDE[boil(frame)], 330, 1110 + 6 * math.sin(tl * 4), 1.05)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([470, 1140, 600, 1230], 14, fill=(70, 74, 86), outline=OUT, width=5)
    d.line([(392, 1050), (430, 1120), (480, 1160)], fill=(60, 58, 70), width=5)
    for j in range(3):
        ph = (tl * 1.6 + j / 3) % 1.0
        r = 30 + 70 * ph
        a = int(255 * (1 - ph))
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).arc([535 - r, 1110 - r, 535 + r, 1110 + r], 220, 320, fill=(255, 226, 150, a), width=7)
        img.alpha_composite(lay)
    overlay(img, 'LISTENING IN', ease_back(seg(tl, 0.3, 0.6), 2.0), size=104)
    return camera(img, cam, 540, 960)

def s4(tl, frame, sd):
    img = LAB.copy()
    t3 = starts[3] - B[3]
    t4 = starts[4] - B[3]
    bu = ease_back(seg(tl, 0.05, 0.4), 1.6)
    ru = ease_back(seg(tl, 0.6, 0.9), 1.8)
    if tl < t4:
        shown = FACES[0][0] if tl > t3 + 1.6 else None
        lit = seg(tl, t3 + 2.2, t3 + 2.5)
    elif tl < t4 + 0.45:
        shown, lit = BEETLE, 0
    elif tl < t4 + 0.95:
        shown, lit = FLY, 0
    else:
        shown, lit = FACES[3][0], seg(tl, t4 + 0.95, t4 + 1.15)
    sc = 0.62 if shown in (BEETLE, FLY) else 0.28
    screen(img, 790, 640, 260, 200, shown, sc)
    bx, by = 380, 1000
    if lit > 0:
        glow(img, bx, by, 300, (255, 230, 130), 0.8 * lit)
    paste(img, BRAIN[boil(frame)], bx, by + 6 * math.sin(tl * 3), 1.1 * bu)
    if lit > 0:
        for k in range(5):
            a = k * 1.256 + tl * 1.5
            sparkle(img, bx + 230 * math.cos(a), by + 170 * math.sin(a), 26 * lit * (0.7 + 0.3 * math.sin(tl * 9 + k)))
    paste(img, RICEG, 845, 1020, 1.6 * ru, rot=6 * math.sin(tl * 2))
    if ru > 0.5:
        dd = ImageDraw.Draw(img)
        for yy in (990, 1030):
            dd.rounded_rectangle([596, yy - 11, 652, yy + 11], 10, fill=PAPER, outline=OUT, width=5)
    if tl < t4:
        overlay(img, 'RICE-SIZED BRAIN', ease_back(seg(tl, 0.2, 0.5), 2.0), size=96)
    else:
        overlay(img, 'JUST WASPS', ease_back(seg(tl, t4 + 0.95, t4 + 1.25), 2.0), size=110)
    return img

def s5(tl, frame, sd):
    img = GARDEN.copy()
    d = ImageDraw.Draw(img)
    lay = Image.new('RGBA', (W, H), (40, 30, 50, 90))
    img.alpha_composite(lay)
    u = ease_back(seg(tl, 0.1, 0.5), 1.7)
    glow(img, 540, 820, 360, (255, 230, 160), 0.6 * seg(tl, 0.1, 0.5))
    paste(img, ROSETTE, 540, 860, 1.25 * u, rot=4 * math.sin(tl * 2.5))
    rng = random.Random(3)
    for k in range(9):
        x0 = rng.uniform(120, 960); y0 = rng.uniform(560, 1150); ph = rng.uniform(0, 1)
        sparkle(img, x0, y0, 24 * max(0, math.sin(math.pi * ((tl * 1.3 + ph) % 1.0))) * seg(tl, 0.3, 0.6))
    fu = ease_back(seg(tl, 0.7, 1.1), 1.8)
    hop = abs(math.sin(tl * 6)) * 40 * seg(tl, 1.1, 1.3)
    paste(img, (FUZZ_W if tl < 1.3 else FUZZ_S)[boil(frame)], 870, lerp(1500, 1090, fu) - hop, 0.7)
    overlay(img, 'FIRST IN INSECTS', ease_back(seg(tl, 0.2, 0.5), 2.0), size=96)
    return img

def s6(tl, frame, sd):
    img = GARDEN.copy()
    p = tl - sd
    garden_base(img, frame, p)
    x, y, r, _, _ = pose(p)
    u = ease_out(seg(tl, 0.0, 0.9))
    sw = ease(seg(tl, 0.7, 1.5))
    paste(img, SIDE[boil(frame)], lerp(-260, x, u), lerp(700, y, u), 1.3 * (1 - sw), alpha=1 - sw)
    if sw > 0.12:
        paste(img, FACES[0][boil(frame)], x, y, FACE_S, rot=r, sx=sw)
    return img

FNS = [s1, s2, s3, s4, s5, s6]
SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate(FNS)]
EP = Episode(NAME, SCENES, CHUNKS, DUR, NO_END_TAG, loop=True)

def audio_plan():
    import pf_audio as A
    sfx = [(A.rustle(0.45), DUR - 0.25, 0.45, 0.4), (A.flutter(0.7), 0.25, 0.35, -0.1),
           (A.pop(), T_BLINK, 0.25, 0), (A.sparkles(), starts[0] + 2.0, 0.3, 0)]
    sfx += [(A.whoosh(0.5), B[1] + 0.05, 0.45, 0.4)]
    sfx += [(A.tick(1400 + 90 * k, 0.05, 0.45), B[1] + 0.5 + k * 0.2, 0.3, 0.6 - k * 0.3) for k in range(5)]
    sfx += [(A.pop(), B[1] + 1.75, 0.3, 0.2)]
    sfx += [(A.tick(1800, 0.04, 0.4), B[2] + 0.3 + k * 0.5, 0.25, 0.3) for k in range(5)]
    sfx += [(A.chime(1568.0), B[2] + 0.5, 0.18, -0.2)]
    t4 = B[3] + starts[4] - B[3]
    sfx += [(A.pop(), B[3] + 0.1, 0.35, -0.2), (A.boing(), B[3] + 0.65, 0.35, 0.3),
            (A.chime(1046.5), starts[3] + 2.2, 0.3, 0),
            (A.thud(), t4 + 0.02, 0.35, 0.2), (A.thud(), t4 + 0.47, 0.35, 0.2),
            (A.chime(1318.5), t4 + 0.95, 0.4, 0), (A.sparkles(), t4 + 1.0, 0.35, 0)]
    sfx += [(A.pop(), B[4] + 0.15, 0.45, 0), (A.sparkles(9, 1.0), B[4] + 0.3, 0.35, 0), (A.boing(), B[4] + 0.75, 0.35, 0.3)]
    sfx += [(A.whoosh(0.8, False), B[5] - 0.05, 0.45, 0), (A.flutter(0.6), B[5] + 0.2, 0.3, -0.3)]
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
