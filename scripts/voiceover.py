"""ElevenLabs voiceover, one file per LINES.tsv row.

  python scripts/voiceover.py videos/<dir> [--force]

Needs secrets ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID (your cloned voice).
Writes videos/<dir>/audio/<id>.mp3 and audio/timings.tsv (id, start, duration, gap).
"""
import csv
import hashlib
import json
import os
import subprocess
import sys
import time

import requests

MODEL = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
SPEED = float(os.environ.get("ELEVENLABS_SPEED", 1.1))  # owner prefers 1.10x
MAX_CHARS = int(os.environ.get("ELEVENLABS_MAX_CHARS", 2500))  # credit guard per video


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


PAUSE_MAX = float(os.environ.get("PAUSE_MAX", 0.28))  # longest pause kept inside a line (seconds)
VOICE_TEMPO = float(os.environ.get("VOICE_TEMPO", 1.0))  # extra speed-up on top of ElevenLabs speed, no new credits


def tighten(src, dst):
    af = (f"silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.05,"
          f"silenceremove=stop_periods=-1:stop_duration={PAUSE_MAX}:stop_threshold=-38dB:stop_silence={PAUSE_MAX}")
    if abs(VOICE_TEMPO - 1.0) > 1e-3:
        af += f",atempo={VOICE_TEMPO}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", af, "-ar", "44100", "-b:a", "128k", dst],
                   check=True)


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
    mpath = f"{d}/audio/manifest.json"
    manifest = json.load(open(mpath)) if os.path.exists(mpath) else {}

    def key(text):
        return hashlib.sha1(f"{text}|{os.environ.get('ELEVENLABS_VOICE_ID')}|{MODEL}|{SPEED}".encode()).hexdigest()

    # Only lines that are new or whose text changed cost credits.
    todo = [r for r in rows if force or manifest.get(r["id"]) != key(r["text"])
            or not os.path.exists(f"{d}/audio/{r['id']}.mp3")]
    chars = sum(len(r["text"]) for r in todo)
    print(f"{len(todo)} of {len(rows)} lines need new audio ({chars} characters)")
    if chars > MAX_CHARS:
        sys.exit(f"Stopping: {chars} characters is over the {MAX_CHARS} limit per video. Shorten the script.")
    for r in todo:
        tts(r["text"], f"{d}/audio/{r['id']}.mp3")
        manifest[r["id"]] = key(r["text"])
        json.dump(manifest, open(mpath, "w"), indent=1)

    # Tighten long pauses (the "..." in the script) without new credits: the raw clip is kept in
    # audio/raw/, the clip used in the video has every pause longer than PAUSE_MAX cut down to it.
    os.makedirs(f"{d}/audio/raw", exist_ok=True)
    for row in rows:
        p, raw = f"{d}/audio/{row['id']}.mp3", f"{d}/audio/raw/{row['id']}.mp3"
        if row in todo or not os.path.exists(raw):
            os.replace(p, raw)
        tighten(raw, p)

    t, out = 0.0, []
    for row in rows:
        p = f"{d}/audio/{row['id']}.mp3"
        dur, gap = duration(p), float(row.get("gap") or 0.35)
        out.append((row["id"], t, dur, gap))
        t += dur + gap
    with open(f"{d}/audio/timings.tsv", "w") as f:
        f.write("id\tstart\tduration\tgap\n")
        for i, s0, du, g in out:
            f.write(f"{i}\t{s0:.3f}\t{du:.3f}\t{g:.2f}\n")
    print(f"{len(rows)} lines, total {t:.1f} s (target 60-70 s)")


if __name__ == "__main__":
    main()
