"""M0 smoke test — run Tier 0 segmentation on ONE chest X-ray (CPU, local).

Run this on your Windows laptop (where torch installs fine). It proves the
"本機推論通" milestone: load TorchXRayVision, segment lung+heart, compute a
geometric CTR, and save an overlay.

    pip install -r requirements.txt
    python scripts/smoke_infer.py path/to/chest_xray.png

⚠️ NON-DIAGNOSTIC. Research/teaching demo only. See DISCLAIMER.md.
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cxrseg.inference import load_seg_model, segment, LUNG_HEART_TARGETS  # noqa: E402
from cxrseg.ctr import cardiothoracic_ratio  # noqa: E402


def load_image(path: str) -> np.ndarray:
    from skimage import io as skio

    img = skio.imread(path)
    return img


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("image", help="path to a chest X-ray (png/jpg)")
    ap.add_argument("--out", default="outputs/smoke_overlay.png")
    ap.add_argument("--threshold", type=float, default=0.5)
    args = ap.parse_args()

    print("Loading TorchXRayVision anatomical segmentation model (weights download on first use)...")
    model = load_seg_model()
    print("Targets:", list(model.targets))

    img = load_image(args.image)
    res = segment(model, img, threshold=args.threshold)

    for t in LUNG_HEART_TARGETS:
        print(f"  {t:>10}: mask pixels = {int(res.masks[t].sum())}, shape = {res.masks[t].shape}")

    ctr = cardiothoracic_ratio(res.lung, res.heart)
    print(f"CTR (geometric, NON-diagnostic): {ctr.ctr:.3f} "
          f"(cardiac {ctr.cardiac_width}px / thoracic {ctr.thoracic_width}px)")

    # save overlay
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        base = res.probs["Left Lung"]  # any channel just for canvas size
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(np.zeros_like(base), cmap="gray")
        ax.imshow(np.ma.masked_where(res.lung == 0, res.lung), alpha=0.4, cmap="Blues")
        ax.imshow(np.ma.masked_where(res.heart == 0, res.heart), alpha=0.5, cmap="Reds")
        ax.set_title("CXR-Seg Tier 0 — NON-DIAGNOSTIC demo", fontsize=10)
        ax.text(0.5, -0.06, "Research/teaching only. CTR is a geometric measurement, not a diagnosis.",
                transform=ax.transAxes, ha="center", va="top", fontsize=7, color="crimson")
        ax.axis("off")
        fig.savefig(args.out, dpi=120, bbox_inches="tight")
        print(f"Saved overlay → {args.out}")
    except Exception as e:  # noqa: BLE001
        print(f"(overlay skipped: {e})")

    print("\nOK — Tier 0 inference pipeline ran end-to-end.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
