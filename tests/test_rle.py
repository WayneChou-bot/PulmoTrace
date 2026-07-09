"""Tests for CheXmask RLE encode/decode (self-consistent, Kaggle convention)."""
import numpy as np
import pytest

from cxrseg.rle import rle_encode, rle_decode


def test_roundtrip_random_masks_fortran_order():
    rng = np.random.default_rng(0)
    for _ in range(20):
        h, w = int(rng.integers(4, 40)), int(rng.integers(4, 40))
        mask = (rng.random((h, w)) > 0.5).astype(np.uint8)
        decoded = rle_decode(rle_encode(mask, order="F"), (h, w), order="F")
        assert np.array_equal(mask, decoded)


def test_roundtrip_c_order():
    rng = np.random.default_rng(1)
    mask = (rng.random((16, 9)) > 0.4).astype(np.uint8)
    decoded = rle_decode(rle_encode(mask, order="C"), (16, 9), order="C")
    assert np.array_equal(mask, decoded)


def test_known_small_example_column_major():
    # 3x3, single foreground pixel at row1,col1 (0-indexed).
    mask = np.zeros((3, 3), dtype=np.uint8)
    mask[1, 1] = 1
    # Column-major flatten index of (r=1,c=1) = c*H + r = 1*3 + 1 = 4 → 1-indexed 5.
    assert rle_encode(mask, order="F") == "5 1"
    assert np.array_equal(rle_decode("5 1", (3, 3), order="F"), mask)


def test_full_and_empty():
    full = np.ones((5, 5), dtype=np.uint8)
    assert rle_decode(rle_encode(full), (5, 5)).sum() == 25
    empty = np.zeros((5, 5), dtype=np.uint8)
    assert rle_encode(empty) == ""


def test_missing_rle_yields_zero_mask():
    for missing in (None, "", "nan", "-1", "None"):
        m = rle_decode(missing, (7, 4))
        assert m.shape == (7, 4)
        assert m.sum() == 0


def test_odd_length_rle_raises():
    with pytest.raises(ValueError):
        rle_decode("1 2 3", (4, 4))


def test_decode_matches_manual_fill():
    # two runs on a 4x4 column-major array
    rle = "1 2 7 3"  # pixels 1-2 and 7-9 (1-indexed) set
    flat = np.zeros(16, dtype=np.uint8)
    flat[0:2] = 1
    flat[6:9] = 1
    expected = flat.reshape((4, 4), order="F")
    assert np.array_equal(rle_decode(rle, (4, 4), order="F"), expected)


def _official_get_mask_from_RLE(rle, height, width):
    """Byte-for-byte re-implementation of CheXmask's official decoder
    (ngaggion/CheXmask-Database, DataPostprocessing/utils.get_mask_from_RLE)."""
    runs = np.array([int(x) for x in rle.split()])
    starts = runs[::2]
    lengths = runs[1::2]
    mask = np.zeros((height * width), dtype=np.uint8)
    for start, length in zip(starts, lengths):
        start -= 1
        end = start + length
        mask[start:end] = 255
    return mask.reshape((height, width))


def test_parity_with_official_chexmask_decoder():
    """Our default decode (C order, 1-indexed) must match CheXmask exactly."""
    rng = np.random.default_rng(2024)
    for _ in range(30):
        h, w = int(rng.integers(8, 64)), int(rng.integers(8, 64))
        mask = (rng.random((h, w)) > 0.5).astype(np.uint8)
        rle = rle_encode(mask)  # default order="C"
        ours = rle_decode(rle, (h, w))  # default order="C" → 0/1
        official = (_official_get_mask_from_RLE(rle, h, w) > 0).astype(np.uint8)
        assert np.array_equal(ours, official)


def test_chexmask_sample_row_shapes():
    """Decode the real CheXmask sample row (from the mounted v0.4 CSV head)."""
    # Heart RLE prefix from image 00025787_047.png, 1024x1024.
    heart_rle = "448036 9 449048 27 450064 41 451086 48 452107 55"
    m = rle_decode(heart_rle, (1024, 1024))  # C order
    assert m.shape == (1024, 1024)
    assert m.sum() == 9 + 27 + 41 + 48 + 55  # total run length
