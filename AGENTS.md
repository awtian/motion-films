# motion-films — notes for coding agents

Personal fork of [Vincentwei1021/mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15) (MIT): 15 motion-design
styles, each a 10-second film that an AI made by writing code. Windows 11, Git Bash.

## Skills (in `.agents/skills/`, installed globally with `node tools/install-skills.mjs`)

| Skill | Use it to |
|---|---|
| `mf-setup` | set up or check the machine, pull upstream changes, reinstall the skills |
| `mf-film` | make a new film from a style prompt (`references/styles.md` lists the 15 styles) |
| `mf-render` | render stills/previews/the final MP4, check the spec, fix render failures |
| `mf-review` | have an independent juror score a film with `rubric.md`, then revise |
| `mf-style` | write a prompt for a new style with `template.md` |

## Rules

- New films go in `demos/my-<slug>/`. Do not change the 15 originals in `demos/` unless asked.
- A film page draws any time t on request (`window.renderAt(t)`, `window.__ready`); every frame is a pure function of t.
- Use `.venv/Scripts/python` for `audio.py` and Chrome for Testing in `.browsers/` (not Edge or Firefox).
- Edit skills in `.agents/skills/`, never in the installed copies, then run `node tools/install-skills.mjs`.
- Assets: CC0 / public domain / OFL / Apache only, listed in the film's `CREDITS.md`. Made-up brand names.
