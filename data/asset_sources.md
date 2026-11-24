# Asset sources that worked (Claude adds to this every run)

Format: `- <topic type>: <site> — query "<query>" — <what it gave> — licence`
- Video game topic: rockstargames.com/VI/media -> GTAVI_Screenshots.zip (138 official 4K stills, "download and share") — credit © Rockstar Games — stills only, no trailers
- Vice City / Miami vibe: Mixkit free-stock-video tags miami, neon, palm-tree, sports-car, night-city (assets.mixkit.co/videos/<id>/<id>-720.mp4) — Mixkit free license
- Money: Mixkit tags money, cash (ids 45703, 47005, 18296 worked) — Mixkit free license
- Gaming: Mixkit tags gaming, video-game (23501 controller hands, 47140, 43527) — Mixkit free license
- Cinema: Mixkit tag cinema (2860 film reel, 49326 clapper, 25478 screen) — Mixkit free license
- SFX: mixkit.co/free-sound-effects/whoosh (1489-1492) and /impact — Mixkit free license
- Company filings as visuals: Take-Two IR PDFs (ir.take2games.com/node/<id>/pdf) rendered with PyMuPDF + highlight; SEC blocks automated browsers

## 24 Nov 2026 (Iran blockade Short)
- Wikimedia Commons via `.claude/skills/video-editing-pro/scripts/fetch_commons.py search/get` works when `fetch_visuals.py` gets 429/non-JSON (it backs off). Great PD finds: "Kharg Island" (NASA satellite), "USS Abraham Lincoln Strait of Hormuz" (US Navy Flickr imagery), "oil tanker Persian Gulf" (ABOT tanker).
- Commons .webm via the API often 429s; budget time or skip.
- Owner's Drive motion backgrounds: download single files by id with gdown (folder sync is slow). Skip "Klickpin.com" files (Pinterest re-posts, no licence).
- Mixkit music by id: https://assets.mixkit.co/music/<id>/<id>.mp3 (846 "I Won't Surrender" = steady tense energy, 114 s).
- Owner's Drive library (24 Nov): root folder has Music_BGM (15 Mixkit tracks, named BGM_<Mood>_...), LUTs_Color_Grades (11 .cube), Sound_Effects (36, SFX_<Type>_...), Transitions (7 ink mattes), BRoll (18), Backgrounds, Motion_Graphics, Animations_Overlays. Fast path: Drive search by parent id + gdown per file id into library/new/<folder>/ (sync_assets.py folder sync takes 30+ min).
- Picks that worked for geopolitics/finance: BGM_Investigation_FallenAsper_565 (steady, 295 s), LUT_ColdThriller_BlueTension (docs stay white, cool look). BigCinematicImpact 788 is too loud on a spoken line; use it only in a gap.
