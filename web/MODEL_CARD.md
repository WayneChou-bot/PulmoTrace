# Model Card — CXR-Seg (Tier 0)

> **⚠️ NON-DIAGNOSTIC. Research / teaching demo only. Must NOT be used for any clinical decision.** See `DISCLAIMER.md`.

## Overview
- **What it is:** a zero-training pipeline that segments **lung fields (left ∪ right) and heart** on a chest X-ray, and computes a **geometric** cardiothoracic ratio (CTR) from the masks.
- **Model:** TorchXRayVision anatomical segmentation (**PSPNet**, trained on ChestX-Det). Used **as-is, no fine-tuning** (Tier 0).
- **Version:** v1 (M0–M2). Date: 2026-07-09.
- **Author:** personal research/教學 project.

## Intended use
- **Intended:** education and methodology demonstration — how to build and, above all, **honestly evaluate** a medical-imaging segmentation demo (external validation, calibration of expectations, failure analysis, reporting standards).
- **NOT intended:** diagnosis, triage, screening, measurement for clinical care, or any real patient use. Not a medical device.
- **Users:** ML/medical-imaging learners and reviewers.

## Data
- **Images (internal):** NIH ChestX-ray14 (public). Patient-level split (no leakage).
- **Reference (internal):** CheXmask **v0.4** (CC BY 4.0) — **silver, model-generated (HybridGNet)**, filtered to RCA(Mean) ≥ 0.7.
- **External validation:** **JSRT** images + **SCR** human **gold** masks (lung + heart). JSRT is independent of the model's training data.
- **Licensing:** NIH public; CheXmask v0.4 CC BY 4.0 (attributed; NC v0.1/0.2 avoided); JSRT/SCR research-use. See `CREDITS.md`.

## Performance (agreement, not clinical accuracy)
| Setting | Reference | Lung Dice | Heart Dice |
|---|---|---|---|
| Internal (NIH, n=200) | CheXmask silver | 0.835 [0.826, 0.843] | 0.851 [0.837, 0.865] |
| **External (JSRT, n=246)** | **SCR gold (human)** | **0.856 [0.853, 0.858]** | **0.918 [0.915, 0.923]** |

- **CTR:** predicted vs gold — MAE 0.028, r 0.90, small systematic under-estimate (−0.026). Geometric only.
- **Subgroups:** PA (0.863) > AP (0.804) lung; nodule vs non-nodule ≈ equal.
- All figures with 95% bootstrap CIs; see `report/M1_baseline.md`.

## Limitations
- **Silver ≠ gold:** internal scores measure agreement with another model (HybridGNet), not correctness. Anchored by JSRT gold.
- **"Friendly" external set:** JSRT is clean PA, single scanner — likely optimistic vs portable/AP or other institutions (cf. AP subgroup drop). A second, harder external source is future work.
- **Systematic failure mode:** disagreement concentrates at the **retrocardiac/mediastinal border** and **costophrenic angle/lung base** (see failure gallery). Model tends to clip these regions.
- **CTR is geometric, non-diagnostic;** slightly under-estimates vs gold; not validated against clinical CTR; view (PA/AP) strongly affects it.
- **No training/uncertainty/calibration head** in v1 (Tier 0). No saliency (would be misleading in medicine).
- **Not evaluated** on pathology segmentation, other modalities, pediatric, or non-frontal views.

## Ethical & safety notes
- Non-diagnostic statement enforced in three places (app, repo, report).
- Uses only public, de-identified data with clean licensing.
- Not a substitute for radiologist interpretation.

## Reproducibility
- Repo: `src/cxrseg/` (+ pytest), `notebooks/` (Kaggle cells), `report/` (results + figures + CLAIM checklist).
- Reference standard: CLAIM 2024 self-assessment in `report/CLAIM_checklist.md`.
