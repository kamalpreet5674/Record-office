# Color: correction, grading, scopes, LUTs, shot matching

## Order of work
1. Input transform (log → Rec.709) **once** — never double-convert (app color management + LUT = twice).
2. Exposure/levels → 3. white balance (neutrals align on RGB parade) → 4. contrast (protect skin mids) →
5. saturation (skin on vectorscope) → 6. shot matching → 7. secondaries → 8. look → 9. output Rec.709/BT.709 + legal check.
Correction makes it right, grading makes it feel. Don't add a style when correction solves the complaint.

## Scopes
| Scope | Use | Targets |
|---|---|---|
| Waveform 0–100 IRE | exposure, clipping | blacks ~0–5, whites ≤ 100, no flat line on top |
| RGB parade | white balance | neutrals line up across R/G/B |
| Vectorscope | hue + saturation, skin | neutral trace centred; skin on the skin-tone line (~11 o'clock, between R and Y) for every ethnicity |
| Histogram | quick overview | no pile-up at walls unless intended |

Skin IRE: darker ~45–60, medium ~55–65, lighter ~65–75. Grass ~40–50. Speculars 90–100.

## HyperFrames grading (official path, tested)

Grades, grain, vignette, blur go through `media-treatment`, which writes `data-color-grading` on the real `<img>/<video>`:
```bash
npx hyperframes media-treatment --project . --file compositions/s2.html --selector '#s2-video' --analyze --json
npx hyperframes media-treatment --project . --file compositions/s2.html --selector '#s2-video' \
  --grading '{"preset":"skin-soft","intensity":0.6,"adjust":{"highlights":-0.08,"shadows":0.08},"details":{"vignette":0.04,"grain":0.06}}' --apply --json
npx hyperframes media-treatment --capabilities --json      # families; then --capability <id> for legal ranges
```
Presets: neutral, skin-soft, warm-daylight, clean-studio, bright-pop, soft-boost, deep-contrast, muted-editorial,
night-lift, vintage-wash, mono-clean, mono-fade, food-pop, creator-camcorder, home-movie-8mm, vhs-playback, editorial-halftone, two-ink-print.

| Intent / source | Recipe seed |
|---|---|
| People, interview, archive portrait | Natural Portrait: `skin-soft` 0.45–0.75, exposure −0.06…0.14, highlights −0.18…−0.04, shadows 0.04…0.18, grain 0 |
| Product/lifestyle | Product Polish (protect label colours) |
| Screen capture / UI | UI Fidelity: leave pixels alone |
| Warm memory / history flashback | Film Memory: `vintage-wash` 0.5–0.75, vignette 0.08–0.16, grain 0.08–0.16 |
| Space/dramatic stills | `deep-contrast` ~0.5 |
| Old home video | 8mm / VHS recipes (only when the story asks) |

- Animatable (seek-safe) properties: `--hf-color-grading-intensity` (0–1), `-exposure` (−2…2), `-blur`, `-bloom`, `-lut-intensity`… set the first value inline, then finite `tl.to()`.
- LUTs: `npx hyperframes media-use resolve --type grade --intent "teal orange blockbuster" --project . --json` → frozen `.cube` with intensity. Never read a `.cube` into context; compare with `grade-compare`.
- Realtime path is Rec.709/SDR: do not push LOG/HDR through it silently.
- Whole-media only: to treat one face/region, make a separate cropped/masked layer.
- Before/after: `snapshot --frames 3` sheets; keep the source if the result isn't clearly better.

## Creative looks (for other tools / reference)
| Look | Shadows | Mids/skin | Highlights | Sat/contrast |
|---|---|---|---|---|
| Teal & orange | teal | warm skin | warm | sat +5–15%, contrast med-high (watch darker skin) |
| Bleach bypass | neutral/cool | desaturated | harsh | sat −40–60%, high contrast, grain |
| Cinematic desaturated | lifted 5–8 IRE, cool | muted | soft roll-off | sat −20–30% |
| Warm nostalgic | amber, lifted | warm | creamy | sat −10%, low contrast, grain |
| Cool thriller | blue-green | believable skin | cold | sat −15%, crushed blacks |
| **Channel default: bright natural** | clean | true skin | clean, bright | sat 0…+10%, medium contrast |

## LUTs (any NLE)
Technical LUT (camera log → Rec.709, exact curve/gamut) then creative LUT at 20–60% intensity on its own node/layer.
Correct before the LUT; max one technical + one creative LUT per shot.

## Shot matching
Hero shot per scene first → match blacks, whites, skin hue/sat, balance → compare split-screen at the cut →
grade the scene group for the look, per-shot only for corrections → recheck after titles.
Archive mixes (B&W newspapers + colour NASA photos): don't force colour onto B&W; unify with consistent contrast, a shared grain level and the same text/graphic palette.

## Outside HyperFrames: CSS/SVG/WebGL
CSS filters (`contrast() saturate()`) only for non-footage graphics. SVG `feColorMatrix` with `color-interpolation-filters="sRGB"`; Safari ignores SVG `url()` filters on `<video>`. WebGL 3D-LUT shader: sample a 3D texture with texel-centre correction `c*((N-1)/N)+0.5/N`, mix by intensity; drive from timeline time, not rAF.
