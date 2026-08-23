#!/usr/bin/env python3
"""Design an original Qwen3-TTS voice, then reuse it across a film narration."""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
from pathlib import Path

import mlx.core as mx
import numpy as np
import soundfile as sf
from mlx_audio.tts.utils import load_model


DESIGN_MODEL = "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit"
CLONE_MODEL = "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit"


def find_ffmpeg(project: Path) -> str:
    installed = shutil.which("ffmpeg")
    if installed:
        return installed
    candidates = sorted(
        (project / ".media-venv/lib/python3.12/site-packages/imageio_ffmpeg/binaries").glob("ffmpeg-*")
    )
    if candidates:
        return str(candidates[0])
    raise FileNotFoundError("ffmpeg is required for MP3 output")


def save_wav(result, path: Path) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    audio = np.asarray(result.audio, dtype=np.float32).squeeze()
    sf.write(path, audio, result.sample_rate, subtype="PCM_16")
    duration = len(audio) / result.sample_rate
    peak = float(np.max(np.abs(audio))) if len(audio) else 0.0
    rms = float(np.sqrt(np.mean(np.square(audio)))) if len(audio) else 0.0
    generation_seconds = float(getattr(result, "processing_time_seconds", 0.0) or 0.0)
    rtf = getattr(result, "real_time_factor", None)
    if rtf is None:
        rtf = generation_seconds / duration if duration else 0.0
    return {
        "duration": round(duration, 3),
        "sample_rate": result.sample_rate,
        "peak_dbfs": round(20 * math.log10(max(peak, 1e-9)), 2),
        "rms_dbfs": round(20 * math.log10(max(rms, 1e-9)), 2),
        "generation_seconds": round(generation_seconds, 3),
        "real_time_factor": round(float(rtf), 3),
    }


def write_mp3(ffmpeg: str, wav: Path, mp3: Path) -> None:
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(wav),
            "-af",
            "loudnorm=I=-19:TP=-2:LRA=7",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(mp3),
        ],
        check=True,
    )


def load_project(project: Path) -> tuple[dict, dict, list[dict]]:
    plan_path = project / "film-plan.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    profiles = json.loads((project / "voice-profiles.json").read_text(encoding="utf-8"))
    narration_path = project / "narration.json"
    narration = (
        json.loads(narration_path.read_text(encoding="utf-8"))
        if narration_path.exists()
        else plan.get("narration", [])
    )
    if not narration:
        raise SystemExit("narration is empty")
    return plan, profiles, narration


def normalized_text(segment: dict, profile: dict) -> str:
    text = segment.get("tts_text", segment["text"])
    for source, target in profile.get("pronunciations", {}).items():
        text = text.replace(source, target)
    return re.sub(r"\s+", " ", text).strip()


def design_samples(args: argparse.Namespace) -> None:
    project = args.project
    _, profiles, _ = load_project(project)
    profile = profiles[args.role]
    instructions = profile.get("sample_instructions") or [profile.get("instructions", "")]
    instructions = [instruction for instruction in instructions if instruction.strip()]
    if not instructions:
        raise SystemExit(f"voice profile has no sample instructions: {args.role}")
    reference_text = profile.get("reference_text") or args.reference_text
    destination = project / "audio/voice-tests/qwen3"
    destination.mkdir(parents=True, exist_ok=True)
    ffmpeg = find_ffmpeg(project)
    model_name = profile.get("design_model", DESIGN_MODEL)
    model = load_model(model_name)
    records = []
    for index, instruction in enumerate(instructions):
        mx.random.seed(args.seed + index)
        result = list(
            model.generate_voice_design(
                text=reference_text,
                instruct=instruction,
                language="Chinese",
                temperature=args.temperature,
                top_k=args.top_k,
                top_p=args.top_p,
                repetition_penalty=args.repetition_penalty,
                max_tokens=args.max_tokens,
                verbose=False,
            )
        )[0]
        name = f"{args.role}-{index + 1:02d}"
        wav = destination / f"{name}.wav"
        record = save_wav(result, wav)
        write_mp3(ffmpeg, wav, destination / f"{name}.mp3")
        record.update(
            {
                "id": name,
                "file": wav.name,
                "model": model_name,
                "reference_text": reference_text,
                "instruction": instruction,
                "seed": args.seed + index,
            }
        )
        records.append(record)
        print(json.dumps(record, ensure_ascii=False), flush=True)
    (destination / "sample-manifest.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def generate_narration(args: argparse.Namespace) -> None:
    project = args.project
    plan, profiles, narration = load_project(project)
    profile = profiles[args.role]
    selected = [segment for segment in narration if segment.get("voice") == args.role]
    if not selected:
        raise SystemExit(f"no narration segments use role: {args.role}")
    reference_audio = project / profile["reference_audio"]
    if not profile.get("reference_audio") or not reference_audio.exists():
        raise SystemExit(f"select a valid synthetic reference_audio for role: {args.role}")
    reference_text = profile.get("reference_text") or args.reference_text
    model_name = profile.get("production_model", CLONE_MODEL)
    voice_dir = project / plan["audio"]["voice_dir"]
    wav_dir = voice_dir / "wav"
    voice_dir.mkdir(parents=True, exist_ok=True)
    wav_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg = find_ffmpeg(project)
    model = load_model(model_name)
    manifest_path = voice_dir / "manifest.json"
    existing_manifest = (
        json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest_path.exists()
        else []
    )
    if isinstance(existing_manifest, dict):
        existing_manifest = existing_manifest.get("segments", [])
    manifest_by_id = {str(item.get("id")): item for item in existing_manifest if item.get("id")}

    for offset in range(0, len(selected), args.batch_size):
        batch = selected[offset : offset + args.batch_size]
        texts = [normalized_text(item, profile) for item in batch]
        mx.random.seed(args.seed + offset)
        results = list(
            model.batch_generate(
                texts=texts,
                ref_audio=str(reference_audio),
                ref_text=reference_text,
                lang_code="Chinese",
                temperature=args.temperature,
                top_k=args.top_k,
                top_p=args.top_p,
                repetition_penalty=args.repetition_penalty,
                max_tokens=args.max_tokens,
                verbose=False,
            )
        )
        indexed = {int(result.sequence_idx): result for result in results}
        if len(indexed) != len(batch):
            raise RuntimeError(f"batch {offset} returned {len(indexed)} of {len(batch)} items")
        for local_index, segment in enumerate(batch):
            result = indexed[local_index]
            wav = wav_dir / f"{segment['id']}.wav"
            mp3 = voice_dir / f"{segment['id']}.mp3"
            record = save_wav(result, wav)
            write_mp3(ffmpeg, wav, mp3)
            segment["duration"] = record["duration"]
            segment["file"] = str(mp3.relative_to(project))
            record.update(
                {
                    "id": segment["id"],
                    "voice": segment["voice"],
                    "file": mp3.name,
                    "wav_file": str(wav.relative_to(voice_dir)),
                    "text": segment["text"],
                    "tts_text": texts[local_index],
                    "model": model_name,
                    "reference_audio": str(reference_audio.relative_to(project)),
                }
            )
            manifest_by_id[str(segment["id"])] = record
            print(f"voice={segment['id']} duration={record['duration']:.3f}", flush=True)

    plan["narration"] = narration
    (project / "film-plan.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest_path.write_text(
        json.dumps(list(manifest_by_id.values()), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--role", default="narrator")
    parser.add_argument("--mode", choices=["samples", "generate"], default="generate")
    parser.add_argument("--reference-text", default="这是一段用于固定原创旁白声线的中文参考文字。")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--seed", type=int, default=6113)
    parser.add_argument("--temperature", type=float, default=0.68)
    parser.add_argument("--top-k", type=int, default=35)
    parser.add_argument("--top-p", type=float, default=0.92)
    parser.add_argument("--repetition-penalty", type=float, default=1.5)
    parser.add_argument("--max-tokens", type=int, default=1536)
    args = parser.parse_args()
    args.project = args.project.expanduser().resolve()
    if args.mode == "samples":
        design_samples(args)
    else:
        generate_narration(args)


if __name__ == "__main__":
    main()
