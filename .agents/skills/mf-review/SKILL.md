---
name: mf-review
description: Jury review and revise loop for a film in the motion-films repo (C:\Users\me\personal\motion-films) using its rubric.md — a fresh, harsh juror scores the film 1–10 on style fidelity, concept, motion, design, finish, sound and technical, lists timecoded fixes, then the film is revised and re-rendered, for one or more rounds. Use when the user says "review it", "judge it", "score it", "make it better", "another round", "mf review", or a film from this repo is done and needs to go up a level.
---

# Review and revise

Repo: `C:\Users\me\personal\motion-films`. Prompts: `rubric.md` (Step 1 = review, Step 2 = revise).
The originals went make → review → revise twice; each round added roughly +0.3 to +0.7.

## The juror must be independent

The juror must not be the session that made the film. It must not see your notes or your
self-score. Use a separate agent with a fresh context: a subagent in this harness, or in
T3 Code a `delegate_task` child. Give it only:
1. The `rubric.md` Step 1 prompt, with `<path to video.mp4>` filled in (absolute path).
2. The film's `PROMPT.md` (or its Style, Output and Signature features sections).
3. One tool hint: "Use ffmpeg/ffprobe for frames and loudness (the commands are in the
   mf-render skill); Read the PNGs to look at them."

Ask for the output format from the rubric: scores per dimension, the overall score, strengths,
and 5–10 fixes ordered by impact, each with timecodes. Save it as
`<dir>/reviews/round-N.md`.

If no separate agent is available, tell the user and offer the manual way: open a new session
and paste the Step 1 prompt.

## Revise (rubric Step 2)

1. Keep the current version: copy `<dir>/out/video.mp4` → `<dir>/out/v<N>.mp4`. Commit the
   source or copy it to `<dir>/versions/v<N>/` so a regression can be undone.
2. Fix every critical and high-impact item. You may use a better fix than the juror's if you
   are sure, and say why. Do not break anything the juror listed as a strength.
3. Re-render stills around each fixed timecode and look at them, then render full and
   re-run the spec check (`mf-render`).
4. Report a short table: fix → applied / changed / skipped (why).

## When to stop

- Stop when the user is happy, after 2 rounds by default, or when a round gains < 0.2.
- If two rounds in a row flag the same deep problem (concept, wrong style choice, layout),
  say so plainly. A redesign of that part beats more polish.
- Report the score history: `round | main changes | score`.
