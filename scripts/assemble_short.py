"""Build a 1080x1920 Short from LINES/audio/SHOTS/CAPTIONS.

  python scripts/assemble_short.py videos/<dir>

Reads:
  audio/timings.tsv   (from voiceover.py)  id, start, duration, gap
  audio/<id>.mp3
  SHOTS.tsv           id, type(image|card), source, motion(zoomin|zoomout|panleft|panright|none), overlay
  CAPTIONS.tsv        id, caption   (Roman Hinglish on-screen text)
  assets/music/*.mp3  optional royalty-free background music
Writes final/short.mp4 (and work files in build/).

Look settings come from environment variables so EDIT_STYLE.md can change them:
  CAPTION_FONT (default "DejaVu Sans"), CAPTION_SIZE (78), CAPTION_WORDS (3),
  ACCENT (hex, default F5C518), BG (hex, default 111111), MUSIC_VOL (0.16)
"""
import csv
import glob
import os
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FONT = os.environ.get("CAPTION_FONT", "DejaVu Sans")
CAP_SIZE = int(os.environ.get("CAPTION_SIZE", 78))
CAP_WORDS = int(os.environ.get("CAPTION_WORDS", 3))
ACCENT = os.environ.get("ACCENT", "F5C518")
BG = os.environ.get("BG", "111111")
MUSIC_VOL = float(os.environ.get("MUSIC_VOL", 0.16))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + " ".join(cmd) + "\n" + r.stderr[-2000:])


def tsv(path):
    return {r["id"]: r for r in csv.DictReader(open(path, encoding="utf-8"), delimiter="\t")}


def bold_font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def make_card(text, path):
    img = Image.new("RGB", (W, H), hexrgb(BG))
    d = ImageDraw.Draw(img)
    d.rectangle([90, 540, 250, 556], fill=hexrgb(ACCENT))
    size = 150 if len(text) <= 12 else 110 if len(text) <= 30 else 84
    f = bold_font(size)
    lines = textwrap.wrap(text, width=max(6, int(900 / (size * 0.58))))
    y = 600
    for ln in lines:
        d.text((90, y), ln, font=f, fill=(255, 255, 255))
        y += int(size * 1.2)
    img.save(path)


def make_overlay(text, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = bold_font(64)
    lines = textwrap.wrap(text.upper(), width=22)
    box_h = 60 + 80 * len(lines)
    d.rectangle([60, 230, W - 60, 230 + box_h], fill=hexrgb(BG) + (215,))
    d.rectangle([60, 230, 76, 230 + box_h], fill=hexrgb(ACCENT) + (255,))
    y = 260
    for ln in lines:
        d.text((110, y), ln, font=f, fill=hexrgb(ACCENT) + (255,))
        y += 80
    img.save(path)


def motion_filter(motion, frames):
    # Input is scaled to cover 2W x 2H, then zoompan renders W x H.
    z = {"zoomin": "1+0.12*on/{f}", "zoomout": "1.12-0.12*on/{f}"}.get(motion, "1.08").format(f=frames)
    x = {"panleft": "(iw-iw/zoom)*(1-on/{f})", "panright": "(iw-iw/zoom)*on/{f}"}.get(
        motion, "iw/2-(iw/zoom/2)").format(f=frames)
    y = "ih/2-(ih/zoom/2)"
    if motion == "none":
        z = "1"
    return (f"scale={2 * W}:{2 * H}:force_original_aspect_ratio=increase,crop={2 * W}:{2 * H},"
            f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS},setsar=1")


def ass_time(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def write_ass(timings, captions, path):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{FONT},{CAP_SIZE},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,6,2,2,80,80,{int(os.environ.get('CAPTION_MARGIN_V', 720))},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    acc = "&H00" + ACCENT[4:6] + ACCENT[2:4] + ACCENT[0:2] + "&"
    ev = []
    for i, t in timings.items():
        cap = (captions.get(i) or {}).get("caption", "").strip()
        if not cap:
            continue
        words = cap.split()
        chunks = [words[k:k + CAP_WORDS] for k in range(0, len(words), CAP_WORDS)]
        start, dur = float(t["start"]), float(t["duration"])
        total = sum(len(" ".join(c)) for c in chunks) or 1
        cur = start
        for c in chunks:
            seg = dur * len(" ".join(c)) / total
            txt = " ".join(c).upper()
            # highlight numbers / years in the accent colour
            txt = " ".join(f"{{\\c{acc}}}{w}{{\\c&H00FFFFFF&}}" if any(ch.isdigit() for ch in w) else w
                           for w in txt.split())
            ev.append(f"Dialogue: 0,{ass_time(cur)},{ass_time(cur + seg)},Cap,,0,0,0,,{{\\fad(40,0)}}{txt}")
            cur += seg
    open(path, "w", encoding="utf-8").write(head + "\n".join(ev) + "\n")


def main():
    d = sys.argv[1].rstrip("/")
    b = f"{d}/build"
    os.makedirs(b, exist_ok=True)
    os.makedirs(f"{d}/final", exist_ok=True)
    timings = tsv(f"{d}/audio/timings.tsv")
    shots = tsv(f"{d}/SHOTS.tsv")
    captions = tsv(f"{d}/CAPTIONS.tsv") if os.path.exists(f"{d}/CAPTIONS.tsv") else {}
    ids = list(timings)
    missing = [i for i in ids if i not in shots]
    if missing:
        sys.exit(f"SHOTS.tsv has no shot for lines: {', '.join(missing)}")

    seg_list, wav_list = [], []
    for n, i in enumerate(ids):
        t, s = timings[i], shots[i]
        seg = float(t["duration"]) + float(t["gap"]) + (0.6 if n == len(ids) - 1 else 0)
        frames = max(int(round(seg * FPS)), 1)
        src = s["source"]
        if s["type"] == "card":
            src = f"{b}/card_{i}.png"
            make_card(s["source"], src)
        elif not os.path.isabs(src) and not os.path.exists(src):
            src = os.path.join(d, src)
        if not os.path.exists(src):
            sys.exit(f"Line {i}: image not found: {src}")
        vf = motion_filter(s.get("motion") or "zoomin", frames)
        out = f"{b}/seg_{i}.mp4"
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", src]
        if (s.get("overlay") or "").strip():
            ov = f"{b}/ov_{i}.png"
            make_overlay(s["overlay"].strip(), ov)
            cmd += ["-loop", "1", "-i", ov, "-filter_complex", f"[0:v]{vf}[bg];[bg][1:v]overlay=0:0,format=yuv420p[v]",
                    "-map", "[v]"]
        else:
            cmd += ["-vf", vf + ",format=yuv420p"]
        run(cmd + ["-frames:v", str(frames), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast",
                   "-crf", "18", "-an", out])
        seg_list.append(out)
        wav = f"{b}/a_{i}.wav"
        run(["ffmpeg", "-y", "-i", f"{d}/audio/{i}.mp3", "-af", f"apad=whole_dur={seg:.3f}", "-t", f"{seg:.3f}",
             "-ar", "48000", "-ac", "2", wav])
        wav_list.append(wav)

    for name, items in (("video.txt", seg_list), ("audio.txt", wav_list)):
        open(f"{b}/{name}", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in items))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"{b}/video.txt", "-c", "copy", f"{b}/video.mp4"])
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"{b}/audio.txt", "-c", "copy", f"{b}/voice.wav"])

    voice = f"{b}/voice.wav"
    music = sorted(glob.glob(f"{d}/assets/music/*.mp3"))
    if music:
        run(["ffmpeg", "-y", "-i", voice, "-stream_loop", "-1", "-i", music[0], "-filter_complex",
             f"[1:a]volume={MUSIC_VOL}[m];[0:a][m]amix=inputs=2:duration=first:normalize=0[a]",
             "-map", "[a]", f"{b}/mix.wav"])
        voice = f"{b}/mix.wav"

    write_ass(timings, captions, f"{b}/captions.ass")
    run(["ffmpeg", "-y", "-i", f"{b}/video.mp4", "-i", voice, "-vf", f"ass={b}/captions.ass",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
         "-shortest", "-movflags", "+faststart", f"{d}/final/short.mp4"])
    total = sum(float(timings[i]["duration"]) + float(timings[i]["gap"]) for i in ids) + 0.6
    print(f"Built {d}/final/short.mp4  (~{total:.1f} s, {len(ids)} lines)")


if __name__ == "__main__":
    main()
