# Prompts for the two daily routines

## Routine A: "Records Office: morning scripts", every day 6:00 AM
```
Phase A (script run). Follow CLAUDE.md in this repo exactly. Do fresh trend and competitor
research and make today's 2 Short scripts (Short 1: History/Geography/Technology,
Short 2: Finance/Geopolitics/Current Affairs), 60 to 70 seconds each, in my style.
Verify every fact with two sources; if a topic fails a gate, pick another.
Email each script to me for approval, update data/pending.csv, commit and push. Then stop.
```

## Routine B: "Records Office: check replies and make videos", every 2 hours, 8 AM to 10 PM
```
Phase B (check run). Follow CLAUDE.md in this repo exactly. Read my email replies to the
RO-SCRIPT emails. Approved scripts: make voiceover, video and upload, then email me the link.
Scripts with changes: revise, re-check facts, and email the new version.
Update data/pending.csv, commit and push. If nothing is pending, end quickly.
```

## Manual test prompt (first time, in a normal Claude Code session)
```
Test run. Follow CLAUDE.md Phase A but make only Short 1, and email it to me.
Show me each stage here too (topic, sources, script). Stop after the email.
```
After you reply to that email, run this in a session:
```
Test run. Follow CLAUDE.md Phase B: check my reply and, if approved, make the video and
upload it as private. Show me the frames and the link.
```
