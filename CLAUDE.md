# The Records Office: daily Shorts factory

You run unattended every morning. Nobody is watching while you work, so you follow this file
exactly, you never guess a fact, and you stop a video rather than publish something unverified.

Channel: **The Records Office**, Hindi/Hinglish documentary Shorts on History, Technology,
Finance and Current Affairs. Brand promise: *the record that shows what really happened.*
Facts first, always.

## Daily target
- **2 Shorts per day**, each **60 to 70 seconds**, vertical 1080x1920, 30 fps.
  - **Short 1**: History, Geography or Technology.
  - **Short 2**: Finance, Geopolitics/Civics or Current Affairs.
- Every Short must be brand new: not already on the channel, not made in an earlier run.

## Two phases with an email approval in between
The owner approves every script by email before any voice or video is made.
- **Phase A, "script run"** (6:00 AM): research, validate, fact-check and write both scripts, then
  email them to the owner and stop. Steps 1 to 5 and 5b below.
- **Phase B, "check run"** (several times a day): read the owner's email replies. Approved scripts
  go through steps 6 to 10. Scripts with changes are revised, re-checked and emailed again.
The run prompt says which phase you are. Never make voice, video or uploads for a script whose
status in `data/pending.csv` is not `approved`.

## Files you must read at the start of every run
1. `style/MY_SCRIPT_STYLE.md`: the owner's own script style. It wins over any style advice in the
   skills, but never over the fact rules below.
2. `style/EDIT_STYLE.md`: how the Shorts look and move.
3. `style/LEARNINGS.md`: lessons from past Shorts. Apply every line marked `RULE`.
4. `config/settings.md`: publish mode, voice, niches, competitors.
5. `data/topics_log.csv`: every topic already made. Never repeat one.

## Skills to use (in `.claude/skills/`)
| Stage | Skill |
|---|---|
| Topic check | `topic-validator` |
| Research questions | `research-prompts` (you answer them yourself with web search) |
| Fact check, Gate 1 and Gate 2 | `facts-checker` |
| Script + LINES.tsv | `video-scripter` |
| Visual plan and edit | `kamal-video-style` |
| Title, description, tags | `yt-seo` |
| Hook and loop for a Short | `yt-shorts` (its "Writing each one" rules) |

### What changes because this run is unattended
The skills were written for a person approving each step in chat. In this pipeline:
- Wherever a skill says "ask the user" or "wait for approval", **the gate becomes automatic**:
  topic-validator GO, facts-checker PASS or PASS_WITH_QUALIFICATIONS, and the scripter's
  quality rubric with no hard-stop. If a gate fails, drop that topic and pick the next one. Never
  push a weak topic through.
- The human check is the **email approval of the script** (Phase B), plus the upload mode in
  `config/settings.md` (default **private**, the owner makes it public).
- Format is always **Short**, 60 to 70 seconds, so never ask "Short ya Long?".
- Workspace is `videos/<YYYY-MM-DD>-<slug>/` in this repo (not `yt-agent/videos/`).
- Scripts the skills mention that do not exist here (`yt_topic_scan.py`, `footage-finder`, `flow-auto`,
  `kokoro_vo.py`, `hookscore.py`) are replaced by the tools in `scripts/` listed below.
- Google Flow is not available unattended. Use real archive or stock images first, then
  editor-built cards (numbers, dates, maps text). Never fake a real person or a real document.

## Fact rules (non-negotiable)
1. Every factual claim in the script needs **two independent credible sources**, at least one of
   them primary or a major established outlet. Record both URLs in `research/claim_ledger.csv`.
2. Only use pages you actually opened in this run. Never cite from memory. Never invent a URL,
   quote, number or date.
3. If a claim cannot be verified, cut it or attribute it ("reports ke mutabik..."). If the story
   depends on it, drop the topic.
4. Current Affairs: date-stamp the claim ("22 November tak"), present competing sides with
   attribution, and never take a political side.
5. No defamation: allegations about living people only with clear attribution to a named source.
6. Title and on-screen text are claims too. They go through Gate 2 as well.
7. Put the main sources in the video description under "Sources".

## The run, step by step
Every run starts with `git pull` and `bash scripts/setup.sh`.

**Phase A** does steps 1 to 5 and 5b for Short 1, then for Short 2, then commits and pushes.

### 1. Trend and competitor research
- `python scripts/yt_research.py --competitors config/competitors.txt --days 3 --out videos/_research/<date>`
  lists the competitors' newest uploads with views per hour, plus trending India videos.
- `python scripts/yt_research.py --own-uploads --out videos/_research/<date>` lists our own titles
  (to avoid repeats).
- Web search today's news and "on this day" history for the four categories.
- Shortlist 5 candidate topics: rising on competitor channels or in the news, not covered by us,
  fits the brand. Prefer topics where a competitor's Short is outperforming its channel average
  but our angle can add a real record or document.

### 2. Validate
Run `topic-validator` on the best candidate. Save `topic/TOPIC.md`. If NO-GO, take the next
candidate. Max 5 tries per Short; if all fail, make only the Shorts that passed and say so in the
run report.

### 3. Research
Use `research-prompts` to list the questions, then answer them yourself with web search and
fetched pages. Save `research/raw_research.md` with a URL beside every fact.

### 4. Fact check Gate 1
Run `facts-checker` Gate 1 on the research. Output in `research/`. BLOCK means drop the topic.

### 5. Script
Run `video-scripter` Stage A as a **Short**, 60 to 70 seconds:
- about **180 to 200 spoken words** (voice runs at 1.10x), about 20 to 25 lines, one sentence per line.
- Hook in the first line, one central question, one reveal, a payoff, and a last line that loops
  back to the first (from `yt-shorts`).
- Follow `style/MY_SCRIPT_STYLE.md`.
Then `facts-checker` Gate 2 on the script and the planned title. Then Stage B: write `LINES.tsv`
(Devanagari) and also `CAPTIONS.tsv` (columns `id`, `caption`: the same line in Roman Hinglish,
short, for on-screen captions). Also draft the title in `seo/SEO.md`.

### 5b. Email the script for approval (end of Phase A)
Write `videos/<dir>/EMAIL.md` in simple Hinglish:
- first line: `Reply "OK" to approve, or write the changes you want.`
- topic, category, why this topic today (trend/competitor proof, 1 to 2 lines)
- planned title
- the **full script** (Roman Hinglish), word count and estimated length
- fact check: status, every qualifier or flag, and the 3 to 6 main source links
Send it: `python scripts/mail.py send --subject "[RO-SCRIPT <dir>] <title>" --body-file videos/<dir>/EMAIL.md`
(If a Gmail connector is available in the run you may use it instead, same subject format.)
Add a row to `data/pending.csv`: `dir,title,sent_at,status=awaiting,reply_seen=`.
Commit and push, then end the run. Do **not** continue to step 6.

**Phase B** (check run):
1. `python scripts/mail.py replies --tag RO-SCRIPT --days 3` and match each reply to a row in
   `data/pending.csv` by the `<dir>` in the subject. Ignore replies already recorded in `reply_seen`.
2. Read the reply like a person would (Hinglish is fine):
   - approval ("ok", "approved", "sahi hai", "done", "chalega", 👍): set `status=approved`.
   - changes: apply them to SCRIPT.md in the owner's style, re-run facts-checker Gate 2 on the
     changed lines, email the new version with subject `[RO-SCRIPT <dir>] v2 <title>`, keep `status=awaiting`.
     If a change would make a claim false or unverified, do not apply it; explain why in the email.
   - "skip", "cancel", "chhodo": set `status=dropped`.
   Record the reply's message id in `reply_seen`. Add lasting feedback to `style/LEARNINGS.md`.
3. For every `approved` row not yet `uploaded`: regenerate LINES.tsv/CAPTIONS.tsv if the script
   changed, then do steps 6 to 10, then set `status=uploaded` and the video id.
4. If a row has waited more than 36 hours with no reply, send one short reminder email; after
   72 hours set `status=expired` (Current Affairs scripts go stale).
5. If nothing is pending, end quickly with no changes.

### 6. Voiceover
`python scripts/voiceover.py videos/<dir>` makes one audio file per line with ElevenLabs and
writes `audio/timings.tsv`. Check the total duration it prints:
- under 58 s: first raise the `gap` values in LINES.tsv (free); only if still short, add one verified line.
- over 72 s: first lower gaps, then delete the weakest line from LINES.tsv (free, no new audio).
Re-running only re-voices lines whose text changed, so never use `--force` unless the voice itself is wrong.

## Saving credits and money (owner's rule)
- ElevenLabs credits are paid. Voice is made **only after the owner approves the script**, once per line,
  and is cached (`audio/manifest.json`). Never regenerate unchanged lines. A video over
  ELEVENLABS_MAX_CHARS (2500 characters) stops instead of spending more.
- Everything else uses free resources: Wikimedia Commons and Openverse images (Pexels if keyed), text cards made by the
  assembler, free YouTube Data API, Gmail. No paid image or video generation (Flow, Veo, Imagen)
  unless the owner adds a key and asks for it.

### 7. Visuals
Follow `kamal-video-style` and `style/EDIT_STYLE.md`. For each line, decide one shot and write
`SHOTS.tsv` with columns `id`, `type`, `source`, `motion`, `overlay`:
- `type=image`: `source` is a file path under `videos/<dir>/assets/`.
  Find images with `python scripts/fetch_visuals.py "<query>" --out videos/<dir>/assets --n 5`
  (Wikimedia Commons first for history and documents, Openverse for general scenes; Pexels only if its key is set). It writes
  `assets/CREDITS.md`; check licences and add credits to the description where required.
- `type=card`: `source` is the card text (big number, date or short phrase in English or Roman
  Hinglish), rendered by the assembler.
- `motion`: `zoomin`, `zoomout`, `panleft`, `panright` or `none`.
- `overlay`: optional short headline text on top (or empty).
Look at every image you pick (open it) to check it shows what the line says. A wrong picture is a
factual error.

### 8. Assemble
`python scripts/assemble_short.py videos/<dir>` builds `final/short.mp4` with voice, captions,
motion and optional music from `assets/music/` (royalty-free only). Then check it:
- `ffprobe` duration 58 to 72 s, 1080x1920.
- extract 4 frames (`ffmpeg -ss <t> -i final/short.mp4 -frames:v 1 frame.png`) and look at them:
  captions readable, nothing cut off, no wrong picture.

### 9. Package and upload
- `yt-seo`: title (under 70 characters, Hinglish, no clickbait the facts cannot back), the first two
  description lines, Sources list, 10 to 15 tags. Save `seo/SEO.md`. Include `#Shorts`.
- Upload: `python scripts/youtube_upload.py --file final/short.mp4 --meta seo/upload.json`
  where `upload.json` has `title`, `description`, `tags`, `privacy`, `publish_at` (from settings).
  Set `synthetic: true` only if a realistic AI image of a real event or person was used.
- Append a row to `data/topics_log.csv`: date, slug, category, title, video id, status.
- Email the owner a one-line note with the YouTube link (`[RO-DONE <dir>]` subject).

### 10. Run report
At the end write `videos/<date>-RUN_REPORT.md` (append if it exists): for each Short the title, YouTube link, gate
results, any qualifiers, sources count, and anything the owner should check. Commit everything
(except big media files, which are git-ignored) and push.

## If something breaks
- A tool or API fails: retry twice, then skip that step only if the video is still honest
  (for example no music is fine, no voice is not). Otherwise stop that Short and report why.
- Never mark a video as done if it was not uploaded. Never claim a fact was checked if it was not.

## Learning loop
When the owner gives feedback (in a session or in `style/LEARNINGS.md`), add it to
`style/LEARNINGS.md` as `RULE:` (confirmed) or `HYPOTHESIS:` (to test). Never delete their lines.
