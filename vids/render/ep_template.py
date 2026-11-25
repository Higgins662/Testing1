"""Pocketfuzzy episode template: a LOOP CUT (the default house format).

Copy to epNN.py, write epNN_lines.json, voice it, then replace the placeholder art and scenes.
    cp ep_template.py ep38.py          # and set NAME below
    python3 tts_lines.py ep38 af_heart en-us
    python3 ep38.py preview 0.0,4.0,9.0,15.0,LAST     # LAST = DUR - 0.04; check first vs last frame match
    ./render.sh ep38 pocketfuzzy_ep38_slug_loop

Rules the template already follows (keep them):
- loop=True: no picture fade, no end tag, music and SFX wrap, so the last frame flows into frame 0.
- The LAST scene settles onto exactly the pose and background of the FIRST frame (see pose()).
- The last VO line is a lead-in that finishes grammatically with the first line ("…so next time, remember:").
- One big overlay per beat, max 3 words, upper third (y 220-300), never covering the captions at the bottom.
- The Fuzz is armless, appears at least once (usually the last beat), same design every episode.
- Draw only original shapes. No logos, brands, real people, franchise characters, or the viral image itself.
Real episodes to learn from: ep16L.py (Car Alarm Bird) and ep20L.py (Bathroom-Tile Rocket) and their bases ep16.py / ep20.py.
"""
import sys, math
from PIL import Image, ImageDraw
from pf import *

NAME = 'ep_template'                      # must match the file name and the *_lines.json / *_durs.json prefix
STYLE = 'bossa'                           # next in rotation: folk jazz lofi bossa synth ambient
lines, durs, starts, DUR = timeline(NAME, first=0.15, gap=0.24, tail=0.42)   # tight gaps: aim 20-24s total
CHUNKS = chunks_from(lines, durs, starts, DUR, emph={0: []})                  # emph: words to highlight per line (UPPERCASE, with punctuation)
NO_END_TAG = DUR + 99                     # loop cuts have no end card

# ------------------------------------------------------------ backgrounds (built once, copied per frame)
SKY = downsample(bg_canvas([(0, (150, 200, 235)), (0.6, (210, 232, 240)), (1, (240, 226, 196))],
                           glows=[(800, 360, 520, (255, 246, 214), 0.5)]), W, H)   # bg_canvas draws at 2x: always downsample
def _ground(img, y=1380, col=(150, 190, 120)):
    d = ImageDraw.Draw(img)
    d.rectangle([0, y, W, H], fill=col)
    d.line([(0, y), (W, y)], fill=OUT, width=6)
    return img
SCENE_A = _ground(SKY.copy())

# ------------------------------------------------------------ sprites: draw with Pen in canvas coordinates
def subject(pen):
    """placeholder subject: replace with the episode's animal/object. Canvas 400x360."""
    pen.ell(200, 220, 150, 110, fill=(240, 190, 120), w=5)      # body
    pen.ell(200, 120, 90, 80, fill=(240, 190, 120), w=5)        # head
    pen.dot(170, 110, 10, OUT); pen.dot(230, 110, 10, OUT)      # eyes
    pen.line([(180, 150), (200, 160), (220, 150)], OUT, 4)      # smile
SUBJ = [make_sprite(400, 360, subject, seed=s) for s in (1, 2, 3)]   # 3 seeds = hand-drawn "boil"
FUZZ_S = fuzz_sprites('happy')
FUZZ_W = fuzz_sprites('shock')

def overlay(img, text, u, y=270, size=104):
    if u <= 0.02: return
    ImageDraw.Draw(img).text((540, y), text, font=font(FONT_CAP, int(size * u)), fill=HL,
                             anchor='mm', stroke_width=11, stroke_fill=OUT)

# scene boundaries: one scene per VO beat; B[k] = start of scene k (a hair before its line starts)
NS = min(5, len(starts))
B = [0] + [starts[i] - 0.12 for i in range(1, NS)] + [DUR]

def pose(p):
    """subject pose as a function of loop phase p. p = 0 at frame 0 AND at the very last frame."""
    return 540, 1100 + 10 * math.sin(p * 2.0), 3 * math.sin(p * 1.3)

# ------------------------------------------------------------ scenes: fn(t_local, frame, scene_duration) -> RGBA image
def s1(tl, frame, sd):                    # HOOK: the most surprising picture, readable in 1 second
    img = SCENE_A.copy()
    x, y, r = pose(tl)
    paste(img, SUBJ[boil(frame)], x, y, 1.3, rot=r)
    overlay(img, 'HOOK WORDS', ease_back(seg(tl, 0.2, 0.5)))
    return img

def s2(tl, frame, sd):                    # CONTEXT: who/where/when
    img = SCENE_A.copy()
    paste(img, SUBJ[boil(frame)], lerp(300, 540, ease(seg(tl, 0, 1))), 1100, 1.0)
    overlay(img, 'CONTEXT', ease_back(seg(tl, 0.3, 0.6)))
    return img

def s3(tl, frame, sd):                    # THE FACT: the visual explanation
    img = SCENE_A.copy()
    camera_z = lerp(1.0, 1.15, ease(seg(tl, 0, sd)))
    paste(img, SUBJ[boil(frame)], 540, 1050, 1.4)
    for k in range(5):
        sparkle(img, 300 + k * 120, 760, 22 * math.sin(math.pi * seg(tl, 0.4 + k * 0.08, 1.0 + k * 0.08)))
    return camera(img, camera_z, 540, 1000)

def s4(tl, frame, sd):                    # TWIST / payoff, the Fuzz reacts
    img = SCENE_A.copy()
    paste(img, SUBJ[boil(frame)], 400, 1100, 1.1)
    paste(img, (FUZZ_W if tl < 0.8 else FUZZ_S)[boil(frame)], 820, 1230 + 8 * math.sin(tl * 4), 0.7)
    overlay(img, 'PAYOFF', ease_back(seg(tl, 0.3, 0.6)))
    return img

def s_last(tl, frame, sd):                # LOOP-BACK: ends on exactly frame 0
    img = SCENE_A.copy()
    p = tl - sd                            # reaches 0 at the final frame
    x, y, r = pose(p)
    u = ease_out(seg(tl, 0.0, 0.8))
    paste(img, SUBJ[boil(frame)], x, lerp(y + 300, y, u), 1.3, rot=r)
    return img

FNS = [s1, s2, s3, s4, s_last][-NS:] if NS < 5 else [s1, s2, s3, s4, s_last]
SCENES = [(B[i], B[i + 1], fn) for i, fn in enumerate(FNS)]
EP = Episode(NAME, SCENES, CHUNKS, DUR, NO_END_TAG, loop=True)

def audio_plan():
    """SFX events: (sound, start_seconds, gain, pan -1..1). Events past DUR wrap to the start."""
    import pf_audio as A
    sfx = [(A.pop(), B[1] + 0.2, 0.5, 0), (A.whoosh(0.6), B[2] - 0.1, 0.5, 0),
           (A.sparkles(), B[2] + 0.4, 0.35, 0), (A.boing(), B[3] + 0.3, 0.45, 0.3),
           (A.whoosh(0.8, False), B[-2] - 0.1, 0.5, 0)]
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
