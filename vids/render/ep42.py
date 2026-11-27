"""Ep 42 Cat Smile (loop cut): a slow cat blink is a 'cat smile', and cats blink back (Humphrey et al. 2020)."""
import sys, math, random
from PIL import Image, ImageDraw
from pf import *

NAME = 'ep42'
STYLE = 'jazz'
lines, durs, starts, DUR = timeline(NAME, first=0.15, gap=0.34, tail=0.42)
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={})
NO_END_TAG = DUR + 99

GINGER = (236, 150, 74)
GINGER_D = (196, 108, 46)
CREAMY = (252, 232, 200)
LAV = (164, 140, 196)
LAV_D = (128, 104, 164)
DENIM = (82, 112, 160)
DENIM_D = (62, 88, 132)
STITCH = (232, 164, 84)
GREEN_EYE = (150, 196, 84)
NAVY = (52, 62, 104)
SKIN = (236, 190, 150)

def overlay(img, text, u, y=270, size=104):
    if u <= 0.02: return
    ImageDraw.Draw(img).text((540, y), text, font=font(FONT_CAP, int(size * u)), fill=HL,
                             anchor='mm', stroke_width=11, stroke_fill=OUT)

# ------------------------------------------------------------ backgrounds
def _room():
    img = downsample(bg_canvas([(0, (246, 222, 190)), (0.7, (236, 204, 170)), (1, (220, 186, 150))],
                               glows=[(300, 420, 520, (255, 240, 206), 0.6)]), W, H)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([640, 360, 960, 640], 16, fill=(230, 210, 230), outline=OUT, width=6)     # picture frame
    d.ellipse([720, 430, 880, 570], fill=(200, 176, 214), outline=OUT, width=4)                    # a yarn ball picture
    d.rectangle([0, 1180, W, H], fill=(170, 120, 90)); d.line([(0, 1180), (W, 1180)], fill=OUT, width=7)
    d.ellipse([140, 1220, 940, 1330], fill=(200, 150, 160), outline=OUT, width=5)                  # rug
    return img
ROOM = _room()
PLAIN = downsample(bg_canvas([(0, (250, 228, 196)), (1, (232, 196, 160))], glows=[(540, 800, 600, (255, 244, 220), 0.6)]), W, H)

def couch(pen):               # canvas 1000x520
    pen.poly(rrect(70, 20, 930, 300, 60), LAV, w=6)                    # back
    pen.poly(rrect(20, 160, 180, 470, 50), LAV_D, w=6)                 # left arm
    pen.poly(rrect(820, 160, 980, 470, 50), LAV_D, w=6)                # right arm
    pen.poly(rrect(160, 250, 500, 400, 30), (180, 156, 210), w=5)      # cushions
    pen.poly(rrect(500, 250, 840, 400, 30), (180, 156, 210), w=5)
    pen.poly(rrect(120, 380, 880, 470, 20), LAV_D, w=5)                # base
    for x in (150, 850):
        pen.poly(rrect(x - 18, 460, x + 18, 510, 6), (110, 80, 60), w=4)
COUCH = make_sprite(1000, 520, couch, seed=3)
COUCH_X, COUCH_Y = 540, 1000

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
POCKET = [make_sprite(300, 260, pocket, seed=s) for s in (1, 2, 3)]

def cat_body(pen):            # canvas 460x520, sitting ginger cat, front view, no eyes (drawn live)
    pen.ell(230, 380, 150, 130, fill=GINGER, w=6)                      # body
    pen.ell(230, 400, 80, 100, fill=CREAMY, outline=None, amp=0.8)     # chest
    for x in (170, 290):
        pen.ell(x, 500, 46, 24, fill=GINGER, w=5)                      # paws
        pen.line([(x - 8, 490), (x - 8, 512)], GINGER_D, 3)
        pen.line([(x + 8, 490), (x + 8, 512)], GINGER_D, 3)
    pen.poly([(110, 120), (130, 20), (200, 90)], GINGER, w=6)          # ears
    pen.poly([(350, 120), (330, 20), (260, 90)], GINGER, w=6)
    pen.poly([(130, 105), (138, 50), (178, 92)], (240, 170, 170), outline=None, amp=0.5)
    pen.poly([(330, 105), (322, 50), (282, 92)], (240, 170, 170), outline=None, amp=0.5)
    pen.ell(230, 170, 135, 112, fill=GINGER, w=6)                      # head
    for k, x in enumerate((190, 230, 270)):                            # forehead stripes
        pen.line([(x, 66 + abs(k - 1) * 6), (x + (k - 1) * 6, 108)], GINGER_D, 6)
    for s in (-1, 1):
        for k in range(2):
            pen.line([(230 + s * 150, 340 + k * 40), (230 + s * 110, 352 + k * 40)], GINGER_D, 6)
    pen.ell(230, 222, 56, 34, fill=CREAMY, outline=None, amp=0.6)       # muzzle
    pen.poly([(218, 206), (242, 206), (230, 220)], (226, 120, 130), w=3, amp=0.3)   # nose
    pen.line([(230, 220), (230, 230), (216, 240)], OUT, 3.5, amp=0.3)
    pen.line([(230, 230), (244, 240)], OUT, 3.5, amp=0.3)
    for s in (-1, 1):
        for k in range(3):
            pen.line([(230 + s * 60, 222 + k * 10), (230 + s * 130, 212 + k * 16)], (90, 70, 60), 2.5, amp=0.5)
CAT = [make_sprite(460, 520, cat_body, seed=s) for s in (1, 2, 3)]
EYE_DX, EYE_DY = 52, -100        # eye offsets from the sprite centre (460x520 -> centre 230,260; eyes at 178/282, 160)

def tail(pen):                # canvas 260x260, tail curling up from bottom-left pivot (40,220)
    pts = [(40 + 180 * math.sin(a) * 0.9, 220 - 160 * (1 - math.cos(a)) * 0.9) for a in [i * 0.12 for i in range(14)]]
    pen.line(pts, OUT, 40, amp=0.6)
    pen.line(pts, GINGER, 30, amp=0.6)
    pen.line(pts[-3:], GINGER_D, 30, amp=0.4)
TAIL = [make_sprite(260, 260, tail, seed=s) for s in (1, 2, 3)]

def draw_eyes(img, cx, cy, sc, o, color=GREEN_EYE):
    """cat eyes at sprite centre (cx, cy) and scale sc; o = openness 0 (closed) .. 1 (open)"""
    d = ImageDraw.Draw(img)
    for s in (-1, 1):
        ex, ey = cx + s * EYE_DX * sc, cy + EYE_DY * sc
        rx, ry = 30 * sc, 26 * sc * max(0.0, o)
        if o > 0.12:
            d.ellipse([ex - rx, ey - ry, ex + rx, ey + ry], fill=color, outline=OUT, width=max(2, int(5 * sc)))
            pw = 7 * sc
            d.ellipse([ex - pw, ey - ry * 0.85, ex + pw, ey + ry * 0.85], fill=(20, 20, 24))
            if o > 0.5:
                d.ellipse([ex + 6 * sc, ey - 12 * sc * o, ex + 14 * sc, ey - 4 * sc * o], fill=(255, 255, 255))
        # upper lid line: a gentle smile-curve when nearly closed
        pts = [(ex - rx + 2 * rx * i / 12, ey - ry * math.sin(math.pi * i / 12) * (1 if o > 0.12 else -0.0) + (8 * sc * math.sin(math.pi * i / 12) if o <= 0.12 else 0)) for i in range(13)]
        d.line(pts, fill=OUT, width=max(3, int(6 * sc)), joint='curve')

def human_eyes(pen):          # canvas 700x260, a big pair of friendly eyes with brows, no face
    for cx in (190, 510):
        pen.line([(cx - 100, 50), (cx, 26), (cx + 100, 50)], (90, 60, 40), 12)
EYEBROWS = make_sprite(700, 260, human_eyes, seed=2)

def draw_human_eyes(img, cx, cy, o):
    d = ImageDraw.Draw(img)
    for s in (-1, 1):
        ex = cx + s * 160
        rx, ry = 110, 64 * max(0.0, o)
        if o > 0.1:
            d.ellipse([ex - rx, cy - ry, ex + rx, cy + ry], fill=(252, 250, 244), outline=OUT, width=7)
            ir = min(48, ry)
            d.ellipse([ex - 48, cy - ir, ex + 48, cy + ir], fill=(110, 76, 50))
            d.ellipse([ex - 22, cy - min(22, ir), ex + 22, cy + min(22, ir)], fill=(20, 18, 24))
        pts = [(ex - rx + 2 * rx * i / 14, cy - ry * math.sin(math.pi * i / 14) + (10 * math.sin(math.pi * i / 14) if o <= 0.1 else 0)) for i in range(15)]
        d.line(pts, fill=OUT, width=8, joint='curve')

def sleeve(pen):              # canvas 700x300, striped sleeve from the right with an open palm (palm up)
    pen.poly([(300, 90), (700, 70), (700, 250), (300, 220)], (244, 236, 220), w=6)
    for k in range(5):
        x = 360 + k * 70
        pen.poly([(x, 86 - k * 2), (x + 34, 84 - k * 2), (x + 34, 236 + k), (x, 232 + k)], NAVY, outline=None, amp=0.4)
    pen.ell(220, 170, 110, 60, fill=SKIN, w=6)                         # flat open palm
    for k in range(4):
        pen.ell(110, 130 + k * 26, 50, 13, fill=SKIN, w=4.5)           # fingers pointing left, together
    pen.ell(250, 110, 40, 18, rot=-30, fill=SKIN, w=4.5)               # thumb
    pen.line([(180, 170), (260, 160)], (200, 150, 116), 3)
SLEEVE = [make_sprite(700, 300, sleeve, seed=s) for s in (1, 2, 3)]

def card(pen, label, kind):   # canvas 300x380
    pen.poly(rrect(14, 14, 286, 366, 28), (255, 250, 240), w=6)
    cx, cy = 150, 150
    if kind == 'open':
        pen.ell(cx, cy, 80, 52, fill=GREEN_EYE, w=6); pen.ell(cx, cy, 14, 44, fill=(20, 20, 24), outline=None)
    elif kind == 'squint':
        pen.ell(cx, cy, 80, 18, fill=GREEN_EYE, w=6); pen.line([(cx - 84, cy - 4), (cx, cy - 22), (cx + 84, cy - 4)], OUT, 7)
    else:
        pen.line([(cx - 84, cy - 6), (cx, cy + 22), (cx + 84, cy - 6)], OUT, 8)
        pen.text((cx, cy + 74), '2 sec', 40, (150, 120, 100))
    pen.text((150, 300), label, 58, NAVY)
CARDS = [make_sprite(300, 380, lambda p, l=l, k=k: card(p, l, k), seed=i + 1)
         for i, (l, k) in enumerate([('SQUINT', 'squint'), ('HOLD', 'closed'), ('OPEN', 'open')])]

def sniff(pen):               # canvas 120x80 little sniff puffs
    for k in range(3):
        pen.ell(20 + k * 38, 40 - 8 * math.sin(k), 14, 10, fill=(255, 255, 255), w=3)
SNIFF = make_sprite(120, 80, sniff, seed=5)

FUZZ_S = fuzz_sprites('happy')
FUZZ_W = fuzz_sprites('shock')

# ------------------------------------------------------------ cat helpers
CAT_X, CAT_Y, CAT_S = 470, 820, 0.95
POCK_X, POCK_Y = 900, 880

def pose(p):
    """tail angle, fuzz bob, cat breathing: p = 0 at frame 0 and at the last frame"""
    return 14 * math.sin(p * 2.4), 6 * math.sin(p * 3.0), 1 + 0.012 * math.sin(p * 2.0)

def draw_cat(img, frame, x, y, sc, o, p, rot=0.0):
    ta, _, br = pose(p)
    paste(img, TAIL[boil(frame)], x + 150 * sc, y + 150 * sc, sc, rot=ta)
    paste(img, CAT[boil(frame)], x, y, sc, rot=rot, sy=br)
    draw_eyes(img, x, y + (EYE_DY * (br - 1)) * sc, sc, o)

def couch_scene(img, frame, p, fuzz=True):
    paste(img, COUCH, COUCH_X, COUCH_Y, 1.0)
    if fuzz:
        _, fb, _ = pose(p)
        paste(img, FUZZ_S[boil(frame, off=1)], POCK_X, POCK_Y - 62 + fb, 0.5)
        paste(img, POCKET[boil(frame, off=2)], POCK_X, POCK_Y + 20, 0.62)

O0 = 0.55                      # eye openness at the loop point (mid-squint)

def hook_open(tl):
    if tl < 0.3: return O0
    if tl < 1.0: return lerp(O0, 0.05, ease(seg(tl, 0.3, 1.0)))
    if tl < 1.8: return 0.05
    return lerp(0.05, 1.0, ease(seg(tl, 1.8, 2.5)))

B = [0, starts[1] - 0.12, starts[3] - 0.12, starts[5] - 0.12, starts[6] - 0.12, DUR]

def s1(tl, frame, sd):
    img = ROOM.copy()
    couch_scene(img, frame, tl)
    draw_cat(img, frame, CAT_X, CAT_Y, CAT_S, hook_open(tl), tl)
    overlay(img, "IT'S A CAT SMILE", ease_back(seg(tl, 0.2, 0.5), 2.0), size=96)
    return img

def s2(tl, frame, sd):
    img = PLAIN.copy()
    t2 = starts[2] - B[1]
    # owner's eyes up top: slow blink, then hold open
    o_h = 1.0
    if 0.9 < tl < 2.8:
        o_h = 1 - math.sin(math.pi * seg(tl, 0.9, 2.8)) ** 0.6 * 0.95
    u = ease_back(seg(tl, 0, 0.4), 1.6)
    paste(img, EYEBROWS, 540, 470 - 70, u)
    if u > 0.9: draw_human_eyes(img, 540, 470, o_h)
    # the cat below copies, then a tally of blinks back
    o_c = 1.0
    if t2 + 0.2 < tl < t2 + 2.0:
        o_c = 1 - math.sin(math.pi * seg(tl, t2 + 0.2, t2 + 2.0)) ** 0.6 * 0.95
    draw_cat(img, frame, 540, 960, 0.8, o_c, tl)
    k = int(seg(tl, t2 + 0.2, t2 + 2.6) * 4)
    for j in range(k):
        sparkle(img, 300 + j * 160, 700, 26)
    overlay(img, 'BLINK BACK', ease_back(seg(tl, t2, t2 + 0.3), 2.0))
    return img

def s3(tl, frame, sd):
    img = ROOM.copy()
    couch_scene(img, frame, tl, fuzz=False)
    t4 = starts[4] - B[2]
    hand_u = ease_out(seg(tl, 0.1, 0.8))
    hx = lerp(1300, 860, hand_u)
    paste(img, SLEEVE[boil(frame)], hx, 1050, 0.9)
    # little eye icon above the hand: slow blink
    o_s = 1 - math.sin(math.pi * seg(tl, 0.7, 1.7)) ** 0.6 * 0.95 if tl < 1.7 else 1.0
    d = ImageDraw.Draw(img)
    ex, ey = hx - 80, 860
    d.ellipse([ex - 70, ey - 44 * max(o_s, 0.06), ex + 70, ey + 44 * max(o_s, 0.06)], fill=(252, 250, 244), outline=OUT, width=6)
    if o_s > 0.2:
        d.ellipse([ex - 22, ey - 22 * o_s, ex + 22, ey + 22 * o_s], fill=(110, 76, 50))
    # cat: blink back, hop down, pad over, sniff
    if tl < t4:
        o = 1 - math.sin(math.pi * seg(tl, 1.1, 1.9)) ** 0.6 * 0.95 if 1.1 < tl < 1.9 else 1.0
        draw_cat(img, frame, CAT_X, CAT_Y, CAT_S, o, tl)
    else:
        hu = seg(tl, t4, t4 + 0.6)
        wu = seg(tl, t4 + 0.6, t4 + 1.6)
        x = lerp(CAT_X, 480, hu) + lerp(0, 0, wu)
        y = lerp(CAT_Y, 1010, ease_in(hu)) - 4 * 120 * hu * (1 - hu)
        x = lerp(x, 520, ease(wu))
        sc = lerp(CAT_S, 0.82, hu)
        bob = 8 * abs(math.sin(tl * 9)) if 0 < wu < 1 else 0
        lean = -8 * ease(seg(tl, t4 + 1.6, t4 + 1.9))
        draw_cat(img, frame, x, y - bob, sc, 1.0, tl, rot=lean)
        if tl > t4 + 1.8:
            paste(img, SNIFF, x + 200, y - 30 + 6 * math.sin(tl * 12), 0.9, alpha=0.5 + 0.5 * abs(math.sin(tl * 6)))
    overlay(img, 'EVEN STRANGERS', ease_back(seg(tl, 0.3, 0.6), 2.0))
    return img

def s4(tl, frame, sd):
    img = PLAIN.copy()
    ts = [0.15, 0.75, 1.7]
    for i in range(3):
        u = ease_back(seg(tl, ts[i], ts[i] + 0.35), 1.8)
        if u <= 0: continue
        paste(img, CARDS[i], 220 + i * 320, 760 + 20 * (1 - u), 0.95 * u, rot=(i - 1) * -4)
    paste(img, FUZZ_S[boil(frame)], 540, 1150 - abs(8 * math.sin(tl * 6)), 0.75)
    return img

def s5(tl, frame, sd):
    img = ROOM.copy()
    p = tl - sd
    couch_scene(img, frame, p)
    ju = seg(tl, 0.0, 0.9)
    x = lerp(520, CAT_X, ease(ju))
    y = lerp(1010, CAT_Y, ease_out(ju)) - 4 * 160 * ju * (1 - ju)
    sc = lerp(0.82, CAT_S, ju)
    o = 1.0 if tl < sd - 1.3 else lerp(1.0, O0, ease(seg(tl, sd - 1.3, sd - 0.25)))
    draw_cat(img, frame, x, y, sc, o, p)
    return img

SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate([s1, s2, s3, s4, s5])]
EP = Episode(NAME, SCENES, CHUNKS, DUR, NO_END_TAG, loop=True)

def audio_plan():
    import pf_audio as A
    sfx = [(A.rustle(0.5), 0.1, 0.25, 0.4), (A.pop(), 0.5, 0.25, 0.6), (A.chime(784), 2.0, 0.25, 0)]
    sfx += [(A.tick(1200, 0.06, 0.5), B[1] + 0.9, 0.25, 0), (A.tick(1000, 0.06, 0.5), B[1] + 2.8, 0.2, 0)]
    sfx += [(A.chime(988 + 110 * j), starts[2] + 0.4 + j * 0.6, 0.22, -0.3 + 0.2 * j) for j in range(4)]
    t4 = starts[4]
    sfx += [(A.whoosh(0.5), B[2] + 0.1, 0.4, 0.5), (A.pop(), t4 + 0.05, 0.3, 0), (A.boing(), t4 + 0.6, 0.3, 0),
            (A.rustle(0.3), t4 + 1.9, 0.3, 0.3), (A.rustle(0.3), t4 + 2.2, 0.25, 0.3)]
    sfx += [(A.tick(1400 + 120 * i, 0.05, 0.5), B[3] + t, 0.3, -0.4 + 0.4 * i) for i, t in enumerate([0.15, 0.75, 1.7])]
    sfx += [(A.whoosh(0.5, False), B[4] - 0.05, 0.35, 0), (A.boing(), B[4] + 0.9, 0.3, 0)]
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
