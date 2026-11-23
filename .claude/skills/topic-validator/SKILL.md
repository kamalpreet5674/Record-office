---
name: topic-validator
description: Validate a documentary topic for The Records Office before any research starts. Checks whether enough credible sources exist, whether it can perform on YouTube (demand, competition, outliers), whether visuals exist (or need 3D/AI reconstruction), risk, shelf life and brand fit, then gives GO / REFRAME / NO-GO. Use for "is this topic good", "validate topic", "check this topic", "chalega ya nahi", or as step 2 of a new video.
---

# Topic Validator

Talk to the user in Hinglish. This is a gate: no research prompts until the user accepts the verdict.

## Setup
1. Workspace: `yt-agent/videos/<slug>/` (English, lowercase, hyphens). Create it and `PROGRESS.md` (topic, category, format if known, asset folder path if given, stage table) if they don't exist.
2. Read `yt-agent/LEARNINGS.md` for what past videos taught about categories, angles and topics.

## The seven checks (score each 1–5, with the evidence behind the score)
1. **Research availability.** Web-search for primary records (archives, official documents, filings, papers, court records) and strong secondary sources (books, scholarly work, named-source reporting). List the best 5–10 with links. Score low if the story rests on one source, memoirs only, or rumours.
2. **Demand.** Run the scan with English and Hindi/Hinglish queries:
   `python <skill>/scripts/yt_topic_scan.py "<english query>" "<hindi query>" --n 15 --out videos/<slug>/topic`
   It ranks each result by views over its own channel's median (newest 3 uploads skipped). Read multiples with care: news channels upload daily and have low medians, so their multiples run high; documentary/explainer channels are the fair comparison. If the vidIQ connector is available, add keyword search volume and competition for the main queries. Optionally `yt-viral`'s `swipe.py` on `topic/scan.json` for the title formulas.
3. **Competition and gap.** From the scan: how many solid videos already exist, in Hindi vs English, how big and how recent. Name the angle nobody has done well yet. "Already covered" is fine if we can add a new record, a sharper question, or better visuals.
4. **Visual availability.** Probe the free licensed sources with `footage-finder`'s search (`--probe`): Wikimedia Commons, Openverse, NASA, Library of Congress. Count usable photos/clips for the key people, places and events. If real material is scarce, plan 3D/AI reconstruction with Flow (maps, objects, environments, abstract recreations) and note it. Realistic recreations of real events or people need YouTube's altered/synthetic label, and real politicians are never faked.
5. **Risk.** Political sensitivity, defamation exposure (named living people, allegations), advertiser-friendliness, graphic content, Content ID (news footage dependency), ongoing legal cases. Score 1 = safe, 5 = needs the user's explicit decision.
6. **Shelf life.** Evergreen (years of search traffic) vs timely (spike then decay). Timely topics need a fast turnaround; say how fast.
7. **Brand fit.** Does it fit The Records Office angle: a "record" or "file" that reveals what really happened? Suggest the framing.

## Verdict
- **GO:** checks 1, 2 and 4 at 3+, risk manageable.
- **REFRAME:** good topic, wrong angle; give the new angle (and why the scan supports it).
- **NO-GO:** too thin on sources, no demand, or risk not worth it. Say what would change the verdict.
Never inflate scores to make a topic pass; the user wants to know before spending research time.

## Output
Save `videos/<slug>/topic/TOPIC.md`:
- Topic · category · suggested format (Short/Long) and why
- Scorecard table (check · score · evidence)
- Top competitor videos (title · channel · views · multiple · link) and the gap
- Best sources found (links)
- Visuals plan: real material available vs reconstruction needed
- Risks and how to handle them
- Working angle + 2–3 working title directions (final title and thumbnail come later in `seo/PACKAGING.md`)
- Verdict

In chat: verdict first, the scorecard in one compact table, the angle, the top 3 risks or gaps, and the file path. Then ask: **GO karein, angle badlein, ya topic chhodein?** Update `PROGRESS.md` once the user decides.

## Owner learnings
Added by the pipeline from the owner's feedback (newest last). These override the general advice above,
but never the fact or copyright rules.
