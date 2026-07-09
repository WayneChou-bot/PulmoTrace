# CXR-Seg — 胸部 X 光肺野與心臟解剖分割(瀏覽器 demo)

> ⚠️ **非診斷用途,不可用於任何臨床決策。** 這是研究 / 教學技術 demo。
> **Research / teaching demo — NOT a diagnostic tool, not for any clinical decision.**

**🔗 Live demo:** _(部署後補上 Vercel 網址)_ · **🔒 隱私:影像不上傳,全程於瀏覽器本機運算。**

胸部 X 光的**肺野(左右肺)+ 心臟**解剖分割,並由分割結果計算幾何**心胸比(CTR)**。
模型為 **零訓練(Tier 0)** 基線,在你的瀏覽器裡以 ONNX Runtime Web 執行。
這個專案的重點不是「準」,而是 **誠實的佐證**。

---

## 護城河 = 誠實佐證(不是分數)

多數醫療影像 AI 很少做外部驗證。本專案把該做的做齊:

- **外部驗證(最可信的錨點):** 在**獨立、人工 gold** 的 JSRT 上測 —— 肺 Dice **0.856**、心 Dice **0.918**(zero-training)。
- **內部基線:** 對 CheXmask **silver** 標註,patient-level 切分 + bootstrap 95% CI(肺 0.835、心 0.851)。
- **子群/公平性:** PA > AP;結節 vs 非結節無差異。
- **失敗分析:** 失敗集中在心臟後方/縱膈交界與肋膈角/肺底(非隨機)。
- **CTR 對 gold 一致性:** MAE 0.028、r 0.90(幾何量測、非診斷)。
- **silver ≠ gold 誠實揭露、CLAIM 2024 自評、model card。**

📄 佐證文件:[evaluation report](web/evaluation_report.md) · [model card](web/MODEL_CARD.md) · [CLAIM 2024 checklist](web/CLAIM_checklist.md)

---

## 隱私 / 架構

- **影像不離開裝置:** 分割完全在瀏覽器端執行(ONNX Runtime Web + Web Worker),不上傳伺服器、不儲存。
- 模型:TorchXRayVision 預訓練解剖分割(PSPNet, ChestX-Det),匯出成 ONNX,以 fp32 於 Hugging Face 上託管、由瀏覽器載入。

## 專案結構

```
web/          瀏覽器 demo(index.html + vercel.json)、佐證文件、圖、範例
src/cxrseg/   研究用 Python:patient-level 切分 / RLE / metrics / CTR / 推論
tests/        pytest(確定性邏輯 TDD;patient-level 切分回歸測試等)
CREDITS.md    資料與模型授權   DISCLAIMER.md   免責聲明
```

## 本機執行

```bash
# 網頁 demo(需 http server,不能直接開 file://)
cd web && python -m http.server 8000   # 開 http://localhost:8000

# Python 研究程式碼 + 測試
pip install -r requirements.txt
pytest -q
```

## 資料與模型授權

- **NIH ChestX-ray14**(影像,no restrictions + 標註)· **CheXmask v0.4**(內部 silver mask,**CC BY 4.0**,Gaggion et al. 2024)· **JSRT + SCR**(外部 gold)· **TorchXRayVision**(模型)。
- 詳見 [`CREDITS.md`](CREDITS.md)。

## 授權 / License

- **程式碼:MIT**(見 [`LICENSE`](LICENSE))。
- 資料集與預訓練模型各自的授權以其原始來源為準(見 `CREDITS.md`)。

---

_This is a research/teaching demo. It is not a medical device and must not be used for clinical decisions._
