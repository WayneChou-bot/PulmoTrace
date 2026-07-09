"""Tier 0 zero-training inference — TorchXRayVision anatomical segmentation.

Primary Tier 0 baseline (decision B, 2026-07-09): TorchXRayVision's pretrained
PSPNet (trained on ChestX-Det) segments 14 anatomical structures automatically,
runs on CPU, and directly outputs Left Lung / Right Lung / Heart — exactly what
CTR needs. It is source-independent from CheXmask (HybridGNet), so evaluating one
against the other is not circular.

This wrapper keeps torch / torchxrayvision as *lazy* imports so the deterministic
modules (splits, rle) and their tests never require heavy deps.

NOT a diagnostic tool. See DISCLAIMER.md.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

LUNG_HEART_TARGETS = ("Left Lung", "Right Lung", "Heart")


@dataclass
class SegResult:
    """Per-structure probability maps and thresholded binary masks (H, W)."""

    targets: list[str]
    probs: dict[str, np.ndarray]
    masks: dict[str, np.ndarray]

    @property
    def lung(self) -> np.ndarray:
        return ((self.masks["Left Lung"] + self.masks["Right Lung"]) > 0).astype(np.uint8)

    @property
    def heart(self) -> np.ndarray:
        return self.masks["Heart"]


def load_seg_model():
    """Load the pretrained TorchXRayVision anatomical segmentation model.

    Weights download on first use (model only, ~tens of MB — NOT the dataset).
    """
    import torchxrayvision as xrv

    model = xrv.baseline_models.chestx_det.PSPNet()
    model.eval()
    return model


def preprocess(image: np.ndarray, size: int = 512) -> np.ndarray:
    """Prepare a 2-D grayscale X-ray for the model.

    Returns a ``(1, 1, size, size)`` float32 array normalized to xrv's
    ``[-1024, 1024]`` range.
    """
    import torchxrayvision as xrv

    img = np.asarray(image).astype(np.float32)
    if img.ndim == 3:  # collapse RGB → grayscale
        img = img.mean(axis=2)
    img = xrv.datasets.normalize(img, maxval=255)  # → [-1024, 1024]
    img = img[None, ...]  # add channel dim → (1, H, W)

    transform = xrv.datasets.XRayResizer(size)
    img = transform(img)
    return img[None, ...].astype(np.float32)  # add batch dim → (1, 1, size, size)


def segment(model, image: np.ndarray, *, size: int = 512, threshold: float = 0.5) -> SegResult:
    """Run segmentation and return probability maps + binary masks per structure."""
    import torch

    batch = torch.from_numpy(preprocess(image, size=size))
    with torch.no_grad():
        logits = model(batch)
        probs = torch.sigmoid(logits)[0].cpu().numpy()  # (14, size, size)

    targets = list(model.targets)
    prob_maps = {t: probs[i] for i, t in enumerate(targets)}
    masks = {t: (prob_maps[t] >= threshold).astype(np.uint8) for t in targets}
    return SegResult(targets=targets, probs=prob_maps, masks=masks)
