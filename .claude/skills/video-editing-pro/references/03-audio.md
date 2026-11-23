# Audio: dialogue, music, SFX, loudness, sync

Sound is half of how a film feels. A film over ~15 s that tells something gets a music bed and sounds on its visible actions (unless asked for silence).

## Loudness targets (integrated, BS.1770 / EBU R128 metering)

| Destination | Integrated | True peak |
|---|---|---|
| YouTube / Shorts / Reels / TikTok (default) | **-14 LUFS** (range -16 to -14 for speech-led) | ≤ -1 dBTP (-1.5 safer) |
| Apple Music style | -16 LUFS | -1 dBTP |
| Podcast/dialogue-only online | -16 LUFS | -1 dBTP |
| EBU R128 broadcast (EU) | -23 LUFS | -1 dBTP |
| ATSC A/85 (US broadcast) | -24 LKFS | -2 dBTP |
| Netflix | -27 LKFS dialog-gated | -2 dBTP |

Loud uploads are turned down, not up: never squash for loudness. Measure the rendered file with `scripts/qc_check.py`.

## Voice-over / dialogue chain (in order)

1. Noise reduction (light; over-NR sounds underwater) → 2. high-pass 80–100 Hz (to 120 for thin voices) →
3. mud cut 200–300 Hz −2…−4 dB → 4. presence +2…+2.5 dB at ~3 kHz → 5. de-ess 5–8 kHz, 3–6 dB →
6. compressor 2:1–4:1, attack 5–20 ms, release 50–150 ms, 3–6 dB GR → 7. limiter −1 dBTP.
Fix EQ before compression (compression amplifies what's wrong).

**HyperFrames (tested):** `data-fx-chain` on the VO `<audio>` (JSON, quotes as `&quot;`):
```json
{"version":1,"nodes":[
 {"type":"highpass","id":"hp","label":"Remove rumble","params":{"frequency":90}},
 {"type":"peaking","id":"mud","params":{"frequency":300,"gain":-3,"q":1}},
 {"type":"peaking","id":"pres","label":"Clarity","params":{"frequency":3000,"gain":2.5,"q":1}},
 {"type":"compressor","id":"comp","params":{"threshold":-20,"ratio":3,"attack":0.01,"release":0.12}},
 {"type":"limiter","id":"lim","params":{"limit":-1}}]}
```
| Sounds like | Reach for |
|---|---|
| Hum, rumble | highpass 80 Hz |
| Boomy / too close | peaking 200 Hz −4 dB |
| Muffled | peaking 250 Hz −3 dB |
| Hard to understand | peaking 3 kHz +2.5 dB, or duck the music more |
| Harsh | peaking 3.2 kHz −3 dB |
| Clipping | limiter last |

**ffmpeg (outside HyperFrames):**
```bash
ffmpeg -i vo.wav -af "highpass=f=90,afftdn=nf=-25,equalizer=f=300:t=q:w=1.2:g=-3,\
equalizer=f=3000:t=q:w=1:g=2.5,deesser=i=0.4,acompressor=threshold=-20dB:ratio=3:attack=10:release=120:makeup=3,\
loudnorm=I=-16:TP=-1.5:LRA=7" vo_clean.wav
ffmpeg -i vo_clean.wav -filter:a "atempo=1.10" vo_fast.wav     # channel default: VO 1.10x, pitch kept
```
ElevenLabs: numbers as words; emotion `[tags]` only on v3 models, `<break>` on v2; one pause system only (tags or TSV gaps, not both).

## Timing from the voice (tested)

```bash
python3 scripts/build_cues.py --vo assets/audio/vo.wav --lines LINES.tsv --out cues.json --bpm 96
```
silencedetect (−35 dB, ≥ 0.28 s) → one speech span per script line (auto merge/split, warns when it had to)
→ words timed by visible characters (Devanagari matras don't count) → frame-quantised.
Real speech sits around −16 to −26 dB; Whisper can invent "Thank you" over silence. Use `npx hyperframes transcribe --model small --language hi` when you need true word timings (never `*.en` models for Hindi: they translate).

## Music

- Pick by **feel and tempo**, not subject: "tense minimal pulse building to a bright drop, 120 bpm".
- Enter at the track's strongest bar, end on a bar line with a short fade under the end card.
- No vocals under VO. Edit music on bar lines, hide edits under a hit.
- Frames per beat = fps × 60 / BPM. Compute each beat from its index (`round(i × 60/BPM × fps)`),
  never add a rounded beat repeatedly (128 BPM @30 fps drifts 2 frames in 32 beats).
- Cut on the beat; change layout on the bar; payoff on a strong beat; hold 0.3–0.75 s before the payoff.

| Mood | BPM |
|---|---|
| Calm, documentary | 60–90 |
| Explainer, vlog | 90–115 |
| Upbeat product/travel | 115–130 |
| Hype/trailer build | 130–160+ |

## Ducking (tested)

```bash
python3 scripts/duck_lane.py --cues cues.json --music-len 24 --duck 0.3 --bridge 0.3 --html
```
Paste into the music `<audio data-volume="1" data-automation="…">`. 0.3 ≈ −10 dB under speech, 1.0 in gaps.
`--bridge` keeps the bed down across short pauses (0.3 s = breathing music, 0.9 s = steady).
Without a lane, a static bed ≈ `data-volume="0.14"` under a voice. Don't combine a lane with GSAP volume tweens.
Typical ranges: duck 6–12 dB (subtle) to 12–18 dB (VO-heavy); attack 30–80 ms; release 250–700 ms.

ffmpeg alternative (sidechain):
```bash
ffmpeg -i vo.wav -i bgm.wav -filter_complex "[0:a]asplit=2[vo][sc];[1:a]volume=-6dB[b];\
[b][sc]sidechaincompress=threshold=0.04:ratio=6:attack=30:release=400[d];\
[vo][d]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[o]" -map "[o]" mix.wav
```

## SFX (few and exact: every sound has a cause on screen)

| Sound | Only on | Placement |
|---|---|---|
| Whoosh | scene cut, big card moving fast | peak at the cut (start = cut − file's peak time) |
| Impact/boom | reveal, title slam, the payoff | peak 1 frame **after** the picture hit |
| Riser → impact | the payoff, once per film | riser ends on the cut |
| Pop | badge/number landing | on landing frame |
| Soft key tick | text arriving letter/line | per line |
| Click | a real cursor click | on click |
| Paper / camera shutter | document or photo arriving (documentary) | on arrival |
| Ambience/room tone | under every scene, fills gaps | −25…−35 dBFS |

- Hits sit 3–6 dB over the bed; a bed with all its energy under 150 Hz plays as nothing on phones.
- Normalise SFX files to ~−3 dBFS peak; give every SFX `<audio>` an `id` and `data-duration`.
- Rotate 2–3 takes of repeated sounds (same whoosh on every cut is a tell). Pan movement SFX with the motion.
- Duck music, never SFX. Silence before a big hit makes it land.

## Mix hierarchy

Dialogue > Music > SFX > Ambience (SFX may briefly exceed music on key hits).
Dialogue peaks −6…−12 dBFS; music under VO 8–15 dB below; ambience −25…−35 dBFS.
Report in the delivery note: sound was **measured, not heard**.
