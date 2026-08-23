#!/usr/bin/env python3
"""Expand approved storyboard asset needs into abundant image-generation jobs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


VARIANT_AXES = [
    ("establishing", "wider context, clear geography, and useful negative space"),
    ("recognition", "the subject or evidence becomes immediately legible"),
    ("transformation", "a visible state change that advances the shot's idea"),
    ("detail", "a close material, human, object, or document detail"),
    ("transition", "composition and movement space designed for the adjoining shot"),
    ("alternate-composition", "a meaningfully different framing, not a cosmetic reroll"),
    ("recovery-insert", "an insert that can replace or shorten a weak visual hold"),
    ("negative-space", "an editorial composition with controlled space for captions"),
]


def load(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return result or "asset"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an image-generation queue from a storyboard")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--replace", action="store_true", help="replace an existing nonempty queue")
    args = parser.parse_args()

    project = args.project.expanduser().resolve()
    storyboard = load(project / "storyboard.json")
    approval = load(project / "storyboard-approval.json")
    brief = load(project / "creative-brief.json")
    revision = int(storyboard.get("revision", 0))
    if not approval.get("approved") or int(approval.get("storyboard_revision", -1)) != revision:
        raise SystemExit("storyboard must be approved at its current revision before queue generation")

    queue_path = project / "assets" / "generation-queue.json"
    if queue_path.exists() and not args.replace:
        current = load(queue_path)
        if current.get("jobs"):
            raise SystemExit(f"generation queue is not empty; use --replace to rebuild: {queue_path}")

    visual = brief.get("visual_world", {})
    continuity = {
        "ontology": visual.get("ontology", []),
        "palette": visual.get("palette", []),
        "texture": visual.get("texture", ""),
        "light": visual.get("light", ""),
        "shot_grammar": visual.get("shot_grammar", ""),
    }
    jobs: list[dict] = []
    for shot in storyboard.get("shots", []):
        shot_id = str(shot.get("id", "shot"))
        for need_index, need in enumerate(shot.get("asset_needs", []), start=1):
            kind = str(need.get("kind", ""))
            if kind not in {"generated-image", "generated-raster", "imagegen"}:
                continue
            count = max(1, int(need.get("target_count", 1)))
            role = str(need.get("role", f"need-{need_index}"))
            for variant_index in range(count):
                axis, axis_note = VARIANT_AXES[variant_index % len(VARIANT_AXES)]
                job_id = f"gen-{slug(shot_id)}-{slug(role)}-{variant_index + 1:02d}"
                jobs.append(
                    {
                        "id": job_id,
                        "status": "pending",
                        "shot_id": shot_id,
                        "scene_id": shot.get("scene_id", ""),
                        "role": role,
                        "kind": kind,
                        "variant_index": variant_index + 1,
                        "variant_axis": axis,
                        "prompt_spec": {
                            "use_case": need.get("use_case", "stylized-concept"),
                            "asset_type": "narrative film shot candidate",
                            "primary_request": need.get("prompt_intent", ""),
                            "shot_function": shot.get("narrative_function", ""),
                            "composition": shot.get("composition", ""),
                            "action": shot.get("action", ""),
                            "variant_direction": axis_note,
                            "continuity": continuity,
                            "constraints": need.get("constraints", []),
                            "avoid": need.get("avoid", []),
                        },
                        "output_hint": f"assets/generated/{job_id}.png",
                        "asset_id": f"asset-{job_id}",
                    }
                )

    queue = {
        "storyboard_revision": revision,
        "created_from_approved_storyboard": True,
        "imagegen_route": "codex-built-in-imagegen",
        "jobs": jobs,
    }
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    queue_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"queue={queue_path}")
    print(f"jobs={len(jobs)} shots={len(storyboard.get('shots', []))}")


if __name__ == "__main__":
    main()
