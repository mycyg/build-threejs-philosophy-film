#!/usr/bin/env python3
"""Detect unexplained long freezes in a rendered film with ffmpeg freezedetect."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


EVENT_RE = re.compile(r"freeze_(start|end|duration):\s*([0-9.]+)")


def overlap_ratio(start: float, end: float, allowed: dict) -> float:
    left = max(start, float(allowed.get("start", 0)))
    right = min(end, float(allowed.get("end", 0)))
    return max(0.0, right - left) / max(0.001, end - start)


def parse_freezes(log: str, duration: float) -> list[dict]:
    freezes: list[dict] = []
    current: dict | None = None
    for match in EVENT_RE.finditer(log):
        kind, raw_value = match.groups()
        value = float(raw_value)
        if kind == "start":
            current = {"start": value}
        elif current is not None and kind == "duration":
            current["duration"] = value
        elif current is not None and kind == "end":
            current["end"] = value
            current.setdefault("duration", value - current["start"])
            freezes.append(current)
            current = None
    if current is not None:
        current["end"] = duration
        current.setdefault("duration", duration - current["start"])
        freezes.append(current)
    return freezes


def probe_duration(ffprobe: str, video: Path) -> float:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(video)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit rendered-film freezes")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--video", type=Path)
    parser.add_argument("--max-freeze", type=float, default=2.5)
    parser.add_argument("--noise", default="-45dB")
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()

    project = args.project.expanduser().resolve()
    plan = json.loads((project / "film-plan.json").read_text(encoding="utf-8"))
    video = args.video.expanduser().resolve() if args.video else project / plan["render"]["output_video"]
    if not video.exists():
        raise SystemExit(f"video not found: {video}")
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise SystemExit("ffmpeg and ffprobe are required")

    duration = probe_duration(ffprobe, video)
    result = subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-nostats",
            "-i",
            str(video),
            "-vf",
            f"freezedetect=noise={args.noise}:duration={args.max_freeze}",
            "-an",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "ffmpeg motion audit failed")

    allowed = plan.get("qa", {}).get("intentional_holds", [])
    freezes = parse_freezes(result.stderr, duration)
    unexpected = []
    for freeze in freezes:
        match = next((item for item in allowed if overlap_ratio(freeze["start"], freeze["end"], item) >= 0.9), None)
        freeze["intentional"] = bool(match)
        if match:
            freeze["reason"] = match.get("reason", "declared intentional hold")
        else:
            unexpected.append(freeze)

    report = {
        "complete": True,
        "passed": not unexpected,
        "video": str(video.relative_to(project)) if video.is_relative_to(project) else str(video),
        "duration": round(duration, 3),
        "threshold_seconds": args.max_freeze,
        "noise_threshold": args.noise,
        "freezes": freezes,
        "unexpected_freezes": unexpected,
    }
    output = project / "qa" / "motion-audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"report={output}")
    print(f"freezes={len(freezes)} unexpected={len(unexpected)} passed={report['passed']}")
    if unexpected and not args.report_only:
        raise SystemExit("unexpected long freezes detected; inspect qa/motion-audit.json")


if __name__ == "__main__":
    main()
