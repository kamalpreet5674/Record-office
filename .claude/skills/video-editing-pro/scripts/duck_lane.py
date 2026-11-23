#!/usr/bin/env python3
"""Make a HyperFrames `data-automation` volume lane that ducks music under speech.

  python3 duck_lane.py --cues cues.json --music-start 0 --music-len 26 \
      [--duck 0.32] [--attack 0.08] [--release 0.45] [--bridge 0.9] [--html]

Reads speech spans from cues.json (build_cues.py). Gaps shorter than --bridge seconds stay
ducked (stops "pumping" between words). Prints the JSON lane, or with --html the attribute
already escaped (&quot;) for pasting on the music <audio>.
Levels: 0.32 ~ -10 dB, 0.2 ~ -14 dB, 0.14 ~ -17 dB (HyperFrames sound guide: bed ~0.14 under VO
when no lane is used). Keep data-volume="1" on the element when you use this lane
(the lane multiplies data-volume).
"""
import argparse, json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cues", required=True)
    ap.add_argument("--music-start", type=float, default=0.0, help="music data-start on its timeline")
    ap.add_argument("--music-len", type=float, required=True)
    ap.add_argument("--full", type=float, default=1.0); ap.add_argument("--duck", type=float, default=0.32)
    ap.add_argument("--attack", type=float, default=0.08); ap.add_argument("--release", type=float, default=0.45)
    ap.add_argument("--bridge", type=float, default=0.9); ap.add_argument("--html", action="store_true")
    a = ap.parse_args()
    sp = json.load(open(a.cues, encoding="utf-8"))["speech"]
    merged = []
    for s, e in sp:
        if merged and s - merged[-1][1] < a.bridge:
            merged[-1][1] = e
        else:
            merged.append([s, e])
    pts = [{"t": 0, "v": a.full}]
    for s, e in merged:
        s0, e0 = s - a.music_start, e - a.music_start
        if e0 <= 0 or s0 >= a.music_len:
            continue
        pts += [{"t": round(max(0, s0 - a.attack), 3), "v": a.full}, {"t": round(max(0, s0), 3), "v": a.duck},
                {"t": round(min(a.music_len, e0), 3), "v": a.duck},
                {"t": round(min(a.music_len, e0 + a.release), 3), "v": a.full}]
    # keep strictly increasing times
    clean = []
    for p in pts:
        if clean and p["t"] <= clean[-1]["t"]:
            clean[-1] = p if p["t"] == clean[-1]["t"] else clean[-1]
            continue
        clean.append(p)
    lane = {"version": 1, "lanes": [{"target": "volume", "points": clean[:512]}]}
    s = json.dumps(lane, separators=(",", ":"))
    print(s.replace('"', "&quot;") if a.html else s)


if __name__ == "__main__":
    main()
