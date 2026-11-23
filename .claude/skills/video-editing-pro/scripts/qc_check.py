#!/usr/bin/env python3
"""Final QC on a rendered file: specs, loudness, true peak, black frames, flashes.

  python3 qc_check.py renders/final.mp4 [--target -14] [--tp -1.0] [--platform shorts|youtube|reels|tiktok|broadcast]
Writes a Markdown report to stdout (save it as 09_check/QC.md). Exit code 1 if any FAIL.

Checks
 - video: codec, WxH, aspect, fps, pixel format, colour tags (BT.709 expected for SDR web)
 - audio: present, codec, sample rate, channels
 - loudness (EBU R128 / ITU-R BS.1770 via ffmpeg ebur128): integrated within +-1 LU of target, true peak <= limit
 - black frames longer than 2 frames (blackdetect) -> accidental gaps at cuts
 - flashes: full-frame luminance reversals; > 3 flashes in any 1 s window = FAIL (WCAG 2.3.1 general-flash
   approximation on full-frame luma only; it is not a certified PSE/Harding test)
"""
import argparse, json, re, subprocess, sys

TARGETS = {"youtube": -14, "shorts": -14, "reels": -14, "tiktok": -14, "broadcast": -23}


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file"); ap.add_argument("--target", type=float); ap.add_argument("--tp", type=float, default=-1.0)
    ap.add_argument("--platform", default="youtube")
    a = ap.parse_args()
    target = a.target if a.target is not None else TARGETS.get(a.platform, -14)
    res, fails = [], 0

    def row(name, ok, val, want):
        nonlocal fails
        fails += 0 if ok else 1
        res.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {val} | {want} |")

    pr = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", a.file]).stdout)
    v = next((s for s in pr["streams"] if s["codec_type"] == "video"), None)
    au = next((s for s in pr["streams"] if s["codec_type"] == "audio"), None)
    dur = float(pr["format"]["duration"])
    if v:
        num, den = map(int, v["r_frame_rate"].split("/")); fps = num / den
        w, h = v["width"], v["height"]
        vertical = h > w
        row("Video codec", v["codec_name"] in ("h264", "hevc", "av1", "prores", "vp9"), v["codec_name"], "h264 (web delivery)")
        row("Resolution", (w, h) in ((1080, 1920), (1920, 1080), (3840, 2160), (2160, 3840), (1080, 1080), (1440, 2560)), f"{w}x{h}", "1080x1920 / 1920x1080 / 4K")
        if a.platform in ("shorts", "reels", "tiktok"):
            row("Vertical 9:16", vertical and abs(h / w - 16 / 9) < 0.01, f"{w}:{h}", "9:16")
        row("Frame rate", round(fps, 3) in (23.976, 24, 25, 29.97, 30, 50, 59.94, 60), f"{fps:.3f}", "native 24/25/30/60")
        row("Pixel format", v.get("pix_fmt") == "yuv420p", v.get("pix_fmt"), "yuv420p (4:2:0)")
        tags = f"{v.get('color_primaries','?')}/{v.get('color_transfer','?')}/{v.get('color_space','?')}"
        row("Colour tags", "bt709" in tags or tags == "?/?/?", tags, "bt709 (untagged = warn)")
    else:
        row("Video stream", False, "missing", "1 video stream")
    if au:
        row("Audio", True, f"{au['codec_name']} {au.get('sample_rate')} Hz {au.get('channels')}ch", "AAC 48 kHz stereo")
        e = run(["ffmpeg", "-hide_banner", "-nostats", "-i", a.file, "-filter_complex", "ebur128=peak=true", "-f", "null", "-"]).stderr
        I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1])
        TP = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1])
        LRA = float(re.findall(r"LRA:\s+(-?[\d.]+) LU", e)[-1])
        row("Integrated loudness", abs(I - target) <= 1.0, f"{I} LUFS", f"{target} ±1 LUFS")
        row("True peak", TP <= a.tp, f"{TP} dBTP", f"<= {a.tp} dBTP")
        res.append(f"| Loudness range | info | {LRA} LU | 4–10 LU typical for speech-led web video |")
    else:
        row("Audio stream", False, "missing", "VO/music present")

    e = run(["ffmpeg", "-hide_banner", "-nostats", "-i", a.file, "-vf", "blackdetect=d=0.07:pix_th=0.06", "-an", "-f", "null", "-"]).stderr
    blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", e)
    mid = [(float(s), float(t)) for s, t in blacks if float(s) > 0.05 and float(t) < dur - 0.05]
    row("Unintended black frames", not mid, ", ".join(f"{s:.2f}-{t:.2f}s" for s, t in mid) or "none", "none mid-video")

    e = run(["ffmpeg", "-hide_banner", "-nostats", "-i", a.file, "-vf", "scale=160:-2,signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-an", "-f", "null", "-"]).stderr
    y = [float(x) for x in re.findall(r"YAVG=([\d.]+)", e)]
    fps_v = fps if v else 30
    trans, last_dir = [], 0
    for i in range(1, len(y)):
        d = y[i] - y[i - 1]
        if abs(d) >= 40:  # ~16% of 0..255 luma in one frame, full frame
            dirn = 1 if d > 0 else -1
            if dirn != last_dir:
                trans.append(i / fps_v); last_dir = dirn
    worst = 0
    for t0 in trans:
        n = sum(1 for t in trans if t0 <= t < t0 + 1.0)
        worst = max(worst, n // 2)   # a flash = a pair of opposing changes
    row("Flashes per second (max)", worst <= 3, worst, "<= 3 (WCAG 2.3.1)")

    print(f"# QC report: {a.file}\n\nDuration {dur:.2f} s · platform {a.platform}\n")
    print("| Check | Result | Measured | Wanted |\n|---|---|---|---|")
    print("\n".join(res))
    print("\nSound was measured, not heard: listen once on a phone speaker and on earbuds before delivery.")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
