"""Patient-level train/val/test splitting.

⚠️ THE most fatal pitfall in medical CV is data leakage from splitting by
*image* instead of by *patient*: multiple X-rays of the same patient landing in
both train and test lets the model memorize patients and produces unrealistically
high Dice that collapses under external validation.

This module guarantees **no patient crosses splits**, and ships an assertion
(`assert_no_patient_leakage`) used as a regression test that must never regress.

Deterministic logic → covered by unit tests (TDD).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Split:
    """Integer index arrays into the original per-image sequence."""

    train: np.ndarray
    val: np.ndarray
    test: np.ndarray

    def sizes(self) -> tuple[int, int, int]:
        return len(self.train), len(self.val), len(self.test)


def nih_patient_id_from_filename(filename: str) -> str:
    """NIH ChestX-ray14 filenames look like ``00000001_000.png`` where the part
    before the underscore is the patient ID and the rest is the follow-up index.

    Returns the patient ID as a string.
    """
    stem = str(filename).rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    stem = stem.split(".", 1)[0]
    return stem.split("_", 1)[0]


def patient_level_split(
    patient_ids,
    *,
    test_size: float = 0.2,
    val_size: float = 0.1,
    seed: int = 42,
) -> Split:
    """Split image indices into train/val/test so that **no patient appears in
    more than one split**.

    Parameters
    ----------
    patient_ids : sequence of length ``n_images``
        ``patient_ids[i]`` is the patient owning image ``i``.
    test_size, val_size : float in [0, 1)
        Fractions of *patients* (not images) assigned to test / val. Must sum < 1.
    seed : int
        Seed for reproducible patient shuffling.

    Returns
    -------
    Split
        Index arrays into the input sequence. The set of patients in train, val
        and test are pairwise disjoint by construction.
    """
    patient_ids = np.asarray(patient_ids)
    n = len(patient_ids)
    if n == 0:
        empty = np.array([], dtype=int)
        return Split(empty, empty.copy(), empty.copy())
    if not (0 <= test_size < 1 and 0 <= val_size < 1 and (test_size + val_size) < 1):
        raise ValueError("test_size and val_size must be in [0, 1) and sum to < 1")

    unique = np.unique(patient_ids)
    n_pat = len(unique)
    rng = np.random.default_rng(seed)
    shuffled = unique[rng.permutation(n_pat)]

    n_test = int(round(n_pat * test_size))
    n_val = int(round(n_pat * val_size))
    n_test = min(n_test, n_pat)
    n_val = min(n_val, n_pat - n_test)

    test_pat = set(shuffled[:n_test].tolist())
    val_pat = set(shuffled[n_test : n_test + n_val].tolist())

    idx = np.arange(n)
    in_test = np.array([p in test_pat for p in patient_ids])
    in_val = np.array([p in val_pat for p in patient_ids])
    in_train = ~(in_test | in_val)

    return Split(idx[in_train], idx[in_val], idx[in_test])


def assert_no_patient_leakage(patient_ids, split: Split) -> None:
    """Raise AssertionError if any patient appears in more than one split.

    This is the regression guard for the most fatal pitfall. Call it after every
    split; wire it into CI so it can never silently regress.
    """
    patient_ids = np.asarray(patient_ids)
    train_pat = set(patient_ids[split.train].tolist())
    val_pat = set(patient_ids[split.val].tolist())
    test_pat = set(patient_ids[split.test].tolist())

    assert train_pat.isdisjoint(val_pat), "patient leakage between train and val"
    assert train_pat.isdisjoint(test_pat), "patient leakage between train and test"
    assert val_pat.isdisjoint(test_pat), "patient leakage between val and test"
