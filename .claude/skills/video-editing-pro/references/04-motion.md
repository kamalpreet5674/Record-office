# Motion: easing, Ken Burns, parallax, blur, speed

## Ease by role (measured on official HyperFrames films + Material 3)
| Role | GSAP | CSS cubic-bezier |
|---|---|---|
| Arrival (lands on a long tail) | `expo.out`, `power4.out`, `power3.out` | Material emphasized decelerate `(0.05,0.7,0.1,1)` |
| Camera move / colour flood (both ways) | `power2.inOut` | Material standard `(0.2,0,0,1)` |
| Exit / zoom-through (accelerates) | `power3.in`, `power2.in` | emphasized accelerate `(0.3,0,0.8,0.15)` |
| Slow drift / Ken Burns | `sine.inOut` or `none` | `linear` for constant drift |
| Overshoot (position/size only) | `back.out(1.4–1.7)`, `elastic.out(1,0.5)` | — |
| Linear only for | rotation, progress, constant speed | — |

- Fast move 0.3–0.6 s, one tween per move. Exits 40–50% shorter than entrances. Overlap: next element starts when the previous is 30–50% done.
- Stagger: letters 1 frame, words 60–120 ms, list items 40–80 ms.
- Springs: damping 0.7–0.85 premium, 0.4–0.6 playful; opacity/colour never bounce.
- Anticipation (2–5% opposite move) and follow-through (secondary elements land 2–6 frames later) for character/organic motion only; UI and titles land clean.
- Same `power2.out` 0.5 s on everything = "generated" look. Vary.
- Feedback: "too fast" → slow zooms/pans to 0.7×; "titles move" → land them and hold dead still; "feels like slides" → enter through an object on screen.

## Ken Burns / push-in (tested in `templates/scene-photo-kenburns.html`)
- Tween `scale` + `x/y` on a wrapper inside the clip. 1.05→1.15 over 3–8 s (Shorts 2–4 s), `sine.inOut`.
- Push-in = tension/focus/reveal; pull-out = context/conclusion. Pan toward what the VO names; alternate direction between consecutive photos.
- Source ≥ end-scale size (1080 × 1.3 ≈ 1400 px short side, prefer 1600–2000).
- Never crop through eyes; end with eyes on the upper third.
- Document push (tested): establish 1 s at scale 1.0–1.02, push to ~1.9 over 1.2 s `power2.inOut` with `transform-origin` on the key line.

## Parallax (tested in `templates/scene-iris-parallax.html`)
Background travels 20–40% of the foreground; subject scale 0.96→1.06; total travel 40–120 px over 4–6 s; cut-out subjects get 1–2 px edge softness + shadow. For photo cut-outs: `npx hyperframes remove-background`.

## Motion blur
- Camera rule: 180° shutter ≈ 1/(2×fps) (24→1/48–1/50, 25→1/50, 30→1/60, 60→1/120). A default, not a law.
- Graphics: fast moves get blur on their own ease, peaking at the fastest frame: 6–12 px text-sized, 15–20 px full-frame, horizontal-only on horizontal moves.
- HyperFrames: `data-motion-blur="on"` on the root smears real paths (tested: it forces screenshot capture → slower render). `data-motion-blur-shutter` for longer smear; opt out a subtree with `data-motion-blur="off"`.

## Speed
| Slow-mo at 24/30 fps playback | Min source fps |
|---|---|
| 50% | 48/60 |
| 25% | 96–120 |
| 20% (5×) | ~120 |
| 10% | 240 |
- Ramp in → hold → ramp out; ramps 4–12 frames on a bezier; slowest point on the musical hit.
- Too few frames → optical flow, then check edges/hands for warping.
- HyperFrames: constant `data-playback-rate`; ramps via a `rate` lane in `data-automation` (t in clip seconds, v 0.1–10).

## Rhythm
Montage cuts 0.13–0.8 s; shots average 1.8–3 s with motion inside; demo holds 7–10 s; hold 0.3–0.75 s before the payoff, payoff at normal speed. Shorts: new beat every 2–4 s.
