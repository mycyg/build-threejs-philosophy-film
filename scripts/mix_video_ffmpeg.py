#!/usr/bin/env python3
"""Cross-platform narration, music-ducking, and picture-master mux with ffmpeg."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def segment_file(project: Path, plan: dict, segment: dict) -> Path:
    if segment.get("file"):
        return project / segment["file"]
    return project / plan["audio"]["voice_dir"] / f"{segment['id']}.mp3"


def main() -> None:
    parser = argparse.ArgumentParser(description="Mix a narrative film with ffmpeg")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--picture", type=Path, help="override render.silent_video")
    parser.add_argument("--output", type=Path, help="override render.output_video")
    args = parser.parse_args()

    project = args.project.expanduser().resolve()
    plan = json.loads((project / "film-plan.json").read_text(encoding="utf-8"))
    duration = float(plan["meta"]["duration"])
    picture = args.picture.expanduser().resolve() if args.picture else project / plan["render"]["silent_video"]
    output = args.output.expanduser().resolve() if args.output else project / plan["render"]["output_video"]
    if not picture.exists():
        raise SystemExit(f"picture master not found: {picture}")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ffmpeg is required")

    music_value = plan["audio"].get("music_file")
    music = project / music_value if music_value else None
    if music and not music.exists():
        raise SystemExit(f"music file not found: {music}")
    narration = sorted(plan.get("narration", []), key=lambda item: float(item["start"]))
    voice_files = [(segment, segment_file(project, plan, segment)) for segment in narration]
    missing = [str(path) for _, path in voice_files if not path.exists()]
    if missing:
        raise SystemExit("missing narration files:\n" + "\n".join(missing))
    if not music and not voice_files:
        raise SystemExit("no music or narration is available to mix")

    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(picture)]
    input_index = 1
    music_index = None
    if music:
        music_index = input_index
        command.extend(["-stream_loop", "-1", "-i", str(music)])
        input_index += 1
    voice_indices: list[tuple[dict, int]] = []
    for segment, path in voice_files:
        voice_indices.append((segment, input_index))
        command.extend(["-i", str(path)])
        input_index += 1

    filters: list[str] = []
    voice_labels: list[str] = []
    for offset, (segment, index) in enumerate(voice_indices):
        delay = max(0, round(float(segment["start"]) * 1000))
        label = f"v{offset}"
        filters.append(
            f"[{index}:a]adelay=delays={delay}:all=1,atrim=duration={duration:.3f},asetpts=N/SR/TB[{label}]"
        )
        voice_labels.append(f"[{label}]")

    voice_mix = None
    if voice_labels:
        voice_mix = "voice"
        if len(voice_labels) == 1:
            filters.append(f"{voice_labels[0]}anull[{voice_mix}]")
        else:
            filters.append(
                f"{''.join(voice_labels)}amix=inputs={len(voice_labels)}:normalize=0:dropout_transition=0[{voice_mix}]"
            )

    if music_index is not None:
        base = float(plan["audio"].get("music_base", 0.19))
        filters.append(
            f"[{music_index}:a]atrim=duration={duration:.3f},asetpts=N/SR/TB,volume={base:.5f}[music]"
        )
        if voice_mix:
            filters.append(f"[{voice_mix}]asplit=2[sidechain][voiceout]")
            filters.append(
                "[music][sidechain]sidechaincompress=threshold=0.015:ratio=10:attack=50:release=850[ducked]"
            )
            filters.append("[ducked][voiceout]amix=inputs=2:normalize=0,alimiter=limit=0.95[aout]")
        else:
            filters.append("[music]alimiter=limit=0.95[aout]")
    elif voice_mix:
        filters.append(f"[{voice_mix}]alimiter=limit=0.95[aout]")

    output.parent.mkdir(parents=True, exist_ok=True)
    command.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            "0:v:0",
            "-map",
            "[aout]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "256k",
            "-t",
            f"{duration:.3f}",
            "-movflags",
            "+faststart",
            "-metadata",
            f"title={plan['meta']['title']}",
            str(output),
        ]
    )
    subprocess.run(command, check=True)
    print(f"final={output}")
    print(f"duration={duration:.3f} narration={len(voice_files)} music={'yes' if music else 'no'}")


if __name__ == "__main__":
    main()
