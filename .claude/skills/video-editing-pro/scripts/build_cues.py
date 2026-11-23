#!/usr/bin/env python3
"""Time every script line (and word) from the REAL voice-over, not an even split.

  python3 build_cues.py --vo assets/audio/vo.wav --lines LINES.tsv --out cues.json \
      [--fps 30] [--noise -35] [--min-silence 0.28] [--bpm 96 --beat-offset 0.0]

LINES.tsv: one line per row, `id<TAB>text` (extra columns ignored, header optional).
Text may be Devanagari, Roman Hinglish or English.

How it works:
 1. ffmpeg silencedetect finds speech spans (default -35 dB, pauses >= 0.28 s).
 2. Spans are merged (smallest gap first) or split (longest span, by character share)
    until there is exactly one span per script line.
 3. Words inside a line get time in proportion to their visible character count.
 4. All times are quantised to frames, so captions, SFX and cuts land on the same frame.
Output cues.json: {fps, duration, speech:[[s,e],...], lines:[{id,text,start,end,words:[{text,start,end}]}], beats:[...]}.
Always eyeball the result: open the VO waveform or snapshot captions at 3-4 line starts.
"""
import argparse, json, re, subprocess, sys, unicodedata


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", path], capture_output=True, text=True).stdout
    return float(out.strip())


def speech_spans(path, noise, dmin):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
                          f"silencedetect=noise={noise}dB:d={dmin}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    dur = probe_duration(path)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    silences = list(zip(starts, ends + [dur] * (len(starts) - len(ends))))
    spans, t = [], 0.0
    for s, e in silences:
        if s - t > 0.05:
            spans.append([t, s])
        t = e
    if dur - t > 0.05:
        spans.append([t, dur])
    return spans, dur


def vis_len(s):
    # count base characters; Devanagari matras/viramas (combining marks) add no width
    return max(1, sum(1 for ch in s if not unicodedata.category(ch).startswith("M") and not ch.isspace()))


def fit(spans, texts):
    spans = [list(x) for x in spans]
    n = len(texts)
    while len(spans) > n:            # merge across the smallest pause
        gaps = [spans[i + 1][0] - spans[i][1] for i in range(len(spans) - 1)]
        i = gaps.index(min(gaps))
        spans[i:i + 2] = [[spans[i][0], spans[i + 1][1]]]
    while len(spans) < n:            # split the longest span by character share
        i = max(range(len(spans)), key=lambda k: spans[k][1] - spans[k][0])
        k = len(spans)  # which lines does span i hold? assume in order
        a, b = spans[i]
        mid = a + (b - a) / 2
        spans[i:i + 1] = [[a, mid], [mid, b]]
    return spans


def q(t, fps):
    return round(round(t * fps) / fps, 4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vo", required=True); ap.add_argument("--lines", required=True)
    ap.add_argument("--out", default="cues.json"); ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--noise", type=float, default=-35); ap.add_argument("--min-silence", type=float, default=0.28)
    ap.add_argument("--offset", type=float, default=0.0, help="VO start time on the root timeline")
    ap.add_argument("--bpm", type=float); ap.add_argument("--beat-offset", type=float, default=0.0)
    a = ap.parse_args()

    rows = []
    for ln in open(a.lines, encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln.strip():
            continue
        parts = ln.split("\t")
        if len(parts) == 1:
            parts = [f"L{len(rows)+1:02d}", parts[0]]
        if parts[0].lower() in ("id", "line_id") and len(rows) == 0:
            continue
        rows.append((parts[0], parts[1].strip()))
    spans, dur = speech_spans(a.vo, a.noise, a.min_silence)
    if not spans:
        sys.exit("no speech found: lower --noise (e.g. -45) or check the file")
    raw = len(spans)
    spans = fit(spans, [t for _, t in rows])
    lines = []
    for (lid, text), (s, e) in zip(rows, spans):
        words = text.split()
        tot = sum(vis_len(w) for w in words)
        t, ws = s, []
        for w in words:
            d = (e - s) * vis_len(w) / tot
            ws.append({"text": w, "start": q(t + a.offset, a.fps), "end": q(t + d + a.offset, a.fps)})
            t += d
        lines.append({"id": lid, "text": text, "start": q(s + a.offset, a.fps),
                      "end": q(e + a.offset, a.fps), "words": ws})
    beats = []
    if a.bpm:
        fpb = 60.0 / a.bpm
        k = 0
        while a.beat_offset + k * fpb < dur + a.offset:
            beats.append(q(a.beat_offset + k * fpb, a.fps)); k += 1   # index-based: no drift
    out = {"fps": a.fps, "duration": round(dur, 3), "offset": a.offset,
           "speech": [[q(s + a.offset, a.fps), q(e + a.offset, a.fps)] for s, e in speech_spans(a.vo, a.noise, a.min_silence)[0]],
           "lines": lines, "beats": beats}
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(rows)} lines, {raw} raw speech spans -> {a.out}")
    if raw != len(rows):
        print(f"WARNING: span count ({raw}) != line count ({len(rows)}); merged/split automatically. Check timing.")


if __name__ == "__main__":
    main()
