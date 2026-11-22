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
