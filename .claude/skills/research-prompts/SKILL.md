---
name: research-prompts
description: Turn a validated documentary topic into detailed, numbered research prompts the user pastes into Perplexity (or uses for their own research), shaped so the answers come back with primary sources, exact figures and disputes marked, ready for facts-checker Gate 1. Use for "research prompts do", "perplexity prompt", "research ke points", "kya research karun", or step 3 of a new video after topic validation.
---

# Research Prompts (for Perplexity)

Talk to the user in Hinglish; write the prompts themselves in **English** (sources are mostly English and Perplexity searches better in English). Add Hindi-language source requests only where Indian-language records matter.

The user does the research. Your job is to make sure nothing important is missed and that every answer comes back checkable.

## Inputs
From `yt-agent/videos/<slug>/`: `topic/TOPIC.md` (angle, category, format, known sources, risks, visuals gaps), `PROGRESS.md`, and `seo/SEO.md` if it already exists. Read `yt-agent/LEARNINGS.md` for research gaps past videos hit.

## Build the prompt set
Scale to the format: **Short ≈ 4–6 prompts, Long ≈ 10–15.** Each prompt asks one focused question set (Perplexity does better with focused prompts than one giant prompt). Cover, adapting to the category:

1. **Core timeline**: exact dates (with time zone for current affairs), sequence, who decided what and when.
2. **Key people and institutions**: roles at the time, documented actions and statements (not motives unless sourced).
3. **Primary records**: official documents, declassified files, court records, filings, parliamentary records, original papers, datasets. Ask for document names, dates and links.
4. **The central question of the angle**: evidence for and against.
5. **Numbers**: every figure with unit, year, nominal/real, and who measured it.
6. **Competing interpretations and disputes**: who says what, and on what evidence.
7. **Myths and common errors**: popular claims about this topic that are wrong or overstated (these become the most valuable reveals and the traps facts-checker must catch).
8. **Consequences and aftermath**: what demonstrably changed, with sources.
9. **Verified quotes**: exact wording, speaker, date, original source; flag paraphrases.
10. **Visual leads**: where real photos, documents, maps or footage exist (archives, Commons, agency pages) and their usage terms.
11. Category extras: **History**: memoir vs contemporaneous record. **Tech**: demo vs deployment, benchmark vs real-world. **Finance**: revenue/profit/cash flow, fiscal year, filings. **Current affairs**: as-of date, allegation vs confirmed, official position vs independent findings.

## Every prompt ends with this answer-format block
```
Answer rules:
- One claim per bullet. After each bullet give the source: title, publisher, date, and a working URL.
- Prefer primary sources (official records, original documents, filings, papers); then reputable named-source reporting or scholarly work. Say "no primary source found" when that's the case.
- Give exact numbers with unit and year. Do not round or estimate without saying so.
- Mark anything disputed as DISPUTED and give both sides with sources.
- Mark anything you could not verify as UNVERIFIED. Do not fill gaps with guesses.
- Quotes: exact words only with speaker, date and original source; otherwise label as paraphrase.
```

## Output
Save `videos/<slug>/research/RESEARCH_PROMPTS.md`:
- How to use: paste one prompt at a time; use Perplexity's deeper research mode for the broad prompts (1, 3, 6, 7) if the plan has it, normal search for the narrow ones; **save every answer with its links** (copy as Markdown or export) into the asset folder as `research/01.md`, `02.md`, … matching the prompt numbers. Links matter more than the prose: facts-checker verifies against them.
- The numbered prompts, each in its own code block so it copies in one click, with a one-line "why this matters for the script" above it.
- A short "follow-up" list: what to ask next if an answer comes back thin, contradictory or without sources.

In chat: the number of prompts, the 3 most important ones in full, and the file path. When the user says the research is in, run `facts-checker` Gate 1 on it.
