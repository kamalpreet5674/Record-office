# Transitions and effects

## Rules
- 3–5 transition kinds per film, each **caused** by something on screen. Hard cuts inside scenes (punch-ins); at most a third of beat seams are plain hard cuts; worlds never crossfade into each other.
- Max one showy transition per 10–15 s (music videos excepted). Never stack glitch + flash + zoom + shake.
- Cut at the fastest frame of a move, matching direction and speed both sides; mirror eases (`power3.in` out, `power3.out` in).
- Always `snapshot` −0.1 / 0 / +0.1 s around every seam: a jump or gap there is the most common bug.
- Scenes overlap their neighbours by ~0.4 s (host `data-start`) so both sides exist during the transition.

## Cut types
| Cut | Use | Avoid |
|---|---|---|
| Hard cut | default | — |
| Jump cut | talking-head time compression; change size ≥ 10–20% (punch 110–120%) | micro framing shifts |
| J-cut (audio leads) | entering scenes, anticipation | when it confuses who speaks |
| L-cut (audio lingers) | reactions, narration into montage | fast comedy timing |
| Match cut | link by shape/motion/sound at the same screen position | elements that don't align |
| Smash cut | sudden contrast | overuse |
| Cutaway/insert | proof, detail, hide a cut | inserts that add nothing |
| Cross dissolve | time passing, memory | between two takes of one speaker |
| Dip cut | outgoing darkens ~40% for 3 frames, then hard cut | — |

## Recipes (durations at 30 fps; tested ones marked ✓)
| Transition | Build |
|---|---|
| ✓ Whip / push | outgoing wrapper x 0→−W and incoming x +W→0, **same** start, 0.3 s, `power3.inOut` (different eases/timings leave a black gap); whoosh peak at the seam; motion blur on |
| Whip smear (official) | 0.13–0.3 s horizontal smear; arriving element lands blurred and sharpens in ~0.13 s |
| ✓ White flash (official recipe) | rise 0.035–0.055 s (1–2 frames), recovery 0.24–0.38 s (7–11 frames), warm white `#fff8ec`, one flash event, never saturated red; impact SFX 1 frame after the peak |
| ✓ Dip cut | black overlay opacity 0→0.4 over the last 3 frames, then hard cut |
| ✓ Iris | `clip-path: circle(0%→80% at x y)` 0.15–0.5 s `power3.out`, from the point of interest |
| ✓ Gradient (luma-style) wipe | `mask-image: linear-gradient(90deg,#000 var(--p),transparent calc(var(--p)+18%))`, tween `--p` −18%→100% in 0.7 s `power2.inOut` |
| ✓ Glitch (deterministic) | 3–5 frames: red/cyan copies `mix-blend-mode:screen` offset ±6–18 px from a fixed array + `clip-path: inset()` slices; then reset; tech/"error" topics only |
| Zoom through | camera tracks to the object with blur (0.6 s), object scales ~8%→250% in 0.35 s strong ease-in; its fill becomes the next frame |
| Object becomes the world | card grows past frame 0.65 s inOut, surroundings blur ~15 px and fade 0.3 s |
| Colour flood | hero stays, ground changes colour in ~0.4 s `power2.inOut` |
| Blur swap | out: opacity→0 + 8 px blur 0.13–0.2 s; in: blur→0 0.13 s |
| Light leak | screen-blended warm gradient 10–30 frames; or registry `organic-light-leak-overlay` / `light-leak` |
| Cross dissolve | 10–30 frames (time-pass up to 60) |
| Shader transitions | registry (`cinematic-zoom`, `sdf-iris`, `whip-pan`, `glitch`…): ≤ 2 per film; installed file is a showcase to learn the HyperShader usage, not a drop-in |

## Flash safety (hard rule)
No more than 3 flashes in any 1-second period (WCAG 2.3.1/2.3.2); avoid saturated red flashes; no full-screen strobes. `scripts/qc_check.py` counts full-frame flashes in the render.

## Effects order
transform → motion blur → colour (media-treatment) → stylization (grain/glow) → overlays. If the viewer notices the effect more than the story, delete it.
