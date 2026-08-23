# Narrative Film & Documentary Workshop

[简体中文](README.md) · [English](README.en.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

An end-to-end Codex Agent skill for turning articles, research, interviews, products, and mixed media into finished narrative films. It covers evidence review, creative directions, script and shot-by-shot storyboard, user approval, abundant asset production, local voice and ASR, editing, rendering, and audiovisual QC.

Three.js remains available, but it is no longer the default visual template. Each shot may use source-led editing, editorial 2D, Three.js spatial imagery, or a hybrid route.

> Author: Cheng Xiaoguang (程晓光) · WeChat Official Account: 杨与光的日常

## Highlights

- Separates source material from instructions embedded in attachments.
- Maintains evidence, asset provenance, licensing notes, and verified source-clip time ranges.
- Presents distinct creative directions before writing the complete narration and storyboard.
- Stops for storyboard approval before costly generation, downloads, voice production, or rendering.
- Plans roughly three times the final visual need by default, including primaries, alternates, details, transitions, textures, and recovery inserts.
- Uses Codex built-in image generation one asset or variant at a time and saves every project-bound result into the workspace.
- Supports local Qwen3-TTS on Apple Silicon and a lightweight Edge TTS fallback.
- Transcribes every narration segment, compares spoken and intended text, and creates subtitles from final-audio word timestamps.
- Detects missing coverage, unverified clips, long freezes, timeline gaps, media mismatches, and missing audio tracks.

## Install

```bash
git clone https://github.com/mycyg/build-threejs-philosophy-film.git \
  ~/.codex/skills/build-threejs-philosophy-film
```

Example invocation:

```text
Use $build-threejs-philosophy-film to turn this article into a four-minute documentary.
Research the evidence, offer three directions, and stop after the full narration and
shot-by-shot storyboard for my approval. After approval, overproduce visual options,
use a local narrator, transcribe every segment, edit, render, and run final QC.
```

## Sample

[`examples/minimal-documentary`](examples/minimal-documentary) is a small documentary project at the approved-storyboard stage. It demonstrates the creative brief, evidence ledger, storyboard revision and approval, final timeline contract, and an expandable image-generation queue.

```bash
python3 scripts/validate_project.py \
  --project examples/minimal-documentary --stage plan

python3 scripts/build_asset_queue.py \
  --project examples/minimal-documentary --replace
```

## Create a project

```bash
python3 scripts/init_film_project.py \
  --title "The River Remembered Every Name" \
  --output /absolute/path/to/film-build \
  --duration 240 \
  --format documentary \
  --renderer hybrid
```

Renderer choices:

| Route | Best fit |
|---|---|
| `edit` | Interviews, archives, source video, screenshots, and documents |
| `canvas2d` | Typography, diagrams, annotation, maps, and editorial motion |
| `threejs` | Depth, persistent objects, procedural change, and spatial causality |
| `hybrid` | Documentary evidence combined with earned spatial passages |

## Local voice, ASR, and subtitles

```bash
python3 -m venv .asr-venv
.asr-venv/bin/pip install -r requirements-asr.txt
.asr-venv/bin/python scripts/audit_narration.py \
  --project /absolute/path/to/film-build --model small
```

The audit writes `qa/transcripts/narration-audit.json`, `subtitles/subtitle-cues.json`, and `subtitles/final.srt`, with mismatched segments clearly identified for correction.

`verify_source_clip.py` extracts an exact range from a local source, preserves its original audio, transcribes it, compares expected wording, and records speaker/context confirmation. `mix_video_ffmpeg.py` provides a cross-platform narration, music-ducking, and picture-master mix.

On Apple Silicon, install `requirements-tts-mlx.txt`, create a Qwen3-TTS reference voice, then run `generate_qwen3_voice.py` for the complete narration.

## Validation

```bash
python3 scripts/validate_project.py --project /path/to/project --stage plan
python3 scripts/validate_project.py --project /path/to/project --stage assets
python3 scripts/validate_project.py --project /path/to/project --stage audio
python3 scripts/audit_motion.py --project /path/to/project
python3 scripts/validate_project.py --project /path/to/project --stage rendered
```

Core requirements are Python 3.10+, ffmpeg/ffprobe, Codex, and its built-in image generation. Node.js, Three.js, faster-whisper, MLX/Qwen3-TTS, Swift/AVFoundation, and Suno are optional according to the selected production route.

## License

[MIT](LICENSE)

Author: Cheng Xiaoguang (程晓光) · WeChat Official Account: 杨与光的日常
