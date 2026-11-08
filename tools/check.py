# Checks every lesson against the writing rules in CLAUDE.md.
# Usage: python3 tools/check.py            (all lessons)
#        python3 tools/check.py lessons/01-05-nao.md
# Exit code 1 if anything fails. Run before every commit.
import json, os, re, sys, glob, yaml
sys.path.insert(0, os.path.dirname(__file__))
from tts import texts_in, MANIFEST, AUDIO_DIR

REQUIRED_SECTIONS = ['## In conversation', '## Watch out', '## Quick check']
STATUSES = {'verified', 'source-checked', 'needs-check'}
# An italic Portuguese sentence: *...* ending in . ? or ! (optionally followed by closing quote)
SENTENCE = re.compile(r'(?<![*\w])\*(?!\*)([^*\n]*?[^\s*][.?!…])\*(?!\*)')
IPA = 'class="ipa"'

def check(path, toc_ids):
    errs = []
    text = open(path, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', text, re.S)
    if not m:
        return [f'{path}: no front matter']
    fm, body = yaml.safe_load(m.group(1)), m.group(2)
    lid = fm.get('lesson_id')
    for key in ['layout', 'lesson_id', 'title', 'permalink', 'goal', 'verification', 'sources']:
        if not fm.get(key):
            errs.append(f'front matter: missing {key}')
    if lid and fm.get('permalink') != f'/lessons/{lid}/':
        errs.append(f'permalink should be /lessons/{lid}/')
    if lid and lid not in toc_ids:
        errs.append(f'{lid} not in _data/toc.yml')
    v = fm.get('verification') or {}
    if v.get('status') not in STATUSES:
        errs.append(f'verification.status must be one of {sorted(STATUSES)}')
    if not v.get('checked_on') or not v.get('note'):
        errs.append('verification needs checked_on and note')
    for i, s in enumerate(fm.get('sources') or []):
        if not s.get('title') or not s.get('used_for'):
            errs.append(f'source #{i+1} needs title and used_for')
    for sec in REQUIRED_SECTIONS:
        if sec not in body:
            errs.append(f'missing section "{sec}"')

    in_ex = False
    for n, line in enumerate(body.split('\n'), 1):
        if '<ul class="ex">' in line:
            in_ex = True
            continue
        if in_ex:
            if '</ul>' in line:
                in_ex = False
            elif '<li>' in line:
                for cls in ['pt', 'ipa', 'en']:
                    if f'class="{cls}"' not in line:
                        errs.append(f'body line {n}: example missing <span class="{cls}">')
            continue
        if line.startswith('|') and line.count('|') - 1 > 3:
            errs.append(f'body line {n}: table has more than 3 columns (split it for phones)')
        if '<summary>' in line:
            continue  # questions may quote the sentence the answer explains
        for sm in SENTENCE.finditer(line):
            sent = sm.group(1)
            if re.search(r'[A-Za-z]', sent) and ' ' in sent.strip() or sent[0].isupper():
                rest = line[sm.end():]
                if line.lstrip('> ').startswith('✗') or '✗' in line[max(0, sm.start()-4):sm.start()]:
                    continue  # wrong examples don't need IPA
                if IPA not in rest:
                    errs.append(f'body line {n}: no IPA after *{sent}*')
    audio = json.load(open(MANIFEST, encoding='utf-8')) if os.path.exists(MANIFEST) else {}
    for text in texts_in(path):
        e = audio.get(text, {})
        if not all(e.get(k) and os.path.exists(f'{AUDIO_DIR}/{e[k]}') for k in ['file', 'textbook']):
            errs.append(f'no audio for "{text}" (run python3 tools/tts.py {path})')
    return [f'{path}: {e}' for e in errs]

toc = yaml.safe_load(open('_data/toc.yml', encoding='utf-8'))
toc_ids = {it['id'] for ch in toc for it in ch['items']}
published = {it['id'] for ch in toc for it in ch['items'] if it['status'] == 'published'}
paths = sys.argv[1:] or sorted(glob.glob('lessons/*.md'))
errors = []
for p in paths:
    errors += check(p, toc_ids)
files = {re.match(r'lessons/(\d\d-\d\d|\d\d-\d+-\d+)(?=-[a-z])', p).group(1) for p in glob.glob('lessons/*.md')}
for lid in sorted(published - files):
    errors.append(f'_data/toc.yml: {lid} is published but has no lesson file')
for lid in sorted(files - published):
    errors.append(f'_data/toc.yml: {lid} has a lesson file but status is not published')
print('\n'.join(errors) if errors else f'OK: {len(paths)} lesson(s) pass')
sys.exit(1 if errors else 0)
