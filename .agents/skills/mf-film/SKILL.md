---
name: mf-film
description: Make a new motion-design film in the motion-films repo (C:\Users\me\personal\motion-films, a fork of mg-styles-15) from one of its 15 style prompts — flat vector, line art, isometric, 3D, cel boil, collage, liquid, morph, Bauhaus, synthwave, aurora glass, hanazi captions, PaperClip sticker explainer, pixel art, HUD. Covers picking the style, rewriting the creative seed (own topic, Indonesian or English copy, 9:16 or 16:9, other lengths), building the film as a web page with renderAt(t), the code-made soundtrack, stills, the full render and the self-check. Use when the user says "make a film/video/clip in <style>", "use the paperclip/synthwave/... prompt", "mf film", or wants a new piece from this repo.
---

# Make a film from a style prompt

Repo: `C:\Users\me\personal\motion-films`. Run every command from the repo root.
If `.browsers/` or `.venv/` is missing, run the `mf-setup` skill first.

A film is a web page that draws any moment on request. The renderer captures it frame by
frame in headless Chrome, and ffmpeg adds the soundtrack that `audio.py` makes from code.
No image or video generation is used.

## 1. Agree the brief (one short message, then go)

Get or propose, in one message:
- **Style**: pick from [references/styles.md](references/styles.md). Match the topic to the
  style's "good for" column. Information content → `19-paperclip`, `03-isometric` or `01-flat-vector`.
- **Topic and copy**: the story in 3–5 beats, and the on-screen words. Default language for the
  user's own content is casual Indonesian; brand names are made up.
- **Format**: 1920×1080 or 1080×1920 (Shorts/Reels), 30 fps (24 for `04`, `05`), length.
  The originals are exactly 10 s. Longer works, but keep one idea per film and keep
  every second busy; 10–20 s is the sweet spot.
- **Slug**: `demos/my-<slug>/`. The `my-` prefix keeps new films apart from the 15 originals.

If the user already gave this, do not ask again.

## 2. Write the prompt

1. Copy `prompts/<style>.md` → `demos/my-<slug>/PROMPT.md`. Keep only the text inside the
   `Prompt` code block.
2. Change only these parts:
   - `# Output (fixed)`: size, fps, duration, frame count. Keep the loudness spec
     (−14 LUFS, true peak ≤ −1 dBTP).
   - `# Creative seed`: the new topic, beats per second, palette, copy, sound.
3. **Do not touch `# Signature features`.** It is what makes the style recognisable, and
   the review checks against it.
4. In `# Rules`, change "idiomatic Chinese, proper CJK punctuation" to the film's language.

## 3. Build it (follow PROMPT.md "How to work")

Read the original source `demos/<style>/` first and reuse its techniques, structure and
helpers. Do not copy its story. Files in `demos/my-<slug>/`:

| File | Content |
|---|---|
| `index.html` (+ `js/`) | The picture. Must follow the page contract below |
| `cues.json` | One cue sheet: `fps`, `bpm`, `key`, `build`, `drop`, `outro`, and `frames` {name: frame}. Picture AND sound read it |
| `audio.py` | Soundtrack with `lib/audio` (mgaudio). See below |
| `CREDITS.md` | Every outside asset with source and licence (CC0/OFL/Apache only) |
| `out/` | Renders (git-ignored) |

**Page contract** (from `harness/render.mjs`):
```js
window.DEMO = { width: 1080, height: 1920, fps: 30, duration: 10, motionBlur: { samples: 1, shutter: 0.5 } };
const cues = await (await fetch('/demos/my-<slug>/cues.json')).json();
await document.fonts.load("700 80px 'Inter'");   // every font + weight you use
await document.fonts.ready;
window.renderAt = async (t) => { /* draw the frame for time t (s); pure function of t */ };
await window.renderAt(0);
window.__ready = true;
```
- Every frame is a pure function of `t`: seeded random only, no `Date.now()`, no CSS
  transitions triggered by state, physics precomputed.
- Paths are from the repo root: `/assets/...`, `/node_modules/three/...`, `/demos/my-<slug>/...`.
- Fonts: use families in `assets/fonts/fonts.css` (link `/assets/fonts/fonts.css`). The free
  Latin ones (Inter, DM Sans, Sora, Poppins, Fredoka, Anton, Bebas Neue, Unbounded, JetBrains
  Mono, …) are installed. A missing font file can stop the page with `NetworkError`.
- Libraries in `node_modules`: three, d3, opentype.js, simplex-noise, topojson-client.
  GSAP is not installed; write easing by hand or `npm install gsap`.

**Soundtrack** (`lib/audio/README.md` has the full API):
```python
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib', 'audio'))
import mgaudio as mg
from mgaudio import recipes, sfx
cues = json.load(open(os.path.join(HERE, 'cues.json'))); T = lambda k: cues['frames'][k] / cues['fps']
m = recipes.for_style('<style-slug>', duration=10, drop=cues['drop'], outro=cues['outro'])
m.sfx(sfx.whoosh(0.5, 'swoosh'), at=T('enter'))        # pass the VISUAL event time
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
res = m.export(os.path.join(HERE, 'out/audio.wav'), lufs=-14, spectrogram=os.path.join(HERE, 'out/audio_spec.png'))
print(res['duration'], res['lufs'], res['true_peak'], res.get('warnings'))
```
The recipe for each style is in [references/styles.md](references/styles.md). Run it with
`.venv/Scripts/python demos/my-<slug>/audio.py`, then look at `out/audio_spec.png` and the warnings.

## 3b. Narration (films with a voice)

The shared tool `tools/tts/voice.py` makes `voice/voice.wav` + `voice/words.json` (per-word timings):
- `voice/narration.txt`: one paragraph per line, inline pause `[pause 400]` or studio's `<break time="500ms"/>`.
  From an infostudio/studio episode: `--from-script ../infostudio/episodes/<slug>/script.md` imports its `## Narasi`
  and voice (approved, fact-checked scripts make the best films).
- `voice/voice.json`: `{"provider": "auto", "voice": "id-ID-GadisNeural", "rate": "+10%", "lead": 0.25, "gap": 0.4}`.
  `auto` = Azure when `AZURE_SPEECH_KEY` is in `.env`, else the free Edge voice. Male voice: `id-ID-ArdiNeural`.
- Pronunciation: `tools/tts/lexicon.id.json` (shared: AI → "Ei Ai", ChatGPT, chatbot, keyboard …) plus
  `voice/lexicon.json` for the film (numbers, money: `"US$5.000": "lima ribu dolar"`). Captions keep the written text.
- `.venv/Scripts/python tools/tts/voice.py demos/my-<slug> --dry` shows what will be spoken; drop `--dry` to make it.
  Auto-fit: if the voice runs past `cues.json` duration minus `lead` and `end_hold` (1.5 s), it re-voices faster up to
  +20% (`max_rate`); still too long means trim the narration. `TTS_PROVIDER=edge` forces the free voice.
- **Time cues to words, not seconds**: in `cues.json` write `"@kasih"`, `"@pede#2"` (2nd occurrence), `"@terima.e"`
  (word end), `"@9,9+1.36"` (offset). The page resolves them with `import {resolveCues} from '/tools/tts/cues.mjs'`,
  `audio.py` with `from cues import load_cues` (`tools/tts/cues.py`). A new voice then re-syncs the whole film.
- Put the voice in the mix: `m.track('voice', level=-16, group='voice', hp=80).add(mg.as_sound(wav), 0.0)` and keep
  `music_level` around −27 (see `demos/my-ai-salah-yakin/audio.py`).

## 4. Look, then move, then finish

Use the `mf-render` skill for the commands.
1. **Key frames first**: stills at 6–10 key times. Open and look at every one. Fix what looks
   default, cramped, off-grid, clipped at the edges, or with wrong text. Repeat.
2. **Motion**: render at `--scale 0.5`, then check the fastest moves with close stills
   (e.g. every 2 frames around the hero moment).
3. **Sound**: run `audio.py`, then render full. The renderer picks up `out/audio.wav` by itself.
4. **Spec check** (see `mf-render`): duration, size, fps, loudness, no black frames.

## 5. Report and offer the review

Tell the user: the path `demos/my-<slug>/out/video.mp4`, the concept in two sentences, the beat
sheet with timecodes, the check numbers, and your honest top 3 weaknesses with a 1–10 self-score.
Then offer `mf-review` (a fresh juror + one revise round). The originals got +0.5 to +1 from
two rounds.

Commit `demos/my-<slug>/` (not `out/`) only when the user asks.
