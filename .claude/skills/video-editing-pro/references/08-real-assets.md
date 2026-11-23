# Real Assets First: sourcing photos, documents and footage

Realism comes from **evidence on screen**: the actual photo, the actual newspaper page, the actual report,
the actual place. Viewers trust what they can see is real.

## Priority order (use the first that exists)

1. **Primary source itself:** the original photo, document scan, newspaper front page, court/government
   filing, official report PDF page, company filing, archival footage, satellite image.
2. **Official/institutional archives** (usually public domain or free-to-reuse):
   - Library of Congress "Free to Use and Reuse" sets (public domain, no known copyright, or cleared), incl. Chronicling America newspapers.
   - US National Archives (NARA) catalog: federal records are treated as public domain, but some holdings (especially Special Media) may still be copyrighted, and NARA does not confirm copyright status.
   - NASA: content generally not copyrighted in the US; insignia/logos are protected; images showing identifiable people need care for commercial use.
   - Wikimedia Commons (check each file's license), Smithsonian Open Access, Europeana, Flickr Commons, DPLA.
   - India: government sites/press releases (check each site's copyright policy before reuse).
3. **Licensed stock of real places/people/events** (Pexels/Unsplash/Storyblocks/paid agencies), license kept.
4. **Screenshots of real documents/web pages** you are reporting on (show source URL/date on screen).
5. **Maps, charts, diagrams** built from real data (cite the dataset).
6. **3D/AI reconstruction**, only when nothing real exists, labelled "Reconstruction" on screen
   (and the platform AI disclosure ticked when realistic). Never present AI as real evidence.

Target mix for documentary/news Shorts: **≥ 70% real visuals**, ≤ 30% graphics/reconstruction.

## Getting them (tested)

```bash
python3 scripts/fetch_commons.py search "Apollo 11 newspaper front page" --limit 8
python3 scripts/fetch_commons.py get "File:Land on the Moon 7 21 1969-repair.jpg" --out assets/raw --width 2000
```
- Prints `[ok]` / `[RESTRICTED]` per result (NC/ND/fair-use refused unless `--allow-restricted`).
- Writes `assets/raw/CREDITS.json` and `CREDITS.md` (author / license / Wikimedia Commons + page URL)
  ready to paste into the description.
- Respects Wikimedia rate limits (honours `Retry-After`). Request ≤ 1 file every few seconds.
- Download width ≥ 1.5× its largest on-screen size (Ken Burns at 1080 wide → ≥ 1600–2000 px).

## Verify before use (every image)

1. **Reverse image search** (Google Lens, TinEye, Yandex; InVID plugin for video keyframes): find the
   earliest publication, date, photographer and original context.
2. Check the caption/description on the source page matches *your* claim (place, date, people, event).
3. Wrong-context photos are factual errors (lesson: a protest photo from a different event). If unsure, don't use it.
4. Record source URL, author, license, date in `CREDITS.json` (the fetch script does it for Commons).

## Showing documents so they feel real

| Technique | How (tested template: `templates/scene-document-pushin.html`) |
|---|---|
| Establish then push in | Show the whole page/person holding it 1 s, then camera push 1.2 s `power2.inOut` to the key line (scale ~1.9) |
| Highlighter | Yellow bar `mix-blend-mode: multiply`, opacity .85, rotated to the text angle, `scaleX 0→1` in 0.45 s, placed in *image* coordinates inside the camera wrapper so it moves with the page |
| Source chip | Small label "SOURCE: publication, date · credit · license" inside the safe zone, 30 px+ |
| Paper on desk | Slight rotation (−2°…2°), soft shadow, real texture background; never a flat white card |
| Quote pull | Crop the exact sentence, then the same words as large clean text (no paraphrase) |
| Multiple pages | Stack/fan pages, each entering on the VO word that names it |

Snapshot the push-in end frame: the marker must sit exactly on the words (adjust x/y/rotation by looking).

## Credits on screen and in description

- On screen: short chip while the asset is visible ("PHOTO: NASA · PD", "Washington Post, 21 July 1969").
- Description: the full lines from `CREDITS.md`. CC BY/BY-SA need author + license + link (Commons credit-line guidance); Commons media reused in YouTube videos should be attributed in the video and the description.
- Paid stock: keep license IDs in `04_audio/music/LICENSES.md` / `assets/LICENSES.md`.
