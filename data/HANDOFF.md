# Handoff: where we stopped (23 Nov 2026, ~13:00 Dubai)

Read this first in a new session, then CLAUDE.md, style/LEARNINGS.md, style/EDIT_STYLE.md.

## Status
- **GTA 6 Short** (`videos/2026-11-23-gta6-day-one-record/`): final v10 uploaded **private**, YouTube id `lTsBPU2qweU`
  (https://youtube.com/shorts/lTsBPU2qweU). Owner has not said "OK" for public yet. If he says OK: set public
  (`videos().update` privacyStatus=public); if YouTube refuses (unverified API app lock), tell him to make it public in Studio.
  Pinned comment to give him: "Aapke hisaab se agla superstar kaun hoga: film star ya game? Comment mein batao."
- **Iran blockade / India oil bill Short** (`videos/2026-11-23-iran-blockade-india-oil-bill/`): script v2 approved,
  NOT built. Owner decided not to upload a 2nd video today -> status `on_hold`. It is Current Affairs: before using it
  later, re-check every fact and date (prices, "23 November tak", tanker status) and send a refreshed script.
- Routines are NOT created yet (owner creates them in claude.ai/code with the Gmail connector; prompts in ROUTINE_PROMPT.md).
- YouTube comment-reply permission: owner still has to re-run get_youtube_token.py and update YT_REFRESH_TOKEN.

## How the owner wants videos (all saved as rules)
- Scripts: dramatic but fact-first, clarity (one question, step-by-step, max 4-5 numbers), India angle when new.
- Edit: pro hook in first 3 s, new visual every 2-3 s, mostly VIDEO (script-literal b-roll), official trailer clips muted
  allowed for game/brand topics (credited), cutouts (rembg), cards, punch/flash/shake/glitch/leak fx, LUT grade,
  captions a little below centre (CAPTION_MARGIN_V=560), strong BGM + layered SFX but **voice always 10+ dB on top**.
- Previews go to the owner in chat; upload only after his OK. Every email/upload/problem also gets a phone ping (ntfy).

## Build command used for the final
```
GRADE="lut3d=file=<dir>/assets/luts/DAEDAL_02_Product_Pop.cube:interp=tetrahedral,eq=saturation=1.1:contrast=1.03,unsharp=5:5:0.5,vignette=PI/5,noise=alls=4:allf=t" \
CAPTION_MARGIN_V=560 MUSIC_START=14 MUSIC_VOL=0.1 python scripts/assemble_short.py videos/<dir>
```
Big media (stock clips, trailer, music, final mp4) is git-ignored: a new container must re-download it
(sources listed in assets/*/CREDITS.md and data/asset_sources.md).

## Tools
scripts/setup.sh installs: ffmpeg, playwright, gdown, rembg, librosa, faster-whisper, hyperframes.
