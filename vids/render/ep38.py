"""Ep 38 Almost Blue Monday (loop cut): Cyber Monday started as a 2005 press release."""
import sys, math
from PIL import Image, ImageDraw
from pf import *

NAME = 'ep38'
STYLE = 'bossa'
lines, durs, starts, DUR = timeline(NAME, first=0.15, gap=0.24, gaps={0: 0.3, 4: 0.3}, tail=0.42)
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={0: ['HOLIDAY.', 'PRESS', 'RELEASE.'], 1: ['2005,'], 2: ['SLOW,', 'WORK.'],
                                                     3: ['BLACK', 'MONDAY?'], 4: ['BLUE', 'GREEN'], 5: ['ZERO', 'RESULTS.'], 6: ['REMEMBER:']})
NO_END_TAG = DUR + 99

# ------------------------------------------------------------ palette
PAPER = (250, 248, 240)
RED = (222, 74, 70)
BEIGE = (226, 216, 190)
BEIGE_D = (196, 184, 156)
SCREEN = (60, 120, 150)
WOOD = (176, 120, 78)
LINK = (50, 110, 230)
CASH = (60, 170, 90)

# ------------------------------------------------------------ backgrounds
def _desk(img, y=1240):
    d = ImageDraw.Draw(img)
    d.rectangle([0, y, W, H], fill=WOOD)
    d.line([(0, y), (W, y)], fill=OUT, width=7)
    for k in range(6):
        yy = y + 70 + k * 90
        d.line([(0, yy), (W, yy + 14)], fill=(160, 106, 68), width=3)
    return img
WALL = _desk(downsample(bg_canvas([(0, (246, 226, 196)), (0.65, (240, 214, 180)), (1, (226, 196, 160))],
                                  glows=[(300, 380, 520, (255, 246, 222), 0.55)]), W, H))
OFFICE = _desk(downsample(bg_canvas([(0, (200, 214, 224)), (0.65, (186, 200, 212)), (1, (170, 186, 200))],
                                    glows=[(760, 360, 520, (236, 244, 250), 0.5)]), W, H))

def _split():
    top = downsample(bg_canvas([(0, (150, 196, 232)), (1, (206, 228, 240))]), W, H // 2)
    bot = downsample(bg_canvas([(0, (196, 204, 214)), (1, (168, 178, 192))]), W, H - H // 2)
    img = Image.new('RGBA', (W, H)); img.paste(top, (0, 0)); img.paste(bot, (0, H // 2))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 820, W, H // 2], fill=(140, 190, 110))
    d.line([(0, 820), (W, 820)], fill=OUT, width=6)
    d.line([(0, H // 2), (W, H // 2)], fill=OUT, width=10)
    return img
SPLIT = _split()

def _board():
    img = OFFICE.copy()
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([70, 430, 1010, 1240], 26, fill=(198, 202, 210), outline=OUT, width=8)
    d.rounded_rectangle([100, 460, 980, 1210], 14, fill=(252, 252, 250), outline=(150, 156, 166), width=4)
    d.rectangle([380, 1210, 700, 1232], fill=(150, 156, 166), outline=OUT, width=4)
    return img
BOARD = _board()

# ------------------------------------------------------------ sprites
def calendar(pen):            # canvas 520x600
    pen.poly(rrect(20, 70, 500, 580, 26), PAPER, w=5)
    pen.poly(rrect(20, 70, 500, 190, 20), RED, w=5)
    for x in (120, 200, 320, 400):
        pen.poly(capsule(x, 40, x, 100, 12), (170, 170, 180), w=3.5)
    pen.text((260, 130), 'NOVEMBER', 54, PAPER)
    pen.text((260, 360), '30', 220, (40, 36, 48))
    pen.text((260, 520), 'MONDAY', 70, RED)

def release(pen):             # canvas 520x600
    pen.poly([(30, 30), (490, 30), (490, 570), (30, 570)], PAPER, w=5, amp=0.8)
    pen.text((260, 95), 'FOR IMMEDIATE', 44, (40, 36, 48))
    pen.text((260, 145), 'RELEASE', 44, (40, 36, 48))
    for k, y in enumerate(range(220, 540, 38)):
        pen.line([(70, y), (450 - (k % 3) * 50, y)], (170, 172, 182), 7, amp=0.6)

def stamp(pen):               # canvas 460x200
    pen.text((230, 100), 'PRESS RELEASE', 58, RED, rot=-10)
    pen.poly(xform(rrect(-205, -62, 205, 62, 20), 230, 100, rot=10), None, outline=RED, w=7, amp=0.8)

def computer(pen):            # canvas 560x560
    pen.poly(rrect(40, 30, 520, 400, 30), BEIGE, w=5)
    pen.poly(rrect(90, 70, 470, 340, 16), SCREEN, w=4.5)
    pen.poly([(220, 400), (340, 400), (370, 450), (190, 450)], BEIGE_D, w=4.5)
    pen.poly(rrect(70, 455, 490, 530, 14), BEIGE, w=4.5)
    for r in range(2):
        for c in range(9):
            x = 100 + c * 42; y = 470 + r * 28
            pen.poly(rrect(x, y, x + 32, y + 20, 4), BEIGE_D, w=2, amp=0.2)
    pen.dot(450, 375, 9, (90, 200, 120))

def cart(pen):                # canvas 220x180
    pen.line([(10, 30), (40, 30), (70, 120), (180, 120)], OUT, 8)
    pen.poly([(48, 50), (200, 50), (182, 110), (66, 110)], (230, 236, 246), w=5)
    for x in (95, 135, 165):
        pen.line([(x, 54), (x - 4, 106)], (150, 160, 180), 3)
    pen.ell(85, 150, 16, 16, fill=(60, 60, 70), w=4); pen.ell(170, 150, 16, 16, fill=(60, 60, 70), w=4)
    pen.poly(rrect(90, 20, 150, 56, 6), (240, 180, 90), w=4)

def house(pen):               # canvas 360x320
    pen.poly([(40, 150), (180, 30), (320, 150)], (200, 90, 80), w=5)
    pen.poly([(70, 150), (290, 150), (290, 300), (70, 300)], (246, 228, 196), w=5)
    pen.poly(rrect(150, 210, 210, 300, 6), (150, 100, 70), w=4)
    pen.poly(rrect(225, 180, 275, 225, 4), (170, 210, 236), w=4)
    pen.poly(rrect(90, 180, 135, 225, 4), (170, 210, 236), w=4)

def office(pen):              # canvas 360x420
    pen.poly([(60, 20), (300, 20), (300, 400), (60, 400)], (120, 136, 160), w=5)
    for r in range(6):
        for c in range(3):
            x = 85 + c * 72; y = 45 + r * 56
            pen.poly(rrect(x, y, x + 50, y + 36, 4), (200, 230, 248), w=3, amp=0.4)
    pen.poly(rrect(150, 345, 210, 400, 4), (70, 80, 100), w=4)

def snail(pen):               # canvas 160x110
    pen.poly([(10, 95), (150, 95), (140, 80), (20, 80)], (190, 170, 120), w=4)
    pen.ell(90, 55, 44, 40, fill=(210, 150, 90), w=4.5)
    pen.line([(90, 55), (100, 48), (96, 38), (84, 40), (80, 56), (92, 70), (108, 62)], OUT, 4, amp=0.3)
    pen.line([(132, 82), (140, 40)], OUT, 3.5); pen.dot(140, 38, 6, OUT)
    pen.line([(122, 82), (124, 46)], OUT, 3.5); pen.dot(124, 44, 6, OUT)

def leaf(pen):                # canvas 120x120
    pen.poly([(20, 100), (40, 40), (100, 20), (80, 80)], CASH, w=4)
    pen.line([(24, 96), (92, 28)], (30, 110, 60), 3)
    pen.text((62, 62), '$', 40, PAPER)

def marker(pen):              # canvas 300x80
    pen.poly(capsule(40, 40, 250, 40, 26), (60, 64, 80), w=4)
    pen.poly([(250, 22), (290, 40), (250, 58)], (40, 40, 48), w=3)
    pen.poly(rrect(70, 24, 140, 56, 6), (240, 240, 244), w=3)

CAL = [make_sprite(520, 600, calendar, seed=s) for s in (1, 2, 3)]
REL = [make_sprite(520, 600, release, seed=s) for s in (1, 2, 3)]
STAMP = make_sprite(460, 200, stamp, seed=4)
PC = [make_sprite(560, 560, computer, seed=s) for s in (1, 2, 3)]
CART = [make_sprite(220, 180, cart, seed=s) for s in (1, 2, 3)]
HOUSE = make_sprite(360, 320, house, seed=5)
OFFICE_B = make_sprite(360, 420, office, seed=6)
SNAIL = [make_sprite(160, 110, snail, seed=s) for s in (1, 2, 3)]
LEAF = make_sprite(120, 120, leaf, seed=7)
MARKER = make_sprite(300, 80, marker, seed=8)
FUZZ_S = fuzz_sprites('happy')
FUZZ_W = fuzz_sprites('shock')

def overlay(img, text, u, y=270, size=104):
    if u <= 0.02: return
    ImageDraw.Draw(img).text((540, y), text, font=font(FONT_CAP, int(size * u)), fill=HL,
                             anchor='mm', stroke_width=11, stroke_fill=OUT)

def bar(img, x0, y0, w, h, p, col):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h // 2, fill=(246, 246, 250), outline=OUT, width=5)
    if p > 0.02:
        d.rounded_rectangle([x0 + 6, y0 + 6, x0 + 6 + (w - 12) * p, y0 + h - 6], (h - 12) // 2, fill=col)

# scene starts: hook | 2005 office | slow internet | name ideas (lines 3-4) | zero results | loop back
B = [0, starts[1] - 0.12, starts[2] - 0.12, starts[3] - 0.12, starts[5] - 0.12, starts[6] - 0.12, DUR]

CAL_X, CAL_Y = 540, 860
def pose(p):
    """calendar pose by loop phase p (0 at the first and last frame)"""
    return CAL_X, CAL_Y + 8 * math.sin(p * 2.2), 2.0 * math.sin(p * 1.7)

T_FLIP = starts[0] + 1.75           # "It's a press release."

def s1(tl, frame, sd):
    img = WALL.copy()
    x, y, r = pose(tl)
    f = seg(tl, T_FLIP, T_FLIP + 0.35)
    if f < 0.5:
        paste(img, CAL[boil(frame)], x, y, 1.0, rot=r, sy=max(0.02, 1 - 2 * f))
    else:
        paste(img, REL[boil(frame)], x, y, 1.0, rot=r, sy=max(0.02, 2 * f - 1))
    su = seg(tl, T_FLIP + 0.45, T_FLIP + 0.7)
    if su > 0:
        paste(img, STAMP, x + 20, y + 40, lerp(1.8, 1.0, ease_out(su)), alpha=min(1, su * 3))
    overlay(img, "IT'S A PRESS RELEASE", ease_back(seg(tl, T_FLIP, T_FLIP + 0.3), 2.0), size=86)
    return img

def s2(tl, frame, sd):
    img = OFFICE.copy()
    paste(img, PC[boil(frame)], 540, 980, 1.25)
    for k in range(5):
        u = (tl * 0.55 + k / 5) % 1.0
        side = -1 if k % 2 else 1
        paste(img, CART[boil(frame, off=k)], 540 + side * lerp(0, 430, ease_in(u) * 0.6 + u * 0.4),
              880 + 220 * u + 30 * math.sin(u * 9), lerp(0.25, 1.0, u), flip=side < 0, alpha=min(1, u * 5))
    overlay(img, '2005', ease_back(seg(tl, 0.3, 0.6), 2.0), size=130)
    return img

def s3(tl, frame, sd):
    img = SPLIT.copy()
    paste(img, HOUSE, 290, 650, 1.0)
    paste(img, OFFICE_B, 290, 1130, 0.7)
    slow = 0.05 + 0.12 * seg(tl, 0.2, sd)
    fast = ease(seg(tl, 0.3, 1.1))
    bar(img, 500, 620, 480, 70, slow, (240, 170, 80))
    paste(img, SNAIL[boil(frame)], 500 + 470 * slow + 10, 575, 1.3)
    bar(img, 500, 1080, 480, 70, fast, (90, 200, 120))
    if fast > 0.98:
        sparkle(img, 960, 1060, 30 * math.sin(math.pi * seg(tl, 1.1, 1.6)))
    cu = ease(seg(tl, 0.4, 1.6))
    paste(img, CART[boil(frame)], lerp(420, 760, cu), lerp(760, 1180, cu), 0.75, rot=-20 * math.sin(math.pi * cu))
    overlay(img, 'SLOW HOME INTERNET', ease_back(seg(tl, 0.2, 0.5), 2.0), size=84)
    return img

def word(img, text, x, y, u, col, size=92):
    if u <= 0.01: return
    n = max(1, int(len(text) * u))
    ImageDraw.Draw(img).text((x, y), text[:n], font=font(FONT_CAP, size), fill=col, anchor='lm')

def s4(tl, frame, sd):
    img = BOARD.copy()
    t_black = 0.35
    t_crash = starts[3] - B[3] + 1.75
    t_blue = starts[4] - B[3] + 0.05
    t_green = starts[4] - B[3] + 1.6
    d = ImageDraw.Draw(img)
    word(img, 'BLACK MONDAY', 150, 610, seg(tl, t_black, t_black + 0.6), (30, 30, 36))
    cu = seg(tl, t_crash, t_crash + 0.35)
    if cu > 0:
        d.line([(140, 612), (140 + 720 * cu, 600)], fill=RED, width=12)
        pts = [(880, 540), (920, 600), (900, 610), (950, 680)]
        k = int(1 + 3 * seg(tl, t_crash + 0.2, t_crash + 0.6))
        d.line(pts[:k + 1], fill=RED, width=10)
        if k >= 3:
            d.polygon([(930, 690), (975, 700), (955, 655)], fill=RED)
    word(img, 'BLUE MONDAY', 150, 830, seg(tl, t_blue, t_blue + 0.6), LINK)
    bu = seg(tl, t_blue + 0.6, t_blue + 0.9)
    if bu > 0:
        d.line([(150, 885), (150 + 600 * bu, 885)], fill=LINK, width=8)
    word(img, 'GREEN MONDAY', 150, 1050, seg(tl, t_green, t_green + 0.6), CASH)
    lu = seg(tl, t_green + 0.6, t_green + 0.9)
    if lu > 0:
        paste(img, LEAF, 900, 1050, ease_back(lu, 2.0), rot=10 * math.sin(tl * 3))
    # marker follows whatever is being written
    tgt = (150 + 640 * seg(tl, t_black, t_black + 0.6), 610)
    if tl > t_crash: tgt = (860, 600)
    if tl > t_blue: tgt = (150 + 600 * seg(tl, t_blue, t_blue + 0.9), 840)
    if tl > t_green: tgt = (150 + 680 * seg(tl, t_green, t_green + 0.6), 1060)
    paste(img, MARKER, tgt[0] + 110, tgt[1] + 50 + 6 * math.sin(tl * 20), 0.9, rot=28)
    overlay(img, 'NAME IDEAS', ease_back(seg(tl, 0.2, 0.5), 2.0), size=100)
    return img

def s5(tl, frame, sd):
    img = OFFICE.copy()
    t_up = 1.25
    fu = ease_back(seg(tl, t_up, t_up + 0.45), 1.6)
    paste(img, (FUZZ_W if tl < t_up + 0.7 else FUZZ_S)[boil(frame)], 830, lerp(720, 480, fu), 0.8)
    paste(img, PC[boil(frame)], 540, 980, 1.6)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([290, 820, 790, 900], 36, fill=PAPER, outline=OUT, width=5)
    q = 'CYBER MONDAY'
    n = int(len(q) * seg(tl, 0.15, 1.0))
    d.text((330, 860), q[:n] + ('|' if (frame // 8) % 2 == 0 and n < len(q) else ''), font=font(FONT_CAP, 50), fill=(40, 36, 48), anchor='lm')
    ru = seg(tl, 1.05, 1.25)
    if ru > 0:
        d.text((540, 980), '0 RESULTS', font=font(FONT_CAP, int(70 * ease_back(ru, 2.0))), fill=PAPER, anchor='mm', stroke_width=6, stroke_fill=OUT)
    overlay(img, 'ZERO RESULTS', ease_back(seg(tl, 1.05, 1.35), 2.0), size=100)
    return img

def s6(tl, frame, sd):
    img = WALL.copy()
    p = tl - sd
    x, y, r = pose(p)
    u = ease_out(seg(tl, 0.0, 0.9))
    paste(img, CAL[boil(frame)], x, lerp(-400, y, u), 1.0, rot=lerp(-25, r, u))
    return img

FNS = [s1, s2, s3, s4, s5, s6]
SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate(FNS)]
EP = Episode(NAME, SCENES, CHUNKS, DUR, NO_END_TAG, loop=True)

def audio_plan():
    import pf_audio as A
    sfx = [(A.flutter(0.6), T_FLIP - 0.05, 0.45, 0), (A.stamp(), T_FLIP + 0.5, 0.6, 0.1)]
    sfx += [(A.tick(1500 + 120 * (k % 3), 0.04, 0.4), B[1] + 0.3 + k * 0.13, 0.22, ((k % 5) - 2) * 0.15) for k in range(20)]
    sfx += [(A.pop(), B[1] + 0.4 + k * 0.36, 0.25, (-1) ** k * 0.4) for k in range(6)]
    sfx += [(A.whoosh(0.9), B[2] + 0.35, 0.5, 0.2), (A.chime(1318.5), B[2] + 1.15, 0.3, 0.3)]
    t4 = B[3]
    sfx += [(A.scribble(0.6), t4 + 0.35, 0.45, -0.2), (A.thud(), t4 + starts[3] - B[3] + 1.75, 0.35, 0.3),
            (A.scribble(0.6), t4 + starts[4] - B[3] + 0.05, 0.45, -0.1), (A.scribble(0.6), t4 + starts[4] - B[3] + 1.6, 0.45, 0.1),
            (A.pop(), t4 + starts[4] - B[3] + 2.25, 0.35, 0.4)]
    sfx += [(A.tick(1700, 0.035, 0.45), B[4] + 0.15 + k * 0.07, 0.25, 0) for k in range(12)]
    sfx += [(A.chime(880.0), B[4] + 1.07, 0.35, 0), (A.boing(), B[4] + 1.25, 0.4, 0.35)]
    sfx += [(A.whoosh(0.8, False), B[5] - 0.05, 0.5, 0), (A.flutter(0.5), B[5] + 0.6, 0.3, 0)]
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
