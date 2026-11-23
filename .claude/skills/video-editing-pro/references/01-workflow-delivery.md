# Workflow and delivery

## 1. Brief (fill before anything)
| Field | Example |
|---|---|
| Goal (feel/do at end) | curiosity → comment/subscribe |
| Audience / language / device | 18–34, Hinglish, phone |
| Platform + aspect | Shorts 1080×1920 |
| Length (hard max / ideal) | 60–110 s |
| Pacing | new beat every 2–4 s |
| References (2–3) | Vox explainer, documentary collage |
| Deliverables | MP4 + SRT + thumbnail + CREDITS.md |

Platform facts: YouTube classes any square/vertical upload up to 3 min as a Short (since 15 Oct 2024); publish 16:9 to stay long-form. Instagram Reels max length varies by account/route (90 s to 20 min reported) — check the app; under ~3 min for reach.

## 2. Hook and retention
- Frame 0 = thumbnail + hook: a face, the result, or one bold line already on screen. Never black, never a logo.
- First second decides the swipe (Shorts); YouTube's "Intro" metric = % still watching after 30 s, high when the opening matches the title/thumbnail promise.
- Hook → deliver → next hook, repeated (don't stop hooking after the intro). Paradox or question hooks beat number/date openers (channel lesson).
- Many watch muted: picture + captions must carry the hook.

## 3. Folders and naming
```
PROJECT_YYYYMMDD_slug/
  00_brief/ (brief.md, EDIT_PLAN.md, DECISIONS.log)   01_script/ (SCRIPT.md, LINES.tsv, versions/)
  assets/raw/ (+CREDITS.json/md)  assets/video/  assets/audio/{vo,music,sfx}  assets/fonts/
  compositions/ (one scene per file)  renders/{draft,final}/  snapshots/  09_check/QC.md
```
Name: `PROJECT_SCENE_SHOT_TAKE_vNN.ext`, zero-padded. Proxies keep the name + `_proxy` (HyperFrames auto-proxies undecodable codecs).

## 4. Rough cut → fine cut → lock
1. Radio edit (VO/interview only) until the story works as audio.
2. Structure: hook (0–3 s) → stakes → 2–3 escalating beats → payoff → question/CTA.
3. Every claim that can be shown gets a real visual (see `08-real-assets.md`); every number appears on screen.
4. Remove dead air (pauses > ~300 ms unless emotional), false starts, repeats.
5. Fine cut: trim to beats, J/L-cuts, match cuts, cut on action, eye-trace continuity.
6. Picture lock → sound → colour → graphics/captions → transitions polish → QC → export.

## 5. Export / delivery
HyperFrames: `render --quality standard` (or `--crf`, `--video-bitrate`), `--fps` = source fps.
Other NLE / ffmpeg master:
```bash
ffmpeg -i master.mov -c:v libx264 -preset slow -crf 17 -profile:v high -pix_fmt yuv420p \
 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 384k -ar 48000 -movflags +faststart out.mp4
```
YouTube recommended: MP4, moov at front, H.264 High, progressive, VBR, 4:2:0, native fps, BT.709 SDR, AAC stereo 384 kbps (mono 128, 5.1 512).
| Resolution | SDR 24–30 fps | SDR 48–60 fps |
|---|---|---|
| 1440p | 20 Mbps | 30 Mbps |
| 1080p | 10 Mbps | 15 Mbps |
| 720p | 6.5 Mbps | 9.5 Mbps |
(figures from YouTube's help page at research time — re-check before delivery)

Thumbnail: 1280×720, < 2 MB. Captions: export SRT/VTT (`npx hyperframes transcribe … --to srt`).
AI disclosure: tick YouTube's altered/synthetic setting when realistic AI content is shown.
Credits: paste `CREDITS.md` into the description.

## 6. Delivery note (REVIEW.md)
Creative calls made; what was measured vs only looked at; weakest shot and the fix with more time; warnings kept on purpose.
