# Generates Brazilian Portuguese audio (Gemini 3.8 Flash TTS on Vertex AI)
# for every Portuguese text that has IPA in a lesson, and records it in
# assets/audio/manifest.json, which assets/audio.js uses to add ▶ buttons.
#
# Usage: python3 tools/tts.py lessons/01-01-subject-pronouns.md   (one lesson)
#        python3 tools/tts.py                                     (all lessons; also prunes unused files)
#        python3 tools/tts.py --redo "Vocês são daqui?"            (re-record one text with a new random voice)
# Needs: gcloud logged in (gcloud auth login), GCP_PROJECT_ID in .env (git-ignored),
#        ffmpeg (brew install ffmpeg) to turn the returned WAV into MP3.
# Clips made with another model are re-recorded automatically.
#
# What gets audio (must match assets/audio.js):
#   - <span class="pt">X</span><span class="ipa">          → X
#   - *X* <span class="ipa">  or  *X*<br><span class="ipa">  → X (bold markers removed)
#   - table row whose last cell is /IPA/                     → the cell containing **bold**
#   - table cell **X**<br><span class="ipa">                → X (a word, e.g. a verb form)
# Dialogues ("— A? — B.") use Gemini's two-speaker mode with two different random voices.
# Each text gets <hash>.mp3 (natural) and <hash>-t.mp3 (textbook) with the same voice(s);
# a word (single word, or an entry in a word table such as "a gente") gets only the textbook one.
import base64, glob, hashlib, json, os, random, re, subprocess, sys, tempfile, time, unicodedata, urllib.request

MODEL = 'gemini-3.8-flash-tts'
# Two recordings per text, same voice(s): natural (②, also played at 0.5x as ③ by audio.js) and textbook (①).
STYLE = 'Brazilian Portuguese with a neutral Brazilian accent, as spoken in everyday conversation; natural pace, clearly articulated.'
TEXTBOOK_STYLE = ('Brazilian Portuguese with a neutral Brazilian accent, read like a language teacher modelling textbook '
                  'pronunciation for beginners: slowly and very crisply, every word pronounced fully and separately '
                  'with a short pause between words, every syllable articulated; no reductions, contractions or '
                  'linking (say "você", never "cê"; keep every vowel).')
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

def texts_in(path, words_only=False):
    out, words = [], []
    body = open(path, encoding='utf-8').read().split('\n---\n', 1)[1]
    for line in body.split('\n'):
        if line.startswith('|') and re.search(r'\|\s*/[^|]+/\s*\|\s*$', line):
            cells = [c.strip() for c in line.strip('|').split('|')][:-1]
            bold = [c for c in cells if '**' in c]
            if bold:
                out.append(bold[-1].replace('**', ''))
                words.append(out[-1])
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
                continue
            cell = before.rsplit('|', 1)[-1]
            if line.startswith('|') and re.search(r'\*\*\s*(<br>)?\s*$', cell):  # form table: **estou**<br>IPA
                out.append(cell.replace('**', '').replace('<br>', ''))
                words.append(out[-1])
    if words_only:  # table entries and single words: word-level audio
        return {norm(t) for t in words} | {norm(t) for t in out if is_single_word(norm(t))}
    return [norm(t) for t in out]

def is_single_word(text):
    return ' ' not in text

def turns(text):
    parts = [p.strip() for p in re.split(r'(?:^|\s)—\s', text) if p.strip()]
    return parts if text.startswith('—') and len(parts) > 1 else [text]

def env(name):
    if os.environ.get(name):
        return os.environ[name]
    for line in open('.env', encoding='utf-8'):
        if line.startswith(f'{name}='):
            return line.split('=', 1)[1].strip().strip('"\'')
    sys.exit(f'{name} not set (environment or .env)')

def synth(parts, voices, project, token, style):
    if len(parts) == 1:
        contents = [{'text': parts[0], 'speechMetadata': {'style': style}}]
        speech = {'voiceConfig': {'voice': voices[0]}}
    else:  # two speakers, alternating turns
        names = ['A', 'B']
        contents = [{'text': t, 'speechMetadata': {'speaker': names[i % 2], 'style': style}} for i, t in enumerate(parts)]
        speech = {'multiSpeakerVoiceConfig': {'speakerVoiceConfigs': [
            {'speaker': n, 'voiceConfig': {'voice': v}} for n, v in zip(names, voices)]}}
    req = urllib.request.Request(
        f'https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/publishers/google/models/{MODEL}:generateContent',
        data=json.dumps({
            'contents': [{'role': 'user', 'parts': contents}],
            'generationConfig': {'responseModalities': ['AUDIO'], 'speechConfig': speech},
        }).encode(),
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req) as r:
                wav = base64.b64decode(json.load(r)['candidates'][0]['content']['parts'][0]['inlineData']['data'])
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 and e.code < 500 or attempt == 4:
                raise
            time.sleep(3 * 2 ** attempt)
    with tempfile.TemporaryDirectory() as d:
        open(f'{d}/in.wav', 'wb').write(wav)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{d}/in.wav', '-b:a', '48k', f'{d}/out.mp3'], check=True)
        return open(f'{d}/out.mp3', 'rb').read()

def auth(project, token):
    return (project or env('GCP_PROJECT_ID'),
            token or subprocess.run(['gcloud', 'auth', 'print-access-token'], capture_output=True, text=True, check=True).stdout.strip())

def main():
    if sys.argv[1:2] == ['--redo']:
        redo = norm(sys.argv[2])
        sys.argv[1:] = [p for p in sorted(glob.glob('lessons/*.md')) if redo in texts_in(p)]
        if not sys.argv[1:]:
            sys.exit(f'not found in any lesson: {redo}')
    else:
        redo = None

    paths = sys.argv[1:] or sorted(glob.glob('lessons/*.md'))
    os.makedirs(AUDIO_DIR, exist_ok=True)
    manifest = json.load(open(MANIFEST, encoding='utf-8')) if os.path.exists(MANIFEST) else {}
    project = token = None
    wanted = set()
    word_level = set().union(*(texts_in(p, words_only=True) for p in paths))
    for p in paths:
        for text in texts_in(p):
            if text in wanted:
                continue
            wanted.add(text)
            entry = manifest.get(text)
            fresh = text == redo or not entry or entry.get('model') != MODEL
            if fresh:
                entry = manifest[text] = {'voices': random.sample(VOICES, min(len(turns(text)), 2)), 'model': MODEL}
            h = hashlib.sha1(text.encode()).hexdigest()[:12]
            if text in word_level:  # a word only needs the careful recording (played at 1x and 0.5x)
                if entry.get('file'):
                    if os.path.exists(f'{AUDIO_DIR}/{entry["file"]}'):
                        os.remove(f'{AUDIO_DIR}/{entry["file"]}')
                    del entry['file']
            elif not entry.get('file') or not os.path.exists(f'{AUDIO_DIR}/{entry["file"]}'):
                project, token = auth(project, token)
                entry['file'] = f'{h}.mp3'
                open(f'{AUDIO_DIR}/{entry["file"]}', 'wb').write(synth(turns(text), entry['voices'], project, token, STYLE))
                print(f'{entry["file"]}    {"/".join(entry["voices"]):24}  {text}')
            if fresh or not entry.get('textbook') or not os.path.exists(f'{AUDIO_DIR}/{entry["textbook"]}'):
                project, token = auth(project, token)
                entry['textbook'] = f'{h}-t.mp3'
                open(f'{AUDIO_DIR}/{entry["textbook"]}', 'wb').write(synth(turns(text), entry['voices'], project, token, TEXTBOOK_STYLE))
                print(f'{entry["textbook"]}  {"/".join(entry["voices"]):24}  {text}')
    if not sys.argv[1:]:
        for text in [t for t in manifest if t not in wanted]:
            entry = manifest.pop(text)
            for f in [entry.get('file'), entry.get('textbook')]:
                if f and os.path.exists(f'{AUDIO_DIR}/{f}'):
                    os.remove(f'{AUDIO_DIR}/{f}')
            print(f'removed  {text}')
    json.dump(dict(sorted(manifest.items())), open(MANIFEST, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{len(wanted)} text(s) in {len(paths)} lesson(s); manifest has {len(manifest)}')

if __name__ == '__main__':
    main()
