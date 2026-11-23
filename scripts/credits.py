"""ElevenLabs credit check (free call, spends nothing). Warns the owner once when credits run low.

  python scripts/credits.py [--warn-below 15000]

Prints characters left. If fewer than --warn-below are left (default about 2 weeks of Shorts at
~1,100 characters each), sends one phone notification and prints WARN, so Claude also emails the
owner. It warns at most once per day (state in data/credit_warning.txt).
"""
import argparse
import datetime as dt
import os
import sys

import requests

sys.path.insert(0, os.path.dirname(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--warn-below", type=int, default=15000)
    a = ap.parse_args()
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("Missing ELEVENLABS_API_KEY")
    s = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": key}, timeout=30).json()
    left = s.get("character_limit", 0) - s.get("character_count", 0)
    reset = s.get("next_character_count_reset_unix")
    reset_txt = dt.datetime.fromtimestamp(reset).strftime("%d %b") if reset else "?"
    shorts = left // 1100
    print(f"{left} characters left (about {shorts} Shorts), resets {reset_txt}, plan {s.get('tier', '?')}")
    if left >= a.warn_below:
        return
    state, today = "data/credit_warning.txt", dt.date.today().isoformat()
    if os.path.exists(state) and open(state).read().strip() == today:
        print("WARN already sent today")
        return
    import mail
    mail.notify("ElevenLabs credits kam hain",
                f"Sirf {left} characters bache hain (lagbhag {shorts} Shorts), reset {reset_txt}. Plan upgrade kar do.",
                "https://elevenlabs.io/app/subscription")
    open(state, "w").write(today)
    print(f"WARN: low credits, notification sent. Email the owner too (subject [RO-CREDITS {today}]).")


if __name__ == "__main__":
    main()
