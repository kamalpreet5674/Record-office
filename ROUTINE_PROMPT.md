# Prompts for the routines (claude.ai/code → Routines)

Every routine: repo **Record-office**, environment **Records office**, time zone **Dubai**,
allow pushing to main. Times come from `config/settings.md` (morning slot 08:15, evening slot 19:00).

## Routine A1: "RO evening script (Short 1)", every day 8:00 PM
```
Phase A (script run), only Short 1 (History/Geography/Technology) for tomorrow's morning slot.
Follow CLAUDE.md in this repo exactly. Do fresh trend and competitor research, use
data/channel_insights.md, write the Short 1 script (60 to 70 seconds) in my style.
Verify every fact with two sources; if a topic fails a gate, pick another.
Email the script to me for approval, update data/pending.csv, commit and push. Then stop.
```

## Routine A2: "RO morning script (Short 2)", every day 9:00 AM
```
Phase A (script run), only Short 2 (Finance/Geopolitics/Current Affairs) for today's evening slot.
Follow CLAUDE.md in this repo exactly. Do fresh trend and competitor research, use
data/channel_insights.md, write the Short 2 script (60 to 70 seconds) in my style.
Verify every fact with two sources; if a topic fails a gate, pick another.
Email the script to me for approval, update data/pending.csv, commit and push. Then stop.
```

## Routine B: "RO check replies + make videos", daily at 5 AM, 6 AM, 10 AM, 12 PM, 2 PM, 4 PM, 5 PM, 9 PM
(If the app allows only one time per routine, make it "every hour" or create a few copies.)
```
Phase B (check run). Follow CLAUDE.md in this repo exactly. Read my email replies to the
RO-SCRIPT emails. Approved scripts: make voiceover, video and upload for its publish slot,
then email me the link and notify my phone. Scripts with changes: revise, re-check facts, and
email the new version. Also handle RO-DONE replies (feedback → rules and skills), check ElevenLabs credits,
and reply to new comments (sensitive ones: email me drafts). Update data/pending.csv, commit and push.
If nothing is pending and there are no new comments, end quickly.
```

## Routine C: "RO audit", every 3 days at 10:30 PM
```
Phase C (audit run). Follow CLAUDE.md "Phase C" exactly: run the audit, learn from the numbers
(including posting time), update style/LEARNINGS.md, data/channel_insights.md and the publish slots
in config/settings.md if the data clearly says so, email me the audit, commit and push.
```

## Routine L: "RO long video topic ideas", every Thursday 9:00 PM
```
Phase L (topic ideas run). Follow CLAUDE.md "Phase L" exactly: find the 3 best topics for my
next long video (I make it myself), with proof, angle, chapters and sources, email them to me
as RO-LONG-IDEAS, commit and push. Then stop.
```

## Setup check (run once, any time, in a normal session)
```
Run: git pull && bash scripts/setup.sh && python scripts/check_setup.py
Show me the OK/FAIL lines. Do not print any secret value. If something fails, tell me which key
to fix in the environment settings. Change no files.
```

## Manual test prompts (first time, in a normal session)
```
Test run. Follow CLAUDE.md Phase A but make only Short 1, and email it to me.
Show me each stage here too (topic, sources, script). Stop after the email.
```
After you reply to that email:
```
Test run. Follow CLAUDE.md Phase B: check my reply and, if approved, make the video and
upload it as private. Show me the frames and the link.
```
