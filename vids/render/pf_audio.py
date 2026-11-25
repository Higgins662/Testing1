"""Pocketfuzzy audio: music-box bed, synth SFX, VO mix with ducking."""
import numpy as np, wave, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly

SR = 44100
rng = np.random.default_rng(3)

def env(n, a=0.005, d=0.3):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def bp(x, lo, hi, order=2): return sosfilt(butter(order, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def lp(x, f): return sosfilt(butter(2, f, 'lowpass', fs=SR, output='sos'), x)
def tone(f, dur, decay, harm=(1, 0.3, 0.1)):
    n = int(dur * SR); t = np.arange(n) / SR
    return sum(a * np.sin(2 * np.pi * f * (k + 1) * t) for k, a in enumerate(harm)) * env(n, 0.004, decay)

NOTES = {'C3': 130.81, 'G2': 98.0, 'A2': 110.0, 'F2': 87.31, 'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'G4': 392.0,
         'A4': 440.0, 'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'G5': 783.99, 'A5': 880.0, 'F4': 349.23, 'B4': 493.88}
MELODIES = {
    'A': ['E5', 'G5', 'A5', 'G5', 'E5', 'D5', 'C5', 'D5', 'E5', 'G5', 'C5', 'A4', 'G4', 'A4', 'C5', None],
    'B': ['C5', 'E5', 'G5', 'E5', 'A5', 'G5', 'E5', 'D5', 'C5', 'D5', 'E5', 'G4', 'A4', 'C5', 'D5', None],
    'C': ['G4', 'C5', 'E5', 'D5', 'C5', 'A4', 'G4', 'A4', 'C5', 'E5', 'G5', 'E5', 'D5', 'C5', 'A4', None],
}

def music(dur, melody='A', bpm=100):
    N = int(SR * dur); m = np.zeros(N, np.float32)
    beat = 60 / bpm; mel = MELODIES[melody]; bass = ['C3', 'A2', 'F2', 'G2']
    t = 0.15; k = 0
    while t < dur - 0.5:
        nm = mel[k % len(mel)]
        def put(s):
            i = int(t * SR); m[i:i + len(s)] += s[: N - i]
        if nm: put(tone(NOTES[nm], 1.6, 0.55, (1, 0.25, 0.08, 0.04)) * 0.33)
        if k % 4 == 0: put(lp(tone(NOTES[bass[(k // 4) % 4]], 1.4, 0.32, (1, 0.5, 0.25, 0.12)) * 0.42, 900))
        if k % 2 == 1: put(tone(NOTES[['C4', 'E4', 'G4', 'E4'][(k // 2) % 4]], 0.4, 0.09, (1, 0.4)) * 0.16)
        t += beat / 2; k += 1
    fade = np.ones(N, np.float32)
    fi = int(0.6 * SR); fade[:fi] = np.linspace(0, 1, fi)
    fo = int(1.4 * SR); fade[-fo:] = np.linspace(1, 0, fo)
    return m * fade

# ---------------- SFX library
def rustle(dur=0.4):
    n = int(dur * SR); x = bp(rng.normal(0, 1, n), 1800, 7000)
    return lp(x * env(n, 0.01, dur / 3) * (0.6 + 0.4 * (rng.random(n) > 0.85)), 9000) * 0.35
def whoosh(dur=0.5, up=True):
    n = int(dur * SR); t = np.arange(n) / SR; x = rng.normal(0, 1, n); out = np.zeros(n)
    for i in range(0, n, 512):
        u = i / n; fc = 300 + 2500 * (u if up else 1 - u)
        out[i:i + 512] = bp(x[i:i + 512], fc * 0.7, fc * 1.4, 1)
    return lp(out * np.sin(np.pi * t / dur) ** 2, 6000) * 0.35
def pop():
    n = int(0.15 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(700 * np.exp(-t * 18) + 160) / SR) * env(n, 0.002, 0.04) * 0.6
def chime(f=1046.5):
    n = int(1.6 * SR); t = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / d) for r, a, d in ((1, 1, 0.9), (2.76, 0.4, 0.4), (5.4, 0.2, 0.2)))
    return x * np.minimum(1, t / 0.003) * 0.22
def sparkles(count=7, span=0.7, base=2200):
    out = np.zeros(int((span + 0.6) * SR))
    for i in range(count):
        s = tone(base * rng.uniform(1, 2.2), 0.5, 0.12, (1, 0.15)) * 0.12
        j = int(rng.uniform(0, span) * SR); out[j:j + len(s)] += s[: len(out) - j]
    return out
def tick(f=900, dur=0.08, g=0.5):
    n = int(dur * SR); return bp(rng.normal(0, 1, n), f * 0.6, f * 1.8) * env(n, 0.001, 0.015) * g
def thud():
    n = int(0.3 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * np.cumsum(120 * np.exp(-t * 8) + 50) / SR) * env(n, 0.002, 0.08) * 0.8 + tick(300, 0.1, 0.5)[:n].sum() * 0)
def wind(dur=2.0):
    n = int(dur * SR); t = np.arange(n) / SR
    x = lp(rng.normal(0, 1, n), 700) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.4 * t))
    return x * np.sin(np.pi * t / dur) * 0.35
def honk(f=400, dur=0.25):
    n = int(dur * SR); t = np.arange(n) / SR
    sq = np.sign(np.sin(2 * np.pi * f * t)) + 0.6 * np.sign(np.sin(2 * np.pi * f * 1.26 * t))
    return lp(sq, 2500) * env(n, 0.01, dur) * 0.12
def whistle(dur=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 2800 + 120 * np.sign(np.sin(2 * np.pi * 28 * t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.02) * np.minimum(1, (dur - t) / 0.05) * 0.16
def crowd(dur=2.0):
    n = int(dur * SR); t = np.arange(n) / SR
    x = bp(rng.normal(0, 1, n), 300, 2200) * (0.7 + 0.3 * np.sin(2 * np.pi * 3 * t + rng.uniform(0, 6)))
    return x * np.sin(np.pi * t / dur) ** 0.5 * 0.25
def scribble(dur=0.6):
    n = int(dur * SR); t = np.arange(n) / SR
    return bp(rng.normal(0, 1, n), 2500, 7000) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t)) ** 2 * 0.25
def stamp():
    return thud() * 0.8 + tick(600, 0.08, 0.6)[:int(0.3 * SR)].mean() * 0
def brass(f=392.0, dur=0.7):
    n = int(dur * SR); t = np.arange(n) / SR
    saw = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 8))
    return lp(saw, 2200) * np.minimum(1, t / 0.05) * np.exp(-t / 0.5) * 0.18
def engine(dur=1.5, f=70):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * (f + 8 * np.sin(2 * np.pi * 3 * t)) * t)) * 0.5 + 0.3 * rng.normal(0, 1, n)
    return lp(x, 600) * np.sin(np.pi * t / dur) * 0.2
def slurp(): return whoosh(0.35, False) * 0.7
def splash():
    n = int(0.5 * SR); return bp(rng.normal(0, 1, n), 800, 5000) * env(n, 0.005, 0.12) * 0.5
def boing():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 300 + 180 * np.sin(2 * np.pi * 12 * t) * np.exp(-t * 6)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, 0.15) * 0.4
def flutter(dur=0.8):
    n = int(dur * SR); t = np.arange(n) / SR
    return lp(rng.normal(0, 1, n), 1500) * (0.5 + 0.5 * np.sin(2 * np.pi * 14 * t)) ** 3 * np.sin(np.pi * t / dur) * 0.5

def build(dur, cues, sfx_events, out, melody='A', music_gain=0.5, style=None):
    """style: one of pf_music.ROTATION (preferred). melody: legacy music-box fallback."""
    N = int(SR * dur)
    if style:
        import pf_music
        st = pf_music.render(style, dur)[:N]
        st = np.pad(st, ((0, N - len(st)), (0, 0)))
        mus2 = st * 1.7
    else:
        m1 = music(dur, melody); mus2 = np.stack([m1, m1], 1)
    sfx = np.zeros((N, 2), np.float32)
    for (sig, t, g, pan) in sfx_events:
        i = int(t * SR)
        if i >= N: continue
        s = np.asarray(sig, np.float32)[: N - i] * g
        sfx[i:i + len(s), 0] += s * np.sqrt(0.5 * (1 - pan)); sfx[i:i + len(s), 1] += s * np.sqrt(0.5 * (1 + pan))
    vo = np.zeros(N, np.float32)
    for path, st in cues:
        a, sr = sf.read(path)
        if a.ndim > 1: a = a.mean(1)
        if sr == 24000: a = resample_poly(a, 147, 80)
        i = int(st * SR); vo[i:i + len(a)] += a[: N - i]
    vo = vo / (np.abs(vo).max() + 1e-9) * 0.9
    envv = np.convolve(np.abs(vo), np.ones(441) / 441, 'same')
    att, rel = np.exp(-1 / (0.02 * SR)), np.exp(-1 / (0.35 * SR))
    e = np.zeros(N, np.float32); cur = 0.0
    for i in range(0, N, 64):
        v = envv[i:i + 64].max()
        cur = att * cur + (1 - att) * v if v > cur else rel * cur + (1 - rel) * v
        e[i:i + 64] = cur
    e = np.clip(e / 0.15, 0, 1)
    mix = np.zeros((N, 2), np.float32)
    mix += mus2 * music_gain * (1 - 0.62 * e)[:, None]
    mix += sfx * 0.75 * (1 - 0.35 * e)[:, None]
    mix[:, 0] += vo; mix[:, 1] += vo
    mix = mix / np.abs(mix).max() * 0.89
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
