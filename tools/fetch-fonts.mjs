#!/usr/bin/env node
// Download the free fonts the films use (Google Fonts, OFL/Apache) to the paths in assets/fonts/README.md.
// The CJK vendor fonts and the static cuts come from tools/fetch-cjk-fonts.sh.
//
// Usage: node tools/fetch-fonts.mjs [--force]

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const GF = 'https://raw.githubusercontent.com/google/fonts/main/';
const force = process.argv.includes('--force');

// target path (from the repo root) → file in github.com/google/fonts
const FONTS = {
  'assets/fonts/latin/anton/Anton-Regular.ttf': 'ofl/anton/Anton-Regular.ttf',
  'assets/fonts/latin/archivo/Archivo-Italic-VF.ttf': 'ofl/archivo/Archivo-Italic[wdth,wght].ttf',
  'assets/fonts/latin/bebasneue/BebasNeue-Regular.ttf': 'ofl/bebasneue/BebasNeue-Regular.ttf',
  'assets/fonts/latin/caveat/Caveat-VF.ttf': 'ofl/caveat/Caveat[wght].ttf',
  'assets/fonts/latin/chakrapetch/ChakraPetch-SemiBold.ttf': 'ofl/chakrapetch/ChakraPetch-SemiBold.ttf',
  'assets/fonts/latin/cormorantgaramond/CormorantGaramond-VF.ttf': 'ofl/cormorantgaramond/CormorantGaramond[wght].ttf',
  'assets/fonts/latin/dmsans/DMSans-VF.ttf': 'ofl/dmsans/DMSans[opsz,wght].ttf',
  'assets/fonts/latin/fredoka/Fredoka-VF.ttf': 'ofl/fredoka/Fredoka[wdth,wght].ttf',
  'assets/fonts/latin/ibmplexmono/IBMPlexMono-Medium.ttf': 'ofl/ibmplexmono/IBMPlexMono-Medium.ttf',
  'assets/fonts/latin/ibmplexmono/IBMPlexMono-SemiBold.ttf': 'ofl/ibmplexmono/IBMPlexMono-SemiBold.ttf',
  'assets/fonts/latin/instrumentserif/InstrumentSerif-Italic.ttf': 'ofl/instrumentserif/InstrumentSerif-Italic.ttf',
  'assets/fonts/latin/instrumentserif/InstrumentSerif-Regular.ttf': 'ofl/instrumentserif/InstrumentSerif-Regular.ttf',
  'assets/fonts/latin/inter/Inter-VF.ttf': 'ofl/inter/Inter[opsz,wght].ttf',
  'assets/fonts/latin/jetbrainsmono/JetBrainsMono-VF.ttf': 'ofl/jetbrainsmono/JetBrainsMono[wght].ttf',
  'assets/fonts/latin/luckiestguy/LuckiestGuy-Regular.ttf': 'apache/luckiestguy/LuckiestGuy-Regular.ttf',
  'assets/fonts/latin/michroma/Michroma-Regular.ttf': 'ofl/michroma/Michroma-Regular.ttf',
  'assets/fonts/latin/poppins/Poppins-Black.ttf': 'ofl/poppins/Poppins-Black.ttf',
  'assets/fonts/latin/poppins/Poppins-SemiBold.ttf': 'ofl/poppins/Poppins-SemiBold.ttf',
  'assets/fonts/latin/pressstart2p/PressStart2P-Regular.ttf': 'ofl/pressstart2p/PressStart2P-Regular.ttf',
  'assets/fonts/latin/rajdhani/Rajdhani-Bold.ttf': 'ofl/rajdhani/Rajdhani-Bold.ttf',
  'assets/fonts/latin/rajdhani/Rajdhani-SemiBold.ttf': 'ofl/rajdhani/Rajdhani-SemiBold.ttf',
  'assets/fonts/latin/sora/Sora-VF.ttf': 'ofl/sora/Sora[wght].ttf',
  'assets/fonts/latin/unbounded/Unbounded-VF.ttf': 'ofl/unbounded/Unbounded[wght].ttf',
  'assets/fonts/latin/vt323/VT323-Regular.ttf': 'ofl/vt323/VT323-Regular.ttf',
  'assets/fonts/cjk/notosanssc/NotoSansSC-VF.ttf': 'ofl/notosanssc/NotoSansSC[wght].ttf',
  'assets/fonts/cjk/notoserifsc/NotoSerifSC-VF.ttf': 'ofl/notoserifsc/NotoSerifSC[wght].ttf',
  'assets/fonts/cjk/longcang/LongCang-Regular.ttf': 'ofl/longcang/LongCang-Regular.ttf',
  'assets/fonts/cjk/zcoolkuaile/ZCOOLKuaiLe-Regular.ttf': 'ofl/zcoolkuaile/ZCOOLKuaiLe-Regular.ttf',
  'demos/10-synthwave/assets/fonts/MrDafoe-Regular.ttf': 'ofl/mrdafoe/MrDafoe-Regular.ttf',
};


let ok = 0, failed = 0;
for (const [dst, src] of Object.entries(FONTS)) {
  const out = path.join(ROOT, dst);
  if (!force && fs.existsSync(out)) { ok++; continue; }
  const url = GF + src.split('/').map(encodeURIComponent).join('/');
  const res = await fetch(url);
  if (!res.ok) { console.log(`FAIL ${res.status} ${src}`); failed++; continue; }
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, Buffer.from(await res.arrayBuffer()));
  console.log(`ok   ${dst}`);
  ok++;
}
console.log(`\n${ok} fonts in place, ${failed} failed.`);
console.log('The CJK vendor fonts and the static cuts come from tools/fetch-cjk-fonts.sh (npm run setup:fonts runs both).');
