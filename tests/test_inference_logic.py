"""Tests for the torch-free logic in inference.py.

The heavy deps (torch, torchxrayvision) are lazily imported inside functions, so
the module imports and SegResult logic are testable without them. The real model
smoke test lives in scripts/smoke_infer.py (run on a machine with torch).
"""
import importlib

import numpy as np

from cxrseg.inference import SegResult, LUNG_HEART_TARGETS


def test_module_imports_without_torch():
    # Lazy imports → importing the module must not require torch/xrv.
    mod = importlib.import_module("cxrseg.inference")
    assert hasattr(mod, "segment")
    assert hasattr(mod, "load_seg_model")
    assert LUNG_HEART_TARGETS == ("Left Lung", "Right Lung", "Heart")


def _fake_result():
    z = np.zeros((8, 8), dtype=np.uint8)
    left = z.copy()
    left[2:6, 1:3] = 1
    right = z.copy()
    right[2:6, 5:7] = 1
    heart = z.copy()
    heart[3:6, 3:5] = 1
    masks = {"Left Lung": left, "Right Lung": right, "Heart": heart}
    probs = {k: v.astype(float) for k, v in masks.items()}
    return SegResult(targets=list(masks), probs=probs, masks=masks)


def test_lung_is_union_of_left_and_right():
    res = _fake_result()
    expected = ((res.masks["Left Lung"] + res.masks["Right Lung"]) > 0).astype(np.uint8)
    assert np.array_equal(res.lung, expected)
    assert res.lung.sum() == res.masks["Left Lung"].sum() + res.masks["Right Lung"].sum()


def test_heart_property():
    res = _fake_result()
    assert np.array_equal(res.heart, res.masks["Heart"])


def test_ctr_from_seg_result_is_computable():
    from cxrseg.ctr import cardiothoracic_ratio

    res = _fake_result()
    out = cardiothoracic_ratio(res.lung, res.heart)
    assert 0.0 < out.ctr <= 1.0
