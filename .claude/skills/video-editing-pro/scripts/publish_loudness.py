#!/usr/bin/env python3
"""Two-pass loudnorm on a rendered video's audio; video stream copied untouched.

  python3 publish_loudness.py renders/final.mp4 renders/final_social.mp4 [--lufs -14] [--tp -1.5] [--lra 11]

HyperFrames mixes around -16 LUFS by default (measured in testing); social platforms normalise to about -14.
Pass 1 measures, pass 2 applies the measured values (linear=true keeps dynamics when possible).
Run scripts/qc_check.py on the output afterwards.
"""
import argparse, json, re, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--lufs", type=float, default=-14); ap.add_argument("--tp", type=float, default=-1.5)
ap.add_argument("--lra", type=float, default=11)
a = ap.parse_args()
base = f"loudnorm=I={a.lufs}:TP={a.tp}:LRA={a.lra}"
err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", a.src, "-af", base + ":print_format=json",
                      "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(re.findall(r"\{[^{}]+\}", err)[-1])
f2 = (f"{base}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=summary")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.src, "-af", f2, "-ar", "48000",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "384k", "-movflags", "+faststart", a.dst], check=True)
print(f"measured {m['input_i']} LUFS / {m['input_tp']} dBTP -> target {a.lufs} LUFS / {a.tp} dBTP: {a.dst}")
