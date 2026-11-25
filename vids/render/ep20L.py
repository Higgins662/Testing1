"""Ep 20 loop cut: the last line and the last frame run straight back into the first."""
import sys, math
from PIL import Image, ImageDraw
from pf import *
import ep20 as E

STYLE = 'ambient'
lines, durs, starts, DUR = timeline('ep20L', first=0.15, gap=0.24, gaps={0: 0.32, 1: 0.28, 4: 0.3, 6: 0.34}, tail=0.42)
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={0: ['BATHROOM', 'TILES.'], 1: ['LAVA.'], 2: ['THOUSANDS'], 4: ['HONEYCOMB.'], 6: ['CHOPSTICKS'], 7: ['SAME', 'WAY:']})
NO_END_TAG = DUR + 99

B = [0] + [starts[i] - 0.12 for i in (1, 2, 4, 5, 7)] + [DUR]

def overlay(img, text, u, y=290, size=112):
    if u <= 0.02: return
    d = ImageDraw.Draw(img)
    d.text((540, y), text, font=font(FONT_CAP, int(size * u)), fill=HL, anchor='mm', stroke_width=11, stroke_fill=OUT)

def speed_lines(img, p):
    d = ImageDraw.Draw(img)
    for k in range(14):
        y = (k * 140 - p * 900) % 2000 - 40
        x = 80 + (k * 197) % 940
        d.line([(x, y), (x, y + 120)], fill=(220, 230, 250), width=4)

def pose(p):
    """rocket position/rotation as a function of loop phase p (p = 0 at the first frame and at the last)"""
    return 540, 760 + 14 * math.sin(p * 2), -6 + 2 * math.sin(p * 1.3)

def s1(tl, frame, sd):
    img = E.SKY.copy()
    speed_lines(img, tl)
    x, y, r = pose(tl)
    paste(img, E.ROCKET, x, y, 1.05, rot=r)
    t_tiles = starts[0] + 2.35
    if tl > t_tiles:
        for k in range(5):
            sparkle(img, 330 + k * 110, 860 + 10 * (k % 2), 26 * math.sin(math.pi * seg(tl, t_tiles + k * 0.08, t_tiles + 0.6 + k * 0.08)))
        du = seg(tl, t_tiles, t_tiles + 2.2)
        paste(img, E.DUCK, lerp(-150, 1250, du), 1100 - 120 * math.sin(math.pi * du), 0.9, rot=20 * math.sin(tl * 3))
        overlay(img, 'BATHROOM TILES?!', ease_back(seg(tl, t_tiles, t_tiles + 0.3), 2.0), size=100)
    return img

def s2(tl, frame, sd):
    img = E.HOT.copy()
    heat = seg(tl, 0.0, 1.2)
    glow(img, 540, 900, 560, (255, 130, 160), 0.55 * heat)
    glow(img, 540, 920, 380, (255, 200, 120), 0.6 * heat)
    d = ImageDraw.Draw(img)
    for k in range(18):
        x = 140 + k * 46
        y0 = 980 + 30 * math.sin(k)
        ln = 120 + 80 * math.sin(tl * 9 + k)
        d.line([(x, y0), (x - 30, y0 + ln * heat)], fill=(255, 190, 150), width=6)
    paste(img, E.ROCKET, 540, 840 + 8 * math.sin(tl * 14), 1.0, rot=-4)
    t_lava = 1.6
    level = ease(seg(tl, 0.2, t_lava + 0.2))
    tx, ty = 900, 420
    paste(img, E.THERM, tx, ty, 0.6)
    d.rectangle([tx - 8, ty + 0.6 * (220 - 360 * level), tx + 8, ty + 0.6 * 225], fill=(220, 60, 50))
    if tl > t_lava + 0.2:
        u = seg(tl, t_lava + 0.2, t_lava + 0.8)
        for k in range(8):
            a = 2 * math.pi * k / 8
            sparkle(img, tx + 90 * u * math.cos(a), ty - 150 + 90 * u * math.sin(a), 24 * (1 - u * 0.5), color=(255, 120, 90))
    if tl > t_lava:
        paste(img, E.LAVA, 200, 420, 0.8 * ease_back(seg(tl, t_lava, t_lava + 0.4), 2.0))
    overlay(img, 'HOTTER THAN LAVA', ease_back(seg(tl, t_lava, t_lava + 0.3), 2.0), y=250, size=96)
    return shake(img, 6 * heat, frame)

def s3(tl, frame, sd):
    img = E.HULL_BG.copy()
    n = int(len(E.HEXES) * ease(seg(tl, 0.1, sd - 1.6)))
    t_heat = starts[3] - B[2]
    gl = math.sin(math.pi * seg(tl, t_heat, t_heat + 1.2)) if tl > t_heat else 0
    img.alpha_composite(E.tiles_layer(n, gl))
    if gl > 0:
        d = ImageDraw.Draw(img)
        for k in range(6):
            x = 160 + k * 160
            pts = [(x + 20 * math.sin(tl * 6 + j + k), 700 - j * 40) for j in range(8)]
            d.line(pts, fill=(255, 200, 150), width=6)
    paste(img, E.WORKER[boil(frame)], 380 + 40 * math.sin(tl * 2), 1120, 1.0)
    overlay(img, 'THOUSANDS OF TILES', ease_back(seg(tl, 0.5, 0.85), 2.0), y=260, size=84)
    return img

def s4(tl, frame, sd):
    img = E.HULL_BG.copy()
    img.alpha_composite(E.tiles_layer(len(E.HEXES)))
    u = ease(seg(tl, 0.1, 1.0))
    off = int(lerp(W, 0, u))
    if off < W:
        img.alpha_composite(E.honeycomb_layer(1.0), (off, 0))
    if u > 0.98:
        glow(img, 540, 900, 500, (255, 220, 120), 0.3 * seg(tl, 1.0, 1.4))
    for k in range(2):
        paste(img, E.BEE[boil(frame, off=k)], 300 + 500 * k + 80 * math.sin(tl * 3 + k), 600 + 60 * math.sin(tl * 5 + k * 2), 1.0, flip=k == 1)
    return img

def s5(tl, frame, sd):
    img = E.PAD.copy()
    paste(img, E.TOWER, 300, 1500 - 710, 1.0)
    desc = ease_out(seg(tl, 0.0, 1.5))
    paste(img, E.ROCKET, 700, lerp(-300, 700, desc), 0.95, rot=90)
    close = ease_back(seg(tl, 1.4, 2.0), 1.4)
    for (yy, sgn) in ((560, 1), (760, -1)):
        ang = lerp(28 * sgn, 0, close)
        paste(img, E.ARM, 300 + 290 * math.cos(math.radians(ang)), yy - 290 * math.sin(math.radians(ang)) * 0.5, 0.85, rot=ang)
    overlay(img, 'CAUGHT!', ease_back(seg(tl, 1.95, 2.25), 2.0), y=220, size=100)
    paste(img, E.CHAIR, 900, 1640, 0.8)
    paste(img, E.FUZZ[boil(frame)], 900, 1560 + 6 * math.sin(tl * 3), 0.6)
    return img

def s6(tl, frame, sd):
    """back up to the fall: settles onto exactly the pose of the first frame"""
    img = E.SKY.copy()
    p = tl - sd
    speed_lines(img, p)
    x, y, r = pose(p)
    u = ease_out(seg(tl, 0.0, 1.0))
    paste(img, E.ROCKET, x, lerp(-350, y, u), 1.05, rot=lerp(20, r, u))
    return img

SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate([s1, s2, s3, s4, s5, s6])]
EP = Episode('ep20L', SCENES, CHUNKS, DUR, NO_END_TAG, loop=True)

def audio_plan():
    import pf_audio as A
    fall_len = (DUR - B[5]) + B[1]             # one continuous wind/rumble bed: last scene -> wraps -> first scene
    sfx = [(A.wind(fall_len), B[5], 0.45, 0), (A.engine(fall_len, 45), B[5], 0.3, 0)]
    t_tiles = starts[0] + 2.35
    sfx += [(A.sparkles(), t_tiles, 0.35, 0), (A.honk(620, 0.15), t_tiles + 0.8, 0.3, -0.3), (A.honk(620, 0.15), t_tiles + 1.05, 0.3, 0.1)]
    sfx += [(A.whoosh(1.0), B[1], 0.6, 0), (A.wind(B[2] - B[1]), B[1], 0.55, 0), (A.pop(), B[1] + 1.8, 0.5, 0.4)]
    sfx += [(A.tick(1600 + 100 * (k % 4), 0.05, 0.45), B[2] + 0.2 + k * 0.2, 0.28, ((k % 5) - 2) * 0.2) for k in range(18)]
    sfx += [(A.engine(1.2, 140), B[3] + 0.15, 0.18, 0), (A.chime(1046.5), B[3] + 1.05, 0.35, 0)]
    sfx += [(A.wind(1.5), B[4], 0.35, 0), (A.thud(), B[4] + 1.7, 0.7, 0.2), (A.stamp(), B[4] + 1.8, 0.4, 0.2)]
    sfx += [(A.whoosh(0.8, False), B[5] - 0.1, 0.5, 0)]
    cues = [(f'/home/claude/eps/ep20L_vo_{i}.wav', s) for i, s in enumerate(starts)]
    return cues, sfx

if __name__ == '__main__':
    if sys.argv[1] == 'audio':
        import pf_audio as A
        cues, sfx = audio_plan()
        A.build(DUR, cues, sfx, '/home/claude/eps/ep20L/audio.wav', style=STYLE, loop=True)
        print('audio ok')
    else:
        EP.main(sys.argv)
