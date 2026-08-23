# ALETHEIA

### 文章を、時間のなかへ

[简体中文](README.md) · [English](README.en.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

**オープンソース Codex 記事動画化 Skill｜AI ドキュメンタリー、映像エッセイ、映像制作ワークフロー**

ALETHEIA は、記事、ブログ、論文、調査資料、インタビュー、製品資料、混合素材を Codex で素早く動画へ変える article-to-video Skill だ。証拠確認、創作方針、脚本、ショット単位の絵コンテ、承認、AI 画像の大量生成、ローカル音声、ASR 字幕照合、編集、Three.js / Canvas2D レンダリング、音楽ミックス、完成映像の品質検査までを扱い、ドキュメンタリー、映像論文、哲学短編、製品映像、YouTube / Bilibili 制作に利用できる。

> 「技術の本質は、決して技術的なものではない。」
>
> —— マルティン・ハイデガー，[『技術への問い』](https://www.beyng.com/pages/de/GA07/GA07.007.html)

ギリシア語の `Aletheia`（ἀλήθεια）は通常「真理」と訳される。ハイデガーはそこに「覆いが外れること」を読み直した。隠れていたものが、ふたたび姿を現す。

文章はスクリーンに入った瞬間、紙の上の安定を失う。文は声を通り、論証はカメラに耐え、判断は証拠の視線を受ける。映画は、第二の執筆になる。

原稿を時間のなかへ送り込み、一本の観られる映画へ育てる。証拠、脚本、絵コンテ、素材、音声、字幕、最終編集は、追跡可能なひとつのプロジェクトに残る。

**作者：程晓光｜WeChat 公式アカウント：杨与光的日常**

## 序章：技術への問い

### ——エンジンに、美的判断の杖を渡さない

ハイデガーにとって技術とは、事物をある仕方で現れさせる「開示」だった。レンダラーもまた、映像が何として現れるかを決める。Three.js を無条件の既定値にすれば、やがてどの記事も、粒子、カード、暗い空間、同じ速度のカメラ移動へ押し込まれていく。道具が枠組みに変わる瞬間だ。

ALETHEIA は四つの経路を開いておく。選ぶのは題材であり、ひとつひとつのショットである。

| 経路 | 何を現れさせるか |
|---|---|
| `edit` | インタビュー、アーカイブ、元映像、スクリーンショット、文献の力 |
| `canvas2d` | タイポグラフィ、図表、注釈、地図、年表、編集的モーション |
| `threejs` | 奥行き、持続する物体、手続き的変化、空間的な因果 |
| `hybrid` | ドキュメンタリーの証拠と空間イメージの緊張 |

Three.js は道具箱に残る。空間が必要になった場面で、はじめて登場する。映像の文法は素材の内側から育ち、単一テンプレートには従わない。

## 第一幕：論理哲学論考

### ——命題が像に入り、論証がカメラの審判を受ける

> 「命題は現実の像である。」
>
> —— ルートヴィヒ・ヴィトゲンシュタイン，[『論理哲学論考』4.01](https://moenarch.github.io/wittgenstein-tractatus-logico-philosophicus/Satz%204.html)

ヴィトゲンシュタインの「像」は、命題と事実が共有する論理形式に関わる。編集卓の上でも、言葉には見える形式が要る。主張には証拠を、感情には行為を、抽象概念には出来事を、引用には出典を、人の声には正確なタイムコードを与える。

プロジェクトは証拠台帳から始まり、互いに明確に異なる創作方向を提示する。完全なナレーションとショット単位の絵コンテができたところで、制作は承認を待つ。絵コンテは時間との契約だ。高コストな生成、取得、音声制作、レンダリングは、契約が結ばれてから動き出す。

### 制作の環

1. 記事、添付資料、ウェブページ、インタビュー、映像、コードを読み込み、事実と主張を整理する。
2. 主張、引用、話者、原音、出典を証拠台帳に結びつける。
3. 2–3 の物語方向を提示し、思想、声、視覚モチーフを決める。
4. 完全なナレーション、脚本、ショット単位の絵コンテを書く。
5. **絵コンテの承認を待つ。**
6. 素材キューを展開し、十分な候補を生成・収集・選別・記録する。
7. ナレーションを生成し、ローカル ASR で全区間を書き起こし、最終音声から字幕を作る。
8. ショットごとに編集、Canvas2D、Three.js、ハイブリッドを選ぶ。
9. 代表シーンを先に完成させ、全編、音楽、ミックスへ進む。
10. 字幕、音文一致、長い静止、ショット境界、メディア情報、最終マスターを検査する。

## 第二幕：創造的進化

### ——時間はフレームレートでは流れない

> 「持続とは、未来へ食い込み、進むほど膨らんでいく過去の連続的な進行である。」
>
> —— アンリ・ベルクソン，[『創造的進化』](https://dhspriory.org/kenny/PhilTexts/Bergson/CreativeEvolution.htm)

24 fps は一本の物差しにすぎない。観客が感じる時間は、呼吸、沈黙、語尾、記憶、フレーム内部の変化から生まれる。ベルクソンは、この生きられた時間を「持続」と呼んだ。

ナレーションはまず実際の音声になり、その後、区間ごとに書き起こされる。字幕は文字数から秒数を推測せず、最終音声の単語タイムスタンプに従う。ショットの長さも、声、動作、素材密度から計算し直す。変化のない長い画面はモーション監査が拾い、部分運動、構図変化、代替素材、インサートで呼吸を取り戻す。

ローカル音声系には、Apple Silicon の Qwen3-TTS MLX、Edge TTS の軽量経路、faster-whisper の区間書き起こし、音文照合、最終音声ベースの字幕、ナレーション・音楽・映像のクロスプラットフォーム混合が含まれる。

編集卓に残す一行：**文字数で時間を推測した字幕は、いつか声を裏切る。**

## 第三幕：歴史の概念について

### ——アーカイブは一閃する。編集はその指紋をつかむ

> 「過去の真の像は、さっと過ぎ去る。」
>
> —— ヴァルター・ベンヤミン，[「歴史の概念について」V](https://www.textlog.de/benjamin/abhandlungen/ueber-den-begriff-der-geschichte)

アーカイブは、かつて起きた世界に映画を固定する。生成画像は、抽象的な思想に夢を見る場所を与える。編集は両者の異なる重さを保つ。一方は「本当に起きたのか」に答え、もう一方は「この思想はどんな姿を持つのか」と問う。

一枚の絵はポスターには足りる。編集には足りない。編集卓で最も高価なものは、第二の選択肢がないことだ。

絵コンテ承認後、素材キューは完成映像に必要な量のおよそ三倍を計画する。主素材、別構図、人物認識ショット、細部、トランジション、テクスチャ、変化過程、救済用インサートを個別に用意する。各アセットと変種は独立して生成され、人物、レンズ、光、材質の連続性を同じ系列のなかで守る。

```bash
python3 scripts/build_asset_queue.py --project /absolute/path/to/film-build
```

Codex 内蔵の画像生成が、各アセットを一枚ずつ生成し、確認し、プロジェクトへ保存する。

## 第四幕：シネマ 1 / シネマ 2

### ——運動は接続し、時間は残像を残す

ドゥルーズは「運動イメージ」と「時間イメージ」によって、映画が知覚をどう組織するかを考えた。運動は行為、因果、空間をつなぐ。時間は逡巡、記憶、亀裂をそのまま現れさせる。次のショットへ明確に進む場面もあれば、観客にもう一秒だけ留まってもらう場面もある。

素材中心の編集は人物、歴史、証拠を担う。Canvas2D は文字と情報を動かす。Three.js は奥行きと持続空間を必要とする場面へ入る。ハイブリッド作品は、章ごとに自らの文法を変えられる。

完成映像に加えて、完全なナレーション、脚本、絵コンテ、最終タイムライン、証拠台帳、素材候補、出典検証、書き起こし監査、SRT、メディア品質検査、編集可能な工程が残る。

## インストール

```bash
git clone https://github.com/mycyg/aletheia.git \
  ~/.codex/skills/aletheia
```

Codex を再起動し、自然言語または Skill 名で呼び出す。

```text
Use $aletheia to turn this article into a four-minute documentary.
Research the evidence, offer three directions, and stop after the complete narration
and shot-by-shot storyboard for my approval. After approval, create abundant visual
options, use a local narrator, transcribe every segment, edit, render, and run final QC.
```

## Sample：*The River Remembered Every Name*

[`examples/minimal-documentary`](examples/minimal-documentary) は、絵コンテ承認後、素材量産の直前で保存された最小ドキュメンタリー工程だ。創作方針、証拠台帳、絵コンテの改訂と承認、最終タイムライン契約、展開可能な画像生成キューを収録する。

```bash
python3 scripts/validate_project.py \
  --project examples/minimal-documentary --stage plan

python3 scripts/build_asset_queue.py \
  --project examples/minimal-documentary --replace
```

## 新規プロジェクト

```bash
python3 scripts/init_film_project.py \
  --title "The River Remembered Every Name" \
  --output /absolute/path/to/film-build \
  --duration 240 \
  --format documentary \
  --renderer hybrid
```

## ローカル音声・ASR・字幕

```bash
python3 -m venv .asr-venv
.asr-venv/bin/pip install -r requirements-asr.txt
.asr-venv/bin/python scripts/audit_narration.py \
  --project /absolute/path/to/film-build --model small
```

Apple Silicon では `requirements-tts-mlx.txt` を導入し、`generate_qwen3_voice.py --mode samples` で合成参照音声を選び、`--mode generate` で全ナレーションを生成する。

## 段階別検証

```bash
python3 scripts/validate_project.py --project /path/to/project --stage plan
python3 scripts/validate_project.py --project /path/to/project --stage assets
python3 scripts/validate_project.py --project /path/to/project --stage audio
python3 scripts/audit_motion.py --project /path/to/project
python3 scripts/validate_project.py --project /path/to/project --stage rendered
```

基本要件は Python 3.10+、ffmpeg/ffprobe、Codex Agent、内蔵画像生成。Node.js、Three.js、faster-whisper、MLX/Qwen3-TTS、Swift/AVFoundation、Suno は制作経路に応じて選択する。

## 終章：第二の執筆

文章は思想に最初の形を与える。映画はそれを光、声、証拠、待つ時間へ通す。戻ってきた思想は、もうひとつの生命を得ている。

## License

[MIT](LICENSE)

作者：程晓光｜WeChat 公式アカウント：杨与光的日常
