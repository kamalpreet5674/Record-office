---
name: video-scripter
description: Research-grounded Roman Hinglish documentary scriptwriter for The Records Office (Hindi YouTube on History, Technology, Finance, Current Affairs). Use whenever the user wants a script, voiceover, narration, hook, rewrite or improvement for a Short or Long video, including when the user gives research for a topic, pastes their own script to enhance or check ("isko improve kro", "script better karo", "hook strong karo", "compare karo"), gives line-by-line feedback, or approves a script ("approved", "script ok", "final", "done"). Writes or enhances the script in the user's own style for approval, then after approval produces the Devanagari LINES.tsv and ElevenLabs parts that the voiceover and edit run on. The only script writer in this project.
---

# Video Scripter — The Records Office

## Mission
Turn research, or the user's own draft, into an accurate documentary voiceover that sounds like the user: a question up front, step-by-step cause → effect, a real twist (often the India angle), and an ending that stings. Accuracy is non-negotiable; retention is the editorial goal, never a promised metric.

The user reads and approves every script, so make approval fast: the script first, short flags after, full reports in a file.

## Three modes, one approval gate
- **Write mode:** the user gives research or a topic. Write v1 from scratch (Stage A).
- **Enhance mode:** the user pastes or attaches their own script ("isko improve kro"). Improve it under the Enhance rules below (Stage A).
- **Revise mode:** the user gives feedback on a draft. Change only what they asked for, plus any fact errors (Stage A).
- **Stage B (after the OK only):** Devanagari `LINES.tsv`, then ElevenLabs parts. Never make LINES.tsv for an unapproved draft. If the script changes after approval, regenerate it.

A short OK counts as approval when it answers a script you just showed ("ok", "done", "approved", "final", "chalega"). If the message is ambiguous, ask in one line before Stage B.

## Length comes from the time the user gives. Never ask "Short ya Long?"
1. Read the target time from the request, the planner row (`duration`), or the script's own header line.
2. **Up to 2:00 → Short (9:16). Over 2:00 → Long (16:9).** The user may override ("Long 90 sec").
3. Word budget = seconds × speaking rate. Count words by whitespace in the Roman script, excluding standalone "...". The default rate is **3.0 words/sec** (Roman Hinglish narration after the 1.10× speed-up). If `LEARNINGS.md` has a line `RATE: <n> words/sec` measured from a real voiceover, use that instead. After any voiceover is generated, measure it (words ÷ seconds of the final, sped-up audio) and add or update that `RATE:` line, so runtime estimates stay honest. `yt-agent/tools/script_stats.py` does the maths.
4. If no time is given: in Enhance mode, keep the draft's current length (±10%). In Write mode, choose what the material needs, a Short of 60–90 sec by default or a Long when one central question can't be answered in 110 sec, and state the choice in the header line so the user can change it.
5. Shorts: **60–110 sec** is the working range. Longs: depth decides length; the user prefers a fuller Long over a thin one.

## Workspace and files
- Helper scripts live in `yt-agent/tools/`. If one is missing, create it from Appendix C exactly as written, then run it.
- Every video lives in `yt-agent/videos/<slug>/` (kebab-case slug from the topic; reuse it if it exists).
- Fixed CAPS files at the root: `SCRIPT.md`, `NOTES.md`, `LINES.tsv`. ElevenLabs output goes in `elevenlabs/part_01.txt … FULL.txt`.
- **Back up before every rewrite:** copy the current `SCRIPT.md` to `script_versions/SCRIPT_vN.md` (and `LINES.tsv` to `LINES_vN.tsv`). Never overwrite a version without its backup. In Enhance mode the user's pasted draft is saved as `SCRIPT_v1.md` exactly as given.
- Never move, edit or save into the user's own asset folder or the planner sheet unless they explicitly ask.
- **Header line** (first line of SCRIPT.md and of the chat summary):
  `Title · Niche (engine) · Short 9:16 | Long 16:9 · vN · WORDCOUNT words · ~RUNTIME`

## Inputs to read first (when they exist in `videos/<slug>/`)
- Research comes from the user: pasted in chat, or as files in their asset folder for this video (path in `PROGRESS.md`). Read it there; never move or edit it. From a planner row, read `topic`, `category`, `format`, `duration` when present; if there is no category, infer one and say so.
- `research/verified_research.md` and `research/gate1_report.md` (facts-checker Gate 1): the facts you may use, required qualifiers, blocked claims and the quote bank. If Gate 1 is BLOCK, do not write a publishable script.
- `seo/SEO.md` and `seo/PACKAGING.md`. The hook must deliver the title/thumbnail promise in the first lines, never by claiming more than the evidence supports. Work the primary keyword in naturally.
- `yt-agent/LEARNINGS.md`: apply every `RULE` entry; treat `HYPOTHESIS` entries as preferences; use a `RATE:` line if present.
- **Current Affairs / Finance:** before writing or enhancing, check the live state of the premise with web search (prices, who holds a role, whether something still holds). A stale premise has killed a script before (Blinkit had already turned profitable).

## The user's style (the house voice)
Appendix A has the full style guide with real before/after examples; read it once per session before writing. In short:
- **Hook:** never open on a number or a date. A question or paradox lands within the first ~3 seconds (first 1–2 lines). Proven openers: a paradox ("Jin scientists ne atom bomb banaya..."), a "Socho..." scene, "Khabar hai...", two stacked questions. A number can come *inside* the hook, just not as its first words.
- **Spine:** sawaal → context → escalation → twist (the India angle *when it is real*; never forced) → payoff that answers the hook → final line that is a question to the viewer or a line that stings. No like/subscribe.
- **Story, not explainer:** frame it as a conflict (a war, a bet, a race, a standoff). Explainer-only drafts get rejected.
- **One line, one idea, 5–15 words.** Quotes may run longer. "Same rider. Same store. Zyada paisa."
- **Fillers are required. They make the script sound human.** A line of facts reads like a news bulletin; a filler makes it sound like someone talking to you. Use: "Socho...", "Aakhir kaise?", "Nateeja?", "Matlab...", "Yaani...", "Haan,", "Ab dekhiye...", "Sawaal bas itna hai...", "Ye toh bas shuruaat thi.", "Par ruko...", and "..." for a breath before a reveal. Aim for **at least 4–6 filler beats in a Short** and roughly one every 20–30 seconds in a Long, mixing different ones. Put them where a listener would naturally react: before a number, before a twist, after a shock, at a turn in the story. If a stretch of 4+ lines has no filler, no question and no "...", it is probably reading like a bulletin; add one.
- **Filler beat ≠ dead line.** A filler beat is a short conversational word or question that moves the listener ("Nateeja?"). A dead line is a whole sentence that says nothing new ("Duniya ki nazar in jahaazon par hai."). Keep and add filler beats; cut dead lines.
- **Number ladder** for growth: "Pehle 37 crore. Phir 102. Aur ab... 184." A question-and-reveal works too: "Ek saal pehle? Sirf 65."
- **Say who did what:** "America aur Europe", never a vague "West". Spell cause → effect out step by step so no link is left for the viewer to guess.
- **Banned filmy/cringe lines:** "asli twist", "asli jhatka", "jaal band hua", "sabak", "hathiyaar", "plan perfect lag raha tha", "lekin aage jo hua", and anything in the same family. Use a plain line instead: "Par ek cheez ab bhi nahi badli."
- **Politics:** neutral words. No "mazedaar", no gratuitous nationalism, no partisan framing presented as fact.
- **Long videos:** after the hook, a short "coming up" teaser of the 2–3 biggest beats (Nitish Rajput style), then the story.

## Retention craft (always)
- One central question; smaller curiosity loops whose answers actually arrive. Use question → evidence → explanation → next question naturally, not as artificial cliffhangers.
- Escalate through real decisions, obstacles and consequences. Show causes, don't dump a chronology.
- Turn facts into discoveries: a statistic lands as a reveal, a date as a turning point, a contradiction as a mystery.
- Put documented people at the centre where evidence allows; feelings and motives only when sourced.
- Each reveal is bigger than the last; save the strongest verified reveal for the final third. A Short has one central claim, one reveal and one payoff.
- Never claim a runtime is tested unless the audio was timed.

## Enhance mode (the user's own script)
The user's wording is the asset. Past "punchier" rewrites that replaced their voice were rejected.
1. Save their draft as `script_versions/SCRIPT_v1.md`, word for word.
2. Fact-check every claim before touching style (see integrity rules). Wrong facts are always fixed.
3. Change a line only for one of these reasons, and label the reason:
   - **FACT:** wrong, outdated or overstated.
   - **RULE:** breaks a house rule (hook position, banned line, vague actor, source in VO, line too long, "pratishat").
   - **CLARITY:** a missing cause → effect link, unclear who/when, a jump the viewer can't follow.
   - **BALANCE:** a disputed claim with no attribution or no other side.
   - **HUMANIZE:** add a filler beat where a stretch reads like a bulletin (see the style rules). This is a normal, expected enhancement.
   - **TRIM:** a dead line (a whole sentence with no new information). Never trim the user's filler beats to save time; cut dead lines or wordy phrasing instead.
4. **Keep strong lines even if a style rule points elsewhere.** If the user's line already lands (a short question-reveal, a sharp ending), keep it word for word. Rules exist to make lines land, not to replace lines that already do.
5. Prefer the smallest edit: move a line, add a word ("June mein", "sarkari"), split a sentence, before rewriting anything.
6. Stay inside the time budget. Each added line costs seconds, so pay for it by cutting dead lines or wordy phrasing, never the filler beats.
7. In chat, show the full new script, then each change as `old → new (REASON)`, one line each. Note what you deliberately kept.
8. If the user asks to compare versions, give an honest per-part verdict, including where their version is better, and offer a merged version.

## Narrative engines (adapt the spine to the category)
- **History, cinematic investigation:** intriguing verified moment → context → people/institutions → conflict and escalation → turning point → documented consequences → insight. Substyles: espionage, biography, event reconstruction, rise and fall.
- **Technology, discovery explainer:** surprising capability or question → the underlying problem → the innovation → how it works in plain words → constraints and evidence → impact and limits.
- **Finance, business investigation:** surprising outcome or paradox → incentives and market context → mechanism with relatable examples → decisions and trade-offs → numbers as reveals → consequences. Keep illustrative maths separate from real figures.
- **Current Affairs, evidence-led explainer:** what happened → why it matters to the viewer → verified timeline → competing claims, attributed → what the evidence does and doesn't establish → stakes and uncertainty. Date-stamp anything still moving.
A topic can mix engines (e.g. Finance + Current Affairs). Name the engine in the header.

## Research and factual integrity (non-negotiable)
1. Separate primary documents, credible reporting, commentary, hypotheses and the researcher's or user's own narration.
2. Verify names, chronology, numbers, quotes and causal claims against trustworthy independent sources when tools are available. Never fake verification or citations.
3. Add no factual specifics, dialogue, thoughts, movements, dates or figures that the evidence doesn't support. No fabricated quotes or composites.
4. Keep important uncertainty in the narration with plain spoken hedges: "khabar hai", "daawa", "confirm nahi hua", "andaazan", plus the other side's denial when one exists. Mark unresolved essentials `[FACT NEEDED: ...]` in NOTES.md, never in the spoken script.
5. Don't overstate. Example: in Pokhran-II, US intelligence failed to *predict* the tests; it did not fail to detect explosions.
6. Quotes need a named speaker and a traceable source. A translated quote is marked as a translation in NOTES.md with the original wording. **A paraphrase must keep the speaker's strength:** never soften or sharpen it. Trump's "they'll all be at the bottom of the sea" is a threat to sink ships, not "rok denge". In this project only quotes in the facts-checker quote bank may be used verbatim.
7. **Sources never appear in the voiceover** ("Reuters ke mutabik" goes in the description). All sources go in NOTES.md.
8. No invented visual scene details. Cinematic structure comes from real stakes, contrast, chronology and verified action. A "Socho..." scene must still match the facts: the Hormuz tankers were at the Kharg Island terminal, not "samundar ke beech".
9. No unproven claims about real people. No AI faces of real public figures in visual ideas.

## Write for the edit
- One spoken line = one on-screen idea. Prefer lines that can be *shown*: a place, object, document, number, map or comparison. Give abstract lines a concrete anchor.
- Planning density: about 15 lines per minute.
- The script is clean narration only: no headings, brackets, sources, or shot notes. Mark section breaks with a blank line. Visual ideas go in NOTES.md.

## Stage A — execution sequence
1. **Input audit:** mode, topic, category, target time → format and word budget, research coverage, gaps, live-data check.
2. **Evidence map** (NOTES.md): every claim → status (VERIFIED / REPORTED / DISPUTED / CORRECTED / FACT NEEDED) → source.
3. **Plan:** engine, central question, conflict frame, escalation steps, twist, payoff, final line.
4. **Hooks:** Write mode, three distinct fact-safe hooks, pick one. Enhance mode, keep the user's hook unless it breaks a rule; then offer one alternative.
5. **Script** in Roman Hinglish (unless the user picks another language).
6. **Shorts moments** (Long only): 2–4 self-contained 20–55 sec stretches with line range, why it works, and a standalone opener if needed.
7. **Self-check:** run `python3 yt-agent/tools/script_stats.py SCRIPT.md --target <seconds>`, then score against the rubric in Appendix B. Fix every hard-stop and every flagged line before showing the script. Scores are editorial judgement, not analytics.
8. **Save** SCRIPT.md (header + script) and NOTES.md (evidence map, changes with reasons, hooks, plan, Shorts moments, rubric scores, visual ideas). Back up first.
9. **Fact check:** hand the draft to `facts-checker` Gate 2 (it keeps the original in `script_versions/` and writes the corrected SCRIPT.md). Show the user the checked version. If facts-checker is unavailable, verify yourself per the integrity rules and label the result **provisional**.

### What to show in chat (Stage A)
1. The header line.
2. The **complete script**, ready to read.
3. **Flags:** fact corrections (old → new, with the evidence in one line), anything REPORTED/DISPUTED/FACT NEEDED, the Gate 2 status or "provisional", and any rubric hard-stop. If there are none, say so.
4. Enhance mode: the change list `old → new (REASON)` and what you kept. Write mode: the chosen hook plus two alternates, one line each.
5. Rubric scores in one compact line, plus the top 1–2 fixes, if any.
6. File paths, then ask: approve, or what to change.

### Revision loop
Back up, revise only what was asked (plus fact errors), re-run the Gate 2 check on changed lines, show the full script again with the changes listed and the new runtime, and ask again. The script is approved only on the user's explicit OK.

## Stage B — LINES.tsv for voice and edit
After the OK, back up any old LINES.tsv, then write `videos/<slug>/LINES.tsv` (UTF-8, tab-separated, header row):

```
id	text	gap	voice
01	ख़बर है... ईरान के एक टापू पर चौदह टैंकर तैयार खड़े हैं।	0.35	main
```

- **id:** two digits, `01`, `02`, … in script order. One script line = one row.
- **text:** the approved line in **Devanagari**, same meaning and wording. This is a script conversion, not a rewrite.
  - English words as spoken, in Devanagari: सैटेलाइट, इंटेलिजेंस, ब्रेंट क्रूड.
  - Every number as spoken words; no digits (Latin or Devanagari): 1998 → उन्नीस सौ अट्ठानवे; 2.7 → दो दशमलव सात; ₹10,49,000 crore → दस लाख उनचास हज़ार करोड़ रुपये.
  - **percent → परसेंट** (not प्रतिशत).
  - Names as said in Hindi; list any uncertain pronunciations in chat.
  - Keep delivery punctuation: `।` `?` `,` `...`
  - Devanagari is required because Whisper word-timing and the Hindi voices both need it.
- **gap** (seconds of silence after the line): **0.35** within a passage · **0.6** at a paragraph end · **0.8** right after a reveal · **1.0** at a section break.
- **voice:** `main` for the narrator (the user's ElevenLabs cloned voice). A verified quote voiced separately uses `kokoro:<voice>` (e.g. `kokoro:am_michael`); a quote in English stays in English on that line, with its attribution in the narrator's line before it.

Then run `python3 yt-agent/tools/check_lines.py LINES.tsv SCRIPT.md` and fix everything it reports.

### ElevenLabs parts
Run `python3 yt-agent/tools/make_elevenlabs_parts.py LINES.tsv` to write `elevenlabs/part_NN.txt` (each under 4,000 characters) and `FULL.txt`. It adds `<break>` tags only where the gap is ≥ 0.6.
- **Use one pause system only.** If audio is generated from these parts, the break tags are the pauses; don't also stitch TSV gaps on top, or you get double pauses.
- **Emotion tags** (`[serious]`, `[whispers]`) work only on the Eleven v3 model. On Multilingual v2, use `<break>` only. Never `[clears throat]`; prefer `[serious]` over `[annoyed]`.

Show the user: the first five rows, the line count, the names list, the number of parts and the file paths.

## Reference cases
- **Pokhran-II, 1998** ("How India Fooled America's Spies"): frame it as an intelligence warning failure, not "US satellites saw nothing".
- **Hormuz ke 14 tanker (Nov 2026), Enhance mode:** the user's draft was strong. The right edits were two fact fixes (pump prices did rise in May, so it became "May ke baad se"; the stuck oil is "naakebandi ke andar", not all on ships), adding Iran's denial and Iran's threat to Gulf oil (the missing cause → effect link to the viewer's petrol tank), cutting "Ab asli jhatka" (banned) and the dead line "Duniya ki nazar...", and **keeping** the user's "Ek saal pehle? Sirf 65." over a textbook number ladder. In the user's later v4 draft the same checks caught a softened Trump quote ("rok denge"), a misplaced scene ("samundar ke beech"), the "asli kahani" / "asli jhatka" lines and "pratishat"; every other line was kept word for word.
- **Dollar Short:** eight fixes; see Appendix A.
These show the standard to meet, not scripts to reuse.

---

## Appendix A — House style, with real examples
This is the user's own style, drawn from their revisions on real videos (Oct–Nov 2026). Read it once per session before writing or enhancing. When a rule and a strong user line disagree, the strong line wins.

### 1. The voice in one line
Open with a question, explain cause → effect step by step, give a twist (often the India angle), and end on a question or a line that stings. Roman Hinglish, spoken the way you'd explain it to a friend, never like a bulletin or Wikipedia.

### 2. Hooks
**Works:**
- Paradox: "Jin scientists ne atom bomb banaya... unhi ne duniya ko ek ghadi di." (Doomsday Clock v4)
- Question: "Agar India rupaye mein tel khareed sakta hai, toh duniya ko dollar ki zaroorat hi kyun hai?"
- "Socho..." scene + two stacked questions (US Outages final).
- "Khabar hai..." + tension + paradox question (Hormuz v3).
- A trend hook built on a famous person's real, sourced statement (AI Bijli).

**Fails:**
- Opening on a number or a date (channel audit, Oct 2026: those hooks underperformed).
- A hook the user called "bekar": generic, no suspense (Binance v1).
- Giving away the answer in the first lines.

### 3. Structure
sawaal → context → escalation ("Ye toh bas shuruaat thi.") → twist (India angle when real) → payoff that answers the hook → final question or sting.
- Make it a **story with a conflict frame**: a war, a bet, a race, a standoff. Quick Commerce went v1 explainer → v2 drama → v3 "burn war" story, and only v3 worked.
- Give the main topic the most time (Malacca: the pipeline became the main topic).
- Long videos: a "coming up" teaser first, then story-led narration with fillers. The user said "lambi script jada badhia hai"; don't cut a Long to a thin version (US Midterms v10 rejected).
- A historical parallel can be the twist (Nvidia: the Cisco 2000 parallel, tied to the viewer's SIP/Nasdaq fund, ending "AI boom hai, ya bubble?").

### 4. Fillers make it human (required)
The user wants fillers because they make narration sound like a person, not a bulletin.
- Toolkit: "Socho...", "Aakhir kaise?", "Nateeja?", "Matlab...", "Yaani...", "Haan,", "Ab dekhiye...", "Par ruko...", "Sawaal bas itna hai...", "Ye toh bas shuruaat thi.", and "..." for a breath.
- Placement: before a number, before a twist, after a shock, at a turn. Mix them; don't repeat one in back-to-back lines.
- Density: 4–6+ beats in a Short; about one every 20–30 sec in a Long.
- Quick Commerce v2 and US Outages both improved when fillers were added.
- **Dead lines are different:** "Duniya ki nazar in jahaazon par hai." adds nothing, so cut it. "Nateeja?" adds a beat, so keep it.

### 5. Lines and numbers
- One line, one idea, 5–15 words: "Same rider. Same store. Zyada paisa."
- Number ladder: "Pehle 37 crore. Phir 102. Aur ab... 184."
- Question-and-reveal: "Ek saal pehle? Sirf 65." (the user's line; it beat a textbook ladder).
- Fewer, bigger numbers. Every number must be one the viewer can feel (doubling, per litre, per order).

### 6. Clarity: who did what, and why
- Name the actor: "America aur Europe ne Russia ke... reserves freeze kar diye." Not "West ne".
- Spell out every link in the chain. Dollar fix #5: India bought $63.8B and sold $4.9B → Russia can't spend the rupees → the rupee doesn't work abroad → so sellers started asking for dirham/yuan.
- Hormuz: tankers move → Iran threatens Gulf oil sites if attacked → the price risk → your petrol tank. Without the middle link, the ending was a jump.
- Make the subject explicit at the payoff: "Jis dollar se **Russia** bachna chahta tha..."

### 7. Banned and replaced
| Don't | Do |
|---|---|
| "Plan perfect lag raha tha. Phir jaal band hua." | Cut |
| "Sabak: dollar sirf currency nahi, hathiyaar bhi hai." | Cut, or state the fact plainly |
| "Lekin asli twist ab aata hai" / "Ab asli jhatka" | "Par ek cheez ab bhi nahi badli." / "Ab Bharat ka hisaab." |
| "Reuters ke mutabik" in the voiceover | Put the source in the description; in the VO, use a hedge if needed ("khabar hai", "confirm nahi hua") |
| "Chowkidaar", "chaabi" metaphors that pull focus (Malacca) | A literal description of the thing |
| A cashier-tijori analogy for crypto (Binance) | Simple real terms |
| "Mazedaar" and other loaded words in politics (US Midterms) | Neutral words |
| Like/subscribe at the end | A question to the viewer, or a sting: "Ab aapke paise se ladi jaayegi." |

### 8. Editing the user's lines
- When fixing facts, don't change their wording (Undersea Cables: a "punchier" v2 was rejected; v1's wording was kept with only the facts fixed).
- Smallest edit first: add a word, move a line, split a sentence.
- Show every change as old → new with its reason.

### 9. Freshness
- For Current Affairs and Finance, check live data before writing. Quick Commerce's premise was stale because Blinkit had already turned profitable.
- Date-stamp moving numbers in NOTES.md (e.g. "Jefferies, 13 Nov, 15-day average").

### 10. Voiceover (ElevenLabs)
- Digits never go to ElevenLabs; write numbers as words (AI Bijli).
- Emotion tags only on the v3 model; on Multilingual v2 use `<break>` only (Binance).
- Use one pause system only: break tags or TSV gaps, never both (Binance).
- Remove `[clears throat]`; `[serious]` reads better than `[annoyed]`.
- Keep each part under 4,000 characters; break tags only at section/paragraph ends (more tags made the voice sound odd).

## Appendix B — Quality rubric
Use this after `yt-agent/tools/script_stats.py` and before showing the script. Scores are editorial judgement, not predictions. Fix every hard-stop first.

### Hard-stops (any one = not ready to show)
1. A factual claim that is wrong, outdated or unsupported, or a disputed claim stated as fact.
2. A fabricated or untraceable quote, or invented dialogue, thoughts or scene detail.
3. The hook opens on a number or a date, or no question/paradox lands in the first ~3 seconds.
4. A source name in the spoken script ("Reuters ke mutabik").
5. A banned filmy line (see Appendix A §7).
6. The ending doesn't answer the hook, or it ends on like/subscribe.
7. Runtime more than ±15% off the target the user gave.
8. Enhance mode: a user line was rewritten with no labelled reason, or a strong user line was replaced by a weaker "rule-compliant" one.
9. `[FACT NEEDED]` or brackets inside the spoken script.

### Scored dimensions (1–10 each; target ≥ 8 on every line before showing)
| # | Dimension | 10 looks like |
|---|---|---|
| 1 | **Accuracy and attribution** | Every claim maps to a source in NOTES.md; uncertain claims are hedged in plain speech; the other side is present where disputed |
| 2 | **Hook (first 3 sec)** | A paradox or question the viewer must answer; it delivers the title/thumbnail promise; no number/date first |
| 3 | **Story and conflict** | A clear conflict frame; one central question; each step raises stakes; reads as a story, not an explainer |
| 4 | **Cause → effect clarity** | Every link is spoken; named actors; no jump the viewer must guess |
| 5 | **Human voice (fillers)** | 4–6+ varied filler beats in a Short (one every 20–30 sec in a Long), at natural reaction points; no stretch of 4+ bulletin lines |
| 6 | **Numbers that land** | Few, felt numbers delivered as reveals (ladder or question-reveal); illustrative maths separate from real data |
| 7 | **Twist and payoff** | A real twist (India angle when genuine); the payoff answers the hook; the last line stings or asks |
| 8 | **Line craft** | 5–15 words per line; one idea per line; every line showable on screen |
| 9 | **User's voice kept** (Enhance) / **house voice** (Write) | User wording intact except labelled changes; sounds like The Records Office |
| 10 | **Time fit** | Runtime within ±10% of target; the main topic gets the most time |

Compact chat line format:
`Scores: Acc 9 · Hook 9 · Story 8 · Clarity 9 · Human 9 · Numbers 9 · Payoff 9 · Lines 9 · Voice 10 · Time 9`

### Self-check questions
- Would a viewer who skipped the first 10 seconds still know the central question by second 15?
- Is there any line I'd be embarrassed to defend with a source?
- Read it aloud: where does it sound like a newsreader? Add a filler beat there.
- Which line is the user's best? Is it still there, word for word?

## Appendix C — Helper scripts
Create these once in `yt-agent/tools/` (skip any that already exist and run cleanly).

### `yt-agent/tools/script_stats.py`
```python
#!/usr/bin/env python3
"""Check a Roman Hinglish SCRIPT.md against the house rules.

Usage:
  python3 script_stats.py SCRIPT.md [--target SECONDS] [--rate WORDS_PER_SEC] [--learnings LEARNINGS.md]

Reports word count, estimated runtime, Short/Long, filler beats, and every
line that breaks a mechanical rule. It can't judge story or accuracy; use
the quality rubric (Appendix B of the skill) for that.
"""
import argparse
import re
import sys
from pathlib import Path

DEFAULT_RATE = 3.0  # words/sec, Roman Hinglish after the 1.10x speed-up; calibrate via LEARNINGS.md RATE:

FILLERS = [
    "socho", "aakhir kaise", "nateeja", "matlab", "yaani", "haan,", "ab dekhiye",
    "par ruko", "sawaal bas itna hai", "ye toh bas shuruaat thi", "khabar hai",
    "aur ab", "phir bhi", "samjhiye", "dekhiye",
]
BANNED = [
    "asli twist", "asli jhatka", "jaal band", "sabak", "hathiyaar", "plan perfect",
    "lekin aage jo hua", "mazedaar", "like karein", "like karo", "subscribe",
    "bell icon",
]
SOURCE_WORDS = [
    "reuters", "bloomberg", "pti", "ani", "kpler", "jefferies", "wikipedia",
    "times of india", "bbc", "cnn", "fox news", "ke mutabik", "ki report",
]
MONTHS = ("january february march april may june july august september october "
          "november december").split()


def words(text):
    return [w for w in text.split() if re.search(r"\w", w)]


def read_rate(learnings):
    if not learnings or not Path(learnings).exists():
        return None
    m = re.search(r"RATE:\s*([\d.]+)", Path(learnings).read_text(encoding="utf-8"))
    return float(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--target", type=float, help="target runtime in seconds")
    ap.add_argument("--rate", type=float, help="words per second")
    ap.add_argument("--learnings", help="path to LEARNINGS.md with a RATE: line")
    a = ap.parse_args()

    raw = Path(a.script).read_text(encoding="utf-8").splitlines()
    header = None
    if raw and " · " in raw[0]:
        header, raw = raw[0], raw[1:]
    lines = [l.strip() for l in raw if l.strip()]
    if not lines:
        sys.exit("No script lines found.")

    rate = a.rate or read_rate(a.learnings) or DEFAULT_RATE
    n = sum(len(words(l)) for l in lines)
    secs = n / rate
    fmt_basis = a.target if a.target else secs
    fmt = "Short 9:16" if fmt_basis <= 120 else "Long 16:9"

    print(f"Header: {header or '(none)'}")
    print(f"Lines: {len(lines)} | Words: {n} | Rate: {rate} w/s | Est. runtime: ~{secs:.0f} sec ({secs/60:.1f} min) | Format: {fmt}")
    if a.target:
        diff = (secs - a.target) / a.target * 100
        budget = round(a.target * rate)
        flag = "OK" if abs(diff) <= 10 else ("WARN" if abs(diff) <= 15 else "HARD-STOP")
        print(f"Target: {a.target:.0f} sec -> budget ~{budget} words | off by {diff:+.0f}% [{flag}]")

    issues = []
    first = lines[0].lower()
    ft = words(first)
    if ft and (re.match(r"^[\d₹$]", ft[0]) or ft[0].strip(".,") in MONTHS):
        issues.append(("HARD-STOP", 1, "Hook opens on a number or date", lines[0]))
    opening = " ".join(lines[:3])
    if "?" not in opening and not any(k in opening.lower() for k in ("socho", "khabar hai")):
        issues.append(("WARN", 1, "No question/paradox in the first 3 lines", lines[0]))

    filler_hits = 0
    since_beat = 0
    for i, l in enumerate(lines, 1):
        low = l.lower()
        wc = len(words(l))
        is_quote = '"' in l or "“" in l
        if wc > 15 and not is_quote:
            issues.append(("WARN", i, f"Line has {wc} words (max 15)", l))
        for b in BANNED:
            if b in low:
                issues.append(("HARD-STOP", i, f"Banned phrase: '{b}'", l))
        for s in SOURCE_WORDS:
            if re.search(r"\b" + re.escape(s.strip()) + r"\b", low):
                issues.append(("CHECK", i, f"Possible source in voiceover: '{s.strip()}'", l))
        if "pratishat" in low or "pratisat" in low:
            issues.append(("WARN", i, "Use 'percent', not 'pratishat'", l))
        if re.search(r"\[|\]|FACT NEEDED", l):
            issues.append(("HARD-STOP", i, "Brackets/markers in the spoken script", l))
        beat = any(f in low for f in FILLERS) or "?" in l or "..." in l
        if any(f in low for f in FILLERS):
            filler_hits += 1
        since_beat = 0 if beat else since_beat + 1
        if since_beat == 4:
            issues.append(("WARN", i, "4 lines in a row with no filler/question/'...': reads like a bulletin", l))

    need = 4 if fmt.startswith("Short") else max(4, int(secs / 25))
    print(f"Filler beats: {filler_hits} (aim >= {need})" + ("" if filler_hits >= need else "  <-- add more to humanize"))
    last = lines[-1]
    if "?" not in last and len(words(last)) > 15:
        issues.append(("WARN", len(lines), "Ending is neither a question nor a short sting", last))

    if not issues:
        print("No mechanical issues found.")
    for sev, i, msg, l in issues:
        print(f"[{sev}] line {i}: {msg}\n    {l}")
    sys.exit(1 if any(s == "HARD-STOP" for s, *_ in issues) else 0)


if __name__ == "__main__":
    main()
```

### `yt-agent/tools/check_lines.py`
```python
#!/usr/bin/env python3
"""Validate LINES.tsv before it goes to the voice and edit stages.

Usage: python3 check_lines.py LINES.tsv [SCRIPT.md]
Exits 1 if anything must be fixed.
"""
import csv
import re
import sys
from pathlib import Path

ALLOWED_GAPS = {0.35, 0.6, 0.8, 1.0}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    tsv = Path(sys.argv[1])
    errs, warns = [], []
    with tsv.open(encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        rows = list(reader)
    if not rows or rows[0] != ["id", "text", "gap", "voice"]:
        errs.append(f"Header must be: id<TAB>text<TAB>gap<TAB>voice (got {rows[0] if rows else 'nothing'})")
    body = rows[1:]
    for n, r in enumerate(body, 1):
        if len(r) != 4:
            errs.append(f"row {n}: expected 4 columns, got {len(r)}")
            continue
        rid, text, gap, voice = r
        if rid != f"{n:02d}":
            errs.append(f"row {n}: id '{rid}' should be '{n:02d}'")
        if not text.strip():
            errs.append(f"row {n}: empty text")
        if re.search(r"[0-9०-९]", text):
            errs.append(f"row {n}: digits left, write numbers as words: {text}")
        if voice == "main":
            if re.search(r"[A-Za-z]", text):
                errs.append(f"row {n}: Roman letters in a main line, convert to Devanagari: {text}")
        elif not voice.startswith("kokoro:"):
            errs.append(f"row {n}: voice must be 'main' or 'kokoro:<voice>' (got '{voice}')")
        if "प्रतिशत" in text:
            errs.append(f"row {n}: use परसेंट, not प्रतिशत")
        try:
            g = float(gap)
            if g not in ALLOWED_GAPS:
                warns.append(f"row {n}: gap {gap} is not one of 0.35 / 0.6 / 0.8 / 1.0")
        except ValueError:
            errs.append(f"row {n}: gap '{gap}' is not a number")
        if re.search(r"\[[^\]]+\]", text):
            warns.append(f"row {n}: emotion tag found; it only works on Eleven v3: {text}")

    if len(sys.argv) > 2:
        lines = Path(sys.argv[2]).read_text(encoding="utf-8").splitlines()
        if lines and " · " in lines[0]:
            lines = lines[1:]
        spoken = [l for l in lines if l.strip()]
        if len(spoken) != len(body):
            errs.append(f"SCRIPT.md has {len(spoken)} lines but LINES.tsv has {len(body)} rows: one line per row")

    print(f"{len(body)} rows checked.")
    for w in warns:
        print("[WARN]", w)
    for e in errs:
        print("[FIX]", e)
    if not errs and not warns:
        print("All good.")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
```

### `yt-agent/tools/make_elevenlabs_parts.py`
```python
#!/usr/bin/env python3
"""Split LINES.tsv into ElevenLabs text parts (each < 4,000 characters) plus FULL.txt.

Usage: python3 make_elevenlabs_parts.py LINES.tsv [--out elevenlabs] [--voice main]

Adds a <break> tag only where the gap is >= 0.6 (paragraph/section ends),
because more tags make the voice sound odd. These break tags are the pause
system; don't also stitch TSV gaps on top of audio made from these parts.
Only lines for the chosen voice (default: main) are included.
"""
import argparse
import csv
from pathlib import Path

LIMIT = 4000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tsv")
    ap.add_argument("--out", default=None, help="output folder (default: elevenlabs/ next to the TSV)")
    ap.add_argument("--voice", default="main")
    a = ap.parse_args()

    tsv = Path(a.tsv)
    out = Path(a.out) if a.out else tsv.parent / "elevenlabs"
    with tsv.open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f, delimiter="\t") if r["voice"] == a.voice]

    parts, cur = [], ""
    for r in rows:
        line = r["text"].strip()
        gap = float(r["gap"])
        if gap >= 0.6:
            line += f' <break time="{gap:.1f}s" />'
        line += "\n"
        if cur and len(cur) + len(line) > LIMIT:
            parts.append(cur)
            cur = ""
        cur += line
    if cur:
        parts.append(cur)

    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("part_*.txt"):
        old.unlink()
    for i, p in enumerate(parts, 1):
        (out / f"part_{i:02d}.txt").write_text(p, encoding="utf-8")
    (out / "FULL.txt").write_text("".join(parts), encoding="utf-8")
    print(f"{len(rows)} lines -> {len(parts)} part(s) in {out}")


if __name__ == "__main__":
    main()
```

## Owner learnings
Added by the pipeline from the owner's feedback (newest last). These override the general advice above,
but never the fact or copyright rules.
- 2026-11-23: Make the first draft a bit more dramatic (Socho opener, "..." pauses, "Par ruko..." question, "asli jhatka" before the twist, short punchy reveal lines). Drama in delivery only; facts unchanged.
- 2026-11-23: Clarity first: one central question, step-by-step cause chain, max 4-5 numbers per Short; a plain "Shuru se samajhiye" bridge after the hook helps.
- 2026-11-23 (skill v2 from owner): "asli jhatka" is now on the banned filmy-lines list. The v2 ban wins over the 23 Nov line above; keep the drama with "..." and "Par ruko..." instead.
- Pipeline note: in this repo, workspace is `videos/<dir>/` and helper tools go in `scripts/` (not `yt-agent/`); Short length for the daily pipeline stays 60-70 sec as set in CLAUDE.md.
