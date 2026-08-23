# 叙事影片与纪录片工坊

[简体中文](README.md) · [English](README.en.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

一个面向 Codex Agent 的完整影片制作 Skill：从文章、研究资料、采访、产品或混合素材出发，完成事实整理、创意方向、脚本、逐镜分镜、用户确认、批量素材准备、配音与转写校对、剪辑渲染和成片质检。

它仍然支持 Three.js，但不会把每部片都套进同一种 3D 模板。每个镜头可以选择素材主导剪辑、编辑型 2D、Three.js 空间影像或混合路线。

> 作者：程晓光 ｜ 公众号：杨与光的日常

## 它解决什么问题

- 导入文章、附件、视频、网页证据和代码，区分原始内容与附件中的指令。
- 建立证据账本，核对引文、采访原声、人物、语言与时间码。
- 提供 2–3 个真正不同的创作方向，再写完整旁白和逐镜分镜。
- 分镜完成后暂停，等待用户确认；也支持用户预先选择连续执行。
- 按分镜展开大规模素材队列。默认准备约为成片所需三倍的候选素材，主画面、替补、细节、转场、纹理和救场插镜分开规划。
- 充分调用 Codex 内置生图能力：每张不同资产或变体独立生成，成组维持人物、镜头、光线与材质连续性。
- 配置本地 TTS / ASR。Apple Silicon 可使用 Qwen3-TTS MLX；旁白完成后逐段转写，字幕由最终音频的词级时间戳生成。
- 检测音文不符、漏段、错误素材、长时间静帧、时间轴断裂、分辨率与音轨问题。
- 输出成片、SRT、分镜、film plan、素材账本、来源核验记录和可编辑工程。

## 制作闭环

1. 导入并审阅原始资料。
2. 建立证据与素材来源账本。
3. 提出创意方向并确认。
4. 写旁白、脚本和逐镜分镜。
5. **等待用户确认分镜。**
6. 展开素材队列并大量生成、抓取、筛选素材。
7. 生成配音；用本地 ASR 全量核对；生成词级字幕时间轴。
8. 按镜头选择素材剪辑、Canvas2D、Three.js 或混合渲染。
9. 先做代表性片段，再完成全片剪辑、配乐与混音。
10. 做静帧检测、联系表、边界帧、字幕、声音与媒体参数质检。

## 安装

```bash
git clone https://github.com/mycyg/build-threejs-philosophy-film.git \
  ~/.codex/skills/build-threejs-philosophy-film
```

重新打开 Codex 后，用自然语言调用，或显式写出 Skill 名称：

```text
Use $build-threejs-philosophy-film 把这篇文章做成一部 4 分钟的中文纪录片。
先整理证据，给我三个方向，完成旁白和逐镜分镜后等我确认。
确认后充分生成候选画面，并用本地模型配音和逐段转写校对。
```

## Sample

仓库内置一个处于“分镜已确认、尚未量产素材”阶段的最小纪录片工程：

[`examples/minimal-documentary`](examples/minimal-documentary)

它演示了：

- `creative-brief.json` 如何记录已确认的方向；
- `storyboard.json` 如何写镜头、声音、动作和素材需求；
- `storyboard-approval.json` 如何固定确认状态与修订号；
- `film-plan.json` 如何成为最终时间轴真相；
- `evidence-ledger.json` 如何把论点绑定到来源；
- 如何从分镜一次展开多张候选图片任务。

验证 Sample：

```bash
python3 scripts/validate_project.py \
  --project examples/minimal-documentary --stage plan
```

重新生成 Sample 的生图队列：

```bash
python3 scripts/build_asset_queue.py \
  --project examples/minimal-documentary --replace
```

## 新建工程

```bash
python3 scripts/init_film_project.py \
  --title "河流记得每一个名字" \
  --output /absolute/path/to/film-build \
  --duration 240 \
  --format documentary \
  --renderer hybrid
```

可选渲染路线：

| 路线 | 适用情况 |
|---|---|
| `edit` | 采访、档案、原始视频、截图和文献主导 |
| `canvas2d` | 文字、图表、批注、地图、时间线与编辑型运动 |
| `threejs` | 深度、持续物体、程序化变化、空间因果确实重要 |
| `hybrid` | 纪录片证据与空间化视觉共同构成叙事 |

## 素材量产

分镜批准后运行：

```bash
python3 scripts/build_asset_queue.py --project /absolute/path/to/film-build
```

生成器会把每个 `asset_need` 展开为独立任务，并自动加入 establishing、recognition、transformation、detail、transition、alternate composition、recovery insert 等变化轴。Agent 随后使用 Codex 内置 `image_gen` 逐张生成、检查并保存到工程目录。

素材校验关注候选数量、主选数量与替补数量，避免一个镜头只拿到一张勉强可用的图。被淘汰但仍可能救场的素材保留在账本中，不计入可用覆盖率。

## 本地配音与转写

### ASR

```bash
python3 -m venv .asr-venv
.asr-venv/bin/pip install -r requirements-asr.txt

.asr-venv/bin/python scripts/audit_narration.py \
  --project /absolute/path/to/film-build --model small
```

该脚本会转写每个旁白文件，比较预期文字与实际语音，输出：

- `qa/transcripts/narration-audit.json`
- `subtitles/subtitle-cues.json`
- `subtitles/final.srt`

### Apple Silicon 上的 Qwen3-TTS

```bash
python3 -m venv .tts-venv
.tts-venv/bin/pip install -r requirements-tts-mlx.txt

.tts-venv/bin/python scripts/generate_qwen3_voice.py \
  --project /absolute/path/to/film-build --mode samples
```

选择合成参考声线后，再运行 `--mode generate` 完成长篇旁白。

## 分阶段校验

```bash
python3 scripts/validate_project.py --project /path/to/project --stage plan
python3 scripts/validate_project.py --project /path/to/project --stage assets
python3 scripts/validate_project.py --project /path/to/project --stage audio
python3 scripts/audit_motion.py --project /path/to/project
python3 scripts/validate_project.py --project /path/to/project --stage rendered
```

## 依赖

基础功能：

- Python 3.10+
- ffmpeg / ffprobe
- Codex Agent 与内置图片生成能力

按需使用：

- Node.js 与 npm：浏览器时间轴和 WebCodecs 模板
- Three.js：仅用于空间路线或混合路线中的必要镜头
- faster-whisper：旁白与采访原声校对、词级字幕
- MLX / Qwen3-TTS：Apple Silicon 本地配音
- Swift + AVFoundation：macOS 下的内置混音脚本
- Suno 或用户提供的音乐：可选

## 目录

```text
SKILL.md                         Agent 工作流
references/                     分镜、素材、渲染、配音与质检规范
scripts/init_film_project.py    初始化中性工程
scripts/build_asset_queue.py    从分镜展开素材任务
scripts/generate_qwen3_voice.py 本地 Qwen3-TTS
scripts/generate_voice.py       Edge TTS 轻量回退
scripts/audit_narration.py      全量 ASR 与字幕时间轴
scripts/verify_source_clip.py   原声采访截取与核验
scripts/mix_video_ffmpeg.py     跨平台配音、配乐与画面合成
scripts/audit_motion.py         长时间静帧检测
scripts/validate_project.py     分阶段工程校验
assets/film-template/           无固定美术风格的确定性网页运行时
examples/minimal-documentary/   最小预制作 Sample
```

## License

[MIT](LICENSE)

作者：程晓光 ｜ 公众号：杨与光的日常
