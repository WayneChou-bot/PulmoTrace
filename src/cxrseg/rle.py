"""Run-length encoding / decoding for CheXmask masks.

CheXmask distributes lung/heart masks as run-length-encoded strings plus the
image Height/Width. This module matches CheXmask's **official** convention
(``DataPostprocessing/utils.get_mask_from_RLE``), verified 2026-07-09 against the
upstream repo:

  * **1-indexed** ``start length start length`` pairs.
  * **row-major (C order)** flatten/reshape.

``test_rle.py`` includes a byte-for-byte parity test against a re-implementation
of the official decoder. The ``order`` argument is retained for generality but
**CheXmask decoding must use the default ``"C"``**.

Deterministic logic → covered by unit tests (TDD).
"""
from __future__ import annotations

import numpy as np


def rle_encode(mask, order: str = "C") -> str:
    """Encode a 2-D binary mask to a run-length string.

    Returns 1-indexed ``start length ...`` pairs. Empty mask → ``""``.
    Default ``order="C"`` (row-major) matches CheXmask.
    """
    pixels = np.asarray(mask, dtype=np.uint8).flatten(order=order)
    padded = np.concatenate([[0], pixels, [0]])
    changes = np.where(padded[1:] != padded[:-1])[0] + 1
    runs = changes.copy()
    runs[1::2] = runs[1::2] - runs[0::2]  # convert end positions → lengths
    return " ".join(str(int(x)) for x in runs)


def rle_decode(rle, shape, order: str = "C") -> np.ndarray:
    """Decode a run-length string to a 2-D ``uint8`` binary mask of ``shape``.

    Default ``order="C"`` (row-major, 1-indexed) matches CheXmask's official
    ``get_mask_from_RLE``. A missing / empty / ``-1`` RLE yields an all-zero mask
    (some CheXmask rows have no annotation for a structure).
    """
    h, w = shape
    flat = np.zeros(h * w, dtype=np.uint8)

    if rle is None:
        return flat.reshape(shape, order=order)
    s = str(rle).strip()
    if s in ("", "nan", "-1", "None"):
        return flat.reshape(shape, order=order)

    nums = np.asarray(s.split(), dtype=np.int64)
    if nums.size % 2 != 0:
        raise ValueError("RLE must contain an even number of integers")
    starts = nums[0::2] - 1  # 1-indexed → 0-indexed
    lengths = nums[1::2]
    for start, length in zip(starts, lengths):
        flat[start : start + length] = 1
    return flat.reshape(shape, order=order)
