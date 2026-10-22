# Variety Show Kinetic Captions (Hanazi)

**Original film**: Miaowu Diary EP.07 "Today's happiness" · 1080×1920 · 30 fps · 10 s · final AI jury score 7.64 / 10

**Source**: [demos/18-hanazi/](../demos/18-hanazi/)

## How to use

1. Make a new empty folder and open an AI assistant that can write code and run commands in it (for example Claude Code). The machine needs to render web pages (Node + Chrome) and have ffmpeg.
2. Copy the whole "Prompt" block below and send it.
3. To use your own content: change the story, brand name, copy and colours in `Creative seed`, or the size in `Output` (for example vertical 1080×1920). Do not delete the `Signature features` section: it is what makes the style recognisable at a glance.
4. To push it further: once the film is done, open another AI, review it with [rubric.md](../rubric.md), and paste the review back to the AI that made it for another round. The original films went through two such rounds.

## Prompt

```text
You are the director, motion designer, engineer and sound designer of ONE 10-second motion-design film.
The goal is the most classic, yet most stunning form of this style — award-shortlist / high-end commercial quality. A clean,
template-looking result is a fail. Benchmarks: Buck, ManvsMachine, Ordinary Folk, Giant Ant, Territory Studio, Apple keynote
motion, Pentagram motion identities, top Behance/Motionographer features, top Douyin/Bilibili designer accounts.

# Style
Variety Show Kinetic Captions (Hanazi)

# Output (fixed)
- 1080×1920, 30 fps, exactly 10.000 s (300 frames), H.264 MP4 with stereo AAC audio (48 kHz), mastered to −14 LUFS
  integrated, true peak ≤ −1 dBTP. Final file: video.mp4.

# Suggested technical route
HTML DOM/SVG: multi-layer text-stroke hanazi (花字, decorative variety-show caption) components + spring pops + SVG burst/sweat/sparkle decorations over a pet-vlog footage layer (CC0 photos with Ken Burns + handheld shake + punch-ins)
(You may choose a better route if it clearly raises quality; say why.)

# Creative seed
"Cute-pet variety vlog" Hanazi (花字) in its native habitat — reactive captions over a pet vlog.
- Base layer that feels like footage: CC0/PD cat or dog photos from /assets/images with slow Ken Burns, subtle handheld shake, snap punch-in zooms on 'moments' (you may also build a stylised scene if photos look weak).
- Hanazi moments synced to beats: title "今日份快乐" ("today's dose of happiness"; fill gradient + thick white stroke + coloured outer stroke + drop shadow, rounded heavy font), "？？？" bouncing question marks, "震惊!!" ("shocked!!") inside a radial 爆炸框 (explosion frame) with speed lines + 放射线 (radiating-line) flash, "（小声）" ("(whispering)") small aside, "绝绝子" ("absolutely amazing", slang) with sparkles, sweat drops, a "猫主子认证" ("certified by the cat boss") stamp.
- Motion: pop 0 → 1.15 → 1.0 in ~8 frames, per-character bounce with 2-frame stagger, slight rotation, gentle wiggle while holding; appear 2–3 frames after the audio/visual moment. High-saturation pink/yellow/cyan with white strokes.
Sound: bouncy variety-show bed (pizzicato/bass/claps) + boing, pop, ding, slide whistle, record scratch on '？？？'.

You are the director: you may change the concept, copy, story beats and brand names if you find a stronger idea, but the result must remain the CANONICAL, instantly-recognisable form of this style and must hit its signature features below.

# Signature features and key techniques (the result is judged against these)
Emotional decorative captions from TV variety-show post-production: multi-stroke rounded type with elastic entrances that changes colour and shape with the person's mood, paired with hit sound effects. It has spread down to vlogs, pet videos, interviews and comedy edits as a general packaging language; CapCut (剪映) ships many hanazi templates, and free hanazi style packs circulate on Bilibili.
Visual features multi-stroke rounded/chunky type, high-saturation clashing colours + white edge + drop shadow, elastic pop entrances, appearing with sound effects, hand-drawn decorative symbols (explosion frames / sweat drops / sparkles)
Key techniques Three-layer type structure: fill colour + thick white stroke + coloured outer stroke/shadow (in CSS, layered text-shadow or an SVG stroke)
Overshoot entrance: scale 0→1.15→1.0 (about 8 frames), or per-character bounce staggered 2 frames
Match the emotion: slanted handwriting for snark, radiating explosion frames for surprise, sweat drops for awkwardness
Time appearances to the punchline/sound effect; 2–3 frames after the voice feels more natural
Captions that stay on screen a long time get a slight wiggle to stay alive

# How to work
1. Treatment. Write down one clear idea: a hook in the first 0.5 s (never open on more than 0.3 s of empty or black), an
   escalation, one unmistakable hero moment at ~60–75 % of the runtime, and a composed end frame held ~0.8–1.2 s with living
   micro-motion. Map every signature feature above to a moment. Keep one cue sheet (beats and hit times) that both the
   picture and the sound read from.
2. Key frames before motion. Build the look, render stills at 6–10 key times and actually look at them. Each still should be
   poster-worthy: composition, hierarchy, negative space, type set properly (kerning, line-height, weight contrast, CJK
   punctuation, ~5 % safe margins). Iterate until nothing looks default, generic, cramped or "AI-template".
3. Motion. Build the choreography and preview at low resolution. Step through the fastest moves frame by frame: spacing,
   easing, arcs, overlap, anticipation and follow-through, motion blur. No unintended dead spans; the energy follows the music.
4. Sound. Write genre-correct music and sound design locked to the cue sheet. Check that visual hits land on audio onsets.
   Master to the output spec.
5. Final. Render at full resolution (motion blur where apt), then check: exactly 10.00 s, resolution, fps, audio present and at
   the right loudness, no black frames, no fallback fonts or tofu, no clipped elements at the frame edges, no shimmer on thin
   lines, no gradient banding. Fix and repeat until you would submit it to a festival.
6. Write an honest self-critique: what is strongest, what is weakest, what you would do with more time.

# Rules
- Rendering must be deterministic: every frame is a pure function of time t. Seeded randomness only; physics and particles
  precomputed or closed-form; no real-time clocks; no state-triggered CSS transitions. A reliable route: a web page that can
  draw any time t on request, captured frame by frame with a headless browser and encoded with ffmpeg (or a Blender script
  that renders a PNG sequence).
- Assets: only CC0 / public domain / OFL / Apache / free-for-commercial-use. Record each source and licence in CREDITS.md.
  No real brand trademarks; invent brand names.
- On-screen text must be correct and natural: idiomatic Chinese, proper CJK punctuation, no typos.

# Craft checklist (what a jury looks for)
- Style authenticity: an expert names the style in one second; every signature technique is present and executed correctly.
- Motion craft: purposeful easing (no linear unless mechanical by design), overlap and stagger, anticipation and
  follow-through, arcs, squash and stretch where the style allows, consistent physics, motion blur where apt; transitions
  carried by elements, not crossfades.
- Rhythm: hits locked to the music; contrast between busy and calm; no monotony.
- Design: strong composition, grid, typographic hierarchy, controlled palette; texture and finishing (grain, glow, vignette)
  only where the style wants it; nothing looks accidental.
- Technical polish: no jitter (unless intended), no popping, no aliasing, no banding, no fallback fonts, no half-loaded images.
- Sound: genre-correct, musical, synced, mastered.

# Before you deliver, score yourself honestly
1–10 on style fidelity, concept wow, motion craft, design & typography, finish & texture, sound & sync, technical
(6 = template-level, 8 = high-end agency, 9 = award shortlist). Aim for 9; fix whatever scores lowest first.

# Deliver
video.mp4, plus a short report: the concept in two sentences; a beat sheet with timecodes; how each signature feature is
realised; the tech route; check numbers (duration, resolution, fps, loudness, true peak); your honest top-3 weaknesses.
```
