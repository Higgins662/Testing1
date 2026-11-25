import soundfile as sf, json, sys, numpy as np
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/tts/kokoro-v1.0.onnx', '/home/claude/tts/voices-v1.0.bin')
ep, voice, lang = sys.argv[1], sys.argv[2], sys.argv[3]; sp = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
lines = json.load(open(f'{ep}_lines.json'))
durs = []
for i, t in enumerate(lines):
    a, sr = k.create(t['say'], voice=voice, speed=sp, lang=lang)
    idx = np.where(np.abs(a) > 0.012)[0]
    s, e = max(0, idx[0] - int(0.02 * sr)), min(len(a), idx[-1] + int(0.06 * sr))
    sf.write(f'{ep}_vo_{i}.wav', a[s:e], sr); durs.append(round((e - s) / sr, 3))
json.dump(durs, open(f'{ep}_durs.json', 'w'))
print(ep, durs, round(sum(durs), 2))
