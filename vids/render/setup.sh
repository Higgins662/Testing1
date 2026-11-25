#!/bin/bash
# Pocketfuzzy render setup: run once in a fresh Linux workspace.
# Episodes are hand-animated in Python (PIL) on the shared library in pf.py,
# voiced with Kokoro TTS (tts_lines.py), scored by pf_music.py and assembled by render.sh.
#
# Per episode:   python3 tts_lines.py ep32 af_heart en-us        # voices: am_michael am_puck bm_george bm_lewis af_heart bf_emma
#                python3 ep32.py preview 1.0,5.0,12.0            # check key frames in ep32/
#                ./render.sh ep32 pocketfuzzy_ep32_mustache_joke
# Then lower the finished file 6 dB to match the posted episodes:
#   ffmpeg -i X.mp4 -map 0:v -map 0:a -c:v copy -af volume=-6dB -c:a aac -b:a 192k X.final.mp4
# The scripts expect to live in /home/claude/eps (paths are hard-coded there).
set -e
pip install --break-system-packages -q kokoro-onnx soundfile scipy numpy pillow
mkdir -p /home/claude/tts /home/claude/vid /home/claude/eps
cd /home/claude/tts
curl -sL -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
curl -sL -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
cd /tmp && npm pack @fontsource/luckiest-guy@5.3.0 @fontsource/patrick-hand@5.3.0 >/dev/null
tar xzf fontsource-luckiest-guy-5.3.0.tgz && cp package/files/luckiest-guy-latin-400-normal.woff /home/claude/vid/lucky.woff && rm -rf package
tar xzf fontsource-patrick-hand-5.3.0.tgz && cp package/files/patrick-hand-latin-400-normal.woff /home/claude/vid/patrick.woff && rm -rf package
cp "$(dirname "$0")"/*.py "$(dirname "$0")"/*.json "$(dirname "$0")"/render.sh /home/claude/eps/ 2>/dev/null || true
echo "setup done"
