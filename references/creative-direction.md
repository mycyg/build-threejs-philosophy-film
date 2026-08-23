# Creative direction

## Direction conversation

Turn broad taste words into two or three distinct production systems. Each option should make different tradeoffs, not merely swap palettes.

Define each option through:

1. **Thesis** — the statement or question that organizes the film.
2. **Tension** — the force that keeps the film from becoming a summary.
3. **Audience residue** — what the viewer should still feel or reconsider afterward.
4. **Evidence strategy** — interviews, archives, documents, product behavior, generated metaphor, or lived observation.
5. **Visual ontology** — what the screen-world is made of: rooms, paper, liquid, faces, archives, threads, instruments, fields, or another source-native material.
6. **Shot grammar** — framing, lens, movement, duration, information density, and use of stillness.
7. **Edit grammar** — cut, match action, dissolve, montage, spatial continuity, evidence reveal, or another motivated system.
8. **Renderer mix** — source-led edit, editorial 2D, Three.js spatial, hybrid, or a shot-level combination.
9. **Sound world** — narrator character, authentic audio, silence, music, and sonic transitions.

Recommend one direction and explain the tradeoff in plain language. A direction should be defensible from the source, not imported from a previous project.

## Renderer decision

Choose the renderer after weighing source material and shot function.

| Evidence and motion need | Strong starting route |
|---|---|
| Interviews, archives, screenshots, documents | Source-led edit or editorial 2D |
| Abstract system behavior, depth continuity, procedural transformation | Three.js spatial |
| Article or documentary combining evidence and metaphor | Hybrid |
| Dense typography, diagrams, annotations | Canvas2D/editorial 2D |

Three.js must earn its use by expressing depth, persistence, transformation, or causality. It is excessive when it only places flat cards in a camera.

## Brief shape

Write `creative-brief.json` with:

```json
{
  "title": "Working title",
  "audience": "Who must understand or feel this",
  "thesis": "One defensible sentence",
  "tension": "The central opposition",
  "emotional_arc": ["distance", "recognition", "pressure", "release"],
  "evidence_strategy": ["primary documents", "one interview clip", "generated metaphor"],
  "visual_world": {
    "ontology": ["paper", "water", "handwritten marks"],
    "palette": ["#hex"],
    "typography": "Typography character",
    "texture": "Texture and grain",
    "light": "Lighting behavior",
    "shot_grammar": "Framing and camera behavior",
    "edit_grammar": "How shots connect"
  },
  "production": {
    "format": "documentary",
    "renderer": "hybrid",
    "asset_surplus_multiplier": 3.0,
    "subtitle_style": "Project-specific",
    "target_runtime_seconds": 180
  },
  "voice": "Narration character",
  "music": "Musical world",
  "approved_by_user": true
}
```

## Idea-to-film test

Reject a concept that only yields quotation cards. Ask what becomes visible, audible, or causally different because of the idea.

| Idea | Human consequence | Evidence | Film consequence |
|---|---|---|---|
| Memory changes responsibility | A person should not repeat their history | A dated record or recalled detail | An earlier object persists into a later shot |
| Authority hides behind safety language | Agency narrows while rhetoric stays benevolent | A quotation beside a concrete decision | The frame closes while the voice remains calm |
| Uncertainty deserves humility | A claim remains provisional | Conflicting sources or confidence marks | Fragments remain unresolved instead of snapping into a logo |

Use original lines when a quotation cannot be verified. Attribute only wording checked against the primary source.
