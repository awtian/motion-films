---
name: mf-setup
description: Set up, check or update the motion-films repo (C:\Users\me\personal\motion-films, a personal fork of Vincentwei1021/mg-styles-15) on this Windows machine — npm packages, Chrome for Testing, fonts, the Python audio venv, ffmpeg, optional Blender — run a health check, pull changes from the upstream repo, and reinstall the mf-* skills to every agent. Use when the user says "set up motion-films", "it doesn't render", "check my setup", "update from upstream/Vincent", "install/sync the mf skills", or on first use of the repo.
---

# Setup, health check and updates

Repo: `C:\Users\me\personal\motion-films`. Windows 11, Git Bash. Run from the repo root.

## Health check (run first, fix only what fails)

```bash
node -v; ffmpeg -version | head -1
ls node_modules/puppeteer-core >/dev/null && echo npm-ok
ls .browsers/chrome/*/*/chrome.exe
ls assets/fonts/latin | wc -l          # 20 folders when the free fonts are in
.venv/Scripts/python -c "import numpy, scipy, numba, pedalboard, librosa; print('audio-ok')"
command -v blender || ls "/c/Program Files/Blender Foundation"
```

## Install what is missing

| Missing | Fix |
|---|---|
| npm packages | `npm install` |
| Chrome | `npm run setup:chrome` (Chrome for Testing in `.browsers/`, git-ignored). Do not use Edge or Firefox |
| Fonts | `npm run setup:fonts` (29 free Google Fonts). The CJK vendor fonts are manual; links are printed at the end and paths are in `assets/fonts/README.md`. Only needed for the Chinese-copy originals |
| Audio venv | `python -m venv .venv` then `.venv/Scripts/python -m pip install --only-binary=:all: numpy scipy soundfile numba pedalboard pyloudnorm librosa matplotlib`. The exact pins in `requirements.txt` include one with no Windows wheel (it tries to compile and fails), so use current wheels. The sound can differ by a hair from the originals; that does not matter for new films |
| Asset tools (only for `06-collage`-style cutouts) | `.venv/Scripts/python -m pip install --only-binary=:all: pillow fonttools scikit-image opencv-python rembg` |
| Blender (only for the 3D style) | `winget install BlenderFoundation.Blender`, then see `demos/04-3d-render/README.md` |

Ask before a large install (Blender, rembg). Then prove it works:
```bash
.venv/Scripts/python demos/01-flat-vector/audio.py
node harness/render.mjs demos/01-flat-vector     # → demos/01-flat-vector/out/video.mp4 with sound
```

## Pull updates from the original repo

`upstream` = `https://github.com/Vincentwei1021/mg-styles-15` (add it with
`git remote add upstream <url>` if `git remote -v` does not show it).
```bash
git fetch upstream && git log --oneline main..upstream/main
git merge upstream/main
```
The prompts, `rubric.md`, `template.md` and `assets/fonts/README.md` were translated in place, so
upstream edits to them conflict. Resolve by keeping the English text and translating the
upstream change. Keep the fork notice and "Changes in this fork" in `README.md`.
Push to `origin main` only when the user asks.

## Reinstall the mf-* skills everywhere

The skills live in the repo at `.agents/skills/mf-*` (edit them there). Copy them to every agent:
```bash
node tools/install-skills.mjs
```
It copies to `~/.agents/skills` (Codex, OpenCode, Gemini CLI, Copilot and other agents) and
`~/.claude/skills` (Claude Code). Do not also copy to `~/.codex/skills`: Codex would list each
skill twice. A running session loads new or changed skills only after a restart.
