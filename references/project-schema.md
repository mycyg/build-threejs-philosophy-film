# Film project schema

Keep production state explicit. `storyboard.json` owns shot intent; `film-plan.json` owns the final timeline; the ledgers own provenance and verification.

## `film-plan.json`

```json
{
  "meta": {
    "title": "Film title",
    "slug": "film-slug",
    "duration": 180,
    "width": 1920,
    "height": 1080,
    "fps": 24,
    "language": "zh-CN",
    "format": "documentary"
  },
  "production": {
    "renderer": "hybrid",
    "audio_locked": false,
    "picture_locked": false
  },
  "design": {
    "thesis": "One sentence",
    "typography": {"display": "Chosen for this film", "text": "Chosen for this film"},
    "palette": ["#hex"],
    "layout_principles": ["Project-specific rules"],
    "materials": ["Project-specific material language"],
    "motion_verbs": ["Project-specific motion grammar"],
    "transition_seconds": 2.0
  },
  "credits": {
    "developed_by": "Creator name",
    "company": "Company",
    "speak_developed_by": true,
    "speak_company": false
  },
  "audio": {
    "music_file": "audio/music.m4a",
    "voice_dir": "voice",
    "music_base": 0.19,
    "music_duck": 0.052
  },
  "render": {
    "silent_video": "render/silent.mp4",
    "output_video": "render/final.mp4"
  },
  "qa": {"intentional_holds": []},
  "scenes": [],
  "narration": []
}
```

Supported renderer values are `hybrid`, `threejs`, `canvas2d`, and `edit`. Renderer choice may vary at shot level, but the top-level value describes the main assembly pipeline.

## `storyboard.json`

```json
{
  "title": "Film title",
  "revision": 1,
  "shots": [
    {
      "id": "sh-001",
      "scene_id": "opening",
      "start": 0,
      "end": 6.5,
      "narrative_function": "Create the first unanswered question",
      "evidence_ids": ["ev-001"],
      "audio": {"type": "narration", "segment_ids": ["nar-001"]},
      "composition": "What is in frame and where",
      "action": "What visibly changes inside the shot",
      "transition_in": "Motivated entry",
      "transition_out": "Motivated exit",
      "renderer": "canvas2d",
      "intentional_hold": false,
      "asset_needs": [
        {
          "role": "primary",
          "kind": "generated-image",
          "prompt_intent": "The shot-specific image requirement",
          "target_count": 6,
          "selected_min": 1
        }
      ]
    }
  ]
}
```

Shot starts and ends must be continuous after picture lock. Before lock, approximate timings are acceptable if the sequence and narration remain complete.

## Scene fields

Each final scene contains `id`, `start`, `end`, `title`, `narrative_function`, `philosophy`, `human_meaning`, `evidence_ids`, `visual_motif`, `motion`, and `assets`. Assets may be ledger IDs or project-relative paths. Ledger IDs are preferred.

## Narration fields

Each narration item contains `id`, `start`, `voice`, and `text`. Optional fields include `subtitle`, `tts_text`, `intent`, `scene_id`, `duration`, and `file`. Generated duration and file path must be written back after synthesis.

## Asset ledger

`assets/asset-ledger.json` is an object:

```json
{
  "policy": {
    "surplus_multiplier": 3.0,
    "default_candidates_per_shot": 6,
    "keep_rejected": true
  },
  "assets": [
    {
      "id": "asset-sh001-primary-01",
      "kind": "generated-image",
      "path": "assets/generated/sh001-primary-01.png",
      "shot_ids": ["sh-001"],
      "role": "primary",
      "status": "candidate",
      "source": "codex-built-in-imagegen",
      "prompt": "Final production prompt",
      "license": "generated for project",
      "verified": true
    }
  ]
}
```

Allowed selection states are `candidate`, `selected`, `alternate`, and `rejected`. Keep useful rejected candidates for recovery edits, but never count them toward coverage.

## Approval record

`storyboard-approval.json` contains `approved`, `mode`, `approved_at`, `storyboard_revision`, and `notes`. `mode` is `user-confirmed` or `delegated`. Any storyboard change that alters argument, narration, renderer mix, source use, or runtime increments the revision and invalidates approval until reconfirmed.
