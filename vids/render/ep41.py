"""Ep 41 Starling Waves (loop cut): starlings can't outfly a falcon, so the flock makes waves that outrun the birds."""
import sys, math, random
from PIL import Image, ImageDraw
from pf import *

NAME = 'ep41'
STYLE = 'folk'
lines, durs, starts, DUR = timeline(NAME, first=0.15, gap=0.28, gaps={0: 0.32}, tail=0.42)
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={})
NO_END_TAG = DUR + 99

DENIM = (82, 112, 160)
DENIM_D = (62, 88, 132)
STITCH = (232, 164, 84)
BIRD = (40, 34, 52)
BIRD_L = (92, 84, 110)
SLATE = (96, 110, 132)
SLATE_D = (64, 74, 94)
CREAM = (246, 236, 214)
YEL = (246, 196, 60)

def overlay(img, text, u, y=270, size=104):
    if u <= 0.02: return
    ImageDraw.Draw(img).text((540, y), text, font=font(FONT_CAP, int(size * u)), fill=HL,
                             anchor='mm', stroke_width=11, stroke_fill=OUT)

# ------------------------------------------------------------ backgrounds
SKY_STOPS = [(0, (92, 86, 140)), (0.38, (196, 120, 128)), (0.62, (246, 170, 108)), (0.8, (252, 208, 140)), (1, (236, 186, 128))]

def _fence(img):
    d = ImageDraw.Draw(img)
    d.polygon([(0, 1060), (260, 1020), (620, 1050), (1080, 1000), (1080, H), (0, H)], fill=(84, 70, 96))   # far hills
    d.rectangle([0, 1180, W, H], fill=(70, 60, 70))
    d.line([(0, 1180), (W, 1180)], fill=OUT, width=6)
    for y in (1095, 1150):                                                    # rails
        d.rectangle([0, y, W, y + 16], fill=(58, 46, 52))
    for x in range(60, W, 230):                                               # posts
        d.rectangle([x, 1040, x + 30, 1200], fill=(52, 40, 46), outline=OUT, width=4)
    return img

SUNSET = _fence(downsample(bg_canvas(SKY_STOPS, glows=[(760, 980, 520, (255, 236, 180), 0.7)]), W, H))
SKY2 = downsample(bg_canvas(SKY_STOPS, glows=[(300, 900, 600, (255, 236, 180), 0.6)]), W, H)
CLOSE = downsample(bg_canvas([(0, (240, 176, 120)), (1, (196, 120, 128))], glows=[(540, 860, 620, (255, 226, 170), 0.6)]), W, H)

# ------------------------------------------------------------ sprites
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
    pen.dot(40, 54, 7, (200, 170, 110)); pen.dot(260, 54, 7, (200, 170, 110))

def falcon_top(pen):          # canvas 520x300, gliding seen from below/above, wings swept
    pen.poly([(260, 120), (40, 70), (10, 92), (150, 150), (240, 170)], SLATE, w=5)        # left wing
    pen.poly([(260, 120), (480, 70), (510, 92), (370, 150), (280, 170)], SLATE, w=5)      # right wing
    for k in range(4):
        pen.line([(40 + k * 28, 84 + k * 6), (60 + k * 30, 100 + k * 10)], SLATE_D, 3, amp=0.3)
        pen.line([(480 - k * 28, 84 + k * 6), (460 - k * 30, 100 + k * 10)], SLATE_D, 3, amp=0.3)
    pen.poly([(240, 160), (280, 160), (296, 270), (224, 270)], SLATE_D, w=5)              # tail
    pen.ell(260, 140, 40, 66, fill=CREAM, w=5)                                             # body
    for k in range(5):
        pen.line([(244, 120 + k * 14), (276, 120 + k * 14)], (150, 140, 130), 2.5, amp=0.4)
    pen.ell(260, 74, 32, 30, fill=SLATE_D, w=5)                                            # head
    pen.poly([(252, 46), (268, 46), (260, 30)], YEL, w=3)                                  # beak tip
    pen.dot(248, 70, 7, (14, 14, 20)); pen.dot(272, 70, 7, (14, 14, 20))

def falcon_head(pen):         # canvas 700x640, big profile close-up facing right
    pen.poly([(150, 380), (420, 380), (470, 640), (90, 640)], SLATE, w=6)                  # neck
    pen.poly([(300, 470), (440, 430), (470, 640), (280, 640)], CREAM, w=5)                 # throat
    pen.ell(330, 290, 230, 190, fill=SLATE, w=7)                                           # head
    pen.ell(300, 200, 200, 110, fill=SLATE_D, outline=None, amp=1.5)                       # dark hood
    pen.ell(420, 380, 130, 90, fill=CREAM, w=5)                                            # cheek
    pen.poly([(415, 310), (470, 310), (452, 470), (398, 474)], (36, 40, 54), w=5)          # moustache stripe
    pen.poly([(535, 250), (595, 268), (595, 330), (535, 330)], YEL, w=5)                    # cere
    pen.poly([(590, 262), (668, 296), (650, 368), (612, 352), (628, 318), (590, 322)], (60, 62, 76), w=5)  # hooked beak
    pen.ell(440, 260, 66, 66, fill=YEL, w=6)                                               # eye ring
    pen.ell(440, 260, 50, 50, fill=(250, 248, 240), w=4)                                   # eye white (pupil drawn live)

def starling(pen, up=True):   # canvas 360x240, side view flying right
    pen.ell(180, 130, 96, 46, fill=BIRD, w=5)
    pen.poly([(90, 120), (30, 100), (40, 150), (96, 146)], BIRD, w=5)                      # tail
    pen.ell(276, 112, 40, 36, fill=BIRD, w=5)                                              # head
    pen.poly([(310, 104), (356, 114), (310, 124)], YEL, w=4)                               # beak
    pen.dot(288, 104, 6, (250, 248, 240)); pen.dot(290, 104, 3, (14, 14, 20))
    rng = random.Random(4)
    for _ in range(26):
        pen.dot(rng.uniform(110, 260), rng.uniform(100, 165), rng.uniform(2.5, 4.5), CREAM)
    if up:
        pen.poly([(150, 110), (230, 108), (170, 10), (120, 20)], (60, 56, 84), w=5)
    else:
        pen.poly([(150, 140), (230, 140), (180, 232), (130, 222)], (60, 56, 84), w=5)

def qmark(pen):               # canvas 160x220
    pen.text((80, 110), '?', 180, YEL, stroke=8, stroke_fill=OUT)

POCKET = [make_sprite(300, 260, pocket, seed=s) for s in (1, 2, 3)]
FALCON = [make_sprite(520, 300, falcon_top, seed=s) for s in (1, 2, 3)]
HEAD = [make_sprite(700, 640, falcon_head, seed=s) for s in (1, 2, 3)]
ST_UP = [make_sprite(360, 240, lambda p: starling(p, True), seed=s) for s in (1, 2, 3)]
ST_DN = [make_sprite(360, 240, lambda p: starling(p, False), seed=s) for s in (1, 2, 3)]
QM = make_sprite(160, 220, qmark, seed=2)
FUZZ_S = fuzz_sprites('happy')
FUZZ_W = fuzz_sprites('shock')

# ------------------------------------------------------------ the flock
rng = random.Random(11)
N_BIRDS = 900
SEEDS = []
while len(SEEDS) < N_BIRDS:
    u, v = rng.uniform(-1, 1), rng.uniform(-1, 1)
    if u * u + v * v <= 1:
        SEEDS.append((u, v, rng.uniform(0, 6.283), rng.uniform(0.7, 1.3)))

def flock_points(T, cx=540, cy=700, rx=400, ry=200):
    """bird positions at flock phase T (any real number, smooth and periodic-ish)"""
    pts = []
    for (u, v, ph, sp) in SEEDS:
        a = math.atan2(v, u)
        rr = math.hypot(u, v)
        bulge = 1 + 0.22 * math.sin(2 * a + T * 0.9) + 0.12 * math.sin(3 * a - T * 1.3)
        x = cx + rx * rr * math.cos(a) * bulge + 30 * math.sin(T * 0.7 + v * 2)
        y = cy + ry * rr * math.sin(a) * bulge + 40 * math.sin(T * 0.8 + u * 2.5) - 50 * u * math.sin(T * 0.5)
        x += 6 * math.sin(T * 3 * sp + ph); y += 5 * math.cos(T * 3.4 * sp + ph)
        pts.append((x, y))
    return pts

def draw_flock(img, T, dark_fn, scale=1.0, alpha=255):
    """dark_fn(x, y) -> 0..1: how strongly a bird is banking (dark band)"""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for (x, y) in flock_points(T):
        k = dark_fn(x, y)
        r = (3.2 + 3.4 * k) * scale
        c = tuple(int(lerp(a, b, k)) for a, b in zip(BIRD_L, BIRD))
        d.ellipse([x - r * 1.5, y - r * 0.7, x + r * 1.5, y + r * 0.7], fill=c + (alpha,))
    img.alpha_composite(lay)

BAND_V = 900            # px/s for the rolling band in the hook

def plane_band(T):
    """planar wave sweeping left->right, repeating: dark near the front"""
    front = (T * BAND_V + 560) % 1500 - 260
    return lambda x, y: max(0.0, 1 - abs((x + 0.35 * (y - 700)) - front) / 110)

def ring_band(ox, oy, t0, tl, speed=700, period=0.75):
    def f(x, y):
        dist = math.hypot(x - ox, y - oy)
        k = 0.0
        for n in range(4):
            age = tl - t0 - n * period
            if age <= 0: continue
            k = max(k, max(0.0, 1 - abs(dist - speed * age) / 90) * max(0, 1 - age / 2.2))
        return k
    return f

# ------------------------------------------------------------ shared hook frame
POCK_X, POCK_Y = 190, 1060

def pose(p):
    return 6 * math.sin(p * 3.1)

def hook_base(img, frame, T):
    draw_flock(img, T, plane_band(T))
    fb = pose(T)
    paste(img, FUZZ_S[boil(frame, off=1)], POCK_X, POCK_Y - 66 + fb, 0.55)
    paste(img, POCKET[boil(frame, off=2)], POCK_X, POCK_Y + 30, 0.72)

B = [0] + [starts[i] - 0.12 for i in (1, 2, 3, 4)] + [DUR]

def s1(tl, frame, sd):
    img = SUNSET.copy()
    hook_base(img, frame, tl)
    return img

def s2(tl, frame, sd):
    img = SKY2.copy()
    T = B[1] + tl
    hit = 1.0
    fx = lerp(1180, 760, ease_out(seg(tl, 0, hit)))
    fy = lerp(220, 560, ease_out(seg(tl, 0, hit)))
    draw_flock(img, T, ring_band(760, 600, hit - 0.1, tl))
    if tl > hit:
        fx += (tl - hit) * 220; fy -= (tl - hit) * 160
    paste(img, FALCON[boil(frame)], fx, fy, 0.85, rot=(135 if tl < hit else lerp(135, 40, ease(seg(tl, hit, hit + 0.6)))) + 4 * math.sin(tl * 2))
    overlay(img, 'RIPPLES', ease_back(seg(tl, 0.9, 1.2), 2.0))
    return img

def s3(tl, frame, sd):
    img = SKY2.copy()
    d = ImageDraw.Draw(img)
    for x in range(-40, W + 40, 60):                         # dotted race track
        d.ellipse([x + (-tl * 40) % 60, 1056, x + 14 + (-tl * 40) % 60, 1070], fill=(250, 236, 210))
    bx = lerp(260, 470, seg(tl, 0, sd))
    flap = (frame // 3) % 2 == 0
    paste(img, (ST_UP if flap else ST_DN)[boil(frame)], bx, 960 + 10 * math.sin(tl * 9), 0.9)
    # the band: a tall column of banking birds zooming past
    wx = lerp(-200, 1400, seg(tl, 0.5, 1.6)) if tl < 1.6 else lerp(-200, 1400, seg(tl, 1.9, 3.0))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    r2 = random.Random(5)
    for _ in range(260):
        x = wx + r2.gauss(0, 34); y = r2.uniform(420, 1000)
        rr = r2.uniform(4, 8)
        dl.ellipse([x - rr * 1.6, y - rr * 0.7, x + rr * 1.6, y + rr * 0.7], fill=BIRD + (255,))
    for k in range(5):                                       # speed lines behind it
        y = 480 + k * 110
        dl.line([(wx - 80, y), (wx - 260, y)], fill=(255, 244, 220, 200), width=6)
    img.alpha_composite(lay)
    overlay(img, 'OUTRUNS THE BIRDS', ease_back(seg(tl, 0.9, 1.2), 2.0), size=88)
    return img

def s4(tl, frame, sd):
    img = CLOSE.copy()
    # reflection of the flock streaming past behind the head
    draw_flock(img, B[3] + tl, plane_band(B[3] + tl * 1.6), scale=1.4, alpha=150)
    u = ease_back(seg(tl, 0, 0.4), 1.5)
    hx, hy, hs = 500, 820, 1.0 * max(0.05, u)
    paste(img, HEAD[boil(frame)], hx, hy, hs, rot=3 * math.sin(tl * 1.4))
    # live swirl pupil
    ex, ey = hx + (440 - 350) * hs, hy + (260 - 320) * hs
    d = ImageDraw.Draw(img)
    spin = tl * 6
    for k in range(60):
        a = spin + k * 0.32; r = 2 + k * 0.72 * hs
        x0, y0 = ex + r * math.cos(a), ey + r * math.sin(a)
        d.ellipse([x0 - 4, y0 - 4, x0 + 4, y0 + 4], fill=(20, 18, 28))
    qu = ease_back(seg(tl, 1.4, 1.8), 2.2)
    paste(img, QM, hx + 140, 430 + 8 * math.sin(tl * 5), 1.0 * qu, rot=10 * math.sin(tl * 3))
    overlay(img, 'TRICKS THE EYE', ease_back(seg(tl, 0.5, 0.8), 2.0))
    return img

def s5(tl, frame, sd):
    img = SUNSET.copy()
    p = tl - sd                                    # 0 at the final frame: matches frame 0
    hook_base(img, frame, p)
    # falcon veers off, empty-taloned, and is gone well before the loop point
    fu = seg(tl, 0.0, 2.2)
    if fu < 1:
        fx = lerp(620, 1300, ease_in(fu)); fy = lerp(560, 160, ease_in(fu))
        paste(img, FALCON[boil(frame)], fx, fy, 0.8, rot=-60)
    jump = hop_y(seg(tl, 0.6, 1.0)) + hop_y(seg(tl, 1.0, 1.35)) * 0.5
    if jump > 0:   # Fuzz bounces in the pocket
        paste(img, FUZZ_S[boil(frame, off=1)], POCK_X, POCK_Y - 66 + pose(p) - jump, 0.55)
        paste(img, POCKET[boil(frame, off=2)], POCK_X, POCK_Y + 30, 0.72)
    overlay(img, 'MISSED', ease_back(seg(tl, 0.3, 0.6), 2.0) * (1 - seg(tl, 2.6, 2.9)), size=120)
    return img

def hop_y(u):
    return 4 * 60 * u * (1 - u)

SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate([s1, s2, s3, s4, s5])]
EP = Episode(NAME, SCENES, CHUNKS, DUR, NO_END_TAG, loop=True, hook="THEY CAN'T OUTFLY A FALCON")

def audio_plan():
    import pf_audio as A
    sfx = [(A.wind(2.5) if hasattr(A, 'wind') else A.whoosh(1.2), 0.0, 0.25, 0),
           (A.flutter(), 0.4, 0.35, -0.3), (A.pop(), 0.7, 0.3, -0.6)]
    sfx += [(A.whoosh(0.8), B[1] + 0.1, 0.5, 0.4), (A.flutter(), B[1] + 1.0, 0.4, 0.2)]
    sfx += [(A.whoosh(0.5), B[2] + 0.45, 0.5, -0.2), (A.whoosh(0.5), B[2] + 1.85, 0.45, 0.2),
            (A.tick(1500, 0.05, 0.5), B[2] + 0.9, 0.25, 0)]
    sfx += [(A.boing(), B[3] + 1.4, 0.4, 0.3), (A.pop(), B[3] + 1.45, 0.35, 0.3)]
    sfx += [(A.whoosh(1.0, False), B[4] + 0.05, 0.5, 0.5), (A.chime(988), B[4] + 0.7, 0.3, -0.5),
            (A.flutter(), DUR - 0.6, 0.3, -0.3)]
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
