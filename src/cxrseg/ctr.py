"""Cardiothoracic ratio (CTR) — GEOMETRIC measurement, NOT a diagnosis.

CTR ≈ maximal transverse cardiac width / maximal internal thoracic width.
Here both are approximated as the widest horizontal extent of the heart mask and
the combined-lung mask respectively.

⚠️ Non-diagnostic: a reference band (~0.50 on PA) may be shown for context only.
AP view and rotation inflate CTR — always report the view and stratify by it.

⚠️ M2 will add rigorous numeric tests on synthetic lung+heart masks and a
geometric-consistency check against JSRT gold hearts (see PROGRESS/VERIFICATION).
This module is provided now so the package structure is complete.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class CTRResult:
    ctr: float
    cardiac_width: int
    thoracic_width: int
    note: str = "Geometric measurement only — NOT diagnostic."


def _max_horizontal_width(mask: np.ndarray) -> int:
    """Widest run of foreground across any single row (max col extent per row)."""
    mask = np.asarray(mask) > 0
    if not mask.any():
        return 0
    cols = np.where(mask.any(axis=0))[0]  # any-row column extent is a simpler proxy
    # per-row extent, then take the max row width
    widths = []
    rows = np.where(mask.any(axis=1))[0]
    for r in rows:
        c = np.where(mask[r])[0]
        widths.append(int(c.max() - c.min() + 1))
    return int(max(widths)) if widths else int(cols.max() - cols.min() + 1)


def cardiothoracic_ratio(lung_mask: np.ndarray, heart_mask: np.ndarray) -> CTRResult:
    """Compute a geometric CTR from a combined-lung mask and a heart mask.

    Returns ``CTRResult`` with ``ctr = 0.0`` if the thoracic width is zero.
    """
    cardiac = _max_horizontal_width(heart_mask)
    thoracic = _max_horizontal_width(lung_mask)
    ctr = (cardiac / thoracic) if thoracic > 0 else 0.0
    return CTRResult(ctr=ctr, cardiac_width=cardiac, thoracic_width=thoracic)
