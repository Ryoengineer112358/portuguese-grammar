# Brazilian Portuguese Grammar — writing rules

A personal grammar of Brazilian Portuguese for the owner only, published with GitHub Pages (Jekyll, no plugins).
The owner adds lessons a little at a time over several years, usually by saying 「次の項目作って」.
**These rules are the only memory between sessions. Follow every one of them, every time, without being reminded.**
When the owner gives new feedback about how lessons should be written, update this file in the same turn (and re-apply the rule to existing lessons if the owner asks).

- Live site: https://ryoengineer112358.github.io/portuguese-grammar/
- Repo: https://github.com/Ryoengineer112358/portuguese-grammar (branch `main`, Pages from `/`)

## Reader and goal
- Reader: a Japanese adult, beginner (a little Duolingo). First goal: everyday conversation.
- Variety: **Brazilian** Portuguese only. Mention European forms only when the reader is likely to meet them (e.g. in apps) and say so explicitly.
- Teach spoken Brazilian usage first (você, a gente, tô/tá, ele as object, pra…). When it differs from the formal written norm, note the formal form briefly. Never present a formal-only form as what people normally say.

## Language and style
- Write in **correct, natural English** — not simplified or "easy" English. Clear, concise, explanatory prose, like a good reference grammar written for learners.
- Use standard grammar terms (subject, infinitive, preterite…) and briefly gloss a term the first time it appears in the book.
- Portuguese in *italics*; English glosses in quotes. Don't italicize English (the checker treats italic sentences as Portuguese).
- Chat replies to the owner are in **Japanese**; the book itself is in English.
- The README is only a list of links (generated). No explanations anywhere for "other readers" — the book is for the owner.

## Translation and IPA — applies to every Portuguese sentence (strict)
1. **Every Portuguese sentence anywhere in a lesson** — tables, explanations, lists, Watch out, Quick check answers — has **both** an English translation **and** IPA. No exceptions except ✗ wrong examples (translation optional, no IPA).
2. IPA markup: `<span class="ipa">/…/</span>` right after the sentence. Format in prose and lists:
   `- *Sou estudante.* <span class="ipa">/ˈso(w) is.tuˈdɐ̃.t͡ʃi/</span> — I'm a student.`
3. In table cells, stack the three: `*Sou casado.*<br><span class="ipa">/ˈso(w) kaˈza.du/</span><br>I'm married.`
4. Single Portuguese words cited in prose get IPA the first time they appear in the lesson (plain `/…/` is fine for single words).
5. Every word in a lesson's main form/vocabulary table gets IPA.
6. IPA source: Wiktionary's "(Brazil)" phonemic form, looked up with `python3 tools/ipa.py word1 word2 …`. Never invent IPA from memory and never use English-letter approximations ("vo-SEH").
7. Sentence IPA = dictionary forms of each word in order (no connected-speech reductions); say so in `note`.
8. If Wiktionary has no IPA for a form (common for inflected verbs, articles), derive it by analogy from a related entry and **name every derived word in `note`**.
9. Regional variants worth knowing (e.g. Rio final /ʃ/) go in one line under the table.

## Audio (Brazilian Portuguese, ▶ buttons)
- **Status: trial in 01-01 only (2026-11-08).** Once the owner approves, run it for every lesson and make it part of the checklist below.
- `python3 tools/tts.py lessons/<file>.md` creates one mp3 per Portuguese text that has IPA and records it in `assets/audio/manifest.json`. Engine: **Gemini 3.8 Flash TTS** (`gemini-3.8-flash-tts` on Vertex AI, chosen 2026-11-08 by the owner over Chirp 3 HD), one of its 30 voices at random per clip; dialogues use its two-speaker mode with two random voices. Existing clips are reused (clips from another model are re-recorded); running it with no arguments does all lessons and deletes unused clips.
- If the owner says a clip sounds wrong (e.g. a syllable is missing), re-record just that text: `python3 tools/tts.py --redo "<text>"` (new random voice). Glitches are occasional and per clip, not per voice. The owner does not want an automatic detector. The page adds the voice and model names as a query string, so the browser fetches the new file.
- `assets/audio.js` adds a ▶ button after each IPA that has a clip. Its text-finding rules must stay in sync with `tools/tts.py`.
- Auth: the owner's `gcloud` login (`gcloud auth print-access-token`) and `GCP_PROJECT_ID` in `.env` (git-ignored; same project as `~/Developer/personal/anki-vocab-app`). Needs ffmpeg. Never commit `.env`.
- The owner does not want a note saying the audio is synthesized. Don't add one.

## Layout rules (phone first)
- Tables have **at most 3 columns**. If you need more, split into two tables.
- Examples in `## In conversation` use exactly this markup, one `<li>` per line:
  `<li><span class="pt">Portuguese</span><span class="ipa">/IPA/</span><span class="en">English</span></li>` inside `<ul class="ex">`.
- In blockquotes and `<details>`, separate lines with `<br>` or a blank line (single newlines are joined).

## Lesson size and content
- One lesson = one grammar point = about **5 minutes** of reading (roughly 400–700 words plus tables).
- Example sentences must be **things people actually say in everyday conversation**: short, natural, colloquial Brazilian. No textbook-only sentences ("The pen is on the table"). Prefer dialogue pairs (— … — …) where they help.
- 6–8 examples per lesson. It's fine if examples contain words not yet taught.
- Don't state a usage is "wrong" unless sources say so; colloquial Brazilian often allows what textbooks forbid.

## Lesson template
File: `lessons/<id>-<slug>.md` (e.g. `lessons/02-01-ar-verbs.md`). Front matter:

```yaml
---
layout: lesson
lesson_id: "02-01"            # must match _data/toc.yml
title: "…"                    # same as in toc.yml
permalink: /lessons/02-01/
goal: "One sentence: what the reader can do after this lesson."
verification:
  status: source-checked      # verified | source-checked | needs-check
  checked_on: YYYY-MM-DD
  note: "What was checked (2+ sources), what rests on one source, IPA source, words whose IPA was derived by analogy."
sources:
  - title: "…"
    publisher: "…"
    url: "…"
    used_for: "Which claims this source supports. Say honestly if only the ToC/summary was seen."
---
```

Body sections, in this order (use `##` headings):
1. The core rule / form (usually a table, ≤3 columns, with IPA)
2. Explanation (2–4 numbered key points, each Portuguese sentence with IPA + translation)
3. `## In conversation` — 6–8 examples in the `ex` markup above
4. `## Watch out` — common mistakes, regional or register notes, as `>` blockquotes
5. `## Quick check` — 2–4 questions, each in `<details markdown="1"><summary>…</summary> answer </details>`; answers containing Portuguese sentences get IPA + translation

The layout adds the chapter label, goal box, sources/verification section, and prev/next links automatically. Do not write those by hand.

## Research and verification (required for every lesson)
- Before writing, research on the web. Prefer: published grammars (Whitlam, *Modern Brazilian Portuguese Grammar*, Routledge), university materials (UW–Madison *Português para principiantes* on LibreTexts, UT Austin COERLL), Wiktionary for forms/IPA, reputable Brazilian-focused teaching sites (Speaking Brazilian, Elon.io Brazilian grammar, Mango, Semantica). Avoid European-Portuguese sites for usage claims.
- Every rule must be supported by **at least two independent sources** (two pages from the same publisher count as one). A point with only one source may be included, but name it in `note`.
- Never claim to have read something you didn't. If only a table of contents or summary was available, say so in `used_for`.
- `verified` is set **only** when the owner reports that a native speaker or teacher reviewed the lesson.

## Adding a lesson (checklist — do all of it, including publishing)
1. Take the next `planned` item in `_data/toc.yml` (or the one the owner names). 「次の章」 from the owner usually means the next item.
2. Research (2+ sources per rule), look up IPA with `tools/ipa.py`.
3. Write `lessons/<id>-<slug>.md` from the template.
4. In `_data/toc.yml`, set that item's `status: published`.
5. `python3 tools/readme.py` (regenerates README.md).
6. `python3 tools/check.py` — **must print OK**. Fix everything it reports. (It checks front matter, sections, example markup, IPA after every italic Portuguese sentence, table width, and toc consistency. Passing it is necessary, not sufficient: also re-read the lesson for any Portuguese sentence lacking a translation.)
7. Commit and push to `main` (the owner has asked for this to be done every time).
8. Confirm publishing: `gh run list -R Ryoengineer112358/portuguese-grammar -L 1` should show a run for the new commit within ~30 s. If no run appears, push an empty commit (`git commit --allow-empty -m "Trigger Pages rebuild"`) — don't wait longer. Then `gh run watch <id>` and `curl` the lesson URL (add `?v=$RANDOM` to bypass cache) to confirm HTTP 200.
9. Report to the owner in Japanese: what was added, key points, sources, verification status, open doubts, the URL.

## Changing the plan
- `_data/toc.yml` is the master plan. Lesson IDs (`CC-II`) never change after publication.
- To add a lesson inside a chapter, give it the next unused number in that chapter and place it where it belongs in the list; list order is reading order.
- New chapters get the next unused chapter number; their position in the file sets their order.
