# CLAIM 2024 Checklist — CXR-Seg (self-assessment)

> **Reference:** Tejani AS, Klontzas ME, Gatti AA, Mongan JT, Moy L, Park SH, Kahn CE Jr; CLAIM 2024 Update Panel. *Checklist for Artificial Intelligence in Medical Imaging (CLAIM): 2024 Update.* Radiol Artif Intell. 2024;6(4):e240300. PMID 38809149. https://pubs.rsna.org/doi/10.1148/ryai.240300
>
> This is a **self-assessment for a research/teaching demo** (not a submitted study). Items are mapped to CLAIM 2024's sections; **exact item numbering/wording should be verified against the official checklist PDF**. Response key: **Y** = addressed · **P** = partial · **NA** = not applicable (with reason). "Where" points to files in this repo.
>
> ⚠️ **This project is NOT a diagnostic tool** (see `DISCLAIMER.md`). Several publication-only items (trial registration, funding, prospective IRB) are legitimately NA.

## Title & Abstract
| # | Item | Resp | Where / note |
|---|---|---|---|
| 1 | Identify as AI/ML study; name technology category | Y | README: "anatomical segmentation… PSPNet (deep learning)"; report title |
| 2 | Structured summary (design, methods, results, conclusions) | Y | `report/M1_baseline.md` header + section summaries |

## Introduction
| # | Item | Resp | Where / note |
|---|---|---|---|
| 3 | Scientific/clinical background & rationale | Y | `files/med_SPEC.md` §0–§1; README |
| 4 | Study objectives / hypotheses | Y | SPEC §1 scope; objective = zero-training anatomical seg + honest evidence |

## Methods — Study design
| # | Item | Resp | Where / note |
|---|---|---|---|
| 5 | Prospective vs retrospective | Y | Retrospective, public datasets |
| 6 | Study goal (feasibility / model creation / …) | Y | Feasibility/教學 demo; **not** diagnostic — DISCLAIMER, SPEC §0.1 |

## Methods — Data
| # | Item | Resp | Where / note |
|---|---|---|---|
| 7 | Data sources | Y | CREDITS: NIH ChestX-ray14; CheXmask v0.4; JSRT+SCR |
| 8 | Inclusion/exclusion criteria | Y | Internal: RCA(Mean) ≥ 0.7; external: JSRT (`jsrt-*`) |
| 9 | Data pre-processing | Y | `src/cxrseg/inference.py` (normalize, resize 512); `rle.py` |
| 10 | Selection of data subsets | Y | patient-level test split (seed 42); n=200 internal, 246 external |
| 11 | Definition of data elements | Y | CREDITS; CheXmask schema (RLE + RCA) documented |
| 12 | De-identification | NA | Public, already de-identified; no PHI handled |
| 13 | Handling of missing data | Y | Missing/empty RLE → zero mask (`rle.py`); images without masks excluded |
| — | **(2024) Data provenance & licensing** | Y | CREDITS: NIH public, CheXmask **v0.4 CC BY 4.0** (not NC v0.1/2), JSRT/SCR research-use; Kaggle "CC0" mislabel flagged |

## Methods — Ground truth (reference standard)
| # | Item | Resp | Where / note |
|---|---|---|---|
| 14 | Definition of reference standard | Y | Internal = CheXmask **silver** (HybridGNet); external = JSRT/SCR **gold (human)** |
| 15 | Rationale for reference standard | Y | report M1 §setup + limitations; silver-vs-gold discussed explicitly |
| 16 | Source of annotations | Y | CheXmask HybridGNet auto; SCR = van Ginneken human |
| 17 | Annotation tooling | Y | RLE masks (CheXmask); SCR contour masks |
| 18 | Inter/intra-rater variability | P | Not re-measured; CheXmask ships **RCA** quality scores (used for filtering + RCA↔Dice analysis) |

## Methods — Data partitions
| # | Item | Resp | Where / note |
|---|---|---|---|
| 19 | Intended sample size & basis | P | Demo sample n=200 (internal) / 246 (external, full JSRT); not powered for a clinical claim |
| 20 | How partitioned (train/val/test) | Y | `src/cxrseg/splits.py`; zero training (Tier 0) so test = evaluation set |
| 21 | **Partition level (leakage prevention)** | **Y** | **patient-level** split via NIH Patient ID; regression test `assert_no_patient_leakage` (11 tests green) |

## Methods — Model
| # | Item | Resp | Where / note |
|---|---|---|---|
| 22 | Model description | Y | TorchXRayVision PSPNet (ChestX-Det), 14 anatomical outputs; lung=L∪R, heart |
| 23 | Software/hardware/frameworks | Y | Python, PyTorch, torchxrayvision, MONAI-stack; CPU inference / Kaggle GPU T4 optional |
| 24 | Parameter initialization (pretraining/transfer) | Y | Pretrained weights, **zero fine-tuning** (Tier 0) |

## Methods — Training
| # | Item | Resp | Where / note |
|---|---|---|---|
| 25–28 | Training approach, hyperparameters, model selection, ensembling | NA | **Zero-training baseline** — no training/HPO/ensembling in v1. (Tier-1 fine-tuning is future work.) |

## Methods — Evaluation
| # | Item | Resp | Where / note |
|---|---|---|---|
| 29 | Performance metrics | Y | Dice, IoU (lung union + heart); geometric CTR |
| 30 | Statistical uncertainty | **Y** | **1000× bootstrap 95% CI** on all means |
| 31 | Robustness / sensitivity | Y | RCA↔Dice (r=0.51/0.57); subgroups (view PA/AP, nodule) |
| 32 | Explainability | P | Mask overlays; no saliency (flagged as potentially misleading in medicine — SPEC §6.5) |
| 33 | **External validation** | **Y** | **JSRT gold**, independent of model training; drop reported honestly (report M2) |
| — | **(2024) Fairness / subgroups** | Y | view (PA 0.863 > AP 0.804), nodule vs non-nodule (no effect) |
| — | **(2024) Compute cost** | P | ~20 min CPU / n=200; GPU optional — noted in report |

## Results
| # | Item | Resp | Where / note |
|---|---|---|---|
| 34 | Flow of cases | Y | report: 112,120→patient-level test→RCA≥0.7→n; JSRT n=246 |
| 35 | Case characteristics | Y | view distribution; JSRT nodule/non-nodule split |
| 36 | Performance with precision (CI) | Y | all metrics with 95% CI (report M1/M2) |
| 37 | **Failure analysis** | **Y** | failure gallery (worst 6, contour overlays + auto-observations); systematic retrocardiac/costophrenic failure mode |

## Discussion
| # | Item | Resp | Where / note |
|---|---|---|---|
| 38 | Limitations / bias / generalizability | **Y** | report: silver≠gold, JSRT is a "friendly" external set, silver-vs-gold reference change, AP worse, CTR under-estimate |
| 39 | Implications / future work | Y | Tier-1 fine-tune, 2nd harder external set, Hausdorff — SPEC backlog |

## Other information
| # | Item | Resp | Where / note |
|---|---|---|---|
| 40 | Registration | NA | Not a registered clinical study (demo) |
| 41 | Protocol access | Y | `files/med_SPEC.md` is the living protocol/spec |
| 42 | Funding / conflicts | NA | None; personal research/教學 project |
| — | **(2024) Model/data/code availability** | Y | Code in repo; datasets public (NIH/CheXmask/JSRT); per-image results CSVs |
| — | **(2024) Intended use & non-diagnostic statement** | **Y** | `DISCLAIMER.md` + app + report (three places) |

---

### Self-assessment summary
Addressed (Y): the substantive rigor items — **patient-level partitioning, uncertainty (CI), external validation on gold, failure analysis, subgroup/fairness, data provenance/licensing, limitations, non-diagnostic intended use**. Partial (P): inter-rater variability (RCA used instead), sample-size justification, explainability, compute reporting. NA: training/HPO (zero-training), de-identification (public data), registration/funding (demo). Items marked NA are documented with reasons — consistent with a zero-training research/teaching demo, not a clinical study.
