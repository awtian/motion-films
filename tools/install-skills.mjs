#!/usr/bin/env node
// Copy the repo's mf-* skills (.agents/skills/mf-*) to the user-level skill folders, so every agent can use them:
//   ~/.agents/skills  — the shared location (Codex, OpenCode, Gemini CLI, Copilot and other agents read it)
//   ~/.claude/skills  — Claude Code
// Edit the skills in the repo, then run this again. Old copies of mf-* skills that no longer exist in the repo are removed.
//
// Usage: node tools/install-skills.mjs

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.join(ROOT, '.agents', 'skills');
const TARGETS = [path.join(os.homedir(), '.agents', 'skills'), path.join(os.homedir(), '.claude', 'skills')];

const skills = fs.readdirSync(SRC).filter((d) => d.startsWith('mf-') && fs.existsSync(path.join(SRC, d, 'SKILL.md')));
for (const dir of TARGETS) {
  fs.mkdirSync(dir, { recursive: true });
  for (const old of fs.readdirSync(dir).filter((d) => d.startsWith('mf-') && !skills.includes(d))) {
    fs.rmSync(path.join(dir, old), { recursive: true, force: true });
    console.log(`removed ${path.join(dir, old)}`);
  }
  for (const s of skills) {
    fs.rmSync(path.join(dir, s), { recursive: true, force: true });
    fs.cpSync(path.join(SRC, s), path.join(dir, s), { recursive: true });
  }
  console.log(`${dir}: ${skills.join(', ')}`);
}
