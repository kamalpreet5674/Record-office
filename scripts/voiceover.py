"""ElevenLabs voiceover, one file per LINES.tsv row.

  python scripts/voiceover.py videos/<dir> [--force]

Needs secrets ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID (your cloned voice).
Writes videos/<dir>/audio/<id>.mp3 and audio/timings.tsv (id, start, duration, gap).
"""
import csv
import os
import subprocess
import sys
import time

import requests

MODEL = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
SPEED = float(os.environ.get("ELEVENLABS_SPEED", 1.1))  # owner prefers 1.10x


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def tts(text, path):
    key, voice = os.environ.get("ELEVENLABS_API_KEY"), os.environ.get("ELEVENLABS_VOICE_ID")
    if not key or not voice:
        sys.exit("Missing ELEVENLABS_API_KEY or ELEVENLABS_VOICE_ID secret. See SETUP.md step 4.")
    for attempt in range(3):
        r = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
            headers={"xi-api-key": key, "Content-Type": "application/json"},
            json={"text": text, "model_id": MODEL,
                  "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.2, "speed": SPEED}},
            timeout=120)
        if r.ok:
            open(path, "wb").write(r.content)
            return
        print(f"ElevenLabs error {r.status_code}: {r.text[:200]}")
        time.sleep(5 * (attempt + 1))
    sys.exit("Voiceover failed after 3 tries.")


def main():
    d = sys.argv[1]
    force = "--force" in sys.argv
    os.makedirs(f"{d}/audio", exist_ok=True)
    rows = list(csv.DictReader(open(f"{d}/LINES.tsv", encoding="utf-8"), delimiter="\t"))
    t, out = 0.0, []
    for row in rows:
        p = f"{d}/audio/{row['id']}.mp3"
        if force or not os.path.exists(p):
            tts(row["text"], p)
        dur, gap = duration(p), float(row.get("gap") or 0.35)
        out.append((row["id"], t, dur, gap))
        t += dur + gap
    with open(f"{d}/audio/timings.tsv", "w") as f:
        f.write("id\tstart\tduration\tgap\n")
        for i, s, du, g in out:
            f.write(f"{i}\t{s:.3f}\t{du:.3f}\t{g:.2f}\n")
    print(f"{len(rows)} lines, total {t:.1f} s (target 60-70 s)")


if __name__ == "__main__":
    main()
