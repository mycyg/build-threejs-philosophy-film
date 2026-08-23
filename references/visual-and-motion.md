# Visual families and motion continuity

## Generate a library, then edit

Do not ask one image to carry an entire scene. For each major motif or recurring subject, produce a coordinated family:

1. **Establishing** — geography, scale, or negative space.
2. **Recognition** — the subject or idea becomes legible.
3. **Transformation** — state, material, or relationship changes.
4. **Convergence** — metaphor meets evidence or human consequence.
5. **Detail** — hands, surfaces, documents, tools, faces, or environmental fragments.
6. **Transition** — frames with composition or negative space designed for the adjoining shot.
7. **Recovery** — alternate crop or insert that can replace a weak hold.

Keep family continuity through identity, era, geography, lens, horizon, palette, lighting direction, material, grain, and aspect ratio. Write those invariants once, then vary only the shot-specific delta.

## Selection

Judge candidates at intended crop and sequence position. A beautiful standalone image may fail because it has no transition space, wrong gaze direction, inconsistent light, or no room for subtitles.

Promote one asset to `selected` and at least one to `alternate` for every designed shot. Preserve candidate and rejected files when they may solve a later continuity or timing problem.

## Bind metaphor to evidence

Useful patterns include:

- material reveal into a real document or interface;
- signal inheritance from generated marks into charts or timelines;
- spatial continuation from an art environment into a source plane;
- shape correspondence between a motif and real evidence;
- human return from systems imagery to an ordinary consequence;
- audio bridge that lets evidence arrive before the picture.

Do not cut from stylized art to an unrelated screenshot solely because both are available.

## Three.js when selected

Build scene-specific groups with deterministic `build` and `update(time, progress, alpha)` behavior. Maintain one timeline clock and one exact `renderAt(seconds)` path shared by preview and encoding.

Three.js can provide object persistence, camera-state blending, occlusion, depth, procedural transformation, and spatial continuity. It should not impose a title location, subtitle box, particle language, portal, camera lens, or transition duration.

## Editorial movement

For still documents and images, use rostrum techniques sparingly: reveal exact lines, compare context with detail, move between page and crop, introduce annotations, or shift focus. A slow zoom without information change is still a static shot in editorial terms.

## Frame-evolution check

At storyboard and rough-cut stages, ask of each three-second span:

- did composition, subject, evidence, or meaning change;
- did the sound create a justified reason to hold;
- is the next available alternate stronger;
- is the viewer given enough time to read the important evidence;
- is motion serving attention rather than filling time.

Declare deliberate holds in `film-plan.json`. Accidental freezes belong in the motion-audit failure report.
