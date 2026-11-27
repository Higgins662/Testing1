"""Ep 24 See-Through Bear, LOOP CUT with the updated hook (Polar bears aren't white...)."""
import sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from pf import *

NAME = 'ep24L'
STYLE = 'lofi'
lines, durs, starts, DUR = timeline(NAME, first=0.15, gap=0.3, gaps={0: 0.35, 2: 0.35}, tail=0.42)
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={0: ["WHITE.", 'BLACK.'], 1: ['CLEAR', 'HOLLOW.'], 2: ['ALGAE', 'GREEN.'],
                                                     3: ['WHITE'], 4: ['BLACK', 'HEAT.'], 5: ['SEE-THROUGH'], 6: ['REMEMBER:']})
NO_END_TAG = DUR + 99

def overlay(img, text, u, y=270, size=104):
    if u <= 0.02: return
    ImageDraw.Draw(img).text((540, y), text, font=font(FONT_CAP, int(size * u)), fill=HL,
                             anchor='mm', stroke_width=11, stroke_fill=OUT)

# ------------------------------------------------------------ bear
FUR = (242, 240, 232)
FUR_SH = (206, 214, 226)
SKIN = (40, 38, 50)

def bear_shapes():
    body = ellpts(300, 385, 170, 158)
    head = ellpts(322, 205, 112, 96)
    earL = ellpts(238, 128, 30, 28)
    earR = ellpts(398, 122, 30, 28)
    armL = capsule(175, 320, 160, 455, 42)
    feetL = ellpts(215, 525, 66, 34)
    feetR = ellpts(385, 528, 66, 34)
    return [earL, earR, body, armL, feetL, feetR, head]

def draw_bear(pen, black=False, blush=False, wave_arm=False):
    fill = SKIN if black else FUR
    line = (90, 92, 110) if black else OUT
    pen.silhouette(bear_shapes(), fill, outline=line, w=4.5, amp=1.4)
    if not black:
        for pts in ([(210, 300), (240, 290)], [(330, 330), (365, 340)], [(250, 430), (280, 445)], [(380, 410), (405, 395)]):
            pen.line(pts, FUR_SH, 4, amp=0.6)
    inner = (70, 66, 82) if black else (226, 214, 206)
    pen.ell(238, 128, 14, 13, fill=inner, outline=None, amp=0.3)
    pen.ell(398, 122, 14, 13, fill=inner, outline=None, amp=0.3)
    snout = (66, 62, 78) if black else (250, 246, 238)
    pen.ell(335, 245, 56, 40, fill=snout, outline=line, w=3.5, amp=0.8)
    pen.ell(335, 228, 19, 14, fill=(20, 18, 26) if not black else (12, 10, 16), outline=None, amp=0.4)
    pen.dot(330, 223, 4, (120, 120, 140))
    pen.line([(335, 242), (335, 258)], (30, 26, 36) if not black else (150, 150, 170), 3, amp=0.2)
    pen.line([(318, 262), (335, 258), (352, 262)], (30, 26, 36) if not black else (150, 150, 170), 3, amp=0.3)
    eye_col = (16, 14, 20) if not black else (236, 234, 228)
    for ex in (282, 376):
        pen.dot(ex, 185, 10, eye_col)
        pen.dot(ex + 3, 181, 3.5, (255, 255, 255) if not black else (40, 38, 50))
    if blush or not black:
        pen.dot(262, 228, 15, (238, 176, 180) if not black else (200, 110, 130))
        pen.dot(408, 224, 15, (238, 176, 180) if not black else (200, 110, 130))
    for fx in (190, 215, 240):
        pen.line([(fx, 548), (fx, 556)], (120, 120, 130), 3, amp=0.2)
    for fx in (360, 385, 410):
        pen.line([(fx, 551), (fx, 559)], (120, 120, 130), 3, amp=0.2)
    if not wave_arm:
        pen.poly(capsule(425, 320, 440, 455, 42), fill, outline=line, w=4.5, amp=1.2)

def draw_wave_arm(pen, black=False):
    fill = SKIN if black else FUR
    line = (90, 92, 110) if black else OUT
    pen.poly(capsule(150, 150, 150, 40, 42), fill, outline=line, w=4.5, amp=1.2)
    for fx in (132, 150, 168):
        pen.line([(fx, 6), (fx, 14)], (120, 120, 130), 3, amp=0.2)

# ------------------------------------------------------------ backgrounds
def build_arctic():
    img = bg_canvas([(0, (168, 190, 222)), (0.25, (196, 206, 230)), (0.47, (234, 228, 236)), (1, (234, 228, 236))],
                    glows=[(820, 520, 420, (255, 244, 220), 0.7)])
    def fn(pen):
        pen.poly([(-20, 900), (1100, 900), (1100, 1940), (-20, 1940)], (88, 132, 152), outline=None, amp=0)
        for y in range(920, 1900, 46):
            pen.line([(random.Random(y).uniform(0, 300), y), (random.Random(y + 1).uniform(500, 1080), y)], (110, 156, 176), 3, amp=1)
        for (x, w_, h_) in [(120, 140, 90), (860, 200, 120), (1000, 120, 70)]:
            pen.poly([(x - w_, 905), (x - w_ * 0.3, 905 - h_), (x + w_ * 0.2, 905 - h_ * 0.8), (x + w_, 905)], (214, 228, 238), w=3.5, amp=1.2)
        pen.poly([(-30, 1060), (120, 1010), (420, 1000), (760, 1012), (1110, 1050), (1110, 1310), (840, 1350),
                  (420, 1340), (80, 1330), (-30, 1300)], (232, 242, 248), w=4.5, amp=2.5)
        pen.poly([(-30, 1300), (80, 1330), (420, 1340), (840, 1350), (1110, 1310), (1110, 1370), (-30, 1360)],
                 (176, 204, 222), w=4, amp=2)
        for (x, y) in [(200, 1100), (640, 1150), (900, 1120), (450, 1250)]:
            pen.line([(x, y), (x + 70, y - 6)], (204, 222, 236), 4, amp=0.8)
    return make_sprite(W, H, fn, seed=4, base=img)

def build_calendar():
    def fn(pen):
        pen.poly([(92, 120), (108, 120), (112, 330), (88, 330)], (130, 96, 66), w=3.5)
        pen.poly(rrect(20, 20, 180, 190, 12), (250, 246, 236), w=4, amp=0.8)
        pen.poly([(20, 32), (32, 20), (168, 20), (180, 32), (180, 70), (20, 70)], (200, 70, 64), w=4, amp=0.6)
        pen.text((100, 46), 'NOV', 34, (252, 248, 240))
        pen.text((100, 130), '2026', 46, (40, 34, 44))
        for x in (55, 145):
            pen.dot(x, 20, 7, (90, 90, 100))
    return make_sprite(200, 340, fn, seed=9)

def build_lab_bg():
    img = bg_canvas([(0, (46, 52, 74)), (0.5, (70, 76, 102)), (1, (40, 44, 62))], glows=[(540, 780, 700, (110, 120, 150), 0.6)])
    def fn(pen):
        pen.ell(540, 780, 420, 420, fill=(180, 140, 80), w=6, amp=1)
        pen.ell(540, 780, 385, 385, fill=(226, 236, 242), w=5, amp=0.8)
    return make_sprite(W, H, fn, seed=5, base=img)

def build_snow_bg():
    return make_sprite(W, H, lambda pen: pen.poly([(-20, 1080), (1100, 1070), (1100, 1940), (-20, 1940)], (206, 218, 232), w=4, amp=2),
                       seed=6, base=bg_canvas([(0, (196, 210, 232)), (0.6, (226, 232, 244)), (1, (214, 222, 236))],
                                              glows=[(540, 700, 600, (255, 250, 240), 0.5)]))

def draw_ice_cube(pen, rot=0):
    pts = xform([(-70, -70), (70, -70), (70, 70), (-70, 70)], 100, 100, 1, rot)
    pen.poly(pts, (196, 228, 240), outline=(84, 128, 160), w=4, amp=0.8)
    pen.poly(xform([(-50, -52), (30, -52), (-50, 20)], 100, 100, 1, rot), (236, 250, 255), outline=None, amp=0.4)
    pen.line(xform([(20, 40), (50, 10)], 100, 100, 1, rot), (250, 255, 255), 5, amp=0.3)

def draw_snow_pile(pen):
    pen.poly([(20, 330), (60, 220), (120, 150), (200, 110), (280, 140), (340, 210), (380, 330)], (252, 252, 255), w=4.5, amp=2.5)
    rng = random.Random(3)
    for i in range(26):
        x, y = rng.uniform(70, 330), rng.uniform(170, 320)
        pen.dot(x, y, rng.uniform(2, 4), (214, 226, 240))

def draw_coat(pen):
    pen.line([(150, 40), (150, 18), (164, 8), (176, 18)], (110, 110, 120), 5, amp=0.2)
    pen.line([(70, 70), (150, 40), (230, 70)], (110, 110, 120), 6, amp=0.2)
    coat = [(70, 70), (110, 60), (150, 90), (190, 60), (230, 70), (262, 160), (240, 170), (232, 330), (68, 330), (60, 170), (38, 160)]
    pen.poly(coat, None, outline=(150, 190, 220), w=5, amp=1.2)
    pen.line([(150, 90), (150, 330)], (180, 210, 232), 3, amp=0.8)

# ------------------------------------------------------------ assets
print('assets...', file=sys.stderr)
ARCTIC = build_arctic()
LAB = build_lab_bg()
SNOWBG = build_snow_bg()
BEAR_W = [make_sprite(600, 600, lambda p: draw_bear(p, False, wave_arm=True), seed=s) for s in (1, 2, 3)]
BEAR_W2 = [make_sprite(600, 600, lambda p: draw_bear(p, False), seed=s) for s in (1, 2, 3)]
BEAR_B = [make_sprite(600, 600, lambda p: draw_bear(p, True), seed=s) for s in (1, 2, 3)]
BEAR_BB = [make_sprite(600, 600, lambda p: draw_bear(p, True, blush=True, wave_arm=True), seed=s) for s in (1, 2, 3)]
ARM_W = [make_sprite(300, 300, lambda p: draw_wave_arm(p, False), seed=s) for s in (1, 2, 3)]
ARM_B = [make_sprite(300, 300, lambda p: draw_wave_arm(p, True), seed=s) for s in (1, 2, 3)]
ICE = [make_sprite(200, 200, lambda p, r=r: draw_ice_cube(p, r), seed=7) for r in (-8, 6, -3)]
SNOWPILE = make_sprite(400, 360, draw_snow_pile, seed=8)
COAT = make_sprite(300, 350, draw_coat, seed=10)
FUZZ_SHOCK = fuzz_sprites('shock')
SNOWDRIFT = make_sprite(420, 200, lambda p: p.poly([(10, 190), (40, 110), (120, 60), (220, 50), (320, 70), (400, 130), (415, 190)],
                                                     (240, 246, 252), w=4.5, amp=2), seed=11)

rng = random.Random(1)
FLAKES = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(3, 8), rng.uniform(40, 110), rng.uniform(0, 6)) for _ in range(70)]
def snow(img, t, alpha=1.0, count=70):
    d = ImageDraw.Draw(img)
    for i, (x, y, r, sp, ph) in enumerate(FLAKES[:count]):
        yy = (y + t * sp) % (H + 40) - 20
        xx = x + 18 * math.sin(t * 1.3 + ph)
        d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=(255, 255, 255, int(210 * alpha)))

def put_bear(img, kind, frame, cx, cy, scale=1.0, wave=None, arm_kind=None, alpha=1.0):
    paste(img, kind[boil(frame)], cx, cy, scale, alpha=alpha)
    if wave is not None:
        sh = (cx + (425 - 300) * scale, cy + (320 - 300) * scale)
        arm = (arm_kind or ARM_W)[boil(frame, off=1)]
        a = math.radians(wave)
        ox, oy = 0, -55 * scale
        paste(img, arm, sh[0] + (ox * math.cos(a) + oy * math.sin(a)) - 0, sh[1] + (-ox * math.sin(a) + oy * math.cos(a)) + 55 * scale - 55 * scale,
              scale, rot=wave)

# ------------------------------------------------------------ scenes
def tint_green(sprite):
    a = np.asarray(sprite).astype(np.float32).copy()
    a[..., 0] *= 0.62; a[..., 1] *= 0.95; a[..., 2] *= 0.55
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')
BEAR_G = [tint_green(b) for b in BEAR_W2]

B = [0] + [starts[i] - 0.15 for i in (1, 3, 4, 5, 6)] + [DUR]

def arctic_bear(tl, frame, wave_amt, z):
    img = ARCTIC.copy()
    bob = 6 * math.sin(tl * 3.2)
    wave = 25 * math.sin(tl * 9) * wave_amt
    put_bear(img, BEAR_W, frame, 600, 860 + bob, 1.0, wave=-wave - 15)
    snow(img, tl, 0.9)
    return img, z

def s1(tl, frame, sd):
    img, z = arctic_bear(tl, frame, seg(tl, 0.2, 0.5), lerp(1.0, 1.06, ease(tl / sd)))
    return camera(img, z, 560, 880)

def s2(tl, frame, sd):
    img = LAB.copy()
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    pop_ = ease_back(seg(tl, 0, 0.4))
    cx, cy, L = 540, 780, 330 * pop_
    a = math.radians(-50)
    x0, y0 = cx - L * math.cos(a), cy - L * math.sin(a)
    x1, y1 = cx + L * math.cos(a), cy + L * math.sin(a)
    tube = capsule(x0, y0, x1, y1, 78)
    d.polygon(tube, fill=(255, 255, 255, 120))
    d.line(tube + [tube[0]], fill=(120, 160, 196, 255), width=7)
    core = capsule(x0, y0, x1, y1, 28)
    hol = seg(tl, starts[1] - B[1] + 0.6, starts[1] - B[1] + 1.1)
    t_g = starts[2] - B[1] + 2.0
    g = seg(tl, t_g, t_g + 1.2)
    col = (int(lerp(196, 96, g)), int(lerp(214, 190, g)), int(lerp(230, 90, g)))
    d.polygon(core, fill=col + (int(255 * hol),))
    d.line(core + [core[0]], fill=(120, 160, 196, int(255 * hol)), width=4)
    d.line([(x0 + 40, y0 - 70), (x1 - 60, y1 - 40)], fill=(255, 255, 255, 200), width=8)
    img.alpha_composite(lay)
    if g <= 0:
        rays = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(rays)
        for k in range(6):
            ph = (tl * 0.9 + k / 6) % 1.0
            sx, sy = 200 + k * 60, 420
            ex, ey = 470 + k * 30, 700 + k * 25
            px, py = lerp(sx, ex, ph), lerp(sy, ey, ph)
            dr.line([(lerp(sx, ex, max(0, ph - 0.25)), lerp(sy, ey, max(0, ph - 0.25))), (px, py)], fill=(255, 214, 90, 220), width=8)
        img.alpha_composite(rays)
        for k in range(8):
            u = (tl * 0.7 + k / 8) % 1.0
            ang = k * 0.8
            sparkle(img, 540 + 260 * u * math.cos(ang), 780 + 260 * u * math.sin(ang), 26 * math.sin(math.pi * u))
    else:
        gb = ease_back(seg(tl, t_g + 0.6, t_g + 1.1), 1.8)
        if gb > 0:
            paste(img, BEAR_G[boil(frame)], 820, 1000, 0.6 * gb, rot=4 * math.sin(tl * 3))
    if g <= 0:
        overlay(img, 'CLEAR + HOLLOW', ease_back(seg(tl, 0.5, 0.8), 2.0), size=96)
    else:
        overlay(img, 'GREEN BEARS', ease_back(seg(tl, t_g, t_g + 0.3), 2.0))
    return img

def s3(tl, frame, sd):
    img = SNOWBG.copy()
    ui = ease_out(seg(tl, 0, 0.6))
    for k, (x, y) in enumerate([(200, 940), (330, 1000), (250, 1060)]):
        paste(img, ICE[k], lerp(-200, x, ui), y, 1.0)
    us = ease_back(seg(tl, 0.4, 1.0))
    paste(img, SNOWPILE, 800, 1010 - 140 * (1 - us) + 0, max(0.05, us))
    if tl > 0.5:
        for k in range(6):
            u = (tl * 0.8 + k / 6) % 1
            sparkle(img, 700 + 40 * k, 900 + 30 * math.sin(k), 18 * math.sin(math.pi * u))
    ue = ease_back(seg(tl, 1.3, 1.7))
    d = ImageDraw.Draw(img)
    if ue > 0:
        for dy in (-26, 26):
            w_ = 70 * ue
            d.rounded_rectangle([540 - w_, 980 + dy - 12, 540 + w_, 980 + dy + 12], 10, fill=(255, 211, 107), outline=OUT, width=6)
    d.text((300, 760), 'ICE', font=font(FONT_CAP, 64), fill=(252, 248, 240), anchor='mm', stroke_width=7, stroke_fill=OUT)
    d.text((800, 760), 'SNOW', font=font(FONT_CAP, 64), fill=(252, 248, 240), anchor='mm', stroke_width=7, stroke_fill=OUT)
    overlay(img, 'LIKE SNOW', ease_back(seg(tl, 0.3, 0.6), 2.0))
    return img

def s4(tl, frame, sd):
    img = ARCTIC.copy()
    sc = 1.25; cx, cy = 540, 840
    scan = seg(tl, 0.2, 1.2)
    paste(img, BEAR_B[boil(frame)], cx, cy, sc)
    w = BEAR_W2[boil(frame)].resize((int(600 * sc), int(600 * sc)), Image.BICUBIC)
    arr = np.asarray(w).copy()
    yline = int(arr.shape[0] * scan)
    a = arr[..., 3].astype(np.float32)
    a[:yline] *= 0.18
    arr[..., 3] = a.astype(np.uint8)
    paste(img, Image.fromarray(arr, 'RGBA'), cx, cy, 1.0)
    if 0 < scan < 1:
        d = ImageDraw.Draw(img)
        y = cy - 300 * sc + yline
        d.rectangle([cx - 380, y - 3, cx + 380, y + 3], fill=(120, 220, 255))
        glow(img, cx, y, 300, (140, 220, 255), 0.35)
    t_sun = starts[3] - B[3] + 1.2
    if tl > t_sun:
        su = seg(tl, t_sun, t_sun + 0.4)
        glow(img, 930, 330, 200, (255, 226, 140), 0.9 * su)
        d = ImageDraw.Draw(img)
        d.ellipse([870, 270, 990, 390], fill=(255, 214, 100))
        for k in range(5):
            ph = (tl * 1.2 + k / 5) % 1
            sx, sy = 900, 360
            ex, ey = 600 + k * 30, 760 + k * 20
            px, py = lerp(sx, ex, ph), lerp(sy, ey, ph)
            d.line([(lerp(sx, ex, max(0, ph - 0.2)), lerp(sy, ey, max(0, ph - 0.2))), (px, py)], fill=(255, 214, 90), width=9)
        glow(img, 560, 760, 220, (255, 170, 90), 0.25 * su)
    snow(img, tl, 0.6, 40)
    overlay(img, 'BLACK SKIN', ease_back(seg(tl, 0.3, 0.6), 2.0))
    return img

def s5(tl, frame, sd):
    img = ARCTIC.copy()
    sc = 1.05
    put_bear(img, BEAR_BB, frame, 470, 850, sc, wave=-35 + 4 * math.sin(tl * 3), arm_kind=ARM_B)
    paste(img, BEAR_W2[boil(frame)], 470, 850, sc, alpha=0.14)
    hang = ease_back(seg(tl, 0.2, 0.7))
    paste(img, COAT, 760, 600 + 60 * (1 - hang), max(0.05, hang), rot=6 * math.sin(tl * 2.2))
    for k in range(4):
        u = (tl * 0.9 + k / 4) % 1
        sparkle(img, 700 + 50 * k, 560 + 80 * (k % 2), 16 * math.sin(math.pi * u))
    t_f = starts[4] - B[4] + 1.4
    if tl > t_f - 0.1:
        u = seg(tl, t_f - 0.1, t_f + 0.35)
        fy = lerp(1330, 1120, ease_back(u, 2.4))
        paste(img, FUZZ_SHOCK[boil(frame)], 900, fy, 0.75, rot=3 * math.sin(tl * 10))
    paste(img, SNOWDRIFT, 900, 1235)
    snow(img, tl, 0.7, 50)
    overlay(img, 'SEE-THROUGH COAT', ease_back(seg(tl, 1.2, 1.5), 2.0), size=96)
    return img

def s6(tl, frame, sd):
    p = tl - sd                      # 0 at the last frame = frame 0 of s1
    img, _ = arctic_bear(p, frame, seg(-p, 0.1, 0.5), 1.0)
    return camera(img, lerp(1.06, 1.0, ease(seg(tl, 0, sd))), 560, 880)

SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate([s1, s2, s3, s4, s5, s6])]
EP = Episode(NAME, SCENES, CHUNKS, DUR, NO_END_TAG, loop=True, hook="POLAR BEARS AREN'T WHITE")

def audio_plan():
    import pf_audio as A
    sfx = [(A.wind(DUR), 0.0, 0.35, 0), (A.pop(), starts[0] + 1.25, 0.4, 0)]
    sfx += [(A.whoosh(0.45), B[1] - 0.15, 0.6, 0), (A.sparkles(8, 1.2, 2600), B[1] + 0.5, 0.6, 0.2),
            (A.slurp(), starts[2] + 2.0, 0.4, 0.2), (A.boing(), starts[2] + 2.6, 0.45, 0.3)]
    sfx += [(A.whoosh(0.4), B[2] - 0.15, 0.6, 0), (A.tick(1800, 0.07, 0.5), B[2] + 0.3, 0.8, -0.4),
            (A.tick(1600, 0.07, 0.5), B[2] + 0.45, 0.8, -0.3), (A.pop(), B[2] + 1.0, 0.5, 0.4), (A.pop(), B[2] + 1.5, 0.6, 0)]
    sfx += [(A.whoosh(1.1, True), B[3] + 0.2, 0.6, 0), (A.chime(784.0), starts[3] + 1.1, 0.4, 0.3)]
    sfx += [(A.boing(), B[4] + 0.3, 0.5, 0.3), (A.pop(), starts[4] + 1.35, 0.7, 0.4), (A.rustle(0.3), starts[4] + 1.3, 0.6, 0.4)]
    sfx += [(A.whoosh(0.8, False), B[5] - 0.05, 0.45, 0)]
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
