# Local models, narration audit, and subtitles

## Configuration

Record chosen engines in `local-models.json` so another Agent can reproduce the project:

```json
{
  "tts": {
    "engine": "qwen3-tts-mlx",
    "environment": ".tts-venv",
    "design_model": "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit",
    "production_model": "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit",
    "device": "apple-silicon"
  },
  "asr": {
    "engine": "faster-whisper",
    "model": "small",
    "device": "auto",
    "compute_type": "auto",
    "language": "zh"
  },
  "image": {
    "engine": "codex-built-in-imagegen",
    "local_fallback": null
  }
}
```

Do not download a large model, install a system service, or reconfigure an existing local model server without user authorization. Project-local Python environments are preferred.

## Qwen3-TTS on Apple Silicon

1. Create a project-local environment and install `mlx-audio`, `soundfile`, and `numpy`.
2. Put materially different narrator descriptions in `voice-profiles.json` under `sample_instructions`.
3. Run `generate_qwen3_voice.py --mode samples`.
4. Listen to complete samples and choose an original synthetic reference.
5. Set `reference_audio` and exact `reference_text`.
6. Run `generate_qwen3_voice.py --mode generate`.
7. Audit all outputs; batching can return plausible audio assigned to the wrong text, so file existence is not evidence of correctness.

Use `tts_text` for pronunciation spelling while keeping `subtitle` or `text` readable. Never solve bad pronunciation by corrupting the visible subtitle.

## Other local routes

On NVIDIA/Linux, a compatible PyTorch Qwen3-TTS or another configured local TTS engine may replace MLX. The film contract is engine-neutral: one file per segment, measured duration, role metadata, and a complete ASR audit.

Edge TTS is a low-resource fallback. Test its voice in context; availability and naturalness vary.

## Full ASR audit

Run `audit_narration.py` after every complete narration generation and after any regenerated segment. The audit should produce:

- expected script and actual transcript for every segment;
- normalized similarity and pass/fail;
- actual file duration;
- detected word timestamps;
- global subtitle cues and SRT;
- a complete flag covering all planned segments.

Do not accept spot checks for a final film. Listen manually to the opening, every voice change, all names and numbers, the densest passage, and the ending even after ASR passes.

## Subtitle timing

Use the final audio's word timestamps. Keep captions readable by chunking at punctuation and semantic boundaries, then enforce reasonable line length and minimum display time. A cue must not begin before its sound or remain on screen into unrelated speech.

Use intended subtitle text only when ASR confirms that the spoken audio matches it. If similarity fails, regenerate the voice; do not retime around the wrong words.

For authentic source clips, transcribe the exact extracted clip and create translation captions as a separate field. Keep source-language and translated text distinguishable in the project data.
