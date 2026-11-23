# Graphics, text and captions

## Safe zones
**9:16 (1080×1920), all platforms (HyperFrames `outside_safe_zone` check):** text and key content between
**y 288–1248** and **x 120–888** (narrows to 780 px wide below y 840 where TikTok's rail widens).
Outside: texture/decoration only. Single-platform check: `--safe-zone tiktok|reels|shorts`.
Ads and some apps reserve more at the bottom — leave 50–100 px extra margin.
**16:9:** content in the 90% action-safe box, captions/key text in the 80% title-safe box.

## Captions (tested: `scripts/make_captions.py`)
```bash
python3 scripts/make_captions.py --cues cues.json --out compositions/captions.html --portrait
```
- Groups: 2–3 words (high energy), 3–5 (conversational), 4–6 (calm); break at sentence ends or ≥150 ms pauses.
- One group visible at a time; first caption 0.1–0.3 s in (never at 0); every group hard-hidden at its end.
- Portrait: caption **bottom edge at y = 1248**, inside x 120–888. Landscape: 80–120 px from bottom.
- Size: base ~66–78 px portrait, min 42; nothing meant to be read under 28 px (2.6% of short side).
- Fade the group or its words, not both. Full-width centred container; never `left:50%;translateX(-50%)`.
- Readability over footage: stroke 8–10 px black + soft shadow, or a scrim sized to the text (30–40%), never a full-width bar.
- Timing floor (Netflix): ≥ 0.83 s on screen, ≤ 7 s, ≥ 2-frame gap; Hindi reading speed ≤ 22 chars/s (adult).
- Active-word highlight in ONE accent colour (channel: #FFD400).
- Don't caption a line that is already the big on-screen title (redundant text is a tell).

## Devanagari / Hinglish type (tested)
- Use a real Devanagari face via `@font-face` (`assets/fonts/noto-sans-devanagari-*-800-normal.woff2`
  from `npm pack @fontsource/noto-sans-devanagari`). Bundled HyperFrames fonts are Latin-only.
- `line-height` 1.35–1.45 so upper matras (ि ी ें) and lower marks never clip; `overflow: visible`.
- Never split a word across spans by character (breaks conjuncts like न्न, र्म); highlight whole words.
- Count length by visible base characters (combining marks don't add width) — the scripts do.
- Mixed Roman + Devanagari: pair by weight; numbers in Latin digits on screen are fine, but in the VO write numbers as words.
- Verify in a snapshot: matras, nuqta (ज़), and reph (र्) must render correctly.

## Titles and kinetic type
- Title 4–9% of frame height; hero word may fill 60–90% of width; one highlighted word with meaning.
- Entrances (vary within a film): per word blur 6 px→0 + opacity in 0.13 s, 0.067 s apart; whole line 8 px→0 in 0.13–0.2 s; per letter 0.1 s apart for a name.
- Landed title is dead still. Hold 0.5 s + 0.3 s per word (last line ≥ 2 s). Exit = blur-out + fade 0.13–0.25 s.
- Avoid: everything fading+sliding up, breathing/pulsing loops, slow creep after landing.

## Lower thirds
Name (bold) + role/source (60–70% size), accent bar grows first (`scaleY` 0.3 s expo.out), text 0.1 s later; on screen ≥ 3–5 s; inside safe zone; never over the mouth/face; once per person.

## Source chips (documentary)
"PHOTO: NASA · PD", "SOURCE: The Washington Post, 21 July 1969": 30 px+, semi-opaque dark chip, upper safe area or ≥ 60 px above the caption band, on screen while the asset is visible.

## Thumbnails (YouTube)
1280×720 (min width 640), 16:9, JPG/PNG < 2 MB. One subject, 3–5 big words, high contrast; must match the first 30 s (YouTube's intro metric compares them). Vertical Shorts with 16:9 custom thumbnails get an auto 4:5 frame on some surfaces, so frame 0 must work as a thumbnail too.

## Brand motion tokens (define once)
Accent `#FFD400`; text white with black stroke; fonts: Noto Sans Devanagari 800 + Inter/Oswald; enter `expo.out`/`power3.out`, exit `power2.in` (40–50% shorter than entrance); stagger words 60–120 ms; transition vocabulary 3–5 kinds per film.
