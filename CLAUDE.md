# Brazilian Portuguese Grammar — writing rules

A grammar of Brazilian Portuguese, published with GitHub Pages (Jekyll, no plugins).
The owner adds lessons a little at a time over several years. Follow these rules every time.

## Reader and goal
- Reader: a Japanese adult, beginner (a little Duolingo). First goal: everyday conversation.
- Variety: **Brazilian** Portuguese only. Mention European forms only when the reader is likely to meet them (e.g. in apps) and say so explicitly.
- Teach spoken Brazilian usage first (você, a gente, ele as object, pra, tá…). When it differs from the formal written norm, note the formal form briefly. Never present a formal-only form as what people normally say.

## Language and style
- Write in **correct, natural English** — not simplified or "easy" English. Clear, concise, explanatory prose, like a good reference grammar written for learners.
- Use standard grammar terms (subject, infinitive, preterite…) and briefly gloss a term the first time it appears in the book.
- Portuguese in *italics* inside prose; tables and example lists as in the template.
- Chat replies to the owner are in Japanese; the book itself is in English.

## Lesson size and content
- One lesson = one grammar point = about **5 minutes** of reading (roughly 400–700 words plus tables).
- Example sentences must be **things people actually say in everyday conversation**: short, natural, colloquial Brazilian. No textbook-only sentences ("The pen is on the table"). Prefer dialogue pairs (— … — …) where they help.
- 5–8 examples per lesson. It's fine if examples contain verbs/words not yet taught; add a one-line "don't worry about X yet" if needed.
- Every Portuguese example has an English translation in the same item.

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
  note: "What was checked, what wasn't, any open doubts."
sources:
  - title: "…"
    publisher: "…"
    url: "…"
    used_for: "Which claims this source supports. Say honestly if only the ToC/summary was seen."
---
```

Body sections, in this order (use `##` headings):
1. The core rule / form (usually a table)
2. Explanation (numbered key points, 2–4)
3. `## In conversation` — examples using `<ul class="ex">` with `<span class="pt">` / `<span class="en">`
4. `## Watch out` — common mistakes, regional or register notes, as `>` blockquotes
5. `## Quick check` — 2–4 questions, each in `<details markdown="1"><summary>…</summary> answer </details>`

The layout adds the chapter label, goal box, sources/verification section, and prev/next links automatically. Do not write those by hand.

## Research and verification (required for every lesson)
- Before writing, research on the web. Prefer: published grammars (Routledge Whitlam, *Modern Brazilian Portuguese Grammar*; Hutchinson & Lloyd), university materials (e.g. UT Austin COERLL / Brazilpod), Wiktionary/Wikipedia for forms, reputable Brazilian-focused teaching sites (Speaking Brazilian, etc.).
- Every rule in the lesson must be supported by **at least two independent sources**. Otherwise set status `needs-check` and say which point is unconfirmed in `note`.
- Never claim to have read something you didn't. If only a table of contents or summary was available, say so in `used_for`.
- `verified` is set **only** when the owner reports that a native speaker or teacher reviewed the lesson.
- Pronunciation hints are rough English-letter approximations; say so in `note` when used.

## Adding a lesson (checklist)
1. Pick the next item in `_data/toc.yml` (or the one the owner asks for).
2. Research, then write `lessons/<id>-<slug>.md` from the template.
3. In `_data/toc.yml`, change that item's `status` to `published`.
4. Run `python3 tools/readme.py` to regenerate `README.md` (a plain list of chapter/lesson links; no explanations — the book is for the owner only).
5. Check the page at phone width if possible.
6. Commit and push to `main` (GitHub Pages publishes automatically), then confirm the live page loads.
7. Report to the owner in Japanese: what was added, sources, verification status, open doubts.

## Changing the plan
- `_data/toc.yml` is the master plan. Lesson IDs (`CC-II`) never change after publication.
- To add a lesson inside a chapter, give it the next unused number in that chapter and place it where it belongs in the list; list order is reading order.
- New chapters get the next unused chapter number; their position in the file sets their order.
