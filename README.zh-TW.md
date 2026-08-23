# ALETHEIA

### 讓文章穿過時間

[简体中文](README.md) · [English](README.en.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

**開源 Codex 文章轉影片 Skill｜AI 紀錄片、敘事影片與完整影片製作工作流**

ALETHEIA 協助 Codex 快速把文章、部落格、論文、研究資料、訪談、產品文件和混合素材轉成影片。流程涵蓋資料核驗、創意方向、腳本、逐鏡分鏡、使用者確認、AI 批量生圖、本地配音、ASR 字幕校對、剪輯、Three.js / Canvas2D 渲染、配樂混音與成片品管，可用於紀錄片、影片論文、哲學短片、產品影片及 YouTube / Bilibili 內容製作。

> 「技術的本質絕不是什麼技術性的東西。」
>
> —— 馬丁・海德格，[〈技術的追問〉](https://www.beyng.com/pages/de/GA07/GA07.007.html)

古希臘語 `Aletheia`（ἀλήθεια）通常譯作「真理」；到了海德格那裡，它被重新追問為「解蔽」：被遮住的事物，重新從陰影裡顯現。

一篇文章抵達螢幕時，會失去紙上的安穩。句子要經歷聲音，論證要經受鏡頭，判斷要接受證據的凝視。影片由此成為第二次寫作。

它把原稿送進時間，讓材料長成一部真正能看的影片。證據、腳本、逐鏡分鏡、素材、聲音、字幕與最終剪輯，都留在同一套可追溯工程裡。

**作者：程曉光｜公眾號：楊與光的日常**

## 序章：技術的追問

### ——引擎不該握有審美的牧杖

海德格把技術理解為一種「解蔽」：它規定事物如何向我們顯現。渲染器同樣如此。預設套用 Three.js，久而久之，文章會被壓成粒子、卡片、深色空間與同一種勻速運鏡；工具悄悄變成了框架。

ALETHEIA 保留四條路線。選擇權屬於題材，也屬於每一個鏡頭。

| 路線 | 它讓什麼顯現 |
|---|---|
| `edit` | 訪談、檔案、原始影片、截圖與文獻自身的力量 |
| `canvas2d` | 文字、圖表、批註、地圖、時間線與編輯型運動 |
| `threejs` | 深度、持續物體、程序化變化與空間因果 |
| `hybrid` | 紀錄片證據與空間化視覺之間的張力 |

Three.js 仍在工具箱裡，需要空間時再讓它出場。影片的視覺語法從文章內部生長，不接受單一模板的統治。

## 第一幕：邏輯哲學論

### ——命題進入圖像，論證接受鏡頭的審判

> 「命題是現實的一幅圖畫。」
>
> —— 路德維希・維根斯坦，[《邏輯哲學論》4.01](https://moenarch.github.io/wittgenstein-tractatus-logico-philosophicus/Satz%204.html)

維根斯坦所說的「圖畫」，關乎命題與事實共享的邏輯形式。搬到剪輯台上，一句話也應當找到自己的可見形式：主張找到證據，情緒找到動作，抽象概念找到事件，引文找到出處，人物原聲找到準確的時間碼。

工程先建立證據帳本，再提出彼此真正有差異的創意方向。旁白與逐鏡分鏡完成後，製作停在確認點。分鏡是一份時間契約；鏡頭尚未獲得同意，昂貴的生成、下載、配音和渲染便沒有理由先行。

### 製作閉環

1. 匯入文章、附件、網頁、訪談、影片和程式碼，梳理事實與論點。
2. 建立證據帳本，把主張、引文、人物、原聲和來源逐項綁定。
3. 提出 2–3 個敘事方向，確認影片的思想、語氣和視覺母題。
4. 寫完整旁白、腳本與逐鏡分鏡。
5. **等待使用者確認分鏡。**
6. 展開素材佇列，大量生成、抓取、篩選並登記候選素材。
7. 生成配音，以本地 ASR 逐段轉寫，依最終音訊製作詞級字幕。
8. 為每個鏡頭選擇剪輯、Canvas2D、Three.js 或混合路線。
9. 先完成代表性片段，再推進全片、配樂與混音。
10. 檢查字幕、音文、長靜幀、鏡頭邊界、媒體參數與最終封裝。

## 第二幕：創造進化

### ——時間從來不按幀率流動

> 「綿延，是過去不斷侵入未來、並在前行中持續膨脹的過程。」
>
> —— 亨利・柏格森，[《創造進化》](https://dhspriory.org/kenny/PhilTexts/Bergson/CreativeEvolution.htm)

每秒 24 幀只是一把尺。影片裡真正被感受到的時間，來自呼吸、停頓、句尾、記憶與畫面內部的變化。柏格森稱這種被生活出來的時間為「綿延」。

旁白先成為真實音訊，隨後接受逐段轉寫。字幕跟隨最終聲音的詞級時間戳，不靠字數猜測節奏。鏡頭時長也會回到聲音、動作和素材密度上重新計算。長時間停在同一張圖上的鏡頭會被運動審計捕獲，隨後透過局部變化、構圖推進、替補素材或插鏡獲得新的呼吸。

本地聲音鏈路包含 Qwen3-TTS MLX、Edge TTS 回退路線、faster-whisper 逐段轉寫、音文相似度檢查、最終音訊字幕與跨平台混音。

一句可供剪輯台記住的話：**字幕若靠字數猜時間，聲音遲早會背叛畫面。**

## 第三幕：歷史哲學論綱

### ——檔案一閃而過，剪輯要抓住它留下的指紋

> 「過去的真實圖像，一閃即逝。」
>
> —— 華特・班雅明，[〈論歷史的概念〉第五節](https://www.textlog.de/benjamin/abhandlungen/ueber-den-begriff-der-geschichte)

檔案負責把影片釘在曾經發生過的世界裡；生成畫面替抽象概念造夢。剪輯保留這兩種圖像各自的重量：前者回答「它真的發生過嗎」，後者回答「這種思想看起來像什麼」。

一張圖只夠做海報，不夠剪片。剪輯台上最昂貴的東西，常常是沒有第二個選擇。

分鏡確認後，素材佇列會按鏡頭展開，預設準備約為成片所需三倍的候選量：主畫面、替補構圖、人物辨識鏡頭、細節、轉場、紋理、變化過程與救場插鏡各自占位。每張資產與變體獨立生成，人物、光線、鏡頭和材質在同組內保持連續。

```bash
python3 scripts/build_asset_queue.py --project /absolute/path/to/film-build
```

Codex 內建生圖能力會逐張生成、檢查並保存工程素材。

## 第四幕：電影 1 / 電影 2

### ——運動負責連接，時間負責留下餘波

德勒茲用「運動—影像」與「時間—影像」討論電影如何組織感知。前者讓動作、因果與空間彼此接續；後者容許停頓、記憶與裂縫自己顯形。一個鏡頭有時需要清楚地走向下一個鏡頭，有時只需讓觀眾在它面前多停留一秒。

素材主導的剪輯處理人物、歷史與證據；Canvas2D 負責文字和資訊的運動；Three.js 處理真正需要深度與持續空間的段落；混合路線容許一部片在不同章節改變自身語法。

成片之外，工程會留下完整旁白、腳本、逐鏡分鏡、最終時間軸、證據帳本、素材主選與替補、來源核驗記錄、轉寫審計、SRT、媒體質檢結果和可編輯工程。

## 安裝

```bash
git clone https://github.com/mycyg/aletheia.git \
  ~/.codex/skills/aletheia
```

重新開啟 Codex 後，以自然語言呼叫，或直接寫出 Skill 名稱：

```text
Use $aletheia 把這篇文章製作成四分鐘中文紀錄片。
先整理證據，給我三個方向，完成旁白與逐鏡分鏡後等我確認。
確認後充分生成候選畫面，並用本地模型配音和逐段轉寫校對。
```

## Sample：河流記得每一個名字

[`examples/minimal-documentary`](examples/minimal-documentary) 保存著一部停在「分鏡已確認、素材即將量產」時刻的最小紀錄片工程，包含創意方向、證據帳本、分鏡修訂與確認、最終時間軸契約和可展開的生圖佇列。

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

## 本地配音、轉寫與字幕

```bash
python3 -m venv .asr-venv
.asr-venv/bin/pip install -r requirements-asr.txt
.asr-venv/bin/python scripts/audit_narration.py \
  --project /absolute/path/to/film-build --model small
```

Apple Silicon 可安裝 `requirements-tts-mlx.txt`，先用 `generate_qwen3_voice.py --mode samples` 選擇合成參考聲線，再以 `--mode generate` 完成全篇旁白。

## 分階段校驗

```bash
python3 scripts/validate_project.py --project /path/to/project --stage plan
python3 scripts/validate_project.py --project /path/to/project --stage assets
python3 scripts/validate_project.py --project /path/to/project --stage audio
python3 scripts/audit_motion.py --project /path/to/project
python3 scripts/validate_project.py --project /path/to/project --stage rendered
```

基礎依賴為 Python 3.10+、ffmpeg/ffprobe、Codex Agent 與內建圖片生成能力。Node.js、Three.js、faster-whisper、MLX/Qwen3-TTS、Swift/AVFoundation 與 Suno 依製作路線選用。

## 尾聲：第二次寫作

文章完成思想的第一次定形。影片讓它經過光線、聲音、證據與等待，回來時已經擁有另一種生命。

## License

[MIT](LICENSE)

作者：程曉光｜公眾號：楊與光的日常
