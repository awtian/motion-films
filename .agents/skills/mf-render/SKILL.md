---
name: mf-render
description: Render, preview and check films in the motion-films repo (C:\Users\me\personal\motion-films) — stills at given times, low-res motion previews, the full MP4 with sound, the browser scrubber, contact sheets, and the spec check (duration, size, fps, loudness, true peak, black frames). Also fixes render failures (NetworkError from missing fonts, no Chrome, WebGL/GPU, page never ready, audio missing). Use when the user wants to render, re-render, preview, scrub, check or "see" a film from this repo, or a render fails.
---

# Render, preview and check

Repo: `C:\Users\me\personal\motion-films`. Run from the repo root. `<dir>` is e.g.
`demos/my-<slug>` or `demos/10-synthwave`.

## Commands

| Goal | Command |
|---|---|
| Stills (PNG → `<dir>/out/stills/`) | `node harness/render.mjs <dir> --stills 0.5,2,4.25,7,9.5` |
| Fast motion preview | `node harness/render.mjs <dir> --scale 0.5 --noaudio --out <dir>/out/preview.mp4` |
| Part of the film | `... --from 3 --to 6` |
| Full render with sound | `.venv/Scripts/python <dir>/audio.py` then `node harness/render.mjs <dir>` → `<dir>/out/video.mp4` |
| Stronger motion blur | `... --mb 4 --shutter 0.5` (slower; use on the final only) |
| Scrub in the browser | `python -m http.server 8000`, open `http://localhost:8000/harness/preview.html?demo=<name>` (films under `demos/` only) |

Other flags: `--crf 14`, `--w --h --fps --duration` (override `window.DEMO`), `--workers N`,
`--audio path.wav`, `--query k=v`. A 10 s 1080p 2D film renders in ~20 s; WebGL takes longer.

**Always open the stills you render** (Read the PNGs) before you say a frame is fine.

## Contact sheet and close looks

```bash
ffmpeg -v error -y -i <dir>/out/video.mp4 -vf "fps=2,scale=480:-1,tile=5x4" -frames:v 1 <dir>/out/contact.png
ffmpeg -v error -y -ss 6.0 -t 0.5 -i <dir>/out/video.mp4 -vf "scale=640:-1,tile=5x3" -frames:v 1 <dir>/out/strip.png
```

## Spec check

```bash
ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate:format=duration -of compact <dir>/out/video.mp4
ffmpeg -nostats -i <dir>/out/video.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
ffmpeg -nostats -i <dir>/out/video.mp4 -vf blackdetect=d=0.1:pix_th=0.05 -an -f null - 2>&1 | grep black_start
```
Pass: duration = spec (10.000 s by default), size and fps as in `window.DEMO`, an audio stream,
I ≈ −14 LUFS (±1), true peak ≤ −1 dBTP, no black spans you did not plan.

## When it fails

| Symptom | Cause → fix |
|---|---|
| `[page error] NetworkError` and nothing renders | A font file is missing. `npm run setup:fonts`. For CJK fonts see `assets/fonts/README.md`. Find which with `rg "fonts.load" <dir>` |
| `No Chrome found` | `npm run setup:chrome`, or set `MG_CHROME=<path to chrome.exe>` |
| Hangs on `__ready` (5 min timeout) | The page threw before `window.__ready = true`. Run with `VERBOSE=1` to see console output; check fetch paths start at the repo root (`/demos/...`) |
| WebGL black or slow | GPU flags. Windows default is `--use-angle=d3d11`. Try `MG_GPU_ARGS="--use-angle=swiftshader"` (software) to tell a GPU problem from a code problem |
| Video has no sound | No `<dir>/out/audio.wav`. Run `audio.py` first, or pass `--audio` |
| `ModuleNotFoundError: numpy` | Use `.venv/Scripts/python`, not the system Python. If `.venv` is missing, run `mf-setup` |
| Frames differ run to run | Something in the page is not a pure function of t (Date, Math.random, CSS transitions) |
