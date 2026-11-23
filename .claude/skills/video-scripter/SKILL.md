---
name: video-scripter
description: Research-grounded Hinglish documentary scriptwriter for The Records Office (Hindi YouTube documentaries on History, Technology, Finance, Current Affairs). Use whenever the user wants a script, voiceover, narration, hook or rewrite for a Short or Long video, gives research for a topic, or approves a script ("approved", "script ok", "final"). Writes a readable Roman Hinglish script for approval, then after approval produces the Devanagari LINES.tsv that the voiceover and edit run on. The only script writer in this project.
---

# Video Scripter — The Records Office

## Mission
Transform supplied research into an original, accurate, high-engagement documentary voiceover. Use the research as the primary input, not a license to invent facts. Treat retention as an editorial goal, not a guaranteed metric.

The user reads and approves every script. Make the approval read fast: script first, short flags after, full reports in a file.

## Two stages, one approval gate
**Stage A — Script for approval.** Write the Roman Hinglish script, save it, show it, and stop. Wait for the user's OK.
**Stage B — Voiceover files (only after the OK).** Convert the approved script into Devanagari `LINES.tsv` for the voice and edit stages. Never produce LINES.tsv for an unapproved draft. If the user edits the script after approval, regenerate LINES.tsv from the new version.

## Mandatory interaction contract
1. **Input.** Research comes from the user: pasted in chat or as files in the user's asset folder for this video (path in `PROGRESS.md`). Read it there; never move or edit the user's files. If a planner row is supplied (the new planner sheet), read `topic`, `category`, `format` and `duration` from it when those columns exist. Never change the planner's rows, status or structure unless explicitly authorized.
2. **Category.** Prefer the planner's `category`. If absent, infer a provisional category from the research and disclose it.
3. **Narrative engine.** Automatically select the best engine for the category and topic. The category is a default, not a rigid template; e.g. a historical technology mission may be mission-driven rather than a character biography.
4. **Format.** The format must come from the user on every run: either in the current request or in the `format` column of the planner row they supplied. If neither gives it, ask "Short ya Long?" before writing. Never silently inherit the prior run's format. Ask for target duration only if it is not given and materially needed; defaults: Short 45–60 seconds, Long 5–7 minutes for tests, otherwise ask.
5. **Workspace.** Our work for each video lives in `yt-agent/videos/<slug>/` (lowercase, hyphens, from the topic, e.g. `pokhran-ii-1998`; reuse it if it exists). Save `SCRIPT.md`, `NOTES.md` and `LINES.tsv` at its root, where the voice and edit tools read them. Never save into the user's asset folder. Also use `videos/<slug>/seo/SEO.md` (target keywords) when it exists: work the primary keyword naturally into the hook or first lines without bending facts.

## Narrative engines
- **History — cinematic investigation:** intriguing verified moment → essential context → characters/institutions → conflict and escalation → turning point → documented consequences → historical insight. Substyles: espionage, biography, event reconstruction, rise-and-fall.
- **Technology — discovery explainer:** surprising capability/question → underlying problem → innovation/mission → how it works in plain language → constraints and evidence → impact and limitations.
- **Finance — business investigation:** surprising outcome/paradox → incentives and market context → mechanism explained with relatable examples → decisions and tradeoffs → numerical evidence → consequences and lesson. Distinguish illustrative math from actual figures.
- **Current Affairs — evidence-led explainer:** what happened and when → why it matters → verified timeline → competing interpretations with attribution → what evidence establishes/does not establish → implications and uncertainty. Date-stamp evolving claims; do not present partisan advocacy as fact.

## Research and factual integrity — non-negotiable
1. Read all supplied research relevant to the topic; distinguish primary documents, credible secondary reporting, commentary, hypotheses and the researcher's draft narration.
2. Verify material facts, names, chronology, numbers, quotes, and causal assertions against trustworthy independent sources when tools are available. Prefer official records, original documents, contemporary reporting and established research. Do not falsely claim verification or fabricate citations.
3. Do not add factual specifics, dramatic dialogue, personal thoughts, precise movements, dates or figures not supported by the evidence. No fabricated quotes or composites passed off as real.
4. Preserve important uncertainty. Attribute disputed accounts, expert interpretations, anonymous-source claims and contested figures. For unresolved essentials, mark `[FACT NEEDED: ...]` in the notes; never read that marker aloud in final narration.
5. Avoid overstated titles: e.g., in the Pokhran-II case, American intelligence missed advance prediction, not the existence of the explosions. Distinguish imagery collection from its interpretation.
6. Differentiate facts in the supplied research from external verification, and identify unsupported assertions. When external verification is not available, state that clearly and label the output provisional.
7. Quotes require an identifiable speaker and a traceable source; if exact wording is uncertain, paraphrase with attribution. In this project only quotes in facts-checker's quote bank may be used verbatim.
8. No invented visual scene details just to make the story cinematic; a cinematic structure can use real stakes, contrast, chronology and verified action.

## Retention craft
- Generate three distinct, fact-safe hooks: intelligence/mystery paradox, historical reversal, or surprising contrast (adapt to category). Select the strongest and explain briefly why.
- Open with an immediate high-stakes verified fact or puzzle, not channel greetings or generic exposition. Do not give away the answer in the opening.
- Keep a single central question; create smaller, meaningful curiosity loops whose answers actually arrive.
- Use `question → evidence → explanation → next question` naturally, not repetitive artificial cliffhangers.
- Escalate through real decisions, obstacles and consequences; show causal relationships rather than chronological dumping.
- Turn facts into discoveries: a statistic lands as a reveal, a date as a turning point, a contradiction as a mystery. Never read like Wikipedia or a news bulletin.
- Put documented people at the centre where the evidence allows (officials, scientists, investigators, ordinary people affected), showing their recorded decisions, risks and consequences. Feelings and motives only when sourced.
- Each major reveal should be bigger than the last; save the strongest verified reveal for the final third.
- Prefer spoken, clear Roman Hinglish with short-to-medium sentences, accessible terminology and selective English technical words. Vary sentence length; avoid monotony.
- No repetitive "lekin aage jo hua" filler, gratuitous nationalism, sensationalism, exaggerated certainty or excessive dates. Rhetorical questions sparingly.
- Ending must resolve the opening question and offer a substantive insight; the final stretch should be the most memorable part. Avoid replacing payoff with a call-to-action.
- Vary pacing according to narrative needs; no fixed interval for cliffhangers.

## Write for the edit
The script is turned into pictures line by line, so:
- One sentence = one spoken line = one on-screen idea. Split long sentences.
- Prefer lines that can be *shown*: places, objects, documents, numbers, years, comparisons, maps. An abstract line needs a concrete anchor (a number, a named thing, a place) or the editor has nothing to show.
- Planning density: about 15 lines per minute of narration.

## Format targets
- **Short:** approximately 100–145 spoken words for 45–60 seconds depending on narration speed; one central claim, one reveal, one payoff.
- **Long:** target runtime and speaking rate together determine length; for 5–7 minutes, approximately 650–950 spoken words is a planning range, not a guarantee. Estimate runtime from final spoken word count; never claim the runtime is tested unless it was timed.
- The voiceover script must be clean narration, without sources, production notes, brackets or shot directions mixed into spoken text. Citations and visual ideas go in `NOTES.md`.

## Inputs in this project
Read before writing, when they exist in `videos/<slug>/`:
- `research/verified_research.md` + `research/gate1_report.md` (facts-checker Gate 1): the facts you may use, required qualifiers, blocked claims, quote bank. If Gate 1 is BLOCK, do not write a publishable script.
- `seo/SEO.md` (target keywords) and `seo/PACKAGING.md` (the approved title + thumbnail concept). **The hook must deliver on the packaging's promise within the first lines**, and the script must never claim more than the evidence supports to match a title.
- `yt-agent/LEARNINGS.md`: lessons from past videos' retention data. Apply every entry marked `RULE`; treat `HYPOTHESIS` entries as preferences.

## Stage A — execution sequence
1. **Input audit:** topic, category, format/duration, research coverage and missing facts.
2. **Evidence map:** extract central claims from the verified pack with source pointers.
3. **Narrative plan:** choose category engine, central question, stakes, turning points, payoff.
4. **Hook set:** three hooks, choose one (consistent with the packaging).
5. **Full voiceover** in Roman Hinglish (unless the user chooses another language).
6. **Shorts moments** (Long videos): mark 2–4 self-contained 20–55 second stretches that work without context: line range, why it works, and a standalone opening line for the Short if the original needs one.
7. **Retention audit** against `references/quality-rubric.md`; scores are subjective editorial judgments, not predictive analytics.
8. **Save** `videos/<slug>/SCRIPT.md` (script only, with a header line: topic · category engine · format · word count · estimated runtime) and `videos/<slug>/NOTES.md` (hooks with rationale, narrative plan, Shorts moments, retention audit, optional visual ideas).
9. **Fact check:** hand the draft to `facts-checker` Gate 2 (it runs automatically, keeps the original in `script_versions/`, and writes the corrected `SCRIPT.md`). Show the user the checked version. If facts-checker is unavailable, do the verification yourself per the integrity rules above and label the result provisional.

### What to show in chat (Stage A)
1. One line: topic · engine · format · words · ~runtime.
2. The **complete script**, ready to read. Mark section breaks with a blank line only (no spoken headings).
3. **Flags only:** Gate 2 status, what it corrected (old → new, one line each), every `[FACT NEEDED]`, disputed or provisional claim, and any hard-stop from the rubric. If none, say so.
4. Hook chosen (one line) + the two alternates (one line each).
5. Retention scores in one compact line, and the top 1–2 fixes, if any.
6. Full paths of SCRIPT.md and NOTES.md, then ask: approve, or what to change.

### Revision loop
The user can change hook, tone, structure, detail, length or claims. Revise SCRIPT.md (keep evidence standards), re-run facts-checker Gate 2 on the changed lines, show only the changed parts plus the new word count, and ask again. The script is approved only on the user's explicit OK.

## Stage B — LINES.tsv for voice and edit
After the OK, write `videos/<slug>/LINES.tsv` (UTF-8, tab-separated, header row):

```
id	text	gap	voice
01	उन्नीस सौ अट्ठानवे की गर्मियों में राजस्थान के रेगिस्तान में कुछ हो रहा था।	0.35	main
```

- **id:** two digits, `01`, `02`, … in script order.
- **text:** the approved line converted to **Devanagari**. The meaning and wording must match the approved script; this is a script conversion, not a rewrite. Whisper word-timing and the Hindi voices both need Devanagari.
  - English words the narrator says go in Devanagari too: सैटेलाइट, इंटेलिजेंस, सीआईए.
  - Numbers, years, dates, money and percentages as spoken words: 1998 → उन्नीस सौ अट्ठानवे, ₹5,000 crore → पाँच हज़ार करोड़ रुपये, 40% → चालीस प्रतिशत.
  - Names as they are said in Hindi; when unsure of a pronunciation, list the name in the chat summary.
  - Keep punctuation that shapes delivery: `।` `?` `,` `...`
- **gap:** seconds of silence after the line. 0.3–0.45 within a passage; 0.6 at the end of a paragraph or after a reveal; about 1.0 before a twist or a new section.
- **voice:** `main` for the narrator (the user's ElevenLabs cloned voice). For a verified quote voiced separately, `kokoro:<voice>` (e.g. `kokoro:am_michael`); a quote in English stays in English Latin script on that line. Only quotes that pass the integrity rules; attribution stays in the narrator's line before it.

Then check: every sentence of the approved script appears once, in order (one sentence per row), no Roman script left in `main` lines, no digits left (Latin or Devanagari), no empty text. Show the user the first five rows, the line count, and the names list, with the full path.

## Reference test case
`How India Fooled America's Spies` / Pokhran-II, 1998: frame as an intelligence warning failure, not a claim that US satellites saw nothing or that detonations went undetected. Explain 1995 vs 1998, Indian operational secrecy, analytical assumptions, tests on 11 and 13 May, and aftermath, only to the degree supported by source evidence. This is an example of standards, not a script to reuse verbatim.

## Related reference
See `references/quality-rubric.md` for a repeatable editorial checklist.

## Owner learnings
Added by the pipeline from the owner's feedback (newest last). These override the general advice above,
but never the fact or copyright rules.
