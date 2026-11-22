# Setup: The Records Office daily Shorts on Claude Code

What you get: every morning two Claude Code routines run in the cloud. Each one finds a fresh
trending topic (competitors + news), checks it, researches and fact-checks it with two sources per
claim, writes a 60 to 70 second Short in your style, makes your ElevenLabs voiceover, builds the
vertical video with captions, and uploads it to YouTube. You check it and make it public.

Time needed: about 1 hour, one time.

---

## What is in this kit
| File | What it is |
|---|---|
| `CLAUDE.md` | The rulebook. Claude reads it on every run. This is the "memory" of the pipeline. |
| `.claude/skills/` | Your skills: topic-validator, research-prompts, facts-checker, video-scripter, kamal-video-style, yt-seo, yt-shorts |
| `style/MY_SCRIPT_STYLE.md` | **You fill this:** your script style + example scripts |
| `style/EDIT_STYLE.md` | Look of the Shorts (colours, captions, motion) |
| `style/LEARNINGS.md` | Your feedback; Claude follows every `RULE:` line |
| `config/settings.md` | Publish mode, time zone, niches |
| `config/competitors.txt` | **You fill this:** competitor channels |
| `scripts/` | Tools: trend research, voiceover, images, video assembly, YouTube upload |
| `ROUTINE_PROMPT.md` | The prompts for the two daily routines |
| `data/topics_log.csv` | Every topic made, so nothing repeats |

---

## Step 1: Put the kit on GitHub
1. On github.com create a **private** repo, e.g. `records-office-shorts` (empty, no README).
2. Upload everything in this kit folder to it (including the `.claude` folder).
   Easier: tell Claude the repo name in the project chat and it can push the kit for you.

## Step 2: Add your style and competitors
1. Open `style/MY_SCRIPT_STYLE.md` and paste your script style notes and 3 to 5 of your best
   Short scripts (the ones from your other account).
2. Open `config/competitors.txt` and add 5 to 15 competitor channels, one per line (`@handle`).
3. Your skills were copied with their main file only. If your other account has extra files for
   them (for example `kamal-video-style/references/visual-style.md`,
   `video-scripter/references/quality-rubric.md`, `facts-checker/references/verdict-policy.md`),
   upload those into the same folders under `.claude/skills/`.

## Step 3: Google Cloud, for YouTube upload (about 15 minutes)
1. Go to https://console.cloud.google.com and create a project, e.g. `records-office`.
2. **APIs & Services → Library** → search **YouTube Data API v3** → **Enable**.
3. **APIs & Services → OAuth consent screen** (Google Auth Platform):
   - User type **External**, app name `Records Office Uploader`, your email as support and developer contact.
   - Scopes: you can skip, the script asks for them.
   - Audience: add your channel's Google account as a **test user**.
   - Then click **Publish app** (set it "In production"). Important: in "Testing" mode the login
     expires every 7 days and the daily upload would stop. In production it keeps working; Google
     shows an "unverified app" warning on your one-time login, which is fine because it is your own app.
4. **APIs & Services → Credentials → Create credentials → OAuth client ID** → type **Desktop app**.
   Download the JSON file (`client_secret_....json`). Keep it private, never upload it to GitHub.

## Step 4: One-time YouTube login (on your own computer)
1. Install Python from python.org if you do not have it.
2. In a terminal, in the kit's `scripts` folder:
   ```
   pip install google-auth-oauthlib
   python get_youtube_token.py path/to/client_secret_....json
   ```
3. A browser opens. Choose the Google account of **The Records Office** channel (if it asks for a
   channel/brand account, pick the channel). Click through the "unverified app" warning (Advanced →
   Go to app) and allow.
4. The terminal prints `YT_REFRESH_TOKEN`. Keep it for step 5. Client ID and secret are inside the JSON file.

## Step 5: Other keys
- **ElevenLabs:** elevenlabs.io → profile → API keys → create one. Voice ID: Voices → your cloned
  voice → copy ID. (A Short is about 1,000 characters, so 2 a day is about 60,000 a month.)
- **Pexels (free):** https://www.pexels.com/api → get key.

## Step 6: Claude Code cloud environment
1. Open https://claude.ai/code, select your repo, and open the **environment settings**
   (cloud environment → gear icon).
2. **Network access:** Full (or allow at least: `api.elevenlabs.io`, `api.pexels.com`,
   `commons.wikimedia.org`, `upload.wikimedia.org`, `*.googleapis.com`, `oauth2.googleapis.com`,
   plus news sites for research; Full is simplest since research needs many sites).
3. **Environment variables / secrets** (type the values yourself, never paste them in a chat):
   ```
   YT_CLIENT_ID=...
   YT_CLIENT_SECRET=...
   YT_REFRESH_TOKEN=...
   ELEVENLABS_API_KEY=...
   ELEVENLABS_VOICE_ID=...
   PEXELS_API_KEY=...
   ```
4. **Setup script:**
   ```
   apt-get update && apt-get install -y ffmpeg fonts-dejavu fonts-noto-core || true
   pip install google-api-python-client google-auth google-auth-oauthlib requests Pillow
   ```

## Step 7: Test once by hand
Start a normal Claude Code session on the repo (claude.ai/code) and paste the **Manual test
prompt** from `ROUTINE_PROMPT.md`. It stops after each stage so you can check the topic, sources,
script, voice and video. Fix your style files until you like the result. Add feedback to
`style/LEARNINGS.md`.

## Step 8: Turn on the daily routines
In Claude Code on the web, open **Routines** (scheduled tasks), or type `/schedule` in a Claude
Code session, and create two routines on this repo and environment:
- **Slot 1**, every day **6:00 AM** (your time zone), prompt "Routine 1" from `ROUTINE_PROMPT.md`.
- **Slot 2**, every day **6:20 AM**, prompt "Routine 2".
Two separate runs are safer than one long run: if one fails, the other still posts.
Allow the routine to push to the repo so it can save the topic log.

## Step 9: Your daily 5 minutes
1. Open YouTube Studio → Content. Two new private Shorts are there.
2. Read the run report in the repo (`videos/<date>-slot1-RUN_REPORT.md`) for sources and flags.
3. Watch, then set **Public** (or schedule). If something is off, write a `RULE:` line in
   `style/LEARNINGS.md` so it is fixed tomorrow.

## Step 10: Later, go fully automatic
- YouTube keeps uploads from unaudited API apps **private**. To let the pipeline publish or schedule
  by itself, apply for the **YouTube API Services audit** (Google Cloud → YouTube Data API → quotas
  page → audit form). After approval, set `Publish mode: scheduled` in `config/settings.md`.
- When vidIQ is back, Claude can add its keyword data to topic validation.

---

## Costs (rough)
- Claude Code: runs on your Claude plan; two research-heavy runs a day need a Max plan to be comfortable.
- ElevenLabs: about 60k characters a month (Creator plan covers it).
- YouTube API, Pexels, Wikimedia: free (YouTube gives 10,000 units a day; one upload is about 1,600).

## Safety rules built in
- No fact without two sources opened in that run; failed topics are dropped, not forced.
- Sources go in the description. No fake documents, no AI faces of real people.
- Nothing is public until you (or, after the audit, your chosen schedule) say so.
