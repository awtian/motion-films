// Resolve word references in a cue sheet against voice/words.json (browser and Node).
//   "@kasih"        start of the first written word "kasih" (exact text, case-sensitive)
//   "@pede#2"       start of its 2nd occurrence
//   "@terima.e"     end instead of start
//   "@9,9+1.36"     with an offset in seconds (+ or -)
// Numbers stay numbers. Arrays and objects are resolved recursively. Same rules as tools/tts/cues.py.
export function wordTime(words, ref) {
  const m = /^@(.+?)(?:#(\d+))?(\.e)?([+-]\d+(?:\.\d+)?)?$/.exec(ref);
  if (!m) throw new Error(`bad word ref ${ref}`);
  const [, text, nth, end, off] = m;
  const hits = words.filter((w) => w.text === text);
  const w = hits[(+nth || 1) - 1];
  if (!w) throw new Error(`word ref ${ref}: "${text}" occurs ${hits.length}x in words.json`);
  return +((end ? w.e : w.s) + (off ? +off : 0)).toFixed(3);
}

export function resolveCues(v, words) {
  if (typeof v === 'string' && v.startsWith('@')) return wordTime(words, v);
  if (Array.isArray(v)) return v.map((x) => resolveCues(x, words));
  if (v && typeof v === 'object') return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, resolveCues(x, words)]));
  return v;
}
