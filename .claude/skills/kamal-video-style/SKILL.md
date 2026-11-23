---
name: kamal-video-style
description: Plan and produce Kamal's script-led videos with documentary collage, bold explainer motion graphics, and clean visual metaphors. Turn a script into a complete material checklist, generate planned visuals with Google Flow, receive user-supplied assets, then assemble and verify the video. Use for Kamal's reference style and revisions after testing.
---

# Kamal's video production workflow

## Intent and working relationship

Communicate in clear conversational Roman Hindi/Hinglish unless the user chooses another language. The user wants a practical staged production workflow: script -> visual requirements and complete materials list -> user supplies materials -> Flow generation for assigned visuals -> edited video. Let user feedback after testing refine this skill. Preserve the script's meaning and the user's creative direction.

The established visual direction combines cinematic documentary collage, bold marketing explainers, and restrained conceptual scenes. Read [references/visual-style.md](references/visual-style.md) when planning scenes. Read [references/production.md](references/production.md) for the materials manifest, Flow workflow, assembly, and checks.

**Long videos use the Records style by default** (Kamal, 2026-11-01): read [references/records-style.md](references/records-style.md) and its frames in `references/records-style/`. Reuse its timeline bar, source cards, maps, transitions, grade and the "COMING UP NEXT" block in every long video, adapted per video; record the adaptations in `EDIT_PLAN.md`.

## Start at the current stage

- If given a script, build a scene plan and a consolidated, actionable materials list. Do not ask the user to repeat details already provided.
- If no script exists, scripts are written by the `video-scripter` skill, not here. Work from its approved `SCRIPT.md` and `LINES.tsv`.
- If supplied materials arrive, inspect them and reconcile against the existing list. Resume production instead of repeating the whole intake.
- If asked for a test, create only the agreed sample scope; do not silently produce the entire video.
- If given feedback, revise the affected output and skill guidance as requested. Do not turn one scene-specific preference into a universal rule.

## Project brief

Capture topic, target audience, platform/aspect ratio, intended duration, narration language, voiceover source, preferred treatment, captions, brand assets, and deliverable. Ask only for missing decisions that materially block work. When unspecified, use 16:9, 1920x1080, 30 fps for long-form YouTube documentaries and 9:16, 1080x1920, 30 fps for Shorts. The original style references are vertical, so recompose layouts for 16:9 rather than letterboxing them. These are changeable defaults, not verified preferences for every video.

Narration: the main narrator is the user's ElevenLabs cloned voice; Kokoro (vox-doc-sound `kokoro_vo.py`) covers secondary voices such as quotes, characters and English speakers. Use the user's supplied voiceover or agreed narration method when given. If final narration is missing, estimate timing explicitly and realign after the actual audio arrives.

## Stage 1: Script to visual plan

Break the script into meaning-based beats. Assign stable scene IDs S01, S02, etc. For each scene record:

- Exact script excerpt and intended message.
- Estimated time range, marked provisional until aligned to narration.
- Chosen treatment and reason: cinematic story, bold explainer, or clean metaphor.
- Main visual subject, background, foreground, text hierarchy, camera framing, and negative space.
- Entry, emphasis, exit, transition, and what each movement helps explain.
- Required assets by stable asset IDs, including voiceover, music and SFX.

Select a dominant treatment per video and use compatible supporting scenes. Avoid switching randomly between every reference aesthetic. Use visual metaphors for abstract ideas, documents for evidence, UI for product/process explanation, and maps for geography.

## Stage 2: Complete materials handoff

Produce a single deduplicated materials manifest covering everything needed. Separate user-supplied items, Flow-generated visuals, editor-built graphics, and items already available. Include backgrounds, cutouts, screenshots, footage, textures, maps/data, fonts, logos, voiceover, music and every purposeful SFX cue. Reuse one asset ID across scenes instead of asking for duplicates.

Give the user a concise checklist of exactly what to send, with content/format/minimum quality and scene purpose. Pair it with the full manifest so nothing is hidden. Identify essential missing items versus optional enhancements. Tell the user they can send assets in batches. Offer concrete alternatives when an essential item cannot be supplied.

Respect the user's staged workflow: deliver this requirements list before committing to final assembly. Waiting for listed materials is a dependency, not an extra permission ceremony. Continue independent preparation such as storyboards, editable text, layouts and Flow prompt drafting. Execute Flow generation when included in the active production request or explicitly requested; a request only for a list should remain planning work.

## Stage 3: Receive and generate assets

Inspect received files, map them to IDs, and update status. Report only remaining gaps, unusable assets, and meaningful choices. Do not fabricate a file, a source, a completed generation, or a successful render.

Use Google Flow for planned AI-generated visuals through the `flow-generate` skill (`flow-auto` CLI). Check tool availability/status, then use the generation modes and parameters actually supported. The user's selected generation service is Flow; do not silently replace it. If unavailable, keep prompts and the manifest ready and explain the concrete blocker.

Keep text, charts, accurate labels, outlines, highlights and arrows editable in the composition where practical. Request text-free generated artwork with clear space reserved for overlays. Generated illustrative documents must not be presented as authentic source evidence.

## Stage 4: Build the video

Once essential assets are available, assemble the video without a redundant confirmation request. Use an available renderer/editor suited to the output. If using HyperFrames, read its authoring and CLI skills and use their verified workflows. This style skill does not depend on one editor.

Align scenes to the actual narration, layer assets, animate emphasis, add captions and planned sound cues, and export a playable video. Preserve editable project files and an asset manifest so later revisions are targeted. If a dependency is missing, a clearly labelled draft may use placeholders, but never label it final.

## Stage 5: Verify and hand off

Check the full timeline for asset presence, readable text, safe framing, synchronized narration, purposeful transitions, clean audio, and a correct export. Inspect representative frames at scene transitions and text holds; test actual playback/audio when available. State limits of verification accurately.

Deliver the rendered video, editable project location, brief validation result and any remaining limitations. Do not claim that a plan, storyboard or preview image is the completed video. Invite concrete test feedback without requiring it before delivering completed work.

## Future feedback

Store confirmed preferences in the relevant reference section, keep observations separate from suggestions, and update only the applicable defaults. Examples: typography too small, excessive motion, slower pacing, fewer textures, different palette, stronger sound design. Retain room for topic-specific choices. Validate the skill structure after edits.

## Owner learnings
Added by the pipeline from the owner's feedback (newest last). These override the general advice above,
but never the fact or copyright rules.
- 2026-11-23: Owner wants a new visual every 2-3 s with many online clips, sticker/cutout photos, transitions, whoosh/impact SFX and BGM. For games/brands use the official media kit stills (credited), never trailers or gameplay video.
- 2026-11-23: Pro edit: hook = 3-4 fast cuts + big pop title + flash/shake + boom; B-roll literal to each line, video over stills; fx on every cut; layered SFX; energetic BGM from its drop.
- 2026-11-23: Check currency in money clips: a rupee line must never show euro/dollar notes (GTA 6 v6 fix).
- 2026-11-23 (owner): run sync_assets.py first; use motion backgrounds from the owner's Drive library behind cards, numbers, doc screenshots and cutouts (no flat backgrounds), plus the library's effects/overlays/sfx where they fit.
