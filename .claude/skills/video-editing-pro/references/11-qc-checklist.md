# QC checklist (run before every delivery)

## Automated
```bash
npx hyperframes check --json                     # fix every error, judge every warning
npx hyperframes snapshot --review                # scene, seam (±0.2 s) and phone-width (360 px) sheets
npx hyperframes render --quality standard --output renders/final.mp4
python3 scripts/publish_loudness.py renders/final.mp4 renders/final_social.mp4 --lufs -14
python3 scripts/qc_check.py renders/final_social.mp4 --platform shorts > 09_check/QC.md   # exit 1 = a FAIL
npx hyperframes audio renders/final.mp4 --json   # hits where the picture hits
```

## Manual passes
Watch 3 times: (1) phone, sound on, full speed; (2) sound off (do pictures + captions tell it?); (3) frame-step every cut.
Describe each beat frame in one sentence as a stranger would; anything you'd have to explain is a P0.
Write notes as `t=4.2s · where · problem → exact change · what stays`; fix P0 (breaks read/contract) and worthwhile P1 (weakens), then re-snapshot only what changed.

**Edit:** hook in 1–3 s without sound · no dead air · every claim has a visual · no visual repeated within ~20 s · no flash/black frames at seams · ending lands · length on target.
**Real assets:** every photo/document verified (reverse search, context), credit chip on screen, `CREDITS.md` complete, no NC/ND misuse, AI shots labelled + disclosed.
**Audio:** −14 LUFS ±1 (or platform target), TP ≤ −1 dBTP, VO clear on phone speaker, music ducks and returns, SFX audible + in sync, no clicks (5–10 ms fades).
**Colour:** skin on the skin-tone line, no casts on neutrals, no unintended clipping, scenes matched, AI/stock/archive unified.
**Text:** inside y 288–1248 / x 120–888 (9:16), spelling/names/numbers/dates checked against sources, captions synced ≥ 0.83 s, Devanagari matras intact, contrast ≥ 4.5:1, ≤ 3 flashes/s.
**Export:** resolution/fps/codec/BT.709/AAC 48 kHz correct; plays start to end; first frame strong; SRT + thumbnail + credits delivered; project + plan + decisions archived.
Delivery note states: measured vs looked-at; sound measured, not heard.
