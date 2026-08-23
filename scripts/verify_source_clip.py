#!/usr/bin/env python3
"""Extract a source clip, transcribe its original audio, and record verification evidence."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import shutil
import subprocess
from pathlib import Path


def normalized(text: str) -> str:
    return "".join(character.lower() for character in text if character.isalnum())


def seconds(value: str) -> float:
    if ":" not in value:
        return float(value)
    parts = [float(part) for part in value.split(":")]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    raise argparse.ArgumentTypeError(f"invalid time value: {value}")


def load_model(name: str, device: str, compute_type: str):
    try:
        from faster_whisper import WhisperModel
    except ImportError as error:
        raise SystemExit(
            "faster-whisper is required. Install requirements-asr.txt in a project-local environment."
        ) from error
    return WhisperModel(name, device=device, compute_type="default" if compute_type == "auto" else compute_type)


def update_verification(path: Path, record: dict) -> None:
    payload = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"clips": []}
    clips = payload.setdefault("clips", [])
    clips[:] = [item for item in clips if item.get("asset_id") != record["asset_id"]]
    clips.append(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_asset_ledger(path: Path, record: dict, rights_note: str) -> None:
    payload = (
        json.loads(path.read_text(encoding="utf-8"))
        if path.exists()
        else {"policy": {"surplus_multiplier": 3.0}, "assets": []}
    )
    if isinstance(payload, list):
        payload = {"policy": {}, "assets": payload}
    assets = payload.setdefault("assets", [])
    existing = next((item for item in assets if item.get("id") == record["asset_id"]), None)
    values = {
        "id": record["asset_id"],
        "kind": "source-video",
        "path": record["clip_file"],
        "shot_ids": existing.get("shot_ids", []) if existing else [],
        "role": existing.get("role", "source-clip") if existing else "source-clip",
        "status": existing.get("status", "candidate") if existing else "candidate",
        "source": record.get("source_url") or record.get("source_file"),
        "license": rights_note or "review required before publication",
        "verified": record["verified"],
    }
    if existing:
        existing.update(values)
    else:
        assets.append(values)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract and verify an authentic source clip")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--asset-id", required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--start", type=seconds, required=True)
    parser.add_argument("--end", type=seconds, required=True)
    parser.add_argument("--speaker", required=True)
    parser.add_argument("--source-url", default="")
    parser.add_argument("--source-title", default="")
    parser.add_argument("--expected", default="")
    parser.add_argument("--language", default="")
    parser.add_argument("--model", default="small")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--compute-type", default="auto")
    parser.add_argument("--threshold", type=float, default=0.88)
    parser.add_argument("--speaker-confirmed", action="store_true")
    parser.add_argument("--context-confirmed", action="store_true")
    parser.add_argument("--rights-note", default="")
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()

    project = args.project.expanduser().resolve()
    source = args.source.expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"source file not found: {source}")
    if args.end <= args.start:
        raise SystemExit("--end must be greater than --start")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ffmpeg is required")

    clip = project / "assets" / "source-clips" / f"{args.asset_id}.mp4"
    if clip.exists() and not args.replace:
        raise SystemExit(f"clip already exists; use --replace: {clip}")
    clip.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-ss",
            f"{args.start:.3f}",
            "-i",
            str(source),
            "-t",
            f"{args.end - args.start:.3f}",
            "-map",
            "0:v:0?",
            "-map",
            "0:a:0?",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "medium",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(clip),
        ],
        check=True,
    )

    model = load_model(args.model, args.device, args.compute_type)
    iterator, info = model.transcribe(
        str(clip),
        language=args.language or None,
        word_timestamps=True,
        vad_filter=True,
        beam_size=5,
    )
    transcript = "".join(segment.text for segment in iterator).strip()
    expected_norm = normalized(args.expected)
    actual_norm = normalized(transcript)
    similarity = (
        difflib.SequenceMatcher(None, expected_norm, actual_norm).ratio()
        if expected_norm
        else None
    )
    text_confirmed = similarity is None or similarity >= args.threshold
    verified = args.speaker_confirmed and args.context_confirmed and text_confirmed
    transcript_path = project / "qa" / "transcripts" / "source" / f"{args.asset_id}.txt"
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    transcript_path.write_text(transcript + "\n", encoding="utf-8")

    record = {
        "asset_id": args.asset_id,
        "verified": verified,
        "speaker": args.speaker,
        "speaker_confirmed": args.speaker_confirmed,
        "context_confirmed": args.context_confirmed,
        "source_file": str(source),
        "source_url": args.source_url,
        "source_title": args.source_title,
        "source_start": round(args.start, 3),
        "source_end": round(args.end, 3),
        "clip_file": str(clip.relative_to(project)),
        "transcript_file": str(transcript_path.relative_to(project)),
        "transcript": transcript,
        "expected": args.expected,
        "similarity": round(similarity, 4) if similarity is not None else None,
        "text_confirmed": text_confirmed,
        "detected_language": getattr(info, "language", args.language),
        "verification_method": "original picture + original audio + local ASR + manual speaker/context check",
    }
    update_verification(project / "assets" / "source-verification.json", record)
    update_asset_ledger(project / "assets" / "asset-ledger.json", record, args.rights_note)
    print(f"clip={clip}")
    print(f"transcript={transcript_path}")
    print(f"verified={verified} similarity={record['similarity']}")
    if not verified:
        raise SystemExit("clip remains unverified; inspect speaker, context, and transcript before selection")


if __name__ == "__main__":
    main()
