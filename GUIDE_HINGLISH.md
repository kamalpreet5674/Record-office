# Poora Setup Guide (step by step, har click ke saath)

Is guide mein total **9 cheezein (keys)** banani hain aur unhe **ek hi jagah** paste karna hai:
**claude.ai/code → Environment settings → Environment variables**.
Kahin bhi chat mein key paste mat karna.

## Pehle ye table dekh lo: kaunsi key, kahan se, kahan daalni hai

| # | Naam (exactly yahi likhna) | Kahan se milegi | Kahan paste karni hai |
|---|---|---|---|
| 1 | `YT_CLIENT_ID` | Google Cloud → JSON file ke andar `client_id` | Claude Code environment variables |
| 2 | `YT_CLIENT_SECRET` | Google Cloud → JSON file ke andar `client_secret` | Claude Code environment variables |
| 3 | `YT_REFRESH_TOKEN` | Laptop par ek script chalane se (Step 3) | Claude Code environment variables |
| 4 | `GMAIL_ADDRESS` | Aapka Gmail jisse email jayega | Claude Code environment variables |
| 5 | `GMAIL_APP_PASSWORD` | Google Account → App passwords (Step 4) | Claude Code environment variables |
| 6 | `OWNER_EMAIL` | Aapka email jisse aap "OK" reply karoge | Claude Code environment variables |
| 7 | `ELEVENLABS_API_KEY` | ElevenLabs → API Keys (Step 5) | Claude Code environment variables |
| 8 | `ELEVENLABS_VOICE_ID` | ElevenLabs → Voices → aapki voice (Step 5) | Claude Code environment variables |
| 9 | `PEXELS_API_KEY` (optional, skip kar sakte ho) | pexels.com/api (Step 6) | Claude Code environment variables |

Tip: ek Notepad file kholo, upar wale 9 naam likh lo, aur har step ke baad value bharte jao.
Last mein (Step 7) poora ek saath paste karna hai. Kaam khatam hone ke baad Notepad file delete kar dena.

---

## Step 1: Google Cloud project + YouTube API (5 min)
1. Kholo: https://console.cloud.google.com (apne channel wale Gmail se login).
2. Upar left mein project dropdown (Google Cloud logo ke paas) → **New Project**.
3. Project name: `records-office` → **Create**. 10 second ruko, phir upar dropdown se yahi project select karo.
4. Left menu (☰) → **APIs & Services** → **Library**.
5. Search box mein likho: `YouTube Data API v3` → us par click → **Enable**. ✅ (Ye aap kar chuke ho)

Billing / free trial maange toh ignore karo, iski zarurat nahi hai.

## Step 2: OAuth consent screen + Credentials (10 min)
Ye isliye kyunki YouTube par upload ke liye "API key" kaam nahi karti; **OAuth client** chahiye.

### 2A. Consent screen
1. Left menu → **APIs & Services** → **OAuth consent screen** → **Get started**.
2. **App information:** App name `Records Office Uploader`, User support email = aapka Gmail → **Next**.
3. **Audience:** **External** select → **Next**.
4. **Contact information:** aapka Gmail → **Next**.
5. **Finish:** "I agree..." tick → **Continue** → **Create**.
6. Left side **Audience** par click:
   - **Test users** → **+ Add users** → channel wala Gmail likho → **Save**.
   - Upar **Publishing status** mein **Publish app** → **Confirm**. Ab "In production" dikhna chahiye.
   (Ye zaroori hai, warna 7 din baad login expire ho jayega.)

### 2B. Credentials (OAuth client ID)
1. Left menu → **APIs & Services** → **Credentials**.
2. Upar **+ Create credentials** → **OAuth client ID** (API key NAHI).
3. **Application type:** `Desktop app`. **Name:** `records-office-desktop` → **Create**.
4. Popup aayega → **Download JSON** → file laptop par save karo (Downloads mein `client_secret_....json`).
5. Is popup mein **Client ID** aur **Client secret** bhi dikhenge:
   - Client ID copy karo → Notepad mein `YT_CLIENT_ID=` ke aage paste.
   - Client secret copy karo → Notepad mein `YT_CLIENT_SECRET=` ke aage paste.
   (Popup band ho gaya? Credentials page → OAuth 2.0 Client IDs → aapke client ke naam par click → wahan bhi dikhenge.)

## Step 3: YouTube login, sirf ek baar (laptop par, 10 min)
Isse `YT_REFRESH_TOKEN` milega.
1. Python install karo: https://www.python.org/downloads → Download → install karte waqt
   **"Add Python to PATH"** tick zaroor karna.
2. GitHub par apna repo kholo: https://github.com/kamalpreet5674/Record-office →
   `scripts` folder → `get_youtube_token.py` → upar right **Download raw file** (⬇ icon).
   Is file ko aur Step 2B wali JSON file ko **ek hi folder** mein rakho (jaise Downloads).
3. Terminal kholo:
   - Windows: Start → `cmd` likho → Command Prompt.
   - Mac: Spotlight → `Terminal`.
4. Us folder mein jao: `cd Downloads`
5. Ye do command chalao (JSON file ka exact naam daalna):
   ```
   pip install google-auth-oauthlib
   python get_youtube_token.py client_secret_XXXX.json
   ```
   (Mac par `pip3` aur `python3` likhna.)
6. Browser khulega:
   - **The Records Office** wala Google account / channel choose karo.
   - "Google hasn't verified this app" → **Advanced** → **Go to Records Office Uploader (unsafe)**. Ye aapka apna app hai, safe hai.
   - **Continue / Allow**.
7. Browser mein "authentication flow has completed" dikhega. Terminal mein ek line aayegi:
   `YT_REFRESH_TOKEN = 1//0g....` → poori value copy karke Notepad mein `YT_REFRESH_TOKEN=` ke aage paste.

## Step 4: Gmail App Password (5 min)
Isse Claude aapko script email karega aur aapka reply padhega.
1. Kholo: https://myaccount.google.com → left **Security**.
2. **2-Step Verification** ON hona chahiye (nahi hai toh ON karo, phone se verify).
3. Upar search bar mein likho `App passwords` → open.
4. App name: `records-office` → **Create**.
5. 16 letters ka password dikhega (jaise `abcd efgh ijkl mnop`). Bina space ke copy karo →
   Notepad mein `GMAIL_APP_PASSWORD=` ke aage.
6. Notepad mein:
   - `GMAIL_ADDRESS=` ke aage wahi Gmail jiska app password banaya.
   - `OWNER_EMAIL=` ke aage wo email jisse aap reply karoge (same Gmail bhi chalega).

## Step 5: ElevenLabs (3 min)
1. Kholo: https://elevenlabs.io → login.
2. https://elevenlabs.io/app/settings/api-keys → **Create API key** → naam `records-office`.
   Credits bachane ke liye **Restrict key** ON karo aur sirf ye access do:
   - **Text to Speech:** Access
   - **Voices:** Read
   - **User:** Read
   - baaki sab: No access
   **Credit limit** (agar option ho): 30,000 per month (2 Shorts roz ke liye kaafi).
   Create → key copy (`sk_...`) → Notepad mein `ELEVENLABS_API_KEY=`.
3. Voice ID ready hai (aapki "Kamal" professional voice): `ELEVENLABS_VOICE_ID=qrQDmG9I6ONIs4PYfwRs`

## Step 6: Pexels (OPTIONAL, skip kar sakte ho)
Pexels abhi naye keys nahi de raha. Koi baat nahi: images Wikimedia Commons aur Openverse se aayengi (dono free, bina key).
Baad mein key mile toh `PEXELS_API_KEY` add kar dena.

1. Kholo: https://www.pexels.com/api → **Get started** / Your API key (free account bana lo).
2. Form bharo (description: "YouTube documentary shorts images") → key copy →
   Notepad mein `PEXELS_API_KEY=`.

Ab aapka Notepad aisa dikhna chahiye (apni values ke saath):
```
YT_CLIENT_ID=123456-abc.apps.googleusercontent.com
YT_CLIENT_SECRET=GOCSPX-xxxx
YT_REFRESH_TOKEN=1//0gxxxx
GMAIL_ADDRESS=aapka@gmail.com
GMAIL_APP_PASSWORD=abcdefghijklmnop
OWNER_EMAIL=aapka@gmail.com
ELEVENLABS_API_KEY=sk_xxxx
ELEVENLABS_VOICE_ID=qrQDmG9I6ONIs4PYfwRs
PEXELS_API_KEY=xxxx
```

## Step 7: Claude Code mein sab paste karo (5 min)
1. Kholo: https://claude.ai/code
2. Neeche/upar repo selector se **kamalpreet5674/Record-office** choose karo.
3. Uske paas **environment** (cloud icon / "Default" naam) par click → **⚙ gear / Edit**
   (ya **+ New environment**, naam `records-office`).
4. **Network access:** `Full`.
5. **Environment variables** box mein Step 6 wala poora Notepad text paste karo.
6. **Setup script** box mein ye paste karo:
   ```
   apt-get update && apt-get install -y ffmpeg fonts-dejavu fonts-noto-core || true
   pip install google-api-python-client google-auth google-auth-oauthlib requests Pillow playwright gdown
   python -m playwright install --with-deps chromium || true
   ```
7. **Save**.

## Step 8: Competitors add karo (3 min)
1. GitHub repo → `config/competitors.txt` → ✏️ pencil (Edit).
2. Har line mein ek competitor channel, jaise:
   ```
   @channelname1
   @channelname2
   ```
3. **Commit changes**.

## Step 9: Pehla test (Claude Code mein)
1. claude.ai/code → repo **Record-office** + environment **records-office** → naya session.
2. Ye paste karo:
   ```
   Test run. Follow CLAUDE.md Phase A but make only Short 1, and email it to me.
   Show me each stage here too (topic, sources, script). Stop after the email.
   ```
3. Email aayega → reply mein `OK` likho (ya changes).
4. Naye session mein ye paste karo:
   ```
   Test run. Follow CLAUDE.md Phase B: check my reply and, if approved, make the video and
   upload it as private. Show me the frames and the link.
   ```
5. YouTube Studio → Content → private Short dekho.

## Step 10: Daily automatic chalu karo
claude.ai/code → **Routines** → **New routine** (ya session mein `/schedule` likho). Do routines banao,
dono mein repo **Record-office** aur environment **records-office**:

| Routine | Time | Prompt (ROUTINE_PROMPT.md se copy) |
|---|---|---|
| A: morning scripts | Roz 6:00 AM | "Routine A" wala text |
| B: check replies + video | Har 2 ghante, 8 AM se 10 PM | "Routine B" wala text |

- Time zone apna (Dubai) check kar lena.
- Agar "push to branch" ki permission pooche → **main par push allow** karo.

---

## Kuch galat ho toh
| Problem | Kya karo |
|---|---|
| "Missing secret XYZ" | Step 7 mein woh naam galat likha ya value missing hai |
| YouTube "invalid_grant" error | Step 3 dobara karo, naya `YT_REFRESH_TOKEN` daalo |
| Email nahi aaya | Step 4 ka app password check karo, spam folder dekho |
| `python` not found (Windows) | Python dobara install karo "Add to PATH" tick karke |
| Upload private hi ho raha hai | Normal hai. Google audit ke baad public/scheduled ho payega |

Kisi bhi step par atak jao toh bas step number batao.
