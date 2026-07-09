# 免責聲明 / Disclaimer

## 中文

**本專案為研究 / 教學用途的技術 demo,非診斷工具,不可用於任何臨床決策。**

- 本工具對胸部 X 光進行**解剖結構分割**(肺野、心臟),並由分割結果**幾何計算**心胸比(CTR)。
- **CTR 為純幾何量測,非診斷**;不代表、不等同臨床測量,亦不用於判斷任何疾病。
- 本工具**不偵測、不宣稱偵測任何疾病或病灶**。
- 內部評估所用的 CheXmask 標註為**模型自動生成的 silver 標註(非人工 gold)**;分數反映與另一模型的一致性,非臨床正確性。
- 效能**不保證**跨醫院、機型或人群泛化;外部驗證的掉幅會如實報告。
- 請勿將本工具或其輸出用於實際醫療照護。

## English

**This project is a research / educational technical demo. It is NOT a diagnostic tool and must NOT be used for any clinical decision-making.**

- It performs **anatomical segmentation** (lung fields, heart) on chest X-rays and computes a **geometric** cardiothoracic ratio (CTR) from the masks.
- **CTR is a purely geometric measurement, not a diagnosis**, and does not equal a clinical measurement.
- It does **not** detect, and does not claim to detect, any disease or lesion.
- Reference masks (CheXmask) are **model-generated silver labels, not human gold standard**; scores reflect agreement with another model, not clinical correctness.
- Performance is **not guaranteed** to generalize across hospitals, devices, or populations; external-validation performance drops are reported honestly.
- Do not use this tool or its outputs in real medical care.
