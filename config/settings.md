# Run settings (edit these any time)

- **Shorts per run:** 2
- **Length:** 60 to 70 seconds
- **Time zone:** Asia/Dubai (change if you prefer IST)
- **Script approval:** by email before any video is made (scripts/mail.py, subject tag RO-SCRIPT)
- **Publish mode:** `private`
  - `private`: upload private, owner checks and makes public (default; also forced by YouTube until Google audits the app)
  - `scheduled`: upload private with publish_at at the publish slots below (only after Google's audit)
  - `public`: publish immediately (only when you fully trust the pipeline)
- **Niches / categories:** History, Technology, Finance, Current Affairs
- **Audience region:** India (regionCode IN), Hindi/Hinglish
- **Voice:** ElevenLabs voice in secret ELEVENLABS_VOICE_ID, model eleven_multilingual_v2
- **Look:** see style/EDIT_STYLE.md

## Publish slots (Dubai time). Phase C may move these when the numbers say so.
- **Morning slot: 07:00**, Short 1 (History / Geography / Technology)
- **Evening slot: 19:00**, Short 2 (Finance / Geopolitics / Current Affairs)

## Routine times (set in claude.ai/code → Routines, Dubai time)
| Routine | When | What |
|---|---|---|
| A1 evening script | daily 20:00 | Phase A, only Short 1 (for next morning 07:00) |
| A2 morning script | daily 09:00 | Phase A, only Short 2 (for 19:00 today) |
| B check replies | daily 05:00, 10:00, 12:00, 14:00, 16:00, 17:00, 21:00, 23:00 | Phase B |
| C audit | every 3 days 22:30 | Phase C |

## Slot history
- 2026-11-23: owner chose 07:00 and 19:00 to start.
