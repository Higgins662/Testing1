"""Pocketfuzzy background music: a rotating set of mellow, grown-up styles."""
import numpy as np
from scipy.signal import butter, sosfilt, lfilter, fftconvolve

SR = 44100
ROTATION = ['folk', 'jazz', 'lofi', 'bossa', 'synth', 'ambient']
STYLE_NAMES = {'folk': 'Acoustic folk', 'jazz': 'Brushed jazz trio', 'lofi': 'Lo-fi hip hop',
               'bossa': 'Bossa nova', 'synth': 'Chill synthwave', 'ambient': 'Ambient downtempo'}

def mf(m): return 440.0 * 2 ** ((m - 69) / 12)
def _sos(kind, f, order=2): return butter(order, f, kind, fs=SR, output='sos')
def lp(x, f, o=2): return sosfilt(_sos('lowpass', f, o), x)
def hp(x, f, o=2): return sosfilt(_sos('highpass', f, o), x)
def bp(x, lo, hi, o=2): return sosfilt(_sos('bandpass', [lo, hi], o), x)

class Track:
    def __init__(self, dur, seed=1):
        self.N = int(dur * SR); self.L = np.zeros(self.N); self.R = np.zeros(self.N)
        self.rng = np.random.default_rng(seed)
    def add(self, sig, t, gain=1.0, pan=0.0):
        i = int(t * SR)
        if i >= self.N or i < 0: return
        s = sig[: self.N - i] * gain
        self.L[i:i + len(s)] += s * np.sqrt(0.5 * (1 - pan)); self.R[i:i + len(s)] += s * np.sqrt(0.5 * (1 + pan))

def env_ad(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)

# ------------------------------------------------------------ instruments
def ep_piano(f, dur=1.6, vel=1.0):
    """Rhodes-style electric piano (FM)."""
    n = int(dur * SR); t = np.arange(n) / SR
    idx = 1.6 * np.exp(-t / 0.35) + 0.25
    mod = np.sin(2 * np.pi * f * t) * idx
    tone = np.sin(2 * np.pi * f * t + mod)
    bell = np.sin(2 * np.pi * f * 7.0 * t) * np.exp(-t / 0.05) * 0.12
    e = env_ad(n, 0.004, 0.9) * np.minimum(1, (dur - t) / 0.08)
    return (tone + bell) * e * 0.3 * vel

def piano(f, dur=1.8, vel=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n); B = 0.0004
    for k in range(1, 7):
        fk = f * k * np.sqrt(1 + B * k * k)
        if fk > 8000: break
        s += np.sin(2 * np.pi * fk * t) * (0.9 ** k) / k * np.exp(-t / (1.2 / k ** 0.7))
    s += lp(np.random.default_rng(int(f)).normal(0, 1, n), 3000) * np.exp(-t / 0.01) * 0.05
    return s * env_ad(n, 0.002, 2.5) * np.minimum(1, (dur - t) / 0.1) * 0.28 * vel

def pluck(f, dur=2.0, bright=0.5, decay=0.996, seed=0):
    """Karplus-Strong string (nylon/steel guitar)."""
    n = int(dur * SR); P = max(2, int(round(SR / f)))
    rng = np.random.default_rng(seed + int(f * 10))
    exc = np.zeros(n); burst = rng.uniform(-1, 1, P)
    burst = lp(burst, 1500 + 6000 * bright)
    exc[:P] = burst
    a = np.zeros(P + 2); a[0] = 1; a[P] = -0.5 * decay; a[P + 1] = -0.5 * decay
    y = lfilter([1.0], a, exc)
    return lp(y, 5000) * np.minimum(1, (dur - np.arange(n) / SR) / 0.05) * 0.5

def upright(f, dur=0.6, vel=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
    s = np.tanh(1.4 * s) * env_ad(n, 0.006, 0.45) * np.minimum(1, (dur - t) / 0.05)
    s += lp(np.random.default_rng(int(f)).normal(0, 1, n), 900) * np.exp(-t / 0.012) * 0.15
    return s * 0.42 * vel

def synth_bass(f, dur=0.4):
    n = int(dur * SR); t = np.arange(n) / SR
    saw = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 12))
    return lp(saw, 700) * env_ad(n, 0.005, 0.35) * np.minimum(1, (dur - t) / 0.03) * 0.35

def pad(freqs, dur, attack=0.6, cutoff=1400, det=0.006):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        for dv in (-det, 0, det):
            ff = f * (1 + dv); kmax = int(min(24, 5000 / ff))
            ph = np.random.default_rng(int(ff)).uniform(0, 6.28)
            s += sum(np.sin(2 * np.pi * ff * k * t + ph * k) / k for k in range(1, kmax + 1))
    s = lp(s, cutoff)
    e = np.minimum(1, t / attack) * np.minimum(1, (dur - t) / 0.6)
    return s * e * 0.05 / max(1, len(freqs)) * 3

def soft_square(f, dur=0.2):
    n = int(dur * SR); t = np.arange(n) / SR
    sq = sum(np.sin(2 * np.pi * f * k * t) / k for k in (1, 3, 5, 7))
    return lp(sq, 2200) * env_ad(n, 0.003, 0.12) * 0.18

# ------------------------------------------------------------ drums
def kick(soft=1.0):
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 45 + 80 * np.exp(-t * 28)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.18)
    return s * 0.75 * soft
def snare(lofi=False):
    n = int(0.3 * SR); t = np.arange(n) / SR
    nz = bp(np.random.default_rng(7).normal(0, 1, n), 1200, 6000) * np.exp(-t / 0.11)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.06)
    s = nz * 0.45 + tone * 0.35
    return lp(s, 3500) * 0.8 if lofi else s * 0.6
def hat(open_=False, seed=0):
    n = int((0.25 if open_ else 0.06) * SR); t = np.arange(n) / SR
    s = hp(np.random.default_rng(11 + seed).normal(0, 1, n), 7000) * np.exp(-t / (0.12 if open_ else 0.02))
    return s * 0.22
def rim():
    n = int(0.06 * SR); t = np.arange(n) / SR
    return (bp(np.random.default_rng(3).normal(0, 1, n), 1500, 4000) * 0.5 + np.sin(2 * np.pi * 1700 * t) * 0.4) * np.exp(-t / 0.012) * 0.45
def brush(dur=0.22, seed=0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = bp(np.random.default_rng(5 + seed).normal(0, 1, n), 2500, 9000)
    return s * np.minimum(1, t / 0.04) * np.exp(-t / 0.09) * 0.2
def shaker(seed=0):
    n = int(0.09 * SR); t = np.arange(n) / SR
    return hp(np.random.default_rng(21 + seed).normal(0, 1, n), 5000) * np.minimum(1, t / 0.02) * np.exp(-t / 0.03) * 0.14
def ride(seed=0):
    n = int(0.9 * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) for f in (3150, 4420, 5320, 6890)) * 0.12
    s += hp(np.random.default_rng(31 + seed).normal(0, 1, n), 6000) * 0.35
    return s * np.exp(-t / 0.35) * 0.14

def vinyl(N, seed=9):
    rng = np.random.default_rng(seed)
    s = lp(rng.normal(0, 1, N), 3000) * 0.004
    pops = np.zeros(N); idx = rng.integers(0, N, N // 9000); pops[idx] = rng.uniform(0.05, 0.25, len(idx))
    return s + hp(pops, 1500)

def reverb(x, decay=1.6, wet=0.22, seed=4):
    n = int(decay * SR)
    ir = np.random.default_rng(seed).normal(0, 1, n) * np.exp(-np.arange(n) / SR / (decay / 4))
    ir = lp(ir, 5000); ir /= np.sqrt((ir ** 2).sum())
    return x * (1 - wet) + fftconvolve(x, ir)[: len(x)] * wet * 1.6

# ------------------------------------------------------------ styles
def _swing(beat_t, frac, amt):
    """frac = 0, 0.5 positions; amt 0.5 = straight, 0.66 = triplet swing"""
    return beat_t + (amt if abs(frac - 0.5) < 1e-6 else frac)

def style_lofi(dur):
    bpm = 78; b = 60 / bpm; T = Track(dur, 1)
    chords = [[57, 60, 64, 67], [55, 59, 62, 64], [53, 57, 60, 64], [52, 55, 59, 62]]
    roots = [41, 40, 38, 36]
    bar = 0
    while bar * 4 * b < dur:
        t0 = bar * 4 * b; c = chords[bar % 4]
        for j, m in enumerate(c):
            T.add(ep_piano(mf(m), 2.2, 0.9), t0 + 0.012 * j, 1.0, -0.2 + 0.13 * j)
        for j, m in enumerate(c[1:]):
            T.add(ep_piano(mf(m), 0.9, 0.6), t0 + b * 1.6 + 0.01 * j, 0.8, 0.2)
        r = roots[bar % 4]
        T.add(upright(mf(r), 0.9), t0, 1.0)
        T.add(upright(mf(r), 0.5, 0.8), t0 + b * 2.62, 1.0)
        T.add(upright(mf(r + 7), 0.4, 0.7), t0 + b * 3.3, 1.0)
        for k in (0, 2.62): T.add(kick(0.9), t0 + b * k, 1.0)
        for k in (1, 3): T.add(snare(True), t0 + b * k + 0.02, 0.9, 0.05)
        for k in range(8):
            tt = t0 + b * (k // 2) + (b * 0.6 if k % 2 else 0)
            T.add(hat(seed=k), tt, 0.7 if k % 2 else 1.0, 0.25)
        bar += 1
    L, R = T.L, T.R
    v = vinyl(T.N)
    L = lp(L, 4200) + v; R = lp(R, 4200) + v
    return L, R, 0.38

def style_jazz(dur):
    bpm = 116; b = 60 / bpm; T = Track(dur, 2); sw = 0.64
    chords = [[53, 57, 60, 64], [53, 57, 59, 64], [52, 55, 59, 62], [55, 59, 61, 66]]
    roots = [38, 43, 36, 45]
    bar = 0
    while bar * 4 * b < dur:
        t0 = bar * 4 * b; c = chords[bar % 4]; r = roots[bar % 4]; nr = roots[(bar + 1) % 4]
        walk = [r, r + (3 if bar % 4 in (0,) else 4), r + 7, nr + (1 if (bar % 2) else -1)]
        for k, m in enumerate(walk):
            T.add(upright(mf(m), b * 0.95, 0.9 if k else 1.0), t0 + b * k, 1.0, -0.1)
        for pos in (0, 1 + sw):
            for j, m in enumerate(c):
                T.add(piano(mf(m), 0.7 if pos else 1.2, 0.75), t0 + b * pos + 0.008 * j, 1.0, 0.25)
        for k in range(4):
            T.add(ride(k), t0 + b * k, 0.9, 0.35)
            if k in (1, 3): T.add(ride(k + 9), t0 + b * (k + sw), 0.6, 0.35)
            if k in (1, 3): T.add(brush(0.25, k), t0 + b * k, 1.0, -0.2)
        T.add(kick(0.35), t0, 1.0)
        bar += 1
    return T.L, T.R, 0.36

def style_folk(dur):
    bpm = 92; b = 60 / bpm; T = Track(dur, 3)
    chords = {'G': (43, [55, 59, 62, 67], 50), 'Em': (40, [55, 59, 64, 67], 47), 'C': (48, [55, 60, 64, 67], 43), 'D': (50, [57, 62, 66, 69], 45)}
    prog = ['G', 'Em', 'C', 'D']
    bar = 0
    while bar * 4 * b < dur:
        t0 = bar * 4 * b; root, tops, fifth = chords[prog[bar % 4]]
        for k in range(4):
            bass = root if k % 2 == 0 else fifth
            T.add(pluck(mf(bass), 1.6, 0.35, 0.995, seed=bar * 10 + k), t0 + b * k, 1.0, -0.15)
        pattern = [None, 2, 1, 3, None, 2, 0, 3]
        for k, pi in enumerate(pattern):
            if pi is None: continue
            T.add(lp(pluck(mf(tops[pi]), 1.4, 0.4, 0.994, seed=bar * 20 + k), 3800), t0 + b * (k * 0.5) + 0.01, 0.9, 0.2)
        T.add(upright(mf(root - 12 if root > 45 else root), 1.0, 0.8), t0, 0.7)
        for k in range(8):
            T.add(shaker(k), t0 + b * k * 0.5, 1.0 if k % 2 else 0.6, 0.4)
        bar += 1
    return T.L, T.R, 0.32

def style_bossa(dur):
    bpm = 132; b = 60 / bpm; T = Track(dur, 4)
    chords = [([52, 55, 59, 64], 36, 43), ([55, 61, 64], 45, 40), ([53, 57, 60, 64], 38, 45), ([53, 59, 62, 65], 43, 38)]
    bar = 0
    while bar * 4 * b < dur:
        t0 = bar * 4 * b; c, r, f5 = chords[(bar // 2) % 4]
        T.add(upright(mf(r), b * 1.4), t0, 0.6)
        T.add(upright(mf(f5), b * 0.5, 0.8), t0 + b * 1.5, 0.6)
        T.add(upright(mf(f5), b * 1.4, 0.9), t0 + b * 2, 0.6)
        T.add(upright(mf(r), b * 0.5, 0.8), t0 + b * 3.5, 0.6)
        for pos in ((0, 1.5, 3) if bar % 2 == 0 else (0.5, 2, 3.5)):
            for j, m in enumerate(c):
                T.add(pluck(mf(m), 0.7, 0.4, 0.993, seed=bar * 7 + j), t0 + b * pos + 0.006 * j, 1.5, 0.2)
        for pos in ((0, 0.75, 1.75, 2.5, 3.25) if bar % 2 == 0 else (0.5, 1.5, 2.25, 3.0)):
            T.add(rim(), t0 + b * pos, 0.6, -0.3)
        for k in range(16):
            T.add(shaker(k), t0 + b * k * 0.25, 0.9 if k % 4 == 2 else 0.45, 0.4)
        T.add(kick(0.25), t0, 1.0); T.add(kick(0.2), t0 + b * 2, 1.0)
        bar += 1
    return T.L, T.R, 0.3

def style_synth(dur):
    bpm = 96; b = 60 / bpm; T = Track(dur, 5)
    chords = [[57, 60, 64], [53, 57, 60], [48, 55, 60], [55, 59, 62]]
    roots = [45, 41, 36, 43]
    bar = 0
    while bar * 4 * b < dur:
        t0 = bar * 4 * b; c = chords[bar % 4]; r = roots[bar % 4]
        T.add(pad([mf(m) for m in c] + [mf(c[0] + 12)], 4 * b + 0.6, 0.5, 1600), t0, 1.0)
        arp = [c[0] + 12, c[1] + 12, c[2] + 12, c[1] + 24]
        for k in range(8):
            T.add(soft_square(mf(arp[k % 4]), 0.25), t0 + b * k * 0.5, 0.7, (-0.35, 0.35)[k % 2])
        for k in range(8):
            T.add(synth_bass(mf(r), b * 0.45), t0 + b * k * 0.5, 0.9 if k % 2 == 0 else 0.6)
        for k in (0, 2): T.add(kick(0.8), t0 + b * k, 1.0)
        for k in (1, 3): T.add(snare(), t0 + b * k, 0.55)
        for k in range(8): T.add(hat(seed=k), t0 + b * k * 0.5 + b * 0.25, 0.6, 0.3)
        bar += 1
    return T.L, T.R, 0.3

def style_ambient(dur):
    bpm = 84; b = 60 / bpm; T = Track(dur, 6)
    chords = [[57, 61, 62, 66], [57, 59, 62, 66], [55, 59, 62, 66], [57, 61, 64, 66]]
    roots = [38, 35, 43, 45]
    bar = 0
    while bar * 4 * b < dur:
        t0 = bar * 4 * b; c = chords[bar % 4]
        T.add(pad([mf(m) for m in c], 4 * b + 1.0, 1.2, 1100), t0, 1.2)
        T.add(upright(mf(roots[bar % 4]), 2.2, 0.8) * 0.9, t0, 0.8)
        seq = [c[1] + 12, c[3], c[2] + 12, c[0] + 12]
        for k, m in enumerate(seq):
            T.add(ep_piano(mf(m), 1.8, 0.55), t0 + b * (k + 0.5), 0.6, (-0.4, 0.4)[k % 2])
        for k in (1, 3): T.add(rim(), t0 + b * k, 0.35, 0.2)
        for k in range(8): T.add(shaker(k), t0 + b * k * 0.5, 0.5, -0.3)
        T.add(kick(0.45), t0, 1.0)
        bar += 1
    return T.L, T.R, 0.42

STYLES = {'lofi': style_lofi, 'jazz': style_jazz, 'folk': style_folk, 'bossa': style_bossa, 'synth': style_synth, 'ambient': style_ambient}

def render(style, dur, fades=True):
    L, R, wet = STYLES[style](dur)
    L = reverb(L, 1.8, wet, 4); R = reverb(R, 1.8, wet, 5)
    st = np.stack([L, R], 1)
    n = len(st)
    if fades:
        fade = np.ones(n)
        fi = int(0.5 * SR); fade[:fi] = np.linspace(0, 1, fi)
        fo = int(1.5 * SR); fade[-fo:] = np.linspace(1, 0, fo)
        st *= fade[:, None]
    rms = np.sqrt((st ** 2).mean()) + 1e-9
    st *= 0.12 / rms
    peak = np.abs(st).max()
    if peak > 0.95: st *= 0.95 / peak
    return st.astype(np.float32)

def style_for(index):
    """index 0 = next episode made"""
    return ROTATION[index % len(ROTATION)]
