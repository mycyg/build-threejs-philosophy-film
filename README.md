# ALETHEIA

### 让文章穿过时间

[简体中文](README.md) · [English](README.en.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

**开源 Codex 文章转视频 Skill｜AI 纪录片、叙事视频与完整视频制作工作流**

ALETHEIA 帮助 Codex 快速把文章、博客、论文、研究资料、采访、产品文档和混合素材转成视频。它覆盖资料核验、创意方向、脚本、逐镜分镜、用户确认、AI 批量生图、本地配音、ASR 字幕校对、剪辑、Three.js / Canvas2D 渲染、配乐混音与成片质检，可用于文章转视频、纪录片、视频论文、哲学短片、产品影片和 YouTube / Bilibili 内容制作。

> “技术的本质绝不是什么技术性的东西。”
>
> —— 马丁·海德格尔，[《技术的追问》](https://www.beyng.com/pages/de/GA07/GA07.007.html)

古希腊语 `Aletheia`（ἀλήθεια）通常译作“真理”；到了海德格尔那里，它被重新追问为“解蔽”：被遮住的事物，从阴影里重新显现。

一篇文章抵达屏幕时，会失去纸上的安稳。句子要经历声音，论证要经受镜头，判断要接受证据的凝视。影片由此成为第二次写作。

它把原稿送进时间，让材料长成一部真正能看的影片。证据、脚本、逐镜分镜、素材、声音、字幕与最终剪辑，都留在同一套可追溯工程里。

**作者：程晓光｜公众号：杨与光的日常**

## 序章：技术的追问

### ——引擎不该拥有审美的牧杖

海德格尔把技术理解为一种“解蔽”：它规定事物如何向我们显现。渲染器同样如此。默认套用 Three.js，久而久之，文章会被压成粒子、卡片、深色空间和同一种匀速运镜；工具悄悄变成了框架。

ALETHEIA 保留四条路线。选择权属于题材，也属于每一个镜头。

| 路线 | 它让什么显现 |
|---|---|
| `edit` | 采访、档案、原始视频、截图和文献自身的力量 |
| `canvas2d` | 文字、图表、批注、地图、时间线与编辑型运动 |
| `threejs` | 深度、持续物体、程序化变化与空间因果 |
| `hybrid` | 纪录片证据和空间化视觉之间的张力 |

Three.js 仍在工具箱里，需要空间时再让它出场。影片的视觉语法从文章内部生长，不接受单一模板的统治。

## 第一幕：逻辑哲学论

### ——命题进入图像，论证接受镜头的审判

> “命题是现实的一幅图画。”
>
> —— 路德维希·维特根斯坦，[《逻辑哲学论》4.01](https://moenarch.github.io/wittgenstein-tractatus-logico-philosophicus/Satz%204.html)

维特根斯坦所说的“图画”，关乎命题与事实共享的逻辑形式。搬到剪辑台上，一句话也应当找到自己的可见形式：主张找到证据，情绪找到动作，抽象概念找到事件，引文找到出处，人物原声找到准确的时间码。

工程先建立证据账本，再提出彼此真正有差异的创意方向。旁白和逐镜分镜完成后，制作停在确认点。分镜是一份时间契约；镜头尚未获得同意，昂贵的生成、下载、配音和渲染便没有理由先行。

### 制作闭环

1. 导入文章、附件、网页、采访、视频和代码，梳理事实与论点。
2. 建立证据账本，把主张、引文、人物、原声和来源逐项绑定。
3. 提出 2–3 个叙事方向，确认影片的思想、语气和视觉母题。
4. 写完整旁白、脚本与逐镜分镜。
5. **等待用户确认分镜。**
6. 展开素材队列，大量生成、抓取、筛选并登记候选素材。
7. 生成配音，用本地 ASR 逐段转写，按最终音频制作词级字幕。
8. 为每个镜头选择剪辑、Canvas2D、Three.js 或混合路线。
9. 先完成代表性片段，再推进全片、配乐与混音。
10. 检查字幕、音文、长静帧、镜头边界、媒体参数和最终封装。

## 第二幕：创造进化

### ——时间从来不按帧率流动

> “绵延，是过去不断侵入未来、并在前行中持续膨胀的过程。”
>
> —— 亨利·柏格森，[《创造进化》](https://dhspriory.org/kenny/PhilTexts/Bergson/CreativeEvolution.htm)

每秒 24 帧只是一把尺。影片里真正被感受到的时间，来自呼吸、停顿、句尾、记忆和画面内部的变化。柏格森称这种被生活出来的时间为“绵延”。

旁白先成为真实音频，随后接受逐段转写。字幕跟随最终声音的词级时间戳，不靠字符数猜测节奏。镜头时长也会回到声音、动作和素材密度上重新计算。长时间停在同一张图上的镜头会被运动审计捕获，随后通过局部变化、构图推进、替补素材或插镜获得新的呼吸。

本地声音链路包括：

- Apple Silicon 上的 Qwen3-TTS MLX；
- 轻量 Edge TTS 回退路线；
- faster-whisper 逐段转写与音文相似度检查；
- 基于最终音频的字幕 cue 与 SRT；
- 配音、音乐 ducking 和画面母版的跨平台混合。

一句可供剪辑台记住的话：**字幕若靠字符数猜时间，声音迟早会背叛画面。**

## 第三幕：历史哲学论纲

### ——档案一闪而过，剪辑要抓住它留下的指纹

> “过去的真实图像，一闪即逝。”
>
> —— 瓦尔特·本雅明，[《论历史的概念》第五节](https://www.textlog.de/benjamin/abhandlungen/ueber-den-begriff-der-geschichte)

档案负责把影片钉在曾经发生过的世界里；生成画面替抽象概念造梦。剪辑保留这两种图像各自的重量：前者回答“它真的发生过吗”，后者回答“这种思想看起来像什么”。

一张图只够做海报，不够剪片。剪辑台上最昂贵的东西，常常是没有第二个选择。

分镜确认后，素材队列会按镜头展开，默认准备约为成片所需三倍的候选量：主画面、替补构图、人物识别镜头、细节、转场、纹理、变化过程和救场插镜各自占位。每张资产与变体独立生成，人物、光线、镜头和材质在同组内保持连续。被淘汰却仍有救场价值的素材继续留在账本里。

```bash
python3 scripts/build_asset_queue.py --project /absolute/path/to/film-build
```

队列会把每个 `asset_need` 展开为独立任务，并加入 `establishing`、`recognition`、`transformation`、`detail`、`transition`、`alternate composition` 与 `recovery insert` 等变化轴。Codex 内置生图能力随后逐张完成生成、检查和入库。

## 第四幕：电影 1 / 电影 2

### ——运动负责连接，时间负责留下余波

德勒兹用“运动—影像”与“时间—影像”讨论电影如何组织感知。前者让动作、因果与空间彼此接续；后者容许停顿、记忆和裂缝自己显形。一个镜头有时需要清楚地走向下一个镜头，有时只需让观众在它面前多停留一秒。

这套工程同时照看两种时间。素材主导的剪辑处理人物、历史与证据；Canvas2D 负责文字和信息的运动；Three.js 处理真正需要深度与持续空间的段落；混合路线允许一部片在不同章节改变自身语法。

成片之外，工程还会留下：

- 完整旁白、脚本和逐镜分镜；
- `film-plan.json` 最终时间轴；
- `evidence-ledger.json` 证据账本；
- 素材队列、主选、替补与来源核验记录；
- 转写审计、字幕 cue 与 `final.srt`；
- 长静帧、镜头边界、音轨和媒体参数质检结果；
- 可继续修改的影片工程。

## 安装

```bash
git clone https://github.com/mycyg/aletheia.git \
  ~/.codex/skills/aletheia
```

重新打开 Codex 后，用自然语言调用，或显式写出 Skill 名称：

```text
Use $aletheia 把这篇文章做成一部 4 分钟的中文纪录片。
先整理证据，给我三个方向，完成旁白和逐镜分镜后等我确认。
确认后充分生成候选画面，并用本地模型配音和逐段转写校对。
```

## Sample：河流记得每一个名字

[`examples/minimal-documentary`](examples/minimal-documentary) 保存着一部停在“分镜已确认、素材即将量产”时刻的最小纪录片工程。

它包含：

- 记录已确认方向的 `creative-brief.json`；
- 写入镜头、声音、动作和素材需求的 `storyboard.json`；
- 固定确认状态与修订号的 `storyboard-approval.json`；
- 作为最终时间轴真相的 `film-plan.json`；
- 将论点绑定到来源的 `evidence-ledger.json`；
- 可一次展开多张候选画面的素材任务。

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

## 本地配音、转写与字幕

### ASR

```bash
python3 -m venv .asr-venv
.asr-venv/bin/pip install -r requirements-asr.txt

.asr-venv/bin/python scripts/audit_narration.py \
  --project /absolute/path/to/film-build --model small
```

审计结果写入：

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

选定合成参考声线后，运行 `--mode generate` 完成长篇旁白。

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

按制作路线选用：

- Node.js 与 npm：浏览器时间轴和 WebCodecs 模板
- Three.js：空间路线或混合路线中的必要镜头
- faster-whisper：旁白、采访原声与词级字幕校对
- MLX / Qwen3-TTS：Apple Silicon 本地配音
- Swift + AVFoundation：macOS 内置混音脚本
- Suno 或用户提供的音乐

## 工程地图

```text
SKILL.md                         Agent 制作流程
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

## 尾声：第二次写作

文章完成思想的第一次定形。影片让它经过光线、声音、证据与等待，回来时已经拥有另一种生命。

## License

[MIT](LICENSE)

作者：程晓光｜公众号：杨与光的日常
