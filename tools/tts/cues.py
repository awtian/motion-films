"""Resolve word references in a cue sheet against voice/words.json. Same rules as tools/tts/cues.mjs:
"@kasih" start of the first word "kasih" · "@pede#2" 2nd occurrence · "@terima.e" its end · "@9,9+1.36" with an offset.

    sys.path.insert(0, '<repo>/tools/tts'); from cues import load_cues
    cues = load_cues(film_dir)        # cues.json with every "@..." replaced by seconds
"""
import json, os, re

REF = re.compile(r'^@(.+?)(?:#(\d+))?(\.e)?([+-]\d+(?:\.\d+)?)?$')


def word_time(words, ref):
    m = REF.match(ref)
    if not m:
        raise ValueError(f'bad word ref {ref}')
    text, nth, end, off = m.groups()
    hits = [w for w in words if w['text'] == text]
    k = int(nth or 1) - 1
    if k >= len(hits):
        raise KeyError(f'word ref {ref}: "{text}" occurs {len(hits)}x in words.json')
    w = hits[k]
    return round((w['e'] if end else w['s']) + (float(off) if off else 0.0), 3)


def resolve(v, words):
    if isinstance(v, str) and v.startswith('@'):
        return word_time(words, v)
    if isinstance(v, list):
        return [resolve(x, words) for x in v]
    if isinstance(v, dict):
        return {k: resolve(x, words) for k, x in v.items()}
    return v


def load_cues(film_dir):
    cues = json.load(open(os.path.join(film_dir, 'cues.json'), encoding='utf-8'))
    wp = os.path.join(film_dir, 'voice', 'words.json')
    if not os.path.exists(wp):
        return cues
    return resolve(cues, json.load(open(wp, encoding='utf-8'))['words'])
