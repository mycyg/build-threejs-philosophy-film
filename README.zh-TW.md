# 敘事影片與紀錄片工坊

[简体中文](README.md) · [English](README.en.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

一個面向 Codex Agent 的完整影片製作 Skill：從文章、研究資料、訪談、產品或混合素材出發，完成證據整理、創意方向、腳本、逐鏡分鏡、使用者確認、大量素材準備、配音與轉寫校對、剪輯渲染及成片質檢。

Three.js 仍受支援，但不再是固定模板。每個鏡頭可依功能選擇素材主導剪輯、編輯型 2D、Three.js 空間影像或混合路線。

> 作者：程曉光 ｜ 微信公眾號：杨与光的日常

## 主要能力

- 區分原始內容與附件中的指令，建立可追溯的證據帳本。
- 核對引文、訪談原聲、人物、語言、上下文與時間碼。
- 先提出不同創作方向，再撰寫完整旁白與逐鏡分鏡。
- 分鏡完成後暫停並等待確認；使用者也可預先授權連續執行。
- 預設準備約為成片所需三倍的候選素材，包含主畫面、替補、細節、轉場、紋理與救場插鏡。
- 使用 Codex 內建生圖能力逐張生成資產與變體，並保存到專案目錄。
- 支援 Apple Silicon 上的 Qwen3-TTS MLX，以及 Edge TTS 輕量備援。
- 逐段轉寫所有旁白，核對實際語音，並由最終音訊的詞級時間戳產生字幕。
- 檢查素材不足、未核驗片段、長時間靜幀、時間軸斷裂與輸出媒體問題。

## 安裝

```bash
git clone https://github.com/mycyg/build-threejs-philosophy-film.git \
  ~/.codex/skills/build-threejs-philosophy-film
```

呼叫範例：

```text
Use $build-threejs-philosophy-film 把這篇文章製作成四分鐘中文紀錄片。
先整理證據並提供三個方向，完成完整旁白與逐鏡分鏡後等我確認。
確認後充分生成候選素材，使用本地模型配音，逐段轉寫校對，再剪輯、渲染與質檢。
```

## Sample

[`examples/minimal-documentary`](examples/minimal-documentary) 是一個停在「分鏡已確認、尚未大量製作素材」階段的最小紀錄片工程，示範創意簡報、證據帳本、分鏡修訂與核准、時間軸，以及可展開的生圖佇列。

```bash
python3 scripts/validate_project.py \
  --project examples/minimal-documentary --stage plan

python3 scripts/build_asset_queue.py \
  --project examples/minimal-documentary --replace
```

## 新建工程

```bash
python3 scripts/init_film_project.py \
  --title "河流記得每一個名字" \
  --output /absolute/path/to/film-build \
  --duration 240 \
  --format documentary \
  --renderer hybrid
```

渲染路線包括 `edit`、`canvas2d`、`threejs` 與 `hybrid`。Three.js 只有在深度、持續物件、程序化變化或空間因果確實有意義時才應使用。

## 本地配音與字幕

```bash
python3 -m venv .asr-venv
.asr-venv/bin/pip install -r requirements-asr.txt
.asr-venv/bin/python scripts/audit_narration.py \
  --project /absolute/path/to/film-build --model small
```

腳本會輸出旁白核驗報告、詞級字幕提示與 SRT。任何失敗片段都應重新生成，不能用修改字幕掩蓋錯誤語音。可辨識真人聲線的模仿必須取得使用者明確請求與授權。

## 分階段校驗

```bash
python3 scripts/validate_project.py --project /path/to/project --stage plan
python3 scripts/validate_project.py --project /path/to/project --stage assets
python3 scripts/validate_project.py --project /path/to/project --stage audio
python3 scripts/audit_motion.py --project /path/to/project
python3 scripts/validate_project.py --project /path/to/project --stage rendered
```

生成重建畫面不得偽裝成真實檔案。來源影片必須以原畫面、原音、轉寫、人物、上下文與精確時間範圍核驗。作者署名只會在成功交付後的 Agent 對話回覆中出現一次，不會自動放入使用者影片、字幕或文章。

## 授權

[MIT](LICENSE)

作者：程曉光 ｜ 微信公眾號：杨与光的日常
