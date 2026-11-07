# Looks up Brazilian Portuguese IPA on English Wiktionary.
# Usage: python3 tools/ipa.py sou você "com licença"
# Prints one line per word: the "(Brazil)" / "(Rio de Janeiro)" IPA lines from the Portuguese section.
# An empty result means Wiktionary has no IPA for that form (common for inflected verbs);
# then fill it in by analogy and name the word in the lesson's verification note.
# Wiktionary rate-limits quickly (HTTP 429), so requests are spaced out.
import sys, re, html, time, urllib.request, urllib.parse

DELAY_SECONDS = 7

for word in sys.argv[1:]:
    time.sleep(DELAY_SECONDS)
    url = 'https://en.wiktionary.org/api/rest_v1/page/html/' + urllib.parse.quote(word.replace(' ', '_'))
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'portuguese-grammar-notes/1.0'})
        page = urllib.request.urlopen(req, timeout=20).read().decode()
    except Exception as e:
        print(word, '| ERROR', e)
        continue
    start = page.find('id="Portuguese"')
    end = page.find('<h2', start + 10)
    section = page[start:end if end > 0 else None] if start >= 0 else ''
    found = []
    for m in re.finditer(r'<li>(.*?)</li>', section, re.S):
        line = ' '.join(html.unescape(re.sub('<[^>]+>', '', m.group(1))).split())
        if 'IPA' in line and ('Brazil' in line or 'Rio' in line) and line not in found:
            found.append(line[:160])
    print(word, '|', ' || '.join(found[:3]))
