#!/usr/bin/env python3
"""Validate narrative-film projects at plan, asset, audio, and rendered stages."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


STAGE_ORDER = {"plan": 0, "assets": 1, "audio": 2, "rendered": 3}
RENDERERS = {"hybrid", "threejs", "canvas2d", "edit"}
SCENE_FIELDS = [
    "id",
    "start",
    "end",
    "title",
    "narrative_function",
    "philosophy",
    "human_meaning",
    "evidence_ids",
    "visual_motif",
    "motion",
    "assets",
]


def load_json(path: Path, errors: list[str], required: bool = True) -> dict | list:
    if not path.exists():
        if required:
            errors.append(f"missing file: {path}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        errors.append(f"cannot read JSON {path}: {error}")
        return {}


def as_assets(ledger: dict | list) -> list[dict]:
    if isinstance(ledger, list):
        return ledger
    return ledger.get("assets", []) if isinstance(ledger, dict) else []


def media_info(path: Path) -> dict | None:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None
    result = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,width,height,r_frame_rate",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def rate(value: str) -> float:
    if "/" in value:
        numerator, denominator = value.split("/", 1)
        return float(numerator) / max(1.0, float(denominator))
    return float(value)


def segment_file(project: Path, plan: dict, segment: dict) -> Path:
    if segment.get("file"):
        return project / segment["file"]
    voice_dir = project / plan["audio"]["voice_dir"]
    for suffix in [".mp3", ".wav", ".m4a", ".aac"]:
        candidate = voice_dir / f"{segment['id']}{suffix}"
        if candidate.exists():
            return candidate
    return voice_dir / f"{segment['id']}.mp3"


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a narrative-film project")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--stage", choices=list(STAGE_ORDER), default="plan")
    parser.add_argument("--rendered", action="store_true", help="legacy alias for --stage rendered")
    args = parser.parse_args()
    stage = "rendered" if args.rendered else args.stage
    stage_level = STAGE_ORDER[stage]
    project = args.project.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    plan_path = project / "film-plan.json"
    plan = load_json(plan_path, errors)
    if not isinstance(plan, dict):
        errors.append("film-plan.json must contain an object")
        plan = {}
    required_top = ["meta", "production", "design", "credits", "audio", "render", "qa", "scenes", "narration"]
    for key in required_top:
        if key not in plan:
            errors.append(f"missing top-level field: {key}")
    if errors:
        raise SystemExit("\n".join(errors))

    meta = plan["meta"]
    duration = float(meta.get("duration", 0))
    if duration <= 0:
        errors.append("meta.duration must be positive")
    renderer = plan["production"].get("renderer")
    if renderer not in RENDERERS:
        errors.append(f"unsupported production.renderer: {renderer}")

    brief = load_json(project / "creative-brief.json", errors)
    if isinstance(brief, dict) and not brief.get("approved_by_user", False):
        errors.append("creative-brief.json is not approved")

    storyboard = load_json(project / "storyboard.json", errors)
    approval = load_json(project / "storyboard-approval.json", errors)
    shots = storyboard.get("shots", []) if isinstance(storyboard, dict) else []
    revision = int(storyboard.get("revision", 0)) if isinstance(storyboard, dict) else 0
    if not shots:
        errors.append("storyboard has no shots")
    if not isinstance(approval, dict) or not approval.get("approved", False):
        errors.append("storyboard is not approved")
    elif int(approval.get("storyboard_revision", -1)) != revision:
        errors.append("storyboard approval revision does not match storyboard.json")
    elif approval.get("mode") not in {"user-confirmed", "delegated"}:
        errors.append("storyboard approval mode must be user-confirmed or delegated")

    design = plan["design"]
    if not design.get("thesis"):
        errors.append("design.thesis is empty")
    typography = design.get("typography", {})
    if not typography.get("display") or not typography.get("text"):
        errors.append("project-specific typography is incomplete")
    for field in ["palette", "layout_principles"]:
        if not design.get(field):
            errors.append(f"project-specific design field is empty: {field}")
    for field in ["materials", "motion_verbs"]:
        if not design.get(field):
            warnings.append(f"project-specific design field is empty: {field}")

    design_source = project / "film-design.js"
    if renderer != "edit":
        if not design_source.exists():
            errors.append("film-design.js is missing for a web-rendered project")
        elif "UNAUTHORED FILM DESIGN" in design_source.read_text(encoding="utf-8"):
            message = "film-design.js is still the un-authored bootstrap stub"
            if stage_level >= STAGE_ORDER["rendered"]:
                errors.append(message)
            else:
                warnings.append(message)

    evidence_ledger = load_json(project / "source" / "evidence-ledger.json", errors)
    evidence_items = evidence_ledger.get("evidence", []) if isinstance(evidence_ledger, dict) else []
    evidence_ids = {str(item.get("id")) for item in evidence_items if item.get("id")}

    scenes = plan["scenes"]
    if not scenes:
        errors.append("film plan has no scenes")
    else:
        if abs(float(scenes[0].get("start", -1))) > 0.001:
            errors.append("first scene must start at 0")
        if abs(float(scenes[-1].get("end", -1)) - duration) > 0.001:
            errors.append("last scene must end at meta.duration")
        for index, scene in enumerate(scenes):
            scene_id = scene.get("id", index)
            for field in SCENE_FIELDS:
                if field not in scene:
                    errors.append(f"scene {scene_id} missing field: {field}")
            if float(scene.get("end", 0)) <= float(scene.get("start", 0)):
                errors.append(f"scene {scene_id} has non-positive duration")
            if index and abs(float(scene["start"]) - float(scenes[index - 1]["end"])) > 0.001:
                errors.append(f"scene boundary gap or overlap: {scenes[index - 1]['id']} -> {scene_id}")
            for evidence_id in scene.get("evidence_ids", []):
                if str(evidence_id) not in evidence_ids:
                    errors.append(f"scene {scene_id} references unknown evidence: {evidence_id}")

    narration = sorted(plan["narration"], key=lambda item: float(item.get("start", 0)))
    if not narration:
        warnings.append("film plan has no narration; valid only for intentionally nonverbal work")
    previous_end = 0.0
    spoken = 0.0
    narration_ids: set[str] = set()
    for segment in narration:
        segment_id = str(segment.get("id", "?"))
        if segment_id in narration_ids:
            errors.append(f"duplicate narration id: {segment_id}")
        narration_ids.add(segment_id)
        for field in ["id", "start", "voice", "text"]:
            if segment.get(field) in [None, ""]:
                errors.append(f"narration segment {segment_id} missing {field}")
        start = float(segment.get("start", -1))
        if start < 0 or start >= duration:
            errors.append(f"narration start outside film: {segment_id}")
        if "duration" in segment:
            item_duration = float(segment["duration"])
            end = start + item_duration
            spoken += item_duration
            if start < previous_end - 0.02:
                errors.append(f"narration overlap: {segment_id}")
            if end > duration + 0.05:
                errors.append(f"narration extends beyond film: {segment_id}")
            previous_end = max(previous_end, end)
    if narration and all("duration" in item for item in narration):
        occupancy = spoken / max(duration, 0.001)
        if occupancy < 0.45:
            warnings.append(f"spoken occupancy is sparse: {occupancy:.1%}")
        if occupancy > 0.90:
            warnings.append(f"spoken occupancy is very dense: {occupancy:.1%}")

    credits = plan["credits"]
    if not credits.get("speak_company", False) and credits.get("company"):
        for segment in narration:
            if segment.get("intent") == "credit" and credits["company"] in segment.get("text", ""):
                errors.append("credit narration speaks the company while speak_company is false")

    ledger = load_json(project / "assets" / "asset-ledger.json", errors if stage_level >= 1 else warnings)
    assets = as_assets(ledger)
    asset_by_id = {str(item.get("id")): item for item in assets if item.get("id")}

    if stage_level >= STAGE_ORDER["assets"]:
        for asset in assets:
            asset_id = asset.get("id", "?")
            if asset.get("status") not in {"candidate", "selected", "alternate", "rejected"}:
                errors.append(f"asset {asset_id} has invalid status")
            if asset.get("status") != "rejected":
                relative = asset.get("path")
                if not relative or not (project / relative).exists():
                    errors.append(f"asset file missing: {asset_id} -> {relative}")

        active_status = {"candidate", "selected", "alternate"}
        for shot in shots:
            shot_id = str(shot.get("id", "?"))
            for need in shot.get("asset_needs", []):
                role = str(need.get("role", "primary"))
                matching = [
                    asset
                    for asset in assets
                    if shot_id in [str(value) for value in asset.get("shot_ids", [])]
                    and str(asset.get("role")) == role
                    and asset.get("status") in active_status
                ]
                target = max(0, int(need.get("target_count", 0)))
                selected_min = max(0, int(need.get("selected_min", 0)))
                selected = [asset for asset in matching if asset.get("status") == "selected"]
                alternates = [asset for asset in matching if asset.get("status") == "alternate"]
                if len(matching) < target:
                    errors.append(f"asset shortage for {shot_id}/{role}: {len(matching)} of {target}")
                if len(selected) < selected_min:
                    errors.append(f"selected asset shortage for {shot_id}/{role}: {len(selected)} of {selected_min}")
                if target > 1 and not alternates:
                    errors.append(f"no alternate asset for {shot_id}/{role}")

        for scene in scenes:
            for reference in scene.get("assets", []):
                asset_id = reference.get("id") if isinstance(reference, dict) else str(reference)
                if asset_id in asset_by_id:
                    relative = asset_by_id[asset_id].get("path")
                    if not relative or not (project / relative).exists():
                        errors.append(f"scene asset file missing: {asset_id}")
                elif not (project / asset_id).exists():
                    errors.append(f"scene references unknown asset or path: {asset_id}")

        queue = load_json(project / "assets" / "generation-queue.json", warnings, required=False)
        if isinstance(queue, dict):
            pending = [job for job in queue.get("jobs", []) if job.get("status") == "pending"]
            if pending:
                warnings.append(f"generation queue still has {len(pending)} pending jobs")

        source_verification = load_json(project / "assets" / "source-verification.json", errors)
        verified_clips = {
            str(item.get("asset_id"))
            for item in source_verification.get("clips", [])
            if item.get("verified") is True
        } if isinstance(source_verification, dict) else set()
        for asset in assets:
            if asset.get("kind") in {"source-video", "source-audio", "interview-clip", "speech-clip"} and asset.get("status") in {"selected", "alternate"}:
                if str(asset.get("id")) not in verified_clips:
                    errors.append(f"selected source clip is not verified: {asset.get('id')}")

    if stage_level >= STAGE_ORDER["audio"]:
        for segment in narration:
            path = segment_file(project, plan, segment)
            if not path.exists() or path.stat().st_size == 0:
                errors.append(f"voice file missing: {path}")
            if "duration" not in segment:
                errors.append(f"narration duration missing after synthesis: {segment.get('id')}")

        audit = load_json(project / "qa" / "transcripts" / "narration-audit.json", errors)
        if not isinstance(audit, dict) or not audit.get("complete"):
            errors.append("narration audit is incomplete")
        if not isinstance(audit, dict) or not audit.get("all_passed"):
            errors.append("one or more narration segments failed ASR audit")
        audited_ids = {
            str(item.get("id")) for item in audit.get("segments", []) if item.get("passed")
        } if isinstance(audit, dict) else set()
        if narration_ids != audited_ids:
            errors.append("ASR audit does not cover exactly the planned narration segments")
        for relative in ["subtitles/subtitle-cues.json", "subtitles/final.srt"]:
            path = project / relative
            if not path.exists() or path.stat().st_size == 0:
                errors.append(f"subtitle artifact missing: {relative}")
        if not plan["production"].get("audio_locked", False):
            errors.append("production.audio_locked is false")

    if stage_level >= STAGE_ORDER["rendered"]:
        music_file = plan["audio"].get("music_file")
        if music_file:
            music_path = project / music_file
            if not music_path.exists() or music_path.stat().st_size == 0:
                errors.append(f"declared music file missing: {music_file}")
        if renderer != "edit":
            silent_path = project / plan["render"]["silent_video"]
            if not silent_path.exists() or silent_path.stat().st_size == 0:
                errors.append(f"silent render missing: {silent_path}")
        final_path = project / plan["render"]["output_video"]
        if not final_path.exists() or final_path.stat().st_size == 0:
            errors.append(f"final render missing: {final_path}")
        else:
            info = media_info(final_path)
            if info:
                streams = info.get("streams", [])
                kinds = {stream.get("codec_type") for stream in streams}
                if not {"video", "audio"}.issubset(kinds):
                    errors.append("final video must contain video and audio tracks")
                video = next((stream for stream in streams if stream.get("codec_type") == "video"), {})
                if int(video.get("width", 0)) != int(meta["width"]) or int(video.get("height", 0)) != int(meta["height"]):
                    errors.append("final video dimensions do not match film-plan.json")
                actual_duration = float(info["format"]["duration"])
                if abs(actual_duration - duration) > 0.25:
                    errors.append(f"final duration mismatch: {actual_duration:.3f}s")
                actual_fps = rate(str(video.get("r_frame_rate", "0")))
                if abs(actual_fps - float(meta["fps"])) > 0.05:
                    errors.append(f"final frame rate mismatch: {actual_fps:.3f}")
            else:
                warnings.append("ffprobe unavailable; final media metadata check skipped")

        motion = load_json(project / "qa" / "motion-audit.json", errors)
        if not isinstance(motion, dict) or not motion.get("complete") or not motion.get("passed"):
            errors.append("motion audit is missing, incomplete, or failed")
        contact_sheets = list((project / "qa" / "contact-sheets").glob("*"))
        if not [path for path in contact_sheets if path.is_file() and path.stat().st_size > 0]:
            warnings.append("no contact sheet found")

    for warning in warnings:
        print(f"warning={warning}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"valid={project}")
    print(f"stage={stage} scenes={len(scenes)} shots={len(shots)} narration={len(narration)} duration={duration:.3f}")


if __name__ == "__main__":
    main()
