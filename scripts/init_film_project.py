#!/usr/bin/env python3
"""Create a style-neutral narrative-film production workspace."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "assets" / "film-template"


def slugify(value: str) -> str:
    ascii_slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return ascii_slug or "narrative-film"


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a narrative-film production project")
    parser.add_argument("--title", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--duration", type=float, default=180.0)
    parser.add_argument(
        "--renderer",
        choices=["hybrid", "threejs", "canvas2d", "edit"],
        default="hybrid",
    )
    parser.add_argument(
        "--format",
        choices=["documentary", "essay", "explainer", "product", "poetic"],
        default="documentary",
    )
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--fps", type=float, default=24.0)
    parser.add_argument("--language", default="zh-CN")
    parser.add_argument("--creator", default="")
    parser.add_argument("--company", default="")
    args = parser.parse_args()

    if args.duration < 15:
        raise SystemExit("duration must be at least 15 seconds")
    if args.width < 320 or args.height < 180 or args.fps <= 0:
        raise SystemExit("invalid render dimensions or frame rate")

    output = args.output.expanduser().resolve()
    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"output directory is not empty: {output}")

    directories = [
        "source/original",
        "source/research",
        "assets/captures",
        "assets/source-clips",
        "assets/generated",
        "assets/derived",
        "assets/selected",
        "voice/reference",
        "voice/wav",
        "audio/candidates",
        "edit",
        "render/work",
        "subtitles",
        "qa/frames",
        "qa/contact-sheets",
        "qa/transcripts",
    ]
    for relative in directories:
        (output / relative).mkdir(parents=True, exist_ok=True)

    for name in ["film.html", "film-runtime.js", "film-design.stub.js", "package.json"]:
        destination = "film-design.js" if name == "film-design.stub.js" else name
        shutil.copy2(TEMPLATE_DIR / name, output / destination)

    meta = {
        "title": args.title,
        "slug": slugify(args.title),
        "duration": float(args.duration),
        "width": args.width,
        "height": args.height,
        "fps": float(args.fps),
        "language": args.language,
        "format": args.format,
    }
    plan = {
        "meta": meta,
        "production": {
            "renderer": args.renderer,
            "audio_locked": False,
            "picture_locked": False,
        },
        "design": {
            "thesis": "",
            "palette": [],
            "typography": {"display": "", "text": ""},
            "layout_principles": [],
            "materials": [],
            "motion_verbs": [],
            "transition_seconds": 2.0,
        },
        "credits": {
            "developed_by": args.creator,
            "company": args.company,
            "speak_developed_by": bool(args.creator),
            "speak_company": False,
        },
        "audio": {
            "music_file": "audio/music.m4a",
            "voice_dir": "voice",
            "music_base": 0.19,
            "music_duck": 0.052,
        },
        "render": {
            "silent_video": "render/silent.mp4",
            "output_video": "render/final.mp4",
        },
        "qa": {"intentional_holds": []},
        "scenes": [],
        "narration": [],
    }
    dump(output / "film-plan.json", plan)
    dump(
        output / "creative-brief.json",
        {
            "title": args.title,
            "audience": "",
            "thesis": "",
            "tension": "",
            "emotional_arc": [],
            "evidence_strategy": [],
            "visual_world": {
                "ontology": [],
                "palette": [],
                "typography": "",
                "texture": "",
                "light": "",
                "shot_grammar": "",
                "edit_grammar": "",
            },
            "production": {
                "format": args.format,
                "renderer": args.renderer,
                "asset_surplus_multiplier": 3.0,
                "subtitle_style": "",
                "target_runtime_seconds": float(args.duration),
            },
            "voice": "",
            "music": "",
            "approved_by_user": False,
        },
    )
    dump(output / "storyboard.json", {"title": args.title, "revision": 1, "shots": []})
    dump(
        output / "storyboard-approval.json",
        {
            "approved": False,
            "mode": "",
            "approved_at": "",
            "storyboard_revision": 1,
            "notes": "",
        },
    )
    dump(output / "narration.json", [])
    dump(output / "source" / "evidence-ledger.json", {"evidence": []})
    dump(
        output / "assets" / "asset-ledger.json",
        {
            "policy": {
                "surplus_multiplier": 3.0,
                "default_candidates_per_shot": 6,
                "keep_rejected": True,
            },
            "assets": [],
        },
    )
    dump(output / "assets" / "generation-queue.json", {"storyboard_revision": 1, "jobs": []})
    dump(output / "assets" / "source-verification.json", {"clips": []})
    dump(
        output / "voice-profiles.json",
        {
            "narrator": {
                "provider": "local-mlx",
                "name": "zh-CN-XiaoxiaoNeural",
                "rate": "+5%",
                "pitch": "-4Hz",
                "volume": "+0%",
                "design_model": "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit",
                "production_model": "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit",
                "reference_audio": "",
                "reference_text": "这是一段用于固定原创旁白声线的中文参考文字。",
                "sample_instructions": [
                    "A natural documentary narrator with precise Mandarin and an unforced conversational cadence.",
                    "A clear cultural-essay narrator with restrained emotion, varied rhythm, and no announcer tone."
                ],
                "pronunciations": {},
            }
        },
    )
    dump(
        output / "local-models.json",
        {
            "tts": {
                "engine": "qwen3-tts-mlx",
                "environment": ".tts-venv",
                "device": "apple-silicon",
            },
            "asr": {
                "engine": "faster-whisper",
                "model": "small",
                "device": "auto",
                "compute_type": "auto",
                "language": args.language.split("-")[0],
            },
            "image": {"engine": "codex-built-in-imagegen", "local_fallback": None},
        },
    )
    dump(output / "edit" / "edl.json", {"version": 1, "tracks": []})
    (output / "audio" / "music-brief.md").write_text(
        "# Music brief\n\n## Thesis and emotional arc\n\n## Duration and tempo\n\n"
        "## Instrumentation and texture\n\n## Opening, central turn, and ending\n\n## Exclusions\n",
        encoding="utf-8",
    )

    print(f"created={output}")
    print(f"renderer={args.renderer} format={args.format}")
    print("next=ingest sources, approve creative brief, write storyboard, then obtain storyboard approval")


if __name__ == "__main__":
    main()
