from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SAMPLE = ROOT / "examples" / "minimal-documentary"


def load_script(name: str):
    path = SCRIPTS / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return module


class PipelineTests(unittest.TestCase):
    def test_initializer_is_style_neutral(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "film"
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "init_film_project.py"),
                    "--title",
                    "Test Film",
                    "--output",
                    str(project),
                    "--duration",
                    "30",
                    "--renderer",
                    "canvas2d",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            plan = json.loads((project / "film-plan.json").read_text(encoding="utf-8"))
            self.assertEqual(plan["production"]["renderer"], "canvas2d")
            self.assertEqual(plan["scenes"], [])
            self.assertTrue((project / "storyboard-approval.json").exists())
            self.assertTrue((project / "subtitles").is_dir())
            self.assertIn("UNAUTHORED FILM DESIGN", (project / "film-design.js").read_text(encoding="utf-8"))

    def test_sample_plan_validates(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "validate_project.py"),
                "--project",
                str(SAMPLE),
                "--stage",
                "plan",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("stage=plan", result.stdout)

    def test_asset_queue_expands_all_generated_needs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "sample"
            shutil.copytree(SAMPLE, project)
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "build_asset_queue.py"),
                    "--project",
                    str(project),
                    "--replace",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            queue = json.loads((project / "assets" / "generation-queue.json").read_text(encoding="utf-8"))
            ids = [job["id"] for job in queue["jobs"]]
            self.assertEqual(len(ids), 12)
            self.assertEqual(len(ids), len(set(ids)))
            self.assertTrue(all(job["status"] == "pending" for job in queue["jobs"]))
            self.assertEqual(queue["imagegen_route"], "codex-built-in-imagegen")

    def test_asset_stage_enforces_and_accepts_surplus_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "sample"
            shutil.copytree(SAMPLE, project)
            storyboard = json.loads((project / "storyboard.json").read_text(encoding="utf-8"))
            assets = []
            for shot in storyboard["shots"]:
                for need in shot["asset_needs"]:
                    for index in range(need["target_count"]):
                        asset_id = f"asset-{shot['id']}-{need['role']}-{index + 1:02d}"
                        path = Path("assets") / "generated" / f"{asset_id}.bin"
                        (project / path).parent.mkdir(parents=True, exist_ok=True)
                        (project / path).write_bytes(b"sample")
                        status = "selected" if index == 0 else "alternate" if index == 1 else "candidate"
                        assets.append(
                            {
                                "id": asset_id,
                                "kind": need["kind"],
                                "path": str(path),
                                "shot_ids": [shot["id"]],
                                "role": need["role"],
                                "status": status,
                                "source": "test",
                                "license": "test",
                                "verified": True,
                            }
                        )
            ledger_path = project / "assets" / "asset-ledger.json"
            ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
            ledger["assets"] = assets
            ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_project.py"), "--project", str(project), "--stage", "assets"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("stage=assets", result.stdout)

    def test_caption_chunking_keeps_text(self) -> None:
        audit = load_script("audit_narration.py")
        text = "河流继续向前，记录让责任留下名字。"
        chunks = audit.split_caption(text, 8)
        self.assertEqual("".join(chunks), text)
        self.assertGreater(len(chunks), 1)

    def test_motion_log_parser(self) -> None:
        motion = load_script("audit_motion.py")
        log = "freeze_start: 1.2\nfreeze_duration: 3.4\nfreeze_end: 4.6\n"
        freezes = motion.parse_freezes(log, 10.0)
        self.assertEqual(len(freezes), 1)
        self.assertAlmostEqual(freezes[0]["duration"], 3.4)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg is unavailable")
    def test_cross_platform_mixer_outputs_audio_and_video(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "render").mkdir()
            (project / "voice").mkdir()
            subprocess.run(
                [
                    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-f", "lavfi", "-i", "color=c=black:s=320x180:r=24:d=2",
                    "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(project / "render" / "silent.mp4"),
                ],
                check=True,
            )
            subprocess.run(
                [
                    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-f", "lavfi", "-i", "sine=frequency=440:duration=0.6",
                    "-c:a", "libmp3lame", str(project / "voice" / "line.mp3"),
                ],
                check=True,
            )
            plan = {
                "meta": {"title": "Mixer Test", "duration": 2},
                "audio": {"music_file": "", "voice_dir": "voice", "music_base": 0.19, "music_duck": 0.05},
                "render": {"silent_video": "render/silent.mp4", "output_video": "render/final.mp4"},
                "narration": [{"id": "line", "start": 0.2, "text": "test", "file": "voice/line.mp3"}],
            }
            (project / "film-plan.json").write_text(json.dumps(plan), encoding="utf-8")
            subprocess.run(
                [sys.executable, str(SCRIPTS / "mix_video_ffmpeg.py"), "--project", str(project)],
                check=True,
                capture_output=True,
                text=True,
            )
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "json", str(project / "render" / "final.mp4")],
                check=True,
                capture_output=True,
                text=True,
            )
            kinds = {stream["codec_type"] for stream in json.loads(probe.stdout)["streams"]}
            self.assertEqual(kinds, {"video", "audio"})


if __name__ == "__main__":
    unittest.main()
