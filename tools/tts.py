# Generates Brazilian Portuguese audio (Google Cloud TTS, pt-BR Chirp3-HD voices)
# for every Portuguese text that has IPA in a lesson, and records it in
# assets/audio/manifest.json, which assets/audio.js uses to add ▶ buttons.
#
# Usage: python3 tools/tts.py lessons/01-01-subject-pronouns.md   (one lesson)
#        python3 tools/tts.py                                     (all lessons; also prunes unused files)
# Needs GOOGLE_TTS_API_KEY in the environment or in .env (git-ignored).
#
# What gets audio (must match assets/audio.js):
#   - <span class="pt">X</span><span class="ipa">          → X
#   - *X* <span class="ipa">  or  *X*<br><span class="ipa">  → X (bold markers removed)
#   - table row whose last cell is /IPA/                     → the cell containing **bold**
# Dialogues ("— A? — B.") get a different random voice for each turn, joined with a
# short pause by ffmpeg (brew install ffmpeg).
import base64, glob, hashlib, json, os, random, re, subprocess, sys, tempfile, time, unicodedata, urllib.request

AUDIO_DIR = 'assets/audio'
MANIFEST = f'{AUDIO_DIR}/manifest.json'
VOICES = [
    'Achernar', 'Achird', 'Algenib', 'Algieba', 'Alnilam', 'Aoede', 'Autonoe', 'Callirrhoe',
    'Charon', 'Despina', 'Enceladus', 'Erinome', 'Fenrir', 'Gacrux', 'Iapetus', 'Kore',
    'Laomedeia', 'Leda', 'Orus', 'Puck', 'Pulcherrima', 'Rasalgethi', 'Sadachbia',
    'Sadaltager', 'Schedar', 'Sulafat', 'Umbriel', 'Vindemiatrix', 'Zephyr', 'Zubenelgenubi',
]

def norm(s):
    s = unicodedata.normalize('NFC', s).replace('’', "'")
    return re.sub(r'\s+', ' ', s).strip()

def texts_in(path):
    out = []
    body = open(path, encoding='utf-8').read().split('\n---\n', 1)[1]
    for line in body.split('\n'):
        if line.startswith('|') and re.search(r'\|\s*/[^|]+/\s*\|\s*$', line):
            cells = [c.strip() for c in line.strip('|').split('|')][:-1]
            bold = [c for c in cells if '**' in c]
            if bold:
                out.append(bold[-1].replace('**', ''))
            continue
        for m in re.finditer(r'<span class="ipa">', line):
            before = line[:m.start()]
            pt = re.search(r'<span class="pt">([^<]*)</span>$', before)
            if pt:
                out.append(pt.group(1))
                continue
            it = re.search(r'\*([^*]+)\*\s*(<br>)?\s*$', before.replace('**', ''))
            if it:
                out.append(it.group(1))
    return [norm(t) for t in out]

def turns(text):
    parts = [p.strip() for p in re.split(r'(?:^|\s)—\s', text) if p.strip()]
    return parts if text.startswith('—') and len(parts) > 1 else [text]

def api_key():
    if os.environ.get('GOOGLE_TTS_API_KEY'):
        return os.environ['GOOGLE_TTS_API_KEY']
    for line in open('.env', encoding='utf-8'):
        if line.startswith('GOOGLE_TTS_API_KEY='):
            return line.split('=', 1)[1].strip().strip('"\'')
    sys.exit('GOOGLE_TTS_API_KEY not set (environment or .env)')

def synth(text, voice, key):
    req = urllib.request.Request(
        f'https://texttospeech.googleapis.com/v1/text:synthesize?key={key}',
        data=json.dumps({
            'input': {'text': text},
            'voice': {'languageCode': 'pt-BR', 'name': f'pt-BR-Chirp3-HD-{voice}'},
            'audioConfig': {'audioEncoding': 'MP3'},
        }).encode(),
        headers={'Content-Type': 'application/json'})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req) as r:
                return base64.b64decode(json.load(r)['audioContent'])
        except urllib.error.HTTPError as e:
            if e.code != 429 and e.code < 500 or attempt == 4:
                raise
            time.sleep(3 * 2 ** attempt)

def join(clips, gap=0.5):
    if len(clips) == 1:
        return clips[0]
    with tempfile.TemporaryDirectory() as d:
        ins = []
        for i, c in enumerate(clips):
            open(f'{d}/{i}.mp3', 'wb').write(c)
            ins += ['-i', f'{d}/{i}.mp3']
        pads = ''.join(f'[{i}]apad=pad_dur={gap}[p{i}];' for i in range(len(clips) - 1))
        seq = ''.join(f'[p{i}]' for i in range(len(clips) - 1)) + f'[{len(clips) - 1}]'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex',
                        f'{pads}{seq}concat=n={len(clips)}:v=0:a=1', '-b:a', '48k', f'{d}/out.mp3'], check=True)
        return open(f'{d}/out.mp3', 'rb').read()

paths = sys.argv[1:] or sorted(glob.glob('lessons/*.md'))
os.makedirs(AUDIO_DIR, exist_ok=True)
manifest = json.load(open(MANIFEST, encoding='utf-8')) if os.path.exists(MANIFEST) else {}
key = None
wanted = set()
for p in paths:
    for text in texts_in(p):
        wanted.add(text)
        if text in manifest and os.path.exists(f'{AUDIO_DIR}/{manifest[text]["file"]}'):
            continue
        key = key or api_key()
        parts = turns(text)
        voices = random.sample(VOICES, len(parts))
        audio = join([synth(t, v, key) for t, v in zip(parts, voices)])
        name = hashlib.sha1(text.encode()).hexdigest()[:12] + '.mp3'
        open(f'{AUDIO_DIR}/{name}', 'wb').write(audio)
        manifest[text] = {'file': name, 'voices': voices}
        print(f'{name}  {"/".join(voices):24}  {text}')
if not sys.argv[1:]:
    for text in [t for t in manifest if t not in wanted]:
        os.remove(f'{AUDIO_DIR}/{manifest.pop(text)["file"]}')
        print(f'removed  {text}')
json.dump(dict(sorted(manifest.items())), open(MANIFEST, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'{len(wanted)} text(s) in {len(paths)} lesson(s); manifest has {len(manifest)}')
