# Setup guide: The Records Office daily Shorts (Claude Code)

## How it works every day
1. **6:00 AM:** Claude researches trends and competitors, picks 2 new topics, fact-checks them,
   writes 2 scripts in your style and **emails them to you**.
2. **You reply to each email:** "OK" (or "sahi hai") to approve, or write the changes you want.
3. **Every 2 hours (8 AM to 10 PM):** Claude checks your replies.
   - Approved: it makes the voiceover, the video and the upload, then emails you the YouTube link.
   - Changes: it fixes the script, checks the facts again and emails you the new version.
4. You open YouTube Studio and make the video public. Until Google approves your app it stays private.

Total setup time: about 1 hour, one time only. The kit is already in your repo
**kamalpreet5674/Record-office**, with your style filled in.

---

## Part 1: Keys you need (collect these first)

### 1A. YouTube upload (Google Cloud), about 15 min
1. Open https://console.cloud.google.com → top bar → **New project** → name `records-office` → Create.
2. Left menu **APIs & Services → Library** → search **YouTube Data API v3** → **Enable**.
3. **APIs & Services → OAuth consent screen** (Google Auth Platform) → Get started:
   - App name `Records Office Uploader`, your email, Audience **External**, then create.
   - **Audience** → Test users → add your channel's Google account.
   - Click **Publish app** so it is "In production". If you skip this, the login stops working
     after 7 days.
4. **APIs & Services → Credentials → Create credentials → OAuth client ID** → type **Desktop app** →
   Create → **Download JSON**. Keep this file private.

### 1B. One-time YouTube login (on your laptop)
1. Install Python from python.org if you don't have it.
2. Download `scripts/get_youtube_token.py` from your repo.
3. Open a terminal in that folder and run:
   ```
   pip install google-auth-oauthlib
   python get_youtube_token.py "C:\path\to\client_secret_xxx.json"
   ```
4. The browser opens. Pick **The Records Office** channel account. On the "unverified app"
   warning click **Advanced → Go to app**, then allow.
5. The terminal shows `YT_REFRESH_TOKEN = ...`. Copy it somewhere safe for Part 2.
   `YT_CLIENT_ID` and `YT_CLIENT_SECRET` are inside the JSON file.

### 1C. Gmail, for script emails (5 min)
1. Open https://myaccount.google.com → **Security** → turn on **2-Step Verification**.
2. Search "App passwords" at the top → create one named `records-office` → copy the 16-letter password.
3. You can send from the same Gmail you reply from. That's fine.

### 1D. ElevenLabs and Pexels
- ElevenLabs: **done.** It works through the ElevenLabs connector, with your voice "Kamal"
  (`qrQDmG9I6ONIs4PYfwRs`, already set in the repo). No API key needed. Just add the
  **ElevenLabs connector** to both routines in Part 5.
- Pexels (free): https://www.pexels.com/api → get your API key.

---

## Part 2: Claude Code cloud environment (in the browser)
1. Open https://claude.ai/code and sign in.
2. Select the repo **kamalpreet5674/Record-office**. If it's not in the list, connect GitHub
   and allow access to this repo.
3. Open the **environment** menu (cloud icon near the repo name) → **gear / Edit environment**
   (or create a new one named `records-office`).
4. **Network access:** choose **Full**, because research needs many news sites.
5. **Environment variables:** add these lines, one per line, with your real values.
   Type them only in this settings box. Never paste them in a chat.
   ```
   YT_CLIENT_ID=...
   YT_CLIENT_SECRET=...
   YT_REFRESH_TOKEN=...
   PEXELS_API_KEY=...
   GMAIL_ADDRESS=your-gmail@gmail.com
   GMAIL_APP_PASSWORD=the16letterpassword
   OWNER_EMAIL=the-email-you-reply-from@gmail.com
   ```
6. **Setup script:** paste:
   ```
   apt-get update && apt-get install -y ffmpeg fonts-dejavu fonts-noto-core || true
   pip install google-api-python-client google-auth google-auth-oauthlib requests Pillow
   ```
7. Save.

---

## Part 3: Fill 1 file in the repo
Open `config/competitors.txt` on GitHub (pencil icon) and add 5 to 15 competitor channels,
one per line, like `@channelhandle`. Commit.
(Your script style is already filled in `style/MY_SCRIPT_STYLE.md`. Edit it anytime.)

---

## Part 4: First test (by hand)
1. At claude.ai/code, start a new session on the repo with the `records-office` environment.
2. Paste the first **Manual test prompt** from `ROUTINE_PROMPT.md`.
3. Check your email for the script and reply "OK", or with changes.
4. In a session, paste the second test prompt. It makes the video and uploads it as **private**.
5. Watch it in YouTube Studio. If anything feels off, tell Claude. It saves your feedback as a rule
   in `style/LEARNINGS.md`.

---

## Part 5: Turn on the daily routines
At claude.ai/code open **Routines** (scheduled tasks) → **New routine**, or type `/schedule` in a session.
Create two routines, both with the Record-office repo and the `records-office` environment:

| Routine | When | Prompt |
|---|---|---|
| A: morning scripts | Every day 6:00 AM | "Routine A" from `ROUTINE_PROMPT.md` |
| B: check replies + make videos | Every 2 hours, 8 AM to 10 PM | "Routine B" from `ROUTINE_PROMPT.md` |

- Check the time zone in the routine settings: your local time (Dubai, or India if you prefer).
- If the routine asks about branch pushes, **allow pushing to main**. It saves `data/pending.csv`
  there, which is how routine B knows which scripts you approved.
- **Add the ElevenLabs connector to both routines** (routine settings → Connectors). Without it the
  voiceover cannot be made. Routine B needs it most, because it makes the voice.
- If you add the Gmail connector to the routines, Claude may use it. The script email works without it.

---

## Your daily routine (5 minutes)
- Morning: read 2 emails and reply "OK" or with changes.
- Evening: open YouTube Studio, watch the 2 private Shorts, make them public.

## Later
- **Fully automatic publishing:** apply for Google's **YouTube API audit** (Google Cloud → YouTube
  Data API → Quotas → audit form). After approval set `Publish mode: scheduled` in `config/settings.md`.
- **vidIQ back:** Claude can add keyword data to topic checks.

## Rough costs
- Claude: runs on your Claude plan. A Max plan is comfortable for daily runs.
- ElevenLabs: about 60k characters a month.
- YouTube API, Gmail, Pexels, Wikimedia: free.

## If something goes wrong
- No email at 6 AM: open the routine's last run at claude.ai/code and read what it says.
- "Missing secret ...": that value is missing in Part 2, step 5.
- YouTube login error: run Part 1B again and update `YT_REFRESH_TOKEN`.
