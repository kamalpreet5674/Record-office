# HyperFrames (HTML → video): the contract and tested patterns

HyperFrames (HeyGen, open source) seeks a paused GSAP timeline frame by frame in headless Chrome and encodes
with FFmpeg, so every render is identical. Tested with CLI 0.9.86. Run `npx hyperframes docs <topic>`
(data-attributes, gsap, compositions, rendering, audio, transcribe, motion-blur, troubleshooting).
If the official `hyperframes` skills are installed, they win on any conflict with this file.

## The contract (break one → broken render)

1. Every timed element: `class="clip"` + `data-start` + `data-duration` (seconds). Shows over `[start, start+duration)`;
   land end states just before the end. `data-track-index` is only a Studio lane; paint order is `z-index`.
2. Video length = root `data-duration` (write it in markup; scripts can't change it).
3. One **paused** timeline per composition, registered last: `window.__timelines["<data-composition-id>"] = tl`.
4. No `Date.now()`, unseeded `Math.random()`, network fetches, timers, `requestAnimationFrame` or `repeat:-1`.
   Everything visible is a function of timeline time. "Random" glitches use fixed arrays.
5. Never tween `display/visibility/autoAlpha` on a `.clip`; animate a child (an instant `tl.set` of
   `visibility` on a non-clip child is fine).
6. No CSS `transform` on an element GSAP transforms (start state goes in `fromTo`).
7. Never `play()/pause()`/seek media. `<video>` with sound: `data-has-audio="true"`; else `muted`.
   Music, VO, SFX, J/L cuts: separate `<audio id=…>` (no id = not mixed). No `crossorigin`.
8. **Time the `<video>`, never its wrapper.** Animate an untimed wrapper around it (Ken Burns, whip, punch-in).
9. Fonts: bundled (Inter, Montserrat, Oswald, Poppins, Roboto, Noto Sans JP…) resolve by name;
   anything else (e.g. Noto Sans Devanagari) needs `@font-face` to `assets/fonts/*.woff2` in the file that uses it.
10. Asset paths `assets/...` (no leading `/`), also inside scene files.
11. Grades/grain/blur/vignette on footage: `npx hyperframes media-treatment` (see `06-color.md`), not CSS filters.
12. Scene files: everything inside `<template>`, root styled as `#root`, `fromTo` not `from`.
    Host id = scene `data-composition-id` = timeline key (mismatch → 45 s wait per scene + static frames).

## Project shape (tested: `templates/index-example.html`)

```html
<div id="root" data-composition-id="main" data-start="0" data-duration="24"
     data-width="1080" data-height="1920" data-motion-blur="on">
  <div id="s1" data-composition-id="s1" data-composition-src="compositions/s1.html"
       data-start="0" data-duration="4.2" data-track-index="0" data-track-kind="graphics"
       data-width="1080" data-height="1920" style="z-index:1"></div>
  <!-- next scene overlaps the previous by 0.4 s so transitions have both sides -->
  <div id="s2" … data-start="3.8" data-duration="4.2" … style="z-index:2"></div>
  <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html"
       data-start="0" data-duration="24" data-track-kind="captions" … style="z-index:20"></div>
  <audio id="vo"  data-start="0" data-duration="24" data-volume="1" data-fx-chain="…" src="assets/audio/vo.wav"></audio>
  <audio id="bgm" data-timeline-role="music" data-start="0" data-duration="24" data-volume="1"
         data-fade-in="0.3" data-fade-out="1.2" data-automation="…duck lane…" src="assets/audio/bgm.wav"></audio>
  <audio id="sfx-whoosh1" data-start="3.65" data-duration="0.6" data-volume="0.8" src="assets/audio/whoosh.wav"></audio>
</div>
```

Scene file:
```html
<template>
<style>#root{position:absolute;inset:0;overflow:hidden;}</style>
<div id="root" data-composition-id="s1" data-width="1080" data-height="1920">
  <div id="s1-shot" class="clip" data-start="0" data-duration="4.2">
    <div id="s1-exit" class="fill"><div id="s1-kb" class="fill"><img src="assets/raw/photo.jpg"></div></div>
  </div>
</div>
<script>
  const tl = gsap.timeline({ paused: true });
  tl.fromTo("#s1-kb", {scale:1.06, x:0}, {scale:1.16, x:-24, duration:4.2, ease:"sine.inOut"}, 0);
  window.__timelines["s1"] = tl;
</script>
</template>
```

## Mechanisms (use these, not hacks)

| Need | Mechanism |
|---|---|
| Ken Burns / punch-in / reframe | `scale`, `x`, `y` on a wrapper *inside* the clip (never on the timed media) |
| Crop / mask / iris | `clip-path` or `mask-image` on an inner wrapper |
| Constant speed | `data-playback-rate` 0.1–10 on the media |
| Speed ramp | `rate` lane in `data-automation` on the media |
| Motion blur | `data-motion-blur="on"` on the root (smears fast 2D movers; forces screenshot capture, slower render) |
| Music ducking | `volume` lane in `data-automation` (`scripts/duck_lane.py`) |
| VO cleanup | `data-fx-chain` (highpass, peaking, compressor, limiter …) |
| Grade/grain/vignette | `data-color-grading` via `media-treatment` |
| Freeze mid-clip | Export a still and place it as its own clip |
| Variables / reuse | `data-composition-variables` + `data-var-text`, `data-variable-values` per host |

## Lessons from the test render (real bugs → rules)

| Found by | Problem | Rule |
|---|---|---|
| `check` duplicate_audio_track | SFX without `data-duration` ran to the end of the film | Always give SFX `data-duration` = file length |
| `check` audio_clip_silent | Generated whoosh was -50 dB | Normalise every SFX to about -3 dBFS peak before use |
| `check` outside_safe_zone | Credit at y 1430 in 9:16 | All text between y 288–1248, x 120–888 |
| `snapshot` at seam | Black gap mid-whip | Push transitions: outgoing −W and incoming +W→0 with the **same** duration/ease/start |
| `qc_check.py` blackdetect | 0.13 s of black mid-whip: the incoming scene's root had `background:#000` and sat above the outgoing scene | A scene that overlaps the previous one has a **transparent** `#root`; only its media/wrapper is opaque |
| `qc_check.py` loudness | HyperFrames mix measured −16 LUFS | Finish with `scripts/publish_loudness.py` (two-pass loudnorm to −14 for social) |
| `snapshot` | Credit chip collided with captions | Keep chips ≥ 60 px above the caption band (captions occupy ~1150–1248) |
| `snapshot` | On-screen hero text = caption text | Don't caption a line that is already the big on-screen text (or style it differently) |

## Commands

```bash
npx hyperframes init my-video --non-interactive --resolution=portrait
npx hyperframes check --json          # lint + runtime + layout + motion + contrast + audio; fix every error
npx hyperframes snapshot --at 0.9,3.9,4.1 --output snapshots/v1   # + contact-sheet.jpg; look at every cut ±0.1 s
npx hyperframes snapshot --review     # scene/beat/seam/phone-width sheets
npx hyperframes timeline --json       # what plays when
npx hyperframes beats music.mp3 --json   # bpm + beatTimes
npx hyperframes transcribe vo.wav --model small --language hi --json   # word timings (non-English: never *.en models)
npx hyperframes render --quality draft --output renders/draft.mp4
npx hyperframes render --quality standard --output renders/final.mp4   # --fps 60 doubles render time
npx hyperframes audio renders/final.mp4 --json    # sound present, hit times, loudness
```
Registry: `npx hyperframes catalog --tag transition --json` (shader transitions: max 2 per film; the
installed file is a showcase to learn from, not a drop-in), `--tag caption-style`, `--tag camera`.

## Performance

- Resize images to ≤ 1.5× on-screen size; avoid stacked full-frame `backdrop-filter`/blur.
- More than two full-frame multipass treatments (blur, bloom, kuwahara) at once → check playback, pre-render if needed.
- Draft render + snapshots while iterating; `--workers auto` (each worker ≈ 256 MB Chrome).
- Long films: one scene per sub-composition; render ranges or scenes when debugging.
