#!/usr/bin/env python3
"""Transcribe every narration file, compare it to the script, and build timed subtitles."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


PUNCTUATION = set("，。！？；：、,.!?;:\n")


@dataclass
class TimedToken:
    text: str
    start: float
    end: float


def normalized(text: str) -> str:
    return "".join(character.lower() for character in text if character.isalnum())


def audio_duration(path: Path) -> float:
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        result = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
            check=True,
            capture_output=True,
            text=True,
        )
        return float(result.stdout.strip())
    afinfo = shutil.which("afinfo")
    if afinfo:
        result = subprocess.run([afinfo, str(path)], check=True, capture_output=True, text=True)
        match = re.search(r"estimated duration:\s*([0-9.]+) sec", result.stdout)
        if match:
            return float(match.group(1))
    raise RuntimeError("ffprobe or afinfo is required to measure audio duration")


def narration_file(project: Path, plan: dict, segment: dict) -> Path:
    if segment.get("file"):
        return project / segment["file"]
    voice_dir = project / plan["audio"]["voice_dir"]
    for suffix in [".mp3", ".wav", ".m4a", ".aac"]:
        candidate = voice_dir / f"{segment['id']}{suffix}"
        if candidate.exists():
            return candidate
    return voice_dir / f"{segment['id']}.mp3"


def split_caption(text: str, max_chars: int) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    chunks: list[str] = []
    current = ""
    for character in text:
        current += character
        visible_length = len(normalized(current))
        if character in PUNCTUATION and visible_length >= max(5, max_chars // 3):
            chunks.append(current.strip())
            current = ""
        elif visible_length >= max_chars:
            chunks.append(current.strip())
            current = ""
    if current.strip():
        chunks.append(current.strip())
    return [chunk for chunk in chunks if chunk]


def flatten_words(asr_segments: list) -> list[TimedToken]:
    tokens: list[TimedToken] = []
    for segment in asr_segments:
        for word in getattr(segment, "words", None) or []:
            clean = normalized(word.word)
            if not clean:
                continue
            duration = max(0.01, float(word.end) - float(word.start))
            for index, character in enumerate(clean):
                start = float(word.start) + duration * index / len(clean)
                end = float(word.start) + duration * (index + 1) / len(clean)
                tokens.append(TimedToken(character, start, end))
    return tokens


def boundary_time(tokens: list[TimedToken], index: int, total_expected: int, at_end: bool) -> float:
    if not tokens:
        return 0.0
    if total_expected <= 0:
        return tokens[-1].end if at_end else tokens[0].start
    mapped = round(index / total_expected * len(tokens))
    if mapped <= 0:
        return tokens[0].start
    if mapped >= len(tokens):
        return tokens[-1].end
    return tokens[mapped - 1].end if at_end else tokens[mapped].start


def build_segment_cues(segment: dict, words: list[TimedToken], duration: float, max_chars: int) -> list[dict]:
    display_text = segment.get("subtitle") or segment["text"]
    chunks = split_caption(display_text, max_chars)
    if not chunks:
        return []
    total_expected = sum(len(normalized(chunk)) for chunk in chunks)
    cursor = 0
    cues: list[dict] = []
    global_start = float(segment["start"])
    for index, chunk in enumerate(chunks):
        chunk_length = len(normalized(chunk))
        local_start = boundary_time(words, cursor, total_expected, at_end=False) if words else duration * cursor / max(1, total_expected)
        cursor += chunk_length
        local_end = boundary_time(words, cursor, total_expected, at_end=True) if words else duration * cursor / max(1, total_expected)
        if index == 0:
            local_start = max(0.0, local_start)
        if index == len(chunks) - 1:
            local_end = min(duration, max(local_end, words[-1].end if words else duration))
        local_end = max(local_start + 0.12, min(duration, local_end))
        cues.append(
            {
                "id": f"sub-{segment['id']}-{index + 1:02d}",
                "segment_id": segment["id"],
                "start": round(global_start + local_start, 3),
                "end": round(global_start + local_end, 3),
                "text": chunk,
            }
        )
    for index in range(len(cues) - 1):
        cues[index]["end"] = min(cues[index]["end"], cues[index + 1]["start"])
    return cues


def srt_time(seconds: float) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_srt(path: Path, cues: list[dict]) -> None:
    blocks = []
    for index, cue in enumerate(cues, start=1):
        blocks.append(
            f"{index}\n{srt_time(float(cue['start']))} --> {srt_time(float(cue['end']))}\n{cue['text']}"
        )
    path.write_text("\n\n".join(blocks) + ("\n" if blocks else ""), encoding="utf-8")


def load_asr_model(name: str, device: str, compute_type: str):
    try:
        from faster_whisper import WhisperModel
    except ImportError as error:
        raise SystemExit(
            "faster-whisper is required. Install it in a project-local environment, for example: "
            "uv venv .asr-venv && uv pip install --python .asr-venv/bin/python faster-whisper"
        ) from error
    effective_compute = "default" if compute_type == "auto" else compute_type
    return WhisperModel(name, device=device, compute_type=effective_compute)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit narration and create word-timed subtitles")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--model", default="small")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--compute-type", default="auto")
    parser.add_argument("--language", default="")
    parser.add_argument("--threshold", type=float, default=0.90)
    parser.add_argument("--min-length-ratio", type=float, default=0.85)
    parser.add_argument("--max-chars", type=int, default=18)
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()

    project = args.project.expanduser().resolve()
    plan_path = project / "film-plan.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    narration_path = project / "narration.json"
    narration = (
        json.loads(narration_path.read_text(encoding="utf-8"))
        if narration_path.exists()
        else plan.get("narration", [])
    )
    if not narration:
        raise SystemExit("narration is empty")

    language = args.language or str(plan.get("meta", {}).get("language", "")).split("-")[0] or None
    model = load_asr_model(args.model, args.device, args.compute_type)
    records: list[dict] = []
    all_cues: list[dict] = []

    for segment in sorted(narration, key=lambda item: float(item["start"])):
        path = narration_file(project, plan, segment)
        expected = segment.get("text", "")
        if not path.exists() or path.stat().st_size == 0:
            records.append(
                {
                    "id": segment.get("id", "?"),
                    "file": str(path),
                    "expected": expected,
                    "transcript": "",
                    "similarity": 0.0,
                    "length_ratio": 0.0,
                    "passed": False,
                    "error": "audio file missing or empty",
                }
            )
            continue

        duration = audio_duration(path)
        asr_iterator, info = model.transcribe(
            str(path),
            language=language,
            word_timestamps=True,
            vad_filter=True,
            beam_size=5,
        )
        asr_segments = list(asr_iterator)
        transcript = "".join(item.text for item in asr_segments).strip()
        expected_norm = normalized(expected)
        actual_norm = normalized(transcript)
        similarity = difflib.SequenceMatcher(None, expected_norm, actual_norm).ratio() if expected_norm else 0.0
        length_ratio = min(len(expected_norm), len(actual_norm)) / max(1, max(len(expected_norm), len(actual_norm)))
        passed = similarity >= args.threshold and length_ratio >= args.min_length_ratio
        words = flatten_words(asr_segments)
        segment_cues = build_segment_cues(segment, words, duration, args.max_chars) if passed else []
        all_cues.extend(segment_cues)
        records.append(
            {
                "id": segment["id"],
                "file": str(path.relative_to(project)) if path.is_relative_to(project) else str(path),
                "expected": expected,
                "transcript": transcript,
                "similarity": round(similarity, 4),
                "length_ratio": round(length_ratio, 4),
                "duration": round(duration, 3),
                "detected_language": getattr(info, "language", language),
                "word_count": len(words),
                "cue_count": len(segment_cues),
                "passed": passed,
            }
        )
        segment["duration"] = round(duration, 3)
        segment["file"] = str(path.relative_to(project)) if path.is_relative_to(project) else str(path)
        print(f"segment={segment['id']} similarity={similarity:.3f} passed={passed}", flush=True)

    expected_ids = {str(item["id"]) for item in narration}
    audited_ids = {str(item["id"]) for item in records}
    complete = audited_ids == expected_ids and len(records) == len(narration)
    all_passed = complete and all(record.get("passed", False) for record in records)
    report = {
        "complete": complete,
        "all_passed": all_passed,
        "model": args.model,
        "device": args.device,
        "language": language,
        "threshold": args.threshold,
        "min_length_ratio": args.min_length_ratio,
        "segments": records,
    }

    transcript_dir = project / "qa" / "transcripts"
    subtitle_dir = project / "subtitles"
    transcript_dir.mkdir(parents=True, exist_ok=True)
    subtitle_dir.mkdir(parents=True, exist_ok=True)
    report_path = transcript_dir / "narration-audit.json"
    cue_path = subtitle_dir / "subtitle-cues.json"
    srt_path = subtitle_dir / "final.srt"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cue_path.write_text(json.dumps({"source": "final-audio-word-timestamps", "cues": all_cues}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_srt(srt_path, all_cues)

    plan["narration"] = narration
    plan["production"]["audio_locked"] = all_passed
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    narration_path.write_text(json.dumps(narration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"report={report_path}")
    print(f"subtitles={srt_path} cues={len(all_cues)} complete={complete} all_passed={all_passed}")
    if not all_passed and not args.report_only:
        raise SystemExit("narration audit failed; regenerate failed segments and rerun")


if __name__ == "__main__":
    main()
