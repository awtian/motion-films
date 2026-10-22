# The 15 styles

Prompt: `prompts/<slug>.md` · original source: `demos/<slug>/` · film: `videos/<slug>.mp4`.
Score = final AI-jury score of the original (out of 10). Audio = `recipes.for_style('<slug>')` default, then the alternative.

| slug | style | original | good for | route | audio (default / alt) |
|---|---|---|---|---|---|
| `01-flat-vector` | Flat vector 2D | 16:9 30 fps · 7.64 | product promo, app/SaaS explainer, friendly brand | SVG, elastic eases, shape wipes | `pop` / `future_bass` |
| `02-line-art` | Line art, one continuous line | 16:9 30 fps · 7.64 | premium brand, logo reveal, architecture, calm story | SVG stroke-dashoffset, camera follows the pen tip | `ambient(piano)` / `explainer` |
| `03-isometric` | Isometric 2.5D | 16:9 30 fps · 8.00 | how a system works, architecture, data centre, city | Three.js orthographic camera or SVG SSR faces | `explainer` / `pop` |
| `04-3d-render` | 3D render (C4D/Blender look) | 16:9 24 fps · 7.71 | product hero, premium ident | **Blender** CLI → PNG sequence (+ HTML type layer). Needs Blender | `pop(bpm=118)` / `ambient(product)` |
| `05-cel-boil` | Frame-by-frame / line boil | 16:9 24 fps · 8.07 | playful character moment, hand-made feel | Canvas2D brush renderer, 3–4 boil variants on 2s | `lofi(piano)` / `variety` |
| `06-collage` | Collage / cut-out | 16:9 30 fps · 8.14 | editorial, opinion, culture, music | DOM/Canvas PNG cutouts (rembg), halftone, 12 fps stepped | `lofi(boombap)` / `vaporwave` |
| `07-liquid` | Liquid motion | 16:9 30 fps · 7.57 | drinks, energetic logo, transitions | WebGL2 SDF metaballs | `future_bass` / `lofi` |
| `08-morph` | Shape morph | 16:9 30 fps · 7.64 | "one idea becomes the next", feature chain | SVG + flubber-style vertex matching | `future_bass(bpm=140)` / `techno` |
| `09-bauhaus` | Geometric / Bauhaus | 16:9 30 fps · 7.71 | kinetic poster, event, music, abstract brand | SVG/Canvas on a strict grid, beat-driven | `techno` / `explainer` |
| `10-synthwave` | 80s synthwave / VHS | 16:9 30 fps · 8.21 | retro, gaming, nostalgia, music | WebGL grid/sun/mountains + chrome text + VHS pass | `synthwave` / `darksynth` |
| `12-aurora-glass` | Aurora + glassmorphism | 16:9 30 fps · 8.07 | AI/tech product launch, calm premium | WebGL aurora shader + CSS backdrop-filter glass cards | `ambient(glass)` / `future_bass` |
| `18-hanazi` | Variety-show captions | **9:16** 30 fps · 7.64 | vlog, pet, reaction, comedy Shorts | DOM/SVG multi-stroke text + spring pops over photos | `variety` / `pop` |
| `19-paperclip` | Sticker explainer (PaperClip) | 16:9 30 fps · 7.71 | **data/infographic explainers**, facts, finance, science | one giant canvas + camera, SVG charts, white-outline photo stickers | `explainer` / `pop` |
| `20-pixel` | Pixel art / 8-bit | 16:9 30 fps · 8.07 | gaming, retro, playful tutorial | Canvas 320×180 ×6 nearest-neighbour, sprites in code | `chiptune` |
| `22-hud` | Cyberpunk HUD / FUI | 16:9 30 fps · 7.93 | tech, security, space, data, "AI scanning" | SVG/Canvas FUI layers + Three.js wireframe, glow/scanlines | `darksynth` |

Notes
- 9:16 from a 16:9 style: rethink the layout for a tall frame (stack, bigger type, keep the
  bottom ~20 % and the right edge free of key content for Shorts UI). Do not just crop.
- The hardest to run here: `04-3d-render` (Blender), `06-collage` (rembg needs the full
  `requirements.txt`). All others need only Node, Chrome, ffmpeg and the audio venv.
- Chinese-copy originals (`18`, `19`, `20`, `22`, `01` tagline) need CJK fonts. A new film in
  Indonesian or English does not.
