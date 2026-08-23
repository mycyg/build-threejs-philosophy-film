# Renderers and editing

## Four production routes

### Source-led edit

Use when interviews, archives, documents, screen recordings, or factual chronology should remain primary. Build an explicit EDL or timeline and use a conventional editor or ffmpeg-based assembly. Motion graphics should clarify evidence, not replace it.

### Editorial 2D / Canvas

Use for articles, diagrams, typography, screenshots, annotations, maps, timelines, and rostrum movement. Canvas2D, DOM, SVG, or a compositing tool may carry the film. Preserve text sharpness and exact layout.

### Three.js spatial

Use when meaning depends on depth, persistent objects, procedural behavior, camera traversal, occlusion, transformation, or a continuous world model. Flat planes in 3D space do not justify the renderer by themselves.

### Hybrid

Use when evidence must remain legible but spatial passages add real meaning. Composite source clips and editorial layers at native clarity; reserve Three.js for the moments that need it.

## Production kernel versus art direction

Reusable code may own:

- deterministic time and frame stepping;
- media loading and caching;
- preview and exact-time seeking;
- encoding hooks;
- audio/subtitle cue lookup;
- color management and resolution;
- test and debug controls.

Reusable code must not decide:

- palette, font, title placement, grid, margins, lens, camera path;
- card shape, portal, particles, glow, texture, vignette;
- scene count, duration pattern, transition preset, subtitle box;
- the relative importance of source evidence and generated art.

The bundled `film-design.stub.js` is intentionally un-authored. Replace it after storyboard approval. The validator blocks final render while the stub marker remains.

## Shot-level motion

Write an internal beat list for each shot. Vary one or more of:

- framing or crop;
- subject action;
- focus or depth;
- evidence layer;
- annotation or comparison;
- light, material, or state;
- camera position;
- foreground occlusion;
- sound-driven reveal.

Do not animate everything. A justified still frame can be powerful; record it as intentional and give it an exit. The motion audit detects accidental freezes, while human review decides whether a hold is meaningful.

## Transitions

Derive transitions from causality: a document fold becomes a landscape, a spoken word becomes an index mark, a camera direction continues into a source clip, a sound begins before the image changes. A crossfade may be correct; a spatial portal may be wrong. Choose the smallest transition that preserves meaning.

## Audio-first picture lock

1. approve script and storyboard;
2. synthesize and audit narration;
3. lock authentic clip in/out points;
4. place final audio on the timeline;
5. retime shots to actual speech;
6. generate subtitles from actual word timing;
7. finish picture and motion;
8. mix music and effects;
9. render and audit.

This order prevents subtitles and visuals from drifting when the voice is regenerated.
