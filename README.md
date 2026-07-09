# CXR-Seg — Chest X-ray Lung & Heart Segmentation (browser demo)

> ⚠️ **Research / teaching demo — NOT a diagnostic tool, and not for any clinical decision.**

**🔗 Live demo: https://pulmo-trace.vercel.app** · **🔒 Privacy: the image never leaves your device — segmentation runs entirely in your browser.**

Anatomical segmentation of the **lung fields (left + right) and heart** on a chest X-ray, with a geometric **cardiothoracic ratio (CTR)** computed from the masks. The model is a **zero-training (Tier 0)** baseline that runs in your browser via ONNX Runtime Web.

**The point of this project isn't accuracy — it's honest evidence.**

---

## The moat: honest evidence, not a score

Most medical-imaging AI is never externally validated. This project does the rigorous parts:

- **External validation (the trustworthy anchor):** tested on **JSRT**, an independent set with **human gold** masks — lung Dice **0.856**, heart Dice **0.918** (zero training).
- **Internal baseline:** vs CheXmask **silver** labels, with **patient-level** splitting and **bootstrap 95% CIs** (lung 0.835, heart 0.851).
- **Fairness / subgroups:** PA > AP; no difference between nodule and non-nodule cases.
- **Failure analysis:** errors are systematic, concentrated at the retrocardiac/mediastinal border and the costophrenic angle — not random.
- **CTR vs gold:** MAE 0.028, r 0.90 (geometric measurement, non-diagnostic).
- **Honesty:** silver ≠ gold is disclosed, plus a **CLAIM 2024** self-assessment and a **model card**.

| Setting | Reference | Lung Dice | Heart Dice |
|---|---|---|---|
| Internal (NIH, n=200) | CheXmask silver | 0.835 [0.826–0.843] | 0.851 [0.837–0.865] |
| **External (JSRT, n=246)** | **SCR gold (human)** | **0.856** [0.853–0.858] | **0.918** [0.915–0.923] |

📄 Evidence docs: [evaluation report](web/evaluation_report.md) · [model card](web/MODEL_CARD.md) · [CLAIM 2024 checklist](web/CLAIM_checklist.md)

---

## Privacy / architecture

- **The image never leaves the device:** inference runs fully client-side (ONNX Runtime Web in a Web Worker) — nothing is uploaded or stored.
- **Model:** TorchXRayVision pretrained anatomical segmentation (PSPNet, ChestX-Det), exported to ONNX (fp32) and hosted on Hugging Face, fetched by the browser at runtime.

## Repository structure

```
web/          Browser demo (index.html + vercel.json), evidence docs, figures, samples
src/cxrseg/   Research Python: patient-level split / RLE / metrics / CTR / inference
tests/        pytest (TDD for deterministic logic; patient-level leakage regression test)
CREDITS.md    Data & model licenses     DISCLAIMER.md    Non-diagnostic disclaimer
```

## Run locally

```bash
# Web demo (needs an http server — file:// won't work)
cd web && python -m http.server 8000   # open http://localhost:8000

# Python research code + tests
pip install -r requirements.txt
pytest -q
```

## Data & model licenses

- **NIH ChestX-ray14** (images; no restrictions + attribution) · **CheXmask v0.4** (internal silver masks, **CC BY 4.0**, Gaggion et al. 2024) · **JSRT + SCR** (external gold) · **TorchXRayVision** (model, Apache-2.0).
- See [`CREDITS.md`](CREDITS.md).

## License

- **Code: MIT** (see [`LICENSE`](LICENSE)).
- Datasets and the pretrained model are governed by their own licenses — see `CREDITS.md`.

---

_This is a research/teaching demo. It is not a medical device and must not be used for clinical decisions._
