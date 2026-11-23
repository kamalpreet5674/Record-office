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
- **Evening slot: 17:30**, Short 2 (Finance / Geopolitics / Current Affairs)
- **Long videos:** made by the owner; the pipeline only sends topic ideas (Phase L)

## Routine times (set in claude.ai/code → Routines, Dubai time)
| Routine | When | What |
|---|---|---|
| A1 evening script | daily 20:00 | Phase A, only Short 1 (for next morning 07:00) |
| A2 morning script | daily 09:00 | Phase A, only Short 2 (for 17:30 today) |
| B check replies | daily 06:00, 10:00, 12:00, 14:00, 15:00, 16:00, 21:00, 23:00 | Phase B |
| C audit | every 3 days 22:30 | Phase C |
| L long-video ideas | weekly, Thursday 21:00 | Phase L, 3 topic ideas emailed to the owner |

## Owner's reply window
The owner can reply between **05:00 and 22:00 Dubai**. Never expect a reply outside it:
- Short 1 script arrives 20:00; reply by 22:00 → built at 23:00, or reply 05:00-06:00 → built at 06:00 for 07:00.
- Short 2 script arrives 09:00; reply by 16:00 → built at 16:00 for 17:30.
- Reminders, alerts and non-urgent emails go out only between 05:00 and 22:00.

## Slot history
- 2026-11-23: owner chose 07:00 and 19:00 to start.
- 2026-11-23: evening slot moved to 17:30 Dubai (19:00 IST) after the first audit: Shorts posted 15:00-18:00
  Dubai averaged 688 views at 60.6% viewed vs 606 views at 48.5% for 18:00-21:00 (14 Shorts, small sample).
  Morning 07:00 kept as a test (only 1 earlier Short in that window). Re-check at 6+ Shorts per window.
