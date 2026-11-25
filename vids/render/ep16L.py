"""Ep 16 loop cut: the last frame (and the last line) runs straight back into the first."""
import sys, math
from PIL import Image, ImageDraw, ImageEnhance
from pf import *
import ep16 as E

STYLE = 'folk'
lines, durs, starts, DUR = timeline('ep16L', first=0.15, gap=0.24, gaps={0: 0.3, 4: 0.3, 5: 0.32}, tail=0.42)
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={0: ['3', 'AM', 'CAR.'], 1: ['MOCKINGBIRD.'], 2: ['200'], 4: ['BEEPS.'], 5: ['ALL', 'NIGHT'], 6: ['3', 'AM,', 'REMEMBER:']})
NO_END_TAG = DUR + 99          # no end card: the loop is the ending

def night(img, k=0.55):
    out = ImageEnhance.Brightness(img.convert('RGB')).enhance(k).convert('RGBA')
    tint = Image.new('RGBA', out.size, (40, 60, 130, 60)); out.alpha_composite(tint)
    return out

STREET = night(E.HOUSE)
STREET_LIT = night(E.HOUSE_LIT, 0.62)
glow(STREET_LIT, 780, 730, 260, (255, 220, 140), 0.45)
def _moon(img):
    d = ImageDraw.Draw(img)
    d.ellipse([840, 90, 980, 230], fill=(244, 240, 220), outline=OUT, width=6)
    return img
STREET = _moon(STREET); STREET_LIT = _moon(STREET_LIT)

BIRD_X, BIRD_Y = 470, 920          # perched on the car roof: identical in the first and last frame
CAR_X, CAR_Y = 520, 1150
PERIOD = 0.3                       # car-alarm pulse

def alarm(img, phase, frame):
    """phase = seconds since the alarm started; drawn the same at t=0 and at the end."""
    E.alarm_waves(img, 620, 860, phase)
    E.alarm_waves(img, 330, 860, phase + 0.3, (255, 200, 80))
    if int(phase / PERIOD) % 2 == 0:
        d = ImageDraw.Draw(img); d.ellipse([60, 1050, 120, 1110], fill=(255, 120, 90))
    return E.BIRD_OPEN[boil(frame)] if int(phase / PERIOD) % 2 == 0 else E.BIRD[boil(frame)]

def overlay(img, text, u, y=290, size=118):
    if u <= 0.02: return
    d = ImageDraw.Draw(img)
    d.text((540, y), text, font=font(FONT_CAP, int(size * u)), fill=HL, anchor='mm', stroke_width=11, stroke_fill=OUT)

B = [0, starts[1] - 0.12, starts[2] - 0.12, starts[3] - 0.12, starts[6] - 0.12, DUR]
LEAD = 0.5                          # the alarm started LEAD seconds before frame 0 (= LEAD before the end)

def s1(tl, frame, sd):
    lit = tl > 1.0
    img = (STREET_LIT if lit else STREET).copy()
    paste(img, E.CAR, CAR_X, CAR_Y, 1.25)
    spr = alarm(img, tl + LEAD, frame)
    paste(img, spr, BIRD_X, BIRD_Y, 1.0)
    overlay(img, '3 AM ALARM?', ease_back(seg(tl, 0.25, 0.55), 2.0) * (1 - seg(tl, 1.7, 1.8)))
    overlay(img, 'NOT A CAR.', ease_back(seg(tl, 1.8, 2.1), 2.0))
    return img

def s2(tl, frame, sd):
    img = STREET_LIT.copy()
    paste(img, E.CAR, CAR_X, CAR_Y, 1.25)
    paste(img, E.BIRD[boil(frame)], BIRD_X, BIRD_Y, 1.0)
    glow(img, BIRD_X, BIRD_Y - 20, 260, (255, 240, 200), 0.35 * seg(tl, 0.1, 0.5))
    img = camera(img, lerp(1.0, 1.7, ease(seg(tl, 0.0, 0.9))), BIRD_X + 40, BIRD_Y - 10)
    overlay(img, 'MOCKINGBIRD', ease_back(seg(tl, 0.35, 0.65), 2.0), y=300, size=104)
    return img

def s3(tl, frame, sd):
    img = night(E.DUSK, 0.6)
    paste(img, E.singing(frame, tl, 6), 540, 900, 1.35)
    for k in range(8):
        t0 = 0.1 + k * 0.25
        u = ease_back(seg(tl, t0, t0 + 0.25), 2.2)
        if u < 0.02: continue
        a = -math.pi / 2 + (k - 3.5) * 0.42
        paste(img, E.BUB['note'], 540 + 400 * math.cos(a), 900 + 380 * math.sin(a) + 8 * math.sin(tl * 3 + k), 0.6 * u)
    n = int(200 * ease(seg(tl, 0.1, sd - 0.3)))
    d = ImageDraw.Draw(img)
    d.text((540, 290), f'~{n} SONGS', font=font(FONT_CAP, 104), fill=HL, anchor='mm', stroke_width=10, stroke_fill=OUT)
    return img

def s4(tl, frame, sd):
    img = E.ROOF.copy()
    paste(img, E.singing(frame, tl, 6), 380, 905 + 4 * math.sin(tl * 4), 1.2, rot=8)
    t_beep = starts[4] - B[3]
    t_night = starts[5] - B[3]
    for k, ic in enumerate(['bird', 'frog', 'gate', 'beep']):
        t0 = 0.15 + k * 0.6 if ic != 'beep' else t_beep - 0.05
        u = ease_back(seg(tl, t0, t0 + 0.3), 2.2) * (1 - seg(tl, t_night - 0.2, t_night + 0.1))
        if u > 0.02:
            paste(img, E.BUB[ic], 200 + k * 230, 560 + 20 * math.sin(tl * 3 + k), 0.7 * u)
    if tl > t_night:
        for k in range(4):
            u = (tl * 0.5 + k * 0.25) % 1
            paste(img, E.BUB['note'], 520 + 260 * u, 760 - 380 * u, 0.45 * math.sin(math.pi * u))
        cu = ease_out(seg(tl, t_night, t_night + 0.6))
        paste(img, E.CAT[boil(frame)], lerp(1300, 860, cu), 1070, 0.9)
        overlay(img, 'ALL NIGHT', ease_back(seg(tl, t_night + 0.2, t_night + 0.5), 2.0), y=300, size=104)
    return img

def s5(tl, frame, sd):
    img = STREET.copy()
    paste(img, E.CAR, CAR_X, CAR_Y, 1.25)
    land = ease_out(seg(tl, 0.0, 0.7))
    bx, by = lerp(1250, BIRD_X, land), lerp(500, BIRD_Y, land) - 140 * math.sin(math.pi * land)
    t_alarm = sd - LEAD
    if tl >= t_alarm:
        spr = alarm(img, tl - t_alarm, frame)
    else:
        spr = E.BIRD[boil(frame)]
    paste(img, spr, bx, by, 1.0, rot=-12 * (1 - land))
    return img

SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate([s1, s2, s3, s4, s5])]
EP = Episode('ep16L', SCENES, CHUNKS, DUR, NO_END_TAG, loop=True)

def audio_plan():
    import pf_audio as A
    sfx = []
    # car alarm: pulses on a fixed grid that started LEAD s before frame 0 and restarts LEAD s before the end
    k = 0
    while True:
        t = -LEAD + k * PERIOD
        if t > B[1] - 0.1: break
        if t >= 0: sfx.append((A.honk(880 if k % 2 == 0 else 660, 0.2), t, 0.34, 0.1))
        k += 1
    for k in range(int(LEAD / PERIOD) + 1):
        t = DUR - LEAD + k * PERIOD
        if t < DUR: sfx.append((A.honk(880 if k % 2 == 0 else 660, 0.2), t, 0.34, 0.1))
    sfx += [(A.chime(988.0), 1.0, 0.18, 0.4)]                        # neighbour's light clicks on
    sfx += [(A.sparkles(), B[1] + 0.2, 0.3, 0), (A.whoosh(0.4), B[2] - 0.15, 0.4, 0)]
    sfx += [(A.whistle(0.22), B[2] + 0.1 + k * 0.25, 0.22, ((k % 3) - 1) * 0.4) for k in range(8)]
    sfx += [(A.chime(988.0), B[3] + 0.15 + k * 0.6, 0.2, 0) for k in range(3)]
    sfx += [(A.honk(760, 0.18), starts[4] + k * 0.25, 0.28, 0.1) for k in range(3)]
    sfx += [(A.whistle(0.5), starts[5] + 0.1, 0.28, -0.3), (A.thud(), starts[5] + 0.5, 0.3, 0.5)]
    sfx += [(A.flutter(), B[4] + 0.05, 0.4, 0.3)]
    cues = [(f'/home/claude/eps/ep16L_vo_{i}.wav', s) for i, s in enumerate(starts)]
    return cues, sfx

if __name__ == '__main__':
    if sys.argv[1] == 'audio':
        import pf_audio as A
        cues, sfx = audio_plan()
        A.build(DUR, cues, sfx, '/home/claude/eps/ep16L/audio.wav', style=STYLE, loop=True)
        print('audio ok')
    else:
        EP.main(sys.argv)
