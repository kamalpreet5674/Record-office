#!/usr/bin/env python3
"""Generate a HyperFrames captions scene (word-highlight, Devanagari-safe) from cues.json.

  python3 make_captions.py --cues cues.json --out compositions/captions.html \
      [--portrait] [--max-words 4] [--max-chars 18] [--font "Noto Sans Devanagari"] \
      [--font-file assets/fonts/noto-sans-devanagari-devanagari-800-normal.woff2] \
      [--size 66] [--accent "#FFD400"] [--id captions]

Mount it in index.html (one host for every caption group):
  <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html"
       data-start="0" data-duration="<root duration>" data-track-index="5" data-track-kind="captions"
       data-width="1080" data-height="1920"></div>

Rules baked in (HyperFrames captions guide + Netflix timing):
 - groups of <= max-words / max-chars; one group visible at a time; hard hide at group end
 - portrait: bottom edge at y=1248, text inside x 120..888 (all-platform 9:16 safe band)
 - line-height 1.45 so matras above/below the shirorekha never clip
 - min on-screen 0.83 s (extends into the next gap when possible), >= 2-frame gap between groups
"""
import argparse, html, json, os, unicodedata


def vis(s):
    return sum(1 for c in s if not unicodedata.category(c).startswith("M") and not c.isspace())


def groups_from(lines, max_words, max_chars):
    out = []
    for ln in lines:
        cur = []
        for w in ln["words"]:
            if cur and (len(cur) >= max_words or vis(" ".join(x["text"] for x in cur + [w])) > max_chars):
                out.append(cur); cur = []
            cur.append(w)
        if cur:
            out.append(cur)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cues", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--portrait", action="store_true"); ap.add_argument("--max-words", type=int, default=4)
    ap.add_argument("--max-chars", type=int, default=18); ap.add_argument("--font", default="Noto Sans Devanagari")
    ap.add_argument("--font-file", default="assets/fonts/noto-sans-devanagari-devanagari-800-normal.woff2")
    ap.add_argument("--size", type=int, default=66); ap.add_argument("--accent", default="#FFD400")
    ap.add_argument("--id", default="captions"); ap.add_argument("--width", type=int); ap.add_argument("--height", type=int)
    a = ap.parse_args()
    cues = json.load(open(a.cues, encoding="utf-8"))
    fps = cues.get("fps", 30)
    W = a.width or (1080 if a.portrait else 1920); H = a.height or (1920 if a.portrait else 1080)
    gs = groups_from(cues["lines"], a.max_words, a.max_chars)
    gap = 2 / fps
    timed = []
    for i, g in enumerate(gs):
        s = max(0.1, g[0]["start"] - 0.05)
        e = g[-1]["end"] + 0.1
        if e - s < 0.83:
            e = s + 0.83
        nxt = gs[i + 1][0]["start"] - 0.05 if i + 1 < len(gs) else None
        if nxt is not None and e > nxt - gap:
            e = nxt - gap
        timed.append((round(s, 4), round(e, 4), g))
    if a.portrait:
        box = "left:120px;width:768px;bottom:672px;"   # bottom edge at y=1248
    else:
        box = f"left:{int(W*0.1)}px;width:{int(W*0.8)}px;bottom:96px;"
    p = []
    p.append("<template>\n<style>\n")
    p.append(f"@font-face{{font-family:'{a.font}';src:url('{a.font_file}') format('woff2');font-weight:800;font-display:block;}}\n")
    p.append("#root{position:absolute;inset:0;}\n")
    p.append(f".cap-group{{position:absolute;{box}text-align:center;opacity:0;overflow:visible;"
             f"font-family:'{a.font}',sans-serif;font-weight:800;font-size:{a.size}px;line-height:1.45;"
             "color:#fff;paint-order:stroke fill;-webkit-text-stroke:10px rgba(0,0,0,.85);"
             "text-shadow:0 6px 18px rgba(0,0,0,.55);}\n")
    p.append(".cap-w{display:inline-block;padding:0 .12em;}\n</style>\n")
    p.append(f'<div id="root" data-composition-id="{a.id}" data-width="{W}" data-height="{H}">\n')
    for gi, (s, e, g) in enumerate(timed):
        words = "".join(f'<span class="cap-w" id="{a.id}-g{gi}-w{wi}">{html.escape(w["text"])}</span>'
                        for wi, w in enumerate(g))
        p.append(f'  <div class="cap-group" id="{a.id}-g{gi}">{words}</div>\n')
    p.append("</div>\n<script>\n  const tl = gsap.timeline({ paused: true });\n")
    for gi, (s, e, g) in enumerate(timed):
        gid = f"#{a.id}-g{gi}"
        p.append(f'  tl.fromTo("{gid}", {{opacity:0, y:14, filter:"blur(6px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.15, ease:"power3.out"}}, {s});\n')
        for wi, w in enumerate(g):
            wid = f"#{a.id}-g{gi}-w{wi}"
            ws = max(s, w["start"])
            p.append(f'  tl.fromTo("{wid}", {{color:"#ffffff", scale:1}}, {{color:"{a.accent}", scale:1.08, duration:0.08, ease:"power2.out"}}, {ws:.4f});\n')
            p.append(f'  tl.to("{wid}", {{color:"#ffffff", scale:1, duration:0.1, ease:"power1.out"}}, {max(ws + 0.09, w["end"]):.4f});\n')
        p.append(f'  tl.to("{gid}", {{opacity:0, duration:0.12, ease:"power2.in"}}, {e - 0.12:.4f});\n')
        p.append(f'  tl.set("{gid}", {{opacity:0, visibility:"hidden"}}, {e:.4f});\n')
    p.append(f'  window.__timelines["{a.id}"] = tl;\n</script>\n</template>\n')
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write("".join(p))
    print(f"{len(timed)} caption groups -> {a.out}")


if __name__ == "__main__":
    main()
