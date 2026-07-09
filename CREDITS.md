# 資料來源與授權 / Credits & Licenses

> 授權乾淨是本專案紅線之一。以下為 v1 使用的資料與其授權;**CheXpert / MIMIC / VinDr / CANDID-PTX 衍生子集一律不碰**。

## 影像與內部標註(乾淨鏈)

- **NIH ChestX-ray14** — 影像來源(內部)。112,120 張、30,805 位病患,含 patient ID。公開可下載。
  - Wang, X. et al. *ChestX-ray8: Hospital-scale Chest X-ray Database...* CVPR 2017. 來源:美國 NIH Clinical Center。
  - https://openaccess.thecvf.com/content_cvpr_2017/html/Wang_ChestX-ray8_Hospital-Scale_Chest_CVPR_2017_paper.html
- **CheXmask Database**(本專案使用 **v0.4**,亦可用 v1.0.0)— 內部分割 mask(左右肺 + 心臟),**僅使用 NIH(ChestX-ray8)衍生子集**。
  - **授權:CC BY 4.0**(✅ v0.3 / v0.4 / v1.0.0 皆為 CC BY 4.0;⚠️ **僅 v0.1 / v0.2 為 CC BY-NC-SA 禁商用 —— 不用**)。
  - ⚠️ 若透過 Kaggle 第三方轉存取得:Kaggle 頁面可能誤標「CC0」——**以原始 CC BY 4.0 為準,務必標註來源**(第三方無權改授權)。
  - 標註為 **HybridGNet 自動生成的 silver 標註**,附 **Dice RCA** 品質分,**非人工 gold**。官方建議:**只用 `Dice RCA (Mean) ≥ 0.7`** 的 mask。
  - 托管於 PhysioNet(Open Access;下載需免費帳號 + 接受授權);**只含 mask(RLE),不含影像**。
  - **資料集引用**:Gaggion, N., Mosquera, C., Aineseder, M., Mansilla, L., Milone, D., & Ferrante, E. (2024). *CheXmask Database: a large-scale dataset of anatomical segmentation masks for chest x-ray images* (version 0.4). PhysioNet. https://doi.org/10.13026/pgag-by42 (最新 v1.0.0:https://doi.org/10.13026/6eky-y831)
  - **原始論文**:Gaggion, N. et al. *CheXmask: a large-scale dataset of anatomical segmentation masks for multi-center chest x-ray images.* Scientific Data 11 (2024). https://www.nature.com/articles/s41597-024-03358-1 ｜ arXiv:2307.03293 https://arxiv.org/abs/2307.03293
  - **方法(HybridGNet)**:Gaggion et al., IEEE TMI 2022;ISBI 2023。官方 repo:https://github.com/ngaggion/CheXmask-Database
  - **PhysioNet 平台引用**:Goldberger, A. et al. (2000). *Circulation* 101(23):e215–e220.

## 外部驗證(gold 人工標註)

- **JSRT + SCR** — 外部驗證(**肺 + 心臟**,人工標註)。JSRT 247 張;SCR 提供左右肺、心臟、鎖骨邊界。
  - 唯一能外部驗證**心臟 + CTR** 的 gold 集。
  - Shiraishi et al. (JSRT, 2000);van Ginneken et al. (SCR, *Med Image Anal* 2006)。研究/教學用途。
- **Montgomery County + Shenzhen** — 外部驗證(**肺**,人工標註)。Montgomery 138 張、Shenzhen 662 張;雙來源。
  - Jaeger et al. (2014);NLM/NIH 公開,研究可用。

## 模型

- **TorchXRayVision**(Tier 0 首選)— 預訓練解剖分割 PSPNet(ChestX-Det),自動輸出左右肺、心臟等 14 結構。
  - Cohen, J.P. et al. *TorchXRayVision: A library of chest X-ray datasets and models.* MIDL 2022. https://github.com/mlmed/torchxrayvision
  - 與 CheXmask(HybridGNet)來源獨立,評估不循環。
- **Medical-SAM3 / MedSAM3**(選配對照)— SAM3 系列可提示醫療分割,權重 2026-01 釋出。

## 使用規則

- 標註來源 + 作者 + **版本號**(CheXmask 標 v1.0.0)。
- 內部只用 NIH+CheXmask v1.0.0 NIH 衍生子集;外部只用 JSRT/Montgomery/Shenzhen。
- 不下載全量影像到本機;資料留 Kaggle 掛載。
