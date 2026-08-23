# ALETHEIA

### Let the Article Pass Through Time

[简体中文](README.md) · [English](README.en.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

**Open-source Codex article-to-video Skill｜AI documentary, cinematic essay, and end-to-end video production workflow**

ALETHEIA helps Codex turn articles, blog posts, papers, research, interviews, product documents, and mixed media into videos. It covers evidence review, creative direction, scripting, shot-by-shot storyboards, approval, abundant AI image generation, local narration, ASR-aligned subtitles, editing, Three.js / Canvas2D rendering, music mixing, and final QC—for documentaries, video essays, philosophy films, product films, and YouTube or Bilibili production.

> “So ist denn auch das Wesen der Technik ganz und gar nichts Technisches.”
>
> — Martin Heidegger, [*The Question Concerning Technology*](https://www.beyng.com/pages/de/GA07/GA07.007.html)

The Greek `Aletheia` (ἀλήθεια) is usually translated as “truth.” Heidegger reopens it as *unconcealment*: what was hidden steps back into view.

An article loses the safety of the page when it enters the screen. Sentences must pass through a voice. Arguments must survive the camera. Judgments must endure the gaze of evidence. Film becomes a second act of writing.

It carries the source into time and gives it the structure of a finished film. Evidence, script, storyboard, assets, voice, subtitles, and the final edit remain inside one traceable project.

**Author: Cheng Xiaoguang (程晓光)｜WeChat Official Account: 杨与光的日常**

## Prologue: The Question Concerning Technology

### — No engine should inherit the shepherd’s staff of taste

For Heidegger, technology is a mode of revealing: it governs how something comes into presence. A renderer does the same. Make Three.js the unquestioned default and, eventually, every essay is compressed into particles, cards, dark space, and the same slow camera drift. The tool has become an enframing.

ALETHEIA keeps four routes open. The subject—and each individual shot—gets to choose.

| Route | What it lets appear |
|---|---|
| `edit` | The force of interviews, archives, source video, screenshots, and documents |
| `canvas2d` | Typography, diagrams, annotation, maps, timelines, and editorial motion |
| `threejs` | Depth, persistent objects, procedural change, and spatial causality |
| `hybrid` | Tension between documentary evidence and spatial imagery |

Three.js remains in the toolbox and enters when space has earned a role. The film’s visual grammar grows from its material instead of a house template.

## Act I: *Tractatus Logico-Philosophicus*

### — A proposition enters the image; an argument faces the camera

> “Der Satz ist ein Bild der Wirklichkeit.”
>
> — Ludwig Wittgenstein, [*Tractatus* 4.01](https://moenarch.github.io/wittgenstein-tractatus-logico-philosophicus/Satz%204.html)

Wittgenstein’s “picture” concerns a logical form shared by proposition and fact. On the edit, every sentence also needs a visible form: a claim finds evidence; an emotion finds action; an abstraction finds an event; a quotation finds its source; a human voice finds its exact timecode.

The project begins with an evidence ledger, then proposes genuinely distinct creative directions. Production pauses after the complete narration and shot-by-shot storyboard. A storyboard is a contract with time. Expensive generation, downloads, voice work, and rendering begin after that contract is approved.

### Production arc

1. Import articles, attachments, webpages, interviews, video, and code; map facts and claims.
2. Bind claims, quotations, speakers, source audio, and provenance in an evidence ledger.
3. Offer 2–3 narrative directions and settle the film’s thought, voice, and visual motif.
4. Write the complete narration, script, and shot-by-shot storyboard.
5. **Wait for storyboard approval.**
6. Expand the asset queue; generate, collect, screen, and register abundant candidates.
7. Create voice, transcribe every segment locally, and time subtitles to the final audio.
8. Choose editing, Canvas2D, Three.js, or a hybrid route shot by shot.
9. Finish a representative passage, then the full cut, score, and mix.
10. Audit subtitles, spoken text, long freezes, shot boundaries, media parameters, and the final master.

## Act II: *Creative Evolution*

### — Time has never flowed at a frame rate

> “Duration is the continuous progress of the past which gnaws into the future and which swells as it advances.”
>
> — Henri Bergson, [*Creative Evolution*](https://dhspriory.org/kenny/PhilTexts/Bergson/CreativeEvolution.htm)

Twenty-four frames per second is a ruler. The time a viewer actually feels is made of breath, silence, cadence, memory, and change within the frame. Bergson called this lived time *durée*.

Narration first becomes real audio and is then transcribed segment by segment. Subtitle timing comes from final-audio word timestamps, never from a character-count estimate. Shot duration returns to voice, action, and visual density. Motion audits catch frames that linger without inner change, making room for reframing, detail motion, alternates, or recovery inserts.

The local voice chain includes Qwen3-TTS MLX on Apple Silicon, an Edge TTS fallback, faster-whisper transcription, spoken-text comparison, final-audio subtitle cues, and a cross-platform narration/music/picture mix.

One line for the edit suite: **When subtitles guess time from character counts, the voice eventually betrays the picture.**

## Act III: *On the Concept of History*

### — The archive flashes past; the edit must catch its fingerprints

> “Das wahre Bild der Vergangenheit huscht vorbei.”
>
> — Walter Benjamin, [*On the Concept of History*, V](https://www.textlog.de/benjamin/abhandlungen/ueber-den-begriff-der-geschichte)

Archives pin the film to a world that once happened. Generated images give abstract thought a place to dream. The edit preserves their different gravities: one answers “did this occur?”; the other asks “what might this idea look like?”

One image is enough for a poster and too little for an edit. The most expensive thing in an edit suite is often the absence of a second choice.

After storyboard approval, the asset queue plans roughly three times the final visual need: primaries, alternate compositions, recognition shots, details, transitions, textures, transformations, and recovery inserts. Each asset or variant is generated separately. Character, lens, light, and material continuity are kept within a visual family. Rejected candidates with possible rescue value remain in the ledger.

```bash
python3 scripts/build_asset_queue.py --project /absolute/path/to/film-build
```

Every `asset_need` becomes an independent task across axes such as `establishing`, `recognition`, `transformation`, `detail`, `transition`, `alternate composition`, and `recovery insert`. Codex built-in image generation then produces, inspects, and saves each project-bound asset.

## Act IV: *Cinema 1 / Cinema 2*

### — Movement connects; time leaves the afterimage

Deleuze used the movement-image and the time-image to think about cinema’s organization of perception. Movement joins action, cause, and space. Time allows hesitation, memory, and fracture to appear on their own. Some shots must clearly arrive at the next shot. Others only ask the viewer to remain one second longer.

ALETHEIA works with both kinds of time. Source-led editing carries people, history, and evidence. Canvas2D gives information a body in motion. Three.js enters passages that truly need depth and persistent space. A hybrid film can change its grammar from one chapter to the next.

The project preserves more than its master:

- complete narration, script, and shot-by-shot storyboard;
- the final timeline contract in `film-plan.json`;
- the evidence ledger in `evidence-ledger.json`;
- asset queues, primaries, alternates, and source-verification records;
- transcription audit, subtitle cues, and `final.srt`;
- freeze, boundary-frame, audio-track, and media-parameter reports;
- an editable production project.

## Install

```bash
git clone https://github.com/mycyg/aletheia.git \
  ~/.codex/skills/aletheia
```

Reopen Codex, then invoke the Skill in natural language or by name:

```text
Use $aletheia to turn this article into a four-minute documentary.
Research the evidence, offer three directions, and stop after the complete narration
and shot-by-shot storyboard for my approval. After approval, produce abundant visual
options, use a local narrator, transcribe every segment, edit, render, and run final QC.
```

## Sample: *The River Remembered Every Name*

[`examples/minimal-documentary`](examples/minimal-documentary) is a small documentary project held at the moment after storyboard approval and before asset production.

It demonstrates `creative-brief.json`, `storyboard.json`, `storyboard-approval.json`, `film-plan.json`, `evidence-ledger.json`, and an image-generation queue that can expand several candidates from every visual need.

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

## Local voice, ASR, and subtitles

```bash
python3 -m venv .asr-venv
.asr-venv/bin/pip install -r requirements-asr.txt
.asr-venv/bin/python scripts/audit_narration.py \
  --project /absolute/path/to/film-build --model small
```

The audit writes `qa/transcripts/narration-audit.json`, `subtitles/subtitle-cues.json`, and `subtitles/final.srt`.

On Apple Silicon:

```bash
python3 -m venv .tts-venv
.tts-venv/bin/pip install -r requirements-tts-mlx.txt
.tts-venv/bin/python scripts/generate_qwen3_voice.py \
  --project /absolute/path/to/film-build --mode samples
```

Choose a synthetic reference voice, then run `--mode generate` for the complete narration.

## Staged validation

```bash
python3 scripts/validate_project.py --project /path/to/project --stage plan
python3 scripts/validate_project.py --project /path/to/project --stage assets
python3 scripts/validate_project.py --project /path/to/project --stage audio
python3 scripts/audit_motion.py --project /path/to/project
python3 scripts/validate_project.py --project /path/to/project --stage rendered
```

Core requirements are Python 3.10+, ffmpeg/ffprobe, Codex Agent, and its built-in image generation. Node.js, Three.js, faster-whisper, MLX/Qwen3-TTS, Swift/AVFoundation, and Suno are selected according to the production route.

## Epilogue: The Second Writing

An article gives thought its first form. Film sends it through light, voice, evidence, and waiting. What returns has acquired another life.

## License

[MIT](LICENSE)

Author: Cheng Xiaoguang (程晓光)｜WeChat Official Account: 杨与光的日常
