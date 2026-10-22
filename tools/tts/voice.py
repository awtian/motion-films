"""Narration for a film: text -> <film>/voice/voice.wav + <film>/voice/words.json (word timings for picture and captions).

Providers
  azure  Azure AI Speech (neural voices, e.g. id-ID-GadisNeural / id-ID-ArdiNeural). Needs AZURE_SPEECH_KEY and
         AZURE_SPEECH_REGION in the environment or in the repo's .env. Free tier F0: 0.5 M characters a month.
  edge   Microsoft Edge read-aloud (same voices, no key, no SSML, a little less control). Fallback.
  auto   azure when a key is set, else edge (default).

Input, all in <film>/voice/
  narration.txt  one paragraph per line. Inline pause: [pause 400] (ms). Lines starting with # are ignored.
  voice.json     optional: {"provider", "voice", "rate", "pitch", "edge_pitch", "lead", "gap", "lexicon"}
                 gap = pause after each paragraph in seconds (number, or a list per paragraph)
  lexicon.json   optional per-film pronunciations, merged over tools/tts/lexicon.id.json

Pronunciation: the lexicon maps what is written (and shown in captions) to what is spoken, e.g. "AI" -> "Ei Ai".
The spoken words are aligned back to the written words, so words.json keeps the written text.

Usage (from the repo root):
  .venv/Scripts/python tools/tts/voice.py demos/my-film [--provider azure|edge|auto] [--voice ...] [--rate +10%] [--dry]
  .venv/Scripts/python tools/tts/voice.py --list-voices id-ID      (azure: list the voices for a locale)
"""
import argparse, asyncio, difflib, io, json, os, re, subprocess, sys, tempfile
from xml.sax.saxutils import escape
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SR = 48000
DEFAULTS = {'provider': 'auto', 'voice': 'id-ID-GadisNeural', 'rate': '+10%', 'pitch': '+0%', 'lead': 0.25, 'gap': 0.4}
PUNCT = '.,?!:;…'
QUOTES = '"“”\'‘’()[]'


def load_env():
    p = os.path.join(ROOT, '.env')
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            m = re.match(r'\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*?)\s*$', line)
            if m and not os.environ.get(m.group(1)):
                os.environ[m.group(1)] = m.group(2).strip('"\'')


# ---------- text: paragraphs -> segments -> written tokens -> spoken words ----------
def read_narration(path):
    paras = []
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if line and not line.startswith('#'):
            paras.append(line)
    return paras


def segments(para):
    """'a b [pause 300] c' -> [('a b', 0.3), ('c', 0.0)]"""
    out, pos = [], 0
    for m in re.finditer(r'\[pause\s+(\d+)\]', para):
        out.append((para[pos:m.start()].strip(), int(m.group(1)) / 1000)); pos = m.end()
    out.append((para[pos:].strip(), 0.0))
    return [(t, p) for t, p in out if t] or [('', 0.0)]


def core(tok):
    """written token -> (lead, core, trail): '"terima"' -> ('"', 'terima', '"'), 'salah,' -> ('', 'salah', ',')"""
    m = re.match(r'^([%s]*)(.*?)([%s%s]*)$' % (re.escape(QUOTES), re.escape(QUOTES), re.escape(PUNCT)), tok)
    return m.group(1), m.group(2), m.group(3)


def spoken_plan(text, lex):
    """Tokens of one segment with their spoken form. Multi-word lexicon keys match greedily (longest first)."""
    toks = text.split()
    keys = sorted(lex, key=lambda k: -len(k.split()))
    plan, i = [], 0
    while i < len(toks):
        hit = None
        for k in keys:
            kw = k.split(); n = len(kw)
            if i + n <= len(toks) and [core(t)[1] for t in toks[i:i + n]] == kw:
                hit = (k, n); break
        if hit:
            k, n = hit
            group = toks[i:i + n]
            plan.append({'written': [core(t)[1] for t in group], 'trail': core(group[-1])[2], 'say': lex[k] + core(group[-1])[2]})
            i += n
        else:
            l, c, t = core(toks[i])
            plan.append({'written': [c], 'trail': t, 'say': toks[i]})
            i += 1
    return plan


norm = lambda w: re.sub(r'[^\w]', '', w.lower())


def align(plan, bounds):
    """Map provider word boundaries [(text, s, e)] back to the written tokens of `plan` -> [{text, s, e}]."""
    exp, owner = [], []          # expected spoken words and which plan item owns each
    for pi, p in enumerate(plan):
        for w in p['say'].split():
            if norm(w):
                exp.append(norm(w)); owner.append(pi)
    got = [norm(b[0]) for b in bounds]
    hits = [[] for _ in plan]
    sm = difflib.SequenceMatcher(a=exp, b=got, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1): hits[owner[i1 + k]].append(bounds[j1 + k])
        elif tag == 'replace':
            for j in range(j1, j2):
                hits[owner[i1 + (j - j1) * (i2 - i1) // (j2 - j1)]].append(bounds[j])
        elif tag == 'insert' and i1 > 0:
            for j in range(j1, j2): hits[owner[i1 - 1]].append(bounds[j])
    times = [(min(b[1] for b in h), max(b[2] for b in h)) if h else None for h in hits]
    for i, t in enumerate(times):            # tokens the provider did not report: fill from the neighbours
        if t is None:
            prev = next((times[k][1] for k in range(i - 1, -1, -1) if times[k]), 0.0)
            nxt = next((times[k][0] for k in range(i + 1, len(times)) if times[k]), prev)
            times[i] = (prev, max(prev, nxt))
    out = []
    for p, (s, e) in zip(plan, times):
        n = len(p['written'])
        for k, w in enumerate(p['written']):     # a multi-word key shares its span evenly
            a, b = s + (e - s) * k / n, s + (e - s) * (k + 1) / n
            out.append({'text': w, 's': round(a, 3), 'e': round(b, 3), 'p': p['trail'] if k == n - 1 else ''})
    return out


# ---------- providers: list of (spoken text, pause after) -> mono float32 at SR + word boundaries ----------
def to_wav48(data, suffix):
    with tempfile.TemporaryDirectory() as d:
        src, dst = os.path.join(d, 'a' + suffix), os.path.join(d, 'a.wav')
        open(src, 'wb').write(data)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-ar', str(SR), '-ac', '1', dst], check=True)
        y, _ = sf.read(dst, dtype='float32')
    return y


def trim_tail(y, keep=0.06):
    nz = np.nonzero(np.abs(y) > 1e-3)[0]
    return y[: nz[-1] + int(keep * SR)] if len(nz) else y


def synth_edge(parts, cfg):
    import edge_tts

    async def one(text):
        c = edge_tts.Communicate(text, cfg['voice'], rate=cfg['rate'], pitch=cfg.get('edge_pitch', '+0Hz'), boundary='WordBoundary')
        mp3, wb = bytearray(), []
        async for ch in c.stream():
            if ch['type'] == 'audio': mp3 += ch['data']
            elif ch['type'] == 'WordBoundary': wb.append((ch['text'], ch['offset'] / 1e7, (ch['offset'] + ch['duration']) / 1e7))
        return trim_tail(to_wav48(bytes(mp3), '.mp3')), wb

    out, bounds, t = [], [], 0.0
    for text, pause in parts:
        y, wb = asyncio.run(one(text))
        bounds += [(w, t + s, t + e) for w, s, e in wb]
        out.append(y); t += len(y) / SR
        if pause: out.append(np.zeros(int(pause * SR), np.float32)); t += pause
    return np.concatenate(out), bounds


def synth_azure(parts, cfg):
    import azure.cognitiveservices.speech as sdk
    key, region = os.environ.get('AZURE_SPEECH_KEY'), os.environ.get('AZURE_SPEECH_REGION')
    if not key or not region:
        sys.exit('Azure needs AZURE_SPEECH_KEY and AZURE_SPEECH_REGION (in .env at the repo root). Or use --provider edge.')
    sc = sdk.SpeechConfig(subscription=key, region=region)
    sc.set_speech_synthesis_output_format(sdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm)
    syn = sdk.SpeechSynthesizer(speech_config=sc, audio_config=None)
    wb = []
    def on_word(e):
        if e.boundary_type == sdk.SpeechSynthesisBoundaryType.Word:
            wb.append((e.text, e.audio_offset / 1e7, e.audio_offset / 1e7 + e.duration.total_seconds()))
    syn.synthesis_word_boundary.connect(on_word)
    lang = '-'.join(cfg['voice'].split('-')[:2])
    body = ''.join(escape(text) + (f'<break time="{int(pause * 1000)}ms"/>' if pause else '') for text, pause in parts)
    ssml = (f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{lang}">'
            f'<voice name="{cfg["voice"]}"><prosody rate="{cfg["rate"]}" pitch="{cfg["pitch"]}">{body}</prosody></voice></speak>')
    r = syn.speak_ssml_async(ssml).get()
    if r.reason != sdk.ResultReason.SynthesizingAudioCompleted:
        d = r.cancellation_details
        sys.exit(f'Azure synthesis failed: {r.reason} {getattr(d, "reason", "")} {getattr(d, "error_details", "")}')
    y, sr = sf.read(io.BytesIO(r.audio_data), dtype='float32')
    assert sr == SR, sr
    return trim_tail(y), wb


def list_voices(locale):
    import azure.cognitiveservices.speech as sdk
    load_env()
    sc = sdk.SpeechConfig(subscription=os.environ['AZURE_SPEECH_KEY'], region=os.environ['AZURE_SPEECH_REGION'])
    r = sdk.SpeechSynthesizer(speech_config=sc, audio_config=None).get_voices_async(locale).get()
    for v in r.voices:
        print(v.short_name, v.gender.name, ','.join(v.style_list) if v.style_list else '')


# ---------- main ----------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('film', nargs='?')
    ap.add_argument('--provider'); ap.add_argument('--voice'); ap.add_argument('--rate'); ap.add_argument('--pitch')
    ap.add_argument('--dry', action='store_true', help='print what would be spoken, do not synthesise')
    ap.add_argument('--list-voices', metavar='LOCALE')
    a = ap.parse_args()
    if a.list_voices: return list_voices(a.list_voices)
    if not a.film: ap.error('give the film folder, e.g. demos/my-film')
    load_env()
    vdir = os.path.join(a.film, 'voice')
    cfg = dict(DEFAULTS)
    if os.path.exists(os.path.join(vdir, 'voice.json')): cfg.update(json.load(open(os.path.join(vdir, 'voice.json'), encoding='utf-8')))
    for k in ('provider', 'voice', 'rate', 'pitch'):
        if getattr(a, k): cfg[k] = getattr(a, k)
    if cfg['provider'] == 'auto': cfg['provider'] = 'azure' if os.environ.get('AZURE_SPEECH_KEY') else 'edge'
    lex = json.load(open(os.path.join(ROOT, 'tools', 'tts', 'lexicon.id.json'), encoding='utf-8'))
    lex = {k: v for k, v in lex.items() if not k.startswith('_')}
    if os.path.exists(os.path.join(vdir, 'lexicon.json')): lex.update(json.load(open(os.path.join(vdir, 'lexicon.json'), encoding='utf-8')))
    lex.update(cfg.get('lexicon') or {})

    paras = read_narration(os.path.join(vdir, 'narration.txt'))
    gaps = cfg['gap'] if isinstance(cfg['gap'], list) else [cfg['gap']] * len(paras)
    parts, plans = [], []          # parts: (spoken text, pause after); plans: (paragraph index, plan) per part
    for pi, para in enumerate(paras):
        segs = segments(para)
        for si, (text, pause) in enumerate(segs):
            plan = spoken_plan(text, lex)
            last = si == len(segs) - 1
            parts.append((' '.join(p['say'] for p in plan), pause if not last else (gaps[pi] if pi < len(paras) - 1 else 0.0)))
            plans.append((pi, plan))
    spoken = '\n'.join(p for p, _ in parts)
    if a.dry:
        print(f'[{cfg["provider"]} {cfg["voice"]} rate {cfg["rate"]}]\n' + spoken); return

    y, bounds = (synth_azure if cfg['provider'] == 'azure' else synth_edge)(parts, cfg)
    lead = float(cfg['lead'])
    y = np.concatenate([np.zeros(int(lead * SR), np.float32), y])
    bounds = [(w, s + lead, e + lead) for w, s, e in bounds]
    # align the provider's word boundaries back to the written tokens, then tag each word with its paragraph
    allplan = [(pi, p) for pi, plan in plans for p in plan]
    words = align([p for _, p in allplan], bounds)
    paras_of = [pi for pi, p in allplan for _ in p['written']]
    for w, pi in zip(words, paras_of): w['para'] = pi
    os.makedirs(vdir, exist_ok=True)
    sf.write(os.path.join(vdir, 'voice.wav'), y, SR, subtype='PCM_24')
    open(os.path.join(vdir, 'spoken.txt'), 'w', encoding='utf-8').write(spoken + '\n')
    meta = {'provider': cfg['provider'], 'voice': cfg['voice'], 'rate': cfg['rate'], 'pitch': cfg['pitch'],
            'duration': round(len(y) / SR, 3), 'words': words}
    json.dump(meta, open(os.path.join(vdir, 'words.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(f'{cfg["provider"]} {cfg["voice"]} {cfg["rate"]}: {meta["duration"]} s, {len(words)} words, '
          f'{len(bounds)} boundaries -> {os.path.join(vdir, "voice.wav")}')
    for pi in range(len(paras)):
        pw = [w for w in words if w['para'] == pi]
        if pw: print(f'  {pi}: {pw[0]["s"]:6.2f} -> {pw[-1]["e"]:6.2f}  {" ".join(w["text"] for w in pw)[:72]}')


if __name__ == '__main__':
    main()
