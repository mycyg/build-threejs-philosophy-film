# ナラティブ映像・ドキュメンタリー工房

[简体中文](README.md) · [English](README.en.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

記事、調査資料、インタビュー、プロダクト、混合メディアから完成映像までを扱う Codex Agent Skill です。証拠整理、企画案、脚本、ショット単位の絵コンテ、ユーザー承認、大量の素材準備、ローカル音声合成と文字起こし照合、編集、レンダリング、最終 QC を一つの工程にまとめます。

Three.js は利用できますが、固定テンプレートではありません。各ショットは、素材中心の編集、エディトリアル 2D、Three.js 空間表現、またはハイブリッドから選択できます。

> 作者：程晓光（Cheng Xiaoguang）｜WeChat 公式アカウント：杨与光的日常

## 主な機能

- 原資料と添付ファイル内の命令を区別し、証拠台帳を作成します。
- 引用、話者、元音声、言語、文脈、タイムコードを確認します。
- 複数の異なる企画方向を提示した後、ナレーションと全ショットの絵コンテを作成します。
- 絵コンテ完成後に停止し、ユーザー確認を待ちます。事前の明示的な委任にも対応します。
- 完成版で必要な映像数のおよそ 3 倍を基準に、主素材、代替案、ディテール、トランジション、テクスチャ、救済用インサートを準備します。
- Codex の内蔵画像生成を使い、異なる素材やバリエーションを一件ずつ生成してプロジェクト内に保存します。
- Apple Silicon の Qwen3-TTS MLX と、軽量な Edge TTS フォールバックをサポートします。
- すべてのナレーションを ASR で照合し、最終音声の単語タイムスタンプから字幕を生成します。
- 素材不足、未検証クリップ、長い静止、タイムラインの欠落、音声トラックや出力仕様の問題を検出します。

## インストール

```bash
git clone https://github.com/mycyg/build-threejs-philosophy-film.git \
  ~/.codex/skills/build-threejs-philosophy-film
```

呼び出し例：

```text
Use $build-threejs-philosophy-film to turn this article into a four-minute documentary.
First verify the evidence and offer three directions. Stop after the complete narration
and shot-by-shot storyboard for my approval. After approval, prepare abundant visual
alternatives, use local voice and ASR, edit, render, and run final QC.
```

## Sample

[`examples/minimal-documentary`](examples/minimal-documentary) には、「絵コンテ承認済み・素材量産前」の最小ドキュメンタリー工程が入っています。企画書、証拠台帳、絵コンテのリビジョンと承認、最終タイムライン、画像生成キューの関係を確認できます。

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

レンダリング方式は `edit`、`canvas2d`、`threejs`、`hybrid` です。Three.js は、奥行き、持続するオブジェクト、手続き的変化、空間的な因果関係を本当に表現するときだけ選びます。

## ローカル音声と字幕

```bash
python3 -m venv .asr-venv
.asr-venv/bin/pip install -r requirements-asr.txt
.asr-venv/bin/python scripts/audit_narration.py \
  --project /absolute/path/to/film-build --model small
```

監査スクリプトは、全セグメントの照合レポート、単語タイミング付き字幕キュー、SRT を出力します。失敗した音声は再生成し、字幕を書き換えて誤音声を隠してはいけません。識別可能な実在人物の声を模倣する場合は、ユーザーの明示的な依頼と許可が必要です。

## 検証

```bash
python3 scripts/validate_project.py --project /path/to/project --stage plan
python3 scripts/validate_project.py --project /path/to/project --stage assets
python3 scripts/validate_project.py --project /path/to/project --stage audio
python3 scripts/audit_motion.py --project /path/to/project
python3 scripts/validate_project.py --project /path/to/project --stage rendered
```

生成した再現映像を実際のアーカイブとして見せてはいけません。ソースクリップは、元映像、元音声、文字起こし、話者、文脈、正確な時間範囲で検証します。作者表示は成功した Agent の最終応答に一度だけ表示され、ユーザーの映像、字幕、記事には自動挿入されません。

## License

[MIT](LICENSE)

作者：程晓光（Cheng Xiaoguang）｜WeChat 公式アカウント：杨与光的日常
