"""Voiceover in the owner's ElevenLabs voice ("Kamal"), one file per LINES.tsv row.

Two ways, same result (audio/<id>.mp3 at 1.10x + audio/timings.tsv):

1. ElevenLabs CONNECTOR (default, no API key needed):
   For each LINES.tsv row, Claude calls the connector tool `creative_generate_speech` with
   voice_id qrQDmG9I6ONIs4PYfwRs, model_id eleven_multilingual_v2, generations_count 1, then
   polls `creative_get_flow_run_status` and writes the row id and the returned content_url to
   videos/<dir>/audio/urls.tsv (columns: id, url). Then:

     python scripts/voiceover.py videos/<dir> --from-urls

   which downloads every clip, speeds it to 1.10x with ffmpeg and writes timings.tsv.

2. API key (fallback, only if secret ELEVENLABS_API_KEY is set):

     python scripts/voiceover.py videos/<dir> [--force]

Writes videos/<dir>/audio/<id>.mp3 and audio/timings.tsv (id, start, duration, gap).
"""
import csv
import os
import subprocess
import sys
import time

import requests

VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "qrQDmG9I6ONIs4PYfwRs")  # owner's voice "Kamal"
MODEL = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
SPEED = float(os.environ.get("ELEVENLABS_SPEED", 1.1))  # owner prefers 1.10x


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def speed_up(src, dst):
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter:a", f"atempo={SPEED}",
                        "-ar", "44100", "-b:a", "128k", dst], capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg speed-up failed: " + r.stderr[-500:])


def download(url, path):
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=120)
            if r.ok and len(r.content) > 1000:
                open(path, "wb").write(r.content)
                return
            print(f"download error {r.status_code} for {path}")
        except requests.RequestException as e:
            print(f"download error {e}")
        time.sleep(5 * (attempt + 1))
    sys.exit(f"Could not download {path}. The link may have expired: generate that line again.")


def tts_api(text, path):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("No ELEVENLABS_API_KEY. Use the ElevenLabs connector and --from-urls (see top of this file).")
    for attempt in range(3):
        r = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=mp3_44100_128",
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
    from_urls = "--from-urls" in sys.argv
    os.makedirs(f"{d}/audio", exist_ok=True)
    rows = list(csv.DictReader(open(f"{d}/LINES.tsv", encoding="utf-8"), delimiter="\t"))
    urls = {}
    if from_urls:
        urls = {r["id"]: r["url"] for r in
                csv.DictReader(open(f"{d}/audio/urls.tsv", encoding="utf-8"), delimiter="\t")}
        missing = [r["id"] for r in rows if r["id"] not in urls]
        if missing:
            sys.exit(f"audio/urls.tsv has no clip for line(s): {', '.join(missing)}")
    t, out = 0.0, []
    for row in rows:
        p = f"{d}/audio/{row['id']}.mp3"
        if force or not os.path.exists(p):
            if from_urls:
                raw = f"{d}/audio/{row['id']}.raw.mp3"
                download(urls[row["id"]], raw)
                speed_up(raw, p)
                os.remove(raw)
            else:
                tts_api(row["text"], p)  # API applies the speed itself
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
