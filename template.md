# Writing a prompt for a new style

Every style prompt has a "shared part" and a "style-specific part". The shared part (the role setup at the top, plus How to work / Rules / Craft checklist /
Self-review / Deliver) is the same for every style; copy it from any `prompts/*.md`. To write a new style, you only fill in these four sections:

```text
# Style
<Style name>

# Output (fixed)
- <width>×<height>, <frame rate> fps, exactly 10.000 s, H.264 MP4 with stereo AAC audio (48 kHz), mastered to −14 LUFS integrated,
  true peak ≤ −1 dBTP. Final file: video.mp4.

# Suggested technical route
<The best route: SVG/Canvas/WebGL/Three.js/Blender… and the key implementation techniques.>
(You may choose a better route if it clearly raises quality; say why.)

# Creative seed
<"One-line film title" + the most classic yet most stunning reading of this style:
 - What happens from 0–X s (hook → escalation → climax → end frame),
 - Palette (3–6 exact colour values), type personality,
 - Sound: music genre + key sound effects.>

You are the director: you may change the concept, copy, story beats and brand names if you find a stronger idea, but the
result must remain the CANONICAL, instantly-recognisable form of this style and must hit its signature features below.

# Signature features and key techniques (the result is judged against these)
<Where this style comes from and what it is used for (one or two sentences)>
Visual features <comma-separated signature features>
Key techniques <actionable techniques, as specific as possible: curve parameters, frame counts, layer structure… one per line>
```

What makes a good one:
- **Signature features must be checkable.** Write "elastic overshoot with cubic-bezier(0.34,1.56,0.64,1), stagger 2–4 frames", not "the motion should feel bouncy".
- **The Creative seed needs beats.** Write the hook, escalation, climax and ending per second, or the AI makes a flat, template-like film.
- **Use made-up brand names and copy** to avoid trademark problems.
