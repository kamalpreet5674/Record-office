"""Build a 1080x1920 Short (or, with LANDSCAPE=1, a 1920x1080 long video) from LINES/audio/SHOTS/CAPTIONS.

  python scripts/assemble_short.py videos/<dir>

Reads:
  audio/timings.tsv   (from voiceover.py)  id, start, duration, gap
  audio/<id>.mp3
  SHOTS.tsv           id, type(image|video|doc|card), source, motion(zoomin|zoomout|panleft|panright|none), overlay
                      image: photo path · video: clip path, optional "@start" seconds (assets/x.webm@12)
                      doc: screenshot of a real source page (framed like a document) · card: text
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
import re
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

LANDSCAPE = os.environ.get("LANDSCAPE") == "1"  # 1 = 1920x1080 long video, else 1080x1920 Short
W, H, FPS = (1920, 1080, 30) if LANDSCAPE else (1080, 1920, 30)
FONT = os.environ.get("CAPTION_FONT", "DejaVu Sans")
CAP_SIZE = int(os.environ.get("CAPTION_SIZE", 78))
CAP_WORDS = int(os.environ.get("CAPTION_WORDS", 3))
ACCENT = os.environ.get("ACCENT", "F5C518")
BG = os.environ.get("BG", "111111")
MUSIC_VOL = float(os.environ.get("MUSIC_VOL", 0.16))
TRANS = float(os.environ.get("TRANS", 0.25))  # crossover transition length in seconds (0 = hard cuts)
TRANS_CYCLE = os.environ.get("TRANS_CYCLE", "zoomin,smoothleft,fadewhite,slideup,radial,smoothright,zoomin,wipeup,hblur").split(",")
SFX_VOL = float(os.environ.get("SFX_VOL", 0.75))
FAST_CLIPS = os.environ.get("FAST_CLIPS", "1") == "1"  # play stock/trailer clips a bit faster
CLIP_SPEED = float(os.environ.get("CLIP_SPEED", 1.25))
MUSIC_BASS = float(os.environ.get("MUSIC_BASS", 5))  # dB bass boost on the music
LEAKS = []  # filled in main() from <video>/assets/fxclips/leak*.mp4


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
    top = int(H * 0.28)
    d.rectangle([90, top, 250, top + 16], fill=hexrgb(ACCENT))
    size = 150 if len(text) <= 12 else 110 if len(text) <= 30 else 84
    f = bold_font(size)
    lines = textwrap.wrap(text, width=max(6, int((W - 180) / (size * 0.58))))
    y = top + 60
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
    oy = 80 if LANDSCAPE else 230
    d.rectangle([60, oy, W - 60, oy + box_h], fill=hexrgb(BG) + (215,))
    d.rectangle([60, oy, 76, oy + box_h], fill=hexrgb(ACCENT) + (255,))
    y = oy + 30
    for ln in lines:
        d.text((110, y), ln, font=f, fill=hexrgb(ACCENT) + (255,))
        y += 80
    img.save(path)


def audio_len(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 1.0


def effects_filter(fx, vis):
    """Entry/emphasis effects added after a shot's own motion. fx = comma list of
    punch (zoom-punch in, default), zoomout (starts wide, punches out), flash (white flash in),
    shake (camera shake on impact), none."""
    out = ""
    names = [x.strip() for x in fx.split(",") if x.strip()]
    if "none" in names:
        return out
    if "punch" in names:
        out += (f",scale=w='trunc(iw*(1+0.22*max(0\\,1-t/0.28))/2)*2':h=-2:eval=frame,"
                f"crop={W}:{H}")
    if "zoomout" in names:
        out += (f",scale=w='trunc(iw*(1.25-0.25*min(1\\,t/0.35))/2)*2':h=-2:eval=frame,crop={W}:{H}")
    if "shake" in names:
        out += (f",scale={int(W * 1.06)}:-2,crop={W}:{H}:x='(iw-{W})/2+14*sin(t*75)*lt(t\\,0.45)'"
                f":y='(ih-{H})/2+12*cos(t*63)*lt(t\\,0.45)'")
    if "flash" in names:
        out += ",fade=t=in:st=0:d=0.22:color=white"
    if "glitch" in names:  # RGB split for the first frames
        out += ",rgbashift=rh=-16:bh=16:gv=6:enable='lt(t\\,0.22)',noise=alls=40:allf=t:enable='lt(t\\,0.12)'"
    if "blurin" in names:
        out += ",boxblur=14:enable='lt(t\\,0.10)',boxblur=6:enable='between(t\\,0.10\\,0.18)'"
    return out


def make_big_text(text, path):
    """Hook title: big centred words with a thick outline, for the first seconds."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = bold_font(132)
    lines = [x.strip() for x in text.upper().split("/")] if "/" in text else textwrap.wrap(text.upper(), width=11)
    y = int(H * 0.30) - len(lines) * 75
    for n, ln in enumerate(lines):
        w = d.textlength(ln, font=f)
        col = hexrgb(ACCENT) if n % 2 else (255, 255, 255)
        d.text(((W - w) / 2, y), ln, font=f, fill=col + (255,), stroke_width=10, stroke_fill=(0, 0, 0, 255))
        y += 150
    img.save(path)


def make_sticker(src, path, tilt=2.0):
    """Cutout/sticker look: the photo with a thick white border, a soft shadow and a slight tilt,
    on a blurred, darkened copy of itself."""
    from PIL import ImageFilter
    im = Image.open(src).convert("RGB")
    bg = im.copy()
    r = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * r) + 1, int(bg.height * r) + 1)).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(28))
    bg = Image.blend(bg, Image.new("RGB", (W, H), hexrgb(BG)), 0.35)
    fw = int(W * 0.84)
    fh = int(im.height * fw / im.width)
    if fh > int(H * 0.62):
        fh = int(H * 0.62)
        fw = int(im.width * fh / im.height)
    fg = im.resize((fw, fh))
    bd = 16
    card = Image.new("RGBA", (fw + 2 * bd, fh + 2 * bd), (255, 255, 255, 255))
    card.paste(fg, (bd, bd))
    card = card.rotate(tilt, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 160), mask=card.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    out = bg.convert("RGBA")
    x, y = (W - card.width) // 2, int(H * 0.40 - card.height / 2)
    out.alpha_composite(sh, (x + 14, y + 22))
    out.alpha_composite(card, (x, y))
    out.convert("RGB").save(path)


def make_doc(src, path):
    """Real document screenshot on a blurred copy of itself, with a white border and shadow."""
    from PIL import ImageFilter
    doc = Image.open(src).convert("RGB")
    bg = doc.resize((W, H)).filter(ImageFilter.GaussianBlur(30))
    bg = Image.blend(bg, Image.new("RGB", (W, H), hexrgb(BG)), 0.45)
    max_w, max_h = (1500, 900) if LANDSCAPE else (940, 1150)
    dw = max_w
    dh = int(doc.height * dw / doc.width)
    if dh > max_h:
        dh = max_h
        dw = int(doc.width * dh / doc.height)
    doc = doc.resize((dw, dh))
    x, y = (W - dw) // 2, ((H - dh) // 2 if LANDSCAPE else 420)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle([x - 4, y + 18, x + dw + 22, y + dh + 34], fill=(0, 0, 0, 150))
    bg = Image.alpha_composite(bg.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(14))).convert("RGB")
    ImageDraw.Draw(bg).rectangle([x - 10, y - 10, x + dw + 10, y + dh + 10], fill=(255, 255, 255))
    bg.paste(doc, (x, y))
    bg.save(path)


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
Style: Cap,{FONT},{CAP_SIZE},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,6,2,2,80,80,{int(os.environ.get('CAPTION_MARGIN_V', 90 if LANDSCAPE else 720))},1

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
            ev.append(f"Dialogue: 0,{ass_time(cur)},{ass_time(cur + seg)},Cap,,0,0,0,,"
                      f"{{\\fscx72\\fscy72\\t(0,90,\\fscx108\\fscy108)\\t(90,150,\\fscx100\\fscy100)}}{txt}")
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

    # Build the picture track as "parts": a line's source may list several visuals separated by "|",
    # each optionally typed ("video:assets/x.mp4@3", "sticker:assets/y.jpg", "card:TEXT", "doc:...").
    # The line's time is split between them, so the picture changes every 2-3 seconds.
    parts, wav_list, line_lens = [], [], []
    for n, i in enumerate(ids):
        t, s = timings[i], shots[i]
        seg = float(t["duration"]) + float(t["gap"]) + (0.6 if n == len(ids) - 1 else 0)
        line_lens.append(seg)
        items = [x.strip() for x in s["source"].split("|") if x.strip()]
        motions = [m.strip() for m in (s.get("motion") or "").split("|")]
        for k, it in enumerate(items):
            kind = s["type"].strip()
            m = re.match(r"^(video|image|doc|card|sticker):(.*)$", it)
            if m:
                kind, it = m.group(1), m.group(2)
            parts.append({"line": i, "k": k, "kind": kind, "src": it, "len": seg / len(items),
                          "motion": motions[k] if k < len(motions) and motions[k] else motions[0],
                          "overlay": (s.get("overlay") or "").strip() if (k == 0 or (s.get("overlay") or "").startswith("big:")) else "",
                          "trans": (s.get("trans") or "").strip() if k == 0 else "",
                          "sfx": (s.get("sfx") or "").strip() if k == 0 else "whoosh",
                          "fx": ((s.get("fx") or "").split("|") + [""] * 9)[k].strip()})
        wav = f"{b}/a_{i}.wav"
        run(["ffmpeg", "-y", "-i", f"{d}/audio/{i}.mp3", "-af", f"apad=whole_dur={seg:.3f}", "-t", f"{seg:.3f}",
             "-ar", "48000", "-ac", "2", wav])
        wav_list.append(wav)

    LEAKS[:] = sorted(glob.glob(f"{d}/assets/fxclips/leak*.mp4"))
    seg_list, seg_lens = [], []
    for n, pt in enumerate(parts):
        tag = f"{pt['line']}_{pt['k']}"
        vis = pt["len"] + (TRANS if TRANS and n < len(parts) - 1 else 0)
        frames = max(int(round(vis * FPS)), 1)
        kind, src, start = pt["kind"], pt["src"], 0.0
        out = f"{b}/seg_{tag}.mp4"
        if kind == "card":
            src = f"{b}/card_{tag}.png"
            make_card(pt["src"], src)
        else:
            if kind == "video" and "@" in src:
                src, st = src.rsplit("@", 1)
                start = float(st or 0)
            if not os.path.isabs(src) and not os.path.exists(src):
                src = os.path.join(d, src)
        if not os.path.exists(src):
            sys.exit(f"Line {pt['line']}: file not found: {src}")
        if kind == "doc":
            framed = f"{b}/doc_{tag}.png"
            make_doc(src, framed)
            src = framed
        if kind == "sticker":
            framed = f"{b}/sticker_{tag}.png"
            make_sticker(src, framed, tilt=(-2.5 if n % 2 else 2.0))
            src = framed
        if kind == "video":
            # cover the frame, then a slow push-in so even static clips move
            vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,"
                  f"scale={int(W * 1.12)}:-2,crop={W}:{H}:x='(iw-{W})/2*(1-t/{max(vis, 0.5):.2f})':y='(ih-{H})/2'")
            cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-ss", f"{start:.2f}", "-i", src]
        else:
            vf = motion_filter(pt["motion"] or "zoomin", frames)
            cmd = ["ffmpeg", "-y", "-loop", "1", "-i", src]
        fxn = [x.strip() for x in (pt["fx"] or "punch").split(",")]
        if kind == "video" and ("fast" in fxn or FAST_CLIPS):
            vf = f"setpts=PTS/{CLIP_SPEED}," + vf  # a little faster = more energy
        vf += effects_filter(pt["fx"] or "punch", vis)
        fc, last, nin = [f"[0:v]{vf}[bg]"], "[bg]", 1
        if "leak" in fxn and LEAKS:
            # light leak / lens flare laid over the shot in screen blend
            lk = LEAKS[n % len(LEAKS)]
            cmd += ["-stream_loop", "-1", "-ss", f"{(n * 1.7) % 4:.2f}", "-i", lk]
            fc.append(f"[{nin}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
                      f"format=gbrp[lk];{last}format=gbrp[bgr];[bgr][lk]blend=all_mode=screen:all_opacity=0.8,"
                      f"format=yuv420p[lkd]")
            last, nin = "[lkd]", nin + 1
        if pt["overlay"]:
            ov = f"{b}/ov_{tag}.png"
            if pt["overlay"].startswith("big:"):
                make_big_text(pt["overlay"][4:], ov)
            else:
                make_overlay(pt["overlay"], ov)
            cmd += ["-loop", "1", "-i", ov]
            fc.append(f"{last}[{nin}:v]overlay=0:0[ovd]")
            last = "[ovd]"
        fc.append(f"{last}format=yuv420p[v]")
        cmd += ["-filter_complex", ";".join(fc), "-map", "[v]"]
        run(cmd + ["-frames:v", str(frames), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast",
                   "-crf", "18", "-an", out])
        seg_list.append(out)
        seg_lens.append(pt["len"])

    for name, items in (("video.txt", seg_list), ("audio.txt", wav_list)):
        open(f"{b}/{name}", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in items))
    if TRANS and len(seg_list) > 1:
        # crossover transitions between every picture (xfade); offsets keep the picture in sync with the voice
        inputs, fc, prev, off = [], [], "[0:v]", 0.0
        for k, p in enumerate(seg_list):
            inputs += ["-i", p]
        for k in range(1, len(seg_list)):
            off += seg_lens[k - 1]
            tr = parts[k]["trans"] or TRANS_CYCLE[k % len(TRANS_CYCLE)]
            out_l = f"[x{k}]" if k < len(seg_list) - 1 else "[vout]"
            fc.append(f"{prev}[{k}:v]xfade=transition={tr}:duration={TRANS}:offset={off - TRANS / 2:.3f}{out_l}")
            prev = out_l
        run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-r", str(FPS),
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", f"{b}/video.mp4"])
    else:
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"{b}/video.txt", "-c", "copy", f"{b}/video.mp4"])
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"{b}/audio.txt", "-c", "copy", f"{b}/voice.wav"])

    voice = f"{b}/voice.wav"
    music = sorted(glob.glob(f"{d}/assets/music/*.mp3"))
    if not music:  # fall back to the owner's own library synced from Drive
        lib = sorted(glob.glob("library/**/music/*.mp3", recursive=True) + glob.glob("library/music/*.mp3"))
        if lib:
            import random
            music = [random.Random(d).choice(lib)]  # stable pick per video
    # sound effects: a whoosh on every cut (softer on cuts inside a line), an impact where SHOTS "sfx" says hit
    sfx_dir = f"{d}/assets/sfx"
    whooshes = sorted(glob.glob(f"{sfx_dir}/whoosh*.mp3"))
    hits = sorted(glob.glob(f"{sfx_dir}/hit*.mp3"))
    bank = {name: sorted(glob.glob(f"{sfx_dir}/{name}*.mp3")) for name in
            ("whoosh", "hit", "riser", "money", "pop", "camera", "boom", "glitch", "swoosh", "transition", "sub", "cine")}
    events, t0, drops = [], 0.0, []
    for n, pt in enumerate(parts):
        modes = [m.strip() for m in (pt["sfx"] or ("whoosh" if n else "")).split(",") if m.strip()]
        if pt["overlay"] and "pop" not in modes:
            modes.append("pop")
        for mode in modes:
            files = bank.get(mode) or []
            if mode == "drop" and pt["k"] == 0:
                drops.append((max(t0 - 0.7, 0), t0))
                continue
            if not files:
                continue
            f = files[n % len(files)]
            if mode == "riser":  # ends exactly on the cut
                dur = min(audio_len(f), 2.5)
                events.append((max(t0 - dur, 0), f, SFX_VOL * 0.9, dur))
            elif mode in ("whoosh", "swoosh", "transition"):
                events.append((max(t0 - 0.25, 0), f, SFX_VOL * (1.0 if pt["k"] == 0 else 0.7), 1.2))
            elif mode == "drop":  # music stops just before this cut, comes back on it
                pass
            elif mode in ("hit", "boom", "sub", "cine"):
                events.append((t0, f, SFX_VOL * 1.6, 2.5))
            else:
                events.append((t0, f, SFX_VOL * 1.1, 1.5))
        t0 += seg_lens[n]
    if events:
        ins, fc = ["-i", voice], []
        for k, (at, f, vol, ln) in enumerate(events, start=1):
            ins += ["-i", f]
            fc.append(f"[{k}:a]atrim=0:{ln},afade=t=out:st={max(ln - 0.3, 0)}:d=0.3,volume={vol},"
                      f"adelay={int(at * 1000)}|{int(at * 1000)}[s{k}]")
        fc.append("".join(f"[s{k}]" for k in range(1, len(events) + 1)) +
                  f"amix=inputs={len(events)}:normalize=0[sfx];[0:a][sfx]amix=inputs=2:duration=first:normalize=0[a]")
        run(["ffmpeg", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[a]", f"{b}/voice_sfx.wav"])
        voice_for_duck = f"{b}/voice.wav"
        voice = f"{b}/voice_sfx.wav"
    else:
        voice_for_duck = voice
    if music:
        # music ducks under the voice (sidechain) so words stay clear
        run(["ffmpeg", "-y", "-i", voice, "-stream_loop", "-1", "-ss", os.environ.get("MUSIC_START", "0"), "-i", music[0], "-i", voice_for_duck, "-filter_complex",
             f"[1:a]volume={MUSIC_VOL * 2.2},bass=g={MUSIC_BASS}:f=90"
             + "".join(f",volume=0:enable='between(t\\,{a:.2f}\\,{b2:.2f})'" for a, b2 in drops) + "[m];"
             f"[2:a]asplit=1[sc];"
             f"[m][sc]sidechaincompress=threshold=0.06:ratio=3:attack=15:release=250[md];"
             f"[0:a][md]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={sum(line_lens) - 1.2:.2f}:d=1.2[a]",
             "-map", "[a]", f"{b}/mix.wav"])
        voice = f"{b}/mix.wav"

    write_ass(timings, captions, f"{b}/captions.ass")
    grade = os.environ.get("GRADE", "eq=contrast=1.06:saturation=1.15,vignette=PI/5,noise=alls=4:allf=t")
    run(["ffmpeg", "-y", "-i", f"{b}/video.mp4", "-i", voice, "-vf", (grade + "," if grade else "") + f"ass={b}/captions.ass",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-2:LRA=11,alimiter=limit=0.70:level=disabled",
         "-shortest", "-movflags", "+faststart", f"{d}/final/short.mp4"])
    total = sum(line_lens)
    print(f"Built {d}/final/short.mp4  (~{total:.1f} s, {len(ids)} lines)")


if __name__ == "__main__":
    main()
