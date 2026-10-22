---
name: mf-style
description: Write a prompt for a NEW motion-design style in the motion-films repo (C:\Users\me\personal\motion-films) using template.md — e.g. kinetic typography, glitch, grain/film, guochao, text-flash, sticker journal, data-viz, a channel's own house style — with a checkable Signature features section, a beat-by-beat Creative seed and a fitting mgaudio recipe; then optionally make the first film with it. Use when the user wants a style that is not one of the 15, "add a style", "make our own style", or "mf style".
---

# Write a new style prompt

Repo: `C:\Users\me\personal\motion-films`. Read `template.md` and one complete prompt
(`prompts/19-paperclip.md` is a good model) before you write.

## Steps

1. **Pin the style.** Get 2–3 reference examples from the user (links, channel names, or a
   description). Name the style in English. If it is close to one of the 15 styles
   (`mf-film` → `references/styles.md`), say so and suggest a variant of that prompt instead.
2. **Write the four style-specific sections** from `template.md`:
   - `# Style`: the name.
   - `# Output (fixed)`: size, fps, exact duration, the standard audio spec.
   - `# Suggested technical route`: a route that works in this repo (SVG/Canvas/WebGL/Three.js
     in a page with `renderAt(t)`; Blender only if 3D is essential).
   - `# Creative seed`: a one-line title + beats per second (hook ≤ 0.5 s → escalation → hero
     at 60–75 % → end frame held ~1 s), 3–6 hex colours, type personality, music + key SFX.
   - `# Signature features and key techniques`: where the style comes from, the visual features
     (comma list), and techniques that can be checked: curve values, frame counts, layer order,
     pixel sizes. "overshoot cubic-bezier(0.34,1.56,0.64,1), stagger 2–4 frames", not "bouncy".
3. **Copy the shared parts unchanged** from any prompt: the opening role paragraph, `How to
   work`, `Rules`, `Craft checklist`, the self-score and `Deliver`. Change only the language
   line in `Rules` if the copy is not Chinese.
4. **Pick the sound**: a recipe from `lib/audio/README.md` §2 that fits, plus 4–6 SFX names
   from §3.
5. **Save** as `prompts/<NN>-<slug>.md` (next free number ≥ 30), with the same header as the
   others: title line, a "How to use" section, and the prompt in a ```text block.
6. Show the user the Creative seed and Signature features. Offer to make the first film with
   `mf-film`.

Use made-up brand names. Assets must be CC0 / public domain / OFL / Apache.
