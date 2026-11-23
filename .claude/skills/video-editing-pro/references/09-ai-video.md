# AI video (last resort after real assets)

## Decide
| Need | Use |
|---|---|
| Real people, events, news, history evidence | **Real/archival/licensed only** — never generate |
| Event with no footage (ancient, unfilmed) | AI/3D reconstruction, on-screen label "Reconstruction", disclosure ticked |
| Abstract concepts (money flow, data, "AI brain") | motion graphics or AI |
| Product without a shoot | image-to-video from the real product photo |
| Backgrounds, loops, textures, transition plates | AI or stock |

YouTube requires creators to disclose realistic AI-generated or meaningfully altered content (real person/place/event that could be mistaken for real); clearly unrealistic/animated content and minor edits don't need it.

## Prompt structure
`[shot size + camera move + lens] [subject: fixed appearance] [one action, speed/physics] [setting + time] [light: source, direction, colour temp] [palette] [style/texture] [duration] [aspect] [audio if supported]`
- Camera words first: dolly in, tracking, crane, aerial, static locked-off, handheld, rack focus, 35/85 mm, shallow DOF.
- One main action per 5–10 s clip; start simple, add detail once motion works.
- **Image-to-video:** describe motion only ("The camera slowly pushes in as the subject turns toward the window"); refer to "the subject/the woman".
- Positive phrasing (some models do the opposite of negative prompts).

Examples:
- Cinematic: "Slow dolly-in, 35mm, shallow depth of field. An elderly fisherman with a grey beard mends a net on a wooden boat at dawn; mist drifts over calm water. Low golden light from the left, teal shadows, amber highlights. Cinematic realism, subtle film grain. 8 seconds, 16:9."
- Product: "Macro tracking shot circling 90° around a matte black smartwatch on dark slate; a water drop slides down the glass. Hard top-right key, thin specular edge, deep black ground. 6 seconds, 9:16."
- Background loop: "Static wide shot of a study with bookshelves and a warm desk lamp, softly out of focus, dust in the lamp beam, 3200K practicals, cool window fill, no people. 10 seconds, seamless loop."
- B-roll: "Aerial drone push over a container port at blue hour; cranes lift containers, lights flicker on; cool ambient with orange sodium lamps; news-documentary realism. 8 seconds, 9:16."
- Transition plate: "Extreme close-up, camera pushes into black ink spreading in water until the frame is fully black. 3 seconds, 9:16."

## Consistency
Same 1–3 reference images every generation · identical "unchangeable features" paragraph · fixed lighting language · reuse seed when exposed · same lens vocabulary · 3–5 variants per shot (expect to keep ~1 in 4) · log prompt/seed/model/version in `prompts.md`.

## Post-processing order
1. Select usable seconds (reject warped hands, identity drift, morphing edges, flicker).
2. Upscale first, on ungraded clips, with a model made for AI footage (generic upscalers amplify artifacts).
3. Deflicker/stabilise.
4. Soften over-sharp "plastic" look: tiny blur, less sharpening.
5. Grade to match real footage (`06-color.md`).
6. Shared grain across AI, stock and camera footage.
7. Add ambience + SFX (silent AI clips read fake).
8. 100% zoom pass on hands, text, faces, logos.
