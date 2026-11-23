"""One-time setup check: are all keys working? Spends no ElevenLabs credits.

  python scripts/check_setup.py

Checks the secrets exist, logs in to YouTube (and the Analytics API), reads the ElevenLabs
account (free call), logs in to Gmail and sends one test email + phone notification.
Prints OK / FAIL per item. Never prints a secret value.
"""
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
results = []


def check(name, fn):
    try:
        msg = fn()
        results.append((name, True, msg or ""))
    except SystemExit as e:
        results.append((name, False, str(e)))
    except Exception as e:
        results.append((name, False, f"{type(e).__name__}: {str(e)[:200]}"))


def secrets():
    need = ["YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN", "GMAIL_ADDRESS", "GMAIL_APP_PASSWORD",
            "OWNER_EMAIL", "ELEVENLABS_API_KEY", "ELEVENLABS_VOICE_ID"]
    missing = [k for k in need if not os.environ.get(k)]
    if missing:
        raise RuntimeError("missing: " + ", ".join(missing))
    opt = [k for k in ("NTFY_TOPIC", "DRIVE_ASSETS_URL", "PEXELS_API_KEY") if not os.environ.get(k)]
    return "all 8 required set" + (f"; optional not set: {', '.join(opt)}" if opt else "")


def yt():
    from yt_common import youtube
    ch = youtube().channels().list(part="snippet,statistics", mine=True).execute()["items"][0]
    return f"channel '{ch['snippet']['title']}', {ch['statistics'].get('subscriberCount')} subs"


def yta():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    creds = Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"], client_id=os.environ["YT_CLIENT_ID"],
                        client_secret=os.environ["YT_CLIENT_SECRET"], token_uri="https://oauth2.googleapis.com/token")
    end = dt.date.today()
    r = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False).reports().query(
        ids="channel==MINE", startDate=(end - dt.timedelta(days=28)).isoformat(), endDate=end.isoformat(),
        metrics="views,averageViewPercentage").execute()
    row = (r.get("rows") or [[0, 0]])[0]
    return f"last 28 days: {row[0]} views, {row[1]}% avg viewed"


def eleven():
    import requests
    h = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}
    r = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers=h, timeout=30)
    r.raise_for_status()
    s = r.json()
    left = s.get("character_limit", 0) - s.get("character_count", 0)
    v = requests.get(f"https://api.elevenlabs.io/v1/voices/{os.environ['ELEVENLABS_VOICE_ID']}", headers=h, timeout=30)
    voice = v.json().get("name", "?") if v.ok else f"voice check HTTP {v.status_code} (key may lack Voices: Read)"
    return f"{left} characters left this month; voice: {voice}"


def gmail():
    import imaplib
    im = imaplib.IMAP4_SSL("imap.gmail.com")
    im.login(os.environ["GMAIL_ADDRESS"], os.environ["GMAIL_APP_PASSWORD"])
    im.logout()
    return "IMAP login OK (can read replies)"


def mail_test():
    import mail
    lines = "\n".join(f"{'OK  ' if ok else 'FAIL'} {n}: {m}" for n, ok, m in results)
    mail.send("[RO-TEST] Records Office setup check",
              "Setup check from Claude Code. If you got this email, sending works.\n\n" + lines +
              "\n\nNo reply needed.")
    return "test email + phone notification sent"


check("secrets", secrets)
check("YouTube Data API", yt)
check("YouTube Analytics API", yta)
check("ElevenLabs (no credits used)", eleven)
check("Gmail read", gmail)
check("Gmail send + ntfy", mail_test)
for n, ok, m in results:
    print(f"{'OK  ' if ok else 'FAIL'} {n}: {m}")
sys.exit(0 if all(ok for _, ok, _ in results) else 1)
