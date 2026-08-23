#!/usr/bin/env python3
import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import edge_tts
    from edge_tts.exceptions import NoAudioReceived
except ImportError as error:
    uv = shutil.which("uv")
    if uv and not os.environ.get("THREEJS_FILM_VOICE_BOOTSTRAPPED"):
        environment = dict(os.environ)
        environment["THREEJS_FILM_VOICE_BOOTSTRAPPED"] = "1"
        os.execve(
            uv,
            [uv, "run", "--with", "edge-tts", "python", __file__, *sys.argv[1:]],
            environment,
        )
    raise SystemExit("edge-tts is unavailable and uv could not bootstrap it") from error


def duration_seconds(path: Path) -> float:
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        result = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
            check=True,
            capture_output=True,
            text=True,
        )
        return round(float(result.stdout.strip()), 3)
    afinfo = shutil.which("afinfo")
    if afinfo:
        result = subprocess.run([afinfo, str(path)], check=True, capture_output=True, text=True)
        match = re.search(r"estimated duration:\s*([0-9.]+) sec", result.stdout)
        if match:
            return round(float(match.group(1)), 3)
    raise RuntimeError(f"ffprobe or afinfo is required to read audio duration: {path}")


def spoken_text(segment: dict, profile: dict) -> str:
    text = segment.get("tts_text", segment["text"])
    for source, target in profile.get("pronunciations", {}).items():
        text = text.replace(source, target)
    return re.sub(r"\s+", " ", text).strip()


async def synthesize(segment: dict, profile: dict, destination: Path) -> None:
    for attempt in range(4):
        destination.unlink(missing_ok=True)
        speech = edge_tts.Communicate(
            spoken_text(segment, profile),
            profile["name"],
            rate=profile.get("rate", "+0%"),
            pitch=profile.get("pitch", "+0Hz"),
            volume=profile.get("volume", "+0%"),
        )
        try:
            await speech.save(destination)
            return
        except NoAudioReceived:
            if attempt == 3:
                raise
            await asyncio.sleep(1.5 * (attempt + 1))


async def main_async(project: Path) -> None:
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

    profiles = json.loads((project / "voice-profiles.json").read_text(encoding="utf-8"))
    voice_dir = project / plan["audio"]["voice_dir"]
    voice_dir.mkdir(parents=True, exist_ok=True)

    manifest_segments = []
    for segment in narration:
        role = segment["voice"]
        if role not in profiles:
            raise SystemExit(f"voice profile not found: {role}")
        destination = voice_dir / f'{segment["id"]}.mp3'
        await synthesize(segment, profiles[role], destination)
        duration = duration_seconds(destination)
        segment["duration"] = duration
        segment["file"] = str(destination.relative_to(project))
        manifest_segments.append(
            {
                "id": segment["id"],
                "voice": role,
                "file": str(destination.relative_to(project)),
                "duration": duration,
                "text": segment["text"],
                "tts_text": spoken_text(segment, profiles[role]),
            }
        )
        print(f"voice={segment['id']} duration={duration:.3f}")

    plan["narration"] = narration
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (voice_dir / "manifest.json").write_text(
        json.dumps({"profiles": profiles, "segments": manifest_segments}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"generated={len(narration)} output={voice_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate multi-role narration with Edge TTS")
    parser.add_argument("--project", type=Path, required=True)
    args = parser.parse_args()
    asyncio.run(main_async(args.project.expanduser().resolve()))


if __name__ == "__main__":
    main()
