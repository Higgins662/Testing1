---
name: pocketfuzzy-render
description: Make a finished Pocketfuzzy video (a loop cut by default) from an episode in a pack doc: preflight first, then animate, voice, score and render in the repo's pipeline.
---

# Pocketfuzzy render

Turns one scripted episode into a finished 1080×1920 MP4. Preflight always runs first. Start right away.

**Where things live**
- Repo `Higgins662/Testing1`, folder `vids/`: `render/` holds the pipeline (pf.py, pf_audio.py, pf_music.py, tts_lines.py, render.sh, setup.sh, ep_template.py and every past episode script). `tools/` holds preflight.py, outliers.py and doc_append.py. If the repo isn't in the workspace, attach it (add_repo, push access) and clone it.
- Pack docs, Google Docs in Drive > Vids: Vol 1 `1HzbLPTaOeejR0k-ONxX-A7aXOp04THam7c__-Ut4SV8`, Vol 2 `19YzBiI2QKU7u8OH4YY1N59oFuxfshdqptdVvwB991q0`, Vol 3 `1wCnpMhK70CSkXnAkmreZz-4uyQddc-XiOSG7eBUHadw` (new episodes from Ep 38 on).
- Queue sheet `1iurNV5lR9im3oFBPgyTrIpA94BxdnJtbhWeReQ-NWMc` (tabs `Queue` and `Runs`).
Load the google-workspace skill before any Docs or Sheets write.

## 1. Preflight (always)

Export the episode's pack doc with Drive `download_file_content` (exportMimeType `text/markdown`; the result is saved to a file), then run `python3 vids/tools/preflight.py <that file>` (it normalizes Google's export). Read the episode's row and fix before animating:
- Hook WEAK, a dealbreaker, or LEANS ON TREND: rewrite it (preflight skill rules), re-score, and write the fix into the pack doc with `replaceAllText`.
- Caption failures: fix the same way.
- VO outside 20–30s: cut the slowest line or add one concrete detail. Aim for 20–24s.
- Re-read the episode's **Never draw**, **Source** and **Accuracy guardrails**. Time-sensitive facts (prices, "this week", records, ages) get a web search today.
Stop and report instead of rendering if the hook still scores under 60 or a fact can't be confirmed.

## 2. Set up

`bash vids/render/setup.sh` (safe to re-run: it skips models and fonts already downloaded and copies the scripts into `/home/claude/eps`, where the scripts expect to run). Work in `/home/claude/eps`.

## 3. Write the loop cut

Loop cuts are the house default (Vol 1 Retention playbook): no end tag, no fades, the last line leads into the first, the last frame matches the first.

1. **Lines.** Write `epNN_lines.json` from the pack's voiceover: a list of `{"say": ..., "cap": ...}`, one per sentence. `say` is what the voice reads (spell out tricky words for TTS), `cap` is the on-screen caption. Make the last line a lead-in that completes with the first line ("So next time something's beeping outside at 3 AM, remember:" → "That car alarm at 3 AM might not be a car."). Keep to 6–9 lines.
2. **Voice.** `python3 tts_lines.py epNN <voice> <lang>` using the pack's voice: Michael `am_michael en-us`, Puck `am_puck en-us`, George `bm_george en-gb`, Lewis `bm_lewis en-gb`, Heart `af_heart en-us`, Emma `bf_emma en-gb`. It prints each line's length and the total; with gaps the video runs about total + 2s. Over 26s: trim lines and re-voice.
3. **Animate.** `cp ep_template.py epNN.py`, set `NAME = 'epNN'` and `STYLE` (the music style the queue assigned: folk, jazz, lofi, bossa, synth, ambient). Then replace the placeholder art and scenes:
   - Draw every character and object with `Pen` (poly, ell, line, dot, capsule, rrect) inside `make_sprite`, 3 seeds each for the hand-drawn boil. Backgrounds with `downsample(bg_canvas(...), W, H)`.
   - **Hook card (required):** set `HOOK` to the pack's **Hook overlay** (2–6 words; write one into the pack first if it's missing). pf draws it big in the upper third from frame 0 to 3.0s, and again over the loop seam. Don't draw other overlays before 3s, and make frame 0 show the subject mid-action, never an empty scene.
   - One scene per beat of the pack's shot list, using its visual prompts and on-screen text. After 3s, one big overlay per beat (≤3 words, upper third).
   - The Fuzz (`fuzz_sprites()`), armless and unchanged, appears at least once.
   - The last scene settles on exactly the first frame's background and pose (`pose(p)` with p = 0 at both ends).
   - Never draw anything on the episode's **Never draw** line, logos, real people, franchise characters, or the viral image.
   Study `ep16L.py`/`ep16.py` and `ep20L.py`/`ep20.py` for the level of detail that works: scenes have motion (ease, seg, lerp, boil, camera, shake, sparkle, glow), not static cards.
4. **Look before rendering.** `python3 epNN.py preview 0.0,<one time per scene>,LAST`, then view the JPGs in `epNN/` with Read. Check: `p_0.0` shows the hook card over the subject (the scroll-stopper), art is recognizable, overlays don't collide with captions, nothing off-canvas, and `p_0.0` vs the LAST frame match apart from captions. Fix and re-preview until it looks right. This is the step that decides quality; take two or three passes.
5. **Sound.** Edit `audio_plan()` so the SFX follow the shot list (pf_audio has rustle, whoosh, pop, chime, sparkles, tick, thud, wind, honk, whistle, crowd, scribble, stamp, brass, engine, slurp, splash, boing, flutter). Sounds that run past the end wrap to the start.

## 4. Render and check

```
cd /home/claude/eps && ./render.sh epNN pocketfuzzy_epNN_slug_loop
ffmpeg -y -loglevel error -i pocketfuzzy_epNN_slug_loop.mp4 -map 0:v -map 0:a -c:v copy -af volume=-6dB -c:a aac -b:a 192k pocketfuzzy_epNN_slug_loop.final.mp4 && mv pocketfuzzy_epNN_slug_loop.final.mp4 pocketfuzzy_epNN_slug_loop.mp4
```
A render takes several minutes; run it in the foreground with a long timeout. Then check with ffprobe (1080×1920, 20–30s, has audio) and pull 6 evenly spaced frames into one contact sheet to look at. If a render fails, read `epNN/w1.log`, `w2.log`, `audio.log`, fix, and retry once.

## 5. Save and hand over

- Commit `vids/render/epNN.py` and `epNN_lines.json` to `main` (never the MP4 or WAV files) with a short message.
- Send the MP4 to the user with SendUserFile, one line of context (episode, length, voice, music).
- Queue sheet: set the row's Status to `rendered`, fill Voice, Music, and Video (`<file name> (daily run <date>)`).
- Give the user the episode's caption and pinned comment from the pack, ready to paste. Never post anything yourself.
