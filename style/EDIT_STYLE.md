# Edit style for Shorts (owner's preferences + kamal-video-style, adapted for automation)

## Look
- 9:16, 1080x1920, 30 fps. Bright, fast, Vox-style edit.
- **Real photos and footage first.** An edit made only of motion graphics felt "dry" and was rejected.
- Documentary collage, cutout or sticker-style images, maps, and 2D motion text on top of real images.
- **Scene variety.** Never repeat the same visual many times (the Doomsday clock shown 7 or 8 times was rejected).
  Use a different image or angle on every line where possible. Reuse an image at most twice.
- Colour: **bright, cool and natural.** Dark or muddy looks were rejected. Pick bright, clear images;
  use dark text cards only for short number beats.
- If exact footage doesn't exist, build a visual from related images, maps and text. Never leave a gap.

## Pace and motion
- One shot per spoken line, so the picture changes every 2 to 4 seconds.
- First 2 seconds: the strongest image plus a short overlay headline (different words from the spoken hook).
- Slow zoom in on reveals, pan across maps and documents, zoom out to show scale.

## Captions
- **Roman Hinglish**, pop style, big bold white, 3 words at a time.
- Keywords and numbers highlighted in accent yellow (F5C518).
- Placed **a little below centre** (CAPTION_MARGIN_V 720).

## Audio
- Voiceover at **1.10x** (ELEVENLABS_SPEED 1.1).
- BGM and SFX must be **clearly audible** under the voice (MUSIC_VOL 0.16). Royalty-free only.

## Never
- No AI faces of real public figures. No logos, no news clips, no watermarked images.
- No fake documents shown as real. Only copyright-safe material (no strikes or Content ID claims).

## Assembler settings (environment variables)
CAPTION_FONT, CAPTION_SIZE, CAPTION_WORDS, CAPTION_MARGIN_V, ACCENT, BG, MUSIC_VOL, ELEVENLABS_SPEED.

Not yet automated (for later): speed ramps, 3D motion graphics, cutout stickers with shadow, SFX
cue placement. Claude can add these to `scripts/assemble_short.py` once the basic pipeline works.

## Owner's edit rules (23 Nov 2026, GTA 6 Short)
- New visual every 2-3 seconds; 2-3 visuals per spoken line (SHOTS.tsv source "video:a.mp4@1|sticker:b.jpg").
- Shot types: `video` (push-in), `image` (Ken Burns), `sticker` (cutout: white border, shadow, tilt, blurred bg), `doc` (real source, highlighted), `card` (number/word).
- Transitions on every cut (assembler TRANS=0.3, TRANS_CYCLE); `fadewhite` on "asli jhatka", `circleopen` at the end.
- Sound: whoosh on every cut (assets/sfx/whoosh*.mp3), impact (hit*.mp3) on the 2-3 biggest reveals (SHOTS sfx=hit), BGM in assets/music ducked under voice.
- Visual sources in order: official media kits/newsrooms, free stock clips (Mixkit/Pexels/Pixabay), owner's Flow, document screenshots. Credits in the description.

## Pro edit upgrade (23 Nov 2026, owner said v3 was weak)
- Hook (0-3 s): 3-4 cuts of ~0.8 s, a big pop title (overlay "big:LINE1/LINE2", stays over all hook cuts), flash + shake, boom SFX. Must work on mute.
- Visuals must show literally what the line says (controller for "game", audience for "cinema", wallet for "jeb", calendar for a date, calculator for "kamai"). Video clips first; stills only when no clip exists.
- Every shot enters with an effect (SHOTS `fx`: punch default, zoomout, flash, shake). Big reveals: flash+shake.
- Captions pop in (scale 72% -> 108% -> 100%).
- Sound design: energetic BGM started at its full-energy part (MUSIC_START), MUSIC_VOL 0.22 with gentle ducking; riser into reveals, hit/boom on reveals, cash on money lines, camera click on documents, pop on titles, glitch on questions, whoosh on cuts.
- (23 Nov, v5) Owner approved using official trailer footage MUTED (Content ID risk accepted by owner). Cut vertical 1080x1920 crops straight from the 4K official file (remove letterbox: cropdetect), 2.6 s each, no audio. Skip shots with weapons. Credit in description.
- New fx: glitch (RGB split + noise, first 0.2 s), blurin; global grade eq contrast 1.06 / saturation 1.15 + vignette + light grain (GRADE env).
- Hook first frame must be bright and clear behind the big title (not a logo, not a dark shot).
- (23 Nov, v6 "strong" mix) Music: energetic track from its drop (MUSIC_START), MUSIC_VOL 0.1 + bass +5 dB, gentle ducking (ratio 3): music sits ~6 dB under the voice, never over it. Music DROP (SHOTS sfx "drop") 0.7 s before the big twist, riser over the silence, cinematic hit on the cut.
- SFX_VOL 0.4: whoosh every cut, sub-bass under every number reveal, cine hit on twist/end, cash on money, pop on titles, camera on documents. Final: loudnorm -14 LUFS + limiter (peak below -1 dBFS).
- Visuals: clips play at 1.25x (FAST_CLIPS), light leaks / lens flares (fx "leak", Mixkit) on hook, reveals and ending; never a leak on the very first frame.
- (23 Nov, v7) Owner: "voice sun hi nahi raha". Voice is ALWAYS the loudest: voice chain (highpass 85, compressor, +4 dB at 3 kHz, loudnorm -16), music EQ carved -8 dB at 2 kHz and -3 dB at 500 Hz, sidechain ratio 6. Check before delivery: voice at least 10 dB above music+SFX during speech (min 6 dB on a hit). Hits/subs on a line start are short (0.8 s) and soft.
- (23 Nov, v8) Cinematic grade by default: colorbalance teal shadows / warm highlights, curves medium_contrast, saturation 1.22, light sharpen, vignette, grain.
- Card cutout (fx "card"): the clip inside a white-bordered, tilted card that scales in, over a blurred darker copy. Use on ~1 in 4 shots, alternate with full-screen shots.
- Never show console/platform logos or "Out Now" promo text from trailers (PS5/Xbox); check every trailer clip frame.
- Real subject cutouts (background removal) need the rembg package; not installed yet.
- (23 Nov, v9) Real cutouts: `rembg` (model isnet-general-use) removes the background from a still; make an outlined PNG (white stroke + shadow) and use SHOTS `cutout:fg.png~bg.mp4@start` (subject pops in over a blurred moving background, placed above the captions). Use 2-3 per Short on character/object lines.
- Tools installed by setup.sh: rembg, librosa (beats), faster-whisper (word timing), hyperframes (HTML -> MP4 motion graphics).
- (23 Nov, final) Colour: owner's library LUT `DAEDAL_02_Product_Pop.cube` (06_LUTs/Clean_Tech_Rec709) via GRADE env + light sharpen/vignette/grain. Captions CAPTION_MARGIN_V=560 (a little below centre). Owner library has LUTs, overlays (film damage, smoke, light leaks), b-roll and fonts in `library/video library/`; music/sfx lists in `library/audio library/` (download Mixkit tracks from their LICENSE_RECORD.tsv URLs).
