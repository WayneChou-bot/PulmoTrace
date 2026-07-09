"""Light sanity checks for CTR geometry.

NOTE: these are smoke-level only. Rigorous numeric verification on synthetic
lung+heart masks and geometric consistency vs JSRT gold hearts is an M2
deliverable (see VERIFICATION.md — CTR remains ⬜ until then).
"""
import numpy as np

from cxrseg.ctr import cardiothoracic_ratio, _max_horizontal_width


def test_width_of_solid_rectangle():
    mask = np.zeros((10, 20), dtype=np.uint8)
    mask[2:8, 3:13] = 1  # width = 10
    assert _max_horizontal_width(mask) == 10


def test_ctr_half_when_heart_half_of_thorax():
    thorax = np.zeros((20, 40), dtype=np.uint8)
    thorax[:, 5:35] = 1  # thoracic width 30
    heart = np.zeros((20, 40), dtype=np.uint8)
    heart[8:12, 10:25] = 1  # cardiac width 15
    res = cardiothoracic_ratio(thorax, heart)
    assert res.cardiac_width == 15
    assert res.thoracic_width == 30
    assert abs(res.ctr - 0.5) < 1e-9


def test_zero_thorax_gives_zero_ctr():
    empty = np.zeros((5, 5), dtype=np.uint8)
    heart = np.zeros((5, 5), dtype=np.uint8)
    heart[2, 1:4] = 1
    assert cardiothoracic_ratio(empty, heart).ctr == 0.0
