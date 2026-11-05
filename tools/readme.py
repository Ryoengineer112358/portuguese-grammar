# Regenerates README.md (chapter links) from _data/toc.yml.
import yaml
toc = yaml.safe_load(open('_data/toc.yml'))
B = 'https://ryoengineer112358.github.io/portuguese-grammar'
out = ['# Brazilian Portuguese Grammar', '']
for ch in toc:
    out.append(f"- [**{ch['chapter']}. {ch['title']}**]({B}/#ch-{ch['chapter']})")
    for it in ch['items']:
        if it['status'] == 'published':
            out.append(f"  - [{it['id']} {it['title']}]({B}/lessons/{it['id']}/)")
open('README.md', 'w').write('\n'.join(out) + '\n')
